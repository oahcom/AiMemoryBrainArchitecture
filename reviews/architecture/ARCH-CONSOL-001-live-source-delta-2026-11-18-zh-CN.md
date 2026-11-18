# ARCH-CONSOL-001 — A 集成实时源增量审查
# 2026-11-18 — 草案 / 部分交付，非最终验收

**仓库：** `oahcom/AiMemoryBrainArchitecture`  
**审查角色：** A — 系统集成 / 架构收敛  
**审查分支：** `review/arch-consol-001-live-delta-2026-11-18`  
**基线 main SHA：** `282a82e58d8d9d1aa876621481df3184fbe5d284`  
**基线父提交：** `ee76e054ccf71bfc3b5d50af6113c699c455852a`  
**状态：** 部分实时源增量审查 — 非完整 G1–G8 验收报告  
**独立性：** 本文由协调 A 审查会话编写，不是独立 D、I、Storage 或 Integration Reviewer 签署。

## 1. 范围与硬边界

本文刷新当前 A–I、P 与 Storage Owner 分支的精确源版本，并记录这些版本可见的 Phase 3.8/3.9 跨 Owner 关键增量。本文不声称已逐行审查所有源文件，不声称 G1–G8 全部证据已完成，也不声称任何 Owner 已批准规范后继契约。

本工作流与 `main` 及所有 Owner 分支隔离。本分支不做生产变更、不改权限/Ruleset、不触发工作流、不合并、不做生产激活。承载本报告的 PR 将保持 Draft。提交信息使用 `[skip ci]`，以遵守 Issue #43 的“不执行工作流”约束。

## 2. 当前 Owner 分支精确版本

