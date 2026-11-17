# Memory Domain Model 三方六维度审查报告

- **审查日期：** 2026-11-16
- **审查对象：** `02-domain-model/` 下六份 Memory Domain Model 文档
- **审查类型：** 静态架构与领域契约审查（非代码审计、非运行测试）
- **结论状态：** 有条件通过；存在一项必须先解决的架构基线冲突，以及若干实现契约缺口
- **审查文件归属：** `reviews/architecture/`
- **审查方法：** 沿用仓库既有三方六维度方法。三方为系统架构师、工程实现负责人、安全与可靠性审计者；六维度为架构边界、领域模型、数据流与一致性、安全与治理、性能与资源、可演进性与可观测性。

> **独立性说明：** 本报告由同一审查流程分别模拟三个专业视角，不代表三名独立审查人员或三个独立模型已实际签署意见。结论是基于文档的设计审查判断，未由实现、渗透测试或性能测试验证。

---

## 1. 审查范围与依据

### 1.1 纳入审查的文档

- `02-domain-model/domain-model-overview.md`
- `02-domain-model/core-entities.md`
- `02-domain-model/epistemic-and-temporal-semantics.md`
- `02-domain-model/relationships-and-provenance.md`
- `02-domain-model/lifecycle-model.md`
- `02-domain-model/scope-and-permission-model.md`

### 1.2 架构基线与交叉依据

- `README.md`
- `00-governance/architecture-invariants.md`
- `00-governance/design-principles.md`
- `00-governance/terminology.md`
- `01-system-architecture/system-overview.md`
- `01-system-architecture/responsibility-matrix.md`
- `01-system-architecture/system-quality-attributes.md`

### 1.3 审查限制

本次只审查领域语义、对象模型、责任边界、状态和跨文档契约。没有验证数据库 DDL、Rust 类型定义、事务实现、并发执行、真实删除行为、检索效果或运行性能。文中“风险”表示设计缺口或潜在故障路径，不表示已在运行系统中复现。

---

## 2. 三方审查结论

### 2.1 第一方：系统架构师

**结论：有条件通过；先解决规范冲突，再进入跨子系统接口冻结。**

认可事项：

- Event、Memory、Claim、Entity、Relation、Evidence、Provenance、Memory Version 和 Memory Context 的语义边界清晰，避免把原始输入、知识主张、证据和上下文渲染混成一个对象。
- Epistemic Status 与 Lifecycle State 分离；Confidence、Relevance、Trust、Evidence Strength 分离；Event Time、Recorded At、Valid Time 分离。这些正交维度是正确的领域基础。
- Brain、Compiler、Canonical Store、Lifecycle、Entity/Relationship、Evidence/Provenance、Runtime、MCM、Governance 的权属大体与系统架构责任矩阵一致。
- Scope 与 Permission 分离，Environment Scope 显式建模，符合跨 Agent、任务、会话和不同世界/存档隔离要求。
- Context Remove 与 Forget 分离，且 Forget 覆盖派生数据的方向正确。

必须收敛：

1. **Fact/Claim 规范冲突：** Domain Model 将 Fact 与 Claim 合并为同一规范对象，但 `architecture-invariants.md` I-04 明确列出 Fact 与 Claim 为不同领域概念；`design-principles.md` P-04 和 README 也保留了 Fact 与 Claim 的区分。该冲突不能仅靠术语解释消除，必须由 ADR 决定是修改基线还是修改 Domain Model。
2. **Context Version 缺少规范对象定义：** Context 具有版本号和并发语义，但领域对象表没有定义 Context Version / Change Set 的完整身份、父版本、提交者、变更内容、摘要和幂等字段。
3. **Scope 通用对象不完整：** 文档定义了 User、Project、Agent、Agent Instance、Task、Session、Environment、System 等 Scope，但实体字段只详细展开 Agent Scope 和 Environment Scope；通用 Scope 的身份、父子关系和生命周期仍未形成统一契约。
4. **冲突对象语义不足：** Claim 的 Disputed 状态要求存在冲突记录或不兼容立场，但没有定义 Conflict / Conflict Set 的规范结构、参与 Claim、冲突原因、裁决历史与状态。
5. **Claim 身份与版本关系尚未闭合：** Claim ID 跨 Memory Version 稳定还是版本局部身份仍为 OPEN；这会影响修订、引用、冲突、撤回和派生 lineage。

### 2.2 第二方：工程实现负责人

**结论：模型结构可实现，但当前还不是可直接生成数据库/接口契约的完整逻辑 Schema。**

认可事项：

