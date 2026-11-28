from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ci" / "autofill_work_item_manifests.py"

spec = importlib.util.spec_from_file_location("autofill_work_item_manifests", SCRIPT)
autofill = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = autofill
spec.loader.exec_module(autofill)


SCHEMA = {
    "required_top_level_keys": ["documentation", "implementation"],
    "fields": {
        "documentation": {
            "relationship_enum": [
                "normative",
                "design",
                "implementation",
                "evidence",
                "reference",
                "code",
                "schema",
            ]
        },
        "implementation": {
            "status_enum": [
                "NOT_STARTED",
                "IN_PROGRESS",
                "IMPLEMENTED",
                "BLOCKED",
                "NOT_APPLICABLE",
            ]
        },
    },
}


def finding(manifest, rule, pointer="", category="required", message="missing"):
    return {
        "manifest": manifest,
        "rule": rule,
        "pointer": pointer,
        "category": category,
        "message": message,
    }


def make_root(tmp_path, manifest_text, extra_files=None):
    manifest = tmp_path / "14-ai-development/work-items/AID-TEST/manifest.yaml"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(manifest_text, encoding="utf-8")

    for relative, content in (extra_files or {}).items():
        path = manifest.parent / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    return manifest


def test_no_verifiable_source_is_blocked(tmp_path):
    manifest = make_root(
        tmp_path,
        "work_item_id: AID-TEST\n"
        "title: Test\n"
        "scope:\n"
        "  objective: ''\n",
    )
    original = manifest.read_bytes()

    result = autofill.build_proposals(
        tmp_path,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "top_level.date.required",
                "/date",
            ),
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "top_level.risk_rationale.required",
                "/risk_rationale",
            ),
        ],
        SCHEMA,
    )

    entries = result["manifests"][0]["findings"]
    assert len(entries) == 2
    assert all(entry["status"] == "BLOCKED" for entry in entries)
    assert all(entry["proposed_value"] is None for entry in entries)
    assert manifest.read_bytes() == original
    assert result["files_written"] == 0


def test_stage_one_does_not_write_manifest_files(tmp_path):
    manifest = make_root(
        tmp_path,
        "work_item_id: AID-TEST\n"
        "title: Test\n"
        "scope:\n"
        "  objective: A verifiable objective.\n",
        {"evidence.md": "# Evidence\n"},
    )
    original = manifest.read_bytes()

    result = autofill.build_proposals(
        tmp_path,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "top_level.documentation.required",
                "/documentation",
            ),
        ],
        SCHEMA,
    )

    assert result["files_written"] == 0
    assert manifest.read_bytes() == original
    assert result["manifests"][0]["findings"][0]["status"] == "PROPOSED"


def test_forward_and_reverse_diffs_are_reversible_pairs(tmp_path):
    manifest = make_root(
        tmp_path,
        "work_item_id: AID-TEST\n"
        "title: Test\n"
        "scope:\n"
        "  objective: A verifiable objective.\n",
        {"evidence.md": "# Evidence\n"},
    )
    original_text = manifest.read_text(encoding="utf-8")

    result = autofill.build_proposals(
        tmp_path,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "top_level.documentation.required",
                "/documentation",
            ),
        ],
        SCHEMA,
    )

    item = result["manifests"][0]
    proposed_document = autofill.load_yaml(manifest)
    autofill.apply_operation(
        proposed_document,
        item["findings"][0]["operation"],
    )
    proposed_text = autofill.render_yaml(proposed_document)

    expected_forward, expected_reverse = autofill.make_diff(
        item["manifest"],
        original_text,
        proposed_text,
    )

    assert item["diff"] == expected_forward
    assert item["reverse_diff"] == expected_reverse
    assert item["diff"].startswith("--- a/")
    assert item["reverse_diff"].startswith("--- b/")
    assert item["before_sha256"] == autofill.sha256(original_text)
    assert item["proposed_sha256"] == autofill.sha256(proposed_text)


def test_out_of_enum_value_is_identified_and_blocked(tmp_path):
    make_root(
        tmp_path,
        "work_item_id: AID-TEST\n"
        "title: Test\n"
        "implementation:\n"
        "  status: DONE\n",
    )

    result = autofill.build_proposals(
        tmp_path,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "implementation.status.enum",
                "/implementation/status",
                category="enum",
                message="status is outside schema enum",
            ),
        ],
        SCHEMA,
    )

    entry = result["manifests"][0]["findings"][0]
    assert entry["status"] == "BLOCKED"
    assert "outside schema enum" in entry["reason"]
    assert entry["source"]["type"] == "schema"
    assert "DONE" in entry["reason"]
    assert "IMPLEMENTED" in entry["source"]["allowed_values"]


