---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-255/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local command output recorded verbatim; no CI run asserted."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Verbatim dispatch prompt snapshot for AID-2026-255"
    canonical_scope_id: "ai-development/aid-2026-255-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "sibling-key"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# Delta contribution — sibling-key association tests against the landed checker

Owner A ruled that `AID-2026-255` is not a second implementation. `main` already carries the checker from `AID-2026-268`; the only authorized delta is **sibling-key association tests** in `scripts/ci/test_check_manifest_blob_pins.py`, plus two evidence files the orchestrator handles.

Your earlier tests targeted your own implementation, which is being retired. These must target the **landed** implementation, reproduced below verbatim, and follow its existing test style (black-box subprocess against `--root` / `--commit`, temp git repos, assertions on stdout).

## The landed checker (verbatim, `scripts/ci/check_manifest_blob_pins.py`)

```python

#!/usr/bin/env python3
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

    def object_bytes(self, commit: str, path: str) -> bytes:
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit):
            raise Incomplete(f"invalid or absent source commit for {path}: {commit!r}")
        # Git accepts abbreviated object IDs in historical manifest notes.
        # Resolve once to a full commit; an unavailable/ambiguous prefix is INCOMPLETE.
        try:
            resolved = self.run("rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()
        except Incomplete as exc:
            raise Incomplete(f"source commit unavailable for {path}: {commit}") from exc
        if not HEX40.fullmatch(resolved):
            raise Incomplete(f"source commit did not resolve uniquely for {path}: {commit}")
        spec = f"{resolved}:{path}"
        p = subprocess.run(["git", "cat-file", "blob", spec], cwd=self.root,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
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
    names = git.run("ls-tree", "-r", "--name-only", commit).decode("utf-8").splitlines()
    return sorted(p for p in names
                  if p.startswith(MANIFEST_ROOT + "/") and p.endswith("/manifest.yaml"))


def verify(root: Path, commit: str, verbose: bool = True):
    git = Git(root)
    manifests = discover_manifests(git, commit)
    if not manifests:
        raise Incomplete(f"no manifests found in commit {commit}")
    ok = mismatch = missing = incomplete = pins = 0
    problems = []

    def check(path, declared, source_commit, kind, algorithm="git"):
        nonlocal ok, mismatch, missing, incomplete, pins
        # Empty/null placeholders are not blob identities and are outside this
        # checker's scope. A non-empty malformed declaration is INCOMPLETE.
        if declared is None or (isinstance(declared, str) and not declared.strip()):
            return
        pins += 1
        if algorithm == "bytes":
            if isinstance(declared, bool) or not isinstance(declared, (int, str)) or str(declared).strip() == "":
                incomplete += 1
                problems.append(f"INCOMPLETE {kind}: invalid byte-count declaration {declared!r}")
                return
        elif not isinstance(declared, str) or not declared.strip():
            incomplete += 1
            problems.append(f"INCOMPLETE {kind}: invalid digest declaration {declared!r}")
            return
        if not nonempty(path):
            missing += 1
            problems.append(f"PATH_MISSING {kind} path=<not-declared> declared={declared}")
            return
        try:
            data = git.object_bytes(source_commit, path)
        except Violation as exc:
            missing += 1
            problems.append(f"{exc}; declared={declared}")
            return
        except Incomplete as exc:
            incomplete += 1
            problems.append(f"INCOMPLETE {kind} path={path}: {exc}")
            return
        actual = (hashlib.sha256(data).hexdigest() if algorithm == "sha256"
                  else git_blob_sha(data))
        if algorithm == "bytes":
            try:
                expected_bytes = int(declared)
            except (TypeError, ValueError):
                incomplete += 1
                problems.append(f"INCOMPLETE {kind} path={path}: invalid byte count {declared!r}")
                return
            actual = str(len(data))
            declared = str(expected_bytes)
        if actual != str(declared).lower():
            mismatch += 1
            problems.append(f"MISMATCH {kind} path={path} declared={declared} actual={actual}")
        else:
            ok += 1

    for manifest_path in manifests:
        try:
            raw = git.object_bytes(commit, manifest_path)
            doc = yaml.safe_load(raw.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError, Incomplete, Violation) as exc:
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: {exc}")
            continue
        if not isinstance(doc, dict):
            incomplete += 1
            problems.append(f"INCOMPLETE manifest={manifest_path}: top-level YAML is not a mapping")
            continue

        # A. Root and language mirrors: root/en_mirror/zh_cn_mirror with
        # root_blob/en_mirror_blob/zh_cn_mirror_blob (candidate tree).
        for path_key, digest_key in (
            ("root", "root_blob"),
            ("en_mirror", "en_mirror_blob"),
            ("zh_cn_mirror", "zh_cn_mirror_blob"),
        ):
            if digest_key in doc:
                check(doc.get(path_key), doc.get(digest_key), commit,
                      f"index.{path_key}")

        # B. gate_a_reconstruction[].root -> reconstructed_root_blob.
        # The source commit is explicit on the entry, or in its source note;
        # it is never silently replaced by the candidate commit.
        for i, item in enumerate(doc.get("gate_a_reconstruction", []) or []):
            if not isinstance(item, dict):
                continue
            if "reconstructed_root_blob" in item:
                source = item.get("source_commit") or item.get("commit")
                if not source and nonempty(item.get("note")):
                    match = re.search(r"\bcommit\s+([0-9a-f]{40})\b", item["note"])
                    source = match.group(1) if match else None
                check(item.get("root"), item.get("reconstructed_root_blob"), source,
                      f"gate_a_reconstruction[{i}].root")

        # B2. authored_indexes[] uses the same root and mirror pin shape
        # as the top-level index fields, but is a list in AID-2026-100-style records.
        source_evidence = as_mapping(doc.get("baseline_and_source_evidence"))
        authored_indexes = source_evidence.get("authored_indexes", doc.get("authored_indexes", []))
        for i, item in enumerate(authored_indexes or []):
            if not isinstance(item, dict):
                continue
            for path_key, digest_key in (
                ("root", "root_blob"),
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                if digest_key in item:
                    check(item.get(path_key), item.get(digest_key), commit,
                          f"authored_indexes[{i}].{path_key}")

        # C. related_evidence[].path/blob and language mirrors.
        for i, item in enumerate(doc.get("related_evidence", []) or []):
            if not isinstance(item, dict):
                continue
            for path_key, digest_key in (
                ("path", "blob"),
                ("en_mirror", "en_mirror_blob"),
                ("zh_cn_mirror", "zh_cn_mirror_blob"),
            ):
                if digest_key in item:
                    check(item.get(path_key), item.get(digest_key), commit,
                          f"related_evidence[{i}].{path_key}")

        # D. Execution evidence file/blob pair.
        if "evidence_blob" in doc:
            check(doc.get("evidence_file"), doc.get("evidence_blob"), commit,
                  "evidence_file")

        # E. Cross-commit D source blobs: "<name>: <git-blob-sha>" resolved
        # against d_source_commit, not the candidate tree.
        if "d_source_blobs" in doc:
            source = doc.get("d_source_commit")
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
                    name, digest = entry.rsplit(":", 1)
                    check(name.strip(), digest.strip(), source,
                          f"d_source_blobs[{i}]")

        # F. Prompt snapshots: SHA-256 and byte length are both over committed
        # bytes. These are not Git blob IDs.
        prompt = as_mapping(doc.get("prompt"))
        if "prompt_sha256" in prompt:
            check(prompt.get("prompt_file"), prompt.get("prompt_sha256"), commit,
                  "prompt.prompt_file", "sha256")
        if "prompt_bytes" in prompt:
            check(prompt.get("prompt_file"), prompt.get("prompt_bytes"), commit,
                  "prompt.prompt_file", "bytes")
        for i, item in enumerate(doc.get("session_evidence", []) or []):
            if not isinstance(item, dict):
                continue
            path_key = "executed_prompt_snapshot_file"
            sha_key = "executed_prompt_sha256"
            bytes_key = "executed_prompt_bytes"
            if sha_key in item:
                check(item.get(path_key), item.get(sha_key), commit,
                      f"session_evidence[{i}].{path_key}", "sha256")
            if bytes_key in item:
                check(item.get(path_key), item.get(bytes_key), commit,
                      f"session_evidence[{i}].{path_key}", "bytes")

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
        commit = Git(args.root).run("rev-parse", f"{args.commit}^{{commit}}").decode().strip()
        return verify(args.root, commit)
    except Incomplete as exc:
        print(f"INCOMPLETE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

```

