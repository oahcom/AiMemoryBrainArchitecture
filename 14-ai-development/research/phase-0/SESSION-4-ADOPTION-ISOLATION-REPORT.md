# AI-DEV-OS-001 — SESSION 4
# Product Adoption, Platform Reality & Architecture Isolation
# 产品采用、平台现实与架构隔离专项研究报告

## 1. Document Metadata / 文档元数据

| Field | Value |
|---|---|
| Repository | `oahcom/AiMemoryBrainArchitecture` |
| Program / Phase | AI-DEV-OS-001 / Phase 0 — Research |
| Session / Owner | Session 4 — Product Adoption, Platform Reality & Architecture Isolation |
| Report status | Research findings and recommendations; not an architecture approval |
| Evidence refresh | 2026-11-18 (UTC+08:00) |
| Repository baseline | `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa` |
| Language | English and Chinese; both languages contain substantive findings |
| Scope | Read-only research; publication does not authorize Phase 1 implementation |

**Status vocabulary:** VERIFIED means directly checked against current repository data or official product documentation; PROPOSED means a recommendation, not an approved decision; UNKNOWN means the relevant state could not be independently verified; NOT APPLICABLE means outside this report's scope.

**证据状态：** VERIFIED 表示已通过当前仓库数据或官方产品文档直接核验；PROPOSED 表示研究建议，不代表已批准；UNKNOWN 表示尚无法独立核实；NOT APPLICABLE 表示不适用。本报告不是架构批准、部署授权或工程实施授权。

---

## 2. Executive Summary / 执行摘要

### 2.1 Principal finding / 核心结论

**PROPOSED — Phase 1 should start with a human-initiated ordinary ChatGPT conversation, GitHub Issues/branches/commits/PRs as durable evidence, and optional developer-controlled local coding tools. A custom durable AI Worker Runtime is not justified for the Phase 1 MVP.**

**建议：Phase 1 采用“人工启动普通 ChatGPT 对话 + GitHub 持久化任务与证据 + 可选的开发者本地编码工具”。当前没有足够的业务需求证明必须部署自建 Durable AI Worker Runtime。**

The product and repository evidence supports a low-infrastructure workflow. Ordinary ChatGPT is a user-triggered reasoning and coordination surface, not an always-on daemon. GitHub provides durable task/change/review history. Local coding execution can remain under the developer's control. Deterministic CI may be added separately after workflow and security review; no AI system should receive business architecture approval authority merely because it can edit files or publish evidence.

产品和仓库证据支持低基础设施成本的工作方式。普通 ChatGPT 是用户触发的推理与协调界面，不是持续运行的守护进程；GitHub 提供持久化任务、变更和审查历史；代码执行可以留在开发者控制的本地环境。确定性 CI 可在工作流和安全审查后单独引入。任何 AI 系统都不能因为具备文件修改或证据发布能力而获得业务架构批准权。

### 2.2 Key decisions / 关键判断

1. **Conversation-first — PROPOSED:** sufficient for bounded, user-triggered Phase 1 tasks, but not unattended execution.
2. **GitHub as durable evidence — VERIFIED capability / PROPOSED usage:** Issues, branches, commits and PRs provide traceability; a PR is not itself business acceptance.
3. **Codex — VERIFIED capability / PROPOSED optional adapter:** local Codex may assist code edits and tests, subject to user-controlled scope; it is not a governance system or independent reviewer.
4. **Work and event triggers — VERIFIED product features with eligibility limits:** do not assume access on every plan or workspace.
5. **Durable Worker Runtime — PROPOSED defer:** queue, webhook, database, worker isolation, credentials, monitoring and on-call ownership add cost and risk without a demonstrated Phase 1 requirement.
6. **Three-layer isolation — PROPOSED:** business architecture, engineering process and external infrastructure must remain separately governed.
7. **Security — PROPOSED:** default to read-only retrieval, explicit human-authorized writes, least privilege, exact-SHA review and no privileged execution of untrusted PR content.

### 2.3 Critical limitations / 关键限制

- Current repository baseline is `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`.
- PR #42, #23 and #27 are proposals on separate, divergent heads, not merged normative decisions.
- The ChatGPT GitHub connection described by OpenAI is read-only; do not confuse it with other GitHub-capable tools or Codex workflows.
- The current account context is Free. Work and Work-based GitHub event triggers must not be assumed available; Codex local availability and usage limits are distinct from Codex Cloud.
- Branch protection and ruleset enforcement were not independently verified because the authorized GitHub read returned 403. CI must not be described as passing or configured based on absent status contexts.

