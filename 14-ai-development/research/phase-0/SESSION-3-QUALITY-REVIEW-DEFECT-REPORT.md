# AI-DEV-OS-001 — Session 3: Engineering Quality, Independent Review & Defect Intelligence
# AI-DEV-OS-001 — 会话 3：工程质量、独立审查与缺陷智能管理

**Document ID:** AI-DEV-OS-001-SESSION-3  
**Report Version:** 1.1 — Session 0 revision  
**Phase:** Phase 0 — Research Publication  
**Status:** RESEARCH FINDINGS — PROPOSED; NOT A NORMATIVE APPROVAL  
**Repository:** oahcom/AiMemoryBrainArchitecture  
**Research Role:** Principal Engineering Quality, Independent Review & Defect Intelligence Research Owner  
**Research Baseline:** main at 4bee3e886cc0dec4a8d03817acd180ba979f8ceb  
**Publication Branch:** research/ai-dev-os-001-session-3  
**Publication Scope:** This report only; no architecture, runtime, infrastructure, governance-standard, or other Session files are changed.  
**Languages:** 简体中文 + English

---

## 1. Executive Summary / 执行摘要

### 中文

本研究审查 AI-DEV-OS-001 项目现有工程治理能力，重点覆盖工程质量门禁、独立审查、精确 Head 绑定、测试证据、缺陷生命周期、发现项关闭验证和迭代结束对账。

核心结论是：仓库已经具备可复用的治理基础，不应再建立一套平行的质量体系。AI-STD-001、AI-PROC-001 和 AI-TPL-001 已分别定义角色分离、DoR/DoD、风险等级、缺陷严重度、审查结论、迭代阶段、测试证据和任务清单。Phase 1 应以增量方式补齐可执行记录与状态转换，而不是重写现有规范。

当前最重要的缺口不是缺少更多原则性文字，而是缺少四种可跨会话、跨 PR 持续核验的结构化记录：

1. Work Item Manifest：冻结范围、Owner、风险、依赖、Prompt、Base/Head 和各 Gate 状态。
2. Test Evidence Record：将每次测试结果绑定到精确目标 SHA、命令、环境和限制。
3. SHA-bound Independent Review Record：将独立审查结论绑定到精确 PR Head，并保留历史审查。
4. Run Closeout Reconciliation：在每轮执行结束时，对发现项、Bug、Follow-up、未完成任务和风险逐项对账。

最低质量控制可用七个 Gate 检查项组织：Scope、Prompt Integrity、Implementation、Test、Review、Defect、Acceptance。必须保留 AI-STD-001 对 Finding Severity 的既有定义：BLOCKER、P0、P1、P2、P3 均属于 Finding Severity（发现项严重度）等级；Gate Disposition 则作为独立研究提案，使用 NOT_EVALUATED、PASS、BLOCKED、CONDITIONAL、NOT_APPLICABLE。BLOCKER 不得被重新定义为 Gate 状态。

仓库当前主要是架构与治理定义仓库，不是已经具备完整生产运行时实现的代码仓库。架构/文档验收、契约验收、参考模型验证、生产实现验证、生产一致性验证和部署验收必须分别陈述。参考模型测试通过不能被表述为生产运行时已通过。

本报告是 Phase 0 研究成果，不是已批准规范，也不授权 Phase 1 实施、修改现有标准、合并 PR 或部署生产系统。

### English

This research evaluates the existing engineering-quality governance of AI-DEV-OS-001, focusing on quality gates, independent review, exact-Head binding, test evidence, defect lifecycle, finding closure verification, and iteration closeout reconciliation.

The repository already contains reusable governance foundations. A parallel quality framework would create duplication and conflicting authority. AI-STD-001, AI-PROC-001, and AI-TPL-001 already define role separation, Definition of Ready/Done, risk classes, defect severity, review dispositions, lifecycle stages, test evidence, and work-item records. Phase 1 should strengthen these artifacts incrementally rather than replace them.

The main gap is operational traceability, not the absence of more principles. Four durable records are needed:

1. A Work Item Manifest freezing scope, Owner, risk, dependencies, prompt, Base/Head, and Gate states.
2. A Test Evidence Record binding every result to the exact target SHA, command, environment, and limitations.
3. A SHA-bound Independent Review Record binding a review disposition to the exact PR Head while preserving historical reviews.
4. A Run Closeout Reconciliation accounting for findings, bugs, follow-ups, unfinished tasks, and risks at the end of each run.

The minimum quality-control model may use seven Gate check dimensions: Scope, Prompt Integrity, Implementation, Test, Review, Defect, and Acceptance. Preserve the existing AI-STD-001 Finding Severity vocabulary: BLOCKER, P0, P1, P2, and P3 are Finding Severity levels. Gate Disposition is a separate proposed dimension using NOT_EVALUATED, PASS, BLOCKED, CONDITIONAL, or NOT_APPLICABLE. BLOCKER must not be redefined as a Gate state.

### Seven Gate dimensions mapped to the existing lifecycle / 七个 Gate 维度与既有生命周期映射

The seven proposed Gate dimensions are evidence/checklist views over the existing AI-STD-001 work-item lifecycle and AI-PROC-001 iteration stages. They are **not** a second lifecycle, independent state machine, or replacement for DoR/DoD. Existing lifecycle states and authorized transitions remain authoritative.

| Gate dimension | Existing lifecycle / process stage | DoR / DoD relationship | Accountable role | Minimum evidence |
|---|---|---|---|---|
| Scope | AI-STD-001 PROPOSED → ANALYZED; AI-PROC Stage 0–1 | DoR: outcome, non-goals, Owner, dependencies, acceptance criteria | Sponsor + accountable Owner | Work Item, impact/dependency map, scope and acceptance criteria |
| Prompt Integrity | PROMPT_READY; AI-PROC Stage 2 | DoR: versioned/reviewed prompt and exact source/base refs | Prompt author + prompt reviewer; Owner accountable | Prompt ID/version/hash, review record, source pins |
| Implementation | IN_PROGRESS → IMPLEMENTED; AI-PROC Stage 4 | DoD: scoped change, commit and changed paths | Accountable Owner | Branch, commit SHA, diff, self-check |
| Test | VERIFIED; AI-PROC Stage 5 | DoD: applicable checks executed; NOT RUN remains explicit | Testing/Quality + accountable Owner | Commands, environment, logs, exact tested SHA |
| Review | REVIEWED; AI-PROC Stage 6 | DoD: independent review and finding disposition | Independent Reviewer | Exact-Head review, independence disclosure, findings |
| Defect | Cross-cutting over VERIFIED/REVIEWED/INTEGRATION_READY/ACCEPTED; AI-PROC Stages 5–8 | DoD: findings resolved or explicitly accepted under authority; no silent closure | Finding Owner; Acceptance Authority for risk acceptance | Stable finding ID, severity, state history, closure proof or risk record |
| Acceptance | INTEGRATION_READY → ACCEPTED → MERGED → CLOSED; AI-PROC Stages 7–8 | DoD: integration, acceptance and traceability closeout | A/Integration Architect + designated Acceptance Authority | Owner boundary approvals, acceptance record, merge SHA, closeout |

Gate disposition is recorded independently from Finding Severity and lifecycle state. For example, a P1 Finding may exist while the Review Gate is FAIL and the work item lifecycle remains REVIEWED or BLOCKED; the finding must not be recoded as a Gate state. No Gate dimension may independently advance the lifecycle or bypass the existing transition/authority rules.

**七个 Gate 维度只是既有 AI-STD-001 工作项生命周期和 AI-PROC-001 迭代阶段上的证据/检查视图，**不是第二套生命周期、独立状态机，也不替代 DoR/DoD。现有生命周期状态和授权转换规则继续保持权威。

