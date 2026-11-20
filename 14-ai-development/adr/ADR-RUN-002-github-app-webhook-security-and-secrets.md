# ADR-RUN-002 — GitHub App, Webhook Ingress and Secret Management
# ADR-RUN-002 — GitHub App、Webhook Ingress 与秘密管理

- **Status / 状态:** PROPOSED — decision pending / 提案中——待决议
- **Date / 日期:** 2026-11-17
- **Risk / 风险:** R2 for read-only pilot; R3 before autonomous repository writes / 只读试点 R2；自主仓库写入前升级为 R3
- **Decision owner / 决策责任:** A — runtime integration; I — security/governance; pilot Owner — operational acceptance / A 负责 Runtime 集成；I 负责安全治理；试点 Owner 负责运行验收
- **Related / 关联:** Issue #30; PR #31; ADR-RUN-001; AI-PROMPT-STD-001; AI-AUTO-001

---

## 1. Context / 背景

AI-RUN-003 needs to receive GitHub events, reconcile repository state, and publish bounded evidence. Authentication and authorization must be separated: a valid webhook proves that GitHub sent an event; it does not prove that the event is current, that a work item is eligible, or that a worker is authorized to mutate the repository.

AI-RUN-003 需要接收 GitHub 事件、对账仓库状态并发布有界证据。认证与授权必须分离：有效 Webhook 只能证明事件由 GitHub 发送，不能证明事件仍然最新、工作项符合执行条件或 Worker 有权修改仓库。

This ADR defines the credential and ingress model. It does not install a GitHub App, expose a webhook endpoint, create secrets, or grant repository permissions.

本 ADR 定义凭据与入口模型，不代表已安装 GitHub App、开放 Webhook Endpoint、创建秘密或授予仓库权限。

## 2. Decision drivers / 决策驱动因素

1. Least privilege and repository-level scope.
2. Short-lived credentials and revocation capability.
3. Exact raw-body signature verification and replay/dedup protection.
4. Durable-before-ACK semantics from ADR-RUN-001.
5. Separation between coordinator, publication broker and untrusted worker processes.
6. Auditable rotation, installation changes and permission changes.
7. No secrets in Git, Issues, PRs, prompts, artifacts or ordinary logs.

1. 最小权限与仓库级授权范围。
2. 短期凭据和可撤销能力。
3. 精确原始请求体签名验证及重放/去重保护。
4. 遵守 ADR-RUN-001 的先持久化后确认语义。
5. Coordinator、Publication Broker 与不可信 Worker 进程隔离。
6. 凭据轮换、Installation 变更和权限变更可审计。
7. 秘密不得进入 Git、Issue、PR、Prompt、Artifact 或普通日志。

## 3. Identity option assessment / 身份方案比较

| Option / 方案 | Advantages / 优点 | Risks / 风险 | Disposition / 结论 |
|---|---|---|---|
| GitHub App installation | Fine-grained repository permissions; short-lived installation tokens; webhook identity; revocable installation / 细粒度仓库权限、短期 Installation Token、Webhook 身份、可撤销安装 | App private key and installation lifecycle must be protected / 必须保护 App 私钥及安装生命周期 | **Preferred / 首选** |
| Fine-grained PAT | Simple for temporary manual diagnostics / 适合临时人工诊断 | User-bound lifecycle, broader persistence, weaker service identity and rotation governance / 绑定个人生命周期、长期驻留风险和服务身份治理较弱 | Not for long-running service; temporary local debugging only / 不用于长期服务，仅限临时本地调试 |
| Classic PAT | Broad compatibility / 兼容性广 | Excessive scope risk and user coupling / 权限过宽风险及个人账号耦合 | Rejected for runtime / Runtime 禁用 |
| Deploy key | Narrow repository Git transport identity / Git 传输身份可限定仓库 | Does not authorize Issues/PR/check APIs or webhook delivery / 不授权 Issue/PR/Check API，也不处理 Webhook | Optional read-only Git transport only; not control-plane identity / 仅可选只读 Git 传输，不作为控制面身份 |

