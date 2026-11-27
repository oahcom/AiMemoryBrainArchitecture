---
document_metadata:
  domain: memory-brain
  role: index
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
        - "03-memory-brain/README.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Bilingual mirror of a candidate root restored by AID-2026-100; content acceptance and semantic parity review remain pending."
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
    canonical_scope: "Bilingual mirror of 03-memory-brain/README.md"
    canonical_scope_id: "mirror/03-memory-brain/README"
    canonical_scope_keywords:
      - mirror
      - candidate
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/README.md"
    en: null
    zh-CN: "docs/zh-CN/03-memory-brain/README.md"
---

# Memory Brain — Reading Guide

- Document ID: D-READING-GUIDE-001
- Version: 1.0
- Chinese counterpart: [Memory Brain 阅读指南](../../zh-CN/03-memory-brain/README.md)

## Recommended reading order

1. [Memory Brain Overview](memory-brain-overview.md) — authority, scope and A–I boundaries.
2. [Canonical Memory Store](canonical-memory-store.md) — immutable versions, commit and outbox.
3. [Memory Lifecycle Manager](memory-lifecycle-manager.md) — lifecycle versus epistemic status and Forget operation.
4. [Entity and Relationship Manager](entity-and-relationship-manager.md) — identity, typed relations and merge/split history.
5. [Memory Versioning](memory-versioning.md) — revisions, temporal queries and concurrency.
6. [Canonical Commit and Cursor Semantics](commit-cursor-semantics.md) — distinct cursor namespaces.
7. [Forget Fence and Completion Contract](forget-fence-and-completion-contract.md) — D-owned suppression and proof boundary.
8. [Forget Fence Operation and Publication Gate](forget-fence-operation-and-publication-gate.md) — operation-level linearization, race and JF-10/COC decisions.

## Authority and status

D owns canonical memory identities/versions, lifecycle semantics, canonical cursor semantics, canonical Forget operation/fence and dependency/barrier evidence. D does not own global authorization, PermissionEpoch, global Forget completion, external-copy policy, physical erasure, BMCP wire, ContextVersion or Agent execution.

DECIDED statements in these guides are limited to D's domain authority. Cross-module implementation, Storage atomicity, I policy and runtime conformance remain OPEN unless explicit evidence says otherwise.

## Source revision discipline

Each document records the exact Owner branch and source blob SHA. Re-query the D branch before using these companions as an implementation baseline. A translated document does not merge or approve the source branch.
