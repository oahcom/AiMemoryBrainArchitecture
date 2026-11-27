---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "正文与全部计数与原始测量一致，未改动。2026-11-23 追加的附注引用两次首次执行（自托管 45011672799、托管 45037267638），均于本次会话从 GitHub Actions REST API 读取。"
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-20-CI-NOT-EXECUTED-005.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-20-CI-NOT-EXECUTED-005.md"
    zh-CN: null
---

# GOV-NC-2026-11-20-CI-NOT-EXECUTED-005 — 门禁连续 36 小时零执行登记

- 登记编号：GOV-NC-2026-11-20-CI-NOT-EXECUTED-005
- 状态：`ACCEPTED` / `CI_NOT_EXECUTED` / 执行侧完全缺失（Owner 裁定 2026-11-21）
- 观测时间：2026-11-21T04:10Z（最后一次取数）
- 观测对象：仓库 `oahcom/AiMemoryBrainArchitecture`，`main` 与其上全部 PR
- 关联：#352（配额临时规则）、#281 / PR-GOVERNANCE-001-ENFORCEMENT v1.2（平台检查不可用的补偿证据规则）、#405（自托管替代尝试）、#403 / #402（本轮合并实例）

## 1. 为什么单独登记

此前三份登记分别记录了：直推绕过 PR、裁定后无审查合并、AC 判定错误。它们共享一个未被单独写下的前提——**这些合并发生时，仓库的结构化门禁一次都没有真正运行过**。

「CI 是红的」和「CI 从来没跑」是两种完全不同的状态。前者说明代码有问题，后者说明**没有任何自动化结论存在**。本登记只做后者：把「零执行」这件事按 run 粒度数清楚，并把它的后果写成可核验的账目。

本登记不重复 #352 的原因分析，也不重复 #405 的替代方案分析。它只回答一个问题：这段时间里，平台侧到底给出了几次门禁裁决。

## 2. 判定规则（与既有 P7 规则一致）

对任一 run，读取 `/repos/{repo}/actions/runs/{id}/jobs`：

| 形态 | 判定 |
|---|---|
| `steps` 为空数组且 `runner_name` 为空字符串 | `NOT_EXECUTED` |
| 有 runner，但失败发生在 `Set up runner`，本项目步骤全部 `skipped` | `NOT_EXECUTED`（门禁逻辑未运行） |
| 项目步骤实际执行并给出 `conclusion` | `EXECUTED` |

`conclusion: failure` 本身不构成 `EXECUTED` 的证据。`failure` 与「测试失败」之间没有蕴含关系。

### 2.1 五层必须分开，不能压缩成一个字段

Owner 在 2026-11-21 裁定中要求本登记显式区分以下五件事：

| 层 | 内容 | 本窗口的事实 |
|---|---|---|
| 1 | CI 平台产生了 run | 是，362 个 |
| 2 | run 被分配了 `conclusion` | 是，348 `failure` / 13 `skipped` / 1 `success` |
| 3 | runner 是否启动 | 345 个未启动；3 个启动后在 `Set up runner` 失败 |
| 4 | **门禁逻辑是否实际执行** | **0 次** |
| 5 | 门禁逻辑执行后的结果 | 不存在（第 4 层为 0） |

第 2 层有一个 `success`，但它**不能仅凭 `conclusion` 推定执行过门禁逻辑**；第 3 层的 3 个自托管 run 也不能读成「自托管能救 CI」，因为项目步骤全部 `skipped`。

**本登记的结论只能用于「第 4 层为 0」这一治理事实，不能据此声称仓库门禁本身通过或失败。** 任何 exact-Head 本地执行（如 #419 的补偿证据）属于第 5 层的人工替代，不是 CI 执行证据。

## 3. 边界：最后一次真实执行，和第一次空执行

| | run | 时刻 | 结论 | steps | runner |
|---|---|---|---|---|---|
| 最后一次真实执行 | `44559466007`（Bilingual documentation gate） | 2026-11-19T15:51:14Z | `success` | 5 | `GitHub Actions 1000002033` |
| 第一次空执行 | `44563397286`（GOV-DOC-001 structural checks） | 2026-11-19T16:12:11Z | `failure` | **0** | `''` |

`44563397286` 的 check-run annotation 原文：

```
The job was not started because recent account payments have failed or your
spending limit needs to be increased. Please check the 'Billing & plans'
section in your settings
```

同一句 annotation 在 2026-11-19T16:12 至 2026-11-21T04:10 的每一个空执行 run 上重复出现。它不是测试反馈。

**边界结论：2026-11-19T16:12:11Z 之后，本项目没有再产生过一次门禁裁决。**

## 4. 全量普查（逐 run，非抽样）

取 `/actions/runs?per_page=100` 连续 5 页，覆盖 2026-11-18T12:56:35Z → 2026-11-21T04:10:03Z 共 500 个 run。

