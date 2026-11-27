---
document_metadata:
  domain: memory-compiler
  role: design-specification
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
    canonical_status: Canonical
    canonical_scope: "E 域 Memory Compiler 记录 forget-fence-and-derived-registration.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-forget-fence-and-derived-registration"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - forget-fence-and-derived-registration
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# Forget 栅栏、生产者准入与派生发布契约

**状态：** 候选 E 执行约束契约；D 的规范语义为 DECIDED；D/E/Storage 原子登记与最终发布门为 **OPEN / BLOCKING**。I/H/B 契约为候选输入，不是已冻结 schema。
**所有者：** Session E —— Memory Compiler。
**范围：** E 从入站到编译器工作、派生血缘、依赖登记、重放与可见性。
**权限：** D 拥有 ForgetOperation、ForgetFenceCursor、生产者登记账本/屏障与规范抑制。I 拥有 Principal/授权、PermissionEpoch、保留与全局完成策略。E 拥有编译器工作生命周期与执行约束。H 拥有已认证传输绑定/线上协议。B 拥有类型化领域引用语义。Storage/Consistency 必须实现原子可见性边界。F 拥有 IndexWatermark；G 拥有 ContextVersion。

## 1. 安全不变量

在下列条件全部满足之前，任何编译器产出的制品、溯源边、提案、嵌入向量、摘录、缓存项、outbox 载荷或其他派生品，都不得对 Runtime、规范读者、检索、Context、Adapter 或任何其他消费者可用：(a) 其源血缘已持久登记到 D 的依赖清单；(b) 当前授权/PermissionEpoch 与 D 的 ForgetFence 检查成功；(c) 权威的最终 Publication Gate 持久提交。

暂存制品是私有的且不可查询。队列成员身份、Accepted Receipt、Compiler Completion、本地溯源持久化、D Registration Receipt 或单凭一次本地预检查，都不构成暴露它的许可。

若任何检查、登记、门结果或必需权威不可用或有歧义，则保持不可见并失败关闭。逻辑抑制、异步清理与物理擦除彼此不同；E 不能声明全局 Forget 完成或物理删除。

## 2. 从当前分支 HEAD 消费的 D 契约

已读源：`session-d-memory-brain-2026-11-16@30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6`。

| D 拥有的契约 | D 当前的语义决策 | E 的消费 / 边界 |
|---|---|---|
| ForgetOperation 身份 | 持久操作 ID；幂等请求键 + 规范化摘要；精确的类型化目标与目标集合摘要 | E 存储并传播 D 签发的操作/栅栏引用；绝不发明 Forget ID 或目标匹配 |
| ForgetFenceCursor | `(forget_operation_id, fence_generation, target_set_digest)`；单调的 D 代号，与提交游标、权限 epoch 均不同 | 每个 worker/尝试记录观测到的类型化栅栏；在受保护读取与最终可见性边界刷新最新适用栅栏 |
| 生产者登记册 | 封闭世界的生产者类/登记账本；每个工作项在执行前登记，携带稳定的生产者/工作 ID、类别、源引用/修订、范围、操作/关联 ID、准入 CanonicalCommitCursor、观测栅栏与租约/尝试身份 | E 在入队/租约/运行前登记；入队不是准入；登记结果未知时以稳定工作 ID 求解，绝不假定 |
| 生产者屏障 | 栅栏安装原子捕获生产者登记高水位；所有栅栏前已登记工作都必须达到持久终态处置 | E 在重试、DLQ、重放与迟到结果处理期间保持登记开启；任何条目都不会因租约过期或队列删除而消失 |
| 栅栏后准入 | 引用被栅栏目标/血缘的新工作被拒绝、隔离，或仅作为抑制/清理工作准入 | 重新入队/重编译不能因新尝试或当前代号而获得正当性；D 重新评估源祖先 |
| 先登记后可见 | 派生记录 + 依赖边原子提交，或等效的持久准备/提交；最终门在可见性之前紧邻复检最新栅栏 | E 持久化私有暂存输出、登记全部依赖，然后请求最终门；不存在本地检查后直接发布 |
| 目标确认 | 按目标的抑制/清理/未知/例外证据；未知不等于成功 | E 只报告 E 的生产者/作业/派生品范围；D/I 拥有汇总与全局完成判定 |
| 规范提交游标 | 每个 Canonical Memory 权威一个全局序列；独立的 AggregateRevision 与按 Memory 的 LifecycleEventCursor | E 原样存储返回的 CanonicalCommitCursor，并分别存储聚合与生命周期引用 |
| 事务可见性 | 规范写入、聚合头 CAS、LifecycleEvent 追加、CanonicalCommit 记录与 outbox 意图共享同一个原子/可恢复 D 事务；游标仅在持久提交后可见 | E 绝不伪造提交证据或游标；结果未知时按稳定操作键查询 |

**重要精确化：** D 规定的是这些语义义务，而不是可调用的 API 名称、请求/响应 schema 或已验证的 Storage 实现。下文 E 侧的标签仅描述所需操作语义；它们不主张某个 D API 已经存在。

## 3. 编译器工作项身份与生命周期

### 3.1 稳定身份

- `EventRef`：不可变的已接受源事件身份；载荷更正作为新事件/更正链接，绝不是变更。
- `AcceptedReceiptId`：持久的 E 接受证据。
- `CompileIntentId`：随接受一同创建的稳定逻辑处理意图。
- `ProducerWorkItemId`：为一个具备派生能力的逻辑工作项向 D 登记的稳定身份。它不是尝试 ID，也不会因重试而重建。
- `DerivationRunId`：一次执行/运行血缘；重编译会创建与原始 Event/意图以及先前运行关联的新运行，并受当前策略约束。
- `AttemptId` 与 `LeaseId`：每次执行尝试/租约唯一。重试保留 ProducerWorkItemId 并创建新的 AttemptId/LeaseId。
- `DerivedArtifactRef`：一个暂存派生品的稳定身份；派生输出发生变化即为新的不可变制品/版本，而不是覆盖。
- `DependencyRegistrationId` 与 `PublicationOperationId`：用于登记与发布对账的稳定幂等身份。

建议的稳定工作身份派生方式是：在接受/编译意图创建时分配的持久不透明 ID，而不是对载荷文本重新计算的哈希。D 必须在该逻辑工作的每次重试/恢复中收到相同的 ProducerWorkItemId。

### 3.2 状态机

| 状态 | 所有者 / 含义 | D 屏障可见性 |
|---|---|---|
| Accepted | E：Event + 载荷引用 + 幂等回执 + CompileIntent 已持久提交 | 尚未准入；不允许执行 |
| Registered | D 已持久接受 ProducerWorkItem 登记，并返回/可查询 Registration Receipt | **是**；计入 D 登记账本/高水位 |
| Queued | E：已登记意图等待派发 | D 登记保持开启 |
| Leased | E：已取得尝试/租约；包含观测到的 PermissionEpoch 与 ForgetFenceCursor | D 必须能把租约/尝试身份关联到已登记工作 |
| Running | E：受保护读取/抽取/合并执行中 | D 登记保持开启 |
| Staged | E/Storage：不可变输出已持久化到私有暂存；不可查询、不可发布 | D 登记保持开启 |
| DependencyRegistered | 每个必需源/传递依赖都有持久 D Registration Receipt；任何部分集合都不可发布 | D 依赖清单反映全部依赖 |
| Published | 最终 Publication Gate 成功；发布回执持久，且制品可见性已原子切换 | 仅在门证据之后 D 才看到成功的终态处置 |
| CanonicalCommitted | 独立的 D 证据确认规范写入；包含 CanonicalCommitCursor + 精确聚合修订引用 | D 的规范事务具有权威性；不由 Published 推定 |
| Retry | E：针对同一工作/血缘安排重试，新 AttemptId；重新检查当前授权/栅栏 | 登记保持开启；重试不是新的准入旁路 |
| DeadLettered | E：在重试预算/永久错误后停泊；仍可能重放 | 只要重放/发布仍可能，即**非终态**；屏障保持开启 |
| Cancelled / Rejected | 持久终态处置；不可能发布；记录取消/抑制原因 | D 收到终态证据 |
| Terminal | E 声明该工作无法再次发布；全部输出已发布、已规范提交，或已抑制/拒绝并完成对账 | 仅在持久终态确认之后，D 才可将其计入屏障 |

`Published` 与 `CanonicalCommitted` 是两个独立的证据维度：派生品可以被发布而不成为规范 Memory，规范提交也不意味着某个派生投影/索引已发布。适用时，一个工作项可同时携带两种结果。`DeadLettered` 是停泊状态，不是屏障自动完成。租约过期不是 Terminal。

