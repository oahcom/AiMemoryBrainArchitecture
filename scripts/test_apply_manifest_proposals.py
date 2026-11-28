from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

import pytest
import yaml


SCRIPT = (
    Path(__file__).resolve().parent
    / "ci"
    / "apply_manifest_proposals.py"
)
SPEC = importlib.util.spec_from_file_location("apply_manifest_proposals", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
app = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(app)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def schema() -> dict:
    return {
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
        }
    }


def make_manifest(root: Path, name: str, objective: str = "Implement the feature") -> tuple[Path, bytes]:
    directory = root / "14-ai-development" / "work-items" / name
    directory.mkdir(parents=True)
    path = directory / "manifest.yaml"
    original = (
        f'work_item_id: {name}\n'
        f'title: "A quoted title"\n'
        f'scope:\n'
        f'  objective: "{objective}"\n'
        f'implementation: {{}}\n'
        f'custom_metadata:\n'
        f'  preserve: "quoted value"\n'
    ).encode("utf-8")
    path.write_bytes(original)
    return path, original


def summary_entry(relative: str, objective: str) -> dict:
    value = objective
    return {
        "finding": {
            "manifest": relative,
            "rule": "implementation.required_key",
            "pointer": "/implementation/summary",
            "category": "OTHER_SCHEMA",
            "message": "implementation.summary is required",
        },
        "status": "PROPOSED",
        "proposed_value": value,
        "operation": {
            "type": "set_nested_key",
            "path": ["implementation", "summary"],
            "value": value,
        },
        "source": {
            "type": "existing_manifest_field",
            "path": "scope.objective",
        },
        "reason": "Copied from scope.objective",
    }


def make_proposal(path: Path, root: Path, entries: list[dict]) -> dict:
    original_bytes = path.read_bytes()
    original = yaml.safe_load(original_bytes)
    proposed = copy.deepcopy(original)

    authorized = {}
    for entry in entries:
        if entry["status"] != "PROPOSED":
            continue
        pointer, value = app.validate_operation(
            entry, original, root, schema()
        )
        authorized[pointer] = value

    for pointer, value in authorized.items():
        app.apply_value(proposed, pointer, value)

    after = app.render_yaml(proposed)
    relative = path.relative_to(root).as_posix()

    return {
        "manifest": relative,
        "before_sha256": digest(original_bytes),
        "proposed_sha256": digest(after),
        "findings": entries,
        # Stage-2 does not use these display-only fields.
        "diff": "",
        "reverse_diff": "",
    }


def make_proposals(root: Path, manifest_entries: list[tuple[Path, list[dict]]]) -> dict:
    return {
        "mode": "stage-1-read-only",
        "files_written": 0,
        "manifests": [
            make_proposal(path, root, entries)
            for path, entries in manifest_entries
        ],
    }


def test_hash_mismatch_fails_entire_batch_before_any_write(tmp_path: Path) -> None:
    root = tmp_path
    first, first_before = make_manifest(root, "AID-TEST-001")
    second, second_before = make_manifest(root, "AID-TEST-002")

    proposals = make_proposals(
        root,
        [
            (first, [summary_entry(first.relative_to(root).as_posix(), "Implement the feature")]),
            (second, [summary_entry(second.relative_to(root).as_posix(), "Implement the feature")]),
        ],
    )

    # Change the second manifest after Stage-1 generated its proposal.
    second.write_bytes(second_before + b"\n# changed after proposal\n")

    with pytest.raises(app.ProposalError, match="before_sha256 mismatch"):
        app.prepare_batch(root, proposals, schema())

    assert first.read_bytes() == first_before
    assert second.read_bytes() != second_before


def test_blocked_findings_are_skipped(tmp_path: Path) -> None:
    root = tmp_path
    path, before = make_manifest(root, "AID-TEST-003")
    relative = path.relative_to(root).as_posix()

    blocked = {
        "finding": {
            "manifest": relative,
            "rule": "top_level.date.required",
            "pointer": "/date",
            "category": "OTHER_SCHEMA",
            "message": "date is required",
        },
        "status": "BLOCKED",
        "proposed_value": None,
        "operation": None,
        "source": None,
        "reason": "No authoritative date source",
    }
    proposals = make_proposals(root, [(path, [blocked])])
    prepared = app.prepare_batch(root, proposals, schema())

    assert prepared[0]["blocked_findings"] == 1
    assert prepared[0]["proposed_findings"] == 0
    assert prepared[0]["changed"] is False

    # A dry-run must not write anything.
    assert path.read_bytes() == before


