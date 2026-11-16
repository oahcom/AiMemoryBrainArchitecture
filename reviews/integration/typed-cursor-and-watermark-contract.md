# Typed Cursor, Revision, Fence and Capability Registry — Phase 3.5

- Owner: Session A / Principal Integration Architect
- Status: **CANDIDATE coordination registry**; not a schema freeze or implementation guarantee.
- Updated: 2026-11-16 against freshly queried A/B/C/D/E/F/G/H/I/Storage branch HEADs.
- Authority: each token's named owner alone defines its semantics. A records the contract and prohibited cross-namespace operations.

## 1. Global hard rules

1. Every token is typed and namespaced. Preserve its type discriminator, issuing authority, scope, schema/version and provenance.
2. Never compare raw numeric values, cast, increment, subtract, max, sort or substitute values from different namespaces.
3. A consumer may order/validate a token only through its owner-defined operation and only within the exact declared scope.
4. Cross-stream causality is represented by typed references, receipts or a vector of independently validated evidence, never by scalar coercion.
5. A token is not proof of a different subsystem's work. Cursor progress is not Forget completion; ContextVersion is not Applied; AdapterCapabilityEpoch is not authorization.
6. Owner decision and implementation are distinct. D's CanonicalCommitCursor semantics are DECIDED; Storage realization and consumer conformance remain OPEN.

## 2. Normative typed registry

| Token | Owner | Namespace / scope | Ordering semantics | Consumers | Forbidden comparisons / conversions |
|---|---|---|---|---|---|
| **CanonicalCommitCursor** | D | One globally ordered sequence per Canonical Memory Authority (Brain authority). Identity includes authority + committed sequence. | D-defined total order within one authority; contiguous committed sequence. A gap blocks contiguous consumer advancement. Multiple authorities have independent sequences; no cross-authority total order. | E stores exact D-issued value; F consumes as canonical source position and IndexWatermark applied-through; G uses only where D supplies causal source references; Storage realizes sequencing; H transports opaquely; I may bind as evidence. | Never compare across authorities or with AggregateRevision, LifecycleEventCursor, IndexWatermark as an independent counter, ProducerRegistrationSequence, ForgetFenceGeneration, PermissionEpoch, ContextVersion or AdapterCapabilityEpoch. Never synthesize or allocate in a consumer. |
| **AggregateRevision** | D | One aggregate identity (Memory/Entity/Relation aggregate). | Monotonic immutable revision order only within the same aggregate. A committed revision references its CanonicalCommitCursor. | E records exact revisions; F/G pin exact canonical versions; Storage persists aggregate head/revision. | No cross-aggregate ordering; not a global commit cursor, lifecycle cursor, watermark, fence or policy epoch. |
| **LifecycleEventCursor** | D | One Memory identity's append-only lifecycle event stream. | Contiguous event sequence within that Memory; each event separately references enclosing CanonicalCommitCursor. | E/F/G consume lifecycle change evidence; Storage persists lifecycle append; I may use as evidence. | Not AggregateRevision or CanonicalCommitCursor; never compare across Memory identities or infer global ordering. |
| **IndexWatermark** | F | One named index + channel/partition + coverage/schema version. It carries an applied-through CanonicalCommitCursor from D. | F advances only the contiguous prefix of canonical commits fully accounted for by that exact partition, including explicit irrelevant/no-op coverage. Gaps stop advancement. A multi-partition index is a vector/map, not one scalar. | F owns and advances; G consumes freshness/completeness; A records; I may consume per-target evidence. | Do not compare watermarks across unrelated partitions as one scalar. Do not treat it as CanonicalCommitCursor, target absence, cache purge, suppression, Context reconciliation, Forget completion or physical erasure. |
| **ForgetFenceGeneration / ForgetFenceCursor** | D | D Forget authority; typed cursor tuple binds ForgetOperationId + generation + target-set digest / applicable lineage. | D generation monotonically advances in the fence namespace. Currentness/coverage is evaluated by D for exact target lineage and operation; installation also has a separate CanonicalCommitCursor for audit order. | D enforces; E/F/G/H consume; I validates global proof references; Storage persists. | Never compare or convert to CanonicalCommitCursor, ProducerRegistrationHighWater, AggregateRevision, LifecycleEventCursor, IndexWatermark, PermissionEpoch, ContextVersion or AdapterCapabilityEpoch. A current generation does not authorize a forgotten ancestor. |
| **PermissionEpoch** | I | Named issuer/policy domain (and its declared subject/resource policy scope). | Opaque policy generation. Currentness, revocation and continuity are validated only under I's same-domain rules; no universal global scalar order is assumed. | D/E/F/G/H/C validate current authorization at protected boundaries; Storage binds decision evidence; A records. | Never compare numerically with ForgetFenceGeneration, ProducerDomainInventoryEpoch, cursors, ContextVersion or CapabilityEpoch. Not a lease, grant or proof absent an I decision. |
| **ProducerDomainInventoryEpoch** | I | Global Producer/Recipient Domain Inventory catalogue, including classes/instances, owners, scopes, capabilities, recipients and backup/restore routes. | I-owned inventory generation changes when membership/coverage/capability/owner/route/evidence obligations change. A seal binds exact epoch + inventory digest; relevant changes reopen the seal. | I global Forget evaluator; D/E/F/G/H/Storage provide local target/work evidence; A coordinates. | Never substitute for D ProducerRegistryVersion or per-Forget ProducerRegistrationHighWater. Not a work-item sequence, canonical cursor or permission epoch. |
| **ContextVersion** | G | One Context identity; immutable desired Context versions with explicit base/target and one authoritative head. | G-defined monotonic version sequence within that Context; ChangeSet commits atomically against exact Base Version (CAS/serialization). | G owns; H transports delivery target; C validates exact version in final Applied proof; F may carry as advisory correlation only; I evaluates policy separately. | Never compare across Context identities or with canonical revisions/cursors, delivery sequence, PermissionEpoch, ForgetFenceGeneration or CapabilityEpoch. Does not prove Delivered, Applied or execution. |
| **AdapterCapabilityEpoch** | H | One registered Adapter instance/capability profile. | H-owned opaque epoch changes when implementation/configuration/capability proof coverage changes. Negotiated and validated for the exact Adapter instance/session. | H owns; C binds the epoch in final-request Applied evidence; G validates delivery/ACK compatibility; I uses it for target/action evidence. | Never compare across Adapter instances or with ContextVersion, PermissionEpoch, ForgetFenceGeneration, CanonicalCommitCursor or Delivery ID. It is not identity authentication or permission. |

