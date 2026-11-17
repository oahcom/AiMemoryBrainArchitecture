# 记忆上下文架构指南

- 文档 ID：DOC-CONTEXT-001
- 版本：1.0
- Owner：G — Memory Context
- 源规范：G Owner 分支中的 Context 架构及 Phase 3 集成契约
- 对应英文：[Memory Context Architecture Guide](../../en/06-memory-context/memory-context-guide.md)
- 状态：解释性指南；内部模型为 CANDIDATE，跨模块 Wire 细节仍为 OPEN

## 1. Memory Context 是什么

Memory Context 是 Brain 为特定 Agent 执行上下文构建的、有 Scope、有版本的工作记忆视图，内容来自选定的 Canonical Memory 资产。

它不是完整 Memory Store，不是完整 Agent Prompt，也不是 Agent 私有工作状态。它是 Brain 管理的记忆区域，Brain 对该区域的成员、排序、限定、过期、预算策略和版本历史拥有权威。

## 2. 三个必须区分的层次

| 层次 | 权威归属 | 内容 |
|---|---|---|
| Canonical Memory | D — 权威领域 | 不可变 Memory Version、Claim、Entity、Relation、Evidence/Provenance 和生命周期 |
| Memory Context | G — Context Manager | 引用已授权 Canonical Version 或受治理呈现内容的 Context Entry，以及排序、理由、有效期、预算和版本历史 |
| Applied Context | Adapter 提供证明，由 G/H 协调 | Adapter 声称已在某个推理边界安装的受管区域内容、对应版本及证据 |

Context Entry 是引用或有界呈现，不是第二个权威记忆。物化文本只是投影；Hash 和来源引用可以支持审计，但不会自动授予访问底层来源的权限。

## 3. Context 身份和隔离

Context 绑定经过解析的身份引用，例如所有者/用户、项目、Agent、Agent Instance、Task、Session 和 Environment Scope。如果所选记忆或任务语义依赖某个世界、存档、模拟环境、租户或工作区，就必须绑定 Environment Identity。

环境身份缺失、存在歧义或被重复使用时必须 Fail Closed。新 Task 不得静默继承另一个 Task 的 Context；任何继承都必须显式授权。

G 保存解析后的不透明引用，并在读取、规划、修改、投递、Replay 和协调时重新检查授权。Agent 提供的 Scope 声明只能作为提示，不能成为权威。

## 4. G 负责什么

- Context 身份和带 Scope 的成员管理。
- ContextEntry 引用及呈现元数据。
- ContextVersion 和每个 Context 的权威版本序列。
- ChangeSet 操作及乐观并发/base-version 规则。
- 排序、激活理由、过期、预算和充分性评估。
- Snapshot/Delta 规划、Delivery Intent 和协调状态。
- Context 侧的 Forget 失效和内容抑制。

G 不拥有 Canonical Memory Version（D）、检索/索引状态（F）、全局身份和 Permission 策略（I）、BMCP Wire 编码（H），也不拥有 Agent 最终推理请求和本地应用行为（C/H）。

## 5. Context 操作与版本控制

常见操作包括 Add、Update、Remove、Replace、Reorder、Expire、Compact 和 Reconcile。变更作用于 G 管理的 Context，不作用于 Canonical Memory。

每次变更必须绑定预期 base version，或显式执行 Snapshot 转换。重试必须幂等。并发编辑必须串行化，或通过明确的并发控制解决；每个 Context 只能有一个权威版本序列。

Context Remove 的含义是“当前 Context 不再包含该条目”，不是“遗忘这条权威记忆”。Forget 是独立的治理流程，会使受影响的 Context Entry、Snapshot、Delta 和待处理 Delivery 失效。

## 6. Delivery 不等于 Applied

G 拥有 ContextVersion 和 Delivery Intent。H 拥有协议投递语义；C/H Adapter 拥有实际在推理边界物化了什么内容的证据。

必须区分以下阶段：
- Prepared：已形成投递包。
- Delivered：传输层报告已投递。
- Accepted：Adapter 校验并接受投递包。
- Applied：Adapter 证明约定推理边界中的最终请求受管区域包含目标 Context Version。
- Rejected/Expired/Superseded：该投递无法或不应应用。

收到消息或传输层 Delivered ACK 不等于 Applied 证明。Applied 也不证明模型关注、理解或遵循了记忆。

## 7. Applied 证据与推理边界

可信 Applied 记录必须按照治理契约，将相关 ContextVersion/ChangeSet 和 Delivery 身份绑定到 Adapter 身份/能力 Epoch、Inference Request 或最终请求摘要、解析后的 Scope 和 PermissionEpoch，以及适用时的当前 ForgetFenceGeneration。

证据必须对应实际提交给推理运行时的最终受管区域，不能只对应中间 Buffer 或较早的 Prompt 草稿。如果 Adapter 无法观察最终请求，就必须报告能力较弱的 ACK Class，不能声称达到 Tier 1 Full Applied。

## 8. Forget 和离线 Adapter 行为

Forget 会使受影响的 Context Entry、Snapshot、Delta 和待处理 Delivery Intent 失效。离线 Adapter 不得在重连后把过期内容当成当前内容重新投递。重连时必须先根据当前 ContextVersion、PermissionEpoch 和 Forget Fence 状态完成协调，再应用内容。

目标 Adapter 不可用或不支持某项能力时，不得自动算作成功。应保持 UNKNOWN/UNSUPPORTED，或按照 I 明确批准的残留例外策略处理。

## 9. 预算与充分性

Context 规划必须遵守受管区域 Token Budget，并尽量保留关键覆盖。Budget Manager 可以压缩或延后条目，但压缩必须保留 Canonical Source 引用和 Provenance，不能把低置信度或有争议的 Claim 改写成没有限定的断言。

充分性是相对于任务的评估，不保证 Agent 行为正确。预算、排序和压缩阈值仍需通过真实负载验证。

## 10. 故障与恢复

| 情况 | 必须行为 |
|---|---|
| Base Version 过期 | 拒绝或协调，不得覆盖 |
| 重复 ChangeSet | 返回幂等结果 |
| Adapter 离线 | 保持待投递/过期，不得标记 Applied |
| 传输部分成功 | 根据明确 Delivery 状态续传或替换 |
| Permission Epoch 变化 | 应用前重新授权 |
| Forget Fence 前进 | 取消/抑制过期 Snapshot、Delta 和 Delivery |
| 无法检查最终请求 | 不得声称 Tier 1 Full Applied |
| Token Budget 超限 | 保留 Provenance 地压缩/延后，不得静默丢弃强制不变量 |

## 11. 仍需验证

- ContextVersion/ChangeSet 并发和幂等。
- Delivery 状态转换与重连协调。
- 与 C/H/I 联合验证最终请求 Applied 证据。
- PermissionEpoch 和 ForgetFenceGeneration 竞态处理。
- Context Remove 与 Forget 的隔离。
- Token Budget 正确性和压缩 Provenance。
- 异构 Agent 接入和离线行为。

详细 Context 契约见 [G Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-g-memory-context/06-memory-context)。
