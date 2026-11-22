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
      last_verification_note: "Owner authorized this root source/mirror topology in PR #429 comment 7061562608; content acceptance, bilingual semantic parity, independent review and CI remain pending."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Memory Compiler reading guide"
    canonical_scope_id: memory-compiler/reading-guide
    canonical_scope_keywords: []
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/README.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/README.md"
---

# Memory Compiler — Reading Guide

- Document ID: E-READING-GUIDE-001
- Version: 1.2
- Stage A frozen-snapshot base: `c58878fce24528a0842b4f8887c93ddbf465b566`; source Blob: `5f50d470bf26d46dfffad48ad23059fc7a36c489`.
- Canonical root reading-guide source: [`04-memory-compiler/README.md`](../../../04-memory-compiler/README.md); source Blob: `414c6c6fd95fbc36829445e3e2dc3f4795af07fc`. This is its Non-Canonical English mirror.

## Available bilingual source specifications

1. [Compiler Overview](compiler-overview.md) — pipeline, boundaries, deterministic/model-assisted stages and safety invariants.
2. [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md) — durable acceptance, independent receipts, retry/replay and evidence boundaries.
3. [Compiler State and D Producer Admission](compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease identity, D registration, barrier and terminal disposition.
4. [Compiler Stage Contract](compiler-stage-contract.md) — the five-stage Rust reference pipeline; Provenance is cross-cutting, not a sixth stage.
   - Frozen-base bilingual source pins: EN Blob `6d733294232a93aa59123009d2a2801d9b83f459`; ZH-CN Blob `ad386cac5636b4ba3eaf8b93ad93afcb444e8b46` (main `c58878fce24528a0842b4f8887c93ddbf465b566`).

## Remaining core source specifications

The E branch inventory also contains Event Ingestion, Extraction/Normalization, Consolidation/Conflict Resolution, Evidence/Provenance, and Forget Fence/Derived Registration specifications. Their full bilingual companions remain pending and are tracked in [translation status](../../governance/translation-status.md).

## Architecture completion contract

The current [Compiler Overview](compiler-overview.md) §§20–28 records the Candidate IR / Canonical Schema boundary, five-stage topology, cross-cutting Provenance, D/I authority split and the #459 execution-lifecycle overlay with its in-memory recovery limits. Option A + I1 is DECIDED; B schema-freeze/consumer acceptance, D transaction/currentness/compatibility, I attestor/retention/Forget mapping and all cross-owner consumer contracts remain OPEN. The Runtime acceptance matrix is a plan only; Rust reference-crate unit tests do not constitute matrix or production integration evidence.

## Authority and status

E owns source ingestion/compilation orchestration, candidate generation, stage lineage, retries/replay and producer-side derivative evidence. D owns canonical identity/version/lifecycle and D-side Forget Fence semantics. I owns authorization/PermissionEpoch, revocation, retention and global Forget policy/completion. D/I authority checks jointly constrain protected publication. Storage/Consistency owns no semantics by default; its accountable implementation owner must be explicitly assigned.

CANDIDATE descriptions are not approved schemas. E emits neutral CandidateProposition/ExtractionIR only; it does not mint ClaimRef/ClaimRevisionRef/FactRef/FactRevisionRef or infer Fact from confidence. D owns canonical identity/revision/currentness/lifecycle and D ForgetFence; I owns authorization/PermissionEpoch, attestor authorization, retention and global Forget policy/completion. Exact B/D/I/H/Storage consumer contracts and transaction/compatibility evidence remain OPEN. No schema, DDL, public API, wire or Runtime freeze is authorized.

**Source/mirror status:** this is the Non-Canonical English mirror of the Informative / Canonical root reading guide `04-memory-compiler/README.md` for scope `memory-compiler/reading-guide`; the ZH-CN file is its Non-Canonical sibling language mirror. The normative specifications have separate canonical root sources.
