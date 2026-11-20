# AI-EXEC-ROLLOUT-001 — AI Development Ecosystem Loop Rollout Plan
# AI 开发生态循环先行方案 —— 先闭环，后加强

- **Document ID:** AI-EXEC-ROLLOUT-001
- **Version:** 4.0（v2 去脚本化 → v3 GitHub 原生跟踪 → v4 对齐项目现行流程）
- **Status:** ADOPTED — owner-directed adoption recorded in Issue #218 comment #6971736655
- **Owner:** Integration Owner
- **Tracking:** Issue #218 · Work Item [AID-2026-002](./work-items/AID-2026-002/manifest.yaml)
- **落地文本**：[AI-EXEC-001](AI-EXEC-001.md)（流程执行细则）、[AI-EXEC-002](AI-EXEC-002.md)（提示词执行细则）
- **Translation status:** COMPLETE — source-aligned English counterpart: `docs/en/14-ai-development/AI-EXEC-ROLLOUT-001.md` (translation commit `e683ea275dfaf85fff0f9d18bb706d3bdb5d60a1`; source commit `778b4d3b4b6c846faa6a02247d31d14a33d8b626`); bilingual closeout AID-2026-004 / Issue #218.

> 本文重排 AI 开发流程痛点分析（前期研究，15 项措施）：**阶段一只做"让循环转起来"的最小闭环，阶段二再做加强**。v4 起**以项目现行流程为底座**——不另立平行制度，全部落在 AI-STD-001 / AI-PROC-001 / PR-GOVERNANCE-001 / AI-PROMPT-STD-001 既有机制上；Work Item（`AID-YYYY-NNN` + `manifest.yaml` + `INDEX.md`）按 AI-STD-001 §13 保留并跑起来。

