#!/usr/bin/env python3
"""Verify the session-evidence workflow shape and its PR-body digest binding.

This guard pins two silent regressions: the three-job independence and edited
trigger introduced for #1014/#1074, and the previously unconsumed PR-body
digest, which allowed the verdict summary to stop binding itself to the body
it judged (#1246).

The properties, each a real failure mode:

  1. All three job ids exist: self-test-trusted-base, self-test-pr-head,
     validate.
  2. No checkout step in self-test-pr-head carries ref:.
  3. validate has no needs:.
  4. pull_request declares edited.
  5. The validate job contains the named body-digest step.
  6. That step runs with if: always().
  7. That step writes AI-SESSION-EVIDENCE-BODY-SHA256 using its digest.
  8. That step validates the digest as 64 lowercase hexadecimal characters.

The workflow is inspected as raw text. This follows the existing guard's
standard-library-only approach and avoids adding a YAML parser dependency.
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
BODY_DIGEST_STEP = "Bind the verdict to the body it judged"

JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
STEP_START_RE = re.compile(r"^(\s*)- \s*\S")
CHECKOUT_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*actions/checkout")
REF_KEY_RE = re.compile(r"^\s*(?:-\s*)?ref:\s*\S")
NEEDS_KEY_RE = re.compile(r"^    needs:(\s*\S|\s*$)")

ON_KEY_RE = re.compile(r"^on:\s*$")
PULL_REQUEST_RE = re.compile(r"^  pull_request:\s*(.*)$")
TYPES_FLOW_RE = re.compile(r"^    types:\s*\[(.*?)\]")
TYPES_BLOCK_RE = re.compile(r"^    types:\s*$")
TYPES_ITEM_RE = re.compile(r"^      -\s*(\S.*?)\s*$")

BODY_DIGEST_NAME_RE = re.compile(
    r"^\s*-\s*name:\s*['\"]?Bind the verdict to the body it judged['\"]?\s*$"
)
BODY_DIGEST_ALWAYS_RE = re.compile(r"^\s*if:\s*always\(\)\s*(?:#.*)?$")
BODY_DIGEST_WRITE_RE = re.compile(
    r'^\s*echo\s+"AI-SESSION-EVIDENCE-BODY-SHA256:\s*\$digest"'
    r'\s*>>\s*"\$GITHUB_STEP_SUMMARY"\s*$'
)
BODY_DIGEST_HEX_RE = re.compile(
    r"""^\s*if\s+!\s*printf\s+'?%s'?\s*"\$digest"\s*\|\s*"""
    r"""grep\s+-Eq\s+'\^\[0-9a-f\]\{64\}\$'\s*;\s*then\s*$"""
)


class JobBlock(NamedTuple):
    """One job's raw lines, plus the 1-based file line its first line came from."""

    text: str
    first_line: int


class StepBlock(NamedTuple):
    """One step's raw lines, plus the 1-based file line its first line came from."""

    text: str
    first_line: int


class TriggerBlock(NamedTuple):
    """The pull_request trigger's raw lines and first line."""

    text: str
    first_line: int


class TypesDecl(NamedTuple):
    """The trigger's types entries and the line of the types key."""

    values: list[str]
    line: int


def job_blocks(text: str) -> dict[str, JobBlock] | None:
    """Map job id to raw block; None means the jobs mapping is absent."""
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.rstrip() == "jobs:"),
        None,
    )
    if start is None:
        return None

    blocks: dict[str, JobBlock] = {}
    current: str | None = None
    body: list[str] = []
    body_start = 0

    for offset, line in enumerate(lines[start + 1:], start=start + 2):
        if line and not line[0].isspace() and not line.startswith("#"):
            break

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
    """Split one job block into step blocks."""
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
    """Return line-specific ref violations in checkout steps."""
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
    """Read the pull_request trigger's raw block."""
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if ON_KEY_RE.match(line)),
        None,
    )
    if start is None:
        return None

    body: list[str] = []
    body_start = 0
    for offset, line in enumerate(lines[start + 1:], start=start + 2):
        if line and not line[0].isspace() and not line.startswith("#"):
            break
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
    """Read flow-form or block-form types entries."""
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
    """Check the edited trigger property."""
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
    """Check the existing three-job independence properties."""
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


def _body_digest_violations(blocks: dict[str, JobBlock]) -> list[str]:
    """Pin the PR-body digest that was previously written but never consumed.

    All three requirements must occur inside the uniquely named step. The
    diagnostic identifies the exact mutation and gives a source line.
    """
    if VERDICT_JOB not in blocks:
        return []

    verdict = blocks[VERDICT_JOB]
    matching = []
    for step in steps(verdict):
        lines = step.text.splitlines()
        if any(BODY_DIGEST_NAME_RE.match(line) for line in lines):
            matching.append(step)

    if not matching:
        return [
            f"PR body digest mutation 1: named step {BODY_DIGEST_STEP!r} is "
            f"missing (expected within {VERDICT_JOB!r}, near line "
            f"{verdict.first_line}); the body digest is no longer bound to "
            "the verdict"
        ]

    found: list[str] = []
    for step in matching:
        lines = step.text.splitlines()
        named_line = next(
            (
                step.first_line + index
                for index, line in enumerate(lines)
                if BODY_DIGEST_NAME_RE.match(line)
            ),
            step.first_line,
        )

        always_line = next(
            (
                step.first_line + index
                for index, line in enumerate(lines)
                if line.lstrip().startswith("if:")
            ),
            named_line,
        )
        if not any(BODY_DIGEST_ALWAYS_RE.match(line) for line in lines):
            found.append(
                f"PR body digest mutation 2: {BODY_DIGEST_STEP!r} must use "
                f"`if: always()` (line {always_line}); `success()` or a missing "
                "condition can suppress the digest after a failed verdict"
            )

        write_line = next(
            (
                step.first_line + index
                for index, line in enumerate(lines)
                if "AI-SESSION-EVIDENCE-BODY-SHA256" in line
                or "AI-SESSION-EVIDENCE: PRESENT" in line
            ),
            named_line,
        )
        if not any(BODY_DIGEST_WRITE_RE.match(line) for line in lines):
            found.append(
                f"PR body digest mutation 3: {BODY_DIGEST_STEP!r} must write "
                f"`AI-SESSION-EVIDENCE-BODY-SHA256: $digest` to "
                f"`$GITHUB_STEP_SUMMARY` (line {write_line}); a generic "
                "`AI-SESSION-EVIDENCE: PRESENT` is not a body digest"
            )

        hex_line = next(
            (
                step.first_line + index
                for index, line in enumerate(lines)
                if "grep" in line and "64" in line
            ),
            named_line,
        )
        if not any(BODY_DIGEST_HEX_RE.match(line) for line in lines):
            found.append(
                f"PR body digest contract: {BODY_DIGEST_STEP!r} must validate "
                f"64 lowercase hexadecimal characters (line {hex_line}); "
                "the digest shape is not enforced"
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

    found = (
        violations(blocks)
        + _trigger_violations(text)
        + _body_digest_violations(blocks)
    )
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
        "the verdict job carries no `needs:`, the `pull_request:` trigger "
        "declares `edited`, and the verdict binds its PR body digest",
        file=sys.stderr,
    )
    print("SESSION EVIDENCE WORKFLOW SHAPE: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
