---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "从 Owner 源分支逐字节恢复；Owner 接受仍待定。"
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-7-e-local-lifecycle-producer-derivative-queue-recall-context-restore"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-7-e-local-lifecycle-producer-derivative-queue-recall-context-restore
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# 第 3.7 阶段 —— E 本地生命周期：生产者、派生品、队列、召回、上下文与恢复

- 所有者：E —— Memory Compiler
- 分支：`session-e-memory-compiler-2026-11-16`
- 状态：**E 本地语义提案；D/E/Storage 发布门与跨所有者 schema 仍为 OPEN / NOT VERIFIED**
- 范围：源事件摄取、编译器工作、派生制品产出、编译器队列/outbox、编译器源召回、编译器输入上下文与恢复。
- 权限边界：D 拥有规范 Memory、ForgetFence、生产者登记册与依赖清单；I 拥有授权/PermissionEpoch；E 拥有编译；F 拥有运行时检索/索引投影；G 拥有面向用户的 Context 与 Applied/Delivery；H 拥有线上协议/适配器能力；Storage 拥有约定的持久事务/可见性实现。

## 1. E 的本地生命周期模型

E 是派生品生产者，不是规范权威。已接受输入、编译器完成与本地存储的制品，都不使制品可见。

| 对象 | E 本地状态 | 终态 / 非终态含义 |
|---|---|---|
| 生产者意图 | Received → Validating → Accepted → RegistrationPending → Registered → Queued → Leased → Running → Staged → DependencyRegistered → GatePending → Published / Suppressed / Rejected | 死信、超时、租约过期与 worker 丢失，在"不再发布"处置持久之前均为非终态 |
| 派生 | Planned → Executing → CandidateProduced → Validated → PrivateStaged → LineageBound → PublicationPending → Published / Quarantined / Discarded | 每次重编译都是新的 DerivationRun；先前输出保持不可变 |
| 队列/outbox | Enqueued → Leased → Dispatched → Acked / Retry / DLQ / Cancelled | 队列 ACK 不是编译器成功、规范提交、发布或 D 屏障关闭 |
| 源召回 | Requested → Authorized → SourceResolved → EvidenceBound → ReturnedToCompiler / Blocked | 编译器源召回不是用户 Recall，且绝不绕过 D/I 检查 |
| 编译器输入上下文 | Assembled → ProvenanceChecked → ScopeChecked → Budgeted → FrozenForRun → Consumed / Invalidated | E 的运行输入包不是 G 的 ContextVersion，也不是 F 的工作集 |
| 恢复单元 | Discovered → Isolated → PrefixReconciled → LedgerReconciled → ReplayValidated → PrivateRebuilt → PublicationGate → Enabled | 在对账完成之前，任何已恢复的暂存制品/outbox 都不得暴露 |

## 2. 生产者行为

1. E 在入队、租约、源解引用或执行之前，为每个具备派生能力的逻辑工作项向 D 登记。必需绑定：稳定 ProducerWorkItemId、生产者类别/身份、CompileIntentId、源 EventRef/精确 Memory 引用、ScopeRefs、完整已知血缘、请求摘要、准入 CanonicalCommitCursor、观测到的 ForgetFence 与 I PermissionEpoch。
2. AcceptedReceiptId 仅证明 E 的持久入站；它不证明 D 的生产者登记。登记不确定性以稳定 WorkItemId+摘要求解。
3. 重试保留 ProducerWorkItemId 与请求摘要；AttemptId 与 LeaseId 变化。重编译创建新的 DerivationRunId 与不可变输出版本，并重新做授权/栅栏检查，且具有 D 治理的登记关系。它不能脱离原始源血缘或 Forget 屏障。
4. 每个终态结果都必须显式且持久：Published、RejectedBeforeAdmission、CancelledNoPublication、SuppressedByFence、FailedNoPublication 或其他 D 批准的处置。DLQ、超时、重试耗尽与进程死亡都不是终态。
5. D 的栅栏前生产者高水位在 D 接受终态/不再发布证据之前保持开启。E 不能移除登记，也不能自行关闭屏障。
6. D/I 权威或登记结果未知时失败关闭；不得投机执行具备派生能力的工作。

