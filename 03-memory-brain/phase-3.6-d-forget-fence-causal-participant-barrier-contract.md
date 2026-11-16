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

## D Owner exact-version decision — CGH-APPLIED-1.1

- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA: `9808b31f840606b329f1a794935dfc9c5084d63b`
- Common contract: `CGH-APPLIED-1.1`
- Causal profile: `CausalOrderProfile/1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within D's authority over ForgetFence, lineage coverage, fence request cutoff/effective position and participant barrier semantics.

D accepts that ParticipantIntentRef is bound to the exact ForgetOperation/Fence and complete target/source/ancestor lineage; a D fence request cutoff before intent denies clearance (FENCE_WON), while a later request includes the participant and remains pending through the exact C submit outcome or safe abort. D accepts that DParticipantClearanceRef is intent- and lineage-bound, and that request/cutoff position is distinct from eventual fence-effective position. D clearance is not provider success or I authorization.

Exceptions and closure conditions:
1. The common coordinator, durable participant registry/order store and accountable operator are not yet designated/deployed/verified. D's barrier acceptance is conditional on the same durable participant transaction being visible to D and I across crash, failover, restore and recovery.
2. No lease expiry, timeout, worker loss, queue deletion, process death or coordinator outage may release a participant while provider outcome is UNKNOWN/IN_DOUBT. D's fence barrier remains open until immutable C outcome and reconciled terminal proof, or a proven safe abort, are durable.
3. Complete lineage inventory/version and digest must be authoritative and closed against late-discovered ancestors/sources; incomplete or conflicting lineage yields UNKNOWN/denied clearance.
4. Coordinator positions do not mint, replace or reinterpret D fence generation, request cutoff, effective position or lineage authority.
5. D-CO tests and production coordinator/failover/restore conformance remain NOT RUN / NOT VERIFIED.

This decision applies only to the exact A Blob above. It does not imply C/I/G/H/B acceptance, deployment, physical erasure, test pass or transfer of CGH-APPLIED-1.0 approval.


## D Owner exact-version reaffirmation — current CGH-APPLIED-1.1 candidate

- A candidate Blob SHA: `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`
- Profile: `CausalOrderProfile/1.0`; H schema: `bmcp.applied-ack/1.1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within D's ForgetFence, lineage and participant-barrier authority.

D accepts the candidate's intent-before-side-effect rule, exact target/source/ancestor lineage binding, DForgetFenceRequestRef admission cutoff, DParticipantClearanceRef, and separate fence-request cutoff versus fence-effective position. A fence request before ParticipantIntentRef yields FENCE_WON even while earlier participants drain; a later request remains pending behind that participant until exact C outcome or safe abort is durable. D clearance never proves I authorization or provider success.

D explicitly accepts the outage-cutoff amendment: if D receives a fence request while COC is unavailable, D locally closes affected lineage admission and reports PENDING/UNKNOWN. D MUST NOT reopen admission or issue favorable clearance until that request cutoff is durably recorded in the common coordinator and reconciled against the same participant ledger. COC outage, process death, lease expiry, timeout or lost ACK cannot release an IN_DOUBT participant.

Exceptions: (1) COC operator/store and durable participant registry are not designated/deployed/verified; (2) authoritative complete lineage inventory and late-discovery closure remain required; (3) D-CO/failover/restore conformance remains NOT RUN; (4) physical erasure/Global Forget completion is not implied. This decision applies only to the exact A Blob above.