| 角色 | 分支 | 精确 HEAD |
|---|---|---|
| A | `session-a-integration-2026-11-16` | `8d2d59fff5ebc6077adc470e91d5d8b9684b3b0e` |
| B | `session-b-domain-model-phase3` | `e8a708faa50f7e0ab3f53b11d2f4f2003feced33` |
| C | `session-c-agent-integration-2026-11-16` | `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c` |
| D | `session-d-memory-brain-2026-11-16` | `b525e1f8fee2471a131e4a38efda99804045e424` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` |
| G | `session-g-memory-context` | `0f77ffbe956c5f93df295c436fcb0a750629d595` |
| H | `session-h-bmcp-protocol` | `654d4449fd491cdda37d9761fe63a3efca55dc9d` |
| I | `session-i-security-governance-2026-11-16` | `029ae8f8f48992532d5c0a9397816e4d8a9220a2` |
| P | `session-p-project-governance-baseline` | `0559a03ccd4f9640ddb7d4af8e37a059930b55af` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `268af57b099209b33835b663596e87d21bb9c22b` |

这些版本号仅证明本次读取时的分支新鲜度，不代表分支已集成、语义完整、独立审查或 Owner 接受。

## 3. 关键源文件 / Blob 台账

下列路径和 Blob SHA 均来自第 2 节对应精确 Owner HEAD 的递归 Git Tree。

| 角色 | 关键产物 | 精确 Blob SHA |
|---|---|---|
| A | `reviews/integration/phase-3.8.1-a-contract-surface-and-exact-pin-refresh.md` | `ad5450ea35f6dabc7de1ffa1ea63661f2e500064` |
| A | `reviews/integration/phase-3.8.2-a-race-crash-failover-conformance-matrix.md` | `29125b89ddf47af4c358c0cddbd5c3d6077e1f53` |
| B | `02-domain-model/ADR-001-fact-claim-semantics.md` | `a1024938ff5baba069cf128c69496a44e143330c` |
| B | `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` |
| B | `02-domain-model/lifecycle-model.md` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` |
| C | `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` |
| C | `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C | `07-agent-integration/phase-3.8.28-c-exact-review-h-applied-delivery-evidence-csubmitoutcome-join.md` | `7ae8f2609a8786c4a5a715a270faa706156ed462` |
| D | `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| D | `03-memory-brain/phase-3.9-d-forget-terminal-semantics-and-linearization-closure-proposal.md` | `9c02b5680317f0092788ad0da66d621338b1c54c` |
| E | `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md` | `475fee41e5eea527af4edefbfe88c58c86967d0a` |
| E | `04-memory-compiler/phase-3.8.6-e-review-storage-serialization-anchor.md` | `19d708bc29b6115d7bccb7d320781f452ee28b78` |
| F | `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md` | `9dae404993d3006e59d2dae88a0a97a3c0998d58` |
| F | `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md` | `122238146830db6188f00a9788e018a82bfb3f90` |
| G | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | `a8efd1aa9696783035e157131fa9751666a4182d` |
| G | `06-memory-context/phase-3.8.26-g-restore-fenced-write-admission-hardening.md` | `d6cd4e8ce18c88ade747eb7d19c6c83840b54792` |
| H | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` | `1b8f44675f30919764481d33755c566ef5cf1ea8` |
| H | `08-bmcp-protocol/phase-3.8.34-h-owner-gate-release-semantic-reference.md` | `b27dbfe57a7b3a3312d3d8576a74b81e72ac86f7` |
| H | `08-bmcp-protocol/phase-3.8.32-h-unified-1.2.16-owner-snapshot-completeness.md` | `cc40b50d99e329eafa6851049ad0e2cdbba5e955` |
| I | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| I | `09-security-governance/phase-3.9-i-d-forget-lifecycle-terminalization-authorization-proposal.md` | `362307f6fff84cbe81fb71f37d6319e691db4f89` |
| P | `00-governance/project-decision-authority.md` | `ca3777acae5ceb38a2a421cbf9e738053e4a4057` |
| P | `00-governance/architecture-invariants.md` | `66266667bdbb1cf15a2644fa98db5ecaaf3bb23b` |
| Storage | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `175ee7b1349cfdb79a19898b311a88391ed88010` |
| Storage | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `bb544ba2f346bdc130d524bd5c7310d86f367988` |
| Storage | `reviews/storage-consistency/phase-3.9-storage-review-d-i-forget-terminalization-and-read-suppression.md` | `1cd9f35f1e28fb5f71cd74599d1560fa36043ed8` |

**版本固定说明：** 本表每个 Blob SHA 均为从第 2 节精确分支 HEAD 的递归 Tree 读取的完整 40 位 Git Object ID。任何规范决策或最终验收前，仍须重新读取分支 HEAD 与 Blob，因为 Owner 分支仍可移动。

## 4. 跨 Owner 架构发现

### 4.1 B 的 Fact/Claim 语义仍是系统级 blocker

B 的 `ADR-001-fact-claim-semantics.md` 仍存在提案/决策缺口。Domain Model Overview 与生命周期材料使用的 Fact/Claim 语义，尚未与控制性 I-04/P-04 区分完成对齐。在 Fact 与 Claim 的含义、权威性、版本化和冲突处理未确定前，系统不能安全冻结规范 Memory Semantics。

**A 结论：** BLOCKED。B 必须发布一个精确规范决策，统一所有下游 Schema 和 Lifecycle 引用，并列出需要迁移的消费者。

### 4.2 Lifecycle Manager 权限不得与 I 的 Policy Authority 重叠

生命周期模型对 Lifecycle Manager 的职责描述，可能被解释为同时拥有 Policy、Execution、Authorization 和 Audit Authority。这与 I 拥有 Authentication、Authorization、Retention 和 Legal Hold 决策权相冲突。

D/I Phase 3.9 提案形成一个候选职责划分：
- D 拥有规范 Lifecycle Semantics、状态迁移、ForgetFence 和 D 侧 Suppression Proof。
- I 拥有经认证的授权、撤权/PermissionEpoch 决策和 I 侧 Receipt。
- Lifecycle Manager 仅负责 Orchestration/Enforcement，不是独立 Policy Authority。
- Storage 拥有持久化原子性以及 Commit/UNKNOWN 结果解析。

这只是候选收敛，并非已批准的规范决策。D 和 I 必须针对同一个精确后继契约 Blob 作出批准。

### 4.3 Forget Terminalization 必须保留四种不可互换事实

D/I/Storage Phase 3.9 文档支持将以下结果严格分开：
1. D Fence 的线性化与立即读抑制。
2. 所有 Fence 前 Participant Barrier 的关闭。
3. D 规范 `LifecycleEvent(Forgotten)` 与 I Governance Completion/Receipt。
4. Physical Erasure Confirmation。

D Fence 必须在其自身持久化线性化点立即抑制读取；不能等待所有旧 Participant Barrier 关闭后才生效。Barrier Closeout 是另一项完成事实。`CanonicalSuppressionComplete`、`LifecycleEvent(Forgotten)`、`GlobalForgetCompleted` 和 `PhysicalErasureConfirmed` 不得互相替代。

Storage Phase 3.9 Review 明确是条件性意见和同会话角色模拟，不是独立 Storage Owner 签署。D/I/Storage 批准仍缺失。

### 4.4 Publication Protocol 模型证据已有实质提升，但仍是抽象模型

当前 main 已包含 PR #179、#181、#183 和 #186：
- D/I/Storage Participant 与 UNKNOWN Binding 之间的精确 Operation Identity；
- 25 个模型化授权上下文位置；
- 内存模型中的 Fail-Closed PermissionEpoch Currentness；
- I COMMIT_WON、Storage Final Commit 和 UNKNOWN Reconciliation 三个边界上的 Dependency Digest 相等性检查；
- PR #186 精确 Head 上 61/61 测试通过。

这些测试仅证明确定性内存参考模型迁移和替换防护，不证明经认证的 Issuer/Key Status、真实 I Sequencer/Registry、规范 Dependency Set Digest 派生、Authenticated Receipt、数据库持久化、事务隔离、分布式竞态、Crash/Failover/Restore 或生产 Adapter。

### 4.5 C/H Applied Delivery 与 Owner-Gate Release 仍需 Schema 级对账

H 的 Unified 1.2.17 Schema 和 Owner-Gate Release Semantic Reference 改善了 COC/JF-10 交接。C 的 SubmitOutcome 1.0.1 Contract 和 Schema 仍是独立规范输入。跨 Owner Join 仍需逐字段精确批准：
- H 的 `final_request_boundary_generation` 要求必须与 C 的 SubmitOutcome Contract 对账；当前尚未证明 C 契约中存在匹配字段。
- D 的 Dependency Cursor/Root 语义必须由 D 提供精确语义。
- I 的 Signed P0 Projection 和 Owner-Snapshot Authorization 必须由 I 明确字段与证据。
- H Validator 的结果不等同于生产经认证 Owner Signature、实时 Quorum 或生产 COC Release。

**A 结论：** CONDITIONAL / NOT ACCEPTED。C、D、H、I 必须就精确字段映射和版本化 Schema Tuple 达成一致。

### 4.6 Storage Topology 仅在逻辑层选定，尚未物理证明

Storage ADR 当前选择 L1 Logical Serialization Topology Option A。L4 Engine/Deployment Topology 仍开放。逻辑 Owner/Transaction Boundary 不等于真实数据库引擎、XA/Prepared-XID 能力、持久化事务、隔离级别、Crash Recovery、HA Failover 或 Restore 行为。

**A 结论：** CONDITIONAL。在真实 Runtime Repository 中选定并验证 L4 前，不得声称生产 Atomicity 或 Crash Safety。

### 4.7 G Persistence/Restore 仍是参考证据

G 的 Idempotency、Crash/Restore 和 Fenced-Write Admission 文档描述了重要安全规则，但本身不能证明生产持久化引擎、原子 Restore Manifest、Delayed-Fill Rejection、Replica Rebuild 或跨进程 Fence。架构阶段可以定义这些要求，但生产符合性仍是 NOT RUN。

### 4.8 Runtime Implementation Binding 已延期，不是架构阶段 blocker

Issue #7 中 Project Owner 决策仍为 `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`。缺少规范 Runtime Repository 不是当前架构阶段 blocker，但意味着现在不能声称生产实现或生产符合性。

## 5. G1–G8 状态快照

| Gate | 当前 A 结论 | 原因 |
|---|---|---|
| G1 精确源清单 | PARTIAL | 已刷新当前分支 HEAD 和选定关键 Blob；仍需对所有关键消费者完成完整逐行审查。 |
| G2 Authority/Consumer Contract | BLOCKED | B Fact/Claim 语义和 D/I/Storage/C/H 精确字段批准仍未解决。 |
| G3 跨 Owner 冲突闭环 | BLOCKED | Lifecycle Manager Authority、C/H 字段 Join、Forget Terminalization 和 Publication Tuple 决策仍是提案。 |
| G4 Race/Crash/Failover/Restore 证据 | NOT PROVEN | 存在矩阵和参考模型，但没有生产对抗性执行证据。 |
| G5 技术/拓扑决策 | PARTIAL | Storage L1 Logical Option A 已选，L4 物理引擎/部署仍未定。 |
| G6 双语/文档一致性 | PARTIAL | 关键配对文档存在，本增量也提供双语版本；完整逐行双语审计仍未完成。 |
| G7 独立 Owner 批准 | NOT EVIDENCED | 未发现针对同一精确 SHA 的 D/I/Storage 批准集合或独立 Integration Reviewer 报告。 |
| G8 架构冻结/发布 | NOT READY | 上游 Gate 仍开放；生产激活未获授权。 |

## 6. 治理与集成状态

- 当前 `main`：`282a82e58d8d9d1aa876621481df3184fbe5d284`。
- 本次刷新时开放 PR：0。
- Main Branch Protection：`protected=false`；Required Checks 未由平台强制。Issue #134 仍 OPEN/P0。
- Issue #7 的 Runtime Binding 决策仍延期至 Engineering Phase。
- AID-2026-001 的 Owner D Approval、Owner I Approval 和 Independent Integration Review 仍待完成；生产 DFI-001…DFI-022 仍 NOT RUN/NOT EVIDENCED；Overall Acceptance 仍 BLOCKED。

## 7. A 的建议

**不得冻结架构 / 不得授权生产激活。**

下一步必须完成：
1. 补齐所有关键 A–I/Storage Consumer 的完整 40 位精确源清单和逐行审查。
2. 解决 B Fact/Claim 语义及 Lifecycle Authority 冲突。
3. 获取 D/I/Storage 对 Phase 3.9 Forget Terminalization 契约的精确 SHA 决策。
4. 获取 C/D/H/I 对 COC/JF-10 Owner-Gate Release 的精确字段/Schema 批准。
5. 选择并证明 L4 物理 Storage Topology。
6. 在 Project Owner 延期的 Runtime Binding 满足后，于规范 Engineering Repository 执行生产边界 Race/Crash/Failover/Restore 和 DFI/R3 Conformance。
7. 由三个独立会话针对同一个冻结规范 SHA 提交 D、I 和 Integration 审查报告。

本文是有限范围实时源增量，不是最终系统级验收报告。不得推断已有 Owner 批准、架构冻结、实施授权或生产激活。
