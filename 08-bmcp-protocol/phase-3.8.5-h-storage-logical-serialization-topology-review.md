# Phase 3.8.5 — H Exact Review of D/Storage Logical Serialization Topology
# Phase 3.8.5 — H 对 D/Storage 逻辑序列化拓扑的精确审查

- Reviewer: H — BMCP Protocol and Adapter Authentication
- Branch: `session-h-bmcp-protocol`
- Exact Storage ADR reviewed: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- ADR Blob: `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`
- H current unified schema 1.2.8 Blob: `70b892797d07489936300a26c0dedfafe1d6e746`
- H crypto wire mapping Blob: `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`
- Decision: **ACCEPT WITH ENUMERATED H-OWNED CONDITIONS — PROTOCOL/IDENTITY BOUNDARY**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H accepts the logical topology as compatible with the protocol authority model, provided that every owner position and participant reference remains a distinct typed opaque value. H transports and validates representations; it does not create ordering authority or decide the semantics of D, I, Storage or C.

H 接受该逻辑拓扑与协议权威模型兼容，前提是每个 Owner Position 和 Participant Reference 均保持独立的类型化不透明值。H 负责传输和表示校验，不创建顺序权威，也不决定 D/I/Storage/C 的语义。

## 2. Required protocol distinctions / 必须保持的协议区分

- D ProducerRegistrationSequence / ForgetFenceGeneration / PublicationParticipantRef / D TerminalReceiptRef;
- I PermissionEpoch / PolicyDomain sequencer position / CommitAuthorizationReceipt / ITerminalProof;
- StorageVisibilityParticipantRef / StorageVisibilityOutcome / VisibilityPointer / PublicationReceipt;
- JF-10 PreparedParticipantRef / PreparedTransactionGID / DB incarnation / engine-native XID;
- C ParticipantIntentRef / CSubmitOutcomeRef / provider idempotency key;
- COC epoch/index/entry digest/quorum proof;
- F IndexWatermark and G ContextVersion/Delivery/Applied.

These values are never cast, compared numerically across namespaces or substituted because their wire encoding is a string.

这些值不得跨命名空间强转、数值比较或因 Wire 编码都是字符串而互相替代。

## 3. Binding H conditions / H 约束条件

1. Every message carries exact owner authority, message family, audience, schema artifact/family version and typed references required by its contract.
2. H must preserve owner-signed payload projection separately from COC quorum attestation and transport channel binding.
3. Structural schema validation does not prove quorum order, owner currentness, D fence coverage, I receipt consumption or Storage visibility commit.
4. Unknown critical fields, duplicate JSON keys, profile downgrade, wrong audience, stale generation and ambiguous absent/null values fail closed under the exact semantic validator.
5. H schema 1.2.8 is a structural candidate; exact semantic validator and current cross-owner decisions remain required.

## 4. Final H disposition / H 最终结论

**ACCEPT WITH ENUMERATED H-OWNED CONDITIONS — PROTOCOL/IDENTITY BOUNDARY.**

H accepts ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` as an abstract topology compatible with the protocol boundaries. H does not claim schema freeze, cryptographic approval, cross-language production interoperability, live COC quorum or implementation conformance.

**有条件接受 — 协议/身份边界。** H 接受该 ADR 的抽象拓扑与协议边界兼容；不声明 Schema 冻结、密码学批准、生产跨语言互操作、真实 COC Quorum 或实现符合性。
