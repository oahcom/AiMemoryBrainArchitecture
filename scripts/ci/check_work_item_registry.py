#!/usr/bin/env python3
"""Validate the work-item claim registry.

The ledger is the authoritative record of which pull request holds which
AID work-item id. This checker validates the schema, the state machine, and the
live consistency of CLAIMED rows with GitHub.

State machine (Owner ruling 2026-11-27):

  CLAIMED -> MERGED      allowed
  CLAIMED -> ABANDONED   allowed
  MERGED                 terminal and permanent; the id is never reused
  ABANDONED              does not release the id automatically

Exit codes: 0 PASS; 1 VIOLATION; 2 INCOMPLETE.

Without ``--check-live-prs`` the checker is fully offline. With it, any GitHub
API failure (missing token, HTTP error, unparsable body) is INCOMPLETE: a
verdict is never guessed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REGISTRY = Path("14-ai-development/work-items/registry/work-item-claims.yaml")
ID_RE = re.compile(r"AID-\d{4}-\d{3}\Z")
REPO_RE = re.compile(r"[^/\s]+/[^/\s]+\Z")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
STATUSES = ("CLAIMED", "MERGED", "ABANDONED")
TRANSITIONS = frozenset({("CLAIMED", "MERGED"), ("CLAIMED", "ABANDONED")})
REQUIRED = (
    "work_item_id", "status", "pull_request", "repository", "head_sha",
    "merge_commit_sha", "claimed_at", "updated_at", "owner_work_item", "evidence",
)
API_ROOT = "https://api.github.com"


class Incomplete(RuntimeError):
    """The ledger or the API could not be read; never a PASS."""


def parse_time(value):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def load(path: Path) -> dict:
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise Incomplete(f"registry {path} is missing") from exc
    except (OSError, UnicodeError) as exc:
        raise Incomplete(f"registry {path} unreadable: {exc}") from exc
    except Exception as exc:  # noqa: BLE001 - any parse failure is INCOMPLETE
        raise Incomplete(f"registry {path} unreadable: {type(exc).__name__}: {exc}") from exc
    if not isinstance(data, dict):
        raise Incomplete(f"registry {path} is not a mapping")
    return data


def claim_key(claim: dict) -> tuple:
    return (claim.get("work_item_id"), claim.get("pull_request"), claim.get("repository"))


def validate_schema(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be the integer 1")
    claims = data.get("claims")
    if not isinstance(claims, list):
        return errors + ["claims must be a list"]

    seen_keys: set[tuple] = set()
    for index, claim in enumerate(claims):
        where = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{where} must be a mapping")
            continue
        missing = [field for field in REQUIRED if field not in claim]
        if missing:
            errors.append(f"{where} is missing {', '.join(missing)}")
            continue
        work_item_id = claim["work_item_id"]
        status = claim["status"]
        if not isinstance(work_item_id, str) or not ID_RE.match(work_item_id):
            errors.append(f"{where}.work_item_id must match AID-YYYY-NNN")
        if status not in STATUSES:
            errors.append(f"{where}.status must be one of {', '.join(STATUSES)}")
        if not isinstance(claim["pull_request"], int) or isinstance(claim["pull_request"], bool) \
                or claim["pull_request"] < 1:
            errors.append(f"{where}.pull_request must be a positive integer")
        if not isinstance(claim["repository"], str) or not REPO_RE.match(claim["repository"]):
            errors.append(f"{where}.repository must be owner/name")
        if not isinstance(claim["head_sha"], str) or not SHA_RE.match(claim["head_sha"]):
            errors.append(f"{where}.head_sha must be a full lowercase 40-character SHA")
        merge_sha = claim["merge_commit_sha"]
        if status == "MERGED":
            if not isinstance(merge_sha, str) or not SHA_RE.match(merge_sha):
                errors.append(f"{where}.merge_commit_sha is required for MERGED")
        elif merge_sha is not None:
            errors.append(f"{where}.merge_commit_sha must be null unless status is MERGED")
        claimed_at = parse_time(claim["claimed_at"])
        updated_at = parse_time(claim["updated_at"])
        if claimed_at is None:
            errors.append(f"{where}.claimed_at must be an ISO-8601 timestamp")
        if updated_at is None:
            errors.append(f"{where}.updated_at must be an ISO-8601 timestamp")
        if claimed_at and updated_at and updated_at < claimed_at:
            errors.append(f"{where}.updated_at precedes claimed_at")
        owner = claim["owner_work_item"]
        if owner is not None and not isinstance(owner, str):
            errors.append(f"{where}.owner_work_item must be a string or null")
        evidence = claim["evidence"]
        if not isinstance(evidence, list) or not all(isinstance(item, str) for item in evidence):
            errors.append(f"{where}.evidence must be a list of strings")
        elif status in ("CLAIMED", "MERGED") and not evidence:
            errors.append(f"{where}.evidence must not be empty for {status}")
        key = claim_key(claim)
        if key in seen_keys:
            errors.append(f"{where} duplicates an existing claim for {key[0]} by pull request {key[1]}")
        seen_keys.add(key)
    return errors


def validate_state(data: dict) -> list[str]:
    errors: list[str] = []
    claims = data.get("claims")
    if not isinstance(claims, list):
        return errors
    rows = [claim for claim in claims if isinstance(claim, dict) and "status" in claim]

    by_id: dict[str, list[dict]] = {}
    for claim in rows:
        by_id.setdefault(str(claim.get("work_item_id")), []).append(claim)

    for work_item_id, group in sorted(by_id.items()):
        open_claims = [claim for claim in group if claim.get("status") == "CLAIMED"]
        pull_requests = {claim.get("pull_request") for claim in open_claims}
        if len(pull_requests) > 1:
            errors.append(
                f"{work_item_id} is CLAIMED by more than one pull request "
                f"({', '.join(str(item) for item in sorted(pull_requests))})"
            )
        merged = [claim for claim in group if claim.get("status") == "MERGED"]
        if merged:
            merged_at = max(
                (parse_time(claim.get("updated_at")) for claim in merged if parse_time(claim.get("updated_at"))),
                default=None,
            )
            for claim in group:
                if claim.get("status") == "MERGED":
                    continue
                if claim.get("status") == "CLAIMED":
                    errors.append(
                        f"{work_item_id} is MERGED and may not be re-claimed "
                        f"(pull request {claim.get('pull_request')})"
                    )
                elif merged_at is not None:
                    claimed_at = parse_time(claim.get("claimed_at"))
                    if claimed_at is not None and claimed_at >= merged_at:
                        errors.append(
                            f"{work_item_id} is MERGED; claim by pull request "
                            f"{claim.get('pull_request')} starts after the merge"
                        )
    return errors


def validate_previous(previous: dict, current: dict) -> list[str]:
    """Check that every row only moved along an allowed transition."""
    errors: list[str] = []
    old_rows = {}
    for claim in previous.get("claims") or []:
        if isinstance(claim, dict):
            old_rows[claim_key(claim)] = claim
    new_rows = {}
    for claim in current.get("claims") or []:
        if isinstance(claim, dict):
            new_rows[claim_key(claim)] = claim
    for key, old in old_rows.items():
        label = f"{key[0]} pull request {key[1]}"
        new = new_rows.get(key)
        if new is None:
            errors.append(f"{label} was removed from the ledger; claims are never deleted")
            continue
        before, after = old.get("status"), new.get("status")
        if before == after:
            continue
        if before == "MERGED":
            errors.append(f"{label} was MERGED and cannot move to {after}")
        elif (before, after) not in TRANSITIONS:
            errors.append(f"{label} cannot move {before} -> {after}")
        if before == "CLAIMED" and after == "MERGED" and not new.get("merge_commit_sha"):
            errors.append(f"{label} moved to MERGED without merge_commit_sha")
    for key, new in new_rows.items():
        if key in old_rows:
            continue
        if new.get("status") != "CLAIMED":
            errors.append(
                f"{key[0]} pull request {key[1]} enters the ledger as "
                f"{new.get('status')}; new rows must start CLAIMED"
            )
    return errors


def read_token(token_file: str | None) -> str:
    if token_file:
        try:
            token = Path(token_file).read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            raise Incomplete(f"cannot read token file {token_file}: {exc}") from exc
        if token:
            return token
        raise Incomplete(f"token file {token_file} is empty")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not token.strip():
        raise Incomplete("--check-live-prs requires --token-file or GITHUB_TOKEN/GH_TOKEN")
    return token.strip()


def fetch_pull_request(repository: str, number: int, token: str) -> dict:
    url = f"{API_ROOT}/repos/{repository}/pulls/{number}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "work-item-registry-check",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="strict")
    except (urllib.error.URLError, OSError, UnicodeError, ValueError) as exc:
        raise Incomplete(f"GitHub API {url} failed: {type(exc).__name__}: {exc}") from exc
    try:
        payload = json.loads(body)
    except ValueError as exc:
        raise Incomplete(f"GitHub API {url} returned unparsable JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise Incomplete(f"GitHub API {url} returned a non-object body")
    return payload


def validate_live(data: dict, token: str) -> list[str]:
    errors: list[str] = []
    claims = data.get("claims") or []
    for claim in claims:
        if not isinstance(claim, dict) or claim.get("status") != "CLAIMED":
            continue
        repository = str(claim.get("repository"))
        number = claim.get("pull_request")
        payload = fetch_pull_request(repository, int(number), token)
        if payload.get("state") != "open":
            errors.append(
                f"{claim.get('work_item_id')} pull request {number} is {payload.get('state')}, not open"
            )
        head = payload.get("head")
        live_sha = head.get("sha") if isinstance(head, dict) else None
        if live_sha != claim.get("head_sha"):
            errors.append(
                f"{claim.get('work_item_id')} pull request {number} head_sha is "
                f"{live_sha}, ledger records {claim.get('head_sha')}"
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--previous", default=None,
                        help="earlier revision of the ledger; enables transition checks")
    parser.add_argument("--check-live-prs", action="store_true",
                        help="verify CLAIMED rows against the GitHub API (fails closed)")
    parser.add_argument("--token-file", default=None)
    args = parser.parse_args(argv)

    path = Path(args.registry)
    try:
        data = load(path)
        previous = load(Path(args.previous)) if args.previous else None
        token = read_token(args.token_file) if args.check_live_prs else None
    except Incomplete as exc:
        print(f"WORK-ITEM REGISTRY: INCOMPLETE ({exc})")
        return 2

    errors = validate_schema(data)
    errors += validate_state(data)
    if previous is not None:
        errors += validate_previous(previous, data)

    if token is not None:
        try:
            errors += validate_live(data, token)
        except Incomplete as exc:
            print(f"WORK-ITEM REGISTRY: INCOMPLETE ({exc})")
            return 2

    claims = data.get("claims") if isinstance(data.get("claims"), list) else []
    counts = {status: 0 for status in STATUSES}
    for claim in claims:
        if isinstance(claim, dict) and claim.get("status") in counts:
            counts[claim["status"]] += 1
    summary = (
        f"registry={path} claims={len(claims)} "
        f"claimed={counts['CLAIMED']} merged={counts['MERGED']} abandoned={counts['ABANDONED']} "
        f"live={'checked' if token is not None else 'offline'}"
    )
    if errors:
        for error in errors:
            print(f"VIOLATION: {error}")
        print(f"WORK-ITEM REGISTRY: VIOLATION ({summary})")
        return 1
    print(f"WORK-ITEM REGISTRY: PASS ({summary})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
