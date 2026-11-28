"""Resolve and validate the merge-queue candidate prefix.

Exit codes:
  0: every member in the candidate prefix was resolved and --exec passed
  1: a confirmed policy violation or a member command failed
  2: queue membership or Git graph could not be established
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


API_ROOT = "https://api.github.com"
API_VERSION = "2022-11-28"


class CandidateError(Exception):
    """Base error for candidate resolution."""


class CandidateViolation(CandidateError):
    """A confirmed candidate membership violation."""


class QueueMembershipIncomplete(CandidateError):
    """The queue snapshot cannot establish a reliable membership prefix."""


class GitGraphIncomplete(CandidateError):
    """A required Git commit or ancestry relation cannot be established."""

def _request_json(url: str, token: str) -> Any:
    request = urllib.request.Request(
        url if url.startswith("https://") else API_ROOT + url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "merge-group-candidate-gate",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            UnicodeDecodeError, json.JSONDecodeError, OSError) as exc:
        raise QueueMembershipIncomplete(
            f"GitHub API read failed for {url}: {type(exc).__name__}: {exc}"
        ) from exc


def _graphql(token: str, query: str, variables: dict) -> dict:
    payload = json.dumps(
        {"query": query, "variables": variables}
    ).encode("utf-8")
    request = urllib.request.Request(
        API_ROOT + "/graphql",
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "merge-group-candidate-gate",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            UnicodeDecodeError, json.JSONDecodeError, OSError) as exc:
        raise QueueMembershipIncomplete(
            f"MergeQueue GraphQL read failed: {type(exc).__name__}: {exc}"
        ) from exc
    if not isinstance(result, dict) or result.get("errors"):
        raise QueueMembershipIncomplete(
            f"MergeQueue GraphQL returned errors: "
            f"{result.get('errors') if isinstance(result, dict) else result!r}"
        )
    data = result.get("data")
    if not isinstance(data, dict):
        raise QueueMembershipIncomplete("GraphQL response has no data object")
    return data


_QUERY = """
query MergeQueueEntries($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    mergeQueue {
      entries(first: 100, after: $after) {
        nodes {
          position
          pullRequest {
            number
            headRefOid
          }
          headCommit {
            oid
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
"""


def _queue_snapshot(token: str, owner: str, name: str) -> list[dict]:
    entries: list[dict] = []
    cursor = None
    seen_cursors = set()

    while True:
        data = _graphql(
            token,
            _QUERY,
            {"owner": owner, "name": name, "after": cursor},
        )
        repository = data.get("repository")
        if not isinstance(repository, dict):
            raise QueueMembershipIncomplete(
                "GraphQL response has no repository object"
            )
        merge_queue = repository.get("mergeQueue")
        if not isinstance(merge_queue, dict):
            raise QueueMembershipIncomplete(
                "GraphQL response has no repository.mergeQueue object"
            )
        connection = merge_queue.get("entries")
        if not isinstance(connection, dict):
            raise QueueMembershipIncomplete(
                "GraphQL response has no mergeQueue.entries connection"
            )

        nodes = connection.get("nodes")
        page_info = connection.get("pageInfo")
        if not isinstance(nodes, list) or not isinstance(page_info, dict):
            raise QueueMembershipIncomplete(
                "GraphQL entries must contain nodes and pageInfo"
            )
        entries.extend(nodes)

        has_next = page_info.get("hasNextPage")
        end_cursor = page_info.get("endCursor")
        if not isinstance(has_next, bool):
            raise QueueMembershipIncomplete(
                "GraphQL pageInfo.hasNextPage is not boolean"
            )
        if not has_next:
            break
        if not isinstance(end_cursor, str) or not end_cursor:
            raise QueueMembershipIncomplete(
                "GraphQL pagination says hasNextPage without endCursor"
            )
        if end_cursor in seen_cursors:
            raise QueueMembershipIncomplete(
                "GraphQL pagination repeated an endCursor"
            )
        seen_cursors.add(end_cursor)
        cursor = end_cursor

    return entries


def _stable_queue_snapshot(token: str, owner: str, name: str) -> list[dict]:
    first = _queue_snapshot(token, owner, name)
    second = _queue_snapshot(token, owner, name)
    if first != second:
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: queue changed between snapshots"
        )
    return first


def _git_is_ancestor(
    ancestor: str,
    descendant: str,
    repository: str | None = None,
) -> bool:
    """Use GitHub Compare API; never depend on local checkout objects.

    For GET /compare/{ancestor}...{descendant}, ancestor is established
    only when behind_by is zero and the merge base is exactly ancestor.
    API failures and incomplete responses are Git-graph incompleteness.
    """
    ancestor = _validate_oid(ancestor, "ancestor")
    descendant = _validate_oid(descendant, "descendant")
    repository = repository or os.environ.get("GITHUB_REPOSITORY", "")
    if not re.fullmatch(r"[^/]+/[^/]+", repository):
        raise GitGraphIncomplete(
            "GIT_GRAPH_INCOMPLETE: GITHUB_REPOSITORY is missing or invalid"
        )

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise GitGraphIncomplete(
            "GIT_GRAPH_INCOMPLETE: GITHUB_TOKEN is missing"
        )

    url = (
        f"/repos/{repository}/compare/"
        f"{ancestor}...{descendant}"
    )
    try:
        response = _request_json(url, token)
    except Exception as exc:
        raise GitGraphIncomplete(
            f"GIT_GRAPH_INCOMPLETE: compare API failed for "
            f"{ancestor}...{descendant}: {type(exc).__name__}: {exc}"
        ) from exc

    if not isinstance(response, dict):
        raise GitGraphIncomplete(
            "GIT_GRAPH_INCOMPLETE: compare API response is not an object"
        )

    behind_by = response.get("behind_by")
    merge_base = response.get("merge_base_commit")
    merge_base_sha = (
        merge_base.get("sha") if isinstance(merge_base, dict) else None
    )

    if (
        not isinstance(behind_by, int)
        or isinstance(behind_by, bool)
        or behind_by < 0
        or not isinstance(merge_base_sha, str)
        or not re.fullmatch(r"[0-9a-fA-F]{40,64}", merge_base_sha)
    ):
        raise GitGraphIncomplete(
            "GIT_GRAPH_INCOMPLETE: compare API omitted valid "
            "behind_by or merge_base_commit.sha"
        )

    # A zero behind count alone is not sufficient: verify the merge base
    # is the proposed ancestor. Equality is included as ancestry; callers
    # that require a strict incremental head classify equality as already
    # contained in base.
    return (
        behind_by == 0
        and merge_base_sha.lower() == ancestor
    )

def _validate_oid(value: Any, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}", value
    ):
        raise GitGraphIncomplete(
            f"GIT_GRAPH_INCOMPLETE: {label} is missing or invalid"
        )
    return value.lower()


def _tail_number_from_ref(github_ref: str) -> int:
    match = re.search(r"(?:^|/)pr-([0-9]+)-[^/]+$", github_ref)
    if not match:
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: GITHUB_REF has no pr-N tail marker"
        )
    return int(match.group(1))


def _resolve_members(
    entries: list[dict],
    tail_pr: int,
    base_sha: str,
    candidate_sha: str,
) -> list[dict]:
    if not entries:
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: merge queue entries are empty"
        )

    # Validate all entry shapes before selecting the tail. A malformed
    # entry cannot be silently ignored merely because it is not the tail.
    normalized = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: queue entry is not an object"
            )
        position = entry.get("position")
        if not isinstance(position, int) or isinstance(position, bool) or position <= 0:
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: queue entry has invalid position"
            )
        normalized.append(entry)

    tail_matches = []
    for entry in normalized:
        pr = entry.get("pullRequest")
        if isinstance(pr, dict) and pr.get("number") == tail_pr:
            tail_matches.append(entry)

    if len(tail_matches) != 1:
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: tail PR "
            f"#{tail_pr} matched {len(tail_matches)} queue entries"
        )

    tail = tail_matches[0]
    tail_position = tail["position"]

    prefix = [
        entry for entry in normalized
        if entry["position"] <= tail_position
    ]
    positions = [entry["position"] for entry in prefix]
    if len(positions) != len(set(positions)):
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: duplicate queue positions"
        )

    prefix.sort(key=lambda item: item["position"])
    if not prefix or prefix[-1] is not tail:
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: tail position cannot be confirmed"
        )

    # The tail entry is unique, but PR identity must also be unique across
    # the entire candidate prefix. Do this before per-entry head checks.
    pr_numbers = []
    for entry in prefix:
        pr = entry.get("pullRequest")
        if not isinstance(pr, dict):
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: prefix entry has no pullRequest"
            )
        number = pr.get("number")
        if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: prefix PR number is invalid"
            )
        pr_numbers.append(number)

    if len(pr_numbers) != len(set(pr_numbers)):
        raise QueueMembershipIncomplete(
            "QUEUE_MEMBERSHIP_INCOMPLETE: duplicate PR number in queue prefix"
        )

    members = []
    for entry in prefix:
        pr = entry["pullRequest"]
        number = pr["number"]
        head_commit = entry.get("headCommit")

        pr_head = _validate_oid(
            pr.get("headRefOid"), f"PR #{number} headRefOid"
        )
        if not isinstance(head_commit, dict):
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: prefix entry has no headCommit"
            )
        candidate_head = _validate_oid(
            head_commit.get("oid"), f"PR #{number} headCommit.oid"
        )

        if candidate_head != pr_head:
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: PR/headCommit identity changed "
                f"for PR #{number}"
            )

        members.append(
            {
                "position": entry["position"],
                "number": number,
                "head_sha": pr_head,
            }
        )

    base = _validate_oid(base_sha, "base_sha")
    candidate = _validate_oid(candidate_sha, "candidate_sha")
    repository = os.environ.get("GITHUB_REPOSITORY", "")

    # A base not contained in the candidate is a confirmed violation.
    if not _git_is_ancestor(base, candidate, repository):
        raise CandidateViolation(
            "BASE_NOT_IN_CANDIDATE: base_sha is not an ancestor of candidate_sha"
        )

    for member in members:
        head = member["head_sha"]
        number = member["number"]

        # This is a confirmed no-increment condition, not missing evidence.
        if _git_is_ancestor(head, base, repository):
            raise CandidateViolation(
                "PR_HEAD_ALREADY_IN_BASE: PR "
                f"#{number} head is already contained in base"
            )

        if not _git_is_ancestor(head, candidate, repository):
            raise CandidateViolation(
                "PR_HEAD_NOT_IN_CANDIDATE: PR "
                f"#{number} head is not an ancestor of candidate_sha"
            )

    return members

def _load_member_bodies(
    token: str, repository: str, members: list[dict]
) -> list[dict]:
    result = []
    for member in members:
        url = f"/repos/{repository}/pulls/{member['number']}"
        pr = _request_json(url, token)
        if not isinstance(pr, dict) or pr.get("number") != member["number"]:
            raise QueueMembershipIncomplete(
                "QUEUE_MEMBERSHIP_INCOMPLETE: PR body lookup identity mismatch "
                f"for #{member['number']}"
            )
        body = pr.get("body")
        if body is None:
            body = ""
        if not isinstance(body, str):
            raise QueueMembershipIncomplete(
                f"QUEUE_MEMBERSHIP_INCOMPLETE: PR #{member['number']} body is invalid"
            )
        result.append({**member, "body": body})
    return result


def _write_output(path: str, document: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(target)


def _exec_members(command: str, members: list[dict]) -> int:
    try:
        argv = shlex.split(command, posix=True)
    except ValueError as exc:
        print(f"INCOMPLETE: invalid --exec command: {exc}", file=sys.stderr)
        return 2
    if not argv:
        print("INCOMPLETE: --exec command is empty", file=sys.stderr)
        return 2

    overall = 0
    for member in members:
        env = os.environ.copy()
        env["PR_NUMBER"] = str(member["number"])
        env["PR_BODY"] = member["body"]
        try:
            result = subprocess.run(argv, env=env, check=False)
        except OSError as exc:
            print(
                f"INCOMPLETE: cannot execute member command for "
                f"PR #{member['number']}: {exc}",
                file=sys.stderr,
            )
            overall = 2
            continue
        if result.returncode == 1:
            overall = max(overall, 1)
        elif result.returncode != 0:
            overall = 2
    return overall


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--exec", dest="exec_command")
    args = parser.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not re.fullmatch(r"[^/]+/[^/]+", repository):
        print(
            "QUEUE_MEMBERSHIP_INCOMPLETE: GITHUB_TOKEN or "
            "GITHUB_REPOSITORY is missing",
            file=sys.stderr,
        )
        return 2

    try:
        owner, name = repository.split("/", 1)
        tail_pr = _tail_number_from_ref(os.environ.get("GITHUB_REF", ""))
        base_sha = _validate_oid(
            os.environ.get("MERGE_GROUP_BASE_SHA"), "MERGE_GROUP_BASE_SHA"
        )
        candidate_sha = _validate_oid(
            os.environ.get("MERGE_GROUP_HEAD_SHA"), "MERGE_GROUP_HEAD_SHA"
        )
        entries = _stable_queue_snapshot(token, owner, name)
        members = _resolve_members(
            entries, tail_pr, base_sha, candidate_sha
        )
        members = _load_member_bodies(token, repository, members)
        document = {
            "repository": repository,
            "tail_pr": tail_pr,
            "base_sha": base_sha,
            "candidate_sha": candidate_sha,
            "members": members,
        }
        _write_output(args.output, document)
    except CandidateViolation as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (QueueMembershipIncomplete, GitGraphIncomplete) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.exec_command is None:
        return 0
    return _exec_members(args.exec_command, members)


if __name__ == "__main__":
    raise SystemExit(main())
