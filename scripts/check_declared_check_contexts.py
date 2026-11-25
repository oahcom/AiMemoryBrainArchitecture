#!/usr/bin/env python3
"""Verify that PR-GOVERNANCE-001's declared check contexts agree with reality.

The document declares a set of GitHub check contexts as the required set on
`main`. Two conditions hold that declaration to something that can disagree
with it:

    forward   document A declares a list C of contexts; artifact B
              (`.github/workflows/*.yml`) must produce every member of C.

    reverse   the live branch-protection payload for the branch must require
              exactly C -- no context required but undeclared, and none
              declared but unrequired.

The forward condition alone is what #1029 records as insufficient. Three
`Session Evidence*` contexts were required on the platform while the Normative
document declared twelve; the forward condition passed throughout, because
every declared context was still produced by a job. The direction that broke
was protected -> declared, and nothing read the platform at all.

Both conditions are needed. A rename breaks forward; a protection change that
nobody recorded breaks reverse.

Exit codes follow the repository vocabulary:
    0  PASS        every declared context is produced by a job in this tree,
                   and (when the reverse check was requested) the protected
                   set equals the declared set
    1  VIOLATION   a declared context is produced by no job, or a declared
                   context is not protected, or a protected context is not
                   declared
    2  INCOMPLETE  a condition could not be evaluated at all

The incomplete branch is the point. A checker whose "cannot find the document"
path falls through to "no violations found, exit 0" is a false PASS, which is
worse than having no checker. The same argument applies to the reverse check:
if the protection payload cannot be read, that is INCOMPLETE (2), never PASS.

The reverse check needs a credential to read branch protection, which CI does
not have by default, so it is opt-in (`--protection`). Without the flag it is
skipped and says so; a run that did not read protection never claims it did.
With the flag, a missing token is INCOMPLETE (2), not a silent downgrade.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

DOC_PATH = "14-ai-development/PR-GOVERNANCE-001.md"
MARKER = "<!-- declared-check-contexts"
WORKFLOWS = ".github/workflows"

# Defaults for the reverse check. `GITHUB_REPOSITORY` wins when present, so the
# same script works in a fork without editing the constant.
DEFAULT_REPOSITORY = "oahcom/AiMemoryBrainArchitecture"
DEFAULT_BRANCH = "main"

_API_ROOT = "https://api.github.com"
_API_VERSION = "2022-11-28"
_PROTECTION_PATH = "/repos/{repo}/branches/{branch}/protection/required_status_checks"

# A job id is a top-level key under `jobs:` (2-space indent). Its display name
# is a 4-space `name:` inside that block. GitHub reports the display name when
# present and the job id otherwise, so both are candidate contexts.
JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
JOB_NAME_RE = re.compile(r"^    name:\s*(.+?)\s*$")
FENCE_RE = re.compile(r"^```")


class ProtectionUnavailable(Exception):
    """The protection payload could not be read, so the reverse check is INCOMPLETE."""


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


def _request_json(path: str) -> Any:
    """GET a GitHub API path. Same header construction as the session-evidence gate."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ProtectionUnavailable("GITHUB_TOKEN is missing")

    url = path if path.startswith("https://") else _API_ROOT + path
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": _API_VERSION,
            "User-Agent": "declared-check-contexts-gate",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ProtectionUnavailable(f"GitHub API HTTP {exc.code}: {url}") from exc
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise ProtectionUnavailable(f"GitHub API request failed: {url}: {exc}") from exc


def protected_checks(payload: Any) -> list[tuple[str, int | None]] | None:
    """`(context, app_id)` for every required check in a protection payload.

    Two shapes exist depending on API version: the legacy `contexts` array of
    bare names, and the newer `checks` array of `{context, app_id}`. Which one
    is populated is not something this script controls, so both are accepted;
    the legacy shape yields `app_id is None` because the payload carries no App
    identity there. None means the shape is unusable, which is INCOMPLETE.
    """
    if not isinstance(payload, dict):
        return None

    checks = payload.get("checks")
    if isinstance(checks, list) and checks:
        pairs: list[tuple[str, int | None]] = []
        for item in checks:
            if not isinstance(item, dict):
                return None
            context = item.get("context")
            if not isinstance(context, str) or not context:
                return None
            app_id = item.get("app_id")
            pairs.append((context, app_id if isinstance(app_id, int) else None))
        return pairs

    contexts = payload.get("contexts")
    if isinstance(contexts, list) and contexts:
        if not all(isinstance(name, str) and name for name in contexts):
            return None
        return [(name, None) for name in contexts]

    return None


