# AI-DEV-OS-001 — Session 2: Prompt Lifecycle & Execution Provenance Architecture
# AI-DEV-OS-001 — 会话 2：Prompt 生命周期与执行来源追踪架构

## 1. Document Metadata / 文档元数据

| Field | Value |
|---|---|
| Program | AI-DEV-OS-001 |
| Session | 2 — Prompt Lifecycle & Execution Provenance |
| Phase | Phase 0 — Research Publication; read-only research findings |
| Status | Research report; recommendations are PROPOSED, not approved architecture |
| Repository baseline | oahcom/AiMemoryBrainArchitecture |
| Baseline main HEAD | e52594f181d2edb77448adcfed64a0fbdffaf3aa |
| Publication path | 14-ai-development/research/phase-0/SESSION-2-PROMPT-RUN-PROVENANCE-REPORT.md |
| Languages | Chinese and English |
| Authority | Research and recommendation only; no implementation authority |
| Scope boundary | AI development governance and evidence only; not business Domain Model |

本报告记录 Session 2 对 Prompt 身份、版本、实际执行 Run、证据来源和 Git 提交关联的 Phase 0 研究结论。所有架构建议均为 PROPOSED，须由 Session 0 独立审查和批准后方可进入 Phase 1。

This report records Session 2 Phase 0 findings on prompt identity, immutable versioning, bounded execution runs, evidence provenance, and Git commit traceability. All architectural recommendations are PROPOSED and require independent Session 0 review and approval before Phase 1.

## 2. Executive Summary / 执行摘要

### 中文

仓库现有 AI Development 标准已经建立了 Work Item、Prompt ID/Version/SHA-256、Owner/Reviewer、风险等级、Branch/Commit/PR、Evidence Manifest、测试证据、审查证据和验收记录等基础治理元素。无需另建一套平行体系。

核心缺口不是缺少 Prompt 文档，而是缺少一个统一、可验证的“实际执行实例”模型：每次有明确边界的执行尝试应有独立 Run ID；Run 必须绑定实际使用的不可变 Prompt 版本、精确 Git 字节摘要、执行主体/渠道、时间、目标 Commit、测试和审查证据。重试应创建新 Run，不得覆盖失败或中断历史。

建议 Phase 1 仅以 Markdown/YAML manifest、GitHub Commit/PR 和现有 CI 证据实现最小可审计闭环。当前不建议数据库、事件总线、Worker Runtime、对象存储或自动化执行平台。该建议不构成对任何 AI 执行渠道或运行时的授权。

### English

The repository already has useful governance primitives: Work Items, Prompt ID/version/SHA-256, Owner/Reviewer, risk level, branch/commit/PR references, evidence manifests, test evidence, review evidence, and acceptance records. A parallel governance framework is unnecessary.

The principal gap is a consistent model for an actual bounded execution attempt. Each attempt should have a unique Run ID and bind the exact immutable prompt version and byte digest, actor/channel, timestamps, target commit, tests, reviews, and acceptance evidence. A retry creates a new Run; it must not overwrite failed, cancelled, or interrupted history.

For Phase 1, use a minimal auditable approach based on Markdown/YAML manifests, GitHub commits and pull requests, and existing CI evidence. Do not introduce a database, event bus, worker runtime, object storage, or autonomous execution platform at this stage. This recommendation does not authorize any AI execution channel or runtime.

## 3. Research Scope / 研究范围

### 中文

本研究聚焦以下问题：

1. Prompt 是否具有独立于 Work Item 的稳定身份？
2. Prompt 版本如何冻结、升级和验证？
3. 如何区分 Prompt 模板与某次真实执行？
4. 如何将 Run、Commit、测试、Review 和 Acceptance 关联？
5. 如何区分声明性证据与独立验证证据？
6. 如何记录失败、重试、取消和中断？
7. Phase 1 是否需要新的持久化基础设施？

研究读取了 main 基线中的以下文件：