| Gate 维度 | 既有生命周期 / 流程阶段 | DoR / DoD 对应关系 | 责任角色 | 最低证据 |
|---|---|---|---|---|
| Scope 范围 | PROPOSED → ANALYZED；AI-PROC Stage 0–1 | DoR：目标、非目标、Owner、依赖、验收标准 | Sponsor + Accountable Owner | Work Item、影响/依赖图、范围与验收标准 |
| Prompt Integrity 提示词完整性 | PROMPT_READY；AI-PROC Stage 2 | DoR：提示词版本化、审查及准确来源/Base 引用 | Prompt 作者 + Prompt Reviewer；Owner 负责 | Prompt ID/版本/Hash、审查记录、来源固定点 |
| Implementation 实现 | IN_PROGRESS → IMPLEMENTED；AI-PROC Stage 4 | DoD：范围内变更、提交和变更路径 | Accountable Owner | 分支、Commit SHA、Diff、自检 |
| Test 测试 | VERIFIED；AI-PROC Stage 5 | DoD：执行适用检查；NOT RUN 必须如实记录 | Testing/Quality + Accountable Owner | 命令、环境、日志、准确测试 SHA |
| Review 审查 | REVIEWED；AI-PROC Stage 6 | DoD：独立审查和 Finding 处置 | Independent Reviewer | 精确 Head 审查、独立性披露、发现项 |
| Defect 缺陷 | 横跨 VERIFIED/REVIEWED/INTEGRATION_READY/ACCEPTED；AI-PROC Stage 5–8 | DoD：Finding 已解决或经授权明确接受；禁止静默关闭 | Finding Owner；风险接受由 Acceptance Authority 负责 | 稳定 Finding ID、严重度、状态历史、关闭证明或风险记录 |
| Acceptance 验收 | INTEGRATION_READY → ACCEPTED → MERGED → CLOSED；AI-PROC Stage 7–8 | DoD：集成、验收和可追溯关闭 | A/Integration Architect + 指定 Acceptance Authority | Owner 边界批准、验收记录、Merge SHA、收尾对账 |

Gate Disposition 必须与 Finding Severity 和生命周期状态分别记录。例如，某个 P1 Finding 存在时，Review Gate 可以为 FAIL，而 Work Item 生命周期仍处于 REVIEWED 或 BLOCKED；不得将 Finding 严重度改写为 Gate 状态。任何 Gate 维度都不能自行推进生命周期或绕过既有状态转换/授权规则。

The repository is primarily an architecture and governance definition repository, not a complete production runtime implementation repository. Architecture/documentation acceptance, contract acceptance, reference-model verification, production implementation verification, production conformance, and deployment acceptance must be reported separately. A passing reference-model test is not evidence that a production runtime has passed.

This is a Phase 0 research artifact. It is not an approved normative standard and does not authorize Phase 1 implementation, changes to existing standards, PR merges, or production deployment.

---

## 2. Document Metadata / 文档元数据

**Revision note / 修订说明:** Version 1.1 addresses Session 0 findings S0-S3-01 (preserve the existing AI-STD-001 BLOCKER severity definition) and S0-S3-02 (map all seven proposed quality-check dimensions to the existing AI-PROC-001 lifecycle and AI-STD-001 DoR/DoD). No normative source file is modified.

| Field | Value |
|---|---|
| Program | AI-DEV-OS-001 |
| Session | Session 3 — Engineering Quality, Independent Review & Defect Intelligence |
| Phase | Phase 0 — Research / Publication |
| Repository | oahcom/AiMemoryBrainArchitecture |
| Research baseline | main: 4bee3e886cc0dec4a8d03817acd180ba979f8ceb |
| Main baseline URL | https://github.com/oahcom/AiMemoryBrainArchitecture/commit/4bee3e886cc0dec4a8d03817acd180ba979f8ceb |
| Principal source standard | 14-ai-development/ai-development-standard.md |
| Lifecycle source | 14-ai-development/iteration-lifecycle.md |
| Prompt/evidence template | 14-ai-development/prompt-and-evidence-template.md |
| Governance invariant source | 00-governance/architecture-invariants.md |
| Research owner | Session 3 — Quality / Review / Defect Intelligence |
| Publication authority | Research artifact publication only |
| Approval state | PROPOSED; Session 0 and governance approval pending |

**Status vocabulary used in this report**

- **VERIFIED** — directly supported by a repository artifact, GitHub object, exact SHA, or other cited primary evidence.
- **PROPOSED** — a research recommendation, not an approved normative rule.
- **UNKNOWN** — the available evidence does not establish the fact.
- **NOT APPLICABLE** — the check does not apply to the stated target or artifact.
- **NOT RUN** — the required check was not executed; it is never equivalent to PASS.
- **HISTORICAL** — evidence remains valid only for the exact historical artifact/commit it names.

---

## 3. Research Scope and Method / 研究范围与方法

### 3.1 In scope / 研究范围

**中文**

本研究范围包括：

- 现有 AI 开发标准、迭代生命周期和 Prompt/Evidence 模板；
- 角色分离、Owner、Implementer、Reviewer、Integration Reviewer 和 Acceptance Authority 的职责边界；
- DoR、DoD、风险等级、严重度和审查结论；
- PR Head 更新后的审查有效性；
- 测试证据的身份、来源、范围和有效性；
- Finding 与 Bug 的登记、分派、修复、验证、关闭和延期；
- 条件通过与风险接受；
- Run 结束时的完整性对账；
- Phase 1 最小可验收记录结构。

本研究不重新设计业务架构，不修改模块 Owner 契约，不实施运行时、数据库、基础设施或自动化程序，也不代替 Session 0 作最终治理决策。

**English**

The scope covers:

- Existing AI development standards, iteration lifecycle, and Prompt/Evidence templates.
- Separation of duties among Owner, Implementer, Reviewer, Integration Reviewer, and Acceptance Authority.
- DoR, DoD, risk classes, defect severity, and review dispositions.
- Review validity after a PR Head changes.
- Identity, provenance, scope, and validity of test evidence.
- Finding and Bug registration, assignment, remediation, verification, closure, and deferral.
- Conditional approval and risk acceptance.
- Complete run-end reconciliation.
- Minimum record structures for Phase 1 acceptance.

The research does not redesign business architecture, amend module Owner contracts, implement runtime/database/infrastructure/automation, or replace Session 0 as the final governance decision authority.

### 3.2 Method / 方法

**中文**

采用只读证据审查：读取 main 的原始文件、Blob、GitHub PR 元数据和历史审查记录，并将作者声明与独立审查证据区分。重要状态以具体文件、Commit、PR、Head SHA 或 Review URL 表达。

对当前 PR 的判断仅针对实际读取的 Head。历史 Review 不会自动迁移到后续 Head。GitHub 的 mergeable 状态仅表示平台的合并冲突判断，不等于质量通过、授权接受或合并批准。

**English**

The method is read-only evidence review of main-branch source files, Git blobs, GitHub PR metadata, and historical review records. Author statements are distinguished from independent review evidence. Important status claims are tied to concrete files, commits, PRs, Head SHAs, or review URLs.

A PR assessment applies only to the Head actually inspected. Historical reviews do not automatically transfer to later Heads. GitHub's mergeable state is a platform merge-conflict signal, not quality approval, acceptance authorization, or merge permission.

### 3.3 Evidence limitations / 证据限制

This report is a bounded research audit, not a repository-wide re-review of every PR, every Issue, every commit, or every test run. The PR examples below are representative evidence cases. Any later operational decision must refresh the live GitHub baseline and re-read the exact target artifacts.

本报告属于有明确边界的研究审计，不是对仓库全部 PR、Issue、Commit 和测试运行的逐一重新审查。以下 PR 是代表性证据案例。后续任何工程决策均须刷新 GitHub 实时基线，并重新读取精确目标工件。

---

## 4. Current State / 当前状态

### 4.1 Repository and implementation boundary / 仓库与实现边界

**VERIFIED**

- Repository default branch is main.
- Research publication baseline is main commit 4bee3e886cc0dec4a8d03817acd180ba979f8ceb.
- The repository includes architecture, governance, testing guidance, engineering decisions, and AI development governance artifacts.
- Issue #7 records the boundary that the repository is an architecture/specification project and that production runtime implementation has not started in the reviewed baseline; a production src/tests/service implementation tree was not evidenced in the reviewed PR #72 baseline.

Evidence:
- Repository: https://github.com/oahcom/AiMemoryBrainArchitecture
- Main baseline: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/4bee3e886cc0dec4a8d03817acd180ba979f8ceb
- Issue #7: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7
- PR #72: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/72

**中文解释**

因此，不能用“生产测试通过”描述仅有架构文件、规范检查或抽象参考模型的证据。必须明确测试对象和证据上限。若测试对象是规范文档，应报告文档结构、双语一致性、引用有效性、Schema/YAML 解析或规范冲突检查；若生产实现尚不存在，则生产集成、并发、恢复、Adapter、数据库原子性和部署测试应标记 NOT RUN 或在确实不适用时标记 NOT APPLICABLE，并说明理由。

