---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-303/manifest.yaml"
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Session artifact; repository application and exact-head CI verification are pending."
    usage_status: Active
    modification_status: Active-Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "AI session evidence for AID-2026-303"
    canonical_scope_id: "ai-development/aid-2026-303-session-evidence"
    canonical_scope_keywords:
      - "issue-1267"
      - "issue-1462"
      - "implementation-session"
      - "source-revision-pointer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-303 — Session evidence

## Session role

Implementation specification and repository governance session for Issue #1267.

## Actual user input

The user supplied:

- The exact baseline commit.
- The measured source revision pointer scan.
- Eight stale pointer replacements.
- Six non-Blob pointer records, including four repairable records.
- The two guide records previously classified as `ORPHAN_MIRROR_PENDING_DECISION`.
- The owner adjudication that the guide source is
  `03-memory-brain/memory-brain-overview.md`.
- The requirement to preserve the former D branch labels as provenance.
- The decision to replace the ratchet integration with a direct hard gate,
  based on the worktree-baseline vulnerability demonstrated by Issue #1462.
- The requirement to remove the source-revision baseline and retain the
  existing workflow and required check context.
- The requirement not to modify scanner decision logic.

## AI-visible output

The assistant produced:

- The revised decision record rejecting the worktree-controlled ratchet.
- The two bilingual guide metadata replacement blocks.
- The root overview Blob ID verified at the specified base:
  `b991f61e412d5cf21824e3ca43b315c3af5f0b4b`.
- The workflow replacement step invoking the scanner directly.
- The deletion instructions for the old ratchet steps and baseline file.
- The revised manifest and this session evidence.
- The verification sequence and expected exit-code contracts.

## Scan-count accounting

The prior post-twelve-repair measurement was:

```text
POINTERS=52
ACCURATE=28
STALE=0
UNRESOLVED=0
DEREFERENCED=24
BAD_DEREFERENCE=0
NON_BLOB_REFERENCE=2
BAD=2
```

The two guide records are now intended to become valid Blob pointers. Under
the unchanged scanner, each such record adds one to POINTERS and one to
ACCURATE. The resulting arithmetic expectation is:

```text
POINTERS=54
ACCURATE=30
STALE=0
UNRESOLVED=0
DEREFERENCED=24
BAD_DEREFERENCE=0
NON_BLOB_REFERENCE=0
BAD=0
```

These are calculated expected counts, not a claim that this session executed
the scanner. The exact candidate-head run must record the actual output.

## Execution boundary

No repository file was written through this session.
No branch was created or updated.
No pull request was opened.
No local or remote CI command was executed.

The root overview Blob ID was independently read from the specified base
commit. The scanner source was inspected to verify its counting and
fail-closed exit behavior. The exact candidate scan and reachability run
remain pending.

## Provenance

Implementing AI session: ChatGPT GPT-6.

Issue references: #1267 and #1462.

Base commit: `7ecf2a8e7d1e40a13f6af6d4335a6766a222194f`.

Execution and acceptance status: PENDING.