---

## 3. Research Scope / 研究范围

### 3.1 Included / 包含范围

This research evaluates the practical adoption boundary among:
- ordinary ChatGPT conversation;
- ChatGPT Work and connected-app workflows;
- ChatGPT GitHub connection;
- Codex local and Codex Cloud;
- ChatGPT Scheduled Tasks and Work event-triggered tasks;
- GitHub Issues, pull requests, branches, commits and Actions;
- API-based agents and durable background workers;
- self-hosted runners and the operational/security implications of persistent execution.

本研究比较普通 ChatGPT 对话、ChatGPT Work、GitHub 连接、Codex 本地与云端能力、Scheduled Tasks、GitHub Issues/PR/Actions、API Agent、持久化 Worker 和自托管 Runner 的实际边界。

### 3.2 Exclusions / 不包含范围

No architecture implementation, code changes, workflow creation, GitHub App installation, webhook receiver, API key, database, queue, runner deployment, secret provisioning, production test or business-domain redesign is authorized or claimed. This report does not approve or merge any existing PR.

本报告不实施架构、不修改代码、不创建 Actions、不安装 GitHub App、不部署 Webhook/Worker/数据库/队列/Runner、不创建 API Key 或 Secret，也不进行业务领域重构。报告不批准、不合并任何现有 PR。

### 3.3 Method / 方法

The study refreshed the live repository baseline and inspected current main-branch files, PR metadata and selected source blobs. Official OpenAI and GitHub documentation was used for product and security claims. PR descriptions were treated as claims to investigate, not independent review evidence. Historical review results were not treated as review of a later PR head.

研究先刷新 GitHub 实时基线，再读取 main 文件、PR 元数据和指定源文件 Blob；产品与安全能力以 OpenAI/GitHub 官方文档为依据。PR 描述仅作为待核查线索，不能替代独立审查；历史 Review 不能代表后续 Head SHA 的审查结果。

---

## 4. Current State / 当前状态

### 4.1 Repository baseline / 仓库基线

