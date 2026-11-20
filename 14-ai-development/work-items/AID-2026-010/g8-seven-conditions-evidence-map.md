# G8 七项条件逐项证据映射（L0 测量记录）

**记录日期：** 2026-11-20
**记录角色：** L0 协调层（机械映射，不作架构裁定）
**条件来源：** `state/a-r22-full.md` L276–282（A-OWNER-ALIGNMENT-001-R22 §四「距离 G8 FREEZE-READY 还差什么？」）
**说明：** 该七项条件目前**无仓库内载体**——只存在于会话裁决文本中。本记录是首个仓库内映射，不改变条件本身。

---

## 一、七项条件逐项映射

| # | 条件原文（逐字） | 当前证据位置 | 实测状态 | 缺口 |
|---:|---|---|---|---|
| 1 | D Owner 对 1.3.0 权威性和双高水位给出正式、精确版本绑定的决定。 | `finding-ledger.md:71`（`D-OWNER-2026-11-19-001` 采纳 BLOCKED / `D-OWNER-2026-11-19-003` 1.3.1 successor ACCEPT）；`finding-ledger.md:26`（`D-OWNER-2026-11-19-002` 六条件 ACCEPT） | PARTIALLY-SATISFIED | 1.3.0 本身仍 `BLOCKED`（`D-OWNER-2026-11-19-001`）；被 ACCEPT 的是 1.3.1 successor，非 1.3.0。条件字面要求「1.3.0 权威性」，当前无 1.3.0 采纳决定。 |
| 2 | H 在真实 Owner 分支修复组合验证器，并通过最终 HEAD 测试。 | `finding-ledger.md:41`（F-43-01/F2 CLOSED，R26；Commit `19a83933`，测试 Blob `f4126e20`，L0 独立重跑 22/22 PASS） | SATISFIED | 无。限 TEST-profile 范围（见该条「范围限制」）。 |
| 3 | H Owner 独立接受具体 D/H 消费契约，不能由 D 或 A 代替。 | `finding-ledger.md:56`（`H-OWNER-2026-11-19-001` 对 H mapping Blob `e60bdd4c` 作 ACCEPT WITH EXPLICIT LIMITATIONS，#43 `7021523060` + 补充 `7021543287`） | SATISFIED | 接受附明确限制（`ACCEPT WITH EXPLICIT LIMITATIONS`），未覆盖 endpoint/transport、真实 Receipt、生产密钥。 |
| 4 | D/H 双向映射、Currentness、操作身份和并发向量通过核验。 | `finding-ledger.md:56`（D `D-OWNER-2026-11-19-006` 对同一 Blob 独立 ACCEPT；`D-OWNER-2026-11-19-007` `D-AUTH-QUERY-1.0` ACCEPT，Commit `4c5183ab` / Blob `da69b840`；A R35 接受）；F-43-01/F3 CLOSED（`:52`） | PARTIALLY-SATISFIED | 双向映射、Currentness、操作身份、`D-Ledger-Consistency-Proof-v1` 规范层已核验；**并发向量未核验**（该条明确排除「Runtime 测试及 CI 均未验证/未运行」）。 |
| 5 | 全系统 P0/P1 风险有各自 Owner 的证明和接受。 | 仅 `prompt-batch2-dispatch.md:68` 与 `:102` 提及 P0/P1 作为 G4 判据与矩阵要求；`development-readiness-register.md` 43 项中无 P0/P1 逐项 Owner 证明与接受条目 | NO-EVIDENCE | 无任何仓库内 P0/P1 逐项 Owner 证明与接受记录。R-01..R-10 为风险分类，非「各自 Owner 的证明和接受」。 |
| 6 | JF-10 P0、#134 P0、Storage 物理拓扑、Global Forget 与恢复防复活等既有阻塞仍需解决。 | `development-readiness-register.md:41`（R-03 Forget / Anti-Resurrection = NOT PROVEN）；同表 Storage 域 = 「physical deployment unproven; L4 and joint D/I acceptance OPEN」；#10（JF-10 P0）`open`，69 评论；#134 **已于 `2026-11-19T17:28:27Z` 以 `completed` 关闭**，残余四项转入 #283；#25 `open`，175 评论 | NOT-SATISFIED | R-03 仍 NOT PROVEN；Storage 物理部署未证；L4 与 D/I 联合验收 OPEN；JF-10（#10）仍 OPEN 且无仓库内状态记录。**更正**：#134 已关闭，其关闭评论 `7016767763` 明确「关闭不等于平台强制已达成」，残余四项（required-check 强制、蓄意失败合并阻断、force-push/删除/绕过限制、P-independence）转入 #283。条件 6 因此部分由 #283 承接：**#283 实测 `open`，16 评论，最近更新 `2026-11-20T06:00:14Z`**，标题 `PLATFORM-RESIDUAL — required-check enforcement and branch controls (trigger-based re-verification)`。故 #134 分支的残余仍 OPEN，只是载体从 #134 转为 #283。 |
| 7 | 双语规范一致性、全系统证据新鲜度和技术可行性达到 #43 的验收要求。 | `.github/workflows/bilingual-docs.yml` + `scripts/check_bilingual_docs.py`（结构性检查，自述不保证语义等价）；`ci-evidence-validity-correction-2026-11-20.md`（CI 自 2026-11-19T15:53Z 起未执行）；`pr-backlog-convergence-plan.md` §6（G6 语义等价需独立合格审查） | NOT-SATISFIED | 双语一致性仅结构性检查，语义等价 NOT VERIFIED；证据新鲜度因 CI 计费阻断中断（100/100 零步骤）；技术可行性无 #43 验收结论。 |

