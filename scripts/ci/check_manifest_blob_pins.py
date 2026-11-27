#!/usr/bin/env python3
"""Fail-closed verification of every registered manifest blob identity.

Exit status: 0 PASS, 1 VIOLATION, 2 INCOMPLETE/UNRESOLVED.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import yaml

MANIFEST_ROOT = "14-ai-development/work-items"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

PIN_FIELD_REGISTRY = (
    ("root_blob", "root", "candidate commit", "Git blob SHA-1"),
    ("en_mirror_blob", "en_mirror", "candidate commit", "Git blob SHA-1"),
    ("zh_cn_mirror_blob", "zh_cn_mirror", "candidate commit", "Git blob SHA-1"),
    ("reconstructed_root_blob", "root", "entry source_commit/commit", "Git blob SHA-1"),
    ("related_evidence[].blob", "related_evidence[].path", "candidate commit", "Git blob SHA-1"),
    ("evidence_blob", "evidence_file", "candidate commit", "Git blob SHA-1"),
    ("d_source_blobs[]", "inline <path>: <sha>", "d_source_commit", "Git blob SHA-1"),
    ("prompt.prompt_sha256", "prompt.prompt_file", "candidate commit", "SHA-256(bytes)"),
    ("prompt.prompt_bytes", "prompt.prompt_file", "candidate commit", "byte length"),
    ("session_evidence[].executed_prompt_sha256/bytes", "executed_prompt_snapshot_file", "candidate commit", "SHA-256(bytes)/byte length"),
    ("prompt_sha256 (top-level)", "prompt_file or prompt-v{prompt_version}.md", "candidate commit", "SHA-256(bytes)"),
    ("source_translation_pairs[].source_blob_sha", "source_path", "source_commit_sha", "Git blob SHA-1"),
    ("source_translation_pairs[].translation_blob_sha", "translation_path", "translation_commit_sha", "Git blob SHA-1"),
    ("source_translation_pairs[].translation_sha256", "translation_path", "translation_commit_sha", "SHA-256(bytes)"),
    ("source_translation_pairs[].reverified_*_blob_sha", "corresponding *_path", "reverification commit or candidate", "Git blob SHA-1"),
    ("source_blobs[].sha", "source_blobs[].path", "base_commit/baseline_commit", "Git blob SHA-1"),
    ("source.selected_source_files[].source_blob_sha", "path", "source.head_sha", "Git blob SHA-1"),
    ("source.selected_source_files[].restored_blob_sha", "path", "candidate commit", "Git blob SHA-1"),
    ("source.selected_source_files[].frontmatter_blob_sha", "frontmatter_path/frontmatter_file", "declared source commit/candidate", "Git blob SHA-1; unresolved without locator"),
    ("source.files[].blob", "source.files[].path", "source.head", "Git blob SHA-1"),
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
            p = subprocess.run(["git", *args], cwd=self.root, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
        except OSError as exc:
            raise Incomplete(f"cannot execute git: {exc}") from exc
        if p.returncode:
            raise Incomplete(p.stderr.decode("utf-8", "replace").strip() or
                             f"git {' '.join(args)} failed ({p.returncode})")
        return p.stdout

    def resolve_commit(self, commit: str, field: str) -> str:
        if field == "--commit" and commit == "HEAD":
            resolved = self.run("rev-parse", "--verify", "HEAD^{commit}").decode().strip()
            if not HEX40.fullmatch(resolved):
                raise Incomplete("UNRESOLVED(commit did not resolve uniquely): HEAD")
            return resolved
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit):
            raise Incomplete(f"UNRESOLVED(commit locator): {field}={commit!r}")
        try:
            resolved = self.run("rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()
        except Incomplete as exc:
            raise Incomplete(f"UNRESOLVED(commit unavailable): {field}={commit}") from exc
        if not HEX40.fullmatch(resolved):
            raise Incomplete(f"UNRESOLVED(commit did not resolve uniquely): {field}={commit}")
        return resolved

    def object_bytes(self, commit: str, path: str, field: str) -> bytes:
        resolved = self.resolve_commit(commit, field)
        if not isinstance(path, str) or not path.strip():
            raise Violation(f"PATH_MISSING {field} path=<not-declared>")
        normalized = PurePosixPath(path)
        if normalized.is_absolute() or ".." in normalized.parts:
            raise Incomplete(f"UNRESOLVED(unsafe repository path): {field} path={path!r}")
        spec = f"{resolved}:{normalized.as_posix()}"
        p = subprocess.run(["git", "cat-file", "blob", spec], cwd=self.root,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if p.returncode:
            raise Violation(f"PATH_MISSING {field} path={normalized.as_posix()}")
        return p.stdout

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def as_mapping(value):
    return value if isinstance(value, dict) else {}

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def discover_manifests(git: Git, commit: str):
    names = git.run("ls-tree", "-r", "--name-only", commit).decode("utf-8").splitlines()
    return sorted(p for p in names
                  if p.startswith(MANIFEST_ROOT + "/") and p.endswith("/manifest.yaml"))

def verify(root: Path, commit: str, verbose: bool = True):
    git = Git(root)
    commit = git.resolve_commit(commit, "--commit")
    manifests = discover_manifests(git, commit)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {commit}")
    ok = mismatch = missing = incomplete = pins = 0
    problems = []

    def check(path, declared, source_commit, kind, algorithm="git"):
        nonlocal ok, mismatch, missing, incomplete, pins
        pins += 1
        if algorithm == "bytes":
            if isinstance(declared, bool) or not isinstance(declared, (int, str)) or not str(declared).strip():
                incomplete += 1
                problems.append(f"INCOMPLETE {kind}: invalid byte-count declaration {declared!r}")
                return
        elif algorithm == "sha256":
            if not isinstance(declared, str) or not HEX64.fullmatch(declared):
                incomplete += 1
                problems.append(f"INCOMPLETE {kind}: invalid SHA-256 declaration {declared!r}")
                return
        elif not isinstance(declared, str) or not HEX40.fullmatch(declared):
            incomplete += 1
            problems.append(f"INCOMPLETE {kind}: invalid Git blob SHA-1 declaration {declared!r}")
            return
        if not nonempty(path):
            missing += 1
            problems.append(f"PATH_MISSING {kind} path=<not-declared> declared={declared}")
            return
        try:
            resolved_commit = git.resolve_commit(source_commit, kind)
            data = git.object_bytes(resolved_commit, path, kind)
            if algorithm == "git":
                resolved_locators.setdefault(str(declared).lower(), set()).add(
                    (resolved_commit, PurePosixPath(path).as_posix())
                )
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
                expected = int(declared)
            except (TypeError, ValueError):
                incomplete += 1
                problems.append(f"INCOMPLETE {kind} path={path}: invalid byte count {declared!r}")
                return
            actual = str(len(data))
            declared = str(expected)
        else:
            actual = git_blob_sha(data)
        if actual != str(declared).lower():
            mismatch += 1
            problems.append(f"MISMATCH {kind} path={path} declared={declared} actual={actual}")
        else:
            ok += 1

    def pair(mapping, path_key, digest_key, source_commit, kind, algorithm="git"):
        if digest_key in mapping:
            check(mapping.get(path_key), mapping.get(digest_key), source_commit, kind, algorithm)

    handled = set()
    resolved_locators = {}
    def mark(mapping, key):
        handled.add((id(mapping), key))

    for manifest_path in manifests:
        try:
            raw = git.object_bytes(commit, manifest_path, "manifest")
            doc = yaml.safe_load(raw.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError, Incomplete, Violation) as exc:
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: {exc}")
            continue
        if not isinstance(doc, dict):
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: top-level YAML is not a mapping")
            continue

        for path_key, digest_key in (("root", "root_blob"), ("en_mirror", "en_mirror_blob"),
                                     ("zh_cn_mirror", "zh_cn_mirror_blob")):
            pair(doc, path_key, digest_key, commit, f"index.{path_key}")
            mark(doc, digest_key)

        source_evidence = as_mapping(doc.get("baseline_and_source_evidence"))
        reconstruction = doc.get("gate_a_reconstruction")
        if reconstruction is None:
            reconstruction = source_evidence.get("gate_a_reconstruction", [])
        for i, item in enumerate(reconstruction or []):
            if not isinstance(item, dict):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: gate_a_reconstruction[{i}] is not a mapping")
                continue
            if "reconstructed_root_blob" in item:
                source_commit = item.get("source_commit") or item.get("commit")
                if not source_commit and nonempty(item.get("note")):
                    match = re.search(r"\bcommit\s+([0-9a-f]{40})\b", item["note"])
                    source_commit = match.group(1) if match else None
                pair(item, "root", "reconstructed_root_blob", source_commit,
                     f"gate_a_reconstruction[{i}].root")
                mark(item, "reconstructed_root_blob")
            for path_key, digest_key in (("en_mirror", "en_mirror_blob"),
                                         ("zh_cn_mirror", "zh_cn_mirror_blob")):
                pair(item, path_key, digest_key, item.get("source_commit") or item.get("commit") or commit,
                     f"gate_a_reconstruction[{i}].{path_key}")
                mark(item, digest_key)

        authored = source_evidence.get("authored_indexes", doc.get("authored_indexes", []))
        for i, item in enumerate(authored or []):
            if not isinstance(item, dict):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: authored_indexes[{i}] is not a mapping")
                continue
            for path_key, digest_key in (("root", "root_blob"), ("en_mirror", "en_mirror_blob"),
                                         ("zh_cn_mirror", "zh_cn_mirror_blob")):
                pair(item, path_key, digest_key, commit, f"authored_indexes[{i}].{path_key}")
                mark(item, digest_key)

        for i, item in enumerate(doc.get("related_evidence", []) or []):
            if not isinstance(item, dict):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: related_evidence[{i}] is not a mapping")
                continue
            for path_key, digest_key in (("path", "blob"), ("en_mirror", "en_mirror_blob"),
                                         ("zh_cn_mirror", "zh_cn_mirror_blob")):
                pair(item, path_key, digest_key, commit, f"related_evidence[{i}].{path_key}")
                mark(item, digest_key)

        if "evidence_blob" in doc:
            pair(doc, "evidence_file", "evidence_blob", commit, "evidence_file")
            mark(doc, "evidence_blob")

        if "d_source_blobs" in doc:
            entries = doc.get("d_source_blobs")
            if not isinstance(entries, list):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: d_source_blobs is not a list")
            else:
                for i, entry in enumerate(entries):
                    if not isinstance(entry, str) or ":" not in entry:
                        incomplete += 1
                        problems.append(f"INCOMPLETE manifest={manifest_path}: malformed d_source_blobs[{i}]")
                        continue
                    path, digest = entry.rsplit(":", 1)
                    check(path.strip(), digest.strip(), doc.get("d_source_commit"), f"d_source_blobs[{i}]")

        prompt = as_mapping(doc.get("prompt"))
        pair(prompt, "prompt_file", "prompt_sha256", commit, "prompt.prompt_file", "sha256")
        mark(prompt, "prompt_sha256")
        pair(prompt, "prompt_file", "prompt_bytes", commit, "prompt.prompt_file", "bytes")
        mark(prompt, "prompt_bytes")
        for i, item in enumerate(doc.get("session_evidence", []) or []):
            if not isinstance(item, dict):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: session_evidence[{i}] is not a mapping")
                continue
            pair(item, "executed_prompt_snapshot_file", "executed_prompt_sha256", commit,
                 f"session_evidence[{i}].executed_prompt_snapshot_file", "sha256")
            mark(item, "executed_prompt_sha256")
            pair(item, "executed_prompt_snapshot_file", "executed_prompt_bytes", commit,
                 f"session_evidence[{i}].executed_prompt_snapshot_file", "bytes")
            mark(item, "executed_prompt_bytes")

        if "prompt_sha256" in doc:
            version = doc.get("prompt_version")
            prompt_file = doc.get("prompt_file")
            if not nonempty(prompt_file):
                prompt_file = (str(PurePosixPath(manifest_path).parent / f"prompt-{version}.md")
                               if isinstance(version, str) and re.fullmatch(r"v[0-9]+", version)
                               else None)
            check(prompt_file, doc.get("prompt_sha256"), commit, "prompt_sha256(top-level)", "sha256")
            mark(doc, "prompt_sha256")

        pairs = doc.get("source_translation_pairs", []) or []
        if not isinstance(pairs, list):
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: source_translation_pairs is not a list")
        else:
            for i, item in enumerate(pairs):
                if not isinstance(item, dict):
                    incomplete += 1
                    problems.append(f"INCOMPLETE manifest={manifest_path}: source_translation_pairs[{i}] is not a mapping")
                    continue
                prefix = f"source_translation_pairs[{i}]"
                pair(item, "source_path", "source_blob_sha", item.get("source_commit_sha"), prefix + ".source_path")
                mark(item, "source_blob_sha")
                pair(item, "translation_path", "translation_blob_sha", item.get("translation_commit_sha"), prefix + ".translation_path")
                mark(item, "translation_blob_sha")
                pair(item, "translation_path", "translation_sha256", item.get("translation_commit_sha"),
                     prefix + ".translation_path", "sha256")
                mark(item, "translation_sha256")
                reverify_commit = (item.get("reverification_commit_sha") or
                                   item.get("reverified_at_commit"))
                if not reverify_commit and nonempty(item.get("reverification_note")):
                    note_commit = re.search(r"\bat\s+([0-9a-fA-F]{7,40})\b",
                                             item["reverification_note"])
                    reverify_commit = note_commit.group(1) if note_commit else None
                reverify_commit = reverify_commit or commit
                for path_key, digest_key in (("source_path", "reverified_source_blob_sha"),
                                             ("translation_path", "reverified_translation_blob_sha")):
                    pair(item, path_key, digest_key, reverify_commit, prefix + "." + digest_key)
                    mark(item, digest_key)

        source_blobs = doc.get("source_blobs")
        if source_blobs is None:
            source_blobs = as_mapping(doc.get("baseline_evidence")).get("source_blobs")
        if source_blobs is not None:
            if not isinstance(source_blobs, list):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: source_blobs is not a list")
            else:
                source_commit = doc.get("base_commit") or doc.get("base_commit_sha") or doc.get("baseline_commit")
                for i, item in enumerate(source_blobs):
                    if not isinstance(item, dict):
                        incomplete += 1
                        problems.append(f"INCOMPLETE manifest={manifest_path}: source_blobs[{i}] is not a mapping")
                        continue
                    pair(item, "path", "sha", source_commit, f"source_blobs[{i}]")
                    mark(item, "sha")

        source = as_mapping(doc.get("source"))
        selected = source.get("selected_source_files", [])
        if selected:
            if not isinstance(selected, list):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: source.selected_source_files is not a list")
            else:
                source_commit = source.get("head_sha") or source.get("head")
                for i, item in enumerate(selected):
                    if not isinstance(item, dict):
                        incomplete += 1
                        problems.append(f"INCOMPLETE manifest={manifest_path}: source.selected_source_files[{i}] is not a mapping")
                        continue
                    prefix = f"source.selected_source_files[{i}]"
                    pair(item, "path", "source_blob_sha", source_commit, prefix + ".source_blob_sha")
                    mark(item, "source_blob_sha")
                    pair(item, "path", "restored_blob_sha", commit, prefix + ".restored_blob_sha")
                    mark(item, "restored_blob_sha")
                    if "frontmatter_blob_sha" in item:
                        front_path = item.get("frontmatter_path") or item.get("frontmatter_file")
                        if not nonempty(front_path):
                            pins += 1
                            incomplete += 1
                            problems.append(f"INCOMPLETE UNRESOLVED({prefix}.frontmatter_blob_sha): no frontmatter_path/frontmatter_file locator")
                        else:
                            locator_key = "frontmatter_path" if "frontmatter_path" in item else "frontmatter_file"
                            pair(item, locator_key, "frontmatter_blob_sha", source_commit or commit,
                                 prefix + ".frontmatter_blob_sha")
                        mark(item, "frontmatter_blob_sha")

        files = source.get("files", [])
        if files:
            if not isinstance(files, list):
                incomplete += 1
                problems.append(f"INCOMPLETE manifest={manifest_path}: source.files is not a list")
            else:
                for i, item in enumerate(files):
                    if not isinstance(item, dict):
                        incomplete += 1
                        problems.append(f"INCOMPLETE manifest={manifest_path}: source.files[{i}] is not a mapping")
                        continue
                    pair(item, "path", "blob", source.get("head") or source.get("head_sha"), f"source.files[{i}]")
                    mark(item, "blob")

        def discover_unregistered(node, where):
            nonlocal incomplete, pins
            if isinstance(node, dict):
                for key, value in node.items():
                    key_text = str(key)
                    digest_shaped = (
                        key_text == "blob" or key_text.endswith("_blob") or
                        key_text.endswith("_blob_sha") or key_text.endswith("_blob_sha256") or
                        (key_text.endswith("_sha256") and key_text != "stdout_sha256")
                    )
                    commit_reference = "commit" in key_text.lower() or key_text in {
                        "head_sha", "base_sha", "merge_sha"
                    }
                    scalar_digest = isinstance(value, (str, int)) and not isinstance(value, bool)
                    if (digest_shaped and scalar_digest and not commit_reference
                            and (id(node), key) not in handled):
                        path_keys = [
                            candidate for candidate in node
                            if isinstance(candidate, str) and (
                                candidate in {"path", "file", "prompt_file", "snapshot_file",
                                              "source_path", "translation_path", "frontmatter_path",
                                              "frontmatter_file"}
                                or candidate.endswith("_path") or candidate.endswith("_file")
                            )
                        ]
                        commit_keys = (
                            "source_commit_sha", "translation_commit_sha", "source_commit",
                            "commit", "head_sha", "head", "base_commit", "base_commit_sha",
                            "baseline_commit", "reverification_commit_sha"
                        )
                        source_ref = next((node.get(candidate) for candidate in commit_keys
                                           if nonempty(node.get(candidate))), commit)
                        if len(path_keys) == 1 and nonempty(node.get(path_keys[0])):
                            path_value = node[path_keys[0]]
                            algorithm = ("sha256" if key_text.endswith("_sha256")
                                         and not key_text.endswith("_blob_sha256") else "git")
                            check(path_value, value, source_ref,
                                  f"discovered.{where}.{key_text}", algorithm)
                        else:
                            matching = resolved_locators.get(str(value).lower(), set())
                            if len(matching) == 1 and key_text.endswith("_blob"):
                                matched_commit, matched_path = next(iter(matching))
                                check(matched_path, value, matched_commit,
                                      f"discovered.{where}.{key_text}")
                            else:
                                pins += 1
                                incomplete += 1
                                problems.append(
                                    f"INCOMPLETE UNRESOLVED(unregistered digest field): "
                                    f"manifest={manifest_path} field={where}.{key_text} value={value!r}"
                                )
                        mark(node, key)
                    discover_unregistered(value, f"{where}.{key_text}")
            elif isinstance(node, list):
                for i, value in enumerate(node):
                    discover_unregistered(value, f"{where}[{i}]")
        discover_unregistered(doc, "manifest")

    if verbose:
        print(f"main={commit} manifests={len(manifests)} pins={pins} ok={ok} "
              f"mismatch={mismatch} path_missing={missing} incomplete={incomplete}")
        for problem in problems:
            print(problem)
    return 2 if incomplete else (1 if mismatch or missing else 0)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args(argv)
    try:
        commit = Git(args.root).resolve_commit(args.commit, "--commit")
        return verify(args.root, commit)
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
