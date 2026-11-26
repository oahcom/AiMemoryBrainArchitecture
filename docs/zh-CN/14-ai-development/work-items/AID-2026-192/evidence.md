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
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-192/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "计数由命令在 4326669c 的树上重新导出而非断言；AID-2026-111 的行清单由其自身单元格重新清点；AID-2026-112 的溯源主张逐行对比 AID-2026-111 第 2.3 节。未改动、未重跑任何历史判定、blob pin 或测试结果。"
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
    source: "14-ai-development/work-items/AID-2026-192/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-192/evidence.md"
    zh-CN: null
---

# AID-2026-192 — 治理记录中的过期计数与一处继承假设

## 范围与署名

- 仓库：`oahcom/AiMemoryBrainArchitecture`；基线 `main` 为
  `4326669caa6c43193d34219a0451b80762b712ff`（分支自此切出）。
- 分支：`fix/2026-11-27-stale-counts-and-claims`；登记编号 `AID-2026-192`
  （原为 190，因 PR #1343 合并了 190、PR #1345 占用 191 而重编）。
- 署名：user-authorized operator（由账户所有者委托）。不声称自然人 Owner 签署、验收或批准，也不关闭任何 Issue。
- 本单元修改四份文档及其两侧镜像，新增本登记集与一行 `INDEX.md`。不改代码、不改 workflow、不改 checker、不改登记表、不改任何历史判定。

## 1. 错在哪里

三处表述无法从它们所描述的树上复现。

| # | 位置 | 记录值 | 可复现值 |
|---|---|---|---|
| 1 | `docs/governance/documentation-gaps.md` GAP-03 | "26 of its files are architecture documents"、"`reviews/` (196 Markdown files …)" | 27 与 198 |
| 2 | `AID-2026-111/evidence.md` §1 合计行 | 0 PASS / **36** PARTIAL_EVIDENCE / **52** UNCHANGED | 0 / **34** / **54** |
| 3 | `AID-2026-112/evidence.md` §8 memory-context 行 | Exit `0`、Test binaries `11`、Passed / Failed `177 / 0` | AID-2026-111 §2.3 记 exit code、failed 数、test-binary 数为 `NOT_RECORDED` |

第 1 处是活文档里的过期数字：它所描述的登记表长期写着 `documents: 27`，于是文字与机器核对的声明互相矛盾。review 计数是纯测量值，差了两个文件。

第 2 处是同一张表内的加法错误。每个分项行自身自洽（23 + 49 = 72，6 + 2 = 8，5 + 3 = 8），列和为 0 / 34 / 54；合计行写 36 / 52，即合计里有两行被从 UNCHANGED 挪成 PARTIAL_EVIDENCE，而 §5–§7 中没有任何一行发生位移。

第 3 处不是加法错误，是升级：同一轮运行的另一份记录声明为 `NOT_RECORDED` 的字段，在这里以数值出现三次，并出现一个更早记录说从未采集过的 stdout 哈希。依赖它的 552 合计仍是三个 passed 计数的加法，但第三组的"0 failed"与"exit 0"没有凭据。

## 2. 改了什么

### 2.1 `docs/governance/documentation-gaps.md`（GAP-03 一行）

- `docs/` 下的架构文档 26 → **27**，同行标注 `(verified 2026-11-27 against tree 4326669c…)`，并写清计数口径：`00-governance/document-scope-registry.yaml` 中的 `backlog: docs: documents: 27` 声明，等于 `docs/**/*.md` 减去 `docs/en`、`docs/zh-CN` 与单独受治理的缺口记录。
- `reviews/` 下的 Markdown 196 → **198**，标注为同一棵树上 `reviews/**/*.md` 的递归计数。
- 其它 GAP 条目、front matter 与登记表数值均未改动。登记表本来就写 27，没有编辑它。

### 2.2 `AID-2026-111/evidence.md` —— 追加 `## Correction`

§1 的表格未动：合计行仍写作 0 / 36 / 52，作为"确实被如此记录"的取值。追加节做四件事：

