"""Conformance tests for H Unified 1.2.15 gateway-attested ingress."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve()
H_ROOT = ROOT.parents[3]
sys.path.insert(0, str(H_ROOT / "validators"))

from envelope_auth_validator import ProtectedTransportContext  # noqa: E402
from gateway_attestation_validator import (  # noqa: E402
    DurableIngressDecision,
    GatewayAttestationChecks,
    H_PROFILE_ID,
    h_p0_digest_and_preimage,
    validate_gateway_attested_provider_outcome,
)
from provider_outcome_validator_1_2_15 import AuthorityChecks  # noqa: E402


class GatewayAttestationSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h_schema = json.loads(
            (H_ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.15.schema.json").read_text(encoding="utf-8")
        )
        cls.c_schema = json.loads(
            (ROOT.parent / "fixtures" / "c-submit-outcome-1.0.1.schema.json").read_text(encoding="utf-8")
        )
        cls.fixture = json.loads(
            (ROOT.parent / "fixtures" / "h-full-provider-outcome-positive-1.0.1.json").read_text(encoding="utf-8")
        )

    def setUp(self):
        self.c_object = copy.deepcopy(self.fixture["c_submit_outcome"])
        self.envelope = copy.deepcopy(self.fixture["envelope"])
        self.origin_bytes = b'{"message_type":"C_PROVIDER_OUTCOME_RECORDED","origin":"C-adapter-test"}'
        self.context = ProtectedTransportContext(
            issuer_ref="H/gateway/issuer-1",
            authority_ref="H/gateway/authority-1",
            authority_kind="H",
            subject_ref="H/gateway/instance-1",
            audience="COC/provider-outcome-validator",
            runtime_session_ref="H/session/receiver-1",
            authentication_context_ref="H/auth-context/receiver-1",
            channel_binding_proof_ref="H/channel-binding/downstream-1",
        )
        self.envelope.update({
            "schema_artifact_revision": "1.2.15",
            "issuer_ref": "H/gateway/issuer-1",
            "sender_authority_ref": "H/gateway/authority-1",
            "sender_subject_ref": "H/gateway/instance-1",
            "subject_ref": "C/subject/provider-outcome",
            "owner_authority": "C",
            "owner_record_ref": self.c_object["record_ref"],
            "channel_binding_proof_ref": "H/channel-binding/downstream-1",
            "key_id_ref": "H/gateway/key-1",
            "key_version": "h-gateway-v1",
            "signature_profile_id": H_PROFILE_ID,
            "origin_transport_context_ref": "H/origin-receipt/1",
            "origin_transport_context_digest": "d" * 64,
            "origin_received_bytes_digest": hashlib.sha256(self.origin_bytes).hexdigest(),
            "origin_issuer_ref": "C/authority/agent-runtime",
            "origin_sender_authority_ref": "C/authority/agent-runtime",
            "origin_sender_subject_ref": "C/adapter/adapter-7",
            "origin_authentication_context_ref": "H/origin-auth-context/1",
            "origin_channel_binding_proof_ref": "C/channel-binding/origin-1",
            "origin_received_at": "2026-11-17T08:00:00Z",
            "signing_sequence_namespace_ref": "H/gateway/signing-sequence/1",
            "signing_record_sequence": "17",
            "signature": "A" * 86,
            "integrity_proof_ref": "H/integrity-proof/1",
        })
        digest, _ = h_p0_digest_and_preimage(self.envelope)
        self.envelope["payload_digest"] = digest

    def gateway_checks(self):
        return GatewayAttestationChecks(
            verify_profile_registration=lambda env, ctx: env.get("signature_profile_id") == H_PROFILE_ID,
            verify_key_status=lambda env, ctx: (
                env.get("signing_sequence_namespace_ref") == "H/gateway/signing-sequence/1"
                and env.get("signing_record_sequence") == "17"
                and env.get("key_version") == "h-gateway-v1"
            ),
            verify_h_signature=lambda env, preimage, ctx: (
                env.get("signature") == "A" * 86
                and preimage.startswith(b"AIMBA-H-GATEWAY-ATTEST-P0\x00v1\x00")
            ),
            verify_integrity_evidence=lambda env, digest, ctx: (
                env.get("integrity_proof_ref") == "H/integrity-proof/1"
                and env.get("payload_digest") == digest
            ),
            verify_identity_binding=lambda env, ctx: (
                env.get("owner_authority") == "C"
                and env.get("issuer_ref") == ctx.issuer_ref
                and env.get("subject_ref") == "C/subject/provider-outcome"
            ),
            verify_origin_transport_receipt=lambda env, raw, obj, ctx: (
                env.get("origin_sender_subject_ref") == "C/adapter/adapter-7"
                and env.get("origin_received_bytes_digest") == hashlib.sha256(raw).hexdigest()
                and obj.get("AdapterRef") == "C/adapter/test"
            ),
            commit_authenticated_ingress=lambda env, digest, ctx: DurableIngressDecision("NEW"),
            verify_replay_disclosure_authorization=lambda env, ctx: True,
        )

    def c_checks(self):
        return AuthorityChecks(
            verify_profile_registration=lambda obj: True,
            verify_key_status=lambda obj: True,
            verify_c_signature=lambda obj, preimage: True,
            verify_provider_evidence=lambda env, obj: True,
            verify_owner_ledger=lambda env, obj: True,
            verify_coc_join=lambda env, obj: True,
            verify_currentness=lambda env, obj: True,
            verify_i_terminal_decision=lambda env, obj: True,
            verify_d_clearance=lambda env, obj: True,
            verify_storage_resolution_proof=lambda env, obj: True,
        )

    def invoke(self, gateway_checks=None, c_checks=None, raw_origin=None):
        raw_env = json.dumps(self.envelope, separators=(",", ":"), sort_keys=True).encode("utf-8")
        raw_c = json.dumps(self.c_object, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return validate_gateway_attested_provider_outcome(
            raw_env,
            raw_c,
            self.origin_bytes if raw_origin is None else raw_origin,
            self.context,
            self.gateway_checks() if gateway_checks is None else gateway_checks,
            self.h_schema,
            self.c_schema,
            self.c_checks() if c_checks is None else c_checks,
        )

    def test_01_complete_1_2_15_gateway_attestation_and_c_object_validate(self):
        result = self.invoke()
        self.assertEqual(result["status"], "VALID", result)
        self.assertTrue(result["h_gateway_attestation_authenticated"])
        self.assertTrue(result["durable_ingress_committed"])
        self.assertEqual(result["h_p0_digest"], self.envelope["payload_digest"])

    def test_02_schema_revision_must_be_exact_1_2_15(self):
        self.envelope["schema_artifact_revision"] = "1.2.14"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

    def test_03_each_new_conditional_origin_field_is_required(self):
        required = (
            "signature_profile_id",
            "origin_transport_context_ref",
            "origin_transport_context_digest",
            "origin_received_bytes_digest",
            "origin_issuer_ref",
            "origin_sender_authority_ref",
            "origin_sender_subject_ref",
            "origin_authentication_context_ref",
            "origin_channel_binding_proof_ref",
            "origin_received_at",
            "signing_sequence_namespace_ref",
            "signing_record_sequence",
        )
        for field in required:
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.envelope)
                candidate.pop(field)
                old = self.envelope
                self.envelope = candidate
                result = self.invoke()
                self.assertEqual(result["status"], "INVALID", result)
                self.envelope = old

    def test_04_owner_authority_must_remain_c(self):
        self.envelope["owner_authority"] = "H"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

    def test_05_digest_encoding_and_origin_raw_bytes_are_exact(self):
        self.envelope["origin_transport_context_digest"] = "z" * 64
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

        self.setUp()
        result = self.invoke(raw_origin=b'{"different":"bytes"}')
        self.assertEqual(result["status"], "INVALID", result)

    def test_06_signing_sequence_must_be_decimal_string(self):
        self.envelope["signing_record_sequence"] = "17x"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

    def test_07_wrong_profile_or_unavailable_registry_fails_closed(self):
        self.envelope["signature_profile_id"] = "AIMBA-C-CRYPTO-1.0"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

        self.setUp()
        checks = self.gateway_checks()
        checks.verify_profile_registration = lambda env, ctx: None
        result = self.invoke(gateway_checks=checks)
        self.assertEqual(result["status"], "UNKNOWN", result)

    def test_08_invalid_h_signature_never_commits_ingress(self):
        checks = self.gateway_checks()
        checks.verify_h_signature = lambda env, preimage, ctx: False
        commits = []
        checks.commit_authenticated_ingress = lambda env, digest, ctx: commits.append(True) or DurableIngressDecision("NEW")
        result = self.invoke(gateway_checks=checks)
        self.assertEqual(result["status"], "INVALID", result)
        self.assertEqual(commits, [])

    def test_09_origin_transport_mismatch_is_invalid(self):
        checks = self.gateway_checks()
        checks.verify_origin_transport_receipt = lambda env, raw, obj, ctx: False
        result = self.invoke(gateway_checks=checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_10_c_signature_must_be_valid_independently_of_h_signature(self):
        checks = self.c_checks()
        checks.verify_c_signature = lambda obj, preimage: False
        result = self.invoke(c_checks=checks)
        self.assertEqual(result["status"], "INVALID", result)
        self.assertTrue(result["h_gateway_attestation_authenticated"])

    def test_11_unknown_c_signature_prevents_durable_ingress_commit(self):
        checks = self.c_checks()
        checks.verify_c_signature = lambda obj, preimage: None
        gateway = self.gateway_checks()
        commits = []
        gateway.commit_authenticated_ingress = lambda env, digest, ctx: commits.append(True) or DurableIngressDecision("NEW")
        result = self.invoke(gateway_checks=gateway, c_checks=checks)
        self.assertEqual(result["status"], "UNKNOWN", result)
        self.assertEqual(commits, [])

    def test_12_p0_mutation_invalidates_original_digest(self):
        self.envelope["origin_sender_subject_ref"] = "C/adapter/attacker"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)
        self.assertIn("H gateway payload_digest mismatch", result["errors"])

    def test_13_unlisted_field_is_rejected_not_silently_omitted_from_p0(self):
        self.envelope["unregistered_security_field"] = "must-not-be-ignored"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

    def test_14_same_digest_replay_rechecks_disclosure_authorization(self):
        checks = self.gateway_checks()
        checks.commit_authenticated_ingress = lambda env, digest, ctx: DurableIngressDecision(
            "SAME_DIGEST_REPLAY", "H/accepted-result/17"
        )
        checks.verify_replay_disclosure_authorization = lambda env, ctx: False
        result = self.invoke(gateway_checks=checks)
        self.assertEqual(result["status"], "INVALID", result)

    def test_15_same_digest_replay_returns_prior_result_only_after_authorization(self):
        checks = self.gateway_checks()
        checks.commit_authenticated_ingress = lambda env, digest, ctx: DurableIngressDecision(
            "SAME_DIGEST_REPLAY", "H/accepted-result/17"
        )
        result = self.invoke(gateway_checks=checks)
        self.assertEqual(result["status"], "IDEMPOTENT_REPLAY", result)
        self.assertEqual(result["prior_result_ref"], "H/accepted-result/17")

    def test_16_unavailable_durable_ingress_state_is_unknown(self):
        checks = self.gateway_checks()
        checks.commit_authenticated_ingress = lambda env, digest, ctx: DurableIngressDecision("UNKNOWN")
        result = self.invoke(gateway_checks=checks)
        self.assertEqual(result["status"], "UNKNOWN", result)


    def test_18_every_present_p0_field_is_digest_bound(self):
        from gateway_attestation_validator import P0_FIELDS

        for field in P0_FIELDS:
            if field not in self.envelope:
                continue
            with self.subTest(field=field):
                old = self.envelope[field]
                if isinstance(old, str):
                    self.envelope[field] = old + "-mutated"
                elif old is None:
                    self.envelope[field] = "mutated"
                else:
                    self.envelope[field] = {"mutated": True}
                result = self.invoke()
                self.assertEqual(result["status"], "INVALID", result)
                self.envelope[field] = old

    def test_19_signature_and_integrity_reference_are_independently_verified(self):
        self.envelope["signature"] = "B" * 86
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

        self.setUp()
        self.envelope["integrity_proof_ref"] = "H/integrity-proof/attacker"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)


    def test_20_wrong_canonicalization_profile_is_invalid(self):
        self.envelope["canonicalization_profile_id"] = "some-other-profile"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

    def test_21_signature_must_use_unpadded_base64url_ed25519_shape(self):
        self.envelope["signature"] = "not-base64url"
        result = self.invoke()
        self.assertEqual(result["status"], "INVALID", result)

    def test_17_missing_protected_h_gateway_context_is_unknown(self):
        raw_env = json.dumps(self.envelope, separators=(",", ":"), sort_keys=True).encode("utf-8")
        raw_c = json.dumps(self.c_object, separators=(",", ":"), sort_keys=True).encode("utf-8")
        result = validate_gateway_attested_provider_outcome(
            raw_env, raw_c, self.origin_bytes, None, self.gateway_checks(),
            self.h_schema, self.c_schema, self.c_checks()
        )
        self.assertEqual(result["status"], "UNKNOWN", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
