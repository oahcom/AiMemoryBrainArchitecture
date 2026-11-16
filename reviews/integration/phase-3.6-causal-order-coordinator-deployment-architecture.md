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

A D fence request must first be quorum-committed as `D_FENCE_REQUEST_RECORDED`. Any affected intent ordered after that cutoff is rejected `FENCE_WON`, even if fence effectiveness is waiting for earlier participants to drain. If D has received a fence request but COC cannot durably record it, D must locally close admission for the affected target/lineage and report PENDING/UNKNOWN; it cannot accept new affected intents or claim the request is safely registered. Once connectivity returns, the request cutoff is committed before admission reopens.

An intent before the cutoff remains a D barrier participant. D cannot commit the effective ForgetFenceGeneration until each earlier participant has a proven C outcome or safe abort and the required lineage coverage is complete. D terminal evidence carries both request cutoff and effective transition position.

### 5.2 I revocation cutoff

An I revocation request must first be quorum-committed as `I_REVOCATION_REQUEST_RECORDED`, blocking new affected receipts/admissions. I still decides the actual PermissionEpoch advance in its own sequencer. If I has received a revocation request but COC cannot durably record it, I must locally suspend issuance/consumption of affected receipts and return UNKNOWN; it cannot allow new protected authorization to pass while the cutoff is unrecorded. Once connectivity returns, the revocation request is committed before affected admission can reopen. This prevents coordinator unavailability from creating a race window in which an owner-known request is invisible to the common log.

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


## 11. COC-outage owner-local cutoff and recovery reconciliation

This section is normative for every deployment claiming `CausalOrderProfile/1.0`. It closes the interval in which an owner has received a fence/revocation request but the common COC cannot accept a quorum-committed cutoff.

### 11.1 Durable local pending gate

- If D receives an applicable ForgetFence request while COC cannot confirm a quorum commit, D MUST first durably persist an owner-local `PENDING_COC_CUTOFF` record and close admission for the affected target/source/ancestor lineage. D reports PENDING/UNKNOWN, not an effective ForgetFenceGeneration or completed fence.
- If I receives an applicable revocation request while COC cannot confirm a quorum commit, I MUST first durably persist an owner-local `PENDING_COC_CUTOFF` record and suspend affected receipt issuance and receipt consumption. I reports UNKNOWN/PENDING, not a committed PermissionEpoch advance.
- The local gate survives process restart, failover and owner-service recovery. A request is not acknowledged as durably pending until its local gate is durable.
- Neither owner may reopen affected admission/receipt processing until the pending request cutoff has been recorded in the quorum-committed COC log and the recovery reconciliation below is complete.
- Owner-local sequence/time is audit metadata only. It does not establish order against the other owner or against COC positions.

### 11.2 Recovery batch and pre-existing participant reconciliation

When COC quorum service returns:

1. Keep all owner-local pending gates closed. No new affected ParticipantIntentRef, I receipt issuance/consumption, reservation or provider submit may proceed.
2. Read the latest quorum-confirmed log prefix and verify term, index and digest continuity. A stale/uncertain prefix enters `RESTORE_FENCED`.
3. Collect every durable I/D request that arrived during the outage into one immutable recovery-cutoff batch. Append that batch atomically after the last committed pre-outage log entry. Do not infer an order between independent I and D requests received during the same outage; preserve each owner request identity and bind both to the batch position.
4. Enumerate every affected ParticipantIntentRef already committed before the batch position. No such intent may be omitted from reconciliation merely because its I/D owner message was delayed or not yet delivered when the outage began.
5. For I: reconcile each pre-batch participant against the authoritative I sequencer. An unconsumed receipt may terminalize as REVOCATION_WON; an earlier COMMIT_WON remains pending behind that participant until its exact C outcome or safe abort is durable. No epoch advance may leap over unresolved participants.
6. For D: register every pre-batch affected intent in the exact target/source/ancestor barrier. D may clear only a proven safe abort or wait for the exact C outcome and compatible I terminal evidence. The effective fence cannot pass any unresolved pre-batch participant.
7. Verify all owner-local pending requests are represented by the committed batch, all pre-batch participants are accounted for, and owner high-water marks are monotonic. Only then may I/D clear their local pending gates; the shared cutoffs continue blocking all later affected intents/receipts.
8. Any missing intent, incomplete lineage, mismatched request digest, unavailable owner sequencer, or unprovable log prefix leaves the relevant local gate closed and the service in UNKNOWN/IN_DOUBT or RESTORE_FENCED.

