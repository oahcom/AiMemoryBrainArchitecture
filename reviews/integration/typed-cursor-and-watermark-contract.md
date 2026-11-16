# Typed Cursor and Watermark Contract — Phase 3 Coordination Proposal

- Status: **CANDIDATE** (integration proposal; not an approved ADR, schema freeze, or implementation guarantee)
- Coordinators: Session A
- Required reviewers/decision owners: D + Storage/Consistency (canonical commit), E (source Event/ingress), D (LifecycleEvent), index publisher/Storage with E/F (publication), I (Forget policy/epoch), G (ContextVersion/Delivery), H (Adapter capability), C/Agent runtime (InferenceRequestID)
- Baseline refs: D `9dc08c63f6912320e290a963c634748ec44a81c8`; E `54df136d1e410af834461950e3c61c5c80abd6ad`; F `dad5deb6bfaa2df9956930d0b1372df354112567`; G `3d2c065be863bc1d349faaeece6f6eaa0047abae`.

## 1. Purpose and hard rule

The word *cursor*, *sequence*, *generation* or *watermark* MUST NOT be used as an untyped integer across unrelated streams. Each token belongs to one namespace, owner, partition/scope and semantic clock. Numeric offsets are comparable only inside the same namespace, epoch and partition. Cross-stream ordering is expressed through explicit causal references or a vector of typed watermarks, never by comparing raw integers.

A cursor identifies a position in a stream. A revision identifies a version of one aggregate. A watermark states the progress of one named consumer/projection over a named source partition. An epoch is a fencing generation, not a stream offset. A ContextVersion is G's immutable desired state, not a cursor into canonical Memory. A Delivery sequence orders delivery attempts in one consumer stream; it is not an inference request number.

## 2. Typed contract inventory

