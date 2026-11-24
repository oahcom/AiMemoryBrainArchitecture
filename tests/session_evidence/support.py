"""Offline fixtures and helpers for the Session Evidence Gate."""

import base64
import hashlib

from scripts.governance.session_evidence import validate


REPOSITORY = "oahcom/AiMemoryBrainArchitecture"
HEAD_SHA = "a" * 40
EFFECTIVE_AT = "2099-01-01T00:00:00Z"
EVIDENCE_A = "14-ai-development/work-items/AID-2026-001/evidence/session-a.md"
EVIDENCE_B = "14-ai-development/work-items/AID-2026-001/evidence/session-b.md"
PROMPT_A = "14-ai-development/work-items/AID-2026-001/evidence/prompt-a.md"
PROMPT_B = "14-ai-development/work-items/AID-2026-001/evidence/prompt-b.md"
MANIFEST = "14-ai-development/work-items/AID-2026-001/manifest.yaml"

PROMPT_BYTES_A = b"actual prompt input A\n"
PROMPT_BYTES_B = b"actual prompt input B\n"

ISSUE_BODY_YES = f"""## AI-assisted work

YES

## Session evidence reference(s)

{EVIDENCE_A}
"""

ISSUE_BODY_NO = """## AI-assisted work

NO

## Session evidence reference(s)

N/A
"""

ISSUE_BODY_UNDECLARED = """## Work description

Historical work item.
"""

EVIDENCE_TEXT_A = """# Session role / use case

IMPLEMENTER — repository implementation.

# Actual AI input

The actual prompt supplied to the AI:
Review the implementation requirements and produce the requested work.

# AI-visible output

The actual output returned by the AI:
The implementation was completed and the validation results were reported.

# Unavailable / not recorded

No hidden reasoning or platform-internal payload is retained.
"""

EVIDENCE_TEXT_B = """# Session role / use case

REVIEWER — independent validation.

# Actual AI input

The actual prompt supplied to the AI:
Review the supplied evidence and report validation findings.

# AI-visible output

The actual output returned by the AI:
The review identified the tested conditions and reported the results.

# Unavailable / not recorded

No platform-internal payload is retained.
"""


def issue_url(number):
    return f"https://github.com/{REPOSITORY}/issues/{number}"


def make_manifest(entries):
    lines = ["session_evidence:"]
    for entry in entries:
        lines.append(f"  - role: {entry['role']}")
        lines.append("    issue_refs:")
        for ref in entry["issue_refs"]:
            lines.append(f'      - "{ref}"')
        for key in (
            "implementing_ai_session",
            "executed_prompt_snapshot_file",
            "executed_prompt_sha256",
            "executed_prompt_bytes",
            "executed_prompt_provenance",
            "session_reference_status",
            "session_evidence_ref",
        ):
            value = entry[key]
            if isinstance(value, int):
                lines.append(f"    {key}: {value}")
            else:
                lines.append(f'    {key}: "{value}"')
    return "\n".join(lines) + "\n"


def make_entry(number, suffix="a"):
    prompt = PROMPT_BYTES_A if suffix == "a" else PROMPT_BYTES_B
    return {
        "role": "IMPLEMENTER" if suffix == "a" else "REVIEWER",
        "issue_refs": [issue_url(number)],
        "implementing_ai_session": f"session-{suffix}",
        "executed_prompt_snapshot_file": PROMPT_A if suffix == "a" else PROMPT_B,
        "executed_prompt_sha256": hashlib.sha256(prompt).hexdigest(),
        "executed_prompt_bytes": len(prompt),
        "executed_prompt_provenance": "VERIFIED",
        "session_reference_status": "RECORDED",
        "session_evidence_ref": EVIDENCE_A if suffix == "a" else EVIDENCE_B,
    }


