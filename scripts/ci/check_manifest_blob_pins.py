#!/usr/bin/env python3
# scripts/ci/check_manifest_blob_pins.py
"""Verify registered manifest blob pins against their declared Git scope.

Exit status:
    0: all registered pins pass
    1: one or more ordinary violations
    2: one or more incomplete/unresolved checks or internal errors
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Mapping

import yaml

from blob_pin_registry import FIELD_REGISTRY
from blob_pin_scope import (
    NoScope,
    PathMissing,
    Scope,
    ScopeUnresolvable,
    Unresolved,
    derive_scope,
    digest_of,
    resolve_bytes,
)


MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
ARRAY_INDEX = re.compile(r"\[\d+\]")

FINDING_KINDS = frozenset({
    "MISMATCH",
    "PATH_MISSING",
    "UNCLASSIFIED",
    "NO_SCOPE",
    "SCOPE_UNRESOLVABLE",
    "UNRESOLVED",
})

SENTINELS = frozenset({
    "NOT_VERIFIED",
    "NOT_APPLICABLE",
})


@dataclass(frozen=True)
class Finding:
    kind: str
    manifest: str
    pin_id: str
    field_path: str
    scope: str
    locator: str
    declared: str = ""
    actual: str = ""
    reason: str = ""
    classification: str = ""
    basis: str = ""


@dataclass
class Verification:
    findings: list[Finding] = field(default_factory=list)
    pins: int = 0
    ok: int = 0

    @property
    def exit_code(self) -> int:
        if any(
            finding.kind in {"UNRESOLVED", "SCOPE_UNRESOLVABLE"}
            for finding in self.findings
        ):
            return 2
        return 1 if self.findings else 0

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)


class Incomplete(Exception):
    """A required repository operation could not be completed."""


class Git:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def run(self, *args: str, label: str = "git operation") -> bytes:
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

        if proc.returncode:
            detail = proc.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(
                f"{label}: {detail or f'git {args!r} failed ({proc.returncode})'}"
            )
        return proc.stdout

    def resolve_commit(self, ref: str, label: str = "commit resolution") -> str:
        if not isinstance(ref, str) or not ref.strip():
            raise Incomplete(f"{label}: empty commit reference")

        raw = self.run(
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{ref}^{{commit}}",
            label=label,
        )
        resolved = raw.decode("ascii", "replace").strip().lower()
        if not HEX40.fullmatch(resolved):
            raise Incomplete(
                f"{label}: {ref!r} did not resolve to a full 40-character commit"
            )
        return resolved


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def registry_field_name(field_path: str, key: str | None = None) -> str:
    """Get the final field name after removing all array indices.

    a.b[0].c[2] -> c
    implementation_commits[0] -> implementation_commits
    """
    if not isinstance(field_path, str) or not field_path:
        return key or ""

    leaf = field_path.rsplit(".", 1)[-1]
    leaf = ARRAY_INDEX.sub("", leaf)
    return leaf or (key or "")


def registry_spec_for(field_path: str, key: str | None = None):
    """Resolve the field using the normalized leaf name."""
    return FIELD_REGISTRY.get(registry_field_name(field_path, key))


def pin_id_for(manifest: str, field_path: str) -> str:
    slug = re.sub(
        r"[^A-Za-z0-9_.-]+",
        "-",
        field_path,
    ).strip("-")[:64] or "pin"
    identity = f"{manifest}\0{field_path}".encode("utf-8")
    suffix = hashlib.sha256(identity).hexdigest()[:12]
    return f"{slug}-{suffix}"


def identity_line(finding: Finding) -> str:
    """Stable identity only; no diagnostic fields or trailing newline."""
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


def explain_line(finding: Finding) -> str:
    """Append JSON-escaped diagnostics without altering identity bytes."""
    return (
        identity_line(finding)
        + f" declared={json.dumps(finding.declared, ensure_ascii=False)}"
        + f" actual={json.dumps(finding.actual, ensure_ascii=False)}"
        + f" reason={json.dumps(finding.reason, ensure_ascii=False)}"
        + f" classification={json.dumps(finding.classification, ensure_ascii=False)}"
        + f" basis={json.dumps(finding.basis, ensure_ascii=False)}"
    )


def _scope_name(scope: Scope | None) -> str:
    return scope.kind if scope is not None else "none"


def _finding(
    *,
    kind: str,
    manifest: str,
    field_path: str,
    scope: Scope | None = None,
    locator: str | None = None,
    declared="",
    actual="",
    reason="",
    classification="",
    basis="",
) -> Finding:
    return Finding(
        kind=kind,
        manifest=manifest,
        pin_id=pin_id_for(manifest, field_path),
        field_path=field_path,
        scope=_scope_name(scope),
        locator=locator if locator is not None else "none",
        declared=str(declared),
        actual=str(actual),
        reason=str(reason),
        classification=str(classification),
        basis=str(basis),
    )


def _has_registered_unverifiable_provenance(node, key) -> bool:
    """A NOT_VERIFIED declaration is only downgraded when it carries evidence."""
    if not isinstance(node, Mapping):
        return False

    value = node.get(key)
    note = node.get(f"{key}_note")
    provenance = node.get(f"{key}_provenance")

    return (
        isinstance(value, str)
        and value.strip().upper() == "NOT_VERIFIED"
        and isinstance(note, str)
        and bool(note.strip())
        and provenance == "NOT_VERIFIED"
    )


def _is_sentinel(value) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().upper()
    return normalized in SENTINELS


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
    return False


def classify_declaration(
    node: Mapping,
    key: str,
    field_path: str | None = None,
) -> tuple[str, str]:
    """Classify strictly from FIELD_REGISTRY.

    Returns (classification, basis). NON_BLOB is a terminal classification.
    """
    spec = registry_spec_for(field_path or key, key)
    if spec is None:
        return "unknown", "UNREGISTERED_FIELD"

    if spec.algorithm == "NON_BLOB":
        return "NON_BLOB", "FIELD_REGISTRY"

    if spec.algorithm not in {"sha256", "git-blob-sha1", "byte-length"}:
        return "unknown", "UNSUPPORTED_REGISTRY_ALGORITHM"

    if not spec.locator_keys:
        return "unknown", "NO_LOCATOR_SIBLING"

    if not isinstance(node, Mapping):
        return "unknown", "PIN_NODE_NOT_MAPPING"

    present = [name for name in spec.locator_keys if name in node]
    usable = [
        (name, node[name])
        for name in present
        if nonempty(node[name])
    ]

    if not usable:
        if present:
            return "unknown", "LOCATOR_NOT_A_PATH"
        return "unknown", "NO_LOCATOR_SIBLING"

    if len({value for _, value in usable}) != 1:
        return "unknown", "LOCATOR_AMBIGUOUS"

    classification = (
        "git-object"
        if spec.algorithm == "git-blob-sha1"
        else "content-digest"
    )
    names = ",".join(name for name, _ in usable)
    return classification, f"FIELD_REGISTRY:{names}"


def _locator_for(
    node: Mapping,
    key: str,
    declaration_kind: str | None = None,
    *,
    field_path: str | None = None,
) -> str | None:
    """Use the exact locator_keys from the authoritative registry."""
    spec = registry_spec_for(field_path or key, key)
    if spec is None or spec.algorithm == "NON_BLOB":
        return None

    candidates = [
        node[name]
        for name in spec.locator_keys
        if name in node and nonempty(node[name])
    ]
    if not candidates or len(set(candidates)) != 1:
        return None
    return candidates[0]


def check_pin(
    *,
    root: Path,
    manifest: str,
    manifest_dir: str,
    field_path: str,
    node: Mapping,
    key: str,
) -> Finding | None:
    """Check one pin occurrence.

    This keyword-only interface is used consistently by record_occurrence;
    there is no caller-supplied algorithm or implicit commit fallback.
    """
    spec = registry_spec_for(field_path, key)
    if spec is None:
        return _finding(
            kind="UNCLASSIFIED",
            manifest=manifest,
            field_path=field_path,
            declared=node.get(key, ""),
            reason="UNREGISTERED_FIELD",
            classification="UNCLASSIFIED",
            basis="UNREGISTERED_FIELD",
        )

    if spec.algorithm == "NON_BLOB":
        return None

    declared = node.get(key)

    if _is_sentinel(declared):
        if _has_registered_unverifiable_provenance(node, key):
            return _finding(
                kind="UNCLASSIFIED",
                manifest=manifest,
                field_path=field_path,
                declared=declared,
                reason="REGISTERED_UNVERIFIABLE_DECLARATION",
                classification="UNVERIFIABLE",
                basis="EXPLICIT_NOTE_AND_PROVENANCE",
            )
        return _finding(
            kind="UNRESOLVED",
            manifest=manifest,
            field_path=field_path,
            declared=declared,
            reason="SENTINEL_DECLARATION",
            classification=spec.algorithm,
            basis="FIELD_REGISTRY",
        )

    classification, basis = classify_declaration(
        node,
        key,
        field_path,
    )
    if classification == "unknown":
        return _finding(
            kind="UNCLASSIFIED",
            manifest=manifest,
            field_path=field_path,
            declared=declared,
            reason=basis,
            classification=classification,
            basis=basis,
        )

    locator = _locator_for(
        node,
        key,
        classification,
        field_path=field_path,
    )
    if locator is None:
        return _finding(
            kind="UNCLASSIFIED",
            manifest=manifest,
            field_path=field_path,
            declared=declared,
            reason="LOCATOR_AMBIGUOUS_OR_INVALID",
            classification=classification,
            basis=basis,
        )

    try:
        scope = derive_scope(
            node,
            key,
            manifest_dir,
            locator_keys=spec.locator_keys,
        )
    except NoScope as exc:
        return _finding(
            kind="NO_SCOPE",
            manifest=manifest,
            field_path=field_path,
            declared=declared,
            reason=str(exc),
            classification=spec.algorithm,
            basis=basis,
        )
    except ScopeUnresolvable as exc:
        return _finding(
            kind="SCOPE_UNRESOLVABLE",
            manifest=manifest,
            field_path=field_path,
            declared=declared,
            reason=str(exc),
            classification=spec.algorithm,
            basis=basis,
        )

    try:
        data = resolve_bytes(root, scope, locator)
    except PathMissing as exc:
        return _finding(
            kind="PATH_MISSING",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            reason=str(exc),
            classification=spec.algorithm,
            basis=basis,
        )
    except Unresolved as exc:
        return _finding(
            kind="UNRESOLVED",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            reason=str(exc),
            classification=spec.algorithm,
            basis=basis,
        )
    except ScopeUnresolvable as exc:
        return _finding(
            kind="SCOPE_UNRESOLVABLE",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            reason=str(exc),
            classification=spec.algorithm,
            basis=basis,
        )

    if not _valid_declaration(spec.algorithm, declared):
        return _finding(
            kind="MISMATCH",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            actual=digest_of(spec.algorithm, data),
            reason="INVALID_DECLARATION_FORMAT",
            classification=spec.algorithm,
            basis=basis,
        )

    actual = digest_of(spec.algorithm, data)
    if actual.lower() != str(declared).lower():
        return _finding(
            kind="MISMATCH",
            manifest=manifest,
            field_path=field_path,
            scope=scope,
            locator=locator,
            declared=declared,
            actual=actual,
            reason="DIGEST_MISMATCH",
            classification=spec.algorithm,
            basis=basis,
        )

    return None


def _looks_like_unregistered_pin(key: str, value) -> bool:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return False

    if isinstance(value, str):
        return bool(HEX40.fullmatch(value) or HEX64.fullmatch(value))

    return key.endswith("_bytes")


def discover_manifests(git: Git, commit: str) -> list[str]:
    raw = git.run(
        "ls-tree",
        "-r",
        "--name-only",
        "--full-tree",
        commit,
        "--",
        MANIFEST_ROOT,
        label="manifest discovery",
    )
    prefix = PurePosixPath(MANIFEST_ROOT)
    manifests = []

    for item in raw.splitlines():
        path = PurePosixPath(item.decode("utf-8", "surrogateescape"))
        if (
            path.name == "manifest.yaml"
            and path.parent.parent == prefix
        ):
            manifests.append(path.as_posix())

    return sorted(set(manifests))


def _load_manifest(git: Git, commit: str, path: str):
    raw = git.run(
        "cat-file",
        "blob",
        f"{commit}:{path}",
        label=f"read manifest {path}",
    )
    try:
        document = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeError, yaml.YAMLError) as exc:
        raise Incomplete(f"cannot parse {path}: {exc}") from exc

    if not isinstance(document, Mapping):
        raise Incomplete(f"{path}: manifest root is not a mapping")
    return document


def verify(
    root: Path,
    commit: str,
    *,
    explain: bool = False,
    verbose: bool = True,
) -> int:
    git = Git(root)
    resolved_commit = git.resolve_commit(commit, "--commit")
    manifests = discover_manifests(git, resolved_commit)
    if not manifests:
        raise Incomplete(f"no manifests found at {resolved_commit}")

    result = Verification()
    seen: set[tuple[str, str]] = set()

    def add_finding(finding: Finding) -> None:
        occurrence = (finding.manifest, finding.field_path)
        if occurrence in seen:
            return
        seen.add(occurrence)
        result.add(finding)

    def record_occurrence(
        manifest_path: str,
        manifest_dir: str,
        field_path: str,
        node: Mapping,
        key: str,
    ) -> None:
        occurrence = (manifest_path, field_path)
        if occurrence in seen:
            return

        spec = registry_spec_for(field_path, key)

        # NON_BLOB entries, including list elements, are consumed here.
        # They are never counted as pins or emitted as findings.
        if spec is not None and spec.algorithm == "NON_BLOB":
            seen.add(occurrence)
            return

        result.pins += 1
        finding = check_pin(
            root=root,
            manifest=manifest_path,
            manifest_dir=manifest_dir,
            field_path=field_path,
            node=node,
            key=key,
        )
        if finding is None:
            result.ok += 1
            seen.add(occurrence)
            return
        add_finding(finding)

    def discover_unregistered(
        manifest_path: str,
        manifest_dir: str,
        node,
        where: str,
    ) -> None:
        if isinstance(node, Mapping):
            for raw_key, value in node.items():
                key = str(raw_key)
                child_path = f"{where}.{key}" if where else key
                spec = registry_spec_for(child_path, key)

                if spec is not None and spec.algorithm == "NON_BLOB":
                    seen.add((manifest_path, child_path))
                    continue

                if spec is not None and spec.algorithm in {
                    "sha256",
                    "git-blob-sha1",
                    "byte-length",
                }:
                    if isinstance(value, Mapping):
                        # A registered scalar declaration cannot be silently
                        # treated as a mapping; descend to discover its members.
                        discover_unregistered(
                            manifest_path,
                            manifest_dir,
                            value,
                            child_path,
                        )
                    elif isinstance(value, list):
                        # Lists of scalar values use the parent field name
                        # for registry lookup; each occurrence retains its index.
                        for index, item in enumerate(value):
                            item_path = f"{child_path}[{index}]"
                            item_spec = registry_spec_for(item_path)
                            if (
                                item_spec is not None
                                and item_spec.algorithm == "NON_BLOB"
                            ):
                                seen.add((manifest_path, item_path))
                            elif isinstance(item, (str, int)) and not isinstance(item, bool):
                                # A list-valued blob declaration has no
                                # per-element sibling mapping; fail closed.
                                if (manifest_path, item_path) not in seen:
                                    result.pins += 1
                                    add_finding(_finding(
                                        kind="UNCLASSIFIED",
                                        manifest=manifest_path,
                                        field_path=item_path,
                                        declared=item,
                                        reason="LIST_SCALAR_WITHOUT_DECLARATION_MAPPING",
                                        classification="unknown",
                                        basis="LIST_SCALAR_WITHOUT_FIELD_KEY",
                                    ))
                    else:
                        record_occurrence(
                            manifest_path,
                            manifest_dir,
                            child_path,
                            node,
                            key,
                        )
                    continue

                if (
                    spec is None
                    and _looks_like_unregistered_pin(key, value)
                    and not isinstance(value, (Mapping, list))
                ):
                    occurrence = (manifest_path, child_path)
                    if occurrence not in seen:
                        result.pins += 1
                        add_finding(_finding(
                            kind="UNCLASSIFIED",
                            manifest=manifest_path,
                            field_path=child_path,
                            declared=value,
                            reason="UNREGISTERED_FIELD",
                            classification="UNCLASSIFIED",
                            basis="UNREGISTERED_FIELD",
                        ))
                    continue

                discover_unregistered(
                    manifest_path,
                    manifest_dir,
                    value,
                    child_path,
                )

        elif isinstance(node, list):
            for index, value in enumerate(node):
                child_path = f"{where}[{index}]"

                # A list scalar is looked up by its index-stripped leaf,
                # which resolves to the containing list field name.
                spec = registry_spec_for(child_path)
                if spec is not None and spec.algorithm == "NON_BLOB":
                    seen.add((manifest_path, child_path))
                    continue

                if isinstance(value, Mapping) or isinstance(value, list):
                    discover_unregistered(
                        manifest_path,
                        manifest_dir,
                        value,
                        child_path,
                    )
                elif _looks_like_unregistered_pin(
                    registry_field_name(child_path),
                    value,
                ):
                    occurrence = (manifest_path, child_path)
                    if occurrence not in seen:
                        result.pins += 1
                        add_finding(_finding(
                            kind="UNCLASSIFIED",
                            manifest=manifest_path,
                            field_path=child_path,
                            declared=value,
                            reason="UNREGISTERED_FIELD",
                            classification="UNCLASSIFIED",
                            basis="LIST_SCALAR_WITHOUT_FIELD_KEY",
                        ))

    for manifest_path in manifests:
        try:
            document = _load_manifest(git, resolved_commit, manifest_path)
        except Incomplete as exc:
            result.pins += 1
            add_finding(_finding(
                kind="SCOPE_UNRESOLVABLE",
                manifest=manifest_path,
                field_path="<manifest>",
                reason=str(exc),
                classification="INCOMPLETE",
                basis="MANIFEST_READ_OR_PARSE_FAILURE",
            ))
            continue

        manifest_dir = str(PurePosixPath(manifest_path).parent)
        discover_unregistered(
            manifest_path,
            manifest_dir,
            document,
            "",
        )

    if verbose:
        print(
            f"main={resolved_commit} manifests={len(manifests)} "
            f"pins={result.pins} ok={result.ok} "
            f"mismatch={sum(f.kind == 'MISMATCH' for f in result.findings)} "
            f"path_missing={sum(f.kind == 'PATH_MISSING' for f in result.findings)} "
            f"incomplete={sum(f.kind in {'UNRESOLVED', 'SCOPE_UNRESOLVABLE'} for f in result.findings)} "
            f"unclassified={sum(f.kind == 'UNCLASSIFIED' for f in result.findings)} "
            f"no_scope={sum(f.kind == 'NO_SCOPE' for f in result.findings)} "
            f"unresolved={sum(f.kind == 'UNRESOLVED' for f in result.findings)} "
            f"scope_unresolvable={sum(f.kind == 'SCOPE_UNRESOLVABLE' for f in result.findings)} "
            f"findings={len(result.findings)} "
            f"violations={sum(f.kind not in {'UNRESOLVED', 'SCOPE_UNRESOLVABLE'} for f in result.findings)}"
        )
        for finding in result.findings:
            # One newline per finding in both modes. The explain prefix is
            # exactly identity_line(finding), with no newline in the identity.
            line = explain_line(finding) if explain else identity_line(finding)
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
    parser.add_argument(
        "--explain",
        action="store_true",
        help="append declared/actual/reason/classification/basis diagnostics",
    )
    args = parser.parse_args(argv)

    try:
        return verify(
            args.root,
            args.commit,
            explain=args.explain,
        )
    except (Incomplete, OSError, ValueError) as exc:
        print(f"SCOPE_UNRESOLVABLE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
