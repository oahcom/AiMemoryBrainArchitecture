# Session D Review — Memory Brain 三方六维度独立架构审查报告

- 审查日期：2026-11-16
- 审查对象：Session D — Memory Brain
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 审查基线：`main` 分支本次读取到的仓库内容
- 审查类型：静态架构与跨文档契约审查
- 总体结论：**FAIL — 当前仓库缺少 Session D 核心设计交付物，无法证明 Memory Brain 已形成可审查、可实现的规范契约**
- 报告性质：三个专业视角的独立模拟审查，不代表三名真实审查人员或三个独立模型签署。

> 本报告不声称完成代码审计、渗透测试、数据库事务验证、故障注入或性能测试。由于 Session D 目录未出现在本次读取的仓库 main 分支中，针对 D 的具体实现细节只能标记为 NOT REVIEWABLE / 缺失，不得根据任务书或其他模块的描述推测其已经实现。

---

## 1. 审查范围与材料

### 1.1 本次实际读取的材料

| 类别 | 路径 | 本次状态 |
|---|---|---|
| 项目基线 | `README.md` | 已读取 |
| 路线图 | `ARCHITECTURE_ROADMAP.md` | 已读取 |
| 治理 | `00-governance/architecture-invariants.md` | 已读取 |
| 治理 | `00-governance/design-principles.md` | 已读取 |
| 治理 | `00-governance/terminology.md` | 已读取 |
| 系统架构 | `01-system-architecture/*` | 目录清单已读取；核心架构文件已读取 |
| 领域模型 | `02-domain-model/*` | 目录清单已读取；六份领域模型文件已读取 |
| Agent 集成 | `07-agent-integration/*` | 目录清单已读取；四份设计文件已读取 |
| A/B/C 集成审查 | `reviews/integration/phase-1-abc-cross-document-integration-review.md` | 已读取 |
| A 专项审查 | `reviews/architecture/2026-11-16-three-party-six-dimension-review.md` | 已读取 |
| B 专项审查 | `reviews/architecture/2026-11-16-memory-domain-model-three-party-six-dimension-review.md` | 已读取 |
| C 专项审查 | `reviews/07-agent-integration/three-party-six-dimension-review.md` | 已读取 |

主要已读取的系统/领域文件包括：
- `01-system-architecture/system-overview.md`
- `01-system-architecture/component-map.md`
- `01-system-architecture/component-interactions.md`
- `01-system-architecture/data-flows.md`
- `01-system-architecture/responsibility-matrix.md`
- `01-system-architecture/system-boundaries.md`
- `01-system-architecture/system-quality-attributes.md`
- `02-domain-model/domain-model-overview.md`
- `02-domain-model/core-entities.md`
- `02-domain-model/epistemic-and-temporal-semantics.md`
- `02-domain-model/lifecycle-model.md`
- `02-domain-model/relationships-and-provenance.md`
- `02-domain-model/scope-and-permission-model.md`

### 1.2 缺失材料（明确记录，不推测内容）

以下目录在本次读取的仓库 main 分支中返回 GitHub 404：

- `03-memory-brain/`
- `04-memory-compiler/`
- `05-memory-runtime/`
- `06-memory-context/`

本轮 D 的五份重点文件全部缺失：

| 文件 | 状态 |
|---|---|
| `03-memory-brain/memory-brain-overview.md` | MISSING |
| `03-memory-brain/canonical-memory-store.md` | MISSING |
| `03-memory-brain/memory-lifecycle-manager.md` | MISSING |
| `03-memory-brain/entity-and-relationship-manager.md` | MISSING |
| `03-memory-brain/memory-versioning.md` | MISSING |

此外：
- `reviews/03-memory-brain/` 不存在。
- 指定的 D 既有审查报告 `reviews/03-memory-brain/three-party-six-dimension-review.md` 不存在。
- E/F/G 的设计目录当前也未提交，故不能对 D 与 E/F/G 的真实文档接口作双向一致性确认。
- H（BMCP）与 I（Security/Governance）尚无本轮可供审查的专项设计目录；不能把 A/B/C 中的待办视为 H/I 已经交付。

缺失判断仅代表本次 main 分支可见仓库状态，不推断其他分支、未提交工作区或其他会话中的内容。

### 1.3 审查方法与限制

本轮采用三方视角模拟：
1. 系统架构师：职责、权威、边界、依赖方向。
2. 工程实现负责人：对象契约、事务、版本、状态机、并发与恢复。
3. 安全与可靠性审计者：Scope、Permission、Forget、Provenance、提示注入与数据残留。

六维度分别给出证据、判断和整改要求。三方是审查视角，不是三名真实独立人员。

---

## 2. 总体结论

### 2.1 最终结论：FAIL

当前不能给 Session D Pass 或 Conditional Pass，原因不是已经证明 D 的内部设计错误，而是 D 的核心设计文件在仓库中完全缺失，无法验证它是否履行了 A/B/C 已经明确分配给 Memory Brain 的规范责任。

本报告采用以下判定：

- **FAIL（本轮）**：核心交付物缺失，审查对象不可审查；阶段门禁不满足。
- 不将缺失文档内容臆测为设计缺陷。
- 不关闭或重写任何 A/B/C 的问题。
- 不把 A/B/C 的原则性承诺当成 D 已经提供的接口契约。

### 2.2 已确认的基线要求

仓库现有文档明确要求：

1. Memory Brain 是 Canonical Memory 的唯一逻辑权威；Canonical Store 是持久化与版本机制的权威执行位置，不能由 Compiler、Runtime 或索引建立第二权威。
2. Memory、Claim、Fact、Evidence、Entity、Relation、Event 的语义必须明确；Fact/Claim 当前存在上游 P0 冲突，不能由 D 擅自冻结。
3. Lifecycle State、Epistemic Status、Memory Version、Claim Revision 必须区分。
4. Scope 与 Permission 独立；对象身份与 Scope 绑定必须支持多 Agent、多 Environment。
5. Forget 是覆盖依赖对象与派生副本的治理工作流，不等同于删除主表记录、Archive 或 Context Remove。
6. Canonical Store 与索引/缓存分离；索引是可重建投影。
7. Memory 内容始终是不可信数据，不能获得 system/developer 指令权限。
8. 生命周期事件、版本历史、Provenance、索引更新和恢复必须有唯一权威及可恢复一致性协议。

