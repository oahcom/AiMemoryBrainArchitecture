# Session E Review — Memory Compiler 三方六维度独立架构审查报告

- 审查日期：2026-11-16
- Repository：oahcom/AiMemoryBrainArchitecture
- 审查分支：本次连接读取的默认分支 HEAD
- 本次树 SHA：e2cc35d382d971061f65294959d3c0e742552cc3
- 审查类型：仓库文档静态审查、跨模块契约审查与失败语义审查
- 总体结论：**FAIL — Review Blocked / Not Passed**
- 报告路径：reviews/04-memory-compiler/three-party-six-dimension-review.md
- 审查方式：三个专业视角的独立模拟；不代表三名真实审查人员或三个独立模型签署。

> 本报告只评价本次实际可见的仓库文档证据。当前仓库 README 标注 Implementation status: Not started by design。本报告不是 Rust 代码审计、数据库事务验证、性能 Benchmark、渗透测试或故障注入结果。E 的核心设计文件未出现在本次仓库树中，因此不能把上位架构约束推断为 E 已经实现的能力。

---

## 1. 审查范围与材料

### 1.1 仓库树核验

本次读取 GitHub 默认分支递归文件树。可见目录包括：

- 00-governance/
- 01-system-architecture/
- 02-domain-model/
- 07-agent-integration/
- reviews/architecture/
- reviews/integration/
- reviews/03-memory-brain/
- reviews/05-memory-runtime/
- reviews/07-agent-integration/

以下目录在本次 HEAD 文件树中不存在：

- 03-memory-brain/
- 04-memory-compiler/
- 05-memory-runtime/
- 06-memory-context/
- 08-protocols/
- 10-security-and-governance/
- 11-consistency-and-recovery/
- 12-testing-and-acceptance/

树中也不存在指定的 E 审查文件 reviews/04-memory-compiler/three-party-six-dimension-review.md。此项是本次新增报告目标，不代表预先存在的报告缺失错误。

### 1.2 已读取材料

| 类别 | 文件 | 状态 |
|---|---|---|
| 项目基线 | README.md | READ |
| 路线图 | ARCHITECTURE_ROADMAP.md | READ |
| 治理 | 00-governance/architecture-invariants.md | READ |
| 治理 | 00-governance/design-principles.md | READ |
| 治理 | 00-governance/terminology.md | READ |
| 系统架构 | 01-system-architecture/component-interactions.md | READ |
| 系统架构 | 01-system-architecture/component-map.md | READ |
| 系统架构 | 01-system-architecture/data-flows.md | READ |
| 系统架构 | 01-system-architecture/responsibility-matrix.md | READ |
| 系统架构 | 01-system-architecture/system-boundaries.md | READ |
| 系统架构 | 01-system-architecture/system-overview.md | READ |
| 系统架构 | 01-system-architecture/system-quality-attributes.md | READ |
| 领域模型 | 02-domain-model/core-entities.md | READ |
| 领域模型 | 02-domain-model/domain-model-overview.md | READ |
| 领域模型 | 02-domain-model/epistemic-and-temporal-semantics.md | READ |
| 领域模型 | 02-domain-model/lifecycle-model.md | READ |
| 领域模型 | 02-domain-model/relationships-and-provenance.md | READ |
| 领域模型 | 02-domain-model/scope-and-permission-model.md | READ |
| Agent 集成 | 07-agent-integration/adapter-capability-tiers.md | READ |
| Agent 集成 | 07-agent-integration/agent-integration-overview.md | READ |
| Agent 集成 | 07-agent-integration/inference-boundary-model.md | READ |
| Agent 集成 | 07-agent-integration/telemetry-model.md | READ |
| 跨模块审查 | reviews/integration/phase-1-abc-cross-document-integration-review.md | READ |
| A 专项审查 | reviews/architecture/2026-11-16-three-party-six-dimension-review.md | READ |
| B 专项审查 | reviews/architecture/2026-11-16-memory-domain-model-three-party-six-dimension-review.md | READ |
| D 审查 | reviews/03-memory-brain/three-party-six-dimension-review.md | READ |
| F 审查 | reviews/05-memory-runtime/three-party-six-dimension-review.md | READ |
| C 审查 | reviews/07-agent-integration/three-party-six-dimension-review.md | READ |

### 1.3 必须审查但缺失的 E 材料

以下文件均未提交，不能审查其具体章节、状态机、字段或实现方案：

| 指定文件 | 状态 |
|---|---|
| 04-memory-compiler/compiler-overview.md | MISSING |
| 04-memory-compiler/event-ingestion-engine.md | MISSING |
| 04-memory-compiler/extraction-and-normalization.md | MISSING |
| 04-memory-compiler/evidence-and-provenance.md | MISSING |
| 04-memory-compiler/consolidation-and-conflict-resolution.md | MISSING |
| reviews/04-memory-compiler/three-party-six-dimension-review.md（既有报告） | MISSING |

因此本轮不能声称已完成“E 全部设计文档逐文件审查”。后文的 E 结论是“缺少设计证据导致门禁失败”，不是对不存在文档中的具体实现作事实判断。

### 1.4 D/F/G/H/I 交叉材料状态

- D：本次树中没有 03-memory-brain/ 设计目录；已有 D 审查报告明确结论为 FAIL，指出 D 核心设计交付物缺失。
- F：本次树中没有 05-memory-runtime/ 设计目录；已有 F 审查报告结论为 Review Blocked / Not Passed，指出 F 核心设计交付物缺失。
- G：06-memory-context/ 不存在，无法验证 Context Version、Change Set 与 Reconcile 消费契约。
- H：08-protocols/ 不存在，BMCP wire schema、Receipt、错误码和认证字段无法直接核验。C 文档仅提供逻辑级 envelope。
- I：10-security-and-governance/ 不存在，无法核验授权执行、Forget、Retention、审计与删除证明的具体机制。
- E 既有审查报告：本次不存在，不能继承任何 E 通过结论。

### 1.5 审查方法与限制

三方视角分别为系统架构、工程实现、安全与可靠性。三方是同一审查任务中的专业视角模拟，不代表三名真实人员签署。所有判断区分：
1. 已有规范约束；
2. 其他模块提出的接口要求；
3. E 自身设计证据；
4. 尚未验证的运行保证。

由于 E 设计文件缺失，第 3 类证据为空。不得将上位设计文档中的目标性语句当作 E 已经交付的机制。

---

## 2. 总体结论

### 2.1 最终决议：FAIL — Review Blocked / Not Passed

当前不能确认 Memory Compiler 能否把 Event、对话、环境经历和文档可靠地转换为可追溯、可恢复的 Canonical Memory。阻断原因是五份 E 核心设计文件均缺失，以下关键契约没有 E 侧可审查定义：

1. Event Envelope、Receipt、Producer 身份、Scope 绑定及 schema version。
2. Accepted 的耐久提交点、Outbox/Queue 语义和失败返回语义。
3. Idempotency Key 的作用域、相同 Key 不同 Payload 的冲突处理。
4. Extraction 中间表示、模型输出校验、候选对象身份和可迁移 Schema。
5. Evidence / Provenance 的引用完整性、原始证据保存策略和派生版本链。
6. Entity Resolution 的 Scope 限制、合并/拆分历史与授权检查。
7. Candidate Memory 到 D Canonical Store 的提交契约。
8. Canonical Commit 与 F Index Publication 的事件、水位线和恢复契约。
9. Forget 对队列、重试、Replay、候选产物和幂等记录的失效机制。
10. Compiler Job 状态机、可观测性、取消、背压和崩溃恢复。

A/B/C 的架构基线提供了正确方向，但不能替代 E 子系统的具体规格。README 亦明确规定，组件有名称不代表已经具备可实现的契约。

### 2.2 通过条件逐项判断

