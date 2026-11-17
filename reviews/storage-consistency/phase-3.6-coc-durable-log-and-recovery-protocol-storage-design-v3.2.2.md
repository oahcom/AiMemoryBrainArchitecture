# Phase 3.6 — Storage Design v3.2.2: COC Durable Log, Recovery Cutoff, Owner Gates & JF-10 Bridge

- Owner: Storage/Consistency
- Date: 2026-11-17
- Status: **REVISED STORAGE TECHNICAL DESIGN PROPOSAL v3.2.2 — FRESH EXACT-VERSION OWNER REVIEW REQUIRED**
- Project phase: **ARCHITECTURE DESIGN**
- Supersedes the earlier Storage design draft at commit `9a975f665ee60f4551effe0104ea8f867716d9dd`, blob `cd5566b3d99b5204401ac713a5bb2dcf89a02726`.
- Exact five-Owner review baseline (pinned by A/I/D/C/H acceptance artifacts): `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`.
- Current Storage companion clarification source: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` (PostgreSQL prepared-participant identity mapping integrated in §7.5; this later Blob is not misrepresented as the five-review baseline).
- Parent COC architecture: A branch `session-a-integration-2026-11-16`, blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Related Storage boundary: `phase-3.6-coc-storage-boundary-acceptance.md`
- Implementation / deployment / conformance: **NOT IMPLEMENTED / NOT DEPLOYED / NOT RUN**
- This proposal does not freeze cryptographic algorithms, wire schemas, a consensus product, production topology, or authorize activation.
- This v3.2.2 is a new immutable review target. v3.2.1, v3.2, v3.1 and earlier review decisions remain historical evidence only.

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


## 20. v3.2 normative Recovery Cutoff Batch / Participant Manifest ordering

This section is normative and supersedes any ambiguous reading of earlier batch/manifest ordering text. It does not change Owner authority or turn a prepared manifest payload into a committed COC record.

### 20.1 Required order and distinct artifacts

The recovery coordinator MUST execute the following order for one immutable `RecoveryEpoch` and one frozen prefix:

**S0a — Close owner-local admission and freeze Owner High-Waters first.** On the COC-outage/recovery trigger, I, D and C independently close their affected owner-local gates using their own authoritative linearization points and atomically capture their request/admission ledgers, high-waters, counts, roots and anti-rollback anchors. The frozen snapshots MUST include already admitted but not-yet-COC-registered operations, receipt issue/consume attempts, D pre-fence WorkItems/Attempts and C provider invocations/reservations/outcomes. Each owner keeps its gate closed. A racing operation is either included at/below that owner's captured high-water or rejected/suppression-only after the close; uncertain ordering is UNKNOWN and blocks recovery. These are independent owner snapshots, not one global atomic snapshot. Owner-local counters are never compared.

**S0b — Restore COC quorum and freeze Prefix P second.** Once quorum is available, enter `RECOVERY_FENCED`, stop all protected COC appends and participant recovery actions, and obtain a linearizable quorum-confirmed prefix:
`P = (CoordinatorEpoch, CoordinatorIndex, EntryDigest, CommittedConfigurationEpoch)`.
No new protected participant intent may be appended after P is frozen. Any operation admitted before an owner Gate close but lacking a COC record MUST remain represented in that owner's frozen ledger and be joined into the manifest under S1; it cannot disappear merely because it is absent from P. If any owner snapshot/high-water advances, becomes ambiguous or cannot be authenticated, or if P cannot be proved linearizable, remain `RESTORE_FENCED` and do not proceed.

**S1 — Construct the complete immutable Participant Manifest payload.** The manifest member set is the canonical union of (a) every committed `ParticipantIntentRef` at or before P from the quorum-confirmed COC prefix, and (b) every applicable I/D/C owner-local admission-ledger entry at or below its frozen owner high-water that can affect a participant, protected admission, receipt, lineage, provider side effect or terminal outcome, including entries not yet registered in COC. Cross-check the deterministic projection against the verified log prefix and cross-join each COC participant with its owner-ledger evidence where applicable.

Each member MUST carry an explicit typed discriminator:
- `COC_PARTICIPANT`: exact ParticipantIntentRef, COC position/digest, transaction/request digest, owner boundary and typed participant evidence refs;
- `OWNER_LOCAL_ADMISSION`: exact OwnerKind (I/D/C), OwnerAdmissionRef, owner-ledger ref/version, owner-local sequence/high-water, request/operation digest, admission state and explicit COC ParticipantIntentRef=null with a reason when no COC registration exists.

A member may carry both the owner-admission reference and the corresponding COC ParticipantIntentRef when the join is established. Deduplication is permitted only through an authoritative typed cross-reference proving the same immutable operation/attempt; shared TransactionId, matching timestamps or similar payloads are insufficient. Every frozen owner-ledger member MUST appear exactly once or have an owner-signed, scope-specific exclusion proof. Every applicable COC participant MUST appear exactly once. Missing COC registration is never an exclusion reason.

Construct the canonical ordered unique union, explicit empty-set representation (empty array, never null), member count, root/digest, COC enumeration high-water, per-owner ledger roots/high-waters, retrieval locator and typed evidence references. Allocate stable `ManifestId` and `ManifestDigest`. The canonical payload digest covers the complete union, P, RecoveryEpoch and frozen owner snapshot roots, but deliberately excludes the later Batch record position and the Manifest Record's Batch back-reference; this avoids circular digest dependency. Persisting/staging this payload is **not** a COC commit and does not authorize participant recovery.

**S2 — Commit Recovery Cutoff Batch first.** Append and quorum-commit exactly one `COC_RECOVERY_CUTOFF_BATCH` for the stable batch identity. It MUST bind:
- exact RecoveryEpoch and P tuple;
- frozen I/D/C owner snapshot attestations, gate generations, request-set counts/digests and owner high-waters;
- the canonical union semantics and each owner-ledger root/version needed to prove inclusion of pre-COC-registered admissions;
- ManifestId, ManifestDigest, participant count and enumeration high-water;
- canonicalization/schema profile identifiers and stable idempotency identity;
- coordinator quorum configuration epoch and commit proof.

The batch record MUST NOT inline a mutable or partial participant set as a substitute for the ManifestDigest. No participant recovery, Storage resolution, owner gate release or protected serving is permitted after S2 alone.

**S3 — Commit the separate Participant Manifest Record second.** Append and quorum-commit a distinct `PARTICIPANT_SET_RECONCILIATION` / Participant Manifest Record. It MUST:
- reference the exact quorum-committed Batch Record position and EntryDigest from S2;
- repeat the same RecoveryEpoch, P, ManifestId, ManifestDigest, count and enumeration high-water;
- carry the canonical union member payload, including both COC participants and pre-COC owner-local admissions; use an explicit empty array only when the complete union is truly empty;
- prove that hashing the canonical payload under the pinned profile yields the ManifestDigest already committed in S2;
- include the immutable record's own COC position, previous-entry digest and quorum commit proof.

The manifest record's envelope references the already committed batch; the canonical manifest payload digest does not include that back-reference. This is the required non-circular two-record binding. A Manifest Record without its prior Batch is invalid. A Batch without its subsequent Manifest Record is incomplete and remains fenced.

**S4 — Linearizable read-back and cross-binding verification.** Before any participant recovery begins, perform authoritative linearizable reads of both records from the quorum-confirmed prefix and verify all of the following:
1. Batch committed before Manifest Record (`BatchPosition < ManifestRecordPosition` in the same COC log namespace);
2. exact RecoveryEpoch and P equality;
3. exact ManifestId, ManifestDigest, count and enumeration high-water equality;
4. canonical union member payload re-hashes to ManifestDigest, with no duplicate, omission, null/empty ambiguity or ordering drift; every frozen owner-ledger member and every applicable COC participant is represented exactly once or has a valid owner-signed exclusion proof;
5. Manifest Record references the exact Batch position/digest;
6. both quorum commit proofs and committed configuration epochs are valid and current;
7. all frozen owner attestations are authentic and their owner-local generations/high-waters remain current;
8. no post-freeze admission crossed a closed owner gate.

Only after S4 succeeds may the coordinator enter `PARTICIPANTS_RECONCILING` and begin participant-specific owner lookups or same-XID/provider reconciliation. Failure at any check means `RESTORE_FENCED`; no best-effort recovery, partial participant iteration or owner release is permitted.

### 20.2 Crash/retry matrix

| Crash point | Durable facts that may exist | Mandatory next-leader behavior |
|---|---|---|
| Before S1 completes | P and owner freezes may exist; no manifest identity committed | Remain fenced; revalidate P and owner generations; deterministically rebuild or restart the attempt without side effects |
| After S1, before S2 | Staged ManifestId/Digest only | Treat staged payload as non-authoritative; verify exact P/owner snapshots, then submit the same stable Batch identity and digest; never release |
| After S2, before S3 | Batch committed and already binds ManifestId/Digest; Manifest Record absent | Remain fenced; linearizably read the exact Batch; retrieve/reconstruct the same canonical manifest payload; commit the same ManifestId/Digest as the required second record; never mint a replacement batch |
| After S3, before S4 | Both records may be committed; read-back incomplete | Remain fenced; re-read both exact records and rerun every S4 predicate |
| After S4, during participant reconciliation | Batch/Manifest verified; some participant outcomes may be pending | Resume idempotently from exact manifest membership and per-participant evidence; UNKNOWN/IN_DOUBT remains blocking |
| Any digest, count, order, P, epoch, owner-generation or identity mismatch | Contradictory evidence | Enter/retain RESTORE_FENCED; append immutable conflict evidence; do not repair by rewriting either record |

Retries MUST use the original immutable BatchId, ManifestId and canonical payload digest. Same identity + same digest is idempotent lookup/replay. Same identity + changed digest, changed P, changed owner snapshot, changed count or changed member set is CONFLICT and remains fenced. A later owner high-water or newly discovered pre-cutoff participant requires a new recovery attempt/cutoff generation; it MUST NOT be silently merged into the already committed batch.

### 20.3 Ordering invariants and forbidden transitions

- The only permitted order is: I/D/C owner-local Gate close + owner-ledger/high-water freeze → COC quorum prefix P freeze → canonical union Manifest payload prepared → Batch quorum commit → Manifest Record quorum commit → linearizable read-back of both → participant recovery/reconciliation.
- The Batch is the first committed COC cutoff record; the Manifest Record is the second committed COC record. The manifest payload may be deterministically constructed before S2, but is not authoritative until S3 and S4.
- Participant recovery MUST NOT begin between S2 and S4. In particular, no Storage COMMIT/ROLLBACK resolution, provider retry/handoff, I/D gate release, visibility publication or protected serving is permitted.
- A Batch with no Manifest Record is incomplete, not an empty manifest. An explicit zero-member Manifest Record is distinct from a missing record.
- No separate “manifest committed” flag, projection row, local file, event-bus ACK or API response substitutes for the quorum-committed Manifest Record and linearizable read-back.
- RecoveryEpoch completion remains a later record and is not implied by S4. It requires complete participant reconciliation and required owner-signed outage-gate releases under existing §5.5.

### 20.4 Exact-version bundle and downstream review gate

This v3.2.2 proposal is bound to:
- parent Storage v3.2 Blob: `e7ab80cdf8af5e0d50c407b06a5deb618d1e2ae6`;
- parent Storage v3.1 Blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`;
- current companion COC / PostgreSQL protocol Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`;
- current I Phase 3.6.8 proposal Blob: `cf4b76f151204fa47b156b5d807e7378c28fd268`;
- current D Phase 3.6.8 proposal Blob: `2d95099a2e19a8cbec325925b70da576f73d9899`.

The C and H exact reviews of Storage v3.2/v3.2.1 are predecessor review artifacts only and do not transfer to v3.2.2. C and H MUST re-review the exact v3.2.2 Blob and the current I/D blobs pinned above. H's unified schema must represent both COC-committed participants and owner-local pre-COC admissions as distinct typed manifest member variants. A must review the final exact-version binding manifest after C/H re-reviews are committed.

**Status:** v3.2.2 is a documentation proposal only. No implementation, quorum crash test, canonical-byte interoperability, provider idempotency, same-XID runtime recovery, owner release, production activation or Global Forget completion is claimed.


## 21. Bidirectional COC ParticipantManifest ↔ I/D/C Owner Admission Join Proof

- Status: **NORMATIVE STORAGE PROPOSAL / EXACT H-I-D-C-STORAGE OWNER REVIEW REQUIRED**
- Related H artifact: `08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.0.schema.json`, Blob `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- Related H semantic vectors: `test_hrc_semantics.py`, Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`; `test_schema_candidates.py`, Blob `67aba74c120f2916d768e7b01c45408ee2624f3a`.
- H CI evidence: run `44040139351`, commit `d36874c2656b08d1d7e10c367f32660241645e6a`, 66/66 candidate methods PASS. This is H candidate-suite evidence, not Storage adapter or integrated authority conformance.

### 21.1 Purpose and authority split

The RecoveryJoinProof is a separately verifiable, immutable relation between:
1. the exact quorum-committed COC ParticipantManifest at a Recovery Cutoff prefix; and
2. the independently frozen I, D and C owner request/admission ledgers at their respective owner-local high-waters.

The manifest's primary owner admission anchor remains the exact C admission identity required by the COC ParticipantIntent contract. I and D evidence are additional typed owner-evidence edges; they are not substituted into the primary C anchor.

Storage owns the completeness and durable evidence of the COC manifest record, its exact prefix/batch binding, its deterministic member union, its read-back, and its own JF-10 prepared-participant resolution evidence. Storage does not decide I/D/C admission, issue owner signatures, or release owner gates. H owns wire schema/encoding and validator implementation. I, D and C remain authoritative for their own ledgers, high-waters, signatures, request dispositions and releases.

### 21.2 Two independently complete source universes

The proof MUST preserve six separate owner enumerations:
- I request ledger and I admission ledger;
- D request ledger and D admission ledger;
- C request ledger and C admission ledger.

For each of the six sets, the signed snapshot binds:
- OwnerAuthorityRef and owner-specific ledger namespace;
- exact GateRef/GateGeneration and ScopeRef/ScopeGeneration;
- snapshot generation and independent anti-rollback anchor;
- enumeration status `COMPLETE_EMPTY` or `COMPLETE_NON_EMPTY`;
- explicit materialized array (empty array for empty; never null or absent);
- exact count, canonical member-set root and source ledger/version/cursor;
- owner-local sequence namespace and captured high-water(s);
- signer/key-status evidence and owner signature.

A missing ledger, unavailable owner, incomplete pagination, stale follower, unknown cursor continuity or unverifiable signature is UNKNOWN. It MUST NOT be represented as COMPLETE_EMPTY. Request and admission arrays are independent: an empty request set does not imply an empty admission set, or vice versa.

### 21.3 Direction A — every Owner Admission row must be accounted for

For every admission row in the frozen I/D/C admission set, RecoveryJoinProof MUST contain exactly one disposition keyed by the pair `(OwnerKind, OwnerEntryRef)`. The disposition resolves the exact owner row and binds:
- stable `OwnerAdmissionRef` (the cross-message admission identity);
- exact `OwnerEntryRef` (the immutable row identity inside the signed owner snapshot);
- OwnerEntryDigest and OperationIdentityRef/OperationDigest;
- owner-local sequence namespace/value, ScopeRef, GateGeneration and ScopeGeneration;
- admission state and exact disposition.

Allowed dispositions:

**REGISTERED_TO_PARTICIPANT**
- MUST bind one exact ParticipantIntentRef;
- MUST bind the ParticipantManifest entry digest and exact COC term/index/entry-digest position;
- MUST match operation identity/digest, participant tuple digest and Scope;
- MUST resolve to the exact row in the owner snapshot;
- MUST be represented in the reverse participant-to-owner evidence relation.

**NOT_REGISTERED_NO_EFFECT**
- MUST carry no ParticipantIntentRef, position or participant digest;
- MUST carry an owner-signed positive no-effect proof, or an explicitly typed still-pending disposition which keeps the gate blocked;
- a possible protected effect without proof is UNKNOWN and blocks release.

**OUT_OF_SCOPE_WITH_PROOF**
- MUST carry an owner-signed, scope-specific exclusion proof bound to the request/operation digest, ScopeRef, gate generation and source row;
- cannot be inferred from absence in the manifest or from COC's view.

No frozen admission row may disappear because it lacks a COC ParticipantIntent. An owner-local admission not yet registered in COC remains in the canonical manifest union as a distinct `OWNER_LOCAL_ADMISSION` member with a null participant locator and explicit disposition reason; it is not fabricated into a COC participant.

### 21.4 Direction B — every COC Participant must join accountable Owner evidence

For every ParticipantIntentRef in the exact COC prefix P, the reverse relation MUST prove:

1. **Primary C anchor:** exactly one C OwnerAdmissionRef and its exact C OwnerEntryRef row match the ParticipantManifest `owner_admission_ref` and primary owner-entry binding.
2. **I evidence:** every I evidence ref declared applicable to the participant resolves to an exact I owner admission row and its row digest, request/receipt identity, PolicyDomainRef, PermissionEpoch/producer inventory epoch, issuer/key identity and authorization/terminal receipt reference.
3. **D evidence:** every D evidence ref declared applicable resolves to an exact D owner admission row and binds ForgetOperationRef, ForgetFenceGeneration, lineage manifest ref/digest, BarrierMemberRef, producer/work/attempt identity and D-local high-water namespace.
4. **C evidence:** the C reservation/provider-attempt evidence resolves to the exact C row and binds provider idempotency namespace/key, reservation identity, attempt identity and actual provider-boundary evidence state. A reservation is not provider invocation or provider success.
5. **Storage evidence where JF-10 applies:** the exact PreparedParticipantRef/GID/DB incarnation and Storage resolution evidence are joined through the separate JF-10 sub-join described in §21.7.

I/D evidence cardinality may be many-to-one where one participant legitimately has distinct issue/consume, receipt/terminal, lineage/barrier or attempt evidence rows. Every individual evidence row nevertheless has exactly one stable OwnerEntryRef and must be accounted for; no row may be reused for a different operation/participant unless an explicit owner-approved typed cardinality rule permits it.

A ParticipantIntent with no primary C anchor, missing required I/D/C evidence, unresolved owner row, mismatched operation digest or scope is UNKNOWN or INVALID and blocks reconciliation. COC manifest membership alone is never proof of owner admission.

### 21.5 Request-ledger join is separate from admission-ledger join

For every I/D/C request-ledger row, JoinProof MUST contain exactly one request disposition. The exact set equality is:

`OwnerRequestRows(owner) = JoinProofRequestDispositionRows(owner)`

Each disposition binds OwnerRequestRef, OwnerEntryRef, OwnerRequestDigest, OwnerEntryDigest, owner-local sequence namespace/value, ScopeRef and owner signature.

Allowed dispositions:
- `IN_BATCH_REQUEST_SET`: exact request row is included in the recovery batch/request inventory and linked to the applicable admission/participant disposition where one exists.
- `OUT_OF_SCOPE_WITH_PROOF`: exact row is excluded only by an owner-signed proof bound to the request digest and scope/generation.
- A pending or unresolved request remains represented and blocks owner release; it is not dropped.

The request set is not derived from the admission set. A request may have no admission or ParticipantIntent and still be a frozen owner obligation. An admission may be present even when a separate request row is not applicable under the owner's declared ledger semantics; the owner must attest that relationship explicitly rather than H or Storage guessing.

### 21.6 Canonical bidirectional set equations and difference sets

Let:
- (A_I,A_D,A_C) be the exact frozen owner admission-row sets;
- (Q_I,Q_D,Q_C) be the exact frozen owner request-row sets;
- (P) be the exact COC ParticipantIntent set at prefix P;
- (J_{A	o P}) be OwnerAdmission-to-Participant edges;
- (J_{P	o A}) be Participant-to-Owner evidence edges;
- (J_Q) be request-row dispositions.

A complete proof MUST establish:
- every member of each (A_o) has exactly one explicit admission disposition;
- every `REGISTERED_TO_PARTICIPANT` member maps to one exact member of (P);
- every member of (P) has exactly one primary C anchor and all required typed owner-evidence edges;
- every member of each (Q_o) has exactly one request disposition;
- every reference resolves to the exact owner row, digest and namespace, not merely a matching string.

The proof MUST publish explicit difference sets, at minimum:
- `owner_admissions_without_disposition`;
- `registered_admissions_without_manifest_participant`;
- `manifest_participants_without_primary_C_admission`;
- `manifest_participants_missing_required_owner_evidence`;
- `owner_evidence_refs_unresolved_in_snapshot`;
- `owner_requests_without_disposition`;
- `duplicate_or_conflicting_owner_entry_refs`;
- `duplicate_or_conflicting_participant_refs`;
- `out_of_scope_dispositions_missing_proof`;
- `storage_jf10_tuple_mismatches`.

For COMPLETE, every blocking difference set MUST be present and empty, each set count MUST equal its materialized array length, and the root MUST be recomputed over the canonical ordered set. Missing/null difference arrays are not empty. UNKNOWN/partial source enumeration makes the entire JoinProof UNKNOWN, never COMPLETE.

### 21.7 JF-10 Storage sub-join and same-XID terminal coupling

The Storage sub-join is a distinct typed relation, not an extension of I/D/C owner-admission identity. For each applicable prepared participant it binds, without aliasing:
- ParticipantIntentRef and CausalOrderTransactionRef;
- PublicationOperationId / RequestDigest / ParticipantTupleDigest;
- PreparedParticipantRef and client-chosen PreparedTransactionGID;
- CanonicalAuthorityDBRef and DatabaseIncarnationRef;
- PostgreSQL native XID as observed engine evidence only;
- PrepareAttemptRef/Generation;
- ParticipantLedgerRef/Version;
- exact COC prepare-intent position/digest;
- exact I receipt/decision reference and I sequencer position;
- exact Storage PreparedParticipantReceipt and StorageResolutionProof.

Terminal mapping for this JF-10 bridge:
- I COMMIT_WON → same participant, same GID and same DB incarnation Storage COMMITTED;
- I REVOCATION_WON or INDETERMINATE_ABORTED → same participant, same GID and same DB incarnation Storage ROLLED_BACK;
- I or Storage UNKNOWN/IN_DOUBT → unresolved; preserve prepared participant and block release;
- any contradictory terminal pair or identity mismatch → INVALID, quarantine and immutable conflict evidence.

The numeric PostgreSQL native XID is never the cross-service identity; the client-chosen GID and PreparedParticipantRef are. This JF-10 terminal coupling MUST NOT be conflated with the Phase 3.8 derivative visibility proof stages: pre-commit ICommitAuthorizationProof is validated at visibility commit; post-commit ITerminalProof is issued only after the Storage outcome. The two proof domains have different state machines and nominal types.

### 21.8 JoinProof immutable binding and currentness CAS

JoinProof binds:
- RecoveryEpoch and round;
- exact RecoveryCutoffBatch ref/digest;
- exact ParticipantManifest ref, content digest and committed record digest;
- exact quorum-confirmed COC prefix term/index/root/configuration epoch;
- six owner request/admission snapshot refs, digests, roots, counts and high-waters;
- ScopeRef/ScopeGeneration and ReconciliationAttemptGeneration;
- both directional edge arrays, request dispositions, JF-10 sub-joins, completeness and difference sets;
- canonicalization/digest profile refs, issuer/audience and signature envelope.

Before I, D or C releases its own outage gate, that owner MUST independently re-read its authoritative current ledger and perform its own currentness CAS against the exact JoinProof root and its own request/admission roots, high-waters, GateGeneration, ScopeGeneration, snapshot generation and anti-rollback anchor. Any advance invalidates the candidate release and requires a subsequent cutoff round. Storage/COC cannot perform this CAS on behalf of an owner.

No cross-owner numeric high-water comparison is permitted. COC term/index, I PermissionEpoch/sequencer position, D ForgetFence/producer high-waters and C reservation/provider-attempt positions remain distinct typed namespaces.

### 21.9 Deterministic Storage acceptance vectors

Storage requires the following integrated tests in addition to H's HRC/JPF/WIRE/schema suite:

| ID | Injected condition | Required result |
|---|---|---|
| ST-JOIN-01 | Omit one frozen I/D/C admission row from all dispositions | INVALID; no gate release |
| ST-JOIN-02 | Add an extra admission disposition not present in owner snapshot | INVALID |
| ST-JOIN-03 | One owner request row lacks a request disposition | INVALID |
| ST-JOIN-04 | One request disposition has changed OwnerRequestDigest or OwnerEntryDigest | INVALID/CONFLICT |
| ST-JOIN-05 | COMPLETE_EMPTY uses missing/null array or incomplete pagination | INVALID/UNKNOWN; never empty |
| ST-JOIN-06 | COC participant omitted from manifest at exact prefix P | INVALID; RESTORE_FENCED |
| ST-JOIN-07 | Manifest participant lacks exact primary C admission anchor | UNKNOWN/INVALID |
| ST-JOIN-08 | OwnerAdmissionRef substituted for OwnerEntryRef, or vice versa | INVALID |
| ST-JOIN-09 | I/D evidence row exists but operation digest, Scope or typed owner evidence differs | INVALID |
| ST-JOIN-10 | One valid I issue/consume evidence pair maps to one participant under explicit many-to-one rule | VALID |
| ST-JOIN-11 | NOT_REGISTERED row carries ParticipantIntentRef or position | INVALID |
| ST-JOIN-12 | NOT_REGISTERED may have had effect but has no positive no-effect proof | UNKNOWN; gate held |
| ST-JOIN-13 | OUT_OF_SCOPE_WITH_PROOF lacks owner signature or exact scope/request binding | INVALID |
| ST-JOIN-14 | Duplicate participant position or duplicate ParticipantIntentRef | INVALID |
| ST-JOIN-15 | JoinProof created, then any owner high-water/gate/scope generation advances before release CAS | STALE; new cutoff round |
| ST-JOIN-16 | JF-10 I COMMIT_WON paired with different GID/DB incarnation or Storage ROLLED_BACK | INVALID |
| ST-JOIN-17 | JF-10 I REVOCATION_WON paired with same-XID Storage COMMITTED | INVALID |
| ST-JOIN-18 | Any owner/COC source unavailable, stale, partial or unverifiable | UNKNOWN; RESTORE_FENCED |
| ST-JOIN-19 | RecoveryJoin digest changes under same message identity | CONFLICT |
| ST-JOIN-20 | COC attempts to manufacture I/D/C owner release | INVALID |

Every test must assert the authoritative source-row set, exact JoinProof edges/digests, difference sets, COC recovery state and each owner gate state. Mocked expected-value returns are not integrated conformance.

### 21.10 Disposition / bilingual status

This §21 is a Storage-authored logical proposal for the two-way join. It aligns with H RecoveryJoin 1.0.0 candidate fields and H's 66-test candidate suite, but it does not establish that the production COC adapter or I/D/C ledger adapters implement the relation.

**Still OPEN:** exact H/I/D/C/Storage owner acceptance of this Storage v3.2.2 amendment; exact wire/canonicalization/signature profile; production COC prefix enumeration; owner-signed source snapshots; real I/D/C ledger adapters; same-XID Storage bridge; currentness CAS; independent implementation and integrated physical conformance.

No COC quorum product, DB topology, cryptographic suite, implementation PASS, production activation, owner gate release or Global Forget completion is selected or claimed.

### 21.11 中文规范

#### 21.11.1 目标与权威边界
RecoveryJoinProof 是 Recovery Cutoff Prefix 下 COC ParticipantManifest 与 I/D/C 三个 Owner 各自 Request/Admission Ledger 的不可变双向关系。COC ParticipantManifest 的主 Owner Admission Anchor 仍然是 C Admission；I/D 证据是额外 Typed Evidence Edge，不能替代 C 主锚点。Storage 负责 COC Manifest 的完整性、Batch/Prefix 绑定、持久化和自身 JF-10 证据；I/D/C 仍拥有各自 Ledger、签名、高水位、请求处置和 Gate Release；H 拥有 Wire/Schema/Validator。

#### 21.11.2 六个独立集合
必须分别枚举 I Request、I Admission、D Request、D Admission、C Request、C Admission 六个集合。每个集合都必须绑定 OwnerAuthority、Ledger Namespace、Gate/Scope Generation、Snapshot Generation、Anti-rollback Anchor、COMPLETE_EMPTY/COMPLETE_NON_EMPTY、显式数组、Count、Canonical Root、Source Cursor/Version、Owner-local High-water、Signer/Key Status 和 Owner Signature。缺失、分页不完整、陈旧副本、签名不可验证或 Cursor 不连续均为 UNKNOWN，不得视为 EMPTY。Request Set 和 Admission Set 永远不能合并。

#### 21.11.3 方向 A：Owner Admission → ParticipantManifest
每个 I/D/C Admission Row 必须按 `(OwnerKind, OwnerEntryRef)` 恰好有一个 JoinProof Disposition。必须区分稳定跨消息身份 OwnerAdmissionRef 和 Snapshot 中的精确行身份 OwnerEntryRef，并绑定 OwnerEntryDigest、OperationIdentity/Digest、Owner-local Sequence Namespace/Value、Scope、GateGeneration/ScopeGeneration。

REGISTERED_TO_PARTICIPANT 必须映射精确 ParticipantIntentRef、Manifest Entry Digest、COC Term/Index/EntryDigest、Operation/Digest 和 Scope，并在反向 Evidence 中出现。NOT_REGISTERED_NO_EFFECT 不得携带 Participant Locator，必须有 Owner-signed 正向 No-effect Proof 或显式 Pending Disposition；可能已经产生效果但无证明时为 UNKNOWN。OUT_OF_SCOPE_WITH_PROOF 必须由 Owner 对精确 Request/Scope/Generation 签名证明。没有 COC Participant 的 Owner-local Admission 仍必须作为独立 OWNER_LOCAL_ADMISSION 成员保留，不能因为未注册到 COC 就遗漏。

#### 21.11.4 方向 B：ParticipantManifest → Owner Evidence
每个 COC Participant 必须有且仅有一个 Primary C Admission Anchor，并通过 OwnerAdmissionRef 和 OwnerEntryRef 分别解析。所有适用 I Receipt/Authorization、D ForgetFence/Lineage/Barrier、C Reservation/Provider Attempt Evidence 必须解析到 Owner Snapshot 中精确 Row，并绑定各自的 Digest、Scope、Operation 和 Owner-local Authority。I/D 可以按明确的多对一语义将多个不同证据行关联同一个 Participant，但每行身份必须独立且唯一。Manifest membership 不是 Owner Admission 证明。

#### 21.11.5 Request Ledger 独立 Join
I/D/C 每个 Request Row 都必须恰好有一个 Request Disposition。精确集合相等：OwnerRequestRows(owner) = JoinProofRequestDispositionRows(owner)。每条边绑定 OwnerRequestRef、OwnerEntryRef、OwnerRequestDigest、OwnerEntryDigest、Owner-local Sequence、Scope 和 Owner Signature。OUT_OF_SCOPE_WITH_PROOF 必须有精确 Owner 签名证明；Pending/Unknown 请求不得遗漏。Request Set 不得从 Admission Set 推导。

#### 21.11.6 双向差集与完整性
JoinProof 必须显式输出缺少 Admission Disposition、REGISTERED 缺少 Participant、Participant 缺少 Primary C、缺少 I/D/C Evidence、Evidence Row 无法解析、Request Row 无 Disposition、重复/冲突身份和缺少 Scope Proof 等 Difference Sets。COMPLETE 时所有阻塞差集必须显式存在且为空，Count 等于数组长度，Root 必须重算匹配。缺失/null 数组不是空集。

#### 21.11.7 JF-10 与 Phase 3.8 Proof 隔离
JF-10 Sub-join 必须绑定同一 ParticipantIntentRef、PreparedParticipantRef、PreparedTransactionGID、DB Incarnation、Operation/Request/Participant Tuple Digest、I Decision 和 Storage Resolution。COMMIT_WON 对应同一 GID/DB 的 COMMITTED；REVOCATION_WON/INDETERMINATE_ABORTED 对应同一 GID/DB 的 ROLLED_BACK；UNKNOWN 保持未解决。PostgreSQL Native XID 仅是观察证据，不能代替 GID/PreparedParticipantRef。

JF-10 的 I Terminal Decision 与 Phase 3.8 衍生可见性 Gate 不得混淆：Phase 3.8 提交前验证 ICommitAuthorizationProof，提交后才签发 ITerminalProof；两套协议必须保持不同类型和状态机。

#### 21.11.8 当前性 CAS 与未决事项
JoinProof 绑定 RecoveryEpoch/Round、Batch/Manifest/Prefix、六个 Owner Snapshot、Scope/Generation、ReconciliationAttemptGeneration、双向 Edge、Request Disposition、JF-10 Sub-join、Difference Set、Canonicalization/Digest Profile 和签名 Envelope。I/D/C 在各自 Gate Release 前必须独立重新读取本地权威 Ledger，并对 JoinProof Root、自己的 Request/Admission Roots、High-water、Gate/Scope Generation、Snapshot Generation 和 Anti-rollback Anchor 执行 Currentness CAS。任何推进都使候选 Release 过期，必须新一轮 Cutoff。

本提案仍需 H/I/D/C/Storage 对精确版本正式审查；生产 Wire/Signature、真实 COC/Owner Adapter、物理 JF-10、Currentness CAS 和集成 Conformance 均 OPEN。没有宣称 Schema Freeze、实现通过或生产激活。