这些是上游已有基线，不代表本次已经在 D 中验证到对应实现。

### 2.3 三方独立结论

| 审查视角 | 结论 | 核心理由 |
|---|---|---|
| 系统架构师 | FAIL / NOT REVIEWABLE | D 的五份核心文件缺失，无法核查 Canonical Memory 权威、组件边界、依赖方向和接口所有权 |
| 工程实现负责人 | FAIL / NOT REVIEWABLE | 无法核查 ID、Version、Revision、状态机、CAS、事务、幂等、Merge/Split 与恢复契约 |
| 安全与可靠性审计者 | FAIL / NOT REVIEWABLE | 无法核查 D 是否为每个对象提供 Scope、Evidence 权限继承、Forget 依赖发现与反复活机制 |

---

## 3. 六维度逐项审查

### 维度一：架构与职责边界

**结论：FAIL — D 的架构职责尚无可审查交付物。**

上游证据：
- `00-governance/architecture-invariants.md` I-01、I-04、I-13、I-20、I-21。
- `01-system-architecture/component-map.md` 的 MB-01 至 MB-04。
- `01-system-architecture/responsibility-matrix.md` 对 Domain Model、Canonical Store、Lifecycle、Entity/Relation 的 primary ownership。
- `01-system-architecture/component-interactions.md` 第 3、4、6 节。
- `01-system-architecture/system-boundaries.md` 第 3、4 节。
- `reviews/integration/phase-1-abc-cross-document-integration-review.md` 第 4、7、8 节。

已知应遵守的边界：
- Domain Model 定义语义，不拥有物理持久化。
- Canonical Store 负责 canonical records、versions 和 durable reads/writes。
- Lifecycle Manager 负责生命周期状态与转换策略执行。
- Entity & Relation Manager 负责身份解析、实体历史和关系一致性。
- Compiler 只提出候选，不得绕过 canonical/lifecycle authority。
- Runtime 只读取 canonical authority 的结果，不可创建第二权威。
- MCM 只拥有 Memory Context 及其版本序列，不拥有 Canonical Memory。

缺少的 D 证据：
- Brain 内部组件关系与依赖方向。
- Canonical authority 的正式定义及写入入口。
- Store、Lifecycle、Entity/Relation 的边界与协作协议。
- 多 Agent / 多 Environment 下的对象归属规则。
- 与 Compiler、Runtime、MCM、Agent Adapter 的明确依赖契约。

**架构判断：** 上游基线是合理的模块化逻辑架构，但不能据此判定 D 已正确实现。不得把 D 的逻辑子组件擅自解释为独立服务、独立 Agent Runtime 或必须独立 Rust crate。

### 维度二：领域模型与数据契约

**结论：FAIL — D 未提供可核验的领域持久化与生命周期契约；上游存在未关闭的 P0/P1。**

已知上游缺口：
- Fact / Claim 规范冲突（INT-P0-01 / DM-001）。
- Claim Identity 与 Revision 规则未决（INT-P1-02 / DM-003）。
- Conflict / Conflict Set 缺少完整规范对象（INT-P1-02 / DM-004）。
- Generic Scope 的统一对象结构未闭合（INT-P0-02、DM-005）。
- TypedObjectRef、ScopeRef、ActorRef、ContentRef、TimeValue、TimeInterval 等最小结构未闭合（INT-P1-06 / DM-006）。
- Entity Merge/Split 的迁移记录、审计与恢复对象不足（INT-P1-02 / DM-009）。
- Relation Revision / Retraction 的不可变历史与操作元数据需要补齐。
- Lifecycle 状态与 append-only lifecycle event 的权威路径未统一（INT-P1-06 / DM-008）。

D 必须提交并明确以下契约，而不是只复用对象名称：
1. Memory、Claim、Evidence、Entity、Relation、Event 的身份、字段、归属、Scope 和引用约束。
2. Memory ID 与 Memory Version ID 的区分；Version 序列、父版本、提交者、原因、摘要、内容摘要和创建时间。
3. Claim ID 跨 Memory Version 的稳定性策略，以及 Revision / successor / retraction 语义。
4. Conflict Set 的身份、成员、冲突维度、证据引用、裁决状态与裁决历史。
5. Entity Merge/Split 的源 ID、目标 ID、映射、引用迁移、回滚/纠错与审计。
6. Relation 的类型词汇版本、端点约束、Scope、有效时间、修订、撤回原因与操作者。
7. TypedObjectRef、ScopeRef、ActorRef、ContentRef、TimeValue、TimeInterval 的最小字段和未知值语义。
8. Fact/Claim ADR 未批准前，所有相关 Schema、API、存储结构必须显式标记 ADR-blocked，不得以候选方案冒充 DECIDED。

**特别裁定：Fact / Claim ADR**
- 现有 Domain Model Overview 第 5 节将 Claim 作为规范命题对象，并把 Fact 视作 Claim 的资格/解释，而治理基线 I-04、P-04 和 README 则将 Fact 与 Claim 并列。
- 集成审查已经明确要求 ADR 解决冲突。
- D 不拥有单方面覆盖治理基线的权限。
- 在 ADR 批准前，D 只能提供可兼容的候选接口和明确阻塞标记；不得冻结 Fact/Claim 的存储身份和对外语义。

### 维度三：数据流与一致性

**结论：FAIL — 无法验证 Canonical Commit、版本历史与 Lifecycle 的唯一权威。**

上游证据：
- `01-system-architecture/component-interactions.md` 第 4.3、4.4、6、9 节。
- `02-domain-model/domain-model-overview.md` 第 10 节。
- `02-domain-model/lifecycle-model.md` 第 7、10 节。
- `02-domain-model/relationships-and-provenance.md` 第 8 节。
- A 审查 AR-004。
- 集成审查 INT-P1-06。

