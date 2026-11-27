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
        - "14-ai-development/work-items/AID-2026-291/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Actions execution and post-merge blob verification pending."
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
    canonical_scope: "Incremental evidence for correcting the AID-2026-291 prompt-to-commit ratchet addition baseline."
    canonical_scope_id: "ai-development/aid-2026-291-ratchet-base-fix"
    canonical_scope_keywords:
      - "AID-2026-291"
      - "prompt-to-commit trace"
      - "ratchet base inventory"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-291 — Ratchet base-fix evidence

- Date: 2026-11-27
- Attribution: user-authorized operator (delegated by account owner)
- Scope: incremental repair to the already-merged AID-2026-291; no new work-item directory is created.

## Defect and correction

The committed baseline is a state-regression reference, not a complete inventory of manifests on the current PR base. The candidate manifest set is compared with the manifest inventory generated from the exact `--base` commit:

1. A manifest absent from the `--base` inventory is new and must be `TRACEABLE`.
2. A manifest present at `--base` is not new, even if it is absent from the older committed baseline.
3. For a manifest present in the committed baseline, the candidate primary state may not worsen and its findings may not grow.
4. A manifest removed from the candidate tree is not iterated and does not create a ratchet violation.

No manifest is added to an exemption list. No historical prompt pin or traceability claim is fabricated. The existing `TRACEABLE=0` inventory result is not altered.

## Regression coverage

The unit tests assert:
- `manifest present at base but absent from committed baseline → NOT new`;
- `manifest removed from main → no violation`;
- a genuinely new non-`TRACEABLE` manifest remains a hard ratchet failure.

The workflow reuses the generated `main-baseline.json` for the PR's exact base. It also reproduces the historical #1453 case using head `bdb4b0d4` and base `460f437e`, reading the committed baseline from the historical base tree and generating the base inventory from that same commit.

## Verification record

Pending GitHub Actions execution:
- PR's own `Prompt-to-commit trace (ratchet)` check: PENDING
- Historical #1453 reproduction: PENDING
- Required contexts (16/16): PENDING
- behind=0: PENDING
- Merge commit SHA: PENDING
- Post-merge per-file blob verification: PENDING

No validation output is represented here as executed before Actions reports it.
