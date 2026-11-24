"""Tests for the single-node G Applied durable-ledger reference model."""
import tempfile
import unittest
from pathlib import Path

from g_applied_ledger import GAppliedLedger, REQUIRED_GATES


def identity():
    return {
        "context_id": "ctx-1",
        "context_version": "cv-7",
        "delivery_id": "delivery-9",
        "delivery_attempt_id": "attempt-2",
        "inference_request_id": "infer-44",
        "final_request_boundary_id": "boundary-3",
        "provider_attempt_ref": "provider-attempt-5",
        "h_delivery_binding_ref": "h-binding-8",
        "coc_participant_ref": "participant-6",
    }


def gates():
    return {name: True for name in REQUIRED_GATES}


class GAppliedLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "g-applied.sqlite"
        self.ledger = GAppliedLedger(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def evaluate(self, evidence=None, outcome="HANDOFF_ACCEPTED", gate_set=None):
        if evidence is None:
            evidence = {"c_record": "C/1", "h_record": "H/1", "ai_session_ref": "session-123"}
        return self.ledger.evaluate(
            identity(), outcome, evidence,
            gates() if gate_set is None else gate_set,
        )

    def test_new_complete_success_commits_one_full_applied_record(self):
        result = self.evaluate()
        self.assertEqual(result["status"], "FULL_APPLIED")
        self.assertEqual(self.ledger.read(identity())["record_id"], result["record_id"])

    def test_same_identity_and_same_evidence_is_idempotent(self):
        first = self.evaluate()
        replay = self.evaluate()
        self.assertEqual(replay["status"], "IDEMPOTENT_REPLAY")
        self.assertEqual(replay["record_id"], first["record_id"])

    def test_same_identity_changed_evidence_is_conflict_and_original_is_unchanged(self):
        first = self.evaluate()
        conflict = self.evaluate({"c_record": "C/2", "h_record": "H/1", "ai_session_ref": "session-123"})
        self.assertEqual(conflict["status"], "CONFLICT")
        self.assertEqual(self.ledger.read(identity())["evidence_digest"], first["evidence_digest"])
        self.assertEqual(self.ledger.conflict_count(identity()), 1)

    def test_missing_ai_session_evidence_blocks_commit_per_issue_799(self):
        # Issue #799 explicitly requires AI session evidence in issues and PRs;
        # ledger evaluation should block if required ai session ref or evidence is missing.
        missing_ai = {"c_record": "C/1", "h_record": "H/1"}
        result = self.evaluate(evidence=missing_ai)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIsNone(self.ledger.read(identity()))

    def test_non_accepted_c_outcomes_never_create_applied(self):
        for outcome in ("HANDOFF_REJECTED", "NOT_INVOKED", "UNKNOWN", "IN_DOUBT"):
            with self.subTest(outcome=outcome):
                self.assertEqual(self.evaluate(outcome=outcome)["status"], "BLOCKED")
                self.assertIsNone(self.ledger.read(identity()))

    def test_missing_or_failed_authority_gate_blocks_commit(self):
        incomplete = gates()
        incomplete.pop("i_authorization_current")
        self.assertEqual(self.evaluate(gate_set=incomplete)["status"], "BLOCKED")
        failed = gates()
        failed["d_forget_fence_clear"] = False
        self.assertEqual(self.evaluate(gate_set=failed)["status"], "BLOCKED")
        self.assertIsNone(self.ledger.read(identity()))

    def test_restart_reads_original_record_and_replay_returns_same_id(self):
        first = self.evaluate()
        restarted = GAppliedLedger(self.path)
        self.assertEqual(restarted.read(identity())["record_id"], first["record_id"])
        replay = restarted.evaluate(identity(), "HANDOFF_ACCEPTED",
                                     {"c_record": "C/1", "h_record": "H/1", "ai_session_ref": "session-123"}, gates())
        self.assertEqual(replay["status"], "IDEMPOTENT_REPLAY")
        self.assertEqual(replay["record_id"], first["record_id"])