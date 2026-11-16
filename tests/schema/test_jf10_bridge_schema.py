"""JSON Schema validation for the five BMCP JF-10 bridge message families."""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "08-bmcp-protocol" / "schemas" / "bmcp.applied-ack-1.1.0-jf10-bridge.schema.json"


def resolve_ref(ref, root):
    assert ref.startswith("#/")
    node = root
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def sample_value(prop_schema, root):
    if "$ref" in prop_schema:
        return sample_value(resolve_ref(prop_schema["$ref"], root), root)
    if "const" in prop_schema:
        return prop_schema["const"]
    if "enum" in prop_schema:
        return prop_schema["enum"][0]
    kind = prop_schema.get("type")
    if kind == "string":
        if prop_schema.get("pattern") == "^[a-f0-9]{64}$":
            return "a" * 64
        return "ref:sample"
    if kind == "array":
        return ["ref:sample"]
    if kind == "integer":
        return 1
    if kind == "boolean":
        return True
    if kind == "object":
        return {}
    raise AssertionError(f"unsupported schema shape: {prop_schema}")


def valid_message(root, variant):
    props = variant["properties"]
    record = {name: sample_value(props[name], root) for name in variant["required"]}
    # Choose conditional branches whose required companion fields are explicit.
    if record.get("message_type") == "JF10_PREPARE_INTENT_REGISTERED":
        record["applicable_d_fence_request_refs"] = ["D:fence:1"]
    if record.get("message_type") == "I_JF10_TERMINAL_DECISION_OBSERVED":
        record["i_revocation_request_state"] = "NONE_AT_TERMINALIZATION"
    if record.get("message_type") == "STORAGE_JF10_PARTICIPANT_RESOLVED":
        record["storage_resolution_outcome"] = "COMMITTED"
        record["storage_visibility_state"] = "VISIBLE"
        record["storage_publication_receipt_ref"] = "Storage:publication:1"
        record["visibility_pointer_transaction_ref"] = record["storage_resolution_transaction_ref"]
    if record.get("message_type") == "JF10_BRIDGE_RECONCILIATION_RECORDED":
        record["reconciliation_state"] = "RECONCILED_TERMINAL"
        record["i_lookup_state"] = "COMMIT_WON"
        record["storage_lookup_state"] = "COMMITTED"
        record["d_barrier_state"] = "SATISFIED"
    return record


class JF10BridgeSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(self.schema)

    def test_exactly_five_distinct_message_variants_exist(self):
        self.assertEqual(len(self.schema["oneOf"]), 5)
        types = [v["properties"]["message_type"]["const"] for v in self.schema["oneOf"]]
        self.assertEqual(len(set(types)), 5)

    def test_each_message_family_has_one_valid_minimal_fixture(self):
        for variant in self.schema["oneOf"]:
            with self.subTest(message_type=variant["properties"]["message_type"]["const"]):
                record = valid_message(self.schema, variant)
                self.validator.validate(record)
                # The root oneOf enforces that exactly one message variant matches.
                self.validator.validate(record)

    def test_bad_sha256_digest_is_rejected(self):
        record = valid_message(self.schema, self.schema["oneOf"][0])
        record["payload_digest"] = "not-a-sha256"
        self.assertFalse(self.validator.is_valid(record))

    def test_wrong_schema_version_is_rejected(self):
        record = valid_message(self.schema, self.schema["oneOf"][0])
        record["schema_version"] = "1.0.0"
        self.assertFalse(self.validator.is_valid(record))

    def test_missing_required_immutable_operation_field_is_rejected(self):
        record = valid_message(self.schema, self.schema["oneOf"][0])
        record.pop("publication_operation_id")
        self.assertFalse(self.validator.is_valid(record))

    def test_empty_d_fence_set_requires_completeness_attestation(self):
        variant = self.schema["oneOf"][0]
        record = valid_message(self.schema, variant)
        record["applicable_d_fence_request_refs"] = []
        self.assertFalse(self.validator.is_valid(record))
        record["d_fence_completeness_attestation_ref"] = "D:complete:1"
        self.validator.validate(record)

    def test_i_revocation_present_requires_owner_cutoff_proof(self):
        variant = self.schema["oneOf"][2]
        record = valid_message(self.schema, variant)
        record["i_revocation_request_state"] = "PRESENT"
        self.assertFalse(self.validator.is_valid(record))
        record["i_revocation_request_ref"] = "I:revoke:1"
        record["i_revocation_cutoff_proof_ref"] = "I:cutoff:1"
        self.validator.validate(record)

    def test_storage_commit_requires_pointer_and_publication_receipt(self):
        variant = self.schema["oneOf"][3]
        record = valid_message(self.schema, variant)
        record.pop("storage_publication_receipt_ref")
        self.assertFalse(self.validator.is_valid(record))

    def test_storage_rollback_requires_nonpublication_proof_and_forbids_pointer(self):
        variant = self.schema["oneOf"][3]
        record = valid_message(self.schema, variant)
        record["storage_resolution_outcome"] = "ROLLED_BACK"
        record["storage_visibility_state"] = "NOT_VISIBLE"
        record["storage_nonpublication_proof_ref"] = "Storage:no-publication:1"
        record.pop("storage_publication_receipt_ref")
        record.pop("visibility_pointer_transaction_ref")
        self.validator.validate(record)

    def test_schema_defers_cross_message_reconciliation_truth_to_semantic_validator(self):
        variant = self.schema["oneOf"][4]
        record = valid_message(self.schema, variant)
        record["d_barrier_state"] = "UNKNOWN"
        # JSON Schema validates shape/enum; cross-message authority consistency is
        # deliberately delegated to the semantic validator and owner lookups.
        self.validator.validate(record)


if __name__ == "__main__":
    unittest.main()