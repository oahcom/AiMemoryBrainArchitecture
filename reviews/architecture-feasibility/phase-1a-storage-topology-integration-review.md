# Phase 3.8.5 — A Integration Review: Storage Logical Serialization Topology
# Phase 3.8.5 — A 集成审查：Storage 逻辑序列化拓扑

- Reviewer: A — Principal Integration Architect
- Branch: `session-a-integration-2026-11-16`
- Exact Storage ADR reviewed: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- ADR Blob: `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`
- Decision: **ACCEPT AS NORMATIVE V1 LOGICAL ARCHITECTURE — L1 CLOSED; L4 DEPLOYMENT OPEN**
- Review provenance: user-delegated A-role simulation, not an independent human integration signature.
- English and Chinese are normative peers.

## 1. Exact Owner review bundle / Owner 精确审查证据

A re-read each review from its named Owner branch and verified the exact Blob SHA.

| Owner | Decision artifact | Readback Blob | Disposition |
|---|---|---|---|
| D | `03-memory-brain/phase-3.8.5-d-storage-logical-serialization-topology-review.md` | `7b44f2b3e346eaa34840797bec391465af6130a3` | ACCEPT WITH D-OWNED CONDITIONS |
| E | `04-memory-compiler/phase-3.8.5-e-storage-logical-serialization-topology-review.md` | `14efd3d32930bec9740bfb4509e18ff6bf670090` | ACCEPT WITH E-OWNED CONDITIONS |
| B | `02-domain-model/phase-3.8.5-b-storage-logical-serialization-type-review.md` | `ad1cc3c3f934b88e8fc3d0200612269198345e2f` | APPROVE TYPE BOUNDARY |
| F | `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md` | `9dae404993d3006e59d2dae88a0a97a3c0998d58` | ACCEPT WITH F READ-PATH CONDITIONS |
| G | `06-memory-context/phase-3.8.5-g-storage-logical-serialization-topology-impact-review.md` | `0e93acea1ebd7f1e6e86b429ef3ad2a652052c41` | ACCEPT WITH G CONTEXT/APPLIED CONDITIONS |
| H | `08-bmcp-protocol/phase-3.8.5-h-storage-logical-serialization-topology-review.md` | `b71e818379117514c4492138780fc80a9b2deba0` | ACCEPT WITH H PROTOCOL CONDITIONS |
| I | `09-security-governance/phase-3.8.5-i-storage-logical-serialization-topology-review.md` | `c63075aead9f0b18de9af4cf6fb0bc3c3a5a6d53` | ACCEPT WITH I SEQUENCER CONDITIONS |
| C | `07-agent-integration/phase-3.8.5-c-storage-logical-serialization-topology-review.md` | `2b7fa5587523a07662729942f765c4db309f50f5` | ACCEPT WITH C EGRESS CONDITIONS |

## 2. A integration decision / A 集成决议

A accepts Storage Option A as the normative v1 logical topology:

**One serializable transaction domain per Canonical Memory authority, physically ordering D admission/fence/dependency/publication-participant records with Storage hidden prepare/final visibility/outcome/receipt/outbox records.**

This is a physical serialization substrate only. It does not merge semantic authority:

- D owns producer admission, ForgetFence, lineage, dependency completeness and D barrier terminality.
- Storage owns PREPARED_HIDDEN, VisibilityPointer, Storage outcome, PublicationReceipt and outbox.
- I owns PolicyDomain authorization, PermissionEpoch, receipt consumption and revocation ordering.
- C owns provider egress and actual CSubmitOutcome.
- COC remains a separate quorum-ordered causal/recovery log.
- E/F/G/H retain compiler, runtime, context and protocol authority respectively.

A accepts the cross-owner composition because each Owner review preserves these boundaries and explicitly refuses authority substitution.

A 接受 Storage Option A 作为 v1 规范逻辑拓扑：

**每个 Canonical Memory Authority 一个 Serializable Transaction Domain，在物理上串行化 D Admission/Fence/Dependency/PublicationParticipant 记录与 Storage Hidden Prepare/Final Visibility/Outcome/Receipt/Outbox 记录。**

这只是物理序列化底座，不合并语义权威。D/Storage/I/C/COC 各自保留其唯一权威；E/F/G/H 保留 Compiler/Runtime/Context/Protocol 权威。A 接受该跨 Owner 组合，因为各 Owner 审查均保留这些边界并拒绝权威替代。

## 3. L1 proof closure / L1 证明闭环

The topology has a complete abstract linearization story:

1. Producer registration and fence installation share D's authoritative ordering domain.
2. Storage hidden prepare creates a durable but non-visible participant.
3. D participant admission binds to the exact Storage participant and is ordered against the fence.
4. I consumes a single-use receipt in its own PolicyDomain sequencer; only COMMIT_WON permits final Storage visibility.
5. Storage final serializable transaction validates exact D participant/fence order and consumed I proof, then atomically commits pointer, receipt, outcome and outbox.
6. D/I close only after the same exact Storage terminal outcome.
7. UNKNOWN keeps artifact private and owner barriers unresolved.