D 必须明确：
- Canonical Commit 的原子提交边界：Memory/Claim/Entity/Relation/Provenance/Lifecycle 状态中哪些必须同事务提交。
- Version immutable；current pointer 的唯一推进者及 CAS / expected-version 规则。
- 同幂等键同 payload 返回原结果；同键不同 payload 必须拒绝并返回冲突。
- 并发修改不得 last-write-wins 覆盖；stale writer 必须显式 Conflict。
- Lifecycle State 是 Memory Version 的字段权威，还是 append-only lifecycle event 的投影权威；只能存在一个规范权威，另一种必须定义为可重建表示。
- Entity Merge/Split 后旧 ID、旧 Relation、Claim 引用、Provenance 边、Index 投影和历史查询的迁移规则。
- Canonical commit 与 outbox/change event 的可恢复关系；commit 成功但发布失败必须可重放。
- Index/Cache 的 generation/watermark、stale-read fence、重建和回放规则。
- Forget 与并发写入的冲突规则：Forget fence 生效后，旧写入、重放、离线任务和延迟编译不得使内容重新可见。

Provenance：
- B 文档仍将 DAG 与受限循环规则列为 OPEN。
- D 不得假设依赖图必然无环，也不得在未定义边界时宣称 Forget 依赖发现完整。
- 应给出 acyclic invariant 或明确受限 cycle 语义、遍历终止条件、深度/节点限制和失败时的部分状态。

### 维度四：安全与治理

**结论：FAIL — 上游安全原则存在，但 D 的逐对象执行契约缺失。**

#### Scope / Permission
每个 canonical 对象及关联记录必须有明确 Scope 绑定或明确继承规则。Scope 不等于 Permission。至少要覆盖 Memory、Memory Version、Claim/Revision、Evidence、Provenance、Entity、Relation、Conflict、Lifecycle Event、Merge/Split Record、Forget Operation。

必须明确：
- 身份来自可信 Principal/Actor 解析，不信任 Agent 自报 Scope 或 display name。
- 读写、关系扩展、Evidence dereference、状态转换和异步任务执行都进行授权。
- Entity Resolution / Merge 不得跨 Scope 自动合并；跨 Scope 合并必须有显式 sharing grant、授权决策和审计。
- Memory 可读不意味着 Evidence 原文可读；Evidence 必须单独授权。
- Scope 过滤应在候选生成、图扩展、重排、聚合、缓存、Working Set 和 Context 之前生效，不能只在最终输出过滤。

#### Forget
`02-domain-model/lifecycle-model.md` 第 8 节已提出依赖发现、访问阻断、异步清理、投影失效和完成验证的方向，但 D 的执行契约未提交。

D 应与 I/E/F/G/H 明确覆盖：
- 所有 Memory Versions、Claim revisions、Evidence、Provenance、Entity/Relation 引用与派生 Memories。
- 索引、向量、图投影、缓存、Working Set、Context Entry、Change Set、离线 Adapter 副本、备份与快照。
- 依赖发现水位、阻断时点、阶段状态、重试、幂等、完成证据和残留例外。
- 并发写入和历史回放的 Forget fence。
- Tombstone 只能保留不违反删除政策的最小元数据，不能重建被忘记内容。
- 外部模型/第三方副本必须标记 Brain 无法单方面保证的边界；不得虚假承诺物理删除。

删除主表记录不构成 Forget 完成。

#### Memory Prompt Injection
- Memory、Evidence、Telemetry、Provenance 中的文本全部是不可信数据。
- 保留来源、Trust、Epistemic Status、Evidence 与 derivation lineage。
- Memory 内容不能获得系统/开发者指令权限，也不能赋予工具调用授权。
- 文本 delimiter 不是安全边界；应与 Agent 自身安全策略协同。
- 恶意记忆、伪造 system 标签、跨 Scope 记忆、多轮间接注入必须进入后续对抗性测试。
- 本轮未执行任何提示注入测试。

### 维度五：性能与资源

**结论：PARTIAL（基线方向可接受，D 的性能契约缺失）。**

上游 `01-system-architecture/system-quality-attributes.md` 要求用代表性 workload 和硬件进行可复现实验，未允许提前宣称固定延迟或吞吐量。

D 的设计至少应给出可测量的复杂度与资源边界：
- Canonical Store 的读写路径、批量提交和事务范围。
- Memory Version 历史增长、压缩/归档策略和历史查询成本。
- Entity/Relation 图规模、fan-out、分页和截断语义。
- Provenance 深度、节点数、遍历预算与部分结果标记。
- Conflict detection 的候选窗口与时间重叠处理成本。
- Merge/Split 的引用迁移规模、批次、恢复和后台任务优先级。
- Forget 的依赖发现成本、分页、水位、重试与长任务进度。
- 热/冷数据策略、索引重建和存储增长。
- Scope/Permission 校验不可因性能优化而被绕过。

**TO_VALIDATE：** 所有实际延迟、吞吐、容量、资源占用和本地硬件可行性。当前没有任何运行基准数据，不能宣称达到特定 SLO。

### 维度六：可演进性与可观测性

**结论：FAIL（D 交付缺失；规范要求未能在 D 层核验）。**

D 必须定义或引用统一策略：
- Schema Version 与 Memory Version、Claim Revision、Relation Revision 的区别。
- Relation Vocabulary / Event Kind / Evidence Kind / Scope Kind 的版本化、弃用和兼容策略。
- 历史版本如何解释；迁移是否产生新版本；旧 Schema 读取失败如何处理。
- 领域事件、Lifecycle Event、Merge/Split、Forget 的审计字段。
- correlation_id / causation_id 如何贯穿 Event → Evidence → Provenance → Claim → Memory Version → Index Generation → Retrieval。
- 错误分类：NOT_FOUND、SCOPE_MISMATCH、PERMISSION_DENIED、INVALID_TRANSITION、STALE_VERSION、CONFLICT、IDEMPOTENCY_KEY_REUSE、FORGET_IN_PROGRESS 等是否有稳定语义。
- 高影响操作如何关联 Actor、Scope、Policy Version、Operation ID、Idempotency Key、Expected Version、Result Version。
- 日志不得复制敏感 Evidence 或被忘记的内容；审计保留与 Forget 的边界必须明确。

---

## 4. 逐文件审查矩阵

