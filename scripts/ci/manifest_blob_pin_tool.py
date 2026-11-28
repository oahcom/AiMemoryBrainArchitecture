#!/usr/bin/env python3
"""Audit and reanchor manifest blob pins against exact Git commit trees."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
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
    """Git data or a required write precondition is unavailable."""


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
    raw = git(
        repo, "ls-tree", "-r", "--name-only", "-z",
        commit, "--", MANIFEST_ROOT,
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
        raise ValueError(
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


def verify_one_pin(repo, pin, candidate_entries, historical_cache):
    selected = pin_tree_for(
        repo, pin, candidate_entries, historical_cache
    )
    # Pin paths are always repository-root-relative. There is deliberately
    # no fallback to the manifest's directory.
    entry = selected.get(pin.path)
    if entry is None:
        raise bp.BlobPinError(
            f"{pin.location}: path_not_in_tree: "
            f"{pin.path!r} absent from selected commit tree"
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


def is_contract_error(exc: bp.BlobPinError) -> bool:
    message = str(exc).lower()
    return any(
        marker in message
        for marker in (
            "path_not_in_tree",
            "absent from selected commit tree",
            "is not a regular file blob",
            "historical source commit must be a full sha-1",
            "unsupported algorithm",
        )
    )


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
        except ValueError as exc:
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
                    repo, record.pin, entries, historical_cache
                )
            except bp.BlobPinError as exc:
                if is_contract_error(exc):
                    counts["errors"] += 1
                    print(
                        f"ERROR manifest={manifest_path} "
                        f"location={record.pin.location} "
                        f"reason={exc}"
                    )
                else:
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
    """Find existing *_bytes scalars paired with sibling *_file paths."""
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


def _diagnostic_signature(diagnostics):
    return [
        (
            item.location,
            item.reason.value,
            item.message,
        )
        for item in diagnostics
    ]


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


def _candidate_replacement(
    repo,
    source,
    *,
    start,
    end,
    line,
    location,
    path,
    new_value,
    object_id,
    byte_size,
    preserve_quote=True,
):
    if line is None:
        raise bp.BlobPinError(
            f"{location}: parser did not provide a source line"
        )
    if start is None or end is None:
        raise bp.BlobPinError(
            f"{location}: parser did not provide an exact token span"
        )
    if start < 0 or end <= start or end > len(source):
        raise bp.BlobPinError(
            f"{location}: token source span is invalid"
        )

    old = source[start:end]
    if preserve_quote:
        new = _source_scalar_replacement(
            source, start, end, str(new_value)
        )
    else:
        new = str(new_value)

    return Replacement(
        start, end, old, new, location, path, object_id, byte_size
    )


def _make_replacements(
    repo,
    source,
    records,
    document,
    candidate_entries,
    historical_cache,
):
    """Build independent candidates; one bad pin never aborts its siblings."""
    candidates = []
    errors = []

    # Pin digest candidates.
    for record in records:
        pin = record.pin
        try:
            selected = pin_tree_for(
                repo, pin, candidate_entries, historical_cache
            )
            # Always repository-root-relative; never resolve beside manifest.
            entry = selected.get(pin.path)
            if entry is None:
                raise bp.BlobPinError(
                    f"{pin.location}: path_not_in_tree: "
                    f"target path {pin.path!r} is absent from selected commit tree"
                )
            if entry.object_type != "blob" or entry.mode not in (
                "100644", "100755"
            ):
                raise bp.BlobPinError(
                    f"{pin.location}: target path {pin.path!r} is not "
                    "a regular file blob"
                )

            raw = read_blob(repo, entry)
            if bp._git_blob_sha1(raw) != entry.oid.lower():
                raise bp.BlobPinError(
                    f"{pin.location}: target blob bytes do not match "
                    "the Git tree object"
                )

            if pin.algorithm == "sha1":
                new_digest = entry.oid.lower()
            elif pin.algorithm == "sha256":
                new_digest = hashlib.sha256(raw).hexdigest()
            else:
                raise bp.BlobPinError(
                    f"{pin.location}: unsupported algorithm {pin.algorithm!r}"
                )

            # d_source_blobs stores "path: SHA" in one scalar. Its parser
            # record span is specifically the SHA child token, not the path.
            # Do not rewrite any other part of that scalar.
            source_list_child = (
                pin.location.endswith("]")
                and ".d_source_blobs[" in pin.location
            )
            if source_list_child:
                start, end = record.start, record.end
                if source[start:end].lower() != pin.digest.lower():
                    raise bp.BlobPinError(
                        f"{pin.location}: SHA child span does not match "
                        "the parsed digest"
                    )
                replacement = _candidate_replacement(
                    repo, source,
                    start=start,
                    end=end,
                    line=pin.line,
                    location=pin.location,
                    path=pin.path,
                    new_value=new_digest,
                    object_id=entry.oid.lower(),
                    byte_size=len(raw),
                    preserve_quote=False,
                )
            else:
                replacement = _candidate_replacement(
                    repo, source,
                    start=record.start,
                    end=record.end,
                    line=pin.line,
                    location=pin.location,
                    path=pin.path,
                    new_value=new_digest,
                    object_id=entry.oid.lower(),
                    byte_size=len(raw),
                )
            candidates.append(replacement)

        except bp.BlobPinError as exc:
            errors.append((pin.location, str(exc)))
        except AuditUnavailable:
            # Git object failures are infrastructure failures, not recoverable
            # per-pin contract errors.
            raise

    # Existing *_bytes candidates. These are independent of digest candidates.
    for location, path, scalar in _collect_bytes_targets(document):
        try:
            # No manifest-relative fallback: path must be repo-root-relative.
            entry = candidate_entries.get(path)
            if entry is None:
                raise bp.BlobPinError(
                    f"{location}: path_not_in_tree: "
                    f"target path {path!r} is absent from selected commit tree"
                )
            if entry.object_type != "blob" or entry.mode not in (
                "100644", "100755"
            ):
                raise bp.BlobPinError(
                    f"{location}: target path {path!r} is not a regular file blob"
                )

            raw = read_blob(repo, entry)
            if bp._git_blob_sha1(raw) != entry.oid.lower():
                raise bp.BlobPinError(
                    f"{location}: target blob bytes do not match "
                    "the Git tree object"
                )

            start = getattr(scalar, "start", None)
            end = getattr(scalar, "end", None)
            line = getattr(scalar, "line", None)
            replacement = _candidate_replacement(
                repo, source,
                start=start,
                end=end,
                line=line,
                location=location,
                path=path,
                new_value=str(len(raw)),
                object_id=entry.oid.lower(),
                byte_size=len(raw),
            )
            candidates.append(replacement)

        except bp.BlobPinError as exc:
            errors.append((location, str(exc)))
        except AuditUnavailable:
            raise

    # Same-line ambiguity is checked across all digest and bytes candidates.
    # Every candidate on an ambiguous line is refused, not just the later one.
    line_counts = {}
    for item in candidates:
        line = source.count("\n", 0, item.start) + 1
        line_counts[line] = line_counts.get(line, 0) + 1

    safe = []
    for item in candidates:
        line = source.count("\n", 0, item.start) + 1
        if line_counts[line] != 1:
            errors.append((
                item.location,
                f"{item.location}: multiple candidate scalar tokens on "
                f"source line {line}",
            ))
        else:
            safe.append(item)

    safe.sort(key=lambda item: (item.start, item.end))
    non_overlapping = []
    for item in safe:
        if non_overlapping and item.start < non_overlapping[-1].end:
            previous = non_overlapping[-1]
            errors.append((
                item.location,
                f"overlapping token spans: {previous.location} and "
                f"{item.location}",
            ))
            # Refuse both overlapping candidates.
            non_overlapping.pop()
        else:
            non_overlapping.append(item)

    # Verify all retained spans still identify exactly their parsed source text.
    verified = []
    for item in non_overlapping:
        if source[item.start:item.end] != item.old:
            errors.append((
                item.location,
                f"{item.location}: source token changed after parsing",
            ))
        else:
            verified.append(item)

    # No-op candidates are reported but never enter the write set.
    changes = []
    for item in verified:
        if item.old == item.new:
            print(
                f"NOOP location={item.location} path={item.path} "
                f"value={item.old!r} blob={item.object_id} "
                f"bytes={item.byte_size}"
            )
        else:
            changes.append(item)

    updated = source
    for item in reversed(changes):
        updated = (
            updated[:item.start]
            + item.new
            + updated[item.end:]
        )

    return changes, updated, errors


def _verify_rewritten_source(
    before,
    after,
    replacements,
    old_records,
    old_diagnostics,
):
    # Character offsets are Python str indices. Reconstruct only the approved
    # half-open token replacements; all other source characters must match.
    expected = before
    for item in reversed(replacements):
        expected = expected[:item.start] + item.new + expected[item.end:]
    if after != expected:
        raise bp.BlobPinError(
            "post-rewrite source differs outside approved token spans"
        )

    new_records, new_diagnostics = bp._enumerate_pin_records(after)
    if _diagnostic_signature(old_diagnostics) != _diagnostic_signature(
        new_diagnostics
    ):
        raise bp.BlobPinError(
            "post-rewrite parser/binding diagnostics changed"
        )

    if _pin_signature(old_records) != _pin_signature(new_records):
        raise bp.BlobPinError(
            "post-rewrite pin path/location/algorithm/source_commit changed"
        )

    # Confirm that every changed digest is the value emitted into its token.
    changed_digest_locations = {
        item.location: item.new.strip("'\"")
        for item in replacements
        if item.location in {record.pin.location for record in old_records}
    }
    for old_record, new_record in zip(old_records, new_records):
        expected_digest = changed_digest_locations.get(
            old_record.pin.location, old_record.pin.digest
        )
        if new_record.pin.digest != expected_digest:
            raise bp.BlobPinError(
                f"{new_record.pin.location}: post-rewrite digest differs "
                "from the planned token value"
            )

    for record in new_records:
        if not bp._valid_digest(record.pin.digest, record.pin.algorithm):
            raise bp.BlobPinError(
                f"{record.pin.location}: post-rewrite digest is invalid"
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
    error_count = 0
    noop_count = 0
    change_count = 0

    print(f"commit={commit}")

    for manifest_path in manifests:
        exclusion = matching_exclusion(manifest_path, exclusions)
        if exclusion is not None:
            print(
                f"EXCLUDED rule-id={exclusion.rule_id} "
                f"path={manifest_path}"
            )
            continue

        # Failure to read the manifest itself is Git/tree data failure.
        raw, source = load_manifest(
            repo, commit, manifest_path, entries
        )

        records, diagnostics = bp._enumerate_pin_records(source)
        yaml_failed = any(
            item.reason == bp.BlobPinErrorReason.YAML_PARSE
            for item in diagnostics
        )

        if yaml_failed:
            error_count += len(diagnostics)
            for diagnostic in diagnostics:
                print(
                    f"ERROR path={manifest_path} "
                    f"location={diagnostic.location} "
                    f"reason={diagnostic.reason.value} "
                    f"message={diagnostic.message}"
                )
            # A syntactically unparseable manifest has no safe rewrite scope.
            continue

        # Binding errors are recorded, but do not suppress independently
        # parsed pins from the same manifest.
        error_count += len(diagnostics)
        for diagnostic in diagnostics:
            print(
                f"ERROR path={manifest_path} "
                f"location={diagnostic.location} "
                f"reason={diagnostic.reason.value} "
                f"message={diagnostic.message}"
            )

        try:
            document = bp._parse_yaml_subset(source)
        except bp.BlobPinError as exc:
            error_count += 1
            print(
                f"ERROR path={manifest_path} location=$ "
                f"reason=yaml_parse message={exc}"
            )
            continue

        replacements, updated, candidate_errors = _make_replacements(
            repo,
            source,
            records,
            document,
            entries,
            historical_cache,
        )

        for location, message in candidate_errors:
            error_count += 1
            print(
                f"ERROR path={manifest_path} location={location} "
                f"reason=reanchor_refused message={message}"
            )

        try:
            _verify_rewritten_source(
                source,
                updated,
                replacements,
                records,
                diagnostics,
            )
        except bp.BlobPinError as exc:
            error_count += 1
            print(
                f"ERROR path={manifest_path} location=$ "
                f"reason=post_reparse message={exc}"
            )
            # Do not write any part of a manifest whose postcondition fails.
            continue

        if not replacements:
            continue

        # Convert character spans to byte offsets explicitly before preparing
        # bytes for disk. This also verifies the source encoding assumption.
        source_bytes = source.encode("utf-8")
        updated_bytes = updated.encode("utf-8")
        reconstructed = source_bytes
        for item in reversed(replacements):
            byte_start = len(source[:item.start].encode("utf-8"))
            byte_end = len(source[:item.end].encode("utf-8"))
            old_bytes = source_bytes[byte_start:byte_end]
            if old_bytes != item.old.encode("utf-8"):
                error_count += 1
                print(
                    f"ERROR path={manifest_path} location={item.location} "
                    "reason=byte_span_mismatch"
                )
                reconstructed = b""
                break
            reconstructed = (
                reconstructed[:byte_start]
                + item.new.encode("utf-8")
                + reconstructed[byte_end:]
            )

        if not reconstructed or reconstructed != updated_bytes:
            error_count += 1
            print(
                f"ERROR path={manifest_path} location=$ "
                "reason=utf8_byte_reconstruction_failed"
            )
            continue

        for item in replacements:
            change_count += 1
            print(
                f"CHANGE manifest={manifest_path} "
                f"location={item.location} "
                f"path={item.path} "
                f"old={item.old!r} new={item.new!r} "
                f"blob={item.object_id} bytes={item.byte_size}"
            )

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
                    "working manifest differs from commit blob; refusing "
                    f"to overwrite: {manifest_path}"
                )

            originals[working_path] = current_bytes
            planned.append((working_path, updated_bytes, manifest_path))
        else:
            planned.append((None, updated_bytes, manifest_path))

    # All worktree/commit comparisons happen before the first write.
    if not args.write:
        print(
            f"DRY-RUN commit={commit} manifests={len(manifests)} "
            f"files_to_change={len(planned)} changes={change_count} "
            f"errors={error_count}"
        )
        return 1 if error_count else 0

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
        f"files_changed={len(written)} changes={change_count} "
        f"errors={error_count}"
    )
    return 1 if error_count else 0


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
    except AuditUnavailable as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2
    except (ValueError, OSError, bp.BlobPinError) as exc:
        # This outer handler is for errors that escaped the per-item
        # recoverable paths. Ordinary parser/binding/pin errors are handled
        # and counted inside audit/reanchor.
        print(f"FATAL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
