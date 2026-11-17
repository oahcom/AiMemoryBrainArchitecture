# AI-DEV-OS-001 — Session 1: GitHub-Native Workflow Architecture Research Report
# AI-DEV-OS-001 — 会话 1：GitHub 原生工作流架构研究报告

**Document ID:** AI-DEV-OS-001-SESSION-1-RESEARCH  
**Version:** 1.0.0  
**Status:** Phase 0 Research — Published for Independent Review  
**Research role:** Session 1 — GitHub-Native Workflow Architecture  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Baseline branch:** `main`  
**Baseline commit:** `e52594f181d2edb77448adcfed64a0fbdffaf3aa`  
**Baseline date:** 2026-11-18  
**Publication branch:** `research/ai-dev-os-001-session-1`  
**Language:** Chinese and English  
**Authority:** Research and recommendation only; no authority to approve cross-session architecture decisions or implement Phase 1.

---

## 1. Executive Summary / 执行摘要

### 中文

本研究评估在 `oahcom/AiMemoryBrainArchitecture` 中采用 GitHub 原生能力，建立 AI 开发任务的登记、提示词版本控制、执行来源追踪、验证、独立审查、验收和关闭流程。研究范围仅限开发工作流与治理载体，不重新设计业务架构，也不将某一种 Agent Runtime 或自动化编排方案视为既定决策。

**核心结论：建议有条件采用 GitHub-Native MVP。** 仓库已经存在一套内容较完整的 AI 开发治理草案：AI-STD-001、AI-PROC-001、AI-TPL-001，明确要求 Work Item、Owner、版本化 Prompt、基线 SHA、分支/提交、测试证据、独立 Reviewer 和 Acceptance Authority。但这些文件在当前 main 中明确标记为 **PROPOSED**，不能据此宣称治理规范已经正式采纳或强制执行。

当前 main 的目录树未发现 `.github/`，也未发现 Phase 0 研究发布目录；Work Item 索引仍声明没有登记的 Work Item。GitHub API 显示有 72 个 Open PR 和 24 个 Open Issue（Issues API 返回 96 条，其中 72 条是 PR）。PR #42 与 PR #23 均仍为 Open/Draft，反映 ChatGPT-native execution 与 Owner Worker 路径尚未形成可据此宣称已裁决的单一方案。PR #42 当前 Head `84d91b10e9069a575b479f6925d3b143757e82cb` 的 Status API 为 pending 且无状态项，Check Runs 为 0；其唯一历史 Review 对应旧 commit `1d6ab39375136d8649235feebeb6232609001222`，不是当前 Head 的审查证据。

建议第一阶段不要建设自研任务平台、数据库、队列、常驻 Worker、GitHub App 或通用 Agent Orchestrator。先复用现有治理文档与 GitHub Issues、Labels、Branches、Pull Requests、GitHub Actions，并以 Work Item Manifest、不可变 Prompt 和 Evidence Markdown 作为可读、可追溯的记录载体。人工或 ChatGPT 会话可以作为执行入口；执行工具和 Runtime 的最终选择交由 Session 0 结合其他 Session 研究裁决。

本报告是研究建议，不是规范采纳决议，也不授权任何 Phase 1 实施。

### English

This study evaluates a GitHub-native operating model for registering AI development work, versioning prompts, recording execution provenance, verifying changes, conducting independent review, accepting results, and closing work items. Its scope is workflow governance and evidence management. It does not redesign the product architecture and does not assume that a particular agent runtime or orchestration model has already been selected.

**Recommendation: conditionally adopt a GitHub-Native MVP.** The repository already contains a substantial proposed governance baseline: AI-STD-001, AI-PROC-001, and AI-TPL-001. They require work-item identity, accountable ownership, versioned prompts, base SHAs, branches and commits, test evidence, independent review, and acceptance authority. However, these documents are explicitly marked **PROPOSED** on the current main branch. Their existence is not proof of formal adoption or enforcement.

The current main tree contains no `.github/` directory and no Phase 0 publication directory. The Work Item index still says that no work items have been registered. The GitHub Issues endpoint returned 96 open records: 72 pull requests and 24 actual issues. PR #42 and PR #23 remain Open/Draft and represent competing execution approaches that cannot be treated as a settled decision. PR #42's current head, `84d91b10e9069a575b479f6925d3b143757e82cb`, has a pending commit status with zero status entries and zero check runs. Its only returned historical review is attached to commit `1d6ab39375136d8649235feebeb6232609001222`, not the current head.

The recommended first phase should avoid building a custom task platform, database, queue, persistent worker, GitHub App, or general-purpose agent orchestrator. Reuse the existing governance documents and GitHub Issues, Labels, Branches, Pull Requests, and GitHub Actions. Use Work Item manifests, immutable prompt files, and evidence Markdown as human-readable traceability records. Human or ChatGPT sessions may serve as execution entry points; the final choice of execution tooling and runtime belongs to Session 0 after reconciling the other research streams.

