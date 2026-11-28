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
BLOB_SHA256_KEY = re.compile(r"^(?P<base>(?:.*_)?)blob_sha256(?:_[a-z0-9]+)*$")
LEDGER_HEADER = (
    "manifest", "field", "path", "previous_pin", "new_pin", "repin_commit",
)
LEDGER_SEPARATOR = re.compile(
    r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*){5}\|?$"
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

    @property
    def identity(self) -> tuple[str, str, str]:
        return (self.manifest, self.field, self.path)

    @property
    def value_identity(self) -> tuple[str, str, str, str]:
        return (*self.identity, self.algorithm)


@dataclass(frozen=True)
class LedgerRecord:
    manifest: str
    field: str
    path: str
    previous_pin: str
    new_pin: str
    repin_commit: str

    @property
    def identity(self) -> tuple[str, str, str]:
        return (self.manifest, self.field, self.path)

    @property
    def algorithm(self) -> str:
        if self.previous_pin.isdigit() and self.new_pin.isdigit():
            return "bytes"
        if HEX64.fullmatch(self.previous_pin) and HEX64.fullmatch(self.new_pin):
            return "sha256"
        return "git"

    @property
    def value_identity(self) -> tuple[str, str, str, str]:
        return (*self.identity, self.algorithm)


class Git:
    def __init__(self, root: Path):
        self.root = root

    def run(self, *args: str) -> bytes:
        try:
            result = subprocess.run(
                ["git", *args], cwd=self.root, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot execute git: {exc}") from exc
        if result.returncode:
            detail = result.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(detail or f"git {' '.join(args)} failed ({result.returncode})")
        return result.stdout

    def resolve_commit(self, ref: str, description: str = "commit") -> str:
        if not isinstance(ref, str) or not ref.strip():
            raise Incomplete(f"{description} is absent")
        try:
            resolved = self.run(
                "rev-parse", "--verify", f"{ref.strip()}^{{commit}}"
            ).decode("ascii", "strict").strip()
        except (Incomplete, UnicodeError) as exc:
            raise Incomplete(f"{description} cannot be resolved: {ref!r}") from exc
        if not HEX40.fullmatch(resolved):
            raise Incomplete(f"{description} did not resolve to a full commit SHA: {ref!r}")
        return resolved

    def object_bytes(self, commit: str, path: str) -> bytes:
        if not isinstance(path, str) or not path.strip():
            raise Violation("PATH_MISSING path=<not-declared>")
        resolved = self.resolve_commit(commit, f"source commit for {path}")
        spec = f"{resolved}:{path}"
        try:
            result = subprocess.run(
                ["git", "cat-file", "blob", spec], cwd=self.root,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot read Git blob {spec}: {exc}") from exc
        if result.returncode:
            raise Violation(f"PATH_MISSING path={path}")
        return result.stdout

    def blob_oid(self, commit: str, path: str) -> str:
        """Return the exact Git blob object ID for path in commit's tree."""
        resolved = self.resolve_commit(commit)
        try:
            oid = self.run("rev-parse", "--verify", f"{resolved}:{path}").decode(
                "ascii", "strict"
            ).strip()
        except (Incomplete, UnicodeError) as exc:
            raise Incomplete(
                f"cannot resolve manifest blob {path} at {resolved}"
            ) from exc
        if not HEX40.fullmatch(oid):
            raise Incomplete(
                f"manifest path {path} at {resolved} is not a Git blob"
            )
        kind = self.run("cat-file", "-t", oid).decode("ascii", "strict").strip()
        if kind != "blob":
            raise Incomplete(f"manifest path {path} at {resolved} is not a blob")
        return oid

    def has_path(self, commit: str, path: str) -> bool:
        resolved = self.resolve_commit(commit)
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{resolved}:{path}"], cwd=self.root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
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
            ["git", "merge-base", "--is-ancestor", a, d], cwd=self.root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
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
        output = self.run("rev-list", "--first-parent", "--reverse", f"{old}..{new}")
        commits = [
            line.strip() for line in output.decode("ascii", "strict").splitlines()
            if line.strip()
        ]
        for commit in commits:
            if not HEX40.fullmatch(commit):
                raise Incomplete(f"invalid commit in first-parent history: {commit!r}")
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
    match = BLOB_SHA256_KEY.match(field)
    if not match:
        return None, None
    base = match.group("base").rstrip("_")
    names = [f"{base}_path", f"{base}_file"] if base else []
    for name in names + ["path", "file"]:
        value = container.get(name)
        if nonempty(value):
            return name, value.strip()
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
    manifest_path: str, document: dict, default_commit: str,
) -> list[Pin]:
    pins: list[Pin] = []

    def add(
        field: str, path: Any, declared: Any, source_commit: Any = None,
        algorithm: str = "git",
    ) -> None:
        if declared is None or (isinstance(declared, str) and not declared.strip()):
            return
        normalized_path = path.strip() if isinstance(path, str) else ""
        if algorithm == "bytes":
            if isinstance(declared, bool) or not isinstance(declared, (int, str)):
                declared_text = repr(declared)
            else:
                declared_text = str(declared).strip()
        else:
            declared_text = declared.strip() if isinstance(declared, str) else repr(declared)
        pins.append(Pin(
            manifest_path, field, normalized_path, declared_text,
            source_commit.strip() if isinstance(source_commit, str) and source_commit.strip()
            else default_commit, algorithm,
        ))

    for path_key, digest_key in (
        ("root", "root_blob"), ("en_mirror", "en_mirror_blob"),
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
            f"gate_a_reconstruction[{index}].root", item.get("root"),
            item.get("reconstructed_root_blob"), source,
        )

    source_evidence = as_mapping(document.get("baseline_and_source_evidence"))
    authored_indexes = source_evidence.get(
        "authored_indexes", document.get("authored_indexes", [])
    )
    for index, item in enumerate(authored_indexes or []):
        if not isinstance(item, dict):
            continue
        for path_key, digest_key in (
            ("root", "root_blob"), ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        ):
            if digest_key in item:
                add(
                    f"authored_indexes[{index}].{path_key}",
                    item.get(path_key), item.get(digest_key),
                )

    for index, item in enumerate(document.get("related_evidence", []) or []):
        if not isinstance(item, dict):
            continue
        for path_key, digest_key in (
            ("path", "blob"), ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        ):
            if digest_key in item:
                add(
                    f"related_evidence[{index}].{path_key}",
                    item.get(path_key), item.get(digest_key),
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
        add("prompt.prompt_file", prompt.get("prompt_file"), prompt.get("prompt_sha256"),
            algorithm="sha256")
    if "prompt_bytes" in prompt:
        add("prompt.prompt_file", prompt.get("prompt_file"), prompt.get("prompt_bytes"),
            algorithm="bytes")

    for index, item in enumerate(document.get("session_evidence", []) or []):
        if not isinstance(item, dict):
            continue
        field = f"session_evidence[{index}].executed_prompt_snapshot_file"
        path_key = "executed_prompt_snapshot_file"
        if "executed_prompt_sha256" in item:
            add(field, item.get(path_key), item.get("executed_prompt_sha256"),
                algorithm="sha256")
        if "executed_prompt_bytes" in item:
            add(field, item.get(path_key), item.get("executed_prompt_bytes"),
                algorithm="bytes")
    return pins


def load_manifest_pins(git: Git, commit: str, manifest_path: str) -> list[Pin]:
    resolved = git.resolve_commit(commit)
    raw = git.object_bytes(resolved, manifest_path)
    try:
        document = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeError, yaml.YAMLError) as exc:
        raise Incomplete(f"cannot parse manifest {manifest_path} at {resolved}: {exc}") from exc
    if not isinstance(document, dict):
        raise Incomplete(f"manifest {manifest_path} at {resolved} is not a YAML mapping")
    return extract_manifest_pins(manifest_path, document, resolved)


def read_all_pins(git: Git, commit: str) -> tuple[list[str], list[Pin]]:
    resolved = git.resolve_commit(commit)
    manifests = discover_manifests(git, resolved)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {resolved}")
    pins: list[Pin] = []
    for manifest_path in manifests:
        pins.extend(load_manifest_pins(git, resolved, manifest_path))
    return manifests, pins


def verify_blob_sha256_declarations(
    git: Git, commit: str, manifests: list[str],
) -> tuple[int, int, int, int, int, int, list[str]]:
    pins = ok = mismatch = missing = incomplete = unbound = 0
    problems: list[str] = []
    for manifest_path in manifests:
        try:
            raw = git.object_bytes(commit, manifest_path)
            document = yaml.safe_load(raw.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError, Incomplete, Violation) as exc:
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
            if declared is None or (isinstance(declared, str) and not declared.strip()):
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
                    f"pointer={pointer} path={path} declared={declared} actual={actual}"
                )
            else:
                ok += 1
    return pins, ok, mismatch, missing, incomplete, unbound, problems


