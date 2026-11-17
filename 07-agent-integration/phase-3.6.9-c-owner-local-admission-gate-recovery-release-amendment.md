# Phase 3.6.9 — C Owner-Local Admission Gate, In-Flight Ledger & Recovery Release Amendment

- Owner perspective: C — Agent Integration / actual provider submit boundary
- Status: **PROPOSED C-LOCAL AMENDMENT — EXACT-VERSION C RE-REVIEW REQUIRED**
- Supersedes: none; append-only refinement of the existing C-submit contract
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED

## 0. Exact source bundle

This amendment is prepared against the following exact sources:

| Source | Blob |
|---|---|
| A Phase 3.6 COC deployment architecture, §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC durable log / recovery protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 global inventory / receipt / restore amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 cross-boundary fencing / terminalization amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6 causal-order contract | `45a48249717c8cddb07ab96197730ef93d406c22` |

This document is a C proposal. It is not a C exact-version decision, not an A integration acceptance, and not an H schema freeze.

## 1. C authority and independent state

C owns the actual final-request/provider submit boundary, C admission ledger, provider reservation/attempt identity, immutable CSubmitOutcome and C outage-admission release. C does not own I authorization, D ForgetFence/lineage, Storage prepared participant state, or COC global ordering.

The following state is independent and MUST NOT be conflated:

- `CGateGeneration`: monotonic C outage/protected-admission gate generation.
- `CRequestHighWater`: C-local accepted protected request ledger boundary.
- `CAdmissionHighWater`: C-local admission/reservation/provider-attempt ledger boundary.
- `CProviderAttemptHighWater`: provider attempt ledger boundary.
- I `IGateGeneration`, `PermissionEpoch`, `ProducerDomainInventoryEpoch` and I request/inventory roots.
- D `ForgetFenceGeneration`, D WorkItem/Attempt high-waters and barrier root.
- COC `RecoveryEpoch`, committed prefix, RecoveryCutoffBatch and ParticipantManifest.
- Storage `PreparedParticipantRef`, GID, DatabaseIncarnationRef, native XID, attempt and participant-ledger version.

No arithmetic comparison or synthetic global counter is permitted.

## 2. C gate-close linearization

### 2.1 Single durable C serialization point

C MUST implement gate closure as one durable, linearizable C-authoritative transaction/CAS over an append-only C control ledger. The successful commit is the sole C gate-close linearization point.

The transaction MUST atomically:

1. authenticate and canonicalize the COC-outage / recovery-suspension request and its stable RequestRef/digest;
2. advance `CGateGeneration` monotonically;
3. set the affected protected-admission gate to CLOSED_PENDING_RECOVERY;
4. append the immutable request record;
5. capture C request, admission, reservation and provider-attempt high-waters;
6. capture the complete C-local in-flight admission member set, count, canonical root and snapshot generation;
7. persist the C anti-rollback anchor and gate-close attestation identity/digest;
8. commit before C acknowledges that the request is durably pending.

A read-then-close, cache invalidation, event-bus broadcast or best-effort worker pause is not a linearization point.

### 2.2 Every C protected boundary serializes against the same gate

Every C operation capable of admitting or advancing protected work MUST validate the current `CGateGeneration` and append/update its C admission record in the same authoritative transaction/CAS. This includes:

- accepting a protected final-request candidate;
- creating or finalizing a ParticipantIntent;
- creating/finalizing a provider reservation;
- acquiring or advancing a provider attempt;
- dispatching a provider invocation;
- recording an invocation result or recovery observation;
- retry/replay after timeout, process restart or lost ACK;
- any transition that could turn a previously private request into a provider-visible side effect.

The gate check and the corresponding admission/state transition MUST be atomic in the same C serialization domain. A check-then-act gap is prohibited.

For each race exactly one result is allowed:

