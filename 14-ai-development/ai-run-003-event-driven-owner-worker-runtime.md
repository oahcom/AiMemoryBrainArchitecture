# AI-RUN-003 — Event-Driven Owner Worker Runtime Pilot
# AI-RUN-003 — 事件驱动 Owner Worker Runtime 试点架构

**Status / 状态:** PROPOSED — design baseline only / 提案中——仅设计基线  
**Risk / 风险:** R2 for read-only pilot; R3 for autonomous repository writes, secrets, or host administration / 只读试点为 R2；自主写仓库、秘密或主机管理操作为 R3  
**Owner / 责任:** A — Integration & orchestration; I — security/governance; selected pilot Owner — domain execution / A 负责集成与编排；I 负责安全治理；试点 Owner 负责领域执行  
**Tracking / 跟踪:** Issue #30; dependencies #26 and PR #27

---

## 1. Purpose / 目标

Build a durable, event-driven execution service on the user-managed Ubuntu host so that A–I Owner work can progress without keeping a ChatGPT conversation open.

在用户管理的 Ubuntu 主机上构建持久化、事件驱动的执行服务，使 A–I Owner 工作无需依赖 ChatGPT 会话持续打开也能推进。

The GitHub Actions self-hosted runner is only an execution substrate for explicitly dispatched workflows. It is **not** the event receiver, durable queue, coordinator, or autonomous Owner fleet.

GitHub Actions Self-hosted Runner 只是显式触发 Workflow 的执行底座，**不是**事件接收器、持久化队列、协调器或自主 Owner Worker 集群。

## 2. Current evidence and non-claims / 当前证据与禁止推断

| Item / 项目 | Current status / 当前状态 |
|---|---|
| Ubuntu Tailscale daemon | Operator-reported enabled/active / 操作方报告 enabled/active |
| GitHub `ai-worker` runner | Operator-confirmed Online and service started; not independently queried / 操作方确认在线且服务已启动；未独立查询 |
| Read-only diagnostics | Workflow file exists on PR #27 branch; no matching run observed / Workflow 文件存在于 PR #27 分支；未观察到匹配运行 |
| PR #27 | Ready for Review, open, not merged; formal review list empty at last query / 已可审查、开放、未合并；最近查询正式审查列表为空 |
| Main branch protection | Earlier check reported disabled; current integration cannot read this admin endpoint, so re-verification by a repository administrator is required / 早期检查报告未启用；当前集成无权读取该管理接口，必须由仓库管理员重新核验 |
| A–I worker runtime | Not deployed / 尚未部署 |

These facts do not establish reboot recovery, least-privilege isolation, durable event processing, 24/7 availability, or autonomous A–I operation.

以上事实不证明重启恢复、最小权限隔离、持久事件处理、24/7 可用性或 A–I 自主运行。

## 3. Goals and non-goals / 目标与非目标

### Goals / 目标

1. Receive authenticated GitHub events and persist them before acknowledging delivery.
2. Process events at least once while making work-item execution idempotent.
3. Reconcile missed events by periodically reading GitHub as the durable source of truth.
4. Route one bounded work item to one approved Owner prompt and isolated worker.
5. Enforce leases, fencing tokens, timeouts, budgets, backpressure, retry and dead-letter handling.
6. Produce auditable run evidence and GitHub Issue/PR updates.
7. Start with one low-risk Owner pilot; expand only after explicit gates.

1. 接收经过认证的 GitHub 事件，并在持久化后才确认投递。
2. 事件至少一次处理，工作项执行保持幂等。
3. 通过周期性读取 GitHub 进行对账，弥补事件丢失。
4. 将一个有界工作项路由给一个已批准的 Owner Prompt 和隔离 Worker。
5. 强制实施租约、fencing token、超时、预算、背压、重试和死信处理。
6. 生成可审计运行证据并更新 GitHub Issue/PR。
7. 先试点一个低风险 Owner，通过明确 Gate 后再扩展。

### Non-goals / 非目标

