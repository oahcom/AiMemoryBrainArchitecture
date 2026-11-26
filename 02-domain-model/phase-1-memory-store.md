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
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: DECIDED for the Phase 1 orchestration boundary). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: 502a342bb47ffd3b634c322383666a235bca3933."
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
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: "docs/en/02-domain-model/phase-1-memory-store.md"
    zh-CN: "docs/zh-CN/02-domain-model/phase-1-memory-store.md"
---
# Phase 1 Memory Store Facade

Status: DECIDED for the Phase 1 orchestration boundary; storage backend remains replaceable.

## Purpose

Provide the smallest application-level facade that composes the frozen Domain Model with the backend-neutral MemoryStorage port.

## Responsibilities

- validate Memory and MemoryVersion domain invariants before storage;
- require resolved Scope on every operation;
- preserve Memory identity and immutable MemoryVersion/revision semantics;
- enforce memory_id == revision.memory_id before commit;
- delegate CAS, idempotency and visibility enforcement to MemoryStorage;
- expose read-current, read-revision and idempotency resolution without owning persistence.

## Non-responsibilities

The facade does not define SQLite DDL, transactions, distributed consensus, physical Forget, permissions, indexing, embeddings, LLM behavior, or deployment topology.

## Revision boundary

Phase 1 treats MemoryVersion as the canonical immutable revision representation. `MemoryRevision` is an API alias only; it does not create a second persistence object.

## Scope boundary

Every facade operation requires a non-empty resolved Scope. Scope compatibility is necessary but is not permission grant; Storage/Governance remain authoritative for visibility and authorization.

## Idempotent write boundary

A revision write carries expected-current-version, idempotency key and request digest together. The facade rejects identity mismatches before Storage and delegates replay/conflict semantics to the Storage port.

## Acceptance

- create/read operations require valid Scope;
- revision identity mismatch is rejected before backend invocation;
- stale revision transitions are rejected by the domain/storage boundary;
- same idempotency key + same digest can resolve to the original receipt;
- different scopes do not become implicitly visible;
- no backend-specific dependency enters the facade.

## Next unit

After this minimal facade is stable, continue with higher-level Memory Store behaviors and application integration; do not add vector/graph/LLM dependencies.
