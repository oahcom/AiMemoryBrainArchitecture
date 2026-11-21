# Agent 集成架构概览

**状态：**基线 DECIDED；执行细节 CANDIDATE；协议细节 OPEN  
**Owner：**Session C — Agent 集成边界预设计  
**范围：**逻辑集成边界。BMCP 线协议规范和具体 Adapter 架构属于 Session H。

## 1. 目的

定义一个与模型及 Agent 无关的 Memory Brain 如何与异构 Agent 协作。集成必须保留 Brain 对 memory 的权威，同时将推理、规划、动作选择、工具执行和安全策略留给 Agent。

目标：
- 标准化结构化 telemetry，而不要求私有推理轨迹。
- 支持由 Agent 发起的 Active Recall 和由 Brain 发起的上下文更新。
- 仅在明确的 inference assembly boundary 应用上下文。
- 明确 capability、delivery、acceptance 和 application 保证。
- 将 Agent 特定协议置于 Adapters 之后。
- 保留 scope、permission、provenance 和 trust 边界。

## 2. 系统边界

~~~mermaid
flowchart LR
  subgraph AgentSide["Agent execution domain"]
    A[Agent: reason, plan, act]
    L[LLM / inference runtime]
    AA[Agent Adapter]
    EA[Environment Adapter]
    SL[Skill Library]
    A <--> L
    A <--> SL
    A <--> AA
    EA --> AA
    AA --> L
  end
  subgraph BrainSide["Memory Brain domain"]
    PG[BMCP integration gateway]
    T[Telemetry normalization]
    O[Memory observer]
    R[Retrieval and activation]
    C[Memory Context Manager]
    S[Context synchronization]
    PG --> T --> O --> R --> C --> S
    PG <--> S
  end
  AA <--> PG
  EA --> PG
~~~

### 所有权

**DECIDED — Brain 拥有**
- Canonical memory 语义、身份、生命周期、provenance 和 governance。
- Memory 选择与 activation policy。
- 每个受管理 Memory Context 的权威版本序列。
- Brain 资源的 scope 和 permission 决策。

**DECIDED — Agent 拥有**
- 推理、规划、任务分解、动作选择和工具调用。
- Agent 原生任务状态和私有执行结构。
- Agent 安全策略及外部动作授权。
- 是否以及如何使用返回的 memories。

**DECIDED — Agent Adapter 拥有**
- 将 Agent 原生信号映射为 Brain 定义的 telemetry。
- Capability 声明和边界验证。
- 接收并验证 context changes。
- 仅在 inference assembly boundary 的有界区域内应用 Brain 管理的上下文。
- 如实确认 receipt、acceptance、application、rejection 和 reconciliation。

Adapter 不拥有 canonical memory、activation policy 或权威 context versions。

**DECIDED — Environment Adapter 拥有**
- 将特定环境的 observations 和状态变化转换为规范化、带来源限定的 signals。
- 附加 environment identity 和 observation provenance。
- 报告 observations，而不是将未观察到的状态断言为事实。
- 它不会代表 Brain 驱动环境。

**DECIDED — LLM/runtime 拥有** inference 和 token processing。Brain 不控制模型内部机制。

**DECIDED — Skill Library 拥有** 可执行 skills 和 procedures。Brain 可以存储引用某项 skill 的经验，但不会执行 skills，也不会把 memories 转换为可执行代码。

## 3. 职责矩阵

| Capability | Brain | Agent | Agent Adapter | Environment Adapter |
|---|---|---|---|---|
| Canonical memory lifecycle | Primary | — | — | — |
| Planning and action choice | — | Primary | — | — |
| Telemetry source | Consumes | Primary | Maps | Supplies observations |
| Telemetry semantics | Defines | Supplies | Maps | Supplies observations |
| Retrieval and activation | Primary | May request | Transports | — |
| Context version authority | Primary | — | Tracks applied version | — |
| Inference context application | Defines target | Invokes inference | Executes | — |
| Environment observation | Consumes | May interpret | Transports | Primary |
| Environment actuation | — | Primary | May expose Agent API | — |
| Skill execution | — | Primary | Optional mapping | — |

