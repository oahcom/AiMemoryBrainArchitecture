#!/usr/bin/env python3
"""GOV-DOC-002 document management gate.

Validates the four-dimension metadata block declared at the top of governed
Markdown files. Rules are listed in
00-governance/architecture-document-management-policy.md 9 (DM-01 .. DM-14).

Trust boundary: the metadata parser is fail-closed. Any input that is not in
the documented YAML subset is an error, never a silently skipped line. If the
parse result cannot be trusted, no downstream rule result can be either.

Checked mechanically (DM-01 .. DM-14). NOT checked mechanically, and printed on
every run as `manual controls (policy 9.2)`: the ten items M-01 .. M-10, from
whether a scope is genuinely non-overlapping to whether an exclusion reason is
honest. `MANUAL_CONTROLS` below is the single authority: policy section 9.2 is
rendered from it, and the run prints each entry's id and control. T69 does not
compare two lists -- it re-renders the table from the constant and compares
bytes, because two independently maintained lists with a synchronisation test
is the defect this file keeps finding.

No third-party dependency: PyYAML is unavailable in this environment, so the
supported subset is declared in _SUBSET below and everything else is rejected.

    python3 scripts/check_document_management.py
    python3 scripts/check_document_management.py --require-changed origin/main
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Normative roots come from the bilingual gate, so the two gates can never
# disagree about which directories are governed. Duplicating the list is
# how 08-protocols silently stopped existing.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_bilingual_docs import NORMATIVE_ROOTS as _BILINGUAL_ROOTS  # noqa: E402

NORMATIVE_ROOTS = tuple(sorted(_BILINGUAL_ROOTS)) + (
    # Bilingual mirrors. Counted so mirror drift is visible instead of falling
    # outside the audit entirely.
    "docs/en", "docs/zh-CN",
)
# Individual files that are governed although their directory is not. The gap
# register is the case that forced this: the policy cites it in three places as
# the record of what is unclosed, so a change to it that escapes GOV-DOC-002
# would let the governance record drift outside governance. A directory would
# pull in unrelated pages; one path keeps the exception as small as the reason.
GOVERNED_FILES = ("docs/governance/documentation-gaps.md",)
# Two exclusion kinds, never blurred (policy section 2). "not documentation"
# makes no architecture claim; "not yet migrated" IS documentation and is
# backlog, so it is a gap the policy names rather than an exclusion it grants.
# There is exactly one kind of exclusion. `not-yet-migrated` used to be a second
# one, which contradicted the policy: section 2 calls it backlog that "is a gap
# the policy must name rather than an exclusion it may grant itself". Allowing it
# here let 27 architecture documents under docs/ be excluded from the gate while
# still being described as governed-in-spirit -- the exact blur the registry
# exists to prevent. Such directories now go in `backlog:`, are scanned, and
# count as unclassified, so the number is real and can go down.
EXCLUSION_KINDS = {"not-documentation"}
# No path exemptions. A bilingual *pairing* exemption is not a *governance*
# exemption: `PAIR_EXEMPT_PREFIXES` in check_bilingual_docs.py means "this file
# need not have a translated twin", which says nothing about whether it is a
# governed document. Importing it here used to shrink the governed set silently
# by 89 files (work-items, prompts, adr). If a path must be out of scope, say so
# in policy section 2 with a reason, not by borrowing another gate's constant.
GOVERNED_ENTRY = "document_metadata"
SCHEMA_FILE = "00-governance/architecture-document-metadata.schema.yaml"
SCHEMA_VERSION = "2"
# The scope registry publishes a version; publishing one and never reading
# it is the defect this gate keeps finding. A registry written for a
# different shape must not be interpreted as if it were current.
REGISTRY_VERSION = "2"
# Build and VCS state: present in some working copies, absent in others.
# Declaring them would make the registry describe a machine, not the repo.
STRUCTURAL_EXCEPTIONS = {".git", "target", ".pytest_cache", "__pycache__"}
SCOPE_REGISTRY = "00-governance/document-scope-registry.yaml"

# The controls a machine cannot perform. **This tuple is the authority**: policy
# section 9.2 is generated from it and T69 fails when the table and the
# derivation differ, so the table is a rendering, not a second opinion.
#
# The distinction matters. An earlier version kept the list here and a hand-kept
# table in the policy, then checked that the two agreed -- which is two
# authorities and a synchronisation test. Two representations derived from one
# authority is fine; two independently maintained authorities is the defect.
#
# Fields: id, control, why a machine cannot do it, who is accountable.
MANUAL_CONTROLS = (
    ("M-01", "Whether two `Canonical` scopes genuinely overlap",
     "Overlap is a claim about meaning. The gate proves the ids are unique and only one document per group is `Canonical`; whether two *different* ids cover the same subject is not derivable from metadata",
     "Reviewer"),
    ("M-02", "Whether an `Approved` decision is real",
     "The gate proves a decision record exists, names an approver and binds to a commit. It cannot prove a person with that authority actually decided",
     "Approver, then reviewer"),
    ("M-03", "Whether `evidence_verification` evidence supports the decision",
     "The gate proves a verification status and a reference exist. Whether the reference supports the claim is an argument, not a field",
     "Reviewer"),
    ("M-04", "Whether the `Selected-sections` chosen are substantively sufficient",
     "The gate proves the declared sections exist, that the identifiers resolve and that the scope is non-empty. Whether that selection is *adequate* for the document is a judgement",
     "Approver"),
    ("M-05", "Semantic parity of a bilingual mirror",
     "GOV-DOC-001 requires that the two versions say the same thing. The gate proves both exist, point at each other, and agree on metadata — not that the prose agrees",
     "Reviewer"),
    ("M-06", "Whether an exclusion reason is honest",
     "DM-14 proves a reason exists and is bilingual. `kind: not-documentation` is an assertion by the author; no file content can refute it",
     "Reviewer"),
    ("M-07", "Whether a declared backlog is acceptable to ship",
     "The count is checked against the disk, which proves the number is true, not that the remainder is tolerable",
     "Governance authority"),
    ("M-08", "Whether external consumers obey `resolve_canonical()`",
     "The gate can see this repository. Readers outside it (agents, tools, downstream systems) are not observable here, so their discipline is a contract, not a check",
     "Consumer owners"),
    ("M-09", "Whether the normalisation equivalence is appropriate for a document's semantics",
     "§9.1 fixes three equivalences (CRLF/CR → LF, trailing whitespace, blank-line edges) and the gate applies them exactly. Whether that equivalence is right for one document's meaning is not a property of the bytes",
     "Reviewer"),
    ("M-10", "Whether the `_unclassified` citation ban is respected",
     "The ban is on how a document is *used*. Nothing in the repository records who cited what",
     "Reader / agent operators"),
)

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
BILINGUAL_KEYS = {"source", "en", "zh-CN"}

# The four dimensions. A schema missing any of them cannot describe a
# classification, so schema() refuses to load rather than checking nothing.
DIMENSIONS = {"domain", "role", "lifecycle", "authority"}

SCOPE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*/[a-z0-9]+(-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
SEQ_MAPPING_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:(\s|$)")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

# Always required, checked leaf by leaf. A dimension that exists but declares
# no state is not a classification.
# Required leaves are NOT restated here. They live in the schema's `required:
# true` and are enforced by check_kinds(). A second hand-maintained list is how
# `approval_scope: required true` stayed unenforceable: the list omitted it, the
# schema declared it, and nothing compared the two.
def _required_in(spec: dict) -> tuple[str, ...]:
    out: list[str] = []
    def walk(node: dict, prefix: str) -> None:
        for name, sub in (node.get("fields") or {}).items():
            if not isinstance(sub, dict):
                continue
            path = f"{prefix}{name}"
            if sub.get("required") is True:
                out.append(path)
            if isinstance(sub.get("fields"), dict):
                walk(sub, path + ".")
    walk(spec, "")
    return tuple(out)

def required_fields(root: Path | None = None) -> tuple[str, ...]:
    """Every leaf path the schema marks required, in document order."""
    return _required_in(schema(root))

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
        inner = text[1:-1]
        i = 0
        while i < len(inner):
            if inner[i] == "'":
                if i + 1 < len(inner) and inner[i + 1] == "'":
                    i += 2
                    continue
                raise ParseError(
                    f"line {lineno}: unescaped ' inside single-quoted scalar; "
                    f"write '' for a literal quote: {text!r}"
                )
            i += 1
        return inner.replace("''", "'")
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
        if rest and not rest.startswith(" "):
            raise ParseError(
                f"line {lineno}: mapping ':' must be followed by a space: {text!r}"
            )
        key, rest = key.strip(), rest.strip()
        if key[:1] in ('"', "'"):
            # A quoted key, so a real name the bare form cannot spell -- a
            # top-level directory like `.github` -- is still expressible. The
            # registry has to name what is on disk; renaming the directory to
            # fit the parser would be the tail wagging the dog.
            key = _scalar(key, lineno)
            if not isinstance(key, str) or not key:
                raise ParseError(f"line {lineno}: quoted key is not a string")
        elif not KEY_RE.match(key):
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
        if not body.startswith(("'", '"')) and SEQ_MAPPING_RE.match(body):
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


def parse_yaml_subset(text: str) -> dict:
    """Parse a whole file as a mapping in the declared YAML subset.

    Used by the schema file, which is a contract rather than a governed
    document: same tokeniser, same parser, same rejection rules as the
    frontmatter path, so the schema cannot be written in syntax the gate
    itself would refuse.
    """
    tokens = _tokens(_lf(text).split("\n"), offset=1)
    if not tokens:
        raise ParseError("empty mapping")
    if tokens[0][1] != 0:
        raise ParseError(f"line {tokens[0][0]}: top-level key must not be indented")
    value, pos = _parse_block(tokens, 0, 0)
    if pos != len(tokens):
        raise ParseError(f"line {tokens[pos][0]}: unparsed input remains")
    if not isinstance(value, dict):
        raise ParseError("top level must be a mapping")
    return value

def read_metadata(text: str) -> dict | None:
    """Return the parsed document_metadata mapping, or None when absent.

    Raises ParseError for anything that is not in the declared subset.
    """
    lines = _lf(text).split("\n")
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
        return [f"DM-01 {where} must be a mapping, got {type(node).__name__}"]
    return [
        f"DM-02 {where}.{key}: unknown key (allowed: {', '.join(sorted(allowed))})"
        for key in node
        if key not in allowed
    ]


def walk_paths(node, segments: list[str], path: str = ""):
    """Yield the dotted path of every occurrence of a full key path.

    `walk_keys()` matches one segment anywhere in the tree, which is right for
    "this key must not appear at all" and wrong for "this *path* must not
    appear". DM-08 states paths, so it needs this.
    """
    if not segments:
        return
    head, rest = segments[0], segments[1:]
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key == head:
                if not rest:
                    yield here
                else:
                    yield from walk_paths(value, rest, here)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_paths(value, segments, f"{path}[{index}]")


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


def rel_path(value, where: str, errors: list[str]) -> str | None:
    """Normalise a repository-relative path, or reject it.

    `str(value).lstrip("./")` is not "strip a leading ./": lstrip takes a
    character set, so "../../00-governance/a.md" collapses to
    "00-governance/a.md" and an illegal reference becomes a legal-looking one.
    Anything that leaves the repository, is absolute, or carries a traversal
    segment is a DM-01 error rather than a silently rewritten string.
    """
    if not isinstance(value, str):
        errors.append(
            f"DM-01 {where} must be a string path, got {type(value).__name__}"
        )
        return None
    raw = value
    if "\x00" in raw:
        errors.append(f"DM-01 {where} contains a NUL byte")
        return None
    if "\\" in raw:
        errors.append(f"DM-01 {where} uses a backslash separator: {raw!r}")
        return None
    if raw.startswith("/") or (len(raw) > 1 and raw[1] == ":"):
        errors.append(f"DM-01 {where} must be repository-relative, got absolute {raw!r}")
        return None
    cleaned = raw.removeprefix("./") if raw.startswith("./") else raw
    if cleaned != raw and cleaned.startswith("./"):
        # "././x" and "./././x" are not paths this repository writes.
        errors.append(f"DM-01 {where} has a repeated ./ prefix: {raw!r}")
        return None
    parts = cleaned.split("/")
    if any(part in ("", ".", "..") for part in parts):
        errors.append(f"DM-01 {where} is not a normalised relative path: {raw!r}")
        return None
    return cleaned

def _lf(text: str) -> str:
    """CRLF and CR become LF; nothing else is a line break.

    `str.splitlines()` also breaks on U+2028, U+2029, U+000B, U+000C, U+001C..
    U+001E and U+0085. Using it for the body hash would mean
    "alpha\u2028beta" and "alpha\nbeta" hash identically — two different
    documents carrying one approval. The policy authorises exactly one
    equivalence (CRLF/CR -> LF), so exactly one is applied.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")