def make_pr_body(
    number=101,
    status="YES",
    refs=None,
    issue_status="YES",
    issue_refs=None,
    related=None,
):
    refs = refs if refs is not None else [EVIDENCE_A]
    issue_refs = issue_refs if issue_refs is not None else refs
    related = related if related is not None else [number]

    overall_refs = "\n".join(refs) if refs else "N/A"
    row_refs = "\n".join(issue_refs) if issue_refs else "N/A"
    related_text = ", ".join(f"#{item}" for item in related)

    return f"""## Work Item

AID-2026-001

## Owning Issue

{related_text}

## Related issue(s)

{related_text}

## AI-assisted work

{status}

## Session evidence reference(s)

{overall_refs}

## Per-Issue AI session evidence

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(number)} | {issue_status} | {row_refs} |
"""


def make_blob(path, content, mode="100644", kind="blob"):
    raw = content if isinstance(content, bytes) else content.encode("utf-8")
    return {
        "path": path,
        "mode": mode,
        "type": kind,
        "sha": hashlib.sha1(
            b"blob " + str(len(raw)).encode() + b"\0" + raw
        ).hexdigest(),
        "size": len(raw),
        "_raw": raw,
    }


def make_valid_world(
    number=101,
    entries=None,
    issue_created="2031-01-01T00:00:00Z",
    issue_body=None,
    pr_body=None,
    extra_tree=None,
):
    entries = entries if entries is not None else [make_entry(number)]
    issue_body = issue_body if issue_body is not None else ISSUE_BODY_YES
    refs = [entry["session_evidence_ref"] for entry in entries]

    if pr_body is None:
        pr_body = make_pr_body(
            number=number,
            refs=refs,
            issue_refs=refs,
        )

    manifest = make_manifest(entries)
    blobs = [
        make_blob(MANIFEST, manifest),
        make_blob(EVIDENCE_A, EVIDENCE_TEXT_A),
        make_blob(EVIDENCE_B, EVIDENCE_TEXT_B),
        make_blob(PROMPT_A, PROMPT_BYTES_A),
        make_blob(PROMPT_B, PROMPT_BYTES_B),
    ]

    if extra_tree:
        blobs.extend(extra_tree)

    tree = [
        {key: value for key, value in item.items() if key != "_raw"}
        for item in blobs
    ]
    raw_by_sha = {item["sha"]: item["_raw"] for item in blobs}
    text_by_sha = {
        item["sha"]: item["_raw"].decode("utf-8", errors="strict")
        for item in blobs
        if item["path"] != PROMPT_A and item["path"] != PROMPT_B
    }

    pr = {
        "number": number,
        "body": pr_body,
        "head": {
            "sha": HEAD_SHA,
            "repo": {"full_name": REPOSITORY},
        },
    }
    issue = {
        "number": number,
        "html_url": issue_url(number),
        "created_at": issue_created,
        "body": issue_body,
    }

    def fake_api(path):
        if path == f"/repos/{REPOSITORY}/pulls/{number}":
            return pr
        if path == f"/repos/{REPOSITORY}/issues/{number}":
            return issue
        if "/git/blobs/" in path:
            sha = path.rsplit("/", 1)[-1]
            if sha not in raw_by_sha:
                raise validate.ValidationError(f"Unknown fake blob {sha}")
            return {
                "encoding": "base64",
                "content": base64.b64encode(raw_by_sha[sha]).decode("ascii"),
            }
        raise validate.ValidationError(f"Unexpected fake API path: {path}")

    def fake_tree(repo, sha):
        assert repo == REPOSITORY
        assert sha == HEAD_SHA
        return tree

    def fake_blob_text(repo, sha, path):
        assert repo == REPOSITORY
        if sha not in text_by_sha:
            raise validate.ValidationError(f"Text blob unavailable: {path}")
        return text_by_sha[sha]

    return {
        "api": fake_api,
        "tree": fake_tree,
        "blob_text": fake_blob_text,
        "pr": pr,
        "issue": issue,
        "git_tree": tree,
        "raw_by_sha": raw_by_sha,
        "blobs": blobs,
        "entries": entries,
        "manifest": manifest,
    }
