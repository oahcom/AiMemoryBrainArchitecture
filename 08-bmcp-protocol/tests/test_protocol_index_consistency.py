from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from check_protocol_index import audit_repository, extract_message_type_definitions


REPO_ROOT = Path(__file__).resolve().parents[2]


def write_fixture(root: Path, schema: dict, rows: list[str]) -> None:
    schema_dir = root / "08-bmcp-protocol" / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)
    (schema_dir / "fixture.schema.json").write_text(
        json.dumps(schema), encoding="utf-8"
    )
    table = [
        "## Message types",
        "",
        "| Message type | Definition source | Schema | Validator | Conformance test | Status |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "## Type definitions",
    ]
    (root / "08-bmcp-protocol" / "protocol-index.md").write_text(
        "\n".join(table), encoding="utf-8"
    )


def row(
    message_type: str,
    schema: str = "schemas/fixture.schema.json",
    source: str = "fixture schema",
) -> str:
    return (
        f"| `{message_type}` | {source} | `{schema}` | — | — | "
        "SCHEMA PRESENT |"
    )


class ProtocolIndexConsistencyTests(unittest.TestCase):
    def test_00_current_repository_index_is_consistent(self):
        result = audit_repository(REPO_ROOT)
        self.assertEqual(result["schema_files"], 32)
        self.assertEqual(result["schemas_with_message_type"], 31)
        self.assertEqual(result["unique_message_types"], 22)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["extra"], [])
        self.assertEqual(result["duplicate_rows"], {})
        self.assertEqual(result["invalid_rows"], [], "\n".join(result["errors"]))

    def test_01_new_schema_message_type_without_index_row_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(
                root,
                {"properties": {"message_type": {"const": "EXISTING_MESSAGE"}}},
                [row("EXISTING_MESSAGE")],
            )
            (root / "08-bmcp-protocol" / "schemas" / "new.schema.json").write_text(
                json.dumps(
                    {"properties": {"message_type": {"const": "NEW_MESSAGE"}}}
                ),
                encoding="utf-8",
            )
            result = audit_repository(root)
            self.assertIn("NEW_MESSAGE", result["missing"])
            self.assertTrue(
                any("missing from index: NEW_MESSAGE" in error for error in result["errors"])
            )

    def test_02_index_message_type_without_schema_definition_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(
                root,
                {"properties": {"message_type": {"const": "REAL_MESSAGE"}}},
                [row("REAL_MESSAGE"), row("GHOST_MESSAGE")],
            )
            result = audit_repository(root)
            self.assertIn("GHOST_MESSAGE", result["extra"])
            self.assertTrue(
                any("does not define message_type GHOST_MESSAGE" in error for error in result["errors"])
            )

    def test_03_duplicate_index_row_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(
                root,
                {"properties": {"message_type": {"const": "ONE_MESSAGE"}}},
                [row("ONE_MESSAGE"), row("ONE_MESSAGE")],
            )
            result = audit_repository(root)
            self.assertEqual(result["duplicate_rows"]["ONE_MESSAGE"], [5, 6])

    def test_04_non_message_enum_is_not_counted(self):
        schema = {
            "properties": {
                "status": {"enum": ["ACTIVE", "INACTIVE"]},
                "outcome": {"enum": ["UNKNOWN", "IN_DOUBT"]},
                "message_type": {"type": "string"},
            }
        }
        self.assertEqual(extract_message_type_definitions(schema), {})

    def test_05_message_type_enum_and_composed_const_are_extracted(self):
        schema = {
            "properties": {
                "message_type": {
                    "oneOf": [
                        {"const": "ENUM_MESSAGE_A"},
                        {"const": "ENUM_MESSAGE_B"},
                    ]
                }
            },
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "message_type": {"enum": ["CONDITIONAL_MESSAGE"]}
                        }
                    }
                }
            ],
        }
        extracted = extract_message_type_definitions(schema)
        self.assertEqual(
            set(extracted),
            {"ENUM_MESSAGE_A", "ENUM_MESSAGE_B", "CONDITIONAL_MESSAGE"},
        )

    def test_06_invalid_schema_reference_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(
                root,
                {"properties": {"message_type": {"const": "ONE_MESSAGE"}}},
                [row("ONE_MESSAGE", "schemas/missing.schema.json")],
            )
            result = audit_repository(root)
            self.assertTrue(
                any("schema path does not exist" in error for error in result["errors"])
            )

    def test_07_invalid_definition_source_path_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_fixture(
                root,
                {"properties": {"message_type": {"const": "ONE_MESSAGE"}}},
                [row("ONE_MESSAGE", source="`missing-contract.md`")],
            )
            result = audit_repository(root)
            self.assertTrue(
                any("definition source path does not exist" in error for error in result["errors"])
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
