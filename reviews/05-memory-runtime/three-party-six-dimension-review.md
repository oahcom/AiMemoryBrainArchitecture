# Session F Review — Memory Runtime 三方六维度独立架构审查报告

- 审查日期：2026-11-16
- 审查对象：Session F — Memory Runtime
- 审查类型：仓库文档静态审查与跨模块契约审查
- 审查结论：**Review Blocked / Not Passed（审查受阻，不予通过）**
- 审查归属：`reviews/05-memory-runtime/`
- 审查方式：三个专业视角的独立模拟；不代表真实三名审查人员签署
- 重要限制：本报告不是性能测试、安全渗透测试、代码审计或运行时验证

> 本报告严格区分“设计缺失/证据缺失”与“已证实的实现缺陷”。由于本次审查时仓库中未能取得 Session F 的核心设计文档，不能对 F 的具体实现方案作出肯定或否定的事实判断。凡缺少 F 设计证据的项目均标记为 PARTIAL 或 NOT ASSESSABLE，不得视为通过。

---

## 1. 审查范围与证据状态

### 1.1 仓库与版本基线

- Repository：`oahcom/AiMemoryBrainArchitecture`
- Branch：`main`
- 本次检查可见的最新提交：`e443b23f8a179ad12c163722ad93bc646fd3a80a`
- 最新提交说明：`Add Phase 1 A/B/C integration review`
- 仓库 README 标记当前阶段为架构定义，Implementation 尚未开始。

### 1.2 已成功读取的基线材料

| 文件 | 状态 | 审查用途 |
|---|---|---|
| `README.md` | READ | 总体定位、组件职责、文档地图 |
| `ARCHITECTURE_ROADMAP.md` | READ | 设计阶段、状态分类、性能验证原则 |
| `00-governance/design-principles.md` | READ | P-01 至 P-16 |
| `00-governance/architecture-invariants.md` | READ | I-01 至 I-22 |
| `00-governance/terminology.md` | READ | Canonical Memory、Working Set、Scope 等规范术语 |
| `01-system-architecture/system-overview.md` | READ | Brain/Runtime/Context/Agent 边界 |
| `01-system-architecture/component-map.md` | READ（返回内容截断） | 组件责任与所有权规则 |
| `01-system-architecture/responsibility-matrix.md` | READ（随组件矩阵返回） | Retrieval、Activation、Context、Governance 主责关系 |
| `02-domain-model/domain-model-overview.md` | READ | Memory/Claim/Version/Provenance/Scope 契约 |
| `reviews/integration/phase-1-abc-cross-document-integration-review.md` | READ | INT-P0 / INT-P1 与跨模块门禁 |

### 1.3 本次未能取得的材料

下列 Session F 核心文件按任务书指定路径读取时均返回 GitHub 404：

- `05-memory-runtime/runtime-overview.md`
- `05-memory-runtime/retrieval-engine.md`
- `05-memory-runtime/activation-policy-engine.md`
- `05-memory-runtime/working-set-and-cache.md`
- `05-memory-runtime/runtime-scheduling.md`

同时，以下目标审查报告在读取时不存在：

- `reviews/05-memory-runtime/three-party-six-dimension-review.md`

通过仓库提交历史检索，未发现与 Runtime、Memory Runtime、Session F、Retrieval、Activation Policy、Working Set 或 Scheduling 对应的提交记录。由此只能确认本次审查所连接的仓库版本中没有取得这些文档，不能推断它们在其他分支、未提交工作区或其他位置不存在。

### 1.4 其他跨模块材料状态

本次已读取 A/B/C 集成报告及部分 A/B 基线，但没有取得 D/E/G/I 的完整设计与专项审查报告。因此：
- D 的 Canonical Store、Lifecycle、Forget 实施契约：未完成直接核验。
- E 的 Index Publication、Outbox、Watermark 契约：未完成直接核验。
- G 的 Context Candidate、Context Version、Change Set 契约：未完成直接核验。
- I 的 Scope/Permission、撤权、Forget、审计执行契约：未完成直接核验。

### 1.5 审查局限

本报告不能声称已完成任务书要求的“05 全部文件逐项审查”或“D/E/G/I 全量契约审查”。本轮对可见基线进行边界检查，并将 F 文档缺失作为审查阻断项。不得将文档未提交解释为某项安全机制已经存在，也不得将其直接描述为已复现的漏洞。

---

## 2. 总体结论

### 2.1 最终决议

**Review Blocked / Not Passed。不得冻结 Session F 架构契约，不得据此放行实现。**

理由不是已经证明 F 的设计错误，而是关键审查对象没有进入可审查状态。任务书规定的核心文件缺失，意味着以下通过条件均无法得到证据支持：

1. 所有检索通道均在 Candidate Generation 前完成 Scope 过滤。
2. Graph Expansion 对关系边与目标节点重新授权。
3. Reranker 不会收到越权候选。
4. Cache 与 Working Set 不会跨 Principal、Scope 或权限版本复用数据。
5. Forget Tombstone/Canonical 状态能阻断旧索引、缓存和在途任务返回。
6. Index Watermark、Publication Lag 与部分结果状态可识别。
7. Runtime 不拥有 Canonical Memory 或 Context Version。
8. F 的输出契约可以被 G 正确消费。
9. 性能目标与实测结果严格区分。
10. Cancellation、Backpressure、Early Stop 和并发隔离具有可实现的语义。

**审查门禁：**
- 不能判定 PASS。
- 不授予 Conditional Pass 作为设计完成的含义。
- 在补齐 F 文档并重新审查之前，所有涉及候选可见性、缓存、Working Set、Forget 和 Context Version 的实现冻结均应阻断。
- 可以继续进行不锁定这些语义的研究与原型准备，但不得将原型假设写成安全保证。

