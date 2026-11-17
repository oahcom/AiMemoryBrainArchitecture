# Phase 3.6 — Storage Design v3.1: COC Durable Log, Recovery Cutoff, Owner Gates & JF-10 Bridge

- Owner: Storage/Consistency
- Date: 2026-11-17
- Status: **REVISED STORAGE TECHNICAL DESIGN PROPOSAL v3.1 — FRESH EXACT-VERSION OWNER REVIEW REQUIRED**
- Project phase: **ARCHITECTURE DESIGN**
- Supersedes the earlier Storage design draft at commit `9a975f665ee60f4551effe0104ea8f867716d9dd`, blob `cd5566b3d99b5204401ac713a5bb2dcf89a02726`.
- Exact five-Owner review baseline (pinned by A/I/D/C/H acceptance artifacts): `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`.
- Current Storage companion clarification source: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` (PostgreSQL prepared-participant identity mapping integrated in §7.5; this later Blob is not misrepresented as the five-review baseline).
- Parent COC architecture: A branch `session-a-integration-2026-11-16`, blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Related Storage boundary: `phase-3.6-coc-storage-boundary-acceptance.md`
- Implementation / deployment / conformance: **NOT IMPLEMENTED / NOT DEPLOYED / NOT RUN**
- This proposal does not freeze cryptographic algorithms, wire schemas, a consensus product, production topology, or authorize activation.
- This v3.1 is a new immutable review target. v3 and earlier review decisions remain historical evidence only.

## 1. Purpose, scope and non-goals

This proposal specifies Storage-facing durable-state, participant-accounting and recovery contracts for the COC append-only quorum log. It addresses five independent Owner reviews (A, I, D, C and H) of the exact review baseline Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`, plus the subsequent A exact-version R1–R6 review as an additional blocking clarification set. The older Storage design draft Blob `cd5566b3d99b5204401ac713a5bb2dcf89a02726` is a separate predecessor, not the exact artifact pinned by the five Owner acceptance records.

It covers:
1. quorum-committed COC records and deterministic participant accounting;
2. an atomic, prefix-bound Recovery Cutoff Batch plus a separately committed immutable participant manifest;
3. durable owner-local cutoff gates and explicit C fail-closed side-effect admission;
4. snapshot/restore anti-rollback requirements and recovery fencing;
5. Storage's exact-XID prepared transaction and publication evidence;
6. a separately gated JF-10 observation/recovery bridge which does not expand COC or Storage authority.

It does not select a consensus implementation/vendor, cryptographic suite, key-management provider, cloud/zone topology, storage media, RPO/RTO, retention period or production operator. Those remain design decisions and block protocol freeze/deployment until approved by their accountable owners.

## 2. Authority and typed-order invariants

| Authority | Owns | COC may record | COC MUST NOT decide |
|---|---|---|---|
| C | Provider submission intent, provider idempotency namespace and actual provider boundary outcome | C-signed request/outcome evidence | Provider success, failure or handoff absent C evidence |
| I | CommitAuthorizationReceipt, PermissionEpoch, revocation order, JF-10 terminal decision and single-use receipt consumption | I-signed sequenced decision and evidence | Authorization, revocation victory or I terminality |
| D | ForgetFence, ForgetFenceGeneration, lineage coverage and producer-work barrier | D-signed cutoff, membership and clearance evidence | Fence effectiveness, lineage completeness or barrier completion |
| Storage | Prepared XID, DB identity, private participant, VisibilityPointer and PublicationReceipt | Storage-signed prepare/resolution evidence | I/D/C decisions or G Applied |
| H | BMCP wire representation, schema/version and transport integrity mapping | Encoded typed references and digests | Any owner decision or gate release |
| G | Applied and current-use | Applied evidence references where required | COC cannot mark Applied |
| A | Integration and cross-owner acceptance tracking | Decision/evidence references | Runtime authority decisions |

**Typed positions are distinct opaque namespaces and are never compared or sorted against one another.** COC (epoch/index), I (PolicyDomainRef/PermissionEpoch/I sequencer position), D (BrainAuthorityRef/ForgetFenceGeneration/producer high-water/canonical cursor), Storage (canonical memory authority/DB identity/XID/owner commit cursor), and C (provider-specific request/outcome references) cannot be collapsed into a synthetic global sequence. Wall-clock timestamps are audit metadata only.

Safety invariants:
- No quorum-confirmed COC prefix and no authoritative owner-local gate state means no new protected admission, reservation finalization or provider invocation.
- No linearizable read means no favorable COC-derived result or terminal inference.
- Stable identity + same canonical digest is idempotent; same identity + changed digest is a hard conflict.
- COC records observations and evidence; they do not make bytes visible, authorize commit, clear ForgetFence, or prove provider success.
- UNKNOWN/IN_DOUBT is durable, non-expiring and blocking. No TTL, timeout, lease expiry, heuristic outcome or operator force-clear.
- A leader/owner restart, stale snapshot, restore, lost ACK or delayed message never reopens a gate by itself.
- COC recovery completion, owner-local outage-gate release, I terminal decision, D Forget effectiveness, Storage visibility and C provider outcome are separate facts/events.

## 3. Durable log and participant model

### 3.1 Immutable COC envelope

Every committed record MUST carry:
- immutable LogRecordId and versioned RecordType;
- exact SchemaVersion and CausalOrderDomainRef resolved by the authoritative registry;
- TransactionId and ParticipantIntentRef when applicable;
- OwnerAuthority and typed OwnerRecordRef;
- stable idempotency identity and canonical payload digest;
- CoordinatorEpoch, CoordinatorIndex, PreviousEntryDigest and EntryDigest;
- authenticated ActorRef, issuer/audience, KeyId, signature and key-status evidence reference;
- canonicalization profile identifier and digest/signature algorithm identifiers once approved;
- CreatedAt for audit only.

The log is append-only. Corrections are additional records referring to earlier records; no in-place mutation or deletion. Unknown critical record types fail closed. Unknown non-critical types may be retained only under an explicitly versioned forward-compatibility rule and must never be interpreted as terminal evidence.

### 3.2 Required record families

| Record | Required immutable content |
|---|---|
| `DOMAIN_BINDING_VERIFIED` | DomainRef, registry version, binding digest, exact policy/target/lineage mapping refs |
| `PARTICIPANT_INTENT_ACCEPTED` | TransactionId, ParticipantIntentRef, request digest, final boundary, idempotency identity and owner refs |
| `I_REVOCATION_REQUEST_RECORDED` | I request ref, PolicyDomainRef, affected tuple digest, I-local request ref |
| `D_FENCE_REQUEST_RECORDED` | D request ref, ForgetOperationRef, target/source/ancestor selector digest, D-local request ref |
| `OWNER_LOCAL_PENDING_GATE` | Owner, gate ref/generation, stable request ID/digest, owner cursor/high-water, pending disposition |
| `COC_RECOVERY_CUTOFF_BATCH` | RecoveryEpoch, exact prefix P, I/D owner snapshot attestations, manifest ID/digest/count/high-water, batch idempotency identity |
| `PARTICIPANT_SET_RECONCILIATION` | Exact batch ref/digest, manifest ref/digest, participant refs and reconciliation status/evidence |
| `OWNER_LOCAL_GATE_RELEASE` | Owner-signed release, gate generation, RecoveryEpoch, batch and manifest digests, owner high-water and reconciliation proof |
| `COC_RESTORE_FENCED` | RecoveryEpoch, failed proof class, prefix/checkpoint refs and immutable reason digest |
| `I_JF10_TERMINAL_DECISION_OBSERVED` | I-signed decision ref/digest, exact final-gate participant tuple and I sequencer position |
| `STORAGE_JF10_PARTICIPANT_RESOLVED` | Same-XID Storage proof, DB identity, outcome and PublicationReceipt or non-publication proof |
| `C_SUBMIT_OUTCOME_RECORDED` | C-signed actual provider boundary outcome, provider idempotency identity and receipt/lookup ref |
| `JF10_BRIDGE_RECONCILIATION_RECORDED` | Typed references/digests for I, D, C and Storage evidence; no synthesized decision |
| `RECOVERY_EPOCH_COMPLETED` | Verified prefix, batch/manifest refs, reconciliation root, required owner acknowledgements |
| `CHECKPOINT_COMMITTED` | Checkpoint ID, term/index/root, snapshot digest, previous checkpoint, retention/archive evidence refs |

