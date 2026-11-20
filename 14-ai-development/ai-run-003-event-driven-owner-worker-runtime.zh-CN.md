# AI-RUN-003 — 事件驱动 Owner Worker 运行时试点
# AI-RUN-003 — 事件驱动 Owner Worker Runtime 试点架构

**状态 / Status:** PROPOSED — 仅设计基线 / 提案中——仅设计基线  
**风险 / Risk:** 只读试点为 R2；自主仓库写入、秘密或主机管理操作为 R3 / R2 for read-only pilot; R3 for autonomous repository writes, secrets, or host administration  
**责任 / Owner:** A — 集成与编排；I — 安全与治理；选定的试点 Owner — 领域执行 / A — Integration & orchestration; I — security/governance; selected pilot Owner — domain execution  
**跟踪 / Tracking:** Issue #30; 依赖 #26 和 PR #27

---

## 1. 目标 / Purpose

在用户管理的 Ubuntu 主机上构建持久化、事件驱动的执行服务，使 A–I Owner 工作无需保持 ChatGPT 会话持续打开也能推进。

GitHub Actions self-hosted runner 仅是显式派发 Workflow 的执行底座，**不是**事件接收器、持久化队列、协调器或自主 Owner 集群。

## 2. 当前证据与禁止推断 / Current evidence and non-claims

| 项目 / Item | 当前状态 / Current status |
|---|---|
| Ubuntu Tailscale daemon | 操作方报告已启用/活动 / Operator-reported enabled/active |
| GitHub `ai-worker` runner | 操作方确认在线且服务已启动；未经独立查询 / Operator-confirmed Online and service started; not independently queried |
| 只读诊断 | Workflow 文件存在于 PR #27 分支；未观察到匹配的运行记录 / Workflow file exists on PR #27 branch; no matching run observed |
| PR #27 | 已可审查、开放、未合并；最近一次查询时正式审查列表为空 / Ready for Review, open, not merged; formal review list empty at last query |
| Main 分支保护 | 早期检查报告未启用；当前集成无法读取此管理端点，因此必须由仓库管理员重新核验 / Earlier check reported disabled; current integration cannot read this admin endpoint, so re-verification by a repository administrator is required |
| A–I Worker运行时 | 尚未部署 / Not deployed |

这些事实不能证明重启恢复能力、最小权限隔离、持久化事件处理能力、24/7 可用性或 A–I 自主运行能力。

## 3. 目标与非目标 / Goals and non-goals

### 目标 / Goals

1. 接收经过身份验证的 GitHub 事件，并在确认投递之前将其持久化。
2. 至少一次处理事件，同时确保工作项执行具有幂等性。
3. 通过定期读取 GitHub 进行对账，以弥补遗漏的事件。
4. 将一个有界工作项路由至一个已批准的 Owner Prompt 和隔离的Worker。
5. 强制实施租约、fencing token、超时、预算、背压、重试和死信处理。
6. 生成可审计的运行证据，并更新 GitHub Issue/PR。
7. 从一个低风险 Owner 试点开始；只有通过明确的 Gate 后才能扩展。

### 非目标 / Non-goals

- 不一次性启动全部 A–I。
- 不在持久化主机上执行来自不可信 fork/PR 的代码。
- 试点阶段不允许自主合并、发布、破坏性迁移、生产数据删除或权限扩张。
- 在完成压力持续运行测试和恢复证据验证之前，不宣称提供 24/7 服务。
- 不替代 GitHub Issues/PRs 作为工程事实记录系统。

## 4. 逻辑架构 / Logical architecture

```text
GitHub App Webhook
        |
        v
HTTPS Ingress + Signature Verification
        |
        v
Durable Event Inbox -----> Delivery Deduplication
        |
        v
Event Normalizer / Policy Filter
        |
        v
Reconciliation + Eligibility Evaluator <---- GitHub API (source of truth)
        |
        v
Durable Work Queue
        |
        v
A Coordinator
        |
        +---- Prompt Registry (version/hash/Owner approval)
        |
        +---- Work Lease + Fencing Token
        |
        v
Isolated Owner Worker (one pilot Owner)
        |
        v
Dedicated Worktree / Branch / Tests
        |
        v
Evidence Publisher -----> GitHub Issue / PR / Checks
        |
        v
Run Ledger + Metrics + Audit Log
```

