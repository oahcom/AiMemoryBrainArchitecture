#!/usr/bin/env python3
"""GOV-DOC-002 document management gate.

Validates the four-dimension metadata block declared at the top of governed
Markdown files. Rules are listed in
00-governance/architecture-document-management-policy.md 9 (DM-01 .. DM-13).

Trust boundary: the metadata parser is fail-closed. Any input that is not in
the documented YAML subset is an error, never a silently skipped line. If the
parse result cannot be trusted, no downstream rule result can be either.

Checked mechanically (DM-01 .. DM-13). NOT checked mechanically, and reported
as manual controls on every run: whether a scope is genuinely non-overlapping,
whether evidence supports a decision, whether selected sections are the right
ones, and whether the document body and its mirror say the same thing.

No third-party dependency: PyYAML is unavailable in this environment, so the
supported subset is declared in _SUBSET below and everything else is rejected.

    python3 scripts/check_document_management.py
    python3 scripts/check_document_management.py --require-changed origin/main
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
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
APPLICABILITY = {
    "Applicable-To-Current-Version", "Not-Applicable-To-Current-Version",
}
SCOPE_TYPES = {"Full-document", "Selected-sections", "Selected-assets"}
VERSION_SCHEMES = {"git", "content-hash"}

# Unknown keys are errors. A misspelled governance field is otherwise invisible.
TOP_KEYS = {"domain", "role", "lifecycle", "authority", "bilingual_counterpart"}
LIFECYCLE_KEYS = {
    "approval", "evidence_verification", "usage_status",
    "modification_status", "supersession", "archival",
}
APPROVAL_KEYS = {
    "decision_status", "approver", "decision_date", "approved_version",
    "approval_scope", "approval_applicability", "evidence_reference",
    "revocation",
}
VERSION_KEYS = {"scheme", "value"}
SCOPE_KEYS = {"type", "included_sections", "included_assets"}
REVOCATION_KEYS = {
    "revocation_decision_id", "revoked_date", "revoker", "revocation_reason",
    "revocation_evidence", "superseding_document",
}
EVIDENCE_KEYS = {
    "verification_status", "last_verified_date", "last_verification_note",
}
SUPERSESSION_KEYS = {"supersedes", "supersession_reason", "effective_date"}
ARCHIVAL_KEYS = {"archived_date", "archival_reason", "archival_reference"}
AUTHORITY_KEYS = {
    "canonical_status", "canonical_scope", "canonical_scope_id",
    "canonical_scope_keywords", "canonical_conflict_status",
    "canonical_conflict_resolution", "normative_status",
}
RESOLUTION_KEYS = {
    "resolution_decision_id", "resolved_date", "selected_document",
    "resolution_evidence",
}
BILINGUAL_KEYS = {"en", "zh-CN"}

SCOPE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*/[a-z0-9]+(-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")

class ParseError(Exception):
    pass


# --------------------------------------------------------------------------
# Strict YAML-subset reader
# --------------------------------------------------------------------------

def _strip_comment(line: str, lineno: int = 0) -> str:
    """Remove a trailing ' # comment', honouring quotes and backslash escapes."""
    out: list[str] = []
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote == '"':
            out.append(ch)
            if ch == "\\" and i + 1 < len(line):
                out.append(line[i + 1])
                i += 2
                continue
            if ch == '"':
                quote = None
            i += 1
            continue
        if quote == "'":
            out.append(ch)
            if ch == "'":
                if i + 1 < len(line) and line[i + 1] == "'":
                    out.append("'")
                    i += 2
                    continue
                quote = None
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "#" and (not out or out[-1] in " \t"):
            break
        out.append(ch)
        i += 1
    if quote:
        raise ParseError(f"line {lineno}: unterminated {quote} quote")
    return "".join(out).rstrip()


def _scalar(text: str, lineno: int):
    text = text.strip()
    if text in ("", "null", "NaN"):
        return None
    if text == "[]":
        return []
    if text == "{}":
        return {}
    if text in ("true", "True"):
        return True
    if text in ("false", "False"):
        return False
    first = text[0]
    if first in "[{&*!|>%@`,?":
        raise ParseError(
            f"line {lineno}: unsupported YAML construct starting with {first!r} "
            f"in {text!r} (see module docstring for the accepted subset)"
        )
    if first == '"':
        if len(text) < 2 or text[-1] != '"':
            raise ParseError(f"line {lineno}: unterminated double-quoted scalar")
        try:
            return json.loads(text)
        except ValueError:
            raise ParseError(f"line {lineno}: invalid escape in {text!r}")
    if first == "'":
        if len(text) < 2 or text[-1] != "'":
            raise ParseError(f"line {lineno}: unterminated single-quoted scalar")
        return text[1:-1].replace("''", "'")
    return text


def _tokens(lines: list[str], offset: int) -> list[tuple[int, int, str]]:
    """(lineno, indent, content) for every non-blank, non-comment line."""
    out: list[tuple[int, int, str]] = []
    for index, raw in enumerate(lines):
        lineno = offset + index
        if "\t" in raw:
            raise ParseError(f"line {lineno}: tab character (use spaces)")
        text = _strip_comment(raw, lineno)
        if not text.strip():
            continue
        indent = len(text) - len(text.lstrip(" "))
        out.append((lineno, indent, text[indent:]))
    return out


def _parse_map(tokens, pos: int, indent: int):
    mapping: dict = {}
    while pos < len(tokens):
        lineno, ind, text = tokens[pos]
        if ind < indent:
            break
        if ind > indent:
            raise ParseError(
                f"line {lineno}: unexpected indentation {ind}, expected {indent}"
            )
        if text.startswith("- ") or text == "-":
            raise ParseError(
                f"line {lineno}: sequence item inside a mapping block"
            )
        if ":" not in text:
            raise ParseError(
                f"line {lineno}: neither 'key: value' nor '- item': {text!r}"
            )
        key, _, rest = text.partition(":")
        key, rest = key.strip(), rest.strip()
        if not KEY_RE.match(key):
            raise ParseError(f"line {lineno}: invalid key {key!r}")
        if key in mapping:
            raise ParseError(f"line {lineno}: duplicate key {key!r}")
        pos += 1
        if rest:
            mapping[key] = _scalar(rest, lineno)
        elif pos < len(tokens) and tokens[pos][1] > indent:
            mapping[key], pos = _parse_block(tokens, pos, tokens[pos][1])
        else:
            mapping[key] = None
    return mapping, pos


def _parse_seq(tokens, pos: int, indent: int):
    items: list = []
    while pos < len(tokens):
        lineno, ind, text = tokens[pos]
        if ind < indent:
            break
        if ind > indent:
            raise ParseError(
                f"line {lineno}: unexpected indentation inside a sequence"
            )
        if not (text.startswith("- ") or text == "-"):
            raise ParseError(
                f"line {lineno}: mapping entry inside a sequence block"
            )
        body = text[1:].strip()
        if not body:
            raise ParseError(f"line {lineno}: empty sequence item")
        if body.startswith("- "):
            raise ParseError(f"line {lineno}: nested sequences are not supported")
        if ": " in body or body.endswith(":"):
            raise ParseError(
                f"line {lineno}: sequence item looks like a mapping "
                f"({body!r}); mappings inside sequences are not supported"
            )
        items.append(_scalar(body, lineno))
        pos += 1
    return items, pos


def _parse_block(tokens, pos: int, indent: int):
    if pos >= len(tokens):
        raise ParseError("unexpected end of block")
    text = tokens[pos][2]
    if text.startswith("- ") or text == "-":
        return _parse_seq(tokens, pos, indent)
    return _parse_map(tokens, pos, indent)


def read_metadata(text: str) -> dict | None:
    """Return the parsed document_metadata mapping, or None when absent.

    Raises ParseError for anything that is not in the declared subset.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    closing = next(
        (i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")),
        None,
    )
    if closing is None:
        raise ParseError("frontmatter opened with '---' but never closed")
    block = lines[1:closing]

    starts = [
        i for i, line in enumerate(block)
        if line.lstrip().startswith(GOVERNED_ENTRY + ":")
    ]
    if not starts:
        return None
    if len(starts) > 1:
        raise ParseError(f"duplicate {GOVERNED_ENTRY} block")
    start = starts[0]
    if block[start] != block[start].lstrip():
        raise ParseError(f"{GOVERNED_ENTRY} must start at column 0")
    if block[start].split(":", 1)[1].strip():
        raise ParseError(f"{GOVERNED_ENTRY} must be a mapping block, not a scalar")

    tokens = _tokens(block[start + 1:], offset=start + 2)
    if not tokens:
        raise ParseError(f"{GOVERNED_ENTRY} block is empty")
    if tokens[0][1] == 0:
        raise ParseError(f"first key of {GOVERNED_ENTRY} must be indented")
    meta, pos = _parse_block(tokens, 0, tokens[0][1])
    if pos != len(tokens):
        lineno = tokens[pos][0]
        raise ParseError(f"line {lineno}: unparsed input remains after the block")
    if not isinstance(meta, dict):
        raise ParseError(f"{GOVERNED_ENTRY} must be a mapping")
    return meta


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def dig(data, *path, default=None):
    cur = data
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def unknown_keys(node, allowed: set[str], where: str) -> list[str]:
    if not isinstance(node, dict):
        return [f"{where} must be a mapping, got {type(node).__name__}"]
    return [
        f"{where}.{key}: unknown key (allowed: {', '.join(sorted(allowed))})"
        for key in node
        if key not in allowed
    ]


def walk_keys(node, name: str, path: str = ""):
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key == name:
                yield here
            yield from walk_keys(value, name, here)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_keys(value, name, f"{path}[{index}]")


def body_text(text: str) -> str:
    """Document body without its own frontmatter.

    An approval binds to document content, not to the governance metadata.
    """
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return "\n".join(lines[i + 1:])
    return text


def body_hash(text: str) -> str:
    normalised = "\n".join(line.rstrip() for line in body_text(text).splitlines())
    return hashlib.sha256((normalised.strip() + "\n").encode()).hexdigest()


def _enum(errors, value, allowed, label, rule="DM-02"):
    if value is not None and value not in allowed:
        errors.append(f"{rule} {label} not in enumeration: {value!r}")


def check_document(path: Path, text: str) -> tuple[list[str], dict | None]:
    """Return (errors, metadata). Empty errors means the file conforms."""
    try:
        meta = read_metadata(text)
    except ParseError as exc:
        return [f"DM-01 frontmatter unparseable: {exc}"], None

    if meta is None:
        # Not yet classified. The caller decides whether that is an error
        # (changed file or --strict) or an adoption gap (policy 8).
        return [], None

    errors: list[str] = []

    # DM-01 structure.
    errors += unknown_keys(meta, TOP_KEYS, GOVERNED_ENTRY)
    for field in ("domain", "role", "lifecycle", "authority"):
        if meta.get(field) is None:
            errors.append(f"DM-01 missing required dimension: {field}")
    lifecycle = meta.get("lifecycle") or {}
    authority = meta.get("authority") or {}
    errors += unknown_keys(lifecycle, LIFECYCLE_KEYS, "lifecycle") if lifecycle else []
    errors += unknown_keys(authority, AUTHORITY_KEYS, "authority") if authority else []
    if "bilingual_counterpart" in meta and meta["bilingual_counterpart"] is not None:
        errors += unknown_keys(
            meta["bilingual_counterpart"], BILINGUAL_KEYS, "bilingual_counterpart"
        )

    # DM-02 closed enumerations.
    domain, role = meta.get("domain"), meta.get("role")
    _enum(errors, domain, DOMAINS, "domain")
    _enum(errors, role, ROLES, "role")
    approval = lifecycle.get("approval") or {}
    if approval:
        errors += unknown_keys(approval, APPROVAL_KEYS, "lifecycle.approval")
    decision = approval.get("decision_status")
    _enum(errors, decision, DECISION_STATUSES, "decision_status")
    usage = lifecycle.get("usage_status")
    _enum(errors, usage, USAGE_STATUSES, "usage_status")
    modification = lifecycle.get("modification_status")
    _enum(errors, modification, MODIFICATION_STATUSES, "modification_status")
    applicability = approval.get("approval_applicability")
    _enum(errors, applicability, APPLICABILITY, "approval_applicability")
    verification_block = lifecycle.get("evidence_verification") or {}
    if verification_block:
        errors += unknown_keys(
            verification_block, EVIDENCE_KEYS, "lifecycle.evidence_verification"
        )
    verification = verification_block.get("verification_status")
    _enum(errors, verification, VERIFICATION_STATUSES, "verification_status")
    canonical = authority.get("canonical_status")
    _enum(errors, canonical, CANONICAL_STATUSES, "canonical_status")
    normative = authority.get("normative_status")
    _enum(errors, normative, NORMATIVE_STATUSES, "normative_status")
    conflict = authority.get("canonical_conflict_status")
    _enum(errors, conflict, CONFLICT_STATUSES, "canonical_conflict_status")

    # DM-03 Approved must bind a version and a scope.
    version = approval.get("approved_version")
    scope = approval.get("approval_scope")
    if version is not None:
        errors += unknown_keys(version, VERSION_KEYS, "approved_version")
        _enum(errors, version.get("scheme"), VERSION_SCHEMES, "approved_version.scheme")
    if scope is not None:
        errors += unknown_keys(scope, SCOPE_KEYS, "approval_scope")
        _enum(errors, scope.get("type"), SCOPE_TYPES, "approval_scope.type")
    if decision == "Approved":
        if not dig(approval, "approved_version", "value"):
            errors.append("DM-03 Approved requires approval.approved_version.value")
        if not dig(approval, "approval_scope", "type"):
            errors.append("DM-03 Approved requires approval.approval_scope.type")
        if not applicability:
            errors.append("DM-03 Approved requires approval.approval_applicability")
    if dig(approval, "approval_scope", "type") == "Selected-sections":
        sections = dig(approval, "approval_scope", "included_sections")
        if not sections or not isinstance(sections, list):
            errors.append(
                "DM-03 Selected-sections requires a non-empty included_sections list"
            )

    # DM-04 Revoked must carry a unique revocation decision id.
    revocation = approval.get("revocation")
    if revocation is not None:
        errors += unknown_keys(revocation, REVOCATION_KEYS, "revocation")
    if decision == "Revoked":
        if not isinstance(revocation, dict):
            errors.append("DM-04 Revoked requires a revocation block")
        else:
            if not revocation.get("revocation_decision_id"):
                errors.append(
                    "DM-04 Revoked requires revocation.revocation_decision_id"
                )
            if not revocation.get("revoked_date"):
                errors.append("DM-04 Revoked requires revocation.revoked_date")
            if not revocation.get("revocation_reason"):
                errors.append("DM-04 Revoked requires revocation.revocation_reason")

    # DM-05 Archived must record when and why.
    archival = lifecycle.get("archival")
    if archival is not None:
        errors += unknown_keys(archival, ARCHIVAL_KEYS, "archival")
    if usage == "Archived":
        if not dig(lifecycle, "archival", "archived_date"):
            errors.append("DM-05 Archived requires archival.archived_date")
        if not dig(lifecycle, "archival", "archival_reason"):
            errors.append("DM-05 Archived requires archival.archival_reason")

    # DM-06 Canonical must declare a normalised scope consistent with domain.
    if canonical in ("Canonical", "Candidate"):
        scope_id = authority.get("canonical_scope_id")
        if not scope_id:
            errors.append("DM-06 Canonical requires authority.canonical_scope_id")
        elif not SCOPE_ID_RE.match(str(scope_id)):
            errors.append(
                f"DM-06 canonical_scope_id not normalized "
                f"(expect '<domain>/<kebab-case>'): {scope_id!r}"
            )
        elif domain is not None and str(scope_id).split("/")[0] != domain:
            errors.append(
                f"DM-06 canonical_scope_id prefix {str(scope_id).split('/')[0]!r} "
                f"must equal the declared domain {domain!r}"
            )
    if canonical == "Canonical":
        if not authority.get("canonical_scope"):
            errors.append("DM-06 Canonical requires authority.canonical_scope")
        keywords = authority.get("canonical_scope_keywords")
        if not keywords or not isinstance(keywords, list):
            errors.append("DM-06 Canonical requires non-empty canonical_scope_keywords")
        elif any(not isinstance(k, str) or not k.strip() for k in keywords):
            errors.append("DM-06 canonical_scope_keywords entries must be non-empty strings")

    # DM-08 Reverse relation is CI-derived, never hand-written (anywhere).
    for where in walk_keys(meta, "superseded_by"):
        errors.append(f"DM-08 {where} is CI-derived and MUST NOT be hand-written")

    # DM-11 Conflict state must not double as authority.
    if canonical == "Canonical" and conflict in ("Under-Review",):
        errors.append(
            "DM-11 a document under canonical conflict MUST NOT be Canonical; "
            "set canonical_status: Candidate until the conflict is resolved"
        )
    resolution = authority.get("canonical_conflict_resolution")
    if resolution is not None:
        errors += unknown_keys(resolution, RESOLUTION_KEYS, "canonical_conflict_resolution")
        if not dig(resolution, "resolution_decision_id"):
            errors.append("DM-11 resolution requires resolution_decision_id")
        if not dig(resolution, "selected_document"):
            errors.append("DM-11 resolution requires selected_document")
        if not dig(resolution, "resolved_date"):
            errors.append("DM-11 resolution requires resolved_date")
    if conflict == "Resolved" and not isinstance(resolution, dict):
        errors.append("DM-11 canonical_conflict_status: Resolved requires a resolution block")

    # DM-09 Generated artifacts must not claim authority.
    if first_body_lines(text) and GENERATED_MARKER.search(first_body_lines(text)):
        if normative == "Normative" or canonical == "Canonical":
            errors.append(
                "DM-09 a generated artifact MUST NOT be Normative or Canonical; "
                "the Markdown source is the authority (policy 7)"
            )

    return errors, meta


GENERATED_MARKER = re.compile(r"GENERATED[ -](FILE|ARTIFACT)|DO NOT EDIT", re.I)


def first_body_lines(text: str, count: int = 8) -> str:
    return "\n".join(body_text(text).splitlines()[:count])


# --------------------------------------------------------------------------
# Repository-wide checks
# --------------------------------------------------------------------------

NO_AUTHORITATIVE_SOURCE = "NO_AUTHORITATIVE_SOURCE"


def resolve_canonical(docs: dict[str, dict], scope_id: str) -> str:
    """The only sanctioned way to resolve authority for a scope.

    Never guesses. Returns NO_AUTHORITATIVE_SOURCE when the scope has no
    document, has an unresolved conflict, or has more than one Canonical.
    There is deliberately no fallback to approval dates: an earlier approval
    is not evidence of authority, and a silent fallback hides the conflict.
    """
    scope = [
        rel for rel, meta in docs.items()
        if dig(meta, "authority", "canonical_scope_id") == scope_id
    ]
    if not scope:
        return NO_AUTHORITATIVE_SOURCE
    if any(
        dig(docs[rel], "authority", "canonical_conflict_status") not in (None, "None")
        for rel in scope
    ):
        return NO_AUTHORITATIVE_SOURCE
    canonical = [
        rel for rel in scope
        if dig(docs[rel], "authority", "canonical_status") == "Canonical"
    ]
    return canonical[0] if len(canonical) == 1 else NO_AUTHORITATIVE_SOURCE


def git(root: Path, *args: str) -> str | None:
    """Run git, returning stdout or None when unavailable/failing."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def check_approval_binding(root: Path, rel: str, text: str, meta: dict,
                           is_git: bool) -> tuple[list[str], list[str]]:
    """DM-10: an Approved decision binds to a version, and must go stale."""
    errors: list[str] = []
    notes: list[str] = []
    approval = dig(meta, "lifecycle", "approval") or {}
    if approval.get("decision_status") != "Approved":
        return errors, notes
    scheme = dig(approval, "approved_version", "scheme")
    value = dig(approval, "approved_version", "value")
    if not scheme or not value:
        return errors, notes  # DM-03 already reported it.
    current = body_hash(text)

    if scheme == "content-hash":
        recorded = str(value).strip().lower()
        stale = recorded != current
    else:
        if not is_git:
            notes.append(
                f"DM-10 {rel}: approval binding NOT VERIFIED (no git work tree); "
                "run the gate inside the repository"
            )
            return errors, notes
        commit = git(root, "rev-parse", "--verify", "--quiet", f"{value}^{{commit}}")
        if not commit:
            errors.append(
                f"DM-10 approved_version {value!r} is not a commit in this repository"
            )
            return errors, notes
        historical = git(root, "show", f"{commit}:{rel}")
        if historical is None:
            errors.append(
                f"DM-10 {rel} did not exist at approved_version {value[:12]}; "
                "the approval cannot be bound to that version"
            )
            return errors, notes
        stale = body_hash(historical) != current

    if not stale:
        if approval.get("approval_applicability") == "Not-Applicable-To-Current-Version":
            notes.append(
                f"DM-10 {rel}: text is unchanged since approved_version, but "
                "approval_applicability says otherwise (conservative, allowed)"
            )
        return errors, notes

    if dig(meta, "lifecycle", "modification_status") != "Pending-Reapproval":        errors.append(
            "DM-10 content changed after approved_version: "
            "modification_status MUST be Pending-Reapproval"
        )
    if approval.get("approval_applicability") != "Not-Applicable-To-Current-Version":
        errors.append(
            "DM-10 content changed after approved_version: approval_applicability "
            "MUST be Not-Applicable-To-Current-Version (a stale approval MUST NOT "
            "be presented as current)"
        )
    return errors, notes


def check_scope_and_relations(root: Path, docs: dict[str, dict]) -> list[str]:
    """DM-07 uniqueness, DM-11 resolution integrity, DM-12 mirror, DM-13 graph."""
    errors: list[str] = []
    scopes: dict[str, list[str]] = {}
    for rel, meta in docs.items():
        scope_id = dig(meta, "authority", "canonical_scope_id")
        if scope_id:
            scopes.setdefault(str(scope_id), []).append(rel)

    for scope_id, owners in sorted(scopes.items()):
        canonical = [
            rel for rel in owners
            if dig(docs[rel], "authority", "canonical_status") == "Canonical"
        ]
        if len(canonical) > 1:
            errors.append(
                f"DM-07 scope {scope_id!r} has {len(canonical)} Canonical documents: "
                + ", ".join(sorted(canonical))
            )
        resolutions = [
            (rel, dig(docs[rel], "authority", "canonical_conflict_resolution"))
            for rel in owners
            if isinstance(dig(docs[rel], "authority", "canonical_conflict_resolution"), dict)
        ]
        if resolutions:
            if len(resolutions) > 1:
                errors.append(
                    f"DM-11 scope {scope_id!r} has {len(resolutions)} resolution "
                    "records: " + ", ".join(sorted(rel for rel, _ in resolutions))
                )
            selected = dig(resolutions[0][1], "selected_document")
            if selected and selected not in owners:
                errors.append(
                    f"DM-11 scope {scope_id!r} resolution selects {selected!r}, "
                    "which does not declare this scope"
                )
            elif selected and canonical and canonical != [selected]:
                errors.append(
                    f"DM-11 scope {scope_id!r} resolution selects {selected!r} "
                    f"but Canonical is {canonical[0]!r}"
                )

        # DM-10 conflict visibility: an unresolved conflict must not resolve.
        if resolve_canonical(docs, scope_id) == NO_AUTHORITATIVE_SOURCE:
            conflicted = [
                rel for rel in owners
                if dig(docs[rel], "authority", "canonical_conflict_status")
                in ("Under-Review", "Resolved")
            ]
            if conflicted:
                print(f"  conflict: scope {scope_id!r} has no authoritative source")

    # DM-12 bilingual counterpart.
    for rel, meta in docs.items():
        counterpart = meta.get("bilingual_counterpart")
        if not isinstance(counterpart, dict):
            continue
        for lang, target in counterpart.items():
            if not target:
                continue
            target_rel = str(target).lstrip("./")
            if target_rel == rel:
                errors.append(f"DM-12 {rel}: bilingual_counterpart.{lang} points to itself")
                continue
            if not (root / target_rel).is_file():
                errors.append(
                    f"DM-12 {rel}: bilingual_counterpart.{lang} does not exist: "
                    f"{target_rel}"
                )
                continue
            other = docs.get(target_rel)
            if other is None:
                continue
            for field in (("domain",), ("role",), ("authority", "normative_status")):
                mine, theirs = dig(meta, *field), dig(other, *field)
                if mine != theirs:
                    errors.append(
                        f"DM-12 {rel}: {'.'.join(field)} {mine!r} disagrees with "
                        f"{target_rel} ({theirs!r})"
                    )
            # Only one carrier of canonical authority; the mirror is a copy.
            if dig(other, "authority", "canonical_status") == "Canonical" and (
                dig(meta, "authority", "canonical_status") == "Canonical"
            ):
                errors.append(
                    f"DM-12 {rel}: both a document and its mirror claim Canonical "
                    f"({target_rel})"
                )

    # DM-13 supersession graph.
    graph: dict[str, list[str]] = {}
    for rel, meta in docs.items():
        targets = dig(meta, "lifecycle", "supersession", "supersedes")
        if not targets:
            continue
        if not isinstance(targets, list):
            errors.append(f"DM-13 {rel}: supersedes must be a list")
            continue
        resolved: list[str] = []
        for target in targets:
            target_rel = str(target).lstrip("./")
            if target_rel == rel:
                errors.append(f"DM-13 {rel}: a document cannot supersede itself")
                continue
            if not (root / target_rel).is_file():
                errors.append(
                    f"DM-13 {rel}: supersedes target does not exist: {target_rel}"
                )
                continue
            resolved.append(target_rel)
        graph[rel] = resolved

    def visit(node: str, path: list[str]) -> None:
        for target in graph.get(node, []):
            if target in path:
                errors.append(
                    "DM-13 supersession cycle: " + " -> ".join(path + [target])
                )
                return
            visit(target, path + [target])

    for node in graph:
        visit(node, [node])

    return errors


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

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


def changed_paths(root: Path, ref: str) -> set[str]:
    names: set[str] = set()
    diff = git(root, "diff", "--name-only", "--diff-filter=AMR", f"{ref}...HEAD")
    if diff is None:
        diff = git(root, "diff", "--name-only", "--diff-filter=AMR", ref)
    if diff is None:
        raise SystemExit(f"cannot diff against {ref!r}; is this a git work tree?")
    names.update(diff.split())
    untracked = git(root, "ls-files", "--others", "--exclude-standard") or ""
    names.update(untracked.split())
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--strict", action="store_true",
        help="treat every unclassified governed document as an error",
    )
    parser.add_argument(
        "--only", nargs="*", default=None,
        help="restrict the run to these repository-relative paths",
    )
    parser.add_argument(
        "--require-changed", metavar="REF", default=None,
        help="require metadata on every governed file changed since REF",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    targets = [root / p for p in args.only] if args.only else governed_files(root)  # noqa: E501
    required = changed_paths(root, args.require_changed) if args.require_changed else set()
    is_git = git(root, "rev-parse", "--git-dir") is not None

    errors: list[str] = []
    notes: list[str] = []
    docs: dict[str, dict] = {}
    unclassified: list[str] = []
    per_root: dict[str, list[int]] = {}

    for path in targets:
        if not path.is_file():
            errors.append(f"DM-01 not a file: {path}")
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            errors.append(f"DM-01 outside the repository root: {path}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"DM-01 not valid UTF-8: {rel}")
            continue
        file_errors, meta = check_document(path, text)
        errors.extend(f"{rel}: {err}" for err in file_errors)

        bucket = per_root.setdefault(rel.split("/")[0] if "/" in rel else rel, [0, 0])
        bucket[1] += 1
        if meta is None:
            unclassified.append(rel)
            if rel in required or args.strict:
                errors.append(f"DM-01 missing {GOVERNED_ENTRY} block: {rel}")
            continue
        bucket[0] += 1
        docs[rel] = meta
        bound_errors, bound_notes = check_approval_binding(root, rel, text, meta, is_git)
        errors.extend(f"{rel}: {err}" for err in bound_errors)
        notes.extend(bound_notes)

    errors.extend(check_scope_and_relations(root, docs))

    # DM-04 uniqueness of revocation decision ids across the repository.
    revocations: dict[str, str] = {}
    for rel, meta in docs.items():
        rev_id = dig(meta, "lifecycle", "approval", "revocation", "revocation_decision_id")
        if rev_id:
            if rev_id in revocations:
                errors.append(
                    f"DM-04 revocation_decision_id {rev_id!r} reused by "
                    f"{revocations[rev_id]} and {rel}"
                )
            revocations[rev_id] = rel

    total = len(targets)
    print(
        f"GOV-DOC-002: {total} governed documents, {len(docs)} classified, "
        f"{len(unclassified)} unclassified"
    )
    for name in sorted(per_root):
        done, seen = per_root[name]
        print(f"  {name}: {done}/{seen} classified")
    if unclassified:
        preview = ", ".join(unclassified[:5])
        suffix = "" if len(unclassified) <= 5 else f", ... (+{len(unclassified) - 5})"
        print(f"  adoption backlog: {preview}{suffix}")

    # Executable evidence that authority is resolved, not guessed.
    scopes = sorted({
        str(dig(meta, "authority", "canonical_scope_id"))
        for meta in docs.values()
        if dig(meta, "authority", "canonical_scope_id")
    })
    for scope_id in scopes:
        print(f"  authority: {scope_id} -> {resolve_canonical(docs, scope_id)}")

    print(
        "  manual controls (not machine-verified): canonical scope overlap; "
        "truth of an approval or evidence claim; chosen Selected-sections; "
        "semantic parity of bilingual mirrors; consumption discipline of "
        "external readers (use resolve_canonical, never ad-hoc logic)"
    )
    for note in notes:
        print(f"  note: {note}")

    if not is_git:
        print("  note: no git work tree here, approval binding NOT VERIFIED")

    if errors:
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print("PASS: no GOV-DOC-002 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
