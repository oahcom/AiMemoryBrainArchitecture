#!/usr/bin/env python3
"""Conservative bilingual documentation gate for pull requests.

This checks changed-file pairing and explicit PR declarations. It does not
claim semantic translation parity; that remains a reviewer responsibility.
"""
from __future__ import annotations

import ast
import os
from datetime import date
import subprocess
import sys
import re
from collections import Counter
from pathlib import Path

NORMATIVE_ROOTS = {
    "00-governance", "01-system-architecture", "02-domain-model",
    "04-memory-compiler", "06-memory-context", "07-agent-integration",
    "08-bmcp-protocol", "13-engineering-decisions", "14-ai-development",
}
REPO_ROOT = Path(__file__).resolve().parents[1]
_missing_roots = sorted(r for r in NORMATIVE_ROOTS if not (REPO_ROOT / r).is_dir())
if _missing_roots:
    sys.stderr.write(
        "NORMATIVE_ROOTS references non-existent directories: "
        + ", ".join(_missing_roots) + "\n"
    )
    sys.exit(2)
# 14-ai-development subtrees holding operational records or prompt templates,
# not bilingual specifications. The PR-body declaration requirement still
# applies; counterpart pairing does not.
PAIR_EXEMPT_PREFIXES = (
    "14-ai-development/work-items/",
    "14-ai-development/prompts/",
    "14-ai-development/adr/",
)
# For 14-ai-development, counterpart pairing applies to prose documents only.
PAIR_ENFORCED_SUFFIXES = {".md"}
# Exact side-by-side pairs temporarily known to be incomplete translations.
# Each key is an unordered pair of repository-relative paths.
# Keep empty when no reviewed partial pair remains unresolved.
PARTIAL_SIDE_BY_SIDE_PAIRS: set[frozenset[str]] = set()
EXEMPT_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".drawio"}
# Each entry is a reviewed single-file bilingual source. The reason must add
# information about the file's external contract, consumer, or governance role
# that the file does not already state about itself. This is a reviewer
# obligation, not a regex/checker rule: reviewers must reject self-describing
# reasons that merely repeat the document's own subject or contents.
#
# Three legacy registrations were made by the same author in the commit that
# created each file. They remain exempt only as explicitly named findings, not
# as precedent for future registrations. IMPORTANT: every SHA in this mapping
# MUST come from _file_add_commit() with complete Git history. A shallow clone
# can report its shallow-boundary commit instead of the true creation commit.
# Example measured on full history: bilingual-documentation-policy.md was
# created at cd1ab0fb346c770d779b1d8d24297f6811a1a74f and registered at
# 32a35f422ba6442d1f700cfb327f348c0740a7f2; these are distinct commits.
# Never calculate or refresh this mapping from a shallow clone.
# Owner measurement found bilingual
# headings and both scripts interleaved across 15–19% of lines (above the 9%
# control-template density), confirming that their content is genuinely
# embedded-bilingual; the defect was the missing second-party registration.
SELF_REGISTERED_AT_CREATION: dict[str, str] = {
    "00-governance/architecture-document-management-policy.md": "0c73f639bf7392a5381d0cc0d9cafd53017bfe05",
    "00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md": "04d35f90d6f1389ee17dc8fba1a32600bd7ac8ec",
    "00-governance/reports/f06-object-reconciliation.md": "9990b645555aef83714ff92c97255110b1fa0960",
}
EMBEDDED_BILINGUAL_SOURCES: dict[str, str] = {
    "00-governance/bilingual-documentation-policy.md": (
        "Defines one repository-wide bilingual obligation, parity rules, "
        "exception fields, and authority boundaries that must remain identical."
    ),
    "14-ai-development/ai-development-standard.md": (
        "Defines shared AI roles, risk classes, task gates, and evidence duties; "
        "splitting it could make one language authorize different workflows."
    ),
    "00-governance/architecture-document-management-policy.md": (
        "Defines document metadata, lifecycle, approval, and validation rules "
        "whose field meanings and governance states must stay in one contract."
    ),
    "00-governance/architecture-document-metadata.schema.yaml": (
        "Is the machine-consumed GOV-DOC-002 metadata schema; one YAML source "
        "keeps parser keys and validation structure canonical across languages."
    ),
    "00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md": (
        "Records a non-normative policy proposal and its explicit adoption "
        "limits, so both language renderings preserve the same draft authority."
    ),
    "00-governance/bilingual-governance-migration-register.md": (
        "Tracks bilingual migration classifications, source versions, and "
        "pending governance decisions as one auditable register."
    ),
    "00-governance/templates/bilingual-issue-template.md": (
        "Provides one shared Issue field layout and bilingual prompts so copied "
        "records retain identical identifiers and acceptance fields."
    ),
    "00-governance/templates/bilingual-umbrella-requirement-template.md": (
        "Defines the common umbrella-requirement metadata and status fields; "
        "separate templates could create incompatible requirement records."
    ),
    "00-governance/templates/bilingual-commit-message.md": (
        "Specifies one commit subject syntax with paired language summaries, "
        "types, and examples that must be copied consistently."
    ),
    "00-governance/templates/repository-policy-inheritance.md": (
        "Defines exact inheritance declaration labels and values consumed by "
        "governance checks, which must not diverge between language templates."
    ),
    "00-governance/templates/document-metadata-template.md": (
        "Provides one copy-paste metadata block whose field names, closed enums, "
        "and REQUIRED markers are consumed verbatim by check_document_management.py; "
        "split mirrors would let the two languages document different enum values."
    ),
    "00-governance/reports/bilingual-baseline-remediation-report.md": (
        "Combines remediation scope, status, and evidence in a single report "
        "so readers cannot mistake divergent language copies for separate facts."
    ),
    "00-governance/reports/f06-object-reconciliation.md": (
        "Presents one object-level reconciliation with computed counts, SHAs, "
        "and verdicts that must describe the same audit evidence in both languages."
    ),
    "14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md": (
        "Publishes binding Owner rulings resolving cross-standard conflicts; "
        "one source prevents the operative decision text from splitting by language."
    ),
    "14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.md": (
        "States one proposed ruling on session independence and R3 review limits, "
        "requiring identical proposal status and caveats in both languages."
    ),
    "14-ai-development/PR-GOVERNANCE-001.md": (
        "Defines shared PR lifecycle, review, and integration controls; divergent "
        "copies could assign different authority to the same repository actions."
    ),
    "14-ai-development/prompt-and-evidence-template.md": (
        "Supplies one Work Item and prompt evidence record structure with stable "
        "IDs, SHA fields, and acceptance evidence slots."
    ),
    "14-ai-development/prompt-authoring-standard.md": (
        "Defines controlled prompt scope, prohibitions, and evidence requirements "
        "whose normative force must be equivalent in both languages."
    ),
    "14-ai-development/iteration-lifecycle.md": (
        "Defines the ordered implementation, verification, review, and acceptance "
        "stages as one shared lifecycle rather than independent language workflows."
    ),
    "14-ai-development/owner-automation-operating-model.md": (
        "Defines the common Issue, PR, and scheduled-task operating model, "
        "including authority and safety boundaries that cannot vary by language."
    ),
    "14-ai-development/README.md": (
        "Acts as the bilingual governance portal and canonical navigation index; "
        "a single file keeps entry points and normative-document links synchronized."
    ),
}
for _source, _reason in EMBEDDED_BILINGUAL_SOURCES.items():
    if not (REPO_ROOT / _source).is_file():
        sys.stderr.write(
            f"EMBEDDED_BILINGUAL_SOURCES references missing file: {_source}\n"
        )
        sys.exit(2)
    if not _reason.strip() or len(_reason.strip()) <= 10:
        sys.stderr.write(
            f"EMBEDDED_BILINGUAL_SOURCES has missing or placeholder reason: {_source}\n"
        )
        sys.exit(2)
