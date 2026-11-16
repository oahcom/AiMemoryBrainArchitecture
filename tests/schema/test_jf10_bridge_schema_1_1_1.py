"""Schema 1.1.1 tests for stable prepared participant/GID/native-XID separation."""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from test_jf10_bridge_schema import valid_message

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "08-bmcp-protocol" / "schemas" / "bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json"


class JF10BridgeSchema111Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_schema_is_valid_draft_2020_12_and_versioned_1_1_1(self):
        Draft202012Validator.check_schema(self.schema)
        self.assertIn("/1.1.1/", self.schema["$id"])
        self.assertTrue(all(v["properties"]["schema_version"]["const"] == "1.1.1"
                            for v in self.schema["oneOf"]))

    def test_all_five_message_families_validate(self):
        self.assertEqual(len(self.schema["oneOf"]), 5)
        for variant in self.schema["oneOf"]:
            with self.subTest(message_type=variant["properties"]["message_type"]["const"]):
                self.validator.validate(valid_message(self.schema, variant))

    def test_stable_participant_and_prepared_gid_are_required_in_all_messages(self):
        for variant in self.schema["oneOf"]:
            record = valid_message(self.schema, variant)
            for field in ("prepared_participant_ref", "prepared_transaction_gid"):
                broken = dict(record)
                broken.pop(field)
                with self.subTest(message_type=record["message_type"], missing=field):
                    self.assertFalse(self.validator.is_valid(broken))

    def test_prepared_and_resolved_messages_require_engine_native_identity_evidence(self):
        for index in (1, 3):
            variant = self.schema["oneOf"][index]
            record = valid_message(self.schema, variant)
            for field in ("engine_native_transaction_xid_ref", "postgres_system_identifier",
                          "target_database_oid", "prepare_timeline", "prepare_lsn",
                          "storage_signer_key_version"):
                broken = dict(record)
                broken.pop(field)
                with self.subTest(message_type=record["message_type"], missing=field):
                    self.assertFalse(self.validator.is_valid(broken))

    def test_prepared_gid_and_native_xid_are_separate_fields(self):
        record = valid_message(self.schema, self.schema["oneOf"][1])
        record["prepared_transaction_gid"] = "gid_1234567890"
        record["engine_native_transaction_xid_ref"] = "native-xid:429496729"
        self.assertNotEqual(record["prepared_transaction_gid"],
                            record["engine_native_transaction_xid_ref"])
        self.validator.validate(record)

    def test_prepared_gid_rejects_invalid_or_oversized_value(self):
        record = valid_message(self.schema, self.schema["oneOf"][0])
        record["prepared_transaction_gid"] = "bad gid with spaces"
        self.assertFalse(self.validator.is_valid(record))
        record["prepared_transaction_gid"] = "g" * 201
        self.assertFalse(self.validator.is_valid(record))

    def test_postgres_system_identifier_and_database_oid_are_decimal_strings(self):
        record = valid_message(self.schema, self.schema["oneOf"][1])
        record["postgres_system_identifier"] = "cluster-A"
        self.assertFalse(self.validator.is_valid(record))
        record["postgres_system_identifier"] = "1234567890"
        record["target_database_oid"] = "db-oid"
        self.assertFalse(self.validator.is_valid(record))

    def test_prepare_lsn_requires_postgres_hex_x_y_form(self):
        record = valid_message(self.schema, self.schema["oneOf"][1])
        record["prepare_lsn"] = "not-an-lsn"
        self.assertFalse(self.validator.is_valid(record))

    def test_reconciliation_with_prepared_state_requires_native_xid_and_storage_key_evidence(self):
        variant = self.schema["oneOf"][4]
        record = valid_message(self.schema, variant)
        record["storage_lookup_state"] = "PREPARED"
        self.validator.validate(record)
        record.pop("engine_native_transaction_xid_ref")
        self.assertFalse(self.validator.is_valid(record))

    def test_legacy_aliases_are_optional_in_1_1_1(self):
        record = valid_message(self.schema, self.schema["oneOf"][1])
        for field in ("storage_participant_ref", "storage_xid_ref",
                      "preallocated_storage_xid_ref", "storage_prepare_transaction_ref"):
            record.pop(field, None)
        self.validator.validate(record)

    def test_1_1_0_message_cannot_be_mislabeled_as_1_1_1(self):
        record = valid_message(self.schema, self.schema["oneOf"][0])
        record["schema_version"] = "1.1.0"
        self.assertFalse(self.validator.is_valid(record))


if __name__ == "__main__":
    unittest.main()