This report is a research recommendation, not an adoption decision and not an authorization to implement Phase 1.

---

## 2. Research Scope / 研究范围

### 中文

**纳入范围**
- GitHub Issues、Labels、Milestones、Projects、Branches、Pull Requests、Reviews、Commit Status/Check Runs、GitHub Actions 等原生能力的适用性。
- 当前仓库治理文档、Work Item 索引和相关 PR 的实时状态。
- Work Item、Prompt、Run、Branch、Commit、Verification、Review、Acceptance 之间的证据关联。
- PR 当前 Head 与历史 Review/CI 证据的绑定规则。
- MVP 范围、阶段验收条件、风险、成本、收益和延期条件。

**排除范围**
- 不设计或修改业务模块、领域模型、存储协议或架构不变量。
- 不实现 Worker Runtime、Webhook、GitHub App、数据库、队列、自动化编排器或 CI Workflow。
- 不决定 ChatGPT、Codex、Owner Worker 或其他执行环境的最终产品策略。
- 不对其他 Session 的研究结论作替代性裁决。

### English

**In scope**
- Applicability of native GitHub Issues, Labels, Milestones, Projects, Branches, Pull Requests, Reviews, commit statuses/check runs, and GitHub Actions.
- Current repository governance documents, the Work Item index, and live status of relevant pull requests.
- Evidence relationships among Work Item, Prompt, Run, Branch, Commit, Verification, Review, and Acceptance.
- Rules for binding review and CI evidence to the exact current PR head.
- MVP scope, phase acceptance conditions, risks, cost/benefit, and deferral criteria.

**Out of scope**
- No changes to business modules, domain models, storage protocols, or architecture invariants.
- No implementation of a Worker Runtime, webhooks, GitHub App, database, queue, orchestrator, or CI workflow.
- No final product decision among ChatGPT, Codex, Owner Worker, or other execution environments.
- No substitute adjudication of findings owned by other research sessions.

---

## 3. Research Method and Evidence Semantics / 研究方法与证据语义

All repository facts below were checked against GitHub resources on 2026-11-18. The refreshed main reference is `e52594f181d2edb77448adcfed64a0fbdffaf3aa`; the recursive Git tree response was not truncated and contained 126 entries. The report uses the following labels:

- **VERIFIED** — directly supported by a current repository file, Git object, API response, or official product documentation.
- **PROPOSED** — a recommendation made by this research; not an adopted project decision.
- **UNKNOWN** — the available evidence or permissions do not establish the fact.
- **NOT APPLICABLE** — outside this report's scope.

Historical PR descriptions and author statements are treated as claims, not independent evidence. A review is current only for the exact commit it reviewed; a review on an earlier commit does not automatically apply to a changed head. A check run or status on another SHA is not evidence for the candidate SHA unless an explicit, independently justified equivalence is recorded.

本报告所有仓库事实均于 2026-11-18 对照 GitHub 资源核验。刷新后的 main 基线为 `e52594f181d2edb77448adcfed64a0fbdffaf3aa`；递归 Git Tree 未被截断，共返回 126 个条目。本文使用 VERIFIED、PROPOSED、UNKNOWN、NOT APPLICABLE 四种证据状态。PR 作者描述仅视为声明，不视为独立证据；Review 只对其精确审查的 Commit SHA 有效；其他 SHA 上的 CI/Status 不自动构成候选 Head 的验证证据。

---

## 4. Current State / 当前状态

### 4.1 Repository baseline / 仓库基线

| Item | Current observation | Status |
|---|---|---|
| Repository visibility | Private repository | VERIFIED |
| Default branch | `main` | VERIFIED |
| Main HEAD | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | VERIFIED |
| Recursive tree | 126 entries; not truncated | VERIFIED |
| Branches returned | 94 | VERIFIED |
| Open PRs | 72 | VERIFIED |
| Open Issues | 24 actual Issues; Issues API returned 96 records including 72 PRs | VERIFIED |
| `.github/` in main tree | No path found | VERIFIED |
| `14-ai-development/research/phase-0/` | Not present in refreshed main tree | VERIFIED |
| Work Item index | States no Work Items are registered | VERIFIED |
| Discussions | Repository metadata reports disabled | VERIFIED |
| Releases | No release record was observed in the prior read-only inventory; current release inventory is not a gate for this proposal | UNKNOWN for current exhaustive state |
| Effective branch protection/rulesets | Full effective policy could not be confirmed with available API permissions | UNKNOWN |

The branch listing marked returned branches as `protected=false`. This is an API observation, not proof that every effective ruleset or organization-level policy is absent. The branch-protection read was permission-restricted; effective enforcement therefore remains UNKNOWN.

