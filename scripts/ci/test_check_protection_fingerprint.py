import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import check_protection_fingerprint as checker


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
EXPERIMENT = {
    "pr": "#1038",
    "head": "b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9",
    "run": "138943464904",
    "date": "2026-11-25",
}


def payload():
    return {
        "url": "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection",
        "required_status_checks": {
            "strict": True,
            "contexts": list(CONTEXTS),
            "checks": [{"context": name, "app_id": 15368} for name in CONTEXTS],
        },
        "required_signatures": {"enabled": False},
        "enforce_admins": {"enabled": True},
        "required_linear_history": {"enabled": False},
        "allow_force_pushes": {"enabled": False},
        "allow_deletions": {"enabled": False},
        "block_creations": {"enabled": False},
        "required_conversation_resolution": {"enabled": False},
        "lock_branch": {"enabled": False},
        "allow_fork_syncing": {"enabled": False},
    }


def summary_payload():
    return {
        "protection": {
            "enabled": True,
            "required_status_checks": {
                "contexts": list(CONTEXTS),
                "enforcement_level": "everyone",
            },
        }
    }


def fingerprint():
    return checker.extract_fingerprint(payload())


def summary_fingerprint():
    return checker.extract_summary_fingerprint(summary_payload())


def baseline_document():
    return {
        "schema_version": 4,
        "fingerprint": fingerprint(),
        "summary_fingerprint": summary_fingerprint(),
        "experiment": dict(EXPERIMENT),
    }


