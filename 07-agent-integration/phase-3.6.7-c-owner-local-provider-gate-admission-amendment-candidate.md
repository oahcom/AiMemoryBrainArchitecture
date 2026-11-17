# Phase 3.6.7 — C Provider-Side-Effect Gate, Admission Inventory & Recovery Snapshot

- Perspective: C — Agent Integration
- Status: **COORDINATOR-PREPARED C-ROLE SEMANTIC AMENDMENT CANDIDATE — INDEPENDENT C REVIEW REQUIRED**
- Exact integration target: A Blob a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d; Storage v3.1 Blob d5bdc72f193fcdaa654e4f07f865b77c578673ca; COC companion Blob 8ac17816476f280ab6fb3afca0688aa03e37de1d
- Scope: R1/R2 only; does not replace C's existing provider outcome contract
- Implementation / deployment / conformance: NOT IMPLEMENTED / NOT DEPLOYED / NOT RUN

## 1. Authority boundary

C owns its provider-side-effect admission gate, provider request identity, provider idempotency namespace, provider invocation ledger and actual provider-boundary outcome evidence.

I alone owns authorization, PermissionEpoch, receipt issuance/consumption and I terminal decision. D alone owns ForgetFence, lineage and D barrier clearance. COC owns quorum-committed causal ordering and participant accounting. Storage owns prepared-XID resolution and visibility. H owns wire representation. A owns integration acceptance.

C's local gate is a fail-closed C admission control. It is not an I authorization decision, D Forget decision, COC cutoff decision or Storage visibility decision. C cannot use its gate to override an I/D result.

## 2. C Gate linearization

### 2.1 Durable close operation

C MUST implement one durable linearizable local transaction or formally equivalent single-writer CAS over an append-only C admission state machine. The successful commit is the C Gate close linearization point.

The operation atomically:
1. authenticates the recovery/outage trigger and binds its stable identity/digest;
2. increments monotonic CGateGeneration;
3. changes the affected provider-admission gate to CLOSED/PENDING;
4. appends the immutable gate-close event;
5. captures C's provider-admission ledger high-water, invocation-attempt high-water, exact member count and canonical member-set root;
6. captures each in-flight member's exact COC registration state, I/D proof references and provider-boundary state;
7. persists an independent anti-rollback anchor and snapshot generation;
8. returns a C-signed CProviderGateCloseAttestation only after durable commit.

No request is acknowledged as pending before the close transaction commits. A process mutex, cache flag, queue pause, COC append ACK or timestamp is not a substitute.

### 2.2 Admission race

Every C operation that can create or advance a protected provider side effect MUST serialize against the same current CGateGeneration. This includes:
- creation/finalization of ParticipantReservationRef;
- issuance of a provider invocation permit;
- transition to INVOCATION_IN_PROGRESS;
- provider retry/replay authorization;
- provider outcome terminalization and same-key recovery.

For a racing operation:
- If its C admission transaction commits before Gate close, its immutable C ledger entry is included at or below the captured high-water and remains an in-flight recovery member.
- If Gate close commits first, no new reservation or provider invocation permit may be admitted.
- If order or durable state is uncertain, the operation is UNKNOWN/IN_DOUBT and no new provider invocation is allowed.

The C gate check and durable reservation/permit admission MUST be in the same transaction or equivalent CAS. A check-then-act gap is prohibited.

### 2.3 Pre-close permit semantics

A provider invocation permit durably admitted before C Gate close is a pre-close in-flight member; it is not silently cancelled and is not a new post-close admission. It may proceed only for the exact immutable request and only if all existing C prerequisites are still authoritative:
- exact I COMMIT_WON for the bound final-gate participant and complete tuple;
- every required D clearance/fence predicate for that operation;
- exact COC participant intent/reservation binding;
- stable provider idempotency key and namespace;
- no contradictory, stale or UNKNOWN evidence.

A permit does not prove that the provider was called. C records the actual provider boundary outcome separately. If any prerequisite is missing, revoked, contradictory or UNKNOWN, the permit remains blocked and C records no provider handoff.

This rule preserves the distinction between an operation admitted before a gate close and a provider side effect that actually occurred. The C Gate does not retroactively rewrite the I/D/COC order.

## 3. C In-Flight Provider Admission Ledger

C MUST maintain a durable append-only ledger for every protected provider operation from the first C admission through authoritative terminal outcome.

Each entry MUST include at least:
- CausalOrderTransactionRef, ParticipantIntentRef and exact COC position/digest where registered;
- explicit COC registration state: REGISTERED or NOT_REGISTERED, with reason;
- FinalRequestBoundaryId, immutable request identity/digest, canonical request bytes reference and context/delivery references;
- authenticated principal/actor/agent/adapter/runtime/session and exact owner boundary;
- PolicyDomainRef, PermissionEpoch and CommitAuthorizationReceiptRef/digest;
- IAuthorizationTerminalRef and exact outcome, including COMMIT_WON versus non-success/UNKNOWN;
- ForgetOperationRef, ForgetFenceGeneration, DParticipantClearanceRef and affected-lineage proof;
- ParticipantReservationRef and reservation digest;
- provider name, idempotency namespace, stable provider idempotency key and key-retention profile;
- C-local sequence, CGateGeneration, ledger ref/version and attempt high-water;
- invocation state: NOT_PERMITTED, PERMITTED_NOT_INVOKED, INVOCATION_IN_PROGRESS, ACCEPTED_WITH_HANDOFF_EVIDENCE, REJECTED_WITH_NO_HANDOFF_PROOF, UNKNOWN;
- provider receipt, actual InferenceRequestId and authoritative provider lookup evidence where applicable;
- retry/replay ancestry, worker/lease identity, lost-ACK state and terminal proof digest;
- anti-rollback anchor, recovery epoch and audit metadata.

