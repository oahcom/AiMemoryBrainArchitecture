#!/usr/bin/env python3
"""Verify the twelve Owner-A-authorized manifest blob pins.

This closes the manifest blob-integrity defect without expanding into general
path/digest inference. Only the explicitly authorized field identities are
applicable. All other digest fields, path fields, prompt hashes and historical
pathless declarations are deliberately outside this gate.

Deliberate ceiling: exactly 12 authorized field identities. Adding another
identity requires an explicit Owner A scope ruling and a corresponding
baseline change.

All referenced bytes are read from Git HEAD, never from the working tree.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import yaml


# (manifest path, digest field path, sibling path field)
#
# This is a closed authorization table, not a list of naming conventions.
# Do not infer additional pairs from YAML key names.
AUTHORIZED_PINS = (
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "baseline_and_source_evidence.authored_indexes[0].root_blob",
        "root",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "baseline_and_source_evidence.authored_indexes[0].en_mirror_blob",
        "en_mirror",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "baseline_and_source_evidence.authored_indexes[0].zh_cn_mirror_blob",
        "zh_cn_mirror",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "baseline_and_source_evidence.authored_indexes[1].root_blob",
        "root",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "baseline_and_source_evidence.authored_indexes[1].en_mirror_blob",
        "en_mirror",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "baseline_and_source_evidence.authored_indexes[1].zh_cn_mirror_blob",
        "zh_cn_mirror",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "related_evidence[0].blob",
        "path",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "related_evidence[0].en_mirror_blob",
        "en_mirror",
    ),
    (
        "14-ai-development/work-items/AID-2026-100/manifest.yaml",
        "related_evidence[0].zh_cn_mirror_blob",
        "zh_cn_mirror",
    ),
    (
        "14-ai-development/work-items/AID-2026-150/manifest.yaml",
        "source.files[0].blob",
        "path",
    ),
    (
        "14-ai-development/work-items/AID-2026-150/manifest.yaml",
        "source.files[1].blob",
        "path",
    ),
    (
        "14-ai-development/work-items/AID-2026-150/manifest.yaml",
        "source.files[2].blob",
        "path",
    ),
)

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")


class CheckerError(Exception):
    """A candidate tree or manifest could not be inspected."""


def git(root: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise CheckerError(detail or "Git command failed")
    return proc.stdout


def tree_bytes(root: Path, repository_path: str) -> bytes | None:
    """Return a regular Git-tree blob's bytes, or None if it is absent."""
    pure = PurePosixPath(repository_path)
    if (
        pure.is_absolute()
        or not pure.parts
        or any(part in ("", ".", "..") for part in pure.parts)
        or "\\" in repository_path
    ):
        return None

    spec = "HEAD:" + pure.as_posix()
    exists = subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if exists.returncode:
        return None

    kind = git(root, "cat-file", "-t", spec).decode("ascii").strip()
    if kind != "blob":
        return None
    return git(root, "cat-file", "blob", spec)


def parse_field_path(field_path: str) -> list[str | int]:
    """Parse the fixed dotted/indexed syntax used by the authorization table."""
    parts: list[str | int] = []
    for segment in field_path.split("."):
        match = re.fullmatch(r"([A-Za-z0-9_-]+)((?:\[\d+\])*)", segment)
        if not match:
            raise CheckerError("Invalid internal authorized field path")
        parts.append(match.group(1))
        parts.extend(int(n) for n in re.findall(r"\[(\d+)\]", match.group(2)))
    return parts


def locate_parent(document, field_path: str):
    current = document
    parts = parse_field_path(field_path)
    if not parts:
        return None, None

    for part in parts[:-1]:
        if isinstance(part, int):
            if not isinstance(current, list) or part >= len(current):
                return None, None
            current = current[part]
        else:
            if not isinstance(current, dict) or part not in current:
                return None, None
            current = current[part]

    return current, parts[-1]


def git_blob_id(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def emit_failure(
    manifest: str,
    field_path: str,
    referenced_path: str,
    declared: str,
    actual: str,
) -> None:
    print(
        f"::error::{manifest}#{field_path} -> {referenced_path} "
        f"(declared={declared}; actual={actual})"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repository_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args(argv)
    root = args.repository_root.resolve()

    if not (root / ".git").exists():
        print(
            "::error::Repository root is not a Git working tree; "
            "nothing was verified."
        )
        return 2

    manifest_paths = sorted({item[0] for item in AUTHORIZED_PINS})
    documents = {}

    try:
        for manifest in manifest_paths:
            raw = tree_bytes(root, manifest)
            if raw is None:
                print(
                    f"::error::{manifest} -> manifest unavailable in candidate "
                    "Git tree; nothing was verified."
                )
                return 2
            try:
                document = yaml.safe_load(raw.decode("utf-8"))
            except (UnicodeDecodeError, yaml.YAMLError) as exc:
                print(
                    f"::error::{manifest} -> manifest cannot be parsed "
                    f"({type(exc).__name__}); nothing was verified."
                )
                return 2
            if not isinstance(document, dict):
                print(
                    f"::error::{manifest} -> manifest root is not a mapping; "
                    "nothing was verified."
                )
                return 2
            documents[manifest] = document

        # The candidate identity is checked explicitly before inspecting pins.
        git(root, "rev-parse", "--verify", "HEAD^{tree}")

        failures = 0
        verified = 0

        for manifest, field_path, path_key in AUTHORIZED_PINS:
            document = documents[manifest]
            parent, digest_key = locate_parent(document, field_path)

            if not isinstance(parent, dict):
                emit_failure(
                    manifest, field_path, "MISSING_PATH_DECLARATION",
                    "UNRESOLVABLE", "MISSING_DECLARATION_MAPPING",
                )
                failures += 1
                continue

            declared_value = parent.get(digest_key)
            path_value = parent.get(path_key)

            if not isinstance(path_value, str) or not path_value.strip():
                emit_failure(
                    manifest, field_path, "MISSING_PATH_DECLARATION",
                    str(declared_value) if declared_value is not None else "MISSING",
                    "MISSING_PATH_DECLARATION",
                )
                failures += 1
                continue

            referenced_path = PurePosixPath(path_value).as_posix()

            if not isinstance(declared_value, str) or not HEX40.fullmatch(
                declared_value
            ):
                emit_failure(
                    manifest, field_path, referenced_path,
                    str(declared_value) if declared_value is not None else "MISSING",
                    "MISSING_OR_INVALID_GIT_BLOB_ID",
                )
                failures += 1
                continue

            actual_bytes = tree_bytes(root, referenced_path)
            if actual_bytes is None:
                emit_failure(
                    manifest, field_path, referenced_path,
                    declared_value, "MISSING",
                )
                failures += 1
                continue

            actual = git_blob_id(actual_bytes)
            verified += 1

            if actual.lower() != declared_value.lower():
                emit_failure(
                    manifest, field_path, referenced_path,
                    declared_value, actual,
                )
                failures += 1

        if failures:
            return 1

        print(f"All {verified} authorized manifest blob pins verified.")
        return 0

    except (CheckerError, OSError) as exc:
        print(
            f"::error::Manifest blob-pin inspection could not complete "
            f"({type(exc).__name__}); nothing was verified."
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