- No all-at-once A–I launch.
- No execution of untrusted fork/PR code on the persistent host.
- No autonomous merge, release, destructive migration, production data deletion, or permission expansion in the pilot.
- No claim of 24/7 service before measured soak and recovery evidence.
- No replacement of GitHub Issues/PRs as the engineering system of record.

- 不一次性启动 A–I 全部角色。
- 不在持久化主机执行不可信 fork/PR 代码。
- 试点阶段不允许自主合并、发布、破坏性迁移、生产数据删除或权限扩张。
- 未完成压力持续运行与恢复验证前，不宣称 24/7 服务。
- 不替代 GitHub Issue/PR 作为工程事实源。

## 4. Logical architecture / 逻辑架构

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

The webhook receiver, coordinator and worker execution are separate logical components even if the first pilot packages them as a small number of systemd services.

Webhook Receiver、Coordinator 和 Worker 执行是独立逻辑组件；即使首个试点将它们打包成少量 systemd 服务，也不得混淆职责。

## 5. Event ingestion contract / 事件接收契约

### 5.1 Authentication / 认证

- Accept HTTPS only.
- Verify `X-Hub-Signature-256` over the exact raw request body using the configured GitHub App webhook secret; use constant-time comparison.
- Reject missing, malformed or invalid signatures before persistence.
- Enforce request body size limits and content-type policy.
- Allowlist event types and repository identity; ignore all others.
- Do not log raw payloads by default; persist only required fields and a protected payload reference.

- 仅接受 HTTPS。
- 使用配置的 GitHub App Webhook Secret，对原始请求体按 `X-Hub-Signature-256` 校验；使用恒定时间比较。
- 缺失、格式错误或签名无效时，在持久化前拒绝。
- 限制请求体大小和 Content-Type。
- 对事件类型和仓库身份做白名单校验，其余忽略。
- 默认不记录原始 Payload；只持久化必要字段和受保护的 Payload 引用。

### 5.2 Durable-before-ACK / 先持久化后确认

The receiver must commit the inbox record and its deduplication key durably before returning a successful 2xx response. If durable storage is unavailable, return a retryable failure; never acknowledge an event held only in memory.

Receiver 必须先持久化 Inbox 记录及去重键，再返回成功 2xx。若持久化不可用，返回可重试失败；绝不能确认仅存在内存中的事件。

Minimum inbox fields / Inbox 最小字段：

- `delivery_id` (GitHub delivery UUID; unique)
- `repository_id`, `event_type`, `action`
- `received_at`, `payload_digest`, `payload_ref`
- `verification_result`, `processing_state`, `attempt_count`
- `correlation_id`, `last_error_class`

### 5.3 Duplicate and out-of-order events / 重复与乱序

- Delivery-level idempotency key: `github:<repository_id>:<delivery_id>`.
- Work-level idempotency key must identify the semantic work target, e.g. repository + issue/PR number + current target revision + work class + approved prompt digest.
- Different delivery IDs may represent the same semantic change; deduplicate again at work-item creation.
- Do not assume webhook order. Before execution, re-fetch the current Issue/PR/branch/check state from GitHub and evaluate eligibility against current state.
- A stale event may trigger reconciliation but must not authorize stale writes.

- 投递级幂等键：`github:<repository_id>:<delivery_id>`。
- 工作级幂等键必须标识语义工作目标，例如仓库 + Issue/PR 编号 + 当前目标修订 + 工作类型 + 已批准 Prompt 摘要。
- 不同 delivery ID 可能代表同一语义变更；创建 Work Item 时再次去重。
- 不假定 Webhook 顺序。执行前必须重新读取 GitHub 当前 Issue/PR/分支/检查状态，并据此判断资格。
- 过期事件可以触发对账，但不能授权过期写入。

## 6. Queue, leases and fencing / 队列、租约与 fencing

A work item moves through:

`DISCOVERED → ELIGIBLE → QUEUED → LEASED → RUNNING → EVIDENCE_PENDING → COMPLETED`

Exceptional states:

`BLOCKED`, `RETRY_WAIT`, `DEAD_LETTER`, `CANCELLED`, `SUPERSEDED`, `FAILED`.