### 2.2 当前可确认的架构基线

仓库现有基线已经规定：
- Brain 是 Canonical Memory 的逻辑权威；Runtime 不应形成第二权威。
- Context Manager 拥有 Context Version 权威。
- Retrieval 返回候选与证据；Activation Policy 决定候选是否属于 Context。
- Context Entry 不是 Canonical Memory。
- Scope 与 Permission 是不同概念，且必须显式隔离。
- Memory 内容是不可信数据，不具有 system/developer 指令权威。
- 性能声明必须由可复现测量支持。

这些规则来自系统架构、责任矩阵、治理原则与领域模型基线；它们只能作为 F 的审查标准，不能证明 F 已经落实。

---

## 3. 三方独立结论

### 3.1 第一方：系统架构师

**结论：PARTIAL — 上位架构边界清楚，F 的实际边界无法验证。**

已取得的系统架构基线明确将 Runtime 定位为检索、激活、Working Set、缓存及上下文服务路径的一部分；同时明确 Context Manager 拥有 Context Version 权威，Canonical Store 拥有 Canonical 持久化权威。

尚无法验证：
- F 是否错误拥有 Canonical Memory 或最终 Context Version。
- Retrieval Result、Activation Recommendation、Context Candidate、Context Entry 是否严格分离。
- 是否混入 Agent Planning State。
- 多 Agent / Agent Instance / Session 是否隔离。
- 是否存在重复缓存或重复权威。
- 异步预取与高风险动作前同步检查是否有清楚边界。
- Runtime 是否可脱离特定 Agent 框架运行。

**架构意见：** 在 F 文档中必须提供组件所有权表、数据对象所有权表、跨 Session 隔离模型及与 D/E/G/I 的接口图。不得以“Runtime 负责 Context”之类宽泛描述覆盖 G 的权威边界。

### 3.2 第二方：工程实现负责人

**结论：NOT ASSESSABLE — 无法审查检索与调度的可实现性。**

缺少 Retrieval Query/Result Schema、检索路由、并行调度、候选融合、Watermark、Cache Key、Working Set、Cancellation 和资源预算设计，无法判断：
- 多通道并行是否会造成不可控的尾延迟。
- ANN、FTS、Structured、Graph、Temporal 的职责是否重叠。
- Scope Filter 是否真正位于每条候选生成路径之前。
- Index Publication Lag 是否有可验证的读取策略。
- Cache Invalidation 是否会引入全局锁或高成本扫描。
- Cancellation 是否能中断底层 ANN/图查询和 Reranker。
- Backpressure 是否覆盖 CPU、磁盘、内存、GPU 与队列。
- 部分结果是否携带 Completeness 与 Watermark。
- Rust 异步任务是否具备预算、优先级、隔离与资源释放规则。

**工程意见：** 在没有 Query Plan、预算模型、并发状态机、错误语义与 Benchmark Plan 之前，不得宣称 Runtime 达到固定 P50/P95/P99、吞吐量或资源占用目标。

### 3.3 第三方：安全与可靠性审计者

**结论：NOT ASSESSABLE — 关键安全路径没有设计证据。**

由于 F 文件缺失，不能验证以下安全控制：
- Structured、FTS、ANN、Graph、Temporal 等通道是否在候选生成前授权。
- 图扩展是否重新授权 Edge 与 Target Node。
- Reranker 是否仅处理已授权候选。
- Cache Lookup 是否使用当前 Principal、Scope、Permission Epoch 与 Forget 状态。
- Working Set Readback 是否重新检查权限与生命周期。
- Forget 是否先阻断访问再异步清理派生副本。
- Index 重建是否读取权威 Tombstone。
- 在途查询遇到撤权/Forget 是否取消或在序列化前重新校验。
- 错误、分数、统计和 Trace 是否形成侧信道。
- 不可信记忆是否保留 Trust、Epistemic Status、Evidence 和 Source 标签。

**安全意见：** 不能因为最终输出阶段有 Scope Filter 就判定安全。必须提供逐通道数据流和可测试的拒绝路径；任何越权候选路径或 Forget 后复活路径均至少导致 Conditional Pass，且不得放行实现冻结。

---

## 4. 六维度审查

### 维度一：架构与职责边界

| 检查项 | 状态 | 证据与结论 |
|---|---|---|
| Runtime 位于 Brain 内部执行层 | PARTIAL | System Overview 有 Runtime 定位；F 自身边界文档缺失 |
| Runtime 不拥有 Canonical Memory | PARTIAL | P-01、I-01 与责任矩阵确立上位规则；F 未验证 |
| Runtime 不拥有 Context Version | PARTIAL | 系统架构明确 Context Manager 为主责；F 未验证 |
| Retrieval 与 Activation 分离 | PARTIAL | 责任矩阵区分 Retrieval 与 Activation；F 未验证接口 |
| Working Set 与 Context 分离 | PARTIAL | 术语表区分 Working Set 与 Memory Context；F 未验证对象模型 |
| 不混入 Agent Planning State | NOT ASSESSABLE | 缺少 F Working Set 与 Session Schema |
| 多 Agent / Instance / Session 隔离 | NOT ASSESSABLE | 缺少 F Session 与 Cache Key 设计 |
| 异步预取 / 高风险同步激活 | NOT ASSESSABLE | 缺少调度与触发策略 |
| Agent 框架无关 | PARTIAL | P-02、I-03 有约束；F 接口未知 |

### 维度二：领域模型与数据契约