### 3.3 D 可观测状态与 E 内部状态

D 必须观测：生产者类别；稳定的 ProducerWorkItemId；适用时的源引用与精确版本/修订；ScopeRefs；操作/关联/因果引用；准入 CanonicalCommitCursor；观测到的 ForgetFenceCursor；尝试/租约身份；持久登记回执/高水位位置；依赖登记证据；终态处置与证据。

E 内部管理：Accepted、Queued、Running、Staged、重试排程、DLQ 停留、worker 健康与阶段检查点。E 可将这些作为进度遥测暴露，但它们不能替代 D 的屏障账本。只要 D 的账本可靠地把已准入工作保持为开启直到显式终态确认，D 无需镜像每一个内部子状态。

栅栏前登记即使其队列行、worker 进程或租约消失，仍留在屏障之内。只有在每个屏障前登记均为终态、且其产出的每个派生品都在可见性之前完成登记之后，D 的屏障才可关闭。

## 4. 先登记后可见协议

以下是所需的语义序列。等宽字体中的名称是 E 侧的操作意图，不是既有的 D API 声明。

1. **持久入站：** 原子地（或通过已验证的可恢复 WAL）持久化不可变 EventRef/载荷引用/摘要、AcceptedReceipt、幂等行与 CompileIntent/outbox。仅在持久提交之后返回 Accepted。
2. **稳定工作身份：** 分配 ProducerWorkItemId，并与 CompileIntent、源 EventRef、源血缘与幂等上下文一并持久化。
3. **D 生产者准入：** 在入队、租约、受保护载荷解引用或执行之前，把工作登记提交给 D。必需字段见 §7。等待持久 Registration Receipt。若响应丢失，以相同工作 ID 与摘要查询/重试。无回执则不执行。
4. **入队与执行：** 只有 Registered 条目可以 Queued/Leased/Running。每次尝试在访问载荷/源之前以及每个受保护边界处，重新校验已认证 ProducerIdentity、当前授权/PermissionEpoch、Scope 绑定与最新适用 ForgetFence。
5. **私有暂存：** 在私有暂存命名空间中写入不可变 DerivedArtifactRef 与溯源。Runtime、检索、规范读者与下游消费者不得列举/读取暂存行。暂存对象存储 ACL 与元数据状态必须默认拒绝消费者。
6. **依赖登记：** 持久化完整的直接与传递血缘；把每条依赖提交给 D 的依赖清单。等待持久 D Registration Receipt。部分登记、超时或回执未知都会使制品保持不可见。
7. **最终授权/栅栏检查：** 针对全部源祖先、目标引用与 ScopeRefs，刷新当前 I PermissionEpoch 与最新 D ForgetFenceCursor。缓存中的准入时取值不足以支撑发布。
8. **最终 Publication Gate：** 提交精确的制品/版本、工作/运行/尝试/租约 ID、全部依赖回执 ID、请求摘要、当前 PermissionEpoch、观测到的 ForgetFenceCursor 与发布操作键。D 必须把门接受与栅栏安装原子/线性地串行化，并证明登记已持久。
9. **原子可见性：** 只有在持久成功的 Publication Receipt 之后，Storage 才可把制品从私有暂存切换为可见。门与存储可见性切换必须共享同一个事务/可线性化提交协议；否则必须有持久的准备/提交协议，保证崩溃与不确定结果都让制品保持隐藏直到对账。
10. **终态确认：** E 记录 Published/CanonicalCommitted 结果，并在该工作项不再可能发布时，向 D 发送持久终态处置。

本地读取栅栏之后再进行独立的 Storage 写入，被明确判定为不安全。若最终门无法与可见性切换绑定，E 不得发布。

## 5. 失败、幂等与崩溃恢复

| 失败/竞争 | 必需的 E 行为 |
|---|---|
| D 准入不可用/未知 | 不入队、不执行。以 ProducerWorkItemId + 请求摘要求解；绝不假定已准入 |
| D 提交后准入 ACK 丢失 | 查询同一工作 ID；接受同一 D Registration Receipt；不产生第二次逻辑登记 |
| 登记后、入队前崩溃 | D 账本保持开启；恢复时扫描已登记未终结的工作，并以同一工作 ID 重新入队 |
| 重复 Event/消息 | 同一已认证幂等命名空间 + 同一摘要返回原始 Event/回执/CompileIntent/WorkItem；不产生第二次副作用 |
| 同幂等键、不同摘要 | 冲突；保留原始回执；不创建工作 |
| worker 崩溃 / 租约过期 | 租约过期但工作仍为 D 已登记/开启；以新 AttemptId 恢复，并在任何受保护读取前重新检查当前授权/栅栏 |
| 暂存后崩溃 | 暂存输出保持私有；在任何后续动作前对账依赖回执与当前栅栏 |
| 依赖登记部分完成 | 保持不可见；以幂等方式重试缺失登记；不发布部分依赖集合 |
| 登记 ACK 丢失 | 以稳定 DependencyRegistrationId/派生引用 + 摘要查询；不产生重复边或假定成功 |
| 因栅栏/权限 epoch 推进而门拒绝 | 抑制/隔离暂存输出；不得刷新代号后当作同一工作刚刚获得授权而重试 |
| 门 ACK 丢失 | 保持输出隐藏；查询 PublicationOperationId。仅在权威的已提交成功之后才揭示 |
| 门提交后、E 记录回执前崩溃 | 查询同一 PublicationOperationId；记录原始 Publication Receipt；绝不签发不同的发布键 |
| DLQ/重放 | DLQ 保留 EventRef、CompileIntentId、ProducerWorkItemId、血缘与最后安全检查点。重放创建新尝试，而非新权威；重新授权并重新检查栅栏 |
| 重编译 | 新的 DerivationRunId 与溯源版本，关联到原始源血缘；按 D 的要求做新的 D 准入/登记；若任何祖先被栅栏或保留策略拒绝则禁止 |
| 租约丢失/取消/栅栏之后的迟到结果 | 丢弃，或仅保留私有的、策略允许的诊断元数据；绝不发布；D 的终态保持权威 |
| 权限被撤销 | 停止受保护读写；使租约失效；除非 I 授权该精确操作，否则不做新的阶段提交、依赖登记或发布 |
| ForgetFence 推进 | 任何旧租约/尝试均为陈旧；抑制输出并做终态确认；不得把旧工作重挂到最新栅栏 |
| 恢复/重建 | 在让恢复的暂存/派生品可查询之前，重新施加当前 ForgetFence 与授权；旧队列快照不是权威 |

每次重试、重放、DLQ 重入队与重编译都复用或关联原始源身份，并且必须通过全新的授权与栅栏检查。队列状态迁移从不创造权限。较新的栅栏代号不是源合格性的替代品。

## 6. 游标与回执分离

| 类型 | 所有者 / 命名空间 | E 的用途 | 绝不可替代 |
|---|---|---|---|
| SourceEventCursor | E；一个声明的入站分区 | 持久源接受位置；重放/续传 | CanonicalCommitCursor、AggregateRevision、IndexWatermark |
| CanonicalCommitCursor | D；每个 Brain 权威一个全局有序序列 | 存储 D 返回的精确游标，用于规范提交与 as-of 引用 | 源偏移、AggregateRevision、LifecycleEventCursor、IndexWatermark |
| AggregateRevision | D；一个聚合 | 存储精确的不可变 Memory/Entity/Relation 修订身份/序列 | 全局规范游标 |
| LifecycleEventCursor | D；一个 Memory 生命周期流 | 存储精确的生命周期事件位置，并单独记录其所属规范游标 | CanonicalCommitCursor 或 AggregateRevision |
| IndexWatermark | F；索引/通道/分区，应用到某个 CanonicalCommitCursor | 仅作为 F 的类型化确认消费 | D 游标本身或 Forget 证明 |
| ForgetFenceCursor | D；ForgetOperation + 目标集合摘要 + 代号 | 作为栅栏观测；仅在 D 定义的栅栏命名空间内比较 | 任何游标、PermissionEpoch |
| PermissionEpoch | I；已定义的主体/安全策略命名空间 | 在受保护边界重校验当前授权 | ForgetFenceCursor 或提交游标 |
| ContextVersion | G；一个 Context | 仅作为下游上下文版本对待 | 任何 E/D 游标 |
| 投递/Adapter 标识符 | G/H | 关联时不透明传递 | 规范或源游标 |