- Opaque ID、不可变 Memory Version、expected-version/CAS、幂等键、结构化错误和 outbox/replay 方向明确。
- 核心工作流“解析 Scope → 授权 → 语义校验 → 引用校验 → 提交不可变记录/版本 → 发布变更事件”具有可执行性。
- 多对多关系、证据链接和 provenance lineage 已明确意识到需要显式关联记录。
- Lifecycle、Epistemic Status、Entity Identity Status、Relation State 分开建模，避免单一 status 字段承担多个状态机。

需要补齐：

- `TimeValue`、`TimeInterval`、`TypedObjectRef`、`ContentRef`、`ScopeRef`、`ActorRef`、`TypedMap` 等类型目前主要以名称出现，缺少最小规范结构、空值/未知值规则和版本兼容约束。
- Claim 状态修订、Conflict 记录、Entity Merge/Split 迁移、Forget Operation、Lifecycle Event 等操作实体尚未形成完整字段与提交语义。
- Memory Version 的 immutable snapshot 与 Claim 的稳定身份/修订模型需要统一，否则历史版本引用可能出现“同一 Claim ID 指向不同内容”或“修订后引用断裂”。
- Context Entry 的 `source_refs`、`rendering_ref` 与 Canonical Version / Provenance 的关系需要明确；当前 Context Entry 的最小数据结构不足以独立重建或审计一次上下文变更。
- Relation 的 retracted 状态有状态语义，但 Relation 本体字段没有明确的撤回原因、操作者、时间及其不可变历史记录归属。

### 2.3 第三方：安全与可靠性审计者

**结论：安全原则方向正确；需要把“定义了隔离/删除”推进到可验证闭环。**

认可事项：

- Default Deny、Scope/Permission 独立判断、异步执行时重新授权、Evidence 单独授权、Fail Closed 等原则明确。
- 不信任 Agent 自报 Scope，不从名称推断身份；不允许模型生成内容自行授予权限。
- Forget 有即时访问阻断、依赖发现、派生清理、索引/缓存/上下文失效和完成验证的工作流。
- Provenance 允许标记 source unavailable，避免回放时伪造源内容。

需要收敛：

1. Scope 过滤必须在检索候选生成、关系扩展、重排、聚合、缓存、Working Set、Context 构建之前生效；不能只在最终输出时过滤。
2. Forget 的依赖发现依赖 Provenance/Source 图完整性；当前 provenance DAG 是否允许循环仍为 OPEN，若不限制派生环，将影响遍历终止、删除覆盖和审计完整性。
3. 对外部模型/第三方服务已接收内容的删除边界不能由 Brain 单方面保证；需要明确已发送数据的控制范围、供应商承诺、用户告知和审计状态。
4. Scope 引用与 Evidence/Provenance 引用都可能暴露环境坐标、用户内容定位符或资源存在性；错误和审计日志必须遵守最小披露。
5. “Verified”必须落实到可审计的验证方法与证据引用；不能只由模型自评或置信度阈值触发。

---

## 3. 六维度审查

### 维度一：架构边界

**判断：基本通过，领域权属清晰；跨系统上下文对象边界仍有缺口。**

已通过的边界：

- Domain Model 定义对象语义，不负责数据库 DDL、LLM 抽取算法、向量索引、Runtime 排序、Agent 规划和工具执行。
- Compiler 负责提出候选，Lifecycle Manager 负责规范状态迁移，Canonical Store 负责持久化和版本机制，Governance 负责授权与 Forget 执行。
- Memory Context 是 Canonical Memory 的任务/范围视图；Context Entry 不拥有或修改 Canonical Memory。
- Agent 提供遥测与环境观察，但不决定 Brain 的内部记忆组织规则。

需要明确：

- System Architecture 定义了 Applied Context、Delivery State、Adapter acknowledgement 和 inference boundary；Domain Model 目前没有明确声明这些对象是领域外协议状态，还是需要在领域模型中定义的引用对象。建议在 Domain Model Overview 增加“外部协议/运行时对象边界”说明，明确本域只定义 Context 及其版本，交付与 Applied 证明由 Sync/BMCP 拥有。
- Context Version 的权威归 MCM，但目前对象模型没有定义其结构；这不是部署层问题，而是跨模块接口的核心领域缺口。

### 维度二：领域模型

**判断：核心语义质量较高，但存在一项基线冲突和多个关键概念未落到对象模型。**

#### P0：Fact 与 Claim 的规范基线冲突

