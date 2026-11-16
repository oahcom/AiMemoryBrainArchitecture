# Phase 3.6 — Causal Order Coordinator Deployment & Durable Recovery Architecture

**Status:** A integration architecture proposal; C/I/D/H/Storage exact-version acceptance PENDING.  
**Profile:** `CausalOrderProfile/1.0`  
**Applies to:** successor `CGH-APPLIED-1.1` / H `bmcp.applied-ack/1.1.0`  
**Decision boundary:** this document does not claim implementation, deployment, production approval or conformance.

## 1. Architecture decision

Adopt one logical **Causal Order Coordinator (COC)** backed by one strongly consistent, quorum-committed append-only consensus log for the initial 1.0 profile.

- **Storage/Consistency is the proposed infrastructure custodian** of the durable log service, replication, snapshots, restore fencing and operational SLO. This is a proposal requiring explicit Storage Owner acceptance; no Storage authority is presumed.
- **C** owns immutable final-request intent and actual provider submit outcome.
- **I** owns CommitAuthorizationReceipt issuance/consumption, authorization terminality and PermissionEpoch changes.
- **D** owns ForgetFence requests, lineage coverage, participant clearance and ForgetFenceGeneration/effective transition.
- **H** owns versioned transport/integrity encoding and preserves owner-issued references.
- **G** alone decides Applied and current-use.
- **A** integrates acceptance evidence but owns none of these runtime decisions.

The coordinator is a neutral ordering and participant-accounting service. It MUST NOT mint, advance, infer or override I PermissionEpoch, D ForgetFenceGeneration, C submit success, H authentication, or G Applied state.

## 2. Deployment topology and consistency model

### 2.1 Initial topology

Deploy a single logical COC service backed by a three-voter consensus group across three independent failure domains, with a quorum of two. Each committed log entry is persisted to durable media by the voting quorum before the service returns a committed position. A node-local write, leader memory, async replica, event-bus acknowledgement or HTTP 200 is not a commit.

- Consensus protocol: Raft or an equivalently proven crash-fault-tolerant replicated state machine; no multi-leader or last-write-wins mode.
- Every committed entry has immutable `CoordinatorEpoch` (consensus term), `CoordinatorIndex` (log index), `EntryDigest`, `PreviousEntryDigest`, and `CausalOrderDomainRef`.
- The service exposes a linearizable append/read API. Stale follower reads cannot authorize a submit, release a barrier or declare a fence/revocation complete.
- A committed position is returned only after quorum durable commit. A leader lease or wall clock is not a substitute for quorum commit.
- Initial profile uses one logical ordered log for all protected C/I/D causal events in the deployment trust boundary. Partitioning/sharding is deferred until a formally proven cross-partition atomic ordering protocol exists.

The three-voter topology is the target deployment profile, not a claim that the repository already has a cloud, region, availability-zone or operator configured. Storage must confirm the actual failure-domain placement, durability class, encryption, backups and SLO before activation.

### 2.2 Causal-order domain

Every protected submit is assigned one immutable `CausalOrderDomainRef` representing the smallest authority boundary in which the applicable C final-request operation, I policy decision and D forget lineage overlap.

The authoritative registry must resolve the operation, PolicyDomainRef, target, source/ancestor lineage and C final boundary to the same domain before admission. A caller cannot choose or weaken the domain.

- Missing, ambiguous, stale or conflicting mapping => DENY/UNKNOWN; no submit.
- The initial single-log profile can order multiple domains, but each participant and owner request remains explicitly bound to its domain.
- A protected operation spanning multiple independently governed policy domains is rejected/UNKNOWN until I's multi-domain atomic authorization profile is approved.
- A D fence covering multiple causal domains must atomically register its request cutoff in every affected domain; if the coordinator cannot guarantee one atomic cutoff transaction across all affected domains, D must keep the fence pending and the affected data suppressed. No partial success is allowed.

## 3. Durable record model

The log is append-only. The minimum record families are:

