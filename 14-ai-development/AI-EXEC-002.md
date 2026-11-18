# AI-EXEC-002 — AI Prompt Execution Rules
# AI 开发提示词执行细则

- **Document ID:** AI-EXEC-002
- **Version:** 1.0
- **Status:** PROPOSED — owner-directed adoption pending (Issue #218; adoption pattern per PR-GOVERNANCE-001)
- **Owner:** Integration Owner
- **Tracking:** Issue #218 · Work Item [AID-2026-002](work-items/AID-2026-002/manifest.yaml)
- **Upstream standards:** [AI-STD-001](ai-development-standard.md) §5/§13、[AI-PROMPT-STD-001](prompt-authoring-standard.md)、[CHATGPT-GLOBAL-001](prompts/global/chatgpt-session-contract-v1.md)、[AI-PROC-001](iteration-lifecycle.md) Stage 2/6、GLB-DOC-001（政策 GOV-DOC-001）
- **Translation status:** 中文版为本批权威版本；English counterpart = **STALE**（GOV-DOC-001 §5 time-bounded exception，登记见 `docs/translation-status.md`，截止 2026-12-02，Owner: Integration Owner，跟踪 Issue #218）

> **定位**：本文不是新规范，而是把项目现有提示词体系**真正跑起来**的执行细则。零脚本强制，约束靠提示词文本自我声明 + Issue/PR/Closeout 留痕。

**English summary.** Execution rules for the existing prompt system. (1) Pre-work record: Work Item ID + manifest, **Prompt ID + version + prompt-file commit SHA triple** (kills empty `NOT RECORDED`; SHA-256 recorded when computable, else `NOT_VERIFIED` per AI-PROMPT-STD-001 §5); (2) mandatory structure = AI-PROMPT-STD-001 §4 twelve items, with a six-item minimum set for R0/R1 and the AI-STD-001 §5 item-15 bilingual manifest added for R2/R3 — the 15-vs-12 inter-standard conflict is disclosed and deferred to adoption Issue #218; (3) in-run traceability with the CHATGPT-GLOBAL-001 eight-state vocabulary (never collapsed); (4) NR-001 review-session rules with project finding levels BLOCKER/P0–P3; (5) Closeout template = AI-STD-001 §13 eight items ∪ PR-GOVERNANCE-001 §2 nine items ∪ §7.1 bilingual result; (6) prohibitions per AI-PROMPT-STD-001 §7 + CHATGPT-GLOBAL-001. Copy-paste templates for session open/closeout and review output are provided in appendices.

---

## 1. 适用范围与提示词库（沿用 AI-STD-001 §5）

- **执行通道**：普通 ChatGPT 对话 + 项目已验证的 GitHub 连接应用。CHATGPT-GLOBAL-001 的十条不可妥协约束原文有效（禁 API Key / Codex / 第三方模型 / 本地中转；GitHub 工件是持久事实来源，聊天记录不是交付物）。
- **提示词库**（canonical 位置为仓库根 `prompts/`，AI-STD-001 §5）：
  - 每会话必读：`prompts/global-project-developer.md` + `prompts/global-bilingual-documentation.md` + 所属 Owner 提示词（`prompts/A/`–`prompts/I/`）
  - 审查会话加读：`prompts/global-architecture-reviewer.md`
  - 现行 `14-ai-development/prompts/`（CHATGPT-GLOBAL-001、`owners/A/owner-session-v1.md` 等）**继续使用**；每次会话必须在证据中写明实际用的是哪一库哪一版本。两库合一属后续加强项。
- **三类会话**：开发会话（Owner A–I）、审查会话（独立 ChatGPT 对话，NR-001）、治理会话（日度治理窗口，见 [AI-EXEC-001](AI-EXEC-001.md) §7）。

## 2. 开工前必录字段（消灭 "Prompt hash: NOT RECORDED"）

工作开始前，在 Work Item 所属 Issue/PR 写明（= AI-STD-001 §13 起始记录 + AI-PROC-001 §8 接收清单）：

1. **Work Item ID**：`AID-YYYY-NNN`（[INDEX.md](work-items/INDEX.md) 注册规则），且 `work-items/AID-YYYY-NNN/manifest.yaml` 已创建；
2. **提示词标识**：Prompt ID + 版本（如 `AID-2026-002-PROMPT v1`）+ **提示词文件的 commit SHA**；
3. **基线**：目标分支、base SHA、依赖 SHA（来源 Pin——分支名不是稳定基线，AI-PROMPT-STD-001 Step 2）；
4. **范围/非目标、任务类（ARCH/IMPL/TEST/SEC/MIG/PERF/DOC/OPS）、风险级（R0–R3）、验收标准**。

**哈希执行口径**（AI-PROMPT-STD-001 §5 本身允许 `NOT_VERIFIED`）：
- **最低可追溯要求 = Prompt ID + 版本 + 提示词文件 commit SHA 三元组**——三者齐全即出处可查；
- SHA-256 有则记录（对仓库内实际提交字节计算，UTF-8 不做归一化），并按其 §5 记路径/字节数/摘要/Blob SHA/commit SHA；无法计算/核验时按其 §5 记 **NOT_VERIFIED**。**禁止补造，禁止继续留空的 NOT RECORDED**；
- 已执行提示词版本不可变；会话内澄清/增补若实质改变指令，必须先出新版本再继续（AI-PROMPT-STD-001 §5）。

> **上位冲突披露（待 Issue #218 adoption 决议）**：AI-STD-001 §5 要求 "Prompt ID、版本和 SHA-256" 必录且未设逃生门，与 AI-PROMPT-STD-001 §5 的 `NOT_VERIFIED` 口径存在字面冲突。本细则暂按 AI-PROMPT-STD-001 §5 执行（三元组 + NOT_VERIFIED），统一口径随批量 adoption 一并裁定。

## 3. 提示词强制结构（按 AI-PROMPT-STD-001 §4，不另立结构）

每份执行提示词必须包含其 12 项结构：

1. Identity（Work Item ID、Issue、prompt ID/version/hash、Owner、会话角色）
2. Objective（目标与可观察结果）
3. Baseline（repo、分支、base SHA、源路径/blob SHA、依赖）
4. Authority（自有决策、允许/禁止动作、审批人）
5. Scope（范围内文件/模块与显式非目标）
6. State of knowledge（DECIDED / CANDIDATE / OPEN / TO_VALIDATE 分列）
7. Required steps（inspect → plan → change → verify → report）
8. Acceptance criteria（编号、客观、可独立核对）
9. Verification（命令、fixture、环境、预期/实际）
10. Git workflow（分支、commit、PR 目标、审查交接、不合并规则）
11. Stop/escalation（停止条件与升级对象）
12. Evidence and final report schema（证据与最终报告格式）

**分级裁剪（运行口径）**：
- **R0/R1** 最小集：1、2、5、8、11、12 六项必录，其余从简；
- **R2/R3**：12 项全量 + AI-STD-001 §5 第 15 项**双语文档清单**（中英路径、源版本、对应件状态、标识/状态对等、交叉链接、语义对等审查人）；
- 定时提示词另按 AI-PROMPT-STD-001 §4 附加项（Owner key、automation ID、频率、时区、幂等、单次上限、无任务行为、权限预检）。

> **上位冲突披露（待 Issue #218 adoption 决议）**：AI-STD-001 §5 另有一份 **15 项**强制清单（含第 15 项双语文档清单），与 AI-PROMPT-STD-001 §4 的 12 项切分口径不同。本细则以 12 项为主清单，将 AI-STD-001 §5 差异项（任务类/风险级、独立审查者角色、双语清单）并入 §2 开工必录与上述分级裁剪执行；两清单的统一列入批量 adoption 一并裁定。

提示词审批沿用其 Step 6（A 起草跨 Owner 任务、accountable Owner 批领域语义；A 自己的任务不得自编自批）。**提示词批准 ≠ 实现批准 ≠ 合并批准**。

## 4. 执行中留痕（AI-PROC-001 Stage 4 + PR-GOVERNANCE-001 §2）

- 重要决策、commit、变更路径、测试结果、阻塞、交接**随手**更新 Issue/PR，不许积压到结项；
- 状态词表只用项目词表（**CHATGPT-GLOBAL-001 会话流程第 7 条**原文八态）：`PROPOSED / IMPLEMENTED / VERIFIED / REVIEWED / ACCEPTED / MERGED / BLOCKED / NOT RUN`，**不得混同**——"Implemented" 不是 "Verified"，"Reviewed" 不是 "Accepted"；（注：AI-STD-001 §10 词表用 `TESTED` 而非 `VERIFIED` 且不含 NOT RUN，两处差异列入 Issue #218 决议统一）；
- 测试状态三值明示：`RUN/PASS`、`RUN/FAIL`、`NOT RUN（+原因）`。**NOT RUN 永远不得报为 PASS**（AI-STD-001 DoD 原文）；
- 测试证据必须指向**准确 commit**；对其他 commit 的测试在证明差异无关并记录之前不算证据（AI-PROC-001 Stage 5）。

## 5. 审查会话规则（NR-001 的落地口径）

1. **独立审查 = 新建一个 ChatGPT 对话**，从 GitHub 读取冻结输入（批准的提示词版本、任务记录与验收标准、base/implementation SHA、diff、测试证据、契约文档）；必须读 `prompts/global-architecture-reviewer.md`。
2. 审查者不得只复述作者报告，须主动找反例、缺失负例、竞态窗口、范围泄漏、陈旧状态行为、兼容性破坏（AI-PROC-001 Stage 6）。
3. **finding 用项目分级**：`BLOCKER / P0 / P1 / P2 / P3`；**处置**：`PASS / CONDITIONAL PASS / FAIL / NOT REVIEWABLE`。每条 finding 有 ID、证据、owner、严重级、状态、关闭条件；CONDITIONAL PASS 必须列限制项，不得当全量验收（AI-STD-001 §9）。
4. **红线（PR-GOVERNANCE-001 §5 原文）**：`COMMENT` 是技术评论不是 `APPROVE`；同一 GitHub 身份的审查不独立（哪怕换角色）；AI 角色扮演不是 Owner 批准；例外必须显式记录，不得默默豁免。
5. **披露义务（NR-001）**：审查记录必须写明"独立 ChatGPT 对话只提供上下文/对话隔离，不是模型/统计独立，不得称多模型共识"；R3 仍须独立安全/领域专家审查 + 可复现测试证据。

## 6. 结项（Closeout）——会话的证据出口

会话结束（完成或受阻）必须在 Issue/PR 发布 Closeout 评论（= AI-STD-001 §13 八项 ∪ PR-GOVERNANCE-001 §2 九项 ∪ AI-STD-001 §7.1 双语门禁结果）：

1. 会话/提示词标识：Prompt ID、版本、SHA-256 或 NOT_VERIFIED、提示词文件 commit SHA、角色、accountable Owner；
2. Work Item ID + 归属 Issue + 相关 PR 链接（优先复用载体，PR-GOVERNANCE-001 §3）；
3. 仓库、分支、base SHA、最终 Head SHA、变更路径；
4. 实际工作与决策，逐项标 `PROPOSED / ACCEPTED / REJECTED / UNRESOLVED / OPEN / BLOCKED` + 决策权威；
5. 验证命令、环境、准确测试 SHA、结果与链接；**逐项列出未运行的必需检查及原因**；
6. 独立审查与集成状态；同作者/委派角色模拟必须披露，不得冒充独立批准；
7. 依赖、阻塞、风险、后续 Owner、客观关闭条件；受阻/无变更也必须发 `BLOCKED` / `NO_CHANGE` Closeout；
8. 合并状态：仅在确实合并后记目标分支、merge commit SHA、合并后回读验证——**不得由 PR 关闭推断已合并**；
9. 双语门禁结果（GOV-DOC-001：双方路径、源版本、对等维度 PASS/FAIL、审查人，或 STALE 例外登记要素）。

随后更新 [INDEX.md](work-items/INDEX.md) 的**会话级交付记录**一行（缺证据标 `NOT RECORDED`，禁止补造；受阻/无变更保持可见并注明解决者与退出条件）。

## 7. 禁止事项（AI-PROMPT-STD-001 §7 + CHATGPT-GLOBAL-001）

- 自编自批、自审充当独立审查、角色扮演面板冒充独立批准；
- 用浮动分支名/"latest" 代替 SHA；一个提示词混多个 Work Item；
- 声称未运行的测试/缺失的批准/未验证的部署行为已完成；
- 执行中未经审查擅改提示词指令；补造 NOT RECORDED 证据；
- 使用 API Key、Codex、第三方/本地模型、Desktop Commander、本地中转；
- 让定时任务默认合并/发布/破坏性操作，或反复重开已完成/已拒绝工作。

## 8. 修订

提示词的新增/修改走**日度治理窗口**（[AI-EXEC-001](AI-EXEC-001.md) §7，即 AI-STD-001 §11 反馈环的日度化）：出新版本（Prompt ID + 版本号 + 新 commit SHA），旧版本不可变、可检索。

---

## 附录 A：开发会话开工 / 结项粘贴模板

```markdown
### 开工记录（写入 Issue/PR）
- Work Item: AID-YYYY-____  (manifest.yaml: 已建/未建)
- Owning Issue: #____   Related PR: #____
- Role: Owner __ (Accountable Owner: __)
- Prompt: <Prompt ID> v<版本> @ <提示词文件 commit SHA>  (SHA-256: ____ 或 NOT_VERIFIED)
- Base: <branch> @ <base SHA>   Deps: <SHA 列表>
- Class/Risk: ARCH|IMPL|TEST|SEC|MIG|PERF|DOC|OPS / R0|R1|R2|R3
- Scope / Non-goals: ____
- Acceptance: 1) ____ 2) ____
- 双语: □ 同变更集同步  □ STALE 例外(原因/临时权威版/Owner/截止日/跟踪 Issue，GOV-DOC-001 §5)

### Closeout（会话结束发布到 Issue/PR，随后补 INDEX.md 一行）
1. Session/Prompt: <Prompt ID> v__ @ __ (hash: ____/NOT_VERIFIED)  Role: __
2. Work Item AID-____ / Issue #____ / PR #____
3. Branch __ / base __ / Head __ / changed: ____
4. Work & decisions: ____(PROPOSED/ACCEPTED/REJECTED/UNRESOLVED/OPEN/BLOCKED + 权威)
5. Verification: <命令> @ <测试 SHA> → RUN/PASS | RUN/FAIL | NOT RUN(__)；未运行清单: ____
6. Review: <独立会话审查 / 同作者披露>  Verdict: PASS | CONDITIONAL PASS | FAIL | NOT REVIEWABLE
   (NR-001 披露: 对话隔离 ≠ 模型独立)
7. Risks/blockers/next owner/exit condition: ____
8. Merge: 未合并 | merged to __ @ __ (回读: __)
9. 双语(GOV-DOC-001): 路径__ / 对等 PASS|FAIL|STALE例外(截止__/跟踪__) / 审查人__
```

## 附录 B：审查会话输出模板（finding 体系）

```markdown
### [REVIEW] PR #____ / AID-____  （独立 ChatGPT 会话，输入已冻结）
Verdict: PASS | CONDITIONAL PASS | FAIL | NOT REVIEWABLE
Findings:
- F-1 [P0] <现象 + 证据(文件:行 / commit)> — owner __ — 关闭条件 __
- F-2 [P2] ...
Checks: 范围一致 / 测试状态诚实(NOT RUN≠PASS) / 出处可查(Prompt+版本+commit SHA) / 双语对等(GOV-DOC-001)
Disclosure: 本审查为独立 ChatGPT 对话，提供上下文隔离，非模型/统计独立（NR-001）。
```
