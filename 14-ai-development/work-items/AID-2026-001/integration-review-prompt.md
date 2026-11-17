# AID-2026-001 Independent Specialist Review Handoff
# AID-2026-001 独立专业审查交接

**Repository:** oahcom/AiMemoryBrainArchitecture
**Historical PR:** #42 — merged; provenance only — https://github.com/oahcom/AiMemoryBrainArchitecture/pull/42
**Review mode:** Read-only independent specialist review in a genuinely new ChatGPT conversation.
**Governance:** NR-001 OPTION A ACCEPTED. This is conversation/context isolation only—not model, provider, runtime/environment or statistical independence. Do not describe it as multi-model consensus.
**Risk:** ARCH / R3.

## Mandatory session and evidence controls

1. This must be a genuinely new ChatGPT conversation. You must not have participated in authoring, editing, implementing or coordinating the remediation.
2. Before reviewing, read the current PR metadata from GitHub and verify that the PR Head exactly equals the expected SHA supplied by the handoff operator. If it differs, STOP; do not silently review a moving target.
3. Independently read the exact Base/Head, full PR diff, AI-STD-001, NR-001 decision, AI-ARCH-002 in both languages, Work Item Manifest, prompt-v2, execution record, test matrix, and relevant Owner contracts.
4. Do not rely on the implementer's explanation or self-review. Treat repository artifacts as evidence; validate claims directly.
5. Do not modify any branch, file, PR description, issue, or manifest. Do not approve, merge, or accept.
6. Record exact Head SHA, paths and SHAs inspected, evidence, commands/checks actually executed, checks not run, findings, residual risks and scope limitations.
7. All R3 controls are mandatory. A specialist report is not the overall architecture acceptance or merge authorization.
8. If evidence is absent, state NOT EVIDENCED. If a test was not executed, state NOT RUN. Do not infer a pass from a test specification.

## Required output

Submit a bilingual report as a PR comment, with:
- exact Base and Head SHA;
- scope and artifacts inspected;
- specialist opinion limited to your assigned domain;
- findings with ID, severity, evidence, impact, required correction and closure condition;
- explicit R3 gate disposition: PASS / FAIL / NOT EVIDENCED;
- checks not run;
- statement that you did not modify implementation or approve/merge.

The reviewer must disclose context-only independence under NR-001.

## Assigned role — Integration Reviewer (not Owner A)

You are the distinct Integration Reviewer for AID-2026-001. You are not Owner A, did not implement or coordinate this Work Item, and must not adopt A's implementation context.

Review only integration architecture and cross-owner compatibility:
- A–I authority and decision boundaries;
- whether A coordinates without replacing B–I domain decisions;
- B domain identity versus I security identity;
- D canonical Forget/lifecycle versus I authorization/privacy/retention/audit;
- explicit bilateral D/I contract agreement;
- consistency of global session contract, Owner prompts, architecture documents, Work Item manifest and execution record;
- deterministic-only CI boundary and prohibition on AI execution via runners/API/Codex/DC/local relays;
- separation between implementing AI, independent reviewer, integration reviewer and acceptance authority;
- bilingual semantic parity for integration-critical clauses.

Read exact current source contracts and the entire PR diff. Do not treat the independent reviewer report or Owner I/D specialist reports as substitutes for your own integration compatibility analysis. Verify their exact Head bindings if present.

You must not fill in for missing specialist evidence or acceptance authority. If Owner I/D reports or reproducible R3 tests are absent, record those gates as NOT EVIDENCED and block integration readiness.

## 中文职责

你是独立的 Integration Reviewer，不是 Owner A，且未参与本 Work Item 的实现或协调。审查 A–I 跨模块权限、B/I 身份边界、D/I Forget 联合契约、提示词/架构/Manifest 一致性、CI 与 AI 执行边界、实现者/独立 Reviewer/Integration Reviewer/验收授权方职责分离，以及双语语义一致性。不得代替 Owner I/D 专业审查或验收授权；缺少 R3 证据时必须阻止 Integration Ready。


## Current review-target clarification / 当前审查目标澄清

PR #42 is historical and MERGED; it is not the current review target. The review operator must provide an immutable target tuple before this prompt is used:
- `target_kind`: `main` or `pull_request`;
- `expected_base_sha`: exact base SHA;
- `expected_head_sha`: exact candidate SHA (for main review, this is the exact main SHA);
- `review_scope`: exact integration paths/contracts to inspect.

For `target_kind=main`, fetch current `main` and verify it equals `expected_head_sha`. For `target_kind=pull_request`, fetch PR metadata and verify exact base and head SHAs. If either differs, STOP and request a refreshed handoff. Do not silently follow a moving ref. The historical PR #42 reference is provenance only.

## 当前审查目标澄清

PR #42 已是历史记录并且已经合并，不再是当前审查目标。使用本提示词前，交接方必须提供不可变目标元组：
- `target_kind`：`main` 或 `pull_request`；
- `expected_base_sha`：准确 Base SHA；
- `expected_head_sha`：准确候选 SHA（审查 main 时即准确 main SHA）；
- `review_scope`：必须检查的准确集成路径/契约。

当 `target_kind=main` 时，读取当前 `main` 并确认等于 `expected_head_sha`。当 `target_kind=pull_request` 时，读取 PR 元数据并确认 Base/Head SHA 完全一致。任一不一致都必须停止并要求刷新交接，不得静默跟随移动引用。上方 PR #42 仅作为历史来源说明。
