---
document_metadata:
  domain: agent-integration
  role: design-specification
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: "Pending Owner review"
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "07-agent-integration/adapter-capability-tiers.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "完整中文翻译草稿；尚待独立语义审查及 Owner 确认。"
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Agent Adapter capability tier specification"
    canonical_scope_id: null
    canonical_scope_keywords:
      - agent-adapter
      - capability-tier
      - inference-boundary
      - active-recall
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
---

# Agent Adapter 能力等级

**状态：** 等级意图与保证边界已决定；符合性细节为候选  
**Owner：** Session C — Agent Integration 边界预设计  
**协议：** Session H 负责 BMCP 能力协商与 Adapter 实现契约。

**规范性措辞约定：** MUST 译为「必须」，SHOULD 译为「应当」，MAY 译为「可以」。这些中文措辞分别保留原文规范性要求的强度，不得将「必须」降格为建议，也不得将「可以」解释为强制要求。原文中的 DECIDED、CANDIDATE、OPEN、TO_VALIDATE 等状态标记，以及接口名、操作枚举、拒绝码和字段名均保持英文原样。

## 1. 目的

能力等级用于分类某个集成能够可靠地观察、请求、接收和应用哪些内容。它们不是对 Agent 智能水平的排名。等级仅描述集成能够提供的保证。

## 2. 等级概览

| 能力 | Tier 1 — 完整推理边界 | Tier 2 — 中间件 | Tier 3 — 事件与 Active Recall |
|---|---|---|---|
| 结构化遥测 | 支持 | 中间件可见的子集 | 事件／显式请求子集 |
| Active Recall | 支持 | 支持 | 支持 |
| 主动上下文交付 | 支持 | 支持，交付至中间件槽位 | 不作保证 |
| 推理提交前应用 | 支持 | 在受控路径上支持 | 不支持 |
| 已应用版本证明 | 支持 | 在受控路径上支持 | 不支持 |
| Snapshot／delta 协调 | 完整支持 | 中间件支持的子集 | 不适用 |
| 观察任务／会话变化 | 若已暴露则支持 | 中间件可见 | 仅限显式提交 |
| 环境遥测 | 支持 | 若已埋点则支持 | 可选 |
| 隔离的 Brain 管理区域 | 明确支持 | 由中间件定义的槽位 | 不作保证 |
| 模型理解保证 | 无 | 无 | 无 |

## 3. Tier 1 — 完整推理上下文边界

### 定义

Adapter 能够观察相关的请求组装边界，并且能够在请求提交至推理运行时之前，修改一个专用的、由 Brain 管理的记忆区域。

### 必需能力

- 映射规范遥测，并识别 Agent 实例／会话／任务／环境作用域。
- 接收快照和增量 Change Set。
- 校验作用域、基础版本／目标版本、能力、预算以及受管理区域的所有权。
- 在推理提交之前，应用完整的、已接受的 Brain 管理区域内容。
- 证明精确版本，并提供边界／请求关联信息。
- 检测不受支持的操作、预算溢出和版本缺口。
- 当 delta 连续性丢失时，通过完整快照进行协调。
- 将受保护指令、用户输入、Agent 策略和工具定义保留在受管理区域之外。

### 保证

**DECIDED：** 对于特定推理请求组装，Tier 1 能够证明指定版本已应用到指定记忆区域。

### 不作保证的事项

Tier 1 不保证模型会关注、理解或正确使用相关内容，也不保证响应正确、Agent 遵从要求，或能够修改正在执行中的推理。不得据此推断系统会暴露隐藏推理过程。

## 4. Tier 2 — 中间件集成

### 定义

集成通过中间件、编排钩子、Prompt／上下文构建器或请求拦截器实现。此类组件能够访问发出的请求和指定记忆槽位，但不一定能够观察所有内部状态或所有推理路径。

### 必需能力

