"""Validate work-item registry records from an immutable Git tree.

Exit codes:
    0 PASS
    1 VIOLATION
    2 INCOMPLETE
    3 VIOLATION_AND_INCOMPLETE
    4 CONFIGURATION_ERROR
    5 NOT_APPLICABLE (diagnostic mode only)

Dependencies: Python 3.12/3.13 standard library, PyYAML, jsonschema.
The validator reads Git tree entries and blobs only. It never reads registry
YAML, manifests, or INDEX content from the working tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator, ValidationError
from jsonschema.exceptions import SchemaError


SCHEMA_PATH = "00-governance/schemas/work-item-registry.schema.json"
REGISTRY_PREFIX = "00-governance/registry/"
MANIFEST_PREFIX = "14-ai-development/work-items/"
INVENTORY_PATH = "00-governance/registry-migration/inventory.yaml"

WORK_ITEM_ID_RE = re.compile(r"^AID-[0-9]{4}-[0-9]{3}$")
FIX_ID_RE = re.compile(r"^FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
GIT_SHA_RE = re.compile(r"^[a-fA-F0-9]{40}$")

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_INCOMPLETE = 2
EXIT_BOTH = 3
EXIT_CONFIG = 4
EXIT_NA = 5

CHECKS = (
    "registry.scan",
    "registry.path_identity",
    "registry.unique_ids",
    "registry.schema",
    "registry.prompt_pin",
    "registry.inventory",
    "registry.index_projection",
)

SUMMARY_KEYS = (
    "type",
    "tree",
    "schema_version",
    "registry_files",
    "parsed",
    "schema_valid",
    "duplicate_ids",
    "prompt_pins_checked",
    "prompt_pins_failed",
    "incomplete_checks",
    "violations",
    "incomplete",
    "overall",
    "exit_code",
)


class ConfigurationError(Exception):
    """Invalid arguments or unavailable/invalid schema configuration."""


class GitReadError(Exception):
    """A required Git tree or blob could not be read."""


class StrictYAMLLoader(yaml.SafeLoader):
    """Safe YAML loader which rejects duplicate mapping keys."""


def _construct_mapping(loader: StrictYAMLLoader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key {key!r}",
                key_node.start_mark,
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictYAMLLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


@dataclass(frozen=True)
class TreeBlob:
    path: str
    oid: str
    data: bytes


@dataclass
class Event:
    check: str
    status: str
    code: str
    tree: str
    fields: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "type": "check",
            "check": self.check,
            "status": self.status,
            "code": self.code,
            **self.fields,
            "tree": self.tree,
        }


@dataclass
class RunResult:
    tree: str
    events: list[Event] = field(default_factory=list)
    registry_files: int = 0
    parsed: int = 0
    schema_valid: int = 0
    duplicate_ids: int = 0
    prompt_pins_checked: int = 0
    prompt_pins_failed: int = 0

    @property
    def violations(self) -> int:
        return sum(event.status == "VIOLATION" for event in self.events)

    @property
    def incomplete(self) -> int:
        return sum(event.status == "INCOMPLETE" for event in self.events)

    @property
    def incomplete_checks(self) -> int:
        return sum(
            event.status == "INCOMPLETE"
            for event in self.events
        )

    @property
    def overall(self) -> str:
        if self.violations and self.incomplete:
            return "VIOLATION_AND_INCOMPLETE"
        if self.violations:
            return "VIOLATION"
        if self.incomplete:
            return "INCOMPLETE"
        return "PASS"

    @property
    def exit_code(self) -> int:
        return {
            "PASS": EXIT_PASS,
            "VIOLATION": EXIT_VIOLATION,
            "INCOMPLETE": EXIT_INCOMPLETE,
            "VIOLATION_AND_INCOMPLETE": EXIT_BOTH,
        }[self.overall]

    def summary(self) -> dict[str, Any]:
        values = {
            "type": "summary",
            "tree": self.tree,
            "schema_version": 1,
            "registry_files": self.registry_files,
            "parsed": self.parsed,
            "schema_valid": self.schema_valid,
            "duplicate_ids": self.duplicate_ids,
            "prompt_pins_checked": self.prompt_pins_checked,
            "prompt_pins_failed": self.prompt_pins_failed,
            "incomplete_checks": self.incomplete_checks,
            "violations": self.violations,
            "incomplete": self.incomplete,
            "overall": self.overall,
            "exit_code": self.exit_code,
        }
        assert tuple(values) == SUMMARY_KEYS
        return values


class GitTree:
    """Read-only access to one immutable Git tree."""

    def __init__(self, root: str, revision: str):
        self.root = root
        self.revision = revision
        self.tree_oid = self._resolve_tree(revision)
        self.entries = self._list_tree(self.tree_oid)
        self._blob_cache: dict[str, bytes] = {}

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", self.root, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def _resolve_tree(self, revision: str) -> str:
        result = self._git("rev-parse", "--verify", f"{revision}^{{tree}}")
        if result.returncode:
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise ConfigurationError(
                f"cannot resolve Git tree {revision!r}: {detail}"
            )
        value = result.stdout.decode("ascii", errors="strict").strip()
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", value):
            raise ConfigurationError(f"invalid resolved tree object ID: {value!r}")
        return value.lower()

    def _list_tree(self, tree_oid: str) -> dict[str, str]:
        result = self._git(
            "ls-tree", "-r", "-z", "--full-tree", tree_oid
        )
        if result.returncode:
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise GitReadError(f"git ls-tree failed: {detail}")

        entries: dict[str, str] = {}
        for record in result.stdout.split(b"\0"):
            if not record:
                continue
            try:
                metadata, raw_path = record.split(b"\t", 1)
                mode, object_type, oid = metadata.decode("ascii").split()
                path = raw_path.decode("utf-8", errors="strict")
            except (ValueError, UnicodeDecodeError) as exc:
                raise GitReadError("invalid git ls-tree record") from exc
            if object_type == "blob":
                entries[path] = oid
        return entries

    def paths(self, prefix: str = "") -> list[str]:
        return sorted(path for path in self.entries if path.startswith(prefix))

    def blob(self, path: str) -> TreeBlob:
        oid = self.entries.get(path)
        if oid is None:
            raise GitReadError(f"blob is absent from selected tree: {path}")
        if oid not in self._blob_cache:
            result = self._git("cat-file", "blob", oid)
            if result.returncode:
                detail = result.stderr.decode("utf-8", errors="replace").strip()
                raise GitReadError(f"cannot read blob {path}: {detail}")
            self._blob_cache[oid] = result.stdout
        return TreeBlob(path=path, oid=oid, data=self._blob_cache[oid])

    def blob_at_commit(self, commit: str, path: str) -> TreeBlob:
        if not GIT_SHA_RE.fullmatch(commit):
            raise GitReadError(f"invalid prompt commit SHA: {commit!r}")
        result = self._git("rev-parse", "--verify", f"{commit}:{path}")
        if result.returncode:
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise GitReadError(
                f"prompt path {path!r} is absent at commit {commit}: {detail}"
            )
        oid = result.stdout.decode("ascii", errors="strict").strip()
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", oid):
            raise GitReadError(f"invalid prompt blob object ID: {oid!r}")
        content = self._git("cat-file", "blob", oid)
        if content.returncode:
            detail = content.stderr.decode("utf-8", errors="replace").strip()
            raise GitReadError(f"cannot read prompt blob {path}: {detail}")
        return TreeBlob(path=path, oid=oid, data=content.stdout)


def parse_yaml(raw: bytes, path: str) -> Any:
    try:
        text = raw.decode("utf-8", errors="strict")
        return yaml.load(text, Loader=StrictYAMLLoader)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def json_pointer(parts: Iterable[Any]) -> str:
    encoded = []
    for part in parts:
        encoded.append(str(part).replace("~", "~0").replace("/", "~1"))
    return "/" + "/".join(encoded) if encoded else ""


def actual_value_summary(value: Any, limit: int = 240) -> str:
    try:
        rendered = json.dumps(
            value, ensure_ascii=False, sort_keys=True, default=str
        )
    except Exception:
        rendered = repr(value)
    return rendered if len(rendered) <= limit else rendered[:limit] + "…"


def emit(
    result: RunResult,
    check: str,
    status: str,
    code: str,
    **fields: Any,
) -> None:
    result.events.append(
        Event(
            check=check,
            status=status,
            code=code,
            tree=result.tree,
            fields=fields,
        )
    )


def load_schema(tree: GitTree) -> dict[str, Any]:
    try:
        raw = tree.blob(SCHEMA_PATH).data
        schema = json.loads(raw.decode("utf-8", errors="strict"))
        Draft202012Validator.check_schema(schema)
    except GitReadError as exc:
        raise ConfigurationError(f"SCHEMA_UNAVAILABLE_OR_INVALID: {exc}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError, SchemaError) as exc:
        raise ConfigurationError(
            f"SCHEMA_UNAVAILABLE_OR_INVALID: {exc}"
        ) from exc
    if not isinstance(schema, dict):
        raise ConfigurationError("schema root must be a JSON object")
    return schema


def registry_yaml_paths(tree: GitTree) -> list[str]:
    return [
        path
        for path in tree.paths(REGISTRY_PREFIX)
        if path.endswith((".yaml", ".yml"))
    ]


def expected_id_from_registry_path(path: str) -> str | None:
    if not path.startswith(REGISTRY_PREFIX):
        return None

    relative = path[len(REGISTRY_PREFIX):]
    if "/" in relative:
        return None

    filename = relative.rsplit("/", 1)[-1]
    if not (filename.endswith(".yaml") or filename.endswith(".yml")):
        return None

    stem = filename.rsplit(".", 1)[0]
    if WORK_ITEM_ID_RE.fullmatch(stem):
        return stem

    return None


def record_id(record: dict[str, Any]) -> Any:
    return record.get("work_item_id")


def schema_error_code(error: ValidationError) -> str:
    if error.validator == "required":
        return "SCHEMA_REQUIRED_FIELD_MISSING"
    if error.validator == "additionalProperties":
        return "SCHEMA_ADDITIONAL_PROPERTY"
    if error.validator == "enum" or error.validator == "const":
        return "SCHEMA_ENUM_OUT_OF_RANGE"
    if error.validator == "oneOf":
        instance = error.instance

        # Collect nested oneOf branch errors. jsonschema exposes the
        # failures of individual alternatives through error.context.
        def iter_context_errors(parent):
            for child in parent.context:
                yield child
                yield from iter_context_errors(child)

        context_errors = list(iter_context_errors(error))

        if isinstance(instance, dict):
            state = instance.get("state")
            has_value = "value" in instance

            # UNKNOWN must not carry a value.
            if state == "UNKNOWN" and has_value:
                return "SCHEMA_STATE_VALUE_CONTRADICTION"

            # KNOWN requires the value property to be present.
            if state == "KNOWN":
                for child in context_errors:
                    if (
                        child.validator == "required"
                        and isinstance(child.validator_value, (list, tuple))
                        and "value" in child.validator_value
                    ):
                        return "SCHEMA_KNOWN_VALUE_MISSING"

            # KNOWN_EMPTY requires a valid empty value.
            # Identify a failed value constraint from the child error
            # location, rather than parsing the parent error message.
            if state == "KNOWN_EMPTY" and has_value:
                for child in context_errors:
                    if (
                        child.validator in ("const", "enum", "minLength", "maxLength")
                        and "value" in child.absolute_path
                    ):
                        return "SCHEMA_KNOWN_EMPTY_INVALID"

        return "SCHEMA_STATE_VALUE_CONTRADICTION"
    if error.validator == "anyOf":
        return "SCHEMA_STATE_VALUE_CONTRADICTION"
    return "SCHEMA_CONSTRAINT_VIOLATION"


def schema_error_events(
    result: RunResult,
    validator: Draft202012Validator,
    path: str,
    record: dict[str, Any],
) -> bool:
    errors = sorted(
        validator.iter_errors(record),
        key=lambda err: (
            tuple(str(part) for part in err.absolute_path),
            str(err.validator),
            err.message,
        ),
    )
    for error in errors:
        pointer = json_pointer(error.absolute_path)
        code = schema_error_code(error)
        actual = None
        try:
            actual = error.instance
        except Exception:
            pass
        emit(
            result,
            "registry.schema",
            "VIOLATION",
            code,
            path=path,
            pointer=pointer,
            keyword=error.validator,
            actual=actual_value_summary(actual),
            detail=error.message,
        )
    return not errors


def scan_registry(
    tree: GitTree,
    result: RunResult,
) -> dict[str, dict[str, Any]]:
    paths = registry_yaml_paths(tree)
    result.registry_files = len(paths)
    records: dict[str, dict[str, Any]] = {}

    for path in paths:
        try:
            raw = tree.blob(path).data
        except GitReadError as exc:
            emit(
                result,
                "registry.scan",
                "INCOMPLETE",
                "REGISTRY_BLOB_UNREADABLE",
                path=path,
                detail=str(exc),
            )
            continue

        try:
            record = parse_yaml(raw, path)
        except ValueError as exc:
            emit(
                result,
                "registry.scan",
                "INCOMPLETE",
                "REGISTRY_PARSE_ERROR",
                path=path,
                detail=str(exc),
            )
            continue

        if not isinstance(record, dict):
            emit(
                result,
                "registry.scan",
                "VIOLATION",
                "REGISTRY_ROOT_NOT_OBJECT",
                path=path,
                actual=actual_value_summary(record),
            )
            continue

        result.parsed += 1
        work_item_id = record_id(record)
        if not isinstance(work_item_id, str):
            emit(
                result,
                "registry.unique_ids",
                "VIOLATION",
                "WORK_ITEM_ID_MISSING_OR_NOT_STRING",
                path=path,
                actual=actual_value_summary(work_item_id),
            )
            continue

        if not WORK_ITEM_ID_RE.fullmatch(work_item_id):
            emit(
                result,
                "registry.unique_ids",
                "VIOLATION",
                "WORK_ITEM_ID_INVALID",
                path=path,
                work_item_id=work_item_id,
            )
            continue

        records[path] = record

    emit(
        result,
        "registry.scan",
        "PASS" if result.incomplete == 0 else "INCOMPLETE",
        "REGISTRY_SCAN_COMPLETE" if result.incomplete == 0 else "REGISTRY_SCAN_INCOMPLETE",
        registry_files=result.registry_files,
        parsed=result.parsed,
    )
    return records


def check_path_identity(
    records: dict[str, dict[str, Any]],
    result: RunResult,
) -> None:
    failures = 0
    for path, record in sorted(records.items()):
        expected = expected_id_from_registry_path(path)
        actual = record.get("work_item_id")
        if expected is None:
            emit(
                result,
                "registry.path_identity",
                "VIOLATION",
                "REGISTRY_PATH_NOT_CANONICAL",
                path=path,
                work_item_id=actual,
            )
            failures += 1
        elif actual != expected:
            emit(
                result,
                "registry.path_identity",
                "VIOLATION",
                "REGISTRY_PATH_ID_MISMATCH",
                path=path,
                expected_id=expected,
                work_item_id=actual,
            )
            failures += 1

    if failures == 0:
        emit(
            result,
            "registry.path_identity",
            "PASS",
            "REGISTRY_PATH_IDENTITY_VALID",
            records=len(records),
        )


def check_unique_ids(
    records: dict[str, dict[str, Any]],
    result: RunResult,
) -> None:
    id_to_paths: dict[str, list[str]] = defaultdict(list)
    for path, record in records.items():
        work_item_id = record.get("work_item_id")
        if isinstance(work_item_id, str) and WORK_ITEM_ID_RE.fullmatch(work_item_id):
            id_to_paths[work_item_id].append(path)

    duplicates = 0
    for work_item_id, paths in sorted(id_to_paths.items()):
        if len(paths) > 1:
            duplicates += 1
            emit(
                result,
                "registry.unique_ids",
                "VIOLATION",
                "DUPLICATE_WORK_ITEM_ID",
                work_item_id=work_item_id,
                paths=sorted(paths),
            )

    result.duplicate_ids = duplicates
    if duplicates == 0:
        emit(
            result,
            "registry.unique_ids",
            "PASS",
            "REGISTRY_IDS_UNIQUE",
            unique_ids=len(id_to_paths),
        )


def check_schema(
    records: dict[str, dict[str, Any]],
    schema: dict[str, Any],
    result: RunResult,
) -> None:
    validator = Draft202012Validator(schema)
    valid = 0
    for path, record in sorted(records.items()):
        if schema_error_events(result, validator, path, record):
            valid += 1
    result.schema_valid = valid
    if valid == len(records):
        emit(
            result,
            "registry.schema",
            "PASS",
            "REGISTRY_SCHEMA_VALID",
            validated=valid,
        )


def get_nested(document: Any, *keys: str) -> Any:
    value = document
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def field_state_value(field: Any) -> tuple[str | None, Any]:
    if not isinstance(field, dict):
        return None, None
    return field.get("state"), field.get("value")


def prompt_pin_check(
    tree: GitTree,
    path: str,
    record: dict[str, Any],
    result: RunResult,
) -> None:
    prompt = record.get("prompt")
    if not isinstance(prompt, dict):
        return

    status = prompt.get("prompt_status")
    if status != "PINNED":
        return

    result.prompt_pins_checked += 1
    required_fields = (
        ("prompt_path", prompt.get("prompt_path")),
        ("prompt_sha256", prompt.get("prompt_sha256")),
        ("prompt_commit_sha", prompt.get("prompt_commit_sha")),
    )

    missing = [
        name
        for name, value in required_fields
        if field_state_value(value)[0] != "KNOWN"
    ]
    if missing:
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "VIOLATION",
            "PROMPT_PIN_REQUIRED_FIELD_NOT_KNOWN",
            path=path,
            work_item_id=record.get("work_item_id"),
            fields=missing,
        )
        return

    prompt_path = prompt["prompt_path"]["value"]
    expected_sha = prompt["prompt_sha256"]["value"]
    commit_sha = prompt["prompt_commit_sha"]["value"]

    if not isinstance(prompt_path, str) or not prompt_path:
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "VIOLATION",
            "PROMPT_PIN_PATH_INVALID",
            path=path,
            work_item_id=record.get("work_item_id"),
        )
        return

    pure_path = PurePosixPath(prompt_path)
    if (
        pure_path.is_absolute()
        or ".." in pure_path.parts
        or "\\" in prompt_path
        or prompt_path.startswith("/")
    ):
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "VIOLATION",
            "PROMPT_PIN_PATH_UNSAFE",
            path=path,
            work_item_id=record.get("work_item_id"),
            prompt_path=prompt_path,
        )
        return

    if not isinstance(expected_sha, str) or not SHA256_RE.fullmatch(expected_sha):
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "VIOLATION",
            "PROMPT_PIN_SHA256_INVALID",
            path=path,
            work_item_id=record.get("work_item_id"),
        )
        return

    if not isinstance(commit_sha, str) or not GIT_SHA_RE.fullmatch(commit_sha):
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "VIOLATION",
            "PROMPT_PIN_COMMIT_INVALID",
            path=path,
            work_item_id=record.get("work_item_id"),
        )
        return

    try:
        prompt_blob = tree.blob_at_commit(commit_sha, prompt_path)
    except GitReadError as exc:
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "INCOMPLETE",
            "PROMPT_PIN_BLOB_UNREADABLE",
            path=path,
            work_item_id=record.get("work_item_id"),
            prompt_path=prompt_path,
            detail=str(exc),
        )
        return

    actual_sha = hashlib.sha256(prompt_blob.data).hexdigest()
    if actual_sha.lower() != expected_sha.lower():
        result.prompt_pins_failed += 1
        emit(
            result,
            "registry.prompt_pin",
            "VIOLATION",
            "PROMPT_PIN_SHA256_MISMATCH",
            path=path,
            work_item_id=record.get("work_item_id"),
            prompt_path=prompt_path,
            expected_sha256=expected_sha,
            actual_sha256=actual_sha,
        )
        return

    prompt_bytes = prompt.get("prompt_bytes")
    if prompt_bytes is not None:
        state, declared_bytes = field_state_value(prompt_bytes)
        if state == "KNOWN" and declared_bytes != len(prompt_blob.data):
            result.prompt_pins_failed += 1
            emit(
                result,
                "registry.prompt_pin",
                "VIOLATION",
                "PROMPT_PIN_BYTES_MISMATCH",
                path=path,
                work_item_id=record.get("work_item_id"),
                expected_bytes=len(prompt_blob.data),
                declared_bytes=declared_bytes,
            )
            return

    emit(
        result,
        "registry.prompt_pin",
        "PASS",
        "PROMPT_PIN_VALID",
        path=path,
        work_item_id=record.get("work_item_id"),
        prompt_path=prompt_path,
        prompt_sha256=actual_sha,
    )


def manifest_identity(document: Any) -> str | None:
    if not isinstance(document, dict):
        return None

    candidates: list[Any] = []
    for key in ("work_item_id", "aid"):
        value = document.get(key)
        if value is not None:
            candidates.append(value)

    work_item = document.get("work_item")
    if isinstance(work_item, dict) and (
        work_item.get("identifier_status")
        == "coordinator_verified_unique_see_identifier_evidence"
    ):
        value = work_item.get("proposed_id")
        if value is not None:
            candidates.append(value)

    if not candidates:
        return None
    if any(
        not isinstance(value, str)
        or not (WORK_ITEM_ID_RE.fullmatch(value) or FIX_ID_RE.fullmatch(value))
        for value in candidates
    ):
        return None
    if len(set(candidates)) != 1:
        return None
    return candidates[0]


def load_inventory(tree: GitTree) -> dict[str, Any]:
    raw = tree.blob(INVENTORY_PATH).data
    inventory = parse_yaml(raw, INVENTORY_PATH)
    if not isinstance(inventory, dict):
        raise ValueError("inventory root is not an object")
    if inventory.get("inventory_version") != 1:
        raise ValueError("inventory_version must be 1")
    if inventory.get("source_prefix") != MANIFEST_PREFIX:
        raise ValueError("inventory source_prefix is invalid")
    if not isinstance(inventory.get("source_tree"), str):
        raise ValueError("inventory source_tree must be a string")
    if not isinstance(inventory.get("entries"), list):
        raise ValueError("inventory entries must be a list")
    return inventory


def check_inventory(
    tree: GitTree,
    records: dict[str, dict[str, Any]],
    result: RunResult,
) -> None:
    try:
        inventory = load_inventory(tree)
    except (GitReadError, ValueError) as exc:
        emit(
            result,
            "registry.inventory",
            "INCOMPLETE",
            "INVENTORY_UNAVAILABLE_OR_INVALID",
            path=INVENTORY_PATH,
            detail=str(exc),
        )
        return

    entries: dict[str, dict[str, Any]] = {}
    for entry in inventory["entries"]:
        if not isinstance(entry, dict):
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "INVENTORY_ENTRY_NOT_OBJECT",
                actual=actual_value_summary(entry),
            )
            continue
        work_item_id = entry.get("work_item_id")
        if not isinstance(work_item_id, str):
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "INVENTORY_WORK_ITEM_ID_INVALID",
                actual=actual_value_summary(work_item_id),
            )
            continue
        if work_item_id in entries:
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "INVENTORY_DUPLICATE_WORK_ITEM_ID",
                work_item_id=work_item_id,
            )
            continue
        entries[work_item_id] = entry

    registry_ids = {
        record.get("work_item_id")
        for record in records.values()
        if isinstance(record.get("work_item_id"), str)
    }

    source_manifest_ids: dict[str, str] = {}
    manifest_paths = [
        path
        for path in tree.paths(MANIFEST_PREFIX)
        if path.endswith("/manifest.yaml")
        and len(path[len(MANIFEST_PREFIX):].split("/")) == 2
    ]

    for path in manifest_paths:
        try:
            document = parse_yaml(tree.blob(path).data, path)
        except (GitReadError, ValueError) as exc:
            emit(
                result,
                "registry.inventory",
                "INCOMPLETE",
                "INVENTORY_SOURCE_MANIFEST_UNREADABLE",
                path=path,
                detail=str(exc),
            )
            continue

        work_item_id = manifest_identity(document)
        if work_item_id is None:
            emit(
                result,
                "registry.inventory",
                "INCOMPLETE",
                "INVENTORY_SOURCE_ID_UNRESOLVED",
                path=path,
            )
            continue
        if work_item_id in source_manifest_ids:
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "DUPLICATE_SOURCE_MANIFEST_ID",
                work_item_id=work_item_id,
                paths=sorted([source_manifest_ids[work_item_id], path]),
            )
            continue
        source_manifest_ids[work_item_id] = path

    for work_item_id, source_path in sorted(source_manifest_ids.items()):
        if work_item_id not in entries:
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "INVENTORY_ENTRY_MISSING",
                work_item_id=work_item_id,
                source_manifest=source_path,
            )

    for work_item_id, entry in sorted(entries.items()):
        state = entry.get("migration_state")
        registry_path = entry.get("registry_path")
        source_path = entry.get("source_manifest")
        if work_item_id not in source_manifest_ids:
            if state != "EXCLUDED_BY_AUTHORITY":
                emit(
                    result,
                    "registry.inventory",
                    "VIOLATION",
                    "INVENTORY_SOURCE_MISSING",
                    work_item_id=work_item_id,
                    source_manifest=source_path,
                )
            continue

        if source_manifest_ids[work_item_id] != source_path:
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "INVENTORY_SOURCE_PATH_MISMATCH",
                work_item_id=work_item_id,
                expected=source_manifest_ids[work_item_id],
                actual=source_path,
            )

        if state == "NOT_MIGRATED":
            if registry_path is not None or work_item_id in registry_ids:
                emit(
                    result,
                    "registry.inventory",
                    "VIOLATION",
                    "INVENTORY_REGISTRY_STATE_MISMATCH",
                    work_item_id=work_item_id,
                    registry_path=registry_path,
                )
        elif state in {"MIGRATED", "MIGRATED_WITH_UNCONFIRMED_FIELDS"}:
            if work_item_id not in registry_ids:
                emit(
                    result,
                    "registry.inventory",
                    "VIOLATION",
                    "MIGRATED_RECORD_MISSING",
                    work_item_id=work_item_id,
                )
        elif state == "EXCLUDED_BY_AUTHORITY":
            evidence = entry.get("exclusion")
            if not isinstance(evidence, dict) or not evidence.get("source_ref") or not evidence.get("reason"):
                emit(
                    result,
                    "registry.inventory",
                    "VIOLATION",
                    "EXCLUSION_UNAUTHORIZED",
                    work_item_id=work_item_id,
                )
        else:
            emit(
                result,
                "registry.inventory",
                "VIOLATION",
                "INVENTORY_MIGRATION_STATE_INVALID",
                work_item_id=work_item_id,
                migration_state=state,
            )

    if not any(event.check == "registry.inventory" for event in result.events):
        emit(
            result,
            "registry.inventory",
            "PASS",
            "INVENTORY_CONSISTENT",
            inventory_entries=len(entries),
            source_manifests=len(source_manifest_ids),
        )


def emit_index_projection_deferred(result: RunResult) -> None:
    emit(
        result,
        "registry.index_projection",
        "NOT_APPLICABLE",
        "INDEX_PROJECTION_DEFERRED_TO_PHASE_D",
        owner="scripts/ci/check_work_item_index.py",
    )


def run_checks(
    root: str,
    revision: str,
    *,
    mode: str = "required",
    strict_inventory: bool = False,
) -> RunResult:
    tree = GitTree(root, revision)
    result = RunResult(tree=tree.tree_oid)

    try:
        schema = load_schema(tree)
    except ConfigurationError as exc:
        emit(
            result,
            "registry.schema",
            "INCOMPLETE",
            "SCHEMA_UNAVAILABLE_OR_INVALID",
            detail=str(exc),
        )
        emit_index_projection_deferred(result)
        return result

    records = scan_registry(tree, result)

    if not records and result.registry_files == 0:
        emit(
            result,
            "registry.path_identity",
            "PASS",
            "REGISTRY_EMPTY",
            records=0,
        )
        emit(
            result,
            "registry.unique_ids",
            "PASS",
            "REGISTRY_EMPTY",
            unique_ids=0,
        )
        emit(
            result,
            "registry.schema",
            "PASS",
            "REGISTRY_EMPTY",
            validated=0,
        )
        emit(
            result,
            "registry.prompt_pin",
            "PASS",
            "NO_PROMPT_PINS",
            checked=0,
        )
        if strict_inventory:
            check_inventory(tree, records, result)
        else:
            emit(
                result,
                "registry.inventory",
                "NOT_APPLICABLE",
                "STRICT_INVENTORY_NOT_REQUESTED",
            )
        emit_index_projection_deferred(result)
        return result

    check_path_identity(records, result)
    check_unique_ids(records, result)
    check_schema(records, schema, result)

    for path, record in sorted(records.items()):
        prompt_pin_check(tree, path, record, result)

    if result.prompt_pins_checked == 0:
        emit(
            result,
            "registry.prompt_pin",
            "PASS",
            "NO_PROMPT_PINS",
            checked=0,
        )

    if strict_inventory:
        check_inventory(tree, records, result)
    else:
        emit(
            result,
            "registry.inventory",
            "NOT_APPLICABLE",
            "STRICT_INVENTORY_NOT_REQUESTED",
        )

    emit_index_projection_deferred(result)
    return result


def diagnostic_not_applicable(result: RunResult) -> bool:
    """Diagnostic mode returns 5 only when no registry record exists."""
    return result.registry_files == 0 and result.overall == "PASS"


def built_in_self_test() -> tuple[bool, list[dict[str, Any]]]:
    """Execute independent input cases and verify their expected outcomes."""
    cases: list[tuple[str, Any, str]] = [
        ("valid_object", {"work_item_id": "AID-2026-001"}, "object"),
        ("root_array", [], "not_object"),
        ("root_scalar", "x", "not_object"),
        ("duplicate_yaml_keys", b"work_item_id: AID-2026-001\nwork_item_id: AID-2026-002\n", "parse_error"),
        ("invalid_yaml", b"work_item_id: [\n", "parse_error"),
        ("invalid_id", {"work_item_id": "AID-26-1"}, "invalid_id"),
        ("missing_id", {"title": "x"}, "missing_id"),
    ]
    results = []
    passed = True

    for name, value, expected in cases:
        actual = "object"
        if isinstance(value, bytes):
            try:
                parsed = parse_yaml(value, f"<self-test:{name}>")
            except ValueError:
                actual = "parse_error"
            else:
                actual = "object" if isinstance(parsed, dict) else "not_object"
        elif not isinstance(value, dict):
            actual = "not_object"
        elif not isinstance(value.get("work_item_id"), str):
            actual = "missing_id"
        elif not WORK_ITEM_ID_RE.fullmatch(value["work_item_id"]):
            actual = "invalid_id"

        ok = actual == expected
        passed = passed and ok
        results.append(
            {
                "case": name,
                "expected": expected,
                "actual": actual,
                "passed": ok,
            }
        )

    return passed, results


def write_jsonl(result: RunResult, *, diagnostic: bool = False) -> None:
    for event in result.events:
        print(json.dumps(event.as_dict(), ensure_ascii=False, sort_keys=True))

    summary = result.summary()
    if diagnostic and diagnostic_not_applicable(result):
        summary["overall"] = "NOT_APPLICABLE"
        summary["exit_code"] = EXIT_NA
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree", help="candidate commit or tree object")
    parser.add_argument("--root", default=".", help="Git repository root")
    parser.add_argument(
        "--mode",
        choices=("required", "diagnostic"),
        default="required",
    )
    parser.add_argument("--strict-inventory", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--diagnose-legacy", action="store_true")
    parser.add_argument("--jsonl", action="store_true")
    # Kept for CLI compatibility. INDEX projection is owned by Phase D.
    parser.add_argument("--index-check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        passed, cases = built_in_self_test()
        for case in cases:
            print(json.dumps(case, sort_keys=True))
        print(
            json.dumps(
                {
                    "type": "self_test_summary",
                    "cases": len(cases),
                    "passed": sum(case["passed"] for case in cases),
                    "failed": sum(not case["passed"] for case in cases),
                    "exit_code": 0 if passed else 1,
                },
                sort_keys=True,
            )
        )
        return 0 if passed else 1

    if not args.tree:
        parser.error("--tree is required unless --self-test is used")

    try:
        result = run_checks(
            args.root,
            args.tree,
            mode=args.mode,
            strict_inventory=args.strict_inventory,
        )
    except ConfigurationError as exc:
        print(
            json.dumps(
                {
                    "type": "check",
                    "check": "registry.configuration",
                    "status": "INCOMPLETE",
                    "code": "CONFIGURATION_ERROR",
                    "detail": str(exc),
                    "tree": None,
                },
                sort_keys=True,
            )
        )
        print(f"CONFIGURATION ERROR: {exc}", file=sys.stderr)
        return EXIT_CONFIG
    except GitReadError as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return EXIT_INCOMPLETE

    write_jsonl(result, diagnostic=args.mode == "diagnostic")

    if args.mode == "diagnostic" and diagnostic_not_applicable(result):
        return EXIT_NA
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