仅当对应事件实际发生时，E 的回执/溯源才可携带类型化字段。CandidateProposition/ExtractionIR 不携带伪造的 CanonicalCommitCursor。规范提交回执仅在 D 确认提交之后记录。E 不定义也不推进 F 的 IndexWatermark。

## 7. D/E/Storage 原子边界 —— 显式 OPEN 接口

D 当前契约定义了语义要求，但**并未**发布下列各项的可调用 API 名称、完整请求/响应 schema、事务所有权或失败/恢复语义。此处 E 侧的名称是要求，不是对既有实现的声明。

| 所需操作语义 | 所需输入/输出证据 | 原子/线性化要求 | 当前状态 |
|---|---|---|---|
| 生产者工作登记 | 输入：ProducerWorkItemId、生产者类别/身份绑定、源 EventRef + 适用时的规范引用/修订、ScopeRefs、操作/关联 ID、准入 CanonicalCommitCursor、观测到的 ForgetFenceCursor、权限/策略 epoch、请求摘要、尝试/租约身份。输出：持久 Registration Receipt + D 登记高水位/epoch + 接受/拒绝处置 | 登记账本提交必须线性化在 E 的入队/租约/执行之前，并与栅栏安装排序 | **OPEN —— D schema/API + Storage 事务** |
| 依赖登记 | 输入：DerivedArtifactRef/版本、ProducerWorkItemId/DerivationRunId、完整源/传递源引用或已批准的不透明令牌、精确源版本、ProvenanceRef、ScopeRefs、血缘摘要、观测栅栏。输出：持久 Derived Registration Receipt、登记 ID 与清单位置 | 依赖边与派生品登记必须在任何可见性之前持久；重复登记幂等 | **OPEN —— D 账本 API + E/Storage 原子性** |
| 最终发布门 | 输入：PublicationOperationId、制品/版本、工作/运行/尝试/租约 ID、全部依赖回执 ID、当前 PermissionEpoch、当前 ForgetFenceCursor、请求摘要。输出：已提交/已拒绝结果、持久 Publication Receipt 与权威栅栏/登记证据 | 门决策必须与栅栏安装串行化，并原子控制 Storage 可见性；或使用已验证的可恢复准备/提交协议，在不确定时保持制品隐藏 | **OPEN / BLOCKING —— D/E/Storage** |
| 生产者终态确认 | 输入：ProducerWorkItemId、最终尝试/租约、终态处置、全部输出/登记/发布引用、原因与摘要。输出：持久终态回执 / 屏障账本更新 | 只有在持久确认之后，D 屏障才把条目计为终态；租约过期/队列删除都不意味着终态 | **OPEN —— D 响应 schema + 对账语义** |
| 当前栅栏/权限查询 | 输入：精确目标/源祖先与 Scope；输出：最新适用 ForgetFenceCursor 与当前 I PermissionEpoch/决策 | 新鲜度与一致性保证必须覆盖最终门；陈旧缓存值不能授权发布 | **OPEN —— D/I API 一致性与 epoch 查询语义** |

### 7.1 需向 D 提出的最小接口问题

1. 哪个精确 API/命令持久登记一个 ProducerWorkItem，以及在规范对象存在之前，仅凭 EventRef 入站需要哪些字段/类型化引用？
2. D 的登记覆盖一个逻辑工作项，还是每次尝试分别登记？重试、DLQ、租约替换与重编译如何被关联而不产生未被追踪的屏障缺口？
3. 精确的回执身份、登记高水位字段/类型、生产者登记册版本与按幂等键查询操作分别是什么？
4. 哪个精确 API 持久登记一个 DerivedArtifactRef 及其每条源依赖？D 是否要求 E 在持久化最终制品行之前先取得准备令牌？
5. 哪个操作原子地安装/推进 ForgetFence 相对 ProducerWork Registration 的次序？当准入与栅栏安装竞争时，线性化顺序是什么？
6. 哪个精确的最终门操作接受依赖回执与 PermissionEpoch/ForgetFenceCursor，并且它拥有可见性翻转，还是返回一个 Storage 必须消费的令牌？
7. 若 Storage 拥有可见性翻转，是什么共享事务、锁/CAS、栅栏令牌或事务性 outbox 协议，使门接受与可见性成为同一个可线性化事件？
8. ACK 丢失、提交后超时、重复回执、部分依赖登记、摘要冲突、租约过期与迟到结果如何查询/对账？
9. 持久终态处置的枚举是什么，哪些 DLQ 状态仍保持屏障开启？
10. 哪些源引用对 D 的清单有效（EventRef、MemoryRef、MemoryVersionRef、EvidenceRef、不透明令牌），传递祖先与 Scope 匹配如何校验？

### 7.2 E 的失败关闭停止条件

E 必须在受影响动作之前停止，当：
- 无法建立持久 D Producer Registration Receipt；
- D 无法确定最新适用 ForgetFenceCursor；
- I 无法确定已认证 Principal/ProducerIdentity 与当前 PermissionEpoch；
- 该操作的 ScopeRef 语义或安全域绑定未决；
- 任何必需的依赖登记缺失/部分/未知；
- 无法证明最终门与 Storage 可见性共享原子/可线性化边界；
- 租约/尝试陈旧、被撤销、已过期或被栅栏；
- 源或祖先已被遗忘、不符合保留策略或未获授权；
- D 的屏障账本报告缺口、未知生产者类别或未解决的先前尝试。

任何可用性回退、手工队列重放或运维覆盖都不得绕过这些条件。只有 I 拥有的显式策略例外可以改变 I 策略；它不能发明 D API，也不能消除可审计 D 屏障的必要性。

## 8. 安全与类型化身份对齐

- ProducerIdentity 绑定到已认证传输上下文：已认证 Principal/签发方、已登记生产者/应用身份、实例/工作负载身份、凭据/密钥有效期、允许的事件族、租户/安全域与撤销/凭据 epoch。
- 载荷中的 `producer_id`、`ProducerId`、`ActorRef`、`agent_id` 或 `scope_ref` 是声明/选择器，绝不是认证。H 绑定传输主体；I 校验信任/策略。不匹配即拒绝或隔离。
- ActorRef 是 B/I 对 Principal 与权限链的类型化引用，不是持有型凭据。E 绝不接受调用方构造的 ActorRef 作为证明。
- ScopeRef 使用 B 的类型化领域引用语义。Scope 成员身份/适用性不是授权；I 对每个源与操作分别授权。
- 当前 PermissionEpoch 在入站、受保护解引用之前、每次敏感阶段提交之前、需要时的 D 登记之前、规范写入提交之前与最终发布处重新检查。准入时 epoch 是一次观测，不是永久能力。
- 幂等命名空间绑定到已认证 Principal + ProducerIdentity + 已校验 Scope 绑定 + 租户/安全域 + 操作/事件族 + 调用方键。精确字段编码，以及多个 ScopeRef 是否构成规范集合，仍为 **CANDIDATE / 需 H-I-B 批准**。ScopeRef 不得被视为授权。
- 若认证、主体绑定、Scope 解析、策略 epoch、保留或撤销状态未知，则失败关闭。

H 的消息信封文档与 I 的 Principal/ActorRef 契约为候选输入，不是已冻结的线上协议/策略 schema。

## 9. 一致性场景（NOT RUN）

1. 在 D 登记回执持久之前，工作项不能被租用。
2. Forget 与准入竞争被串行化：登记要么被纳入已捕获屏障，要么被拒绝/隔离。
3. 每个栅栏前工作项在 worker 崩溃、租约过期、重试与 DLQ 期间对 D 始终可见。
4. 在仍可重放时，DLQ 条目不计为终态。
5. 在全部依赖回执与 Publication Receipt 存在之前，派生制品不能被 Runtime/消费者读取。
6. 依赖登记与最终门之间发生 Forget，会拒绝陈旧发布。
7. PermissionEpoch 在租约与门之间推进；旧尝试不能发布。
8. 重复事件与丢失的 Accepted ACK 返回同一回执/工作身份。
9. 丢失的 D 登记 ACK 返回同一回执，且不产生重复登记。
10. 丢失的 Publication ACK 使制品保持隐藏，直到查询证明门已提交。
11. 取消/栅栏之后的迟到 worker 结果不能变为可见。
12. 传递祖先的 Forget 会抑制"派生品的派生品"。
13. 跨范围血缘不能扩大授权。
14. 恢复/重放在可查询之前重新施加当前栅栏。
15. Canonical 游标按 Brain 权威全局有序；聚合修订/生命周期游标保持独立；E 绝不重写 F IndexWatermark。