### 4.2 Existing governance documents / 已有治理文档

The following files exist on current main and were read directly:

| File | Blob SHA | Status declared in file | Research interpretation |
|---|---|---|---|
| `14-ai-development/README.md` | `9593fd66f2b830748d826d754ce3e6da00e6f144` | Initial PROPOSED baseline | Defines required use and says adoption needs explicit decision |
| `14-ai-development/ai-development-standard.md` | `f46867f97fc1860015adbe2a1f7b8262640c16fd` | AI-STD-001 v1.0 PROPOSED | Defines roles, lifecycle, DoR/DoD, review and acceptance |
| `14-ai-development/iteration-lifecycle.md` | `8ecc8e4ddde78be01e2038be4ece8dc8ac282c97` | AI-PROC-001 v1.0 PROPOSED | Defines iteration and integration stages |
| `14-ai-development/prompt-and-evidence-template.md` | `c9c545ae884991d2f5dd08c6880c50c97a13c143` | AI-TPL-001 v1.0 PROPOSED | Defines manifest, prompt record and evidence bundle |
| `14-ai-development/work-items/INDEX.md` | `a9d433337c7e1d2c497b18a437f5289dd74134ea` | No registered work items | Index registration is not yet demonstrated |

**Important:** The README says each substantive task MUST have a Work Item ID and repository-stored prompt, a single accountable Owner and distinct independent reviewer, and a base SHA/branch/commit/test evidence. It also says the documents are an initial PROPOSED baseline and do not retroactively certify earlier work. AI-STD-001 explicitly says one AI session adopting several personas is not independent review. These are documented requirements, not evidence that every active PR currently complies.

### 中文补充

现有治理文档并非空白，反而已经覆盖了大部分应有概念。主要缺口不是“再设计一套流程”，而是规范采纳状态、登记覆盖率、执行证据、当前 Head 证据和门禁执行情况尚未得到证明。必须避免把文档中使用 MUST 的措辞误读为 GitHub 已自动强制执行。

---

## 5. Existing Capabilities / 已有能力

### 中文

1. **Work Item 与角色模型 — VERIFIED（文档存在）**：AI-STD-001 定义 A–I Owner、Sponsor、Accountable Owner、Implementing AI、Independent Reviewer、Integration Architect 和 Acceptance Authority。
2. **任务生命周期 — VERIFIED（文档存在）**：生命周期包含 PROPOSED、ANALYZED、PROMPT_READY、READY、IN_PROGRESS、IMPLEMENTED、VERIFIED、REVIEWED、INTEGRATION_READY、ACCEPTED、MERGED、CLOSED，并包含 BLOCKED、REJECTED。
3. **Prompt 版本化 — VERIFIED（模板存在）**：模板包含 Prompt ID、版本、SHA-256、执行 Run、基线 SHA、分支、Commit、Verification、Review、Acceptance 等字段。
4. **DoR/DoD 与验证分层 — VERIFIED（文档存在）**：规范描述静态检查、单元/集成/契约测试、故障注入、安全测试和端到端验收。
5. **GitHub 原生协作载体 — VERIFIED（产品能力）**：Issues 可跟踪任务/缺陷并与 PR、Labels、Milestones、Projects 关联；PR 可承载代码差异与 Review；Actions 可执行自动化工作流。仓库实际启用和配置情况必须单独核验。
6. **已有 PR 与 Actions 历史 — VERIFIED（存在性）**：仓库有大量 PR，且 Actions API 可观察到历史运行。历史运行不证明当前 main 上存在正确的 PR-required checks 或有效分支门禁。

### English

1. **Work-item and role model — VERIFIED as documented:** AI-STD-001 defines A–I Owners, Sponsor, Accountable Owner, Implementing AI, Independent Reviewer, Integration Architect, and Acceptance Authority.
2. **Task lifecycle — VERIFIED as documented:** The lifecycle includes PROPOSED, ANALYZED, PROMPT_READY, READY, IN_PROGRESS, IMPLEMENTED, VERIFIED, REVIEWED, INTEGRATION_READY, ACCEPTED, MERGED, and CLOSED, plus BLOCKED and REJECTED.
3. **Prompt versioning — VERIFIED as a template capability:** The template contains Prompt ID/version/hash, execution Run, base SHA, branch, commit, verification, review, and acceptance fields.
4. **DoR/DoD and layered verification — VERIFIED as documented:** The standard describes static checks, unit/integration/contract tests, fault injection, security tests, and end-to-end acceptance.
5. **Native GitHub collaboration primitives — VERIFIED as product capabilities:** Issues can track tasks and defects and relate to PRs, labels, milestones, and projects; PRs carry diffs and reviews; Actions runs workflows. Repository configuration and actual adoption must be checked separately.
6. **Existing PR and Actions history — VERIFIED as existence:** The repository has a large PR inventory and historical Actions runs. Historical runs do not prove that current main has correctly configured required PR checks or effective branch gates.