The recovery batch is a coordinator ordering fact, not an I authorization decision or D fence decision. I still commits PermissionEpoch; D still commits ForgetFenceGeneration and lineage completion. A coordinator append cannot clear either owner barrier by itself.

### 11.3 Required outage conformance additions

- COC-13: D fence request received during COC outage; durable local gate survives restart; no affected intent admitted; recovery batch records cutoff; all earlier affected intents are reconciled before fence effectiveness.
- COC-14: I revocation request received during COC outage; local receipt issuance/consumption suspension survives restart; no receipt is consumed; recovery batch records cutoff; pre-existing COMMIT_WON participants remain pending and unconsumed receipts may resolve REVOCATION_WON.
- COC-15: simultaneous I and D requests during one outage are represented in one recovery batch without inventing an order between the owner-local request times.
- COC-16: COC restore with missing pre-outage log prefix or owner high-water mismatch enters RESTORE_FENCED; no local gate reopens.

These cases are SPECIFIED / NOT RUN. This section does not claim the owner-local gates, recovery batch or reconciliation are implemented.

## 12. JF-10 prepared participant bridge

This section incorporates I Owner's binding decision for the exact single-policy-domain bridge. It supplements the generic participant model above; it does not transfer I's policy decision authority to COC. The reviewed I decision is recorded in `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`, I branch `session-i-security-governance-2026-11-16`, Blob `1dedce596761807b25d337daf4a0d21bb797a197`. I's disposition is **ACCEPT WITH BINDING BRIDGE AMENDMENTS — SINGLE I POLICY DOMAIN ONLY**. This A document is amended to incorporate those requirements; this amendment is not a substitute for fresh Owner acceptance of this exact A Blob.

### 12.1 Authority boundary

The JF-10 bridge is a two-authority protocol, not two competing transaction coordinators:

- **COC** is the cross-owner causal-order log and durable participant-accounting/observation service. It orders cross-owner intents and request cutoffs, records participant lifecycle and recovery observations, and preserves causal references. It MUST NOT decide JF-10 Storage XID COMMIT/ABORT.
- **I policy-domain sequencer** is the sole durable decision coordinator for the prepared participant/XID. It alone consumes the single-use `CommitAuthorizationReceipt`, orders authorization against I revocation, and durably decides COMMIT/ABORT.
- **Storage** alone executes forward-commit or rollback of the exact XID and atomically publishes VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox in its local transaction.
- **D** alone owns ForgetFence, target/lineage registration, barrier and effective-fence semantics. A COC position never mints D clearance or ForgetFenceGeneration.
- **H** transports authenticated, versioned evidence without changing owner authority. **A** integrates evidence and does not decide runtime outcomes.

### 12.2 Immutable bridge identity and prepare registration

One immutable bridge tuple MUST bind, without lossy conversion:

- CausalOrderCoordinatorRef, CausalOrderDomainRef, COC epoch/index/entry digest;
- CausalOrderTransactionRef and ParticipantIntentRef;
- PublicationOperationId, canonical RequestDigest and exact owner_boundary;
- stable Storage participant identity, preallocated XID, participant digest and canonical authority DB identity;
- PolicyDomainRef, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef and delegation-chain digest;
- CommitAuthorizationReceiptRef, PermissionEpoch, I sequencer identity/epoch/position;
- applicable DForgetFenceRequestRef and D target/source/ancestor lineage and owner-predicate/clearance evidence;
- when required by effective I policy, authoritative ProducerDomainInventoryEpoch and InventorySealReceipt identity/digest.

Before Storage executes PREPARE, COC MUST quorum-commit `JF10_PREPARE_INTENT_REGISTERED` with stable operation identity, preallocated XID, participant digest, owner boundary, policy domain, ParticipantIntentRef and exact COC position. This makes the prospective participant visible to later I revocation and D fence cutoffs even if Storage crashes during PREPARE.

