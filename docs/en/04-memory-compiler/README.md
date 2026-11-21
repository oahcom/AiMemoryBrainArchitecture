---
document_metadata:
  domain: memory-compiler
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Owner semantic direction is recorded; cross-owner consumer contracts remain pending. GOV-DOC-001 remains PENDING until an authoritative artifact and exact version/Blob are adopted; the GOV-DOC-002 DM-12 source path is unresolved because no root source is authorized."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Candidate
    canonical_scope: null
    canonical_scope_id: memory-compiler/reading-guide
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Memory Compiler — Reading Guide

- Document ID: E-READING-GUIDE-001
- Version: 1.1
- Current-main baseline (pre-change): `0d0c1c6238e4e70a93609070b97fef596873916e`; source Blob: `5f50d470bf26d46dfffad48ad23059fc7a36c489`.
- Chinese counterpart: [Memory Compiler 阅读指南](../../zh-CN/04-memory-compiler/README.md)

## Available bilingual source specifications

1. [Compiler Overview](compiler-overview.md) — pipeline, boundaries, deterministic/model-assisted stages and safety invariants.
2. [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md) — durable acceptance, independent receipts, retry/replay and evidence boundaries.
3. [Compiler State and D Producer Admission](compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease identity, D registration, barrier and terminal disposition.
4. [Compiler Stage Contract](compiler-stage-contract.md) — the five-stage Rust reference pipeline; Provenance is cross-cutting, not a sixth stage.
   - Current-main bilingual source pins: EN Blob `6d733294232a93aa59123009d2a2801d9b83f459`; ZH-CN Blob `ad386cac5636b4ba3eaf8b93ad93afcb444e8b46` (main `0d0c1c6238e4e70a93609070b97fef596873916e`).

## Remaining core source specifications

The E branch inventory also contains Event Ingestion, Extraction/Normalization, Consolidation/Conflict Resolution, Evidence/Provenance, and Forget Fence/Derived Registration specifications. Their full bilingual companions remain pending and are tracked in [translation status](../../governance/translation-status.md).

## Architecture completion contract

The current [Compiler Overview](compiler-overview.md) §§20–28 records the Candidate IR / Canonical Schema boundary, five-stage topology, cross-cutting Provenance, D/I authority split and the #459 execution-lifecycle overlay with its in-memory recovery limits. Option A + I1 is DECIDED; B schema-freeze/consumer acceptance, D transaction/currentness/compatibility, I attestor/retention/Forget mapping and all cross-owner consumer contracts remain OPEN. The Runtime acceptance matrix is a plan only; Rust reference-crate unit tests do not constitute matrix or production integration evidence.

## Authority and status

E owns source ingestion/compilation orchestration, candidate generation, stage lineage, retries/replay and producer-side derivative evidence. D owns canonical identity/version/lifecycle and D-side Forget Fence semantics. I owns authorization/PermissionEpoch, revocation, retention and global Forget policy/completion. D/I authority checks jointly constrain protected publication. Storage/Consistency owns no semantics by default; its accountable implementation owner must be explicitly assigned.

CANDIDATE descriptions are not approved schemas. E emits neutral CandidateProposition/ExtractionIR only; it does not mint ClaimRef/ClaimRevisionRef/FactRef/FactRevisionRef or infer Fact from confidence. D owns canonical identity/revision/currentness/lifecycle and D ForgetFence; I owns authorization/PermissionEpoch, attestor authorization, retention and global Forget policy/completion. Exact B/D/I/H/Storage consumer contracts and transaction/compatibility evidence remain OPEN. No schema, DDL, public API, wire or Runtime freeze is authorized.

**Normative source/mirror status:** the EN and ZH-CN files are the maintained paired language mirrors under `docs/en` and `docs/zh-CN`. No root duplicate normative files are created. The historical root source paths are absent; GOV-DOC-001 remains PENDING until an authoritative artifact and exact version/Blob are adopted. GOV-DOC-002 DM-12 therefore remains blocked on an authorized source-path decision.