def body_text(text: str) -> str:
    """Document body without its own frontmatter.

    An approval binds to document content, not to the governance metadata.
    """
    lines = _lf(text).split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return "\n".join(lines[i + 1:])
    return text


def body_hash(text: str) -> str:
    """Hash of the document body under the declared equivalence.

    Declared, not incidental: line endings are normalised to LF because
    checkouts differ (core.autocrlf) and would otherwise break every approval;
    trailing spaces/tabs per line are ignored; leading and trailing blank lines
    are ignored. Everything else is compared byte-for-byte, including leading
    spaces on a non-blank line.
    """
    unified = _lf(body_text(text))
    lines = [line.rstrip(" \t") for line in unified.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def _enum(errors, value, allowed, label, rule="DM-02"):
    if value is None:
        return
    if not isinstance(value, str):
        # A list or mapping here would raise TypeError on set membership.
        errors.append(
            f"DM-01 {label} must be a scalar, got {type(value).__name__}"
        )
        return
    if value not in allowed:
        errors.append(f"{rule} {label} not in enumeration: {value!r}")


KINDS = {
    "string", "nullable-string", "mapping", "nullable-mapping",
    "sequence", "boolean",
}

def _kind_ok(value, kind: str) -> bool:
    if kind == "string":
        # bool is not a string here: YAML `true` parses to bool, and accepting
        # it as a string is how `evidence_reference: [true]` slipped through.
        return isinstance(value, str)
    if kind == "nullable-string":
        return value is None or isinstance(value, str)
    if kind == "mapping":
        return isinstance(value, dict)
    if kind == "nullable-mapping":
        return value is None or isinstance(value, dict)
    if kind == "sequence":
        return isinstance(value, list)
    if kind == "boolean":
        return isinstance(value, bool)
    raise AssertionError(f"unreachable kind {kind!r}")

_SCHEMA: dict[str, dict] = {}

def schema(root: Path | None = None) -> dict:
    """The published metadata contract, parsed by this gate's own reader.

    Loaded from `root`, not from the script's own directory: the contract
    belongs to the repository being checked. Reading it from the script's
    location meant `--root elsewhere` silently validated against this
    repository's schema, so a repository could not ship its own contract and a
    test could not substitute a broken one.

    Fail-closed at three levels, because each one alone is a silent no-op:
      * a missing or unparseable file stops the run;
      * a `fields` node that is not a mapping stops the run;
      * a `fields` node that has lost the four dimensions, or marks fewer than
        five leaves required, stops the run.

    The third check exists because `fields: {}` parses, is a dict, and leaves
    check_kinds() with nothing to check -- every type and required rule would
    quietly pass. A schema that declares nothing must not read as "no rules".
    """
    global _SCHEMA
    base = root if root is not None else Path(__file__).resolve().parents[1]
    path = base / SCHEMA_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"cannot load {SCHEMA_FILE}: {exc}")
    # Keyed on content, not on path. A path key meant the first parse of a root
    # won for the whole process: rewrite that root's schema and every later call
    # still validated against the old contract, so a run could report PASS while
    # proving the previous schema. Content keying also makes the cache correct
    # rather than merely harmless -- the same bytes reuse one parse, changed
    # bytes always reparse.
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if key not in _SCHEMA:
        try:
            loaded = parse_yaml_subset(text)
        except ParseError as exc:
            raise SystemExit(f"cannot load {SCHEMA_FILE}: {exc}")
        if not isinstance(loaded, dict):
            raise SystemExit(f"{SCHEMA_FILE} is not a mapping")
        # The version is the only statement that gate and contract are the same
        # generation. It was published and never compared, so a schema written
        # for a different rule set loaded silently.
        declared_version = loaded.get("schema_version")
        if str(declared_version) != SCHEMA_VERSION:
            raise SystemExit(
                f"{SCHEMA_FILE} declares schema_version {declared_version!r} "
                f"but this gate implements {SCHEMA_VERSION!r}"
            )
        fields = loaded.get("fields")
        if not isinstance(fields, dict) or not fields:
            raise SystemExit(f"{SCHEMA_FILE} declares no fields mapping")
        missing = DIMENSIONS - set(fields)
        if missing:
            raise SystemExit(
                f"{SCHEMA_FILE} no longer declares {sorted(missing)}; a schema "
                f"without the four dimensions cannot describe a classification"
            )
        unread = check_schema_keys(loaded)
        if unread:
            raise SystemExit(f"{SCHEMA_FILE}: " + "; ".join(unread))
        if len(_required_in(loaded)) < 5:
            raise SystemExit(
                f"{SCHEMA_FILE} marks fewer than 5 leaves required; "
                f"a classification needs at least the four dimensions' states"
            )
        _SCHEMA[key] = loaded
    return _SCHEMA[key]

