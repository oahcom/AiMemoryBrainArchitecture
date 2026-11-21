"""CSubmitOutcome 1.0.1 structural conformance only.

The fixture declares profile_status=PROPOSED_NOT_REGISTERED and
signature_values=TEST_FIXTURE_PLACEHOLDERS_NOT_CRYPTOGRAPHICALLY_VALID.
These values MUST NOT be treated as valid signatures or cryptographic evidence.
No signature verification or C-owned semantic validation is performed here.

The C-owned schema is pinned by Blob SHA
a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda. Its exact bytes are embedded below
as a test-only immutable snapshot because BMCP does not own or install a copy.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PATH = (
    ROOT / "tests" / "conformance" / "provider_outcome"
    / "fixtures" / "c_submit_outcome_1_0_1_vectors.json"
)
C_SCHEMA_BLOB = "a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda"
C_SCHEMA_JSON = json.loads("{\n  \"$schema\": \"https://json-schema.org/draft/2020-12/schema\",\n  \"$id\": \"urn:aimba:schema:c-submit-outcome:1.0.1\",\n  \"title\": \"CSubmitOutcome\",\n  \"description\": \"Immutable C-owned provider handoff outcome record. Schema validates structure only; issuer authentication, append-only ledger inclusion, gate linearization, provider evidence and COC joins require semantic validation.\",\n  \"type\": \"object\",\n  \"additionalProperties\": false,\n  \"required\": [\n    \"schema_id\",\n    \"schema_version\",\n    \"schema_artifact_revision\",\n    \"signature_profile_id\",\n    \"record_ref\",\n    \"record_id\",\n    \"record_sequence\",\n    \"created_at\",\n    \"issuer_authority_ref\",\n    \"issuer_subject_ref\",\n    \"audience\",\n    \"purpose\",\n    \"message_id\",\n    \"message_nonce\",\n    \"CAdmissionRef\",\n    \"CAdmissionDigest\",\n    \"COwnerLedgerRef\",\n    \"COwnerLedgerVersion\",\n    \"COwnerLocalSequence\",\n    \"COwnerHighWater\",\n    \"COwnerLedgerRoot\",\n    \"CGateRef\",\n    \"CGateGeneration\",\n    \"CGateCommitRef\",\n    \"CGateCommitDigest\",\n    \"ProviderAttemptRef\",\n    \"ProviderAttemptGeneration\",\n    \"ProviderRef\",\n    \"ProviderAccountRef\",\n    \"AdapterRef\",\n    \"AdapterBuildRef\",\n    \"EndpointRef\",\n    \"RegionRef\",\n    \"ApiOperation\",\n    \"IdempotencyNamespaceRef\",\n    \"IdempotencyKeyRef\",\n    \"ProviderCapabilityRecordRef\",\n    \"ProviderCapabilityDigest\",\n    \"FinalRequestBoundaryRef\",\n    \"FinalRequestBoundaryType\",\n    \"RequestDigest\",\n    \"RequestContentType\",\n    \"RequestMethod\",\n    \"CausalOrderTransactionRef\",\n    \"Outcome\",\n    \"SideEffectStatus\",\n    \"OutcomeObservedAt\",\n    \"OutcomeEvidenceRef\",\n    \"OutcomeEvidenceDigest\",\n    \"COCParticipantIntentRef\",\n    \"COCParticipantReservationRef\",\n    \"COCAbsenceReason\",\n    \"PriorObservationRef\",\n    \"SupersedesObservationRef\",\n    \"ReconciliationParentRef\",\n    \"payload_digest\",\n    \"key_id_ref\",\n    \"key_version\",\n    \"signature\",\n    \"ProviderEvidenceIssuerRef\",\n    \"ProviderEvidenceType\",\n    \"message_type\",\n    \"OwnerSignatureRef\",\n    \"sequence_namespace_ref\"\n  ],\n  \"properties\": {\n    \"schema_id\": {\n      \"const\": \"CSubmitOutcome\"\n    },\n    \"schema_version\": {\n      \"const\": \"1.0.1\"\n    },\n    \"schema_artifact_revision\": {\n      \"const\": \"1.0.1\"\n    },\n    \"signature_profile_id\": {\n      \"const\": \"AIMBA-C-CRYPTO-1.0\"\n    },\n    \"record_ref\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"record_id\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 256\n    },\n    \"record_sequence\": {\n      \"type\": \"string\",\n      \"pattern\": \"^(0|[1-9][0-9]*)$\",\n      \"maxLength\": 40\n    },\n    \"created_at\": {\n      \"type\": \"string\",\n      \"format\": \"date-time\"\n    },\n    \"issuer_authority_ref\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"issuer_subject_ref\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"audience\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 256\n    },\n    \"purpose\": {\n      \"const\": \"C_PROVIDER_SUBMIT_OUTCOME\"\n    },\n    \"message_id\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 256\n    },\n    \"message_nonce\": {\n      \"type\": \"string\",\n      \"minLength\": 16,\n      \"maxLength\": 256\n    },\n    \"CAdmissionRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"CAdmissionDigest\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"COwnerLedgerRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"COwnerLedgerVersion\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 128\n    },\n    \"COwnerLocalSequence\": {\n      \"$ref\": \"#/$defs/sequence\"\n    },\n    \"COwnerHighWater\": {\n      \"$ref\": \"#/$defs/sequence\"\n    },\n    \"COwnerLedgerRoot\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"CGateRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"CGateGeneration\": {\n      \"$ref\": \"#/$defs/sequence\"\n    },\n    \"CGateCommitRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"CGateCommitDigest\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"ProviderAttemptRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderAttemptGeneration\": {\n      \"$ref\": \"#/$defs/sequence\"\n    },\n    \"ProviderRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderAccountRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"AdapterRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"AdapterBuildRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"EndpointRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"RegionRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ApiOperation\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 256\n    },\n    \"IdempotencyNamespaceRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"IdempotencyKeyRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderCapabilityRecordRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderCapabilityDigest\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"FinalRequestBoundaryRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"FinalRequestBoundaryType\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 128\n    },\n    \"RequestDigest\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"RequestContentType\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 256\n    },\n    \"RequestMethod\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 32\n    },\n    \"CausalOrderTransactionRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"Outcome\": {\n      \"enum\": [\n        \"HANDOFF_ACCEPTED\",\n        \"HANDOFF_REJECTED\",\n        \"NOT_INVOKED\",\n        \"UNKNOWN\",\n        \"IN_DOUBT\"\n      ]\n    },\n    \"SideEffectStatus\": {\n      \"enum\": [\n        \"PROVEN_OCCURRED\",\n        \"PROVEN_NONE\",\n        \"POSSIBLE_OR_UNKNOWN\"\n      ]\n    },\n    \"OutcomeObservedAt\": {\n      \"type\": \"string\",\n      \"format\": \"date-time\"\n    },\n    \"OutcomeEvidenceRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"OutcomeEvidenceDigest\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"ProviderRequestRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderReceiptRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderLookupProofRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderNoHandoffProofRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"NotInvokedProofRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"UnknownReasonRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"COCParticipantIntentRef\": {\n      \"type\": [\n        \"string\",\n        \"null\"\n      ],\n      \"maxLength\": 512\n    },\n    \"COCParticipantReservationRef\": {\n      \"type\": [\n        \"string\",\n        \"null\"\n      ],\n      \"maxLength\": 512\n    },\n    \"COCAbsenceReason\": {\n      \"type\": [\n        \"string\",\n        \"null\"\n      ],\n      \"maxLength\": 256\n    },\n    \"PriorObservationRef\": {\n      \"type\": [\n        \"string\",\n        \"null\"\n      ],\n      \"maxLength\": 512\n    },\n    \"SupersedesObservationRef\": {\n      \"type\": [\n        \"string\",\n        \"null\"\n      ],\n      \"maxLength\": 512\n    },\n    \"ReconciliationParentRef\": {\n      \"type\": [\n        \"string\",\n        \"null\"\n      ],\n      \"maxLength\": 512\n    },\n    \"payload_digest\": {\n      \"$ref\": \"#/$defs/sha256\"\n    },\n    \"key_id_ref\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"key_version\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 128\n    },\n    \"signature\": {\n      \"type\": \"string\",\n      \"pattern\": \"^[A-Za-z0-9_-]{86}$\"\n    },\n    \"ProviderEvidenceIssuerRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ProviderEvidenceType\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 128\n    },\n    \"message_type\": {\n      \"const\": \"C_PROVIDER_OUTCOME_RECORDED\"\n    },\n    \"OwnerSignatureRef\": {\n      \"$ref\": \"#/$defs/ref\"\n    },\n    \"ActualInferenceRequestId\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 512\n    },\n    \"sequence_namespace_ref\": {\n      \"$ref\": \"#/$defs/ref\"\n    }\n  },\n  \"$defs\": {\n    \"ref\": {\n      \"type\": \"string\",\n      \"minLength\": 1,\n      \"maxLength\": 512\n    },\n    \"sha256\": {\n      \"type\": \"string\",\n      \"pattern\": \"^[a-f0-9]{64}$\"\n    },\n    \"sequence\": {\n      \"type\": \"string\",\n      \"pattern\": \"^(0|[1-9][0-9]*)$\",\n      \"maxLength\": 40\n    }\n  },\n  \"allOf\": [\n    {\n      \"if\": {\n        \"properties\": {\n          \"Outcome\": {\n            \"const\": \"HANDOFF_ACCEPTED\"\n          }\n        },\n        \"required\": [\n          \"Outcome\"\n        ]\n      },\n      \"then\": {\n        \"required\": [\n          \"ProviderRequestRef\",\n          \"ProviderReceiptRef\"\n        ],\n        \"properties\": {\n          \"SideEffectStatus\": {\n            \"const\": \"PROVEN_OCCURRED\"\n          }\n        }\n      }\n    },\n    {\n      \"if\": {\n        \"properties\": {\n          \"Outcome\": {\n            \"const\": \"HANDOFF_REJECTED\"\n          }\n        },\n        \"required\": [\n          \"Outcome\"\n        ]\n      },\n      \"then\": {\n        \"required\": [\n          \"ProviderRequestRef\"\n        ],\n        \"properties\": {\n          \"SideEffectStatus\": {\n            \"enum\": [\n              \"PROVEN_NONE\",\n              \"POSSIBLE_OR_UNKNOWN\",\n              \"PROVEN_OCCURRED\"\n            ]\n          }\n        }\n      }\n    },\n    {\n      \"if\": {\n        \"properties\": {\n          \"Outcome\": {\n            \"const\": \"NOT_INVOKED\"\n          }\n        },\n        \"required\": [\n          \"Outcome\"\n        ]\n      },\n      \"then\": {\n        \"required\": [\n          \"ProviderNoHandoffProofRef\",\n          \"NotInvokedProofRef\"\n        ],\n        \"properties\": {\n          \"SideEffectStatus\": {\n            \"const\": \"PROVEN_NONE\"\n          }\n        }\n      }\n    },\n    {\n      \"if\": {\n        \"properties\": {\n          \"Outcome\": {\n            \"enum\": [\n              \"UNKNOWN\",\n              \"IN_DOUBT\"\n            ]\n          }\n        },\n        \"required\": [\n          \"Outcome\"\n        ]\n      },\n      \"then\": {\n        \"required\": [\n          \"UnknownReasonRef\"\n        ],\n        \"properties\": {\n          \"SideEffectStatus\": {\n            \"const\": \"POSSIBLE_OR_UNKNOWN\"\n          }\n        }\n      }\n    },\n    {\n      \"if\": {\n        \"properties\": {\n          \"COCParticipantIntentRef\": {\n            \"type\": \"null\"\n          }\n        },\n        \"required\": [\n          \"COCParticipantIntentRef\"\n        ]\n      },\n      \"then\": {\n        \"properties\": {\n          \"COCParticipantReservationRef\": {\n            \"type\": \"null\"\n          },\n          \"COCAbsenceReason\": {\n            \"type\": \"string\",\n            \"minLength\": 1\n          }\n        }\n      }\n    },\n    {\n      \"if\": {\n        \"properties\": {\n          \"COCParticipantIntentRef\": {\n            \"type\": \"string\"\n          }\n        },\n        \"required\": [\n          \"COCParticipantIntentRef\"\n        ]\n      },\n      \"then\": {\n        \"properties\": {\n          \"COCParticipantReservationRef\": {\n            \"type\": \"string\",\n            \"minLength\": 1\n          },\n          \"COCAbsenceReason\": {\n            \"type\": \"null\"\n          }\n        }\n      }\n    },\n    {\n      \"if\": {\n        \"properties\": {\n          \"COCParticipantReservationRef\": {\n            \"type\": \"string\"\n          }\n        },\n        \"required\": [\n          \"COCParticipantReservationRef\"\n        ]\n      },\n      \"then\": {\n        \"properties\": {\n          \"COCParticipantIntentRef\": {\n            \"type\": \"string\",\n            \"minLength\": 1\n          }\n        }\n      }\n    }\n  ]\n}\n")
# C_SCHEMA_JSON is already a dict: it was parsed from the embedded JSON text above.
C_SCHEMA = C_SCHEMA_JSON

FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
SCHEMA_BLOB = FIXTURE["schema_blob"]
SCHEMA_VERSION = FIXTURE["schema_version"]
PROFILE_STATUS = FIXTURE["profile_status"]
SIGNATURE_VALUES = FIXTURE["signature_values"]
VECTORS = {item["id"]: item for item in FIXTURE["vectors"]}


class ProviderOutcomeStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SCHEMA_BLOB != C_SCHEMA_BLOB:
            raise RuntimeError("Fixture schema_blob does not match pinned C schema Blob")
        if SCHEMA_VERSION != "1.0.1":
            raise RuntimeError("Unexpected CSubmitOutcome schema version")
        cls.validator = Draft202012Validator(C_SCHEMA)

    def assert_schema_rejected(self, record):
        self.assertTrue(
            list(self.validator.iter_errors(record)),
            "Expected CSubmitOutcome schema to reject this record",
        )

    def test_cpo01_and_cpo03_are_schema_structurally_valid(self):
        for vector_id in ("CPO-01-accepted", "CPO-03-not-invoked"):
            with self.subTest(vector=vector_id):
                self.validator.validate(VECTORS[vector_id]["record"])

    def test_cpo06_accepted_without_provider_receipt_is_rejected(self):
        record = VECTORS["CPO-06-accepted-without-receipt"]["record"]
        self.assertNotIn("ProviderReceiptRef", record)
        self.assert_schema_rejected(record)

    def test_cpo07_not_invoked_without_both_proofs_is_rejected(self):
        record = VECTORS["CPO-07-not-invoked-without-proof"]["record"]
        self.assertNotIn("ProviderNoHandoffProofRef", record)
        self.assertNotIn("NotInvokedProofRef", record)
        self.assert_schema_rejected(record)

    def test_cpo08_fixture_is_rejected_and_coc_half_pair_rule_is_checked(self):
        record = VECTORS["CPO-08-coc-half-pair"]["record"]
        # Checked-in CPO-08 actually has BOTH COC refs as non-null strings.
        # It is rejected because HANDOFF_ACCEPTED lacks ProviderRequestRef
        # and ProviderReceiptRef. Do not misreport this as a COC fixture defect.
        self.assertIsInstance(record["COCParticipantIntentRef"], str)
        self.assertIsInstance(record["COCParticipantReservationRef"], str)
        self.assertNotIn("ProviderRequestRef", record)
        self.assertNotIn("ProviderReceiptRef", record)
        self.assert_schema_rejected(record)

        # Separately probe the schema COC half-pair rule using an in-memory
        # mutation; the checked-in fixture remains untouched.
        half_pair = copy.deepcopy(record)
        half_pair["COCParticipantReservationRef"] = None
        errors = list(self.validator.iter_errors(half_pair))
        self.assertTrue(errors)
        self.assertTrue(
            any(
                "COCParticipantReservationRef" in error.message
                or "COCParticipantReservationRef" in str(list(error.path))
                for error in errors
            ),
            "Expected schema rejection of a COC intent/reservation half-pair",
        )

    def test_unregistered_profile_and_placeholder_signature_are_not_valid_evidence(self):
        self.assertEqual(PROFILE_STATUS, "PROPOSED_NOT_REGISTERED")
        self.assertEqual(
            SIGNATURE_VALUES,
            "TEST_FIXTURE_PLACEHOLDERS_NOT_CRYPTOGRAPHICALLY_VALID",
        )
        self.assertNotEqual(PROFILE_STATUS, "REGISTERED")
        # No cryptographic validity assertion: placeholder is not valid evidence.

    def test_cpo02_requires_owner_c_semantic_validator(self):
        self.skipTest("SEMANTIC: requires Owner C authoritative validator")

    def test_cpo04_requires_owner_c_semantic_validator(self):
        self.skipTest("SEMANTIC: requires Owner C authoritative validator")

    def test_cpo05_requires_owner_c_semantic_validator(self):
        self.skipTest("SEMANTIC: requires Owner C authoritative validator")

    def test_cpo09_requires_owner_c_semantic_validator(self):
        self.skipTest("SEMANTIC: requires Owner C authoritative validator")

    def test_cpo10_requires_owner_c_semantic_validator(self):
        self.skipTest("SEMANTIC: requires Owner C authoritative validator")


if __name__ == "__main__":
    unittest.main()