Webhook Receiver、Coordinator 和 Worker 执行是彼此独立的逻辑组件，即使首个试点将它们打包为少量 systemd 服务，也不改变这一点。

## 5. 事件接收契约 / Event ingestion contract

### 5.1 身份验证 / Authentication

- 仅接受 HTTPS。
- 使用配置的 GitHub App webhook secret，对原始请求体精确计算并验证 `X-Hub-Signature-256`；采用恒定时间比较。
- 对缺失、格式错误或无效的签名，在持久化之前予以拒绝。
- 强制执行请求体大小限制和 Content-Type 策略。
- 对事件类型和仓库身份实施白名单；忽略所有其他事件。
- 默认不记录原始 Payload；仅持久化必要字段和受保护的 Payload 引用。

### 5.2 先持久化后确认 / Durable-before-ACK

Receiver 必须先持久化 Inbox 记录及其去重键，然后才能返回成功的 2xx 响应。如果持久化存储不可用，则返回可重试的失败响应；绝不能确认仅保存在内存中的事件。

Inbox 最小字段：

- `delivery_id`（GitHub delivery UUID；唯一）
- `repository_id`, `event_type`, `action`
- `received_at`, `payload_digest`, `payload_ref`
- `verification_result`, `processing_state`, `attempt_count`
- `correlation_id`, `last_error_class`

### 5.3 重复与乱序事件 / Duplicate and out-of-order events

- 投递级幂等键：`github:<repository_id>:<delivery_id>`。
- 工作级幂等键必须标识语义上的工作目标，例如：仓库 + issue/PR 编号 + 当前目标修订版本 + 工作类别 + 已批准 Prompt 摘要。
- 不同的 delivery ID 可能代表相同的语义变更；创建工作项时必须再次去重。
- 不得假设 Webhook 按顺序到达。执行前必须从 GitHub 重新获取当前 Issue/PR/分支/检查状态，并依据当前状态评估执行资格。
- 过期事件可以触发对账，但不得授权基于过期状态的写入。

## 6. 队列、租约与 fencing / Queue, leases and fencing

工作项按以下状态流转：

`DISCOVERED → ELIGIBLE → QUEUED → LEASED → RUNNING → EVIDENCE_PENDING → COMPLETED`

异常状态：

`BLOCKED`, `RETRY_WAIT`, `DEAD_LETTER`, `CANCELLED`, `SUPERSEDED`, `FAILED`。

租约包含 `work_item_id`、`worker_id`、`lease_expires_at` 和单调递增的 `fencing_token`。每次回写操作都必须证明其持有当前 fencing token。租约过期并由新的Worker重新领取该工作项时，fencing token 必须递增；过期的Worker不得再发布 Commit 或完成证据。

租约权威必须具备持久化和原子性。仅依赖进程内 Mutex 并不足够。Worker必须在租约过期前发送心跳；如果错过心跳，则应触发租约过期和恢复，而不是静默继续执行。

### 6.1 带 fencing 的发布权限 / Fenced publication authority

只有在实际执行副作用的系统强制检查 fencing token 时，fencing token 才能发挥作用。如果Worker持有共享 GitHub 写入 Token，就可以绕过 Coordinator 侧的租约检查，在租约过期后继续 Push。因此，在试点阶段：

- Owner Worker不获得 GitHub 写入凭据。
- 所有 GitHub 变更（创建分支、Push、PR/评论/Check 更新）都必须通过由 Coordinator 控制的单一 Publication Broker。
- Broker 在接受每次变更之前，必须原子地验证当前租约所有者、fencing token、工作项状态、允许写入的路径以及预期的 base/head SHA。
- Broker 拒绝已过期（expired）、已被取代（superseded）或陈旧（stale）的 fencing token 的请求。Worker此前执行过的检查并不足以满足要求。
- 如果 Broker 无法提供原子 compare-and-set 强制校验，则必须继续禁用自主回写；Worker只能生成 Patch Artifact，供人工应用。
- 在 Broker 内部使用范围严格受限的短期 GitHub App installation token；不得将其暴露给Worker进程或其 Worktree。

