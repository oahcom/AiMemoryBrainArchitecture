# AI Development Standard
# AI 开发规范

**Document ID:** AI-STD-001  
**Version:** 1.0  
**Status:** PROPOSED — initial governance baseline  
**Applies to:** All AI-assisted and AI-executed work in this repository  
**Normative language:** MUST / MUST NOT / SHOULD / MAY

> This standard establishes the engineering controls for a project developed by AI agents under explicit project governance. AI agents are developers, not autonomous authorities over project scope, security policy, or acceptance.

## 1. Purpose / 目的

The project is developed end-to-end by AI developers organized around named module Owners. Quality must come from explicit authority boundaries, reproducible work, independent verification, and traceable decisions—not from confidence or verbosity in an AI response.

本规范建立全 AI 开发项目的统一工程制度。质量依靠明确的职责边界、可复现的开发过程、独立验证和可追溯决策，而不是依靠 AI 的自我评价。

The standard governs architecture changes, implementation, tests, documentation, migrations, security changes, and release work. It applies equally to every Owner and cross-cutting specialist.

## 2. Governing principles / 基本原则

1. **Prompt is a controlled work instruction.** No substantive development starts from an informal chat request alone. A versioned task prompt MUST exist in the repository before execution.
2. **Owner accountability.** Every task has one accountable Owner. Multiple contributors may assist, but ownership is singular and explicit.
3. **Authority follows the contract.** An Owner may decide within its domain, but MUST NOT silently redefine another Owner's contracts.
4. **Independent verification.** The implementing AI MUST NOT be the sole reviewer or sole acceptance authority for its own work.
5. **Evidence over assertion.** “Implemented”, “tested”, “secure”, “passed” and “complete” require specific evidence.
6. **Small, reversible increments.** Prefer small vertical slices and narrow changes over broad speculative rewrites.
7. **Fail closed on uncertainty.** Unknown contract, identity, permission, data-loss, or recovery behavior blocks unsafe progression.
8. **No silent decisions.** Material changes require a decision record, rationale, alternatives, consequences, and affected owners.
9. **Traceability is mandatory.** Requirement → task → prompt version → branch/commit → changed files → tests → review → integration decision must be traceable.
10. **Bilingual architecture documentation.** Normative architecture and engineering specifications MUST provide Chinese and English content or an explicitly linked bilingual companion. Code comments may follow repository language conventions.

## 3. AI developer roles / AI 开发角色

### 3.1 Module Owners

The project uses the A–I Owner model:

| Owner | Primary authority |
|---|---|
| A | Principal integration, cross-module contract registry, integration decisions |
| B | Domain model and canonical domain semantics |
| C | Agent integration, telemetry and inference-boundary requirements |
| D | Canonical Memory Brain, memory lifecycle and Forget semantics |
| E | Memory Compiler and derived-memory production |
| F | Memory Runtime, retrieval, activation, working sets and runtime cache |
| G | Memory Context, ContextVersion, ChangeSet and reconciliation |
| H | BMCP protocol and Adapter protocol behavior |
| I | Security, identity, authorization and governance |

Storage/Consistency, Testing/Quality, Observability/Performance and Release may operate as named cross-cutting specialist roles. They MUST have explicit task authority and MUST NOT silently take ownership of a module's domain decisions.

### 3.2 Required separation of duties

For every non-trivial task, assign:

- **Request/Task Sponsor:** clarifies intended outcome and priority.
- **Accountable Owner:** owns the domain result and branch.
- **Implementing AI:** performs the change under the approved prompt.
- **Independent Reviewer:** a separate AI session/agent that did not author the implementation.
- **Integration Architect:** checks cross-module compatibility and integration evidence.
- **Acceptance Authority:** approves scope, risk and merge according to project governance.

One AI session adopting several personas does NOT constitute independent review. A simulated panel is useful for brainstorming but is not evidence of independent approval.

For low-risk documentation-only changes, one reviewer may cover several review dimensions, but author and reviewer MUST remain distinct. Security, data deletion, authorization, consistency, recovery and public protocol changes require independent specialist review.

## 4. Task classification and gates / 任务分类与门禁

Every work item MUST declare its class:

- **ARCH:** architecture or contract definition;
- **IMPL:** production implementation;
- **TEST:** test infrastructure, fixtures or conformance tests;
- **SEC:** security, identity, privacy, retention or deletion;
- **MIG:** schema/data migration or compatibility;
- **PERF:** performance/resource measurement;
- **DOC:** documentation-only;
- **OPS:** build, CI, release or operational work.

Risk levels:

