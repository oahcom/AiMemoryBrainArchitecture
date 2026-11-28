#!/usr/bin/env python3
"""Hold every platform-required check context to merge-queue wiring.

Three conditions, each silent when broken:

1. WIRING. Every context actually required by main branch protection must be
   produced by at least one workflow subscribing to
   `merge_group: types: [checks_requested]`.

   The governance declaration may contain additional produced contexts that are
   not platform-required. Those extra contexts are not merge gates and do not
   need merge_group subscriptions.

   `check_declared_check_contexts.py` verifies the relationship
   required ⊆ declared ⊆ produced. This checker verifies the separate
   event-wiring property for the actual required set. A context that only runs
   on `pull_request` is never reported on a queue candidate, so the queue
   silently loses that gate and no other check notices: #1453 dropped
   `merge_group` from document-management.yml this way and `GOV-DOC-002 metadata
   checks` left the queue with 15/16.

2. CONCURRENCY ISOLATION. document-management.yml is read-only and re-fetches
   the current target base, so it does not serialize across pull requests; it
   isolates by workflow, event type and pull-request number instead, with
   `github.ref_name` as the non-PR fallback (AID-2026-013, `0962fbdc5`).
   `cancel-in-progress: false` is required, `queue` must stay undeclared, and a
   target-branch selector (`pull_request.base.ref`, `merge_group.base_ref`,
   `github.ref` as a group key) must not come back.

3. COUNT. A workflow comment stating "<N> required contexts live in this file"
   must state the number of declared contexts that workflow actually produces.

Exit codes:
    0  PASS
    1  VIOLATION   a condition above is false
    2  INCOMPLETE  the declaration, the platform set, or a workflow is unreadable
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from check_declared_check_contexts import (
    DOC_PATH,
    WORKFLOWS,
    declared_contexts,
    fetch_protected_contexts,
    strip_yaml_comments,
    workflow_files,
)

ISOLATED_WORKFLOW = "document-management.yml"

JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
JOB_NAME_RE = re.compile(r"^    name:\s*(.+?)\s*$")
MERGE_GROUP_RE = re.compile(r"^\s+merge_group\s*:")
COUNT_CLAIM_RE = re.compile(r"^#\s*([A-Za-z]+|\d+)\s+required contexts?\b")

NUMBERS = {
    word: value
    for value, word in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve "
        "thirteen fourteen fifteen sixteen".split()
    )
}


def block(lines: list[str], header: str) -> tuple[int, int] | None:
    """Line range (1-based, inclusive header) of a top-level `header:` mapping."""
    for index, line in enumerate(lines):
        if line.rstrip() == header:
            end = index + 1
            while end < len(lines):
                candidate = lines[end]
                if candidate.strip() and not candidate[0].isspace():
                    break
                end += 1
            return index + 1, end
    return None


def job_contexts(text: str) -> dict[str, int]:
    """Job id and display name -> 1-based line number, comments stripped."""
    found: dict[str, int] = {}
    stripped = strip_yaml_comments(text).splitlines()
    bounds = block(stripped, "jobs:")
    if bounds is None:
        return found
    start, end = bounds
    current: str | None = None
    for offset in range(start, end):
        line = stripped[offset]
        job_id = JOB_ID_RE.match(line)
        if job_id:
            current = job_id.group(1)
            found.setdefault(current, offset + 1)
            continue
        job_name = JOB_NAME_RE.match(line)
        if job_name and current is not None:
            found.setdefault(job_name.group(1).strip("'\""), offset + 1)
    return found


def merge_group_subscription(text: str) -> tuple[int, bool] | None:
    """(line number, types include checks_requested) for `merge_group:` in `on:`.

    A `merge_group` key alone is not a subscription: `types: [some_other_event]`
    names an activity type GitHub does not emit for this event, so the workflow
    would never report on a queue candidate.
    """
    stripped = strip_yaml_comments(text).splitlines()
    bounds = block(stripped, "on:")
    if bounds is None:
        return None
    start, end = bounds
    for offset in range(start, end):
        match = MERGE_GROUP_RE.match(stripped[offset])
        if not match:
            continue
        indent = len(stripped[offset]) - len(stripped[offset].lstrip())
        types_ok = True
        for child in range(offset + 1, end):
            line = stripped[child]
            if not line.strip():
                continue
            child_indent = len(line) - len(line.lstrip())
            if child_indent <= indent:
                break
            if line.strip().startswith("types:"):
                value = line.split("types:", 1)[1].strip()
                items = re.findall(r"[A-Za-z_][\w-]*", value)
                types_ok = "checks_requested" in items
                break
        return offset + 1, types_ok
    return None


def concurrency_group_expression(stripped: list[str], start: int, end: int) -> str:
    """The `group:` value only, folded scalar or inline, comments already gone."""
    for offset in range(start, end):
        line = stripped[offset]
        if not re.match(r"^\s+group:", line):
            continue
        value = line.split("group:", 1)[1].strip()
        if value not in {">", ">-", "|", "|-", ""}:
            return value
        indent = len(line) - len(line.lstrip())
        parts = []
        for child in range(offset + 1, end):
            child_line = stripped[child]
            if not child_line.strip():
                continue
            if len(child_line) - len(child_line.lstrip()) <= indent:
                break
            parts.append(child_line.strip())
        return " ".join(parts)
    return ""


def count_claims(text: str) -> list[tuple[int, int]]:
    """(line number, claimed count) for every `<N> required contexts` comment."""
    claims = []
    for index, line in enumerate(text.splitlines()):
        match = COUNT_CLAIM_RE.match(line.strip())
        if not match:
            continue
        token = match.group(1).lower()
        if token.isdigit():
            claims.append((index + 1, int(token)))
        elif token in NUMBERS:
            claims.append((index + 1, NUMBERS[token]))
    return claims


def concurrency_isolation_violations(path: str, text: str) -> list[str]:
    """document-management.yml must isolate per workflow/event/PR (AID-2026-013)."""
    problems = []
    stripped = strip_yaml_comments(text).splitlines()
    bounds = block(stripped, "concurrency:")
    if bounds is None:
        return [f"::error::{path}: has no `concurrency:` block"]
    start, end = bounds
    body = "\n".join(stripped[start - 1:end])

    if not re.search(r"^\s*cancel-in-progress:\s*false\s*$", body, re.MULTILINE):
        problems.append(
            f"::error::{path}:{start}: concurrency must set `cancel-in-progress: false`"
        )

    # `queue: max` would turn per-PR isolation back into same-group queueing.
    if re.search(r"^\s*queue\s*:", body, re.MULTILINE):
        problems.append(
            f"::error::{path}:{start}: concurrency must not declare `queue`; "
            "per-PR/event isolation uses the default single-pending behaviour"
        )

    # The isolation tokens must be in the `group` expression itself: a token in
    # a neighbouring comment or a sibling key is not a grouping decision.
    group = concurrency_group_expression(stripped, start, end)
    for token in (
        "github.workflow",
        "github.event_name",
        "github.event.pull_request.number",
        "github.ref_name",
    ):
        if token not in group:
            problems.append(
                f"::error::{path}:{start}: the concurrency `group` must include "
                f"`{token}`; AID-2026-013 isolates by workflow, event and PR"
            )

    # `github.ref` is a prefix of `github.ref_name`, so a plain substring test
    # would flag the required fallback. Only a bare `github.ref` is forbidden.
    if re.search(r"github\.ref(?![\w])", group):
        problems.append(
            f"::error::{path}:{start}: the concurrency `group` must not key off "
            "the target branch via `github.ref`; AID-2026-013 isolates per PR"
        )
    for token in (
        "github.event.pull_request.base.ref",
        "github.event.merge_group.base_ref",
    ):
        if token in group:
            problems.append(
                f"::error::{path}:{start}: the concurrency `group` must not use "
                f"target-branch selector `{token}`; AID-2026-013 isolates per PR"
            )
    return problems


def main(
    root: Path | None = None,
    protection: list[str] | None = None,
) -> int:
    """
    Verify merge_group wiring for platform-required contexts only.

    The governance declaration may intentionally contain extra contexts
    that are produced by monitoring or reporting workflows but are not
    required by branch protection.

    The protected set is read live from:
        GET /repos/{repo}/branches/{branch}
        .protection.required_status_checks.contexts

    Exit codes:
        0 PASS
        1 VIOLATION
        2 INCOMPLETE
    """
    root = Path(root or ".").resolve()
    doc = root / DOC_PATH

    if not doc.is_file():
        print(
            f"::error::INCOMPLETE: declaring document is absent: {DOC_PATH}",
            file=sys.stderr,
        )
        return 2

    doc_text = doc.read_text(encoding="utf-8")
    declared = declared_contexts(doc_text)

    if declared is None:
        print(
            f"::error::INCOMPLETE: no declared-context block in {DOC_PATH}",
            file=sys.stderr,
        )
        return 2

    # Resolve the actual platform-required set. Never substitute the
    # declaration for an unreadable platform response.
    if protection is None:
        try:
            protection = fetch_protected_contexts()
        except Exception as error:  # noqa: BLE001
            print(
                "::error::INCOMPLETE: platform required contexts could "
                "not be read: "
                f"{type(error).__name__}: {error}",
                file=sys.stderr,
            )
            return 2

    if (
        not isinstance(protection, list)
        or not protection
        or not all(isinstance(context, str) and context for context in protection)
    ):
        print(
            "::error::INCOMPLETE: platform required contexts are "
            "missing, empty, or malformed",
            file=sys.stderr,
        )
        return 2

    if len(protection) != len(set(protection)):
        print(
            "::error::INCOMPLETE: platform required contexts contain "
            "duplicates; the authoritative set is ambiguous",
            file=sys.stderr,
        )
        return 2

    required = protection

    doc_lines = doc_text.splitlines()

    def doc_line(context: str) -> int:
        return next(
            (
                i + 1
                for i, line in enumerate(doc_lines)
                if line.strip() == context
            ),
            0,
        )

    workflows = workflow_files(root / WORKFLOWS)

    if not workflows:
        print(
            f"::error::INCOMPLETE: no workflows under {WORKFLOWS}",
            file=sys.stderr,
        )
        return 2

    produced: dict[
        str,
        list[tuple[str, int, tuple[int, bool] | None]],
    ] = {}

    violations: list[str] = []

    for path in workflows:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        subscription = merge_group_subscription(text)

        for context, line in job_contexts(text).items():
            produced.setdefault(context, []).append(
                (relative, line, subscription)
            )

        if path.name == ISOLATED_WORKFLOW:
            violations.extend(
                concurrency_isolation_violations(relative, text)
            )

        # Count comments remain tied to the complete declaration.
        # They are documentation claims, not the MG-01 required set.
        declared_here = [
            context
            for context in declared
            if any(
                source[0] == relative
                for source in produced.get(context, [])
            )
        ]

        for line, claimed in count_claims(text):
            if claimed != len(declared_here):
                violations.append(
                    f"::error::{relative}:{line}: the comment claims "
                    f"{claimed} required contexts, but this workflow "
                    f"produces {len(declared_here)} of the "
                    f"{len(declared)} declared in {DOC_PATH}"
                )

    # MG-01 applies exclusively to the live platform-required set.
    # Additional declared/produced contexts are not merge-queue gates
    # unless branch protection actually requires them.
    for context in required:
        sources = produced.get(context)
        where = f"{DOC_PATH}:{doc_line(context)}"

        if not sources:
            violations.append(
                f"::error::{where}: platform requires context "
                f"{context!r}, but no job under {WORKFLOWS} produces it"
            )
            continue

        # Multiple workflows may produce the same context. At least one
        # valid producer must subscribe to checks_requested.
        valid_source = next(
            (
                source
                for source in sources
                if source[2] is not None and source[2][1]
            ),
            None,
        )

        if valid_source is not None:
            continue

        path, line, subscription = sources[0]

        if subscription is None:
            violations.append(
                f"::error::{path}:{line}: produces platform-required "
                f"context {context!r} (declared at {where}) but the "
                "`on:` block has no `merge_group` entry; "
                "a merge-group candidate never reports this context"
            )
        else:
            violations.append(
                f"::error::{path}:{subscription[0]}: produces "
                f"platform-required context {context!r} "
                f"(declared at {where}) but its `merge_group` entry "
                "does not request `checks_requested`; "
                "the queue never schedules it"
            )

    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)

        print(
            "REQUIRED CONTEXT MERGE_GROUP WIRING: "
            f"FAIL ({len(violations)} violation(s))",
            file=sys.stderr,
        )
        return 1

    for context in required:
        path, line, subscription = next(
            source
            for source in produced[context]
            if source[2] is not None and source[2][1]
        )

        print(
            f"OK  {context}  {path}:{line}  "
            f"merge_group={path}:{subscription[0]} "
            "(checks_requested)",
            file=sys.stderr,
        )

    extra = sorted(set(declared) - set(required))

    print(
        f"PLATFORM REQUIRED CONTEXTS: {len(required)}",
        file=sys.stderr,
    )
    print(
        f"DECLARED BUT NOT PLATFORM-REQUIRED: {len(extra)}",
        file=sys.stderr,
    )

    for context in extra:
        print(
            f"INFO  {context}: declared and produced, "
            "but not currently required by branch protection; "
            "MG-01 merge_group wiring does not apply",
            file=sys.stderr,
        )

    print(
        "REQUIRED CONTEXT MERGE_GROUP WIRING: "
        f"PASS ({len(required)} platform-required contexts)",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