边界之后的分布：

| 指标 | 数值 |
|---|---|
| 边界后 run 总数 | 362 |
| `failure` | 348 |
| `skipped` | 13（全部为 `issues` 事件，`AI Owner Worker`） |
| `success` | 1 |
| **其中 `failure` 里逐 run 复核过的** | **348 / 348** |
| → `NOT_EXECUTED`（`steps=[]`, `runner=''`） | **345** |
| → 分配到自托管 runner 后在 `Set up runner` 失败，项目步骤全 `skipped` | **3** |
| → 真正执行了门禁逻辑并给出结论 | **0** |

那 3 个例外值得单独写明，因为它们曾被误读为「自托管可以救 CI」：

| run | workflow | runner | 失败步 | 项目步骤 |
|---|---|---|---|---|
| `44862136704` | Rust Phase 1 Workspace Tests | `zesu-x64` | 2 `Set up runner` | 全部 `skipped` |
| `44862136705` | Bilingual documentation gate | `zesu-x64` | 2 `Set up runner` | 全部 `skipped` |
| `44862537055` | Bilingual documentation gate | `zesu-x64` | 2 `Set up runner` | 全部 `skipped` |

三者都在第 2 步被拒绝，第 3 步起（checkout / 检查脚本）全部 `skipped`。**门禁脚本一行都没跑。**

唯一的 `success` 也不是门禁：

| run | workflow | 触发 | runner | steps |
|---|---|---|---|---|
| `44861020897` | `ubuntu-worker-diagnostics.yml` | `workflow_dispatch` on `main`（actor `oahcom`） | `zesu-x64`（`self-hosted, linux, x64`） | 4（Set up job / Set up runner / Read-only host diagnostics / Complete job） |

它证明自托管 runner 活着且能跑 `workflow_dispatch`；它不证明任何 PR 合规。

## 5. 这段时间里发生了什么合并

同窗口内 `merged_at >= 2026-11-19T16:12:11Z` 的 PR：**85 个**（#289 … #408，作者全部为 `oahcom`）。

| 指标 | 数值 |
|---|---|
| 合并总数 | 85 |
| 有 `APPROVED` 审查的 | **0** |
| 审查事件总数（全窗口） | 36，**全部为 `COMMENTED`，全部来自 `oahcom`（= 作者 = 合并者）** |
| 完全无任何审查的 | **64** |
| 在 #352 裁定（2026-11-20T09:03:35Z）之前合并的 | 42 |
| 在 #352 裁定之后合并的 | 43 |

**没有任何一次合并的审查来自第二个账号。** 这不是「审查意见写得不好」，是这一时段内该仓库不存在第二个审查主体。

> **2026-11-25 附注（引文时效）。** 上一段的第一句是测量，取不回：85 次合并里没有一次审查来自第二个账号。第二句不是测量——「该仓库不存在第二个审查主体」把「没有第二个账号」推成了「没有第二个审查主体」。按 2026-11-24 修订后的 §5，审查主体是会话，第二个会话一直开得出来；这一时段缺的是有人去开，不是位置本身不存在。结论不变（该窗口确实零独立审查），但依据换了：那不是结构性空缺，是一条当时没人认领的待办。同一处错误的完整说明见 `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §12.4 与 `GOV-REV-2026-11-24-CONVERGENCE-CEILING-034` §9。

## 6. 本登记自身的第一个样本：PR #409 在门禁下是红的

这是本轮唯一一次「门禁真的跑了一次」——由我在本地对 exact Head 执行同一脚本得到，不是在 CI 里。

| 项 | 值 |
|---|---|
| PR | #409（本登记随该 PR 提交） |
| 门禁脚本 blob | `ce072be30a9d9d53c6f4e4add3b9cbc59f192d25`（24404 B，BASE 与 HEAD 同一 blob） |
| BASE | `423fb4b7e62f…`（本地重建 `26b702fd8864…`） |
| HEAD | `ccd19ecd91f0…`（本地重建 `f3df9d670fc8…`） |
| 首次执行 | `::error::Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED'.` / `EXIT=1` |

也就是说：**#409 的第一版 PR 正文会让门禁退出 1**。这个缺陷在 CI 可用的日子里会在提交后一分钟内被拦下；在门禁零执行的 36 小时里，它只能靠人肉本地复现才发现——而且如果没有本登记，没人会去复现。

这构成一个可复用的结论：门禁零执行期间，**唯一仍在工作的检测通道是「有人主动在 exact Head 上本地跑一遍」**。#281 早已把这条通道写成规则（PR-GOVERNANCE-001-ENFORCEMENT v1.2 §1「平台检查不可用」），并在同一天 16:57Z——空执行开始 45 分钟后——点名了 `44563397286` 这个 run。规则存在，通道可用，但它是**自愿的**，且它的产出不进 `checks` 字段。

## 7. 客观事实与推断的分界

