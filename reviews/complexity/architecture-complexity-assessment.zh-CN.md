# 架构复杂度评估与预算 / Architecture Complexity Assessment and Budget（中文）

- 评估角色：X — 首席架构复杂度评估负责人
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 精确基线：`main@b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- assessor: X — 首席架构复杂度评估负责人（历史来源；原始会话身份未记录）
- assessed_version: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- evidence_baseline: `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001`（源报告记载的历史基线；不声称存在同期会话签名）
- 评估日期：2026-11-17
- 类型：基于可读取仓库证据的静态架构复杂度评估
- 状态：**PROVISIONAL — NOT PROVEN**
- 范围限制：本报告不批准架构、不替代 Owner 决策、不证明实现/性能/安全性，也不代表全部 Owner 分支已完整审查。

## 0. 执行结论

**结论：当前架构复杂度是否处于可实现、可验证、可维护范围内？NOT PROVEN。**

原因不是模块数多，而是跨模块状态和证明语义尚未形成一个可完整验证的闭环：Forget 同时依赖 D 的 canonical fence / producer barrier、E 的 Admission / derived registration / publication gate、F 的 index watermark 与 in-flight recall、G 的 Context version / delivery、H 的 Adapter Applied / clear acknowledgement、I 的 authorization epoch / retention / global completion，以及 Storage/Consistency 的原子持久化和恢复协议。任何单方本地成功都不足以证明全局完成。

现有系统级数据流明确区分 Accepted、Compiler Completion、Canonical Commit、Index Applied、Context Applied 和 Forget completion；这有正确性价值，但也造成大量不同证明对象、状态、游标和跨模块责任。不能将其压缩成一个 Success 状态。另一方面，若每个概念都形成独立服务、独立队列、独立版本号或独立协议，则复杂度将不必要地指数式放大。

**当前评估等级：高复杂度 / 受控性未证明。** 设计可继续收敛，但不应据此启动完整分布式实现或冻结全部契约。

## 1. 证据、边界与方法

### 1.1 直接检查的证据

- Main HEAD：`b372b62c640a2b656e54b6db62a4ee67d7d8c001`。
- Issue #43：System-wide Architecture Consolidation & Feasibility Review，Open。
- PR #28：Draft / Open；其说明明确指出双语覆盖并非全仓完成，C/G/H Applied 与 Storage/Consistency 详细契约仍不完整，ADR-001 blocked，H36 与 C-FR 测试 NOT RUN，JF-10 P0 OPEN / NOT IMPLEMENTED / NOT RUN。
- `01-system-architecture/component-interactions.md` 与 `data-flows.md`：规定了事件接收、异步编译、Canonical authority、索引投影、Recall、Context version/delivery/Applied、Forget 等端到端流程。
- `reviews/integration/phase-2-defg-cross-session-reconciliation.md`：明确 D/E/F/G 的历史分支评审并非独立外部签署；模块设计仍是候选契约，P0/P1 及 H/I 缺失仍阻止契约冻结。
- D Owner 分支文件 `forget-fence-and-completion-contract.md`（Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`）与 `commit-cursor-semantics.md`（Blob `4688a0ca487bf4d853c7f0220408abe8d743d159`）。
- E Owner 分支文件 `forget-fence-and-derived-registration.md`（Blob `00e37ba56596e710513c8d0568acd79141d9101b`）与 `accepted-receipt-and-idempotency-contract.md`（Blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46`）。

Owner 分支文档作为候选设计证据，不视为已集成到 Main、已批准或已实现。若分支路径读取失败，不推断其内容不存在；该维度标为证据不足。

### 1.2 评分定义

每项采用 1–5 级：1 Low，2 Moderate，3 Significant，4 High，5 Extreme。分数描述需要管理和验证的复杂度，不是质量分数、工时、风险概率或成熟度。置信度：高/中/低。未见权威契约时使用暂定评分并降低置信度。

八个维度：
- 内部复杂度：模块自身职责、算法、内部状态。
- 依赖复杂度：外部 Owner、共享契约、依赖扇出。
- 状态复杂度：状态、版本、身份、转换及不变量。
- 并发复杂度：竞争、线性化点、锁/事务、重试和重复投递。
- 恢复复杂度：崩溃窗口、重放、修复、备份恢复。
- 验证复杂度：测试层级、状态空间、故障注入及证据。
- 运维复杂度：部署、监控、升级、恢复与人工操作。
- 认知复杂度：理解、变更传播、Owner 协作和文档维护。

不得将八项简单相加作为项目总分。矩阵用于定位瓶颈；整体结论由关键路径、耦合和证据缺口决定。

## 2. 模块复杂度矩阵

分数顺序：内部 / 依赖 / 状态 / 并发 / 恢复 / 验证 / 运维 / 认知。

| 模块/能力 | 八维评分 | 置信度 | 依据与主要放大因素 |
|---|---:|---|---|
| A 架构治理/集成 | 3/5/4/3/3/5/2/5 | 中 | 多 Owner 权威边界、ADR 阻塞、双语及证据追踪、PR/审查门槛；变更传播面大 |
| B Domain Model | 4/5/5/3/3/5/2/5 | 中 | Fact/Claim、Scope、Principal/Actor、identity 与 revision 是全系统语义根；ADR-001/P0 未闭合导致下游返工 |
| C Agent Integration | 3/5/4/4/3/5/4/4 | 中低 | Agent 请求/推理边界、Adapter、Applied 证明依赖 H/G；C/G/H 契约和测试仍不完整 |
| D Memory Brain | 5/5/5/5/5/5/3/5 | 中高 | Canonical lifecycle、commit cursor、Forget fence、dependency inventory、producer barrier、completion proof |
| E Memory Compiler | 5/5/5/5/5/5/4/5 | 中高 | durable admission、receipt 分层、lease/retry/replay、derived registration、final publication gate；D/Storage 原子登记仍 OPEN |
| F Memory Runtime | 4/5/5/5/4/5/4/4 | 中低 | 多路检索、index watermark、freshness、permission filtering、in-flight recall 与 Forget 竞态；详细契约基线不完整 |
| G Memory Context | 4/5/5/4/4/5/4/4 | 中低 | Context version、ChangeSet、delivery retry、Adapter Applied、reconnect/snapshot/reconcile；Applied 依赖 H/C |
| H BMCP / Adapter protocol | 4/5/5/5/5/5/4/5 | 低 | wire identity、capability、ack stages、boundary receipt、offline/reconnect、clear acknowledgement；当前主分支规范证据不足 |
| I Security / Governance | 4/5/5/5/5/5/4/5 | 低 | principal/permission epoch、revocation、retention、global Forget、backup/external copy、physical erasure；规范证据不足 |
| Storage / Consistency | 5/5/5/5/5/5/5/5 | 低 | 多权威状态原子提交、outbox、fence/registration/publication、恢复、拓扑 ADR blocked；详细契约和拓扑未决 |

评分解释：D/E 具有较直接的 Owner 源文件证据，故置信度相对较高；H/I/Storage 评分是基于被其他模块引用的责任与系统数据流推断，必须由对应 Owner 的规范和技术决策校准。

## 3. 跨模块机制复杂度矩阵

| 跨模块机制 | 八维评分 | 置信度 | 复杂度原因 / 关键阻塞 |
|---|---:|---|---|
| Forget fence → producer admission → derived registration → publication gate | 5/5/5/5/5/5/5/5 | 高 | 登记与最终发布必须防止 fence 竞态；任何局部检查都不能代替权威原子边界；D/E/Storage/I 共同参与 |
| Canonical commit → index watermark → retrieval freshness | 4/5/5/4/4/5/4/4 | 中 | cursor、aggregate revision、partition watermark、coverage/schema version 不可混用；索引只能证明连续应用前缀 |
| Context desired version → delivery → Adapter Applied | 4/5/5/5/4/5/4/5 | 中 | desired/applied 分离、重试幂等、旧 ACK、离线、快照回补、推理边界证明 |
| Authorization/revocation epoch across operations | 4/5/5/5/5/5/4/5 | 低 | 权限可能在异步工作期间撤销；必须定义检查时点、epoch 绑定和失效传播 |
| Global Forget completion and residual evidence | 5/5/5/5/5/5/5/5 | 中低 | canonical、derivatives、indexes、cache、context、adapter、replicas、backups 均可能具有不同完成语义 |
| Durable acceptance / outbox / replay | 4/5/4/5/5/5/4/4 | 中 | Accepted 必须对应可恢复数据与处理意图；重复投递不能产生重复事件或副作用 |
| Cross-owner bilingual contract / version traceability | 3/5/4/2/3/5/2/5 | 中高 | 来源 Blob、翻译对照、decision status、PR manifests 和 Owner authority 同步负担 |

**判断：** Forget 全链路、Publication 与 Applied/Forget 的交叉竞争，比单个模块本身更复杂。应把它们当作系统级协议单独预算，不应把它们藏在 D/E/F/G/H/I 各自的局部评分中。

## 4. 状态空间与组合爆炸

### 4.1 不能混为一谈的证明对象

至少需要区分：
1. AcceptedReceipt：事件及处理意图可持久恢复。
2. ProducerRegistrationReceipt：生产者工作已进入 D 的 barrier inventory。
3. CompilerCompletionReceipt：一次编译执行有持久终态。
4. DerivedRegistrationReceipt：派生物 lineage 已登记。
5. CanonicalCommitReceipt：Canonical 变更已提交。
6. IndexWatermark：指定索引分区已连续应用至某个 canonical cursor。
7. Context desired version / delivery state。
8. Adapter Applied acknowledgement：指定 Context 版本在约定推理组装边界生效。
9. Forget target acknowledgement / global completion proof：适用目标按 I 的策略完成或留下批准的 residual。

这些对象证明不同事实，不可合并为单一 Success，也不能通过一个模块的成功推断其他对象已成立。

### 4.2 组合放大因子

- 每个状态机都与权限 epoch、scope、版本/游标、重试次数、持久化结果和故障窗口相交。
- 多个独立时钟/序列（CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor、IndexWatermark、ForgetFenceCursor、ContextVersion、PermissionEpoch）若缺乏明确的比较域，会产生错误比较和隐性耦合。
- 对每个状态再叠加在线/离线、可重试/终态、成功/拒绝/部分完成，会形成乘法式测试空间。
- 若为每个 Owner 再复制一套状态、receipt、retry 和审计协议，维护负担会再次放大。

### 4.3 可控的状态约束

架构阶段必须规定：
- 每个 ID、cursor、revision、epoch 的唯一 owner、作用域、单调性和比较规则。
- 每个状态机唯一权威写入方；消费者只保存明确标记为投影/缓存/观察值的副本。
- 状态转换表必须包含前置条件、持久化点、幂等键、失败结果、重试策略和恢复动作。
- 证明对象必须说明 issuer、subject、scope、generation/version、durability、freshness 和“不能证明什么”。
- 任何 stale/unknown/ambiguous 情况都必须有 fail-closed 行为，且不得伪造完成状态。

## 5. 并发与恢复复杂度分析

### 5.1 关键竞争窗口

| 竞争 | 必须证明的安全属性 | 复杂度等级 |
|---|---|---|
| Forget fence 与新 Producer Admission | fence 建立后不能接纳未被 barrier 覆盖的旧世代工作 | Extreme |
| Producer registration 与 fence/barrier seal | 不得出现“未登记但可发布”的生产者窗口 | Extreme |
| Derived publication 与 Forget | 最终发布必须与 fence/权限检查在权威持久化边界协调 | Extreme |
| In-flight Recall 与 Forget | fence 后不得返回已被抑制的候选；响应最终化需定义线性化点 | High |
| Canonical commit 与 index apply | watermark 只推进连续前缀，不越过缺口 | High |
| Context delivery 与新版本/Forget | 旧 delivery/ACK 不得回滚较新版本或重新引入被移除内容 | High |
| Permission revocation 与异步 worker | worker 不得凭过期授权完成敏感副作用 | Extreme |
| Crash 与 partial cleanup | 重放单调、幂等；不得把部分完成误报全局完成 | Extreme |

### 5.2 恢复必须是设计的一部分

至少为以下崩溃点定义可恢复行为：durable accept 后未 enqueue；compiler 完成后未登记 lineage；登记后未 final publish；canonical commit 后 index 未更新；Context commit 后未 delivery；Adapter 已应用但 ACK 丢失；Forget fence 后部分目标清理；backup restore 引入旧数据；恢复后旧 worker/消息重新出现。

恢复证据必须证明 generation/fence 仍有效、已完成目标不会倒退、重复执行安全、旧快照不会覆盖新权威状态。当前文档材料不足以证明这些窗口均已闭合，因此 Recovery Complexity 评估为高且可控性 NOT PROVEN。

## 6. 复杂度热点、放大器与瓶颈

### Hotspots
- H1：D/E/Storage 的 producer registration + publication gate。
- H2：I/D/F/G/H/Storage 的 Global Forget 端到端完成。
- H3：C/G/H 的 Applied 证明与推理边界。
- H4：D/F 的 Canonical cursor 与 IndexWatermark。
- H5：B 的 Fact/Claim、Scope、Principal/Actor 基础语义。
- H6：Storage topology、事务/日志/outbox 和 recovery。
- H7：全仓双语规范、Owner Blob 精确绑定、状态同步和 PR 审查。

### Complexity Multipliers
- 同一事实由多个 Owner 以不同名称、状态或 receipt 重复表达。
- 把逻辑边界误实现成独立进程/服务/数据库/队列。
- 对每个模块独立定义 retry、idempotency、audit、version 和 reconciliation 框架。
- 同时支持多个存储拓扑、多个索引后端、多个部署模式，却没有可验证需求。
- 在基础身份/Scope/Fact-Claim ADR 未决时冻结下游 Schema。
- 把文档覆盖率、结构 CI 或模拟多角色评审误当成语义一致性和系统可行性证明。

### Bottlenecks
- B/ADR 的基础语义未决，会传播到 D/E/F/G/H/I。
- Storage 原子边界未定，使 D/E 最关键的发布正确性无法证明。
- H Applied 与 I Forget/retention 规范未闭合，使 G/C 和全局完成无法验收。
- 端到端状态空间测试与故障注入证据缺失。

## 7. 复杂度预算与阈值

以下为 X 建议的治理阈值，不是当前项目已批准的 SLA 或 Owner 决策。

### 7.1 模块预算

- 每个模块只能有一个权威写入方；投影/缓存不得成为隐性第二权威。
- 每个模块最多维护一个主要持久化状态机作为首选预算；额外状态机必须说明独立故障域/独立正确性收益。
- 每个 ID/cursor/version/epoch 必须有唯一语义定义和比较规则；禁止同名异义或跨域比较。
- 每个跨模块工作流应有一个可追踪 operation ID、一个明确的全局状态 owner，以及有限、枚举的参与者集合。
- 新增独立服务、数据库、消息系统或协议必须证明模块化单体/现有基础设施无法满足需求。

### 7.2 测试预算

最低测试层级：
1. 单元：本地状态转换、纯规则、边界值。
2. 组件：持久化与本地事务、幂等、outbox、投影。
3. 契约：Owner 间 schema/receipt/状态语义。
4. 状态空间：合法/非法转换、重复、乱序、过期、部分成功。
5. 并发：线性化点附近的竞态与并发 admission/publication/forget。
6. 故障注入：每个 durable boundary 前后崩溃、超时、网络分区、ACK 丢失。
7. 恢复：重放、checkpoint、backup/restore、旧 worker/消息。
8. E2E：接受→编译→canonical→索引→recall→context→Applied；另有完整 Forget 端到端链路。

**阈值：** 每个 P0/P1 不变量至少有一个直接失败测试；每个 durable boundary 至少有 crash-before/crash-after 测试；每个跨模块状态机至少有重复、乱序、重试、部分失败和恢复用例。关键安全不变量不得仅依赖 happy-path E2E。

### 7.3 运维预算

第一阶段建议单一可部署模块化单体、单一权威数据库、一个可恢复任务/outbox 机制；索引可作为可重建投影。必须具备 operation/correlation ID、队列年龄、重试/DLQ、watermark lag、fence generation、reconciliation backlog、Applied lag、Forget residual、backup/restore 结果等监控。

不建议首阶段引入多数据库分片、跨地域 active-active、独立微服务网格或多个消息总线。除非有经测量的吞吐、隔离、可用性或法规需求，否则其运维成本没有证据支持。

### 7.4 认知预算

- 一份术语表作为唯一术语入口。
- 一个跨模块协议登记表，记录 owner、状态、线性化点、证明对象和消费者。
- 一份全局状态/游标注册表，禁止散落重复定义。
- 每项架构决策只在权威 Owner 文件定义；其他模块引用稳定 ID，不复制完整语义。
- 双语文档应由同一变更集同步维护；覆盖登记必须区分源规范、阅读指南、翻译副本和批准状态。

## 8. 简化建议与分类

### 必须保留（Correctness-required）
- Canonical authority 与派生投影分离。
- Accepted、Canonical Commit、Index Applied、Context Applied、Forget complete 等证明语义分离。
- Forget fence、producer barrier、derived dependency registration、最终 publication gate。
- Scope/Principal/Permission 与 revocation epoch 的边界校验。
- 幂等、持久化工作意图、可恢复重放、stale generation 拒绝。
- Index watermark 连续前缀语义及 Applied 的确切 Adapter 边界证明。
- 对 backup/replica/external copy 的明确 Forget 策略。

### 可以简化（Simplify）
- 以模块化单体部署所有逻辑 Owner；先用模块接口和事务边界隔离，不以网络服务隔离。
- 共享一个通用 durable work/outbox/lease/retry 框架，允许领域状态不同，但不重复实现调度与重试基础设施。
- 使用一个明确的跨模块 operation envelope/correlation 方案；只在需要时增加专属字段。
- 第一阶段采用少量明确索引类型；不为每个检索策略引入独立服务。
- 将可重建索引、缓存、working set 作为投影处理，不复制 canonical lifecycle。
- 使用枚举化状态转换表替代散文中重复叙述同一状态机。

### 可以延后（Defer）
- 微服务拆分、跨地域 active-active、复杂多租户物理隔离。
- 多种可插拔向量/图/搜索后端同时运行。
- 自适应/自动调参的复杂检索融合与学习型策略。
- 高级多级 checkpoint、复杂 compaction 和多代备份优化（但基础 backup/restore 与 Forget 约束不能延后）。
- 多级 Agent 主动预测和复杂 proactive activation（先验证基本 bounded recall/context 流程）。

### 需要重新评估（Reassess）
- 每一种 cursor/revision/epoch 是否真有独立语义，是否有不必要的重复 generation。
- 全局 CanonicalCommitCursor 的必要范围及其事务吞吐/锁竞争代价。
- producer barrier 的精确参与者集合、封口协议与线性化点。
- Applied 是否需要多个中间 ACK，还是保留最少且可验证的阶段。
- Forget completion 的物理擦除、逻辑抑制、备份过期和外部副本证明是否需要分层，而非一个总状态。
- 所有权边界是否导致过度跨模块往返；只能由相关 Owner 共同批准后调整。

### 不应引入（Do not introduce）
- 仅为“未来扩展”而建立的抽象层、插件框架、事件总线或服务。
- 同一数据的多个可写权威副本。
- 未有需求证据的分布式事务/全局锁/全局时钟。
- 将 Accepted/Applied/Forget complete 合并为通用 Success。
- 仅依赖定时重试或最终一致性、没有 generation/fence 防 stale 的协议。
- 为降低评分而删除必要安全检查、审计或恢复证明。

## 9. 模块化单体适配判断

**推荐作为第一阶段工程形态。** 逻辑模块仍保留 Owner 边界、独立接口、领域状态机和测试契约，但可在一个进程、一个部署单元和一个权威数据库中实现。使用本地事务、outbox、后台 worker 和可重建投影；通过模块接口而非网络调用建立边界。

适合模块化单体：D/E/F/G 的核心域逻辑、BMCP Gateway 的内部处理、治理策略执行、索引投影和 Context 管理。需要独立边界但未必独立部署：Adapter（位于 Agent 运行环境）、外部模型/工具调用、未来外部集成。只有在负载、故障隔离、安全边界或部署自治有测量证据后再拆服务。

模块化单体不能消除并发/恢复复杂度，但能减少网络分区、分布式事务、版本协商、部署编排和跨服务观测成本。

## 10. 架构阶段必须消除 vs 实现阶段处理

**架构阶段必须消除：**
- 权威身份、Scope、Fact/Claim、cursor/revision/epoch 语义冲突。
- Forget 与 Admission/Registration/Publication 的竞态和线性化点不明。
- Applied、Index watermark、Canonical commit、Forget proof 的证明边界混淆。
- 无法恢复的持久化窗口、无法识别 stale generation 的读写路径。
- Owner 间责任空洞或双重权威。
- 未批准的拓扑/技术选型被下游当成既定事实。

**可在实现阶段解决：**
- 具体锁类型、SQL 语句、索引参数、队列批量大小和重试间隔（前提是架构契约定义正确性条件）。
- 具体监控产品、部署流水线、告警阈值与容量参数。
- 在既定契约内优化算法、缓存和性能。
- 不改变外部语义的内部代码结构。

## 11. 复杂度相关架构约束（X 建议）

- X-CX-001：每个状态、游标、revision、epoch 必须登记 owner、scope、单调性、比较规则和权威持久化点。
- X-CX-002：跨模块操作必须登记参与者、operation ID、线性化点、可重试阶段、terminal states 和恢复动作。
- X-CX-003：任何 Receipt/Manifest/Applied/Watermark 必须声明 issuer、subject、scope、generation/version、durability、freshness 与 non-claims。
- X-CX-004：逻辑模块边界不自动要求独立服务；服务拆分需提供量化需求证据和新增运维预算。
- X-CX-005：所有 P0/P1 并发/恢复不变量必须绑定负向测试与故障注入证据。
- X-CX-006：投影/缓存/索引不得成为第二权威；必须可检测过期并可重建。
- X-CX-007：任何全局完成声明必须由授权 Owner 按全目标清单与 residual policy 证明。
- X-CX-008：未批准 ADR/候选契约不得作为实现冻结依据。

以上约束是 X 的建议，不自动成为项目规范；需 A/相关 Owner 依治理流程审议。

## 12. 必须回答的问题

A. 最复杂模块：D、E、Storage/Consistency；H/I 因跨模块责任与证据不足亦属高复杂度候选。  
B. 最复杂跨模块机制：Forget fence–producer barrier–derived registration–publication gate–global completion。  
C. 组合爆炸来源：多个状态机 × 多个 cursor/epoch × retry/duplicate/out-of-order × crash windows × partial completion。  
D. 正确性必要成本：权威边界、身份/权限、持久化 admission、fence、幂等、proof separation、恢复和可审计 residual。  
E. 过度设计风险：服务拆分过早、重复 retry/outbox/audit/version 框架、过多抽象和无需求多后端。当前不能把所有复杂设计直接判定为过度设计。  
F. 可延后：微服务、active-active、多后端、复杂自适应检索和高级 proactive activation。  
G. 模块化单体：适合首阶段，保留逻辑 Owner 和契约边界。  
H. 未来增长点：Forget 目标种类、索引分区/重建、Agent/Adapter 数量、权限撤销传播、备份/外部副本、双语与证据版本追踪。  
I. 测试维护成本：高，且当前不可证明可持续；跨模块并发/故障注入与回归矩阵尚无完整证据。  
J. 小团队最可能失控：D/E/Storage 发布原子性、I/D/F/G/H Forget 完成、C/G/H Applied 证明，以及 B 基础语义变更传播。

## 13. 验收门槛与最终判断

只有满足以下条件，才可把 NOT PROVEN 改为有证据支持的 CONDITIONAL PASS：
1. B 的 P0 身份/Scope/Fact-Claim ADR 由授权方决议并同步引用。
2. D/E/Storage 明确并测试 producer admission、dependency registration、barrier seal、publication gate 的原子边界。
3. H/C/G 对 Applied 的 issuer、Adapter boundary、版本、ACK 丢失、重连和旧 ACK 给出一致契约与测试。
4. I/D/F/G/H/Storage 定义 Global Forget 目标清单、permission revocation、backup/external copies、residual exceptions 与 completion proof。
5. Storage topology/transaction/recovery ADR 明确，且至少有 crash/replay/restore 证据。
6. P0/P1 每项不变量具备单元、契约、并发和故障注入测试；E2E 覆盖正常与部分失败。
7. 独立审查实际 Owner 源规范、集成版本和测试结果，而不是仅审查阅读指南、PR 描述或模拟角色报告。

在这些证据出现前，**不得声称架构复杂度已被证明可实现、可验证、可维护。最终结论：NOT PROVEN。**

## 14. 来源与精确版本

- Main baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Issue #43: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43
- PR #28 (Draft): https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28
- D Forget contract Blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D cursor contract Blob: `4688a0ca487bf4d853c7f0220408abe8d743d159`
- E Forget/publication contract Blob: `00e37ba56596e710513c8d0568acd79141d9101b`
- E receipt/idempotency contract Blob: `5ca77a5b48e69afb3bc81429baf538be7dce4d46`
- System interaction/data flow specifications and Phase 2 reconciliation report were read from the stated main baseline.