**VERIFIED:** repository `oahcom/AiMemoryBrainArchitecture` is private and uses `main` as its default branch. The refreshed main HEAD is `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.

Key current-main source files:
- `00-governance/architecture-invariants.md` — Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe`.
- `14-ai-development/README.md` — Blob `9593fd66f2b830748d826d754ce3e6da00e6f144`.
- `14-ai-development/ai-development-standard.md` — Blob `f46867f97fc1860015adbe2a1f7b8262640c16fd`.
- `14-ai-development/iteration-lifecycle.md` — Blob `8ecc8e4ddde78be01e2038be4ece8dc8ac282c97`.
- `14-ai-development/prompt-and-evidence-template.md` — Blob `c9c545ae884991d2f5dd08c6880c50c97a13c143`.
- `13-engineering-decisions/technology-architecture-blueprint.md` — Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`.

**VERIFIED:** the current main tree did not contain a `.github/` directory; the Contents API lookup returned 404. The inspected combined-status responses returned no status contexts for the reviewed main/PR heads. This means no CI execution or successful check is evidenced by those observations; it is not proof that no external validation ever occurred.

**UNKNOWN:** branch protection and repository rulesets. The read interface returned 403 for both classes of settings, so an authorized repository administrator must provide current configuration evidence.

### 4.2 Related proposals / 相关提案

| Item | Live revision and state | Evidence and interpretation |
|---|---|---|
| PR #42 — ChatGPT-native execution model | Head `84d91b10e9069a575b479f6925d3b143757e82cb`; OPEN / DRAFT; 106 ahead / 34 behind main at refresh | Direct source file Blob `9136e131e1166d9ba17d993efb5312d1d7d26121` was read. Proposal is not merged or approved. |
| PR #23 — AI development governance / runtime | Head `b6b9d2662729fdf2c112ae689cda34e235fdc82f`; OPEN; 22 ahead / 52 behind | AI-RUN-001 Blob `675d667eebd2a0d8c3d79ec502f903725db9788e` and AI-AUTO-001 Blob `c406d8c5b32977e8510b016ee71f9693d35ce821` were read; both are proposals. |
| PR #27 — persistent Ubuntu worker endpoint | Head `6c70b2fadf39220b31824c3f32114e4e65b617f4`; OPEN; 8 ahead / 51 behind | Current live head differs from a historical SHA quoted in its PR body. Treat body snapshots as potentially stale. |
| Issue #24 — GitHub-mediated Owner workflow | OPEN; updated 2026-11-17 | Separates periodic scheduled tasks from uninterrupted event-driven runtime. |
| Issue #26 — persistent Ubuntu worker runtime | OPEN; updated 2026-11-17 | Defines runner pilot acceptance topics; does not prove a complete A–I fleet exists. |

The PRs above have diverged histories relative to the refreshed main. Their existence does not constitute approval, deployment or current-head independent review. A mergeable flag, if present, is not equivalent to approval or policy compliance.

上述 PR 相对于刷新后的 main 存在分叉。PR 的存在不代表批准、部署或对当前 Head 的独立审查。即使 GitHub 返回 mergeable，也不等同于审查批准或治理合规。

---

## 5. Existing Capabilities / 已有能力

### 5.1 Product capability matrix / 产品能力矩阵

| Capability | Verified reality | Limitations and adoption consequence |
|---|---|---|
| Ordinary ChatGPT | Interactive user-started reasoning and coordination. | Not an always-on worker; requires user initiation and supervision. |
| ChatGPT Work | Supports longer multi-step work, connected apps/files and deliverables. | Plan, workspace and rollout dependent; not a universal baseline. |
| ChatGPT GitHub connection | Retrieves permitted repository content on demand. | OpenAI documents this connection as read-only; do not assume push, issue mutation or PR creation. |
| Codex local | Coding agent for local repository work, edits and tests. | Requires local setup and user-controlled environment; plan usage limits apply. |
| Codex Cloud | Isolated cloud coding environments and managed tasks. | Not included with Free/Go according to the plan documentation; not a baseline dependency here. |
| Scheduled Tasks | One-time and recurring tasks exist. | Free plan limits include up to three active tasks and recurrence no more than daily; flexible execution windows. |
| Work GitHub event triggers | Eligible Work surfaces can react to supported GitHub PR activity. | Paid-plan/workspace eligibility applies; not available as a Free/Go assumption and not a general arbitrary webhook service. |
| GitHub Issues / PRs | Durable task discussion, source changes, commit history and review records. | Repository permissions and policy apply; PR approval is not automatically business acceptance. |
| GitHub Actions | Event-driven deterministic workflows and checks. | Requires reviewed workflow files, permissions and runner configuration; untrusted PR content is a security boundary. |
| API agents | Technically possible with API credentials and external compute. | Separate API billing from ChatGPT subscription; introduces key, runtime and operational responsibilities. |
| Durable worker | Can provide webhook-driven background execution if implemented. | Requires durable queue/inbox, identity, authorization, leases, recovery, monitoring, operator ownership and security controls. |

### 5.2 Account and product implications / 套餐与产品影响

The current account context is Free. Therefore ordinary conversation is the dependable baseline; Work and Work-based event triggers must not be assumed; Codex local and Codex Cloud must be distinguished; and ChatGPT subscription billing must not be confused with API billing.

当前账户上下文为 Free，因此普通对话是可靠基线；不能假设可使用 Work 或 Work 事件触发；必须区分 Codex 本地与 Codex Cloud；ChatGPT 订阅也不包含 API 平台账单。

### 5.3 GitHub capabilities / GitHub 能力

GitHub can persist Issues, branches, commits, PRs, comments and review records. GitHub Actions can run deterministic validation when workflows are explicitly added and governed. GitHub Apps can be scoped more narrowly than broad personal tokens and can use short-lived installation tokens. None of these mechanisms inherently grants domain decision authority.

GitHub 可以持久化 Issue、分支、提交、PR、评论和 Review；Actions 在显式配置并经过治理后可以运行确定性验证；GitHub App 可比宽权限个人 Token 更精细地限制范围，并使用短期 Installation Token。但这些机制本身都不会获得业务决策权。

---

## 6. Missing Capabilities and Gaps / 缺失能力与差距

1. **No proven always-on conversation runtime — VERIFIED gap:** ordinary ChatGPT interaction is user-driven. Scheduled Tasks do not equal continuous event processing.
2. **No universal write-capable GitHub connector — VERIFIED product limitation:** the official ChatGPT GitHub connection is documented as read-only. Write paths must be explicitly identified and separately authorized.
3. **No current-main CI evidence — VERIFIED observation:** no `.github/` directory was found on the refreshed main tree and no status contexts were returned for inspected heads.
4. **Branch enforcement unknown — UNKNOWN:** current rules/protection settings were not readable through the authorized integration.
5. **No evidence of deployed complete A–I worker fleet — UNKNOWN / NOT EVIDENCED:** open PRs/issues are proposals and pilot discussions, not proof of production services.
6. **Governance approval status needs care — VERIFIED source state:** current AI development documents describe proposed process; their presence must not be misrepresented as formal approval.
7. **Prompt and evidence friction — PROPOSED risk:** mandatory repository-stored prompt rules can be expensive for low-risk work; any tiering change requires Session 0 governance decision.
8. **Independent review semantics — OPEN:** separate ChatGPT conversations may improve context separation but do not by themselves prove provider, personnel or statistical independence.

1. **缺少已证明的持续对话运行时：** 普通 ChatGPT 由用户触发，Scheduled Tasks 不等于持续事件处理。
2. **缺少通用写入型 GitHub Connector：** 官方 ChatGPT GitHub 连接为只读，写入路径必须单独识别和授权。
3. **当前 main 无 CI 证据：** 未发现 `.github/`，检查的提交也没有返回 status contexts。
4. **分支保护未知：** 授权接口无法读取当前 rules/protection。
5. **没有完整 A–I Worker Fleet 部署证据：** 开放 PR/Issue 是提案或试点讨论，不是生产服务证明。
6. **治理批准状态需谨慎：** 当前 AI 开发文档标记为 proposed，不能误称正式批准。
7. **Prompt 与证据流程摩擦：** 低风险任务也强制存档可能增加成本；是否分级须由 Session 0 决定。
8. **独立审查语义仍待明确：** 不同 ChatGPT 会话并不自动证明人员、供应商或统计独立性。

---

## 7. Proposed Architecture and Isolation / 建议架构与隔离

### 7.1 Three-layer model / 三层模型

| Layer | Responsibility | Authority boundary |
|---|---|---|
| **Layer A — Business Architecture** | A–I Owners, Memory Brain, Compiler, Runtime, BMCP and canonical business/domain contracts. | Business semantics and architecture decisions remain with designated Owners and project governance. |
| **Layer B — Engineering Operating System** | Work Items, Prompts, Runs, Evidence, Reviews, Acceptance records and development workflow. | May read Layer A specifications and coordinate engineering work; cannot approve or redefine Layer A. |
| **Layer C — External Infrastructure** | GitHub, Actions, Codex, databases, queues, model APIs, runners and agent tools. | Supplies execution/storage capabilities only; cannot bypass Layer A governance or create business authority. |

**PROPOSED isolation rules:**
- Layer A must remain independently understandable, buildable and evolvable without AI-DEV-OS.
- Layer B may reference Layer A contracts but must not become a runtime dependency of the business architecture.
- Layer C is replaceable infrastructure; no vendor, model or agent framework is canonical by default.
- Work Item, Prompt, Run, Agent, Worker, Coordinator, Lease, Retry, Evidence Bundle and CI Run are engineering-process concepts unless a relevant Owner explicitly approves a domain mapping.
- A Prompt is not automatically Memory; a Run is not automatically a business Event; a Worker Lease is not automatically a domain lock.
- Removing AI-DEV-OS must not prevent Layer A from operating or evolving.

**建议隔离规则：**
- 删除 AI-DEV-OS 后，Layer A 仍须可独立理解、构建和演进。
- Layer B 可以引用 Layer A 合同，但不能成为业务架构运行时依赖。
- Layer C 是可替换基础设施，任何厂商、模型或 Agent 框架默认都不是 Canonical。
- Work Item、Prompt、Run、Agent、Worker、Coordinator、Lease、Retry、Evidence Bundle、CI Run 属于工程流程概念，除非相应 Owner 明确批准领域映射。
- Prompt 不自动等于 Memory；Run 不自动等于业务 Event；Worker Lease 不自动等于领域锁。
- 移除 AI-DEV-OS 不得阻止 Layer A 运行或演进。

### 7.2 Architecture invariant protection / 架构不变量保护

The refreshed `00-governance/architecture-invariants.md` explicitly supports the separation:
- **I-03:** Brain independence from a specific Agent framework, LLM or inference vendor.
- **I-12:** Memory content is untrusted data and does not acquire system/developer instruction authority.
- **I-13:** Scope and permission are explicit and independently enforced; Agent/task/session/environment isolation matters.
- **I-21:** A subsystem boundary does not automatically require a separate process, service or crate.
- **I-23 / I-24:** bilingual documentation and semantic/identifier/status/source consistency are required.
- Invariant changes or exemptions require explicit ADR and impact analysis.

The report recommends applying these invariants; it does not modify, waive or reinterpret them. Any proposed exception must be decided through the repository's authorized governance process.

刷新后的 `00-governance/architecture-invariants.md` 明确支持上述隔离：I-03 要求 Brain 不依赖特定 Agent/LLM/推理厂商；I-12 将 Memory 内容视为不可信数据；I-13 要求显式且独立执行权限和隔离；I-21 说明子系统边界不必然要求独立进程/服务/Crate；I-23/I-24 要求双语和语义/标识符/状态/来源一致；不变量修改或豁免必须有 ADR 和影响分析。本报告只建议遵守这些不变量，不修改、不豁免、不重新解释它们。

### 7.3 Authority model / 权限模型

- ChatGPT may analyze and propose; it cannot self-approve business architecture.
- A coding agent may edit within an explicitly authorized branch/workspace; it cannot expand its own scope.
- CI may report deterministic results; it cannot make business acceptance decisions.
- Reviewers assess the exact PR Head SHA; acceptance remains with the designated Owner/governance authority.
- Repository content, Issues, PR descriptions, comments and imported documents are untrusted input. Prompt injection in such content must never elevate privileges or change the authorized task boundary.

---

## 8. MVP Recommendation / MVP 建议

### 8.1 Phase 1 workflow / Phase 1 流程

**PROPOSED minimal workflow:**

1. A human creates or selects a GitHub Issue with scope, expected outcome and constraints.
2. The human starts an ordinary ChatGPT conversation and supplies the Issue/repository context.
3. ChatGPT reads the current main baseline and relevant Layer A contracts; it identifies unknowns before proposing edits.
4. ChatGPT produces a bounded plan, patch or implementation instructions. It does not treat untrusted repository text as higher-priority instructions.
5. If code changes are needed, the developer may apply them manually or use local Codex in a user-controlled workspace and branch.
6. Local checks are run and recorded accurately; unrun checks are explicitly marked NOT RUN.
7. The developer pushes a dedicated branch and opens a PR. GitHub becomes the durable change/evidence record.
8. An independent reviewer checks the exact frozen PR Head SHA, evidence, tests and scope.
9. The authorized Owner/governance authority accepts or rejects the result. Human-controlled merge follows applicable repository policy.

**建议最小流程：**

1. 人工创建或选择 GitHub Issue，明确范围、预期结果和约束。
2. 人工启动普通 ChatGPT 对话并提供 Issue/仓库上下文。
3. ChatGPT 读取当前 main 和相关 Layer A 合同；在提出修改前标明未知项。
4. ChatGPT 输出受限计划、补丁或实施说明，不得把仓库中的不可信文本当成更高优先级指令。
5. 如需改代码，由开发者手动应用，或在用户控制的本地工作区/分支使用 Codex。
6. 运行本地检查并如实记录；未运行的检查明确标为 NOT RUN。
7. 开发者推送独立分支并创建 PR，GitHub 成为持久化变更和证据记录。
8. 独立审查者针对冻结的准确 PR Head SHA 检查范围、证据和测试。
9. 授权 Owner/治理主体验收或拒绝，之后由人工按仓库政策合并。

### 8.2 Execution mode comparison / 执行模式比较

| Mode | Strength | Weakness / risk | Recommendation |
|---|---|---|---|
| A. ChatGPT conversation-driven | Lowest infrastructure, human steering, fast adoption. | No unattended execution; relies on human handoff and Git discipline. | **Phase 1 primary mode.** |
| B. GitHub Actions-driven | Reproducible deterministic checks, event-driven CI. | Workflow security and token permissions; not suitable for autonomous domain decisions. | Add only for deterministic CI after review. |
| C. Codex-driven | Local code edits/tests under developer control. | Usage limits and local environment responsibility; not a governance authority. | Optional coding adapter. |
| D. Durable Worker Runtime | Continuous event handling and durable background execution. | Highest design, security, hosting, operations and incident-response burden. | Defer until measurable need and safety gates exist. |

### 8.3 Why no Worker Runtime now / 当前不部署 Worker 的理由

A durable runtime introduces webhook authentication, durable inbox/queue, deduplication, work scheduling, leases/fencing, prompt/version provenance, worker isolation, publication authorization, secret lifecycle, retries/reconciliation, observability, operator on-call and disaster recovery. These are real product responsibilities, not free extensions of ChatGPT.

只有当事件量、延迟目标、人工成本或可用性要求证明人工触发模式无法满足需求时，才应重新评估 Worker。重新评估前必须明确运维 Owner、威胁模型、安全评审、预算上限、Kill Switch、审计、恢复模型和低风险试点。持久化 Runner 不得执行不可信 PR 代码。

---

## 9. Phase 1 Acceptance Criteria / Phase 1 验收标准

Phase 1 should not be declared accepted until all applicable criteria below are demonstrated with evidence.

### Product and adoption / 产品与采用
- [ ] A user can start and complete a bounded task without deploying a new service, database, queue or API worker.
- [ ] The workflow distinguishes read-only ChatGPT GitHub retrieval from write-capable local Git/Codex actions.
- [ ] Work, event triggers and Codex Cloud are optional and never assumed without account-level verification.
- [ ] A task can be resumed from durable Issue, branch, commit, PR and evidence references rather than relying solely on chat history.

### Architecture isolation / 架构隔离
- [ ] Layer A has no required import, runtime dependency or operational dependency on Layer B or Layer C.
- [ ] Layer B metadata is not silently promoted into canonical business/domain entities.
- [ ] No Agent/Worker/Coordinator gains Layer A approval authority.
- [ ] Invariant changes or exceptions follow explicit ADR and impact analysis.

### Security and permissions / 安全与权限
- [ ] Repository access is scoped to the minimum necessary repositories and permissions.
- [ ] No AI identity receives administration, workflow/secrets, merge, release or deployment authority by default.
- [ ] Issue/PR/repository content is treated as untrusted data; prompt injection cannot change authorization or scope.
- [ ] Branch protection and required review settings are verified by an authorized administrator and recorded.
- [ ] Untrusted PR code is never executed in a privileged persistent self-hosted runner.

### Engineering evidence / 工程证据
- [ ] Each substantive task has an approved work-item/prompt/evidence record appropriate to its risk tier.
- [ ] Every change is on a dedicated branch and PR with exact base and head SHAs.
- [ ] Deterministic checks are run and linked; unrun checks are marked NOT RUN.
- [ ] Independent review targets the exact PR Head SHA, not an earlier revision.
- [ ] Business Owner/governance acceptance is explicit and distinct from technical review.
- [ ] Removing AI-DEV-OS does not impair Layer A.

### CI / 持续集成
Current main has no observed `.github/` directory and no status contexts were returned for the inspected heads. Automated CI is therefore **NOT EVIDENCED** at this baseline. Phase 1 may use reproducible local checks, but CI must not be claimed until a reviewed workflow is merged and an actual successful run is linked.

当前 main 未观察到 `.github/` 目录，检查的 Head 也未返回 status contexts，因此当前基线的自动 CI 为 **NOT EVIDENCED**。Phase 1 可以使用可复现的本地检查，但只有在工作流经过审查、合并并有真实成功运行记录后，才能宣称 CI 已通过。

---

## 10. Risks and Conflicts / 风险与冲突

| ID | Risk / conflict | Evidence and status | Required decision / action |
|---|---|---|---|
| C-01 | PR #42's ChatGPT-native claims vs official read-only GitHub connection docs. | PR #42 live head `84d91b10e9069a575b479f6925d3b143757e82cb`; official OpenAI docs describe GitHub connection as read-only. | Session 0 must distinguish ChatGPT GitHub connection from other connector/tool write surfaces. |
| C-02 | Repository-stored prompt requirement vs low-risk adoption friction. | Main AI development docs are present; status is PROPOSED. | Session 0 decides whether risk-tiered prompt/evidence records are allowed; do not silently bypass current text. |
| C-03 | Separate conversation as independent review. | Separate context is possible, but not proof of independent personnel/provider/statistical review. | Define reviewer independence and conflict-of-interest requirements. |
| C-04 | PR #42 excludes Codex while current official plan docs describe Codex availability. | PR #42 is unmerged; Codex local and Codex Cloud have different eligibility. | Session 0 decides whether local Codex is an optional adapter or prohibited channel. |
| C-05 | Scheduled Tasks vs continuous event-driven runtime. | Official task docs distinguish scheduled tasks, event triggers and Codex automations; Free/Go limitations apply. | Do not treat reminders or scheduled tasks as a durable event runtime. |
| C-06 | Engineering metadata may leak into business domain. | Architecture invariants and three-layer proposal. | Session 0 with A/I/affected Owners confirms strict separation and any explicit domain mapping. |
| C-07 | Self-hosted runner may be confused with AI worker runtime. | PR #27 and Issues #24/#26 are open proposals/pilot discussions. | Separate deterministic CI runner from privileged AI worker; require independent security acceptance. |
| C-08 | Branch protection and ruleset state unavailable. | API read returned 403. | Repository administrator supplies current settings and enforcement evidence. |
| C-09 | Stale PR metadata and head drift. | PR #27 body contains a historical SHA different from live head; all cited PRs have divergent histories. | Every reviewer refreshes exact PR Head and base before review. |

**Cross-domain disposition:** these issues are escalated to Session 0. Session 4 does not resolve governance conflicts or approve another Session's proposal.

**跨领域裁定：** 上述事项提交 Session 0 统一决策。Session 4 不擅自解决治理冲突，也不批准其他 Session 的提案。

---

## 11. Deferred Capabilities / 延期能力

Defer the following until a measurable requirement and independent approval exist:
- API-based autonomous model worker and API credential provisioning;
- webhook receiver, durable inbox, queue, scheduler and coordinator;
- persistent A–I worker fleet and publication broker;
- database-backed run ledger, leases/fencing and automated reconciliation;
- self-hosted AI execution of repository code;
- automatic PR merge, release or deployment;
- broad GitHub App permissions, long-lived PATs and shared master credentials;
- event-triggered Work automation as a required platform dependency.

以下能力延期，直到存在可量化需求并获得独立批准：API 自主模型 Worker、API 凭证、Webhook Receiver、持久化 Inbox/Queue/Scheduler/Coordinator、A–I Worker Fleet、Publication Broker、数据库 Run Ledger/Lease/Fencing、自动协调、自托管 AI 代码执行、自动 PR 合并/发布/部署、宽权限 GitHub App、长期 PAT 和共享主凭证，以及将 Work 事件触发作为强制平台依赖。

---

## 12. Open Questions / 待决问题

1. Does Session 0 approve conversation-first as the Phase 1 execution channel, and what explicit limits apply?
2. Can prompt/evidence requirements be risk-tiered without contradicting the current proposed AI development standard?
3. What qualifies as an independent review: separate session, separate human, different model, or a combination?
4. Is local Codex an optional coding adapter, or does the project require ordinary ChatGPT only?
5. Who is the authorized administrator to provide branch protection/ruleset evidence?
6. Which deterministic checks are mandatory before a PR can be accepted?
7. What measurable trigger (event volume, latency, toil, availability) would justify reconsidering a durable worker?
8. Which Owner(s) must approve any mapping between engineering process metadata and Layer A domain concepts?

1. Session 0 是否批准对话优先作为 Phase 1 执行通道，具体边界是什么？
2. Prompt/证据要求能否按风险分级，而不与当前 proposed 标准冲突？
3. 独立审查如何定义：独立会话、独立人员、不同模型，还是组合要求？
4. 本地 Codex 是可选编码适配器，还是项目只允许普通 ChatGPT？
5. 谁是能够提供 Branch Protection/Rulesets 证据的授权管理员？
6. PR 验收前哪些确定性检查是强制项？
7. 事件量、延迟、人工成本或可用性达到什么阈值才值得重新考虑 Durable Worker？
8. 工程流程元数据映射到 Layer A 领域概念时，需要哪些 Owner 批准？

---

## 13. Evidence Index / 证据索引

### 13.1 Repository evidence / 仓库证据

| ID | Source | Exact revision | Evidence |
|---|---|---|---|
| R-01 | Main branch | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | Live baseline refreshed 2026-11-18. |
| R-02 | `00-governance/architecture-invariants.md` | Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe` | I-03, I-12, I-13, I-21, I-23, I-24 and ADR/impact requirement. |
| R-03 | `14-ai-development/README.md` | Blob `9593fd66f2b830748d826d754ce3e6da00e6f144` | Engineering OS scope, work-item and prompt conventions; proposed status. |
| R-04 | `14-ai-development/ai-development-standard.md` | Blob `f46867f97fc1860015adbe2a1f7b8262640c16fd` | Owner authority, review, prompt lifecycle and acceptance vocabulary; proposed status. |
| R-05 | `14-ai-development/iteration-lifecycle.md` | Blob `8ecc8e4ddde78be01e2038be4ece8dc8ac282c97` | Request-to-acceptance lifecycle. |
| R-06 | `14-ai-development/prompt-and-evidence-template.md` | Blob `c9c545ae884991d2f5dd08c6880c50c97a13c143` | Prompt/evidence record template. |
| R-07 | `13-engineering-decisions/technology-architecture-blueprint.md` | Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | Local-first, modular architecture and infrastructure restraint. |
| R-08 | `.github/` on current main | Contents API 404 | No .github directory observed on refreshed main. |
| R-09 | Combined status for inspected main/PR heads | Empty status arrays | No status contexts returned; not proof of checks elsewhere. |
| R-10 | Branch protection and rulesets | API 403 | Enforcement is UNKNOWN; administrator evidence required. |