The participant registry is a deterministic projection of the committed log, never a separate authority. It includes stable transaction/participant identity, domain, idempotency identity, exact owner evidence refs/digests, XID/DB identity when applicable, state, transition position, unresolved reason, RecoveryEpoch and checkpoint provenance. Projection disagreement is repaired by rebuilding from the verified prefix; it never authorizes an outcome.

## 4. Append, read, replay and error contract

### 4.1 Append

`Append(record)` MUST authenticate the submitting authority; validate issuer/audience, schema/version, key status, signature, domain binding, canonical digest and state-machine preconditions; resolve idempotency identity against the quorum-confirmed prefix; return the original committed position for an exact replay; reject same identity/different digest as CONFLICT with immutable audit evidence; and return a signed commit receipt only after quorum durable commit.

A leader-local append, local fsync, follower receipt, event-bus ACK, HTTP success or uncommitted index is not a commit. A lost response is transport UNKNOWN, not a transaction outcome. Resolve it by authoritative linearizable same-identity lookup under the same message family and digest; never mint a replacement identity.

### 4.2 Required authoritative reads

- `ReadLinearizable(TransactionId, digest)`
- `ReadLinearizableDomainPrefix(CausalOrderDomainRef)`
- `ReadUnresolvedParticipants(domain, exact_prefix)`
- `ReadCutoffState(owner_request_ref)`
- `ReadCheckpointAndPrefixProof(checkpoint_id)`
- `ReadParticipantByXid(DBIdentity, XID)` (delegated to Storage's authoritative source, never inferred from COC projection)
- `LookupByIdempotencyIdentity(identity, digest, message_family)`
- `ReconcileSameTransaction(TransactionId, typed_evidence)`

Follower/stale reads are dashboard-only and must be explicitly marked non-authoritative.

### 4.3 Typed outcomes

The protocol/API envelope must distinguish at least:
- `QUORUM_UNAVAILABLE`
- `LINEARIZABLE_READ_UNAVAILABLE`
- `UNKNOWN` (transport/result not authoritatively resolved)
- `IN_DOUBT` (durable participant outcome unresolved)
- `CONFLICT` (same identity, different digest)
- `OWNER_UNAVAILABLE`
- `RESTORE_FENCED`
- `COMMITTED` (COC record quorum committed only; not owner terminality)

Timeout, lost ACK, connection reset or client cancellation MUST NOT be encoded as COMMIT, ABORT, provider rejection or safe rollback.

## 5. Recovery Cutoff Batch — normative v2 protocol

### 5.1 Recovery states

`SERVING → QUORUM_UNAVAILABLE → RECOVERY_FENCED → PREFIX_VERIFIED → CUTOFF_BATCH_COMMITTED → PARTICIPANT_MANIFEST_COMMITTED → PARTICIPANTS_RECONCILING → RECOVERY_EPOCH_COMPLETED → SERVING`

Any failed, missing, stale or contradictory proof enters `RESTORE_FENCED`. A new leader MUST start `RECOVERY_FENCED`; process startup, local disk availability or leader election never implies readiness.

### 5.2 Owner inventory freeze and high-water capture

Before acknowledging a pending cutoff, each authority durably closes its own gate and atomically captures a stable owner-local request snapshot:
- I suspends affected receipt issuance and consumption and captures I request refs/digests plus monotonic I high-water.
- D closes admission for affected target/source/ancestor lineage and captures D request refs/digests, ForgetOperationRefs, selector digests and monotonic D high-water.
- C closes protected side-effect admission as defined in §6 and captures every already admitted provider participant and its provider-boundary state.
- Each owner attests the snapshot using its own authority, request-set digest, high-water/cursor, gate generation and local anti-rollback generation/anchor.

The owner snapshot operation is atomic with gate closure: a request is either included at/below the captured high-water or is after it and remains behind the still-closed gate. It MUST NOT be possible for a racing request to be acknowledged as pending yet omitted from both snapshots. I and D inventories are never sorted against each other.

### 5.3 Exact prefix and participant manifest construction

After quorum returns, the coordinator enters `RECOVERY_FENCED` and disables all protected appends, reservations, finalizations and favorable reads. It verifies the exact last committed prefix:

`P = (CoordinatorEpoch, CoordinatorIndex, EntryDigest, committed configuration epoch)`.

Any missing log suffix, digest discontinuity, term/configuration ambiguity, stale checkpoint or rollback evidence enters `RESTORE_FENCED`.

Against this immutable P, the coordinator performs a linearizable, prefix-bound enumeration of **every** participant intent committed at or before P. It computes a deterministic, retrievable manifest before the batch is committed. The manifest includes:
- RecoveryEpoch and exact P;
- sorted unique ParticipantIntentRefs in canonical opaque-reference byte order;
- participant count, manifest root/digest and retrieval locator;
- COC enumeration high-water and query/projection provenance;
- per-participant typed C/D/I/Storage evidence references known at P;
- explicit empty-set representation (empty array, never null; one canonical encoding);
- duplicate detection and conflict evidence.

The manifest is immutable and its digest is computed over a domain-separated canonical representation. No participant may be excluded due to projection lag, delayed messages, stale replica, owner ACK loss or a post-P index. If the complete manifest cannot be obtained and independently re-read against P, remain fenced.

### 5.4 Batch and manifest commit sequence (resolves v1 atomicity gap)

The protocol uses two immutable quorum-committed records to avoid circular digest dependencies while binding the complete set:

1. **Prepare immutable manifest payload** as above, bound to RecoveryEpoch, P and the frozen I/D owner high-water attestations. Compute `manifest_id` and `manifest_digest`. This precomputed payload is not yet authoritative or sufficient to reopen anything.
2. **Commit `COC_RECOVERY_CUTOFF_BATCH`** with a stable batch identity. It binds exact P, RecoveryEpoch, complete I and D snapshot attestations and request-set digests, owner high-water/gate generations, `manifest_id`, `manifest_digest`, participant count and enumeration high-water. The batch is quorum committed before any post-recovery protected intent.
3. **Commit `PARTICIPANT_SET_RECONCILIATION` / manifest record** as a separate immutable record, referencing the exact committed batch position/digest and repeating `manifest_id`, `manifest_digest`, P and count. Its canonical participant-set payload MUST hash to the digest already bound by the batch. Any mismatch, omission, duplicate or changed payload enters `RESTORE_FENCED`.
4. Read back both records linearly and verify their cross-bindings before entering `PARTICIPANTS_RECONCILING`.

The batch is not complete merely because step 2 committed. Serving and owner-gate release require both the batch and its exact manifest record. A crash between steps 2 and 3 leaves the next leader fenced; it resumes by same-key lookup and commits/verifies the same manifest, never creates a replacement batch or manifest identity.

### 5.5 Reconciliation and recovery completion

For every participant in the manifest, reconcile authoritative evidence from I, D, C and Storage as applicable. Record per-participant outcomes idempotently and preserve each authority's evidence as separate typed references. Missing owner evidence, ambiguous provider handoff, unresolved prepared XID, unknown lineage, stale high-water or digest conflict remains blocking.

I and D independently verify:
- all their frozen pending requests are represented exactly once;
- owner-local high-water and gate generation are monotonic and anchored;
- every pre-P participant relevant to their authority is accounted for;
- no request after the captured high-water was admitted through the closed gate;
- the exact batch and manifest digests match their attestations.

C independently verifies all pre-P side-effect participants and provider evidence under §6. Storage independently verifies prepared XID and same-XID resolution evidence under §7.

Only after all required participant reconciliations and owner-signed outage-gate releases are durably recorded may COC append `RECOVERY_EPOCH_COMPLETED`, bound to P, batch, manifest, reconciliation root and owner acknowledgements. A crash before that record leaves the next leader fenced. `RECOVERY_EPOCH_COMPLETED` means COC service recovery is complete only; it does not mean I authorization, D Forget effectiveness, Storage visibility, C provider success or G Applied.

### 5.6 Requests arriving after an owner snapshot

A request arriving after an owner's captured high-water remains behind that owner's closed gate. It is not silently appended to the already frozen batch. Before that owner gate may reopen, the owner must either:
- include the request in a subsequent Recovery Cutoff Batch with a new immutable snapshot/manifest; or
- prove through its own monotonic cursor and gate-generation protocol that the request is outside the affected scope and was never admitted.

No owner may release its gate while an unrepresented request exists. Same request ID/digest is idempotent; changed digest is CONFLICT and keeps the gate closed.

## 6. Owner-local gates and C side-effect admission

### 6.1 I gate

I alone closes and releases its local gate. CloseIRecoveryGate MUST be one serializable I PolicyDomain sequencer transaction: append the idempotent IRevocationRequestRef/RequestDigest, set the affected gate to PENDING_COC_CUTOFF, increment GateGeneration and capture request-set count/digest/high-water before acknowledging. Every affected receipt issuance and consumption transaction serializes through that same sequencer and checks gate state/generation in-transaction. If gate-close commits first, issuance/consumption is denied; if it commits later, the exact admitted operation remains in the durable I ledger and recovery inventory. No admitted operation may exist outside both records. Its pending attestation binds I authority, stable request IDs/digests, PolicyDomainRef, I cursor/high-water, gate generation, RecoveryEpoch (when known), and anti-rollback anchor.

I release is an I-signed, idempotent, monotonic CAS bound to the exact batch and manifest digests, complete I request set/count/digest, I high-water, GateGeneration, independent anti-rollback anchor and complete applicable participant reconciliation root. Immediately before release, I rechecks the current request-set high-water and scope generation. Any advance, new in-scope request or omission keeps the gate closed and requires a subsequent batch/manifest. COC cannot issue I release. Release clears only the outage gate; it does not issue authorization, advance PermissionEpoch or decide revocation victory.

### 6.2 D gate

D alone closes and releases its local gate. Before acknowledging a pending cutoff, D durably closes admission for all affected target/source/ancestor scopes and persists ForgetOperationRef, selector digest, D cursor/high-water, gate generation and anti-rollback anchor.

For each D fence request, D must produce a per-fence affected-lineage membership/completeness manifest. Each participant is authoritatively classified affected/not-affected with supporting lineage evidence. Unknown lineage remains blocking. A global pre-P participant set is not a substitute for per-fence lineage membership.

D release is D-signed, idempotent and monotonic, bound to RecoveryEpoch, exact batch/participant-manifest digests, D request set, D high-water and complete affected-lineage reconciliation. It clears only the outage gate. It does not make Forget effective or release the producer-work barrier. D separately commits effective ForgetFenceGeneration only after every lineage and producer-work barrier obligation is satisfied.

If D cannot prove cursor monotonicity after restart/restore, its gate remains closed. Gate release, effective ForgetFence and producer barrier completion are three distinct states.

### 6.3 C gate and provider boundary

C's runtime gate is a fail-closed side-effect admission rule, not an I/D authority gate:
- If COC quorum, exact prefix, recovery cutoff state or relevant I/D gate state cannot be authoritatively confirmed, C MUST NOT create/accept a new protected intent/reservation and MUST NOT invoke the provider for that protected operation.
- C MUST NOT infer absence of an I revocation or D fence from COC unavailability.
- A participant already admitted before the gate closed is not blindly cancelled or replayed. It is included in the recovery manifest and reconciled against C's authoritative provider evidence.
- Before any provider side effect, C freezes the exact request identity/digest, owner boundary and provider idempotency key/namespace.
- **Provider invocation is permitted only after I has durably decided `COMMIT_WON` for the exact bound operation/final-gate participant and every required D predicate for that operation is satisfied.** An I `REVOCATION_WON`, `INDETERMINATE_ABORTED` or other abort terminal requires same-XID Storage rollback/non-publication and MUST NOT invoke the provider. `UNKNOWN` / `IN_DOUBT`, missing I proof, mismatched tuple or unresolved D predicate blocks provider invocation.
- Any pre-provider reservation is strictly non-side-effecting: it may reserve internal bookkeeping capacity but MUST NOT contact the provider, create externally observable work, or be represented as provider handoff.
- C records actual provider boundary evidence only. Provider ACCEPTED requires determinate handoff evidence; definitive REJECTED requires proof of no handoff. Timeout, process death, lost response or contradictory evidence is UNKNOWN/IN_DOUBT.
- Recovery uses the same provider key and authoritative provider lookup where supported. Never mint a new transaction, reservation or provider key to escape ambiguity.

Provider-specific idempotency namespace, retention window, lookup consistency, duplicate-submit behavior and whether an ambiguous operation can be queried without resubmission MUST be specified and verified per adapter before production claims. If a provider cannot prove safe same-key recovery, the participant remains IN_DOUBT; exactly-once behavior MUST NOT be claimed.

The C manifest state for every participant distinguishes: NOT_INVOKED, INVOCATION_IN_PROGRESS, ACCEPTED_WITH_HANDOFF_EVIDENCE, REJECTED_WITH_NO_HANDOFF_PROOF, and UNKNOWN/AMBIGUOUS. C evidence is never inferred from Storage resolution; Storage visibility is never inferred from provider acceptance.

### 6.4 Gate anti-rollback and release

Every owner pending/release attestation binds owner authority, stable request ID/digest, owner cursor/high-water, local gate generation, RecoveryEpoch, exact batch digest, participant-manifest digest and independent monotonic anchor. A release is owner-signed, idempotent and monotonic. Restoring an older owner snapshot cannot decrease the cursor/generation or reopen a closed gate. If the independent anchor or owner recovery proof is unavailable, remain closed.

COC can record and verify owner-signed attestations but cannot issue, simulate or override them. A COC `RECOVERY_EPOCH_COMPLETED` record is not an owner gate release.

## 7. JF-10 same-XID bridge — separately gated proposal

**Scope warning:** I's prior COC disposition does not approve automatic COC↔JF-10 composition. This section is a proposed, separately governed interface, not an accepted extension of the COC persistence contract. It requires fresh exact-version I acceptance and compatible D/C/Storage acceptance before implementation or conformance claims. COC does not become the JF-10 coordinator.

### 7.1 Stable participant binding before PREPARE

Before Storage PREPARE, bind one immutable tuple:
- OperationId and OperationDigest;
- ParticipantIntentRef and CausalOrderDomainRef;
- owner_boundary and exact Storage owner-final visibility-gate participant identity;
- PolicyDomainRef and applicable PermissionEpoch;
- DBIdentity and preallocated XID;
- provider idempotency identity where C is in scope;
- pre-prepare COC position and exact evidence digests.

The XID is allocated once and remains bound to that tuple. Storage's signed PreparedParticipantReceipt must identify the same XID, DBIdentity, participant, operation digest and owner boundary. Any mismatch is CONFLICT and blocks resolution.

### 7.2 I exact owner-final-gate transaction

A detached I `COMMIT_WON` token followed by an independent, unrelated Storage commit is forbidden.

The I sequenced operation MUST be the exact Storage owner-final visibility-gate participant. In one I coordinator transaction, I must bind and atomically validate/consume:
- owner_boundary and stable final-gate participant identity;
- OperationId/OperationDigest and ParticipantIntentRef;
- DBIdentity and exact preallocated XID;
- PolicyDomainRef and PermissionEpoch;
- participant digest and exact single-use CommitAuthorizationReceipt identity/digest;
- I sequencer position and terminal decision.

The resulting I-signed terminal proof references that complete immutable tuple. I alone decides COMMIT/ABORT/INDETERMINATE and owns the I sequence. A generic I terminal token, detached receipt, COC batch membership or COC position cannot authorize a later unrelated Storage commit.

Storage MUST verify the I proof against the exact prepared participant tuple before resolving. An absent, mismatched, replayed, already-consumed or unverifiable receipt/proof keeps the participant UNKNOWN/IN_DOUBT and blocks visibility.

### 7.3 Same-XID Storage resolution

- I durable COMMIT_WON for the exact owner-final-gate participant: Storage forward-commits the same DBIdentity/XID and emits the authoritative PublicationReceipt/VisibilityPointer evidence.
- I durable REVOCATION_WON / INDETERMINATE_ABORTED as defined by I's accepted terminal vocabulary: Storage rolls back the same participant/GID and emits authoritative non-publication proof. ABORT_WON is not an I terminal outcome and MUST NOT be emitted or inferred.
- I UNKNOWN/IN_DOUBT, missing terminal proof, lost ACK or mismatched tuple: retain the same prepared XID/private bytes/locks and remain blocking. Do not infer from timeout, process death, missing row, stale replica or absent ACK.
- No alternate XID, new operation identity, heuristic resolution or timeout-based terminality is permitted.
- Storage's PublicationReceipt proves Storage visibility publication only. It does not prove C provider handoff, D fence clearance or G Applied.
- C provider outcome remains separately evidenced by C; D barrier completion remains separately evidenced by D.

COC records I and Storage proofs as observations and performs later idempotent reconciliation. COC availability is not a prerequisite for Storage to follow an already durable, verified I decision. Conversely, COC cannot create an I decision or authorize Storage commit.

### 7.4 COC bridge state names are observations, not authority decisions

Use explicit observed states:
`I_TERMINAL_DECISION_OBSERVED(COMMIT_WON | REVOCATION_WON | INDETERMINATE_ABORTED)`,
`STORAGE_RESOLUTION_OBSERVED(COMMITTED | ROLLED_BACK)`,
`C_PROVIDER_OUTCOME_OBSERVED(...)`,
and `D_LINEAGE_CLEARANCE_OBSERVED(...)`.

Every transition carries the issuing owner's signed evidence ref/digest. Bare COC states named `COMMIT_WON`, `ABORT_WON` or `STORAGE_RESOLVED` MUST NOT be interpreted as COC-owned decisions. Terminalization requires the complete applicable typed evidence set; no aggregate state may synthesize missing owner facts.

Multi-PolicyDomain JF-10 remains unsupported/blocked absent a separate I-approved atomic authorization profile.

### 7.5 PostgreSQL prepared-participant identity mapping — Storage clarification

The engine-neutral `preallocated XID` MUST be distinguished from an engine-assigned native transaction number. For the PostgreSQL 18.7 candidate profile:

1. `PreparedParticipantRef` is the stable cross-service participant identity.
2. `PreparedTransactionGID` is the client-chosen PostgreSQL prepared-transaction GID. Storage allocates and durably binds this unique GID to the immutable `PublicationOperationId` / `RequestDigest` before `JF10_PREPARE_INTENT_REGISTERED`. This is the preallocated identifier carried in the COC prepare-intent record and reused for every lookup, retry, `COMMIT PREPARED` and `ROLLBACK PREPARED`.
3. PostgreSQL's numeric `pg_prepared_xacts.transaction` value is an engine-assigned native XID allocated by PostgreSQL; the client cannot preallocate it. It MUST NOT be described as the preallocated cross-service XID or used as the sole participant identity. Storage records it as observed engine evidence after PREPARE.
4. `PreparedParticipantReceipt` MUST bind at least: `PreparedParticipantRef`; `PreparedTransactionGID`; native XID as observed; `CanonicalAuthorityDBRef`; PostgreSQL cluster `system_identifier`; target database identity/OID; original prepare timeline and observed prepare LSN; participant digest; `PublicationOperationId` and `RequestDigest`; exact `owner_boundary`; `CausalOrderDomainRef` and `PolicyDomainRef`; COC prepare-intent position/digest; prepared state; Storage signer/key version and audience.
5. The GID MUST be unique within the bound PostgreSQL cluster/database authority and MUST NOT be reassigned to a different operation after resolution. A same-GID/same-digest retry is lookup/replay; a same-GID/different-tuple request is `CONFLICT`.
6. After a durable I terminal decision, `StorageResolutionProof` MUST bind the same GID and original participant tuple to the final `COMMITTED` or `ROLLED_BACK` state. On commit it includes the exact VisibilityPointer/PublicationReceipt transaction identity and receipt digest; on rollback it includes authoritative non-publication evidence. It also records recovery timeline/LSN context without replacing the original prepare identity.
7. Absence of a GID from `pg_prepared_xacts` is not, by itself, proof of commit or rollback. Storage MUST resolve through the durable participant outcome/idempotency ledger and authoritative DB readback. If those disagree or are unavailable, the result remains `UNKNOWN` / `IN_DOUBT` and protected reads stay closed.

This clarification preserves the protocol's engine-neutral intent while making the PostgreSQL mapping implementable. Other database engines MUST define an equivalent stable prepared-participant identifier and separately typed engine-native transaction identifier. Exact field names and wire encoding require H review; the security tuple and same-participant recovery invariant are normative.

## 8. Snapshot, compaction and restore anti-rollback

A checkpoint contains quorum-certified epoch/index/root, committed membership/configuration history, snapshot digest, previous checkpoint, complete participant projection, unresolved manifest, cutoff batches, participant manifests, owner gate refs/high-waters, reconciliation root, key-status evidence and archive proof.

Rules:
1. Snapshot only at a quorum-committed index; never treat leader memory or uncommitted suffix as authoritative.
2. Retain and verify the complete post-checkpoint log suffix and digest continuity.
3. Do not compact unresolved participants, gate evidence or proof needed to establish terminality.
4. Restore compares against the newest independently retained monotonic checkpoint/high-water anchor. Missing, stale, rolled-back or unverifiable anchor => RESTORE_FENCED.
5. Rebuild projections from the verified log. Projection mismatch is repairable; missing authoritative prefix is not.
6. Reconcile every owner-local pending gate and every participant at/before the restored cutoff before any reader, submit, reservation or barrier is reopened.
7. Owner-local gate generations/cursors require their own independently retained monotonic anchors; a COC checkpoint cannot substitute for I/D owner anti-rollback proof.
8. Archive replacement, checkpoint rollback, membership change and key compromise recovery require separated privileged roles, two-person approval and immutable audit. No privileged action can erase unresolved evidence.

## 9. Failure matrix

| Failure | Required behavior |
|---|---|
| Leader dies before batch quorum commit | No committed batch; remain fenced; retry same batch identity |
| Batch commits, manifest record not yet committed | Remain fenced; same-key lookup and commit/verify same manifest identity |
| Batch or manifest ACK lost | Linearizable lookup by same identity/digest; never mint replacement |
| Manifest count/root/prefix/batch digest mismatch | RESTORE_FENCED; no owner release or serving |
| I/D request races owner snapshot | Atomic gate/snapshot assigns it to captured set or later set; gate stays closed |
| Request arrives after captured high-water | Remains gated; later batch or authoritative proof of out-of-scope |
| D lineage unknown or incomplete | D barrier remains open; no effective Forget |
| C provider invocation outcome ambiguous | Same provider key lookup; IN_DOUBT if no authoritative proof; no blind resubmit |
| COC unavailable before new protected provider submit | C fails closed; no new provider call |
| Storage prepared XID cannot be authoritatively read | IN_DOUBT; retain same XID/locks/private bytes |
| I exact owner-final-gate proof missing/mismatched | No Storage commit; same XID remains blocking |
| I COMMIT proof durable, COC unavailable | Storage follows exact same-XID decision; COC observation can reconcile later |
| Stale owner snapshot attempts gate reopen | Reject via owner monotonic anchor; remain closed |
| Snapshot behind independent anchor | RESTORE_FENCED |
| Same identity, changed digest | CONFLICT; preserve evidence; no transition |
| Unknown critical record/schema family | Fail closed; no downgrade or silent field dropping |

## 10. Wire/schema requirements and owner boundary

H owns the normative BMCP wire schema and version negotiation; Storage does not claim to publish or freeze H's schema. A versioned H schema MUST model these distinct message families, not overload Applied ACK:
- `OWNER_LOCAL_PENDING_GATE`
- `COC_RECOVERY_CUTOFF_BATCH`
- `PARTICIPANT_SET_RECONCILIATION`
- `OWNER_LOCAL_GATE_RELEASE`
- `COC_RESTORE_FENCED`

The schema contract must define exact field names, types and requiredness for prefix P/root, owner attestations/high-waters/gate generations, batch identity/position/digest, manifest ID/digest/count/retrieval reference, canonical set ordering, explicit empty-array semantics, owner signature references and error/outcome envelopes. A manifest receiver rejects any prefix, batch digest, owner high-water or manifest digest mismatch. Unknown critical types fail closed; version negotiation must prevent downgrade that drops required recovery fields.

The JF-10 bridge schema candidate remains separate and non-frozen. It requires cross-field semantic validators: all XID references share DB identity/participant/operation digest/owner boundary; COMMITTED requires PublicationReceipt and VisibilityPointer and forbids non-publication proof; ROLLED_BACK requires authoritative non-publication proof and forbids PublicationReceipt/VisibilityPointer; I decision must bind the exact prepared final-gate participant; UNKNOWN/PENDING cannot be coerced terminal; typed positions remain opaque.

## 11. Security profile and explicit freeze blockers

The following are mandatory design outputs but remain **OPEN / NOT FROZEN** in this proposal:
- canonical serialization profile, canonicalization profile ID and domain-separated digest suite;
- signature algorithms, issuer/audience semantics, key custody, key lifecycle, rotation/revocation propagation, compromise recovery and historical verification policy;
- consensus membership/configuration proof and leader term/commit proof binding;
- independent monotonic anti-rollback anchors for COC checkpoints and I/D owner gates;
- threat model and controls for compromised owner keys, replay across recovery epochs, leader rollback/term reuse, malicious checkpoint restore and privileged archive replacement;
- retention/archive integrity, privacy/data residency, RPO/RTO and production topology;
- provider-specific idempotency and authoritative lookup capability for each C adapter.

These are acceptable as open decisions in an architecture proposal, but they block contract freeze, implementation conformance claims and production deployment until accountable owners approve exact versions. I/Security owns cryptographic governance; H owns schema/wire definition; C owns provider adapter evidence; D and I own their respective gate attestations; A owns cross-owner integration acceptance.

## 12. Required verification scenarios (not claimed as run)

The following are acceptance-test requirements only; no PASS is claimed:
- RCB-01: precompute complete manifest at exact P; batch binds digest/count/high-water; post-batch manifest record matches byte-for-byte digest.
- RCB-02: crash between batch and manifest commits; next leader stays fenced and resumes same identities.
- RCB-03: batch ACK lost; same-key linearizable lookup returns exact batch.
- RCB-04: participant omission, duplicate, root mismatch or stale projection => RESTORE_FENCED.
- RCB-05: I/D request races atomic owner snapshot; each request is in captured or later set, never omitted.
- RCB-06: request after high-water remains gated until subsequent batch or authoritative out-of-scope proof.
- GATE-01: I gate release is I-signed, exact-batch/manifest-bound, monotonic and does not mint authorization.
- GATE-02: D per-fence lineage manifest complete; unknown lineage blocks; outage-gate release does not make Forget effective.
- GATE-03: stale I/D owner snapshot cannot decrease cursor/generation or reopen gate.
- C-01: COC unavailable before protected reservation/provider invocation => no new provider call.
- C-02: provider boundary crossed then response/ACK lost => same provider key lookup, no new identity or blind resubmit.
- C-03: provider ambiguous participant appears in manifest and remains IN_DOUBT until authoritative evidence.
- C-04: provider idempotency namespace/retention/lookup mismatch => fail closed.
- JF10-01: I sequenced operation atomically binds exact Storage final-gate participant, owner boundary, XID/DB, operation tuple, PolicyDomain/PermissionEpoch and single-use receipt.
- JF10-02: detached COMMIT token cannot authorize unrelated Storage commit.
- JF10-03: I COMMIT_WON forward commits same XID; accepted abort terminal rolls back same XID.
- JF10-04: UNKNOWN/lost ACK/mismatched proof retains same XID and locks.
- JF10-05: PublicationReceipt, provider outcome, D barrier and G Applied remain separate evidence.
- WIRE-01: schema rejects missing owner completeness attestations, wrong prefix/root, duplicate refs, unbound manifest, COC-issued gate release and downgrade dropping fields.
- SEC-01: signature/key status, membership/configuration, restore anti-rollback and owner gate anti-rollback checks fail closed.

## 13. Five-review disposition matrix

The exact Owner review source pins are:

| Owner | Acceptance artifact | Branch | Review artifact Blob |
|---|---|---|---|
| A | `reviews/integration/phase-3.6.3-a-coc-durable-protocol-integration-acceptance.md` | `session-a-integration-2026-11-16` | `d20d08581fd8606a1adf0400bf5dcb24004a9611` |
| I | `09-security-governance/phase-3.6.3-i-coc-durable-protocol-authority-acceptance.md` | `session-i-security-governance-2026-11-16` | `528945f82e3e25258052240a7a4ba43753ae6cf8` |
| D | `03-memory-brain/phase-3.6.3-d-coc-durable-protocol-acceptance.md` | `session-d-memory-brain-2026-11-16` | `e2a74d138ccebfb4266d19ea0c0c03f58a815bf5` |
| C | `07-agent-integration/phase-3.6.3-c-coc-durable-protocol-acceptance.md` | `session-c-agent-integration-2026-11-16` | `8c8a43f99ecd5986f802fb81ddfa5fd942cef0ae` |
| H | `08-bmcp-protocol/phase-3.6.3-h-coc-durable-protocol-wire-acceptance.md` | `session-h-bmcp-protocol` | `5dfc7ae56b2ae7351d6c2c108f7be3249125f6c3` |

All five acceptance artifacts pin the same reviewed Storage baseline Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`. The separate earlier Storage draft Blob `cd5566b3d99b5204401ac713a5bb2dcf89a02726` is retained as predecessor history only.

| Review | Original finding | v2 response | Status |
|---|---|---|---|
| A | Batch committed before participant enumeration | §5.3–5.4 precomputes deterministic manifest and binds it into batch; separate committed manifest cross-binds batch digest | Addressed in proposal; A re-review required |
| A | Detached I COMMIT and ambiguous COC state names | §7.2–7.4 exact I final-gate participant binding and explicit observed states | Addressed in proposal; I re-review required |
| A | Missing C local side-effect gate | §6.3 explicit C fail-closed admission and in-flight participant reconciliation | Addressed in proposal; C re-review required |
| I | JF-10 composition not approved by prior COC disposition | §7 explicitly labels bridge separately gated and requires fresh exact I acceptance | Addressed as scope restriction; I re-review required |
| I | Exact owner-final-gate transaction missing | §7.2 specifies atomic I binding/consumption tuple | Addressed in proposal; I re-review required |
| I | Batch completeness and security/anti-rollback freeze gaps | §5, §6.4, §8, §11 define protocol requirements; cryptographic/anchor selections remain open and explicitly block freeze | Partially addressed; I/security approval required |
| D | Batch-bound participant manifest | §5.3–5.4 | Addressed in proposal; D re-review required |
| D | Per-fence affected-lineage completeness | §6.2 requires D-owned per-fence membership manifest and unknown-lineage blocking | Addressed in proposal; D re-review required |
| D | Concurrent/delayed request and gate release race | §5.2, §5.6, §6.2, §6.4 | Addressed in proposal; D re-review required |
| C | C fail-closed admission | §6.3 | Addressed in proposal; C re-review required |
| C | Complete provider state inventory | §5.3, §6.3 and §12 | Addressed in proposal; C re-review required |
| C | Provider-specific idempotency/lookup proof | §6.3 and §11 | Defined as per-adapter production blocker; C evidence required |
| C | C outcome distinct from Storage | §§2, 6.3, 7.3–7.4 | Addressed in proposal; C re-review required |
| H | Recovery batch/gate wire families absent | §10 defines required distinct schema families and required field classes; H must publish schema | Storage-side contract supplied; H schema delivery pending |
| H | Batch/manifest identity ambiguity | §5.4 and §10 | Addressed in proposal; H re-review required |
| H | Envelope/canonicalization/security schema gaps | §§3.1, 10–11 | Requirements enumerated; exact H/I schema/security profile remains open |
| H | Error/lost ACK semantics | §4.3 and §5.4 | Addressed in proposal; H re-review required |

## 13.1 Additional A exact-version review R1–R6 disposition

This is a subsequent review gate, distinct from the five earlier A/I/D/C/H acceptance artifacts above. A reviewed its exact COC bundle and published **ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED**. The v2 amendment addressed the findings as follows; this v3 does not claim A has accepted v3:

| Finding | v2 disposition | Normative location / remaining condition |
|---|---|---|
| R1 Recovery Cutoff Batch completeness | Addressed by owner high-water attestations, explicit empty manifest, exact prefix-bound participant manifest, batch/manifest cross-binding, and subsequent batch for post-high-water requests | §§5.2–5.6; each Owner must verify its own request set and gate disposition |
| R2 Owner-local Gate linearization | Addressed by atomic owner gate closure + local snapshot/high-water capture; racing requests are either captured or remain behind the closed gate | §§5.2, 5.6, 6.1–6.4; Owner implementation proof remains required |
| R3 Participant completeness and gate release | Addressed by immutable retrievable manifest, per-fence D lineage manifest, owner-signed independent releases and separate outage-gate / effective-fence states | §§5.3–5.5, 6.1–6.4 |
| R4 C provider invocation | Explicitly requires exact I `COMMIT_WON` plus all required D predicates; abort outcomes prohibit provider invocation; pre-provider reservation is non-side-effecting | §6.3; C must provide provider-specific same-key lookup/idempotency evidence |
| R5 Same-XID recovery | Exact DB identity/GID/XID tuple remains immutable; I COMMIT_WON forward-commits same participant; abort rolls back same participant; UNKNOWN retains prepared state; no alternate identity or heuristic resolution | §§7.1–7.5; selected-engine conformance remains required |
| R6 Exact-version/schema drift | Five review source pins and later A bundle are distinguished; H must bind recovery schema applicability to exact A §11/§12 and reject downgrade/field omission | Header, §§10, 13; H schema remains candidate and requires exact-version H review |


## 14. Acceptance and release boundary

This v3 is a Storage technical proposal, not a joint acceptance. All five Owners must independently review this exact v2 commit/blob. Earlier v1 decisions do not carry forward automatically.

Required next decisions:
- A: integration acceptance of batch/manifest ordering, C gate, state semantics and cross-owner boundaries.
- I: exact I gate proof, security/anti-rollback profile, and separate JF-10 composition acceptance or rejection.
- D: per-fence lineage completeness, D gate release and effective-Fence separation.
- C: provider side-effect inventory, fail-closed gate and provider-specific same-key recovery.
- H: versioned BMCP schema, canonical wire fields, requiredness, compatibility and error envelopes.
- Storage: maintain exact-XID/DB identity, prepared participant, publication and non-publication proof boundaries.

**Disposition:** v3 revised proposal published for fresh exact-version review. No joint acceptance, protocol freeze, implementation, deployment, conformance PASS, production readiness or production activation is claimed. Gate B/C and JF-10 remain blocked until their existing prerequisites and owner decisions are satisfied.


## 15. Prepared participant identity and receipt contract — v3 normative amendment

This section is the Storage-owned normative amendment for the prepared-participant lifecycle. It applies to PostgreSQL 18.x adapter behavior described in §7 and the BMCP proof references in §10. It does not make PostgreSQL identifiers universal across storage engines.

### 15.1 Nominal identity types

The following are distinct, non-coercible nominal types. A serializer MUST preserve the type tag; application code MUST NOT cast between them based on equal textual or numeric values.

| Type | Meaning | Constraints |
|---|---|---|
| `PreparedParticipantRef` | Stable cross-service identity for one prepared participant lifecycle | Opaque, globally unique, never reused |
| `PreparedTransactionGID` | PostgreSQL client-chosen prepared-transaction locator | Adapter-scoped validated string; exact byte/case preservation; never treated as native XID |
| `PostgreSQLNativeXID` | PostgreSQL engine-assigned native transaction identifier observed for the prepared transaction | Adapter-specific unsigned numeric representation; never client-selected |
| `CanonicalAuthorityDBRef` | Canonical Storage authority/database reference | Opaque registry-issued reference |
| `DatabaseIncarnationRef` | Governed identity for one logical database incarnation under one canonical Storage authority | Globally unique, non-reusable; survives ordinary restart/failover of that same incarnation; clone/re-provision creates a new value unless an explicit authorized migration preserves identity |
| `PostgreSQLSystemIdentifier` | PostgreSQL cluster system identifier | Separate from authority and incarnation references |
| `PostgreSQLDatabaseOID` | Database-local PostgreSQL OID | Never treated as globally stable identity |
| `PostgreSQLTimeline` | PostgreSQL timeline identifier | Separate nominal integer type |
| `PostgreSQLLSN` | PostgreSQL log sequence number | Canonical uppercase hexadecimal PostgreSQL LSN string; never a generic integer |
| `PublicationOperationId` | Stable publication operation identity | Opaque, immutable |
| `RequestDigest` | Digest of canonical request bytes | Algorithm/profile-tagged |
| `ParticipantTupleDigest` | Digest of the complete immutable participant tuple | Algorithm/profile-tagged |
| `COCPosition`, `IPolicyPosition`, `DForgetGeneration` | Authority-local positions/generations | Mutually incomparable; no global sorting |

A generic field named `xid` is prohibited. Other database engines MUST define their own tagged locator and native transaction-ID types.

### 15.2 Database incarnation registry contract

`DatabaseIncarnationRef` MUST be minted by the canonical Storage authority registry before a participant can be prepared. The registry record binds:
- CanonicalAuthorityDBRef;
- DatabaseIncarnationRef;
- engine and adapter profile/version;
- PostgreSQLSystemIdentifier (where applicable);
- PostgreSQLDatabaseOID and database name as observed metadata;
- creation/activation authority and registry generation;
- predecessor/successor incarnation references for authorized migration;
- clone/restore/re-provision classification;
- anti-rollback anchor reference and registry record digest.

Rules:
1. Ordinary process restart, primary failover and timeline promotion within the same governed database incarnation do not by themselves mint a new DatabaseIncarnationRef.
2. Physical clone, independent restore, database copy, re-provision or authority migration MUST default to a new DatabaseIncarnationRef.
3. Preserving an incarnation across migration requires a separately authorized, auditable migration record binding old and new infrastructure identities, cutover boundary, source checkpoint, target verification, authority approvals and anti-rollback evidence. No automatic inference from matching system_identifier/OID/name is permitted.
4. A prepared GID found in another DatabaseIncarnationRef MUST NOT resolve the original participant.
5. Lookup key is the exact tuple `(CanonicalAuthorityDBRef, DatabaseIncarnationRef, PreparedParticipantRef, PreparedTransactionGID)`. GID-only lookup is forbidden for authoritative resolution.
6. Registry rollback, missing registry proof or conflicting incarnation evidence yields UNKNOWN and keeps the participant private/fenced.

### 15.3 Immutable prepare-attempt and participant ledger

Before issuing PREPARE, Storage MUST durably allocate and commit:
- `PreparedParticipantRef`;
- `PrepareAttemptRef`;
- strictly monotonic `PrepareAttemptGeneration` scoped to the participant;
- `ParticipantLedgerRef`;
- `ParticipantLedgerVersion`;
- complete immutable operation tuple and its `ParticipantTupleDigest`;
- COC prepare-intent identity, position and digest;
- exact DB authority and DatabaseIncarnationRef;
- GID reservation and idempotency identity.

The participant tuple MUST bind at least:
`PublicationOperationId`, RequestDigest, PreparedParticipantRef, PrepareAttemptRef, PrepareAttemptGeneration, PreparedTransactionGID, CanonicalAuthorityDBRef, DatabaseIncarnationRef, PostgreSQLSystemIdentifier, PostgreSQLDatabaseOID, owner boundary, CausalOrderDomainRef, PolicyDomainRef, COC prepare-intent position/digest and the participant-ledger identity/version.

Replay rules:
- Same participant + same attempt generation + same complete canonical tuple: idempotent lookup/replay; return the original evidence.
- Same participant/attempt identity with any changed tuple field or digest: immutable CONFLICT.
- New attempt generation: allowed only after the previous attempt has an authoritative append-only terminal attempt record and a new COC prepare-intent binding. A new generation MUST NOT inherit or reuse the prior attempt's receipt.
- An aborted/failed attempt remains in the ledger forever as audit evidence; it is never overwritten or erased.
- Same GID under a different participant, attempt, DB incarnation or tuple is CONFLICT. GID reuse is prohibited for the lifetime of the database incarnation and the configured retention/archive horizon; the adapter profile MUST define the stronger of engine constraints and policy retention.

### 15.4 PreparedParticipantReceipt issuance preconditions

A Storage `PreparedParticipantReceipt` is evidence that one exact participant is prepared and retained privately. It is not authorization, COC commit, Forget clearance or publication visibility.

Storage MAY issue the receipt only after all of the following:
1. The immutable participant tuple, attempt generation and GID reservation are durably committed in the participant ledger.
2. The matching COC prepare-intent record is quorum committed and linearly read back by exact identity/digest.
3. PostgreSQL PREPARE TRANSACTION completed on the authoritative writable primary.
4. Storage performs an authoritative readback from that primary's `pg_prepared_xacts` and matches exact GID, database identity and observed native XID.
5. The readback is bound to the same DatabaseIncarnationRef and participant-ledger version.
6. The participant remains private: no VisibilityPointer or PublicationReceipt is visible to authoritative readers.
7. The signed receipt is durably persisted and its receipt identity/digest is recorded in the participant ledger before it is returned.

A command ACK, client response, driver success, standby-only observation, COC log record, stale replica read or absence/presence inferred from a cache is insufficient. If readback is unavailable, contradictory or not bound to the exact primary/incarnation, no PREPARED receipt is issued. State remains UNKNOWN/IN_DOUBT, locks/private data are retained, and no protected read is served.

### 15.5 PreparedParticipantReceipt candidate field contract

The following logical fields are required. This is a typed semantic contract; exact wire spelling/serialization is H-owned and the signed-envelope profile is I/H joint-owned.

| Logical field | Type | Required | Semantics |
|---|---|---:|---|
| message_type | MessageType | yes | Fixed value `Storage.PreparedParticipantReceipt` |
| schema_version | SchemaVersion | yes | Exact major/minor schema |
| issuer | AuthorityPrincipalRef | yes | Storage signing principal |
| subject | PreparedParticipantRef | yes | Exact participant |
| owner_authority | OwnerAuthorityRef | yes | Storage authority |
| audience | AudienceRef | yes | Exact verifier/service audience |
| purpose | MessagePurpose | yes | Fixed receipt purpose |
| key_id / key_version | KeyRef / KeyVersion | yes | Signer key identity/version |
| algorithm_profile | SignatureProfileRef | yes | I-approved profile identifier |
| canonicalization_profile | CanonicalizationProfileRef | yes | I/H-frozen profile identifier |
| digest_profile | DigestProfileRef | yes | I/H-frozen digest profile |
| prepared_participant_ref | PreparedParticipantRef | yes | Same as subject |
| prepared_transaction_gid | PreparedTransactionGID | yes | Exact PostgreSQL GID |
| postgresql_native_xid | PostgreSQLNativeXID | yes | Authoritatively observed engine XID |
| canonical_authority_db_ref | CanonicalAuthorityDBRef | yes | Canonical Storage authority |
| database_incarnation_ref | DatabaseIncarnationRef | yes | Non-reusable incarnation |
| postgresql_system_identifier | PostgreSQLSystemIdentifier | yes | Cluster identity evidence |
| postgresql_database_oid | PostgreSQLDatabaseOID | yes | Database-local identity evidence |
| original_prepare_timeline | PostgreSQLTimeline | yes | Immutable original prepare timeline |
| original_prepare_lsn | PostgreSQLLSN | yes | Immutable original prepare LSN |
| publication_operation_id | PublicationOperationId | yes | Exact operation |
| request_digest | RequestDigest | yes | Exact request |
| participant_tuple_digest | ParticipantTupleDigest | yes | Complete tuple digest |
| owner_boundary | OwnerBoundaryRef | yes | Exact Storage owner boundary |
| causal_order_domain_ref | CausalOrderDomainRef | yes | COC causal domain |
| policy_domain_ref | PolicyDomainRef | yes | I policy domain reference; not I authorization |
| coc_prepare_intent_position | COCPosition | yes | Exact quorum-committed intent position |
| coc_prepare_intent_digest | EntryDigest | yes | Exact intent record digest |
| prepare_attempt_ref | PrepareAttemptRef | yes | Exact attempt |
| prepare_attempt_generation | PrepareAttemptGeneration | yes | Exact monotonic generation |
| participant_ledger_ref | ParticipantLedgerRef | yes | Durable Storage ledger identity |
| participant_ledger_version | ParticipantLedgerVersion | yes | Exact durable version |
| prepared_state | PreparedState | yes | Fixed value PREPARED |
| prepared_observation_source | ObservationSource | yes | Authoritative writable-primary readback |
| prepared_observed_at | TrustedAuditTimestamp | yes | Audit metadata only; not causal order |
| payload_digest | PayloadDigest | yes | Digest of complete canonical payload |
| signature_envelope | SignatureEnvelope | yes | I/H-approved protected envelope |

No required field may be null or empty. Optional extension fields MUST be namespaced, explicitly declared non-critical or critical, and covered by schema-version rules. Unknown critical fields fail closed. The timestamp is not used to order, authorize or resolve a participant.

### 15.6 StorageResolutionProof and append-only recovery observations

A StorageResolutionProof MUST bind the same immutable tuple as the receipt, including participant ref, GID, native XID, authority DB ref, DatabaseIncarnationRef, cluster/database evidence, operation/request/tuple digests, owner boundary, COC prepare-intent identity, attempt generation and participant-ledger version.

It additionally contains:
- message type/schema and the same protected envelope fields;
- outcome enum exactly one of COMMITTED, ROLLED_BACK, UNKNOWN;
- original prepare timeline/LSN copied unchanged from the receipt;
- durable participant outcome-ledger reference/version;
- authoritative source role and evidence references;
- for COMMITTED: exact same-GID resolution evidence, VisibilityPointer transaction identity, PublicationReceipt identity/digest and atomic publication transaction reference;
- for ROLLED_BACK: exact same-GID rollback evidence and authoritative non-publication proof showing no VisibilityPointer/PublicationReceipt became visible;
- for UNKNOWN: unresolved reason class and retained prepared-state/lock evidence where available;
- append-only RecoveryObservation[] entries.

Each RecoveryObservation contains RecoveryEpoch, observed DatabaseIncarnationRef, PostgreSQLSystemIdentifier, PostgreSQLTimeline, PostgreSQLLSN, source role, observation timestamp (audit only), evidence reference and digest. New timeline/LSN observations append; they MUST NOT mutate original_prepare_timeline or original_prepare_lsn.

Cross-field validation:
- COMMITTED requires a VisibilityPointer and PublicationReceipt bound to the exact same participant tuple and atomic transaction identity; it MUST NOT carry a contradictory rollback proof.
- ROLLED_BACK requires authoritative non-publication proof; it MUST NOT carry a VisibilityPointer or PublicationReceipt.
- UNKNOWN cannot be coerced to either terminal outcome and cannot release the participant gate.
- Absence from pg_prepared_xacts is never, by itself, COMMIT or ROLLBACK evidence.
- If authoritative sources disagree, the outcome is UNKNOWN/IN_DOUBT.

### 15.7 Exact I terminal proof join — Storage acceptance rule

Before Storage commits a prepared participant, it MUST validate an I-authoritative terminal proof that binds:
- exact CommitAuthorizationReceiptRef and digest;
- one-time receipt-consumption identity;
- PreparedParticipantRef and PreparedTransactionGID;
- CanonicalAuthorityDBRef and DatabaseIncarnationRef;
- PublicationOperationId, RequestDigest and ParticipantTupleDigest;
- owner boundary, PolicyDomainRef and PermissionEpoch;
- I sequencer position and terminal decision;
- exact Storage final-gate participant identity;
- PrepareAttemptRef and PrepareAttemptGeneration;
- ParticipantLedgerRef and ParticipantLedgerVersion;
- PreparedParticipantReceiptRef and the exact signed receipt payload digest;
- the complete ParticipantTupleDigest.

The I proof must demonstrate that authorization validation, current PermissionEpoch/key-status check, one-time receipt consumption, exact participant binding and terminal decision were atomically persisted in I's own authoritative transaction. A detached token, COC projection, Storage receipt or transport ACK is insufficient.

Storage accepts only an I terminal decision whose outcome explicitly permits the same participant to proceed. A terminal abort requires rollback of that same GID/participant. UNKNOWN, missing proof, replay, mismatch or unverifiable I signature keeps the same prepared participant private and blocked. Storage MUST NOT allocate a replacement participant or GID to escape uncertainty.

This section specifies what Storage requires; I owns and must define the proof's issuance/consumption transaction and its security semantics.

## 16. Signed envelope, canonical bytes and trust boundary — owner split

### 16.1 Protected envelope semantic requirements

Every signed Storage receipt/proof and every signed owner attestation MUST expose a protected envelope with at least:
- PayloadType, SchemaVersion;
- IssuerPrincipalRef, SubjectRef, OwnerAuthorityRef;
- AudienceRef, Purpose;
- KeyId, KeyVersion, AlgorithmProfileRef;
- CanonicalizationProfileRef, DigestProfileRef;
- PayloadDigest;
- Signature bytes;
- trust-status evidence reference where required by I policy.

The signature MUST cover a domain-separated byte sequence that unambiguously binds the protected header and the complete canonical payload. A digest or mutable object reference without a normative preimage construction is insufficient.

### 16.2 I-owned security policy decisions (not selected by Storage)

I MUST select and publish:
- permitted signature algorithm suite and parameter constraints;
- key generation, custody, activation, rotation, suspension, revocation, compromise, retirement, destruction, recovery and dual-control policy;
- trust-root identity and issuer/subject authorization rules;
- audience/environment/purpose allowlists;
- historical verification policy distinguishing mathematical signature validity from key authorization at signing time;
- revocation effective-time and compromise backdating rules;
- trusted time/append-only key-status evidence sources and retention;
- anti-rollback anchors for key status, receipt consumption and PermissionEpoch;
- behavior when historical key-status evidence is unavailable (default UNKNOWN/fail closed).

A later revocation MUST NOT silently rewrite history. A compromise believed effective before signing may invalidate the receipt according to I's published policy. Missing historical status evidence MUST NOT be treated as valid by default.

### 16.3 H-owned wire and canonicalization decisions (not selected by Storage)

H MUST publish:
- exact field names, nominal type encodings, requiredness and nullability;
- serialization format and deterministic canonicalization rules;
- UTF-8/Unicode normalization or rejection behavior;
- duplicate-key rejection;
- integer, decimal, hex, timestamp and byte-string encodings and bounds;
- absent-versus-null semantics;
- unknown-critical-field and extension behavior;
- schema evolution/version negotiation and downgrade rejection;
- exact signature preimage construction implementing I's approved profile;
- positive and negative interoperability fixtures.

### 16.4 I/H joint freeze gate

No signature or wire profile is frozen until:
1. I approves the trust and cryptographic policy;
2. H publishes the exact schema/canonical byte contract implementing that policy;
3. both bind the same immutable profile identifiers and version;
4. positive/negative fixtures verify cross-implementation identical canonical bytes, digest and signature input;
5. A confirms integration composition and no authority conflation;
6. Storage confirms its adapter receipt/proof fields conform without weakening fail-closed semantics.

Until then, the envelope above is a semantic candidate contract only. No algorithm, key provider, canonicalization scheme or wire encoding is selected by this Storage document.

## 17. Required negative and positive conformance vectors

Before implementation/conformance acceptance, the owning engineering and protocol teams MUST provide fixtures covering at least:
1. exact same tuple and same attempt replay returns original receipt/position;
2. same participant with changed tuple or attempt generation returns immutable CONFLICT;
3. same GID under another DatabaseIncarnationRef cannot resolve;
4. matching system_identifier/OID/name without matching governed incarnation is insufficient;
5. PREPARE command ACK without authoritative pg_prepared_xacts readback cannot issue receipt;
6. authoritative readback with mismatched GID/database/native XID fails closed;
7. native XID cannot be parsed into PreparedTransactionGID and vice versa;
8. timeline change appends RecoveryObservation and preserves original prepare coordinates;
9. COMMITTED proof without matching VisibilityPointer + PublicationReceipt is rejected;
10. ROLLED_BACK proof carrying publication evidence is rejected;
11. UNKNOWN cannot release gate or become terminal through timeout/absence;
12. wrong issuer/subject/audience/purpose/environment is rejected;
13. signature preimage changes when any protected tuple field changes;
14. duplicate keys, invalid Unicode, noncanonical numeric form and absent/null ambiguity are rejected per frozen H profile;
15. revoked/compromised key and missing historical key-status evidence follow I policy and fail closed when unverifiable;
16. receipt replay across COC epoch, recovery epoch, attempt generation or participant is rejected;
17. restored snapshot cannot resurrect consumed authorization receipt or stale key status;
18. unknown critical field or downgrade that omits a required field is rejected.

## 18. v3 disposition and owner re-review requirements

This v3 incorporates the coordinator-prepared A/I/H role-review findings as Storage amendments. It does not claim that those simulated reviews are independent owner signatures or that A/I/H have accepted v3.

Exact review target for the next round is the immutable v3 commit/blob only. Required independent owner decisions:
- A: verify DatabaseIncarnationRef lifecycle, attempt/ledger replay semantics, authoritative PREPARED evidence, recovery-coordinate separation and exact I-to-Storage final-gate join.
- I: publish the authoritative signed envelope trust policy, key lifecycle/historical verification, anti-rollback and atomic receipt-consumption proof schema.
- H: publish exact strict wire schema, canonicalization/profile binding, validators and interoperability vectors.
- D/C: re-review only where the v3 amendments affect their Forget/provider side-effect gates; prior acceptance cannot be presumed to cover changed fields.
- Storage: verify exact PostgreSQL adapter mapping and participant-ledger invariants.

**Status:** Storage v3 technical proposal — fresh exact-version review required. No joint contract freeze, cryptographic profile freeze, wire-schema freeze, implementation/conformance PASS, deployment, production readiness or production activation is claimed. JF-10 P0 remains OPEN until the accountable Owner decisions and required evidence close.


## 19. v3.1 exact-owner findings and normative reconciliation (2026-11-17)

This v3.1 amendment responds to the exact-Blob v3 reviews by I, H and B. It also reconciles the companion PostgreSQL §14 source contract to this document's §§15.1–15.7. It does not treat prior v3 or §14 acceptance as acceptance of v3.1.

### 19.1 Closed Storage drafting conflicts

1. The I terminal vocabulary is exactly `COMMIT_WON`, `REVOCATION_WON`, `INDETERMINATE_ABORTED`, plus nonterminal `UNKNOWN/IN_DOUBT`. `ABORT_WON` is prohibited. Storage outcome remains a separate enum: `COMMITTED`, `ROLLED_BACK`, `UNKNOWN`.
2. I terminal proof now binds the exact prepare attempt/generation, participant-ledger ref/version, PreparedParticipantReceipt ref/digest and complete ParticipantTupleDigest in addition to the exact final-gate participant and one-time authorization receipt consumption.
3. I recovery-gate close is specified as one I-sequencer serialization transaction; receipt issue/consume races must resolve in that same transaction order. Gate release requires a second current high-water/scope-generation check and a new batch/manifest if either advances.
4. The companion §14 source now contains the same DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, ParticipantTupleDigest and authoritative PREPARED readback requirements as §§15.1–15.7. The earlier abbreviated §14 tuple is superseded.

### 19.2 Remaining cross-owner blockers (not silently waived)

- **I:** must confirm the exact v3.1 I-gate serialization/release clauses and publish its final security policy for issuer/subject/audience/purpose, key lifecycle, historical verification, compromise/revocation and independent anti-rollback. The proposed domain-separated signature input remains a candidate, not a selected profile.
- **H:** must reconcile the exact schema with the full §15 tuple and publish schemas for Recovery Cutoff Batch, Participant Manifest, owner pending/release attestations and RecoveryEpoch completion; cross-message validators must bind envelope subject, receipt digest, attempt/ledger, DB incarnation and tuple digest. H must explicitly map the current A §11/§12 package and all required C/G/H Applied evidence families.
- **B:** must confirm the v3.1 type names and PostgreSQLNativeXID versus EngineNativeTransactionXIDRef mapping against its amended registry.
- **A:** must verify end-to-end ordering, exact I terminal participant binding, batch/manifest crash ordering and all cross-owner exact-blob dependencies.
- **D/C/E/G:** earlier acceptance of the §14 source Blob does not automatically accept v3.1. Each must confirm whether these clarified fields alter its owner boundary and pin this exact v3.1 Blob.

### 19.3 Evidence and status boundary

The H schema/parser CI result of 47/47 on its cited candidate commit is structural schema/reference-test evidence only. It is not canonical-byte interoperability, cryptographic verification, complete BMCP family coverage, production transport or runtime conformance. I's security review is an owner-scope technical disposition, not approval of I36-GOV-01..10 or a selected cryptographic suite.

**v3.1 status:** Storage proposal amended; exact-version A/B/C/D/E/G/H/I review required. No joint contract freeze, no cryptographic or full-wire freeze, no implementation/conformance PASS, no deployment and no production activation. JF-10 runtime P0 remains OPEN; Multi-PolicyDomain remains BLOCKED.
