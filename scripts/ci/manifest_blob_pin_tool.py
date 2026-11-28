#!/usr/bin/env python3
"""Audit and reanchor manifest blob pins against exact Git commit trees."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from scripts.governance.session_evidence import blob_pins as bp


MANIFEST_ROOT = "14-ai-development/work-items"
MANIFEST_SUFFIX = "/manifest.yaml"
_FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class AuditUnavailable(RuntimeError):
    """The requested commit/tree/blob audit could not be completed."""


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    object_type: str
    oid: str
    size: int
    path: str


@dataclass(frozen=True)
class Exclusion:
    pattern: str
    rule_id: str


@dataclass(frozen=True)
class Replacement:
    start: int
    end: int
    old: str
    new: str
    location: str
    path: str
    object_id: str
    byte_size: int


def git(repo: Path, *args: str, check: bool = True) -> bytes:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(repo),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise AuditUnavailable(f"cannot execute git: {exc}") from exc

    if check and completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        raise AuditUnavailable(
            f"git {' '.join(args)} failed ({completed.returncode}): {detail}"
        )
    return completed.stdout


def resolve_commit(repo: Path, ref: str) -> str:
    raw = git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    commit = raw.decode("ascii", "strict").strip().lower()
    if not _FULL_SHA_RE.fullmatch(commit):
        raise AuditUnavailable(
            f"resolved commit is not a complete 40-character SHA-1: {commit!r}"
        )
    return commit


def discover_manifests(repo: Path, commit: str) -> list[str]:
    # NUL termination preserves unusual Git path names, including newlines.
    raw = git(
        repo,
        "ls-tree",
        "-r",
        "--name-only",
        "-z",
        commit,
        "--",
        MANIFEST_ROOT,
    )
    paths = [
        item.decode("utf-8", "strict")
        for item in raw.split(b"\0")
        if item
    ]
    return sorted(
        path for path in paths
        if path.startswith(MANIFEST_ROOT + "/")
        and path.endswith(MANIFEST_SUFFIX)
    )


def read_tree(repo: Path, commit: str) -> dict[str, TreeEntry]:
    raw = git(repo, "ls-tree", "-r", "-l", "-z", commit)
    result: dict[str, TreeEntry] = {}

    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, path_bytes = record.split(b"\t", 1)
            mode, object_type, oid, size_text = (
                metadata.decode("ascii").split(" ", 3)
            )
            path = path_bytes.decode("utf-8", "strict")
            size = int(size_text)
        except (ValueError, UnicodeDecodeError) as exc:
            raise AuditUnavailable(
                f"cannot parse ls-tree record {record!r}: {exc}"
            ) from exc

        result[path] = TreeEntry(mode, object_type, oid, size, path)

    return result


def tree_index(entries: dict[str, TreeEntry]) -> dict:
    return {
        path: {
            "mode": entry.mode,
            "type": entry.object_type,
            "sha": entry.oid,
            "size": entry.size,
        }
        for path, entry in entries.items()
    }


def read_blob(repo: Path, entry: TreeEntry) -> bytes:
    raw = git(repo, "cat-file", "blob", entry.oid)
    if len(raw) != entry.size:
        raise AuditUnavailable(
            f"blob size mismatch for {entry.path}: "
            f"tree={entry.size}, cat-file={len(raw)}"
        )
    return raw


def decode_manifest(raw: bytes, path: str) -> str:
    try:
        return raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise AuditUnavailable(
            f"{path}: manifest blob is not valid UTF-8: {exc}"
        ) from exc


def parse_exclusion(spec: str) -> Exclusion:
    if "=" not in spec:
        raise ValueError(
            f"contract exclusion must be <path-glob>=<rule-id>: {spec!r}"
        )
    pattern, rule_id = spec.split("=", 1)
    if not pattern.strip() or not rule_id.strip():
        raise ValueError(
            f"contract exclusion requires both path-glob and rule-id: {spec!r}"
        )
    return Exclusion(pattern.strip(), rule_id.strip())


def matching_exclusion(path: str, exclusions: list[Exclusion]):
    for exclusion in exclusions:
        if fnmatch.fnmatchcase(path, exclusion.pattern):
            return exclusion
    return None


def iter_mappings(value, location="$"):
    if isinstance(value, dict):
        yield location, value
        for key, child in value.items():
            child_location = bp._location(location, str(key))
            yield from iter_mappings(child, child_location)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_mappings(child, f"{location}[{index}]")


def count_path_declarations(document) -> int:
    """Count explicit file/path declarations, not embedded source-list paths."""
    explicit_path_keys = {
        path_key for path_key, _algorithm in bp._EXPLICIT_BINDINGS.values()
    }
    count = 0
    for _location, mapping in iter_mappings(document):
        for key, value in mapping.items():
            if (
                key in explicit_path_keys
                or (isinstance(key, str) and key.endswith("_file"))
            ):
                if isinstance(value, str) and value:
                    count += 1
    return count


def load_manifest(repo, commit, manifest_path, entries):
    entry = entries.get(manifest_path)
    if entry is None or entry.object_type != "blob":
        raise AuditUnavailable(
            f"manifest discovered by ls-tree is not a blob: {manifest_path}"
        )
    raw = read_blob(repo, entry)
    return raw, decode_manifest(raw, manifest_path)


def pin_tree_for(repo, pin, candidate_entries, historical_cache):
    if pin.source_commit is None:
        return candidate_entries

    source_commit = pin.source_commit.lower()
    if not _FULL_SHA_RE.fullmatch(source_commit):
        raise bp.BlobPinError(
            f"{pin.location}: historical source commit must be a full SHA-1"
        )

    if source_commit not in historical_cache:
        historical_cache[source_commit] = read_tree(repo, source_commit)
    return historical_cache[source_commit]


def verify_one_pin(
    repo,
    pin,
    candidate_entries,
    historical_cache,
):
    selected = pin_tree_for(
        repo, pin, candidate_entries, historical_cache
    )
    entry = selected.get(pin.path)
    if entry is None:
        raise bp.BlobPinError(
            f"{pin.location}: path {pin.path!r} absent from selected commit tree"
        )
    if entry.object_type != "blob" or entry.mode not in ("100644", "100755"):
        raise bp.BlobPinError(
            f"{pin.location}: {pin.path!r} is not a regular file blob"
        )

    raw = read_blob(repo, entry)
    actual_git_sha = bp._git_blob_sha1(raw)

    if actual_git_sha != entry.oid.lower():
        raise bp.BlobPinError(
            f"{pin.location}: cat-file bytes do not hash to tree object "
            f"{entry.oid}"
        )

    if pin.algorithm == "sha1":
        actual = entry.oid.lower()
    elif pin.algorithm == "sha256":
        actual = hashlib.sha256(raw).hexdigest()
    else:
        raise bp.BlobPinError(
            f"{pin.location}: unsupported algorithm {pin.algorithm!r}"
        )

    if actual != pin.digest.lower():
        raise bp.BlobPinError(
            f"{pin.location}: mismatch for {pin.path}: "
            f"declared={pin.digest}, actual={actual}"
        )

    return entry, raw, actual


def audit(args) -> int:
    repo = Path(args.repo).resolve()
    commit = resolve_commit(repo, args.ref)
    entries = read_tree(repo, commit)
    manifests = discover_manifests(repo, commit)
    exclusions = [parse_exclusion(item) for item in args.contract_exclusion]

    counts = {
        "manifests": len(manifests),
        "parsed": 0,
        "unparsed": 0,
        "pins": 0,
        "path_declarations": 0,
        "mismatches": 0,
        "errors": 0,
        "excluded_by_contract": 0,
    }
    historical_cache = {}

    print(f"commit={commit}")

    for manifest_path in manifests:
        exclusion = matching_exclusion(manifest_path, exclusions)
        if exclusion is not None:
            counts["excluded_by_contract"] += 1
            print(
                f"EXCLUDED rule-id={exclusion.rule_id} "
                f"path={manifest_path}"
            )
            continue

        try:
            _raw, source = load_manifest(
                repo, commit, manifest_path, entries
            )
        except (AuditUnavailable, UnicodeDecodeError) as exc:
            counts["errors"] += 1
            counts["unparsed"] += 1
            print(f"ERROR path={manifest_path} reason={exc}")
            continue

        records, diagnostics = bp._enumerate_pin_records(source)
        yaml_failed = any(
            item.reason == bp.BlobPinErrorReason.YAML_PARSE
            for item in diagnostics
        )
        if yaml_failed:
            counts["unparsed"] += 1
        else:
            counts["parsed"] += 1

        counts["pins"] += len(records)
        counts["errors"] += len(diagnostics)

        try:
            document = bp._parse_yaml_subset(source)
            counts["path_declarations"] += count_path_declarations(document)
        except bp.BlobPinError:
            # The parser diagnostic above already accounts for this file.
            pass

        for diagnostic in diagnostics:
            print(
                f"ERROR path={manifest_path} location={diagnostic.location} "
                f"reason={diagnostic.reason.value} message={diagnostic.message}"
            )

        for record in records:
            try:
                verify_one_pin(
                    repo,
                    record.pin,
                    entries,
                    historical_cache,
                )
            except bp.BlobPinError as exc:
                counts["mismatches"] += 1
                print(
                    f"MISMATCH manifest={manifest_path} "
                    f"location={record.pin.location} "
                    f"pin_path={record.pin.path} reason={exc}"
                )

    if counts["manifests"] != counts["parsed"] + counts["unparsed"]:
        counts["errors"] += 1
        print(
            "ERROR invariant manifests != parsed + unparsed: "
            f"{counts['manifests']} != "
            f"{counts['parsed']} + {counts['unparsed']}"
        )

    print("COUNTS " + " ".join(
        f"{key}={counts[key]}" for key in (
            "manifests",
            "parsed",
            "unparsed",
            "pins",
            "path_declarations",
            "mismatches",
            "errors",
            "excluded_by_contract",
        )
    ))
    return 1 if counts["mismatches"] or counts["errors"] else 0


def _source_scalar_replacement(source, start, end, new_value):
    if start is None or end is None or start < 0 or end <= start:
        raise bp.BlobPinError("token source span is missing or invalid")

    token = source[start:end]
    if not token:
        raise bp.BlobPinError("empty token source span")

    if token[0] in ("'", '"'):
        quote = token[0]
        if len(token) < 2 or token[-1] != quote:
            raise bp.BlobPinError(
                "quoted token boundary is incomplete or crosses its span"
            )
        if quote == '"' and ("\\" in token or "\n" in token or "\r" in token):
            raise bp.BlobPinError(
                "quoted token contains escapes or line crossings; "
                "refusing ambiguous rewrite"
            )
        if quote == "'" and ("''" in token or "\n" in token or "\r" in token):
            raise bp.BlobPinError(
                "single-quoted token contains doubled quotes or line crossings"
            )
        return quote + new_value + quote

    if any(char in token for char in ("'", '"', "\\", "\n", "\r")):
        raise bp.BlobPinError(
            "plain token contains quote/escape boundary; refusing rewrite"
        )
    return new_value


def _collect_bytes_targets(document):
    """Find existing *_bytes scalars paired with their sibling *_file path."""
    targets = []
    for location, mapping in iter_mappings(document):
        for key, value in mapping.items():
            if not isinstance(key, str) or not key.endswith("_bytes"):
                continue
            path_key = key[:-6] + "_file"
            if path_key not in mapping:
                continue
            if not isinstance(value, (int, str)):
                continue
            targets.append(
                (
                    bp._location(location, key),
                    str(mapping[path_key]),
                    value,
                )
            )
    return targets


def _make_replacements(
    repo,
    source,
    records,
    document,
    candidate_entries,
    historical_cache,
):
    replacements = []

    # Reject multiple candidate scalar tokens on the same source line. This
    # is intentionally conservative, even when their individual spans exist.
    line_counts = {}
    for record in records:
        line = record.pin.line
        line_counts[line] = line_counts.get(line, 0) + 1

    for record in records:
        pin = record.pin
        if pin.line is None:
            raise bp.BlobPinError(
                f"{pin.location}: parser did not provide a source line"
            )
        if line_counts.get(pin.line, 0) != 1:
            raise bp.BlobPinError(
                f"{pin.location}: multiple candidate pin scalars on line "
                f"{pin.line}"
            )
        if record.start is None or record.end is None:
            raise bp.BlobPinError(
                f"{pin.location}: parser did not provide an exact token span"
            )

        selected = pin_tree_for(
            repo, pin, candidate_entries, historical_cache
        )
        entry = selected.get(pin.path)
        if entry is None or entry.object_type != "blob":
            raise bp.BlobPinError(
                f"{pin.location}: target path {pin.path!r} is not a blob"
            )
        raw = read_blob(repo, entry)
        if bp._git_blob_sha1(raw) != entry.oid.lower():
            raise bp.BlobPinError(
                f"{pin.location}: target blob bytes do not match tree object"
            )

        new_digest = (
            entry.oid.lower()
            if pin.algorithm == "sha1"
            else hashlib.sha256(raw).hexdigest()
        )

        old_source_token = source[record.start:record.end]
        if pin.location.endswith("]") and ".d_source_blobs[" in pin.location:
            if old_source_token.lower() != pin.digest.lower():
                raise bp.BlobPinError(
                    f"{pin.location}: SHA child span does not match parsed digest"
                )
            replacement_text = new_digest
        else:
            replacement_text = _source_scalar_replacement(
                source, record.start, record.end, new_digest
            )

        replacements.append(
            Replacement(
                record.start,
                record.end,
                old_source_token,
                replacement_text,
                pin.location,
                pin.path,
                entry.oid.lower(),
                len(raw),
            )
        )

    # Existing *_bytes fields are updated only when their paired *_file path
    # is present in the same mapping. No new field is ever created.
    for location, path, scalar in _collect_bytes_targets(document):
        entry = candidate_entries.get(path)
        if entry is None or entry.object_type != "blob":
            continue
        raw = read_blob(repo, entry)
        if bp._git_blob_sha1(raw) != entry.oid.lower():
            raise bp.BlobPinError(
                f"{location}: target blob bytes do not match tree object"
            )
        start = getattr(scalar, "start", None)
        end = getattr(scalar, "end", None)
        line = getattr(scalar, "line", None)
        if start is None or end is None or line is None:
            raise bp.BlobPinError(
                f"{location}: *_bytes scalar has no exact parser span"
            )
        new_value = str(len(raw))
        token = source[start:end]
        if token.startswith(("'", '"')):
            replacement_text = _source_scalar_replacement(
                source, start, end, new_value
            )
        else:
            replacement_text = new_value
        replacements.append(
            Replacement(
                start,
                end,
                token,
                replacement_text,
                location,
                path,
                entry.oid.lower(),
                len(raw),
            )
        )

    replacements.sort(key=lambda item: (item.start, item.end))
    for previous, current in zip(replacements, replacements[1:]):
        if current.start < previous.end:
            raise bp.BlobPinError(
                f"overlapping token spans: {previous.location} and "
                f"{current.location}"
            )

    # Every target span is checked against its exact old source slice before
    # constructing any modified source.
    for item in replacements:
        if source[item.start:item.end] != item.old:
            raise bp.BlobPinError(
                f"{item.location}: source token changed after parsing"
            )

    updated = source
    for item in reversed(replacements):
        updated = (
            updated[:item.start]
            + item.new
            + updated[item.end:]
        )

    return replacements, updated


def _pin_signature(records):
    return [
        (
            record.pin.path,
            record.pin.algorithm,
            record.pin.location,
            record.pin.source_commit,
        )
        for record in records
    ]


def _verify_rewritten_source(before, after, replacements, old_records):
    # Explicitly reconstruct the expected source using only the approved
    # half-open character spans. Any other character difference fails.
    expected = before
    for item in reversed(replacements):
        expected = expected[:item.start] + item.new + expected[item.end:]
    if after != expected:
        raise bp.BlobPinError(
            "post-write source differs outside the approved token spans"
        )

    new_records, diagnostics = bp._enumerate_pin_records(after)
    if diagnostics:
        raise bp.BlobPinError(
            "post-write parser diagnostics: "
            + "; ".join(item.message for item in diagnostics)
        )
    if _pin_signature(old_records) != _pin_signature(new_records):
        raise bp.BlobPinError(
            "post-write pin path/location/algorithm/source_commit changed"
        )

    # Every resulting digest must be syntactically valid. Exact blob identity
    # is checked by the subsequent audit against the same commit tree.
    for record in new_records:
        if not bp._valid_digest(record.pin.digest, record.pin.algorithm):
            raise bp.BlobPinError(
                f"{record.pin.location}: post-write digest is invalid"
            )


def _write_atomically(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


def reanchor(args) -> int:
    repo = Path(args.repo).resolve()
    commit = resolve_commit(repo, args.ref)
    head = resolve_commit(repo, "HEAD")

    if args.write and head != commit:
        raise AuditUnavailable(
            f"--write requires HEAD == ref: HEAD={head}, ref={commit}"
        )

    entries = read_tree(repo, commit)
    manifests = discover_manifests(repo, commit)
    exclusions = [parse_exclusion(item) for item in args.contract_exclusion]
    historical_cache = {}
    planned = []
    originals = {}

    for manifest_path in manifests:
        exclusion = matching_exclusion(manifest_path, exclusions)
        if exclusion is not None:
            print(
                f"EXCLUDED rule-id={exclusion.rule_id} "
                f"path={manifest_path}"
            )
            continue

        raw, source = load_manifest(
            repo, commit, manifest_path, entries
        )
        records, diagnostics = bp._enumerate_pin_records(source)
        if diagnostics:
            for diagnostic in diagnostics:
                print(
                    f"ERROR path={manifest_path} "
                    f"location={diagnostic.location} "
                    f"reason={diagnostic.reason.value} "
                    f"message={diagnostic.message}"
                )
            # A manifest with any parser/binding error is never rewritten.
            continue

        document = bp._parse_yaml_subset(source)
        replacements, updated = _make_replacements(
            repo,
            source,
            records,
            document,
            entries,
            historical_cache,
        )
        _verify_rewritten_source(
            source, updated, replacements, records
        )

        if not replacements:
            continue

        updated_bytes = updated.encode("utf-8")
        if args.write:
            working_path = repo / manifest_path
            try:
                current_bytes = working_path.read_bytes()
            except OSError as exc:
                raise AuditUnavailable(
                    f"cannot read working manifest {manifest_path}: {exc}"
                ) from exc
            if current_bytes != raw:
                raise AuditUnavailable(
                    f"working manifest differs from commit blob; refusing "
                    f"to overwrite: {manifest_path}"
                )
            originals[working_path] = current_bytes
            planned.append((working_path, updated_bytes, manifest_path))
        else:
            planned.append((None, updated_bytes, manifest_path))

        for item in replacements:
            print(
                f"CHANGE manifest={manifest_path} "
                f"location={item.location} "
                f"path={item.path} "
                f"old={item.old!r} new={item.new!r} "
                f"blob={item.object_id} bytes={item.byte_size}"
            )

    if not args.write:
        print(
            f"DRY-RUN commit={commit} manifests={len(manifests)} "
            f"files_to_change={len(planned)}"
        )
        return 0

    written = []
    try:
        for working_path, updated_bytes, manifest_path in planned:
            _write_atomically(working_path, updated_bytes)
            written.append(working_path)
            print(f"WRITTEN path={manifest_path}")
    except Exception:
        for working_path in reversed(written):
            try:
                _write_atomically(
                    working_path,
                    originals[working_path],
                )
            except Exception as rollback_exc:
                print(
                    f"ROLLBACK-ERROR path={working_path}: {rollback_exc}",
                    file=sys.stderr,
                )
        raise

    print(
        f"REANCHORED commit={commit} manifests={len(manifests)} "
        f"files_changed={len(written)}"
    )
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description="Audit/reanchor manifest blob pins using Git commit blobs."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="repository working directory (default: current directory)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("audit", "reanchor"):
        sub = subparsers.add_parser(name)
        sub.add_argument(
            "--ref",
            default="HEAD",
            help="commit-ish to audit (default: HEAD)",
        )
        sub.add_argument(
            "--contract-exclusion",
            action="append",
            default=[],
            metavar="<path-glob>=<rule-id>",
            help="explicitly exclude matching manifest paths under a rule ID",
        )
        if name == "reanchor":
            sub.add_argument(
                "--write",
                action="store_true",
                help="write changes; without this flag reanchor is dry-run",
            )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return audit(args) if args.command == "audit" else reanchor(args)
    except (AuditUnavailable, ValueError, OSError, bp.BlobPinError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
