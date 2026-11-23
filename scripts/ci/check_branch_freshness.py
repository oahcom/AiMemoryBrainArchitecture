#!/usr/bin/env python3
"""Stale-branch gate (#719).

A pull request's diff is computed from `merge-base(base, head)` to `head`. When
the branch is old, that diff is wrong in both directions at once and it does not
say so: files `main` changed after the merge base appear as if the PR changed
them, and files `main` added after the merge base do not appear at all, so a PR
that re-implements one reads as "adds it for the first time".

The diff cannot report its own staleness. The commit graph can:

    git merge-base --is-ancestor BASE HEAD    -> 0 means head contains all of base

When that is false the branch is behind, and the increment it shows is not the
increment merging it would produce. This gate fails that case only for the path
classes #719 names -- governance documents, bilingual mirrors, `crates/*/src` --
because a stale typo fix is tolerable and a stale issuer allowlist is not.

    BASE_SHA=<sha> HEAD_SHA=<sha> python3 scripts/ci/check_branch_freshness.py

Exit: 0 fresh or stale-but-tolerable, 1 stale on a guarded path, 2 cannot decide.
2 is never 0: a gate that cannot read the graph must not certify the branch.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Normative roots come from the bilingual gate, so "governed" means one thing in
# this repository. A second hand-kept list is how 08-protocols stopped existing.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from check_bilingual_docs import NORMATIVE_ROOTS  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
# #719 names three classes. Only governance documents and bilingual mirrors are
# here as directories; code is matched by shape below, since `crates/*/src` is
# every crate and no fixed prefix.
GUARDED_ROOTS = tuple(sorted(NORMATIVE_ROOTS)) + ("docs/en", "docs/zh-CN")
GUARDED_CODE_ROOT = "crates/"
GUARDED_CODE_INFIX = "/src/"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, text=True, capture_output=True
    )


def names(raw: str) -> set[str]:
    """NUL-separated path list. Splitting on whitespace would let
    `00-governance/new policy.md` escape classification."""
    return {p for p in raw.split("\0") if p}


def is_guarded(path: str) -> bool:
    if any(path == root or path.startswith(root + "/") for root in GUARDED_ROOTS):
        return True
    return path.startswith(GUARDED_CODE_ROOT) and GUARDED_CODE_INFIX in path


def undecidable(reason: str) -> int:
    print(f"::error::branch freshness cannot be determined: {reason}")
    return 2


def main() -> int:
    base = os.environ.get("BASE_SHA", "").strip()
    head = os.environ.get("HEAD_SHA", "").strip()
    if not base or not head:
        return undecidable("BASE_SHA and HEAD_SHA are both required")

    ancestor = git("merge-base", "--is-ancestor", base, head)
    if ancestor.returncode == 0:
        print(f"fresh: {base[:9]} is an ancestor of {head[:9]}")
        return 0
    # 1 is the answer "not an ancestor". Anything else -- 128 for an unknown
    # object, 129 for bad usage, a missing git -- is not an answer, and must not
    # be read as one.
    if ancestor.returncode != 1:
        return undecidable(
            f"git merge-base --is-ancestor exited {ancestor.returncode}: "
            f"{ancestor.stderr.strip()[:200]} (shallow checkout? fetch-depth must be 0)"
        )

    merge_base = git("merge-base", base, head).stdout.strip()
    if not merge_base:
        return undecidable(f"no merge base for {base[:9]} and {head[:9]}")
    behind = int(git("rev-list", "--count", f"{head}..{base}").stdout.strip() or 0)

    increment = names(git("diff", "--name-only", "-z", f"{merge_base}...{head}").stdout)
    moved = names(
        git("diff", "--name-only", "-z", "--diff-filter=AMR", f"{merge_base}..{base}").stdout
    )
    # Two distinct lies, and #719 gives one PR per shape.
    #
    # False positive: a path the branch changed AND main changed after the merge
    # base. The displayed diff shows main's change as the PR's doing (#699).
    ambiguous = sorted(increment & moved)
    # False negative: a path main ADDED after the merge base. It is absent from
    # the branch and absent from the diff, so a PR that re-implements it reads
    # as adding it for the first time (#703's attestor.rs).
    added_on_base = names(
        git("diff", "--name-only", "-z", "--diff-filter=A", f"{merge_base}..{base}").stdout
    )
    hidden = sorted(added_on_base - increment)

    guarded = sorted(path for path in increment if is_guarded(path))

    # Printed before the verdict: both lies are reported whether or not the
    # branch is allowed to stay stale. A tolerable stale branch still has a
    # misleading diff, and the reviewer is the one who has to know that.
    print(f"stale: {behind} commit(s) behind {base[:9]}, merge_base {merge_base[:9]}")
    if ambiguous:
        print(f"diff shows base's changes as this PR's on {len(ambiguous)} path(s):")
        for path in ambiguous[:20]:
            print(f"  both-sides: {path}")
    if hidden:
        print(f"{len(hidden)} path(s) added on base are invisible in this diff:")
        for path in hidden[:20]:
            print(f"  hidden: {path}")

    if not guarded:
        print(
            f"::warning::{behind} commit(s) behind (merge_base {merge_base[:9]}) but no "
            "guarded path is touched; rebase when convenient"
        )
        return 0

    print(
        f"::error::branch is {behind} commit(s) behind {base[:9]} and touches "
        f"{len(guarded)} guarded path(s); rebase before review so the diff equals "
        f"the increment (merge_base {merge_base[:9]})"
    )
    for path in guarded[:20]:
        print(f"  guarded: {path}")
    if len(guarded) > 20:
        print(f"  ... and {len(guarded) - 20} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
