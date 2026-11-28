#!/usr/bin/env python3
"""Verify every declared manifest blob pin against committed Git objects.

Exit status: 0 PASS, 1 CLASSIFIED VIOLATION, 2 SCAN/EXECUTION INCOMPLETE.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import yaml

MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
COMMIT_REF = re.compile(r"^[0-9a-fA-F]{7,40}$")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
# A blob_sha256 declaration is a claim about committed file bytes. The name
# token may carry a qualifier suffix (model_blob_sha256_lf); the declaration is
# still a blob digest and still needs a path. An unbound one is a violation,
# never an out-of-scope field: PR #1417 comment 7212343821 rejected exactly
# that exclusion.
BLOB_SHA256_KEY = re.compile(r"^(?P<base>(?:.*_)?)blob_sha256(?:_[a-z0-9]+)*$")


class Incomplete(Exception):
    """The scan itself could not be completed."""


class Unresolved(Exception):
    """A declared source or locator cannot be resolved deterministically."""

    def __init__(self, reason: str, detail: str):
        super().__init__(detail)
        self.reason = reason


class Violation(Exception):
    """A declared path is missing from its source commit."""


class Git:
    def __init__(self, root: Path):
        self.root = root
        self.object_types: dict[str, str | None] = {}

    def run(self, *args: str) -> bytes:
        """Run a required Git command; any nonzero result aborts the scan."""
        try:
            p = subprocess.run(
                ["git", *args],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot execute git: {exc}") from exc

        if p.returncode:
            detail = p.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(
                detail or f"git {' '.join(args)} failed ({p.returncode})"
            )
        return p.stdout

    def query(self, *args: str):
        """Run a Git query whose nonzero result may be classifiable."""
        try:
            return subprocess.run(
                ["git", *args],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise Incomplete(f"cannot execute git: {exc}") from exc

    def object_type(self, oid: str) -> str | None:
        """Return a known object type; None means no type could be resolved.

        A missing object is deliberately not an UNRESOLVED result. The caller
        must continue with the original locator-based content verification.
        """
        if oid not in self.object_types:
            p = self.query("cat-file", "-t", oid)
            if p.returncode:
                self.object_types[oid] = None
            else:
                self.object_types[oid] = p.stdout.decode(
                    "ascii", "replace"
                ).strip()
        return self.object_types[oid]

    def resolve_source_commit(self, commit: str | None, path: str) -> str:
        if not isinstance(commit, str) or not COMMIT_REF.fullmatch(commit):
            raise Unresolved(
                "SOURCE_MISSING",
                f"source commit missing or invalid for {path}: {commit!r}",
            )

        p = self.query("rev-parse", "--verify", f"{commit}^{{commit}}")
        if p.returncode:
            raise Unresolved(
                "SOURCE_MISSING",
                f"source commit unavailable for {path}: {commit}",
            )

        resolved = p.stdout.decode("ascii", "replace").strip()
        if not HEX40.fullmatch(resolved):
            raise Unresolved(
                "SOURCE_MISSING",
                f"source commit did not resolve to a full commit for {path}: "
                f"{commit}",
            )
        return resolved

    def manifest_bytes(self, commit: str, path: str) -> bytes:
        """Read a manifest from the scan commit; failure aborts the scan."""
        p = self.query("cat-file", "blob", f"{commit}:{path}")
        if p.returncode:
            detail = p.stderr.decode("utf-8", "replace").strip()
            raise Incomplete(
                f"cannot read manifest blob {path}: {detail or 'git cat-file failed'}"
            )
        return p.stdout

    def pinned_bytes(self, commit: str, path: str) -> bytes:
        """Read a declared locator; classify missing/ambiguous paths."""
        p = self.query("cat-file", "blob", f"{commit}:{path}")
        if p.returncode:
            detail = p.stderr.decode("utf-8", "replace").strip()
            if "ambiguous" in detail.lower():
                raise Unresolved(
                    "PATH_AMBIGUOUS",
                    detail or f"ambiguous path in source commit: {path}",
                )
            raise Violation(f"PATH_MISSING path={path}")
        return p.stdout


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def as_mapping(value):
    return value if isinstance(value, dict) else {}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def pointer_token(key):
    return str(key).replace("~", "~0").replace("/", "~1")


def walk_declarations(node, pointer=""):
    """Yield (pointer, field, value, containing mapping) for every blob_sha256 key."""
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


def bind_paths(container, field):
    """Return (bindings, invalid) for a declaration, in the main-branch order.

    ``bindings`` holds every non-empty (key, path) the declaration offers, so
    two live locators surface as ambiguity instead of silently picking the
    first one. ``invalid`` holds keys that exist but carry no usable value.
    """
    match = BLOB_SHA256_KEY.match(field)
    base = match.group("base").rstrip("_") if match else ""
    names = ([f"{base}_path", f"{base}_file"] if base else []) + ["path", "file"]
    bindings = []
    invalid = []
    for name in names:
        if name not in container:
            continue
        value = container.get(name)
        if nonempty(value):
            bindings.append((name, value.strip()))
        else:
            invalid.append(name)
    # A bare base key ("root" for "root_blob_sha256") counts only when the
    # value reads as a path, so a description string cannot be mistaken for one.
    if not bindings and base and base in container:
        value = container.get(base)
        if nonempty(value) and ("/" in value or re.search(r"\.[A-Za-z0-9]{1,8}$", value)):
            bindings.append((base, value.strip()))
        elif value is not None:
            invalid.append(base)
    return bindings, invalid


def discover_manifests(git: Git, commit: str):
    names = git.run("ls-tree", "-r", "--name-only", commit).decode(
        "utf-8"
    ).splitlines()
    return sorted(
        path for path in names
        if path.startswith(MANIFEST_ROOT + "/")
        and path.endswith("/manifest.yaml")
    )


def verify(root: Path, commit: str, verbose: bool = True):
    git = Git(root)
    manifests = discover_manifests(git, commit)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {commit}")

    pins = ok = mismatch = missing = 0
    unresolved = non_blob = incomplete = unbound = 0
    problems: list[str] = []
    current_manifest = "<unknown>"

    def record_unresolved(kind, declared, exc):
        nonlocal unresolved
        unresolved += 1
        problems.append(
            f"INCOMPLETE UNRESOLVED({exc.reason}): "
            f"manifest={current_manifest} field={kind} "
            f"declared={declared!r}: {exc}"
        )

    def record_invalid_declaration(kind, declared, detail):
        record_unresolved(
            kind,
            declared,
            Unresolved("DECLARATION_INVALID", detail),
        )

    def check(path, declared, source_commit, kind, algorithm="git"):
        nonlocal pins, ok, mismatch, missing, unresolved, non_blob, incomplete

        # Empty/null placeholders are outside the checker scope.
        if declared is None or (
            isinstance(declared, str) and not declared.strip()
        ):
            return

        # Object-type probing is only a NON_BLOB discriminator.
        # Missing objects deliberately fall through to locator verification.
        if algorithm == "git" and isinstance(declared, str):
            if HEX40.fullmatch(declared):
                object_kind = git.object_type(declared)
                if object_kind in ("commit", "tree", "tag"):
                    non_blob += 1
                    return

        # Preserve the legacy meaning: every non-empty checked declaration
        # counts as a pin, including a declaration that later has a missing
        # locator or an unresolved source commit.
        pins += 1

        if algorithm == "bytes":
            if (
                isinstance(declared, bool)
                or not isinstance(declared, (int, str))
                or str(declared).strip() == ""
            ):
                record_invalid_declaration(
                    kind, declared,
                    f"invalid byte-count declaration {declared!r}",
                )
                return
        elif not isinstance(declared, str) or not declared.strip():
            record_invalid_declaration(
                kind, declared,
                f"invalid digest declaration {declared!r}",
            )
            return

        if not nonempty(path):
            missing += 1
            problems.append(
                f"PATH_MISSING {kind} path=<not-declared> declared={declared}"
            )
            return

        try:
            resolved = git.resolve_source_commit(source_commit, path)
            data = git.pinned_bytes(resolved, path)
        except Unresolved as exc:
            record_unresolved(kind, declared, exc)
            return
        except Violation as exc:
            missing += 1
            problems.append(f"{exc}; declared={declared}")
            return
        except Incomplete as exc:
            incomplete += 1
            problems.append(f"INCOMPLETE {kind} path={path}: {exc}")
            return

        if algorithm == "sha256":
            actual = hashlib.sha256(data).hexdigest()
        elif algorithm == "bytes":
            try:
                expected_bytes = int(declared)
            except (TypeError, ValueError):
                record_invalid_declaration(
                    kind, declared,
                    f"invalid byte count {declared!r}",
                )
                return
            actual = str(len(data))
            declared = str(expected_bytes)
        else:
            actual = git_blob_sha(data)

        if actual != str(declared).lower():
            mismatch += 1
            problems.append(
                f"MISMATCH {kind} path={path} "
                f"declared={declared} actual={actual}"
            )
        else:
            ok += 1

    for manifest_path in manifests:
        current_manifest = manifest_path
        try:
            raw = git.manifest_bytes(commit, manifest_path)
            doc = yaml.safe_load(raw.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError, Incomplete) as exc:
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: {exc}")
            continue

        if not isinstance(doc, dict):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: "
                "top-level YAML is not a mapping"
            )
            continue

        # A. Root and language mirrors.
        for path_key, digest_key in (
            ("root", "root_blob"),
            ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        ):
            if digest_key in doc:
                check(
                    doc.get(path_key),
                    doc.get(digest_key),
                    commit,
                    f"index.{path_key}",
                )

        # B. gate_a_reconstruction[].root -> reconstructed_root_blob.
        entries = doc.get("gate_a_reconstruction", []) or []
        if not isinstance(entries, list):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: "
                "gate_a_reconstruction is not a list"
            )
        else:
            for i, item in enumerate(entries):
                if not isinstance(item, dict):
                    incomplete += 1
                    problems.append(
                        f"INCOMPLETE manifest={manifest_path}: "
                        f"gate_a_reconstruction[{i}] is not a mapping"
                    )
                    continue

                if "reconstructed_root_blob" in item:
                    source = item.get("source_commit") or item.get("commit")
                    if not source and nonempty(item.get("note")):
                        match = re.search(
                            r"\bcommit\s+([0-9a-f]{40})\b",
                            item["note"],
                        )
                        source = match.group(1) if match else None

                    check(
                        item.get("root"),
                        item.get("reconstructed_root_blob"),
                        source,
                        f"gate_a_reconstruction[{i}].root",
                    )

        # B2. authored_indexes[].
        source_evidence = as_mapping(
            doc.get("baseline_and_source_evidence")
        )
        authored_indexes = source_evidence.get(
            "authored_indexes",
            doc.get("authored_indexes", []),
        )
        if authored_indexes is None:
            authored_indexes = []

        if not isinstance(authored_indexes, list):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: "
                "authored_indexes is not a list"
            )
        else:
            for i, item in enumerate(authored_indexes):
                if not isinstance(item, dict):
                    incomplete += 1
                    problems.append(
                        f"INCOMPLETE manifest={manifest_path}: "
                        f"authored_indexes[{i}] is not a mapping"
                    )
                    continue

                for path_key, digest_key in (
                    ("root", "root_blob"),
                    ("en_mirror", "en_mirror_blob"),
                    ("zh_cn_mirror", "zh_cn_mirror_blob"),
                ):
                    if digest_key in item:
                        check(
                            item.get(path_key),
                            item.get(digest_key),
                            commit,
                            f"authored_indexes[{i}].{path_key}",
                        )

        # C. related_evidence[].path/blob and language mirrors.
        entries = doc.get("related_evidence", []) or []
        if not isinstance(entries, list):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: "
                "related_evidence is not a list"
            )
        else:
            for i, item in enumerate(entries):
                if not isinstance(item, dict):
                    incomplete += 1
                    problems.append(
                        f"INCOMPLETE manifest={manifest_path}: "
                        f"related_evidence[{i}] is not a mapping"
                    )
                    continue

                for path_key, digest_key in (
                    ("path", "blob"),
                    ("en_mirror", "en_mirror_blob"),
                    ("zh_cn_mirror", "zh_cn_mirror_blob"),
                ):
                    if digest_key in item:
                        check(
                            item.get(path_key),
                            item.get(digest_key),
                            commit,
                            f"related_evidence[{i}].{path_key}",
                        )

        # D. Execution evidence file/blob pair.
        if "evidence_blob" in doc:
            check(
                doc.get("evidence_file"),
                doc.get("evidence_blob"),
                commit,
                "evidence_file",
            )

        # E. Cross-commit D source blobs.
        if "d_source_blobs" in doc:
            source = doc.get("d_source_commit")
            entries = doc.get("d_source_blobs")

            if not isinstance(entries, list):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE manifest={manifest_path}: "
                    "d_source_blobs is not a list"
                )
            else:
                for i, entry in enumerate(entries):
                    if not isinstance(entry, str) or ":" not in entry:
                        incomplete += 1
                        problems.append(
                            f"INCOMPLETE manifest={manifest_path}: "
                            f"malformed d_source_blobs[{i}]"
                        )
                        continue

                    name, digest = entry.rsplit(":", 1)
                    check(
                        name.strip(),
                        digest.strip(),
                        source,
                        f"d_source_blobs[{i}]",
                    )

        # F. Prompt snapshots: SHA-256 and byte length.
        prompt_value = doc.get("prompt", {})
        if prompt_value is not None and not isinstance(prompt_value, dict):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: "
                "prompt is not a mapping"
            )
            prompt = {}
        else:
            prompt = as_mapping(prompt_value)

        if "prompt_sha256" in prompt:
            check(
                prompt.get("prompt_file"),
                prompt.get("prompt_sha256"),
                commit,
                "prompt.prompt_file",
                "sha256",
            )

        if "prompt_bytes" in prompt:
            check(
                prompt.get("prompt_file"),
                prompt.get("prompt_bytes"),
                commit,
                "prompt.prompt_file",
                "bytes",
            )

        entries = doc.get("session_evidence", []) or []
        if not isinstance(entries, list):
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: "
                "session_evidence is not a list"
            )
        else:
            for i, item in enumerate(entries):
                if not isinstance(item, dict):
                    incomplete += 1
                    problems.append(
                        f"INCOMPLETE manifest={manifest_path}: "
                        f"session_evidence[{i}] is not a mapping"
                    )
                    continue

                path_key = "executed_prompt_snapshot_file"

                if "executed_prompt_sha256" in item:
                    check(
                        item.get(path_key),
                        item.get("executed_prompt_sha256"),
                        commit,
                        f"session_evidence[{i}].{path_key}",
                        "sha256",
                    )

                if "executed_prompt_bytes" in item:
                    check(
                        item.get(path_key),
                        item.get("executed_prompt_bytes"),
                        commit,
                        f"session_evidence[{i}].{path_key}",
                        "bytes",
                    )

        # G. Explicit blob_sha256 declarations, wherever they sit.
        # The field itself declares a blob pin, so it counts as a pin even
        # when no path binds it; that case is UNRESOLVED(UNBOUND), not a
        # silent skip. A generic 40/64-hex scalar is only a candidate, so an
        # unbound one is NO_PATH and is not a pin -- see AID-2026-343.
        for pointer, field, declared, container in walk_declarations(doc):
            if declared is None or (
                isinstance(declared, str) and not declared.strip()
            ):
                continue

            pins += 1

            if (
                isinstance(declared, bool)
                or not isinstance(declared, str)
                or not declared.strip()
            ):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} field={field}: "
                    f"invalid digest declaration {declared!r}"
                )
                continue

            declared = declared.strip()

            if not HEX64.fullmatch(declared):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE blob_sha256 manifest={manifest_path} "
                    f"pointer={pointer} field={field}: "
                    f"digest is not 64 hexadecimal characters: {declared!r}"
                )
                continue

            bindings, invalid = bind_paths(container, field)

            if len(bindings) > 1:
                unresolved += 1
                names = ", ".join(name for name, _ in bindings)
                problems.append(
                    f"INCOMPLETE UNRESOLVED(PATH_AMBIGUOUS): "
                    f"manifest={manifest_path} pointer={pointer} "
                    f"field={field} declared={declared} locators={names}"
                )
                continue

            if not bindings:
                if invalid:
                    unresolved += 1
                    problems.append(
                        f"INCOMPLETE UNRESOLVED(LOCATOR_INVALID): "
                        f"manifest={manifest_path} pointer={pointer} "
                        f"field={field} declared={declared} "
                        f"locator={invalid[0]}"
                    )
                else:
                    unbound += 1
                    unresolved += 1
                    problems.append(
                        f"INCOMPLETE UNRESOLVED(UNBOUND): "
                        f"manifest={manifest_path} pointer={pointer} "
                        f"field={field} declared={declared}"
                    )
                continue

            name, path = bindings[0]
            # Default to the candidate tree; only an explicit, mapping-local
            # source_commit/commit may redirect the read to history.
            source = (
                container.get("source_commit")
                or container.get("commit")
                or commit
            )

            try:
                resolved = git.resolve_source_commit(source, path)
                data = git.pinned_bytes(resolved, path)
            except Unresolved as exc:
                unresolved += 1
                problems.append(
                    f"INCOMPLETE UNRESOLVED({exc.reason}): "
                    f"manifest={manifest_path} pointer={pointer} "
                    f"field={field} declared={declared}: {exc}"
                )
                continue
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

    if verbose:
        # Legacy summary: retain its exact field order and formatting.
        print(
            f"main={commit} manifests={len(manifests)} pins={pins} ok={ok} "
            f"mismatch={mismatch} path_missing={missing} "
            f"incomplete={incomplete} unbound={unbound}"
        )
        print(
            f"verified={ok} mismatch={mismatch} path_missing={missing} "
            f"unresolved={unresolved} non_blob={non_blob} incomplete={incomplete}"
        )
        for problem in problems:
            print(problem)

    return 2 if incomplete else (
        1 if mismatch or missing or unresolved else 0
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args(argv)

    try:
        commit = (
            Git(args.root)
            .run("rev-parse", f"{args.commit}^{{commit}}")
            .decode()
            .strip()
        )
        if not HEX40.fullmatch(commit):
            raise Incomplete(
                f"requested commit did not resolve to a full commit: "
                f"{args.commit}"
            )
        return verify(args.root, commit)
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
