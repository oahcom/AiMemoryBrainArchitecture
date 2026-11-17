# BMCP 协议架构指南

- 文档 ID：DOC-BMCP-001
- 版本：1.0
- Owner：H — BMCP Protocol
- 源规范：H Owner 分支中的 Protocol Overview 及 Adapter Capability/Applied Attestation 契约
- 对应英文：[BMCP Protocol Architecture Guide](../../en/08-bmcp-protocol/bmcp-guide.md)
- 状态：CANDIDATE 架构；依赖的 Wire/身份契约仍有 OPEN 或 ADR-BLOCKED 项

## 1. BMCP 做什么

Brain Memory Context Protocol（BMCP）是 Memory Brain 与 Agent Adapter 之间由 Brain 定义的契约。它传输结构化 Telemetry、Event Ingress 引用、Context Snapshot/Delta、Delivery 生命周期、Acknowledgement、Capability Negotiation，以及 Forget/Revocation 通知。

BMCP 传输领域引用和 Payload，不重新定义 Memory、Claim、Scope、Permission、ContextVersion 或 Forget 的含义。这些语义仍由 B/D/G/I 负责。H 拥有 Wire Encoding、协议版本、传输交互、Adapter 能力词汇以及 ACK/Attestation 编码。

## 2. 职责边界

| Owner | 权威职责 |
|---|---|
| B/D | 领域对象、规范身份、生命周期、Canonical Forget 状态 |
| C | Agent 集成语义、Telemetry 含义、Agent 侧推理边界要求 |
| G | Context 成员、ContextVersion、ChangeSet、Delivery Intent 语义 |
| H | BMCP Wire Envelope、版本、消息类型、传输和 ACK 编码 |
| I | Principal 信任、授权策略、Permission Epoch、全局 Forget 策略 |

Brain 不可用时，BMCP 不负责让 Agent 停止或继续其自身工作；Agent 仍负责自身运行和安全策略。BMCP 不能改写模型供应商隐藏 Prompt、供应商保留的请求副本、模型内部机制或模型注意力。

## 3. 消息类型

| 类型 | 方向 | 目的 |
|---|---|---|
| Telemetry | Adapter → Brain | 结构化 Agent 观察、结果、意图、计划摘要、工具/环境事件 |
| Event Ingress | Producer → Brain | 提交带幂等和 Provenance 引用的类型化来源 Event |
| Context Snapshot | Brain → Adapter | 在目标版本替换完整受管 Context |
| Context Delta | Brain → Adapter | 从精确 base version 应用原子 ChangeSet |
| Delivery | Brain → Adapter | 将 Snapshot/Delta 绑定到接收者、Session 和投递生命周期 |
| Acknowledgement | Adapter → Brain | 报告生命周期状态和证据 |
| Capability Negotiation | 双向 | 协商协议版本、消息类型、限制和证明等级 |
| Forget / Revocation | Brain/I → Adapter | 使受管内容、Session、队列任务和离线旧状态失效 |
| Administrative Governance | I/控制面 → Adapter/Gateway | 携带 Policy Epoch、撤销、接收者 Scope 和管理指令 |

## 4. Delivery 状态不能混为一谈

- Prepared：Adapter 已校验并暂存投递，尚未确认传输成功。
- Delivered：传输端点已为目标 Adapter 接收投递。
- Applied：Adapter 对推理边界上的明确应用覆盖范围作出证明。
- Rejected：接收方以分类原因明确拒绝。
- Expired：有效期结束，未能有效完成。
- Superseded：更新的 Context 目标或治理 Epoch 已使该操作过时。
- Unknown：无法确认结果，例如超时、进程丢失或离线。

没有明确状态转换和证据时，一个状态不能推导出另一个状态。Delivered 绝不能解释为 Applied。Applied 不能解释为模型已经关注或使用。

## 5. Adapter 能力等级

### Tier 1 — 可观察最终请求
Adapter 能观察全部组装和转换后的精确最终请求，识别实际提交给推理运行时的请求，证明受管区域完整且对应精确目标 ContextVersion，对该区域计算声明过的摘要，关联 Request/Delivery/Session/Context/Capability 身份，并输出具备完整性保护的证据。

只有 Tier 1 可以发出 Full Applied，而且必须满足每个 Request 的全部证明条件。否则必须报告 Partial、Bypassed 或 Unknown。

### Tier 2 — 可观察受管区域，但无法观察最终提交
Adapter 可以校验本地受管区域，但无法证明精确最终请求确实提交给推理运行时；后续 Middleware 可能修改或丢弃它。本地 Buffer Digest 不是最终请求证明。Tier 2 禁止声称 Full Applied。

### Tier 3 — 基础传输集成
Adapter 校验协议 Envelope/Version 并传输消息，报告传输成功、拒绝和未知结果。它不证明 Context 已应用到推理请求，禁止发出 Applied=Full。

## 6. Capability Epoch 与 Attestation

能力必须显式、版本化声明，不能根据产品名称或传输是否可达来推断。能力项可包括协议/Schema 版本、消息类型、Snapshot/Delta 操作、Payload 限制、持久化队列、幂等、受管区域隔离、最终请求可见性、Runtime Handoff 观察、Request 关联、Digest/Evidence 能力、Forget 清理/重连能力、ACK 覆盖范围和 Context 大小限制。

如果二进制、配置或运行时变化导致能力集合变化，就必须创建新的 Adapter Capability Epoch 并重新协商。Attestation 必须按生成它的 Epoch 评估，不能使用之后的当前能力集合追溯替代。

## 7. Applied 证据

Applied Attestation 必须按照正式批准的契约，将 Delivery Attempt 绑定到目标 Context/Version、实际应用版本、Coverage、Adapter 身份和 Capability Epoch、认证 Transport Principal、Inference Request/Final Request 身份或摘要、相关 Scope/PermissionEpoch，以及适用的当前 Forget Fence Generation。

Receipt ACK 或本地 Buffer Hash 单独都不充分。Applied 只能证明 Adapter 声明的边界操作，不能证明模型理解或行为遵循。

## 8. Forget、Revocation 和重连

Forget/Revocation 通知必须使受管区域和过期队列 Delivery 失效。离线 Adapter 重连后，在复用本地内容之前，必须协调当前 Context 目标、授权 Epoch 和 Forget Fence。目标不支持或不可达时应保持 UNKNOWN/UNSUPPORTED，除非 I 批准了明确的残留例外；不得静默算作成功。

## 9. 兼容性和故障处理

- 必须显式协商版本；不兼容的主版本必须 Fail Closed。
- 未知必需字段或不支持的操作必须拒绝，或遵循明确声明的前向兼容规则。
- 状态变更消息重复发送时，必须在规定幂等范围内保持幂等。
- 部分传输或部分应用必须如实报告。
- 超时和进程丢失时，除非有更强证据，否则结果为 Unknown。
- Capability 降级不得继续沿用 Full Applied 声明。

## 10. 未决依赖与验证

- 最终请求 Applied 证明需要 C/G/H/I 联合确认。
- Principal/ActorRef/ScopeRef 和认证 Transport Binding 仍依赖 B/I/H 决议。
- Forget ACK Class 必须映射到 I 的逐目标完成向量。
- 跨语言 Schema 和签名规范化需要 Conformance Vector。
- 重连、Replay、重复投递、Capability 降级和最终请求被修改都需要故障测试。

详细候选协议文档见 [H Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-h-bmcp-protocol/08-bmcp-protocol)。