**验收：** 仅记录设计要求。不声称任何运行时实现、Storage 原子性、一致性测试或生产安全。



---
## 第 3.5 阶段 —— D 到 E 的操作映射与发布门证据

**规范边界：** 下文操作名称是为本工作流提供的 D 操作契约名称。本节仅陈述 E 的消费要求。它不声明可调用 API、不填补 D 拥有的 schema 缺口，也不证明 Storage 原子性。

### 1. D 到 E 的操作映射

| D 操作 | E 的调用点 | 必需的 E 输入/证据 | E 消费的必需 D 结果 | E 的失败行为 / OPEN |
|---|---|---|---|---|
| RegisterProducerWork | 在持久 Accepted/CompileIntent 身份创建之后、入队/租约/运行之前；恢复时重复查询 | 稳定 ProducerWorkItemId；ProducerClass ID/版本；已认证 ProducerIdentity 绑定；EventRef + 可用的规范源引用/精确修订；血缘摘要；ScopeRefs；操作/关联/因果 ID；准入 CanonicalCommitCursor；观测到的 ForgetFenceCursor；PermissionEpoch/决策引用；请求摘要 | 持久 ProducerRegistrationReceipt 与登记高水位/账本位置；显式的接受/拒绝结果 | ACK 未知 => 以同一 ID/摘要查询，不派发。OPEN：精确字段、错误、生产者类登记 API、仅 EventRef 源语义、高水位类型与栅栏竞争线性化 |
| InstallForgetFence | D 拥有的 Forget 工作流；E 是消费者/参与者，不是安装者 | E 保留已登记工作 ID、尝试/租约清单、血缘、输出清单与最新已知登记回执；消费栅栏/目标/屏障快照 | 持久栅栏身份/代号、生产者登记屏障高水位、受影响目标摘要、安装提交位置与可恢复通知 | E 停止或隔离受影响工作，对账屏障前条目。OPEN：通知/查询 schema、D 是否返回完整逐条目屏障快照、排序/一致性 SLA |
| RegisterDerivedDependency | 不可变输出已私有暂存之后、任何可见性切换之前 | DerivedArtifactRef/版本；ProducerWorkItemId；DerivationRunId/AttemptId；直接 + 传递源引用/精确版本或已批准的不透明令牌；ProvenanceRef；ScopeRefs；血缘摘要；观测栅栏；幂等键/摘要 | 每条必需边/制品的持久 DerivedRegistrationReceipt，以及清单位置与显式重复/冲突结果 | 部分/未知登记 => 制品保持私有；以同一键/摘要求解。OPEN：权威源引用类别、D 与指定清单服务的所有权、原子批量/部分语义、精确回执字段/错误 |
| PublishDerivedIfFenceCurrent | 紧邻发布之前，在全部依赖回执与当前授权确立之后 | PublicationOperationId；制品/版本；ProducerWorkItemId；DerivationRunId；AttemptId/LeaseId；全部依赖回执 ID；源血缘摘要；ScopeRefs；当前 I 授权决策 + PermissionEpoch；观测到的 ForgetFenceCursor；请求摘要 | 持久 PublicationReceipt，绑定制品/版本、精确依赖、已检查栅栏、权限 epoch、可见性结果与提交身份 | 任何陈旧/未知栅栏、授权失败、回执缺失或结果歧义 => 不产生可见性；查询同一操作 ID。OPEN：D 是执行可见性提交，还是签发一次性令牌由 Storage 原子消费；跨存储线性化与错误分类 |
| CompleteProducerWork | 仅在全部输出、依赖、发布/规范提交与"不再发布"结果都已持久对账之后 | ProducerWorkItemId + RegistrationReceipt；终态处置；全部 Attempt/DerivationRun ID；输出清单摘要；依赖/发布/规范回执引用；观测到的最终栅栏 + 授权证据；终态请求摘要 | 持久终态确认与屏障账本状态；同证据幂等结果或冲突 | ACK 丢失 => 以同一工作 ID/摘要查询；绝不在本地假定屏障已关闭。OPEN：终态枚举/schema、必需证明完整性、迟到派生品的重开/失效行为 |

InstallForgetFence 不是 E 的 API 调用。E 消费其持久结果，并确保被捕获屏障内的每个 E 工作项在终态确认之前始终可被发现。E 不主张安装或推进 D 栅栏的权限。

### 2. 必需的操作顺序

1. 持久化 AcceptedReceipt + CompileIntent + 稳定 ProducerWorkItemId/outbox。
2. 确认 ProducerClass 登记处于活动状态（类登记 API 仍为 D OPEN）。
3. 调用/求解 RegisterProducerWork；在其持久回执已知之前不入队、不租用、不执行。
4. 获取 LeaseId/AttemptId；在受保护源读取之前重校验当前 I 授权/PermissionEpoch 与 D 栅栏。
5. 执行编译阶段，仅把不可变 Candidate/Staged 制品写入私有存储。
6. 构建完整的直接/传递依赖集合，并对每个制品/版本/边调用/求解 RegisterDerivedDependency。
7. 紧邻门请求之前重新授权，并获取/校验最新适用栅栏。
8. 调用/求解 PublishDerivedIfFenceCurrent；可见性切换必须共享 D 规定的原子边界。若不存在此类已验证边界，则保持暂存/私有。
9. 将 PublicationReceipt 与 CanonicalCommitReceipt、IndexAppliedAcknowledgement 分开记录。
10. 仅在终态处置已持久且不再有未结算的重试/重放/发布路径时，才调用/求解 CompleteProducerWork。

### 3. 暂存、依赖持久性与可见性

- CandidateProposition、ExtractionIR、规范化输出、合并候选、嵌入向量、摘要、溯源边、outbox 载荷与所有其他派生品，在发布成功之前均为私有。
- 暂存存储必须排除在 Runtime 检索、规范读取、F 索引器、G 上下文构建、H 投递、导出与通用检索之外。"UI 未链接"不是访问控制边界。
- 依赖登记持久且幂等。在完整必需依赖集合被确认之前，派生品不具备发布资格。部分成功是私有的未完成状态，绝不是部分可见。
- 最终门在其线性化点检查最新 D 栅栏与当前 I 授权。预检查、worker 租约、较早代号、缓存权限决策或本地 E 数据库读取均不充分。
- 栅栏安装与最终发布必须串行化：要么发布先线性化并被纳入屏障/清单，要么栅栏安装胜出而发布被拒绝/隔离。不存在"迟到派生品在屏障之外变为可见"的第三种结果。
- 若依赖登记与可见性无法成为一个原子事务，则只接受 D 批准的、具备恢复能力且"提交前不可见"语义的持久准备/提交协议。未经协调的"D 令牌然后 Storage 写入"不充分。
- 任何栅栏/授权/血缘/回执失败都使制品保持私有，并把工作标记为阻塞/抑制。E 不得静默丢弃或报告成功。

### 4. 发布门证据包

| 证据 | 必需绑定 |
|---|---|
| 工作身份 | ProducerClass ID/版本、ProducerWorkItemId、ProducerRegistrationReceipt、DerivationRunId、AttemptId、LeaseId |
| 源血缘 | EventRef、源规范引用 + 精确修订、完整直接/传递血缘摘要、ProvenanceRef、ScopeRefs |
| 授权 | 已认证 ProducerIdentity 引用、I PolicyDecision 引用、PermissionEpoch、动作/资源/受众/范围绑定、门处决策有效性 |
| Forget 状态 | 门处观测到的最新 D ForgetFenceCursor/代号、目标集合/血缘适用性结果、D 门决策引用 |
| 依赖证明 | DerivedRegistrationReceipt ID 的完整列表/摘要与清单位置 |
| 发布证明 | PublicationOperationId、PublicationReceipt、制品/版本、可见性提交身份/时间与结果 |
| 恢复证明 | 幂等请求摘要、ACK 查询/恢复结果、关联/因果 ID |

证据包仅证明所指的发布边界。它不是全局 Forget 完成证明、物理擦除证明、F 索引水位或 G 上下文投递证明。

### 5. 显式 OPEN 契约缺口（不得提升为 DECIDED）

