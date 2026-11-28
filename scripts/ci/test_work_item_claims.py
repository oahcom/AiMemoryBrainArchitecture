#!/usr/bin/env python3
"""Tests for the authoritative claim ledger, its writer, and the gate wiring.

Run: python scripts/ci/test_work_item_claims.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

CI = Path(__file__).resolve().parent
CHECKER = CI / "check_work_item_uniqueness.py"
CLAIM = CI / "claim_work_item.py"
REGISTRY = "14-ai-development/work-items/registry/work-item-claims.yaml"
ROOT = "14-ai-development/work-items"
REPOSITORY = "oahcom/AiMemoryBrainArchitecture"
REF = "work-item-claims"

MANIFEST = "work_item_id: {id}\ntitle: t\n"


def run(cwd, *args):
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def git(cwd, *args):
    result = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True
    )
    if result.returncode:
        raise AssertionError(f"git {' '.join(args)}: {result.stderr}")
    return result.stdout.strip()


def init_repo(root: Path):
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "seed")
    return repo


def commit_file(repo: Path, path: str, text: str, message: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)
    return git(repo, "rev-parse", "HEAD")


def ledger(claims: list[dict], schema_version: int = 2) -> str:
    return yaml.safe_dump(
        {"schema_version": schema_version, "claims": claims},
        sort_keys=False,
        allow_unicode=True,
    )


def claim(work_item_id: str, status: str, pull_request=None, **extra) -> dict:
    record = {
        "work_item_id": work_item_id,
        "status": status,
        "repository": REPOSITORY,
        "pull_request": pull_request,
        "owner_work_item": work_item_id,
        "claimed_at": "2026-11-28T00:00:00Z",
        "updated_at": "2026-11-28T00:00:00Z",
    }
    record.update(extra)
    return record


def publish_ledger(repo: Path, text: str) -> str:
    """Put the ledger on its own ref, the way the writer does."""
    blob = subprocess.run(
        ["git", "hash-object", "-w", "--stdin"],
        cwd=str(repo),
        input=text,
        capture_output=True,
        text=True,
    ).stdout.strip()
    index = os.path.join(str(repo), ".git", "ledger-index")
    env = dict(os.environ, GIT_INDEX_FILE=index)
    subprocess.run(["git", "read-tree", "HEAD"], cwd=str(repo), env=env, check=True)
    subprocess.run(
        ["git", "update-index", "--add", "--cacheinfo", f"100644,{blob},{REGISTRY}"],
        cwd=str(repo),
        env=env,
        check=True,
    )
    tree = subprocess.run(
        ["git", "write-tree"], cwd=str(repo), env=env, capture_output=True, text=True
    ).stdout.strip()
    os.remove(index)
    commit = subprocess.run(
        ["git", "commit-tree", tree, "-p", git(repo, "rev-parse", "HEAD"), "-m", "ledger"],
        cwd=str(repo),
        capture_output=True,
        text=True,
    ).stdout.strip()
    git(repo, "update-ref", f"refs/heads/{REF}", commit)
    return commit


def invoke(repo: Path, base: str, head: str, *extra):
    return run(repo, CHECKER, "--base", base, "--head", head, *extra)


class AuthoritativeLedgerTests(unittest.TestCase):
    def build(self, claims, *, schema_version=2):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = init_repo(Path(self.temp.name))
        self.base = git(self.repo, "rev-parse", "HEAD")
        publish_ledger(self.repo, ledger(claims, schema_version))
        self.head = commit_file(
            self.repo, f"{ROOT}/AID-2026-500/manifest.yaml", MANIFEST.format(id="AID-2026-500"), "item"
        )
        return self.repo

    def test_unregistered_id_is_a_violation(self):
        repo = self.build([])
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("WORK_ITEM_ID_UNREGISTERED AID-2026-500", result.stdout)

    def test_released_id_is_reported_separately(self):
        repo = self.build([claim("AID-2026-500", "EXPIRED", 41)])
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("WORK_ITEM_ID_RELEASED AID-2026-500", result.stdout)

    def test_own_claimed_id_passes(self):
        repo = self.build([claim("AID-2026-500", "CLAIMED", 42)])
        result = invoke(
            repo,
            self.base,
            self.head,
            "--registry-ref",
            REF,
            "--pull-request",
            "42",
            "--repository",
            REPOSITORY,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_other_pull_request_claim_blocks(self):
        repo = self.build([claim("AID-2026-500", "CLAIMED", 41)])
        result = invoke(
            repo,
            self.base,
            self.head,
            "--registry-ref",
            REF,
            "--pull-request",
            "42",
            "--repository",
            REPOSITORY,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("is already CLAIMED", result.stdout)

    def test_merged_is_never_exempted(self):
        repo = self.build([claim("AID-2026-500", "MERGED", 42)])
        result = invoke(
            repo,
            self.base,
            self.head,
            "--registry-ref",
            REF,
            "--pull-request",
            "42",
            "--repository",
            REPOSITORY,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_missing_authoritative_ref_is_incomplete(self):
        repo = self.build([claim("AID-2026-500", "CLAIMED", 42)])
        git(repo, "update-ref", "-d", f"refs/heads/{REF}")
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cannot be resolved", result.stdout)

    def test_missing_registry_file_is_incomplete(self):
        repo = self.build([])
        publish_ledger(repo, "schema_version: 2\n")
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("declares no claims list", result.stdout)

    def test_duplicate_current_claims_are_a_violation(self):
        repo = self.build(
            [
                claim("AID-2026-500", "CLAIMED", 41),
                claim("AID-2026-500", "CLAIMED", 42),
            ]
        )
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DUPLICATE_CURRENT_CLAIM", result.stdout)

    def test_unknown_schema_version_is_incomplete(self):
        repo = self.build([claim("AID-2026-500", "CLAIMED", 42)], schema_version=9)
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("unsupported", result.stdout)

    def test_claim_missing_required_field_is_incomplete(self):
        broken = claim("AID-2026-500", "CLAIMED", 42)
        broken.pop("owner_work_item")
        repo = self.build([broken])
        result = invoke(repo, self.base, self.head, "--registry-ref", REF)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("owner_work_item", result.stdout)

    def test_candidate_cannot_supply_the_ledger(self):
        repo = self.build([])
        head = commit_file(repo, REGISTRY, ledger([]), "candidate ledger")
        result = invoke(repo, self.base, head)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


class ClaimWriterTests(unittest.TestCase):
    def test_two_writers_race_for_one_id(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        remote = root / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)

        seed = init_repo(root)
        seed.rename(root / "seed")
        seed = root / "seed"
        git(seed, "remote", "add", "origin", str(remote))
        git(seed, "push", "-q", "origin", "main")
        publish_ledger(seed, ledger([]))
        git(seed, "push", "-q", "origin", f"refs/heads/{REF}")

        def clone(name):
            target = root / name
            subprocess.run(
                ["git", "clone", "-q", str(remote), str(target)], check=True
            )
            git(target, "config", "user.email", "t@example.com")
            git(target, "config", "user.name", "t")
            return target

        first = clone("A")
        second = clone("B")
        stale = git(second, "rev-parse", f"origin/{REF}")
        common = [
            "--id", "AID-2099-001",
            "--repository", REPOSITORY,
            "--ref", f"refs/heads/{REF}",
        ]
        a = run(first, CLAIM, *common, "--pull-request", "9001")
        # B built its claim from the ledger it read before A pushed: a stale
        # writer. Its push must be rejected as non-fast-forward.
        b = run(
            second, CLAIM, *common, "--pull-request", "9002",
            "--base-commit", stale,
        )

        self.assertEqual(a.returncode, 0, a.stdout + a.stderr)
        self.assertEqual(b.returncode, 3, b.stdout + b.stderr)
        self.assertIn("LOST_THE_RACE", b.stdout)

        shown = git(second, "show", f"origin/{REF}:{REGISTRY}")
        data = yaml.safe_load(shown)
        claims = [c for c in data["claims"] if c["work_item_id"] == "AID-2099-001"]
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0]["pull_request"], 9001)

        # A different id can still be claimed after re-reading the ref.
        git(second, "fetch", "-q", "origin", f"refs/heads/{REF}:refs/heads/{REF}")
        c = run(
            second,
            CLAIM,
            "--id", "AID-2099-002",
            "--repository", REPOSITORY,
            "--ref", f"refs/heads/{REF}",
            "--pull-request", "9002",
        )
        self.assertEqual(c.returncode, 0, c.stdout + c.stderr)
        data = yaml.safe_load(git(second, "show", f"origin/{REF}:{REGISTRY}"))
        self.assertEqual(len(data["claims"]), 2)

    def test_writer_refuses_an_id_held_by_another_pull_request(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        repo = init_repo(root)
        publish_ledger(repo, ledger([claim("AID-2099-003", "CLAIMED", 41)]))
        result = run(
            repo,
            CLAIM,
            "--id", "AID-2099-003",
            "--repository", REPOSITORY,
            "--ref", f"refs/heads/{REF}",
            "--pull-request", "42",
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("CLAIM REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
