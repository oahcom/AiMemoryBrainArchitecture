# ChatGPT-Native AI Development Execution Model

- Document ID: AI-ARCH-002
- Version: 0.1
- Status: **PROPOSED — NOT APPROVED**
- Owner: A — Principal Integration Architect
- Chinese counterpart: [ChatGPT 原生 AI 开发执行模型](chatgpt-native-execution-model.zh-CN.md)
- Parent: AI-STD-001, AI-PROC-001
- Work Item: AID-2026-001

## 1. Decision summary

Use **ordinary ChatGPT conversations with the already-validated GitHub connected-app workflow** as the only AI reasoning, design, coding, and review channel.

GitHub is the durable coordination and evidence system. Ubuntu is limited to deterministic build, test, and CI execution. No backend process is allowed to invoke an AI model.

This proposal intentionally defines a **conversation-driven development system**, not a 24/7 unattended AI service. It does not claim that GitHub events can wake or create ordinary ChatGPT conversations.

## 2. Verified baseline and non-goals

The project has already verified that ChatGPT conversations can use the connected GitHub app to inspect and modify repository content, Issues, branches, commits, and Pull Requests. This capability is an accepted premise; this work item does not repeat that POC.

This document does not design or authorize:
- OpenAI API / Responses API workers or API keys;
- Codex CLI, Codex Cloud, or Codex automations;
- any third-party or locally hosted model;
- Desktop Commander or a local-computer relay;
- browser-cookie extraction, session-token reuse, or private undocumented interfaces;
- GitHub Actions that call ChatGPT or any model endpoint.

## 3. System boundary

### 3.1 ChatGPT conversation

A ChatGPT conversation is the only AI execution unit. The conversation reads its task, prompt, contracts, and current repository state from GitHub; performs authorized reasoning and repository operations through the connected GitHub app; and records results back to GitHub.

A conversation is interactive and user-started. A task may span multiple turns and can be resumed in a later conversation from its durable GitHub records.

### 3.2 GitHub

GitHub is the cross-conversation source of truth for:
- Issues and task status;
- immutable global and Owner-specific prompts;
- architecture decisions and bilingual specifications;
- branches, commits, Pull Requests, and review comments;
- test-run links, evidence, findings, and acceptance records.

Conversation history is not the project database. A new conversation must be able to resume from the GitHub Work Item, prompt version, exact SHAs, and evidence.

### 3.3 Ubuntu and GitHub Actions

Ubuntu may execute deterministic operations only: checkout, build, formatting, lint, unit/integration/conformance tests, packaging, and deployment steps that have separately approved runbooks.

Ubuntu MUST NOT:
- call an LLM or ChatGPT endpoint;
- use an API key, ChatGPT cookie, OAuth token, or browser session to impersonate ChatGPT;
- poll Issues in order to generate AI work;
- autonomously author code or review findings.

GitHub Actions may start deterministic CI in response to repository events. A CI result is evidence for ChatGPT to inspect; it is not an AI invocation mechanism.

**Current repository status:** the cleaned `main` branch currently contains no `.github/workflows/` files. The self-hosted runner may remain registered on the host, but this proposal does not claim that a repository CI workflow is currently configured or running. CI is **NOT CONFIGURED / NOT RUN** until a deterministic workflow is added, reviewed, and executed with evidence.

## 4. A–I conversation model

Each Owner has a distinct ChatGPT conversation context and a versioned Owner prompt:

| Owner | Conversation responsibility |
|---|---|
| A | Intake, prompt authoring, dependency sequencing, cross-owner integration, decision/evidence registry |
| B | Domain model and canonical domain semantics |
| C | Agent integration, telemetry, inference-boundary requirements |
| D | Canonical Memory Brain, memory lifecycle, Forget semantics |
| E | Memory Compiler and derived-memory production |
| F | Memory Runtime, retrieval, activation, working sets, runtime cache |
| G | Memory Context, ContextVersion, ChangeSet, reconciliation |
| H | BMCP and Adapter protocol behavior |
| I | Security, identity, authorization, and governance |

A coordinates work but MUST NOT replace a domain Owner's decisions. Each Owner may decide only within its approved authority and must escalate cross-owner conflicts.

A separate ChatGPT conversation performs independent review using the frozen prompt, task record, diff, exact SHAs, test evidence, and applicable contracts. It must not rely on the implementer's unrecorded chat context.

**Independence limitation:** separate conversations provide context separation and a fresh review pass; they do not provide a different model, provider, or statistical independence. The project MUST NOT describe this as multi-model consensus. High-risk acceptance remains subject to the project's explicit security and governance authority.

