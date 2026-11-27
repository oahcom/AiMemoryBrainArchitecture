#!/usr/bin/env python3
"""Verify required ⊆ declared ⊆ produced for the governed check contexts.

The checker compares three independently sourced sets:

  required   live main branch protection payload:
             GET /repos/{owner}/{repo}/branches/{branch}
             .protection.required_status_checks.contexts
  declared   the fenced context list in PR-GOVERNANCE-001.md §7
  produced   job ids and job display names from every .yml/.yaml workflow

The contract is inclusion, not equality. Extra documented contexts are
permitted; every platform-required context must be documented, and every
documented context must be produced by a workflow job. No protected-context
snapshot is committed. The Administration-only /protection endpoint is not
used.

Exit codes:
    0  PASS        required ⊆ declared ⊆ produced
    1  VIOLATION   a required context is undocumented, a declared context is
                   unproduced, or the declaration contains duplicates
    2  INCOMPLETE  a required input cannot be read or evaluated

An unreadable platform payload is INCOMPLETE, never PASS and never a repository
VIOLATION. A network failure must not be mistaken for an empty required set.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

DOC_PATH = "14-ai-development/PR-GOVERNANCE-001.md"
MARKER = "<!-- declared-check-contexts"
WORKFLOWS = ".github/workflows"

# The branch whose protection payload is the protected side of the comparison.
REPO_SLUG = "oahcom/AiMemoryBrainArchitecture"
BRANCH = "main"
TIMEOUT_SECONDS = 20
DEFAULT_API = "https://api.github.com"

# A job id is a top-level key under `jobs:` (2-space indent). Its display name
# is a 4-space `name:` inside that block. GitHub reports the display name when
# present and the job id otherwise, so both are candidate contexts.
JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
JOB_NAME_RE = re.compile(r"^    name:\s*(.+?)\s*$")
FENCE_RE = re.compile(r"^```")

# GitHub reads both suffixes. Globbing `*.yml` alone left a `.yaml` workflow's
# jobs invisible to the produced side.
WORKFLOW_GLOBS = ("*.yml", "*.yaml")


def strip_yaml_comment(line: str) -> str:
    """Drop a trailing YAML comment, ignoring `#` inside quotes.

    A YAML comment starts at a `#` in column 0 or preceded by a space or tab, so
    `name: "Build #7"` keeps its `#` and `jobs:  # comment` loses its comment.
    Removing the comment is what lets the `jobs:` key and a commented job line
    be read as the structure they are.
    """
    quote = None
    for index, char in enumerate(line):
        if quote:
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "#" and (index == 0 or line[index - 1] in " \t"):
            return line[:index]
    return line


def strip_yaml_comments(text: str) -> str:
    """Strip every line's comment, keeping the line count unchanged."""
    return "\n".join(strip_yaml_comment(line) for line in text.splitlines())


def workflow_files(workflows_dir: Path) -> list[Path]:
    """Every workflow file, `.yml` and `.yaml` alike, in one sorted list."""
    paths = [
        path
        for pattern in WORKFLOW_GLOBS
        for path in workflows_dir.glob(pattern)
    ]
    return sorted(paths)


def declared_contexts(doc_text: str) -> list[str] | None:
    """The fenced block under the marker, one context per line. None if absent."""
    lines = doc_text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.lstrip().startswith(MARKER)),
        None,
    )
    if start is None:
        return None

    opening = next(
        (i for i in range(start, len(lines)) if FENCE_RE.match(lines[i])),
        None,
    )
    if opening is None:
        return None

    contexts = []
    for line in lines[opening + 1:]:
        if FENCE_RE.match(line):
            break
        name = line.strip()
        if name:
            contexts.append(name)
    return contexts or None


def produced_contexts(workflow_text: str) -> set[str]:
    """Job ids and job display names in one workflow file.

    Comments are stripped first, so a commented-out job line and a
    `jobs:  # comment` header cannot hide or invent a context.
    """
    found: set[str] = set()
    in_jobs = False
    current: str | None = None

    for line in strip_yaml_comments(workflow_text).splitlines():
        if not in_jobs:
            if line.rstrip() == "jobs:":
                in_jobs = True
            continue

        # Any column-0 key ends the jobs mapping.
        if line and not line[0].isspace() and not line.startswith("#"):
            break

        job_id = JOB_ID_RE.match(line)
        if job_id:
            current = job_id.group(1)
            found.add(current)
            continue

        job_name = JOB_NAME_RE.match(line)
        if job_name and current is not None:
            found.add(job_name.group(1).strip("'\""))

    return found


def fetch_protected_contexts(
    api: str | None = None,
    repo: str = REPO_SLUG,
    branch: str = BRANCH,
    timeout: int = TIMEOUT_SECONDS,
) -> list[str]:
    """The required contexts on `branch`, in payload order.

    Raises on any transport, status or shape failure. The caller turns that into
    INCOMPLETE; this function never returns a value it did not read.
    """
    base = api or os.environ.get("GITHUB_API_URL") or DEFAULT_API
    request = urllib.request.Request(
        f"{base.rstrip('/')}/repos/{repo}/branches/{branch}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "declared-check-contexts",
        },
    )
    # Optional, and only to raise the rate limit. Absence must not skip the
    # comparison: the endpoint is readable without it on a public repository.
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)

    contexts = payload["protection"]["required_status_checks"]["contexts"]
    if not isinstance(contexts, list) or not all(isinstance(c, str) for c in contexts):
        raise ValueError("protection.required_status_checks.contexts is not a list of strings")
    return contexts


