#!/usr/bin/env python3
"""Fail-closed validator for exact work-item status and repository-backed gate evidence."""
import argparse
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


def _git_tree_has_file(root, subject_head, relative_path):
    """Check the repository HEAD tree, not an untracked/local-only working-tree file."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only",
         "HEAD", "--", relative_path],
        check=True, capture_output=True, text=True)
    return relative_path in {line.strip() for line in result.stdout.splitlines()}


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
    try:
        content = target.read_text(encoding="utf-8")
    except (UnicodeError, OSError) as error:
        raise ValueError(f"{field} is not readable UTF-8 evidence") from error
    if subject_head not in content:
        raise ValueError(f"{field} is not bound to subject_head")
    return target


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
        _evidence_file(evidence[field], f"{name}.{field}", root, subject_head)


def check(path):
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
    for index, name in enumerate(ORDER):
        record = gates.get(name)
        if record is None:
            if index < required_count:
                raise ValueError("required gate record missing: " + name)
            continue
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
    return {"result": "PASS", "path": str(path), "phase": lifecycle["phase"]}


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
