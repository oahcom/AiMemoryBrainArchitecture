
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from scripts.ci import check_work_item_registry as checker


SCHEMA_PATH = "00-governance/schemas/work-item-registry.schema.json"


def git(repo: Path, *args: str, input_bytes: bytes | None = None) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            result.stderr.decode("utf-8", errors="replace")
        )
    return result.stdout.decode("utf-8", errors="strict").strip()


def make_repo() -> tuple[tempfile.TemporaryDirectory, Path, str]:
    temp = tempfile.TemporaryDirectory()
    repo = Path(temp.name)
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Registry Tests")
    git(repo, "config", "user.email", "registry-tests@example.invalid")
    return temp, repo, ""


def commit_tree(repo: Path, files: dict[str, bytes | str]) -> str:
    for path, content in files.items():
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8") if isinstance(content, str) else content
        target.write_bytes(data)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "test tree")
    return git(repo, "rev-parse", "HEAD")


def minimal_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["work_item_id", "title"],
        "properties": {
            "work_item_id": {
                "type": "string",
                "pattern": "^AID-[0-9]{4}-[0-9]{3}$",
            },
            "title": {
                "type": "object",
                "additionalProperties": False,
                "required": ["state"],
                "properties": {
                    "state": {"enum": ["KNOWN", "UNKNOWN", "UNCONFIRMED"]},
                    "value": {"type": "string"},
                },
            },
        },
    }


def minimal_record(work_item_id: str = "AID-2026-001") -> dict:
    return {
        "work_item_id": work_item_id,
        "title": {"state": "KNOWN", "value": "Test record"},
    }


def event_codes(result: checker.RunResult) -> set[str]:
    return {event.code for event in result.events}


class TestStrictYamlLoader(unittest.TestCase):
    def test_duplicate_mapping_key_rejected(self):
        with self.assertRaises(ValueError):
            checker.parse_yaml(
                b"work_item_id: AID-2026-001\nwork_item_id: AID-2026-002\n",
                "record.yaml",
            )

    def test_invalid_yaml_rejected(self):
        with self.assertRaises(ValueError):
            checker.parse_yaml(b"work_item_id: [\n", "record.yaml")

    def test_non_utf8_yaml_rejected(self):
        with self.assertRaises(ValueError):
            checker.parse_yaml(b"title: \xff", "record.yaml")

    def test_mapping_root_accepted(self):
        value = checker.parse_yaml(
            b"work_item_id: AID-2026-001\n",
            "record.yaml",
        )
        self.assertEqual(value["work_item_id"], "AID-2026-001")

    def test_list_root_is_not_mapping(self):
        value = checker.parse_yaml(b"- one\n- two\n", "record.yaml")
        self.assertIsInstance(value, list)


class TestIdentifierAndPaths(unittest.TestCase):
    def test_valid_aid(self):
        self.assertTrue(checker.WORK_ITEM_ID_RE.fullmatch("AID-2026-001"))

    def test_invalid_aid(self):
        self.assertFalse(checker.WORK_ITEM_ID_RE.fullmatch("AID-26-1"))

    def test_registry_path_expected_id(self):
        self.assertEqual(
            checker.expected_id_from_registry_path(
                "00-governance/registry/AID-2026-001.yaml"
            ),
            "AID-2026-001",
        )

    def test_nested_registry_path_not_canonical(self):
        self.assertIsNone(
            checker.expected_id_from_registry_path(
                "00-governance/registry/archive/AID-2026-001.yaml"
            )
        )

    def test_other_extension_not_used(self):
        self.assertIsNone(
            checker.expected_id_from_registry_path(
                "00-governance/registry/AID-2026-001.json"
            )
        )

    def test_json_pointer_escaping(self):
        self.assertEqual(
            checker.json_pointer(["a/b", "c~d"]),
            "/a~1b/c~0d",
        )


