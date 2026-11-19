#!/usr/bin/env python3
"""Additive, backup-first YAML status migration. Requires PyYAML; dry-run is default."""
import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

import yaml


class UniqueKeySafeLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate keys at every mapping depth."""


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
                "unhashable mapping key", key_node.start_mark,
            ) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


PHASES = {
    "PROPOSED": "INTAKE", "ANALYZED": "INTAKE", "PROMPT_READY": "INTAKE",
    "READY": "READY", "IN_PROGRESS": "ACTIVE", "IMPLEMENTED": "ACTIVE",
    "VERIFIED": "VALIDATION", "REVIEWED": "VALIDATION",
    "INTEGRATION_READY": "VALIDATION", "ACCEPTED": "ACCEPTANCE",
    "MERGED": "COMPLETE", "CLOSED": "COMPLETE",
}
GATES = ("verified", "independent_review", "integration",
         "owner_acceptance", "merge", "closeout")


def _load(raw):
    return yaml.load(raw, Loader=UniqueKeySafeLoader)


def _serialize_lifecycle_preserving_source(raw, lifecycle):
    """Append only the new top-level block; preserve all existing bytes/comments."""
    block = yaml.safe_dump({"lifecycle": lifecycle}, allow_unicode=True,
                           sort_keys=False, width=1000).encode("utf-8")
    lines = raw.splitlines(keepends=True)
    # YAML's explicit document-end marker must remain the final document token.
    marker_index = next((i for i, line in enumerate(lines)
                         if line.strip() == b"..."), None)
    if marker_index is not None:
        prefix = b"".join(lines[:marker_index])
        suffix = b"".join(lines[marker_index:])
        return prefix + (b"" if prefix.endswith(b"\n") else b"\n") + block + suffix
    separator = b"" if raw.endswith(b"\n") or not raw else b"\n"
    return raw + separator + block


def run(path, apply=False, rollback=False):
    path = Path(path)
    backup = path.with_name(path.name + ".pre-status-migration.bak")
    temporary = path.with_name(path.name + ".tmp-status-migration")
    digest_file = path.with_name(path.name + ".post-status-migration.sha256")
    if rollback:
        if not backup.is_file():
            raise ValueError("byte-for-byte backup missing")
        if not digest_file.is_file():
            raise ValueError("post-migration SHA-256 record missing; refusing rollback")
        expected = digest_file.read_text(encoding="ascii").strip()
        current = hashlib.sha256(path.read_bytes()).hexdigest()
        if not expected or current != expected:
            raise ValueError("post-migration file changed; refusing rollback")
        restore_tmp = path.with_name(path.name + ".tmp-status-rollback")
        if restore_tmp.exists():
            raise ValueError("rollback temporary output already exists")
        shutil.copy2(backup, restore_tmp)
        os.replace(restore_tmp, path)
        return {"result": "ROLLED_BACK", "path": str(path)}

    raw = path.read_bytes()
    data = _load(raw)
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")
    source = data.get("status")
    if not isinstance(source, str) or source not in PHASES:
        raise ValueError(f"unknown/ambiguous status; exact canonical value required: {source!r}")
    phase = PHASES[source]
    if "lifecycle" in data:
        lifecycle = data["lifecycle"]
        if (isinstance(lifecycle, dict) and lifecycle.get("source_status") == source
                and lifecycle.get("phase") == phase):
            return {"result": "ALREADY_MIGRATED", "path": str(path), "phase": phase}
        raise ValueError("conflicting lifecycle metadata; refusing overwrite")
    existing_markers = data.get("markers", {})
    if not isinstance(existing_markers, dict):
        raise ValueError("existing markers must be a mapping")
    markers = dict(existing_markers)
    for marker in ("blocked", "rejected"):
        if marker in data:
            markers[marker] = data[marker]
    lifecycle = {
        "phase": phase, "source_status": source,
        "gates": {gate: {"status": "NOT_RECORDED"} for gate in GATES},
        "markers": markers,
    }
    if not apply:
        return {"result": "WOULD_MIGRATE", "path": str(path), "phase": phase}
    if backup.exists() or digest_file.exists():
        raise ValueError("backup or migration digest already exists; refusing overwrite")
    if temporary.exists():
        raise ValueError("temporary output already exists; refusing overwrite")
    shutil.copy2(path, backup)
    try:
        serialized = _serialize_lifecycle_preserving_source(raw, lifecycle)
        with temporary.open("wb") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        digest_tmp = digest_file.with_suffix(digest_file.suffix + ".tmp")
        with digest_tmp.open("w", encoding="ascii", newline="\n") as stream:
            stream.write(digest + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(digest_tmp, digest_file)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise
    return {"result": "MIGRATED", "path": str(path), "phase": phase,
            "backup": str(backup), "post_migration_sha256": digest}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    failed = 0
    for name in args.paths:
        try:
            print(json.dumps(run(name, apply=args.apply, rollback=args.rollback), ensure_ascii=False))
        except Exception as error:
            failed += 1
            print(json.dumps({"result": "BLOCKED", "path": name, "error": str(error)}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
