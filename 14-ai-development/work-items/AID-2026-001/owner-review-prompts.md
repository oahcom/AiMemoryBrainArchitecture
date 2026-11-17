# AID-2026-001 — A–I Independent Domain Review Prompts
# A–I 九个 Owner 独立领域审查提示词

**Work Item:** AID-2026-001  
**Class / Risk:** ARCH / R2  
**Review target base:** `main` at `55d44b9276456f88bd2193de8b06aff146c228a4`  
**Target documents:** AI-STD-001 v1.0 PROPOSED, AI-PROC-001 v1.0 PROPOSED, AI-TPL-001 v1.0 PROPOSED  
**Purpose:** Produce nine separately attributable Owner reviews. These are review instructions, not approvals.

## Common instructions — mandatory for every Owner session

You are the named Owner for exactly one domain (A, B, C, D, E, F, G, H or I) in repository `oahcom/AiMemoryBrainArchitecture`.

Review the target governance documents as an engineering control system for a project developed by AI. Do not rubber-stamp them. Review from your own domain's authority and identify where the standard would fail, conflict with, weaken or leave ambiguous your domain's invariants.

### Required source material

Read the complete contents of:
- `14-ai-development/README.md`
- `14-ai-development/ai-development-standard.md`
- `14-ai-development/iteration-lifecycle.md`
- `14-ai-development/prompt-and-evidence-template.md`
- `14-ai-development/work-items/INDEX.md`
- root `README.md`

Also read your domain's current authoritative design and the latest relevant integration findings on your own branch. Record exact branch name, branch HEAD SHA, file paths and blob SHAs. If a referenced source cannot be read, mark NOT REVIEWABLE for that question; do not infer its contents.

### Independence and attribution

- This review must be performed in a dedicated session that did not author the governance documents or implementation changes under review.
- Do not rely on another Owner's conclusion as a substitute for your own analysis.
- Do not treat a role-played panel, a shared coordinator summary, or another Owner's report as your approval.
- Record the actual session identity/label available to you. Do not invent a human identity or separate agent identity.
- The review author must not modify the governance baseline in this task.
- Do not approve project-wide governance authority outside your own domain.

### Required review questions

1. Does AI-STD-001 preserve your domain authority and prevent other Owners/AI agents from silently redefining it?
2. Are task classification, risk levels, DoR/DoD and stop conditions sufficient for changes in your domain?
3. Does the prompt template force the inputs, invariants, tests, evidence and exact source versions your domain needs?
4. Does the lifecycle establish the right dependency order, cross-owner approval and integration handoff?
5. Are independence, review, acceptance and merge controls enforceable rather than aspirational?
6. Are failure, retry, rollback, replay, recovery and audit requirements adequate where relevant?
7. What exact text should be added, removed or changed? Give proposed wording, not just general advice.
8. Identify any BLOCKER/P0/P1/P2/P3 findings and the evidence that supports each.
9. Give a disposition: PASS, CONDITIONAL PASS, FAIL or NOT REVIEWABLE. List restrictions for any conditional pass.

### Required deliverables

Create a report at:
`14-ai-development/work-items/AID-2026-001/reviews/<OWNER>-review.md`

The report must include:
- Owner and domain;
- actual session label;
- exact branch and HEAD SHA;
- source paths and blob SHAs actually read;
- independent analysis;
- findings with stable IDs, severity, evidence, required change, and closure condition;
- exact proposed normative wording;
- disposition and residual risks;
- explicit statement that this is a domain review, not final project-wide approval.

Do not edit the governance standard, do not merge branches, and do not claim tests were run unless they were.

---

## A — Principal Integration Architect

Focus on:
- A's authority to maintain the Contract Registry and adjudicate cross-module conflicts versus project governance authority to approve the AI Development Standard itself;
- parent/child Work Item model for cross-module tasks, owner sign-offs and integration evidence;
- distinction between local owner acceptance, bilateral agreement, multi-owner agreement, integration acceptance and project-level governance approval;
- status vocabulary and traceability across branches/SHAs;
- how A handles conflicting Owner findings and dissent without erasing minority positions.

Decide whether the current standard gives A too much, too little, or correctly bounded authority. Propose an explicit governance approval path and decision record schema.

## B — Domain Model Architect

Focus on:
- protection of canonical domain semantics and the rule that Owners decide only within their domains;
- requirement/assumption/proposal/decision distinctions in prompts and task records;
- schema evolution, identity, typed references, lifecycle semantics and ADR handling;
- domain model review obligations for generated schemas, migrations, fixtures and compatibility;
- how AI must avoid inventing facts or turning candidate concepts into normative domain objects.