- `00-governance/architecture-invariants.md` I-04：Event、Memory、Fact、Entity、Relation、Evidence 是不同领域概念。
- `00-governance/design-principles.md` P-04：同样明确 Fact 与 Claim 不同。
- `README.md`：同样写明 Event、Memory、facts、entities、relations、evidence distinct。
- `02-domain-model/domain-model-overview.md` 第 5 节：将 Claim 定义为 canonical proposition object，并写明 Fact 是 Claim 的 qualified interpretation，不作为独立对象类型。

**影响：** 后续 Compiler、Canonical Store、检索、API 和测试可能分别实现两种互不兼容的数据模型；这会污染核心对象身份和接口契约。

**建议：** 暂停该决策的下游冻结，创建 ADR 明确选择：
- 方案 A：Fact 是独立领域对象，Claim 是待验证/带来源的主张，二者通过证据、验证与派生关系连接；
- 方案 B：Fact 是 Claim 的一种 epistemic/semantic qualification，不是独立持久化对象，并同步修改 I-04、P-04、README 和术语表。
不能让 Domain Model 单方面覆盖治理基线。审查方不在本报告中替项目作出该产品语义决策。

#### P1：缺失的关键领域对象/结构

1. **Conflict / Conflict Set：** Disputed Claim 需要明确冲突集合、冲突参与方、冲突维度、证据、裁决记录和未决状态。
2. **Context Version / Context Change Set：** 定义 context_id、version_id/sequence、parent_version、base_version、actor、change_reason、entry snapshot/delta、digest、commit time、idempotency key。
3. **Generic Scope：** 定义统一 Scope 身份及 kind、owner、parent、namespace、status、policy_ref；Agent Scope 和 Environment Scope 作为受约束的专门化类型。
4. **Claim Revision / Epistemic Revision：** 明确是原 Claim 不可变并产生 successor，还是 Claim ID 稳定而版本快照承载修订；定义引用和撤回历史。
5. **Governance Operation：** Forget Operation 至少需要目标、授权决策、依赖快照/发现水位、访问阻断时间、阶段状态、重试/幂等、完成证明和残留例外。
6. **Entity Merge/Split Record：** 定义旧 ID、新 ID、映射/重定向、迁移范围、证据、操作者和回滚/纠错记录。

#### P1：类型定义尚未达到规范 Schema 完整度

以下类型需要最小字段和语义约束，而不能只作为未展开的类型名：
- `TimeValue` / `TimeInterval`：精确值、区间、精度、时区、原始表达、来源和不确定性。
- `TypedObjectRef`：对象类型、对象 ID、可选版本 ID、引用可见性/授权规则。
- `ScopeRef`：Scope ID、kind、是否必须绑定版本或状态。
- `ContentRef`：内容定位、版本/摘要、存储或外部来源可用性。
- `ActorRef`：主体类型、稳定身份和认证来源；不能把 display name 当作身份。
- `TypedPredicate` / `TypedValue`：词汇版本、类型约束、单位/编码和兼容规则。

### 维度三：数据流与一致性

**判断：提交和恢复原则正确；对象修订、上下文版本与派生图一致性还需要明确。**

主要风险：

- **Claim 修订与 Memory Version 不对齐：** Memory Version 保存 ClaimSnapshot，但 Claim ID 跨版本的身份策略未决；这会影响增量索引、历史查询、冲突链接和 Provenance。
- **Context 版本无法独立审计：** Context 仅有 current_context_version，缺少版本对象/变更记录结构，难以定义 delta 重放、snapshot 修复和并发冲突。
- **Provenance 依赖关系不够严格：** source_edges、parent_provenance_refs 的空集合语义、派生节点的唯一目标、DAG 约束和事务提交边界需要明确。
- **Lifecycle 变更双路径：** 文档允许生命周期变更进入 Memory Version 或 append-only lifecycle event。需要确定唯一权威事件/版本机制，避免两个来源出现状态分歧。
- **Relation/Entity 历史迁移：** Merge/Split 和 Relation successor 的迁移记录尚未定义，索引和下游引用可能保留旧 ID 或丢失历史语义。

建议：

1. 统一 Claim identity/revision 规则，并用并发、修订、撤回、回放测试覆盖。
2. 定义 Context Version 与 Change Set 的不可变结构，明确 base_version 冲突时拒绝、重算或合并的规则。
3. 对 Provenance lineage 明确 acyclic invariant（若确有循环业务需求，必须定义受控 cycle type 与遍历边界），并明确空来源/未知来源的表达。
4. 明确 Canonical commit、Provenance visibility、outbox publication 和 Index watermark 的原子性/恢复协议。
5. 定义 Entity Merge/Split 与 Relation 更新的引用迁移和 projection rebuild 行为。

### 维度四：安全与治理

**判断：原则通过；必须把 Scope 与 Forget 的验证边界具体化。**