**状态统计：** SATISFIED 2 / PARTIALLY-SATISFIED 2 / NOT-SATISFIED 2 / NO-EVIDENCE 1 / 合计 7。

## 二、性质判定：验收前置 vs 开发准入

| # | 性质 | 理由（一行） |
|---:|---|---|
| 1 | 架构验收前置 | 要求 D 对契约权威性作决定，属规范采纳，不是可写代码的前置。 |
| 2 | 架构验收前置（已满足） | 组合验证器修复已完成，其性质是实现修复而非准入条件。 |
| 3 | 架构验收前置（已满足） | Owner 间契约接受是跨域治理动作，不是开发准入。 |
| 4 | 架构验收前置 | 映射/Currentness/身份核验属跨域一致性验收，实现工作可先行。 |
| 5 | 架构验收前置 | P0/P1 风险的 Owner 证明与接受是系统级验收证据。 |
| 6 | 架构验收前置 | 既有阻塞项（JF-10/#134/Storage 拓扑/防复活）是系统验收项。 |
| 7 | 架构验收前置 | 双语一致性、证据新鲜度、技术可行性属 #43 验收口径。 |

**七项全部为架构验收（G8 FREEZE-READY）前置条件，无一为开发开工的准入条件。**

该判定与 `development-readiness-register.md:50` 一致：G8 记 `NOT READY` 且 `DOES-NOT-BLOCK`，理由列为「Blocks architecture/system acceptance and any G8 readiness claim; it is not the engineering-baseline entry gate.」同文件 `:106` 重申「G8 remains NOT READY and architecture remains NOT ACCEPTED. Neither is being waived by this entry ruling.」

## 三、本记录不改变的事项

- 不改变 G8 `NOT READY`，不改变架构 `NOT ACCEPTED`。
- 不改变任何 finding 状态，不改变 `development-readiness-register.md` 的 43 项判定。
- 不构成开发开工授权、生产授权、角色任命或配额解冻。
- 七项条件仍未获得仓库内规范载体；本记录只是测量映射，不使其成为正式验收基线。

## 四、复现方式

```bash
cd state/repo
sed -n '276,282p' ../a-r22-full.md            # 七项条件原文
grep -n 'G8' 14-ai-development/work-items/AID-2026-010/development-readiness-register.md
grep -n '^| 状态 |' 14-ai-development/work-items/AID-2026-010/finding-ledger.md
```

---

## 五、更正日志（L0，2026-11-20T12:15Z）

| 更正项 | 原记载 | 实测 | 依据 |
|---|---|---|---|
| 条件 6 中 #134 状态 | 「#134 未在 AID-2026-010 目录内出现……无法从仓库核验其是否仍 OPEN」 | **已关闭 `2026-11-19T17:28:27Z`，reason=`completed`** | `GET /issues/134`；关闭评论 `7016767763` |
| 条件 6 残余去向 | 未记载 | **#283 `open`，16 评论，更新 `2026-11-20T06:00:14Z`** | `GET /issues/283` |
| 条件 6 中 JF-10 | 「无法核验」 | **#10 `open`，69 评论**（JF-10 P0） | `GET /issues/10` |
| 条件 6 中 Storage/#25 | 未记载 Issue 号 | **#25 `open`，175 评论**（Phase 3.8 D/E/I/Storage） | `GET /issues/25` |

**更正不影响判定。** 条件 6 的 `NOT-SATISFIED` 结论不变：R-03 仍 NOT PROVEN、Storage 物理部署未证、L4 与 D/I 联合验收 OPEN、#283 残余仍 OPEN、#10 仍 OPEN。改的是**证据可追溯性**——原记载称「无法核验」，实测可核验且状态已明。

---

**记录边界：** 本记录只映射证据，不裁定 G8 是否可推进、不裁定开发是否可开始。二者分别属 Architecture Owner 与相应裁决权威。
