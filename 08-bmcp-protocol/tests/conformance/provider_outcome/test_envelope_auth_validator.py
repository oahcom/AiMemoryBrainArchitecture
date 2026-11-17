import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve()
H_ROOT = ROOT.parents[3]
sys.path.insert(0, str(H_ROOT / "validators"))

from envelope_auth_validator import (  # noqa: E402
    EnvelopeAuthChecks,
    ProtectedTransportContext,
    ReplayCheck,
    ReplayDecision,
    authenticate_outer_envelope,
    validate_authenticated_provider_outcome,
    outer_envelope_digest_and_preimage,
)
from provider_outcome_validator import AuthorityChecks  # noqa: E402


class OuterEnvelopeAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.context = ProtectedTransportContext(
            issuer_ref="C/authority/agent-runtime",
            authority_ref="C/authority/agent-runtime",
            authority_kind="C",
            subject_ref="C/adapter/adapter-7",
            audience="COC/provider-outcome-validator",
            runtime_session_ref="H/session/runtime-7",
            authentication_context_ref="I/auth-context/7",
            channel_binding_proof_ref="C/channel-binding/test",
        )
        self.envelope = {
            "schema_id": "bmcp.coc-jf10-unified",
            "schema_artifact_revision": "1.2.14",
            "schema_version": "1.3.0",
            "message_type": "C_PROVIDER_OUTCOME_RECORDED",
            "owner_record_ref": "C/outcome/record-7",
            "causal_order_profile_ref": "CausalOrderProfile/1.0",
            "causal_order_coordinator_ref": "COC/coordinator/1",
            "causal_order_domain_ref": "COC/domain/provider-outcome",
            "created_at": "2026-11-17T12:00:00Z",
            "owner_signature_ref": "C/signature/envelope-7",
            "message_id": "msg/h-envelope/CPO-01-accepted",
            "message_nonce": "nonce/h-envelope/CPO-01-accepted-0123456789",
            "audience": "COC/provider-outcome-validator",
            "issuer_ref": "C/authority/agent-runtime",
            "sender_authority_ref": "C/authority/agent-runtime",
            "sender_subject_ref": "C/adapter/adapter-7",
            "subject_ref": "C/adapter/adapter-7",
            "owner_authority": "C",
            "canonicalization_profile_id": "RFC8785-JCS-1.0",
            "signature_profile_id": "AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0",
            "digest_algorithm": "SHA-256",
            "payload_digest": "0" * 64,
            "integrity_proof_ref": "C/integrity-proof/test",
            "channel_binding_proof_ref": "C/channel-binding/test",
            "key_id_ref": "C/key/test-only",
            "key_version": "test-v1",
            "signature": "TEST-ONLY-SIGNATURE",
        }

    def checks(self):
        return EnvelopeAuthChecks(
            verify_envelope_integrity=lambda raw, env, ctx: True,
            verify_key_status=lambda env, ctx: True,
            verify_channel_binding=lambda env, ctx: True,
            verify_identity_binding=lambda env, ctx: True,
            check_and_reserve_replay=lambda env, ctx: ReplayCheck(ReplayDecision.NEW),
        )

    def raw(self, refresh_digest=True):
        if refresh_digest:
            self.envelope["payload_digest"] = outer_envelope_digest_and_preimage(self.envelope)[0]
        return json.dumps(self.envelope, separators=(",", ":"), sort_keys=True).encode("utf-8")

    def test_01_new_envelope_authenticates_only_with_protected_context_and_all_verifiers(self):
        result = authenticate_outer_envelope(self.raw(), self.context, self.checks())
        self.assertEqual(result["status"], "AUTHENTICATED_NEW", result)

    def test_02_duplicate_json_members_are_invalid_before_auth_callbacks(self):
        raw = b'{"message_id":"a","message_id":"b"}'
        result = authenticate_outer_envelope(raw, self.context, self.checks())
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("DuplicateJSONKey", result["errors"][0])

    def test_03_missing_protected_transport_context_is_unknown(self):
        result = authenticate_outer_envelope(self.raw(), None, self.checks())
        self.assertEqual(result["status"], "UNKNOWN", result)

    def test_04_payload_issuer_subject_audience_and_channel_claims_cannot_override_context(self):
        for field, value in (
            ("issuer_ref", "C/authority/attacker"),
            ("sender_authority_ref", "C/authority/attacker"),
            ("sender_subject_ref", "C/adapter/attacker"),
            ("audience", "COC/other-service"),
            ("channel_binding_proof_ref", "C/channel-binding/other-session"),
        ):
            with self.subTest(field=field):
                self.envelope[field] = value
                result = authenticate_outer_envelope(self.raw(), self.context, self.checks())
                self.assertEqual(result["status"], "INVALID", result)
                self.envelope[field] = {
                    "issuer_ref": "C/authority/agent-runtime",
                    "sender_authority_ref": "C/authority/agent-runtime",
                    "sender_subject_ref": "C/adapter/adapter-7",
                    "subject_ref": "C/adapter/adapter-7",
                    "audience": "COC/provider-outcome-validator",
                    "channel_binding_proof_ref": "C/channel-binding/test",
                    "owner_authority": "C",
                }[field]

    def test_05_signature_or_digest_contradiction_is_invalid(self):
        checks = self.checks()
        checks.verify_envelope_integrity = lambda raw, env, ctx: False
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_06_unavailable_key_status_is_unknown(self):
        checks = self.checks()
        checks.verify_key_status = lambda env, ctx: None
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "UNKNOWN", result)

    def test_07_channel_binding_contradiction_is_invalid(self):
        checks = self.checks()
        checks.verify_channel_binding = lambda env, ctx: False
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_08_identity_registry_contradiction_is_invalid(self):
        checks = self.checks()
        checks.verify_identity_binding = lambda env, ctx: False
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_09_missing_any_required_verifier_is_unknown(self):
        checks = self.checks()
        checks.verify_envelope_integrity = None
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "UNKNOWN", result)

    def test_10_same_digest_replay_returns_prior_result_without_reprocessing(self):
        checks = self.checks()
        checks.check_and_reserve_replay = lambda env, ctx: ReplayCheck(
            ReplayDecision.SAME_DIGEST_REPLAY, "H/replay-result/17"
        )
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "IDEMPOTENT_REPLAY", result)
        self.assertEqual(result["prior_result_ref"], "H/replay-result/17")

    def test_11_reused_message_identity_with_changed_digest_is_invalid(self):
        checks = self.checks()
        checks.check_and_reserve_replay = lambda env, ctx: ReplayCheck(ReplayDecision.CONFLICT)
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_12_unavailable_replay_ledger_is_unknown(self):
        checks = self.checks()
        checks.check_and_reserve_replay = lambda env, ctx: ReplayCheck(ReplayDecision.UNKNOWN)
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "UNKNOWN", result)

    def test_13_authenticated_provider_entrypoint_never_calls_domain_validator_before_auth(self):
        checks = self.checks()
        checks.verify_envelope_integrity = lambda raw, env, ctx: False
        with patch("envelope_auth_validator.validate_provider_outcome") as downstream:
            result = validate_authenticated_provider_outcome(
                self.raw(), b'{}', self.context, checks, {}, {}, AuthorityChecks()
            )
        self.assertEqual(result["status"], "INVALID")
        downstream.assert_not_called()

    def test_14_authenticated_provider_entrypoint_calls_domain_validator_only_after_auth(self):
        with patch(
            "envelope_auth_validator.validate_provider_outcome",
            return_value={"status": "VALID", "errors": [], "unknown": []},
        ) as downstream:
            result = validate_authenticated_provider_outcome(
                self.raw(), b'{"record_ref":"C/outcome/1"}', self.context,
                self.checks(), {}, {}, AuthorityChecks()
            )
        downstream.assert_called_once()
        self.assertEqual(result["status"], "VALID")
        self.assertTrue(result["outer_envelope_authenticated"])

    def test_15_replay_reservation_is_not_attempted_before_authentication(self):
        from unittest.mock import Mock

        checks = self.checks()
        replay = Mock(return_value=ReplayCheck(ReplayDecision.NEW))
        checks.verify_envelope_integrity = lambda raw, env, ctx: False
        checks.check_and_reserve_replay = replay
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)
        replay.assert_not_called()

    def test_16_replay_reservation_is_not_attempted_when_key_status_is_unknown(self):
        from unittest.mock import Mock

        checks = self.checks()
        replay = Mock(return_value=ReplayCheck(ReplayDecision.NEW))
        checks.verify_key_status = lambda env, ctx: None
        checks.check_and_reserve_replay = replay
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "UNKNOWN", result)
        replay.assert_not_called()

    def test_17_gateway_signer_may_transport_c_owned_record_only_if_registry_allows(self):
        gateway_context = ProtectedTransportContext(
            issuer_ref="H/gateway/issuer",
            authority_ref="H/gateway/authority",
            authority_kind="H",
            subject_ref="H/gateway/instance-7",
            audience=self.context.audience,
            runtime_session_ref="H/session/gateway-7",
            authentication_context_ref="I/auth-context/gateway-7",
            channel_binding_proof_ref=self.context.channel_binding_proof_ref,
        )
        self.envelope["issuer_ref"] = "H/gateway/issuer"
        self.envelope["sender_authority_ref"] = "H/gateway/authority"
        self.envelope["sender_subject_ref"] = "H/gateway/instance-7"
        self.envelope["subject_ref"] = "C/authority/agent-runtime"
        self.envelope["owner_authority"] = "C"
        result = authenticate_outer_envelope(self.raw(), gateway_context, self.checks())
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("authenticated C origin principal", result["errors"][0])

    def test_18_subject_and_owner_authority_are_checked_by_registry_not_sender_string_equality(self):
        self.envelope["subject_ref"] = "C/subject/unauthorized"
        self.envelope["owner_authority"] = "D"
        checks = self.checks()
        checks.verify_identity_binding = lambda env, ctx: (
            env.get("subject_ref") == "C/subject/authorized"
            and env.get("owner_authority") == "C"
        )
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_19_signature_profile_id_is_required_and_cannot_fall_back_to_canonicalization_profile(self):
        self.envelope.pop("signature_profile_id")
        self.assertTrue(self.envelope["canonicalization_profile_id"])
        # Do not recompute a P0 whose required signature_profile_id is absent;
        # serialize the malformed envelope so the validator returns INVALID.
        result = authenticate_outer_envelope(self.raw(refresh_digest=False), self.context, self.checks())
        self.assertEqual(result["status"], "INVALID", result)
        self.assertTrue(any("signature_profile_id" in error for error in result["errors"]))

    def test_20_unregistered_signature_profile_is_not_accepted(self):
        checks = self.checks()
        checks.verify_envelope_integrity = lambda raw, env, ctx: (
            env.get("signature_profile_id") == "I-APPROVED-TEST-PROFILE"
        )
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_21_unavailable_signature_profile_registry_is_unknown(self):
        checks = self.checks()
        checks.verify_envelope_integrity = lambda raw, env, ctx: None
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "UNKNOWN", result)

    def test_22_outer_p0_digest_is_recomputed_before_signature_callback(self):
        self.envelope["message_id"] = "msg/tampered"
        called = []
        checks = self.checks()
        checks.verify_envelope_integrity = lambda raw, env, ctx: called.append(True) or True
        result = authenticate_outer_envelope(self.raw(refresh_digest=False), self.context, checks)
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("outer-envelope payload_digest mismatch", result["errors"])
        self.assertEqual(called, [])

    def test_23_outer_p0_binds_integrity_and_channel_binding_references(self):
        digest, _ = outer_envelope_digest_and_preimage(self.envelope)
        self.envelope["integrity_proof_ref"] = "C/integrity-proof/attacker"
        changed_integrity, _ = outer_envelope_digest_and_preimage(self.envelope)
        self.assertNotEqual(digest, changed_integrity)
        self.envelope["integrity_proof_ref"] = "C/integrity-proof/test"
        self.envelope["channel_binding_proof_ref"] = "C/channel-binding/attacker"
        changed_channel, _ = outer_envelope_digest_and_preimage(self.envelope)
        self.assertNotEqual(digest, changed_channel)

    def test_24_coordinator_appended_coc_fields_are_excluded_from_c_origin_p0(self):
        digest, _ = outer_envelope_digest_and_preimage(self.envelope)
        self.envelope["coc_commit_proof_ref"] = "COC/commit/1"
        self.envelope["coc_record_ref"] = "COC/record/1"
        self.envelope["coc_record_position"] = "COC/position/1"
        self.envelope["coc_entry_digest"] = "b" * 64
        after_append, _ = outer_envelope_digest_and_preimage(self.envelope)
        self.assertEqual(digest, after_append)

    def test_25_unknown_outer_envelope_member_is_rejected(self):
        self.envelope["unclassified_extension"] = "must-not-be-ignored"
        result = authenticate_outer_envelope(self.raw(refresh_digest=False), self.context, self.checks())
        self.assertEqual(result["status"], "INVALID", result)
        self.assertTrue(any("unclassified outer-envelope members" in e for e in result["errors"]))

    def test_26_wrong_outer_signature_profile_is_rejected_before_crypto_callback(self):
        self.envelope["signature_profile_id"] = "AIMBA-C-CRYPTO-1.0"
        result = authenticate_outer_envelope(self.raw(refresh_digest=False), self.context, self.checks())
        self.assertEqual(result["status"], "INVALID", result)
        self.assertTrue(any("wrong C outer-envelope signature_profile_id" in e for e in result["errors"]))

    def test_27_signature_callback_receives_exact_candidate_preimage(self):
        expected_digest, expected_preimage = outer_envelope_digest_and_preimage(self.envelope)
        self.envelope["payload_digest"] = expected_digest
        seen = {}
        checks = self.checks()
        checks.verify_envelope_signature = lambda env, preimage, ctx: seen.update({"preimage": preimage}) or True
        result = authenticate_outer_envelope(self.raw(), self.context, checks)
        self.assertEqual(result["status"], "AUTHENTICATED_NEW", result)
        self.assertEqual(seen["preimage"], expected_preimage)

    def test_28_non_c_transport_principal_cannot_sign_c_origin_message(self):
        gateway_context = ProtectedTransportContext(
            issuer_ref="H/gateway/issuer",
            authority_ref="H/gateway/authority",
            authority_kind="H",
            subject_ref="H/gateway/instance-7",
            audience=self.context.audience,
            runtime_session_ref="H/session/gateway-7",
            authentication_context_ref="I/auth-context/gateway-7",
            channel_binding_proof_ref=self.context.channel_binding_proof_ref,
        )
        self.envelope["issuer_ref"] = gateway_context.issuer_ref
        self.envelope["sender_authority_ref"] = gateway_context.authority_ref
        self.envelope["sender_subject_ref"] = gateway_context.subject_ref
        result = authenticate_outer_envelope(self.raw(), gateway_context, self.checks())
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("authenticated C origin principal", result["errors"][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
