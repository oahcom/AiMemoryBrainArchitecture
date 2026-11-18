# AI-EXEC-001 — AI Development Process Execution Rules
# AI 开发流程执行细则

- **Document ID:** AI-EXEC-001
- **Version:** 1.0
- **Status:** ADOPTED — owner-directed adoption recorded in Issue #218 comment #6971736655
- **Owner:** Integration Owner
- **Tracking:** Issue #218 · Work Item [AID-2026-002](work-items/AID-2026-002/manifest.yaml)
- **Upstream standards:** [AI-STD-001](ai-development-standard.md)、[AI-PROC-001](iteration-lifecycle.md)、[PR-GOVERNANCE-001](PR-GOVERNANCE-001.md)（ADOPTED）、[AI-PROMPT-STD-001](prompt-authoring-standard.md)、GOV-DOC-001
- **Translation status:** 中文版为本批权威版本；English counterpart = **STALE**（GOV-DOC-001 §5 time-bounded exception，登记见 `docs/translation-status.md`，截止 2026-12-02，Owner: Integration Owner，跟踪 Issue #218）

> **定位**：本文不是新制度，而是让项目现有流程（AI-STD-001 / AI-PROC-001 / PR-GOVERNANCE-001）**真正运转起来**的执行细则。零脚本强制——PR-GOVERNANCE-001 §7 明确"模板/标签/评论/AI 自审不得冒充硬门禁"，本细则与之一致，只加运行纪律。
> **本文不修改**任何上位文档条款；凡冲突处以上位文档为准，只补充"怎么跑、留什么痕、多久闭环"。

**English summary.** Execution rules that operationalize the existing governance stack — no parallel institution, no script enforcement. Adds: (1) a Stage 0–8 run table binding each lifecycle stage to its Work Item state and evidence; (2) tracking carriers per AI-STD-001 §13 (Issue / PR / AID+manifest / INDEX / Closeout); (3) PR discipline = PR-GOVERNANCE-001 five dispositions + exact-Head gate + flow quotas (open PR ≤ 10, weekly integration window — running discipline, violations logged as findings, never hard-blocked); (4) review & exception rules (NR-001 independent session for R2/R3, explicit exception recording, ≤ 2/iteration); (5) a **daily governance window** (≤ 20 min, AI-STD-001 §11 loop materialized) as the only feedback→rules re-entry point; (6) a five-point Definition of Done for closing the ecosystem loop. Conflicts between upstream standards (prompt-structure 15-vs-12 items, TESTED-vs-VERIFIED vocabulary, SHA-256 mandatory-vs-NOT_VERIFIED) are recorded and deferred to the adoption decision in Issue #218.

---

## 1. 总则：让规则生效的三条运行原则

1. **规则先生效再约束**：上位文档当前多为 PROPOSED。按 PR-GOVERNANCE-001 已示范的 **owner-directed adoption** 模式（Issue #130 comment #6962523529 + PR #144 合并记录）批量转 **ADOPTED**；未生效条款不作为门禁依据（AI-STD-001 §12"初始治理状态"本来就允许）。
2. **证据随产出**：NOT RUN ≠ PASS（AI-STD-001 DoD 原文）；证据指向准确 Head/commit（PR-GOVERNANCE-001 §4 exact-Head 门禁）。
3. **缺陷必回流**：finding 进 Issue/Closeout；**规则类问题**（提示词/流程/契约缺陷）进**日度治理窗口**处置（AI-STD-001 §11 反馈环的日度化）。

## 2. 迭代生命周期 = AI-PROC-001 Stage 0–8（运行表）

不新设阶段，只规定每个阶段"跑起来要留下什么"：