An entry MUST be durably appended before C returns a reservation/permit or allows the operation to cross the corresponding C-owned boundary. COC registration remains required before any provider side effect under the existing C contract. A missing COC ACK is resolved by exact same-identity/digest lookup; it is never treated as proof of non-registration or permission to mint a replacement operation.

## 4. Recovery snapshot and completeness

C produces an immutable CProviderAdmissionSnapshot bound to:
- C authority and CGate ref/generation;
- exact recovery epoch and COC prefix/batch/manifest refs when known;
- C admission high-water and provider invocation-attempt high-water;
- canonical ordered member identities, count, root and retrievable ledger snapshot;
- per-member COC registration state and exact ParticipantIntentRef where registered;
- per-member I/D/Storage evidence refs and provider-boundary state;
- provider idempotency namespace/key and authoritative lookup status;
- anti-rollback anchor, signer/key version and snapshot generation.

The set status is explicit:
- COMPLETE_NON_EMPTY; or
- COMPLETE_EMPTY with canonical empty member array, count zero and the canonical empty-set digest.

NOT_ENUMERATED, UNAVAILABLE, PARTIAL or UNKNOWN is never equivalent to COMPLETE_EMPTY.

C must include operations admitted before C Gate close even when provider invocation has not started, including reservations with lost ACKs, expired leases, worker restarts and COC projection lag. Queue emptiness, missing worker, timeout or missing provider receipt does not prove absence.

The C snapshot is separate from the COC prefix participant manifest. COC enumerates only intents committed in its exact prefix. C's own ledger additionally accounts for C admissions that have not yet appeared in that prefix. The Recovery Cutoff Batch binds both evidence families by exact refs/digests; it does not invent ParticipantIntentRefs for C-only entries.

## 5. Post-high-water and repeated cutoff rounds

An admission request that arrives after C's captured high-water while the C gate remains closed MUST be rejected or held in a non-invokable quarantine lane. It MUST NOT be silently added to the already committed snapshot.

If C accepts a later request into a protected admission ledger after the current snapshot, C must advance its local high-water and produce a subsequent immutable snapshot/recovery cutoff round before releasing its gate. Any high-water or relevant scope-generation advance invalidates the prior C release proof.

Same request identity + same digest is idempotent. Same identity + changed digest is immutable CONFLICT. A new attempt cannot change the logical provider operation or idempotency key.

## 6. Independent C Gate release

Only C may issue a monotonic CProviderGateReleaseReceipt. C may release its outage/pending admission gate only after:
1. exact COC RecoveryEpoch, committed prefix, Recovery Cutoff Batch and participant manifest are linearly verified;
2. the C snapshot is complete and its explicit empty/non-empty status is verified;
3. every C entry at/below the captured high-water has an authoritative disposition;
4. every provider invocation is either proven not invoked, proven accepted/rejected with authoritative boundary evidence, or remains explicitly UNKNOWN and blocks release where it can affect protected side effects;
5. every pre-close reservation/permit is joined to exact I/D/COC/Storage evidence;
6. provider same-key lookup/idempotency behavior is reconciled; no timeout or lost ACK is treated as a terminal outcome;
7. C's current high-water, gate generation, scope generation and anti-rollback anchor remain unchanged or are covered by a subsequent cutoff round;
8. no unrepresented C admission exists.

The receipt binds exact C Gate ref/generation, C high-waters, snapshot root/count/status, RecoveryEpoch, COC prefix/batch/manifest digests, reconciliation root and signer/key version.

C Gate release means only that C's local outage admission suspension has been reconciled. It does not mean provider success, I authorization, D Forget completion, Storage visibility, COC recovery completion or G Applied.

## 7. Failure rules

- COC unavailable or no quorum-confirmed prefix: no new protected intent, reservation or provider invocation.
- I result REVOCATION_WON / INDETERMINATE_ABORTED: no provider invocation; preserve same participant for same-XID rollback/reconciliation.
- I UNKNOWN/IN_DOUBT: no provider invocation.
- D predicate missing/stale/UNKNOWN: no provider invocation.
- lost C reservation/permit ACK: authoritative lookup by original C identity/digest; no replacement operation.
- lost provider response or ambiguous handoff: UNKNOWN/IN_DOUBT; use the same provider key and authoritative lookup where supported; never blindly resubmit with a new key.
- stale snapshot, rollback, incomplete ledger, missing owner evidence or contradictory provider result: C Gate remains closed.

## 8. Required conformance cases (not run)

1. concurrent C Gate close versus reservation finalization;
2. concurrent C Gate close versus provider-permit issuance;
3. lost Gate-close ACK and exact idempotent readback;
4. operation admitted before close but not yet provider-invoked;
5. provider invocation in progress when Gate closes;
6. COC ParticipantIntent committed but C response ACK lost;
7. C ledger entry admitted but COC projection not yet visible;
8. explicit COMPLETE_EMPTY versus NOT_ENUMERATED;
9. post-high-water admission rejected or assigned to a subsequent cutoff round;
10. I abort/UNKNOWN and D UNKNOWN prohibit provider invocation;
11. provider response loss preserves same idempotency key;
12. C release attempted with an unresolved provider outcome;
13. restored C ledger rollback or anti-rollback anchor mismatch;
14. same C operation identity with changed request digest.

**Disposition:** This is a coordinator-prepared C-role semantic amendment candidate. It is not a C Owner decision, provider adapter conformance, implementation PASS, production activation or proof of exactly-once provider behavior. Independent C review and A integration remain required.
