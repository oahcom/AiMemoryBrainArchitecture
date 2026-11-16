# C Owner Contract Addendum — C-submit / I-authorization / D-ForgetFence Causal Ordering

- Owner: Session C — Agent Integration and actual Final Request Submission boundary
- Branch: `session-c-agent-integration-2026-11-16`
- Target profile: `CausalOrderProfile/1.0`
- Target H schema: `bmcp.applied-ack/1.1.0`
- Target common package: `CGH-APPLIED-1.1` (proposed successor; not cross-owner frozen)
- Status: **C-SIDE CONTRACT AMENDMENT SPECIFIED; coordinator deployment and cross-owner acceptance OPEN**.

## 1. C authority and boundary

C remains the sole producer of immutable evidence that the exact post-transformation request crossed the actual successful provider/runtime submit boundary. C does not mint I authorization, issue D fences, operate the common coordinator by implication, or mutate G Applied state.

A local buffer, middleware render, transport ACK, reservation receipt, provider-call intent or H receiver durability receipt is not a successful submit.

## 2. Required pre-submit sequence

1. Freeze the exact final request bytes/semantic canonical form and digest; bind actual ContextId/ContextVersion, DeliveryId/attempt, InferenceRequestId namespace, FinalRequestBoundaryId, ManagedRegion digest, authenticated Principal/Actor/Agent/Adapter/runtime/session, ScopeBindingSet, applicable EnvironmentRef and CapabilityEpoch.
2. Create CausalOrderTransactionRef and obtain a durable ParticipantIntentRef from the coordinator, bound to the exact request digest, boundary, identity/session, context/delivery and capability. This intent is registered before any provider side effect and is not permission to submit.
3. Bind the exact intent to an I-issued single-use CommitAuthorizationReceipt; I consumes it once in its own sequencer and returns IAuthorizationTerminalRef. If revocation wins, abort. If authorization wins, later revocation cannot become effective past this unresolved participant until terminal outcome.
4. Bind the same intent to D's ForgetFence and complete target/source/ancestor lineage. D returns DParticipantClearanceRef only if no earlier fence wins; any later fence remains pending behind this unresolved participant.
5. Coordinator validates the exact I/D owner references and finalizes ParticipantReservationRef. If any owner proof is missing, stale or mismatched, do not call the provider.
6. Invoke the provider/runtime exactly once under the finalized reservation's idempotency/attempt contract; capture actual provider receipt and actual InferenceRequestId.
7. Append CSubmitOutcomeRef. Obtain CausalOrderTerminalProofRef binding C, I and D terminal evidence.
8. Emit Final Request Submitted evidence only when actual provider outcome is successful and terminal proof is determinate. Otherwise emit REJECTED / UNKNOWN / IN_DOUBT and suppress Full Applied.

## 3. Race and barrier semantics

- A D fence requested after ParticipantIntentRef cannot become effective past that unresolved intent until C's exact submit outcome is durably terminal or a safe abort is authoritatively committed.
- An I revocation requested before I receipt consumption may win and force abort. Once I has terminalized the receipt as COMMIT_WON, later revocation effectiveness is held behind that participant until C's exact outcome is terminal.
- If provider success is proven before the later effective fence/revocation, preserve the historical submit fact; later D/I transitions invalidate current-use.
- If D fence or I revocation wins before reservation/authorization consumption, C MUST NOT invoke provider.
- If provider outcome is unknown after timeout/crash, the participant remains IN_DOUBT. C MUST NOT retry as a new operation or report success; reconciliation must use the same transaction/reservation and provider idempotency key. D/I barriers remain open.
- If coordinator order, owner evidence, lineage or exact digest cannot be reconciled, C emits UNKNOWN and no Full Applied evidence.

## 4. Required C evidence fields

In addition to existing C Final Request Submission Evidence fields, require:
- CausalOrderProfileRef, CausalOrderCoordinatorRef, CausalOrderTransactionRef;
- ParticipantIntentRef and its coordinator epoch/position; ParticipantReservationRef and final reservation position;
- CommitAuthorizationReceiptRef and IAuthorizationTerminalRef;
- ForgetFenceRef/generation, ForgetLineageCoverageRef and DParticipantClearanceRef;
- CSubmitOutcomeRef, actual provider receipt ref, actual InferenceRequestId and FinalRequestBoundaryId;
- CausalOrderTerminalProofRef, terminal outcome and proof digest;
- exact request/managed-region digests and canonicalization profile IDs.

All refs remain opaque and authority-issued. C verifies issuer/integrity and exact binding; C does not reinterpret I/D semantics or compare their independent epoch numbers.

## 5. Forbidden shortcuts