1. `DOMAIN_BINDING_VERIFIED`: registry version, domain ref, policy/target/lineage mapping digest.
2. `PARTICIPANT_INTENT_ACCEPTED`: transaction, ParticipantIntentRef, C request digest, final boundary, identity/session, context/delivery, capability and idempotency identity.
3. `I_REVOCATION_REQUEST_RECORDED`: IRevocationRequestRef, PolicyDomainRef, affected action/resource/scope and request cutoff.
4. `D_FENCE_REQUEST_RECORDED`: DForgetFenceRequestRef, ForgetOperationRef, target/source/ancestor selector and request cutoff.
5. `I_AUTHORIZATION_TERMINAL_RECORDED`: I-signed CommitAuthorizationReceiptRef + IAuthorizationTerminalRef, I sequencer position, intent and exact digest.
6. `D_PARTICIPANT_CLEARANCE_RECORDED`: D-signed fence/lineage/clearance refs, request cutoff and effective position or explicit pending state.
7. `PARTICIPANT_RESERVATION_FINALIZED`: immutable binding of exact I/D proofs to intent and provider idempotency key.
8. `C_SUBMIT_OUTCOME_RECORDED`: C-signed actual provider boundary outcome, provider receipt, exact InferenceRequestId and digest.
9. `PARTICIPANT_TERMINALIZED`: terminal proof ref, terminal result and complete evidence digest.
10. `RECOVERY_RECONCILIATION_RECORDED`: same transaction's authoritative recovery evidence; never a synthetic success.
11. `CHECKPOINT_COMMITTED`: quorum-certified log index, term, root digest, snapshot digest and prior checkpoint reference.

All records are immutable and idempotent by stable operation key plus canonical payload digest. Same key + same digest returns the original position. Same key + different digest is CONFLICT, quarantined and security-audited.

## 4. API and state machine

### 4.1 Required linearizable operations

- `ResolveDomain(binding)`: return authoritative domain mapping and registry version; no mapping means fail closed.
- `RecordIntent(intent)`: atomically compare the domain's current admission cutoffs and append intent.
- `RecordIRevocationRequest(iRequest)`: append cutoff before I reports the request durably registered; blocks new affected intents/receipts.
- `RecordDFenceRequest(dRequest)`: append cutoff before D reports the request durably registered; blocks new affected intents.
- `RecordIAuthorizationTerminal(intent, iProof)`: validate I signature, exact intent/digest and one-time receipt identity; append owner proof, not reinterpret it.
- `RecordDParticipantClearance(intent, dProof)`: validate D signature, exact intent/lineage/digest and request/effective positions.
- `FinalizeReservation(intent, iProof, dProof)`: append only if both owner proofs are compatible and no earlier cutoff wins.
- `RecordCSubmitOutcome(reservation, cProof)`: append only C-signed actual boundary evidence bound to exact reservation.
- `Terminalize(transaction, proofSet)`: append terminal proof only when required owner evidence and C outcome are durable and consistent.
- `ReadLinearizable(transaction/domain)`: return quorum-confirmed state and log position.
- `Reconcile(transaction, evidence)`: append recovery facts to the same transaction; never replace its identity.

### 4.2 Participant states

`UNSEEN → INTENT_ACCEPTED → OWNER_TERMINALS_PENDING → RESERVED → SUBMIT_IN_PROGRESS → {SUBMIT_COMMIT_WON | SAFE_ABORT_WON | IN_DOUBT | CONFLICT}`

- `SAFE_ABORT_WON` is permitted only with authoritative proof that the provider side effect did not occur or an idempotent provider lookup proves the same request terminally absent.
- `IN_DOUBT` is durable and non-expiring. It blocks relevant I/D completion and cannot be cleared by TTL, lease expiry, queue deletion, operator force-delete or process restart.
- `CONFLICT` is quarantined; only a governed reconciliation procedure may append a superseding resolution, preserving all prior evidence.
- No retry may create a new transaction after ambiguous provider outcome. Recovery must reuse the same transaction, reservation and provider idempotency key.

## 5. Exact causal rules

### 5.1 D fence cutoff

A D fence request must first be quorum-committed as `D_FENCE_REQUEST_RECORDED`. Any affected intent ordered after that cutoff is rejected `FENCE_WON`, even if fence effectiveness is waiting for earlier participants to drain.

An intent before the cutoff remains a D barrier participant. D cannot commit the effective ForgetFenceGeneration until each earlier participant has a proven C outcome or safe abort and the required lineage coverage is complete. D terminal evidence carries both request cutoff and effective transition position.

### 5.2 I revocation cutoff

An I revocation request must first be quorum-committed as `I_REVOCATION_REQUEST_RECORDED`, blocking new affected receipts/admissions. I still decides the actual PermissionEpoch advance in its own sequencer.

If revocation wins before receipt consumption, C aborts. If I has already terminalized the exact receipt as COMMIT_WON, the revocation remains pending and I cannot claim effective epoch advancement past that unresolved participant until its exact C outcome or safe abort is terminal. If I's sequencer and COC cannot establish compatible order, outcome is UNKNOWN and no submit is admitted.

### 5.3 Submit terminal

C's provider call is forbidden before finalized reservation. C's outcome is accepted only from actual provider/runtime boundary evidence, not local buffering, middleware rendering or transport ACK. Terminal proof binds the intent, reservation, I receipt and terminal order, D fence request and lineage clearance, C provider receipt/outcome, all coordinator positions and canonical digests.

## 6. Crash, failover and restore

