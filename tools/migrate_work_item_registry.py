#!/usr/bin/env python3
"""Read-only, tree-based migration assessor for the work-item registry.

Inventory and source evidence deliberately have different trust boundaries:

* --source-tree selects the immutable Git commit being assessed. Work-item
  manifests and referenced Git blobs are read only from that commit.
* --inventory is a current-working-tree input. Its source_tree declaration
  must identify the exact resolved source commit.
* Inventory rows are matched by source_manifest.
* The registry schema is an output of a later governance phase. If absent
  from the selected source commit, schema validation is explicitly deferred.

The assessor never writes registry records. With --dry-run, --output is a
destination declaration only and is never created, inspected, or modified.
All report output is written to stdout; diagnostics are written to stderr.

Exit codes:
    0: all requested discovery, inventory, parsing, and pin checks completed.
       A schema absent from the historical source tree is reported as deferred.
    2: an assertion failed or a fail-closed data condition was encountered.
    4: command-line, inventory, or present-schema configuration is invalid.

Dependencies: Python 3.12 standard library and PyYAML.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
    from yaml.nodes import MappingNode, ScalarNode, SequenceNode
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "CONFIGURATION ERROR: PyYAML is required; install pyyaml."
    ) from exc


IDENTITY_RE = re.compile(
    r"^(?:AID-[0-9]{4}-[0-9]{3}|FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*)$"
)
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
COMMIT_PREFIX_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")
PROMPT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$")
CLASS_RE = re.compile(
    r"^[A-Z][A-Z0-9_-]*(?:/[A-Z][A-Z0-9_-]*)*"
    r"(?:[ ]*\+[ ]*[A-Z][A-Z0-9_-]*(?:/[A-Z][A-Z0-9_-]*)*)*$"
)
RISK_VALUES = {"R1", "R2", "R3", "NOT_ASSIGNED", "NOT_ADJUDICATED"}
STATUS_VALUES = {
    "DISPATCHED", "MERGED", "REGISTERED", "PROPOSED", "IMPLEMENTED",
    "VERIFIED", "IMPLEMENTED_ACCEPTANCE_PENDING",
    "REMEDIATION_IN_PROGRESS", "CLOSED", "ADOPTED", "COMPLETE",
    "PENDING_FORMAL_REGISTRATION", "DRAFT", "IMPLEMENTATION_IN_PROGRESS",
    "IN_PROGRESS",
}
PROMPT_STATUS_VALUES = {"PINNED", "NOT_PRESENT"}

WORK_ITEMS_PREFIX = "14-ai-development/work-items/"
SCHEMA_PATH = "00-governance/schemas/work-item-registry.schema.json"
INVENTORY_VERSION = 1

IDENTITY_SHAPES = (
    ("work_item_id",),
    ("aid",),
    ("work_item", "proposed_id"),
)
OWNER_PATHS = (
    ("authority", "accountable_owner"),
    ("governance", "accountable_owner"),
    ("accountable_owner",),
    ("owner",),
)
PROMPT_ID_PATHS = (("prompt_id",), ("prompt", "id"))
PROMPT_SHA_PATHS = (
    ("prompt_sha256",),
    ("prompt", "sha256"),
    ("prompt", "prompt_sha256"),
)
PROMPT_STATUS_PATHS = (
    ("prompt_status",),
    ("prompt", "prompt_status"),
)
PROMPT_FILE_PATHS = (
    ("prompt_file",),
    ("prompt", "prompt_file"),
)
PROMPT_COMMIT_PATHS = (
    ("prompt_file_commit_sha",),
    ("prompt", "prompt_file_commit_sha"),
)
FIELD_NAMES = (
    "work_item_id", "title", "owner", "class", "risk", "status",
    "prompt_id", "prompt_sha256", "prompt_status", "implementation",
    "review", "acceptance",
)
INVENTORY_STATES = {
    "NOT_MIGRATED", "MIGRATED", "MIGRATED_WITH_UNCONFIRMED_FIELDS",
    "EXCLUDED_BY_AUTHORITY",
}


class ConfigurationError(Exception):
    """Invalid CLI, inventory, or present-schema configuration."""


class AssessmentError(Exception):
    """A fail-closed data or validation condition."""


@dataclass(frozen=True)
class GitBlob:
    path: str
    oid: str
    data: bytes
    sha256: str


@dataclass(frozen=True)
class Manifest:
    path: str
    directory_id: str
    blob: GitBlob
    document: dict[str, Any]


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader rejecting duplicate mapping keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "unhashable mapping key", key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def git(root: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssessmentError(
            f"git {' '.join(args)} failed ({result.returncode}): {message}"
        )
    return result


def resolve_commit(root: str, revision: str) -> str:
    result = git(root, "rev-parse", "--verify", f"{revision}^{{commit}}")
    value = result.stdout.decode("ascii", errors="strict").strip()
    if not COMMIT_RE.fullmatch(value):
        raise ConfigurationError(
            f"source revision did not resolve to a commit: {revision}"
        )
    return value


def resolve_tree(root: str, revision: str) -> tuple[str, str]:
    commit = resolve_commit(root, revision)
    result = git(root, "rev-parse", "--verify", f"{commit}^{{tree}}")
    tree_oid = result.stdout.decode("ascii", errors="strict").strip()
    if not COMMIT_RE.fullmatch(tree_oid):
        raise ConfigurationError(
            f"source revision did not resolve to a tree: {revision}"
        )
    return commit, tree_oid


def list_tree(root: str, tree_oid: str) -> dict[str, str]:
    result = git(
        root, "ls-tree", "-r", "-z", "--full-tree", tree_oid,
        "--", WORK_ITEMS_PREFIX,
    )
    entries: dict[str, str] = {}
    for raw_entry in result.stdout.split(b"\0"):
        if not raw_entry:
            continue
        try:
            metadata, raw_path = raw_entry.split(b"\t", 1)
            _mode, object_type, oid = metadata.decode("ascii").split()
            path = raw_path.decode("utf-8", errors="strict")
        except (ValueError, UnicodeDecodeError) as exc:
            raise AssessmentError(
                "work-item tree listing contains an invalid entry"
            ) from exc
        if object_type != "blob":
            continue
        if not path.startswith(WORK_ITEMS_PREFIX):
            raise AssessmentError(
                f"Git returned a path outside the requested work-item prefix: {path}"
            )
        if path in entries:
            raise AssessmentError(f"duplicate path in Git tree listing: {path}")
        if not re.fullmatch(r"[0-9a-f]{40}", oid):
            raise AssessmentError(f"invalid blob object ID for {path}")
        entries[path] = oid
    return entries


def read_blob(root: str, oid: str, path: str) -> GitBlob:
    if not re.fullmatch(r"[0-9a-f]{40}", oid):
        raise AssessmentError(f"invalid Git blob object ID for {path}: {oid!r}")
    data = git(root, "cat-file", "blob", oid).stdout
    return GitBlob(path, oid, data, hashlib.sha256(data).hexdigest())


def parse_yaml(data: bytes, path: str) -> dict[str, Any]:
    try:
        text = data.decode("utf-8", errors="strict")
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise AssessmentError(f"YAML parse/read failure at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AssessmentError(f"YAML root is not a mapping: {path}")
    return value


def get_path(document: Any, path: tuple[str, ...]) -> Any:
    value = document
    for part in path:
        if isinstance(value, list):
            try:
                index = int(part)
                value = value[index]
            except (ValueError, IndexError):
                return None
        elif isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    return value


def line_for_path(text: str, path: tuple[str, ...]) -> int | None:
    if not path:
        return None
    key = re.escape(path[-1])
    match = re.search(rf"^\s*{key}\s*:", text, re.MULTILINE)
    return text.count("\n", 0, match.start()) + 1 if match else None


def candidate(source: str, blob: GitBlob, line: int | None, value: Any):
    return {
        "source": source, "path": blob.path, "line": line,
        "blob_sha256": blob.sha256, "value": value,
    }


def state_result(
    state: str,
    authority: str | None,
    candidates: list[dict[str, Any]],
    reason: str,
):
    return {
        "state": state, "authority": authority,
        "candidates": candidates, "reason": reason,
    }


def extract_identity(document: dict[str, Any]):
    declarations: list[tuple[str, Any]] = []
    for path in IDENTITY_SHAPES:
        value = get_path(document, path)
        if value is None:
            continue
        if path == ("work_item", "proposed_id"):
            status = get_path(document, ("work_item", "identifier_status"))
            if status != "coordinator_verified_unique_see_identifier_evidence":
                declarations.append((
                    "work_item.proposed_id (rejected: identifier_status missing or invalid)",
                    value,
                ))
                continue
        declarations.append((".".join(path), value))

    if not declarations:
        return None, [], "no supported identity declaration was present"
    values = [value for _, value in declarations]
    if any(
        not isinstance(value, str) or not IDENTITY_RE.fullmatch(value)
        for value in values
    ):
        return None, declarations, (
            "one or more identity declarations are malformed or not authorized"
        )
    if len(set(values)) != 1:
        return None, declarations, "supported identity declarations disagree"
    return values[0], declarations, "all supported identity declarations agree"


def discover_manifests(root: str, blobs: dict[str, str]):
    manifests: list[Manifest] = []
    failures: list[dict[str, str]] = []
    for path, oid in sorted(blobs.items()):
        if not path.startswith(WORK_ITEMS_PREFIX) or not path.endswith("/manifest.yaml"):
            continue
        parts = path[len(WORK_ITEMS_PREFIX):].split("/")
        if len(parts) != 2 or parts[1] != "manifest.yaml":
            continue
        directory_id = parts[0]
        if not IDENTITY_RE.fullmatch(directory_id):
            failures.append({
                "path": path,
                "reason": "manifest directory is not an AID/FIX identifier",
            })
            continue
        try:
            blob = read_blob(root, oid, path)
            document = parse_yaml(blob.data, path)
        except AssessmentError as exc:
            failures.append({"path": path, "reason": str(exc)})
            continue
        manifests.append(Manifest(path, directory_id, blob, document))
    return manifests, failures


def _inventory_file_path(root: str, inventory_path: str) -> Path:
    pure = PurePosixPath(inventory_path)
    if (
        not inventory_path or pure.is_absolute() or "\\" in inventory_path
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise ConfigurationError(
            f"--inventory must be a safe repository-relative path: {inventory_path!r}"
        )
    root_path = Path(root).resolve()
    candidate_path = (root_path / Path(*pure.parts)).resolve()
    try:
        candidate_path.relative_to(root_path)
    except ValueError as exc:
        raise ConfigurationError(
            f"--inventory resolves outside the repository root: {inventory_path}"
        ) from exc
    if not candidate_path.is_file():
        raise ConfigurationError(
            f"inventory is not present in the current working tree: {inventory_path}"
        )
    return candidate_path


def load_inventory(root: str, inventory_path: str):
    path = _inventory_file_path(root, inventory_path)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ConfigurationError(
            f"cannot read current-working-tree inventory {inventory_path}: {exc}"
        ) from exc
    try:
        inventory = parse_yaml(data, inventory_path)
    except AssessmentError as exc:
        raise ConfigurationError(str(exc)) from exc
    if type(inventory.get("inventory_version")) is not int or inventory["inventory_version"] != INVENTORY_VERSION:
        raise ConfigurationError(f"inventory_version must be integer {INVENTORY_VERSION}")
    if inventory.get("source_prefix") != WORK_ITEMS_PREFIX:
        raise ConfigurationError(f"source_prefix must be {WORK_ITEMS_PREFIX!r}")
    if not isinstance(inventory.get("source_tree"), str):
        raise ConfigurationError("inventory.source_tree must be a string")
    if not isinstance(inventory.get("entries"), list):
        raise ConfigurationError("inventory.entries must be a list")
    return inventory


def _normalise_inventory_entries(raw_entries: list[Any]):
    normalized = []
    seen: set[str] = set()
    for index, entry in enumerate(raw_entries):
        if not isinstance(entry, dict):
            raise ConfigurationError(f"inventory entry #{index + 1} must be a mapping")
        source_manifest = entry.get("source_manifest")
        pure = PurePosixPath(source_manifest) if isinstance(source_manifest, str) else None
        if (
            not isinstance(source_manifest, str)
            or not source_manifest.startswith(WORK_ITEMS_PREFIX)
            or "\\" in source_manifest
            or pure.is_absolute()
            or ".." in pure.parts
            or pure.as_posix() != source_manifest
        ):
            raise ConfigurationError(
                f"inventory entry #{index + 1} has invalid source_manifest: {source_manifest!r}"
            )
        if source_manifest in seen:
            raise ConfigurationError(f"duplicate inventory source_manifest: {source_manifest}")
        seen.add(source_manifest)
        normalized.append(entry)
    return normalized


def validate_inventory(
    inventory: dict[str, Any],
    manifests: list[Manifest],
    failures: list[dict[str, str]],
    expected_source: str,
    resolved_commit: str,
):
    declared_source = inventory["source_tree"]
    if not COMMIT_PREFIX_RE.fullmatch(declared_source):
        raise ConfigurationError(
            "inventory.source_tree must be a hexadecimal commit ID or abbreviation "
            f"of at least 7 characters: {declared_source!r}"
        )
    if not resolved_commit.startswith(declared_source.lower()):
        raise ConfigurationError(
            "inventory source_tree does not identify the selected source commit: "
            f"{declared_source} != {resolved_commit}"
        )
    if expected_source:
        expected = expected_source.lower()
        if COMMIT_PREFIX_RE.fullmatch(expected) and not resolved_commit.startswith(expected):
            raise ConfigurationError(
                "--source-tree resolution does not match the requested revision: "
                f"{expected_source} != {resolved_commit}"
            )

    manifest_ids: dict[str, list[str]] = {}
    manifest_by_path: dict[str, Manifest] = {}
    for manifest in manifests:
        if manifest.path in manifest_by_path:
            raise AssessmentError(f"duplicate source manifest path discovered: {manifest.path}")
        manifest_by_path[manifest.path] = manifest
        work_item_id, _, _ = extract_identity(manifest.document)
        if work_item_id is None:
            failures.append({
                "path": manifest.path,
                "reason": "manifest identity could not be resolved",
            })
            continue
        manifest_ids.setdefault(work_item_id, []).append(manifest.path)

    duplicate_ids = {
        work_item_id: paths for work_item_id, paths in manifest_ids.items()
        if len(paths) > 1
    }
    if duplicate_ids:
        raise AssessmentError(
            "duplicate manifest identities: " + json.dumps(duplicate_ids, sort_keys=True)
        )

    entries: dict[str, dict[str, Any]] = {}
    entries_by_source_manifest: dict[str, dict[str, Any]] = {}
    normalized_entries = _normalise_inventory_entries(inventory["entries"])
    for entry in normalized_entries:
        work_item_id = entry.get("work_item_id")
        if not isinstance(work_item_id, str) or not IDENTITY_RE.fullmatch(work_item_id):
            raise ConfigurationError(f"invalid inventory work_item_id: {work_item_id!r}")
        if work_item_id in entries:
            raise ConfigurationError(f"duplicate inventory ID: {work_item_id}")
        migration_state = entry.get("migration_state")
        if migration_state not in INVENTORY_STATES:
            raise ConfigurationError(
                f"invalid migration_state for {work_item_id}: {migration_state!r}"
            )
        source_manifest = entry["source_manifest"]
        if source_manifest in entries_by_source_manifest:
            raise ConfigurationError(f"duplicate inventory source_manifest: {source_manifest}")
        entries[work_item_id] = entry
        entries_by_source_manifest[source_manifest] = entry

    if len(entries) != 140:
        raise ConfigurationError(f"expected 140 inventory entries, found {len(entries)}")
    aid_count = sum(item.startswith("AID-") for item in entries)
    fix_count = sum(item.startswith("FIX-") for item in entries)
    if aid_count != 139 or fix_count != 1:
        raise ConfigurationError(
            f"expected 139 AID and 1 FIX inventory entries; found {aid_count} and {fix_count}"
        )

    for work_item_id, paths in manifest_ids.items():
        if work_item_id not in entries:
            raise AssessmentError(f"manifest identity missing from inventory: {work_item_id}")
        if len(paths) != 1:
            raise AssessmentError(
                f"manifest identity does not have exactly one source path: {work_item_id}"
            )
        source_manifest = paths[0]
        entry = entries_by_source_manifest.get(source_manifest)
        if entry is None:
            raise AssessmentError(
                f"inventory source_manifest missing for source record {work_item_id}: {source_manifest}"
            )
        if entry.get("work_item_id") != work_item_id:
            raise AssessmentError(
                f"inventory identity/source_manifest mismatch: {source_manifest} declares "
                f"{work_item_id}, inventory declares {entry.get('work_item_id')!r}"
            )

    for work_item_id, entry in entries.items():
        source_manifest = entry["source_manifest"]
        manifest = manifest_by_path.get(source_manifest)
        if manifest is None:
            if entry.get("migration_state") != "EXCLUDED_BY_AUTHORITY":
                raise AssessmentError(
                    "inventory source_manifest is absent from the selected source tree "
                    f"and is not an authorized exclusion: {source_manifest}"
                )
            continue
        manifest_id, _, _ = extract_identity(manifest.document)
        if manifest_id != work_item_id:
            raise AssessmentError(
                f"inventory source_manifest identity mismatch for {work_item_id}: "
                f"{source_manifest} resolves to {manifest_id!r}"
            )
        if entry.get("migration_state") == "NOT_MIGRATED" and entry.get("registry_path") is not None:
            raise AssessmentError(
                f"NOT_MIGRATED entry must have registry_path null: {work_item_id}"
            )

    failed_paths = {failure["path"] for failure in failures}
    for entry in normalized_entries:
        if entry["source_manifest"] in failed_paths and entry.get("migration_state") != "EXCLUDED_BY_AUTHORITY":
            raise AssessmentError(
                "inventory source_manifest points to a manifest that could not be parsed "
                f"or identified: {entry['source_manifest']}"
            )
    return entries


def walk_mapping(document: Any, prefix: tuple[str, ...] = ()):
    if isinstance(document, dict):
        for key, value in document.items():
            path = prefix + (str(key),)
            yield path, value
            yield from walk_mapping(value, path)
    elif isinstance(document, list):
        for index, value in enumerate(document):
            yield from walk_mapping(value, prefix + (str(index),))


def raw_text(blob: GitBlob) -> str:
    return blob.data.decode("utf-8", errors="strict")


def scalar_truncations(data: bytes, path: str) -> dict[tuple[str, ...], dict[str, Any]]:
    """Find plain YAML scalar nodes followed by an inline whitespace-# tail.

    YAML itself treats that tail as a comment and discards it before producing
    the Python value. The raw Git blob is therefore inspected independently.

    Only plain scalar nodes are candidates. A quoted scalar has an explicit
    closing quote, and a block scalar owns its content lines; a # in either
    form is not treated as an ambiguous plain-scalar truncation.
    """
    try:
        source = data.decode("utf-8", errors="strict")
        root = yaml.compose(source, Loader=UniqueKeyLoader)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise AssessmentError(f"cannot inspect raw YAML scalar boundaries at {path}: {exc}") from exc

    if root is None:
        return {}

    lines = source.splitlines()
    affected: dict[tuple[str, ...], dict[str, Any]] = {}

    def visit(node, prefix: tuple[str, ...]):
        if isinstance(node, MappingNode):
            for key_node, value_node in node.value:
                if isinstance(key_node, ScalarNode):
                    key = str(key_node.value)
                else:
                    key = "<non-scalar-key>"
                visit(value_node, prefix + (key,))
            return

        if isinstance(node, SequenceNode):
            for index, child in enumerate(node.value):
                visit(child, prefix + (str(index),))
            return

        if not isinstance(node, ScalarNode) or node.style is not None:
            return

        line_index = node.end_mark.line
        if line_index >= len(lines):
            return
        line = lines[line_index]
        tail = line[node.end_mark.column:]
        if not re.match(r"\s+#", tail):
            return

        line_number = line_index + 1
        raw_line = line
        parsed_value = node.value
        affected[prefix] = {
            "line": line_number,
            "raw": raw_line,
            "parsed": parsed_value,
            "style": "plain",
            "reason": (
                "plain scalar is followed by a whitespace-# comment tail; "
                "the original intended boundary cannot be recovered unambiguously "
                "from the parsed YAML value"
            ),
        }

    visit(root, ())
    return affected


def apply_truncation_policy(
    result: dict[str, Any],
    affected: dict[tuple[str, ...], dict[str, Any]],
) -> dict[str, Any]:
    """Downgrade any field whose selected evidence includes an affected scalar."""
    matches = []
    for item in result.get("candidates", []):
        source = item.get("source", "")
        if not isinstance(source, str) or not source.startswith("manifest."):
            continue
        suffix = source[len("manifest."):]
        candidate_path = tuple(suffix.split("."))
        details = affected.get(candidate_path)
        if details is None:
            continue
        matches.append({
            "source": source,
            "line": details["line"],
            "raw": details["raw"],
            "parsed": details["parsed"],
            "style": details["style"],
        })

    if not matches:
        return result

    result = dict(result)
    result["state"] = "UNCONFIRMED"
    result["authority"] = None
    details_text = json.dumps(matches, ensure_ascii=True, sort_keys=True)
    result["reason"] = (
        "raw Git blob scalar-boundary check found an ambiguous plain-scalar "
        "comment tail; field is UNCONFIRMED. raw/parsed evidence and line "
        f"number(s): {details_text}"
    )
    result["truncation_evidence"] = matches
    return result


def extract_candidates(
    manifest: Manifest,
    text: str,
    source_paths: tuple[tuple[str, ...], ...],
    source_prefix: str,
):
    found = []
    for path in source_paths:
        value = get_path(manifest.document, path)
        if value is None:
            continue
        found.append(candidate(
            source_prefix + "." + ".".join(path),
            manifest.blob, line_for_path(text, path), value,
        ))
    return found


def choose_scalar(
    candidates: list[dict[str, Any]],
    *,
    validator,
    missing_reason: str,
    invalid_reason: str,
    conflict_reason: str = "populated authoritative candidates disagree",
):
    if not candidates:
        return state_result("UNKNOWN", None, [], missing_reason)
    values = [item["value"] for item in candidates]
    if any(not validator(value) for value in values):
        return state_result("UNCONFIRMED", None, candidates, invalid_reason)
    canonical = {
        json.dumps(value, sort_keys=True, ensure_ascii=True) for value in values
    }
    if len(canonical) != 1:
        return state_result("UNCONFIRMED", None, candidates, conflict_reason)
    return state_result(
        "KNOWN", candidates[0]["path"], candidates,
        "all populated authoritative candidates agree and satisfy the field rule",
    )


def assess_identity(manifest: Manifest, text: str):
    work_item_id, declarations, reason = extract_identity(manifest.document)
    candidates = [
        candidate(
            f"manifest.{source}", manifest.blob,
            line_for_path(text, tuple(source.split(".")[-1:])), value,
        )
        for source, value in declarations
    ]
    if work_item_id is None:
        return state_result("UNCONFIRMED", None, candidates, reason)
    if work_item_id != manifest.directory_id:
        return state_result(
            "UNCONFIRMED", None, candidates,
            f"content identity {work_item_id} does not match directory {manifest.directory_id}",
        )
    return state_result("KNOWN", manifest.path, candidates, reason)


def assess_owner(manifest: Manifest, text: str):
    found: list[tuple[int, dict[str, Any]]] = []
    for priority, path in enumerate(OWNER_PATHS):
        value = get_path(manifest.document, path)
        if value is None:
            continue
        found.append((priority, candidate(
            "manifest." + ".".join(path), manifest.blob,
            line_for_path(text, path), value,
        )))
    if not found:
        return state_result(
            "UNKNOWN", None, [],
            "no accountable-owner declaration was found; attribution is not an owner alias",
        )
    candidates = [item for _, item in found]
    values = {
        json.dumps(item["value"], sort_keys=True, ensure_ascii=True)
        for item in candidates
    }
    if len(values) != 1 or any(
        not isinstance(item["value"], str) or not item["value"].strip()
        for item in candidates
    ):
        return state_result(
            "UNCONFIRMED", None, candidates,
            "accountable-owner declarations disagree or contain invalid values",
        )
    selected = min(found, key=lambda item: item[0])[1]
    return state_result(
        "KNOWN", selected["path"], candidates,
        "accountable-owner declarations agree; highest-precedence populated source selected",
    )


def assess_field(
    field: str,
    manifest: Manifest,
    text: str,
    all_blobs: dict[str, str],
    root: str,
    commit: str,
):
    doc = manifest.document

    if field == "work_item_id":
        return assess_identity(manifest, text)

    if field == "title":
        value = get_path(doc, ("title",))
        if value is None:
            return state_result("UNKNOWN", None, [], "top-level title is absent")
        item = candidate("manifest.title", manifest.blob, line_for_path(text, ("title",)), value)
        if not isinstance(value, str) or not value.strip():
            return state_result("UNCONFIRMED", None, [item], "title is not a non-empty YAML scalar")
        return state_result(
            "KNOWN", manifest.path, [item],
            "top-level YAML title scalar selected",
        )

    if field == "owner":
        return assess_owner(manifest, text)

    if field == "class":
        value = get_path(doc, ("class",))
        if value is None:
            return state_result("UNKNOWN", None, [], "top-level class is absent")
        item = candidate("manifest.class", manifest.blob, line_for_path(text, ("class",)), value)
        if (
            not isinstance(value, str) or not CLASS_RE.fullmatch(value)
            or value == "NOT_ASSIGNED"
            or re.search(r"(?:^|/)(?:R1|R2|R3)(?:$|[ /+])", value)
        ):
            return state_result(
                "UNCONFIRMED", None, [item],
                "class is outside the policy grammar, unassigned, provisional, or mixes risk into class",
            )
        return state_result("KNOWN", manifest.path, [item], "class matches policy grammar")

    if field == "risk":
        value = get_path(doc, ("risk",))
        if value is None:
            return state_result("UNKNOWN", None, [], "top-level risk is absent")
        item = candidate("manifest.risk", manifest.blob, line_for_path(text, ("risk",)), value)
        if not isinstance(value, str) or value not in RISK_VALUES:
            return state_result(
                "UNCONFIRMED", None, [item],
                "risk is not one of the policy's exact allowed values",
            )
        return state_result("KNOWN", manifest.path, [item], "risk matches exact allowed-value set")

    if field == "status":
        value = get_path(doc, ("status",))
        if value is None:
            return state_result("UNKNOWN", None, [], "top-level status is absent")
        item = candidate("manifest.status", manifest.blob, line_for_path(text, ("status",)), value)
        if not isinstance(value, str) or value not in STATUS_VALUES:
            return state_result(
                "UNCONFIRMED", None, [item],
                "status is not an exact member of the policy enum",
            )
        return state_result("KNOWN", manifest.path, [item], "status matches exact allowed-value set")

    if field == "prompt_id":
        return choose_scalar(
            extract_candidates(manifest, text, PROMPT_ID_PATHS, "manifest"),
            validator=lambda value: isinstance(value, str) and bool(PROMPT_ID_RE.fullmatch(value)),
            missing_reason="no registered prompt ID declaration was found",
            invalid_reason="registered prompt ID is not a valid non-empty identifier",
        )

    if field == "prompt_status":
        return choose_scalar(
            extract_candidates(manifest, text, PROMPT_STATUS_PATHS, "manifest"),
            validator=lambda value: isinstance(value, str) and value in PROMPT_STATUS_VALUES,
            missing_reason="no registered prompt status declaration was found",
            invalid_reason="registered prompt status is outside the exact allowed set",
        )

    if field == "prompt_sha256":
        found = extract_candidates(manifest, text, PROMPT_SHA_PATHS, "manifest")
        if not found:
            return state_result("UNKNOWN", None, [], "no registered prompt digest declaration was found")
        if any("executed_prompt_sha256" in item["source"] for item in found):
            raise AssessmentError(
                "executed prompt digest leaked into registered prompt_sha256 candidates: "
                f"{manifest.path}"
            )
        values = [item["value"] for item in found]
        if any(not isinstance(value, str) or not SHA256_RE.fullmatch(value) for value in values):
            return state_result(
                "UNCONFIRMED", None, found,
                "registered prompt digest is not a 64-hex SHA-256",
            )
        if len(set(value.lower() for value in values)) != 1:
            return state_result(
                "UNCONFIRMED", None, found,
                "registered prompt digest candidates disagree",
            )
        prompt_paths = extract_candidates(manifest, text, PROMPT_FILE_PATHS, "manifest")
        prompt_commits = extract_candidates(manifest, text, PROMPT_COMMIT_PATHS, "manifest")
        if len(prompt_paths) != 1 or len(prompt_commits) != 1:
            return state_result(
                "UNCONFIRMED", None, found + prompt_paths + prompt_commits,
                "a single explicit registered prompt path and prompt commit are required",
            )
        prompt_path = prompt_paths[0]["value"]
        prompt_commit = prompt_commits[0]["value"]
        if not isinstance(prompt_path, str) or not prompt_path:
            return state_result("UNCONFIRMED", None, found + prompt_paths, "registered prompt path is invalid")
        if not isinstance(prompt_commit, str) or not COMMIT_RE.fullmatch(prompt_commit):
            return state_result(
                "UNCONFIRMED", None, found + prompt_commits,
                "registered prompt commit must be a full 40-character commit SHA",
            )
        pure = PurePosixPath(prompt_path)
        if pure.is_absolute() or ".." in pure.parts or "\\" in prompt_path:
            return state_result(
                "UNCONFIRMED", None, found + prompt_paths,
                "registered prompt path is not a safe repository-relative path",
            )
        try:
            prompt_blob_oid = git(
                root, "rev-parse", "--verify", f"{prompt_commit}:{prompt_path}"
            ).stdout.decode("ascii").strip()
            if not re.fullmatch(r"[0-9a-f]{40}", prompt_blob_oid):
                raise AssessmentError(f"invalid prompt blob object ID: {prompt_blob_oid!r}")
            prompt_blob = read_blob(root, prompt_blob_oid, prompt_path)
        except AssessmentError:
            return state_result(
                "UNCONFIRMED", None, found + prompt_paths + prompt_commits,
                "registered prompt commit or blob is unreadable",
            )
        expected = values[0].lower()
        actual = hashlib.sha256(prompt_blob.data).hexdigest()
        found.append({
            "source": "registered_prompt_blob.sha256",
            "path": prompt_path, "line": None,
            "blob_sha256": prompt_blob.sha256, "value": actual,
        })
        if actual != expected:
            return state_result(
                "UNCONFIRMED", None, found,
                "registered prompt digest does not match the referenced Git blob bytes",
            )
        return state_result(
            "KNOWN", found[0]["path"], found,
            "registered prompt digest matches the exact referenced Git blob bytes",
        )

    if field in {"implementation", "review", "acceptance"}:
        return state_result(
            "UNKNOWN", None, [],
            "no independently authoritative registry-notes record was supplied in this source tree",
        )

    raise AssessmentError(f"unsupported registry field: {field}")


def validate_schema_presence(root: str, commit: str):
    result = git(root, "cat-file", "-e", f"{commit}:{SCHEMA_PATH}", check=False)
    if result.returncode != 0:
        return {
            "status": "NOT_PRESENT", "validation": "DEFERRED",
            "reason": "schema is a later-phase artifact and is absent from the selected source commit",
            "path": SCHEMA_PATH,
        }
    try:
        raw = git(root, "show", f"{commit}:{SCHEMA_PATH}").stdout
        schema = json.loads(raw.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError, AssessmentError) as exc:
        raise ConfigurationError(f"registry schema is unreadable or invalid JSON: {exc}") from exc
    if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ConfigurationError("registry schema must declare JSON Schema Draft 2020-12")
    return {
        "status": "PRESENT", "validation": "STRUCTURE_CHECKED",
        "reason": "schema is present and declares JSON Schema Draft 2020-12",
        "path": SCHEMA_PATH,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-tree", required=True)
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report", choices=("json",), required=True)
    parser.add_argument("--root", default=".", help="Git repository root (default: current directory)")
    parser.add_argument(
        "--cells-csv", default=None,
        help="Optional external evidence cross-check; never read unless explicitly supplied",
    )
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")

    if not args.dry_run:
        print("CONFIGURATION ERROR: this implementation only supports --dry-run", file=sys.stderr)
        return 4
    if (
        not args.output or args.output.startswith("/") or "\\" in args.output
        or ".." in PurePosixPath(args.output).parts
    ):
        print("CONFIGURATION ERROR: --output must be a repository-relative path", file=sys.stderr)
        return 4

    try:
        commit, tree_oid = resolve_tree(args.root, args.source_tree)
        blobs = list_tree(args.root, tree_oid)
        schema_report = validate_schema_presence(args.root, commit)
        inventory = load_inventory(args.root, args.inventory)
        manifests, discovery_failures = discover_manifests(args.root, blobs)
        entries = validate_inventory(
            inventory, manifests, discovery_failures, args.source_tree, commit,
        )
        if discovery_failures:
            raise AssessmentError(
                "one or more manifests could not be read or have a resolvable identity: "
                + json.dumps(discovery_failures, ensure_ascii=True)
            )

        by_id: dict[str, Manifest] = {}
        for manifest in manifests:
            work_item_id, _, _ = extract_identity(manifest.document)
            if work_item_id is None:
                raise AssessmentError(f"unresolved identity: {manifest.path}")
            if work_item_id in by_id:
                raise AssessmentError(f"duplicate resolved manifest identity: {work_item_id}")
            by_id[work_item_id] = manifest
        if len(by_id) != 140:
            raise AssessmentError(f"expected 140 resolvable manifests, found {len(by_id)}")

        item_results = []
        state_counts: Counter[str] = Counter()
        prompt_sha_pass = 0
        prompt_sha_fail = 0
        affected_field_count = 0

        for work_item_id in sorted(entries):
            entry = entries[work_item_id]
            manifest = by_id.get(work_item_id)
            if manifest is None:
                raise AssessmentError(f"inventory item has no manifest: {work_item_id}")
            if entry["source_manifest"] != manifest.path:
                raise AssessmentError(
                    f"inventory source_manifest does not match resolved manifest for "
                    f"{work_item_id}: {entry['source_manifest']!r} != {manifest.path!r}"
                )
            try:
                text = raw_text(manifest.blob)
                truncations = scalar_truncations(manifest.blob.data, manifest.path)
            except UnicodeDecodeError as exc:
                raise AssessmentError(f"manifest is not UTF-8: {manifest.path}") from exc

            field_results = {}
            for field in FIELD_NAMES:
                try:
                    result = assess_field(
                        field, manifest, text, blobs, args.root, commit,
                    )
                    result = apply_truncation_policy(result, truncations)
                except (AssessmentError, UnicodeDecodeError) as exc:
                    result = state_result(
                        "UNCONFIRMED", None, [],
                        f"field assessment failed closed: {exc}",
                    )
                field_results[field] = result
                state_counts[result["state"]] += 1
                if result.get("truncation_evidence"):
                    affected_field_count += 1
                if field == "prompt_sha256":
                    if result["state"] == "KNOWN":
                        prompt_sha_pass += 1
                    elif result["state"] == "UNCONFIRMED":
                        prompt_sha_fail += 1

            item_results.append({
                "work_item_id": work_item_id,
                "source_manifest": manifest.path,
                "migration_state": entry["migration_state"],
                "registry_path": entry.get("registry_path"),
                "fields": field_results,
            })

        total_cells = len(item_results) * len(FIELD_NAMES)
        if total_cells != 1680:
            raise AssessmentError(f"expected 1680 field cells, found {total_cells}")

        report = {
            "source_tree": commit,
            "source_tree_oid": tree_oid,
            "inventory_path": args.inventory,
            "inventory_source": "current_working_tree",
            "schema": schema_report,
            "summary": {
                "items": len(item_results),
                "fields_per_item": len(FIELD_NAMES),
                "field_cells": total_cells,
                "field_state_counts": dict(sorted(state_counts.items())),
                "truncation_affected_field_count": affected_field_count,
                "truncation_detection_semantics": (
                    "Count of assessed field cells downgraded to UNCONFIRMED because "
                    "their source YAML scalar is a plain scalar followed by an inline "
                    "whitespace-# tail. Detection uses raw Git blob bytes and YAML "
                    "node scalar style/boundaries. This is not a line count."
                ),
                "prompt_sha256_validation_passed": prompt_sha_pass,
                "prompt_sha256_validation_failed": prompt_sha_fail,
            },
            "items": item_results,
        }

        print(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2))
        print(
            f"migration dry-run completed: items={len(item_results)} "
            f"field_cells={total_cells} "
            f"prompt_sha256_pass={prompt_sha_pass} "
            f"prompt_sha256_fail={prompt_sha_fail} "
            f"schema={schema_report['status']}/{schema_report['validation']}",
            file=sys.stderr,
        )
        return 0

    except ConfigurationError as exc:
        print(f"CONFIGURATION ERROR: {exc}", file=sys.stderr)
        return 4
    except (AssessmentError, subprocess.SubprocessError) as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