## 3. 派生品行为

- 派生品包括规范化 claim、抽取的实体/关系、证据片段、摘要、嵌入向量、溯源边、编译器提案、暂存的规范候选，以及任何后续可能暴露或再生源派生内容的持久 outbox/缓存制品。
- 每个不可变 DerivedArtifactRef/版本绑定 ProducerWorkItemId、DerivationRunId、源 EventRef 与精确源版本、完整传递血缘、溯源、Scope、策略 epoch、schema/模型/编译器版本与内容摘要。
- 在依赖被持久登记到 D、且权威发布门相对当前 D 栅栏与 I 权限成功之前，候选输出保持私有/不可查询。
- 依赖集合不完整、有歧义或无法求解的派生品被隔离，而不是部分发布。
- 同依赖登记键+同摘要幂等；同键+不同摘要冲突。已发布制品不得可变覆盖；输出变化即产生新的不可变版本。
- Forget/撤销会立即逻辑抑制受影响制品、阻止迟到发布，并启动受治理的清理。E 不能声称 F 索引清除、G Context 移除、物理字节擦除或全局完成。

## 4. 队列与 outbox 行为

- 队列条目是已登记工作的持久引用，不是授权。载荷绑定 WorkItemId、摘要、源引用、血缘摘要、Scope、schema 与尝试/租约代号。
- 预期至少一次派发。稳定身份+摘要去重；摘要变化即冲突。陈旧租约不能发布。
- D 登记必须先于入队。若入队成功但登记不确定，则隔离并以稳定身份求解；绝不运行。
- 重试/DLQ 保留开启的生产者登记。新尝试不是新的逻辑工作项。
- 在执行、源读取、依赖登记与发布之前，重校验当前 I PermissionEpoch 与 D 栅栏。最终门必须与可见性串行化；禁止本地检查后直接发布。
- 恢复会隔离队列/outbox 记录，直到 COC 前缀、D 生产者账本/高水位、I 策略与 Storage 参与者/可见性记录对账完成。未知缺口阻止重放。

## 5. 召回行为

- E 的 Recall 被狭义定义为编译器源/证据解析：为某个具体 DerivationRun 获取精确、已授权的 EventRef/MemoryVersionRef 与所需溯源。
- 它不是交互式/用户召回、排序、上下文投递或授权授予。F 拥有运行时检索；G 拥有 Context 选择。
- 每次源读取都绑定已认证生产者身份、目的、Scope、I PermissionEpoch 与 D 栅栏；在解引用之前重校验源生命周期与血缘。
- 解析精确源修订。不得静默把引用浮动到更新版本，或替换为首选 claim。被取代/被撤回/被遗忘/未授权的源被阻塞或显式分类。
- 源覆盖不完整时记为不完整；检索/索引结果中缺失并不证明源不存在。
- 证据/溯源在抽取、规范化、合并与输出过程中始终附着。编译器输出不得把不可信源文本提升为特权指令。

## 6. 上下文行为

- E 仅拥有某个 DerivationRun 的不可变编译器输入包：选定的源引用、证据/溯源、精确版本、Scope、策略 epoch、编译器/模型/schema 版本、预算与确定性输入摘要。
- 在执行前冻结输入包。任何源、权限、栅栏、schema 或模型配置变化，都需要新的运行身份/输入摘要与全新校验。
- 该包不是 G 的目标 Context、ContextVersion、Snapshot/Delta、Delivery 或 Applied 记录，也不是 F 的检索工作集。
- E 可向 F 请求源候选，或向 G 提供已校验的派生引用；F 决定检索机制，G 决定 Context 成员与投递。E 不能声明面向用户的召回结果或 Applied 状态。
- 不得跨 Scope 混用。若源溯源或 scope 不确定，不得编译/发布。

