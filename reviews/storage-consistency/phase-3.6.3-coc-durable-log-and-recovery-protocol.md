# Phase 3.6.3 — COC Durable Log, Participant Registry & Recovery Protocol

- Owner: Storage/Consistency, in coordination with A, I, D, C, E and H
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- Status: **ARCHITECTURE PROTOCOL SPECIFICATION — PROPOSED FOR EXACT OWNER REVIEW; NOT IMPLEMENTED**
- Applies to: `CausalOrderProfile/1.0`, single logical COC log, one-I-PolicyDomain JF-10 bridge
- Companion A COC architecture: Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Common JF-10 v2 protocol: Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- Storage JF-10 realization evidence: Blob `107d21bd2c604ee0b04feff2ee5580e1de9c7fce`
- Date: 2026-11-17

## 1. Decision boundary and system separation

This specification completes the architecture-phase COC durable protocol design requested by the Storage boundary review. It defines a deterministic, quorum-committed ordering and participant-accounting protocol. It does not select a production consensus library, deploy a quorum, implement a COC service, or authorize production activation.

Three durable authorities remain distinct:

1. **COC consensus log:** establishes the total order of COC events, participant intent registration, owner-request cutoffs, recovery batches and observation records. It never decides owner policy or Storage visibility.
2. **I policy-domain sequencer:** alone decides single-use CommitAuthorizationReceipt consumption, authorization/revocation order, PermissionEpoch and the terminal COMMIT_WON / REVOCATION_WON / INDETERMINATE_ABORTED outcome.
3. **Canonical Authority Storage transaction:** alone resolves the exact prepared XID and atomically commits or rolls back VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox. D's ForgetFence/lineage barrier remains an independent authority that must participate in the same final visibility ordering.

COC, I and Storage log positions are typed and incomparable. A shared transaction ID, copied receipt, matching wall-clock timestamp or same physical server does not merge these authorities into one transaction manager. COC is not an XA coordinator for I or Storage.

## 2. Normative topology and consensus profile

### 2.1 Logical topology

- One logical COC cluster with three voting members in three independent failure domains; two durable votes form quorum.
- One active Raft leader per term. Multi-leader, last-write-wins, async acknowledgement, node-local success and split-brain write modes are forbidden.
- One initial ordered log for all protected C/I/D causal events in the deployment trust boundary. Sharding, independent per-domain logs and cross-shard transactions are unsupported in v1.
- COC service custody belongs logically to Storage/Consistency. A and the owner services consume the API; they do not operate an alternate log.
- The actual consensus implementation/library, host placement, regions/zones, durable media, network security, operator identities and deployment manifest are engineering/deployment selections, not inferred here.

### 2.2 Raft state and durable commit

Use the Raft consensus safety model (or a formally reviewed equivalent crash-fault-tolerant replicated state machine) with these normative requirements:

- Every entry carries `cluster_id`, `CausalOrderDomainRef`, `CoordinatorEpoch` (Raft term), `CoordinatorIndex`, `VoterConfigurationEpoch`, `EntryType`, `SchemaVersion`, stable `OperationId`, canonical payload digest, previous-entry digest, entry digest and authenticated issuer reference.
- The leader may append locally as uncommitted, but it MUST NOT return a committed receipt until the entry is persisted and acknowledged by a quorum and the Raft commit index covers that entry.
- A follower acknowledgement counts only after its configured durable-write boundary. Volatile memory, page cache without required flush, queue acknowledgement or a client timeout is not a durable vote.
- A client timeout after a possible quorum commit returns `UNKNOWN`; the caller must perform an authenticated linearizable lookup using the same stable OperationId and digest. Retrying with a new OperationId is forbidden.
- A leader may serve protected writes only while it holds a valid current term and can establish quorum. Old leaders are fenced by term/configuration checks and MUST reject protected writes after losing leadership.
- A linearizable read uses a quorum-confirmed ReadIndex/barrier or an equivalent proof that the responding leader is current. Follower reads and cached results are never decision sources.
- A quorum loss makes protected append, reservation, owner-gate reopening and favorable reads unavailable. Fail closed; do not use a lease or local clock to continue.

### 2.3 Voter membership changes

- Membership is versioned by `VoterConfigurationEpoch` and represented by an immutable configuration record in the log.
- Add/remove/replace voter uses joint-consensus transition with an overlapping safe quorum. The new configuration is not effective until the joint transition is committed.
- A voter is not promoted from learner to voter until it has authenticated snapshot/log catch-up and matches the quorum-committed index and digest.
- Configuration rollback, term reuse, index reuse, two-voter emergency mode or operator force-promotion without quorum proof is prohibited.
- If quorum membership cannot be proven after restore, cluster state is `RESTORE_FENCED`.

## 3. Canonical log and record model

### 3.1 Common immutable envelope

Every log record contains:

- `CoordinatorClusterRef`, `CausalOrderDomainRef`, `CoordinatorEpoch`, `CoordinatorIndex`, `VoterConfigurationEpoch`;
- `RecordType`, `RecordSchemaVersion`, stable `OperationId`, `ParticipantIntentRef` where applicable, `OwnerAuthorityRef`, `OwnerOperationRef`;
- `CanonicalizationProfileId`, `DigestAlgorithm=SHA-256`, `PayloadDigest`, `PreviousEntryDigest`, `EntryDigest`;
- authenticated `IssuerRef`, signer/key version reference, audience and integrity-proof reference;
- `ObservedAt` as audit metadata only (never a causal ordering input).

