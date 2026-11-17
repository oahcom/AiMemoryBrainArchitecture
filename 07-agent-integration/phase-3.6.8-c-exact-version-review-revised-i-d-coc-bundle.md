# Phase 3.6.8 — C Exact-Version Re-Review of Revised I/D/Storage/COC Bundle

- Reviewer role: C — Agent Integration / Provider Side-Effect Boundary (delegated role simulation)
- Decision date: 2026-11-17
- Decision: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**
- Scope: C provider admission, final egress serialization, CSubmitOutcome, recovery cutoff gating and provider idempotency evidence.
- Architecture only: NOT IMPLEMENTED / NOT PROVIDER-CONFORMANCE-VERIFIED.

## 1. Exact review bundle

| Artifact | Exact Blob |
|---|---|
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC protocol with §15–16 ordering/digest supersession | `a07a8d352f31d5406786e1cd8ecddd4065ec384a` |
| Storage ordering amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` |
| I Phase 3.6.8 revised source | `cf4b76f151204fa47b156b5d807e7378c28fd268` |
| D Phase 3.6.8 revised source | `2d95099a2e19a8cbec325925b70da576f73d9899` |
| C Provider Outcome semantic contract | `f538d921d06c92dfaba13fbe326a80d6550fe1b7` |
| C cross-authority causal-order contract | `45a48249717c8cddb07ab96197730ef93d406c22` |
| H Phase 3.6.11 two-phase wire/validator addendum | `5a3def4f7e84ed489993681455b6840b93ecc282` |
| H Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` |

## 2. Decision rationale

C accepts the revised I/D/Storage/COC semantics for the C-owned provider boundary, with the following confirmations:

1. D Phase 3.6.8 §11.3 correctly requires C-owned CSubmitOutcomeRef/digest, provider idempotency-key namespace, exact request digest and authoritative provider receipt/lookup evidence. C alone creates and attests the provider outcome.
2. C's immutable CSubmitOutcome tuple in its provider-outcome contract binds exact ParticipantIntent, reservation, provider identity/idempotency reference, final request digest/boundary, provider receipt/lookup, and the applicable I/D/Storage participant references.
3. Provider terminality is limited to HANDOFF_ACCEPTED with authoritative same-key evidence or HANDOFF_REJECTED with definitive no-handoff proof. NOT_INVOKED is a distinct local pre-invocation disposition. UNKNOWN/IN_DOUBT is durable and blocking.
4. C's final provider invocation/retry gate requires current C admission/reservation plus exact I COMMIT_WON, D current clearance/fence predicate and Storage/participant predicates as applicable. COC state, H ACK and Storage visibility cannot synthesize provider outcome.
5. Revised COC §15–16 and Storage v3.1 §5.4 now align on the manifest-first two-record sequence and distinguish ParticipantManifestContentDigest, RecoveryBatchDigest and ParticipantManifestRecordDigest.
6. C provider invocation remains prohibited after Batch commit but before Manifest Record commit, and after Manifest commit but before linearizable pair readback. C may only begin participant-specific provider reconciliation after verified pair readback and current C/I/D/Storage predicates.
7. C's pre-COC owner-local admission inventory remains distinct from the committed COC participant manifest. A C admission not yet registered in COC remains a C-owned obligation; it must not be fabricated as a COC participant.

## 3. D36.8-R3 acceptance

**D36.8-R3 is satisfied as an architecture contract.** C has a named authoritative CSubmitOutcome object and the required provider idempotency namespace, request digest and receipt/lookup evidence. D must reference and validate C's proof, not create it.

This decision does not claim that actual provider outcome records exist for any production transaction, nor that any provider adapter has passed same-key recovery tests.

## 4. C-owned exceptions and blockers retained

1. Provider-specific idempotency and same-key lookup must be proven separately for each production provider. Generic exactly-once semantics are not assumed.
2. Provider outcome persistence must be durable across process death between provider handoff and C ledger/COC persistence. Without authoritative same-key recovery, outcome remains UNKNOWN.
3. Provider receipt semantics and definitive no-handoff evidence must be documented for each provider/adapter version.
4. C owner snapshot completeness, egress serialization against CGateGeneration, crash/restart, duplicate, timeout, lost-ACK and failover tests remain specified, not executed.
5. C cannot release I Gate, D Forget Fence, Storage locks or COC RecoveryEpoch and cannot claim G Applied.

## 5. Conformance boundary

The C-PO-01..10 vectors and C-CO-01..10 cases remain **SPECIFIED / NOT RUN**. This review is not provider-vendor approval, independent human Owner signature, runtime adapter conformance, production authorization or proof of exactly-once provider behavior.

## 6. Final disposition

**ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS.** D36.8-R3's required C evidence contract is present and correctly owner-scoped. Provider-specific idempotency, durable outcome recovery and executable conformance remain activation blockers.

## 7. Provenance

Assistant-authored delegated C role review at the user's direction. It is not an independent human C Owner signature or approval.