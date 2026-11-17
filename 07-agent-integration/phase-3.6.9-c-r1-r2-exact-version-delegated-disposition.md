# Phase 3.6.9 — C Exact-Version R1/R2 Owner Disposition

- Role: C — Agent Integration / actual provider submit boundary
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Scope: C admission ledger, provider reservation/egress, CSubmitOutcome and C outage-gate release
- Provenance: **delegated role simulation authored in the coordinating ChatGPT session at the user's direction; not an independent human Owner signature or cryptographic attestation**
- Status: architecture proposal only; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED

## Exact review bundle

| Source | Blob |
|---|---|
| A Phase 3.6 architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H recovery wire contract | `707ed85642ba4b0275c4ec851d599fde28ec6cae` |
| H recovery schema 1.0.3 | `9c3b98abab0c04a241a93c5e6f02e9424059b07b` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |


## R1 — C admission and provider-attempt completeness

C accepts its Phase 3.6.9 local ledger and snapshot model. Every accepted protected request is durably represented before C acknowledges acceptance or creates a reservation. A pre-COC admission is a first-class C-local item and remains NOT_REGISTERED until the exact stable identity is appended to COC; C must never fabricate a ParticipantIntentRef.

C's snapshot distinguishes request entries from admission/reservation/provider-attempt entries and binds each to exact request digest, scope, final boundary, context/delivery identity, attempt/idempotency identity and effect state. A sent/ambiguous provider attempt remains in the inventory until the same-key authoritative provider outcome is resolved.

## R2 — C gate and actual egress boundary

C accepts the one durable C gate-close transaction/CAS and the same-serialization-domain rule for local admission and provider reservation. C further requires the actual egress adapter to serialize the final outbound send boundary against current CGateGeneration, exact CAdmissionRef/reservation, I COMMIT_WON, D clearance, request digest and one-use provider-attempt identity.

Reservation is not invocation. A queued, reserved or DISPATCH_AUTHORIZED but NOT_DISPATCHED attempt cannot send provider bytes after C gate close. If the send boundary committed first, the attempt is pre-close and must be reconciled by the same provider key. Lost send/result ACK is UNKNOWN; no retry-as-new-operation is allowed.

During COC outage, no new protected provider-send boundary may commit after the local C gate closes. A pre-existing SENT_OR_AMBIGUOUS attempt is reconciled; a NOT_DISPATCHED attempt remains unsent until the recovery batch and C release permit a fresh currentness check.

## Enumerated amendments / conditions

1. The concrete egress adapter must demonstrate gate-close-wins and send-wins races using one authoritative serialization/fencing boundary. A process-local check followed by an unrelated network call is insufficient.
2. Every provider adapter must define same-key idempotency and authoritative outcome lookup. Generic exactly-once semantics are not assumed.
3. The C owner snapshot must include reservation and provider-attempt high-waters and explicit COMPLETE_EMPTY/NOT_ENUMERATED distinction.
4. H semantic validation must bind every REGISTERED C admission to exactly one COC participant and every NOT_REGISTERED item to an owner-local terminal or later same-identity registration.
5. Only exact I COMMIT_WON plus D clearance and the final C gate predicate permits provider invocation. REVOCATION_WON, INDETERMINATE_ABORTED and UNKNOWN prohibit invocation.
6. C outage-Gate Release is C-only and cannot resolve I/D/Storage state or declare a provider outcome.

## C disposition

C's R1/R2 architecture is conditionally acceptable with these amendments. This does **not** close A's R1/R2 findings: the adapter proof, H semantic validators and A integration remain required. No provider production integration, runtime conformance or production activation is approved.
