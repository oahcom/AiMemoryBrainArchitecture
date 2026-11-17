# Phase 1 — A/B/C 跨文档架构集成审查报告

- 审查日期：2026-11-16
- 审查对象：Session A System Architecture、Session B Memory Domain Model、Session C Agent Integration，以及三份对应的三方六维度审查报告
- 审查类型：跨文档静态集成审查（非代码审计、非运行测试）
- 结论：**Conditional Pass — 允许进入受控的子系统深化设计；不允许冻结核心领域 Schema、BMCP 接口或安全/删除保证**
- 报告归属：`reviews/integration/`

> 本报告是对仓库现有文档及其审查报告的横向综合，不代表三名独立审查人员或三个独立模型签署。报告中列出的是文档层面的冲突、缺口和待验证风险，不代表已在运行实现中复现。

---

## 1. 审查材料与范围

### 1.1 设计基线
- `README.md`
- `ARCHITECTURE_ROADMAP.md`
- `00-governance/design-principles.md`
- `00-governance/architecture-invariants.md`
- `00-governance/terminology.md`
- `01-system-architecture/*`
- `02-domain-model/*`
- `07-agent-integration/*`

### 1.2 专项审查报告
- `reviews/architecture/2026-11-16-three-party-six-dimension-review.md`
- `reviews/architecture/2026-11-16-memory-domain-model-three-party-six-dimension-review.md`
- `reviews/07-agent-integration/three-party-six-dimension-review.md`

### 1.3 本轮不做的事
- 不审计 Rust 代码、数据库事务或实际 Adapter。
- 不验证性能、隔离、Forget、提示注入防护是否已在实现中成立。
- 不替各子系统 Owner 擅自关闭其审查报告中的问题。
- 不把 C 的 BMCP wire contract、G 的 Context 内部模型、I 的治理执行模型视为已经完成。

---

## 2. 总体结论

A/B/C 的主架构方向彼此兼容，最重要的权力边界没有发生根本冲突：

1. Brain 拥有 Canonical Memory 与其管理的 Memory Context 的逻辑权威。
2. Agent 拥有推理、规划、行动选择、工具执行及行动安全策略。
3. Adapter 负责 Agent 原生遥测映射，并在推理上下文组装边界应用 Brain 管理的记忆区域。
4. Event、Memory、Claim/Fact、Evidence、Entity、Relation、Context 是不同层次的语义对象，不应被压成一个“记忆记录”。
5. Telemetry Accepted、Memory Compiled、Context Delivered、Context Applied 是不同阶段事实。
6. Context Remove 不等于 Canonical Memory Forget；Applied 不等于模型理解或使用。
7. Scope 与 Permission 分离；Memory/Telemetry 是数据，不具有系统指令或工具授权权力。
8. 逻辑组件不等于进程、服务或 Rust crate；模块化单体仍是合理的初始工程候选。

但当前材料还不能组成一套可冻结的统一契约。跨文档审查发现 **1 项明确的规范基线冲突、3 组安全/治理冻结门槛、6 组关键跨模块接口缺口**。其中部分已被专项报告单独指出，本报告进一步明确它们之间的依赖关系和处理顺序。

---

## 3. 跨文档一致性矩阵

