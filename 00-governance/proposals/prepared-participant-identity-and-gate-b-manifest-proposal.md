# Prepared Participant Identity & Gate B Canonical Manifest — P Proposal

- Proposal ID: P-COC-JF10-IDENTITY-MANIFEST-001
- Status: **PROPOSED — NON-NORMATIVE COORDINATION INPUT**
- Prepared by: Session P coordinator
- Date: 2026-11-17
- Authority: This document does not create A/B/C/D/E/F/G/H/I/Storage decisions. Each Owner must decide its own fields, invariants, interfaces and exceptions on its own branch.
- Purpose: Provide one reviewable cross-module candidate for the current PreparedParticipant / JF-10 / COC Gate B work, so the same participant identity and proof tuple is not independently reinterpreted by Storage, B, H, I, C, D and E.

## 1. Exact source bundle under review

| Artifact | Exact blob | Role / current status |
|---|---|---|
| A COC/JF-10 bridge architecture | a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d | Integration architecture; decisions with exceptions recorded. |
| Common JF-10 v2 protocol | 94679897e84a6f58fd8b9467b5249e1a885cb0b0 | Existing protocol; generic XID terminology requires alignment. |
| Phase 3.6.3 COC protocol with §14 | 86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7 | Storage accepts with conditions; A/H/I role reviews exist but are not independent; exact re-review pending. |
| Storage Design v2 | 4ed4234ce548a814a9496adf7a14c4459ea9f7ce | Current revised proposal; fresh exact Owner review required. |
| H JF-10 bridge schema candidate | a8a945cc3623c2907003b93625e3c79742150944 | Candidate only; current fields need explicit nominal mapping. |
| A prior COC acceptance matrix | 9a39e48a394fedbab16d15589056d59ef33f390f | Applies to prior COC protocol Blob 4ac63..., not automatically to 86ff3... or 4ed423.... |

This is a proposed canonical bundle, not a claim that all artifacts have already accepted one another. A must designate the normative relationship between the COC service protocol and Storage realization design. Until then, treat them as related but separately versioned review targets.

## 2. Candidate identity model

The following identifiers must be nominally distinct. They may be represented as opaque strings on the wire, but they must not be interchangeable in domain logic, signatures, logs or SQL calls.

| Type | Candidate meaning | Must not be confused with |
|---|---|---|
| PreparedParticipantRef | Stable engine-neutral cross-service participant identity for one prepared participant in one JF-10 operation. | DB-native XID, GID or a provider idempotency key. |
| PreparedTransactionGID | Client-chosen PostgreSQL prepared-transaction GID, allocated and durably bound before the COC prepare intent. | Numeric PostgreSQL native XID or PreparedParticipantRef. |
| NativeXidObserved | Engine-assigned native transaction identifier observed after authoritative PREPARE/readback; evidence only. | Stable participant identity or the identifier passed to COMMIT PREPARED. |
| DatabaseIncarnationRef | Governed, globally unique, non-reusable identifier for one database authority incarnation. | Database name, OID alone, host name, connection string or a restorable clone identity. |
| DBIdentity | Engine-specific identity tuple, including the cluster/system identifier and database identity/OID, plus the relevant timeline/LSN evidence. | DatabaseIncarnationRef; both are required for different purposes. |
| PrepareAttemptRef | Immutable identity for one durable prepare attempt. | Retry count alone or a mutable row ID reused across attempts. |
| PrepareAttemptGeneration | Monotonic generation/version for the participant's prepare-attempt ledger. | COC coordinator epoch or I authorization epoch. |

### 2.1 Candidate invariant

For one prepared participant:

