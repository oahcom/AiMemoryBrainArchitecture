# AI-EXEC-002 — AI Prompt Execution Rules
# AI 开发提示词执行细则

- **Document ID:** AI-EXEC-002
- **Version:** 1.2
- **Status:** v1.2 PENDING ADOPTION（本变更集提交并合入 main 后按 AI-EXEC-UNIFICATION-RULING-001 §5 生效条款登记采纳）。Previous versions: v1.1 ADOPTED via PR #256 (merge commit `48a556491506d25e78be47957276bf3821797a0a`, 2026-11-18); v1.0 ADOPTED via PR #230 (merge commit `53aae842c390eac6d54f937af6cd2744dbe8d09d`, 2026-11-18). v1.2 变更内容：F-006 锚点修订（结构=七章节 per AI-STD-001 §5.1；15/12 项重分类为按 AI-PROMPT-STD-001 §4 映射的内容义务）。
- **Owner:** Integration Owner
- **Tracking:** Issue #218 · Work Item [AID-2026-002](./work-items/AID-2026-002/manifest.yaml) · 修订 Work Item [AID-2026-003](./work-items/AID-2026-003/manifest.yaml)
- **Upstream standards:** [AI-STD-001](ai-development-standard.md) §5/§13、[AI-PROMPT-STD-001](prompt-authoring-standard.md)、[CHATGPT-GLOBAL-001](prompts/global/chatgpt-session-contract-v1.md)、[AI-PROC-001](iteration-lifecycle.md) Stage 2/6、GLB-DOC-001（政策 GOV-DOC-001）
- **Translation status:** COMPLETE — source-aligned English counterpart: `docs/en/14-ai-development/AI-EXEC-002.md` (translation commit `08b07d228dbe78a209a5af68c4988b292e65e9c8`; source commit `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856`); bilingual closeout AID-2026-004 / Issue #218.

> **定位**：本文不是新规范，而是把项目现有提示词体系**真正跑起来**的执行细则。零脚本强制，约束靠提示词文本自我声明 + Issue/PR/Closeout 留痕。