## The landed tests (verbatim, `scripts/ci/test_check_manifest_blob_pins.py`)

```python

#!/usr/bin/env python3
"""Tests for committed-byte manifest blob-pin verification."""
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
GATE = HERE / "check_manifest_blob_pins.py"


def git(root, *args, data=None):
    return subprocess.run(["git", *args], cwd=root, input=data, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout.decode().strip()


def commit_tree(root, files):
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    git(root, "add", ".")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-m", "fixture")
    return git(root, "rev-parse", "HEAD")


class BlobPinsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self, commit="HEAD"):
        p = subprocess.run([sys.executable, str(GATE), "--root", str(self.root),
                            "--commit", commit], text=True, capture_output=True)
        return p.returncode, p.stdout, p.stderr

    def manifest(self, path, digest):
        return ("work_item_id: AID-2026-900\n"
                f"root: {path}\nroot_blob: \"{digest}\"\n")

    @staticmethod
    def blob_sha(data):
        return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

    def test_valid_pin_is_silent_about_individual_pin(self):
        data = b"committed bytes\n"
        sha = self.blob_sha(data)
        commit = commit_tree(self.root, {
            "README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("README.md", sha),
        })
        code, out, err = self.run_gate(commit)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)
        self.assertNotIn("MISMATCH", out)

    def test_nested_authored_index_mirror_pin_is_checked(self):
        data = b"authored mirror bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "docs/en/05-memory-runtime/README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\n"
                 "  authored_indexes:\n"
                 "    - en_mirror: docs/en/05-memory-runtime/README.md\n"
                 f"      en_mirror_blob: \"{wrong}\"\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH authored_indexes[0].en_mirror", out)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)

    def test_changed_byte_is_rejected_with_declared_and_actual_digest(self):
        data = b"committed bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("README.md", wrong),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)
        print(out.strip())

    def test_deleted_path_is_rejected_and_named(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("missing.md", "1" * 40),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn("path=missing.md", out)
        print(out.strip())

    def test_cross_commit_pin_reads_the_declared_source_commit(self):
        source_data = b"source revision\n"
        source = commit_tree(self.root, {"source.md": source_data})
        source_sha = self.blob_sha(source_data)
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("d_source_commit: " + source + "\n"
                 "d_source_blobs:\n"
                 f"  - 'source.md: {source_sha}'\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unavailable_cross_commit_is_incomplete_not_pass(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("d_source_commit: " + "f" * 40 + "\n"
                 "d_source_blobs:\n  - 'source.md: " + "1" * 40 + "'\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("INCOMPLETE", out)
        print(out.strip())

    def test_prompt_sha256_and_byte_count_are_both_checked(self):
        data = b"prompt\n"
        commit_tree(self.root, {
            "prompt.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("prompt:\n  prompt_file: prompt.md\n"
                 f"  prompt_sha256: {hashlib.sha256(data).hexdigest()}\n"
                 f"  prompt_bytes: {len(data)}\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2 mismatch=0", out)

    def test_empty_tree_is_incomplete(self):
        code, out, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)

```