### 4.2 Existing governance artifacts / 现有治理文件

| Artifact | Current source identity | Verified capability |
|---|---|---|
| AI-STD-001 | Blob f46867f97fc1860015adbe2a1f7b8262640c16fd | Roles, DoR/DoD, R0–R3, BLOCKER/P0–P3, review dispositions, evidence expectations |
| AI-PROC-001 | Blob 8ecc8e4ddde78be01e2038be4ece8dc8ac282c97 | Iteration stages, automated verification, independent review, integration review, acceptance and closeout |
| AI-TPL-001 | Blob c9c545ae884991d2f5dd08c6880c50c97a13c143 | Work Item manifest, immutable prompt versioning, evidence bundle, test/review/acceptance references |
| Architecture invariants | Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe | System invariants and architectural constraints |

The source identities above are Blob SHAs read from the research baseline, not claims that these documents have already been approved as a complete operational quality system.

### 4.3 Representative PR evidence / 代表性 PR 证据

#### PR #42 — AID-2026-001 / ChatGPT-native execution proposal

- URL: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42
- Current Head at research review: 84d91b10e9069a575b479f6925d3b143757e82cb
- Base SHA reported by PR: b372b62c640a2b656e54b6db62a4ee67d7d8c001
- State: OPEN / DRAFT / NOT MERGED
- GitHub mergeable: true; this is not a quality approval.
- Current changed-file inventory reported in the PR: 35 files; Manifest changed_paths alignment 35/35.
- Current Head CI/workflow runs: 0; commit status checks: 0.
- YAML parser, schema validation, and full Manifest validation: NOT RUN.
- Owner D/I specialist reports: NOT EVIDENCED.
- Reproducible R3 contract tests: NOT RUN.
- Distinct Integration Review: PENDING.
- Acceptance: BLOCKED / PENDING; merge not authorized.

Historical review:
- Review URL: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42#pullrequestreview-5937629228
- Review Head: 1d6ab39375136d8649235feebeb6232609001222
- Historical disposition: FAIL for that historical Head only.

**Conclusion:** the historical FAIL must remain visible, but it is not a review of current Head 84d91b10e9069a575b479f6925d3b143757e82cb. A new independent review is required for the current Head. Author remediation statements are not independent verification.

#### PR #72 — joined Forget lifecycle and governance proposal

- URL: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/72
- Head: 3bd943ad6ef2acf55a48e23e6b4cba92fdd3ada0
- Base branch: design/chatgpt-native-execution-model
- Base SHA reported by PR: 4f8c5218c8d33f5fdb690a7c4bdb671639ebb807
- State: OPEN / DRAFT / NOT MERGED.
- Proposal status: D/I approval pending; E/F/G/H/C acknowledgements pending; Storage/Backup accountable operator assignment and acknowledgement pending.
- Reference model: 14/14 unit tests PASS under Python 3.13.5, as reported in the PR evidence.
- Production R3 / DFI-001…DFI-022 tests: NOT RUN / NOT EVIDENCED.
- Current-head CI/workflow runs and commit statuses: none returned in the PR evidence.
- The reference model is in-memory and does not exercise database atomicity, real concurrency, queues, indexes, adapters, replicas, or backup media.
- The PR records that its reviewed base tree had no production src/tests/package/service implementation tree.

**Conclusion:** 14/14 reference-model tests are evidence for that bounded model and its exact source/test inputs only. They are not proof of production runtime correctness or cross-system conformance.

### 4.4 Issue and governance references / Issue 与治理依据

- Issue #3 — formal decision mechanism: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/3
- Issue #7 — repository/project boundary: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7
- Issue #41 — AID-2026-001 Work Item: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/41

---

## 5. Existing Capabilities / 已有能力

### 5.1 Role separation / 角色分离

**VERIFIED:** AI-STD-001 §3.2 states that an author/implementer cannot be the sole reviewer or acceptance authority. It distinguishes Owner, Implementer, Reviewer, Integration Reviewer, and Acceptance Authority responsibilities.

**Implication:** the project already has the principle needed to prevent self-approval. Phase 1 should make the role identities and evidence mandatory in the Work Item and Review records.

### 5.2 Definition of Ready and Definition of Done / 就绪与完成定义

**VERIFIED:** AI-STD-001 defines DoR and DoD. AI-PROC-001 describes intake, dependency analysis, prompt review, readiness, implementation, verification, independent review, integration review, acceptance, merge, and closeout.

**Implication:** quality gates should map to existing lifecycle stages. Avoid introducing a second lifecycle with competing state names.

### 5.3 Risk and severity / 风险与严重度

**VERIFIED:** existing standard uses R0–R3 risk classes, BLOCKER, and P0–P3 finding severities. Review dispositions include PASS, CONDITIONAL PASS, FAIL, and NOT REVIEWABLE.

**Implication:** retain these terms. Clarify their dimensions and transition rules instead of replacing them.

### 5.4 Prompt and evidence provenance / Prompt 与证据来源

**VERIFIED:** AI-TPL-001 provides a Work Item manifest with prompt ID/version/SHA-256, Base SHA, dependencies, implementation commits, changed paths, verification status/commit, review status/report, findings, acceptance, and merge references. It also requires immutable prompt versions and an evidence bundle.

**Implication:** the proposed Work Item Manifest is an extension/normalization of AI-TPL-001, not a competing record system.

### 5.5 Independent review and integration review / 独立审查与集成审查

**VERIFIED:** AI-PROC-001 requires a reviewer distinct from the implementer, gives the reviewer the approved prompt, task record, Base/implementation SHAs, diff, test evidence, and contracts, and requires cross-owner integration review where applicable.

**Implication:** the missing capability is a durable, SHA-specific review record with invalidation rules and complete finding reconciliation.

### 5.6 Recovery and iteration learning / 失败恢复与迭代学习

**VERIFIED:** AI-PROC-001 requires preserving failed-run prompts, branches, commits, logs, and findings; classifying failure; avoiding force-push evidence loss; and recording retrospective metrics.

**Implication:** Run Closeout should formalize this existing expectation and make it machine-checkable where practical.

---

## 6. Missing Capabilities / 缺失能力

The following gaps are research findings and proposed capabilities, not statements that the existing standards contain no related principles.

| ID | Priority | Missing operational capability | Required outcome |
|---|---|---|---|
| MC-001 | P1 | Explicit seven-Gate record | One current state and evidence pointer per Gate |
| MC-002 | P1 | Immutable review identity | Reviewer, role, exact Head SHA, scope, disposition, timestamp, report |
| MC-003 | P1 | Review invalidation on Head change | Previous review becomes HISTORICAL for the new Head |
| MC-004 | P1 | Test evidence identity | Test ID, target SHA, command, environment, result, evidence link |
| MC-005 | P1 | NOT RUN / BLOCKED semantics | Unexecuted tests cannot be treated as PASS |
| MC-006 | P1 | Finding registry schema | Stable ID, severity, evidence, owner, state, closure criteria |
| MC-007 | P1 | Independent closure verification | RESOLVED is not CLOSED until evidence is checked |
| MC-008 | P1 | Run-end reconciliation | Every finding, Bug, follow-up and unfinished task is accounted for |
| MC-009 | P1 | Acceptance authority record | Explicit person/role and scope of acceptance |
| MC-010 | P1 | Conditional approval contract | Owner, expiry/deadline, risk rationale, restrictions and tracking link |
| MC-011 | P1 | Evidence freshness rules | Evidence validity tied to source SHA and tested target |
| MC-012 | P2 | Duplicate finding reconciliation | Deduplication by invariant, failure condition and root cause |
| MC-013 | P2 | Cross-PR defect linkage | One Bug can link multiple affected Work Items/PRs |
| MC-014 | P2 | Risk-based test selection matrix | R0–R3 requirements map to deterministic test obligations |
| MC-015 | P2 | Finding trend metrics | Escape rate, reopen rate, severity aging, repeated root causes |
| MC-016 | P2 | Reviewer limitation disclosure | Conversation/model/provider independence limitations recorded |
| MC-017 | P2 | Evidence link health and retention | Durable references, unavailable evidence state, immutable history |

### 中文说明

这些缺口应优先以模板字段、记录约束、状态转换和验收检查补齐。不要先引入数据库、服务、复杂自动化或新的治理委员会。若已有文件已经表达某项规则，Phase 1 应链接并复用原文，不应重复复制成第二份规范。