| Type | Authoritative owner | Namespace / scope | Monotonicity | Gap semantics | Resume / replay | Causal relation |
|---|---|---|---|---|---|---|
| **Source Event cursor** `SourceEventCursor` | E for Brain-assigned durable ingress position; source owns any producer sequence it supplies | `brain.event-log/{tenant-or-owner-scope}/{producer-stream-partition}`; partition key must be stable and authorized. Producer's optional `stream_sequence` is separate metadata, not this cursor | Strictly increasing committed offset within one partition/epoch; no global total order promised | Missing producer sequence may be legal/out-of-order. A gap in Brain committed offsets is not silently skipped; filtered/inaccessible records do not imply absence. Retention may make an old range unavailable explicitly | Resume with opaque typed token (namespace, partition, epoch, exclusive after-offset); at-least-once replay; dedupe EventID. If retention expired, return CURSOR_EXPIRED / coverage gap, never pretend caught up | EventID/ReceiptID → compile intent → zero or more derivative proposals → canonical commit(s). Source time does not order commits |
| **Canonical commit cursor** `CanonicalCommitCursor` | D decides canonical semantics; Storage/Consistency implements durable ordering | Candidate: `brain.canonical-commit/{authority-epoch}/{partition}`; partition key and epoch rules require D + Storage approval | Strictly increasing committed offset per partition. No global order unless explicitly implemented and approved | Offsets are allocated/visible only on committed transactions; aborted attempts do not appear as committed positions. A gap in retained/replay range is explicit. Multi-partition snapshot is a vector, not max(offset) | Resume exclusive after typed partition offset; replay outbox/change feed at least once; idempotent by canonical Outbox/EventID. Expired history yields incomplete/blocked recovery, not guessed continuity | A commit references its source Event cursor(s), operation/idempotency key, aggregate revision(s), and Outbox EventID. Cursor is transaction visibility order within its partition, not truth-time order |
| **Per-aggregate revision** `AggregateRevision` | D for Memory/Claim/Entity/Relation canonical aggregates; exact aggregate semantics for Claim ADR remain blocked | `brain.aggregate/{aggregate-type}/{aggregate-id}` | Strictly increasing per aggregate; one committed head; immutable revisions; never compare across aggregates | A skipped revision is integrity/recovery error unless explicit migration/fork record explains it. Concurrent proposals use expected-parent CAS; rejected attempts do not consume committed revision numbers | Read exact revision or head; replay parent chain/outbox by immutable revision ID; no blind replay onto a changed head | Commit cursor orders commits in a partition; aggregate revision orders one object's history. One commit may affect multiple aggregates, so no 1:1 assumption |
| **LifecycleEvent cursor** `LifecycleEventCursor` | D owns append-only LifecycleEvent stream and lifecycle fold/projection | `brain.lifecycle/{memory-id}` (per-Memory aggregate); optional global lifecycle index is a derived consumer | Strictly increasing per Memory lifecycle stream; each event has immutable LifecycleEventID | No silent gaps in a complete per-Memory fold. Projection lag is represented by its own applied watermark. Missing event range blocks authoritative lifecycle reconstruction | Resume by MemoryID + exclusive lifecycle sequence; dedupe by LifecycleEventID; rebuild projection by ordered fold. If history is unavailable under Forget/retention, return explicit unavailable projection | LifecycleEvent may reference related MemoryVersion/CanonicalCommitCursor and ForgetOperationID. It is not interchangeable with MemoryVersion sequence or aggregate revision |
| **Per-index/per-partition publication watermark** `IndexPublicationWatermark` | Named index publisher owns its progress; E owns compiler publication intent, F owns retrieval freshness interpretation; Storage/Consistency owns shared progress substrate if applicable | `index/{index-name}/{schema-generation}/{source-partition}` | Monotonic contiguous applied prefix per index partition and schema generation. A separate sparse set/in-flight position may exist but is not the completeness watermark | Watermark N means every eligible source offset through N has been applied or explicitly accounted for (e.g. tombstoned/filtered with durable disposition). If N+1 applied before N, watermark stays N. Unknown source disposition is a gap | Resume from first offset after contiguous prefix; replay at least once by source EventID; rebuild creates a new schema generation and starts with explicit checkpoint. Old generation remains distinguishable | Must identify source namespace/partition/epoch and canonical commit fence represented. F compares required canonical cursor vector to observed watermark vector; cannot compare unrelated offsets |
| **Forget fence / epoch** `ForgetFenceEpoch` | D owns durable canonical ForgetOperation/fence record; I owns global authorization, retention and completion policy | Candidate scope: target typed object/family + affected ScopeRef set + policy domain; exact partition/epoch allocation needs D/I decision | Strictly increasing per fence namespace; never decreases or reuses epoch. Epoch change fences all work carrying older epoch | Epoch is not a cursor; gaps are allowed only as opaque monotonic generation jumps and do not represent missing events. Absence of an epoch value is not proof of no Forget | Consumers fetch current fence snapshot and subscribe/reconcile; stale cached epochs are rejected. Rebuild/replay must consult current fence before visibility. Offline consumer remains Unknown/blocked until refresh | A ForgetOperation installs suppression before cleanup. Every worker, index publication, cache read/write, Context reconciliation/delivery and Adapter application checks fence; target acknowledgements roll up into I policy completion |
| **Context version** `ContextVersion` | G | `brain.context/{context-id}` | Strictly increasing per Context only after atomic ChangeSet CAS; immutable version | No committed sequence gaps expected for successful commits; rejected/prepared ChangeSets have no target version. Concurrent base mismatch is Conflict, not hidden gap | Resume by ContextID + exact version/ChangeSet chain; rebuild from committed snapshots/audit/outbox. Never replay a ChangeSet onto a different head without replanning | Version pins canonical MemoryVersion refs and canonical watermark vector observed at commit. It is desired Context state, not evidence of delivery/application |
| **Delivery ID / sequence** `ContextDeliveryRef` + `DeliverySequence` | G owns Delivery record/ID and desired delivery sequence; H owns transport and Adapter-side receipt/attestation only | Candidate sequence namespace: `brain.delivery/{context-id}/{adapter-id}/{agent-context-session-id}` | DeliveryID immutable globally unique; sequence strictly increases within one Context+Adapter+AgentContextSession stream | Sequence gaps mean a delivery was superseded/cancelled/never dispatched only if explicit durable disposition exists; otherwise gap is unresolved. Duplicate sequence with different DeliveryID is integrity conflict | Retry same DeliveryID with same target payload; query by DeliveryID after timeout (Unknown). A new target/attempt requiring a new logical delivery gets new DeliveryID and next sequence | Delivery references ChangeSet/Base/Target ContextVersion, session, capability epoch and eventual InferenceRequestID. DeliverySequence is not ContextVersion or InferenceRequestID |
| **Adapter capability epoch** `AdapterCapabilityEpoch` | H (not yet present); C/Agent runtime supplies observed integration boundary | `adapter/{adapter-id}/{adapter-instance-or-session}` | Strictly increases whenever negotiated capability, adapter binary/config identity or observable inference boundary changes; monotonic per Adapter instance identity | Epoch discontinuity requires fresh capability negotiation; missing current epoch means capability Unknown. No claim is inherited from stale epoch | Re-negotiate on connect/reconnect/restart/config change; old attestation accepted only as historical evidence for the exact old epoch, never as current capability | Applied proof must include the exact capability epoch. Tier claims cannot exceed observable final-request boundary |
| **Inference request ID** `InferenceRequestID` | C/Agent inference runtime generates the request identity; H binds attestation to it; G records it | Agent-defined namespace, at minimum Agent + AgentInstance + Session (and provider/request namespace if needed) | Unique per actual inference submission; no numeric monotonicity required unless Agent runtime guarantees a sequence. Treat ID as opaque and immutable | Missing ID means final-request Applied cannot be proven at Tier 1; request retries/new submissions must not reuse ID unless the runtime defines them as the same actual request | Resolve by exact request ID and boundary attestation; no cursor resume semantics. Unknown/expired request evidence remains Unknown | Request is the final causal child of Delivery/application attempt; proof binds target ContextVersion + DeliveryID + capability epoch + actual submitted request/boundary |