- OPEN-E/D-01 RegisterProducerWork：ProducerClass 登记/版本、仅 EventRef 入站、源修订可用性、已认证生产者绑定、登记高水位类型、精确回执与重复/冲突/错误码。
- OPEN-E/D-02 RegisterProducerWork 与 InstallForgetFence：并发准入与栅栏安装的事务/线性化规则与精确串行化结果。
- OPEN-E/D-03 RegisterDerivedDependency：权威清单所有者、完整源引用类型集合、传递闭包规则、批量/部分行为、回执与重试/错误语义。
- OPEN-E/D-04 PublishDerivedIfFenceCurrent：精确的最新栅栏读取/串行化与授权检查、输出/证据 schema、门是提交可见性还是协调 D/Storage CAS/事务。
- OPEN-E/D-05 CompleteProducerWork：终态处置、终态证据 schema、迟到派生品失效/重开行为、ACK 查询与冲突规则。
- OPEN-E/ST-06 Storage 原子性：原子依赖登记 + 可见性、持久准备/提交替代方案、崩溃恢复、隔离与读路径执行约束均未选定或测试。
- OPEN-E/I/B/H-07 身份绑定：精确的 ActorRef/ScopeRef/ProducerIdentity schema 仍属 B/I/H 联合工作；Fact/Claim ADR 仍为 ADR-BLOCKED。
- OPEN-E/I-08 保留：幂等/墓碑与重放证据的保留视野仍归 I 所有，且数值为 OPEN。

### 6. 故障与竞争一致性矩阵（仅设计；未执行）

| ID | 竞争/故障 | 必需的安全结果 | 所需证据 |
|---|---|---|---|
| D-RACE-01 | RegisterProducerWork 与 InstallForgetFence 竞争 | 恰好一个串行化结果：被纳入已捕获屏障之内/之下，或被拒绝/隔离；绝不出现未被追踪的已准入工作 | D 登记回执/高水位、栅栏屏障快照、事务排序结果 |
| D-RACE-02 | 栅栏安装时存在已入队工作 | 队列条目留在 D 屏障内；取消/隔离或排空到持久终态处置 | 工作 ID、队列/outbox 状态、终态 ACK |
| D-RACE-03 | 已租用/在途编译在栅栏之后完成 | 最终门拒绝；暂存输出保持私有并被抑制/隔离 | 尝试/租约 ID、观测/当前栅栏、门拒绝、私有暂存证明 |
| D-RACE-04 | 栅栏之后重试调度器触发 | 同一工作 ID 仍保持屏障开启；新尝试重检当前栅栏/授权，且不能发布陈旧血缘 | 重试事件、新 AttemptId、登记查询、拒绝/终态证据 |
| D-RACE-05 | 栅栏之后 DLQ 重放 | 重放按原始血缘登记/对账，并因源被遗忘而被拒绝/隔离 | DLQ 条目、重放 AttemptId、栅栏结果 |
| D-RACE-06 | 栅栏排空期间租约过期 | 过期不关闭屏障；恢复创建新尝试或给出显式终态证据 | 租约历史、未解决工作账本、恢复/终态 ACK |
| D-RACE-07 | 依赖登记部分完成 | 制品保持私有；以同一幂等键继续或隔离 | 逐边回执、缺失边集合、"不可见"断言 |
| D-RACE-08 | 暂存之后、最终门之前栅栏推进 | 最新栅栏胜出；发布被拒绝 | 暂存制品、栅栏代号、门结果 |
| D-RACE-09 | 门之前 PermissionEpoch 被撤销/推进 | 授权失败关闭；即使 Forget 栅栏未变也不可见 | PolicyDecision、旧/当前 epoch、门拒绝 |
| D-RACE-10 | 屏障/证明之后发现迟到派生品 | 立即抑制；登记目标、使证明失效/重开并告警 D/I；不得静默完成 | 血缘、发现时间、新依赖条目、失效事件 |
| E-FAULT-11 | D 登记之后编译器进程崩溃 | 以同一 ProducerWorkItemId 与意图恢复；绝不创建未追踪的重复 | 登记回执查询、恢复日志、尝试序列 |
| E-FAULT-12 | outbox 重放重复派发 | 至少一次重放解析为同一工作/回执；不产生重复逻辑工作或副作用 | outbox 事件 ID、工作 ID、幂等摘要、重复结果 |
| E-FAULT-13 | DLQ 重放重复或并发 | 同一工作 ID；不同尝试；一个终态/发布结果，重复项幂等对账 | DLQ ID、AttemptIds、门/发布回执 |
| E-FAULT-14 | Forget 之后重编译 | 新 DerivationRunId 不能绕过原始源血缘；D 拒绝/隔离被遗忘祖先 | 原始 EventRef/工作 ID、先前运行、新运行、当前栅栏决策 |
| E-FAULT-15 | 重复提交 AcceptedReceipt | 同一已认证命名空间 + 同一语义摘要返回原始回执/意图；不产生重复准入 | 回执 ID、幂等键/摘要、既有工作身份 |
| E-FAULT-16 | 丢失 RegisterProducerWork ACK | 在按同一 ID/摘要查询证明持久登记或拒绝之前，不入队/不租用 | 请求摘要、查询响应、派发挂起 |

这些用例仅为规格验收标准。不声称任何运行时测试、故障注入、竞争执行或实现一致性。



---
## 第 3.5 阶段附录 —— 与精确 D 操作集合对齐

在 D 较新的规范操作契约定义了额外操作与更精确语义之处，本附录取代上文 §1 中简略的五行为操作清单。D 操作源：session-d-memory-brain-2026-11-16 上的 03-memory-brain/forget-fence-operation-and-publication-gate.md（blob 2c5b1358ff58f99af838b741a75966ccd07ad088）。D 的决策日志记录 D35-01 至 D35-10。这些是 D 的语义决策，不是可调用 API 或 Storage 实现的证明。

| D 规范操作 | E 的消费 / 产出 | D 的持久结果 / 关键语义 | E 的错误/恢复处理 |
|---|---|---|---|
| RegisterProducerClass | E 在接受派生工作之前登记编译器、抽取/合并、重放、重编译及其他具备派生能力生产者类别 | ProducerClassRegistrationReceipt、ProducerRegistryVersion、ENABLED/DISABLED/QUARANTINED 状态与生效登记册序列；键为类 ID + 版本 + 摘要 | 未知/禁用/不完整类别失败关闭；禁用后既有工作仍被追踪。OPEN：与 I/A 的全局清单对账及精确 H/B 身份绑定 |
| RegisterProducerWork | E 在入队、租约、源解引用或执行之前登记稳定逻辑工作 | RegistrationReceipt，含 ProducerRegistrationSequence、ProducerRegistryVersion、准入栅栏观测与 ACCEPTED/REJECTED/QUARANTINED/CLEANUP_ONLY 处置；键为 WorkItemId + 规范摘要 | 同 ID/摘要解析为同一回执；摘要变化即冲突。登记/栅栏竞争遵循 D 的单一可线性化顺序。支持仅 EventRef 入站，但 E 必须在规范引用/修订可用后立即关联 |
| InstallForgetFence | 由 D 安装；E 消费并反应 | ForgetFenceCursor + 安装 CanonicalCommitCursor + 捕获的 ProducerRegistryVersion + ProducerRegistrationHighWater + 目标快照/水位 + outbox 意图；键为 ForgetOperationId + 目标/请求摘要 | E 必须停止/对账被覆盖工作。栅栏安装与登记属于同一个 D 串行化域。E 不安装也不推进栅栏 |
| CaptureProducerRegistrationHighWater | E 在对账期间消费不可变快照回执 | BarrierSnapshotReceipt，含精确高水位、登记册版本、目标摘要、栅栏代号与账本一致性证明；键为栅栏 + 快照键 | 重复捕获不能推进截止点。快照缺失/有缺口 => UNKNOWN/阻塞；绝不近似高水位 |
| RegisterDerivedDependency | E 在可见性之前登记每个暂存制品与完整血缘 | DependencyRegistrationReceipt + 清单位置；键为 DependencyRegistrationId + 规范摘要；完整的直接/传递引用、父制品回执、溯源、范围、栅栏与权限证据 | 部分/未知边集合保持私有；同键/摘要查询；不同摘要冲突；血缘变化必须产生新的不可变制品版本 |
| PublishDerivedIfFenceCurrent | E 在紧邻可见性之前提交完整门证据 | PublicationReceipt 绑定登记、类别/版本、工作/尝试/租约/运行、源修订、范围、观测与权威栅栏、I PermissionEpoch 决策、每条依赖回执、制品与可见性提交身份；键为 PublicationOperationId + 摘要 | 门与可见性、最新栅栏及当前权限一同线性化。被栅栏/陈旧/不完整/权限/存储不可用的结果保持私有。不允许独立的检查后写入，也不允许延迟的未绑定令牌 |
| CompleteProducerWork | 仅在不再有发布/重放路径时，E 提交终态处置 | ProducerWorkTerminalReceipt、屏障状态、未解决输出计数与对账游标；键为 WorkItemId + 终态摘要 | 终态单调；同摘要幂等；冲突返回终态冲突。租约过期、队列删除、worker 关闭与 DLQ 停泊都不是终态 |
| ResolveProducerWork | E 在 ACK 丢失、超时、崩溃或恢复之后使用 | 权威的登记/依赖/发布/终态回执、当前租约/尝试与屏障成员身份；只读键为 WorkItemId + 原始登记摘要，可选操作 ID | UNKNOWN/账本不可用仍失败关闭；查询绝不创建工作或推进栅栏；复用原始 ID/摘要 |
| ReconcileForgetBarrier | E 提供证据并消费 D 的屏障处置 | BarrierReconciliationReceipt，含精确高水位、已纳入/终态/开启/过期/DLQ/未知计数、依赖水位、迟到派生品计数、登记册缺口与 DRAINED/OPEN_WORK/OPEN_DEPENDENCY/REGISTRY_GAP/LATE_DERIVATIVE/UNKNOWN；键为栅栏 + 快照/检查点 | 仅追加的检查点；任何迟到派生品/缺口都会重开对账。D 仅断言 D 本地屏障；I 决定全局完成 |