| 对象/契约 | 状态 | 必须提供的证据 |
|---|---|---|
| Retrieval Query | NOT ASSESSABLE | Query ID、Principal、Scope、目标、过滤器、预算、版本、取消句柄 |
| Retrieval Candidate | NOT ASSESSABLE | Memory ID/Version、Claim/Conflict、来源、权限判定、通道与候选原因 |
| Retrieval Result | NOT ASSESSABLE | 候选集合、排序信息、证据引用、完整性、不确定性、水位 |
| Activation Recommendation | NOT ASSESSABLE | 推荐/拒绝/延迟原因、政策版本、证据与置信边界 |
| Evidence Summary | NOT ASSESSABLE | Evidence 引用、可见性、来源与保留限制 |
| Completeness / Uncertainty | NOT ASSESSABLE | 明确枚举、缺失原因与传播规则 |
| Index Watermark | NOT ASSESSABLE | Canonical commit 与投影消费位置、分区及版本 |
| Runtime Session | NOT ASSESSABLE | Principal、Agent Instance、Session、Task、Environment 绑定 |
| Working Set Entry | NOT ASSESSABLE | 权威 ID/Version、Scope、过期、撤权与 Forget 失效状态 |
| Cache Entry | NOT ASSESSABLE | 完整安全 Cache Key、版本、失效依据 |
| Scope / Permission Context | NOT ASSESSABLE | 权威身份、资源 Scope、操作权限、Permission Epoch |
| Claim / Conflict / Provenance 引用 | PARTIAL | Domain Model 定义语义，但 F 的引用方式缺失 |

**强制结论：** Retrieval Result 不得直接等同于 Context Entry。F 应只提供可审计的 Retrieval Result 和 Activation Recommendation，G 再根据自己的权威规则创建、更新或移除 Context Entry，并提交 Context Version。

### 维度三：数据流与一致性

| 场景 | 状态 | 审查要求 |
|---|---|---|
| Canonical Commit 后 Index 尚未更新 | NOT ASSESSABLE | Watermark、Lag、回退读取或不完整结果策略 |
| Forget 已发生、ANN 删除未完成 | NOT ASSESSABLE | Canonical/Tombstone 访问阻断优先于 ANN 结果 |
| 查询期间权限撤销 | NOT ASSESSABLE | 撤销 Epoch 检查、取消或最终序列化前重新授权 |
| 旧缓存与新 Memory Version 冲突 | NOT ASSESSABLE | Version-aware key、失效与读后校验 |
| Graph Expansion 跨 Scope | NOT ASSESSABLE | 每条 Edge 和 Target Node 单独授权 |
| 多通道融合时发生版本更新 | NOT ASSESSABLE | 同一查询快照或显式混合版本标记 |
| 部分结果与取消竞争 | NOT ASSESSABLE | Terminal State、Completeness、取消后的不可再发布约束 |
| Index 重建与 Forget 并发 | NOT ASSESSABLE | Tombstone/治理水位必须参与重建 |

必须明确的五个问题：

1. **Canonical 已提交、Index 未更新：** F 必须能识别 Index Watermark 落后。不得把“未检索到”解释为“Canonical 不存在”。可以采用受预算限制的 Canonical delta 查询、短暂不完整结果或其他明确策略，但必须标注完整性与水位。
2. **Forget 已发生、ANN 删除未完成：** ANN 命中只能视为非权威候选。必须通过权威 Forget/Lifecycle 状态阻断候选向后传播，不能等待物理向量删除完成。
3. **查询期间权限撤销：** 仅在 Query Start 检查不足。必须定义撤销传播、在途任务取消及输出提交前的授权检查点。
4. **旧缓存与新 Memory Version 冲突：** 不得返回旧版本作为当前版本。Cache Key 或 Entry 必须绑定 Memory Version/Projection Version，并由权威状态校验。
5. **跨 Scope 图扩展：** 关系本身和目标节点都需要授权；不能因起始节点可见就推导其邻居可见。

上述是必须满足的设计要求，不是对未提交 F 设计的缺陷认定。

### 维度四：安全与治理

#### 4.1 Scope-before-Candidate 检查矩阵

| Pipeline Stage | 必须执行的安全检查 | 当前状态 |
|---|---|---|
| Structured Search | 在数据库候选扫描/返回前按可信 Scope 与 Permission 约束 | NOT ASSESSABLE |
| Full-text Search | 在倒排候选进入通用 Candidate Set 前授权 | NOT ASSESSABLE |
| Vector ANN | 使用预过滤或具备等价安全证明的分区/查询策略；不得仅最终过滤 | NOT ASSESSABLE |
| Graph Expansion | Edge 与 Target Node 均重新授权；限制跨 Scope Fan-out | NOT ASSESSABLE |
| Temporal Search | 时间范围与 Scope 同时约束候选生成 | NOT ASSESSABLE |
| Evidence Retrieval | Evidence 独立权限检查，不能继承 Memory 的可见性假设 | NOT ASSESSABLE |
| Candidate Fusion | 只融合已授权候选；来源通道与授权决策可追踪 | NOT ASSESSABLE |
| Reranking | 未授权候选不得进入 Reranker；不得以最终过滤补救 | NOT ASSESSABLE |
| Result Serialization | 输出前重新验证权限/Forget/版本；字段级脱敏 | NOT ASSESSABLE |
| Cache Lookup | 授权上下文进入 Key，命中后仍检查撤权/Forget 状态 | NOT ASSESSABLE |
| Working Set Readback | 读取时校验 Scope、Permission Epoch、Lifecycle、Forget 与 Version | NOT ASSESSABLE |

