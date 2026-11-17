# Phase 3.6.7 — D Owner-Local Forget Gate, Admission Inventory & Independent Release

- Owner perspective: D — Memory Brain / Forget Authority
- Status: **OWNER-BRANCH SEMANTIC AMENDMENT CANDIDATE — INDEPENDENT D REVIEW REQUIRED**
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 1. Authority boundary

D alone owns Forget request registration, ForgetFenceGeneration, affected producer/work admission, lineage closure, barrier membership and D Gate release. I owns global policy/permission Gate and global Producer/Recipient inventory membership. COC records typed order and recovery evidence; it does not mint D Fence or D Release. Storage proves its own prepared participant and visibility outcome; it does not decide D clearance.

This amendment is scoped to the current Storage Design v3.1 Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca` and COC companion Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d`. Storage Design v2 Blob `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` is retained as historical predecessor only; it lacks the §§15.1–15.7 required by the current COC protocol.

## 2. Atomic D Gate linearization

### 2.1 Required primitive

D MUST implement one linearizable durable transaction (or formally equivalent single-writer CAS over a durable append-only state machine) that atomically:
1. authenticates and normalizes ForgetOperationRef, request digest, canonical target, PolicyDomainRef and Scope;
2. advances monotonic `ForgetFenceGeneration` for the affected scope;
3. closes affected Producer/Derivative/Queue/Recall/Context/Restore publication and admission paths;
4. appends the Forget request and all currently admitted affected WorkItem/Attempt membership to the D In-flight Admission Ledger;
5. captures D-local producer registration high-water, WorkItem/Attempt high-water and exact barrier-membership root/count;
6. persists an independent anti-rollback anchor and returns a D-signed `DGateCloseAttestation`.

The **linearization point** is the durable commit/CAS at which FenceGeneration, closed admission state, request record, ledger high-waters and barrier membership become visible together. Before that point the request is not acknowledged as fenced. After it, every affected admission and publication path must observe the new FenceGeneration and closed state.

A separate “write fence then scan queues”, process mutex, cache invalidation, COC append or queue pause is not an atomic gate.

### 2.2 Racing admission/publication rule

For each racing WorkItem:
- If its D admission transaction linearizes before the Fence close, it is in the captured pre-fence inventory and barrier.
- If it linearizes after the Fence close, it is rejected or admitted only into a non-publishing suppression/cleanup lane; it cannot publish into the covered lineage.
- If the system cannot establish which side won, it is UNKNOWN and the Gate remains closed.

Producer registration, WorkItem admission, Derivative creation/registration, queue dispatch, recall/context materialization, restore and final publication must all check the same current FenceGeneration at their own authoritative boundary. A pre-fence receipt cannot authorize post-fence publication.

## 3. In-flight Admission Ledger — mandatory inventory

D's ledger MUST include every affected operation from before durable WorkItem registration through final visibility/terminalization, including work that has not yet produced a COC participant.

Minimum fields:
- `ForgetOperationRef`, request ID/digest, canonical target identity, normalized ScopeRefs, PolicyDomainRef and scope-binding fingerprint;
- `ForgetFenceGeneration`, D gate ref/state, D-local request sequence, ledger ref/version, anti-rollback anchor;
- I-authorized global `InventoryEntryRef`, `InventoryEntryGeneration`, PolicyDomainRef and scope binding for Producer/Transformer/Recipient roles;
- D's local producer projection version and registration contract version (not global membership authority);
- `ProducerClassRef`, `WorkItemId`, `AttemptRef`, `LeaseGeneration`, retry/replay ancestry and worker/queue identity;
- source object, canonical target, parent/child/derivative refs, lineage edges and dependency-closure refs/digests;
- Queue/Recall/Context/Restore/Derivative admission refs and visibility/publication destination;
- admission phase and timestamps for audit only;
- D registration high-water, WorkItem high-water, barrier-membership generation/root/count;
- COC ParticipantIntentRef/OperationId/position/digest if registered; explicit null with reason if not yet registered;
- Storage PreparedParticipantRef/GID/PrepareAttemptRef/ParticipantLedgerVersion if applicable;
- I receipt/decision refs if applicable;
- terminalization proof, cancellation/no-output proof, quarantine/suppression proof or unresolved reason.

Mandatory in-flight classes:
1. Producer registered but no WorkItem yet;
2. WorkItem admitted but not dispatched;
3. queued, leased, running, retrying, replayed or worker-restarted work;
4. producer output created but Derivative not yet registered;
5. Derivative registered but not yet visible;
6. recall/context materialization in progress;
7. restore/replay work and restored queue entries;
8. COC prepare intent not yet registered or COC ACK lost;
9. Storage PREPARE in progress or prepared participant not yet reflected in D/COC projection;
10. publication transaction started, ACK lost or result uncertain;
11. post-fence late-discovered producer/work/lineage;
12. cancelled, suppressed, quarantined or failed work awaiting authoritative no-publish terminal evidence.

Queue emptiness, worker absence, expired lease, timeout, DLQ movement, missing COC intent or missing Storage row is not proof that no work exists.