| 通过条件 | 判断 | 理由 |
|---|---|---|
| 不存在未解决 P0 | FAIL | Scope、Forget、Prompt Injection 和 Fact/Claim 基线冲突均未由 E 设计闭环 |
| Accepted 耐久承诺明确 | FAIL | C/系统层提出要求，E 的 Durable Ingestion 设计缺失 |
| Event / Candidate / Canonical 语义不混淆 | PARTIAL | 治理、B、系统交互文档有区分；E 自身转换与提交契约不可审查 |
| Scope 覆盖全 Pipeline | FAIL | B 有全链路要求，但 E 的各阶段授权与数据过滤设计缺失 |
| Forget 不会被 Retry/Replay 复活 | FAIL | I 和 E 的队列取消、generation fence、tombstone 规则均无 E 证据 |
| Evidence / Provenance 完整追溯 | PARTIAL | B 定义领域语义；E 的持久化、事务与引用完整性缺失 |
| Canonical Commit / Index Publication 一致性 | FAIL | 系统层有异步/outbox 方向；E/D/F 实际契约缺失 |
| D/F/G/H/I 可消费 E 接口 | FAIL | D/F/G/H/I 多数设计目录缺失，E 接口本身也缺失 |

### 2.3 放行建议

不允许冻结 E 的架构、Schema、Receipt、Idempotency、Candidate-to-Canonical 写入契约，也不允许据此放行实现。可以继续受控设计，但 E 必须先补齐五份核心文档，并明确引用 INT、AR、DM、C 审查问题 ID。不得将本报告中的候选修正方案误写为已批准 ADR。

---

## 3. 三方独立结论

### 3.1 第一方：系统架构师

**结论：FAIL — E 的职责边界只能从上位架构推知，缺少 E 自身规范证明。**

已有基线支持以下正确边界：

- Memory Compiler 是 Memory Brain 内部的体验到记忆转换层，不是 Agent Runtime、Agent Planner 或工具执行器。
- MC-01 Event Ingestion 负责验证、Scope、去重和耐久接受。
- MC-02 Extraction & Normalization 负责产生 Candidate Memory / Claim 提案，不直接成为 Canonical Truth。
- MC-03 Evidence & Provenance 负责来源定位、证据与派生链。
- MC-04 Consolidation & Conflict Resolver 负责候选整合与冲突提案，不得静默覆盖。
- D/Canonical Authority 拥有 Canonical Memory、版本和生命周期权威。
- F 消费 Canonical Commit 变更并构建可重建索引；E 不应拥有索引权威。
- G 消费 Canonical Memory 版本变化并 Reconcile Context；Candidate Memory 不得直接进入正式 Context。
- Agent 的规划、行动选择和工具执行权留在 Agent。

但 E 文件缺失，无法确认其是否：
1. 把 Canonical Commit 误放在 Compiler 内部；
2. 把 Index Publication 当成 Canonical Commit 的同一事务；
3. 把 Candidate Memory 直接暴露给 Runtime/G；
4. 在 Entity Resolution 中建立跨 Scope 的全局身份；
5. 让模型输出直接触发生命周期 Active/Verified；
6. 通过 Compiler Job 反向控制 Agent 或 Environment。

系统架构方向本身没有要求 E 成为独立进程或 Rust crate。任何部署拓扑都应留待工程证据，不应在缺失文档时推断。

### 3.2 第二方：工程实现负责人

**结论：FAIL — 关键持久化边界与故障语义没有可审查的 E 契约。**

系统架构的 Component Interactions 已提出：
- Event Ingestion 只有在 Durable Event 加可恢复处理意图之后才可返回 Accepted。
- Ingestion 到 Compiler 可采用至少一次投递，但各阶段必须幂等。
- Compiler 故障时 Event 应保持 durable/pending，并可从持久化状态恢复。
- Canonical mutation 使用版本前置条件或等价并发控制。
- Canonical 变更事件应支持 outbox/replay；索引为派生表示。
- Forget 应先建立 durable governance job/fence，再进行异步清理。

B 的 Core Entities 又规定：
- 同一幂等键、相同摘要返回先前结果；同一键、不同摘要必须拒绝。
- Memory Version 不可变；current pointer 原子推进。
- Canonical 提交前失败不得留下部分 Canonical mutation。
- Post-commit projection failure 通过 outbox/replay 修复。
- Event Recorded At 是耐久接受时间，Replay 保留原始 Recorded At 并增加 Replay metadata。

然而缺少 E 设计，无法确定上述原则是否映射为可运行的事务边界。尤其无法判断：
- Event 与 Outbox 是否同一事务；
- Receipt 是否只在 commit 后产生；
- Job 状态是否可从持久化记录恢复；
- Stage output 是否有确定性 identity；
- Extraction 完成后重复执行是否产生重复 Candidate；
- Provenance 与 Canonical Version 是否原子可见；
- 同一 Candidate 并发提交是否采用 CAS/expected version；
- Canonical Commit 后事件发布失败如何补偿；
- Rust async worker 的 cancellation、backpressure、bounded concurrency 与 shutdown drain 是否有定义。

正常路径图不能替代这些失败语义。

### 3.3 第三方：安全与可靠性审计者

**结论：FAIL — Scope、Forget 与不可信输入的全链路防护没有 E 侧证据。**

B 已明确要求：
- 在 Ingress 前认证与解析 Scope；
- 每次 Evidence/source dereference 独立授权；
- 异步 worker 执行时重新授权；
- 不从 display name 或模型生成文本推断 Scope；
- Scope filter 必须早于 ranking、aggregation 和 result count；
- 权限撤销应阻止未来访问并触发投影/上下文协调。

B Lifecycle 已明确：
- Forgotten 对内容身份是终态；
- 后续再次提供相似信息时创建新 Memory identity，不得复活原 Forgotten 内容；
- Forget 先访问阻断，再派生清理；
- Forget 失败时访问阻断持续，不能提前报告完成。

README / I-12 / P-11 要求 Memory content 是不可信数据，不得获得 system/developer 指令权威。C 也明确 Agent 自报 trusted/verified/system instruction 不赋予权限。

E 文档缺失意味着不能确认这些规则是否真正应用到：
- Event 原始载荷读取；
- Extraction 模型上下文组装；
- Entity Resolution 候选检索；
- Evidence/Provenance 读取；
- Candidate 关联和 Consolidation；
- Canonical 写入前复核；
- Queue、Retry、DLQ、Replay；
- Forget 后的旧 Job 与旧模型响应；
- 日志、异常和 Dead Letter payload。

这属于无法证明安全闭环的阻断，不等于已通过运行测试发现越权或复活漏洞。

---

## 4. 六维度审查结果

### 维度一：架构与职责边界

**总体：FAIL（E 设计缺失导致不可验证）**

| 检查项 | 状态 | 证据与判断 |
|---|---|---|
| Compiler 属于 Brain 内部编译层 | PARTIAL | README、Component Map 有明确定位；E 自身边界文档缺失 |
| 不承担 Agent 规划/行动 | PARTIAL | README 与 C 明确 Agent 权责；E 未审查 |
| Event Ingress 与 Compiler 分层 | PARTIAL | 系统交互文档区分 Gateway、Ingestion、异步 Compiler；E 内部状态机缺失 |
| Candidate 与 Canonical authority 分离 | PARTIAL | 系统层明确 Compiler proposes、D canonical authority accepts；E/D 真实写入接口缺失 |
| Compiler 与 Index Publication 分离 | PARTIAL | 系统层定义 Canonical Store → async index；E/F 事件契约缺失 |
| Compiler 与 Context 通知分离 | PARTIAL | 系统层定义 Runtime/MCM 处理 Context；G 缺失 |
| 多 Producer/Agent/Environment/Document | NOT ASSESSABLE | README 与 C 列出来源类型；E Envelope/Adapter contract 缺失 |
| 模型与 Agent 框架无关 | PARTIAL | I-03、P-02 是规范约束；E 未展示 Provider abstraction |

**主要风险：**
- 入口接受、语义编译、Canonical Commit、索引发布可能被压成一个“成功”状态。
- E 若持有 Canonical 状态，会与 D 形成重复权威。
- E 若直接发布 Runtime 可检索候选，会绕过 D 的 Lifecycle/Canonical gate。
- E 若依赖单一 LLM 输出结构，会破坏模型无关性与 Fact/Claim ADR 的可迁移要求。

### 维度二：领域模型与数据契约

**总体：FAIL（核心 E 契约不可审查）**

