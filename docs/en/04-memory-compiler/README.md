# Memory Compiler — Reading Guide

- Document ID: E-READING-GUIDE-001
- Version: 1.0
- Chinese counterpart: [Memory Compiler 阅读指南](../../zh-CN/04-memory-compiler/README.md)

## Available bilingual source specifications

1. [Compiler Overview](compiler-overview.md) — pipeline, boundaries, deterministic/model-assisted stages and safety invariants.
2. [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md) — durable acceptance, independent receipts, retry/replay and evidence boundaries.
3. [Compiler State and D Producer Admission](compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease identity, D registration, barrier and terminal disposition.

## Remaining core source specifications

The E branch inventory also contains Event Ingestion, Extraction/Normalization, Consolidation/Conflict Resolution, Evidence/Provenance, and Forget Fence/Derived Registration specifications. Their full bilingual companions remain pending and are tracked in [translation status](../../governance/translation-status.md).

## Authority and status

E owns source ingestion/compilation orchestration, candidate generation, stage lineage, retries/replay and producer-side derivative evidence. D owns canonical identity/version/lifecycle and Forget Fence semantics. I owns authorization/PermissionEpoch and global Forget policy. Storage/Consistency owns no semantics by default; its accountable implementation owner must be explicitly assigned.

CANDIDATE descriptions are not approved schemas. No Fact/Claim mapping is frozen while ADR-BLOCKED. D/E/Storage atomic admission/dependency/publication implementation remains OPEN until joint evidence is reviewed.