def check_schema_keys(loaded: dict) -> list[str]:
    """Validate the schema against itself: keys, types, and combinations.

    The eleventh review was right that rejecting unknown key *names* is not the
    same as enforcing the contract. `required: "false"` is a string, and
    `is True` is False for it, so the field was silently optional; `enum:
    architecture` is a string, and iterating it yields characters, so the
    enumeration check compared against letters; `items` on a non-sequence
    describes a constraint nothing applies. All of these use only known keys.

    So every key is typed here, and combinations that cannot mean anything are
    refused. This is the schema-of-schema: the contract has to satisfy its own
    kind of rigour before it can impose any.
    """
    allowed = {"kind", "required", "enum", "items", "fields"}
    problems: list[str] = []

    def walk(node, prefix: str) -> None:
        if not isinstance(node, dict):
            problems.append(f"schema node {prefix or '<root>'} is not a mapping")
            return
        for name, sub in node.items():
            here = f"{prefix}{name}"
            if not isinstance(sub, dict):
                problems.append(f"schema field {here} is not a mapping")
                continue
            unknown = set(sub) - allowed
            if unknown:
                problems.append(
                    f"schema field {here} declares key(s) the gate does not "
                    f"read: {sorted(unknown)}; remove them or implement them"
                )
                continue
            nested = sub.get("fields")
            kind = sub.get("kind")

            # A node with children is a mapping, and saying so is consistent:
            # `kind: mapping` + `fields:` states the same thing twice, which is
            # harmless. `kind: string` + `fields:` is a contradiction -- the
            # node claims to be a scalar while the walk descends into its
            # children -- and the twelfth review's counterexample passed the
            # previous version unchanged because only key names were checked.
            if nested is not None and kind is not None and kind not in (
                "mapping", "nullable-mapping",
            ):
                problems.append(
                    f"schema field {here} declares fields but kind {kind!r}; a "
                    f"node with children can only be a mapping"
                )
                continue

            if nested is not None:
                if not isinstance(nested, dict) or not nested:
                    problems.append(
                        f"schema field {here} declares an empty or non-mapping "
                        f"fields node; a structure must declare its children"
                    )
                else:
                    walk(nested, f"{here}.")

            if kind is not None and kind not in KINDS:
                problems.append(
                    f"schema field {here} declares unknown kind {kind!r}; "
                    f"legal kinds are {sorted(KINDS)}"
                )
                continue

            # `required` must be a real boolean. `required: "false"` is a string,
            # `is True` is False, and the field silently became optional -- the
            # exact class of defect this function exists to stop.
            if "required" in sub and not isinstance(sub["required"], bool):
                problems.append(
                    f"schema field {here} declares required: {sub['required']!r}, "
                    f"which is {type(sub['required']).__name__}, not a boolean"
                )

            # `enum` must be a list of scalars. A bare string iterates as
            # characters, so every value would fail -- loudly but for the wrong
            # reason -- and a mapping is not an enumeration at all.
            if "enum" in sub:
                values = sub["enum"]
                if not isinstance(values, list) or not values:
                    problems.append(
                        f"schema field {here} declares enum as "
                        f"{type(values).__name__}; it must be a non-empty sequence"
                    )
                elif any(isinstance(v, (dict, list)) for v in values):
                    problems.append(
                        f"schema field {here} declares a non-scalar enum value"
                    )
                if kind not in ("string", "nullable-string", "sequence"):
                    problems.append(
                        f"schema field {here} declares enum on kind {kind!r}, "
                        f"which cannot hold an enumerated value"
                    )

            # `items` only means something for a sequence.
            if "items" in sub:
                if kind != "sequence":
                    problems.append(
                        f"schema field {here} declares items on kind {kind!r}; "
                        f"only a sequence has items"
                    )
                elif not isinstance(sub["items"], str):
                    problems.append(
                        f"schema field {here} declares items as "
                        f"{type(sub['items']).__name__}, not a kind name"
                    )
                elif sub["items"] not in KINDS:
                    problems.append(
                        f"schema field {here} declares items: {sub['items']!r}, "
                        f"which is not a kind"
                    )

            # A leaf must say what it is. A node with `fields` is structural and
            # needs no kind; a node without one must have a kind, or the gate
            # has nothing to type-check it against.
            if nested is None and kind is None:
                problems.append(
                    f"schema field {here} declares no kind and no fields; the "
                    f"gate cannot type-check it"
                )

    walk(loaded.get("fields"), "")
    return problems

def check_kinds(node, spec: dict, errors: list[str], where: str = "") -> None:
    """Enforce the schema's declared kind for every present field.

    Without this, the schema is a description of the gate rather than a
    constraint on it: two files can agree with each other while the gate
    accepts a type the schema forbids (a null where `mapping` is declared, a
    bool inside a `sequence` of strings). Presence is DM-01's job and enum
    membership is DM-02's; this function only checks types.
    """
    if not isinstance(node, dict):
        return
    for name, sub in (spec.get("fields") or {}).items():
        if not isinstance(sub, dict):
            errors.append(f"DM-01 schema field {where}{name} is not a mapping")
            continue
        kind = sub.get("kind")
        if kind not in KINDS:
            errors.append(f"DM-01 schema field {where}{name} declares unknown kind {kind!r}")
            continue
        if name not in node:
            # `required` is a constraint, not a comment. Skipping absent fields
            # made `approval_scope: required true` unenforceable while
            # REQUIRED_FIELDS never listed it -- the schema and the gate
            # disagreed and neither noticed.
            if sub.get("required") is True:
                errors.append(f"DM-01 missing required field: {where}{name}")
            continue
        path = f"{where}{name}"
        value = node[name]
        if not _kind_ok(value, kind):
            errors.append(
                f"DM-01 {path} must be {kind}, got {type(value).__name__}"
            )
            continue
        if isinstance(value, dict):
            check_kinds(value, sub, errors, path + ".")
        elif isinstance(value, list):
            item_kind = sub.get("items")
            if item_kind is not None:
                if item_kind not in KINDS:
                    errors.append(
                        f"DM-01 schema field {path} declares unknown items kind {item_kind!r}"
                    )
                    continue
                for index, item in enumerate(value):
                    if not _kind_ok(item, item_kind):
                        errors.append(
                            f"DM-01 {path}[{index}] must be {item_kind}, "
                            f"got {type(item).__name__}"
                        )