B Core Entities 提供了可供 E 消费的基础：
- Event：event_id、event_kind、source_type/source_id、payload_ref、event_time、recorded_at、scope_refs、environment_scope_id、idempotency_key、classification、schema_version、retention_class、integrity_digest。
- Candidate Memory / Claim：需要保留 scope、epistemic、temporal、source/evidence 与 provenance 语义。
- Evidence：source_ref、locator、excerpt_ref、collector、recorded_at、scope_refs、availability_state。
- Provenance：target_ref、source_edges、derivation_kind、method_ref、derived_at、input_digest_refs、parent_provenance_refs、unavailable_reason。
- Memory Version：immutable snapshot、parent_version、claims、entity/relation refs、provenance refs、content digest、schema version。

但 E 应明确的下列数据契约全部无文档证据：

| 契约 | E 应定义的最小内容 | 当前判断 |
|---|---|---|
| Event Envelope | authenticated producer、actor、scope、event/source time、recorded time、schema、payload ref、integrity、retention、idempotency | NOT ASSESSABLE |
| Event Identity | source identity、event identity、idempotency namespace、payload digest | NOT ASSESSABLE |
| Receipt | receipt ID、event ID、durable commit identity、accepted/rejected state、durability scope、timestamp | NOT ASSESSABLE |
| Compiler Job | job ID、event ref、pipeline version、stage、attempt、lease/owner、checkpoint、terminal state | NOT ASSESSABLE |
| Candidate IR | 可迁移类型、source spans、claims、entities、relations、uncertainty、scope、method metadata | NOT ASSESSABLE |
| Evidence | typed source ref、locator、digest、access scope、availability/retention | NOT ASSESSABLE |
| Provenance | input/output refs、method/model/rule versions、digest、parent lineage、unavailable reason | NOT ASSESSABLE |
| Conflict Set | participants、dimension、evidence、status、decision history | NOT ASSESSABLE |
| Canonical Write | expected version、candidate refs、evidence/provenance refs、scope、idempotency、result | NOT ASSESSABLE |
| Commit Result | canonical IDs/revisions、commit generation、outbox/event ref、deferred/rejected reason | NOT ASSESSABLE |

**Fact/Claim 约束：** B 的 Domain Model Overview 第 5 节选择 Claim 为规范命题对象，并将 Fact 视为 Claim 的资格/解释；但治理 I-04、P-04 与 README 把 Fact 和 Claim 列为不同概念。INT-P0-01 要求 ADR 解决前不得冻结。E 的中间表示必须保持可迁移，不得在 ADR 前把某一方案写死。

### 维度三：数据流与一致性

**总体：FAIL（缺少每阶段事务、状态与恢复契约）**

上位架构要求的逻辑路径是：

Event → Durable Acceptance → Normalization → Extraction → Entity Resolution → Evidence → Provenance → Candidate Memory → Consolidation → Canonical Commit → Index Publication。

E 必须逐段定义 durable input、idempotency、checkpoint、retry、commit point、failure outcome、recovery、observability。当前没有 E 文档可以验证其中任何一段的具体语义。

| 阶段 | 必须具备的语义 | 当前证据判断 |
|---|---|---|
| Event Ingress | 身份认证、Scope/Permission、schema/size 验证、payload durable store | NOT ASSESSABLE |
| Durable Acceptance | Event + recoverable work intent 的原子提交；receipt 只在 commit 后返回 | FAIL：无 E 证据 |
| Normalization | 确定性版本化、保留原始来源/时间/未知值、可重试 | NOT ASSESSABLE |
| Extraction | 模型输出视为 untrusted proposal；schema validate；model/prompt/rule version | NOT ASSESSABLE |
| Entity Resolution | Scope-filtered candidate generation；避免跨 Scope merge；merge/split history | FAIL：无 E 证据 |
| Evidence | source locator、digest、scope、retention、访问控制 | NOT ASSESSABLE |
| Provenance | lineage 原子可见、可追溯、可标记不可用 | NOT ASSESSABLE |
| Candidate Memory | 不可误当 Canonical；可追溯 event/job/stage | NOT ASSESSABLE |
| Consolidation | 冲突保留、并发控制、非静默覆盖 | NOT ASSESSABLE |
| Canonical Commit | D 授权、CAS/expected version、原子版本与 lineage | FAIL：D 文档也缺失 |
| Index Publication | Canonical change event、watermark、replay、stale fence | FAIL：F 文档缺失 |

#### 3.1 Durable Acceptance 的最低规范

系统 Component Interactions §4.1 已定义：Accepted 只有在 Durable Event 加可恢复处理意图后才成立；存储不可用时必须返回 RetryableUnavailable/backpressure，而不能虚假 Accepted。§4.2 允许至少一次 dispatch，但阶段处理必须幂等。C 的 Telemetry workflow 也明确 Accepted 不等于 Memory creation。

E 至少需要证明：
1. 原始 Envelope / payload reference 已持久化；
2. Scope、producer identity、schema version、idempotency identity 已持久化；
3. 可恢复的 Compiler Job / outbox intent 已持久化；
4. Receipt 与 Event/Job 的逻辑身份稳定；
5. 同 Key 同规范化 Payload 返回原结果；
6. 同 Key 不同 Payload 明确返回 IdempotencyConflict；
7. Receipt 不代表 Extraction 或 Canonical Commit 完成。

缺少上述任一项，不得宣称 Durable Accepted。

### 维度四：安全与治理

**总体：FAIL（P0 门禁无法证明）**

#### 4.1 Scope Isolation

B Scope and Permission Model §6 要求异步任务执行时重新授权；§12 要求 Scope filter 在 ranking、aggregation 和 result count 之前生效；Evidence/Provenance 需要独立授权。

E 应在以下位置明确授权检查：
- 原始 Event 读取前；
- 文档/对话 chunk 读取前；
- Extraction 上下文拼装时；
- Entity Resolution 候选生成前；
- Entity/Relation 关联时；
- Evidence/Provenance dereference 时；
- Consolidation 读取 Canonical 候选时；
- Canonical Commit 前；
- Retry、DLQ、Replay 和人工 reprocess 时。

当前 E 文件不存在，无法证明 Scope 连续性。INT-P0-02 为阻断项。

#### 4.2 Forget

B Lifecycle Model §3 定义 Forgotten 是内容身份终态；§8 定义先访问阻断、后依赖清理；§10 要求失败后访问阻断持续、可重试且不得提前报告完成。A/B/C 集成报告进一步要求覆盖 Event、Evidence、Provenance、Candidate、Queue、Retry、Replay、Index、Cache、Context、Backup。

E 必须能定位并失效：
- Event payload 与 Event metadata；
- extraction chunks / intermediate outputs；
- model response / structured output；
- Evidence / Provenance；
- Candidate Memory 与 Conflict proposal；
- Queue / Outbox / Retry / DLQ；
- Idempotency record；
- Compiler Job / checkpoint；
- Replay source 与 derived artifact。

还必须明确：
- Forget fence / generation 如何阻止旧 worker 写回；
- 已运行中的模型请求如何在返回后丢弃；
- 已领取的 job 如何取消或在每个提交点重新检查；
- tombstone 保留哪些不可逆、不可重建的最小元数据；
- 幂等记录保留期如何避免 Forget 后相同 key 重新生成内容。

E 文档缺失，无法证明 Forget 不会因 Retry/Replay 复活数据。INT-P0-03 为阻断项。

#### 4.3 Prompt Injection 与 Trust Promotion

README、I-12、P-11 规定 Memory 是数据而非指令；C Overview §6 规定 Agent 提交的 trusted/verified/system instruction 标签不授予权限。B Epistemic Model §2 规定 Verified 需要验证方法、验证者/来源、Evidence 和验证时间；高置信度本身不能 Verified。

E 应确保：
- 原始文档、网页、对话、工具输出都以 untrusted data 传给模型；
- 抽取 Prompt 的 system/developer instruction 与 source content 严格分层；
- 模型不得决定权限、Scope、Retention、Trust 或 lifecycle authority；
- 模型返回的 verified/trusted 标签只能作为未验证提案；
- Verified 必须由明确验证程序及 Evidence 支持；
- 输出经过类型、引用、Scope、时间和来源校验；
- 失败、低置信度、解析不确定时不得升级 epistemic status；
- 日志、错误、DLQ 不复制敏感原文。