事实（可逐条复算，见 §8）：
- §3 两个 run 的时刻、steps、runner、annotation 原文。
- §4 全部计数：362 / 348 / 345 / 3 / 1 / 0。
- §5 全部计数：85 / 0 / 36 / 64 / 42 / 43。
- §6 本地执行的命令、输入、输出、退出码。

推断（**本登记不作出**）：
- 不判定 85 次合并在治理上是否「违规」。`#352` 规则 1 已把 CI 结果从合并判据中移除；这些合并在该规则下是被允许的。规则 2 要求的「本地可复核证据」是否逐次满足，属审查者判断，不由本登记代替。
- 不判定被合并代码的正确性。没有证据，就没有结论——这正是本登记要说明的状态。
- 不把 `NOT_EXECUTED` 读成 `PASS`，也不读成 `FAIL`。

## 8. 复算方式

```bash
# 1) 边界后的 run 列表
GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runs?per_page=100&page=1..5

# 2) 逐 run 判定
GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runs/{id}/jobs
#   steps == [] 且 runner_name == ""  -> NOT_EXECUTED

# 3) annotation 原文
GET /repos/oahcom/AiMemoryBrainArchitecture/check-runs/{job_id}/annotations

# 4) 合并与审查
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=closed&per_page=100
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/{n}/reviews

# 5) 本登记 §6 的本地复现
BASE_SHA=<base> HEAD_SHA=<head> PR_BODY="$(cat pr_body.txt)" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"
```

## 9. 处置要求（不代 Owner 决定）

| 编号 | 要求 | 归属 |
|---|---|---|
| R-1 | 在恢复前，任何 2026-11-19T16:12:11Z 之后创建的 PR，其 `checks` 一律按 `NOT_EXECUTED` 登记，不得写作「测试通过」或「测试失败」 | 本登记已执行 |
| R-2 | 恢复通道的取舍（付费 hosted / 转公开 / 自托管 post-merge `push` 按 runbook §4.1 option 4 / 维持现状）属 Owner 决定，#405 已把四条路的边界写清 | Owner |
| R-3 | 85 次合并中「本地可复核证据」是否逐次满足 #352 规则 2/5，需要一次独立抽样复核；本登记不代替该复核 | 独立审查 |
| R-4 | `checks: failure` 不得作为任何 REQ-06…REQ-12 验收链路的证据；引用时必须同时写明 run id 与 `NOT_EXECUTED` 判定 | 验收链 |

## 10. 与既有登记的关系

- **GOV-NC-2026-11-20-MERGE-AFTER-RULING-003**：#403 合并时 check 为 `failure`，本登记说明该 `failure` 是 `NOT_EXECUTED`，不是门禁否决。实例计数仍按 Owner 裁定冻结为 4，本登记不改动该计数。
- **GOV-NC-2026-11-20-DIRECT-MAIN-001**：直推 62 次同样落在零执行窗口内；该登记的结论（直推绕过 PR 通道）不因本登记改变，但其中「push 触发的工作流会检查」这一隐含前提不成立。
- **GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004**：AC-5 的更正基于本地三次重测，与 CI 无关；本登记不影响该更正。

**登记状态**：`ACCEPTED` / `CI_NOT_EXECUTED` / 36 小时内门禁逻辑实际执行 **0 次** / 期间合并 **85 次** / 其中 `APPROVED` **0** 次

Owner 裁定（2026-11-21）：接受本登记的统计边界与 `NOT_EXECUTED` 归类。同时明确——**本登记可以作为治理事实登记，但不得据此声称仓库门禁本身通过或失败**；#419 的本地 exact-head 实测是补偿性证据，不是 CI 执行证据。

---

## 11. 执行侧于 2026-11-22 恢复（2026-11-23 附注）

本登记的正文与计数**不改动**。它记录的是 2026-11-19T16:12Z 起 36 小时窗口内的事实，那些事实没有变。

但本登记的状态行是现在时（「执行侧完全缺失」），而执行侧已经恢复。首次真实执行：

| | 首次执行 `cargo test --workspace --all-targets` | run | head | runner |
|---|---|---|---|---|
| 自托管 | 2026-11-22T10:17:02Z | `45011672799` | `550bb864` | `zesu-x64` |
| GitHub 托管 | 2026-11-22T15:15:13Z | `45037267638` | `38c3c975` | `GitHub Actions 1000005167` |

后果：本登记「不得据此声称仓库门禁通过或失败」的限制**仍然有效**（执行了不等于可信），但「CI 在本仓库中不会执行」这一读法**已经失效**。凡引用本登记作为该前提的依据者，必须改引 `GOV-NC-2026-11-23-EXECUTION-RESTORED-029`。

本附注由 owner-proxy 会话添加，不是独立审查，也不改变本登记的 `ACCEPTED` 状态——那个状态是对**窗口内统计**的裁定，不是对现在的能力判断。