Entry digest is computed over the canonical envelope excluding the digest field itself and includes the prior committed entry digest. A gap, fork, changed payload under the same operation identity or mismatched predecessor digest is a hard integrity conflict; it is never repaired by selecting the latest timestamp.

### 3.2 Required record families

| Record | Required binding | Effect (and non-effect) |
|---|---|---|
| `DOMAIN_BINDING_VERIFIED` | Registry version, CausalOrderDomainRef, PolicyDomainRef, target/source/ancestor lineage digest | Freezes the resolved domain binding for the operation; does not authorize. |
| `PARTICIPANT_INTENT_ACCEPTED` | TransactionRef, ParticipantIntentRef, PublicationOperationId, request digest, owner boundary, authenticated C/producer identity, provider/producer idempotency key | Registers a prospective participant before external side effect; does not authorize submit. |
| `I_REVOCATION_REQUEST_RECORDED` | IRevocationRequestRef, PolicyDomainRef, affected action/resource/scope, immutable request digest | Establishes COC cutoff position; I alone advances PermissionEpoch/decides terminality. |
| `D_FENCE_REQUEST_RECORDED` | DForgetFenceRequestRef, ForgetOperationRef, complete target/source/ancestor selector digest | Establishes COC cutoff position; D alone advances ForgetFenceGeneration/effective fence. |
| `JF10_PREPARE_INTENT_REGISTERED` | Stable operation tuple, preallocated Storage participant/XID, DB authority ref, D barrier refs, I PolicyDomainRef | Makes the prospective prepared participant visible to cutoffs before Storage PREPARE. |
| `JF10_PREPARED_PARTICIPANT_REGISTERED` | Storage-signed PreparedParticipantReceipt, exact same XID/digest/DB/operation | Records durable prepared participant observation; not I COMMIT or visibility. |
| `I_AUTHORIZATION_TERMINAL_RECORDED` | I-signed CommitAuthorizationReceipt/terminal ref, I sequencer position, exact tuple and receipt-consumption proof | Observes I's terminal decision; COC does not decide or reinterpret it. |
| `D_PARTICIPANT_CLEARANCE_RECORDED` | D-signed lineage/clearance evidence, request cutoff and effective position | Observes D's barrier/clearance; COC does not mint D clearance. |
| `PARTICIPANT_RESERVATION_FINALIZED` | Exact intent + compatible I/D proofs + provider idempotency key | Reserves the exact operation before side effect; does not prove provider success. |
| `C_SUBMIT_OUTCOME_RECORDED` | C-signed actual provider outcome, final request digest, provider receipt and InferenceRequestId | Records observed C outcome; no synthetic success from ACK/intent. |
| `STORAGE_JF10_PARTICIPANT_RESOLVED` | Storage-signed same-XID COMMITTED/ROLLED_BACK proof, VisibilityPointer/PublicationReceipt or non-publication proof | Observes Storage result; does not itself create visibility. |
| `PARTICIPANT_TERMINALIZED` | Complete consistent evidence digest and terminal proof | Closes COC participant accounting only; owner states remain owned by their authorities. |
| `RECOVERY_CUTOFF_BATCH` | Pre-batch prefix, complete I/D request sets, owner completeness attestations, participant set digest, owner high-water marks | Establishes one recovery batch position; does not order I vs D local request times. |
| `CHECKPOINT_COMMITTED` | Term, index, configuration epoch, prefix root, snapshot digest and prior checkpoint ref | Anchors a recoverable committed prefix. |
| `RESTORE_RECONCILIATION_RECORDED` | Restored checkpoint, prefix proof, unresolved participant set and owner lookup evidence | Records reconciliation; cannot reopen gates until every required predicate is satisfied. |

### 3.3 Idempotency and immutable identity

- Primary append idempotency key is `(CausalOrderDomainRef, RecordType, OperationId)`; the exact tuple and payload digest are immutable.
- Same key + same canonical digest returns the original committed term/index/entry digest.
- Same key + different digest, participant, authority, policy domain, XID or owner boundary returns `CONFLICT`, retains the original record and creates a security audit event.
- An owner retry after lost ACK queries the original operation and does not mint a new participant, XID, reservation or provider key.
- Reconciliation appends new observations against the original transaction. It never edits or overwrites earlier records.

## 4. Participant registry and state machine

### 4.1 Registry identity

Each participant registry row is keyed by immutable `CausalOrderTransactionRef` and `ParticipantIntentRef`, and binds exactly one `PublicationOperationId`, request digest, owner boundary, `CausalOrderDomainRef`, one `PolicyDomainRef`, provider/producer idempotency key, and (for JF-10) one preallocated Storage participant/XID + canonical DB authority ref. All authority references remain opaque typed references.

### 4.2 States

`UNSEEN → INTENT_ACCEPTED → PREPARE_INTENT_REGISTERED → PREPARED_PARTICIPANT_REGISTERED → OWNER_TERMINALS_PENDING → RESERVED → SUBMIT_IN_PROGRESS → {SUBMIT_COMMIT_WON | SAFE_ABORT_WON | IN_DOUBT | CONFLICT}`