def as_map(node, where: str, errors: list[str]) -> dict:
    """Return node as a mapping, or record a DM-01 type error and return {}.

    Every nested read goes through here so a wrong node type is a diagnosable
    gate error rather than an AttributeError traceback.
    """
    if node is None:
        return {}
    if not isinstance(node, dict):
        errors.append(
            f"DM-01 {where} must be a mapping, got {type(node).__name__}"
        )
        return {}
    return node


def check_document(path: Path, text: str, root: Path | None = None) -> tuple[list[str], dict | None]:
    """Return (errors, metadata). Empty errors means the file conforms.

    `root` selects which repository's schema applies. Callers that pass a
    document from a temp repo must pass that repo's root, otherwise the
    contract checked is this repository's, not the one under test.
    """
    try:
        meta = read_metadata(text)
    except ParseError as exc:
        return [f"DM-01 frontmatter unparseable: {exc}"], None

    if meta is None:
        # Not yet classified. The caller decides whether that is an error
        # (changed file or --strict) or an adoption gap (policy 8).
        return [], None

    errors: list[str] = []

    # DM-01 structure. Presence is checked leaf by leaf: `lifecycle: {approval:
    # {}}` would otherwise satisfy "the dimension exists" while declaring no
    # lifecycle state at all.
    errors += unknown_keys(meta, TOP_KEYS, GOVERNED_ENTRY)
    # Type and presence contract, both from the schema. A null where the schema
    # declares `mapping` is a type error, not merely a missing leaf that DM-03
    # happens to tolerate; an absent field the schema marks required is equally
    # an error, not an optional omission.
    check_kinds(meta, schema(root), errors)
    lifecycle = as_map(meta.get("lifecycle"), "lifecycle", errors)
    authority = as_map(meta.get("authority"), "authority", errors)
    errors += unknown_keys(lifecycle, LIFECYCLE_KEYS, "lifecycle")
    errors += unknown_keys(authority, AUTHORITY_KEYS, "authority")
    if "bilingual_counterpart" in meta and meta["bilingual_counterpart"] is not None:
        counterpart_node = as_map(
            meta["bilingual_counterpart"], "bilingual_counterpart", errors
        )
        errors += unknown_keys(counterpart_node, BILINGUAL_KEYS, "bilingual_counterpart")

    # DM-02 closed enumerations.
    domain, role = meta.get("domain"), meta.get("role")
    _enum(errors, domain, DOMAINS, "domain")
    _enum(errors, role, ROLES, "role")
    approval = as_map(lifecycle.get("approval"), "lifecycle.approval", errors)
    errors += unknown_keys(approval, APPROVAL_KEYS, "lifecycle.approval")
    decision = approval.get("decision_status")
    _enum(errors, decision, DECISION_STATUSES, "decision_status")
    usage = lifecycle.get("usage_status")
    _enum(errors, usage, USAGE_STATUSES, "usage_status")
    modification = lifecycle.get("modification_status")
    _enum(errors, modification, MODIFICATION_STATUSES, "modification_status")
    applicability = approval.get("approval_applicability")
    _enum(errors, applicability, APPLICABILITY, "approval_applicability")
    verification_block = as_map(
        lifecycle.get("evidence_verification"), "lifecycle.evidence_verification", errors
    )
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
    supersession_block = as_map(
        lifecycle.get("supersession"), "lifecycle.supersession", errors
    )
    errors += unknown_keys(supersession_block, SUPERSESSION_KEYS, "lifecycle.supersession")

    # DM-03 Approved must bind a version and a scope.
    version = as_map(approval.get("approved_version"), "approved_version", errors)
    scope = as_map(approval.get("approval_scope"), "approval_scope", errors)
    errors += unknown_keys(version, VERSION_KEYS, "approved_version")
    _enum(errors, version.get("scheme"), VERSION_SCHEMES, "approved_version.scheme")
    errors += unknown_keys(scope, SCOPE_KEYS, "approval_scope")
    _enum(errors, scope.get("type"), SCOPE_TYPES, "approval_scope.type")
    if decision == "Approved":
        if not version.get("value"):
            errors.append("DM-03 Approved requires approval.approved_version.value")
        if not scope.get("type"):
            errors.append("DM-03 Approved requires approval.approval_scope.type")
        if not applicability:
            errors.append("DM-03 Approved requires approval.approval_applicability")
    if scope.get("type") == "Selected-sections":
        sections = scope.get("included_sections")
        if not sections or not isinstance(sections, list):
            errors.append(
                "DM-03 Selected-sections requires a non-empty included_sections list"
            )
    if scope.get("type") == "Selected-assets":
        # Symmetric with Selected-sections. The scope type existed in the
        # enumeration and required nothing: declaring it and listing no asset
        # was accepted, which made the type a label rather than a scope.
        assets = scope.get("included_assets")
        if not assets or not isinstance(assets, list):
            errors.append(
                "DM-03 Selected-assets requires a non-empty included_assets list"
            )

    # DM-04 Revoked must carry a unique revocation decision id.
    revocation = approval.get("revocation")
    if revocation is not None:
        revocation = as_map(revocation, "revocation", errors)
        errors += unknown_keys(revocation, REVOCATION_KEYS, "revocation")
    if decision == "Revoked":
        if not revocation:
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
    archival = as_map(lifecycle.get("archival"), "archival", errors)
    errors += unknown_keys(archival, ARCHIVAL_KEYS, "archival")
    if usage == "Archived":
        if not archival.get("archived_date"):
            errors.append("DM-05 Archived requires archival.archived_date")
        if not archival.get("archival_reason"):
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
    # The list comes from the schema's `forbidden:`, which the gate reads. A
    # second hard-coded key here would be a rule declared twice and enforced
    # once: the schema would name one forbidden path and DM-08 would check a
    # different one, and neither would notice.
    for forbidden_path in schema(root).get("forbidden") or []:
        if not isinstance(forbidden_path, str):
            continue
        # The whole path, not its last segment. Matching on the leaf name was a
        # real misreport: `authority.superseded_by` was flagged as
        # `lifecycle.supersession.superseded_by`, so the gate named a location
        # the author had not written. It also merged two declarations that
        # happened to share a leaf, turning a path rule into a global name rule
        # -- a different contract from the one the schema states.
        for where in walk_paths(meta, forbidden_path.split(".")):
            errors.append(
                f"DM-08 {where} is {forbidden_path}: CI-derived, MUST NOT be "
                f"hand-written"
            )

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

    # DM-09 Generated artifacts must not claim authority. Scan the whole body:
    # a marker on line 9 is still a marker.
    if GENERATED_MARKER.search(body_text(text)):
        if normative == "Normative" or canonical == "Canonical":
            errors.append(
                "DM-09 a generated artifact MUST NOT be Normative or Canonical; "
                "the Markdown source is the authority (policy 7)"
            )

    return errors, meta


# A generated artifact MUST carry this HTML comment anywhere in its body. The
# comment form is the protocol: prose that merely says "generated artifacts"
# does not mark a file, so a policy document can discuss the rule without
# tripping it. See policy 9 (DM-09).
GENERATED_MARKER = re.compile(
    r"<!--[^>]*\b(GENERATED[ -](FILE|ARTIFACT)|DO NOT EDIT)\b[^>]*-->", re.I
)


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