当前无 E 的 extraction/security 设计可供检查。INT-P0-04 为阻断项。

### 维度五：性能与资源

**总体：NOT ASSESSABLE（不得作吞吐或延迟承诺）**

System Quality Attributes §3/§4 要求按硬件、模型、量化、语料、Scope 分布、并发、事件大小、缓存状态、到达速率与持续时间声明 Benchmark。E 应分别测量：

- Event ingress durable commit latency；
- Ingress throughput、backpressure、rejection rate；
- Queue age、stage latency、retry rate；
- Normalization throughput；
- Extraction LLM call rate、token/cost、GPU/VRAM、fallback rate；
- Entity Resolution fan-out、候选数与 scope cardinality；
- Provenance DAG depth/fan-out 与写放大；
- Conflict Detection 候选窗口与成本；
- Canonical commit latency；
- Index publication lag；
- DLQ backlog 与 retry storm；
- 大型文档切块、重试和资源释放。

确定性处理可包括 Envelope/schema validation、timestamp normalization（有明确输入时）、digest、idempotency lookup、scope binding validation、结构化引用检查、stage bookkeeping、状态机与 outbox 操作。是否可完全确定性完成，取决于最终规范规则。

模型辅助步骤可能包括自然语言抽取、实体提及识别、关系/命题候选生成、语义归一化、摘要或冲突候选发现。但模型结果必须保持 proposal 状态并经过确定性校验与治理流程。任何模型调用都不得同步阻塞 Durable Acceptance。

E 未提交，无法确认是否有 Queue isolation、priority、batching、bounded concurrency、backpressure、cancellation 或 resource budgets。不得编造固定吞吐量或 p95/p99。

### 维度六：可演进性与可观测性

**总体：FAIL（版本与派生追踪契约无证据）**

从 Event 到 Canonical Memory 至少应记录：
- Event schema version；
- Compiler pipeline version；
- Normalization version；
- Extraction model/provider/version；
- Prompt/template version；
- Rule/config version；
- Entity Resolution algorithm/version；
- Provenance schema/version；
- Candidate IR version；
- Canonical domain schema version；
- retry/replay attempt 与原始 Recorded At；
- correlation_id / causation_id；
- stage/job/event/candidate/canonical IDs；
- scope class / permission decision reference（避免泄露原始敏感标识）；
- error class、retryability、queue age、stage duration。

日志与 Trace 不得替代 Evidence/Provenance；不得把原始敏感载荷复制到日志、指标标签或错误消息。Schema 迁移必须能解释旧 Event 和旧 Candidate 的处理版本，Replay 必须明确是重放原始结果还是按新 Pipeline 重新编译，不能静默混用。

E 文档缺失，以上要求均无法核验。

---

## 5. Pipeline 分阶段风险矩阵

| Pipeline 阶段 | 关键风险 | 级别 | 当前状态 |
|---|---|---:|---|
| Event Envelope / Producer | 身份与 Scope 绑定不可信 | P0 | 无 E 契约，未证明 |
| Durable Acceptance | Accepted 早于 Event/Job 耐久提交 | P1 | 无 E 契约，阻断 |
| Idempotency | 相同 Key 不同 Payload 被覆盖或误去重 | P1 | 无 E 契约，阻断 |
| Normalization | 丢失原始时间、来源、未知值或 Scope | P1 | 无 E 契约 |
| Extraction | Prompt Injection、模型输出提升为事实/指令 | P0 | 无 E 契约 |
| Entity Resolution | 跨 Scope 合并身份或污染引用 | P0 | 无 E 契约 |
| Evidence | 原始证据不可定位、越权读取或提前删除 | P1 | B 有语义，E 无实现契约 |
| Provenance | 派生链断裂、引用悬空、Forget 无法发现依赖 | P1/P0 | B 有语义，E 无提交契约 |
| Candidate Memory | Candidate 被误当 Canonical/Active | P0 | 无 E→D 契约 |
| Consolidation | 冲突被静默覆盖或模型单方裁决 | P1 | 无 E 契约 |
| Canonical Commit | 非原子版本提交、越权或重复写入 | P1/P0 | D/E 设计均缺失 |
| Index Publication | Canonical 成功但 Index 永久遗漏/旧数据复活 | P1 | F 设计缺失 |
| Forget propagation | Retry/Replay 重新创建已忘记数据 | P0 | E/I 设计缺失 |

---

## 6. 强制崩溃窗口与恢复矩阵

由于 E 的持久化状态机与实现文档缺失，以下是必须通过设计和后续故障注入证明的恢复要求；不是声称这些故障已在运行环境复现。

| # | 崩溃窗口 | 正确恢复语义 | 当前审查判断 |
|---|---|---|---|
| 1 | Durable Commit 前崩溃 | 不得返回 Accepted；未提交数据由 Producer 重试；不存在伪 Receipt/Job | NOT PROVEN |
| 2 | Durable Commit 后、Receipt 返回前崩溃 | Event + Job intent 已耐久；同幂等键重试返回同一 Event/Receipt，不重复创建 | NOT PROVEN |
| 3 | Receipt 返回后、Compiler Job 开始前崩溃 | Job 可由 durable outbox/pending state 扫描恢复；Accepted 不丢失 | NOT PROVEN |
| 4 | Extraction 完成后、Canonical Commit 前崩溃 | Extraction artifact/checkpoint 可恢复；重复执行幂等；Candidate 可重新提交；无部分 Canonical commit | NOT PROVEN |
| 5 | Canonical Commit 成功后、Index Publication 前崩溃 | Canonical commit 与 publication intent 可恢复；F 可按 generation/watermark 重放；Canonical 不回滚 | NOT PROVEN |
| 6 | Forget 发生后、旧任务重试 | Forget fence 优先；旧 job/worker/replay 在写入前重新检查并拒绝；模型迟到响应丢弃 | NOT PROVEN — P0 |
| 7 | 同一幂等键被不同 Payload 重用 | digest mismatch 返回明确冲突；不得覆盖原事件或复用旧 Receipt | NOT PROVEN — P1 |

### 6.1 必须补充的崩溃注入点

至少还应覆盖：
- Outbox commit 后 publisher 启动前；
- Queue publish 成功但 ack 丢失；
- Worker lease 到期但旧 worker 仍在执行；
- Entity Resolution 完成后、Evidence/Provenance 写入前；
- Provenance 写入成功但 Candidate 写入失败；
- Candidate 已生成但 Scope 权限撤销；
- Canonical commit 与 Forget fence 竞争；
- DLQ 重放与 schema migration 并发；
- Index watermark 更新成功但部分 shard 未完成；
- Retention 清理与 Replay 同时运行。

---

## 7. P0/P1/P2/P3 问题清单

> Owner 为责任建议，不代表已分配或已接受。每项均需由对应 Owner 在修订文档中提供证据并满足 Acceptance Criteria。

### E-REV-P0-01 — Scope 在 Compiler 全链路无可审查执行契约

- **Severity：** P0
- **File / Section：** 缺失的 04-memory-compiler/ 全部五份文件；对照 02-domain-model/scope-and-permission-model.md §6、§9、§12
- **Evidence：** B 要求入口、Canonical read、Evidence dereference、mutation、activation、async worker 均授权；要求过滤在 ranking/aggregation 前生效。E 文件树不存在。
- **Problem：** 无法证明 Scope/Permission 在原始读取、模型上下文、实体解析、证据读取、关联、合并、写入和重试时持续生效。
- **Impact：** 跨用户/项目/Agent/Environment 读取、实体错误合并、证据泄露或越权写入。
- **Required Correction：** 在每个 Pipeline stage 明确 principal、resource、scope、action、policy version、授权时点与失败语义；每个 worker 执行前重授权；Entity Resolution 候选必须先 Scope filter。
- **Owner：** Session E + Session I；B 定义语义，H 提供可信身份。
- **Dependency：** INT-P0-02、DM-005、DM-010、C P1-03。
- **Acceptance Criteria：** 跨 Scope 负向测试覆盖 Ingress、Extraction context、Entity Resolution、Evidence、Consolidation、Canonical write、Retry、Replay；权限撤销后旧任务不得继续受保护操作；拒绝响应不泄露内容或对象存在性。

