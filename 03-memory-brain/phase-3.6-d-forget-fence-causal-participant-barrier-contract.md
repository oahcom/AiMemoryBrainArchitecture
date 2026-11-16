# D Owner Contract Addendum — ForgetFence Participant Barrier and C-submit Causal Ordering

- Owner: Session D — Memory Brain / ForgetFence / lineage
- Branch: `session-d-memory-brain-2026-11-16`
- Target profile: `CausalOrderProfile/1.0`
- Target H schema: `bmcp.applied-ack/1.1.0`
- Target common package: `CGH-APPLIED-1.1` (proposed successor; not cross-owner frozen)
- Status: **D-SIDE FENCE/BARRIER CONTRACT SPECIFIED; coordinator/Storage deployment and cross-owner acceptance OPEN**.

## 1. D remains Forget authority

D alone issues ForgetOperationRef, ForgetFenceRef/ForgetFenceGeneration, target/source/ancestor lineage coverage and D-local barrier disposition. Coordinator positions do not mint or replace D fence generations, lineage truth or D completion.

## 2. Participant registration before external submit

Before C invokes a provider/runtime submit side effect, the exact operation MUST be durably registered as a participant against:
- ForgetOperation/target and all applicable source/ancestor lineage;
- CausalOrderProfileRef, CausalOrderCoordinatorRef and CausalOrderTransactionRef;
- ParticipantIntentRef (durable pre-side-effect intent; D's barrier is registered against this intent);
- exact request/ManagedRegion digest, ContextVersion, DeliveryId/attempt, FinalRequestBoundaryId;
- I CommitAuthorizationReceiptRef and PolicyDomainRef/PermissionEpoch;
- authenticated C workload/instance/session and applicable Scope/Environment.

D returns a signed DParticipantClearanceRef only after verifying the participant is included in the current fence/barrier accounting and no earlier effective fence suppresses it.

## 2.1 Fence-request causal cutoff

Every ForgetFence request affecting this target/lineage MUST be durably recorded with the common coordinator and carry an immutable DForgetFenceRequestRef plus coordinator request position. D remains the sole authority that commits the effective ForgetFenceGeneration and barrier terminality.

- Fence request position before ParticipantIntentRef: D rejects the later intent as FENCE_WON immediately, even if the fence's effective commit is waiting for earlier participants.
- ParticipantIntentRef before fence request: D keeps that participant in the barrier; the fence request remains pending until exact submit outcome or safe abort is terminal, then D commits the effective fence point.
- D terminal evidence binds both request cutoff position and effective fence position; these must not be conflated.
- No new affected participant may be admitted after the fence request cutoff.

## 3. Fence installation and terminality

- A fence request is durably recorded in the coordinator/D authoritative barrier before it becomes effective. Its request position establishes the admission cutoff: any ParticipantIntentRef ordered after the fence request is rejected as FENCE_WON even while the fence is waiting for earlier participants to drain.
- If a ParticipantIntentRef is ordered before the fence request, D MUST keep the fence barrier open until that participant has a durable C submit outcome and compatible I terminal evidence, or a safe abort is durably established. Only then may D commit the fence's effective position.
- D terminal evidence carries both the fence-request position/cutoff and the eventual fence-effective position; these are not interchangeable.
- A participant cannot be dropped because of process death, timeout, lease expiry, queue deletion, DLQ movement, worker replacement, coordinator disconnection or lost ACK.
- If provider outcome is unknown, participant state is IN_DOUBT and fence effectiveness/completion remains blocked. Recovery must reconcile the same transaction/reservation and provider idempotency identity.
- If the fence is effective before ParticipantIntentRef, D returns FENCE_WON and C cannot submit.
- If the participant safely aborts before provider side effect, D may clear it only with immutable terminal abort evidence.
- A successful submit proven before a later fence remains a historical event requiring the normal Forget reconciliation; it is not eligible for subsequent current use.

## 4. Lineage and multi-source correctness

DParticipantClearanceRef binds ParticipantIntentRef plus complete target and source/ancestor lineage coverage and the exact lineage inventory version. Any missing, late-discovered or changed dependency invalidates clearance and forces reconciliation. D does not infer global producer inventory completeness, TargetInventorySeal or Global Forget completion from local participant drainage.

## 5. Authority separation

I independently decides authorization and revocation; D independently decides ForgetFence and lineage; C alone observes the actual submit boundary; coordinator only supplies common durable ordering and participant barrier state; H only transports evidence; G alone decides Applied/current-use. None may substitute its token or sequence for another's.

## 6. Failure behavior

Missing coordinator, unavailable I, unknown C outcome, incomplete lineage, stale fence, coordinator rollback, conflicting digest or contradictory owner terminal evidence => UNKNOWN/IN_DOUBT, suppress affected content and keep barrier open. Wall-clock, H receiver sequence, queue order or local cache is never causal proof.

## 7. D conformance

Add D-CO-01..10: fence before reservation; reservation before fence; fence waits behind participant; safe abort clears participant; provider success then later fence; unknown provider outcome blocks fence; lineage gap invalidates clearance; coordinator failover/restore; stale replay after fence; contradictory terminal evidence.

Status: **SPECIFIED / NOT RUN**. No deployed coordinator, durable participant registry, storage transaction, executable race proof or Global Forget completion is claimed.

## 8. Acceptance boundary

This artifact specifies D's required fence/participant behavior. It does not approve I authorization implementation, C provider integration, H wire encoding, coordinator operator or Storage durability. Exact cross-owner acceptance of `CausalOrderProfile/1.0` and `bmcp.applied-ack/1.1.0` remains required before `CGH-APPLIED-1.1` can be frozen.