**Proposed direction:** use a GitHub App installed only on `oahcom/AiMemoryBrainArchitecture` for the pilot. Do not install it across the whole organization unless a separate approved decision proves that necessary.

**提议方向：** 试点使用仅安装在 `oahcom/AiMemoryBrainArchitecture` 仓库的 GitHub App。除非另有批准决议证明必要，不得安装到整个组织。

## 4. Permission model / 权限模型

Permissions are granted only after mapping each pilot operation to the exact GitHub API endpoint. The table below is a ceiling for review, not a grant request.

只有将每项试点操作映射到精确 GitHub API Endpoint 后才授予权限。下表是审查上限，不是权限申请。

| Permission area / 权限域 | Pilot default / 试点默认 | Conditional need / 条件性需求 |
|---|---|---|
| Metadata | Read | Required for repository identity and installation context / 仓库身份和 Installation 上下文 |
| Issues | Read | Write only if broker posts comments or updates issue metadata / 仅当 Broker 需要发评论或更新 Issue 元数据时写 |
| Pull requests | Read | Write only for explicitly approved PR creation/update operations / 仅对明确批准的 PR 创建/更新操作开放写 |
| Contents | Read | Write only if broker-mediated branch/commit publication is enabled after R3 gates / 仅在 R3 Gate 后启用 Broker 代写分支/Commit |
| Checks | Read | Write only if the runtime must publish check runs / 仅当 Runtime 必须发布 Check Run 时写 |
| Commit statuses | Read | Write only if required by an accepted check integration / 仅在已批准的 Check 集成要求时写 |
| Actions | None | No workflow dispatch, runner administration or workflow mutation in pilot / 试点不开放 Workflow Dispatch、Runner 管理或 Workflow 修改 |
| Administration | None | Never required for ordinary runtime; repository admin configures rules manually / 普通 Runtime 不需要；仓库管理员手工配置规则 |
| Secrets / Variables | None | Runtime must not read repository secrets / Runtime 不得读取仓库 Secrets |
| Workflows | None | No workflow-file writes / 不写 Workflow 文件 |
| Members / Organization | None | No organization-wide enumeration or management / 不枚举或管理组织级资源 |

Additional constraints / 额外约束：

- Installation repository selection must be an explicit allowlist containing the single pilot repository.
- Runtime must verify repository ID and full name on every event and API operation; reject mismatches.
- Do not use wildcard permissions or grant write scopes “for future convenience”.
- Permission expansion requires a new work item, risk assessment, I review and installation change record.
- Worker processes receive no GitHub token. Only the trusted ingress needs webhook verification capability; only the Publication Broker receives short-lived installation tokens for mutations.
- Separate read-only reconciliation identity from publication identity if the GitHub App permission model and deployment support it; otherwise enforce API route-level capability checks inside the trusted broker.

- Installation 仓库选择必须是明确白名单，试点只包含目标仓库。
- 每次事件和 API 操作都验证 repository ID 与完整名称；不匹配即拒绝。
- 不使用通配权限，不得以“未来方便”为由授予写权限。
- 权限扩张必须有新 Work Item、风险评估、I 审查和 Installation 变更记录。
- Worker 进程不获得 GitHub Token。只有可信 Ingress 具备 Webhook 验签能力；只有 Publication Broker 获得用于变更的短期 Installation Token。
- 如果 GitHub App 权限模型和部署支持，读对账身份与写发布身份应分离；否则在可信 Broker 内实施 API 路由级能力检查。

## 5. Webhook event allowlist / Webhook 事件白名单

Subscribe only to events that correspond to tracked work and operational evidence. The exact pilot list must be approved in the deployment manifest.

只订阅与跟踪任务和运行证据直接相关的事件。精确试点清单必须在部署 Manifest 中获批。