### E-REV-P0-02 — Forget 与 Queue/Retry/Replay 的复活防护未定义

- **Severity：** P0
- **File / Section：** 缺失的 event-ingestion-engine.md、evidence-and-provenance.md、consolidation-and-conflict-resolution.md；对照 02-domain-model/lifecycle-model.md §3、§8、§10
- **Evidence：** B 定义 Forgotten 为内容身份终态，Forget 先访问阻断，失败时继续阻断且可重试；E 文件不存在。
- **Problem：** 无法确认 Forget 是否能定位并失效 Event、派生输出、Evidence、Candidate、Queue、Retry、DLQ、Replay、幂等记录与在途 worker。
- **Impact：** Forget 后旧任务可能重建 Candidate/Canonical，违反删除语义；审计无法证明完成。
- **Required Correction：** 定义 durable Forget fence/tombstone、目标 generation、job cancellation、worker pre-commit recheck、late model response discard、DLQ/Replay denylist、幂等记录协调、派生依赖清单和完成状态。
- **Owner：** Session I 主责；Session E、D、F、G、H 协作。
- **Dependency：** INT-P0-03、DM-007、DM-011、DM-013。
- **Acceptance Criteria：** 对每一阶段注入 Forget 与旧任务竞争；旧任务不得产生可读内容；Replay 识别 tombstone；部分清理失败时状态不报告完成；审计数据不能重建被忘记内容。

### E-REV-P0-03 — 不可信输入与模型输出的信任升级防护无设计证据

- **Severity：** P0
- **File / Section：** 缺失的 extraction-and-normalization.md、evidence-and-provenance.md
- **Evidence：** README、I-12、P-11 要求 Memory 是数据而非指令；B Epistemic Model 要求 Verified 必须有方法与 Evidence；C Overview §6 拒绝 Agent 自报 trust/verified 标签授予权威。
- **Problem：** 无法确认恶意文档、对话、网页或工具输出是否作为不可信数据处理，也无法确认模型输出是否被限制为候选提案。
- **Impact：** Prompt Injection 可能影响抽取；模型可能把恶意文本转为规则、Verified Claim 或权限元数据。
- **Required Correction：** 定义不可信输入边界、模型提示隔离、结构化输出 Schema、确定性校验、Trust/Epistemic Status 来源规则；禁止模型单方设置 Verified、授权、Retention 或 Scope。
- **Owner：** Session E + Session I；B 定义 epistemic semantics。
- **Dependency：** INT-P0-04、AR-002、B DM-006、C P1-02。
- **Acceptance Criteria：** 恶意 prompt/document/tool fixtures 不得改变系统规则、权限、Scope 或 Trust；Verified 缺少独立验证方法/Evidence 时必须拒绝；模型输出不得越过 Candidate/Canonical gate。

### E-REV-P0-04 — Candidate/Canonical 权威与 Fact/Claim 未决基线未被证明遵守

- **Severity：** P0
- **File / Section：** 缺失 compiler-overview.md、consolidation-and-conflict-resolution.md；对照 domain-model-overview.md §5、governance I-04/P-04
- **Evidence：** 系统 Component Interactions §4.3 规定 Compiler proposes、Canonical/Lifecycle authority accepts；INT-P0-01 指出 Fact/Claim 基线冲突，ADR 前不得冻结 Schema。
- **Problem：** 无 E 输出 IR 与 D Canonical Write Contract，无法确认 Candidate 不会被当成 Canonical；也无法确认 Fact/Claim 身份没有提前锁定。
- **Impact：** 重复权威、规范 Schema 分叉、Candidate 未经 Lifecycle 进入 Runtime/Context、下游数据迁移困难。
- **Required Correction：** 明确 Candidate IR 与 Canonical object 分离；Canonical commit 必须由 D authority 接受；Fact/Claim 相关字段通过可迁移 IR/extension 暂存，等待 ADR。
- **Owner：** Session E + Session D + Architecture Governance。
- **Dependency：** INT-P0-01、DM-001、INT-P1-02。
- **Acceptance Criteria：** 未经 D commit 的 Candidate 不可由 F/G 当作正式 Canonical Memory；Fact/Claim ADR 未批准前不存在不可逆 Schema/wire freeze；冲突和修订保留历史。

### E-REV-P1-01 — Accepted / Durable Ingestion / Receipt / Idempotency 契约缺失

- **Severity：** P1（在实现冻结前阻断）
- **File / Section：** 缺失 event-ingestion-engine.md
- **Evidence：** Component Interactions §4.1、§4.2；C Telemetry workflow；B Core Entities §2、§12；INT-P1-04。
- **Problem：** 无 E Receipt 字段、事务边界、幂等作用域、payload digest、相同键冲突语义和重试结果定义。
- **Impact：** 假 Accepted、重复 Event、不同 Payload 被错误去重、崩溃后丢失编译任务。
- **Required Correction：** 定义 Envelope、Receipt、Idempotency namespace、canonicalized payload digest、durable Event+Job/outbox commit、重复与冲突返回语义。
- **Owner：** Session E；H 定义 wire contract，I 定义认证/保留。
- **Dependency：** INT-P1-04、C P1-03、C P1-04。
- **Acceptance Criteria：** 覆盖七个强制崩溃窗口；相同 key+相同 payload 返回同 receipt；相同 key+不同 payload 返回冲突；无 durable commit 不返回 Accepted。

### E-REV-P1-02 — Candidate IR 与 Fact/Claim ADR 可迁移性未定义

- **Severity：** P1
- **File / Section：** 缺失 extraction-and-normalization.md
- **Evidence：** B Domain Model 将 Claim 作为当前规范命题对象，但治理基线存在 Fact/Claim 冲突；INT-P0-01 要求 ADR 前不冻结。
- **Problem：** 无法确认抽取中间表示是否与最终 Canonical Schema 解耦，是否保存原始语义、来源类型和未知字段。
- **Impact：** ADR 决议后可能需要重抽取或破坏性迁移。
- **Required Correction：** 定义 versioned, typed, migration-friendly Candidate IR；保留 source phrase、raw field、normalized value、uncertainty、proposed semantic type 与 mapping version。
- **Owner：** Session E + B + Architecture Governance。
- **Dependency：** INT-P0-01、DM-001、DM-006。
- **Acceptance Criteria：** Candidate IR 可映射到 ADR 任一合法方案；Schema version 升级可重放或迁移；未知扩展不会被静默丢弃。

### E-REV-P1-03 — Provenance 与 Evidence 原子持久化和引用完整性缺失

- **Severity：** P1
- **File / Section：** 缺失 evidence-and-provenance.md
- **Evidence：** I-05、P-05；B relationships-and-provenance.md §5、§7、§8、§9；INT-P1-06。
- **Problem：** 无法确认每个 Candidate/Canonical target 是否与所需 Evidence/Provenance 同时提交或通过可恢复 outbox 关联，也没有 lineage cycle、empty source 和 unavailable semantics 的 E 侧说明。
- **Impact：** 派生记忆无法追溯、引用悬空、Forget 依赖发现不完整、Replay 无法重建。
- **Required Correction：** 明确 lineage graph 规则、source version/locator/digest、method/model/rule version、atomic visibility、reference validation、unavailable reason 与 retention handling。
- **Owner：** Session E + D + I。
- **Dependency：** INT-P1-06、DM-007、DM-011。
- **Acceptance Criteria：** 任一派生 Claim/Memory 可追溯到 source evidence 或明确 unavailable reason；不存在 dangling reference；目标提交不可在必需 lineage 缺失时成功；Forget 能发现注册的所有派生对象。

### E-REV-P1-04 — Canonical Commit 与 Index Publication 的一致性接口缺失

