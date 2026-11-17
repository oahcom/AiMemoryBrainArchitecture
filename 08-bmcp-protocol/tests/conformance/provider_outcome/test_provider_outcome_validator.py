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
    validate_provider_outcome,
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
                if vector["expected"] == "INVALID":
                    self.assertTrue(
                        schema_errors or vector["id"] in ("CPO-09-highwater-exceeded", "CPO-10-request-digest-conflict")
                    )
                else:
                    self.assertFalse(schema_errors, [e.message for e in schema_errors])

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


    def test_10_validator_is_pinned_to_unified_1_2_14(self):
        self.assertEqual(SCHEMA_ARTIFACT_REVISION, "1.2.14")
        self.assertEqual(WIRE_SCHEMA_VERSION, "1.3.0")
        schema_path = H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.14.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertTrue(schema["$id"].endswith("/1.2.14"))
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
    def test_09_c_submit_outcome_1_0_1_schema_requires_sequence_namespace(self):
        fixture_dir = ROOT.parent / "fixtures"
        schema = json.loads((fixture_dir / "c-submit-outcome-1.0.1.schema.json").read_text(encoding="utf-8"))
        vectors = json.loads((fixture_dir / "c_submit_outcome_1_0_1_vectors.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual(schema["$id"], "urn:aimba:schema:c-submit-outcome:1.0.1")
        self.assertIn("sequence_namespace_ref", schema["required"])
        for vector in vectors["vectors"]:
            self.assertEqual(vector["record"]["sequence_namespace_ref"], "C/sequencer/provider-outcome")
            if vector["expected"] != "INVALID":
                self.assertFalse(list(validator.iter_errors(vector["record"])))


    def test_12_unified_1_2_13_removes_ambiguous_intent_alias_and_corrects_rejected_branch(self):
        schema_path = H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.13.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["const"], "1.2.13")
        self.assertIn("1.2.13", schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["description"])

        provider_branch = next(
            branch for branch in schema["oneOf"]
            if any(part.get("properties", {}).get("message_type", {}).get("const") == "C_PROVIDER_OUTCOME_RECORDED"
                   for part in branch.get("allOf", []))
        )
        properties = {}
        for part in provider_branch.get("allOf", []):
            properties.update(part.get("properties", {}))
        self.assertIn("coc_participant_intent_ref", properties)
        self.assertNotIn("participant_intent_ref", properties)

        def walk(value):
            if isinstance(value, dict):
                yield value
                for child in value.values():
                    yield from walk(child)
            elif isinstance(value, list):
                for child in value:
                    yield from walk(child)

        rejected_rules = [
            node for node in walk(provider_branch)
            if node.get("if", {}).get("properties", {}).get("provider_outcome", {}).get("const") == "HANDOFF_REJECTED"
        ]
        self.assertTrue(rejected_rules)
        required_sets = [set(node.get("then", {}).get("required", [])) for node in rejected_rules]
        self.assertTrue(any({"provider_request_ref", "provider_outcome_evidence_ref"}.issubset(req)
                            and "provider_no_handoff_proof_ref" not in req for req in required_sets))

    def test_13_rejected_outcome_proof_is_conditional_on_side_effect_status(self):
        base = {
            "sequence_namespace_ref": "C/sequencer/provider-outcome",
            "COwnerLocalSequence": "41",
            "COwnerHighWater": "41",
            "COCParticipantIntentRef": "COC/intent/41",
            "COCParticipantReservationRef": "COC/reservation/41",
            "COCAbsenceReason": None,
            "Outcome": "HANDOFF_REJECTED",
            "SideEffectStatus": "POSSIBLE_OR_UNKNOWN",
        }
        self.assertEqual(_semantic_errors(base), [])

        occurred = dict(base, SideEffectStatus="PROVEN_OCCURRED")
        self.assertEqual(_semantic_errors(occurred), [])

        no_side_effect = dict(base, SideEffectStatus="PROVEN_NONE")
        errors = _semantic_errors(no_side_effect)
        self.assertTrue(any("rejected-as-no-side-effect" in error for error in errors))

        # HANDOFF_REJECTED + PROVEN_NONE needs an authoritative no-handoff
        # proof, but it is not the same outcome as NOT_INVOKED and therefore
        # does not require NotInvokedProofRef.
        proven_none = dict(
            no_side_effect,
            ProviderNoHandoffProofRef="C/no-handoff/41",
        )
        self.assertEqual(_semantic_errors(proven_none), [])

        # NOT_INVOKED remains stricter and requires both proofs.
        not_invoked = dict(
            no_side_effect,
            Outcome="NOT_INVOKED",
            ProviderNoHandoffProofRef="C/no-handoff/41",
            NotInvokedProofRef="C/not-invoked/41",
        )
        self.assertEqual(_semantic_errors(not_invoked), [])
        missing_not_invoked_proof = dict(
            no_side_effect,
            Outcome="NOT_INVOKED",
            ProviderNoHandoffProofRef="C/no-handoff/41",
        )
        self.assertTrue(_semantic_errors(missing_not_invoked_proof))

    def test_14_wire_mapping_does_not_accept_legacy_participant_intent_alias(self):
        from provider_outcome_validator import WIRE_TO_C
        self.assertNotIn("participant_intent_ref", WIRE_TO_C)
        self.assertEqual(WIRE_TO_C["coc_participant_intent_ref"], "COCParticipantIntentRef")
        self.assertEqual(WIRE_TO_C["c_submit_outcome_digest"], "payload_digest")

    def test_15_wrong_loaded_schema_uris_are_rejected(self):
        result = validate_provider_outcome(
            envelope={},
            c_object={},
            envelope_schema={"$id": "urn:wrong:bmcp"},
            c_object_schema={"$id": "urn:wrong:c-object"},
            checks=AuthorityChecks(),
        )
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("wrong BMCP schema_id", result["errors"])
        self.assertIn("wrong loaded BMCP schema artifact URI", result["errors"])
        self.assertIn("wrong loaded C object schema artifact URI", result["errors"])



    def test_15_unified_1_2_14_binds_d_forget_fence_generation(self):
        schema_path = H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.14.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["const"], "1.2.14")
        d_highwaters = schema["$defs"]["ownerSpecificHighWatersD"]
        self.assertIn("forget_fence_generation_high_water", d_highwaters["required"])
        self.assertIn("barrier_generation", d_highwaters["required"])
        self.assertIn("barrier_generation", d_highwaters["properties"])
        self.assertIn("owner_gate_generation", schema["$defs"]["ownerSnapshot"]["properties"])
        self.assertNotIn("forget_fence_generation_high_water", schema["$defs"]["ownerSnapshot"]["properties"])
        self.assertEqual(d_highwaters["properties"]["forget_fence_generation_high_water"]["type"], "string")

if __name__ == "__main__":
    unittest.main(verbosity=2)

    def test_15_unified_1_2_14_binds_d_forget_fence_generation(self):
        schema_path = H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.14.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["const"], "1.2.14")
        d_highwaters = schema["$defs"]["ownerSpecificHighWatersD"]
        self.assertIn("forget_fence_generation_high_water", d_highwaters["required"])
        self.assertIn("barrier_generation", d_highwaters["required"])
        self.assertIn("barrier_generation", d_highwaters["properties"])\n        self.assertIn("owner_gate_generation", schema["$defs"]["ownerSnapshot"]["properties"])\n        self.assertNotIn("forget_fence_generation_high_water", schema["$defs"]["ownerSnapshot"]["properties"])
        self.assertEqual(d_highwaters["properties"]["forget_fence_generation_high_water"]["type"], "string")
