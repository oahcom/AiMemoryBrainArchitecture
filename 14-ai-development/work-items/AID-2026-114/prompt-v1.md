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
      last_verification_note: "Assembled after the session from the ruling it worked to, not captured live. The digest below matches this file; nothing claims it matches the original instruction."
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

# AID-2026-114 prompt snapshot

**Provenance: assembled after the session, not captured live.** This file records the task as it was
handed to the implementing session: close the Session Evidence fail-open hole in which a pull request
body carrying no `AI-assisted work` field passed as `NOT_APPLICABLE`. `prompt_status` is
`RECORDED_NOT_FROZEN` and `executed_prompt_provenance` is `NOT_VERIFIED` for that reason.

## What the session was asked

Change `scripts/governance/session_evidence/validate.py` so that a PR body that omits
`AI-assisted work` fails. A body that declares `NO` with `N/A` references must still pass. A body that
declares `YES` must still supply a reference that exists in the PR head tree. Add a test for each of
those four cases. Do not relax any existing refusal, and do not mix this with any other change.

## What the session found

The brief named `_parse_status` as the hole. It is not one: `_parse_status` already raises
`missing AI-assisted work declaration` when the field is absent. The hole is the early return at
`validate.py:2195-2203`, which returned `_not_applicable_verdict` for a PR opened before
`AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC` whose linked Issues were all historical and whose body carried
neither field.

That early return is the #1026 ceiling. The comment above it said not to widen the exemption without a
test that pins the volunteering case. Closing the hole therefore inverts the two tests that pinned the
exemption instead of deleting them, and leaves every other check untouched.

## Measured effect

`#1275`, `#1266` and `#1220` passed the gate with no declaration field. `#1251` and `#1249` failed with
`YES` and a reference that did not resolve. After this change the first group fails; the second group's
failure mode is unchanged.
