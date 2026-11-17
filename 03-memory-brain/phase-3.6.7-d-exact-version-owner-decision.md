# Phase 3.6.7 — D Exact-Version Owner Decision

- Decision authority represented: D — Memory Brain / Forget Authority
- Decision class: exact-blob semantic review of the Phase 3.6.7 D Gate / Admission / Release amendment
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Decision scope: architecture semantics only; no implementation or production approval
- Reviewed D amendment commit: `1426822b05fa5ad4f3ea19dd40ee10fd93f9c059`
- Reviewed D amendment blob: `84f6875ce382fb37f35b01140c19a482fcfa9fab`
- Companion Storage Design v3.1 blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- Companion COC protocol blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- I owner-local Gate amendment reviewed alongside: `0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7`
- Historical Storage Design v2 blob: `4ed4234ce548a814a9496adf7a14c4459ea9f7ce` (not current companion)

## 1. Exact-version disposition

D accepts the reviewed Phase 3.6.7 D amendment as the correct owner-local semantic direction for:
- D-only ForgetFenceGeneration, affected work admission and publication suppression;
- atomic capture of D request, producer/work high-waters and barrier membership;
- mandatory inventory of pre-fence producers, WorkItems, attempts, derivatives, queues, recall/context, restore and Storage/COC in-flight work;
- explicit terminalization and reopen/invalidation semantics;
- D-only outage-Gate Release, distinct from the continuing effective Forget Fence and global Forget completion.

This is **not unconditional acceptance**. The exact blob is accepted only with the mandatory amendments below. The reviewed blob remains immutable; amendments MUST be published as a new append-only revision and reviewed by exact blob.

## 2. Mandatory amendments before D semantic freeze

### D-M1 — Atomicity across all admission and publication boundaries

A D-local database transaction cannot by itself atomically mutate every producer, queue, worker, recall/context and restore subsystem. Specify the enforceable fencing protocol:
- a single authoritative D Gate/Fence generation and durable close record;
- every affected admission and publication boundary must validate the current generation using a linearizable read, lease/fencing token or equivalent;
- a worker holding a stale pre-fence lease cannot publish after Fence linearization;
- the final visibility/publication transaction must atomically compare the current FenceGeneration and commit the effect, or leave the output private/quarantined;
- partitions or inability to validate the generation fail closed.

Without this protocol, "close all paths" is an intended property, not a proven atomic operation.

### D-M2 — Exact I global registry mapping and currentness

D's snapshot must bind the I-authorized Producer/Transformer membership projection using:
`InventoryEntryRef + InventoryEntryGeneration + PolicyDomainRef + ScopeBindingFingerprint ↔ ProducerClassRef + DRegistrationContractVersion`.

It must include the exact I ProducerDomainInventoryEpoch and registry snapshot digest. Before D release, D must revalidate relevant I epoch/entry generations. An epoch advance only invalidates D evidence if the affected membership mapping changes or reveals omitted D work, but D must prove that unaffected relevant entries remain current.

### D-M3 — Joint D/I/COC reconciliation tuple

Every D snapshot, barrier closure and release must bind the same typed reconciliation attempt:
- ForgetOperationRef and normalized request digest;
- PolicyDomainRef and exact Scope binding;
- D FenceGeneration, fence cursor, producer/work high-waters, barrier root/count and closure digest/cursor;
- I ProducerDomainInventoryEpoch, registry snapshot digest, relevant entry generations and I request Gate generation/high-water;
- COC RecoveryEpoch, exact prefix, Recovery Cutoff Batch and participant manifest digests;
- Storage PreparedParticipantRef, tuple digest, GID, DB incarnation, prepare attempt and ledger version for applicable members;
- reconciliation attempt generation and canonicalization/schema profile.

D and I local sequence numbers remain owner-local and must never be numerically compared or collapsed into one global counter.

### D-M4 — Terminalization must bind publication and restore evidence

For each barrier member, terminal proof must bind WorkItem/Attempt/LeaseGeneration, producer/derivative lineage, exact publication destination and visibility receipt or no-publish proof. Restore members must additionally bind RestoreAttemptRef/checkpoint generation and prove that restored queue/context state cannot replay pre-fence work into serving paths. A status enum without source evidence/digest is insufficient.

