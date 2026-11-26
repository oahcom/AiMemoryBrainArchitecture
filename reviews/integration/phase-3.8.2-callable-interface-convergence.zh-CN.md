# Phase 3.8.2 — D/E/I/Storage 可调用接口收敛

- 工作项：Issue #25
- 状态：**CANDIDATE / 待 Owner 评审；未冻结**
- 视角：A — 集成接口提案
- 依据：下列精确 Owner 分支 Blob 与 RFC-IDE-001 v1.0.0
- 本文定义逻辑调用面与依赖装配边界；不定义 H Wire 编码、密码学配置、物理拓扑或生产启用。

## 1. 范围与去重

本增量把 Phase 3.8.1 的候选操作矩阵推进为 Owner 可调用边界，并明确尚未闭合的调用/响应接口。它不重复实现 SQLite Event Store、Compile Intent Outbox、Scope 隔离测试、Publication Protocol 参考模型或幂等身份 RFC。

- PR #245：SQLite 持久化 Event 接收适配器，已合并。
- PR #246：事务性 Compile Intent Outbox，已合并；仅持久化意图，不负责派发或执行。
- PR #247：Phase 1 SQLite 持久化边界证据，已合并。
- PR #251：RFC-IDE-001 v1.0.0，Draft/Open；本文引用其提案，不把它当作已批准决策。

## 2. 本次审阅的精确输入

