# Phase 3.6 — Storage Design: COC Durable Log, Participant Registry & Recovery Cutoff

- Owner: Storage/Consistency
- Date: 2026-11-17
- Status: **STORAGE TECHNICAL DESIGN PROPOSAL — OWNER ACCEPTANCE PENDING**
- Project phase: **ARCHITECTURE DESIGN**
- Parent COC architecture: A branch `session-a-integration-2026-11-16`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Related Storage boundary: `phase-3.6-coc-storage-boundary-acceptance.md`
- Implementation / deployment / conformance: **NOT IMPLEMENTED / NOT DEPLOYED / NOT RUN**
- This proposal does not designate a production operator, select a consensus product, or authorize activation.

## 1. Purpose and non-goals

This document turns the COC logical architecture into a Storage-oriented durable-state and recovery protocol proposal. It specifies the data and ordering contracts required for:

1. quorum-committed append-only COC records;
2. immutable participant intent and exact owner-evidence binding;
3. owner-local I/D cutoffs while COC is unavailable;
4. recovery fencing, batch cutoff, and exhaustive reconciliation;
5. snapshot/restore rollback protection and `RESTORE_FENCED`;
6. explicit separation between COC causal order, I authorization order, D Forget order, and Storage visibility commit order.

It does not select Raft implementation/vendor, cloud/zone topology, key-management provider, storage media, RPO/RTO, retention duration, or a production on-call owner. Those are design decisions requiring A/I/Storage/security/operator review. It does not claim COC itself is the JF-10 transaction coordinator or Storage visibility database.

## 2. Authority and ordering invariants

| Authority | Owns | COC may record | COC MUST NOT decide |
|---|---|---|---|
| C | Provider submission intent and actual provider boundary outcome | C-signed request/outcome evidence | Whether a provider side effect happened absent C evidence |
| I | CommitAuthorizationReceipt, PermissionEpoch, revocation order, JF-10 terminal decision | I-signed receipt/terminal proof and I sequencer position | Authorization, revocation victory, or I terminality |
| D | ForgetFence, lineage coverage, producer-work barrier, ForgetFenceGeneration | D-signed cutoff/clearance evidence and D cursor | Fence effectiveness, lineage completeness, barrier completion |
| Storage | Prepared XID, private participant, VisibilityPointer, PublicationReceipt, owner outcome | Storage-signed prepared/resolved participant evidence | I/D/C decisions or CGH Applied |
| H | Wire encoding, schema/version and integrity mapping | Encoded references/digests | Any owner terminal decision |
| G | Applied and current-use | Applied evidence references where required | N/A; COC cannot mark Applied |
| A | Integration and cross-owner acceptance tracking | Decision/evidence references | Any runtime authority decision |

**Typed positions are never compared across authorities.** COC `(CoordinatorEpoch, CoordinatorIndex)`, I `(PolicyDomainRef, PermissionEpoch, ISequencerPosition)`, D `(BrainAuthorityRef, ForgetFenceGeneration, ProducerRegistrationHighWater, CanonicalCommitCursor)`, and Storage `(CanonicalMemoryAuthorityRef, DBIdentity, XID, OwnerCommitCursor)` are separate namespaces. A signed bridge record may carry all of them, but may not collapse them into a synthetic global sequence.

Safety invariants:

- No quorum-confirmed append, no protected admission/submit/favorable decision.
- No linearizable read, no reservation finalization, barrier release, or terminal inference.
- Same stable ID + same canonical digest is idempotent; same ID + different digest is a hard conflict.
- No COC record alone makes bytes visible, authorizes commit, clears a Forget fence, or proves provider success.
- UNKNOWN/IN_DOUBT is durable and non-expiring. No TTL, heuristic outcome, lease expiry, or operator force-clear.
- No service reopens after quorum recovery or restore until prefix, owner-local cutoffs, and every pre-cutoff participant are reconciled.

## 3. Logical durable model

### 3.1 COC log envelope

Every committed log record has an immutable envelope:

