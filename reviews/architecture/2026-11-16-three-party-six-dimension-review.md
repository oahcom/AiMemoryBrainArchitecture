# 三方六维度架构审查报告

- **审查日期：** 2026-11-16
- **审查对象：** AI Memory Brain 当前系统架构基线及 System Architecture 深化文档
- **审查类型：** 静态架构设计审查（非代码审计、非运行测试）
- **结论状态：** 有条件通过；P0 风险关闭前不建议冻结架构
- **审查文件归属：** `reviews/architecture/`

> **审查方法说明：** “三方”指三个互相独立的审查视角：系统架构、工程实现、安全与可靠性。本报告由同一审查流程按三个视角分别推演，不代表三名独立审查人员或三个独立模型已实际签署意见。结论属于设计审查判断，尚未由实现与运行测试验证。

---

## 1. 审查范围与依据

### 1.1 纳入审查的文档

系统架构深化文档：

- `01-system-architecture/system-boundaries.md`
- `01-system-architecture/data-flows.md`
- `01-system-architecture/component-interactions.md`
- `01-system-architecture/system-quality-attributes.md`

架构基线与治理文档：

- `README.md`
- `ARCHITECTURE_ROADMAP.md`
- `00-governance/design-principles.md`
- `00-governance/architecture-invariants.md`
- `00-governance/terminology.md`
- `01-system-architecture/system-overview.md`
- `01-system-architecture/component-map.md`
- `01-system-architecture/responsibility-matrix.md`

### 1.2 审查限制

本报告根据上述文档进行静态审查。它没有验证 Rust 实现、数据库事务、协议报文、并发行为、性能数据或安全测试结果。报告中提出的风险是设计层面的风险判断，不应误读为已复现的实现缺陷。

本报告也不替代 Memory Domain Model、Agent Integration、BMCP、安全治理等专项设计的详细审查。相关专项文档完成后，应进行跨文档一致性复核。

---

## 2. 三方审查视角与结论

### 2.1 第一方：系统架构师

**结论：原则通过。**

认可事项：

- Brain、Agent、LLM、Adapter、Environment Adapter、Skill Library 的职责边界总体清晰。
- Canonical Memory、Memory Context、Delivery State、Applied Evidence 的权属区分是正确的方向。
- Event Ingestion 与 Runtime Recall 被定义为不同逻辑通道，有利于隔离延迟和故障。
- 逻辑组件不等同于独立部署单元，允许先采用 Modular Monolith。

需要收敛的事项：

- 明确 Brain 的记忆激活决策与 Agent 的任务决策之间的权力边界。
- 明确 Memory Context 是 Brain 管理的上下文载体，不是 Agent 必须服从的指令。
- 进一步定义 Entity Identity、Claim Revision、Temporal Validity、Contradiction Management。
- 明确“记忆相关性/适用性”与“事实真实性/可信度”不可互相替代。

### 2.2 第二方：工程实现负责人

**结论：有条件通过。**

认可事项：

- 以 Rust Modular Monolith 为初始实现形态，避免过早分布式化。
- Canonical Store、Index、Cache 的权威性与可重建性已有基本区分。
- 异步编译、幂等处理、重放恢复和 Context 版本化已有设计方向。

需要收敛的事项：

- 跨组件状态转换必须落到可实现的状态机和持久化契约。
- Canonical 更新与 Index 更新之间需要明确事务外盒、版本水位线、重放和修复策略。
- Context 并发编辑需要明确乐观并发控制、冲突检测和合并/拒绝规则。
- Sync 的投递状态和 Adapter 的应用证据需要定义可验证的关联标识。
- 逻辑组件应按领域边界组织，不应机械地变成独立服务、队列或数据库。

### 2.3 第三方：安全与可靠性审计者

**结论：P0 风险关闭前暂不建议冻结。**

认可事项：

- Scope 与 Permission 分离。
- 外部输入、遥测、环境观察和检索记忆均被视为不可信数据。
- Brain 不拥有 Agent 工具执行权或环境直接控制权。
- Forget 与 Context Remove 被明确区分。

需要收敛的事项：

- 记忆内容即使作为数据注入，也可能通过自然语言影响模型；“不是指令”这一标记本身不足以构成防护。
- Scope 隔离必须贯穿检索、重排、图扩展、缓存、上下文构建、日志和派生数据。
- Forget 必须定义 Canonical、索引、缓存、派生记忆、备份及外部模型边界上的删除语义。
- Adapter 的 Applied 证明只能覆盖约定的上下文安装边界，不能推断模型注意、理解或采用了记忆。

---

## 3. 六维度审查

### 维度一：架构边界

**判断：基本通过，需明确决策权边界。**

当前设计将记忆管理与 Agent 推理/行动分离，避免 Brain 演变为 Agent Orchestrator。

待明确：

1. Brain 可以决定候选记忆的检索、排序、激活和 Context 管理策略。
2. Agent 仍负责判断这些记忆对当前任务的适用性，并独立决定行动。
3. LLM 只执行 Agent 组织的推理请求，不成为 Canonical Memory 或 Applied 状态的权威。
4. Context 中的记忆不能覆盖系统/开发者指令、用户输入或 Agent 安全策略。