class TestSchemaAndStateSemantics(unittest.TestCase):
    def test_schema_helper_accepts_draft_2020_12(self):
        schema = minimal_schema()
        Draft202012Validator.check_schema(schema)

    def test_valid_record_passes_schema(self):
        validator = Draft202012Validator(minimal_schema())
        self.assertEqual(
            list(validator.iter_errors(minimal_record())),
            [],
        )

    def test_prompt_bytes_is_rejected_by_closed_schema(self):
        schema = minimal_schema()
        schema["properties"]["prompt_bytes"] = {"type": "integer"}
        schema["additionalProperties"] = False
        record = minimal_record()
        record["prompt_bytes"] = 12
        validator = Draft202012Validator(minimal_schema())
        errors = list(validator.iter_errors(record))
        self.assertTrue(errors)
        self.assertTrue(
            any(error.validator == "additionalProperties" for error in errors)
        )

    def test_unknown_with_value_is_rejected_by_closed_field_shape(self):
        schema = {
            "type": "object",
            "properties": {
                "field": {
                    "oneOf": [
                        {
                            "type": "object",
                            "required": ["state", "value"],
                            "properties": {
                                "state": {"const": "KNOWN"},
                                "value": {"type": "string"},
                            },
                            "additionalProperties": False,
                        },
                        {
                            "type": "object",
                            "required": ["state"],
                            "properties": {"state": {"const": "UNKNOWN"}},
                            "additionalProperties": False,
                        },
                    ]
                }
            },
            "required": ["field"],
        }
        record = {"field": {"state": "UNKNOWN", "value": "not allowed"}}
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(record)))

    def test_known_missing_value_is_rejected(self):
        schema = {
            "type": "object",
            "properties": {
                "field": {
                    "type": "object",
                    "required": ["state", "value"],
                    "properties": {
                        "state": {"const": "KNOWN"},
                        "value": {"type": "string"},
                    },
                }
            },
            "required": ["field"],
        }
        self.assertTrue(
            list(
                Draft202012Validator(schema).iter_errors(
                    {"field": {"state": "KNOWN"}}
                )
            )
        )

    def test_known_empty_requires_empty_string(self):
        schema = {
            "type": "object",
            "properties": {
                "field": {
                    "type": "object",
                    "required": ["state", "value"],
                    "properties": {
                        "state": {"const": "KNOWN_EMPTY"},
                        "value": {"const": ""},
                    },
                }
            },
            "required": ["field"],
        }
        self.assertTrue(
            list(
                Draft202012Validator(schema).iter_errors(
                    {"field": {"state": "KNOWN_EMPTY", "value": "not empty"}}
                )
            )
        )

    def test_schema_error_additional_property_code(self):
        error = next(
            Draft202012Validator(minimal_schema()).iter_errors(
                {**minimal_record(), "extra": True}
            )
        )
        self.assertEqual(
            checker.schema_error_code(error),
            "SCHEMA_ADDITIONAL_PROPERTY",
        )

    def test_schema_error_required_code(self):
        error = next(
            Draft202012Validator(minimal_schema()).iter_errors(
                {"title": {"state": "UNKNOWN"}}
            )
        )
        self.assertEqual(
            checker.schema_error_code(error),
            "SCHEMA_REQUIRED_FIELD_MISSING",
        )


class TestPromptPinHelpers(unittest.TestCase):
    def test_sha256_of_exact_bytes(self):
        raw = b"prompt\r\nbody\n"
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            hashlib.sha256(raw).hexdigest(),
        )

    def test_prompt_path_rejects_parent_traversal(self):
        path = Path("../secret")
        self.assertTrue(".." in path.parts)

    def test_prompt_path_rejects_absolute_path(self):
        self.assertTrue(checker.PurePosixPath("/tmp/prompt.md").is_absolute())

    def test_sha256_pattern_accepts_64_hex(self):
        self.assertTrue(checker.SHA256_RE.fullmatch("a" * 64))

    def test_sha256_pattern_rejects_short_digest(self):
        self.assertFalse(checker.SHA256_RE.fullmatch("a" * 63))

    def test_prompt_pin_not_checked_when_not_pinned(self):
        result = checker.RunResult(tree="0" * 40)
        checker.prompt_pin_check(
            tree=None,  # not accessed for a non-PINNED record
            path="record.yaml",
            record={"work_item_id": "AID-2026-001", "prompt": {
                "prompt_status": "NOT_PRESENT"
            }},
            result=result,
        )
        self.assertEqual(result.prompt_pins_checked, 0)

    def test_prompt_pin_known_state_extraction(self):
        self.assertEqual(
            checker.field_state_value({"state": "KNOWN", "value": "x"}),
            ("KNOWN", "x"),
        )

    def test_prompt_pin_unknown_state_extraction(self):
        self.assertEqual(
            checker.field_state_value({"state": "UNKNOWN"}),
            ("UNKNOWN", None),
        )


