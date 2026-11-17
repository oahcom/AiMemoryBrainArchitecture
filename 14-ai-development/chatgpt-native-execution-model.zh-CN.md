# ChatGPT 原生 AI 开发执行模型

- 文档 ID：AI-ARCH-002
- 版本：0.1
- 状态：**PROPOSED — 尚未批准**
- Owner：A — 首席集成架构师
- 英文对应：[ChatGPT-Native AI Development Execution Model](chatgpt-native-execution-model.en.md)
- 上位规范：AI-STD-001、AI-PROC-001
- 工作项：AID-2026-001

## 1. 决策摘要

将**普通 ChatGPT 对话及已经验证的 GitHub 已连接应用工作流**作为唯一 AI 推理、设计、编码和审查通道。

GitHub 是持久化协作与证据系统。Ubuntu 仅负责确定性的构建、测试和 CI 执行。任何后台进程都不得调用 AI 模型。

本提案有意定义的是**由对话驱动的开发系统**，不是 7×24 小时无人值守 AI 服务。本文不声称 GitHub 事件能够唤醒或创建普通 ChatGPT 对话。

## 2. 已验证前提与非目标

项目已经验证：ChatGPT 对话可以通过已连接的 GitHub 应用读取和修改仓库内容、Issues、分支、提交及 Pull Requests。这是已接受的前提，本工作项不重复做该能力 POC。

本文不设计或授权以下内容：
- OpenAI API / Responses API Worker 或 API Key；
- Codex CLI、Codex Cloud 或 Codex 自动化；
- 任何第三方模型或本地模型；
- Desktop Commander 或本地电脑中转；
- 浏览器 Cookie 提取、会话令牌复用或未公开私有接口；
- 调用 ChatGPT 或任何模型端点的 GitHub Actions。

## 3. 系统边界

### 3.1 ChatGPT 对话

ChatGPT 对话是唯一 AI 执行单元。对话从 GitHub 读取任务、提示词、契约和当前仓库状态；通过已连接的 GitHub 应用执行授权范围内的推理与仓库操作；再将结果写回 GitHub。

对话是交互式、由用户启动的。一个任务可以跨越多轮对话，并可在后续新对话中依据 GitHub 中的持久记录恢复。

### 3.2 GitHub

GitHub 是跨对话协作的唯一事实来源，保存：
- Issues 和任务状态；
- 不可变的全局提示词与 Owner 专属提示词；
- 架构决策和中英双语规范；
- 分支、提交、Pull Requests 和审查评论；
- 测试运行链接、证据、问题和验收记录。

对话历史不是项目数据库。新对话必须能够通过 GitHub 工作项、提示词版本、准确 SHA 和证据恢复工作。

### 3.3 Ubuntu 与 GitHub Actions

Ubuntu 只允许执行确定性操作：checkout、构建、格式化、lint、单元/集成/一致性测试、打包，以及另有批准运行手册的部署步骤。

Ubuntu **禁止**：
- 调用 LLM 或 ChatGPT 端点；
- 使用 API Key、ChatGPT Cookie、OAuth Token 或浏览器会话来冒充 ChatGPT；
- 轮询 Issue 以生成 AI 工作；
- 自主编写代码或审查结论。

GitHub Actions 可以响应仓库事件启动确定性 CI。CI 结果是 ChatGPT 可以检查的证据，不是 AI 调用机制。

**当前仓库状态：** 清理后的 `main` 分支目前不包含任何 `.github/workflows/` 文件。主机上的自托管 Runner 可以继续保持注册状态，但本提案不声称仓库 CI 工作流已经配置或正在运行。只有在新增、审查并实际执行确定性工作流且取得证据后，CI 才能从 **NOT CONFIGURED / NOT RUN** 更新状态。

## 4. A–I 对话模型

每个 Owner 使用独立的 ChatGPT 对话上下文和版本化 Owner 提示词：

| Owner | 对话职责 |
|---|---|
| A | 任务接收、提示词编写、依赖排序、跨 Owner 集成、决策与证据登记 |
| B | 领域模型与领域身份语义（不含安全身份） |
| C | Agent 集成、遥测、推理边界要求 |
| D | Canonical Memory Brain、记忆生命周期、Forget 语义 |
| E | Memory Compiler 与派生记忆生产 |
| F | Memory Runtime、检索、激活、工作集和运行时缓存 |
| G | Memory Context、ContextVersion、ChangeSet 与协调 |
| H | BMCP 与 Adapter 协议行为 |
| I | 安全身份、认证/授权、隐私/保留治理及 Forget 安全控制（不拥有规范 Forget 生命周期语义） |

A 负责协调，但**不得替代领域 Owner 做决策**。每个 Owner 只能在已批准的职责范围内决策；跨 Owner 冲突必须升级处理。

独立审查由另一个 ChatGPT 对话执行，输入为冻结的提示词、任务记录、Diff、准确 SHA、测试证据和适用契约。审查者不得依赖实现者未记录的聊天上下文。

**独立性限制：** 不同对话提供上下文隔离和一次全新的审查，但并不提供不同模型、不同服务商或统计意义上的独立性。项目不得将其描述为多模型共识。高风险验收仍须遵守项目明确的安全与治理授权。