- 提交中间件钩子可见的遥测。
- 支持显式 Active Recall。
- 通过中间件管理的槽位接收上下文更新。
- 在经过受控钩子的请求发出之前，应用已接受的更新。
- 报告已覆盖的请求路径和绕过受控钩子的请求路径。
- 为受控槽位维护已应用版本记录。

### 保证

**DECIDED：** 如果 Tier 2 能够检查最终发出的请求表示，那么它可以证明指定上下文版本已插入经过其受控组装钩子的请求。

### 不作保证的事项

Tier 2 不保证覆盖绕过受控钩子的路径，不保证获得完整 Agent 状态、隐藏或由 Provider 管理的上下文、所有任务／环境转换，也不保证模型理解。若不具备与 Tier 1 等效的边界可观测性和控制能力，不得声称具备 Tier 1 覆盖范围。

## 5. Tier 3 — 事件与 Active Recall

### 定义

Tier 3 是一种最小化集成方式，适用于能够提交带作用域的事件／遥测并显式请求记忆，但无法在推理边界可靠接受 Brain 主动上下文变更的 Agent。

### 必需能力

- 对生产者进行身份认证，并提交带作用域的遥测／事件。
- 为可重试写入提供幂等标识符。
- 使用显式作用域和任务上下文请求 Active Recall。
- 通过 API／工具响应，以数据形式接收记忆结果。
- 在向下游传递结果时保留来源／出处引用。

### 保证

**DECIDED：** Tier 3 仅保证已接受的遥测契约和 Recall 响应契约。它不作主动同步保证，也不作 Applied Context 声明。Agent 自行决定是否以及如何将结果放入自身上下文；Brain 无法验证这一行为。

### 安全降级

Tier 3 不属于错误状态。Brain 保留规范记忆和 Recall，将结果标记为数据，不创建具有误导性的主动交付，并明确暴露同步能力不受支持。在边界能力通过验证后，可以升级 Tier。

## 6. 协商能力

最终协商消息由 Session H 负责。逻辑声明包括：

- Tier 和功能标志。
- 支持的遥测信号类型和 Schema 版本。
- 支持的上下文操作以及 snapshot／delta 模式。
- 在已知情况下，最大上下文负载／Token／字节预算。
- 确认语义。
- 推理边界类型和最终请求可见性。
- 环境遥测支持情况。
- 离线缓冲和协调支持情况。
- 不支持的功能和已知绕过路径。

能力声明在通过符合性测试之前不构成保证。协商必须具有版本，并绑定到经过身份认证的 Adapter 身份。

## 7. Tier 选择规则

1. 选择已被证明的最高等级，而不是仅选择所声明的等级。
2. 覆盖路径不完整的中间件可以属于 Tier 2，但必须披露绕过路径。
3. 如果插入操作没有精确的版本／请求标识，就不具备完整的 Tier 1 Applied 语义。
4. 仅通过 API／工具提供 Recall 的集成属于 Tier 3。
5. 能力丧失时，集成进入 Degraded；停止作出不受支持的保证。
6. Tier 升级必须重新验证并协调上下文。

## 8. Tier 状态机

~~~mermaid
stateDiagram-v2
  [*] --> Unassessed
  Unassessed --> Negotiating
  Negotiating --> Tier1: boundary, apply, attest verified
  Negotiating --> Tier2: middleware path verified
  Negotiating --> Tier3: events and recall verified
  Negotiating --> Unsupported: minimum contract unavailable
  Tier1 --> Degraded: capability lost
  Tier2 --> Degraded: capability lost
  Tier3 --> Degraded: capability lost
  Degraded --> Negotiating: revalidation
  Tier1 --> Negotiating: capability change
  Tier2 --> Negotiating: capability change
  Tier3 --> Negotiating: upgrade
  Unsupported --> Negotiating: new Adapter version
~~~

状态转换：

