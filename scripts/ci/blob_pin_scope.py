#!/usr/bin/env python3
# scripts/ci/blob_pin_scope.py
"""Derive and resolve the Git scope for a manifest blob pin."""
from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping


HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")


class ScopeError(Exception):
    """Base class for blob-pin scope errors."""


class NoScope(ScopeError):
    """No commit or usable registered locator sibling determines a scope."""


class PathMissing(ScopeError):
    """The selected, readable tree does not contain the declared path."""


class Unresolved(ScopeError):
    """The selected Git tree or object cannot be read or resolved."""


class ScopeUnresolvable(ScopeError):
    """The declared scope or locator is malformed or unsafe."""


@dataclass(frozen=True)
class Scope:
    kind: str
    commit_sha: str | None = None
    content_ref: str | None = None


def _pin_stem(key: str) -> str:
    """Remove the recognized digest/count suffix from a pin field."""
    for suffix in (
        "_blob_sha256",
        "_blob_sha",
        "_blob",
        "_sha256",
        "_sha",
        "_bytes",
    ):
        if key.endswith(suffix):
            return key[:-len(suffix)]
    return key


def _sibling_commit_keys(key: str) -> tuple[str, ...]:
    stem = _pin_stem(key)
    return (f"{stem}_commit_sha", f"{stem}_commit")


def _sibling_path_keys(key: str) -> tuple[str, ...]:
    """Built-in fallback for callers that do not pass registry locator keys."""
    stem = _pin_stem(key)

    # Explicit known shapes where the locator is the stem itself.
    if key.endswith("_blob"):
        return (stem, f"{stem}_path", f"{stem}_file")

    if key == "blob":
        return ("path",)

    return (
        f"{stem}_path",
        f"{stem}_file",
        f"{stem}_snapshot_file",
        f"{stem}_content_path",
        f"{stem}_content_file",
        "snapshot_file",
        "file",
        "path",
    )


def derive_scope(
    node: Mapping,
    key: str,
    manifest_dir: str,
    locator_keys: tuple[str, ...] | None = None,
) -> Scope:
    """Derive scope using registry locator_keys as the sole locator authority.

    Commit siblings take precedence. Otherwise, the presence of a valid
    locator sibling selects candidate scope. No locator sibling is NO_SCOPE;
    a present but malformed locator or commit is SCOPE_UNRESOLVABLE.
    """
    if not isinstance(node, Mapping):
        raise NoScope("pin node is not a mapping")
    if not isinstance(key, str) or not key:
        raise NoScope("pin field key is missing")

    if locator_keys is None:
        path_keys = _sibling_path_keys(key)
    else:
        path_keys = tuple(locator_keys)

    if not path_keys:
        raise NoScope(f"pin field {key!r} has no registered locator keys")

    commit_key = next(
        (candidate for candidate in _sibling_commit_keys(key) if candidate in node),
        None,
    )
    if commit_key is not None:
        commit_value = node[commit_key]
        if isinstance(commit_value, str) and HEX40.fullmatch(commit_value):
            return Scope(
                kind="commit",
                commit_sha=commit_value.lower(),
                content_ref=manifest_dir,
            )
        # A present but non-SHA commit sibling is not a commit scope. The
        # mechanical order falls through to the path sibling; a malformed
        # commit value must not turn a candidate pin into INCOMPLETE.

    present_keys = [candidate for candidate in path_keys if candidate in node]
    if not present_keys:
        raise NoScope(
            f"no locator sibling for pin field {key!r}; "
            f"registry keys={path_keys!r}"
        )

    # Presence of a path sibling establishes candidate scope even when the
    # value is malformed or ambiguous. Locator selection reports that case
    # as UNCLASSIFIED (LOCATOR_NOT_A_PATH), never as INCOMPLETE.
    return Scope(
        kind="candidate",
        content_ref=manifest_dir,
    )


def _git_bytes(repo_root: Path, *args: str) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise Unresolved(f"cannot execute git: {exc}") from exc

    if proc.returncode:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise Unresolved(
            detail or f"git {' '.join(args)} failed ({proc.returncode})"
        )
    return proc.stdout


def _repository_path(scope: Scope, locator: str, repo_root: Path) -> str:
    """Resolve a locator relative to repository root.

    Only a slash-free locator may fall back to manifest_dir/locator, and only
    when the root-relative path does not exist in the selected tree.
    The existence check is against the selected tree, not the worktree.
    """
    if not isinstance(locator, str) or not locator.strip():
        raise ScopeUnresolvable("locator must be a nonempty string")

    path = PurePosixPath(locator)
    if path.is_absolute() or ".." in path.parts:
        raise ScopeUnresolvable(f"unsafe repository locator: {locator!r}")

    return path.as_posix()


