"""Structural tests for the Storage prepared-participant proof schema candidate 1.0.0."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "08-bmcp-protocol" / "schemas" / "bmcp.storage-prepared-participant-proof-1.0.0.schema.json"


def envelope(payload_type):
    return {
        "payload_type": payload_type,
        "schema_version": "1.0.0",
        "issuer_principal_ref": "Principal/StorageSigner",
        "subject_ref": "PreparedParticipant/001",
        "owner_authority_ref": "StorageAuthority/Canonical",
        "audience_ref": "Service/COC-I-Storage",
        "target_environment_ref": "Environment/ProdCandidate",
        "purpose": "prepared-participant-proof",
        "key_id": "Key/Storage/001",
        "key_version": "1",
        "algorithm_profile_ref": "SignatureProfile/UNAPPROVED",
        "canonicalization_profile_ref": "CanonicalizationProfile/UNAPPROVED",
        "digest_profile_ref": "DigestProfile/SHA-256-CANDIDATE",
        "issued_at": "2026-11-17T09:00:00Z",
        "trust_status_evidence_ref": "KeyStatusEvidence/001",
        "payload_digest": "a" * 64,
        "signature": "c2lnbmF0dXJl"
    }


def common_payload():
    return {
        "prepared_participant_ref": "PreparedParticipant/001",
        "prepared_transaction_gid": "gid_001",
        "postgresql_native_xid": 4294967000,
        "canonical_authority_db_ref": "CanonicalAuthorityDB/001",
        "database_incarnation_ref": "DatabaseIncarnation/001",
        "postgresql_system_identifier": "765432109876543210",
        "postgresql_database_oid": "16384",
        "original_prepare_timeline": 3,
        "original_prepare_lsn": "0/16B6C50",
        "publication_operation_id": "PublicationOperation/001",
        "request_digest": "b" * 64,
        "participant_tuple_digest": "c" * 64,
        "owner_boundary_ref": "OwnerBoundary/Storage/001",
        "causal_order_domain_ref": "CausalOrderDomain/001",
        "policy_domain_ref": "PolicyDomain/001",
        "coc_prepare_intent_position": "COCPosition/100",
        "coc_prepare_intent_digest": "d" * 64,
        "prepare_attempt_ref": "PrepareAttempt/001",
        "prepare_attempt_generation": 1,
        "participant_ledger_ref": "ParticipantLedger/001",
        "participant_ledger_version": 1
    }


def valid_receipt():
    payload = common_payload()
    payload.update({
        "prepared_state": "PREPARED",
        "prepared_observation_source": "AUTHORITATIVE_WRITABLE_PRIMARY_READBACK",
        "prepared_observed_at": "2026-11-17T09:00:01Z"
    })
    return {
        "schema_id": "bmcp.storage-prepared-participant-proof",
        "schema_version": "1.0.0",
        "message_type": "Storage.PreparedParticipantReceipt",
        "message_id": "Message/001",
        "message_nonce": "Nonce/001",
        "signature_envelope": envelope("Storage.PreparedParticipantReceipt"),
        "payload": payload
    }


def valid_resolution(outcome):
    payload = common_payload()
    payload.update({
        "storage_resolution_outcome": outcome,
        "participant_outcome_ledger_ref": "ParticipantOutcomeLedger/001",
        "participant_outcome_ledger_version": 2,
        "authoritative_source_role": "CANONICAL_WRITABLE_PRIMARY",
        "storage_same_gid_resolution_ref": "SameGidResolution/001",
        "storage_private_visibility_state": "NOT_VISIBLE",
        "storage_lock_retention_state": "RETAINED",
        "recovery_observations": [{
            "recovery_epoch_ref": "RecoveryEpoch/001",
            "observed_database_incarnation_ref": "DatabaseIncarnation/001",
            "postgresql_system_identifier": "765432109876543210",
            "recovery_timeline": 4,
            "recovery_lsn": "0/16B7000",
            "source_role": "RECOVERY_AUTHORITY",
            "observed_at": "2026-11-17T09:10:00Z",
            "evidence_ref": "RecoveryObservation/001",
            "evidence_digest": "e" * 64
        }],
        "i_terminal_outcome": "UNKNOWN"
    })
    if outcome == "COMMITTED":
        payload.update({
            "owner_final_gate_participant_ref": "OwnerFinalGateParticipant/001",
            "commit_authorization_receipt_ref": "CommitAuthorizationReceipt/001",
            "commit_authorization_receipt_digest": "f" * 64,
            "i_receipt_consumption_ref": "ReceiptConsumption/001",
            "i_receipt_consumption_digest": "1" * 64,
            "i_terminal_proof_ref": "ITerminalProof/001",
            "i_terminal_proof_digest": "2" * 64,
            "i_sequencer_ref": "ISequencer/001",
            "i_sequencer_epoch": "ISequencerEpoch/7",
            "i_sequencer_position": "IPolicyPosition/99",
            "i_permission_epoch": "PermissionEpoch/12",
            "i_terminal_outcome": "COMMIT_WON",
            "storage_private_visibility_state": "VISIBLE",
            "storage_lock_retention_state": "RELEASED_AFTER_TERMINAL",
            "visibility_pointer_transaction_ref": "VisibilityPointerTxn/001",
            "publication_receipt_ref": "PublicationReceipt/001",
            "publication_receipt_digest": "3" * 64,
            "atomic_publication_transaction_ref": "AtomicPublicationTxn/001"
        })
    elif outcome == "ROLLED_BACK":
        payload.update({
            "owner_final_gate_participant_ref": "OwnerFinalGateParticipant/001",
            "commit_authorization_receipt_ref": "CommitAuthorizationReceipt/001",
            "commit_authorization_receipt_digest": "f" * 64,
            "i_receipt_consumption_ref": "ReceiptConsumption/001",
            "i_receipt_consumption_digest": "1" * 64,
            "i_terminal_proof_ref": "ITerminalProof/001",
            "i_terminal_proof_digest": "2" * 64,
            "i_sequencer_ref": "ISequencer/001",
            "i_sequencer_epoch": "ISequencerEpoch/7",
            "i_sequencer_position": "IPolicyPosition/99",
            "i_permission_epoch": "PermissionEpoch/12",
            "i_terminal_outcome": "REVOCATION_WON",
            "storage_private_visibility_state": "NOT_VISIBLE",
            "storage_lock_retention_state": "RELEASED_AFTER_TERMINAL",
            "nonpublication_proof_ref": "NonPublicationProof/001"
        })
    else:
        payload.update({
            "unknown_reason_class": "I_OUTCOME_UNKNOWN",
            "storage_private_visibility_state": "NOT_VISIBLE",
            "storage_lock_retention_state": "RETAINED",
            "i_terminal_outcome": "UNKNOWN"
        })
    return {
        "schema_id": "bmcp.storage-prepared-participant-proof",
        "schema_version": "1.0.0",
        "message_type": "Storage.StorageResolutionProof",
        "message_id": "Message/002",
        "message_nonce": "Nonce/002",
        "signature_envelope": envelope("Storage.StorageResolutionProof"),
        "payload": payload
    }


class StoragePreparedParticipantProofSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_schema_is_valid_draft_2020_12_and_versioned(self):
        Draft202012Validator.check_schema(self.schema)
        self.assertIn("/1.0.0", self.schema["$id"])

    def test_receipt_and_all_resolution_outcomes_validate(self):
        self.validator.validate(valid_receipt())
        for outcome in ("COMMITTED", "ROLLED_BACK", "UNKNOWN"):
            with self.subTest(outcome=outcome):
                self.validator.validate(valid_resolution(outcome))

    def test_database_incarnation_attempt_and_ledger_are_required(self):
        record = valid_receipt()
        for field in ("database_incarnation_ref", "prepare_attempt_ref",
                      "prepare_attempt_generation", "participant_ledger_ref",
                      "participant_ledger_version", "participant_tuple_digest"):
            broken = copy.deepcopy(record)
            broken["payload"].pop(field)
            with self.subTest(missing=field):
                self.assertFalse(self.validator.is_valid(broken))

    def test_gid_and_native_xid_are_distinct_and_strictly_typed(self):
        record = valid_receipt()
        self.assertIsInstance(record["payload"]["prepared_transaction_gid"], str)
        self.assertIsInstance(record["payload"]["postgresql_native_xid"], int)
        broken = copy.deepcopy(record)
        broken["payload"]["postgresql_native_xid"] = "4294967000"
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["prepared_transaction_gid"] = "bad gid"
        self.assertFalse(self.validator.is_valid(broken))

    def test_gid_bound_and_postgres_metadata_formats(self):
        record = valid_receipt()
        broken = copy.deepcopy(record)
        broken["payload"]["prepared_transaction_gid"] = "g" * 201
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["postgresql_system_identifier"] = "cluster-A"
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["postgresql_database_oid"] = "db-oid"
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["original_prepare_lsn"] = "not-an-lsn"
        self.assertFalse(self.validator.is_valid(broken))

    def test_receipt_requires_authoritative_primary_readback(self):
        record = valid_receipt()
        record["payload"]["prepared_observation_source"] = "DRIVER_ACK"
        self.assertFalse(self.validator.is_valid(record))

    def test_committed_requires_i_commit_won_and_atomic_publication_evidence(self):
        record = valid_resolution("COMMITTED")
        self.validator.validate(record)
        for field in ("i_terminal_proof_ref", "publication_receipt_ref",
                      "visibility_pointer_transaction_ref", "atomic_publication_transaction_ref"):
            broken = copy.deepcopy(record)
            broken["payload"].pop(field)
            with self.subTest(missing=field):
                self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["i_terminal_outcome"] = "ABORT_WON"
        self.assertFalse(self.validator.is_valid(broken))

    def test_rollback_requires_i_abort_terminal_and_nonpublication_proof(self):
        record = valid_resolution("ROLLED_BACK")
        self.validator.validate(record)
        broken = copy.deepcopy(record)
        broken["payload"].pop("nonpublication_proof_ref")
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["i_terminal_outcome"] = "COMMIT_WON"
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["publication_receipt_ref"] = "PublicationReceipt/Contradictory"
        self.assertFalse(self.validator.is_valid(broken))

    def test_unknown_retains_private_state_and_locks(self):
        record = valid_resolution("UNKNOWN")
        self.validator.validate(record)
        broken = copy.deepcopy(record)
        broken["payload"]["storage_lock_retention_state"] = "RELEASED_AFTER_TERMINAL"
        self.assertFalse(self.validator.is_valid(broken))
        broken = copy.deepcopy(record)
        broken["payload"]["unknown_reason_class"] = None
        self.assertFalse(self.validator.is_valid(broken))

    def test_signature_envelope_is_required_and_non_nullable(self):
        record = valid_receipt()
        record["signature_envelope"].pop("trust_status_evidence_ref")
        self.assertFalse(self.validator.is_valid(record))
        record = valid_receipt()
        record["signature_envelope"]["key_id"] = None
        self.assertFalse(self.validator.is_valid(record))

    def test_payload_type_and_schema_version_downgrade_are_rejected(self):
        record = valid_receipt()
        record["signature_envelope"]["payload_type"] = "Storage.StorageResolutionProof"
        self.assertFalse(self.validator.is_valid(record))
        record["schema_version"] = "0.9.0"
        self.assertFalse(self.validator.is_valid(record))

    def test_original_prepare_coordinates_are_separate_from_recovery_observations(self):
        record = valid_resolution("UNKNOWN")
        self.assertEqual(record["payload"]["original_prepare_timeline"], 3)
        self.assertEqual(record["payload"]["original_prepare_lsn"], "0/16B6C50")
        observation = record["payload"]["recovery_observations"][0]
        self.assertEqual(observation["recovery_timeline"], 4)
        self.assertEqual(observation["recovery_lsn"], "0/16B7000")
        self.validator.validate(record)

    def test_unknown_fields_are_rejected_until_a_new_schema_version(self):
        record = valid_receipt()
        record["payload"]["unregistered_critical_field"] = "must-not-be-ignored"
        self.assertFalse(self.validator.is_valid(record))


if __name__ == "__main__":
    unittest.main()