| 文件 | 本次状态 | 结论 | 说明 |
|---|---|---|---|
| `03-memory-brain/memory-brain-overview.md` | MISSING | FAIL | 无法验证 Brain 权威、组件职责与跨模块边界 |
| `03-memory-brain/canonical-memory-store.md` | MISSING | FAIL | 无法验证 canonical schema、事务、并发、幂等、索引投影分离 |
| `03-memory-brain/memory-lifecycle-manager.md` | MISSING | FAIL | 无法验证状态机、非法转换、Forget 与 Lifecycle 唯一权威 |
| `03-memory-brain/entity-and-relationship-manager.md` | MISSING | FAIL | 无法验证 Entity Resolution、Merge/Split、Relation revision 与 Scope 约束 |
| `03-memory-brain/memory-versioning.md` | MISSING | FAIL | 无法验证 Memory Version、Claim Revision、历史查询和回放 |
| `reviews/03-memory-brain/three-party-six-dimension-review.md` | MISSING | FAIL | 本轮指定交付报告不存在；本文件为创建目标 |

上游文件矩阵：

| 文件 | 审查结果 | 关键发现 |
|---|---|---|
| `00-governance/architecture-invariants.md` | PARTIAL | I-04 Fact/Claim 与 Domain Model 存在冲突；I-13/I-20 需要 D 提供执行契约 |
| `00-governance/design-principles.md` | PARTIAL | P-04 Fact/Claim 冲突；P-13 Forget 原则尚未有 D 执行契约 |
| `00-governance/terminology.md` | PARTIAL | 术语区分清晰，但不足以替代 D 的规范 schema |
| `01-system-architecture/component-map.md` | PASS（基线） | MB-01 至 MB-04 职责边界已给出 |
| `01-system-architecture/responsibility-matrix.md` | PASS（基线） | Primary ownership 基本清晰 |
| `01-system-architecture/component-interactions.md` | PARTIAL | Compiler→Canonical authority、Canonical→Index 的逻辑交互存在；D 的具体写入契约缺失 |
| `01-system-architecture/system-boundaries.md` | PARTIAL | 权威、信任和 Scope 原则明确；D 的逐对象落地不可核验 |
| `02-domain-model/domain-model-overview.md` | PARTIAL | Claim 规范决策与治理基线冲突；多项核心类型和身份规则 OPEN |
| `02-domain-model/lifecycle-model.md` | PARTIAL | 状态语义已有；状态存储权威、Forget 完成边界仍 OPEN |
| `02-domain-model/relationships-and-provenance.md` | PARTIAL | 关系/Evidence/Provenance 语义较完整；DAG/循环与 Merge/Split 迁移仍需契约 |
| `02-domain-model/scope-and-permission-model.md` | PARTIAL | Scope/Permission 分离明确；通用 Scope 与全链路过滤需补齐 |
| `reviews/integration/phase-1-abc-cross-document-integration-review.md` | PASS（作为审查依据） | 明确列出 INT-P0-01..04、INT-P1-01..06；均不能因 D 开始设计而自动关闭 |
| A/B/C 专项审查报告 | PASS（作为审查依据） | 已识别上游风险；不代表 D 已解决这些问题 |

---

## 5. P0 / P1 / P2 / P3 问题清单

### P0 — 阻断项

#### D-REV-P0-01 — Session D 核心设计交付物缺失

- **Severity:** P0
- **File / Section:** `03-memory-brain/*`（目录与五份核心文件均缺失）
- **Evidence:** 本次 main 分支目录读取中，`03-memory-brain` 返回 404；指定五份文件均不可读取。
- **Problem:** 无法确认 Memory Brain 是否定义 Canonical Memory 唯一权威、Store/Lifecycle/Entity/Relation/Version 契约。
- **Impact:** E/F/G 无法依赖 D 的规范接口实现；核心数据权威和状态语义只能从 A/B 的概念性文档猜测，可能造成重复权威、不同 ID 语义和不可恢复的数据分叉。
- **Required Correction:** 提交任务书要求的五份 D 设计文件；每份标记 DECIDED/CANDIDATE/TO_VALIDATE/OPEN，并提供输入输出、数据契约、状态机、事务、失败恢复、安全、性能测量和验收条件。
- **Owner:** Session D Principal Architect
- **Dependency:** A/B 基线；INT-P0-01 至 INT-P0-04；INT-P1-02、INT-P1-06。
- **Acceptance Criteria:** 五份文件全部存在；核心权威和接口边界明确；不存在将候选设计伪装为决议；E/F/G 可直接引用 D 的对象和操作语义，不需要自行猜测。

#### D-REV-P0-02 — 上游 Fact / Claim 规范冲突尚未有批准 ADR

- **Severity:** P0（继承上游阻塞项；不是本轮新发现的 D 内部缺陷）
- **File / Section:** `00-governance/architecture-invariants.md` I-04；`00-governance/design-principles.md` P-04；`02-domain-model/domain-model-overview.md` 第 5 节；`reviews/integration/phase-1-abc-cross-document-integration-review.md` 第 4 节
- **Evidence:** 治理基线将 Fact 与 Claim 并列为不同概念；Domain Model 则把 Fact 解释为 Claim 的资格/解释而非独立对象。集成审查明确要求 ADR。
- **Problem:** 核心对象身份与 schema 语义冲突。
- **Impact:** Store、Compiler、Runtime、API、历史版本和测试可能实现两套互不兼容模型。
- **Required Correction:** 由 Architecture Governance + B 建立并批准 ADR；D/E/F 同步评估 Store、写入、索引、检索和历史影响。批准前所有相关 schema 标记 ADR-blocked。
- **Owner:** Architecture Governance + Session B；Session D/E/F 为影响评估方。
- **Dependency:** INT-P0-01。
- **Acceptance Criteria:** ADR 有明确选项、权衡、批准记录；基线文档同步；D 的 schema 与 ADR 一致；不存在未经授权的局部定义。

### P1 — 核心契约阻断项

#### D-REV-P1-01 — Canonical Commit、Memory Version 与 Lifecycle 双权威风险未在 D 层闭合

- **Severity:** P1
- **File / Section:** D 缺失；上游 `02-domain-model/lifecycle-model.md` 第 7、10 节；`02-domain-model/domain-model-overview.md` 第 10 节
- **Evidence:** B 允许生命周期语义进入 Memory Version 或 append-only lifecycle event；集成审查 INT-P1-06 要求明确唯一权威。
- **Problem:** 尚无 D 契约说明生命周期状态与不可变版本/事件记录的唯一权威关系。
- **Impact:** current state、历史回放、索引投影可能出现分歧。
- **Required Correction:** 明确一个规范权威及另一表示的派生规则；规定 commit 原子边界、CAS、outbox 和恢复。
- **Owner:** Session D
- **Dependency:** B / INT-P1-06 / A AR-004
- **Acceptance Criteria:** 生命周期变更可唯一重建；并发、崩溃重放、索引滞后均有明确语义和验收用例。

