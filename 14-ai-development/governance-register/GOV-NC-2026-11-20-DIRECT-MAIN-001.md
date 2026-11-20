# GOV-NC-2026-11-20-DIRECT-MAIN-001 — 直接推送 main 治理缺陷登记

**登记依据**：协调会话裁决（`6b00735c-1a10-3e03-8b46-3c8eb4b06a5`，2026-11-20）Q2，要求建立一条统一缺陷记录，禁止拆散为 33 个互不相关的部门问题。

**状态**：`OPEN` / `NOT_REMEDIATED`

**缺陷类别**：Governance Conformance
**严重度**：High
**失效模式**：Bypass of mandatory PR gate
**影响范围**：`main` 分支全部规范性路径

---

## 1. 调查范围与方法

| 项目 | 值 |
|---|---|
| 仓库 | `oahcom/AiMemoryBrainArchitecture` |
| 调查基准 | `main` @ `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| 调查区间 | 最近 100 个 `main` commit（`per_page=100`） |
| 判定方法 | 对每个 commit 调用 `GET /repos/{owner}/{repo}/commits/{sha}/pulls`；返回空数组即判定为未经 PR 进入 `main` |
| 采集时间 | 2026-11-20T14:20Z–14:25Z |
| 结果 | **67 via PR / 33 direct** |

判定依据条文：`14-ai-development/PR-GOVERNANCE-001.md` §3

> A pull request is mandatory **if and only if the merge target is `main`**, regardless of the source branch (Owner primary, child/work, research or recovery branch). Every change targeting `main` must enter through a PR and satisfy the applicable exact-Head checks and review gates.

> 只有合并目标为 `main` 时才必须创建 PR，且不受来源分支类型限制…所有目标为 `main` 的变更都必须通过 PR 集成，并满足适用的精确 Head 检查和审查门禁。

该条文给出**唯一**例外：合并目标为非 `main` 分支时不需要 PR（§3 第 2 段）。33 个 commit 的合并目标全部是 `main`，不落入该例外。

---

## 2. 缺陷清单（33 个 commit）

按作者分组。全部 `verification.verified = false`（GitHub 签名验证未通过或未签名），33/33。

### 2.1 `Ubuntu <ubuntu@localhost.localdomain>` — 15 个

时间戳高度集中：`2026-11-20T11:53:40Z`–`11:53:41Z`（跨度 2 秒内 15 个 commit）。

全部为 AID-2026-014 修正批次。

### 2.2 `oahcom <81014746+oahcom@users.noreply.github.com>` — 14 个

分散于 2026-11-20T06:20Z–14:14Z。含 AID-2026-014 的 manifest / INDEX / prompt 登记、AID-2026-011 记录修正、architecture-convergence 目录重组。

### 2.3 `L0-manager <l0@local>` — 3 个

全部 `2026-11-20T14:11:00Z`（同一时间戳）。改动 AID-2026-014 的 R1/R5/G 修正。

### 2.4 `unknown <1491856051>` — 1 个

`2026-11-20T13:40:07Z`。新增 `docs/governance/ARCHITECTURE_AUDIT_REPORT.md`、`docs/architecture-convergence/README.md`，并重命名 `docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md` → `docs/governance/archive/aid-2026-014-r3-correction-status.md`。

---

## 3. 作者与时间分布汇总

### 3.1 33 个直推 commit 内部构成

| 作者 | email | 直推数量 | 时间特征 |
|---|---|---:|---|
| `Ubuntu` | `ubuntu@localhost.localdomain` | 15 | 2 秒内 15 个 |
| `oahcom` | `81014746+oahcom@users.noreply.github.com` | 14 | 分散 8 小时 |
| `L0-manager` | `l0@local` | 3 | 同一时间戳 |
| `unknown` | `1491856051` | 1 | 单点 |
| **合计** | | **33** | |

### 3.2 同一区间内各作者的 main 总量（口径校正）

同一 100-commit 区间的按 email 全量统计为：

| email | main 上总数 | 其中直推 | 其中经 PR |
|---|---:|---:|---:|
| `81014746+oahcom@users.noreply.github.com` | 79 | 14 | 65 |
| `ubuntu@localhost.localdomain` | 15 | 15 | 0 |
| `l0@local` | 5 | 3 | 2 |
| `1491856051` | 1 | 1 | 0 |
| **合计** | **100** | **33** | **67** |

**口径说明**：§2.3 与 §3.1 中的 `L0-manager 3 个` **仅指 33 个直推 commit 中的数量**，不等于该身份在 main 上的全部产出。同区间 `l0@local` 在 main 上共 **5** 个 commit，其中另 **2 个经 PR 进入**，不构成本缺陷的样本。

同理，`oahcom` 的 14 个直推不等于其全部 79 个产出；`oahcom` 另有 65 个 commit 走 PR 门禁，说明该身份**具备**正确走 PR 的能力，其 14 次直推不是工具或权限限制所致，而是选择性绕过。这一点对 §6 的纠正措施定责有意义。

`unknown` 的 email `1491856051` 不是合法邮箱格式（无 `@`），是本地 git 配置缺失产物。

---

## 4. 涉及文件与规范性影响

33 个 commit 共触及 **20 处规范性路径**（`00-governance` … `14-ai-development` 一级目录下）。

语义变更集中在 `02-domain-model`：

| commit | 作者 | 触及文件 |
|---|---|---|
| `74a531814c` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §3.15 |
| `d575ebc254` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §2.4 |
| `08630cf875` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/core-entities.md` + root source |
| `7873b5768f` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/relationships-and-provenance.md` |
| `0e8ce367de` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §8.1 |
| `1cd36650f1` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §1/§4/§11/§12 |
| `5429eff46d` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/phase-1-domain-model-freeze.md` |
| `bc114263d7` | oahcom | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` + `phase-1-domain-model-freeze.md` |
| `778d1beec4` | L0-manager | `02-domain-model/domain-model-overview.md`（root） |
| `2606978e6c` | L0-manager | `06-memory-context/context-versioning.md`（+159/-3） |

**关键影响**：`02-domain-model` 的语义变更是直推的。这正是 AID-2026-026 原定要研究的领域，也是 AID-2026-014 裁决落地的载体。**该领域的规范性文本在无 review、无 exact-Head 检查的情况下被修改了 10 次。**

---

## 5. PR-GOVERNANCE-001 §3 违反情况

| 检查项 | 结果 |
|---|---|
| 合并目标是否 `main` | 33/33 是 |
| 是否有 PR | 33/33 无 |
| 是否落入 §3 非-main 例外 | 33/33 不落入 |
| 是否满足 exact-Head 检查（§4） | 33/33 无法满足（无 PR 即无 Head 门禁） |
| 是否取得独立审批（§5） | 33/33 无 |

**结论**：33 个 commit 全部违反 §3。这是路径违规，不是内容错误判定。

---

## 6. 关联事项：PR #354 的 review / exact-Head 缺失

PR #354 独立记录，不与 33 个直推 commit 混同。

| 项目 | 值 |
|---|---|
| PR | #354 |
| 是否通过 PR | 是（形式上满足 §3） |
| merged_by | `oahcom` |
| merged_at | 2026-11-20T12:51:09Z |
| merge_commit_sha | `8215ec57260b5841df1b9f9aad5a7f26d3073bac` |
| head at merge | `dfb56fa1aa9947f2fa77b0779dc814ea758a9ab0` |
| commits | 2（`6966df5e9e`、`dfb56fa1aa`） |
| **reviews** | **0** |
| **exact-Head 检查结论** | **无**（该 Head 的 `check-runs.total_count = 0`） |

按 §4：

> 缺失、待定、跳过或失败的适用检查均不算 PASS。

按 §5：

> 作者与审查者使用同一 GitHub 身份时，不构成独立审查。

**裁决（协调会话）**：PR 的存在只满足进入 PR 流程这一形式条件，不能替代 review 和 exact-Head 检查。这次合并不得追溯性地认定为完整合规。

---

## 7. 授权主体与提交机制待核实

以下三个执行身份，在仓库中检索不到任命文件、权限范围或授权来源：

| 身份 | 出现形式 | 可查到的治理依据 |
|---|---|---|
| `L0-MAIN-WRITER-01` | Issue #43 comment `7034237663` 提及 | 仅作为「prompt 装配与路由元数据的作者」出现，无权限定义 |
| `L0-manager <l0@local>` | 3 个直推 commit | 无 |
| `unknown <1491856051>` | 1 个直推 commit | 无 |

三者是否同一实体、是否受 §5 的 Owner 授权约束，均为 `NOT_VERIFIED`。

**登记状态**：`AUTHORITY_SOURCE_UNVERIFIED`

---

## 8. 后续纠正措施（待批准，未执行）

| # | 措施 | 状态 |
|---|---|---|
| C-1 | 建立本登记文件于仓库，作为统一缺陷记录 | 本文档为候选稿，未提交 |
| C-2 | 对 20 处规范性路径变更补做追溯性独立审查 | 未开始 |
| C-3 | 在仓库配置层强制 `main` 分支保护，使无 PR 的直推在平台侧失败 | 未开始（#134 / #283 仍在跟踪） |
| C-4 | 明确 `L0-MAIN-WRITER-01` / `L0-manager` / `unknown` 的授权来源与权限边界 | 未开始 |
| C-5 | 对 `02-domain-model` 当前 main 状态做一次完整基线复核 | 未开始 |

---

## 9. 验证证据

| 证据 | 值 |
|---|---|
| main head | `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| 采样区间 | 最近 100 commits |
| via PR | 67 |
| direct | 33 |
| direct 中 verified=true | 0 / 33 |
| direct 触及规范性路径处数 | 20 |
| 数据采集脚本 | `reqs/_collect.py`（ThreadPool 6 并发，逐 commit 调 `/commits/{sha}/pulls`） |
| 原始数据 | `reqs/_direct100.json`（33 条）、`reqs/_direct_full.json`（33 条含 files） |