## 7. 恢复与重放

1. 把事件日志、编译器状态、暂存制品、队列/outbox 与依赖清单恢复到隔离/私有存储中。
2. 校验 Storage 恢复/参与者证据，并对账 COC 已提交前缀、D 生产者登记/依赖高水位与 I PermissionEpoch/撤销/登记册状态。这些是彼此独立的类型化权威。
3. 在存在已准备发布时，保留相同的 CompileIntentId、ProducerWorkItemId、请求摘要、PublicationOperationId、PreparedParticipantRef 与 PreparedTransactionGID。AttemptId/LeaseId 可变化；不可变事务元组不可变化。
4. 以稳定身份求解每个在途条目。绝不从队列消息缺失、租约过期、回执缺失或陈旧副本推断完成。
5. 重校验源修订、完整血缘、Scope、策略、ForgetFence 与模型/schema 兼容性。仅重建私有制品。
6. 幂等重新登记/对账依赖；最终发布必须通过当前 D/I 门。若指针/回执/GID/权威不一致，保持隔离。
7. 在开放队列消费者或暴露制品之前，对账恢复后的事件。连续性未知即不重放/不发布。
8. RestoreReconciliationReceipt 不是 PublicationReceipt、D 放行、I 授权、COC 终态决策或全局 Forget 完成。

## 8. 证据与测试

E 发出 AcceptedReceipt、生产者登记回执引用、不可变运行/尝试身份、源/输入摘要、依赖回执、发布操作/结果、终态"不再发布"处置、队列状态与恢复对账结果。仅 D 关闭其屏障；仅 Storage 提供其约定的事务证据。

必需测试：入队前登记崩溃；先入队后 ACK；重复投递与摘要变化；陈旧租约发布；跨 Forget 栅栏的重试/DLQ；不完整传递血缘；编译期间撤销；门对栅栏竞争；带陈旧前缀/参与者账本的恢复；源被取代后的重编译；未知 GID 求解。这些是必需的规格，不是已执行测试的声明。

## 9. 非目标 / 阻塞项

- E 不拥有规范真值、Forget 决策、面向用户的 Recall、F 索引、G Context/Applied、H ACK 或 I 授权。
- 在可调用 schema 与崩溃安全的线性化被约定并核实之前，D/E/Storage 的原子登记/依赖/最终发布门保持 **BLOCKING**。
- **不声称任何编译器实现、一致性 PASS、生产恢复或发布激活。**


## 10. 第 3.7 阶段跨 Owner 对齐修订

**处置：** E 本地修订提案，覆盖 LIF-01/02/04/05/08/09/10。D 的 §8 仅 EventRef 登记规则是本提案集合的控制性 D 决策；E 消费该规则，但不铸造 D 准入。

### 10.1 ProducerClass 与仅含 EventRef 的入口
- E 本地的生产者分类不构成准入授权。每个具备派生能力的 CompileIntent 都必须由 D 签发的、带版本且已启用的 ProducerClass 登记覆盖，明确所有者、接受的源引用类别、输出/派生类别与允许能力（normal、replay、rebuild、cleanup-only）。
- E 的入站接受（AcceptedReceipt）与 D 的生产者准入（RegistrationReceipt）彼此不同，且都不能替代对方。
- **仅含 EventRef 的入口遵循 D §8，在 Canonical MemoryRef 存在之前即可获得 D 登记**，但前提是已认证生产者、已启用 ProducerClass/版本、精确 Scope、规范请求摘要与 D 批准的不透明血缘令牌/摘要均完整。E 必须在入队/租约/执行之前取得持久 D RegistrationReceipt。E 不得把该回执视为受保护载荷授权；当前 I 授权须另行要求。在依赖登记/发布之前，E 必须把精确的 Canonical MemoryRef/MemoryVersionRef 身份与修订关联到原始 EventRef 血缘。缺失/无效绑定保持隔离且不授予执行能力。