### 13.2 Pull request and issue evidence / PR 与 Issue 证据

- PR #42: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42 — live head `84d91b10e9069a575b479f6925d3b143757e82cb`; source Blob `9136e131e1166d9ba17d993efb5312d1d7d26121`; OPEN/DRAFT, not merged.
- PR #23: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/23 — live head `b6b9d2662729fdf2c112ae689cda34e235fdc82f`; AI-RUN-001 Blob `675d667eebd2a0d8c3d79ec502f903725db9788e`; AI-AUTO-001 Blob `c406d8c5b32977e8510b016ee71f9693d35ce821`; OPEN, proposals only.
- PR #27: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/27 — live head `6c70b2fadf39220b31824c3f32114e4e65b617f4`; OPEN; PR body includes stale historical head reference.
- Issue #24: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/24 — GitHub-mediated Owner workflow, OPEN, updated 2026-11-17.
- Issue #26: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/26 — persistent Ubuntu worker runtime, OPEN, updated 2026-11-17.

For all historical or current review claims, reviewers must read the review record and confirm its commit/head SHA. No PR author description is treated as an independent review.

### 13.3 Official product and security documentation / 官方产品与安全文档

All links below were checked on 2026-11-18. Availability and product behavior can change; verify again before implementation.

1. OpenAI — Connecting GitHub to ChatGPT: https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt-deep-research
2. OpenAI — ChatGPT Work and Codex: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
3. OpenAI — Get started with ChatGPT Work: https://learn.chatgpt.com/docs/get-started-with-work
4. OpenAI — Using Codex with your ChatGPT plan: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
5. OpenAI — Using Codex Cloud: https://help.openai.com/en/articles/20001545-using-codex-cloud
6. OpenAI — Scheduled tasks in ChatGPT: https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
7. OpenAI — ChatGPT and API billing: https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform
8. GitHub — Choosing permissions for a GitHub App: https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app
9. GitHub — GitHub App best practices: https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app
10. GitHub — GITHUB_TOKEN: https://docs.github.com/en/actions/concepts/security/github_token
11. GitHub — Workflow syntax and permissions: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
12. GitHub — Securely using pull_request_target: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
13. GitHub — Secure use reference: https://docs.github.com/en/actions/reference/security/secure-use