### English explanation

These gaps should first be addressed through template fields, record constraints, state transitions, and acceptance checks. Do not begin by introducing a database, service, complex automation, or a new governance committee. Where an existing document already expresses a rule, Phase 1 should reference and reuse it rather than duplicating it in a second standard.

---

## 7. Proposed Architecture / 建议架构

**Status: PROPOSED — requires Session 0 synthesis and governance approval.**

### 7.0 Session 0 revision findings and correction traceability / Session 0 复审发现与修订追踪

#### S0-S3-01 — Preserve the existing BLOCKER severity / 保留既有 BLOCKER 严重度定义

- **Original proposal (superseded) / 原提案（现已废止）：** The earlier wording stated: “BLOCKER is a Gate disposition, not a severity level.” This reclassified an existing AI-STD-001 term.
- **Existing authoritative definition / 既有权威定义：** AI-STD-001 §9 defines Finding Severity as **BLOCKER** = “unsafe, incorrect, or prevents integration”; **P0** = critical invariant/security/data-integrity defect; **P1** = major contract or correctness gap; **P2** = important quality or maintainability issue; **P3** = minor improvement.
- **Conflict analysis / 冲突分析：** Treating BLOCKER as a Gate disposition silently changes the existing Finding Severity vocabulary and collapses defect impact with progression status. This conflicts with the source definition and makes historical findings ambiguous.
- **Corrected proposal / 修正提案：** Preserve BLOCKER/P0/P1/P2/P3 as the existing Finding Severity vocabulary. Introduce a separate **proposed, non-normative Gate Disposition** dimension: NOT_EVALUATED, PASS, BLOCKED, CONDITIONAL, NOT_APPLICABLE. A finding may have severity BLOCKER while its affected Gate disposition is BLOCKED. Never use BLOCKER as a Gate state. Keep AI-STD-001 Review Disposition (PASS, CONDITIONAL PASS, FAIL, NOT REVIEWABLE) and test outcomes (PASS, FAIL, NOT RUN, BLOCKED, NOT APPLICABLE) distinct.
- **Lifecycle mapping / 生命周期映射：** Severity belongs to the Finding record raised during verification/review and carried through remediation, verification, integration and acceptance (AI-PROC-001 Stages 5–8). Gate Disposition is only a proposed checklist result attached to an existing stage; it does not replace or add Work Item lifecycle states.
- **Evidence source / 证据来源：** `14-ai-development/ai-development-standard.md` §9, current main `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`, Blob `f46867f97fc1860015adbe2a1f7b8262640c16fd`; `14-ai-development/iteration-lifecycle.md` §§2 and 5, same main SHA, Blob `8ecc8e4ddde78be01e2038be4ece8dc8ac282c97`.
- **Governance status / 治理状态：** Existing severity vocabulary and exact definition: **VERIFIED**. Separate Gate Disposition values: **PROPOSED**, not adopted. AI-STD-001 is the terminology source for this research; this report does not amend it or claim a new formal adoption decision.

**中文说明：** 原表述把 BLOCKER 从既有缺陷严重度中移走，属于未经授权的术语重定义。本次恢复 AI-STD-001 §9 原义，并将 Gate Disposition 作为独立研究提案。BLOCKER 描述 Finding 严重程度；BLOCKED 描述某个检查点当前不能放行。两者可以同时成立，但不可互换。本修正仅调整研究报告，不修改规范。

#### S0-S3-02 — Map seven proposed Gates to the existing lifecycle / 将七项建议 Gate 映射到既有生命周期

- **Original proposal / 原提案：** Seven quality Gates were listed without a complete clause-level mapping to the existing lifecycle and DoR/DoD, and without consistently identifying stage, decision authority and governance status.
- **Existing authoritative model / 既有权威模型：** AI-PROC-001 §2 defines Stage 0 Intake and registration, Stage 1 Impact and dependency analysis, Stage 2 Prompt drafting and review, Stage 3 Readiness gate, Stage 4 AI implementation, Stage 5 Automated verification, Stage 6 Independent AI review, Stage 7 Cross-owner integration review, and Stage 8 Acceptance, merge and closeout. AI-PROC-001 §5 already defines release checkpoints G0–G7. AI-STD-001 §§4.1, 7–9 define Work Item states, DoR/DoD, verification and review/acceptance; AI-TPL-001 defines Manifest and evidence fields.
- **Conflict analysis / 冲突分析：** Adding seven independent Gate states would duplicate AI-PROC-001 stages, existing release checkpoints G0–G7 and AI-STD-001 Work Item states. This risks a second state machine, duplicated Issue Labels/status fields and competing progression authority.
- **Corrected proposal / 修正提案：** Treat G-SCOPE, G-PROMPT, G-IMPLEMENTATION, G-TEST, G-REVIEW, G-DEFECT and G-ACCEPTANCE solely as **evidence/checklist dimensions inside the existing lifecycle**. Map each to existing stages, G0–G7 checkpoints, DoR/DoD clauses, Owners, evidence and decision authority below. Add no lifecycle state, duplicate Issue Label or parallel state machine.
- **Lifecycle mapping / 生命周期映射：** The complete mapping is in §7.3. Where an exact decision right or canonical artifact is not established by the sources, it is marked UNKNOWN or PROPOSED rather than invented.
- **Evidence source / 证据来源：** `14-ai-development/iteration-lifecycle.md` §§2 and 5, current main `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`, Blob `8ecc8e4ddde78be01e2038be4ece8dc8ac282c97`; `14-ai-development/ai-development-standard.md` §§4.1 and 5–9, Blob `f46867f97fc1860015adbe2a1f7b8262640c16fd`; `14-ai-development/prompt-and-evidence-template.md` §§1 and 4, Blob `c9c545ae884991d2f5dd08c6880c50c97a13c143`.
- **Governance status / 治理状态：** Existing lifecycle, states, DoR/DoD and G0–G7 checkpoints: **VERIFIED as source content**. Seven named quality-check dimensions and this crosswalk: **PROPOSED**. No normative amendment or new lifecycle state is created.

**中文说明：** 七项 Gate 不是新的流程阶段，也不是七个新的 Work Item 状态。它们只是把已有阶段中的证据要求组织成可复核的检查清单。AI-PROC-001 已有 Stage 0–8 和发布检查点 G0–G7，必须映射和复用，而不是另建一套状态机。

### 7.1 Seven proposed quality-check dimensions / 七项建议质量检查维度

**Architectural rule / 架构规则**

The seven Gates are evidence and checklist dimensions within the existing AI-PROC-001 lifecycle. They are not a replacement lifecycle, not a parallel state machine, and not additional Work Item states. Existing lifecycle transitions and decision rights remain unchanged unless a formal governance decision explicitly authorizes an amendment.

七项 Gate 仅是既有 AI-PROC-001 生命周期中的证据与检查清单维度，不是替代生命周期，不是并行状态机，也不是新增 Work Item 状态。除非治理机构正式批准修订，否则既有生命周期转换和决策权保持不变。

