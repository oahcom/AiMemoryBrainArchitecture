# L2-04-F-E-G-LIFECYCLE：跨 Owner 生命周期核验

<badge color="warning">CANDIDATE / NO APPROVAL</badge> <badge color="info">READ-ONLY</badge>

**初步裁定：三份 Owner-local 契约在核心安全原则上高度一致，但尚不足以形成可冻结的共享生命周期契约。**

本轮按以下边界执行：

- 实际加载：AI-EXEC-001 v1.1、AI-EXEC-002 v1.1；不采用尚未批准的 v1.2 变体。
- 不创建或修改 PR、Issue、Git、assignee、PR 状态。
- 不替 F、E、G、D、I、Storage 或 A 作批准。
- 不将契约中的 Required Tests 当成已经执行的测试。
- 不将语义一致视为接口已实现。

## 1. 启动记录与来源核验

三个 Artifact 均已通过 GitHub 连接器按指定 Commit 读取，实际 Blob SHA 与提交材料完全一致。

| Owner | Commit SHA | Blob SHA | 核验 |
|---|---|---|---|
| F | `413a22d05208e4736895d8233e35587407292fa6` | `23d00ce7ec60c2145f637e7bc9323294b25b4d77` | <badge color="success">MATCH</badge> |
| E | `1e0fcd1e58e215f076043e6cd004892e8fc2bd50` | `ef5e735e0fad3cb1b6475ac2532b1f3419d130b8` | <badge color="success">MATCH</badge> |
| G | `fc96973a4f5479c5ac5f4f428163a4d4002b8cd0` | `d6d18684ba8a31a538e2e719be3f6e1b715cadf8` | <badge color="success">MATCH</badge> |

来源路径：

- F：`05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md`
- E：`04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md`
- G：`06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md`

三个文档均明确声明：Owner-local semantic proposal；跨 Owner 接口和实现尚未验证；没有生产激活或 Conformance PASS 声明。

**版本限制：** 本轮已经确认指定 Commit 和 Blob 的对应关系，但不能据此推断三个分支当前仍停留在这些 Commit，也不能推断 main 已经吸收这些内容。

## 2. 六维生命周期对照矩阵

以下是对三个指定 Blob 的逐项语义比较，而非将三份状态机强行合并。

| 维度 | F Runtime | E Compiler | G Context | 跨 Owner 结论 |
|---|---|---|---|---|
| Producer | Runtime derivative producer；纯只读 Recall 有窄例外 | Compiler derivative producer | Context derivative producer | 基本一致；D ProducerClass 注册机制未闭合 |
| Derivative | Index、Cache、Embedding、Working Set | Claims、Evidence、Embedding、Compiler artifacts | Entry、Snapshot、Delta、ChangeSet、Delivery payload | 共同要求完整 lineage、私有构建、最终 Gate |
| Queue | Runtime queue、Attempt、Lease | Compiler queue/outbox | Delivery queue、DeliveryAttempt | At-least-once 语义一致；Delivery 与普通工作队列不能混为一谈 |
| Recall | 检索、候选生成、最终返回 | 精确源事件与证据解析 | Context membership 选择 | E→F→G 职责总体清晰 |
| Context | F Working Set | E Frozen Input Bundle | G ContextVersion | 所有权边界正确，必须保留不同名义类型 |
| Restore | Index/Cache/Queue/Working Set | Compiler state/outbox/artifact | Context/Delivery/Adapter/Applied | 都要求先隔离；独立证明的最终合取闸门未完全定义 |

### 2.1 Producer：基本一致，但 Admission 仍有阻断项

三个 Owner 的共同语义：

1. derivative-capable work 必须先注册 D。
2. 注册先于 Queue、Lease、Execute 和受保护的 Source Dereference。
3. `ProducerWorkItemId` 跨重试保持稳定。
4. `AttemptId`、`LeaseId` 随尝试变化。
5. 同一身份、同一 Digest 才能幂等；身份相同而 Digest 不同必须 Conflict。
6. D 的 pre-fence high-water 不能由 F/E/G 自行结算。

具体差异：

