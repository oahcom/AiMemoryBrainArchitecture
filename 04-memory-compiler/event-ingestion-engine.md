---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-e-memory-compiler-2026-11-16"
        - "source commit: ee098e14747d9915de5b3efb63b3a8dd77f670ed"
        - "original source blob: 9fa3db53175452bf9e6f0fce8b1540765e46905f"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact E source Blob pinned; Owner exact-version and dependency review pending."
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
    canonical_status: Candidate
    canonical_scope: "Memory Compiler event ingestion and Accepted semantics"
    canonical_scope_id: memory-compiler/event-ingestion-engine
    canonical_scope_keywords:
      - event-ingestion
      - accepted-receipt
      - outbox
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/event-ingestion-engine.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/event-ingestion-engine.md"
---

# Event Ingestion Engine

**Status:** DECIDED for Accepted semantics and safety invariants; CANDIDATE for outbox/queue topology; TO_VALIDATE for sizing and ordering targets.  
**Owner:** Memory Compiler / MC-01.  
**Integration:** INT-P0-02/03; INT-P1-03/04; C telemetry identity and source semantics.

## 1. Purpose

Accept authenticated source events into durable Brain custody with truthful receipt semantics, idempotent retries, recoverable compile intent, and explicit backpressure. Ingestion is a durability boundary, not semantic verification or Memory compilation.

## 2. Scope

Includes envelope validation, source identity binding, Scope resolution, permission checks, payload integrity, idempotency, durable event persistence, processing intent/outbox, receipts, admission control, queue priority, retry, DLQ, replay and crash recovery.

Excludes Agent-side telemetry mapping and BMCP wire format (H), canonical Memory semantics/lifecycle (D), global policy/retention definitions (I), Runtime Recall, and compilation stages after dispatch.

## 3. Responsibilities

Validate a versioned Event Envelope; bind authenticated producer to source identity; resolve explicit Scope including Environment Scope; authorize event.ingest and retention obligations; persist immutable source Event, payload reference/digest, idempotency record, receipt and processing intent as one recoverable unit; return Accepted only after durable commit; preserve event_time separately from Brain recorded_at; reconstruct work; re-check authorization and Forget/retention fences before processing.

## 4. Non-Responsibilities

Ingestion does not decide whether a statement is true, extract Claims, infer outcomes, resolve semantic entities, create Canonical Memory, authorize future actions, or guarantee index visibility. Accepted is not compiled, verified, indexed, or activated.

## 5. Inputs / Outputs

Input: authenticated principal/producer context, schema version, source type/id, source payload or durable ContentRef, ScopeRefs, optional EnvironmentScope, event kind/classification, event_time with source precision/timezone, idempotency key, payload digest, retention class, sensitivity, correlation/causation IDs, and source trust metadata.

Output: AcceptedReceipt or typed rejection/retryable-unavailable. Receipt contains stable event_id, receipt_id, accepted_at/recorded_at, idempotency identity fingerprint, payload digest, schema version, and processing_state=Pending. It must not claim compilation.

## 6. Data Model

### 6.1 EventEnvelope (logical; wire names owned by H)

~~~text
EventEnvelope {
  schema_version: Version
  event_kind: EventKind
  source_type: SourceType
  source_id: OpaqueIdOrNamespacedString
  producer_actor_ref: ActorRef
  producer_instance_ref: ActorRef?
  scope_refs: ScopeRef[]
  environment_scope_ref: ScopeRef?
  classification: observed | reported | planned | predicted |
                  attempted | outcome | administrative | unknown
  payload_ref: ContentRef
  payload_digest: Digest
  content_type: MediaType
  event_time: TimeValue?
  source_recorded_at: TimeValue?
  idempotency_key: OpaqueString
  retention_class: RetentionClass
  sensitivity: Sensitivity
  trust_metadata: SourceTrustMetadata
  correlation_id: OpaqueId
  causation_id: OpaqueId?
  stream_ref: TypedObjectRef?
  stream_sequence: u64?
}
~~~