A lease contains `work_item_id`, `worker_id`, `lease_expires_at`, and a monotonically increasing `fencing_token`. Every write-back operation must prove possession of the current fencing token. When a lease expires and a new worker claims the item, the fencing token increments; a stale worker cannot publish commits or completion evidence.

租约包含 `work_item_id`、`worker_id`、`lease_expires_at` 和单调递增的 `fencing_token`。每个回写操作都必须证明持有当前 fencing token。租约过期并由新 Worker 领取后，fencing token 递增；旧 Worker 不得再发布 Commit 或完成证据。

The lease authority must be durable and atomic. Process-local mutexes are insufficient. A worker must heartbeat before expiry; missed heartbeats cause lease expiry and recovery, not silent continuation.

租约权威必须持久化且原子化。仅使用进程内 Mutex 不够。Worker 必须在过期前 Heartbeat；心跳丢失后应触发租约过期和恢复，不得静默继续执行。

### 6.1 Fenced publication authority / 带 fencing 的发布权威

A fencing token is effective only if the system that performs the side effect enforces it. A worker holding a shared GitHub write token can bypass a coordinator-side lease check and push after its lease expires. Therefore, in the pilot:

- Owner workers receive no GitHub write credential.
- All GitHub mutations (branch creation, push, PR/comment/check updates) pass through a single publication broker controlled by the Coordinator.
- The broker atomically validates the current lease owner, fencing token, work-item state, allowed paths and expected base/head SHA immediately before accepting each mutation.
- The broker rejects expired, superseded or stale fencing tokens. A check performed earlier by the worker is not sufficient.
- If the broker cannot provide atomic compare-and-set enforcement, autonomous write-back remains disabled; workers may produce patch artifacts for human application only.
- Use narrowly scoped short-lived GitHub App installation tokens inside the broker; do not expose them to worker processes or their worktrees.

只有实际执行副作用的系统强制检查 fencing token，fencing 才有效。若 Worker 持有共享 GitHub 写 Token，它可以绕过 Coordinator 的租约检查，在租约过期后仍然 Push。因此试点阶段：

- Owner Worker 不获得 GitHub 写凭据。
- 所有 GitHub 变更（创建分支、Push、PR/评论/Check 更新）都经过 Coordinator 控制的单一 Publication Broker。
- Broker 在接受每次变更前，原子校验当前租约所有者、fencing token、Work Item 状态、允许路径和预期 base/head SHA。
- Broker 拒绝过期、已 superseded 或 fencing token 过期的请求。Worker 之前做过的检查不够。
- 如果 Broker 无法提供原子 compare-and-set 强制执行，则保持自主写回关闭；Worker 只能生成 Patch Artifact，由人类应用。
- 使用 Broker 内部的最小权限、短期 GitHub App Installation Token；不得暴露给 Worker 进程或其 Worktree。

## 7. GitHub authority and credentials / GitHub 权威与凭据

- GitHub Issues/PRs/commits/checks are the durable engineering source of truth.
- The runtime is a reconciler/executor, not a new source of project authorization.
- Use a GitHub App installation identity with the minimum repository permissions required for the pilot.
- Prefer short-lived installation access tokens; keep the App private key and webhook secret in a host secret store with restricted file permissions.
- Never store PATs, private keys, registration tokens, webhook secrets or model credentials in Git, Issues, PR comments, workflow artifacts or ordinary logs.
- Read current branch protection/ruleset state before any write operation. An earlier check reported main branch protection disabled, but the current integration receives HTTP 403 for this administrative endpoint and cannot independently re-verify it. A repository administrator must confirm the active ruleset/branch protection and required review/check rules; autonomous write mode remains blocked until this evidence is recorded.

- GitHub Issue/PR/Commit/Check 是持久化工程事实源。
- Runtime 是对账器和执行器，不是新的项目授权来源。
- 使用 GitHub App Installation 身份，并将仓库权限限制为试点所需最小集合。
- 优先使用短期 Installation Access Token；App 私钥和 Webhook Secret 放在权限受限的主机 Secret Store。
- PAT、私钥、注册 Token、Webhook Secret、模型凭据不得进入 Git、Issue、PR 评论、Workflow Artifact 或普通日志。
- 写操作前读取当前分支保护/Ruleset。早期检查报告 main 分支保护未启用，但当前集成访问该管理接口返回 HTTP 403，无法独立重新核验。仓库管理员必须确认生效的 Ruleset/分支保护及必要审查/检查规则；在记录该证据前，禁止自主写入模式。