**判定：Scope-before-Candidate 未获证明。** 在 F 提交逐通道设计与负向测试前，不得宣称 INT-P0-02 已解决。

#### 4.2 Forget / Cache / Index 失效矩阵

| 触发事件 | Canonical | Index / ANN / FTS / Graph | Cache | Working Set | In-flight Query |
|---|---|---|---|---|---|
| Permission Revocation | 权限权威更新 | 查询必须读取新权限状态 | Permission Epoch 失效 | Readback 拒绝 | 取消或重新授权 |
| Forget Requested/Committed | 进入权威 Forget 状态 | Tombstone/过滤先于物理清理 | 立即阻断旧命中 | 立即标记不可读 | 取消或在输出前剔除 |
| Memory Version Superseded | 新版本成为当前权威 | 投影更新并暴露水位 | 旧版本不能冒充当前版本 | 旧 Entry 失效或明确历史读取 | 按查询快照策略标记 |
| Index Rebuild | 以 Canonical 与治理记录为依据 | 不得重建 Forgotten 对象 | 重建期间不能绕过权威检查 | 不得从旧快照恢复 | 读取端持续检查 |
| Scope/Sharing Change | 权威 Scope 变更 | 重新应用可见性策略 | Scope/Permission 维度失效 | 重新授权 | 取消或重新授权 |

本矩阵是后续设计验收要求。当前 F 的实际失效传播实现没有证据。

#### 4.3 Prompt Injection 与不可信记忆

F 必须将 Trust、Epistemic Status、Evidence、Source、Provenance 与 Relevance 分开表达。排序分数不得解释为可信度或授权。Runtime 不得将记忆中的工具调用文本、伪造 system 标签或指令性自然语言转化为工具权限或 Agent 命令。即使结构化封装，也不能声称完全消除模型受提示注入影响的风险。

当前状态：**PARTIAL（上位原则已确立，F 输出标签与传播链未验证）**。

### 维度五：性能与资源

当前无 F 性能设计文档、Benchmark 方案或实测数据。所有性能结论均为 NOT ASSESSABLE。

必须补充的性能设计：

- ANN/FTS/Structured/Graph/Temporal 并行度、候选预算与超时预算。
- Graph Fan-out、最大深度、节点/边预算及跨 Scope 拒绝成本。
- Provenance 展开深度、字节数和超时上限。
- Reranker 的调用门槛、候选上限、批处理策略、CPU/GPU fallback。
- Query Cache 命中率、失效成本、冷热分层及安全检查开销。
- Working Set 容量、TTL、内存回收与 Session 配额。
- CPU、RAM、Disk I/O、GPU/VRAM 的全局和每 Session 预算。
- 并发隔离、优先级、公平调度、Backpressure 与拒绝策略。
- Cancellation 对下游实际计算的传播与资源回收保证。
- Early Stop 的质量/完整性语义，不能将预算截断伪装为完整结果。
- P50/P95/P99、吞吐、资源占用、召回质量和 Agent 任务效用的测量方案。

**禁止事项：** 不得把目标延迟、候选上限、并发数或资源估算写成已经实现的性能事实。没有可复现 Benchmark 时，只能标记为 CANDIDATE 或 TO_VALIDATE。

### 维度六：可演进性与可观测性

F 至少需要定义并记录：

- Index Schema Version、Index Build ID、Index Watermark。
- Retrieval Query Version、Retrieval Policy Version。
- Activation Policy Version。
- Cache Schema/Key Version。
- Runtime Session ID、Task/Agent Instance 关联。
- Correlation ID / Causation ID。
- 每通道候选数量、拒绝数量及 Scope Denial Audit。
- Candidate Reason、Source Channel、Version 与 Provenance Reference。
- Activation Reason、Policy Version、拒绝/延迟原因。
- Completeness、Uncertainty、Truncation、Timeout、Cancellation。
- Permission Epoch、Forget/Tombstone 检查结果。
- Index rebuild、replay、schema migration 的进度与恢复点。

日志与指标不得暴露越权候选的 ID、文本、分数或可推断内容。应区分安全审计日志与普通性能指标，并约束 cardinality、保留期限与访问权限。

当前状态：**NOT ASSESSABLE（F 观测设计缺失）**。

---

## 5. 逐文件审查矩阵

| 文件 | 读取状态 | 审查结论 |
|---|---|---|
| `runtime-overview.md` | NOT FOUND | 无法审查职责、状态机、边界 |
| `retrieval-engine.md` | NOT FOUND | 无法审查 Query、通道、融合、Scope-before-Candidate |
| `activation-policy-engine.md` | NOT FOUND | 无法审查策略、证据、拒绝与推荐语义 |
| `working-set-and-cache.md` | NOT FOUND | 无法审查隔离、失效、容量与撤权 |
| `runtime-scheduling.md` | NOT FOUND | 无法审查 Rust 并发、预算、取消与背压 |
| `three-party-six-dimension-review.md` | NOT FOUND | 本报告为该目标文件的首次创建 |

不得对不存在的文件虚构章节号或行号证据。

---

## 6. Retrieval Pipeline 风险清单

以下是必须在 F 设计中排除的风险路径，不代表已在代码中复现：