#### 已建立的防护方向

- Scope 不等于 Permission；默认拒绝。
- 每次读取、Evidence dereference、写入、状态转换、激活、Context delivery、导出和异步任务执行均需授权。
- 不能从 display string 推断 Scope，不能隐式跨用户/环境 join。
- Evidence 访问可比 Memory 更严格。
- Forget 与 Context Remove 明确分离，Forget 需要依赖发现、访问阻断、派生清理和完成验证。

#### P1：Scope 泄漏路径

需要把以下要求写成统一的验收矩阵，而非只保留原则性描述：

- Scope filter 在 candidate generation 前生效；
- Graph expansion 的每条边和目标节点均重新检查 Scope/Permission；
- reranker、聚合计数、相似度分数和错误信息不能泄露未授权对象；
- cache key 包含足以区分主体、Scope、权限版本和环境版本的维度；
- Working Set、Context Entry、Delta、Snapshot、日志和诊断均遵循同一隔离规则；
- 异步任务在执行时重新授权，撤权后不得继续执行受保护阶段。

#### P1：Forget 依赖图完整性与边界

- Provenance 循环会使依赖发现、递归清理和完成证明变复杂；应先定义 DAG 或受限循环规则。
- 对索引、缓存、上下文、工作集、备份、快照、外部模型副本分别定义状态和完成语义。
- 逻辑访问阻断必须先于异步物理删除；部分失败时不得报告 Forget 完成。
- 审计元数据不能保留足以重建被忘记内容的信息。
- 对外部模型或第三方系统已接收数据，必须明确不可由 Brain 单方保证的删除范围。

### 维度五：性能与资源

**判断：性能责任与测量方向正确；领域层仍需定义复杂度边界，不应提前承诺数值。**

认可事项：

- 已将验证成本、关系 fan-out、Provenance traversal、时间查询、冲突检测和 Forget dependency discovery 列为 TO_VALIDATE。
- 没有虚构固定延迟或吞吐指标，符合系统质量属性基线。
- 将 scope-filtered correctness 作为性能测试的硬约束，避免通过跳过安全过滤获得虚假加速。

需要补齐的性能契约：

- 关系查询的最大 fan-out、遍历深度、分页/截断语义和“结果不完整”标识。
- Provenance traversal 的深度、节点数、时间预算与部分结果语义。
- Conflict detection 的候选窗口、时间重叠计算成本和批量处理策略。
- Scope composition 与 Permission check 的批量评估接口及缓存失效约束。
- Forget 依赖发现的分页、水位线、重试和长任务进度语义。

建议以系统质量属性文档中的可复现实验声明为准，分别测量冷/热缓存、不同 Scope 数量、关系 fan-out、Provenance 深度、数据规模与并发量。性能不得以丢失 Evidence、弱化 Scope 校验或跳过历史记录为代价。

### 维度六：可演进性与可观测性

**判断：扩展意识较好；词汇版本、迁移和端到端追踪仍需闭合。**

认可事项：

- Opaque ID 不携带业务语义。
- Event、Memory Version 等包含 schema_version。
- Relation type 采用受控词汇；Scope kind、epistemic status、lifecycle state 都有明确分类。
- 未决设计被标为 OPEN、CANDIDATE 或 TO_VALIDATE，没有把候选方案伪装成决定。

需要补齐：

- Relation vocabulary、TypedPredicate、Event kind、Memory kind、Evidence kind、Scope kind 的注册、版本、弃用和兼容规则。
- Enum 新增、未知值、旧版本读取和数据迁移策略；“未知枚举拒绝”与“可安全保留未知扩展值”应按字段类别分别定义。
- Claim/Memory/Entity/Relation/Context Version 的迁移脚本与历史版本解释规则。
- 每个跨组件变更应可由 correlation_id / causation_id 串联 Event → Evidence → Provenance → Claim → Memory Version → Index → Retrieval → Context Version → Adapter acknowledgement。
- 冲突裁决、Claim 撤回、Entity Merge/Split、Forget 等高影响操作应有统一审计事件字段。

---

## 4. 风险清单与优先级