- **Severity：** P1
- **File / Section：** 缺失 compiler-overview.md、consolidation-and-conflict-resolution.md；D/F 设计目录缺失
- **Evidence：** Component Interactions §4.3/§4.4；B Core Entities §12；INT-P1-06。
- **Problem：** 无 Canonical Commit Result、commit generation、outbox event、F 消费事件、Index Watermark 或 stale generation fence 定义。
- **Impact：** Canonical 已提交但索引永久遗漏；旧候选/旧 revision 覆盖新状态；索引延迟期间返回 Retraction/Forget 数据。
- **Required Correction：** 定义 Canonical commit 的原子结果与可重放 publication intent；F 维护单调 watermark/generation；Retraction/Forget 先建立 serving deny fence；明确 eventual consistency 与查询降级语义。
- **Owner：** D + E + F；I 定义 Forget fence。
- **Dependency：** INT-P1-06、AR-004、DM-007。
- **Acceptance Criteria：** Canonical commit 后 publisher 任意时点崩溃可恢复；重复/乱序 publication 不回退 watermark；索引滞后时不返回被撤回/Forget 的内容。

### E-REV-P1-05 — Entity Resolution / Conflict Set / Merge-Split 契约缺失

- **Severity：** P1
- **File / Section：** 缺失 extraction-and-normalization.md、consolidation-and-conflict-resolution.md
- **Evidence：** B Core Entities §6/§7；B Relationships and Provenance §2/§3；B 专项报告 DM-003/DM-004/DM-009；C P1-02。
- **Problem：** 无法审查实体候选生成、Scope 限制、identity evidence、Conflict Set、merge/split 映射和回滚/修正。
- **Impact：** 同名不同实体合并、跨环境污染、冲突被吞并、历史引用失效。
- **Required Correction：** 定义 Entity Resolution proposal vs canonical identity decision；scope-compatible match；evidence threshold；merge/split record；Conflict Set participant/evidence/decision history；禁止模型直接合并。
- **Owner：** E + D + B；I 负责权限。
- **Dependency：** INT-P1-02、DM-003、DM-004、DM-009、C P1-02。
- **Acceptance Criteria：** 同名跨 Scope/Environment 不自动合并；每个 merge/split 可追溯且可纠错；Conflict Set 保留全部不兼容主张及裁决历史。

### E-REV-P1-06 — Compiler Job 状态、Retry、DLQ、Replay 与取消语义缺失

- **Severity：** P1
- **File / Section：** 缺失 event-ingestion-engine.md、compiler-overview.md
- **Evidence：** Component Interactions §6/§8/§9；System Quality Attributes §5；INT-P1-04。
- **Problem：** 无 stage state machine、lease/attempt、retry classification、DLQ、replay mode、cancellation、backpressure 和 idempotent output identity。
- **Impact：** 重试风暴、任务丢失、重复派生、旧任务覆盖新版本、Forget 后复活。
- **Required Correction：** 定义 durable job state machine、bounded retry/backoff、DLQ reason、operator replay authorization、pipeline version pinning、cancellation/fence、per-stage idempotency 和 queue quotas。
- **Owner：** E；I/Consistency 与 H 协作。
- **Dependency：** INT-P1-04、INT-P0-03、DM-013。
- **Acceptance Criteria：** 任一阶段 worker crash 可从 checkpoint 恢复；重复投递不重复提交逻辑产物；DLQ 重放受授权、版本和 Forget fence 约束；过载产生明确 backpressure。

### E-REV-P1-07 — Scope/Permission 在长任务阶段的撤权和身份重绑定规则缺失

- **Severity：** P1
- **File / Section：** 缺失 event-ingestion-engine.md、extraction-and-normalization.md
- **Evidence：** B Scope Model §6、§11；C P1-03；INT-P0-02。
- **Problem：** 无法确认任务在排队期间 producer/Agent/Session/Environment 身份变化、授权撤销或 Scope 关闭后如何处理。
- **Impact：** 已排队工作在权限失效后继续读取、抽取或写入。
- **Required Correction：** Job 固化可信 principal/scope reference 与 policy decision reference，但执行时重新授权；权限变化触发 pause/cancel/reject；不得只信任入队时的授权结果。
- **Owner：** E + I + H。
- **Dependency：** INT-P0-02、C P1-03、DM-005。
- **Acceptance Criteria：** 撤权、Scope revoked/closed、Agent instance 解绑后，旧任务在下一受保护阶段失败关闭；不泄露受保护源内容。

### E-REV-P2-01 — Pipeline 与模型/规则版本可观测性不足以评估

- **Severity：** P2
- **File / Section：** 缺失 compiler-overview.md、extraction-and-normalization.md、evidence-and-provenance.md
- **Evidence：** I-05、I-22；System Quality Attributes §3/§4/§9。
- **Problem：** 未提供 Pipeline version、Model/Prompt/Rule/Normalization version、stage trace 与重放记录设计。
- **Impact：** 无法解释某个 Canonical Claim 如何生成，无法比较新旧编译结果。
- **Required Correction：** 为每次 job/stage 固化版本、input/output digest、attempt、duration、correlation/causation IDs；日志脱敏。
- **Owner：** E + I。
- **Dependency：** INT-P1-06、DM-013。
- **Acceptance Criteria：** 从 Canonical Version 可反查 Event、Evidence、Provenance、pipeline/model/rule versions；日志不含不必要原文。

### E-REV-P2-02 — 背压、优先级、批处理和大文档资源边界未定义

- **Severity：** P2
- **File / Section：** 缺失 event-ingestion-engine.md、compiler-overview.md
- **Evidence：** System Quality Attributes §3/§5/§8。
- **Problem：** 没有队列隔离、最大 payload、文档切块、模型并发、GPU/VRAM budget、优先级或过载语义。
- **Impact：** 高频 Telemetry 被大型文档阻塞，重试风暴和模型调用挤占资源。
- **Required Correction：** 定义 admission control、per-source quotas、queue classes、bounded concurrency、batching、large-document chunking、model budget 与 graceful degradation。
- **Owner：** E + Rust Engineering。
- **Dependency：** INT-P1-04、QA-01/QA-05。
- **Acceptance Criteria：** 过载可预测并显式拒绝/延迟；资源上限可配置；无 Benchmark 不承诺吞吐量。

### E-REV-P2-03 — Schema/Replay 演进策略与可审计性缺失

- **Severity：** P2
- **File / Section：** 缺失 compiler-overview.md、event-ingestion-engine.md
- **Evidence：** B Core Entities §1/§12；System Quality Attributes §7/§9。
- **Problem：** 不清楚 Replay 使用原始 Pipeline 版本还是当前 Pipeline，旧 Schema 的兼容、迁移与重新编译语义未定义。
- **Impact：** 同一 Event 在不同版本得到不可解释结果，历史 Canonical 变更无法审计。
- **Required Correction：** 区分 exact replay、reprocess/recompile；固定原始 schema/pipeline version；记录迁移链和新旧产物关系。
- **Owner：** E + I + Architecture Governance。
- **Dependency：** INT-P1-04、DM-013。
- **Acceptance Criteria：** Replay 模式显式选择；旧结果不可静默覆盖；重编译产生新的 derivation/version 记录。

### E-REV-P3-01 — E 设计文档与接口矩阵尚未交付

- **Severity：** P3（但缺失本身造成整体审查 FAIL）
- **File / Section：** 04-memory-compiler/ 全目录
- **Evidence：** 本次 HEAD 文件树中无该目录与五份指定文件。
- **Problem：** 无法进行逐文件审查、章节证据定位和 E 与 D/F/G/H/I 的双向契约核对。
- **Impact：** 设计评审不可追踪，子系统无法达到路线图规定的接口、失败语义与验收准入标准。
- **Required Correction：** 提交五份核心文件，使用统一规格模板，列出输入/输出/状态机/事务/失败/恢复/安全/性能/验收/OPEN。
- **Owner：** Session E Owner。
- **Dependency：** ARCHITECTURE_ROADMAP.md Phase 2/3。
- **Acceptance Criteria：** 五份文件全部可读取；每个跨模块接口有 producer/consumer、authority、schema version、idempotency、failure/recovery semantics 和 testable acceptance criteria。

---

## 8. INT-* 状态矩阵

状态说明：PASS 表示 E 侧已有足够证据满足；PARTIAL 表示上位材料有规则但 E 侧证据不足；FAIL 表示相关冻结门禁未满足；NOT APPLICABLE 表示本轮无关。本次没有任何 INT 项能因 E 自身设计而获得 PASS。

