#!/usr/bin/env python3
"""Safely repin exactly the manifest byte-count mismatches in the baseline.

Default mode is read-only. Use --apply to write the authorized manifest files.
The two AID-2026-261 PATH_MISSING sentinel rows are deliberately preserved.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


MANIFEST_ROOT = "14-ai-development/work-items"
BASELINE_DEFAULT = "scripts/ci/baselines/manifest-blob-pins.txt"
CHECKER_DEFAULT = "scripts/ci/check_manifest_blob_pins.py"

EXPECTED_SENTINELS = 2
SENTINEL_PATH = (
    "14-ai-development/work-items/AID-2026-261/prompt-v1.md"
)
SENTINEL_DECLARATIONS = {
    "0",
    "0000000000000000000000000000000000000000000000000000000000000000",
}
EXPECTED_SENTINEL_ROWS = Counter(
    {
        (SENTINEL_PATH, "0"): 1,
        (
            SENTINEL_PATH,
            "0000000000000000000000000000000000000000000000000000000000000000",
        ): 1,
    }
)

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MISMATCH_RE = re.compile(
    r"^MISMATCH (?P<field>\S+) path=(?P<path>\S+) "
    r"declared=(?P<declared>\S+) actual=(?P<actual>\S+)$"
)
MISSING_RE = re.compile(
    r"^PATH_MISSING path=(?P<path>\S+); declared=(?P<declared>\S+)$"
)
SESSION_BYTES_FIELD_RE = re.compile(
    r"^session_evidence\[[0-9]+\]\.executed_prompt_snapshot_file$"
)
LEDGER_MISSING_INCOMPLETE_RE = re.compile(
    r"^INCOMPLETE ledger=scripts/ci/manifest-pin-ledger\.md: "
    r"scripts/ci/manifest-pin-ledger\.md is absent from commit "
    r"[0-9a-f]{40}; ledger must be present before pin verification can pass$"
)


class Refused(Exception):
    """A safety or authorization check failed."""


class CannotComplete(Exception):
    """Required Git data or input could not be read."""


@dataclass
class Pin:
    manifest: str
    field: str
    path: str
    declared: str
    algorithm: str
    node: yaml.ScalarNode

    @property
    def identity(self) -> tuple[str, str, str]:
        return (self.field, self.path, self.declared)


@dataclass
class AuthorizedPin:
    pin: Pin
    actual: str


class Git:
    def __init__(self, root: Path):
        self.root = root

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
            raise CannotComplete(f"cannot execute git: {exc}") from exc

        if result.returncode != 0:
            message = result.stderr.decode("utf-8", "replace").strip()
            raise CannotComplete(
                message or f"git {' '.join(args)} failed ({result.returncode})"
            )
        return result.stdout

    def resolve_commit(self, ref: str) -> str:
        raw = self.run("rev-parse", "--verify", f"{ref}^{{commit}}")
        commit = raw.decode("ascii", "strict").strip()
        if not HEX40.fullmatch(commit):
            raise CannotComplete(
                f"ref did not resolve to a full commit SHA: {ref}"
            )
        return commit

    def first_parent(self, commit: str) -> str | None:
        raw = self.run("rev-list", "--parents", "-n", "1", commit)
        parts = raw.decode("ascii", "strict").strip().split()
        if len(parts) < 2:
            return None
        parent = parts[1]
        if not HEX40.fullmatch(parent):
            raise CannotComplete(
                f"invalid first parent for commit {commit}: {parent!r}"
            )
        return parent

    def tree_paths(self, commit: str) -> list[str]:
        raw = self.run("ls-tree", "-r", "--name-only", "-z", commit)
        return [
            item.decode("utf-8", "strict")
            for item in raw.split(b"\0")
            if item
        ]

    def blob(self, commit: str, path: str) -> bytes:
        spec = f"{commit}:{path}"
        try:
            result = subprocess.run(
                ["git", "cat-file", "blob", spec],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise CannotComplete(
                f"cannot read Git blob {spec}: {exc}"
            ) from exc

        if result.returncode != 0:
            message = result.stderr.decode("utf-8", "replace").strip()
            raise CannotComplete(
                f"cannot read Git blob {spec}: {message}"
            )
        return result.stdout


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def scalar_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def node_mapping_value(node: Any, key: str) -> Any:
    if not isinstance(node, yaml.MappingNode):
        return None
    for key_node, value_node in node.value:
        if (
            isinstance(key_node, yaml.ScalarNode)
            and key_node.value == key
        ):
            return value_node
    return None


def node_sequence_item(node: Any, index: int) -> Any:
    if not isinstance(node, yaml.SequenceNode):
        return None
    if index < 0 or index >= len(node.value):
        return None
    return node.value[index]


def iter_pairs(
    manifest: str,
    data: dict[str, Any],
    root_node: yaml.Node,
) -> list[Pin]:
    """Return supported path/digest pairs with their original YAML nodes."""
    found: list[Pin] = []

    def add(
        mapping_data: Any,
        mapping_node: Any,
        path_key: str,
        digest_key: str,
        field: str,
        algorithm: str = "git",
    ) -> None:
        if (
            not isinstance(mapping_data, dict)
            or digest_key not in mapping_data
        ):
            return

        path_value = mapping_data.get(path_key)
        if not isinstance(path_value, str):
            return

        digest_node = node_mapping_value(mapping_node, digest_key)
        if not isinstance(digest_node, yaml.ScalarNode):
            return

        found.append(
            Pin(
                manifest=manifest,
                field=field,
                path=path_value,
                declared=scalar_text(mapping_data.get(digest_key)),
                algorithm=algorithm,
                node=digest_node,
            )
        )

    for path_key, digest_key in (
        ("root", "root_blob"),
        ("en_mirror", "en_mirror_blob"),
        ("zh_cn_mirror", "zh_cn_mirror_blob"),
    ):
        add(data, root_node, path_key, digest_key, f"index.{path_key}")

    gate_data = data.get("gate_a_reconstruction", []) or []
    gate_node = node_mapping_value(root_node, "gate_a_reconstruction")
    if isinstance(gate_data, list):
        for index, item in enumerate(gate_data):
            item_node = node_sequence_item(gate_node, index)
            if isinstance(item, dict):
                add(
                    item,
                    item_node,
                    "root",
                    "reconstructed_root_blob",
                    f"gate_a_reconstruction[{index}].root",
                )

    source_data = data.get("baseline_and_source_evidence")
    if not isinstance(source_data, dict):
        source_data = {}

    source_node = node_mapping_value(
        root_node, "baseline_and_source_evidence"
    )
    authored_data = source_data.get(
        "authored_indexes", data.get("authored_indexes", [])
    )
    authored_node = node_mapping_value(source_node, "authored_indexes")
    if authored_node is None:
        authored_node = node_mapping_value(root_node, "authored_indexes")

    if isinstance(authored_data, list):
        for index, item in enumerate(authored_data):
            item_node = node_sequence_item(authored_node, index)
            if not isinstance(item, dict):
                continue
            for path_key, digest_key in (
                ("root", "root_blob"),
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                add(
                    item,
                    item_node,
                    path_key,
                    digest_key,
                    f"authored_indexes[{index}].{path_key}",
                )

    related_data = data.get("related_evidence", []) or []
    related_node = node_mapping_value(root_node, "related_evidence")
    if isinstance(related_data, list):
        for index, item in enumerate(related_data):
            item_node = node_sequence_item(related_node, index)
            if not isinstance(item, dict):
                continue
            for path_key, digest_key in (
                ("path", "blob"),
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                add(
                    item,
                    item_node,
                    path_key,
                    digest_key,
                    f"related_evidence[{index}].{path_key}",
                )

    add(data, root_node, "evidence_file", "evidence_blob", "evidence_file")

    prompt_data = data.get("prompt")
    prompt_node = node_mapping_value(root_node, "prompt")
    if isinstance(prompt_data, dict):
        if "prompt_sha256" in prompt_data:
            add(
                prompt_data,
                prompt_node,
                "prompt_file",
                "prompt_sha256",
                "prompt.prompt_file",
                "sha256",
            )
        if "prompt_bytes" in prompt_data:
            add(
                prompt_data,
                prompt_node,
                "prompt_file",
                "prompt_bytes",
                "prompt.prompt_file",
                "bytes",
            )

    sessions = data.get("session_evidence", []) or []
    sessions_node = node_mapping_value(root_node, "session_evidence")
    if isinstance(sessions, list):
        for index, item in enumerate(sessions):
            item_node = node_sequence_item(sessions_node, index)
            if not isinstance(item, dict):
                continue

            path_key = "executed_prompt_snapshot_file"
            if "executed_prompt_sha256" in item:
                add(
                    item,
                    item_node,
                    path_key,
                    "executed_prompt_sha256",
                    f"session_evidence[{index}].{path_key}",
                    "sha256",
                )
            if "executed_prompt_bytes" in item:
                add(
                    item,
                    item_node,
                    path_key,
                    "executed_prompt_bytes",
                    f"session_evidence[{index}].{path_key}",
                    "bytes",
                )

    return found


def load_baseline(
    git: Git,
    commit: str,
    baseline_path: str,
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[str],
]:
    try:
        raw = git.blob(commit, baseline_path)
    except CannotComplete as exc:
        raise CannotComplete(
            f"baseline unavailable at {commit}:{baseline_path}: {exc}"
        ) from exc

    try:
        content = raw.decode("utf-8")
    except UnicodeError as exc:
        raise CannotComplete(
            f"baseline is not UTF-8: {baseline_path}"
        ) from exc

    mismatch_rows: list[dict[str, str]] = []
    missing_rows: list[dict[str, str]] = []
    other_rows: list[str] = []

    for original in content.splitlines():
        line = original.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("MISMATCH "):
            match = MISMATCH_RE.fullmatch(line)
            if match is None:
                other_rows.append(f"unparseable baseline row: {line}")
            else:
                mismatch_rows.append(match.groupdict())
        elif line.startswith("PATH_MISSING "):
            match = MISSING_RE.fullmatch(line)
            if match is None:
                other_rows.append(f"unparseable baseline row: {line}")
            else:
                missing_rows.append(match.groupdict())
        else:
            other_rows.append(f"unexpected baseline row: {line}")

    return mismatch_rows, missing_rows, other_rows


def run_checker(root: Path, commit: str) -> tuple[list[str], int]:
    checker_path = root / CHECKER_DEFAULT
    if not checker_path.is_file():
        raise CannotComplete(f"checker file not found: {checker_path}")

    spec = importlib.util.spec_from_file_location(
        "_manifest_blob_pin_checker_for_repin",
        checker_path,
    )
    if spec is None or spec.loader is None:
        raise CannotComplete(f"cannot load checker module: {checker_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(spec.name, None)
        raise CannotComplete(
            f"cannot import checker module: {exc}"
        ) from exc

    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            status = module.verify(root, commit, verbose=True)
    except Exception as exc:
        raise CannotComplete(
            f"checker failed while verifying {commit}: {exc}"
        ) from exc

    return output.getvalue().splitlines(), status


def validate_baseline_shape(
    baseline_mismatches: list[dict[str, str]],
    baseline_missing: list[dict[str, str]],
    baseline_other: list[str],
) -> None:
    if baseline_other:
        for row in baseline_other:
            print(f"REFUSED baseline: {row}", file=sys.stderr)
        raise Refused("baseline contains malformed or unexpected rows")

    if not baseline_mismatches:
        raise Refused("baseline contains no MISMATCH rows to authorize")

    mismatch_identities: list[tuple[str, str]] = []
    for row in baseline_mismatches:
        field = row["field"]
        path = row["path"]
        declared = row["declared"]
        actual = row["actual"]

        # This migration authorizes only executed-prompt byte-count changes.
        # Other mismatch families require a separately scoped authorization.
        if not SESSION_BYTES_FIELD_RE.fullmatch(field):
            raise Refused(
                f"unexpected MISMATCH field type: {field!r}"
            )

        if not path.startswith(MANIFEST_ROOT + "/"):
            raise Refused(f"MISMATCH path is outside manifest work items: {path!r}")
        if path.startswith("/") or ".." in Path(path).parts:
            raise Refused(f"unsafe MISMATCH path: {path!r}")
        if not path.endswith("/prompt-v1.md"):
            raise Refused(
                f"unexpected executed-prompt source path: {path!r}"
            )

        if not declared.isdigit() or not actual.isdigit():
            raise Refused(
                f"executed_prompt_bytes must use decimal values: "
                f"{declared!r} -> {actual!r}"
            )
        if declared == actual:
            raise Refused(
                f"MISMATCH row declares identical values: {path}: {declared}"
            )

        mismatch_identities.append((field, path))

    if len(set(mismatch_identities)) != len(mismatch_identities):
        raise Refused("baseline contains duplicate MISMATCH identities")

    sentinel_rows = Counter(
        (row["path"], row["declared"])
        for row in baseline_missing
    )
    if len(baseline_missing) != EXPECTED_SENTINELS:
        raise Refused(
            f"expected exactly {EXPECTED_SENTINELS} PATH_MISSING sentinel "
            f"rows, found {len(baseline_missing)}"
        )
    if sentinel_rows != EXPECTED_SENTINEL_ROWS:
        raise Refused(
            "PATH_MISSING rows do not equal the two exact AID-2026-261 sentinels"
        )


def validate_baseline_and_checker(
    baseline_mismatches: list[dict[str, str]],
    baseline_missing: list[dict[str, str]],
    baseline_other: list[str],
    checker_lines: list[str],
    checker_status: int,
) -> None:
    validate_baseline_shape(
        baseline_mismatches,
        baseline_missing,
        baseline_other,
    )

    live_mismatches = [
        line for line in checker_lines
        if line.startswith("MISMATCH ")
    ]
    live_missing = [
        line for line in checker_lines
        if line.startswith("PATH_MISSING ")
    ]
    live_incomplete = [
        line for line in checker_lines
        if line.startswith("INCOMPLETE ")
    ]

    baseline_mismatch_lines = [
        (
            "MISMATCH "
            + row["field"]
            + " path="
            + row["path"]
            + " declared="
            + row["declared"]
            + " actual="
            + row["actual"]
        )
        for row in baseline_mismatches
    ]
    baseline_missing_lines = [
        f"PATH_MISSING path={row['path']}; declared={row['declared']}"
        for row in baseline_missing
    ]

    if Counter(live_mismatches) != Counter(baseline_mismatch_lines):
        live_set = Counter(live_mismatches)
        baseline_set = Counter(baseline_mismatch_lines)

        for line, count in (live_set - baseline_set).items():
            print(
                f"REFUSED unauthorized live mismatch: {line} (count={count})",
                file=sys.stderr,
            )
        for line, count in (baseline_set - live_set).items():
            print(
                f"REFUSED baseline mismatch not present in commit: "
                f"{line} (count={count})",
                file=sys.stderr,
            )
        raise Refused(
            "live MISMATCH set does not exactly match baseline"
        )

    if Counter(live_missing) != Counter(baseline_missing_lines):
        for line in live_missing:
            if line not in baseline_missing_lines:
                print(
                    f"REFUSED unauthorized PATH_MISSING: {line}",
                    file=sys.stderr,
                )
        raise Refused(
            "live PATH_MISSING set does not exactly match the two baseline sentinels"
        )

    ledger_missing = [
        line for line in live_incomplete
        if LEDGER_MISSING_INCOMPLETE_RE.fullmatch(line)
    ]
    other_incomplete = [
        line for line in live_incomplete
        if not LEDGER_MISSING_INCOMPLETE_RE.fullmatch(line)
    ]

    if other_incomplete:
        for line in other_incomplete:
            print(f"REFUSED {line}", file=sys.stderr)
        raise Refused(
            "checker reported INCOMPLETE entries other than the absent migration ledger"
        )

    if len(ledger_missing) > 1:
        raise Refused(
            "checker reported the absent migration ledger more than once"
        )

    if ledger_missing and checker_status != 2:
        raise Refused(
            "checker reported the absent migration ledger with an unexpected status"
        )

    if checker_status == 2 and not ledger_missing:
        raise Refused(
            "checker reported INCOMPLETE status without the permitted missing-ledger entry"
        )

    if checker_status not in (1, 2):
        raise Refused(
            "expected checker status 1 or the permitted missing-ledger "
            f"status 2 before repin, got {checker_status}"
        )


def algorithm_for_declaration(declared: str) -> str:
    if declared.isdigit():
        return "bytes"
    if HEX64.fullmatch(declared):
        return "sha256"
    if HEX40.fullmatch(declared):
        return "git"
    raise Refused(
        f"unsupported pin declaration format: {declared!r}"
    )


def compute_actual(
    git: Git,
    commit: str,
    path: str,
    algorithm: str,
) -> str:
    try:
        data = git.blob(commit, path)
    except CannotComplete as exc:
        raise Refused(
            f"path={path}: cannot read source bytes: {exc}"
        ) from exc

    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    if algorithm == "bytes":
        return str(len(data))
    if algorithm == "git":
        return git_blob_sha1(data)
    raise Refused(
        f"path={path}: unsupported algorithm {algorithm}"
    )


def locate_authorized_pins(
    git: Git,
    commit: str,
    baseline_mismatches: list[dict[str, str]],
) -> list[AuthorizedPin]:
    manifest_paths = [
        path for path in git.tree_paths(commit)
        if (
            path.startswith(MANIFEST_ROOT + "/")
            and path.endswith("/manifest.yaml")
        )
    ]
    if not manifest_paths:
        raise CannotComplete(
            f"no manifests found in commit {commit}"
        )

    candidates: list[Pin] = []
    for manifest_path in manifest_paths:
        raw = git.blob(commit, manifest_path)
        try:
            text = raw.decode("utf-8")
            data = yaml.safe_load(text)
            root_node = yaml.compose(text)
        except (UnicodeError, yaml.YAMLError) as exc:
            raise Refused(
                f"manifest={manifest_path}: YAML cannot be parsed: {exc}"
            ) from exc

        if (
            not isinstance(data, dict)
            or not isinstance(root_node, yaml.MappingNode)
        ):
            continue

        candidates.extend(
            iter_pairs(manifest_path, data, root_node)
        )

    authorized: list[AuthorizedPin] = []
    for row in baseline_mismatches:
        field = row["field"]
        path = row["path"]
        declared = row["declared"]
        expected_actual = row["actual"]

        matches = [
            candidate for candidate in candidates
            if candidate.identity == (field, path, declared)
        ]
        if len(matches) != 1:
            reason = (
                "no matching manifest pin"
                if not matches
                else "ambiguous manifest pin"
            )
            print(
                f"REFUSED field={field} path={path} "
                f"declared={declared} reason={reason} "
                f"matches={len(matches)}",
                file=sys.stderr,
            )
            raise Refused(
                f"expected exactly one owner for "
                f"({field}, {path}, {declared}); found {len(matches)}"
            )

        pin = matches[0]
        algorithm = algorithm_for_declaration(declared)
        if algorithm != "bytes":
            raise Refused(
                f"unexpected pin algorithm for this migration: {algorithm}"
            )

        actual = compute_actual(
            git,
            commit,
            path,
            algorithm,
        )
        if actual != expected_actual:
            raise Refused(
                f"baseline actual value differs from committed source bytes "
                f"for {path}: baseline={expected_actual} computed={actual}"
            )

        authorized.append(
            AuthorizedPin(
                pin=Pin(
                    manifest=pin.manifest,
                    field=pin.field,
                    path=pin.path,
                    declared=pin.declared,
                    algorithm=algorithm,
                    node=pin.node,
                ),
                actual=actual,
            )
        )

    if len(authorized) != len(baseline_mismatches):
        raise Refused(
            "authorized pin count differs from the parsed baseline MISMATCH count"
        )

    identities = [
        (item.pin.manifest, item.pin.field, item.pin.path)
        for item in authorized
    ]
    if len(set(identities)) != len(identities):
        raise Refused(
            "authorized manifest pin identities are not unique"
        )

    return authorized


def quote_scalar(value: str, style: str | None) -> str:
    if style == "'":
        return "'" + value.replace("'", "''") + "'"
    if style == '"':
        return json.dumps(value, ensure_ascii=False)
    return value


def char_offset_to_byte(text: str, char_offset: int) -> int:
    return len(text[:char_offset].encode("utf-8"))


def pin_values_for_manifest(
    raw: bytes,
    manifest: str,
) -> Counter:
    try:
        text = raw.decode("utf-8")
        data = yaml.safe_load(text)
        node = yaml.compose(text)
    except (UnicodeError, yaml.YAMLError) as exc:
        raise Refused(
            f"manifest={manifest}: post-write YAML parse failed: {exc}"
        ) from exc

    if (
        not isinstance(data, dict)
        or not isinstance(node, yaml.MappingNode)
    ):
        raise Refused(
            f"manifest={manifest}: YAML root is not a mapping"
        )

    return Counter(
        (pin.field, pin.path, pin.declared)
        for pin in iter_pairs(manifest, data, node)
    )


def prepare_modified_files(
    git: Git,
    commit: str,
    authorized: list[AuthorizedPin],
) -> tuple[
    dict[str, bytes],
    dict[str, bytes],
    dict[str, Counter],
]:
    by_manifest: dict[str, list[AuthorizedPin]] = {}
    for item in authorized:
        by_manifest.setdefault(item.pin.manifest, []).append(item)

    originals: dict[str, bytes] = {}
    modified: dict[str, bytes] = {}
    before_pin_values: dict[str, Counter] = {}

    for manifest, pins in by_manifest.items():
        committed = git.blob(commit, manifest)
        worktree_path = git.root / manifest
        try:
            worktree = worktree_path.read_bytes()
        except OSError as exc:
            raise Refused(
                f"manifest={manifest}: cannot read worktree file: {exc}"
            ) from exc

        if worktree != committed:
            raise Refused(
                f"manifest={manifest}: worktree bytes differ from "
                "--commit tree; refusing to overwrite local changes"
            )

        try:
            text = committed.decode("utf-8")
            data = yaml.safe_load(text)
            root_node = yaml.compose(text)
        except (UnicodeError, yaml.YAMLError) as exc:
            raise Refused(
                f"manifest={manifest}: cannot parse committed YAML: {exc}"
            ) from exc

        if (
            not isinstance(data, dict)
            or not isinstance(root_node, yaml.MappingNode)
        ):
            raise Refused(
                f"manifest={manifest}: committed YAML root is not a mapping"
            )

        originals[manifest] = committed
        before_pin_values[manifest] = pin_values_for_manifest(
            committed,
            manifest,
        )

        edits: list[tuple[int, int, bytes]] = []
        for item in pins:
            node = item.pin.node
            if not isinstance(node, yaml.ScalarNode):
                raise Refused(
                    f"manifest={manifest} field={item.pin.field} "
                    f"path={item.pin.path}: target pin is not a scalar"
                )

            replacement = quote_scalar(
                item.actual,
                node.style,
            ).encode("utf-8")
            start = char_offset_to_byte(
                text,
                node.start_mark.index,
            )
            end = char_offset_to_byte(
                text,
                node.end_mark.index,
            )
            edits.append((start, end, replacement))

        edits.sort(key=lambda entry: entry[0], reverse=True)
        result = committed
        previous_start = len(committed) + 1

        for start, end, replacement in edits:
            if end > previous_start or start > end:
                raise Refused(
                    f"manifest={manifest}: overlapping or invalid scalar edits"
                )
            result = result[:start] + replacement + result[end:]
            previous_start = start

        modified[manifest] = result

    return originals, modified, before_pin_values


def verify_modified_files(
    modified: dict[str, bytes],
    before_pin_values: dict[str, Counter],
    authorized: list[AuthorizedPin],
) -> None:
    expected_changes: dict[str, Counter] = {}

    for item in authorized:
        manifest = item.pin.manifest
        delta = expected_changes.setdefault(manifest, Counter())
        delta[(item.pin.field, item.pin.path, item.pin.declared)] -= 1
        delta[(item.pin.field, item.pin.path, item.actual)] += 1

    for manifest, raw in modified.items():
        after = pin_values_for_manifest(raw, manifest)
        before = before_pin_values[manifest]

        actual_delta = after - before
        reverse_delta = before - after
        signed_actual = actual_delta.copy()
        for key, count in reverse_delta.items():
            signed_actual[key] -= count

        expected = expected_changes.get(manifest, Counter())
        if (
            +signed_actual != +expected
            or +expected != +signed_actual
        ):
            raise Refused(
                f"manifest={manifest}: post-write pin inventory differs "
                "from the exact baseline-authorized change set"
            )

    for item in authorized:
        after = pin_values_for_manifest(
            modified[item.pin.manifest],
            item.pin.manifest,
        )
        target = (
            item.pin.field,
            item.pin.path,
            item.actual,
        )
        if target not in after:
            raise Refused(
                f"manifest={item.pin.manifest} field={item.pin.field} "
                f"path={item.pin.path}: new value {item.actual} "
                "not found after rewrite"
            )


def emit_ledger(
    authorized: list[AuthorizedPin],
    repin_commit: str,
) -> None:
    for item in sorted(
        authorized,
        key=lambda entry: (
            entry.pin.manifest,
            entry.pin.field,
            entry.pin.path,
        ),
    ):
        print(
            f"|{item.pin.manifest}|{item.pin.field}|{item.pin.path}|"
            f"{item.pin.declared}|{item.actual}|{repin_commit}|"
        )


def parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--baseline",
        default=BASELINE_DEFAULT,
        help=f"baseline path in the selected Git commit (default: {BASELINE_DEFAULT})",
    )
    parser.add_argument(
        "--commit",
        default="HEAD",
        help="commit whose tree supplies manifests and source bytes (default: HEAD)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the baseline-authorized scalar replacements to the worktree",
    )
    parser.add_argument(
        "--emit-ledger",
        action="store_true",
        help="print the Markdown ledger rows; does not write files",
    )
    parser.add_argument(
        "--repin-commit",
        help="full 40-character SHA recorded in emitted ledger rows",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    if args.emit_ledger:
        if args.apply:
            print(
                "REFUSED: --emit-ledger and --apply cannot be combined",
                file=sys.stderr,
            )
            return 3
        if (
            not args.repin_commit
            or not HEX40.fullmatch(args.repin_commit)
        ):
            print(
                "REFUSED: --emit-ledger requires --repin-commit "
                "with a full 40-hex SHA",
                file=sys.stderr,
            )
            return 3
    elif args.repin_commit:
        print(
            "REFUSED: --repin-commit is only valid with --emit-ledger",
            file=sys.stderr,
        )
        return 3

    try:
        git = Git(root)
        commit = git.resolve_commit(args.commit)

        if args.emit_ledger:
            repin_commit = git.resolve_commit(args.repin_commit)
            if repin_commit != args.repin_commit:
                raise Refused(
                    "--repin-commit must be the exact full lowercase commit SHA"
                )
            repin_parent = git.first_parent(repin_commit)
            if repin_parent != commit:
                raise Refused(
                    "--repin-commit must be a direct child of --commit: "
                    f"parent={repin_parent} source={commit}"
                )

        baseline_mismatches, baseline_missing, baseline_other = load_baseline(
            git,
            commit,
            args.baseline,
        )

        checker_lines, checker_status = run_checker(root, commit)
        validate_baseline_and_checker(
            baseline_mismatches,
            baseline_missing,
            baseline_other,
            checker_lines,
            checker_status,
        )

        authorized = locate_authorized_pins(
            git,
            commit,
            baseline_mismatches,
        )

        manifest_counts = Counter(
            item.pin.manifest for item in authorized
        )
        if not manifest_counts:
            raise Refused("no manifest files are authorized for repinning")

        if args.emit_ledger:
            emit_ledger(authorized, args.repin_commit)
            return 0

        originals, modified, before_pin_values = prepare_modified_files(
            git,
            commit,
            authorized,
        )
        verify_modified_files(
            modified,
            before_pin_values,
            authorized,
        )

        if args.apply:
            written: list[str] = []
            try:
                for manifest in sorted(modified):
                    path = root / manifest
                    path.write_bytes(modified[manifest])
                    written.append(manifest)

                for manifest in sorted(modified):
                    on_disk = (root / manifest).read_bytes()
                    if on_disk != modified[manifest]:
                        raise Refused(
                            f"manifest={manifest}: on-disk bytes differ after write"
                        )

                verify_modified_files(
                    {
                        name: (root / name).read_bytes()
                        for name in modified
                    },
                    before_pin_values,
                    authorized,
                )
            except Exception as exc:
                if written:
                    print(
                        "WRITE_SELF_CHECK_FAILED; files written and requiring "
                        "manual rollback:",
                        file=sys.stderr,
                    )
                    for manifest in written:
                        print(f"written={manifest}", file=sys.stderr)

                if isinstance(exc, Refused):
                    raise
                raise Refused(
                    f"write or post-write self-check failed: {exc}"
                ) from exc

        print(f"baseline_commit={commit}")
        print(f"mode={'APPLY' if args.apply else 'DRY_RUN'}")
        print(f"authorized_pins={len(authorized)}")
        print(f"touched_manifests={len(manifest_counts)}")
        print(f"touched_pins={len(authorized)}")
        print("refused=0")
        print(f"sentinels_preserved={len(baseline_missing)}")

        for manifest in sorted(manifest_counts):
            print(
                f"manifest_pins={manifest_counts[manifest]}:{manifest}"
            )

        return 0

    except Refused as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 3
    except (
        CannotComplete,
        OSError,
        UnicodeError,
        subprocess.SubprocessError,
    ) as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
