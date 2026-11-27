#!/usr/bin/env python3
"""Ratchet Git blob pins declared in work-item manifest YAML files."""

from __future__ import annotations

import argparse
import collections
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
MANIFEST_GLOB = "14-ai-development/work-items/**/manifest.yaml"
SENTINEL = re.compile(
    r"^\s*(?:NOT_SEPARATELY_COMMITTED|NOT_VERIFIED|NOT_AVAILABLE|N/A)"
    r"(?:\b|(?=\s|[(:;,.-]))",
    re.IGNORECASE,
)

# A key is a Git blob pin only when it is explicitly registered here.
# The value is the ordered list of path sibling keys accepted for that pin.
PATH_KEYS = {
    "prompt_file_blob_sha": ("prompt_file",),
    "snapshot_git_blob_sha": ("snapshot_file",),
    "git_blob_sha": ("file",),
    "source_blob_sha": ("source_path", "path"),
    "translation_blob_sha": ("translation_path",),
    "blob_sha": ("path", "test_matrix_path"),
    "sha256_or_blob_sha": ("path",),
    "evidence_blob": ("evidence_file",),
    "root_blob": ("root",),
    "en_mirror_blob": ("en_mirror",),
    "zh_cn_mirror_blob": ("zh_cn_mirror",),
    "blob": ("path",),
    "current_blob": ("current_artifact",),
    "superseded_blob": ("superseded_artifact",),
    "sha": ("path",),
    "restored_blob_sha": ("restored_path", "path", "file"),
}

# These values are not full-file Git blob identities.
EXCLUDED_BLOB_KEYS = {
    "frontmatter_blob_sha",
    "reverified_source_blob_sha",
    "reverified_translation_blob_sha",
}

COMMIT_KEYS_BY_FIELD = {
    "prompt_file_blob_sha": ("prompt_file_commit_sha",),
    "source_blob_sha": ("head_sha", "source_commit_sha"),
    "translation_blob_sha": ("translation_commit_sha",),
    "blob_sha": (
        "commit_before_manifest_update",
        "test_matrix_commit_before_manifest_update",
    ),
    # source.files[].blob is pinned against the enclosing source.head.
    "blob": ("head",),
    # restored_blob_sha intentionally has no commit key: it uses HEAD.
}


@dataclass
class Entry:
    key: str
    value: str
    line: int
    mapping: dict[str, object]
    ancestors: tuple[dict[str, object], ...]
    manifest: str


@dataclass
class Finding:
    manifest: str
    line: int
    kind: str
    path: str
    field: str
    declared: str
    actual: str
    base: str

    def item(self) -> str:
        return (
            f"{self.manifest}:{self.line} {self.kind} "
            f"path={self.path} field={self.field} "
            f"declared={self.declared} actual={self.actual} base={self.base}"
        )


def run_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "git command failed")
    return proc.stdout.strip()


def scalar(node: object) -> object:
    if isinstance(node, ScalarNode):
        return node.value
    return None


def node_to_value(node: object) -> object:
    """Convert YAML nodes to plain Python values without losing mapping context."""
    if isinstance(node, ScalarNode):
        if node.tag.endswith(":null"):
            return None
        if node.tag.endswith(":bool"):
            return node.value.lower() == "true"
        if node.tag.endswith(":int"):
            try:
                return int(node.value, 0)
            except ValueError:
                return node.value
        return node.value
    if isinstance(node, SequenceNode):
        return [node_to_value(child) for child in node.value]
    if isinstance(node, MappingNode):
        result = {}
        for key_node, value_node in node.value:
            key = scalar(key_node)
            if isinstance(key, str):
                result[key] = node_to_value(value_node)
        return result
    return None


def walk(
    node: object,
    manifest: str,
    ancestors: tuple[dict[str, object], ...] = (),
) -> Iterable[Entry]:
    if not isinstance(node, MappingNode):
        if isinstance(node, SequenceNode):
            for child in node.value:
                yield from walk(child, manifest, ancestors)
        return

    mapping: dict[str, object] = {}
    value_nodes: dict[str, object] = {}
    for key_node, value_node in node.value:
        key = scalar(key_node)
        if isinstance(key, str):
            mapping[key] = node_to_value(value_node)
            value_nodes[key] = value_node

    for key, value_node in value_nodes.items():
        value = scalar(value_node)
        if isinstance(value, str) and HEX40.fullmatch(value):
            yield Entry(
                key=key,
                value=value.lower(),
                line=value_node.start_mark.line + 1,
                mapping=mapping,
                ancestors=ancestors,
                manifest=manifest,
            )

    next_ancestors = ancestors + (mapping,)
    for value_node in value_nodes.values():
        yield from walk(value_node, manifest, next_ancestors)


def is_candidate(entry: Entry) -> bool:
    """Candidate nodes are blob-named fields plus explicitly registered keys."""
    return "blob" in entry.key.lower() or entry.key in PATH_KEYS