JF-10 participant substate is tracked separately: `NOT_PREPARED → PREPARE_INTENT_DURABLE → STORAGE_PREPARED → I_TERMINAL_KNOWN → STORAGE_RESOLVED → RECEIPT_VERIFIED`. COC does not infer one substate from another.

- `IN_DOUBT` is durable, non-expiring and blocks relevant I/D completion and new conflicting operation admission.
- `SAFE_ABORT_WON` requires authoritative proof that the external side effect did not occur and, for a provider with idempotency support, a same-key authoritative lookup.
- `CONFLICT` is quarantined. Only a governed owner-authorized reconciliation can append a superseding resolution; history remains immutable.
- No TTL, lease expiry, DLQ movement, queue deletion, worker death, coordinator restart or operator override terminalizes a participant.
- A terminal COC record means participant accounting is complete only after all owner outcomes are present and consistent. It is not a substitute for G Full Applied or I/D completion.

## 5. Normative API contract

All methods are authenticated, versioned, idempotent and linearizable where they read or append authoritative state. All responses include a request digest, authority identity and a signed/verified COC commit proof.

| API | Required behavior |
|---|---|
| `ResolveDomain(binding)` | Resolve authoritative policy/target/source/ancestor mapping and registry version; ambiguous or stale mapping fails closed. |
| `AppendIntent(intent)` | Atomically check current COC cutoffs and append the immutable intent; reject if an earlier affected I/D cutoff exists. |
| `RecordOwnerCutoff(ownerRequest)` | Append I or D cutoff before owner reports common-log registration; on COC outage owner-local pending gate remains closed. |
| `RegisterJF10PrepareIntent(tuple)` | Quorum-commit prospective participant + preallocated XID before Storage PREPARE. |
| `RegisterPreparedParticipant(receipt)` | Verify Storage signature and exact same XID/digest/DB/operation; append durable prepared receipt observation. |
| `RecordIAuthorizationTerminal(proof)` | Verify I signature and exact tuple; record observation only. |
| `RecordDParticipantClearance(proof)` | Verify D signature, exact lineage and cutoff/effective positions; record observation only. |
| `FinalizeReservation(tuple, proofs)` | Append only when I/D proofs are compatible and no earlier cutoff wins. |
| `RecordCSubmitOutcome(proof)` | Accept only C-signed actual provider boundary evidence bound to exact reservation. |
| `RecordStorageResolution(proof)` | Accept only Storage-signed authoritative same-XID commit/rollback proof. |
| `Terminalize(transaction, evidenceSet)` | Require complete consistent I/D/Storage/C evidence and canonical digest; no owner authority is synthesized. |
| `GetByOperationId(id,digest)` | Linearizable exact lookup; changed digest conflicts. |
| `ReadLinearizable(domain)` | Return quorum-confirmed committed prefix and term/index/configuration epoch. |
| `ListUnresolvedParticipants(domain, cutoff)` | Enumerate every participant in the committed prefix not proven terminal; include digest and owner references. |
| `GetCommittedPrefix(position)` | Return exact contiguous prefix with root digest and quorum proof; holes or mismatch fail. |
| `AppendRecoveryBatch(batch)` | Atomically append the complete outage request set and participant reconciliation cutoff. |
| `ReconcileParticipant(id,digest,ownerEvidence)` | Append new authoritative observations to same transaction; never replace identity. |
| `CreateCheckpoint()` / `RestoreCheckpoint(manifest)` | Create/verify committed-prefix checkpoint and external anti-rollback anchor; restore is fenced until all checks pass. |

## 6. COC outage and recovery-cutoff algorithm

### 6.1 During outage

- If D receives a Forget request while COC cannot establish quorum commit, D durably records `PENDING_COC_CUTOFF` and closes affected target/source/ancestor admission. This is not an effective ForgetFenceGeneration.
- If I receives a revocation request while COC cannot establish quorum commit, I durably records `PENDING_COC_CUTOFF` and suspends affected receipt issuance/consumption. This is not a PermissionEpoch advance.
- C rejects new protected intents/reservations/provider side effects while common order is unavailable. G does not promote new Full Applied. E keeps derivatives private.
- Owner-local request sequence/time is audit metadata only; it is not comparable across I and D.

### 6.2 Recovery batch