### D-M5 — Release and Forget completion are separate gates

Define two explicit transitions:
1. D outage-Gate Release: ends temporary outage admission suspension only, after complete recovery inventory and COC reconciliation.
2. D Forget Barrier/Completion: retains the effective Fence and suppresses covered lineage until all D terminalization, dependency closure and required I recipient/backup evidence are complete.

The D outage release receipt must not be accepted by any serving/publication path as permission to clear the Forget Fence. Global completion remains dependent on I's GlobalInventoryCompletenessProof and all other accountable Owner evidence.

### D-M6 — Late discovery and post-fence safety proof

Specify deterministic handling for:
- producer registered globally in I but missing from D projection;
- producer discovered after snapshot with evidence it existed before Fence;
- post-Fence producer attempt or derivative;
- a publication whose commit time/order relative to Fence cannot be proven;
- Restore rollback or a stale worker publishing after Fence.

Pre-fence discovery reopens the barrier and invalidates closure proof. Post-fence publication is a safety violation: quarantine output, preserve evidence, reopen affected barrier and block release. Unknown order is UNKNOWN, never inferred from wall-clock timestamps.

## 3. D-owned atomicity and in-flight admission decisions

D confirms its linearization point must atomically persist FenceGeneration, closed admission state, Forget request, local ledger high-waters and exact barrier membership. Every racing WorkItem must either be included as pre-fence or rejected/suppression-only as post-fence; unresolved order blocks release.

The D in-flight inventory must include at least:
- producer registered but no WorkItem;
- admitted but undispatched WorkItem;
- queued/leased/running/retrying/replayed/worker-restarted work;
- output created before derivative registration;
- registered but not visible derivative;
- recall/context materialization;
- restore and queue replay;
- COC intent missing or ACK lost;
- Storage PREPARE/prepared participant not yet reflected in D/COC;
- publication transaction started or ACK lost;
- late-discovered producer/work/lineage;
- cancelled/suppressed/quarantined/failed work awaiting authoritative no-publish proof.

Queue emptiness, worker absence, expired lease, timeout or missing COC row is not terminal evidence.

## 4. Independent D Release rule

D may issue `DGateReleaseReceipt` only after:
1. exact COC RecoveryEpoch/prefix/batch/manifest verified;
2. all D requests through captured high-water reconciled;
3. complete pre-fence barrier membership including unregistered work;
4. authoritative terminal evidence for every member;
5. current dependency closure and no unaccounted descendant/publication;
6. exact I receipt/decision and Storage participant tuple reconciliation;
7. current relevant I registry epoch/mapping and shared tuple per D-M2/D-M3;
8. no late producer, post-fence publication, restore rollback or unknown ordering;
9. FenceGeneration, high-waters and anti-rollback anchor remain current;
10. all post-high-water work rejected or suppression-only.

UNKNOWN, timeout, expired lease, lost ACK, missing worker, incomplete lineage, stale I mapping or unresolved Storage participant blocks D release. Only D releases D outage Gate. The effective Forget Fence is not cleared by this release.

## 5. Non-negotiable authority boundary

- D alone issues Forget Fence, barrier closure and D outage-Gate Release evidence.
- I alone owns global membership/registry, permission and recipient/backup completeness evidence.
- Storage alone attests prepared participant durability and visibility outcome.
- COC persists typed ordering/evidence but cannot mint D/I/Storage proof.
- A integration acceptance cannot substitute for D's owner-local terminalization.

## 6. Final decision

**ACCEPT WITH ENUMERATED AMENDMENTS** for the exact reviewed D amendment blob `84f6875...`, subject to D-M1 through D-M6. No semantic freeze until these are incorporated and exact-version re-reviewed.

Not approved: implementation conformance, physical erasure, global Forget completion, production activation, or release of any live Gate.

## 7. Authorship and provenance

This is a delegated role-based architectural decision record prepared in this ChatGPT session and committed to D's working branch at the user's direction. It is not a cryptographic signature or proof that a separate human D Owner independently authored or approved it. Treat it as a proposed D decision for governance review, not independent human sign-off.
