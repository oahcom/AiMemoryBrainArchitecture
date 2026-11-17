# Session C — Agent Integration 三方六维度审查报告

**审查对象：** Session C — Agent Integration 的四份设计文档  
**审查日期：** 2026-11-16  
**审查方式：** 三方独立视角 × 六个架构维度  
**审查结论：** 有条件通过（Conditional Pass）；核心边界设计方向正确，但若干接口语义必须在进入协议冻结和实现前补齐。  
**风险概览：** P0：0；P1：6；P2：8。  
**范围说明：** 本报告审查逻辑架构和可验证契约，不代表 BMCP wire schema、Session G Context 数据模型或 Session I 治理策略已完成审查。

---

## 1. 审查基线与对象

### 1.1 审查文档

1. `07-agent-integration/agent-integration-overview.md`
2. `07-agent-integration/telemetry-model.md`
3. `07-agent-integration/adapter-capability-tiers.md`
4. `07-agent-integration/inference-boundary-model.md`

### 1.2 对照基线

- `README.md`：产品定位、核心架构原则、状态标记。
- `ARCHITECTURE_ROADMAP.md`：子系统规格模板、设计阶段退出条件、实现准入规则。
- `00-governance/architecture-invariants.md`：I-01 至 I-22。
- `01-system-architecture/system-overview.md`：系统边界、主数据流、隔离模型。
- `01-system-architecture/component-map.md`：MR-03、MR-04、XF-02、XF-03、XF-04 等组件职责。
- `01-system-architecture/responsibility-matrix.md`：主责/协作关系。
- `02-domain-model/domain-model-overview.md`：Event、Memory、Claim、Evidence、Provenance、Scope、Context 的语义。

### 1.3 总体判断

Session C 正确坚持了几个重要原则：

- Brain 管理 Canonical Memory、Activation Policy 和 Brain-managed Context 的权威版本；Agent 仍拥有推理、规划、行动与工具执行。
- Telemetry 是有来源、有范围、有时间语义的数据，不是指令，也不是隐藏思维链的镜像。
- Intent、Plan、Pending Action 不等于已完成结果；Observation、Outcome、Evidence 不应混为一谈。
- Received、Accepted、Applied 是不同事实；Applied 只证明 Adapter 在指定推理边界应用了指定版本，不证明模型理解或遵从。
- Brain 只能修改专属 managed region，不能覆盖 system/developer、用户输入、Agent 安全策略或工具授权。
- Tier 1/2/3 描述集成能力，不代表 Agent 智力等级；低能力集成可以安全降级。

上述方向与 README、系统架构和 I-01、I-03、I-06 至 I-13、I-16 至 I-18 基本一致。

---

## 2. 风险优先级定义

| 级别 | 含义 | 处理要求 |
|---|---|---|
| P0 | 可能造成跨租户/跨用户严重泄露、不可恢复数据损坏、核心安全边界失效 | 冻结相关设计/实现，先修复 |
| P1 | 核心语义、状态、一致性或权限契约不完整，容易造成实现分叉或后续返工 | 协议冻结或实现前必须解决 |
| P2 | 重要但可通过后续接口细化、测试或 ADR 解决的问题 | 进入明确的后续任务，不得遗忘 |
| P3 | 文档表达、非关键优化或低风险补充 | 有需要时处理 |

本轮没有发现足以直接判定为 P0 的已证实缺陷；这不等于实现层不存在 P0 风险。

---

## 3. 六维度审查

## 维度一：架构边界

### 通过项

- Brain、Agent、Agent Adapter、Environment Adapter、LLM Runtime、Skill Library 的责任边界总体清晰。
- Agent 仍拥有推理、规划、行动选择、工具调用和外部行动安全策略；Brain 不成为 Agent Runtime。
- Adapter 是语义映射与边界应用执行者，不拥有 Canonical Memory 或 Activation Policy。
- Environment Adapter 负责观察与报告，不代表 Brain 执行环境动作。
- BMCP wire contract 留给 Session H，Context 语义和版本留给 Session G，符合组件主责原则。

### P1-01：Environment Adapter 的接入拓扑在图中被画成双路并行，文字却称其为待决方案

**位置：** `agent-integration-overview.md` 第 2、4、7、14 节。

