#!/usr/bin/env python3
"""Structural requirement/work-item traceability checker.

The requirements registry is a non-authoritative index. GitHub Issues remain
the requirement authority. This checker does not assess semantic correctness.

The registry is deliberately restricted to JSON syntax, which is a valid
YAML subset. No PyYAML or third-party package is required.

Manifest parsing is deliberately narrow: only selected top-level scalar
values are read. Nested YAML is ignored. Unsupported or malformed input is
reported as indeterminate rather than silently interpreted.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, TextIO, Tuple


REGISTRY_PATH = Path("00-governance/requirements-registry.yaml")
INDEX_PATH = Path("14-ai-development/work-items/INDEX.md")
WORK_ITEMS_DIR = Path("14-ai-development/work-items")

REQUIREMENT_ID_RE = re.compile(r"^REQ-[0-9]{2,}$")
ISSUE_URL_RE = re.compile(
    r"^https://github\.com/[^/]+/[^/]+/issues/([1-9][0-9]*)$"
)
AID_LINK_RE = re.compile(
    r"\[\s*(AID-[0-9]{4}-[0-9]{3})\s*\]\(([^)]+/manifest\.yaml)\)"
)
ISSUE_NUMBER_RE = re.compile(r"#([1-9][0-9]*)")
REQ_REF_RE = re.compile(r"\bREQ-[0-9]{2,}\b")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")

STAGE_0_RECORD_TYPE = "STAGE_0_WORK_ITEM_REGISTRATION"

# Closed historical compatibility list. These records may use `aid:` instead
# of the normative `work_item_id:` key until their manifests are migrated.
LEGACY_AID_KEY_IDS = {
    "AID-2026-014",
    "AID-2026-023",
    "AID-2026-026",
}

MANIFEST_KEYS = {
    "work_item_id",
    "aid",
    "record_type",
    "tracking_issue",
    "base_commit_sha",
}


class CheckFailure(Exception):
    """A structural input or parse failure."""


class Reporter:
    def __init__(
        self,
        stream: TextIO,
        warning_stream: Optional[TextIO] = None,
    ) -> None:
        self.stream = stream
        self.warning_stream = warning_stream or stream
        self.errors = 0
        self.warnings = 0
        self.indeterminate = False
        self._error_item_number = 0

    def error(self, message: str, path: Optional[str] = None) -> None:
        self.errors += 1
        if path:
            self._error_item_number += 1
            # gate_ratchet.py --format paths strips the numbered prefix and
            # everything after " -> ", leaving only the stable repo path.
            self.stream.write(
                "{:03d}. {} -> ERROR {}\n".format(
                    self._error_item_number, path, message
                )
            )
        else:
            self.stream.write("ERROR " + message + "\n")

    def warn(self, message: str) -> None:
        self.warnings += 1
        self.warning_stream.write("WARN " + message + "\n")

    def unknown(self, message: str) -> None:
        self.warnings += 1
        self.indeterminate = True
        self.warning_stream.write("WARN " + message + "\n")


def parse_registry(path: Path) -> List[dict]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CheckFailure("cannot read registry: {}".format(exc)) from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CheckFailure(
            "registry must use the documented JSON-compatible YAML subset: "
            "{}".format(exc)
        ) from exc

    if not isinstance(data, dict):
        raise CheckFailure("registry root must be an object")

    requirements = data.get("requirements")
    if not isinstance(requirements, list):
        raise CheckFailure("registry requirements must be an array")

    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            raise CheckFailure(
                "registry requirements[{}] must be an object".format(index)
            )

    return requirements


def parse_manifest_top_level(path: Path) -> Dict[str, Optional[str]]:
    """Read selected top-level YAML scalars without a YAML dependency."""
    found: Dict[str, Optional[str]] = {}

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise CheckFailure(
            "cannot read manifest {}: {}".format(path, exc)
        ) from exc

    for line_number, line in enumerate(lines, 1):
        if not line or line.lstrip().startswith("#"):
            continue

        if line[0].isspace():
            continue

        match = re.match(
            r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$",
            line,
        )
        if not match:
            if ":" in line:
                raise CheckFailure(
                    "unsupported top-level YAML syntax at {}:{}".format(
                        path, line_number
                    )
                )
            continue

        key, value = match.group(1), match.group(2)
        if key not in MANIFEST_KEYS:
            continue

        if key in found:
            raise CheckFailure(
                "duplicate top-level manifest key {} in {}".format(key, path)
            )

        if value is None or value == "" or value in (
            "null", "Null", "NULL", "~"
        ):
            found[key] = None
            continue

        value = value.strip()

        if value.startswith('"'):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError as exc:
                raise CheckFailure(
                    "invalid double-quoted scalar {}:{}: {}".format(
                        path, line_number, exc
                    )
                ) from exc

            if not isinstance(parsed, str):
                raise CheckFailure(
                    "expected string scalar for {} in {}".format(key, path)
                )

            found[key] = parsed

        elif value.startswith("'"):
            if len(value) < 2 or not value.endswith("'"):
                raise CheckFailure(
                    "invalid single-quoted scalar {}:{}".format(
                        path, line_number
                    )
                )
            found[key] = value[1:-1].replace("''", "'")

        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].strip()

            if value in ("null", "Null", "NULL", "~", ""):
                found[key] = None
            else:
                if value.startswith(("[", "{", "!", "&", "*", "|", ">")):
                    raise CheckFailure(
                        "unsupported scalar form for {} in {}".format(
                            key, path
                        )
                    )
                found[key] = value

    return found


def safe_repo_path(root: Path, relative: str) -> Optional[Path]:
    """Resolve a repository-relative path and reject traversal/symlink escape."""
    if not isinstance(relative, str) or not relative:
        return None

    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None

    resolved_root = root.resolve()
    resolved = (root / candidate).resolve()

    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None

    return resolved


def safe_work_item_manifest_path(
    repository_root: Path,
    manifest_relative_to_work_items: str,
) -> Optional[Path]:
    """Resolve an INDEX link relative to WORK_ITEMS_DIR."""
    work_items_root = repository_root / WORK_ITEMS_DIR

    if not isinstance(manifest_relative_to_work_items, str):
        return None

    relative = Path(manifest_relative_to_work_items)
    if relative.is_absolute() or ".." in relative.parts:
        return None

    resolved_work_items_root = work_items_root.resolve()
    resolved_manifest = (work_items_root / relative).resolve()

    try:
        resolved_manifest.relative_to(resolved_work_items_root)
    except ValueError:
        return None

    return resolved_manifest


def repo_relative_path(root: Path, path: Path) -> str:
    """Return a stable POSIX repository-relative path."""
    return path.resolve().relative_to(root.resolve()).as_posix()


def git_object_type(
    root: Path, sha: str
) -> Tuple[Optional[str], Optional[str]]:
    try:
        result = subprocess.run(
            ["git", "cat-file", "-t", sha],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return None, "cannot execute git cat-file: {}".format(exc)

    if result.returncode == 0:
        return result.stdout.strip(), None

    try:
        shallow_result = subprocess.run(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return None, "cannot execute git rev-parse: {}".format(exc)

    if shallow_result.returncode != 0:
        return None, "cannot determine repository shallow state"

    shallow = shallow_result.stdout.strip().lower() == "true"

    if shallow:
        return None, "commit {} not present in shallow object database".format(
            sha
        )

    return "", None


# T-08: independent review is a separate dimension from session-side
# acceptance. The four values below are a REQ-05-local field enumeration for
# 00-governance/requirements-registry.yaml. They deliberately do not extend,
# rename, or reinterpret any GOV-DOC-002 document status enumeration; the
# policy's own enums remain a closed set owned by the Owner.
#
# BLOCKED vs PENDING is the whole point: BLOCKED records a measured structural
# obstacle. PENDING would say "not done yet", which hides a condition no
# session can satisfy by working harder.
#
# The example this comment used to give for BLOCKED -- "no second write-capable
# identity exists on the repository, so an independent reviewer cannot be
# established" -- is retired. PR-GOVERNANCE-001 section 5 was amended on
# 2026-11-24 (GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036): independence
# is a property of the reviewing session, not of the GitHub account, so the
# absence of a second account does not make an independent reviewer
# unestablishable. A session that did not author the change can supply it. The
# correct state for "review not performed yet" is therefore PENDING (or, where
# a caller distinguishes them, UNFULFILLED) -- not BLOCKED. BLOCKED remains
# valid for an obstacle that no session can clear, and the value is kept
# because dropping it would silently reinterpret existing registry entries.
# This is a comment change only: the enumeration below is unchanged, and no
# check behaviour moves.

ALLOWED_INDEPENDENT_REVIEW_STATES = {
    "NOT_REQUIRED",
    "PENDING",
    "BLOCKED",
    "PASSED",
}


def validate_acceptance(
    requirement_id: str,
    item: dict,
    reporter: Reporter,
) -> None:
    if "acceptance_state" in item:
        reporter.error(
            "T-08 {} retains legacy acceptance_state; migrate it to "
            "session_acceptance.acceptance_state".format(requirement_id)
        )

    session = item.get("session_acceptance")
    if not isinstance(session, dict):
        reporter.error(
            "T-08 {} session_acceptance must be an object".format(
                requirement_id
            )
        )
    else:
        state = session.get("acceptance_state")
        refs = session.get("evidence_refs")

        if not isinstance(state, str) or not state.strip():
            reporter.error(
                "T-08 {} session_acceptance.acceptance_state is required"
                .format(requirement_id)
            )

        if not isinstance(refs, list) or any(
            not isinstance(ref, str) or not ref.strip()
            for ref in refs
        ):
            reporter.error(
                "T-08 {} session_acceptance.evidence_refs must be an "
                "array of non-empty strings".format(requirement_id)
            )

    review = item.get("independent_review")
    if not isinstance(review, dict):
        reporter.error(
            "T-08 {} independent_review must be an object".format(
                requirement_id
            )
        )
        return

    required = review.get("required")
    status = review.get("status")
    blocker_reason = review.get("blocker_reason")
    exception_ref = review.get("exception_ref")
    implementation_identity = review.get("implementation_identity")
    reviewer_identity = review.get("reviewer_identity")
    evidence_refs = review.get("evidence_refs")

    if not isinstance(required, bool):
        reporter.error(
            "T-08 {} independent_review.required must be boolean".format(
                requirement_id
            )
        )
        return

    if status not in ALLOWED_INDEPENDENT_REVIEW_STATES:
        reporter.error(
            "T-08 {} independent_review.status is missing or unsupported"
            .format(requirement_id)
        )
        return

    if not isinstance(evidence_refs, list) or any(
        not isinstance(ref, str) or not ref.strip()
        for ref in evidence_refs
    ):
        reporter.error(
            "T-08 {} independent_review.evidence_refs must be an array "
            "of non-empty strings".format(requirement_id)
        )
        return

    if not required:
        if status != "NOT_REQUIRED":
            reporter.error(
                "T-08 {} required=false must use NOT_REQUIRED".format(
                    requirement_id
                )
            )
        if reviewer_identity is not None or evidence_refs:
            reporter.error(
                "T-08 {} NOT_REQUIRED must not claim reviewer evidence"
                .format(requirement_id)
            )
        return

    if status == "NOT_REQUIRED":
        reporter.error(
            "T-08 {} required=true cannot use NOT_REQUIRED".format(
                requirement_id
            )
        )
        return

    if status == "BLOCKED":
        if not isinstance(blocker_reason, str) or not blocker_reason.strip():
            reporter.error(
                "T-08 {} BLOCKED requires blocker_reason".format(
                    requirement_id
                )
            )
        if not isinstance(exception_ref, str) or not exception_ref.strip():
            reporter.error(
                "T-08 {} BLOCKED requires exception_ref".format(
                    requirement_id
                )
            )
        if reviewer_identity is not None or evidence_refs:
            reporter.error(
                "T-08 {} BLOCKED cannot claim completed reviewer evidence"
                .format(requirement_id)
            )
        if implementation_identity and reviewer_identity == implementation_identity:
            reporter.error(
                "T-08 {} BLOCKED cannot claim same-identity review".format(
                    requirement_id
                )
            )
        reporter.warn(
            "T-08 {} independent review is explicitly BLOCKED".format(
                requirement_id
            )
        )
        return

    if status == "PENDING":
        if reviewer_identity is not None or evidence_refs:
            reporter.error(
                "T-08 {} PENDING cannot claim completed review evidence"
                .format(requirement_id)
            )
        reporter.warn(
            "T-08 {} independent review is pending".format(requirement_id)
        )
        return

    if status == "PASSED":
        if (
            not isinstance(implementation_identity, str)
            or not implementation_identity.strip()
            or not isinstance(reviewer_identity, str)
            or not reviewer_identity.strip()
        ):
            reporter.error(
                "T-08 {} PASSED requires implementation_identity and "
                "reviewer_identity".format(requirement_id)
            )
        elif implementation_identity == reviewer_identity:
            reporter.error(
                "T-08 {} reviewer must differ from implementation identity"
                .format(requirement_id)
            )

        if not evidence_refs:
            reporter.error(
                "T-08 {} PASSED requires review evidence_refs".format(
                    requirement_id
                )
            )

        if blocker_reason not in (None, "") or exception_ref not in (None, ""):
            reporter.error(
                "T-08 {} PASSED must not retain active blocker fields"
                .format(requirement_id)
            )


def validate_registry(
    root: Path,
    requirements: List[dict],
    reporter: Reporter,
) -> Tuple[set, set]:
    seen = set()
    authority_issues = set()
    requirement_ids = set()

    for index, item in enumerate(requirements):
        rid = item.get("requirement_id")

        if not isinstance(rid, str) or not REQUIREMENT_ID_RE.fullmatch(rid):
            reporter.error(
                "T-01 requirements[{}] has invalid requirement_id".format(
                    index
                )
            )
        elif rid in seen:
            reporter.error("T-01 duplicate requirement_id {}".format(rid))
        else:
            seen.add(rid)
            requirement_ids.add(rid)

        authority = item.get("authority_url")
        issue_match = (
            ISSUE_URL_RE.fullmatch(authority)
            if isinstance(authority, str)
            else None
        )

        if not issue_match:
            reporter.error(
                "T-01 {} authority_url must be a non-empty GitHub Issue URL"
                .format(rid or "requirements[{}]".format(index))
            )
        else:
            authority_issues.add(issue_match.group(1))

        docs = item.get("linked_docs")
        if not isinstance(docs, list):
            reporter.error(
                "T-02 {} linked_docs must be an array".format(rid)
            )
            docs = []

        for doc in docs:
            path = safe_repo_path(root, doc)

            if path is None:
                reporter.error(
                    "T-02 {} has unsafe linked_docs path {!r}".format(
                        rid, doc
                    )
                )
            elif not path.is_file():
                reporter.error(
                    "T-02 {} references missing document {}".format(
                        rid, doc
                    )
                )

        linked = item.get("linked_work_items")
        if not isinstance(linked, list):
            reporter.error(
                "T-03 {} linked_work_items must be an array".format(rid)
            )
            linked = []

        index_path = root / INDEX_PATH
        index_text = None

        if linked:
            try:
                index_text = index_path.read_text(encoding="utf-8")
            except OSError as exc:
                raise CheckFailure(
                    "cannot read work item INDEX: {}".format(exc)
                ) from exc

        for work_item_id in linked:
            if not isinstance(work_item_id, str) or not re.fullmatch(
                r"AID-[0-9]{4}-[0-9]{3}", work_item_id
            ):
                reporter.error(
                    "T-03 {} has invalid linked work item {!r}".format(
                        rid, work_item_id
                    )
                )
                continue

            if not re.search(
                r"\[\s*" + re.escape(work_item_id) + r"\s*\]\(",
                index_text or "",
            ):
                reporter.error(
                    "T-03 {} links {} but it is absent from INDEX.md".format(
                        rid, work_item_id
                    )
                )

        if not linked:
            no_item = item.get("no_work_item_yet")
            reason = item.get("no_work_item_yet_reason")

            if (
                no_item is not True
                or not isinstance(reason, str)
                or not reason.strip()
            ):
                reporter.error(
                    "T-07 {} needs linked_work_items or "
                    "no_work_item_yet=true with a reason".format(rid)
                )

        validate_acceptance(rid, item, reporter)

    return requirement_ids, authority_issues


def manifest_identity(
    aid: str,
    fields: Dict[str, Optional[str]],
    manifest_path: Path,
    reporter: Reporter,
    root: Path,
) -> bool:
    """Validate the closed manifest identity-key policy.

    The Stage 0 registration record has its own record type and is not
    interpreted as a normal Work Item manifest.

    For ordinary Work Items, `work_item_id` is normative. `aid` is accepted
    only for the three explicitly listed historical records. Unknown keys
    are never guessed or treated as identity fields.
    """
    record_type = fields.get("record_type")

    if record_type == STAGE_0_RECORD_TYPE:
        reporter.warn(
            "T-04 {} is a Stage 0 registration record "
            "(record_type={}); ordinary Work Item identity fields are "
            "not applicable".format(aid, STAGE_0_RECORD_TYPE)
        )
        return True

    has_work_item_id = "work_item_id" in fields
    has_aid = "aid" in fields

    if has_work_item_id and has_aid:
        reporter.error(
            "T-04 manifest {} contains both work_item_id and aid".format(
                manifest_path
            ),
            repo_relative_path(root, manifest_path),
        )
        return False

    if has_work_item_id:
        manifest_id = fields.get("work_item_id")
        if manifest_id != aid:
            reporter.error(
                "T-04 manifest {} work_item_id={!r} does not match "
                "directory".format(manifest_path, manifest_id),
                repo_relative_path(root, manifest_path),
            )
            return False
        return True

    if has_aid:
        manifest_id = fields.get("aid")
        if aid not in LEGACY_AID_KEY_IDS:
            reporter.error(
                "T-04 manifest {} uses non-normative aid key outside the "
                "explicit legacy compatibility list".format(manifest_path),
                repo_relative_path(root, manifest_path),
            )
            return False

        if manifest_id != aid:
            reporter.error(
                "T-04 manifest {} aid={!r} does not match directory".format(
                    manifest_path, manifest_id
                ),
                repo_relative_path(root, manifest_path),
            )
            return False

        reporter.warn(
            "T-04 {} uses legacy aid identity key; migrate to "
            "work_item_id".format(aid)
        )
        return True

    reporter.error(
        "T-04 manifest {} has no recognized identity key "
        "(work_item_id required)".format(manifest_path),
        repo_relative_path(root, manifest_path),
    )
    return False


def validate_index_and_manifests(
    root: Path,
    authority_issues: set,
    reporter: Reporter,
) -> Tuple[int, set]:
    index_path = root / INDEX_PATH

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CheckFailure(
            "cannot read {}: {}".format(INDEX_PATH, exc)
        ) from exc

    index_entries: Dict[str, str] = {}

    for match in AID_LINK_RE.finditer(index_text):
        aid, manifest_relative = match.groups()

        if aid in index_entries:
            reporter.error("T-04 duplicate INDEX entry {}".format(aid))

        index_entries[aid] = manifest_relative

    manifests = sorted(
        (root / WORK_ITEMS_DIR).glob("AID-*/manifest.yaml")
    )
    manifest_by_id = {path.parent.name: path for path in manifests}

    # Forward direction: every INDEX entry must resolve to its manifest.
    for aid, manifest_relative in index_entries.items():
        expected = safe_work_item_manifest_path(root, manifest_relative)

        if expected is None:
            reporter.error(
                "T-04 {} has unsafe manifest path {}".format(
                    aid, manifest_relative
                )
            )
            continue

        if not expected.is_file():
            reporter.error(
                "T-04 INDEX entry {} has no manifest at {}".format(
                    aid, manifest_relative
                )
            )
            continue

        if expected.parent.name != aid:
            reporter.error(
                "T-04 INDEX id {} does not match manifest directory {}".format(
                    aid, expected.parent.name
                )
            )

    # Reverse direction: every governed record on disk must be indexed.
    # Stage 0 records remain subject to this INDEX entry-point requirement.
    for aid, manifest_path in sorted(manifest_by_id.items()):
        fields = parse_manifest_top_level(manifest_path)

        manifest_identity(
            aid, fields, manifest_path, reporter, root
        )

        if aid not in index_entries:
            reporter.error(
                "T-04 manifest {} exists on disk but is not indexed".format(
                    manifest_path
                ),
                repo_relative_path(root, manifest_path),
            )

        tracking = fields.get("tracking_issue")

        if tracking:
            issue_numbers = set(ISSUE_NUMBER_RE.findall(tracking))
            req_refs = set(REQ_REF_RE.findall(tracking))
            matched = issue_numbers.intersection(authority_issues)

            if issue_numbers and matched:
                pass
            elif issue_numbers or req_refs:
                reporter.warn(
                    "T-05 {} tracking_issue={!r} contains references that "
                    "cannot be treated as requirement authority: "
                    "tracking_issue is free text and no explicit manifest "
                    "requirement link exists".format(aid, tracking)
                )
            else:
                reporter.warn(
                    "T-05 {} tracking_issue is descriptive/free text; "
                    "no authoritative requirement mapping can be inferred"
                    .format(aid)
                )

        base_sha = fields.get("base_commit_sha")

        if not base_sha:
            reporter.warn(
                "T-06 {} has no base_commit_sha; historical baseline is "
                "NOT_RECORDED".format(aid)
            )
        elif not SHA_RE.fullmatch(base_sha):
            reporter.warn(
                "T-06 {} base_commit_sha={!r} is not a full hexadecimal SHA"
                .format(aid, base_sha)
            )
        else:
            object_type, git_error = git_object_type(root, base_sha)

            if git_error:
                reporter.unknown(
                    "T-06 {} cannot verify base_commit_sha {}: {}".format(
                        aid, base_sha, git_error
                    )
                )
            elif object_type is None:
                reporter.unknown(
                    "T-06 {} cannot determine whether base_commit_sha {} "
                    "exists".format(aid, base_sha)
                )
            elif object_type == "":
                reporter.warn(
                    "T-06 {} base_commit_sha {} is absent from the complete "
                    "local Git object database".format(aid, base_sha)
                )
            elif object_type != "commit":
                reporter.warn(
                    "T-06 {} base_commit_sha {} resolves to {}, not a commit"
                    .format(aid, base_sha, object_type)
                )

    return len(manifests), set(index_entries)


def verdict(reporter: Reporter) -> Tuple[str, int]:
    """Map the measured state to one word and one exit code.

    The word and the code are derived from the same predicate so the text
    cannot contradict the exit status.
    """
    if reporter.errors:
        return "FAIL", 1

    if reporter.indeterminate:
        return "INCOMPLETE", 2

    return "PASS", 0


def summarize(
    reporter: Reporter,
    requirement_count: int,
    work_item_count: int,
) -> int:
    word, code = verdict(reporter)

    reporter.warning_stream.write(
        "{} TRACEABILITY: {} requirements / {} work items / {} errors / "
        "{} warnings\n".format(
            word,
            requirement_count,
            work_item_count,
            reporter.errors,
            reporter.warnings,
        )
    )

    return code


def run_index_check(
    root: Path,
    stream: TextIO,
    warning_stream: Optional[TextIO] = None,
) -> int:
    """Run only the INDEX/manifest half, which needs no registry.

    `validate_index_and_manifests` reads `INDEX.md` and the work-item
    directories, and nothing else. It was nevertheless unreachable in
    practice because `run_check` called `parse_registry` first inside the
    same `try`, so a missing registry took the whole run with it (#1071).

    This entry point deliberately does not make the registry optional: the
    registry-dependent path is unchanged and still fails loudly when the
    file is absent. It only gives the four assertions that do not need a
    requirement a caller, because a gate nobody runs is not a gate.

    `authority_issues` is empty here by construction. It only upgrades T-05
    from a warning to nothing when a `tracking_issue` reference matches a
    registry requirement, so the empty set can add warnings but cannot hide
    an error. `errors` is what `verdict` keys on, so a run of this path can
    be green without the registry and cannot be greener than the full check
    would be on the same tree.
    """
    reporter = Reporter(stream, warning_stream)

    try:
        work_item_count, _ = validate_index_and_manifests(
            root, set(), reporter
        )
    except CheckFailure as exc:
        reporter.error("cannot complete INDEX/manifest check: {}".format(exc))
        return summarize(reporter, 0, 0)
    except OSError as exc:
        reporter.unknown("I/O failure: {}".format(exc))
        return summarize(reporter, 0, 0)

    return summarize(reporter, 0, work_item_count)


def run_check(
    root: Path,
    stream: TextIO,
    warning_stream: Optional[TextIO] = None,
) -> int:
    reporter = Reporter(stream, warning_stream)

    try:
        requirements = parse_registry(root / REGISTRY_PATH)

        _, authority_issues = validate_registry(
            root, requirements, reporter
        )

        work_item_count, _ = validate_index_and_manifests(
            root, authority_issues, reporter
        )

    except CheckFailure as exc:
        message = "cannot complete traceability check: {}".format(exc)
        if not (root / REGISTRY_PATH).is_file():
            # The registry is a required input. Its absence is a repo defect,
            # not an environment that could not be read: report it as an error
            # so the summary line cannot say "0 errors" while the exit code
            # says failure. Text and status must agree here too.
            reporter.error("required registry unavailable: {}".format(exc))
        else:
            reporter.unknown(message)
        return summarize(reporter, 0, 0)

    except OSError as exc:
        reporter.unknown("I/O failure: {}".format(exc))
        return summarize(reporter, 0, 0)

    return summarize(reporter, len(requirements), work_item_count)


def main() -> int:
    # `--index-only` exists so the INDEX/manifest assertions can run where the
    # registry is not available. It changes which half runs, not what a missing
    # registry means: the default path is untouched and still exits 1 when
    # `00-governance/requirements-registry.yaml` is absent (#1071, #1064).
    root = Path(os.getcwd())
    if "--index-only" in sys.argv[1:]:
        return run_index_check(root, sys.stdout, sys.stderr)
    return run_check(root, sys.stdout, sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