---

## 6. Missing Capabilities and Evidence Gaps / 缺失能力与证据缺口

| Gap | Evidence / observation | Status | Consequence |
|---|---|---|---|
| Formal adoption of AI-STD-001 / AI-PROC-001 / AI-TPL-001 | All declare PROPOSED | VERIFIED gap | Requirements cannot be treated as approved policy |
| Central registration completeness | Work Item INDEX says none registered | VERIFIED | No reliable governed-work inventory |
| `.github/` governance configuration | No `.github/` path on main | VERIFIED | No repository-level issue form, CODEOWNERS or workflow config evidenced there |
| Effective branch protection/rulesets | Read permission restricted; returned branches show protected=false | UNKNOWN | Cannot claim automated merge enforcement |
| Current-head check coverage | PR #42 current head has zero statuses and zero check runs | VERIFIED for that SHA | No machine evidence currently visible for that candidate head |
| Review freshness | PR #42 review commit differs from current head | VERIFIED | Historical review cannot approve current head |
| Independent reviewer identity | Review API identifies reviewer as `oahcom`; same repository account as PR author | VERIFIED identity; independence UNKNOWN/not established | No evidence of an independent review on current head |
| Work Item → Prompt → Run binding | Template proposes fields; index has no entries | VERIFIED gap in current registration evidence | Execution provenance cannot be reconstructed consistently |
| Defect/finding reconciliation | Standard defines severity and finding fields, but no complete operational registry is evidenced in the reviewed index | UNKNOWN | Findings may be scattered across PR threads/issues |
| Acceptance and closure proof | Normative stages exist; operational records are not established | UNKNOWN | GitHub closed state may be mistaken for engineering acceptance |
| Projects/Milestones usage | Repository metadata has projects enabled, but accessible live inventory was not established | UNKNOWN | Do not assume these are operational control planes |

### PR #42 and PR #23 evidence / 相关 PR 证据

- **PR #42** — [docs(ai-dev): restart on ChatGPT-native execution model](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42), Open/Draft. The open-PR listing identifies head branch `design/chatgpt-native-execution-model`, head SHA `84d91b10e9069a575b479f6925d3b143757e82cb`, and base SHA `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. Current main is `e52594f...`, so this PR is not based on the current main snapshot. Its current head status is `pending` with zero statuses; check-runs total is 0. The only returned review is [review 5937629228](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42#pullrequestreview-5937629228), submitted by `oahcom` on 2026-11-17T11:30:43Z against commit `1d6ab39375136d8649235feebeb6232609001222`. That commit is not the current PR head. **Conclusion: no current-head independent approval is established.**
- **PR #23** — [AID-2026-001 A–I review package](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/23), Open/Draft. The open-PR listing identifies head branch `ai/AID-2026-001/governance-owner-review`, head SHA `b6b9d2662729fdf2c112ae689cda34e235fdc82f`, and base SHA `55d44b9276456f88bd2193de8b06aff146c228a4`. It remains a proposal, not an adopted governance decision.
- These PRs are evidence that alternative workflow approaches have been proposed. Their descriptions are not independent proof of correctness, adoption, or operational behavior.

### English interpretation

The primary gaps are not a lack of workflow vocabulary. They are the absence of demonstrated formal adoption, complete task registration, consistent prompt/run binding, current-head verification, independent review evidence, and enforceable acceptance/merge gates. PR #42's prior review is tied to an earlier commit and does not establish review of its current head. PR #23 and #42 remain proposals and should be adjudicated by Session 0.

---

## 7. Proposed Architecture / 建议架构

### 7.1 GitHub-native evidence chain / GitHub 原生证据链

**PROPOSED:**  
`GitHub Issue → Work Item Manifest → Immutable Prompt Version → Execution Run Record → Branch → Commit(s) → Verification Evidence → Independent Review → PR → Acceptance Record → Merge Commit → Work Item Closeout`

Each link should use stable identifiers and direct GitHub URLs/SHAs. GitHub Issues and PRs provide discussion and collaboration surfaces; version-controlled Markdown/YAML files provide durable structured records. Avoid a second database as the source of truth during MVP.

**中文说明：** Issue 负责可发现的任务入口；Manifest 负责身份、责任、状态和证据索引；Prompt 文件负责冻结执行指令；Run 记录负责区分一次执行尝试与任务本身；Branch/Commit 负责代码来源；测试报告绑定精确 Commit SHA；Review 报告绑定精确 Head SHA；Acceptance 记录绑定审查结论、风险处置与合并授权；合并后将 Merge SHA 回写 Work Item 记录。