def git(root: Path, *args: str, nul: bool = False, raw: bool = False) -> str | None:
    """Run git, returning stdout or None when unavailable/failing.

    nul=True reads a NUL-separated path list, so filenames containing spaces
    are not split into fragments. raw=True returns stdout untouched: stripping
    a `git show` result would be a second, undeclared normalisation applied
    before the body hash ever sees the text.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    if out.returncode != 0:
        return None
    return out.stdout if (nul or raw) else out.stdout.strip()


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
        # Pin to an immutable commit id. A branch or tag name can move, which
        # would silently re-point the approval at different content.
        if not COMMIT_RE.match(str(value).strip()):
            errors.append(
                f"DM-10 approved_version {value!r} must be a full 40-hex commit id, "
                "not a branch, tag or abbreviated reference"
            )
            return errors, notes
        commit = git(root, "rev-parse", "--verify", "--quiet", f"{value}^{{commit}}")
        if not commit:
            errors.append(
                f"DM-10 approved_version {value!r} is not a commit in this repository"
            )
            return errors, notes
        historical = git(root, "show", f"{commit}:{rel}", raw=True)
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
            if selected:
                selected = rel_path(
                    selected, f"scope {scope_id!r} resolution selected_document", errors
                )
                if selected is None:
                    pass
                elif selected not in owners:
                    errors.append(
                        f"DM-11 scope {scope_id!r} resolution selects {selected!r}, "
                        "which does not declare this scope"
                    )
                elif canonical != [selected]:
                    errors.append(
                        f"DM-11 scope {scope_id!r} resolution selects {selected!r}, "
                        f"which is not the unique Canonical document "
                        f"({canonical or 'none holds Canonical'})"
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

    # DM-12 bilingual counterpart: exists, classified, same group, no missing
    # link.
    #
    # Model: a source document names its mirrors under en / zh-CN. A mirror
    # names the source under `source`, and may name its sibling mirror. Every
    # document in one group therefore resolves to the same source, and the
    # source lists every mirror that names it. That last check is what a plain
    # pairwise symmetry test cannot catch: with A<->en only, a third mirror
    # could be absent from both and nobody would notice.
    lang_prefix = {"en": "docs/en/", "zh-CN": "docs/zh-CN/"}

    def source_of(meta: dict, rel: str) -> str | None:
        node = meta.get("bilingual_counterpart")
        if not isinstance(node, dict) or not node.get("source"):
            return None
        return rel_path(node["source"], f"{rel}: bilingual_counterpart.source", errors)

    for rel, meta in docs.items():
        counterpart = meta.get("bilingual_counterpart")
        if not isinstance(counterpart, dict):
            continue
        own_source = source_of(meta, rel)
        if own_source and own_source.startswith(("docs/en/", "docs/zh-CN/")):
            errors.append(
                f"DM-12 {rel}: source must be the authoritative file, not a mirror "
                f"({own_source})"
            )
        for lang, target in counterpart.items():
            if not target:
                continue
            target_rel = rel_path(
                target, f"{rel}: bilingual_counterpart.{lang}", errors
            )
            if target_rel is None:
                continue
            if target_rel == rel:
                errors.append(f"DM-12 {rel}: bilingual_counterpart.{lang} points to itself")
                continue
            if not (root / target_rel).is_file():
                errors.append(
                    f"DM-12 {rel}: bilingual_counterpart.{lang} does not exist: "
                    f"{target_rel}"
                )
                continue
            expected = lang_prefix.get(lang)
            if expected and not target_rel.startswith(expected):
                errors.append(
                    f"DM-12 {rel}: bilingual_counterpart.{lang} must point under "
                    f"{expected}, got {target_rel}"
                )
            other = docs.get(target_rel)
            if other is None:
                errors.append(
                    f"DM-12 {rel}: counterpart {target_rel} exists but carries no "
                    "document_metadata, so parity cannot be verified"
                )
                continue
            # Both ends must belong to the same group.
            others_source = source_of(other, target_rel)
            if own_source:
                # A mirror may point at its own source, or at a sibling mirror
                # of that same source; anything else is a stray link.
                if target_rel != own_source and others_source != own_source:
                    errors.append(
                        f"DM-12 {rel} -> {target_rel}: neither its source "
                        f"({own_source}) nor a sibling mirror of it "
                        f"({others_source!r})"
                    )
            elif others_source != rel:
                errors.append(
                    f"DM-12 {rel} <-> {target_rel}: the counterpart does not name "
                    f"{rel} as its source"
                )
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

    # Every mirror must appear in its source's list: no silent third party.
    # default=set() matters: a source with no bilingual_counterpart block has
    # no entry here, and `.get()` returning None used to skip the check
    # entirely. "The source never declared anything" is the strongest form of
    # "the source does not list this mirror", not a reason to stay silent.
    listed_by_source: dict[str, set[str]] = defaultdict(set)
    for rel, meta in docs.items():
        node = meta.get("bilingual_counterpart")
        if not isinstance(node, dict):
            continue
        for lang, value in node.items():
            if value and lang in lang_prefix:
                target_rel = rel_path(value, f"{rel}: bilingual_counterpart.{lang}", errors)
                if target_rel is not None:
                    listed_by_source[rel].add(target_rel)

    for rel, meta in docs.items():
        # A mirror that declares nothing is invisible to the closure check
        # above: no source ever lists it, and nothing asks why. Being under a
        # language mirror root is the declaration.
        in_mirror_root = rel.startswith(("docs/en/", "docs/zh-CN/"))
        if in_mirror_root and not source_of(meta, rel):
            errors.append(
                f"DM-12 {rel}: lives under a language mirror root but declares no "
                "bilingual_counterpart.source, so it belongs to no group"
            )
        source_rel = source_of(meta, rel)
        if not source_rel:
            continue
        if source_rel not in docs:
            errors.append(
                f"DM-12 {rel}: names {source_rel} as its source, but that file is "
                "not a classified governed document"
            )
            continue
        if rel not in listed_by_source[source_rel]:
            errors.append(
                f"DM-12 {rel}: names {source_rel} as its source, but {source_rel} "
                "does not list this mirror"
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
            target_rel = rel_path(
                target, f"DM-13 {rel}: supersedes", errors
            )
            if target_rel is None:
                continue
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

def inside_repo(root: Path, rel: str) -> bool:
    """True when rel resolves to a regular file that is physically in root.

    `Path.is_symlink()` only inspects the final component: a file at
    `docs/governance/x.md` whose *parent* is a link to /outside still reads
    /outside/x.md, and nothing about `x.md` says so. Proving containment means
    resolving the whole path and comparing it to the resolved root, which also
    catches `..` and link chains in any component.
    """
    try:
        real = (root / rel).resolve(strict=True)
        real_root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    if real_root not in real.parents:
        return False
    return real.is_file()


_REGISTRY: dict[str, dict] = {}

def registry(root: Path) -> dict:
    """The scope registry, parsed once per content. Fail-closed on absence.

    Governed roots come from NORMATIVE_ROOTS; *backlog* roots come from here.
    A backlog directory is scanned and counted as unclassified, so "27 documents
    are not yet migrated" is a number the gate produces rather than a claim the
    registry makes. It is keyed on content for the same reason schema() is.
    """
    path = root / SCOPE_REGISTRY
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"cannot read scope registry {SCOPE_REGISTRY}: {exc}")
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if key not in _REGISTRY:
        try:
            loaded = parse_yaml_subset(text)
        except ParseError as exc:
            raise SystemExit(f"cannot read scope registry {SCOPE_REGISTRY}: {exc}")
        if not isinstance(loaded, dict):
            raise SystemExit(f"{SCOPE_REGISTRY} is not a mapping")
        _REGISTRY[key] = loaded
    return _REGISTRY[key]

def backlog_roots(root: Path) -> tuple[str, ...]:
    """Directories declared as backlog: scanned, counted, expected to shrink.

    A malformed registry yields no backlog roots instead of stopping the run.
    `governed_files()` is called before `check_scope_registry()` and has no
    error channel; raising here would replace DM-14's diagnostic with a
    traceback-free exit that names no rule. The registry check runs next and
    reports the parse failure properly, so nothing is silently tolerated.
    """
    try:
        node = registry(root).get("backlog")
    except SystemExit:
        return ()
    if not isinstance(node, dict):
        return ()
    return tuple(sorted(str(name).strip("/") for name in node))

# A number immediately followed by a document noun is a claim about how many
# documents there are. Only `documents:` is allowed to make that claim: prose
# that repeats the number is a second copy of a fact, and a second copy is a
# copy that can disagree. The twelfth review found `documents: 27` beside
# "26 architecture documents" in the English reason -- a number stated twice
# and true once. Checking that two statements agree is weaker than not having
# two statements, so the registry prose is now forbidden from stating a count.
#
# Coverage: digits, optional `architecture`, then a document noun -- English
# `documents`, `docs`, `files`, `Markdown`, Chinese `份`, `个`, `篇`, `文档`,
# `文件`. Spelled-out numbers are also caught (`twenty-seven documents`), because
# a spelled-out count is still a second statement of the count: the fact that a
# regex cannot parse English is not a licence to restate the number in prose.
# Numbers written as words are matched by a small explicit list of English and
# Chinese numerals.
#
# Still not caught: a noun outside the list (`27 artefacts`), and a number
# separated from its noun by something other than whitespace. Neither is
# declared acceptable -- they are simply not detected, and the guarantee that
# matters is elsewhere: the count is *checked against the disk*. This rule only
# reduces the number of places a wrong count can be written, and no test asserts
# that a gap stays a gap, because a test that protects a shortfall also blocks
# fixing it.
_WORDS = (
    r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen"
    r"|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty"
    r"|forty|fifty|sixty|seventy|eighty|ninety|hundred"
)
# `\b` is a word boundary between a word character and a non-word character.
# CJK characters are not word characters to `re`, so `\b二十七` never matches
# inside Chinese prose -- the Chinese numerals need their own branch with no
# boundary assertion at all.
COUNT_CLAIM_RE = re.compile(
    r"(?:\d+"
    r"|(?:\b(?:" + _WORDS + r")(?:[-\s](?:" + _WORDS + r"))*\b)"
    r"|(?:[一二两三四五六七八九十百]+)"
    r")\s*(?:architecture\s+)?(?:documents?|docs?|files?|Markdown"
    r"|份|个|篇|文档|文件)",
    re.I,
)


def _count(value) -> int | None:
    """A non-negative integer declared as a YAML scalar.

    The subset reader has no numeric type: `documents: 27` arrives as "27".
    Accepting a digit string keeps the reader honest about what it can prove --
    it does not pretend to parse numbers -- while still rejecting `documents:
    many` or `documents: -1` as the registry errors they are.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def governed_prefixes() -> tuple[str, ...]:
    """Paths that are governed regardless of which root they sit under.

    docs/ is backlog, but docs/en, docs/zh-CN and the gap record inside it are
    governed. The same list has to be used by the counter and the scanner, or
    they disagree about what they are counting -- which is exactly the defect
    the tenth review found.
    """
    return tuple(NORMATIVE_ROOTS) + GOVERNED_FILES