架构图同时画出 Environment Adapter → Agent Adapter 和 Environment Adapter → BMCP Gateway；第 14 节又把“直连 Gateway 还是经 Agent Adapter 中继”标为 OPEN。图形容易被实现者理解为两条链路都必须存在。

**风险：**
- 同一环境观察可能被双重提交，造成重复事件或来源混淆。
- 环境身份、认证主体、幂等键由谁生成不明确。
- Agent Adapter 与 Environment Adapter 对同一观察进行不同规范化时，可能产生冲突。

**修正要求：**
- 将两种拓扑画成互斥的 A/B 方案，或明确主路径与可选路径。
- 明确环境观察的原始 producer、认证主体、scope 绑定、correlation_id 与 idempotency_key 的生成责任。
- 若允许双路，应定义唯一事件身份和去重规则。

**责任方：** Session C + Session H；环境授权由 Session I 确认。

### P2-01：Agent Adapter 与 Protocol Gateway 的运行时部署边界容易被误读

**位置：** overview 第 2、3、13 节。

文档区分了逻辑责任，但尚未明确 Adapter 是 Agent 进程内库、sidecar、独立服务还是多种实现形态。当前阶段不必强行选型，但需要明确“逻辑边界不等于进程边界”。

**建议：** 继承系统基线“逻辑子系统不自动意味着独立进程/crate”的原则，并把部署形态列为 OPEN/ADR，不应由逻辑图暗示。

### 本维度结论

<badge color="success">通过，附条件</badge>

责任边界设计正确。必须消除环境接入双路图示歧义，并将部署拓扑留在明确的实现决策流程中。

---

## 维度二：领域模型

### 通过项

- Telemetry 不被直接等同于 Event、Memory 或 Claim。
- Agent 报告、环境观察、工具结果保留来源差异。
- Intent、Plan Summary、Pending Action 与 Outcome 分离。
- Active Entity 的 mention 不自动等于 Canonical Entity。
- 未知、冲突、低可观测性等状态得到保留。
- 不要求收集完整 CoT，符合模型无关性与数据最小化原则。
- Context Remove 与 Canonical Memory Forget 分离。

### P1-02：Observation 与 Outcome 的语义重叠，尚缺少确定性判别规则

**位置：** `telemetry-model.md` 第 5.6、5.7 节。

Observation 被定义为来源报告“观察到的条件、事件或结果”；Outcome 又被定义为与 Action/Task/Plan Step 相关的“报告或观察结果”。同一工具返回值或环境状态变化可能同时满足两者。

**风险：**
- 不同 Adapter 对同一信号选择不同类型。
- Compiler 可能把同一来源结果重复编译为 Event/Claim。
- Outcome 可能被误当成更高可信度的 Observation，或反之。

**修正要求：**
- 明确 Observation 表达“来源观测到什么”；Outcome 表达“某个 Action/Task 的结果状态是什么”。
- 允许一个 Outcome 引用一个或多个 Observation/Evidence，但不要把两者定义成互斥替代物。
- 定义最小示例：工具返回 HTTP 200、环境中方块已放置、Agent 声称任务完成，分别如何表达。
- 说明 Outcome 的 result_status 是结果分类，不是 epistemic status；是否 Verified 仍由 Domain/Evidence 语义决定。

**责任方：** Session C + Session B + Session E。

### P1-03：Telemetry envelope 的身份字段与 Scope 结构未形成完整、可校验的语义契约

**位置：** `telemetry-model.md` 第 4、8、9 节；overview 第 5、10 节。

当前包含 producer_id、agent_id、agent_instance_id、session_id、task_id、environment_id 和 scope，但未规定它们之间的绑定关系，也未给出 scope 的规范组成/引用规则。Domain Model 已区分 Agent Scope 与 Environment Scope；系统架构也明确 Scope 与 Permission 分离。

**风险：**
- producer_id 可能代表 Adapter，也可能被误当作 Agent 身份。
- Agent 实例、用户、项目、Session、Environment 的归属关系可能由各 Adapter 自行解释。
- 一个合法 Agent 身份可能被错误地用于其他 Agent instance 或 Environment 的数据写入。
- 仅校验 scope 字符串不足以证明 producer 有权访问该 scope。

