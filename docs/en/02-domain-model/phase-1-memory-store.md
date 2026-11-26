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
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a mirror that carried no front-matter: records domain, role, status and the canonical source path only (basis, the document's own statement: Status: DECIDED for the Phase 1 orchestration boundary). Claims no canonical authority and does not verify semantic parity with the source. Pre-metadata content blob: f53182e183e5a571fc6c1cc9a9472e3872e124e2."
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
    source: "02-domain-model/phase-1-memory-store.md"
    en: null
    zh-CN: "docs/zh-CN/02-domain-model/phase-1-memory-store.md"
---
# Phase 1 Memory Store Facade

Status: DECIDED for the Phase 1 orchestration boundary; the storage backend remains replaceable.

## Purpose
Provide the smallest application-level facade composing the frozen Domain Model with the backend-neutral MemoryStorage port.

## Responsibilities
- validate Memory and MemoryVersion invariants before storage;
- require resolved Scope for every operation;
- preserve stable Memory identity and immutable MemoryVersion semantics;
- reject memory_id != revision.memory_id before commit;
- delegate CAS, idempotency and visibility enforcement to MemoryStorage;
- expose current/revision reads and idempotency resolution without owning persistence.

## Non-responsibilities
No SQLite DDL, distributed consensus, physical Forget, permission policy, indexing, embeddings, LLM behavior, or deployment topology.

## Revision boundary
MemoryVersion is the canonical immutable revision representation. MemoryRevision is an API alias only and is not a second persistence object.

## Scope boundary
Every facade operation requires a non-empty resolved Scope. Scope compatibility is not a permission grant.

## Idempotent write boundary
A revision write carries expected-current-version, idempotency key and request digest together. Identity mismatches are rejected before Storage; replay/conflict semantics are delegated to Storage.

## Acceptance
Create/read require valid Scope; revision identity mismatch fails before backend invocation; stale transitions are rejected; same key + same digest can resolve to the original receipt; different scopes are not implicitly visible; no backend-specific dependency enters the facade.

## Next unit
After this minimal facade is stable, continue with higher-level Memory Store behaviors and application integration. Do not add vector/graph/LLM dependencies.