| Stage（AI-PROC-001） | Work Item 状态（AI-STD-001 §4.1） | Gate | 本细则要求 |
|---|---|---|---|
| 0 Intake & registration | PROPOSED | G0 | 复用或创建 Issue；建 `AID-YYYY-NNN` + `manifest.yaml`；记 Sponsor/Owner |
| 1 Impact & dependency | ANALYZED | G1 | 影响图、依赖/契约状态（DECIDED/CANDIDATE/OPEN/TO_VALIDATE）、验收标准写入 Issue |
| 2 Prompt drafting | PROMPT_READY | G1 | 提示词入库并冻结版本（AI-EXEC-002 §2–§3）；A 起草、Owner 批 |
| 3 Readiness gate | READY | G1 | DoR 全满足（AI-STD-001 §7）；上游契约 OPEN 时按其三选项：先解契约 / 只做隔离切片 / BLOCKED |
| 4 AI implementation | IN_PROGRESS → IMPLEMENTED | G2 | 分支 `ai/<work-item-id>/<owner>-<short-topic>`（AI-STD-001 §6）；最小连贯变更；随手更新 Issue/PR |
| 5 Automated verification | VERIFIED | G3 | exact-Head 检查证据；`NOT RUN` 明示原因；R2/R3 加并发/故障/安全测试 |
| 6 Independent AI review | REVIEWED | G4 | NR-001 独立 ChatGPT 会话 + finding 体系（AI-EXEC-002 §5） |
| 7 Cross-owner integration | INTEGRATION_READY | G5 | 各 Owner 只批自己契约边界；A 调和冲突并更新 Contract Registry；五级区分（本地批准/双边契约/多模块/实现证据/系统符合性） |
| 8 Acceptance & merge | ACCEPTED → MERGED → CLOSED | G6（G7 发布就绪另计） | PR 五态处置（§5）；Closeout 8 项 + INDEX 行；合并后回读 merge SHA |

- 状态推进**不得跳态**（AI-STD-001 §4.1 原文）：Implemented ≠ Verified ≠ Reviewed ≠ Accepted ≠ Merged。
- `BLOCKED`：依赖/决议/权限不可用，记阻塞 owner 与退出条件；`REJECTED`：方案无效，保留提示词与审查记录，不抹除失败痕迹（§4.2）。

## 3. 任务类与风险级（直接沿用 AI-STD-001 §4，不重定义）

- 任务类：`ARCH / IMPL / TEST / SEC / MIG / PERF / DOC / OPS`，每个 Work Item 必须声明。
- 风险级：`R0` 编辑性改动 / `R1` 影响有界的实现或文档 / `R2` 跨模块契约、持久化、协议、并发、兼容 / `R3` 安全边界、授权、Forget/删除、数据完整性、恢复、迁移、发布关键。
- R2/R3 必须显式影响分析 + 指名审查人；R3 必须独立安全/领域专家审查 + 可复现测试证据后才能验收。
- 双语门禁（AI-STD-001 §7.1 / GOV-DOC-001）：影响架构含义的任务，中英文档同变更集更新；审查者对含义/标识/状态/示例/链接记 PASS/FAIL；缺失或实质不一致 = BLOCKED/NOT DONE，或按 GOV-DOC-001 §5 登记有期限 STALE 例外（原因/临时权威版/Owner/截止日/跟踪 Issue）。

## 4. 跟踪机制（AI-STD-001 §13 + PR-GOVERNANCE-001 现行载体）

| 载体 | 承载内容 | 规则 |
|------|---------|------|
| **GitHub Issue** | 需求、缺陷（finding）、决策、阻塞 | 优先复用现有 Issue（决策类如 #41/#130，工作类以 AID 归属 Issue 为准）；实质会话必须有归属 Issue/PR；缺陷=finding 以 BLOCKER/P0–P3 记入 Issue 评论或 Closeout |
| **GitHub PR** | 集成单元 | PR-GOVERNANCE-001 §3 准入与合并整理：先搜现有载体；独立可审查单元才开新 PR；禁止重复/拆分刷记录 |
| **Work Item** | `AID-YYYY-NNN` + `work-items/AID-YYYY-NNN/manifest.yaml` | 实质工作开始前创建；注册规则见 [INDEX.md](work-items/INDEX.md)（唯一编号、先建目录和 manifest、链接提示词版本与哈希、重大门禁与结项时更新、被拒/受阻记录不删除） |
| **INDEX.md** | 会话级交付记录一行 | AI-STD-001 §13 指定由 Integration Owner 维护；缺证据标 `NOT RECORDED` 禁止补造 |
| **Closeout** | Issue/PR 评论 | AI-STD-001 §13 八项 ∪ PR-GOVERNANCE-001 §2 九项 ∪ §7.1 双语门禁结果（AI-EXEC-002 §6 模板） |