**修正要求：**
- 明确 producer_id 是经过认证的 Adapter/producer 主体；agent_id 是其代表的逻辑 Agent 身份。
- 定义身份绑定校验：producer → Agent → Agent instance → session/task/environment 的授权关系。
- scope 必须引用 Session B 的规范 Scope 模型，不要在 Agent Integration 内另造一套平行结构。
- 每个操作都执行授权检查；scope 仅表示命名空间，不等于权限。

**责任方：** Session B + Session I + Session H；Session C 负责消费并写清语义。

### P2-02：source_kind 枚举在 Envelope 与 Observation payload 中命名不一致

**位置：** `telemetry-model.md` 第 4、5.6 节。

Envelope 使用 Agent/environment/user/tool/external；Observation 使用 environment/tool/agent_report/user/external。Agent 与 agent_report 的区别没有定义。

**建议：** 统一规范枚举，或明确 envelope 的 producer/source 身份与 payload 的 observation source 是不同层级；禁止靠自由文本推断。

### P2-03：Task/Plan/Action 的更新、撤回和乱序语义不足

**位置：** `telemetry-model.md` 第 5.1–5.5、8、10 节。

文档定义了状态集合，但没有规定状态转换合法性、修订号、过期更新处理、并发上报和乱序到达规则。

**建议：**
- 为可变逻辑对象定义 revision/sequence 或明确采用事件追加模型。
- 明确旧状态迟到时不能覆盖新状态。
- 对 Plan revised/abandoned、Intent withdrawn、Pending Action cancelled 等给出状态迁移约束。
- 不要把网络到达顺序当作业务发生顺序。

### P2-04：Risk Signal 与 confidence 的跨模块语义仍不够精确

**位置：** `telemetry-model.md` 第 5.4、5.9 节。

producer-reported severity 需要“documented semantics”，但没有规范等级或映射机制；confidence 也需要声明语义。Domain Model 明确 Confidence、Trust、Relevance、Evidence Strength 是正交维度。

**建议：** 明确这些字段是来源自述值，不是 Brain 认可的可信度；定义可选标准化映射，保留原始值和映射版本，不允许把风险等级或置信度直接当作授权依据。

### 本维度结论

<badge color="warning">有条件通过</badge>

主要语义方向正确，但 Observation/Outcome、身份与 Scope、状态修订三个问题必须在跨模块接口冻结前解决。

---

## 维度三：数据流与一致性

### 通过项

- Telemetry 接收与 Memory 编译被明确拆开。
- Accepted 被定义为耐久接收，不暗示 Memory 已创建。
- 幂等、重试、版本基线、快照恢复和 Applied 状态被纳入设计。
- Delta base 不匹配时拒绝或重建 Snapshot，不猜测版本。
- In-flight inference 不会被追溯性地改写。
- Adapter 重启后无法证明本地 applied watermark 时，要求重新同步。

### P1-04：Telemetry 接受、处理、事件持久化之间的事务语义尚不够具体

**位置：** `telemetry-model.md` 第 10、11、13 节；overview 第 7、9 节。

文档称 Accepted 表示 Brain durably accepted，并把 Accepted telemetry 视为耐久源记录；但没有明确它对应 Event Ingestion 的哪一个原子提交点，也没有明确 receipt 与原始 payload、幂等记录、outbox/后续处理任务之间的原子关系。

**风险：**
- 返回 Accepted 后进程崩溃，源记录已写但处理任务丢失。
- 幂等记录先写、payload 后写或反过来，产生无法重试的半状态。
- Accepted 的 durability 语义在不同存储实现中被解释为内存队列、单表写入或完整事务。

**修正要求：**
- 明确 Accepted 的最低承诺：原始 Telemetry/Event envelope、idempotency key、scope、receipt/acceptance identity 必须在一个可恢复的提交边界内持久化。
- 明确下游处理采用事务 outbox、可重建队列或等效机制。
- 定义崩溃点测试：提交前、提交后但响应前、响应后但处理前。
- 对“Processing/Processed”明确它们是可重试派生流程状态，不改变原始接受记录的身份。

**责任方：** Session C + Session E + Session H + Session K/一致性相关模块（以仓库责任分工为准）。

### P1-05：幂等键的作用域和冲突行为尚未定义

