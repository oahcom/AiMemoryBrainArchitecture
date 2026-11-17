# Phase 3.6.8.2 — C Exact-Version Re-review: Storage v3.2.2 + Current I/D Admission Tuple

- Owner perspective: C — Agent Integration / Provider Side-Effect Boundary
- Status: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS — EXACT BUNDLE REVIEW**
- Storage v3.2.2 Blob: `4039fd4c08aa0bb7da63fe5dab92e419487f48d1`
- Companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Current I Phase 3.6.8 Blob: `cf4b76f151204fa47b156b5d807e7378c28fd268`
- Current D Phase 3.6.8 Blob: `2d95099a2e19a8cbec325925b70da576f73d9899`
- C source contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- Prior C v3.2.1 re-review Blob: `377c16531d5d8b43b353a09f61ebac9e999fc48d`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 1. Decision and scope

**C DECISION: ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**, limited to C's owner-local protected admission ledger, provider invocation boundary, provider idempotency namespace and actual Provider Outcome evidence.

C accepts Storage v3.2.2's complete order:
1. I/D/C close their own gates and freeze owner-local ledgers/high-waters/roots (S0a);
2. COC quorum recovers and freezes exact prefix P (S0b);
3. S1 constructs the canonical union of COC participants at/before P and applicable I/D/C owner-local admissions through frozen high-waters;
4. S2 commits the Recovery Cutoff Batch bound to P, owner snapshots and ManifestId/Digest/count;
5. S3 commits the separate Manifest Record referencing the exact prior Batch position/digest and carrying the complete union;
6. S4 linearly reads back both records and verifies all cross-bindings;
7. only then may participant recovery/reconciliation begin.

C confirms the v3.2.2 binding now pins the current I and D Phase 3.6.8 proposal Blobs, rather than the earlier versions pinned by v3.2.1. C's previous v3.2/v3.2.1 reviews do not transfer to v3.2.2; this artifact is the exact current review.

## 2. C owner-local admission and manifest union

C's owner-local high-water MUST include every protected provider operation that was admitted before C Gate close, including reservation not yet finalized, invocation started, provider response/ACK lost, provider outcome known locally but not durably recorded, same-key lookup pending, and work not yet registered in COC.

Each such C ledger member appears as `OWNER_LOCAL_ADMISSION` with:
- OwnerKind=C, OwnerAdmissionRef and immutable admission digest;
- C owner-ledger ref/version/root, local sequence and frozen high-water;
- request/operation digest, admission phase and provider idempotency-key reference;
- associated ParticipantIntentRef if authoritatively joined, otherwise explicit COC ParticipantIntentRef=null plus reason.

A COC ParticipantIntentRef absent from the prefix does not remove the C owner admission from the manifest. Deduplication requires a typed immutable cross-reference proving the same operation/attempt. Every C ledger member appears exactly once or has a C-signed scope-specific exclusion proof.

## 3. Provider Outcome semantics

C alone authors CSubmitOutcome from the actual provider/runtime boundary. It binds CSubmitOutcomeRef/digest, provider/adapter identity, stable provider idempotency-key reference, provider request/receipt, actual InferenceRequestId when supplied, FinalRequestBoundaryId, exact request digest, TransactionRef, ParticipantReservationRef, OwnerAdmissionRef, optional COC ParticipantIntentRef, and the applicable I/D/Storage participant/attempt/ledger/tuple evidence.

Outcomes:
- `HANDOFF_ACCEPTED`: authoritative provider acceptance for the exact request/key, with provider receipt evidence;
- `HANDOFF_REJECTED`: definitive no-handoff proof;
- `NOT_INVOKED`: pre-provider disposition, not provider rejection;
- `UNKNOWN/IN_DOUBT`: unresolved/contradictory/timeout/lost ACK/lookup unavailable, durable and blocking.

Storage COMMITTED/PublicationReceipt, I COMMIT_WON, D clearance, COC Batch/Manifest, H ACK and G Applied cannot synthesize C provider outcome. HANDOFF_ACCEPTED is not inference completion, content correctness, user delivery or G Applied.

## 4. Cross-owner tuple alignment

C reviewed the current I/D amendments for their C-facing obligations:
- I's exact I Gate generation, PermissionEpoch, request ledger, ProducerDomainInventoryEpoch/registry currentness, key-status generation, sequencer and Restore tuple remain independent; C does not compare or mint them.
- D's FenceGeneration, publication boundary fencing, barrier membership/closure and current I evidence remain D-owned; C supplies its own provider outcome evidence for crossed side-effect members.
- D's terminalization requires CSubmitOutcomeRef/digest for any barrier member that crossed or may have crossed the provider boundary. If invocation was forbidden, C must provide authoritative C-owned non-invocation proof; absence of COC row/worker is not proof.
- UNKNOWN provider outcome, missing same-key evidence or mismatch of provider idempotency namespace/request digest keeps the D barrier and relevant owner Gates blocking.

C accepts these cross-owner references as consistent with C's own Provider Outcome contract. C does not approve I's key lifecycle/crypto policy, D's Forget semantics outside the provider evidence join, or Storage's database implementation.

## 5. Recovery-time provider rules

No new provider invocation, retry, Storage resolution or visibility publication is permitted after S2 or S3 alone. S4 must pass. After S4, an already invoked UNKNOWN operation may only be reconciled using the same provider idempotency key and immutable request/participant tuple. A repeat invocation is allowed only if the specific provider contract proves same-key idempotency. Otherwise UNKNOWN remains blocking and C does not retry as a new transaction.

## 6. Enumerated C-owned exceptions and tests

1. Provider-specific same-key idempotency, receipt authenticity, lookup behavior and crash/failover recovery remain to be proven per provider. Generic exactly-once is not assumed.
2. C's response observation must be durably recorded; volatile in-memory response is not terminal evidence.
3. C-PO-01..10 and provider-specific crash/timeout/duplicate/failover tests remain SPECIFIED / NOT RUN.
4. C does not release I Gate, D Forget Fence, Storage locks, COC RecoveryEpoch or G Applied.
5. No runtime, production provider, interoperability or Global Forget E2E result is claimed.

**Disposition:** C accepts exact Storage v3.2.2 + companion COC §14 Blob 8ac178 with the current I/D proposal blobs above, subject to the enumerated C-owned exceptions. This is an assistant-authored role-based review, not independent human Owner signature, provider-vendor approval, implementation PASS or production authorization.

## 7. Provenance

Assistant-authored role-based C exact-bundle re-review committed at the user's direction. It is not a cryptographic signature and does not prove independent human C Owner authorship or approval.
