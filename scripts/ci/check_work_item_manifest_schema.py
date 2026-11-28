#!/usr/bin/env python3
"""Validate Work Item manifests using either the legacy ratchet or full schema mode."""
from __future__ import annotations

import argparse
import fnmatch
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

# These constants intentionally remain only for the legacy compatibility path.
# --all-manifests never uses them; it loads the schema from the selected Git tree.
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


def run_git_utf8(args: list[str], root: Path) -> str:
    """Run Git without relying on the platform's default text encoding.

    stdout is repository data and must be valid UTF-8. stderr is diagnostic
    text only, so replacement decoding is safe there.
    """
    result = subprocess.run(
        args,
        cwd=root,
        capture_output=True,
        text=False,
        check=False,
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
    """Return all paths in a Git tree, using NUL delimiters."""
    output = run_git_utf8(
        ["git", "ls-tree", "-r", "-z", "--name-only", tree],
        root,
    )
    return {item for item in output.split("\0") if item}


def git_show(root: Path, tree: str, path: str) -> str:
    """Read one blob from a Git tree as strict UTF-8."""
    return run_git_utf8(
        ["git", "show", f"{tree}:{path}"],
        root,
    )


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
# Legacy validation path. Its rule set and default invocation semantics are
# intentionally retained for existing CI callers.
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
            path.read_text(encoding="utf-8"),
            path.as_posix(),
            tree_paths,
        )
    except (OSError, UnicodeError) as exc:
        return [f"read error: {exc}"]


def is_ac4(error: str) -> bool:
    """Legacy classifier retained only for legacy ratchet output."""
    return "documentation" in error.lower()


# ---------------------------------------------------------------------------
# Schema-driven validation path. This path is used only with --all-manifests.
# ---------------------------------------------------------------------------

def _schema_error(message: str) -> SchemaConfigurationError:
    return SchemaConfigurationError(message)


def _require_mapping(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        raise _schema_error(f"{label} must be a mapping")
    return value


def _require_string_list(value: Any, label: str, *, nonempty: bool = True) -> list[str]:
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
    """Validate the supported schema DSL and reject unknown keywords."""
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

    required_top = _require_string_list(
        root["required_top_level_keys"],
        "required_top_level_keys",
    )

    fields = _require_mapping(root["fields"], "fields")
    unknown_fields = set(fields) - set(SCHEMA_FIELD_KEYS)
    if unknown_fields:
        raise _schema_error(
            f"unsupported schema field(s): {sorted(unknown_fields)}"
        )

    for field_name, allowed_keys in SCHEMA_FIELD_KEYS.items():
        if field_name not in fields:
            raise _schema_error(f"missing schema field definition: {field_name}")

        definition = _require_mapping(
            fields[field_name],
            f"fields.{field_name}",
        )
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
        docs.get("item_required_keys"),
        "fields.documentation.item_required_keys",
    )
    if docs.get("path_kind") != "repository-relative-path":
        raise _schema_error(
            "unsupported fields.documentation.path_kind"
        )
    if not isinstance(docs.get("path_must_exist_in_git_tree"), bool):
        raise _schema_error(
            "fields.documentation.path_must_exist_in_git_tree must be boolean"
        )
    _require_string_list(
        docs.get("relationship_enum"),
        "fields.documentation.relationship_enum",
    )

    session = fields["session_evidence"]
    if session.get("kind") != "sequence":
        raise _schema_error("fields.session_evidence.kind must be 'sequence'")
    if not isinstance(session.get("required"), bool):
        raise _schema_error("fields.session_evidence.required must be boolean")
    _require_string_list(
        session.get("item_required_keys"),
        "fields.session_evidence.item_required_keys",
    )
    pattern = session.get("session_evidence_ref_pattern")
    if not isinstance(pattern, str) or not pattern:
        raise _schema_error(
            "fields.session_evidence.session_evidence_ref_pattern "
            "must be a non-empty string"
        )
    allowlist = session.get("session_evidence_ref_exact_allowlist")
    _require_string_list(
        allowlist,
        "fields.session_evidence.session_evidence_ref_exact_allowlist",
        nonempty=False,
    )

    implementation = fields["implementation"]
    if implementation.get("kind") != "mapping":
        raise _schema_error("fields.implementation.kind must be 'mapping'")
    if not isinstance(implementation.get("required"), bool):
        raise _schema_error("fields.implementation.required must be boolean")
    _require_string_list(
        implementation.get("required_keys"),
        "fields.implementation.required_keys",
    )
    _require_string_list(
        implementation.get("status_enum"),
        "fields.implementation.status_enum",
    )
    for key in ("files_changed_kind", "tests_kind"):
        if implementation.get(key) != "sequence":
            raise _schema_error(
                f"fields.implementation.{key} must be 'sequence'"
            )

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