系统不会自动创建或启动九个对话。用户在 ChatGPT 中启动相应 Owner/Reviewer 对话并提供对应提示词。GitHub 为这些对话提供持久化交接依据。

## 5. 端到端运行闭环

1. **登记：** 创建 GitHub Issue 和 Work Item，记录唯一责任 Owner、任务类别/风险、范围、依赖和验收条件。
2. **准备：** A 创建或更新全局提示词与相关 Owner 提示词；提示词一旦执行，其版本即不可变。
3. **启动 Owner 对话：** 用户打开对应 Owner 的 ChatGPT 对话，提供提示词和 Work Item 引用。
4. **读取权威状态：** Owner 从 GitHub 读取准确的源文档、Issue、分支/基线 SHA、依赖 SHA 和既有证据。
5. **执行：** Owner 仅通过已连接的 GitHub 应用完成其授权范围内的设计或实现工作，创建任务分支并记录提交和变更路径。
6. **验证：** GitHub Actions/Ubuntu 执行确定性检查。ChatGPT 检查结果，并通过新的有界变更修复失败。
7. **审查：** 另一个 ChatGPT 对话读取冻结 PR 和证据，记录审查问题。实现对话不得自我批准。
8. **集成：** A 协调跨 Owner 兼容性并记录集成状态，不得覆盖领域 Owner 的决策权。
9. **验收与关闭：** 具备授权的验收方记录验收；只有在所需证据和批准齐全后才能合并。

每次状态迁移都写入 GitHub。Implemented、Verified、Reviewed、Accepted 和 Merged 必须保持不同状态。

## 6. 提示词目录

全局指令直接存放在全局提示词目录下；每个 Owner 的指令只放在自己的目录下。

```text
14-ai-development/
  prompts/
    global/
      chatgpt-session-contract-v1.md
    owners/
      A/owner-session-v1.md
      B/owner-session-v1.md
      C/owner-session-v1.md
      D/owner-session-v1.md
      E/owner-session-v1.md
      F/owner-session-v1.md
      G/owner-session-v1.md
      H/owner-session-v1.md
      I/owner-session-v2.md
```

每份 Owner 提示词必须引用全局会话契约、自己的权限边界、准确的权威源文档、任务验收条件和停止条件。已经执行的提示词版本不得覆盖。

## 7. 自动化边界与套餐限制

普通 ChatGPT 对话是选定的 AI 通道。**ChatGPT 定时任务不作为核心依赖**，因为它是另一个具有套餐限制的功能。

OpenAI 当前的定时任务文档明确说明：
- Free 和 Go：最多 3 个活跃定时任务；
- Free：重复任务最多每天运行一次，且采用灵活执行时段；
- Free 和 Go：不支持事件触发型（Webhook）任务；
- 事件触发的 GitHub PR 任务需要符合条件的 Work 套餐。

来源：[ChatGPT 中的定时任务 — OpenAI 帮助中心](https://help.openai.com/zh-hans-cn/articles/10291617-scheduled-tasks-in-chatgpt)。

因此本提案不承诺：
- 7×24 小时自主开发；
- GitHub Webhook 自动调用 ChatGPT；
- 自动创建 A–I 对话；
- 无限后台任务调度。

当前受支持的运行模式是：**用户启动 ChatGPT 对话 + GitHub 持久化工作状态 + 确定性 CI**。如果无人值守事件驱动执行成为强制要求，项目必须在当前套餐/功能约束下将其标记为 BLOCKED，而不是暗中替换为 Codex、API 调用或其他模型。

## 8. 安全与权限规则

- 只能使用已经授予 ChatGPT 的 GitHub 应用权限。
- 禁止在提示词或仓库文件中索取、保存、打印或提交 PAT、OAuth 凭据、浏览器 Cookie 或服务器密码。
- Ubuntu 不保存任何 AI 凭据。
- 自托管 Runner 不是 AI Worker。应保留现有主机级准入保护，直到另行完成审查；不得新增 AI 调用型 Job。
- 不自动合并。仍须由人或项目授权的验收方明确批准。
- 没有准确证据时，不得声称测试、审查、部署或运行结果已经完成。

## 9. 本提案验收条件

- 普通 ChatGPT 对话是唯一 AI 通道。
- GitHub 是跨会话持久化状态与证据层。
- Ubuntu/GitHub Actions 只执行确定性检查。
- A–I 职责边界和独立审查对话明确。
- 提示词目录区分全局指令与 Owner 专属指令。
- 不依赖定时任务、Codex、API Worker、Desktop Commander、其他模型或本地中转。
- 不把交互式操作伪装成无人值守自动化。
- 中英文版本语义和状态一致。

## 10. 未决决策

1. 在禁止额度依赖和 API 的约束下，项目是否接受由用户启动对话的协作模式。
2. 是否修订现有治理规范，明确将“独立 ChatGPT 对话”定义为上下文独立审查，并同时声明其不具备模型独立性。
3. 每个 Owner 提示词默认必须读取哪些准确的仓库契约和测试套件。

上述事项决议前，AI-ARCH-002 保持 **PROPOSED**，不授权生产自动化或自主执行。