---

## 14. Final Recommendation / 最终建议

**PROPOSED — ADOPT CONVERSATION-FIRST, GITHUB-EVIDENCE-CENTRIC PHASE 1; DEFER DURABLE WORKER RUNTIME.**

Start Phase 1 without deploying a new platform. Use a human-created Issue, an ordinary ChatGPT conversation, current source retrieval, bounded analysis, user-controlled code changes, a dedicated Git branch and PR, exact-Head independent review, and explicit Owner/governance acceptance. Add deterministic CI only after a separate workflow/security review. Keep local Codex optional and user-controlled. Do not create an API-backed worker, webhook service, queue, database or persistent AI fleet until a measurable need and independent safety/operations approval exist.

**建议：Phase 1 采用对话优先、GitHub 证据中心的工作模式，延期 Durable Worker Runtime。** 无需部署新平台即可启动：人工创建 Issue、启动普通 ChatGPT 对话、读取当前规范、开展限定分析、由用户控制代码修改、通过独立分支和 PR 持久化变更、针对准确 Head SHA 独立审查，并由授权 Owner/治理主体明确验收。确定性 CI 需另行经过工作流和安全审查；本地 Codex 保持可选且由用户控制。在没有可量化需求和独立安全/运维批准前，不创建 API Worker、Webhook 服务、Queue、数据库或持久化 AI Worker Fleet。

This recommendation is not an approval of PR #42, #23 or #27; it does not settle cross-session governance conflicts, claim branch protection or CI success, or authorize implementation. Those decisions remain with Session 0 and the designated Owners.

本建议不批准 PR #42、#23 或 #27；不裁决跨 Session 治理冲突；不声称 Branch Protection 或 CI 已通过；也不授权实施。相关决策仍属于 Session 0 和指定 Owner。
