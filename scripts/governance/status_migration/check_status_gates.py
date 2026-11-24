#!/usr/bin/env python3
"""Fail-closed validator for exact work-item status and repository-backed gate evidence."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import yaml


class UniqueKeySafeLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "unhashable mapping key", key_node.start_mark) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)

PHASES = {
    "PROPOSED": "INTAKE", "ANALYZED": "INTAKE", "PROMPT_READY": "INTAKE",
    "READY": "READY", "IN_PROGRESS": "ACTIVE", "IMPLEMENTED": "ACTIVE",
    "VERIFIED": "VALIDATION", "REVIEWED": "VALIDATION",
    "INTEGRATION_READY": "VALIDATION", "ACCEPTED": "ACCEPTANCE",
    "MERGED": "COMPLETE", "CLOSED": "COMPLETE",
}
ORDER = ("verified", "independent_review", "integration",
         "owner_acceptance", "merge", "closeout")
REQUIRED = {"VERIFIED": 1, "REVIEWED": 2, "INTEGRATION_READY": 3,
            "ACCEPTED": 4, "MERGED": 5, "CLOSED": 6}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EVIDENCE_FIELDS = {
    "verified": ("commands", "environment", "tested_head", "expected_result", "actual_result", "logs"),
    "independent_review": ("reviewer", "implementer", "reviewed_head", "report", "findings_disposition"),
    "integration": ("compatibility_result", "registry_updates", "integration_report"),
    "owner_acceptance": ("authority", "decision", "decision_record"),
    "merge": ("target_branch", "merge_commit", "merge_record"),
    "closeout": ("index_update", "closeout_record"),
}
PATH_FIELDS = {
    "verified": ("logs",),
    "independent_review": ("report",),
    "integration": ("integration_report",),
    "owner_acceptance": ("decision_record",),
    "merge": ("merge_record",),
    "closeout": ("closeout_record",),
}
PLACEHOLDERS = {"", "n/a", "na", "none", "null", "todo", "tbd",
                "not_recorded", "not_verified", "fake", "test://exact-run"}


def _meaningful(value, field):
    if isinstance(value, str):
        value = value.strip()
        lowered = value.casefold()
        if (lowered in PLACEHOLDERS or len(value) < 3
                or lowered.startswith(("fake://", "test://", "placeholder://"))
                or "example.com/" in lowered or lowered.startswith("placeholder")):
            raise ValueError(f"empty/placeholder evidence content: {field}")
        if field in {"tested_head", "reviewed_head", "merge_commit"} and not SHA_RE.fullmatch(value):
            raise ValueError(f"{field} must be a full 40-character commit SHA")
        return
    if isinstance(value, list):
        if not value:
            raise ValueError(f"empty evidence list: {field}")
        for index, item in enumerate(value):
            _meaningful(item, f"{field}[{index}]")
        return
    if isinstance(value, dict):
        if not value:
            raise ValueError(f"empty evidence mapping: {field}")
        for key, item in value.items():
            _meaningful(item, f"{field}.{key}")
        return
    raise ValueError(f"invalid evidence content type: {field}")


def _repo_root(path):
    resolved = Path(path).resolve()
    for parent in (resolved.parent, *resolved.parents):
        if (parent / ".git").exists():
            return parent
    raise ValueError("manifest is not inside a Git working tree")


def _git_object_type(root, ref):
    """Return the git object type of ref, or None when unresolvable."""
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-t", ref],
        check=False, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def _git_tree_has_file(root, subject_head, relative_path):
    """Check the subject commit tree, not HEAD and not an untracked working-tree file."""
    if _git_object_type(root, subject_head) != "commit":
        raise ValueError(f"subject_head must resolve to a commit object: {subject_head}")
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only",
         subject_head, "--", relative_path],
        check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise ValueError(f"subject_head is not a resolvable commit: {subject_head}")
    return relative_path in {line.strip() for line in result.stdout.splitlines()}


def _git_blob_at(root, subject_head, relative_path):
    """Return the exact bytes stored in subject_head for relative_path."""
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{subject_head}:{relative_path}"],
        check=True, capture_output=True).stdout


MIN_EVIDENCE_BYTES = 32


def _evidence_file(value, field, root, subject_head):
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a repository-relative file path")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise ValueError(f"{field} must be a safe repository-relative path")
    relative = candidate.as_posix()
    target = (root / candidate).resolve()
    if root not in target.parents or not target.is_file():
        raise ValueError(f"{field} does not resolve to an existing repository file")
    if not _git_tree_has_file(root, subject_head, relative):
        raise ValueError(f"{field} is not present in the subject_head Git tree")
    # Trust the committed blob, not the working tree: a local edit must not
    # silently satisfy the gate.  Membership in the subject tree plus blob
    # equality is the cryptographic binding of evidence to subject_head.
    try:
        blob = _git_blob_at(root, subject_head, relative)
    except subprocess.CalledProcessError as error:
        raise ValueError(f"{field} blob is unreadable at subject_head") from error
    if blob != target.read_bytes():
        raise ValueError(f"{field} working-tree content differs from subject_head blob")
    if len(blob) < MIN_EVIDENCE_BYTES:
        raise ValueError(f"{field} evidence content is too short to be meaningful")
    try:
        content = blob.decode("utf-8")
    except UnicodeError as error:
        raise ValueError(f"{field} is not readable UTF-8 evidence") from error
    # The evidence file itself must carry real content: placeholder or
    # near-empty artifacts must not satisfy a PASS gate.
    _meaningful(content, f"{field}.content")
    return target


SIDECAR_PATH = "scripts/governance/status_migration/PR272-evidence-hardening.sha256"


def _validator_root():
    """Repo containing this validator, not the manifest under review."""
    return _repo_root(Path(__file__))


def _verify_sidecar_anchor(root, sidecar_path=SIDECAR_PATH):
    """Enforce the committed integrity anchor for the validator itself.

    The sidecar records git blob SHA-1s of protected source files.  The most
    recent commit touching the sidecar must embed sha256(committed sidecar
    bytes) in its message.  Silent local edits to a protected file or to the
    sidecar break the recorded values; updating both still forces a fresh
    commit whose message must carry a matching anchor, so any bypass leaves
    a visible, auditable commit in history rather than silent tampering.
    """
    message = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%B", "--", sidecar_path],
        check=True, capture_output=True, text=True).stdout
    match = re.search(r"\b[0-9a-f]{64}\b", message)
    if match is None:
        raise ValueError("sidecar commit message lacks a sha256 anchor")
    expected = match.group(0)

    # Verify the anchor against authoritative committed bytes.
    committed = subprocess.run(
        ["git", "-C", str(root), "cat-file", "blob", f"HEAD:{sidecar_path}"],
        check=True, capture_output=True).stdout
    actual = hashlib.sha256(committed).hexdigest()
    if actual != expected:
        raise ValueError("sidecar sha256 does not match its commit anchor")

    # Also reject local edits, comparing clean-filtered Git object IDs.
    committed_blob = subprocess.run(
        ["git", "-C", str(root), "rev-parse", f"HEAD:{sidecar_path}"],
        check=True, capture_output=True, text=True).stdout.strip()
    working_blob = subprocess.run(
        ["git", "-C", str(root), "hash-object", str(root / sidecar_path)],
        check=True, capture_output=True, text=True).stdout.strip()
    if working_blob != committed_blob:
        raise ValueError("sidecar sha256 does not match its commit anchor")

    sidecar = root / sidecar_path
    for line in sidecar.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 3 or parts[0] != "git-blob-sha1":
            raise ValueError("malformed sidecar record: " + line[:40])
        recorded, relative = parts[1], parts[2]
        blob = subprocess.run(
            ["git", "-C", str(root), "hash-object", str(root / relative)],
            check=True, capture_output=True, text=True).stdout.strip()
        if blob != recorded:
            raise ValueError("protected file does not match sidecar blob: " + relative)
    return True

def _identity_token(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("review identities must be non-empty strings")
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    normalized = re.sub(r"^(?:https?://)?(?:www\.)?github\.com/", "", normalized)
    normalized = normalized.lstrip("@")
    return re.sub(r"[^a-z0-9]", "", normalized)


def _identity(value, aliases):
    token = _identity_token(value)
    seen = set()
    while token in aliases:
        if token in seen:
            raise ValueError("review_identity_aliases contains a cycle")
        seen.add(token)
        token = _identity_token(aliases[token])
    return token


def _normalized_aliases(raw_aliases):
    if not isinstance(raw_aliases, dict):
        raise ValueError("review_identity_aliases must be a mapping")
    aliases = {}
    for alias, canonical in raw_aliases.items():
        key, value = _identity_token(alias), _identity_token(canonical)
        if not key or not value:
            raise ValueError("review identity aliases must be non-empty")
        if key in aliases and aliases[key] != value:
            raise ValueError(f"conflicting normalized identity alias: {alias}")
        aliases[key] = value
    for key in aliases:
        _identity(key, aliases)
    return aliases


def _validate_evidence(name, evidence, data, lifecycle, root, subject_head):
    if not isinstance(evidence, dict):
        raise ValueError("PASS gate evidence must be a structured mapping: " + name)
    for field in EVIDENCE_FIELDS[name]:
        if field not in evidence:
            raise ValueError(f"required evidence field missing: {name}.{field}")
        _meaningful(evidence[field], f"{name}.{field}")
    if name in {"verified", "independent_review"}:
        head_field = "tested_head" if name == "verified" else "reviewed_head"
        if evidence[head_field] != subject_head:
            raise ValueError(f"{name}.{head_field} does not match manifest subject_head")
    if name == "independent_review":
        aliases = _normalized_aliases(data.get("review_identity_aliases", {}))
        if _identity(evidence["reviewer"], aliases) == _identity(evidence["implementer"], aliases):
            raise ValueError("REVIEWED reviewer and implementer must be different identities")
    for field in PATH_FIELDS[name]:
        target = _evidence_file(evidence[field], f"{name}.{field}", root, subject_head)
        # Optional independent content digest: when the manifest records a
        # SHA-256 alongside a path field, it must match the subject blob.
        digest_field = field + "_sha256"
        if digest_field in evidence:
            recorded = evidence[digest_field]
            if not isinstance(recorded, str) or not re.fullmatch(r"[0-9a-f]{64}", recorded):
                raise ValueError(f"{name}.{digest_field} must be a 64-hex sha256 digest")
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != recorded:
                raise ValueError(f"{name}.{digest_field} does not match evidence content")


def check(path):
    # Fail closed if the validator's own source has been tampered with.
    _verify_sidecar_anchor(_validator_root())
    manifest_path = Path(path).resolve()
    root = _repo_root(manifest_path)
    data = yaml.load(manifest_path.read_bytes(), Loader=UniqueKeySafeLoader)
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")
    source = data.get("status")
    if not isinstance(source, str) or source not in PHASES:
        raise ValueError("status is not an exact canonical state")
    lifecycle = data.get("lifecycle")
    if not isinstance(lifecycle, dict):
        raise ValueError("missing/invalid lifecycle")
    if lifecycle.get("source_status") != source:
        raise ValueError("source_status mismatch; original status must remain exact")
    if lifecycle.get("phase") != PHASES[source]:
        raise ValueError("phase/status mapping mismatch")
    lifecycle_head = lifecycle.get("subject_head")
    manifest_head = data.get("subject_head")
    if lifecycle_head and manifest_head and lifecycle_head != manifest_head:
        raise ValueError("manifest and lifecycle subject_head values do not match")
    subject_head = lifecycle_head or manifest_head
    required_count = REQUIRED.get(source, 0)
    if required_count and (not isinstance(subject_head, str) or not SHA_RE.fullmatch(subject_head)):
        raise ValueError("manifest subject_head must be a full 40-character commit SHA")
    gates = lifecycle.get("gates")
    if not isinstance(gates, dict):
        raise ValueError("lifecycle.gates must be a mapping")
    unknown = set(gates) - set(ORDER)
    if unknown:
        raise ValueError("unknown gate records: " + ", ".join(sorted(unknown)))
    # Source-authenticity boundary: content-integrity PASS must never be
    # presented as proof that evidence came from a trusted producer.  Any
    # PASS gate therefore requires the manifest to declare the honest
    # capability boundary explicitly.
    has_pass = any(
        isinstance(gates.get(name), dict) and gates[name].get("status") == "PASS"
        for name in ORDER)
    authenticity = data.get("source_authenticity")
    if has_pass:
        if authenticity is None:
            raise ValueError(
                "source_authenticity is required (NOT_VERIFIED) when any gate is PASS")
        if authenticity != "NOT_VERIFIED":
            raise ValueError(
                "source_authenticity must be NOT_VERIFIED; authenticity cannot be "
                "self-certified: " + str(authenticity))
    for index, name in enumerate(ORDER):
        record = gates.get(name)
        if record is None:
            if index < required_count:
                raise ValueError("required gate record missing: " + name)
            raise ValueError(
                "future gate record missing; must be explicitly NOT_RECORDED: " + name)
        if not isinstance(record, dict):
            raise ValueError("gate record must be a mapping: " + name)
        disposition = record.get("status")
        if disposition not in {"PASS", "NOT_RECORDED", "BLOCKED", "REJECTED"}:
            raise ValueError("invalid gate disposition: " + name)
        if index < required_count:
            if disposition != "PASS":
                raise ValueError("required gate not proven PASS: " + name)
            if "evidence" not in record:
                raise ValueError("PASS gate evidence missing: " + name)
            _validate_evidence(name, record["evidence"], data, lifecycle, root, subject_head)
        elif disposition != "NOT_RECORDED":
            raise ValueError("future gate must remain NOT_RECORDED: " + name)
    markers = lifecycle.get("markers", {})
    if not isinstance(markers, dict):
        raise ValueError("lifecycle.markers must be a mapping")
    return {"result": "PASS", "path": str(path), "phase": lifecycle["phase"],
            "content_integrity": "PASS", "source_authenticity": "NOT_VERIFIED"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    failed = 0
    for name in args.paths:
        try:
            print(json.dumps(check(name), ensure_ascii=False))
        except Exception as error:
            failed += 1
            print(json.dumps({"result": "FAIL", "path": name, "error": str(error)}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