recorded_at is assigned by Brain at durable acceptance and immutable. Source-provided timestamps remain separately attributed. Environment-dependent events require Environment Scope; a display label is never a stable scope identifier.

### 6.2 Acceptance transaction

~~~text
IngressCommit {
  event_record: ImmutableEvent
  payload_record_or_durable_ref: ContentRef
  idempotency_record: IdempotencyRecord
  accepted_receipt: AcceptedReceipt
  compile_outbox_record: OutboxRecord
  transaction_generation: u64
}
~~~

All records are atomically committed in one local transaction or equivalent WAL protocol. If payload storage is external, payload must be durably staged and integrity-verified before the transaction publishes Accepted; a dangling object-store upload is not an Accepted Event.

### 6.3 Idempotency identity (CANDIDATE pending H/I)

~~~text
IdempotencyScope = (
  authenticated_producer_id,
  owner_scope_id,
  operation_family,
  idempotency_key
)
IdempotencyRecord {
  scope: IdempotencyScope
  canonical_payload_digest: Digest
  event_id: OpaqueId
  receipt_id: OpaqueId
  accepted_at: Instant
  expires_at: Instant?
  state: accepted | forgotten_tombstone | expired
}
~~~

Exact field names and retention window are jointly owned with H/I. Digest is calculated over a versioned canonical envelope representation and payload integrity, not arbitrary JSON key order.

## 7. Pipeline / State Machine

~~~mermaid
sequenceDiagram
 participant P as Producer / Adapter
 participant G as Gateway
 participant I as Ingestion
 participant DB as Durable Event Store + Outbox
 participant W as Compiler Worker
 P->>G: EventEnvelope + idempotency key
 G->>G: Authenticate / resolve Scope / authorize
 G->>I: Validated envelope
 I->>DB: Atomic Event + payload ref + idempotency + receipt + outbox
 DB-->>P: AcceptedReceipt(event_id, receipt_id)
 DB-->>W: Durable pending work
 W->>W: Recheck permission, scope and Forget fence
 W->>W: Claim work lease / process idempotently
~~~

~~~mermaid
stateDiagram-v2
 [*] --> Validating
 Validating --> Rejected: schema / scope / permission invalid
 Validating --> CapacityBlocked: durable capacity unavailable
 CapacityBlocked --> Validating: retry after capacity
 Validating --> Committing: all checks pass
 Committing --> AcceptedPending: atomic durable commit
 Committing --> RetryableUnavailable: commit outcome unknown/unavailable
 AcceptedPending --> Processing
 Processing --> CompiledProposal
 Processing --> RetryScheduled
 RetryScheduled --> Processing
 Processing --> DeadLetter: retry budget / permanent error
 DeadLetter --> Processing: authorized replay
 AcceptedPending --> Suppressed: Forget fence / retention restriction
~~~

### 7.1 Four distinct milestones

| Milestone | Meaning | Evidence |
|---|---|---|
| Accepted | Event, payload reference, Scope, idempotency, receipt, and recoverable processing intent durable | commit generation + receipt |
| Processing | Worker leased or staged work | durable lease/stage receipt |
| Compiled | Compiler completed a candidate proposal, not necessarily canonical | terminal compiler stage receipt |
| Canonical Commit | D/lifecycle authority accepted and persisted canonical Memory/Claim version | canonical version + commit event |

Indexed is a later F/storage projection milestone and is not implied by Canonical Commit.

## 8. Invariants

No Accepted before durable commit; accepted Events survive compiler/model outage and restart; same idempotency identity and digest returns same Event/receipt; same identity with different digest conflicts; event/source/Brain times remain distinct; acceptance does not verify truth; scope and permission rechecked during async work; environment-dependent data never falls back to Agent-only scope; Forget fences block replay resurrection; lost responses are recovered by retry/status query.

## 9. Idempotency

