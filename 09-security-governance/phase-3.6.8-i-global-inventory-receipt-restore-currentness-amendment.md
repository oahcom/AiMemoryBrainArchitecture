# Phase 3.6.8 — I Global Inventory, Receipt Boundary & Restore Currentness Amendment

- Owner perspective: I — Security & Governance
- Status: **PROPOSED OWNER-LOCAL AMENDMENT — EXACT-VERSION I RE-REVIEW REQUIRED**
- Supersedes: none; append-only refinement of Phase 3.6.7
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 0. Exact-version lineage and normative bundle

This amendment is a new revision responding to I's Phase 3.6.7 decision. It does not modify the reviewed source blob or its decision record.

- Phase 3.6.7 I source commit: `b0723c61a22d1f1d82bf395d37e0602d2c863d73`
- Phase 3.6.7 I source blob: `0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7`
- Phase 3.6.7 I exact-version decision commit: `b637e58e98275a684283fab15f9c1de16e25696e`
- Phase 3.6.7 I decision blob: `325cd63164c217f8712964da58509f867d105740`
- Current Storage Design v3.1 blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- Current COC protocol blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Historical Storage Design v2 blob (not current companion): `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`

Normative pairing for this amendment is Storage Design v3.1 + COC protocol 8ac178. The v2 blob is retained solely as historical lineage.

## 1. Authority and vocabulary

I remains the sole authority for PolicyDomain permission/revocation, I Gate generation, I request ledger, ProducerDomainInventoryEpoch, global Producer/Recipient/Backup/Export/Restore inventory membership, I receipt issue/consume and I Gate release. D owns ForgetFenceGeneration, D work admission, barrier membership and D terminalization. Storage owns prepared participant durability and visibility. COC persists ordered evidence and recovery batches but cannot mint Owner decisions.

The protocol MUST keep these independent values distinct:
- `IGateGeneration`: I outage/admission Gate generation;
- `IRequestHighWater` and request-ledger root: I request/receipt in-flight inventory boundary;
- `PermissionEpoch`: policy authorization/revocation epoch;
- `ProducerDomainInventoryEpoch`: global inventory membership epoch;
- registry snapshot digest and per-entry generations;
- D `ForgetFenceGeneration`, D producer/work high-waters and barrier closure;
- COC `RecoveryEpoch`, committed prefix, Recovery Cutoff Batch and participant manifest;
- Storage participant identity, prepare attempt and participant ledger version;
- RestoreAttemptRef/checkpoint generation and anti-rollback anchor.

These values are typed, owner-local and not numerically comparable. No synthetic global counter or fictional atomic cross-owner snapshot is introduced.

## 2. I-M1 — Typed global inventory and cross-owner reconciliation tuple

Every I inventory-completeness proof, I receipt issue/consume decision and I Gate Release receipt MUST bind a typed `IReconciliationTuple` containing:

1. **I request Gate snapshot**: I Gate ref/state, IGateGeneration, IRequestHighWater, canonical ordered request refs/count/root, PermissionEpoch and I sequencer position.
2. **I global inventory snapshot**: PolicyDomainRef, normalized ScopeBindingFingerprint, ProducerDomainInventoryEpoch, registry snapshot digest, relevant InventoryEntryRef + InventoryEntryGeneration set, TargetInventorySealRef/digest, completeness proof generation/status, signer/key status generation.
3. **D owner snapshot**: ForgetOperationRef + request digest, D FenceGeneration, D producer-registration and work/attempt high-waters, barrier membership root/count/generation, dependency-closure digest/cursor.
4. **COC recovery snapshot**: RecoveryEpoch, exact committed prefix/term-index range, Recovery Cutoff Batch identity/digest, participant manifest identity/digest.
5. **Storage participant join where applicable**: PreparedParticipantRef, PreparedTransactionGID, DatabaseIncarnationRef, PostgreSQLNativeXID when known, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, ParticipantTupleDigest, PublicationOperationId, RequestDigest, owner boundary and COC Prepare Intent position/digest.
6. **Restore identity when applicable**: RestoreAttemptRef, checkpoint generation/digest, restored sequencer/registry epoch refs and anti-rollback anchor.