- 14-ai-development/README.md
- 14-ai-development/ai-development-standard.md
- 14-ai-development/iteration-lifecycle.md
- 14-ai-development/prompt-and-evidence-template.md
- 14-ai-development/work-items/INDEX.md

同时检查了 PR #23、PR #42 和 Issue #41 的相关内容，用于识别已有提案、执行记录实例和执行渠道边界。

### English

The research addresses stable prompt identity, immutable versioning, the distinction between a prompt template and an actual execution, Run-to-commit/test/review/acceptance traceability, evidence trust levels, failure and retry history, and the minimum persistence needed for Phase 1.

The five current-main files listed above were inspected. PR #23, PR #42, and Issue #41 were also examined as proposal and implementation evidence. They are not treated as approved standards merely because they exist.

### Research boundary / 研究边界

- VERIFIED means directly supported by an inspected repository artifact or GitHub object.
- PROPOSED means a recommendation made by this research.
- UNKNOWN means evidence is insufficient to conclude.
- NOT APPLICABLE means the question does not apply to this scope.

本报告不实现 schema、工具、Worker、数据库或 CI；不修改 Prompt 模板；不修改业务领域模型；不批准任何历史 PR。

This report does not implement schemas, tools, workers, databases, or CI; does not modify prompt templates or business domain models; and does not approve any historical PR.

## 4. Current State / 当前状态

### 4.1 Main-branch baseline / main 分支基线

**VERIFIED** — At research refresh, main resolved to commit e52594f181d2edb77448adcfed64a0fbdffaf3aa. The recursive Git tree was complete (not truncated). It contained the five AI-development files listed in Section 3, but no 14-ai-development/research/phase-0 directory and no Session 2 publication report.

The five inspected file Blob SHAs at that baseline were:

| File | Blob SHA |
|---|---|
| 14-ai-development/README.md | 9593fd66f2b830748d826d754ce3e6da00e6f144 |
| 14-ai-development/ai-development-standard.md | f46867f97fc1860015adbe2a1f7b8262640c16fd |
| 14-ai-development/iteration-lifecycle.md | 8ecc8e4ddde78be01e2038be4ece8dc8ac282c97 |
| 14-ai-development/prompt-and-evidence-template.md | c9c545ae884991d2f5dd08c6880c50c97a13c143 |
| 14-ai-development/work-items/INDEX.md | a9d433337c7e1d2c497b18a437f5289dd74134ea |

### 4.2 Existing proposals / 现有提案

**VERIFIED** — PR #23 is OPEN and DRAFT, not merged. Its current Head at the time inspected was b6b9d2662729fdf2c112ae689cda34e235fdc82f; its base was main at b372b62c640a2b656e54b6db62a4ee67d7d8c001. The PR proposes AI-PROMPT-STD-001, AI-RUN-001, immutable prompt versions, byte-exact hashing, and an event-driven worker model. These are proposal contents, not approved repository policy.

**VERIFIED** — PR #42 is OPEN and DRAFT, not merged. Its current Head at the time inspected was 84d91b10e9069a575b479f6925d3b143757e82cb; its recorded base SHA was b372b62c640a2b656e54b6db62a4ee67d7d8c001. It contains an AID-2026-001 manifest, prompt versions, and an execution record. Its latest historical independent review is recorded against a different Head (1d6ab39375136d8649235feebeb6232609001222); it must not be represented as a review of the current Head.

**VERIFIED** — PR #42's current PR description reports zero workflow runs and zero commit status checks for its current Head, with YAML/schema validation and reproducible R3 contract tests marked NOT RUN, and acceptance BLOCKED/PENDING. These are the PR's reported status statements; they are not an independent test execution by this research.

**VERIFIED** — Issue #41 states the intended execution boundary as ordinary ChatGPT conversations plus connected GitHub operations, and explicitly excludes API Worker/API Key, Codex, other model providers, Desktop Commander, and local-computer relay. It also states Ubuntu/GitHub Actions may run deterministic build/test/CI jobs only and must not invoke an AI model. This report therefore keeps provenance channel-neutral and does not recommend a runtime.