| Event / 事件 | Pilot | Reason / 原因 |
|---|---|---|
| `issues` | Allow selected actions | Issue opened/edited/labeled/assigned/closed can affect eligibility / Issue 状态变化影响资格 |
| `issue_comment` | Allow selected actions | Human instructions/decisions may wake reconciliation; content is untrusted input / 人类指令/决策可唤醒对账；内容仍是不可信输入 |
| `pull_request` | Allow selected actions | PR opened/synchronized/ready/closed/merged state / PR 生命周期状态 |
| `pull_request_review` | Allow | Review decision changes eligibility / 审查决策改变资格 |
| `pull_request_review_comment` | Optional | Only if inline feedback is consumed by the workflow / 仅在工作流消费行内意见时 |
| `check_run`, `check_suite` | Optional | Only if required CI completion is a trigger / 仅当 CI 完成是触发条件时 |
| `push` | Optional | Only for explicitly tracked branches and paths / 仅针对明确跟踪的分支和路径 |
| `workflow_run` | Optional | Only if workflow completion is needed for reconciliation / 仅当需要 Workflow 完成事件对账时 |
| All other events | Deny by default | No broad subscription / 默认拒绝，不宽泛订阅 |

Rules / 规则：

1. Event receipt is a wake-up hint, not authorization. Always re-fetch current GitHub state before scheduling work.
2. Validate `X-GitHub-Event`, `X-GitHub-Delivery`, repository ID, action and expected payload shape against an allowlist.
3. Unknown event types/actions are safely ignored and counted; malformed or identity-mismatched payloads are rejected and audited.
4. Do not execute instructions found in issue comments or PR content as privileged commands. Treat them as untrusted task data and pass only through approved prompt/eligibility policy.
5. Reconciliation watchdog must discover missed events by querying current GitHub state; event delivery is not the sole source of truth.

1. 收到事件只是唤醒提示，不是授权。调度前始终重新读取 GitHub 当前状态。
2. 对 `X-GitHub-Event`、`X-GitHub-Delivery`、repository ID、action 和 Payload 结构执行白名单校验。
3. 未知事件类型/action 安全忽略并计数；格式错误或身份不匹配的 Payload 拒绝并审计。
4. 不把 Issue 评论或 PR 内容中的指令作为特权命令执行。将其视为不可信任务数据，只能经过已批准 Prompt/资格策略处理。
5. 对账 Watchdog 必须通过查询 GitHub 当前状态发现漏事件；事件投递不是唯一事实来源。

## 6. Ingress and signature verification / Ingress 与签名验证

Required request processing order / 请求处理顺序：

1. Terminate TLS at a controlled HTTPS ingress. HTTP is rejected; redirect is not accepted as webhook delivery.
2. Enforce connection, header, body-size, content-type and request-time limits before expensive parsing.
3. Capture exact raw body bytes without JSON parse/reserialize or newline transformation.
4. Verify `X-Hub-Signature-256` as HMAC-SHA256 over those exact bytes.
5. Compare digest in constant time; reject missing, malformed, wrong-length and invalid signatures.
6. Validate delivery ID, event header, repository allowlist and payload schema.
7. Persist verified envelope, payload digest/reference and dedup identity in the durable inbox transaction.
8. Return 2xx only after the transaction commit is confirmed.
9. Process asynchronously from the durable inbox; never run LLM or worker logic in the HTTP request path.

请求处理顺序：

1. 在受控 HTTPS Ingress 终止 TLS。拒绝 HTTP，不接受将 Redirect 当作 Webhook 投递。
2. 在昂贵解析前限制连接、Header、Body 大小、Content-Type 和请求耗时。
3. 捕获精确原始 Body 字节，不进行 JSON 解析后重序列化或换行转换。
4. 对这些精确字节验证 `X-Hub-Signature-256` HMAC-SHA256。
5. 使用恒定时间比较；拒绝缺失、格式错误、长度错误和无效签名。
6. 校验 Delivery ID、事件 Header、仓库白名单和 Payload Schema。
7. 在 Durable Inbox 事务中持久化已验证 Envelope、Payload 摘要/引用和去重身份。
8. 只有确认事务 Commit 后才返回 2xx。
9. 从 Durable Inbox 异步处理；HTTP 请求路径内不得运行 LLM 或 Worker 逻辑。