## 3. Canonical commit cursor versus aggregate revision

D's branch currently describes both a monotonic canonical commit sequence and a per-Memory sequence, while explicitly leaving sequence partitioning open. D-REV-P1-002 is therefore still OPEN.

**CANDIDATE recommendation for owner review:**
1. Keep `AggregateRevision` as the authoritative per-object history number (MemoryVersion sequence; ClaimRevision only after INT-P0-01 ADR; equivalent Entity/Relation revision where owned).
2. Define `CanonicalCommitCursor` as a partitioned durable commit-log position allocated by Storage/Consistency under D's canonical semantics. Do not claim a global total order unless engineering selects a single global sequencer and demonstrates its transaction semantics.
3. Each canonical commit returns a cursor vector if it spans multiple partitions, plus exact aggregate revision IDs.
4. A consumer requiring a consistent multi-partition read uses a typed vector/fence or snapshot token. It must not take the maximum integer across partitions.
5. LifecycleEventCursor remains separate because LifecycleEvent is D's authoritative lifecycle transition stream; it can reference a canonical commit but is not the canonical commit cursor itself.

This is not a final choice: D + Storage/Consistency must approve the partition key, authority epoch, transaction visibility and recovery rules. If they choose a single global commit stream, it must still remain a distinct type and not replace aggregate revisions or LifecycleEvent cursors.

## 4. Causal chain and ordering

Expected causal chain (not a single total order):

`Producer observation`
→ `EventEnvelope`
→ `EventID + ReceiptID + SourceEventCursor` (E durable acceptance)
→ `CompileIntent / derivative registration`
→ `CanonicalCommitCursor + AggregateRevision(s) + OutboxEventID` (D canonical commit)
→ `LifecycleEventCursor` (if lifecycle transition occurs)
→ `IndexPublicationWatermark[index, partition]` (publisher applies source event)
→ `RetrievalResult freshness vector` (F)
→ `ContextChangeSet + ContextVersion` (G)
→ `DeliveryID + DeliverySequence` (G)
→ `AdapterCapabilityEpoch + InferenceRequestID + boundary attestation` (H/C)
  
Forget is an orthogonal monotonic fence/epoch that can invalidate any stage in flight. It is not appended as the next numeric item in the chain. A fence check must occur before each state-changing publication or visibility boundary; a stale worker cannot publish merely because it holds an earlier valid lease.

Causality is represented with immutable IDs and explicit parent/correlation/causation refs. Event time, ingestion time, valid time, commit time, publication time, delivery time and inference submission time are distinct clocks.

## 5. Consumer requirements and failure semantics