### English interpretation

The repository contains useful proposals and examples, but their open/draft state matters. A proposal is not an accepted standard. Historical reviews are tied to the exact commit they reviewed. A PR's own narrative is evidence of what its author declared, not independent verification. Issue #41's explicit channel restrictions are treated as a boundary for this research, not as a reason to design a new execution platform.

## 5. Existing Capabilities / 已有能力

| Capability | Status | Finding |
|---|---|---|
| Work Item identity | VERIFIED | AID-YYYY-NNN pattern is present in existing governance materials |
| Prompt identity/version | VERIFIED | Prompt ID and version are already represented |
| Prompt digest | VERIFIED | SHA-256 is already part of prompt/evidence conventions |
| Owner and Reviewer | VERIFIED | Roles are represented in existing templates |
| Risk classification | VERIFIED | Risk Level is represented |
| Git traceability | VERIFIED | Branch, Commit and PR references are represented |
| Evidence manifest | VERIFIED | Evidence Manifest is an existing concept |
| Test/review/acceptance evidence | VERIFIED | Existing materials provide fields/concepts for these records |
| Independent bounded Run identity | PARTIAL / GAP | An execution record example exists in PR #42, but no complete accepted current-main lifecycle contract was established |
| Retry lineage and immutable failed attempts | GAP | Not established as a complete accepted contract in the inspected current-main files |

### 中文说明

已有规范已覆盖治理对象和证据类别，因此 Phase 1 应复用现有 Work Item 与 Evidence Manifest。缺少的是把一次真实执行尝试作为一等证据对象，并明确其状态、唯一性和与 Commit 的绑定规则。

### English explanation

Existing standards already cover governance objects and evidence categories. Phase 1 should extend those conventions rather than replace them. The missing piece is a first-class record for each real execution attempt, including identity, lifecycle state, retry lineage, and commit binding.

## 6. Missing Capabilities / 缺失能力

### 中文

1. **Run identity**：没有在当前 main 规范中确认一套完整、统一、不可复用的 Run ID 规则。
2. **Run lifecycle**：开始、完成、失败、取消、中断等状态及其终态语义不够完整。
3. **Retry lineage**：重试如何关联原 Run、如何保留失败记录尚未形成统一规则。
4. **Exact prompt binding**：需要把 Prompt ID、Version、Path、Git Blob SHA、文件 SHA-256 和来源 Commit 明确区分并绑定到 Run。
5. **Evidence trust model**：模型自述、GitHub 客观事实、独立验证结果必须明确区分。
6. **Test-to-commit binding**：测试证据必须指向精确 subject commit，不能仅写“测试通过”。
7. **Review freshness**：PR Head 变化后，旧 Review 不应被当作新 Head 的有效审查。
8. **Missing evidence semantics**：必须明确 NOT RUN、NOT VERIFIED、BLOCKED、INTERRUPTED 等状态。
9. **Acceptance gate**：Mandatory evidence 缺失时，不得宣称验收完成。

### English

The gaps are a consistent Run ID and lifecycle, retry lineage, exact prompt-to-run binding, explicit evidence trust classes, test-to-commit binding, review freshness, precise missing-evidence states, and acceptance gates that prevent unsupported success claims.

## 7. Proposed Architecture / 建议架构

All items in this section are **PROPOSED** and require Session 0 approval.

### 7.1 Identity hierarchy / 身份层级

**PROPOSED** — Keep the identities separate:

- Work Item ID identifies the governed unit of work, e.g. AID-2026-001.
- Prompt ID identifies a reusable prompt definition.
- Prompt Version identifies one immutable revision of that definition.
- Run ID identifies one bounded execution attempt.
- Evidence ID identifies one evidence artifact or observation.
- Commit SHA identifies an exact repository state.