def compare_protected(
    declared: list[str],
    protected: list[tuple[str, int | None]],
) -> tuple[list[str], list[str]]:
    """Split the two sets into (not protected, not declared).

    The comparison is on names, and only on names, because the declaring
    document lists names and no App: there is no `app_id` on the declared side
    to compare against, and inventing one would assert a fact the document does
    not state. The App requirement is therefore *reported*, not compared -- a
    context can be required of a specific App and a name-only match would still
    pass if a different App published it. `main` prints the `(context, app_id)`
    pairs so a reader can see what was not verified.
    """
    declared_names = set(declared)
    protected_names = {name for name, _ in protected}

    missing_from_protection = [c for c in declared if c not in protected_names]
    undeclared = sorted(protected_names - declared_names)
    return missing_from_protection, undeclared


def main(
    root: Path | None = None,
    branch: str = DEFAULT_BRANCH,
    check_protection: bool = False,
    fetch: Callable[[str], Any] | None = None,
) -> int:
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
    failed = bool(missing)

    for context in missing:
        print(
            f"::error::{DOC_PATH} declares required check context "
            f"{context!r}, but no job in {WORKFLOWS} produces it",
            file=sys.stderr,
        )

    if check_protection:
        repository = os.environ.get("GITHUB_REPOSITORY", "").strip() or DEFAULT_REPOSITORY
        path = _PROTECTION_PATH.format(repo=repository, branch=branch)
        try:
            payload = (fetch or _request_json)(path)
        except ProtectionUnavailable as exc:
            print(
                f"::error::INCOMPLETE: cannot read required status checks for "
                f"{repository}@{branch}: {exc}; protection cannot be verified",
                file=sys.stderr,
            )
            return 2

        protected = protected_checks(payload)
        if protected is None:
            print(
                f"::error::INCOMPLETE: required status checks for "
                f"{repository}@{branch} have an unexpected shape; protection "
                "cannot be verified",
                file=sys.stderr,
            )
            return 2

        not_protected, undeclared = compare_protected(contexts, protected)

        for context in not_protected:
            print(
                f"::error::{DOC_PATH} declares required check context "
                f"{context!r}, but {repository}@{branch} does not require it",
                file=sys.stderr,
            )
        for context in undeclared:
            print(
                f"::error::{repository}@{branch} requires check context "
                f"{context!r}, but {DOC_PATH} does not declare it",
                file=sys.stderr,
            )

        if not_protected or undeclared:
            print(f"declared ({len(contexts)}): {sorted(contexts)}", file=sys.stderr)
            print(
                f"protected ({len(protected)}): "
                f"{sorted((name, app_id) for name, app_id in protected)}",
                file=sys.stderr,
            )
            print(
                "DECLARED CHECK CONTEXTS: FAIL "
                f"({len(not_protected)} declared but unprotected, "
                f"{len(undeclared)} protected but undeclared)",
                file=sys.stderr,
            )
            return 1

        # Names match; the App binding is reported because it was not compared.
        print(
            f"::notice::protected checks on {repository}@{branch}, as "
            f"(context, app_id): "
            f"{sorted((name, app_id) for name, app_id in protected)}",
            file=sys.stderr,
        )
    else:
        print(
            "::notice::reverse check skipped: protection was not requested "
            "(--protection); only declared -> produced was verified",
            file=sys.stderr,
        )

    if failed:
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
    arguments = sys.argv[1:]
    requested = "--protection" in arguments
    arguments = [a for a in arguments if a != "--protection"]
    branch = DEFAULT_BRANCH
    if "--branch" in arguments:
        index = arguments.index("--branch")
        try:
            branch = arguments[index + 1]
        except IndexError:
            print("::error::INCOMPLETE: --branch requires a value", file=sys.stderr)
            sys.exit(2)
        del arguments[index:index + 2]
    sys.exit(
        main(
            arguments[0] if arguments else None,
            branch=branch,
            check_protection=requested,
        )
    )
