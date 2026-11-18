"""Tests for I global Forget target inventory and completion invariants."""
import unittest

from global_forget_model import Blocked, Conflict, Evidence, GlobalForgetModel, Target


class GlobalForgetModelTests(unittest.TestCase):
    def setUp(self):
        self.g = GlobalForgetModel()
        self.target = Target("F:partition-1", "F-owner", ("scope-A",), "F-cap-v1", "SUPPRESS")
        self.g.register_target(self.target)
        self.seal()

    def seal(self, gaps=()):
        return self.g.seal_inventory(seal_id="seal-1", digest="digest-1",
                                     signer="I-inventory-authority", gaps=gaps)

    def evidence(self, *, status="CONFIRMED", **overrides):
        values = dict(operation_id="forget-op-1", target_id="F:partition-1",
                      seal_id="seal-1", inventory_epoch=self.g.inventory_epoch,
                      owner="F-owner", scope_ref="scope-A", action="SUPPRESS",
                      capability_profile="F-cap-v1", status=status,
                      evidence_ref="evidence-1", integrity_valid=True)
        values.update(overrides)
        return Evidence(**values)

    def complete_setup(self):
        self.g.suppression_established = True
        self.g.d_barrier_complete = True
        self.g.backup_restore_safe = True
        for name in self.g.COMPONENTS:
            self.g.set_component(name, "Confirmed", proof=f"{name}-proof",
                                 reviewer="independent-verifier")

    def test_inventory_seal_requires_authorized_i_signer(self):
        self.g.seal = None
        with self.assertRaises(Blocked):
            self.g.seal_inventory(seal_id="s", digest="d", signer="F-owner")

    def test_inventory_seal_rejects_registry_gaps(self):
        self.g.seal = None
        with self.assertRaises(Blocked):
            self.seal(gaps=["unknown provider"])

    def test_inventory_seal_requires_target_identity_scope_capability(self):
        self.g.seal = None
        self.g.targets["bad"] = Target("bad", "", (), "", "")
        with self.assertRaises(Blocked):
            self.seal()

    def test_inventory_epoch_change_invalidates_seal(self):
        self.g.apply_inventory_change()
        self.assertEqual(self.g.evaluate(now=1), "Reopened")

    def test_new_target_after_seal_reopens_inventory(self):
        self.g.register_target(Target("H:adapter-2", "H-owner", ("scope-A",), "H-cap-v2", "CLEAR"))
        self.assertIsNone(self.g.seal)
        self.assertEqual(self.g.state, "Reopened")

    def test_evidence_must_match_current_seal_and_scope(self):
        result = self.g.record_evidence(self.evidence(scope_ref="scope-B"))
        self.assertEqual(result, "UNKNOWN")
        self.assertEqual(self.g.targets["F:partition-1"].state, "Unknown")

    def test_evidence_from_old_inventory_epoch_is_rejected(self):
        ev = self.evidence()
        self.g.apply_inventory_change()
        with self.assertRaises(Blocked):
            self.g.record_evidence(ev)

    def test_adapter_request_receipt_is_not_delete_ack(self):
        result = self.g.record_evidence(self.evidence(action="REQUEST_RECEIPT"))
        self.assertEqual(result, "UNKNOWN")

    def test_unsupported_capability_remains_unknown(self):
        result = self.g.record_evidence(self.evidence(status="UNSUPPORTED"))
        self.assertEqual(result, "UNKNOWN")

    def test_timeout_or_offline_unknown_blocks_completion(self):
        self.g.record_evidence(self.evidence(status="UNKNOWN"))
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_d_barrier_open_blocks_global_completion(self):
        self.g.record_evidence(self.evidence())
        self.g.suppression_established = True
        self.g.backup_restore_safe = True
        for name in self.g.COMPONENTS:
            self.g.set_component(name, "Confirmed", proof="proof")
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_missing_target_evidence_blocks_completion(self):
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_backup_restore_requires_quarantine_control_replay_and_suppression(self):
        with self.assertRaises(Blocked):
            self.g.restore_backup("F:partition-1", quarantined=False,
                                  current_control_ledger_replayed=True, suppression_revalidated=True)
        self.assertFalse(self.g.backup_restore_safe)

    def test_safe_backup_restore_requires_all_three_proofs(self):
        self.g.restore_backup("F:partition-1", quarantined=True,
                              current_control_ledger_replayed=True, suppression_revalidated=True)
        self.assertTrue(self.g.backup_restore_safe)

    def test_physical_erasure_required_needs_physical_erasure_action(self):
        target = Target("backup-1", "Storage-owner", ("scope-A",), "backup-v1",
                        "SUPPRESS", physical_erasure_required=True)
        self.g.register_target(target)
        self.assertIsNone(self.g.seal)
        self.seal()
        self.g.record_evidence(self.evidence())
        self.g.record_evidence(Evidence("forget-op-1", "backup-1", "seal-1",
            self.g.inventory_epoch, "Storage-owner", "scope-A", "SUPPRESS",
            "backup-v1", "CONFIRMED", "suppress-only-proof"))
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_exception_requires_authorized_independent_approver(self):
        with self.assertRaises(Blocked):
            self.g.approve_exception("F:partition-1", approver_role="privacy",
                                     approver="requester", requester="requester",
                                     scope_ref="scope-A", reason="reason", expiry=10,
                                     now=1, signed_evidence="signed")

    def test_exception_must_be_exact_scoped_signed_and_unexpired(self):
        with self.assertRaises(Blocked):
            self.g.approve_exception("F:partition-1", approver_role="privacy",
                                     approver="approver", requester="requester",
                                     scope_ref="scope-B", reason="reason", expiry=10,
                                     now=1, signed_evidence="signed")

    def test_expired_exception_reopens_completion(self):
        self.g.approve_exception("F:partition-1", approver_role="privacy",
                                 approver="approver", requester="requester",
                                 scope_ref="scope-A", reason="reason", expiry=5,
                                 now=1, signed_evidence="signed")
        self.g.expire_exceptions(now=5)
        self.assertEqual(self.g.targets["F:partition-1"].state, "Unknown")
        self.assertEqual(self.g.state, "Reopened")

    def test_not_applicable_requires_positive_absence_proof_and_independent_reviewer(self):
        with self.assertRaises(Blocked):
            self.g.mark_not_applicable("F:partition-1", proof_of_absence="",
                                       reviewer="reviewer", target_owner="F-owner")
        with self.assertRaises(Blocked):
            self.g.mark_not_applicable("F:partition-1", proof_of_absence="proof",
                                       reviewer="F-owner", target_owner="F-owner")

    def test_owner_local_evidence_cannot_claim_global_completion(self):
        evidence = self.g.report_owner_evidence("F", "F:partition-1")
        self.assertEqual(evidence["global_completion"], "NOT_AUTHORIZED")

    def test_failure_cannot_be_overwritten_by_later_ack_without_resolution(self):
        self.g.set_failed("F:partition-1", "failure-1")
        result = self.g.record_evidence(self.evidence(evidence_ref="late-ack"))
        self.assertEqual(result, "CONFLICT_REQUIRES_OWNER_RESOLUTION")
        self.assertEqual(self.g.targets["F:partition-1"].state, "Failed")

    def test_valid_owner_resolution_can_clear_prior_failure_without_erasing_history(self):
        self.g.set_failed("F:partition-1", "failure-1")
        result = self.g.record_evidence(self.evidence(evidence_ref="resolved-ack",
                                                      resolution_ref="owner-resolution-1"))
        self.assertEqual(result, "CONFIRMED")
        self.assertEqual(self.g.targets["F:partition-1"].evidence_ref, "resolved-ack")

    def test_empty_inventory_cannot_be_sealed_without_absence_proof(self):
        empty = GlobalForgetModel()
        with self.assertRaises(Blocked):
            empty.seal_inventory(seal_id="empty", digest="empty", signer="I-inventory-authority")

    def test_valid_exception_yields_completed_with_policy_exception(self):
        self.g.approve_exception("F:partition-1", approver_role="privacy",
                                 approver="independent-approver", requester="requester",
                                 scope_ref="scope-A", reason="documented retention hold",
                                 expiry=100, now=1, signed_evidence="approval-proof")
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=2), "CompletedWithPolicyException")

    def test_not_applicable_target_requires_proof_and_independent_review_to_complete(self):
        self.g.mark_not_applicable("F:partition-1", proof_of_absence="signed inventory proves absent",
                                   reviewer="independent-reviewer", target_owner="F-owner")
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Completed")

    def test_failed_target_blocks_global_completion(self):
        self.g.set_failed("F:partition-1", "failure-proof")
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_new_target_after_completed_operation_reopens_it(self):
        self.g.record_evidence(self.evidence())
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Completed")
        self.g.register_target(Target("H:late-adapter", "H-owner", ("scope-A",), "H-cap-v1", "CLEAR"))
        self.assertEqual(self.g.state, "Reopened")
        self.assertIsNone(self.g.seal)

    def test_global_completion_requires_every_component_and_target(self):
        self.g.record_evidence(self.evidence())
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Completed")

    def test_component_not_applicable_requires_proof_and_reviewer(self):
        with self.assertRaises(Blocked):
            self.g.set_component("ExternalCopyHandling", "NotApplicable")
        self.g.set_component("ExternalCopyHandling", "NotApplicable",
                             proof="sealed inventory proves absent", reviewer="independent")

    def test_component_confirmation_requires_proof_and_verifier(self):
        with self.assertRaises(Blocked):
            self.g.set_component("ExternalCopyHandling", "Confirmed")
        with self.assertRaises(Blocked):
            self.g.set_component("ExternalCopyHandling", "Confirmed", proof="proof")
        with self.assertRaises(Blocked):
            self.g.set_component("ExternalCopyHandling", "PolicyException",
                                 proof="approval-proof", reviewer="independent-reviewer")

    def test_completion_rechecks_component_proof_at_evaluation(self):
        self.g.record_evidence(self.evidence())
        self.complete_setup()
        self.g.component_proofs["ExternalCopyHandling"]["proof"] = ""
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_component_policy_exception_cannot_complete_without_governance_workflow(self):
        self.g.record_evidence(self.evidence())
        self.complete_setup()
        self.g.component_states["ExternalCopyHandling"] = "PolicyException"
        self.g.component_proofs["ExternalCopyHandling"] = {
            "proof": "approval-proof", "reviewer": "independent-reviewer"
        }
        self.assertEqual(self.g.evaluate(now=1), "Pending")

    def test_physical_erasure_target_requires_explicit_action(self):
        self.g.register_target(Target("backup-2", "Storage-owner", ("scope-A",),
                                      "backup-v1", "PHYSICAL_ERASURE",
                                      physical_erasure_required=True))
        self.assertIsNone(self.g.seal)
        self.seal()
        self.g.record_evidence(self.evidence())
        self.g.record_evidence(Evidence("forget-op-1", "backup-2", "seal-1",
            self.g.inventory_epoch, "Storage-owner", "scope-A", "PHYSICAL_ERASURE",
            "backup-v1", "CONFIRMED", "erase-proof"))
        self.complete_setup()
        self.assertEqual(self.g.evaluate(now=1), "Completed")


if __name__ == "__main__":
    unittest.main()