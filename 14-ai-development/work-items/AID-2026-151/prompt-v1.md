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

# AID-2026-151 prompt snapshot

**Provenance: assembled after the fact, not captured live.** This file records the task as it was
handed to the recording session: register the historical Session Evidence coverage gap that `#1275`
and `#1266` passed through, as a record of what the gate did at the time rather than as a finding
against either pull request. `prompt_status` is `RECORDED_NOT_FROZEN` and
`executed_prompt_provenance` is `NOT_VERIFIED` for that reason.

## What the session was asked

Write a work record for the window between the Session Evidence gate's effective time
(`AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC`) and the removal of the `#1026` exemption, in which a pull
request opened before the effective time, linked only to Issues older than that time, and carrying no
`AI-assisted work` declaration returned `NOT_APPLICABLE` with exit 0.

The record must:

- name the two pull requests that passed through the window, with head SHA, merge SHA, check count and
  the body field state that produced the `NOT_APPLICABLE` verdict;
- state plainly that under the gate then in force both pull requests were compliant and PASS was the
  correct verdict -- neither bypassed the gate, and neither is accused of anything;
- say what a merged record can and cannot be changed to after the fact, and what happens to the same
  two bodies now that the exemption is gone.

## What the session was told not to do

- Not to claim that a merged pull request violated the rules in force at its merge time.
- Not to describe either pull request as having bypassed, evaded or disabled a check.
- Not to re-open, re-label, re-close or edit either pull request.
- Not to touch `scripts/check_bilingual_docs.py` (its `NORMATIVE_ROOTS` belong to the bilingual-root
  work) and not to move the workflow's effective-time literal.
- Not to touch `#1220`.