**不用脚本限制，也不用标签冒充门禁**（PR-GOVERNANCE-001 §7）：Label/模板只是检索与书写便利；真正的约束是上述记录义务 + 审查处置 + owner 权威。

## 5. PR 纪律（= PR-GOVERNANCE-001 现行条款的执行口径）

1. **五态处置**（§6 原文）：`MERGE / HOLD / REMEDIATE / SUPERSEDED / REJECT`——每次合并决策必须五选一并写明缺项或理由。
2. **Exact-Head 门禁**（§4）：一切检查与审批必须指向当前 Head SHA；Head 变更则证据刷新。旧 Head 检查、其他 PR 的绿勾、本地口头声明均不算；缺失/待定/跳过/失败 = NOT PASS。
3. **流动性运行纪律**（运行层，不依赖平台强制）：open PR ≤ 10，**先清后开**；每周一个集成窗口集中合并清淤（对应 PR-GOVERNANCE"验证即合入"原则：满足 MERGE 条件及时合入，不为堆积审查轮次而搁置）。违规不拦截，但在回顾记 finding。
4. **非 main 目标分支的 PR** 保留其目标分支与依赖链，不得擅自改投 main；主线发布另建集成 PR（§3）。
5. 合并后**回读目标分支**，记录真实 merge commit SHA（§6）。

## 6. 审查与例外（NR-001 + PR-GOVERNANCE-001 §5）

| 场景 | 要求 |
|------|------|
| R0/R1 低风险文档 | 作者与审查者区分即可；一人可覆盖多个审查维度（AI-STD-001 §3.2） |
| R2 | 独立 ChatGPT 会话审查（NR-001）+ 受影响 Owner 明确批准其契约边界 |
| R3 | 独立审查 + **安全/领域专家审查** + 可复现测试证据 + Acceptance Authority 明确批准 |
| 涉安全/身份/授权/Forget/生命周期/持久化/恢复/跨 Owner 契约 | 审查者必须独立于作者与实现会话（PR-GOVERNANCE §5） |

**例外（owner-directed exception）**：
- 仅限 R2/R3 的**时效豁免**（如审查会话不可用），不适用于证据缺失、NOT RUN 混同；
- 必须显式记录在 Issue/Closeout（豁免理由 + 补审计划）并计数——"例外必须显式记录，不得默默豁免"（§5 原文）；
- 每迭代例外 ≤ 2；连续 2 迭代超限 → 触发日度治理窗口做**规则修订**（说明流程不现实，修订而非硬扛）。此配额为**本细则新增运行纪律**（非上位文档条款），违规不拦截、记 finding。

## 7. 日度治理窗口（AI-STD-001 §11 的日度化——闭环关键）

**每日一次、固定时段、≤ 20 分钟**，与迭代边界解耦。这是"反馈流回接规则流"的唯一入口：

1. **输入**：当日规则类 finding（提示词/流程/契约缺陷）+ 最近一次迭代回顾改进项（AI-PROC-001 §4 指标清单产出）。
2. **动作**（照 AI-STD-001 §11 七步）：停止/隔离不安全部分 → 开 finding/变更请求 → 指定权威 Owner → 决策记录（rationale/alternatives/consequences）→ 提示词升版本 → 更新依赖任务与兼容测试 → 获批后恢复执行。
3. **产出**：修订 PR **当日合并生效**（owner 一票），文档头 `Status` 翻转（PROPOSED→ADOPTED/ACTIVE），受影响提示词出新版本。
4. **回流登记**：对应 finding/Issue 评论注明"回流 RW-YYYYMMDD / PR #N"；当日排不上的顺延次日，积压每日清零。

