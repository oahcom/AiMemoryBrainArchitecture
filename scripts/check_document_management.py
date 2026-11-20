#!/usr/bin/env python3
"""GOV-DOC-002 document management gate.

Validates the four-dimension metadata block declared at the top of governed
Markdown files. Checked rules are listed in
00-governance/architecture-document-management-policy.md §9 (DM-01 .. DM-09).

This checks structural conformance only. Semantic parity and the truth of an
approval decision remain reviewer responsibilities under GOV-DOC-001 §2.1.

No third-party dependency: the metadata block is a constrained YAML subset,
parsed by the small reader below.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Normative roots to govern. Keep in sync with check_bilingual_docs.py.
NORMATIVE_ROOTS = (
    "00-governance", "01-system-architecture", "02-domain-model",
    "03-memory-brain", "04-memory-compiler", "05-memory-runtime",
    "06-memory-context", "07-agent-integration", "08-protocols",
    "09-storage-and-index", "10-security-and-governance",
    "11-consistency-and-recovery", "12-testing-and-acceptance",
    "13-engineering-decisions", "14-ai-development",
    # Bilingual mirrors of the sources above. Counted so that mirror drift is
    # visible rather than falling outside the audit entirely.
    "docs/en", "docs/zh-CN",
)
EXEMPT_PREFIXES = (
    "14-ai-development/work-items/",
    "14-ai-development/prompts/",
    "14-ai-development/adr/",
    "00-governance/templates/",
    "00-governance/reports/",
    "00-governance/drafts/",
)
GOVERNED_ENTRY = "document_metadata"

DOMAINS = {
    "architecture", "domain-model", "memory-brain", "memory-compiler",
    "memory-runtime", "memory-context", "agent-integration", "protocol",
    "security-governance", "storage-index", "consistency-recovery",
    "testing-acceptance", "ai-development",
}
ROLES = {
    "design-specification", "decision-record", "normative-standard",
    "research", "review-report", "work-record", "guide", "reference", "index",
}
DECISION_STATUSES = {
    "Draft", "Under-Review", "Approved", "Rejected", "Withdrawn", "Revoked",
}
USAGE_STATUSES = {"Active", "Deprecated", "Archived", "Superseded"}
VERIFICATION_STATUSES = {"Unverified", "Verified", "Invalidated"}
CANONICAL_STATUSES = {"Canonical", "Non-Canonical", "Candidate"}
NORMATIVE_STATUSES = {"Normative", "Informative"}
CONFLICT_STATUSES = {"None", "Under-Review", "Resolved"}
MODIFICATION_STATUSES = {
    "Unchanged", "Modified", "Active-Modified", "Pending-Reapproval",
}

SCOPE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*/[a-z0-9]+(-[a-z0-9]+)*$")


class ParseError(Exception):
    pass


def _strip_comment(line: str) -> str:
    """Remove a trailing YAML comment, respecting quoted scalars."""
    out, quote = [], None
    for ch in line:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            continue
        if ch == "#":
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(text: str):
    text = text.strip()
    if text in ("", "null", "~", "None"):
        return None
    if text in ("[]", "{}"):
        return [] if text == "[]" else {}
    if text == "true":
        return True
    if text == "false":
        return False
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def parse_block(lines: list[str], base_indent: int, start: int, end: int):
    """Parse an indentation-based mapping/list block into dict/list."""
    items: dict = {}
    seq: list = []
    i = start
    mode = None
    while i < end:
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent < base_indent:
            break
        content = _strip_comment(raw.strip())
        if not content:
            i += 1
            continue
        if content.startswith("- "):
            mode = mode or "list"
            seq.append(_scalar(content[2:]))
            i += 1
            continue
        if ":" not in content:
            i += 1
            continue
        mode = mode or "dict"
        key, _, rest = content.partition(":")
        key, rest = key.strip(), rest.strip()
        # Look ahead for a nested block.
        j = i + 1
        while j < end and not lines[j].strip():
            j += 1
        nested = (
            j < end
            and (len(lines[j]) - len(lines[j].lstrip(" "))) > indent
        )
        if rest:
            items[key] = _scalar(rest)
            i += 1
        elif nested:
            child, i = parse_block(lines, indent + 1, j, end)
            items[key] = child
        else:
            items[key] = None
            i += 1
    return (seq if mode == "list" else items), max(i, start + 1)


def read_metadata(text: str):
    """Return the parsed document_metadata block, or None when absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        closing = next(
            i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")
        )
    except StopIteration:
        raise ParseError("frontmatter opened with '---' but never closed")
    block = lines[1:closing]
    for i, line in enumerate(block):
        if line.startswith(GOVERNED_ENTRY + ":"):
            parsed, _ = parse_block(block, 1, i + 1, len(block))
            return parsed if isinstance(parsed, dict) else {}
    return None