建议将“Brain 提供记忆建议与受治理的上下文管理”写为边界原则，避免把激活结果误解为 Agent 必须执行的命令。

### 维度二：领域模型

**判断：基础术语划分合理，语义完整性仍需专项设计。**

当前已区分 Event、Memory、Fact/Claim、Entity、Relation、Evidence、Provenance、Epistemic Status、Lifecycle State、Confidence 和 Relevance。

主要风险：

- 来源陈述被错误提升为已验证事实。
- Entity 名称相似导致身份错误合并。
- Claim 更新覆盖历史主张，导致无法追溯。
- 时间有效性、记录时间和事件时间混淆。
- 相关性分数被误用为真实性或置信度。

建议后续专项明确：

- Claim 的提出、支持、反驳、修订、撤回与失效。
- Entity Resolution 的候选、确认、合并、拆分和回滚。
- Evidence 与派生 Claim 的可追溯关系。
- Temporal Validity 与 Event Time / Recorded At 的语义。
- Confidence 的校准方法和适用范围。

### 维度三：数据流与一致性

**判断：流程方向正确，恢复与并发契约需要补齐。**

当前流程中 Accepted、Compiled、Canonical、Indexed、Retrieved、Activated、Delivered、Applied 是不同阶段，不能合并成一个“完成”状态。

重点风险：

1. Canonical 已提交而 Index 更新失败，导致记忆存在但检索不可见。
2. Outbox/队列消息重复或乱序，造成重复处理或旧版本覆盖新版本。
3. Context 多写者并发更新，产生丢失更新或错误合并。
4. Adapter 断线重连后，Snapshot/Delta 基线不一致。
5. Applied 回执与具体 Context Version、Inference Request 关联不足。

建议：

- Canonical 变更与待发布事件使用事务性 Outbox 或等价的可恢复机制。
- Index 记录其已处理的 Canonical Version / Watermark，并提供滞后监测与重建。
- 对写操作定义幂等键、重试边界和重复请求返回语义。
- Context 使用明确的 base_version / expected_version 进行并发控制。
- Applied 回执关联 Adapter Instance、Context ID、Context Version、Change Set ID、Inference Request ID 和应用时间。
- Applied 只表示 Adapter 在约定推理边界安装了指定上下文，不代表模型理解或使用。

### 维度四：安全与治理

**判断：原则已建立，但威胁模型与删除闭环不足。**

#### P0-A：Forget 全链路语义

需要定义 Forget 的目标范围和各数据层的处理结果：

- Canonical Memory 与版本历史。
- Evidence / Provenance 与原始事件载荷。
- 全部派生索引、向量、图关系和搜索缓存。
- Runtime Working Set、Context Entry 和待投递 Change Set。
- 备份、快照、灾备副本与保留期。
- 已经发送给外部 LLM / 第三方服务的数据。

不能笼统承诺所有外部副本立即物理删除。应区分逻辑删除、在线派生数据清理、备份到期清理和无法控制的外部副本，并给出可审计状态与限制说明。

#### P0-B：记忆内容的指令注入风险

记忆即使被标记为“不可信数据”，也可能通过自然语言语义影响 LLM。

建议建立：

- 来源身份、信任等级和证据类型。
- 不可信/外部内容的显式标记。
- 高风险指令性内容检测与隔离策略。
- Agent 对高影响记忆的独立验证。
- 工具权限与行动授权始终由 Agent 自己的策略决定。
- 对抗性记忆注入测试集及回归测试。

检测器只能降低风险，不能被当作完备防线。

#### P0-C：Scope 隔离贯穿全链路

Scope 校验不应只发生在 API 入口或最终输出阶段。必须覆盖：

- Retrieval Candidate Generation。
- Reranking 与 Graph Expansion。
- Index / Cache Key。
- Working Set 与 Context Planning。
- 派生记忆与跨 Scope Consolidation。
- 日志、诊断和审计数据。
- Forget、Export、Backup 与恢复。

必须确保未经授权的数据不会先进入候选集合，再依赖最终渲染过滤。

### 维度五：性能与资源

**判断：部署方向合理，性能目标需要真实工作负载验证。**

建议采用：

- Rust Modular Monolith。
- 领域模块内部明确接口，避免无必要的网络调用。
- Canonical 数据与可重建 Index 分离。
- Event 编译异步化，持久化接收不依赖同步 LLM 推理。
- CPU / RAM / Disk / GPU 分别设置预算与背压。
- 向量检索与结构化、关键词、时间、关系检索组合路由。

不要在缺少工作负载和基准数据时承诺固定延迟或吞吐量。

建议至少建立以下基准：

1. 无记忆 Agent 基线。
2. 简单向量检索基线。
3. Brain 多路检索基线。
4. 检索 + Activation + Context 管理基线。
5. 确定性编译与模型辅助编译的质量/成本对比。