| 主题 | A 系统架构 | B 领域模型 | C Agent 集成 | 集成判断 |
|---|---|---|---|---|
| Brain / Agent 权责 | Brain 管记忆与 Context；Agent 管行动 | Domain Model 不接管 Agent 决策 | Adapter 不改写 Brain 规则 | 一致，保留 |
| Event / Memory / Claim / Evidence | 要求区分领域对象 | 对象分层较完整，但 Fact/Claim 与基线冲突 | Telemetry 不等于 Event/Memory | 有一项 P0 规范冲突 |
| Context 权威与版本 | MCM 管理 Context 版本 | Context Version / Change Set 结构未完整规范 | Adapter 消费版本并回执 | 语义一致，数据契约缺口 |
| Scope / Permission | 端到端隔离要求 | 通用 Scope 结构与过滤验收需补齐 | 身份绑定依赖 B/I/H | 方向一致，授权链缺口 |
| Telemetry | 作为激活信号与事件输入 | Event/Evidence/时间语义提供基础 | Schema 与状态模型较细 | Observation/Outcome 与 revision 规则未闭合 |
| Accepted / Applied | 阶段必须区分 | 持久化与版本对象需要支持 | Accepted/Applied 证明要求明确 | 事务和证明链需协议化 |
| Forget / Retention | P0 风险 | Forget Operation 与依赖图缺口 | 撤权/离线缓存传播缺口 | 必须跨 B/C/H/I/G 共同定义 |
| Memory Prompt Injection | 数据不提升为指令 | 来源、Trust、Evidence 可承载风险信息 | Adapter 明确非安全边界 | 原则一致，运行防护与测试未闭环 |
| Index / Provenance / Recovery | Canonical 与 Index 分离 | Provenance DAG、生命周期双路径未定 | Accepted 依赖耐久处理 | 需 E/I/Consistency 落地 |

---

## 4. P0：冻结前必须解决

### INT-P0-01 — Fact 与 Claim 的规范基线冲突

**来源：** B 审查报告 DM-001。

治理基线 `architecture-invariants.md` I-04、`design-principles.md` P-04 及 README 将 Fact 与 Claim 列为不同领域概念；Domain Model Overview 则将 Claim 定义为规范命题对象，并把 Fact 解释为 Claim 的一种资格/解释，而非独立对象。

**影响：** Brain Store、Compiler、检索、API、历史版本与测试可能形成两套不兼容对象模型。这是当前唯一已明确定位到规范基线文字冲突的 P0。

**裁决要求：**
- 必须建立 ADR，明确选择“Fact 独立对象”或“Fact 是 Claim 的资格/解释”。
- 若统一对象，必须同步修改 I-04、P-04、README、术语表和所有引用。
- 若独立对象，必须定义身份、生命周期、Evidence 关系、验证/派生关系和权限语义。
- ADR 被批准前，不得冻结 Canonical Schema、Compiler 输出 Schema 或公开 API 中 Fact/Claim 的身份语义。

**Owner：** Architecture Governance + Session B；Session D/E/F 参与影响分析。

### INT-P0-02 — Scope 隔离必须成为全链路安全不变量

**来源：** A 审查 AR-003；B 审查 DM-010；C 审查 P1-03/P1-07。

Scope/Permission 的原则已经一致，但三份材料共同表明：仅在入口或最终输出时授权不够。Scope 必须在候选生成前生效，并贯穿图扩展、重排、聚合、缓存、Working Set、Context、日志、导出、备份、恢复和异步任务。

**冻结要求：**
- 明确 Principal / Producer / Agent / Agent Instance / Session / Task / Environment 的可信身份绑定链。
- 每次受保护操作按当前主体、资源 Scope、操作权限和授权版本判定；不得信任 Agent 自报 Scope 或 display name。
- 检索候选生成前执行 Scope 过滤；关系扩展的边和目标节点都重新授权。
- 缓存键必须绑定足以区分主体、Scope、Environment、权限/撤销版本的维度。
- Accepted→Applied、reconnect、reconciliation 和异步任务执行阶段必须重新检查授权。
- 建立跨 Scope 的自动化负向测试矩阵。

**Owner：** Session I 主责；B 定义 Scope 语义；C/H 定义身份与操作边界；D/E/F/G 落实各自数据路径。

### INT-P0-03 — Forget 全链路语义与完成证明必须闭环

**来源：** A 审查 AR-001；B 审查 DM-011；C 审查 P1-07。

三份材料均承认 Forget 不能只删除 Canonical 主记录。必须覆盖版本历史、原始 Event/Evidence、Provenance 派生对象、索引、向量、图关系、缓存、Working Set、Context Entry、待投递 Change Set、备份/快照以及外部模型边界。