Propose domain-specific DoR/DoD and schema/ADR evidence requirements.

## C — Agent Integration Architect

Focus on:
- inference-boundary and Adapter ownership;
- telemetry, Task State, Intent, Plan Summary, Tool Call/Pending Action, Observation, Outcome, Uncertainty, Risk Signal and Environment Delta distinctions;
- prohibitions against requiring raw chain-of-thought or exposing protected system/developer instructions;
- final-request evidence, Applied semantics, Agent/Runtime/Adapter identity and capability boundaries;
- compatibility requirements across Agent frameworks and models.

Propose mandatory prompt constraints and conformance evidence for Agent-facing changes.

## D — Memory Brain Architect

Focus on:
- Canonical Memory authority, lifecycle, immutable revisions, evidence/provenance and conflict preservation;
- Forget as a high-risk operation: durable fence, target inventory, producer admission/barrier, suppression versus cleanup versus physical erasure;
- prohibition on claiming global Forget completion from local module evidence;
- transaction, cursor, recovery and canonical write serialization requirements;
- domain-owner stop conditions where implementation would violate memory integrity.

Propose mandatory Forget/data-integrity review and fault-injection gates.

## E — Memory Compiler Architect

Focus on:
- Event/Accepted Receipt/Memory Candidate/Canonical Commit distinctions;
- idempotency, retries, leases, DLQ, replay, recompile and derivative lineage;
- durable producer registration before execution and derivative dependency registration before visibility;
- final publish gate and re-check of current Forget fence and authorization;
- model-generated extraction being candidate evidence, not canonical truth.

Propose mandatory compiler replay/failure-path tests and artifact lineage evidence.

## F — Memory Runtime Architect

Focus on:
- retrieval correctness, Scope-before-Candidate, index/channel watermarks, stale cache and Working Set invalidation;
- in-flight query cancellation/finalization and Forget suppression races;
- activation recommendations versus ownership of Context versions;
- latency/resource budgets and representative workload benchmarks;
- cache/index rebuild correctness and failure recovery.

Propose mandatory runtime conformance, cache invalidation and benchmark gates.

## G — Memory Context Architect

Focus on:
- ContextVersion, ChangeSet, Delivery and Applied authority boundaries;
- immutable version sequence, CAS/base version, reconciliation and stale delivery handling;
- Context Remove versus canonical Forget;
- invalidation on Forget, permission revocation, scope changes and canonical supersession;
- proof that Applied refers to the exact final request and managed region, not a local buffer write.

Propose mandatory context state-machine and delivery evidence requirements.

## H — BMCP Protocol Architect

Focus on:
- wire/schema versioning, canonical encoding, typed identifiers, envelope identity and compatibility;
- Delivery/ACK idempotency, replay protection, anti-replay, ordering and unknown outcomes;
- authenticated transport identity versus payload identity claims;
- Adapter capability epochs and final-request boundary evidence;
- backward/forward compatibility, golden vectors and protocol conformance fixtures.

Propose mandatory protocol review, schema compatibility and golden-vector gates.

## I — Security & Governance Architect

Focus on:
- principal authentication, ActorRef/ScopeRef, delegation, authorization, permission epochs and least privilege;
- untrusted memory/evidence and prompt-injection defense;
- secrets/credentials and sensitive data handling in prompts, logs, test fixtures and evidence bundles;
- Forget, retention, backup, external recipient and physical-erasure policy;
- threat model, adversarial testing, independent security review and risk acceptance authority.

Propose mandatory security review triggers, adversarial tests and who may accept residual R3 risk.

---

## A final integration review — execute only after A–I reports are present

A acts as Principal Integration Architect, not as a substitute for the nine domain reviews.

A must:
1. Verify each report's provenance, source SHAs and independent-session declaration.
2. Build a finding matrix with owner, severity, overlap, conflict and closure condition.
3. Separate domain decisions from project-wide governance decisions.
4. Resolve wording conflicts only within A's integration authority; escalate authority/policy questions to the Project Governance Authority.
5. Preserve dissent and conditional approvals.
6. Update the governance documents only after the affected Owner has reviewed the proposed correction.
7. Issue one integration disposition: PASS, CONDITIONAL PASS, FAIL or NOT REVIEWABLE.
8. State exactly whether AI-STD-001 / AI-PROC-001 / AI-TPL-001 may become DECIDED, and what explicit project-governance approval remains required.
9. Never describe this review pack as nine independent approvals until nine separate reports with verifiable provenance exist.
