# AI Development Governance
# AI 开发治理

This directory defines how all AI developers work on AiMemoryBrainArchitecture. It is the project's engineering operating model, not an Agent framework specification.

本目录规定 AiMemoryBrainArchitecture 的全部 AI 开发活动如何组织、执行、验证和审计。

## Normative documents

1. [AI Development Standard](ai-development-standard.md) — roles, authority, task gates, DoR/DoD, verification and acceptance.
2. [AI Development Iteration Lifecycle](iteration-lifecycle.md) — the end-to-end development loop and multi-Owner collaboration patterns.
3. [AI Work Item and Prompt Record Template](prompt-and-evidence-template.md) — immutable prompt versions, task manifest and evidence bundle.

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


## Canonical prompt library / 规范提示词库

All reusable AI prompts MUST be stored in the repository-root `prompts/` directory before execution. The directory structure is mandatory:

- Global prompts are placed directly under `prompts/`.
- Owner-specific prompts are placed only under `prompts/A/` through `prompts/I/`.
- Cross-owner work combines the global prompts with the relevant Owner prompt(s).
- Executed prompt versions are immutable and copied into the corresponding `14-ai-development/work-items/AID-YYYY-NNN/` evidence bundle with Prompt ID, version and SHA-256.

Start at [Prompt Library](../prompts/README.md). Every session MUST read [Global Project Developer](../prompts/global-project-developer.md) and [Global Bilingual Documentation](../prompts/global-bilingual-documentation.md), plus its assigned [Owner prompt](../prompts/). Review sessions MUST also read [Global Architecture Reviewer](../prompts/global-architecture-reviewer.md).

全局可复用提示词必须直接存放在仓库根目录的 `prompts/` 下；A–I 专属提示词必须分别存放在 `prompts/A/` 至 `prompts/I/`。跨 Owner 工作组合全局提示词和相关 Owner 提示词。执行过的提示词版本必须保持不可变，并将实际执行版本及 Prompt ID、版本、SHA-256 复制到对应 Work Item 证据包。
