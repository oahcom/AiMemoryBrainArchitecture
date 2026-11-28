import copy
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_aid_2026_293_carriers import validate


def valid_data():
    risk_ids = [f"R-{i:02d}" for i in range(1, 11)]
    module_ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "Storage"]
    return {
        "work_item_id": "AID-2026-293",
        "risks": [
            {
                "id": rid,
                "evidence_state": "PENDING_SEARCH_EXECUTION",
                "planned_search_command": "git grep -n pattern baseline -- docs",
            }
            for rid in risk_ids
        ],
        "modules": [
            {
                "id": mid,
                "scores": {
                    "change_surface": 3,
                    "coupling": 3,
                    "irreversibility": 3,
                    "concurrency_state": 3,
                },
                "evidence_gap": "EVIDENCE_GAP: fixture intentionally lacks source proof.",
            }
            for mid in module_ids
        ],
        "statuses": {
            "ac6_negative_cases": "PENDING_COORDINATOR_EXECUTION",
            "ac8_independent_review": "PENDING_INDEPENDENT_REVIEW",
        },
    }


class CarrierRulesTest(unittest.TestCase):
    def assert_rule(self, data, rule, root=None):
        errors = validate(data, root=root)
        self.assertTrue(any(item.startswith(rule + " ") for item in errors), errors)

    def path_line_fixture(self, temp_root, path_line, quote):
        data = valid_data()
        data["risks"][0] = {
            "id": "R-01",
            "evidence_state": "PATH_LINE",
            "path_line": path_line,
            "quote": quote,
        }
        return data

    def test_positive(self):
        self.assertEqual(validate(valid_data()), [])

        repo_root = Path(__file__).resolve().parents[2]
        carrier_path = (
            repo_root
            / "14-ai-development"
            / "work-items"
            / "AID-2026-293"
            / "carrier-data.yaml"
        )
        self.assertTrue(carrier_path.is_file(), f"missing real carrier file: {carrier_path}")
        carrier_data = yaml.safe_load(carrier_path.read_text(encoding="utf-8"))
        self.assertEqual(validate(carrier_data, root=repo_root), [])

    def test_negative_r1_wrong_work_item(self):
        data = valid_data()
        data["work_item_id"] = "AID-2026-999"
        self.assert_rule(data, "R1_WORK_ITEM_ID")

    def test_negative_r2_missing_risk(self):
        data = valid_data()
        data["risks"].pop()
        self.assert_rule(data, "R2_RISK_REGISTER")

    def test_negative_r3_no_evidence_without_executed_search(self):
        data = valid_data()
        data["risks"][0] = {
            "id": "R-01",
            "evidence_state": "NO_EVIDENCE_FOUND",
            "search_command": "git grep -n token",
            "search_scope": "docs/",
            "search_executed": False,
        }
        self.assert_rule(data, "R3_RISK_EVIDENCE_STATE")

    def test_negative_r4_missing_module(self):
        data = valid_data()
        data["modules"].pop()
        self.assert_rule(data, "R4_MODULE_COVERAGE")

    def test_negative_r5_out_of_range_score(self):
        data = valid_data()
        data["modules"][0]["scores"]["coupling"] = 6
        self.assert_rule(data, "R5_FOUR_DIMENSION_SCORES")

    def test_negative_r6_missing_module_evidence(self):
        data = valid_data()
        data["modules"][0].pop("evidence_gap")
        self.assert_rule(data, "R6_MODULE_EVIDENCE")

    def test_negative_r7_false_pending_state(self):
        data = valid_data()
        data["statuses"]["ac8_independent_review"] = "APPROVED"
        self.assert_rule(data, "R7_AC6_AC8_PENDING")

    def test_negative_r8_source_file_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data = self.path_line_fixture(
                root,
                "missing/source.md:1",
                "A source line that does not exist.",
            )
            self.assert_rule(data, "R8_PATH_EXISTS", root=root)

    def test_negative_r9_line_out_of_range(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            source.write_text("The only source line.\n", encoding="utf-8")
            data = self.path_line_fixture(
                root,
                "source.md:2",
                "The only source line.",
            )
            self.assert_rule(data, "R9_LINE_IN_RANGE", root=root)

    def test_negative_r10_quote_not_equal_to_whole_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            source.write_text("The complete source line has extra words.\n", encoding="utf-8")
            data = self.path_line_fixture(
                root,
                "source.md:1",
                "The complete source line",
            )
            self.assert_rule(data, "R10_QUOTE_MATCHES_LINE", root=root)


if __name__ == "__main__":
    unittest.main()
