# Phase 3.6.8.1 — C Exact-Version Re-review: Provider Outcome and Complete Union Manifest

- Owner perspective: C — Agent Integration / Provider Side-Effect Boundary
- Status: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS — EXACT BLOB REVIEW**
- Storage v3.2.1 Blob: `491e8e916cf9b1609c5220fb41fb766b8cddccf2`
- Superseded Storage v3.2 Blob: `e7ab80cdf8af5e0d50c407b06a5deb618d1e2ae6` (review predecessor only)
- Companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- C source contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- I Phase 3.6.8 proposal Blob: `929b30ba10ac627927d3959e0777b467846b268d`
- D Phase 3.6.8 proposal Blob: `0668667daeb936bf223ab049277ea2a4117c3b09`
- Prior C review of v3.2 Blob: `f538d921d06c92dfaba13fbe326a80d6550fe1b7`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 1. C exact-version decision

**C DECISION: ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**, limited to C's authenticated final-request boundary, provider invocation, provider idempotency namespace, owner-local provider admission inventory and actual provider outcome evidence.

C accepts the corrected v3.2.1 sequence:
1. **S0a:** I/D/C close their own admission gates and freeze owner-local ledgers/high-waters first.
2. **S0b:** after COC quorum returns, freeze the linearizable COC prefix P.
3. **S1:** build the complete canonical union manifest of COC participants at/before P and applicable owner-local I/D/C admissions through their frozen high-waters, including not-yet-COC-registered work.
4. **S2:** quorum-commit the Recovery Cutoff Batch binding P, all owner snapshots and the union ManifestId/Digest/count.
5. **S3:** quorum-commit the separate Manifest Record referencing the exact prior Batch position/digest and carrying the exact union member payload.
6. **S4:** linearly read back both records and verify all cross-bindings, owner generations and high-water completeness.
7. Only after S4 may participant-specific recovery/reconciliation begin.

This corrects the important race in the predecessor v3.2 ordering: owner-local admission is frozen before P, and an already admitted C operation cannot disappear merely because it has no COC ParticipantIntentRef yet.

## 2. C manifest membership and provider admission

C's frozen owner snapshot MUST enumerate every C-owned protected provider operation through the captured C high-water, including:
- reservation created but provider not invoked;
- provider invocation started, response/ACK lost;
- provider handoff accepted/rejected but CSubmitOutcome persistence or COC append delayed;
- same-key provider lookup pending;
- worker restart/retry/replay and contradictory outcome evidence;
- operation admitted but not yet assigned/registered as a COC ParticipantIntentRef.

Each such entry is represented as an `OWNER_LOCAL_ADMISSION` manifest member with C OwnerAdmissionRef, C ledger ref/version, request digest, provider idempotency-key reference and explicit null COC ParticipantIntentRef when no COC registration exists. Once a typed immutable join exists, the same member may also carry its COC ParticipantIntentRef. Shared TransactionId, timestamp similarity or matching text is not sufficient for deduplication.

The complete manifest is the union of COC-committed participants and I/D/C owner-local admissions. Every frozen C ledger member MUST appear exactly once or carry an authoritative C-signed, scope-specific exclusion proof. An absent COC record is never an exclusion reason.

## 3. Provider Outcome remains independent and C-owned

C alone emits `CSubmitOutcome` from actual provider/runtime boundary evidence. The outcome is not derivable from I COMMIT_WON, D clearance, Storage COMMITTED/PublicationReceipt, COC Batch/Manifest commit, H ACK or G Applied.

The immutable C outcome binds CSubmitOutcomeRef/digest, authenticated C adapter/runtime boundary, provider identity, stable provider idempotency-key reference, provider request/receipt references, actual InferenceRequestId when supplied, FinalRequestBoundaryId, exact final request digest, TransactionRef, ParticipantReservationRef, ParticipantIntentRef or OwnerAdmissionRef, and the exact JF-10 participant/attempt/ledger/tuple plus I/D/Storage evidence refs where applicable.

Outcome states remain:
- `HANDOFF_ACCEPTED`: authoritative provider acceptance/handoff for the exact request and same key, with provider receipt evidence;
- `HANDOFF_REJECTED`: definitive no-handoff proof;
- `NOT_INVOKED`: distinct pre-provider disposition;
- `UNKNOWN/IN_DOUBT`: timeout, crash, lost ACK, contradictory evidence or unavailable authoritative same-key lookup.

A provider receipt is not an inference-completion result. HANDOFF_ACCEPTED does not prove content correctness, user delivery or G Applied.

## 4. C provider invocation and recovery gate

For a new protected provider invocation, C requires exact COC participant intent, Storage prepared participant registration where JF-10 applies, I COMMIT_WON for the complete immutable participant tuple, current D lineage-bound clearance/fence predicates, current C reservation/final-request digest and COC serving state.

During COC recovery, no new provider invocation, provider retry, Storage resolution or visibility publication is allowed after S2 or S3 alone. S4 read-back must succeed first. After S4, an already invoked UNKNOWN operation may only be reconciled using the same provider idempotency key and immutable request/participant tuple. A repeat invocation is permissible only if the provider-specific contract proves same-key idempotency; otherwise UNKNOWN remains blocking and I/D barriers remain held.

C does not release I or D Gate/Fence, Storage locks, COC RecoveryEpoch or G Applied.

## 5. Exact S0–S4 assessment

| Step | C disposition | C safety condition |
|---|---|---|
| S0a owner-local freeze | ACCEPT | C provider admission and outcome ledger high-water captured atomically with C gate close |
| S0b Prefix P | ACCEPT | no protected COC append after P; pre-P admitted C work still included via owner ledger |
| S1 union Manifest | ACCEPT | all C local admissions included or C-signed scoped exclusion; no null/absent treated as empty |
| S2 Batch | ACCEPT | binds exact C snapshot and union digest; no provider side effect permitted |
| S3 Manifest Record | ACCEPT | references exact Batch position/digest and exact canonical union |
| S4 read-back | ACCEPT | verify order, digest, count, P, RecoveryEpoch and owner generations before recovery |

## 6. Enumerated C-owned exceptions and tests

1. Provider-specific same-key idempotency, query semantics, receipt authenticity and crash/failover recovery remain to be proven per production provider. Generic exactly-once semantics are not assumed.
2. A provider response observed only in volatile memory is not durable terminal C evidence. If crash occurs between provider handoff and CSubmitOutcome persistence, authoritative same-key recovery is required or state remains UNKNOWN.
3. C must preserve the original provider key and immutable request tuple across retries/reconnect; same key with changed request digest/participant tuple is CONFLICT.
4. C-PO-01..10 remain SPECIFIED / NOT RUN. They must be supplemented with a pre-COC-registration admission discovered in the C frozen ledger and an S0a/S0b race test.
5. No production provider integration, adapter runtime, COC quorum, or end-to-end Forget proof is claimed.

**Disposition:** C accepts exact Storage v3.2.1 and companion COC §14 Blob 8ac178 for C's Provider Outcome and provider-side-effect boundary with the above exceptions. This is an assistant-authored role-based exact-version review, not independent human Owner signature, provider-vendor approval, implementation PASS or production authorization.

## 7. Provenance

Assistant-authored role-based C re-review proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human C Owner authorship or approval.