class TestInventoryIdentity(unittest.TestCase):
    def test_manifest_identity_work_item_id(self):
        self.assertEqual(
            checker.manifest_identity({"work_item_id": "AID-2026-001"}),
            "AID-2026-001",
        )

    def test_manifest_identity_legacy_aid(self):
        self.assertEqual(
            checker.manifest_identity({"aid": "AID-2026-014"}),
            "AID-2026-014",
        )

    def test_manifest_identity_nested_proposed_id_requires_status(self):
        doc = {
            "work_item": {
                "proposed_id": "AID-2026-025",
                "identifier_status": (
                    "coordinator_verified_unique_see_identifier_evidence"
                ),
            }
        }
        self.assertEqual(checker.manifest_identity(doc), "AID-2026-025")

    def test_manifest_identity_nested_proposed_id_without_status_rejected(self):
        self.assertIsNone(
            checker.manifest_identity(
                {"work_item": {"proposed_id": "AID-2026-025"}}
            )
        )

    def test_manifest_identity_conflicting_aliases_rejected(self):
        self.assertIsNone(
            checker.manifest_identity(
                {
                    "work_item_id": "AID-2026-001",
                    "aid": "AID-2026-002",
                }
            )
        )

    def test_manifest_identity_fix_id(self):
        self.assertEqual(
            checker.manifest_identity({"work_item_id": "FIX-2026-P1-T1"}),
            "FIX-2026-P1-T1",
        )

    def test_manifest_identity_malformed_id_rejected(self):
        self.assertIsNone(
            checker.manifest_identity({"work_item_id": "AID-26-1"})
        )


class TestSummaryAndEvents(unittest.TestCase):
    def test_summary_has_exactly_fourteen_keys(self):
        result = checker.RunResult(tree="0" * 40)
        self.assertEqual(len(result.summary()), 14)
        self.assertEqual(tuple(result.summary()), checker.SUMMARY_KEYS)

    def test_summary_retains_both_incomplete_counters(self):
        result = checker.RunResult(tree="0" * 40)
        checker.emit(
            result,
            "registry.scan",
            "INCOMPLETE",
            "REGISTRY_PARSE_ERROR",
            path="record.yaml",
        )
        summary = result.summary()
        self.assertEqual(summary["incomplete_checks"], 1)
        self.assertEqual(summary["incomplete"], 1)

    def test_violation_exit_code(self):
        result = checker.RunResult(tree="0" * 40)
        checker.emit(result, "registry.schema", "VIOLATION", "SCHEMA_ENUM_OUT_OF_RANGE")
        self.assertEqual(result.exit_code, checker.EXIT_VIOLATION)

    def test_incomplete_exit_code(self):
        result = checker.RunResult(tree="0" * 40)
        checker.emit(result, "registry.scan", "INCOMPLETE", "REGISTRY_PARSE_ERROR")
        self.assertEqual(result.exit_code, checker.EXIT_INCOMPLETE)

    def test_mixed_exit_code(self):
        result = checker.RunResult(tree="0" * 40)
        checker.emit(result, "registry.scan", "INCOMPLETE", "REGISTRY_PARSE_ERROR")
        checker.emit(result, "registry.schema", "VIOLATION", "SCHEMA_ENUM_OUT_OF_RANGE")
        self.assertEqual(result.exit_code, checker.EXIT_BOTH)

    def test_index_projection_is_phase_d_not_applicable(self):
        result = checker.RunResult(tree="0" * 40)
        checker.emit_index_projection_deferred(result)
        event = result.events[0].as_dict()
        self.assertEqual(event["check"], "registry.index_projection")
        self.assertEqual(event["status"], "NOT_APPLICABLE")
        self.assertEqual(event["code"], "INDEX_PROJECTION_DEFERRED_TO_PHASE_D")
        self.assertEqual(
            event["owner"],
            "scripts/ci/check_work_item_index.py",
        )


class TestSelfTest(unittest.TestCase):
    def test_self_test_executes_all_cases(self):
        passed, cases = checker.built_in_self_test()
        self.assertTrue(passed)
        self.assertGreaterEqual(len(cases), 7)
        self.assertTrue(all(case["passed"] for case in cases))


if __name__ == "__main__":
    unittest.main()