The two legal fence races are complete:
- Fence first → D admission rejected, no visibility.
- Participant first → unresolved D barrier holds later fence; exact Storage/I terminal reconciliation closes the participant.

No check-then-write, queue-order, process-local mutex, stale reusable token or outbox-only shortcut is accepted.

该拓扑的抽象线性化故事完整：D 注册/Fence 排序；Storage Hidden Prepare；D 绑定 Participant 并与 Fence 排序；I 独立 Sequencer 消费单次 Receipt；仅 COMMIT_WON 可进入 Storage 最终 Visibility；Storage 原子提交 Pointer/Receipt/Outcome/Outbox；D/I 在同一 Storage 终态后独立关闭；UNKNOWN 保持私有和 Barrier 未解决。

Fence 竞争只有两种合法顺序：Fence First 则拒绝 D Admission、不产生 Visibility；Participant First 则 D Barrier 持有后续 Fence，等待精确 Storage/I 终态协调。禁止 Check-then-write、Queue Order、Process Mutex、过期可复用 Token 或 Outbox-only 捷径。

## 4. L2/L3 residual obligations / L2/L3 遗留义务

This decision closes the **topology selection question at L1**, not the entire Phase 3.8 contract freeze.

Remaining L2:
- exact current D/E/I/Storage Phase 3.8 participant tuple and semantic API cross-review;
- exact H schema 1.2.8 semantic validator and RecoveryJoin 1.0.1 currentness mapping;
- C Provider Outcome source contract exact acceptance by H/I/G/Storage/A;
- exact COC Recovery Cutoff Batch/Manifest/JoinProof and owner-local gate release semantics;
- current Owner exact-version binding manifest and no stale pins.

Remaining L3:
- reference-model coverage for every crash boundary, fence/visibility interleaving, I revocation/receipt consumption, C egress close/send and COC recovery-cutoff enumeration;
- explicit counterexample analysis for participant omission, duplicate/digest conflict, incomplete owner snapshot, stale restore prefix, and owner-currentness races.
- The H 101/101 candidate suite is bounded evidence, not proof of all these integrated properties. The COC 10/11 reference-model runs are also bounded evidence.

该决策关闭的是 **L1 拓扑选择问题**，不是整个 Phase 3.8 合同冻结。

剩余 L2：当前 D/E/I/Storage Participant Tuple 与语义 API 交叉审查；H Schema 1.2.8 Semantic Validator/RecoveryJoin 1.0.1 映射；C Provider Outcome 精确 Owner 接受；COC Recovery Cutoff Batch/Manifest/JoinProof 与 Owner-local Gate Release；当前 Owner 精确版本绑定清单。

剩余 L3：每个崩溃边界、Fence/Visibility 交错、I Revocation/Receipt Consumption、C Egress Close/Send、COC Recovery Cutoff Enumeration 的参考模型；针对 Participant 遗漏、Digest 冲突、Owner Snapshot 不完整、Restore Prefix 过期和 Currentness Race 的反例分析。H 101/101 和 COC 10/11 只是有限范围证据。

## 5. L4 explicitly separated / L4 明确分离

The following remain L4 and MUST NOT block architecture freeze by themselves:
- selecting the concrete DB product/version/configuration and deployment manifest;
- naming the production operator/on-call and failure-domain placement;
- production HA/PITR/backup/restore drill and physical crash/failover testing;
- actual application read-path and cache/index enforcement;
- production provider adapters, HSM/KMS, real trust registry deployment and performance/resource benchmarks.

If a later selected engine cannot satisfy serializable transaction assumptions, the deployment is non-conforming and must not weaken the design. A successor architecture ADR would be required before changing the logical topology.

以下属于 L4，不能单独阻塞架构冻结：具体 DB 产品/版本/配置与部署清单；生产 Operator/On-call 与故障域；生产 HA/PITR/Backup/Restore 演练和物理故障测试；真实应用读路径及 Cache/Index 强制执行；生产 Provider Adapter、HSM/KMS、Trust Registry 部署和性能/资源基准。

若后续选定引擎无法满足 Serializable Transaction 假设，则部署不符合架构，不得弱化设计。更改逻辑拓扑必须提交后继架构 ADR。

## 6. Final A disposition / A 最终结论

<badge color="success">L1 CLOSED</badge> **ACCEPT AS NORMATIVE V1 LOGICAL ARCHITECTURE.**

Storage ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` is accepted at the abstract architecture level with the exact Owner conditions above. Physical deployment remains L4 OPEN. Overall architecture freeze remains **NOT YET DETERMINED** until the separate L2/L3 obligations across all Owners are closed.

**L1 已关闭。** A 接受该 ADR 作为 v1 规范逻辑架构，并保留各 Owner 的精确约束。物理部署属于 L4，仍 OPEN。全系统架构冻结仍**尚未裁决**，需先完成其他 Owner 的 L2/L3 义务。