def scan_root(root: Path, name: str, skip: tuple[str, ...] = ()) -> tuple[list[Path], list[str]]:
    """Walk one root, returning (markdown files, problems).

    There is deliberately one walk, not two. `backlog_counts()` and
    `governed_files()` used to traverse the tree separately with different skip
    rules, and the tenth review showed what that costs: a symlinked `docs/` was
    skipped by the counter (so the declared count was compared to nothing) and
    skipped by the scanner (so the run reported `0 governed documents` and exit
    0). Two traversals can disagree; one cannot.

    `skip` holds prefixes this root must not descend into, because they are
    governed by another root.

    A symlink is *reported*, never silently dropped. Dropping it is what made
    the failure silent: a link is either a mistake or content the gate cannot
    verify, and both deserve a diagnostic rather than a shorter file list.
    """
    files: list[Path] = []
    problems: list[str] = []
    base = root / name
    if base.is_symlink():
        problems.append(
            f"DM-14 {name} is a symbolic link; a governed or backlog root must be "
            f"a real directory inside the repository, not a pointer to one"
        )
        return files, problems
    if not base.is_dir():
        return files, problems

    # `os.walk` swallows errors by default: an unreadable directory is skipped
    # and the walk continues, so a permission problem would shrink the scanned
    # set with no diagnostic -- the same silent-shortening failure the tenth
    # review found in the two-walk version, arriving by a different route.
    def on_error(exc: OSError) -> None:
        where = getattr(exc, "filename", None) or name
        problems.append(f"DM-14 cannot read {where}: {exc.strerror or exc}")

    for dirpath, dirnames, filenames in os.walk(
        base, followlinks=False, onerror=on_error,
    ):
        here = Path(dirpath)
        rel_dir = here.relative_to(root).as_posix()
        # Prune symlinked directories and governed subtrees before descending,
        # so a link cannot pull files from outside into the count.
        kept = []
        for d in sorted(dirnames):
            child = here / d
            rel_child = (rel_dir + "/" + d) if rel_dir != "." else d
            if child.is_symlink():
                problems.append(
                    f"DM-14 {rel_child} is a symbolic link; the gate does not "
                    f"follow links, and a linked directory would make the scanned "
                    f"set depend on a target outside the repository"
                )
                continue
            if any(rel_child == s or rel_child.startswith(s + "/") for s in skip):
                continue
            kept.append(d)
        dirnames[:] = kept
        for f in sorted(filenames):
            if not f.endswith(".md"):
                continue
            path = here / f
            rel = path.relative_to(root).as_posix()
            if any(rel == s or rel.startswith(s + "/") for s in skip):
                continue
            if path.is_symlink():
                problems.append(
                    f"DM-14 {rel} is a symbolic link; a governed document must be "
                    f"a regular file inside the repository"
                )
                continue
            files.append(path)
    return files, problems

def backlog_counts(root: Path) -> tuple[dict[str, int], list[str]]:
    """Actual Markdown count per backlog root, and anything the walk refused.

    Returns problems as well as counts: a root that could not be walked has no
    trustworthy count, and reporting zero for it would be a lie the registry
    comparison would then accept.
    """
    skip = governed_prefixes()
    counts: dict[str, int] = {}
    problems: list[str] = []
    for name in backlog_roots(root):
        found, issues = scan_root(root, name, skip)
        problems += issues
        if not issues:
            counts[name] = len(found)
    return counts, problems

def collect_governed(root: Path) -> tuple[list[Path], list[str]]:
    """The governed set, built once, with every problem the walk found.

    Three sources feed this set -- normative roots, backlog roots, and
    individually governed files -- and the eleventh review was right that
    concatenating them at the call site was not a unified scan. Two defects
    followed from that shape and both are fixed here:

      * the problems from `scan_root()` were discarded (`found, _ = ...`), so a
        symlinked subdirectory inside a *normative* root produced no diagnostic
        at all -- only backlog problems reached DM-14 (R11-05);
      * nothing enforced uniqueness, so a path reachable both as a governed
        file and through a root could be classified twice, inflating the counts
        that DM-14's accounting identity is supposed to make trustworthy
        (R11-01).

    The set is therefore returned as a set-like list: one entry per resolved
    path, and the problems travel with it instead of being dropped.
    """
    problems: list[str] = []
    backlog = set(backlog_roots(root))
    skip = governed_prefixes()
    seen: dict[str, Path] = {}

    def add(path: Path) -> None:
        # Keyed on the resolved path: two spellings of one file are one file.
        # A symlink never reaches here -- scan_root() reports it instead -- so
        # this cannot silently collapse a link into its target.
        try:
            key = path.resolve(strict=True).as_posix()
        except (OSError, RuntimeError) as exc:
            # Falling back to the unresolved spelling would let one file enter
            # the set twice under two names -- the duplication this function
            # exists to prevent. An unresolvable path is a problem, not a key.
            problems.append(f"DM-01 cannot resolve {path}: {exc}")
            return
        seen.setdefault(key, path)

    for name in NORMATIVE_ROOTS + tuple(sorted(backlog)):
        # A backlog root must not re-scan a governed subtree inside it.
        found, issues = scan_root(root, name, skip if name in backlog else ())
        problems += issues
        for path in found:
            add(path)

    # Individually governed files. They are checked with inside_repo() -- the
    # same containment proof the registry uses -- and then enter the same set,
    # so the declared set and the scanned set cannot diverge.
    for rel in GOVERNED_FILES:
        if inside_repo(root, rel):
            add(root / rel)
        else:
            problems.append(
                f"DM-14 governed file {rel} is not a regular file inside the "
                f"repository (missing, a symlink, or reached through one)"
            )

    return list(seen.values()), problems