| ID | 状态 | E 审查判断与证据 |
|---|---|---|
| INT-P0-01 | FAIL | Fact/Claim 基线冲突未见 ADR；B Domain Model §5 与 I-04/P-04 不一致；E IR 缺失，不能冻结 |
| INT-P0-02 | FAIL | B Scope Model 有全链路授权要求；E 每阶段 Scope 传播/重授权设计缺失 |
| INT-P0-03 | FAIL | B Lifecycle 定义 Forget 终态和访问阻断；E Queue/Retry/DLQ/Replay fence 缺失 |
| INT-P0-04 | FAIL | README/I-12/P-11 与 B Epistemic Model 有原则；E 不可信输入和模型输出验证文档缺失 |
| INT-P1-02 | FAIL | Claim identity/revision、Conflict Set、Entity merge/split 未在 E 侧定义；B DM-003/004/009 未关闭 |
| INT-P1-03 | PARTIAL | C Envelope/Telemetry 有 producer、agent、scope 等字段，但身份绑定与权限归属未闭合；E 消费契约缺失 |
| INT-P1-04 | FAIL | System/C 定义 durable acceptance 的目标；E Receipt、事务、幂等和七个崩溃窗口无证据 |
| INT-P1-06 | FAIL | B 定义 Provenance/Version 语义；E 持久化、引用完整性、提交可见性和 Index publication 契约缺失 |

---

## 9. A/B/C 问题 ID 响应矩阵

### 9.1 A：AR-001 至 AR-004

| ID | 状态 | E 侧判断 |
|---|---|---|
| AR-001 | FAIL | Forget 全链路必须覆盖 Event、Evidence、Provenance、Candidate、Queue/Retry/Replay；E 未提交 Forget fence 与派生依赖设计 |
| AR-002 | FAIL | 模型抽取与 Memory Prompt Injection 必须把来源内容视为不可信；E extraction 文档缺失 |
| AR-003 | FAIL | Scope 必须在候选生成前并贯穿图扩展/缓存/异步任务；E 全 Pipeline 授权设计缺失 |
| AR-004 | PARTIAL | B 已定义 Provenance lineage 与 source unavailable；E 的实际写入原子性、DAG/cycle、引用完整性与重放契约缺失 |

### 9.2 B：DM-001 至 DM-013

| ID | 状态 | 对 E 的影响 |
|---|---|---|
| DM-001 | FAIL | Fact/Claim 基线冲突；E IR 必须保持可迁移，ADR 前不得冻结 |
| DM-002 | PARTIAL | Context Version/Change Set 由 G 主责；E 需仅发布 Canonical 变化通知，不得建立第二 Context authority；G 缺失 |
| DM-003 | FAIL | Claim identity/revision 规则未决，E Candidate Claim identity 与修订映射不能冻结 |
| DM-004 | FAIL | Conflict/Conflict Set 结构缺失，E Consolidation 无法形成可审计冲突结果 |
| DM-005 | FAIL | Generic Scope 结构不完整；E Envelope/Job scope reference 不能自行定义另一套 Scope |
| DM-006 | FAIL | TypedRef/TimeValue/ContentRef/ActorRef 等核心类型不完整；E IR 和 provenance refs 依赖这些类型 |
| DM-007 | FAIL | Provenance DAG/cycle 规则 OPEN；E 不能承诺依赖遍历/Forget 完整性 |
| DM-008 | PARTIAL | Lifecycle 变更双路径未决；E 必须把生命周期决策交给 D，不能自建第二权威 |
| DM-009 | FAIL | Entity merge/split 与 Relation 撤回审计不足；E Resolution 不能直接覆盖 canonical identity |
| DM-010 | FAIL | Scope 过滤验收矩阵未闭合；E 候选生成和 Entity Resolution 需前置过滤 |
| DM-011 | FAIL | Forget 外部副本/备份边界未闭合；E 必须记录 source availability 与派生对象清单 |
| DM-012 | PARTIAL | Provenance/Conflict/Forget 复杂度尚无预算；E 应提供测量点但不虚构数字 |
| DM-013 | FAIL | Schema/词汇版本迁移与审计追踪未完整定义；E 需要 Pipeline/Model/Rule/Schema versioning |

### 9.3 C：指定问题 ID

| ID | 状态 | E 侧判断 |
|---|---|---|
| P1-02 | PARTIAL | Observation/Outcome 判别由 C/B 定义；E 需保持两类来源语义，不重复编译为相互覆盖的事实 |
| P1-03 | FAIL | Producer→Agent→Instance→Session/Task/Environment 身份绑定未闭合；E 必须消费可信身份与 Scope，不信任 payload 自述 |
| P1-04 | FAIL | Accepted 必须表示耐久 Event 与可恢复处理意图已提交；E 侧事务/Receipt 缺失 |
| P1-05 | PARTIAL | C 的后续状态/乱序或幂等相关契约需 E 采用 revision/sequence 与 idempotency 规则；具体 E 处理未提交 |
| P1-07 | FAIL | 权限撤销、Context/缓存及本轮异步数据路径的安全治理依赖 I；E 对旧任务、派生物和 Forget/revoke 的阻断策略缺失 |

---

## 10. 与 D/F/G/H/I 的接口冲突与契约缺口

| 模块 | 应由 E 提供/遵守的接口 | 当前证据 | 审查结论 |
|---|---|---|---|
| D — Canonical Memory | Candidate proposal、Claim/Entity/Relation refs、Evidence/Provenance refs、Scope、expected version、idempotency、Canonical Commit Result | D 设计目录缺失；B 仅有领域语义 | NOT VERIFIED；不得让 E 自建 Canonical authority |
| F — Memory Runtime | Canonical commit/change event、revision/retraction/forget signal、generation/watermark | F 设计目录缺失；已有 F Review 也指出核心文件缺失 | NOT VERIFIED；索引不得消费未提交 Candidate |
| G — Memory Context | Canonical version change notification；Superseded/Retraction/Forget 的 reconcile trigger | G 目录缺失 | NOT VERIFIED；Accepted/Candidate 不可解释为 Context 可激活对象 |
| H — BMCP/Adapter | producer identity、scope claims、Receipt、Accepted/Rejected、error taxonomy、schema negotiation | H 目录缺失；C 仅有逻辑 envelope | NOT VERIFIED；不能自行冻结 wire contract |
| I — Security/Governance | authz recheck、Forget fence、retention、audit redaction、tombstone/replay deny | I 目录缺失；B 有领域要求 | NOT VERIFIED；不得承诺 Forget 完成或异步任务持续授权 |

### 10.1 D — Canonical Write Contract

E 只能提交 Candidate/Canonical proposal。D 应返回明确的 committed/deferred/rejected/conflict 结果，并由 D 管理 canonical IDs、immutable versions、lifecycle state 和 current pointer。E 不应在本地先行声明 Canonical Memory 已成立。Canonical commit 与 Evidence/Provenance 的可见性必须具有原子或可恢复语义。

### 10.2 F — Index Publication

E 不应直接把 Candidate 发给索引作为 Canonical 数据。索引输入必须源自 Canonical Commit event/change feed，携带可比较的 revision/generation。F 必须能够检测延迟、重复和乱序。Forget/Retraction 的 serving fence 不得等待异步索引完全删除才生效。

### 10.3 G — Context Reconcile

Accepted、Extraction Complete、Candidate Created 均不等于可激活 Memory。只有 D 已提交的 Canonical version 才能成为正式 Context 的合法来源，且 G 仍须检查 Scope、Lifecycle、Epistemic Status 和 Forget state。Superseded、Retracted、Forgotten 应触发 reconcile/invalidation。

### 10.4 H — Receipt 与 Producer Trust

C 的逻辑 Envelope 包含 telemetry_id、producer_id、agent_instance_id、scope、signal_type、schema_version、recorded_at、idempotency_key 等。H 应负责 wire-level 身份与消息契约；E 负责 durable acceptance 语义。Producer ID 不能由未经认证的 payload 自报字符串决定。

### 10.5 I — Forget 与 Retention

E 必须提供完整的派生对象登记与清理入口，但 Forget 权威、授权、Retention policy 与完成证明应由治理层定义。审计日志不能保留足以恢复被删除的原始内容。幂等记录和 tombstone 的保留应避免内容复活，同时不无限保留敏感载荷。