| Proposed Gate ID / 建议 Gate ID | Gate name / 名称 | Check type / 检查类型 | Existing lifecycle stage(s) / 既有阶段 | Existing AI-PROC-001 release checkpoint(s) / 既有发布检查点 | DoR/DoD clause / 条款锚点 | Responsible Owner / 责任角色 | Required evidence / 必需证据 | Decision authority / 决策权 | Blocking conditions / 阻断条件 | Status / 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| G-SCOPE | Scope and authority / 范围与授权 | Entry check / 入口检查 | Stage 0 Intake; Stage 1 Impact and dependency analysis | G0 Task valid; G1 Contract ready | AI-STD-001 §7 DoR: outcome/non-goals, accountable Owner, contracts/base SHAs, dependencies, testable acceptance criteria, impact classification | Sponsor and accountable Owner | Existing: Work Item identity and Owner fields in AI-TPL-001 §1. Proposed consolidation: bounded in/out scope, impact/dependency map, acceptance criteria and source SHAs | Accountable Owner confirms readiness; Sponsor confirms objective/scope where applicable. Any unassigned authority is UNKNOWN until recorded in the Work Item. | Missing accountable Owner/authority; undefined outcome or scope; unsafe unresolved dependency; untestable acceptance criteria | Existing stages/checkpoint: VERIFIED. Named Gate checklist: PROPOSED. |
| G-PROMPT | Prompt integrity / 提示词完整性 | Entry check / 入口检查 | Stage 2 Prompt drafting and review; Stage 3 Readiness gate | G1 Contract ready | AI-STD-001 §5 prompt controls; §7 DoR: prompt stored, versioned and reviewed; no unresolved blocker makes safe work impossible | Prompt author and distinct prompt reviewer; accountable Owner remains accountable | Existing: AI-TPL-001 prompt ID/version/hash, base/dependency refs, verification plan and evidence bundle. Proposed: explicit frozen-run-input/readback check. | Prompt reviewer verifies prompt quality; accountable Owner confirms PROMPT_READY/READY. Prompt reviewer is not automatically the implementation reviewer. | Executed prompt/version/hash unknown; authority or file boundaries conflict; material prompt drift; critical assumptions unresolved | Existing stages/checkpoint: VERIFIED. Named Gate checklist: PROPOSED. |
| G-IMPLEMENTATION | Implementation traceability / 实施可追溯性 | Execution check / 执行检查 | Stage 4 AI implementation | G2 Implementation complete | AI-STD-001 §6 branch/change discipline; §7 DoD: code/docs match approved prompt and scope; commit SHA and changed paths recorded | Implementing AI under the accountable Owner | Existing: implementation branch, commit list, changed paths, readback and self-check in AI-TPL-001 §1 and §4. Proposed: explicit scope-diff reconciliation. | Implementing Owner records IMPLEMENTED evidence; accountable Owner controls Work Item transition under the existing process. | Untraceable Base/Head/commit; unauthorized or out-of-scope files; invariant breach; missing readback or unexplained deviation | Existing stage/checkpoint: VERIFIED. Named Gate checklist: PROPOSED. |
| G-TEST | Verification and test evidence / 验证与测试证据 | Verification check / 验证检查 | Stage 5 Automated verification | G3 Verification passed | AI-STD-001 §7 DoD: applicable formatting/lint/build/type checks, unit/integration/contract/regression and failure-path tests; §8 layered verification and exact-commit evidence | Test/verification owner executes checks; implementation Owner remains accountable for complete evidence | Existing: AI-TPL-001 verification status, commit SHA, commands and evidence_refs; §4 test-report bundle. Proposed: complete environment/fixture/expected-vs-actual evidence where template fields are absent. | Verification owner reports results; accountable Owner confirms required evidence is complete. Required-check pass criteria remain governed by existing task/risk acceptance criteria. | Required test FAIL; required test NOT RUN/BLOCKED; result not bound to candidate SHA; missing command/environment/fixture or unverifiable output | Existing stage/checkpoint and test outcomes: VERIFIED. Additional structured Gate record: PROPOSED. |
| G-REVIEW | Independent review / 独立审查 | Review check / 审查检查 | Stage 6 Independent AI review | G4 Independent review | AI-STD-001 §3.2 role separation; §9 review dimensions, Finding fields and review dispositions | Independent Reviewer distinct from implementer; specialist reviewers when risk requires | Existing: review report, exact Base/Head, reviewer identity, findings and disposition. Proposed: explicit independence disclosure and exact-Head attestation if not captured in the current record. | Independent Reviewer issues review disposition; Acceptance Authority retains final acceptance authority. Reviewer does not self-accept implementation. | No distinct reviewer; stale/non-matching Head; NOT REVIEWABLE; required review findings unresolved without authorized risk acceptance | Existing stage/checkpoint and review disposition: VERIFIED. Additional Gate checklist: PROPOSED. |
| G-DEFECT | Finding and Bug reconciliation / 发现项与 Bug 对账 | Cross-stage verification/closeout check / 跨阶段验证与收尾检查 | Findings arise in Stage 5–7 and are resolved/reconciled before Stage 8 closeout | Cross-cuts G4 Independent review, G5 Integration accepted and G6 Merge authorized; no one-to-one existing release Gate | AI-STD-001 §9: Finding Severity, ID, evidence, owner, status and closure condition; §7 DoD: review findings resolved or explicitly accepted as residual risk | Finding Owner; distinct verifier for required closure; affected Owner for domain remediation | Existing: Finding fields and review/evidence references. Proposed: canonical Finding/Bug reconciliation ledger and RESOLVED→VERIFIED→CLOSED evidence chain if not already represented in Work Item/Issue. | Finding Owner proposes remediation; distinct verifier verifies; authorized Acceptance Authority decides residual-risk acceptance. Authority for additional automated state transitions is UNKNOWN and is not proposed here. | Open BLOCKER or P0; P1 classified as blocking under the proposed §7.9 policy; missing owner/evidence/closure condition; unresolved critical finding; unauthorized or expired residual-risk acceptance | Existing Finding vocabulary/fields: VERIFIED. P1 blocking default and canonical reconciliation checklist: PROPOSED, not existing AI-STD-001 norm. |
| G-ACCEPTANCE | Integration and acceptance / 集成与验收 | Integration/review/closeout check / 集成、审查与收尾检查 | Stage 7 Cross-owner integration review; Stage 8 Acceptance, merge and closeout | G5 Integration accepted; G6 Merge authorized; G7 Release ready only when release is in scope | AI-STD-001 §4.1 lifecycle transitions; §7 DoD: integration and acceptance authority explicitly accept; §9 conditional review restrictions | Affected module Owners; Integration Architect; authorized Acceptance Authority | Existing: integration report, affected-Owner approvals, contract registry, acceptance record, merge SHA; release/rollback evidence only when applicable | Affected Owners decide contract boundaries; Integration Architect reconciles integration conflicts; Acceptance Authority makes acceptance decision. Merge follows existing authorization; no Gate grants merge authority by itself. | Missing affected-Owner approval; incompatible contracts; unmet required checks; unresolved BLOCKER/P0 or P1 classified as blocking under proposed §7.9 policy; missing acceptance authority/record; release evidence missing when release is in scope | Existing stages/checkpoints: VERIFIED. Seven-Gate checklist overlay and P1 blocking default: PROPOSED. |

**Status interpretation / 状态解释**

- **VERIFIED** means the cited source stage, lifecycle state, DoR/DoD clause, or evidence field exists in the current source file. It does not mean the governance document has been formally adopted or that every repository Work Item complies.
- **PROPOSED** means the named Gate/checklist organization or additional record is a research recommendation only.
- **UNKNOWN** means the current source does not establish a precise decision right, owner assignment, or canonical artifact; the Work Item must identify it before relying on it.
- The seven Gates are checklists only. They do not add states to the AI-STD-001 Work Item lifecycle, and they must not be duplicated as new Issue Labels or parallel status fields.

**状态解释**

- **VERIFIED** 表示当前源文件中确实存在相应阶段、生命周期状态、DoR/DoD 条款或证据字段；不表示规范已被正式采纳，也不表示所有 Work Item 均已遵守。
- **PROPOSED** 表示七项 Gate/检查清单的组织方式或新增记录建议，尚未成为规范。
- **UNKNOWN** 表示当前源文件未明确某项决策权、Owner 分配或规范化证据载体；在依赖该项之前必须在 Work Item 中明确记录。
- 七项 Gate 仅为检查清单，不增加 AI-STD-001 Work Item 生命周期状态，不得复制为新的 Issue Label 或并行状态字段。

### 7.2 Finding severity and Gate disposition are independent dimensions / Finding 严重度与 Gate 处置是独立维度

| Dimension / 维度 | Values / 值 | Meaning and authority / 含义与依据 |
|---|---|---|
| Finding Severity / Finding 严重度 | **BLOCKER / P0 / P1 / P2 / P3** | Existing AI-STD-001 §9 vocabulary. BLOCKER = unsafe, incorrect, or prevents integration. This is the authoritative source vocabulary for this research. |
| Gate Disposition / Gate 处置 | **NOT_EVALUATED / PASS / BLOCKED / CONDITIONAL / NOT_APPLICABLE** | **PROPOSED only.** Checklist result for whether the relevant existing-stage evidence supports progression. Not an adopted standard and not a Work Item lifecycle state. |
| Review Disposition / Review 审查结论 | **PASS / CONDITIONAL PASS / FAIL / NOT REVIEWABLE** | Existing AI-STD-001 §9 review conclusion; do not collapse it into Finding Severity or Gate Disposition. |
| Test Result / 测试结果 | **PASS / FAIL / NOT RUN / BLOCKED / NOT APPLICABLE** | Existing DoD/verification semantics; each result is bound to its exact test target and evidence. |
| Work Item State / Work Item 状态 | **PROPOSED / ANALYZED / PROMPT_READY / READY / IN_PROGRESS / IMPLEMENTED / VERIFIED / REVIEWED / INTEGRATION_READY / ACCEPTED / MERGED / CLOSED; plus BLOCKED / REJECTED** | Existing AI-STD-001 §4.1–4.2 lifecycle vocabulary. Do not add Gate states to this list. |