## 8. 迭代回顾（AI-PROC-001 §4 照常，收口到日度窗口）

每迭代末 30 分钟，按其指标清单记录：lead time / active time、提示词澄清修订次数、finding 按严重级、合并后逃逸缺陷、新增测试与 NOT RUN 项、陈旧依赖返工、跨 Owner 契约冲突、文档漂移。产出 ≤ 3 条改进项，进次日日度治理窗口。

## 9. 闭环验收（让 G0–G7 真正转起来的判定）

满足 5 条即"生态循环达成"，进入加强阶段：

1. **规则生效**：核心上位文档（AI-STD-001、AI-PROC-001、AI-PROMPT-STD-001 等）按 owner-directed adoption 转 ADOPTED，记录可查（模式同 PR-GOVERNANCE-001 / Issue #130）。
2. **跑通验证**：连续 2 个迭代走完 Stage 0–8，Work Item 状态无跳态推进至 CLOSED（或 BLOCKED 记退出条件）。
3. **追溯测试**：抽 3 个已合并 PR，全链路可查——`AID / manifest → Prompt ID+版本+commit SHA → Issue → PR Head → 测试证据 → 审查 finding → Closeout → INDEX 行`。
4. **证据诚实**：NOT RUN 零混同 PASS；新增记录中 Prompt 出处（ID+版本+commit SHA）零 NOT_RECORDED；同作者审查全部披露。
5. **流动健康**：open PR ≤ 10 且无超 7 天滞留；满足 MERGE 条件的 PR 不搁置；每迭代例外 ≤ 2。

---

## 附 A：现状差距 → 本细则对应动作（全部落在现行文档机制内）

| 现状证据（仓库实证） | 对应动作 | 落点 |
|---|---|---|
| 6 份规范 PROPOSED 从未生效 | owner-directed adoption 批量转 ADOPTED（模式复制 PR-GOVERNANCE-001） | §1 |
| prompt hash `NOT RECORDED` 泛滥 | Prompt ID + 版本 + commit SHA 三元组；SHA-256 允许 NOT_VERIFIED，禁补造 | AI-EXEC-002 §2 |
| 142 PR 仅登记 2 个 Work Item | 实质工作前建 AID + manifest；PR 准入整理先搜现有载体 | §4、PR-GOVERNANCE §3 |
| 0 独立审查、例外成常态 | NR-001 独立会话 + finding 体系 + 例外显式计数 | §6 |
| PR 堰塞湖（76 open/72 draft） | 10 上限先清后开 + 每周集成窗口 + 五态处置及时 MERGE | §5 |
| 测试 NOT RUN 混同 PASS | 三值明示 + exact-Head 证据 + DoD 原文执行 | §2 Stage 5、AI-EXEC-002 §4 |
| 双提示词库并存 | 记录实际所用库与版本，合一列加强项 | AI-EXEC-002 §1 |

## 附 B：本细则与上位文档的关系

- 本文**不修改** AI-STD-001 / AI-PROC-001 / PR-GOVERNANCE-001 / AI-PROMPT-STD-001 的任何条款定义；
- 凡冲突处以上位文档为准；本文只补充"怎么跑、留什么痕、多久闭环"；
- 已知上位冲突三处（AI-STD-001 §5 十五项 vs AI-PROMPT-STD-001 §4 十二项；§10 词表 TESTED vs 会话契约 VERIFIED；AI-STD-001 §5 SHA-256 必录 vs AI-PROMPT-STD-001 §5 NOT_VERIFIED）——已在 AI-EXEC-002 显式披露，统一口径列入 Issue #218 adoption 决议；
- 本文自身的修订同样走 §7 日度治理窗口。