1. ANN 先生成全局候选，再在序列化阶段过滤 Scope。
2. FTS/Structured 查询返回跨 Scope 候选后才统一授权。
3. Graph Expansion 只检查起点节点，未检查关系边和目标节点。
4. Reranker 接收未经授权的候选文本，形成越权数据处理与侧信道。
5. Cache 命中绕过当前 Permission Epoch 与 Forget 状态。
6. Working Set 将旧权限下的数据当作可信热数据直接返回。
7. Forget 只删除 Canonical 行，索引重建从旧快照恢复已忘记对象。
8. 多通道融合把不同 Memory Version 混为一个无版本候选。
9. 部分结果未标记 Completeness，调用方误认为已完成全部检索。
10. Early Stop 或 Cancellation 后仍有后台任务发布迟到候选。
11. Reranker/LLM 作为默认同步依赖，导致本地模型不可用时检索主路径阻塞。
12. Provenance 展开无深度/字节/时间预算，造成资源放大或越权 Evidence 暴露。

---

## 7. P0/P1/P2/P3 问题登记

> 本节把“审查交付阻断”与“待验证的设计风险”分开。缺少文档本身是已确认的交付问题；下列安全路径是尚未排除的风险，不冒充已证实漏洞。

### FREV-P0-01 — Session F 核心设计材料缺失

- **Severity：** P0（审查与安全门禁阻断）
- **File / Section：** `05-memory-runtime/*`；五份任务书指定核心文件均未取得
- **Evidence：** 本次对五个指定路径的 GitHub fetch 均返回 404；可见提交历史未发现 F 相关提交
- **Problem：** 无法审查候选生成前授权、Forget 阻断、Cache/Working Set 隔离及 G 接口契约
- **Impact：** 不能证明不存在越权候选或 Forget 后复活路径；无法冻结 F 契约
- **Required Correction：** 提交五份核心设计文件，补齐目录索引与跨模块引用；明确状态分类与验收条件
- **Owner：** Session F Principal Architect
- **Dependency：** D Canonical Store、E Index Publication、G Context Manager、I Security/Governance
- **Acceptance Criteria：** 五份文件均可从默认分支读取；内容覆盖本任务书审查点；每个安全不变量有执行位置、失败语义和测试标准；重新完成三方六维度审查

### FREV-P0-02 — Scope-before-Candidate 尚未获得证明

- **Severity：** P0（安全门禁）
- **File / Section：** Retrieval Engine、所有检索通道、Fusion、Reranking
- **Evidence：** INT-P0-02 要求 Scope 在候选生成前生效；本次无 F Retrieval 文档
- **Problem：** 无法确认 Structured、FTS、ANN、Graph、Temporal、Evidence 各通道的候选生成边界
- **Impact：** 存在候选越权、Reranker 越权接收、错误统计泄露等未排除风险
- **Required Correction：** 逐通道给出过滤执行位置；图边/目标节点二次授权；Fusion/Reranker 仅接收已授权候选；给出跨 Scope 负向测试
- **Owner：** F Retrieval Owner；I Security/Governance 定义授权契约
- **Dependency：** INT-P0-02、B DM-010、C P1-03/P1-07
- **Acceptance Criteria：** 所有通道在候选进入共享 Candidate Set 前执行 Scope/Permission 检查；未授权数据不进入 Reranker、Cache、Working Set 或日志载荷；负向测试证明拒绝

### FREV-P0-03 — Forget 阻断与派生副本失效尚未获得证明

- **Severity：** P0（安全门禁）
- **File / Section：** Index、Cache、Working Set、In-flight Query、Index Rebuild
- **Evidence：** INT-P0-03 要求 Forget 覆盖索引、缓存、工作集、快照及在途任务；无 F 设计材料
- **Problem：** 无法确认权威 Forget 状态能否在 ANN/FTS/Graph 物理删除前阻断访问
- **Impact：** 存在 Forget 后通过旧索引、旧缓存、旧工作集或重建快照复活的未排除风险
- **Required Correction：** 定义权威 Tombstone/状态检查、先阻断后清理、在途任务取消/重检、重建过滤及审计
- **Owner：** I Governance 主责；F Runtime 派生数据路径负责；D/E 提供权威状态与投影机制
- **Dependency：** INT-P0-03、A AR-001、B DM-011
- **Acceptance Criteria：** Forget 生效后所有检索/缓存/工作集读取均拒绝目标对象；索引重建不能复活；故障注入覆盖异步清理未完成、重试、旧快照和在途查询

### FREV-P1-01 — Retrieval Result / Activation Recommendation / Context Candidate 契约缺失

- **Severity：** P1
- **File / Section：** Retrieval Engine、Activation Policy Engine、G 接口
- **Evidence：** A/B/C 集成基线要求 Retrieval 与 Activation 分离，Context Version 由 G 管理；F 文件未取得
- **Problem：** 不清楚检索结果与激活建议是否混用，更无法证明不会直接写入 Context Version
- **Impact：** G 可能无法消费 F 输出，或出现 Runtime 隐性 Context Owner
- **Required Correction：** 定义版本化 Query/Result/Recommendation Schema；明确 G 对 Context Entry 与 Version 的唯一所有权
- **Owner：** F + G
- **Dependency：** INT-P1-01、INT-P1-02、INT-P1-06
- **Acceptance Criteria：** F 输出可被 G 映射为 Context Candidate；Result 不等于 Entry；F 无 Context Version 写权限；契约测试覆盖版本、冲突、证据和不完整结果

### FREV-P1-02 — Index Watermark 与 Canonical/Index 一致性契约缺失

- **Severity：** P1
- **File / Section：** Retrieval Engine、Index Reader、Cache
- **Evidence：** A AR-004 与 INT-P1-06 要求 Canonical Commit、Outbox Publication、Provenance Visibility、Index Watermark 语义闭合
- **Problem：** 无法判断 F 如何识别索引延迟、重建和多分区不一致
- **Impact：** 旧版本可能被当成最新，缺失候选可能被误认为不存在
- **Required Correction：** 定义 per-index/per-partition Watermark、查询快照策略、Lag、staleness 与 Completeness
- **Owner：** E Index Publication + F Runtime
- **Dependency：** A AR-004、B DM-006/007/008、INT-P1-06
- **Acceptance Criteria：** 每个 Result 可追溯所用 Index Build/Schema/Watermark；滞后与部分结果明确可见；重建与重放保持 Forget 约束