| Owner | Branch | Artifact | Blob |
|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` | `4c01713bc8793a8926ef18b625b72d132572173d` |
| E | `session-e-memory-compiler-2026-11-16` | `04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| I | `session-i-security-governance-2026-11-16` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` (not restored on main; see AID-2026-107 §10) | `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md` | `2ab899ee37a18ae6c8f2f64dbb82ad6499842060` |
| A 候选接口面 | `session-a-integration-2026-11-16` | `reviews/integration/phase-3.8.1-a-contract-surface-and-exact-pin-refresh.md` | `ad5450ea35f6dabc7de1ffa1ea63661f2e500064` |
| 幂等 RFC | PR #251，`rfc/idempotency-identity-tuple-2026-11-18` | `reviews/contracts/RFC-IDE-001-idempotency-identity-tuple.en.md` | `0f42db17325ba5402b7d8000fad8ce11aeadfbc4` |
| 幂等 RFC | PR #251，同一分支 | `reviews/contracts/RFC-IDE-001-idempotency-identity-tuple.zh-CN.md` | `3cd023ff1293b5d3ac8b7fdd5f8ddd9ef9598a1a` |

以上是精确源 Blob，不是独立 Owner 签名。任何源 Blob 变化都要求重新读取后再沿用评审结论。

## 3. 权限归属与调用方

| 边界 | 可调用权威 | 调用方/消费者 | 不得从以下内容推断 |
|---|---|---|---|
| Producer Class/Work 准入、ForgetFence、依赖完整性、Publication Participant、Producer 终态 | D | E 调用；Storage 在 Visibility Commit 验证 D 证明 | E AcceptedReceipt、Queue ACK、Storage 行、I Receipt |
| Compile Intent、Queue、Attempt/Lease、Derivation、Private Stage、输出清单与编排 | E | Compiler Worker/Runtime | D Registration 不代表 I 授权；Outbox 行不代表执行许可 |
| 当前授权、PolicyDomain Sequencer、撤权排序与 I Closeout | I | E 在受保护边界请求；Storage 验证提交前证明 | 缓存 ALLOW、陈旧 PermissionEpoch、D Clearance |
| 隐藏 Participant 持久化、事务/序列化、权威 Visibility Pointer/Outcome 与恢复 | Storage | E 编排；D/I 消费结果 | Object 存在、Object URL、Queue/Outbox 投递、Transport ACK |
| 规范 Wire 名称、编码、签名、密钥生命周期与互操作 | H（后续 Gate） | 所有 Adapter | 本逻辑提案 |

任何 Adapter 都不得签发其他 Owner 的 Receipt、终态、Epoch、Participant Ref 或授权。D、I、Storage 的数值位置不可跨域比较。

## 4. 类型化操作面（逻辑 API；候选）

以下名称是稳定逻辑操作提案，不是已冻结的 Rust Trait、HTTP Endpoint 或 Wire Schema。所有引用均为不透明名义类型。每个命令携带对不可变规范输入计算的 Request Digest；每个查询都按同一操作身份解析。

### D 所有的操作

- `D.register_producer_work(ProducerWorkRegistration) -> RegistrationResult`
  - 输入：稳定 `ProducerWorkItemId`、认证 ProducerIdentity 绑定、ProducerClassId/Version、EventRef 与已知 Source Ref、精确 Scope、批准的 Lineage Token/Digest、Request Digest。
  - 成功：持久化 `DRegistrationReceipt` 与 D 本地 ProducerRegistrationSequence。
  - 只有持久化成功后 E 才能入队/租约/执行。允许 D §8 规定的 EventRef-only ingress，但不授予受保护 Payload 读取权限。
- `D.install_forget_fence(ForgetFenceRequest) -> FenceResult`
  - 成功：不可变 Fence、Registry Version、捕获的 Producer Registration High-water 和 Inventory Snapshot Ref。
- `D.register_derived_dependency_set(CompleteDependencySet) -> DependencyResult`
  - E 提供完整直接/传递依赖集合及精确 Source Revision/Scope；D 验证 Lineage 与当前 Fence。
  - 仅在完整不可变集合提交后成功；部分集合不得签发完整 Receipt。
- `D.admit_publication(PublicationTuple, StorageVisibilityParticipantRef) -> DPublicationParticipantRef`
  - 要求 Storage Participant 已持久化为 PREPARED_HIDDEN，依赖完整，Attempt/Lease 当前，且 D Fence 准入允许。
  - 成功：D 所有的 `DPublicationParticipantRef`；它只是 Barrier Hold，不是 Visibility Permission。
- `D.close_publication_participant(DPublicationParticipantRef, StorageOutcomeProof) -> DTerminalReceipt`
  - 仅接受同一 Tuple 对应的权威 `COMMITTED_VISIBLE` 或 `NO_PUBLICATION`。
- `D.complete_producer_work(WorkItemId, FinalOutputInventory) -> ProducerTerminalReceipt`
  - 只有所有输出、重试、延迟 Publisher 和未知结果都已核清，D 才能关闭 Barrier。

### E 所有的操作

- `E.accept_compile_intent(CompileIntent) -> EAcceptedReceipt`：仅证明本地持久化入口接收。
- `E.register_work_with_d(WorkItemId, RequestDigest) -> DRegistrationReceipt`：入队前解析 D 准入。
- `E.enqueue_registered_work(DRegistrationReceipt) -> QueueReceipt`：拒绝缺失、陈旧或未解决的 D 证明。
- `E.acquire_attempt(WorkItemId) -> AttemptLease`：分配 Attempt/Lease Generation；陈旧 Generation 不得修改依赖或发布。
- `E.stage_derivative_privately(AttemptLease, Artifact) -> PrivateStageRef`：不产生 Serving Locator 或 Visibility。
- `E.submit_complete_dependencies(AttemptLease, CompleteDependencySet) -> DDependencyReceipt`。
- `E.publish_derivative(PublicationTuple) -> PublicationResolution`：编排 Storage Prepare → D Admission → I Consume → Storage Commit → D/I Closeout；绝不把 E 自己的 Receipt 当作 Owner 决策。
- `E.complete_work(WorkItemId, FinalOutputInventory) -> ProducerTerminalReceipt`：委托 D 作出终态决定；E 自身不能关闭 D Barrier。

### Storage 所有的操作

- `Storage.prepare_visibility(PublicationTuple) -> StorageVisibilityParticipant`
  - 在 D Admission 前，原子持久化不可变 Tuple 和隐藏 Private Participant。
  - 相同 Operation + 相同 Tuple Digest 返回同一 Participant；Digest 不同则冲突。
- `Storage.commit_visibility(StorageVisibilityParticipantRef, DPublicationParticipantRef, ICommitAuthorizationProof) -> StorageVisibilityOutcome`
  - 提交前 I 证明是已消费的一次性 `ICommitAuthorizationProof/ICommitAuthorizationProof`，不是提交后签发的 `ITerminalProof`。
  - 权威 Commit 验证精确 D Participant/当前 Fence 与精确 I 证明，并原子安装 Visibility Pointer 和不可变 Outcome。
- `Storage.resolve_visibility(PublicationOperationId, TupleDigest) -> StorageVisibilityOutcome`
  - Lost ACK、Crash、Failover、Restore 都解析同一 Operation。UNKNOWN 始终 Private；不得根据年龄或行缺失推断终态。
- `Storage.prove_no_publication(StorageVisibilityParticipantRef) -> NoPublicationProof`
  - 仅当 Storage 能证明没有安装 Pointer，且没有延迟 Publisher/Outbox/Retry 可以在未来安装 Pointer 时才成立。

### I 所有的操作

- `I.consume_commit_authorization(AuthorizationRequest) -> ICommitAuthorizationProof`
  - 在权威 PolicyDomain Sequencer 中单次消费；绑定认证 Subject/Delegation、Action、Purpose、Audience、Scope、Environment、PolicyDomain/当前 PermissionEpoch、Artifact/Version、PublicationOperationId/Tuple Digest，以及精确 D + Storage Participant Ref。
  - 返回权威产生的 `COMMIT_WON`、`REVOCATION_WON` 或 `UNKNOWN/IN_DOUBT`；调用方不得自行填写结果。
- `I.close_publication_authorization(ICommitAuthorizationProof, StorageOutcomeProof) -> ITerminalProof`
  - 仅用于 Storage Outcome 之后的 Closeout。COMMIT_WON 使后续适用撤权等待精确 Storage 终态；UNKNOWN 保持阻塞。
- I 必须提供已消费 Receipt 在响应丢失后的权威解析查询。重新消费 Nonce 不能代替解析原 Sequencer 结果。

## 5. 强制发布调用顺序

1. E 本地接收 CompileIntent；这不构成派发许可。
2. E 在 Queue、Lease、受保护读取或执行前取得持久化 D RegistrationReceipt。
3. E 在当前 AttemptId/LeaseId 下执行，私有暂存输出，并通过 D 完成精确依赖集合登记。
4. Storage 持久化隐藏的 `StorageVisibilityParticipantRef`。
5. D 准入绑定该精确 Storage Participant 的 `DPublicationParticipantRef`。
6. I 在自己的 PolicyDomain Sequencer 中消费单次 `ICommitAuthorizationProof`，绑定两个 Participant Ref 和同一 Tuple。
7. Storage 使用精确 D 当前 Participant/Fence 证明和提交前 I `ICommitAuthorizationProof` 提交 Visibility，并原子写入权威 Visibility Pointer 与 Outcome。
8. D/I 只有读取同一权威 Storage Outcome（`COMMITTED_VISIBLE` 或已证明的 `NO_PUBLICATION`）后，才分别关闭自己的 Participant。
9. 所有输出、重试和重放路径核清后，E/D 才关闭 Producer Work。

顺序固定为 Storage 隐藏持久化 Participant → D Admission → I Receipt Consumption → Storage Visibility Commit → D/I Closeout。它取代旧的 D-first 顺序。

## 6. 幂等、重试与身份隔离

Producer Append 命名空间与 Receipt 重放语义使用 RFC-IDE-001 v1.0.0（PR #251 Draft）：

`(ProducerIdentity, Scope, IdempotencyKey)`，并要求 Digest 完全一致。

本文不重复或重新解释该契约。尤其是：
- 披露任何 Receipt（包括重放）前都必须重新授权；
- 同一 Namespace + 同一 Digest 返回原 Receipt；
- 同一 Namespace + 不同 Digest 是不可变冲突；
- 跨 Scope 复用 Key 属于独立 Namespace，不得跨 Scope 查询 Receipt；
- ProducerIdentity 组合、Digest 规范化和 Receipt 保留策略维持 RFC 原有 CANDIDATE / TO_VALIDATE 状态。

Publication 使用独立的不可变操作身份：`PublicationOperationId + PublicationTupleDigest`。它不是 Producer 的 IdempotencyKey。同一 Operation + 同一 Tuple 解析到同一 Participant/Outcome；同一 Operation + 不同 Tuple 为 `IMMUTABLE_IDENTITY_CONFLICT`。权威 `NO_PUBLICATION` 后的新发布尝试，或 Artifact/Version、Dependency Set、Scope、Source Revision、Attempt/Lease Tuple 发生变化时，必须分配新的 PublicationOperationId、新 Participant 身份并重新执行 D/I 检查。相同逻辑 Work 的 Retry 可以轮换 AttemptId/LeaseId，但不能替换已经提交的 Publication Tuple。

名义类型必须隔离：ProducerIdentity、ScopeRef、IdempotencyKey、ProducerWorkItemId、DerivationRunId、AttemptId、LeaseId、PublicationOperationId、DPublicationParticipantRef、ICommitAuthorizationProof、StorageVisibilityParticipantRef、Storage PreparedParticipantRef/GID、C ParticipantIntentRef 和 ITerminalProof。

## 7. 解析与失败契约

每个变更操作都必须有同一身份的解析查询。Transport Timeout 不是状态转换。

| 结果 | 含义 | 调用方必须行为 |
|---|---|---|
| REJECTED | 权威拒绝 | 不授予下游能力 |
| QUARANTINED | 身份/Lineage/Scope 证据不足或未决 | 不得 Queue/Lease/Execute/Visibility |
| IMMUTABLE_IDENTITY_CONFLICT | 相同操作身份但 Digest/Tuple 改变 | 停止；不得覆盖原记录 |
| FENCE_WON | D Fence 先完成排序 | 不得发布 |
| REVOCATION_WON | I Revocation 先于消费完成排序 | 不得发布 |
| STALE_ATTEMPT | Attempt/Lease Generation 已被替代 | Worker 不得修改或发布 |
| INCOMPLETE_DEPENDENCY_SET | 直接/传递依赖不完整 | 不得签发完整 Receipt 或发布 |
| UNKNOWN / IN_DOUBT | 无法证明终态 | 保持 Private；保持已准入 Barrier 开放；按同一 ID 解析 |
| COMMITTED_VISIBLE | Storage 权威 Visibility Commit 证明 | D/I 验证精确证明后可 Close |
| NO_PUBLICATION | 权威证明当前及未来均不会出现 Visibility | D/I 验证精确证明后可 Close |

DLQ、Lease Expiry、Process Death、Queue Deletion、Missing Row、Lost ACK、Stale Replica 和 Timeout 均不是终态证据。

## 8. 依赖注册与启用 Gate

Runtime Composition Root 只能按显式类型化能力注册 Adapter：
- D：Producer Admission、Fence、Dependency、Publication Participant 和 Terminal API；
- E：Intent Ingress、Queue/Lease/Attempt、Staging、Orchestration 和 Inventory；
- I：受保护边界当前授权、单次 Sequencer 和 Closeout/Resolution；
- Storage：Hidden Prepare、Atomic Visibility Commit、权威 Outcome Resolution 和 Restore-safe NO_PUBLICATION Proof。

若任一必需能力缺失、生产配置指向 Test/Fake Adapter，或缺少 Owner 批准的 Contract Version，Startup/Readiness 必须 Fail Closed。Compile Intent Outbox 不是 Dispatcher。不能仅因 Outbox 行存在就启动 Worker。部分 Adapter 组合只能用于本地非受保护测试，不得开放 Derivative Execution 或 Serving。

H Wire Adapter 与规范化/签名配置仍是独立依赖；本逻辑 API 不冻结它们。

## 9. 必需 Owner 决策与符合性验证

| Owner | 必须针对当前 Blob 明确决策 |
|---|---|
| D | 操作名/输入输出类型、Registration/Fence 线性化、完整 Dependency Receipt、Storage-first Publication Admission、Terminalization、Replay/Error 映射 |
| E | CompileIntent/WorkItem/Attempt/Lease 身份、调用顺序、同操作恢复与 NO_PUBLICATION 后新发布的区分、清除过时 §10 顺序 |
| I | Authorization Request、已消费 Receipt、提交后 ITerminalProof 三种类型隔离；Nonce Resolution；Issuer/Key/Policy 当前性；Revocation Hold 与 Commit Proof 有效性 |
| Storage | Prepare-before-D-admission、原子验证 D 当前证明 + 提交前 I 证明、Visibility Pointer/Outcome 原子性、权威 NO_PUBLICATION、物理拓扑与 Restore |
| H | Canonical Bytes、Digest/Profile 标识、签名、Key Status/Rotation/Revocation、版本协商和跨语言向量 |

必需确定性测试：Register-vs-Fence 两种顺序；EventRef-only Admission；D ACK 丢失；Complete Dependency Crash；Storage Prepare Crash；D Admission 缺少 Participant 时拒绝；I Revocation-vs-Consumption 两种顺序；Storage Visibility ACK 丢失；Stale Lease；同 ID 不同 Tuple 冲突；带延迟 Publisher/Outbox 的 NO_PUBLICATION；Owner Ledger 缺失或不一致时 Restore。断言必须覆盖持久化记录、Visibility Pointer、D Barrier、I Revocation Hold 和精确 Retry 身份。

## 10. 明确矛盾与阻塞

1. **E 旧顺序：** E §10 仍写 D Admission 先于 Storage Prepare，并把 I Terminal Proof 描述为 Storage Commit 前置条件。E §11 已明确取代该顺序。E 必须删除或显著标记 §10 旧表述，避免实现者选错顺序。
2. **Storage 证明阶段歧义：** Storage §12 仍称最终 Commit 验证 I “terminal proof”。A 当前候选映射及因果顺序区分提交前已消费的 `ICommitAuthorizationProof/ICommitAuthorizationProof` 与提交后 `ITerminalProof`。Storage 与 I 必须明确接受前者作为 Visibility Commit 的提交前证明；ITerminalProof 只能用于 Closeout。
3. **Callable API 未冻结：** D/E/I/Storage 源文件定义了语义义务，但尚无共同接受的精确类型化方法/DTO/查询接口。本提案签名仍为 CANDIDATE。
4. **物理拓扑无证明：** Storage 共享 Serializable Domain 仍是提案；没有已选择/部署的拓扑，也没有 Crash/Failover/Restore 符合性 PASS。
5. **缺少独立 Owner 批准：** A 的角色模拟评审不等于 D/E/I/Storage 签名。各 Owner 必须针对上列精确 Blob 独立决策。

## 11. 状态与非声明

- **CANDIDATE：** 本文的 Callable Logical API 与 Dependency Composition 提案。
- **OPEN：** D/E/I/Storage Owner 精确批准、H Wire Profile、物理事务拓扑、真实 Adapter 和跨 Owner 符合性。
- **TO_VALIDATE：** Runtime Registration/Readiness、Crash/Failover/Restore、多进程序列化、证明验证和 Retry/Expiry Race 测试。
- **DECIDED：** 仅指仓库此前已批准的决策。本文不把 RFC-IDE-001 Draft 或任何 Owner 提案升级为全仓 DECIDED。

本文不声称 API 已实现、Schema 已冻结、Owner 已独立签署、CI 符合性 PASS、生产派发、Compiler 执行、生产启用、Global Forget 完成或物理擦除。
