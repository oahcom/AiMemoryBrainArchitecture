---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation record; validation and migration counts remain pending Actions evidence."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "AID-2026-252 steward adoption implementation evidence"
    canonical_scope_id: "ai-development/aid-2026-252-steward-adoption-evidence"
    canonical_scope_keywords:
      - "steward"
      - "metadata-schema"
      - "DM-15"
      - "DM-15b"
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-252 — Steward adoption evidence

## Authorized stewardship mapping

The selected value for the document-maintenance responsibility field is `steward: "Architecture Governance"`. The mapping is grounded in `00-governance/architecture-document-management-policy.md`, policy ownership row 49: `Owner: A — Principal Integration / Architecture Governance`. DM-15 defines steward as the maintenance-responsibility field, not an approval identity or document author. The 26 existing documents already using this value provide repository precedent.

This mapping is an explicit owner-authorized decision for this rollout. More granular domain-level stewardship may be proposed as a later, separately reviewed increment; this rollout does not infer or invent domain-specific owners.

## Implementation plan

- Make `steward` schema-required and include it in `required_fields()` through the schema-derived mechanism.
- Enforce DM-15 on newly added and modified governed documents. The existing DM-15 diagnostic wording is retained.
- Defer unchanged legacy omissions to DM-15b and the committed census, without excluding unclassified documents from the governed denominator.
- Add `--list-missing --json` output with pin, governed, classified, present, and exact missing paths.
- Capture the initial census from the GOV-DOC-002 Actions run and commit it at `14-ai-development/reports/steward-adoption-baseline.json`.
- Migrate work-item documents in batches of at most 25 changed files per Git tree/commit operation, updating the baseline in the same increment.

## Execution attribution

- Operator: user-authorized operator (delegated by account owner)
- Date: 2026-11-27
- Decision status: delegated implementation evidence; no natural-person Owner signature or acceptance is represented.

## Current evidence status

The branch contains the initial schema/checker/test/workflow mechanism commits. The exact census, baseline file, test run, Actions contexts, migration batches, PR merge, post-merge blob verification, and Issue #266 comment are pending direct readback and must not be represented as complete until observed.

## Addendum — migration and prompt snapshot integrity

- The AID-2026-001 through AID-2026-099 work-item slice has 127 steward additions across six bounded commits (25, 25, 25, 25, 25, and 2 files).
- The latest GOV-DOC-002 Actions census before prompt-pin reconciliation reported 526 classified documents missing steward, 1137 governed documents, 767 classified documents, and 370 unclassified documents.
- For modified prompt snapshots that are declared by work-item manifests, the corresponding SHA-256 and byte-count declarations have been refreshed in the affected manifests. This preserves the prompt-snapshot identity check rather than waiving it.
- The shrink-only manifest-blob-pins baseline reconciliation and final required-context verification remain pending direct Actions readback.

## R5 reconciliation — current main and gate evidence

- Latest merged main pin used for this census: 6482901cbc55e98d4a53f2203e6864b34a888b26
- Actions census after merging current main and adding the work-items index steward: governed=1144, classified=774, present=249, missing=525.
- The latest DM-15/GOV-DOC-002 lines are recorded by Architecture document management gate run 45966438510 (job 140396112780); changed-file validation succeeded.
- Cumulative steward assignments in this branch: 128 files (127 work-item files in AID-2026-001 through AID-2026-099 plus the modified work-items index).
- Repository hygiene was reconciled using its observed output: 76 stale manifest-blob-pin baseline entries removed and the one new AID-2026-059 prompt SHA mismatch corrected; no failure was added to the ratchet.
