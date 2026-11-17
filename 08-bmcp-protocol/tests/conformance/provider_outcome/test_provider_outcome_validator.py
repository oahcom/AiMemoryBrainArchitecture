"""Unit tests for H's fail-closed C Provider Outcome validator core.

These tests cover parsing and deterministic local predicates only. They do not
claim profile registration, signature/key verification, provider truth, ledger
membership, COC quorum, cross-language interoperability or production readiness.
"""
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
)


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
        self.assertIsNone(checks.verify_c_signature)
        self.assertIsNone(checks.verify_provider_evidence)


if __name__ == "__main__":
    unittest.main(verbosity=2)