### 7.2 Reuse the existing lifecycle / 复用现有生命周期

**PROPOSED — reuse, do not replace:** retain the lifecycle already defined in AI-STD-001:

`PROPOSED → ANALYZED → PROMPT_READY → READY → IN_PROGRESS → IMPLEMENTED → VERIFIED → REVIEWED → INTEGRATION_READY → ACCEPTED → MERGED → CLOSED`

Use the existing `BLOCKED` and `REJECTED` states for exception paths.

Do not create a GitHub label for every lifecycle state. GitHub Issue state (OPEN/CLOSED) and engineering lifecycle state are different dimensions. Keep lifecycle state in the existing Work Item manifest; use GitHub labels for a small number of stable classification dimensions such as class, risk, owner/domain, and blocker. Reuse existing repository labels where they already fit; do not create a parallel taxonomy without an adoption decision.

### 7.3 Work Item, Prompt, and Run are separate entities / 三类对象必须分离

- **Work Item (What):** the requested outcome, ownership, scope, acceptance criteria, dependencies and lifecycle.
- **Prompt Artifact (How):** the immutable, reviewed instruction version used for a run; identify by Prompt ID, version and SHA-256.
- **Execution Run (Which attempt):** one attempt to execute a prompt against a base SHA with a specific tool/session/environment; preserve failed and interrupted attempts rather than overwriting them.

One Work Item may have multiple Prompt versions and multiple Runs. One Run may produce multiple commits. A PR may integrate one Work Item or an explicitly declared bounded set; do not infer these relationships from branch names alone.

### 7.4 Evidence integrity rules / 证据完整性规则

1. Every test report identifies the exact tested commit SHA, command, environment, fixture, expected result, actual result and PASS/FAIL/NOT RUN.
2. Every review identifies the exact reviewed head SHA, reviewer identity/role, findings and disposition.
3. If the PR head changes after review, mark that review stale for the new head and require delta or full re-review according to risk.
4. Required check evidence must be associated with the candidate commit. A workflow run on another SHA is not a pass for the candidate.
5. AI-generated statements are assertions until backed by GitHub or reproducible evidence.
6. Acceptance is a human/governance decision with an identified authority; it is not inferred from a green check or PR close event.
7. Preserve rejected, blocked, superseded and failed runs as historical evidence; do not erase or rewrite provenance.

---

## 8. MVP Recommendation / MVP 建议

### 中文

建议 MVP 仅使用以下能力：

- GitHub Issues：任务、缺陷和 follow-up 的入口。
- Existing Labels：轻量分类，不复制完整生命周期。
- Branches + Pull Requests：隔离变更和审查。
- GitHub Actions：仅运行确定性、可重复、与 PR Head 绑定的检查；具体 workflow 和 required-check 配置须另行批准并验证。
- Existing Manifest/Prompt/Evidence Markdown：结构化登记和证据。
- 人工/ChatGPT 会话执行：先保持执行入口简单，不把 Runtime 产品选择混入 GitHub 治理 MVP。

**不建议在 MVP 引入**：自研 Dashboard、任务数据库、消息队列、常驻 Worker、Webhook 服务、GitHub App、跨系统编排器或多层状态同步服务。

### English

The MVP should use only:
- GitHub Issues for work, defects, and follow-up entry points.
- Existing labels for lightweight classification rather than duplicating the full lifecycle.
- Branches and Pull Requests for isolation and review.
- GitHub Actions only for deterministic, reproducible checks bound to the PR head; workflow and required-check configuration require separate approval and verification.
- Existing manifest, prompt, and evidence Markdown templates for structured records.
- Human/ChatGPT-session execution as the initial simple entry point; do not couple the governance MVP to a runtime product decision.

Do not introduce a custom dashboard, task database, message queue, persistent worker, webhook service, GitHub App, cross-system orchestrator, or multi-layer status synchronization service in the MVP.

### Cost / benefit / risk / defer conditions

| Capability | Cost | Benefit | Risk | Defer until |
|---|---|---|---|---|
| Issue + existing labels | Low | Visible intake, assignment, search | Label sprawl or duplicate task records | Never defer basic task registration; defer taxonomy expansion |
| Manifest + Prompt Markdown | Low–medium | Immutable, inspectable provenance | Manual drift and incomplete updates | Automate only after repeated measured failure |
| PR + exact-SHA review | Low | Auditable change and review boundary | Review can become stale after force/update | Keep mandatory from MVP |
| GitHub Actions checks | Medium | Repeatable objective verification | False confidence if checks are not required or are bound to wrong SHA | Add per risk class after policy/permissions confirmed |
| Projects/Milestones | Low–medium | Portfolio view and scheduling | Duplicate source of truth and maintenance overhead | Adopt only when cross-work-item planning need is demonstrated |
| Issue Forms | Low | Consistent intake fields | Form rigidity and maintenance | Adopt when intake variability causes measurable rework |
| CODEOWNERS / branch rules | Medium; plan/permission dependent | Reviewer routing and enforcement | Availability/permission assumptions may be wrong | Confirm repository plan, effective rules and owner mapping first |
| Custom DB/dashboard | High | Querying and reporting at scale | New source of truth, sync and security burden | Defer until GitHub-native records demonstrably fail scale needs |
| Persistent Worker / GitHub App / orchestrator | Very high | Autonomous execution and integration | Credential, isolation, retry, event and operational complexity | Defer until Session 0 approves execution strategy and a measured need |