- F 的 Runtime Producer 状态为 `Requested → AuthorityChecked → DRegistered → Queued → Leased → Running`。
- E 增加 `Accepted`、`RegistrationPending`，并区分 `CompileIntentId` 和 `DerivationRunId`。
- G 绑定 `ContextId`、目标 ContextVersion 和 ChangeSet Digest。

**Finding FEG-01 [P1]：ProducerClass 尚不是统一的 D Admission。**

本地定义 Producer class 不等于 D 已注册并启用该 ProducerClass。

还缺：

- D-issued ProducerClass Registry。
- ProducerClass 版本及允许的 Source/Output 类型。
- Normal、Replay、Rebuild、Cleanup-only 能力区分。
- 精确 RegistrationReceipt 和 D ProducerRegistrationSequence。
- pre-fence Work 的 D 接受终态及 no-future-publication 证据。

E 的 `AcceptedReceiptId` 也不能代替 D RegistrationReceipt。

**Finding FEG-02 [P1]：终态命名存在语义风险。**

F 的 `Completed / Suppressed / Failed`、E 的 `Published / Rejected / FailedNoPublication`、G 的 `Committed / Blocked / CancelledNoPublication`，不能直接映射为 D 的 Producer Barrier 关闭。

规范必须明确：

`LocalTerminal ≠ DTerminalAccepted`

只有 D 接受的、具有持久证据的 TerminalNoPublication，才能关闭对应 D Producer obligation。

### 2.2 Derivative：安全原则一致，最终原子性未解决

<text color="success" weight="medium" size="sm">一致原则</text>

- 私有 staging。
- 精确 Source Version。
- 完整 direct/transitive lineage。
- Scope 和 authority provenance。
- D 依赖注册先于 visibility。
- D 最新 Fence 与 I 当前授权共同参与最终 Gate。
- Gate UNKNOWN 时不得发布。

各 Owner 的责任：

- E：规范化 Claim、Entity、Evidence Span、Summary、Embedding。
- F：Index Segment、Vector、Cache、Graph Projection、Working Set。
- G：ContextEntry、Snapshot、Delta、ChangeSet、Materialized Region、Delivery Payload。

**Finding FEG-03 [BLOCKING]：Lineage Digest 不能替代 D 的完整依赖登记。**

三个契约都表达了完整 lineage，但跨模块仍缺少可核验的共同接口：

- 精确 DerivativeRef/version。
- 完整 Parent/Ancestor 依赖集合。
- D Dependency RegistrationReceipt。
- Dependency Digest 与实际依赖清单绑定。
- 发布操作与 D Fence 的线性化边界。
- Storage PreparedParticipant / Transaction GID 与最终可见性证据。

因此不能以三个 Owner 都写了 `LineageRegistered`，推断 D/E/Storage 原子发布已经实现。

### 2.3 Queue / Retry / DLQ / Lease

<badge color="success">核心语义一致</badge>

| 核验项目 | F | E | G |
|---|---|---|---|
| At-least-once | 是 | 是 | 是 |
| Stable identity | WorkItemId | ProducerWorkItemId | ProducerWorkItemId |
| Digest conflict | 是 | 是 | 是 |
| Attempt 独立 | 是 | 是 | 是 |
| Lease 独立 | 是 | 是 | 是 |
| ACK 非业务终态 | 是 | 是 | 是 |
| DLQ 非终态 | 是 | 是 | 是 |
| Restore quarantine | 是 | 是 | 是 |
| Late ACK 防旧状态覆盖 | 需要补强 | 需要补强 | 明确规定 |

重要裁定：

- Queue ACK 只证明其声明的本地处理边界。
- Lease expiry 只意味着当前租约失效，不意味着任务终止。
- DLQ 仍保留 Forget 约束。
- Retry 不能创建新 WorkItemId 逃避 D Barrier。
- Cancel 是尽力操作，不能替代最终 Publication Gate。
- Missing queue row 不等于工作已经完成。

**Finding FEG-04 [P1]：G Delivery 与 F/E 普通工作 Queue 必须维持独立状态机。**

G 的 `Delivered → Materialized → FinalRequestSubmitted → Applied` 是证据递进，不是简单 Queue ACK 状态。