The tuple is a reconciliation envelope over independent authoritative snapshots, not a claim that all owners took one globally atomic snapshot. Each owner signs only its own fields. Cross-owner fields are references/digests and must be checked against the owning authority.

IRequestHighWater MUST NOT be used as a proxy for ProducerDomainInventoryEpoch. The I request ledger and global inventory registry are separate completeness domains.

## 3. I-M2 — Inventory epoch currentness and mutation race closure

### 3.1 Currentness predicate

Before issuing GlobalInventoryCompletenessProof, TargetInventorySeal, an I authorization receipt, or IGateReleaseReceipt, I MUST re-read and compare:
- ProducerDomainInventoryEpoch;
- registry snapshot digest;
- every relevant InventoryEntryGeneration and scope/policy mapping;
- completeness-proof and target-seal generations;
- signer/key status and revocation generation;
- PermissionEpoch and sequencer/anti-rollback generation;
- the D and COC tuple members required for the operation.

The proof is current only if the authoritative values still match the values bound into the candidate proof. A changed value makes the affected proof STALE and requires a new snapshot/reconciliation attempt; it must not be silently patched in place.

### 3.2 Linearization boundary

The final I issue/release operation MUST execute as one authoritative sequencer/CAS transaction that:
1. validates the candidate tuple against the latest inventory and permission generations;
2. validates the request Gate generation and exact request high-water;
3. verifies no registry mutation committed between snapshot validation and proof issuance;
4. appends the proof/receipt and advances the relevant I sequence atomically.

A read-then-sign workflow without a compare-at-commit or equivalent linearizable guard is insufficient. If I cannot establish currentness due to partition, leader uncertainty, missing epoch source or unavailable registry authority, result is UNKNOWN and I Gate stays closed; no completeness or release receipt may be issued.

### 3.3 Scope of invalidation

A ProducerDomainInventoryEpoch advance makes I inventory evidence stale until revalidated. Re-sealing may preserve unaffected entry evidence only if I proves the relevant entry generations, scope mapping and completeness dependencies remain current. It cannot assume that an unrelated-looking epoch increment is harmless without dependency proof.

## 4. I-M3 — Exact Storage participant receipt consumption

Where an I decision authorizes or consumes a receipt for a Storage participant, the I terminal transaction MUST bind the complete immutable participant tuple:
- PreparedParticipantRef and PreparedTransactionGID;
- CanonicalAuthorityDBRef and DatabaseIncarnationRef;
- PostgreSQLSystemIdentifier and PostgreSQLDatabaseOID where defined by Storage profile;
- PostgreSQLNativeXID when known;
- PrepareAttemptRef/PrepareAttemptGeneration;
- ParticipantLedgerRef/ParticipantLedgerVersion;
- PublicationOperationId, RequestDigest and ParticipantTupleDigest;
- owner boundary, PolicyDomainRef and exact scope binding;
- COC PrepareIntentRef, typed COC position and entry digest;
- original prepare timeline/LSN and Storage's authoritative prepared observation reference where required by the Storage v3.1 contract.

GID, native XID, database authority, database incarnation, attempt identity and ledger identity are not interchangeable.

If PostgreSQLNativeXID is not yet known at initial intent, I records an explicit typed UNKNOWN/not-yet-observed value and the exact participant/attempt identity. Later discovery is append-only enrichment referencing the same PreparedParticipantRef, PrepareAttemptGeneration and ParticipantLedger lineage. It MUST NOT replace the participant identity, rewrite the original intent, or permit a different participant to consume the same I receipt.

Receipt consumption is single-use and atomic with the I terminal decision. A tuple mismatch, conflicting enrichment, changed attempt, stale ledger version or ambiguous COC position returns CONFLICT/UNKNOWN and fails closed.

