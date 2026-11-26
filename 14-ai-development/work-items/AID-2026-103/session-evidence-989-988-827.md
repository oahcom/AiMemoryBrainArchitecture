---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count in this file was produced by the commands quoted, in the session that wrote it, on the commits named. The concurrency table is two runs of six processes on one commit with only the fixture lines changed; the binding table is five mutations, each restored and its sha256 checked."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session evidence — #989, #988, #827 AC-A

This session produced three rulings on the linked issues and the test-only branch this pull
request carries. It ran from an issue ruling, not from a recorded prompt snapshot, so there is no
`prompt-v1.md` and no prompt SHA-256 to state.

## Session role / use case

`TEST_AUTHOR` and `OWNER_RULING`. The session measured three defects in
`scripts/test_check_document_management.py`, posted a ruling on each, then wrote the tests and the
fixture-ownership fix the rulings called for. The same session did both, which is why the pull
request declares `Independent reviewer: NONE`.

## Actual AI input

NOT_RECORDED

The conversation was not captured to a file while it ran. What the session was given, in order:

- an instruction to continue work on the repository's open issues;
- the issue bodies of #989, #988 and #827, read through the GitHub API in this session;
- the seven existing comments on #989, the six on #988 and the twenty on #827, also read in this
  session, which carry the earlier rulings this one corrects.

The rulings quote the measurements taken here, and every quoted number can be re-derived from the
commands recorded in the ruling comments. The input text itself — the conversation transcript — was
obtainable and was not saved. That is `NOT_RECORDED`, not `NOT_AVAILABLE`.

## AI-visible output

The session's output is three issue comments and one branch. All four are retrievable, and the
comments are the primary record because they were written at the time:

| what | where |
|---|---|
| #989 ruling | issue comment `7184097261` |
| #988 ruling | issue comment `7184110940` |
| #827 AC-A ruling | issue comment `7184611981` |
| the change | branch `fix/989-fixture-ownership-988-827-cases`, commit `4517c159` |

The measurements those comments state, reproduced here so this file is not merely a pointer:

```
# baseline, main = 8d84c16e, six fixtures unmodified
$ grep -c 'Path(tmp).parent' scripts/test_check_document_management.py
6

# 6 concurrent runs, one shared TMPDIR, no mutation applied
318/318  318/318  317/318  316/318  316/318  316/318      -> 4 of 6 red

# same commit, only the fixture lines changed
324/324 x6, rc=0 x6, no outside-* residue

# serial, three times, after the change
324/324  324/324  324/324
```

Five emitters were each confirmed unbound by deleting them (suite stayed `319/319`), then bound;
deleting each bound site afterwards turned exactly its own case red (`323/324`, no collateral).
`#988`'s enum-on-kind branch turned out to be bound already, by `T63`'s "neither kind nor fields"
case, so that part of the issue is corrected rather than implemented.

## What this file does not establish

It does not establish that the rulings are correct, that the measurements were taken by any
particular model, or that the change is good. It establishes that this session existed, what it
claimed to run, and where the claims are recorded. The verdict on the change is the review's, and
no review has been performed.
