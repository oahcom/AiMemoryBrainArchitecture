---
document_metadata:
  domain: ai-development
  role: work-record
  steward: user-authorized operator (delegated by account owner)
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
        - "AID-2026-301/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Provisional implementation evidence; exact-Head CI and independent review control acceptance."
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
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Session evidence for AID-2026-301"
    canonical_scope_id: "ai-development/aid-2026-301-session-evidence"
    canonical_scope_keywords:
      - "implementation-session"
      - "issue-1350"
      - "ci-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# Session evidence — AID-2026-301

## Session role / use case

Implementation session for Issue #1350. The task is to close the independently reviewed field-discovery gap in the committed-byte blob-pin checker, add fail-closed discovery for future digest-shaped declarations, and preserve the existing required Repository hygiene gate. This session is not the coordinator or independent reviewer.

## Actual AI input

The user supplied the implementation contract for #1350, the exact independent-review counterexample for AID-2026-001 top-level `prompt_sha256`, the missed AID-004 / AID-023 / AID-109 / AID-150 field shapes, the measured pre-change counters, and the requirements for negative controls, ratchet behavior, regression checks, PR metadata, and no merge before independent review.

## AI-visible output

The implementation adds a declarative field registry, explicit parsers for the supplied manifest shapes, top-level prompt-version path resolution, recursive fail-closed detection of unregistered digest-shaped fields, and isolated Git fixture tests. The implementation report and exact-head CI output are recorded in `evidence.md` and the PR description. This session does not claim independent review, Owner acceptance, merge, or CI success until those platform results are observed.
