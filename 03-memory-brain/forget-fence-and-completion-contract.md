# Canonical Forget Fence and Completion Contract

**Owner:** Session D — Memory Brain Principal Architect  
**Status:** D canonical-domain semantics DECIDED; cross-module execution and global completion policy OPEN / I-owned.  
**Related:** D-REV-P1-001, D-REV-P1-003, INT-P0-02, INT-P0-03, INT-P1-03, INT-P1-06.

## 1. Purpose and authority

This contract defines the canonical authority boundary for Forget: durable operation identity, monotonic suppression fence, dependency inventory, producer admission/registration, barrier semantics, target acknowledgements and canonical-domain proof. It is a domain contract, not a wire/API schema.

- **D owns:** canonical ForgetOperation ID and state; affected canonical target references; durable ForgetFenceCursor/generation; dependency inventory authority; producer registration/barrier ledger; canonical target progress; canonical-domain suppression proof; lifecycle transition to Forgotten once I supplies the governing criterion.
- **I owns:** principal/authorization and revocation policy, permission epochs, retention, backup/external-copy rules, residual-exception approval, global completion policy and physical-erasure requirements. D cannot authorize itself or declare global/physical completion.
- **E owns:** compiler work queues/leases/retries/DLQ/replay and derivative publication enforcement.
- **F owns:** retrieval in-flight cancellation/finalization, candidate suppression, caches/Working Sets, index rebuild and per-index watermarks.
- **G owns:** Context snapshots/deltas/ChangeSets/delivery intents and Context reconciliation.
- **H owns:** BMCP wire, Adapter local state, offline reconnect and trustworthy application/clear acknowledgement.

D's references to module actions are mandatory boundary requirements, not an attempt to define their internal state machines, wire fields or implementation.

## 2. Vocabulary: three different outcomes

1. **Logical suppression:** covered canonical targets become unavailable to ordinary reads, candidate generation, reference resolution and new publication. It is enforced by the durable fence and is immediate at the canonical authority boundary. Suppression is not deletion.
2. **Asynchronous cleanup:** each derivative owner invalidates/removes/rebuilds/quarantines its own materializations and records a target-specific acknowledgement. Cleanup may be retried and may remain partial.
3. **Physical erasure:** irreversible removal from storage, backups, external recipients or provider-controlled systems under I's policy and evidence rules. D does not perform or prove it.

D's `CanonicalSuppressionComplete` means only that the D-defined closed-world producer barrier has drained and all required canonical-domain targets are suppressed or carry an explicit I-approved residual exception. It does not mean every module has physically deleted bytes, and it is not global Forget completion.

## 3. Durable identity and fence

Every accepted Forget request receives one opaque, durable `ForgetOperationId`. Client retries use a scoped idempotency key plus normalized request digest: same key/same digest returns the same operation; same key/different digest is an idempotency conflict. The operation records exact target TypedObjectRefs, target-set digest, ScopeRefs, requester ActorRef, I authorization-decision reference/policy version, reason, timestamps, dependency inventory ID, producer barrier metadata, per-target status and proof references. It stores no forgotten plaintext.

Fence installation is a canonical transaction. D allocates a strictly increasing `fence_generation` from the canonical Forget authority and persists:

- `ForgetFenceCursor = (forget_operation_id, fence_generation, target_set_digest)`;
- exact covered target identities and version families, including canonical descendants discovered later;
- effective suppression timestamp and canonical commit cursor of fence installation;
- idempotency receipt and recoverable outbox intent.

The generation never decreases, is never reused, and survives restart/restore. Overlapping Forget operations create later generations; the effective fence for a target is the greatest applicable generation. A fence applies to the target identity/version family and registered descendants, not merely to the exact payload revision observed at request time. A new Memory ID is not a way to re-import the same forgotten source or derivative lineage.

Every read/write/publication boundary evaluates the latest applicable fence against the target and its source lineage. A stale cached fence is insufficient: if the latest fence cannot be established, fail closed for affected targets. A worker's admission generation is evidence of what it observed, not a permanent authorization to publish.

## 4. Dependency inventory and producer registration

### 4.1 Closed-world producer registry

D maintains the canonical producer-class/registration ledger for all components permitted to create, transform, replay or publish derivatives of canonical targets. Each module owner registers its producer classes and work-admission boundary before that class can process data. Each individual work item registers durably before execution with:

- stable producer/work ID and producer class;
- source canonical refs and exact revisions/lineage;
- target ScopeRefs and operation/correlation IDs;
- admission CanonicalCommitCursor and observed ForgetFenceCursor/generation;
- lease/attempt identity and registration status.

Producer classes required by the current architecture include E compilation and replay, F retrieval/materialization and index rebuild, G Context reconciliation/snapshot/delta/delivery, and H Adapter delivery/reconnect. This is an inventory of producer boundaries, not a claim that D implements their workers.

