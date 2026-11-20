# MVP Architecture Decisions — Store / Query / Inject

- Document ID: MVP-ARCH-DECISIONS-001
- Version: 1.0
- Date: 2026-11-20
- Status: **MVP PILOT BASELINE — implementation profile selected; cross-owner contracts remain conditional**
- Chinese counterpart: [MVP 架构决策](../zh-CN/governance/MVP-ARCHITECTURE-DECISIONS.md)
- Source baseline: main@e52594f181d2edb77448adcfed64a0fbdffaf3aa
- Sources: ARCH-CONVERGENCE-001-SOURCE-OF-TRUTH.md (aa9d4325cf3a67351ee8532828b76529466f272e); ARCH-CONVERGENCE-001-CANONICAL-TRANSACTION.md (927e31fe10ebe0b8dc0893ec75dc10cf25c4f671); ARCH-CONVERGENCE-001-CONTEXT-APPLIED-RUNTIME.md (b3be28a20d537d6fe4a0dcf5a190c539b6380dc1); TAB-001 (7b6f2d139217dbe13ab3a3af31bfbff525f20e71); GOV-DOC-001 (0e170479e1a71e8f4c124c6f1dc170241652f42b).

## 1. Decision summary

This document defines the smallest usable pilot contract across three public operations:

1. **Store** — accept a typed, evidence-linked memory write and commit one immutable canonical MemoryVersion.
2. **Query** — retrieve authorized canonical MemoryVersion references as candidates; an index hit is neither canonical truth nor Context application.
3. **Inject** — create a versioned Context delivery and report the strongest runtime stage actually evidenced. Only G may persist an Applied decision.

These are implementation-facing MVP decisions, not a declaration that the underlying Owner contracts have become globally approved. D's detailed record layout and transaction implementation remain candidates; B ADR-001 Fact/Claim semantics remain blocked; Storage L1 Option A is selected but L4 physical engine/deployment is open; C/G/H/I cross-owner Applied evidence mapping is not frozen. This document preserves those limits.

## 2. Three core interfaces

The following are complete TypeScript contract modules. Each block is independently copyable. TypeScript expresses the public API; the core implementation language is Rust.

### 2.1 Store

~~~typescript
/* Store contract — standalone TypeScript */
export type StoreId = string;
export type StoreDigest = string;

export interface StoreActor {
  principalRef: StoreId;
  producerRef: StoreId;
  permissionEpoch: number;
}
export interface StoreScope {
  scopeRef: StoreId;
  environmentRef: StoreId;
}
export interface StoreEvidenceRef {
  evidenceRef: StoreId;
  digest: StoreDigest;
  mediaType: string;
}
export interface StoreProvenance {
  sourceEventRef: StoreId;
  sourceRecordedAt: string; // RFC 3339
  derivationRunRef?: StoreId;
  evidence: readonly StoreEvidenceRef[];
}
export type StoreCandidateValue =
  | { kind: "text"; value: string }
  | { kind: "number"; value: number; unit?: string }
  | { kind: "boolean"; value: boolean }
  | { kind: "entity-reference-candidate"; mention: string; typeHint?: string }
  | { kind: "structured-candidate"; schemaId: string; fields: Readonly<Record<string, string | number | boolean | null>> };

export interface StoreCandidateProposition {
  schemaVersion: "candidate-proposition/1";
  candidateRef: StoreId;
  subject: { label: string; typeHint: string };
  predicate: { name: string; typeHint: string };
  value: StoreCandidateValue;
  scope: StoreScope;
  observedAt?: string;
  validFrom?: string;
  validUntil?: string;
  epistemicQualifier?: "reported" | "observed" | "inferred" | "uncertain";
  provenance: StoreProvenance;
}
/** Neutral memory envelope; not a canonical Fact or Claim. */
export interface StoreMemoryContent {
  schemaVersion: "memory-content/1";
  title: string;
  bodyText: string;
  tags: readonly string[];
  candidatePropositions: readonly StoreCandidateProposition[];
  provenance: StoreProvenance;
}
export interface StoreCommitRequest {
  actor: StoreActor;
  scope: StoreScope;
  idempotencyKey: string;
  semanticRequestDigest: StoreDigest;
  memoryRef?: StoreId;
  expectedParentVersionRef?: StoreId;
  content: StoreMemoryContent;
}
export interface StoreCommitReceipt {
  memoryRef: StoreId;
  memoryVersionRef: StoreId;
  aggregateRevision: number;
  canonicalCommitCursor: string;
  lifecycleEventRef: StoreId;
  committedAt: string;
  contentDigest: StoreDigest;
  replayed: boolean;
}
export type StoreErrorCode =
  | "INVALID_INPUT" | "AUTHORIZATION_DENIED" | "PERMISSION_EPOCH_STALE"
  | "FORGET_FENCE_ACTIVE" | "PROVENANCE_INCOMPLETE" | "VERSION_CONFLICT"
  | "IDEMPOTENCY_CONFLICT" | "STORAGE_UNAVAILABLE"
  | "OUTCOME_UNKNOWN" | "OUTCOME_IN_DOUBT";