Storage then durably prepares that exact XID, retains private bytes and required target/lineage serialization locks, and returns an authenticated Storage-signed `PreparedParticipantReceipt` binding the same XID, participant digest, operation ID/digest, DB identity and prepare state. COC MUST quorum-commit `JF10_PREPARED_PARTICIPANT_REGISTERED` with that receipt before I may decide the owner-final gate. A lost response is recovered by authoritative lookup of the same preallocated XID; retries MUST NOT mint a new XID or operation identity.

If COC is unavailable after intent registration or Storage PREPARE, the participant remains private, durable and locked. No I owner-final-gate decision is admitted until the required COC prefix and prepared-participant evidence are linearly readable. Recovery resumes the same XID.

### 12.3 I owner-final-gate transaction

Before deciding, I MUST obtain a linearizable quorum-confirmed COC read of the exact intent, prepare registration and relevant I/D cutoff prefix; verify exact tuple equality; validate the current I authorization tuple, PermissionEpoch and single-use receipt; and validate any policy-required inventory seal against I's authoritative registry/sequencer path.

I MUST persist receipt consumption, participant/XID binding, operation identity/digest, owner boundary, COC position/digest, terminal decision identity and I sequencer position in one I coordinator transaction. Detached preflight receipt consumption followed by a separate participant transaction is forbidden. COC position, COC reservation, H ACK and Storage PREPARE receipt are not authorization decisions.

### 12.4 Terminal outcomes and same-XID recovery

The I sequencer is the sole source of I terminality:

- `COMMIT_WON`: I durably commits the exact prepared XID before conflicting revocation; Storage MUST forward-commit that same XID.
- `REVOCATION_WON`: I orders revocation first and durably ABORTs that exact XID; Storage MUST roll back it and prove non-publication.
- `INDETERMINATE_ABORTED`: I durably decides ABORT/non-success; Storage rolls back and MUST NOT reinterpret it as COMMIT.
- `UNKNOWN/IN_DOUBT`: not terminal. Retain prepared XID, private bytes and locks; block conflicting revocation progress and relevant D barrier completion. Timeout, missing COC row, stale replica, process death or lost ACK never determines outcome.

After a durable I decision, recovery direction is irrevocable: COMMIT means forward-commit the same XID; ABORT means rollback the same XID. No heuristic outcome, alternate XID or reversal is permitted. If I COMMIT is durable while COC is unavailable, Storage still forward-commits/re recovers that exact XID; COC later records the signed I decision and Storage receipt/proof idempotently. If Storage cannot recover it, remain blocked and escalate; do not rewrite I's decision.

### 12.5 Typed-order and cutoff rules

COC positions and I sequencer positions are distinct typed orders. They MUST NOT be numerically or lexically compared, merged into a synthetic total order, or substituted for one another. The immutable signed bridge tuple carries both positions and digests.

- D fence cutoff before `JF10_PREPARE_INTENT_REGISTERED`: reject prepare; no Storage XID may be prepared.
- Prepare intent before D fence cutoff: D MUST include the prospective/prepared participant in its target/source/ancestor barrier. D cannot make the fence effective or close the barrier until I's exact decision, Storage's exact participant resolution and all D lineage obligations are proven.
- I revocation cutoff before prepare intent: reject affected prepare and receipt consumption.
- Prepare intent before revocation cutoff but no I terminal decision: I may order revocation first and durably ABORT.
- I COMMIT_WON before a later revocation: revocation remains pending behind that exact participant until Storage resolution and required D barrier accounting are durable.
- If I or D receives a request during COC outage, its owner-local pending gate remains durable and closed. No later affected admission, receipt processing, claimed cutoff order or effective completion is allowed until COC records the cutoff and recovery reconciles earlier participants.

### 12.6 Required COC bridge records and read APIs

The COC schema/API MUST add or explicitly version-map these records:

