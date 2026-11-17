# Agent 集成架构指南

- 文档 ID：DOC-AGENT-001
- 版本：1.0
- Owner：C — Agent Integration
- 源规范：C Owner 分支中的 Agent Integration Architecture Overview
- 对应英文：[Agent Integration Architecture Guide](../../en/07-agent-integration/agent-integration-guide.md)
- 状态：解释性指南；执行细节为 CANDIDATE，协议细节仍为 OPEN 且归 H 负责

## 1. 目的

Agent Integration 定义独立于模型和 Agent 的 Brain 如何与不同类型的 Agent 协作，同时保持清晰的权威边界。

Brain 拥有 Canonical Memory 及其管理的 Context。Agent 拥有推理、规划、行动选择、工具执行和自身安全策略。Adapter 连接双方，但不能把 Brain 变成 Agent 框架。

## 2. 三类参与者

| 参与者 | 负责内容 | 不得接管 |
|---|---|---|
| Memory Brain | Canonical Memory、选择/激活策略、受管 Context 版本权威、Brain 资源授权 | Agent 规划、工具执行、外部行动策略 |
| Agent | 推理、规划、任务拆解、行动选择、工具、原生任务状态、安全策略 | Brain 内部记忆语义 |
| Agent Adapter | 遥测映射、能力声明、推理边界上的 Context 校验/应用、如实 ACK | Canonical Memory、激活策略、权威 ContextVersion |

Environment Adapter 负责规范化环境观察、绑定环境身份和 Provenance，并报告观察；它不代表 Brain 驱动环境。LLM/Inference Runtime 负责模型推理和 Token 处理。

## 3. 需要什么遥测

Brain 需要 Agent 任务和环境的结构化信号，不需要私有思维链。可用遥测包括 Task State、Intent、Plan Summary、Active Entities、Tool Call/Pending Action、Observation、Outcome、Uncertainty、Risk Signal 和 Environment Delta。

Intent、Plan、Prediction 和 Pending Action 必须与已完成结果区分。Telemetry 是不可信输入：它可以辅助判断相关性和记忆需求，但不能证明真实性，也不能授予权限。

## 4. 双向集成

~~~text
Agent → Adapter → BMCP Gateway → Brain
   任务/意图/观察/结果                 |
                                      | Recall / 激活 / Context 变更
Agent ← Adapter ← BMCP Gateway ← Brain
        在推理边界应用受管上下文
~~~

Agent 可以主动请求 Active Recall。Brain 也可以根据策略和遥测判断主动发起 Context 更新。两个方向上，Adapter 都必须校验 Scope、能力、版本和授权。

## 5. 推理边界上的应用

Context 变更只能在明确的推理上下文组装边界应用，并且只能修改 Brain 管理的区域。Adapter 不得改写 System/Developer 指令、用户原始输入或 Agent 安全策略。

若要达到 Tier 1 Full Applied，Adapter 必须能够观察最终提交给推理运行时的请求，并证明该边界上的受管区域版本/内容准确。如果只能观察中间 Buffer 或传输 Receipt，就必须报告较弱能力，不得声称 Full Applied。

Applied 的含义是“Adapter 在约定边界应用了这份受管 Context”，不代表模型关注、理解、记住或遵循了它。

## 6. 集成部署方式

可能的 Adapter 形态包括：
- 嵌入 Agent 进程的 SDK/Library。
- 通过明确 IPC 边界连接的本地 Sidecar。
- 无法嵌入 SDK 的 Agent 使用本地或远程 Gateway Client。

这些都只是候选方案，并非已冻结的部署选择。选型要看集成能否可靠观察最终推理请求、保持受管区域边界、认证身份、支持重连并提供可信证据。仅仅建立传输连接不构成 Tier 1 集成。

## 7. 能力与兼容性

Adapter 必须声明支持的协议版本、Telemetry 类型、Context 操作、最大 Context Budget、推理边界可见性、清理/抑制能力和重连行为。能力协商必须显式且版本化。

H 拥有 BMCP Wire Schema 和消息语义；C 拥有 Agent 侧集成要求和兼容性行为。不同语言的 SDK 或 FFI 不得改变协议规范字段名和安全语义。

## 8. 故障与恢复

| 情况 | 必须行为 |
|---|---|
| Agent 不暴露最终请求 | 不得声称 Tier 1 Full Applied |
| Adapter 离线 | 只有明确策略允许时才可排队；重连时必须协调当前版本和 Forget 状态 |
| 不支持某个 Context 操作 | 拒绝或协商兼容回退，不得静默忽略 |
| Scope/身份存在歧义 | Fail Closed |
| Permission Epoch 变化 | 应用前重新授权 |
| Forget Fence 前进 | 清理/抑制本地受管区域，并如实确认实际能力和结果 |
| Context 只部分物化 | 报告部分成功/拒绝，不得 ACK Applied |
| Agent Prompt 布局变化 | 下次应用前重新验证受管区域定位 |

## 9. 信任与安全边界

Memory 内容是不可信数据，不是指令。Adapter 必须保持明确隔离的受管区域，不能把检索内容提升为 System/Developer 权限。Brain 记忆不授权外部行动；Agent 的安全策略和工具授权仍归 Agent。

Telemetry 不得要求隐藏思维链。只要带有来源、时间、Scope 和不确定性，Plan Summary 与结构化观察就足够。

## 10. 仍需验证

- Embedded、Sidecar 和 Gateway 的集成可行性。
- 最终请求观察与 Applied 证明。
- Adapter 身份、Capability Epoch、PermissionEpoch 和 ForgetFence 绑定。
- 离线/重连、清理/抑制和部分投递。
- Prompt Injection 与受管区域隔离。
- 多语言 Agent 兼容性和 Conformance Test。

详细 Agent 集成契约见 [C Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-c-agent-integration-2026-11-16/07-agent-integration)，BMCP 详细契约见 H 的协议规范。