def pin_map_for_manifest(
    git: Git, commit: str, manifest_path: str,
) -> dict[tuple[str, str, str, str], Pin]:
    pins = load_manifest_pins(git, commit, manifest_path)
    result: dict[tuple[str, str, str, str], Pin] = {}
    for pin in pins:
        if pin.value_identity in result:
            raise Incomplete(
                f"pin identity is not unique at {commit}: "
                f"{pin.manifest}::{pin.field}::{pin.path}::{pin.algorithm}"
            )
        result[pin.value_identity] = pin
    return result


def parse_ledger(raw: bytes) -> list[LedgerRecord]:
    try:
        content = raw.decode("utf-8")
    except UnicodeError as exc:
        raise Incomplete(f"{LEDGER_PATH} is not UTF-8: {exc}") from exc
    lines = content.splitlines()
    header_index = None
    for index, line in enumerate(lines):
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if tuple(cells) == LEDGER_HEADER:
            header_index = index
            break
    if header_index is None:
        raise Incomplete(f"{LEDGER_PATH} has no exact six-column ledger header")
    if header_index + 1 >= len(lines) or not LEDGER_SEPARATOR.fullmatch(
        lines[header_index + 1].strip()
    ):
        raise Incomplete(f"{LEDGER_PATH} has an invalid Markdown table separator")
    records: list[LedgerRecord] = []
    for line_number, line in enumerate(lines[header_index + 2:], start=header_index + 3):
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("|") or not stripped.endswith("|"):
            raise Incomplete(
                f"{LEDGER_PATH}:{line_number}: ledger row must be a pipe table row"
            )
        cells = [cell.strip().strip("`") for cell in stripped[1:-1].split("|")]
        if len(cells) != 6 or any(not cell for cell in cells):
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: expected six non-empty cells")
        manifest, field, path, previous_pin, new_pin, repin_commit = cells
        if manifest.startswith("/") or ".." in Path(manifest).parts:
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: invalid manifest path {manifest!r}")
        if path.startswith("/") or ".." in Path(path).parts:
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: invalid pinned path {path!r}")
        if not field.strip():
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: field must be non-empty")
        valid_previous = previous_pin.isdigit() or bool(HEX40.fullmatch(previous_pin)) or bool(HEX64.fullmatch(previous_pin))
        valid_new = new_pin.isdigit() or bool(HEX40.fullmatch(new_pin)) or bool(HEX64.fullmatch(new_pin))
        if not valid_previous:
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: invalid previous_pin {previous_pin!r}")
        if not valid_new:
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: invalid new_pin {new_pin!r}")
        if not HEX40.fullmatch(repin_commit):
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: repin_commit must be a full lowercase SHA")
        record = LedgerRecord(manifest, field, path, previous_pin, new_pin, repin_commit)
        if record.algorithm == "bytes":
            valid_kind = previous_pin.isdigit() and new_pin.isdigit()
        elif record.algorithm == "sha256":
            valid_kind = bool(HEX64.fullmatch(previous_pin)) and bool(HEX64.fullmatch(new_pin))
        else:
            valid_kind = bool(HEX40.fullmatch(previous_pin)) and bool(HEX40.fullmatch(new_pin))
        if not valid_kind:
            raise Incomplete(f"{LEDGER_PATH}:{line_number}: mixed pin kinds in ledger row")
        records.append(record)
    return records


