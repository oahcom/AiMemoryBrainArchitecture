#!/usr/bin/env python3
"""Verify the three-job shape of `.github/workflows/session-evidence.yml`.

PR #1014 split that workflow into three jobs because a single-job workflow had
produced 18 consecutive failing runs: the `validate` verdict and the PR-head
self-test shared one checkout, so a broken head could suppress the verdict and
the base tree was never tested as itself. Nothing now prevents the workflow
from being collapsed back, and the collapse is silent -- the gate keeps
reporting PASS while it has stopped being independent.

The three properties, each a real failure mode:

  1. All three job ids exist: `self-test-trusted-base`, `self-test-pr-head`,
     `validate`. Merging them back is regression #1.
  2. No checkout step in `self-test-pr-head` carries `ref:`. A `ref:` there
     silently points the head job at the base tree -- the exact defect #1014
     fixed -- and the job still passes, over the wrong tree.
  3. `validate` has no `needs:`. A `needs:` there lets a PR suppress its own
     verdict by deleting a test, because a failed dependency skips the job and
     a skipped required context is not a failure.

Exit codes follow the repository vocabulary:
    0  PASS        the workflow has the three-job shape
    1  VIOLATION   a job is missing, or carries the key that re-creates a defect
    2  INCOMPLETE  the workflow file or its `jobs:` mapping cannot be read

The incomplete branch matters: a checker that treats "file not found" as "no
violations" is a false PASS, which is worse than having no checker.

Parsing is regex-over-raw-text, deliberately. The repository has no YAML
parser available (PyYAML and node `yaml` both fail to install in this tree), so
this follows scripts/check_declared_check_contexts.py rather than adding a
dependency. ponytail: indentation-based block scanning, not YAML semantics; a
`ref:` or `needs:` inside a `run:` block scalar whose text happens to sit at the
key's indent would read as a key. The verdict job's `run:` bodies are indented
ten spaces and a job-level key four, so this tree is safe; a future step that
shells out at four-space indent would need the scanner replaced by a real
parser. Upgrade path: swap the block scanner for a real parser if one ever
becomes installable.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

WORKFLOW_PATH = ".github/workflows/session-evidence.yml"

REQUIRED_JOB_IDS = ("self-test-trusted-base", "self-test-pr-head", "validate")
HEAD_JOB = "self-test-pr-head"
VERDICT_JOB = "validate"

# A job id is a top-level key under `jobs:` (2-space indent).
JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
# A step in a job's `steps:` list starts with "- " at some indent.
STEP_START_RE = re.compile(r"^(\s*)- \s*\S")
CHECKOUT_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*actions/checkout")
REF_KEY_RE = re.compile(r"^\s*(?:-\s*)?ref:\s*\S")
# A job-level key is at 4-space indent. `needs:` may put its value on the same
# line (flow form, `needs: [a, b]`) or on the following lines (block form,
# `needs:` alone) -- both are the dependency the guard forbids, so both match.
NEEDS_KEY_RE = re.compile(r"^    needs:(\s*\S|\s*$)")


class JobBlock(NamedTuple):
    """One job's raw lines, plus the 1-based file line its first line came from."""

    text: str
    first_line: int


class StepBlock(NamedTuple):
    """One step's raw lines, plus the 1-based file line its first line came from."""

    text: str
    first_line: int