支持某项 capability 并不意味着获得该项 capability 的权威。

## 4. 集成模式

**DECIDED：** 三种模式可以共存。

1. **Telemetry ingress：** Agent/Adapter 提交结构化的 task、intent、observation、outcome、uncertainty、risk 和 environment signals。
2. **Active Recall：** Agent 针对 task、entity、environment 或 question 请求受 scope 限定的 memories。
3. **Context synchronization：** Brain 发布带版本的 snapshots 或 changes；Adapter 在未来的 inference boundary 应用它们并确认结果。

Telemetry ingress 与 Runtime Recall 具有不同的 latency 和 durability 目标。它们可以共享 gateway，但不得被强制放入同一个同步处理路径。**CANDIDATE：** 使用具有共同 identity 和 scope envelope 的独立逻辑 lanes/priority classes。物理隔离必须有证据支持。

## 5. Canonical integration envelope

最终 BMCP message shape 属于 Session H。逻辑 envelope 包含：

| Field | Semantics | Requirement |
|---|---|---|
| telemetry_id | Stable submission identifier | Required |
| schema_version | Canonical schema version | Required |
| producer_id | Authenticated Adapter identity | Required |
| agent_instance_id | Agent instance | Required for context/session operations |
| scope | Ownership namespace | Required |
| signal_type | Canonical signal category | Required |
| occurred_at / observed_at | Source time | When known |
| recorded_at | Brain acceptance time | Brain assigned |
| payload | Typed signal body | Required |
| source_kind | Agent, environment, user, tool, external | Required |
| correlation_id | Task/turn/action correlation | Recommended |
| idempotency_key | Retry deduplication identity | Required for retryable writes |
| provenance | Origin and transformation history | Required for derived claims |

未知 extension fields 是带命名空间的不透明数据；它们不得覆盖 canonical fields。

## 6. Trust boundary

Telemetry 和 memory 是数据，不是指令。Agent 提供的 trusted、verified、high priority 或 system instruction 等标签不授予任何权威。Adapter 仅将 memory 插入 Brain 管理的区域，且不能覆盖 system/developer instructions、user-originated input、tool definitions 或 Agent security policy。

## 7. 核心工作流

### Telemetry
1. Authenticate producer 并解析 identity。
2. 将 native fields 映射为 canonical signal types，并附加 scope/environment。
3. 验证 schema、permission、timestamps、size 和 idempotency。
4. Durable accept 或 reject。
5. 返回 ingestion receipt。Acceptance 不意味着 semantic compilation 或 Memory creation。
6. 保留 provenance，异步处理下游流程。

### Active Recall
1. Agent 提交受 scope 限定的 query，以及 task/environment context。
2. Brain 授权并解析 scope。
3. Runtime 检索候选项并应用 activation/visibility policy。
4. Brain 返回符合条件的 memory data 和获准的 evidence references。
5. Agent 决定是否以及如何使用它。

### Proactive context update
1. Brain 观察获授权的 telemetry/triggers。
2. Activation policy 请求 context planning。
3. Context Manager 基于其权威 base 创建带版本的 change。
4. Synchronization 交付该 change。
5. Adapter 验证 scope、version、budget 和 managed-region boundary。
6. Adapter 分别报告 receipt 和 acceptance。
7. 在下一个 inference assembly boundary，Adapter 应用该 version 并报告 Applied。
8. 通过 delta 或 full snapshot 对离线/过期的 Adapter 进行 reconciliation。

## 8. 状态与权威

| State | Authority |
|---|---|
| Canonical Memory | Brain |
| Telemetry acceptance | Brain |
| Activation decision | Brain |
| Memory Context version | Brain Context Manager |
| Delivery state | Brain synchronization subsystem |
| Local applied version | Adapter, reported as attestation to Brain |
| Inference execution | Agent/runtime |

Applied Context 是一条 acknowledgement record，不是第二份 canonical context。

## 9. 可靠性、一致性与降级

