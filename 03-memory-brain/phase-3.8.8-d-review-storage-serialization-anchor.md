# Phase 3.8.8 — D Review of Per-Authority Storage Serialization Anchor
# Phase 3.8.8 — D 对每 Authority Storage Serialization Anchor 的复审

- Owner: D — Memory Brain / ForgetFence
- Exact Storage ADR Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`
- H Unified 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- D RecoveryJoin P0 crosswalk: `c4adf827dd62d44c43b8e871dec4835581508adf`
- Decision: **ACCEPT AS D FENCE/PARTICIPANT SERIALIZATION SUBSTRATE**
- Provenance: delegated D-role review, not independent human D Owner approval.

## Decision / 决议

D accepts one shared physical anchor per BrainAuthority as the ordering point for D ProducerWork registration, dependency registration, PublicationParticipant admission and InstallForgetFence, together with Storage final visibility/NO_PUBLICATION transitions. D semantic authority remains solely D-owned.

D 接受每个 BrainAuthority 一个共享物理锚点，排序 D ProducerWork 注册、Dependency 注册、PublicationParticipant Admission、InstallForgetFence，以及 Storage Final Visibility/NO_PUBLICATION 变更。D 语义权威仍完全属于 D。

## D-specific invariants / D 专属不变量

1. D Fence installation and D admission both update the same anchor in the same transaction as their D owner records.
2. Storage final visibility updates that same anchor and must verify the exact D participant/fence ordering proof before writing the public pointer.
3. `SerializationRevision`, D `ForgetFenceGeneration`, D `owner_gate_generation` and D `barrier_generation` are four distinct nominal values.
4. H 1.2.14 `forget_fence_generation_high_water` is a D snapshot high-water; it is not the physical anchor revision.
5. Per-row ForgetFenceGeneration, lineage selector, barrier member identity and dependency closure remain committed by the D canonical row digest and D snapshot attestation.
6. If anchor incarnation, serialization history, D fence currentness or D ledger pagination is UNKNOWN, D barrier stays held and Storage stays private.
7. The anchor cannot release a D fence, close a D barrier or synthesize a D terminal receipt.

## Disposition / 结论

**ACCEPT AS L1/L2 D/Storage ORDERING SUBSTRATE.** D row schemas, full dependency pagination, late-discovery fault campaign, database failover and independent human Owner approval remain OPEN. No Forget completion or physical erasure is claimed.