### 6.1 Reverse proxy requirements / 反向代理要求

- The TLS-terminating proxy must preserve request body bytes exactly.
- Trust forwarded client/protocol headers only from explicitly configured proxy addresses; never trust arbitrary `X-Forwarded-*` headers from the public internet.
- Limit ingress to the webhook endpoint; no administrative console on the public listener.
- Rate limiting must not silently drop valid deliveries; overload responses must be retryable and observable.
- Record TLS certificate expiry and ingress health without logging secrets or raw payloads.

- TLS 终止代理必须逐字节保留请求 Body。
- 仅信任明确配置的代理地址传来的客户端/协议转发 Header；绝不信任公网任意 `X-Forwarded-*`。
- 公网 Listener 仅开放 Webhook Endpoint，不暴露管理控制台。
- 限流不得静默丢弃有效投递；过载响应必须可重试且可观测。
- 记录 TLS 证书到期时间和 Ingress 健康状态，不记录秘密或原始 Payload。

### 6.2 Replay and deduplication / 重放与去重

GitHub delivery IDs are deduplication identities, not cryptographic nonces and not semantic work IDs. Persist each accepted delivery ID uniquely. A duplicate delivery must return a safe successful response only if the original durable record exists; if storage outcome is unknown, retry the same transaction identity and reconcile before acknowledging.

GitHub Delivery ID 是去重身份，不是密码学 Nonce，也不是语义 Work ID。每个接受的 Delivery ID 必须唯一持久化。只有原始 Durable 记录确实存在时，重复投递才可安全返回成功；若存储结果未知，必须用相同事务身份重试并完成对账后再确认。

Do not invent a time-window-only replay rule that rejects legitimate GitHub retries. Signature validity plus unique delivery persistence and current-state reconciliation are the primary controls. Apply bounded retention to dedup records based on the maximum replay/retry and audit window, and document the retention period in the deployment manifest.

不得仅凭时间窗口拒绝合法 GitHub 重试。签名有效性、Delivery 唯一持久化和当前状态对账是主要控制。根据最大重放/重试和审计窗口为去重记录设置有界保留期，并在部署 Manifest 中记录。

## 7. Secret storage and token lifecycle / 秘密存储与 Token 生命周期

### 7.1 GitHub App private key and webhook secret / App 私钥与 Webhook Secret

- Store in an external secret manager or OS-protected credential facility. For a single-host pilot, systemd credentials or a root-owned, mode-0600 file outside the repository may be evaluated; do not place secrets in unit environment variables or command-line arguments.
- The runtime service account receives read access only to the exact credential it needs. Worker identities receive none.
- Keep secrets out of shell history, process arguments, crash dumps, debug logs, metrics labels, support bundles and backups unless backups are encrypted and access-controlled under an approved retention policy.
- Load only when needed, minimize in-memory lifetime, avoid copying, and clear buffers where practical.
- Never commit secret values, even encrypted values, to the project repository.
- Document secret owner, purpose, storage location identifier (not value), creation date, rotation date, expiry/renewal method and revocation procedure.

- 存放于外部 Secret Manager 或 OS 保护的凭据设施。单机试点可评估 systemd credentials 或仓库外 root-owned、mode 0600 文件；不得放入 Unit 环境变量或命令行参数。
- Runtime 服务账号只读取自己所需的精确凭据；Worker 身份一律无权读取。
- 秘密不得进入 Shell History、进程参数、Crash Dump、Debug Log、Metrics Label、支持包或备份；若备份必须包含秘密，则须在批准的保留策略下加密并严格控权。
- 仅在需要时加载，尽量缩短内存驻留时间，避免复制，并在可行时清理缓冲区。
- 任何秘密值（包括加密值）都不得提交到项目仓库。
- 记录秘密负责人、用途、存储位置标识（不记录值）、创建日期、轮换日期、到期/续期方式和撤销流程。