def job_blocks(text: str) -> dict[str, JobBlock] | None:
    """Map job id -> that job's raw block. None if the `jobs:` map is absent."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.rstrip() == "jobs:"), None)
    if start is None:
        return None

    blocks: dict[str, JobBlock] = {}
    current: str | None = None
    body: list[str] = []
    body_start = 0

    for offset, line in enumerate(lines[start + 1:], start=start + 2):
        if line and not line[0].isspace() and not line.startswith("#"):
            break  # a column-0 key ends the jobs mapping

        match = JOB_ID_RE.match(line)
        if match:
            if current is not None:
                blocks[current] = JobBlock("\n".join(body), body_start)
            current = match.group(1)
            body = []
            body_start = offset + 1
            continue

        if current is not None:
            body.append(line)

    if current is not None:
        blocks[current] = JobBlock("\n".join(body), body_start)

    return blocks or None


def steps(block: JobBlock) -> list[StepBlock]:
    """Split one job block into step blocks, one per `- ` list entry."""
    found: list[StepBlock] = []
    indent: str | None = None
    body: list[str] = []
    body_start = 0

    for offset, line in enumerate(block.text.splitlines(), start=block.first_line):
        match = STEP_START_RE.match(line)
        if match and (indent is None or match.group(1) == indent):
            indent = match.group(1)
            if body:
                found.append(StepBlock("\n".join(body), body_start))
            body = [line]
            body_start = offset
            continue
        if body:
            body.append(line)

    if body:
        found.append(StepBlock("\n".join(body), body_start))
    return found


def _checkout_refs(block: JobBlock) -> list[str]:
    """`line N: ref: ...` for each checkout step in this job that declares `ref:`.

    The offender is the `ref:` line, not the step's `uses:` line: the action
    reference is the one line in such a step that is already correct, so naming
    it sends the reader to look for a `ref:` that is not there (#1045).
    """
    offenders = []
    for step in steps(block):
        step_lines = step.text.splitlines()
        if not any(CHECKOUT_RE.match(line) for line in step_lines):
            continue
        for offset, line in enumerate(step_lines, start=step.first_line):
            if REF_KEY_RE.match(line):
                offenders.append(f"line {offset}: {line.strip()}")
                break
    return offenders


def violations(blocks: dict[str, JobBlock]) -> list[str]:
    """Every violated property, named specifically. Empty means conformant."""
    found: list[str] = []

    for job_id in REQUIRED_JOB_IDS:
        if job_id not in blocks:
            found.append(
                f"job id {job_id!r} is missing from {WORKFLOW_PATH}; the workflow "
                "must keep the three jobs PR #1014 split it into (job: "
                f"{job_id})"
            )

    if HEAD_JOB in blocks:
        for offender in _checkout_refs(blocks[HEAD_JOB]):
            found.append(
                f"the {HEAD_JOB!r} job's checkout step declares a `ref:` key "
                f"({offender}); it must check out the PR head to test the PR's "
                f"own tree, and a `ref:` silently points it at the base tree "
                f"(job: {HEAD_JOB})"
            )

    if VERDICT_JOB in blocks:
        for offset, line in enumerate(
            blocks[VERDICT_JOB].text.splitlines(),
            start=blocks[VERDICT_JOB].first_line,
        ):
            if NEEDS_KEY_RE.match(line):
                found.append(
                    f"the {VERDICT_JOB!r} job declares `needs:` "
                    f"(line {offset}: {line.strip()}); the verdict must not "
                    "depend on another job, or a PR can suppress it by breaking "
                    f"that job (job: {VERDICT_JOB})"
                )

    return found


def main(root: Path | None = None) -> int:
    root = Path(root or ".").resolve()
    workflow = root / WORKFLOW_PATH

    if not workflow.is_file():
        print(
            f"::error::INCOMPLETE: workflow is absent: {WORKFLOW_PATH}",
            file=sys.stderr,
        )
        return 2

    blocks = job_blocks(workflow.read_text(encoding="utf-8"))
    if blocks is None:
        print(
            f"::error::INCOMPLETE: no `jobs:` mapping found in {WORKFLOW_PATH}; "
            "the shape cannot be read, so it cannot be verified",
            file=sys.stderr,
        )
        return 2

    found = violations(blocks)
    if found:
        for message in found:
            print(f"::error::{message}", file=sys.stderr)
        print(
            f"SESSION EVIDENCE WORKFLOW SHAPE: FAIL ({len(found)} violation(s))",
            file=sys.stderr,
        )
        return 1

    print(
        f"::notice::{WORKFLOW_PATH} has the three independent jobs "
        f"{', '.join(REQUIRED_JOB_IDS)}; the head job carries no `ref:`, "
        "the verdict job carries no `needs:`",
        file=sys.stderr,
    )
    print("SESSION EVIDENCE WORKFLOW SHAPE: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
