# Phase 3.6.8.3 — C Exact-Version Review: Provider Outcome × Storage v3.2.3 × COC Union Manifest

- Reviewer role: C — Agent Integration / Provider Side-Effect Boundary (delegated role simulation)
- Decision: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**
- Scope: C owner-local admission inventory, provider invocation/effect boundary, Provider Outcome, recovery cutoff gating and provider idempotency.
- Status: ARCHITECTURE DESIGN ONLY — NOT IMPLEMENTED / NOT PROVIDER-CONFORMANCE-VERIFIED
- Provenance: assistant-authored C role review at the user's direction; not independent human C Owner approval.

## 0. Exact review bundle

| Artifact | Exact Blob |
|---|---|
| Storage Design v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` |
| COC protocol §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` |
| Storage ordering amendment §3.6.4 | `9704d110a06d0c2ee98be960054e0396d0b68546` |
| I Phase 3.6.8 revised source | `cf4b76f151204fa47b156b5d807e7378c28fd268` |
| D Phase 3.6.8 revised source | `2d95099a2e19a8cbec325925b70da576f73d9899` |
| C Provider Outcome semantic contract | `f538d921d06c92dfaba13fbe326a80d6550fe1b7` |
| C cross-authority causal-order contract | `45a48249717c8cddb07ab96197730ef93d406c22` |
| H unified COC/JF-10/Provider Outcome schema artifact 1.2.5 | `164ec3c436558d5d93032edc51e127d15e03db4` |
| Prior C v3.2.2 review | `535579cdfeedf705195bb4aa04cf1a85cb9b9a0f` (predecessor; not transferred) |
| Prior H schema 1.2.3 review | `36ed239019e34eaafff9e22b127a58e8e2557842` (predecessor; not transferred) |

## 1. C decision and authority boundary

**C ACCEPTS the exact v3.2.3 / COC §17 / H schema 1.2.5 candidate for C's own Provider Outcome and side-effect boundary, with the exceptions in §7.**

C alone owns:
- C owner-local protected admission and provider-attempt ledger;
- provider identity/adapter and idempotency namespace;
- final request boundary and actual provider invocation;
- immutable CSubmitOutcome and provider receipt/lookup evidence;
- C outage Gate and C Gate release.

C does not mint I authorization, D Forget clearance, Storage prepared/resolution proof, COC quorum proof, H transport ACK or G Applied.

## 2. Provider Outcome verification

C confirms the following facts are independent and non-substitutable:

| Evidence | What it proves | What it does not prove |
|---|---|---|
| I COMMIT_WON | I's exact authorization receipt was consumed | Provider invocation or success |
| D clearance | D's current owner-local fence/lineage predicate | Provider invocation or success |
| Storage PreparedParticipantReceipt | Exact Storage participant is prepared/private | Provider invocation or success |
| Storage COMMITTED / PublicationReceipt | Storage's exact participant visibility outcome | Provider handoff or inference completion |
| COC Batch/Manifest | Recovery prefix membership and frozen accounting | Provider invocation or success |
| H ACK/schema validity | Message transport/structural validity | Provider invocation or success |
| CSubmitOutcome | C's observed provider/runtime handoff outcome for exact request/key | Inference correctness, user delivery or G Applied |

Only C's actual egress-boundary observation plus provider-specific authoritative same-key evidence can establish provider terminality.

## 3. C owner-local admission and union-manifest verification

C accepts the v3.2.3 S0a–S4 protocol:

1. **S0a:** C closes its protected side-effect Gate and atomically freezes request and admission/effect ledgers separately, including reservation, provider-attempt and provider-outcome high-waters, roots, counts and anti-rollback anchor.
2. **S0b:** after quorum restoration, COC freezes exact linearizable prefix P.
3. **S1:** manifest is the union of every COC ParticipantIntentRef at/before P and every applicable I/D/C owner-local admission through frozen admission high-waters.
4. **S2:** quorum-commit Batch bound to exact P, owner snapshots and union ManifestId/Digest/count.
5. **S3:** quorum-commit Manifest Record after Batch, referencing exact Batch position/digest and carrying the complete union.
6. **S4:** linearly read back both records and verify exact cross-bindings, owner roots/currentness and member completeness.
7. Only after S4 may participant-specific reconciliation/provider lookup begin, under C's own current Gate and exact I/D/Storage predicates.

Every C operation admitted before C Gate close must be represented, including:
- reservation created but provider not invoked;
- provider invocation started and response/ACK lost;
- provider accepted/rejected but C outcome persistence/COC append delayed;
- same-key provider lookup pending;
- retry/replay/worker restart;
- admitted operation not yet registered as a COC ParticipantIntentRef.

A pre-COC C admission is an `OWNER_LOCAL_ADMISSION`, not an omitted participant. It carries OwnerAdmissionRef/digest, C ledger ref/version, local sequence/high-water/root, request/operation digest, provider idempotency-key ref and explicit null COC ParticipantIntentRef plus reason where unregistered. It may carry both owner and COC identities only after exact typed immutable join. Matching TransactionRef, timestamp or payload similarity is not a deduplication proof.