#### D-REV-P1-02 — Claim Identity / Revision / Conflict Set 缺少 D 侧提交契约

- **Severity:** P1
- **File / Section:** D 缺失；`02-domain-model/domain-model-overview.md` 第 7、10、12 节；B 审查 DM-003、DM-004
- **Evidence:** Claim ID 跨 Memory Version 的策略 OPEN；Conflict Set 结构未定义。
- **Problem:** D 尚无可审查的 Claim 修订、冲突成员和历史引用策略。
- **Impact:** 历史查询、撤回、证据链接、索引增量、冲突裁决与 Runtime 过滤不稳定。
- **Required Correction:** 定义稳定 Claim identity 与 immutable revision/successor 方案；定义 Conflict Set 的身份、参与者、证据、维度、裁决历史和状态；Fact/Claim ADR 未决部分保持阻塞。
- **Owner:** Session B 定义语义；Session D 负责 Store/Lifecycle 契约；E/F 参与。
- **Dependency:** INT-P1-02、INT-P0-01。
- **Acceptance Criteria:** 同一 Claim 在多 Memory Version 中的引用语义确定；并发修订、撤回、冲突和历史查询可测试。

#### D-REV-P1-03 — Scope 与 Permission 未形成 D 对每种 canonical 对象的约束表

- **Severity:** P1
- **File / Section:** D 缺失；`02-domain-model/scope-and-permission-model.md`；`01-system-architecture/system-boundaries.md` 第 4、5 节
- **Evidence:** 上游要求 Scope 与 Permission 分离，但 Generic Scope 身份和逐对象继承规则仍未完整。
- **Problem:** 无法验证 Memory、Version、Claim、Evidence、Provenance、Entity、Relation、Conflict、Lifecycle Event 等对象的 Scope 绑定和授权边界。
- **Impact:** 跨用户、项目、Agent、Agent Instance、Session、Environment 的引用混淆和越权读取/合并风险。
- **Required Correction:** 提供对象级 Scope binding / inheritance matrix；定义 cross-scope reference 与显式 sharing grant；Entity Resolution/Merge 强制 scope compatibility 和操作授权；Evidence 单独授权。
- **Owner:** Session D + Session B；Session I 主责治理策略。
- **Dependency:** INT-P0-02、DM-005、DM-010。
- **Acceptance Criteria:** 每种对象均有明确 Scope 规则；跨 Scope 读取、图扩展、Merge、Evidence dereference 的负向测试全部拒绝且不泄露元数据。

#### D-REV-P1-04 — Forget Operation 与依赖发现/完成证明缺少 D 侧领域契约

- **Severity:** P1（与上游 P0-03 联动）
- **File / Section:** D 缺失；`02-domain-model/lifecycle-model.md` 第 8、10 节；`02-domain-model/relationships-and-provenance.md` 第 9 节
- **Evidence:** B 已描述 Forget 的概念流程，但 backup expiry、外部副本、Provenance cycle 等仍 OPEN。
- **Problem:** D 未提供 Forget Operation 身份、依赖水位、阶段、访问阻断、幂等、完成证明与残留例外的规范对象/接口。
- **Impact:** 删除主记录后，历史版本、Evidence、派生 Memory、索引、缓存或 Context 可能仍可恢复/检索；并发重放可能复活内容。
- **Required Correction:** 定义 Forget Operation/Job、dependency discovery、deny fence、per-target progress、retry/idempotency、completion evidence、residual exception；与 E/F/G/H/I 明确数据层责任。
- **Owner:** Session I 主责治理；Session D 定义 canonical object/lifecycle/dependency 语义；E/F/G/H 落地各自副本清理。
- **Dependency:** INT-P0-03、INT-P1-06、DM-007、DM-011。
- **Acceptance Criteria:** Forget fence 后普通访问立即受阻；所有登记依赖可发现；失败可恢复但不得提前报告完成；历史重放/并发写入不得复活；审计不保留可重建内容。

#### D-REV-P1-05 — Entity Merge/Split、Relation Revision 与引用迁移缺少可恢复操作契约

- **Severity:** P1
- **File / Section:** D 缺失；`02-domain-model/relationships-and-provenance.md` 第 3、8、11 节；B 审查 DM-009
- **Evidence:** B 要求 Merge/Split 产生迁移记录，但尚无完整操作对象字段与恢复协议。
- **Problem:** 缺少旧/新 ID 映射、引用迁移范围、证据、操作者、版本、回滚/纠错和索引重建契约。
- **Impact:** Entity 误合并可能污染跨任务长期记忆；Split 后旧引用、Relation、Provenance 和 Context 可能指向错误身份。
- **Required Correction:** 定义 Merge/Split Operation 与 immutable audit record；限定 Scope；定义 redirects/aliases、引用迁移、双读/历史查询、纠错和投影重建。
- **Owner:** Session D；Session B 定义领域语义；F/G 消费变更。
- **Dependency:** INT-P1-02、DM-009、INT-P0-02。
- **Acceptance Criteria:** Merge/Split 可审计、可恢复/纠错；历史版本保持可解释；跨 Scope 合并默认拒绝；所有受影响投影可重建。

#### D-REV-P1-06 — E/F/G/H/I 所需的 D 接口尚不可消费

- **Severity:** P1
- **File / Section:** D 五份核心文件均缺失；上游 `01-system-architecture/component-interactions.md` 第 10 节；集成审查第 7、8 节
- **Evidence:** 上游已把 Candidate→Canonical、Canonical→Retrieval、MCM references、Governance/Forget 等责任分配给 D，但 D 接口文档不存在。
- **Problem:** 没有稳定的 canonical IDs、version references、scope fields、write result、lifecycle events、entity migration events 和 Forget semantics 可供下游使用。
- **Impact:** E 可能自创候选提交协议；F 可能猜测过滤字段/状态；G 可能猜测 Memory 引用和撤回通知；H/I 无法稳定定义 wire 与治理操作。
- **Required Correction:** 提供 D-owned contract section：Candidate acceptance/write transaction、canonical read reference、version/lifecycle event、entity/relation change event、Forget notification/fence、error taxonomy、idempotency/concurrency semantics。
- **Owner:** Session D；E/F/G/H/I 为消费者与联合审查方。
- **Dependency:** INT-P1-01、INT-P1-02、INT-P1-06；INT-P0-02/03。
- **Acceptance Criteria:** E/F/G/H/I 能仅依赖已发布 D 契约完成接口映射；不得依赖私有实现细节或自行猜测语义。