- Same key + same payload: return original event_id, receipt identity and accepted_at; no second logical work item.
- Same key + different payload digest: reject with IDEMPOTENCY_KEY_REUSE_CONFLICT; preserve original.
- Same payload + different key: distinct submission unless an explicit source-level dedup policy applies.
- Concurrent identical submissions: unique constraint/serialized transaction elects one winner; others return its receipt.
- Replay reuses original Event identity and recorded_at; it adds attempt/replay metadata only.
- Forgotten/expired key: governed tombstone prevents resurrection for the required retention window; exact horizon is I-owned and OPEN.
- Digest algorithm/canonicalization version is stored; historical identity interpretation is never silently changed.

## 10. Consistency and Transaction Boundaries

DECIDED requirement: Event + idempotency record + receipt + compile intent commit atomically or through an equivalent recoverable protocol that cannot expose Accepted without all four.

CANDIDATE implementation: one database transaction writes Event metadata, durable payload reference, idempotency row, receipt and outbox row. Dispatcher reads outbox and publishes work at least once. Worker stage operations are idempotent. If separate blob storage is used, write and verify immutable payload before committing its metadata reference; orphan staged blobs are garbage-collected only after reconciliation.

No distributed transaction across model provider, canonical store and index is assumed.

## 11. Failure Recovery

| Failure point | Required behavior |
|---|---|
| Before transaction | No receipt; producer retries |
| During transaction before commit | Rollback; no Accepted |
| Commit succeeds, response lost | Retry returns original receipt |
| Response returned, worker not dispatched | Outbox scan reconstructs pending work |
| Worker crashes before stage commit | Lease expires; stage retries idempotently |
| Worker commits stage but crashes before ack | Duplicate worker reads committed stage receipt |
| Model unavailable | Accepted work remains pending |
| Canonical write outcome unknown | Query commit/idempotency reference; do not duplicate version |
| Forget after acceptance before processing | Fence suppresses work and schedules derivatives |
| Replay after retention expiry | Reject or mark source unavailable under I policy; never recreate erased payload |

## 12. Security / Scope

At ingress authenticate producer, bind principal to producer/Agent/instance/session/task/environment identity, resolve ScopeRefs, authorize event.ingest, validate retention/sensitivity, and apply per-scope quota. At processing re-evaluate current permission and scope status, validate each referenced payload, and check Forget fence. Filters precede event lookup, source dereference, stream joins, and replay selection.

Agent-provided Scope is a hint until authenticated/resolved. User permission does not automatically grant Evidence access. Raw payload is untrusted; instruction-like content remains data. Errors avoid revealing whether an inaccessible Event exists.

## 13. Performance / Backpressure

CANDIDATE priority classes:
- P0 operational/governance events (Forget, revocation, security incidents);
- P1 task transitions, action outcomes, high-value observations;
- P2 ordinary user/Agent messages and documents;
- P3 high-frequency replaceable telemetry/snapshots and bulk backfills.

Before acceptance, reject with retryable INGRESS_CAPACITY_EXCEEDED if durable capacity cannot be guaranteed; never volatile-buffer and say Accepted. After acceptance, do not discard required Events; delay lower priority compile, batch workers, or coalesce only events whose source contract explicitly permits replacement. Sampling must carry gap/coverage metadata. Bound payload size, producer rate, queue bytes, oldest age, active leases and retry budget. Numeric limits are TO_VALIDATE.

## 14. Observability

Record event/receipt IDs, producer class, scope class, payload digest (not payload), schema version, accepted_at, commit generation, queue age, priority, attempt, lease epoch, error class, replay origin and Forget suppression. Metrics: acceptance p50/p95/p99, rejection/backpressure, outbox lag, queue bytes/age, per-priority wait, duplicate rate, idempotency conflicts, worker lease expiry, replay count, DLQ count, accepted-to-compiled/canonical latency. Avoid raw source and high-cardinality identifiers in metric labels.

## 15. Interfaces

### 15.1 H / BMCP Accepted Contract (logical candidate)