## 4. D cutoff and barrier manifest

D creates an immutable `DInFlightAdmissionSnapshot` bound to:
- exact ForgetOperationRef, normalized request digest, PolicyDomainRef and Scope;
- FenceGeneration and atomic fence-installation cursor;
- I-sourced registry projection snapshot ref/digest, entry generations and scope mapping;
- D producer registration high-water, WorkItem/Attempt high-water;
- canonical ordered barrier member refs, count and root;
- dependency closure digest/cursor/generation;
- per-member admission phase, publication boundary and terminal status;
- COC prefix/batch/manifest refs once available;
- anti-rollback anchor, signer/key version and snapshot generation.

The COC Recovery Cutoff Batch carries D's attestation as an opaque typed owner snapshot. I's request high-water is separate and incomparable.

D must reconcile the local ledger against producer/queue/worker/derivative/restore/Storage projections and include items without COC registration. If a producer or work item is discovered after snapshot that could have existed before the Fence, D reopens the barrier, invalidates the affected closure proof and produces a new snapshot generation while keeping the Fence closed.

## 5. Terminalization and independent D Release conditions

D may release only its outage/pending Gate (not the Forget Fence itself) through a D-signed monotonic `DGateReleaseReceipt` when ALL conditions hold:

1. Exact COC RecoveryEpoch, prefix, Recovery Cutoff Batch and participant manifest are linearly verified and match D's attestation.
2. Every D request at/below the captured high-water is represented exactly once.
3. Every affected pre-fence ProducerClass/WorkItem/Attempt/Derivative/Queue/Recall/Context/Restore member is in the barrier manifest, including unregistered in-flight work.
4. Every barrier member has an authoritative terminal disposition: `PUBLISHED_BEFORE_FENCE` with exact publication evidence; `CANCELLED_NO_OUTPUT`; `SUPPRESSED_QUARANTINED`; or `FAILED_PARKED_NO_PUBLISH`. UNKNOWN, timeout, expired lease, missing worker or absent queue row is non-terminal.
5. Dependency closure is complete and current; every descendant, derivative, onward publication and Storage-visible artifact is accounted for.
6. Every I receipt/decision and Storage prepared participant affecting a member is reconciled by exact typed refs and tuple digests; D does not infer I terminality or Storage resolution.
7. No late producer, late derivative, unregistered WorkItem, restore rollback, lineage mismatch or post-fence publication exists. Any such discovery reopens the barrier and invalidates the affected proof.
8. FenceGeneration, D request high-water, producer/work high-waters, barrier generation and anti-rollback anchor remain current and monotonic.
9. Post-high-water work has been rejected or placed in a non-publishing suppression lane; it is not silently merged into the already sealed batch.
10. No unknown target, scope, owner, recipient, dependency or publication destination remains within D's responsibility.

The D Release receipt binds exact RecoveryEpoch, COC prefix/batch/manifest digests, ForgetOperationRef, FenceGeneration, D request high-water, producer/work high-waters, barrier membership root/count, dependency-closure digest/cursor, reconciliation root and signer/key version.

### 5.1 Outage Gate Release is not Forget effectiveness

D outage Gate release only ends the temporary COC-outage admission suspension. It does not:
- decrement or clear ForgetFenceGeneration;
- reopen producer publication for covered lineage;
- declare global Forget completion;
- prove external Recipient/Backup deletion or physical erasure;
- substitute for I global inventory completeness or authorization;
- resolve Storage XIDs or make bytes visible;
- release I's Gate or COC's recovery Gate.

The effective Forget Fence/barrier remains in force until D's separate Forget completion protocol proves all required D predicates. Global completion additionally requires I's inventory/recipient/backup evidence and any other accountable owner proofs.

## 6. Reopen and invalidation

- FenceGeneration is monotonic and never rolled back by recovery.
- New pre-fence work discovered after snapshot reopens the affected barrier and invalidates its closure/snapshot proof.
- New post-fence work is rejected or suppression-only; if it can publish, treat as a safety violation, quarantine it and reopen the barrier.
- A changed I registry entry generation invalidates D's affected producer projection mapping and requires refresh/reconciliation. D cannot create global membership entries.
- A D closure proof can be invalidated by newly discovered D work/lineage or contradiction. An I inventory epoch advance alone does not automatically invalidate unrelated D closure unless it changes the relevant membership mapping or reveals omitted D work.
- Restore begins with D Gate closed and replays current Fence/Barrier control state before any protected publication or context serving.
- Only D can issue a new D Gate Release receipt.

## 7. Required conformance evidence and status

Required tests (not run): admission racing Fence CAS; producer registration vs high-water; derivative created before/after fence; queue lease expiry; worker restart; COC outage with pre-existing unregistered WorkItem; Storage prepared participant missing from COC projection; late producer discovery; restore rollback; barrier release with UNKNOWN member; attempted post-fence publication.

**Disposition:** proposed D semantic amendment. It is not an independent D Owner approval, implementation PASS, physical erasure proof, global Forget completion or production activation.
