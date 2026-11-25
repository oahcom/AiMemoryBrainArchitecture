# Forget Fence 原子性 — 第 3 部分：Phase 3.6 线性化与证明矩阵

- 文档 ID：D-FORGET-GATE-001-P3
- 源文件版本：d3ddfff9500d9138d643989e8496d99b8d9ed79e
- 源分支：session-d-memory-brain-2026-11-16
- 对应英文：[Part 3 — Phase 3.6 Linearization and Proof Matrix](../../en/03-memory-brain/forget-fence-operation-and-publication-gate-part3.md)
- 源规范：[D 规范源](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md)（源提交 `b525e1f8fee2471a131e4a38efda99804045e424`；原始源 Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`）。

**Owner：** Session D — Memory Brain Principal Architect  
**状态：** D 拥有的领域语义为 DECIDED；E/Storage 执行、I 授权新鲜度和跨模块一致性为 OPEN。  
**权威性：** 本补充对 D 的 Canonical Forget 语义具有规范效力。它不选择数据库、不声称事务协议已部署，也不声称实现/测试成功。

## 1. Forget 原子性不变量

### 1.1 唯一安全不变量

对于每个具备派生能力的 Producer Work W，以及每个由 W 直接或传递派生的 Artifact A：

> **除非 W 已持久登记、W 已被每个适用 Forget Barrier 核算、完整 Dependency Lineage 已持久登记，并且最终 Visibility Decision 已针对准确 Principal、Scope 和 Artifact 校验当前适用 ForgetFence 与 I 当前授权/PermissionEpoch，否则 A 绝不能进入任何可检索、可投递、可索引、可推理、可被外部枚举或以其他方式对消费者可见的状态。**

等价的 Fail-closed 表述：

> 任何未被适用 Forget Barrier 捕获的 Producer Work，或未在最终 Visibility Boundary 通过当前 Fence/Authorization 检查的 Producer Work，**MUST NOT** 导致派生物可见。

Queue、Lease、Worker 本地状态、Staged Object、Accepted Event、Dependency Receipt、Gate Response、缓存授权结果、Outbox Message、Replay Token 或历史 Publication Receipt，都不能单独授予 Visibility。

### 1.2 不同的持久化阶段

| 阶段 | 含义 | 必需持久化证据 | 不代表什么 |
|---|---|---|---|
| Work Registration | D 接纳一个带 Source/Lineage/Scope Binding 的稳定逻辑 ProducerWorkItemId | RegistrationReceipt、Request Digest、ProducerRegistryVersion、ProducerRegistrationSequence、Disposition | Work 已被之后安装的 Fence 捕获 |
| Barrier Capture | InstallForgetFence 对其线性化点之前排序的全部已接纳 Work 进行 Snapshot | ForgetFenceCursor、不可变 BarrierSnapshotReceipt、ProducerRegistrationHighWater、Registry Version、Target Digest | 被捕获的 Work 获准 Publish |
| Dependency Registration | 完整 Artifact Identity 和必需的直接/传递 Source Edge 已写入 D Dependency Inventory | DependencyRegistrationReceipt、完整集合/Lineage Digest、Inventory Position | Artifact 已可见 |
| Staging | E 或其他 Producer 将不可变 Candidate Bytes/Metadata 写入 Private Namespace | ArtifactRef/Version、Payload Digest、Private-stage Identity、WorkItemId | Artifact 已登记或可见 |
| Publish Authorization | Final Gate 校验 Work、Attempt/Lease、Dependency、当前 Fence、当前 PermissionEpoch 和 Principal/Scope 授权 | 绑定准确 ID、Digest 和当前 Authority Decision 的不可变 Gate Decision | Visibility 已提交 |
| Durable Commit | 一个外部可观察 Commit 同时持久化 Publication Decision 和权威 Visibility State，或完成已证明等价的协议 | PublicationReceipt、Commit Identity/Cursor、权威 Visibility Marker、Recovery Evidence | 所有消费者都已刷新 Cache |
| Artifact Visibility | 消费者可以通过权威 Visibility Predicate 发现/读取/投递 Artifact | 已提交 PUBLISHED Receipt，且受保护读取仍执行当前 Fence/Authorization | 物理擦除或 Global Forget 完成 |
| Terminal Disposition | 只有所有 Output 和所有未来 Publication Path 都已核算，D 才关闭逻辑 Work Item | ProducerWorkTerminalReceipt、最终 Attempt/Lease Epoch、Output/Dependency/Publication Inventory、无未来发布证明 | Queue 删除、Lease 过期、DLQ 停放或 Worker 退出 |

阶段顺序具有规范效力，但并非每个 Work Item 都必须走到每个阶段。Rejected、Suppressed 或 Cleanup-only Work 可以在不 Staging/Publication 的情况下终结。一个阶段的 Receipt 不能替代后续阶段 Receipt。

### 1.3 Barrier 与 Visibility 规则

1. Registration 必须先于 Enqueue、Lease Acquire、受保护 Payload Dereference、Execution、Retry、DLQ Replay 或 Publication 持久化。
2. Registration 和 Fence Installation 必须针对每个受影响 Canonical Memory Authority 和适用 Lineage 共享一个可线性化排序域。
3. 在 Fence Installation 之前排序的每个 Accepted Registration 都必须纳入不可变捕获 High-water。Fence 之后排序的 Registration 必须被拒绝/隔离，或明确作为 Cleanup-only 接纳且不具备普通 Publication 能力。
4. Barrier Capture 使 Fence 前 Work 可核算；它不授予 Publication Permission。
5. 完整 Dependency Registration 必须先于 Visibility。Dependency 不完整、部分完成或 Unknown 时，Artifact 保持 Private。
6. Final Publication 必须在 Visibility Linearization Point 校验每个 Source Ancestor、Target、ScopeRef、当前 Fence 和 I 当前授权。
7. 任意 Commit 不确定、Receipt 缺失、Authority 不可用、Lease 过期、PermissionEpoch 陈旧、Fence Unknown、Lineage 不完整或 Idempotency 结果未解决，都必须保持不可见且未解决。
8. Lease 过期、DLQ 状态、Retry 延迟、进程消失和 Queue 删除永远不能关闭逻辑 Work Item。
9. 迟到派生物或新发现的 Lineage Edge 会使当前 Barrier Proof 失效，并要求抑制和协调；不能静默改写历史。
10. 任何 Consumer 都不得通过直接读取 Staging Storage、Object Path、Cache、Index、Outbox Payload、Delivery Queue 或陈旧 Snapshot 绕过权威 Visibility Predicate。

## 2. Operation Linearization Table

Linearization Point 是决定外部可观察顺序的单个持久化事件。下列 Evidence 是必需契约，不代表当前系统已经能够产生它。

| Operation / 竞争 | Linearization Point | 唯一合法结果 | 最低持久化证据 |
|---|---|---|---|
| RegisterProducerWork vs InstallForgetFence | 两个操作在同一 Authority/Lineage 排序域中的 Commit | Registration 先：Accepted Sequence s 纳入且 s <= 捕获 H。Fence 先：普通 Work 被拒绝/隔离或仅 Cleanup-only。不存在已 Accepted 但未捕获 Work | RegistrationReceipt + Sequence + Digest；ForgetFence Receipt + Generation + 不可变 H + Install Cursor；共享顺序/Commit Evidence |
| RegisterDerivedDependency vs InstallForgetFence | 完整 Dependency Set 在相同适用 Fence 排序域中的 Commit | Dependency 先：完整 Artifact/Edge 已持久化并纳入 Fence Reconciliation；Fence 先：覆盖 Lineage 的 Registration 被拒绝/隔离，Artifact 保持 Private | DependencyRegistrationReceipt + 完整 Lineage Digest + Inventory Position；Fence Receipt/H；Commit Order |
| PublishDerivedIfFenceCurrent vs InstallForgetFence | 与 Fence Installation 排序的原子/可线性化 Visibility Commit | Publish 先：Artifact 在 Fence 前已可见，必须纳入 Dependency/Barrier Inventory 以便抑制/协调。Fence 先：Publish 被拒绝/隔离。不存在第三种状态 | PublicationReceipt + Visibility Commit Identity；权威 Fence Receipt/Generation；Dependency Receipt；Serialized Commit Trace |
| PublishDerivedIfFenceCurrent vs Permission Revocation | Final Visibility Commit 必须依据 I 定义的撤销新鲜度语义，消费/校验 I 权威的当前 Authorization Decision | Revocation 先：拒绝。Publication 先：在 Commit Point 已获授权；后续撤销按 I Policy 向未来生效。如果无法确定当前性/顺序，保持 Private | I Decision Ref + PermissionEpoch + Principal/Scope Binding + Decision Freshness Proof；Publication Commit Record。跨服务精确排序仍由 I/Storage OPEN |
| CompleteProducerWork vs Crash Recovery | D Barrier Ledger 中不可变 Terminal Disposition 的 Commit | Terminal 先提交：Recovery 返回相同 Terminal Receipt。Terminal 前崩溃：Work 仍开放，Recovery 使用同一 WorkItemId 协调。不得从消失推断 Terminal | ProducerWorkTerminalReceipt + 最终 AttemptId/LeaseEpoch + Output Accounting Digest + Terminal Commit Cursor |
| 不确定结果后的 ResolveProducerWork | 对原始稳定 ID/Digest 的权威一致读取 | 返回原 Receipt/State 或 UNKNOWN；Lookup 不创建第二个 Operation | Lookup Key、原 Digest、权威 Ledger Snapshot/Version 和返回 Receipt |
| ReconcileForgetBarrier | 对不可变 Barrier/Dependency/Target Checkpoint 的一致读取 | DRAINED 仅对准确命名的 Checkpoint 有效；后续 Evidence 创建新 Checkpoint 或重新打开 Proof | BarrierSnapshotReceipt、Registry Version、High-water、Dependency Inventory Position、Reconciliation Receipt 和未解决数量 |

**Permission 竞争限定：** D 不拥有 I 的 PermissionEpoch 或 Revocation Ordering。D 要求 I 提供权威、当前、可用于 Commit 的 Decision。陈旧缓存 ALLOW、调用方自报 Epoch 或数值比较永远不够。在 I 与 Storage 明确规定并证明 Revocation Freshness 如何绑定最终 Visibility Commit 之前，该部分 CR-P1-01 仍为 OPEN，实现必须 Fail-closed。

## 3. Producer Work 状态机

### 3.1 状态

| 状态 | 含义 | Publication 能力 |
|---|---|---|
| Registered | 稳定 WorkItemId 和 D 持久 Registration Receipt 已存在 | 后续检查之前无 |
| CapturedByBarrier | 已安装 Fence 的不可变 Barrier Snapshot 包含该 Work | 不因被捕获而获得任何能力 |
| Staged | Candidate Artifact 仅存在于 Private Staging | 禁止 |
| DependencyRegistered | 完整 Dependency Set 已持久记录 | Final Gate 前禁止 |
| PublishEligible | 所有前置条件当前看似满足；这是可撤销评估，不是持久许可 | 无独立能力；Commit 时必须重新校验 |
| Published | 准确 Artifact/Version 已有已提交 PUBLISHED Receipt 和权威 Visibility Marker | 仅在当前 Read-time Fence/Authorization 允许时 |
| Suppressed | Work/Output 已持久阻止普通 Publication/Exposure | 禁止 |
| Rejected | Admission、Dependency 或 Publication 已持久拒绝 | 禁止 |
| RetryPending | 相同逻辑 WorkItemId 仍开放；新 Attempt 通过重新检查后可签发 | 旧/未校验 Attempt 禁止 |
| Terminal | 持久化最终处置证明不存在未解决或未来 Publication Path | 禁止；除非是未源自受 Fence 约束 Lineage 的独立新 Work |

### 3.2 允许转换与 Guard

- ABSENT → Registered：仅在 RegisterProducerWork 持久化接受后。
- Registered → CapturedByBarrier：仅当已提交 Fence Snapshot 包含 Registration Sequence。
- Registered → Staged：仅在 Receipt 有效且执行前 Authorization/Fence 检查当前有效后。
- CapturedByBarrier → Staged：Fence 前已运行 Work 可以继续 Staging，但不因此获得 Publish Permission；Final Gate 仍然适用。
- Staged → DependencyRegistered：仅在完整必需 Dependency Set 拥有持久 Receipt 后。
- DependencyRegistered → PublishEligible：仅在当前 Work/Attempt/Lease、Source Revision、Scope、Fence 和 Permission 检查通过后。
- PublishEligible → Published：仅在原子/可线性化 Visibility Commit 和已提交 PublicationReceipt 时。
- 任意非终态 → Suppressed：仅在具有持久抑制/隔离 Evidence，并证明没有任何 Attempt 以后还能 Publish 时。
- 任意 Admission/Gate State → Rejected：仅在具有持久类型化拒绝 Receipt 时。
- Registered/CapturedByBarrier/Staged/DependencyRegistered → RetryPending：必须保留 WorkItemId 和 Lineage；旧 Attempt/Lease 失效。
- RetryPending → Registered：解析相同逻辑 Registration，再建立新的 AttemptId/LeaseEpoch；这不是新的 Admission。
- Published/Suppressed/Rejected → Terminal：仅当所有 Output 和未来 Publication Path 均已核算，并且 D 提交 Terminal Evidence。
- Terminal 对该 Work Identity 不可变。迟到 Evidence 不改写它；它会使适用 Forget Proof 失效/重新打开，并创建可审计的 Reconciliation Obligation。

未登记、Unknown、部分登记、Authorization 陈旧、Fence 陈旧或 Dependency 不完整状态，不得转换到 Published。PublishEligible 不是 Bearer Token，任何绑定前置条件变化都会使其失效。

### 3.3 Retry、Lease 与 Replay Identity

WorkItemId 是 Retry、Lease 替换、DLQ Replay 和 Worker Recovery 期间的根 Barrier Identity。AttemptId、LeaseId 和单调 LeaseEpoch 只标识执行。被替换或过期的 Attempt 不能使用陈旧 Lease Evidence 登记 Dependency、Publish 或 Terminalize。Recompile 创建新的 DerivationRunId，明确关联原 Source Lineage，并要求 D 明确 Admission/Re-admission 决策；不能重置 Lineage 或绕过活动 Fence。

## 4. Fence / Permission 双重校验契约

FenceGeneration 和 PermissionEpoch 是由不同 Authority 拥有的独立类型化 Namespace。

最终 Visibility Commit 前，以下条件必须全部成立：

1. **Current Fence：** D 为 Artifact、每个 Source Ancestor 和准确 Target/Version Family 确定最新适用 ForgetFence。Fence Unknown/不可用即拒绝。
2. **Current Permission：** I 根据自己的 Policy Domain 语义确定当前 PermissionEpoch 和 Authorization Decision。陈旧、已撤销、Unknown 或不可用即拒绝。
3. **Principal Binding：** 认证 Principal/ProducerIdentity 由 I/H Trust Mechanism 验证；Payload Identity 不是证明。
4. **Scope Authorization：** 每个 Source/Target ScopeRef 都有效，并且已针对认证 Principal 和 Producer Operation 授权。Scope 不匹配或 Binding 缺失即拒绝。
5. **Work State：** WorkItemId 已持久登记、未终结、具有正确 Forget Barrier Disposition，且 Producer Class 已获准执行该操作。
6. **Attempt/Lease State：** AttemptId 和 LeaseId（如使用）仍然当前有效；LeaseEpoch 未被替换或过期。
7. **Dependency State：** 每个必需直接/传递 Dependency Receipt 都已持久化、完整、不可变，并绑定准确 Artifact/Version、WorkItemId 和 Lineage Digest。
8. **Artifact Binding：** Staged Artifact Identity/Version 和 Payload Digest 与 Publication Request/Dependency Receipt 匹配。
9. **Atomic Visibility：** 上述 Predicate 与 Visible Transition 构成一个外部可观察 Linearization Point，或由已证明等价的崩溃安全协议实现。

禁止：
- 比较、递增、转换或替代 PermissionEpoch 与 ForgetFenceGeneration；
- 把 Admission 时的 Authorization 或 Observed Fence 当作最终授权；
- 把 D Fence Receipt 当作 I Permission；
- 把 I Permission Decision 当作 D Fence 豁免；
- 在 Visibility Commit 时不重新验证当前 Fence/Permission，仍接受旧的一次性 Token；
- 任何必需检查 Unknown 时暴露 Artifact。

## 5. Storage 语义要求（与实现无关）

D 只规定可观察语义。Storage 可以选择 Database Transaction、Linearizable Conditional Write/CAS、Coordinator、Durable Prepare/Commit Protocol、Distributed Transaction 或其他机制，但必须证明相同的外部可观察行为。

Storage **MUST** 证明：

1. 对每个适用 Authority/Lineage，RegisterProducerWork 与 InstallForgetFence 之间具有持久化全序。
2. Fence Installation 和捕获的 ProducerRegistrationHighWater 是一个不可分割的可观察决策；Retry 返回相同 Generation 和 H。
3. 完整 Dependency Registration 在 Visibility 前持久化；部分/Unknown Set 不可 Publish。
4. 最终 Fence + Permission + Work/Lease + Dependency Validation 与 Visibility Commit 绑定。先检查再执行不相关写入不够。
5. Crash、Failover、Retry 或 Restore 后，成功 PublicationReceipt 与权威 Visibility Marker 不得互相矛盾。
6. 稳定 ID 和 Canonical Request Digest 使所有操作幂等；相同 ID/Digest 返回原结果；相同 ID/不同 Digest 冲突。
7. Unknown Commit Outcome 必须能通过原 ID 查询，并在解决前保持隐藏。
8. Lease 替换具有单调 Fencing Epoch 或等价条件，以拒绝陈旧 Worker。
9. Outbox Delivery 可 Replay/幂等，但它本身不是安全串行化机制。
10. 每条 Consumer Path 都使用权威 Visibility Predicate；Staging Bytes、Object URL、Index、Cache、Delivery Queue 和 Rebuild 不得绕过它。
11. Restore/Rebuild 从隔离状态开始，在提供服务前重新应用当前独立 Forget/Revocation Control State。
12. 必须针对实际部署配置提供 Durability、Replication、Failover、Isolation、Read Consistency、Retention 和 Backup 行为证据。

D 不强制指定 Database、SQL Isolation Level、Lock Type、供应商功能或物理拓扑。某种机制的描述听起来像 Serializable，不代表它已被接受。

### 5.1 明确拒绝条件

D 拒绝任何允许以下行为的实现：
- 本地读取 Fence，随后执行独立 Visibility Write；
- 仅依赖 Queue Order 或进程内 Mutex 决定 Registration/Fence 顺序；
- Accepted Work 未纳入捕获 H；
- Dependency Set 部分完成后 Artifact 仍可见；
- Gate ACK 后通过独立暴露操作发布 Artifact，且没有 Commit-bound Protocol；
- Fence 推进/Permission 撤销后仍可使用可 Replay/陈旧 Publication Token；
- 使用 Lease Expiry 或 DLQ Parking 关闭 Barrier；
- 直接读取 Object Store/Index/Cache/Delivery 绕过已提交 Visibility；
- 从旧 Snapshot 恢复后，未重放当前 Control Ledger 就提供服务；
- 将 Unknown Outcome 解释为成功。

当前 Storage 提出的 Shared Transactional Coordinator 在方向上兼容这些要求，但仍为 PROPOSED / NOT IMPLEMENTED；不能据此声称已具备原子性。

## 6. Fault / Race Proof Matrix

本矩阵是设计验收期望，**NOT RUN**。每一行都需要可重复的 Fault Injection、持久化证据和恢复后状态检查。

| # | 故障/竞争 | 必须证明的安全结果 | 必需 Evidence |
|---:|---|---|---|
| 1 | RegisterProducerWork 与 Fence Installation 并发 | 只能得到 Registration-first（纳入 H）或 Fence-first（拒绝/隔离）；不能漏掉已 Accepted Work | Receipt、Sequence、Fence Cursor、H、Commit Order |
| 2 | Fence 前 Registration 已提交但 ACK 丢失 | 相同 Work ID/Digest 返回原 Receipt；若 Fence 已获胜则权威拒绝 | 原 Registration Receipt、Fence Snapshot、Lookup Result |
| 3 | Dependency Registration 部分写入后 Crash | Artifact 保持 Private；恢复补齐完整 Set 或隔离 | Dependency ID/Digest、完整 Edge Inventory、Visibility Marker |
| 4 | Dependency 已提交、Publish 前 Fence 推进 | Final Gate 拒绝；没有 Visibility Commit | Dependency Receipt、Fence Generation、Gate Result |
| 5 | Publish 与 Fence 同时提交 | 一个 Linearization Point 决定先后；Publish-first 纳入 Barrier，Fence-first 拒绝 | PublicationReceipt、Fence Receipt、Serialized Commit Evidence |
| 6 | Final Gate 后、Visibility Commit 前 Crash | 恢复时重新解析同 Operation；没有证明 Commit 前保持 Private | Operation ID、Prepare/Commit Record、Visibility Marker |
| 7 | Visibility Commit 成功但 ACK 丢失 | Lookup 返回原 PublicationReceipt；不重复 Publish | PublicationOperationId、Digest、Commit ID、Receipt |
| 8 | PermissionEpoch 在 Staging 后被撤销 | Final Gate Fail-closed；陈旧 ALLOW 不可用 | I Decision Ref、Epoch、Final Gate Decision |
| 9 | Lease 过期且旧 Worker 迟到 | 旧 Attempt 被拒绝；新 Attempt 复用 WorkItemId 并刷新控制状态 | WorkItemId、Attempt/Lease Epoch、Final Gate Result |
| 10 | DLQ/Retry/Replay 在 Fence 后恢复 | 重新授权/检查 Fence；被覆盖 Lineage 不得 Publish | Work/Attempt Identity、Replay Receipt、Fence/Permission Decision |
| 11 | Index Rebuild/Backfill 重放历史 Staged/Published Record | 只有已提交 PUBLISHED Record 是候选；提交 Index 前重新检查当前 Fence/Permission 和 Source Ancestry | Rebuild Work Receipt、PublicationReceipt Lookup、Fence/Permission Decision、Index Watermark |
| 12 | Adapter 在 Forget Fence 或 PermissionEpoch 变化后重连，Replay 旧 Delivery | 旧 Delivery 被抑制/取消，或从当前授权 Context 重建；交付前重新验证 | DeliveryId/Attempt、认证 Adapter/Session、Fence/Permission Decision、ACK |
| 13 | Barrier Checkpoint 或表面完成后出现迟到派生物 | 立即隔离/抑制；记录 Lineage 和 Producer Class 缺陷；使旧 Proof 失效/重开；协调 D/I Inventory | Late Artifact/Lineage Digest、发现时间、旧/新 Checkpoint Ref、Suppression Receipt、Reopen Event |

## 7. D / E / Storage OPEN Decision Register

| 决策 | D 立场 | E 立场 | Storage 立场 | 总体 |
|---|---|---|---|---|
| Work Registration 与 Fence 全序 | 语义 DECIDED | 有 Consumer Mapping；可调用接口 OPEN | Shared Coordinator 已提议，未实现 | CR-P1-01 OPEN |
| 不可变 Barrier High-water | 语义 DECIDED | 必须消费 Fence Snapshot 并保留 Work Identity | 同一 Transaction 已提议 | 实现 OPEN |
| Dependency Registration 完整性 | 语义 DECIDED | 要求完整 Lineage/Receipt；API 细节 OPEN | Atomic Complete-set Write 已提议 | 实现 OPEN |
| Publish/Fence Linearization | 语义 DECIDED | 要求 Final Gate 和 Hidden Staging；跨边界 Gate OPEN | 单一 Commit/Visibility Pointer 已提议；未证明 | P0 OPEN |
| Final Commit 时 PermissionEpoch | D 要求 I 权威当前 Decision | I Decision Mapping 已请求/未确认 | 必须将 Decision Freshness 绑定 Visibility Commit | I + Storage OPEN |
| Lease/Retry/DLQ/Recovery | D Terminal/Barrier 语义 DECIDED | Work/Attempt Lifecycle 已描述 | Durable Lease Epoch/Recovery 已提议 | NOT VERIFIED |
| Index Rebuild / Adapter Replay / Context Consumer | D 要求边界处执行相同 Fence/Lineage 检查 | F/G/H 拥有执行和 Evidence | Visibility Predicate 必须防止绕过 | F/G/H OPEN |
| Global Inventory 和 Completion | D 只提供 Canonical Barrier Result | E 提供 Producer Evidence | Storage 提供 Backup/Restore Evidence | I OPEN |
| Physical Erasure / External Copies | 不属于 D | 不属于 E | 适用时需要执行证据 | I + Target Owner OPEN |

**CR-P1-01 MUST 保持 OPEN。** D 的语义定义不能证明 Database Transaction、已部署 Storage 行为、Permission Freshness Protocol 或跨模块符合性。只有 E 和 Storage 联合确认可实现接口，并且必需 Conformance Evidence 存在后，才可以关闭。I 的授权决策和全局 Inventory 仍由 I 单独负责。

## 8. 基线与证据边界

本 Phase 3.6 补充使用 Phase 3.6 Baseline Manifest 中记录的分支来源：
- A Phase 3.5 Review：A 分支的准确 Review Artifact。
- D Forget Completion/Operation Contract：D 分支。
- E Producer Admission、Derived Registration 和 Phase 3.6 Conformance：E 分支。
- Storage Atomicity Proposal：Storage 分支。
- I Global Forget Inventory/Completion Contract：I 分支。

后续集成验收前必须重新查询各源分支 HEAD。旧报告中嵌入的历史 SHA 不是当前分支证据。

**非声明：** 本文是 D 拥有的语义契约和静态设计文档。它不声称存在可执行实现、已部署的线性化数据库、已通过的竞争/故障测试、Global Forget 完成、Backup 擦除或物理删除。

## 9. 精确源基线清单（编辑前发现快照）

以下分支 HEAD 在 D 拥有的 Phase 3.6 编辑前查询。Blob SHA 标识实际读取的准确源 Artifact。这些值是本次工作的历史源快照，不表示其他分支在发现后仍停留于这些 HEAD。

| Artifact | Owner | Source Branch | Source Branch HEAD | Path | Source Blob SHA | Evidence Status |
|---|---|---|---|---|---|---|
| Phase 3.5 Cross-Module Closure Review | A | session-a-integration-2026-11-16 | 5ce61e0982ce8e22b29f1267ca67c9a085a96a06 | reviews/integration/phase-3.5-cross-module-closure-review.md | a05f1d817514bbed7bddec1729d6598d0835ef3e | Artifact Exists；A Review 结论 BLOCKED |
| D Forget Completion Contract（本次编辑前） | D | session-d-memory-brain-2026-11-16 | da8e5882d0b238d765d00b2225b79eea45a483b1 | 03-memory-brain/forget-fence-and-completion-contract.md | cce2108899525c9ce6808716224641baa11faf4f | Artifact Exists；D Semantic Decision DECIDED |
| D Operation / Publication Gate（本次编辑前） | D | session-d-memory-brain-2026-11-16 | da8e5882d0b238d765d00b2225b79eea45a483b1 | 03-memory-brain/forget-fence-operation-and-publication-gate.md | 2c5b1358ff58f99af838b741a75966ccd07ad088 | Artifact Exists；D Operation Semantics DECIDED |
| E Producer Admission | E | session-e-memory-compiler-2026-11-16 | a19feb57c85819cc0e49ab39abfd945b268aa51e | 04-memory-compiler/compiler-state-and-producer-admission.md | e59f517fff161ab882aa0ddc4a5bda513964ae1a | Artifact Exists；E Design，Implementation OPEN |
| E Derived Registration | E | session-e-memory-compiler-2026-11-16 | a19feb57c85819cc0e49ab39abfd945b268aa51e | 04-memory-compiler/forget-fence-and-derived-registration.md | 00e37ba56596e710513c8d0568acd79141d9101b | Artifact Exists；Interface/Atomicity OPEN |
| E Phase 3.6 Producer Publication Conformance | E | session-e-memory-compiler-2026-11-16 | a19feb57c85819cc0e49ab39abfd945b268aa51e | 04-memory-compiler/phase-3.6-producer-publication-conformance.md | a21f81dfe53ae6998818d2cc59e865f5dd1b839d | Artifact Exists；DESIGN COMPLETE / IMPLEMENTATION NOT VERIFIED |
| Storage Forget Atomicity Realization Review | Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 3a14550648f21c0bc2725dac38b29e099c2f3196 | reviews/storage-consistency/forget-atomicity-storage-realization-review.md | 5e2d55c8b210997693a7f83d35a5a03588e4ae6b | Artifact Exists；PROPOSED / NOT IMPLEMENTED / NOT VERIFIED |
| I Global Forget Inventory and Completion Evidence | I | session-i-security-governance-2026-11-16 | d52cd47972bd9d1d17f0fe6f2ab09646d084a80b | 09-security-governance/global-forget-target-inventory-and-completion-evidence.md | 9100061fa986fb6676656169de3fcf9fc1c72664 | Artifact Exists；CANDIDATE；跨 Owner Conformance OPEN |

同期发现的依赖分支 HEAD：B 66adf6bdcf5ec69a146fe75afe20ce3b85af8448；C a585307222b0169c007915c25ff8ed0da517f3e4；F f86f9b536ea69d8e0fbb4bf290c7023ef0eada76；G 557c68fd863f73dd09f6fccb3b9e920740db2e9c；H 1ee65928f123d92a4758b0de09bc8d6df1e46253；main 8a6414158c9c056c1638222534e1993d1bbc99d2。这些是依赖上下文，不代表跨模块批准。
