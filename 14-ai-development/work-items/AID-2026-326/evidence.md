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
- Canonical source updated with section 15; new source blob: `025b00bbbd253882ee019a834f817ece772ca59d`.
- English mirror updated and pinned to the new canonical source blob; mirror blob: `855f549691d5176a4f353c1630c848b684bd7160`.
- Chinese mirror updated and pinned to the new canonical source blob; mirror blob: `33b83f60f0c8a6fa763214e5e558a2b06b9c0a5a`.
- The canonical source's approval remains Draft and evidence verification remains Unverified. No formal document approval is claimed.
- No code, API, schema, DDL, test, workflow, branch-protection, Issue-body, or runtime change is included.

## Follow-up boundary

The Owner decision does not define the serialized representation of a multi-shard transaction's cursor-entry set or the consistent snapshot/cut protocol for F/G consumers. Those remain explicit follow-up contract work. The existing D/F detailed documents still contain older global-cursor wording and must be reconciled under separately scoped work after this decision record is reviewed.

## Exact-head CI evidence (2026-11-28)

- PR: #1475, draft, head `e1a8604749c9c6d25d6eb4412a39a38703c1ef3e`, base `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`.
- Successful exact-head checks: Repository hygiene (run 46085829070), Architecture document management (46085829066), Session Evidence Gate (46085829094), Bilingual documentation gate (46085829097), Rust Phase 1 workspace tests (46085829038), plus Rust clippy/format/doctests, BMCP conformance, BMCP protocol index, schema non-empty audit, manifest schema and runner admission within Existing gates run 46085829108.
- Failed check: Prompt-to-commit trace (job 140795033528, run 46085829108). No other check failed at this exact head.
- Direct source inspection of `scripts/ci/check_prompt_commit_trace.py`: `ratchet_violations()` lines 214–235 requires every Work Item absent from the base manifest set to be `TRACEABLE` (lines 219–224). AID-2026-326 is newly introduced on this PR branch and has no merged implementation commit. The workflow log says it seeds a baseline for the new Work Item's current `NO_TRACE` state, but that seed does not change the base-manifest membership test. The PR cannot truthfully claim a merge commit before merge; no false `implementation_commit_sha` or `merge_commit_sha` has been added.
- Disposition: **BLOCKED by the pre-merge prompt-to-commit ratchet contract** pending an authorized CI contract/exception decision. PR remains draft and unmerged. No code or CI workflow was modified. Independent exact-head review remains unassigned.