A Work Item may reference multiple prompts; a Prompt Version may be used by multiple Runs; a Work Item may have multiple Runs; and a Run may produce or reference multiple evidence items. These identities must not be overloaded into one identifier.

建议 Run ID 格式：AID-2026-001-RUN-001。实际命名可由 Session 0 统一裁定。重试创建新的 Run ID，并通过 retry_of_run_id 指向前一 Run。

### 7.2 Immutable prompt version / 不可变 Prompt 版本

**PROPOSED** — A material prompt change creates a new version. Do not overwrite a version that has already been used for an execution whose evidence must remain auditable.

For every Run, record:

- prompt_id
- prompt_version
- prompt_path
- prompt_git_blob_sha
- prompt_sha256
- prompt_source_commit_sha
- prompt_byte_length
- optional prompt media type / encoding metadata

The SHA-256 digest should be computed over the exact committed file bytes. Do not silently normalize line endings, whitespace, Unicode normalization, or byte-order marks before hashing. Record the byte encoding and any transformation only if a transformation is explicitly part of the prompt production process.

**Important distinction:** Git Blob SHA and SHA-256 of file bytes are different identifiers with different purposes. Store them in separate fields. A Git Blob SHA is Git object identity; the SHA-256 field is the prompt content digest required by the governance contract. Do not copy one into the other.

### 7.3 Bounded Run lifecycle / 有界执行生命周期

**PROPOSED** — One Run represents one bounded attempt, not an indefinitely appended activity log.

Suggested terminal states:

- COMPLETED
- FAILED
- CANCELLED
- INTERRUPTED

Suggested in-progress state:

- RUNNING

A retry creates a new Run and records retry_of_run_id. The prior Run remains immutable. If a Run is resumed after interruption, the governance owner must decide whether the action is a continuation event under the same Run or a new Run linked by resumed_from_run_id; the MVP should prefer a new Run when execution context or prompt inputs materially change.

A Run record should be append-only after finalization. Corrections should be new correction/verification evidence, not silent replacement of the original record.

### 7.4 Minimal execution record / 最小执行记录

**PROPOSED** — The following is a conceptual field set, not an implemented schema:

| Field group | Minimum fields |
|---|---|
| Schema and identity | schema_version, run_id, work_item_id |
| Repository context | repository, issue_refs, pr_refs |
| Prompt binding | prompt_id, prompt_version, prompt_path, prompt_git_blob_sha, prompt_sha256, prompt_source_commit_sha, prompt_byte_length |
| Actor and channel | actor, execution_channel, model_identifier_if_available |
| Time and status | started_at, finished_at, status |
| Git state | initial_commit_sha, resulting_commit_sha, subject_commit_sha |
| Actions | changed_paths, commands_or_operations_declared |
| Test evidence | tests_executed, tests_not_run, result, workflow_run_id, job_id, artifact_refs |
| Findings | errors, findings, follow_up_refs |
| Review and acceptance | review_refs, reviewed_head_sha, acceptance_refs, final_disposition |
| Provenance | evidence_class, verifier, verification_timestamp |

Do not require or invent model metadata that the execution environment does not expose. Use UNKNOWN or NOT AVAILABLE where appropriate.

### 7.5 Evidence provenance classes / 证据来源类别

**PROPOSED** — Distinguish three evidence classes:

1. **FACT** — Directly observable GitHub facts: commit SHA, PR Head SHA, file Blob SHA, workflow run/job identifiers, review identifiers, timestamps, and repository state.
2. **DECLARED** — Statements made by an actor or model: claimed commands, claimed test outcomes, self-reported findings, or a narrative that work was completed.
3. **VERIFIED** — A claim independently checked against its source: CI result tied to an exact commit, independent review tied to an exact PR Head, independently recalculated prompt digest, or successful read-back of committed content.

A model's statement that tests passed is DECLARED, not VERIFIED. A PR body written by the author is not an independent review. Verification should identify who or what performed it, when, and against which immutable subject.