## 8. Worker isolation / Worker 隔离

For the pilot:

- One dedicated non-root Unix service identity for the runtime; do not run as root.
- A separate, per-run working directory/worktree and branch.
- No shared mutable working directory between concurrent runs.
- No Docker socket, sudo, host package manager, or unrestricted filesystem access.
- Explicit command/tool allowlist per work class.
- Network egress allowlist where practical.
- Resource limits: CPU, memory, disk, wall-clock timeout and model/API budget.
- No untrusted PR code or arbitrary user-provided shell script execution.
- Cleanup only the run-owned worktree after evidence publication and retention policy checks.

试点要求：

- Runtime 使用专用非 root Unix 服务身份，不以 root 运行。
- 每次 Run 使用独立工作目录/Worktree 和分支。
- 并发 Run 不共享可变工作目录。
- 不授予 Docker Socket、sudo、主机包管理器或无限制文件系统权限。
- 按 Work Class 设置显式命令/工具白名单。
- 尽可能限制网络出口。
- 设置 CPU、内存、磁盘、墙钟超时和模型/API 预算。
- 不执行不可信 PR 代码或任意用户 Shell 脚本。
- 证据发布且保留策略检查完成后，只清理本 Run 拥有的 Worktree。

## 9. Prompt and Owner authority / Prompt 与 Owner 权限

Each run binds to:

- Work item ID and current GitHub state snapshot.
- Owner identity (A–I logical role) and approved prompt version.
- Prompt file path, exact byte length, SHA-256 of repository blob bytes, blob SHA and source commit SHA.
- Base branch/head SHA and allowed write paths.
- Risk class, acceptance criteria, timeout and budget.
- Owner approval evidence and required independent reviewers.

每次 Run 绑定：

- Work Item ID 和当前 GitHub 状态快照。
- Owner 身份（A–I 逻辑角色）及已批准 Prompt 版本。
- Prompt 文件路径、精确字节长度、仓库 Blob 字节 SHA-256、Blob SHA 和来源 Commit SHA。
- Base branch/head SHA 和允许写入路径。
- 风险等级、验收标准、超时和预算。
- Owner 批准证据及所需独立审查者。

A may draft cross-owner prompts and coordinate routing. A cannot replace domain Owner approval, I security approval, independent review, or governance acceptance. A must not author and approve its own implementation prompt.

A 可以起草跨 Owner Prompt 并协调路由，但不能替代领域 Owner 批准、I 安全批准、独立审查或治理验收。A 不得为自己的实现任务同时编写并批准 Prompt。

## 10. Run ledger and evidence / Run Ledger 与证据

Every run records at least:

- `run_id`, `work_item_id`, `event_delivery_ids`
- `owner_id`, `worker_instance_id`, `prompt_digest`
- `base_sha`, `head_sha`, `branch`, `worktree_ref`
- `lease_id`, `fencing_token`, `started_at`, `finished_at`
- `actions_summary`, `files_changed`, `tests_invoked`, `tests_passed/failed`
- `evidence_urls`, `review_state`, `acceptance_state`
- `exit_reason`, `error_class`, `retry_count`, `budget_usage`

Evidence must distinguish:
`DESIGNED`, `IMPLEMENTED`, `TESTED`, `REVIEWED`, `INTEGRATION_ACCEPTED`, `MERGED`, `DEPLOYED`, `RUNTIME_VERIFIED`.

A commit or successful unit test is not system acceptance. A scheduled run is not proof of a continuously healthy worker.

证据必须区分上述状态。Commit 或单元测试成功不等于系统验收；定时 Run 不等于 Worker 持续健康的证明。

## 11. Storage decision remains open / 存储选型仍开放

