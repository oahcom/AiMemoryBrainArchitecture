---
document_metadata:
  domain: memory-compiler
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: null
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "PR #429 reading guide mirror
        - "OWNER-DECISION-FACT-CLAIM-001, merged PR #446"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Source restored from the current bilingual E design artifact; Fact/Claim semantics reconciled to the merged Owner decision. Runtime/schema approval is not implied."
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
    canonical_status: Canonical
    canonical_scope: "Memory Compiler guide: reading-guide"
    canonical_scope_id: "memory-compiler/reading-guide"
    canonical_scope_keywords:
      - reading-guide
      - source-index
      - acceptance-plan
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/README.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/README.md"
---

# Memory Compiler — Reading Guide

- Document ID: E-READING-GUIDE-001
- Version: 1.2
- Canonical source: restored in 04-memory-compiler/README.md.
- Chinese counterpart: [Memory Compiler 阅读指南](../../zh-CN/04-memory-compiler/README.md)

## Available bilingual source specifications

1. [Compiler Overview](compiler-overview.md) — pipeline, boundaries, deterministic/model-assisted stages and safety invariants.
2. [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md) — durable acceptance, independent receipts, retry/replay and evidence boundaries.
3. [Compiler State and D Producer Admission](compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease identity, D registration, barrier and terminal disposition.

## Available bilingual source specifications

4. [Event Ingestion Engine](event-ingestion-engine.md) — durable Accepted semantics, outbox/queue topology and ordering.
5. [Extraction and Normalization](extraction-and-normalization.md) — neutral CandidateProposition, evidence spans, modality and scope.
6. [Consolidation and Conflict Resolution](consolidation-and-conflict-resolution.md) — no-silent-overwrite, conflict and revision boundaries.
7. [Evidence and Provenance](evidence-and-provenance.md) — source traceability, authorization and derivative lineage.

## Remaining core source specification

Forget Fence and Derived Registration remains the one unpaired core specification (7/8 paired). Its source is available in the historical E owner branch, but the full current bilingual source/mirror pair is not yet restored. Do not treat the surviving Part 1 mirror as a complete normative substitute. Progress is tracked in [translation status](../../governance/translation-status.md).

## Architecture completion contract

The current [Compiler Overview](compiler-overview.md) §§20–27 records the Candidate IR / Canonical Schema boundary, D/I authority split, Owner decision Option A + I1 adopted in merged PR #446; the D schema-freeze and D/I/H consumer-contract gates remain open, compile/validate/serialize semantics, lifecycle flow, Runtime acceptance matrix and engineering-phase prerequisites. The acceptance matrix is a plan only; no Runtime tests or implementation are claimed.

## Authority and status

E owns source ingestion/compilation orchestration, candidate generation, stage lineage, retries/replay and producer-side derivative evidence. D owns canonical identity/version/lifecycle and D-side Forget Fence semantics. I owns authorization/PermissionEpoch, revocation, retention and global Forget policy/completion. D/I authority checks jointly constrain protected publication. Storage/Consistency owns no semantics by default; its accountable implementation owner must be explicitly assigned.

CANDIDATE descriptions are not approved schemas. The Owner has approved Option A + I1 semantics; exact Fact/Claim mapping remains Candidate until D/E/Storage consumer contracts are version-pinned and reviewed. D/E/Storage atomic admission/dependency/publication implementation remains OPEN until joint evidence is reviewed.
