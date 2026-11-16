"""Unit tests for the JF-10 COC bridge semantic reference validator."""
import unittest

from jf10_coc_semantic_validator import BridgeValidationError, MESSAGE_TYPES, validate_bridge


def valid_messages():
    common = {
        "publication_operation_id": "op:1", "request_digest": "a" * 64,
        "owner_boundary": "owner:C", "participant_intent_ref": "I:pi:1",
        "policy_domain_ref": "I:pd:1", "storage_participant_ref": "S:p:1",
        "storage_xid_ref": "S:xid:1", "participant_digest": "b" * 64,
        "storage_authority_db_ref": "S:db:1", "causal_order_coordinator_ref": "COC:1",
        "causal_order_domain_ref": "COC:d:1", "causal_order_transaction_ref": "COC:t:1",
    }
    records = []
    for i, kind in enumerate(MESSAGE_TYPES):
        records.append({**common, "message_type": kind, "message_id": f"m:{i}",
                        "payload_digest": f"{i:064x}"})
    records[0].update(prepare_intent_state="REGISTERED", preallocated_storage_xid_ref="S:xid:1",
                      prepare_intent_coc_position="COC:pos:1", prepare_intent_entry_digest="c"*64,
                      registration_commit_proof_ref="COC:commit:1")
    records[1].update(prepared_participant_receipt_ref="S:prepared:1", prepared_participant_receipt_digest="d"*64,
                      storage_prepare_state="PREPARED_DURABLE", storage_prepare_transaction_ref="S:xid:1",
                      prepared_coc_position="COC:pos:2", prepare_intent_coc_position="COC:pos:1",
                      prepare_intent_entry_digest="c"*64, storage_private_visibility_state="NOT_VISIBLE",
                      storage_lock_retention_state="RETAINED", registration_commit_proof_ref="COC:commit:2")
    records[2].update(i_authorization_terminal_ref="I:terminal:1", i_receipt_consumption_proof_ref="I:consume:1",
                      i_sequencer_ref="I:seq:1", i_sequencer_position="I:pos:1", i_decision_digest="e"*64,
                      i_terminal_outcome="COMMIT_WON", i_revocation_request_state="NONE_AT_TERMINALIZATION",
                      i_owner_signature_ref="I:sig:1", observed_coc_prepare_intent_position="COC:pos:1",
                      observed_coc_prepared_position="COC:pos:2")
    records[3].update(storage_resolution_outcome="COMMITTED", storage_resolution_transaction_ref="S:xid:1",
                      storage_resolution_digest="f"*64, storage_owner_outcome_ref="S:outcome:1",
                      storage_owner_signature_ref="S:sig:1", storage_same_xid_proof_ref="S:same-xid:1",
                      storage_visibility_state="VISIBLE", storage_lock_release_state="RELEASED_AFTER_TERMINAL",
                      storage_publication_receipt_ref="S:pub:1", visibility_pointer_transaction_ref="S:xid:1")
    records[4].update(reconciliation_state="RECONCILED_TERMINAL", i_lookup_state="COMMIT_WON",
                      storage_lookup_state="COMMITTED", d_barrier_state="SATISFIED",
                      reconciled_coc_prefix_position="COC:pos:5", reconciliation_observation_ref="COC:reconcile:1")
    return records


class BridgeValidatorTests(unittest.TestCase):
    def test_valid_terminal_bridge(self):
        result = validate_bridge(valid_messages())
        self.assertEqual(result["reconciliation_state"], "RECONCILED_TERMINAL")

    def test_changed_xid_is_conflict(self):
        records = valid_messages()
        records[3]["storage_xid_ref"] = "S:xid:other"
        with self.assertRaisesRegex(BridgeValidationError, "immutable tuple conflict"):
            validate_bridge(records)

    def test_prepared_receipt_must_bind_exact_xid(self):
        records = valid_messages()
        records[1]["storage_prepare_transaction_ref"] = "S:xid:other"
        with self.assertRaisesRegex(BridgeValidationError, "exact XID"):
            validate_bridge(records)

    def test_i_revocation_present_requires_cutoff_proof(self):
        records = valid_messages()
        records[2]["i_revocation_request_state"] = "PRESENT"
        records[2]["i_revocation_request_ref"] = "I:revoke:1"
        with self.assertRaisesRegex(BridgeValidationError, "i_revocation_cutoff_proof_ref"):
            validate_bridge(records)

    def test_commit_requires_visibility_and_publication_receipt(self):
        records = valid_messages()
        del records[3]["storage_publication_receipt_ref"]
        with self.assertRaisesRegex(BridgeValidationError, "storage_publication_receipt_ref"):
            validate_bridge(records)

    def test_rollback_forbids_publication_receipt(self):
        records = valid_messages()
        records[3].update(storage_resolution_outcome="ROLLED_BACK",
                          storage_visibility_state="NOT_VISIBLE",
                          storage_nonpublication_proof_ref="S:not-published:1")
        records[4]["storage_lookup_state"] = "ROLLED_BACK"
        with self.assertRaisesRegex(BridgeValidationError, "must not carry publication evidence"):
            validate_bridge(records)

    def test_terminal_reconciliation_requires_d_satisfied(self):
        records = valid_messages()
        records[4]["d_barrier_state"] = "OPEN"
        with self.assertRaisesRegex(BridgeValidationError, "satisfied D barrier"):
            validate_bridge(records)

    def test_unknown_cannot_be_reported_as_terminal_i(self):
        records = valid_messages()
        records[2]["i_terminal_outcome"] = "UNKNOWN"
        records[4]["i_lookup_state"] = "UNKNOWN"
        with self.assertRaisesRegex(BridgeValidationError, "I outcome is not terminal"):
            validate_bridge(records)

    def test_multi_policy_domain_rejected(self):
        records = valid_messages()
        records[0]["policy_domain_refs"] = ["I:pd:1", "I:pd:2"]
        with self.assertRaisesRegex(BridgeValidationError, "multi-policy-domain"):
            validate_bridge(records)

    def test_reconciliation_must_match_owner_lookups(self):
        records = valid_messages()
        records[4]["storage_lookup_state"] = "ROLLED_BACK"
        with self.assertRaisesRegex(BridgeValidationError, "Storage lookup conflicts"):
            validate_bridge(records)


if __name__ == "__main__":
    unittest.main()