A Finding with severity **BLOCKER** may cause the affected Gate to have disposition **BLOCKED**. This does not convert BLOCKER into a Gate status. A test result of FAIL is a test outcome; a review disposition of FAIL is a review conclusion; the proposed Gate disposition records whether progression is blocked. NOT_EVALUATED means the checklist has not yet been evaluated, not that the check passed. CONDITIONAL is limited to a non-blocking condition with documented restrictions and authorized risk acceptance. NOT_APPLICABLE requires an explicit reason and authorized scope.

**中文说明：** Finding Severity 描述问题本身的严重程度；Gate Disposition 描述某个既有阶段的证据是否允许继续。BLOCKER 可以导致 Gate=BLOCKED，但不能把 BLOCKER 写入 Gate 状态集合。测试 FAIL、Review FAIL 与 Gate BLOCKED 也是不同语义。Gate Disposition 全部属于研究提案，不构成规范修改。

### 7.3 Gate-to-lifecycle and DoR/DoD crosswalk / Gate—生命周期及 DoR/DoD 对照表

The table in §7.1 is the complete crosswalk. The following rules govern its interpretation:

1. A Gate is an entry, execution, verification, review, integration, or closeout **check on an existing stage**, not a new stage.
2. The existing AI-PROC-001 Stage 0–8 sequence remains the only lifecycle sequence described by this report.
3. AI-PROC-001 §5 already contains release checkpoints G0–G7. The seven proposed quality checks map onto those checkpoints as shown above; G-DEFECT is deliberately cross-cutting and has no invented one-to-one G0–G7 equivalent.
4. Existing Work Item state transitions remain those in AI-STD-001 §4.1–4.2. No new Gate state, Issue Label, or parallel state machine is introduced.
5. Where a source does not define an authority or artifact precisely, the mapping marks it UNKNOWN/PROPOSED; it does not invent a new governance role.
6. If governance later decides that a separate Gate state machine is necessary, that requires an explicit governance amendment and impact analysis across AI-STD-001, AI-PROC-001, AI-TPL-001 and GitHub labels/status fields.

**中文解释：** §7.1 已给出七项 Gate 的完整映射。Gate 仅检查既有阶段的进入条件、执行结果、验证证据、独立审查、跨 Owner 集成和收尾结果。AI-PROC-001 的 Stage 0–8 与 G0–G7 保持不变；AI-STD-001 的 Work Item 状态保持不变。若未来确需单独状态机，必须走正式治理修订流程，评估标准、流程、模板和 GitHub 状态字段的整体影响。

### 7.4 SHA-bound review model / SHA 绑定审查模型

Every review record MUST identify:

- Repository and PR number.
- Base branch and exact Base SHA.
- Exact PR Head SHA reviewed.
- Changed-file inventory and review scope.
- Reviewer identity and role.
- Whether the reviewer participated in implementation.
- Independence limitation disclosure.
- Contracts and source SHAs inspected.
- Tests/evidence inspected and their target SHAs.
- Findings and their stable IDs.
- Review disposition and rationale.
- Timestamp and report URL.

**Head-change rule**

If the PR Head changes after review, the prior review remains historical evidence for its original SHA. It is not current review evidence for the new Head. The PR must receive a new review against the new Head. The reviewer must inspect the new diff and determine impact; a claim that the change is documentation-only does not automatically preserve the previous review.

No historical FAIL may be overwritten or silently relabeled as PASS. A later PASS is a new review record for a new exact Head and must link to the prior finding/remediation history.

### 7.5 Reviewer independence model / Reviewer 独立性模型

Minimum independence:

1. Reviewer did not author or implement the change under review.
2. Reviewer uses a fresh, separate review context.
3. Reviewer independently retrieves the exact PR Head, source contracts, diff, and evidence from GitHub.
4. Reviewer does not treat author narrative as proof.
5. Reviewer actively searches for counterexamples, missing negative tests, race windows, scope leaks, stale-state behavior, compatibility breaks, and hidden assumptions.
6. Reviewer records limitations.

A separate ChatGPT conversation provides conversation/context isolation only. It does not prove model, provider, runtime/environment, or statistical independence and must not be called multi-model consensus. R3 specialist review and reproducible tests remain mandatory where required by the standard.

### 7.6 Test Evidence Record / 测试证据记录

Each test record should contain:

- Test ID and purpose.
- Test class: documentation, static, unit, integration, contract, security, concurrency, recovery, performance, deployment, or other named type.
- Exact target commit SHA.
- Source/test file SHAs where relevant.
- Command or workflow identifier.
- Environment and tool/runtime versions.
- Start/end time and execution identity.
- Result: PASS, FAIL, NOT RUN, BLOCKED, or NOT APPLICABLE.
- Expected and actual outcome.
- Failed tests and unexecuted tests.
- Failure or non-execution reason.
- Logs/artifact/CI URL.
- Coverage and limitations.
- Reviewer/Owner interpretation where required.

A test result is evidence only for the target and scope it actually exercised. Results from a different SHA are not current-Head evidence unless the equivalence is explicitly demonstrated and accepted. NOT RUN and BLOCKED are never PASS.

### 7.7 Defect and Finding lifecycle / 缺陷与发现项生命周期

Proposed lifecycle:

DISCOVERED → REGISTERED → TRIAGED → ASSIGNED → RESOLVED → VERIFIED → CLOSED

Additional terminal or controlled states may include DUPLICATE, REJECTED, DEFERRED, and BLOCKED, each with rationale and linkage.

Required Finding fields:

- Unique stable ID (for example, QF-2026-001).
- Title and failure condition.
- Severity P0–P3 and Gate impact.
- Affected invariant, contract, file, Work Item, PR, and exact SHA.
- Reproduction/evidence references.
- Root cause or current hypothesis, clearly distinguished.
- Accountable Owner and assignee.
- Remediation plan and due/expiry condition.
- Verification criteria and verifier.
- Current state and state-transition history.
- Related/duplicate findings and downstream impacts.
- Risk acceptance reference if deferred or conditionally accepted.

**Closure rule**

RESOLVED means the author claims remediation is complete. VERIFIED means a distinct verifier checked the fix against the stated closure criteria and exact evidence. CLOSED means the authorized process accepted that verification and all required follow-ups are reconciled. A PR author cannot close their own critical finding solely by changing its status or asserting it is fixed.

### 7.8 Run Closeout Reconciliation / Run 结束对账

Every run must reconcile:

- Original scope and acceptance criteria.
- All expected and actual changed paths.
- All findings discovered, registered, resolved, verified, closed, deferred, blocked, rejected, or duplicated.
- All Bugs and linked Issues/PRs.
- All follow-ups and unfinished subtasks.
- All failed, blocked, and unrun tests.
- All architecture/security/privacy risks and unresolved assumptions.
- All upstream/downstream dependencies and affected Work Items.
- All decisions requested, accepted, rejected, or pending.
- All evidence links and exact SHAs.
- Final Gate and Work Item state.

For each registered Finding, exactly one current state must be recorded. Reconciliation invariant:

Registered Findings = Closed + Open + Deferred + Blocked + Rejected + Duplicate (with duplicate linkage and canonical owner record).

No item may disappear merely because a PR was updated, a branch was deleted, an iteration ended, or an author report was rewritten.

### 7.9 Conditional approval / 条件通过

**PROPOSED policy clarification — not an existing AI-STD-001 severity rule:** conditional approval would be limited to non-blocking findings and must include:

**中文：** **建议政策说明，并非 AI-STD-001 现有严重度规则：** 条件通过仅适用于非阻断发现项，并必须记录以下内容：

- Finding ID and severity.
- Explicit risk description and impact.
- Accountable risk owner.
- Authorized risk-acceptance authority.
- Rationale for accepting the residual risk.
- Concrete restriction or Gate limitation.
- Deadline, expiry, or completion condition.
- Tracking Issue/Work Item.
- Re-evaluation trigger (new evidence, scope change, incident, Head change, or expiry).