No producer may start work, acquire a lease, enqueue a retry/DLQ replay or publish a derivative before its registration is durable. Queue insertion alone is not sufficient registration. Work registration is idempotent. A producer registration ledger gap or unknown producer class prevents the barrier from closing.

### 4.2 Fence snapshot and barrier

Fence installation atomically captures the current producer-registration high-water mark `producer_registration_barrier` together with the target inventory snapshot/watermark. This barrier includes every work item durably admitted before the fence transaction. Every such item must reach a durable terminal disposition before canonical suppression proof:

- committed/published before fence, with all resulting derivatives already registered and included in dependency inventory;
- cancelled/expired without publication;
- suppressed/quarantined by the fence;
- failed and durably parked with publication disabled pending explicit recovery.

A lease timeout is not an acknowledgement. Expired leases require owner recovery/reconciliation; the work item remains unresolved until terminal evidence is recorded. A producer cannot make itself disappear from the barrier by deleting a queue message or dropping a lease.

After fence installation, new work registration referencing a fenced target or its lineage is rejected, quarantined, or admitted only as a suppression/cleanup task. A new task cannot publish a derivative of a forgotten source merely because it carries the current generation. Its source lineage is re-evaluated against active and terminal fences. Producer classes must not have an unregistered side channel; if registry completeness cannot be established, the barrier remains open.

### 4.3 Register-before-visible rule

Every derivative must be registered with D's dependency inventory before it becomes visible to any consumer. The derivative record and dependency edge must be committed atomically, or an equivalent durable prepare/commit protocol must ensure that failure leaves the derivative invisible. The final publish/commit gate rechecks the latest applicable fence after any expensive processing and immediately before visibility. If a fence has advanced or covers any ancestor, the output is suppressed/quarantined and cannot enter canonical reads, indexes, caches, Context, delivery or inference input.

This rule closes the “scan completed, late output appears” race: a producer admitted before the fence is represented in the barrier; its output cannot become visible without a final fence check and prior dependency registration. A producer admitted after the fence cannot bypass the active fence. A post-fence discovery of an unregistered derivative is a barrier-integrity violation: immediately suppress it, reopen/invalidate any prior proof, record the producer-class defect and notify I/A; do not silently count it as already covered.

## 5. Target acknowledgement and completion proof

Each target acknowledgement is keyed by `(forget_operation_id, target_ref, target_owner, target_attempt)` and records:

- state: `discovered | suppression_requested | suppression_confirmed | cleanup_confirmed | failed | unknown | excepted`;
- target owner's stable acknowledgement ID and contract/capability version;
- observed ForgetFenceCursor/generation and exact target/ref digest;
- timestamp, retry/attempt, correlation/causation IDs and structured error;
- whether the acknowledgement covers active reads, queued work, in-flight work, caches, indexes, snapshots/deltas, delivery or local Adapter managed region.

Acknowledgement semantics are not interchangeable. `suppression_confirmed` proves the owner will not expose or newly publish the target under its stated boundary. `cleanup_confirmed` proves that owner's declared cleanup action completed. Neither proves physical erasure outside that owner's controlled domain. Unknown and timeout are not success. Acknowledgements are monotonic for a given attempt; retries cannot downgrade a confirmed suppression, but a later-discovered derivative creates a new target entry and invalidates the prior closed-world proof until reconciled.

D's canonical-domain proof MUST bind:

1. ForgetOperationId, normalized request digest, target-set digest and final fence generation;
2. fence installation CanonicalCommitCursor and exact affected canonical refs;
3. producer registry version and producer-registration barrier high-water mark;
4. evidence that every registered pre-fence work item is terminal and every derivative was registered before visibility;
5. dependency inventory snapshot and final reconciliation watermark/cursor;
6. per-target suppression acknowledgements or exact I-approved residual-exception references;
7. no unresolved producer registry gap, lease, retry, DLQ/replay item, publication gap or unknown required target;
8. canonical lifecycle event/ref if and when Memory transitions to Forgotten;
9. proof schema version, creation time and audit correlation.

The proof is immutable and non-reconstructive: it contains identifiers, digests, statuses and references, not forgotten content. It can prove only D's canonical-domain suppression boundary and the registered target acknowledgements it enumerates.

I's policy decides whether cleanup acknowledgements, offline Adapter acknowledgement, backups, external recipients or physical erasure are required for global completion. An exception is valid only when I supplies a durable policy-approved exception reference with target, scope, rationale, expiry/review condition and residual risk. D never invents or approves an exception.

## 6. Required race matrix and boundary requirements