export interface StoreError {
  code: StoreErrorCode;
  message: string;
  operationRef: StoreId;
  retry: "NEVER" | "READ_BACK_SAME_OPERATION" | "RECONCILE_SAME_OPERATION";
}
export type StoreResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: StoreError };

export interface Store {
  /**
   * Atomically commits immutable version, head CAS, provenance/evidence links,
   * lifecycle event, commit receipt/cursor and durable outbox intent.
   * Same key + same digest returns the original receipt; changed digest conflicts.
   */
  commit(request: StoreCommitRequest): Promise<StoreResult<StoreCommitReceipt>>;
}
~~~

### 2.2 Query

~~~typescript
/* Query contract — standalone TypeScript */
export type QueryId = string;
export interface QueryActor {
  principalRef: string;
  agentInstanceRef: string;
  permissionEpoch: number;
}
export interface QueryScope {
  scopeRef: string;
  environmentRef: string;
}
export interface QueryRequest {
  queryId: QueryId;
  actor: QueryActor;
  scope: QueryScope;
  text: string;
  limit: number; // MVP: 1..50
  filters?: {
    tagsAny?: readonly string[];
    sourceEventRefs?: readonly string[];
    recordedAfter?: string;
    recordedBefore?: string;
  };
}
export interface QueryCandidate {
  memoryRef: string;
  memoryVersionRef: string;
  title: string;
  excerpt: string;
  score: number;
  recordedAt: string;
  provenanceRefs: readonly string[];
  contentDigest: string;
}
export interface QueryResult {
  queryId: QueryId;
  candidates: readonly QueryCandidate[];
  completeness: "COMPLETE" | "PARTIAL" | "UNAVAILABLE";
  indexWatermark?: string;
  evaluatedPermissionEpoch: number;
  evaluatedAt: string;
}
export type QueryErrorCode =
  | "INVALID_QUERY" | "AUTHORIZATION_DENIED" | "PERMISSION_EPOCH_STALE"
  | "FORGET_FENCE_ACTIVE" | "INDEX_UNAVAILABLE" | "CANONICAL_READ_UNAVAILABLE";
export interface QueryError {
  code: QueryErrorCode;
  message: string;
  retryable: boolean;
}
export type QueryResponse =
  | { ok: true; value: QueryResult }
  | { ok: false; error: QueryError };

export interface Query {
  /**
   * Finds canonical references through a rebuildable index. Before returning
   * candidates, revalidate canonical version, Scope, current authorization and
   * Forget visibility. Index rows and scores are never authoritative.
   */
  search(request: QueryRequest): Promise<QueryResponse>;
}
~~~

### 2.3 Inject

~~~typescript
/* Inject contract — standalone TypeScript */
export interface InjectActor {
  principalRef: string;
  agentInstanceRef: string;
  sessionRef: string;
  permissionEpoch: number;
}
export interface InjectScope {
  scopeRef: string;
  environmentRef: string;
}
export interface InjectRequest {
  actor: InjectActor;
  scope: InjectScope;
  contextRef: string;
  expectedContextVersionRef?: string;
  deliveryIdempotencyKey: string;
  queryId: string;
  memoryVersions: readonly {
    memoryRef: string;
    memoryVersionRef: string;
    contentDigest: string;
  }[];
  managedRegion: {
    regionRef: string;
    inventoryDigest: string;
    contentDigest: string;
  };
}
export type InjectStage =
  | "CONTEXT_VERSION_COMMITTED" | "DELIVERY_INTENT_COMMITTED"
  | "DELIVERY_ACCEPTED" | "MANAGED_REGION_MATERIALIZED"
  | "FINAL_REQUEST_SUBMITTED" | "APPLIED_DECISION_COMMITTED" | "REJECTED" | "UNKNOWN" | "IN_DOUBT";
