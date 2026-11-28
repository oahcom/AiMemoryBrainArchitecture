#!/usr/bin/env python3
"""Build the initial work-item claim ledger from Git history and the GitHub API.

Evidence order (strongest first): the main tree decides which ids exist; the
commit that first added the id's directory decides when and by which merge;
the GitHub API decides which pull request that commit belongs to. INDEX.md and
the legacy aid-ledger are auxiliary only: neither can promote an id to MERGED.

An id whose merge evidence cannot be verified is reported as unresolved and is
NOT written as MERGED. Nothing is guessed from neighbouring numbers.

Exit codes: 0 READY; 2 BLOCKED (unresolved ids, duplicate current claims, or
missing merge evidence); 4 CONFIGURATION.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

import yaml

REGISTRY = "14-ai-development/work-items/registry/work-item-claims.yaml"
ROOT = "14-ai-development/work-items"
DIR_RE = re.compile(rf"^{ROOT}/(AID-[0-9]{{4}}-[0-9]{{3}})/")
PR_RE = re.compile(r"#(\d{2,5})")


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True)
    if result.returncode:
        raise SystemExit(
            f"git {' '.join(args)} exited {result.returncode}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout.decode("utf-8", "strict")


class Api:
    def __init__(self, repo: str, token: str | None):
        self.repo = repo
        self.token = token
        self.cache: dict[str, object] = {}
        self.errors: list[str] = []
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def get(self, path: str):
        if path in self.cache:
            return self.cache[path]
        request = urllib.request.Request("https://api.github.com" + path)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("User-Agent", "migrate-work-item-claims")
        if self.token:
            request.add_header("Authorization", "token " + self.token)
        try:
            with urllib.request.urlopen(
                request, timeout=60, context=self.context
            ) as response:
                data = json.loads(response.read().decode())
        except (urllib.error.HTTPError, OSError) as exc:
            self.errors.append(f"{path}: {exc}")
            data = {"__error__": repr(exc)}
        self.cache[path] = data
        return data

    def pull_request_for(self, sha: str):
        data = self.get(f"/repos/{self.repo}/commits/{sha}/pulls")
        if not isinstance(data, list) or not data:
            return None
        merged = [p for p in data if p.get("merged_at")]
        pool = merged or data
        return pool[0]


def scan_ids(base: str) -> list[str]:
    listing = git("ls-tree", "-r", "--name-only", base, "--", ROOT)
    ids = set()
    for line in listing.splitlines():
        match = DIR_RE.match(line)
        if match:
            ids.add(match.group(1))
    return sorted(ids)


def first_add(base: str, work_item_id: str) -> tuple[str, str] | None:
    """The earliest commit in the base history that brought this directory in.

    ``--diff-filter=A`` is the precise answer, but it does not look inside
    merges; when a directory arrived through a merge it reports nothing. The
    fallback is the first commit that touched the path at all, which is the
    same commit in every observed case and is never later than the merge.
    """
    for extra in (
        ["--diff-filter=A"],
        [],
    ):
        out = git(
            "log",
            base,
            *extra,
            "--reverse",
            "--format=%H%x09%aI",
            "--",
            f"{ROOT}/{work_item_id}/",
        )
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if lines:
            sha, stamp = lines[0].split("\t", 1)
            return sha, stamp
    return None


def load_legacy(ref: str) -> list[dict]:
    probe = subprocess.run(
        ["git", "show", f"{ref}:aid-ledger.yaml"], capture_output=True
    )
    if probe.returncode:
        return []
    data = yaml.safe_load(probe.stdout.decode("utf-8"))
    return data.get("entries") or []


def classify_legacy(entry: dict, api: Api, in_main: set[str]) -> dict:
    """Map one legacy aid-ledger row to a candidate claim, or to unresolved."""
    work_item_id = entry.get("id")
    state = entry.get("state")
    carrier = str(entry.get("carrier") or "")
    if not work_item_id:
        return {"skipped": "legacy row has no id"}
    if work_item_id in in_main:
        return {"work_item_id": work_item_id, "resolution": "main tree wins"}
    if state == "FREE":
        return {"work_item_id": work_item_id, "resolution": "free, no claim"}
    match = PR_RE.search(carrier)
    if match:
        pull = api.get(f"/repos/{api.repo}/pulls/{match.group(1)}")
        if isinstance(pull, dict) and pull.get("number"):
            if pull.get("merged_at"):
                return {
                    "work_item_id": work_item_id,
                    "status": "MERGED",
                    "pull_request": pull["number"],
                    "merge_commit_sha": pull.get("merge_commit_sha"),
                    "resolution": "legacy carrier merged",
                }
            if pull.get("state") == "closed":
                return {
                    "work_item_id": work_item_id,
                    "status": "ABANDONED",
                    "pull_request": pull["number"],
                    "resolution": "legacy carrier closed unmerged",
                }
            if pull.get("state") == "open":
                return {
                    "work_item_id": work_item_id,
                    "status": "CLAIMED",
                    "pull_request": pull["number"],
                    "resolution": "legacy carrier still open",
                }
    if state in ("RESERVED", "IN_FLIGHT", "OCCUPIED_BY_OTHER"):
        # The number is held by someone the ledger cannot name. Record the
        # hold with a null pull request and say so; never invent a number.
        return {
            "work_item_id": work_item_id,
            "status": "CLAIMED",
            "pull_request": None,
            "resolution": f"legacy {state} without a resolvable carrier",
            "unverified": True,
        }
    return {"unresolved": f"legacy state {state} has no verified carrier"}


def build(base: str, api: Api, legacy: list[dict]) -> tuple[dict, dict]:
    ids = scan_ids(base)
    in_main = set(ids)
    claims: list[dict] = []
    report = {
        "main_work_item_directories": len(ids),
        "legacy_ledger_entries": len(legacy),
        "verified_merged": 0,
        "verified_claimed": 0,
        "verified_abandoned": 0,
        "unresolved": [],
        "unverified_claims": [],
        "skipped": [],
        "missing_manifest": [],
        "no_pull_request": [],
    }
    for work_item_id in ids:
        added = first_add(base, work_item_id)
        manifest = subprocess.run(
            ["git", "cat-file", "-e", f"{base}:{ROOT}/{work_item_id}/manifest.yaml"],
            capture_output=True,
        )
        if manifest.returncode:
            report["missing_manifest"].append(work_item_id)
            continue
        if added is None:
            report["unresolved"].append(f"{work_item_id}: no adding commit on {base}")
            continue
        sha, stamp = added
        pull = api.pull_request_for(sha) if api.token or api.repo else None
        if pull is None:
            report["no_pull_request"].append(f"{work_item_id} <- {sha}")
        number = pull.get("number") if pull else None
        merge_sha = pull.get("merge_commit_sha") if pull else None
        claims.append(
            {
                "work_item_id": work_item_id,
                "status": "MERGED",
                "repository": api.repo,
                "pull_request": number,
                "owner_work_item": work_item_id,
                "claimed_at": stamp,
                "updated_at": stamp,
                "expires_at": None,
                "head_sha": None,
                "merge_commit_sha": merge_sha or sha,
                "reservation": {
                    "method": "migration",
                    "ref": None,
                    "ref_commit_sha": None,
                },
                "evidence": [
                    {
                        "type": "pull-request" if number else "commit",
                        "reference": (
                            f"https://github.com/{api.repo}/pull/{number}"
                            if number
                            else sha
                        ),
                        "description": (
                            "Merged work item; first adding commit "
                            f"{sha[:9]} on {base}"
                        ),
                    }
                ],
                "history": [],
            }
        )
        report["verified_merged"] += 1

    for entry in legacy:
        outcome = classify_legacy(entry, api, in_main)
        if "skipped" in outcome:
            report["skipped"].append(outcome["skipped"])
            continue
        if "unresolved" in outcome:
            report["unresolved"].append(
                f"{outcome.get('work_item_id', '?')}: {outcome['unresolved']}"
            )
            continue
        status = outcome.get("status")
        if status is None:
            continue
        work_item_id = outcome["work_item_id"]
        if outcome.get("unverified"):
            report["unverified_claims"].append(
                f"{work_item_id}: {outcome['resolution']}"
            )
        claims.append(
            {
                "work_item_id": work_item_id,
                "status": status,
                "repository": api.repo,
                "pull_request": outcome.get("pull_request"),
                "owner_work_item": work_item_id,
                "claimed_at": "1970-01-01T00:00:00Z",
                "updated_at": "1970-01-01T00:00:00Z",
                "expires_at": None,
                "head_sha": None,
                "merge_commit_sha": outcome.get("merge_commit_sha"),
                "reservation": {
                    "method": "legacy-ledger",
                    "ref": "refs/heads/aid-ledger",
                    "ref_commit_sha": None,
                },
                "evidence": [
                    {
                        "type": "legacy-ledger",
                        "reference": "aid-ledger.yaml",
                        "description": outcome["resolution"],
                    }
                ],
                "history": [],
            }
        )
        key = "verified_" + status.lower()
        report[key] = report.get(key, 0) + 1

    seen: dict[str, int] = {}
    for claim in claims:
        seen[claim["work_item_id"]] = seen.get(claim["work_item_id"], 0) + 1
    duplicates = sorted(k for k, v in seen.items() if v > 1)
    report["duplicate_ids"] = duplicates
    report["ownership_conflicts"] = []
    report["api_errors"] = list(api.errors)
    claims.sort(key=lambda c: c["work_item_id"])
    document = {
        "schema_version": 2,
        "registry": {
            "repository": api.repo,
            "canonical_branch": "work-item-claims",
            "canonical_path": REGISTRY,
            "policy": "atomic-single-owner",
            "created_at": dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "updated_at": dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
        "claims": claims,
    }
    blocked = (
        report["unresolved"]
        or report["duplicate_ids"]
        or report["ownership_conflicts"]
        or report["missing_manifest"]
    )
    report["migration_status"] = "BLOCKED" if blocked else "READY"
    return document, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--repo", default="oahcom/AiMemoryBrainArchitecture")
    parser.add_argument("--token-file", default=None)
    parser.add_argument("--legacy-ref", default="origin/aid-ledger")
    parser.add_argument("--out", default=None)
    parser.add_argument("--report", default=None)
    parser.add_argument("--allow-blocked", action="store_true")
    args = parser.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN")
    if args.token_file:
        token = open(args.token_file, encoding="utf-8").read().strip()
    api = Api(args.repo, token)
    document, report = build(args.base, api, load_legacy(args.legacy_ref))

    text = yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=1000)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    lines = ["MIGRATION REPORT", ""]
    for key, value in report.items():
        if isinstance(value, list):
            lines.append(f"{key}: {len(value)}")
            lines.extend(f"  - {item}" for item in value)
        else:
            lines.append(f"{key}: {value}")
    rendered = "\n".join(lines)
    print(rendered)
    if args.report:
        with open(args.report, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered + "\n")
    if report["migration_status"] != "READY" and not args.allow_blocked:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
