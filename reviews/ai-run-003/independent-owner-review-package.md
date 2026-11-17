# AI-RUN-003 Independent Owner Review Package
# AI-RUN-003 独立 Owner 审查任务包

**Status / 状态:** PROPOSED — review requests prepared; no approvals recorded / 提案中——已准备审查任务；尚无批准记录

## 1. Review rules / 审查规则

- Reviewers must inspect the exact PR head SHA and all files in the diff, not rely on this summary.
- A reviewer must not approve work they authored or materially edited.
- One ChatGPT conversation simulating multiple roles is not independent review.
- Each reviewer records PASS / CONDITIONAL PASS / REQUEST CHANGES / BLOCKED with findings, evidence paths, tested SHA and unresolved risks.
- Silence, a comment reaction, scheduled execution or PR mergeability is not approval.
- Any change to the reviewed head SHA invalidates the review unless the reviewer explicitly confirms the new SHA.
- All project architecture/design documents must be bilingual Chinese/English under the project convention.

审查者必须检查精确 PR Head SHA 和全部 Diff；不得审查自己编写/实质修改的内容；一个会话模拟多角色不构成独立审查；必须记录结论、Finding、证据路径、测试 SHA 和风险；沉默、Reaction、定时执行或 Mergeable 都不等于批准；Head SHA 变化后审查失效，除非审查者明确确认新 SHA；所有项目架构/设计文档遵循中英双语规范。

## 2. Review matrix / 审查矩阵

| Reviewer role | PR scope | Required focus | Required output |
|---|---|---|---|
| A — independent integration reviewer (not the author of the runtime docs) | PR #31–#35 cumulative diff | Cross-ADR consistency, authority boundaries, no contradictory state/identity/lease/publication semantics, dependency ordering | Integration review report + disposition of each cross-ADR conflict |
| I — Security & Governance Owner | PR #31–#35 cumulative diff | Threat model, webhook trust, least privilege, secret lifecycle, prompt injection, capability authorization, worker isolation, audit, branch bypass | Security review with severity, exploit preconditions, mitigations and residual risk |
| Storage/Consistency | ADR-RUN-001 and runtime data model | TX-01..TX-08, transaction isolation, uniqueness, lease fencing, outbox/reconciliation, migrations, backup/restore | Physical schema proposal or explicit blockers; transaction/fault test plan |
| Testing/Quality | ADRs + data model | Testability, exact-SHA checks, fault injection, race tests, acceptance coverage and CI check names | Conformance matrix and executable test plan |
| H / Protocol owner (if BMCP or external message contracts are reused) | ADR-RUN-002/004/005 interfaces | Event envelope compatibility, identity fields, schema versioning, acknowledgment semantics | Protocol compatibility findings |
| Pilot Owner (selected low-risk Owner) | Read-only pilot scope | Whether work routing, prompt binding, evidence and stop conditions are usable and bounded | Pilot acceptance or concrete changes requested |
| Repository administrator | PR #27 and ADR-RUN-006 | Runner isolation, branch rules, required checks, bypass policy and settings readback | Settings evidence and successful negative tests |

## 3. Exact review targets / 精确审查目标

- PR #31 — ba07e5499e9c1cc5474aa367df67b4df9e04e8e3 (runtime architecture + ADR-RUN-001)
- PR #32 — 83545e6565c93f8b5c886e848b8cc989ca9a7e4a (ADR-RUN-002; base is PR #31 branch)
- PR #33 — aba96fcaf7c7504d221e02b1612888a2dd557718 (ADR-RUN-003; base is PR #32 branch)
- PR #34 — bc38965dbdbafa5dd9bcf08cfaba6216a5bb10c6 (ADR-RUN-004/005/006; base is PR #33 branch)
- PR #35 — 4bd853805cd91440360ed5b0f6a995e9e3ec1437 (logical runtime data model; base is PR #34 branch)

These are author-recorded target SHAs at package creation. Reviewers must re-fetch the live PR head before review.

以上 SHA 是本审查包创建时记录的目标；审查者必须在审查前重新读取实时 PR Head。

## 4. A — independent integration review prompt / A 集成审查提示词

You are A, acting only as an independent integration reviewer for AI-RUN-003. You did not author the reviewed changes. Fetch PR #31–#35 live and inspect their complete diffs and linked source ADRs. Build a traceability matrix across ADR-RUN-001..006 and the runtime data model. Verify: (1) no duplicate or contradictory authority for GitHub identity, event eligibility, prompt approval, lease/fencing, publication and audit; (2) all transaction boundaries have matching failure/recovery semantics; (3) the stacked PR dependency order is explicit; (4) no proposal is described as implemented/deployed/accepted; (5) all architecture documents are bilingual. Report findings with severity, exact file/section, evidence and required owner. Do not edit files, approve your own work or merge.

你是 A，且仅担任独立集成审查者。你没有编写被审查变更。实时获取 PR #31–#35 并检查完整 Diff 和关联 ADR。建立 ADR-RUN-001..006 与 Runtime 数据模型的追踪矩阵，核验权威边界、事务/故障语义、PR 堆叠依赖、状态真实性和双语规范。报告精确 Finding，不修改文件、不自批、不合并。