**PROPOSED policy (requires governance adoption):** P0 cannot be conditionally bypassed. P1 is blocking by default; any exception requires explicit governance authority and cannot weaken mandatory safety/security invariants. P2 may be conditionally accepted when risk and restrictions are explicit. P3 is normally tracked as improvement work. CONDITIONAL PASS is not full PASS or unrestricted acceptance. AI-STD-001 currently defines the severity meanings and requires restrictions for CONDITIONAL PASS, but does not itself prescribe this complete P0/P1/P2/P3 blocking policy.

**中文：** **建议政策（须经治理采纳）：** P0 不得通过条件接受绕过；P1 默认阻断，任何例外均须由明确的治理授权主体批准，且不得削弱强制安全/安全性不变量；P2 可在风险与限制明确时条件接受；P3 通常作为改进项跟踪。CONDITIONAL PASS 不等于完整 PASS 或不受限制的验收。AI-STD-001 当前只定义严重度含义，并要求 CONDITIONAL PASS 记录限制条件；它本身并未规定这套完整的 P0/P1/P2/P3 阻断政策。

---

## 8. MVP Recommendation / MVP 建议

### 8.1 Minimal deliverables / 最小交付物

**PROPOSED:** Phase 1 should deliver four constructs, reusing AI-TPL-001 and AI-PROC-001:

1. **Work Item Manifest vNext** — one authoritative record for scope, roles, prompt identity, dependency pins, Base/Head, Gates, evidence, findings, and acceptance.
2. **Test Evidence Record** — immutable evidence records bound to exact target SHA.
3. **Independent Review Record** — one review per exact Head, including reviewer independence disclosure and finding disposition.
4. **Run Closeout Reconciliation** — a complete ledger of findings, Bugs, follow-ups, unrun checks, risks, and final states.

These may initially be Markdown/YAML templates plus deterministic validation. A database or service is not required for the MVP.

### 8.2 Minimal workflow / 最小流程

1. Register Work Item and freeze scope.
2. Freeze the executed Prompt version and digest.
3. Record Base SHA and dependency SHAs.
4. Implement on isolated branch and record commit/changed paths.
5. Run required tests and publish exact-SHA evidence.
6. Obtain independent review of exact Head.
7. Reconcile every finding and follow-up.
8. Record authorized acceptance and restrictions.
9. Perform run closeout; do not mark CLOSED while required evidence or blockers remain.

### 8.3 Explicit non-goals / 明确不做

- No new runtime or orchestration service.
- No AI worker, model invocation automation, or autonomous remediation.
- No database-backed defect platform.
- No automatic merge or automatic acceptance.
- No new governance authority.
- No rewrite of AI-STD-001 or AI-PROC-001 before Session 0 decides the precise amendments.

---

## 9. Phase 1 Acceptance Criteria / Phase 1 验收标准

Phase 1 should not be considered complete until all applicable criteria below are demonstrated on repository artifacts and exact commit SHAs.

| ID | Acceptance criterion | Evidence required |
|---|---|---|
| P1-QA-01 | Work Item Manifest contains required scope, roles, risk, dependencies, prompt, Base/Head, Gate and acceptance fields | Schema/template and valid example |
| P1-QA-02 | Prompt version and SHA-256 are immutable per executed run | Two-version example and digest verification |
| P1-QA-03 | Every test record identifies exact target SHA | Test Evidence examples |
| P1-QA-04 | Test outcomes distinguish PASS, FAIL, NOT RUN, BLOCKED, NOT APPLICABLE | Valid and invalid fixtures |
| P1-QA-05 | NOT RUN/BLOCKED cannot satisfy required test Gate | Negative validation test |
| P1-QA-06 | Review record requires exact PR Head SHA | Review schema/template |
| P1-QA-07 | A PR Head update invalidates prior review as current evidence | Head-change scenario and expected state |
| P1-QA-08 | Historical review remains immutable and discoverable | Review-history example |
| P1-QA-09 | Reviewer must be distinct from implementer and disclose independence limits | Review-record validation |
| P1-QA-10 | Finding has stable identity, severity, evidence, owner, state and closure criteria | Finding fixtures |
| P1-QA-11 | RESOLVED cannot transition directly to CLOSED without required verification | Negative state-transition test |
| P1-QA-12 | Conditional approval requires authorized risk owner, rationale, restrictions and expiry/condition | Conditional-approval fixture |
| P1-QA-13 | Run Closeout reconciles every finding, Bug, follow-up and unrun test | Closeout fixture and count invariant |
| P1-QA-14 | Work Item cannot close with unresolved BLOCKER/P0 or required missing evidence | Negative closure tests |
| P1-QA-15 | Existing standards are reused; no duplicate or conflicting lifecycle/authority is introduced | Cross-reference and consistency review |

### Mandatory scenario tests / 必测场景

**Scenario A — PR Head changes after review**

- Review Head H1 has PASS.
- Author pushes H2.
- Expected: H1 review remains historical; current review state for H2 becomes PENDING/NOT REVIEWED until a new review is completed.
- Forbidden: automatic carryover of H1 PASS to H2.

**Scenario B — Required test is NOT RUN**

- Work Item requires a critical contract test.
- Test record says NOT RUN with reason.
- Expected: Test Gate is BLOCKED or FAIL according to policy; it cannot be PASS.
- Forbidden: treating missing CI or absent logs as success.

**Scenario C — P2 finding is deferred**

- A P2 finding remains open.
- Expected: explicit risk owner, acceptance authority, reason, restriction, due/expiry, tracking Issue, and re-evaluation trigger.
- Forbidden: silently marking the finding CLOSED or treating CONDITIONAL PASS as unrestricted PASS.

### Acceptance boundary / 验收边界

Passing these Phase 1 criteria validates the governance record model and its deterministic checks. It does not prove the correctness of a production runtime, authorize a business architecture decision, or waive R3 domain/security/concurrency/recovery testing.

通过上述 Phase 1 标准，只能证明治理记录模型及其确定性校验达到验收要求；不能证明生产运行时正确，不能替代业务架构决策，也不能豁免 R3 领域、安全、并发和恢复测试。

---

## 10. Risks and Conflicts / 风险与冲突

| Risk | Impact | Control |
|---|---|---|
| Historical review treated as current | Defects can enter after an unreviewed Head change | Exact-Head binding and mandatory re-review |
| Author self-report treated as independent evidence | False confidence and self-approval | Separate reviewer identity and evidence retrieval |
| NOT RUN treated as PASS | Missing critical behavior remains invisible | Explicit test result enum and Gate validation |
| Reference-model result overstated | Production failure modes remain untested | Evidence ceiling and test-target classification |
| RESOLVED treated as CLOSED | Defects disappear without verification | Independent closure verification |
| Conditional approval has no expiry | Temporary risk acceptance becomes permanent | Owner, deadline, restrictions and re-evaluation trigger |
| Finding duplication across PRs | Inconsistent remediation and double counting | Canonical Finding identity and duplicate linkage |
| New framework duplicates existing standards | Conflicting states and maintenance burden | Incremental changes and explicit source references |
| Run closeout omits unresolved work | Lost defects and hidden technical debt | Reconciliation invariant and explicit state counts |
| GitHub mergeability mistaken for acceptance | Unapproved change may be merged | Separate platform mergeability from Gate/authority decision |

### Known tension: independence / 已知张力：独立性

AI-STD-001 requires role separation and an independent reviewer. The ChatGPT-native execution proposal discusses a separate conversation as an independent AI session while explicitly acknowledging that this is not model/provider/runtime/statistical independence. The quality process must preserve that limitation and must not imply multi-model consensus. Whether this interpretation fully satisfies the governance requirement is a decision for the authorized governance body, not an inference made by this report.

### Known tension: architecture repository versus production tests / 架构仓库与生产测试

The repository can validate document structure, bilingual parity, schema examples, reference models, and contract definitions before production code exists. It cannot claim production integration, concurrency, storage atomicity, Adapter delivery, or restore correctness without corresponding implementation and execution evidence.

---

## 11. Deferred Capabilities / 延期能力

The following capabilities are intentionally deferred beyond the Phase 1 MVP:

