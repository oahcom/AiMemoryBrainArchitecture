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

1. One deployment has one logical Brain authority; tenant and shard are partition boundaries within that authority, not separate authorities.
2. `CanonicalCommitCursor` is partitioned per tenant/shard. There is no total order across tenants or shards. A globally ordered cursor across tenants is rejected because it would require a global serialization point or distributed consensus not specified by this architecture.
3. Cursor entries are ordered only within their own tenant/shard partition.
4. Authority identity and epoch/incarnation are explicit parts of cursor identity. Rollover is an epoch change. Cursors from different authorities or epochs are not comparable; comparison across them is an error, never a numeric ordering.
5. A cross-shard transaction produces one cursor entry per participating shard, ordered within each shard. The transaction is atomic all-or-none; atomicity does not imply a cross-shard total order, and no API may imply one.
6. Aggregate revisions and lifecycle cursors remain separate domains.
7. `ForgetFence`, `ProducerRegistrationHighWater`, and similar fences are per-authority and carry authority identity plus applicable target/partition scope so a fence from one shard cannot be read as covering another.
8. Required negative cases: `cursor_comparison_across_authority_rejected` and `cross_shard_commit_exposes_no_total_order`.

## Base-tree evidence

At base commit `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`:

- Canonical `01-system-architecture/system-boundaries.md` was blob `bf20b204688bf51a1df76968db7e52ee0dd597c1` and ended at section 14; it had no canonical commit-cursor authority section.
- `03-memory-brain/commit-cursor-semantics.md` (blob `2c68161d039310b8df0e1387b4f1111ed74699db`) and `03-memory-brain/canonical-memory-store.md` (blob `2e10e23f651f1f6cb03247f01727f2b7ff5342f1`) still described a per-Brain-authority global commit order.
- `05-memory-runtime/retrieval-engine.md` (blob `38fb72395166b52d8c1b0380757110ecc508cc05`) still described a global per-authority sequence and a scalar `IndexWatermark.applied_through`.
- `05-memory-runtime/runtime-overview.md` (blob `80879fd3ed23b2f4545e186b8bd3626c80960c70`) remained Informative/Candidate. These D/F/G consumer documents are deliberately not changed by this Work Item.

## Branch result

- Branch: `docs/aid-2026-326-d10-cursor-authority`
- Canonical source updated with section 15; new source blob: `42b2411048b53ebe6c7947075427665cdfb2d30c`.
- English mirror updated and pinned to the new canonical source blob; mirror blob: `ea8e291a2b25d2c2dd9dd4456ceba5ea3d237e69`.
- Chinese mirror updated and pinned to the new canonical source blob; mirror blob: `65432c147ef3ee991a19f822849f6064fd12c2e3`.
- The canonical source's approval remains Draft and evidence verification remains Unverified. No formal document approval is claimed.
- No code, API, schema, DDL, test, workflow, branch-protection, Issue-body, or runtime change is included.

## Follow-up boundary

The Owner decision does not define the serialized representation of a multi-shard transaction's cursor-entry set or the consistent snapshot/cut protocol for F/G consumers. Those remain explicit follow-up contract work. The existing D/F detailed documents still contain older global-cursor wording and must be reconciled under separately scoped work after this decision record is reviewed.

## Prompt-to-implementation trace pins

The Work Item manifest now records the prompt and implementation ancestry inputs consumed by `scripts/ci/check_prompt_commit_trace.py`:

- `prompt_file`: `14-ai-development/work-items/AID-2026-326/prompt-v1.md`
- `prompt_sha256`: `228d7d3d9b22dd6a4908b00583378c55a3bde03f7962f7fabe03a16c771a1c09`
- `prompt_file_blob_sha`: `9721457bf64f03929abf8153dcc214d8e4f55755`
- `prompt_file_commit_sha`: `15fe58287566d3b7370499b2b0837b5a43ebcb38` (verified to contain that exact prompt blob)
- `implementation_commit_sha`: `1c208822c880b2666395e6a199fdee236f830341` (verified to contain the complete canonical + EN + ZH-CN D-10 decision record)
- `implementation.merge_commit_sha`: `3595ce6ed3b45287a59a7658ad0a38b2797267fb`, explicitly typed as `PR_HEAD_TRACE_TARGET_NOT_MERGED`. This is a branch commit used only as the checker's ancestry target; it is not an actual merge commit and does not claim that PR #1475 is merged.
- GitHub’s unmerged test-merge commit for the preceding candidate head was `7d985e1560d3c91e31757abed015f2f2076b1680`; it is retained as provenance only and is not used as the checker target because the workflow checkout fetches branch heads/tags, not pull-request merge refs.

These pins make the implementation commit reachable from a verifiable PR-head target while preserving the unmerged status. The checker’s exact semantics are ancestry-based; no source code or workflow was changed. The GitHub Actions checkout log for the prior run shows a fetch refspec limited to `refs/heads/*` and `refs/tags/*`; therefore the GitHub synthetic test-merge commit is not assumed to be locally resolvable in that job. The PR-head trace target is explicitly labeled as unmerged. The manifest/prompt pins were added after the prior exact-head CI run, so their final CI outcome remains unverified until a run on the new head completes.

## Exact-head CI evidence (2026-11-28)

- PR: #1475, draft, head `e1a8604749c9c6d25d6eb4412a39a38703c1ef3e`, base `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`.
- Successful exact-head checks: Repository hygiene (run 46085829070), Architecture document management (46085829066), Session Evidence Gate (46085829094), Bilingual documentation gate (46085829097), Rust Phase 1 workspace tests (46085829038), plus Rust clippy/format/doctests, BMCP conformance, BMCP protocol index, schema non-empty audit, manifest schema and runner admission within Existing gates run 46085829108.
- Failed check: Prompt-to-commit trace (job 140795033528, run 46085829108). No other check failed at this exact head.
- Direct source inspection of `scripts/ci/check_prompt_commit_trace.py`: `ratchet_violations()` lines 214–235 requires every Work Item absent from the base manifest set to be `TRACEABLE` (lines 219–224). The prior run at head `e1a8604749c9c6d25d6eb4412a39a38703c1ef3e` predated the top-level prompt and implementation pins and therefore failed with the new item untraceable. The manifest now includes verified prompt digest/blob/commit pins, an implementation commit, and a clearly labeled pre-merge PR-head ancestry target. No actual merge is claimed; the GitHub test-merge SHA is recorded separately and not used as the checker target.
- Disposition: **TRACE PINS ADDED — CURRENT-HEAD CI NOT YET VERIFIED**. PR remains draft and unmerged. No code or CI workflow was modified. Independent exact-head review remains unassigned.