### E 消费的 D 操作错误语义

E 必须保留类型化的非成功结果，而不是把它们压平成"重试成功"：

- 生产者类/准入：UNKNOWN_PRODUCER_CLASS、CLASS_DISABLED、REGISTRY_INCOMPLETE、FENCE_CLOSED、FENCE_UNKNOWN、PERMISSION_STALE_OR_DENIED、SCOPE_INVALID、SOURCE_LINEAGE_INVALID、IDEMPOTENCY_CONFLICT。
- 栅栏/快照：FENCE_STATE_CONFLICT、SERIALIZATION_RETRY_EXHAUSTED、FENCE_NOT_INSTALLED、FENCE_MISMATCH、LEDGER_GAP、SNAPSHOT_UNAVAILABLE。
- 依赖：WORK_NOT_REGISTERED、WORK_TERMINAL、SOURCE_FENCED、LINEAGE_INCOMPLETE、SCOPE_MISMATCH、ARTIFACT_ID_CONFLICT、DEPENDENCY_NOT_DURABLE。
- 发布：REGISTRATION_NOT_DURABLE、WORK_NOT_ACTIVE、ATTEMPT_STALE、LEASE_STALE、FENCE_ADVANCED_OR_COVERS_ANCESTOR、FENCE_UNKNOWN、PERMISSION_EPOCH_STALE_OR_REVOKED、DEPENDENCY_NOT_DURABLE、STORAGE_ATOMICITY_UNAVAILABLE。
- 完成/恢复：OUTPUT_UNRECONCILED、PUBLICATION_UNKNOWN、LEASE_STILL_VALID、REPLAY_STILL_POSSIBLE、TERMINAL_CONFLICT、EVIDENCE_INCOMPLETE、DIGEST_MISMATCH、RECEIPT_NOT_RETAINED、LEDGER_UNAVAILABLE、DEPENDENCY_INVENTORY_GAP、RECONCILIATION_UNAVAILABLE。

上述错误名称为 D 的语义词汇；精确的传输/线上编码与 API 暴露仍为 OPEN。E 只能在保留原始类型化原因与可重试性的前提下于内部映射。

### 附加的精确线性化规则

- RegisterProducerClass 在持久登记册版本/状态提交处线性化；工作准入必须观测到已启用且已提交的版本。
- RegisterProducerWork 在持久工作账本插入处、与 InstallForgetFence 同一排序域内线性化；ProducerRegistrationSequence 仅在此处分配。
- InstallForgetFence 在一个持久规范事务处线性化，该事务使栅栏生效并捕获登记册版本 + 工作高水位。
- CaptureProducerRegistrationHighWater 是与安装事务/版本绑定的持续快照读；它校验但绝不改变不可变截止点。
- RegisterDerivedDependency 在制品记录与全部必需依赖边的持久提交处线性化；部分边持久化不是成功。
- PublishDerivedIfFenceCurrent 在单个持久可见性提交处线性化，并在该点校验当前栅栏、依赖/登记状态与 I 授权。
- CompleteProducerWork 在证据校验之后、持久 D 终态处置提交处线性化。
- ResolveProducerWork 是一致性读；若无法确立权威当前状态，必须返回 UNKNOWN。
- ReconcileForgetBarrier 是跨屏障账本、依赖清单与目标清单的一致、带版本快照；DRAINED 结果仅适用于那些检查点。

### 类型化序列命名空间更正

ProducerRegistrationSequence / ProducerRegistrationHighWater 与 ProducerRegistryVersion 归 D 所有，与 CanonicalCommitCursor 不同。它们必须按类型化值存储，且绝不与 CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor、ForgetFenceGeneration、PermissionEpoch、IndexWatermark 或 ContextVersion 相互替代或做数值比较。



---
## 第 3.5 阶段附录 —— OPEN 项精确化更正

在 §5 中较早的 OPEN-E/D-01 至 OPEN-E/D-05 措辞可能被读作"D 尚未规定操作级输入、输出、幂等、错误结果或线性化"之处，本节予以取代。D 的规范操作契约现已为全部九项操作规定了这些语义要素。剩余缺口更窄：

| OPEN ID | 精确的未解决项 | 所有者 / 为何仍开放 |
|---|---|---|
| OPEN-API-01 | D 语义操作的可调用 API/传输 schema、序列化、认证绑定、兼容/版本协商与错误到线上错误的映射 | D + H + B/I；D 明确声明语义操作契约不主张公共 API 或线上 schema |
| OPEN-STORAGE-01 | 具名且可问责的 Storage/Consistency 所有者；选定的 事务/CAS/可串行化协议；持久隐藏准备/提交；副本/读一致性；崩溃/恢复行为；栅栏安装与可见性提交串行化的证明 | D 审阅中 Storage/Consistency 所有者未指派；语义契约不是实现证据 |
| OPEN-I-AUTH-01 | 最终门处 I 权威 PermissionEpoch 的新鲜度/相等性/决策查询、决策有效性与撤销传播 | 归 I 所有；E 不能定义策略语义 |
| OPEN-REGISTRY-GLOBAL-01 | 将 D 本地 ProducerRegistryVersion/ProducerRegistrationHighWater 与 I 的全局生产者/接收方清单及 A/模块所有权登记册对账；证明封闭世界完整性 | I/A + 模块所有者；仅 D 本地账本不能证明全局清单完整性 |
| OPEN-RECOMPILE-01 | 重编译所需的精确关联子项/再准入身份规则，以及是否需要独立的 ProducerWorkItemId | D/E；D 要求显式的关联子项/再准入决策，但未冻结 E 的运行模型 |
| OPEN-TEST-01 | 可执行的竞争/故障夹具、存储故障注入、实际期望/观测输出与所有者签核 | D/E/Storage + 受影响消费者；此处所有矩阵仍仅为设计 |

"精确字段"、"精确回执/错误 schema"、"高水位类型"与"与 InstallForgetFence 的串行化"等较早措辞，不再可作为"D 的语义契约未规定"的陈述。D 已规定语义字段与单一顺序竞争。仍开放的是其可调用传输/API 实现、全局清单对账与经测试的存储线性化。不得为填补这些实现缺口而发明 D 决策。


---

## 第 3.5 阶段重校验 —— D 到 E 的操作映射与故障一致性

D 的规范操作语义按其原文消费；本表不是替代 API 或传输 schema。

| D 操作 | E 的调用 / 证据 | E 持久化的 D 回执/结果 | E 的失败/未知行为 |
|---|---|---|---|
| RegisterProducerWork | 入队/租约/解引用/运行之前；稳定 WorkItemId、ProducerClass/版本、已认证 ProducerIdentity 绑定引用、源 EventRef/精确修订或血缘令牌、ScopeRefs、观测栅栏、PermissionEpoch 决策引用、摘要 | RegistrationReceipt、ProducerRegistrationSequence、ProducerRegistryVersion、处置 | 不入队/不租用/不运行。以同一 WorkItemId+摘要求解；未知即未解决。 |
| InstallForgetFence | D 拥有；E 消费栅栏与屏障快照 | ForgetFenceCursor、安装 CanonicalCommitCursor、捕获的登记册版本/高水位、BarrierSnapshotReceipt | 当权威栅栏可见时停止受影响的准入/发布；对账栅栏前工作。绝不从游标推导栅栏代号。 |
| RegisterDerivedDependency | 私有暂存与完整血缘之后、任何读者/索引/下游可见性之前 | DependencyRegistrationReceipt、清单位置与完整边集合证据 | 部分/未知登记使所有暂存制品保持私有；以同一 DependencyRegistrationId+摘要求解。 |
| PublishDerivedIfFenceCurrent | 最终可见性边界；登记回执、全部依赖回执、制品/版本、WorkItem/Run/Attempt/Lease、血缘、ScopeRefs、观测栅栏、当前 I 决策/PermissionEpoch、PublicationOperationId/摘要、私有暂存引用 | PublicationReceipt、权威栅栏/权限决策、依赖证据与可见性提交身份 | 失败关闭。本地预检查/缓存栅栏不充分。保持私有直到同一 PublicationOperationId 查询证明发布已提交。 |
| CompleteProducerWork | 全部输出已结算且不再有尝试/重放可发布之后；终态尝试/租约、回执、处置/原因/摘要 | ProducerWorkTerminalReceipt 与屏障状态 | 在 D 确认终态回执之前保持屏障开启；摘要冲突是不可变冲突。 |