旧 DeliveryAttempt 的迟到 ACK 只能保留为历史证据，不能覆盖新的 Context target。

### 2.4 Recall：职责分配正确

<box border radius="lg" gap={2} padding={3}>
  **E → F → G 的职责链**

  <box background="rgba(59,130,246,0.08)" radius="md" padding={3}>
    **E — Compiler Source Recall**

    精确 EventRef / MemoryVersionRef 解析、Evidence、Provenance、DerivationRun 输入。
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box background="rgba(16,185,129,0.08)" radius="md" padding={3}>
    **F — Runtime Recall**

    候选生成、检索、Ranking、IndexWatermark、Completeness、最终返回 Gate。
  </box>
  <box align="center">
    <icon name="arrow-down" color="secondary" size="lg"/>
  </box>
  <box background="rgba(168,85,247,0.08)" radius="md" padding={3}>
    **G — Context Membership**

    精确引用重新验证、Scope/Policy 检查、ContextEntry 选择、预算与 ContextVersion。
  </box>
</box>

需要共同满足：

1. Exact MemoryVersionRef，禁止悄悄漂移到新版。
2. Exact Scope、Purpose、Environment。
3. I 当前 PermissionEpoch。
4. D 当前 ForgetFence、Lifecycle 和 Lineage。
5. F 的 IndexWatermark、Gap、Completeness。
6. G 不得把缺失的索引结果解释为源数据不存在。

**Finding FEG-05 [BLOCKING]：I 的授权验证上下文不够完整。**

旧契约虽然都写了 I PermissionEpoch，但没有充分统一：

- Authenticated Issuer / Principal / Workload。
- PolicyDomainRef。
- Purpose、Audience、Delegation。
- Scope 和 Environment 的可信来源。
- 每个受保护操作边界的当前性验证。
- UNKNOWN、incomparable、stale 状态的拒绝规则。

这里必须由 I Owner 定义权威语义，不能由 F/E/G 自行发明授权协议。

### 2.5 Context：没有发现所有权混淆

<badge color="success">语义边界正确</badge>

| 类型 | 唯一 Owner | 生命周期意义 |
|---|---|---|
| F Working Set | F | Runtime-local refs/materialization |
| E Frozen Input Bundle | E | 单次 DerivationRun 的不可变输入 |
| G ContextVersion | G | Context desired membership 的不可变版本 |
| G Delivery | G | 对特定 Adapter/session 的交付记录 |
| G Applied | G | 精确请求边界的 Applied 证据 |

不得使用：

- F IndexWatermark 代表 G ContextVersion。
- E Input Digest 代表 G ContextVersion。
- G ContextVersion 代表 MemoryVersion。
- G Applied 代表 C Execution Success。
- RestoreReconciliationReceipt 代表 Applied。

**Finding FEG-06 [MAJOR]：需要进一步固化 nominal type。**

目前三个文档在文字层面明确区分了这些对象，但尚无统一可验证的类型定义及跨模块拒绝测试。

特别是 `Version`、`Generation`、`Watermark`、`Epoch`、`Sequence` 不得成为无类型的通用标量。

### 2.6 Restore：顺序原则一致，证明模型尚未闭合

| 检查项 | F | E | G |
|---|---|---|---|
| 初始隔离 | 是 | 是 | 是 |
| COC committed prefix | 是 | 是 | 是 |
| I policy/registry | 是 | 是 | 是 |
| D Fence/lineage/producer ledger | 是 | 是 | 是 |
| Storage participant evidence | 是 | 是 | 是 |
| Owner-local replay | 是 | 是 | 是 |
| 最终 Gate | 是 | 是 | 是 |
| 新 Session/Adapter 认证 | Runtime reconnect | 依赖相关消费者 | 明确规定 |

三个文档的步骤排列并不完全相同。这不一定意味着技术矛盾，但不能据此推断 COC、I、D、Storage 存在一个全局数字顺序。

**Finding FEG-07 [BLOCKING]：缺少统一的 Conjunctive Restore Proof Gate。**

必须满足独立证明：

