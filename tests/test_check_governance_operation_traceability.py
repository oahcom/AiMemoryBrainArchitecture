#!/usr/bin/env python3
"""Unit tests for governance-operation authority traceability."""
from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_governance_operation_traceability import FILES, HEADERS, check

ROWS = (
    ("Authorization and revocation", "Owner I", "Owner I for PermissionEpoch", "Each affected subsystem", "Versioned authorization record and boundary enforcement evidence"),
    ("Retention and legal hold", "Owner I", "Owner I policy record; Owner D lifecycle state", "Each data custodian", "Decision and per-custodian acknowledgement"),
    ("Logical Forget suppression / fence", "Owner I", "Owner D canonical state", "D and each downstream subsystem", "Canonical fence receipt and per-executor suppression evidence"),
    ("Physical erasure", "Owner I", "Owner D canonical record; each store owner deletion state", "Storage operator for each copy", "Per-store deletion receipts and replica/cache evidence"),
    ("Backup expiry / deletion", "Owner I", "Backup catalog object state", "Backup service operator", "Backup service expiry/deletion evidence; Owner gap remains open"),
    ("External-recipient deletion", "Owner I", "Each recipient deletion/compliance state", "Each external recipient", "Authenticated recipient-specific completion evidence"),
    ("Global Forget Completion assessment", "Owner I", "Joint evidence from D and relevant execution Owners", "Every relevant storage/subsystem/recipient executor", "Reconciled inventory and jointly accepted evidence; no unilateral declaration"),
)

def document(path: str, rows=ROWS) -> str:
    if path == FILES[2]:
        translations = {
            "Authorization and revocation": "授权与撤销",
            "Retention and legal hold": "Retention 与 Legal Hold",
            "Logical Forget suppression / fence": "逻辑 Forget 抑制/围栏",
            "Physical erasure": "物理擦除",
            "Backup expiry / deletion": "备份到期/删除",
            "External-recipient deletion": "外部接收方删除",
            "Global Forget Completion assessment": "Global Forget Completion 判定",
        }
        rows = tuple((translations.get(row[0], row[0]), *row[1:]) for row in rows)
    header = "| " + " | ".join(HEADERS[path]) + " |\n"
    separator = "|---|---|---|---|---|\n"
    body = "".join("| " + " | ".join(row) + " |\n" for row in rows)
    return header + separator + body

class GovernanceTraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for path in FILES:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document(path), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_check(self):
        return check(self.root)

    def test_complete_three_way_register_passes(self):
        code, errors = self.run_check()
        self.assertEqual((code, errors), (0, []))

    def test_missing_physical_executor_fails(self):
        rows = list(ROWS)
        rows[2] = rows[2][:3] + ("",) + rows[2][4:]
        (self.root / FILES[0]).write_text(document(FILES[0], rows), encoding="utf-8")
        code, errors = self.run_check()
        self.assertEqual(code, 1)
        self.assertTrue(any("physical executor is empty" in item for item in errors))

    def test_unassigned_role_is_open_finding(self):
        rows = list(ROWS)
        rows[4] = rows[4][:3] + ("NOT_ASSIGNED",) + rows[4][4:]
        (self.root / FILES[0]).write_text(document(FILES[0], rows), encoding="utf-8")
        code, errors = self.run_check()
        self.assertEqual(code, 1)
        self.assertTrue(any("NOT_ASSIGNED" in item for item in errors))

    def test_policy_and_executor_cannot_be_collapsed(self):
        rows = list(ROWS)
        rows[0] = (rows[0][0], "Owner I", rows[0][2], "Owner I", rows[0][4])
        (self.root / FILES[0]).write_text(document(FILES[0], rows), encoding="utf-8")
        code, errors = self.run_check()
        self.assertEqual(code, 1)
        self.assertTrue(any("collapses an authority role" in item for item in errors))

    def test_missing_mirror_fails_incomplete(self):
        (self.root / FILES[2]).unlink()
        code, errors = self.run_check()
        self.assertEqual(code, 2)
        self.assertTrue(any("INCOMPLETE" in item for item in errors))

    def test_mirror_row_count_drift_fails(self):
        rows = ROWS[:-1]
        (self.root / FILES[1]).write_text(document(FILES[1], rows), encoding="utf-8")
        code, errors = self.run_check()
        self.assertEqual(code, 1)
        self.assertTrue(any("row-count mismatch" in item for item in errors))

    def test_false_completion_claim_fails(self):
        path = self.root / FILES[0]
        path.write_text(path.read_text(encoding="utf-8") + "\nForgotten state proves physical erasure.\n", encoding="utf-8")
        code, errors = self.run_check()
        self.assertEqual(code, 1)
        self.assertTrue(any("false/unilateral completion" in item for item in errors))

if __name__ == "__main__":
    unittest.main()
