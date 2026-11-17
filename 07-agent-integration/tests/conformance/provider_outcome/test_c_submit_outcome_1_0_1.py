"""Structural and semantic tests for CSubmitOutcome 1.0.0.

These tests deliberately do NOT verify cryptographic signatures, provider truth,
ledger inclusion, gate linearizability, or COC authority. Fixture signatures are
placeholders. A passing run is not production certification.
"""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT.parents[2] / "schemas" / "c-submit-outcome-1.0.1.schema.json"
VECTOR_PATH = ROOT / "c_submit_outcome_1_0_1_vectors.json"


def semantic_errors(record, vector):
    errors = []
    if int(record["COwnerLocalSequence"]) > int(record["COwnerHighWater"]):
        errors.append("owner sequence exceeds high-water")
    intent = record["COCParticipantIntentRef"]
    reservation = record["COCParticipantReservationRef"]
    absence_reason = record["COCAbsenceReason"]
    if intent is None:
        if reservation is not None or not absence_reason:
            errors.append("null COC intent requires null reservation and explicit reason")
    elif not isinstance(reservation, str) or not reservation or absence_reason is not None:
        errors.append("non-null COC intent requires reservation and null absence reason")
    if vector.get("wire_request_digest") is not None:
        if vector["wire_request_digest"] != record["RequestDigest"]:
            errors.append("wire request digest differs from immutable C object")
    if record["Outcome"] == "HANDOFF_ACCEPTED":
        if "ProviderReceiptRef" not in record or record["SideEffectStatus"] != "PROVEN_OCCURRED":
            errors.append("accepted outcome lacks receipt or proven side effect")
    if record["Outcome"] == "HANDOFF_REJECTED" and record["SideEffectStatus"] == "PROVEN_NONE":
        if not record.get("ProviderNoHandoffProofRef") or not record.get("NotInvokedProofRef"):
            errors.append("rejected-as-no-side-effect lacks authoritative no-handoff proof")
    if record["Outcome"] == "NOT_INVOKED":
        if not record.get("ProviderNoHandoffProofRef") or not record.get("NotInvokedProofRef"):
            errors.append("not-invoked lacks durable no-handoff proof")
    if record["Outcome"] in ("UNKNOWN", "IN_DOUBT"):
        if record["SideEffectStatus"] != "POSSIBLE_OR_UNKNOWN" or not record.get("UnknownReasonRef"):
            errors.append("unknown/in-doubt must remain nonterminal with a reason")
    return errors


class CSubmitOutcomeV101Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_01_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(self.schema["$id"], "urn:aimba:schema:c-submit-outcome:1.0.1")
        self.assertIn("sequence_namespace_ref", self.schema["required"])
        for vector in self.fixture["vectors"]:
            self.assertEqual(vector["record"]["schema_version"], "1.0.1")
            self.assertEqual(vector["record"]["schema_artifact_revision"], "1.0.1")
            self.assertEqual(vector["record"]["sequence_namespace_ref"], "C/sequencer/provider-outcome")

    def test_02_expected_outcomes_for_all_vectors(self):
        self.assertEqual(len(self.fixture["vectors"]), 10)
        for vector in self.fixture["vectors"]:
            with self.subTest(vector=vector["id"]):
                record = vector["record"]
                schema_errors = list(self.validator.iter_errors(record))
                semantic = semantic_errors(record, vector)
                if vector["expected"] == "INVALID":
                    self.assertTrue(schema_errors or semantic, "invalid vector unexpectedly accepted")
                else:
                    self.assertFalse(schema_errors, [e.message for e in schema_errors])
                    self.assertFalse(semantic, semantic)
                if vector["expected"] in ("UNKNOWN", "VALID_AS_OBSERVATION_NOT_TERMINAL"):
                    self.assertIn(record["Outcome"], ("UNKNOWN", "IN_DOUBT", "HANDOFF_REJECTED"))

    def test_03_no_vector_claims_production_crypto(self):
        self.assertEqual(self.fixture["profile_status"], "PROPOSED_NOT_REGISTERED")
        self.assertIn("NOT_CRYPTOGRAPHICALLY_VALID", self.fixture["signature_values"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