- Storage：DB incarnation、participant、pointer、receipt、visibility。
- COC：committed prefix 和 coordinator continuity。
- I：PolicyDomain、revocation、registry continuity。
- D：ForgetFence、lineage、producer registration/dependency inventory。
- E：Compiler work/outbox/publication continuity。
- F：Index partition watermark 和 invalidation coverage。
- G：Context、Delivery、Adapter reconciliation。
- H/C：相应的 transport 和 final-request 证据。

所有证明必须由各自 Owner 签发和验证。

不得创造统一 `RestoreHighWater` 来代替这些证明。

---

## 3. 重要既有跨 Owner 裁决：A 的整合审查

本轮发现，Issue #21 已存在 A 的四视角整合审查，并且该报告精确对应本轮指定的三个 Commit/Blob。

<text color="secondary" size="xs">Artifact: reviews/integration/phase-3.7-a-d-i-h-cross-review-and-feg-lifecycle-reconciliation.md</text>

- Commit：`3d4e07ed061233031c5f10788861463c71512123`
- Blob：`d9817963f3a8e23f44129a548e67a13bdd54dc2f`

报告的结论：

| 参与者 | 已有语义审查结论 |
|---|---|
| A | ACCEPT WITH ENUMERATED INTEGRATION AMENDMENTS |
| D | ACCEPT WITH D-OWNED BOUNDARY AMENDMENTS |
| I | ACCEPT WITH SECURITY ENFORCEMENT AMENDMENTS |
| H | ACCEPT SEMANTIC HANDOFFS；WIRE NOT FROZEN |
| F/E/G | ACCEPT WITH ENUMERATED AMENDMENTS |

这不是 F/E/G 各 Owner 的独立批准。

报告已经登记 12 个冲突，其中六个 BLOCKING：

| ID | 阻断问题 | 责任 |
|---|---|---|
| LIF-01 | D ProducerClass Registry | D、F、E、G |
| LIF-02 | EventRef-only ingress | D、E |
| LIF-03 | G Delivery 与 D ParticipantIntentRef | D、G、C、I |
| LIF-04 | Restore 独立证明与合取 Gate | A、D、I、H、Storage |
| LIF-05 | I 当前授权逐边界重新验证 | I、F、E、G |
| LIF-06 | H Wire Schema 未冻结 | H、I、B、各 Owner |

另外六项 MAJOR：

- LIF-07：F Read-only Recall 例外范围。
- LIF-08：D Barrier Terminality。
- LIF-09：E/F/G Context 类型分离。
- LIF-10：历史证据不能代替当前授权。
- LIF-11：Index 缺失不能证明 Forget 完成。
- LIF-12：跨 Owner ACK 不能升级为其他 Owner 的业务证据。

**特别更新：LIF-02 有后续状态变化。**

Issue #21 的后续评论 `6940692625` 声称，Phase 3.8 的 D/E 修订已允许在满足 Producer identity、Enabled class、Scope、Digest 和 D-approved lineage token 等条件时，先注册 EventRef-only ProducerWork，再建立 Canonical MemoryRef。

这意味着 A 原先提出的“EventRef-only 必须等待 D 决定”的限制，已经有后续修订声明予以处理。

但本轮没有重新读取该 D/E Phase 3.8 精确契约 Blob，因此：

<badge color="warning">NOT INDEPENDENTLY VERIFIED</badge>

不能直接将 LIF-02 标记为 CLOSED。

## 4. 状态机冲突与遗漏登记

以下是本轮独立归纳的冲突，不能仅因为 A 报告已有类似条目就视为已关闭。

| Finding | 严重度 | 问题 | 状态 |
|---|---|---|---|
| FEG-01 | P1 | ProducerClass 与 D Registry 没有完整接口 | OPEN |
| FEG-02 | P1 | 本地终态与 D Barrier Terminality 不等价 | OPEN |
| FEG-03 | BLOCKING | Lineage Registration 与原子 Publication Gate 未验证 | OPEN |
| FEG-04 | P1 | DeliveryAttempt 与普通 Queue Attempt 的证据边界 | OPEN |
| FEG-05 | BLOCKING | I 完整授权上下文与当前性验证 | OPEN |
| FEG-06 | MAJOR | 三种 Context/Input/Working Set 的 nominal type | OPEN |
| FEG-07 | BLOCKING | Restore 独立证明的最终合取条件 | OPEN |