Required: protocol/schema version; authenticated producer identity; ActorRef; resolved ScopeRefs; Event kind/source type/source ID; content type; payload reference or bytes; payload digest; idempotency key; source event time; retention/sensitivity; correlation/causation. H owns wire serialization and authentication envelope.

Receipt: receipt_id, event_id, accepted_at, payload_digest, idempotency identity fingerprint, state=accepted_pending, schema version. accepted_pending does not mean compilation complete.

Errors: INVALID_ENVELOPE, UNAUTHENTICATED_PRODUCER, SCOPE_INVALID, PERMISSION_DENIED, IDEMPOTENCY_KEY_REUSE_CONFLICT, INGRESS_CAPACITY_EXCEEDED, PAYLOAD_UNAVAILABLE, RETRYABLE_UNAVAILABLE.

### 15.2 Retry and Recovery

Retry reuses the same idempotency identity. Receipt lookup returns original acceptance state and later processing state as separate fields. Replay requires authorization and preserves source identity and recorded_at.

### 15.3 D / F / G / I

D receives accepted Event references and owns canonical output; F receives only committed canonical generation events; G receives lifecycle/Forget notifications; I defines retention, deletion, tombstone horizon and worker revocation semantics.

## 16. Test Scenarios

Crash before/during commit, after commit/before response, after response/before dispatch; same key/same digest sequential and concurrent; same key/different digest; payload staged but metadata commit fails; outbox outage/restart; compiler outage; scope/permission revoked while queued; Forget fence while retry/DLQ/replay pending; missing Environment Scope; overload/coalescing; replay after source expiry.

## 17. Dependencies

H for producer identity and BMCP envelope; I for authorization, retention, Forget, audit and tombstones; D for Event semantics and typed references; Consistency/Storage for durable transaction/outbox; C for telemetry classifications and identity binding; F for canonical/index event consumption.

## 18. Open Questions

- **OPEN:** INT-P1-04 final idempotency key composition and receipt schema with H/I.
- **OPEN:** idempotency tombstone and receipt retention horizon under Forget/Retention.
- **CANDIDATE:** local transactional outbox versus WAL-backed journal; select in Rust/storage design.
- **CANDIDATE:** four priority classes and logical lane scheduling.
- **TO_VALIDATE:** payload-size limits, throughput, queue budgets, recovery time and model-offline backlog drain.
- **OPEN:** per-source ordering guarantees and late/out-of-order event policy (coordinate C/H).


## 19. Phase 3 H/I alignment and durable receipt addendum

- H's `message-envelope-and-versioning.md` requires an owner-defined idempotency namespace/key/payload digest, versioned canonicalization and integrity metadata. H currently proposes JCS as a canonicalization candidate; E owns ingress key semantics, while H owns wire representation. Protocol version, payload schema version, permission epoch and Forget fence remain distinct.
- I's `principal-actor-and-authorization-contract.md` proposes idempotency identity scoped by authenticated producer + tenant/security domain + operation family + caller key. The payload ActorRef/producer claim is never authentication. Receipt lookup/replay must not disclose a receipt across principals or scopes.
- I requires authorization at ingress and again on every retry/replay; a durable Accepted receipt is not a standing permission to compile later. E must revalidate current permission epoch and Forget fence at worker execution and final commit/publication linearization points.
- Retention duration is not frozen: I requires coverage of declared retry/replay horizon while minimizing content and subjecting idempotency metadata/tombstones to Forget policy. Exact numeric horizon and legal-hold treatment remain OPEN with I/Privacy/Legal.
- I's scope/revocation matrix explicitly covers compile start, each dereference, derivative creation/publication, canonical commit, DLQ/replay and retries. Missing/stale permission epoch or Forget fence fails closed.
- E's Accepted linearization point remains the atomic/recoverable commit of Event, immutable payload reference/digest, idempotency record, receipt and compile intent. H's receipt wire format and I's identity/retention policy do not move that durability boundary.
- See `accepted-receipt-and-idempotency-contract.md` for the transaction/WAL crash matrix and cursor separation.
