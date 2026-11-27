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
    canonical_scope: "E 域 Memory Compiler 记录 module-baseline-and-redlines.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-module-baseline-and-redlines"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - module-baseline-and-redlines
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# E 模块基线与红线 —— Memory Compiler

**提案 ID：** DEF-G0-E-001  
**Owner：** E —— Memory Compiler 架构负责人  
**状态：** PROPOSED —— 需要 Owner 审查  
**版本：** 0.1.0  
**分支：** `session-e-memory-compiler-2026-11-16`  
**权限：** E 拥有编译器生命周期与执行约束。D、I 与 Storage 各自保留其权限。

## 1. 模块使命

E 将持久化接受的源 Event 与已登记的源材料转化为可追溯的候选 Memory/Claim/Entity/Relation 资产，并协调其向规范权威与下游投影发布的受控交接。E 是一条可恢复的语义变换流水线，而不是规范数据库写入方、权限权威或索引/运行时所有者。被接受的输入在模型不可用的情况下仍独立保持持久；编译可能产出"无候选""转人工审查""延期""拒绝"或"死信"等结果。

## 2. 所有权基线

E 拥有：
- CompilerWorkItem、CompileIntent、DerivationRun、Attempt、Lease 及阶段生命周期。
- 持久化阶段回执、确定性规范化，以及模型辅助抽取的编排。
- CandidateEnvelope／前规范化中间表示、Evidence/Provenance 草案，以及冲突/修订提案。
- 重试调度器、DLQ、重放/重编译策略与编译器本地恢复。
- 不可变派生制品的私有暂存与冻结输出清单。
- 对下列前提的执行约束：D 登记、依赖登记、当前 I 授权/PermissionEpoch、当前 D ForgetFence，以及 Storage 最终可见性门，均为发布的前置条件。
- 编译器侧的持久回执与终态结果对账。

E 不拥有 Canonical Memory 的 schema/修订/提交、D 的 ProducerRegistration 账本/屏障、D 的 ForgetOperation/Fence、I 的 PermissionEpoch/授权、Storage 的物理原子可见性、F 的索引/IndexWatermark/缓存/检索、G 的 ContextVersion，或 H 的线上协议 schema。

## 3. 能力基线

1. 持久化的接受入站回执，以及与编译器/模型可用性无关的稳定 CompileIntent。
2. 幂等、带版本的确定性规范化，以及可选的、有界的模型辅助抽取。
3. 候选与证据/溯源血缘可追溯到不可变的源身份。
4. 通过事务性 outbox 或等效的可恢复日志，实现持久的阶段结果/下一阶段调度。
5. 跨重试保持稳定的逻辑工作身份；每次尝试/租约使用新的 AttemptId/LeaseId；重编译使用新的 DerivationRunId。
6. 在入队、获取租约、解引用受保护源或执行之前完成 D 的 ProducerWorkItem 登记。
7. 不可变的私有暂存；在最终门之前不提供查询、基于列举的暴露或消费者访问。
8. 在发布前完成全部直接/传递依赖登记。
9. 在每次受保护读取与最终门处，重新校验 I 的 PermissionEpoch/授权与 D 的 ForgetFence。
10. 在 E 记录 Published/终态成功之前，回读 Storage 的 PublicationReceipt。
11. 重放、DLQ 与恢复保留原始血缘，且不得绕过 D 的屏障或当前栅栏。

流水线拓扑、模型路由、队列预算与可调用传输绑定，在尚未由 Owner 决策固定的地方，仍为候选/TO_VALIDATE 状态。

## 4. 领域所有权

| 实体 | 所有者 | E 的规则 |
|---|---|---|
| CompilerWorkItem / CompileIntent | E | 稳定的逻辑工作身份 |
| DerivationRunId | E | 重编译时新建；关联先前运行与原始源 |
| AttemptId / LeaseId | E | 每次尝试/租约新建；权限仅限于执行栅栏 |
| StageReceipt | E | 不可变的输入/输出摘要、阶段/版本与结果 |
| CandidateEnvelope | E | 前规范化 IR；不是 D 的 schema 或规范对象 |
| Evidence/Provenance 草案 | E 产出；按 D/B 契约进行规范接受 | 绝不虚构血缘或证据 |
| ProducerClass 登记 / ProducerWork 登记 | D 的权限；E 请求/消费 | 未取得 D 回执前不得执行 |
| 依赖登记 | D 的权限；E 请求/消费 | 全部必需边在门之前持久化 |
| ForgetFenceCursor | D | E 存储/消费不透明的当前令牌 |
| PermissionEpoch / 授权 | I | E 重新校验；绝不铸造或比较 epoch |
| PublicationOperationId / PublicationReceipt | 在跨所有者协议下由 Storage 拥有的操作/回执；E 维护请求/对账状态 | 仅在匹配到持久 Storage 回执后才视为 Published |
| CanonicalCommitCursor / AggregateRevision | D | E 消费精确的 D 结果 |
| IndexWatermark | F | E 仅发出发布请求/事件 |
| ContextVersion | G | E 不得变更 |

