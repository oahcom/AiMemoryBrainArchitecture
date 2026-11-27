#!/usr/bin/env python3
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
    """The pin has no mechanically determinable scope."""


class ScopeUnresolvable(ScopeError):
    """The declared scope exists, but its target cannot be resolved."""


@dataclass(frozen=True)
class Scope:
    kind: str
    commit_sha: str | None = None
    content_ref: str | None = None


def _pin_stem(key: str) -> str:
    """Return the name shared by a pin field and its sibling locator fields."""
    for suffix in (
        "_blob_sha256",
        "_blob_sha",
        "_blob",
        "_sha256",
        "_sha",
        "_bytes",
    ):
        if key.endswith(suffix):
            return key[: -len(suffix)]
    return key


def _sibling_commit_keys(key: str) -> tuple[str, ...]:
    stem = _pin_stem(key)
    return (f"{stem}_commit_sha", f"{stem}_commit")


def _sibling_path_keys(key: str) -> tuple[str, ...]:
    if key == "blob":
        return ("path",)
    stem = _pin_stem(key)
    return (f"{stem}_path", f"{stem}_file")


def derive_scope(node: Mapping, key: str, manifest_dir: str) -> Scope:
    """Derive scope from sibling fields only; raise NoScope if absent.

    `content_ref` carries the manifest directory so resolve_bytes can
    resolve a relative locator against the manifest's directory.
    """
    if not isinstance(node, Mapping):
        raise NoScope("pin node is not a mapping")
    if not isinstance(key, str) or not key:
        raise NoScope("pin key is missing")

    commit_key = next(
        (candidate for candidate in _sibling_commit_keys(key)
         if candidate in node),
        None,
    )
    if commit_key is not None:
        commit_value = node[commit_key]
        if not isinstance(commit_value, str) or not HEX40.fullmatch(commit_value):
            raise NoScope(
                f"sibling commit field {commit_key!r} is not a full 40-digit SHA"
            )
        return Scope(
            kind="commit",
            commit_sha=commit_value.lower(),
            content_ref=manifest_dir,
        )

    path_key = next(
        (candidate for candidate in _sibling_path_keys(key)
         if candidate in node),
        None,
    )
    if path_key is None:
        raise NoScope(f"no sibling commit or path for pin field {key!r}")

    path_value = node[path_key]
    if not isinstance(path_value, str) or not path_value.strip():
        raise NoScope(f"sibling path field {path_key!r} is not a nonempty string")

    return Scope(kind="candidate", content_ref=manifest_dir)


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
        raise ScopeUnresolvable(f"cannot execute git: {exc}") from exc

    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise ScopeUnresolvable(
            detail or f"git {' '.join(args)} failed ({proc.returncode})"
        )
    return proc.stdout


def _repository_path(scope: Scope, locator: str) -> str:
    if not isinstance(locator, str) or not locator.strip():
        raise ScopeUnresolvable("locator must be a nonempty string")

    path = PurePosixPath(locator)
    if path.is_absolute() or ".." in path.parts:
        raise ScopeUnresolvable(f"unsafe repository locator: {locator!r}")

    if scope.content_ref:
        manifest_dir = PurePosixPath(scope.content_ref)
        if manifest_dir.is_absolute() or ".." in manifest_dir.parts:
            raise ScopeUnresolvable(
                f"unsafe manifest directory: {scope.content_ref!r}"
            )
        path = manifest_dir / path

    normalized = path.as_posix()
    if normalized in ("", "."):
        raise ScopeUnresolvable("locator resolves to an empty repository path")
    return normalized


def resolve_bytes(repo_root: Path, scope: Scope, locator: str) -> bytes:
    """Read locator bytes from the exact tree selected by scope."""
    if scope.kind == "content":
        raise ScopeUnresolvable("content scope has no resolver")

    if scope.kind not in ("candidate", "commit"):
        raise ScopeUnresolvable(f"unsupported scope kind: {scope.kind!r}")

    path = _repository_path(scope, locator)

    if scope.kind == "candidate":
        # The candidate is the checked-out candidate tree at repo_root/HEAD.
        treeish = "HEAD"
    else:
        commit = scope.commit_sha
        if not isinstance(commit, str) or not HEX40.fullmatch(commit):
            raise ScopeUnresolvable("commit scope has no full 40-digit commit SHA")
        treeish = commit.lower()

    return _git_bytes(repo_root, "cat-file", "blob", f"{treeish}:{path}")


def digest_of(algorithm: str, data: bytes) -> str:
    """Compute a supported digest or byte count."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    if algorithm == "git-blob-sha1":
        header = b"blob " + str(len(data)).encode("ascii") + b"\0"
        return hashlib.sha1(header + data).hexdigest()
    if algorithm == "sha256":
        normalized = data.replace(b"\r\n", b"\n")
        return hashlib.sha256(normalized).hexdigest()
    if algorithm == "byte-length":
        return str(len(data))

    raise ValueError(f"unsupported digest algorithm: {algorithm!r}")