### 7.2 Installation access tokens / Installation Access Token

- Mint on demand through the GitHub App API.
- Use the shortest practical token lifetime and request only the permission subset and repository subset required for the single operation.
- Keep tokens only in the trusted Publication Broker process; never pass to Owner workers, subprocess environments, worktrees, artifacts or prompts.
- Do not persist token values. Persist only non-secret metadata such as token creation time, expiry, installation ID and granted permission names.
- Refresh on expiry; fail closed if refresh is denied or installation is suspended/revoked.
- Never fall back silently to PAT or a user's personal credentials.

- 通过 GitHub App API 按需生成。
- 使用实际可行的最短 Token 生命周期，并仅请求单次操作所需权限和仓库范围。
- Token 仅保留在可信 Publication Broker 进程中；绝不传给 Owner Worker、子进程环境、Worktree、Artifact 或 Prompt。
- 不持久化 Token 值。只持久化非秘密元数据，如创建时间、到期时间、Installation ID 和授予的权限名称。
- Token 过期后刷新；若刷新被拒绝或 Installation 被暂停/撤销，则失败关闭。
- 不得静默回退到 PAT 或用户个人凭据。

### 7.3 Rotation / 轮换

Webhook secret rotation must support a controlled overlap: configure a new secret, deploy verifier support for current and previous secret identifiers, update the GitHub App webhook secret, verify successful deliveries using the new secret, then remove the previous secret. The overlap window must be short, explicitly time-bounded and audited. Do not accept an unbounded list of old secrets.

Webhook Secret 轮换必须支持受控重叠：配置新 Secret、部署同时识别当前与上一 Secret 的验证器、更新 GitHub App Webhook Secret、确认新 Secret 投递成功，再移除旧 Secret。重叠窗口必须短、有明确时限并可审计。不得接受无限增长的旧 Secret 列表。

App private-key rotation follows GitHub's supported key lifecycle: add new key, validate signing/token minting, switch active use, then revoke old key. Record each transition. The exact operational procedure must be verified against current GitHub App settings before execution.

App 私钥轮换遵循 GitHub 支持的密钥生命周期：添加新密钥、验证签名/Token 生成、切换活跃使用，再撤销旧密钥。记录每次转换。实际执行前必须根据当前 GitHub App 设置核实具体操作步骤。

## 8. Compromise and revocation playbook / 泄露与撤销预案

On suspected compromise / 怀疑泄露时：

1. Stop new work dispatch and disable publication broker writes.
2. Revoke the affected webhook secret or App private key; suspend/uninstall the App if scope is uncertain.
3. Revoke or allow short-lived installation tokens to expire, according to incident severity; do not assume private-key rotation invalidates already minted tokens.
4. Preserve sanitized audit evidence and identify affected run IDs, delivery IDs and repository mutations.
5. Rotate dependent credentials and inspect GitHub audit log, branches, commits, PRs, comments and workflow changes.
6. Reconcile repository state from GitHub and mark in-flight work SUPERSEDED or BLOCKED.
7. Restore service only after I/security review, credential verification and explicit governance approval for R3 incidents.

1. 停止新任务派发并关闭 Publication Broker 写入。
2. 撤销受影响 Webhook Secret 或 App 私钥；若影响范围不确定，暂停/卸载 App。
3. 根据事件严重程度撤销 Token 或等待短期 Token 到期；不得假定轮换私钥会自动使已生成 Token 失效。
4. 保存脱敏审计证据，识别受影响 Run ID、Delivery ID 和仓库变更。
5. 轮换关联凭据，检查 GitHub Audit Log、分支、Commit、PR、评论和 Workflow 变更。
6. 从 GitHub 对账仓库状态，将在途工作标记为 SUPERSEDED 或 BLOCKED。
7. 只有完成 I/安全审查、凭据验证以及 R3 事件明确治理批准后，才恢复服务。