## 5. 接口基线

### 5.1 入站与身份

"被接受（Accepted）"仅指持久化保管/入站。它不等于 Processed、Compiled、CanonicalCommitted、Published 或 Indexed。EventRef 不可变。AcceptedReceiptId 与 CompileIntentId 保持稳定。ProducerWorkItemId 在同一个逻辑工作项的各次重试之间保持稳定；AttemptId/LeaseId 每次执行都会变化。重编译会创建新的 DerivationRunId，并重新做授权/栅栏检查。关于重编译时是新建 ProducerWorkItemId 还是登记子项，D 的精确策略仍为 OPEN，E 不得自行发明。

### 5.2 生产者准入与屏障

E 必须在入队、获取租约、解引用源或执行之前，取得持久的 D Producer Registration Receipt。若请求 ACK 丢失，E 以相同的 ProducerWorkItemId + 摘要重新求解；结果为 UNKNOWN 时阻止执行。队列状态、租约、重试次数、DLQ、worker 替换或运维重放，都不会移除 D 登记。租约过期仅使该租约失效，不终止工作，也不释放屏障。D 仍是类/工作账本、登记高水位、栅栏截止与屏障关闭的权威。

生产者类别的声明与逐个工作的准入是两件事。D 精确的类别登记操作/版本语义仍为 OPEN（OPEN-D-CLASS-01）。E 不得发明 D 的 API，也不得运行未登记的生产者路径。

### 5.3 阶段、抽取与溯源

确定性校验、解码、结构规范化、时间戳保留、范围检查、证据定位符校验与溯源构造，均不得依赖 LLM。模型辅助的分类/抽取是可选的、有界的、带版本的，并且其输出按不可信提案处理。模型输出不得授予权限、改变 Scope、虚构血缘、决定规范身份或裁决冲突。在 B/D 决策确定 Fact/Claim 映射与规范 schema 之前，CandidateProposition 仍属前规范化状态。

每个阶段回执绑定输入/输出摘要、阶段与流水线版本、确定性/模型辅助模式、适用时的方法/模型配置、尝试、权限/栅栏观测值与结果。原始受保护载荷不进入常规日志。

### 5.4 私有暂存与依赖登记

StagedPrivate 不可变且不可查询。对象存储路径、列举、带签名的暂存 URL、队列成员身份、outbox 事件、编译器本地状态或持有某个制品引用，都不得暴露字节内容。E 冻结完整输出清单与血缘，为所有直接/传递源与制品请求 D 的依赖登记，并等待持久回执。依赖登记部分完成或状态未知时，所有受影响的制品都保持私有。

### 5.5 最终发布门

在最终门之前，E 重新校验：当前 I 授权/PermissionEpoch、每个源祖先与目标的当前 D ForgetFence、当前工作/尝试/租约栅栏、完整依赖集合与冻结清单、范围，以及 I 要求的任何清单封存（inventory seal）。实际的可见性切换必须与 D 的栅栏/生产者/依赖操作，以及 I 的 owner-final-gate 排序协议串行化。禁止"先做本地检查、再独立写入"。

JF-10 v2 的 owner 侧设计规定了：已准备的 Storage 参与者/XID、D/Storage 按权威共享的串行化、I 的排序器决策，以及 Storage 同 XID 的提交/回滚。I COMMIT 不是发布。只有原子的 Storage VisibilityPointer + PublicationReceipt + owner 结果 + 回执消费证据 + outbox 提交，并且随后完成权威回执回读，才允许 E 记录 Published。Storage 必须先证明真实数据库的支持能力，之后才能将其视为可实现。

### 5.6 游标语义

E 将 D 的 CanonicalCommitCursor 与 LifecycleEventCursor 作为两个独立的类型化值消费，保留精确引用，绝不铸造它们。F 拥有 IndexWatermark，且仅在连续规范前缀结算之后推进。ForgetFenceCursor 由 D 拥有，且独立于 CanonicalCommitCursor、LifecycleEventCursor、IndexWatermark 与 I PermissionEpoch。E 不得比较不透明游标的值，也不得把一个当作另一个使用。

## 6. 安全基线