## 3. Supporting typed evidence (not substitutes for the nine registry tokens)

| Type | Owner / scope | Semantics | Consumer rule / prohibited substitution |
|---|---|---|---|
| ProducerRegistryVersion | D; producer-class registry | Immutable version of registered producer classes and enabled/disabled status. | Work admission must observe an enabled registered class. Not I's global ProducerDomainInventoryEpoch. |
| ProducerRegistrationSequence / ProducerRegistrationHighWater | D; per-authority producer-work ledger and one ForgetOperation barrier | Monotonic work-admission sequence; fence captures immutable high-water. | Compare/membership only under D ledger rules. Not CanonicalCommitCursor or I inventory epoch. |
| SourceEventCursor | E; declared ingress stream/partition | Durable accepted-source position. Producer-supplied source sequence remains separate metadata. | E ingress/replay only; never canonical commit or index watermark. |
| DeliveryId / DeliveryAttemptId | G; logical delivery and its attempt | Stable delivery identity and per-attempt identity. | Correlation/idempotency only; no canonical or ContextVersion ordering inference. |
| InferenceRequestId / FinalRequestBoundaryId | C/runtime evidence domain | Identifies exact final inference submission and observable boundary. | Required in Full Applied evidence; not proof by itself and not a cursor. |
| RegistrationReceipt / DependencyRegistrationReceipt / PublicationReceipt | D; operation-specific durable receipts | Evidence of exact admission, dependency registration or visibility-gate outcome. | Resolve by stable ID + request digest; receipt types are not interchangeable and do not imply terminal work/global Forget. |
| TargetInventorySeal / ForgetCompletionVector | I; one Forget operation + sealed target inventory | Typed vector of target/action states and module-owned proofs at a named inventory epoch. | Every mandatory target must be evaluated. Never collapse to one scalar or infer from D barrier alone. |

## 4. Cross-module use constraints

### D → E/F/G/Storage
- D's selected CanonicalCommitCursor is one global sequence per Canonical Memory Authority, not partitioned by aggregate or index.
- E stores the D-issued cursor unchanged. E SourceEventCursor remains separate.
- F's IndexWatermark is partition-local and records a contiguous applied-through canonical cursor.
- G uses exact immutable MemoryVersion references and maintains its own ContextVersion.
- Storage must prove uniqueness, atomic visibility, crash/failover/recovery and contiguous replay for D's per-authority sequence.

### Forget and authorization
- ForgetFenceGeneration is a fencing namespace; ProducerRegistrationHighWater is an admission ledger position; PermissionEpoch is a policy-domain generation; ProducerDomainInventoryEpoch is a global inventory generation.
- A Forget completion proof must reconcile both I's sealed global inventory and D's per-operation work barrier, plus F/G/H and external/backup evidence as I policy requires.
- No consumer may use “larger number wins” across these namespaces.

### Context and Applied
- ContextVersion identifies G's immutable desired target. Delivery and Adapter ACK are separate.
- Full Applied must bind the exact ContextVersion, Delivery/attempt, final InferenceRequestId/boundary, AdapterCapabilityEpoch, current PermissionEpoch and applicable D ForgetFence, plus identity/scope and integrity evidence.
- Prepared, Delivered, materialized, final-request Submitted and Execution Started are distinct events. No cursor/epoch alone promotes a delivery to Applied.

## 5. Validation and conformance status

