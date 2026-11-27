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
        - "14-ai-development/work-items/AID-2026-240/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "本文所有数字均由本 worktree 在基线 951051313b6cac60b1a3acb069e08de6c5e796c0 上实跑得出：清单通过导入检查器并逐个读取候选文件枚举，比较器在扩围前后各跑一次，两套单元测试与棘轮均在本地执行。不声称任何 CI 结果、合并 SHA 或合并后 blob。"
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
    canonical_scope: "AID-2026-240 指定 scripts/ci/baselines/bilingual-docs.txt 为 77 条冻结双语清单的唯一权威，并扩围副本比较器、为 81 条审查快照加历史标注"
    canonical_scope_id: "ai-development/aid-2026-240-frozen-inventory-single-authority"
    canonical_scope_keywords:
      - "bilingual"
      - "baseline"
      - "frozen-inventory"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-240/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-240/evidence.md"
    zh-CN: null
---

# AID-2026-240 —— 让 77 条冻结清单只有一个权威

## 1. 本记录声称什么

77 条冻结双语清单此前由七个文件承载，AID-2026-172 只比较了其中两个。一份副本已漂到 81 条，
而树里没有任何一处变红。本记录陈述四件事：

1. 七份承载件的实测枚举，含行数以及与权威副本的逐条结论；
2. 指定 `scripts/ci/baselines/bilingual-docs.txt` 为唯一权威；
3. 扩围后的 `check_baseline_copies_agree()`：按声明角色覆盖全部副本，未声明的副本一律判红；
4. 为漂移的 81 条快照加历史标注，并修正两处引用 `baseline=81` 的指南段落。

本记录不声称 77 条缺口可以接受，不声称任何门禁结果来自 CI，也不声称分支已合并。

## 2. 七份承载件（实测）

枚举方法：读取全部受 Git 跟踪的文件，用 `inventory_entries_in()` 识别四种条目形态（裸路径行、
带编号的表格行、JSON 字符串行、列表项），保留命中至少一半权威条目的文件。恰好七个文件达到阈值。

| # | 路径 | 行数 | 清单条目 | 角色 | 与权威副本的结论 |
|---|---|---:|---:|---|---|
| 1 | `scripts/ci/baselines/bilingual-docs.txt` | 77 | 77 | 权威 | 与自身一致；唯一门禁输入 |
| 2 | `scripts/bilingual-baseline.txt` | 80 | 77 | 活副本 | 条目集合完全相同（77/77，双向皆 0） |
| 3 | `14-ai-development/governance-register/evidence/main-paths.json` | 805 | 803 | 超集登记表 | 包含全部 77 条；其余 726 行不是清单条目 |
| 4 | `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` | 96 | 83 | 带日期快照 | 共同 72、多 11、缺 5 —— `568b847c` 上的 83 条扫描 |
| 5 | `reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md` | 737 | 分类表内 81 | 历史快照 | 共同 73、多 8、缺 4 |
| 6 | `reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md` | 737 | 分类表内 81 | 历史快照 | 与 #5 相同的漂移 |
| 7 | `14-ai-development/work-items/FIX-2026-P1-T3/tier-confirmation-proposal.yaml` | 2452 | 0 | 仅散文 | 以散文提到 77 条中的 62 条；无列表块，不是副本 |

上述数字为加标注**前**的实测：第 5、6 份当时各 735 行且无标注；表中的行与条目本身未被改动。

派发前提「多 9 / 缺 5」不复现。对照权威副本，81 条表多出 **8** 条、缺失 **4** 条：
73 + 8 = 81 = 77 − 4。前提的算式自洽，两个操作数不自洽；本记录采用实测的那一对。

## 3. 唯一权威

`scripts/ci/baselines/bilingual-docs.txt`（77 行、77 条）之所以是权威，是因为
`.github/workflows/gates.yml` 的 `bilingual` job 把这个文件喂给 `scripts/ci/gate_ratchet.py`。
没有任何门禁读取的文件，不能定义一个门禁允许什么。`scripts/bilingual-baseline.txt` 仍是
`check_bilingual_docs.py` 的门禁输入，因此它是必须与权威相等的**活副本**，不是第二份定义。

## 4. 扩围后的比较器

`check_baseline_copies_agree()` 现在读取声明式登记表 `BASELINE_COPIES`，按角色套用唯一一条规则：

| 角色 | 规则 | 失败形式 |
|---|---|---|
| `authority` | 即权威 | — |
| `live` | 条目集合等于权威 | 每条差异一个 `::error::`，双向 |
| `superset` | 包含全部权威条目 | 每条缺失一个 `::error::` |
| `snapshot` | 声明取样时的 40 位源版本 | 声明消失即 `::error::` |
| `historical` | 携带 `HISTORICAL — not a gate input` | 标注消失即 `::error::`；实测漂移仅 `::notice::` |

