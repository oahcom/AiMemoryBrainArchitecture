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
      approval_scope: {type: Full-document}
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: ["14-ai-development/work-items/AID-2026-150/manifest.yaml"]
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "User-directed task snapshot; platform session identifier unavailable."
    usage_status: Active
    modification_status: Unchanged
    supersession: {supersedes: [], supersession_reason: null, effective_date: null}
    archival: {archived_date: null, archival_reason: null, archival_reference: null}
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-150 — Prompt snapshot v1

Restore exactly three D canonical source files from `session-d-memory-brain-2026-11-16`, preserving supplied source bodies and adding GOV-DOC-002 metadata only:

- `03-memory-brain/canonical-memory-store.md` — `6b37c91033fda21f072e2a3bde6f274663b1e76e`
- `03-memory-brain/commit-cursor-semantics.md` — `4688a0ca487bf4d853c7f0220408abe8d743d159`
- `03-memory-brain/forget-fence-operation-and-publication-gate.md` — `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`

Use account-fixed range AID-2026-150 through AID-2026-159. Select the first unused ID; do not allocate max+1 or use any number outside the range; stop if all ten are occupied.

Do not restore the other 57 source paths. Keep all 11 EN/ZH-CN orphan mirror pairs classified ORPHAN_MIRROR_PENDING_DECISION. Six existing language mirror files may receive GOV-DOC-002 metadata and minimum source-provenance corrections required by the bilingual gate; this does not adopt the cursor/Fence orphan pairs. Do not add any README.

Add 03-memory-brain to scripts/check_bilingual_docs.py NORMATIVE_ROOTS and 00-governance/document-scope-registry.yaml governed; do not alter checker logic.

Fence authority remains as in AID-2026-089: D sole logical authority; Storage projection only; no signer conflict; Owner acceptance pending; normative approval not claimed; implementation authorization not granted.

Run all 16 required checks. Merge only when all are green on the exact PR head and behind==0; refresh-to-merge within 1–2 minutes. Verify the three merged blobs and comment on #1212. Attribution is user-authorized delegated operator, not a natural-person Owner signature.