| Validation | Required proof | Status at this review |
|---|---|---|
| D per-authority CanonicalCommitCursor semantics | D owner artifact explicitly chooses single total order per authority | **DECIDED by D** |
| Storage sequence realization | concurrent commit, atomic cursor/transaction/outbox, crash/failover/restore and gap tests | **OPEN / NOT RUN** |
| E/F/G cursor consumption | each consumer preserves type, scope, gaps, duplicate/replay and partition semantics | **Partially specified; cross-consumer conformance OPEN / NOT RUN** |
| Fence vs registration vs PermissionEpoch | type-check/negative tests reject namespace mixups and stale authorization | **Specified; NOT RUN** |
| I inventory epoch vs D work barrier | sealed global inventory and per-operation barrier reconcile independently | **Specified as distinct; owner approval and execution OPEN** |
| ContextVersion / AdapterCapabilityEpoch | exact delivery and final-request evidence, stale/late ACK behavior | **Specified; cross-owner approval and execution OPEN** |

This registry records D's owner decision without claiming Storage or consumer implementation. It does not close CR-P1-01, CR-P1-02, INT-P0-02, INT-P0-03, INT-X-01, INT-X-04 or INT-X-07.


---

## Phase 3.6 closure reconciliation — 2026-11-16

The Phase 3.5 token semantics above remain the controlling typed-namespace baseline. The following Phase 3.6 closure facts are added without changing any token owner or semantic meaning.

### 1. Current source baseline

Current branch tips: A `9c3dafb97b97aee50a8b61fe60836ed0a8e92fe3`; B `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f`; C `3b6c1d9a5d648f61daa04f5874d887f33475f098`; D `968ce314cf2e44f50e3efd711060e495374cac98`; E `e3afa99728f399d154767c959e37ff38f651b4b6`; F `2da5209d7072272d5510d376c0f319bed0402a6f`; G `ac32e980003aa41faf0ae958ffef3df5ab387984`; H `59926f5090dfd2e2ad78d9c25d0bd9062b4bcabc`; I `6a92f49bd740f6e2db11568d9bd61e8c58132cbc`; Storage `c0d01d81698fa6bc2a22e84b0e2ada66ce329815`.

### 2. Typed namespace closure requirements

| Namespace / receipt | Phase 3.6 closure owner | Required reconciliation | Current status |
|---|---|---|---|
| `PermissionEpoch` / `AuthorizationCommitPermit` | I | Named policy domain, currentness/revocation ordering, single-use commit receipt and approval/effective policy version | Contract specified; governance and consumer integration OPEN |
| `ProducerDomainInventoryEpoch` / `InventorySealReceipt` | I | Closed-world producer/recipient/backup inventory, authenticated member enumeration, digest and seal; D validates reference but cannot manufacture it | Contract specified; inventory owner I; operational seal not supplied |
| `ProducerRegistryVersion` / `ProducerRegistrationHighWater` | D | D-local class registry and per-Forget work admission barrier remain distinct from I global inventory | D semantics decided; implementation NOT VERIFIED |
| `ForgetFenceGeneration` / `FenceSnapshotReceipt` | D | Bind D barrier snapshot and current inventory seal; fence remains separate from PermissionEpoch | D semantics decided; implementation NOT VERIFIED |
| `CanonicalCommitCursor` | D | One ordered sequence per Canonical Memory authority; Storage proves sequence/transaction/recovery continuity | D decision recorded; Storage realization NOT VERIFIED |
| `IndexWatermark` | F | Partition-local contiguous accounted-through D cursor; gaps cannot be skipped | F semantics decided; tests NOT RUN |
| `ContextVersion` / DeliveryId / DeliveryAttemptId | G | Exact immutable target and attempt; no scalar applied_version substitution | G semantics decided; Applied freeze blocked |
| `AdapterCapabilityEpoch` / ACK evidence | H | Exact Adapter instance/session/capability and action/region evidence; ACK is not Applied by itself | H technical baseline decided; governance/consumer acceptance open |
| `InferenceRequestId` / `FinalRequestBoundaryId` | C | Exact immutable request and observable final submit boundary | C semantic contract delivered; C/G/H freeze blocked |

### 3. No implicit ordering or approval

- I's global inventory epoch is not D's per-Forget work high-water.
- I's PermissionEpoch is not D's ForgetFenceGeneration, F's IndexWatermark, G's ContextVersion or H's AdapterCapabilityEpoch.
- A receipt proves only the operation and authority named by its type; RegistrationReceipt, DependencyRegistrationReceipt, PublicationReceipt, InventorySealReceipt and AuthorizationCommitPermit are not interchangeable.
- The DE-S design self-review is closed after two zero-finding rounds; physical storage implementation and I integration remain open.
- BIH36-JD-01..17 are a delegated joint technical baseline; governance and consumer acceptance are separate gates.
- C/G/H do not share a pinned Applied schema/version or common approval record; Applied Contract Frozen remains NO.
- Typed-cursor and cross-namespace conformance tests remain NOT RUN. No test result is implied by this registry.