export type InjectAppliedStatus = "NOT_APPLIED" | "FULL_APPLIED";
export interface InjectEvidence {
  inferenceRequestRef?: string;
  deliveryRef: string;
  contextVersionRef: string;
  adapterInstanceRef?: string;
  boundaryRef?: string;
  adapterCapabilityEpoch?: number;
  permissionEpoch: number;
  forgetFenceRef: string;
  managedRegionInventoryDigest: string;
  managedRegionContentDigest: string;
  coverage: "COMPLETE" | "PARTIAL" | "BYPASSED" | "UNKNOWN";
  evidenceTier: 1 | 2 | 3;
  providerHandoff:
    | "HANDOFF_ACCEPTED" | "HANDOFF_REJECTED" | "NOT_INVOKED"
    | "UNKNOWN" | "IN_DOUBT";
}
export interface InjectResult {
  deliveryRef: string;
  contextVersionRef: string;
  stage: InjectStage;
  applied: InjectAppliedStatus;
  evidence?: InjectEvidence;
  appliedRecordRef?: string;
  reasonCode?: string;
}
export type InjectErrorCode =
  | "AUTHORIZATION_DENIED" | "PERMISSION_EPOCH_STALE" | "FORGET_FENCE_ACTIVE"
  | "CONTEXT_VERSION_CONFLICT" | "DELIVERY_REJECTED" | "EVIDENCE_INCOMPLETE"
  | "PROVIDER_OUTCOME_UNKNOWN" | "PROVIDER_OUTCOME_IN_DOUBT"
  | "APPLIED_COMMIT_UNAVAILABLE";
export interface InjectError {
  code: InjectErrorCode;
  message: string;
  retry: "NEVER" | "RECONCILE_SAME_DELIVERY" | "RECONCILE_SAME_PROVIDER_ATTEMPT";
}
export type InjectResponse =
  | { ok: true; value: InjectResult }
  | { ok: false; error: InjectError };

export interface Inject {
  /**
   * Creates/updates G-owned versioned Context delivery and coordinates H/C.
   * FULL_APPLIED is allowed only after G durably commits its Applied record
   * from complete Tier-1 evidence bound to the exact immutable submitted
   * inference request and current I authorization + D Forget state.
   * ACK, materialization, workflow completion or provider response alone
   * must leave applied = NOT_APPLIED.
   */
  deliver(request: InjectRequest): Promise<InjectResponse>;
}
~~~

## 3. Technology selection

| Concern | MVP selection | Status and boundary |
|---|---|---|
| Core implementation language | **Rust stable, Edition 2024** | Follows TAB-001 Rust-primary direction. |
| Async runtime | **Tokio** | IO and workers; keep correctness-critical transitions in one process initially. |
| Serialization | **Serde** | Typed, versioned envelopes; never deserialize arbitrary payloads into canonical Fact/Claim. |
| Error handling | **thiserror** in domain/storage libraries; typed result enums at ports; **anyhow** only at process/CLI boundary | Preserve stable error codes and retry disposition. |
| Pilot persistence | **SQLite in WAL mode**, behind a Storage adapter | TAB-001 conditional first-prototype recommendation; not an L4 freeze. |
| Transaction topology | **One logical serializable transaction domain per Canonical Memory authority** | Storage/D L1 Option A. SQLite locking/transaction behavior must pass race/crash tests before claiming conformance. |
| Identifiers | UUIDv7 strings for generated entity/operation IDs; distinct Rust newtypes | Cursor namespaces are never interchangeable. |
| Canonical data | Immutable MemoryVersion rows, aggregate-head CAS, append-only LifecycleEvent, CanonicalCommit receipt/cursor, idempotency receipt, durable outbox | Atomic commit or formally proven recoverable equivalent. |
| Retrieval index | SQLite FTS5 lexical index as rebuildable projection | IndexWatermark is not CanonicalCommitCursor or ForgetFenceCursor. |
| Vector/graph | Deferred | Not required for first vertical slice; no graph inference from co-occurrence. |

### Data structure rules

- D owns canonical Memory identity and immutable MemoryVersion.
- Every write carries typed source Event/Evidence/Provenance references. If provenance is unavailable, record an explicitly permitted unavailable reason; never silently omit it.
- While B ADR-001 is ADR-BLOCKED, proposition data remains a versioned neutral CandidateProposition/ExtractionIR envelope. Do not introduce canonical FactRef/ClaimRef, Fact/Claim DDL or wire discriminants.
- CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark, ForgetFenceCursor, PermissionEpoch, ContextVersion and AdapterCapabilityEpoch are distinct typed namespaces, not interchangeable integers.
- Search indexes, caches, excerpts and embeddings are projections only. Revalidate canonical version, authorization and Forget state before use.
- Context is a G-owned versioned selection of immutable canonical references; editing Context does not mutate Canonical Memory.