## 7. GitHub 权威与凭据 / GitHub authority and credentials

- GitHub Issues/PRs/commits/checks 是持久化的工程事实来源。
- 运行时是对账器/执行器，而不是新的项目授权来源。
- 使用 GitHub App installation 身份，并将仓库权限限制在试点所需的最小范围内。
- 优先使用短期 installation access token；将 App 私钥和 webhook secret 存储在文件权限受到严格限制的主机 Secret Store 中。
- 绝不得将 PAT、私钥、注册 Token、webhook secret 或模型凭据存入 Git、Issues、PR 评论、Workflow Artifact 或普通日志。
- 任何写操作之前，都必须读取当前分支保护/规则集状态。早期检查报告称 main 分支保护未启用，但当前集成访问此管理端点时收到 HTTP 403，无法独立重新核验。仓库管理员必须确认当前生效的规则集/分支保护以及必要的审查/检查规则；在记录此证据之前，自主写入模式必须保持阻止状态。

## 8. Worker隔离 / Worker isolation

试点要求：

- 为运行时配置专用的非 root Unix 服务身份；不得以 root 运行。
- 每次运行使用独立的工作目录/Worktree 和分支。
- 并发运行之间不得共享可变工作目录。
- 不提供 Docker socket、sudo、主机包管理器或不受限制的文件系统访问权限。
- 针对每种工作类别设置明确的命令/工具白名单。
- 在可行的情况下设置网络出口白名单。
- 设置资源限制：CPU、内存、磁盘、墙钟超时以及模型/API 预算。
- 不执行不可信 PR 代码或任意用户提供的 Shell 脚本。
- 仅在证据发布完成且保留策略检查通过后，清理本次运行所拥有的 Worktree。

## 9. Prompt 与 Owner 权限 / Prompt and Owner authority

每次运行都必须绑定以下信息：

- 工作项 ID 和当前 GitHub 状态快照。
- Owner 身份（A–I 逻辑角色）及已批准的 Prompt 版本。
- Prompt 文件路径、精确字节长度、仓库 Blob 字节的 SHA-256、Blob SHA 和来源 Commit SHA。
- Base branch/head SHA 和允许写入的路径。
- 风险等级、验收标准、超时和预算。
- Owner 批准证据及要求的独立审查者。

A 可以起草跨 Owner Prompt 并协调路由。但 A 不能替代领域 Owner 批准、I 的安全批准、独立审查或治理验收。A 不得同时编写并批准自己的实现 Prompt。

## 10. Run 台账与证据 / Run ledger and evidence

每次运行至少记录：

- `run_id`, `work_item_id`, `event_delivery_ids`
- `owner_id`, `worker_instance_id`, `prompt_digest`
- `base_sha`, `head_sha`, `branch`, `worktree_ref`
- `lease_id`, `fencing_token`, `started_at`, `finished_at`
- `actions_summary`, `files_changed`, `tests_invoked`, `tests_passed/failed`
- `evidence_urls`, `review_state`, `acceptance_state`
- `exit_reason`, `error_class`, `retry_count`, `budget_usage`

证据必须区分以下状态：

`DESIGNED`, `IMPLEMENTED`, `TESTED`, `REVIEWED`, `INTEGRATION_ACCEPTED`, `MERGED`, `DEPLOYED`, `RUNTIME_VERIFIED`。

Commit 或成功的单元测试不等于系统验收。定时运行不构成Worker持续健康的证明。

## 11. 存储决策仍未确定 / Storage decision remains open