---

## 11. DECIDED / CANDIDATE / TO_VALIDATE / OPEN

本节区分现有基线决策与本报告提出的设计建议。下列候选方案不是 E 已批准的设计。

### 11.1 DECIDED（来自现有上位基线）

- Brain 是 Canonical Memory 的逻辑权威；Agent 不决定 Brain 内部记忆组织规则。
- Event、Memory、Claim、Evidence、Entity、Relation 是不同语义层次；Event Accepted 不等于 Memory Compiled。
- Compiler 提出 Candidate；Canonical/Lifecycle authority 决定是否成为 Canonical。
- Accepted、Compiled、Canonical Commit、Index Published 是不同阶段事实。
- Durable acceptance 不应依赖 LLM 在线；语义编译默认异步。
- Scope 与 Permission 分离；异步 worker 执行时重新授权。
- Memory 内容是 untrusted data，不获得 system/developer instruction 权限。
- Provenance 应追溯来源和派生过程；冲突不得静默覆盖。
- Forget 是治理工作流；Forgotten 内容不得因重试或重放而复活。
- Index/Cache 是派生表示，不拥有 Canonical authority。
- 性能目标必须通过可复现 Benchmark 验证。

### 11.2 CANDIDATE（建议 E 评估，不视为批准）

- Event 与可恢复 Compiler Job intent 通过同一数据库事务或等价事务性 Outbox 提交。
- 使用 at-least-once delivery + stage-level idempotent processing，而不是假设 exactly-once。
- 每个 Compiler Job 固化 pipeline/schema/model/prompt/rule version。
- Candidate IR 与 Canonical Schema 解耦，允许 Fact/Claim ADR 后映射。
- Provenance 采用可终止遍历的 DAG；如业务确需循环，应定义显式 cycle type 与边界。
- Canonical commit event 通过 outbox/change feed 交付 F；索引使用单调 watermark。
- Forget fence 使用单调 generation/epoch，旧 worker 在每个受保护写入点校验。
- 按 source class / workload 分离队列优先级，限制大文档和模型调用占用。
- 以 deterministic validation gate 限制所有 LLM extraction output。

### 11.3 TO_VALIDATE

- 目标硬件上的 LLM 辅助抽取成本、VRAM、吞吐和尾延迟。
- 不同文档长度、对话长度和环境事件频率下的 chunking/normalization 成本。
- Entity Resolution 的 Scope-filtered fan-out 与误合并率。
- Provenance DAG depth/fan-out 与长期存储增长。
- Conflict Detection 的误报/漏报与批处理成本。
- Queue fairness、backpressure、retry storm containment。
- Index publication lag 与 Forget suppression latency。
- Rust async runtime 的 worker concurrency、cancellation 与 shutdown drain 行为。

### 11.4 OPEN

- INT-P0-01 Fact/Claim ADR 的最终选择。
- Claim identity/revision 与 Conflict Set 规范。
- Generic Scope 与 Typed Reference 最终 Schema。
- Durable Acceptance 的存储/Outbox 实现机制。
- Event/Compiler Job/Receipt 的 wire 与 persistence schema。
- Provenance DAG/cycle、lineage compaction 和 retention 规则。
- Canonical Commit Result 与 F Index Watermark 的完整协议。
- Forget 与幂等记录、DLQ、Replay 的最终协调规则。
- I 的外部模型副本、备份、物理删除和审计边界。
- G 对 Canonical revision/retraction/forget 的 Context reconcile 契约。

---

## 12. 修复顺序与退出条件

### Phase 0 — 恢复可审查性（立即）

1. 提交五份 E 核心设计文档。
2. 每份文档标记 DECIDED/CANDIDATE/TO_VALIDATE/OPEN。
3. 为每个跨模块接口列出 producer、consumer、authority、schema version、scope、idempotency、failure/recovery。
4. 将本报告 E-REV IDs 与 INT/AR/DM/C IDs 交叉引用。

**退出条件：** 五份文件在仓库默认分支可读取，章节和版本明确；不再以任务书或图示代替实际设计证据。

### Phase 1 — 先解决阻断性领域与安全契约

1. INT-P0-01：Fact/Claim ADR 或明确保持中间表示可迁移。
2. INT-P0-02：统一 Principal/Producer/Scope/Permission contract，落实全 Pipeline 重授权。
3. INT-P0-03：Forget fence、Queue/Retry/DLQ/Replay cancellation 与 tombstone。
4. INT-P0-04：不可信输入、模型输出验证与 Verified 证据门槛。
5. 明确 Candidate 与 Canonical authority 的唯一写入边界。

**退出条件：** 不存在未处置 P0；安全设计具备负向测试矩阵；未经批准的 ADR 不被 E 设计偷偷冻结。

### Phase 2 — Durable Ingestion 与 Canonical Commit

1. 定义 Event Envelope、Receipt、Idempotency namespace 和 payload digest。
2. 定义 Event + recoverable Job intent 的提交边界。
3. 定义 Job state machine、checkpoint、lease、retry、DLQ、Replay。
4. 定义 Candidate IR、Evidence/Provenance 持久化与引用完整性。
5. 定义 Canonical Write Contract、expected version、冲突返回和 Commit Result。
6. 定义 Canonical outbox/change event 与 F watermark。

**退出条件：** 七个强制崩溃窗口有可执行测试；所有状态有持久化恢复来源；重复与乱序不造成语义漂移。

### Phase 3 — 跨模块契约与工程验证

1. 与 D 对 Candidate/Canonical/Claim/Conflict/Provenance 合同。
2. 与 F 对 Canonical change feed、Index Watermark、Retraction/Forget fence。
3. 与 G 对 Canonical-only activation source 与 Reconcile trigger。
4. 与 H 对 Producer identity、Receipt、Accepted、错误语义。
5. 与 I 对授权撤销、Forget、Retention、审计脱敏。
6. 执行故障注入、Scope negative tests、Forget replay tests、Prompt Injection fixtures 和性能 Benchmark。

**最终退出条件：**
- 所有 P0 关闭；
- 所有 P1 关闭或经正式 ADR/接口裁决明确接受；
- Event/Candidate/Canonical 语义分离；
- Accepted 的耐久承诺和幂等边界可测试；
- Scope 覆盖读取、处理、关联、写入和 Replay；
- Forget 不会被 Retry/Replay 复活；
- Evidence/Provenance 可追溯且引用完整；
- Canonical Commit 与 Index Publication 有恢复和 watermark 方案；
- D/F/G/H/I 均能消费 E 的已版本化契约；
- 无未经 Benchmark 的性能承诺。

---

## 13. 审查局限

1. 本轮没有 E 设计文档，不能对其内部组件、数据结构、事务实现或状态机作肯定/否定的细节判断。
2. D/F/G 设计目录、H/I 专项设计目录均未在本次树中出现，跨模块检查主要依据 A/B/C 上位契约和既有审查报告。
3. 本报告没有执行 Rust 编译、数据库事务测试、并发测试、队列故障注入、Prompt Injection 测试、Scope 渗透测试或性能 Benchmark。
4. 本次树状态只代表本次连接读取到的默认分支 HEAD；不推断其他分支、未提交工作区或其他会话内容。
5. 三方是专业视角的独立模拟，不代表三名真实审查人员或三个独立模型签署。
6. 缺失文档导致的 FAIL 是交付与证据门禁失败，不应误写成已复现的运行时漏洞。

---

## 14. 最终决议

**Session E：FAIL — Review Blocked / Not Passed。**

当前仓库没有提交 Memory Compiler 的五份核心设计文件，因此无法证明 Compiler 已形成可靠、可追溯、可恢复的 Canonical Memory 编译契约。上位架构已明确 Accepted、Compiled、Canonical Commit、Index Publication 的阶段边界，也明确 Scope、Forget、Provenance 与不可信输入的治理要求；但 E 必须在自己的设计中把这些要求落为字段、状态机、事务边界、失败语义、恢复流程和验收测试。

**不得冻结 E 的接口或放行实现。** 完成 Phase 0–3 并满足退出条件后，重新执行 E 三方六维度审查。

报告结束。