1. Keep every I/D local pending gate closed; disable new affected admission, receipt issuance/consumption, reservation and provider submit.
2. Establish the newest quorum-confirmed COC prefix. Verify cluster ID, term, index, voter configuration epoch, predecessor digest chain and external checkpoint anchor. Any missing/corrupt/stale prefix enters `RESTORE_FENCED`.
3. Collect all owner-durable I and D outage requests. Each owner supplies a completeness attestation and request-set digest for its own local sequence space.
4. Append one immutable `RECOVERY_CUTOFF_BATCH` at the next COC position. Include separate canonical I and D request arrays, both owner completeness attestations, the pre-batch prefix anchor, batch digest and owner high-water marks. Never infer I-vs-D order from local sequence or clock.
5. Enumerate every affected `ParticipantIntentRef` in the committed pre-batch prefix. Bind the exact participant-set digest and verify no omitted participant, including delayed owner-message delivery and pre-existing unresolved JF-10 XIDs.
6. Reconcile each pre-batch participant against authoritative I sequencer, D barrier/lineage ledger, Storage exact-XID lookup and C actual provider idempotency/outcome lookup. Preserve original IDs and digests.
7. For I, an unconsumed receipt may resolve REVOCATION_WON; an earlier COMMIT_WON remains pending until same participant C outcome and Storage terminal outcome are durable. For D, every pre-batch affected intent is inserted into the full lineage barrier; fence effectiveness waits for all participants to resolve.
8. Verify each owner's high-water covers every request and each owner has independently recorded its own gate disposition. COC never emits an I or D owner-gate release.
9. Only after all pre-batch participants and owner requests are accounted for may owners reopen their local pending gates. The committed batch cutoff continues to block all later affected operations.
10. Any missing prefix, owner request, participant, lineage, receipt, XID, signature, high-water or contradictory evidence keeps the relevant owner gate closed and the participant UNKNOWN/IN_DOUBT.

### 6.3 Recovery receipt

COC emits a signed `RecoveryReconciliationReceipt` binding: checkpoint/prefix term-index-root, recovery batch ref/digest/position, I request-set digest and high-water, D request-set digest and high-water, complete pre-batch participant-set digest, unresolved participant list, per-owner authoritative lookup refs, restored voter configuration epoch and reconciliation result. `RECONCILED_TERMINAL` is permitted only when all required participant states are terminal and owner high-water proofs match. Otherwise state is `PENDING`, `UNKNOWN` or `RESTORE_FENCED`.

## 7. Snapshot, WAL, PITR and restore protocol

### 7.1 Checkpoint manifest

Each checkpoint manifest binds cluster ID, coordinator term, committed index, voter configuration epoch, previous checkpoint ref, committed prefix root digest, snapshot digest, exact log segment list and checksums, unresolved participant set/digest, I/D owner high-water observations, creation signer and external monotonic anchor. Checkpoint is not valid merely because a file exists.

### 7.2 Restore

- Restore only from the newest independently retained quorum-certified checkpoint plus a complete, contiguous sequence of subsequent committed log records.
- Verify every segment checksum, previous-entry digest, term/index continuity, configuration transition and unresolved participant identity.
- Reject rollback below the latest external monotonic anchor. Never reset/reuse term, index or voter configuration epoch.
- Reconcile the restored COC prefix with authoritative I/D/Storage owner lookups before protected service resumes.
- If any prefix, archive, checkpoint, owner high-water or participant is missing, corrupt, incomplete, stale or contradictory, set `RESTORE_FENCED`; no new intent, receipt consumption, reservation, provider submit, barrier release or Full Applied.
- Restored canonical data remains quarantined until the current Forget/authorization control ledger has been replayed and verified. COC restore alone does not establish Global Forget completeness.

### 7.3 WAL archive and PITR requirements

For any PostgreSQL-backed owner participant/Canonical Authority store, WAL archiving must prove a contiguous prefix through the target LSN and preserve prepared-XID state. Missing, corrupt or incomplete required WAL is a hard restore failure. A restored prepared participant is resolved only by the same original XID after recovery; no replacement XID. The current I/D control state is replayed before any protected reads. These are owner-DB requirements, distinct from COC's own Raft log/checkpoint recovery.

## 8. Retention, compaction, audit and security

- Retain every unresolved/IN_DOUBT participant, owner cutoff, request digest and required lineage reference indefinitely until authoritative terminal resolution and approved evidence retention.
- A terminal record may be compacted only after a quorum-certified checkpoint includes it, the complete evidence bundle is archived with integrity proof, the retention period is approved, and no owner requires it for audit/recovery/Forget.
- Compaction preserves a non-reconstructive tombstone containing stable operation identity, digest, terminal outcome, evidence archive reference and checkpoint anchor. It must not retain forgotten plaintext or become an alternate memory store.
- Owner signatures and COC quorum proofs are distinct. COC validates signature/key status and exact binding but does not issue owner signatures.
- Mutual workload authentication; encryption in transit/at rest; key rotation; signer revocation; admin separation; append-only administrative audit; two-person restore/rollback approval; no single operator can clear IN_DOUBT.
- KMS/HSM, cipher suite, key custody, data residency and audit retention require I/Security/Governance approval. No cryptographic algorithm or key provider is frozen here.

## 9. Failure and recovery matrix