def pin_value_at(
    git: Git, commit: str, identity: tuple[str, str, str], algorithm: str,
) -> str:
    manifest_path, field, path = identity
    pins = load_manifest_pins(git, commit, manifest_path)
    matches = [
        pin for pin in pins
        if pin.field == field and pin.path == path and pin.algorithm == algorithm
    ]
    if len(matches) != 1:
        raise Incomplete(
            f"cannot uniquely resolve pin identity at {commit}: "
            f"{manifest_path}::{field}::{path}::{algorithm} (matches={len(matches)})"
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
            f"manifest pin baseline {baseline} is not an ancestor of target {target_commit}"
        )
    return baseline


def resolve_ledger_transition(
    git: Git,
    record: LedgerRecord,
    original_repin: str,
    baseline_commit: str,
    target_commit: str,
) -> str:
    """Prove the original repin and return its actual target-history transition.

    For squash merges, the original commit remains the evidence source. A
    first-parent target commit is accepted as its equivalent only if the
    before/after pin values and the exact manifest blob object ID agree.
    """
    parent = git.first_parent(original_repin)
    if parent is None:
        raise Incomplete(f"repin commit {original_repin} has no first parent")

    parent_value = pin_value_at(git, parent, record.identity, record.algorithm)
    repin_value = pin_value_at(git, original_repin, record.identity, record.algorithm)
    if parent_value != record.previous_pin:
        raise Incomplete(
            f"ledger previous_pin does not match first parent for "
            f"{record.manifest}::{record.field}::{record.path} at {original_repin}: "
            f"ledger={record.previous_pin} actual={parent_value}"
        )
    if repin_value != record.new_pin:
        raise Incomplete(
            f"ledger new_pin does not match repin commit for "
            f"{record.manifest}::{record.field}::{record.path} at {original_repin}: "
            f"ledger={record.new_pin} actual={repin_value}"
        )

    if git.is_ancestor(original_repin, target_commit):
        return original_repin

    original_manifest_blob = git.blob_oid(original_repin, record.manifest)
    candidates: list[str] = []
    for candidate in git.first_parent_commits(baseline_commit, target_commit):
        candidate_parent = git.first_parent(candidate)
        if candidate_parent is None:
            raise Incomplete(f"cannot inspect first parent of history commit {candidate}")
        if record.manifest not in git.changed_manifest_paths(candidate_parent, candidate):
            continue
        if not git.has_path(candidate_parent, record.manifest):
            continue
        if not git.has_path(candidate, record.manifest):
            continue
        before = pin_value_at(git, candidate_parent, record.identity, record.algorithm)
        after = pin_value_at(git, candidate, record.identity, record.algorithm)
        if before != record.previous_pin or after != record.new_pin:
            continue
        if git.blob_oid(candidate, record.manifest) != original_manifest_blob:
            continue
        candidates.append(candidate)

    if len(candidates) != 1:
        if not candidates:
            detail = "no matching first-parent squash transition"
        else:
            detail = f"multiple matching first-parent squash transitions: {candidates}"
        raise Incomplete(
            f"ledger repin commit {original_repin} is not an ancestor of target "
            f"{target_commit}; {detail}"
        )
    return candidates[0]