- PreparedParticipantRef is stable across coordinator restart and participant recovery.
- PreparedTransactionGID is allocated once, durably bound to that participant and operation before COC prepare intent, and reused for every same-participant lookup, COMMIT PREPARED or ROLLBACK PREPARED attempt.
- NativeXidObserved is captured as database evidence after PREPARE; it is never used as the stable lookup key or as a replacement for PreparedTransactionGID.
- DatabaseIncarnationRef is never silently reused after clone, restore, reinitialization or authority replacement. The exact rotation/continuity policy is an I/Storage decision.
- A retry of the same PrepareAttempt is idempotent. A new attempt must be explicit, immutable and linked to the prior attempt; it must not silently overwrite the old participant record.
- OriginalPrepareCoordinates and RecoveryObservationCoordinates are distinct evidence objects. Recovery must not rewrite the original prepare time/timeline/LSN.

## 3. Candidate PreparedParticipantReceipt

Storage may issue a signed PreparedParticipantReceipt only after an authoritative database readback confirms that the exact PreparedTransactionGID is present as prepared in the expected DatabaseIncarnationRef and DBIdentity.

Candidate receipt payload:

| Field | Purpose / validation |
|---|---|
| receipt_version | Immutable schema/version identifier. |
| PreparedParticipantRef | Stable participant identity. |
| PreparedTransactionGID | Exact client-chosen GID used for PREPARE and all same-participant resolution. |
| NativeXidObserved | Native XID observed after PREPARE; evidence only. |
| DatabaseIncarnationRef | Non-reusable authority incarnation. |
| DBIdentity | Cluster/system identifier, database OID/identity and engine-specific incarnation evidence. |
| PrepareAttemptRef / PrepareAttemptGeneration | Immutable attempt identity and generation. |
| operation_digest | Canonical digest of the immutable operation/request tuple. |
| owner_boundary | Owner and policy/causal domain boundary for this participant. |
| original_prepare_coordinates | Original timeline/LSN/time and authoritative readback source. |
| coc_prepare_intent_position | Exact COC epoch/index/entry digest that admitted this participant. |
| observed_prepared_state | Explicit state and readback evidence proving the GID is prepared. |
| signer_identity / key_id / signature_profile | Exact signer and versioned verification profile. |
| receipt_digest | Digest over the canonical signed payload. |

The exact canonical byte format, signature suite, key custody, rotation and historical verification are I/H decisions. This table is not a signature-profile approval.

## 4. Candidate StorageResolutionProof

A StorageResolutionProof is a separate signed artifact proving a terminal database resolution for the same PreparedParticipantRef, PreparedTransactionGID and DatabaseIncarnationRef.

It should bind:
- terminal outcome: COMMITTED or ROLLED_BACK;
- exact PreparedParticipantReceipt digest;
- exact operation digest and owner boundary;
- exact COC terminal decision position/digest;
- exact database incarnation and DB identity;
- resolution observation coordinates and authoritative database readback;
- signer identity, key ID, signature profile and receipt digest.

A resolution proof must not be synthesized from a coordinator timeout, a client response, a COC state alone or an unverified pointer.

## 5. Candidate I terminal-decision binding

I remains the sole authorization/sequencer authority. COC may durably record I's signed decision, but must not decide policy, principal, permission epoch or revocation semantics.

A candidate I terminal decision binds in one durable I-owned transaction:
- exact PreparedParticipantRef;
- exact PreparedTransactionGID;
- exact DatabaseIncarnationRef and DBIdentity;
- exact PrepareAttemptRef/generation;
- exact operation digest and owner boundary;
- exact PreparedParticipantReceipt digest and signer/key identity;
- exact D fence/lineage proof and cutoff state;
- exact I policy/principal/permission epoch and revocation state;
- exact COC prepare-intent and commit-decision position/digest.

The transaction must ensure the I terminal decision and the consumption/acknowledgement of the exact Storage receipt cannot be split into two independently visible states. I must define the actual durable transaction boundary and recovery behavior.

Provider invocation is allowed only when both conditions are proven:
1. I has a durable, exact COMMIT_WON decision for this participant/operation; and
2. D's required ForgetFence/lineage predicates are satisfied for the same participant and owner boundary.