## 4. H schema 1.2.5 verification

C accepts H schema artifact 1.2.5 as the correct structural direction for the C owner boundary because it:
- distinguishes `COC_PARTICIPANT` from `OWNER_LOCAL_ADMISSION`;
- allows explicit null COC ParticipantIntentRef plus absence reason for an unregistered owner admission;
- binds owner-local admission ref/digest, ledger ref/version, sequence/high-water/root and request/operation digest;
- separates request and admission high-water/count/digest/ledger roots in each owner snapshot;
- requires I/D/C-specific high-waters;
- requires the exact Batch and Manifest positions/digests on owner release;
- adds outcome-dependent C Provider Outcome evidence: ACCEPTED/REJECTED require finalized reservation and appropriate provider receipt/no-handoff evidence; NOT_INVOKED requires separate pre-invocation proof; UNKNOWN/IN_DOUBT requires unresolved reason.

The on-wire protocol-family `schema_version=1.2.0` is explicitly distinguished from the schema artifact revision 1.2.5. C accepts this distinction only as documented; downgrade/compatibility negotiation must use the artifact revision/profile, not silently infer it from the wire family version.

Schema validity does not prove provider outcome truth, exact C ledger completeness, C Gate currentness or semantic S4. H validators remain mandatory and C remains the sole outcome authority.

## 5. C Provider Outcome wire contract

Every CSubmitOutcome MUST bind:
- CSubmitOutcomeRef/digest and C issuer/adapter/runtime boundary;
- C OwnerAdmissionRef/digest, owner ledger ref/version, local sequence/high-water/root;
- exact provider and provider-adapter identity;
- stable provider idempotency-key reference and provider request/receipt/lookup references;
- FinalRequestBoundaryId and exact final request digest;
- TransactionRef, ParticipantReservationRef and COC ParticipantIntentRef or explicit null + absence reason;
- PreparedParticipant/attempt/ledger/tuple and I/D/Storage evidence references where JF-10 applies;
- actual InferenceRequestId when supplied;
- outcome enum and matching evidence type.

Terminal vocabulary:
- `HANDOFF_ACCEPTED`: authoritative provider acceptance for the exact request/key plus provider receipt/evidence;
- `HANDOFF_REJECTED`: definitive no-handoff proof;
- `NOT_INVOKED`: C-authoritative proof the provider boundary was never crossed;
- `UNKNOWN/IN_DOUBT`: timeout, crash, lost ACK, contradictory evidence or unavailable same-key lookup; nonterminal and blocking.

C confirms that H schema 1.2.5's conditional evidence requirements are structurally aligned. H semantic validation must still reject contradictory extra evidence, wrong request/key/attempt tuple, stale C Gate generation and provider outcome inferred from non-C facts.

## 6. Provider invocation and recovery gate

No new provider invocation, provider retry, Storage resolution or visibility publication is allowed after S2 or S3 alone. S4 must succeed. After S4, an already invoked UNKNOWN operation may only be reconciled with the same provider idempotency key and immutable request/participant tuple. Retry-as-new-operation, replacement reservation or changed request digest is forbidden.

C's final egress transaction must validate current CGateGeneration, exact C admission/reservation/attempt, final request digest/boundary, I COMMIT_WON proof, D current clearance/FenceGeneration and provider idempotency binding. If the adapter cannot serialize the final egress boundary against Gate close, it records UNKNOWN; it cannot claim NOT_INVOKED.

## 7. Enumerated C-owned exceptions and activation blockers

1. Provider-specific idempotency, key namespace, same-key lookup, receipt authenticity and definitive no-handoff semantics must be proven separately for every production provider. Generic exactly-once is not assumed.
2. CSubmitOutcome must survive process death between provider handoff and durable C ledger/COC append. If no authoritative same-key recovery exists, outcome remains UNKNOWN/IN_DOUBT.
3. C-PO-01..10 and provider-specific crash/timeout/duplicate/failover tests remain SPECIFIED / NOT RUN.
4. H semantic validators, cross-language canonical-byte fixtures and cryptographic trust-profile verification remain NOT RUN / OPEN.
5. C cannot release I Gate, D Forget Fence, Storage locks, COC RecoveryEpoch or G Applied.
6. No provider-vendor approval, runtime conformance, production activation, Global Forget E2E or physical erasure is claimed.

## 8. Final disposition

**ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS.** The C Provider Outcome authority boundary and the S0a–S4 union-manifest recovery contract are semantically aligned in the exact reviewed bundle. H schema 1.2.5 carries the necessary typed C owner admission and outcome evidence shape. Provider-specific idempotency/recovery and executable conformance remain activation blockers.

This is a delegated role review, not an independent human C Owner signature or production approval.