**冻结要求：**
- 定义 Forget Operation 的目标、授权、幂等、依赖发现水位、访问阻断时间、阶段状态、重试、完成证明和残留例外。
- 先阻断访问，再异步清理派生副本；部分失败不得报告完成。
- 明确在线数据、备份保留期、外部模型/第三方副本各自的删除保证与不可控边界。
- Provenance lineage 必须定义 DAG 或受限循环规则，否则依赖发现和清理覆盖无法证明。
- Forget 与 Retention、幂等记录保留、离线 Adapter 缓存失效必须协调。
- 审计记录不能保留足以重建被忘记内容的敏感载荷。

**Owner：** Session I 主责；B 定义对象与依赖语义；D/E/G/H 定义各自副本清理和同步；测试阶段验证。

### INT-P0-04 — Memory Prompt Injection 作为残余风险必须进入威胁模型

**来源：** A 审查 AR-002；C 审查 P2-07；B 安全维度。

“Memory 是数据而不是指令”是必要的权限原则，但不是模型行为层面的充分防护。自然语言记忆仍可能影响模型，文本分隔符也不是安全边界。

**冻结要求：**
- 保留来源身份、Trust、Epistemic Status、Evidence 与派生链。
- managed region 使用结构化承载和明确来源/信任标签；不得携带工具授权或提升指令层级。
- 明确检测/隔离只能降低风险，不能承诺完全防止模型受影响。
- Agent 的工具权限、行动授权和安全策略始终由 Agent 自身策略控制。
- 验收包含恶意记忆、伪造 system 标签、跨 Scope 记忆和多轮间接提示注入。
  
**Owner：** Session I 主责；C/H 定义 Adapter 与协议边界；B/E 保留来源与信任语义；Agent 侧负责行动授权。

---

## 5. P1：详细接口冻结前必须解决

### INT-P1-01 — Context Version / Change Set 的统一权威模型

**关联：** A 的 Context 并发控制与 Applied 关联；B 的 DM-002；C 的 P1-06、P2-05、P2-06。

必须明确：
- Context Version 是不可变快照还是可重建版本指针。
- Change Set 的 base_version、target_version、parent、提交身份、幂等键、原因、摘要和操作列表。
- 同一 Context 的并发提交策略（串行化或 CAS）；版本冲突如何拒绝/重算。
- Snapshot 的完整替换语义；Delta 的原子性、重复应用和局部失败回滚。
- Applied 必须关联 delivery、Context Session、目标版本、capability epoch 和本次 inference request。
- timeout/迟到 ack/重试通过统一 reconciliation 查询模型处理。

**Owner：** Session G 主责；H 定义 wire 与重试；C 定义 inference boundary 证明条件。

### INT-P1-02 — Claim 身份、修订、冲突与 Entity Merge/Split

**关联：** B 的 DM-003/004/009；A 的 AR-006。

必须统一：
- Claim ID 跨 Memory Version 是否稳定；修订采用 successor 还是稳定 ID + immutable revision。
- Conflict / Conflict Set 的参与 Claim、冲突维度、Evidence、裁决历史和未决状态。
- Entity Merge/Split 的 ID 映射、旧引用处理、回滚/纠错记录。
- Relation retract/supersede 的原因、主体、时间和不可变历史。
- 历史查询、索引更新、Provenance 和 Context 引用如何处理修订。

**Owner：** Session B 定义领域语义；D/E 负责持久化和编译/冲突处理；F 负责检索投影。

### INT-P1-03 — Telemetry 的身份、事件语义与乱序规则

**关联：** C 的 P1-01/P1-02/P1-03；B 的 Scope/Time/Actor 语义。

必须统一：
- Environment Adapter 是单路还是双路接入；图示不得暗示双提交。
- Observation 与 Outcome 的判别规则、边界示例及 Evidence 关系。
- Producer → Agent → Agent Instance → Session/Task/Environment 的身份绑定。
- Task/Plan/Intent/Pending Action 的 revision、撤回、过期与乱序处理。
- source_kind 的 Envelope producer 与 payload observation source 是否为不同维度。
- Risk severity/confidence 是来源自述值还是 Brain 评估值，不得直接作为授权依据。

