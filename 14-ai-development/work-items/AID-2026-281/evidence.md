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
        - "14-ai-development/work-items/AID-2026-281/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local Rust test evidence was supplied by the implementing machine. Independent review, Owner acceptance, GitHub Actions results and post-merge verification are not claimed."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "memory-read-authorization-boundary"
      - "complete-scope-read"
      - "canonical-memory-version"
      - "cross-scope-disclosure"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-281 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Branch:** `triage-20261127-p0-authz-read-boundary`  
**Base:** `main` at `a588cd99`  
**Issues:** #1128, #1129, #1136, #1138, #1139  
**Changed implementation path:** `crates/memory-storage-sqlite/src/lib.rs`

## Contract and decision

The SQLite adapter must not return a canonical `Memory` or `MemoryVersion` when the caller's requested Scope set does not cover every Scope stored on the parent Memory.

The selected policy is complete-Scope authorization for canonical reads:

1. Validate the requested Scope set.
2. Decode and validate the stored Scope set.
3. Require `scope_set_contains_all(requested, stored)`.
4. Return `StorageError::ScopeMismatch` when the caller does not cover every stored Scope.
5. When authorization succeeds, return the complete canonical stored object without filtering its Claims or changing its identity, digest, references or Scope membership.

A partial object is not returned under the canonical Memory or MemoryVersion identity. This avoids introducing a scope-specific projection whose identity, digest and downstream compatibility would need a separate contract.

The implementation adds `scope_allowed_complete()` and applies it to the SQLite MemoryVersion row read, `read_memory`, `read_current`, and `list_changes` paths. The in-place `version.claims.retain(...)` projection was removed. The existing write-side check remains: a commit whose Claim Scope is outside the commit caller's Scope set is rejected.

## Issue disposition

### #1128 — Filter aggregate MemoryVersion references for partial-Scope readers

**Disposition:** addressed by complete-Scope denial; intended to close with this PR.

The prior behavior could remove a hidden Claim while still returning aggregate entity, relation, source and provenance references and the full content digest. The new read policy returns no canonical MemoryVersion to a partial-Scope caller. It therefore withholds the entire aggregate object rather than trying to construct a partial object with potentially inconsistent references or digest.

Focused negative test:

- Test: `sqlite_partial_scope_cannot_read_hidden_claim_dependencies_or_digest`
- Command: `cargo test -p memory-storage-sqlite sqlite_partial_scope_cannot_read_hidden_claim_dependencies_or_digest`

Observed output:

