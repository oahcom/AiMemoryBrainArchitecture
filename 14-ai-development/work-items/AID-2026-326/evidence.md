---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-326/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Evidence records the repository observations available to this session; independent review and CI acceptance remain pending."
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
    canonical_scope: "Records the Owner D-10 decision source, base-tree observations, and documentation-only branch changes for AID-2026-326."
    canonical_scope_id: "ai-development/aid-2026-326-evidence"
    canonical_scope_keywords:
      - "AID-2026-326"
      - "d10-cursor-authority"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Evidence — AID-2026-326

## Decision authority

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`
- Base commit: `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`
- Final Owner decision: [Issue #1210, comment 7174534633](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1210#issuecomment-7174534633), dated 2026-11-27.
- The decision is recorded as final. This Work Item records it; it does not reopen the decision.

## Decision recorded

1. One deployment has one logical Brain authority. Tenant and shard are partition boundaries within that authority.
2. `CanonicalCommitCursor` is partitioned per tenant/shard. There is no total order across shards.
3. A cross-shard transaction produces one cursor entry per participating shard and is atomic all-or-none.
4. Authority identity and epoch/incarnation are explicit. Cursors from different authorities are not comparable.
5. Aggregate revisions and lifecycle cursors remain separate cursor domains.
6. `ForgetFence`, `ProducerRegistrationHighWater`, and similar fences are per-authority and carry authority identity so a fence from one shard cannot be interpreted as covering another.

## Base-tree evidence

At base commit `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`:

- Canonical `01-system-architecture/system-boundaries.md` was blob `bf20b204688bf51a1df76968db7e52ee0dd597c1` and ended at section 14; it had no canonical commit-cursor authority section.
- `03-memory-brain/commit-cursor-semantics.md` (blob `2c68161d039310b8df0e1387b4f1111ed74699db`) and `03-memory-brain/canonical-memory-store.md` (blob `2e10e23f651f1f6cb03247f01727f2b7ff5342f1`) still described a per-Brain-authority global commit order.
- `05-memory-runtime/retrieval-engine.md` (blob `38fb72395166b52d8c1b0380757110ecc508cc05`) still described a global per-authority sequence and a scalar `IndexWatermark.applied_through`.
- `05-memory-runtime/runtime-overview.md` (blob `80879fd3ed23b2f4545e186b8bd3626c80960c70`) remained Informative/Candidate. These D/F/G consumer documents are deliberately not changed by this Work Item.

## Branch result

- Branch: `docs/aid-2026-326-d10-cursor-authority`
- Canonical source updated with section 15; new source blob: `dc0e15e7f872dbbebc64545f92b398ef15700786`.
- English mirror updated and pinned to the new canonical source blob; mirror blob: `b3957b2e7af10e47ff25a10ff9efa27f1737eaf5`.
- Chinese mirror updated and pinned to the new canonical source blob; mirror blob: `14d7b34f428c3479a7f90de5e3039e7d036cb94d`.
- The canonical source's approval remains Draft and evidence verification remains Unverified. No formal document approval is claimed.
- No code, API, schema, DDL, test, workflow, branch-protection, Issue-body, or runtime change is included.

## Follow-up boundary

The Owner decision does not define the serialized representation of a multi-shard transaction's cursor-entry set or the consistent snapshot/cut protocol for F/G consumers. Those remain explicit follow-up contract work. The existing D/F detailed documents still contain older global-cursor wording and must be reconciled under separately scoped work after this decision record is reviewed.