## 9. Audit, telemetry and redaction / 审计、遥测与脱敏

Audit the following metadata / 以下元数据必须审计：

- App installation ID and repository ID (not credential values).
- Permission changes, installation repository selection and suspension/revocation.
- Webhook secret/key rotation version identifiers and timestamps (never values).
- Signature verification outcome, event type/action, delivery ID and payload digest.
- Token mint/expiry metadata and operation class (never token value).
- Denied API operations, rate-limit events, invalid signatures and repository identity mismatches.
- Broker authorization decision, work item, lease ID and fencing token for each mutation.

必须审计 App Installation ID、Repository ID、权限变更、仓库选择、暂停/撤销、秘密/密钥轮换版本标识和时间、验签结果、事件类型/action、Delivery ID、Payload 摘要、Token 生成/到期元数据、操作类型、拒绝操作、限流、无效签名、身份不匹配，以及每次变更的 Broker 授权决策、Work Item、Lease ID 和 fencing token。

Redaction tests must scan application logs, reverse-proxy logs, systemd journal, crash output, metrics, traces and workflow artifacts for canary secret values. Logging a digest or identifier is allowed only when it cannot be used to recover the secret.

脱敏测试必须扫描应用日志、反向代理日志、systemd Journal、Crash 输出、Metrics、Trace 和 Workflow Artifact 中的 Canary Secret 值。只有在无法据此恢复秘密时，才允许记录摘要或标识符。

## 10. Acceptance tests / 验收测试

| ID | Test / 测试 | Required result / 预期结果 |
|---|---|---|
| GH-01 | Valid signature / 有效签名 | Accepted and durably persisted / 接受并持久化 |
| GH-02 | Missing/invalid signature / 缺失或无效签名 | Rejected before persistence / 持久化前拒绝 |
| GH-03 | Body tampering / Body 篡改 | Signature fails / 签名失败 |
| GH-04 | JSON reserialization/newline mutation / JSON 重序列化或换行变化 | Signature fails against altered bytes / 对变更字节验签失败 |
| GH-05 | Current/previous secret overlap / 新旧 Secret 重叠 | Both accepted only within approved overlap / 仅在批准窗口内均可接受 |
| GH-06 | Previous secret after retirement / 旧 Secret 退役后 | Rejected / 拒绝 |
| GH-07 | Revoked secret / 已撤销 Secret | Rejected and audited / 拒绝并审计 |
| GH-08 | Oversized body / 超大 Body | Rejected before expensive parsing / 昂贵解析前拒绝 |
| GH-09 | Invalid content type / 无效 Content-Type | Rejected / 拒绝 |
| GH-10 | Duplicate delivery ID / 重复 Delivery ID | One durable inbox identity / 仅一个 Durable Inbox 身份 |
| GH-11 | Out-of-order events / 事件乱序 | Current GitHub state controls eligibility / 以 GitHub 当前状态判断资格 |
| GH-12 | Missing webhook / 漏投递 | Reconciliation discovers target / 对账发现目标 |
| GH-13 | Installation token expiry / Installation Token 过期 | Refresh or fail closed / 刷新或失败关闭 |
| GH-14 | Installation suspended/revoked / Installation 暂停或撤销 | No new token and no writes / 不生成新 Token、不写入 |
| GH-15 | Permission denied / 权限不足 | Operation fails safely; no privilege fallback / 安全失败，不回退扩大权限 |
| GH-16 | Secret log scan / 日志秘密扫描 | No canary secret in logs/artifacts / 日志和 Artifact 无 Canary Secret |
| GH-17 | Replay / 重放 | Duplicate delivery safely deduplicated; semantic work remains idempotent / 重复投递安全去重，语义工作保持幂等 |
| GH-18 | Repository mismatch / 仓库身份不匹配 | Rejected and audited / 拒绝并审计 |
| GH-19 | Proxy header spoofing / 代理 Header 伪造 | Untrusted forwarded headers ignored / 忽略不可信转发 Header |
| GH-20 | Broker token isolation / Broker Token 隔离 | Worker cannot read or exfiltrate installation token / Worker 无法读取或外泄 Installation Token |

