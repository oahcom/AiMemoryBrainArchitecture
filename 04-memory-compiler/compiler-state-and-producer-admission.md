# Compiler State Machine and D Producer Admission Interface

**Status:** CANDIDATE E state/adapter contract; D API schema and D/E/Storage linearization remain OPEN.
**Owner:** Session E — Memory Compiler.
**Authority boundary:** E owns compiler-internal work/attempt/stage state. D owns Producer Registration ledger, Forget barrier and canonical gate semantics. I owns authorization/PermissionEpoch and global Forget policy. H owns authenticated transport binding. Storage owns physical transaction/visibility realization only when explicitly agreed.

## 1. Identity hierarchy

| Identity | Stability | Meaning |
|---|---|---|
| EventRef | Immutable | One accepted source event |
| AcceptedReceiptId | Immutable | E evidence of durable ingress |
| CompileIntentId | Stable across retries | Logical compilation intent |
| ProducerWorkItemId | Stable across retries of one logical work | D-visible producer registration/barrier identity |
| DerivationRunId | One run; new for recompile | Specific compiler/model/schema execution lineage |
| AttemptId | New for each attempt | Retry/worker execution attempt |
| LeaseId | New for each lease | Time-bounded worker ownership |
| DerivedArtifactRef/version | Immutable per output version | Private staged derivative identity |
| DependencyRegistrationId | Stable idempotency key | D dependency-registration reconciliation |
| PublicationOperationId | Stable idempotency key | Final gate/visibility reconciliation |

IDs are opaque and allocated durably. Payload-supplied IDs are never trusted as authority. A recompile creates a new DerivationRunId and fresh authorization/fence checks; whether D requires a new ProducerWorkItemId or a child registration under the original item is an OPEN D interface decision. It may never bypass the original source lineage or barrier.

## 2. State transitions

```text
Received
  -> Validating
  -> Accepted
  -> D_Registration_Pending
  -> Registered
  -> Queued
  -> Leased
  -> Running
  -> Staged
  -> Dependency_Registration_Pending
  -> DependencyRegistered
  -> Publication_Gate_Pending
  -> Published
  -> Terminal
```

Alternative exits:
- Validating -> Rejected (no Accepted receipt; unless a durable policy-safe rejection receipt is separately defined).
- Accepted / Queued / Leased / Running / Staged -> Cancelled or Suppressed, then Terminal after durable no-publication evidence.
- Running / Staged / dependency pending -> Retry, then Queued with same ProducerWorkItemId and a new AttemptId after fresh authorization/fence checks.
- Retry budget exhausted -> DeadLettered; this is **not terminal** while replay remains possible.
- D canonical write -> CanonicalCommitted is a separate result/evidence axis, not an alias for Published.
- LeaseExpired is an operational condition; it invalidates that lease but does not terminate the work item or remove it from D's barrier.

## 3. Admission and barrier mapping

| E event/state | Required D ledger meaning |
|---|---|
| Accepted | No D admission implied |
| D_Registration_Pending | Request may have committed; E must resolve by stable ProducerWorkItemId/digest |
| Registered | D Registration Receipt exists; barrier high-water/registration identity is durable |
| Queued / Retry / DeadLettered | Same D registration remains open; retry/DLQ does not disappear from barrier |
| Leased / LeaseExpired | D can correlate active/expired LeaseId + AttemptId; expiration is not terminal |
| Running / Staged | D registration remains open; E progress is telemetry, not barrier completion |
| DependencyRegistered | D dependency inventory has every required direct/transitive edge receipt |
| Published / CanonicalCommitted | Durable gate and/or canonical commit evidence recorded independently |
| Cancelled / Rejected / Terminal | E sends durable terminal disposition; D closes barrier item only after validating evidence and no further publication is possible |

D's Forget contract requires every work item admitted before the fence's producer-registration high-water mark to reach a durable terminal disposition. E must never delete a registration, hide a DLQ item or treat a lost worker as completed.

## 4. Required D operation semantics (not API names)

### 4.1 Producer registration

E needs a D operation that durably registers the logical producer work before enqueue or execution. Minimum semantic request fields:

