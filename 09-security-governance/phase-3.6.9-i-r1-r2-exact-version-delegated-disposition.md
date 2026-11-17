# Phase 3.6.9 — I Exact-Version R1/R2 Owner Disposition

- Role: I — Security & Governance Architect
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Scope: I-owned revocation/permission gate, receipt issue/consume, global inventory currentness and I outage-gate release
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


## R1 — I request and inventory completeness

I accepts the Phase 3.6.8 I-local request snapshot and the typed reconciliation tuple as the correct authority split. I owns its request ledger, IGateGeneration, PermissionEpoch, ProducerDomainInventoryEpoch, registry snapshot/entry generations, TargetInventorySeal and I Gate Release.

I requires two separately proven completeness domains:
1. I request/receipt issue/consume ledger through exact IRequestHighWater.
2. I global inventory membership through exact ProducerDomainInventoryEpoch, registry digest, relevant entry generations and TargetInventorySeal.

Neither can substitute for the other. The H 1.0.3 schema's separate request_members and admission_members are necessary but structural only. I will issue no completeness or release proof unless its ledger sources, counts, canonical roots, explicit COMPLETE_EMPTY states and current registry generations are independently verified.

I accepts that the COC ParticipantManifest is a separate prefix-complete set. The batch join must map every REGISTERED I entry to its exact participant identity/digest and account for every relevant pre-batch participant. NOT_REGISTERED I entries remain owner-local obligations; no fabricated ParticipantIntentRef is permitted.

## R2 — I Gate linearization

I accepts one durable I-sequencer transaction/CAS as the I gate-close linearization point. The transaction must atomically close the scoped gate, increment IGateGeneration, append the request, and capture the request/in-flight high-water and root before acknowledgment.

Every affected receipt issuance and consumption MUST serialize through that same I sequencer and compare the current gate generation and PermissionEpoch at commit. A check in one transaction followed by receipt issue/consume in another is prohibited. Lost ACK resolves by stable identity against the authoritative sequencer; same identity/digest is idempotent, changed digest/scope is CONFLICT.

I release remains an I-only currentness CAS. Immediately before release, I revalidates PermissionEpoch, IGateGeneration, ProducerDomainInventoryEpoch, registry digest, relevant entry generations, signer/key status, anti-rollback anchor, exact RecoveryCutoffBatch/ParticipantManifest and current D/Storage evidence. Any advance makes the candidate stale and requires another immutable cutoff round.

## Enumerated amendments / conditions

1. H semantic validation must prove request/admission count-to-array equality, canonical ordering/root, complete enumeration and explicit empty-set digest; schema parsing alone is insufficient.
2. The COC participant prefix and I owner-local sets require a complete bidirectional exact-identity join; no missing row is an empty set.
3. I global inventory currentness must be rechecked at final release CAS, not merely at snapshot time.
4. PreparedParticipant receipt consumption must bind the full Storage v3.1 tuple, including DB incarnation, GID/native XID where known, attempt/generation, participant ledger ref/version, COC intent position/digest and tuple digest.
5. I's final cryptographic profile, key lifecycle, historical verification and anti-rollback policy remain governed by I's separate security freeze; this decision does not select or freeze them.

## I disposition

I's R1/R2 owner-local architecture is conditionally acceptable with these amendments. This does **not** close A's R1/R2 findings: C/H/Storage joins and A integration remain required. No multi-PolicyDomain atomicity, implementation conformance, deployment or production activation is approved.
