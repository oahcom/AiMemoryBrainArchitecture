# Phase 3.6.7 — I Owner-Local Atomic Gate, Admission Inventory & Independent Release

- Owner perspective: I — Security & Governance
- Status: **OWNER-BRANCH SEMANTIC AMENDMENT CANDIDATE — INDEPENDENT I REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 1. Authority boundary

I alone owns the PolicyDomain permission/revocation Gate, PermissionEpoch, receipt issuance/consumption, I request ledger and I Gate release. COC records ordering/evidence only. D owns its Forget Gate and lineage barrier. Storage owns prepared participant durability and visibility. No COC batch, Storage receipt, D receipt or A integration decision can release I's Gate.

This amendment is scoped to the current Storage Design v3.1 Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca` and COC companion Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d`. Storage Design v2 Blob `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` is retained as historical predecessor only; it lacks the §§15.1–15.7 required by the current COC protocol.

## 2. Atomic Gate linearization

### 2.1 Required primitive

I MUST provide one linearizable, durable owner-local transaction (or a formally equivalent single-writer CAS over a durable append-only state machine) that atomically:
1. validates the authenticated request identity, PolicyDomainRef, Scope and canonical request digest;
2. advances the monotonic `IGateGeneration`;
3. changes the affected gate from OPEN to CLOSED/PENDING;
4. appends the immutable request to the I Pending Admission Ledger;
5. captures the request-ledger high-water/cursor and exact set root/count;
6. persists an anti-rollback anchor and returns an I-signed GateCloseAttestation.

The **linearization point** is the successful durable commit/CAS that makes both Gate=CLOSED and the corresponding request-ledger entry/high-water visible together. Before that point the request is not acknowledged as pending. After that point all affected receipt issuance/consumption and protected admission must observe the closed generation. There is no state in which the request is acknowledged but absent from the captured inventory.

A process-local mutex, cache, queue ACK, COC append, timestamp, or separate “close then enumerate” sequence is not sufficient.

### 2.2 Racing request rule

Every request racing the close operation has exactly one outcome:
- included in the closed snapshot at or below captured `IRequestHighWater`; or
- assigned a later I request sequence and remains behind the still-closed Gate for the next Recovery Cutoff Batch.

The gate remains closed across retries, leader changes, COC outage, restore and lost ACK. Same request ID + same digest is replay; same ID + changed digest is CONFLICT.

### 2.3 Request scope

Gate close applies to the exact PolicyDomainRef and normalized Scope binding in the request. Unknown or ambiguous scope expands to the conservative protected scope or is rejected; it MUST NOT be silently narrowed. Independent PolicyDomains are not ordered by wall clock or by D's sequence.

## 3. In-flight Admission Ledger — mandatory inventory

I's ledger MUST include all work that can issue, consume, authorize, or rely on an I decision, whether or not it has reached COC or Storage.

Minimum entry fields:
- `IRequestRef`, stable `RequestId`, `RequestDigest`, idempotency key and request type;
- `PolicyDomainRef`, normalized `ScopeRefs`, scope-binding fingerprint, affected action/resource/subject;
- `IGateGeneration`, I-local sequence, ledger ref/version and admission high-water;
- `PermissionEpochBefore`, proposed/committed epoch, revocation/authorization decision ref;
- `CommitAuthorizationReceiptRef`, receipt digest, issue/consume status and single-use consumption identity;
- transaction/participant refs: `TransactionRef`, `ParticipantIntentRef`, `PreparedParticipantRef`, `PrepareAttemptRef`, `ParticipantLedgerRef/Version`, COC intent ref/digest;
- issuer/recipient identity, audience, signer/key version and verification status;
- operation state, admission state, retry/replay ancestry, lease/worker identity if applicable;
- durable effect boundary: NOT_ISSUED, ISSUED, CONSUMPTION_ATTEMPTED, CONSUMED, REVOKED, UNKNOWN;
- terminal evidence refs/digests, unresolved reason, recovery epoch, anti-rollback anchor and audit metadata.

Mandatory inventory classes:
1. admitted before Gate close and not yet COC registered;
2. receipt prepared/issued but response ACK lost;
3. receipt issuance in progress;
4. receipt consumption in progress or response uncertain;
5. COC participant intent committed but I terminal decision not yet recorded;
6. final-gate I decision prepared but not durably consumed;
7. I decision consumed but Storage/COC observation delayed;
8. retry, replay, duplicate delivery, expired lease or worker restart;
9. restored/replayed entries and requests discovered after the captured high-water.

No item may be omitted because it lacks a COC ParticipantIntentRef. The I ledger is the authority for I-local admission completeness.

## 4. Recovery Cutoff Batch binding