| Failure / race | Required durable result | Forbidden behavior |
|---|---|---|
| Leader crash before quorum commit | Entry uncommitted; no receipt | Treat local append as committed |
| Leader crash after quorum commit before ACK | Same operation lookup returns original position | Mint new OperationId/XID |
| Minority partition | No protected writes or favorable reads | Continue under lease/cache |
| Stale leader writes after term change | Reject by term/configuration fence | Accept old-term append |
| Voter membership change interrupted | Old/joint config remains authoritative; no unsafe promotion | Rewrite voter set locally |
| Same key + changed digest | Immutable conflict/quarantine | Overwrite prior participant |
| COC outage with D fence request | D local pending gate durable; affected lineage closed | Treat request as absent |
| COC outage with I revocation | I local pending gate durable; receipt issuance/consumption suspended | Reuse stale ALLOW/epoch |
| Recovery batch omits request/participant | RESTORE_FENCED; gates remain closed | Partial batch success |
| I and D local requests simultaneous | One batch with separate owner sets; no cross-owner clock order | Sort local sequence/time globally |
| Prepared XID after Storage crash | Same XID lookup/forward commit or rollback per I decision | Alternate XID or heuristic outcome |
| Storage commit ACK lost | Authoritative lookup resolves same XID and same PublicationReceipt | Duplicate visibility |
| Snapshot rollback or missing log segment | RESTORE_FENCED | Start from older checkpoint as healthy |
| Required WAL missing/corrupt/incomplete | PITR fails closed; no authoritative service | Best-effort recovery to guessed state |
| Stale replica or cache | Excluded from decisions; authoritative leader/DB lookup | Infer terminal outcome from lagging replica |
| Key compromised / signature invalid | Reject/quarantine affected evidence and rotate under policy | Accept unsigned owner outcome |
| Operator unavailable | Remain unavailable/blocked until authorized recovery | Single-person force clear |

## 10. Conformance plan and phase gates

### 10.1 Gate B architecture conformance cases

- COC-B-01: immutable log record schema, digest chain and duplicate same-digest idempotency.
- COC-B-02: same OperationId with changed digest/authority/participant/XID returns conflict.
- COC-B-03: Raft quorum durable commit and response-loss lookup.
- COC-B-04: linearizable ReadIndex rejects stale leader/follower decision reads.
- COC-B-05: minority partition blocks protected writes and favorable reads.
- COC-B-06: voter configuration epoch joint-consensus transition and stale-member rejection.
- COC-B-07: snapshot manifest binds term/index/configuration/root/unresolved participants.
- COC-B-08: stale checkpoint, rollback, missing prefix or mismatched root enters RESTORE_FENCED.
- COC-B-09: recovery batch includes complete I/D outage request sets and owner completeness attestations.
- COC-B-10: recovery batch enumerates every affected pre-batch participant and preserves owner high-water spaces.
- COC-B-11: unresolved JF-10 participant survives restart/restore and cannot be compacted or released.
- COC-B-12: terminal compaction preserves proof anchor and does not retain forgotten plaintext.

### 10.2 Existing reference-model evidence

The A branch in-memory COC outage recovery model passed 11 unit tests in GitHub Actions run `43897364938` (commit `386b03f4ae76cc175ab18c6013437a9c726de8a5`, job `133404449208`). The JF-10/COC semantic validator passed 18 unit tests in run `43905568915` (commit `b154913a8594d04c799a05c799bbe7242f0e8651`, job `133433336488`). These are logical-model and semantic-validator tests only; neither is a Raft/quorum implementation test.

### 10.3 Storage engine capability evidence

Seven PostgreSQL 18.7 CI workflows completed SUCCESS on Storage commit `2d476dd32ac020d329e8290ee2aaaa1f0c057c92`: prepared-XID, synchronous standby promotion, backup/restore, WAL archive PITR, prepared-XID PITR with missing/corrupt/incomplete WAL negatives, synchronous-standby-unavailable fail-closed, and old-primary pg_rewind/rejoin. Exact run IDs and job IDs are recorded in the Storage readiness addendum. These qualify the pinned engine/fixture capabilities only; they do not implement COC quorum or production I/D/Storage integration.

### 10.4 Phase boundaries

- Gate A: close the architecture design contract for Storage/JF-10 and identify future implementation/operations acceptance criteria. Production runtime binding is `DEFERRED_TO_ENGINEERING_PHASE` because the project is in architecture design.
- Gate B: this protocol is the proposed COC durable log/state machine/participant/recovery design. It requires exact A/I/D/C/E/H/Storage review and reconciliation of any remaining decision owners before Gate B can be called design-accepted.
- Gate C: distributed implementation fault injection, quorum/network partition, actual leader failover, owner-service integration, real snapshot/PITR and production-equivalent recovery are engineering-phase work after executable participants exist.

## 11. Operational objectives and accountable roles

- Logical service custodian: Storage/Consistency Owner.
- Protocol/architecture authority: A integrates; I owns policy sequencer and inventory; D owns ForgetFence/lineage; C owns provider outcome; E owns compiler producer lifecycle; H owns wire encoding/authenticated transport; G owns Applied/current-use; B owns domain types.
- Engineering phase must name a primary COC service operator and backup/on-call, consensus implementation owner, DB platform operator, Security/KMS owner and incident commander. No named individual is designated by this architecture document.
- Durability objective: **RPO 0 for every quorum-acknowledged COC commit** under the specified synchronous durable quorum. A commit not covered by quorum is not acknowledged.
- Availability objective: fail closed without quorum. No availability SLA is claimed.
- RTO: numeric target is intentionally **TBD by engineering/operations** after workload, deployment geography and service dependency SLOs are defined. Until recovery is complete, service remains RESTORE_FENCED/UNKNOWN; no time-based release.
- Backup/restore objective: restore to the latest verifiable checkpoint plus contiguous committed log; any uncertainty blocks protected service rather than accepting data loss.

## 12. Explicit non-claims and required exact review

This specification does not claim a running Raft cluster, selected consensus library, production quorum, COC operator, deployed KMS, actual RPO/RTO measurement, I sequencer integration, D barrier integration, C provider idempotency, E compiler integration, G Applied implementation, H SDK interoperability, global Forget completeness or production activation.

