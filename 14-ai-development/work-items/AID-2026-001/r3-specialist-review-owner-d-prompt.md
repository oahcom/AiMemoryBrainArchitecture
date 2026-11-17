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

## Assigned role — Owner D Forget / Memory Lifecycle Specialist

You are the independent Owner D domain specialist for this review only.

Review canonical Memory Brain and Forget/lifecycle contracts:
- canonical meaning and completeness of Forget;
- lifecycle/deletion stages and terminal completion semantics;
- partial failure, retry, idempotency and recovery;
- what evidence is required before reporting deletion completion;
- boundaries with I-owned authorization, privacy, retention, legal hold and audit governance;
- bilateral D/I agreement requirements for joined contracts.

Read Owner D v2 and Owner I v2, AI-STD-001 §3.1–§4, the exact architecture documents and R3 test matrix. Confirm D retains canonical lifecycle authority while I controls security authorization/governance. Identify any contract ambiguity that could cause false completion, incomplete deletion, unsafe retries or unauthorized mutation.

Do not perform an implementation review outside this Forget/lifecycle scope. Do not claim deletion behavior is proven by architecture prose alone. If no executable reproducible test evidence exists, the R3 evidence gate is NOT EVIDENCED.

## 中文职责

你仅作为本 Work Item 的独立 Owner D Forget/记忆生命周期专业审查者。重点审查 Forget 的规范含义和完整性、删除阶段及完成语义、部分失败/重试/幂等/恢复、完成证明，以及与 I 所有的授权、隐私、保留、法律保留和审计治理边界。确认联合契约需要 D/I 双边同意。没有可执行、可复现测试证据时，必须标记 NOT EVIDENCED。


## Current review-target clarification / 当前审查目标澄清

PR #42 is historical and MERGED; it is not the current review target. The review operator must provide an immutable target tuple before this prompt is used:
- `target_kind`: `main` or `pull_request`;
- `expected_base_sha`: exact base SHA;
- `expected_head_sha`: exact candidate SHA (for main review, this is the exact main SHA);
- `review_scope`: the exact paths/contracts required for this specialist role.

For `target_kind=main`, fetch the current `main` ref and verify it equals `expected_head_sha`. For `target_kind=pull_request`, fetch PR metadata and verify both base and head SHAs exactly. If either differs, STOP and request a refreshed handoff; never silently follow a moving ref. The historical PR #42 reference above is retained only to explain provenance.

## 当前审查目标澄清

PR #42 已是历史记录并且已经合并，不再是当前审查目标。使用本提示词前，交接方必须提供不可变目标元组：
- `target_kind`：`main` 或 `pull_request`；
- `expected_base_sha`：准确 Base SHA；
- `expected_head_sha`：准确候选 SHA（审查 main 时即准确 main SHA）；
- `review_scope`：本专业角色必须审查的准确路径/契约。

当 `target_kind=main` 时，读取当前 `main` 引用并确认等于 `expected_head_sha`。当 `target_kind=pull_request` 时，读取 PR 元数据并确认 Base/Head SHA 均完全一致。任一不一致都必须停止并要求刷新交接，不得静默跟随移动引用。上方 PR #42 仅保留为历史来源说明。
