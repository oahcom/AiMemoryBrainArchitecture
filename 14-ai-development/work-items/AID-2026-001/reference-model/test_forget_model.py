import unittest

from forget_model import (
    ContractError, ForgetOperation, Governance, MemoryState, Phase,
    Target, TargetState, idempotent_request,
)


class ForgetReferenceModelTests(unittest.TestCase):
    def operation(self):
        op = ForgetOperation("op-1", "mem-1", "principal-1", "scope-1", "user-request")
        op.authorize(True)
        op.suppress()
        op.seal_inventory(
            [Target("canonical", "D", "suppress")],
            [Target("index", "F", "invalidate"), Target("adapter", "H", "clear")],
        )
        op.start_cleanup()
        return op

    def test_suppression_linearizes_memory_and_fence_together(self):
        op = ForgetOperation("op", "mem", "p", "s", "forget")
        op.authorize(True)
        generation = op.suppress()
        self.assertEqual(generation, 1)
        self.assertEqual(op.memory_state, MemoryState.FORGOTTEN)
        self.assertEqual(op.phase, Phase.SUPPRESSION_COMMITTED)

    def test_cancel_after_suppression_cannot_restore_access(self):
        op = self.operation()
        with self.assertRaises(ContractError):
            op.cancel()
        self.assertEqual(op.memory_state, MemoryState.FORGOTTEN)
        self.assertEqual(op.fence_generation, 1)

    def test_domain_completion_is_separate_from_governance(self):
        op = self.operation()
        op.record_target("canonical", TargetState.CLEANED, "ev-d", "transaction", domain_target=True)
        self.assertTrue(op.evaluate_domain())
        self.assertEqual(op.phase, Phase.COMPLETED)
        self.assertEqual(op.governance, Governance.PENDING)
        self.assertEqual(op.public_result(), "Incomplete")

    def test_unknown_or_unsupported_cross_system_target_blocks_compliance(self):
        op = self.operation()
        op.record_target("canonical", TargetState.CLEANED, "ev-d", "transaction", domain_target=True)
        op.evaluate_domain()
        op.record_target("index", TargetState.ERASED, "ev-f", "erase-proof")
        op.record_target("adapter", TargetState.UNKNOWN, "ev-h", "unknown-receipt", capability="conditional")
        self.assertEqual(op.evaluate_governance(), Governance.NON_COMPLIANT)
        self.assertEqual(op.public_result(), "Incomplete")

    def test_ack_is_not_erase_evidence(self):
        op = self.operation()
        op.record_target("canonical", TargetState.CLEANED, "ev-d", "transaction", domain_target=True)
        op.evaluate_domain()
        op.record_target("index", TargetState.ERASED, "ev-f", "erase-proof")
        op.record_target("adapter", TargetState.ACKNOWLEDGED, "ack", "adapter-ack")
        self.assertEqual(op.evaluate_governance(), Governance.NON_COMPLIANT)

    def test_notify_ack_can_only_satisfy_notify_action(self):
        op = self.operation()
        op.cross_system_targets["adapter"].required_action = "notify"
        op.record_target("canonical", TargetState.CLEANED, "ev-d", "transaction", domain_target=True)
        op.evaluate_domain()
        op.record_target("index", TargetState.ERASED, "ev-f", "erase-proof")
        op.record_target("adapter", TargetState.ACKNOWLEDGED, "ack", "notify-receipt")
        self.assertEqual(op.evaluate_governance(), Governance.COMPLIANT)
        self.assertEqual(op.public_result(), "Completed")

    def test_bounded_approved_exception_is_derived_projection_only(self):
        op = self.operation()
        op.record_target("canonical", TargetState.CLEANED, "ev-d", "transaction", domain_target=True)
        op.evaluate_domain()
        op.record_target("index", TargetState.ERASED, "ev-f", "erase-proof")
        retained = op.cross_system_targets["adapter"]
        retained.state = TargetState.POLICY_RETAINED
        retained.fence_generation = op.fence_generation
        retained.evidence_ref = "retention-proof"
        retained.evidence_kind = "policy-retention"
        retained.exception_approved = True
        retained.exception_expires = 100
        self.assertEqual(op.evaluate_governance(now=1), Governance.COMPLIANT_WITH_EXCEPTION)
        self.assertEqual(op.public_result(), "CompletedWithPolicyException")
        self.assertEqual(op.evaluate_governance(now=101), Governance.NON_COMPLIANT)

    def test_inventory_expansion_invalidates_prior_evaluation(self):
        op = self.operation()
        op.record_target("canonical", TargetState.CLEANED, "ev-d", "transaction", domain_target=True)
        op.evaluate_domain()
        op.record_target("index", TargetState.ERASED, "ev-f", "erase-proof")
        op.record_target("adapter", TargetState.ERASED, "ev-h", "erase-proof")
        op.evaluate_governance()
        self.assertEqual(op.public_result(), "Completed")
        old_revision = op.inventory_revision
        op.expand_inventory(Target("late-cache", "F", "invalidate"))
        self.assertEqual(op.inventory_revision, old_revision + 1)
        self.assertEqual(op.phase, Phase.CLEANUP_IN_PROGRESS)
        self.assertEqual(op.governance, Governance.PENDING)
        self.assertEqual(op.public_result(), "Incomplete")

    def test_stale_lease_cannot_commit_checkpoint(self):
        op = self.operation()
        first = op.acquire_lease()
        second = op.acquire_lease()
        with self.assertRaises(ContractError):
            op.commit_checkpoint("cleanup", first, "stale-evidence")
        op.commit_checkpoint("cleanup", second, "current-evidence")
        self.assertEqual(op.checkpoints["cleanup"], "current-evidence")

    def test_idempotency_key_binds_canonical_request(self):
        store = {}
        digest = ForgetOperation.canonical_request_hash("mem", "p", "s", "purpose")
        self.assertEqual(idempotent_request(store, "key", digest, "op-1"), "op-1")
        self.assertEqual(idempotent_request(store, "key", digest, "op-2"), "op-1")
        other = ForgetOperation.canonical_request_hash("other-mem", "p", "s", "purpose")
        with self.assertRaises(ContractError):
            idempotent_request(store, "key", other, "op-3")

    def test_backup_restore_must_apply_latest_fence_before_serving(self):
        op = self.operation()
        self.assertFalse(op.restore_is_queryable(0))
        self.assertTrue(op.restore_is_queryable(op.fence_generation))

    def test_context_remove_does_not_change_canonical_lifecycle(self):
        op = ForgetOperation("op", "mem", "p", "s", "forget")
        context = {"entry-a", "entry-b"}
        updated = op.context_remove(context, "entry-a")
        self.assertEqual(updated, {"entry-b"})
        self.assertEqual(op.memory_state, MemoryState.ACTIVE)
        self.assertEqual(op.phase, Phase.REQUESTED)

    def test_denied_authorization_never_suppresses(self):
        op = ForgetOperation("op", "mem", "p", "s", "forget")
        op.authorize(False)
        self.assertEqual(op.phase, Phase.FAILED)
        self.assertEqual(op.memory_state, MemoryState.ACTIVE)
        self.assertEqual(op.fence_generation, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
