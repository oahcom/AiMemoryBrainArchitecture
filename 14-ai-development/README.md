# AI Development Governance
# AI 开发治理

This directory defines how all AI developers work on AiMemoryBrainArchitecture. It is the project's engineering operating model, not an Agent framework specification.

本目录规定 AiMemoryBrainArchitecture 的全部 AI 开发活动如何组织、执行、验证和审计。

## Normative documents

1. [AI Development Standard](ai-development-standard.md) — roles, authority, task gates, DoR/DoD, verification and acceptance.
2. [AI Development Iteration Lifecycle](iteration-lifecycle.md) — the end-to-end development loop and multi-Owner collaboration patterns.
3. [AI Work Item and Prompt Record Template](prompt-and-evidence-template.md) — immutable prompt versions, task manifest and evidence bundle.
4. [Owner Automation Operating Model](owner-automation-operating-model.md) — GitHub Issue/PR collaboration and per-Owner scheduled execution.
5. [AI Prompt Authoring Standard](prompt-authoring-standard.md) — A's prompt-authoring process, Owner approvals, quality gates and hashing.

## Required usage

- Every substantive task MUST have a Work Item ID and a repository-stored prompt before execution.
- Every task MUST have one accountable Owner and a distinct independent reviewer.
- Every implementation MUST be tied to a base SHA, branch, commit SHA and verification evidence.
- Every review finding MUST have an owner and closure evidence.
- No status may be upgraded without its required evidence.

## Suggested IDs and paths

- Work Item: `AID-YYYY-NNN`
- Prompt: `AID-YYYY-NNN-PROMPT-vN`
- Review: `AID-YYYY-NNN-REV-N`
- Branch: `ai/AID-YYYY-NNN/<owner>-<topic>`
- Evidence: `14-ai-development/work-items/AID-YYYY-NNN/`

## Status

These documents are an initial **PROPOSED** governance baseline. They do not retroactively certify earlier work. Adoption and any later normative change require an explicit governance decision.