Detailed decision records: [ADR-RUN-001 — Durable Store and Transaction Boundaries](adr/ADR-RUN-001-durable-store-and-transaction-boundaries.md) and [ADR-RUN-002 — GitHub App, Webhook Ingress and Secret Management](adr/ADR-RUN-002-github-app-webhook-security-and-secrets.md) and [ADR-RUN-003 — Owner Worker Isolation and Execution Boundary](adr/ADR-RUN-003-owner-worker-isolation-and-execution-boundary.md). All ADRs are PROPOSED: they define constraints and acceptance gates; none authorizes deployment or selects production credentials.

详细决策记录：[ADR-RUN-001 — 持久化存储与事务边界](adr/ADR-RUN-001-durable-store-and-transaction-boundaries.md)。该 ADR 处于 PROPOSED：定义事务不变量、候选方案比较、基准/故障矩阵和验收 Gate；不代表已选择或部署数据库。


## 12. Failure and recovery model / 故障与恢复模型

| Failure / 故障 | Required behavior / 必须行为 |
|---|---|
| Crash before inbox commit | No 2xx; GitHub retries / 不返回 2xx，由 GitHub 重试 |
| Crash after commit before 2xx | Duplicate delivery deduplicated / 重复投递去重 |
| Duplicate delivery | Same delivery ID no duplicate inbox work / 同 Delivery ID 不重复入队 |
| Distinct deliveries, same target revision | Semantic work key prevents duplicate execution / 语义工作键阻止重复执行 |
| Out-of-order webhook | Re-fetch GitHub state; stale work superseded / 重读 GitHub 状态，过期工作 superseded |
| Worker crash during run | Lease expires; new fencing token on reclaim / 租约过期，重新领取时生成新 fencing token |
| Stale worker resumes | Writes rejected by fencing check / 通过 fencing 检查拒绝旧 Worker 写入 |
| Queue/store unavailable | Fail closed; no in-memory-only acknowledgement / 失败关闭，不确认仅在内存中的事件 |
| GitHub API unavailable | Retry with bounded backoff; no stale write / 有界退避重试，不做过期写入 |
| Budget/time limit reached | Stop safely, persist partial evidence, release/expire lease / 安全停止，保存部分证据，释放或过期租约 |
| Emergency stop | Disable dispatch, stop workers, revoke tokens if needed / 禁止派发、停止 Worker，必要时撤销 Token |

## 13. Staged delivery / 分阶段交付

### Phase 0 — Governance and host acceptance / 治理与主机验收

- Independently review and merge PR #27 only after acceptance.
- Establish main branch protection: required independent review, required CI checks, no force-push, no direct pushes for automation identities.
- Run the read-only diagnostic workflow and preserve run URL.
- Verify non-root service identity, systemd unit, controlled restart, reboot recovery and runner group scope.
- Verify untrusted PR workflows cannot target the persistent runner.

### Phase 1 — Deterministic GitHub-native controls / GitHub 原生确定性控制

- Define GitHub App permission matrix and event allowlist.
- Add schema validation and unit tests for webhook envelope, normalized event, work item and run ledger.
- Add CI that validates workflow safety invariants.
- Do not yet enable autonomous code-writing.

### Phase 2 — Event bridge + durable inbox / 事件桥接与持久 Inbox

- Deploy HTTPS receiver and signature verification.
- Persist before ACK; implement delivery deduplication.
- Add a read-only event processor and reconciliation watchdog.
- Run fault-injection tests around persist/ACK crash windows.

### Phase 3 — Single Owner pilot / 单 Owner 试点

- Select a low-risk DOC/ARCH Owner task.
- Execute only in isolated worktree with approved prompt digest.
- Require human review for every PR; no autonomous merge.
- Verify lease/fencing, run ledger, evidence publishing, restart and queue recovery.

### Phase 4 — Controlled A–I expansion / 受控扩展到 A–I

- Add one Owner at a time.
- Each Owner approves its prompt policy and path/command allowlist.
- I reviews security-sensitive permissions and data handling.
- A coordinates dependencies and integration but cannot self-accept.
- Conduct soak testing, incident drills and rollback rehearsal before continuous-operation claim.