Tests must run in CI with synthetic credentials and test installations where available. No production secret is used in test fixtures.

测试必须在 CI 中使用合成凭据和可用的测试 Installation 运行。测试夹具不得使用生产秘密。

## 11. Operational questions / 运维待决问题

The following require explicit answers before deployment:

1. Who is the named GitHub App owner/admin and who can rotate/revoke its keys?
2. What HTTPS ingress and DNS name will receive webhooks? Who owns TLS renewal?
3. Which secret store is available on the Ubuntu host, and who administers its access policy?
4. Which exact pilot operations require Issues/PR/Contents/Checks write permissions?
5. Is a separate read-only App installation feasible for reconciliation?
6. What is the approved dedup retention period and payload retention policy?
7. What is the alert path for invalid-signature spikes, failed delivery persistence, token mint failures and installation revocation?
8. Who has emergency-stop authority and how is it exercised independently of the runtime?

部署前必须明确：GitHub App 负责人/管理员及密钥轮换撤销权；Webhook HTTPS Ingress/DNS/TLS 负责人；Ubuntu Secret Store 与访问策略管理员；试点精确写权限需求；是否可拆分只读 Installation；去重和 Payload 保留期；异常告警路径；紧急停止授权人及独立于 Runtime 的停止方式。

## 12. Decision and rollout gates / 决议与上线 Gate

**Current decision: OPEN.** The preferred direction is GitHub App + repository-scoped installation + exact raw-body HMAC verification + durable inbox + short-lived installation tokens isolated to a publication broker. This remains a proposal until A, I and the selected pilot Owner review and approve their respective domains.

**当前决议：OPEN。** 首选方向为 GitHub App + 仓库级 Installation + 精确原始 Body HMAC 验签 + Durable Inbox + 仅在 Publication Broker 中使用短期 Installation Token。在 A、I 和选定试点 Owner 分别审查并批准其领域前，这仍是提案。

Gates / Gate：

- G0 — App ownership, repository scope and permission matrix approved.
- G1 — I security review approves secret storage, ingress, rotation and incident playbook.
- G2 — Raw-body verification, durable-before-ACK and dedup tests pass.
- G3 — Token isolation and broker fencing are independently tested.
- G4 — Branch protection and independent review requirements are verified by repository administrator.
- G5 — Read-only pilot accepted by its Owner.
- G6 — R3 approval before enabling any broker-mediated repository write.

- G0：App 负责人、仓库范围和权限矩阵批准。
- G1：I 安全审查批准秘密存储、Ingress、轮换和事件预案。
- G2：原始 Body 验签、先持久化后确认和去重测试通过。
- G3：Token 隔离与 Broker fencing 经独立测试。
- G4：仓库管理员核实分支保护和独立审查要求。
- G5：只读试点 Owner 验收。
- G6：启用任何 Broker 代写仓库操作前取得 R3 批准。

Until all applicable gates pass, no GitHub App/webhook deployment, autonomous repository writes, or production operation is authorized by this ADR.

在所有适用 Gate 通过前，本 ADR 不授权部署 GitHub App/Webhook、自主仓库写入或生产运行。

## 13. References / 参考

- [AI-RUN-003 Event-Driven Owner Worker Runtime](../ai-run-003-event-driven-owner-worker-runtime.en.md)
- [ADR-RUN-001 Durable Store and Transaction Boundaries](ADR-RUN-001-durable-store-and-transaction-boundaries.md)
- [AI-PROMPT-STD-001 Prompt Authoring Standard](../prompt-authoring-standard.md)
- [AI-AUTO-001 Owner Automation Operating Model](../owner-automation-operating-model.md)
- GitHub documentation: GitHub Apps, webhook events, validating webhook deliveries, and installation access tokens (verify current platform documentation at implementation time).

