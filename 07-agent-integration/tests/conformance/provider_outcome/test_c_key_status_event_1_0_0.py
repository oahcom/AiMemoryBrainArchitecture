"""Structural and state-machine tests for C key-status event schema 1.0.0.

Governance signatures, trust roots, custody and external anti-rollback are not
verified by this unit suite.
"""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT.parents[2] / "schemas" / "c-key-status-event-1.0.0.schema.json"

ALLOWED = {
    None: {"PENDING"},
    "PENDING": {"ACTIVE", "DESTROYED"},
    "ACTIVE": {"RETIRED", "REVOKED", "COMPROMISED"},
    "RETIRED": {"REVOKED", "COMPROMISED", "DESTROYED"},
    "REVOKED": {"COMPROMISED", "DESTROYED"},
    "COMPROMISED": {"DESTROYED"},
    "DESTROYED": set(),
}


def validate_transition(prior, next_state):
    return next_state in ALLOWED[prior]


def status_at_sequence(events, signing_sequence, namespace):
    ordered = sorted(events, key=lambda e: int(e["event_sequence"]))
    prior = None
    prior_seq = -1
    latest = None
    for event in ordered:
        if event["sequence_namespace_ref"] != namespace:
            return "INVALID"
        seq = int(event["event_sequence"])
        if seq <= prior_seq or not validate_transition(prior, event["state"]):
            return "INVALID"
        prior_seq = seq
        prior = event["state"]
        if seq <= int(signing_sequence):
            latest = event["state"]
    if latest is None:
        return "UNKNOWN"
    return "VALID" if latest == "ACTIVE" else "INVALID"


class CKeyStatusEventV100Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_01_schema_is_valid_and_closed(self):
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual(self.schema["$id"], "urn:aimba:schema:c-key-status-event:1.0.0")
        self.assertFalse(self.schema["additionalProperties"])
        Draft202012Validator(self.schema, format_checker=FormatChecker())

    def test_02_profile_and_governance_signature_are_separate(self):
        props = self.schema["properties"]
        self.assertEqual(props["profile_id"]["const"], "AIMBA-C-CRYPTO-1.0")
        self.assertEqual(props["governance_signature_profile_id"]["const"], "AIMBA-I-KEY-GOVERNANCE-1.0")
        self.assertEqual(props["message_type"]["const"], "C_KEY_STATUS_EVENT")

    def test_03_state_transition_matrix(self):
        self.assertTrue(validate_transition(None, "PENDING"))
        self.assertTrue(validate_transition("PENDING", "ACTIVE"))
        self.assertTrue(validate_transition("ACTIVE", "COMPROMISED"))
        self.assertTrue(validate_transition("COMPROMISED", "DESTROYED"))
        self.assertFalse(validate_transition("ACTIVE", "PENDING"))
        self.assertFalse(validate_transition("REVOKED", "ACTIVE"))
        self.assertFalse(validate_transition("DESTROYED", "ACTIVE"))

    def test_04_status_is_sequence_scoped_not_wall_clock_scoped(self):
        events = [
            {"event_sequence": "10", "sequence_namespace_ref": "C/sequencer/1", "state": "PENDING"},
            {"event_sequence": "12", "sequence_namespace_ref": "C/sequencer/1", "state": "ACTIVE"},
            {"event_sequence": "20", "sequence_namespace_ref": "C/sequencer/1", "state": "REVOKED"},
        ]
        self.assertEqual(status_at_sequence(events, "15", "C/sequencer/1"), "VALID")
        self.assertEqual(status_at_sequence(events, "20", "C/sequencer/1"), "INVALID")
        self.assertEqual(status_at_sequence(events, "9", "C/sequencer/1"), "UNKNOWN")

    def test_05_fork_duplicate_sequence_and_wrong_namespace_fail_closed(self):
        duplicate = [
            {"event_sequence": "10", "sequence_namespace_ref": "C/sequencer/1", "state": "PENDING"},
            {"event_sequence": "10", "sequence_namespace_ref": "C/sequencer/1", "state": "ACTIVE"},
        ]
        wrong_ns = [
            {"event_sequence": "10", "sequence_namespace_ref": "C/sequencer/1", "state": "PENDING"},
            {"event_sequence": "12", "sequence_namespace_ref": "C/sequencer/2", "state": "ACTIVE"},
        ]
        self.assertEqual(status_at_sequence(duplicate, "15", "C/sequencer/1"), "INVALID")
        self.assertEqual(status_at_sequence(wrong_ns, "15", "C/sequencer/1"), "INVALID")


if __name__ == "__main__":
    unittest.main(verbosity=2)