**位置：** `telemetry-model.md` 第 4、9、10、13 节；overview 第 5、7、9 节。

文档要求 retryable writes 使用稳定 idempotency_key，但没有明确唯一约束范围、相同 key 不同 payload 的处理、保留周期、不同 producer 重放的冲突规则。

**风险：**
- 不同 Agent 或 scope 之间发生错误去重。
- 相同 key 被复用于不同 payload，系统可能静默吞掉合法数据。
- Forget/retention 后重放旧请求，产生意外复活或重复编译。

**修正要求：**
- 定义幂等身份复合键，例如 authenticated producer + scope + operation family + idempotency_key（最终字段名由 H 决定）。
- 相同幂等键、相同规范化 payload：返回原 receipt。
- 相同幂等键、不同 payload：返回明确冲突，不得静默覆盖。
- 明确幂等记录保留与重放窗口，并与 Retention/Forget 协调。

**责任方：** Session E + Session H + Session I + 一致性负责人。

### P1-06：Applied 证明链与最终请求可见性的判据需要再收紧

**位置：** `inference-boundary-model.md` 第 5、6、8、10 节；`adapter-capability-tiers.md` 第 3、4、6 节。

文档已正确要求 Applied 发生在 inference assembly boundary，并要求 Tier 2 检查最终 outgoing request representation。但 Applied attestation 的关键证据仍主要是 Adapter 自述；applied_region_digest 是可选项，coverage 语义也尚未规范。对于模板缓存、请求重试、流式多阶段调用、最终请求二次变换等情形，何谓“真正进入被提交的请求”仍需 conformance 证据。

**风险：**
- Adapter 在中间模板上插入成功，却在后续请求构造阶段被覆盖。
- 只应用部分区域却报告完整 Applied。
- 重试请求沿用旧请求 ID 或错误复用 Applied 记录。
- Tier 2 对受控路径之外的请求产生过度承诺。

**修正要求：**
- 将 Applied 的必要条件定义为：目标版本完整物化在受控 managed region，且该区域属于本次提交给 inference runtime 的最终请求上下文。
- 明确最终提交点的可观测证据；不能观测最终请求的实现不得声称 Tier 1。
- 将 request/boundary correlation 的唯一性与重试语义写入 H 的 conformance contract。
- coverage 不得只用含糊布尔值；至少区分 full、partial、bypassed、unknown（具体枚举由 G/H 协同确认）。
- 对 digest 的规范化算法、版本和隐私边界作明确约束；digest 可选不应削弱 Applied 必要条件。

**责任方：** Session C + Session G + Session H。

### P2-05：Snapshot/Delta 的原子性、重复应用和局部失败仍需协议化

**位置：** `inference-boundary-model.md` 第 7、9、10 节。

“完整物化后才 Applied”是正确默认值，但尚未定义多个 Change Set 操作如何原子提交、重复操作如何处理、局部失败如何回滚，以及 snapshot 是否具备完整替换语义。

**建议：** G 定义 Change Set 原子性和版本语义；H 定义消息重试和逐项结果表达。C 只保留完整应用才 Applied 的原则，不自行设计 wire 细节。

### P2-06：超时与未知状态需要统一 reconciliation 查询模型

**位置：** `inference-boundary-model.md` 第 5、8、11 节。

文档正确指出 timeout 不是 Applied/Rejected，但未定义 Brain 在超时后如何查询 Adapter 的 delivery/version 状态、查询是否幂等、查询结果与迟到 ack 如何排序。

**建议：** 由 H 定义按 delivery_id 查询/重放；由 G 定义版本 reconciliation；迟到 ack 必须校验 delivery、context session、target version 与 capability epoch。

### 本维度结论

<badge color="warning">有条件通过</badge>

一致性思路扎实，但 P1-04 至 P1-06 是进入协议冻结和实现前的硬门槛。

---

## 维度四：安全与治理

### 通过项

- 明确 Memory/Telemetry 是数据而非指令。
- 不允许 Adapter 覆盖 system/developer/user/policy/tool regions。
- Scope 与 Permission 分离。
- 明确环境隔离，防止不同 world/save/simulation 混淆。
- 不要求收集 CoT、凭证、API Key 或无关 prompt history。
- Forget 与 Context Remove 分离，并承认远端物理删除需要确认与保证模型。
- Capability tier 不授予额外权限，降级不能扩大访问范围。

