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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Unverified"
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
    canonical_scope: "Prompt snapshot for bounded D Memory Brain normative-root restoration"
    canonical_scope_id: "ai-development/aid-2026-150-prompt"
    canonical_scope_keywords:
      - "aid-2026-150"
      - "memory-brain"
      - "restore"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# AID-2026-150 — Prompt snapshot v1

Restore exactly these three D normative roots from source branch `session-d-memory-brain-2026-11-16`:

1. `03-memory-brain/canonical-memory-store.md` — source blob `6b37c91033fda21f072e2a3bde6f274663b1e76e`
2. `03-memory-brain/commit-cursor-semantics.md` — source blob `4688a0ca487bf4d853c7f0220408abe8d743d159`
3. `03-memory-brain/forget-fence-operation-and-publication-gate.md` — source blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`

Use the account-fixed identifier range `AID-2026-150..AID-2026-159`; assign 150 if free, otherwise advance only within this range. Never allocate by INDEX max+1 and never leave the range.

Preserve each source body byte-for-byte. Add only valid GOV-DOC-002 metadata. For Canonical Memory Store and Commit Cursor Semantics, retain the existing EN/ZH-CN mirrors, add metadata and three-way counterpart links without changing their bodies. The existing Fence stub and split Parts 1–4 are not equivalent to the complete source blob: restore the full source at the root path, do not concatenate or overwrite the split family, and classify all 11 unmatched mirror pairs as `ORPHAN_MIRROR_PENDING_DECISION`.

Do not restore any of the other 57 D source paths. Preserve the exact AID-2026-107 §10.4 classifications: 29 `HISTORICAL_PHASE_RECORD`, 28 `UNDECIDED`; include every path and source blob SHA in evidence. Do not create or modify any README.

Add `03-memory-brain` to the authoritative bilingual `NORMATIVE_ROOTS` set. Update the work-item INDEX row. Produce canonical, EN and ZH-CN restoration evidence and a manifest/session record. Do not modify runtime implementation, validators, schemas, tests, workflows, deployment or production.

Run the repository's required CI. All 16 required contexts must succeed on the exact final PR Head. With strict branch protection, verify `behind == 0`; if the base advanced, refresh the branch, wait for green checks, then merge immediately within 1–2 minutes with the exact expected head SHA. Do not insert unrelated operations between final refresh/green verification and merge.

After merge, verify the three root bodies and final blob SHAs on main, then post a factual comment to Issue #1212. Do not close or reopen #1212. Do not claim Owner approval, independent review, implementation conformance or production readiness.

Attribution: user-authorized operator (delegated by account owner); no natural-person Owner signature or session identifier is to be fabricated.
