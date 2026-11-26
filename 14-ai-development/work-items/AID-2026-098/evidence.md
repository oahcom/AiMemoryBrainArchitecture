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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-098/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Repository reads and document drafting only. No physical backend, crash, power-loss, restore or production conformance test was executed."
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
    canonical_scope: "AID-2026-098 registration and execution evidence"
    canonical_scope_id: "ai-development/aid-2026-098-evidence"
    canonical_scope_keywords:
      - storage-consistency
      - registration
      - evidence
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-098 — Evidence and registration record

Attribution: user-authorized operator (delegated by account owner), 2026-11-26. Proxy registration only: 代理登记，非自然人 Owner 签署.

## Baseline and allocation

- Repository: `oahcom/AiMemoryBrainArchitecture`.
- Exact main baseline read before branch creation: `d5107f68a7f1b61f5f2f7352fadf828aae06cf1c`.
- Work item ID: `AID-2026-098`, `id_status: PROVISIONAL`.
- Observed INDEX maximum at baseline: AID-2026-096.
- AID-2026-097 is reserved for E/F mirror work by the account-owner instruction and was not reused.
- Branch: `docs/2026-11-26-storage-physical-consistency-098`.
- The ID must be rechecked against current main/INDEX/Issues/PRs/branches before any merge; renumber if occupied and preserve `RENUMBERED_FROM`.

## Carrier

- Draft PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1276.
- Branch: `docs/2026-11-26-storage-physical-consistency-098`.
- Initial PR head at creation: `c9f08ba9bf244ad0a92d840af9fd9cd1a419b478` (subsequent evidence/index updates may advance the head; CI must be read against the final head).

## Source evidence reviewed

- `14-ai-development/work-items/AID-2026-095/manifest.yaml` and `evidence.md`: F8 is BLOCKED_WITH_REASON; nine original checkpoints are not evidenced.
- `00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md` §F8: Storage trait is candidate-only; backend atomicity, crash recovery, serialization, multiprocess concurrency and durability are not proven.
- `02-domain-model/phase-1-storage-trait-contract.md`: one recoverable commit boundary is specified for immutable version, current-version CAS, idempotency and canonical commit sequence; trait explicitly excludes backend proof.
- `01-system-architecture/forget-fence-and-completion-contract.md` and AID-2026-089 / PR #1232: D is the sole logical Forget Fence authority; Storage rows are derived rebuildable projections.
- `14-ai-development/work-items/AID-2026-089/manifest.yaml`: AID-2026-089 merged, Owner acceptance remains pending.
- Issue #1211: full Storage/Consistency normative source set remains absent and historical COC/JF-10 proposals remain unratified.
- Issue #1212: A–I + Storage end-to-end composition review remains open.
- Issue #1125: historical/current issue text describes the dual-fence problem; it remains open.
- Issue #1180: G delivery-state projection remains unresolved; G owns delivery intent/projection and Applied authority, while Storage supplies durable persistence only.

## Critical implementation discrepancy

The current-main `crates/memory-storage-sqlite/src/lib.rs` defines a `canonical_forget_fences` table and local `next_fence_sequence` allocation. The current-main `crates/memory-event-store-sqlite/src/forget_fence.rs` defines a separate namespace-keyed `forget_fence` table and `next_seq`. These source observations are incompatible with the AID-2026-089 direction if interpreted as independent logical authorities. This Work Item does not edit code or resolve the runtime ownership/migration. The candidate requires a D-derived projection and explicitly classifies physical conformance as unproven.

## Checkpoint accounting

- Total: 18.
- DOCUMENTED_ONLY: 10 (candidate clause completeness only).
- EVIDENCE_REQUIRED: 8 (SC-04, SC-05, SC-06, SC-10, SC-12, SC-13, SC-17, SC-18); current result FAIL / NOT EVIDENCED.
- No checkpoint result closes Gate A. No Owner acceptance is claimed.

## Known documentation-gate compatibility issue

The required canonical path introduces top-level numbered root `10-storage-consistency/`. Current `scripts/check_bilingual_docs.py` has a literal `NORMATIVE_ROOTS` set that does not include this root; `scripts/check_bilingual_docs_full.py` derives numbered roots from the filesystem and fails when the sets differ. The root was absent from the baseline tree. The user explicitly prohibited validator changes, so this PR does not modify either validator. The bilingual root-set check is therefore expected to fail until the repository's validator-owner process authorizes and lands a separate root-registration change. This is not silently treated as a green CI result.

## Limitations

- No runtime/validator/schema/test/workflow file was changed.
- No crash/fault-injection, multiprocess, WAL power-loss, replica, backup/restore or production test was run.
- No backend was selected; COC/JF-10, anti-rollback anchor, RPO/RTO and production topology remain open.
- No natural-person Owner signature or exact-version Owner acceptance was recorded.
- No merge, Issue closure, implementation or deployment is authorized.
- Implementing session identity is NOT_RECORDED; no identifier is invented.
