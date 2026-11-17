import json
import unittest
from pathlib import Path
import jsonschema


class Issue20SchemaStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = Path(__file__).resolve().parents[1] / "issue20.archive-forget-restore.v0.1.0.schema.json"
        cls.schema = json.loads(schema_path.read_text(encoding="utf-8"))

    def test_d_i_storage_and_module_contract_types_exist(self):
        required = {
            "ProducerInstanceRef", "DRegistrationReceipt", "DPublicationParticipantAdmissionReceipt", "DPublicationTerminalReceipt",
            "DForgetBarrierProof", "IInventorySeal", "ICommitAuthorizationReceipt",
            "IReconciliationTuple", "StorageVisibilityParticipantRef", "StorageOutcomeProof",
            "FRecallCursor", "EPublicationRequest", "GContextLineageManifest",
            "RestoreProofBundle", "ITerminalProof"
        }
        self.assertTrue(required.issubset(set(self.schema["$defs"])))

    def test_receipt_outcomes_are_explicit_and_typed(self):
        decisions = self.schema["$defs"]["ICommitAuthorizationReceipt"]["allOf"][1]["properties"]["decision"]["enum"]
        self.assertEqual(set(decisions), {
            "COMMIT_WON", "REVOCATION_WON", "UNKNOWN_IN_DOUBT"
        })
        outcomes = self.schema["$defs"]["StorageOutcomeProof"]["allOf"][1]["properties"]["outcome"]["enum"]
        self.assertEqual(set(outcomes), {"COMMITTED_VISIBLE", "NO_PUBLICATION"})

    def test_restore_bundle_requires_each_independent_proof(self):
        required = set(self.schema["$defs"]["RestoreProofBundle"]["allOf"][1]["required"])
        self.assertTrue({
            "storageProofDigest", "cocPrefixDigest", "iProofDigest", "dProofDigest",
            "fProofDigest", "eProofDigest", "gProofDigest", "adapterProofDigest",
            "antiRollbackAnchor"
        }.issubset(required))

    def test_schema_does_not_define_a_global_high_water(self):
        all_defs = json.dumps(self.schema["$defs"], sort_keys=True)
        self.assertNotIn('"globalHighWater"', all_defs)
        self.assertNotIn('"unifiedHighWater"', all_defs)

    def test_draft_2020_12_schema_is_valid(self):
        jsonschema.Draft202012Validator.check_schema(self.schema)

    def test_d_registration_receipt_validates_and_rejects_wrong_authority(self):
        validator = jsonschema.Draft202012Validator(
            self.schema, format_checker=jsonschema.FormatChecker()
        )
        receipt = {
            "schemaId": "issue20.archive-forget-restore",
            "schemaVersion": "0.1.0",
            "messageId": "msg-1",
            "issuer": "D",
            "audience": "E",
            "issuedAt": "2026-11-17T00:00:00Z",
            "signatureProfileId": "profile-1",
            "keyId": "key-1",
            "signature": "signed",
            "messageType": "D_REGISTRATION_RECEIPT",
            "producerInstanceRef": {
                "policyDomainRef": "pd-1",
                "producerDomainRef": "domain-1",
                "producerId": "producer-1",
                "producerInstanceId": "instance-1",
                "identityGeneration": 1
            },
            "producerClassRef": "class-1",
            "producerWorkItemId": "work-1",
            "requestDigest": "sha256:" + "a" * 64,
            "scopeRef": "scope-1",
            "registrationCursor": {"authority": "D", "positionRef": "d:42"},
            "forgetFenceGeneration": 0,
            "sourceLineageDigest": "sha256:" + "b" * 64
        }
        validator.validate(receipt)
        wrong_owner_position = dict(receipt)
        wrong_owner_position["registrationCursor"] = {
            "authority": "I", "positionRef": "i:42"
        }
        self.assertFalse(validator.is_valid(wrong_owner_position))
        extra_field = dict(receipt)
        extra_field["untypedPermissionEpoch"] = "not-allowed"
        self.assertFalse(validator.is_valid(extra_field))


    def test_i_precommit_receipt_and_postcommit_terminal_proof_are_distinct(self):
        receipt = self.schema["$defs"]["ICommitAuthorizationReceipt"]["allOf"][1]["properties"]
        terminal = self.schema["$defs"]["ITerminalProof"]["allOf"][1]["properties"]
        self.assertIn("decision", receipt)
        self.assertIn("authorizationReceiptRef", terminal)
        self.assertIn("storageOutcomeDigest", terminal)
        self.assertEqual(set(terminal["storageOutcome"]["enum"]),
                         {"COMMITTED_VISIBLE", "NO_PUBLICATION"})
        self.assertNotIn("ITerminalProof", json.dumps(receipt))

    def test_owner_local_positions_reject_cross_authority_substitution(self):
        validator = jsonschema.Draft202012Validator(self.schema)
        dpos = {"authority": "D", "positionRef": "d:10"}
        ipos = {"authority": "I", "positionRef": "i:10"}
        validator.validate(dpos, self.schema["$defs"]["DPosition"])
        self.assertFalse(validator.is_valid(ipos, self.schema["$defs"]["DPosition"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