ROOT = Path.cwd()
BASELINE_PATH = REPO_ROOT / "scripts" / "bilingual-baseline.txt"


def _git_log_output(*args: str) -> str:
    """Read repository history for registration provenance checks."""
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


SHALLOW_HISTORY_ERROR = (
    "cannot verify registration provenance on a shallow clone; "
    "run git fetch --unshallow"
)


class ShallowRepositoryError(RuntimeError):
    """Raised when provenance cannot be established from incomplete history."""


def _require_full_git_history() -> None:
    """Fail closed before deriving provenance from a potentially shallow log."""
    result = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    shallow = result.stdout.strip().lower()
    if shallow == "true":
        raise ShallowRepositoryError(SHALLOW_HISTORY_ERROR)
    if shallow != "false":
        raise RuntimeError(
            "Unable to determine whether the Git repository has complete history: "
            f"unexpected rev-parse output {result.stdout!r}"
        )


def _file_add_commit(source: str) -> str | None:
    """Return the newest commit that added this path (full history required)."""
    _require_full_git_history()
    commits = _git_log_output(
        "log", "--diff-filter=A", "--format=%H", "-1", "HEAD", "--", source
    )
    return commits or None


def _embedded_sources_in_revision(revision: str, gate_path: str) -> set[str]:
    """Return keys in EMBEDDED_BILINGUAL_SOURCES at one Git revision."""
    content = _git_log_output("show", f"{revision}:{gate_path}")
    tree = ast.parse(content)
    for node in tree.body:
        target = None
        value = None
        if isinstance(node, ast.AnnAssign):
            target, value = node.target, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, value = node.targets[0], node.value
        if isinstance(target, ast.Name) and target.id == "EMBEDDED_BILINGUAL_SOURCES":
            literal = ast.literal_eval(value)
            return set(literal)
    return set()