def test_dry_run_prepares_without_writing(tmp_path: Path) -> None:
    root = tmp_path
    path, before = make_manifest(root, "AID-TEST-004")
    relative = path.relative_to(root).as_posix()

    proposals = make_proposals(
        root,
        [(path, [summary_entry(relative, "Implement the feature")])],
    )
    prepared = app.prepare_batch(root, proposals, schema())

    assert prepared[0]["changed"] is True
    assert path.read_bytes() == before


def test_batch_failure_rolls_back_previously_written_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path
    first, first_before = make_manifest(root, "AID-TEST-005")
    second, second_before = make_manifest(root, "AID-TEST-006")

    proposals = make_proposals(
        root,
        [
            (first, [summary_entry(first.relative_to(root).as_posix(), "Implement the feature")]),
            (second, [summary_entry(second.relative_to(root).as_posix(), "Implement the feature")]),
        ],
    )
    prepared = app.prepare_batch(root, proposals, schema())

    real_write = app.write_file
    calls = 0

    def fail_on_second_write(path: Path, content: bytes) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated second-file write failure")
        real_write(path, content)

    monkeypatch.setattr(app, "write_file", fail_on_second_write)

    with pytest.raises(app.ProposalError, match="all written files restored"):
        app.commit_batch(prepared)

    assert first.read_bytes() == first_before
    assert second.read_bytes() == second_before


def test_rollback_failure_reports_the_unrestored_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path
    first, _ = make_manifest(root, "AID-TEST-007")
    second, _ = make_manifest(root, "AID-TEST-008")

    proposals = make_proposals(
        root,
        [
            (first, [summary_entry(first.relative_to(root).as_posix(), "Implement the feature")]),
            (second, [summary_entry(second.relative_to(root).as_posix(), "Implement the feature")]),
        ],
    )
    prepared = app.prepare_batch(root, proposals, schema())

    real_write = app.write_file
    calls = 0

    def fail_on_second_write(path: Path, content: bytes) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated write failure")
        real_write(path, content)

    def fail_restore(path: Path, content: bytes) -> None:
        raise OSError("simulated rollback failure")

    monkeypatch.setattr(app, "write_file", fail_on_second_write)
    monkeypatch.setattr(app, "restore_file", fail_restore)

    with pytest.raises(app.RollbackError) as captured:
        app.commit_batch(prepared)

    assert first.relative_to(root).as_posix() in str(captured.value)


def test_post_write_pointer_values_are_verified(tmp_path: Path) -> None:
    root = tmp_path
    path, before = make_manifest(root, "AID-TEST-009")
    relative = path.relative_to(root).as_posix()

    proposals = make_proposals(
        root,
        [(path, [summary_entry(relative, "Implement the feature")])],
    )
    prepared = app.prepare_batch(root, proposals, schema())

    app.commit_batch(prepared)

    committed = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert committed["implementation"]["summary"] == "Implement the feature"
    assert path.read_bytes() != before
    assert digest(path.read_bytes()) == prepared[0]["after_sha256"]


def test_yaml_format_drift_is_allowed_but_other_semantics_are_unchanged(
    tmp_path: Path,
) -> None:
    root = tmp_path
    path, before = make_manifest(root, "AID-TEST-010")
    relative = path.relative_to(root).as_posix()

    proposals = make_proposals(
        root,
        [(path, [summary_entry(relative, "Implement the feature")])],
    )
    prepared = app.prepare_batch(root, proposals, schema())
    candidate = prepared[0]["after_bytes"]

    before_document = yaml.safe_load(before)
    after_document = yaml.safe_load(candidate)

    assert before != candidate  # PyYAML may normalize quoting/formatting.
    assert app.semantic_projection(
        before_document, {"/implementation/summary"}
    ) == app.semantic_projection(
        after_document, {"/implementation/summary"}
    )
    assert app.get_pointer(
        after_document, "/implementation/summary"
    ) == "Implement the feature"

    # Preparing a proposal never changes the source file.
    assert path.read_bytes() == before