def dig(data: dict, *path, default=None):
    cur = data
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def check_document(path: Path, text: str) -> tuple[list[str], dict | None]:
    """Return (errors, metadata). Empty errors means the file conforms."""
    try:
        meta = read_metadata(text)
    except ParseError as exc:
        return [f"DM-01 frontmatter unparseable: {exc}"], None

    if meta is None:
        # Not yet adopted. Reported by the caller as an adoption gap, not an
        # error, so progressive adoption stays possible (policy §8).
        return [], None

    errors: list[str] = []

    # DM-01 required dimensions present.
    for field in ("domain", "role", "lifecycle", "authority"):
        if meta.get(field) is None:
            errors.append(f"DM-01 missing required dimension: {field}")

    domain = meta.get("domain")
    role = meta.get("role")
    if domain is not None and domain not in DOMAINS:
        errors.append(f"DM-02 domain not in enumeration: {domain!r}")
    if role is not None and role not in ROLES:
        errors.append(f"DM-02 role not in enumeration: {role!r}")

    lifecycle = meta.get("lifecycle") or {}
    authority = meta.get("authority") or {}
    approval = lifecycle.get("approval") or {}

    decision = approval.get("decision_status")
    if decision is not None and decision not in DECISION_STATUSES:
        errors.append(f"DM-02 decision_status invalid: {decision!r}")

    usage = lifecycle.get("usage_status")
    if usage is not None and usage not in USAGE_STATUSES:
        errors.append(f"DM-02 usage_status invalid: {usage!r}")

    modification = lifecycle.get("modification_status")
    if modification is not None and modification not in MODIFICATION_STATUSES:
        errors.append(f"DM-02 modification_status invalid: {modification!r}")

    verification = dig(lifecycle, "evidence_verification", "verification_status")
    if verification is not None and verification not in VERIFICATION_STATUSES:
        errors.append(f"DM-02 verification_status invalid: {verification!r}")

    # DM-03 Approved must bind a version and a scope.
    if decision == "Approved":
        version_value = dig(approval, "approved_version", "value")
        if not version_value:
            errors.append("DM-03 Approved requires approval.approved_version.value")
        scope_type = dig(approval, "approval_scope", "type")
        if not scope_type:
            errors.append("DM-03 Approved requires approval.approval_scope.type")

    # DM-04 Revoked must carry a unique revocation decision id.
    if decision == "Revoked":
        revocation = approval.get("revocation")
        if not isinstance(revocation, dict):
            errors.append("DM-04 Revoked requires a revocation block")
        elif not revocation.get("revocation_decision_id"):
            errors.append(
                "DM-04 Revoked requires revocation.revocation_decision_id"
            )

    # DM-05 Archived must record when and why.
    if usage == "Archived":
        if not dig(lifecycle, "archival", "archived_date"):
            errors.append("DM-05 Archived requires archival.archived_date")
        if not dig(lifecycle, "archival", "archival_reason"):
            errors.append("DM-05 Archived requires archival.archival_reason")

    canonical = authority.get("canonical_status")
    if canonical is not None and canonical not in CANONICAL_STATUSES:
        errors.append(f"DM-02 canonical_status invalid: {canonical!r}")

    normative = authority.get("normative_status")
    if normative is not None and normative not in NORMATIVE_STATUSES:
        errors.append(f"DM-02 normative_status invalid: {normative!r}")

    conflict = authority.get("canonical_conflict_status")
    if conflict is not None and conflict not in CONFLICT_STATUSES:
        errors.append(f"DM-02 canonical_conflict_status invalid: {conflict!r}")

    # DM-06 Canonical must declare a normalized scope.
    if canonical == "Canonical":
        scope_id = authority.get("canonical_scope_id")
        if not scope_id:
            errors.append("DM-06 Canonical requires authority.canonical_scope_id")
        elif not SCOPE_ID_RE.match(str(scope_id)):
            errors.append(
                f"DM-06 canonical_scope_id not normalized "
                f"(expect '<domain>/<kebab-case>'): {scope_id!r}"
            )
        keywords = authority.get("canonical_scope_keywords")
        if not keywords or not isinstance(keywords, list):
            errors.append(
                "DM-06 Canonical requires non-empty canonical_scope_keywords"
            )

    # DM-08 Reverse relation must never be hand-written.
    if isinstance(dig(lifecycle, "supersession"), dict):
        if "superseded_by" in lifecycle["supersession"]:
            errors.append(
                "DM-08 superseded_by is CI-derived and MUST NOT be hand-written"
            )

    return errors, meta


def governed_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in NORMATIVE_ROOTS:
        base = root / name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            if any(rel.startswith(prefix) for prefix in EXEMPT_PREFIXES):
                continue
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat documents without metadata as errors (use once adopted)",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=None,
        help="restrict the run to these repository-relative paths",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    targets = (
        [root / p for p in args.only]
        if args.only
        else governed_files(root)
    )

    errors: list[str] = []
    canonical_scopes: dict[str, list[str]] = {}
    classified = 0
    unclassified: list[str] = []

    for path in targets:
        if not path.is_file():
            errors.append(f"DM-01 not a file: {path}")
            continue
        rel = path.relative_to(root).as_posix()
        file_errors, meta = check_document(path, path.read_text(encoding="utf-8"))
        errors.extend(f"{rel}: {err}" for err in file_errors)
        if meta is None:
            unclassified.append(rel)
            continue
        classified += 1
        if dig(meta, "authority", "canonical_status") == "Canonical":
            scope_id = dig(meta, "authority", "canonical_scope_id")
            if scope_id:
                canonical_scopes.setdefault(str(scope_id), []).append(rel)

    # DM-07 at most one Canonical per scope.
    for scope_id, owners in canonical_scopes.items():
        if len(owners) > 1:
            errors.append(
                f"DM-07 scope {scope_id!r} has {len(owners)} Canonical documents: "
                + ", ".join(sorted(owners))
            )

    if args.strict:
        for rel in unclassified:
            errors.append(f"DM-01 missing {GOVERNED_ENTRY} block: {rel}")

    total = len(targets)
    print(
        f"GOV-DOC-002: {total} governed documents, "
        f"{classified} classified, {len(unclassified)} unclassified"
    )
    if unclassified and not args.strict:
        preview = ", ".join(unclassified[:5])
        suffix = "" if len(unclassified) <= 5 else f", ... (+{len(unclassified) - 5})"
        print(f"  adoption backlog: {preview}{suffix}")

    if errors:
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print("PASS: no GOV-DOC-002 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