def main(root: Path | None = None, protection: list[str] | None = None) -> int:
    """`protection` injects the protected side; None reads it from the platform."""
    root = Path(root or ".").resolve()
    doc = root / DOC_PATH

    if not doc.is_file():
        print(
            f"::error::INCOMPLETE: declaring document is absent: {DOC_PATH}",
            file=sys.stderr,
        )
        return 2

    contexts = declared_contexts(doc.read_text(encoding="utf-8"))
    if contexts is None:
        print(
            "::error::INCOMPLETE: no declared-context block found in "
            f"{DOC_PATH}; the condition cannot be read, so it cannot be verified",
            file=sys.stderr,
        )
        return 2

    workflows_dir = root / WORKFLOWS
    workflow_files_found = workflow_files(workflows_dir)
    if not workflow_files_found:
        print(
            f"::error::INCOMPLETE: no workflows under {WORKFLOWS}; "
            "no context can be shown to be produced",
            file=sys.stderr,
        )
        return 2

    produced: set[str] = set()
    for path in workflow_files_found:
        produced |= produced_contexts(path.read_text(encoding="utf-8"))

    unproduced = [context for context in contexts if context not in produced]

    if unproduced:
        for context in unproduced:
            print(
                f"::error::{DOC_PATH} declares required check context "
                f"{context!r}, but no job in {WORKFLOWS} produces it",
                file=sys.stderr,
            )
        print(
            f"DECLARED CHECK CONTEXTS: FAIL "
            f"({len(unproduced)} of {len(contexts)} unproduced)",
            file=sys.stderr,
        )
        return 1

    # A line listed twice is invisible to the set comparison below: the sets
    # still match, so a copy-paste that overwrote a missing context reads as
    # PASS. The duplication is itself the disagreement, so it fails on the list.
    duplicates = sorted({context for context in contexts if contexts.count(context) > 1})
    if duplicates:
        for context in duplicates:
            print(
                f"::error::{DOC_PATH} declares required check context "
                f"{context!r} more than once; the document no longer says what "
                "its author meant it to say",
                file=sys.stderr,
            )
        print(
            f"DECLARED CHECK CONTEXTS: FAIL (declared {len(contexts)}; "
            f"{len(duplicates)} duplicated)",
            file=sys.stderr,
        )
        return 1

    if protection is None:
        try:
            protection = fetch_protected_contexts()
        except Exception as error:  # noqa: BLE001 - every failure is INCOMPLETE
            print(
                "::error::INCOMPLETE: input "
                f"{REPO_SLUG}/branches/{BRANCH}.protection.required_status_checks.contexts "
                "could not be read: "
                f"{type(error).__name__}: {error}",
                file=sys.stderr,
            )
            return 2

    if protection is None:
        print(
            "::error::INCOMPLETE: input "
            f"{REPO_SLUG}/branches/{BRANCH}.protection.required_status_checks.contexts "
            "returned None; the required set is unavailable",
            file=sys.stderr,
        )
        return 2
    if not isinstance(protection, list) or not protection:
        print(
            "::error::INCOMPLETE: input "
            f"{REPO_SLUG}/branches/{BRANCH}.protection.required_status_checks.contexts "
            "is missing, empty, or not a list of required context strings",
            file=sys.stderr,
        )
        return 2
    if not all(isinstance(context, str) for context in protection):
        print(
            "::error::INCOMPLETE: input "
            f"{REPO_SLUG}/branches/{BRANCH}.protection.required_status_checks.contexts "
            "contains a non-string context",
            file=sys.stderr,
        )
        return 2

    required_not_declared = sorted(set(protection) - set(contexts))
    declared_not_produced = sorted(set(contexts) - produced)

    print(
        f"CONTEXT COUNTS: declared={len(contexts)} required={len(protection)} "
        f"produced={len(produced)}",
        file=sys.stderr,
    )
    print(f"required_not_declared={required_not_declared}", file=sys.stderr)
    print(f"declared_not_produced={declared_not_produced}", file=sys.stderr)

    violated = False
    for context in required_not_declared:
        print(
            f"::error::{BRANCH} requires {context!r}, but {DOC_PATH} does not "
            "declare it",
            file=sys.stderr,
        )
        violated = True
    for context in declared_not_produced:
        print(
            f"::error::{DOC_PATH} declares required check context "
            f"{context!r}, but no job in {WORKFLOWS} produces it",
            file=sys.stderr,
        )
        violated = True

    if violated:
        print("DECLARED CHECK CONTEXTS: VIOLATION", file=sys.stderr)
        return 1

    print(
        f"::notice::{len(contexts)} declared, {len(protection)} required, all produced",
        file=sys.stderr,
    )
    print("DECLARED CHECK CONTEXTS: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
