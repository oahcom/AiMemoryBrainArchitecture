#!/usr/bin/env python3
"""Verify the three-job shape and the `edited` trigger of the session-evidence workflow.

PR #1014 split that workflow into three jobs because a single-job workflow had
produced 18 consecutive failing runs: the `validate` verdict and the PR-head
self-test shared one checkout, so a broken head could suppress the verdict and
the base tree was never tested as itself. Nothing now prevents the workflow
from being collapsed back, and the collapse is silent -- the gate keeps
reporting PASS while it has stopped being independent.

The properties, each a real failure mode:

  1. All three job ids exist: `self-test-trusted-base`, `self-test-pr-head`,
     `validate`. Merging them back is regression #1.
  2. No checkout step in `self-test-pr-head` carries `ref:`. A `ref:` there
     silently points the head job at the base tree -- the exact defect #1014
     fixed -- and the job still passes, over the wrong tree.
  3. `validate` has no `needs:`. A `needs:` there lets a PR suppress its own
     verdict by deleting a test, because a failed dependency skips the job and
     a skipped required context is not a failure.
  4. The `pull_request:` trigger lists `edited` among its `types:`. The
     validator reads the PR body live, so without `edited` a body edit after a
     green run leaves a verdict describing text that no longer exists (#1074).
     GitHub's default set is `opened, synchronize, reopened`, which omits it.

Exit codes follow the repository vocabulary:
    0  PASS        the workflow has the three-job shape and the `edited` trigger
    1  VIOLATION   a job is missing, carries the key that re-creates a defect, or
                   the trigger does not declare `edited`
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

# The trigger block. `on:` sits at column 0, `pull_request:` under it at 2-space
# indent, and that trigger's `types:` at 4. `types:` takes two spellings and both
# must be read: flow form `types: [a, b]` and block form `types:` followed by
# `- item` lines. Accepting only one is #1045's bug class in a new place.
ON_KEY_RE = re.compile(r"^on:\s*$")
PULL_REQUEST_RE = re.compile(r"^  pull_request:\s*(.*)$")
TYPES_FLOW_RE = re.compile(r"^    types:\s*\[(.*?)\]")
TYPES_BLOCK_RE = re.compile(r"^    types:\s*$")
TYPES_ITEM_RE = re.compile(r"^      -\s*(\S.*?)\s*$")


class JobBlock(NamedTuple):
    """One job's raw lines, plus the 1-based file line its first line came from."""

    text: str
    first_line: int


class StepBlock(NamedTuple):
    """One step's raw lines, plus the 1-based file line its first line came from."""

    text: str
    first_line: int


class TriggerBlock(NamedTuple):
    """The `pull_request:` trigger's raw lines, plus the 1-based line of that key."""

    text: str
    first_line: int


class TypesDecl(NamedTuple):
    """The trigger's `types:` entries, plus the 1-based line of the `types:` key."""

    values: list[str]
    line: int


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


def trigger_block(text: str) -> TriggerBlock | None:
    """The `pull_request:` trigger's raw block. None if no `on:` block is readable."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if ON_KEY_RE.match(line)), None)
    if start is None:
        return None

    body: list[str] = []
    body_start = 0
    for offset, line in enumerate(lines[start + 1:], start=start + 2):
        if line and not line[0].isspace() and not line.startswith("#"):
            break  # a column-0 key ends the `on:` mapping
        if not body and not line.strip():
            continue
        match = PULL_REQUEST_RE.match(line)
        if match:
            body = [line]
            body_start = offset
            continue
        if body:
            body.append(line)

    if not body:
        return None
    return TriggerBlock("\n".join(body), body_start)


def types_decl(block: TriggerBlock) -> TypesDecl | None:
    """The trigger's `types:` entries in either spelling. None if the key is absent.

    Flow form (`types: [a, b]`) puts the values on the key's line; block form
    (`types:` then `- a` lines) puts them below it. Both are valid YAML and both
    are accepted -- rejecting a correct block form is #1045's bug class.
    """
    lines = block.text.splitlines()
    for index, line in enumerate(lines):
        offset = block.first_line + index
        flow = TYPES_FLOW_RE.match(line)
        if flow:
            values = [item.strip().strip("'\"") for item in flow.group(1).split(",")]
            return TypesDecl([value for value in values if value], offset)
        if TYPES_BLOCK_RE.match(line):
            values = []
            for follower in lines[index + 1:]:
                item = TYPES_ITEM_RE.match(follower)
                if not item:
                    break
                values.append(item.group(1).strip("'\""))
            return TypesDecl(values, offset)
    return None


def _trigger_violations(text: str) -> list[str]:
    """The `edited` trigger property, named specifically. Empty means conformant."""
    block = trigger_block(text)
    if block is None:
        return [
            f"no `pull_request:` trigger is readable under `on:` in {WORKFLOW_PATH}; "
            "the trigger cannot be verified, so the `edited` activity type is not "
            "known to be declared (#1074)"
        ]

    declared = types_decl(block)
    if declared is None:
        return [
            f"the `pull_request:` trigger declares no `types:` key in "
            f"{WORKFLOW_PATH} (trigger at line {block.first_line}); GitHub's "
            "default set is `opened, synchronize, reopened`, which omits "
            "`edited`, so a PR body edit after a green run leaves a verdict "
            "describing text that no longer exists. Declare "
            "`types: [opened, synchronize, reopened, edited]` (#1074)"
        ]

    if "edited" not in declared.values:
        return [
            f"the `pull_request:` trigger's `types:` omits `edited` "
            f"(line {declared.line}: types: {', '.join(declared.values)}); the "
            "validator reads the PR body live, so a body edit after a green run "
            "leaves a verdict describing text that no longer exists. Add "
            "`edited` to the list (#1074)"
        ]
    return []


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

    text = workflow.read_text(encoding="utf-8")
    blocks = job_blocks(text)
    if blocks is None:
        print(
            f"::error::INCOMPLETE: no `jobs:` mapping found in {WORKFLOW_PATH}; "
            "the shape cannot be read, so it cannot be verified",
            file=sys.stderr,
        )
        return 2

    found = violations(blocks) + _trigger_violations(text)
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
        "the verdict job carries no `needs:`, and the `pull_request:` trigger "
        "declares `edited`",
        file=sys.stderr,
    )
    print("SESSION EVIDENCE WORKFLOW SHAPE: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
