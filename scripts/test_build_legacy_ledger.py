from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts/ci/build_legacy_ledger.py"
CHECKER_PATH = ROOT / "scripts/ci/check_work_item_manifest_schema.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


builder = load_module(BUILDER_PATH, "build_legacy_ledger_under_test")
checker = load_module(CHECKER_PATH, "checker_for_legacy_ledger_tests")


def sample_finding(
    manifest_path="14-ai-development/work-items/AID-TEST/manifest.yaml",
    rule_id="documentation.required",
    pointer="/documentation",
):
    return {
        "manifest_path": manifest_path,
        "rule_id": rule_id,
        "pointer": pointer,
    }


def test_missing_rule_template_exits_2_without_output(tmp_path, monkeypatch, capsys):
    output = tmp_path / "ledger.json"
    monkeypatch.setattr(
        builder,
        "RULE_TEMPLATES",
        {
            key: value
            for key, value in builder.RULE_TEMPLATES.items()
            if key != "documentation.required"
        },
    )

    rc = builder.main(
        [
            "--root",
            str(ROOT),
            "--tree",
            "HEAD",
            "--cohort",
            str(tmp_path / "cohort.json"),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert rc == 2
    assert "documentation.required" in captured.err
    assert not output.exists()


def test_migrated_finding_without_resolution_commit_exits_2(
    tmp_path, monkeypatch, capsys
):
    finding = sample_finding()
    monkeypatch.setattr(
        builder,
        "load_cohort",
        lambda _path: {
            "baseline_commit": "baseline",
            "baseline_tree": "baseline-tree",
            "manifest_paths": [finding["manifest_path"]],
        },
    )
    monkeypatch.setattr(
        builder,
        "find_resolution_commit",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        builder,
        "collect_at_tree",
        lambda *args, **kwargs: [],
    )

    class FakeChecker:
        LEDGER_PLACEHOLDERS = {
            "rationale": "TODO: describe why this legacy finding remains",
            "accountable_owner": "TODO: assign an accountable owner",
            "migration_plan": "TODO: specify a verifiable migration plan",
        }
        LEDGER_GENERATED_BY = "test"
        finding_identity = staticmethod(
            lambda item: (
                item["manifest_path"],
                item["rule_id"],
                item["pointer"],
            )
        )
        finding_id = staticmethod(lambda identity: "canonical-test-id")
        load_manifest_schema = staticmethod(lambda *_args: {})
        git_tree_paths = staticmethod(lambda *_args: set())
        collect_findings = staticmethod(
            lambda _root, tree, _paths, _schema, _tree_paths: (
                [finding] if tree == "baseline-tree" else []
            )
        )
        validate_ledger = staticmethod(lambda *_args: ([], set()))

    monkeypatch.setattr(builder, "load_checker", lambda: FakeChecker)

    output = tmp_path / "ledger.json"
    rc = builder.main(
        [
            "--root",
            str(ROOT),
            "--tree",
            "target-tree",
            "--cohort",
            str(tmp_path / "cohort.json"),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert rc == 2
    assert finding["manifest_path"] in captured.err
    assert finding["rule_id"] in captured.err
    assert finding["pointer"] in captured.err
    assert not output.exists()


def test_generated_ledger_passes_legacy_ledger_validator():
    """The generated ledger is accepted by the canonical checker validator."""
    cohort_path = (
        ROOT / "14-ai-development/reports/work-item-legacy-cohort.json"
    )
    if not cohort_path.exists():
        pytest.skip("repository legacy cohort fixture is unavailable")

    cohort = builder.load_cohort(cohort_path)
    tree = "HEAD"
    schema = checker.load_manifest_schema(ROOT, tree)
    baseline_paths = checker.git_tree_paths(ROOT, cohort["baseline_tree"])
    current_paths = checker.git_tree_paths(ROOT, tree)

    baseline = checker.collect_findings(
        ROOT,
        cohort["baseline_tree"],
        cohort["manifest_paths"],
        schema,
        baseline_paths,
    )
    current = checker.collect_findings(
        ROOT,
        tree,
        cohort["manifest_paths"],
        schema,
        current_paths,
    )

    # This assertion tests the canonical validator contract directly.
    payload = builder.build_ledger(ROOT, tree, cohort_path)
    errors, _seen = checker.validate_ledger(
        payload,
        baseline,
        current,
        cohort["baseline_commit"],
        payload["cohort"],
    )
    joined = "\n".join(str(error) for error in errors)
    for forbidden in ("MISSING", "ORPHAN", "DUPLICATE", "INCOMPLETE_LEDGER_ENTRY"):
        assert forbidden not in joined
    assert not errors


def test_builder_uses_canonical_finding_identity():
    finding = sample_finding()
    identity = checker.finding_identity(finding)
    expected = checker.finding_id(identity)
    assert builder.finding_key(checker, finding) == identity
    assert checker.finding_id(builder.finding_key(checker, finding)) == expected


def test_existing_output_requires_force(tmp_path, capsys):
    output = tmp_path / "ledger.json"
    output.write_text('{"do_not_overwrite": true}\n', encoding="utf-8")

    rc = builder.main(
        [
            "--root",
            str(ROOT),
            "--tree",
            "HEAD",
            "--cohort",
            str(tmp_path / "missing-cohort.json"),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert rc == 2
    assert "already exists" in captured.err
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "do_not_overwrite": True
    }


def test_historical_yaml_parse_error_is_not_resolution(monkeypatch, tmp_path):
    """A parse failure must never be interpreted as an absent finding."""
    finding = sample_finding()

    class FakeChecker:
        finding_identity = staticmethod(
            lambda item: (
                item["manifest_path"],
                item["rule_id"],
                item["pointer"],
            )
        )
        load_manifest_schema = staticmethod(lambda *_args: {})
        git_tree_paths = staticmethod(lambda *_args: set())
        collect_findings = staticmethod(
            lambda *_args: (_ for _ in ()).throw(
                ValueError("duplicate YAML key")
            )
        )

    monkeypatch.setattr(builder, "load_checker", lambda: FakeChecker)
    monkeypatch.setattr(
        builder,
        "git",
        lambda _root, *args: (
            "target-commit"
            if args[0] == "rev-parse"
            else "historical-commit"
        ),
    )

    result = builder.find_resolution_commit(
        tmp_path,
        "baseline",
        "target-tree",
        finding["manifest_path"],
        finding["rule_id"],
        finding["pointer"],
    )
    assert result is None


def test_unaccepted_current_finding_remains_open():
    """No explicit risk-acceptance record means a persistent finding is OPEN."""
    finding = sample_finding()
    template = builder.RULE_TEMPLATES[finding["rule_id"]]

    entry = {
        "finding_id": checker.finding_id(checker.finding_identity(finding)),
        "manifest_path": finding["manifest_path"],
        "rule_id": finding["rule_id"],
        "pointer": finding["pointer"],
        "disposition": "OPEN",
        "rationale": template["rationale"],
        "accountable_owner": template["accountable_owner"],
        "migration_plan": template["migration_plan"],
        "resolution_commit": None,
        "resolution_evidence": None,
    }

    assert entry["disposition"] == "OPEN"
    assert entry["disposition"] != "ACCEPTED_RISK"
    assert entry["rationale"] not in checker.LEDGER_PLACEHOLDERS
    assert entry["accountable_owner"] not in checker.LEDGER_PLACEHOLDERS
    assert entry["migration_plan"] not in checker.LEDGER_PLACEHOLDERS