## What to add

Append new test methods to the existing class, keeping all eight existing tests byte-identical. Each new test must be a **mutation test**: it must fail if the resolver associated a digest with the wrong sibling path key. Four cases:

1. **Neighbouring digest key.** A fixture where two sibling pairs exist and the digest of pair A's file is placed under pair B's digest key, while pair A's own key holds a wrong digest. A resolver that read the neighbouring key would report pair B as clean; the correct resolver must report **A as mismatched** and **B as mismatched** (B is now wrong for its own file). Assert on the exact stdout tokens the checker emits, and state in the docstring which wrong implementation the case kills. If the checker's output cannot distinguish these two, say so instead of writing a test that passes either way.
2. **Path-key identity.** `en_mirror` points at file X, `en_mirror_blob` holds the blob id of file Y. Must FAIL and name the `en_mirror` path X, not Y.
3. **Cross-identity isolation.** Two pins, one correct and one wrong: the summary counters must read exactly one mismatch, and the failing token must be the wrong one. This proves the resolver does not share state or carry a "last seen" digest between identities.
4. **Field coverage.** For each path/digest sibling pair the checker actually supports (read the code: `root`/`root_blob`, `en_mirror`/`en_mirror_blob`, `zh_cn_mirror`/`zh_cn_mirror_blob`, `path`/`blob`, `evidence_file`/`evidence_blob`, and whatever else it enumerates), one minimal fixture that must be validated. If a pair is documented but not enumerated, that is a finding: report it in your closing paragraph instead of writing a test that pretends it works.

Do not modify the checker, the baseline, the workflow, or any manifest. If a case requires a checker change, do not write it — report it.

## Return

```
<<<FILE scripts/ci/test_check_manifest_blob_pins.py>>>
...
<<<END FILE>>>
```

plus one line per new test naming the mutation it catches, and one paragraph listing any pair the checker documents but does not enumerate.