### P2 — 性能、可演进性与可观测性

#### D-REV-P2-01 — 图与 Provenance 遍历预算未能从 D 验证

- **Severity:** P2
- **File / Section:** D 缺失；`02-domain-model/relationships-and-provenance.md` 第 8、10、11 节
- **Evidence:** B 将 lineage depth/fan-out 和 Forget dependency traversal 列为 TO_VALIDATE。
- **Problem:** D 尚无分页、截断、最大深度/节点、超时与部分结果语义。
- **Impact:** 高 fan-out 图与长 lineage 可能导致不受控资源消耗或 Forget 长任务阻塞。
- **Required Correction:** 提供候选复杂度边界和测量计划，不预设未测数值。
- **Owner:** Session D + F + I
- **Dependency:** INT-P0-03、INT-P1-06。
- **Acceptance Criteria:** 查询/依赖遍历具有显式资源预算、部分结果状态和可观测进度；有代表性负载基准计划。

#### D-REV-P2-02 — 领域事件与审计关联字段未能从 D 验证

- **Severity:** P2
- **File / Section:** D 缺失；`01-system-architecture/system-quality-attributes.md` 第 9 节
- **Evidence:** 上游要求 correlation/causation、actor、scope、version/generation、stage、attempt 和 timestamps。
- **Problem:** 无法核查 D 的 Lifecycle、Merge/Split、Forget、Version commit 是否携带统一追踪字段。
- **Impact:** 线上问题定位、审计追溯和跨模块回放困难。
- **Required Correction:** 定义高影响领域事件 envelope、稳定错误分类和敏感字段脱敏规则。
- **Owner:** Session D + I + H
- **Dependency:** INT-P1-06。
- **Acceptance Criteria:** 关键写操作可从请求追踪到 commit、projection、通知和审计；敏感内容不进入普通日志/指标。

#### D-REV-P2-03 — Schema/Vocabulary 演进与历史迁移契约未能验证

- **Severity:** P2
- **File / Section:** D 缺失；B 审查 DM-013；`ARCHITECTURE_ROADMAP.md` Phase 3/4
- **Evidence:** Relation vocabulary、枚举兼容、历史 Schema 解释和迁移策略仍待定义。
- **Problem:** D 未说明新增/弃用字段、未知枚举、数据迁移和历史版本解释规则。
- **Impact:** 长期演进可能导致旧 Memory 无法读取，或不同模块对同一枚举解释不一致。
- **Required Correction:** 定义 Schema version、Vocabulary version、兼容规则、迁移和回滚原则。
- **Owner:** Session D + B + H
- **Dependency:** INT-P1-06。
- **Acceptance Criteria:** 旧版本读取/迁移有明确策略；未知核心语义不会被静默误解释；历史内容仍可审计。

### P3 — 文档与协作改进

#### D-REV-P3-01 — D 审查交付目录及文档索引缺失

- **Severity:** P3（但不降低 P0-01 的阻断等级）
- **File / Section:** `reviews/03-memory-brain/`、`README.md` Documentation map
- **Evidence:** 本次仓库目录清单未见 D 设计目录及其审查目录。
- **Problem:** 审查产物无法按预定路径发现，文档索引也无法体现实际完成状态。
- **Impact:** 后续会话容易基于过期或不存在的材料协作。
- **Required Correction:** D 交付后更新目录/索引状态；本报告仅创建于指定审查路径，不修改 README 或 D 文件。
- **Owner:** Session D / Repository Maintainer
- **Dependency:** D-REV-P0-01。
- **Acceptance Criteria:** 文档路径存在且索引状态与仓库真实状态一致。

---

## 6. 强制跨模块接口审查

由于 D 文件缺失，以下是基于上游职责分配的**契约缺口判断**，不是对未提交模块实现的审计。

### 6.1 对 E — Memory Compiler

**结论：FAIL / 接口不可消费。**

D 必须明确：
- Candidate Memory/Claim/Entity/Relation/Evidence/Provenance proposal 的输入 envelope。
- canonical acceptance/rejection/defer 结果及其 ID/version。
- 写入事务的原子范围；Provenance 与 target version 的可见性保证。
- Conflict Set、Claim Revision、Entity resolution proposal 的提交语义。
- idempotency key、payload digest、重复提交和同键异 payload 行为。
- Compiler 不得绕过 Lifecycle Manager 直接修改 canonical state。

### 6.2 对 F — Memory Runtime

**结论：FAIL / 接口不可消费。**

D 必须明确：
- 稳定 Memory ID、Version ID、Claim Revision 和 TypedObjectRef。
- Scope 过滤所需的规范字段及跨 Scope share 语义。
- Entity/Relation/Temporal 查询可用的稳定类型与历史引用。
- Active / Superseded / Archived / Forgotten 与 Claim Disputed / Retracted 对默认检索的影响。
- Evidence 按权限展开的接口和拒绝语义。
- Index generation 与 canonical version 的 freshness fence。

### 6.3 对 G — Memory Context Manager

**结论：PARTIAL（责任边界可由 A/B 确认，D 的引用与通知契约缺失）。**

D 必须明确：
- Context Entry 引用 Memory ID + immutable Version ID（或受控 rendering ref）的规范形式。
- Memory 新版本、Superseded、Retracted、Archived、Forgotten 如何向 MCM 发出可恢复变更通知。
- Entity Merge/Split 后 Context Entry 的 reconcile/invalidation 语义。
- Canonical Memory Version 与 Context Version 完全分离；D 不得成为 Context Version 权威。
- Forget fence 发生后 G 如何阻断旧引用、待投递 delta 与离线缓存的再次应用。

### 6.4 对 H — BMCP

**结论：PARTIAL（系统边界明确，wire-safe contract 未能从 D 验证）。**

D 应提供稳定领域引用和语义，不应直接把内部数据库行、Rust 类型或私有状态机结构暴露为不稳定 Wire Model。H 应负责 wire envelope、兼容和编码；D 负责领域语义、稳定标识、错误含义和操作结果。