---

## 9. Phase 1 Acceptance Criteria / Phase 1 验收标准

**PROPOSED:** Phase 1 should not be declared complete until each applicable criterion has a directly inspectable evidence reference.

| ID | Acceptance criterion | Required evidence |
|---|---|---|
| P1-01 | Every substantive new task has a unique Work Item ID | Issue URL + manifest |
| P1-02 | Each Work Item has one accountable Owner and named acceptance authority | Manifest and Issue assignment/record |
| P1-03 | Scope, non-goals, class, risk, dependencies and testable acceptance criteria are recorded | Manifest/prompt |
| P1-04 | Executed prompt version is immutable and identified by Prompt ID/version/SHA-256 | Prompt file and digest |
| P1-05 | Every execution attempt has a distinct Run identity and records tool/session, start/end or interruption, base SHA and prompt SHA | Run record |
| P1-06 | Implementation branch and commits are linked to Work Item and Run | Manifest + commit URLs |
| P1-07 | PR links the Work Item and declares included Runs/commits | PR body and manifest |
| P1-08 | Verification records command, environment, exact commit SHA, fixture, expected/actual result and status | Test report / Actions run |
| P1-09 | Independent review is performed by a distinct reviewer, not the implementation author/session | Reviewer identity + review record |
| P1-10 | Review is bound to exact current PR Head SHA | Review commit SHA equals reviewed head SHA |
| P1-11 | Findings have severity, owner, status, evidence and closure condition | Review report / linked Issue |
| P1-12 | BLOCKER/P0/P1 findings are resolved or handled by explicit authorized risk decision consistent with policy | Finding disposition and decision record |
| P1-13 | Acceptance authority explicitly records ACCEPTED or a bounded conditional disposition | Acceptance record |
| P1-14 | Merge evidence identifies target branch and merge commit SHA | PR and merge commit |
| P1-15 | Work Item closeout reconciles Prompt, Runs, Branch, Commits, Tests, Review, Findings, Acceptance and Merge | Updated manifest and index |
| P1-16 | Missing or unrun checks are recorded as NOT RUN, never implied PASS | Evidence report |
| P1-17 | Evidence links can be opened by an authorized independent reviewer | Read-back verification |

**Gate note:** A Phase 1 process may begin with manual controls if machine enforcement is unavailable, but it must label them as manual controls. Do not claim that a rule is enforced by GitHub until the effective repository/organization configuration has been read and tested. Phase 1 acceptance must distinguish process compliance from automated enforcement.

---

## 10. Risks and Conflicts / 风险与冲突

| ID | Risk / conflict | Impact | Mitigation / owner |
|---|---|---|---|
| R-01 | Governance docs are PROPOSED, not formally adopted | Teams may treat recommendations as binding or inconsistent | Session 0 decides adoption and normative status |
| R-02 | PR backlog is large (72 Open PRs at baseline) | New process may add overhead without resolving integration debt | Session 0 decides whether backlog recovery is a prerequisite or parallel track |
| R-03 | PR #42 vs PR #23 execution-model conflict | Competing proposals may lead to duplicated runtime/workflow investment | Session 0 adjudicates with Sessions 2–4 findings |
| R-04 | Historical review/check evidence is stale | Unsafe acceptance based on wrong commit | Bind all review/check evidence to exact current head |
| R-05 | No `.github/` files in current main | No repository-level workflows/templates/CODEOWNERS evidenced in main | Do not assume automatic enforcement; configuration is separate approved work |
| R-06 | Branch protection/rulesets not fully readable | Merge controls unknown | Session 0 / repository admin confirms plan, permissions and effective rules |
| R-07 | Manual manifests can drift | Missing or stale provenance | Begin with a small required checklist; automate only after measured failure |
| R-08 | Lifecycle labels can proliferate | Duplicate and inconsistent status systems | Keep engineering lifecycle in manifest; Issue state remains separate |
| R-09 | Different AI sessions may be incorrectly called independent | Self-review risk | Apply existing AI-STD-001 separation-of-duties rule; reviewer must be genuinely distinct |
| R-10 | Projects/Milestones/Issue Forms/CODEOWNERS are assumed available | Unverified platform assumptions | Treat current usage/configuration as UNKNOWN unless directly verified |

