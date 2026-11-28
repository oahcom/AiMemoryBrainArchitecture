#!/usr/bin/env python3
"""Verify manifest blob pins against committed Git objects and their append-only ledger.

Exit status:
  0 PASS
  1 VIOLATION (a pin mismatch, a declared path is missing, an unbound
    blob_sha256 declaration, or an unledgered pin transition)
  2 INCOMPLETE (required Git data, commit history, or ledger evidence is unavailable)
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


MANIFEST_ROOT = "14-ai-development/work-items"
BASELINE_PATH = "scripts/ci/baselines/manifest-blob-pins.txt"
LEDGER_PATH = "scripts/ci/manifest-pin-ledger.md"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
BASELINE_COMMIT_RE = re.compile(r"Measured against main ([0-9a-f]{40})\.")

# A blob_sha256 declaration is a claim about committed file bytes. The name
# token may carry a qualifier suffix (model_blob_sha256_lf); the declaration
# still needs a path binding. An unbound declaration is a violation, not an
# out-of-scope field.
BLOB_SHA256_KEY = re.compile(
    r"^(?P<base>(?:.*_)?)blob_sha256(?:_[a-z0-9]+)*$"
)

LEDGER_HEADER = (
    "manifest",
    "field",
    "path",
    "previous_pin",
    "new_pin",
    "repin_commit",
)
LEDGER_HEADER_V2 = (
    "manifest",
    "field",
    "path",
    "reference_mode",
    "previous_pin",
    "new_pin",
    "repin_commit",
)
LEDGER_SEPARATOR = re.compile(
    r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*){5,6}\|?$"
)


class Incomplete(Exception):
    """The checker cannot establish a trustworthy result."""


class Violation(Exception):
    """A declared path is absent or a pin transition is unauthorized."""


@dataclass(frozen=True)
class Pin:
    manifest: str
    field: str
    path: str
    declared: str
    source_commit: str
    algorithm: str = "git"
    reference_mode: str = "current"

    @property
    def identity(self) -> tuple[str, str, str, str]:
        return (self.manifest, self.field, self.path, self.reference_mode)

    @property
    def value_identity(self) -> tuple[str, str, str, str, str]:
        return (*self.identity, self.algorithm)


@dataclass(frozen=True)
class LedgerRecord:
    manifest: str
    field: str
    path: str
    previous_pin: str
    new_pin: str
    repin_commit: str
    reference_mode: str = "current"

    @property
    def identity(self) -> tuple[str, str, str, str]:
        return (self.manifest, self.field, self.path, self.reference_mode)

    @property
    def algorithm(self) -> str:
        if self.previous_pin.isdigit() and self.new_pin.isdigit():
            return "bytes"
        if HEX64.fullmatch(self.previous_pin) and HEX64.fullmatch(self.new_pin):
            return "sha256"
        return "git"

    @property
    def value_identity(self) -> tuple[str, str, str, str, str]:
        return (*self.identity, self.algorithm)


@dataclass(frozen=True)
class ReferenceModeIssue:
    manifest: str
    field: str
    reason: str


class Git:
    def __init__(self, root: Path):
        self.root = root
        self._historical_blob_cache: dict[
            tuple[str, str, str], bool
        ] = {}

    def run(self, *args: str) -> bytes:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot execute git: {exc}") from exc
        if result.returncode:
            detail = result.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(
                detail or f"git {' '.join(args)} failed ({result.returncode})"
            )
        return result.stdout

    def resolve_commit(self, ref: str, description: str = "commit") -> str:
        if not isinstance(ref, str) or not ref.strip():
            raise Incomplete(f"{description} is absent")
        try:
            resolved = self.run(
                "rev-parse", "--verify", f"{ref.strip()}^{{commit}}"
            ).decode("ascii", "strict").strip()
        except (Incomplete, UnicodeError) as exc:
            raise Incomplete(
                f"{description} cannot be resolved: {ref!r}"
            ) from exc
        if not HEX40.fullmatch(resolved):
            raise Incomplete(
                f"{description} did not resolve to a full commit SHA: {ref!r}"
            )
        return resolved

    def object_bytes(self, commit: str, path: str) -> bytes:
        """Read a blob from a commit tree, distinguishing absent paths from bad commits."""
        if not isinstance(path, str) or not path.strip():
            raise Violation("PATH_MISSING path=<not-declared>")
        resolved = self.resolve_commit(commit, f"source commit for {path}")
        spec = f"{resolved}:{path}"
        try:
            result = subprocess.run(
                ["git", "cat-file", "blob", spec],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot read Git blob {spec}: {exc}") from exc
        if result.returncode:
            raise Violation(f"PATH_MISSING path={path}")
        return result.stdout

    def historical_blob_exists(
        self,
        commit: str,
        path: str,
        declared_blob: str,
    ) -> bool:
        """Prove a declared blob existed at this path anywhere in reachable history."""
        resolved = self.resolve_commit(commit, "historical reference commit")
        if not path or path.startswith("/") or ".." in Path(path).parts:
            raise Incomplete(f"invalid historical reference path: {path!r}")
        if not HEX40.fullmatch(declared_blob):
            raise Incomplete(
                f"historical reference is not a full Git blob SHA: "
                f"{declared_blob!r}"
            )

        cache_key = (resolved, path, declared_blob)
        cached = self._historical_blob_cache.get(cache_key)
        if cached is not None:
            return cached

        output = self.run(
            "log",
            "--format=%H",
            "--diff-filter=AMR",
            resolved,
            "--",
            path,
        )
        commits = [
            line.strip()
            for line in output.decode("ascii", "strict").splitlines()
            if line.strip()
        ]

        found = False
        for historical_commit in commits:
            if not HEX40.fullmatch(historical_commit):
                raise Incomplete(
                    f"invalid commit in historical path log: "
                    f"{historical_commit!r}"
                )
            spec = f"{historical_commit}:{path}"
            object_type = self.run("cat-file", "-t", spec)
            if object_type.decode("ascii", "strict").strip() != "blob":
                continue
            blob_sha = self.run("rev-parse", "--verify", spec)
            resolved_blob = blob_sha.decode("ascii", "strict").strip()
            if not HEX40.fullmatch(resolved_blob):
                raise Incomplete(
                    f"historical path did not resolve to a full blob SHA: {spec}"
                )
            if resolved_blob == declared_blob:
                found = True
                break

        self._historical_blob_cache[cache_key] = found
        return found

    def has_path(self, commit: str, path: str) -> bool:
        """Test tree membership without turning an expected absent path into an error."""
        resolved = self.resolve_commit(commit)
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{resolved}:{path}"],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode == 0:
            return True
        self.run("cat-file", "-e", f"{resolved}^{{commit}}")
        return False

    def first_parent(self, commit: str) -> str | None:
        resolved = self.resolve_commit(commit)
        fields = self.run("rev-list", "--parents", "-n", "1", resolved)
        parts = fields.decode("ascii", "strict").strip().split()
        if len(parts) < 2:
            return None
        if not HEX40.fullmatch(parts[1]):
            raise Incomplete(f"invalid first parent for commit {resolved}")
        return parts[1]

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        a = self.resolve_commit(ancestor, "ancestor commit")
        d = self.resolve_commit(descendant, "descendant commit")
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", a, d],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode == 0:
            return True
        if result.returncode == 1:
            return False
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise Incomplete(detail or f"cannot establish ancestry: {a} -> {d}")

    def first_parent_commits(self, older: str, newer: str) -> list[str]:
        old = self.resolve_commit(older, "history start")
        new = self.resolve_commit(newer, "history end")
        if not self.is_ancestor(old, new):
            raise Incomplete(f"history start {old} is not an ancestor of {new}")
        output = self.run(
            "rev-list", "--first-parent", "--reverse", f"{old}..{new}"
        )
        commits = [
            line.strip()
            for line in output.decode("ascii", "strict").splitlines()
            if line.strip()
        ]
        for commit in commits:
            if not HEX40.fullmatch(commit):
                raise Incomplete(
                    f"invalid commit in first-parent history: {commit!r}"
                )
        return commits

    def changed_manifest_paths(self, parent: str, commit: str) -> list[str]:
        output = self.run(
            "diff", "--name-only", "--diff-filter=ACMR",
            parent, commit, "--", MANIFEST_ROOT,
        )
        return sorted(
            path for path in output.decode("utf-8", "strict").splitlines()
            if path.startswith(MANIFEST_ROOT + "/")
            and path.endswith("/manifest.yaml")
        )


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def as_mapping(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def pointer_token(key: Any) -> str:
    return str(key).replace("~", "~0").replace("/", "~1")


def walk_declarations(node: Any, pointer: str = ""):
    """Yield (JSON pointer, field, value, containing mapping) for blob_sha256 keys."""
    stack = [(pointer, node)]
    while stack:
        ptr, current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                child = f"{ptr}/{pointer_token(key)}"
                if isinstance(key, str) and BLOB_SHA256_KEY.match(key):
                    yield child, key, value, current
                stack.append((child, value))
        elif isinstance(current, list):
            for index, value in enumerate(current):
                stack.append((f"{ptr}/{index}", value))


def bind_blob_sha256_path(container: dict, field: str) -> tuple[str | None, str | None]:
    """Find the path bound to a blob_sha256 declaration in its own mapping only."""
    match = BLOB_SHA256_KEY.match(field)
    if not match:
        return None, None

    base = match.group("base").rstrip("_")
    names = [f"{base}_path", f"{base}_file"] if base else []

    for name in names + ["path", "file"]:
        value = container.get(name)
        if nonempty(value):
            return name, value.strip()

    # A bare base key ("root" for "root_blob_sha256") counts only when its
    # value reads as a path, so a description string cannot be mistaken for one.
    value = container.get(base) if base else None
    if nonempty(value) and (
        "/" in value or re.search(r"\.[A-Za-z0-9]{1,8}$", value)
    ):
        return base, value.strip()

    return None, None


def discover_manifests(git: Git, commit: str) -> list[str]:
    names = git.run(
        "ls-tree", "-r", "--name-only", git.resolve_commit(commit)
    ).decode("utf-8", "strict").splitlines()
    return sorted(
        path for path in names
        if path.startswith(MANIFEST_ROOT + "/")
        and path.endswith("/manifest.yaml")
    )


def extract_manifest_pins(
    manifest_path: str,
    document: dict,
    default_commit: str,
    reference_mode_issues: list[ReferenceModeIssue] | None = None,
    allow_missing_reference_mode: bool = False,
) -> list[Pin]:
    """Extract supported pins and apply the Owner Option C reference semantics."""
    pins: list[Pin] = []
    issues = reference_mode_issues if reference_mode_issues is not None else []

    def add(
        field: str,
        path: Any,
        declared: Any,
        source_commit: Any = None,
        algorithm: str = "git",
        reference_mode: str = "current",
    ) -> None:
        if declared is None or (
            isinstance(declared, str) and not declared.strip()
        ):
            return
        normalized_path = path.strip() if isinstance(path, str) else ""
        if algorithm == "bytes":
            if isinstance(declared, bool) or not isinstance(declared, (int, str)):
                declared_text = repr(declared)
            else:
                declared_text = str(declared).strip()
        else:
            declared_text = (
                declared.strip() if isinstance(declared, str) else repr(declared)
            )
        pins.append(
            Pin(
                manifest=manifest_path,
                field=field,
                path=normalized_path,
                declared=declared_text,
                source_commit=(
                    source_commit.strip()
                    if isinstance(source_commit, str) and source_commit.strip()
                    else default_commit
                ),
                algorithm=algorithm,
                reference_mode=reference_mode,
            )
        )

    for path_key, digest_key in (
        ("root", "root_blob"),
        ("en_mirror", "en_mirror_blob"),
        ("zh_cn_mirror", "zh_cn_mirror_blob"),
    ):
        if digest_key in document:
            add(f"index.{path_key}", document.get(path_key), document.get(digest_key))

    for index, item in enumerate(document.get("gate_a_reconstruction", []) or []):
        if not isinstance(item, dict) or "reconstructed_root_blob" not in item:
            continue
        source = item.get("source_commit") or item.get("commit")
        if not source and nonempty(item.get("note")):
            match = re.search(r"\bcommit\s+([0-9a-f]{40})\b", item["note"])
            source = match.group(1) if match else None
        add(
            f"gate_a_reconstruction[{index}].root",
            item.get("root"),
            item.get("reconstructed_root_blob"),
            source,
        )

    source_evidence = as_mapping(document.get("baseline_and_source_evidence"))
    authored_indexes = source_evidence.get(
        "authored_indexes", document.get("authored_indexes", [])
    )
    for index, item in enumerate(authored_indexes or []):
        if not isinstance(item, dict):
            continue
        for path_key, digest_key in (
            ("root", "root_blob"),
            ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        ):
            if digest_key in item:
                add(
                    f"authored_indexes[{index}].{path_key}",
                    item.get(path_key),
                    item.get(digest_key),
                    reference_mode="historical",
                )

    for index, item in enumerate(document.get("related_evidence", []) or []):
        if not isinstance(item, dict):
            continue

        digest_keys = (
            ("path", "blob"),
            ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        )
        declared_pairs = [
            (path_key, digest_key)
            for path_key, digest_key in digest_keys
            if digest_key in item
        ]
        if not declared_pairs:
            continue

        mode_present = "reference_mode" in item
        mode_value = item.get("reference_mode")

        if not mode_present:
            if allow_missing_reference_mode:
                reference_mode = "current"
            else:
                issues.append(
                    ReferenceModeIssue(
                        manifest_path,
                        f"related_evidence[{index}].reference_mode",
                        "missing reference_mode",
                    )
                )
                reference_mode = "current"
        elif mode_value not in ("historical", "current"):
            issues.append(
                ReferenceModeIssue(
                    manifest_path,
                    f"related_evidence[{index}].reference_mode",
                    f"invalid reference_mode {mode_value!r}",
                )
            )
            reference_mode = "current"
        else:
            reference_mode = mode_value

        for path_key, digest_key in declared_pairs:
            add(
                f"related_evidence[{index}].{path_key}",
                item.get(path_key),
                item.get(digest_key),
                reference_mode=reference_mode,
            )

    if "evidence_blob" in document:
        add("evidence_file", document.get("evidence_file"), document.get("evidence_blob"))

    if "d_source_blobs" in document:
        source = document.get("d_source_commit")
        entries = document.get("d_source_blobs")
        if isinstance(entries, list):
            for index, entry in enumerate(entries):
                if not isinstance(entry, str) or ":" not in entry:
                    add(f"d_source_blobs[{index}]", "", repr(entry), source)
                    continue
                name, digest = entry.rsplit(":", 1)
                add(f"d_source_blobs[{index}]", name.strip(), digest.strip(), source)

    prompt = as_mapping(document.get("prompt"))
    if "prompt_sha256" in prompt:
        add(
            "prompt.prompt_file",
            prompt.get("prompt_file"),
            prompt.get("prompt_sha256"),
            algorithm="sha256",
        )
    if "prompt_bytes" in prompt:
        add(
            "prompt.prompt_file",
            prompt.get("prompt_file"),
            prompt.get("prompt_bytes"),
            algorithm="bytes",
        )

    for index, item in enumerate(document.get("session_evidence", []) or []):
        if not isinstance(item, dict):
            continue
        field = f"session_evidence[{index}].executed_prompt_snapshot_file"
        path_key = "executed_prompt_snapshot_file"
        if "executed_prompt_sha256" in item:
            add(
                field, item.get(path_key), item.get("executed_prompt_sha256"),
                algorithm="sha256",
            )
        if "executed_prompt_bytes" in item:
            add(
                field, item.get(path_key), item.get("executed_prompt_bytes"),
                algorithm="bytes",
            )
    return pins


def load_manifest_pins(
    git: Git,
    commit: str,
    manifest_path: str,
    reference_mode_issues: list[ReferenceModeIssue] | None = None,
    allow_missing_reference_mode: bool = False,
) -> list[Pin]:
    resolved = git.resolve_commit(commit)
    raw = git.object_bytes(resolved, manifest_path)
    try:
        document = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeError, yaml.YAMLError) as exc:
        raise Incomplete(
            f"cannot parse manifest {manifest_path} at {resolved}: {exc}"
        ) from exc
    if not isinstance(document, dict):
        raise Incomplete(
            f"manifest {manifest_path} at {resolved} is not a YAML mapping"
        )
    return extract_manifest_pins(
        manifest_path,
        document,
        resolved,
        reference_mode_issues=reference_mode_issues,
        allow_missing_reference_mode=allow_missing_reference_mode,
    )


def read_all_pins(
    git: Git,
    commit: str,
    allow_missing_reference_mode: bool = False,
) -> tuple[list[str], list[Pin], list[ReferenceModeIssue]]:
    resolved = git.resolve_commit(commit)
    manifests = discover_manifests(git, resolved)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {resolved}")
    pins: list[Pin] = []
    issues: list[ReferenceModeIssue] = []
    for manifest_path in manifests:
        pins.extend(
            load_manifest_pins(
                git,
                resolved,
                manifest_path,
                reference_mode_issues=issues,
                allow_missing_reference_mode=allow_missing_reference_mode,
            )
        )
    return manifests, pins, issues


def verify_blob_sha256_declarations(
    git: Git,
    commit: str,
    manifests: list[str],
) -> tuple[int, int, int, int, int, int, list[str]]:
    """Verify every non-empty blob_sha256 declaration in every manifest.

    These declarations are deliberately kept outside the append-only ledger
    identity model. They are independently checked against the candidate
    commit's file bytes and cannot silently become ledger-authorized pins.
    """
    pins = ok = mismatch = missing = incomplete = unbound = 0
    problems: list[str] = []

    for manifest_path in manifests:
        try:
            raw = git.object_bytes(commit, manifest_path)
            document = yaml.safe_load(raw.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError, Incomplete, Violation) as exc:
            # The normal manifest loader already checks this input. Keep this
            # second pass fail-closed if the tree cannot be read consistently.
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: {exc}")
            continue

        if not isinstance(document, dict):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: top-level YAML is not a mapping"
            )
            continue

        for pointer, field, declared, container in walk_declarations(document):
            # Empty/null placeholders are not blob identities.
            if declared is None or (
                isinstance(declared, str) and not declared.strip()
            ):
                continue

            pins += 1

            if isinstance(declared, bool) or not isinstance(declared, str):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer}: invalid digest declaration {declared!r}"
                )
                continue

            declared = declared.strip()
            _, path = bind_blob_sha256_path(container, field)

            if not path:
                unbound += 1
                problems.append(
                    f"UNBOUND_BLOB_SHA256 manifest={manifest_path} "
                    f"pointer={pointer} field={field} declared={declared}"
                )
                continue

            try:
                data = git.object_bytes(commit, path)
            except Violation:
                missing += 1
                problems.append(
                    f"PATH_MISSING blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} path={path} declared={declared}"
                )
                continue
            except Incomplete as exc:
                incomplete += 1
                problems.append(
                    f"INCOMPLETE blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} path={path}: {exc}"
                )
                continue

            actual = hashlib.sha256(data).hexdigest()
            if actual != declared.lower():
                mismatch += 1
                problems.append(
                    f"MISMATCH blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} path={path} declared={declared} "
                    f"actual={actual}"
                )
            else:
                ok += 1

    return pins, ok, mismatch, missing, incomplete, unbound, problems


def pin_map_for_manifest(
    git: Git,
    commit: str,
    manifest_path: str,
) -> dict[tuple[str, str, str, str, str], Pin]:
    pins = load_manifest_pins(git, commit, manifest_path)
    result: dict[tuple[str, str, str, str, str], Pin] = {}
    for pin in pins:
        if pin.value_identity in result:
            raise Incomplete(
                f"pin identity is not unique at {commit}: "
                f"{pin.manifest}::{pin.field}::{pin.path}::"
                f"{pin.reference_mode}::{pin.algorithm}"
            )
        result[pin.value_identity] = pin
    return result


def parse_ledger(raw: bytes) -> list[LedgerRecord]:
    """Parse legacy six-column and mode-aware seven-column ledger tables."""
    try:
        content = raw.decode("utf-8")
    except UnicodeError as exc:
        raise Incomplete(f"{LEDGER_PATH} is not UTF-8: {exc}") from exc

    lines = content.splitlines()
    headers: list[tuple[int, tuple[str, ...]]] = []

    for index, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = tuple(
            cell.strip().strip("`")
            for cell in line.strip().strip("|").split("|")
        )
        if cells in (LEDGER_HEADER, LEDGER_HEADER_V2):
            headers.append((index, cells))

    if not headers:
        raise Incomplete(
            f"{LEDGER_PATH} has no exact six-column or seven-column ledger header"
        )

    records: list[LedgerRecord] = []
    seen_transitions: set[tuple[tuple[str, str, str, str, str], str]] = set()

    for header_index, header in headers:
        columns = len(header)
        if header_index + 1 >= len(lines) or not LEDGER_SEPARATOR.fullmatch(
            lines[header_index + 1].strip()
        ):
            raise Incomplete(
                f"{LEDGER_PATH}: invalid Markdown table separator "
                f"after line {header_index + 1}"
            )

        separator_cells = [
            cell.strip()
            for cell in lines[header_index + 1].strip().strip("|").split("|")
        ]
        if len(separator_cells) != columns:
            raise Incomplete(
                f"{LEDGER_PATH}: separator must have {columns} columns"
            )

        for line_number in range(header_index + 2, len(lines)):
            stripped = lines[line_number].strip()
            if not stripped:
                break
            if not stripped.startswith("|") or not stripped.endswith("|"):
                break

            cells = [
                cell.strip().strip("`")
                for cell in stripped[1:-1].split("|")
            ]
            if len(cells) != columns or any(not cell for cell in cells):
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    f"expected {columns} non-empty cells"
                )

            if columns == 6:
                manifest, field, path, previous_pin, new_pin, repin_commit = cells
                reference_mode = "current"
            else:
                (
                    manifest,
                    field,
                    path,
                    reference_mode,
                    previous_pin,
                    new_pin,
                    repin_commit,
                ) = cells
                if reference_mode not in ("historical", "current"):
                    raise Incomplete(
                        f"{LEDGER_PATH}:{line_number + 1}: "
                        f"invalid reference_mode {reference_mode!r}"
                    )

            if manifest.startswith("/") or ".." in Path(manifest).parts:
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    f"invalid manifest path {manifest!r}"
                )
            if path.startswith("/") or ".." in Path(path).parts:
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    f"invalid pinned path {path!r}"
                )
            if not field.strip():
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: field must be non-empty"
                )

            valid_previous = (
                previous_pin.isdigit()
                or bool(HEX40.fullmatch(previous_pin))
                or bool(HEX64.fullmatch(previous_pin))
            )
            valid_new = (
                new_pin.isdigit()
                or bool(HEX40.fullmatch(new_pin))
                or bool(HEX64.fullmatch(new_pin))
            )
            if not valid_previous:
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    f"invalid previous_pin {previous_pin!r}"
                )
            if not valid_new:
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    f"invalid new_pin {new_pin!r}"
                )
            if not HEX40.fullmatch(repin_commit):
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    "repin_commit must be a full lowercase SHA"
                )

            record = LedgerRecord(
                manifest=manifest,
                field=field,
                path=path,
                previous_pin=previous_pin,
                new_pin=new_pin,
                repin_commit=repin_commit,
                reference_mode=reference_mode,
            )

            if record.algorithm == "bytes":
                valid_kind = previous_pin.isdigit() and new_pin.isdigit()
            elif record.algorithm == "sha256":
                valid_kind = bool(HEX64.fullmatch(previous_pin)) and bool(
                    HEX64.fullmatch(new_pin)
                )
            else:
                valid_kind = bool(HEX40.fullmatch(previous_pin)) and bool(
                    HEX40.fullmatch(new_pin)
                )
            if not valid_kind:
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: mixed pin kinds in ledger row"
                )

            transition_key = (record.value_identity, record.repin_commit)
            if transition_key in seen_transitions:
                raise Incomplete(
                    f"{LEDGER_PATH}:{line_number + 1}: "
                    "duplicate ledger transition across ledger tables"
                )
            seen_transitions.add(transition_key)
            records.append(record)

    return records


def pin_value_at(
    git: Git,
    commit: str,
    identity: tuple[str, str, str, str],
    algorithm: str,
) -> str:
    manifest_path, field, path, reference_mode = identity
    pins = load_manifest_pins(git, commit, manifest_path)
    matches = [
        pin for pin in pins
        if (
            pin.field == field
            and pin.path == path
            and pin.reference_mode == reference_mode
            and pin.algorithm == algorithm
        )
    ]
    if len(matches) != 1:
        raise Incomplete(
            f"cannot uniquely resolve pin identity at {commit}: "
            f"{manifest_path}::{field}::{path}::{reference_mode}::{algorithm} "
            f"(matches={len(matches)})"
        )
    return matches[0].declared


def read_baseline_commit(git: Git, target_commit: str) -> str:
    raw = git.object_bytes(target_commit, BASELINE_PATH)
    try:
        content = raw.decode("utf-8")
    except UnicodeError as exc:
        raise Incomplete(f"{BASELINE_PATH} is not UTF-8: {exc}") from exc
    match = BASELINE_COMMIT_RE.search(content)
    if not match:
        raise Incomplete(
            f"{BASELINE_PATH} does not declare "
            "'Measured against main <full-commit-sha>.'"
        )
    baseline = git.resolve_commit(match.group(1), "manifest pin baseline commit")
    if not git.is_ancestor(baseline, target_commit):
        raise Incomplete(
            f"manifest pin baseline {baseline} is not an ancestor "
            f"of target {target_commit}"
        )
    return baseline


def verify_unledgered_history(
    git: Git,
    baseline_commit: str,
    target_commit: str,
    records: list[LedgerRecord],
    target_mismatch_identities: set[tuple[str, str, str, str, str]],
) -> list[str]:
    """Check only target-mismatching identities after the committed baseline.

    Ledger rows are still checked against actual transitions. Rows at or before
    the baseline are historical context, not transitions to re-audit.
    """
    baseline = git.resolve_commit(baseline_commit, "manifest pin baseline")
    commits = git.first_parent_commits(baseline, target_commit)

    records_by_transition: dict[
        tuple[tuple[str, str, str, str, str], str], LedgerRecord
    ] = {}
    active_records: dict[
        tuple[tuple[str, str, str, str, str], str], LedgerRecord
    ] = {}
    for record in records:
        repin = git.resolve_commit(record.repin_commit, "ledger repin commit")
        if git.is_ancestor(repin, baseline):
            continue
        key = (record.value_identity, repin)
        if key in records_by_transition:
            raise Incomplete(
                f"duplicate ledger record for "
                f"{record.manifest}::{record.field}::{record.path} "
                f"({record.reference_mode}, {record.algorithm}) at {repin}"
            )
        records_by_transition[key] = record
        active_records[key] = record

    violations: list[str] = []
    scanned_transitions: set[
        tuple[tuple[str, str, str, str, str], str]
    ] = set()

    for commit in commits:
        parent = git.first_parent(commit)
        if parent is None:
            raise Incomplete(f"cannot inspect first parent of history commit {commit}")
        for manifest_path in git.changed_manifest_paths(parent, commit):
            if not git.has_path(parent, manifest_path):
                continue
            if not git.has_path(commit, manifest_path):
                continue
            before = pin_map_for_manifest(git, parent, manifest_path)
            after = pin_map_for_manifest(git, commit, manifest_path)

            for value_identity in sorted(set(before).intersection(after)):
                old_pin = before[value_identity]
                new_pin = after[value_identity]
                if old_pin.declared == new_pin.declared:
                    continue

                transition_key = (value_identity, commit)
                record = records_by_transition.get(transition_key)

                # Changes to unrelated identities are outside this baseline
                # authorization check unless a ledger row explicitly claims them.
                if value_identity not in target_mismatch_identities and record is None:
                    continue

                label = (
                    f"{old_pin.manifest}::{old_pin.field}::{old_pin.path}"
                    f" ({old_pin.reference_mode}, {old_pin.algorithm})"
                )
                if record is None:
                    violations.append(
                        f"VIOLATION unledgered pin transition at {commit}: "
                        f"{label}: {old_pin.declared} -> {new_pin.declared}"
                    )
                    continue
                if (
                    record.previous_pin != old_pin.declared
                    or record.new_pin != new_pin.declared
                ):
                    violations.append(
                        f"VIOLATION ledger row does not authorize actual "
                        f"transition at {commit}: {label}: "
                        f"actual={old_pin.declared}->{new_pin.declared} "
                        f"ledger={record.previous_pin}->{record.new_pin}"
                    )
                    continue
                scanned_transitions.add(transition_key)

    for key, record in active_records.items():
        if key not in scanned_transitions:
            violations.append(
                f"VIOLATION ledger repin is not a matching first-parent "
                f"manifest transition: {record.manifest}::{record.field}::"
                f"{record.path} ({record.reference_mode}, {record.algorithm}) "
                f"at {record.repin_commit}"
            )
    return violations


def verify_ledger(
    git: Git,
    target_commit: str,
    target_manifests: list[str],
    target_pins: list[Pin],
    target_mismatch_identities: set[tuple[str, str, str, str, str]],
    allow_missing_ledger: bool = False,
) -> tuple[list[str], int]:
    """Validate mode-separated ledger chains and prove recorded transitions."""
    resolved_target = git.resolve_commit(target_commit)
    tree_paths = set(
        git.run(
            "ls-tree", "-r", "--name-only", resolved_target
        ).decode("utf-8", "strict").splitlines()
    )
    if BASELINE_PATH not in tree_paths:
        return [], 0
    if LEDGER_PATH not in tree_paths:
        if allow_missing_ledger:
            return [], 0
        raise Incomplete(
            f"{LEDGER_PATH} is absent from commit {resolved_target}; "
            "ledger must be present before pin verification can pass"
        )

    records = parse_ledger(git.object_bytes(resolved_target, LEDGER_PATH))
    grouped: dict[tuple[str, str, str, str, str], list[LedgerRecord]] = defaultdict(list)
    for record in records:
        grouped[record.value_identity].append(record)

    target_pin_map: dict[
        tuple[str, str, str, str, str], list[Pin]
    ] = defaultdict(list)
    for pin in target_pins:
        target_pin_map[pin.value_identity].append(pin)

    baseline_commit = read_baseline_commit(git, resolved_target)

    for value_identity, chain in grouped.items():
        manifest_path, field, path, reference_mode, algorithm = value_identity
        if manifest_path not in target_manifests:
            raise Incomplete(
                f"ledger identity references absent manifest: {manifest_path}"
            )
        previous_new: str | None = None
        for record in chain:
            repin = git.resolve_commit(
                record.repin_commit,
                f"ledger repin_commit for {manifest_path}::{field}",
            )
            parent = git.first_parent(repin)
            if parent is None:
                raise Incomplete(f"repin commit {repin} has no first parent")
            if previous_new is not None and record.previous_pin != previous_new:
                raise Incomplete(
                    f"ledger history discontinuity for "
                    f"{manifest_path}::{field}::{path}::{reference_mode}: "
                    f"expected previous_pin={previous_new}, "
                    f"found {record.previous_pin}"
                )
            parent_value = pin_value_at(git, parent, record.identity, algorithm)
            repin_value = pin_value_at(git, repin, record.identity, algorithm)
            if parent_value != record.previous_pin:
                raise Incomplete(
                    f"ledger previous_pin does not match first parent for "
                    f"{manifest_path}::{field}::{path}::{reference_mode} "
                    f"at {repin}: ledger={record.previous_pin} "
                    f"actual={parent_value}"
                )
            if repin_value != record.new_pin:
                raise Incomplete(
                    f"ledger new_pin does not match repin commit for "
                    f"{manifest_path}::{field}::{path}::{reference_mode} "
                    f"at {repin}: ledger={record.new_pin} "
                    f"actual={repin_value}"
                )
            if not git.is_ancestor(repin, resolved_target):
                raise Incomplete(
                    f"ledger repin commit {repin} is not an ancestor "
                    f"of target {resolved_target}"
                )
            previous_new = record.new_pin

        latest = chain[-1].new_pin
        target_matches = target_pin_map.get(value_identity, [])
        if len(target_matches) != 1:
            raise Incomplete(
                f"latest ledger identity is not unique in target tree: "
                f"{manifest_path}::{field}::{path}::"
                f"{reference_mode}::{algorithm}"
            )
        if target_matches[0].declared != latest:
            raise Incomplete(
                f"target pin does not equal latest ledger new_pin for "
                f"{manifest_path}::{field}::{path}::{reference_mode}: "
                f"ledger={latest} target={target_matches[0].declared}"
            )

    history_violations = verify_unledgered_history(
        git,
        baseline_commit,
        resolved_target,
        records,
        target_mismatch_identities,
    )
    return history_violations, len(records)


def verify_reference_modes(
    git: Git,
    target_commit: str,
    pins: list[Pin],
    issues: list[ReferenceModeIssue],
) -> tuple[int, int, int, list[str]]:
    """Verify historical pins against any reachable blob at the declared path."""
    mismatch = 0
    incomplete = 0
    ok = 0
    problems: list[str] = []

    for issue in issues:
        incomplete += 1
        problems.append(
            f"INCOMPLETE {issue.field} manifest={issue.manifest}: "
            f"{issue.reason}"
        )

    for pin in pins:
        if pin.reference_mode != "historical":
            continue

        if pin.algorithm != "git":
            incomplete += 1
            problems.append(
                f"INCOMPLETE {pin.field} path={pin.path}: "
                "historical reference_mode requires a Git blob SHA-1 pin"
            )
            continue

        if not HEX40.fullmatch(pin.declared):
            incomplete += 1
            problems.append(
                f"INCOMPLETE {pin.field} path={pin.path}: "
                f"invalid historical Git blob declaration {pin.declared!r}"
            )
            continue

        if not pin.path:
            mismatch += 1
            problems.append(
                f"MISMATCH {pin.field} path=<not-declared> "
                f"declared={pin.declared} "
                "actual=not-found-in-reachable-history"
            )
            continue

        try:
            exists = git.historical_blob_exists(
                target_commit,
                pin.path,
                pin.declared,
            )
        except Incomplete as exc:
            incomplete += 1
            problems.append(
                f"INCOMPLETE {pin.field} path={pin.path}: {exc}"
            )
            continue

        if exists:
            ok += 1
        else:
            mismatch += 1
            problems.append(
                f"MISMATCH {pin.field} path={pin.path} "
                f"declared={pin.declared} "
                "actual=not-found-in-reachable-history"
            )

    return ok, mismatch, incomplete, problems


def verify(
    root: Path,
    commit: str,
    verbose: bool = True,
    allow_missing_ledger: bool = False,
    allow_missing_reference_mode: bool = False,
) -> int:
    git = Git(root)
    resolved = git.resolve_commit(commit, "candidate commit")
    manifests, pins_list, reference_mode_issues = read_all_pins(
        git,
        resolved,
        allow_missing_reference_mode=allow_missing_reference_mode,
    )

    ok = mismatch = missing = incomplete = 0
    unbound = 0
    problems: list[str] = []
    mismatch_identities: set[tuple[str, str, str, str, str]] = set()
    pins = len(pins_list)

    (
        historical_ok,
        historical_mismatch,
        historical_incomplete,
        historical_problems,
    ) = verify_reference_modes(
        git,
        resolved,
        pins_list,
        reference_mode_issues,
    )
    ok += historical_ok
    mismatch += historical_mismatch
    incomplete += historical_incomplete
    problems.extend(historical_problems)

    for pin in pins_list:
        if pin.reference_mode == "historical":
            continue

        declared = pin.declared
        path = pin.path
        kind = pin.field

        if pin.algorithm == "bytes":
            if not declared or not re.fullmatch(r"[0-9]+", declared):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE {kind}: invalid byte-count declaration {declared!r}"
                )
                continue
        elif pin.algorithm == "sha256":
            if not HEX64.fullmatch(declared):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE {kind}: invalid SHA-256 declaration {declared!r}"
                )
                continue
        elif not HEX40.fullmatch(declared):
            incomplete += 1
            problems.append(
                f"INCOMPLETE {kind}: invalid Git blob declaration {declared!r}"
            )
            continue

        if not path:
            missing += 1
            problems.append(
                f"PATH_MISSING {kind} path=<not-declared> declared={declared}"
            )
            continue

        try:
            data = git.object_bytes(pin.source_commit, path)
        except Violation as exc:
            missing += 1
            problems.append(f"{exc}; declared={declared}")
            continue
        except Incomplete as exc:
            incomplete += 1
            problems.append(f"INCOMPLETE {kind} path={path}: {exc}")
            continue

        if pin.algorithm == "sha256":
            actual = hashlib.sha256(data).hexdigest()
        elif pin.algorithm == "bytes":
            actual = str(len(data))
        else:
            actual = git_blob_sha(data)

        if actual != declared.lower():
            mismatch += 1
            mismatch_identities.add(pin.value_identity)
            problems.append(
                f"MISMATCH {kind} path={path} "
                f"declared={declared} actual={actual}"
            )
        else:
            ok += 1

    (
        blob_pins,
        blob_ok,
        blob_mismatch,
        blob_missing,
        blob_incomplete,
        blob_unbound,
        blob_problems,
    ) = verify_blob_sha256_declarations(git, resolved, manifests)

    pins += blob_pins
    ok += blob_ok
    mismatch += blob_mismatch
    missing += blob_missing
    incomplete += blob_incomplete
    unbound += blob_unbound
    problems.extend(blob_problems)

    ledger_records: int | None = None
    try:
        ledger_violations, ledger_records = verify_ledger(
            git,
            resolved,
            manifests,
            pins_list,
            mismatch_identities,
            allow_missing_ledger=allow_missing_ledger,
        )
        problems.extend(ledger_violations)
    except Violation as exc:
        problems.append(f"VIOLATION ledger={LEDGER_PATH}: {exc}")
    except Incomplete as exc:
        incomplete += 1
        problems.append(f"INCOMPLETE ledger={LEDGER_PATH}: {exc}")

    if verbose:
        print(
            f"main={resolved} manifests={len(manifests)} pins={pins} "
            f"ok={ok} mismatch={mismatch} path_missing={missing} "
            f"incomplete={incomplete} unbound={unbound}"
        )
        if ledger_records is not None:
            print(f"ledger_records={ledger_records}")
        for problem in problems:
            print(problem)

    has_violation = (
        mismatch > 0
        or missing > 0
        or unbound > 0
        or any(problem.startswith("VIOLATION ") for problem in problems)
    )
    if incomplete:
        return 2
    if has_violation:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument(
        "--allow-missing-ledger",
        action="store_true",
        help="Allow a pre-ledger base measurement to omit the ledger; "
             "never use for candidate verification.",
    )
    parser.add_argument(
        "--allow-missing-reference-mode",
        action="store_true",
        help="Treat an absent related_evidence.reference_mode as legacy "
             "current mode for base measurement only; invalid values still fail.",
    )
    args = parser.parse_args(argv)

    try:
        git = Git(args.root)
        commit = git.resolve_commit(args.commit, "candidate commit")
        return verify(
            args.root,
            commit,
            allow_missing_ledger=args.allow_missing_ledger,
            allow_missing_reference_mode=args.allow_missing_reference_mode,
        )
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