Required exact review: A (integrated protocol), I (owner policy/sequencer boundary), D (cutoff/lineage/barrier), C (provider side-effect lifecycle), E (producer lifecycle), H (wire/identity), G (Applied evidence), Storage (durability/restore/retention). Any change to this artifact after review requires exact-Blob re-acceptance from affected owners.
## 13. Protocol review clarifications — quorum proof and fault model

### 13.1 COC commit receipt

A client-visible committed append returns a COC-issued immutable `COCCommitReceipt` binding cluster ID, CausalOrderDomainRef, CoordinatorEpoch, CoordinatorIndex, VoterConfigurationEpoch, EntryDigest, PreviousEntryDigest, OperationId, canonical request digest, leader identity and the quorum-confirmed commit index. The receipt is authenticated by the COC service signing identity. The verifier checks the signer/key status and the receipt against a current linearizable COC read or a verifiable quorum-commit proof supported by the selected consensus implementation. A leader signature by itself, without a commit-index/quorum proof, is not sufficient. COCCommitReceipt proves only COC log commitment; it never substitutes for an I/D/Storage owner signature or decision.

### 13.2 Explicit crash-fault model and RPO boundary

The initial three-voter/two-quorum profile tolerates one crash/unavailable voter while preserving quorum. RPO 0 applies to every quorum-acknowledged COC entry under this stated crash-fault model, assuming each counted vote has crossed its configured durable-media boundary. Two unavailable voters, correlated loss of a majority, Byzantine behavior, operator deletion, compromised credentials or total correlated site loss are outside the initial availability guarantee. Such conditions do not permit an inferred rollback or a new empty cluster: restore must use the latest externally anchored checkpoint plus contiguous committed log, or remain RESTORE_FENCED. No numeric RTO is claimed.

### 13.3 Proof namespace and authority invariants

- `COCCommitReceipt` / CoordinatorEpoch / CoordinatorIndex prove only COC ordering and commit.
- `CommitAuthorizationReceipt` / I sequencer position / PermissionEpoch prove only I authorization and revocation order.
- D fence request cutoff / effective position / ForgetFenceGeneration prove only D Forget ordering and lineage completion.
- Storage PreparedParticipantReceipt / XID / PublicationReceipt / VisibilityPointer transaction prove only Storage's prepared participant and visibility outcome.
- CSubmitOutcome proves only the observed provider/runtime side effect.
- CausalOrderTerminalProof is a cross-reference bundle over these independently authoritative facts; it cannot mint or upgrade any constituent fact.

Any missing, invalid, stale or contradictory proof keeps the operation UNKNOWN/IN_DOUBT. No authority may infer another authority's decision from a COC index, common transaction ID or elapsed time.

## 14. PostgreSQL prepared-participant identity mapping — Storage normative clarification

This section defines the PostgreSQL 18.x adapter mapping and MUST be read together with Storage design §§15.1–15.7. The complete immutable tuple below is normative for this profile; abbreviated field lists in prior revisions are superseded.

### 14.1 Distinct identity and evidence types

1. `PreparedParticipantRef` is the stable, engine-neutral cross-service identity for one prepared-participant lifecycle. It is opaque, globally unique and never reused.
2. `PreparedTransactionGID` is the client-chosen PostgreSQL prepared-transaction locator. Storage allocates it once, preserves its exact bytes/case, and binds it to the immutable participant tuple. It is a PostgreSQL locator, not a native transaction number.
3. `PostgreSQLNativeXID` is the engine-assigned numeric XID observed from authoritative `pg_prepared_xacts` readback after PREPARE. It is evidence only, never client-preallocated, never a cross-service participant identity and never interchangeable with GID.
4. `CanonicalAuthorityDBRef` and governed non-reusable `DatabaseIncarnationRef` identify the exact canonical authority/database incarnation. `PostgreSQLSystemIdentifier`, `PostgreSQLDatabaseOID`, timeline and LSN are separate typed engine evidence; system identifier/OID/name alone do not establish incarnation identity.
5. `PrepareAttemptRef` + monotonic `PrepareAttemptGeneration` identify one immutable prepare attempt. `ParticipantLedgerRef` + `ParticipantLedgerVersion` identify the durable append-only Storage participant record/version. `ParticipantTupleDigest` covers the complete canonical immutable tuple.

A generic field named `xid` is prohibited. Other database engines MUST define separately tagged locator and native-transaction-ID types.

### 14.2 Required pre-PREPARE binding and sequence

Storage MUST durably allocate and bind, before COC prepare-intent registration: PreparedParticipantRef, PreparedTransactionGID, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, PublicationOperationId, RequestDigest, ParticipantTupleDigest, owner boundary, CausalOrderDomainRef, the single PolicyDomainRef, CanonicalAuthorityDBRef, DatabaseIncarnationRef and the exact database/engine metadata available before PREPARE.

