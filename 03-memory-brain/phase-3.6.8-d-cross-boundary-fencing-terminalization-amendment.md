# Phase 3.6.8 — D Cross-Boundary Fencing, Barrier Terminalization & Late-Discovery Amendment

- Owner perspective: D — Memory Brain / Forget Authority
- Status: **PROPOSED OWNER-LOCAL AMENDMENT — EXACT-VERSION D RE-REVIEW REQUIRED**
- Supersedes: none; append-only refinement of Phase 3.6.7
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 0. Exact-version lineage and normative bundle

This amendment is a new revision responding to D's Phase 3.6.7 decision. It does not modify the reviewed source blob or its decision record.

- Phase 3.6.7 D source commit: `1426822b05fa5ad4f3ea19dd40ee10fd93f9c059`
- Phase 3.6.7 D source blob: `84f6875ce382fb37f35b01140c19a482fcfa9fab`
- Phase 3.6.7 D exact-version decision commit: `825a6af968bee11d33e77557da901423ac2f1bcc`
- Phase 3.6.7 D decision blob: `3603aff5881dd8a375f22aad67b90ade312bbfad`
- Phase 3.6.7 I companion source blob: `0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7`
- Phase 3.6.7 I decision blob: `325cd63164c217f8712964da58509f867d105740`
- Current Storage Design v3.1 blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- Current COC protocol blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Historical Storage Design v2 blob (not current companion): `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`

Normative pairing is Storage Design v3.1 + COC protocol 8ac178. Storage v2 is historical only.

## 1. Authority and non-collapsible state

D alone owns ForgetOperation semantics, ForgetFenceGeneration, affected WorkItem admission, lineage barrier membership, dependency closure, D terminalization and D outage-Gate release. I alone owns global Producer/Recipient/Backup/Export/Restore membership and ProducerDomainInventoryEpoch. Storage alone attests prepared participant identity/durability/visibility. COC persists ordered evidence and recovery batches. None may mint another owner's proof.

The following remain distinct typed values: D FenceGeneration and D-local high-waters; I ProducerDomainInventoryEpoch, registry digest/entry generations, IGateGeneration and IRequestHighWater; COC RecoveryEpoch/prefix/batch/manifest; Storage PreparedParticipant/GID/DB incarnation/native XID/attempt/ledger; RestoreAttempt/checkpoint; reconciliation attempt generation. Do not compare owner-local counters or infer a global atomic snapshot.

## 2. D-M1 — Enforceable fencing at every admission and publication boundary

### 2.1 D fence authority and linearization

D's owner-local durable transaction/CAS atomically persists ForgetOperationRef/request digest, FenceGeneration increment, D Gate closed state, local request/producer/work high-waters, exact barrier membership root/count and anti-rollback anchor. This is the D control-plane linearization point only; it does not magically atomically mutate every external queue, worker or publication subsystem.

### 2.2 Required boundary protocol

Every affected boundary MUST enforce a current D fence using one of:
- linearizable read of authoritative D FenceGeneration at the boundary;
- a signed, bounded lease/fencing token whose generation is compared by the final authoritative effect transaction;
- a formally equivalent monotonic fencing primitive with proof that stale generations cannot commit.

This applies independently to Producer registration/admission, WorkItem creation, queue dispatch/lease acquisition, worker start/retry/replay, Derivative creation/registration, Recall/Context materialization, Restore queue replay and final publication/visibility.

The final publication/visibility transaction MUST atomically compare the current FenceGeneration and exact scope/lineage authorization with the generation carried by the WorkItem/Attempt/Lease. If the generation is stale, the transaction aborts and the output remains private/quarantined; no externally visible pointer, serving index, context item or derivative is published.

A worker's pre-fence lease is not a post-fence publication capability. Lease expiry, worker restart or queue redelivery requires fresh generation validation. A process-local cache or best-effort invalidation is insufficient.

### 2.3 Partition and uncertainty behavior

If an admission/publication boundary cannot reach the authoritative fence source and has no still-valid fencing token that the final effect transaction enforces, it MUST fail closed. It may persist private work for later reconciliation but may not publish, serve, expose or create a visible derivative. Unknown generation/order is UNKNOWN, never inferred from wall-clock time.

## 3. D-M2 — Bind I global registry projection and prove currentness

D does not own global Producer membership. For each relevant I inventory entry, D records a projection mapping:

