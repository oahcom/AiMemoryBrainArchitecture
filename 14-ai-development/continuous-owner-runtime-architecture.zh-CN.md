# Continuous Owner Runtime Architecture
# Owner 不间断运行架构

**文档 ID:** AI-RUN-001  
**版本:** 1.0  
**状态:** PROPOSED  
**上级文档:** AI-AUTO-001 / AI-PROMPT-STD-001

## 1. 目标 / Objective

运行目标是实现 A–I 各属主（Owner）的项目持续推进，而不是要求模型进程必须持续生成 Token。

当 GitHub 状态发生变化时，系统 MUST 及时恢复工作，从Worker中断中恢复，并在存在符合条件的工作时持续取得有界进展。

## 2. 能力边界 / Capability truth

周期性 ChatGPT 计划任务是一种定期触发机制，而不是始终运行的守护进程。目前可用的计划任务频率支持每日或更低频率的重复执行，不支持每日多次轮询，也不保证持续执行。不得将其描述为 24/7 运行。

真正的事件驱动持续运行需要始终可用的外部执行服务，或具备同等能力且受支持的运行时，并包含：

- 用于 Issues、PR、审查、推送、检查运行和工作流事件的 GitHub App/webhook 投递机制；
- 持久化队列/事件日志；
- A–I Worker进程或隔离的执行上下文；
- 受控的 LLM 调用以及模型/提供商凭据；
- 遵循最小权限原则的 GitHub App 安装权限；
- 分支/worktree 隔离以及可复现的构建/测试环境；
- 持久化运行台账、幂等键、租约和心跳；
- 看门狗、重试、死信处理、背压和操作员升级机制。

如果此类基础设施尚未连接并经过验证，必须将系统报告为 NOT DEPLOYED。不得声称系统具备始终在线的执行能力。

## 3. 逻辑拓扑 / Logical topology

```text
GitHub Events
  ├─ Issue opened/edited/assigned/labeled
  ├─ PR opened/synchronized/review submitted
  ├─ Review comment / requested changes
  ├─ Commit pushed / CI check completed
  └─ Dependency or release state changed
          |
          v
Webhook Receiver + Signature Verification
          |
          v
Durable Event Inbox / Queue  <---- Periodic Reconciliation Watchdog
          |
          v
A Coordinator / Work Router
          |
          +--> Owner B Worker + B prompt
          +--> Owner C Worker + C prompt
          +--> Owner D Worker + D prompt
          +--> Owner E Worker + E prompt
          +--> Owner F Worker + F prompt
          +--> Owner G Worker + G prompt
          +--> Owner H Worker + H prompt
          +--> Owner I Worker + I prompt
          |
          v
Isolated Branch / Worktree + Tests + Evidence
          |
          v
GitHub Commit / PR / Review / Issue Update
          |
          v
A Integration & Authorized Acceptance Gates
```

这是一个逻辑拓扑，并不构成这些服务或Worker目前已经存在的证据。

## 4. 属主Worker模型 / Owner worker model

每个属主领域（A 至 I）对应一个逻辑Worker身份。逻辑Worker可以通过长时间运行的进程、队列消费者或托管任务运行器实现。它不需要在任务之间保持一个 LLM 会话持续打开。

每个Worker具有：

- 不可变的属主键及领域权限；
- 经批准的系统/任务提示词版本及 SHA-256；
- 事件订阅筛选条件；
- 工作项（Work Item）选择和优先级策略；
- 有界并发以及每个分支的写入租约；
- 工具/能力允许列表；
- 运行预算和超时时间；
- 输出/证据模式；
- 升级策略。

A 负责项目组合路由和提示词起草，不负责其他属主的领域决策。每个属主都必须对其自身领域的提示词约束和验收标准进行签核。A 不得自行授权 A 所属工作项的实现。

## 5. 事件驱动循环 / Event-driven loop