- 在解引用受保护源、抽取、实体检索、合并、重放、规范写入请求与发布之前，先解析范围与权限。
- 在 worker 准入、租约、受保护读取、重试/重放与最终门处，重新校验当前授权与 PermissionEpoch。
- 在准入时、昂贵工作完成后、以及紧邻可见性切换之前，重新校验 D ForgetFence 与完整的源/祖先血缘。
- 将源载荷与模型输出视为不可信数据；它们不得修改策略、工具、Scope 或编译器配置。
- 缓存/暂存键绑定范围、环境、参与者类别、策略/撤销 epoch 与源版本；私有暂存不是读取面。
- 对缺失、过期、歧义或不可用的 I/D/Storage 证据一律失败关闭（fail closed）。
- 不在常规遥测中记录被遗忘的明文、原始敏感摘录、提示词或凭据。

## 7. 模块红线

1. StagedPrivate 永不查询可见，也不对消费者可见。
2. Accepted、Registered、Queued、Leased、Running、Staged、DependencyRegistered、I COMMIT_WON 与 E 本地的 Published 意图，彼此不可互换。
3. 重试、租约过期、DLQ、重放、重编译或 worker 替换，都不得绕过原始 D 生产者屏障，也不得创建未登记的旁路。
4. 每次重试/重放/重编译都重新检查当前 I PermissionEpoch 与 D ForgetFence；陈旧的尝试不能通过把较新的令牌复制到陈旧输出上而获得正当性。
5. 依赖登记必须在可见性之前完成；部分登记不可发布。
6. 最终门必须在串行化协议中重新检查精确血缘与最新栅栏，而不是"检查后写入"的序列。
7. E 不得铸造 CanonicalCommitCursor、规范修订、ForgetFenceCursor、ProducerRegistrationReceipt 或 IndexWatermark。
8. E 不得决定规范提交、权限、全局 Forget 完成、索引新鲜度或 Context 变更。
9. 仅 I COMMIT_WON 从不等于 Published；Storage 参与者提交与回执回读是强制要求。
10. 参与者未知/存疑、回执缺失、副本陈旧、超时或 ACK 丢失，都不等于成功，也不等于安全中止。
11. 在 Storage 识别并验证实际引擎/配置与崩溃/恢复行为之前，不得声称任何具体的 DB/XA/prepared-XID 能力。

## 8. 禁止的跨模块操作

- D：E 可以提交候选与规范写入请求，但不得选择 D 的规范 schema、修订、提交游标、生命周期或 Forget 状态。
- F：E 可以发出规范提交/投影通知，但不得写入索引投影、对检索排序、变更缓存/工作集或推进 IndexWatermark。
- G：E 可以发出生命周期/变更通知，但不得变更 Context 或 ContextVersion。
- I：E 消费授权/PermissionEpoch 与策略决策；不得铸造、重新解释或覆盖它们。
- Storage：E 负责暂存并请求发布；不得代替 Storage 宣称物理可见性已原子化，或恢复已准备的 XID。
- H：E 消费已认证的入站身份/信封；不得重新定义 BMCP 线上协议或 Adapter 行为。

## 9. 依赖契约

| 依赖 | 提供方 | 必需契约 | 当前状态 |
|---|---|---|---|
| 规范 schema/提交/游标/栅栏/生产者账本 | D | 类型化规范写入、持久的生产者/依赖回执、最终栅栏门 | D 语义已 DECIDED；可调用 API/原子化实现 OPEN |
| 权限/PermissionEpoch/撤销 | I | 当前决策与精确的受保护操作绑定 | 归 I 策略所有；实现 NOT VERIFIED |
| 持久可见性 / 已准备参与者 | Storage | 同 XID 准备/恢复、原子指针+回执+outbox、恢复证明 | 数据库引擎 NOT SELECTED / NOT VERIFIED |
| 入站身份/线上协议 | H | 已认证的 ProducerIdentity、稳定幂等与范围绑定 | 归 H 所有；精确 schema 接受另议 |
| 类型化领域引用 / Fact-Claim 映射 | B | 候选到规范的映射与引用类型 | Fact/Claim ADR OPEN |
| 运行时/索引消费 | F | 规范事件与感知栅栏的发布、独立的 IndexWatermark | 需要消费者契约 |
| Context 失效 | G | 类型化生命周期/遗忘事件；G 拥有 Context | 需要消费者契约 |
| I 清单封存 | I | 策略要求时的当前 epoch/seal | 治理/实现 OPEN |

## 10. 一致性要求

