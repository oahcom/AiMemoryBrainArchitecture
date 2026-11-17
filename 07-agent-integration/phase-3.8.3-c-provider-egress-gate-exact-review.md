# Phase 3.8.3 — C Exact Review: Provider Egress Gate Adapter Contract
# C 精确审查：Provider Egress Gate Adapter 合同

- Owner: C — Agent Integration / Actual Provider Submit Boundary
- Review mode: independent C-role semantic review at the user's direction
- Decision: **ACCEPT WITH CONDITIONS**
- Status: provider egress semantics composed; Adapter implementation and runtime conformance OPEN
- Exact reviewed file: provider-egress-gate-adapter-contract.md
- Exact reviewed Blob: 6cee9eeaf826feb4f27895aeeebcfe32d42306e7

## 1. C decision

C accepts §13 as the controlling composition of the Provider Egress Gate with C Phase 3.6 causal ordering, Phase 3.6.9 C local admission/recovery, and Phase 3.8.2 exact review. The final C-owned egress CAS is a distinct boundary from COC ParticipantIntent/Reservation, I authorization, D clearance and provider outcome.

## 2. Accepted invariants

1. C local admission is durable before the common COC intent; it binds the exact immutable final-request digest and authenticated request/session/context tuple.
2. COC ParticipantIntent is a durable causal-order record, not provider permission.
3. Provider invocation requires exact D participant/lineage/fence clearance and I single-use authorization terminality COMMIT_WON.
4. COC ParticipantReservation is required but is not proof of send and cannot bypass C's local gate.
5. Immediately before transport handoff, the transport-owning Adapter performs the final C Gate CAS against CGateGeneration and exact admission/reservation/attempt/request digest.
6. CloseEgressGate and CommitEgress share the same durable C serialization authority. Close-first means zero provider bytes; egress-commit-first means the exact attempt is captured as in-flight.
7. Crash or ambiguous transport handoff remains UNKNOWN/IN_DOUBT; recovery uses the same provider idempotency key. No retry-as-new-operation is permitted.
8. C alone emits immutable CSubmitOutcome from actual provider/runtime observation. I/D/COC/H/Storage evidence cannot synthesize provider truth.
9. Final Request Submitted and Full Applied remain distinct from admission, reservation, egress commitment, transport ACK and model execution.

## 3. Required clarification on I and D currentness

At final C egress, I currentness is established by the exact operation-bound I terminal receipt and I PolicyDomain sequencing, not by comparing PermissionEpoch numerically with CGateGeneration or by blindly rejecting every later I epoch. If I REVOCATION_WON before authorization consumption, no send. If I COMMIT_WON consumed first, that exact participant is held ahead of later revocation until C terminal outcome; the Adapter must verify that the receipt remains the authoritative COMMIT_WON outcome for this exact digest/participant.

Likewise D currentness is established by exact D participant/clearance and D fence ordering. A later D fence cannot pass the unresolved participant. Stale/mismatched D proof or a fence that won first blocks send. No wall-clock comparison or stale cached token is sufficient.

## 4. H and Storage dependencies

- H must map CAdmissionRef, COC ParticipantIntentRef/ParticipantReservationRef, I terminal receipt, D participant/fence evidence, C provider attempt, CSubmitOutcome and terminal proof into one canonical versioned wire contract. H owns schema and validation; C does not invent a parallel wire enum.
- Storage/Consistency must prove the durable C gate sequencer/ledger and its crash/HA/restore behavior if the C gate shares infrastructure with the common causal coordinator. The current Storage Phase 3.8.2 ADR does not select a deployed topology.
- Each actual provider adapter must prove same-key idempotency and authoritative outcome lookup. Providers without lookup support may leave ambiguous outcomes IN_DOUBT and block release.

## 5. Required tests and status

The 15 C vectors in provider-egress-gate-adapter-contract.md §13.5 plus C-RJ-02 and the existing C-CO vectors are **SPECIFIED / NOT RUN**. H's schema/reference-model test results are not a substitute for a real transport Adapter race test or provider-specific same-key recovery test.

## 6. Explicit non-claims

This review does not claim:
- an actual provider Adapter or transport implementation exists;
- multi-replica C Gate serialization is deployed;
- any provider accepted a request;
- provider exactly-once semantics are universal;
- Full Applied, inference execution or model use is proven;
- COC, I or D gates can be released based on this semantic review.

**C disposition: ACCEPT WITH CONDITIONS.** C semantic composition is accepted; H wire mapping, I/D exact proof validation, Storage topology, provider-specific recovery and runtime race execution remain OPEN.