### 7.6 Commit and test binding / Commit 与测试绑定

**PROPOSED** — Every test result must identify its subject_commit_sha. Where available, also record workflow_run_id, job_id, command, environment, toolchain version, and artifact reference.

A result for commit X does not automatically validate commit Y. When a PR Head changes, review and test evidence must be evaluated for freshness against the new Head. A historical review remains valid evidence of what was reviewed at its recorded SHA, but not of later changes.

### 7.7 Failure and missing evidence / 失败与缺失证据

**PROPOSED** — Use explicit statuses:

- NOT RUN: the test or review was not executed.
- NOT VERIFIED: a claim exists but has not been independently checked.
- BLOCKED: execution or acceptance cannot proceed because a prerequisite is missing.
- INTERRUPTED: execution stopped without a verified terminal result.
- FAILED: execution occurred and produced a failure result.
- CANCELLED: execution was intentionally stopped.

Missing evidence must never be converted into PASS by inference. Mandatory evidence absent at an acceptance gate blocks acceptance.

### English summary of the model

The architecture separates work, prompt definition, immutable prompt version, bounded Run, evidence item, and commit identity. It binds each Run to the exact prompt bytes and exact repository state. It classifies evidence by how it is known, preserves failure and retry history, and makes acceptance depend on explicit evidence rather than narrative claims.

## 8. MVP Recommendation / MVP 建议

### 中文

**建议 Phase 1 MVP 采用轻量、可读、可审计的 Git-native 方案：**

1. 复用现有 Work Item 和 Evidence Manifest。
2. 为每次 bounded attempt 增加独立 Run ID 和一份执行记录。
3. 记录 Prompt ID/Version、精确 SHA-256、Git Blob SHA、来源 Commit。
4. 将测试、Review 和 Acceptance 绑定到精确 Commit/PR Head。
5. 以 Git Commit 历史保存不可变版本；修订以新 Commit 或新 Run 记录，不覆盖历史。
6. 使用 GitHub PR 作为审查入口，要求报告证据可读回。
7. 缺失证据采用显式状态，并由验收 Gate 阻断不完整结果。

现阶段不引入数据库、事件溯源平台、消息队列、对象存储、常驻 Worker 或新的自动化 AI 执行系统。只有当实际出现明确的并发、吞吐、事务一致性、保留期限、查询或访问控制需求时，才重新评估持久化设施。

### English

**Recommended Phase 1 MVP: a lightweight, readable, Git-native evidence model.**

1. Reuse the existing Work Item and Evidence Manifest.
2. Add a unique Run ID and execution record for each bounded attempt.
3. Record Prompt ID/version, exact SHA-256, Git Blob SHA, and source commit.
4. Bind tests, reviews, and acceptance to exact commits and PR Heads.
5. Preserve history through Git commits; use new records rather than overwriting prior evidence.
6. Use GitHub PRs as the review surface and verify committed content by read-back.
7. Represent missing evidence explicitly and block acceptance when mandatory evidence is absent.

Do not introduce a database, event-sourcing platform, message queue, object store, always-on worker, or new autonomous AI execution system at this stage. Reassess infrastructure only when concrete scale, concurrency, transaction, retention, query, or access-control requirements justify it.

## 9. Phase 1 Acceptance Criteria / Phase 1 验收标准

The following criteria are **PROPOSED**. Session 0 must approve or amend them before implementation.

