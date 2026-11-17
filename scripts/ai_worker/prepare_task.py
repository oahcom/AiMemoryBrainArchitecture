#!/usr/bin/env python3
"""Validate and normalize a trusted, bounded AI development issue."""
from __future__ import annotations
import json
import pathlib
import re
import sys

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)

if len(sys.argv) != 3:
    fail("usage: prepare_task.py ISSUE_JSON OUTPUT_JSON")
source = pathlib.Path(sys.argv[1])
target = pathlib.Path(sys.argv[2])
try:
    issue = json.loads(source.read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"cannot parse issue JSON: {exc}")

if "pull_request" in issue:
    fail("pull requests are not eligible work items")
if issue.get("state") != "open":
    fail("issue must be open")
labels = {str(x.get("name", "")).strip().lower() for x in issue.get("labels", [])}
if "ai:ready" not in labels:
    fail("issue must carry ai:ready label")
owners = sorted(x for x in labels if re.fullmatch(r"owner:[a-i]", x))
risks = sorted(x for x in labels if x in {"risk:r0", "risk:r1"})
classes = sorted(x for x in labels if x in {"work:doc", "work:arch"})
if len(owners) != 1:
    fail("exactly one owner:A..I label is required")
if len(risks) != 1:
    fail("exactly one risk:R0 or risk:R1 label is required")
if len(classes) != 1:
    fail("exactly one work:DOC or work:ARCH label is required")
body = issue.get("body") or ""
for heading in ("## Objective", "## Acceptance Criteria", "## Non-goals"):
    if heading.lower() not in body.lower():
        fail(f"issue body must contain heading: {heading}")
if len(body) > 20000:
    fail("issue body exceeds 20,000 characters")
normalized = {
    "schema_version": 1,
    "issue_number": int(issue["number"]),
    "title": str(issue.get("title", ""))[:300],
    "url": str(issue.get("html_url", "")),
    "owner": owners[0].split(":", 1)[1].upper(),
    "risk": risks[0].split(":", 1)[1].upper(),
    "work_class": classes[0].split(":", 1)[1].upper(),
    "body": body,
    "labels": sorted(labels),
}
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Eligible issue #{normalized['issue_number']}: owner={normalized['owner']} class={normalized['work_class']} risk={normalized['risk']}")