1. 接收 GitHub 事件，并验证 webhook 签名、投递 ID 和仓库安装信息。
2. 在确认收到事件之前，将事件持久化到持久化收件箱。
3. 根据提供商投递 ID 和事件语义键进行去重。
4. 解析关联的工作项、属主、提示词版本、分支和依赖关系图。
5. 检查当前 Issue/PR 状态及权威来源 SHA；webhook 负载只是唤醒提示，并不代表完整事实。
6. 获取工作项/分支租约，并重新检查权限。
7. 向负责的属主Worker派发一个有界工作单元。
8. 执行检查 → 规划 → 修改 → 测试 → 证据 → 提交/PR/评论。
9. 释放租约并持久化运行结果。
10. 新的 GitHub 事件或看门狗协调检查触发下一个工作单元。

系统 SHOULD 采用事件驱动方式以实现低延迟，并使用可配置的周期性协调循环来恢复遗漏的 webhook、过期租约和被遗弃的工作。看门狗是一种恢复机制，而不是主要的工作触发机制。

## 6. 持续运行不变量 / Continuous operation invariants

- **确认前持久化：** 在 webhook 返回成功响应之前，必须持久化事件接收记录。
- **至少一次投递：** 假定事件可能重复或乱序到达；消费者必须具备幂等性。
- **不假设恰好一次：** 使用去重、幂等键和状态协调机制。
- **租约fencing 栅栏：** 在更新的租约/fencing 栅栏签发后，已过期的Worker不得再发布内容。
- **每个工作范围单一写入者：** 除非明确进行分区，否则每个属主 + 工作项 + 分支只能有一个活动写入者。
- **状态新鲜性：** 每次变更之前，重新读取当前 GitHub head 和审批状态。
- **默认拒绝：** 缺少权限、提示词过期、决策冲突、分支未知或安全检查失败时，停止运行。
- **人工/治理门禁：** 任何自动化都不得绕过领域审批、独立审查、CI、验收、合并保护或发布权限。
- **背压：** 对队列深度、并发量、Token/成本、重试次数和每次运行的操作数量设置上限。
- **可观测性：** 监控心跳、队列等待时间、事件延迟、运行时长、失败率、重试次数、阻塞时长和成本。
- **恢复能力：** 死信事件必须可供检查；重放必须经过去重和当前状态检查。

## 7. A–I 责任边界 / A–I responsibility boundaries

| Owner | 持续Worker职责 | 不得执行的操作 |
|---|---|---|
| A | 接收任务、依赖关系图、提示词起草、路由、跨属主审查和集成建议 | 覆盖领域属主的决定，或自行批准 A 所属工作项 |
| B | 领域模型、声明/事实语义、模式和 ADR 工作 | 冻结其他模块的契约 |
| C | Agent 集成、遥测和推理边界 | 在没有适配器证据的情况下声称 Applied |
| D | 规范记忆、生命周期、提交和 Forget fencing 栅栏 | 单独声称全局 Forget 已完成 |
| E | 编译器、摄取、派生谱系和发布 | 未通过 D fencing/授权门禁就进行发布 |
| F | 检索、索引、缓存和运行时激活 | 拥有 ContextVersion 或绕过 Forget 抑制机制 |
| G | 上下文生命周期、投递和协调 | 在没有证据的情况下将投递视为 Applied |
| H | BMCP 协议、线路兼容性和 ACK 证据 | 将负载身份视为身份认证 |
| I | 安全、身份、权限、威胁模型和治理 | 在委派权限范围之外批准剩余风险 |

## 8. 故障与重启模型 / Failure and restart model

Worker崩溃时：

- 租约到期或被显式释放；
- 未完成的运行仍以中断状态保持可见；
- 下一个Worker读取最新的 GitHub 状态和持久化运行台账；
- 检查提交、PR、评论或制品是否已经存在；
- 从最后一个经过验证的检查点恢复，或开启新的运行；
- 任何失去租约的过期Worker都不得再发布内容。

