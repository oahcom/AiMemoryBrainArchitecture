"""Candidate wire-interoperability checks for BMCP recovery-cutoff 1.0.4.

These tests define a TEST PROFILE only. They do not freeze production canonicalization,
signature bytes, key trust, or the final H/I security profile.
"""
import hashlib
import json
import unittest


def reject_duplicate_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key: " + key)
        out[key] = value
    return out


def strict_parse(raw):
    return json.loads(raw, object_pairs_hook=reject_duplicate_pairs)


def canonical_test_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def valid_counter(value):
    return isinstance(value, str) and (
        value == "0" or (value.isascii() and value.isdigit()
                         and value[0] != "0")
    )


def reject_unknown_critical(obj, allowed):
    return all(not (key.startswith("critical_") and key not in allowed)
               for key in obj)


class WireInteropVectors(unittest.TestCase):
    def test_WIRE_01_object_member_order_is_canonicalized(self):
        left = strict_parse('{"schema_version":"1.0.0","message_type":"COC_PARTICIPANT_MANIFEST"}')
        right = strict_parse('{"message_type":"COC_PARTICIPANT_MANIFEST","schema_version":"1.0.0"}')
        self.assertEqual(canonical_test_bytes(left), canonical_test_bytes(right))

    def test_WIRE_02_absent_and_null_are_not_equivalent(self):
        absent = {"enumeration_status": "COMPLETE_EMPTY"}
        explicit_null = {"enumeration_status": "COMPLETE_EMPTY", "participant_entries": None}
        self.assertNotEqual(canonical_test_bytes(absent), canonical_test_bytes(explicit_null))

    def test_WIRE_03_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            strict_parse('{"message_id":"m/1","message_id":"m/2"}')

    def test_WIRE_04_counters_are_canonical_decimal_strings(self):
        for value in ("0", "1", "10", "18446744073709551616"):
            self.assertTrue(valid_counter(value))
        for value in ("", "00", "01", "-1", "+1", 1, 1.0, " 1"):
            self.assertFalse(valid_counter(value))

    def test_WIRE_05_utf8_is_deterministic_without_ascii_escape(self):
        value = {"label": "恢复批次"}
        self.assertEqual(canonical_test_bytes(value), '{"label":"恢复批次"}'.encode("utf-8"))

    def test_WIRE_06_unknown_critical_field_fails_closed(self):
        obj = {"schema_version": "1.0.0", "critical_new_gate_field": "x"}
        self.assertFalse(reject_unknown_critical(obj, {"schema_version"}))
        self.assertTrue(reject_unknown_critical(obj, {"schema_version", "critical_new_gate_field"}))

    def test_WIRE_07_absent_vs_empty_array_is_distinct(self):
        absent = {"enumeration_status": "COMPLETE_EMPTY"}
        empty = {"enumeration_status": "COMPLETE_EMPTY", "participant_entries": []}
        self.assertNotEqual(canonical_test_bytes(absent), canonical_test_bytes(empty))

    def test_WIRE_08_gid_is_an_opaque_string_not_native_numeric_xid(self):
        gid = "jf10:tenant-a:op-00017"
        wire = canonical_test_bytes({"prepared_transaction_gid": gid})
        self.assertIn(gid.encode("utf-8"), wire)
        self.assertNotEqual(canonical_test_bytes({"prepared_transaction_gid": gid}),
                            canonical_test_bytes({"postgresql_native_xid_observed": 17}))

    def test_WIRE_09_domain_separation_changes_digest(self):
        payload = canonical_test_bytes({"message_type": "RECOVERY_JOIN_PROOF"})
        h1 = hashlib.sha256(b"BMCP-RECOVERY-JOIN-TEST\\0" + payload).digest()
        h2 = hashlib.sha256(b"BMCP-RECOVERY-BATCH-TEST\\0" + payload).digest()
        self.assertNotEqual(h1, h2)

    def test_WIRE_10_same_bytes_produce_same_digest(self):
        payload = canonical_test_bytes({"a": "1", "b": "2"})
        self.assertEqual(hashlib.sha256(payload).digest(), hashlib.sha256(payload).digest())


if __name__ == "__main__":
    unittest.main(verbosity=2)