1. Database-backed defect intelligence platform.
2. Automated cross-repository finding correlation.
3. Automated risk scoring or AI-generated severity decisions.
4. Autonomous defect assignment and remediation.
5. Automatic PR approval or merge.
6. Continuous production telemetry ingestion.
7. Predictive defect analytics and machine-learning prioritization.
8. Organization-wide quality dashboards.
9. Automated evidence retention/archive service.
10. Complex policy-as-code for every exception type.

These capabilities should be considered only after the basic evidence model, exact-SHA review process, and reconciliation invariants are adopted and proven. They are not prerequisites for the first usable quality-control loop.

上述能力均不属于 Phase 1 最小闭环的前置条件。只有在基础证据模型、精确 SHA 审查和对账不变量得到实际验证后，才应评估是否引入。

---

## 12. Open Questions / 待决问题

1. **Governance authority:** Which role/body formally approves the quality record schema and any changes to AI-STD-001 / AI-PROC-001?
2. **Independent review sufficiency:** Does a fresh separate ChatGPT conversation satisfy the repository's independent-review requirement for each risk class, and which cases require a human or specialist reviewer?
3. **P1 exception:** Is any P1 risk acceptance permitted, and if so, which authority can authorize it without weakening mandatory invariants?
4. **Review freshness:** Should any change to the PR Head always require a full review, or can an explicitly scoped delta review be accepted under a documented policy?
5. **Evidence retention:** What is the canonical retention location and lifecycle for test logs, workflow artifacts, and review records?
6. **Finding ownership:** Who is the canonical owner when a finding spans multiple Owner domains or multiple PRs?
7. **Closure authority:** Which role may transition VERIFIED to CLOSED for P0/P1 and cross-owner findings?
8. **Metrics:** Which quality metrics are decision-useful without incentivizing suppression of findings or superficial closure?
9. **Repository automation:** Which deterministic validators are permitted in the documentation repository, and what governance review is required before adding them?
10. **Status vocabulary:** Should the proposed Gate states be encoded directly in AI-TPL-001 or mapped to existing Work Item and review statuses?

Session 0 should resolve these questions during cross-session synthesis. This report does not unilaterally decide them.

---

## 13. Evidence Index / 证据索引

### 13.1 Primary repository sources / 仓库原始文件

| Evidence | Exact identity | URL |
|---|---|---|
| AI-STD-001 | Blob f46867f97fc1860015adbe2a1f7b8262640c16fd | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/4bee3e886cc0dec4a8d03817acd180ba979f8ceb/14-ai-development/ai-development-standard.md |
| AI-PROC-001 | Blob 8ecc8e4ddde78be01e2038be4ece8dc8ac282c97 | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/4bee3e886cc0dec4a8d03817acd180ba979f8ceb/14-ai-development/iteration-lifecycle.md |
| AI-TPL-001 | Blob c9c545ae884991d2f5dd08c6880c50c97a13c143 | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/4bee3e886cc0dec4a8d03817acd180ba979f8ceb/14-ai-development/prompt-and-evidence-template.md |
| Architecture invariants | Blob 33b037318e459ebb73bea33b3186f31a41d5dcfe | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/4bee3e886cc0dec4a8d03817acd180ba979f8ceb/00-governance/architecture-invariants.md |

### 13.2 Issues / 议题

| Evidence | Purpose | URL |
|---|---|---|
| Issue #3 | Formal decision mechanism | https://github.com/oahcom/AiMemoryBrainArchitecture/issues/3 |
| Issue #7 | Architecture repository and production implementation boundary | https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7 |
| Issue #41 | AID-2026-001 Work Item | https://github.com/oahcom/AiMemoryBrainArchitecture/issues/41 |

### 13.3 Pull Requests and review evidence / PR 与审查证据

| Evidence | Exact Head / status | URL |
|---|---|---|
| PR #42 | Head 84d91b10e9069a575b479f6925d3b143757e82cb; OPEN/DRAFT/NOT MERGED | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42 |
| PR #42 historical Review | Head 1d6ab39375136d8649235feebeb6232609001222; historical FAIL | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42#pullrequestreview-5937629228 |
| PR #72 | Head 3bd943ad6ef2acf55a48e23e6b4cba92fdd3ada0; OPEN/DRAFT/NOT MERGED | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/72 |

### 13.4 Evidence interpretation / 证据解释

- PR descriptions are useful as author-supplied evidence indexes, but are not independent review.
- A GitHub mergeable=true response is not a quality or governance approval.
- Historical Review evidence applies only to the exact Head SHA recorded in that Review.
- A passing reference model proves only the bounded model/test scope stated in its evidence.
- No CI result, production test, or runtime behavior is claimed unless an exact run and target SHA are available.
- All evidence should be refreshed before a later acceptance or merge decision.

---

## 14. Final Recommendation / 最终建议

### 中文

建议 Session 0 将本研究纳入 Phase 0 综合设计，并批准一个范围受控的 Phase 1 质量治理 MVP：

1. 复用 AI-STD-001、AI-PROC-001 和 AI-TPL-001，不新建平行规范。
2. 优先实现四项结构化工件：Work Item Manifest、Test Evidence Record、SHA-bound Independent Review Record、Run Closeout Reconciliation。
3. 将 PR Head 变化后的 Review 失效规则作为硬约束。
4. 将 NOT RUN/BLOCKED 与 PASS 明确分离。
5. 将 Finding 的 RESOLVED、VERIFIED、CLOSED 分离，并要求独立验证。
6. 对条件通过设置责任人、期限、授权、限制和重新评估条件。
7. 以 Head 更新、关键测试 NOT RUN、P2 延期三个场景验证 MVP。
8. 在治理批准前，不修改现有标准、不实施自动化、不创建运行时服务、不合并本研究 PR。

**最终判断：** 现有治理基础足以支撑一个小型、可审计的 Phase 1 MVP；当前最紧迫的工作是补齐 SHA 绑定、测试证据、缺陷关闭和运行结束对账的可执行机制，而不是扩张治理体系。研究方案仍需 Session 0 统一裁定并取得正式治理批准。

### English

Session 0 should incorporate this research into the Phase 0 synthesis and authorize a tightly scoped Phase 1 quality-governance MVP:

1. Reuse AI-STD-001, AI-PROC-001, and AI-TPL-001; do not create a parallel standard.
2. Prioritize four structured artifacts: Work Item Manifest, Test Evidence Record, SHA-bound Independent Review Record, and Run Closeout Reconciliation.
3. Make review invalidation after a PR Head change a hard rule.
4. Explicitly separate NOT RUN/BLOCKED from PASS.
5. Separate Finding states RESOLVED, VERIFIED, and CLOSED, requiring independent verification.
6. Require owner, deadline, authority, restrictions, and re-evaluation conditions for conditional approval.
7. Validate the MVP with the Head-update, required-test-NOT-RUN, and deferred-P2 scenarios.
8. Before governance approval, do not modify existing standards, implement automation, create runtime services, or merge this research PR.

**Final judgment:** The existing governance foundation is sufficient for a small, auditable Phase 1 MVP. The most urgent work is to make SHA binding, test evidence, defect closure, and run-end reconciliation operational—not to expand the governance framework. The proposal still requires Session 0 synthesis and formal governance approval.

---

## 15. Publication and Authority Boundary / 发布与权限边界

This report is a research artifact only.

- No business architecture changes are proposed as approved decisions.
- No architecture invariant is changed.
- No Owner contract is amended.
- No production runtime, database, infrastructure, or worker is implemented.
- No GitHub Actions workflow or automation is implemented.
- No Issue is created or modified by this publication.
- No existing standard is modified by this publication.
- This report does not authorize implementation, acceptance, deployment, or merge.
- The PR must remain open for independent review by Session 0.

本报告仅为研究成果。它不构成业务架构批准，不修改架构不变量或 Owner 契约，不实施生产运行时、数据库、基础设施、Worker、GitHub Actions 或自动化，不修改 Issue 或现有规范，也不授权实施、验收、部署或合并。PR 应保持 Open，等待 Session 0 独立审查。

---

## 16. Research Conclusion / 研究结论

**Research disposition: READY FOR SESSION 0 SYNTHESIS — NOT YET A NORMATIVE APPROVAL.**

**研究结论：可进入 Session 0 综合收敛；尚未构成正式规范批准。**

The next authorized decision belongs to Session 0 — AI-DEV-OS-001 Principal Architect and the repository's designated governance authority.