- Durable-acceptance receipt 表示已接受的 telemetry 按声明的 durability contract 在 restart 后仍然存在。
- 在相同的 scoped idempotency key 下重复 retry，只创建一个逻辑上的 accepted event。
- Context versions 按 Brain authority 排序。
- 未知 base versions 和 gaps 必须被 reject 或 reconcile，绝不能猜测。
- 默认情况下，Brain failure 不得停止 Agent reasoning 或 environment control。
- Adapter offline 意味着不能产生新的 Applied claim；Brain 跟踪 pending delivery，并在之后进行 reconciliation。
- 缺失/有歧义的 environment identity 会导致 environment-specific signals 被 reject 或 quarantine。
- Permission revocation 会停止进一步访问并触发受治理的 reconciliation；它本身不是 Forget。

## 10. 安全与隔离

Authentication 和 authorization 适用于每一项操作。Scope 不等于 permission。必须明确隔离 user、project、Agent、Agent instance、task、session 和 environment。Environment IDs 用于区分 worlds、save files、tenants 和 simulations。返回给 Agent 的 memory 是不可信数据，不能授权工具，也不能覆盖 Agent policy。

## 11. 性能与可观测性

在受控比较下，测量 telemetry acceptance latency/durability、duplicate suppression、Recall p50/p95/p99、context generation-to-delivery 和 acceptance-to-applied latency、applied-version lag、reconciliation rate、rejection/error rate，以及 Agent task outcomes。

**TO_VALIDATE：** SLO values、payload budgets、telemetry cadence、activation thresholds 和 local buffering windows。不假定任何性能倍数。

## 12. 验收标准

1. 更换 Agent framework 或 LLM 不会改变 canonical Brain semantics。
2. Planning、tool execution 和 external action policy 仍归 Agent 所有。
3. Telemetry 可以独立于 model-assisted compilation 被 durably accepted。
4. 不能仅凭提交 intent/plan/pending action 就将其变为 completed outcome。
5. Received、Accepted 和 Applied 可以分别观测。
6. Applied 标识 Adapter、Agent instance、context session、version 和 boundary correlation。
7. Brain 不能覆盖受保护的 instruction/user/policy regions。
8. 无效的 cross-scope 或未经授权的操作必须 fail closed。
9. Tier 3 可以使用 telemetry 和 Recall，而不会产生虚假的 proactive-sync claims。
10. 在 Brain integration outage 期间，Agent 继续其主要任务，但仍受 Agent policy 约束。

## 13. 跨 Session 接口

| Partner | Required confirmation |
|---|---|
| Session B — Domain Model | Scope tuple, epistemic/time semantics, Event and provenance identity |
| Session E — Compiler | Telemetry-to-Event mapping and durable ingress |
| Session F — Runtime | Recall query context, activation triggers, risk/freshness signals |
| Session G — Context | Context/session identity, versions, Change Set and Applied record |
| Session H — BMCP/Adapter | Wire envelope, capability negotiation, acknowledgements, retries, errors |
| Session I — Governance | Authentication, authorization, audit, retention, idempotency and offline replay |

## 14. 开放决策

- **OPEN：** 使用一个通用 typed telemetry envelope，还是一小组 message families。
- **OPEN：** Environment Adapter 直接 ingress，还是通过 Agent Adapter relay。
- **CANDIDATE：** 独立的逻辑 ingress 和 recall lanes。
- **TO_VALIDATE：** Event-specific payload/frequency limits。
- **OPEN：** Offline retention 和 local Adapter cache policy（Session I）。
- **OPEN：** Partial context application。安全默认值是 reject，除非明确规定 partial semantics 和 per-entry results。

## 15. 决策摘要

- **DECIDED：** Brain 拥有 memory 和 managed-context authority；Agent 拥有 reasoning 和 action；Adapter 在 inference boundaries 进行映射和应用。
- **DECIDED：** Environment Adapter 报告 observations，而不是 actions。
- **DECIDED：** Telemetry acceptance 与 compilation 相互独立。
- **DECIDED：** Applied 不证明 model comprehension。
- **DECIDED：** Memory 始终是不可信数据。
- **OPEN：** BMCP wire details 仍由 Session H 负责。
