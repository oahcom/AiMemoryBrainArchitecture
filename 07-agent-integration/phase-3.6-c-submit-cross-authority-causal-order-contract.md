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
2. Obtain an I-issued single-use CommitAuthorizationReceipt bound to that exact operation, request digest, PolicyDomainRef/PermissionEpoch, full authorization tuple, CausalOrderTransactionRef and FinalRequestBoundaryId. A detached PermissionDecision/ALLOW is not enough.
3. Obtain D-issued current ForgetFence and complete target/source/ancestor lineage coverage for the exact managed region.
4. Before the provider side effect, register a durable participant reservation with the named CausalOrderCoordinator. The reservation binds the exact request digest and the I/D evidence refs. If reservation is unavailable, stale, mismatched or indeterminate, do not call the provider.
5. Obtain I terminal consumption evidence and D participant clearance. Neither owner may be replaced by a coordinator-supplied assertion.
6. Invoke the provider/runtime exactly once under the reservation's idempotency/attempt contract; capture the actual provider receipt and actual InferenceRequestId.
7. Append CSubmitOutcomeRef. Obtain a CausalOrderTerminalProofRef that binds C, I and D terminal evidence.
8. Emit Final Request Submitted evidence only when the actual provider outcome is successful and the terminal proof is determinate. Otherwise emit REJECTED / UNKNOWN / IN_DOUBT evidence and suppress Full Applied.

## 3. Race and barrier semantics

- A D fence or I revocation requested after a valid participant reservation cannot become effective past that unresolved participant until C's exact submit outcome is durably terminal or a safe abort is authoritatively committed.
- If provider success is proven before the later effective fence/revocation, preserve the historical submit fact; later D/I transitions invalidate current-use.
- If D fence or I revocation wins before reservation/authorization consumption, C MUST NOT invoke provider.
- If provider outcome is unknown after timeout/crash, the participant remains IN_DOUBT. C MUST NOT retry as a new operation or report success; reconciliation must use the same transaction/reservation and provider idempotency key. D/I barriers remain open.
- If coordinator order, owner evidence, lineage or exact digest cannot be reconciled, C emits UNKNOWN and no Full Applied evidence.

## 4. Required C evidence fields

In addition to existing C Final Request Submission Evidence fields, require:
- CausalOrderProfileRef, CausalOrderCoordinatorRef, CausalOrderTransactionRef;
- ParticipantReservationRef and reservation coordinator epoch/position;
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