- **Admission commits first:** its immutable C admission record is durable and included in the captured high-water/member set, even if its caller ACK or COC registration is delayed.
- **Gate close commits first:** the new protected admission/reservation/provider attempt is rejected or placed in a typed non-provider, non-publishing suppression lane.
- **Ordering/evidence uncertain:** C records UNKNOWN, keeps the gate closed, and performs no provider side effect.

### 2.3 Pre-COC admitted work

C MUST write a durable C-local admission record before acknowledging acceptance of a protected request or creating any reservation. Therefore a request admitted locally but not yet represented by a COC ParticipantIntent remains discoverable.

Each admission entry carries:

- stable CAdmissionRef and immutable sequence/generation;
- exact request digest, final-request boundary and authenticated principal/session binding;
- applicable ContextId/ContextVersion, DeliveryId/attempt and scope binding;
- reservation/provider-attempt identity if created;
- current phase and effect boundary;
- exact COC ParticipantIntentRef/position/digest if registered, otherwise explicit `NOT_REGISTERED` plus reason;
- I and D evidence references when obtained;
- retry/replay ancestry and terminal/no-effect proof or UNKNOWN;
- canonical entry digest and append-only predecessor/root linkage.

A C admission with `NOT_REGISTERED` MUST NOT be assigned a fabricated COC ParticipantIntentRef. If the operation is eligible to proceed after recovery, C must register the same stable operation identity before any further protected effect. It must not mint a replacement identity to hide the original admission.

## 3. C provider boundary and terminal semantics

The following remains mandatory and is made explicit for the outage gate:

1. A durable C admission record exists.
2. The exact COC ParticipantIntent is quorum-committed and bound to the exact final request digest and C admission identity.
3. I's authoritative terminal outcome is exactly `COMMIT_WON`, with the exact receipt/participant binding and single-use consumption proof.
4. D's exact lineage-bound clearance and current FenceGeneration predicates permit the operation.
5. The final C reservation is committed under the current C gate generation and exact same transaction/idempotency identity.
6. The provider invocation is dispatched exactly once under that reservation's provider-specific idempotency/recovery contract.
7. C records immutable CSubmitOutcome from the actual provider/runtime observation.

`REVOCATION_WON` and `INDETERMINATE_ABORTED` require no provider invocation and same-XID rollback where Storage has prepared the participant. `UNKNOWN/IN_DOUBT` remains blocked. A COC intent, I terminality other than COMMIT_WON, D clearance, reservation, timeout, transport ACK or lost ACK is not provider success.

Reservation creation before provider invocation is a C-local durable admission/control action, not permission to invoke the provider. If a provider reservation itself causes an externally visible or irreversible provider-side effect, it MUST be treated as a provider invocation and gated identically.

## 4. C snapshot and explicit completeness state

A C owner snapshot attestation MUST include:

- C authority and gate ref/generation;
- request high-water and admission/reservation/provider-attempt high-waters;
- snapshot generation and anti-rollback anchor;
- exact affected scope and scope-binding digest;
- enumeration status `COMPLETE_NON_EMPTY` or `COMPLETE_EMPTY`;
- canonical ordered member array (empty array for COMPLETE_EMPTY; never null);
- exact member count and canonical member-set root/digest;
- ledger/source identity and completeness method;
- each entry's COC registration state (`REGISTERED` with exact intent identity, or `NOT_REGISTERED` with reason);
- RecoveryEpoch/RecoveryCutoffBatch/ParticipantManifest refs when available;
- issuer/subject/audience/purpose and integrity evidence under I/H policy.

`NOT_ENUMERATED`, `UNAVAILABLE`, `PARTIAL`, `UNKNOWN`, missing member arrays or unavailable ledger reads MUST NOT be encoded as `COMPLETE_EMPTY`. Zero count alone is insufficient. The canonical empty representation and its digest must be defined by H and verified by the receiver.

## 5. Recovery reconciliation and repeated cutoff rounds