- **R0:** editorial, no normative or executable behavior change;
- **R1:** isolated implementation/documentation with bounded impact;
- **R2:** cross-module contract, persistence, protocol, concurrency or compatibility impact;
- **R3:** security boundary, authorization, Forget/deletion, data integrity, recovery, migration or release-critical change.

R2/R3 require explicit impact analysis and named reviewers. R3 requires security/domain specialist review and reproducible test evidence before acceptance.

### 4.1 Work item lifecycle

| State | Meaning | Exit evidence |
|---|---|---|
| PROPOSED | Outcome and motivation recorded | Sponsor and candidate Owner identified |
| ANALYZED | Scope, dependencies, risks and alternatives analyzed | Impact map and acceptance criteria |
| PROMPT_READY | Prompt reviewed and frozen for execution | Prompt ID/version/hash and base refs |
| READY | Dependencies and contracts sufficient to start | Owner accepts task; blockers explicit |
| IN_PROGRESS | AI implementation underway | Branch and progress record |
| IMPLEMENTED | Change submitted by Owner | Commit SHA, changed-file list, self-check |
| VERIFIED | Automated/manual checks executed | Commands, environment, logs/results |
| REVIEWED | Independent review completed | Review report and finding disposition |
| INTEGRATION_READY | Cross-module contracts compatible | Integration evidence and updated registry |
| ACCEPTED | Acceptance authority approves | Explicit acceptance record |
| MERGED | Approved change integrated | Merge commit and target branch |
| CLOSED | Traceability and follow-up complete | Work item index updated |

A task MUST NOT skip a required gate. “Implemented” is not “Verified”; “Verified” is not “Reviewed”; “Reviewed” is not “Accepted”; “Accepted” is not “Merged”.

### 4.2 Blocked and rejected states

Use **BLOCKED** when a required contract, decision, permission, dependency or environment is unavailable. Record the blocker owner and resolution condition.

Use **REJECTED** when the proposed approach is invalid or unacceptable. Preserve the prompt and review record; do not erase failed attempts.

## 5. Prompt engineering as controlled engineering / 提示词工程化

A task prompt is a versioned engineering artifact, not disposable chat text.

Every prompt MUST include:

1. Work Item ID, prompt ID, version, status and task class/risk.
2. Objective and observable outcome.
3. Accountable Owner, implementer role and independent reviewer role.
4. Repository, branch, base commit SHA and relevant dependency SHAs.
5. Required source documents and exact paths.
6. Scope: allowed files/modules and explicit non-goals.
7. Normative constraints, invariants and authority boundaries.
8. Required design/implementation steps.
9. Acceptance criteria stated as observable conditions.
10. Test plan, exact commands where known, fixtures and expected results.
11. Security, failure, concurrency, recovery and compatibility considerations as applicable.
12. Required deliverables and report format.
13. Commit, read-back, branch-head and evidence requirements.
14. Stop conditions and escalation path for ambiguity or conflicting contracts.

Prompts MUST be reviewed before execution. Prompt changes after execution starts MUST create a new version and record the reason and impact. The previous prompt version remains immutable and retrievable.

AI MUST NOT invent missing approvals, dependencies, test results, file paths, commits, or Owner decisions. If inputs conflict, stop at the affected boundary, document the conflict and request an authorized decision.

## 6. Branching and change discipline / 分支与变更纪律

- One work item SHOULD map to one dedicated branch or a clearly isolated branch segment.
- Suggested branch format: `ai/<work-item-id>/<owner>-<short-topic>`.
- Do not combine unrelated work items in one commit series.
- Module Owners modify only files within their ownership unless an explicit integration task authorizes a cross-cutting change.
- Cross-owner edits require notification, impact analysis and approval from the affected Owner.
- No direct push to protected integration branches unless repository policy explicitly permits it.
- No merge based only on an AI self-review.
- Each implementation commit SHOULD be small, reviewable and use a meaningful message.
- Generated code, schemas, migrations and lockfiles MUST be reviewed as source artifacts, not treated as harmless generated output.

## 7. Definition of Ready / Definition of Done

### Definition of Ready (DoR)

A task is READY only when:

- the outcome and non-goals are explicit;
- one accountable Owner is assigned;
- relevant architecture/contracts and base SHAs are identified;
- dependencies are available or explicitly accepted as assumptions;
- acceptance criteria are testable;
- security/data/compatibility impact is classified;
- the prompt is stored, versioned and reviewed;
- no unresolved blocker makes safe work impossible.

### Definition of Done (DoD)

