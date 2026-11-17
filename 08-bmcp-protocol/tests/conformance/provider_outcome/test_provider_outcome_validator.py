"""Unit tests for H's fail-closed C Provider Outcome validator core.

These tests cover parsing and deterministic local predicates only. They do not
claim profile registration, signature/key verification, provider truth, ledger
membership, COC quorum, cross-language interoperability or production readiness.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve()
H_ROOT = ROOT.parents[3]
sys.path.insert(0, str(H_ROOT / "validators"))

from provider_outcome_validator import (  # noqa: E402
    AuthorityChecks,
    DuplicateJSONKey,
    _candidate_digest_and_preimage,
    _semantic_errors,
    parse_strict_json,
    SCHEMA_ARTIFACT_REVISION,
    WIRE_SCHEMA_VERSION,
)
from jsonschema import Draft202012Validator, FormatChecker


class ProviderOutcomeValidatorUnitTests(unittest.TestCase):
    def test_01_duplicate_json_members_are_rejected(self):
        with self.assertRaises(DuplicateJSONKey):
            parse_strict_json(b'{"a":1,"a":2}')

    def test_02_invalid_utf8_is_rejected(self):
        with self.assertRaises(UnicodeDecodeError):
            parse_strict_json(b'{"value":"\xff"}')

    def test_03_non_finite_numbers_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_strict_json(b'{"value":NaN}')

    def test_04_digest_and_preimage_bind_profile_and_message_type(self):
        record = {
            "message_type": "C_PROVIDER_OUTCOME_RECORDED",
            "message_id": "message-not-domain-component",
            "signature_profile_id": "AIMBA-C-CRYPTO-1.0",
            "record_ref": "C/outcome/1",
            "payload_digest": "0" * 64,
            "signature": "A" * 86,
        }
        digest, preimage = _candidate_digest_and_preimage(record)
        self.assertEqual(len(digest), 64)
        self.assertIn(b"AIMBA-C-SIGNATURE-v1\x00", preimage)
        self.assertIn(b"AIMBA-C-CRYPTO-1.0\x00", preimage)
        self.assertIn(b"C_PROVIDER_OUTCOME_RECORDED\x00", preimage)
        self.assertNotIn(b"message-not-domain-component\x00", preimage)

    def test_05_local_semantics_reject_owner_highwater_violation(self):
        record = {
            "COwnerLocalSequence": "9",
            "COwnerHighWater": "8",
            "COCParticipantIntentRef": "COC/intent/1",
            "COCParticipantReservationRef": "COC/reservation/1",
            "COCAbsenceReason": None,
            "Outcome": "UNKNOWN",
            "SideEffectStatus": "POSSIBLE_OR_UNKNOWN",
            "UnknownReasonRef": "C/unknown/1",
        }
        self.assertIn("C owner local sequence exceeds high-water", _semantic_errors(record))

    def test_06_missing_authority_callbacks_are_not_silent_success(self):
        checks = AuthorityChecks()
        self.assertIsNone(checks.verify_profile_registration)
        self.assertIsNone(checks.verify_key_status)
        self.assertIsNone(checks.verify_c_signature)
        self.assertIsNone(checks.verify_provider_evidence)


    def test_07_exact_c_schema_and_ten_vectors(self):
        fixture_dir = ROOT.parent / "fixtures"
        schema = json.loads((fixture_dir / "c-submit-outcome-1.0.0.schema.json").read_text(encoding="utf-8"))
        vectors = json.loads((fixture_dir / "c_submit_outcome_1_0_0_vectors.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual(schema["$id"], "urn:aimba:schema:c-submit-outcome:1.0.0")
        self.assertEqual(len(vectors["vectors"]), 10)
        for vector in vectors["vectors"]:
            with self.subTest(vector=vector["id"]):
                schema_errors = list(validator.iter_errors(vector["record"]))
                semantic = _semantic_errors(vector["record"])
                if vector["expected"] == "INVALID":
                    self.assertTrue(schema_errors or semantic)
                else:
                    self.assertFalse(schema_errors, [e.message for e in schema_errors])
                    self.assertFalse(semantic, semantic)

    def test_08_c_key_status_event_schema_is_closed_and_governance_scoped(self):
        fixture_dir = ROOT.parent / "fixtures"
        schema = json.loads((fixture_dir / "c-key-status-event-1.0.0.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(schema["$id"], "urn:aimba:schema:c-key-status-event:1.0.0")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["message_type"]["const"], "C_KEY_STATUS_EVENT")
        self.assertEqual(schema["properties"]["profile_id"]["const"], "AIMBA-C-CRYPTO-1.0")
        self.assertEqual(schema["properties"]["governance_signature_profile_id"]["const"], "AIMBA-I-KEY-GOVERNANCE-1.0")
        self.assertEqual(set(schema["properties"]["state"]["enum"]), {"PENDING","ACTIVE","RETIRED","REVOKED","COMPROMISED","DESTROYED"})


    def test_09_validator_is_pinned_to_unified_1_2_12(self):
        self.assertEqual(SCHEMA_ARTIFACT_REVISION, "1.2.12")
        self.assertEqual(WIRE_SCHEMA_VERSION, "1.3.0")
        schema_path = H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.12.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertTrue(schema["$id"].endswith("/1.2.12"))
        provider_branch = next(
            branch for branch in schema["oneOf"]
            if any(part.get("properties", {}).get("message_type", {}).get("const") == "C_PROVIDER_OUTCOME_RECORDED"
                   for part in branch.get("allOf", []))
        )
        properties = {}
        required = set()
        for part in provider_branch["allOf"]:
            properties.update(part.get("properties", {}))
            required.update(part.get("required", []))
        self.assertTrue({"c_submit_outcome_ref", "c_submit_outcome_digest", "provider_outcome",
                         "provider_request_ref", "provider_receipt_ref", "owner_admission_ref"}.issubset(properties))
        self.assertIn("c_submit_outcome_ref", required)
        self.assertIn("c_submit_outcome_digest", required)
        self.assertIn("owner_admission_ref", required)

    def test_10_legacy_1_2_11_is_not_the_current_validator_revision(self):
        self.assertNotEqual(SCHEMA_ARTIFACT_REVISION, "1.2.11")

if __name__ == "__main__":
    unittest.main(verbosity=2)