1. 给出判定行清点——**88** 行（72 个 Gate A 单元、8 条 SC、8 条 HIR），并记录派发时给出的"95 行"在本文中复现不出来；
2. 把三个分项行及其列和与合计行并排列出，使差异表现为算术而不是主张；
3. 逐行列出**每个判定**：72 个 Gate A 单元排成 9 检查点 × 8 流程的表并给出按流程小计（F1 5P/4U、F2 5P/4U、F3 0P/9U、F4 6P/3U、F5 0P/9U、F6 0P/9U、F7 0P/9U、F8 7P/2U），随后逐条列出 8 条 SC（6P/2U）与 8 条 HIR（5P/3U）；
4. 结论为 **0 PASS / 34 PARTIAL_EVIDENCE / 54 UNCHANGED = 88**，并指出 AID-2026-111 自己的 `AI-visible output` 一节本就写着 34 / 54，因此合计行是唯一的偏离值。

### 2.3 `AID-2026-112/evidence.md` —— 追加 `## Provenance correction`

§8 表格、标题与全部判定未动。追加节记录：

- AID-2026-111 §2.3，同一 HEAD `a123ea4e…`、同一组：passed 177；failed 数与 exit code `NOT_RECORDED`；命令、test-binary 数、stdout 字节数、raw stdout SHA-256、逐 harness multiset 与测试名清单 `NOT_RECORDED`；normalised digest `NOT_SUPPLIED`；
- 这三个字段在本文中没有任何新捕获、命令日志、stdout 工件或哈希算法被引用，§8 的"操作者提供、本会话未重跑"说明的是谁执行，不是字段从哪来；
- `Exit code = 0`、`Failed count = 0`、`Test binaries = 11` 标为 **`INHERITED_ASSUMPTION`**；
- 同一行的 stdout SHA-256 同样无出处；按 AID-2026-111 §2.1 的口径，raw stdout 哈希只钉住一次捕获，没有捕获就不承担验证作用；
- 仍然成立的：177 有记录，552 = 99 + 276 + 177 仍作为三个 passed 计数之和成立，且不声称本记录有任何错判。

### 2.4 镜像

`docs/en/.../AID-2026-111/evidence.md`、`docs/zh-CN/.../AID-2026-111/evidence.md`、`docs/en/.../AID-2026-112/evidence.md`、`docs/zh-CN/.../AID-2026-112/evidence.md` 携带相同章节、相同标题（`## Correction`、`## Provenance correction`）与相同表格；需要翻译的镜像给出译文。`docs/governance/documentation-gaps.md` 没有镜像：`docs/governance/` 不是 `NORMATIVE_ROOT`，该文件在 `governed_files` 中单独登记，而它改动的 GAP-03 行本身只有英文，这两个数字不存在第二份副本。

## 3. 与 main 的合流核对

本 PR 打开期间，`main` 推进到 `0c752ee6`（PR #1340），向 AID-2026-111 的三份副本追加了 **§12 "memory-context capture (2026-11-27)"**：同一 HEAD `a123ea4e…`、同一命令、exit `0`、11 个 test binary、`177 / 0`，并明确写出 stdout 字节数、raw stdout SHA-256、逐 harness multiset、normalised digest 与测试名清单仍为 `NOT_RECORDED`。

这改变了本记录 §2.3 中一项主张的真值，因此合流不是机械照收：

- §12 独立印证了本记录的算术——它同样写明 0 PASS、34 PARTIAL_EVIDENCE、54 UNCHANGED——追加的 `## Correction` 现已引用这一点。
- 它**不**能替 AID-2026-112 §8 那一行自证：AID-2026-112 成文时没有捕获存在，也没有引用任何捕获。因此这三项在当时就是 `INHERITED_ASSUMPTION`，该节现在正是这样写，并把 §12 记为后到的、独立的确认，同时保持那一行的 `43b2b9b6…` stdout 哈希为 `UNSUPPORTED`——因为 §12 同样把该哈希记为从未捕获。
- 合流保留两份文本：PR #1340 写入的 §12 原样保留，`## Correction` 接在其后，两者互不改写。

