# Canonical Memory Brain — Architecture Guide

- Document ID: DOC-BRAIN-001
- Version: 1.0
- Owner: D — Memory Brain
- Source revision: a157b0ed6fc8e45e66fe01a99e6b895f995fd20c
- Chinese counterpart: [权威记忆大脑架构指南](../../zh-CN/03-memory-brain/memory-brain-guide.md)
- Status: Explanatory guide; cross-module execution and implementation evidence remain subject to integration gates

## 1. What the Memory Brain is

The Memory Brain is the authority for durable, addressable Canonical Memory assets. It owns stable Memory identities, immutable versions, canonical references to Claims, Entities and Relations, lifecycle history, and the canonical-domain records needed to govern Forget.

It is not the ingestion pipeline, retrieval engine, Agent context planner, protocol gateway, global authorization provider, or physical deletion executor. Those responsibilities belong to E/F/G/H/I and shared infrastructure under explicit contracts.

## 2. What D owns—and what it does not

| D owns | D does not own |
|---|---|
| Canonical Memory identity and immutable versions | Event ingestion and full compilation pipeline (E) |
| Canonical current-version pointer and historical reads | Retrieval ranking, Runtime cache, index maintenance (F) |
| Canonical lifecycle records and transition history | Context planning, ContextVersion, delivery state (G) |
| Entity/Relation canonical identity and references | BMCP wire protocol and Adapter local behavior (H) |
| ForgetOperation, canonical Forget Fence, dependency inventory authority | Global authorization, retention/backup policy, physical erasure (I) |
| Canonical commit cursor semantics | Storage engine implementation and transaction proof |

This boundary is important: D can define the canonical Forget barrier and provide evidence about canonical targets, but it cannot claim that all indexes, caches, Adapters, backups, and external copies have been erased.

## 3. Canonical Memory and immutable versions

A Memory is a stable identity with a sequence of immutable versions. Updating a Memory creates a successor version; it never edits a historical version in place.

A canonical commit must:
- Validate object identity, references, scope compatibility, schema version, and required evidence/provenance.
- Use expected-version/CAS or equivalent concurrency control.
- Preserve historical versions and explicit change reasons.
- Advance the current-version pointer consistently with the committed version.
- Publish a recoverable change intent so indexes and consumers can reconcile.

A schema-valid object is not automatically true. D stores canonical assertions and their evidence/epistemic qualification; it does not independently adjudicate objective truth.

## 4. Lifecycle is not truth

Lifecycle describes management state, not confidence, relevance, trust, or Claim epistemic status. The D canonical lifecycle vocabulary includes Candidate, Consolidated, Active, Superseded, Archived, and Forgotten. A Claim may be Disputed while its containing Memory remains Active.

Forget is represented by a governed ForgetOperation and its durable records. Temporary suppression/workflow state must not be confused with an ordinary Memory lifecycle transition. A Memory is marked Forgotten only when the governing completion criterion is met; D cannot unilaterally declare global completion.

## 5. Entity and Relation identity

Entity identity is not a display name, mention string, or similarity match. D preserves stable opaque Entity IDs, versioned attributes/aliases, resolution evidence, and explicit merge/split history.

A Relation is a typed association with validated endpoints, directionality, scope, temporal validity, epistemic qualification, and evidence references. Co-occurrence or embedding similarity is not sufficient to create a canonical Relation. Ambiguous identity resolution must return ambiguity rather than guess.

## 6. Canonical cursor model

D defines one globally ordered CanonicalCommitCursor per Canonical Memory authority. Other cursors remain separate typed namespaces:

| Cursor | Scope | What it orders |
|---|---|---|
| CanonicalCommitCursor | One Brain authority | Successful canonical transactions |
| AggregateRevision | One aggregate | Immutable revisions of that aggregate |
| LifecycleEventCursor | One Memory | Append-only lifecycle events |
| IndexWatermark | One index partition | Contiguous canonical commit prefix accounted for by that partition |
| ForgetFenceCursor | One Forget operation | Fence generation and target-set identity |

These tokens are not interchangeable. A canonical commit cursor does not prove index application, Context delivery, Forget suppression, or physical deletion. IndexWatermark does not prove global Forget completion.

## 7. Forget Fence and completion boundary

The Forget Fence is a durable suppression barrier. Its purpose is to prevent stale or late work from publishing or exposing content after a Forget operation has taken effect.

D's canonical-domain contract covers:
1. A durable ForgetOperation identity and monotonic fence generation.
2. The affected canonical target set and dependency inventory.
3. Producer registration and barrier accounting.
4. A canonical-domain suppression decision and per-target progress evidence.
5. A controlled lifecycle transition to Forgotten under I's governing completion criterion.

Cross-module execution is divided by owner:

| Owner | Forget responsibility |
|---|---|
| D | Canonical ForgetOperation, Fence, dependency inventory, canonical target proof |
| E | Queues, leases, retries, DLQ, replay, derivative registration and publish gate |
| F | In-flight retrieval, candidate suppression, cache/working set, index rebuild and watermarks |
| G | Context snapshots, deltas, ChangeSets, delivery intents and reconciliation |
| H | Adapter local state, offline reconnect, clear/suppression ACK |
| I | Principal/authorization, retention, backup/external copies, residual exceptions, global completion policy |

**Critical implementation gap:** producer admission, Fence installation, dependency registration, and derivative publication must share a proven atomic/linearizable boundary. A separate “read Fence, then publish” sequence is unsafe. D and E have described the required semantics, but D/E/Storage integration and fault-injection evidence are still required. Do not mark the global Forget loop complete based on D's local records.

## 8. Failure and recovery expectations

- Canonical versions are immutable; recovery advances or reconciles pointers rather than rewriting history.
- Stale writes are rejected and reconciled against the latest canonical version.
- Outbox/replay must be idempotent and re-check current Fence and authorization.
- Missing evidence/source material is marked unavailable; it must not be fabricated during replay.
- Indexes and projections are rebuildable, but rebuild must respect Forget fences and current policy.
- Cursor gaps and consumer lag must be explicit; a cursor is not a substitute for a consumer receipt.
- A crash between durable state and publication must be recoverable without duplicate logical effects or stale resurrection.

## 9. Open and validation items

- Fact/Claim identity and revision semantics remain subject to the blocked ADR; downstream schema freeze is prohibited until formal resolution.
- Storage must prove the atomic producer-admission/Fence/publication operation.
- E/F/G consumers must conform to the typed cursor namespaces.
- I must define global Forget completion and residual-exception policy.
- H/C must prove Adapter clear/reconnect and Applied evidence.
- Crash, race, replay, index rebuild, cache invalidation, and backup-restore tests remain required.

## 10. Detailed D source specifications

- [Memory Brain Overview](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/memory-brain-overview.md)
- [Canonical Memory Store](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/canonical-memory-store.md)
- [Memory Lifecycle Manager](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/memory-lifecycle-manager.md)
- [Entity and Relationship Manager](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/entity-and-relationship-manager.md)
- [Memory Versioning](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/memory-versioning.md)
- [Forget Fence and Completion Contract](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/forget-fence-and-completion-contract.md)
- [Canonical Commit Cursor Semantics](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/commit-cursor-semantics.md)

This guide makes the responsibility boundaries and critical invariants readable; it does not claim the atomic storage operation or end-to-end Forget behavior has been implemented or verified.
