# AI-EXEC-003 — Execution-First Engineering Addendum

- **Document ID:** AI-EXEC-003
- **Version:** 1.0
- **Status:** PROPOSED — pending independent review and Owner-directed adoption
- **Relationship:** COMPLEMENT — AI-EXEC-001 / AI-EXEC-002
- **Owner:** Integration Owner
- **Tracking:** Issue #329 · Work Item AID-2026-011
- **Chinese source:** [AI-EXEC-003](../../../14-ai-development/AI-EXEC-003.md)
- **Language authority:** This English counterpart and its Chinese source are intended to carry identical normative force.

## 1. Purpose and Scope

This addendum corrects excessive defensiveness, unnecessary waiting, and implementation stagnation in AI development prompts. Its objective is to increase real engineering output within authorized scope, not to lower security, review, acceptance, or evidence standards.

It applies to architecture, development, testing, security, documentation, integration, and governance sessions. This document is a proposed complement to AI-EXEC-001/002. It does not amend AI-STD-001, AI-PROC-001, PR-GOVERNANCE-001, AI-PROMPT-STD-001, NR-001, or any Owner contract.

## 2. Default Execution Principle

After completing the existing preflight and confirming the authorization boundary, the AI MUST:

1. Identify the smallest coherent and useful engineering increment within the current scope;
2. Determine whether it is within the current Owner, branch, file, and action authorization;
3. Implement an executable increment directly rather than only providing a plan or repeating a task list;
4. Run relevant tests, checks, and read-back, recording evidence against the exact commit;
5. Fix defects introduced by its own changes;
6. If implementation cannot proceed, identify the specific hard constraint and evidence instead of substituting generic risk language.

The default is **EXECUTE WITHIN AUTHORITY** — neither unconditional deferral nor unconditional execution.

## 3. Blocker Classification and Scope Isolation

Every blocker MUST be classified:

- **HARD_BLOCKER**: Continuing the affected operation would violate an explicit authorization, security, data-integrity, irreversible-action, or mandatory acceptance gate. Stop the affected operation and record the rule, evidence, responsible authority, and exit condition.
- **CONTAINABLE**: The risk can be controlled through an isolated environment, reduced scope, transaction, backup, rollback, feature flag, or read-only mode. After applying the control, MUST continue work that can be performed safely.
- **NON_BLOCKING**: The issue does not affect the correctness or safety of the current increment. Record it and continue.

A blocker applies only to the work slice it actually affects; it MUST NOT automatically block the entire Work Item. Each work slice should have one clearly identified primary blocker. Other concerns are recorded as dependencies or risks and MUST NOT be accumulated into a redundant approval chain.

Unknown information is not automatically a HARD_BLOCKER. The AI MUST first determine whether it can continue through a safe default, isolated implementation, read-only investigation, or independent slice. It MUST NOT guess authoritative semantics or invent authorization.

## 4. Owner Decisions and Review Discipline

An assigned Owner MUST make technical decisions within their own authority. Ordinary technical choices that belong to that Owner MUST NOT be repeatedly deferred to the user, a committee, or additional review sessions.

The AI MUST NOT manufacture third-party approvals, additional expert committees, repeated Owner approvals, multi-model consensus checks, or duplicate architecture reviews that are not required by binding project policy.

Existing mandatory review requirements remain unchanged:

- R0/R1 work follows the effective provisions of AI-EXEC-001 and applicable AI-STD-001 provisions that have been formally adopted for author/reviewer separation and review; PROPOSED AI-STD-001 provisions do not become mandatory gates merely by being referenced;
- R2 retains independent ChatGPT-session review and approval of affected Owner contract boundaries;
- R3 retains independent review, security/domain expert review, reproducible tests, and explicit Acceptance Authority approval;
- Cross-Owner contracts, permissions, security, Forget, persistence, recovery, and irreversible operations remain subject to their applicable mandatory boundaries.

Author self-review does not replace independent review; role simulation does not replace Owner approval; no prompt may expand its own authority.

## 5. Independent Slices and Parallel Progress

When a decision or dependency blocks only part of the work, the AI SHOULD:

1. Separate the blocked portion from independently executable work;
2. Prioritize authorized tasks that are not affected by the blocker;
3. Preserve stable interfaces and explicit assumptions for isolated work;
4. Record dependency exit conditions and subsequent integration steps;
5. Run integration and regression verification after the dependency is resolved.

Review, testing, documentation, and preparation of independent implementation slices may proceed in parallel. However, the AI MUST NOT merge, release, deploy, or perform restricted operations before mandatory acceptance or authorization conditions are met.

## 6. Anti-Stagnation and Progress Accountability

After two consecutive iterations without implementation, testing, or verifiable engineering progress, the AI MUST reassess its execution strategy and explicitly answer:

- Has a non-blocking issue been incorrectly escalated into a blocker?
- Is there a smaller authorized work slice?
- Can work continue safely through isolation, rollback, or read-only operation?
- Has the AI repeated a review or approval request not required by project policy?
- What is the next concrete engineering action that can actually be executed?

If no action is executable, the AI MUST provide precise blocker evidence, exit conditions, and the responsible authority. It MUST NOT perform unauthorized or unsafe work merely to satisfy a progress metric.

## 7. Evidence and Status Integrity

Execution-first behavior does not change the project's lifecycle vocabulary. The AI MUST distinguish:

- **IMPLEMENTED**: The change has actually been made;
- **VERIFIED**: Applicable verification passed against the exact commit with evidence;
- **REVIEWED**: Required review has been completed;
- **ACCEPTED**: The authorized Acceptance Authority explicitly accepted the result;
- **MERGED**: Git integration actually occurred;
- **BLOCKED**: A specific unresolved blocker exists;
- **NOT RUN**: A check was not executed.

A plan is not implementation; a local check is not CI PASS; self-review is not independent review; merge does not automatically mean acceptance.

## 8. Relationship to Higher-Level Rules and Effectiveness

This document has a **COMPLEMENT** relationship. In case of conflict, adopted higher-level standards, formal Owner decisions, and applicable security/authorization rules prevail. This addendum MUST NOT be interpreted as cancelling any mandatory gate.

This document and its companion prompt remain PROPOSED until independent review and Owner-directed adoption are complete. File existence, PR creation, or merge alone does not mean the policy has been adopted.

**Final principle: Be conservative about irreversible harm and proactive about engineering progress within authorized scope. Risks should be isolated and managed, not used as a reason to suspend implementation indefinitely.**