def test_each_finding_has_exactly_one_proposal(tmp_path):
    make_root(
        tmp_path,
        "work_item_id: AID-TEST\n"
        "title: Test\n"
        "scope:\n"
        "  objective: Verify the test fixture.\n"
        "  files_to_modify:\n"
        "    - src/example.py\n"
        "implementation:\n"
        "  tests:\n"
        "    - python -m pytest -q\n",
        {
            "evidence.md": "# Evidence\n",
            "src/example.py": "VALUE = 1\n",
        },
    )

    findings = [
        finding(
            "14-ai-development/work-items/AID-TEST/manifest.yaml",
            "top_level.documentation.required",
            "/documentation",
        ),
        finding(
            "14-ai-development/work-items/AID-TEST/manifest.yaml",
            "implementation.required_key",
            "/implementation/summary",
        ),
        finding(
            "14-ai-development/work-items/AID-TEST/manifest.yaml",
            "implementation.required_key",
            "/implementation/files_changed",
        ),
        finding(
            "14-ai-development/work-items/AID-TEST/manifest.yaml",
            "implementation.required_key",
            "/implementation/tests",
        ),
        finding(
            "14-ai-development/work-items/AID-TEST/manifest.yaml",
            "top_level.date.required",
            "/date",
        ),
    ]

    result = autofill.build_proposals(tmp_path, findings, SCHEMA)
    entries = result["manifests"][0]["findings"]

    assert len(entries) == len(findings)
    assert [entry["finding"] for entry in entries] == findings
    assert sum(entry["status"] == "PROPOSED" for entry in entries) == 4
    assert sum(entry["status"] == "BLOCKED" for entry in entries) == 1

    for entry, original in zip(entries, findings):
        assert entry["finding"] == original
        if entry["status"] == "PROPOSED":
            assert entry["source"] is not None
            assert entry["proposed_value"] is not None
        else:
            assert entry["reason"]


def test_index_is_not_used_as_documentation(tmp_path):
    make_root(
        tmp_path,
        "work_item_id: AID-TEST\n"
        "title: Test\n",
        {"INDEX.md": "# Index\n"},
    )

    result = autofill.build_proposals(
        tmp_path,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "top_level.documentation.required",
                "/documentation",
            ),
        ],
        SCHEMA,
    )

    entry = result["manifests"][0]["findings"][0]
    assert entry["status"] == "BLOCKED"
    assert "INDEX.md is an index" in entry["reason"]


def test_write_flag_is_rejected():
    original_argv = sys.argv[:]
    try:
        sys.argv = [
            str(SCRIPT),
            "--root", ".",
            "--findings", "findings.json",
            "--schema", "schema.yaml",
            "--write",
        ]
        with pytest.raises(SystemExit) as exc:
            autofill.parse_args()
        assert exc.value.code == 2
    finally:
        sys.argv = original_argv


def test_merged_implementation_status_is_mapped_only_for_exact_pointer(
    tmp_path,
):
    # Exact authorized case: implementation.status == MERGED.
    positive_root = tmp_path / "positive"
    make_root(
        positive_root,
        "work_item_id: AID-TEST-MERGED\n"
        "title: Test\n"
        "implementation:\n"
        "  status: MERGED\n",
    )

    positive = autofill.build_proposals(
        positive_root,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "implementation.status.enum",
                "/implementation/status",
                category="enum",
                message="status is outside schema enum",
            ),
        ],
        SCHEMA,
    )

    entry = positive["manifests"][0]["findings"][0]
    assert entry["status"] == "PROPOSED"
    assert entry["proposed_value"] == "IMPLEMENTED"
    assert entry["operation"] == {
        "type": "set_nested_key",
        "path": ["implementation", "status"],
        "value": "IMPLEMENTED",
    }
    assert entry["source"] == {
        "type": "existing_manifest_value",
        "pointer": "/implementation/status",
        "value": "MERGED",
    }
    assert entry["reason"] == (
        "MERGED explicitly records that the implementation was merged. "
        "IMPLEMENTED is the corresponding value in the implementation.status schema enum."
    )

    # Same current value, but a different pointer: must not be mapped.
    wrong_pointer_root = tmp_path / "wrong-pointer"
    make_root(
        wrong_pointer_root,
        "work_item_id: AID-TEST-WRONG-POINTER\n"
        "title: Test\n"
        "implementation:\n"
        "  status: MERGED\n",
    )

    wrong_pointer = autofill.build_proposals(
        wrong_pointer_root,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "implementation.status.enum",
                "/implementation/other_status",
                category="enum",
                message="status is outside schema enum",
            ),
        ],
        SCHEMA,
    )

    entry = wrong_pointer["manifests"][0]["findings"][0]
    assert entry["status"] == "BLOCKED"
    assert entry["proposed_value"] is None

    # Exact pointer, but a different invalid value: must not be mapped.
    other_value_root = tmp_path / "other-value"
    make_root(
        other_value_root,
        "work_item_id: AID-TEST-OTHER-VALUE\n"
        "title: Test\n"
        "implementation:\n"
        "  status: DONE\n",
    )

    other_value = autofill.build_proposals(
        other_value_root,
        [
            finding(
                "14-ai-development/work-items/AID-TEST/manifest.yaml",
                "implementation.status.enum",
                "/implementation/status",
                category="enum",
                message="status is outside schema enum",
            ),
        ],
        SCHEMA,
    )

    entry = other_value["manifests"][0]["findings"][0]
    assert entry["status"] == "BLOCKED"
    assert entry["proposed_value"] is None
    assert "outside schema enum" in entry["reason"]