1. `JF10_PREPARE_INTENT_REGISTERED` — stable operation/XID identity, ParticipantIntentRef, digest, boundary, policy domain and pre-prepare COC position.
2. `JF10_PREPARED_PARTICIPANT_REGISTERED` — Storage-signed PreparedParticipantReceipt and exact XID/digest/DB identity.
3. `I_JF10_TERMINAL_DECISION_OBSERVED` — I-signed receipt-consumption proof, IAuthorizationTerminalRef, decision ID, I sequencer position and exact COC/XID/operation tuple.
4. `STORAGE_JF10_PARTICIPANT_RESOLVED` — same-XID commit or rollback proof; commit includes exact PublicationReceipt and visibility transaction identity; abort includes authoritative non-publication proof.
5. `JF10_BRIDGE_RECONCILIATION_RECORDED` — idempotent recovery observations linking COC prefix, I authoritative decision lookup, Storage XID state and D barrier state without synthesizing owner decisions.

COC reads MUST return the quorum-confirmed prefix and all unresolved JF-10 participant registrations for the domain. I reads MUST return authoritative linearizable sequencer decision and receipt-consumption state. Storage reads MUST return authoritative same-XID prepared/committed/rolled-back state and PublicationReceipt. Stale replicas and caches are never decision sources.

### 12.7 Scope, failure handling and conformance

This bridge applies only to one I PolicyDomainRef. Multi-policy-domain atomicity remains **BLOCKED / NOT ACCEPTED**; reject or pause such operations as BLOCKED/UNKNOWN. Partial commit, independent per-domain COMMIT_WON aggregation and best-effort completion are forbidden.

Fail closed on missing/unverifiable COC prefix; unregistered or mismatched XID; changed operation digest/boundary/security tuple; duplicate receipt consumption; stale PermissionEpoch or required inventory seal; winning D fence cutoff; unknown lineage; invalid owner signature; COC rollback/term reuse; ambiguous participant state; or inability to prove same-XID recovery.

The following cases are added to COC-01..12 and are **SPECIFIED / NOT RUN**:

- JF10-COC-01: crash after prepare-intent registration before Storage PREPARE; retry preserves operation/XID identity.
- JF10-COC-02: crash after Storage PREPARE before COC prepared-receipt append; authoritative same-XID lookup repairs registration without a second XID.
- JF10-COC-03: D cutoff races prepare-intent registration; one COC order and correct D barrier membership.
- JF10-COC-04: I revocation cutoff races prepare-intent and owner-final-gate; one I terminal decision and no detached preflight.
- JF10-COC-05: durable I COMMIT during COC outage; Storage forward-commits same XID and later COC observation is idempotent.
- JF10-COC-06: durable I ABORT during COC outage; Storage rolls back same XID and later observation cannot change the decision.
- JF10-COC-07: distinct COC/I typed positions, leader terms and lost ACKs; no synthetic order comparison.
- JF10-COC-08: IN_DOUBT survives I/COC/Storage restart, replica lag and restore; no TTL, heuristic resolution or barrier release.
- JF10-COC-09: durable Storage PublicationReceipt with lost COC ACK; authoritative readback records the same receipt without duplicate visibility.
- JF10-COC-10: required InventorySeal invalidation around I owner-final-gate; I validates and binds the authoritative seal snapshot.

Evidence must include COC quorum positions/digests, I sequencer decision and receipt-consumption proof, Storage XID transaction traces, D fence/barrier traces, exact build/schema/DB/runtime identities, deterministic fault-injection results and independent review. These tests are not asserted to have run.

### 12.8 Reconciliation and acceptance status

This amendment reconciles A's COC proposal with I's binding JF-10 bridge requirements at the architecture-text level only. Fresh exact-Blob acceptance remains required from I and the relevant C/D/H/Storage Owners; D and Storage must explicitly accept their barrier and same-XID responsibilities, and H must approve any required wire-schema mapping. The amendment does not designate a Storage operator, select/deploy a concrete database, prove implementation, pass conformance, approve governance, close InventorySeal/Global Forget, or approve production activation.

**Status:** JF-10 bridge architecture amended; Owner re-acceptance PENDING; implementation NOT VERIFIED; COC-01..12 and JF10-COC-01..10 NOT RUN; multi-policy-domain atomicity BLOCKED; JF-10 P0 OPEN.