**English summary.** Rollout plan that turns the existing governance stack into a running ecosystem loop first, then hardens it. Phase 1 = seven minimal actions (L0 PR flood relief → L1 bulk owner-directed adoption → L2 prompt provenance triple → L3 AID/manifest/INDEX registration → L4 exact-Head three-value evidence + Closeout → L5 NR-001 review with finding levels → L6 finding feedback + L7 **daily governance window** closing the loop). Loop-done DoD = two consecutive full Stage 0–8 iterations + three merged PRs traceable end-to-end + evidence honesty + healthy PR flow. Phase 2 (post-DoD): bilingual STALE-window mechanization, structured evidence set, delta review, prompt-library unification, KPI-driven rule reduction, multi-session review, platform enforcement (Issue #134), branch/currentness governance.

---

## 1. 目标定义：什么是"AI 开发生态循环"

在本项目语境下，生态循环 = **AI-PROC-001 的 Stage 0–8 + AI-STD-001 的 Work Item 状态机 + §11 反馈环，在日度节奏下完整转动**：

| 流 | 链路（项目原文机制） |
|---|---|
| **规则流** | 规范文档 ADOPTED（owner-directed adoption）→ 写入提示词（AI-PROMPT-STD-001 结构）→ 约束会话 |
| **执行流** | AID/manifest → 提示词冻结版本 → 分支实现 → exact-Head 验证 → NR-001 独立审查 → 五态处置合并 → Closeout + INDEX 行 |
| **反馈流** | finding（BLOCKER/P0–P3）/ 迭代回顾 → **日度治理窗口**（AI-STD-001 §11）→ 决策记录 + 提示词升版 → 规范/提示词翻状态 |

```
① 规则生效 → ② 提示词受控 → ③ 会话执行 → ④ AID/PR 登记 → ⑤ 证据留痕 → ⑥ NR-001 审查 → ⑦ Closeout/回顾 ─┐
      ↑                                                                                                  │
      └────────────── 反馈回流（finding → 日度治理窗口 → 决策/升版）←─────────────────────────────────────┘
```

**"循环达成"操作性定义**：连续 2 个完整迭代走通 Stage 0–8，且抽 3 个已合并 PR 能反查
`AID/manifest → Prompt ID+版本+commit SHA → Issue → PR Head → 测试证据 → finding → Closeout → INDEX 行` 全链路。

---

## 2. 现状断点诊断（对应项目机制的缺口）

| # | 环节 | 现状证据 | 断点性质 |
|---|------|---------|---------|
| ① | 规则生效 | AI-STD-001/AI-PROC-001/AI-PROMPT-STD-001 等全部 PROPOSED；PR-GOVERNANCE-001 是唯一 ADOPTED（Issue #130 模式） | **整环缺失**，但 adoption 模式已存在 |
| ② | 提示词受控 | Prompt hash 几乎全部 `NOT RECORDED`（INDEX 实录） | 有规则无执行口径 |
| ③ | 会话执行 | CHATGPT-GLOBAL-001 会话契约存在但产出与 AID/Closeout 时有脱节 | 链路靠人肉记忆 |
| ④ | 登记 | 142 PR 仅登记 2 个 Work Item；INDEX 会话表大量空缺 | 注册规则未跑 |
| ⑤ | 证据 | NOT RUN 可混同 PASS；exact-Head 门禁（PR-GOVERNANCE §4）执行不严 | **整环缺失** |
| ⑥ | 审查 | NR-001 规则在，但实际 0 独立审查人、"owner-directed exception"成放行惯例 | 规则与执行脱节 |
| ⑦ | 反馈 | 迭代回顾（AI-PROC-001 §4）与 §11 变更环未形成日节奏；finding 无回流入口 | 反馈流断 |
| ⑦→① | 规则迭代 | 无固定修订节奏 → 规范永远停在 PROPOSED | **循环无法闭合** |

---

## 3. 阶段一：最小闭环集（先达成）—— 7 个动作，零脚本、零新制度

### L0 循环前置：PR 泄洪（= PR-GOVERNANCE-001 "验证即合入" 的运行化）
- open PR ≤ 10、**先清后开**；每周一个集成窗口集中合并清淤；满足 MERGE 条件不搁置。
- 五态处置（MERGE/HOLD/REMEDIATE/SUPERSEDED/REJECT）逐单执行，清存量。
- Issue #134（分支保护未证实强制）按 PR-GOVERNANCE-001 §7 保持 OPEN 并升级管理员决断；不指望平台强制，靠处置纪律。

### L1 规则生效环 ⭐ 断点①
- **复制 PR-GOVERNANCE-001 的 owner-directed adoption 模式**（Issue comment 决议 + PR 合并记录），把 AI-STD-001、AI-PROC-001、AI-PROMPT-STD-001 及配套规范批量转 **ADOPTED**；不适用条款显式标注。
- 产出：一次治理决议 Issue/PR，文档头 `Status` 翻转——半天量级。

### L2 提示词受控环 ⭐ 断点②
- 执行口径：**Prompt ID + 版本 + 提示词文件 commit SHA 三元组**必录；SHA-256 有则录、无则按 AI-PROMPT-STD-001 §5 记 `NOT_VERIFIED`（其原文允许），**消灭空的 NOT RECORDED**。
- 提示词结构沿用 AI-PROMPT-STD-001 §4 十二项（R0/R1 六项最小集，R2/R3 全量+双语清单）。

### L3 登记环（AID/manifest/INDEX 跑起来）⭐ 断点④
- 实质工作开始前：建 `AID-YYYY-NNN` + `work-items/AID-YYYY-NNN/manifest.yaml`（INDEX.md 注册规则原文）。
- 会话结束补 **INDEX 会话级交付记录一行**；PR 准入先搜现有载体（PR-GOVERNANCE §3），杜绝 142 PR / 2 WI。

### L4 证据留痕环 ⭐ 断点⑤
- 测试三值明示（`RUN/PASS`｜`RUN/FAIL`｜`NOT RUN+原因`）；证据指向准确 Head/commit（PR-GOVERNANCE §4 exact-Head）。
- Closeout 八项∪九项∪双语结果（AI-EXEC-002 §6 模板）随 Issue/PR 发布。

### L5 审查环（NR-001 严格执行）⭐ 断点⑥
- R2/R3：**新建独立 ChatGPT 对话**审查，finding 分级 `BLOCKER/P0–P3`，处置 `PASS/CONDITIONAL PASS/FAIL/NOT REVIEWABLE`；COMMENT ≠ APPROVE、同 GitHub 身份不独立、角色扮演不冒充批准（PR-GOVERNANCE §5 原文）。
- 例外仅 R2/R3 时效豁免、显式记录 + 计数（每迭代 ≤ 2）；R0/R1 作者/审查者区分即可。

### L6 反馈回流环 ⭐ 断点⑦
- 缺陷 = finding 落 Issue/Closeout（不建 DEFECTS.md）；每迭代末 30 分钟回顾按 AI-PROC-001 §4 指标清单产出 ≤ 3 条改进项。
- 迭代末 Run 对账：AID ↔ PR ↔ 证据 ↔ 审查 ↔ Closeout ↔ INDEX 六方核对。

### L7 日度治理窗口（闭环关键）⭐ 断点⑦→①
- **每日固定 20 分钟**：按 AI-STD-001 §11 七步处置当日规则类 finding + 回顾改进项 → 决策记录 → 提示词升版 → 修订 PR 当日合并 → 文档头 Status 翻转。
- 反馈流**每日**回接规则流——循环按日闭合。

---

## 4. 闭环验收（Definition of Done）

1. **规则生效**：核心规范经 owner-directed adoption 转 ADOPTED，决议记录可查。
2. **跑通验证**：连续 2 个迭代走完 Stage 0–8，Work Item 状态无跳态（BLOCKED 记退出条件）。
3. **追溯测试**：抽 3 个已合并 PR，`AID/manifest → Prompt ID+版本+SHA → Issue → Head → 测试 → finding → Closeout → INDEX` 全链路无断链。
4. **证据诚实**：NOT RUN 零混同；新增记录 Prompt 出处零空缺 NOT RECORDED；同作者审查全部披露。
5. **流动健康**：open PR ≤ 10 且无超 7 天滞留；例外 ≤ 2/迭代。

---

## 5. 阶段二：后续加强（闭环达成后逐项投入）

| 加强项 | 内容 | 建议时机 |
|--------|------|---------|
| 双语门禁细化 | R0/R1 STALE 窗口机制化（GOV-DOC-001 §5 例外流程） | 循环达成后第 1 个月 |
| 结构化证据全套 | Phase-0 研究已设计的 Manifest/测试证据/SHA 绑定审查/Run 对账 | 同上 |
| delta review 成文 | 终结 Head 一变全量重验 | 同上 |
| 提示词库合一 | root `prompts/` 与 `14-ai-development/prompts/` 归一（AI-STD-001 §5 本就要求 root） | 第 2 个月 |
| KPI 驱动规则减法 | 用 AI-PROC-001 §4 指标触发"删规则" | 第 2 个月 |
| 审查升级 | NR-001 独立会话 → 多会话/外部审查源交叉 | 第 2–3 个月 |
| 平台强制落地 | Issue #134 决断：分支保护/Rulesets 真正生效后，把纪律升级为硬门禁 | 第 3 个月 |
| 时效性成本治理 | 175 分支收敛、23 份 currentness 审计合并 | 第 3 个月 |

---

## 6. 两周执行节奏

| 时间 | 动作 | 产出 |
|------|------|------|
| D1 | L0 泄洪 + L1 adoption 批量生效 | 规范文档 ADOPTED |
| D2–D3 | L2 提示词三元组口径 + L3 AID/manifest/INDEX 注册跑通 | 登记链路成文并启用 |
| D4–D5 | L4 exact-Head 证据 + Closeout 模板 + L5 NR-001 审查执行 | 证据+审查可留痕 |
| D6 | L6 finding 回流 + 回顾模板 + 六方对账表 | 反馈回流载体 |
| D7 起 | L7 日度治理窗口每日运转 | **循环闭合** |
| W2–W3 | 按 AI-PROC-001 §4 批次跑 2 个验证迭代 → 对照 §4 验收 | 判定循环达成 |
| 验收后 | 阶段二逐项加强 | 持续优化 |

---

## 7. 与原报告措施的映射

| 原报告措施 | 阶段一落点（项目机制） | 阶段二落点 |
|-----------|---------------------|-----------|
| 治理决议批量生效 | **L1** owner-directed adoption（复制 Issue #130 模式） | 修订窗口常态化 |
| PR 限额/限流 | **L0** 五态处置 + 集成窗口（PR-GOVERNANCE §6） | Issue #134 平台强制 |
| 提示词哈希自动化 | **L2** ID+版本+commit SHA 三元组 / NOT_VERIFIED 口径 | 提示词库合一 |
| Work Item 强制登记 | **L3** AID + manifest + INDEX（AI-STD-001 §13 原文机制） | — |
| 四类记录 + CI 校验 | **L4** exact-Head 三值证据 + Closeout 八项 | 结构化记录全套 |
| 独立审查分级 | **L5** NR-001 独立会话 + finding 体系 | 多会话/外部审查源 |
| 缺陷注册表 + 回顾 | **L6** finding 落 Issue + AI-PROC-001 §4 回顾 | 指标看板 |
| delta review | 暂缓 | 成文+自动化 |
| 双语门禁分级 | 仅按 AI-STD-001 §7.1 现行门禁 + GOV-DOC-001 §5 STALE 例外登记 | STALE 窗口机制化 |
| 元工作预算 + KPI | 暂缓（仅用 §4 验收） | KPI 体系 |
| Issue #134 决断 | L0 一并升级管理员 | 平台强制落地 |

---

## 8. 一句话总结

**不动项目既有制度，只让它转起来：ADOPTED 批量生效（复制 Issue #130 模式）、AID/manifest/INDEX 登记跑通、Prompt 三元组替代空哈希、exact-Head 三值证据、NR-001 独立会话审查、finding 回流日度治理窗口——零脚本、零平行制度，先转通 2 个迭代，验收后逐项加强。**