def governed_files(root: Path) -> list[Path]:
    """The governed set alone. **Diagnostics only -- never a verdict.**

    This function discards the walk's problems, so a caller that decides
    pass/fail from it is deciding on a possibly-truncated list. That is not a
    style preference: the tenth review's blocker was exactly this shape, a scan
    that reported `0 governed documents` and exit 0.

    `main()` therefore uses `collect_governed()`, and T67 asserts that
    `governed_files()` has no other production caller -- a grep over the
    scripts, not a comment promising good behaviour.
    """
    files, _ = collect_governed(root)
    return files

def check_scope_registry(root: Path) -> list[str]:
    """Prove the scan set is the declared set, and that nothing was left out.

    The accounting identity in main() only proves no file was dropped *inside*
    the scan. It is silent about a top-level directory the scan never entered:
    add `15-new-architecture/` with a policy document in it, and
    classified + unclassified == governed still holds while the gate reports a
    clean tree. This function closes that hole by requiring every top-level
    directory to be either governed or excluded with a reason, and by requiring
    the declared governed list to equal the enforced one.

    Three independent comparisons, so no single edit can satisfy it by accident:
      registry.governed  ==  NORMATIVE_ROOTS   (declared == enforced)
      on-disk dirs       ==  governed + excluded (nothing unaccounted for)
      docs/en, docs/zh-CN  governed            (mirrors are always in scope)
    """
    errors: list[str] = []
    path = root / SCOPE_REGISTRY
    try:
        registry = parse_yaml_subset(path.read_text(encoding="utf-8"))
    except (OSError, ParseError) as exc:
        return [f"DM-14 cannot read scope registry {SCOPE_REGISTRY}: {exc}"]

    if not isinstance(registry, dict):
        return [f"DM-14 {SCOPE_REGISTRY} must be a mapping"]

    # A published version that nothing compares is decoration. If the registry
    # is written for another generation, its `backlog:`/`excluded:` semantics
    # may differ, and reading it as current would be a silent misreading.
    declared_registry_version = registry.get("registry_version")
    if str(declared_registry_version) != REGISTRY_VERSION:
        errors.append(
            f"DM-14 {SCOPE_REGISTRY} declares registry_version "
            f"{declared_registry_version!r} but this gate implements "
            f"{REGISTRY_VERSION!r}"
        )

    declared = registry.get("governed")
    if not isinstance(declared, list) or not declared:
        errors.append(f"DM-14 {SCOPE_REGISTRY} must declare a non-empty governed list")
        declared = []
    declared = [str(x).strip("/") for x in declared]

    excluded = registry.get("excluded")
    if excluded is None:
        excluded = {}
    if not isinstance(excluded, dict):
        errors.append(f"DM-14 {SCOPE_REGISTRY} excluded must be a mapping")
        excluded = {}

    backlog = registry.get("backlog")
    if backlog is None:
        backlog = {}
    if not isinstance(backlog, dict):
        errors.append(f"DM-14 {SCOPE_REGISTRY} backlog must be a mapping")
        backlog = {}

    for name, node in backlog.items():
        if not isinstance(node, dict):
            errors.append(f"DM-14 backlog {name!r} must be a mapping with a count")
            continue
        declared_count = _count(node.get("documents"))
        if declared_count is None:
            errors.append(
                f"DM-14 backlog {name!r} must declare `documents` as a "
                f"non-negative integer, got {node.get('documents')!r}"
            )
        if not str(node.get("reason") or "").strip():
            errors.append(f"DM-14 backlog {name!r} has no reason")
        if not str(node.get("reason_zh") or "").strip():
            errors.append(f"DM-14 backlog {name!r} has no reason_zh (GOV-DOC-001)")
        # The count is a machine field; the prose explains, it does not count.
        # Requiring the two to agree would still leave two numbers to keep in
        # step, so the prose is simply not allowed to state one.
        for field in ("reason", "reason_zh"):
            said = COUNT_CLAIM_RE.findall(str(node.get(field) or ""))
            if said:
                errors.append(
                    f"DM-14 backlog {name!r} {field} restates a document count "
                    f"{said}; `documents:` is the only place a count may be "
                    f"stated, so the prose cannot drift from it"
                )

    for name, node in excluded.items():
        if not isinstance(node, dict):
            errors.append(f"DM-14 excluded {name!r} must be a mapping with a reason")
            continue
        kind = node.get("kind")
        if kind not in EXCLUSION_KINDS:
            errors.append(
                f"DM-14 excluded {name!r} must declare kind one of "
                f"{sorted(EXCLUSION_KINDS)}, got {kind!r}"
            )
        if not str(node.get("reason") or "").strip():
            errors.append(f"DM-14 excluded {name!r} has no reason")
        if not str(node.get("reason_zh") or "").strip():
            errors.append(f"DM-14 excluded {name!r} has no reason_zh (GOV-DOC-001)")

    overlap = sorted((set(declared) | set(backlog)) & set(excluded))
    if overlap:
        errors.append(f"DM-14 {overlap} are both governed-or-backlog and excluded")
    both = sorted(set(declared) & set(backlog))
    if both:
        errors.append(f"DM-14 {both} are both governed and backlog; pick one")

    # (1) declared == enforced
    enforced = set(NORMATIVE_ROOTS) - {"docs/en", "docs/zh-CN"}
    if set(declared) != enforced:
        only_declared = sorted(set(declared) - enforced)
        only_enforced = sorted(enforced - set(declared))
        errors.append(
            f"DM-14 scope registry and NORMATIVE_ROOTS disagree; "
            f"declared-only {only_declared}, enforced-only {only_enforced}"
        )

    # (2) every top-level directory is accounted for
    #
    # Hidden directories are included. Excluding them meant `.new-architecture/`
    # was not on disk as far as this check was concerned: not governed, not
    # excluded, not reported, not scanned. A dot is not an exemption.
    #
    # Two structural exceptions, and they are structural rather than declared:
    # `.git` is the version-control store and `target/` is Rust build output.
    # Both exist in some working copies and not others, so a registry entry
    # would assert something about a machine instead of about the repository --
    # a fresh clone would then fail for naming a directory it does not have.
    accounted = set(declared) | set(backlog) | set(excluded) | {"docs/en", "docs/zh-CN"}
    # `Path.is_dir()` follows links, so a symlink to a directory satisfied both
    # "is a directory" and "is a symlink" and was subtracted from the unknown
    # list twice: once as accounted, once as a link. It then also satisfied the
    # `missing` check below, which asks whether every *declared* directory
    # exists -- so pointing `docs` at /tmp/elsewhere made a registry entry true
    # that was false. Enumeration is by `is_dir() and not is_symlink()`: a link
    # is never a directory, for either purpose.
    links = sorted(p.name for p in root.iterdir() if p.is_symlink())
    if links:
        errors.append(
            f"DM-14 symbolic links at the repository root are not governed roots: {links}. "
            f"A symlink makes the governed set depend on a target outside the repository"
        )
    on_disk = {
        p.name for p in root.iterdir()
        if p.is_dir() and not p.is_symlink()
    } - STRUCTURAL_EXCEPTIONS
    unknown = sorted(on_disk - accounted)
    if unknown:
        errors.append(
            f"DM-14 top-level directories not accounted for: {unknown}. "
            f"Add each to {SCOPE_REGISTRY} as governed or excluded-with-reason"
        )
    missing = sorted((set(declared) | set(backlog) | set(excluded)) - on_disk)
    if missing:
        errors.append(
            f"DM-14 {SCOPE_REGISTRY} names directories that do not exist: {missing}"
        )

    # (3) the bilingual mirrors are always governed
    for mirror in ("docs/en", "docs/zh-CN"):
        # `is_dir()` follows links, so a symlinked mirror looked present while
        # the scanner refused to descend into it: the registry would assert the
        # mirror exists and the run would classify nothing from it.
        target = root / mirror
        if target.is_symlink():
            errors.append(
                f"DM-14 bilingual mirror directory {mirror} is a symbolic link; "
                f"a mirror must be real content of this repository"
            )
        elif not target.is_dir():
            errors.append(f"DM-14 bilingual mirror directory {mirror} is missing")

    # (4) individually governed files must exist and sit in an excluded dir:
    # otherwise GOVERNED_FILES is dead weight or a hidden scope expansion.
    registry_files = registry.get("governed_files")
    if registry_files is None:
        registry_files = []
    if not isinstance(registry_files, list):
        errors.append(f"DM-14 {SCOPE_REGISTRY} governed_files must be a sequence")
        registry_files = []
    registry_files = [str(x).lstrip("/") for x in registry_files]
    if set(registry_files) != set(GOVERNED_FILES):
        errors.append(
            f"DM-14 governed_files disagrees with the gate; "
            f"registry-only {sorted(set(registry_files) - set(GOVERNED_FILES))}, "
            f"gate-only {sorted(set(GOVERNED_FILES) - set(registry_files))}"
        )

    # (5) a declared backlog count must equal the count on disk. Without this,
    # `documents: 27` is a sentence rather than a claim: the number could drift
    # as files are added or migrated and nobody would notice. With it, the
    # registry either states the truth or the gate fails.
    actual, walk_problems = backlog_counts(root)
    errors += walk_problems
    for name, node in backlog.items():
        if not isinstance(node, dict):
            continue
        declared_count = _count(node.get("documents"))
        if declared_count is None or name not in actual:
            continue
        if declared_count != actual[name]:
            errors.append(
                f"DM-14 backlog {name!r} declares {declared_count} documents "
                f"but {actual[name]} are on disk; update the registry"
            )

    for rel in GOVERNED_FILES:
        # The same containment test the scanner uses. `is_file()` follows
        # symlinks, so a symlinked entry passed the registry while the scanner
        # skipped it: the declared set and the scanned set disagreed, which is
        # exactly what this function exists to prevent. A parent-directory link
        # is caught too, because containment is proven on the resolved path.
        if not inside_repo(root, rel):
            errors.append(
                f"DM-14 governed file {rel} is not a regular file inside the "
                f"repository (missing, a symlink, or reached through one)"
            )
            continue
        top = rel.split("/")[0]
        if top in declared:
            errors.append(
                f"DM-14 governed file {rel} is already covered by root {top}; "
                f"drop the individual entry"
            )
        elif top not in excluded and top not in backlog:
            errors.append(
                f"DM-14 governed file {rel} sits in {top}, which is neither "
                f"governed, backlog nor excluded: declare the directory's status first"
            )

    return errors