The exact sequence is:
1. Storage commits the immutable reservation and GID mapping as `ALLOCATED_NOT_PREPARED`; this is not a prepared side effect and does not create visibility.
2. COC quorum-commits `JF10_PREPARE_INTENT_REGISTERED` containing the exact participant/GID/attempt/ledger/DB-incarnation tuple and digest, then Storage linearly reads back that exact identity/digest.
3. Only after that authoritative COC readback may Storage issue PostgreSQL PREPARE.
4. Storage reads the authoritative writable primary's `pg_prepared_xacts`, matches exact GID/database and records the observed PostgreSQLNativeXID, original prepare timeline and LSN.
5. Storage persists the signed PreparedParticipantReceipt and receipt digest in the same durable participant ledger before returning it or registering the prepared participant with COC.

A D/I cutoff before step 2 forbids PREPARE. A preallocated reservation in that window may be cancelled only with an append-only Storage terminal-attempt record plus authoritative engine evidence that PREPARE never occurred; absence from `pg_prepared_xacts` alone is insufficient.

### 14.3 PreparedParticipantReceipt required binding

The Storage-signed receipt MUST bind the complete immutable tuple, including:
- PreparedParticipantRef, PreparedTransactionGID, PostgreSQLNativeXID;
- CanonicalAuthorityDBRef, DatabaseIncarnationRef, PostgreSQLSystemIdentifier and PostgreSQLDatabaseOID;
- PrepareAttemptRef, PrepareAttemptGeneration, ParticipantLedgerRef and ParticipantLedgerVersion;
- PublicationOperationId, RequestDigest, ParticipantTupleDigest and exact owner boundary;
- CausalOrderDomainRef, PolicyDomainRef, COC prepare-intent identity/position/digest;
- original prepare timeline/LSN, authoritative PREPARED observation source and time;
- payload/message type and schema version, issuer, subject, owner authority, audience, purpose, key ID/version, algorithm/canonicalization/digest profile identifiers, payload digest and signature.

The receipt proves only that this exact Storage participant was authoritatively PREPARED and remains private. It does not imply I authorization, COC commit beyond the referenced intent, D clearance, C provider outcome, VisibilityPointer/PublicationReceipt publication or G Applied.

### 14.4 Replay, resolution and recovery

- Same participant + same GID + same attempt generation + same complete tuple/digest is lookup/replay and returns the original evidence.
- Any changed tuple field under the same participant/attempt/GID is immutable CONFLICT.
- A new attempt generation is allowed only after an append-only authoritative terminal attempt record and a new COC prepare-intent binding; receipts cannot be carried across attempts.
- GID cannot be reassigned within the DatabaseIncarnationRef and configured retention/archive horizon. Same GID in another authority or incarnation MUST NOT resolve.
- StorageResolutionProof binds the same participant, GID, native XID, DB incarnation, attempt, ledger version, operation/request/tuple digests and owner boundary. COMMITTED includes exact VisibilityPointer and PublicationReceipt transaction identities/digests; ROLLED_BACK includes authoritative non-publication proof; UNKNOWN retains the participant and locks.
- Original prepare timeline/LSN are immutable. Failover/PITR/recovery timeline and LSN are appended as separate RecoveryObservation entries.
- Absence from `pg_prepared_xacts` is never terminal evidence by itself. Storage reconciles the durable outcome ledger with authoritative database readback. Missing, stale, contradictory or unavailable evidence remains UNKNOWN/IN_DOUBT.

### 14.5 Trust and wire ownership

H owns exact wire spelling, nominal encoding, requiredness, nullability, canonical serialization, schema evolution and interoperability vectors. I owns the signature algorithm/profile, issuer/subject authorization, key lifecycle, revocation, historical verification and anti-rollback policy. Until both approve the same versioned envelope and profile, the fields above are a semantic contract candidate, not a cryptographic or wire freeze.


## 15. Normative supersession — Recovery Cutoff Batch / Participant Manifest ordering (Storage v3.1 alignment)

- Amendment class: append-only normative correction to §6.2 and the `AppendRecoveryBatch` API contract.
- Governing Storage companion: Storage Design v3.1, exact Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca`, §§5.2–5.6.
- Superseded COC source Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`.
- This section controls over any inconsistent ordering in §6.2 or earlier API prose. It does not rewrite historical records or claim runtime implementation.

### 15.1 Required ordering and immutable identities

The Recovery Cutoff protocol MUST use the following order. The order is normative and MUST NOT be rearranged:

