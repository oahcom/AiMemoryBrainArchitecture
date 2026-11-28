---
document_metadata:
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
        - "14-ai-development/work-items/AID-2026-284/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured snapshot, not a byte-for-byte transcript; prompt provenance is NOT_VERIFIED."
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
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Structured prompt snapshot for AID-2026-284"
    canonical_scope_id: "ai-development/aid-2026-284-prompt"
    canonical_scope_keywords:
      - "req-04"
      - "aid-2026-284"
      - "prompt-snapshot"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-284 — REQ-04 AC1 scope confirmation

## Role
Act as the delegated documentation operator for repository oahcom/AiMemoryBrainArchitecture. Record the bounded REQ-04 scope statement without impersonating a natural-person Owner.

## Objective
Create one auditable work-item carrier that supersedes the ineffective AC8 exclusion in AID-2026-260 while preserving AC8 as in scope and ABSENT. Do not modify AID-2026-260, Issue #265's body, unrelated work items, code, tests, workflows, or branch protection.

## Authoritative inputs
- Base: main at cbdaf78313404fc24a6c250dc06faa72d4d0b97c.
- AID-2026-260 scope-confirmation blob: e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a.
- AID-2026-280 decision blob: 3cde57f77fa9c93a702eaab0f3164f27c70c4573.
- Governance policy: 00-governance/architecture-document-management-policy.md.
- Issue #265 and Issue #305 comment 7042461592 are GitHub-hosted facts; preserve their API read references and do not claim they are offline-recomputable.

## Authority and constraints
- Attribution: user-authorized operator (delegated by account owner).
- Decision character: 代理裁决，非自然人 Owner 签署.
- Approval remains Under-Review; approver remains null; verification remains Unverified.
- AID-2026-260 is immutable in this task. Do not write superseded_by into it.
- Do not PATCH Issue #265. After merge, add exactly one comment only.
- Exactly one PR for AID-2026-284. Do not create a second carrier.
- Use only six paths: this work item's manifest.yaml, scope-confirmation.md, evidence.md, session-evidence.md, prompt-v1.md, and work-items/INDEX.md with exactly one appended AID-2026-284 row.
- Do not mark AC1 or AC9 passed. Keep AC2/AC5/AC7 SATISFIED and AC3/AC4/AC6 PARTIAL without expanding their completion.
- Copy the specified AC8 disposition verbatim into scope-confirmation.md.

## Required outcome
Record AC8 as in scope, not excluded, not satisfied, status ABSENT, direct-measurement carrier NO_CARRIER_FOUND. Retain AID-2026-254 as optional out-of-scope proxy observation only. AC9 remains NOT YET JUDGEABLE and follows: merge this carrier, disposition AC3/AC4/AC6 residuals, then Owner records AC9.

## Verification and reporting
Record source blob identities, exact source line locations, reproducible git/API read commands, and the distinction between offline-recomputable repository blobs and GitHub Issue/comment facts. Preserve the prompt snapshot's actual byte count and SHA-256 in the manifest.