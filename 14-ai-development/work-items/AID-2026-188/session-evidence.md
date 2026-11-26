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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Assembled after the fact from the pull request records it cites, not captured live. Every merge SHA, timestamp, check count and body field quoted below was read back from the repository, not recalled."
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

# Session role / use case

RECORDER -- register the historical Session Evidence coverage gap that two already-merged pull requests
passed through, as a dated record of gate behaviour rather than as a finding against either pull
request.

# Actual AI input

The actual prompt supplied to the AI:
Record the window in which the Session Evidence gate returned `NOT_APPLICABLE` for a pre-effective-time
pull request that carried no AI-assisted work declaration. Name #1275 and #1266 with head SHA, merge
SHA, check count and body field state. State that both were compliant under the gate then in force and
that PASS was the correct verdict. Do not accuse either pull request of a bypass. Do not edit either.

# AI-visible output

The actual output returned by the AI:

- Read both pull requests back from the repository rather than from the summary that named them.

  | | `#1275` | `#1266` |
  |---|---|---|
  | head | `3c5ed22e` | `6f1ad214` |
  | merge commit | `baca092b` | `4c8a3e1d` |
  | checks | 24, all green | 16, all green |
  | `Session Evidence` | SUCCESS | SUCCESS |
  | `AI-assisted work` field | absent | absent |
  | `Session evidence reference(s)` field | absent | absent |
  | linked Issues | `#1212`, `#1208`, `#1135` | `#1201` |
  | work item | `AID-2026-099` | `AID-2026-080` |

- Read the gate code that produced that verdict: `scripts/governance/session_evidence/validate.py`,
  early return at 2195-2203 on the tree of that period -- `pr_created < ctx.effective_at` and
  `_historical_not_applicable(ctx)` and both declaration fields absent, returning
  `_not_applicable_verdict(ctx)`. The verdict came from the code path, not from an operator choice, and
  neither pull request did anything to obtain it.
- Recorded that `#1266`'s own body already described the outcome accurately: its `Session Evidence`
  context "returns NOT_APPLICABLE on this branch, which is a genuine historical-path validation, not a
  bypass".
- Recorded the disposal: the exemption was removed by `#1287` (merge `17bfc43c`,
  `2026-11-26T13:41:46Z`; `validate.py` blob `c27b41cf`, in which the `pr_created` guard is gone and
  the declaration is required unconditionally). Re-running the current gate against either body now
  reports `MISSING: PR: missing AI-assisted work declaration`. Neither pull request is re-opened,
  re-labelled or edited, and no merged record is rewritten.

# Unavailable / not recorded

Both pull requests are merged, so no head-tree replay is possible for them any more: the head trees are
retained by the repository, but the `strict` freshness requirement no longer applies to them. The body
field state above is read from the stored pull request body, which is exactly what the gate read.