| ID | 优先级 | 风险 | 主要影响 | 建议状态 |
|---|---|---|---|---|
| DM-001 | P0 | Fact/Claim 定义与 I-04、P-04、README 冲突 | 核心对象模型分叉，阻塞接口冻结 | OPEN |
| DM-002 | P1 | Context Version / Change Set 缺少规范对象 | 并发、重放、Applied 关联与审计不完整 | OPEN |
| DM-003 | P1 | Claim identity/revision 策略未决 | 历史引用、冲突和索引更新不确定 | OPEN |
| DM-004 | P1 | Conflict / Conflict Set 未定义 | Disputed 状态缺乏可持久化裁决对象 | OPEN |
| DM-005 | P1 | Generic Scope 规范结构不完整 | Scope 解析、父子约束和跨域隔离难以统一 | OPEN |
| DM-006 | P1 | 核心引用/时间类型未形成最小 Schema | 各子系统可能产生不兼容编码 | OPEN |
| DM-007 | P1 | Provenance DAG/循环规则未定 | 依赖遍历、Forget 和 lineage 审计不确定 | OPEN |
| DM-008 | P1 | Lifecycle 变更记录允许双路径 | Memory 状态与事件历史可能分歧 | OPEN |
| DM-009 | P1 | Entity Merge/Split 与 Relation 撤回审计结构不足 | 引用迁移、历史解释与恢复困难 | OPEN |
| DM-010 | P1 | Scope 端到端过滤验收矩阵不完整 | 检索、缓存、图扩展或上下文泄漏 | OPEN |
| DM-011 | P1 | Forget 外部副本和备份边界未闭合 | 删除承诺不可验证或过度承诺 | OPEN |
| DM-012 | P2 | 关系、Provenance、Conflict、Forget 缺少复杂度预算 | 大规模数据下延迟与资源不可预测 | OPEN |
| DM-013 | P2 | 词汇注册、Schema 迁移与审计追踪规则未完整定义 | 长期兼容性与可运维性下降 | OPEN |

---

## 5. 整改建议与验收标准

### 5.1 领域基线冻结前必须完成（P0）

**DM-001 Fact / Claim 决策**

验收标准：

- 通过 ADR 明确 Fact 与 Claim 是两个对象还是一个对象的不同资格状态。
- 若选择统一对象，必须同步更新 I-04、P-04、README、terminology 和所有引用处。
- 若选择独立对象，必须定义两者身份、生命周期、证据关系、验证/派生关系和权限语义。
- Compiler、Canonical Store、Runtime 和测试规范对同一决策达成一致。
- 不允许某个子系统自行采用与基线不同的解释。

### 5.2 详细接口冻结前必须完成（P1）

- 定义 Context Version / Change Set 结构和并发协议。
- 决定 Claim ID 跨版本策略与不可变修订模型。
- 定义 Conflict Set 和裁决历史。
- 定义 Generic Scope 与 Agent/Environment Scope 的继承/组合规则。
- 定义核心 Typed Reference、TimeValue、ContentRef、ActorRef 等最小结构。
- 明确 Provenance DAG 约束、空来源语义和提交原子性。
- 统一 Lifecycle state 与 append-only event 的权威关系。
- 定义 Entity Merge/Split、Relation retract/supersede 和 Forget Operation 的审计对象。
- 将 Scope 与 Forget 的端到端测试矩阵纳入安全治理与系统验收。

### 5.3 原型与运行验证阶段完成（P2）

- 关系和 Provenance fan-out/depth 基准。
- 时间查询与冲突检测正确性/成本基准。
- Forget 依赖发现、部分失败、重试和恢复演练。
- 大规模 Scope 过滤和缓存隔离压力测试。
- Schema 演进、历史数据迁移和多版本 Adapter 兼容测试。

---

## 6. 决议

1. **保留 Domain Model 的总体方向与核心对象分层。**
2. **DM-001 必须先通过 ADR 解决；在此之前，不建议冻结 Fact/Claim 相关接口和存储 Schema。**
3. **Context Version、Claim Revision、Conflict Set、Generic Scope 是进入详细接口设计前的优先补齐项。**
4. **Provenance、Scope、Forget 的安全与一致性要求必须落实为跨组件验收用例。**
5. **本次不要求将逻辑对象机械映射为独立服务、数据库或 Rust crate。**
6. **本报告不代表领域模型已经通过实现、隐私、安全或性能验证。**
7. **建议下一轮将 Domain Model 与 Memory Brain、Memory Compiler、Memory Runtime、Memory Context、Governance 的接口文档进行交叉审查。**

## 7. 后续审查记录

| 审查轮次 | 范围 | 状态 |
|---|---|---|
| Round 1 | System Architecture 三方六维度静态审查 | 已有报告 |
| Round 2 | Memory Domain Model 三方六维度静态审查 | 本报告 |
| Round 3 | Domain Model P0/P1 整改复审 | 待 ADR 与接口补齐 |
| Round 4 | Domain Model 与 Brain/Compiler/Runtime/Context/Governance 交叉审查 | 待相关文档齐备 |
| Round 5 | 实现与运行验证 | 待原型和测试数据 |

---

**报告结束**
