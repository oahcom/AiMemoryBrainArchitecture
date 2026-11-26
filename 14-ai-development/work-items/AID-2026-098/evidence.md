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

## Per-Issue AI session evidence

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| #1211 | LEGACY_UNDECLARED | N/A |
| #1212 | LEGACY_UNDECLARED | N/A |
| #1125 | LEGACY_UNDECLARED | N/A |
| #1180 | LEGACY_UNDECLARED | N/A |

## Known documentation-gate compatibility issue

The required canonical path introduces top-level numbered root `10-storage-consistency/`. This root is now explicitly registered as governed in `00-governance/document-scope-registry.yaml`. Current `scripts/check_bilingual_docs.py` still has a literal `NORMATIVE_ROOTS` set that does not include this root; `scripts/check_bilingual_docs_full.py` derives numbered roots from the filesystem and fails when the sets differ. GOV-DOC-002 therefore also reports the declared/enforced root-set mismatch and cannot classify the canonical source for mirror parity. The root was absent from the baseline tree. The user explicitly prohibited validator changes, so this PR does not modify either validator. The bilingual root-set check is therefore expected to fail until the repository's validator-owner process authorizes and lands a separate root-registration change. This is not silently treated as a green CI result.

## Limitations

- No runtime/validator/schema/test/workflow file was changed.
- No crash/fault-injection, multiprocess, WAL power-loss, replica, backup/restore or production test was run.
- No backend was selected; COC/JF-10, anti-rollback anchor, RPO/RTO and production topology remain open.
- No natural-person Owner signature or exact-version Owner acceptance was recorded.
- No merge, Issue closure, implementation or deployment is authorized.
- Implementing session identity is NOT_RECORDED; no identifier is invented.


## Session role / use case

Documentation author for the Storage/Consistency physical contract candidate. The work was limited to repository inspection, drafting bilingual candidate documents, Work Item registration, a draft PR and two Issue comments. No runtime or validator code was changed.

## Actual AI input

The exact user task is preserved in `14-ai-development/work-items/AID-2026-098/prompt-v1.md`. It requested the Storage physical contract candidate, 3 language/source documents, AID-2026-098 provisional registration, a Draft PR, comments on #1212 and #1180, and explicitly prohibited runtime/validator changes, merge and Issue closure.

## AI-visible output

- Read the repository baseline at `d5107f68a7f1b61f5f2f7352fadf828aae06cf1c`, including AID-2026-095 F8, AID-2026-089 and the Forget Fence contract, Storage trait, relevant implementation files, GOV-DOC-002 schema/policy, bilingual gate source and related Issues.
- Created initial branch `docs/2026-11-26-storage-physical-consistency-098` and Draft PR #1276; because main advanced, this candidate is being re-based onto the current main in a successor Draft PR.
- Added Canonical, EN and ZH-CN candidate contract documents; 18 checkpoints total (10 DOCUMENTED_ONLY, 8 EVIDENCE_REQUIRED).
- Registered AID-2026-098 as PROVISIONAL and added its INDEX row. AID-2026-097 remains reserved as instructed.
- Added `10-storage-consistency` to `00-governance/document-scope-registry.yaml` and aligned the existing `NORMATIVE_ROOTS` scope set to include the same governed root. This changes only the declared scan scope; checker logic and validator semantics are unchanged.
- Posted comment #7187485412 on #1212 and comment #7187486337 on #1180; both Issues remained OPEN at readback.
- Current PR Head at the time of this evidence update is tracked by the PR API; no claim of exact-Head CI success is made.
- Forget Fence check: the candidate preserves D as sole logical authority under AID-2026-089 and flags current-main local Fence sequence code as a discrepancy requiring separate implementation disposition.
- No merge, Issue closure, runtime change, validator change, deployment or production conformance claim.

## Session identity limitation

The exact ChatGPT session identifier was not exposed in the available execution context and is recorded as `NOT_RECORDED`. The prompt snapshot provenance is `NOT_VERIFIED`; the recorded SHA-256 and byte count bind the committed snapshot bytes, not the external origin of the prompt.


## Follow-up: implementation drift and governance scope repair

- Issue #1211 implementation-drift finding posted: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1211#issuecomment-7188271324. It distinguishes the document-layer tension from implementation behavior that remains unverified; assigns D, Storage and I the minimum call-graph, projection-rebuild and anti-rollback evidence.
- CI scope repair: `10-storage-consistency` is listed in both the governed roots registry and the pre-existing `NORMATIVE_ROOTS`. No check predicate, validation rule or runtime code was changed.
- Current-main rebase baseline: `fa8268fef659891efcdab9164f3e7703e19975c0`. Successor Draft PR #1283 is open on `docs/2026-11-26-storage-physical-consistency-098-rebased`; previous PR #1276 remains an earlier Draft carrier.