详细决策记录：[ADR-RUN-001 — 持久化存储与事务边界](adr/ADR-RUN-001-durable-store-and-transaction-boundaries.md)、[ADR-RUN-002 — GitHub App、Webhook 接入与秘密管理](adr/ADR-RUN-002-github-app-webhook-security-and-secrets.md) 和 [ADR-RUN-003 — Owner Worker隔离与执行边界](adr/ADR-RUN-003-owner-worker-isolation-and-execution-boundary.md)。所有 ADR 均为 PROPOSED：它们定义约束和验收 Gate；没有任何一项授权部署或选择生产凭据。

详细决策记录：[ADR-RUN-001 — 持久化存储与事务边界](adr/ADR-RUN-001-durable-store-and-transaction-boundaries.md)。该 ADR 处于 PROPOSED 状态：定义事务不变量、候选方案比较、基准/故障矩阵和验收 Gate；不代表数据库已经选定或部署。

## 12. 故障与恢复模型 / Failure and recovery model

| 故障 / Failure | 必须行为 / Required behavior |
|---|---|
| Inbox Commit 前崩溃 | 不返回 2xx；由 GitHub 重试 / No 2xx; GitHub retries |
| Commit 后、2xx 前崩溃 | 对重复投递进行去重 / Duplicate delivery deduplicated |
| 重复投递 | 相同 delivery ID 不产生重复 Inbox 工作 / Same delivery ID no duplicate inbox work |
| 不同投递，相同目标修订版本 | 语义工作键阻止重复执行 / Semantic work key prevents duplicate execution |
| Webhook 乱序 | 重新获取 GitHub 状态；过期工作标记为 superseded / Re-fetch GitHub state; stale work superseded |
| Worker运行期间崩溃 | 租约过期；重新领取时使用新的 fencing token / Lease expires; new fencing token on reclaim |
| 过期Worker恢复 | 通过 fencing 检查拒绝其写入 / Writes rejected by fencing check |
| 队列/存储不可用 | 失败关闭；不得仅通过内存确认事件 / Fail closed; no in-memory-only acknowledgement |
| GitHub API 不可用 | 使用有界退避策略重试；不得进行过期写入 / Retry with bounded backoff; no stale write |
| 达到预算/时间限制 | 安全停止，持久化部分证据，释放或使租约过期 / Stop safely, persist partial evidence, release/expire lease |
| 紧急停止 | 禁止派发，停止Worker，必要时撤销 Token / Disable dispatch, stop workers, revoke tokens if needed |

## 13. 分阶段交付 / Staged delivery

### 阶段 0 — 治理与主机验收 / Phase 0 — Governance and host acceptance

- 仅在 PR #27 通过验收后，才进行独立审查并合并。
- 建立 main 分支保护：要求独立审查、要求 CI 检查通过、禁止强制推送、自动化身份不得直接推送。
- 运行只读诊断 Workflow，并保留运行 URL。
- 验证非 root 服务身份、systemd unit、受控重启、重启后恢复能力以及 Runner 组范围。
- 验证不可信 PR Workflow 无法使用持久化 Runner。

### 阶段 1 — 确定性的 GitHub 原生控制 / Phase 1 — Deterministic GitHub-native controls

- 定义 GitHub App 权限矩阵和事件白名单。
- 为 Webhook 信封、规范化事件、工作项和运行台账添加 Schema 验证及单元测试。
- 添加用于验证 Workflow 安全不变量的 CI。
- 此阶段尚不启用自主代码写入。

### 阶段 2 — 事件桥接与持久化 Inbox / Phase 2 — Event bridge + durable inbox

- 部署 HTTPS Receiver 和签名验证。
- 实现先持久化后 ACK，以及投递去重。
- 添加只读事件处理器和对账看门狗。
- 围绕持久化/ACK 崩溃时间窗口执行故障注入测试。

### 阶段 3 — 单 Owner 试点 / Phase 3 — Single Owner pilot

- 选择一个低风险 DOC/ARCH Owner 任务。
- 仅在隔离的 Worktree 中执行，并使用已批准的 Prompt 摘要。
- 每个 PR 都必须经过人工审查；不得自主合并。
- 验证租约/fencing、运行台账、证据发布、重启和队列恢复。

### 阶段 4 — 受控扩展至 A–I / Phase 4 — Controlled A–I expansion