下列用例在另行链接可执行证据之前，均为 SPECIFIED / NOT RUN：
- 接受回执在编译器/模型中断与重启后仍然存在。
- 重复的入站/阶段派发是幂等的；同键不同摘要构成冲突。
- 在源解引用与候选生成之前，范围/权限即被拒绝。
- D 生产者登记发生在入队/租约/运行之前；登记未知则阻止执行。
- 栅栏与登记的竞争只有一个串行化结果。
- 队列待处理、已租用、已过期、重试、DLQ 与重放，都仍处于 D 屏障之内。
- PermissionEpoch 或 ForgetFence 变更之后的重试/重放被拒绝，或从安全点重启。
- 任何消费者都无法读取/列举/索引查询 StagedPrivate。
- 依赖登记 ACK 丢失时按稳定键求解；部分登记保持私有。
- 暂存与最终门之间栅栏或权限推进时，发布被拒绝。
- Storage 准备/栅栏竞争只有两种合法顺序；未知时保持私有/存疑。
- 同 XID 提交/回滚在进程重启/故障切换与 ACK 丢失下仍然成立。
- 仅有 I COMMIT_WON 而无 Storage 参与者提交时，不暴露任何字节。
- 原子的 VisibilityPointer/PublicationReceipt/结果/回执消费/outbox 事务是全有或全无。
- 恢复/重建/重放不得复活已被栅栏隔离的源派生品。
- 候选到规范的映射遵守 B/D 已批准的 schema，且不预设 Fact/Claim 决策。

## 11. 验收标准

E 的 G0 提案仅在下列条件全部满足时才可接受：
1. 全部 14 个必需章节齐备，且 owner 边界明确。
2. 工作/尝试/运行/租约身份与 D 准入语义，与 D 当前分支契约一致。
3. 私有暂存、依赖登记与最终门可阻止发布前的可见性。
4. 重试/重放不得绕过 D Producer Barrier 或当前 I/D 检查。
5. JF-10 v2 仅被描述为架构协议，并保留精确的例外与 NOT VERIFIED/NOT RUN 状态。
6. 各游标领域保持彼此独立。
7. E Owner 审查并显式接受某个精确版本；本提案自身仍为 PROPOSED。

## 12. 变更权限

仅 E 可变更编译器内部的工作生命周期、抽取、规范化、阶段日志、尝试/租约/重试/DLQ/重放与候选 IR。仅 D 可变更规范领域、Producer Registration 账本/屏障、ForgetFence 与规范发布权限。仅 I 可变更权限/撤销/全局 Forget 策略。仅 Storage 可认证数据库/已准备 XID/可见性实现。B 拥有领域类型化与 Fact/Claim 决策；F/G/H 拥有各自的消费者/运行时/线上协议领域。跨所有者变更需要受影响 Owner 给出精确版本决策。

## 13. 未决事项

- OPEN-D-CLASS-01：D 的 ProducerClass 登记操作与版本迁移语义。
- OPEN-D-WORK-02：在规范 MemoryRef 存在之前，仅凭 EventRef 的入站准入。
- OPEN-D-RECOMPILE-03：重编译时沿用同一 ProducerWorkItemId，还是登记子项；原始血缘/屏障始终保留。
- OPEN-D-GATE-04：最终发布门与 Storage 可见性切换所需的精确 D API/线性化绑定。
- Storage 的具体数据库引擎/版本、隔离级别、prepared-XID/锁保留、同 XID 恢复、故障切换与备份/恢复。
- I 的 InventorySeal 权威/签名方/验证方/epoch 生命周期与治理。
- B 的 Fact/Claim ADR、Claim 身份/修订、Provenance 循环策略。
- F/G 的消费者契约与事件重放/保留语义。
- 模型路由、吞吐、显存/资源预算与队列配额仍为 TO_VALIDATE。

## 14. 明确不作的声明

本提案不声称：编译器生产实现、D API 可用、D/E/Storage 原子登记、私有暂存隔离认证、最终发布门实现、已选定数据库、prepared-XID 持久性、同 XID 崩溃恢复、I 排序器实现、InventorySeal 治理、测试通过、Global Forget 完成或生产激活。JF-10 P0 仍为 OPEN；多策略域原子性仍为 BLOCKED / NOT ACCEPTED。JF-10 v2 文档是枚举了各 owner 依赖的架构协议，不是实现证据。

## 证据

- E 分支起始 HEAD：`530645a08b55716257cf4cde20b0900b628abb52`
- `04-memory-compiler/compiler-overview.md` Blob：`35a766fae29c0b8ddf692a6ec062762f0fca29d2`
- `04-memory-compiler/compiler-state-and-producer-admission.md` Blob：`e59f517fff161ab882aa0ddc4a5bda513964ae1a`
- `04-memory-compiler/forget-fence-and-derived-registration.md` Blob：`00e37ba56596e710513c8d0568acd79141d9101b`
- `04-memory-compiler/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` Blob：`94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- D 的精确 JF-10 v2 决策：D 分支 HEAD `1460fbd17ee38ea4044dc6c75cfe49039c7fc585`；D 接受了单 I-PolicyDomain、D 拥有的语义，仅含枚举例外。
