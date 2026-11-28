#!/usr/bin/env python3
"""Claim a work-item id by a non-force push to the authoritative ledger ref.

The atomic step is the Git ref update, not the local file write: two writers
that both read the same ledger commit cannot both update the same ref. The
loser's push is rejected as non-fast-forward and must re-read the ledger and
re-scan before trying again. Nothing here retries automatically.

Exit codes: 0 CLAIMED; 1 REFUSED (id already held); 2 INCOMPLETE (ledger
unreadable); 3 LOST_THE_RACE (non-fast-forward); 4 CONFIGURATION.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys

import yaml

REGISTRY = "14-ai-development/work-items/registry/work-item-claims.yaml"
REF = "refs/heads/work-item-claims"
ID_RE = re.compile(r"^AID-[0-9]{4}-[0-9]{3}$")
BLOCKING = frozenset({"CLAIMED", "MERGED"})
RELEASED = frozenset({"ABANDONED", "EXPIRED"})


class Incomplete(RuntimeError):
    pass


def git(*args: str, input_bytes: bytes | None = None, env: dict | None = None):
    full_env = dict(os.environ)
    if env:
        full_env.update(env)
    return subprocess.run(
        ["git", *args], input=input_bytes, capture_output=True, env=full_env
    )


def must(*args: str, input_bytes: bytes | None = None, env: dict | None = None) -> bytes:
    result = git(*args, input_bytes=input_bytes, env=env)
    if result.returncode:
        raise Incomplete(
            f"git {' '.join(args)} exited {result.returncode}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(moment: dt.datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_ledger(commit: str, registry: str) -> dict:
    """Read the ledger from one commit; absent means an empty v2 document."""
    probe = git("cat-file", "-e", f"{commit}:{registry}")
    if probe.returncode:
        return {
            "schema_version": 2,
            "registry": {
                "repository": None,
                "canonical_branch": "work-item-claims",
                "canonical_path": registry,
                "policy": "atomic-single-owner",
            },
            "claims": [],
        }
    raw = must("show", f"{commit}:{registry}")
    try:
        data = yaml.safe_load(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - unreadable ledger is INCOMPLETE
        raise Incomplete(f"{registry} on {commit} is unreadable: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") not in (1, 2):
        raise Incomplete(f"{registry} on {commit} is not a supported ledger")
    if not isinstance(data.get("claims"), list):
        raise Incomplete(f"{registry} on {commit} has no claims list")
    data.setdefault("registry", {})
    data["registry"].setdefault("canonical_branch", "work-item-claims")
    data["registry"].setdefault("canonical_path", registry)
    data["registry"].setdefault("policy", "atomic-single-owner")
    return data


def claim_for(data: dict, work_item_id: str) -> dict | None:
    matches = [c for c in data["claims"] if c.get("work_item_id") == work_item_id]
    if len(matches) > 1:
        raise Incomplete(
            f"ledger holds {len(matches)} current claims for {work_item_id}; "
            "a duplicate current claim is data corruption and must be fixed "
            "by hand before any further claim"
        )
    return matches[0] if matches else None


def write_ledger(work_item_id: str, data: dict, args, stamp: dt.datetime) -> bytes:
    existing = claim_for(data, work_item_id)
    if existing is not None and existing.get("status") in BLOCKING:
        raise SystemExit_refused(
            f"{work_item_id} is already {existing.get('status')} by pull request "
            f"{existing.get('pull_request')} ({existing.get('repository')})"
        )
    history = list(existing.get("history") or []) if existing else []
    if existing is not None:
        history.append(
            {
                "previous_status": existing.get("status"),
                "previous_pull_request": existing.get("pull_request"),
                "previous_owner_work_item": existing.get("owner_work_item"),
                "released_at": existing.get("updated_at"),
                "reason": args.note or "released by a new atomic claim",
            }
        )
    record = {
        "work_item_id": work_item_id,
        "status": "CLAIMED",
        "repository": args.repository,
        "pull_request": args.pull_request,
        "owner_work_item": work_item_id,
        "claimed_at": iso(stamp),
        "updated_at": iso(stamp),
        "expires_at": iso(stamp + dt.timedelta(days=args.expires_days)),
        "head_sha": None,
        "merge_commit_sha": None,
        "reservation": {
            "method": "git-ref",
            "ref": REF,
            "ref_commit_sha": None,
        },
        "evidence": [
            {
                "type": "pull-request" if args.pull_request else "manual",
                "reference": (
                    f"https://github.com/{args.repository}/pull/{args.pull_request}"
                    if args.pull_request
                    else (args.note or "manual claim")
                ),
                "description": "Authoritative claim request",
            }
        ],
        "history": history,
    }
    claims = [c for c in data["claims"] if c.get("work_item_id") != work_item_id]
    claims.append(record)
    claims.sort(key=lambda c: str(c.get("work_item_id")))
    data["claims"] = claims
    data["schema_version"] = 2
    data["registry"]["repository"] = args.repository
    data["registry"]["updated_at"] = iso(stamp)
    data["registry"].setdefault("created_at", iso(stamp))
    return yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, width=1000
    ).encode("utf-8")


class SystemExit_refused(SystemExit):
    def __init__(self, message: str):
        print(f"CLAIM REFUSED: {message}")
        super().__init__(1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True)
    parser.add_argument("--pull-request", type=int, default=None)
    parser.add_argument("--repository", default=None)
    parser.add_argument("--registry", default=REGISTRY)
    parser.add_argument("--ref", default=REF)
    parser.add_argument("--expires-days", type=int, default=14)
    parser.add_argument(
        "--base-commit",
        default=None,
        help=(
            "build the claim on this ledger commit instead of the freshly "
            "fetched ref; used to reproduce a stale writer, whose push must "
            "still be rejected"
        ),
    )
    parser.add_argument("--note", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if not ID_RE.match(args.id):
        print(f"CLAIM REFUSED: {args.id} is not a work-item id")
        return 1
    if args.repository is None:
        url = must("remote", "get-url", "origin").decode().strip()
        match = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
        if not match:
            print("CLAIM INCOMPLETE: cannot derive the repository from origin")
            return 4
        args.repository = match.group(1)

    try:
        fetch = git("fetch", "origin", f"{args.ref}:{args.ref}")
        if fetch.returncode:
            stderr = fetch.stderr.decode("utf-8", "replace")
            tolerated = (
                "couldn't find remote ref",
                "does not appear to be a git repository",
                "No such remote",
            )
            if not any(marker in stderr for marker in tolerated):
                raise Incomplete(stderr.strip() or "fetch failed")
        exists = git("rev-parse", "--verify", f"{args.ref}^{{commit}}")
        base = exists.stdout.decode().strip() if exists.returncode == 0 else None
        if args.base_commit:
            base = must("rev-parse", "--verify", f"{args.base_commit}^{{commit}}").decode().strip()
        if base is None:
            base = must("rev-parse", "origin/main").decode().strip()
        data = load_ledger(base, args.registry)
        payload = write_ledger(args.id, data, args, now_utc())
    except Incomplete as exc:
        print(f"CLAIM INCOMPLETE: {exc}")
        return 2

    if args.dry_run:
        sys.stdout.write(payload.decode("utf-8"))
        return 0

    index = os.environ.get("GIT_INDEX_FILE")
    scratch = os.path.join(
        os.environ.get("TEMP", "/tmp"), f"claim-index-{os.getpid()}"
    )
    env = {"GIT_INDEX_FILE": scratch}
    try:
        must("read-tree", base, env=env)
        blob = must("hash-object", "-w", "--stdin", input_bytes=payload).decode().strip()
        must("update-index", "--add", "--cacheinfo", f"100644,{blob},{args.registry}", env=env)
        tree = must("write-tree", env=env).decode().strip()
        message = f"claim: {args.id} for PR {args.pull_request}\n"
        commit = must("commit-tree", tree, "-p", base, "-m", message).decode().strip()
    finally:
        if os.path.exists(scratch):
            os.remove(scratch)

    push = git("push", "--porcelain", "origin", f"{commit}:{args.ref}")
    if push.returncode:
        print(
            "CLAIM LOST_THE_RACE: the authoritative ref moved while this claim "
            "was being built; re-read the ledger, re-scan the id, and try again. "
            "Do not rebase this claim onto the new ref and re-push it."
        )
        print(push.stderr.decode("utf-8", "replace").strip())
        return 3
    print(f"CLAIMED {args.id} for PR {args.pull_request} at {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
