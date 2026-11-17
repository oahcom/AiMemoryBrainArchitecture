import json
import unittest
from pathlib import Path


class Issue20SchemaStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = Path(__file__).resolve().parents[1] / "issue20.archive-forget-restore.v0.1.0.schema.json"
        cls.schema = json.loads(schema_path.read_text(encoding="utf-8"))

    def test_d_i_storage_and_module_contract_types_exist(self):
        required = {
            "ProducerInstanceRef", "DRegistrationReceipt", "DForgetBarrierProof",
            "IInventorySeal", "ICommitAuthorizationReceipt",
            "StorageVisibilityParticipantRef", "StorageOutcomeProof",
            "FRecallCursor", "EPublicationRequest", "GContextLineageManifest",
            "RestoreProofBundle"
        }
        self.assertTrue(required.issubset(set(self.schema["$defs"])))

    def test_receipt_outcomes_are_explicit_and_typed(self):
        decisions = self.schema["$defs"]["ICommitAuthorizationReceipt"]["allOf"][1]["properties"]["decision"]["enum"]
        self.assertEqual(set(decisions), {
            "COMMIT_WON", "REVOCATION_WON", "INDETERMINATE_ABORTED", "UNKNOWN_IN_DOUBT"
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
