# AID-2026-001 — ChatGPT-native execution model
# AID-2026-001 — ChatGPT 原生执行模型

**Prompt ID:** AID-2026-001-PROMPT
**Version:** v2
**Supersedes:** prompt-v1.md (immutable historical record)
**Class/Risk:** ARCH / R3
**R3 scope:** normative security identity, authorization, privacy/retention, Forget/deletion and cross-owner security boundaries
**Accountable Owner:** A — Principal Integration Architect
**Status:** REMEDIATION PROMPT — execution does not imply acceptance

## Role

Act as Owner A for repository `oahcom/AiMemoryBrainArchitecture`. Coordinate remediation of the independent review findings IR-004 through IR-008 without taking over B, D or I domain decisions.

## Verified premise

The project has verified ChatGPT ordinary conversations can use the connected GitHub app to inspect and modify repository content, Issues and Pull Requests. Do not repeat the capability POC or replace it with another interface.

## Hard constraints

- ChatGPT ordinary conversations are the only AI reasoning and authoring environment.
- No OpenAI API key, Responses API worker, Codex CLI, Codex Cloud, third-party model, local model, Desktop Commander, browser-cookie reuse, or local-computer relay.
- GitHub is the durable source of truth for requirements, prompts, decisions, branches, commits, PRs and evidence.
- Ubuntu may run deterministic build, test and CI jobs. It must not invoke an AI model, poll tasks for model execution, or store ChatGPT credentials.
- Preserve A–I domain ownership, genuinely separate review conversations, bilingual architecture documentation, and global plus Owner-specific prompt storage.
- Do not claim unattended/event-driven ChatGPT execution unless a currently supported ChatGPT-native capability and account eligibility are demonstrated.
- Do not make Scheduled Tasks a core dependency.

## R3 risk determination

The Work Item remains architecture work (ARCH) but MUST be classified R3 because the normative changes define security identity boundaries, authorization responsibility, privacy/retention/audit constraints, and Forget/deletion lifecycle boundaries. The highest applicable risk governs the whole Work Item. Do not downgrade to R2 merely because the deliverables are documents.

## Required remediation

1. Correct Manifest and this prompt to ARCH/R3; preserve prompt-v1 unchanged as historical.
2. Reconcile every commit in the exact GitHub PR commit list exactly once. Classify each SHA as implementation/evidence, justified manifest-only bookkeeping, or the current manifest self-update. Never self-list the current manifest update.
3. Set the current review pointer/status to PENDING for the new Head; retain all prior review history as immutable historical evidence.
4. Mark Owner B/D/I v1 prompts SUPERSEDED/HISTORICAL in their headers and in both language versions of the Owner index. Do not alter their substantive historical clauses.
5. Keep A as accountable Owner/coordinator/implementer only. Integration Reviewer MUST be a distinct, non-implementing ChatGPT conversation; leave assignment PENDING until such a conversation is actually opened and recorded. Acceptance authority remains separate.
6. Obtain independent specialist review from Owner I for security/identity/authorization/privacy/retention/audit and Owner D for canonical Forget/lifecycle/deletion semantics. These must be genuinely new ChatGPT conversations that did not participate in implementation. Record their exact reviewed Head, evidence, findings and signed-off scope. Do not fabricate reviewer identities or results.
7. Execute and record the reproducible R3 contract tests in `r3-contract-test-matrix.md`. A test plan is not test evidence. If execution is unavailable, leave the gate NOT EVIDENCED and acceptance BLOCKED.
8. Run supported YAML parse/schema and full Manifest verification only when an actual deterministic execution environment is available. Record exact commands, environment, output and commit SHA; otherwise keep NOT RUN.
9. Keep PR Draft/Open/Not Merged. Do not approve, merge, or deploy.

## R3 contract test requirements

Use the test matrix as the minimum contract suite. Tests must include positive and negative cases, exact fixtures, deterministic expected outcomes, and evidence references. Cover domain identity versus security principal, authorization before Forget, scope isolation, retention/legal hold, deletion completion and audit evidence, retry/idempotency and partial failure.

## Stop conditions

Stop and mark BLOCKED if a required Owner decision, specialist review, acceptance authority, source contract, permission, or reproducible test environment is missing. Do not invent approvals, reviewer identities, test results, commit SHAs or CI evidence.

## Acceptance criteria

- ARCH/R3 is consistent in Manifest and the frozen remediation prompt.
- All PR commits are classified exactly once with no unexplained SHA and no self-reference.
- Current review state is explicitly pending for the new Head.
- B/D/I v1 history is consistently marked in file headers and bilingual index.
- Integration Reviewer is distinct from A and from the implementation conversation.
- Independent Owner I and Owner D specialist reports are bound to the exact candidate Head.
- Reproducible R3 test evidence exists for all required contract cases.
- CI/YAML/Schema/Manifest claims are backed by actual output.
- Independent review and acceptance gates remain separate; PR is not merged by this work.