### 特别需要防止的五个 Crash Window

1. **Registration 成功、Queue 入队失败：** 必须按稳定 WorkItemId 恢复，不能重新注册新身份绕过 D Barrier。
2. **Queue 入队成功、ACK 丢失：** 重试必须幂等，不能重复产生新 DerivationRun 或发布副作用。
3. **Lease 过期、旧 Worker 恢复：** 旧 Lease/Attempt 不得重新发布。
4. **Dependency 注册后、Visibility 前发生 Forget：** 最终 Gate 必须以最新 D/I 状态拒绝旧输出。
5. **Restore 完成但 Adapter/Storage 参与者未完成证明：** 必须继续隔离，不能先恢复服务再清理。

目前三份契约没有提供覆盖上述全部 Crash Window 的实际执行证据。

## 5. 已有测试与缺失测试

这里区分测试源码存在、测试实际运行、生产符合性三个不同层次。

### 5.1 已发现的测试

<box border radius="lg" padding={3} gap={3}>
  **F — Anti-Resurrection Reference Model**

  <badge color="success">TEST SOURCE FOUND</badge>

  `tests/anti_resurrection/test_f_runtime_model.py`

  Blob：

  `c2575327a75577923440ef770d42122218a1e091`

  覆盖内容：

  - Forget 后旧 Index/Cache 不得复活。
  - In-flight Cache Fill 与 Forget 竞态。
  - 旧 Snapshot 重建。
  - Watermark Gap 阻断。
  - PermissionEpoch 失效。
  - Reconnect 清理旧 Working Set。
  - 相同身份幂等、不同 Digest 冲突。
  - F 不得宣称 Global Completion。

  关联模型：

  `tests/anti_resurrection/f_runtime_model.py`

  Blob：`33fa2ca2dc29771aca241e194f13e078a4f8d774`

  **限制：** 这是 F 逻辑参考模型，不是生产 Queue、D Registration 或 Storage 原子性验证。
  <divider color="subtle"/>
  **G — Applied Persistence Reference Model**

  <badge color="success">TEST SOURCE FOUND</badge>

  `06-memory-context/reference_model/test_g_applied_persistence.py`

  Blob：

  `e77d2375506e423bf53d8341fe9aecf2719d0609`

  覆盖内容：

  - Applied 身份幂等。
  - Changed Digest / Revision Conflict。
  - 缺少 Owner Proof 阻断。
  - Crash-before-commit。
  - Lost ACK 重试。
  - Ledger/Outbox 原子提交。
  - 并发重复提交。
  - Forget 后 Current-use Invalidation。
  - Restore Anchor 不一致阻断。
  - Unknown C Outcome 阻断。

  **限制：** 文件明确声明这是 SQLite 单文件参考模型，不是 PostgreSQL Serializable、多副本或生产保证。
  <divider color="subtle"/>
  **E — Compiler**

  <badge color="warning">NOT IDENTIFIED</badge>

  本轮核验的 E 分支相对 main 的文件差异中，没有发现对应的 Phase 3.7 生命周期专用测试文件或工作流。

  这不等于整个 E 项目没有测试，而是当前没有取得对应生命周期契约的测试证据。
</box>

### 5.2 测试覆盖缺口

| 测试场景 | F | E | G |
|---|---|---|---|
| Register-before-Queue Crash | 缺 | 缺 | 缺 |
| Register-before-Lease | 缺 | 缺 | 缺 |
| Stable WorkItem Retry | 部分 | 缺 | 缺 |
| Changed Digest Conflict | 有模型测试 | 缺 | 有模型测试 |
| Stale Lease Worker Publish | 缺 | 缺 | 缺 |
| DLQ 跨 ForgetFence | 缺 | 缺 | 缺 |
| Complete Transitive Lineage | 缺 | 缺 | 缺 |
| D Fence vs Final Publication | 部分 | 缺 | 部分 |
| I Revocation vs Final Visibility | 部分 | 缺 | 部分 |
| Restore COC/I/D/Storage 联合证明 | 部分 | 缺 | 部分 |
| Late Delivery ACK | 缺 | 不适用 | 缺 |
| Applied vs Current-use | 不适用 | 不适用 | 有模型测试 |