ABORT, UNKNOWN, IN_DOUBT, stale receipt, mismatched DB incarnation, missing D proof, or ambiguous I outcome must not authorize provider invocation. C owns provider idempotency and ambiguous side-effect recovery; COC must not infer provider success from a request or timeout.

## 6. Candidate COC / Storage recovery bundle

The COC service protocol and Storage realization design should be treated as a versioned pair with a canonical manifest.

The manifest must pin:
- COC protocol blob and version;
- Storage realization-design blob and version;
- A integration architecture blob;
- common JF-10 protocol blob;
- H BMCP schema blob and exact message-family mapping;
- B domain-type artifact;
- I policy/authorization/registry artifact;
- all exact Owner decisions and exceptions.

The manifest must define the normative precedence and map every Storage record to the COC RecordType and H BMCP message/schema. In particular, reconcile these Storage Design v2 records with the COC service protocol:
- COC_RECOVERY_CUTOFF_BATCH;
- PARTICIPANT_SET_RECONCILIATION;
- OWNER_LOCAL_GATE_RELEASE;
- RECOVERY_EPOCH_COMPLETED;
- I_JF10_TERMINAL_DECISION_OBSERVED;
- JF10_BRIDGE_RECONCILIATION_RECORDED.

The mapping must state whether each item is a quorum-committed COC record, an owner-local signed receipt, or an external proof reference. It must bind the same coordinator epoch/index, VoterConfigurationEpoch, entry digest and COCCommitReceipt/quorum proof. No record-name alias may silently change durability or authority.

### 6.1 Recovery batch and owner gates

Candidate invariants:
- Construct the full immutable participant manifest before committing the cutoff batch.
- Commit the cutoff batch and participant-set reconciliation as separate durable, quorum-committed records with exact count, digest/root, locator and high-water boundary.
- Requests arriving after a sealed owner high-water are not silently omitted; they require a subsequent cutoff batch or a proved out-of-scope result.
- An owner-local gate remains closed until all requests through its high-water are included and every required participant is resolved or explicitly exception-disposed.
- Each owner signs its own gate-release evidence. COC cannot impersonate I, D, C, G or Storage.
- RECOVERY_EPOCH_COMPLETED is emitted only after all required owner-local gate releases and reconciliation proofs are committed.
- A COC quorum loss or unknown commit result fails closed; no new protected provider admission may proceed without a committed prefix and required owner gates.

## 7. Candidate field mapping obligations

| Existing artifact | Current ambiguity | Required Owner action |
|---|---|---|
| Common JF-10 protocol Blob 9467... | Uses generic “preallocated XID” / “same XID” wording. | B/E/Storage define engine-neutral participant identity and Storage's PostgreSQL-specific GID/native-XID mapping. |
| Storage readiness §26.2 | Says “preallocate exact XID” without the GID/native-XID distinction. | Storage updates to PreparedTransactionGID plus separate NativeXidObserved and DB incarnation. |
| H schema Blob a8a9... | Has opaque preallocated_storage_xid_ref and storage_xid_ref fields. | H maps them to nominal types or introduces explicit fields; tests must reject field interchange and missing DB incarnation/receipt proof. |
| B typed-reference model | Does not yet define the new nominal types. | B owns the domain types and equality/identity semantics. |
| I security trust profile | H/I role reviews are CANDIDATE / NO APPROVAL. | I defines trust, key lifecycle, historical verification, revocation, replay and atomic receipt consumption; H defines canonical wire bytes. |
| Storage Design v2 Blob 4ed... | Contains GID/native-XID mapping but predates A's A-1..A-5 amendments. | Storage updates DatabaseIncarnationRef, PrepareAttempt, readback, original/recovery coordinates and I terminal proof consumption. |

## 8. Required negative and recovery tests

