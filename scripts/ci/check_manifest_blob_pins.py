#!/usr/bin/env python3
# scripts/ci/check_manifest_blob_pins.py
"""Verify every declared manifest blob pin against committed Git objects.

Exit status: 0 PASS, 1 VIOLATION, 2 INCOMPLETE (including unreadable Git data).
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
HEX64 = re.compile(r"^[0-9a-f]{64}$")

PROMPT_FIELDS = {"prompt_file", "prompt_sha256", "prompt_bytes"}
PROMPT_DIGEST_FIELDS = {"prompt_sha256"}
PROMPT_DIGEST_PATTERN = re.compile(
    r"(?:digest|sha(?:1|256|384|512)|md5)", re.IGNORECASE
)


class Incomplete(Exception):
    pass


class Violation(Exception):
    pass


class Git:
    def __init__(self, root: Path):
        self.root = root

    def run(self, *args: str) -> bytes:
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
            raise Incomplete(
                p.stderr.decode("utf-8", "replace").strip()
                or f"git {' '.join(args)} failed ({p.returncode})"
            )
        return p.stdout

    def object_bytes(self, commit: str, path: str) -> bytes:
        if not isinstance(commit, str) or not re.fullmatch(
            r"[0-9a-fA-F]{7,40}", commit
        ):
            raise Incomplete(
                f"invalid or absent source commit for {path}: {commit!r}"
            )

        try:
            resolved = self.run(
                "rev-parse", "--verify", f"{commit}^{{commit}}"
            ).decode().strip()
        except Incomplete as exc:
            raise Incomplete(
                f"source commit unavailable for {path}: {commit}"
            ) from exc

        if not HEX40.fullmatch(resolved):
            raise Incomplete(
                f"source commit did not resolve uniquely for {path}: {commit}"
            )

        spec = f"{resolved}:{path}"
        p = subprocess.run(
            ["git", "cat-file", "blob", spec],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if p.returncode:
            raise Violation(f"PATH_MISSING path={path}")
        return p.stdout


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def as_mapping(value):
    return value if isinstance(value, dict) else {}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def discover_manifests(git: Git, commit: str):
    names = (
        git.run("ls-tree", "-r", "--name-only", commit)
        .decode("utf-8")
        .splitlines()
    )
    return sorted(
        p
        for p in names
        if p.startswith(MANIFEST_ROOT + "/")
        and p.endswith("/manifest.yaml")
    )


def is_unrecognized_prompt_digest_field(name):
    """Recognize digest-like fields without silently accepting new spellings."""
    if not isinstance(name, str):
        return False
    return (
        name not in PROMPT_FIELDS
        and name.lower().startswith("prompt_")
        and PROMPT_DIGEST_PATTERN.search(name) is not None
    )


def verify(root: Path, commit: str, verbose: bool = True):
    git = Git(root)
    manifests = discover_manifests(git, commit)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {commit}")

    ok = mismatch = missing = incomplete = pins = 0
    prompt_declared = 0
    prompt_compared = 0
    problems = []
    prompt_checks = []

    def check(
        path,
        declared,
        source_commit,
        kind,
        algorithm="git",
    ):
        nonlocal ok, mismatch, missing, incomplete, pins

        # Empty/null placeholders retain their historical meaning.
        if declared is None or (
            isinstance(declared, str) and not declared.strip()
        ):
            return False

        pins += 1

        if algorithm == "bytes":
            if (
                isinstance(declared, bool)
                or not isinstance(declared, (int, str))
                or str(declared).strip() == ""
            ):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE {kind}: invalid byte-count declaration "
                    f"{declared!r}"
                )
                return False
        elif not isinstance(declared, str) or not declared.strip():
            incomplete += 1
            problems.append(
                f"INCOMPLETE {kind}: invalid digest declaration "
                f"{declared!r}"
            )
            return False

        if not nonempty(path):
            missing += 1
            problems.append(
                f"PATH_MISSING {kind} path=<not-declared> "
                f"declared={declared}"
            )
            return False

        try:
            data = git.object_bytes(source_commit, path)
        except Violation as exc:
            missing += 1
            problems.append(f"{exc}; declared={declared}")
            return False
        except Incomplete as exc:
            incomplete += 1
            problems.append(
                f"INCOMPLETE {kind} path={path}: {exc}"
            )
            return False

        actual = (
            hashlib.sha256(data).hexdigest()
            if algorithm == "sha256"
            else git_blob_sha(data)
        )

        if algorithm == "bytes":
            try:
                expected_bytes = int(declared)
            except (TypeError, ValueError):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE {kind} path={path}: "
                    f"invalid byte count {declared!r}"
                )
                return False

            actual = str(len(data))
            declared = str(expected_bytes)

        if actual != str(declared).lower():
            mismatch += 1
            problems.append(
                f"MISMATCH {kind} path={path} "
                f"declared={declared} actual={actual}"
            )
        else:
            ok += 1

        # True means that bytes were actually retrieved and compared.
        return True

    def check_prompt(path, declared, source_commit, kind):
        nonlocal prompt_declared, prompt_compared, prompt_checks

        if declared is None or (
            isinstance(declared, str) and not declared.strip()
        ):
            return

        prompt_declared += 1
        if check(path, declared, source_commit, kind, "sha256"):
            prompt_compared += 1
            prompt_checks.append(
                f"CHECKED {kind} path={path} declared={declared}"
            )

    for manifest_path in manifests:
        try:
            raw = git.object_bytes(commit, manifest_path)
            doc = yaml.safe_load(raw.decode("utf-8"))
        except (
            UnicodeError,
            yaml.YAMLError,
            Incomplete,
            Violation,
        ) as exc:
            incomplete += 1
            problems.append(
                f"INCOMPLETE manifest={manifest_path}: {exc}"
            )
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
        for i, item in enumerate(
            doc.get("gate_a_reconstruction", []) or []
        ):
            if not isinstance(item, dict):
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

        # B2. authored_indexes[] uses the same root and mirror pin shape.
        source_evidence = as_mapping(
            doc.get("baseline_and_source_evidence")
        )
        authored_indexes = source_evidence.get(
            "authored_indexes",
            doc.get("authored_indexes", []),
        )

        for i, item in enumerate(authored_indexes or []):
            if not isinstance(item, dict):
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
        for i, item in enumerate(
            doc.get("related_evidence", []) or []
        ):
            if not isinstance(item, dict):
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

        # F. Prompt snapshots: SHA-256 and byte length are over committed
        # bytes, not Git blob IDs.
        #
        # First reject unrecognized digest-like spellings.
        for field in doc:
            if is_unrecognized_prompt_digest_field(field):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE manifest={manifest_path}: "
                    f"unrecognized prompt digest field={field}"
                )

        prompt = as_mapping(doc.get("prompt"))

        for field in prompt:
            if is_unrecognized_prompt_digest_field(field):
                incomplete += 1
                problems.append(
                    f"INCOMPLETE manifest={manifest_path}: "
                    f"unrecognized nested prompt digest field={field}"
                )

        # Top-level prompt SHA-256.
        #
        # Explicit prompt_file has precedence. Only when the key is absent
        # do we use the work item's conventional prompt-v1.md path.
        if "prompt_sha256" in doc:
            if "prompt_file" in doc:
                top_level_prompt_path = doc.get("prompt_file")
            else:
                top_level_prompt_path = (
                    Path(manifest_path).parent / "prompt-v1.md"
                ).as_posix()

            check_prompt(
                top_level_prompt_path,
                doc.get("prompt_sha256"),
                commit,
                "prompt.top_level",
            )

        # Preserve nested prompt semantics.
        if "prompt_sha256" in prompt:
            check_prompt(
                prompt.get("prompt_file"),
                prompt.get("prompt_sha256"),
                commit,
                "prompt.nested",
            )

        if "prompt_bytes" in prompt:
            check(
                prompt.get("prompt_file"),
                prompt.get("prompt_bytes"),
                commit,
                "prompt.nested",
                "bytes",
            )

        # Session evidence prompt snapshots.
        for i, item in enumerate(
            doc.get("session_evidence", []) or []
        ):
            if not isinstance(item, dict):
                continue

            path_key = "executed_prompt_snapshot_file"
            sha_key = "executed_prompt_sha256"
            bytes_key = "executed_prompt_bytes"

            if sha_key in item:
                check(
                    item.get(path_key),
                    item.get(sha_key),
                    commit,
                    f"session_evidence[{i}].{path_key}",
                    "sha256",
                )

            if bytes_key in item:
                check(
                    item.get(path_key),
                    item.get(bytes_key),
                    commit,
                    f"session_evidence[{i}].{path_key}",
                    "bytes",
                )

    # Fail closed if any non-empty prompt SHA-256 declaration did not
    # participate in an actual byte-level comparison.
    if prompt_declared != prompt_compared:
        incomplete += 1
        problems.append(
            "PROMPT_COVERAGE "
            f"declared={prompt_declared} compared={prompt_compared}"
        )

    if verbose:
        print(
            f"main={commit} manifests={len(manifests)} pins={pins} "
            f"ok={ok} mismatch={mismatch} path_missing={missing} "
            f"incomplete={incomplete} "
            f"prompt_declared={prompt_declared} "
            f"prompt_compared={prompt_compared}"
        )
        for problem in problems:
            print(problem)
        for record in prompt_checks:
            print(record)

    return 2 if incomplete else (1 if mismatch or missing else 0)


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
        return verify(args.root, commit)
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
