# Phase 3.8.6 — B Exact Review of Storage Serialization Anchor Nominal Types
# Phase 3.8.6 — B 对 Storage Serialization Anchor 名义类型的精确审查

- Reviewer: B — Domain Model / Typed References
- Exact Storage ADR: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- Exact ADR Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`
- Predecessor B nominal-type review: Blob `ad1cc3c3f934b88e8fc3d0200612269198345e2f`
- Decision: **APPROVE THE PER-AUTHORITY ANCHOR TYPE BOUNDARY WITH ENUMERATED CLARIFICATIONS**
- English and Chinese are normative peers.
- Provenance: delegated B-role technical review; **not an independent human B Owner signature**.

## 1. B decision / B 决议

B approves the concrete `CanonicalAuthoritySerializationAnchor` as a physical serialization primitive for Option A. The anchor does not merge semantic authorities and does not create a global cross-owner counter.

B 批准 `CanonicalAuthoritySerializationAnchor` 作为 Option A 的物理序列化原语。该锚点不合并语义权威，也不创建跨 Owner 全局计数器。

## 2. Required nominal types / 必须区分的名义类型

| Type | Meaning | Must not alias |
|---|---|---|
| `BrainAuthorityRef` | Canonical Memory semantic authority | StorageAuthorityRef, PolicyDomainRef |
| `SerializationDomainRef` | Physical/logical transaction domain | BrainAuthorityRef, COC domain |
| `AuthoritySerializationAnchorRef` | One physical anchor row per BrainAuthority | SerializationDomainRef, D Fence, VisibilityPointer |
| `SerializationTransitionRef` | Stable idempotent transition record identity | PublicationOperationId, PreparedTransactionGID |
| `SerializationRevision` | Monotonic physical revision local to one anchor/domain | D FenceGeneration, GateGeneration, BarrierGeneration, I PermissionEpoch, C sequence, COC position, XID |
| `StorageAuthorityRef` | Storage physical authority/incarnation | D authority, database product |
| `DatabaseIncarnationRef` | DB incarnation across restore/failover | XID, engine version |
| `PreparedTransactionGID` | JF-10 stable prepared transaction identity | EngineNativeXIDRef, SerializationTransitionRef |
| `EngineNativeXIDRef` | Engine-assigned native transaction ID | PreparedTransactionGID |
| `StorageVisibilityParticipantRef` | Hidden Storage visibility participant | D PublicationParticipantRef |
| `D PublicationParticipantRef` | D barrier admission identity | StorageVisibilityParticipantRef, COC ParticipantIntentRef |
| `I CommitAuthorizationReceiptRef` | I single-use sequencer decision | PermissionEpoch, SerializationRevision |
| `PublicationOperationId` | Logical publication operation | WorkItemId, AttemptId, SerializationTransitionRef |
| `ParticipantTupleDigest` | Exact cross-owner participant tuple digest | RequestDigest, ArtifactDigest |
| `VisibilityPointerRef` | Public Storage visibility root | PrivateStageRef, PublicationReceiptRef |

## 3. Type and ordering rules / 类型与排序规则

1. One `AuthoritySerializationAnchorRef` exists per `BrainAuthorityRef` / `SerializationDomainRef`. It is not global across the installation.
2. `SerializationRevision` orders only physical transitions within that one anchor. It is not an authorization epoch and is not comparable across authorities.
3. D's `ForgetFenceGeneration`, `owner_gate_generation` and `barrier_generation` remain three separate D types. H 1.2.14 carries the ForgetFence high-water explicitly; it is not the anchor revision.
4. I PermissionEpoch/PolicyDomain positions, C `sequence_namespace_ref` and record sequence, COC quorum positions, Storage PreparedTransactionGID and EngineNativeXID remain separate.
5. The anchor row's physical owner is Storage; its revision does not grant Storage authority to create or interpret D/I/C/COC semantic decisions.
6. A serialization transition is idempotent by `SerializationTransitionRef` plus immutable transition digest. A retry with same ref/different digest is an integrity incident.
7. `StorageVisibilityParticipantRef` and `D PublicationParticipantRef` are distinct, even when joined in the same database transaction.
8. Database incarnation is part of recovery proof; native XID alone is not stable across restore/reinitialization.

## 4. B disposition / B 侧结论

**APPROVE THE PER-AUTHORITY ANCHOR TYPE BOUNDARY WITH ENUMERATED CLARIFICATIONS.** This is an L1/L2 type-system approval for the logical topology. It does not prove the database engine, HA/restore, serializable behavior, old-primary fencing, runtime lock/commit implementation or performance. Those remain L4.

**批准每 Canonical Authority 的 Anchor 名义类型边界，并附带明确澄清。** 这是逻辑拓扑的 L1/L2 类型系统批准，不证明数据库引擎、HA/Restore、Serializable 行为、旧主隔离、运行时 Lock/Commit 实现或性能；这些仍属 L4。