def _registration_add_commit(source: str) -> str | None:
    """Return the registration commit; full Git history is required."""
    _require_full_git_history()
    gate_path = "scripts/check_bilingual_docs.py"
    commits = _git_log_output(
        "log", "--format=%H", "-S", f'"{source}"', "HEAD", "--", gate_path
    )
    for commit in commits.splitlines():
        try:
            current_sources = _embedded_sources_in_revision(commit, gate_path)
            parent = _git_log_output("rev-parse", f"{commit}^")
            previous_sources = _embedded_sources_in_revision(parent, gate_path)
        except subprocess.CalledProcessError:
            previous_sources = set()
            current_sources = _embedded_sources_in_revision(commit, gate_path)
        if source in current_sources and source not in previous_sources:
            return commit
    return None


def check_embedded_registration_history() -> list[str]:
    """Require exemption registration to post-date file creation.

    The only same-commit cases accepted are the three explicitly identified
    legacy self-registrations above, pinned to their measured creation SHAs.
    """
    try:
        _require_full_git_history()
    except ShallowRepositoryError as exc:
        return [str(exc)]
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        return [f"Unable to determine Git history completeness: {exc}"]

    errors: list[str] = []
    for source in sorted(EMBEDDED_BILINGUAL_SOURCES):
        try:
            file_commit = _file_add_commit(source)
            registration_commit = _registration_add_commit(source)
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(
                f"Unable to verify embedded bilingual registration history for "
                f"{source}: {exc}"
            )
            continue
        if not file_commit or not registration_commit:
            errors.append(
                f"Unable to identify both file-creation and exemption-registration "
                f"commits for {source}; full Git history is required."
            )
            continue
        if file_commit == registration_commit:
            if SELF_REGISTERED_AT_CREATION.get(source) != file_commit:
                errors.append(
                    f"Embedded bilingual source {source} was registered in the "
                    f"same commit that added the file ({file_commit[:8]}). "
                    "Register it in a later commit with independent review."
                )
        elif source in SELF_REGISTERED_AT_CREATION:
            errors.append(
                f"SELF_REGISTERED_AT_CREATION record for {source} does not match "
                f"its actual same-commit creation/registration SHA ({file_commit}, "
                f"{registration_commit})."
            )
    return errors


def _carries_chinese(source: str) -> bool:
    """Return True when a source contains at least 100 CJK Unified Ideographs."""
    path = ROOT / source
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff") >= 100


def _has_any_chinese(source: str) -> bool:
    """Return True when a source contains at least one CJK Unified Ideograph."""
    path = ROOT / source
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _side_by_side_bilingual(source: str) -> bool:
    """True when `source` has a side-by-side partner and the pair carries Chinese.

    One CJK character anywhere in either file is enough: a short but genuine
    translation must not be rejected for being brief.  The >=100 threshold in
    _carries_chinese() stays for the embedded-bilingual shape only.
    """
    partner = side_by_side_partner(source)
    if partner is None:
        return False
    return _has_any_chinese(source) or _has_any_chinese(partner)


def current_bilingual_gaps() -> set[str]:
    """Return non-exempt normative Markdown sources missing either language mirror."""
    gaps: set[str] = set()
    for root_name in sorted(NORMATIVE_ROOTS):
        root = REPO_ROOT / root_name
        for path in sorted(root.rglob("*.md")):
            source = path.relative_to(REPO_ROOT).as_posix()
            if source in EMBEDDED_BILINGUAL_SOURCES:
                continue
            # Inventory and changed-path gates must share prefixes or pair-exempt paths become permanent gaps.
            if source.startswith(PAIR_EXEMPT_PREFIXES):
                continue
            english = REPO_ROOT / "docs" / "en" / source
            chinese = REPO_ROOT / "docs" / "zh-CN" / source
            mirrored = english.is_file() and chinese.is_file()
            side_by_side = side_by_side_partner(source)
            partial_side_by_side = (
                side_by_side is not None
                and frozenset((source, side_by_side)) in PARTIAL_SIDE_BY_SIDE_PAIRS
            )
            # Structural pairing is not enough: a side-by-side pair must carry Chinese text.
            # A pair registered as partially translated is not a pairing at all.
            paired = mirrored or (_side_by_side_bilingual(source) and not partial_side_by_side)
            if not paired and root_name == "14-ai-development":
                # Shape 3: the root file IS the Chinese source and docs/en holds
                # the English side. It must be earned by actually carrying Chinese.
                paired = english.is_file() and _carries_chinese(source)
            if not paired:
                gaps.add(source)
    return gaps

def write_baseline() -> int:
    gaps = sorted(current_bilingual_gaps())
    header = (
        "# Frozen inventory of pre-existing bilingual documentation gaps.\n"
        "# This baseline may only shrink; entries must never be added.\n"
        "# Regenerate only when explicitly adopting a new baseline.\n"
    )
    BASELINE_PATH.write_text(header + "\n".join(gaps) + "\n", encoding="utf-8")
    print(f"baseline written: {len(gaps)} entries")
    return 0