- Unassessed 转为 Negotiating：完成经过身份认证的注册。
- Negotiating 转为 Tier N：所有该 Tier 的符合性检查均通过。
- Tier N 转为 Degraded：必需能力不可用，或证明不再可靠。
- Degraded 转为 Negotiating：恢复的能力经过重新验证。
- Tier N 转为 Negotiating：Adapter 版本／功能发生变化。
- Negotiating 转为 Unsupported：没有任何 Tier 的最低要求能够通过。

单纯的传输故障不一定需要降低 Tier；连接状态应单独跟踪。

## 9. 失败行为

| 失败情况 | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Brain 离线 | Agent 继续运行；仅使用有效且已授权的本地上下文 | 中间件路径同左 | Recall 不可用 |
| Adapter 离线 | 不再进行新的应用 | 不再进行新的中间件插入 | 不再接收输入／提供 Recall |
| 版本缺口 | 拒绝 delta；通过 snapshot 协调 | 受控槽位采用相同处理 | N/A |
| 中间件绕过 | 在所声明的边界保证下不应发生 | 将该请求标记为未覆盖 | 由 Agent 控制 |
| 超出预算 | 拒绝，或执行显式协商的压缩 | 同左 | 遵循显式响应截断契约 |
| 权限撤销 | 停止交付并进行协调 | 同左 | 在适用情况下拒绝 Recall／输入 |
| 部分应用 | 除非具有显式的部分应用语义，否则拒绝 | 同左 | N/A |

## 10. 安全

Tier 本身不授予权限。作用域和授权仍然是强制要求。Adapter 身份必须绑定到 Agent／实例以及允许访问的作用域。Memory 是数据，绝不是指令。

Tier 1／2 的插入操作仅限于受管理区域；Tier 3 的结果属于不可信数据。降级不得扩大访问权限。本地缓存必须遵守保留期限、撤销和 Forget 要求。

## 11. 性能与验收

应测量以下指标：遥测覆盖率、Recall 延迟／质量、交付／应用延迟（Tier 1／2）、版本滞后、拒绝率和协调率、推理路径覆盖率、中间件绕过率，以及在受控比较条件下的 Agent 结果。

验收要求：

1. Tier 1 通过 snapshot、delta、缺口恢复、区域隔离和 Applied 证明测试。
2. Tier 2 报告已覆盖与被绕过的请求，并且绝不声称已应用于被绕过的请求。
3. Tier 3 支持带作用域的遥测／Recall，且不产生虚假的 Applied 声明。
4. 无效的能力声明必须无法通过符合性验证。
5. 能力丧失时进入 Degraded，并停止作出不受支持的保证。
6. Tier 升级必须先重新验证并协调，然后才能声称具备新 Tier。
7. 所有 Tier 均拒绝跨作用域访问。
8. 所有 Tier 均保持数据与指令分离。

## 12. 接口与待决事项

- **Session H：** 协商 Schema、消息 ID、确认机制和符合性握手。
- **Session G：** 上下文操作、版本协调、部分应用语义、Applied 记录。
- **Session I：** 本地缓存保留期限、撤销、离线缓冲、审计。
- **OPEN：** Tier 2 覆盖范围应采用百分比，还是逐请求记录。**CANDIDATE：** 逐请求记录具有权威性。
- **TO_VALIDATE：** 最低符合性测试套件和覆盖证据。

## 13. 决策摘要

- **DECIDED：** Tier 描述集成保证，而不是 Agent 质量。
- **DECIDED：** Tier 1 在完全可观测的推理边界应用上下文。
- **DECIDED：** Tier 2 仅在中间件控制的路径上应用上下文。
- **DECIDED：** Tier 3 提供事件和 Active Recall，不提供主动 Applied 语义。
- **DECIDED：** 任何 Tier 都不保证模型理解。
- **DECIDED：** 能力声明必须具有符合性证据；失败会触发显式降级。
- **OPEN：** 线上协商属于 Session H 的职责范围。

## 14. 可执行操作绑定（参考模型契约）