def find_path(entry: Entry) -> tuple[str | None, str | None]:
    candidates = PATH_KEYS.get(entry.key)
    if candidates is None:
        return None, None

    found = [
        (key, entry.mapping.get(key))
        for key in candidates
        if isinstance(entry.mapping.get(key), str)
        and str(entry.mapping.get(key)).strip()
    ]
    if len(found) != 1:
        return None, None
    key, value = found[0]
    return str(value).strip(), key


def nearest_value(entry: Entry, keys: tuple[str, ...]) -> str | None:
    # Same mapping takes precedence, then walk outward from the nearest ancestor.
    for key in keys:
        value = entry.mapping.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    for ancestor in reversed(entry.ancestors):
        for key in keys:
            value = ancestor.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def declared_base(entry: Entry) -> str | None:
    keys = COMMIT_KEYS_BY_FIELD.get(entry.key, ())
    return nearest_value(entry, keys) if keys else None


def is_sentinel_base(entry: Entry) -> bool:
    declared = declared_base(entry)
    return declared is not None and SENTINEL.match(declared) is not None


def is_historical_read(entry: Entry) -> bool:
    """A *_read evidence item with an observation records a past inspection."""
    kind = entry.mapping.get("kind")
    observation = entry.mapping.get("observation")
    return (
        isinstance(kind, str)
        and kind.lower().endswith("_read")
        and isinstance(observation, str)
        and bool(observation.strip())
    )


def current_main_snapshot_matches(
    repo: Path, head: str, entry: Entry, path: str
) -> bool:
    """Recognize historical pins superseded by latest_reconciliation data."""
    manifest_path = repo / entry.manifest
    try:
        document = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return False

    if not isinstance(document, dict):
        return False

    # Deliberately limit the search to the latest_reconciliation section.
    # Do not treat an unrelated current_main_blobs key elsewhere in the
    # manifest as evidence that this pin is historical.
    reconciliation = document.get("latest_reconciliation")
    if not isinstance(reconciliation, dict):
        return False

    basename_key = PurePosixPath(path).name.replace(".", "_")

    # Permit current_main_blobs mappings nested inside latest_reconciliation,
    # but collect every occurrence so conflicting duplicate declarations
    # cannot accidentally authorize historical classification.
    current_maps: list[dict[str, object]] = []

    def collect(value: object) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "current_main_blobs" and isinstance(child, dict):
                    current_maps.append(child)
                else:
                    collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(reconciliation)

    if not current_maps:
        return False

    declared_values = [
        mapping[basename_key]
        for mapping in current_maps
        if isinstance(mapping.get(basename_key), str)
        and HEX40.fullmatch(mapping[basename_key])
    ]

    # Require at least one matching declaration, and require every matching
    # declaration to agree. Conflicting duplicate sections are not evidence.
    if not declared_values or len(set(v.lower() for v in declared_values)) != 1:
        return False

    current_oid = declared_values[0].lower()

    try:
        head_oid = run_git(repo, "rev-parse", "--verify", f"{head}:{path}")
    except RuntimeError:
        return False

    return head_oid.lower() == current_oid


def is_historical_snapshot(
    repo: Path, head: str, entry: Entry, path: str
) -> bool:
    # Structural evidence only: a current_main_blobs value must identify the
    # same file and must itself match that file in the candidate HEAD tree.
    return current_main_snapshot_matches(repo, head, entry, path)


def resolve_base(repo: Path, entry: Entry, head: str) -> tuple[str, str]:
    declared = declared_base(entry)
    if declared is None:
        return head, "HEAD"
    # Resolve only a commit object. A tree/blob/tag is not accepted as a base.
    resolved = run_git(repo, "rev-parse", "--verify", f"{declared}^{{commit}}")
    return resolved, resolved


def normalize_path(raw: str, manifest: str, path_key: str) -> str:
    raw = raw.replace("\\", "/").strip()
    if raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise ValueError("absolute path is not allowed")

    # snapshot_file without a directory component is relative to the manifest.
    if path_key == "snapshot_file" and "/" not in raw:
        candidate = PurePosixPath(manifest).parent / raw
        parts = [part for part in candidate.parts if part not in ("", ".")]
    else:
        parts = [part for part in raw.split("/") if part not in ("", ".")]

    if any(part == ".." for part in parts):
        raise ValueError("path traversal is not allowed")
    return PurePosixPath(*parts).as_posix()


def inspect_pin(repo: Path, head: str, entry: Entry) -> Finding | None:
    raw_path, path_key = find_path(entry)
    if raw_path is None or path_key is None:
        return None

    try:
        path = normalize_path(raw_path, entry.manifest, path_key)
    except ValueError:
        return Finding(
            entry.manifest, entry.line, "INVALID", raw_path, entry.key,
            entry.value, "NONE", "NONE",
        )

    try:
        tree_base, display_base = resolve_base(repo, entry, head)
    except (RuntimeError, ValueError):
        return Finding(
            entry.manifest, entry.line, "INVALID", path, entry.key,
            entry.value, "NONE", "UNRESOLVED",
        )

    try:
        actual = run_git(repo, "rev-parse", "--verify", f"{tree_base}:{path}")
    except RuntimeError:
        return Finding(
            entry.manifest, entry.line, "PATH_MISSING", path, entry.key,
            entry.value, "NONE", display_base,
        )

    try:
        object_type = run_git(repo, "cat-file", "-t", actual)
    except RuntimeError:
        object_type = ""
    if object_type != "blob":
        return Finding(
            entry.manifest, entry.line, "PATH_MISSING", path, entry.key,
            entry.value, "NONE", display_base,
        )

    if actual.lower() != entry.value:
        return Finding(
            entry.manifest, entry.line, "MISMATCH", path, entry.key,
            entry.value, actual.lower(), display_base,
        )
    return None