I produces an immutable `IRequestSnapshotAttestation` bound to:
- exact I Gate ref/generation and status;
- PolicyDomainRef and scope-binding fingerprint;
- request high-water/cursor, count, canonical ordered member refs and digest/root;
- current PermissionEpoch and I sequencer position;
- unresolved receipt issue/consume set and participant cross-reference digest;
- anti-rollback anchor, signer/key version and snapshot generation;
- RecoveryEpoch and exact COC prefix/batch/manifest refs once available.

The COC Recovery Cutoff Batch must bind the exact I attestation and exact D attestation as separate typed fields. It MUST NOT merge or compare their owner-local sequence values.

I verifies before batch attestation that its request set is complete and internally consistent. After batch/manifest commit, I re-reads its local ledger at the captured generation and checks exact set equality. Any post-high-water admission remains gated and requires a subsequent batch or an I-authoritative proof that it is outside scope.

## 5. Independent I Release conditions

I may release only the I outage/pending Gate, through a new I-signed monotonic `IGateReleaseReceipt`, when ALL conditions hold:

1. Exact COC RecoveryEpoch, committed prefix, Recovery Cutoff Batch and participant manifest are linearly verified; batch/manifest digest, count and prefix agree.
2. Every I request at or below the captured high-water is represented exactly once and has an authoritative I disposition.
3. Every in-flight receipt issuance/consumption has a terminal or explicitly safe non-effect proof. UNKNOWN, lost ACK, expired lease or missing worker remains blocking.
4. Every I decision that could authorize a Storage participant is bound to the exact PreparedParticipant tuple, DB incarnation, prepare attempt, participant ledger version, owner boundary, PolicyDomainRef, PermissionEpoch and COC prepare-intent digest.
5. Every receipt consumption is proven single-use and consistent with I sequencer order; stale or replayed receipts are rejected.
6. I's current PermissionEpoch, sequencer position, registry/key status and anti-rollback anchor are current and non-forked.
7. No request after the captured high-water crossed the closed Gate. Later requests are in a later cutoff set or are authoritatively out of scope.
8. No unresolved I-owned revocation/authorization conflict, missing owner evidence, digest mismatch, unknown scope or restore rollback remains.

The I Release receipt binds exact RecoveryEpoch, COC prefix/batch/manifest digests, I Gate ref/generation, request high-water/root, PermissionEpoch, sequencer position, reconciliation root and signer/key version.

### 5.1 What I Release does not mean

I Gate Release clears only I's outage/pending Gate. It does not:
- issue a new CommitAuthorizationReceipt;
- decide a particular revocation won unless I's sequencer terminal record says so;
- advance PermissionEpoch except through the normal I policy transaction;
- release D's Forget Gate/barrier;
- resolve Storage prepared XIDs or make VisibilityPointer visible;
- release C provider side-effect admission;
- mark COC recovery complete or G Applied.

## 6. I terminal-decision atomicity versus outage-Gate release

The I final JF-10 decision is a distinct atomic transaction from outage Gate release. It MUST bind and atomically consume the single-use receipt against the exact tuple:
`PolicyDomainRef + PermissionEpoch + CommitAuthorizationReceiptRef/Digest + PreparedParticipantRef + PreparedTransactionGID + DatabaseIncarnationRef + PrepareAttemptRef/Generation + ParticipantLedgerRef/Version + PublicationOperationId + RequestDigest + owner_boundary + COC prepare-intent ref/digest`.

The I terminal decision and receipt consumption are one I sequencer transaction. A detached COMMIT token, receipt copy, common TransactionRef or COC index cannot authorize another participant. The decision's idempotency key is immutable; same key/digest returns the original terminal record, changed digest conflicts.

## 7. Reopen, invalidation and fail-closed rules

- Gate generation and request high-water are strictly monotonic and anchored outside rollback-prone snapshots.
- Restore always starts CLOSED until current I ledger and sequencer position are reconciled.
- Newly discovered pre-close I work reopens the reconciliation barrier and invalidates the affected I snapshot/release proof; it does not roll back the generation.
- New unrelated inventory membership invalidates only the affected PolicyDomain/scope snapshot; do not globally invalidate unrelated domains without dependency.
- Any stale key status, epoch fork, missing evidence, contradictory receipt consumption or incomplete ledger enumeration => UNKNOWN and Gate remains closed.
- Only I can issue a new release receipt for its Gate.

## 8. Required evidence and status

Required conformance cases (not run): concurrent close/admission CAS; lost close ACK; request racing high-water; unregistered receipt issuance; receipt-consumption ACK loss; duplicate/replayed receipt; restored ledger rollback; exact PreparedParticipant tuple mismatch; release with one unresolved in-flight item; stale generation replay.

**Disposition:** proposed I semantic amendment. It is not an independent I Owner approval, cryptographic profile freeze, implementation PASS, production deployment or authorization to reopen the Gate.