def read_baseline() -> set[str] | None:
    if not BASELINE_PATH.is_file():
        print(f"::error::Required bilingual baseline is missing: {BASELINE_PATH.relative_to(REPO_ROOT)}")
        return None
    return {
        line.strip()
        for line in BASELINE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }



def changed_status() -> dict[str, str]:
    """Return changed paths and their A/M/D status without rename collapsing."""
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    if not base or not head:
        raise RuntimeError("BASE_SHA and HEAD_SHA are required")
    raw = subprocess.check_output(
        ["git", "diff", "--name-status", "--no-renames", f"{base}...{head}"],
        text=True,
    )
    result: dict[str, str] = {}
    for line in raw.splitlines():
        fields = line.split("\t", 1)
        if len(fields) != 2 or fields[0] not in {"A", "M", "D"}:
            raise RuntimeError(f"Unexpected name-status record: {line!r}")
        result[fields[1]] = fields[0]
    return result


def changed_paths() -> set[str]:
    """Compatibility set view for existing callers."""
    return set(changed_status())


CATCH_UP_DECLARATION_RE = re.compile(
    r"^BILINGUAL-CATCH-UP:\s+"
    r"source=(\S+)\s+"
    r"counterpart=(\S+)\s*$"
)

def parse_catch_up_declarations(
    body: str,
) -> tuple[dict[str, str], list[str]]:
    """Parse explicit one-sided translation catch-up declarations."""
    declarations: dict[str, str] = {}
    errors: list[str] = []

    for line_number, line in enumerate(body.splitlines(), start=1):
        if not line.startswith("BILINGUAL-CATCH-UP:"):
            continue

        match = CATCH_UP_DECLARATION_RE.fullmatch(line)
        if match is None:
            errors.append(
                f"Malformed BILINGUAL-CATCH-UP declaration at PR-body "
                f"line {line_number}"
            )
            continue

        source, counterpart = match.groups()
        if source in declarations:
            errors.append(
                f"Duplicate BILINGUAL-CATCH-UP declaration for {source}"
            )
            continue

        declarations[source] = counterpart

    return declarations, errors