def load_baseline(path: Path) -> set[str]:
    if not path.exists():
        return set()
    items = set()
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        if item.startswith("NNN. "):
            raise ValueError(
                f"{path}:{number}: baseline item must not contain NNN. prefix"
            )
        items.add(item)
    return items


def write_baseline(path: Path, findings: list[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(f.item() + "\n" for f in findings)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument(
        "--baseline", default="scripts/ci/baselines/blob-pins.txt"
    )
    parser.add_argument("--emit-baseline", metavar="PATH")
    parser.add_argument("--manifest-glob", default=MANIFEST_GLOB)
    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    try:
        head = run_git(repo_root, "rev-parse", "--verify", "HEAD^{commit}")
        manifest_paths = sorted(
            p for p in repo_root.glob(args.manifest_glob) if p.is_file()
        )
        findings: list[Finding] = []
        pin_count = 0
        out_of_scope = collections.Counter()

        for absolute in manifest_paths:
            rel = absolute.relative_to(repo_root).as_posix()
            try:
                root = yaml.compose(absolute.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, yaml.YAMLError) as exc:
                findings.append(Finding(
                    rel, 1, "INVALID", "NONE", "manifest", "YAML",
                    str(exc).replace("\n", " "), "NONE",
                ))
                continue
            if root is None:
                continue

            for entry in walk(root, rel):
                if not is_candidate(entry):
                    continue

                if entry.key in EXCLUDED_BLOB_KEYS:
                    out_of_scope[entry.key] += 1
                    continue

                raw_path, path_key = find_path(entry)
                if raw_path is None or path_key is None:
                    out_of_scope[entry.key] += 1
                    continue

                if is_sentinel_base(entry):
                    out_of_scope[entry.key] += 1
                    continue

                try:
                    normalized = normalize_path(raw_path, rel, path_key)
                except ValueError:
                    # A path-bearing candidate with an invalid path is in
                    # scope and produces an INVALID finding.
                    pin_count += 1
                    finding = inspect_pin(repo_root, head, entry)
                    if finding is not None:
                        findings.append(finding)
                    continue

                if is_historical_read(entry):
                    out_of_scope[entry.key] += 1
                    continue

                if is_historical_snapshot(
                    repo_root, head, entry, normalized
                ):
                    out_of_scope[entry.key] += 1
                    continue

                pin_count += 1
                finding = inspect_pin(repo_root, head, entry)
                if finding is not None:
                    findings.append(finding)

        findings.sort(key=lambda f: (
            f.manifest, f.line, f.field, f.path, f.kind, f.declared
        ))
        items = [finding.item() for finding in findings]

        print(f"MANIFESTS={len(manifest_paths)}")
        print(f"PINS={pin_count}")
        print(f"OUT_OF_SCOPE={sum(out_of_scope.values())}")
        for key in sorted(out_of_scope):
            print(f"OUT_OF_SCOPE_KEY {key}={out_of_scope[key]}")

        counts = collections.Counter(f.kind for f in findings)
        for kind in ("MISMATCH", "PATH_MISSING", "NO_PATH", "INVALID"):
            print(f"{kind}={counts[kind]}")
        bad = sum(counts[k] for k in ("MISMATCH", "PATH_MISSING", "INVALID"))
        print(f"BAD={bad}")

        for number, item in enumerate(items, 1):
            print(f"{number:03d}. {item}")

        if args.emit_baseline:
            write_baseline(Path(args.emit_baseline), findings)
            print(f"BASELINE_WRITTEN={args.emit_baseline}")
            return 0

        baseline_path = Path(args.baseline)
        try:
            known = load_baseline(baseline_path)
        except (OSError, ValueError) as exc:
            print(f"BASELINE_ERROR={exc}", file=sys.stderr)
            return 2

        new_items = [item for item in items if item not in known]
        stale_items = sorted(known - set(items))
        print(f"BASELINE_ITEMS={len(known)}")
        print(f"NEW_FINDINGS={len(new_items)}")
        print(f"STALE_BASELINE_ITEMS={len(stale_items)}")
        for item in new_items:
            print(f"NEW. {item}")
        for item in stale_items:
            print(f"STALE. {item}")

        return 1 if new_items or stale_items else 0

    except (OSError, RuntimeError, yaml.YAMLError) as exc:
        print(f"CHECKER_ERROR={exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