## 5. I-M4 — Generation fencing at every issue/consume boundary

Every I receipt issuer, verifier and consumer MUST validate the current IGateGeneration and PermissionEpoch at its authoritative effect boundary. A cached OPEN value is never sufficient.

Required behavior:
- **stale cache**: reject if cached generation is older or cannot be refreshed;
- **partitioned worker**: no issue/consume without an authoritative sequencer read or valid unexpired fencing token whose generation is checked by the final transaction;
- **retry/replay**: same idempotency key and same digest returns the original outcome; same key with changed digest is CONFLICT; a replay cannot mint a second receipt or consume twice;
- **leader change**: new leader proves monotonic sequencer/anti-rollback continuity before accepting work; uncertain/forked state is UNKNOWN;
- **close race**: issue/consume transaction must compare the generation it observed with the current generation at commit; if Gate close won, operation aborts;
- **lost ACK**: outcome is recovered from the authoritative ledger by stable operation identity; absence of ACK is not proof of non-effect.

I Gate closure blocks new protected receipt issue/consume unless an explicitly typed recovery/cleanup action is authorized by I. COC persistence alone does not authorize an I operation.

## 6. I-M5 — Restore and anti-rollback release handshake

Restore MUST begin with I Gate CLOSED. Before any I serving/admission release, I MUST bind:
- exact RestoreAttemptRef and source checkpoint generation/digest;
- restored I sequencer identity/position and proof it is non-forked;
- current ProducerDomainInventoryEpoch, registry digest and relevant entry generations;
- current PermissionEpoch, IGateGeneration and request-ledger high-water/root;
- anti-rollback anchor external to the rollback-prone restored snapshot;
- D's current ForgetOperationRef, FenceGeneration, barrier root and dependency-closure digest/cursor;
- exact COC RecoveryEpoch/prefix/batch/participant-manifest identity;
- Storage participant reconciliation where applicable.

Immediately before issuing release, I revalidates its own currentness and obtains/validates D's current owner-signed fence/barrier/closure tuple for the same RestoreAttemptRef, ForgetOperationRef, PolicyDomainRef and scope. This is a two-owner currentness handshake, not a shared atomic snapshot. If either side advances or cannot prove currentness, the release attempt is stale and must restart.

I release never authorizes D to clear a Forget Fence, Storage to expose a participant, or any owner to serve restored pre-fence material. Restore rollback, sequencer fork, stale registry or absent D closure evidence is blocking UNKNOWN.

## 7. I release algorithm and negative conditions

I may issue `IGateReleaseReceipt` only when:
1. exact COC RecoveryEpoch/prefix/Recovery Cutoff Batch/participant manifest are verified;
2. I request ledger is complete through captured IRequestHighWater, including all issue/consume attempts and uncertain ACKs;
3. global inventory proof and all relevant entry generations are current;
4. all applicable Storage tuples join exactly and all I receipts are single-use/terminal;
5. PermissionEpoch, IGateGeneration, sequencer and anti-rollback anchors are current;
6. D fence/barrier/closure and RestoreAttempt tuple are current where applicable;
7. no unresolved UNKNOWN, lost ACK, scope ambiguity, digest conflict, stale key, missing evidence or concurrent mutation remains.

Only I can release I Gate. I release does not clear D Fence, resolve Storage XIDs, prove physical erasure or imply Global Forget Completion.

## 8. Owner-local in-flight classes retained

The I ledger continues to include: request admitted but not COC registered; receipt issue in progress/ACK lost; receipt consume in progress/outcome uncertain; COC intent committed but I decision absent; I decision consumed but Storage/COC observation delayed; retry/replay/duplicate/lease expiry/worker restart; restore/replay; post-high-water discoveries; and registry mutations racing completeness/release.

No missing COC row, expired lease, absent worker, timeout or stale cache is terminal evidence.

## 9. Required conformance cases — specified, not executed

