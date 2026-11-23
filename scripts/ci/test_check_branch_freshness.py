#!/usr/bin/env python3
"""Self-check for scripts/ci/check_branch_freshness.py (#719).

Builds real repositories. A mock of the commit graph would prove the mock, and
the whole point of this gate is that the graph is the only thing that knows the
branch is stale.

    python3 scripts/ci/test_check_branch_freshness.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "check_branch_freshness.py"
REPO = HERE.parents[1]
# Real paths in this tree. `crates/*/src` and `docs/en` are the guarded classes
# #719 names; a non-existent fixture path would test the string prefix and
# nothing else.
CODE_FILE = "crates/memory-compiler/src/admission.rs"
NEW_CODE_FILE = "crates/memory-compiler/src/branch_freshness_probe.rs"
DOC_FILE = "docs/en/00-governance/architecture-invariants.md"
PLAIN_FILE = "ARCHITECTURE_ROADMAP.md"

RESULTS: list[tuple[str, bool, str]] = []


def git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    )
    return out.stdout.strip()


def make_repo(tmp: Path) -> Path:
    """A copy of this repository, re-initialised as its own git history.

    The gate imports NORMATIVE_ROOTS from check_bilingual_docs.py, which is
    fail-closed at import time against files on disk. A hand-built fixture
    therefore cannot exercise the gate at all: it exits 2 before main() runs.
    Copying the real tree is both simpler and more honest -- the gate is tested
    against the layout it will actually see.
    """
    repo = tmp / "repo"
    shutil.copytree(
        REPO,
        repo,
        ignore=shutil.ignore_patterns(".git", "target", "__pycache__"),
        symlinks=True,
    )
    git(repo, "init", "-q", ".")
    git(repo, "config", "user.email", "self-check@example.invalid")
    git(repo, "config", "user.name", "self-check")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base")
    return repo


def run_gate(repo: Path, base: str, head: str) -> tuple[int, str]:
    env = dict(os.environ, BASE_SHA=base, HEAD_SHA=head)
    out = subprocess.run(
        [sys.executable, str(repo / "scripts" / "ci" / GATE.name)],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
    )
    return out.returncode, out.stdout + out.stderr


def case(name: str, expect_code: int, expect_in: str, base: str, head: str, repo: Path) -> None:
    code, text = run_gate(repo, base, head)
    ok = code == expect_code and expect_in in text
    RESULTS.append((name, ok, f"exit={code} want={expect_code} looking for {expect_in!r}\n{text}"))


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="freshness-"))
    try:
        repo = make_repo(tmp)
        base = git(repo, "rev-parse", "HEAD")

        # main advances on three paths, one per shape the gate must tell apart:
        #   CODE_FILE     changed here and on the branch   -> ambiguous (code)
        #   NEW_CODE_FILE added here, absent on the branch -> hidden
        #   DOC_FILE      changed here and on the branch   -> ambiguous (governed)
        (repo / CODE_FILE).write_text("v2\n", encoding="utf-8")
        (repo / NEW_CODE_FILE).write_text("new\n", encoding="utf-8")
        (repo / DOC_FILE).write_text("doc2\n", encoding="utf-8")
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "main advances")
        advanced = git(repo, "rev-parse", "HEAD")

        # Case 1: branch at base, touches a governed doc only.
        git(repo, "checkout", "-q", "-b", "doc-only", base)
        (repo / DOC_FILE).write_text("doc3\n", encoding="utf-8")
        git(repo, "commit", "-qam", "doc only")
        doc_head = git(repo, "rev-parse", "HEAD")
        case(
            "stale on a governed path fails",
            1,
            "guarded: " + DOC_FILE,
            advanced,
            doc_head,
            repo,
        )
        case(
            "the path whose diff lies is named, not just counted",
            1,
            "both-sides: " + DOC_FILE,
            advanced,
            doc_head,
            repo,
        )

        # Case 2: same base, touches a non-governed path only.
        git(repo, "checkout", "-q", "-b", "unguarded", base)
        (repo / PLAIN_FILE).write_text("x\n", encoding="utf-8")
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "readme")
        readme_head = git(repo, "rev-parse", "HEAD")
        case(
            "stale but tolerable warns and passes",
            0,
            "no guarded path is touched",
            advanced,
            readme_head,
            repo,
        )

        # Case 2b: main ADDED a file the branch does not have. #719 Case A: it is
        # absent from the diff entirely, so a PR re-implementing it looks like a
        # first addition. Reported even though it cannot be "guarded" -- an
        # absent path is not a changed path.
        case(
            "a file added on base is reported as hidden",
            0,
            "hidden: " + NEW_CODE_FILE,
            advanced,
            readme_head,
            repo,
        )
        case(
            "the hidden path is reported on a governed-only branch too",
            1,
            "hidden: " + NEW_CODE_FILE,
            advanced,
            doc_head,
            repo,
        )

        # Case 3: rebased onto main -- the state the gate asks for.
        git(repo, "checkout", "-q", "-b", "rebased", advanced)
        (repo / DOC_FILE).write_text("doc3\n", encoding="utf-8")
        git(repo, "commit", "-qam", "doc only, rebased")
        rebased_head = git(repo, "rev-parse", "HEAD")
        case("fresh passes", 0, "fresh:", advanced, rebased_head, repo)

        # Case 4: `crates/*/src` is guarded even though it is not a normative
        # root -- #719 names it, and it is where the issuer allowlist lives.
        git(repo, "checkout", "-q", "-b", "code", base)
        (repo / CODE_FILE).write_text("v3\n", encoding="utf-8")
        git(repo, "commit", "-qam", "code")
        code_head = git(repo, "rev-parse", "HEAD")
        case(
            "stale on crates/*/src fails",
            1,
            "guarded: " + CODE_FILE,
            advanced,
            code_head,
            repo,
        )

        # Case 5: cannot decide. An unknown sha must not read as "fresh".
        case("unknown base is undecidable, not fresh", 2, "cannot be determined", "0" * 40, code_head, repo)
        case("missing shas are undecidable", 2, "both required", "", "", repo)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print("  " + detail.replace("\n", "\n  "))
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