### FREV-P1-03 — Cache / Working Set 安全隔离与撤权失效契约缺失

- **Severity：** P1（若存在跨 Scope 命中则升级 P0）
- **File / Section：** Working Set and Cache
- **Evidence：** INT-P0-02 要求缓存绑定主体、Scope、Environment 与权限版本；F 文件缺失
- **Problem：** 无 Cache Key、Entry Validation、Invalidation、Session 隔离设计
- **Impact：** 跨主体、跨环境或撤权后的旧数据复用风险无法排除
- **Required Correction：** 定义安全 Key、Permission Epoch、Memory Version、Forget Epoch、TTL、读时校验和并发失效语义
- **Owner：** F Runtime；I 提供 Permission/Revocation contract
- **Dependency：** INT-P0-02、INT-P0-03、C P1-07
- **Acceptance Criteria：** 不同 Principal/Scope/Environment 不会错误命中；撤权与 Forget 立即阻断读取；旧版本不会冒充当前版本

### FREV-P2-01 — 多通道预算、背压、取消与 Early Stop 缺少可审查方案

- **Severity：** P2
- **File / Section：** Runtime Scheduling / Retrieval Engine
- **Evidence：** F 调度文件未取得；Roadmap 要求性能预算与测量计划
- **Problem：** 无法判断并行成本、队列、公平性、资源上限与取消传播是否可实现
- **Impact：** 可能出现尾延迟放大、资源耗尽、任务堆积或取消后资源泄漏
- **Required Correction：** 定义每 Query/Session/全局预算、队列上限、优先级、超时、取消、背压与部分结果语义
- **Owner：** F Runtime Engineering
- **Dependency：** Index Provider、Rust Runtime、目标硬件基线
- **Acceptance Criteria：** 有可复现 Benchmark Plan、压力/取消/故障注入用例；性能指标只在测量后报告

### FREV-P2-02 — Retrieval Trace 与安全审计可观测性缺少证据

- **Severity：** P2
- **File / Section：** Runtime Observability / Retrieval Trace
- **Evidence：** F 文档未取得；INT-P0-02/03 要求安全审计可追踪
- **Problem：** 无法解释候选来源、拒绝原因、激活原因、Completeness 与 Watermark
- **Impact：** 无法定位越权尝试、索引滞后、错误激活与性能退化；也可能在日志中泄露越权信息
- **Required Correction：** 定义 Trace Schema、Correlation ID、字段脱敏、指标维度与保留策略
- **Owner：** F + I
- **Dependency：** INT-P0-02、INT-P0-03、INT-P1-06
- **Acceptance Criteria：** 可解释找到/未找到/激活/未激活；审计字段不暴露未授权内容；Trace 可关联 Query、Index、Policy、Session

### FREV-P3-01 — Runtime 文档导航与状态分类缺失

- **Severity：** P3
- **File / Section：** `05-memory-runtime/`、README 文档地图
- **Evidence：** 指定 Runtime 文档路径未取得
- **Problem：** 读者无法确认 F 的规范入口、文件清单和 DECIDED/CANDIDATE/TO_VALIDATE/OPEN 状态
- **Impact：** 增加跨模块误读和实现时擅自冻结假设的风险
- **Required Correction：** 补充目录索引、Owner、版本、依赖和状态表
- **Owner：** F
- **Dependency：** 无
- **Acceptance Criteria：** 所有文档可从 README/目录索引导航；状态与 ADR 一致

---

## 8. INT-* 状态矩阵

状态定义：
- **PASS：** 有充分文档证据满足要求。
- **PARTIAL：** 上位原则或部分契约已存在，但 F 落地证据缺失。
- **FAIL：** 已有证据证明违反要求。
- **NOT APPLICABLE：** 经确认不适用。
- 对 F 核心实现无法核验的情况，不以 PARTIAL 冒充完成；在矩阵中明确标注“F 侧未评估”。

