#!/usr/bin/env python3
"""Read-only, fail-closed verifier for the four historical REQ-01 assessment comments."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Callable

REPOSITORY = "oahcom/AiMemoryBrainArchitecture"
COMMENT_IDS = (7011312621, 7014315135, 7143927480, 7149369280)
EXPECTED = {
    7011312621: {
        "assessor_session": "6afdd273-f2e8-83e8-b554-e52408b6086e",
        "assessed_version": "d61f813cac6780b6bcc5c09536a8e9bee96cc362",
    },
    7014315135: {
        "assessor_session": "6afdd273-f2e8-83e8-b554-e52408b6086e",
        "assessed_version": "d61f813cac6780b6bcc5c09536a8e9bee96cc362",
    },
    7143927480: {
        "assessor_session": "6b05b478-39e0-83ec-8bf-03ff7eb53ce5",
        "assessed_version": "aeebcbeefae874aabdf85c44f74dffd6d8fc0a1e",
    },
    7149369280: {
        "assessor_session": "6b0633de-b128-83ec-b601-d6931b084344",
        "assessed_version": "a33b482e5da5f78c4144e85dd9aef0f3f2e54fbf",
    },
}
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")


def fetch_comment(comment_id: int) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to read the four Issue #262 assessment comments")
    url = f"https://api.github.com/repos/{REPOSITORY}/issues/comments/{comment_id}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AID-2026-250-read-only-checker",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def field(body: str, name: str) -> str | None:
    match = re.search(
        rf"(?im)^\s*(?:[-*]\s*)?{re.escape(name)}\s*:\s*\x60?([^\x60\r\n]+?)\x60?\s*$",
        body,
    )
    return match.group(1).strip() if match else None


def inspect(fetcher: Callable[[int], dict] = fetch_comment) -> list[str]:
    findings: list[str] = []
    for comment_id in COMMENT_IDS:
        expected = EXPECTED[comment_id]
        try:
            record = fetcher(comment_id)
        except Exception as exc:  # fail closed on API errors or missing records
            findings.append(f"FAIL comment {comment_id}: unable to read record ({type(exc).__name__}: {exc})")
            continue

        if int(record.get("id", -1)) != comment_id:
            findings.append(f"FAIL comment {comment_id}: API returned a different comment id")
            continue

        body = record.get("body")
        if not isinstance(body, str) or not body:
            findings.append(f"FAIL comment {comment_id}: empty or missing body")
            continue

        assessor = field(body, "assessor")
        version = field(body, "assessed_version")
        baseline = field(body, "evidence_baseline")
        failed = False

        if not assessor:
            findings.append(f"FAIL comment {comment_id}: missing or empty assessor")
            failed = True
        elif expected["assessor_session"] not in assessor:
            findings.append(f"FAIL comment {comment_id}: assessor does not identify the recorded source session")
            failed = True

        if not version:
            findings.append(f"FAIL comment {comment_id}: missing or empty assessed_version")
            failed = True
        elif not SHA40.fullmatch(version):
            findings.append(f"FAIL comment {comment_id}: assessed_version must be a full 40-character hexadecimal commit")
            failed = True
        elif version.lower() != expected["assessed_version"]:
            findings.append(f"FAIL comment {comment_id}: assessed_version differs from the source report baseline")
            failed = True

        expected_baseline = f"main@{expected['assessed_version']}"
        if not baseline:
            findings.append(f"FAIL comment {comment_id}: missing or empty evidence_baseline")
            failed = True
        elif baseline != expected_baseline:
            findings.append(f"FAIL comment {comment_id}: evidence_baseline differs from the recorded source baseline")
            failed = True

        if not failed:
            findings.append(f"PASS comment {comment_id}: assessor, assessed_version, evidence_baseline")

    return findings


def main() -> int:
    results = inspect()
    for item in results:
        print(item)
    failures = sum(item.startswith("FAIL ") for item in results)
    print(f"SUMMARY comments={len(COMMENT_IDS)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