def test_conflicting_duplicate_pointer_fails_closed(tmp_path: Path) -> None:
    root = tmp_path
    path, _ = make_manifest(root, "AID-TEST-011")
    relative = path.relative_to(root).as_posix()

    original_bytes = path.read_bytes()
    before_sha256 = digest(original_bytes)

    first = summary_entry(relative, "First proposed summary")
    second = summary_entry(relative, "Conflicting proposed summary")

    # Deliberately bypass make_proposal(): its source validation correctly
    # rejects values that do not equal the current scope.objective.
    # This test targets batch-level conflict detection, which must run
    # before source-specific validation.
    proposals = {
        "mode": "stage-1-read-only",
        "files_written": 0,
        "manifests": [
            {
                "manifest": relative,
                "before_sha256": before_sha256,
                "proposed_sha256": "",
                "findings": [first, second],
                "diff": "",
                "reverse_diff": "",
            }
        ],
    }

    with pytest.raises(
        app.ProposalError,
        match="conflicting PROPOSED values",
    ):
        app.prepare_batch(root, proposals, schema())

    assert path.read_bytes() == original_bytes


def test_merged_status_mapping_is_narrowly_authorized(tmp_path: Path) -> None:
    root = tmp_path
    path, original_bytes = make_manifest(root, "AID-TEST-012")

    original = yaml.safe_load(original_bytes)
    original["implementation"]["status"] = "MERGED"
    original_bytes = app.render_yaml(original)
    path.write_bytes(original_bytes)

    relative = path.relative_to(root).as_posix()

    valid_entry = {
        "finding": {
            "manifest": relative,
            "rule": "implementation.status.enum",
            "pointer": "/implementation/status",
            "category": "OTHER_SCHEMA",
            "message": "implementation.status is outside schema enum",
        },
        "status": "PROPOSED",
        "proposed_value": "IMPLEMENTED",
        "operation": {
            "type": "set_nested_key",
            "path": ["implementation", "status"],
            "value": "IMPLEMENTED",
        },
        "source": {
            "type": "existing_manifest_value",
            "pointer": "/implementation/status",
            "value": "MERGED",
        },
        "reason": (
            "MERGED explicitly records that the implementation was merged. "
            "IMPLEMENTED is the corresponding value in the implementation.status schema enum."
        ),
    }

    # 1. Exact MERGED -> IMPLEMENTED mapping is accepted by the full
    # prepare_batch validation path.
    proposed_document = copy.deepcopy(original)
    app.apply_value(
        proposed_document,
        "/implementation/status",
        "IMPLEMENTED",
    )
    after_bytes = app.render_yaml(proposed_document)

    proposals = {
        "mode": "stage-1-read-only",
        "files_written": 0,
        "manifests": [
            {
                "manifest": relative,
                "before_sha256": digest(original_bytes),
                "proposed_sha256": digest(after_bytes),
                "findings": [valid_entry],
                "diff": "",
                "reverse_diff": "",
            }
        ],
    }

    prepared = app.prepare_batch(root, proposals, schema())

    assert prepared[0]["authorized_pointers"] == [
        "/implementation/status"
    ]
    assert prepared[0]["changed"] is True
    assert path.read_bytes() == original_bytes

    # 2. Same pointer, but a different proposed value, is rejected.
    wrong_value = copy.deepcopy(valid_entry)
    wrong_value["proposed_value"] = "BLOCKED"
    wrong_value["operation"]["value"] = "BLOCKED"

    with pytest.raises(
        app.ProposalError,
        match="unauthorized set_nested_key operation",
    ):
        app.validate_operation(
            wrong_value,
            original,
            root,
            schema(),
        )

    # 3. Same proposed value, but a different pointer and operation path,
    # is rejected.
    wrong_pointer = copy.deepcopy(valid_entry)
    wrong_pointer["finding"]["pointer"] = "/implementation/summary"
    wrong_pointer["operation"]["path"] = [
        "implementation",
        "summary",
    ]

    with pytest.raises(
        app.ProposalError,
        match="unauthorized set_nested_key operation",
    ):
        app.validate_operation(
            wrong_pointer,
            original,
            root,
            schema(),
        )

    # Validation must not modify the original manifest.
    assert path.read_bytes() == original_bytes