### Error and retry rules

1. Domain/contract failures return typed errors; do not swallow exceptions or translate every failure to false/empty results.
2. Same idempotency key + same semantic digest returns the original receipt/result. Same key + different digest returns IDEMPOTENCY_CONFLICT.
3. Version/CAS conflict is explicit; no last-writer-wins overwrite or implicit merge.
4. Timeout, lost ACK, process crash or missing row is not proof of failure. Reconcile UNKNOWN/IN_DOUBT with the same stable operation identity; never issue a new provider key while side effects may exist.
5. A retry gets a new execution AttemptId/LeaseId but preserves logical work/operation identity. Recheck PermissionEpoch and ForgetFence before resuming.
6. No partial canonical commit is visible. Version/head, lifecycle event, receipt/cursor and outbox intent are one atomic set.
7. Query index lag is reported as PARTIAL/UNAVAILABLE; never fabricate completeness or present stale data as current.
8. Inject stages are not collapsed into a generic success boolean. Only G's durable predicate may produce FULL_APPLIED.

## 4. Implementation boundary

### Do in the MVP

- Implement Store as the only canonical write port, with D-owned identity/version/head and transaction semantics.
- Implement durable idempotency, expected-version CAS, provenance/evidence linkage, append-only lifecycle events and transactional outbox.
- Implement Query with FTS5, bounded top-K, explicit filters, provenance references, completeness and IndexWatermark.
- Revalidate canonical version, Scope, current I authorization/PermissionEpoch and D ForgetFence before query results are exposed or injected.
- Implement Inject with G ContextVersion and Delivery intent, a controlled in-process H Adapter/runtime harness, and an observable C final-request submission hook where available.
- Persist G Applied separately and only when the exact final immutable request has complete Tier-1 evidence and all required owner proofs are current.
- Test idempotency replay/conflict, CAS races, crash-before/after-commit, outbox duplication, permission revocation, Forget races, stale Context delivery, incomplete evidence, provider UNKNOWN/IN_DOUBT and Applied replay.

### Do not do in the MVP

- Do not freeze or invent canonical Fact/Claim identity while B ADR-001 is blocked.
- Do not let agents, adapters, providers or external memory products write canonical storage directly.
- Do not conflate Event acceptance, compiler completion, canonical commit, index publication, delivery ACK, materialization, provider response or workflow completion.
- Do not claim Full Applied without exact final-request observation, actual request identity, complete managed-region digest and G's durable Applied commit.
- Do not infer model attention, understanding, recall, behavioral compliance or correctness from Applied.
- Do not claim global Forget completion or physical erasure in Store/Query/Inject; enforce D local suppression and defer global completion to I/D governance.
- Do not add microservices, Kafka, Kubernetes, hosted vector DB, mandatory cloud inference, graph DB, autonomous agent planning or a second canonical store.
- Do not make vector search, embeddings, graph traversal, summarization or LLM extraction prerequisites for the first vertical slice.
- Do not claim SQLite WAL has proven L1 serializability, crash recovery, HA, PITR or restore quarantine until Storage validation evidence exists.

## 5. Acceptance gates

The pilot is implementation-ready at the interface level, but is **not production-certified** until executable evidence exists:

- Store: atomic version/head/event/receipt/cursor/outbox commit; CAS failure has no visible effects; same-key replay is idempotent; changed digest conflicts.
- Query: authorization and Forget revalidation; stale projection cannot bypass canonical read; watermark advances only across a contiguous prefix.
- Inject: delivery and materialization remain distinct; Tier-2/Tier-3 cannot yield Full Applied; exact final-request digest is checked; UNKNOWN/IN_DOUBT suppresses blind retries; G Applied is idempotent across crash/replay.
- Storage: actual SQLite WAL profile passes concurrent-writer, process-crash and restore tests for the selected L1 topology.
- Documentation: Chinese/English semantic parity and links are checked in the same change set.

## 6. Authority and change control

This MVP profile does not approve B ADR-001, replace D/E/F/G/H/I/Storage Owner contracts, freeze Storage L4, or certify C/G/H/I production evidence. If implementation convenience conflicts with an Owner contract, the Owner contract and approved ADR take precedence. Changes to canonical identity, transaction atomicity, authorization, Forget, Applied semantics or wire identity require the relevant Owner/ADR decision.

**Disposition:** Store / Query / Inject are defined for a bounded pilot. Rust + Tokio + Serde + SQLite WAL is the concrete first-prototype stack; SQLite remains conditional pending Storage validation. No production conformance or end-to-end execution is claimed.