### Cross-session conflicts requiring Session 0 / 必须交 Session 0 的跨领域冲突

1. **Execution channel:** ChatGPT-native session execution versus Codex/Owner Worker Runtime. PR #42 and #23/#36 are proposals; Session 0 must compare against Session 2 provenance findings and Session 4 platform adoption reality.
2. **Independent reviewer definition:** AI-STD-001 says the implementing session cannot review itself and a single session adopting multiple personas is not independent. Session 0 must decide acceptable separation boundaries for separate sessions/agents and high-risk work.
3. **Normative adoption:** whether and when AI-STD-001, AI-PROC-001 and AI-TPL-001 become DECIDED/NORMATIVE.
4. **Work Item identity:** formal mapping between AID IDs and GitHub Issues, including retrospective registration of existing work.
5. **Backlog sequencing:** whether PR backlog recovery precedes Phase 1 rollout, or proceeds as a controlled parallel track.
6. **Manual versus machine gates:** who owns acceptance when GitHub branch protection/check enforcement cannot be confirmed.
7. **Repository plan/permissions:** whether the project should change GitHub plan or permissions to enable required protections, CODEOWNERS or other controls.

These are decision requests, not unilateral decisions by Session 1.

---

## 11. Deferred Capabilities / 延期能力

| Capability | Why defer | Revisit trigger |
|---|---|---|
| Custom workflow dashboard | Existing GitHub surfaces and Markdown are sufficient for MVP | Demonstrated reporting/search bottleneck across a sustained workload |
| External task database | Creates a second source of truth and sync burden | Git-native manifest/index cannot meet measured query/scale needs |
| Persistent worker runtime | Adds credentials, lifecycle, retry, isolation and operations | Session 0 approves runtime model and bounded use case |
| GitHub App/webhook orchestration | Security and event-delivery complexity is premature | Explicit integration requirement with threat model and owner |
| Automated lifecycle state synchronization | Risks silently changing state without evidence | Stable manifest schema and tested transition rules exist |
| Projects V2 / Milestones as control plane | Current adoption/access not established; may duplicate manifest | Portfolio scheduling need is demonstrated and ownership decided |
| Broad Issue Forms taxonomy | Could freeze unsettled governance fields | Intake errors justify a small controlled form |
| CODEOWNERS / mandatory branch rules | Effective plan/permissions/configuration UNKNOWN | Admin confirms support and exact policy design |
| Multi-agent orchestrator | Execution strategy is a Session 0 decision | Multiple repeatable workloads prove manual/session coordination inadequate |

---

## 12. Open Questions / 待决问题

1. Does Session 0 formally adopt the existing proposed AI development governance documents, and what is the effective date?
2. Is a GitHub Issue the canonical external identity for each AID Work Item, or is the AID ID primary with an optional Issue link?
3. What exactly qualifies as an independent reviewer for documentation, implementation, security, and cross-module changes?
4. Is ChatGPT-native execution the default, or is a bounded Owner Worker/Codex runtime required? What is the fallback?
5. Must every execution attempt have a separate immutable Run record, including interrupted and failed runs?
6. Can one PR contain multiple Work Items or multiple Runs, and what explicit mapping is required?
7. Which acceptance authority may accept residual findings, and what severities may never be waived?
8. Should PR backlog recovery be a Phase 1 entry gate?
9. Which GitHub plan and repository permissions are available for effective branch protection, required checks and CODEOWNERS?
10. Should Projects/Milestones be used for portfolio planning, or remain optional views over Issues?
11. What is the minimal set of labels that already exists and is authoritative? A complete current label catalog was not established in this research.
12. Who owns periodic Work Item index reconciliation and stale-evidence detection?

---

## 13. Evidence Index / 证据索引

### 13.1 Repository and GitHub evidence / 仓库与 GitHub 证据

All file links below point to the exact baseline commit `e52594f181d2edb77448adcfed64a0fbdffaf3aa`, not a moving branch URL.

