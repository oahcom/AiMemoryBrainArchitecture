#!/usr/bin/env python3
"""Offline behavioral tests for check_required_context_execution."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import check_required_context_execution as checker


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


def make_run(
    name,
    status="completed",
    conclusion="success",
    started_at="2026-11-27T10:00:00Z",
    run_id=1,
):
    return {
        "name": name,
        "status": status,
        "conclusion": conclusion,
        "started_at": started_at,
        "id": run_id,
    }


class RequiredContextExecutionTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        doc = self.root / checker.DOC_PATH
        doc.parent.mkdir(parents=True)
        doc.write_text(
            "<!-- declared-check-contexts: test -->\n"
            "```text\n"
            + "\n".join(CONTEXTS)
            + "\n```\n",
            encoding="utf-8",
        )

        self.pr = {
            "head": {"sha": "a" * 40},
            "mergeable_state": "clean",
            "draft": False,
        }

        self.runs = [
            make_run(name, run_id=i + 1)
            for i, name in enumerate(CONTEXTS)
        ]

        self.calls = []
        self.sleep = Mock()

        def api_get(path, token):
            self.calls.append(path)

            if "/pulls/" in path:
                return dict(self.pr)

            if "/check-runs?" in path:
                return {"check_runs": list(self.runs)}

            raise AssertionError(f"Unexpected API path: {path}")

        self.api_get = api_get

    def tearDown(self):
        self.tempdir.cleanup()

    def evaluate(self, **kwargs):
        options = {
            "pr": 1469,
            "repo": "oahcom/AiMemoryBrainArchitecture",
            "token": "test-token",
            "root": self.root,
            "api_get": self.api_get,
            "sleep": self.sleep,
            "retries": 5,
            "retry_delay": 0,
        }
        options.update(kwargs)
        return checker.evaluate(**options)

    def test_all_green_is_executed(self):
        result = self.evaluate()

        self.assertEqual(result["verdict"], "EXECUTED")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 0)
        self.assertEqual(len(result["checks"]), 16)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["failed"], [])
        self.assertEqual(result["pending"], [])

    def test_one_missing_context_is_absent(self):
        missing_context = CONTEXTS[5]
        self.runs = [
            run for run in self.runs
            if run["name"] != missing_context
        ]

        result = self.evaluate()

        self.assertEqual(result["verdict"], "ABSENT")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 1)
        self.assertEqual(result["missing"], [missing_context])

    def test_dirty_head_is_stale_even_if_all_runs_are_green(self):
        self.pr["mergeable_state"] = "dirty"

        result = self.evaluate()

        self.assertEqual(result["verdict"], "STALE")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 1)
        self.assertEqual(result["stale"], CONTEXTS)
        self.assertEqual(result["missing"], [])
        self.assertNotIn(
            "check-runs?",
            "\n".join(self.calls),
        )

    def test_unknown_after_retries_is_incomplete(self):
        self.pr["mergeable_state"] = "unknown"

        result = self.evaluate()

        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 2)
        self.assertEqual(result["retries_used"], 5)
        self.assertEqual(len(self.calls), 6)
        self.assertEqual(self.sleep.call_count, 5)
        self.assertEqual(result["mergeable_state"], "unknown")

    def test_latest_run_is_selected_by_started_at_not_list_order(self):
        name = CONTEXTS[0]

        old_failure = make_run(
            name,
            conclusion="failure",
            started_at="2026-11-27T09:00:00Z",
            run_id=100,
        )
        new_success = make_run(
            name,
            conclusion="success",
            started_at="2026-11-27T11:00:00Z",
            run_id=101,
        )

        # Deliberately put the old run last.
        self.runs.extend([new_success, old_failure])

        result = self.evaluate()

        self.assertEqual(result["verdict"], "EXECUTED")
        selected = next(
            item for item in result["checks"]
            if item["name"] == name
        )
        self.assertEqual(selected["run_id"], 101)
        self.assertEqual(selected["conclusion"], "success")

    def test_api_exception_is_incomplete_not_absent(self):
        def failing_api(path, token):
            raise OSError("simulated network failure")

        result = self.evaluate(api_get=failing_api)

        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 2)
        self.assertEqual(result["missing"], [])
        self.assertIn("simulated network failure", result["error"])

    def test_in_progress_run_is_incomplete(self):
        name = CONTEXTS[3]
        self.runs = [
            (
                make_run(
                    run["name"],
                    status="in_progress",
                    conclusion=None,
                    started_at=run["started_at"],
                    run_id=run["id"],
                )
                if run["name"] == name
                else run
            )
            for run in self.runs
        ]

        result = self.evaluate()

        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(result["pending"], [name])
        self.assertEqual(result["missing"], [])

    def test_completed_failure_is_failed_not_absent(self):
        name = CONTEXTS[7]
        self.runs = [
            (
                make_run(
                    run["name"],
                    conclusion="failure",
                    started_at=run["started_at"],
                    run_id=run["id"],
                )
                if run["name"] == name
                else run
            )
            for run in self.runs
        ]

        result = self.evaluate()

        self.assertEqual(result["verdict"], "FAILED")
        self.assertEqual(result["failed"], [name])
        self.assertEqual(result["missing"], [])
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 1)

    def test_missing_token_is_incomplete_without_api_call(self):
        result = self.evaluate(token=None)

        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 2)
        self.assertEqual(self.calls, [])

    def test_declaration_parse_failure_is_incomplete(self):
        doc = self.root / checker.DOC_PATH
        doc.write_text("no declaration here\n", encoding="utf-8")

        result = self.evaluate()

        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(checker.EXIT_CODES[result["verdict"]], 2)
        self.assertEqual(self.calls, [])

    def test_head_change_during_unknown_retry_is_incomplete(self):
        responses = [
            {
                "head": {"sha": "a" * 40},
                "mergeable_state": "unknown",
            },
            {
                "head": {"sha": "b" * 40},
                "mergeable_state": "clean",
            },
        ]

        def changing_api(path, token):
            return responses.pop(0)

        result = self.evaluate(api_get=changing_api)

        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertIn("head changed", result["error"])


if __name__ == "__main__":
    unittest.main()