1. **Keep all affected I/D/C gates closed and freeze owner snapshots.** I, D and C durably close their respective admission/receipt/provider boundaries and capture their own request/participant high-waters, request-set digests, gate generations/cursors and anti-rollback anchors. Each owner signs only its own attestation. A request acknowledged after the snapshot cannot be omitted; it remains behind the closed gate and requires a subsequent batch or authoritative out-of-scope proof under §5.6.
2. **Establish exact committed prefix P.** Verify the quorum-confirmed COC term/index/configuration epoch, contiguous prefix root and external anti-rollback/checkpoint anchor. Any uncertainty remains RESTORE_FENCED.
3. **Enumerate and precompute the complete participant manifest before committing the batch.** Against immutable P, perform linearizable prefix-bound enumeration of every ParticipantIntentRef committed at or before P. Include delayed owner-message delivery, unresolved/prepared JF-10 participants and every participant class discoverable through the authoritative COC registry. Produce the deterministic canonical manifest, explicit empty-set representation, count, root/digest, retrieval locator, enumeration high-water and provenance. Independently re-read and verify the manifest against P. This prepared payload is immutable as a candidate but is not yet an authoritative committed record and cannot authorize release.
4. **Commit COC_RECOVERY_CUTOFF_BATCH.** The quorum-committed batch binds RecoveryEpoch, exact P, complete I/D/C owner snapshot attestations and request-set digests, owner high-waters/gate generations, stable batch idempotency identity, manifest_id, manifest_digest, participant count and enumeration high-water. No protected post-recovery intent, reservation, finalization or favorable read may pass before the required batch/manifest sequence is complete.
5. **Commit PARTICIPANT_SET_RECONCILIATION as a separate immutable manifest record.** This record references the exact committed batch position/digest and repeats RecoveryEpoch, P, manifest_id, manifest_digest, count and enumeration high-water. Its canonical participant-set payload MUST hash to the digest already bound by the batch. Duplicate, omission, count/root/prefix mismatch or changed payload enters RESTORE_FENCED.
6. **Linearizable readback of both records.** Read back the exact batch and exact manifest record from the authoritative quorum log and verify all cross-bindings, prefix, owner attestations, count and digests. Only after both records are confirmed may the coordinator enter PARTICIPANTS_RECONCILING.
7. **Reconcile participants and obtain owner-local releases.** Reconcile each manifest member against its owning I/D/C/Storage evidence. Each Owner independently verifies its own high-water and completeness, and only that Owner may issue its outage-Gate release. COC cannot mint Owner authorization or release.
8. **Complete the RecoveryEpoch only after all required evidence.** Append RECOVERY_EPOCH_COMPLETED only after all manifest participants are accounted for, all required owner-local reconciliations and signed outage-Gate releases are durable, and the exact batch/manifest references and reconciliation root are verified.

### 15.2 Record and API contract

`AppendRecoveryBatch(batch)` MUST reject a request unless it includes the already computed immutable manifest identity and digest, participant count, enumeration high-water, exact prefix P and complete owner snapshot attestations. It appends only the COC_RECOVERY_CUTOFF_BATCH record; it MUST NOT perform participant enumeration after batch commit as the authoritative source of the batch-bound manifest.

The separate `PARTICIPANT_SET_RECONCILIATION` append MUST be idempotent on the stable batch identity plus manifest identity/digest. A retry after a lost ACK performs linearizable same-key lookup and either confirms the exact prior record or resumes the same immutable payload. It MUST NOT mint a replacement batch ID, manifest ID or digest.

The coordinator MUST expose or internally implement an operation equivalent to:
- FreezeAndReadOwnerSnapshots();
- VerifyCommittedPrefix();
- EnumerateAndPrepareManifest(prefix, ownerSnapshots);
- AppendRecoveryBatch(batchWithManifestBinding);
- AppendParticipantSetReconciliation(batchRef, exactManifestPayload);
- ReadBackAndVerifyBatchAndManifest(batchRef, manifestRef);
- BeginParticipantReconciliation();

These names describe required semantic steps, not a mandate for a particular programming-language API.

### 15.3 Crash, retry and late-arrival rules

- Crash before batch commit: no batch exists; remain fenced and resume from the same frozen owner snapshots/prefix only if their anchors remain current, otherwise restart the recovery attempt.
- Batch committed but manifest record absent: remain RESTORE_FENCED; next leader performs same-key lookup and commits/verifies the exact precomputed manifest payload under the same batch identity.
- Manifest record committed but ACK lost: linearizable lookup by exact batch and manifest identity/digest; never create a replacement.
- Batch/manifest cross-binding mismatch or incomplete enumeration: RESTORE_FENCED; no owner release, serving or protected admission.
- Request arriving after an owner snapshot: keep that Owner's gate closed; do not silently mutate the existing batch or manifest. Use a subsequent Recovery Cutoff Batch with a new snapshot/manifest, or prove authoritatively that the request was outside scope and never admitted.
- UNKNOWN participant, delayed message, projection lag, stale replica, missing owner evidence or unresolved prepared XID: remain blocking; absence is not a terminal outcome.

### 15.4 Explicit correction to §6.2

The former §6.2 step 4 ("append RECOVERY_CUTOFF_BATCH") followed by step 5 ("enumerate every affected ParticipantIntentRef") is superseded. The correct order is: freeze owner snapshots; establish P; enumerate and precompute the complete manifest; commit the batch binding the manifest digest/count/high-water; commit the separate manifest record; read back and verify both; then reconcile participants.

This is a substantive ordering correction, not a wording clarification. The old COC Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d` remains immutable historical evidence and MUST NOT be used as the current normative companion for a joint freeze.

### 15.5 Conformance obligations — specified, not executed

- assert the participant enumeration and manifest digest exist before the batch append is invoked;
- assert the batch binds exact manifest ID/digest/count/enumeration high-water and owner snapshots;
- crash after batch commit but before manifest commit and prove all gates remain closed while the same manifest identity is resumed;
- lose the manifest ACK and prove exact same-key readback without replacement identity;
- inject duplicate, omitted, delayed and post-snapshot participants and prove mismatch or subsequent-batch behavior;
- verify both records are quorum-read back and cross-bound before PARTICIPANTS_RECONCILING;
- verify no owner release or protected serving occurs with batch-only state;
- verify UNKNOWN, incomplete enumeration or prefix mismatch remains RESTORE_FENCED.