**Owner：** Session C + B；H 定义消息契约；I 定义身份授权；E 定义事件耐久接收。

### INT-P1-04 — Telemetry Accepted 的持久化和幂等事务边界

**关联：** C 的 P1-04/P1-05；A 的 Canonical/Index 一致性要求。

必须定义 Accepted 的最低耐久承诺：原始 envelope、Scope、幂等身份、receipt 与后续处理任务必须处于可恢复提交边界。相同 key + 相同规范化 payload 返回原 receipt；相同 key + 不同 payload 返回明确冲突。定义提交前、提交后响应前、响应后处理前的崩溃测试。

**Owner：** Session E 主责；H 定义协议字段；I 定义权限与保留；Consistency/Recovery 定义 Outbox/replay。

### INT-P1-05 — Applied 必须能证明最终请求边界上的完整应用

**关联：** C 的 P1-06；A 的 AR-005；B 的 Context Version。

Applied 的必要条件应为：目标版本完整物化于受控 managed region，且该区域属于本次实际提交给 inference runtime 的最终请求上下文。不能观测最终提交点的 Adapter 不得声称 Tier 1。定义 full/partial/bypassed/unknown coverage、request/boundary correlation、重试唯一性及 digest 规范化/隐私边界。

**Owner：** Session G + H 主责；C 负责 Tier conformance；I 负责权限撤销检查点。

### INT-P1-06 — Provenance、Lifecycle 与引用类型需要唯一语义

**关联：** B 的 DM-006/007/008；A 的 AR-004。

必须定义：
- Provenance DAG 或受限循环规则、空来源/未知来源语义、派生节点唯一目标。
- Lifecycle 状态权威究竟由不可变 Memory Version 还是 append-only lifecycle event 承载，不能形成双权威。
- TimeValue、TimeInterval、TypedObjectRef、ContentRef、ScopeRef、ActorRef、TypedPredicate/TypedValue 的最小结构和未知值规则。
- Canonical commit、outbox publication、Provenance visibility、Index watermark 的一致性/恢复语义。

**Owner：** B 定义领域契约；D/E/I/Consistency 落地。

---

## 6. P2：后续设计与原型阶段必须纳入

1. Telemetry 高频场景的背压、采样、批处理与优先级策略。
2. Context budget 超限、压缩、拒绝和压缩后版本语义。
3. Schema、枚举、Relation vocabulary 的注册、弃用、兼容和迁移规则。
4. 从 Telemetry → Event → Evidence/Provenance → Canonical Version → Index → Retrieval → Activation → Context Version → Delivery → Applied → Outcome 的端到端 correlation/causation chain。
5. 日志脱敏、指标 cardinality、原始证据与派生摘要的访问分级。
6. Scope 过滤、Provenance 深度、关系 fan-out、Conflict 检测、Forget 依赖发现的复杂度预算。
7. 性质测试与故障注入：重复、乱序、并发、崩溃窗口、迟到 ack、离线重连、权限撤销、Forget 部分失败。
8. 代表性 Agent 工作负载的性能和效用基准；不得以弱化安全检查换取性能数字。

---

## 7. 依赖关系与整改顺序

建议按以下顺序推进，不要让并行会话各自发明同一接口：

| 顺序 | 工作 | 依赖 | 主要 Owner |
|---|---|---|---|
| 1 | ADR：Fact vs Claim | 无；先解决规范基线冲突 | Architecture Governance + B |
| 2 | 统一 Scope/Identity/Permission contract | ADR 与 B 的 Scope 语义 | B + I + C + H |
| 3 | Forget/Retention/Provenance dependency contract | Scope、Provenance、Lifecycle | B + D/E + G/H + I |
| 4 | Context Version/Change Set contract | Context 领域对象 | G + H + C |
| 5 | Telemetry Event/Accepted/Idempotency contract | Scope/Identity、Event 模型 | C + E + H + I |
| 6 | Applied proof & inference request correlation | Context Version、Adapter boundary | G + H + C |
| 7 | Cross-system conformance & fault matrix | 上述契约稳定 | Testing + 全部 Owner |

