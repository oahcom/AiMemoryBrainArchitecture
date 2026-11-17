# Phase 3.8.5 — D Exact Review of Storage Logical Serialization Topology
# Phase 3.8.5 — D 对 Storage 逻辑序列化拓扑的精确审查

- Reviewer: D — Canonical Memory / ForgetFence / Lineage
- Branch: `session-d-memory-brain-2026-11-16`
- Exact Storage ADR reviewed: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- ADR Blob: `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`
- D controlling Forget/Fence contract: `03-memory-brain/forget-fence-operation-and-publication-gate.md`, Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- D Phase 3.7 Producer registry/EventRef contract: Blob `4c01713bc8793a8926ef18b625b72d132572173d`
- Decision: **ACCEPT WITH ENUMERATED D-OWNED CONDITIONS — L1 LOGICAL TOPOLOGY**
- English and Chinese are normative peers.

## 1. D decision / D 决议

D accepts Option A as the normative v1 **logical** serialization topology: one serializable transaction domain per Canonical Memory authority must physically serialize D's producer admission/fence/dependency/publication-participant ledger transitions with Storage's final visibility transaction.

D's semantic authority is not transferred to Storage. D remains sole owner of ProducerClass eligibility, ProducerWork registration, RegistrationReceipt, ProducerRegistrationSequence, ForgetFence, lineage/dependency completeness, PublicationParticipantRef and D terminality. Storage supplies the transaction substrate and owns the Storage visibility outcome.

D 接受 Option A 作为 v1 规范**逻辑**序列化拓扑：每个 Canonical Memory Authority 使用一个 Serializable Transaction Domain，在物理上串行化 D Producer Admission/Fence/Dependency/PublicationParticipant Ledger 与 Storage 最终 Visibility Transaction。

D 的语义权威不会转移给 Storage。D 仍唯一拥有 ProducerClass Eligibility、ProducerWork 注册、RegistrationReceipt、ProducerRegistrationSequence、ForgetFence、Lineage/Dependency Completeness、PublicationParticipantRef 和 D Terminality。Storage 只提供事务底座并拥有 Storage Visibility Outcome。

## 2. Binding D conditions / D 约束条件

1. RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, AdmitPublication and D terminalization MUST share the same D-authoritative serialization order for one Brain authority.
2. Storage final visibility transaction MUST validate the exact D PublicationParticipantRef and the D fence-order proof against the same serialization domain. A stale D token or detached check-then-write is invalid.
3. Fence-first: if InstallForgetFence wins before AdmitPublication, D rejects/quarantines and Storage must not commit VisibilityPointer.
4. Participant-first: if AdmitPublication wins first, the unresolved participant is durably in D's barrier. A later fence may be recorded but cannot become effective past that participant until Storage provides the exact terminal outcome and D accepts its terminal receipt.
5. Storage's physical transaction may atomically read/lock D-owned rows, but it cannot author a D semantic decision, mint a D receipt or independently close a D barrier.
6. If the serialization domain is unavailable, split, stale or cannot prove order, publication remains private and D barrier remains open.
7. One Canonical Memory authority per serialization domain. Cross-authority transactions require a separate explicit protocol. This does not authorize multi-I-PolicyDomain atomicity.

## 3. Rejected and conditional alternatives / 拒绝及条件备选

- Option C (check-then-write, queue order, process mutex, outbox-only, stale token) is rejected.
- Option B (separate services + durable coordinator) is not a v1 fallback. It requires a successor ADR and proof of equivalent ordering, participant durability, failure/recovery and owner authority separation.
- This review does not select a concrete database engine or claim a physical deployment.

## 4. L1 proof obligation / L1 证明义务

The architecture has exactly two legal fence/admission orders. The final visibility transaction must prove that the D participant is either:
- rejected because the fence linearized first; or
- admitted before the fence and still held as an unresolved pre-fence participant, with Storage terminal outcome subsequently closing the exact D barrier.

There is no third state in which the participant is admitted but omitted from the high-water/barrier, or an artifact becomes visible without a valid D participant/fence proof.

## 5. Final D disposition / D 最终结论

**ACCEPT WITH ENUMERATED D-OWNED CONDITIONS — L1 LOGICAL TOPOLOGY.**

D accepts Storage ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` as the normative v1 abstract topology within the conditions above. Actual DB product/version, deployment, operator, HA/PITR and physical fault campaigns remain L4; they do not reopen this L1 decision unless a selected engine cannot satisfy the stated transaction assumptions.

**有条件接受 — L1 逻辑拓扑。** D 接受该 ADR 作为 v1 抽象拓扑，须满足上述约束。实际数据库、部署、Operator、HA/PITR 和物理故障演练属于 L4；除非后续所选引擎无法满足事务假设，否则不得据此重新打开 L1 决策。