### P1-07：身份认证、权限撤销与本地缓存治理仍依赖外部模块，C 文档缺少强制检查点

**位置：** `agent-integration-overview.md` 第 6、10 节；`adapter-capability-tiers.md` 第 6、9、10 节；`inference-boundary-model.md` 第 11–13 节。

文档提到认证、授权、scope、revocation、retention、Forget，但尚未形成统一的检查时点。尤其 Accepted 后、Applied 前权限被撤销，或 Adapter 离线缓存中仍持有旧 context 的场景，需要明确行为。

**风险：**
- 只在交付时检查权限，实际应用前授权已撤销。
- Adapter 离线继续使用已过期或已撤销的本地 context。
- Agent instance 或 Environment 绑定变化后复用旧缓存。
- Brain 无法区分“已请求删除”“Adapter 已收到删除”“本地缓存已清理”。

**修正要求：**
- 定义授权检查至少发生在 ingress、Recall/readback、context delivery、Accepted→Applied 前、reconnect/reconciliation。
- 将 revocation epoch/授权版本或等效机制交由 I/H 定义。
- 缓存记录必须绑定 scope、context session、version、retention validity 与授权状态。
- 未能确认撤销/删除传播时，状态应为 pending/unknown，不得宣称已完成物理删除。

**责任方：** Session I + Session H + Session G；C 负责明确调用边界和不作过度承诺。

### P2-07：不可信 Memory 内容的下游提示注入风险需要在 Adapter 契约中具体化

**位置：** `agent-integration-overview.md` 第 6、10 节；`inference-boundary-model.md` 第 4、13 节。

“Memory 是数据，不是指令”是必要原则，但仅靠文本标记或分隔符不能阻止模型将内容当成指令。文档已说明 delimiter 不是安全边界，但缺少 Adapter 输出格式与 Agent-side policy 的最小要求。

**建议：**
- managed region 采用结构化/明确标记的数据承载方式，并保留来源与信任标签。
- 不允许记忆内容携带可执行 tool authorization 或改变 system policy 的能力。
- 明确提示注入是模型行为风险，Adapter 只能降低风险、不能保证模型忽略恶意内容。
- 将恶意 Memory 文本、伪造 system 标签、跨 scope 记忆作为验收用例。

### P2-08：遥测敏感数据分类、脱敏和原始证据引用的访问边界不足

**位置：** `telemetry-model.md` 第 9、11、12 节。

文档提到 redaction、classification 和 retention，但没有明确原始 payload、raw_evidence_ref、派生 summary 的不同访问策略。

**建议：** 由 I 定义数据分类与访问策略；C 应保证 provenance 引用不绕过原始证据的权限控制，派生摘要也不能默认比源材料更开放。

### 本维度结论

<badge color="warning">有条件通过</badge>

原则层面的安全边界良好，但撤销传播、离线缓存和 Applied 前授权复核必须与 Session I/H/G 形成可测试契约。

---

## 维度五：性能与资源

### 通过项

- 将 Telemetry ingress 与 Active Recall 的延迟/耐久性目标区分。
- 没有无证据地宣称性能倍率或固定 SLO。
- 明确记录 ingress p50/p95/p99、Recall latency、delivery/application latency、version lag、reconciliation 等指标。
- 对 payload size、频率、采样、缓存和离线窗口保留 TO_VALIDATE。
- Brain 故障默认不应阻断 Agent 主任务。

### P2-09：遥测高频场景的背压、批处理和优先级策略未形成候选设计

**位置：** `agent-integration-overview.md` 第 4、11、14 节；`telemetry-model.md` 第 12 节。

Minecraft、浏览器自动化或长时 Agent 可能持续产生位置、状态、观察和动作信号。当前只提出 logical lanes/priority classes，未定义采样/合并/批量提交/丢弃策略。

**建议：**
- 将 task transition、action outcome、risk、关键环境变更与高频状态采样区分优先级。
- 定义背压时哪些信号可合并、降采样、延迟或丢弃，哪些必须保留。
- 明确被采样或丢弃的数据不得被伪装成完整环境历史。
- 先在代表性 workload 测量，再决定物理队列拆分。