| Field | Meaning |
|---|---|
| `LogRecordId` | Globally unique immutable record identity |
| `RecordType` | Versioned discriminant; unknown critical types fail closed |
| `SchemaVersion` | Exact record schema version |
| `CausalOrderDomainRef` | Authoritative domain resolved by registry, never caller-selected |
| `TransactionId` | Stable protected transaction identity |
| `ParticipantIntentRef` | Stable participant identity, when applicable |
| `OwnerAuthority` | C / I / D / Storage |
| `OwnerRecordRef` | Opaque typed reference to owner evidence |
| `IdempotencyKey` | Stable operation key |
| `CanonicalPayloadDigest` | Digest of canonical immutable payload |
| `CoordinatorEpoch` | Consensus term / epoch |
| `CoordinatorIndex` | Monotonic log index |
| `PreviousEntryDigest` | Digest of previous committed record |
| `EntryDigest` | Digest over envelope and canonical payload |
| `ActorRef`, `KeyId`, `Signature` | Authenticated submitting owner/service evidence |
| `CreatedAt` | Audit metadata only; never used to establish cross-owner order |

The log is append-only. Corrections are additional records that reference the prior record; no in-place mutation or deletion. Canonical serialization, digest algorithm, signature algorithm, key rotation, and algorithm-agility rules are security-owned open decisions.

### 3.2 Minimum record families

| Record | Required immutable payload |
|---|---|
| `DOMAIN_BINDING_VERIFIED` | DomainRef, registry version, binding digest, exact policy/target/lineage mapping refs |
| `PARTICIPANT_INTENT_ACCEPTED` | TransactionId, ParticipantIntentRef, request digest, final boundary, idempotency key, owner refs |
| `I_REVOCATION_REQUEST_RECORDED` | IRevocationRequestRef, PolicyDomainRef, affected tuple digest, I local request ref |
| `D_FENCE_REQUEST_RECORDED` | DForgetFenceRequestRef, ForgetOperationRef, target/lineage digest, D local request ref |
| `RECOVERY_CUTOFF_BATCH_COMMITTED` | RecoveryEpoch, prior quorum prefix, all pending I/D cutoff refs and digests, participant enumeration high-water |
| `I_AUTHORIZATION_TERMINAL_RECORDED` | I-signed terminal proof, receipt ref, I sequencer position, exact transaction/digest |
| `D_PARTICIPANT_CLEARANCE_RECORDED` | D-signed clearance, request cutoff, effective position or explicit pending |
| `PARTICIPANT_RESERVATION_FINALIZED` | Exact I/D proofs, provider idempotency key, immutable reservation digest |
| `JF10_PREPARE_INTENT_REGISTERED` | Stable operation ID/digest, preallocated XID, DB identity, participant ref, pre-prepare COC position |
| `JF10_PREPARED_PARTICIPANT_REGISTERED` | Storage-signed PreparedParticipantReceipt and exact XID/DB/participant binding |
| `C_SUBMIT_OUTCOME_RECORDED` | C-signed actual provider boundary outcome and provider receipt |
| `STORAGE_JF10_PARTICIPANT_RESOLVED` | Same-XID commit/rollback evidence; commit includes exact PublicationReceipt |
| `PARTICIPANT_TERMINALIZED` | Terminal proof ref and complete evidence-set digest |
| `RECOVERY_RECONCILIATION_RECORDED` | Same-transaction recovery facts; no synthetic success |
| `CHECKPOINT_COMMITTED` | Checkpoint ID, term/index, root digest, snapshot digest, prior checkpoint ref, retention metadata |

COC stores signed owner proofs or immutable references plus their digests. It does not copy mutable owner state and does not reinterpret owner signatures.

### 3.3 Participant registry projection

The participant registry is a deterministic projection of the committed log, not a second authority. Minimum fields:

- `TransactionId`, `ParticipantIntentRef`, `CausalOrderDomainRef`;
- `IdempotencyKey`, `CanonicalPayloadDigest`, `RecordPosition`;
- typed I/D/C/Storage evidence refs and digests;
- JF-10 preallocated `XID` + `DBIdentity` binding when applicable;
- participant state, last state-transition record position, evidence-set digest;
- `UnresolvedReason`, `RecoveryEpoch`, `FirstSeenCheckpoint`.

The projection can be rebuilt from a verified log prefix. If projection checkpoint and log digest disagree, discard/rebuild projection; never use it to authorize an outcome. An unavailable or stale projection means the operation remains UNKNOWN until a linearizable log-derived read succeeds.

## 4. Append and read protocol

### 4.1 Append

`Append(record)` MUST:

1. authenticate owner/service identity and verify issuer, audience, schema version, key status, signature, domain binding, and canonical payload digest;
2. resolve the stable idempotency key in the quorum-confirmed prefix;
3. return the original position if the key and digest match exactly;
4. return hard `CONFLICT` and preserve audit evidence if the key exists with a different digest;
5. validate state-machine preconditions against the current quorum-confirmed state;
6. append under the current consensus term and obtain quorum durable commit;
7. return a signed commit receipt containing term/index/entry digest only after quorum commit.