- inventory epoch advances between snapshot and proof commit;
- relevant entry generation changes while unrelated entries remain stable;
- signer/key revocation races release;
- receipt issue races IGateGeneration close;
- partitioned stale worker attempts receipt consumption;
- leader change with uncertain anti-rollback continuity;
- native XID appears after initial intent;
- same participant identity but changed PrepareAttemptGeneration;
- Restore checkpoint is stale while D FenceGeneration advances;
- exact tuple mismatch or missing COC participant manifest;
- release attempted with one UNKNOWN request or inventory member.

**Disposition:** Phase 3.6.8 I proposed amendment incorporating I-M1 through I-M5. Exact-blob I re-review is required. No implementation PASS, cryptographic profile freeze, production activation, global inventory completeness, physical erasure or Global Forget Completion is claimed.

## 10. Provenance

This document is an assistant-authored role-based proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human I Owner authorship or approval.


## 11. I36.8-R1..R4 — Mandatory owner-local revision (append-only)

This section is a normative append-only refinement of §§2–7. Where an earlier sentence is less specific or inconsistent with this section, this section controls for the revised Phase 3.6.8 proposal. The previously reviewed source Blob remains immutable historical evidence.

### 11.1 I36.8-R1 — Atomic I Gate-close and request admission

For each affected PolicyDomain, I MUST execute Gate close through one authoritative serializable sequencer transaction. That single transaction MUST:
1. append the stable IRevocationRequestRef and immutable RequestDigest to the I request ledger;
2. set the affected I Gate state to PENDING_COC_CUTOFF;
3. increment IGateGeneration;
4. capture the exact request-set count, canonical digest/root, IRequestHighWater and owner cursor;
5. persist the anti-rollback anchor bound to the resulting sequencer position and generation;
6. commit all of the above atomically, and only after that commit acknowledge the revocation request as pending.

The request is not acknowledged as pending before the close transaction commits. There is no intermediate state in which a request is accepted but absent from the authoritative I request ledger or in which the Gate remains OPEN at the old generation after the request is acknowledged.

Every affected receipt issue and receipt consume operation MUST serialize through the same PolicyDomain sequencer. Its final authoritative transaction MUST compare the current Gate state and IGateGeneration in-transaction, and MUST be ordered either before the close transaction (and therefore included in the captured request/in-flight accounting) or after it (and therefore rejected unless it is an explicitly authorized typed recovery/cleanup action). A prior read, cached OPEN value, worker lease or detached token is not sufficient. Lost acknowledgement is resolved by stable request identity and ledger readback; it is not evidence that the close did not commit.

### 11.2 I36.8-R2 — Exact Storage owner-final-gate participant and terminal proof

Whenever I terminalizes a Storage owner-final visibility-gate participant, the I terminal decision MUST be one authoritative I sequencer transaction that validates and atomically consumes the exact participant and authorization tuple. The proof MUST bind all of the following:
- stable StorageFinalGateParticipantRef identifying the exact owner-final visibility-gate participant;
- owner_boundary and PolicyDomainRef;
- ISequencerPosition at which the terminal decision linearized;
- terminal outcome enum: COMMIT_WON, REVOCATION_WON or INDETERMINATE_ABORTED; UNKNOWN and IN_DOUBT are explicitly nonterminal and MUST NOT be encoded as a terminal result;
- exact CommitAuthorizationReceiptRef and digest, plus its single-use consumption identity and ledger evidence;
- PreparedParticipantRef, PreparedTransactionGID, CanonicalAuthorityDBRef, DatabaseIncarnationRef, PostgreSQLSystemIdentifier and PostgreSQLDatabaseOID where defined, PostgreSQLNativeXID when known;
- PrepareAttemptRef and PrepareAttemptGeneration, ParticipantLedgerRef and ParticipantLedgerVersion, PreparedParticipantReceiptRef and digest, and the complete ParticipantTupleDigest;
- PublicationOperationId, RequestDigest, COC PrepareIntentRef, typed COC position and entry digest;
- the relevant PermissionEpoch, exact scope binding and owner-local references needed to validate the decision.