def _treeish(scope: Scope) -> str:
    if scope.kind == "candidate":
        return "HEAD"

    if scope.kind == "commit":
        if (
            not isinstance(scope.commit_sha, str)
            or not HEX40.fullmatch(scope.commit_sha)
        ):
            raise ScopeUnresolvable(
                "commit scope does not contain a full 40-character commit SHA"
            )
        return scope.commit_sha.lower()

    raise ScopeUnresolvable(f"unsupported scope kind: {scope.kind!r}")


def _tree_path_exists(repo_root: Path, treeish: str, path: str) -> bool:
    """Return whether path is an entry in the selected tree.

    The caller has already established that treeish resolves to a tree.
    """
    output = _git_bytes(
        repo_root,
        "ls-tree",
        "-z",
        "--full-tree",
        treeish,
        "--",
        path,
    )
    if not output:
        return False

    for entry in output.split(b"\0"):
        if not entry:
            continue
        try:
            metadata, raw_path = entry.split(b"\t", 1)
            _mode, object_type, _oid = metadata.decode("ascii").split()
            found_path = raw_path.decode("utf-8", "surrogateescape")
        except (ValueError, UnicodeError) as exc:
            raise Unresolved(f"malformed git ls-tree entry: {entry!r}") from exc

        if found_path == path and object_type == "blob":
            return True

    return False


def _manifest_fallback_path(
    scope: Scope,
    locator: str,
    repo_root: Path,
    treeish: str,
) -> str:
    """Apply the manifest-relative fallback only for slash-free locators."""
    root_relative = _repository_path(scope, locator, repo_root)
    if "/" in root_relative or _tree_path_exists(repo_root, treeish, root_relative):
        return root_relative

    if not scope.content_ref:
        return root_relative

    manifest_dir = PurePosixPath(scope.content_ref)
    if (
        manifest_dir.is_absolute()
        or ".." in manifest_dir.parts
        or not manifest_dir.parts
    ):
        raise ScopeUnresolvable(
            f"unsafe manifest directory: {scope.content_ref!r}"
        )

    fallback = (manifest_dir / root_relative).as_posix()
    if fallback in ("", ".") or fallback.startswith("../"):
        raise ScopeUnresolvable(
            f"manifest-relative locator is unsafe: {fallback!r}"
        )
    return fallback


def resolve_bytes(repo_root: Path, scope: Scope, locator: str) -> bytes:
    """Read the locator's raw bytes from the exact selected Git tree.

    Resolution order:
      1. prove treeish resolves to a tree;
      2. look for the root-relative path, then optional manifest fallback;
      3. classify absent path as PathMissing;
      4. read the blob; an unavailable object is Unresolved.
    """
    repo_root = Path(repo_root).resolve()
    treeish = _treeish(scope)

    # rev-parse verifies the selected commit/tree before path lookup.
    tree_output = _git_bytes(
        repo_root,
        "rev-parse",
        "--verify",
        "--end-of-options",
        f"{treeish}^{{tree}}",
    )
    tree_oid = tree_output.decode("ascii", "replace").strip()
    if not HEX40.fullmatch(tree_oid):
        raise Unresolved(
            f"treeish {treeish!r} did not resolve to a full tree object ID"
        )

    path = _manifest_fallback_path(
        scope,
        locator,
        repo_root,
        treeish,
    )

    if not _tree_path_exists(repo_root, treeish, path):
        raise PathMissing(
            f"path {path!r} is absent from selected {scope.kind} tree {treeish}"
        )

    try:
        return _git_bytes(
            repo_root,
            "cat-file",
            "blob",
            f"{treeish}:{path}",
        )
    except Unresolved as exc:
        raise Unresolved(
            f"tree contains {path!r}, but its blob object cannot be read: {exc}"
        ) from exc


def digest_of(algorithm: str, data: bytes) -> str:
    """Compute digests over raw bytes; no newline or content normalization."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()

    if algorithm == "git-blob-sha1":
        header = b"blob " + str(len(data)).encode("ascii") + b"\0"
        return hashlib.sha1(header + data).hexdigest()

    if algorithm == "byte-length":
        return str(len(data))

    raise ValueError(f"unsupported digest algorithm: {algorithm!r}")
