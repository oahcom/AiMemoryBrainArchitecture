#!/usr/bin/env python3
"""Stage-2, guarded application of source-backed manifest proposals."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required", file=sys.stderr)
    raise SystemExit(2)


class ProposalError(Exception):
    """A proposal failed validation; no writes should be committed."""


class RollbackError(ProposalError):
    """A write failed and one or more original files could not be restored."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_yaml_bytes(value: bytes, label: str) -> dict:
    try:
        parsed = yaml.safe_load(value.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ProposalError(f"{label}: invalid YAML: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ProposalError(f"{label}: YAML root must be a mapping")
    return parsed


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProposalError(f"cannot read proposals JSON {path}: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("manifests"), list):
        raise ProposalError("proposals JSON must contain a manifests array")
    return value


def load_schema(path: Path) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ProposalError(f"cannot read schema {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProposalError("schema root must be a mapping")
    return value


def safe_manifest_path(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ProposalError(f"unsafe manifest path: {relative!r}")

    root_resolved = root.resolve()
    path = root / candidate

    # Reject symlinks in every existing path component.
    current = root
    for part in candidate.parts:
        current = current / part
        if current.is_symlink():
            raise ProposalError(f"symlink path is not allowed: {relative}")

    resolved = path.resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise ProposalError(f"manifest escapes repository root: {relative}")

    if not path.is_file():
        raise ProposalError(f"manifest is not a regular file: {relative}")
    return path


def pointer_parts(pointer: str) -> list[str]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ProposalError(f"invalid JSON Pointer: {pointer!r}")
    return [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer[1:].split("/")
    ]


def get_pointer(document: Any, pointer: str) -> Any:
    current = document
    for part in pointer_parts(pointer):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if index < len(current) else None
        else:
            return None
    return current


def remove_pointer(document: dict, pointer: str) -> None:
    parts = pointer_parts(pointer)
    if len(parts) == 1:
        document.pop(parts[0], None)
        return

    if len(parts) == 2 and parts[0] == "implementation":
        implementation = document.get("implementation")
        if isinstance(implementation, dict):
            implementation.pop(parts[1], None)
            if not implementation:
                document.pop("implementation", None)
        return

    raise ProposalError(f"unsupported semantic-exclusion pointer: {pointer}")


def semantic_projection(document: dict, pointers: set[str]) -> dict:
    result = copy.deepcopy(document)
    for pointer in sorted(pointers):
        remove_pointer(result, pointer)
    return result


def schema_enum(schema: dict, group: str, key: str) -> list:
    try:
        values = schema["fields"][group][key]
    except (KeyError, TypeError):
        raise ProposalError(
            f"schema is missing fields.{group}.{key}"
        )
    if not isinstance(values, list) or not values:
        raise ProposalError(
            f"schema fields.{group}.{key} must be a non-empty list"
        )
    return values


def validate_documentation_value(value: Any, root: Path, schema: dict) -> None:
    if not isinstance(value, list) or not value:
        raise ProposalError("documentation proposal must be a non-empty list")

    allowed = schema_enum(schema, "documentation", "relationship_enum")
    seen_paths: set[str] = set()

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ProposalError(f"documentation[{index}] must be a mapping")
        if set(item) != {"path", "relationship"}:
            raise ProposalError(
                f"documentation[{index}] must contain only path and relationship"
            )

        relative = item["path"]
        relationship = item["relationship"]
        if not isinstance(relative, str) or not relative:
            raise ProposalError(f"documentation[{index}].path must be non-empty")
        if relationship not in allowed:
            raise ProposalError(
                f"documentation[{index}].relationship {relationship!r} "
                f"is outside schema enum {allowed!r}"
            )

        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ProposalError(f"unsafe documentation path: {relative!r}")
        if candidate.name.upper() == "INDEX.MD":
            raise ProposalError("INDEX.md is an index, not documentation evidence")

        current = root
        for part in candidate.parts:
            current = current / part
            if current.is_symlink():
                raise ProposalError(f"documentation path is a symlink: {relative}")

        resolved_root = root.resolve()
        resolved = (root / candidate).resolve()
        if resolved_root not in resolved.parents:
            raise ProposalError(f"documentation path escapes root: {relative}")
        if not resolved.is_file():
            raise ProposalError(
                f"documentation source does not exist as a file: {relative}"
            )
        if relative in seen_paths:
            raise ProposalError(f"duplicate documentation path: {relative}")
        seen_paths.add(relative)


def validate_source(
    finding: dict,
    source: Any,
    value: Any,
    document: dict,
    root: Path,
) -> None:
    if not isinstance(source, dict):
        raise ProposalError("PROPOSED finding has no source mapping")

    rule = finding.get("rule")
    pointer = finding.get("pointer")
    source_type = source.get("type")

    if rule in {
        "top_level.documentation.required",
        "documentation.required",
    }:
        if pointer != "/documentation":
            raise ProposalError("documentation proposal has unexpected pointer")
        if source_type != "existing_work_item_markdown":
            raise ProposalError("documentation proposal has unsupported source type")
        if source.get("files") != value:
            raise ProposalError("documentation source.files differs from proposed value")
        return

    if rule == "implementation.required_key":
        parts = pointer_parts(pointer)
        if len(parts) != 2 or parts[0] != "implementation":
            raise ProposalError("implementation proposal has unexpected pointer")

        field = parts[1]
        if field not in {"summary", "files_changed", "tests"}:
            raise ProposalError(f"unsupported implementation field: {field}")

        if field == "summary":
            if (
                source_type != "existing_manifest_field"
                or source.get("path") != "scope.objective"
            ):
                raise ProposalError("summary must cite scope.objective")
            scope = document.get("scope")
            objective = scope.get("objective") if isinstance(scope, dict) else None
            if not isinstance(objective, str) or objective.strip() != value:
                raise ProposalError("summary does not match current scope.objective")
            return

        if field == "tests":
            scope = document.get("scope")
            scope_tests = scope.get("tests") if isinstance(scope, dict) else None
            implementation = document.get("implementation")
            impl_tests = (
                implementation.get("tests")
                if isinstance(implementation, dict)
                else None
            )

            if source_type == "existing_manifest_field" and source.get("path") == "scope.tests":
                if not isinstance(scope_tests, list) or scope_tests != value:
                    raise ProposalError("tests do not match current scope.tests")
                return
            if source_type == "existing_manifest_field" and source.get("path") == "implementation.tests":
                if not isinstance(impl_tests, list) or impl_tests != value:
                    raise ProposalError("tests do not match current implementation.tests")
                return
            raise ProposalError("tests proposal has unsupported source")

        if field == "files_changed":
            if source_type == "existing_manifest_field" and source.get("path") == "implementation.files_changed":
                implementation = document.get("implementation")
                current = (
                    implementation.get("files_changed")
                    if isinstance(implementation, dict)
                    else None
                )
                if current != value:
                    raise ProposalError(
                        "files_changed does not match current implementation.files_changed"
                    )
                return

            if source_type == "existing_manifest_scope":
                paths = source.get("paths")
                if paths != value or not isinstance(paths, list) or not paths:
                    raise ProposalError("files_changed scope source does not match value")

                scope = document.get("scope")
                if not isinstance(scope, dict):
                    raise ProposalError("files_changed scope source is missing")
                declared = []
                for key in ("files_to_create", "files_to_modify"):
                    items = scope.get(key)
                    if isinstance(items, list):
                        declared.extend(
                            item.strip()
                            for item in items
                            if isinstance(item, str) and item.strip()
                        )
                if paths != list(dict.fromkeys(declared)):
                    raise ProposalError(
                        "files_changed differs from explicit scope file declarations"
                    )
                for relative in paths:
                    candidate = Path(relative)
                    if candidate.is_absolute() or ".." in candidate.parts:
                        raise ProposalError(f"unsafe files_changed path: {relative!r}")
                return

            raise ProposalError("files_changed proposal has unsupported source")

    if rule == "implementation.status.enum":
        if pointer != "/implementation/status":
            raise ProposalError(
                "implementation status proposal has unexpected pointer"
            )

        if source_type != "existing_manifest_value":
            raise ProposalError(
                "implementation status proposal has unsupported source type"
            )

        if (
            source.get("pointer") != "/implementation/status"
            or source.get("value") != "MERGED"
        ):
            raise ProposalError(
                "implementation status source must record the original MERGED value"
            )

        implementation = document.get("implementation")
        current = (
            implementation.get("status")
            if isinstance(implementation, dict)
            else None
        )
        if current != "MERGED":
            raise ProposalError(
                "implementation status source no longer matches current MERGED value"
            )
        if value != "IMPLEMENTED":
            raise ProposalError(
                "MERGED implementation status may only be mapped to IMPLEMENTED"
            )
        return

    raise ProposalError(f"no Stage-2 source validator for rule {rule!r}")


def validate_operation(
    entry: dict,
    document: dict,
    root: Path,
    schema: dict,
) -> tuple[str, Any]:
    finding = entry.get("finding")
    operation = entry.get("operation")
    value = entry.get("proposed_value")

    if not isinstance(finding, dict) or not isinstance(operation, dict):
        raise ProposalError("PROPOSED finding must contain finding and operation")
    if value is None:
        raise ProposalError("PROPOSED finding has null proposed_value")
    if operation.get("value") != value:
        raise ProposalError("operation.value differs from proposed_value")

    rule = finding.get("rule")
    pointer = finding.get("pointer")

    if operation.get("type") == "replace_top_level_key":
        if (
            rule not in {
                "top_level.documentation.required",
                "documentation.required",
            }
            or pointer != "/documentation"
            or operation.get("key") != "documentation"
        ):
            raise ProposalError("unauthorized replace_top_level_key operation")
        validate_documentation_value(value, root, schema)
        validate_source(finding, entry.get("source"), value, document, root)
        return pointer, value

    if operation.get("type") == "set_nested_key":
        parts = operation.get("path")

        # Narrow exception: the exact MERGED -> IMPLEMENTED status mapping.
        if (
            rule == "implementation.status.enum"
            and pointer == "/implementation/status"
            and parts == ["implementation", "status"]
        ):
            if value != "IMPLEMENTED" or operation.get("value") != "IMPLEMENTED":
                raise ProposalError("unauthorized set_nested_key operation")

            allowed = schema_enum(schema, "implementation", "status_enum")
            if "IMPLEMENTED" not in allowed:
                raise ProposalError(
                    "IMPLEMENTED is not allowed by implementation.status schema enum"
                )

            validate_source(
                finding,
                entry.get("source"),
                value,
                document,
                root,
            )
            return pointer, value

        # Existing allowlist for ordinary implementation.required_key proposals.
        if (
            rule != "implementation.required_key"
            or not isinstance(parts, list)
            or len(parts) != 2
            or parts[0] != "implementation"
            or parts[1] not in {"summary", "files_changed", "tests"}
            or pointer != f"/implementation/{parts[1]}"
        ):
            raise ProposalError("unauthorized set_nested_key operation")

        validate_source(finding, entry.get("source"), value, document, root)
        return pointer, value

    raise ProposalError(f"unsupported operation type: {operation.get('type')!r}")


def apply_value(document: dict, pointer: str, value: Any) -> None:
    parts = pointer_parts(pointer)
    if len(parts) == 1:
        document[parts[0]] = copy.deepcopy(value)
        return

    if len(parts) == 2 and parts[0] == "implementation":
        implementation = document.get("implementation")
        if not isinstance(implementation, dict):
            implementation = {}
            document["implementation"] = implementation
        implementation[parts[1]] = copy.deepcopy(value)
        return

    raise ProposalError(f"unsupported write pointer: {pointer}")


def render_yaml(document: dict) -> bytes:
    text = yaml.safe_dump(
        document,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=100,
    )
    return text.encode("utf-8")


def write_file(path: Path, content: bytes) -> None:
    path.write_bytes(content)


def restore_file(path: Path, content: bytes) -> None:
    path.write_bytes(content)


def prepare_manifest(
    root: Path,
    item: dict,
    schema: dict,
) -> dict:
    relative = item.get("manifest")
    if not isinstance(relative, str):
        raise ProposalError("manifest entry has no manifest path")

    path = safe_manifest_path(root, relative)
    original_bytes = path.read_bytes()
    before_hash = sha256_bytes(original_bytes)

    if before_hash != item.get("before_sha256"):
        raise ProposalError(
            f"before_sha256 mismatch for {relative}: "
            f"expected {item.get('before_sha256')}, actual {before_hash}"
        )

    original = load_yaml_bytes(original_bytes, relative)
    proposed = copy.deepcopy(original)
    authorized: dict[str, Any] = {}
    proposed_count = 0
    blocked_count = 0

    entries = item.get("findings")
    if not isinstance(entries, list):
        raise ProposalError(f"{relative}: findings must be a list")

    # Pass 1: validate proposal envelope and detect conflicting values
    # before performing source-specific validation.
    proposed_entries = []

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ProposalError(
                f"{relative}: findings[{index}] must be a mapping"
            )

        status = entry.get("status")
        finding = entry.get("finding")
        if not isinstance(finding, dict):
            raise ProposalError(
                f"{relative}: findings[{index}] has no finding mapping"
            )
        if finding.get("manifest") != relative:
            raise ProposalError(
                f"{relative}: findings[{index}] refers to a different manifest"
            )

        if status == "BLOCKED":
            blocked_count += 1
            continue

        if status != "PROPOSED":
            raise ProposalError(
                f"{relative}: findings[{index}] has unknown status {status!r}"
            )

        pointer = finding.get("pointer")
        value = entry.get("proposed_value")

        if not isinstance(pointer, str) or value is None:
            raise ProposalError(
                f"{relative}: findings[{index}] has invalid PROPOSED pointer/value"
            )

        if pointer in authorized and authorized[pointer] != value:
            raise ProposalError(
                f"{relative}: conflicting PROPOSED values for {pointer}"
            )

        authorized[pointer] = copy.deepcopy(value)
        proposed_entries.append((index, entry))
        proposed_count += 1

    # Pass 2: validate operation shape, source provenance, and schema rules.
    for index, entry in proposed_entries:
        pointer, value = validate_operation(entry, original, root, schema)

        if pointer not in authorized or authorized[pointer] != value:
            raise ProposalError(
                f"{relative}: validated operation differs from its preflight value "
                f"at {pointer}"
            )

    for pointer, value in authorized.items():
        apply_value(proposed, pointer, value)

    after_bytes = render_yaml(proposed)
    parsed_after = load_yaml_bytes(after_bytes, f"proposed {relative}")

    if semantic_projection(original, set(authorized)) != semantic_projection(
        parsed_after, set(authorized)
    ):
        raise ProposalError(
            f"{relative}: YAML round-trip changed an unauthorized semantic field"
        )

    for pointer, expected in authorized.items():
        actual = get_pointer(parsed_after, pointer)
        if actual != expected:
            raise ProposalError(
                f"{relative}: post-serialization pointer mismatch at {pointer}"
            )

    after_hash = sha256_bytes(after_bytes)
    if item.get("proposed_sha256") != after_hash:
        raise ProposalError(
            f"{relative}: proposed_sha256 mismatch: "
            f"proposal={item.get('proposed_sha256')}, recomputed={after_hash}"
        )

    return {
        "manifest": relative,
        "path": path,
        "before_bytes": original_bytes,
        "after_bytes": after_bytes,
        "before_sha256": before_hash,
        "after_sha256": after_hash,
        "authorized_pointers": sorted(authorized),
        "proposed_findings": proposed_count,
        "blocked_findings": blocked_count,
        "changed": bool(authorized),
    }


def prepare_batch(root: Path, proposals: dict, schema: dict) -> list[dict]:
    items = proposals.get("manifests")
    if not isinstance(items, list):
        raise ProposalError("proposals.manifests must be a list")

    prepared = []
    seen_paths = set()
    for item in items:
        if not isinstance(item, dict):
            raise ProposalError("each manifest proposal must be a mapping")
        relative = item.get("manifest")
        if relative in seen_paths:
            raise ProposalError(f"duplicate manifest proposal: {relative}")
        seen_paths.add(relative)
        prepared.append(prepare_manifest(root, item, schema))

    return prepared


def commit_batch(prepared: list[dict]) -> None:
    written: list[dict] = []

    try:
        # Recheck every source hash immediately before the first write.
        for item in prepared:
            current = item["path"].read_bytes()
            actual = sha256_bytes(current)
            if actual != item["before_sha256"]:
                raise ProposalError(
                    f"before_sha256 changed before commit for {item['manifest']}: "
                    f"expected {item['before_sha256']}, actual {actual}"
                )

        for item in prepared:
            if not item["changed"]:
                continue
            write_file(item["path"], item["after_bytes"])
            written.append(item)

        # Verify written files against their prepared output.
        # Verify untouched files remain byte-for-byte unchanged.
        written_paths = {item["path"] for item in written}

        for item in prepared:
            current = item["path"].read_bytes()
            actual_hash = sha256_bytes(current)

            if item["path"] in written_paths:
                if actual_hash != item["after_sha256"]:
                    raise ProposalError(
                        f"post-write SHA-256 mismatch for {item['manifest']}"
                    )

                parsed = load_yaml_bytes(current, item["manifest"])
                # Re-parse the candidate and verify the committed semantic content.
                expected = load_yaml_bytes(item["after_bytes"], item["manifest"])
                for pointer in item["authorized_pointers"]:
                    if get_pointer(parsed, pointer) != get_pointer(expected, pointer):
                        raise ProposalError(
                            f"post-write pointer verification failed: "
                            f"{item['manifest']} {pointer}"
                        )
            else:
                if actual_hash != item["before_sha256"]:
                    raise ProposalError(
                        f"untouched file SHA-256 mismatch for {item['manifest']}"
                    )

    except Exception as original_error:
        rollback_errors = []
        for item in reversed(written):
            try:
                restore_file(item["path"], item["before_bytes"])
                restored = item["path"].read_bytes()
                if restored != item["before_bytes"]:
                    raise OSError("restored bytes do not match original bytes")
            except Exception as rollback_error:
                rollback_errors.append(
                    f"{item['manifest']}: {rollback_error}"
                )

        if rollback_errors:
            raise RollbackError(
                f"batch failed: {original_error}; rollback failures: "
                + "; ".join(rollback_errors)
            ) from original_error
        raise ProposalError(
            f"batch failed; all written files restored: {original_error}"
        ) from original_error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--proposals", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply validated proposals. Without this flag, perform dry-run only.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    proposals = load_json(args.proposals)
    schema = load_schema(args.schema)

    prepared = prepare_batch(root, proposals, schema)
    total_proposed = sum(item["proposed_findings"] for item in prepared)
    total_blocked = sum(item["blocked_findings"] for item in prepared)
    changed = sum(item["changed"] for item in prepared)

    if args.apply:
        commit_batch(prepared)
        mode = "APPLIED"
    else:
        mode = "DRY_RUN"

    print(
        f"STAGE2: mode={mode} manifests={len(prepared)} "
        f"proposed_findings={total_proposed} blocked={total_blocked} "
        f"files_to_change={changed} files_written={changed if args.apply else 0}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RollbackError as exc:
        print(f"ROLLBACK_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(3)
    except (ProposalError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
