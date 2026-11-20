#!/usr/bin/env python3
"""AC-5 contract-level Forget recovery tests.

These tests exercise the existing non-production reference model only. They do
not claim production storage, index/cache, context, replica, or deployment
conformance.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = (
    ROOT
    / "14-ai-development"
    / "work-items"
    / "AID-2026-001"
    / "reference-model"
    / "forget_model.py"
)
SPEC = importlib.util.spec_from_file_location("forget_model", MODEL_PATH)
assert SPEC is not None and SPEC.loader is not None
forget_model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(forget_model)

ContractError = forget_model.ContractError
ForgetOperation = forget_model.ForgetOperation
Governance = forget_model.Governance
Phase = forget_model.Phase
Target = forget_model.Target
TargetState = forget_model.TargetState


class ForgetRecoveryTests(unittest.TestCase):
    def operation_after_suppression(self):
        op = ForgetOperation(
            operation_id="forget-ac5-001",
            memory_id="memory-001",
            principal="principal-001",
            scope="user:001",
            purpose="AC-5 recovery conformance fixture",
        )
        op.authorize(True)
        generation = op.suppress()
        return op, generation

    def test_end_to_end_forget_cleanup_and_restore_recovery(self):
        op, generation = self.operation_after_suppression()
        op.seal_inventory(
            [Target("canonical-memory", "D", "erase")],
            [Target("derived-index", "F", "erase")],
        )
        op.start_cleanup()
        op.record_target(
            "canonical-memory", TargetState.CLEANED,
            "evidence://canonical-memory-cleaned", "cleanup-receipt",
            domain_target=True,
        )
        op.record_target(
            "derived-index", TargetState.ERASED,
            "evidence://derived-index-invalidated", "invalidation-receipt",
        )

        self.assertTrue(op.evaluate_domain())
        self.assertEqual(op.phase, Phase.COMPLETED)
        self.assertEqual(op.evaluate_governance(), Governance.COMPLIANT)
        self.assertEqual(op.public_result(), "Completed")

        # A pre-fence restored snapshot must remain unqueryable. Once the
        # current fence is applied, the restored snapshot may become queryable.
        self.assertFalse(op.restore_is_queryable(generation - 1))
        self.assertTrue(op.restore_is_queryable(generation))

        lease = op.acquire_lease()
        op.commit_checkpoint("forget-complete", lease, "audit://forget-ac5-001")
        self.assertEqual(op.checkpoints["forget-complete"], "audit://forget-ac5-001")

    def test_restore_rejects_pre_forget_snapshot(self):
        op, _ = self.operation_after_suppression()
        self.assertFalse(op.restore_is_queryable(0))

    def test_restore_accepts_snapshot_only_after_current_fence_is_applied(self):
        op, generation = self.operation_after_suppression()
        self.assertTrue(op.restore_is_queryable(generation))
        self.assertFalse(op.restore_is_queryable(generation - 1))

    def test_domain_completion_rejects_stale_generation_evidence(self):
        op, _ = self.operation_after_suppression()
        target = Target("canonical-memory", "D", "erase")
        op.seal_inventory([target], [])
        op.start_cleanup()
        op.record_target(
            "canonical-memory", TargetState.CLEANED,
            "evidence://cleanup", "cleanup-receipt", domain_target=True,
        )
        target.fence_generation -= 1
        self.assertFalse(op.evaluate_domain())
        self.assertNotEqual(op.public_result(), "Completed")

    def test_recovery_checkpoint_rejects_stale_worker_lease(self):
        op, _ = self.operation_after_suppression()
        stale_lease = op.acquire_lease()
        op.acquire_lease()
        with self.assertRaisesRegex(ContractError, "stale lease fence"):
            op.commit_checkpoint("late-checkpoint", stale_lease, "audit://stale")

    def test_cleanup_cannot_start_before_inventory_is_sealed(self):
        op, _ = self.operation_after_suppression()
        with self.assertRaisesRegex(ContractError, "cleanup requires sealed inventory"):
            op.start_cleanup()


if __name__ == "__main__":
    unittest.main(verbosity=2)