| Race / subsystem | D canonical requirement | Owning module execution obligation | Failure outcome |
|---|---|---|---|
| E queued compiler work | Queue admission and work registration precede execution; fence inventory includes queued work | E checks fence before dequeue/lease and before canonical proposal/commit | Cancel/quarantine; keep barrier open until terminal |
| E leased/in-flight work | Lease/work ID is in pre-fence barrier; final publish gate rechecks fence | E checks after extraction/consolidation and immediately before derived registration/commit | Suppress output; register discovered target as blocked; no canonical visibility |
| E retry, retry scheduler, DLQ and replay | Every retry/replay is a registered work item linked to original source lineage | E carries original source refs/fence context; reauthorization and fence check on every retry/replay | Reject/quarantine stale replay; no retry can renew publication rights |
| F in-flight retrieval | Request/source refs and active execution are covered by producer registration | F rechecks fence before final candidate/result emission, not only at query start | Drop affected candidates; response marked incomplete/blocked as F defines |
| F cache / Working Set | Cache/materialization target is in dependency inventory | F checks fence on cache read and write; key/invalidation includes fence generation and scope/policy context | Cache miss/deny; stale entries cannot be returned |
| F index rebuild | Rebuild job and output generation are registered; IndexWatermark is not a Forget proof | F checks fence before segment publish/swap and candidate generation; rebuild from canonical snapshot plus replay | Do not publish stale segment; quarantine/rebuild; watermark cannot advance over unresolved commit gap |
| G Context snapshot / delta / ChangeSet | Context refs and pending changes are discoverable targets | G tombstones affected refs, invalidates snapshots/deltas and commits a new safe ContextVersion | Old immutable snapshot retained only as audit; never served as current |
| G Prepared / Delivered work | Pending deliveries are registered and bound to exact ContextVersion | G cancels/supersedes when possible and checks tombstone/fence immediately before delivery | Delivery stays pending/unknown/superseded; no late Applied promotion |
| H Adapter online delivery | Adapter/session is a registered derivative target; D does not define wire fields | H consumes fence/revocation and returns its owned acknowledgement | Suppress managed region; missing ACK remains unknown |
| H Adapter offline reconnect | Offline adapter remains an outstanding target; offline is not implicit success | H authenticates/reconciles latest fence, discards stale snapshots/deltas, applies safe state and attests before reuse | No cached Context reuse; remain unknown/blocked until H's criterion is met |
| Late Applied acknowledgement | A late ACK cannot override a newer fence or restore stale target | G/H reject stale target-version application for current state; preserve it only as historical evidence | Record late evidence; no resurrection or head rollback |
| Backup / external copy | Inventory/ack requirement is I-defined; D records discovered targets and references | I and designated owners enforce retention, backup and external-recipient policy | D cannot call physical deletion; global completion stays I-owned |
| Concurrent canonical write | Fence and write gate serialize against same target lineage | D checks latest fence in the canonical transaction at commit | Reject or quarantine write; no post-fence visible derivative |

## 7. Operation state and lifecycle separation

ForgetOperation state is not Memory lifecycle. D operation phases are Requested, FenceEstablished, InventoryOpen, BarrierDraining, TargetReconciliation, CanonicalSuppressionComplete, Blocked and Failed. The Memory lifecycle remains Candidate, Consolidated, Active, Superseded, Archived or Forgotten. “Forgetting” is not a Memory state. The lifecycle transition to Forgotten is appended only as a separate canonical lifecycle event when I's applicable policy criterion is met; the event itself is not physical-erasure evidence.

## 8. Interfaces, failure, idempotency and observability

- **Producer registration contract:** owner D; producers E/F/G/H; consumer D dependency/barrier ledger and I completion evaluator. Stable work ID, source refs/revisions, ScopeRefs and observed fence are required. Retry preserves work identity/lineage or creates a linked attempt; no untracked replay.
- **Target acknowledgement contract:** owner D defines domain meaning; E/F/G/H produce owner-specific evidence; I determines required target classes and exception policy. Same acknowledgement ID/digest is idempotent; conflicting evidence is rejected and audited.
- **Failure behavior:** fail closed for affected target if latest fence is unavailable; unknown target/producer/lease/gap blocks barrier closure. Partial work is resumable. Never convert timeout to success.
- **Observability:** operation ID, fence generation, target-set digest, producer registration high-water, open work count, dependency inventory cursor, target state counts, late derivative count, barrier age, blocked reason and correlation/causation. Do not log forgotten payloads.

## 9. Conformance tests (design acceptance; not yet executed)