def validate_against_schema(
    data: Any,
    manifest_path: str,
    schema: dict,
    tree_paths: set[str],
) -> list[dict[str, str]]:
    """Validate one parsed manifest against the loaded schema definition."""
    findings: list[dict[str, str]] = []

    def add(rule_id: str, category: str, pointer: str, message: str) -> None:
        findings.append(
            _finding(manifest_path, rule_id, category, pointer, message)
        )

    if not isinstance(data, dict):
        add(
            "manifest.root.mapping",
            "OTHER_SCHEMA",
            "",
            "document root must be a mapping",
        )
        return findings

    for key in schema["required_top_level_keys"]:
        if key not in data:
            add(
                f"top_level.{key}.required",
                "OTHER_SCHEMA",
                _pointer(key),
                f"missing required top-level key: {key}",
            )

    fields = schema["fields"]

    # documentation
    docs_rule = fields["documentation"]
    docs_present = "documentation" in data
    if docs_rule["required"] and not docs_present:
        add(
            "documentation.required",
            "AC4",
            "/documentation",
            "documentation is required",
        )
    elif docs_present:
        docs = data["documentation"]
        if not isinstance(docs, list):
            add(
                "documentation.kind.sequence",
                "AC4",
                "/documentation",
                "documentation must be a sequence",
            )
        else:
            minimum = docs_rule["min_items"]
            if len(docs) < minimum:
                add(
                    "documentation.min_items",
                    "AC4",
                    "/documentation",
                    f"documentation must contain at least {minimum} reference(s)",
                )

            required_keys = docs_rule["item_required_keys"]
            relationships = set(docs_rule["relationship_enum"])

            for index, item in enumerate(docs):
                base = _pointer("documentation", index)
                if not isinstance(item, dict):
                    add(
                        "documentation.item.mapping",
                        "AC4",
                        base,
                        f"documentation[{index}] must be a mapping",
                    )
                    continue

                for key in required_keys:
                    if key not in item:
                        add(
                            "documentation.item.required_key",
                            "AC4",
                            _pointer("documentation", index, key),
                            f"documentation[{index}] missing {key}",
                        )

                relationship = item.get("relationship")
                if relationship not in relationships:
                    add(
                        "documentation.relationship.enum",
                        "AC4",
                        _pointer("documentation", index, "relationship"),
                        "documentation relationship must be one of "
                        f"{sorted(relationships)}",
                    )

                if "path" in item:
                    ref = item.get("path")
                    if not isinstance(ref, str) or not ref:
                        add(
                            "documentation.path.nonempty",
                            "AC4",
                            _pointer("documentation", index, "path"),
                            "documentation path must be a non-empty string",
                        )
                    else:
                        parsed = PurePosixPath(ref)
                        if (
                            parsed.is_absolute()
                            or ".." in parsed.parts
                            or "\\" in ref
                            or ref.startswith("/")
                        ):
                            add(
                                "documentation.path.repository_relative",
                                "AC4",
                                _pointer("documentation", index, "path"),
                                f"documentation path is not repository-relative: {ref}",
                            )
                        elif (
                            docs_rule["path_must_exist_in_git_tree"]
                            and ref not in tree_paths
                        ):
                            add(
                                "documentation.path.exists_in_git_tree",
                                "AC4",
                                _pointer("documentation", index, "path"),
                                f"documentation path not in git tree: {ref}",
                            )

    # session_evidence
    session_rule = fields["session_evidence"]
    session_present = "session_evidence" in data
    if session_rule["required"] and not session_present:
        add(
            "session_evidence.required",
            "OTHER_SCHEMA",
            "/session_evidence",
            "session_evidence is required",
        )
    elif session_present:
        records = data["session_evidence"]
        if not isinstance(records, list) or not records:
            add(
                "session_evidence.kind.nonempty_sequence",
                "OTHER_SCHEMA",
                "/session_evidence",
                "session_evidence must be a non-empty sequence",
            )
        else:
            required_keys = session_rule["item_required_keys"]
            pattern = session_rule["session_evidence_ref_pattern"]
            allowlist = set(
                session_rule["session_evidence_ref_exact_allowlist"]
            )

            for index, item in enumerate(records):
                base = _pointer("session_evidence", index)
                if not isinstance(item, dict):
                    add(
                        "session_evidence.item.mapping",
                        "OTHER_SCHEMA",
                        base,
                        f"session_evidence[{index}] must be a mapping",
                    )
                    continue

                for key in required_keys:
                    if key not in item:
                        add(
                            "session_evidence.item.required_key",
                            "OTHER_SCHEMA",
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
                            "session_evidence.ref.pattern",
                            "OTHER_SCHEMA",
                            _pointer(
                                "session_evidence", index,
                                "session_evidence_ref",
                            ),
                            "session_evidence_ref must match "
                            f"{pattern!r} or the exact allowlist",
                        )

    # implementation
    implementation_rule = fields["implementation"]
    implementation_present = "implementation" in data
    if implementation_rule["required"] and not implementation_present:
        add(
            "implementation.required",
            "OTHER_SCHEMA",
            "/implementation",
            "implementation is required",
        )
    elif implementation_present:
        implementation = data["implementation"]
        if not isinstance(implementation, dict):
            add(
                "implementation.kind.mapping",
                "OTHER_SCHEMA",
                "/implementation",
                "implementation must be a mapping",
            )
        else:
            for key in implementation_rule["required_keys"]:
                if key not in implementation:
                    add(
                        "implementation.required_key",
                        "OTHER_SCHEMA",
                        _pointer("implementation", key),
                        f"implementation missing {key}",
                    )

            if (
                "status" in implementation
                and implementation.get("status")
                not in set(implementation_rule["status_enum"])
            ):
                add(
                    "implementation.status.enum",
                    "OTHER_SCHEMA",
                    "/implementation/status",
                    "implementation.status must be one of "
                    f"{sorted(implementation_rule['status_enum'])}",
                )

            for key, expected_kind in (
                ("files_changed", implementation_rule["files_changed_kind"]),
                ("tests", implementation_rule["tests_kind"]),
            ):
                if key in implementation:
                    if expected_kind == "sequence" and not isinstance(
                        implementation[key], list
                    ):
                        add(
                            f"implementation.{key}.kind.sequence",
                            "OTHER_SCHEMA",
                            _pointer("implementation", key),
                            f"implementation.{key} must be a sequence",
                        )

    return findings