| ID | 状态 | 依据与 F 侧结论 |
|---|---|---|
| INT-P0-02 | PARTIAL | 治理/集成报告明确要求 Scope-before-Candidate；F 通道实现未评估，安全门禁未关闭 |
| INT-P0-03 | PARTIAL | 集成报告定义 Forget 全链路门禁；F Index/Cache/Working Set 路径未评估 |
| INT-P0-04 | PARTIAL | I-12、P-11 确立 Memory 非指令权威；F Trust/Evidence 输出传播未评估 |
| INT-P1-01 | PARTIAL | G 拥有 Context Version 的基线明确；F Result/Recommendation 对 G 契约未评估 |
| INT-P1-02 | PARTIAL | Domain Model 已定义 Claim/Memory Version，但 Claim Revision/Conflict 的 F 引用方式未评估 |
| INT-P1-06 | PARTIAL | Domain Model 定义 Provenance；A AR-004/集成报告要求一致性闭环；F Index/Provenance 引用未评估 |
| A AR-001 | PARTIAL | Forget 全链路风险由集成报告记录；F 侧缓存/工作集阻断未评估 |
| A AR-002 | PARTIAL | Prompt Injection 残余风险已在集成报告记录；F Trust/Epistemic 标记未评估 |
| A AR-003 | PARTIAL | Scope 隔离要求已确立；F 候选前过滤未评估 |
| A AR-004 | PARTIAL | Provenance/Index 一致性风险已确立；F Watermark 未评估 |
| B DM-006 | PARTIAL | Provenance 语义在 Domain Model 有定义；F Evidence/Provenance 引用未评估 |
| B DM-007 | PARTIAL | Lifecycle 语义在 Domain Model 有定义；F Retracted/Superseded 过滤未评估 |
| B DM-008 | PARTIAL | Typed 引用/关系语义部分定义；F Query/Result 引用未评估 |
| B DM-010 | PARTIAL | Scope 与 Permission 区分明确；F 通道执行点未评估 |
| B DM-011 | PARTIAL | Forget/Retention 要求明确；F 派生缓存与索引失效未评估 |
| C P1-03 | PARTIAL | 身份/Scope 绑定要求在集成报告中；F Runtime Session 绑定未评估 |
| C P1-07 | PARTIAL | 撤权/Forget 传播缺口在集成报告中；F Cache/Working Set 失效未评估 |
| C P2-07 | PARTIAL | Memory Prompt Injection 风险在集成报告中；F 不可信记忆标记未评估 |
| C P2-09 | PARTIAL | 端到端关联与观测要求在集成报告中；F Trace 未评估 |
| C P2-12 | PARTIAL | 性能复杂度预算要求在集成报告中；F 预算未评估 |
| C P2-13 | PARTIAL | 故障注入与性质测试要求在集成报告中；F 测试矩阵未评估 |

> 注：任务书要求的 C P2-07/P2-09/P2-12/P2-13 采用集成报告中可见的对应风险主题；本报告未取得 C 专项审查原文，故不声称已复核其原始章节或全部细节。任何 ID 的 PARTIAL 都不代表 F 已满足。

---

## 9. 对 A/B/C 指定问题 ID 的逐项回应

### A：AR-001 / AR-002 / AR-003 / AR-004

| ID | 状态 | F 必须回应 |
|---|---|---|
| AR-001 | PARTIAL | Forget 必须先阻断访问，再清理索引、Cache、Working Set 与在途查询；F 证据缺失 |
| AR-002 | PARTIAL | 保留来源、Trust、Epistemic Status、Evidence；不得把 Memory 变成工具授权；F 证据缺失 |
| AR-003 | PARTIAL | Scope/Permission 必须贯穿候选生成与派生路径；F 证据缺失 |
| AR-004 | PARTIAL | Canonical/Index/Provenance/Watermark 一致性与恢复规则必须明确；F 证据缺失 |

### B：DM-006 / DM-007 / DM-008 / DM-010 / DM-011

| ID | 状态 | F 必须回应 |
|---|---|---|
| DM-006 | PARTIAL | Retrieval Candidate/Result 必须保留 Provenance 与 Evidence 引用，不因摘要或排序丢失来源 |
| DM-007 | PARTIAL | Superseded/ Retracted / Forgotten 的过滤必须基于权威生命周期状态 |
| DM-008 | PARTIAL | Memory、Claim、Relation、Evidence 等引用类型不得退化为无类型字符串 |
| DM-010 | PARTIAL | Scope-before-Candidate 必须逐通道实现，并对图边/目标节点授权 |
| DM-011 | PARTIAL | Forget 必须覆盖索引、缓存、Working Set、重建快照和在途任务 |

### C：P1-03 / P1-07 / P2-07 / P2-09 / P2-12 / P2-13

| ID | 状态 | F 必须回应 |
|---|---|---|
| P1-03 | PARTIAL | Runtime Session 绑定可信 Principal/Agent/Instance/Task/Environment，不接受 Agent 自报 Scope |
| P1-07 | PARTIAL | 撤权与 Forget 必须传播至 Cache、Working Set、异步任务和 Readback |
| P2-07 | PARTIAL | 不可信 Memory 的来源/信任/认识状态需保留；不升级为指令 |
| P2-09 | PARTIAL | Query → Candidate → Activation → Context Candidate 具备端到端 Correlation |
| P2-12 | PARTIAL | Graph/Provenance/检索通道具备复杂度与资源预算 |
| P2-13 | PARTIAL | 重复、乱序、并发、取消、崩溃、撤权、Forget 部分失败需进入故障注入测试 |

---

## 10. 与 D/E/G/I 的契约冲突与接口门禁

由于 D/E/G/I 设计文件未在本轮完整取得，本节列出必须满足的接口门禁，不把未知内容伪装成已发现的实际冲突。

### 10.1 D — Memory Brain

F 必须消费 D 提供的权威 Memory ID、Memory Version、Lifecycle 状态、Scope、Claim/Relation、Evidence/Provenance 引用。Runtime 不得自行创造 Canonical ID、修订权威状态或将 Superseded/Retracted/ Forgotten 对象当作当前可用记忆。

### 10.2 E — Memory Compiler / Index Publication

E 必须提供可验证的 Publication Event、Index Schema/Build Version、Watermark、Tombstone/Forget 传播语义。F 必须将索引视为 Canonical Memory 的派生投影，不能把 ANN/FTS/Graph 命中当成权威事实。

### 10.3 G — Memory Context Manager

F 应输出 Retrieval Result 与 Activation Recommendation。G 决定是否创建/更新/移除 Context Entry，并拥有 Context Version 与 Change Set 权威。F 不得直接提交最终 Context Version，也不得把 Retrieval Result 序列化成 Context Entry 后绕过 G 的预算、冲突和并发策略。

### 10.4 I — Security / Governance