def changed_paths(root: Path, ref: str) -> set[str]:
    """Repository-relative paths added, modified, renamed or type-changed.

    NUL-separated, so a filename containing spaces stays one path. Splitting on
    whitespace would let `00-governance/new policy.md` dodge the requirement.

    T (type change) is included: replacing a regular file with a symlink, or a
    symlink with a regular file, changes what the gate reads without changing
    the path. `--diff-filter=AMR` skipped exactly that, so the increment could
    report PASS while a governed path had become a link to somewhere else.
    Deletions stay excluded: a removed file has nothing to classify. Copies are
    included: with `diff.renames=copies` a new path can arrive as C, and a
    copied governed document is still a governed document.
    """
    names: set[str] = set()
    filter_arg = "--diff-filter=AMRTC"
    diff = git(root, "diff", "--name-only", "-z", filter_arg, f"{ref}...HEAD", nul=True)
    if diff is None:
        diff = git(root, "diff", "--name-only", "-z", filter_arg, ref, nul=True)
    if diff is None:
        raise SystemExit(f"cannot diff against {ref!r}; is this a git work tree?")
    names.update(p for p in diff.split("\0") if p)
    untracked = git(root, "ls-files", "-z", "--others", "--exclude-standard", nul=True) or ""
    names.update(p for p in untracked.split("\0") if p)
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--strict", action="store_true",
        help="fail if any governed document is unclassified (whole-tree verdict)",
    )
    parser.add_argument(
        "--require-changed", metavar="REF", default=None,
        help="require metadata on every governed file changed since REF "
             "(incremental: does NOT claim the whole tree is classified)",
    )
    args = parser.parse_args()

    # Two different verdicts, and they must not be confused:
    #   --require-changed REF  incremental. The backlog may stay, it may not
    #                          grow. Says nothing about the rest of the tree.
    #   --strict               whole-tree. Any unclassified governed document
    #                          is a failure.
    # Neither flag = backlog allowed, tree-wide completeness NOT claimed. The
    # PASS line says which of the three happened, so a first push (no base
    # commit, no --strict) can never read as "the repository is classified".
    #
    # There is deliberately no --only: cross-document rules (DM-07, DM-11,
    # DM-12, DM-13) are only sound over the whole tree. A partial set would let
    # one file hide another's duplicate Canonical claim and still print PASS.
    root = Path(args.root).resolve()
    # Checked before any work: with an unusable REF the diff would fail first
    # and mask the real problem (two contradictory verdicts were requested).
    incremental = args.require_changed is not None
    if incremental and args.strict:
        parser.error("--require-changed and --strict are different verdicts; pick one")
    targets, walk_problems = collect_governed(root)
    required = changed_paths(root, args.require_changed) if args.require_changed else set()
    is_git = git(root, "rev-parse", "--git-dir") is not None

    # Problems the walk itself found -- symlinks, unreadable roots -- are
    # errors of the run, not warnings. They arrive with the file list so that
    # no path can produce a shorter list without a diagnostic.
    errors: list[str] = list(walk_problems)
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
        file_errors, meta = check_document(path, text, root)
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
    errors.extend(check_scope_registry(root))

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
    # Accounting identity: every governed file is either classified or listed
    # as backlog. Printed so "403 unclassified" is a number you can check
    # against the file system, not a claim. If this ever fails to balance, the
    # classification loop dropped a file silently.
    if len(docs) + len(unclassified) != total:
        errors.append(
            f"DM-01 accounting: {len(docs)} classified + {len(unclassified)} "
            f"unclassified != {total} governed files"
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
        "  manual controls (not machine-verified, policy 9.2): "
        + "; ".join(f"{cid} {control}" for cid, control, _, _ in MANUAL_CONTROLS)
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

    if unclassified and not incremental:
        # Backlog is allowed to exist; it is not allowed to be called done.
        print(
            f"INCOMPLETE: no rule violations in {len(docs)} classified documents, "
            f"but {len(unclassified)} governed documents are still unclassified",
            file=sys.stderr,
        )
        print(
            "  This is not a whole-tree pass. Run with --strict for that verdict, "
            "or --require-changed REF for an incremental one.",
            file=sys.stderr,
        )
        return 2

    scope = "incremental" if incremental else "whole tree"
    print(
        f"PASS ({scope}): no GOV-DOC-002 violations; "
        f"{len(docs)} classified, {len(unclassified)} unclassified"
    )
    if incremental:
        print(
            "  Incremental verdict only: files outside the changed set were not "
            "required to be classified."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