| ID | Acceptance criterion | 验收标准 |
|---|---|---|
| P1-01 | Identity separation | Work Item, Prompt, Prompt Version, Run, Evidence and Commit identities are distinct |
| P1-02 | Immutable prompt | Used prompt versions cannot be silently overwritten |
| P1-03 | Digest correctness | SHA-256 is calculated from exact committed bytes and independently checked |
| P1-04 | Run uniqueness | Each bounded attempt has one unique Run ID |
| P1-05 | Retry lineage | Retry creates a new Run and links the previous Run |
| P1-06 | Lifecycle completeness | Completed, failed, cancelled and interrupted states are representable |
| P1-07 | Commit binding | Tests and reviews identify the exact commit/PR Head they cover |
| P1-08 | Evidence classification | FACT, DECLARED and VERIFIED are distinguishable |
| P1-09 | Missing evidence | NOT RUN, NOT VERIFIED, BLOCKED and INTERRUPTED are explicit |
| P1-10 | Acceptance gate | Mandatory missing evidence prevents acceptance |
| P1-11 | Read-back | Committed manifest and report are fetched and compared after publication |
| P1-12 | Boundary isolation | No business Domain Model, runtime or infrastructure changes are introduced |

### 中文补充

验收必须验证真实 GitHub 对象和精确 SHA，而非只检查 Markdown 中的自述。PR Head 发生变化时，必须重新判断 Review 和 Test 是否覆盖当前 Head。Phase 1 不得将 AI-DEV-OS 的治理身份扩展为业务 Domain Model 的领域实体。

### English supplement

Acceptance must inspect actual GitHub objects and exact SHAs, not merely read narrative claims. When the PR Head changes, review and test freshness must be reassessed. AI-DEV-OS governance identities must not be promoted into business Domain Model entities.

## 10. Risks and Conflicts / 风险与冲突

| Risk | Status | Assessment and mitigation |
|---|---|---|
| Proposal mistaken for approved standard | VERIFIED risk | PR #23 and #42 are open/draft; label all proposal-derived material as PROPOSED |
| Historical review mistaken for current review | VERIFIED risk | PR #42 history includes reviews against earlier Heads; bind every review to its exact SHA |
| One execution record reused for multiple attempts | VERIFIED observation | PR #42's execution record example appends later remediation activity under one record; enforce bounded Run identity and retry lineage |
| Self-reported test result treated as verified | PROPOSED risk control | Separate DECLARED from VERIFIED |
| Git Blob SHA confused with SHA-256 | PROPOSED risk control | Use separate named fields and independent digest check |
| Stale test/review evidence | PROPOSED risk control | Bind evidence to subject_commit_sha and reviewed_head_sha |
| Over-engineering | PROPOSED risk control | Start with Git-native records; defer database and worker infrastructure |
| Runtime/channel contradiction | VERIFIED cross-artifact tension | PR #23 proposes event-driven worker execution; Issue #41 and PR #42 describe a ChatGPT-native boundary excluding API Worker/Codex/other providers/local relay. Session 2 does not resolve the conflict; provenance stays channel-neutral and records the actually authorized channel |
| Incomplete reproducibility | UNKNOWN / inherent limitation | Hidden platform instructions, context, and model nondeterminism may prevent exact replay; distinguish auditability from full reproducibility |

### 中文风险裁定

PR #23 的 AI-RUN-001 目标运行模型与 Issue #41 所定义的 ChatGPT-native 执行边界存在明显张力。Session 2 不应借 Prompt/Run 研究擅自决定哪个运行时获批。Run 记录只需如实记录实际执行渠道及其授权依据。

可审计性不等于完全可复现。对于无法导出的隐藏系统指令、平台内部上下文和模型随机性，应记录已知边界，不得声称可以完整重放。

### English risk assessment

PR #23's proposed event-driven worker model is in tension with the ChatGPT-native boundary stated in Issue #41 and reflected in PR #42. Session 2 has no authority to resolve that runtime decision. The provenance model should record the channel actually used and its authorization basis without prescribing a runtime.

Auditability is not equivalent to perfect reproducibility. Hidden system instructions, inaccessible platform context, and model nondeterminism may prevent exact replay. The report should state those limits honestly.

## 11. Deferred Capabilities / 延期能力

### 中文

以下能力不属于 Phase 1 MVP，除非 Session 0 基于真实需求另行批准：