---

## 10. 明确未做的事

- 未 revert 任何 commit。
- 未对任何作者作出个人责任判断。
- 未认定 33 个 commit 的内容技术错误。
- 未修改仓库任何文件。

上述四项均超出本登记范围。

---

# 11. 第二轮增量复检（2026-11-20T16:50Z）

§1–§10 的 33 个样本是第一轮在 `main @ 0b6cebdfa2` 的观测事实，不改写。本节追加第二轮复检。

## 11.1 触发与范围

第一轮登记完成后，`main` 继续推进。复检区间：

| 项目 | 值 |
|---|---|
| 起点 | `0b6cebdfa288df33406779f356c8e409ad0b4049`（第一轮复检基准） |
| 终点 | `a7d12fe9835d8f53403946ab08c1cae8c3f12fbf`（本轮 main head） |
| 区间 commit 数 | **49** |
| 其中经 PR | **37** |
| 其中直推 | **12** |
| 采集方式 | 对 49 个 SHA 逐个调用 `GET /commits/{sha}/pulls`，失败重试 3 次 |
| 原始数据 | `reqs/_delta.json` |

**累计口径**：两个区间不重叠，`main` 历史整体缺陷规模为 **33 + 12 = 45 个直推 commit**。

## 11.2 新增的 12 个直推 commit

