# Forget Fence 原子性、Producer Admission 与 Publication Gate — 第 2 部分

- 文档 ID：D-FORGET-GATE-001-P2
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：DEREFERENCED — 保留历史源 Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`；当前仓库不存在可解析的规范性源文件。
- 对应英文：[Part 2 — Derivative Visibility, Evidence, Fault Matrix and Decisions](../../en/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md)
- 源规范：DEREFERENCED — 原规范源路径 `03-memory-brain/forget-fence-operation-and-publication-gate.md` 在当前 main tree 中不存在；替代物：[英文对照版](../../en/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md)（Blob `5a5e084e4af57a9017a38da03c950fd209ce9054`；仅为对照文本，不是规范性替代源）。
- 覆盖源规范第 6–11 节

## 6. 派生物可见性的原子边界

Artifact 对消费者可见的状态，与最终 Fence/Permission 决策必须具有同一个外部可观察的线性化点。D 拥有语义规则；Storage/Consistency 必须指定并验证具体实现。

1. Staged Artifact 默认保持 Private；任何面向消费者的 Index、Outbox、Cache、Canonical Read 或 Context Input 都不得枚举它。
2. D Dependency Registration 必须在 Publication 前持久化 Artifact Identity 和每条直接/传递 Source Edge。
3. Final Gate 校验 RegistrationReceipt、全部 DependencyRegistrationReceipt、Work/Attempt/Lease 是否仍有效、准确 ScopeRefs、每个 Source Ancestor 的当前 Fence 状态，以及 I 当前 PermissionEpoch/Authorization Decision。
4. 同一个原子/可线性化 Commit 必须记录成功 PublicationReceipt，并翻转权威 Visibility Marker。如果 Commit Abort，则既不能存在成功 Receipt，也不能存在 Visible State。
5. 跨 Store Prepare/Commit 只有在 Prepare 始终隐藏、Commit 是绑定准确 Fence/Permission Decision 的一次性 CAS/Transaction、Fence Installation 与 Commit 串行化，并且 Recovery 永不在缺少已提交 Proof 时暴露 Prepared/Unknown Artifact 的前提下才允许。
6. Crash、Replay、Rebuild 或 Restore 后，只能根据已提交 Publication Record 重建 Visibility；暴露前还必须根据最新 Fence 重新校验。单独重放 Dependency Record 不能让 Artifact 变为 Visible。

ACK 丢失时，使用相同稳定 Operation ID/Digest 调用 ResolveProducerWork。若已提交，返回原 Receipt；否则使用相同幂等 Key Retry。绝不能创建新 Artifact Identity 或 Publication Key 来绕过不确定状态。

## 7. Publish Gate Evidence — 最低不可变绑定

每个 PublicationReceipt 必须绑定：
- WorkItemId 和 AttemptId；使用 Lease 时还包括 LeaseId；
- ProducerClassId 和 ProducerRegistryVersion；
- DerivationRunId；
- Source MemoryVersionRef、准确 SourceRevision 和完整传递 Lineage Digest；
- ScopeRef 集合以及 Scope/Tenant/Security Domain Binding；
- Producer RegistrationReceipt ID + Request Digest + ProducerRegistrationSequence；
- 已观察 ForgetFenceCursor 和 Commit 时的权威 Fence Decision（分别使用不同类型）；
- I PermissionEpoch + Authorization Decision Reference/Result；
- DerivedArtifactRef/Version 和 Private Staging Object/Version Identity；
- 每个 DependencyRegistrationReceipt ID、Inventory Position 和 Lineage Digest；
- PublicationOperationId、Request Digest、Visibility Commit ID/适用时的 CanonicalCommitCursor，以及最终 Disposition。

不得把 FenceGeneration 和 PermissionEpoch 放进共享整数栏位，也不得进行数值比较。可能在 Lease 替换后迟到返回的 Worker，必须记录 AttemptId。Receipt 不可变且不能反向重建内容：只包含标识符、Digest 和结果，不包含已遗忘明文。

## 8. E / Storage / I 接口映射

| 边界 | D 提供/决议 | E 消费/产生 | 其他 Owner / OPEN |
|---|---|---|---|
| Producer Class | Registry Identity/Version/Status/Receipt 和封闭世界完整性 | 接纳 Work 前登记 Compiler/Replay/Rebuild Class | I/A 协调跨 Producer Domain 的 Registry Inventory；Owner Mapping 未决 |
| Work Admission | RegistrationReceipt、High-water Sequence、Disposition 和 Barrier Membership | Retry 使用稳定 WorkItemId；没有 Receipt 不得 Queue/Lease/Run；ACK 丢失时 Lookup | H/I 认证 ProducerIdentity 和 Scope/Permission 校验仍 OPEN |
| Fence Install | ForgetFenceCursor、Install Commit Cursor、捕获 Registry Version + Work High-water + Target Snapshot | 停止/停放受覆盖 Work，并传播类型化 Fence | Storage/Consistency 证明 Registration/Fence 串行化 |
| Dependency Inventory | 持久化 Dependency Receipt 和 Inventory Position | 可见前登记全部直接/传递 Lineage；Staged Output 保持 Private | E 负责产生 Lineage；B Typed-ref Vocabulary 可能仍受 ADR 阻塞 |
| Publish Gate | 最终权威 Fence/Registration Decision 和 PublicationReceipt 语义 | 提交 Evidence；只有成功 Commit Receipt 后才暴露 | Storage/Consistency 原子耦合 Gate/Visibility；I 提供当前 Permission Decision |
| Terminal Work | 已验证 Terminal Receipt 和 Barrier 更新 | 保留 DLQ/Retry/Lease Identity；无剩余 Publish Path 后才提交 Terminal | E 拥有 Terminal Truth；D 校验 Barrier Evidence |
| Reconciliation | 带准确 High-water 和未解决数量的 D Barrier Receipt | 提供 Registration/Dependency/Publication/Terminal Evidence | I 消费 D 结果，但决定 Global Completion |
| Global Forget | 仅 D-local Canonical Suppression Proof | 不得声称 Global Completion | I 拥有 Policy、Exceptions、Backup/External-copy 和 Physical Erasure |

### 8.1 Storage/Consistency 验收要求 — Owner 未指定

实施批准之前必须明确指定 Storage/Consistency Owner。该 Owner 必须选择并验证以下一种方案：
- 一个 ACID Transaction 同时覆盖 Fence State、Registration Ledger/Dependency Record 和 Artifact Visibility Marker；
- 共享可线性化 Fence Version/Publication Decision 的 Serializable Transaction 或 Conditional Write/CAS；
- Durable Transactional Outbox + Hidden Prepare/Commit Protocol，且 Recovery 保证 Commit 前不可见；
- 其他有正式规范、明确 Serialization Point 和 Crash-recovery Proof 的等价方案。

必须提供的证据：Isolation/Consistency Model；Transaction Participant；Linearization Point；Idempotency/Uniqueness Constraint；每次 Durable Write 前后注入故障；Crash Recovery；并发 Register/Fence/Publish 测试；Replica/Read Consistency；Backup/Restore 后重新应用 Fence；证明陈旧 Token 无法在更新 Fence 后 Publish。D 不选择或认证特定 Database、Lock Manager 或 Distributed Transaction 产品。

**OPEN：在已审查的契约集合中，尚未找到正式命名的 Storage/Consistency Owner 或实现证据。**

## 9. Fault/Race Conformance Matrix — 设计预期，NOT RUN

| # | 初始状态 | 交错/故障 | 必需结果 | 禁止结果 |
|---:|---|---|---|---|
| 1 | Class Enabled；Work 不存在；Fence 不存在 | RegisterProducerWork 与 InstallForgetFence 竞争 | 共享串行化得到：Accepted 且 Sequence <= 捕获的 H，或 Fence 后 Rejected/Quarantined | Accepted Work 不在 H 中却仍可运行/发布 |
| 2 | Fence 已安装；Registration 已 Commit 但响应丢失 | E 用相同 WorkItemId/Digest Retry 或 Resolve | 返回相同 Receipt/Sequence；若 Fence 获胜，则权威拒绝 | 新 Work ID、重复 Ledger Row、假定 Accepted |
| 3 | Work 已登记；Artifact 私有 Staged；Dependency Receipt 已持久化 | Publish 前 Crash | Artifact 保持 Private；Recovery 使用相同 ID 并重新检查 Fence/Permission | 重启/Replay 时 Staged Artifact 可见 |
| 4 | Publish 已 Commit；响应丢失 | E 用相同 PublicationOperationId Retry | 返回相同 PublicationReceipt；Visibility 与已提交 Receipt 一致 | 重复发布，或无 Receipt 的可见 Artifact |
| 5 | Work 在 Attempt A / Lease L1 下已 Lease | Lease 过期；Worker B 用 Attempt B / Lease L2 Retry | 相同 WorkItemId/Lineage；旧 Attempt 被 Fence；新 Attempt 刷新 Permission/Fence | 过期自动关闭 Barrier，或旧 Attempt 发布 |
| 6 | Work 在 DLQ；Registration 仍开放 | Operator/System Replay Item | 相同 WorkItemId/Lineage、新 AttemptId；重新授权/检查 Fence；Barrier 仍开放 | 新建未跟踪 Admission，或将 DLQ 当成 Terminal |
| 7 | Dependency Inventory 已包含 Artifact Lineage | Index/Backfill/Rebuild 重放旧 Staged/Visible Data | Rebuild 使用已提交 Publication State 和当前 Fence；受覆盖 Artifact 在 Index Visibility 前被抑制 | Replay 未重新检查 Fence 就使 Artifact 可见 |
| 8 | Artifact 在 Fence G 时已 Staged 且 Dependency Registered | Final Publish 前 Fence 推进到 G+1 | Final Gate 看到最新 Fence 并拒绝/隔离；没有 Visibility Commit | Staging 时观察到的 G 授权后续 Publication |
| 9 | Admission 时观察到 PermissionEpoch P | Final Publish 前 I 撤销/推进 Policy | Final Gate 的 I Decision 拒绝/标记过期；Artifact 保持 Private | 与 FenceGeneration 数值比较，或把 Admission Epoch 当成永久授权 |
| 10 | ProducerClass 缺失/禁用/未知 | Producer 尝试 Registration/Submit | Reject/Quarantine；Audit；Registry 不完整时 Barrier 不能证明关闭 | 首次 Work 自动注册，或允许旁路 Publish |

其他强制变体：部分 Dependency Receipt；相同 Key/不同 Digest；Fence Lookup 不可用；Terminal ACK 丢失；既有 Proof 后出现迟到派生物；重叠 Forget Fence；从 Backup Restore；Publication CAS Conflict；Permission Lookup Timeout。所有场景均 Fail-closed，并要求确定性 Reconciliation。

## 10. 决议状态与未解决 Owner

| 项目 | 决议 | Owner / 下一步 |
|---|---|---|
| Operation 语义和幂等性 | DECIDED — D Semantic Contract | D 维护规范 Operation 含义 |
| Register/Fence 全序及双结果竞争 | DECIDED — D Semantic Contract | Storage/Consistency 实现并证明共享串行化 |
| Dependency-before-visible 规则 | DECIDED — D Semantic Contract | E 产生 Lineage；Storage/Consistency 证明 Visibility Boundary |
| Publish Gate Evidence | DECIDED — D Semantic Contract | I 提供 Permission Decision；E 提供 Work/Attempt Evidence |
| PermissionEpoch/Revocation Policy | OPEN / I-owned | I 定义当前 Decision 语义和查询 |
| Authenticated ProducerIdentity / ActorRef / ScopeRef | OPEN / I-H-B-owned | I/H/B 对齐身份和类型化引用；D 消费已验证引用 |
| Producer Class 全局完整性 | OPEN / I + A + 模块 Owner | 将 D Local Registry 与 I Global Producer/Recipient Inventory 对齐 |
| Storage Transaction/CAS/Lock/Consistency | OPEN — OWNER UNASSIGNED | Architecture/Engineering 指定责任 Owner；D 不得自我批准 |
| E Operation/API Mapping 和 Terminal Evidence | OPEN / E + D | E 将 Compiler State 映射到语义；D 定义 Receipt 语义 |
| H/F/G Producer/Consumer Enforcement | OPEN / H/F/G | 各 Owner 提供自己的符合性证据；D 不修改其文件 |
| Global Forget、Exceptions、Backup/External Copies、Physical Erasure | OPEN / I-owned | I 决定 Policy 和 Global Proof |
| Runtime/Fault-injection Tests | NOT RUN | Storage + E + D + 相关 Consumer 附上证据 |

## 11. D-local 验收与非声明

D-local 文档验收要求：Operation Contract 清晰无歧义；Register/Fence 两种结果的排序明确；PublishReceipt 最低 Evidence 完整；全部十种 Fault/Race Scenario 的预期结果确定。本文仅满足文档/设计规范标准。

本文不证明 D API 已存在、E 已消费最终批准 Schema、Storage Atomicity 已实现、任何 Fault Test 已通过、H/F/G 符合要求、I 已批准 Global Policy，或 Forget 已端到端/物理完成。D-REV-P1-003 仍为 Integration-open，直到 Owner 实现和 Conformance Evidence 经审查。
