#!/usr/bin/env python3
"""Offline regression and mutation tests for the protection ratchet."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from check_protection_fingerprint import (
    classify_field,
    compare_fingerprints,
    extract_fingerprint,
    main,
)


CONTEXTS = [
    "GOV-DOC-001 structural checks",
    "Branch freshness vs base",
    "audit",
    "GOV-DOC-002 metadata checks",
    "BMCP protocol index (hard gate)",
    "BMCP conformance suite (hard gate)",
    "Schema non-empty audit (hard gate)",
    "Bilingual docs coverage (ratchet)",
    "Rust clippy (hard gate)",
    "Repository hygiene (hard gate)",
    "Rust format (hard gate)",
    "Rust doctests (hard gate)",
    "Session Evidence",
    "Session Evidence self-test (base)",
    "Session Evidence self-test (head)",
    "rust-workspace-test",
]


def fake_payload(
    *,
    enabled=True,
    contexts=None,
    enforcement_level="everyone",
):
    if contexts is None:
        contexts = list(CONTEXTS)

    return {
        "name": "main",
        "protection": {
            "enabled": enabled,
            "required_status_checks": {
                "enforcement_level": enforcement_level,
                "contexts": list(contexts),
                "checks": [
                    {
                        "context": item,
                        "app_id": 15368,
                    }
                    for item in contexts
                ],
            },
        },
    }


def fingerprint(**kwargs):
    return extract_fingerprint(fake_payload(**kwargs))


class ProtectionFingerprintTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "fingerprint.json"

        self.recorded = fingerprint()

        self.write_baseline(self.recorded)

    def tearDown(self):
        self.temp.cleanup()

    def write_baseline(self, protection):
        self.path.write_text(
            json.dumps({
                "schema_version": 2,
                "repository": "oahcom/AiMemoryBrainArchitecture",
                "branch": "main",
                "protection": protection,
                "experiment": {
                    "pr": 1038,
                    "head": (
                        "b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9"
                    ),
                    "run": 138943464904,
                    "date": "2026-11-25",
                    "result": (
                        "HTTP 405: Required status check "
                        "rust-workspace-test is failing"
                    ),
                },
            }),
            encoding="utf-8",
        )

    def run_checker(self, payload, extra=None):
        args = [
            "--repo",
            "oahcom/AiMemoryBrainArchitecture",
            "--branch",
            "main",
            "--fingerprint",
            str(self.path),
        ]

        if extra:
            args.extend(extra)

        return main(
            args,
            payload_fetcher=lambda repo, branch: payload,
        )

    def test_no_changes_pass(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(fake_payload())

        self.assertEqual(result, 0)
        self.assertIn(
            "PROTECTION FINGERPRINT: PASS",
            output.getvalue(),
        )

    def test_contexts_removed_is_loosened_violation(self):
        live = fingerprint(contexts=CONTEXTS[:-1])

        self.assertEqual(
            classify_field(
                "contexts",
                self.recorded["contexts"],
                live["contexts"],
            ),
            "LOOSENED",
        )

        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(
                fake_payload(contexts=CONTEXTS[:-1])
            )

        self.assertEqual(result, 1)
        self.assertIn("DIRECTION=LOOSENED", output.getvalue())

    def test_contexts_added_is_tightened(self):
        contexts = CONTEXTS + ["New required context"]

        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(
                fake_payload(contexts=contexts)
            )

        self.assertEqual(result, 0)
        self.assertIn("DIRECTION=TIGHTENED", output.getvalue())
        self.assertIn(
            "synchronize the committed fingerprint",
            output.getvalue(),
        )

    def test_context_replacement_is_loosened(self):
        contexts = CONTEXTS[:-1] + ["Replacement context"]

        live = fingerprint(contexts=contexts)

        self.assertEqual(
            classify_field(
                "contexts",
                self.recorded["contexts"],
                live["contexts"],
            ),
            "LOOSENED",
        )

    def test_enforcement_everyone_to_non_admins_is_violation(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(
                fake_payload(enforcement_level="non_admins")
            )

        self.assertEqual(result, 1)
        self.assertIn("DIRECTION=LOOSENED", output.getvalue())

    def test_enforcement_everyone_to_off_is_violation(self):
        self.assertEqual(
            self.run_checker(
                fake_payload(enforcement_level="off")
            ),
            1,
        )

    def test_enforcement_off_to_everyone_is_tightened(self):
        baseline = fingerprint(enforcement_level="off")
        self.write_baseline(baseline)

        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(fake_payload())

        self.assertEqual(result, 0)
        self.assertIn("DIRECTION=TIGHTENED", output.getvalue())

    def test_protection_enabled_true_to_false_is_violation(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(
                fake_payload(enabled=False)
            )

        self.assertEqual(result, 1)
        self.assertIn("DIRECTION=LOOSENED", output.getvalue())

    def test_protection_enabled_false_to_true_is_tightened(self):
        baseline = fingerprint(enabled=False)
        self.write_baseline(baseline)

        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self.run_checker(fake_payload())

        self.assertEqual(result, 0)
        self.assertIn("DIRECTION=TIGHTENED", output.getvalue())

    def test_unreadable_payload_is_exit_two(self):
        output = io.StringIO()
        errors = io.StringIO()

        with (
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(errors),
        ):
            result = self.run_checker({})

        self.assertEqual(result, 2)
        self.assertIn("INCOMPLETE:", errors.getvalue())

    def test_missing_protection_enabled_is_exit_two(self):
        payload = fake_payload()
        del payload["protection"]["enabled"]

        self.assertEqual(
            self.run_checker(payload),
            2,
        )

    def test_missing_enforcement_level_is_exit_two(self):
        payload = fake_payload()
        del payload["protection"]["required_status_checks"][
            "enforcement_level"
        ]

        self.assertEqual(
            self.run_checker(payload),
            2,
        )

    def test_unknown_enforcement_level_is_exit_two(self):
        self.assertEqual(
            self.run_checker(
                fake_payload(enforcement_level="unknown")
            ),
            2,
        )

    def test_duplicate_contexts_are_exit_two(self):
        contexts = CONTEXTS + [CONTEXTS[0]]

        self.assertEqual(
            self.run_checker(
                fake_payload(contexts=contexts)
            ),
            2,
        )

    def test_write_missing_experiment_parameters_exit_two(self):
        result = main(
            [
                "--repo",
                "oahcom/AiMemoryBrainArchitecture",
                "--fingerprint",
                str(self.path),
                "--write",
            ],
            payload_fetcher=lambda repo, branch: fake_payload(),
        )

        self.assertEqual(result, 2)

    def test_write_requires_full_sha(self):
        result = main(
            [
                "--repo",
                "oahcom/AiMemoryBrainArchitecture",
                "--fingerprint",
                str(self.path),
                "--write",
                "--experiment-pr",
                "1038",
                "--experiment-head",
                "b5cf4f25",
                "--experiment-run",
                "138943464904",
                "--experiment-date",
                "2026-11-25",
            ],
            payload_fetcher=lambda repo, branch: fake_payload(),
        )

        self.assertEqual(result, 2)

    def test_write_updates_snapshot_and_experiment_atomically(self):
        result = main(
            [
                "--repo",
                "oahcom/AiMemoryBrainArchitecture",
                "--branch",
                "main",
                "--fingerprint",
                str(self.path),
                "--write",
                "--experiment-pr",
                "1038",
                "--experiment-head",
                (
                    "b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9"
                ),
                "--experiment-run",
                "138943464904",
                "--experiment-date",
                "2026-11-25",
            ],
            payload_fetcher=lambda repo, branch: fake_payload(),
        )

        self.assertEqual(result, 0)

        updated = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        self.assertEqual(updated["schema_version"], 2)
        self.assertEqual(updated["protection"], self.recorded)
        self.assertEqual(updated["experiment"]["pr"], 1038)

    def test_baseline_wrong_repository_is_exit_two(self):
        data = json.loads(
            self.path.read_text(encoding="utf-8")
        )
        data["repository"] = "wrong/repository"

        self.path.write_text(json.dumps(data), encoding="utf-8")

        self.assertEqual(
            self.run_checker(fake_payload()),
            2,
        )

    def test_removed_loosened_classification_is_detected(self):
        """Mutation guard: removing LOOSENED must break this test."""

        original = classify_field(
            "contexts",
            self.recorded["contexts"],
            CONTEXTS[:-1],
        )

        self.assertEqual(original, "LOOSENED")

        differences = compare_fingerprints(
            self.recorded,
            fingerprint(contexts=CONTEXTS[:-1]),
        )

        self.assertEqual(differences[0][3], "LOOSENED")

        self.assertEqual(
            self.run_checker(
                fake_payload(contexts=CONTEXTS[:-1])
            ),
            1,
        )

    def test_unreadable_payload_cannot_become_pass(self):
        """Mutation guard: changing unreadable input to exit 0 breaks this test."""

        result = self.run_checker({
            "protection": {
                "enabled": True,
                "required_status_checks": {
                    "contexts": CONTEXTS
                    # enforcement_level deliberately missing
                },
            },
        })

        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
