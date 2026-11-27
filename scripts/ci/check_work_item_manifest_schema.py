#!/usr/bin/env python3
"""Read-only structural validator for Work Item manifests.

Validates the AID-2026-251 manifest contract without rewriting any input.
Legacy manifests are reported individually so migration can be planned rather
than silently performed by a gate.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml
from yaml.constructor import ConstructorError

ROOT = Path(__file__).resolve().parents[2]
GLOB = "14-ai-development/work-items/*/manifest.yaml"
REQUIRED = (
    "work_item_id", "title", "class", "risk", "risk_rationale", "status",
    "id_status", "sponsor", "accountable_owner", "acceptance_authority",
    "attribution", "date", "repository", "base_branch", "base_commit_sha",
    "scope", "evidence", "documentation", "session_evidence", "implementation",
)
DOC_RELATIONSHIPS = {"normative", "design", "implementation", "evidence", "reference"}
IMPL_STATUSES = {"NOT_STARTED", "IN_PROGRESS", "IMPLEMENTED", "BLOCKED", "NOT_APPLICABLE"}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ConstructorError("while constructing a mapping", node.start_mark,
                                   f"duplicate key {key!r}", key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def validate(path: Path) -> list[str]:
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return [f"YAML: {' '.join(str(exc).split())}"]
    errors = []
    if not isinstance(data, dict):
        return ["document root must be a mapping"]
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required top-level key: {key}")
    if "documentation" in data:
        docs = data["documentation"]
        if not isinstance(docs, list):
            errors.append("documentation must be a sequence of {path, relationship} mappings")
        else:
            for i, item in enumerate(docs):
                if not isinstance(item, dict):
                    errors.append(f"documentation[{i}] must be a mapping")
                    continue
                for key in ("path", "relationship"):
                    if key not in item:
                        errors.append(f"documentation[{i}] missing {key}")
                if item.get("relationship") not in DOC_RELATIONSHIPS:
                    errors.append(f"documentation[{i}].relationship must be one of {sorted(DOC_RELATIONSHIPS)}")
                ref = item.get("path")
                if isinstance(ref, str) and (not ref.endswith(".md") or ref.startswith("/") or ".." in Path(ref).parts):
                    errors.append(f"documentation[{i}].path must be a repository-relative .md path")
    if "session_evidence" in data:
        records = data["session_evidence"]
        if not isinstance(records, list) or not records:
            errors.append("session_evidence must be a non-empty sequence of mappings")
        else:
            for i, item in enumerate(records):
                if not isinstance(item, dict):
                    errors.append(f"session_evidence[{i}] must be a mapping")
                    continue
                for key in ("role", "issue_refs", "implementing_ai_session", "session_evidence_ref"):
                    if key not in item:
                        errors.append(f"session_evidence[{i}] missing {key}")
                ref = item.get("session_evidence_ref")
                if isinstance(ref, str) and not ref.endswith("session-evidence.md"):
                    errors.append(f"session_evidence[{i}].session_evidence_ref must end in session-evidence.md")
    if "implementation" in data:
        impl = data["implementation"]
        if not isinstance(impl, dict):
            errors.append("implementation must be a mapping")
        else:
            for key in ("status", "summary", "files_changed", "tests"):
                if key not in impl:
                    errors.append(f"implementation missing {key}")
            if impl.get("status") not in IMPL_STATUSES:
                errors.append(f"implementation.status must be one of {sorted(IMPL_STATUSES)}")
            for key in ("files_changed", "tests"):
                if key in impl and not isinstance(impl[key], list):
                    errors.append(f"implementation.{key} must be a sequence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    paths = sorted(args.root.glob(GLOB))
    if not paths:
        print(f"ERROR: no manifests found: {args.root / GLOB}", file=sys.stderr)
        return 2
    compliant, violations = [], []
    for path in paths:
        errors = validate(path)
        rel = path.relative_to(args.root).as_posix()
        if errors:
            violations.append((rel, errors))
        else:
            compliant.append(rel)
    print(f"Manifest schema v1: total={len(paths)} compliant={len(compliant)} violations={len(violations)}")
    print("COMPLIANT:")
    for item in compliant:
        print(f"  {item}")
    print("VIOLATIONS:")
    for path, errors in violations:
        print(f"  {path}")
        for error in errors:
            print(f"    - {error}")
    print("Read-only: no manifest or repository file is modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
