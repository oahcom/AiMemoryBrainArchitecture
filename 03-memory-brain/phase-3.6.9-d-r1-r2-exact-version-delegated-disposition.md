# Phase 3.6.9 — D Exact-Version R1/R2 Owner Disposition

- Role: D — Memory Brain / Forget Authority
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Scope: D ForgetFence, work admission, lineage/barrier membership, publication fencing and D outage-gate release
- Provenance: **delegated role simulation authored in the coordinating ChatGPT session at the user's direction; not an independent human Owner signature or cryptographic attestation**
- Status: architecture proposal only; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED

## Exact review bundle

| Source | Blob |
|---|---|
| A Phase 3.6 architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H recovery wire contract | `707ed85642ba4b0275c4ec851d599fde28ec6cae` |
| H recovery schema 1.0.3 | `9c3b98abab0c04a241a93c5e6f02e9424059b07b` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |


## R1 — D work and lineage completeness

D accepts the Phase 3.6.8 D snapshot and typed reconciliation tuple. D owns ForgetOperationRef, FenceGeneration, D producer/work/attempt high-waters, barrier membership, dependency closure, D terminalization and D outage-gate release. I remains the authority for global producer/recipient/backup/export/restore inventory membership.

D requires separate evidence for:
- D request ledger and fence generation;
- producer registration and work/attempt inventories;
- derivative/descendant and dependency closure;
- exact I registry epoch/digest/relevant entry-generation projection;
- COC committed-prefix ParticipantManifest;
- Storage prepared participant and publication/no-publication evidence where applicable.

A new I inventory entry or late-discovered pre-fence producer/work item reopens the affected barrier if it could have produced omitted work or lineage. Empty queue, missing worker, expired lease, absent COC row or zero count is never proof of an empty set.

## R2 — D Fence linearization

D accepts one durable D-local transaction/CAS that atomically advances ForgetFenceGeneration, closes affected admission/publication gates, appends the request and captures D request/producer/work/attempt high-waters and barrier membership.

The same current FenceGeneration and exact scope/lineage check MUST be enforced at every authoritative effect boundary: producer registration, work creation, queue dispatch/lease, worker start/retry/replay, derivative registration, recall/context materialization, restore replay and final visibility publication. Final publication compare-and-commit is mandatory; a worker lease or cached generation is not a publication capability.

If a boundary cannot reach the authoritative D fence or enforce a valid generation token in the final effect transaction, it must fail closed and keep output private/quarantined. Unknown order is UNKNOWN, never wall-clock inferred.

## Enumerated amendments / conditions

1. H snapshot roots must bind distinct D request and admission sets, with D-specific producer-registration/work-item/attempt/barrier high-waters.
2. D's I registry projection must bind exact ProducerDomainInventoryEpoch, registry digest and relevant entry generations; D cannot infer global inventory completeness.
3. Every barrier member needs terminal evidence tied to exact WorkItem/Attempt/Lease, lineage, destination and publication/no-publication proof.
4. A stale publication after FenceGeneration is a safety violation: quarantine/withdraw visibility, preserve evidence, reopen the barrier and block release.
5. D outage-Gate Release remains distinct from effective Forget Fence completion, D local completion, Global Forget Completion and physical erasure.
6. C's egress attempt state and Storage's same-XID resolution must be joined before D can terminalize a protected participant.

## D disposition

D's R1/R2 owner-local architecture is conditionally acceptable with these amendments. This does **not** close A's R1/R2 findings: exact H/COC joins, C adapter proof and A integration remain required. No physical erasure, implementation conformance, deployment or production activation is approved.