### 6.5 对 I — Security / Governance

**结论：FAIL / 治理执行所需领域支撑未能从 D 验证。**

D 必须提供：
- 每种 canonical object 的 Scope binding。
- Forget Operation、依赖关系、阻断 fence、完成状态和 residual exception。
- Entity Merge/Split 的授权与跨 Scope 限制。
- Evidence/Provenance 的独立访问检查。
- Lifecycle/Version 历史清理或去标识化的可治理边界。
- 审计记录不保留可恢复的已忘记内容。

---

## 7. 强制问题 ID 状态矩阵

状态说明：
- PASS：本次材料有充分证据证明该项满足。
- PARTIAL：有原则或局部语义，但关键执行契约未闭合。
- FAIL：存在明确冲突，或本轮要求的关键契约/交付缺失。
- NOT APPLICABLE：该问题不属于 D 的职责范围；本矩阵不轻易使用该状态。

### 7.1 INT 问题

| ID | 状态 | 证据与理由 |
|---|---|---|
| INT-P0-01 | FAIL | Fact/Claim 基线冲突仍在；无批准 ADR，D 文件缺失，无法验证 ADR-blocked schema |
| INT-P0-02 | FAIL | A/B 已定义 Scope/Permission 原则，但 D 对象级 Scope 契约缺失；不能验证 canonical 访问与 Merge 的隔离 |
| INT-P0-03 | FAIL | B 有 Forget 概念流程；D 的 Forget Operation、canonical dependency/fence/完成证明契约缺失 |
| INT-P0-04 | PARTIAL | A/B/C 基线明确 Memory 是不可信数据；D 未提供来源/信任/派生信息的 canonical 保存与下游消费契约 |
| INT-P1-01 | PARTIAL | Context Version 主权已归 G/MCM；D 应提供稳定 Memory reference 与变更通知，但未提交 |
| INT-P1-02 | FAIL | Claim Revision、Conflict Set、Entity Merge/Split 是 D/B 的关键协作契约；B 标记 OPEN，D 缺失 |
| INT-P1-03 | PARTIAL | 主要由 C/B/E/H/I 负责；D 需消费稳定 Event/Actor/Scope/Evidence 语义，但本轮无 D 接口可核验 |
| INT-P1-06 | FAIL | Lifecycle 唯一权威、Provenance DAG、Typed References、Canonical commit/outbox/index watermark 均未由 D 闭合 |

### 7.2 A — System Architecture 审查问题

| ID | 状态 | 证据与理由 |
|---|---|---|
| A: AR-001 | FAIL | Forget 全链路依赖发现与完成证明是 D 必须支撑的 canonical 契约；D 未提交。上游已要求覆盖派生对象和副本 |
| A: AR-002 | PARTIAL | 全局不可信 Memory 原则存在；D 的 canonical 来源/信任/epistemic 元数据保存契约不可核验 |
| A: AR-003 | FAIL | Scope 隔离原则存在，但 D 对象级 Scope 绑定与关系解析/合并授权契约缺失 |
| A: AR-004 | FAIL | Lifecycle State 与 Version/Event 的唯一权威尚未由 D 明确；集成审查 INT-P1-06 明确要求解决 |
| A: AR-006 | FAIL | Entity/Claim identity 与跨版本引用、Merge/Split 的一致性契约未提交 |

### 7.3 B — Domain Model 审查问题

| ID | 状态 | 证据与理由 |
|---|---|---|
| B: DM-001 | FAIL | Fact/Claim 冲突未获 ADR 解决；不得冻结相关 schema |
| B: DM-002 | PARTIAL | Context Version/Change Set 由 G 主责；D 仍须提供稳定 canonical version reference，但未提交 |
| B: DM-003 | FAIL | Claim identity/revision OPEN；D 未给出存储/历史策略 |
| B: DM-004 | FAIL | Conflict/Conflict Set 未形成完整规范对象；D 未提交持久化契约 |
| B: DM-005 | FAIL | Generic Scope 不完整；D 未提交逐对象绑定/继承规则 |
| B: DM-006 | FAIL | TypedObjectRef、TimeValue、TimeInterval、ContentRef、ActorRef 等最小 Schema 未由 D/B 闭合 |
| B: DM-007 | FAIL | Provenance DAG/循环规则仍 OPEN；Forget 依赖发现不可据此证明完整 |
| B: DM-008 | FAIL | Lifecycle Version/Event 双路径权威问题未解决 |
| B: DM-009 | FAIL | Entity Merge/Split 与 Relation 撤回的审计/迁移契约不足 |
| B: DM-010 | PARTIAL | 上游有 scope-before-candidate 原则，但 D 的 canonical scope 与关联对象约束未交付 |
| B: DM-011 | FAIL | Forget 外部副本/备份边界仍 OPEN；D 未提供 canonical Forget 支撑契约 |
| B: DM-012 | PARTIAL | 上游已要求测量复杂度；D 未交付遍历/批量/长任务预算 |
| B: DM-013 | PARTIAL | 上游有 schema/vocabulary 演进方向；D 的迁移、事件与可观测契约缺失 |

> 这些状态是对“D 本轮能否提供所需契约/上游问题是否已解决”的判定，不是把所有 B 的问题重新归责给 D。DM-001/005/006/007 等需要 B、治理或 I 联合决策，D 不能单方面关闭。

---

## 8. DECIDED / CANDIDATE / TO_VALIDATE / OPEN 清单

### 8.1 当前可继承的 DECIDED（上游基线，不等于 D 已交付）

- Brain 是 Canonical Memory 的逻辑权威。
- Domain Model 定义语义；Canonical Store 负责持久化机制。
- Compiler 提交候选，不得绕过 Lifecycle authority。
- Memory Version immutable；更新通过新版本与 expected-version/CAS 语义。
- Lifecycle 与 Epistemic Status 分离。
- Scope 与 Permission 分离。
- Evidence 权限可比 Memory 更严格。
- Memory 内容是不可信数据，不得成为 system/developer instruction。
- Context Remove 不等于 Forget。
- Forget 是跨 canonical/derived representations 的治理工作流。
- Index/Cache/Working Set 是派生表示，不是 Canonical authority。
- 逻辑组件边界不强制等于独立服务或 Rust crate。
- 未经测量不得承诺性能数字。

