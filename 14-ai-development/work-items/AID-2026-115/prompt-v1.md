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
        - "14-ai-development/work-items/AID-2026-115/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Prompt snapshot records the user-directed scope; platform prompt and session identifiers are unavailable."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-115-PROMPT v1 — Gate Dispatch Deduplication and Rust Cache

## Identity
- Work Item: AID-2026-115; Issue: #1212
- Repository: oahcom/AiMemoryBrainArchitecture; baseline: 8722a37b0cd72dc550d99c0eaebe9e7556ce2f95
- Role: user-authorized operator (delegated by account owner)
- Prompt status: RECORDED_NOT_FROZEN; platform session identifiers NOT_RECORDED.

## Objective
Add head-SHA-scoped concurrency to all eight required workflows; add Swatinem/rust-cache@v2 to clippy, fmt, doctest and Rust Phase 1 tests with distinct shared keys and a key containing Cargo.lock hash plus resolved toolchain version; explicitly name audit and rust-workspace-test while preserving protected context names; create Canonical/EN/ZH-CN evidence.

## Authority and scope
Authorized: branch, implement, PR to main, verify 16 contexts, merge only after all SUCCESS, read back merged blobs, comment on #1212.
Forbidden: merge jobs; change fetch-depth; change gate/checker semantics; alter protected contexts or branch protection; close #1212; modify runtime, schema, API, database or deployment.

## Required sequence
1. Re-read main and allocate the next collision-free AID at push time.
2. Add the exact concurrency group using github.workflow and PR head SHA (github.sha fallback), never github.ref.
3. Confirm existing stable toolchain setup, record resolved rustc version, then cache with job-specific shared-key and Cargo.lock/toolchain key.
4. Add explicit job names audit and rust-workspace-test matching the protected names.
5. Add complete GOV-DOC-002 metadata to Canonical/EN/ZH-CN evidence; update INDEX/session evidence.
6. Verify exact-head CI; all 16 must be SUCCESS before merge.
7. Read back main blobs and comment on #1212 with measured/estimated performance and cache-hit observation.

## Acceptance
Eight workflows changed; four Rust caches isolated; two explicit context names; no job merges/fetch-depth/checker changes; all 16 exact-head contexts green; merge SHA and post-merge blob SHAs recorded; #1212 stays open.

## Verification
Record exact branch/base/head/merge SHAs, changed paths, all 16 check conclusions and run links, cache-hit evidence or NOT YET MEASURED, post-merge blob SHAs and comment ID. Missing, pending, skipped or failed required checks are not PASS.
