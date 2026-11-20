# Project Prompt Library / 项目提示词库

- Library ID: PROMPT-LIBRARY-001
- Version: 1.0
- Status: PROPOSED — pending governance-baseline adoption
- Repository: `oahcom/AiMemoryBrainArchitecture`

This is the canonical repository location for reusable AI prompts. Store prompts here before execution; do not rely on chat history as the only copy.

本目录是项目可复用 AI 提示词的规范存放位置。提示词必须在执行前存入仓库，不能只依赖聊天记录保存。

## 1. Directory rules / 目录规则

- Files directly under `prompts/` are **global prompts**. They apply across Owners and work types.
- `prompts/A/` through `prompts/I/` contain prompts owned by the corresponding Owner only.
- Do not put Owner-specific prompts at the root.
- Do not duplicate global policy text in Owner prompts. Reference the global prompt IDs and paths; Owner prompts may add stricter domain-specific requirements.
- Cross-owner work uses a global prompt plus one or more relevant Owner prompts. A multi-owner task must identify one accountable integration Owner and each participating Owner's bounded responsibility.
- Keep executed prompt versions immutable. Material changes create a new versioned file; never silently overwrite a prompt already used.

- Reusable executable global prompts remain directly under prompts/; Owner prompts remain under prompts/A/ through prompts/I/. The prompts/00-setup/ directory is reserved for non-executable templates, migration guides and setup aids; those files do not become global prompts or override the directory rules above.
- 可复用、可执行的全局提示词仍直接存放在 prompts/ 根目录；Owner 提示词仍存放在 prompts/A/ 至 prompts/I/。prompts/00-setup/ 专用于不可执行的模板、迁移指南和设置辅助材料；这些文件不因此成为全局提示词，也不改变上述目录规则。

- `prompts/` 根目录中的文件属于**全局提示词**，适用于所有 Owner 和工作类型。
- `prompts/A/` 至 `prompts/I/` 仅存放对应 Owner 负责的专属提示词。
- Owner 专属提示词不得放在根目录。
- 不要在 Owner 提示词中复制全局规范全文；应引用全局提示词 ID 和路径。Owner 提示词可以增加更严格的领域要求。
- 跨 Owner 任务使用全局提示词，并组合相关 Owner 提示词。多 Owner 任务必须指定一个集成责任 Owner，并明确每个参与 Owner 的职责边界。
- 已执行的提示词版本必须不可变。实质性修改应创建新版本文件，不得静默覆盖已执行版本。

## 2. Global prompts / 全局提示词

| Prompt ID | Path | Purpose |
|---|---|---|
| GLB-DEV-001 v1.1 (PROPOSED) | [English](global-project-developer.md) / [中文](global-project-developer.zh-CN.md) | Execution-first global developer baseline; AI-EXEC-003 remains proposed until adoption |
| GLB-REV-001 | [global-architecture-reviewer.md](global-architecture-reviewer.md) | Independent architecture review and evidence discipline |
| GLB-DOC-001 | [global-bilingual-documentation.md](global-bilingual-documentation.md) | Bilingual documentation execution requirements |

The execution-first policy source is [AI-EXEC-003](../14-ai-development/AI-EXEC-003.md) with its [English counterpart](../docs/en/14-ai-development/AI-EXEC-003.md). GLB-DEV-001 v1.1 and AI-EXEC-003 are PROPOSED; they do not override adopted governance or authorize restricted actions.

## 3. Owner prompts / Owner 专属提示词

| Owner | Directory | Responsibility |
|---|---|---|
| A | [A/](A/) | Charter, Phase 3 remediation prompt, technology review prompt |
| B | [B/](B/) | Charter, Phase 3 remediation prompt, technology review prompt |
| C | [C/](C/) | Charter, Phase 3 remediation prompt, technology review prompt |
| D | [D/](D/) | Charter, Phase 3 remediation prompt, technology review prompt |
| E | [E/](E/) | Charter, Phase 3 remediation prompt, technology review prompt |
| F | [F/](F/) | Charter, Phase 3 remediation prompt, technology review prompt |
| G | [G/](G/) | Charter, Phase 3 remediation prompt, technology review prompt |
| H | [H/](H/) | Charter, Phase 3 remediation prompt, technology review prompt |
| I | [I/](I/) | Charter, Phase 3 remediation prompt, technology review prompt |

## 4. Mandatory execution sequence / 强制执行顺序

1. Read this index and the applicable global prompts.
2. Read `00-governance/bilingual-documentation-policy.md` (GOV-DOC-001) and the relevant Chinese/English contract counterparts.
3. Read the applicable Owner prompt(s) and refresh all referenced branch heads, files and SHAs.
4. Copy the selected prompt into an immutable work-item record under `14-ai-development/work-items/` before execution; record Prompt ID, version and SHA-256.
5. Execute only within the authorized Owner boundary and assigned branch.
6. Return exact changed paths, branch/base/head SHAs, tests, review evidence, open issues and bilingual manifest.
7. Read back every changed artifact. Never claim tests, reviews, approvals or merges that did not occur.

## 5. Versioning and authority / 版本与权威

Prompt files guide task execution; they do not override approved governance, Owner authority, ADRs, or normative architecture specifications. If a prompt conflicts with a newer approved source, stop, report the conflict, and request prompt maintenance.

提示词用于指导任务执行，不能覆盖已批准治理规范、Owner 权限、ADR 或规范性架构文档。如果提示词与更新的已批准规范冲突，必须停止并报告冲突，先维护提示词。

The prompts in this directory are PROPOSED until adopted through the repository's approved governance process. A prompt's presence does not itself grant implementation, merge, security-risk-acceptance, or contract-freeze authority.


## 6. Seven-section prompt template and migration guide / 七章节提示词模板与迁移指南

- English template: [TEMPLATE-v2.md](00-setup/TEMPLATE-v2.md) / [中文模板](00-setup/TEMPLATE-v2.zh-CN.md)
- English migration guide: [MIGRATION-GUIDE.md](00-setup/MIGRATION-GUIDE.md) / [中文迁移指南](00-setup/MIGRATION-GUIDE.zh-CN.md)
- These are paired PROPOSED artifacts; neither their presence nor this index adopts the standard. Semantic parity and governance adoption remain separate gates.