---

## 8. 对下一阶段 D/E/F/G 的放行建议

**不建议把本报告理解成“所有后续工作必须停摆”。** 可以开始 D/E/F/G 的详细设计，但必须采用受控并行：

### 可立即开展
- D：Memory Brain 的职责、存储职责、生命周期流程和版本历史方案；Fact/Claim 相关 Schema 必须标记为 ADR-blocked。
- E：Event Ingestion、Compiler pipeline、Evidence/Provenance 流程；Accepted/Idempotency 与 Claim 输出契约必须标记为待跨模块决议。
- F：Retrieval 路由、候选生成和工作集设计；Scope-before-candidate 是强制不变量，不能等最终渲染才过滤。
- G：Context Architecture、MCM 职责、Context Sufficiency 与预算策略；Context Version/Change Set 先给出候选模型，待统一接口审查后冻结。

### 当前不得冻结
- Fact/Claim 的规范身份和存储 Schema。
- Scope/Permission 与 Principal/Producer 身份的最终 wire contract。
- Forget 的“已完成”承诺与外部副本物理删除保证。
- BMCP 的 Accepted/Idempotency/Applied 最终消息契约。
- Context Snapshot/Delta 的原子提交与最终 Applied 证明协议。

### 并行协作纪律
- 每个会话只写自己的独占路径。
- 公共基线、术语表、ADR、接口契约由总控统一修改；子会话只能提出变更建议。
- 所有跨模块依赖必须引用本报告的 INT-* ID。
- 新设计必须标记 DECIDED / CANDIDATE / TO_VALIDATE / OPEN。
- 专项审查报告中的 P0/P1 不得因进入下一阶段而自动视为关闭。
- 所有文件写入后由总控做一次合并审查，不允许并发会话相互覆盖。

---

## 9. 阶段门禁与验收标准

### Gate 1 — Domain Baseline
- INT-P0-01 有批准的 ADR，所有基线文档同步。
- Claim revision、Conflict Set、Entity Merge/Split 的责任与候选语义明确。

### Gate 2 — Security & Governance
- Scope/Permission 身份绑定和端到端过滤矩阵有明确 Owner 与测试要求。
- Forget 各数据层状态、保留期、外部边界和部分失败语义明确。
- Prompt injection 残余风险、Agent 行动授权边界和对抗性测试要求明确。

### Gate 3 — Context & Integration Contract
- Context Version/Change Set、Snapshot/Delta、并发、幂等、reconciliation 有统一规范。
- Accepted 与 Applied 的必要条件可自动化测试。
- Adapter capability tiers 与最终请求边界证明不夸大能力。

### Gate 4 — System Conformance
- 跨 Scope 负向测试、Forget 故障注入、Telemetry 崩溃窗口、Context 乱序/重复/并发、Applied 最终请求关联均有测试计划。
- 所有 P0 已关闭；P1 已关闭或有明确 ADR/接口决议和 Owner。
- 性能和 Agent 效用仍以实测为准，不得使用未验证的倍率承诺。

---

## 10. 最终决议

**A/B/C 的总体架构方向通过；当前阶段整体状态为 Conditional Pass。**

可以启动 D/E/F/G 的受控详细设计，但必须把 INT-P0-01 作为首要 ADR，把 INT-P0-02/03/04 作为安全治理横向门禁，并把 INT-P1-01 至 INT-P1-06 作为跨模块接口任务。任何会锁定上述语义的 Schema、wire contract 或实现决策，都必须等对应决议完成后再冻结。

本报告只新增于 `reviews/integration/`，不修改 A/B/C 原始设计文档或其专项审查报告。