### P2-10：Context budget 超限时的拒绝/压缩语义仍过于粗略

**位置：** `adapter-capability-tiers.md` 第 9 节；`inference-boundary-model.md` 第 6、9 节。

文档倾向拒绝超限或显式协商压缩，但没有定义压缩责任归属、保留证据引用、版本身份以及压缩结果是否形成新的 Context version。

**建议：** MCM 决定内容选择/预算与压缩；Adapter 不得自行静默截断。若 Adapter 有本地传输限制，应返回 typed rejection/budget error，不得把部分插入报告为完整 Applied。

### 本维度结论

<badge color="success">通过，待验证</badge>

资源设计没有不合理的过早优化；下一阶段需用高频环境 Agent workload 验证队列、采样、背压和上下文预算。

---

## 维度六：可演进性与可观测性

### 通过项

- 设计状态均有 DECIDED/CANDIDATE/TO_VALIDATE/OPEN 标记。
- 逻辑 Telemetry schema 与最终 BMCP wire schema 分离。
- Tier 通过 conformance evidence 确认，而不是只看 Adapter 自报。
- capability epoch、schema version、context version、delivery identity 等演进要素已出现。
- 验收标准覆盖多种降级、重启、版本不匹配与跨 scope 场景。
- 指标能够区分 ingestion、Recall、delivery、application 和 Agent outcome。

### P2-11：Schema evolution 的兼容规则尚未具体化

**位置：** `telemetry-model.md` 第 4、9、14 节；`adapter-capability-tiers.md` 第 6 节。

目前只说明 unsupported major rejected、extensions namespaced opaque、schema negotiation 交给 H。缺少旧字段弃用、未知 enum、未知必需字段、字段语义变化和 producer/consumer 升级错配的兼容规则。

**建议：** H 定义 wire compatibility；C 定义逻辑语义兼容原则：未知扩展字段可忽略但不能覆盖核心字段；未知核心 signal type 不得静默解释；语义破坏必须升级 major 或采用显式能力协商。

### P2-12：可观测性缺少统一 correlation chain 与敏感字段日志规则

**位置：** 四份文档的 envelope、Applied record、metrics/test 部分。

当前有 telemetry_id、correlation_id、delivery_id、context_id、boundary_id、inference_request_id 等字段，但没有定义端到端 trace 关联方式，以及哪些字段可写入日志/指标标签。

**建议：**
- 定义从 telemetry → Event/Compiler → activation → context change → delivery → inference boundary → Agent outcome 的关联链。
- 禁止将原始 prompt、Memory 内容、凭证或敏感 evidence 放入普通日志/metric labels。
- 指标维度应控制 cardinality；高基数 ID 进入 trace/log，不进入 metric labels。
- 对 Applied attestation、scope denial、Forget/revocation、version conflict 保留可审计事件。

### P2-13：Conformance 测试虽覆盖正常路径，但缺少性质测试与故障注入矩阵

**位置：** `adapter-capability-tiers.md` 第 11 节；`inference-boundary-model.md` 第 14 节；`telemetry-model.md` 第 13 节。

现有测试是有价值的场景测试，但对乱序、重复、并发、崩溃窗口、重启和长时间离线组合还不够系统。

**建议：**
- 加入 property-based tests：幂等性、版本单调性、scope 隔离、Applied 不越过请求边界。
- 加入 fault injection：提交前后崩溃、响应丢失、重复 ack、迟到 ack、并发 delta、reconnect 期间 revocation。
- 建立 Tier 1/2/3 共用的 conformance suite，并允许每种 Agent adapter 增加 framework-specific tests。

### P2-14：Rust 落地尚未形成实现约束，但当前阶段不应在 C 文档中提前锁定 crate

**位置：** 四份文档整体；对照 `ARCHITECTURE_ROADMAP.md` Phase 4。

这是设计阶段的合理留白，不是缺陷。当前应先冻结纯逻辑契约，再由 Rust Engineering Architecture 决定模块/crate、异步运行时、持久化与并发实现。

**建议：** 后续实现设计至少将状态转换、版本校验、scope authorization、幂等判定设计为可独立测试的纯逻辑/明确事务边界；不要把每个逻辑子系统机械地变成独立服务或 crate。

### 本维度结论