- 数据库或独立证据服务；
- Event Sourcing、消息队列、分布式调度和 Worker lease；
- 常驻或事件触发的 AI Worker；
- 自动模型调用、自动 PR 合并或自动验收；
- 跨平台统一模型遥测；
- 对隐藏模型上下文的完整快照和精确重放；
- 高级证据保留、签名和防篡改存储服务。

### English

Defer databases, evidence services, event sourcing, queues, distributed schedulers, worker leases, always-on/event-triggered AI workers, automatic model invocation, auto-merge, auto-acceptance, cross-platform model telemetry, exact replay of hidden context, and specialized retention/signature/tamper-evident services unless a separately approved requirement justifies them.

## 12. Open Questions / 待决问题

1. **Run boundary** — Should a continuation after interruption be a new Run by default, or can a same-Run continuation be represented as an append-only event?
2. **Prompt scope** — Which prompt artifacts must be frozen and hashed: only the primary prompt file, or also referenced global/Owner instructions where accessible?
3. **Channel authorization** — Which governance artifact is authoritative when runtime proposals conflict with the ChatGPT-native boundary in Issue #41?
4. **Independent verification** — What qualifies as an independent verifier when the workflow is conversation-driven?
5. **Retention** — What retention period applies to Run records, logs, and CI artifacts?
6. **Schema ownership** — Which role owns the canonical Run schema and its versioning?
7. **Privacy boundary** — Which prompt or execution context fields must be redacted or excluded from committed evidence?

These questions require Session 0 or the relevant governance owner. Session 2 does not decide them.

以上问题需要 Session 0 或对应治理 Owner 决策；Session 2 不作越权裁定。

## 13. Evidence Index / 证据索引

All GitHub links below identify source artifacts. Blob SHAs are recorded to make the inspected content version explicit. PR and Issue states are snapshots at the research refresh and may change later.

### 13.1 Current-main source files / 当前 main 原始文件

| Evidence | URL | SHA / finding |
|---|---|---|
| AI development README | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/README.md | Blob 9593fd66f2b830748d826d754ce3e6da00e6f144 |
| Development standard | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/ai-development-standard.md | Blob f46867f97fc1860015adbe2a1f7b8262640c16fd |
| Iteration lifecycle | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/iteration-lifecycle.md | Blob 8ecc8e4ddde78be01e2038be4ece8dc8ac282c97 |
| Prompt/evidence template | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/prompt-and-evidence-template.md | Blob c9c545ae884991d2f5dd08c6880c50c97a13c143 |
| Work Item index | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/e52594f181d2edb77448adcfed64a0fbdffaf3aa/14-ai-development/work-items/INDEX.md | Blob a9d433337c7e1d2c497b18a437f5289dd74134ea |
| Main commit | https://github.com/oahcom/AiMemoryBrainArchitecture/commit/e52594f181d2edb77448adcfed64a0fbdffaf3aa | Research baseline |

### 13.2 Related proposal and governance evidence / 相关提案与治理证据

| Evidence | URL | Exact reference |
|---|---|---|
| PR #23 — AI development governance proposal | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/23 | Inspected Head b6b9d2662729fdf2c112ae689cda34e235fdc82f; base SHA b372b62c640a2b656e54b6db62a4ee67d7d8c001; OPEN/DRAFT |
| PR #23 prompt authoring proposal file | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/b6b9d2662729fdf2c112ae689cda34e235fdc82f/14-ai-development/prompt-authoring-standard.md | Blob eace2b8478f5720f248a415b77993212b85e121c |
| PR #23 automation operating model | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/b6b9d2662729fdf2c112ae689cda34e235fdc82f/14-ai-development/owner-automation-operating-model.md | Blob c406d8c5b32977e8510b016ee71f9693d35ce821 |
| PR #42 — ChatGPT-native execution proposal | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42 | Inspected Head 84d91b10e9069a575b479f6925d3b143757e82cb; base SHA b372b62c640a2b656e54b6db62a4ee67d7d8c001; OPEN/DRAFT |
| PR #42 manifest | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/84d91b10e9069a575b479f6925d3b143757e82cb/14-ai-development/work-items/AID-2026-001/manifest.yaml | Blob c83a6a093cdda58cf26cba93a92a452e6a1717a0 |
| PR #42 execution record | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/84d91b10e9069a575b479f6925d3b143757e82cb/14-ai-development/work-items/AID-2026-001/execution-record-001.md | Blob a3d28acb510da004f6644f52f390b846aaa819e7 |
| PR #42 prompt v2 | https://github.com/oahcom/AiMemoryBrainArchitecture/blob/84d91b10e9069a575b479f6925d3b143757e82cb/14-ai-development/work-items/AID-2026-001/prompts/global-session-contract-v2.md | Blob 20fe27cdac1ee0f8b0dcbe047b88302327fa97b1 |
| Historical PR #42 review | https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42#pullrequestreview-5937629228 | Review against Head 1d6ab39375136d8649235feebeb6232609001222; not current Head |
| Issue #41 — ChatGPT-native execution boundary | https://github.com/oahcom/AiMemoryBrainArchitecture/issues/41 | OPEN at research refresh |

