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
from unittest.mock import patch


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


    def test_07_current_c_schema_and_ten_vectors(self):
        fixture_dir = ROOT.parent / "fixtures"
        schema = json.loads((fixture_dir / "c-submit-outcome-1.0.1.schema.json").read_text(encoding="utf-8"))
        vectors = json.loads((fixture_dir / "c_submit_outcome_1_0_1_vectors.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual(schema["$id"], "urn:aimba:schema:c-submit-outcome:1.0.1")
        self.assertEqual(len(vectors["vectors"]), 11)
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


    def test_12_current_unified_1_2_14_removes_ambiguous_intent_alias_and_corrects_rejected_branch(self):
        schema_path = H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.14.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["const"], "1.2.14")
        self.assertIn("1.2.14", schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["description"])

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


    def test_16_owner_authority_proofs_have_independent_verifier_seams(self):
        checks = AuthorityChecks()
        self.assertIsNone(checks.verify_i_terminal_decision)
        self.assertIsNone(checks.verify_d_clearance)
        self.assertIsNone(checks.verify_storage_resolution_proof)

    def test_17_full_validator_accepts_only_after_separate_i_d_storage_checks(self):
        digest = "a" * 64
        envelope_schema = {"$id": "https://schemas.aimemorybrainarchitecture.invalid/bmcp.coc-jf10-unified/1.2.14"}
        c_schema = {"$id": "urn:aimba:schema:c-submit-outcome:1.0.1"}
        envelope = {
            "schema_id": "bmcp.coc-jf10-unified",
            "schema_artifact_revision": "1.2.14",
            "schema_version": "1.3.0",
            "message_type": "C_PROVIDER_OUTCOME_RECORDED",
            "c_submit_outcome_ref": "C/outcome/1",
            "c_submit_outcome_digest": digest,
        }
        c_object = {
            "schema_id": "CSubmitOutcome",
            "schema_version": "1.0.1",
            "schema_artifact_revision": "1.0.1",
            "signature_profile_id": "AIMBA-C-CRYPTO-1.0",
            "message_type": "C_PROVIDER_OUTCOME_RECORDED",
            "record_ref": "C/outcome/1",
            "payload_digest": digest,
        }
        callbacks = {
            "verify_profile_registration": lambda record: True,
            "verify_key_status": lambda record: True,
            "verify_c_signature": lambda record, preimage: True,
            "verify_provider_evidence": lambda wire, record: True,
            "verify_owner_ledger": lambda wire, record: True,
            "verify_coc_join": lambda wire, record: True,
            "verify_currentness": lambda wire, record: True,
            "verify_i_terminal_decision": lambda wire, record: True,
            "verify_d_clearance": lambda wire, record: True,
            "verify_storage_resolution_proof": lambda wire, record: True,
        }
        checks = AuthorityChecks(**callbacks)
        with patch("provider_outcome_validator._schema_errors", return_value=[]), patch("provider_outcome_validator._semantic_errors", return_value=[]), patch("provider_outcome_validator._candidate_digest_and_preimage", return_value=(digest, b"test-preimage")):
            result = validate_provider_outcome(envelope, c_object, envelope_schema, c_schema, checks)
        self.assertEqual(result["status"], "VALID", result)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["unknown"], [])

    def test_18_missing_i_d_or_storage_authority_is_unknown_not_valid(self):
        digest = "a" * 64
        envelope_schema = {"$id": "https://schemas.aimemorybrainarchitecture.invalid/bmcp.coc-jf10-unified/1.2.14"}
        c_schema = {"$id": "urn:aimba:schema:c-submit-outcome:1.0.1"}
        envelope = {
            "schema_id": "bmcp.coc-jf10-unified",
            "schema_artifact_revision": "1.2.14",
            "schema_version": "1.3.0",
            "message_type": "C_PROVIDER_OUTCOME_RECORDED",
            "c_submit_outcome_ref": "C/outcome/1",
            "c_submit_outcome_digest": digest,
        }
        c_object = {
            "schema_id": "CSubmitOutcome",
            "schema_version": "1.0.1",
            "schema_artifact_revision": "1.0.1",
            "signature_profile_id": "AIMBA-C-CRYPTO-1.0",
            "message_type": "C_PROVIDER_OUTCOME_RECORDED",
            "record_ref": "C/outcome/1",
            "payload_digest": digest,
        }
        callbacks = {
            "verify_profile_registration": lambda record: True,
            "verify_key_status": lambda record: True,
            "verify_c_signature": lambda record, preimage: True,
            "verify_provider_evidence": lambda wire, record: True,
            "verify_owner_ledger": lambda wire, record: True,
            "verify_coc_join": lambda wire, record: True,
            "verify_currentness": lambda wire, record: True,
        }
        checks = AuthorityChecks(**callbacks)
        with patch("provider_outcome_validator._schema_errors", return_value=[]), patch("provider_outcome_validator._semantic_errors", return_value=[]), patch("provider_outcome_validator._candidate_digest_and_preimage", return_value=(digest, b"test-preimage")):
            result = validate_provider_outcome(envelope, c_object, envelope_schema, c_schema, checks)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(len(result["unknown"]), 3)
        self.assertTrue(any("I terminal decision" in item for item in result["unknown"]))
        self.assertTrue(any("D Forget clearance" in item for item in result["unknown"]))
        self.assertTrue(any("Storage resolution proof" in item for item in result["unknown"]))



    def test_19_exact_current_bundle_and_owner_authority_seams(self):
        fixture_dir = ROOT.parent / "fixtures"
        c_schema = json.loads((fixture_dir / "c-submit-outcome-1.0.1.schema.json").read_text(encoding="utf-8"))
        h_schema = json.loads((H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.14.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(c_schema["$id"], "urn:aimba:schema:c-submit-outcome:1.0.1")
        self.assertEqual(h_schema["$defs"]["commonEnvelope"]["properties"]["schema_artifact_revision"]["const"], "1.2.14")
        self.assertEqual(SCHEMA_ARTIFACT_REVISION, "1.2.14")
        self.assertEqual(WIRE_SCHEMA_VERSION, "1.3.0")
        from provider_outcome_validator import C_OBJECT_SCHEMA_URI, C_PROFILE_ID, BMCP_SCHEMA_URI, AuthorityChecks
        self.assertEqual(C_OBJECT_SCHEMA_URI, "urn:aimba:schema:c-submit-outcome:1.0.1")
        self.assertEqual(BMCP_SCHEMA_URI, h_schema["$id"])
        self.assertEqual(C_PROFILE_ID, "AIMBA-C-CRYPTO-1.0")
        checks = AuthorityChecks()
        self.assertIsNone(checks.verify_i_terminal_decision)
        self.assertIsNone(checks.verify_d_clearance)
        self.assertIsNone(checks.verify_storage_resolution_proof)

    def test_20_current_c_sequence_namespace_is_required_and_schema_is_closed(self):
        fixture_dir = ROOT.parent / "fixtures"
        schema = json.loads((fixture_dir / "c-submit-outcome-1.0.1.schema.json").read_text(encoding="utf-8"))
        self.assertIn("sequence_namespace_ref", schema["required"])
        self.assertIn("sequence_namespace_ref", schema["properties"])
        self.assertFalse(schema["additionalProperties"])



    def _full_validator_fixture(self):
        fixture_dir = ROOT.parent / "fixtures"
        fixture = json.loads(
            (fixture_dir / "h-full-provider-outcome-positive-1.0.1.json").read_text(encoding="utf-8")
        )
        envelope_schema = json.loads(
            (H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.14.schema.json").read_text(encoding="utf-8")
        )
        c_object_schema = json.loads(
            (fixture_dir / "c-submit-outcome-1.0.1.schema.json").read_text(encoding="utf-8")
        )
        checks = AuthorityChecks(
            verify_profile_registration=lambda record: True,
            verify_key_status=lambda record: True,
            verify_c_signature=lambda record, preimage: True,
            verify_provider_evidence=lambda envelope, record: True,
            verify_owner_ledger=lambda envelope, record: True,
            verify_coc_join=lambda envelope, record: True,
            verify_currentness=lambda envelope, record: True,
            verify_i_terminal_decision=lambda envelope, record: True,
            verify_d_clearance=lambda envelope, record: True,
            verify_storage_resolution_proof=lambda envelope, record: True,
        )
        return fixture["envelope"], fixture["c_submit_outcome"], envelope_schema, c_object_schema, checks

    def test_21_full_unmocked_schema_semantics_and_digest_path_is_valid(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "VALID", result)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["unknown"], [])

    def test_22_full_path_rejects_wire_object_duplicate_mismatch(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        envelope["provider_ref"] = "Provider/attacker"
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertTrue(any("wire/object mismatch: provider_ref" in item for item in result["errors"]))

    def test_23_full_path_recomputes_c_payload_digest(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        c_object["payload_digest"] = "0" * 64
        envelope["c_submit_outcome_digest"] = "0" * 64
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("C payload_digest mismatch", result["errors"])

    def test_24_full_path_missing_i_d_storage_verifiers_is_unknown(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        checks.verify_i_terminal_decision = None
        checks.verify_d_clearance = None
        checks.verify_storage_resolution_proof = None
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "UNKNOWN", result)
        self.assertEqual(len(result["unknown"]), 3)

    def test_25_full_path_i_d_storage_contradictions_are_invalid(self):
        for callback_name in (
            "verify_i_terminal_decision",
            "verify_d_clearance",
            "verify_storage_resolution_proof",
        ):
            with self.subTest(callback=callback_name):
                envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
                setattr(checks, callback_name, lambda *args: False)
                result = validate_provider_outcome(
                    envelope, c_object, envelope_schema, c_object_schema, checks
                )
                self.assertEqual(result["status"], "INVALID", result)


    def test_26_full_path_rejects_every_present_duplicated_wire_field_mutation(self):
        from provider_outcome_validator import WIRE_TO_C
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        present = [
            (wire_name, object_name)
            for wire_name, object_name in WIRE_TO_C.items()
            if wire_name in envelope and object_name in c_object and c_object[object_name] is not None
        ]
        self.assertGreaterEqual(len(present), 18)
        for wire_name, object_name in present:
            with self.subTest(wire_field=wire_name, object_field=object_name):
                mutated_envelope, mutated_object, h_schema, c_schema, callbacks = self._full_validator_fixture()
                original = mutated_envelope[wire_name]
                if wire_name == "provider_outcome":
                    mutated = "HANDOFF_REJECTED"
                elif isinstance(original, str) and len(original) == 64:
                    mutated = "0" * 64 if original != "0" * 64 else "1" * 64
                else:
                    mutated = str(original) + "/tampered"
                mutated_envelope[wire_name] = mutated
                result = validate_provider_outcome(
                    mutated_envelope, mutated_object, h_schema, c_schema, callbacks
                )
                self.assertEqual(result["status"], "INVALID", result)

    def test_27_full_path_recomputes_digest_after_p0_member_and_wire_are_mutated_together(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        c_object["ProviderRef"] = "Provider/attacker"
        envelope["provider_ref"] = "Provider/attacker"
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("C payload_digest mismatch", result["errors"])

    def test_28_full_path_rejects_c_sequence_namespace_mismatch(self):
        from provider_outcome_validator import _candidate_digest_and_preimage
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        c_object["sequence_namespace_ref"] = "C/sequencer/attacker"
        digest, _ = _candidate_digest_and_preimage(c_object)
        c_object["payload_digest"] = digest
        envelope["c_submit_outcome_digest"] = digest
        checks.verify_key_status = lambda record: (
            record["sequence_namespace_ref"] == "C/sequencer/provider-outcome"
        )
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("C key status at signing sequence verification contradiction", result["errors"])

    def test_29_full_path_i_terminal_requires_commit_won(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        envelope["i_terminal_decision_ref"] = "I/terminal/REVOCATION_WON/operation-41"
        checks.verify_i_terminal_decision = lambda wire, record: (
            wire.get("i_terminal_decision_ref") == "I/terminal/COMMIT_WON/operation-41"
        )
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("I terminal decision / COMMIT_WON authority verification contradiction", result["errors"])

    def test_30_full_path_d_clearance_is_bound_to_exact_fence(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        envelope["d_clearance_ref"] = "D/clearance/other-operation/fence-20"
        checks.verify_d_clearance = lambda wire, record: (
            wire.get("d_clearance_ref") == "D/clearance/forget-op-41/fence-19"
        )
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("D Forget clearance / fence authority verification contradiction", result["errors"])

    def test_31_full_path_storage_resolution_binds_same_gid_and_prepare_attempt(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        envelope["storage_resolution_proof_ref"] = "Storage/resolution/gid/other-incarnation/gid-99"
        checks.verify_storage_resolution_proof = lambda wire, record: (
            wire.get("storage_resolution_proof_ref") == "Storage/resolution/gid/pg-inc-7/gid-41"
            and wire.get("prepare_attempt_ref") == "Storage/prepare-attempt/41"
            and wire.get("prepared_participant_ref") == "Storage/prepared-participant/41"
            and wire.get("participant_ledger_ref") == "Storage/participant-ledger/1"
        )
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("Storage resolution proof / same-GID authority verification contradiction", result["errors"])

    def test_32_c_p0_projection_covers_every_member_except_derived_digest_and_signature(self):
        from provider_outcome_validator import _p0, _candidate_digest_and_preimage

        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        p0 = _p0(c_object)
        self.assertEqual(set(p0), set(c_object) - {"payload_digest", "signature"})
        digest, _ = _candidate_digest_and_preimage(c_object)
        self.assertEqual(digest, c_object["payload_digest"])



    def test_32_every_present_c_p0_member_is_bound_by_schema_semantics_or_digest(self):
        from provider_outcome_validator import _p0, WIRE_TO_C
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        p0_fields = list(_p0(c_object))
        self.assertGreaterEqual(len(p0_fields), 60)
        inverse_wire = {object_name: wire_name for wire_name, object_name in WIRE_TO_C.items()}
        for field in p0_fields:
            with self.subTest(c_p0_field=field):
                wire, obj, h_schema, c_schema, callbacks = self._full_validator_fixture()
                original = obj[field]
                if field == "Outcome":
                    mutated = "HANDOFF_REJECTED"
                elif field == "SideEffectStatus":
                    mutated = "POSSIBLE_OR_UNKNOWN"
                elif original is None:
                    mutated = "C/tampered/" + field
                elif isinstance(original, str) and len(original) == 64 and all(ch in "0123456789abcdef" for ch in original):
                    mutated = "0" * 64 if original != "0" * 64 else "1" * 64
                elif field in ("COwnerLocalSequence", "COwnerHighWater", "record_sequence"):
                    mutated = str(int(original) + 1)
                elif isinstance(original, str):
                    mutated = original + "-tampered"
                else:
                    continue
                obj[field] = mutated
                wire_name = inverse_wire.get(field)
                if wire_name is not None and wire_name in wire:
                    wire[wire_name] = mutated
                if field == "record_ref":
                    wire["c_submit_outcome_ref"] = mutated
                if field == "Outcome":
                    wire["provider_outcome"] = mutated
                if field == "COCAbsenceReason":
                    wire["coc_absence_reason"] = mutated
                result = validate_provider_outcome(wire, obj, h_schema, c_schema, callbacks)
                self.assertEqual(result["status"], "INVALID", result)

    def test_33_not_invoked_without_coc_intent_is_valid_only_with_explicit_absence_reason(self):
        from provider_outcome_validator import _candidate_digest_and_preimage
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        c_object["Outcome"] = "NOT_INVOKED"
        c_object["SideEffectStatus"] = "PROVEN_NONE"
        c_object.pop("ProviderReceiptRef")
        c_object["ProviderNoHandoffProofRef"] = "C/no-handoff/CPO-01"
        c_object["NotInvokedProofRef"] = "C/not-invoked/CPO-01"
        c_object["COCParticipantIntentRef"] = None
        c_object["COCParticipantReservationRef"] = None
        c_object["COCAbsenceReason"] = "not-a-COC-participant"
        digest, _ = _candidate_digest_and_preimage(c_object)
        c_object["payload_digest"] = digest

        envelope["c_submit_outcome_digest"] = digest
        envelope["provider_outcome"] = "NOT_INVOKED"
        envelope.pop("provider_receipt_ref")
        envelope["provider_no_handoff_proof_ref"] = c_object["ProviderNoHandoffProofRef"]
        envelope["not_invoked_proof_ref"] = c_object["NotInvokedProofRef"]
        envelope["coc_participant_intent_ref"] = None
        envelope.pop("participant_reservation_ref")
        envelope["coc_absence_reason"] = c_object["COCAbsenceReason"]

        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "VALID", result)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["unknown"], [])

    def test_34_coc_absence_reason_null_and_absent_are_not_interchangeable(self):
        envelope, c_object, envelope_schema, c_object_schema, checks = self._full_validator_fixture()
        c_object.pop("COCAbsenceReason")
        result = validate_provider_outcome(
            envelope, c_object, envelope_schema, c_object_schema, checks
        )
        self.assertEqual(result["status"], "INVALID", result)
        self.assertTrue(any("COCAbsenceReason" in item for item in result["errors"]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