### 10.2 派生、重试与终态处置
- 重试保留逻辑 ProducerWorkItemId 与请求摘要；AttemptId/LeaseId 轮换。重编译创建新的不可变 DerivationRun/输出版本，并通过 D 治理的关系关联前驱/源血缘；它不能甩掉先前依赖或栅栏。
- E 本地的 Published、Rejected、Cancelled、Failed、DLQ 或 Completed 标签都不关闭 D 生产者屏障。E 提供持久的"不再发布"证据；仅 D 接受终态处置并关闭其屏障。
- 每次源解引用、执行边界、依赖登记与发布门都重校验当前 I 授权与 D 栅栏/血缘。历史权限或缓存 ALLOW 不充分。

### 10.3 恢复与类型化上下文
- 恢复受下列独立证明共同约束：Storage 参与者/可见性与 DB 世代证明、COC 已提交前缀证明、I 当前策略/撤销/登记册证明、D 栅栏/血缘/生产者/依赖证明，以及 E 编译器账本/运行/依赖证明。保留各签发方特有的签名与不透明位置；绝不合成标量恢复高水位。
- 前缀、已准备发布元组、GID、参与者回执、登记或依赖连续性任何一项未知，都使受影响的运行/制品/outbox 保持隔离。绝不从缺失队列行或陈旧副本推断完成。
- E 的冻结编译器输入包是绑定单个 DerivationRun/摘要的名义类型，不是 F 工作集，也不是 G ContextVersion/Delivery/Applied。

## 8. 规范更正 —— 仅 EventRef 工作与 D 准入

本节取代更早 §3.7 中"仅 EventRef 入站必须留在 D 准入之外"的表述。D 的控制性 §3.2 允许在 Canonical MemoryRef 创建之前登记。

1. E 创建稳定 CompileIntentId/ProducerWorkItemId 与 E AcceptedReceipt 作为本地入站证据。
2. 在入队、租约、受保护源解引用或具备派生能力的执行之前，E 调用 D RegisterProducerWork。当已认证 ProducerClass、Scope、请求摘要与 D 批准的不透明血缘令牌/摘要完整时，D 可接受仅含 EventRef 的源。
3. D 的接受产生持久 RegistrationReceipt 与 ProducerRegistrationSequence。ACK 未知时以同一 WorkItemId+摘要求解；未解决期间 E 不派发。
4. 仅 EventRef 的登记同样计入 D ForgetFence 高水位，并遵循 D 的两结果准入/栅栏线性化。
5. 在 RegisterDerivedDependency 或发布之前，E 把精确的 Canonical MemoryRef/MemoryVersionRef 修订追加/关联到原始 EventRef 血缘。不完整/冲突的血缘保持私有/隔离，不能发布。
6. D 登记不是受保护载荷授权。E 在每次受保护解引用与最终发布处检查当前 I 权限。
7. 身份、Scope、血缘令牌、登记册或当前权威缺失，意味着没有入队/租约/执行能力。

## 9. D/E/Storage 从登记到可见性的原子消费

E 采用 D 的九项操作语义契约，以及 Storage 的"每个 Canonical Memory Authority 一个共享串行化域"建议，但以 Storage 证明为前提。必需顺序：

E AcceptedReceipt → 持久 D RegistrationReceipt → 队列/租约/运行 → 私有不可变暂存 → 完整 D DependencyRegistrationReceipt → D PublishDerivedIfFenceCurrent + Storage 权威 Visibility Commit → D CompleteProducerWork。

在持久 D 登记之前不得入队/租约/执行。重试保留 ProducerWorkItemId 与请求摘要，同时 AttemptId/LeaseId 轮换。重编译使用新的 DerivationRunId 与显式的 D 关联子项/再准入决策，绝不重置血缘。暂存字节保持私有。依赖集合与血缘摘要作为一个完整不可变单元提交。可见性仅在权威原子提交处改变，该提交检查当前 D 栅栏、I 授权、D 登记、完整依赖、活动尝试/租约、Scope 与精确制品摘要。ACK 丢失以同一稳定操作 ID+摘要求解；UNKNOWN 使制品保持私有、屏障保持开启。终态关闭需要在全部输出/尝试/重放路径结算之后取得 D 终态回执。