C's in-flight set and COC's committed participant set are separate sets:

- C local ledger enumerates every C-admitted request/reservation/provider attempt, including pre-COC admissions.
- COC enumerates every ParticipantIntentRef in the exact quorum-committed prefix.

The RecoveryCutoffBatch binds the C snapshot attestation and its root; the COC ParticipantManifest binds the exact committed prefix and its root. The join uses exact typed references, never a fabricated common sequence.

A C admission after captured C high-water remains behind the closed gate. It must be included in a subsequent immutable cutoff/manifest round before C can release, unless C proves with authoritative scope evidence that it is outside the affected scope and was never admitted. If any C high-water, scope generation, admission root or provider-attempt membership changes during reconciliation, the current release candidate is stale and another round is required.

Every pre-batch C admission must resolve to one of:

- exact COC-registered participant with authoritative I/D/Storage/C outcome evidence;
- authoritative provider no-invocation proof and safe terminal cancellation;
- actual provider outcome with immutable CSubmitOutcome and same-key recovery evidence;
- UNKNOWN/IN_DOUBT, which blocks release.

Missing COC rows, queue emptiness, worker absence, reservation expiry, timeout or lost ACK are not terminal evidence.

## 6. C-only outage Gate release

Only C may issue `CGateReleaseReceipt`. COC, I, D, Storage and H cannot release C's gate.

C may release its temporary outage gate only after:

1. exact RecoveryEpoch, COC prefix, RecoveryCutoffBatch and ParticipantManifest are verified;
2. C request/admission/provider-attempt ledgers are complete through the captured high-waters;
3. all `NOT_REGISTERED` admissions are registered under the same stable identity or authoritatively terminalized with no provider effect;
4. every provider invocation has an authoritative same-key outcome; UNKNOWN/IN_DOUBT remains blocking;
5. every COC participant joins exact I terminal proof, D lineage/fence evidence and Storage resolution where applicable;
6. the final C high-water, scope generation, ledger root and anti-rollback anchor are revalidated atomically at release commit;
7. no later request or membership advance has made the snapshot stale.

If any high-water or scope changes before release commit, C stays closed and produces a subsequent cutoff round. The release receipt is typed `OUTAGE_ADMISSION_RELEASE_ONLY`; it does not authorize provider invocation for an old participant, clear I/D gates, resolve Storage, or declare Forget complete.

## 7. Retry, idempotency and lost-ACK invariants

- Same CAdmissionRef + same canonical digest returns the original result.
- Same idempotency identity with changed request/scope digest is immutable CONFLICT.
- An ambiguous provider outcome is reconciled using the same provider idempotency key and same C transaction/reservation; never retry as a new operation.
- A terminal provider result is append-only and cannot be overwritten by a later timeout or retry.
- A lost C ACK is resolved by authoritative lookup of the original CAdmissionRef/provider-attempt identity.
- Provider-specific exactly-once behavior is not assumed; each production adapter must prove its actual idempotency and outcome-lookup contract before activation.

## 8. Required C negative/positive vectors

At minimum:

1. Gate-close wins before C admission: reject; no ParticipantIntent/reservation/provider call.
2. C admission wins before close: admission appears in sealed snapshot despite lost caller ACK.
3. Gate-close races reservation: one atomic order only; no check-then-act path.
4. C admission exists but no COC ParticipantIntent: snapshot marks NOT_REGISTERED; no fabricated intent.
5. Same admission replay/same digest returns original; changed digest conflicts.
6. COC prefix empty but C local admission non-empty: not a globally empty recovery set.
7. C local COMPLETE_EMPTY with unavailable ledger: reject as invalid empty proof.
8. Post-high-water request before release: C gate stays closed; subsequent batch required.
9. High-water advances between release validation and commit: CAS fails; no release.
10. Provider invocation attempted with I REVOCATION_WON: reject, zero provider calls.
11. Provider invocation attempted with I INDETERMINATE_ABORTED or UNKNOWN: reject, zero provider calls.
12. Provider result ACK lost: same key lookup; no new attempt identity.
13. Provider outcome UNKNOWN: CSubmitOutcome UNKNOWN; C/I/D barriers remain open.
14. Provider success without exact D clearance or current C gate: reject before invocation.
15. Reservation adapter performs side effect: classify as provider boundary and require same gate.
16. Restore replays stale C reservation/provider attempt: remain closed until same-key reconciliation.

