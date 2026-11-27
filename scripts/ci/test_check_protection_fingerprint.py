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
        # Key absence is the observed baseline state.
    }


def fingerprint():
    return checker.extract_fingerprint(payload())


class ProtectionFingerprintTests(unittest.TestCase):
    def setUp(self):
        self.live_payload = payload()
        self.live = checker.extract_fingerprint(self.live_payload)
        self.recorded = dict(self.live)

    def run_main(self, argv, fetcher=None, directory=None):
        output = io.StringIO()
        errors = io.StringIO()
        fetcher = fetcher or (lambda repo, branch, token: self.live_payload)
        args = list(argv)
        if directory is not None:
            args += ["--fingerprint", str(Path(directory) / "fingerprint.json")]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = checker.main(args, payload_fetcher=fetcher, environ={"GITHUB_TOKEN": "test-token"})
        return code, output.getvalue(), errors.getvalue()

    def test_no_changes_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fingerprint.json"
            checker.write_baseline(path, self.recorded, EXPERIMENT)
            code, out, err = self.run_main(["--fingerprint", str(path)], directory=None)
        self.assertEqual(code, 0)
        self.assertIn("0 field(s) changed, 0 loosened, 0 tightened", out)
        self.assertEqual(err, "")

    def test_strict_true_to_false_is_loosened(self):
        self.recorded["strict"] = True
        live = dict(self.recorded, strict=False)
        self.assertEqual(checker.classify_field("strict", self.recorded["strict"], live["strict"]), "LOOSENED")

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
            checker.classify_field("required_pull_request_reviews", {"required_approving_review_count": 1}, None),
            "LOOSENED",
        )

    def test_context_removal_is_loosened(self):
        self.assertEqual(checker.classify_contexts(CONTEXTS, CONTEXTS[:-1]), "LOOSENED")

    def test_context_addition_is_tightened(self):
        self.assertEqual(checker.classify_contexts(CONTEXTS, CONTEXTS + ["New required check"]), "TIGHTENED")

    def test_context_mixed_addition_and_removal_is_loosened(self):
        changed = CONTEXTS[:-1] + ["Replacement required check"]
        self.assertEqual(checker.classify_contexts(CONTEXTS, changed), "LOOSENED")

    def test_required_linear_history_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("required_linear_history", False, True), "TIGHTENED")

    def test_required_conversation_resolution_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("required_conversation_resolution", False, True), "TIGHTENED")

    def test_lock_branch_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("lock_branch", False, True), "TIGHTENED")

    def test_allow_fork_syncing_true_to_false_is_tightened(self):
        self.assertEqual(checker.classify_field("allow_fork_syncing", True, False), "TIGHTENED")

    def test_required_signatures_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("required_signatures", False, True), "TIGHTENED")

    def test_required_reviews_absent_to_present_is_tightened(self):
        self.assertEqual(
            checker.classify_field("required_pull_request_reviews", None, {"required_approving_review_count": 1}),
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
        self.assertEqual(checker.classify_field("required_linear_history", True, False), "LOOSENED")

    def test_block_creations_false_to_true_is_tightened(self):
        self.assertEqual(checker.classify_field("block_creations", False, True), "TIGHTENED")

    def test_required_conversation_resolution_true_to_false_is_loosened(self):
        self.assertEqual(checker.classify_field("required_conversation_resolution", True, False), "LOOSENED")

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
            raise checker.ApiError("GitHub protection API HTTP 403: Forbidden")
        code, out, err = self.run_main(["--fingerprint", "unused.json"], fetcher=forbidden)
        self.assertEqual(code, 2)
        self.assertIn("HTTP 403", err)
        self.assertNotIn("PROTECTION FINGERPRINT:", out)

    def test_http_404_is_incomplete_exit_two(self):
        def missing(repo, branch, token):
            raise checker.ApiError("GitHub protection API HTTP 404: Not Found")
        code, out, err = self.run_main(["--fingerprint", "unused.json"], fetcher=missing)
        self.assertEqual(code, 2)
        self.assertIn("HTTP 404", err)
        self.assertNotIn("PROTECTION FINGERPRINT:", out)

    def test_missing_live_field_is_incomplete_exit_two(self):
        broken = payload()
        del broken["lock_branch"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fingerprint.json"
            checker.write_baseline(path, self.live, EXPERIMENT)
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
        baseline = {
            "schema_version": 3,
            "fingerprint": dict(self.live),
            "experiment": EXPERIMENT,
        }
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
            args = [
                "--write",
                "--fingerprint", str(path),
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
        code = checker.main(
            ["--fingerprint", "unused.json"],
            payload_fetcher=lambda repo, branch, token: self.live_payload,
            environ={},
        )
        self.assertEqual(code, 2)

    def test_live_context_order_does_not_change_fingerprint(self):
        shuffled = payload()
        shuffled["required_status_checks"]["contexts"] = list(reversed(CONTEXTS))
        self.assertEqual(checker.extract_fingerprint(shuffled)["contexts"], sorted(CONTEXTS))


if __name__ == "__main__":
    unittest.main()