A leader-local append, local fsync, follower receipt, event-bus ACK, HTTP success, or uncommitted index is not a commit. The response lost after quorum commit is resolved by same-key linearizable lookup, never a new ID.

### 4.2 Read APIs

Required APIs:

- `ReadLinearizable(TransactionId, digest)`;
- `ReadLinearizableDomainPrefix(CausalOrderDomainRef)`;
- `ListUnresolvedParticipants(domain, prefix)`;
- `ReadCutoffState(ownerRequestRef)`;
- `ReadCheckpointAndPrefixProof(checkpointId)`;
- `ReadParticipantByXid(DBIdentity, XID)` (delegated to Storage authoritative read, not answered by COC's projection);
- `ReconcileSameTransaction(TransactionId, evidence)`.

Follower/stale reads may support dashboards only when explicitly marked non-authoritative. They cannot gate a protected action.

## 5. COC availability and recovery state machine

### 5.1 Coordinator service states

`SERVING → QUORUM_UNAVAILABLE → RECOVERY_FENCED → PREFIX_VERIFIED → CUTOFF_BATCH_COMMITTED → PARTICIPANTS_RECONCILING → SERVING`

Any failed proof transitions to `RESTORE_FENCED`. These are service admission states, not substitutes for the consensus log's term/index.

- `SERVING`: quorum write/read available; protected operations may proceed subject to owner gates.
- `QUORUM_UNAVAILABLE`: no quorum-confirmed writes or favorable reads; C/I/D owner-local gates close for affected operations.
- `RECOVERY_FENCED`: after quorum returns or a new leader is elected, protected writes/finalization remain disabled until recovery epoch and prefix verification complete.
- `PREFIX_VERIFIED`: quorum agrees on committed prefix, term, index and digest; owner-local pending requests are being collected.
- `CUTOFF_BATCH_COMMITTED`: one immutable batch record contains all outage-period I/D pending cutoffs and prior-prefix participant high-water.
- `PARTICIPANTS_RECONCILING`: every pre-batch participant is enumerated and owner evidence reconciled; unresolved participants remain blocking.
- `RESTORE_FENCED`: missing prefix, rollback, stale checkpoint, owner high-water mismatch, digest conflict or incomplete reconciliation. No protected operation or barrier release.

A new leader MUST start in `RECOVERY_FENCED`; it must not infer `SERVING` from process startup or a reachable local disk. The transition to `SERVING` requires a durable, quorum-confirmed recovery-complete record tied to the verified prefix, recovery batch, owner high-water set and unresolved participant enumeration. If the leader crashes before this record commits, the next leader starts fenced again.

### 5.2 Owner-local outage gates

When COC cannot confirm quorum commit:

- D durably writes `PENDING_COC_CUTOFF` locally and closes admission for the affected target/source/ancestor lineage before acknowledging the request as pending.
- I durably writes `PENDING_COC_CUTOFF` locally and suspends affected receipt issuance and consumption before acknowledging the request as pending.
- These local gates survive owner restart/failover. Owner-local timestamps are audit metadata only; they cannot order I against D or either owner against COC.
- COC unavailable does not mean owner requests are lost or that new affected operations may proceed.

### 5.3 Recovery cutoff algorithm

1. New leader enters `RECOVERY_FENCED` and refuses protected appends, reservation finalization, and favorable reads.
2. Verify the quorum-confirmed committed prefix: consensus epoch, last index, last entry digest, membership/configuration epoch, and checkpoint anchor. Any mismatch -> `RESTORE_FENCED`.
3. Ask I and D for authenticated, durable inventories of their owner-local pending cutoff requests, including stable request refs, digests, authority cursors and local high-water marks. Do not sort I and D requests by time.
4. Capture the exact last pre-recovery COC prefix `P=(epoch,index,digest)`. Atomically append one `RECOVERY_CUTOFF_BATCH_COMMITTED` record containing P, a RecoveryEpoch, the complete I request set, complete D request set, and per-owner high-water/digest manifests.
5. The batch record is the common cutoff barrier. It does not assign a relative order to independent I/D requests inside the batch. Each owner retains its own internal order and commits its own terminal decision/effective fence.
6. Enumerate every participant intent committed at or before P, using a linearizable prefix-bound query. Persist the participant count, sorted stable ParticipantIntentRefs (or a deterministic Merkle/set digest plus retrievable manifest), and the enumeration high-water in the batch/recovery evidence.
7. Reconcile every pre-P participant against I, D, C and Storage authoritative sources. No participant may be omitted due to delayed messages, owner ACK loss, projection lag or a stale replica.
8. Persist per-participant reconciliation records idempotently. IN_DOUBT stays unresolved and continues blocking the relevant owner gates/barriers; no TTL or operator override.
9. I and D verify that every pending local request is represented in the batch, every pre-P participant is accounted for, and their own high-water/cursors are monotonic. They then issue signed gate-clearance acknowledgements bound to the RecoveryEpoch and batch digest. Acknowledgement clears only the local outage gate; it does not itself grant authorization or make a D fence effective.
10. COC appends `RECOVERY_EPOCH_COMPLETED` only after all required owner acknowledgements and the participant enumeration/reconciliation manifest are complete. Only then may COC return to `SERVING`. Any lost ACK is resolved by same-key read; no new batch or RecoveryEpoch may be minted to escape ambiguity.

The batch append must be serialized before any post-recovery protected intent. If the batch cannot be made complete or a required owner is unavailable, the coordinator remains fenced. The protocol MUST NOT reopen admission and then append the cutoff asynchronously.

### 5.4 Concurrent owner requests and idempotency

- Each owner-local request has a stable owner request ID, canonical digest and owner-local sequence/cursor.
- The batch includes all requests visible in the owner's durable pending-gate snapshot at its declared high-water.
- A request arriving after that snapshot remains behind the still-closed owner gate and must be included in a subsequent recovery batch before that gate can reopen.
- Same owner request ID + same digest is idempotent; same ID + changed digest is conflict and keeps the gate closed.
- I and D may have different request counts and cursor types. No synthetic sort key or wall-clock tie-break is allowed.

## 6. Snapshot, compaction and restore

A checkpoint contains:

- quorum-certified `CoordinatorEpoch`, `CoordinatorIndex`, last `EntryDigest`;
- consensus membership/configuration epoch and committed configuration history;
- snapshot digest and previous checkpoint ref;
- complete participant registry projection and unresolved participant manifest;
- all pending/recovery cutoff batches and owner-local gate refs known at the checkpoint;
- owner high-water manifests and reconciliation evidence digest;
- signing-key identity/status references needed to verify retained evidence.

Rules:

1. Snapshot only at a committed index; never snapshot leader memory or an uncommitted suffix as authoritative.
2. Retain the complete log suffix after the checkpoint and verify previous-digest continuity.
3. Compaction may remove old payload bytes only after a quorum-certified checkpoint and approved durable evidence archive are verified; never compact unresolved/IN_DOUBT participant state or the evidence needed to prove terminality.
4. Restore must compare against the newest independently retained checkpoint/high-water anchor. If the anchor is missing, stale, rolled back, or unverifiable, enter `RESTORE_FENCED`.
5. Rebuild projections from the verified log. Projection mismatch is repairable; missing authoritative log prefix is not.
6. Before serving, reconcile every owner-local pending gate and every participant at or before the restored cutoff. No reader, submit, reservation, or owner barrier may reopen before this completes.

## 7. Participant state machine and JF-10 bridge

COC participant states:

`UNSEEN → INTENT_ACCEPTED → OWNER_TERMINALS_PENDING → PREPARE_INTENT_REGISTERED → PREPARED_PARTICIPANT_REGISTERED → OWNER_FINAL_GATE_PENDING → {COMMIT_WON | ABORT_WON | IN_DOUBT | CONFLICT} → STORAGE_RESOLVED → TERMINALIZED`

- `PREPARE_INTENT_REGISTERED` binds stable operation ID/digest, preallocated XID, DB identity, ParticipantIntentRef and COC position.
- `PREPARED_PARTICIPANT_REGISTERED` requires Storage-signed PreparedParticipantReceipt for that same XID/digest/DB identity.
- I alone supplies the terminal COMMIT/ABORT/INDETERMINATE decision and I sequencer position.
- Storage alone resolves the same prepared XID and proves committed PublicationReceipt or rollback/non-publication.
- COC records those owner proofs and tracks unresolved participants; it cannot synthesize a decision.
- If COC is unavailable after Storage PREPARE, XID and locks remain durable/private. No second XID or operation identity may be created.
- I COMMIT during COC outage means Storage forward-commits the same XID; I ABORT means Storage rolls back the same XID. COC observation is later idempotent reconciliation, not a prerequisite to the owner decision.
- A COC record is not itself a visibility record. A Storage PublicationReceipt is not COC terminality or G Applied.

Multi-PolicyDomain JF-10 remains unsupported unless I approves a separate atomic authorization profile.

## 8. Failure matrix

| Failure point | Durable facts | Required state / recovery |
|---|---|---|
| Leader dies before quorum commit | No committed record | Retry same key; remain fenced if quorum unavailable |
| Leader dies after quorum commit before ACK | Record exists in committed prefix | Linearizable same-key read returns same position |
| Minority partition | No quorum write/read | Owner-local gates closed; no favorable result |
| New leader elected | Term changes; prefix must be verified | Start `RECOVERY_FENCED`; no protected writes |
| Owner cutoff arrives during outage | Owner-local pending gate durable | Include in recovery batch; no reopen |
| Batch append ACK lost | Batch may be committed | Same-key linearizable read; never mint another batch |
| Owner unavailable during reconciliation | Prefix/batch may be valid; owner proof absent | Remain `PARTICIPANTS_RECONCILING` / `RESTORE_FENCED` |
| Pre-batch participant omitted | Enumeration digest/count mismatch | `RESTORE_FENCED`; no gate clear |
| Storage prepared XID unknown | Same XID may exist | IN_DOUBT; retain locks/private state; authoritative same-XID lookup |
| I terminal proof unavailable | No verified terminal decision | IN_DOUBT; no synthetic COMMIT/ABORT |
| Snapshot behind external anchor | Prefix/high-water rollback | `RESTORE_FENCED` |
| Duplicate key, changed digest | Conflicting immutable intent | CONFLICT; preserve both evidence references; no transition |
| Signature/key revoked or invalid | Owner evidence untrusted | Reject; security audit; no terminalization |

## 9. Security and retention boundary

- COC authenticates each owner and validates signature, audience, schema version, key status, domain binding and exact digest; it never signs on behalf of owners.
- Node administration, key rotation, restore, checkpoint rollback exception and conflict reconciliation are separate privileged roles. High-risk recovery requires two-person approval; no admin role can erase unresolved participant evidence.
- Encrypt in transit and at rest. KMS/HSM, key custody, rotation, revocation propagation and compromise recovery require I/Security approval.
- Metrics include quorum health, term/index/digest, commit latency, unresolved participant age/count, local pending gate age, recovery epoch, checkpoint lag, RESTORE_FENCED duration, key failures and conflicting idempotency keys.
- Retention, privacy/data residency, immutable archive and RPO/RTO remain explicit design decisions. Unresolved/IN_DOUBT participants are never TTL-expired or compacted away.

## 10. Required architecture decisions / owner acceptance

| Decision | Accountable owner | Current status |
|---|---|---|
| Consensus algorithm and safety model (Raft or equivalent crash-fault-tolerant protocol) | A + Storage | Candidate; exact profile review pending |
| Three-voter/two-quorum failure-domain assumptions | A + Storage + operator/security | Design target only |
| COC canonical serialization, digest and signature profile | H + I + A | Pending exact schema/security decision |
| COC recovery-batch API and request inventory contract | A + I + D + Storage | Proposed here; owner acceptance pending |
| Owner-local pending-gate durability and clear protocol | I and D | Owner confirmation required |
| Participant/XID bridge records | I + D + Storage + A | Must reconcile with JF-10 owner-final-gate requirement |
| Snapshot external high-water/rollback anchor | A + Storage + I | Pending |
| Retention, archive and RPO/RTO | Storage + accountable operator + security | Deferred to design selection / engineering handoff |
| Multi-PolicyDomain atomicity | I | Unsupported / blocked in v1 |

## 11. Architecture acceptance checklist

The design is ready for cross-owner review only when each item is explicitly accepted or amended by its owner:

- [ ] A accepts COC state machine, log semantics and recovery batch as the integration architecture.
- [ ] I accepts revocation-cutoff behavior, I receipt/terminal proof semantics, and owner-local gate close/reopen rules.
- [ ] D accepts fence cutoff, barrier participant enumeration, D-local gate close/reopen and effective-fence rules.
- [ ] C accepts provider idempotency and actual submit-outcome evidence boundary.
- [ ] H accepts canonical wire/schema/digest/signature mapping.
- [ ] Storage accepts durable log/participant registry/recovery design and exact same-XID Storage evidence boundary.
- [ ] All owners accept the crash matrix and UNKNOWN/IN_DOUBT invariants.
- [ ] A records the exact artifact versions and owner decisions in the integration tracker.

**Disposition:** Storage technical design proposal only. Owner acceptance pending. No implementation, deployment, conformance, production readiness, or production activation is claimed.