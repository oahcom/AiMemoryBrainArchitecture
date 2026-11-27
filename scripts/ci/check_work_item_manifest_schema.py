#!/usr/bin/env python3
"""Validate Work Item manifests and ratchet legacy findings against a pinned tree."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import subprocess
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
DOC_RELATIONSHIPS = {"normative", "design", "implementation", "evidence", "reference", "code", "schema"}
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


def validate_text(content: str, label: str = "<manifest>", tree_paths: set[str] | None = None) -> list[str]:
    try:
        data = yaml.load(content, Loader=UniqueKeyLoader)
    except (UnicodeError, yaml.YAMLError) as exc:
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
        elif not docs:
            errors.append("documentation must contain at least one reference")
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
                if not isinstance(ref, str) or not ref:
                    errors.append(f"documentation[{i}].path must be a non-empty repository-relative path")
                else:
                    parsed = PurePosixPath(ref)
                    if parsed.is_absolute() or ".." in parsed.parts or "\\" in ref:
                        errors.append(f"documentation[{i}].path must be repository-relative without '..': {ref}")
                    elif tree_paths is not None and ref not in tree_paths:
                        errors.append(f"documentation[{i}].path not in git tree: {ref}")
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
                if isinstance(ref, str) and not (
                    PurePosixPath(ref).name.startswith("session-evidence")
                    and PurePosixPath(ref).name.endswith(".md")
                ):
                    errors.append(f"session_evidence[{i}].session_evidence_ref must match session-evidence*.md")
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


def validate(path: Path, tree_paths: set[str] | None = None) -> list[str]:
    try:
        return validate_text(path.read_text(encoding="utf-8"), path.as_posix(), tree_paths)
    except (OSError, UnicodeError) as exc:
        return [f"read error: {exc}"]


def git_tree_paths(root: Path, tree: str) -> set[str]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", tree],
        cwd=root, text=True, capture_output=True, check=True,
    )
    return set(result.stdout.splitlines())


def git_show(root: Path, tree: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{tree}:{path}"],
        cwd=root, text=True, capture_output=True, check=True,
    )
    return result.stdout


def is_ac4(error: str) -> bool:
    return "documentation" in error.lower()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--tree", default="HEAD", help="Git tree-ish used for path existence checks")
    parser.add_argument("--baseline", type=Path, help="JSON file pinning a legacy baseline tree")
    parser.add_argument("--batch-report", action="store_true", help="print before/after AC4 counts for the pinned 83-manifest cohort")
    args = parser.parse_args()
    paths = sorted(args.root.glob(GLOB))
    if not paths:
        print(f"ERROR: no manifests found: {args.root / GLOB}", file=sys.stderr)
        return 2
    try:
        tree_paths = git_tree_paths(args.root, args.tree)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: cannot enumerate git tree {args.tree}: {exc}", file=sys.stderr)
        return 2

    baseline_tree = None
    baseline_errors: dict[str, set[str]] = {}
    if args.baseline:
        try:
            baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
            baseline_tree = baseline["baseline_tree"]
            baseline_paths = git_tree_paths(args.root, baseline_tree)
            manifest_paths = sorted(
                p for p in baseline_paths
                if p.startswith("14-ai-development/work-items/") and p.endswith("/manifest.yaml")
            )
            for rel in manifest_paths:
                try:
                    baseline_errors[rel] = set(validate_text(
                        git_show(args.root, baseline_tree, rel), rel, baseline_paths
                    ))
                except (OSError, subprocess.CalledProcessError):
                    baseline_errors[rel] = {"baseline manifest could not be read"}
        except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
            print(f"ERROR: cannot load baseline: {exc}", file=sys.stderr)
            return 2

    if args.batch_report:
        try:
            cohort_tree = baseline["cohort_tree"]
            cohort_paths = sorted(
                p for p in git_tree_paths(args.root, cohort_tree)
                if p.startswith("14-ai-development/work-items/") and p.endswith("/manifest.yaml")
            )
            if len(cohort_paths) != 83:
                raise ValueError(f"expected 83 cohort manifests, found {len(cohort_paths)}")
            print("AC4 migration batch comparison (baseline tree -> current tree):")
            for batch_no, start in enumerate((0, 21, 42, 63), start=1):
                batch = cohort_paths[start:start + (21 if batch_no < 4 else 20)]
                before_bad, after_bad = [], []
                for rel in batch:
                    before_errors = validate_text(
                        git_show(args.root, baseline_tree, rel), rel,
                        git_tree_paths(args.root, cohort_tree)
                    )
                    current_file = args.root / rel
                    after_errors = validate(current_file, tree_paths)
                    if any(is_ac4(e) for e in before_errors):
                        before_bad.append(rel)
                    if any(is_ac4(e) for e in after_errors):
                        after_bad.append(rel)
                print(
                    f"  batch {batch_no}/4: total={len(batch)} "
                    f"before_AC4_violations={len(before_bad)} "
                    f"after_AC4_violations={len(after_bad)} "
                    f"resolved={len(before_bad) - len(after_bad)}"
                )
                for rel in before_bad:
                    print(f"    BEFORE {rel}: missing/invalid documentation reference")
                for rel in after_bad:
                    print(f"    AFTER  {rel}: AC4 documentation violation remains")
        except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
            print(f"ERROR: cannot produce batch report: {exc}", file=sys.stderr)
            return 2

    compliant, ac4, other, regressions = [], [], [], []
    for path in paths:
        rel = path.relative_to(args.root).as_posix()
        errors = validate(path, tree_paths)
        if not errors:
            compliant.append(rel)
        ac4_errors = [e for e in errors if is_ac4(e)]
        other_errors = [e for e in errors if not is_ac4(e)]
        if ac4_errors:
            ac4.append((rel, ac4_errors))
        if other_errors:
            other.append((rel, other_errors))
        old = baseline_errors.get(rel, set()) if baseline_tree else set()
        for error in errors:
            if error not in old:
                regressions.append((rel, error))

    print(f"Manifest schema v2: total={len(paths)} compliant={len(compliant)}")
    print(f"AC4 violations: {len(ac4)} manifest(s)")
    for rel, errors in ac4:
        print(f"  {rel}")
        for error in errors:
            print(f"    - {error}")
    print(f"Other schema violations: {len(other)} manifest(s)")
    for rel, errors in other:
        print(f"  {rel}")
        for error in errors:
            print(f"    - {error}")
    print(f"New violations versus baseline: {len(regressions)}")
    for rel, error in regressions:
        print(f"  {rel}: {error}")
    if baseline_tree:
        print(f"Legacy ratchet baseline tree: {baseline_tree}")
    print("Read-only: no manifest or repository file is modified.")
    return 1 if regressions else 0


if __name__ == "__main__":
    raise SystemExit(main())