在声明集合之外，另有一趟发现：遍历 `git ls-files`，任何其他受跟踪文件只要命中至少一半权威条目，
未标注就是 `::error::`，已标注就是提示。声明了但树中不存在的副本会被跳过 —— 不存在的文件不可能
与任何东西不一致，这也正是该检查能在只含两份基线的测试夹具上继续可用的原因。

在本 head 上实测：

```
扩围前: check_baseline_copies_agree() -> 0 errors, 0 notices   （比较 2 份）
扩围后: check_baseline_copies_agree() -> 0 errors, 2 notices   （比较 6 份 + 发现趟）
```

两条提示就是两个历史快照，它们报告的正是标注里写的内容：该审查快照全文件共列出 27 条权威副本
没有的清单形态条目，且权威的 4 条在其中完全不存在。它们之所以只是提示，是因为已标注的快照不是
门禁输入；一旦移除任一标注，同一个函数就会返回 `::error::`。

## 5. 漂移快照与 81 的两处引用

内容未改。`BMCP-ARCH-001.en.md` 与 `.zh-CN.md` 各加了一个标题前缀和一行引用块：

```
### HISTORICAL — not a gate input: path-by-path classification of the 81 frozen GOV-DOC-001 findings
```

其下的表格逐字节保持原样；两份文件从 735 行变为 737 行。
`00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` **未**改动：它本身已声明
`Source revision / 扫描源 Commit` 及 40 位版本号，正是 `snapshot` 规则要求的形态，改它反而会
迫使一份它并不需要的双语例外。

`14-ai-development/ci-gates-and-ratchets.en.md` 与 `.zh-CN.md` 各有三处更新：基线表指出唯一权威，
并说明 `81` 是历史审查快照的条目数；两行实测（`baseline=81 current=81`、`81 uncovered paths`）
补上了这些数字所属的日期。数字本身保持实测原样 —— 那是 2026-11-22 的记录，改写它等于伪造记录。

## 6. 测试

`scripts/test_check_bilingual_docs.py` 新增 `BaselineCopyRegistryTests`（10 例）：

| 用例 | 锁定什么 |
|---|---|
| `test_registry_declares_every_role` | 恰好一个 `authority`，且它就是棘轮基线 |
| `test_all_declared_copies_agreeing_passes` | 各角色一致 → `[]`，无 `::error::` |
| `test_historical_snapshot_without_marker_fails` | 漂移文件在标注前判红 |
| `test_historical_snapshot_drift_is_a_notice_not_an_error` | 已标注且漂移 → `[]` 加一条提示 |
| `test_register_missing_a_frozen_entry_fails` | 登记表必须包含每一条 |
| `test_snapshot_without_revision_declaration_fails` | 扫描记录丢失版本声明即判红 |
| `test_undeclared_copy_of_the_inventory_fails` | 无人声明的新副本即使大体一致也判红 |
| `test_marked_undeclared_snapshot_is_a_notice` | 已标注 → 提示而非错误 |
| `test_this_repository_has_no_undeclared_inventory_copy` | 本 head 上声明集合即全集 |
| `test_entry_shapes_are_read_from_every_copy_format` | 四种条目形态都能读出 |

```
python -m unittest discover -s scripts -p "test_check_bilingual*"   -> Ran 25 tests, OK   （原 15）
python -m unittest discover -s tests   -p "test_check_bilingual*"   -> Ran 7 tests, OK
```

## 7. 本地门禁运行

```
python scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
  --format paths --command "python scripts/check_bilingual_docs_full.py"
  -> ratchet: baseline=77 current=77 regressions=0 fixed=0
  -> ratchet: PASS - failure set matches the baseline exactly.          exit 0

python scripts/check_bilingual_docs_full.py
  -> 77 violations                                                        exit 1

python scripts/check_bilingual_docs.py   （BASE_SHA=origin/main，HEAD_SHA=PR head）
  -> bilingual baseline: 77 frozen, 0 new gaps
  -> PASS                                                               exit 0
```

## 8. 没有做什么

- 任何副本的条目都未增删或重排。权威与活副本与 `4326669c` 上的字节完全一致；两份审查快照
  只变了 §5 点名的两行。
- 两份基线都没有重新生成，`current_bilingual_gaps()` 未改。
- `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` 与 `main-paths.json` 未编辑。
- 未改任何 workflow、分支保护设置、required context 或 Issue。
- 本记录不声称任何 CI 结果、合并 SHA 或合并后 blob。