E 拒绝"先得到 D 批准消息、随后无约束写入对象存储"。若不存在共享 ACID 域，E 要求 D+Storage 批准的持久准备/提交、一次性最终可见性 CAS、提交时当前栅栏校验、崩溃恢复与 UNKNOWN 时隐藏行为。

## 10. D/I/Storage 最终发布序列 —— 无分离的门令牌

E 为受保护派生发布采用两个独立的在途屏障：

1. E 完成私有暂存与完整依赖集合。
2. D 相对当前 ForgetFence 准入一个 D 拥有的 PublicationParticipantRef，并在 D 屏障中记为未解决。
3. Storage 持久创建一个隐藏的 StorageVisibilityParticipantRef，绑定 PublicationOperationId/摘要、制品/版本、WorkItemId、尝试/租约、依赖摘要与 D PublicationParticipantRef。
4. I 在其自身的 PolicyDomain 排序器中消费一次性 CommitAuthorizationReceipt，绑定该精确发布与 Storage 参与者。REVOCATION_WON/UNKNOWN 阻止可见性。COMMIT_WON 不是可见性；I 把后续撤销挡在未解决参与者之后。
5. Storage 仅在最终边界校验精确 D 参与者当前性与 I 终态证明之后，在 D/Storage 串行化域中提交可见性。提交记录不可变 PublicationReceipt 与参与者结果。
6. D 与 I 各自独立消费权威 Storage 结果：COMMITTED_VISIBLE 或已证明的 NO_PUBLICATION 关闭各自参与者；UNKNOWN 使两个屏障保持开启且制品保持私有。

D 栅栏与 I 撤销是彼此独立的门。D 发布意图先行意味着后续 D 栅栏等待该参与者；I 回执消费先行意味着后续撤销等待该参与者。若任一权威先行胜出，发布被拒绝或安全中止。禁止跨权威数值 epoch 比较。

## 11. 崩溃窗口更正 —— Storage 准备先于 D PublicationParticipant 准入

本节取代 §10 中 D 准入先于 Storage 准备的顺序。

必需顺序：
1. Storage 首先持久化一个隐藏的 StorageVisibilityParticipantRef，绑定不可变 PublicationOperationId/摘要、WorkItemId、制品/版本、AttemptId/LeaseId、完整依赖摘要与私有暂存身份。
2. D 随后准入 PublicationParticipantRef，绑定该精确的、已持久化的 StorageVisibilityParticipantRef，并在 D 栅栏/屏障中记为未解决。
3. I 消费一次性 CommitAuthorizationReceipt，绑定两个精确引用与完整不可变发布元组。
4. Storage 仅在最终边界上精确 D 与 I 证明均校验通过之后提交可见性。
5. D 与 I 仅在取得权威 Storage COMMITTED_VISIBLE 或 NO_PUBLICATION 证据之后，才关闭各自参与者。

崩溃语义：
- Storage 准备存在但 D 准入尚未接受：保持私有；无 D 屏障参与者，也无发布能力。D 的拒绝以同一 D 操作 ID/摘要求解。
- D 准入 ACK 未知：以同一 PublicationParticipantRef + 摘要求解；不得创建第二个 Storage 参与者。
- D 准入已接受：其精确 Storage 参与者必须已存在。参与者状态缺失属于 UNKNOWN/账本不一致，不是安全中止。
- I 回执已消费为 COMMIT_WON：后续撤销保持待定，直到 Storage 终态结果。
- 任何未知结果都使制品保持私有，且所有已准入屏障保持开启。

D PublicationParticipantRef 与 I CommitAuthorizationReceipt 都绑定精确的 StorageVisibilityParticipantRef。该参与者不是 C 的 ParticipantIntentRef，也不是 Storage PreparedParticipantRef/GID。