以下操作映射使已经标记为 DECIDED 的 Tier 保证具备可执行形式。这是一个确定性的参考模型契约，不是 BMCP 线上协商协议，也不是生产级 Adapter 实现。

| 操作枚举 | 最低 Tier | Tier 1 | Tier 2 | Tier 3 |
|---|---:|---:|---:|---:|
| `SubmitScopedTelemetry`（提交带作用域的遥测） | 3 | 允许 | 允许 | 允许 |
| `RequestActiveRecall`（主动回忆请求） | 3 | 允许 | 允许 | 允许 |
| `InsertMiddlewareMemorySlot`（写入中间件记忆槽） | 2 | 允许 | 允许 | 拒绝 |
| `AttestMiddlewareApplication`（证明中间件应用） | 2 | 允许 | 允许 | 拒绝 |
| `ObserveFullInferenceBoundary`（观察完整推理边界） | 1 | 允许 | 拒绝 | 拒绝 |
| `ApplyFullBoundaryMemory`（在完整边界应用记忆） | 1 | 允许 | 拒绝 | 拒绝 |
| `AttestFullBoundaryApplication`（证明完整边界应用） | 1 | 允许 | 拒绝 | 拒绝 |
| `ReconcileSnapshotAndDelta`（快照与增量协调） | 1 | 允许 | 拒绝 | 拒绝 |

较低 Tier 不得仅仅因为能够表达某项请求，就执行该操作。参考模型返回类型化错误 `AdapterError::TierInsufficient { required, actual }`；调用方必须根据枚举进行分支处理，不得解析显示文本。Tier 1 包含 Tier 2 和 Tier 3 的操作能力；Tier 2 包含 Tier 3 的操作能力。

### 边界拒绝码

参考模型还暴露了类型化的边界拒绝原因：

- `ProtectedRegionMutation(region)`：任何试图写入 System 指令、Developer 指令、用户输入、Agent 安全策略、工具 Schema／授权或 Agent 工作状态的操作。
- `RequestAlreadyFrozen`：请求组装器已经冻结推理请求后，仍试图修改受管理区域。

这两条规则直接落实 `inference-boundary-model.md` 中已经决定的原则：受保护区域不得由 Brain 写入；正在执行中或已经冻结的请求不可变。这是当前实现的两种边界情形；版本缺口协调仍由源契约规定，但尚未由这个最小参考模型实现。

### 作用域与状态

此映射是对本文中已经标记为 DECIDED 的 Tier 保证所作的可执行解释。线上协商、经过身份认证的能力声明、传输、Provider 集成、实际推理以及生产级遥测均不在本模型范围内。本模型不声称实现上述任何能力。

## 15. 内存上下文交付生命周期（已实现的参考行为）

crate 现在提供 `ContextDeliveryAdapter` trait 和 `InMemoryContextDeliveryAdapter`。内存实现按 session 保存已应用的 `ContextSnapshot` 与连接标志。

| 生命周期动作/状态 | 已实现行为 |
|---|---|
| 已连接 / apply | 仅接受精确的后继版本（新 session 或清空后的 session 从版本 1 开始）；只有接受后才记录快照 |
| 版本拒绝 | 返回类型化错误 `AdapterError::VersionMismatch { expected, received }`；已应用快照保持不变 |
| Clear | 移除已应用快照；下一次 apply 从版本 1 开始 |
| 已断连 | 使用 `SessionDisconnected` 拒绝 apply；保留最后一次成功应用的快照 |
| Reconnected | 恢复内存连接标志，并报告最后一次成功应用的版本（或 `None`） |

**NOT IMPLEMENTED（未实现）：** 真实传输；逐运行时 Agent 集成；持久化交付账本；持久化 session 状态；自动重试/重新交付；生产级协调或应用证明。Reconnect 只是确定性的内存状态转换，并不能证明远端 Agent 的真实状态。本实现不转换 Provider 特定运行时对象，也不声称交付状态超出当前进程内存的范围。