测试报告应记录数据规模、并发量、硬件、模型、上下文预算和缓存状态。

### 维度六：可演进性与可观测性

**判断：设计方向正确，协议兼容和端到端追踪仍需细化。**

BMCP 应成为版本化协议契约，而不是某个 Agent 框架的私有 API。

需要定义：

- Principal / Workload Identity。
- Protocol Version Negotiation。
- Capability Negotiation。
- Snapshot / Delta 语义。
- 幂等键与重放语义。
- 兼容性、弃用和迁移策略。
- Adapter 应用回执的可信边界。
- 跨组件 Correlation ID / Causation ID。

可观测性至少需要串联 Event → Compilation → Canonical Change → Index Watermark → Retrieval → Activation → Context Version → Delivery → Adapter Applied Evidence。

---

## 4. 风险清单与优先级

| ID | 优先级 | 风险 | 主要影响 | 建议状态 |
|---|---|---|---|---|
| AR-001 | P0 | Forget 全链路删除语义不完整 | 删除承诺不可靠、残留数据 | OPEN |
| AR-002 | P0 | 记忆指令注入缺少完整防护模型 | 影响 Agent 行为与工具安全 | OPEN |
| AR-003 | P0 | Scope 隔离未形成端到端验证闭环 | 跨用户/环境信息泄露 | OPEN |
| AR-004 | P1 | Canonical 与 Index 一致性/修复策略不足 | 记忆存在但不可检索 | OPEN |
| AR-005 | P1 | Applied 证据语义可能被过度解释 | 错误推断模型已理解/使用 | OPEN |
| AR-006 | P1 | Entity 合并与 Claim 冲突规则待细化 | 长期知识污染 | OPEN |
| AR-007 | P1 | Context 并发版本控制待定义 | 丢失更新、上下文错乱 | OPEN |
| AR-008 | P1 | BMCP 身份、版本和兼容策略待明确 | 多 Agent 集成成本上升 | OPEN |
| AR-009 | P2 | 逻辑组件可能被过度服务化 | 本地部署复杂度和资源开销 | MONITOR |
| AR-010 | P2 | 缺少代表性工作负载的量化基准 | 无法客观验收质量属性 | OPEN |

---

## 5. 架构整改建议与验收标准

### 5.1 冻结前必须完成（P0）

**AR-001 Forget**

验收标准：

- 明确每种数据副本的删除状态与时限。
- Forget 请求可追踪、可重试、幂等。
- 在线索引、缓存、Working Set 和 Context 均有清理或失效确认。
- 备份与外部模型边界有明确限制和用户可理解的结果状态。
- 有删除失败、部分完成和恢复后的审计测试。

**AR-002 Memory Prompt Injection**

验收标准：

- 外部内容来源与信任标签可沿 Provenance 保留。
- 记忆内容不能获得系统/开发者指令权限。
- 记忆不能自行授予工具权限或触发外部行动。
- 建立恶意记忆、间接提示注入和多轮诱导测试。
- 高风险行动仍由 Agent 独立授权和验证。

**AR-003 Scope Isolation**

验收标准：

- 未授权数据不会进入检索候选、图扩展、重排或上下文。
- 缓存键和索引分区能够表达必要的 Scope 边界。
- 跨 Scope Consolidation 有明确授权与来源保留规则。
- 对查询、导出、日志、备份、恢复和 Forget 进行隔离测试。
- 任意越权访问均产生无敏感内容泄露的拒绝结果和审计记录。

### 5.2 实现设计前必须明确（P1）

- Canonical / Index 版本水位线、Outbox、重放和修复策略。
- Applied 的精确定义与回执关联字段。
- Entity 合并/拆分、Claim 修订/冲突的状态机。
- Context 乐观并发控制与版本冲突处理。
- BMCP 身份、能力协商、协议版本与兼容策略。

### 5.3 运行验证阶段完成（P2）

- Modular Monolith 模块边界与资源预算。
- 多路检索与模型辅助编译的工作负载基准。
- 端到端可观测性与故障演练。
- Agent 任务层面的真实效用评估。

---

## 6. 决议

1. **保留现有系统总体方向与核心职责边界。**
2. **不因本次审查推翻现有逻辑组件划分。**
3. **不将 16 个逻辑组件直接解释为 16 个独立服务。**
4. **P0 三项风险必须进入专项设计和验收。**
5. **P1 项目在详细实现接口冻结前完成定义。**
6. **专项文档完成后，进行 System Architecture、Memory Domain Model、Agent Integration、BMCP 和 Governance 的交叉一致性审查。**
7. **本报告不代表架构已通过代码、安全或性能验证。**

## 7. 后续审查记录

| 审查轮次 | 范围 | 状态 |
|---|---|---|
| Round 1 | 三方六维度静态架构审查 | 本报告 |
| Round 2 | Memory Domain Model / Agent Integration 交叉审查 | 待专项文档齐备 |
| Round 3 | P0 风险整改复审 | 待整改方案完成 |
| Round 4 | 实现与运行验证 | 待原型实现和测试数据 |

---

**报告结束**