### 8.2 CANDIDATE（不可当作冻结决议）

- Canonical directed relation + query-time inverse traversal。
- Outbox-backed canonical change publication 或等效可恢复机制。
- Memory Version 与 lifecycle event 的具体持久化组合（但必须只有一个规范权威）。
- Claim identity 使用 stable ID + immutable revision 或 successor 的具体方案。
- Provenance graph representation 与 lineage compaction。
- Forget 的物理删除/加密擦除和备份清理技术。
- Entity Merge/Split 的 redirect、alias 与迁移实现策略。

### 8.3 TO_VALIDATE

- Canonical Store 的读写与批量事务成本。
- Version 历史增长与历史查询性能。
- Entity/Relation fan-out、Merge/Split 迁移成本。
- Provenance 深度与依赖发现成本。
- Forget 大规模清理的吞吐、恢复时间和资源峰值。
- Index rebuild 与 replay 成本。
- 目标本地硬件上的存储、缓存与并发容量。

### 8.4 OPEN / BLOCKED

- Fact vs Claim ADR。
- Claim ID 跨版本身份与 revision 语义。
- Conflict Set 规范结构。
- Generic Scope 规范对象与继承/组合边界。
- TypedObjectRef / ScopeRef / ActorRef / ContentRef / TimeValue / TimeInterval 最小契约。
- Provenance DAG 或受限循环规则。
- Lifecycle 状态的唯一规范权威。
- Forget Operation 的完成定义、备份与外部副本边界。
- Entity Merge/Split 的迁移/纠错/审计协议。
- D 到 E/F/G/H/I 的稳定接口。

---

## 9. 修复顺序与退出条件

### Gate 0 — 恢复 D 的可审查交付物

1. 提交五份 D 核心设计文件。
2. 在每份文件中标记 DECIDED/CANDIDATE/TO_VALIDATE/OPEN。
3. 给出文件内章节与跨模块问题 ID 的映射。
4. 不得覆盖 A/B/C 或公共治理文件。

**退出条件：** 五份文件均可在 main 分支读取，目录与索引一致。

### Gate 1 — 领域基线与身份决策

1. 由 Architecture Governance + B 解决 Fact/Claim ADR。
2. 由 B/D 联合明确 Claim identity/revision、Conflict Set、Typed References。
3. 明确 Generic Scope 和 Entity/Relation Scope compatibility。
4. D 明确 Version 与 Lifecycle 的唯一权威。

**退出条件：** 不存在核心对象身份冲突；相关 schema 不再伪装未决决策为 DECIDED。

### Gate 2 — Canonical Commit 与历史一致性

1. 明确写入事务、CAS、幂等和冲突返回。
2. 明确 Memory Version、Claim Revision、Lifecycle Event 的关系。
3. 明确 Provenance visibility 与 canonical commit 原子性。
4. 明确 outbox/replay、index watermark 和恢复。
5. 明确 Merge/Split 的引用迁移和纠错。

**退出条件：** 并发、重复、崩溃恢复和历史回放具有可测试的确定语义。

### Gate 3 — Scope / Forget / Injection 安全门禁

1. 每种 canonical 对象有 Scope 绑定/继承表。
2. Entity Resolution/Merge 有授权和 Scope 兼容约束。
3. Evidence 独立授权。
4. Forget Operation 有依赖发现、访问阻断、逐目标清理、完成证明与残留例外。
5. Forget fence 与并发写入、异步重放、离线缓存协调。
6. 保留来源、Trust、Epistemic Status、Evidence 与 provenance lineage。

**退出条件：** 领域契约能够支持 I 的治理规则与负向测试；不得以删除主表记录替代 Forget。

### Gate 4 — E/F/G/H/I 接口冻结

1. E 能提交候选并得到规范 canonical result。
2. F 能依据稳定 Memory/Version/Scope/Claim/Relation 状态执行检索。
3. G 能引用 canonical version 并收到生命周期/Forget/Entity migration 变更。
4. H 能使用稳定领域引用构造 wire contract，不暴露私有实现类型。
5. I 能依据 D 对象和操作模型实施授权、Retention、Forget 与审计。

**退出条件：** 下游不再需要猜测 D 的 ID、版本、状态、Scope、错误和事件语义。

### Gate 5 — 静态复审与后续验证

- 重新执行三方六维度静态审查。
- P0 全部关闭；阻断契约冻结的 P1 全部关闭或通过正式 ADR 明确处置。
- 之后再开展实现审查、性质测试、故障注入、渗透测试与性能基准。
- 不得把本轮静态审查结论描述为已完成上述运行验证。

---

## 10. 未验证事项与审查局限

本轮没有：
- 审计 Rust 源码、数据库 DDL、事务实现或并发控制代码。
- 执行 Entity Resolution / Merge / Split 测试。
- 执行 Scope 越权测试或跨租户渗透测试。
- 执行 Forget、备份清理、缓存失效或复活攻击测试。
- 执行 Prompt Injection 对抗测试。
- 执行 Provenance cycle / graph traversal 测试。
- 执行存储容量、延迟、吞吐、CPU/RAM/GPU 或恢复时间基准。
- 验证未提交分支、未提交文件或其他会话中的 D 文档。

因此，本报告的 FAIL 是**仓库交付与架构契约可审查性失败**，不是对不存在的 D 设计内容作出的虚构技术定罪。

---

## 11. 最终裁决

**Session D：FAIL — Not Reviewable / Core Deliverables Missing。**

当前不允许：
- 宣称 Session D 已通过三方六维度审查；
- 冻结 D 的 Canonical Memory Schema、Lifecycle API、Entity/Relation API 或 Versioning Contract；
- 让 E/F/G/H/I 依赖未发布的 D 私有语义；
- 将 INT-P0-01..04 或 INT-P1-01/02/06 标记为已关闭；
- 将 A/B/C 的原则性架构说明当作 D 的实现级契约。

当前允许：
- D 按任务书补交五份设计文件；
- 以 A/B/C 现有基线为约束推进受控设计；
- 对候选方案开展比较，但必须显式标记候选与 ADR-blocked 项；
- 文件齐备后重新进行独立静态复审。

**本报告不修改 Session D 原始设计文件、公共治理文件、A/B/C 文档或其他模块审查报告。仅作为 D 的审查记录提交。**

---

**报告结束**
