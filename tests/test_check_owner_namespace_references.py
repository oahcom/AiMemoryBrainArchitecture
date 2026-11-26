#!/usr/bin/env python3
"""Unit tests for the Owner namespace checker."""
from __future__ import annotations

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_owner_namespace_references import violations

class OwnerNamespaceTests(unittest.TestCase):
    def test_explicit_owner_and_sys_identifier_are_not_confused(self):
        text = "Owner E owns ingestion. SYS-MEMORY-COMPILER is a subsystem.\n"
        self.assertEqual(violations(text), [])

    def test_sys_identifier_cannot_fill_owner_slot(self):
        self.assertEqual(violations("Primary Owner: SYS-MEMORY-COMPILER"), [
            (1, "SYS_ID_AS_OWNER", "Primary Owner: SYS-MEMORY-COMPILER")
        ])

    def test_capability_label_cannot_fill_owner_slot(self):
        self.assertEqual(violations("Accountable Owner: Canonical Store"), [
            (1, "CAPABILITY_AS_OWNER", "Accountable Owner: Canonical Store")
        ])

    def test_bare_owner_letter_in_accountability_claim_is_rejected(self):
        self.assertEqual(violations("B owns canonical persistence."), [
            (1, "BARE_LETTER_AS_OWNER", "B owns canonical persistence.")
        ])

    def test_unrelated_prose_and_qualified_example_pass(self):
        text = "The letter B appears in this paragraph.\nOwner B owns domain semantics.\n"
        self.assertEqual(violations(text), [])

    def test_owner_crosswalk_table_qualifies_bare_owner_letters(self):
        text = "\\n".join((
            "| Logical group | Primary Owner authority | Supporting Owners |",
            "|---|---|---|",
            "| SYS-MEMORY-BRAIN | B for semantics; D for lifecycle | E, F, G |",
        ))
        self.assertEqual(violations(text), [])

    def test_sys_id_in_owner_crosswalk_cell_is_rejected(self):
        text = "\\n".join((
            "| Logical group | Primary Owner authority | Supporting Owners |",
            "|---|---|---|",
            "| SYS-MEMORY-BRAIN | SYS-MEMORY-COMPILER | E |",
        ))
        self.assertEqual(violations(text)[0][1], "SYS_ID_AS_OWNER")

    def test_capability_in_owner_crosswalk_cell_is_rejected(self):
        text = "\\n".join((
            "| Logical group | Primary Owner authority | Supporting Owners |",
            "|---|---|---|",
            "| SYS-MEMORY-BRAIN | Canonical Store | E |",
        ))
        self.assertEqual(violations(text)[0][1], "CAPABILITY_AS_OWNER")

    def test_code_fence_example_is_not_treated_as_live_claim(self):
        self.assertEqual(violations("```text\nB owns X\n```"), [])

if __name__ == "__main__":
    unittest.main()