| Evidence | Direct URL | What it supports |
|---|---|---|
| Repository | https://github.com/oahcom/AiMemoryBrainArchitecture | Repository identity and visibility |
| Main baseline commit | https://github.com/oahcom/AiMemoryBrainArchitecture/commit/e52594f181d2edb77448adcfed64a0fbdffaf3aa | Main HEAD at research refresh |
| Recursive tree API | https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/git/trees/e52594f181d2edb77448adcfed64a0fbdffaf3aa?recursive=1 | 126-entry tree; no `.github/` or Phase 0 path |
| Governance README | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/README.md | Required usage and PROPOSED status |
| AI-STD-001 | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/ai-development-standard.md | Roles, lifecycle, DoR/DoD, review and acceptance |
| AI-PROC-001 | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/iteration-lifecycle.md | Workflow stages, CI/review/integration/closeout |
| AI-TPL-001 | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcf64a0fbdffaf3aa/14-ai-development/prompt-and-evidence-template.md | Manifest, prompt versioning and evidence bundle |
| Work Item index | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcf64a0fbdffaf3aa/14-ai-development/work-items/INDEX.md | No registered Work Items statement |
| PR #42 | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42 | ChatGPT-native execution proposal |
| PR #42 current head commit | https://github.com/oahcom/AiMemoryBrainArchitecture/commit/84d91b10e9069a575b479f6925d3b143757e82cb | Exact head SHA identified in open PR inventory |
| PR #42 historical review | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42#pullrequestreview-5937629228 | Review ID 5937629228; reviewed commit `1d6ab39375136d8649235feebeb6232609001222` |
| PR #23 | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/23 | AID-2026-001 governance/Owner review proposal |
| Open PR API | https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls?state=open&per_page=100 | 72 Open PRs and their listed head/base refs |
| Open Issues API | https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/issues?state=open&per_page=100 | 96 records: 24 Issues and 72 PRs |
| PR #42 status API | https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/84d91b10e9069a575b479f6925d3b143757e82cb/status | Pending state, zero status entries |
| PR #42 check-runs API | https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/84d91b10e9069a575b479f6925d3b143757e82cb/check-runs | Zero check runs |

### 13.2 Official GitHub product documentation / GitHub 官方产品文档

- Issues overview: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- Using issues: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues
- Issue forms: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues/using-issue-forms
- GitHub Projects: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
- CODEOWNERS: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Required status checks: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging

Official documentation establishes product capabilities, not that those features are enabled or available under this repository's current plan and permissions.

### 13.3 Evidence limitations / 证据限制

- Effective branch protection and rulesets could not be fully read with the available API permissions; status remains UNKNOWN.
- The full current Projects V2/Milestones adoption state was not established.
- The complete label catalog was not established.
- Absence of `.github/` in the current main tree establishes absence of repository files at that ref, not absence of organization-level policy.
- PR review identity and commit binding are observable, but whether a reviewer is organizationally independent beyond the account/session evidence is not inferable from a username alone.
- The report does not claim any test execution, CI success, workflow enforcement, or runtime behavior beyond the exact API evidence listed above.

---

## 14. Final Recommendation / 最终建议

### 中文

**建议 Session 0 对 GitHub-Native MVP 作条件性批准，并将现有 AI-STD-001 / AI-PROC-001 / AI-TPL-001 作为优先复用对象，而不是另建一套治理体系。**

批准 Phase 1 前至少需要 Session 0 明确：
1. 现有规范是否正式采纳以及何时生效；
2. AID Work Item 与 GitHub Issue 的身份关系；
3. 独立 Reviewer 的定义和高风险任务的审查分离要求；
4. ChatGPT-native 与 Worker/Codex 的执行策略；
5. PR 积压治理与 Phase 1 的先后关系；
6. 在当前 GitHub plan/permissions 下哪些门禁可以真实强制，哪些只能人工执行。

MVP 的原则是：GitHub 作为协作与变更记录面，现有 Markdown/YAML 作为任务与证据记录面，所有关键状态必须有精确 SHA 和可复核链接；任何未验证事项都保持 UNKNOWN。不要先建设新平台，再寻找需要它解决的问题。

**本报告不批准规范，不批准任何跨领域架构选择，也不授权实施。** 所有跨 Session 冲突提交 Session 0 Principal Architect 裁决。

### English

**Session 0 should conditionally approve the GitHub-Native MVP and prioritize reuse of AI-STD-001, AI-PROC-001, and AI-TPL-001 rather than create a second governance system.**

Before Phase 1, Session 0 should decide at least:
1. Whether and when the existing standards become formally adopted;
2. The identity relationship between AID Work Items and GitHub Issues;
3. The definition of an independent reviewer and stricter separation for high-risk work;
4. The execution strategy across ChatGPT-native sessions and Worker/Codex options;
5. Whether PR backlog recovery precedes or runs alongside Phase 1;
6. Which gates can actually be enforced under current GitHub plan/permissions and which remain manual.

The MVP principle is simple: GitHub is the collaboration and change-record surface; existing Markdown/YAML is the work and evidence record surface; every critical state is tied to exact SHAs and inspectable links; unverified facts remain UNKNOWN. Do not build a new platform before demonstrating the problem it must solve.

**This report does not adopt standards, approve cross-domain architecture choices, or authorize implementation.** All cross-session conflicts are submitted to Session 0 Principal Architect for adjudication.