The system does not automatically create or launch nine conversations. The user starts the required Owner/reviewer conversations in ChatGPT and supplies the corresponding prompt. GitHub provides durable handoff between them.

## 5. End-to-end operating loop

1. **Register:** create a GitHub Issue and Work Item record with one accountable Owner, class/risk, scope, dependencies, and acceptance criteria.
2. **Prepare:** A creates or updates the global prompt and the relevant Owner prompt; prompt versions are immutable once executed.
3. **Start Owner conversation:** the user opens the Owner's ChatGPT conversation and provides the prompt and Work Item reference.
4. **Load authoritative state:** the Owner reads the exact source documents, Issue, branch/base SHA, dependency SHAs, and prior evidence from GitHub.
5. **Execute:** the Owner performs only its authorized design or implementation work through the connected GitHub app. It creates a task branch and records commits and changed paths.
6. **Verify:** GitHub Actions/Ubuntu run deterministic checks. ChatGPT inspects results and fixes failures through a new bounded change.
7. **Review:** a different ChatGPT conversation reads the frozen PR and evidence and records findings. The authoring conversation does not self-approve.
8. **Integrate:** A reconciles cross-owner compatibility and records integration status without overriding domain-owner authority.
9. **Accept and close:** authorized acceptance is recorded; merge occurs only after required evidence and approvals.

Every state transition is written to GitHub. “Implemented”, “Verified”, “Reviewed”, “Accepted”, and “Merged” remain distinct.

## 6. Prompt layout

Global instructions live directly under the global prompt directory. Each Owner's instructions live only in that Owner's directory.

```text
14-ai-development/
  prompts/
    global/
      chatgpt-session-contract-v1.md
    owners/
      A/owner-session-v1.md
      B/owner-session-v1.md
      C/owner-session-v1.md
      D/owner-session-v1.md
      E/owner-session-v1.md
      F/owner-session-v1.md
      G/owner-session-v1.md
      H/owner-session-v1.md
      I/owner-session-v1.md
```

Every Owner prompt MUST reference the global session contract, its authority boundary, the exact source-of-truth documents, the task's acceptance criteria, and stop conditions. Executed prompt versions are immutable.

## 7. Automation boundary and plan constraints

Ordinary ChatGPT conversations are the chosen AI channel. **ChatGPT Scheduled Tasks are not a core dependency** because they are a separate feature with plan-specific limits.

OpenAI's current Scheduled Tasks documentation states:
- Free and Go: at most 3 active scheduled tasks;
- Free: recurring tasks no more than once per day, with flexible time windows;
- Free and Go: no event-triggered (webhook-based) tasks;
- event-triggered GitHub PR tasks require an eligible Work plan.

Source: [Scheduled tasks in ChatGPT — OpenAI Help Center](https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt).

Therefore this proposal does not promise:
- 24/7 autonomous development;
- GitHub webhook → automatic ChatGPT invocation;
- automatic creation of A–I conversations;
- unlimited background task scheduling.

The supported operating mode is **user-triggered ChatGPT conversations + GitHub-persisted work state + deterministic CI**. If unattended event-driven execution becomes a mandatory requirement, the project must record it as BLOCKED under the current plan/feature constraints rather than silently substituting Codex, API calls, or another model.

## 8. Security and authority rules

- Only the connected GitHub app permissions already granted to ChatGPT may be used.
- Never request, store, print, or commit personal access tokens, OAuth credentials, browser cookies, or server passwords in prompts or repository files.
- No AI credentials are stored on Ubuntu.
- The self-hosted runner is not an AI worker. Keep its existing host-level admission protections until separately reviewed; do not add AI invocation jobs.
- No automatic merge. A human/project-authorized acceptance decision remains required.
- Do not claim a test, review, deployment, or runtime result without exact evidence.

## 9. Acceptance criteria for this proposal

- ChatGPT ordinary conversations are the only AI channel.
- GitHub is the durable cross-session state and evidence layer.
- Ubuntu/GitHub Actions execute deterministic checks only.
- A–I role boundaries and separate review conversations are explicit.
- The prompt directory separates global and Owner-specific instructions.
- Scheduled Tasks, Codex, API workers, Desktop Commander, other models, and local relays are not required.
- Interactive operation is not misrepresented as unattended automation.
- Chinese and English counterparts preserve identical semantics and status.

## 10. Open decisions

1. Whether the project accepts user-triggered conversation orchestration as the operating mode under the no-quota/no-API constraint.
2. Whether the existing governance standard should be amended to explicitly define “separate ChatGPT conversation” as context-independent review, with its model-independence limitation.
3. Which exact repository contracts and test suites each Owner prompt must load by default.

Until these are decided, AI-ARCH-002 remains **PROPOSED** and does not authorize production automation or autonomous execution.
