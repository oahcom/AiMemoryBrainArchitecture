
import hashlib
import json
import os
import subprocess
import sys
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

    def test_schema_error_unknown_with_value_is_contradiction(self):
        error = production_error({"state": "UNKNOWN", "value": "not allowed"})
        self.assertEqual(error.validator, "oneOf")
        self.assertEqual(
            checker.schema_error_code(error),
            "SCHEMA_STATE_VALUE_CONTRADICTION",
        )

    def test_schema_error_known_without_value_is_missing(self):
        error = production_error({"state": "KNOWN"})
        self.assertEqual(error.validator, "oneOf")
        self.assertEqual(
            checker.schema_error_code(error),
            "SCHEMA_KNOWN_VALUE_MISSING",
        )

    def test_schema_error_known_empty_invalid_value(self):
        error = production_error({"state": "KNOWN_EMPTY", "value": "not empty"})
        self.assertEqual(error.validator, "oneOf")
        self.assertEqual(
            checker.schema_error_code(error),
            "SCHEMA_KNOWN_EMPTY_INVALID",
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


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "ci" / "check_work_item_registry.py"
PRODUCTION_SCHEMA = REPO_ROOT / SCHEMA_PATH
MANIFEST_PREFIX = "14-ai-development/work-items/"
INVENTORY_PATH = "00-governance/registry-migration/inventory.yaml"


def production_record(work_item_id: str = "AID-2026-001") -> dict:
    return {
        "schema_version": 1,
        "work_item_id": work_item_id,
        "title": {"state": "KNOWN", "value": "Registry fixture record"},
        "owner": {
            "accountable_owner": {"state": "KNOWN", "value": "owner"},
            "attribution": {"state": "KNOWN", "value": "attribution"},
            "authority": {"state": "KNOWN", "value": "authority"},
            "resolution": "SINGLE_SOURCE",
        },
        "class": {"state": "KNOWN", "value": "GOVERNANCE"},
        "risk": {"state": "KNOWN", "value": "LOW"},
        "status": {"state": "KNOWN", "value": "PROPOSED"},
        "prompt": {
            "prompt_status": "NOT_PRESENT",
            "prompt_id": {"state": "UNKNOWN"},
            "prompt_sha256": {"state": "UNKNOWN"},
            "prompt_path": {"state": "UNKNOWN"},
            "prompt_version": {"state": "UNKNOWN"},
            "prompt_commit_sha": {"state": "UNKNOWN"},
            "provenance_note": {"state": "UNKNOWN"},
        },
        "provenance": {"grade": "PRIMARY", "evidence": []},
        "supersedes": {"state": "KNOWN_EMPTY", "value": []},
        "superseded_by": {"state": "KNOWN_EMPTY", "value": []},
        "source_refs": [],
    }


def production_error(title_value: dict):
    schema = json.loads(PRODUCTION_SCHEMA.read_text(encoding="utf-8"))
    record = production_record()
    record["title"] = title_value
    errors = list(Draft202012Validator(schema).iter_errors(record))
    if len(errors) != 1:
        raise AssertionError(f"expected one error, got {errors!r}")
    return errors[0]


class RegistryCliTestCase(unittest.TestCase):
    """End-to-end fixtures: real Git tree -> CLI -> JSONL -> exit code."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "user.name", "Registry E2E")
        self.git("config", "user.email", "registry-e2e@example.invalid")
        self.commit_sha = ""

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args: str, input_bytes: bytes | None = None) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repo), *args],
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

    def write_file(self, path: str, content: bytes | str) -> None:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8") if isinstance(content, str) else content
        target.write_bytes(data)

    def commit_all(self, message: str = "fixture") -> str:
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        self.commit_sha = self.git("rev-parse", "HEAD")
        return self.commit_sha

    def install_schema(self) -> None:
        self.write_file(SCHEMA_PATH, PRODUCTION_SCHEMA.read_bytes())

    def valid_record(self, work_item_id: str = "AID-2026-001") -> dict:
        return production_record(work_item_id)

    def write_registry(
        self,
        record: dict | None = None,
        name: str = "AID-2026-001.yaml",
    ) -> str:
        path = f"00-governance/registry/{name}"
        document = record if record is not None else self.valid_record()
        self.write_file(path, yaml.safe_dump(document, sort_keys=False))
        return path

    def write_manifest(self, work_item_id: str = "AID-2026-001") -> str:
        path = f"{MANIFEST_PREFIX}{work_item_id}/manifest.yaml"
        self.write_file(path, f"work_item_id: {work_item_id}\n")
        return path

    def write_inventory(self, entries: list[dict]) -> str:
        document = {
            "inventory_version": 1,
            "source_prefix": MANIFEST_PREFIX,
            "source_tree": "HEAD",
            "entries": entries,
        }
        self.write_file(
            INVENTORY_PATH,
            yaml.safe_dump(document, sort_keys=False),
        )
        return INVENTORY_PATH

    def run_checker(self, *args: str, tree: str | None = None):
        result = subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--tree",
                tree or self.commit_sha,
                "--root",
                str(self.repo),
                "--jsonl",
                *args,
            ],
            cwd=self.repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        records = [
            json.loads(line)
            for line in result.stdout.splitlines()
            if line.strip()
        ]
        self.assertTrue(records, msg=result.stderr)
        self.assertEqual(records[-1]["type"], "summary")
        self.assertEqual(
            len([item for item in records if item.get("type") == "summary"]),
            1,
        )
        return result, records

    def assert_event(self, records, code):
        matches = [
            item for item in records[:-1] if item.get("code") == code
        ]
        self.assertTrue(
            matches,
            msg=f"Expected event {code}; got {records!r}",
        )
        return matches

    def assert_summary(self, result, records, *, overall, exit_code):
        summary = records[-1]
        self.assertEqual(summary["overall"], overall)
        self.assertEqual(summary["exit_code"], exit_code)
        self.assertEqual(result.returncode, exit_code)
        self.assertEqual(
            len(summary),
            14,
            msg=f"Summary keys changed: {sorted(summary)}",
        )
        return summary


class TestRegistryEndToEnd(RegistryCliTestCase):
    def test_empty_registry_required_passes(self):
        self.install_schema()
        self.commit_all()
        result, records = self.run_checker()
        summary = self.assert_summary(result, records, overall="PASS", exit_code=0)
        self.assertEqual(summary["registry_files"], 0)
        self.assert_event(records, "REGISTRY_SCAN_COMPLETE")

    def test_empty_registry_diagnostic_not_applicable(self):
        self.install_schema()
        self.commit_all()
        result, records = self.run_checker("--mode", "diagnostic")
        summary = self.assert_summary(
            result,
            records,
            overall="NOT_APPLICABLE",
            exit_code=5,
        )
        self.assertEqual(summary["registry_files"], 0)

    def test_single_valid_registry_record_passes(self):
        self.install_schema()
        self.write_registry()
        self.commit_all()
        result, records = self.run_checker()
        summary = self.assert_summary(result, records, overall="PASS", exit_code=0)
        self.assertEqual(summary["registry_files"], 1)
        self.assertEqual(summary["schema_valid"], 1)
        self.assertEqual(summary["violations"], 0)
        self.assertEqual(summary["incomplete"], 0)

    def test_duplicate_work_item_id_across_two_paths(self):
        self.install_schema()
        expected_id = "AID-2026-001"
        first = self.write_registry(name=f"{expected_id}.yaml")
        second = self.write_registry(name=f"{expected_id}.yml")
        self.commit_all()
        result, records = self.run_checker()
        summary = self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        self.assertEqual(summary["duplicate_ids"], 1)
        events = self.assert_event(records, "DUPLICATE_WORK_ITEM_ID")
        self.assertEqual(events[0]["work_item_id"], expected_id)
        self.assertEqual(events[0]["paths"], sorted([first, second]))

    def test_registry_path_identity_mismatch(self):
        self.install_schema()
        self.write_registry(record=self.valid_record("AID-2026-002"))
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "REGISTRY_PATH_ID_MISMATCH")
        self.assertEqual(events[0]["expected_id"], "AID-2026-001")
        self.assertEqual(events[0]["work_item_id"], "AID-2026-002")

    def test_registry_yaml_parse_failure(self):
        self.install_schema()
        self.write_file("00-governance/registry/AID-2026-001.yaml", "work_item_id: [\n")
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="INCOMPLETE", exit_code=2)
        events = self.assert_event(records, "REGISTRY_PARSE_ERROR")
        self.assertEqual(events[0]["status"], "INCOMPLETE")

    def test_registry_blob_read_failure(self):
        self.install_schema()
        self.commit_all()
        schema_oid = self.git(
            "rev-parse",
            f"HEAD:{SCHEMA_PATH}",
        )
        missing_oid = "0" * 40
        registry_tree = self.git(
            "mktree",
            "--missing",
            input_bytes=f"100644 blob {missing_oid}\tAID-2026-001.yaml\n".encode(),
        )
        schemas_tree = self.git(
            "mktree",
            input_bytes=(
                f"100644 blob {schema_oid}\twork-item-registry.schema.json\n"
            ).encode(),
        )
        governance_tree = self.git(
            "mktree",
            input_bytes=(
                f"040000 tree {schemas_tree}\tschemas\n"
                f"040000 tree {registry_tree}\tregistry\n"
            ).encode(),
        )
        root_tree = self.git(
            "mktree",
            input_bytes=f"040000 tree {governance_tree}\t00-governance\n".encode(),
        )
        broken_commit = self.git("commit-tree", root_tree, "-m", "missing blob")

        result, records = self.run_checker(tree=broken_commit)
        self.assert_summary(result, records, overall="INCOMPLETE", exit_code=2)
        events = self.assert_event(records, "REGISTRY_BLOB_UNREADABLE")
        self.assertEqual(events[0]["status"], "INCOMPLETE")
        self.assertEqual(
            events[0]["path"],
            "00-governance/registry/AID-2026-001.yaml",
        )
        self.assertTrue(events[0]["detail"])
        self.assertNotIn(
            "REGISTRY_PARSE_ERROR",
            [item.get("code") for item in records[:-1]],
        )

    def test_enum_out_of_range(self):
        self.install_schema()
        record = self.valid_record()
        record["owner"]["resolution"] = "NOT_A_RESOLUTION"
        self.write_registry(record=record)
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "SCHEMA_ENUM_OUT_OF_RANGE")
        self.assertEqual(events[0]["status"], "VIOLATION")

    def test_undeclared_property_rejected(self):
        self.install_schema()
        record = self.valid_record()
        record["extra_field"] = "not declared"
        self.write_registry(record=record)
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "SCHEMA_ADDITIONAL_PROPERTY")
        self.assertEqual(events[0]["status"], "VIOLATION")

    def test_unknown_state_with_value_rejected(self):
        self.install_schema()
        record = self.valid_record()
        record["title"] = {"state": "UNKNOWN", "value": "not allowed"}
        self.write_registry(record=record)
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "SCHEMA_STATE_VALUE_CONTRADICTION")
        self.assertEqual(events[0]["status"], "VIOLATION")

    def test_known_state_without_value_rejected(self):
        self.install_schema()
        record = self.valid_record()
        record["title"] = {"state": "KNOWN"}
        self.write_registry(record=record)
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "SCHEMA_KNOWN_VALUE_MISSING")
        self.assertEqual(events[0]["status"], "VIOLATION")

    def test_known_empty_invalid_value_rejected(self):
        self.install_schema()
        record = self.valid_record()
        record["title"] = {"state": "KNOWN_EMPTY", "value": "not empty"}
        self.write_registry(record=record)
        self.commit_all()
        result, records = self.run_checker()
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "SCHEMA_KNOWN_EMPTY_INVALID")
        self.assertEqual(events[0]["status"], "VIOLATION")

    def _pinned_record(self, prompt_bytes: bytes, commit_sha: str, **prompt_overrides):
        record = self.valid_record()
        prompt = {
            "prompt_status": "PINNED",
            "prompt_id": {"state": "KNOWN", "value": "PROMPT-FIXTURE-1"},
            "prompt_sha256": {
                "state": "KNOWN",
                "value": hashlib.sha256(prompt_bytes).hexdigest(),
            },
            "prompt_path": {"state": "KNOWN", "value": "prompts/example.md"},
            "prompt_version": {"state": "KNOWN", "value": "v1"},
            "prompt_commit_sha": {"state": "KNOWN", "value": commit_sha},
            "provenance_note": {"state": "UNKNOWN"},
        }
        prompt.update(prompt_overrides)
        record["prompt"] = prompt
        return record

    def _commit_prompt(self) -> tuple[bytes, str]:
        prompt_bytes = b"# fixture prompt\nbody line\n"
        self.write_file("prompts/example.md", prompt_bytes)
        return prompt_bytes, self.commit_all("prompt")

    def test_pinned_prompt_correct_digest_passes(self):
        self.install_schema()
        prompt_bytes, prompt_commit = self._commit_prompt()
        self.write_registry(record=self._pinned_record(prompt_bytes, prompt_commit))
        self.commit_all("registry")
        result, records = self.run_checker()
        summary = self.assert_summary(result, records, overall="PASS", exit_code=0)
        self.assertEqual(summary["prompt_pins_checked"], 1)
        self.assertEqual(summary["prompt_pins_failed"], 0)
        self.assert_event(records, "PROMPT_PIN_VALID")

    def test_pinned_prompt_wrong_digest_fails(self):
        self.install_schema()
        prompt_bytes, prompt_commit = self._commit_prompt()
        self.write_registry(
            record=self._pinned_record(
                prompt_bytes,
                prompt_commit,
                prompt_sha256={"state": "KNOWN", "value": "a" * 64},
            )
        )
        self.commit_all("registry")
        result, records = self.run_checker()
        summary = self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        self.assertEqual(summary["prompt_pins_checked"], 1)
        self.assertEqual(summary["prompt_pins_failed"], 1)
        events = self.assert_event(records, "PROMPT_PIN_SHA256_MISMATCH")
        self.assertEqual(events[0]["status"], "VIOLATION")

    def test_pinned_prompt_missing_path_is_incomplete(self):
        # Current implementation intentionally classifies both an absent
        # prompt path and an unreadable commit/blob as
        # PROMPT_PIN_BLOB_UNREADABLE / INCOMPLETE.
        self.install_schema()
        prompt_bytes, prompt_commit = self._commit_prompt()
        self.write_registry(
            record=self._pinned_record(
                prompt_bytes,
                prompt_commit,
                prompt_path={"state": "KNOWN", "value": "prompts/missing.md"},
            )
        )
        self.commit_all("registry")
        result, records = self.run_checker()
        summary = self.assert_summary(result, records, overall="INCOMPLETE", exit_code=2)
        self.assertEqual(summary["prompt_pins_checked"], 1)
        self.assertEqual(summary["prompt_pins_failed"], 1)
        self.assertEqual(summary["incomplete"], True)
        events = self.assert_event(records, "PROMPT_PIN_BLOB_UNREADABLE")
        self.assertEqual(events[0]["status"], "INCOMPLETE")
        self.assertEqual(events[0]["prompt_path"], "prompts/missing.md")
        self.assertNotIn(
            "PROMPT_PIN_PATH_MISSING",
            [item.get("code") for item in records[:-1]],
        )

    def test_manifest_discovered_but_not_registered(self):
        self.install_schema()
        self.write_registry()
        manifest = self.write_manifest()
        self.write_inventory([])
        self.commit_all()
        result, records = self.run_checker("--strict-inventory")
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "INVENTORY_ENTRY_MISSING")
        self.assertEqual(events[0]["status"], "VIOLATION")
        self.assertEqual(events[0]["work_item_id"], "AID-2026-001")
        self.assertEqual(events[0]["source_manifest"], manifest)

    def test_not_migrated_without_registry_file(self):
        self.install_schema()
        manifest = self.write_manifest()
        self.write_inventory(
            [
                {
                    "work_item_id": "AID-2026-001",
                    "migration_state": "NOT_MIGRATED",
                    "source_manifest": manifest,
                    "registry_path": None,
                }
            ]
        )
        self.commit_all()
        result, records = self.run_checker("--strict-inventory")
        summary = self.assert_summary(result, records, overall="PASS", exit_code=0)
        self.assertEqual(summary["violations"], 0)
        self.assertEqual(summary["incomplete"], 0)
        self.assert_event(records, "INVENTORY_CONSISTENT")

    def test_migrated_missing_registry_file(self):
        self.install_schema()
        manifest = self.write_manifest()
        self.write_inventory(
            [
                {
                    "work_item_id": "AID-2026-001",
                    "migration_state": "MIGRATED",
                    "source_manifest": manifest,
                    "registry_path": None,
                }
            ]
        )
        self.commit_all()
        result, records = self.run_checker("--strict-inventory")
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "MIGRATED_RECORD_MISSING")
        self.assertEqual(events[0]["status"], "VIOLATION")
        self.assertEqual(events[0]["work_item_id"], "AID-2026-001")

    def test_strict_inventory_unreadable_is_incomplete(self):
        self.install_schema()
        self.write_registry()
        self.commit_all()
        result, records = self.run_checker("--strict-inventory")
        summary = self.assert_summary(result, records, overall="INCOMPLETE", exit_code=2)
        self.assertEqual(summary["incomplete"], True)
        self.assertGreater(summary["incomplete_checks"], 0)
        events = self.assert_event(records, "INVENTORY_UNAVAILABLE_OR_INVALID")
        self.assertEqual(events[0]["status"], "INCOMPLETE")
        self.assertTrue(events[0]["path"])
        self.assertTrue(events[0]["detail"])

    def test_not_migrated_with_registry_record_is_state_mismatch(self):
        self.install_schema()
        registry_path = self.write_registry()
        manifest = self.write_manifest()
        self.write_inventory(
            [
                {
                    "work_item_id": "AID-2026-001",
                    "migration_state": "NOT_MIGRATED",
                    "source_manifest": manifest,
                    "registry_path": registry_path,
                }
            ]
        )
        self.commit_all()
        result, records = self.run_checker("--strict-inventory")
        self.assert_summary(result, records, overall="VIOLATION", exit_code=1)
        events = self.assert_event(records, "INVENTORY_REGISTRY_STATE_MISMATCH")
        self.assertEqual(events[0]["status"], "VIOLATION")
        self.assertEqual(events[0]["work_item_id"], "AID-2026-001")


if __name__ == "__main__":
    unittest.main()
