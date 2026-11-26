---
document_metadata:
  domain: memory-brain
  role: index
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Issue #1177"
        - "D bilingual reading-guide companion"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Candidate source index; semantic mirror review pending."
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
    canonical_scope_keywords: []
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
- Version: 1.1
- Chinese counterpart: [Memory Brain 阅读指南](../../zh-CN/03-memory-brain/README.md)

## Recommended reading order

1. [Memory Brain Overview](memory-brain-overview.md) — authority, scope and A–I boundaries.
2. [Canonical Memory Store](canonical-memory-store.md) — immutable versions, commit and outbox.
3. [Memory Lifecycle Manager](memory-lifecycle-manager.md) — lifecycle versus epistemic status and Forget operation.
4. [Forget Fence Operation and Publication Gate](forget-fence-operation-and-publication-gate.md) — operation-level linearization, race and JF-10/COC decisions.

## Canonical source set

The canonical source paths are in the repository root under [03-memory-brain](../../../03-memory-brain/README.md). The four source documents are restored in the Draft source-restoration PR as candidates. They remain `canonical_status: Candidate` and `normative_status: Informative` until D Owner acceptance, required dependency acceptance and Governance approval are recorded against their exact final Blobs. The English and Chinese files in this directory are reading companions, not canonical sources.

## Authority and status

D owns canonical memory identities/versions, lifecycle semantics, canonical cursor semantics, canonical Forget operation/fence and dependency/barrier evidence. D does not own global authorization, PermissionEpoch, global Forget completion, external-copy policy, physical erasure, BMCP wire, ContextVersion or Agent execution.

DECIDED statements in these guides are limited to D's domain authority. Cross-module implementation, Storage atomicity, I policy and runtime conformance remain OPEN unless explicit evidence says otherwise.

## Source revision discipline

The source pointers in each companion identify the exact current canonical-source Blob. The source body is pinned to the Owner-branch commit and original Blob recorded in GOV-DOC-002 metadata. Translation or restoration does not constitute Owner acceptance.