The final I transaction MUST reject a mismatched participant, attempt, database incarnation, XID, ledger version, receipt digest, authorization receipt or COC intent. CommitAuthorizationReceipt consumption and I terminal-proof issuance are atomic and single-use. The resulting proof authorizes only the exact bound participant and cannot be detached and replayed to authorize another Storage commit. Storage remains the authority for same-XID resolution and its PublicationReceipt/VisibilityPointer or authoritative non-publication proof; I terminality does not itself prove Storage visibility.

### 11.3 I36.8-R3 — Shared reconciliation-attempt join envelope

IReconciliationTuple MUST carry an interoperable join identity with these exact typed fields:
- ReconciliationAttemptRef and monotonically increasing AttemptGeneration;
- TupleSchemaId, TupleSchemaVersion and CanonicalizationProfileRef;
- canonical tuple digest computed over the versioned canonical representation;
- I-signed subrecord reference and digest, and D-signed subrecord reference and digest;
- D FenceGeneration and D FenceInstallationCursor, plus the applicable D work/producer high-waters and barrier membership root/generation;
- exact COC RecoveryEpoch, committed-prefix/position reference, RecoveryCutoffBatchRef/digest and ParticipantManifestRef/digest;
- the I inventory and permission fields already required by §§2–3, and the Storage participant join fields where applicable.

The same ReconciliationAttemptRef, AttemptGeneration, schema/version and canonicalization profile MUST be used by I and D for a given join attempt. Each Owner signs only its own subrecord. The envelope joins independently authoritative evidence; it is not a globally atomic cross-owner snapshot and must not imply simultaneous sampling.

Any change to a bound owner generation, high-water, fence installation cursor, inventory epoch, target seal, completeness proof, scope mapping, key-status generation, COC recovery reference, participant manifest or signed subrecord digest invalidates the affected attempt. The owners MUST append a new attempt generation and recapture/reconcile the affected evidence; they MUST NOT mutate or silently refresh the old signed tuple in place. The exact COC and participant-manifest references remain mandatory even while their cross-document ordering conflict is unresolved; this amendment does not declare that conflict solved.

### 11.4 I36.8-R4 — Cryptographic lifecycle separation and fail-closed terminality

This Phase 3.6.8 revision does not select or freeze a cryptographic/key lifecycle profile. I MUST publish that profile as a separately versioned normative artifact defining, at minimum, issuer, subject, audience, purpose, canonical signed bytes, algorithm agility, key custody, rotation, revocation, compromise response, historical verification, signer authorization and anti-rollback behavior. H must map the wire representation to that separately approved profile; a tuple digest or signature field alone is not a complete cryptographic policy.

Stale or unavailable key status, unknown or conflicting terminal outcome, missing owner proof, changed digest, unavailable sequencer/registry authority, uncertain restore, participant mismatch or incomplete reconciliation MUST yield UNKNOWN/CONFLICT and keep the affected I Gate closed. UNKNOWN and IN_DOUBT are durable blocking states, not terminal enums. Timeout, lease expiry, missing COC row, absent worker, lost ACK or operator assertion cannot manufacture terminality or release authority.

### 11.5 Added conformance obligations — specified, not executed

- prove the serializable close transaction commits all six R1 effects before the pending acknowledgement is emitted;
- race receipt issue and receipt consumption against Gate close and show that each operation is serialized on the same sequencer;
- verify a lost close acknowledgement is recovered by stable request identity without duplicate close or receipt consumption;
- reject terminal proof with wrong StorageFinalGateParticipantRef, owner boundary, ISequencerPosition, authorization receipt, participant tuple, XID, attempt or ledger version;
- reject UNKNOWN/IN_DOUBT as terminal and keep the Gate closed;
- verify I and D use the same attempt generation, schema, canonicalization profile and signed-subrecord digests, including D FenceInstallationCursor;
- invalidate and restart the attempt after any bound owner generation or evidence digest changes;
- verify stale/revoked/unknown key status blocks terminalization and release.
