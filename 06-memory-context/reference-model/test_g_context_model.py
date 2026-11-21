"""Conformance tests for G-local Context ChangeSet/reconciliation reference model."""
import unittest

from g_context_model import ContextLedger, ContextModelError, reconcile_entry, current_use_allowed


def entry(entry_id="e1", memory_id="m1", version_id="v1", scopes=None):
    return {
        "entry_id": entry_id, "memory_id": memory_id, "memory_version_id": version_id,
        "scope_refs": scopes or ["scope-user"], "lifecycle": "Active",
        "rendered_content": "memory", "source_refs": ["source-1"], "content_hash": "sha256:1",
        "position": 0, "tier": "P1", "priority": 1,
    }


class ContextChangeSetTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ContextLedger("ctx-1", ("scope-user",))
        self.ledger.entries["e1"] = entry()

    def apply_ops(self, ops, key="k1", base=1):
        return self.ledger.apply_changeset(base_version=base, idempotency_key=key, operations=ops)

    def test_add_creates_one_immutable_target_version(self):
        result = self.apply_ops([{"type": "ADD", "entry": entry("e2", "m2", "v2")}])
        self.assertEqual(result["target_version"], 2)
        self.assertIn("e2", self.ledger.entries)
        self.assertEqual(len(self.ledger.history), 1)

    def test_update_changes_only_context_metadata(self):
        self.apply_ops([{"type": "UPDATE", "entry_id": "e1",
                         "patch": {"priority": 9, "rendered_content": "updated"}}])
        self.assertEqual(self.ledger.entries["e1"]["priority"], 9)
        self.assertEqual(self.ledger.entries["e1"]["memory_version_id"], "v1")

    def test_remove_tombstones_membership_not_canonical_memory(self):
        self.apply_ops([{"type": "REMOVE", "entry_id": "e1"}])
        self.assertNotIn("e1", self.ledger.entries)
        self.assertIn("e1", self.ledger.tombstones)

    def test_replace_is_one_atomic_membership_transition(self):
        self.apply_ops([{"type": "REPLACE", "old_entry_id": "e1",
                         "entry": entry("e2", "m2", "v2")}])
        self.assertNotIn("e1", self.ledger.entries)
        self.assertIn("e2", self.ledger.entries)
        self.assertIn("e1", self.ledger.tombstones)

    def test_reorder_requires_exact_permutation(self):
        self.apply_ops([
            {"type": "ADD", "entry": entry("e2", "m2", "v2")},
            {"type": "REORDER", "entry_ids": ["e2", "e1"]},
        ])
        self.assertEqual(self.ledger.entries["e2"]["position"], 0)
        self.assertEqual(self.ledger.entries["e1"]["position"], 1)

    def test_expire_removes_entry_and_leaves_tombstone(self):
        self.apply_ops([{"type": "EXPIRE", "entry_id": "e1"}])
        self.assertNotIn("e1", self.ledger.entries)
        self.assertIn("e1", self.ledger.tombstones)

    def test_changeset_is_all_or_nothing_on_late_invalid_operation(self):
        before = dict(self.ledger.entries)
        with self.assertRaises(ContextModelError):
            self.apply_ops([
                {"type": "ADD", "entry": entry("e2", "m2", "v2")},
                {"type": "REMOVE", "entry_id": "missing"},
            ])
        self.assertEqual(self.ledger.entries, before)
        self.assertEqual(self.ledger.head_version, 1)
        self.assertEqual(self.ledger.history, [])

    def test_same_key_same_payload_is_idempotent(self):
        ops = [{"type": "UPDATE", "entry_id": "e1", "patch": {"priority": 3}}]
        first = self.apply_ops(ops)
        replay = self.apply_ops(ops)
        self.assertEqual(replay["status"], "IDEMPOTENT_REPLAY")
        self.assertEqual(first["target_version"], replay["target_version"])
        self.assertEqual(self.ledger.head_version, 2)

    def test_same_key_changed_payload_is_conflict(self):
        self.apply_ops([{"type": "UPDATE", "entry_id": "e1", "patch": {"priority": 3}}])
        with self.assertRaisesRegex(ContextModelError, "IDEMPOTENCY_KEY_REUSE"):
            self.apply_ops([{"type": "UPDATE", "entry_id": "e1", "patch": {"priority": 4}}])

    def test_stale_base_version_is_rejected(self):
        self.apply_ops([{"type": "UPDATE", "entry_id": "e1", "patch": {"priority": 3}}])
        with self.assertRaisesRegex(ContextModelError, "BASE_VERSION_MISMATCH"):
            self.apply_ops([{"type": "REMOVE", "entry_id": "e1"}], key="k2", base=1)

    def test_duplicate_membership_and_cross_scope_are_rejected(self):
        with self.assertRaisesRegex(ContextModelError, "DUPLICATE_MEMBERSHIP"):
            self.apply_ops([{"type": "ADD", "entry": entry("e2", "m1", "v1")}])
        with self.assertRaisesRegex(ContextModelError, "SCOPE_MISMATCH"):
            self.apply_ops([{"type": "ADD", "entry": entry("e2", "m2", "v2", ["scope-other"])}])

    def test_unknown_operation_and_canonical_mutation_fields_are_rejected(self):
        with self.assertRaisesRegex(ContextModelError, "UNKNOWN_OPERATION"):
            self.apply_ops([{"type": "MUTATE_CANONICAL", "entry_id": "e1"}])
        with self.assertRaisesRegex(ContextModelError, "INVALID_UPDATE_PATCH"):
            self.apply_ops([{"type": "UPDATE", "entry_id": "e1",
                             "patch": {"memory_version_id": "v2"}}])

    def test_reconciliation_fails_closed_on_unknown_authority_or_incomplete_retrieval(self):
        facts = dict(canonical_status="ACTIVE", permission_current=None,
                     forget_clear=True, retrieval_complete=True)
        self.assertEqual(reconcile_entry(entry(), **facts)["action"], "Block")
        facts["permission_current"] = True
        facts["retrieval_complete"] = False
        self.assertEqual(reconcile_entry(entry(), **facts)["classification"], "Unknown")

    def test_reconciliation_maps_forget_and_supersession_without_rewriting_canonical_truth(self):
        common = dict(permission_current=True, forget_clear=True, retrieval_complete=True)
        forgotten = reconcile_entry(entry(), canonical_status="FORGOTTEN", **common)
        superseded = reconcile_entry(entry(), canonical_status="SUPERSEDED", **common)
        self.assertEqual(forgotten, {"classification": "Forgotten", "action": "Remove"})
        self.assertEqual(superseded["action"], "ReplaceOrRemove")

    def test_current_use_requires_every_currentness_gate(self):
        gates = dict(context_is_head=True, delivery_not_superseded=True,
                     permission_current=True, forget_clear=True, scope_matches=True,
                     session_current=True, capability_current=True)
        self.assertTrue(current_use_allowed(**gates))
        gates["forget_clear"] = None
        self.assertFalse(current_use_allowed(**gates))


if __name__ == "__main__":
    unittest.main()