<badge color="success">通过，待完善</badge>

演进方向合理；需补全兼容策略、trace 关联和故障注入测试。

---

## 4. 三方独立结论

### 4.1 系统架构师

**结论：有条件通过。**

优点：
- Brain 与 Agent 的主权边界清楚，没有把 Memory Brain 变成 Agent Runtime。
- 与系统架构的主数据流和组件职责基本一致。
- Telemetry、Recall、Context Sync 分离，避免所有交互被塞入一个同步请求。
- Inference Boundary 的概念非常关键，且避免了“动态改写正在运行的模型上下文”这一错误假设。

主要担忧：
- Environment Adapter 双路拓扑图示与 OPEN 决策不一致。
- Observation/Outcome 和身份/Scope 语义需要与 Domain Model 对齐。
- Applied 的最终请求可见性是核心架构保证，不能停留在 Adapter 自报。

架构师建议：先解决 P1-01、P1-02、P1-03、P1-06，再冻结跨模块接口。

### 4.2 工程实现负责人

**结论：有条件通过，暂不建议据此直接开始协议实现。**

优点：
- Telemetry 和 Context Sync 都有生命周期/状态机雏形。
- 明确了 version base、snapshot recovery、idempotency 和 retry。
- 对 Brain outage、Adapter offline、restart、capability loss 有初步降级处理。

主要担忧：
- Accepted 的原子提交点、幂等复用冲突和 outbox 恢复语义未精确化。
- Task/Plan/Action 状态更新缺少 revision/乱序规则。
- Snapshot/Delta 多操作原子性与 partial failure 尚未定义。
- Applied 与最终请求提交点的关联，需要可自动化测试的 hook/conformance evidence。

工程负责人建议：P1-04、P1-05、P1-06 是协议与 Rust 实现前置条件；不要先写 Adapter 再反向猜语义。

### 4.3 安全与可靠性审计者

**结论：原则层面通过，运行时保障有条件通过。**

优点：
- 不把 Memory 作为指令，不允许覆盖保护区域。
- 明确 Scope 与 Permission 分离。
- 认识到 Forget、Retention、Revocation 不能靠删除 Context Entry 代替。
- 不要求采集 CoT 或不相关 Prompt 历史。

主要担忧：
- Accepted 后到 Applied 前的权限撤销窗口。
- 离线缓存、重连、重启与 Forget 的交互。
- Agent/Environment/Adapter 身份绑定尚未形成可验证授权链。
- 恶意记忆内容的提示注入风险需要明确标为残余风险，并提供测试。

安全审计者建议：P1-03、P1-07 必须由 B/I/H 明确责任与检查点；不能把“Adapter 已认证”当作“本次 scope 操作已授权”。

---

## 5. P0/P1/P2 汇总与修复优先级

### P0 — 阻断项

**本轮未发现已证实 P0。**

说明：本轮只审阅架构文档，尚未审计具体实现、权限代码、持久化事务或真实 Adapter，不能据此宣称系统没有 P0 风险。

### P1 — 协议冻结/实现前必须处理

| ID | 问题 | 主要责任方 | 验收标准 |
|---|---|---|---|
| P1-01 | Environment Adapter 双路拓扑图与 OPEN 决策不一致 | C/H/I | 明确单一路径或双路去重契约；身份/幂等责任明确 |
| P1-02 | Observation 与 Outcome 语义重叠 | C/B/E | 定义判别规则、引用关系和至少 3 个边界示例 |
| P1-03 | producer/Agent/instance/session/task/environment/scope 绑定不完整 | B/I/H/C | 有规范身份绑定与逐操作授权规则 |
| P1-04 | Telemetry Accepted 的持久化/事务提交语义不完整 | E/H/Consistency/C | 崩溃窗口测试证明 Accepted 不丢失且可恢复处理 |
| P1-05 | idempotency key 作用域和 payload 冲突行为未定义 | E/H/I | 同键同 payload 返回原 receipt；同键异 payload 明确冲突 |
| P1-06 | Applied 与最终提交请求的可验证证明链不足 | G/H/C | conformance 测试证明完整 managed region 属于指定最终请求 |

### P2 — 后续设计阶段必须进入任务