## 4. 已执行的验证

以下命令均在 `D:\code\wt-counts`、基线提交上、以 `PYTHONUTF8=1` 运行。

| 检查 | 命令形态 | 结果 |
|---|---|---|
| `docs/` 下架构文档 | `.md` 递归计数，减去 `docs/en`、`docs/zh-CN` 与缺口记录 | **27**，与登记表声明一致 |
| review 记录 | `reviews/` 下 `.md` 递归计数 | **198**（改前 196） |
| AID-2026-111 行清单 | 按三个章节前缀解析行并统计加粗判定 | **88** 行 → 23/49、6/2、5/3 → **0/34/54** |
| 元数据解析 | `check_document_management` 的 `read_metadata`，对七份被改文件 | 全部 `True` |
| 行尾 | `python scripts/ci/check_line_endings.py` | 1641 个文件，**0 违规** |
| 文档管理门禁 | `python scripts/check_document_management.py` | `INCOMPLETE: no rule violations in 506 classified documents, but 446 governed documents are still unclassified`（exit 2）——即 GAP-02 记录的既有积压状态，**零规则违规** |

DM 门禁的 exit 2 是本仓库在 GAP-02 中记录的积压状态（"该扫描现在返回 INCOMPLETE (exit 2)，只要积压仍在"），不是针对本次改动的发现。

## 5. 刻意未做

- 未改任何判定：23/49 + 6/2 + 5/3 的全部单元格、72 个 flow 单元、Gate A PARTIAL / OPEN 与 Gate B PARTIAL / OPEN（NOT VERIFIED）的结论均按原样保留。
- 未重写 AID-2026-111 §1 合计行与 AID-2026-112 §8 表格；"曾经这样写"的记录被保留，订正是追加式的。
- 未改动任何 blob pin；也未运行任何测试、harness 或 workflow 去补 `NOT_RECORDED` 字段——那样等于制造出"它的缺失正是要点"的那份证据。
- AID-2026-111 的 zh-CN 镜像中 §4 表格位置错乱是既有排版缺陷，未并入本次计数与溯源改动。
- 未关闭任何 Issue，未触碰分支保护或 required context，`scripts/`、`tests/`、`.github/` 无改动。

## 6. 非主张

- 本记录不声称 AID-2026-111 或 AID-2026-112 错判了任何谓词；它订正一个合计与一个溯源等级。
- 不声称 memory-context 那次运行没有通过 177 项测试——177 有记录——只声称它的 exit code、failed 数与 harness 数没有记录。
- 不声称门禁为绿：只要积压存在，全树 DM 扫描按设计就是 INCOMPLETE。
- 不声称 Owner 验收、独立评审或 Issue 关闭。

## Session role / use case

治理记录与两份证据工作项的文档修复会话。会话读取两份 brief，按树重新导出争议计数，在不改动任何判定前提下追加两节订正，同步镜像，并把结果登记为 AID-2026-192。未修改 runtime、schema、测试、workflow 或部署。

## Actual AI input

NOT_RECORDED

派发消息未逐字保存。本目录的 `prompt-v1.md` 是事后整理的结构化任务快照，manifest 因此记 `prompt_status: NOT_RECORDED`。

## AI-visible output

在 AID-2026-111 的 canonical、EN、ZH-CN 三份中追加 `## Correction`——枚举 88 行、确立 0/34/54、把 0/36/52 原样留在原处。在 AID-2026-112 的三份中追加 `## Provenance correction`——Exit code、Failed count、Test binaries 标为 `INHERITED_ASSUMPTION`，指出无出处的 stdout 哈希，552 保留为三个 passed 计数之和。把 GAP-03 的 26/196 更正为 27/198 并附验证注记与树 SHA。新增本登记集与一行 INDEX。回报上列本地门禁结果，包括既有的 INCOMPLETE 积压状态。