| Consumer | Must persist/observe | On gap/lag/epoch mismatch |
|---|---|---|
| D canonical store/lifecycle | Event references, expected aggregate head, canonical cursor, LifecycleEvent cursor, Forget fence | Reject stale CAS; rebuild projection from canonical append-only history; never infer lifecycle from stale projection |
| E compiler | SourceEventCursor, EventID, idempotency receipt, compile intent, current Forget fence | Resume from durable offset; at-least-once stage replay; suppress stale-fence work; explicit expired source range |
| F index/retrieval | Source/canonical cursor mapping and per-index watermark vector | Canonical read-through/bounded wait; else partial/stale/unavailable; no global top-k then post-filter; no index-only Forget guarantee |
| G Context reconciler | Canonical cursor vector, per-index watermark vector, Forget fence epoch, policy epoch, ContextVersion | Mark Stale/ReconcileRequired/Blocked; validate affected entries directly; do not infer absence from missing index results |
| H Adapter | DeliveryID/sequence, target ContextVersion, capability epoch, Forget/revocation epoch, InferenceRequestID | Timeout is Unknown; stale delivery/epoch rejected; reconnect requires re-auth, fence refresh and safe snapshot/clear |
| I governance | ForgetOperation/fence state, policy epoch, per-target progress and exceptions | Do not declare completion while required target is unknown/failed; reauthorize async/irreversible steps |

## 6. Required common envelope (semantic, not wire-format)

Every cross-boundary message should carry only the fields applicable to its operation, but must preserve:
- immutable message/event/operation ID and schema version;
- typed source cursor and/or typed target version (never generic `generation: u64`);
- typed partition/scope identity;
- ActorRef/producer identity resolved from authenticated transport (payload identity alone is not authority);
- correlation_id and causation_id;
- authorization/policy epoch where relevant;
- Forget fence epoch or explicit “not applicable” determined by policy, not caller omission;
- idempotency key and canonical request digest for state-changing operations;
- explicit observed/required watermark vector and completeness where projections are consumed.

H owns serialization and compatibility behavior. B/I own typed reference and authorization semantics. This section is a coordination requirement, not a BMCP schema.

## 7. Conformance scenarios (planned; none passed)

- Cursor tokens from two namespaces cannot be compared or substituted; API rejects type/namespace mismatch.
- Resume is exclusive and stable across retry; at-least-once duplicate replay is deduped by immutable source event ID.
- A producer-supplied sequence gap does not create a false Brain-ingress gap or imply missing Brain records.
- Canonical transaction crash before commit exposes no cursor; crash after commit returns the same receipt/cursor on idempotent retry.
- Per-aggregate CAS race allows one head advance; other proposal gets stale-parent conflict; aggregate revision never equals a global commit cursor by accidental reuse.
- Lifecycle projection replay yields the same fold; missing per-Memory event range is explicit.
- Index offset N+1 applied before N does not advance contiguous watermark past N-1.
- A Forget epoch increment blocks stale compiler lease, DLQ replay, index rebuild, cache fill, Context delivery and late Adapter Applied.
- Context version sequence is scoped to Context; Delivery sequence is scoped to its delivery stream; neither can be substituted for request ID.
- Adapter capability change increments epoch; old Tier 1 attestation cannot certify a new capability epoch.
- Missing or unobservable InferenceRequestID/final boundary produces Unknown/Partial, never Full Applied.

## 8. Open decisions / owner actions

| Question | Accountable owner | State |
|---|---|---|
| Canonical commit partition key, authority epoch and global-vs-partitioned order | D + Storage/Consistency (D accountable) | OPEN |
| Event cursor partition key and retention/replay horizon | E | CANDIDATE |
| LifecycleEvent retention and projection rebuild horizon | D + I | OPEN |
| Index watermark source mapping, schema generation and filtered disposition | E + index engineering (E accountable for publication contract) | OPEN |
| Forget fence namespace, epoch authority and producer barrier | D + I (I accountable for global policy) | OPEN |
| Context canonical watermark vector representation | G | CANDIDATE |
| Delivery sequence allocation/stream identity | G + H (G accountable for desired delivery record) | OPEN |
| Adapter capability epoch definition | H | OPEN |
| InferenceRequestID guarantee and final-request capture | C | OPEN |
| Storage transaction, outbox/WAL, partition failover and cursor durability | Storage/Consistency owner TBD | OPEN |

No test in this document is PASS. Performance, scalability, and physical-erasure guarantees are not assessed here.