**English summary.** Every execution prompt MUST use the seven structural sections defined by AI-STD-001 §5.1 (post-#269 canonical structure). The 12 items in AI-PROMPT-STD-001 §4 and AI-STD-001's former items 13–15 remain mandatory **content obligations** and MUST be mapped into those seven sections per the mapping rule in AI-PROMPT-STD-001 §4; they are not separate headings. Six/seven-item focus subsets never waive content obligations. VERIFIED is the canonical lifecycle status; TESTED is evidence wording only. SHA-256 is mandatory for exact prompt bytes; NOT_VERIFIED records an evidence limitation and never waives the gate. T1/T2/T3 provenance, grandfather distinctions, traceability, review, finding fields, bilingual exceptions and Closeout remain governed by this document.

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

1. **Work Item ID**：`AID-YYYY-NNN`（[INDEX.md](./work-items/INDEX.md) 注册规则），且 `work-items/AID-YYYY-NNN/manifest.yaml` 已创建；
2. **提示词标识**：Prompt ID + 版本（如 `AID-2026-002-PROMPT v1`）+ 出处锚点（按下述 **T1/T2/T3 三档**执行）；
3. **基线**：目标分支、base SHA、依赖 SHA（来源 Pin——分支名不是稳定基线，AI-PROMPT-STD-001 Step 2）；
4. **范围/非目标、任务类（ARCH/IMPL/TEST/SEC/MIG/PERF/DOC/OPS）、风险级（R0–R3）、验收标准**。

**提示词出处三档（v1.1 新增，缺口②对策）**——原三元组假设提示词必是仓库文件，盖不住 chat-instruction 会话；按实际形态分档：

| 档 | 适用 | 出处锚点（最低可追溯） |
|---|---|---|
| **T1 仓库文件** | 提示词存为仓库文件（`work-items/AID-*/prompt-vN.md` 等） | **Prompt ID + 版本 + 提示词文件 commit SHA 三元组**；SHA-256 有则记录（对实际提交字节计算，UTF-8 不做归一化，并按 AI-PROMPT-STD-001 §5 记路径/字节数/摘要/Blob SHA/commit SHA），无法计算/核验时记 **NOT_VERIFIED** |
| **T2 会话内指令** | chat-instruction：指令在对话中给出，无仓库文件 | **Prompt ID + 版本 + 指令全文快照**——开工时把实际执行的指令全文存入 Issue/PR 评论（或归档为 `prompt-vN.md`）；出处锚点 = **评论永久链接 + 创建时间戳**（归档则升级为 T1） |
| **T3 混合** | 仓库文件 + 会话内增补指令 | 以**实际执行的指令集**为准：文件三元组 + 增补快照（T2 方式）两段都记 |

- **禁止补造，禁止留空的 NOT RECORDED**（各档同）；
- 已执行提示词版本不可变；会话内澄清/增补若实质改变指令，必须先出新版本（T1 出新文件版本 / T2 出新快照）再继续（AI-PROMPT-STD-001 §5）；
- **Grandfather 条款**：v1.1 生效前已开工的会话按 v1.0 口径追溯，**不倒签、不补造、不追罚**。有直接证据证明未载入时，才记 `RULES-NOT-LOADED`；仅缺少 LOADED 声明/记录时，记 `RULES-LOAD-NOT-RECORDED`，仅表示证据缺口，不得反向推定实际未载入或认定历史违规。

> **已裁定（2026-11-18）**：提示词出处及哈希统一执行 `AI-EXEC-UNIFICATION-RULING-001` RULING-03。SHA-256 对准确提示词字节必录；`NOT_VERIFIED` 仅用于如实说明无法计算/核验的证据限制，不构成豁免。未满足提示词完整性要求时不得进入 `PROMPT_READY`。

## 3. 提示词强制结构（七个结构章节 + 十二/十五项内容义务映射，不另立结构）

> **结构权威**：结构章节以 AI-STD-001 §5.1 的七章节为准；内容义务以 AI-PROMPT-STD-001 §4 的映射规则为准——十二项内容必须按 §4 映射纳入七章节。下列 12 项 + 附加项为**内容义务清单**（不是独立标题）；映射后七章节为唯一结构层。
>
> **全风险级基线义务（F-02）**：全部风险级别（R0–R3）、全部任务类别的实质执行提示词，均须保留完整 **15 项内容义务**（12 项 + 原第 13–15 项），并全部映射入七章节。R0/R1 与 R2/R3 不得改变 15 项的基础强制适用范围；六项/七项重点子集仅表示审查重点。定时提示词附加要求继续叠加。

每份执行提示词必须包含其 12 项内容义务（按 AI-PROMPT-STD-001 §4 映射入七章节；连同原第 13–15 项构成完整 15 项内容义务，对全部风险级别生效）：

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

**分级重点检查（不是内容义务豁免）**：
- **所有执行提示词、所有风险级别与任务类**均必须保留上述 12 项完整内容义务（映射入七章节）；不得因 R0/R1、DOC 或代码会话而删除、合并或省略其余内容义务。
- **R0/R1 文档会话重点子集**：1、2、5、8、11、12 六项须特别具体；这六项只是审查重点，不是六项替代模板。
- **代码会话重点子集**：任务类 `IMPL/TEST/SEC/MIG/PERF` 的 1、2、3、5、8、9、12 七项须特别具体；其余五项仍必须保留在提示词中。R2/R3 无论任务类均须完整 12 项内容义务，并执行适用的额外风险/双语要求。
- **R2/R3**（任意任务类）：完整 15 项全量内容义务（映射入七章节），并执行适用的额外风险/双语要求；该要求与 R0/R1 内容义务一致，不构成 R2/R3 独有的义务豁免差异。
- 定时提示词另按 AI-PROMPT-STD-001 §4 附加项（Owner key、automation ID、频率、时区、幂等、单次上限、无任务行为、权限预检）。

> **已裁定（2026-11-18；2026-11-19 F-006 锚点修订）**：唯一完整强制**结构**为 AI-STD-001 §5.1 的七章节，见 `AI-EXEC-UNIFICATION-RULING-001` RULING-01（修订版）。AI-PROMPT-STD-001 §4 的 12 项与原第 13–15 项为强制**内容义务**，必须按 §4 映射纳入七章节；六项/七项重点子集不构成删减或豁免。precedence：结构层以 AI-STD-001 §5.1 为准，内容义务映射以 AI-PROMPT-STD-001 §4 为准。

提示词审批沿用其 Step 6（A 起草跨 Owner 任务、accountable Owner 批领域语义；A 自己的任务不得自编自批）。**提示词批准 ≠ 实现批准 ≠ 合并批准**。

## 4. 执行中留痕（AI-PROC-001 Stage 4 + PR-GOVERNANCE-001 §2）

- 重要决策、commit、变更路径、测试结果、阻塞、交接**随手**更新 Issue/PR，不许积压到结项；
- 状态词表唯一主口径为 **CHATGPT-GLOBAL-001 会话流程第 7 条**八态：`PROPOSED / IMPLEMENTED / VERIFIED / REVIEWED / ACCEPTED / MERGED / BLOCKED / NOT RUN`。`VERIFIED` 是唯一验证阶段状态；`TESTED` 仅描述已执行的测试证据，不是生命周期状态。历史 `TESTED` 按证据描述映射，不自动等同于 `VERIFIED`。详见 `AI-EXEC-UNIFICATION-RULING-001` RULING-02；
- 测试状态三值明示：`RUN/PASS`、`RUN/FAIL`、`NOT RUN（+原因）`。**NOT RUN 永远不得报为 PASS**（AI-STD-001 DoD 原文）；
- 测试证据必须指向**准确 commit**；对其他 commit 的测试在证明差异无关并记录之前不算证据（AI-PROC-001 Stage 5）。

## 5. 审查会话规则（NR-001 的落地口径）

1. **独立审查 = 新建一个 ChatGPT 对话**，从 GitHub 读取冻结输入（批准的提示词版本、任务记录与验收标准、base/implementation SHA、diff、测试证据、契约文档）；必须读 `prompts/global-architecture-reviewer.md`。
2. 审查者不得只复述作者报告，须主动找反例、缺失负例、竞态窗口、范围泄漏、陈旧状态行为、兼容性破坏（AI-PROC-001 Stage 6）。
3. **finding 用项目分级**：`BLOCKER / P0 / P1 / P2 / P3`；**处置**：`PASS / CONDITIONAL PASS / FAIL / NOT REVIEWABLE`。每条 finding 有 ID、证据、owner、严重级、状态、关闭条件；CONDITIONAL PASS 必须列限制项，不得当全量验收（AI-STD-001 §9）。**最低登记线（v1.1，与 [AI-EXEC-001](AI-EXEC-001.md) §4 对齐）**：ID + 严重级 + **回流去向**（关闭条件 + 回流落点：Issue #N / RW-YYYYMMDD / Closeout 项 k）三要素缺一即未登记；审查输出的每条 `F-n` 必须写明回流去向，反馈流才能取数。
4. **红线（PR-GOVERNANCE-001 §5 原文，2026-11-24 修订后）**：`COMMENT` 是技术评论不是 `APPROVE`；独立性是**审查会话**的属性，不是承载它的 GitHub 账号的属性——只要审查会话不是撰写会话，即使沿用同一已连接身份，仍构成独立；在撰写会话内做 AI 角色扮演不是独立审查，也不是 Owner 批准；例外必须显式记录，不得默默豁免。
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

随后更新 [INDEX.md](./work-items/INDEX.md) 的**会话级交付记录**一行（缺证据标 `NOT RECORDED`，禁止补造；受阻/无变更保持可见并注明解决者与退出条件）。

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
- LOADED: AI-EXEC-001 v__ + AI-EXEC-002 v__（§1.4 开工载入声明；仅缺少声明记 RULES-LOAD-NOT-RECORDED；有直接证据证明未载入才记 RULES-NOT-LOADED）
- Work Item: AID-YYYY-____  (manifest.yaml: 已建/未建)
- Owning Issue: #____   Related PR: #____
- Role: Owner __ (Accountable Owner: __)
- Prompt: <Prompt ID> v<版本> [T1|T2|T3]
  - T1: @ <提示词文件 commit SHA>  (SHA-256: ____ 或 NOT_VERIFIED)
  - T2: 指令快照 → <Issue/PR 评论永久链接> @ <时间戳>
  - T3: 两者都记
- Base: <branch> @ <base SHA>   Deps: <SHA 列表>
- Class/Risk: ARCH|IMPL|TEST|SEC|MIG|PERF|DOC|OPS / R0|R1|R2|R3
- Scope / Non-goals: ____
- Acceptance: 1) ____ 2) ____
- 双语: □ 同变更集同步  □ STALE 例外(原因/临时权威版/Owner/截止日/跟踪 Issue，GOV-DOC-001 §5)

### Closeout（会话结束发布到 Issue/PR，随后补 INDEX.md 一行）
1. Session/Prompt: <Prompt ID> v__ [T1|T2|T3] @ __ (hash: ____/NOT_VERIFIED；T2: 快照链接__)  Role: __
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
- F-1 [P0] <现象 + 证据(文件:行 / commit)> — owner __ — 关闭条件 __ — 回流 __ (Issue #N / RW-YYYYMMDD / Closeout k)
- F-2 [P2] ... — 回流 __
Checks: 范围一致 / 测试状态诚实(NOT RUN≠PASS) / 出处可查(Prompt+版本+commit SHA) / 双语对等(GOV-DOC-001)
Disclosure: 本审查为独立 ChatGPT 对话，提供上下文隔离，非模型/统计独立（NR-001）。
```
