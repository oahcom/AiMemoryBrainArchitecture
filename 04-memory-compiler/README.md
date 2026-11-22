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
      last_verification_note: "Source/mirror topology was authorized by PR #429 comment 7061562608; the later Owner decision in Issue #564 comment 7074302216 keeps this reading guide Informative / Non-Canonical. Content acceptance, bilingual semantic parity, independent review and CI remain pending."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Memory Compiler reading guide"
    canonical_scope_id: memory-compiler/reading-guide
    canonical_scope_keywords:
      - reading-guide
      - orientation
      - navigation
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/README.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/README.md"
---

# Memory Compiler — Reading Guide

- Document ID: E-READING-GUIDE-001
- Version: 1.2
- Root reading-guide source restored from historical root Blob `6f235483aec156dce744846ddd2595ee96ba621c` (commit `7494d218`) and reconciled with the accepted #429 guide; batch-base EN mirror Blob `5f50d470bf26d46dfffad48ad23059fc7a36c489`; ZH-CN mirror Blob `1ce0146bfd4acfccc7c2747a5b1eaf6440002725`.
- Stage A frozen-snapshot validation base: `c58878fce24528a0842b4f8887c93ddbf465b566`.
- Chinese mirror: [Memory Compiler 阅读指南](../docs/zh-CN/04-memory-compiler/README.md).

## Available bilingual source specifications

1. [Compiler Overview](compiler-overview.md) — pipeline, boundaries, deterministic/model-assisted stages and safety invariants.
2. [Accepted Receipt and Idempotency Contract](../docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md) — durable acceptance, independent receipts, retry/replay and evidence boundaries.
3. [Compiler State and D Producer Admission](../docs/en/04-memory-compiler/compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease identity, D registration, barrier and terminal disposition.
4. [Compiler Stage Contract](../docs/en/04-memory-compiler/compiler-stage-contract.md) — the five-stage Rust reference pipeline; Provenance is cross-cutting, not a sixth stage.
   - Current-main bilingual source pins: EN Blob `6d733294232a93aa59123009d2a2801d9b83f459`; ZH-CN Blob `ad386cac5636b4ba3eaf8b93ad93afcb444e8b46` (main `d647e7d5eff0049fd6b223908f27d674b6c9f5f1`).

## Remaining core source specifications

The E branch inventory also contains Event Ingestion, Extraction/Normalization, Consolidation/Conflict Resolution, Evidence/Provenance, and Forget Fence/Derived Registration specifications. Their full bilingual companions remain pending and are tracked in [translation status](../docs/governance/translation-status.md).

## Architecture completion contract

The current [Compiler Overview](compiler-overview.md) §§20–28 records the Candidate IR / Canonical Schema boundary, five-stage topology, cross-cutting Provenance, D/I authority split and the #459 execution-lifecycle overlay with its in-memory recovery limits. Option A + I1 is DECIDED; B schema-freeze/consumer acceptance, D transaction/currentness/compatibility, I attestor/retention/Forget mapping and all cross-owner consumer contracts remain OPEN. The Runtime acceptance matrix is a plan only; Rust reference-crate unit tests do not constitute matrix or production integration evidence.

## Authority and status

E owns source ingestion/compilation orchestration, candidate generation, stage lineage, retries/replay and producer-side derivative evidence. D owns canonical identity/version/lifecycle and D-side Forget Fence semantics. I owns authorization/PermissionEpoch, revocation, retention and global Forget policy/completion. D/I authority checks jointly constrain protected publication. Storage/Consistency owns no semantics by default; its accountable implementation owner must be explicitly assigned.

CANDIDATE descriptions are not approved schemas. E emits neutral CandidateProposition/ExtractionIR only; it does not mint ClaimRef/ClaimRevisionRef/FactRef/FactRevisionRef or infer Fact from confidence. D owns canonical identity/revision/currentness/lifecycle and D ForgetFence; I owns authorization/PermissionEpoch, attestor authorization, retention and global Forget policy/completion. Exact B/D/I/H/Storage consumer contracts and transaction/compatibility evidence remain OPEN. No schema, DDL, public API, wire or Runtime freeze is authorized.

**Source/mirror status:** this root reading guide is Informative / Non-Canonical. The EN and ZH-CN files under `docs/en` and `docs/zh-CN` are its Non-Canonical language mirrors. The normative Compiler Overview and Extraction/Normalization specifications have separate canonical root sources.