def verify_unledgered_history(
    git: Git,
    baseline_commit: str,
    target_commit: str,
    records: list[LedgerRecord],
    target_mismatch_identities: set[tuple[str, str, str, str]],
    effective_commits: dict[LedgerRecord, str],
) -> list[str]:
    """Check target-mismatching identities against authorized first-parent transitions."""
    baseline = git.resolve_commit(baseline_commit, "manifest pin baseline")
    commits = git.first_parent_commits(baseline, target_commit)
    records_by_transition: dict[
        tuple[tuple[str, str, str, str], str], LedgerRecord
    ] = {}
    active_records: dict[
        tuple[tuple[str, str, str, str], str], LedgerRecord
    ] = {}
    for record in records:
        effective = effective_commits[record]
        if git.is_ancestor(effective, baseline):
            continue
        key = (record.value_identity, effective)
        if key in records_by_transition:
            raise Incomplete(
                f"duplicate ledger record for {record.manifest}::{record.field}::"
                f"{record.path} ({record.algorithm}) at {effective}"
            )
        records_by_transition[key] = record
        active_records[key] = record

    violations: list[str] = []
    scanned_transitions: set[tuple[tuple[str, str, str, str], str]] = set()
    for commit in commits:
        parent = git.first_parent(commit)
        if parent is None:
            raise Incomplete(f"cannot inspect first parent of history commit {commit}")
        for manifest_path in git.changed_manifest_paths(parent, commit):
            if not git.has_path(parent, manifest_path) or not git.has_path(commit, manifest_path):
                continue
            before = pin_map_for_manifest(git, parent, manifest_path)
            after = pin_map_for_manifest(git, commit, manifest_path)
            for value_identity in sorted(set(before).intersection(after)):
                old_pin, new_pin = before[value_identity], after[value_identity]
                if old_pin.declared == new_pin.declared:
                    continue
                transition_key = (value_identity, commit)
                record = records_by_transition.get(transition_key)
                if value_identity not in target_mismatch_identities and record is None:
                    continue
                label = (
                    f"{old_pin.manifest}::{old_pin.field}::{old_pin.path}"
                    f" ({old_pin.algorithm})"
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
                        f"VIOLATION ledger row does not authorize actual transition "
                        f"at {commit}: {label}: actual={old_pin.declared}->{new_pin.declared} "
                        f"ledger={record.previous_pin}->{record.new_pin}"
                    )
                    continue
                scanned_transitions.add(transition_key)

    for key, record in active_records.items():
        if key not in scanned_transitions:
            violations.append(
                f"VIOLATION ledger repin is not a matching first-parent "
                f"manifest transition: {record.manifest}::{record.field}::"
                f"{record.path} ({record.algorithm}) at {effective_commits[record]}"
            )
    return violations


