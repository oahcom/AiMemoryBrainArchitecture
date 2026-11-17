# Memory Compiler — Architecture Guide

- Document ID: DOC-COMP-001
- Version: 1.0
- Owner: E — Memory Compiler
- Source: E owner branch, compiler overview and Phase 3 accepted-receipt/Forget contracts
- Chinese counterpart: [记忆编译器架构指南](../../zh-CN/04-memory-compiler/memory-compiler-guide.md)
- Status: Explanatory guide; stage topology remains CANDIDATE and resource/performance claims TO_VALIDATE

## 1. Purpose

The Memory Compiler turns durably accepted Events and registered source material into traceable candidate Memory, Claim, Entity, and Relation assets. It coordinates canonical commit only through D-owned contracts, then requests downstream projection/index publication.

It is a recoverable semantic transformation pipeline—not a shortcut that sends text to an LLM and writes vectors to a database.

## 2. What E owns

- Compile-work orchestration and durable work-item state.
- Deterministic validation, normalization, classification, and source handling.
- Optional model-assisted extraction under bounded, versioned policies.
- Evidence and Provenance creation, including exact source references and derivation lineage.
- Candidate Entity/Relation proposals and conflict proposals.
- Retry, lease, replay, and terminal disposition of compiler work.
- Coordination of canonical writes and publication notifications without taking over D's authority.

E does not own canonical schema/lifecycle authority (D), Runtime retrieval and cache (F), ContextVersion (G), BMCP wire/Adapter behavior (H/C), global identity/permission/retention policy (I), or physical index implementation.

## 3. Acceptance is not compilation

Keep these milestones separate:

| Milestone | Meaning |
|---|---|
| Accepted | Source Event and required receipt/idempotency state are durably recorded |
| Compiled | A compiler work item reached a recorded processing outcome |
| Candidate produced | A structured candidate and its lineage were created |
| Canonical committed | D accepted and committed an authoritative Memory version |
| Indexed | A particular index partition accounted for the canonical commit |
| Context applied | A later Adapter boundary attestation; not an E responsibility |

An Accepted Event may legitimately result in NO_CANDIDATE, PENDING_EVIDENCE, REVIEW_REQUIRED, DEFERRED, or REJECTED. Durable acceptance must not depend on synchronous LLM inference.

## 4. Pipeline

~~~text
Durable Event + Idempotency + Accepted Receipt
        ↓
Recoverable Compile Intent / Work Item
        ↓
Scope and authorization checks
        ↓
Deterministic normalization and classification
        ↓
Optional model-assisted extraction
        ↓
Evidence / Provenance / Candidate Memory & Claim
        ↓
Entity and Relation resolution proposals
        ↓
Conflict proposal and canonical write request
        ↓
D Canonical Commit
        ↓
Index / projection publication request
~~~

Scope filtering occurs before source dereference, extraction, entity matching, merge, or write. Deterministic stages must continue to function when the inference provider is unavailable.

## 5. Model-assisted processing

LLMs may propose extraction or normalization results, but they do not establish truth, approve canonical lifecycle transitions, resolve authorization, or decide whether Fact is a separate domain object. Every model-assisted transformation must record enough information to identify its model/prompt/policy version, input lineage, output, and validation result according to the detailed contract.

The pipeline must be bounded: timeouts, retries, concurrency, token budgets, and resource quotas must be explicit. Model failure should defer or retry eligible work, not lose the accepted source.

## 6. Durable work, idempotency, and replay

Each work item needs stable identity, source and scope references, schema/policy version, idempotency scope, lease/retry state, and durable stage outcome. Replaying the same logical work must not create duplicate canonical effects.

A repeated idempotency key with a different payload digest is a conflict, not a successful duplicate. Accepted Receipt is not the same as Canonical Commit Receipt.

Retries and replay must re-check current authorization and Forget Fence state. Old work cannot bypass a later Forget operation simply because it was accepted before the fence.

## 7. Forget and derived publication

E is a producer of derived artifacts and must participate in D's Forget contract:
- Register producer classes and individual work before their output becomes visible.
- Preserve durable lineage and dependency registration for each derivative.
- Keep staged output invisible until the publication gate passes.
- At final publication, re-check the current Forget Fence and authorization.
- On retry, lease recovery, DLQ replay, or recompile, do not resurrect suppressed content.

The exact atomic boundary between producer admission, Fence installation, dependency registration, and publication is a cross-owner D/E/Storage/Consistency requirement. An E-local check alone cannot close the race. This remains an implementation/conformance blocker until proven by transaction design and fault-injection tests.

## 8. Failure handling

| Failure | Required behavior |
|---|---|
| LLM unavailable | Continue deterministic stages; defer/retry model-dependent stage |
| Worker crash | Recover durable work from lease/intent state |
| Duplicate delivery | Idempotent no-op or return prior receipt |
| Same key, different digest | Reject as conflict |
| Missing source | Preserve reference and mark unavailable; do not fabricate |
| Permission revoked | Re-check and fail closed before protected processing/publication |
| Forget Fence advanced | Suppress stale output; record terminal disposition |
| Canonical commit conflict | Re-read D state and reconcile; never silently overwrite |
| Index publication delayed | Keep canonical commit distinct from index visibility |

## 9. Interfaces and non-guarantees

Inputs include Accepted Event references, source/content references, authenticated Actor/Scope context, permission decision context, schema version, timestamps, idempotency identity, retention class, trust metadata, and correlation/causation IDs.

Outputs include stage receipts, candidate envelopes, Evidence/Provenance references, Entity/Relation and ConflictSet proposals, CanonicalWriteRequest/Result, publication requests, and structured retryable/permanent errors.

Compiler output does not prove truth, user intent, authorization for external actions, model correctness, index visibility, Context application, or physical erasure.

## 10. Validation still required

- Accepted receipt and idempotency crash consistency.
- Worker crash, lease expiry, retry, DLQ, replay, and recompile behavior.
- D/E/Storage atomic producer admission and publication gate.
- Forget race and late-derivative suppression.
- Provenance completeness and unauthorized source dereference denial.
- Model-offline degraded operation and bounded resource use.
- Representative throughput and latency benchmarks.

## 11. Detailed source specifications

See the [E owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-e-memory-compiler-2026-11-16/04-memory-compiler) for the detailed Compiler contracts. This guide does not replace field-level schemas or claim implementation acceptance.
