#!/usr/bin/env python3
"""Additive, backup-first YAML status migration. Requires PyYAML; dry-run is default."""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import yaml

PHASES = {
    "PROPOSED": "INTAKE",
    "ANALYZED": "INTAKE",
    "PROMPT_READY": "INTAKE",
    "READY": "READY",
    "IN_PROGRESS": "ACTIVE",
    "IMPLEMENTED": "ACTIVE",
    "VERIFIED": "VALIDATION",
    "REVIEWED": "VALIDATION",
    "INTEGRATION_READY": "VALIDATION",
    "ACCEPTED": "ACCEPTANCE",
    "MERGED": "COMPLETE",
    "CLOSED": "COMPLETE",
}
GATES = (
    "verified",
    "independent_review",
    "integration",
    "owner_acceptance",
    "merge",
    "closeout",
)


def run(path, apply=False, rollback=False):
    path = Path(path)
    backup = path.with_name(path.name + ".pre-status-migration.bak")
    temporary = path.with_name(path.name + ".tmp-status-migration")

    if rollback:
        if not backup.is_file():
            raise ValueError("byte-for-byte backup missing")
        shutil.copy2(backup, path)
        return {"result": "ROLLED_BACK", "path": str(path)}

    raw = path.read_bytes()
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")

    # Exact matching is deliberate: suffixes, annotations and unknown values
    # must be reviewed, not silently interpreted as a canonical state.
    source = data.get("status")
    if not isinstance(source, str) or source not in PHASES:
        raise ValueError(
            f"unknown/ambiguous status; exact canonical value required: {source!r}"
        )
    phase = PHASES[source]

    if "lifecycle" in data:
        lifecycle = data["lifecycle"]
        if (
            isinstance(lifecycle, dict)
            and lifecycle.get("source_status") == source
            and lifecycle.get("phase") == phase
        ):
            return {
                "result": "ALREADY_MIGRATED",
                "path": str(path),
                "phase": phase,
            }
        raise ValueError("conflicting lifecycle metadata; refusing overwrite")

    existing_markers = data.get("markers", {})
    if not isinstance(existing_markers, dict):
        raise ValueError("existing markers must be a mapping")
    markers = dict(existing_markers)
    for marker in ("blocked", "rejected"):
        if marker in data:
            markers[marker] = data[marker]

    data["lifecycle"] = {
        "phase": phase,
        "source_status": source,
        "gates": {
            gate: {"status": "NOT_RECORDED"} for gate in GATES
        },
        "markers": markers,
    }

    if not apply:
        return {"result": "WOULD_MIGRATE", "path": str(path), "phase": phase}

    if backup.exists():
        raise ValueError("backup already exists; refusing overwrite")
    if temporary.exists():
        raise ValueError("temporary output already exists; refusing overwrite")

    # Preserve exact pre-migration bytes before writing. Atomic replacement
    # prevents a partially serialized manifest from replacing the source.
    shutil.copy2(path, backup)
    try:
        serialized = yaml.safe_dump(
            data, allow_unicode=True, sort_keys=False, width=1000
        ).encode("utf-8")
        with temporary.open("wb") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()

    return {
        "result": "MIGRATED",
        "path": str(path),
        "phase": phase,
        "backup": str(backup),
    }


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
            result = run(name, apply=args.apply, rollback=args.rollback)
            print(json.dumps(result, ensure_ascii=False))
        except Exception as error:
            failed += 1
            print(
                json.dumps(
                    {"result": "BLOCKED", "path": name, "error": str(error)},
                    ensure_ascii=False,
                )
            )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