这里的“部分”只表示参考模型有相关局部断言，不表示完整跨 Owner 接口已验证。

**测试裁定：**

- F：有逻辑参考模型测试。
- G：有 Applied 持久化参考模型测试。
- E：本轮没有找到对应测试。
- 三方：均没有取得足以证明生产 Conformance PASS 的证据。

## 6. 责任重叠与遗漏

### 责任归属

| 领域 | Accountable Owner | 其他 Owner 的职责 |
|---|---|---|
| Canonical Memory / ForgetFence | D | F/E/G 消费 |
| Producer Registry / Barrier | D | F/E/G 注册及提交证据 |
| Compiler production | E | F/G 消费结果 |
| Runtime retrieval / Index / Cache | F | E/G 提供或消费引用 |
| Working Set | F | G 不得接管 |
| Compiler Input Bundle | E | F/G 不得接管 |
| Context / ContextVersion | G | F/E 提供来源证据 |
| Delivery / Applied | G | H/C 提供传输及请求证据 |
| PermissionEpoch | I | F/E/G 验证 |
| Adapter capability | H | G 消费 |
| Final request submission | C | G 判定 Applied |
| Durable transaction / Visibility | Storage | D/E/G/F 按约定参与 |

### 当前最明显的责任遗漏

1. D 尚需对 ProducerClass Registry 的完整 Admission 规则给出权威定义。
2. D/E/Storage 必须完成原子 Register-before-Visible 契约。
3. D/G/C/I 必须明确 ParticipantIntentRef 与 Provider Submit 的因果顺序。
4. C/G/H 必须形成 Applied 的完整证据链。
5. Storage 必须提供独立的 Restore/Visibility 证据。
6. A 必须在各 Owner 独立决定明确之后完成最终整合，而不是替 Owner 批准。

没有证据表明 F、E、G 有权自行关闭这些责任。

## 7. 各 Owner 后续动作

以下是建议的工作分派，不是替 Owner 下达批准。

<box border radius="lg" padding={3} gap={3}>
  **F — Memory Runtime**

  1. 补齐 D ProducerClass、RegistrationReceipt 的前置要求。
  2. 限定 Read-only Recall 的非持久、非衍生例外。
  3. 明确 IndexWatermark 只代表分区本地覆盖。
  4. 补充 Stale Lease、DLQ、旧 Worker 发布测试。
  5. 明确 Restore 期间 Working Set 的不可服务条件。

  **Decision_ID：NOT_CREATED**
  <divider color="subtle"/>
  **E — Memory Compiler**

  1. 明确 EventRef-only Admission 与 D Registry 的关系。
  2. 补齐 AcceptedReceipt 与 D RegistrationReceipt 的区别。
  3. 明确 Recompile 与 Retry 的不同身份关系。
  4. 增加完整 lineage 和依赖注册测试。
  5. 补齐 Restore 中 PreparedTransactionGID 的冲突恢复测试。

  **Decision_ID：NOT_CREATED**
  <divider color="subtle"/>
  **G — Memory Context**

  1. 区分 Context derivative registration 与 Delivery。
  2. 明确 C Provider Submit 前的 D ParticipantIntentRef。
  3. 保留历史 Applied，独立重新计算 Current-use。
  4. 补齐旧 DeliveryAttempt 迟到 ACK 测试。
  5. 明确 Adapter Offline/Unknown 时的 Context 服务限制。

  **Decision_ID：NOT_CREATED**
  <divider color="subtle"/>
  **D / I / Storage / C / H**

  - D：Producer Registry、Barrier、Lineage、ParticipantIntentRef。
  - I：当前授权和撤销验证。
  - Storage：Crash-safe Visibility、Restore Participant Evidence。
  - C：FinalRequestSubmitted 精确证据。
  - H：Authenticated Transport、Capability、Wire Schema。

  均须由各自 Owner 处理。
</box>

## 8. A 需要整合的冲突