| SHA | 时间 | 作者 | verified | 消息 |
|---|---|---|---|---|
| `22451b9cd3` | 14:39:42Z | L0-manager | false | AID-2026-014 R4 correction: root phase-1 freeze Claim identity sync |
| `7f3707e0ef` | 14:39:42Z | L0-manager | false | AID-2026-014 R5 correction: B ordering + T17/T18 + §5 admission retiming |
| `d8fdf54f40` | 15:15:36Z | oahcom | false | docs(work-items): record AID-2026-029 merge and closeout evidence |
| `e6a7a544c4` | 15:18:44Z | oahcom | false | docs(work-items): finalize AID-2026-029 acceptance and Issue #264 closure |
| `5f0f7a095b` | 15:24:39Z | oahcom | false | test(REQ-09): add Forget-safe backup restore fence reference |
| `39b25a3fd5` | 15:26:14Z | oahcom | false | test(req-07): add AC-5 Forget recovery contract tests (#347) |
| `568b847ce3` | 15:26:24Z | oahcom | false | docs(REQ-11): record development-baseline scope disposition (ZH) |
| `0cc5ad5b75` | 15:28:37Z | oahcom | false | test(req-07): fix reference model loader for AC-5 recovery suite (#347) |
| `dcfd1bd7a3` | 15:31:41Z | oahcom | false | docs(req06): record evidence-calibrated quality and efficiency thresholds |
| `fc17542de7` | 15:40:46Z | oahcom | false | AID-2026-014 R5 correction: §14.5 subordinate to §13.3 canonical source |
| `4aad69941c` | 15:43:00Z | oahcom | false | AID-2026-014 R5 correction: sync status table, G §13.3 applied, Storage §8 |
| `a7d12fe983` | 16:10:51Z | oahcom | false | Refresh fixture report from final local harness execution |

第二轮作者构成：`oahcom` 10、`L0-manager` 2。`verified=true` 为 **0 / 12**。累计 45 个直推中 `verified=true` 为 **0 / 45**。

## 11.3 性质升级一：绕过被书面合理化

第一轮的 33 个直推没有给出理由。第二轮出现了明确的**违规定性说明**——把直推 `main` 描述成遵守规范所必需：

**Issue #347 关闭评论原文**（carrier 段）：

> Additional AC-5 test artifact committed directly to `main` **to preserve the one-PR-per-Issue rule**

**Issue #349 关闭评论原文**（carrier 段）：

> Per the **no-second-PR rule**, no duplicate PR was opened. The follow-on implementation was committed directly to `main` at `5f0f7a095be1…` (this is a direct main commit, **not** a PR merge commit).

`PR-GOVERNANCE-001` §3 的措辞是无条件的：

> A pull request is mandatory **if and only if** the merge target is `main`

「一个 Issue 一个 PR」不是 §3 的例外。§3 给出的**唯一**例外是合并目标为非 `main` 分支。因此：

- 「为遵守一 Issue 一 PR 而直推 main」是**两个规则之间的错误取舍**，不是合规折衷。
- 正确做法是在既有 PR 内追加 commit 后重新通过 exact-Head 门禁，或新开 PR；两者都不需要牺牲 §3。
- 该表述使缺陷从「未察觉的流程疏漏」变为「已知规则下的主动选择」，严重度应上调。

## 11.4 性质升级二：验收裁定依赖违规载体

七个战略需求 Issue 已全部由 `oahcom` 关闭。逐条核对关闭评论引用的 main commit 是否经 PR：

| Issue | 关闭评论引用的 main commit | 该 commit 的进入方式 | 该载体在裁定中的作用 |
|---|---|---|---|
| #346 | `dcfd1bd7a305` | **直推（无 PR）** | AC5 阈值决定的唯一载体 |
| #347 | `0cc5ad5b752f` | **直推（无 PR）** | AC-5 测试与参考模型加载器修正 |
| #349 | `5f0f7a095be1` | **直推（无 PR）** | F-349-02 Forget-safe restore 参考实现 |
| #351 | `568b847ce39f` | **直推（无 PR）** | 中文裁定记录，PR #370 以其为 base |
| #348 | `0d33c61378e1`、`6620756d5d72` | 经 PR #362 | — |
| #350 | `010edea0f0a3` | 经 PR #355 | — |
| #345 | `8215ec57260b`、`927eadcb1a8e` | 经 PR #354 及后续 | — |

**缺陷传导链**：直推 → 无 Head 门禁 → 无 review → 无 exact-Head 检查 → 该 commit 成为验收裁定引用的证据 → 裁定结论的合规性不可追溯。

### 11.4.1 正式定性标注 `EVIDENCE_CARRIER_NONCOMPLIANT`

协调会话裁决 **P2 选项 (a)**（2026-11-20）：在本书记中标注，不强制重新提交相同内容。

| Issue | commit | 在裁定中的作用 | 进入方式 | 定性 |
|---|---|---|---|---|
| #346 | `dcfd1bd7a305` | AC5 阈值决定的唯一载体 | 直推无 PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #347 | `0cc5ad5b752f` | AC-5 测试与参考模型加载器修正 | 直推无 PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #349 | `5f0f7a095be1` | F-349-02 Forget-safe restore 参考实现 | 直推无 PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #351 | `568b847ce39f` | 中文裁定记录，PR #370 以其为 base | 直推无 PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |

**定性含义**：该 commit 从未经过 exact-Head 检查或 review 门禁，因为不存在可供这些门禁适用的 PR。这不改变 commit 的内容，只改变该 commit 可被引作何种证明。

**未予采纳的选项 (b)**（要求补一次合规载体重复提交相同内容）：理由是不能追溯性地改变原始 commit 的进入方式；重复提交只为制造形式上的第二次合规记录。若确需补充验证，应提交独立的复现报告或纠正变更，且该补充 PR 的合并**不得**被描述为原始 commit 已通过 PR 门禁。

**Issue 原有 `closed` 状态不因此自动改变。**

### 11.4.2 七项关闭裁定的追溯标注已执行

同日按裁决 **P1 选项 (a)**，向 `#345`–`#351` 各发布一条 `AUTHORITY_SELF_ISSUED_DISPUTED` 标注评论：

| Issue | 标注评论 ID | 字节数 | 附带标注 |
|---|---|---:|---|
| #345 | `7045697997` | 2491 | — |
| #346 | `7045698917` | 3278 | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #347 | `7045699653` | 4838 | `EVIDENCE_CARRIER_NONCOMPLIANT` + `NOT_VERIFIED_AT_REPOSITORY_SCOPE` |
| #348 | `7045700373` | 2491 | — |
| #349 | `7045701128` | 4560 | `EVIDENCE_CARRIER_NONCOMPLIANT` + `NOT_VERIFIED_AT_REPOSITORY_SCOPE` |
| #350 | `7045702110` | 2491 | — |
| #351 | `7045702894` | 3294 | `EVIDENCE_CARRIER_NONCOMPLIANT` |

标注正文明确声明五项不作为：不证明授权伪造、不证明同一账号即同一自然人、不否定技术交付、不撤销关闭、不认定任何 AC 判断错误。

`#351` 的路径尤其值得单独记录。其自述为：

> 该中文文件由 commit `568b847ce3…` 先行写入 `main`；PR #370 随后以该 main 版本为 base，合并英文正式记录。

即：中文记录先直推落地（不触发 PR body 的 `BILINGUAL-MANIFEST` 检查），再用 PR 补英文。双语配对在形式上成立，但中文侧从未经过 PR 门禁审核。这是用直推规避双语门禁的可复现手法。

## 11.5 性质升级三：测试执行环境不等于仓库状态

`#347` 关闭评论自述：

> The local environment could not resolve `raw.githubusercontent.com` (DNS failure), so a full repository checkout was unavailable. The test file was executed from a local mirror against the exact relevant class/method excerpt copied from the pinned reference-model Blob above; this is explicitly not a full-checkout run.

含义：`Ran 6 tests / OK` 这一结果，是对**从 Blob 手工摘录的类/方法片段**运行的，不是对 `0cc5ad5b75` 所提交文件的真实导入运行。

- 该测试**未被证明**能针对 repository 的真实模块图导入成功（缺依赖、缺包路径、缺 `__init__` 都可能使真实运行失败）。
- 评论已如实声明「not a full-checkout run」，这一点不构成虚假陈述。
- 但关闭裁定把 `Ran 6 tests / OK` 列为 AC-5 的证据。按任务书「CI 未跑不得当测试通过」的同一法理，**片段级运行不得当提交级验证**。

登记结论：`#347` AC-5 的测试状态应为 `NOT_VERIFIED_AT_REPOSITORY_SCOPE`，而非「已通过」。

同理 `#349` 的执行路径为 `python3 /tmp/forget_safe_restore_reference.py`——从 `/tmp` 运行，非从仓库工作树运行。

### 11.5.1 裁决结果：状态阶梯正式采用

协调会话裁决 **P3**（2026-11-20）统一批准 `NOT_VERIFIED_AT_REPOSITORY_SCOPE`，并确立四态语义：

| 状态 | 含义 |
|---|---|
| `DELIVERED` | 交付物存在于 `main` |
| `LOCALLY_EXECUTED` | 在某一局部环境执行成功 |
| `NOT_VERIFIED_AT_REPOSITORY_SCOPE` | 未证明在仓库范围内有效 |
| `VERIFIED_AT_REPOSITORY_SCOPE` | 已提供仓库范围的验证证据 |

裁定要点：`#347` 的 `Ran 6 tests / OK` 只能证明被摘录的片段在局部环境下运行成功；不能证明仓库模块可正确导入、依赖完整、提交文件可在仓库环境执行。`#349` 从 `/tmp` 执行同理。

**关键法理**：局部测试成功 ≠ 仓库范围验证成功。两项的当前状态均为 `LOCALLY_EXECUTED` + `NOT_VERIFIED_AT_REPOSITORY_SCOPE`；`DELIVERED` 与 `LOCALLY_EXECUTED` 不予撤回，被撤回的是「从局部执行推出仓库级通过」这一推论。

这一区分与任务书「CI 未跑不得当测试通过」同源：拒绝以局部证据替代完整验证。

已按此裁决在 `#347`、`#349` 发布标注评论。

## 11.6 关联发现：双语文档门禁白名单与真实树 7/15 错配

`scripts/check_bilingual_docs.py` 的 `NORMATIVE_ROOTS` 与 `main` 实际顶层目录不符：

| 白名单条目 | main 树中是否存在 | 文件数 |
|---|---|---|
| `00-governance` | 是 | 13 |
| `01-system-architecture` | 是 | 7 |
| `02-domain-model` | 是 | 10 |
| `03-memory-brain` | **否** | 0 |
| `04-memory-compiler` | 是 | 2 |
| `05-memory-runtime` | **否** | 0 |
| `06-memory-context` | 是 | 21 |
| `07-agent-integration` | 是 | 4 |
| `08-protocols` | **否**（实际名为 `08-bmcp-protocol`） | 0 |
| `09-storage-and-index` | **否** | 0 |
| `10-security-and-governance` | **否** | 0 |
| `11-consistency-and-recovery` | **否** | 0 |
| `12-testing-and-acceptance` | **否** | 0 |
| `13-engineering-decisions` | 是 | 60 |
| `14-ai-development` | 是 | 157 |

命中 **8 / 15**。main 树中真实存在 9 个编号目录，其中 **`08-bmcp-protocol`（4 个 `.md`）完全不在白名单**——该目录下的规范性变更不触发双语门禁。

失效方向是**静默放行**，不是误报：脚本对不在白名单的路径直接 `continue`，无告警、无审计记录。

**已立 Issue**：[#384](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/384) — Bilingual documentation gate whitelist does not match the repository tree，含 AC-1~AC-10，其中 AC-5 为「中文先直推、英文后补 PR 不得判为双语合规」的负向测试，直接覆盖 `#351` 的实测绕过路径。

## 11.7 关联发现：编号域存在 5 个「幽灵号」

对 main 与全部 346 个分支做 `AID-2026-(\d{3})` 正则扫描：

| 编号 | 分支引用数 | 是否进入 main |
|---|---:|---|
| `AID-2026-007` | 1`（`ai/AID-2026-007/reqtrace-spec`）` | **否** |
| `AID-2026-010` | 5 | **否** |
| `AID-2026-012` | 5 | **否** |
| `AID-2026-013` | 5 | **否** |
| `AID-2026-015` | 1`（`ai/AID-2026-011/IO-execution-first-baseline`）` | **否** |

main 上已登记的编号为 `001–006, 008, 009, 011, 014, 023–026, 029, 030`。`007/010/012/013/015` 在分支上被引用但从未进入 main，`14-ai-development/work-items/INDEX.md` 无对应条目。

后果：编号唯一性判定若只看 main，会把 007/010/012/013/015 误判为可用，造成二次占用。全域真正空闲的编号为 **016–022、027、028、031 及以上**。

## 11.8 §7 授权主体结论的变化

第一轮登记为 `AUTHORITY_SOURCE_UNVERIFIED` 的 `L0-manager <l0@local>`，在第二轮又直推 **2 个** commit（`22451b9cd3`、`7f3707e0ef`，同一秒时间戳），仍未在仓库中找到任命文件。

Issue #305 在 2026-11-20T14:46Z 发布了一份 `OWNER DELEGATION INSTRUMENT`，但该文书：只建立 `acceptance_authority`，**不涉及** `Sponsor` / `accountable_owner` 的任命；且发布者与被任命者同为 `oahcom`。详见 `GOV-NC-2026-11-20-SELF-AUTH-002.md`。

因此本登记的 §7 结论维持不变，并补充：`L0-manager` 的授权来源仍为 `NOT_VERIFIED`，且该身份在授权书发布后继续直推。

## 11.9 更新后的验证证据

| 证据 | 值 |
|---|---|
| 第一轮 main head | `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| 本轮 main head | `a7d12fe9835d8f53403946ab08c1cae8c3f12fbf` |
| 累计直推 commit | **45**（33 + 12） |
| 累计 `verified=true` | **0 / 45** |
| 受影响的验收裁定 | 4 个（#346 / #347 / #349 / #351） |
| 双语门禁白名单命中率 | 8 / 15 |
| 编号域幽灵号 | 5（007/010/012/013/015） |
| 分支总数 | 346 |
| main blob 总数 | 803 |
| 原始数据 | `reqs/_delta.json`、`reqs/_scan2.json`、`reqs/_clos.json`、`reqs/_mainpaths.json` |
| 复检脚本 | `reqs/_recheck.py`、`reqs/_scan2.py`、`reqs/_xref.py` |

## 11.10 本轮明确未做的事

- 未 revert 任何 commit，未修改仓库任何文件。
- 未对 `#345`–`#351` 的关闭动作做撤销或重开。
- 未认定七份关闭评论中的技术结论错误——本登记只质疑**证据载体的合规性**，不质疑结论的技术内容。
- 未对 `oahcom` 账号背后是否为同一自然人作出判断。

---

## 12. 第三轮复检（2026-11-21 03:00Z）

### 12.1 规模变化：45 → 53

在 `c099816f19e1`（PR #390 合并点）之后的两次 main 推进中，又出现 8 个无 PR 的直推 commit。

| 区间 | 直推 commit | 作者 |
|---|---:|---|
| `c099816f...ee9b3031` | 1 | `L0-manager <l0@local>` |
| `ee9b3031...1a0dc911` | 7 | `unknown <1491856051>` × 4，`oahcom` × 3 |
| **本轮新增** | **8** | |
| **累计** | **53** | |

第三轮新增清单：

| commit | 时间（Z） | 作者 email | 消息 |
|---|---|---|---|
| `ae5a886fa0` | 18:02:27 | `l0@local` | AID-2026-014 R3 correction: root freeze identity exclusion |
| `0c73f639bf` | 17:35:49 | `1491856051` | docs(governance): add GOV-DOC-002 document management |
| `7d76c589bc` | 17:45:56 | `1491856051` | docs(governance): pair bilingual mirrors for GOV-DOC |
| `965a66b9a9` | 17:57:00 | `1491856051` | docs(governance): normalise work-items links on both |
| `e2644784c0` | 18:25:24 | `1491856051` | docs(governance): register GOV-DOC-002 sources as single-file bilingual |
| `25c6128321` | 19:05:13 | `oahcom` | AID-2026-014 R5 correction: restore ZH status counterpart |
| `8b9cb11985` | 19:09:10 | `oahcom` | AID-2026-014 R5 correction: Storage §8.8 applied on both sides |
| `1a0dc911a9` | 19:15:14 | `oahcom` | AID-2026-014 R5 correction: add bilingual read-back |

### 12.2 新出现的性质：三类身份并行直推

第三轮新增的 8 个直推 commit 分属三个身份：

- `l0@local` — 已在 §7 记为 `AUTHORITY_SOURCE_UNVERIFIED`，第三轮继续直推。
- `1491856051` — email 无 `@`，不是合法邮箱。第一轮只出现 1 次（`bc114263d7` 同批），本轮一次出现 4 次，且全部是**双语文档治理**提交。
- `oahcom` — 3 次，全部是 `AID-2026-014 R5 correction` 系列。

其中 `1491856051` 的 4 个 commit 值得单独指出：它们的消息本身讲的是「pair bilingual mirrors」「register ... as single-file bilingual」「normalise work-items links on both」，即**内容是关于双语配对的治理，而投递方式是没有 PR 体、无法携带 `BILINGUAL-MANIFEST` 声明的直推**。门禁对直推没有可检查对象，因此这 4 个 commit 绕过的正是它们所描述的那道门禁。

这不是推断，是机制事实：`check_bilingual_docs.py` 读取 `PR_BODY` 环境变量；直推不产生 PR，CI 不触发，`PR_BODY` 为空。

### 12.3 `1491856051` 身份的验证状态

**口径校正**：上一轮我记为「累计 5」，那是**仅统计直推**的口径。全量统计如下。

| 项目 | 值 |
|---|---|
| main 上该 email 的 commit 总数 | **20** |
| 其中无 PR（直推） | **5** |
| 其中经 PR 进入 | **15**（PR #279/#285/#286/#287/#288/#298/#299/#301/#302/#303/#304） |
| 首次出现 | 2026-11-19T15:38:12Z（`33302f40e7`，via PR #279） |
| email 格式合法性 | 否（无 `@`，`git config user.email` 缺失产物） |
| GitHub 账号归属 | 无。GitHub API 的 `commit.author` 恒为 `null` |
| 授权来源 | `NOT_VERIFIED` |

5 个直推全部发生在 2026-11-20（13:40–18:25Z）：

| commit | 时间（Z） | 消息 |
|---|---|---|
| `927eadcb1a` | 13:40:07 | docs: 架构文档治理 - 建立清晰层次结构 |
| `0c73f639bf` | 17:35:49 | docs(governance): add GOV-DOC-002 document management policy |
| `7d76c589bc` | 17:45:56 | docs(governance): pair bilingual mirrors for GOV-DOC-002 |
| `965a66b9a9` | 17:57:00 | docs(governance): normalise work-items links on both languages |
| `e2644784c0` | 18:25:24 | docs(governance): register GOV-DOC-002 sources as single-file bilingual |

`git commit` 使用无法解析的 email 时，GitHub 不建立 commit 与账号的关联。后果是：**这 20 个 commit 在 GitHub UI 上全部不显示作者头像与链接，无法通过账号维度审计**，无论它走的是 PR 还是直推。这是可规避审计的最小成本手段，无论使用者的意图如何。

需要注意：该身份**曾经正常走 PR 流程**（15 次）。因此「它不能走 PR」不成立。5 次直推是选择，不是能力限制。

### 12.4 与 #384 关闭的关系

`e2644784c0`（`1491856051`，18:25:24）的时间点值得单独记录：它比 #384 的关闭时间（18:25:06）晚 **18 秒**，比 PR #394 的合并时间（18:25:04）晚 **20 秒**。

该 commit 的内容不是文档，而是**再次修改门禁脚本本身**：

```
commit e2644784c010da488b4794f3e6b10d17c32e9b4b
     modified scripts/check_bilingual_docs.py +3/-0

@@ -40,6 +40,9 @@
+    "14-ai-development/ai-development-standard.md",
+    # GOV-DOC-002 requires the policy to be bilingual in a single file so that
+    # the policy and its metadata schema cannot drift apart between languages.
     "00-governance/architecture-document-management-policy.md",
```

即向 `EMBEDDED_BILINGUAL_SOURCES`（配对豁免白名单）追加一项。

三点后果：

1. **豁免白名单本身可以由直推扩大**。`EMBEDDED_BILINGUAL_SOURCES` 是「该文件不需要配对」的唯一开关。它可以被一个没有 PR、没有 `PR_BODY`、没有审查的 commit 追加成员。这意味着 Issue #384 试图修复的「覆盖不全」，可以从另一侧——豁免方向——继续扩大。
2. **同一个 Issue 的门禁，在关闭后 18 秒被无 PR 修改**。修复 #384 的 PR #394 改的是 `NORMATIVE_ROOTS`；18 秒后的 `e2644784c0` 改的是 `EMBEDDED_BILINGUAL_SOURCES`。两者是同一文件的两套豁免机制，后者未在 #384 的 AC 中被约束。
3. **修改者仍是 `1491856051`**，无法映射到 GitHub 账号。

对 `14-ai-development/ai-development-standard.md` 本身的实测（`main`，`sha=...`，40409 字节，CJK 3572 字符 / Latin 28321 字符）显示该文件确实同时含中英内容，因此 GOV-DOC-002 的单文件中英并存要求**可能是合理的**。本登记不质疑该豁免的技术理由，只记录**授予该豁免的方式**：无 PR、无声明、无审查、无法归属账号。

### 12.4.1 由此产生的登记条目

| 编号 | 内容 | 状态 |
|---|---|---|
| `EMBEDDED-EXEMPT-VIA-DIRECT-PUSH` | `EMBEDDED_BILINGUAL_SOURCES` 可被直推扩大，构成第二类旁路 | `OPEN` |

### 12.5 更新后的验证证据

| 证据 | 值 |
|---|---|
| 第三轮 main head | `1a0dc911a9e3779c975f570a7996f980ffb98e9c` |
| 累计直推 commit | **53**（33 + 12 + 8） |
| 累计 `verified=true` | **0 / 53** |
| 第三轮新增直推 | 8（3 个身份） |
| `1491856051` 累计 | 5 |
| main blob 总数 | 826 |
| 原始数据 | `reqs/_delta.json`、`reqs/_delta2.json`、`reqs/_delta3.json` |
| 复检脚本 | `reqs/_recheck.py`、`reqs/_merge_ev.json` |

---

**登记状态更新**：`OPEN` / `NOT_REMEDIATED` / **规模 53** / **性质由「流程疏漏」升级为「已知规则下的主动选择并书面合理化」**，第三轮追加：**在多身份并行下持续，并出现无法归属账号的提交身份**
