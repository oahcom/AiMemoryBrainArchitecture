# Forget Fence 原子性 — 第 4 部分：JF-10 / COC Owner 决议

- 文档 ID：D-FORGET-GATE-001-P4
- 源文件版本：d3ddfff9500d9138d643989e8496d99b8d9ed79e
- 源分支：session-d-memory-brain-2026-11-16
- 对应英文：[Part 4 — JF-10 / COC Owner Decisions](../../en/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md)
- 源规范：[D 规范源](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md)（源提交 `b525e1f8fee2471a131e4a38efda99804045e424`；原始源 Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`）。

## Phase 3.6.2 — D Owner 接受修订版 JF-10 v2

**状态：D 接受 DE-S v2 提案中由 D 拥有的 Serialization 与 Fence Predicate；I 接受和实现仍为 OPEN。**

D 确认以下内容是拟议 Owner-gate-participating 2PC Protocol 的 D 侧规范要求：

1. D 的 ForgetOperation、ForgetFence、ProducerClass/ProducerWork Ledger、Dependency Inventory、BarrierSnapshotReceipt 和 Canonical Suppression Proof 仍由 D 拥有。
2. 对每个 Canonical Memory Authority，RegisterProducerWork、RegisterDerivedDependency、InstallForgetFence 和 Storage Publication Participant 必须在相同的持久化 Authority/Target-Lineage 排序记录上串行化。Fence Transaction 原子持久化严格递增 FenceGeneration、不可变 Target Digest、ProducerRegistryVersion、ProducerRegistrationHighWater、BarrierSnapshotReceipt 和 Installation CanonicalCommitCursor。
3. ProducerRegistrationHighWater 限定于该 Canonical Memory Authority 的 ProducerWork Registration Ledger。CanonicalCommitCursor 是独立的每个 Brain Authority Commit Order/Audit Cursor。两者都不能与 FenceGeneration、PermissionEpoch 或 I ProducerDomainInventoryEpoch 互换。
4. Prepared Storage Participant 必须保留 D Fence/Lineage Serialization Lock，直到 I 的持久 Coordinator Decision 已恢复，并且 Storage Participant 已 Commit 或 Abort。Fence-first 表示 Publication Prepare 被拒绝；Participant-first 表示 Fence Installation 不能越过未解决 Participant。Timeout 是 UNKNOWN，不是 Publish Permission，也不能关闭 Barrier。
5. D Final Predicate 在 Participant Boundary 重新检查每个 Source Ancestor/Target、准确 Dependency Completeness、WorkItem/Attempt/Lease Fencing，以及最新适用 Fence。I 的 COMMIT_WON 不能覆盖 D Fence。
6. ForgetOperation 阶段仍为 Requested、FenceEstablished、InventoryOpen、BarrierDraining、TargetReconciliation、CanonicalSuppressionComplete、Blocked 和 Failed。只有 D 自己捕获的 Barrier 已 Terminal、所有必需 D-domain Target 都有 Suppression Proof 或精确 I-approved Residual Exception，且不存在 D-owned Unknown/Gap/Late Derivative 时，D 才能声明 CanonicalSuppressionComplete。这不是 I Global Forget Completion，也不是 Physical Erasure。
7. 迟到派生物、新发现 Producer、Registry Gap 或恢复的陈旧 Task 会使相关 D Proof 失效/重新打开，并创建可审计 Reconciliation Obligation；不得静默复用先前 Completion Checkpoint。

D 仅将 v2 Protocol 接受为仍需 I 对准确 Owner-gate 进行审查的跨 Authority 提案。D 不定义 I Sequencer 实现、不批准 I Inventory/Authorization/Exception Policy、不选择具体 Database Engine，也不声称 Runtime Conformance。

### D36 §9 第 11–13 行 — 离线重入、Inventory Epoch 变化与陈旧 Task 恢复

| Source ID | 测试名称 | 必需结果 | 状态 |
|---|---|---|---|
| D36 §9 row 11 | Fence 后离线 Producer 重连 | 重连 Worker 在访问 Source 前解析原始已登记 WorkItemId 和当前 Fence；陈旧 Task 被拒绝/隔离；Offline/Unknown Producer Evidence 不得关闭 I Global Inventory | NOT RUN |
| D36 §9 row 12 | Forget 期间 I Inventory Epoch 变化 | D Local ProducerRegistrationHighWater 保持不变；I Seal 变陈旧/重新打开；在 I 签发替代 Seal 且所有新增适用 Target 完成协调前，不得 Global Completion | NOT RUN |
| D36 §9 row 13 | CanonicalSuppressionComplete 后旧 Compiler Task 恢复 | 当前 D Fence 在 Publication 前抑制它；保留稳定 WorkItemId/Lineage；任何迟到派生物都会使既有 D Proof 失效/重新打开并接受审计 | NOT RUN |

这些用例扩展原始 D36 §9 矩阵，不重新编号，也不削弱第 1–10 行。

## Phase 3.6.2 — D 确认 Applied Submission Boundary 上的 Forget 排序

D 审查了 A 固定版本的 C/G/H Applied Contract Package（Blob SHA 61d961c32138fd875069e8cbac4696bb031447c0），并确认以下 D-owned 语义：

1. D 签发并验证权威 ForgetOperation/Fence Identity、Generation/Cursor、Target Digest 和 Lineage Coverage。Consumer 必须为每个相关 Source Ancestor 和 Target 解析最新适用 Fence；仅有 Observed Token、没有完整 Lineage/Currentness Proof 不够。
2. Final Request Submission Boundary 是受保护披露边界。适用 D Fence 必须与真实 Submit Event 建立因果/线性化顺序，不能通过比较不透明 Token 数值或独立 Wall-clock Timestamp 推断。
3. 如果成功 Submit 排在适用 Fence Installation 之前，D 后来的 Fence 不会改写该历史 Submit 事实；只有在 C 的不可变 Submit Evidence 和 I Authorization Ordering 均独立得到证明时，G 才可以保留历史上有效的 Applied 事实。当前使用资格仍会被 Fence 立即撤销。
4. 如果 Fence Installation 排在 Submit 之前，Request 已过期/不具资格，不能提升为 Full Applied；受管区域保持 Suppressed。
5. 如果 Submit/Fence 顺序、Lineage Coverage 或 Fence Currentness 为 Unknown/不可比较，结果就是 Unknown 并保持 Suppressed。不得提升 Full Applied。
6. D Fence Receipt 只证明 D-owned Fence/Lineage 事实。它不证明 I Authorization、H Adapter Purge、G Applied、Global Forget Completion、Backup Deletion 或 Physical Erasure。
7. 已 Commit 的 Fence/Suppression Obligation 不会因为 Requester 后续撤销而回滚；后续 Cleanup 必须由当前获得授权的 I Service/Continuity Principal 推进。D 不定义或批准该 I Principal Policy。

**D 处置：** 对 A 准确版本 Package，**APPROVE D-OWNED FENCE/LINEAGE SEMANTICS WITH AUTHORITY RESERVATIONS**。I Authorization 和 D/E/Storage 可执行 Linearization 仍是独立阻塞项。D36 与 DE-S Fault/Race Suite 仍为 **SPECIFIED / NOT RUN**；不声称已实现或端到端完成。

## Phase 3.6.2 — D 对 JF-10 Prepared Participant ↔ COC Bridge 的精确版本接受

**审查的准确 A Artifact：** A 分支 session-a-integration-2026-11-16 中的 reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md，Blob a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d，§12.1–12.8。

**D 决议：ACCEPT — 对该准确 A Blob 的 D-owned Fence/Barrier 语义予以接受，并保留权威边界。**

D 接受 Bridge 的 Prospective-participant Ordering 和 Barrier 要求与现有 D Fence Contract 一致，但必须遵守以下 D 解释：

1. 在 D Fence Cutoff 之前，已由 COC Quorum Commit 的 JF10_PREPARE_INTENT_REGISTERED 会使 Prospective Participant 成为受影响 Target/Source/Ancestor Barrier 的成员，即使 Storage PREPARE 或 Signed Prepared Receipt 尚未登记。
2. D Fence Cutoff 若先于 Prepare-intent Registration，则拒绝受影响 Prepare；不得为该 Lineage 执行 Storage XID Prepare。
3. D 独占 ForgetOperation、ForgetFence、Target/Lineage Registration、ProducerRegistrationHighWater、BarrierSnapshotReceipt、D Fence Generation 和 Effective-fence/Suppression Completion 的权威。COC Record/Position 是跨 Owner 排序 Evidence；它们不能创建 D State，也不能清除 D Obligation。
4. Fence 前 Participant 必须留在 D Barrier，直到 I Sequencer 的准确 Terminal Decision 和 Storage 同 XID Commit/Rollback Resolution 得到权威证明，且所有 D Lineage Obligation 均已满足。
5. 未解决/有歧义 Participant 使 Barrier 保持开放。COC/I/Storage Outage、Timeout、Missing Row、Stale Replica 或 Lost ACK 都不能释放 Participant，也不能允许 Effective Fence Completion。
6. D 与 COC Position 是类型化的不同排序。D 不比较不透明值，也不根据 Wall-clock 推断顺序；D 消费经过认证的 Bridge Tuple 和自身 Canonical Fence/Lineage Evidence。

这是 D 对 D-owned Fence/Barrier 语义的精确版本架构接受。它不批准 I Sequencer 实现、Storage Database/XA Capability、COC 部署/运维方、H Schema、实现、Conformance 或 Production Activation。D36 和 JF10-COC-01..10 仍为 NOT RUN。JF-10 仍为 P0 OPEN；Multi-policy-domain Atomicity 仍为 BLOCKED。

## Phase 3.6.2 — D 对完整 JF-10 ↔ COC 决议包的精确接受

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS。** 该接受严格限于单一 I-PolicyDomain JF-10 v2 Profile 下 D-owned ForgetFence、Producer Registration、Dependency Inventory、Lineage 和 Barrier 语义。它不是 I Authorization 批准、Storage Capability 认证、C Provider 批准、H Production Schema Freeze 或 Production Implementation Acceptance。

### 审查的准确决议包

- A COC Architecture：a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d
- I JF-10 v2 Owner Disposition：8069ff86988396442c8d9dc3fd58653683abe2f3
- D/E/Storage Common JF-10 v2 Recovery Protocol：94679897e84a6f58fd8b9467b5249e1a885cb0b0
- C Bridge Owner Contract：45a48249717c8cddb07ab96197730ef93d406c22
- D Fence/Barrier Owner Contract：5a56c406578fdf257509315eb3f6f3f75456116c
- Storage Realization/Participant Contract：55c01f4512f2e3d8aac767dd004e768ae073178e
- H Bridge Wire Mapping Owner Contract（当前分支回读）：e7ca5ce4ece5d8fd77fe0760e49a85afa0133248
- H JSON Schema Candidate：a8a945cc3623c2907003b93625e3c79742150944

### D-owned 接受的语义

1. 在 D Fence Cutoff 之前，由 COC Quorum Commit 的 Prepare-intent Registration 是 Prospective D Barrier Participant，即使 Storage Prepared Receipt 尚未登记。D Cutoff 若先于 Prepare-intent，则拒绝受影响 Prepare。
2. 同一个预分配 XID/Participant Identity 必须贯穿 Storage PREPARE、I Terminal Decision 和同 XID Commit/Rollback Resolution。XID、Digest、Owner Boundary 或 Lineage Binding 变化都构成 Conflict。
3. Participant-first 保留 D Target/Lineage Serialization，并保持 D Barrier 开放，直到 I Terminal Evidence、Storage 同 XID Resolution、必要时的 C Provider Outcome，以及 D Lineage Obligation 均获得权威证明。Fence-first 则拒绝。不存在第三种顺序。
4. UNKNOWN/IN_DOUBT、COC Outage、缺失 Log Prefix、Stale Replica、Lost ACK、缺失 Participant Row 或 Owner Proof 不完整，都不能释放 Barrier 或建立 CanonicalSuppressionComplete。
5. D 保留 ForgetOperation、ForgetFence、ProducerRegistrationHighWater、BarrierSnapshotReceipt、Target/Ancestor Coverage 和 D Completion 的唯一权威。COC/I/Storage Position 是不同类型化 Evidence；D 不比较它们，也不根据 Wall-clock 推断顺序。
6. Outage Recovery Batch 和 Owner-local Pending-gate Rule 只作为 Fail-closed Coordination Evidence 接受。只有在 Durable Cutoff、完整 Fence 前 Participant Reconciliation 和 D Owner High-water Verification 后，D 才能重新开放本地 Gate。
7. 接受范围仅限一个 I PolicyDomain。Multi-PolicyDomain Atomicity 仍为 BLOCKED / NOT ACCEPTED。

### 明确例外 / 关闭条件

- 这是架构/接口接受，不是实现验收。D API、Durable Ledger、Lock、Participant Recovery、COC Deployment 和 Production Conformance 均 NOT VERIFIED。
- Storage 必须证明所选 DB 的实际 Prepared-XID/Lock Retention、同 XID Restart/Failover Recovery 和 Atomic Visibility Transaction。D 不选择或认证 DB Engine。
- I 拥有 Sequencer、Receipt Consumption、PermissionEpoch 和 Revocation Effective Point；D 的接受不认证 I 实现或外部治理。
- C Provider Idempotency/Outcome、H Generated Schema/Parser/SDK Interoperability，以及 COC Consensus/Quorum Durability 仍由各自 Owner 负责且未验证。
- D36、JF10-01..13、Storage Crash/Fault 和 Cross-owner Conformance 仍 NOT RUN。JF-10 P0 仍 OPEN；未授权 Production Activation 或 Merge。