- ProducerWorkItemId, producer class and authenticated ProducerIdentity binding;
- source EventRef(s), and canonical source refs/exact versions when available;
- source/transitive lineage digest or approved opaque dependency token;
- ScopeRefs and security-domain binding;
- operation, correlation and causation IDs;
- admission CanonicalCommitCursor (D-issued current authority position, or an explicit D-defined genesis/empty value if no canonical commit has occurred);
- observed ForgetFenceCursor and I PermissionEpoch;
- request digest, initial AttemptId/LeaseId if applicable, and producer schema/version.

Minimum result: durable ProducerRegistrationReceipt, registration ledger sequence/high-water token and accepted/rejected disposition. Receipt lookup by ProducerWorkItemId + digest must be idempotent.

**OPEN:** D must define how EventRef-only ingress registers before any canonical MemoryRef exists, and whether one logical work item or each attempt/recompile is a separate ledger entry.

### 4.2 Dependency registration

E needs a D operation to durably register each DerivedArtifactRef/version and complete source ancestry before visibility. Minimum request: artifact ref/version, ProducerWorkItemId, DerivationRunId, direct and transitive source refs or I-approved opaque tokens, exact source versions, ProvenanceRef, ScopeRefs, lineage digest, observed fence and idempotency identity. Result: durable DerivedRegistrationReceipt and inventory position.

Duplicate same-key/same-digest registration returns the original receipt. Same key/different digest conflicts. Partial registration remains non-visible. D must define source-reference classes and whether D or a D-designated inventory service is authoritative.

### 4.3 Final Publication Gate

E needs a final D-authoritative gate that checks the latest ForgetFenceCursor and registration inventory, and serializes the result against concurrent fence installation. Minimum request: PublicationOperationId, artifact/version, ProducerWorkItemId, DerivationRunId, AttemptId/LeaseId, all dependency receipt IDs, current PermissionEpoch/authorization decision ref, observed ForgetFenceCursor, ScopeRefs and request digest.

The result must be a durable PublicationReceipt bound to exact artifact/version, dependency receipts, fence generation, permission epoch and visibility outcome. Storage must not expose the artifact until the gate's committed success is proven.

**OPEN:** D must define whether the gate itself performs the visibility transition, or issues a single-use fencing token consumed by Storage under a shared transaction/CAS. A token followed by an uncoordinated write is not sufficient.

## 5. Failure semantics

- Admission ACK loss: query same work ID; never enqueue while unknown.
- Worker crash/lease expiry: D registration stays open; new attempt must refresh permission/fence.
- Dependency ACK loss: query stable dependency key; artifact stays private.
- Partial dependency writes: resume idempotently; no partial publication.
- Publication ACK loss: artifact stays private until lookup proves commit.
- Fence or PermissionEpoch advances: stale lease/attempt rejected; no generation refresh can legitimize the same stale result.
- DLQ: barrier-open until explicit terminal acknowledgement or authorized replay.
- Late result: discard/quarantine; cannot overwrite a newer or terminal state.
- Restore: apply current fence before any staging or derived object is made queryable.

## 6. Observability

Required telemetry: EventRef, AcceptedReceiptId, CompileIntentId, ProducerWorkItemId, DerivationRunId, AttemptId, LeaseId, D registration receipt/high-water, DependencyRegistrationIds, PublicationOperationId/Receipt, observed CanonicalCommitCursor, AggregateRevision refs, LifecycleEventCursor, ForgetFenceCursor, PermissionEpoch, state transition, retry count, terminal disposition, correlation/causation IDs and structured failure class. Never log forgotten content or sensitive locators.

## 7. Conformance cases (NOT RUN)

- D registration precedes queue/lease; admission timeout blocks execution.
- Fence install races registration and exactly one serialized outcome wins.
- D barrier includes queue pending, leased, expired, retry, DLQ and replay.
- Lease expiry cannot be counted terminal.
- Dependency registration must be complete before final gate.
- Fence/permission changes between staging and gate reject publication.
- ACK loss at each boundary resolves to the same receipt.
- Recompile creates new provenance/run identity and cannot bypass source fence.
- Late result cannot publish after terminal/cancel.
- D and E state transitions reconcile after crash/restore.

**No runtime interface or implementation is claimed by this document.**
