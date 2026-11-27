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
    ("d_source_blobs[]", "inline <path>: <sha>; unique basename search in source commit when path is basename-only", "d_source_commit", "Git blob SHA-1"),
    ("baseline_and_source_evidence.d_source_blobs[]", "same as d_source_blobs[]", "baseline_and_source_evidence.d_source_commit", "Git blob SHA-1"),
    ("prompt_file_blob_sha", "prompt_file", "prompt_file_commit_sha", "Git blob SHA-1"),
    ("execution_boundary_extension.owner_contracts.sha256_or_blob_sha", "path", "commit_before_manifest_update", "Git blob SHA-1"),
    ("added_conformance_cases.blob_sha", "test_matrix_path", "test_matrix_commit_before_manifest_update", "Git blob SHA-1"),
    ("joined_contract_updated.blob_sha", "path", "commit_before_manifest_update", "Git blob SHA-1"),
    ("reference_model_validation.*.git_blob_sha", "sibling file", "candidate commit", "Git blob SHA-1"),
    ("dev_baseline_integration.model_blob/tests_blob", "reference-model/r3_contract_model.py / test_r3_contract.py", "target_commit", "Git blob SHA-1"),
    ("mainline_integration.forget_model_blob/forget_tests_blob", "reference-model/forget_model.py / test_forget_model.py", "merged_main_head", "Git blob SHA-1"),
    ("mainline_integration.reference_model_readme_blob_before_append", "reference-model/README.md", "pre_update_branch_head", "Git blob SHA-1"),
    ("measurement_basis.model_blob_sha256_lf/tests_blob_sha256_lf", "model/test file", "mainline integration commit", "SHA-256(bytes)"),
    ("measurement_basis.model_blob_bytes_lf/tests_blob_bytes_lf", "model/test file", "mainline integration commit", "byte length"),
    ("current_main_blobs.*", "per-field path mapping required; otherwise UNRESOLVED", "observed_main_head", "Git blob SHA-1"),
    ("source_baseline.*_blob / source_pins.*_blob / *_source_blob", "no path in declaration", "no declared locator", "UNRESOLVED; never treated as PASS"),
    ("owner_ruling.current_blob/superseded_blob", "current_artifact/superseded_artifact", "candidate commit", "Git blob SHA-1"),
    ("reconciliation.pointers_changed[].before_blob/after_blob", "owner_ruling.superseded_artifact/current_artifact", "candidate commit", "Git blob SHA-1"),
    ("renumbering.previous_prompt_sha256", "previous_prompt_file", "candidate commit", "SHA-256(bytes); unresolved if absent"),
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
    ("source.selected_source_files[].frontmatter_blob_sha", "frontmatter_path/frontmatter_file or unique blob-OID path in source tree", "source.head_sha", "Git blob SHA-1; UNRESOLVED if no unique locator"),
    ("source.files[].blob", "source.files[].path", "source.head", "Git blob SHA-1"),
    ("source.source_blob_sha", "source_path", "branch_head", "Git blob SHA-1"),
    ("prompt_file_blob_sha", "prompt_file", "prompt_file_commit_sha", "Git blob SHA-1"),
    ("execution_boundary_extension.owner_contracts.sha256_or_blob_sha", "path", "commit_before_manifest_update", "Git blob SHA-1"),
    ("added_conformance_cases.blob_sha", "test_matrix_path", "test_matrix_commit_before_manifest_update", "Git blob SHA-1"),
    ("joined_contract_updated.blob_sha", "path", "commit_before_manifest_update", "Git blob SHA-1"),
    ("reference_model_validation.*.git_blob_sha", "sibling file", "candidate commit", "Git blob SHA-1"),
    ("current_main_blobs.*", "explicit per-key path or unique workflow blob-OID path", "observed_main_head", "Git blob SHA-1"),
    ("dev_baseline_integration.model_blob/tests_blob", "r3_contract_model.py/test_r3_contract.py", "target_commit", "Git blob SHA-1"),
    ("mainline_integration.forget_model_blob/forget_tests_blob", "forget_model.py/test_forget_model.py", "merged_main_head", "Git blob SHA-1"),
    ("mainline_integration.reference_model_readme_blob_before_append", "reference-model/README.md", "pre_update_branch_head", "Git blob SHA-1"),
    ("measurement_basis.*_blob_sha256_lf/*_blob_bytes_lf", "model/test source file", "merged_main_head", "SHA-256(bytes)/byte length"),
    ("owner_ruling.current_blob/superseded_blob", "current_artifact/superseded_artifact", "candidate commit", "Git blob SHA-1"),
    ("reconciliation.pointers_changed[].before_blob/after_blob", "owner_ruling.superseded_artifact/current_artifact", "candidate commit", "Git blob SHA-1"),
    ("renumbering.current_prompt_sha256", "renumbering.current_prompt_file or top-level prompt_file", "candidate commit", "SHA-256(bytes)"),
    ("renumbering.previous_prompt_sha256", "previous_prompt_file (absent in AID-2026-241)", "candidate commit", "UNRESOLVED without locator"),
    ("source_baseline.*_blob/source_pins.*_blob/latest_*_source_blob", "no declared path", "no declared locator", "UNRESOLVED; not PASS"),
    ("prompt_original_payload_sha256/instruction_sha256", "no declared committed file", "no declared locator", "UNRESOLVED; not PASS"),
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

    def paths_by_basename(self, commit: str, basename: str, field: str):
        resolved = self.resolve_commit(commit, field)
        names = self.run("ls-tree", "-r", "--name-only", resolved).decode("utf-8").splitlines()
        return [name for name in names if PurePosixPath(name).name == basename]

    def paths_by_blob_oid(self, commit: str, blob_oid: str, field: str):
        resolved = self.resolve_commit(commit, field)
        lines = self.run("ls-tree", "-r", resolved).decode("utf-8").splitlines()
        matches = []
        for line in lines:
            try:
                metadata, path = line.split("\t", 1)
                mode, object_type, oid = metadata.split()
            except ValueError:
                continue
            if object_type == "blob" and oid == blob_oid:
                matches.append(path)
        return matches

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

    def check_blob_oid(source_commits, declared, kind):
        nonlocal pins, incomplete
        if isinstance(source_commits, str):
            source_commits = [source_commits]
        if not isinstance(declared, str) or not HEX40.fullmatch(declared):
            pins += 1
            incomplete += 1
            problems.append(f"INCOMPLETE {kind}: invalid Git blob SHA-1 declaration {declared!r}")
            return
        for source_commit in source_commits:
            if not nonempty(source_commit):
                continue
            try:
                matches = git.paths_by_blob_oid(source_commit, declared, kind)
            except Incomplete:
                continue
            if len(matches) == 1:
                check(matches[0], declared, source_commit, kind)
                return
            if len(matches) > 1:
                pins += 1
                incomplete += 1
                problems.append(
                    f"INCOMPLETE UNRESOLVED({kind} blob locator ambiguous): "
                    f"commit={source_commit} blob={declared} paths={matches!r}"
                )
                return
        pins += 1
        incomplete += 1
        problems.append(
            f"INCOMPLETE UNRESOLVED({kind} blob locator): "
            f"blob={declared} not found in declared commit tree(s)"
        )

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
                source_commit = (item.get("source_commit") or item.get("source_commit_sha")
                                 or item.get("commit") or item.get("commit_sha")
                                 or source_evidence.get("main_reconciliation_head"))
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

        d_source_entries = doc.get("d_source_blobs")
        d_source_commit = doc.get("d_source_commit")
        if d_source_entries is None:
            d_source_entries = source_evidence.get("d_source_blobs")
            d_source_commit = d_source_commit or source_evidence.get("d_source_commit")
        if d_source_entries is not None:
            entries = d_source_entries
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
                    path_value = path.strip()
                    if "/" not in path_value:
                        try:
                            matches = git.paths_by_basename(d_source_commit, path_value, f"d_source_blobs[{i}]")
                        except Incomplete as exc:
                            incomplete += 1
                            pins += 1
                            problems.append(f"INCOMPLETE d_source_blobs[{i}]: {exc}")
                            continue
                        if len(matches) != 1:
                            incomplete += 1
                            pins += 1
                            problems.append(
                                f"INCOMPLETE UNRESOLVED(d_source basename locator): "
                                f"manifest={manifest_path} basename={path_value!r} matches={matches!r}"
                            )
                            continue
                        path_value = matches[0]
                    check(path_value, digest.strip(), d_source_commit, f"d_source_blobs[{i}]")

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
        if "source_blob_sha" in source:
            source_locator_commit = (source.get("branch_head") or source.get("head_sha")
                                     or source.get("head"))
            source_path = source.get("source_path") or source.get("path")
            if nonempty(source_path):
                pair(source, "source_path" if "source_path" in source else "path",
                     "source_blob_sha", source_locator_commit, "source.source_blob_sha")
            elif nonempty(source_locator_commit):
                check_blob_oid(source_locator_commit, source.get("source_blob_sha"), "source.source_blob_sha")
            else:
                pins += 1
                incomplete += 1
                problems.append(
                    f"INCOMPLETE UNRESOLVED(source.source_blob_sha): "
                    f"manifest={manifest_path} no sibling path or commit locator"
                )
            mark(source, "source_blob_sha")
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
                        if nonempty(front_path):
                            locator_key = "frontmatter_path" if "frontmatter_path" in item else "frontmatter_file"
                            pair(item, locator_key, "frontmatter_blob_sha", source_commit or commit,
                                 prefix + ".frontmatter_blob_sha")
                        else:
                            check_blob_oid(source_commit or commit, item.get("frontmatter_blob_sha"),
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

        owner_ruling = as_mapping(doc.get("owner_ruling"))
        if "current_blob" in owner_ruling:
            pair(owner_ruling, "current_artifact", "current_blob", commit, "owner_ruling.current_blob")
            mark(owner_ruling, "current_blob")
        if "superseded_blob" in owner_ruling:
            pair(owner_ruling, "superseded_artifact", "superseded_blob", commit, "owner_ruling.superseded_blob")
            mark(owner_ruling, "superseded_blob")
        reconciliation = as_mapping(doc.get("reconciliation"))
        for i, item in enumerate(reconciliation.get("pointers_changed", []) or []):
            if not isinstance(item, dict):
                continue
            if "before_blob" in item:
                # The document field names the pointer document, not the blob target.
                check(owner_ruling.get("superseded_artifact"), item.get("before_blob"), commit,
                      f"reconciliation.pointers_changed[{i}].before_blob.target")
                mark(item, "before_blob")
            if "after_blob" in item:
                check(owner_ruling.get("current_artifact"), item.get("after_blob"), commit,
                      f"reconciliation.pointers_changed[{i}].after_blob.target")
                mark(item, "after_blob")

        # Historical reference-model pins carry an explicit baseline commit.
        if doc.get("work_item_id") == "AID-2026-001":
            dev = as_mapping(doc.get("dev_baseline_integration"))
            target_commit = dev.get("target_commit")
            ref_validation = as_mapping(doc.get("reference_model_validation"))
            for section_name in ("model", "tests"):
                section = as_mapping(ref_validation.get(section_name))
                if "git_blob_sha" in section:
                    check(section.get("file"), section.get("git_blob_sha"), target_commit,
                          f"reference_model_validation.{section_name}.git_blob_sha")
                    mark(section, "git_blob_sha")
            execution_record = as_mapping(ref_validation.get("execution_record"))
            if "git_blob_sha" in execution_record:
                check_blob_oid(target_commit, execution_record.get("git_blob_sha"),
                               "reference_model_validation.execution_record.git_blob_sha")
                mark(execution_record, "git_blob_sha")
            post_merge = as_mapping(doc.get("post_merge_manifest_validation"))
            observed_head = post_merge.get("observed_main_head") or commit
            current_blobs = as_mapping(doc.get("current_main_blobs"))
            current_paths = {
                "forget_model_py": "14-ai-development/work-items/AID-2026-001/reference-model/forget_model.py",
                "test_forget_model_py": "14-ai-development/work-items/AID-2026-001/reference-model/test_forget_model.py",
                "readme_md": "14-ai-development/work-items/AID-2026-001/reference-model/README.md",
            }
            for key, value in current_blobs.items():
                if key in current_paths:
                    check(current_paths[key], value, observed_head, f"current_main_blobs.{key}")
                elif key == "workflow_yml":
                    try:
                        matches = [p for p in git.paths_by_blob_oid(observed_head, value, f"current_main_blobs.{key}")
                                   if p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml"))]
                    except Incomplete as exc:
                        matches = []
                        problems.append(f"INCOMPLETE current_main_blobs.{key}: {exc}")
                        incomplete += 1
                        pins += 1
                    if len(matches) == 1:
                        check(matches[0], value, observed_head, f"current_main_blobs.{key}")
                    elif not any(f"current_main_blobs.{key}" in p for p in problems):
                        incomplete += 1
                        pins += 1
                        problems.append(
                            f"INCOMPLETE UNRESOLVED(current_main_blobs.{key}): "
                            f"expected one workflow path, found {matches!r}"
                        )
                else:
                    pins += 1
                    incomplete += 1
                    problems.append(f"INCOMPLETE UNRESOLVED(current_main_blobs.{key}): no path mapping")
                mark(current_blobs, key)

            for key, path_value, source_ref in (
                ("model_blob", "14-ai-development/work-items/AID-2026-001/reference-model/r3_contract_model.py",
                 dev.get("target_commit")),
                ("tests_blob", "14-ai-development/work-items/AID-2026-001/reference-model/test_r3_contract.py",
                 as_mapping(dev.get("mainline_integration")).get("pre_update_branch_head")),
            ):
                if key in dev:
                    check(path_value, dev.get(key), source_ref, f"dev_baseline_integration.{key}")
                    mark(dev, key)

            integration = as_mapping(dev.get("mainline_integration"))
            merged_head = integration.get("merged_main_head") or integration.get("merge_commit")
            for key, path_value in (
                ("forget_model_blob", "14-ai-development/work-items/AID-2026-001/reference-model/forget_model.py"),
                ("forget_tests_blob", "14-ai-development/work-items/AID-2026-001/reference-model/test_forget_model.py"),
            ):
                if key in integration:
                    check(path_value, integration.get(key), merged_head,
                          f"mainline_integration.{key}")
                    mark(integration, key)
            readme_before = "reference_model_readme_blob_before_append"
            if readme_before in integration:
                check("14-ai-development/work-items/AID-2026-001/reference-model/README.md",
                      integration.get(readme_before),
                      integration.get("pre_update_branch_head") or merged_head,
                      f"mainline_integration.{readme_before}")
                mark(integration, readme_before)

            measurement = as_mapping(integration.get("measurement_basis"))
            model_path = "14-ai-development/work-items/AID-2026-001/reference-model/r3_contract_model.py"
            tests_path = "14-ai-development/work-items/AID-2026-001/reference-model/test_r3_contract.py"
            measurement_commit = merged_head or commit
            for key, path_value, algorithm in (
                ("model_blob_sha256_lf", model_path, "sha256"),
                ("tests_blob_sha256_lf", tests_path, "sha256"),
                ("model_blob_bytes_lf", model_path, "bytes"),
                ("tests_blob_bytes_lf", tests_path, "bytes"),
            ):
                if key in measurement:
                    check(path_value, measurement.get(key), measurement_commit,
                          f"measurement_basis.{key}", algorithm)
                    mark(measurement, key)
            # CRLF values are measurements of a rendered Windows working copy,
            # not Git tree blobs; retain them as evidence, not blob pins.
            for key in ("model_blob_sha256_crlf", "tests_blob_sha256_crlf"):
                if key in measurement:
                    mark(measurement, key)

        source_baseline = as_mapping(doc.get("source_baseline"))
        if source_baseline:
            baseline_commit = source_baseline.get("main")
            for key, value in source_baseline.items():
                if isinstance(key, str) and (key.endswith("_blob") or key.endswith("_blob_sha")):
                    check_blob_oid(baseline_commit, value, f"source_baseline.{key}")
                    mark(source_baseline, key)

        source_pins = as_mapping(doc.get("source_pins"))
        if source_pins:
            pins_commit = doc.get("latest_sync_main_commit_sha")
            for key, value in source_pins.items():
                if isinstance(key, str) and (key.endswith("_blob") or key.endswith("_blob_sha")):
                    check_blob_oid(pins_commit, value, f"source_pins.{key}")
                    mark(source_pins, key)

        post_merge_validation = as_mapping(as_mapping(doc.get("impl2_scope_adjudication")).get("post_merge_validation"))
        if post_merge_validation:
            post_merge_commit = post_merge_validation.get("merge_commit_sha") or post_merge_validation.get("final_pr_head")
            for key in ("canonical_evidence_blob", "en_evidence_blob", "zh_cn_evidence_blob"):
                if key in post_merge_validation:
                    check_blob_oid(post_merge_commit, post_merge_validation.get(key),
                                   f"impl2_scope_adjudication.post_merge_validation.{key}")
                    mark(post_merge_validation, key)

        # AID-2026-093 records source blob identities but omits their path fields.
        # Resolve only against the explicitly recorded reconciliation commits.
        if doc.get("latest_main_sha") or doc.get("latest_main_merge_sha"):
            candidate_commits = [doc.get("latest_main_sha"), doc.get("latest_main_merge_sha"),
                                 doc.get("post_merge_main_sha")]
            for key in ("latest_invariant_source_blob", "prior_invariant_source_blob",
                        "latest_forget_fence_contract_blob", "latest_system_boundaries_blob",
                        "latest_context_version_blob", "latest_applied_evidence_blob"):
                if key in doc:
                    check_blob_oid(candidate_commits, doc.get(key), key)
                    mark(doc, key)

        renumbering = as_mapping(doc.get("renumbering"))
        if "current_prompt_sha256" in renumbering:
            current_prompt_file = renumbering.get("current_prompt_file") or doc.get("prompt_file")
            check(current_prompt_file, renumbering.get("current_prompt_sha256"), commit,
                  "renumbering.current_prompt_sha256", "sha256")
            mark(renumbering, "current_prompt_sha256")
        if "previous_prompt_sha256" in renumbering:
            previous_prompt_file = renumbering.get("previous_prompt_file")
            if nonempty(previous_prompt_file):
                check(previous_prompt_file, renumbering.get("previous_prompt_sha256"), commit,
                      "renumbering.previous_prompt_sha256", "sha256")
            else:
                pins += 1
                incomplete += 1
                problems.append(
                    f"INCOMPLETE UNRESOLVED(renumbering.previous_prompt_sha256): "
                    f"manifest={manifest_path} no previous_prompt_file locator"
                )
            mark(renumbering, "previous_prompt_sha256")

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
                        if key_text == "prompt_original_payload_sha256" and not nonempty(
                            node.get("prompt_original_payload_file")
                        ):
                            pins += 1
                            incomplete += 1
                            problems.append(
                                f"INCOMPLETE UNRESOLVED(prompt_original_payload_sha256): "
                                f"manifest={manifest_path} no dedicated prompt_original_payload_file locator"
                            )
                            mark(node, key)
                            discover_unregistered(value, f"{where}.{key_text}")
                            continue
                        path_keys = [
                            candidate for candidate in node
                            if isinstance(candidate, str) and (
                                candidate in {"path", "file", "prompt_file", "snapshot_file",
                                              "source_path", "translation_path", "frontmatter_path",
                                              "frontmatter_file", "document", "artifact",
                                              "current_artifact", "superseded_artifact"}
                                or candidate.endswith("_path") or candidate.endswith("_file")
                                or candidate.endswith("_artifact")
                            )
                        ]
                        base_name = key_text
                        for suffix in ("_blob_sha256", "_blob_sha", "_blob", "_sha256"):
                            if base_name.endswith(suffix):
                                base_name = base_name[:-len(suffix)]
                                break
                        preferred_paths = [
                            base_name + "_path", base_name + "_file", base_name + "_artifact"
                        ]
                        if key_text == "current_blob":
                            preferred_paths = ["current_artifact"]
                        elif key_text == "superseded_blob":
                            preferred_paths = ["superseded_artifact"]
                        elif key_text in {"before_blob", "after_blob"}:
                            preferred_paths = ["document"]
                        elif key_text in {"snapshot_git_blob_sha", "snapshot_sha256"}:
                            preferred_paths = ["snapshot_file"]
                        elif key_text == "prompt_file_blob_sha":
                            preferred_paths = ["prompt_file"]
                        elif key_text == "prompt_original_payload_sha256":
                            preferred_paths = ["prompt_original_payload_file", "prompt_file"]
                        elif key_text == "current_prompt_sha256":
                            preferred_paths = ["current_prompt_file", "prompt_file"]
                        elif key_text == "previous_prompt_sha256":
                            preferred_paths = ["previous_prompt_file"]
                        selected_path = next((candidate for candidate in preferred_paths
                                               if candidate in node and nonempty(node.get(candidate))), None)
                        if selected_path is None and base_name in node and nonempty(node.get(base_name)):
                            selected_path = base_name
                        commit_keys = (
                            "source_commit_sha", "translation_commit_sha", "prompt_file_commit_sha",
                            "source_commit", "commit", "head_sha", "head", "base_commit",
                            "base_commit_sha", "baseline_commit", "reverification_commit_sha",
                            "commit_before_manifest_update", "test_matrix_commit_before_manifest_update"
                        )
                        source_ref = next((node.get(candidate) for candidate in commit_keys
                                           if nonempty(node.get(candidate))), None)
                        if source_ref is None:
                            source_ref = next((value for name, value in node.items()
                                               if isinstance(name, str) and
                                               ("_commit_" in name or name.endswith("_commit"))
                                               and nonempty(value)), commit)
                        if isinstance(source_ref, str) and (
                            "NOT_SEPARATELY_COMMITTED" in source_ref or
                            "same commit as registration package" in source_ref
                        ):
                            source_ref = commit
                        if where.startswith("manifest.source_baseline."):
                            source_ref = as_mapping(doc.get("source_baseline")).get("main") or source_ref
                        elif where.startswith("manifest.source_pins."):
                            source_ref = doc.get("latest_sync_main_commit_sha") or source_ref
                        locator_key = selected_path or (path_keys[0] if len(path_keys) == 1 else None)
                        if locator_key and nonempty(node.get(locator_key)):
                            path_value = node[locator_key]
                            if isinstance(path_value, str) and "/" not in path_value and locator_key in {
                                "prompt_file", "snapshot_file", "prompt_original_payload_file", "file"
                            }:
                                path_value = str(PurePosixPath(manifest_path).parent / path_value)
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
    # Per-record INCOMPLETE/UNRESOLVED declarations are ratcheted as failures:
    # they are never counted in ok, but an exact baseline line can be retained
    # without turning the entire scan into an un-ratchetable infrastructure error.
    return 1 if incomplete or mismatch or missing else 0

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
