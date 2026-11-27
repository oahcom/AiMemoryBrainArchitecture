#!/usr/bin/env python3
"""Regression tests for the closed AID-2026-255 authorization set."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

CHECKER = Path(__file__).resolve().with_name("check_manifest_blob_pins.py")
sys.path.insert(0, str(CHECKER.parent))
import check_manifest_blob_pins as checker  # noqa: E402


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc.stdout.strip()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


class Fixture:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "user.name", "AID-2026-255 Tests")

        self.references = []
        self.documents = {
            "100": {
                "baseline_and_source_evidence": {
                    "authored_indexes": [{}, {}],
                },
                "related_evidence": [{}],
            },
            "150": {
                "source": {
                    "files": [{}, {}, {}],
                },
            },
        }

        for index, (manifest, field_path, path_key) in enumerate(
            checker.AUTHORIZED_PINS
        ):
            data = f"authorized-reference-{index}\n".encode("utf-8")
            referenced_path = f"fixture/authorized-{index}.md"
            self.write(referenced_path, data)

            identity = (manifest, field_path)
            self.references.append(
                {
                    "identity": identity,
                    "path": referenced_path,
                    "path_key": path_key,
                    "data": data,
                    "declared": blob_id(data),
                }
            )

            document = self.documents[
                "100" if "AID-2026-100" in manifest else "150"
            ]
            parent, digest_key = checker.locate_parent(document, field_path)
            parent[path_key] = referenced_path
            parent[digest_key] = blob_id(data)

        self.manifest_paths = {
            "100": (
                self.root
                / "14-ai-development/work-items/AID-2026-100/manifest.yaml"
            ),
            "150": (
                self.root
                / "14-ai-development/work-items/AID-2026-150/manifest.yaml"
            ),
        }

    def write(self, path: str, data: bytes):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def write_manifests(self):
        for key, document in self.documents.items():
            path = self.manifest_paths[key]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                yaml.safe_dump(document, sort_keys=False),
                encoding="utf-8",
            )

    def commit(self):
        self.write_manifests()
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "Create isolated blob-pin fixture")

    def run(self):
        return subprocess.run(
            [sys.executable, str(CHECKER), str(self.root)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def close(self):
        self.temp.cleanup()


class ClosedAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()

    def tearDown(self):
        self.fx.close()

    def test_authorization_table_contains_exactly_twelve_identities(self):
        self.assertEqual(len(checker.AUTHORIZED_PINS), 12)
        self.assertEqual(len(set(checker.AUTHORIZED_PINS)), 12)

        expected = {
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "baseline_and_source_evidence.authored_indexes[0].root_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "baseline_and_source_evidence.authored_indexes[0].en_mirror_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "baseline_and_source_evidence.authored_indexes[0].zh_cn_mirror_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "baseline_and_source_evidence.authored_indexes[1].root_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "baseline_and_source_evidence.authored_indexes[1].en_mirror_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "baseline_and_source_evidence.authored_indexes[1].zh_cn_mirror_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "related_evidence[0].blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "related_evidence[0].en_mirror_blob"),
            ("14-ai-development/work-items/AID-2026-100/manifest.yaml",
             "related_evidence[0].zh_cn_mirror_blob"),
            ("14-ai-development/work-items/AID-2026-150/manifest.yaml",
             "source.files[0].blob"),
            ("14-ai-development/work-items/AID-2026-150/manifest.yaml",
             "source.files[1].blob"),
            ("14-ai-development/work-items/AID-2026-150/manifest.yaml",
             "source.files[2].blob"),
        }

        actual = {
            (manifest, field_path)
            for manifest, field_path, _ in checker.AUTHORIZED_PINS
        }
        self.assertEqual(actual, expected)

    def test_main_equivalent_fixture_produces_exactly_twelve_items(self):
        for reference in self.fx.references:
            parent, digest_key = checker.locate_parent(
                self.fx.documents[
                    "100" if "AID-2026-100" in reference["identity"][0]
                    else "150"
                ],
                reference["identity"][1],
            )
            parent[digest_key] = "0" * 40

        self.fx.commit()
        proc = self.fx.run()

        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        lines = [
            line for line in proc.stdout.splitlines()
            if line.startswith("::error::")
        ]
        self.assertEqual(len(lines), 12, proc.stdout)

        actual_identities = {
            line.split(" -> ", 1)[0]
            for line in lines
        }
        expected_identities = {
            f"::error::{manifest}#{field_path}"
            for manifest, field_path, _ in checker.AUTHORIZED_PINS
        }
        self.assertEqual(actual_identities, expected_identities)

    def test_all_twelve_authorized_pins_are_individually_verified(self):
        self.fx.commit()
        proc = self.fx.run()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("All 12 authorized manifest blob pins verified.", proc.stdout)
        self.assertNotIn("::error::", proc.stdout)

    def test_out_of_scope_prompt_hash_and_scope_path_are_ignored(self):
        self.fx.documents["100"]["prompt"] = {
            "prompt_file": "fixture/nonexistent-prompt.md",
            "prompt_sha256": "f" * 64,
        }
        self.fx.documents["100"]["scope"] = {
            "changes": [
                {"path": "fixture/nonexistent-change.md"},
                {"path": "fixture/another-nonexistent-change.md"},
            ],
        }
        self.fx.commit()

        proc = self.fx.run()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("All 12 authorized manifest blob pins verified.", proc.stdout)
        self.assertNotIn("prompt_sha256", proc.stdout)
        self.assertNotIn("scope.changes", proc.stdout)
        self.assertNotIn("::error::", proc.stdout)

    def test_out_of_scope_digest_mismatch_does_not_change_result(self):
        self.fx.documents["100"]["prompt"] = {
            "prompt_file": "fixture/nonexistent.md",
            "prompt_sha256": "0" * 64,
        }
        self.fx.documents["100"]["unrelated"] = {
            "path": "fixture/nonexistent.md",
            "blob": "0" * 40,
        }
        self.fx.commit()

        proc = self.fx.run()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(
            proc.stdout.count("::error::"),
            0,
        )

    def test_one_byte_mutation_inside_authorized_pin_is_caught(self):
        reference = self.fx.references[0]
        mutated = reference["data"][:-1] + b"X"
        self.fx.write(reference["path"], mutated)
        self.fx.commit()

        proc = self.fx.run()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)

        expected_identity = (
            f"::error::{reference['identity'][0]}#"
            f"{reference['identity'][1]}"
        )
        matching = [
            line for line in proc.stdout.splitlines()
            if line.startswith(expected_identity + " -> ")
        ]

        self.assertEqual(len(matching), 1, proc.stdout)
        self.assertIn(f"declared={reference['declared']}", matching[0])
        self.assertIn(f"actual={blob_id(mutated)}", matching[0])

        # The other eleven identities remain independently represented.
        self.assertEqual(proc.stdout.count("::error::"), 1)

    def test_deleted_authorized_path_is_caught_as_missing(self):
        reference = self.fx.references[0]
        self.fx.write_manifests()
        (self.fx.root / reference["path"]).unlink()
        git(self.fx.root, "add", "-A")
        git(self.fx.root, "commit", "-qm", "Delete authorized reference")

        proc = self.fx.run()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("actual=MISSING", proc.stdout)
        self.assertIn(reference["path"], proc.stdout)
        self.assertIn(reference["identity"][1], proc.stdout)

    def test_missing_required_manifest_exits_two(self):
        self.fx.write_manifests()
        self.manifest_path = self.fx.manifest_paths["150"]
        self.manifest_path.unlink()
        git(self.fx.root, "add", "-A")
        git(self.fx.root, "commit", "-qm", "Remove required manifest")

        proc = self.fx.run()
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("nothing was verified", proc.stdout.lower())
        self.assertIn("::error::", proc.stdout)

    def test_missing_repository_path_does_not_affect_other_pins(self):
        reference = self.fx.references[0]
        self.fx.write_manifests()
        (self.fx.root / reference["path"]).unlink()
        git(self.fx.root, "add", "-A")
        git(self.fx.root, "commit", "-qm", "Remove one reference")

        proc = self.fx.run()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout.count("::error::"), 1)
        self.assertIn("actual=MISSING", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