## 5. I — independent security review prompt / I 安全审查提示词

You are I, Security & Governance Owner, reviewing AI-RUN-003. Inspect PR #31–#35 at their live heads. Threat-model webhook spoofing/replay, secret theft, token exfiltration, prompt injection, untrusted PR execution, path traversal, worker escape, stale lease publication, branch-rule bypass, audit tampering and recovery abuse. Verify exact trust boundaries and fail-closed behavior. Challenge whether systemd sandboxing is adequate for the stated pilot threat model and whether rootless containers are overstated. Identify missing controls and residual risks; classify P0–P2; provide adversarial test cases. Do not approve a design that relies only on coordinator-side checks when the side-effect broker can bypass them. Do not claim deployment or penetration testing without evidence.

你是 I 安全治理 Owner。检查实时 PR #31–#35。对 Webhook 伪造/重放、秘密窃取、Token 外泄、Prompt Injection、不可信 PR 执行、路径穿越、Worker 逃逸、旧租约发布、分支规则绕过、审计篡改和恢复滥用进行威胁建模。核验信任边界与失败关闭；质疑 systemd Sandbox 是否足以覆盖试点威胁模型及 Rootless Container 的安全表述。输出 P0–P2 Finding 和对抗测试。不得接受仅由 Coordinator 检查、而副作用 Broker 可绕过的设计。无证据不得声称部署或渗透测试。

## 6. Storage/Consistency review prompt / Storage/Consistency 审查提示词

Inspect ADR-RUN-001 and runtime-data-model-and-migration-contract.md at live PR heads. Reconcile TX-01..TX-08 with actual candidate database semantics. Explicitly analyze unique constraints under concurrency, transaction isolation, atomic claim/fencing, heartbeat expiry, work supersession, outbox uncertainty, migration crash recovery, backup/restore, retention and audit consistency. Do not choose SQLite/PostgreSQL by preference. Produce a physical schema only after ADR-RUN-001's benchmark inputs are answered. List unprovable invariants and the exact fault-injection tests needed.

检查 ADR-RUN-001 与 Runtime 数据模型，按真实候选数据库语义核验 TX-01..TX-08。分析并发唯一约束、隔离级别、Claim/Fencing 原子性、Heartbeat 过期、Work Supersession、Outbox 不确定结果、Migration 崩溃恢复、备份恢复、保留和审计一致性。不得凭偏好选 SQLite/PostgreSQL。只有 ADR-RUN-001 的基准输入得到回答后才提出物理 Schema。列出无法证明的不变量及精确故障注入测试。

## 7. Testing/Quality review prompt / 测试质量审查提示词

Inspect all runtime ADRs and the logical data model. Convert each acceptance test ID (DB-01..DB-14, GH-01..GH-20, ISO-01..ISO-14, EVT-01..EVT-12, AUTH-01..AUTH-14, BR-01..BR-10, RM-01..RM-15, RT-01..RT-15) into a traceable conformance matrix. Identify tests that are vague, non-deterministic, unautomatable or lack a measurable oracle. Specify race/fault injection, exact-SHA fixtures, test doubles vs real GitHub test installation, CI check names and evidence format. Do not mark tests passed until executable tests and logs exist.

检查全部 Runtime ADR 和逻辑数据模型，将各测试 ID 转成可追踪一致性矩阵。识别模糊、非确定、不可自动化或缺乏可测 Oracle 的测试。明确竞争/故障注入、精确 SHA Fixture、Mock 与真实测试 Installation、CI Check Name 和证据格式。可执行测试与日志不存在时不得标记通过。

## 8. Pilot Owner review prompt / 试点 Owner 审查提示词

Act as the selected low-risk Owner. Review the proposed read-only pilot workflow, prompt digest binding, work eligibility, stop conditions, evidence output and escalation behavior. Identify ambiguous instructions, missing inputs, unsafe assumptions and any action that exceeds your domain authority. Accept only a bounded read-only task with a measurable result and no secrets or write credentials.

你作为选定低风险 Owner，审查只读试点流程、Prompt Digest 绑定、工作资格、停止条件、证据输出和升级行为。指出模糊指令、缺失输入、不安全假设及超越领域权限的操作。仅接受有界、可度量、不含秘密或写凭据的只读任务。

## 9. Review result template / 审查结果模板

Each reviewer must publish reviewer role and identity; exact PR numbers and live head SHAs; reviewed files and excluded files; verdict (PASS / CONDITIONAL PASS / REQUEST CHANGES / BLOCKED); findings with severity, evidence and owner; test environment and evidence; unresolved risks and explicit non-claims; and whether a new commit invalidated the review.

每位审查者必须发布角色/身份、PR 和实时 SHA、文件范围、结论、Finding/严重度/证据/责任人、测试环境/证据、未决风险/禁止推断，以及新 Commit 是否使审查失效。

## 10. Current status / 当前状态

No independent reviews or approvals are recorded by this package. PRs #31–#35 remain draft design proposals. The repository administrator has not supplied current branch-protection evidence. The remote runner remains operator-confirmed only; no runtime deployment or 24/7 operation is claimed.