def _json_report(
    tree: str,
    discovered_paths: list[str],
    manifest_results: list[dict],
    schema_source: str,
) -> dict:
    all_findings = [
        finding
        for result in manifest_results
        for finding in result.get("findings", [])
    ]
    ac4_findings = [
        finding for finding in all_findings
        if finding["category"] == "AC4"
    ]
    other_findings = [
        finding for finding in all_findings
        if finding["category"] == "OTHER_SCHEMA"
    ]

    parse_errors = sum(
        1 for result in manifest_results
        if result["status"] == "PARSE_ERROR"
    )
    decode_errors = sum(
        1 for result in manifest_results
        if result["status"] == "DECODE_ERROR"
    )
    read_errors = sum(
        1 for result in manifest_results
        if result["status"] == "READ_ERROR"
    )
    incomplete = sum(
        1 for result in manifest_results
        if result["status"] in {
            "PARSE_ERROR", "DECODE_ERROR", "READ_ERROR",
        }
    )
    validated = sum(
        1 for result in manifest_results
        if result["status"] in {"PASS", "VIOLATION"}
    )

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
        "ac4_manifests": len({
            finding["manifest_path"] for finding in ac4_findings
        }),
        "other_schema_violations": len(other_findings),
        "other_schema_manifests": len({
            finding["manifest_path"] for finding in other_findings
        }),
        # There is no second hard-coded checker in this mode. The schema is
        # the single rule source, so cross-check divergence is not applicable.
        "schema_checker_divergences": 0,
        "manifests": manifest_results,
    }