- 每次增加一个 Owner。
- 每个 Owner 批准自己的 Prompt 策略以及路径/命令白名单。
- I 审查涉及安全的权限和数据处理。
- A 协调依赖关系和集成，但不能自行验收。
- 在宣称持续运行之前，必须完成持续运行测试、事件演练和回滚演练。

## 14. 验收测试矩阵 / Acceptance test matrix

| 测试 ID | 场景 / Scenario | 通过条件 / Pass condition |
|---|---|---|
| RT-01 | 无效/缺失签名 / Invalid/missing signature | 在 Inbox 持久化之前拒绝 / Rejected before inbox persistence |
| RT-02 | 持久化失败 / Persist failure | 不返回成功 ACK / No success ACK |
| RT-03 | Commit 后、ACK 前崩溃 / Crash after commit before ACK | 重试请求被去重 / Retry deduplicated |
| RT-04 | 重复 Delivery ID / Duplicate delivery ID | 仅产生一条 Inbox 记录 / One inbox record |
| RT-05 | 语义重复 / Semantic duplicate | 仅产生一个符合资格的工作项 / One eligible work item |
| RT-06 | 乱序状态 / Out-of-order state | 以当前 GitHub 状态为准 / Current GitHub state wins |
| RT-07 | 租约过期 / Lease expiry | 重新领取时递增 fencing token / Reclaim increments fencing token |
| RT-08 | 过期Worker写入 / Stale worker write | 拒绝 / Rejected |
| RT-09 | Worker进程崩溃 / Worker process crash | 持久化恢复，不丢失工作 / Durable recovery, no lost work |
| RT-10 | 存储重启/恢复 / Store restart/restore | Inbox、租约和运行台账保持一致 / Inbox, leases and run ledger consistent |
| RT-11 | 不可信 PR 隔离 / Untrusted PR isolation | 无法在持久化Worker上执行 / Cannot execute on persistent worker |
| RT-12 | 秘密扫描 / Secret scan | 仓库/日志/Artifact 中不存在秘密 / No secret in repo/log/artifact |
| RT-13 | 预算/超时 / Budget/timeout | 工作停止并记录证据 / Work stops and records evidence |
| RT-14 | 紧急停止 / Emergency stop | 不发放新租约；活动Worker安全停止 / No new lease; active workers stop safely |
| RT-15 | 对账 / Reconciliation | 找回遗漏的 Webhook 工作，且不产生重复副作用 / Missed webhook work is discovered without duplicate side effects |

## 15. 待决事项 / Open decisions

- **ADR-RUN-001:** 持久化存储选型与事务边界。
- **ADR-RUN-002:** GitHub App 权限矩阵、Webhook 接入/网络暴露及秘密存储。
- **ADR-RUN-003:** Worker隔离机制（systemd + Unix 身份，或每次运行使用独立容器/VM）。
- **ADR-RUN-004:** 事件到工作项的映射及语义幂等键。
- **ADR-RUN-005:** Owner Prompt 审批与运行时授权强制机制。
- **ADR-RUN-006:** 分支保护及必要的审查/检查规则。

在上述 ADR 获得正式批准之前，不得将候选方案描述为已经决议的架构。

## 16. 停止条件 / Stop conditions

如果出现以下任一情况，立即停止自主执行：

- Webhook 签名验证不可用或失败。
- 持久化 Inbox/租约存储不可用或失去一致性。
- 缺少分支保护或必要的独立审查。
- 无法验证 Prompt 摘要、Owner 批准或 base SHA。
- 过期Worker能够绕过租约 fencing 并发布内容。
- 不可信 PR 代码能够访问持久化 Runner 或秘密。
- 检测到秘密泄露、意外权限提升、无法解释的写入或预算失控。
- 无法持久化记录审计证据。

## 17. 状态声明 / Status statement

本文档是一份提议中的设计和分阶段试点计划。本文档不声称 Webhook Receiver、持久化队列、Coordinator、自主 Owner Worker或 24/7 服务已经部署。

本译文由 RD-F08-01（P1）驱动，对照原文 EN，语义一致性待 R1 核验。
