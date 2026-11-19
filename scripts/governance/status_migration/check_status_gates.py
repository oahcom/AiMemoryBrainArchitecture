#!/usr/bin/env python3
"""Fail-closed validator for exact work-item status and structured gate evidence."""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml


class UniqueKeySafeLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int, float, bool, tuple)):
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "unhashable mapping key", key_node.start_mark)
        if key in result:
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
PLACEHOLDERS = {"", "n/a", "na", "none", "null", "todo", "tbd",
                "not_recorded", "not_verified", "fake", "test://exact-run"}


def _meaningful(value, field):
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in PLACEHOLDERS or len(value) < 3:
            raise ValueError(f"empty/placeholder evidence content: {field}")
        if field in {"tested_head", "reviewed_head", "merge_commit"} and not SHA_RE.fullmatch(value):
            raise ValueError(f"{field} must be a full 40-character commit SHA")
        return
    if isinstance(value, list):
        if not value:
            raise ValueError(f"empty evidence list: {field}")
        for item in value:
            _meaningful(item, field)
        return
    if isinstance(value, dict):
        if not value:
            raise ValueError(f"empty evidence mapping: {field}")
        for key, item in value.items():
            _meaningful(item, f"{field}.{key}")
        return
    raise ValueError(f"invalid evidence content type: {field}")


def _validate_evidence(name, evidence, data, lifecycle):
    if not isinstance(evidence, dict):
        raise ValueError("PASS gate evidence must be a structured mapping: " + name)
    for field in EVIDENCE_FIELDS[name]:
        if field not in evidence:
            raise ValueError(f"required evidence field missing: {name}.{field}")
        _meaningful(evidence[field], f"{name}.{field}")
    if name == "verified":
        subject_head = lifecycle.get("subject_head") or data.get("subject_head")
        if not isinstance(subject_head, str) or not SHA_RE.fullmatch(subject_head):
            raise ValueError("manifest subject_head must be a full commit SHA for VERIFIED")
        if evidence["tested_head"] != subject_head:
            raise ValueError("VERIFIED tested_head does not match manifest subject_head")
    elif name == "independent_review":
        subject_head = lifecycle.get("subject_head") or data.get("subject_head")
        if not isinstance(subject_head, str) or not SHA_RE.fullmatch(subject_head):
            raise ValueError("manifest subject_head must be a full commit SHA for REVIEWED")
        if evidence["reviewed_head"] != subject_head:
            raise ValueError("REVIEWED reviewed_head does not match manifest subject_head")
        if evidence["reviewer"].strip().casefold() == evidence["implementer"].strip().casefold():
            raise ValueError("REVIEWED reviewer and implementer must be different identities")


def check(path):
    data = yaml.load(Path(path).read_bytes(), Loader=UniqueKeySafeLoader)
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
    gates = lifecycle.get("gates")
    if not isinstance(gates, dict):
        raise ValueError("lifecycle.gates must be a mapping")
    required_count = REQUIRED.get(source, 0)
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
        if disposition == "PASS":
            if "evidence" not in record:
                raise ValueError("PASS gate evidence missing: " + name)
            _validate_evidence(name, record["evidence"], data, lifecycle)
        elif index < required_count:
            raise ValueError("required gate not proven PASS: " + name)
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