| ID | 问题 | 主要责任方 |
|---|---|---|
| P2-01 | Adapter/Gateway 部署形态避免被逻辑图误导 | C/Engineering |
| P2-02 | source_kind 枚举命名不一致 | C/H |
| P2-03 | Task/Plan/Action revision、乱序和撤回规则 | B/E/C |
| P2-04 | Risk severity/confidence 语义及映射 | B/I/C |
| P2-05 | Snapshot/Delta 原子性、重复应用、局部失败 | G/H |
| P2-06 | Timeout/迟到 ack 的 reconciliation 查询模型 | G/H |
| P2-07 | Memory 提示注入与 Agent policy 残余风险 | I/H/C |
| P2-08 | 原始遥测、证据引用、派生摘要的数据分类 | I/C |
| P2-09 | 高频 Telemetry 背压、批处理、采样策略 | C/E/F |
| P2-10 | Context budget 超限、压缩和拒绝语义 | G/H |
| P2-11 | Schema evolution 与兼容策略 | H/C |
| P2-12 | 端到端 correlation chain 与日志脱敏 | XF-04/H/C |
| P2-13 | 性质测试、故障注入和共用 conformance suite | H/I/Testing/C |
| P2-14 | Rust 实现边界和并发落地约束 | Engineering |

---

## 6. 对四份文档的逐文件审查结论

| 文件 | 结论 | 必须修正/确认 |
|---|---|---|
| agent-integration-overview.md | 有条件通过 | P1-01；与 B/E/F/G/H/I 的身份、事件和上下文接口对齐 |
| telemetry-model.md | 有条件通过 | P1-02、P1-03、P1-04、P1-05；P2-02 至 P2-04 |
| adapter-capability-tiers.md | 有条件通过 | P1-06；明确 Tier 1/2 的 Applied conformance evidence |
| inference-boundary-model.md | 有条件通过 | P1-06、P1-07；与 G/H/I 明确授权复核、原子应用和恢复契约 |

### 保留的核心架构决策

本次审查不建议推翻以下设计：
1. Brain owns canonical memory and managed-context authority.
2. Agent owns reasoning, planning, action selection and execution.
3. Adapter applies context only at a future inference assembly boundary.
4. Received != Accepted != Applied.
5. Applied is not model comprehension or behavioral compliance.
6. Telemetry acceptance != semantic compilation != Memory creation.
7. Intent/Plan/Pending Action != completed Outcome.
8. Memory is untrusted data, never instruction authority.
9. Tier 3 is a valid integration mode and must not claim proactive Applied.
10. Context Remove != Canonical Memory Forget.

---

## 7. 建议的修复顺序与跨会话协调

1. **C + B + E：** 先统一 Observation/Outcome/Event/Evidence 的语义和 Telemetry 身份字段。
2. **C + H + I：** 再统一 Environment Adapter 拓扑、producer 身份、scope 授权与撤销检查点。
3. **C + E + H + Consistency：** 明确 Accepted 持久化点、幂等键和崩溃恢复。
4. **C + G + H：** 明确 Applied 的最终请求证明、Change Set 原子性、超时 reconciliation。
5. **C + I + Testing：** 补充提示注入、离线缓存、Forget/revocation 故障注入。
6. **Engineering：** 上述逻辑契约稳定后，再进入 Rust 模块/并发/存储实现设计。

### 建议的退出条件

Session C 的架构设计可在以下条件满足后标记为 **Review Accepted**：
- 六项 P1 均已关闭，或由对应 Owner 提供明确、可追踪的 ADR/接口决议。
- 四份文档中的 OPEN/CANDIDATE 与跨模块文档不冲突。
- Tier 1/2/3 的 conformance criteria 可由自动化测试判定。
- Telemetry Accepted、Context Applied、Revocation/Forget 三条关键链路均有故障恢复测试。
- 不把模型理解、遵从或真实世界动作成功伪装成协议层保证。

---

## 8. 最终结论

**Session C 的方向是正确的，核心架构边界值得保留；但当前版本不应被视为可直接冻结的协议规范。**

建议状态：**Conditional Pass — Architecture Accepted in Principle, Interface Contracts Pending.**

本报告仅新增在 `reviews/07-agent-integration/`，不修改 Session C 的四份原始设计文档，也不替其他 Session 关闭其 Owner 范围内的问题。
