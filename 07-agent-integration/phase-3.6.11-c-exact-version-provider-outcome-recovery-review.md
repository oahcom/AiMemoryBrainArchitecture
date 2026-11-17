# Phase 3.6.11 — C Exact-Version Review: Provider Outcome × Recovery Batch/Manifest

- Role: C — Agent Integration / actual provider egress authority
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: assistant-authored delegated C role review at the user's direction; not an independent human C Owner signature.
- Status: architecture review only; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED

## 0. Exact review bundle

| Artifact | Blob |
|---|---|
| A COC architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| Storage Phase 3.6.12 ordering/bundle amendment | `1c8c0bc11798293293bcf47fa560f1699a5bcfe0` |
| COC base protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| Storage/COC two-phase ordering amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` |
| I Phase 3.6.8 | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C owner-local gate/provider amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` |
| H two-phase wire/validator addendum | `5a3def4f7e84ed489993681455b6840b93ecc282` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |

## 1. C authority and Provider Outcome ruling

C alone owns the actual provider/runtime egress boundary, C admission/reservation/provider-attempt ledger, provider-specific idempotency namespace, immutable CSubmitOutcome and C outage-gate release.

C confirms the authority separation:
- COC intent, RecoveryCutoffBatch and ParticipantManifest prove ordering and committed-prefix membership only.
- I `COMMIT_WON` proves I authorization/receipt consumption only.
- D clearance proves D's owner-local lineage/fence predicate only.
- Storage PreparedParticipantReceipt proves one exact participant is prepared and private only.
- C reservation or `DISPATCH_AUTHORIZED` does not prove request bytes crossed the provider boundary.
- H receiver ACK does not prove provider success.
- Only C's actual egress observation plus provider-specific authoritative same-key reconciliation can establish the CSubmitOutcome.

The C 3.6.9 amendment's final egress generation check, C-local pre-COC admission inventory, same-key retry and UNKNOWN/IN_DOUBT rules are accepted as the correct semantic boundary.

## 2. C-M1 — Required typed CSubmitOutcome tuple

Before any future wire/schema freeze, every CSubmitOutcome MUST bind at minimum:
- CAdmissionRef and immutable C admission sequence/generation;
- CProviderAttemptRef + ProviderAttemptGeneration;
- exact CausalOrderTransactionRef, ParticipantIntentRef, ParticipantReservationRef and COC position/digest when registered;
- ProviderRef, provider idempotency namespace and exact idempotency key reference;
- FinalRequestBoundaryId, exact final request digest, scope binding and authenticated runtime/adapter identity;
- current CGateGeneration checked at the egress boundary;
- exact I terminal proof ref/digest and D clearance/fence-generation proof ref/digest;
- egress disposition, one of `NOT_SENT`, `SENT_OR_AMBIGUOUS`, `OUTCOME_KNOWN`;
- provider outcome, one of `ACCEPTED`, `REJECTED_NO_HANDOFF`, `UNKNOWN`;
- actual provider receipt/reference and actual InferenceRequestId when returned;
- authoritative observation source, observation digest and same-key lookup evidence where required;
- append-only attempt ancestry and terminal/no-effect proof.

The wire contract must distinguish the egress disposition from provider outcome. `NOT_SENT` is a C-authoritative no-egress proof; `SENT_OR_AMBIGUOUS` is nonterminal; `OUTCOME_KNOWN` is terminal only with a determinate provider receipt or authoritative same-key lookup. `UNKNOWN` never becomes success or safe abort by timeout.

## 3. C-M2 — Final egress serialization

Immediately before request bytes are released to the provider transport, C's egress adapter must atomically validate:
- current CGateGeneration and CAdmissionRef;
- exact reservation and one-use ProviderAttemptRef/Generation;
- exact final request digest and boundary;
- I COMMIT_WON proof and single-use consumption identity;
- current D clearance and FenceGeneration/lineage scope;
- provider idempotency key binding.

If the gateway cannot serialize the final send boundary against Gate close, it cannot claim NOT_SENT or SENT; it records UNKNOWN and suppresses additional sends. A pre-close SENT_OR_AMBIGUOUS attempt is captured in the C snapshot and reconciled with the same provider key. A post-close reserved/queued/NOT_DISPATCHED attempt cannot send.