## 14. Acceptance test matrix / 验收测试矩阵

| Test ID | Scenario / 场景 | Pass condition / 通过条件 |
|---|---|---|
| RT-01 | Invalid/missing signature / 无效或缺失签名 | Rejected before inbox persistence / 持久化前拒绝 |
| RT-02 | Persist failure / 持久化失败 | No success ACK / 不返回成功 ACK |
| RT-03 | Crash after commit before ACK / Commit 后 ACK 前崩溃 | Retry deduplicated / 重试去重 |
| RT-04 | Duplicate delivery ID / 重复 Delivery ID | One inbox record / 仅一条 Inbox 记录 |
| RT-05 | Semantic duplicate / 语义重复 | One eligible work item / 仅一个合格 Work Item |
| RT-06 | Out-of-order state / 乱序状态 | Current GitHub state wins / 以当前 GitHub 状态为准 |
| RT-07 | Lease expiry / 租约过期 | Reclaim increments fencing token / 重新领取递增 fencing token |
| RT-08 | Stale worker write / 旧 Worker 写入 | Rejected / 拒绝 |
| RT-09 | Worker process crash / Worker 进程崩溃 | Durable recovery, no lost work / 持久恢复，不丢任务 |
| RT-10 | Store restart/restore / 存储重启恢复 | Inbox, leases and run ledger consistent / 数据一致 |
| RT-11 | Untrusted PR isolation / 不可信 PR 隔离 | Cannot execute on persistent worker / 无法在持久 Worker 执行 |
| RT-12 | Secret scan / 秘密扫描 | No secret in repo/log/artifact / 仓库、日志、Artifact 无秘密 |
| RT-13 | Budget/timeout / 预算与超时 | Work stops and records evidence / 停止并记录证据 |
| RT-14 | Emergency stop / 紧急停止 | No new lease; active workers stop safely / 不发新租约，活动 Worker 安全停止 |
| RT-15 | Reconciliation / 对账 | Missed webhook work is discovered without duplicate side effects / 找回漏事件且无重复副作用 |

## 15. Open decisions / 待决事项

- **ADR-RUN-001:** Durable store selection and transaction boundaries.
- **ADR-RUN-002:** GitHub App permission matrix, webhook ingress/network exposure and secret storage.
- **ADR-RUN-003:** Worker isolation mechanism (systemd + Unix identities vs per-run containers/VMs).
- **ADR-RUN-004:** Event-to-work-item mapping and semantic idempotency keys.
- **ADR-RUN-005:** Owner prompt approval and runtime authorization enforcement.
- **ADR-RUN-006:** Branch protection and required review/check rules.

以上 ADR 未获正式批准前，不得将候选方案描述为已决议架构。

## 16. Stop conditions / 停止条件

Stop autonomous execution immediately if any of the following occurs:

- Webhook signature verification is unavailable or fails.
- Durable inbox/lease store is unavailable or loses consistency.
- Branch protection or required independent review is missing.
- Prompt digest, Owner approval or base SHA cannot be verified.
- A stale worker can publish after lease fencing.
- Untrusted PR code can access the persistent runner or secrets.
- Secret exposure, unexpected privilege escalation, unexplained write, or budget runaway is detected.
- Audit evidence cannot be durably recorded.

出现以下任一情况，立即停止自主执行：Webhook 签名验证不可用或失败；Inbox/租约存储不可用或不一致；缺少分支保护或独立审查；Prompt 摘要、Owner 批准或 Base SHA 无法验证；旧 Worker 能越过 fencing 发布；不可信 PR 可访问持久 Runner 或秘密；发生秘密泄露、权限提升、未解释写入或预算失控；审计证据无法持久化。

## 17. Status statement / 状态声明

This document is a proposed design and staged pilot plan. No webhook receiver, durable queue, coordinator, autonomous Owner worker, or 24/7 service is claimed deployed by this document.

本文是提议中的设计和分阶段试点计划。本文件不声称 Webhook Receiver、持久化队列、Coordinator、自主 Owner Worker 或 24/7 服务已经部署。