def verify_ledger(
    git: Git,
    target_commit: str,
    target_manifests: list[str],
    target_pins: list[Pin],
    target_mismatch_identities: set[tuple[str, str, str, str]],
    allow_missing_ledger: bool = False,
) -> tuple[list[str], int]:
    """Validate ledger chains and prove recorded transitions in Git."""
    resolved_target = git.resolve_commit(target_commit)
    tree_paths = set(git.run(
        "ls-tree", "-r", "--name-only", resolved_target
    ).decode("utf-8", "strict").splitlines())
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
    grouped: dict[tuple[str, str, str, str], list[LedgerRecord]] = defaultdict(list)
    for record in records:
        grouped[record.value_identity].append(record)
    target_pin_map: dict[tuple[str, str, str, str], list[Pin]] = defaultdict(list)
    for pin in target_pins:
        target_pin_map[pin.value_identity].append(pin)
    baseline_commit = read_baseline_commit(git, resolved_target)

    effective_commits: dict[LedgerRecord, str] = {}
    for value_identity, chain in grouped.items():
        manifest_path, field, path, algorithm = value_identity
        if manifest_path not in target_manifests:
            raise Incomplete(f"ledger identity references absent manifest: {manifest_path}")
        previous_new: str | None = None
        for record in chain:
            repin = git.resolve_commit(
                record.repin_commit, f"ledger repin_commit for {manifest_path}::{field}"
            )
            if previous_new is not None and record.previous_pin != previous_new:
                raise Incomplete(
                    f"ledger history discontinuity for {manifest_path}::{field}::{path}: "
                    f"expected previous_pin={previous_new}, found {record.previous_pin}"
                )
            effective_commits[record] = resolve_ledger_transition(
                git, record, repin, baseline_commit, resolved_target
            )
            previous_new = record.new_pin

        latest = chain[-1].new_pin
        target_matches = target_pin_map.get(value_identity, [])
        if len(target_matches) != 1:
            raise Incomplete(
                f"latest ledger identity is not unique in target tree: "
                f"{manifest_path}::{field}::{path}::{algorithm}"
            )
        if target_matches[0].declared != latest:
            raise Incomplete(
                f"target pin does not equal latest ledger new_pin for "
                f"{manifest_path}::{field}::{path}: ledger={latest} "
                f"target={target_matches[0].declared}"
            )

    history_violations = verify_unledgered_history(
        git, baseline_commit, resolved_target, records,
        target_mismatch_identities, effective_commits,
    )
    return history_violations, len(records)


def verify(
    root: Path, commit: str, verbose: bool = True,
    allow_missing_ledger: bool = False,
) -> int:
    git = Git(root)
    resolved = git.resolve_commit(commit, "candidate commit")
    manifests, pins_list = read_all_pins(git, resolved)
    ok = mismatch = missing = incomplete = 0
    unbound = 0
    problems: list[str] = []
    mismatch_identities: set[tuple[str, str, str, str]] = set()
    pins = len(pins_list)

    for pin in pins_list:
        declared, path, kind = pin.declared, pin.path, pin.field
        if pin.algorithm == "bytes":
            if not declared or not re.fullmatch(r"[0-9]+", declared):
                incomplete += 1
                problems.append(f"INCOMPLETE {kind}: invalid byte-count declaration {declared!r}")
                continue
        elif pin.algorithm == "sha256":
            if not HEX64.fullmatch(declared):
                incomplete += 1
                problems.append(f"INCOMPLETE {kind}: invalid SHA-256 declaration {declared!r}")
                continue
        elif not HEX40.fullmatch(declared):
            incomplete += 1
            problems.append(f"INCOMPLETE {kind}: invalid Git blob declaration {declared!r}")
            continue
        if not path:
            missing += 1
            problems.append(f"PATH_MISSING {kind} path=<not-declared> declared={declared}")
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
            problems.append(f"MISMATCH {kind} path={path} declared={declared} actual={actual}")
        else:
            ok += 1

    (
        blob_pins, blob_ok, blob_mismatch, blob_missing,
        blob_incomplete, blob_unbound, blob_problems,
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
            git, resolved, manifests, pins_list, mismatch_identities,
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
        mismatch > 0 or missing > 0 or unbound > 0
        or any(problem.startswith("VIOLATION ") for problem in problems)
    )
    if incomplete:
        return 2
    if has_violation:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument(
        "--allow-missing-ledger", action="store_true",
        help="Allow a pre-ledger base measurement to omit the ledger; "
             "never use for candidate verification.",
    )
    args = parser.parse_args(argv)
    try:
        git = Git(args.root)
        commit = git.resolve_commit(args.commit, "candidate commit")
        return verify(
            args.root, commit, allow_missing_ledger=args.allow_missing_ledger,
        )
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
