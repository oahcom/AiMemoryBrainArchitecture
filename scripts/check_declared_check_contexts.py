#!/usr/bin/env python3
"""Verify that every check context PR-GOVERNANCE-001 declares is still produced.

The document declares a set of GitHub check contexts as the required set on
`main`. Those names are asserted about a different artifact -- the workflows in
this tree -- and nothing else re-reads them: rename a job and the document keeps
claiming a context that no longer exists. That is the defect class #864 records.

This is deliberately one condition: document A declares a list C of contexts,
artifact B (`.github/workflows/*.yml`) must produce every member of C.

Exit codes follow the repository vocabulary:
    0  PASS        every declared context is produced by a job in this tree
    1  VIOLATION   a declared context is produced by no job
    2  INCOMPLETE  the condition could not be evaluated at all

The incomplete branch is the point. A checker whose "cannot find the document"
path falls through to "no violations found, exit 0" is a false PASS, which is
worse than having no checker.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOC_PATH = "14-ai-development/PR-GOVERNANCE-001.md"
MARKER = "<!-- declared-check-contexts"
WORKFLOWS = ".github/workflows"

# A job id is a top-level key under `jobs:` (2-space indent). Its display name
# is a 4-space `name:` inside that block. GitHub reports the display name when
# present and the job id otherwise, so both are candidate contexts.
JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
JOB_NAME_RE = re.compile(r"^    name:\s*(.+?)\s*$")
FENCE_RE = re.compile(r"^```")


def declared_contexts(doc_text: str) -> list[str] | None:
    """The fenced block under the marker, one context per line. None if absent."""
    lines = doc_text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.lstrip().startswith(MARKER)),
        None,
    )
    if start is None:
        return None

    opening = next(
        (i for i in range(start, len(lines)) if FENCE_RE.match(lines[i])),
        None,
    )
    if opening is None:
        return None

    contexts = []
    for line in lines[opening + 1:]:
        if FENCE_RE.match(line):
            break
        name = line.strip()
        if name:
            contexts.append(name)
    return contexts or None


def produced_contexts(workflow_text: str) -> set[str]:
    """Job ids and job display names in one workflow file."""
    found: set[str] = set()
    in_jobs = False
    current: str | None = None

    for line in workflow_text.splitlines():
        if not in_jobs:
            if line.rstrip() == "jobs:":
                in_jobs = True
            continue

        # Any column-0 key ends the jobs mapping.
        if line and not line[0].isspace() and not line.startswith("#"):
            break

        job_id = JOB_ID_RE.match(line)
        if job_id:
            current = job_id.group(1)
            found.add(current)
            continue

        job_name = JOB_NAME_RE.match(line)
        if job_name and current is not None:
            found.add(job_name.group(1).strip("'\""))

    return found


def main(root: Path | None = None) -> int:
    root = Path(root or ".").resolve()
    doc = root / DOC_PATH

    if not doc.is_file():
        print(
            f"::error::INCOMPLETE: declaring document is absent: {DOC_PATH}",
            file=sys.stderr,
        )
        return 2

    contexts = declared_contexts(doc.read_text(encoding="utf-8"))
    if contexts is None:
        print(
            "::error::INCOMPLETE: no declared-context block found in "
            f"{DOC_PATH}; the condition cannot be read, so it cannot be verified",
            file=sys.stderr,
        )
        return 2

    workflows_dir = root / WORKFLOWS
    workflow_files = sorted(workflows_dir.glob("*.yml"))
    if not workflow_files:
        print(
            f"::error::INCOMPLETE: no workflows under {WORKFLOWS}; "
            "no context can be shown to be produced",
            file=sys.stderr,
        )
        return 2

    produced: set[str] = set()
    for path in workflow_files:
        produced |= produced_contexts(path.read_text(encoding="utf-8"))

    missing = [context for context in contexts if context not in produced]

    if missing:
        for context in missing:
            print(
                f"::error::{DOC_PATH} declares required check context "
                f"{context!r}, but no job in {WORKFLOWS} produces it",
                file=sys.stderr,
            )
        print(
            f"DECLARED CHECK CONTEXTS: FAIL "
            f"({len(missing)} of {len(contexts)} unproduced)",
            file=sys.stderr,
        )
        return 1

    print(
        f"::notice::{len(contexts)} declared check contexts, all produced by "
        f"a job in {WORKFLOWS}",
        file=sys.stderr,
    )
    print("DECLARED CHECK CONTEXTS: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