1. Forget races with a canonical write: exactly one serialization order wins; if fence wins, write is rejected; if write wins, derivative is registered and included in the barrier.
2. Queued, leased, retry, DLQ and replayed compiler work cannot publish after fence; all are visible in the registration ledger.
3. A delayed compiler output whose extraction completes after the fence is quarantined before registration/visibility and cannot create a new readable canonical asset.
4. Runtime in-flight result and cache hit are suppressed by a fence installed after query start but before response finalization.
5. Index rebuild cannot swap a stale segment after fence; its watermark does not imply suppression or cleanup.
6. G snapshot/delta and Prepared/Delivered Context cannot be re-applied after fence; late Applied evidence cannot reactivate it.
7. Offline Adapter reconnect must reconcile latest fence before using cached Context; no acknowledgement means unknown.
8. A producer registration gap, expired un-recovered lease, unknown target or missing acknowledgement prevents barrier closure.
9. A post-fence attempt to register a derivative from a forgotten ancestor is rejected/quarantined even if it presents the latest generation.
10. Duplicate Forget request returns same operation; same idempotency key with different target digest conflicts.
11. A late unregistered derivative invalidates a prior proof and reopens reconciliation; no silent success.
12. Proof includes no forgotten plaintext and does not claim backup/provider physical erasure.

**Acceptance status:** semantics specified; implementation conformance, I policy approval and E/F/G/H enforcement evidence remain OPEN. This document does not close INT-P0-03 globally.


## 10. Phase 3.5 operation-level atomicity contract

The operation-level contract in [forget-fence-operation-and-publication-gate.md](forget-fence-operation-and-publication-gate.md) is normative for the D semantics of CR-P1-01 / D-REV-P1-003. It refines, and does not weaken, §§3–9 above.

The normative operations are RegisterProducerClass, RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. Their inputs, outputs, idempotency keys, error outcomes and linearization points are specified in the operation contract.

### 10.1 Mandatory serialization rule

RegisterProducerWork and InstallForgetFence must share one linearizable ordering domain. If registration commits first, its ProducerRegistrationSequence is at or below the immutable high-water captured by the fence and the work is included in the barrier. If fence installation commits first, ordinary derivative admission for a covered source is rejected/quarantined or explicitly cleanup-only. An accepted-but-uncaptured work item that can publish is forbidden.

### 10.2 Mandatory visibility rule

Dependency registration is durable before visibility. PublishDerivedIfFenceCurrent validates the complete dependency set, work/attempt identity, latest applicable ForgetFence, and I's current PermissionEpoch at the same externally observable atomic/linearizable boundary that changes the artifact from private to visible. An independent check-then-write or uncoordinated gate token is insufficient. Ambiguous outcomes remain private until ResolveProducerWork establishes the committed result.

### 10.3 Evidence and type separation

Publication evidence binds WorkItemId/AttemptId, ProducerClass, source MemoryVersion/Revision, ScopeRefs, RegistrationReceipt, observed and authoritative ForgetFenceCursor, PermissionEpoch and I decision reference, DerivedArtifact identity, and every DependencyRegistrationReceipt. ForgetFenceGeneration and PermissionEpoch are distinct typed namespaces and must never be numerically compared or mixed.

### 10.4 Status

D operation semantics and required race outcomes are DECIDED as a domain contract. E mapping, I authorization decision semantics, global producer inventory completeness and Storage/Consistency realization remain OPEN. No Storage/Consistency Owner was established in the reviewed package; this is an explicit OPEN ownership gap. Design conformance cases are specified but NOT RUN. This section does not close INT-P0-03 or assert end-to-end Forget completion.


---

## Phase 3.6 normative addendum — atomicity boundary

The D-owned operation-level Phase 3.6 linearization, Producer Work state machine, Fence/Permission dual-validation rules, implementation-neutral Storage semantic requirements, 12-case Fault/Race Proof Matrix and D/E/Storage OPEN Decision Register are specified normatively in [forget-fence-operation-and-publication-gate.md](forget-fence-operation-and-publication-gate.md), **Phase 3.6 — Forget Fence Linearization & Atomicity Semantics**.

The unique safety invariant is: no derivative may become retrievable, deliverable, indexable, inferable or otherwise visible unless its logical Producer Work is durably registered and accounted for by every applicable Forget barrier, its complete dependency lineage is durable, and the final visibility commit validates the latest applicable D ForgetFence and current I authorization/PermissionEpoch for the authenticated Principal and exact Scope. Unknown or stale evidence is non-visible.

Work Registration, Barrier Capture, Dependency Registration, Staging, Publish Authorization, Durable Commit, Artifact Visibility and Terminal Disposition are separate evidence-bearing stages. Barrier capture accounts for pre-fence work; it is not publication permission. Lease expiry, queue deletion, retry delay and DLQ parking do not terminalize work.

D defines domain semantics and observable ordering only. Storage may choose any realization that proves the same linearization and crash-recovery behavior; this addendum does not approve a database or claim implementation. **CR-P1-01 remains OPEN pending E + Storage joint confirmation and executable evidence.**