## 9. C disposition and remaining owner decisions

This proposal addresses the missing C-local R1/R2 contribution identified in the coordinator cross-owner review. It does not close R1/R2 by itself.

- C exact-version re-review is required against this amendment and the exact A/Storage/COC/I/D bundle.
- H must publish the exact wire schemas and canonical empty-set contract.
- I/D must re-review only where their owner evidence is consumed by the C admission/release joins.
- A must perform the final cross-owner integration review after all exact-version decisions.

**Status:** C proposal only; no C independent approval, no A integration acceptance, no H schema freeze, no runtime conformance, no deployment and no production activation. JF-10 P0 remains OPEN; Multi-PolicyDomain remains BLOCKED.


## 10. Provider egress linearization — dispatch is not invocation

A reservation or durable provider-attempt record does not prove that request bytes crossed the actual provider boundary. C MUST distinguish:

`NOT_DISPATCHED` → `DISPATCH_AUTHORIZED` → `SENT_OR_AMBIGUOUS` → `OUTCOME_KNOWN`

with `UNKNOWN/IN_DOUBT` retained whenever send/result evidence is ambiguous.

The C Gate linearization contract applies at the actual egress boundary, not only when a worker creates a reservation or queues a provider job:

1. The provider egress adapter/gateway MUST serialize its final send authorization against the same authoritative `CGateGeneration` used by C gate closure.
2. Immediately before releasing request bytes to the provider transport, it MUST atomically verify current gate generation, exact CAdmissionRef, exact reservation, I `COMMIT_WON`, D clearance, request digest and the one-use provider-attempt identity, then durably record the send-boundary transition.
3. If Gate close commits first, no outbound provider request bytes may be released. A reservation or `DISPATCH_AUTHORIZED` record is not an exception.
4. If the provider-send boundary commits first, the attempt is a pre-close in-flight participant. Gate closure captures it; C reconciles the same provider idempotency key and exact attempt until the actual outcome is authoritative.
5. If the gateway cannot serialize the final send boundary against Gate close, or cannot prove whether bytes were sent, it MUST return UNKNOWN and suppress further sends. A process-local check followed by an unrelated network call is not sufficient proof of ordering.

During a COC outage, no new provider-send boundary may commit after C's local pending gate closes. Pre-existing `SENT_OR_AMBIGUOUS` attempts are reconciled using the same key; pre-existing `NOT_DISPATCHED` or merely reserved attempts remain unsent until the recovery batch and C gate release permit a fresh currentness check. They may not be silently treated as already invoked.

This is an explicit adapter boundary requirement. Generic exactly-once provider behavior is not assumed; each adapter must prove that the gateway's send record and provider's idempotency/outcome lookup compose safely. If the provider offers no authoritative same-key lookup, an ambiguous send remains IN_DOUBT indefinitely and blocks C release.

Required additional vectors:
17. Reservation exists but provider send has not crossed egress; Gate close wins; assert zero provider requests.
18. Provider send boundary wins immediately before Gate close; attempt appears in sealed C inventory and is reconciled with the same key.
19. Gate close races final egress generation compare; exactly one serialization order is observed.
20. Egress gateway cannot reach authoritative C Gate; no provider bytes are sent.
21. Provider transport ACK is lost after send; same-key lookup only, no new attempt.
22. Reserved/queued attempt during COC outage remains NOT_DISPATCHED until recovery release.
