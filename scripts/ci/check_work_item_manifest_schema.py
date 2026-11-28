#!/usr/bin/env python3
"""Validate Work Item manifests and enforce an explicit legacy-finding ratchet."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from typing import Any

import yaml
from yaml.constructor import ConstructorError


ROOT = Path(__file__).resolve().parents[2]
GLOB = "14-ai-development/work-items/*/manifest.yaml"
SCHEMA_PATH = "14-ai-development/work-items/work-item-manifest.schema.yaml"
DEFAULT_COHORT = (
    "14-ai-development/reports/work-item-legacy-cohort.json"
)
DEFAULT_LEDGER = (
    "14-ai-development/reports/work-item-legacy-disposition.json"
)
LEDGER_GENERATED_BY = (
    "scripts/ci/check_work_item_manifest_schema.py --generate-ledger"
)
LEDGER_PLACEHOLDERS = {
    "rationale": (
        "TODO: describe why this legacy finding remains"
    ),
    "accountable_owner": "TODO: assign an accountable owner",
    "migration_plan": "TODO: specify a verifiable migration plan",
}
LEDGER_DISPOSITIONS = {"OPEN", "ACCEPTED_RISK", "MIGRATED"}
LEDGER_ENTRY_KEYS = {
    "finding_id", "manifest_path", "rule_id", "pointer", "disposition",
    "rationale", "accountable_owner", "migration_plan",
    "resolution_commit", "resolution_evidence",
}
COHORT_KEYS = {
    "schema_version", "baseline_commit", "baseline_tree",
    "cohort_tree", "manifest_paths",
}

# These constants intentionally remain only for the legacy compatibility path.
# --all-manifests and the legacy baseline comparison use the selected Git tree's
# schema rather than this compatibility rule set.
REQUIRED = (
    "work_item_id", "title", "class", "risk", "risk_rationale", "status",
    "id_status", "sponsor", "accountable_owner", "acceptance_authority",
    "attribution", "date", "repository", "base_branch", "base_commit_sha",
    "scope", "evidence", "documentation", "session_evidence", "implementation",
)
DOC_RELATIONSHIPS = {
    "normative", "design", "implementation", "evidence",
    "reference", "code", "schema",
}
IMPL_STATUSES = {
    "NOT_STARTED", "IN_PROGRESS", "IMPLEMENTED", "BLOCKED", "NOT_APPLICABLE",
}

SCHEMA_ROOT_KEYS = {"schema_version", "required_top_level_keys", "fields"}
SCHEMA_FIELD_KEYS = {
    "documentation": {
        "kind", "required", "min_items", "item_required_keys", "path_kind",
        "path_must_exist_in_git_tree", "relationship_enum",
    },
    "session_evidence": {
        "kind", "required", "item_required_keys",
        "session_evidence_ref_pattern", "session_evidence_ref_exact_allowlist",
    },
    "implementation": {
        "kind", "required", "required_keys", "status_enum",
        "files_changed_kind", "tests_kind",
    },
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _mapping,
)


class GitCommandError(RuntimeError):
    def __init__(self, command: list[str], returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(
            f"git command failed with exit {returncode}: "
            f"{' '.join(command)}: {stderr.strip()}"
        )


class GitOutputDecodeError(RuntimeError):
    def __init__(self, command: list[str], stream: str, error: UnicodeDecodeError):
        self.command = command
        self.stream = stream
        self.error = error
        super().__init__(
            f"git output decode failed: stream={stream} "
            f"encoding=utf-8 offset={error.start}"
        )


class SchemaConfigurationError(RuntimeError):
    pass


class LegacyConfigurationError(RuntimeError):
    pass


def run_git_utf8(args: list[str], root: Path) -> str:
    """Run Git using strict UTF-8 for repository data."""
    result = subprocess.run(
        args, cwd=root, capture_output=True, text=False, check=False,
    )
    try:
        stdout = result.stdout.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise GitOutputDecodeError(args, "stdout", exc) from exc
    stderr = result.stderr.decode("utf-8", errors="replace")
    if result.returncode != 0:
        raise GitCommandError(args, result.returncode, stderr)
    return stdout


def git_tree_paths(root: Path, tree: str) -> set[str]:
    output = run_git_utf8(
        ["git", "ls-tree", "-r", "-z", "--name-only", tree], root,
    )
    return {item for item in output.split("\0") if item}


def git_show(root: Path, tree: str, path: str) -> str:
    return run_git_utf8(["git", "show", f"{tree}:{path}"], root)


def git_resolve_tree(root: Path, commit: str) -> str:
    output = run_git_utf8(
        ["git", "rev-parse", "--verify", f"{commit}^{{tree}}"], root,
    )
    return output.strip()


def discover_manifest_paths(tree_paths: set[str]) -> list[str]:
    prefix = "14-ai-development/work-items/"
    suffix = "/manifest.yaml"
    return sorted(
        path for path in tree_paths
        if path.startswith(prefix) and path.endswith(suffix)
    )


def _parse_yaml(content: str, label: str) -> Any:
    try:
        return yaml.load(content, Loader=UniqueKeyLoader)
    except (UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"{label}: {' '.join(str(exc).split())}") from exc


# ---------------------------------------------------------------------------
# Legacy validation path. Its rules and default invocation semantics remain.
# ---------------------------------------------------------------------------

def validate_text(
    content: str,
    label: str = "<manifest>",
    tree_paths: set[str] | None = None,
) -> list[str]:
    try:
        data = _parse_yaml(content, label)
    except ValueError as exc:
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
            errors.append(
                "documentation must be a sequence of {path, relationship} mappings"
            )
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
                    errors.append(
                        f"documentation[{i}].relationship must be one of "
                        f"{sorted(DOC_RELATIONSHIPS)}"
                    )
                ref = item.get("path")
                if not isinstance(ref, str) or not ref:
                    errors.append(
                        f"documentation[{i}].path must be a non-empty "
                        "repository-relative path"
                    )
                else:
                    parsed = PurePosixPath(ref)
                    if (
                        parsed.is_absolute()
                        or ".." in parsed.parts
                        or "\\" in ref
                    ):
                        errors.append(
                            "documentation"
                            f"[{i}].path must be repository-relative "
                            f"without '..': {ref}"
                        )
                    elif tree_paths is not None and ref not in tree_paths:
                        errors.append(
                            f"documentation[{i}].path not in git tree: {ref}"
                        )

    if "session_evidence" in data:
        records = data["session_evidence"]
        if not isinstance(records, list) or not records:
            errors.append(
                "session_evidence must be a non-empty sequence of mappings"
            )
        else:
            for i, item in enumerate(records):
                if not isinstance(item, dict):
                    errors.append(f"session_evidence[{i}] must be a mapping")
                    continue
                for key in (
                    "role", "issue_refs", "implementing_ai_session",
                    "session_evidence_ref",
                ):
                    if key not in item:
                        errors.append(f"session_evidence[{i}] missing {key}")
                ref = item.get("session_evidence_ref")
                if isinstance(ref, str) and not (
                    (
                        PurePosixPath(ref).name.startswith("session-evidence")
                        and PurePosixPath(ref).name.endswith(".md")
                    )
                    or PurePosixPath(ref).name == "ac4-repair-evidence.md"
                ):
                    errors.append(
                        f"session_evidence[{i}].session_evidence_ref "
                        "must match session-evidence*.md"
                    )

    if "implementation" in data:
        impl = data["implementation"]
        if not isinstance(impl, dict):
            errors.append("implementation must be a mapping")
        else:
            for key in ("status", "summary", "files_changed", "tests"):
                if key not in impl:
                    errors.append(f"implementation missing {key}")
            if impl.get("status") not in IMPL_STATUSES:
                errors.append(
                    f"implementation.status must be one of "
                    f"{sorted(IMPL_STATUSES)}"
                )
            for key in ("files_changed", "tests"):
                if key in impl and not isinstance(impl[key], list):
                    errors.append(f"implementation.{key} must be a sequence")
    return errors


def validate(path: Path, tree_paths: set[str] | None = None) -> list[str]:
    try:
        return validate_text(
            path.read_text(encoding="utf-8"), path.as_posix(), tree_paths,
        )
    except (OSError, UnicodeError) as exc:
        return [f"read error: {exc}"]


def is_ac4(error: str) -> bool:
    return "documentation" in error.lower()


# ---------------------------------------------------------------------------
# Schema-driven validation.
# ---------------------------------------------------------------------------

def _schema_error(message: str) -> SchemaConfigurationError:
    return SchemaConfigurationError(message)


def _require_mapping(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        raise _schema_error(f"{label} must be a mapping")
    return value


def _require_string_list(
    value: Any, label: str, *, nonempty: bool = True,
) -> list[str]:
    if not isinstance(value, list):
        raise _schema_error(f"{label} must be a sequence")
    if nonempty and not value:
        raise _schema_error(f"{label} must not be empty")
    if any(not isinstance(item, str) or not item for item in value):
        raise _schema_error(f"{label} must contain non-empty strings")
    if len(value) != len(set(value)):
        raise _schema_error(f"{label} contains duplicate values")
    return value


def validate_schema_definition(schema: Any) -> dict:
    root = _require_mapping(schema, "schema root")
    unknown_root = set(root) - SCHEMA_ROOT_KEYS
    missing_root = SCHEMA_ROOT_KEYS - set(root)
    if unknown_root:
        raise _schema_error(
            f"unsupported schema root keyword(s): {sorted(unknown_root)}"
        )
    if missing_root:
        raise _schema_error(
            f"missing schema root keyword(s): {sorted(missing_root)}"
        )
    if not isinstance(root["schema_version"], (str, int)):
        raise _schema_error("schema_version must be a string or integer")

    _require_string_list(root["required_top_level_keys"], "required_top_level_keys")
    fields = _require_mapping(root["fields"], "fields")
    unknown_fields = set(fields) - set(SCHEMA_FIELD_KEYS)
    if unknown_fields:
        raise _schema_error(
            f"unsupported schema field(s): {sorted(unknown_fields)}"
        )

    for field_name, allowed_keys in SCHEMA_FIELD_KEYS.items():
        if field_name not in fields:
            raise _schema_error(f"missing schema field definition: {field_name}")
        definition = _require_mapping(fields[field_name], f"fields.{field_name}")
        unknown = set(definition) - allowed_keys
        if unknown:
            raise _schema_error(
                f"unsupported schema keyword(s) in fields.{field_name}: "
                f"{sorted(unknown)}"
            )

    docs = fields["documentation"]
    if docs.get("kind") != "sequence":
        raise _schema_error("fields.documentation.kind must be 'sequence'")
    if not isinstance(docs.get("required"), bool):
        raise _schema_error("fields.documentation.required must be boolean")
    if not isinstance(docs.get("min_items"), int) or docs["min_items"] < 0:
        raise _schema_error("fields.documentation.min_items must be >= 0")
    _require_string_list(
        docs.get("item_required_keys"), "fields.documentation.item_required_keys",
    )
    if docs.get("path_kind") != "repository-relative-path":
        raise _schema_error("unsupported fields.documentation.path_kind")
    if not isinstance(docs.get("path_must_exist_in_git_tree"), bool):
        raise _schema_error(
            "fields.documentation.path_must_exist_in_git_tree must be boolean"
        )
    _require_string_list(docs.get("relationship_enum"), "fields.documentation.relationship_enum")

    session = fields["session_evidence"]
    if session.get("kind") != "sequence":
        raise _schema_error("fields.session_evidence.kind must be 'sequence'")
    if not isinstance(session.get("required"), bool):
        raise _schema_error("fields.session_evidence.required must be boolean")
    _require_string_list(
        session.get("item_required_keys"), "fields.session_evidence.item_required_keys",
    )
    pattern = session.get("session_evidence_ref_pattern")
    if not isinstance(pattern, str) or not pattern:
        raise _schema_error(
            "fields.session_evidence.session_evidence_ref_pattern must be non-empty"
        )
    _require_string_list(
        session.get("session_evidence_ref_exact_allowlist"),
        "fields.session_evidence.session_evidence_ref_exact_allowlist",
        nonempty=False,
    )

    implementation = fields["implementation"]
    if implementation.get("kind") != "mapping":
        raise _schema_error("fields.implementation.kind must be 'mapping'")
    if not isinstance(implementation.get("required"), bool):
        raise _schema_error("fields.implementation.required must be boolean")
    _require_string_list(
        implementation.get("required_keys"), "fields.implementation.required_keys",
    )
    _require_string_list(
        implementation.get("status_enum"), "fields.implementation.status_enum",
    )
    for key in ("files_changed_kind", "tests_kind"):
        if implementation.get(key) != "sequence":
            raise _schema_error(f"fields.implementation.{key} must be 'sequence'")
    return root


def load_manifest_schema(root: Path, tree: str) -> dict:
    try:
        content = git_show(root, tree, SCHEMA_PATH)
    except (GitCommandError, GitOutputDecodeError) as exc:
        raise _schema_error(f"cannot read {SCHEMA_PATH}: {exc}") from exc
    try:
        schema = _parse_yaml(content, SCHEMA_PATH)
    except ValueError as exc:
        raise _schema_error(f"cannot parse {SCHEMA_PATH}: {exc}") from exc
    return validate_schema_definition(schema)


def _pointer(*parts: Any) -> str:
    escaped = [
        str(part).replace("~", "~0").replace("/", "~1")
        for part in parts
    ]
    return "/" + "/".join(escaped)


def _finding(
    manifest_path: str,
    rule_id: str,
    category: str,
    pointer: str,
    message: str,
) -> dict[str, str]:
    return {
        "manifest_path": manifest_path,
        "rule_id": rule_id,
        "category": category,
        "pointer": pointer,
        "message": message,
    }


def finding_identity(finding: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(finding["manifest_path"]),
        str(finding["rule_id"]),
        str(finding["pointer"]),
    )


def finding_id(identity: tuple[str, str, str]) -> str:
    encoded = json.dumps(
        list(identity), ensure_ascii=False, separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_against_schema(
    data: Any,
    manifest_path: str,
    schema: dict,
    tree_paths: set[str],
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(rule_id: str, category: str, pointer: str, message: str) -> None:
        findings.append(_finding(manifest_path, rule_id, category, pointer, message))

    if not isinstance(data, dict):
        add("manifest.root.mapping", "OTHER_SCHEMA", "", "document root must be a mapping")
        return findings

    for key in schema["required_top_level_keys"]:
        if key not in data:
            add(
                f"top_level.{key}.required", "OTHER_SCHEMA", _pointer(key),
                f"missing required top-level key: {key}",
            )

    fields = schema["fields"]
    docs_rule = fields["documentation"]
    docs_present = "documentation" in data
    if docs_rule["required"] and not docs_present:
        add("documentation.required", "AC4", "/documentation", "documentation is required")
    elif docs_present:
        docs = data["documentation"]
        if not isinstance(docs, list):
            add(
                "documentation.kind.sequence", "AC4", "/documentation",
                "documentation must be a sequence",
            )
        else:
            minimum = docs_rule["min_items"]
            if len(docs) < minimum:
                add(
                    "documentation.min_items", "AC4", "/documentation",
                    f"documentation must contain at least {minimum} reference(s)",
                )
            required_keys = docs_rule["item_required_keys"]
            relationships = set(docs_rule["relationship_enum"])
            for index, item in enumerate(docs):
                base = _pointer("documentation", index)
                if not isinstance(item, dict):
                    add(
                        "documentation.item.mapping", "AC4", base,
                        f"documentation[{index}] must be a mapping",
                    )
                    continue
                for key in required_keys:
                    if key not in item:
                        add(
                            "documentation.item.required_key", "AC4",
                            _pointer("documentation", index, key),
                            f"documentation[{index}] missing {key}",
                        )
                if item.get("relationship") not in relationships:
                    add(
                        "documentation.relationship.enum", "AC4",
                        _pointer("documentation", index, "relationship"),
                        "documentation relationship must be one of "
                        f"{sorted(relationships)}",
                    )
                if "path" in item:
                    ref = item.get("path")
                    if not isinstance(ref, str) or not ref:
                        add(
                            "documentation.path.nonempty", "AC4",
                            _pointer("documentation", index, "path"),
                            "documentation path must be a non-empty string",
                        )
                    else:
                        parsed = PurePosixPath(ref)
                        if (
                            parsed.is_absolute() or ".." in parsed.parts
                            or "\\" in ref or ref.startswith("/")
                        ):
                            add(
                                "documentation.path.repository_relative", "AC4",
                                _pointer("documentation", index, "path"),
                                f"documentation path is not repository-relative: {ref}",
                            )
                        elif (
                            docs_rule["path_must_exist_in_git_tree"]
                            and ref not in tree_paths
                        ):
                            add(
                                "documentation.path.exists_in_git_tree", "AC4",
                                _pointer("documentation", index, "path"),
                                f"documentation path not in git tree: {ref}",
                            )

    session_rule = fields["session_evidence"]
    session_present = "session_evidence" in data
    if session_rule["required"] and not session_present:
        add(
            "session_evidence.required", "OTHER_SCHEMA", "/session_evidence",
            "session_evidence is required",
        )
    elif session_present:
        records = data["session_evidence"]
        if not isinstance(records, list) or not records:
            add(
                "session_evidence.kind.nonempty_sequence", "OTHER_SCHEMA",
                "/session_evidence",
                "session_evidence must be a non-empty sequence",
            )
        else:
            required_keys = session_rule["item_required_keys"]
            pattern = session_rule["session_evidence_ref_pattern"]
            allowlist = set(session_rule["session_evidence_ref_exact_allowlist"])
            for index, item in enumerate(records):
                base = _pointer("session_evidence", index)
                if not isinstance(item, dict):
                    add(
                        "session_evidence.item.mapping", "OTHER_SCHEMA", base,
                        f"session_evidence[{index}] must be a mapping",
                    )
                    continue
                for key in required_keys:
                    if key not in item:
                        add(
                            "session_evidence.item.required_key", "OTHER_SCHEMA",
                            _pointer("session_evidence", index, key),
                            f"session_evidence[{index}] missing {key}",
                        )
                ref = item.get("session_evidence_ref")
                if isinstance(ref, str):
                    basename = PurePosixPath(ref).name
                    if (
                        basename not in allowlist
                        and not fnmatch.fnmatchcase(basename, pattern)
                    ):
                        add(
                            "session_evidence.ref.pattern", "OTHER_SCHEMA",
                            _pointer("session_evidence", index, "session_evidence_ref"),
                            "session_evidence_ref must match "
                            f"{pattern!r} or the exact allowlist",
                        )

    implementation_rule = fields["implementation"]
    implementation_present = "implementation" in data
    if implementation_rule["required"] and not implementation_present:
        add(
            "implementation.required", "OTHER_SCHEMA", "/implementation",
            "implementation is required",
        )
    elif implementation_present:
        implementation = data["implementation"]
        if not isinstance(implementation, dict):
            add(
                "implementation.kind.mapping", "OTHER_SCHEMA", "/implementation",
                "implementation must be a mapping",
            )
        else:
            for key in implementation_rule["required_keys"]:
                if key not in implementation:
                    add(
                        "implementation.required_key", "OTHER_SCHEMA",
                        _pointer("implementation", key),
                        f"implementation missing {key}",
                    )
            if (
                "status" in implementation
                and implementation.get("status")
                not in set(implementation_rule["status_enum"])
            ):
                add(
                    "implementation.status.enum", "OTHER_SCHEMA",
                    "/implementation/status",
                    "implementation.status must be one of "
                    f"{sorted(implementation_rule['status_enum'])}",
                )
            for key, expected_kind in (
                ("files_changed", implementation_rule["files_changed_kind"]),
                ("tests", implementation_rule["tests_kind"]),
            ):
                if key in implementation:
                    if expected_kind == "sequence" and not isinstance(implementation[key], list):
                        add(
                            f"implementation.{key}.kind.sequence", "OTHER_SCHEMA",
                            _pointer("implementation", key),
                            f"implementation.{key} must be a sequence",
                        )
    return findings


def collect_findings(
    root: Path,
    tree: str,
    manifest_paths: list[str],
    schema: dict,
    tree_paths: set[str],
) -> dict[tuple[str, str, str], dict[str, str]]:
    """The single finding collector used by generation and ledger validation."""
    collected: dict[tuple[str, str, str], dict[str, str]] = {}
    for rel in manifest_paths:
        content = git_show(root, tree, rel)
        try:
            data = _parse_yaml(content, rel)
        except ValueError as exc:
            raise LegacyConfigurationError(
                f"cannot parse manifest {rel} in tree {tree}: {exc}"
            ) from exc
        for finding in validate_against_schema(data, rel, schema, tree_paths):
            identity = finding_identity(finding)
            if identity in collected:
                raise LegacyConfigurationError(
                    f"finding collector produced duplicate identity: {identity}"
                )
            collected[identity] = finding
    return collected


def _json_report(
    tree: str,
    discovered_paths: list[str],
    manifest_results: list[dict],
    schema_source: str,
) -> dict:
    all_findings = [
        finding for result in manifest_results
        for finding in result.get("findings", [])
    ]
    ac4_findings = [f for f in all_findings if f["category"] == "AC4"]
    other_findings = [f for f in all_findings if f["category"] == "OTHER_SCHEMA"]
    parse_errors = sum(1 for r in manifest_results if r["status"] == "PARSE_ERROR")
    decode_errors = sum(1 for r in manifest_results if r["status"] == "DECODE_ERROR")
    read_errors = sum(1 for r in manifest_results if r["status"] == "READ_ERROR")
    incomplete = sum(
        1 for r in manifest_results
        if r["status"] in {"PARSE_ERROR", "DECODE_ERROR", "READ_ERROR"}
    )
    validated = sum(1 for r in manifest_results if r["status"] in {"PASS", "VIOLATION"})
    return {
        "tree": tree,
        "schema_source": schema_source,
        "population": "ALL_DISCOVERED_MANIFESTS",
        "discovered": len(discovered_paths),
        "validated": validated,
        "incomplete": incomplete,
        "parse_errors": parse_errors,
        "decode_errors": decode_errors,
        "read_errors": read_errors,
        "ac4_violations": len(ac4_findings),
        "ac4_manifests": len({f["manifest_path"] for f in ac4_findings}),
        "other_schema_violations": len(other_findings),
        "other_schema_manifests": len({f["manifest_path"] for f in other_findings}),
        "schema_checker_divergences": 0,
        "manifests": manifest_results,
    }


def run_all_manifests(args: argparse.Namespace) -> int:
    try:
        tree_paths = git_tree_paths(args.root, args.tree)
        manifest_paths = discover_manifest_paths(tree_paths)
        if not manifest_paths:
            raise GitCommandError(
                ["git", "ls-tree", "-r", args.tree], 1,
                "no Work Item manifests found in selected Git tree",
            )
        schema = load_manifest_schema(args.root, args.tree)
    except SchemaConfigurationError as exc:
        print(f"ERROR: schema configuration invalid: {exc}", file=sys.stderr)
        return 2
    except GitOutputDecodeError as exc:
        print(
            "ERROR: git output decode failed: "
            f"stream={exc.stream} encoding=utf-8 offset={exc.error.start}",
            file=sys.stderr,
        )
        return 2
    except GitCommandError as exc:
        print(f"ERROR: cannot read selected Git tree: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: cannot access Git repository: {exc}", file=sys.stderr)
        return 2

    results: list[dict] = []
    for rel in manifest_paths:
        try:
            content = git_show(args.root, args.tree, rel)
        except GitOutputDecodeError as exc:
            results.append({
                "path": rel, "status": "DECODE_ERROR", "findings": [],
                "error": (
                    "git output decode failed: stream=stdout "
                    f"encoding=utf-8 offset={exc.error.start}"
                ),
            })
            continue
        except (GitCommandError, OSError) as exc:
            results.append({
                "path": rel, "status": "READ_ERROR", "findings": [],
                "error": str(exc),
            })
            continue
        try:
            data = _parse_yaml(content, rel)
        except ValueError as exc:
            results.append({
                "path": rel, "status": "PARSE_ERROR", "findings": [],
                "error": str(exc),
            })
            continue
        findings = validate_against_schema(data, rel, schema, tree_paths)
        results.append({
            "path": rel, "status": "VIOLATION" if findings else "PASS",
            "findings": findings,
        })

    report = _json_report(args.tree, manifest_paths, results, SCHEMA_PATH)
    if args.report:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        for key in (
            "tree", "schema_source", "population", "discovered", "validated",
            "incomplete", "ac4_violations", "other_schema_violations",
        ):
            print(f"{key}={report[key]}")
        for result in results:
            if result["status"] == "PASS":
                continue
            print(f"{result['status']}: {result['path']}", file=sys.stderr)
            if "error" in result:
                print(f"  {result['error']}", file=sys.stderr)
            for finding in result["findings"]:
                print(
                    f"  {finding['rule_id']} {finding['pointer']}: "
                    f"{finding['message']}",
                    file=sys.stderr,
                )

    if report["incomplete"]:
        print(
            "ERROR: full-tree validation incomplete: "
            f"incomplete={report['incomplete']} "
            f"parse_errors={report['parse_errors']} "
            f"decode_errors={report['decode_errors']} "
            f"read_errors={report['read_errors']}",
            file=sys.stderr,
        )
        return 3 if (
            report["ac4_violations"] or report["other_schema_violations"]
        ) else 2

    has_violations = bool(report["ac4_violations"] or report["other_schema_violations"])
    if args.strict and has_violations:
        print(
            "ERROR: strict schema validation found violations: "
            f"ac4={report['ac4_violations']} "
            f"other={report['other_schema_violations']}",
            file=sys.stderr,
        )
        return 1
    if has_violations:
        print(
            "INFO: diagnostic mode completed with findings; "
            "use --strict to make findings fail the command.",
            file=sys.stderr,
        )
    return 0


# ---------------------------------------------------------------------------
# Explicit legacy cohort and finding-disposition ledger.
# ---------------------------------------------------------------------------

def _read_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LegacyConfigurationError(f"cannot load {label} {path}: {exc}") from exc


def load_cohort(path: Path, root: Path) -> dict:
    cohort = _read_json(path, "legacy cohort")
    if not isinstance(cohort, dict):
        raise LegacyConfigurationError("legacy cohort root must be an object")
    if set(cohort) != COHORT_KEYS:
        raise LegacyConfigurationError(
            "legacy cohort keys must be exactly "
            f"{sorted(COHORT_KEYS)}; found {sorted(cohort)}"
        )
    if cohort["schema_version"] != 1:
        raise LegacyConfigurationError("unsupported legacy cohort schema_version")
    for key in ("baseline_commit", "baseline_tree", "cohort_tree"):
        value = cohort[key]
        if not isinstance(value, str) or not value:
            raise LegacyConfigurationError(f"cohort.{key} must be a non-empty string")
    paths = cohort["manifest_paths"]
    if (
        not isinstance(paths, list)
        or any(not isinstance(p, str) or not p for p in paths)
        or len(paths) != len(set(paths))
    ):
        raise LegacyConfigurationError(
            "cohort.manifest_paths must be a unique sequence of non-empty paths"
        )
    if paths != sorted(paths):
        raise LegacyConfigurationError("cohort.manifest_paths must be sorted")
    for rel in paths:
        p = PurePosixPath(rel)
        if (
            p.is_absolute() or ".." in p.parts or "\\" in rel
            or not rel.startswith("14-ai-development/work-items/")
            or not rel.endswith("/manifest.yaml")
        ):
            raise LegacyConfigurationError(f"invalid cohort manifest path: {rel}")

    resolved_baseline_tree = git_resolve_tree(root, cohort["baseline_commit"])
    if resolved_baseline_tree != cohort["baseline_tree"]:
        raise LegacyConfigurationError(
            "cohort baseline_tree does not match baseline_commit: "
            f"declared={cohort['baseline_tree']} resolved={resolved_baseline_tree}"
        )
    actual_cohort_paths = discover_manifest_paths(
        git_tree_paths(root, cohort["cohort_tree"])
    )
    if set(actual_cohort_paths) != set(paths):
        missing = sorted(set(actual_cohort_paths) - set(paths))
        extra = sorted(set(paths) - set(actual_cohort_paths))
        raise LegacyConfigurationError(
            "cohort manifest_paths do not match cohort_tree enumeration: "
            f"missing={missing} extra={extra}"
        )
    return cohort


def _ledger_entry(finding: dict[str, str]) -> dict[str, Any]:
    identity = finding_identity(finding)
    return {
        "finding_id": finding_id(identity),
        "manifest_path": identity[0],
        "rule_id": identity[1],
        "pointer": identity[2],
        "disposition": "OPEN",
        "rationale": LEDGER_PLACEHOLDERS["rationale"],
        "accountable_owner": LEDGER_PLACEHOLDERS["accountable_owner"],
        "migration_plan": LEDGER_PLACEHOLDERS["migration_plan"],
        "resolution_commit": None,
        "resolution_evidence": None,
    }


def generate_ledger(
    baseline_findings: dict[tuple[str, str, str], dict[str, str]],
    cohort: dict,
    cohort_path: Path,
) -> dict:
    return {
        "schema_version": 1,
        "baseline_commit": cohort["baseline_commit"],
        "cohort": cohort_path.as_posix(),
        "generated_by": LEDGER_GENERATED_BY,
        "entries": [
            _ledger_entry(baseline_findings[key])
            for key in sorted(baseline_findings)
        ],
    }


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_ledger(
    ledger: Any,
    baseline_findings: dict[tuple[str, str, str], dict[str, str]],
    current_findings: dict[tuple[str, str, str], dict[str, str]],
    expected_baseline_commit: str,
    expected_cohort_path: str,
) -> tuple[list[dict[str, str]], dict[tuple[str, str, str], dict[str, Any]]]:
    errors: list[dict[str, str]] = []

    def error(code: str, message: str, finding_key: str = "") -> None:
        errors.append({
            "code": code,
            "finding_id": finding_key,
            "message": message,
        })

    if not isinstance(ledger, dict):
        error("INCOMPLETE_LEDGER_ENTRY", "ledger root must be a versioned object")
        return errors, {}
    expected_top = {
        "schema_version", "baseline_commit", "cohort", "generated_by", "entries",
    }
    if set(ledger) != expected_top:
        error(
            "INCOMPLETE_LEDGER_ENTRY",
            "ledger top-level keys must be exactly "
            f"{sorted(expected_top)}",
        )
    if ledger.get("schema_version") != 1:
        error("INCOMPLETE_LEDGER_ENTRY", "ledger schema_version must be 1")
    if ledger.get("baseline_commit") != expected_baseline_commit:
        error(
            "INCOMPLETE_LEDGER_ENTRY",
            "ledger baseline_commit does not match cohort baseline_commit",
        )
    if ledger.get("cohort") != expected_cohort_path:
        error("INCOMPLETE_LEDGER_ENTRY", "ledger cohort path does not match --legacy-cohort")
    if not _nonempty_text(ledger.get("generated_by")):
        error("INCOMPLETE_LEDGER_ENTRY", "ledger generated_by must be non-empty")
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        error("INCOMPLETE_LEDGER_ENTRY", "ledger entries must be an array")
        return errors, {}

    baseline_ids = {finding_id(key): key for key in baseline_findings}
    seen: dict[tuple[str, str, str], dict[str, Any]] = {}
    seen_ids: set[str] = set()

    for index, entry in enumerate(entries):
        label = f"entries[{index}]"
        if not isinstance(entry, dict):
            error("INCOMPLETE_LEDGER_ENTRY", f"{label} must be an object")
            continue
        if set(entry) != LEDGER_ENTRY_KEYS:
            error(
                "INCOMPLETE_LEDGER_ENTRY",
                f"{label} keys must be exactly {sorted(LEDGER_ENTRY_KEYS)}",
                str(entry.get("finding_id", "")),
            )
        required_identity = ("manifest_path", "rule_id", "pointer")
        if any(not _nonempty_text(entry.get(k)) for k in required_identity):
            error("INCOMPLETE_LEDGER_ENTRY", f"{label} has incomplete identity")
            continue
        identity = (
            entry["manifest_path"], entry["rule_id"], entry["pointer"],
        )
        expected_id = finding_id(identity)
        supplied_id = entry.get("finding_id")
        if supplied_id != expected_id:
            error(
                "INCOMPLETE_LEDGER_ENTRY",
                f"{label} finding_id does not match its identity",
                str(supplied_id or ""),
            )
        if expected_id in seen_ids:
            error("DUPLICATE_LEDGER_ENTRY", f"duplicate ledger identity at {label}", expected_id)
            continue
        seen_ids.add(expected_id)
        if expected_id not in baseline_ids:
            error("ORPHAN_LEDGER_ENTRY", f"{label} is not present in baseline findings", expected_id)
        else:
            seen[identity] = entry

        disposition = entry.get("disposition")
        if disposition not in LEDGER_DISPOSITIONS:
            error(
                "INCOMPLETE_LEDGER_ENTRY",
                f"{label} disposition must be one of {sorted(LEDGER_DISPOSITIONS)}",
                expected_id,
            )
            continue

        for field in ("rationale", "accountable_owner", "migration_plan"):
            value = entry.get(field)
            if (
                not _nonempty_text(value)
                or value == LEDGER_PLACEHOLDERS[field]
            ):
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} {field} is missing or still contains its draft placeholder",
                    expected_id,
                )

        present_now = identity in current_findings
        if disposition == "MIGRATED":
            if present_now:
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} is MIGRATED but the same finding still exists",
                    expected_id,
                )
            if not _nonempty_text(entry.get("resolution_commit")):
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} MIGRATED entry requires resolution_commit",
                    expected_id,
                )
            if not _nonempty_text(entry.get("resolution_evidence")):
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} MIGRATED entry requires resolution_evidence",
                    expected_id,
                )
        else:
            if not present_now:
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} is {disposition} but the finding has disappeared; use MIGRATED",
                    expected_id,
                )
            if entry.get("resolution_commit") is not None:
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} non-MIGRATED entry must have null resolution_commit",
                    expected_id,
                )
            if entry.get("resolution_evidence") is not None:
                error(
                    "INCOMPLETE_LEDGER_ENTRY",
                    f"{label} non-MIGRATED entry must have null resolution_evidence",
                    expected_id,
                )

    for identity in sorted(baseline_findings):
        expected_id = finding_id(identity)
        if expected_id not in seen_ids:
            error(
                "MISSING_LEDGER_ENTRY",
                "baseline finding has no ledger entry",
                expected_id,
            )
    return errors, seen


def _write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def run_legacy_governance(args: argparse.Namespace) -> int:
    cohort_path = args.legacy_cohort or (args.root / DEFAULT_COHORT)
    cohort_path = cohort_path.resolve() if not cohort_path.is_absolute() else cohort_path
    ledger_path = args.legacy_ledger or (args.root / DEFAULT_LEDGER)
    ledger_path = ledger_path.resolve() if not ledger_path.is_absolute() else ledger_path

    try:
        cohort = load_cohort(cohort_path, args.root)
        current_tree_paths = git_tree_paths(args.root, args.tree)
        current_manifest_paths = discover_manifest_paths(current_tree_paths)
        baseline_tree = cohort["baseline_tree"]
        baseline_tree_paths = git_tree_paths(args.root, baseline_tree)

        cohort_paths = cohort["manifest_paths"]
        baseline_schema = load_manifest_schema(args.root, args.tree)
        # Deliberately use the current tree's schema for both sides.
        baseline_findings = collect_findings(
            args.root, baseline_tree, cohort_paths,
            baseline_schema, baseline_tree_paths,
        )
        current_cohort_findings = collect_findings(
            args.root, args.tree, cohort_paths,
            baseline_schema, current_tree_paths,
        )
        outside_paths = sorted(set(current_manifest_paths) - set(cohort_paths))
        outside_findings = collect_findings(
            args.root, args.tree, outside_paths,
            baseline_schema, current_tree_paths,
        )
    except (
        LegacyConfigurationError, SchemaConfigurationError, GitCommandError,
        GitOutputDecodeError, OSError, ValueError,
    ) as exc:
        print(f"ERROR: legacy cohort validation could not complete: {exc}", file=sys.stderr)
        return 2

    if args.generate_ledger:
        if args.legacy_ledger:
            print(
                "ERROR: --generate-ledger cannot be combined with --legacy-ledger",
                file=sys.stderr,
            )
            return 2
        payload = generate_ledger(baseline_findings, cohort, cohort_path)
        output_path = args.generate_ledger
        if not output_path.is_absolute():
            output_path = args.root / output_path
        try:
            _write_json_atomic(output_path, payload)
        except OSError as exc:
            print(f"ERROR: cannot write generated ledger: {exc}", file=sys.stderr)
            return 2
        print(
            f"generated legacy ledger draft: entries={len(payload['entries'])} "
            f"path={output_path}"
        )
        return 0

    if args.legacy_ledger:
        ledger_path = args.legacy_ledger
    ledger = _read_json(ledger_path, "legacy disposition ledger")
    ledger_errors, ledger_entries = validate_ledger(
        ledger,
        baseline_findings,
        current_cohort_findings,
        cohort["baseline_commit"],
        cohort_path.relative_to(args.root).as_posix()
        if cohort_path.is_relative_to(args.root)
        else cohort_path.as_posix(),
    )

    baseline_keys = set(baseline_findings)
    current_keys = set(current_cohort_findings)
    regressions = current_keys - baseline_keys
    outside_keys = set(outside_findings)
    new_keys = regressions | outside_keys

    ac4_new = sum(
        1 for key in new_keys
        if (
            (current_cohort_findings.get(key) or outside_findings.get(key))["category"]
            == "AC4"
        )
    )
    other_new = len(new_keys) - ac4_new
    migrated_or_accepted = sum(
        1 for key, entry in ledger_entries.items()
        if entry.get("disposition") in {"MIGRATED", "ACCEPTED_RISK"}
    )
    disposition_pct = (
        round(100.0 * migrated_or_accepted / len(baseline_keys), 2)
        if baseline_keys else 100.0
    )

    ledger_covered = sum(
        1 for key in baseline_keys
        if key in ledger_entries
    )
    ledger_coverage_pct = (
        round(100.0 * ledger_covered / len(baseline_keys), 2)
        if baseline_keys else 100.0
    )
    no_new = not new_keys

    report = {
        "tree": args.tree,
        "baseline_commit": cohort["baseline_commit"],
        "baseline_tree": baseline_tree,
        "cohort_tree": cohort["cohort_tree"],
        "new_manifests": len(outside_paths),
        "legacy_manifests": len(cohort_paths),
        "ac4_new": ac4_new,
        "other_new": other_new,
        "legacy_baseline_findings": len(baseline_findings),
        "legacy_current_findings": len(current_cohort_findings),
        "legacy_regressions": len(regressions),
        "legacy_ledger_entries": len(ledger_entries),
        "legacy_disposition": disposition_pct,
        "legacy_ledger_coverage": ledger_coverage_pct,
        "no_new_legacy_violations": no_new,
        "ledger_errors": ledger_errors,
    }

    if args.report_output:
        report_path = args.report_output
        if not report_path.is_absolute():
            report_path = args.root / report_path
        try:
            _write_json_atomic(report_path, report)
        except OSError as exc:
            print(f"ERROR: cannot write report: {exc}", file=sys.stderr)
            return 2

    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    if ledger_errors:
        print(
            "ERROR: legacy disposition ledger validation failed: "
            f"errors={len(ledger_errors)}",
            file=sys.stderr,
        )
        return 1
    if not no_new:
        print(
            "ERROR: new Work Item manifest findings detected: "
            f"ac4_new={ac4_new} other_new={other_new}",
            file=sys.stderr,
        )
        return 1
    return 0


# ---------------------------------------------------------------------------
# Legacy CLI path. Existing --tree/--baseline/--batch-report callers retain
# their original behavior unless an explicit new legacy option is selected.
# ---------------------------------------------------------------------------

def run_legacy(args: argparse.Namespace) -> int:
    paths = sorted(args.root.glob(GLOB))
    if not paths:
        print(f"ERROR: no manifests found: {args.root / GLOB}", file=sys.stderr)
        return 2
    try:
        tree_paths = git_tree_paths(args.root, args.tree)
    except GitOutputDecodeError as exc:
        print(
            "ERROR: git output decode failed: "
            f"stream={exc.stream} encoding=utf-8 offset={exc.error.start}",
            file=sys.stderr,
        )
        return 2
    except (OSError, GitCommandError) as exc:
        print(f"ERROR: cannot enumerate git tree {args.tree}: {exc}", file=sys.stderr)
        return 2

    baseline = None
    baseline_tree = None
    baseline_paths: set[str] = set()
    baseline_errors: dict[str, set[str]] = {}
    if args.baseline:
        try:
            baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
            baseline_tree = baseline["baseline_tree"]
            baseline_paths = git_tree_paths(args.root, baseline_tree)
            manifest_paths = discover_manifest_paths(baseline_paths)
            for rel in manifest_paths:
                try:
                    baseline_errors[rel] = set(
                        validate_text(
                            git_show(args.root, baseline_tree, rel), rel, baseline_paths,
                        )
                    )
                except (OSError, GitCommandError, GitOutputDecodeError):
                    baseline_errors[rel] = {"baseline manifest could not be read"}
        except (
            OSError, UnicodeError, ValueError, KeyError,
            GitCommandError, GitOutputDecodeError,
        ) as exc:
            print(f"ERROR: cannot load baseline: {exc}", file=sys.stderr)
            return 2

    if args.batch_report:
        if baseline is None:
            print("ERROR: --batch-report requires --baseline", file=sys.stderr)
            return 2
        try:
            cohort_tree = baseline["cohort_tree"]
            cohort_paths = discover_manifest_paths(git_tree_paths(args.root, cohort_tree))
            if len(cohort_paths) != 83:
                raise ValueError(
                    f"expected 83 cohort manifests, found {len(cohort_paths)}"
                )
            print("AC4 migration batch comparison (baseline tree -> current tree):")
            for batch_no, start in enumerate((0, 21, 42, 63), start=1):
                batch_size = 21 if batch_no < 4 else 20
                batch = cohort_paths[start:start + batch_size]
                before_bad, after_bad = [], []
                for rel in batch:
                    before_errors = validate_text(
                        git_show(args.root, baseline_tree, rel), rel, baseline_paths,
                    )
                    after_errors = validate(args.root / rel, tree_paths)
                    if any(is_ac4(error) for error in before_errors):
                        before_bad.append(rel)
                    if any(is_ac4(error) for error in after_errors):
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
        except (
            KeyError, ValueError, OSError, GitCommandError, GitOutputDecodeError,
        ) as exc:
            print(f"ERROR: cannot produce batch report: {exc}", file=sys.stderr)
            return 2

    compliant, ac4, other, regressions = [], [], [], []
    for path in paths:
        rel = path.relative_to(args.root).as_posix()
        errors = validate(path, tree_paths)
        if not errors:
            compliant.append(rel)
        ac4_errors = [error for error in errors if is_ac4(error)]
        other_errors = [error for error in errors if not is_ac4(error)]
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
    print(f"Legacy ratchet new regressions: {len(regressions)}")
    for rel, error in regressions:
        print(f"  {rel}: {error}")
    if baseline_tree:
        print(f"Legacy ratchet baseline tree: {baseline_tree}")
        print("Legacy ratchet is not repository-wide conformance.")
    print("Read-only: no manifest or repository file is modified.")
    return 1 if regressions else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--tree", default="HEAD",
        help="Git tree-ish used for manifest content and path checks",
    )
    parser.add_argument("--baseline", type=Path, help="legacy compatibility baseline JSON")
    parser.add_argument("--batch-report", action="store_true")
    parser.add_argument("--all-manifests", action="store_true")
    parser.add_argument("--schema-driven", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--report", action="store_true")

    parser.add_argument("--legacy-baseline", type=Path)
    parser.add_argument("--legacy-cohort", type=Path)
    parser.add_argument("--legacy-ledger", type=Path)
    parser.add_argument("--generate-ledger", type=Path, nargs="?", const=Path(DEFAULT_LEDGER))
    parser.add_argument("--report-output", type=Path)

    args = parser.parse_args()
    new_mode = any((
        args.legacy_baseline, args.legacy_cohort, args.legacy_ledger,
        args.generate_ledger, args.report_output,
    ))
    if new_mode:
        if args.all_manifests or args.schema_driven or args.strict or args.report:
            parser.error("legacy cohort options cannot be combined with --all-manifests mode")
        if args.baseline or args.batch_report:
            parser.error("legacy cohort options cannot be combined with --baseline/--batch-report")
        if args.legacy_baseline:
            # --legacy-baseline is accepted as an explicit baseline commit/tree
            # selector; the cohort remains authoritative and must agree with it.
            cohort_path = args.legacy_cohort or (args.root / DEFAULT_COHORT)
            try:
                cohort_obj = _read_json(cohort_path, "legacy cohort")
                declared = cohort_obj.get("baseline_commit") or cohort_obj.get("baseline_tree")
                if args.legacy_baseline.as_posix() not in {
                    str(declared), str(cohort_obj.get("baseline_tree")),
                }:
                    parser.error("--legacy-baseline does not match cohort baseline")
            except LegacyConfigurationError as exc:
                parser.error(str(exc))
        return run_legacy_governance(args)

    if args.all_manifests:
        if args.baseline:
            parser.error(
                "--baseline is not accepted with --all-manifests; "
                "the full-tree result must not be suppressed by a ratchet"
            )
        if args.batch_report:
            parser.error("--batch-report is a legacy-mode option")
        return run_all_manifests(args)
    if args.schema_driven or args.strict or args.report:
        parser.error("--schema-driven, --strict, and --report require --all-manifests")
    return run_legacy(args)


if __name__ == "__main__":
    raise SystemExit(main())