At minimum, the exact conformance plan should include:
1. GID reused for a different PreparedParticipantRef is rejected.
2. Same PreparedParticipantRef retried with same attempt is idempotent; a new attempt is explicit and immutable.
3. PreparedParticipantReceipt is rejected if PREPARED readback cannot find the exact GID in the expected DB incarnation.
4. A receipt from a different DatabaseIncarnationRef, DB OID/system identifier or owner boundary is rejected.
5. NativeXidObserved cannot be substituted for PreparedTransactionGID in lookup/COMMIT PREPARED/ROLLBACK PREPARED.
6. Original prepare coordinates and recovery observation coordinates cannot overwrite one another.
7. I terminal decision with wrong receipt digest, participant, GID, DB incarnation, operation digest or D proof is rejected.
8. ABORT, UNKNOWN or IN_DOUBT cannot trigger provider invocation.
9. Missing/invalid signature, unknown signer, revoked key, wrong audience/purpose or replayed receipt fails closed.
10. Recovery restore from an older anchor cannot re-enable a previously fenced participant or resurrect a stale receipt.
11. A missing participant in the recovery manifest prevents owner-local gate release.
12. A request arriving after owner high-water requires a subsequent cutoff batch; it cannot be omitted.
13. RECOVERY_EPOCH_COMPLETED cannot be committed before every required owner-local gate release.
14. COC quorum loss and ambiguous append result do not permit protected provider admission.
15. PITR/restart/failover preserves same-GID resolution semantics and separately records native-XID observations.

## 9. Owner decision matrix required

| Owner | Required decision |
|---|---|
| A | Canonical COC/Storage manifest, authority boundaries, record mapping and integration gate. |
| B | Nominal type semantics and identity/equality rules for PreparedParticipantRef, PreparedTransactionGID, NativeXidObserved, DatabaseIncarnationRef, DBIdentity and PrepareAttempt. |
| C | Provider idempotency, terminal outcome, ambiguous side-effect and no-invocation gates. |
| D | ForgetFence/lineage participant membership, cutoff, late-discovery and owner-local gate release semantics. |
| E | Compiler producer/participant registration, immutable operation tuple, retries and derivation dependencies. |
| F | Archive/Recall invalidation only where its contract consumes the relevant Forget/restore evidence; F does not own COC or Storage. |
| G | Applied consumption of exact recovery/owner-gate evidence; G does not own COC or Storage. |
| H | BMCP message family, strict nominal fields, canonical serialization, signature envelope and positive/negative wire tests. |
| I | PolicyDomain/CausalOrderDomain registry, authorization/sequencer, signature trust, key lifecycle, revocation, historical verification and atomic terminal receipt consumption. |
| Storage | DatabaseIncarnationRef lifecycle, durable PrepareAttempt ledger, pre-PREPARE GID binding, authoritative readback, prepared-XID/GID resolution, PITR/restore and signed receipts. |

## 10. Open decisions — do not infer

- Who owns and versions DatabaseIncarnationRef, including clone/restore/authority-replacement behavior.
- Which component owns the durable PrepareAttempt ledger and its generation/retention.
- Exact canonical signed-byte format, signature suite, key custody and historical verification.
- Whether OWNER_LOCAL_GATE_RELEASE is a COC quorum record or a separately signed owner-local receipt referenced by COC.
- Exact mapping between Storage Design v2 RecordTypes, COC protocol RecordTypes and H BMCP messages.
- Whether VoterConfigurationEpoch and COCCommitReceipt are inherited from the COC protocol or repeated in each Storage-facing proof.
- I-owned PolicyDomain/CausalOrderDomain registry semantics and revocation/change authority.
- External monotonic anchor custody and failure-domain independence.
- Multi-PolicyDomain atomicity remains BLOCKED; this proposal covers only the single-I-PolicyDomain profile.

## 11. Current non-claims

- This proposal is not accepted by A/B/C/D/E/F/G/H/I/Storage.
- It does not update any Owner branch, schema, protocol or implementation.
- It does not select PostgreSQL or any final production database.
- It does not close JF-10 P0, Gate A, Gate B implementation, Gate C, Global Forget, ADR-001 or project G0.
- It does not authorize provider invocation, production activation, schema freeze or architecture freeze.

