# Phase 3.8.5 — B Exact Review of D/Storage Logical Serialization Types
# Phase 3.8.5 — B 对 D/Storage 逻辑序列化类型的精确审查

- Reviewer: B — Domain Model / Typed References
- Branch: `session-b-domain-model-phase3`
- Exact Storage ADR reviewed: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- ADR Blob: `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`
- B Actor/Scope/Environment mapping: Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`
- Decision: **APPROVE THE NOMINAL TYPE BOUNDARY WITH ENUMERATED CLARIFICATIONS**
- English and Chinese are normative peers.

## 1. B decision / B 决议

B approves the topology's separation of semantic owners and physical serialization substrate. A shared transaction domain does not merge D and Storage object identity or authority. The topology is type-safe only if the following identities remain nominally distinct even when stored in the same database or encoded as strings.

B 批准该拓扑对语义 Owner 与物理序列化底座的区分。共享 Transaction Domain 不合并 D 与 Storage 对象身份或权威。即使存储在同一数据库或都编码为字符串，下列身份也必须保持名义类型独立。

## 2. Required nominal type distinctions / 必须区分的名义类型

| Type | Meaning | Must not alias |
|---|---|---|
| `BrainAuthorityRef` | One canonical memory authority scope | PolicyDomainRef, StorageAuthorityRef |
| `SerializationDomainRef` | Physical/logical transaction serialization domain | BrainAuthorityRef, COC epoch |
| `StorageAuthorityRef` | Storage authority/incarnation namespace | D authority, DB engine identity |
| `DatabaseIncarnationRef` | One database incarnation across restore/failover lineage | DB product/version, XID |
| `PreparedTransactionGID` | Stable client-chosen prepared transaction identity | EngineNativeXID, PublicationOperationId |
| `EngineNativeXIDRef` | Engine-assigned native transaction identifier | PreparedTransactionGID |
| `StorageVisibilityParticipantRef` | Storage hidden-visibility participant identity | Storage PreparedParticipantRef/GID, D PublicationParticipantRef |
| `D PublicationParticipantRef` | D barrier admission identity | StorageVisibilityParticipantRef, C ParticipantIntentRef |
| `I CommitAuthorizationReceiptRef` | I single-use sequencer decision reference | PermissionEpoch, generic bearer token |
| `PublicationOperationId` | Stable logical publication operation identity | WorkItemId, AttemptId, PreparedTransactionGID |
| `ParticipantTupleDigest` | Digest of exact immutable cross-owner participant tuple | RequestDigest, ArtifactDigest |
| `VisibilityPointerRef` | Storage public visibility root reference | PrivateStageRef, PublicationReceiptRef |

No equality, arithmetic or ordering is inferred between identifiers from different namespaces. A typed reference's string wire representation does not erase its nominal type.

不同命名空间的 ID 不得进行相等性推断、算术或排序。类型化引用的 Wire String 表达不消除其名义类型。

## 3. Clarifications / 澄清

1. The serialization domain is a physical substrate reference, not an authorization principal or policy scope.
2. Database incarnation must be included in any same-XID proof; native XID alone is not stable across database restore/reinitialization.
3. PreparedTransactionGID belongs to JF-10 same-XID recovery; it is not the StorageVisibilityParticipantRef used in Phase 3.8 derivative visibility.
4. A single database row may persist both D and Storage records, but each record retains its issuing semantic authority and typed owner reference.
5. Legacy string fields may not be silently cast into these new nominal types. Mapping requires an authoritative registry or an explicit versioned migration contract.

## 4. Final B disposition / B 最终结论

**APPROVE THE NOMINAL TYPE BOUNDARY WITH ENUMERATED CLARIFICATIONS.**

B approves ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` at the domain-type boundary. This is not a concrete database schema or implementation approval. Fact/Claim semantics and any separate B ADRs remain governed by their own decision records.

**批准名义类型边界并附澄清。** B 在领域类型边界批准该 ADR；不代表批准具体数据库 Schema 或实现。Fact/Claim 语义及 B 其他 ADR 仍由各自决策记录控制。