`InventoryEntryRef + InventoryEntryGeneration + PolicyDomainRef + ScopeBindingFingerprint ↔ ProducerClassRef + DRegistrationContractVersion`

The D snapshot binds the exact I ProducerDomainInventoryEpoch and registry snapshot digest, plus all relevant entry generations and scope mappings. D records source authority and mapping provenance; it cannot create or repair an I global membership entry.

Before D barrier closure or D outage-Gate release, D MUST obtain/validate current I evidence for the relevant entries and epoch. If the epoch advanced, D determines whether relevant mappings changed or a previously omitted producer/work item was exposed. D may preserve an unaffected closure only with positive proof that all relevant entries and mappings remain current and that the new epoch did not reveal omitted D work. An epoch advance alone is not numerically compared with D counters; absence of current I evidence means UNKNOWN and blocks release.

A newly discovered I entry mapped to this PolicyDomain/scope reopens the affected D barrier if it could have produced pre-fence work or lineage not represented in the D snapshot.

## 4. D-M3 — Typed shared reconciliation attempt

Every D snapshot, terminalization proof, barrier closure and release receipt binds a `DReconciliationTuple`:
1. ForgetOperationRef, normalized request digest, PolicyDomainRef and ScopeBindingFingerprint;
2. D Gate ref, FenceGeneration, fence installation cursor, producer registration high-water, WorkItem/Attempt high-water, barrier root/count/generation and dependency-closure digest/cursor;
3. I ProducerDomainInventoryEpoch, registry digest, relevant InventoryEntryRef/Generation mapping, I Gate generation and I request high-water/root where relevant;
4. COC RecoveryEpoch, exact prefix, Recovery Cutoff Batch identity/digest and participant-manifest identity/digest;
5. Storage PreparedParticipantRef, PreparedTransactionGID, DatabaseIncarnationRef, PostgreSQLNativeXID where known, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, ParticipantTupleDigest, PublicationOperationId, RequestDigest, owner boundary and COC PrepareIntent position/digest where applicable;
6. RestoreAttemptRef/checkpoint generation and anti-rollback anchor where applicable;
7. reconciliation attempt generation, schema version and canonicalization profile.

Each owner signs its own authoritative subrecord. The tuple is a join/reconciliation envelope, not a globally atomic cross-owner snapshot. Any missing or contradictory owner subrecord is UNKNOWN. Owner-local counters are not compared or collapsed.

## 5. D-M4 — Terminalization proof binds work, publication and restore

Every barrier member must have a typed terminal proof bound to:
- WorkItemRef, AttemptRef, LeaseGeneration and source ProducerClassRef;
- exact pre-fence admission generation and D FenceGeneration;
- producer/derivative parent-child lineage and dependency closure;
- exact publication destination, visibility pointer/index/context destination and publication operation identity;
- authoritative visibility receipt for a proven pre-fence publication, or a source-backed no-publish/cancel/suppress/quarantine proof;
- COC evidence position/digest and Storage participant tuple when applicable;
- terminal proof generation, signer/authority and immutable evidence digest.

Permitted dispositions are not merely status strings:
- `PUBLISHED_BEFORE_FENCE`: requires authoritative publication commit proof ordered before the D fence linearization point, exact destination and visibility evidence;
- `CANCELLED_NO_OUTPUT`: requires proof no output/derivative escaped and all attempts are terminal;
- `SUPPRESSED_QUARANTINED`: requires output identity, quarantine location, suppression enforcement and proof it is not served;
- `FAILED_PARKED_NO_PUBLISH`: requires all attempts terminal and authoritative proof no publication/visibility effect occurred.

Missing ACK, empty queue, absent worker, expired lease, timeout, DLQ status or missing COC row is not terminal proof.

Restore terminalization additionally binds RestoreAttemptRef, checkpoint generation/digest, restored queue/context snapshot and replay manifest. Before serving, restored queue/context state must reapply the current D FenceGeneration and prove no pre-fence WorkItem can be replayed into a serving/publication path. A restore attempt with uncertain rollback/fork is UNKNOWN and blocks release.

## 6. D-M5 — Two distinct transitions: outage release vs Forget completion

### 6.1 D outage-Gate Release

This transition ends only the temporary D outage/admission suspension after COC recovery inventory, D in-flight ledger, I projection, Storage participant joins and exact recovery batch are reconciled. It is represented by a D-signed `DGateReleaseReceipt` bound to the current DReconciliationTuple.