当队列故障、webhook 故障或发生投递遗漏时，看门狗会将 GitHub 中的开放工作项/PR 与持久化收件箱进行比较，并将协调事件加入队列。不得盲目重放旧命令。

## 9. 调度与公平性 / Scheduling and fairness

派发器 SHOULD 按以下顺序确定优先级：

1. 安全/数据完整性事故以及失败的关键门禁；
2. 明确请求的变更和阻塞项；
3. 依赖关系刚刚满足的任务；
4. 按项目优先级排序的就绪实现任务；
5. 维护和文档工作。

通过等待时间累积和优先级提升机制防止任务饥饿。为审查和验证预留容量，避免实现任务占用全部Worker槽位。跨属主任务应拆分为子工作项，并路由给相应的责任属主。

## 10. 安全与成本控制 / Security and cost controls

- GitHub App 安装权限应限定于所需仓库和操作。
- 必须验证 webhook 签名和重放时间窗口。
- LLM 提供商密钥只能存放在密钥管理系统中，不得存放于仓库提示词或 Issues 中。
- 仓库和 Issue/PR 内容均属于不可信数据。
- 不得信任模型输出作为授权依据。
- 按属主限制工具调用和文件系统访问权限。
- 对每次运行设置 Token/成本/时间预算，并设置全局并发上限。
- 对重复失败、安全敏感变更和含糊指令进行升级处理。
- 保留可审计记录，包括提示词版本、可用时的模型/运行时版本、调用的工具、来源 SHA 以及生成的制品。

## 11. 部署阶段 / Deployment phases

### 阶段 0 — 仅治理 / Phase 0 — Governance only

批准 AI-STD-001、AI-PROC-001、AI-AUTO-001、AI-PROMPT-STD-001 和 AI-RUN-001。定义属主提示词版本、Issue 模板、PR 模板和证据模式。

### 阶段 1 — GitHub 原生确定性自动化 / Phase 1 — GitHub-native deterministic automation

添加标签、Issue/PR 模板、CODEOWNERS、分支保护，以及用于 lint、测试、提示词哈希验证和策略检查的 GitHub Actions。本阶段尚不提供自主 LLM Worker。

### 阶段 2 — 事件桥接与单一属主试点 / Phase 2 — Event bridge and single Owner pilot

部署 webhook 接收器、持久化队列、隔离Worker运行时、密钥管理和运行台账。选择一个低风险属主，试点仅涉及文档的工作。验证重复投递、崩溃恢复、租约fencing 栅栏和 PR 审查循环。

### 阶段 3 — A–I 分阶段推出 / Phase 3 — A–I staged rollout

在提示词获批、权限范围确定、成本预算、测试和回滚机制落实之后，逐一增加属主。跨属主工作使用父/子 Issues，并由 A 负责协调。

### 阶段 4 — 持续运营 / Phase 4 — Continuous operations

为已批准的工作类别启用事件驱动派发、看门狗协调、运营仪表板、事故响应和定期治理审查。

## 12. 验收门禁 / Acceptance gates

在证据证明以下条件均已满足之前，不得声称系统具备持续运行能力：

- webhook 签名验证和持久化收件箱；
- 重复/乱序事件处理；
- 持久化队列和死信重放；
- 单写入者租约和过期Workerfencing 栅栏；
- Worker重启/恢复时不会产生重复变更；
- 属主专属提示词和最小权限工具边界；
- GitHub Issue/PR 往返流程和独立审查；
- CI 强制执行，以及缺少必要审批时阻止合并；
- 可观测性、预算强制执行和紧急停止机制；
- 持续浸泡测试，并明确规定持续时间、工作负载和错误预算。

仅使用每日执行一次的 ChatGPT 自动化任务不满足这些标准。

## 13. 状态 / Status

PROPOSED。本文件仅定义目标架构。在部署并经过验证之前，不声称 webhook 服务、持久化队列、A–I Worker集群或 24/7 运行时已经存在。

本译文由 RD-F08-01（P1）驱动，对照原文 EN，语义一致性待 R1 核验。