I 应定义可信身份、Scope、Permission、Permission Epoch、Revocation 与 Forget 权威语义。F 必须在检索通道、Cache Lookup、Working Set Readback 和输出提交点执行本地授权检查，并提供审计事件。不能只依赖入口 Gateway 的一次性检查。

---

## 11. DECIDED / CANDIDATE / TO_VALIDATE / OPEN

### DECIDED（由现有上位基线约束）

- Runtime 不拥有 Canonical Memory。
- Runtime 不拥有 Context Version。
- Retrieval 与 Activation 是不同职责。
- Retrieval Result 不等于 Context Entry。
- Scope 与 Permission 分离且必须执行。
- Index 是 Canonical Memory 的派生投影。
- Cache 不得绕过权限检查。
- Memory 内容不具有 system/developer 指令权威。
- 性能声明需要可复现测量。

### CANDIDATE（建议 F 设计比较的方案，不得当成已定案）

- 对各检索通道采用统一的 Scope-aware Query Context。
- 将权威 Forget/Revocation 状态作为索引与缓存命中的二次门禁。
- 采用按 Principal/Scope/Environment/Permission Epoch 分区或隔离的 Cache。
- 将 Retrieval Result 设计为不可变、带版本和 Completeness 的结果对象。
- 将异步预取与高风险动作前的同步重新校验组合使用。

### TO_VALIDATE（必须通过原型/基准验证）

- ANN 预过滤对目标索引的召回与性能影响。
- 多通道并发对 P95/P99 与资源占用的影响。
- Graph Fan-out、Provenance 展开与缓存失效的最坏成本。
- Rust Cancellation 对下游驱动/查询任务的实际中断能力。
- Watermark 落后时 Canonical delta fallback 的成本与一致性。
- 不同 Cache Key 粒度下的命中率与隔离开销。

### OPEN（阻断契约冻结）

- F 的正式 Query/Result/Recommendation Schema。
- Runtime Session 的可信身份绑定结构。
- Index Watermark 的分区、快照与混合版本语义。
- Permission Revocation 与 Forget 对在途查询的线性化/检查点语义。
- Cache/Working Set 的失效与读时授权协议。
- F 与 G 的 Context Candidate 交接契约。
- 多通道资源预算、Early Stop 与 Completeness 的统一语义。

---

## 12. 修复顺序与退出条件

| 顺序 | 工作 | Owner | 退出条件 |
|---|---|---|---|
| 0 | 提交 F 五份核心设计文档 | F | 文件可读取、版本和状态完整 |
| 1 | 冻结 Scope/Permission/Identity 接口 | I + B + F | Scope-before-Candidate 逐通道矩阵通过 |
| 2 | 冻结 Forget/Tombstone/Revocation 契约 | I + D + E + F | Forget 与撤权能阻断索引、缓存、工作集及在途任务 |
| 3 | 冻结 Canonical/Index Watermark 契约 | D + E + F | Lag、重建、部分结果和版本新鲜度可识别 |
| 4 | 冻结 Retrieval Query/Result Schema | F + D + E | Memory/Claim/Version/Provenance 引用完整 |
| 5 | 冻结 Activation Recommendation 与 G 接口 | F + G | Result、Recommendation、Context Candidate、Context Entry 分层 |
| 6 | 冻结 Working Set/Cache 与 Session 隔离 | F + I | Cache Key、失效、Readback 与撤权验收通过 |
| 7 | 完成 Scheduling 与 Benchmark Plan | F | 预算、取消、背压、尾延迟测量方案可复现 |
| 8 | 重新进行三方六维度审查 | 独立审查 | P0 关闭；P1 关闭或有批准的决议与风险接受 |

### 12.1 审查通过退出条件

只有全部满足以下条件，才能将本报告状态改为 Pass：

1. 五份 F 核心文件完整提交。
2. 不存在未关闭的 P0。
3. Scope-before-Candidate 覆盖所有检索通道。
4. Graph Expansion、Reranker、Cache、Working Set、Result Serialization 不绕过授权。
5. Forget 后不再从索引、缓存、工作集、旧快照或在途查询返回目标记忆。
6. Index 延迟、Watermark 与结果不完整性可识别。
7. Runtime 不拥有 Canonical Memory 或 Context Version。
8. F 的输出接口能被 G 正确消费。
9. Trust、Epistemic Status、Evidence、Source 与 Provenance 不因检索/排序丢失。
10. 性能目标与实测结果严格区分；Benchmark Plan 可复现。
11. Cancellation、Backpressure、Early Stop 与并发隔离有明确语义和验收测试。
12. 重新完成逐文件、逐通道和跨模块审查。

---

## 13. 最终审查决议

**结论：Review Blocked / Not Passed。**

当前仓库版本提供了足以约束 Runtime 的上位架构原则，但没有提供 Session F 核心设计文件。因此无法对 Runtime 的检索安全、Forget 一致性、缓存隔离、调度可实现性或 G 接口兼容性作出通过判断。

本报告不声称已发现 F 代码漏洞，也不声称完成了性能或渗透测试。它确认的是：在当前仓库证据状态下，关键风险尚未被设计文档排除。

**明确要求：**
- F Owner 补齐五份核心文档。
- I/D/E/G 分别确认其授权、Canonical、Index、Context 接口。
- 在 Scope-before-Candidate 与 Forget 阻断证明完成前，不得冻结 F 安全契约或放行相关实现。
- 文档补齐后重新审查，不得把本报告中的 PARTIAL 自动改为 PASS。

**审查局限：** 本报告只基于本次可读取的默认分支文件与提交历史；未检查未提交工作区、其他分支或外部设计稿。三个角色是专业视角模拟，不代表真实三人独立签署。