支撑操作：RegisterProducerClass（类启用与工作准入分离）；CaptureProducerRegistrationHighWater（不可变快照校验，绝不移动截止点）；ResolveProducerWork（按原始 ID/摘要的只读查询）；ReconcileForgetBarrier（D 的仅追加 DRAINED/OPEN/UNKNOWN 检查点；E 提供证据但不自行关闭屏障）。

### 原子性与可见性不变量

1. RegisterProducerWork 与 InstallForgetFence 共享 D 已决定的、可线性化排序：工作被纳入已捕获高水位之内/之下，或在栅栏之后被拒绝/隔离；不存在已准入但未结算的状态。
2. 依赖登记在可见性之前持久且完整。E 本地的溯源边不是 D 依赖回执。
3. PublishDerivedIfFenceCurrent 与权威可见性一同线性化，并与栅栏安装串行化。发布先行则被纳入清单；栅栏先行则拒绝。门回执之后再进行独立、未协调的可见性写入是无效的。
4. I 的当前授权/PermissionEpoch 在最终受保护边界检查；绝不与 ForgetFenceGeneration 做数值比较。
5. Candidate/Staged 输出、溯源、嵌入向量、摘录与边，在最终 PublicationReceipt 与可见性提交之前，对 Runtime/检索/索引/下游保持私有且不可枚举。
6. 任何失败的/未知的栅栏、授权、依赖或发布检查都阻止可见性。

### 精确 OPEN 项

| OPEN ID | 未解决项 | 所有者 |
|---|---|---|
| OPEN-API-01 | 可调用 API/传输 schema、序列化、认证绑定、兼容性与 D 语义错误到线上错误的映射 | D/H/B/I |
| OPEN-STORAGE-01 | 具名 Storage 所有者；事务/CAS/可串行化或已验证的隐藏准备协议；提交后读、故障切换、副本与恢复语义；共享的栅栏到可见性线性化证据 | Storage + D/E |
| OPEN-I-AUTH-01 | 最终门处 I 当前 PermissionEpoch/决策新鲜度与撤销证明 | I + D/E |
| OPEN-REGISTRY-GLOBAL-01 | 将 I ProducerDomainInventoryEpoch/A 清单与 D ProducerRegistryVersion/ProducerRegistrationHighWater 对账；证明封闭世界完整性 | I/A + D/E/H |
| OPEN-RECOMPILE-01 | 重编译所需的关联子项/再准入身份与屏障结算 | D/E |
| OPEN-TEST-01 | 可执行夹具、崩溃/故障切换注入、实际输出与所有者审阅的证据 | D/E/Storage + 消费者 |

这些不重新打开 D 的语义操作字段/错误/线性化；它们属于传输、身份、全局清单、Storage 实现与验证缺口。

### 故障一致性矩阵 —— 仅设计，未运行

| ID | 竞争/故障 | 必需结果 | 状态 |
|---|---|---|---|
| D-RACE-01 | RegisterProducerWork 先于 Fence | 被纳入已捕获高水位之内/之下；屏障保持开启 | NOT RUN |
| D-RACE-02 | Fence 先于 RegisterProducerWork | 被拒绝/隔离；不租用/不解引用/不运行 | NOT RUN |
| D-RACE-03 | 依赖登记与 Fence 竞争 | 依赖先行则被纳入清单；Fence 先行则拒绝；制品保持私有 | NOT RUN |
| D-RACE-04 | 发布与 Fence 竞争 | 发布先行则被纳入清单；Fence 先行则拒绝；无陈旧可见性 | NOT RUN |
| D-FAULT-05 | 登记提交后 ACK 丢失 | 以同一 ID/摘要恢复同一 RegistrationReceipt/序列 | NOT RUN |
| D-FAULT-06 | 栅栏提交后 ACK 丢失 | 恢复同一栅栏代号/高水位；不产生新代号 | NOT RUN |
| D-FAULT-07 | worker 暂停期间租约过期 | 旧租约不能发布/终结；WorkItem 保持开启 | NOT RUN |
| D-FAULT-08 | 队列删除、worker 丢失或 DLQ 停泊 | D 账本仍追踪该 WorkItem；不推断终态 | NOT RUN |
| D-FAULT-09 | 屏障证明之后的迟到派生品 | 抑制/隔离；使证明失效并重开对账 | NOT RUN |
| D-FAULT-10 | 可见性提交崩溃 / 栅栏竞争 | 读者要么看到私有/不存在，要么看到带回执的完全可见；绝不出现部分/陈旧 | NOT RUN |
| E-FAULT-11 | 阶段检查点附近的编译器进程崩溃 | 恢复同一 WorkItem/CompileIntent；按需新 AttemptId；已完成阶段/outbox 幂等 | NOT RUN |
| E-FAULT-12 | 重复/乱序 outbox 重放 | 稳定 ID/摘要去重；无重复副作用，也不跳过游标缺口 | NOT RUN |
| E-FAULT-13 | Forget 之后的 DLQ 重放 | 全新授权/栅栏检查拒绝或隔离；无复活 | NOT RUN |
| E-FAULT-14 | Forget 之后重编译 | 保留祖先血缘；需要关联子项/再准入；被覆盖祖先不能发布 | NOT RUN |
| E-FAULT-15 | 同键/摘要重复 Accepted | 返回原始回执与原始逻辑 ID；无重复登记/编译 | NOT RUN |
| E-FAULT-16 | 丢失登记/依赖/发布/完成 ACK | 以同一稳定 ID/摘要求解；未知则保持私有/屏障开启 | NOT RUN |
| E-FAULT-17 | Forget 之后恢复陈旧快照 | 在服务/索引之前隔离并重放当前控制账本 | NOT RUN |
| E-FAULT-18 | 部分依赖边/不完整血缘 | 无完整依赖回执；制品保持私有 | NOT RUN |
| E-FAULT-19 | 最终门处权限被撤销/未知 | 拒绝/隔离；无可见性 | NOT RUN |
| E-FAULT-20 | 终态摘要冲突 | 保留原始终态记录；审计冲突；不静默覆盖 | NOT RUN |

PASS 需要可执行夹具、具名引擎/配置、确定性交错/崩溃钩子、期望与实际输出、留存证据与所有者签核。本矩阵是计划，不是测试证据。


---

## 第 3.6 阶段 —— 暂存可见性与最终发布门

**状态：** 已定义 E 执行约束契约。D 操作语义从 `03-memory-brain/forget-fence-operation-and-publication-gate.md` 消费；Storage 实现仅为拟议设计。跨所有者事务确认与实现验证仍为 OPEN。

### 1. 私有暂存可见性契约

Candidate、CandidateProposition、ExtractionIR、规范化输出、合并提案、证据/溯源检查点与每个 Staged DerivedArtifactRef/版本，在最终可见性事务提交之前均为**私有**。

私有意味着对下列主体不可用：

- F 索引器、检索、搜索、ANN/图/时序投影与重建/回填消费者；
- G 的上下文激活、成员、排序、预算与投递意图消费者；
- H/Agent 投递及任何外部投递路径；
- 其他 ProducerClass 实例、其他 WorkItemId 与独立编译器运行；
- 公共对象存储列举、通用事件消费者、分析/导出、缓存预热，以及任何未显式限定到所属 E 尝试的查询路径。

只有同一已认证 WorkItemId/AttemptId 执行可为其内部下一步编译读取自己的私有暂存字节，且受当前授权与栅栏检查约束。其他生产者不得把私有候选当作已提交源消费。

