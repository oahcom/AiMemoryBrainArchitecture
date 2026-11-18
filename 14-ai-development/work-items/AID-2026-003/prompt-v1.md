# AID-2026-003-PROMPT v1 — AI-EXEC-001/002 v1.1 修订会话

<!-- T1 档：仓库文件提示词（AI-EXEC-002 §2 v1.1 三档口径）；本文件为会话指令归档，版本不可变 -->

## Identity

- Work Item: AID-2026-003
- Owning Issue: #218
- Prompt ID/version: AID-2026-003-PROMPT v1
- Owner: Integration Owner
- 会话角色: 开发会话（治理文档修订）

## Objective

针对《规范执行观察报告》提炼的 6 条规范不完整缺口，起草并落地 AI-EXEC-001 / AI-EXEC-002 **v1.1 修订**，使登记流与反馈流可运转（七环 ④⑥⑦ 接通）。

## Baseline

- repo: oahcom/AiMemoryBrainArchitecture
- base: main @ 6b5db291（起草时 origin/main）
- 修改对象: 14-ai-development/AI-EXEC-001.md、14-ai-development/AI-EXEC-002.md

## Authority

- 修订走日度治理窗口（AI-EXEC-001 §7）：修订 PR 合并生效（owner 一票），文档头 Status 随采纳翻转。
- 不修改上位文档（AI-STD-001 / AI-PROC-001 / PR-GOVERNANCE-001 / AI-PROMPT-STD-001）任何条款。

## Scope

六缺口对应条款（观察报告 ①–⑥）：

1. ① ADOPTED 无"开工载入"义务 → AI-EXEC-001 §1.4 + §2 Stage 0
2. ② 三元组盖不住 chat-instruction → AI-EXEC-002 §2 T1/T2/T3 三档 + grandfather
3. ③ 后发治理文档无挂接 → AI-EXEC-001 §10 挂接裁定
4. ④ 代码会话无裁剪档 → AI-EXEC-002 §3 代码会话最小集（七项）
5. ⑤ finding 无最低登记线 → AI-EXEC-001 §4 + AI-EXEC-002 §5 三要素
6. ⑥ 独立审查获取无桥 → AI-EXEC-001 §6 获取桥（来源顺序 + 24h/3 工作日时限）

## Non-goals

- 不解决三处上位冲突（15v12、TESTEDvVERIFIED、SHA-256 逃生门）——仍留 Issue #218 决议；
- 不动 AI-EXEC-ROLLOUT-001（其映射在阶段二，另行处置）；
- 不引入任何脚本/CI 强制。

## Required steps

inspect（重读两份规范现文 + 观察报告缺口）→ plan（六缺口补丁点定位）→ change（v1.1 条款 + 模板）→ verify（内部一致性 / 术语对齐 / 无上位条款改动）→ report（PR + Issue 评论）。

## Acceptance criteria

1. 六缺口各有对应条款落点，且与上位文档不冲突；
2. 两份规范交叉引用一致（finding 三要素、版本口径）；
3. Work Item AID-2026-003 注册齐全（manifest + 本提示词 + INDEX 两行）；
4. 修订 PR 准入五要素齐（PR-GOVERNANCE-001 §3）。

## Verification

- 全文重读 diff，确认只增不改上位引用语义；
- grep 一致性检查（T1/T2/T3、LOADED、回流去向 等新术语在两文件口径一致）；
- 提示词字节哈希按 AI-PROMPT-STD-001 §5 记录（见 manifest）。

## Git workflow

- 分支: ai/AID-2026-003/IO-exec-v11
- PR 目标: main；不在 PR 内自行合并；合并后回读 merge SHA 记 Closeout。

## Stop/escalation

- 发现与上位文档实质冲突 → 停止写入，记 finding 回流 Issue #218；
- 观察缺口与条款对不上 → 升级 Integration Owner 裁定。

## Evidence and final report

Closeout 按 AI-EXEC-002 §6 九项模板；finding 按 §5 三要素（ID + 严重级 + 回流去向）。