- Leader crash before quorum commit: entry is uncommitted and invisible; retry is idempotent.
- Leader crash after quorum commit but before response: linearizable read returns the committed entry; retry returns the same position.
- Minority partition: no writes and no favorable reads; C cannot submit; I/D cannot claim request or terminal completion absent quorum confirmation.
- Leader election: new leader must contain the committed quorum prefix. No old leader can commit or serve protected writes.
- Node replacement: join from authenticated snapshot plus log catch-up; it cannot become voter until its committed index and digest match the quorum.
- Snapshot: only from a committed index, includes all unresolved participants, all request cutoffs and all terminal evidence; snapshot root is tied to a quorum-certified checkpoint.
- Restore after total-cluster loss: restore only from the newest independently retained quorum-certified checkpoint plus complete subsequent log. If checkpoint freshness/completeness cannot be proven, enter `RESTORE_FENCED`: no new intents, no reservation finalization, no barrier release and no Full Applied until C/I/D/Storage reconcile all outstanding transactions and owner high-water marks.
- Rollback protection: a restored cluster must prove its term/index/root is not behind the latest externally retained checkpoint. Never silently reset term/index or reuse a prior coordinator epoch.
- Retention/compaction: terminal records may be compacted only after the evidence bundle and checkpoint are durably archived under approved retention; unresolved/IN_DOUBT participant records are never compacted away.

## 7. Security and operational controls

- Mutual workload authentication and per-owner signing keys; COC validates issuer, signature, audience, profile version, key status and exact payload digest. It does not mint owner signatures.
- Separate operator/admin roles for node management, snapshot/restore, key rotation and emergency recovery. No single operator can force-clear an unresolved participant.
- Append-only audit of admin operations; two-person approval for restore, checkpoint rollback exception, key compromise response and manual conflict reconciliation.
- Encryption in transit and at rest; key custody, HSM/KMS selection, rotation and compromise recovery require I/Security approval.
- Metrics: quorum health, commit latency, leader term/index, oldest unresolved participant, pending fence/revocation age, restore-fenced duration, conflicting idempotency keys and checkpoint lag.
- SLOs, RPO/RTO, retention duration, data residency and backup media are Storage/operator decisions and remain OPEN until signed acceptance.

## 8. Explicitly unsupported in v1

- Cross-policy-domain atomic authorization.
- Cross-log or multi-shard distributed transactions.
- Offline authorization leases or cached ALLOW.
- Automatic expiry/garbage collection of unresolved participants.
- Heuristic commit/abort after ambiguous provider outcome.
- Manual override that clears I/D barriers without owner-issued terminal evidence.
- Treating H ACK, event bus order, wall-clock time or a stale follower read as causal proof.

Unsupported cases fail closed as DENY/UNKNOWN/IN_DOUBT.

## 9. Required executable proof

Before production activation, implement and run:
- COC-01 quorum append linearizability under concurrent intent/revocation/fence requests.
- COC-02 leader crash before/after quorum commit and lost response idempotency.
- COC-03 minority partition blocks writes and all favorable decisions.
- COC-04 stale follower reads cannot finalize reservation.
- COC-05 D cutoff rejects later intents while earlier participants drain.
- COC-06 I cutoff blocks new receipts; pre/post-consumption revocation races.
- COC-07 provider success/definitive failure/unknown outcome and same-key recovery.
- COC-08 restart/restore with unresolved participants; no TTL release.
- COC-09 stale snapshot/rollback/term reuse detection and RESTORE_FENCED.
- COC-10 duplicate same-digest and conflicting different-digest idempotency.
- COC-11 multi-lineage D fence cutoff and partial registration failure.
- COC-12 key compromise, owner signature invalidity and conflicting terminal proofs.

Each test must attach exact build, schema/profile, topology, fault-injection script, raw logs, quorum positions, owner signatures and reproducible result. This document specifies tests; it does not claim they have run.

## 10. Acceptance and deployment gates

Required explicit approvals:
1. Storage/Consistency Owner accepts or revises the replicated-log, snapshot, restore, retention and operational model and names the accountable service operator.
2. C accepts intent/submit API, provider idempotency and recovery contract.
3. I accepts receipt consumption/revocation cutoff integration and signer trust.
4. D accepts fence cutoff, participant barrier and lineage integration.
5. H accepts exact 1.1.0 wire mapping and critical-field handling.
6. G accepts terminal proof inputs and historical Applied/current-use separation.
7. Security/Governance approves workload identities, keys, custody, admin and recovery controls.
8. Production conformance passes COC-01..12 plus C/I/D/H/G consumer suites.

Until then: **DESIGN PROPOSED / DEPLOYMENT NOT DESIGNATED / OWNER ACCEPTANCE PENDING / TESTS NOT RUN / PRODUCTION CAUSAL PROOF NOT VERIFIED**.