def _blob_at(revision: str, path: str) -> str | None:
    """Return the git blob id of path at revision, or None when absent."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--verify", f"{revision}:{path}"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip() or None
    except subprocess.CalledProcessError:
        return None

def check_side_by_side_catch_up(
    source: str,
    counterpart: str,
    changed: set[str],
    statuses: dict[str, str],
) -> str | None:
    """Return None when the catch-up is verifiable, else the failure reason.

    The declared version is not trusted and is not supplied by the author:
    both blobs are read from the object database, so a rebase cannot leave a
    stale declaration behind and a PR cannot edit both sides and call it a
    catch-up.
    """
    if not (source.endswith(".zh-CN.md") or source.endswith(".en.md")):
        return "source is not a translation file (.zh-CN.md or .en.md)"

    if source not in changed:
        return "source is not changed in this PR"

    if statuses.get(source) == "D":
        return "source is deleted in this PR"

    if counterpart in changed:
        return "counterpart is also changed in this PR"

    if side_by_side_partner(source) != counterpart:
        return "declared counterpart does not match side-by-side partner"

    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    if not base or not head:
        return "BASE_SHA and HEAD_SHA must both be set"

    base_blob = _blob_at(base, counterpart)
    if base_blob is None:
        return "counterpart does not exist at PR base"

    head_blob = _blob_at(head, counterpart)
    if head_blob is None:
        return "counterpart does not exist at PR HEAD"

    if base_blob != head_blob:
        return "counterpart blob changed between PR base and HEAD"

    return None

def valid_side_by_side_catch_up(
    source: str,
    counterpart: str,
    changed: set[str],
    statuses: dict[str, str],
) -> bool:
    """Boolean view of check_side_by_side_catch_up for callers and tests."""
    return check_side_by_side_catch_up(source, counterpart, changed, statuses) is None

def check_counterpart_requirement(
    source: str,
    counterparts: list[str],
    changed: set[str],
    statuses: dict[str, str],
    exception: bool,
    catch_up_declaration: str | None = None,
) -> list[str]:
    """Require paired edits, with a verified side-by-side translation catch-up."""
    if exception:
        return []

    required = [source, *counterparts]

    if any(path not in changed for path in required):
        catch_up_failure = "no catch-up declaration"

        if len(counterparts) == 1 and catch_up_declaration is not None:
            if catch_up_declaration != counterparts[0]:
                catch_up_failure = (
                    "declared counterpart does not match side-by-side partner"
                )
            else:
                reason = check_side_by_side_catch_up(
                    source,
                    counterparts[0],
                    changed,
                    statuses,
                )
                if reason is None:
                    # The changed translation side is required; the verified
                    # counterpart is unchanged and identical at base and HEAD.
                    required = [source]
                    catch_up_failure = None
                else:
                    catch_up_failure = reason

        if catch_up_failure is not None:
            if catch_up_declaration is None:
                return [
                    f"{source} requires all counterparts changed in this PR: "
                    + ", ".join(required)
                ]
            return [
                f"{source} has an invalid BILINGUAL-CATCH-UP declaration: "
                + catch_up_failure
            ]
    deleted = [path for path in required if statuses.get(path) == "D"]
    if deleted and len(deleted) != len(required):
        return [
            f"{source} has an unpaired deletion; all related paths must move together or remain present"
        ]
    # Complete removals are not balanced by counting unrelated additions.
    # The independent root-departure check rejects normative-source deletion
    # and renames leaving NORMATIVE_ROOTS; mirror-only pairs remain unaffected.
    if len(deleted) == len(required):
        return []
    return [
        f"Counterpart file must exist for {source}: {path}"
        for path in required if not (ROOT / path).is_file()
    ]


def _is_normative_root_path(path: str) -> bool:
    parts = Path(path).parts
    return len(parts) >= 2 and parts[0] in NORMATIVE_ROOTS


def check_normative_root_departures(exception: bool) -> list[str]:
    """Reject normative-source deletions and renames leaving NORMATIVE_ROOTS."""
    if exception:
        return []
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    if not base or not head:
        raise RuntimeError("BASE_SHA and HEAD_SHA are required")
    raw = subprocess.check_output(
        ["git", "diff", "--name-status", "-M", f"{base}...{head}"],
        cwd=ROOT,
        text=True,
    )
    errors: list[str] = []
    for line in raw.splitlines():
        fields = line.split("\t")
        if len(fields) == 2 and fields[0] == "D":
            old_path = fields[1]
            if _is_normative_root_path(old_path):
                errors.append(
                    f"Normative source left NORMATIVE_ROOTS by deletion: {old_path}; "
                    "use BILINGUAL-EXCEPTION: APPROVED"
                )
        elif len(fields) == 3 and fields[0].startswith("R"):
            old_path, new_path = fields[1], fields[2]
            if _is_normative_root_path(old_path) and not _is_normative_root_path(new_path):
                errors.append(
                    f"Normative source moved outside NORMATIVE_ROOTS: "
                    f"{old_path} -> {new_path}; use BILINGUAL-EXCEPTION: APPROVED"
                )
        elif len(fields) != 2 or fields[0] not in {"A", "M"}:
            if not (len(fields) == 3 and fields[0].startswith("R")):
                raise RuntimeError(f"Unexpected name-status record: {line!r}")
    return errors

def approved_exception(body: str) -> bool:
    if "BILINGUAL-EXCEPTION: APPROVED" not in body:
        return False
    labels = (
        "Exception Owner:", "Authoritative language/version:",
        "Missing counterpart path:", "Exact source revision:",
        "Due date (YYYY-MM-DD", "Tracking Issue/PR:",
        "Approval evidence",
    )
    values: dict[str, str] = {}
    lines = body.splitlines()
    for label in labels:
        value = ""
        for line in lines:
            if line.strip().startswith("- " + label):
                value = line.split(":", 1)[1].strip() if ":" in line else ""
                break
        values[label] = value
    if not all(values.values()):
        return False
    if any(value.upper() in {"TBD", "TODO", "N/A", "PENDING"} for value in values.values()):
        return False
    due = values["Due date (YYYY-MM-DD"][:10]
    try:
        date.fromisoformat(due)
    except ValueError:
        return False
    return True



def check_policy_inheritance(body: str, changed: set[str]) -> list[str]:
    """Validate declaration syntax and consistency, not remote authority."""
    errors: list[str] = []
    marker = "POLICY-INHERITANCE-DECLARATION"
    fields = (
        "Policy ID",
        "Inherited Version",
        "Authoritative Repository",
        "Approved Source Commit",
        "Policy Blob SHA",
        "Inheritance State",
    )
    lines = body.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == marker]

    # This checks parseability and internal consistency only. It does not
    # resolve the authoritative repository remotely. Reviewers or a later CI
    # step must independently recompute the actual policy blob SHA.
    if not starts:
        if any(p.startswith("00-governance/") for p in changed):
            errors.append(
                "POLICY-INHERITANCE-DECLARATION missing for 00-governance changes."
            )
        return errors

    if len(starts) != 1:
        errors.append(
            "PR body must contain exactly one POLICY-INHERITANCE-DECLARATION block."
        )
        return errors

    values: dict[str, str] = {}
    for line in lines[starts[0] + 1:]:
        stripped = line.strip()
        if stripped == "===END":
            break
        if stripped.startswith("- ") and ":" in stripped:
            label, value = stripped[2:].split(":", 1)
            label, value = label.strip(), value.strip()
            if label in fields:
                if label in values:
                    errors.append(
                        f"POLICY-INHERITANCE-DECLARATION duplicate field: {label}."
                    )
                values[label] = value

    for field in fields:
        if field not in values:
            errors.append(
                f"POLICY-INHERITANCE-DECLARATION missing required field: {field}."
            )

    state = values.get("Inheritance State", "")
    if state not in {"PENDING", "INHERITED", "NOT_APPLICABLE"}:
        errors.append(
            "Inheritance State must be PENDING, INHERITED, or NOT_APPLICABLE."
        )

    if values.get("Policy ID") != "GOV-DOC-001":
        errors.append("Policy ID must equal GOV-DOC-001.")

    evidence_fields = (
        "Inherited Version",
        "Authoritative Repository",
        "Approved Source Commit",
        "Policy Blob SHA",
    )
    placeholders = {"TBD", "TODO", "N/A", "PENDING"}

    if state == "PENDING":
        for field in evidence_fields:
            if values.get(field) != "NOT_RECORDED":
                errors.append(
                    f"{field} must be explicitly NOT_RECORDED when Inheritance State is PENDING."
                )

    elif state == "NOT_APPLICABLE":
        for field in evidence_fields:
            if values.get(field, "").upper() in {"TBD", "TODO", "N/A"}:
                errors.append(
                    f"{field} must not be TBD, TODO, or N/A when Inheritance State is NOT_APPLICABLE."
                )
        if not values.get("Authoritative Repository", "").strip():
            errors.append(
                "Authoritative Repository must be non-empty when Inheritance State is NOT_APPLICABLE."
            )

    elif state == "INHERITED":
        for field in evidence_fields:
            value = values.get(field, "")
            if not value or value.upper() in placeholders:
                errors.append(
                    f"{field} must not be empty or a placeholder when Inheritance State is INHERITED."
                )

        for field in ("Approved Source Commit", "Policy Blob SHA"):
            if not re.fullmatch(r"[0-9a-fA-F]{40}", values.get(field, "")):
                errors.append(
                    f"{field} must be a 40-character hexadecimal SHA when Inheritance State is INHERITED."
                )

        commit = values.get("Approved Source Commit", "").lower()
        blob = values.get("Policy Blob SHA", "").lower()
        if re.fullmatch(r"[0-9a-f]{40}", commit) and blob == commit:
            errors.append(
                "Policy Blob SHA must differ from Approved Source Commit."
            )

    return errors

def check_prompt_library() -> list[str]:
    """Validate the canonical global/Owner prompt library structure and metadata."""
    errors: list[str] = []
    prompt_root = ROOT / "prompts"
    required = [
        prompt_root / "README.md",
        prompt_root / "global-project-developer.md",
        prompt_root / "global-architecture-reviewer.md",
        prompt_root / "global-bilingual-documentation.md",
    ]
    for owner in "ABCDEFGHI":
        owner_dir = prompt_root / owner
        required.extend(
            owner_dir / name
            for name in (
                "owner-charter.md",
                "phase-3-remediation.md",
                "technology-review.md",
            )
        )

    seen_ids: dict[str, str] = {}
    for path in required:
        rel = path.relative_to(ROOT).as_posix()
        if not path.is_file():
            errors.append(f"Required prompt library file is missing: {rel}")
            continue
        content = path.read_text(encoding="utf-8").strip()
        if len(content) < 250:
            errors.append(f"Required prompt library file is empty or incomplete: {rel}")
            continue

        prompt_id_match = re.search(
            r"^(?:- )?(?:Prompt ID|Library ID):\s*([A-Za-z0-9._-]+)\s*$",
            content,
            re.MULTILINE,
        )
        version_match = re.search(
            r"^(?:- )?Version:\s*([^\r\n]+)$", content, re.MULTILINE
        )
        status_match = re.search(
            r"^(?:- )?Status:\s*(.+)$", content, re.MULTILINE
        )
        if not prompt_id_match:
            errors.append(f"Prompt ID / Library ID metadata missing: {rel}")
        else:
            prompt_id = prompt_id_match.group(1)
            if prompt_id in seen_ids:
                errors.append(
                    f"Duplicate prompt identifier {prompt_id}: "
                    f"{seen_ids[prompt_id]} and {rel}"
                )
            seen_ids[prompt_id] = rel
        if not version_match:
            errors.append(f"Version metadata missing: {rel}")
        if not status_match:
            errors.append(f"Status metadata missing: {rel}")

    # Owner-specific prompts must remain inside their matching Owner directory.
    for owner in "ABCDEFGHI":
        charter = prompt_root / owner / "owner-charter.md"
        if charter.is_file():
            content = charter.read_text(encoding="utf-8")
            if not re.search(rf"Owner:\s*{owner}\b", content):
                errors.append(
                    f"Owner charter does not declare its directory Owner {owner}: "
                    f"prompts/{owner}/owner-charter.md"
                )

    return errors


def side_by_side_partner(source: str) -> str | None:
    """Conventional side-by-side counterpart, accepted in every normative root."""
    if source.endswith(".en.md"):
        stem = source[: -len(".en.md")]
        for cand in (stem + ".zh-CN.md", stem + ".md"):
            if cand != source and (ROOT / cand).is_file():
                return cand
    elif source.endswith(".zh-CN.md"):
        stem = source[: -len(".zh-CN.md")]
        for cand in (stem + ".en.md", stem + ".md"):
            if cand != source and (ROOT / cand).is_file():
                return cand
    elif source.endswith(".md"):
        stem = source[: -len(".md")]
        for cand in (stem + ".en.md", stem + ".zh-CN.md"):
            if cand != source and (ROOT / cand).is_file():
                return cand
    return None


def mirror_partner(source: str) -> str | None:
    """docs/en or root mirror counterpart for a 14-ai-development path."""
    if source.startswith("14-ai-development/"):
        en = "docs/en/" + source
        if (ROOT / en).is_file():
            return en
    if source.startswith("docs/en/14-ai-development/"):
        rest = source[len("docs/en/") :]
        if (ROOT / rest).is_file():
            return rest
        zh = "docs/zh-CN/" + rest
        if (ROOT / zh).is_file():
            return zh
    if source.startswith("docs/zh-CN/14-ai-development/"):
        rest = source[len("docs/zh-CN/") :]
        if (ROOT / rest).is_file():
            return rest
        en = "docs/en/" + rest
        if (ROOT / en).is_file():
            return en
    return None


def counterpart_14(source: str) -> str | None:
    """The single counterpart path for a 14-ai-development source, or None."""
    return side_by_side_partner(source) or mirror_partner(source)


def check_mirror_pairing(changed, statuses, exception):
    # type: (set[str], dict[str, str], bool) -> list[str]
    """A docs/en or docs/zh-CN change must update both sides in the same PR."""
    errors = []
    for path in sorted(changed):
        if path.startswith("docs/en/14-ai-development/"):
            counterpart = counterpart_14(path)
            if counterpart is None:
                if not exception:
                    errors.append(
                        f"{path} changed but no counterpart is resolvable "
                        "(root source or docs/zh-CN mirror); pair it or use "
                        "a documented BILINGUAL-EXCEPTION"
                    )
                continue
            errors.extend(check_counterpart_requirement(path, [counterpart], changed, statuses, exception))
        elif path.startswith("docs/zh-CN/14-ai-development/"):
            counterpart = counterpart_14(path)
            if counterpart is None:
                if not exception:
                    errors.append(
                        f"{path} changed but no counterpart is resolvable "
                        "(root source or docs/en mirror); pair it or use "
                        "a documented BILINGUAL-EXCEPTION"
                    )
                continue
            if counterpart not in changed and not exception:
                errors.append(f"{path} changed without paired change {counterpart}")
        elif path.startswith("docs/en/"):
            counterpart = "docs/zh-CN/" + path[len("docs/en/"):]
            errors.extend(check_counterpart_requirement(
                path, [counterpart], changed, statuses, exception
            ))
        elif path.startswith("docs/zh-CN/"):
            counterpart = "docs/en/" + path[len("docs/zh-CN/"):]
            errors.extend(check_counterpart_requirement(
                path, [counterpart], changed, statuses, exception
            ))
    return errors


def check_normative_pairing(
    normative_changes, changed, statuses, complete, exception,
    catch_up_declarations=None,
):
    # type: (
    #     list[str], set[str], dict[str, str], bool, bool,
    #     dict[str, str] | None
    # ) -> list[str]
    """Normative changes need paired counterparts (or an explicit exemption)."""
    errors = []
    if not (normative_changes and complete):
        return errors
    for source in normative_changes:
        if source in EMBEDDED_BILINGUAL_SOURCES:
            continue
        if source.startswith(PAIR_EXEMPT_PREFIXES):
            continue
        if source.startswith("14-ai-development/"):
            if Path(source).suffix.lower() not in PAIR_ENFORCED_SUFFIXES:
                continue
            partner = counterpart_14(source)
            if partner is None:
                errors.append(
                    f"{source} has no resolvable bilingual counterpart "
                    "(side-by-side .en.md/.zh-CN.md or docs/en mirror); "
                    "pair it, register it in EMBEDDED_BILINGUAL_SOURCES, "
                    "or use a documented BILINGUAL-EXCEPTION"
                )
                continue
            errors.extend(
                check_counterpart_requirement(
                    source, [partner], changed, statuses, exception,
                    catch_up_declaration=(catch_up_declarations or {}).get(source),
                )
            )
            continue
        partner = side_by_side_partner(source)
        if partner is not None:
            errors.extend(
                check_counterpart_requirement(
                    source, [partner], changed, statuses, exception,
                    catch_up_declaration=(catch_up_declarations or {}).get(source),
                )
            )
            continue

        en = f"docs/en/{source}"
        zh = f"docs/zh-CN/{source}"
        errors.extend(check_counterpart_requirement(source, [en, zh], changed, statuses, exception))
    return errors


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--write-baseline":
        try:
            return write_baseline()
        except Exception as exc:
            print(f"::error::Unable to write bilingual baseline: {exc}")
            return 2
    if len(sys.argv) > 1:
        print("::error::Unknown argument. Supported option: --write-baseline")
        return 2

    # Refuse to make any gate judgment from a shallow checkout. This must run
    # before baseline/path checks so their unrelated diagnostics cannot mask
    # the fact that provenance is unverifiable.
    try:
        _require_full_git_history()
    except ShallowRepositoryError as exc:
        print(f"::error::{exc}")
        return 2
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"::error::Unable to determine Git history completeness: {exc}")
        return 2

    try:
        statuses = changed_status()
        changed = set(statuses)
    except Exception as exc:
        print(f"::error::Unable to determine changed paths: {exc}")
        return 2

    baseline = read_baseline()
    if baseline is None:
        return 2
    gap_now = current_bilingual_gaps()
    new_gaps = sorted(gap_now - baseline)
    resolved = sorted(baseline - gap_now)
    if new_gaps:
        for path in new_gaps:
            print(f"::error::New bilingual gap outside frozen baseline: {path}")
        return 2
    if resolved:
        for path in resolved:
            print(
                f"::error::Resolved bilingual gap must be removed from "
                f"scripts/bilingual-baseline.txt: {path}"
            )
        return 2
    print(f"bilingual baseline: {len(baseline)} frozen, 0 new gaps")

    body = os.environ.get("PR_BODY", "")
    errors: list[str] = check_prompt_library()
    history_errors = check_embedded_registration_history()
    if SHALLOW_HISTORY_ERROR in history_errors:
        print(f"::error::{SHALLOW_HISTORY_ERROR}")
        return 2
    if any(error.startswith("Unable to determine Git history completeness:") for error in history_errors):
        for error in history_errors:
            print(f"::error::{error}")
        return 2
    errors.extend(history_errors)
    catch_up_declarations, catch_up_errors = parse_catch_up_declarations(body)
    errors.extend(catch_up_errors)
    # ADVISORY ONLY: the inheritance requirement originates from the unadopted
    # GOV-DOC-001 v1.2 draft. Reporting it as a blocking error would impose an
    # unapproved normative obligation through tooling, so it is emitted as a
    # notice until the requirement is formally adopted.
    for notice in check_policy_inheritance(body, changed):
        print(f"::notice::advisory (non-blocking): {notice}")
    exception = approved_exception(body)
    complete = "BILINGUAL-MANIFEST: COMPLETE" in body

    # A language-pair change must update both sides in the same PR.
    errors.extend(check_mirror_pairing(changed, statuses, exception))

    bilingual_doc_changes = any(
        path.startswith("docs/en/") or path.startswith("docs/zh-CN/")
        or path in {"docs/README.md", "docs/translation-status.md"}
        for path in changed
    )
    if bilingual_doc_changes and not complete and not exception:
        errors.append(
            "Bilingual guide/spec files changed but PR body lacks the explicit "
            "COMPLETE manifest status or a fully documented approved exception."
        )

    # A normative source-spec change requires paired reader/spec documents
    # or a formally approved, time-bounded exception.
    normative_changes = []
    for path in sorted(changed):
        parts = Path(path).parts
        if len(parts) >= 2 and parts[0] in NORMATIVE_ROOTS:
            if Path(path).suffix.lower() in EXEMPT_SUFFIXES:
                continue
            if Path(path).suffix.lower() == ".md":
                normative_changes.append(path)

    if normative_changes and not complete and not exception:
        errors.append(
            "Normative source files changed but PR body lacks "
            "'BILINGUAL-MANIFEST: COMPLETE' or a fully documented "
            "'BILINGUAL-EXCEPTION: APPROVED'."
        )

    errors.extend(
        check_normative_pairing(
            normative_changes,
            changed,
            statuses,
            complete,
            exception,
            catch_up_declarations,
        )
    )
    errors.extend(check_normative_root_departures(exception))

    skipped = [p for p in changed if Path(p).parts and Path(p).parts[0] not in NORMATIVE_ROOTS
               and Path(p).suffix.lower() == ".md"]
    if skipped:
        sys.stderr.write(f"NOTE: {len(skipped)} changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked\n")

    if exception:
        print("Approved bilingual exception declaration detected; human governance approval remains mandatory.")
    if errors:
        for error in errors:
            print(f"::error::{error}")
        print("Bilingual documentation gate: FAIL")
        return 1

    print(f"exemptions: {len(EMBEDDED_BILINGUAL_SOURCES)}")
    print(f"Bilingual documentation and prompt-library gate: PASS ({len(changed)} changed paths inspected).")
    print("This is a structural gate only; semantic parity requires independent review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())