- No wall-clock comparison, local monotonic clock comparison across processes, H receiver sequence, ACK arrival order or event-bus delivery order as causal proof.
- No submit before participant reservation and compatible I/D clearances.
- No automatic reservation expiry that silently releases D/I barriers while provider outcome is unknown.
- No new transaction on retry after ambiguous provider outcome.
- No Full Applied claim from a reservation, PermissionDecision, PermissionEpoch, ForgetFenceGeneration, transport ACK or partial lineage alone.

## 6. C conformance

Add C-CO-01..10 aligned with H36-CO-01..10: reservation-before-side-effect; wrong digest/replayed I receipt; revocation-first; fence-first; fence waits behind reservation; successful submit then later fence/revocation; crash/unknown provider outcome; coordinator failover/restore; contradictory terminal evidence; wall-clock/receiver-order inversion.

Status: **SPECIFIED / NOT RUN**. No production provider integration or runtime conformance is claimed.

## 7. Acceptance boundary

This artifact specifies C's required integration behavior. It does not approve I's receipt implementation, D's barrier implementation, the coordinator operator/deployment, H wire schema, G Applied predicate or Storage durability. Cross-owner acceptance of the exact `CausalOrderProfile/1.0` and `bmcp.applied-ack/1.1.0` remains required before the proposed `CGH-APPLIED-1.1` can be frozen.

## C Owner exact-version decision — CGH-APPLIED-1.1

- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob SHA: `9808b31f840606b329f1a794935dfc9c5084d63b`
- Common contract: `CGH-APPLIED-1.1`
- Causal profile: `CausalOrderProfile/1.0`
- H schema target: `bmcp.applied-ack/1.1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, within C's authority over the actual final-request/provider submit boundary and C-owned evidence.

C accepts the normative ordering: durable ParticipantIntent before provider side effect; exact I receipt consumption/terminal and D lineage-bound clearance; coordinator-finalized reservation; actual provider handoff; immutable CSubmitOutcome; and common terminal proof. C accepts that I COMMIT_WON, D clearance, reservation, H ACK or coordinator intent alone never proves provider success. C alone emits CSubmitOutcome from the observed provider/runtime outcome, including actual provider receipt and InferenceRequestId; only determinate ACCEPTED handoff may support Final Request Submitted.

Exceptions and closure conditions:
1. Coordinator/operator, durable participant registry and monotonic order store are not designated/deployed/verified. C acceptance is conditional on one durable transaction/participant surviving process death, crash, failover and restore without releasing IN_DOUBT.
2. Provider exactly-once semantics cannot be assumed generically. Production activation requires a provider-specific idempotency/recovery contract proving same transaction/key recovery and no retry-as-new-operation after ambiguous outcome.
3. CSubmitOutcome and CausalOrderTerminalProof must bind the exact final request digest, boundary, transaction, reservation, actual provider receipt and outcome; missing/ambiguous provider result remains UNKNOWN/IN_DOUBT and must retain I/D barriers.
4. H 1.1.0 field mapping and cryptographic/replay interoperability remain candidate/unverified; C does not approve H implementation or crypto governance.
5. G alone validates and commits Applied; C acceptance does not establish G acceptance, tests, deployment or current-use eligibility.

No C-CO execution or production implementation verification is claimed. This decision applies only to the exact A Blob above and does not transfer any CGH-APPLIED-1.0 approval.


## C Owner exact-version reaffirmation — current CGH-APPLIED-1.1 candidate

- A candidate Blob SHA: `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`
- Profile: `CausalOrderProfile/1.0`; H schema: `bmcp.applied-ack/1.1.0`

**Decision: ACCEPT WITH ENUMERATED EXCEPTIONS**, limited to C's final-request/provider boundary and C-owned evidence.

C reaffirms the exact ordering and evidence chain for this candidate: durable ParticipantIntentRef before provider side effect; I receipt consumption and IAuthorizationTerminalRef; D lineage-bound clearance and fence cutoff; coordinator-finalized ParticipantReservationRef; actual provider/runtime handoff; immutable CSubmitOutcomeRef; and CausalOrderTerminalProofRef. I COMMIT_WON, D clearance, reservation, coordinator intent and H ACK do not prove provider success. C alone emits CSubmitOutcome from actual provider observation, including provider receipt, actual InferenceRequestId, FinalRequestBoundaryId and exact request digest. UNKNOWN remains IN_DOUBT and must not be retried as a new transaction.

C accepts the current outage-cutoff safety rule as a necessary admission invariant: if COC is unavailable, C does not create or accept a new protected intent/reservation and does not call the provider. C relies on I/D to keep their local admission gates closed until their request cutoffs are durably committed to COC; C does not infer absence of revocation/fence from coordinator unavailability.

Exceptions: (1) COC/operator and durable participant registry remain undesignated/undeployed/unverified; (2) provider-specific same-key idempotency and ambiguous-outcome recovery remain to be proven; (3) H 1.1.0 interoperability and I crypto/key governance remain open; (4) G acceptance and C-CO execution remain open/not run. This decision is only for the exact A Blob above; no 1.0 approval is transferred.