The receipt is explicitly typed `OUTAGE_ADMISSION_RELEASE_ONLY`. No producer, worker, queue, recall/context, restore or publication path may interpret it as permission to clear or bypass an effective Forget Fence.

### 6.2 Forget Barrier/Completion

The effective Forget Fence and lineage suppression remain in force until D separately proves all D terminalization, descendant/dependency closure, no-publication requirements and relevant current I/Storage/COC evidence. D's Forget completion proof is a different proof type, generation and state transition; it cannot be derived from DGateReleaseReceipt.

Global Forget Completion additionally requires I's GlobalInventoryCompletenessProof and recipient/backup/export/restore-domain evidence plus all other accountable Owner proofs. Neither D outage release nor D local completion alone means global completion or physical erasure.

## 7. D-M6 — Late discovery, publication race and post-fence safety

D handles each case deterministically:

1. **I registry entry omitted from D projection**: fetch current I authoritative entry and generation; determine scope/producer mapping. If it could have produced pre-fence work, reopen affected barrier, extend membership, invalidate closure and re-run reconciliation.
2. **Producer discovered after snapshot but existed before Fence**: classify as pre-fence late discovery; append evidence, reopen barrier, invalidate snapshot/closure and include all related WorkItems/derivatives/attempts.
3. **New producer/work after Fence**: reject admission or place it in a suppression-only non-publishing lane. Any visible output is a safety violation.
4. **Publication order relative to Fence cannot be established**: classify UNKNOWN; quarantine/private the output, preserve source evidence, reopen barrier and block release. Wall-clock timestamps are not ordering proof.
5. **Stale worker publishes after Fence**: treat as post-fence safety violation; immediately quarantine/withdraw visibility through the authoritative publication owner, preserve immutable evidence, invalidate affected closure and block D release until remedied and re-proven.
6. **Restore rollback/fork replays stale work**: keep D Gate closed, restore current FenceGeneration/anti-rollback anchor, quarantine replayed outputs and rebuild the restore/barrier snapshot. No serving before currentness validation.
7. **Post-high-water discovery with proven post-fence origin**: keep it outside the sealed batch and suppression-only; it cannot be silently merged into the old barrier snapshot. If its ancestry/order is uncertain, UNKNOWN and reopen.

A safety violation cannot be converted to success by deleting the evidence or by advancing a high-water. FenceGeneration never rolls back.

## 8. D release decision algorithm

D may issue DGateReleaseReceipt only after:
1. exact COC RecoveryEpoch/prefix/Recovery Cutoff Batch/participant manifest match;
2. D request and work ledgers complete through captured high-waters;
3. complete pre-fence barrier membership, including unregistered work and current I registry projection;
4. every barrier member has authoritative terminal proof under §5;
5. dependency closure current and no unaccounted descendant/publication;
6. all I receipts/decisions and applicable Storage tuples join exactly;
7. current I epoch/registry mapping and D FenceGeneration/high-waters/anti-rollback anchor revalidated;
8. RestoreAttempt/checkpoint/replay proof current where applicable;
9. no late discovery, post-fence publication, rollback, unknown order, lost ACK or unresolved participant;
10. all post-high-water work rejected or suppression-only.

Only D releases D outage Gate. The effective Forget Fence remains. Any failed currentness check restarts reconciliation or leaves Gate closed; no partial/optimistic release.

## 9. Required conformance cases — specified, not executed

- stale worker lease attempts publication after FenceGeneration increment;
- publication transaction loses race against Fence CAS;
- partitioned queue/worker cannot validate current generation;
- I registry epoch advances without relevant entry change;
- I epoch reveals omitted producer mapping;
- D closure proof attempted without exact I currentness evidence;
- derivative exists before registration and is discovered late;
- publication ACK lost with uncertain visibility outcome;
- Restore replays a pre-fence queue item;
- post-fence visible publication is detected and quarantined;
- unknown publication/fence order;
- D outage receipt presented as permission to clear Forget Fence;
- exact Storage tuple mismatch or COC participant-manifest mismatch.

**Disposition:** Phase 3.6.8 D proposed amendment incorporating D-M1 through D-M6. Exact-blob D re-review is required. No implementation PASS, physical erasure, production activation or Global Forget Completion is claimed.

## 10. Provenance

This document is an assistant-authored role-based proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human D Owner authorship or approval.