暂存记录与 blob 必须在创建时标记为私有/隔离。Outbox 消息只能宣告"存在私有工作"；在发布之前不得携带可供消费者动作的制品引用。最终门之前不得发出任何可索引/公开 URI、公共对象 ACL、可查询行、已提交投影事件或缓存填充。

### 2. 数据库提交与 Artifact Visible 的区别

暂存字节、元数据、依赖边、门决策或 outbox 意图写入成功，**并不**意味着 Artifact Visible。

`ArtifactVisible = true` 仅在权威可见性提交已原子校验当前 D 栅栏、当前 I 授权、活动生产者工作/尝试/租约、完整依赖登记与精确制品/版本身份，并提交可见性标记/记录之后成立。读者与消费者必须按该已提交可见性状态过滤；存储列举、暂存存在性、回执存在性或较早的门响应都不充分。

成功的原子事务可在其提交瞬间使制品可见。若事务 ACK 丢失，制品状态对 E 为 UNKNOWN，并在同一 PublicationOperationId 解析为已提交 PublicationReceipt 之前保持不可消费。实现不得基于未提交的准备或歧义的协调器状态暴露制品。

### 3. 最终发布门输入与不变量

E 以如下内容调用 D 的语义操作 `PublishDerivedIfFenceCurrent`：

- 稳定 PublicationOperationId 与规范请求摘要；
- ProducerClassId + ProducerRegistryVersion；
- 稳定 WorkItemId + D RegistrationReceipt；
- 当前 AttemptId + LeaseId + 租约 epoch/到期时间；
- 精确源 EventRef、MemoryRef 与源 MemoryVersionRef；
- 精确 ScopeRef/安全域绑定；
- 完整血缘摘要与全部直接/传递依赖回执 ID；
- DerivedArtifactRef + 不可变制品版本 + 私有暂存对象/版本引用；
- 观测到的 ForgetFenceCursor/FenceGeneration；
- 当前 I PermissionEpoch 与权威授权决策引用；
- 当同一编译操作同时提出规范写入时所需的任何 D CanonicalCommitReceipt/操作引用。

D 与 Storage 必须在最终串行化边界执行以下全部要求：

1. **栅栏代号检查：** 校验最新适用 ForgetFenceCursor 与每条源祖先/目标血缘。陈旧的观测代号或任何覆盖祖先的栅栏都会拒绝或隔离该派生品。
2. **PermissionEpoch 检查：** 按 I 的语义校验当前 I 授权与 PermissionEpoch。陈旧/被撤销/未知决策即拒绝。绝不把 PermissionEpoch 与 FenceGeneration 做数值比较。
3. **生产者工作校验：** 验证 WorkItemId 登记/摘要/类别、非终态状态、当前 AttemptId/LeaseId/租约 epoch，且无被取代/过期的 worker。重试不创建新的 WorkItemId。
4. **依赖登记校验：** 验证全部必需的直接与传递依赖边已作为一个完整的制品/版本集合持久登记，且血缘摘要、ScopeRefs 与源修订匹配。部分、缺失、冲突或 UNKNOWN 回执即拒绝。
5. **规范提交 / 派生制品提交：** 若规范 Memory 变更属于同一逻辑发布的一部分，其 D 规范 CAS/提交回执与派生制品可见性提交必须在同一串行化决策下协调。两类证据保持彼此不同。不得从派生发布回执推断规范提交回执，反之亦然。
6. **可见性切换：** 在执行检查 1–5 的同一原子事务/可线性化提交中，提交权威可见标记与 PublicationReceipt。不得把任何中间"门已批准"状态当作可见性许可消费。

最终操作必须与并发的 D InstallForgetFence 串行化。只有两种结果合法：发布先提交并被纳入持久栅栏前依赖/目标清单；或栅栏先提交而发布被拒绝。若顺序无法证明，结果为 UNKNOWN 且制品保持私有。

### 4. Storage 操作映射与必需的物理边界

| 逻辑操作 | D 语义所有者/操作 | Storage 职责 | E 行为 |
|---|---|---|---|
| 生产者类准入 | RegisterProducerClass | 持久带版本类登记册与启用/禁用状态 | 在解析到已启用回执之前不工作 |
| 生产者工作准入 | RegisterProducerWork | 栅栏串行化域内的原子工作行 + 摘要 + 登记序列 | 在持久回执之前不入队/不租用/不运行 |
| 栅栏安装 | InstallForgetFence + 不可变 BarrierSnapshotReceipt | 一并提交生效栅栏 + ProducerRegistryVersion + ProducerRegistrationHighWater | 对账同一栅栏/回执；无本地截止点 |
| 依赖登记 | RegisterDerivedDependency | 原子完整制品 + 全部必需边，或隐藏准备/定稿协议 | 部分/未知保持私有 |
| 最终发布 | PublishDerivedIfFenceCurrent | 原子校验 + 可见性标记 + PublicationReceipt/提交身份 | 在已提交回执解析之前无可见性 |
| 终态工作 | CompleteProducerWork | 在全部输出/尝试/重放解决之后持久终态记录 | 本地终态关闭之前需要 D 回执 |
| 未知结果恢复 | ResolveProducerWork / ReconcileForgetBarrier | 持久幂等查询与一致快照读 | 复用原始 ID/摘要；UNKNOWN 时失败关闭 |

**首选实现：** 每个 Canonical Memory 权威一个持久事务/可串行化协调器，覆盖 D 的权威栅栏/生产者账本与权威制品可见性存储。同一串行化域必须为 RegisterProducerWork、InstallForgetFence、RegisterDerivedDependency、PublishDerivedIfFenceCurrent 与 CompleteProducerWork 排序。最终可见性标记在该域中提交。

**分离存储替代方案：** 禁止"先由 D 签发普通令牌、随后由 E/对象存储独立写入"。只有在 D 与 Storage 明确批准持久准备/提交协议或等效可线性化协调器时才可接受，且须满足：(a) 持久隐藏准备；(b) 准备绑定 WorkItemId、AttemptId/LeaseId、依赖摘要、栅栏代号与 PermissionEpoch 决策；(c) 栅栏安装与最终提交串行化；(d) 最终可见性 CAS/提交在其自身提交点重校验当前栅栏与权限；(e) 幂等的参与者/协调器恢复；(f) 已准备/歧义制品在每条读路径上不可见；(g) 栅栏推进后不得重放陈旧提交令牌。若这些性质无法证明，则失败关闭且不发布。

### 5. 规范提交与派生提交的关系

CanonicalCommitReceipt 与派生 PublicationReceipt 是两个独立事实。当编译器输出既改变规范 Memory 又发布派生品时，该操作必须有一个 D/Storage 串行化决策，把规范提交与派生可见性相对 ForgetFence 安装原子排序。若二者无法原子提交，则已批准的协调器必须保证：在规范提交结果持久之前，任何派生制品都不可见；且当栅栏在竞争中胜出时，按 D 的操作语义同时阻止迟到的规范变更与派生发布。混合规范/派生操作的精确全有或全无策略需要 D/Storage 显式确认；E 不自行发明。

### 6. 失败与恢复不变量

- 登记/依赖/发布 ACK 丢失：通过 D ResolveProducerWork 以同一稳定操作 ID + 摘要查询；UNKNOWN 保持私有且屏障开启。
- worker 崩溃/租约过期：撤销旧尝试的发布能力；同一 WorkItemId，仅在当前授权/栅栏检查之后才创建新 AttemptId/LeaseId。
- 重复 AttemptId/Lease：拒绝陈旧或冲突所有者；绝不允许两次尝试发布同一不可变制品版本。
- DLQ/outbox 重放：重放同一语义操作时使用同一 WorkItemId 与操作 ID；只有新的执行才用新 AttemptId。重编译使用新 DerivationRunId 与不可变制品版本，WorkItemId 不变。
- 依赖登记部分完成：以同一 DependencyRegistrationId/摘要幂等重试；任何部分边集合都不可发布。
- 部分提交恢复：检查权威事务/协调器记录。若最终可见性提交存在，返回原始 PublicationReceipt；若已证明中止，则在全新授权/栅栏下重试同一逻辑操作；若结果未知，保持私有并对账。
- 恢复：隔离所有暂存与可见投影物化；在任何内容被服务之前重放当前 D 栅栏与 I 权限/撤销控制状态。

### 7. 明确不作的声明

本文档不构成下列存在的证据：D 可调用端点、Storage 事务/CAS、分布式协调器、outbox、租约栅栏、对象存储 ACL 执行约束、索引门控或故障恢复。Storage 的拟议报告仅为设计证据。不声称任何竞争/故障测试通过。
