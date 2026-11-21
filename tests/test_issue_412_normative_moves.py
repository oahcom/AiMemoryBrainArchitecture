"""Regression tests for Issue #412 normative-root departure handling.

These tests use real temporary Git histories so a rename has an extant
destination while a deletion does not. No filesystem-only imitation of a move.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_bilingual_docs.py"
SPEC = importlib.util.spec_from_file_location("check_bilingual_docs_issue_412", SCRIPT)
GATE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(GATE)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=repo, text=True, stderr=subprocess.STDOUT
    ).strip()


def commit_tree(repo: Path, files: dict[str, str], message: str) -> str:
    for name, value in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "tests@example.invalid")
    git(repo, "config", "user.name", "Issue 412 tests")
    baseline = {
        "00-governance/policy.md": "normative policy body\n",
        "docs/en/00-governance/policy.md": "English mirror body\n",
        "docs/zh-CN/00-governance/policy.md": "Chinese mirror body\n",
    }
    base = commit_tree(repo, baseline, "base")
    monkeypatch.setattr(GATE, "ROOT", repo)
    monkeypatch.setenv("BASE_SHA", base)
    return repo, base


def changed_and_statuses(repo: Path, base: str):
    raw = git(repo, "diff", "--name-status", "--no-renames", f"{base}...HEAD")
    statuses = {}
    for line in raw.splitlines():
        status, path = line.split("\t", 1)
        statuses[path] = status
    return set(statuses), statuses


def evaluate_root_departures(repo: Path, base: str) -> list[str]:
    os.environ["HEAD_SHA"] = git(repo, "rev-parse", "HEAD")
    return GATE.check_normative_root_departures(exception=False)


def test_p2_normative_triple_move_within_same_root_is_allowed(history):
    repo, base = history
    git(repo, "mv", "00-governance/policy.md", "00-governance/renamed-policy.md")
    git(repo, "mv", "docs/en/00-governance/policy.md", "docs/en/00-governance/renamed-policy.md")
    git(repo, "mv", "docs/zh-CN/00-governance/policy.md", "docs/zh-CN/00-governance/renamed-policy.md")
    git(repo, "commit", "-m", "move triple within docs")
    assert evaluate_root_departures(repo, base) == []


def test_p3_mirror_only_pair_move_out_to_archive_is_allowed(history):
    repo, base = history
    # Remove the root source from this fixture: this is a mirror-only pair.
    (repo / "00-governance/policy.md").unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "fixture becomes mirror-only")
    base = git(repo, "rev-parse", "HEAD")
    os.environ["BASE_SHA"] = base
    old_en = "docs/en/00-governance/policy.md"
    old_zh = "docs/zh-CN/00-governance/policy.md"
    new_en = "docs/en/governance/archive/policy.md"
    new_zh = "docs/zh-CN/governance/archive/policy.md"
    git(repo, "mv", old_en, new_en)
    git(repo, "mv", old_zh, new_zh)
    git(repo, "commit", "-m", "move mirror-only pair to archive")
    changed, statuses = changed_and_statuses(repo, base)
    assert evaluate_root_departures(repo, base) == []
    assert GATE.check_counterpart_requirement(old_en, [old_zh], changed, statuses, False) == []


def test_p5_mirror_only_pair_deleted_together_is_allowed(history):
    repo, base = history
    (repo / "00-governance/policy.md").unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "fixture becomes mirror-only")
    base = git(repo, "rev-parse", "HEAD")
    os.environ["BASE_SHA"] = base
    (repo / "docs/en/00-governance/policy.md").unlink()
    (repo / "docs/zh-CN/00-governance/policy.md").unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "delete mirror-only pair")
    changed, statuses = changed_and_statuses(repo, base)
    assert evaluate_root_departures(repo, base) == []
    assert GATE.check_counterpart_requirement(
        "docs/en/00-governance/policy.md",
        ["docs/zh-CN/00-governance/policy.md"],
        changed, statuses, False,
    ) == []


def test_d7_normative_triple_move_outside_covered_roots_is_rejected(history):
    repo, base = history
    git(repo, "mv", "00-governance/policy.md", "docs/governance/archive/policy.md")
    git(repo, "mv", "docs/en/00-governance/policy.md", "docs/en/governance/archive/policy.md")
    git(repo, "mv", "docs/zh-CN/00-governance/policy.md", "docs/zh-CN/governance/archive/policy.md")
    git(repo, "commit", "-m", "move triple outside normative roots")
    errors = evaluate_root_departures(repo, base)
    assert any("moved outside NORMATIVE_ROOTS" in error for error in errors)


def test_d8_normative_triple_deletion_is_rejected(history):
    repo, base = history
    for path in (
        "00-governance/policy.md",
        "docs/en/00-governance/policy.md",
        "docs/zh-CN/00-governance/policy.md",
    ):
        (repo / path).unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "delete normative triple")
    errors = evaluate_root_departures(repo, base)
    assert any("by deletion" in error for error in errors)


def test_d9_normative_triple_move_to_another_normative_root_is_allowed(history):
    repo, base = history
    git(repo, "mv", "00-governance/policy.md", "13-engineering-decisions/policy.md")
    git(repo, "mv", "docs/en/00-governance/policy.md", "docs/en/13-engineering-decisions/policy.md")
    git(repo, "mv", "docs/zh-CN/00-governance/policy.md", "docs/zh-CN/13-engineering-decisions/policy.md")
    git(repo, "commit", "-m", "move triple across normative roots")
    assert evaluate_root_departures(repo, base) == []
