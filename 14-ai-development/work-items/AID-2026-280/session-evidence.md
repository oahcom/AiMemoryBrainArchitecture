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
        - "14-ai-development/work-items/AID-2026-280/manifest.yaml"
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records actual AI input/output and GitHub API-only actions; no local execution claimed."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "session-evidence"
      - "req-04"
      - "ac8"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Session evidence — AID-2026-280

## Session role / use case

Cross-workflow conflict adjudication session S8. The task was to independently inspect the AC8 EXIT-1/EXIT-2 source carriers, determine the operative evidence state, and prepare an auditable decision record. This is a proxy adjudication, not a natural-person Owner signature.

## Actual AI input

The user supplied the complete task brief in this conversation, including:
- repository and expected main pin;
- mandatory F1–F9 facts and the demand to independently verify F1–F4;
- questions Q1–Q6 and mandatory A/B/C ruling;
- AID-2026-280 as the recommended reserved work-item number;
- API-only execution constraints, cache-busting reads, required metadata format, required PR body fields, merge rules, and attribution requirements.

The AI additionally discovered and fetched Issue #305 after reading AID-260. That source says a session cannot constitute its own delegation or appointment instrument. This new primary-source constraint materially affects the authority assessment.

## AI-visible output

The AI fetched Issue #265, comment #7193586920, comment #7209840981, AID-2026-260/scope-confirmation.md, AID-2026-254/manifest.yaml, AID-2026-254/evidence.md, INDEX.md, Issue #305, and the main ref through cache-busted GitHub API URLs. It confirmed that main had advanced to 756e1e25d735f526254fc3241b47880fef527b24, that AID-2026-280 was absent (404), and that the explicit AC8 exclusion is at AID-260 scope-confirmation.md:69, blob e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a.

The AI selected ruling B: AC8 remains in scope because the canonical Issue body still lists it and the AID-260 proxy scope record is not an effective delegation act under Issue #305; AID-2026-254 is a fan-out proxy and does not satisfy direct attention/context-switching measurement. No local git, shell, or script execution was performed.