建议 A 最终整合时只保留一个共享生命周期词汇，不建立一个跨 Owner 的巨大统一状态机。

建议共享术语：

```text
Accepted
Registered
Queued
Leased
Running
Staged
DependenciesRegistered
GatePending
Published
Suppressed
Invalidated
Unknown / InDoubt
TerminalNoPublication
RestoredButQuarantined
```

各 Owner 可以保留自己的内部状态，但必须定义与共享术语的映射。

A 还必须明确：

- F/E/G 的 Owner-local ACCEPT 不代表共享 Schema Freeze。
- D/I 的安全批准不能被 A 的技术整合意见替代。
- Storage/C 的生产证据不能由 Reference Model PASS 替代。
- Restore 的证明是多方合取，不是跨 Owner 数值比较。
- Historical Evidence 与 Current-use Eligibility 必须分离。
- Global Forget Completion 只能由有权的治理责任方确认。

### 当前 Issue 状态与版本漂移

本轮额外核对了 #21 的状态及分支变化：

- Issue #21：仍为 OPEN。
- F/E/G 分支均存在。
- 与提供的 main tip 比较，三个分支均已分叉，分别领先 main 41、88、68 个 Commit。
- 分支当前读取到的生命周期文件 Blob 已变化：

| Owner | 原始指定 Blob | 当前分支读取 Blob |
|---|---|---|
| F | `23d00ce7ec60c2145f637e7bc9323294b25b4d77` | `29e9504c75d737c2dd200ebc3306eda555f0b0ac` |
| E | `ef5e735e0fad3cb1b6475ac2532b1f3419d130b8` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| G | `d6d18684ba8a31a538e2e719be3f6e1b715cadf8` | `c1de241ec69834377d9b0e24aa4770a809796d4b` |

Issue #21 评论明确说明，这些后续修订属于整合会话中的 Owner-role-authored proposals，**不是三个 Owner 的独立批准**。

因此本轮不得将旧 Blob 的审查结论自动迁移为新 Blob 的批准，也不得将新 Blob 的存在视为 Owner 决策已经完成。

---

## 9. 最终裁定及登记

<badge color="danger">HOLD — NOT FREEZE-READY</badge>

**总体结论：三份 Owner-local 语义设计可以协调，但跨 Owner 生命周期契约尚未达到批准、冻结或生产实施条件。**

| 项目 | 本轮裁定 |
|---|---|
| Producer | ACCEPT WITH ENUMERATED AMENDMENTS |
| Derivative | CANDIDATE / NO APPROVAL |
| Queue | ACCEPT WITH ENUMERATED AMENDMENTS |
| Recall | ACCEPT WITH ENUMERATED AMENDMENTS |
| Context | ACCEPT WITH ENUMERATED AMENDMENTS |
| Restore | CANDIDATE / NO APPROVAL |
| 共享 Schema | NOT FROZEN |
| 生产实现符合性 | NOT VERIFIED |
| Restore 生产安全性 | NOT VERIFIED |
| Global Forget Completion | NOT CLAIMED |

**正式登记字段：**

| 字段 | 值 |
|---|---|
| Decision_ID | NOT_CREATED |
| Delta_Scope | 本次只读核验，无仓库变更 |
| Relevant_Artifacts | F/E/G 三个指定 Blob + A 整合审查 Blob |
| Evidence | GitHub 精确 Commit/Blob 读取、Issue #21、参考测试源码 |
| Unresolved_Findings | FEG-01 至 FEG-07；LIF-01 至 LIF-06 的权威关闭状态待核验 |

### 停止条件

当前至少三个阻断条件仍然成立：

1. D/I/Storage 的权威接口和原子发布边界没有完整核验。
2. Restore 的跨 Owner 合取证明没有生产级验证。
3. F/E/G 尚未提供可确认的独立 Owner 决策。

因此不建议将 #21 视为已完成，不建议冻结共享接口，不建议批准生产激活。

**建议下一步：** 先取得 F/E/G 三个 Owner 对各自最新 Blob 的具名独立决定，再由 A 对这些精确 Blob 做最终差异审查；D/I/Storage/C/H 的阻断项仍由各自 Owner 关闭。