def run_all_manifests(args: argparse.Namespace) -> int:
    try:
        tree_paths = git_tree_paths(args.root, args.tree)
        manifest_paths = discover_manifest_paths(tree_paths)
        if not manifest_paths:
            raise GitCommandError(
                ["git", "ls-tree", "-r", args.tree],
                1,
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
                "path": rel,
                "status": "DECODE_ERROR",
                "findings": [],
                "error": (
                    "git output decode failed: stream=stdout "
                    f"encoding=utf-8 offset={exc.error.start}"
                ),
            })
            continue
        except GitCommandError as exc:
            results.append({
                "path": rel,
                "status": "READ_ERROR",
                "findings": [],
                "error": str(exc),
            })
            continue
        except OSError as exc:
            results.append({
                "path": rel,
                "status": "READ_ERROR",
                "findings": [],
                "error": str(exc),
            })
            continue

        try:
            data = _parse_yaml(content, rel)
        except ValueError as exc:
            results.append({
                "path": rel,
                "status": "PARSE_ERROR",
                "findings": [],
                "error": str(exc),
            })
            continue

        findings = validate_against_schema(
            data,
            rel,
            schema,
            tree_paths,
        )
        results.append({
            "path": rel,
            "status": "VIOLATION" if findings else "PASS",
            "findings": findings,
        })

    report = _json_report(
        args.tree,
        manifest_paths,
        results,
        SCHEMA_PATH,
    )

    if args.report:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"tree={report['tree']}")
        print(f"schema_source={report['schema_source']}")
        print(f"population={report['population']}")
        print(f"discovered={report['discovered']}")
        print(f"validated={report['validated']}")
        print(f"incomplete={report['incomplete']}")
        print(f"ac4_violations={report['ac4_violations']}")
        print(f"other_schema_violations={report['other_schema_violations']}")

        for result in results:
            if result["status"] == "PASS":
                continue
            print(
                f"{result['status']}: {result['path']}",
                file=sys.stderr,
            )
            if "error" in result:
                print(f"  {result['error']}", file=sys.stderr)
            for finding in result["findings"]:
                print(
                    f"  {finding['rule_id']} "
                    f"{finding['pointer']}: {finding['message']}",
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
            report["ac4_violations"]
            or report["other_schema_violations"]
        ) else 2

    has_violations = bool(
        report["ac4_violations"]
        or report["other_schema_violations"]
    )
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
# Legacy CLI path. Existing --tree/--baseline and --batch-report callers use
# this path unless --all-manifests is explicitly supplied.
# ---------------------------------------------------------------------------

def run_legacy(args: argparse.Namespace) -> int:
    paths = sorted(args.root.glob(GLOB))
    if not paths:
        print(
            f"ERROR: no manifests found: {args.root / GLOB}",
            file=sys.stderr,
        )
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
                            git_show(args.root, baseline_tree, rel),
                            rel,
                            baseline_paths,
                        )
                    )
                except (OSError, GitCommandError, GitOutputDecodeError):
                    baseline_errors[rel] = {
                        "baseline manifest could not be read"
                    }
        except (
            OSError, UnicodeError, ValueError, KeyError,
            GitCommandError, GitOutputDecodeError,
        ) as exc:
            print(f"ERROR: cannot load baseline: {exc}", file=sys.stderr)
            return 2

    if args.batch_report:
        if baseline is None:
            print(
                "ERROR: --batch-report requires --baseline",
                file=sys.stderr,
            )
            return 2
        try:
            cohort_tree = baseline["cohort_tree"]
            cohort_paths = discover_manifest_paths(
                git_tree_paths(args.root, cohort_tree)
            )
            if len(cohort_paths) != 83:
                raise ValueError(
                    f"expected 83 cohort manifests, found {len(cohort_paths)}"
                )

            print(
                "AC4 migration batch comparison "
                "(baseline tree -> current tree):"
            )
            for batch_no, start in enumerate((0, 21, 42, 63), start=1):
                batch_size = 21 if batch_no < 4 else 20
                batch = cohort_paths[start:start + batch_size]
                before_bad, after_bad = [], []

                for rel in batch:
                    before_errors = validate_text(
                        git_show(args.root, baseline_tree, rel),
                        rel,
                        baseline_paths,
                    )
                    current_file = args.root / rel
                    after_errors = validate(current_file, tree_paths)

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
                    print(
                        f"    BEFORE {rel}: "
                        "missing/invalid documentation reference"
                    )
                for rel in after_bad:
                    print(
                        f"    AFTER  {rel}: "
                        "AC4 documentation violation remains"
                    )
        except (
            KeyError, ValueError, OSError, GitCommandError,
            GitOutputDecodeError,
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

    print(
        f"Manifest schema v2: total={len(paths)} "
        f"compliant={len(compliant)}"
    )
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
        "--tree",
        default="HEAD",
        help="Git tree-ish used for manifest content and path checks",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="JSON file pinning a legacy baseline tree",
    )
    parser.add_argument(
        "--batch-report",
        action="store_true",
        help="print before/after AC4 counts for the pinned 83-manifest cohort",
    )

    parser.add_argument(
        "--all-manifests",
        action="store_true",
        help="validate every manifest discovered in the selected Git tree",
    )
    parser.add_argument(
        "--schema-driven",
        action="store_true",
        help="explicitly select the schema-defined validation contract",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return nonzero when full-tree validation finds violations",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="emit a machine-readable JSON report in full-tree mode",
    )

    args = parser.parse_args()

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
        parser.error(
            "--schema-driven, --strict, and --report require --all-manifests"
        )

    return run_legacy(args)


if __name__ == "__main__":
    raise SystemExit(main())
