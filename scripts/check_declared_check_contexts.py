#!/usr/bin/env python3
"""Verify that the required check contexts PR-GOVERNANCE-001 declares are real.

The document declares a set of GitHub check contexts as the required set on
`main`. Two different artifacts can disagree with that declaration, and they
disagree in opposite directions:

  declared -> produced    every declared name is produced by a job in this tree.
                          A renamed job makes the document claim a context that
                          no longer exists. That is the defect class #864 records.
  declared -> protected   every declared name is required on the platform, and
                          every required name is declared. A context added to
                          branch protection without a document change leaves the
                          document under-declaring; a context removed from
                          protection while the document still lists it leaves
                          merges gated by a check that no longer blocks. Neither
                          is visible to the produced test, which is a subset
                          test -- dropping a line can only make it truer. That is
                          the defect class #1029 records.

The protected side is read from `GET /repos/{owner}/{repo}/branches/{branch}`,
whose `protection.required_status_checks.contexts` needs only Contents (read) --
`GITHUB_TOKEN`'s default, and no credential at all on a public repository. The
separate `/protection` endpoint needs Administration (read), which the token
permission vocabulary cannot express; it is not used here and must not be.
`GITHUB_TOKEN` is sent when present, only to raise the anonymous rate limit.

Exit codes follow the repository vocabulary:
    0  PASS        every declared context is produced, and the two sets are equal
    1  VIOLATION   a declared context is produced by no job, or the sets differ
    2  INCOMPLETE  a condition could not be evaluated at all

The incomplete branch is the point, and it covers the credential case: an absent
token is not a reason to skip the comparison, and an unreadable payload is not
"no violations". A checker whose "cannot read the platform" path falls through to
exit 0 is a false PASS, which is worse than having no checker (#1003, #1017).
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

DOC_PATH = "14-ai-development/PR-GOVERNANCE-001.md"
MARKER = "<!-- declared-check-contexts"
WORKFLOWS = ".github/workflows"

# The branch whose protection payload is the protected side of the comparison.
REPO_SLUG = "oahcom/AiMemoryBrainArchitecture"
BRANCH = "main"
TIMEOUT_SECONDS = 20
DEFAULT_API = "https://api.github.com"

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


def fetch_protected_contexts(
    api: str | None = None,
    repo: str = REPO_SLUG,
    branch: str = BRANCH,
    timeout: int = TIMEOUT_SECONDS,
) -> list[str]:
    """The required contexts on `branch`, in payload order.

    Raises on any transport, status or shape failure. The caller turns that into
    INCOMPLETE; this function never returns a value it did not read.
    """
    base = api or os.environ.get("GITHUB_API_URL") or DEFAULT_API
    request = urllib.request.Request(
        f"{base.rstrip('/')}/repos/{repo}/branches/{branch}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "declared-check-contexts",
        },
    )
    # Optional, and only to raise the rate limit. Absence must not skip the
    # comparison: the endpoint is readable without it on a public repository.
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)

    contexts = payload["protection"]["required_status_checks"]["contexts"]
    if not isinstance(contexts, list) or not all(isinstance(c, str) for c in contexts):
        raise ValueError("protection.required_status_checks.contexts is not a list of strings")
    return contexts


def main(root: Path | None = None, protection: list[str] | None = None) -> int:
    """`protection` injects the protected side; None reads it from the platform."""
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

    unproduced = [context for context in contexts if context not in produced]

    if unproduced:
        for context in unproduced:
            print(
                f"::error::{DOC_PATH} declares required check context "
                f"{context!r}, but no job in {WORKFLOWS} produces it",
                file=sys.stderr,
            )
        print(
            f"DECLARED CHECK CONTEXTS: FAIL "
            f"({len(unproduced)} of {len(contexts)} unproduced)",
            file=sys.stderr,
        )
        return 1

    if protection is None:
        try:
            protection = fetch_protected_contexts()
        except Exception as error:  # noqa: BLE001 - every failure is INCOMPLETE
            print(
                "::error::INCOMPLETE: the branch-protection payload could not be "
                "read, so the declared set cannot be compared to it: "
                f"{type(error).__name__}: {error}",
                file=sys.stderr,
            )
            return 2

    if not protection:
        print(
            "::error::INCOMPLETE: the branch-protection payload reports no "
            "required contexts; an empty protected set cannot be compared",
            file=sys.stderr,
        )
        return 2

    undeclared = sorted(set(protection) - set(contexts))
    unprotected = sorted(set(contexts) - set(protection))

    if undeclared or unprotected:
        for context in unprotected:
            print(
                f"::error::{DOC_PATH} declares {context!r}, but it is not a "
                f"required context on {BRANCH}",
                file=sys.stderr,
            )
        for context in undeclared:
            print(
                f"::error::{BRANCH} requires {context!r}, but {DOC_PATH} does not "
                "declare it",
                file=sys.stderr,
            )
        print(
            f"DECLARED CHECK CONTEXTS: FAIL (declared {len(contexts)}, protected "
            f"{len(protection)}; {len(unprotected)} declared-not-protected, "
            f"{len(undeclared)} protected-not-declared)",
            file=sys.stderr,
        )
        return 1

    print(
        f"::notice::{len(contexts)} declared check contexts, all produced by "
        f"a job in {WORKFLOWS} and all required on {BRANCH}",
        file=sys.stderr,
    )
    print("DECLARED CHECK CONTEXTS: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
