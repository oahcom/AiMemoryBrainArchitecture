---
document_metadata:
  domain: domain-model
  role: design-specification
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
        - "14-ai-development/work-items/AID-2026-193/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a mirror that carried no front-matter: records domain, role, status and the canonical source path only (basis, the document's own statement: Status: CANDIDATE implementation seam; no backend is selected). Claims no canonical authority and does not verify semantic parity with the source. Pre-metadata content blob: 8ccce8ecee41ee46e5a38693eb0126b3e7aad08b."
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "02-domain-model/phase-1-storage-trait-contract.md"
    en: null
    zh-CN: "docs/zh-CN/02-domain-model/phase-1-storage-trait-contract.md"
---
# Phase 1 Storage Trait Contract

Status: CANDIDATE implementation seam; no backend is selected.

## Purpose

Define the backend-neutral application port between the pure memory-domain crate and future persistent implementations.

## Operations

- create_memory (with resolved scope)
- read_current
- read_version
- commit_version
- list_changes
- resolve_idempotency

## Commit boundary

A backend implementation MUST treat the immutable version, current-version CAS, idempotency record and canonical commit sequence as one recoverable commit boundary. This trait does not prescribe SQLite DDL or a distributed transaction protocol.

## Safety

Every read/write receives resolved scope, including create_memory. A backend MUST authorize Scope before resolving an idempotency receipt and MUST reject memory_id != new_version.memory_id. A backend MUST NOT use a stale projection as canonical state. `expected_current_version` is an optimistic-concurrency guard.

## Idempotency

The same idempotency key and request digest may return the original receipt. The same key with a different digest MUST return `IdempotencyConflict`.

## Explicit non-goals

No SQLite adapter, Event Store, Memory Store facade, network transport, vector/graph index, physical Forget implementation, or production durability claim is included.

## Verification boundary

The crate contains pure Rust contract-shape tests only. They do not prove backend atomicity, crash recovery, serialization, concurrency across processes, or durability.

> This English document is the normative counterpart of `docs/zh-CN/02-domain-model/phase-1-storage-trait-contract.md`.

<!-- BILINGUAL-MANIFEST: paired counterpart verified in this PR; semantic content unchanged. -->