class ProtectionFingerprintTests(unittest.TestCase):
    def setUp(self):
        self.live_payload = payload()
        self.live = checker.extract_fingerprint(self.live_payload)
        self.recorded = dict(self.live)
        self.live_summary_payload = summary_payload()
        self.live_summary = checker.extract_summary_fingerprint(
            self.live_summary_payload
        )

    def make_baseline(self, path):
        Path(path).write_text(
            json.dumps(baseline_document(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def run_main(
        self, argv, fetcher=None, directory=None, summary_fetcher=None,
        environ=None,
    ):
        output = io.StringIO()
        errors = io.StringIO()
        fetcher = fetcher or (lambda repo, branch, token: self.live_payload)
        summary_fetcher = summary_fetcher or (
            lambda repo, branch, token: self.live_summary_payload
        )
        args = list(argv)
        if directory is not None:
            args += ["--fingerprint", str(Path(directory) / "fingerprint.json")]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = checker.main(
                args,
                payload_fetcher=fetcher,
                summary_payload_fetcher=summary_fetcher,
                environ={"GITHUB_TOKEN": "test-token"} if environ is None else environ,
            )
        return code, output.getvalue(), errors.getvalue()

    def test_no_changes_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fingerprint.json"
            self.make_baseline(path)
            code, out, err = self.run_main(["--fingerprint", str(path)])
        self.assertEqual(code, 0)
        self.assertIn("0 field(s) changed, 0 loosened, 0 tightened", out)
        self.assertEqual(err, "")

    def test_strict_true_to_false_is_loosened(self):
        self.recorded["strict"] = True
        live = dict(self.recorded, strict=False)
        self.assertEqual(
            checker.classify_field("strict", self.recorded["strict"], live["strict"]),
            "LOOSENED",
        )

    def test_enforce_admins_true_to_false_is_loosened(self):
        self.assertEqual(checker.classify_field("enforce_admins", True, False), "LOOSENED")

    def test_allow_force_pushes_false_to_true_is_loosened(self):
        self.assertEqual(checker.classify_field("allow_force_pushes", False, True), "LOOSENED")

    def test_allow_deletions_false_to_true_is_loosened(self):
        self.assertEqual(checker.classify_field("allow_deletions", False, True), "LOOSENED")

    def test_block_creations_true_to_false_is_loosened(self):
        self.assertEqual(checker.classify_field("block_creations", True, False), "LOOSENED")

    def test_required_reviews_present_to_absent_is_loosened(self):
        self.assertEqual(
            checker.classify_field(
                "required_pull_request_reviews",
                {"required_approving_review_count": 1},
                None,
            ),
            "LOOSENED",
        )

    def test_context_removal_is_loosened(self):
        self.assertEqual(checker.classify_contexts(CONTEXTS, CONTEXTS[:-1]), "LOOSENED")

    def test_context_addition_is_tightened(self):
        self.assertEqual(
            checker.classify_contexts(CONTEXTS, CONTEXTS + ["New required check"]),
            "TIGHTENED",
        )

    def test_context_mixed_addition_and_removal_is_loosened(self):
        changed = CONTEXTS[:-1] + ["Replacement required check"]
        self.assertEqual(checker.classify_contexts(CONTEXTS, changed), "LOOSENED")

    def test_required_linear_history_false_to_true_is_tightened(self):
        self.assertEqual(
            checker.classify_field("required_linear_history", False, True), "TIGHTENED"
        )

    def test_required_conversation_resolution_false_to_true_is_tightened(self):
        self.assertEqual(
            checker.classify_field("required_conversation_resolution", False, True),
            "TIGHTENED",
        )

    def test_lock_branch_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("lock_branch", False, True), "TIGHTENED")

    def test_allow_fork_syncing_true_to_false_is_tightened(self):
        self.assertEqual(checker.classify_field("allow_fork_syncing", True, False), "TIGHTENED")

    def test_required_signatures_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("required_signatures", False, True), "TIGHTENED")

    def test_required_reviews_absent_to_present_is_tightened(self):
        self.assertEqual(
            checker.classify_field(
                "required_pull_request_reviews",
                None,
                {"required_approving_review_count": 1},
            ),
            "TIGHTENED",
        )

    def test_approving_review_count_increase_is_tightened(self):
        self.assertEqual(
            checker.classify_reviews(
                {"required_approving_review_count": 1},
                {"required_approving_review_count": 2},
            ),
            "TIGHTENED",
        )

    def test_approving_review_count_decrease_is_loosened(self):
        self.assertEqual(
            checker.classify_reviews(
                {"required_approving_review_count": 2},
                {"required_approving_review_count": 1},
            ),
            "LOOSENED",
        )

    def test_allow_force_pushes_true_to_false_is_tightened(self):
        self.assertEqual(checker.classify_field("allow_force_pushes", True, False), "TIGHTENED")

    def test_allow_deletions_true_to_false_is_tightened(self):
        self.assertEqual(checker.classify_field("allow_deletions", True, False), "TIGHTENED")

    def test_strict_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("strict", False, True), "TIGHTENED")

    def test_enforce_admins_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("enforce_admins", False, True), "TIGHTENED")

    def test_required_linear_history_true_to_false_is_loosened(self):
        self.assertEqual(
            checker.classify_field("required_linear_history", True, False), "LOOSENED"
        )

    def test_block_creations_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("block_creations", False, True), "TIGHTENED")

    def test_required_conversation_resolution_true_to_false_is_loosened(self):
        self.assertEqual(
            checker.classify_field("required_conversation_resolution", True, False),
            "LOOSENED",
        )

    def test_allow_fork_syncing_false_to_true_is_loosened(self):
        self.assertEqual(checker.classify_field("allow_fork_syncing", False, True), "LOOSENED")

    def test_required_signatures_true_to_false_is_loosened(self):
        self.assertEqual(checker.classify_field("required_signatures", True, False), "LOOSENED")

    def test_lock_branch_true_to_false_is_loosened(self):
        self.assertEqual(checker.classify_field("lock_branch", True, False), "LOOSENED")

    def test_tightening_emits_baseline_sync_notice(self):
        recorded = dict(self.live)
        live = dict(self.live)
        live["required_linear_history"] = True
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            checker.compare(recorded, live)
        self.assertIn("TIGHTENED", output.getvalue())
        self.assertIn("synchronize the fingerprint baseline", output.getvalue())

    def test_http_403_is_incomplete_exit_two(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("GitHub protection API HTTP 403: Forbidden", 403)
        code, out, err = self.run_main(
            ["--endpoint", "full", "--fingerprint", "unused.json"],
            fetcher=forbidden,
        )
        self.assertEqual(code, 2)
        self.assertIn("HTTP 403", err)
        self.assertNotIn("PROTECTION FINGERPRINT:", out)

    def test_http_404_is_incomplete_exit_two(self):
        def missing(repo, branch, token):
            raise checker.ApiError("GitHub protection API HTTP 404: Not Found", 404)
        code, out, err = self.run_main(
            ["--endpoint", "full", "--fingerprint", "unused.json"],
            fetcher=missing,
        )
        self.assertEqual(code, 2)
        self.assertIn("HTTP 404", err)
        self.assertNotIn("PROTECTION FINGERPRINT:", out)

    def test_missing_live_field_is_incomplete_exit_two(self):
        broken = payload()
        del broken["lock_branch"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fingerprint.json"
            self.make_baseline(path)
            code, out, err = self.run_main(
                ["--fingerprint", str(path)],
                fetcher=lambda repo, branch, token: broken,
            )
        self.assertEqual(code, 2)
        self.assertIn("lock_branch", err)
        self.assertNotIn("PROTECTION FINGERPRINT:", out)

    def test_wrong_live_field_type_is_incomplete(self):
        broken = payload()
        broken["enforce_admins"]["enabled"] = "true"
        with self.assertRaises(checker.IncompleteError):
            checker.extract_fingerprint(broken)

    def test_missing_baseline_field_is_incomplete(self):
        baseline = baseline_document()
        del baseline["fingerprint"]["allow_fork_syncing"]
        with self.assertRaises(checker.IncompleteError):
            checker.validate_baseline(baseline)

    def test_reviews_absent_is_recorded_as_null(self):
        self.assertIsNone(self.live["required_pull_request_reviews"])

    def test_reviews_present_object_is_stably_extracted(self):
        current = payload()
        current["required_pull_request_reviews"] = {
            "required_approving_review_count": 2,
            "dismiss_stale_reviews": True,
        }
        extracted = checker.extract_fingerprint(current)
        self.assertEqual(
            extracted["required_pull_request_reviews"],
            {"dismiss_stale_reviews": True, "required_approving_review_count": 2},
        )

    def test_reviews_present_null_is_incomplete_not_absent(self):
        current = payload()
        current["required_pull_request_reviews"] = None
        with self.assertRaises(checker.IncompleteError):
            checker.extract_fingerprint(current)

    def test_write_without_experiment_parameters_is_exit_two(self):
        code, out, err = self.run_main(["--write"])
        self.assertEqual(code, 2)
        self.assertIn("--experiment-pr", err)
        self.assertEqual(out, "")

    def test_write_is_idempotent_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fingerprint.json"
            self.make_baseline(path)
            args = [
                "--write", "--fingerprint", str(path),
                "--experiment-pr", EXPERIMENT["pr"],
                "--experiment-head", EXPERIMENT["head"],
                "--experiment-run", EXPERIMENT["run"],
                "--experiment-date", EXPERIMENT["date"],
            ]
            first, _, err1 = self.run_main(args)
            first_bytes = path.read_bytes()
            second, _, err2 = self.run_main(args)
            second_bytes = path.read_bytes()
        self.assertEqual(first, 0)
        self.assertEqual(second, 0)
        self.assertEqual(err1, "")
        self.assertEqual(err2, "")
        self.assertEqual(first_bytes, second_bytes)

    def test_missing_token_is_exit_two(self):
        code, _, _ = self.run_main(
            ["--endpoint", "full", "--fingerprint", "unused.json"],
            environ={},
        )
        self.assertEqual(code, 2)

    def test_live_context_order_does_not_change_fingerprint(self):
        shuffled = payload()
        shuffled["required_status_checks"]["contexts"] = list(reversed(CONTEXTS))
        self.assertEqual(checker.extract_fingerprint(shuffled)["contexts"], sorted(CONTEXTS))

    def test_auto_403_degrades_and_unchanged_exits_zero(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("HTTP 403", 403)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, err = self.run_main(
                ["--fingerprint", str(path)],
                fetcher=forbidden,
            )
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("DEGRADED MODE", out)

    def test_degraded_context_removal_exits_one(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("HTTP 403", 403)
        summary = summary_payload()
        summary["protection"]["required_status_checks"]["contexts"].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, _ = self.run_main(
                ["--fingerprint", str(path)],
                fetcher=forbidden,
                summary_fetcher=lambda repo, branch, token: summary,
            )
        self.assertEqual(code, 1)
        self.assertIn("FIELD contexts:", out)
        self.assertIn("DIRECTION=LOOSENED", out)

    def test_degraded_enforcement_downgrade_exits_one(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("HTTP 403", 403)
        summary = summary_payload()
        summary["protection"]["required_status_checks"]["enforcement_level"] = "non_admins"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, _ = self.run_main(
                ["--fingerprint", str(path)],
                fetcher=forbidden,
                summary_fetcher=lambda repo, branch, token: summary,
            )
        self.assertEqual(code, 1)
        self.assertIn("FIELD enforcement_level:", out)
        self.assertIn("DIRECTION=LOOSENED", out)

    def test_degraded_output_lists_all_eleven_unverifiable_fields(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("HTTP 403", 403)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, _ = self.run_main(
                ["--fingerprint", str(path)], fetcher=forbidden
            )
        lines = [line for line in out.splitlines() if line.startswith("UNVERIFIABLE ")]
        self.assertEqual(len(lines), 11)
        self.assertEqual(
            [line.split()[1] for line in lines],
            list(checker.UNVERIFIABLE_FIELDS),
        )
        self.assertIn(
            "PROTECTION FINGERPRINT: DEGRADED MODE — 3 field(s) verifiable, 11 unverifiable",
            out,
        )

    def test_full_endpoint_403_exits_two(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("HTTP 403", 403)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, err = self.run_main(
                ["--endpoint", "full", "--fingerprint", str(path)],
                fetcher=forbidden,
            )
        self.assertEqual(code, 2)
        self.assertIn("HTTP 403", err)
        self.assertNotIn("DEGRADED MODE", out)

    def test_degraded_write_preserves_full_fingerprint_bytes(self):
        def forbidden(repo, branch, token):
            raise checker.ApiError("HTTP 403", 403)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            before = json.loads(path.read_text(encoding="utf-8"))["fingerprint"]
            args = [
                "--write", "--fingerprint", str(path),
                "--experiment-pr", EXPERIMENT["pr"],
                "--experiment-head", EXPERIMENT["head"],
                "--experiment-run", EXPERIMENT["run"],
                "--experiment-date", EXPERIMENT["date"],
            ]
            code, _, err = self.run_main(args, fetcher=forbidden)
            after = json.loads(path.read_text(encoding="utf-8"))["fingerprint"]
        self.assertEqual(code, 0, err)
        self.assertEqual(before, after)

    def test_summary_endpoint_does_not_call_full_endpoint(self):
        calls = []
        def full(repo, branch, token):
            calls.append("full")
            raise AssertionError("full endpoint must not be called")
        def summary(repo, branch, token):
            calls.append("summary")
            return self.live_summary_payload
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, _, _ = self.run_main(
                ["--endpoint", "summary", "--fingerprint", str(path)],
                fetcher=full, summary_fetcher=summary,
            )
        self.assertEqual(code, 0)
        self.assertEqual(calls, ["summary"])

    def test_auto_401_degrades(self):
        def unauthorized(repo, branch, token):
            raise checker.ApiError("HTTP 401", 401)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, _ = self.run_main(
                ["--fingerprint", str(path)],
                fetcher=unauthorized, environ={},
            )
        self.assertEqual(code, 0)
        self.assertIn("DEGRADED MODE", out)

    def test_auto_404_degrades(self):
        def missing(repo, branch, token):
            raise checker.ApiError("HTTP 404", 404)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, _ = self.run_main(["--fingerprint", str(path)], fetcher=missing)
        self.assertEqual(code, 0)
        self.assertIn("DEGRADED MODE", out)

    def test_auto_non_auth_http_error_does_not_degrade(self):
        def unavailable(repo, branch, token):
            raise checker.ApiError("HTTP 500", 500)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, out, err = self.run_main(
                ["--fingerprint", str(path)], fetcher=unavailable
            )
        self.assertEqual(code, 2)
        self.assertIn("HTTP 500", err)
        self.assertNotIn("DEGRADED MODE", out)

    def test_unknown_summary_enforcement_is_incomplete(self):
        broken = summary_payload()
        broken["protection"]["required_status_checks"]["enforcement_level"] = "admins"
        with self.assertRaises(checker.IncompleteError):
            checker.extract_summary_fingerprint(broken)

    def test_summary_enabled_false_is_loosened(self):
        self.assertEqual(
            checker.compare_summary(
                self.live_summary,
                dict(self.live_summary, enabled=False),
                False,
            )[1],
            1,
        )

    def test_summary_enabled_false_to_true_is_tightened(self):
        self.assertEqual(
            checker.classify_enforcement("non_admins", "everyone"),
            "TIGHTENED",
        )

    def test_baseline_requires_both_sections(self):
        broken = baseline_document()
        del broken["summary_fingerprint"]
        with self.assertRaises(checker.IncompleteError):
            checker.validate_baseline(broken)

    def test_baseline_summary_requires_all_fields(self):
        broken = baseline_document()
        del broken["summary_fingerprint"]["enforcement_level"]
        with self.assertRaises(checker.IncompleteError):
            checker.validate_baseline(broken)

    def test_full_write_preserves_summary_section(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            before = json.loads(path.read_text())["summary_fingerprint"]
            args = [
                "--endpoint", "full", "--write", "--fingerprint", str(path),
                "--experiment-pr", EXPERIMENT["pr"],
                "--experiment-head", EXPERIMENT["head"],
                "--experiment-run", EXPERIMENT["run"],
                "--experiment-date", EXPERIMENT["date"],
            ]
            code, _, _ = self.run_main(args)
            after = json.loads(path.read_text())["summary_fingerprint"]
        self.assertEqual(code, 0)
        self.assertEqual(before, after)

    def test_summary_write_preserves_full_section(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            before = json.loads(path.read_text())["fingerprint"]
            args = [
                "--endpoint", "summary", "--write", "--fingerprint", str(path),
                "--experiment-pr", EXPERIMENT["pr"],
                "--experiment-head", EXPERIMENT["head"],
                "--experiment-run", EXPERIMENT["run"],
                "--experiment-date", EXPERIMENT["date"],
            ]
            code, _, _ = self.run_main(args)
            after = json.loads(path.read_text())["fingerprint"]
        self.assertEqual(code, 0)
        self.assertEqual(before, after)

    def test_context_normalization_applies_to_summary(self):
        shuffled = summary_payload()
        shuffled["protection"]["required_status_checks"]["contexts"] = list(reversed(CONTEXTS))
        self.assertEqual(
            checker.extract_summary_fingerprint(shuffled)["contexts"],
            sorted(CONTEXTS),
        )

    def test_auto_full_success_does_not_call_summary(self):
        calls = []
        def full(repo, branch, token):
            calls.append("full")
            return self.live_payload
        def summary(repo, branch, token):
            calls.append("summary")
            return self.live_summary_payload
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            self.make_baseline(path)
            code, _, _ = self.run_main(
                ["--fingerprint", str(path)],
                fetcher=full, summary_fetcher=summary,
            )
        self.assertEqual(code, 0)
        self.assertEqual(calls, ["full"])


if __name__ == "__main__":
    unittest.main()
