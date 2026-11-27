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
        - "14-ai-development/work-items/AID-2026-113/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Execution prompt snapshot for AID-2026-113; not an approved architecture specification."
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
    canonical_scope_keywords:
      - "aid-2026-113"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-113 — Execution prompt snapshot

Restore the five F Memory Runtime Canonical roots from `session-f-memory-runtime` byte-for-byte, adding only GOV-DOC-002 frontmatter. The five files are activation-policy-engine.md, retrieval-engine.md, runtime-overview.md, runtime-scheduling.md, and working-set-and-cache.md.

Do not create README.md. Owner ruling designates `05-memory-runtime/runtime-overview.md` as the explicit replacement for the never-existing `05-memory-runtime/README.md`. Record `source_hierarchy_decision: OWNER_REPLACEMENT`, `replaces: 05-memory-runtime/README.md`, and the delegated authority exactly as stated in manifest/evidence. The runtime-overview frontmatter must include `designated_root: true` and `retrieval_semantics_acceptance: F_ACCEPTS_RETRIEVAL_SEMANTICS`.

Add GOV-DOC-002 metadata only to the five EN/ZH-CN mirror pairs that have Canonical sources: activation-policy-engine, retrieval-engine, runtime-overview, runtime-scheduling, working-set-and-cache. Preserve every mirror body byte-for-byte. The `memory-runtime-guide.md` orphan pair remains `ORPHAN_MIRROR_PENDING_DECISION` and is left entirely untouched because no Canonical source exists for the required three-way linkage; do not create or promote a Canonical guide.

Do not restore the ten source-branch historical records; classify them as `HISTORICAL_PHASE_RECORD`. Register 05-memory-runtime as a governed root in the scope registry and bilingual NORMATIVE_ROOTS, since the Canonical root is being restored.

Allocate the AID identifier at push time by re-reading main and INDEX. Run all 16 required checks; merge only when all are green. Verify merged blob identities and comment on #1212.
