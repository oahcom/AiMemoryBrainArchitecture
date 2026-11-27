#!/usr/bin/env python3
"""Fail-closed verification of manifest blob and content declarations.

Exit status:
    0: all discovered declarations verified
    1: one or more ordinary violations
    2: one or more scope-unresolvable declarations
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Mapping

import yaml

from blob_pin_registry import FIELD_REGISTRY, PinSpec
from blob_pin_scope import (
    NoScope,
    Scope,
    ScopeUnresolvable,
    derive_scope,
    digest_of,
    resolve_bytes,
)


MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

FINDING_KINDS = frozenset({
    "MISMATCH",
    "PATH_MISSING",
    "UNCLASSIFIED",
    "NO_SCOPE",
    "SCOPE_UNRESOLVABLE",
})


@dataclass(frozen=True)
class Finding:
    """One stable, occurrence-scoped validation result."""

    kind: str
    manifest: str
    pin_id: str
    field_path: str
    scope: str
    locator: str

    # Diagnostic-only fields. Never include these in identity_line().
    declared: str = ""
    actual: str = ""
    reason: str = ""
    classification: str = "unknown"
    classification_basis: str = ""


@dataclass
class Verification:
    """Mutable aggregation for one complete manifest scan."""

    findings: list[Finding] = field(default_factory=list)
    pins: int = 0
    ok: int = 0
    mismatch: int = 0
    path_missing: int = 0
    unclassified: int = 0
    no_scope: int = 0
    scope_unresolvable: int = 0

    @property
    def exit_code(self) -> int:
        if self.scope_unresolvable:
            return 2
        if self.findings:
            return 1
        return 0


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def as_mapping(value):
    return value if isinstance(value, Mapping) else {}


def pin_id_for(field_path: str) -> str:
    """Produce a stable, manifest-local identifier from the structural path."""
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", field_path).strip("-")
    slug = slug[:72] or "pin"
    suffix = hashlib.sha256(field_path.encode("utf-8")).hexdigest()[:10]
    return f"{slug}-{suffix}"


def identity_line(finding: Finding) -> str:
    """Render only the stable occurrence identity, never digest diagnostics."""
    if finding.kind not in FINDING_KINDS:
        raise ValueError(f"unsupported finding kind: {finding.kind!r}")

    return (
        f"{finding.kind}"
        f" manifest={finding.manifest}"
        f" pin_id={finding.pin_id}"
        f" field={finding.field_path}"
        f" scope={finding.scope}"
        f" locator={finding.locator}"
    )


def _field_stem(key: str) -> str:
    """Remove recognized digest/count suffixes to find sibling evidence."""
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


def _sibling_content_locator_keys(key: str) -> tuple[str, ...]:
    """Return explicit content locator names associated with this occurrence."""
    stem = _field_stem(key)
    return (
        f"{stem}_content_path",
        f"{stem}_content_file",
        "content_path",
        "content_file",
    )


def _sibling_git_locator_keys(key: str) -> tuple[str, ...]:
    """Return ordinary Git-tree locator names associated with this occurrence."""
    stem = _field_stem(key)
    if key == "blob":
        return ("path",)
    return (
        f"{stem}_path",
        f"{stem}_file",
        "path",
    )


def _present_sibling_locators(
    node: Mapping,
    keys: tuple[str, ...],
) -> list[tuple[str, str]]:
    """Return only nonempty locators declared in this exact mapping."""
    found = []
    for key in keys:
        if key not in node:
            continue
        value = node[key]
        if nonempty(value):
            found.append((key, value))
    return found


def classify_declaration(node: Mapping, key: str) -> tuple[str, str]:
    """Classify the declared verification path using occurrence-local evidence.

    Returns:
        ("git-object", basis)
        ("content-digest", basis)
        ("unknown", basis)

    Neither the field name nor the digest length is sufficient evidence.
    Conflicting locator evidence is deliberately classified as unknown.
    """
    if not isinstance(node, Mapping):
        return "unknown", "PIN_NODE_NOT_MAPPING"

    content_locators = _present_sibling_locators(
        node, _sibling_content_locator_keys(key)
    )
    git_locators = _present_sibling_locators(
        node, _sibling_git_locator_keys(key)
    )

    # Explicit content locator evidence is stronger than digest shape.
    if content_locators and git_locators:
        content_names = {name for name, _ in content_locators}
        git_names = {name for name, _ in git_locators}
        if content_names.isdisjoint(git_names):
            return "unknown", "DECLARATION_KIND_AMBIGUOUS"

    if content_locators:
        return (
            "content-digest",
            "SIBLING_CONTENT_LOCATOR:" + ",".join(
                name for name, _ in content_locators
            ),
        )

    # A Git object declaration needs a locator belonging to this occurrence.
    # A sibling commit alone is not enough to establish the byte locator.
    if git_locators:
        return (
            "git-object",
            "SIBLING_GIT_LOCATOR:" + ",".join(
                name for name, _ in git_locators
            ),
        )

    return "unknown", "DECLARATION_KIND_AMBIGUOUS"


def _locator_for(
    node: Mapping,
    key: str,
    declaration_kind: str,
) -> str | None:
    if declaration_kind == "content-digest":
        candidates = _present_sibling_locators(
            node, _sibling_content_locator_keys(key)
        )
    elif declaration_kind == "git-object":
        candidates = _present_sibling_locators(
            node, _sibling_git_locator_keys(key)
        )
    else:
        return None

    # Multiple distinct locators for one declaration are ambiguous.
    values = {value for _, value in candidates}
    if len(values) != 1:
        return None
    return next(iter(values))


def _scope_label(scope: Scope | None) -> str:
    if scope is None:
        return "NO_SCOPE"
    return scope.kind


def _make_finding(
    *,
    kind: str,
    manifest: str,
    field_path: str,
    scope: Scope | None,
    locator: str | None,
    declared="",
    actual="",
    reason="",
    classification="unknown",
    classification_basis="",
) -> Finding:
    return Finding(
        kind=kind,
        manifest=manifest,
        pin_id=pin_id_for(field_path),
        field_path=field_path,
        scope=_scope_label(scope),
        locator=locator if locator is not None else "<not-declared>",
        declared=str(declared),
        actual=str(actual),
        reason=reason,
        classification=classification,
        classification_basis=classification_basis,
    )


def _valid_declaration(algorithm: str, declared) -> bool:
    if algorithm == "git-blob-sha1":
        return isinstance(declared, str) and bool(HEX40.fullmatch(declared))
    if algorithm == "sha256":
        return isinstance(declared, str) and bool(HEX64.fullmatch(declared))
    if algorithm == "byte-length":
        return (
            isinstance(declared, (str, int))
            and not isinstance(declared, bool)
            and bool(str(declared).strip())
            and str(declared).isdigit()
        )
    raise ValueError(f"unsupported pin algorithm: {algorithm!r}")


def _actual_digest(algorithm: str, data: bytes) -> str:
    return digest_of(algorithm, data)


def check_pin(
    node: Mapping,
    key: str,
    field_path: str,
    algorithm: str,
    manifest_dir: str,
    commit: str,
    *,
    manifest: str = "",
) -> Finding | None:
    """Validate one pin occurrence; return a finding or None when verified.

    Required order:
      1. derive the scope from this occurrence's mapping;
      2. classify the declaration's verification path;
      3. select this occurrence's locator;
      4. resolve bytes in the derived scope;
      5. validate declaration syntax and compare the digest.

    `commit` is retained in the public signature for handler compatibility.
    It is intentionally not used as a fallback scope.
    """
    if not isinstance(node, Mapping) or key not in node:
        return _make_finding(
            kind="UNCLASSIFIED",
            manifest=manifest,
            field_path=field_path,
            scope=None,
            locator=None,
            reason="PIN_OCCURRENCE_MISSING",
        )

    declared = node[key]

    # Scope derivation is mandatory and precedes object resolution.
    try:
        scope = derive_scope(node, key, manifest_dir)
    except NoScope as exc:
        return _make_finding(
            kind="NO_SCOPE",
            manifest=manifest,
            field_path=field_path,
            scope=None,
            locator=None,
            declared=declared,
            reason=str(exc),
        )

    declaration_kind, basis = classify_declaration(node, key)
    if declaration_kind == "unknown":
        return _make_finding(
            kind="UNCLASSIFIED",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=None,
            declared=declared,
            reason="DECLARATION_KIND_AMBIGUOUS",
            classification=declaration_kind,
            classification_basis=basis,
        )

    locator = _locator_for(node, key, declaration_kind)
    if locator is None:
        return _make_finding(
            kind="UNCLASSIFIED",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=None,
            declared=declared,
            reason="DECLARATION_LOCATOR_MISSING_OR_AMBIGUOUS",
            classification=declaration_kind,
            classification_basis=basis,
        )

    # Scope is already fixed. A missing target cannot turn it into NO_SCOPE.
    try:
        data = resolve_bytes(Path.cwd(), scope, locator)
    except ScopeUnresolvable as exc:
        return _make_finding(
            kind="SCOPE_UNRESOLVABLE",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            reason=str(exc),
            classification=declaration_kind,
            classification_basis=basis,
        )

    # Invalid syntax is an ordinary mismatch, not a scope failure.
    if not _valid_declaration(algorithm, declared):
        return _make_finding(
            kind="MISMATCH",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            actual=_actual_digest(algorithm, data),
            reason="INVALID_DECLARATION_FORMAT",
            classification=declaration_kind,
            classification_basis=basis,
        )

    actual = _actual_digest(algorithm, data)
    expected = str(declared).lower()

    if actual != expected:
        return _make_finding(
            kind="MISMATCH",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            actual=actual,
            reason="DIGEST_MISMATCH",
            classification=declaration_kind,
            classification_basis=basis,
        )

    return None


class Incomplete(Exception):
    """A required Git object or repository operation is unavailable."""


class Violation(Exception):
    """Repository or manifest content violates the checker contract."""


class Git:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()

    def _run(self, *args: str, label: str = "git operation") -> bytes:
        try:
            proc = subprocess.run(
                ["git", *args],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"{label}: cannot execute git: {exc}") from exc

        if proc.returncode != 0:
            detail = proc.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(
                f"{label}: {detail or f'git {' '.join(args)} failed ({proc.returncode})'}"
            )
        return proc.stdout

    def resolve_commit(self, ref: str, label: str) -> str:
        if not isinstance(ref, str) or not ref.strip():
            raise Incomplete(f"{label}: commit reference is empty")

        output = self._run(
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{ref}^{{commit}}",
            label=label,
        )
        resolved = output.decode("ascii", "replace").strip().lower()
        if not HEX40.fullmatch(resolved):
            raise Incomplete(
                f"{label}: reference {ref!r} did not resolve to a full commit SHA"
            )
        return resolved

    def object_bytes(self, commit: str, path: str, label: str) -> bytes:
        resolved = self.resolve_commit(commit, label)
        if (
            not isinstance(path, str)
            or not path
            or path.startswith("/")
            or ".." in PurePosixPath(path).parts
        ):
            raise Violation(f"{label}: unsafe repository path {path!r}")

        return self._run(
            "cat-file",
            "blob",
            f"{resolved}:{PurePosixPath(path).as_posix()}",
            label=f"{label} ({path})",
        )

    def _tree_entries(self, treeish: str, label: str) -> list[tuple[str, str, str]]:
        resolved = self.resolve_commit(treeish, label)
        output = self._run(
            "ls-tree",
            "-r",
            "--full-tree",
            resolved,
            label=label,
        )

        entries = []
        for raw_line in output.splitlines():
            try:
                metadata, raw_path = raw_line.split(b"\t", 1)
                mode, object_type, oid = metadata.decode("ascii").split()
                path = raw_path.decode("utf-8", "surrogateescape")
            except (ValueError, UnicodeError) as exc:
                raise Incomplete(
                    f"{label}: malformed git ls-tree entry: {raw_line!r}"
                ) from exc

            if object_type == "blob":
                entries.append((oid.lower(), path, mode))

        return entries

    def paths_by_blob_oid(self, *args: str) -> list[str]:
        """Find paths for a blob OID.

        Accepts paths_by_blob_oid(oid) to search HEAD, or the
        occurrence-handler form paths_by_blob_oid(commit, oid, label).
        """
        if len(args) == 1:
            treeish, oid, label = "HEAD", args[0], "blob OID lookup"
        elif len(args) == 3:
            treeish, oid, label = args
        else:
            raise TypeError(
                "paths_by_blob_oid expects (oid) or (commit, oid, label)"
            )

        if not isinstance(oid, str) or not HEX40.fullmatch(oid):
            return []

        return sorted(
            path
            for found_oid, path, _mode in self._tree_entries(
                treeish,
                str(label),
            )
            if found_oid == oid.lower()
        )

    def paths_by_basename(self, *args: str) -> list[str]:
        """Find paths by basename in HEAD or in a specified commit tree."""
        if len(args) == 1:
            treeish, name, label = "HEAD", args[0], "basename lookup"
        elif len(args) == 3:
            treeish, name, label = args
        else:
            raise TypeError(
                "paths_by_basename expects (name) or (commit, name, label)"
            )

        if not isinstance(name, str) or not name:
            return []

        return sorted(
            path
            for _oid, path, _mode in self._tree_entries(
                treeish,
                str(label),
            )
            if PurePosixPath(path).name == name
        )


def discover_manifests(git: Git, commit: str) -> list[str]:
    """Return work-item manifest paths in deterministic order."""
    resolved = git.resolve_commit(commit, "manifest discovery")
    output = git._run(
        "ls-tree",
        "-r",
        "--name-only",
        "--full-tree",
        resolved,
        "--",
        "14-ai-development/work-items",
        label="manifest discovery",
    )

    prefix = PurePosixPath("14-ai-development/work-items")
    found = set()

    for raw_path in output.splitlines():
        path_text = raw_path.decode("utf-8", "surrogateescape")
        path = PurePosixPath(path_text)
        if (
            path.name == "manifest.yaml"
            and path.parent.parent == prefix
            and path.parent.name not in ("", ".", "..")
        ):
            found.add(path.as_posix())

    return sorted(found)


def verify(root: Path, commit: str, verbose: bool = True) -> int:
    git_root = root.resolve()
    git = Git(git_root)
    commit = git.resolve_commit(commit, "--commit")
    manifests = discover_manifests(git, commit)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {commit}")

    result = Verification()
    problems: list[str] = []
    seen: set[tuple[str, str]] = set()

    def add_finding(
        kind: str,
        manifest_path: str,
        field_path: str,
        *,
        node=None,
        key=None,
        scope="none",
        locator="none",
        reason="",
        declared="",
        actual="",
    ) -> None:
        occurrence = (manifest_path, field_path)
        if occurrence in seen:
            return
        seen.add(occurrence)
        finding = Finding(
            kind=kind,
            manifest=manifest_path,
            pin_id=pin_id_for(field_path),
            field_path=field_path,
            scope=scope,
            locator=locator,
            reason=reason,
            declared=str(declared),
            actual=str(actual),
        )
        result.findings.append(finding)
        if kind == "MISMATCH":
            result.mismatch += 1
        elif kind == "PATH_MISSING":
            result.path_missing += 1
        elif kind == "UNCLASSIFIED":
            result.unclassified += 1
        elif kind == "NO_SCOPE":
            result.no_scope += 1
        elif kind == "SCOPE_UNRESOLVABLE":
            result.scope_unresolvable += 1
        if verbose:
            problems.append(identity_line(finding))

    def record_occurrence(
        manifest_path: str,
        manifest_dir: str,
        field_path: str,
        node,
        key,
        algorithm: str,
        candidate_commit: str,
    ) -> None:
        occurrence = (manifest_path, field_path)
        if occurrence in seen:
            return
        result.pins += 1

        if not isinstance(node, Mapping) or key not in node:
            add_finding(
                "UNCLASSIFIED",
                manifest_path,
                field_path,
                reason="DECLARATION_OCCURRENCE_MISSING",
            )
            return

        declaration = node[key]
        if algorithm == "auto":
            classification, basis = classify_declaration(node, key)
            if classification == "unknown":
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    field_path,
                    node=node,
                    key=key,
                    reason=basis or "DECLARATION_KIND_AMBIGUOUS",
                    declared=declaration,
                )
                return
            algorithm = (
                "git-blob-sha1"
                if classification == "git-object"
                else "sha256"
            )

        if algorithm == "git":
            algorithm = "git-blob-sha1"
        elif algorithm == "bytes":
            algorithm = "byte-length"

        try:
            finding = check_pin(
                node,
                key,
                field_path,
                algorithm,
                manifest_dir,
                candidate_commit,
                manifest=manifest_path,
            )
        except NoScope as exc:
            add_finding(
                "NO_SCOPE",
                manifest_path,
                field_path,
                node=node,
                key=key,
                reason=str(exc),
                declared=declaration,
            )
            return
        except ScopeUnresolvable as exc:
            add_finding(
                "SCOPE_UNRESOLVABLE",
                manifest_path,
                field_path,
                node=node,
                key=key,
                reason=str(exc),
                declared=declaration,
            )
            return
        except Exception as exc:
            add_finding(
                "SCOPE_UNRESOLVABLE",
                manifest_path,
                field_path,
                node=node,
                key=key,
                reason=f"CHECK_PIN_EXCEPTION:{type(exc).__name__}:{exc}",
                declared=declaration,
            )
            return

        if finding is None:
            result.ok += 1
            return

        if finding.kind == "PATH_MISSING":
            add_finding(
                "PATH_MISSING",
                manifest_path,
                field_path,
                node=node,
                key=key,
                scope=finding.scope,
                locator=finding.locator,
                reason=finding.reason,
                declared=finding.declared,
                actual=finding.actual,
            )
        elif finding.kind == "MISMATCH":
            add_finding(
                "MISMATCH",
                manifest_path,
                field_path,
                node=node,
                key=key,
                scope=finding.scope,
                locator=finding.locator,
                reason=finding.reason,
                declared=finding.declared,
                actual=finding.actual,
            )
        elif finding.kind in FINDING_KINDS:
            add_finding(
                finding.kind,
                manifest_path,
                field_path,
                node=node,
                key=key,
                scope=finding.scope,
                locator=finding.locator,
                reason=finding.reason,
                declared=finding.declared,
                actual=finding.actual,
            )
        else:
            add_finding(
                "UNCLASSIFIED",
                manifest_path,
                field_path,
                node=node,
                key=key,
                reason=f"UNKNOWN_CHECK_RESULT:{finding.kind!r}",
                declared=declaration,
            )

    def record_direct(
        manifest_path: str,
        manifest_dir: str,
        field_path: str,
        node: Mapping,
        key: str,
        locator_key: str,
        algorithm: str,
        candidate_commit: str,
    ) -> None:
        if key not in node:
            return
        if locator_key not in node:
            record_occurrence(
                manifest_path,
                manifest_dir,
                field_path,
                node,
                key,
                algorithm,
                candidate_commit,
            )
            return

        locator_value = node.get(locator_key)
        if not isinstance(locator_value, str) or not locator_value.strip():
            record_occurrence(
                manifest_path,
                manifest_dir,
                field_path,
                node,
                key,
                algorithm,
                candidate_commit,
            )
            return

        record_occurrence(
            manifest_path,
            manifest_dir,
            field_path,
            node,
            key,
            algorithm,
            candidate_commit,
        )

    def record_blob_oid(
        manifest_path: str,
        manifest_dir: str,
        field_path: str,
        node: Mapping,
        key: str,
        candidate_commits,
    ) -> None:
        if isinstance(candidate_commits, str):
            candidate_commits = [candidate_commits]
        if not isinstance(candidate_commits, (list, tuple)):
            candidate_commits = []

        if key not in node:
            return

        if not isinstance(node.get(key), str) or not HEX40.fullmatch(node[key]):
            record_occurrence(
                manifest_path,
                manifest_dir,
                field_path,
                node,
                key,
                "git-blob-sha1",
                commit,
            )
            return

        # Locator discovery is occurrence-local. A unique path may be used
        # only for this declaration and only in one of its declared trees.
        matches = []
        for source_commit in candidate_commits:
            if not isinstance(source_commit, str) or not source_commit.strip():
                continue
            try:
                matches.extend(
                    (source_commit, path)
                    for path in git.paths_by_blob_oid(
                        source_commit,
                        node[key],
                        field_path,
                    )
                )
            except Incomplete:
                continue

        unique = {(source_ref, path) for source_ref, path in matches}
        if len(unique) == 1:
            source_ref, path = next(iter(unique))
            # The occurrence has no sibling locator in the original mapping.
            # Use an occurrence-local copy so derive_scope sees only this
            # declaration's mechanically discovered locator and scope.
            synthetic = dict(node)
            synthetic["path"] = path
            synthetic["path_commit_sha"] = source_ref
            record_occurrence(
                manifest_path,
                manifest_dir,
                field_path,
                synthetic,
                key,
                "git-blob-sha1",
                source_ref,
            )
        else:
            add_finding(
                "NO_SCOPE",
                manifest_path,
                field_path,
                node=node,
                key=key,
                reason=(
                    "BLOB_OID_LOCATOR_NOT_UNIQUE"
                    if len(unique) > 1
                    else "BLOB_OID_LOCATOR_NOT_FOUND"
                ),
                declared=node[key],
            )
            result.pins += 1

    def mapping(value):
        return value if isinstance(value, Mapping) else {}

    def sequence(value):
        return value if isinstance(value, list) else []

    def field(
        manifest_path,
        manifest_dir,
        node,
        key,
        path,
        algorithm="git",
        source_commit=None,
    ):
        if key in node:
            record_occurrence(
                manifest_path,
                manifest_dir,
                path,
                node,
                key,
                algorithm,
                source_commit or commit,
            )

    def pair(
        manifest_path,
        manifest_dir,
        node,
        path_key,
        digest_key,
        path,
        algorithm="git",
        source_commit=None,
    ):
        if digest_key in node:
            record_direct(
                manifest_path,
                manifest_dir,
                path,
                node,
                digest_key,
                path_key,
                algorithm,
                source_commit or commit,
            )

    for manifest_path in manifests:
        manifest_dir = PurePosixPath(manifest_path).parent.as_posix()
        try:
            raw = git.object_bytes(commit, manifest_path, "manifest")
            doc = yaml.safe_load(raw.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError, Incomplete, Violation) as exc:
            add_finding(
                "SCOPE_UNRESOLVABLE",
                manifest_path,
                "manifest",
                reason=f"MANIFEST_READ_FAILED:{exc}",
            )
            continue

        if not isinstance(doc, Mapping):
            add_finding(
                "UNCLASSIFIED",
                manifest_path,
                "manifest",
                reason="TOP_LEVEL_YAML_NOT_MAPPING",
            )
            continue

        source_evidence = mapping(doc.get("baseline_and_source_evidence"))

        # Root and mirror index pins.
        for path_key, digest_key in (
            ("root", "root_blob"),
            ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        ):
            pair(
                manifest_path,
                manifest_dir,
                doc,
                path_key,
                digest_key,
                f"{path_key}.{digest_key}",
            )

        # gate_a_reconstruction.
        reconstruction = doc.get("gate_a_reconstruction")
        if reconstruction is None:
            reconstruction = source_evidence.get("gate_a_reconstruction", [])
        for index, item in enumerate(sequence(reconstruction)):
            prefix = f"gate_a_reconstruction[{index}]"
            if not isinstance(item, Mapping):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    prefix,
                    reason="NON_MAPPING_ARRAY_ITEM",
                )
                continue
            source_commit = (
                item.get("source_commit")
                or item.get("source_commit_sha")
                or item.get("commit")
                or item.get("commit_sha")
                or source_evidence.get("main_reconciliation_head")
                or commit
            )
            if "reconstructed_root_blob" in item:
                pair(
                    manifest_path,
                    manifest_dir,
                    item,
                    "root",
                    "reconstructed_root_blob",
                    f"{prefix}.reconstructed_root_blob",
                    source_commit=source_commit,
                )
            for path_key, digest_key in (
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                pair(
                    manifest_path,
                    manifest_dir,
                    item,
                    path_key,
                    digest_key,
                    f"{prefix}.{digest_key}",
                    source_commit=item.get("source_commit") or item.get("commit") or commit,
                )

        # authored_indexes.
        authored = source_evidence.get(
            "authored_indexes",
            doc.get("authored_indexes", []),
        )
        for index, item in enumerate(sequence(authored)):
            prefix = f"authored_indexes[{index}]"
            if not isinstance(item, Mapping):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    prefix,
                    reason="NON_MAPPING_ARRAY_ITEM",
                )
                continue
            for path_key, digest_key in (
                ("root", "root_blob"),
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                pair(
                    manifest_path,
                    manifest_dir,
                    item,
                    path_key,
                    digest_key,
                    f"{prefix}.{digest_key}",
                )

        # related_evidence.
        for index, item in enumerate(sequence(doc.get("related_evidence", []))):
            prefix = f"related_evidence[{index}]"
            if not isinstance(item, Mapping):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    prefix,
                    reason="NON_MAPPING_ARRAY_ITEM",
                )
                continue
            for path_key, digest_key in (
                ("path", "blob"),
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                pair(
                    manifest_path,
                    manifest_dir,
                    item,
                    path_key,
                    digest_key,
                    f"{prefix}.{digest_key}",
                )

        # Top-level evidence_blob.
        if "evidence_blob" in doc:
            pair(
                manifest_path,
                manifest_dir,
                doc,
                "evidence_file",
                "evidence_blob",
                "evidence_blob",
            )

        # d_source_blobs, including the nested baseline_and_source_evidence form.
        d_source_entries = doc.get("d_source_blobs")
        d_source_commit = doc.get("d_source_commit")
        if d_source_entries is None:
            d_source_entries = source_evidence.get("d_source_blobs")
            d_source_commit = (
                d_source_commit or source_evidence.get("d_source_commit")
            )
        if d_source_entries is not None:
            if not isinstance(d_source_entries, list):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    "d_source_blobs",
                    reason="D_SOURCE_BLOBS_NOT_LIST",
                )
            else:
                for index, entry in enumerate(d_source_entries):
                    prefix = f"d_source_blobs[{index}]"
                    if not isinstance(entry, str) or ":" not in entry:
                        add_finding(
                            "UNCLASSIFIED",
                            manifest_path,
                            prefix,
                            reason="MALFORMED_D_SOURCE_BLOB_ENTRY",
                            declared=entry,
                        )
                        continue
                    path_value, digest_value = entry.rsplit(":", 1)
                    path_value = path_value.strip()
                    digest_value = digest_value.strip()
                    if not path_value:
                        add_finding(
                            "NO_SCOPE",
                            manifest_path,
                            prefix,
                            reason="D_SOURCE_PATH_EMPTY",
                            declared=digest_value,
                        )
                        result.pins += 1
                        continue
                    if "/" not in path_value:
                        try:
                            matches = git.paths_by_basename(
                                d_source_commit,
                                path_value,
                                prefix,
                            )
                        except Incomplete:
                            matches = []
                        if len(matches) != 1:
                            add_finding(
                                "NO_SCOPE",
                                manifest_path,
                                prefix,
                                reason="D_SOURCE_BASENAME_NOT_UNIQUE",
                                declared=digest_value,
                            )
                            result.pins += 1
                            continue
                        path_value = matches[0]
                    synthetic = {
                        "d_source_blob_sha": digest_value,
                        "d_source_path": path_value,
                        "d_source_commit_sha": d_source_commit,
                    }
                    record_occurrence(
                        manifest_path,
                        manifest_dir,
                        prefix,
                        synthetic,
                        "d_source_blob_sha",
                        "git-blob-sha1",
                        d_source_commit or commit,
                    )

        # prompt.prompt_sha256 and prompt.prompt_bytes.
        prompt = mapping(doc.get("prompt"))
        pair(
            manifest_path,
            manifest_dir,
            prompt,
            "prompt_file",
            "prompt_sha256",
            "prompt.prompt_sha256",
            "sha256",
        )
        pair(
            manifest_path,
            manifest_dir,
            prompt,
            "prompt_file",
            "prompt_bytes",
            "prompt.prompt_bytes",
            "byte-length",
        )

        # session_evidence.
        for index, item in enumerate(sequence(doc.get("session_evidence", []))):
            prefix = f"session_evidence[{index}]"
            if not isinstance(item, Mapping):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    prefix,
                    reason="NON_MAPPING_ARRAY_ITEM",
                )
                continue
            prompt_commit = item.get("executed_prompt_commit_sha") or commit
            pair(
                manifest_path,
                manifest_dir,
                item,
                "executed_prompt_snapshot_file",
                "executed_prompt_sha256",
                f"{prefix}.executed_prompt_sha256",
                "sha256",
                prompt_commit,
            )
            pair(
                manifest_path,
                manifest_dir,
                item,
                "executed_prompt_snapshot_file",
                "executed_prompt_bytes",
                f"{prefix}.executed_prompt_bytes",
                "byte-length",
                prompt_commit,
            )

        # Top-level prompt_sha256.
        if "prompt_sha256" in doc:
            version = doc.get("prompt_version")
            prompt_file = doc.get("prompt_file")
            if not isinstance(prompt_file, str) or not prompt_file.strip():
                prompt_file = (
                    f"prompt-{version}.md"
                    if isinstance(version, str)
                    and re.fullmatch(r"v[0-9]+", version)
                    else None
                )
            synthetic = dict(doc)
            if prompt_file:
                synthetic["prompt_path"] = prompt_file
            if "prompt_commit_sha" in doc:
                synthetic["prompt_commit_sha"] = doc["prompt_commit_sha"]
            record_occurrence(
                manifest_path,
                manifest_dir,
                "prompt_sha256",
                synthetic,
                "prompt_sha256",
                "sha256",
                doc.get("prompt_commit_sha") or commit,
            )

        # source_translation_pairs.
        pairs = doc.get("source_translation_pairs", [])
        if pairs:
            if not isinstance(pairs, list):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    "source_translation_pairs",
                    reason="SOURCE_TRANSLATION_PAIRS_NOT_LIST",
                )
            else:
                for index, item in enumerate(pairs):
                    prefix = f"source_translation_pairs[{index}]"
                    if not isinstance(item, Mapping):
                        add_finding(
                            "UNCLASSIFIED",
                            manifest_path,
                            prefix,
                            reason="NON_MAPPING_ARRAY_ITEM",
                        )
                        continue
                    source_commit = item.get("source_commit_sha") or commit
                    translation_commit = item.get("translation_commit_sha") or commit
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "source_path",
                        "source_blob_sha",
                        f"{prefix}.source_blob_sha",
                        source_commit=source_commit,
                    )
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "translation_path",
                        "translation_blob_sha",
                        f"{prefix}.translation_blob_sha",
                        source_commit=translation_commit,
                    )
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "translation_path",
                        "translation_sha256",
                        f"{prefix}.translation_sha256",
                        "sha256",
                        translation_commit,
                    )
                    reverify_commit = (
                        item.get("reverification_commit_sha")
                        or item.get("reverified_at_commit")
                        or commit
                    )
                    for digest_key, path_key in (
                        ("reverified_source_blob_sha", "source_path"),
                        ("reverified_translation_blob_sha", "translation_path"),
                    ):
                        pair(
                            manifest_path,
                            manifest_dir,
                            item,
                            path_key,
                            digest_key,
                            f"{prefix}.{digest_key}",
                            source_commit=reverify_commit,
                        )

        # source_blobs and baseline_evidence.source_blobs.
        source_blobs = doc.get("source_blobs")
        if source_blobs is None:
            source_blobs = mapping(doc.get("baseline_evidence")).get("source_blobs")
        if source_blobs is not None:
            if not isinstance(source_blobs, list):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    "source_blobs",
                    reason="SOURCE_BLOBS_NOT_LIST",
                )
            else:
                source_commit = (
                    doc.get("base_commit")
                    or doc.get("base_commit_sha")
                    or doc.get("baseline_commit")
                    or commit
                )
                for index, item in enumerate(source_blobs):
                    prefix = f"source_blobs[{index}]"
                    if not isinstance(item, Mapping):
                        add_finding(
                            "UNCLASSIFIED",
                            manifest_path,
                            prefix,
                            reason="NON_MAPPING_ARRAY_ITEM",
                        )
                        continue
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "path",
                        "sha",
                        f"{prefix}.sha",
                        source_commit=source_commit,
                    )

        # source.source_blob_sha.
        source = mapping(doc.get("source"))
        if "source_blob_sha" in source:
            source_commit = (
                source.get("branch_head")
                or source.get("head_sha")
                or source.get("head")
                or commit
            )
            source_path_key = (
                "source_path"
                if "source_path" in source
                else "path"
                if "path" in source
                else None
            )
            if source_path_key:
                pair(
                    manifest_path,
                    manifest_dir,
                    source,
                    source_path_key,
                    "source_blob_sha",
                    "source.source_blob_sha",
                    source_commit=source_commit,
                )
            else:
                record_blob_oid(
                    manifest_path,
                    manifest_dir,
                    "source.source_blob_sha",
                    source,
                    "source_blob_sha",
                    source_commit,
                )

        # source.selected_source_files.
        selected = source.get("selected_source_files", [])
        if selected:
            if not isinstance(selected, list):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    "source.selected_source_files",
                    reason="SELECTED_SOURCE_FILES_NOT_LIST",
                )
            else:
                source_commit = (
                    source.get("head_sha") or source.get("head") or commit
                )
                for index, item in enumerate(selected):
                    prefix = f"source.selected_source_files[{index}]"
                    if not isinstance(item, Mapping):
                        add_finding(
                            "UNCLASSIFIED",
                            manifest_path,
                            prefix,
                            reason="NON_MAPPING_ARRAY_ITEM",
                        )
                        continue
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "path",
                        "source_blob_sha",
                        f"{prefix}.source_blob_sha",
                        source_commit=source_commit,
                    )
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "path",
                        "restored_blob_sha",
                        f"{prefix}.restored_blob_sha",
                    )
                    if "frontmatter_blob_sha" in item:
                        front_path_key = (
                            "frontmatter_path"
                            if "frontmatter_path" in item
                            else "frontmatter_file"
                            if "frontmatter_file" in item
                            else None
                        )
                        if front_path_key:
                            pair(
                                manifest_path,
                                manifest_dir,
                                item,
                                front_path_key,
                                "frontmatter_blob_sha",
                                f"{prefix}.frontmatter_blob_sha",
                                source_commit=source_commit,
                            )
                        else:
                            record_blob_oid(
                                manifest_path,
                                manifest_dir,
                                f"{prefix}.frontmatter_blob_sha",
                                item,
                                "frontmatter_blob_sha",
                                source_commit,
                            )

        # source.files.
        source_files = source.get("files", [])
        if source_files:
            if not isinstance(source_files, list):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    "source.files",
                    reason="SOURCE_FILES_NOT_LIST",
                )
            else:
                source_commit = (
                    source.get("head") or source.get("head_sha") or commit
                )
                for index, item in enumerate(source_files):
                    prefix = f"source.files[{index}]"
                    if not isinstance(item, Mapping):
                        add_finding(
                            "UNCLASSIFIED",
                            manifest_path,
                            prefix,
                            reason="NON_MAPPING_ARRAY_ITEM",
                        )
                        continue
                    pair(
                        manifest_path,
                        manifest_dir,
                        item,
                        "path",
                        "blob",
                        f"{prefix}.blob",
                        source_commit=source_commit,
                    )

        # owner_ruling.
        owner_ruling = mapping(doc.get("owner_ruling"))
        for digest_key, path_key in (
            ("current_blob", "current_artifact"),
            ("superseded_blob", "superseded_artifact"),
        ):
            pair(
                manifest_path,
                manifest_dir,
                owner_ruling,
                path_key,
                digest_key,
                f"owner_ruling.{digest_key}",
            )

        # reconciliation.pointers_changed.
        reconciliation = mapping(doc.get("reconciliation"))
        for index, item in enumerate(
            sequence(reconciliation.get("pointers_changed", []))
        ):
            prefix = f"reconciliation.pointers_changed[{index}]"
            if not isinstance(item, Mapping):
                add_finding(
                    "UNCLASSIFIED",
                    manifest_path,
                    prefix,
                    reason="NON_MAPPING_ARRAY_ITEM",
                )
                continue
            for digest_key, artifact_key in (
                ("before_blob", "superseded_artifact"),
                ("after_blob", "current_artifact"),
            ):
                if digest_key not in item:
                    continue
                synthetic = {
                    digest_key: item[digest_key],
                    f"{digest_key}_path": owner_ruling.get(artifact_key),
                    f"{digest_key}_commit_sha": commit,
                }
                record_occurrence(
                    manifest_path,
                    manifest_dir,
                    f"{prefix}.{digest_key}",
                    synthetic,
                    digest_key,
                    "git-blob-sha1",
                    commit,
                )

        # renumbering.
        renumbering = mapping(doc.get("renumbering"))
        if "current_prompt_sha256" in renumbering:
            locator = (
                renumbering.get("current_prompt_file")
                or doc.get("prompt_file")
            )
            synthetic = dict(renumbering)
            if locator:
                synthetic["current_prompt_path"] = locator
            record_occurrence(
                manifest_path,
                manifest_dir,
                "renumbering.current_prompt_sha256",
                synthetic,
                "current_prompt_sha256",
                "sha256",
                commit,
            )
        if "previous_prompt_sha256" in renumbering:
            synthetic = dict(renumbering)
            if renumbering.get("previous_prompt_file"):
                synthetic["previous_prompt_path"] = renumbering["previous_prompt_file"]
            record_occurrence(
                manifest_path,
                manifest_dir,
                "renumbering.previous_prompt_sha256",
                synthetic,
                "previous_prompt_sha256",
                "sha256",
                commit,
            )

        # measurement_basis, scoped to the AID-2026-001 historical record.
        if doc.get("work_item_id") == "AID-2026-001":
            dev = mapping(doc.get("dev_baseline_integration"))
            integration = mapping(dev.get("mainline_integration"))
            measurement = mapping(integration.get("measurement_basis"))
            merged_head = (
                integration.get("merged_main_head")
                or integration.get("merge_commit")
                or commit
            )
            model_path = "reference-model/r3_contract_model.py"
            tests_path = "reference-model/test_r3_contract.py"
            for key, path_value, algorithm in (
                ("model_blob_sha256_lf", model_path, "sha256"),
                ("tests_blob_sha256_lf", tests_path, "sha256"),
                ("model_blob_bytes_lf", model_path, "byte-length"),
                ("tests_blob_bytes_lf", tests_path, "byte-length"),
            ):
                if key not in measurement:
                    continue
                synthetic = dict(measurement)
                synthetic[f"{key}_path"] = path_value
                synthetic[f"{key}_commit_sha"] = merged_head
                record_occurrence(
                    manifest_path,
                    manifest_dir,
                    f"measurement_basis.{key}",
                    synthetic,
                    key,
                    algorithm,
                    merged_head,
                )

        # Historical source and reference-model declarations.
        if doc.get("work_item_id") == "AID-2026-001":
            dev = mapping(doc.get("dev_baseline_integration"))
            target_commit = dev.get("target_commit") or commit
            ref_validation = mapping(doc.get("reference_model_validation"))
            for section_name in ("model", "tests"):
                section = mapping(ref_validation.get(section_name))
                if "git_blob_sha" in section:
                    pair(
                        manifest_path,
                        manifest_dir,
                        section,
                        "file",
                        "git_blob_sha",
                        f"reference_model_validation.{section_name}.git_blob_sha",
                        source_commit=target_commit,
                    )
            execution_record = mapping(ref_validation.get("execution_record"))
            if "git_blob_sha" in execution_record:
                record_blob_oid(
                    manifest_path,
                    manifest_dir,
                    "reference_model_validation.execution_record.git_blob_sha",
                    execution_record,
                    "git_blob_sha",
                    target_commit,
                )

            post_merge = mapping(doc.get("post_merge_manifest_validation"))
            observed_head = post_merge.get("observed_main_head") or commit
            current_blobs = mapping(doc.get("current_main_blobs"))
            current_paths = {
                "forget_model_py": "reference-model/forget_model.py",
                "test_forget_model_py": "reference-model/test_forget_model.py",
                "readme_md": "reference-model/README.md",
            }
            for key, value in current_blobs.items():
                if key in current_paths:
                    synthetic = {
                        key + "_blob_sha": value,
                        key + "_path": current_paths[key],
                        key + "_commit_sha": observed_head,
                    }
                    record_occurrence(
                        manifest_path,
                        manifest_dir,
                        f"current_main_blobs.{key}",
                        synthetic,
                        key + "_blob_sha",
                        "git-blob-sha1",
                        observed_head,
                    )
                elif key == "workflow_yml":
                    record_blob_oid(
                        manifest_path,
                        manifest_dir,
                        f"current_main_blobs.{key}",
                        {"workflow_yml_blob_sha": value},
                        "workflow_yml_blob_sha",
                        observed_head,
                    )
                else:
                    add_finding(
                        "UNCLASSIFIED",
                        manifest_path,
                        f"current_main_blobs.{key}",
                        reason="NO_FIELD_SPECIFIC_LOCATOR_RULE",
                        declared=value,
                    )
                    result.pins += 1

            for key, path_value, source_ref in (
                (
                    "model_blob",
                    "reference-model/r3_contract_model.py",
                    target_commit,
                ),
                (
                    "tests_blob",
                    "reference-model/test_r3_contract.py",
                    mapping(dev.get("mainline_integration")).get(
                        "pre_update_branch_head"
                    )
                    or target_commit,
                ),
            ):
                if key in dev:
                    synthetic = {
                        key: dev[key],
                        key + "_path": path_value,
                        key + "_commit_sha": source_ref,
                    }
                    record_occurrence(
                        manifest_path,
                        manifest_dir,
                        f"dev_baseline_integration.{key}",
                        synthetic,
                        key,
                        "git-blob-sha1",
                        source_ref,
                    )

            integration = mapping(dev.get("mainline_integration"))
            merged_head = (
                integration.get("merged_main_head")
                or integration.get("merge_commit")
                or commit
            )
            for key, path_value in (
                (
                    "forget_model_blob",
                    "reference-model/forget_model.py",
                ),
                (
                    "forget_tests_blob",
                    "reference-model/test_forget_model.py",
                ),
            ):
                if key in integration:
                    synthetic = {
                        key: integration[key],
                        key + "_path": path_value,
                        key + "_commit_sha": merged_head,
                    }
                    record_occurrence(
                        manifest_path,
                        manifest_dir,
                        f"mainline_integration.{key}",
                        synthetic,
                        key,
                        "git-blob-sha1",
                        merged_head,
                    )

            readme_key = "reference_model_readme_blob_before_append"
            if readme_key in integration:
                synthetic = {
                    readme_key: integration[readme_key],
                    readme_key + "_path": "reference-model/README.md",
                    readme_key + "_commit_sha": (
                        integration.get("pre_update_branch_head")
                        or merged_head
                    ),
                }
                record_occurrence(
                    manifest_path,
                    manifest_dir,
                    f"mainline_integration.{readme_key}",
                    synthetic,
                    readme_key,
                    "git-blob-sha1",
                    synthetic[readme_key + "_commit_sha"],
                )

        # prompt_file_blob_sha and other registered prompt pins.
        for key in (
            "prompt_file_blob_sha",
            "prompt_original_payload_sha256",
            "instruction_sha256",
        ):
            if key in doc:
                synthetic = dict(doc)
                locator_key = (
                    "prompt_file"
                    if key == "prompt_file_blob_sha"
                    else "prompt_original_payload_file"
                )
                synthetic[key + "_path"] = synthetic.get(locator_key)
                synthetic[key + "_commit_sha"] = (
                    synthetic.get("prompt_file_commit_sha")
                    or synthetic.get("prompt_commit_sha")
                    or commit
                )
                record_occurrence(
                    manifest_path,
                    manifest_dir,
                    key,
                    synthetic,
                    key,
                    "auto",
                    synthetic[key + "_commit_sha"],
                )

        # Discover remaining declared pin-shaped scalar occurrences. This is
        # deliberately not a whitelist: anything with a pin-shaped field name
        # is either verified or explicitly classified as unclassified.
        def discover_unregistered(node, where: str) -> None:
            if isinstance(node, Mapping):
                for key, value in node.items():
                    key_text = str(key)
                    if key_text in {
                        "stdout_sha256",
                        "prompt_original_payload_file",
                    }:
                        discover_unregistered(value, f"{where}.{key_text}")
                        continue

                    is_pin_key = (
                        key_text == "blob"
                        or key_text.endswith("_blob")
                        or key_text.endswith("_blob_sha")
                        or key_text.endswith("_blob_sha256")
                        or key_text.endswith("_sha256")
                        or key_text.endswith("_sha")
                    )
                    is_commit_key = (
                        "commit" in key_text.lower()
                        or key_text in {"head_sha", "base_sha", "merge_sha"}
                    )
                    if (
                        is_pin_key
                        and not is_commit_key
                        and isinstance(value, (str, int))
                        and not isinstance(value, bool)
                    ):
                        field_path = f"{where}.{key_text}"
                        if (manifest_path, field_path) not in seen:
                            classification, basis = classify_declaration(
                                node,
                                key_text,
                            )
                            if classification == "unknown":
                                result.pins += 1
                                add_finding(
                                    "UNCLASSIFIED",
                                    manifest_path,
                                    field_path,
                                    node=node,
                                    key=key_text,
                                    reason=basis or "DECLARATION_KIND_AMBIGUOUS",
                                    declared=value,
                                )
                            else:
                                record_occurrence(
                                    manifest_path,
                                    manifest_dir,
                                    field_path,
                                    node,
                                    key_text,
                                    "auto",
                                    commit,
                                )

                    discover_unregistered(value, f"{where}.{key_text}")

            elif isinstance(node, list):
                for index, value in enumerate(node):
                    if isinstance(value, Mapping):
                        discover_unregistered(value, f"{where}[{index}]")
                    elif isinstance(value, list):
                        discover_unregistered(value, f"{where}[{index}]")
                    elif (
                        isinstance(value, str)
                        and (HEX40.fullmatch(value) or HEX64.fullmatch(value))
                    ):
                        # Bare list scalars have no declaration-local locator
                        # contract in this handler; they are not silently lost.
                        field_path = f"{where}[{index}]"
                        if (manifest_path, field_path) not in seen:
                            result.pins += 1
                            add_finding(
                                "UNCLASSIFIED",
                                manifest_path,
                                field_path,
                                reason="LIST_SCALAR_WITHOUT_DECLARATION_MAPPING",
                                declared=value,
                            )

        discover_unregistered(doc, "manifest")

    if verbose:
        print(
            f"main={commit} manifests={len(manifests)} pins={result.pins} "
            f"ok={result.ok} mismatch={result.mismatch} "
            f"path_missing={result.path_missing} "
            f"incomplete={result.scope_unresolvable}"
        )
        for line in problems:
            print(line)

    return result.exit_code


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args(argv)

    try:
        resolved_commit = Git(args.root).resolve_commit(
            args.commit,
            "--commit",
        )
        return verify(args.root, resolved_commit)
    except Incomplete as exc:
        print(f"SCOPE_UNRESOLVABLE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