## 4. C-M3 — Provider idempotency and ambiguous outcomes

Exactly-once provider behavior is not assumed. Before production activation, each provider adapter must prove:
- idempotency key scope and retention horizon;
- same-key lookup semantics and authoritative result source;
- behavior for duplicate send, timeout after send, connection reset and provider-side acceptance with lost response;
- whether a definitive no-handoff result exists;
- no retry-as-new-operation, no replacement CAdmissionRef, no new ParticipantIntent and no new XID to escape ambiguity.

If the provider lacks authoritative same-key lookup after an ambiguous send, the participant remains IN_DOUBT indefinitely and C/I/D release predicates remain blocked.

## 5. C-M4 — Batch/Manifest is not Provider Outcome

C accepts the two-phase COC ordering:
1. freeze I/D/C snapshots and exact COC prefix P;
2. enumerate participants at P and precompute ManifestId + ParticipantManifestContentDigest;
3. commit Batch binding ManifestId/content digest and exact owner snapshots;
4. commit Manifest after Batch with exact BatchRef/BatchDigest back-reference;
5. linearly read back and verify the pair;
6. only then reconcile participants.

The Manifest accounts for COC-registered participants in P. C's owner-local admission snapshot separately accounts for all C-accepted work, including NOT_REGISTERED admissions. A C admission cannot be fabricated into a COC ParticipantIntent. Conversely, a manifest entry is not a C provider outcome.

C's release requires every C admission/provider attempt to have a determinate provider outcome or authoritative no-egress proof. A participant-set match alone is insufficient.

## 6. C-M5 — H schema dependency

H schema 1.0.5 correctly separates ParticipantManifestContentDigest from ParticipantManifestRecordDigest and provides the Batch/Manifest back-reference fields. C accepts this as the recovery-cutoff evidence shape, subject to H's semantic validators.

However, the reviewed Recovery Cutoff 1.0.5 and JF-10 bridge 1.1.0 schemas do not themselves define a dedicated `C_SUBMIT_OUTCOME_RECORDED` / `CSubmitOutcome` message family. C's provider outcome semantics must therefore remain an explicit C-owned evidence contract until H publishes a separately versioned strict wire schema (or an exact mapped schema family) for it. This gap must not be papered over by reusing the Recovery Cutoff manifest or JF-10 Storage receipt schema.

## 7. C decision

**ACCEPT WITH ENUMERATED AMENDMENTS C-M1 through C-M5.**

C accepts the Storage two-phase Batch/Manifest ordering and H Recovery Cutoff schema 1.0.5 as a sound candidate for recovery membership evidence. C accepts its own 3.6.9 provider gate/effect-boundary model as the required semantic source. C does not accept any interpretation that COC or H can mint CSubmitOutcome or infer provider success.

This disposition is limited to C's authority over provider egress and C-owned outcome evidence. It does not approve I policy, D Forget semantics, Storage prepared-XID resolution, COC deployment or H cryptographic policy.

## 8. Required conformance evidence — specified, not run

- Gate close wins immediately before egress: zero provider bytes.
- Egress serialization wins immediately before Gate close: captured pre-close attempt and same-key reconciliation.
- Lost provider ACK after bytes sent: same-key lookup, no new attempt.
- Provider no same-key lookup after ambiguous send: IN_DOUBT, no C release.
- Batch committed, Manifest absent: no participant reconciliation or C release.
- Batch/Manifest pair valid but C local admission is NOT_REGISTERED: same stable C admission remains blocking until registered or no-effect terminalized.
- Manifest membership with no CSubmitOutcome: no provider success inference.
- Provider ACCEPTED/REJECTED outcome bound to wrong request digest, attempt or idempotency key: INVALID.
- C release with one UNKNOWN provider attempt: rejected.
- Replay with same C admission/key/digest: idempotent; changed digest: CONFLICT.

## 9. Status and provenance

This is an assistant-authored delegated C role review. It is not independent human C Owner approval. No provider adapter, same-key recovery, egress fencing, C-CO test, schema interoperability, production deployment or activation has been executed or verified.
