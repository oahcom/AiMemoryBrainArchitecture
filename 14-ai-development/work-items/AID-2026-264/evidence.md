---
document_metadata:
  domain: ai-development
  role: work-record
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
        - "14-ai-development/work-items/AID-2026-264/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local gate output is quoted verbatim below. CI verdicts for the new head are NOT_VERIFIED: the API quota was exhausted, so no run was read back."
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
    canonical_scope_keywords:
      - "merge-authorization"
      - "pr-1325"
      - "evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-264

## 1. What this work item produced

The governance record `OA-MERGE-2026-11-27-1325` at
`00-governance/decisions/2026-11-27-merge-authorization-pr-1325.md`, with English and Chinese
mirrors, plus the registration that lets PR #1393's Session Evidence gate resolve its declared
evidence reference to a manifest entry.

The record states, in its own text, that it is published by a delegated operator, that `oahcom`
is the publishing identity only, and that no natural-person signature exists. That sentence is
the point of the artifact: the previous attempt at this authorization was missing exactly this
repository-internal, attributable record.

## 2. Commits

| Commit | Message | Content |
|---|---|---|
| `9fbaa09ac6d38f3148302ad40474528c2202f3c6` | `docs(gov): record delegated merge authorization for PR #1325` | the three record files |
| `25b1ec6ebf88af22887f9631ee1e7e7078ea901c` | `docs(gov): correct the API-channel note in OA-MERGE-2026-11-27-1325` | replaces the record's "quota exhausted" claim with "measurement not repeated", recomputes all three body hashes |
| merge commit | `Merge remote-tracking branch 'origin/main' into governance/2026-11-27-merge-authorization-1325` | plain merge, no rebase, no force push |

The correction commit exists because the record asserted something the same session then
disproved: the API was not exhausted at publication time, and the pull request was created. The
claim was fixed in place rather than left standing, and the three `approved_version` content
hashes were recomputed in the same commit because DM-10 binds them to the body.

## 3. Local gate results (verbatim key lines)

```
GOV-DOC-002: 1035 governed documents, 664 classified, 371 unclassified
PASS (incremental): no GOV-DOC-002 violations; 664 classified, 371 unclassified

bilingual baseline: 77 frozen, 0 new gaps
Bilingual documentation and prompt-library gate: PASS (3 changed paths inspected).

Line-ending check: 1748 files inspected, 0 binary skipped, 0 violations.

Repository new-file admission passed: 3 new path(s) checked.

FMT_RESULT=PASS
CHECK_RESULT=PASS

PASS TRACEABILITY: 0 requirements / 113 work items / 0 errors / 108 warnings
```

Full log: `D:\code\_aimb\round\govrec-gates.log`.

## 4. Known gaps

1. **Independent review of the record: NOT_RECORDED.** The record was written and published by
   one session under one account. Its own text requires review evidence independent of the
   authoring session for PR #1325; it does not claim to have such evidence for itself.
2. **CI verdicts for this work item's head: NOT_VERIFIED.** The GitHub API quota was exhausted
   (`core_remaining=0`) before the new head could be read back, so no run set is cited here. A
   green local gate is not a CI verdict.
3. **`issue_refs` is empty by necessity, not by preference.** The Session Evidence validator
   rejects any `issue_refs` value that is not a linked Issue in the PR body, and this pull
   request links no Issue. Naming one to fill the field would have been an unverifiable claim,
   so the entry is PR-scoped, which OD-A3 permits.
4. **PR #1325's technical state was not re-measured.** Every value in the record's section 4 is
   the earlier W1 measurement. The record says so; this evidence file repeats it rather than
   upgrading it.
5. **The `Branch freshness vs base` context.** The branch was brought forward with a plain merge
   of `origin/main`; `main` moved again during the session. Whether the context is green on the
   pushed head is NOT_VERIFIED for the same quota reason as item 2.