### 13.3 Digest verification limitation / 摘要验证限制

PR #42's manifest/appendendum declares Prompt v2 SHA-256 as c49b09af16fd34941926665b450b8cd0788283240f4b31b2877695bc5b8b1cb7. This research confirmed the declaration exists in the proposal material but did **not** independently re-hash the file bytes. Therefore that digest is **DECLARED**, not independently VERIFIED by Session 2.

PR #42's author-maintained status statements about zero workflow runs, zero status checks, tests NOT RUN, and acceptance BLOCKED/PENDING are attributed to the PR description. They are not presented here as a fresh independent CI execution.

### 13.4 Evidence classification / 证据分类

- **VERIFIED** — Current-main files, tree, commit and Blob SHAs; GitHub PR/Issue metadata; exact historical review Head references as surfaced by GitHub.
- **DECLARED** — Prompt digest declaration in PR #42; author-reported test/CI and remediation status in PR descriptions.
- **PROPOSED** — Run schema, evidence classes, lifecycle rules, MVP and acceptance criteria in this report.
- **UNKNOWN** — Independent digest re-hash of PR #42 Prompt v2; complete reproducibility of hidden model context; unresolved runtime authorization conflict.
- **NOT APPLICABLE** — Production runtime performance or business-domain behavior; this is a read-only governance research report.

## 14. Final Recommendation / 最终建议

### 中文最终建议

建议 Session 0 **有条件采纳**本报告的核心方向：复用现有 Work Item 和 Evidence Manifest，补齐 Prompt immutable version 与 bounded Run 的精确绑定，建立 FACT/DECLARED/VERIFIED 证据区分、Commit-bound Test/Review 和显式缺失证据 Gate。

Phase 1 应先定义并审查最小 Run 记录规范，再实施最小 Git-native 记录机制。不得因本报告而批准 PR #23 的 event-driven Worker Runtime，也不得绕过 Issue #41 的执行渠道边界。PR #23、PR #42 仍须分别按各自精确 Head 接受独立审查。

**本报告不是架构批准、实施授权或运行时选择决议。** 它只提供可供 Session 0 复核的研究依据。

### English final recommendation

Session 0 should **conditionally adopt** the direction of reusing existing Work Item and Evidence Manifest conventions while adding exact immutable prompt binding, a bounded Run identity, FACT/DECLARED/VERIFIED evidence classes, commit-bound tests and reviews, and explicit missing-evidence gates.

Phase 1 should first approve a minimal Run record contract, then implement the smallest Git-native evidence mechanism. This report does not approve PR #23's event-driven Worker Runtime and does not override the execution-channel boundary in Issue #41. PR #23 and PR #42 still require independent review against their own exact current Heads.

**This report is not architecture approval, implementation authorization, or a runtime selection decision.** It is a research artifact for Session 0's independent assessment.

---

**End of report / 报告结束**
