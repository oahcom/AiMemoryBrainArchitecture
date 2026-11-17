# AID-2026-001 — ChatGPT-native execution model

**Prompt ID:** AID-2026-001-PROMPT  
**Version:** v1  
**Class/Risk:** ARCH / R2  
**Accountable Owner:** A — Principal Integration Architect  
**Status:** EXECUTED FOR PROPOSAL DRAFT; independent review pending

## Role

Act as Owner A for repository `oahcom/AiMemoryBrainArchitecture`. Define an execution model that uses ChatGPT ordinary conversations as the only AI execution channel.

## Verified premise

The project has already verified that ChatGPT conversations can use the connected GitHub app to inspect and modify repository content, Issues and Pull Requests. Do not repeat that capability POC or replace it with another interface.

## Hard constraints

- ChatGPT ordinary conversations are the only AI reasoning and authoring environment.
- No OpenAI API key, Responses API worker, Codex CLI, Codex Cloud, third-party model, local model, Desktop Commander, browser-cookie reuse, or local-computer relay.
- GitHub is the durable source of truth for requirements, prompts, decisions, branches, commits, PRs and evidence.
- Ubuntu may run deterministic build, test and CI jobs. It must not invoke an AI model, poll tasks for model execution, or store ChatGPT credentials.
- Preserve A–I domain ownership, separate review conversations, bilingual architecture documentation, and global plus Owner-specific prompt storage.
- Do not claim unattended/event-driven ChatGPT execution unless a currently supported ChatGPT-native capability and the account's eligibility are demonstrated.
- Do not make ChatGPT Scheduled Tasks a core dependency. Official limits for Free include at most three active tasks, no more than one recurring run per day, and no event-triggered tasks.

## Required work

1. Read the current AI development governance documents and bilingual documentation policy.
2. Define ChatGPT conversation as the execution unit and explain how Owner-specific conversations share state through GitHub.
3. Define A as coordinator without taking over B–I domain decisions.
4. Define independent review using a separate conversation with frozen inputs; explicitly state that this provides context separation, not a different model or statistical independence.
5. Distinguish interactive conversation-driven development from unattended event-driven execution.
6. Define the role of Ubuntu as deterministic CI/test infrastructure only.
7. Define prompt storage: global prompts directly under `14-ai-development/prompts/global/`; Owner prompts under `14-ai-development/prompts/owners/<A-I>/`.
8. Provide Chinese and English documents with semantic parity.
9. Create a Draft PR and leave review/acceptance pending.

## Stop conditions

Stop and mark OPEN if a required capability is not supported by the already-validated ChatGPT/GitHub workflow. Do not invent a backend interface, API, webhook trigger, or account entitlement. Do not merge.

## Acceptance criteria

- No forbidden AI execution dependency appears in the proposed architecture.
- Every AI action is initiated inside ChatGPT ordinary conversations.
- GitHub is the durable cross-session coordination and evidence layer.
- Ubuntu only executes deterministic CI/test workloads.
- A–I authority and separate review boundaries are explicit.
- The model makes no promise of 24/7 unattended execution under Free constraints.
- Bilingual semantic parity is checked.
- Independent review is performed in a separate conversation before acceptance.