A task is DONE only when applicable conditions are satisfied:

- code/docs match the approved prompt and scope;
- formatting, lint, build and type checks pass where applicable;
- unit, integration, contract and regression tests pass at the required level;
- negative/failure-path tests cover critical invariants;
- security and permission checks are tested for relevant changes;
- migration/rollback/compatibility behavior is documented and tested where relevant;
- independent review findings are resolved or explicitly accepted as residual risk;
- bilingual normative documentation is updated where architecture/contract behavior changes;
- commit SHA, test evidence, review report and final status are recorded;
- integration and acceptance authority have explicitly accepted the result.

If a check cannot run, record **NOT RUN** with reason. Never report it as PASS.

## 8. Verification model / 验证模型

Use layered evidence:

1. Static checks: formatting, lint, type checks, schema validation, dependency/license checks.
2. Unit tests: local invariants and state transitions.
3. Component integration tests: persistence, queues, indexes, protocol adapters.
4. Contract/conformance tests: cross-owner compatibility and wire semantics.
5. Fault-injection tests: crashes, retries, duplicate messages, lost ACKs, reordering, stale epochs and recovery.
6. Security tests: authorization boundaries, scope isolation, untrusted memory and prompt injection.
7. Workload benchmarks: representative data, hardware, warm/cold conditions, latency, throughput and resource use.
8. End-to-end acceptance: user-visible system behavior and operational recovery.

A test result is valid only with test identity, code commit, environment, command/configuration, input fixture, expected result, actual result and outcome. Performance claims MUST include workload and hardware context. Security claims MUST identify tested threat model and coverage; passing tests do not prove absence of vulnerabilities.

## 9. Review and acceptance / 审查与验收

Independent review MUST evaluate at least:

- requirement coverage and scope discipline;
- domain correctness and ownership boundaries;
- API/schema/protocol compatibility;
- data integrity, transaction and concurrency behavior;
- failure handling, idempotency, replay and recovery;
- security, identity, authorization and isolation;
- tests, observability and maintainability;
- documentation and traceability.

Findings use:

- **BLOCKER:** unsafe, incorrect, or prevents integration;
- **P0:** critical invariant/security/data-integrity defect;
- **P1:** major contract or correctness gap;
- **P2:** important quality or maintainability issue;
- **P3:** minor improvement.

Review disposition: PASS, CONDITIONAL PASS, FAIL, or NOT REVIEWABLE. Every finding has an ID, evidence, owner, severity, status and closure condition. Conditional Pass MUST list restrictions and MUST NOT be presented as full acceptance.

## 10. Architecture and implementation status vocabulary

Use separate statuses; do not collapse them:

- **DECIDED:** approved normative contract.
- **CANDIDATE:** proposal awaiting approval.
- **OPEN:** unresolved question.
- **TO_VALIDATE:** requires experiment or implementation evidence.
- **IMPLEMENTED:** code exists at a named commit.
- **TESTED:** named checks executed with recorded results.
- **REVIEWED:** independent review completed.
- **ACCEPTED:** authorized acceptance recorded.
- **MERGED:** integrated into the named target branch.

A document existing does not mean a decision is approved. A passing unit test does not prove system-level correctness. A commit does not prove deployment or runtime behavior.

## 11. Change management and learning loop / 变更与反馈

When implementation reveals a contract defect:

1. stop or isolate the unsafe part;
2. open a finding/change request;
3. identify authoritative Owner(s);
4. revise the contract through a decision record;
5. version affected prompts;
6. update dependent tasks and compatibility tests;
7. resume only after required approvals.

At the end of each iteration, record: expected vs actual, escaped defects, prompt ambiguity, rework causes, test gaps, review effectiveness, cycle time and next process improvement. Improve templates and automation based on evidence; do not weaken gates merely to increase throughput.

## 12. Initial governance status / 初始治理状态

This document is a proposed baseline until explicitly approved by the project's governance authority. Existing A–I module authority remains unchanged. Adoption does not retroactively convert previous work into compliant work; prior artifacts may be mapped to this standard with clearly marked evidence gaps.

---

# Appendix A — Minimum task record

- Work Item ID:
- Title / Class / Risk:
- Sponsor:
- Accountable Owner:
- Implementing AI session:
- Independent Reviewer:
- Prompt ID / Version / SHA-256:
- Base branch / SHA:
- Dependency SHAs:
- Scope / Non-goals:
- Acceptance criteria:
- Test plan:
- Security and compatibility impact:
- Implementation commit(s):
- Verification evidence:
- Review report:
- Acceptance record:
- Final state:
