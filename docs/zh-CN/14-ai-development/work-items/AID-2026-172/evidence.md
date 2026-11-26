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
        - "14-ai-development/work-items/AID-2026-172/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "记录两份基线的一致性比较、只许缩小的写入拒绝与新增单元测试；在 PR 运行前不声称任何 CI 结果。"
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
    canonical_scope: "AID-2026-172 bilingual baseline copy consistency check and shrink-only baseline write assertion"
    canonical_scope_id: "ai-development/aid-2026-172-bilingual-baseline-copy-consistency"
    canonical_scope_keywords:
      - bilingual-baseline
      - baseline-drift
      - shrink-only
      - gate-ratchet
      - write-baseline
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-172/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-172/evidence.md"
    zh-CN: null
---
# AID-2026-172 — 两份"只许缩小"的 77 条基线缺乏一致性检查

- Work item: AID-2026-172；id_status: PROVISIONAL。
- Attribution: user-authorized operator (delegated by account owner)；date: 2026-11-26。
- base_commit_sha: `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`（建分支时的 `origin/main`）。
- 结论先行：两份基线条目集合当前相同；本变更让"它们必须相同"成为可判定的失败，并让 `--write-baseline` 真正拒绝抬高基线。
- 本记录不声称任何 CI 结果，也不声称独立评审或 Owner 接受。

## 1. 观察到的事实

仓库里存在两份**内容相同的 77 条**冻结缺口清单，语义上都是"只许缩小"：

| 文件 | 读取方 | 读取方式 |
|---|---|---|
| `scripts/bilingual-baseline.txt` | `scripts/check_bilingual_docs.py`（job：GOV-DOC-001 structural checks） | `read_baseline()`，以集合与 `current_bilingual_gaps()` 做双向差集 |
| `scripts/ci/baselines/bilingual-docs.txt` | `scripts/ci/gate_ratchet.py`（job：Bilingual docs coverage (ratchet)） | `read_baseline()`，与 `check_bilingual_docs_full.py` 的输出集合比对 |

- 前者带 3 行注释头，后者无注释头；去掉 `#` 注释与空行后，两者条目集合逐条相同（77 条）。
- **没有任何检查器比较这两份文件。** 单独重新生成其中一份，另一份保持不变，于是同一份"冻结清单"在两处给出不同答案，而两道门各自只读自己那一份。
- `write_baseline()` 只校验工作树干净（`git status --porcelain --untracked-files=all`），**不校验新集合是旧集合的子集**。
- `check_bilingual_docs.py` 里 `"This baseline may only shrink; entries must never be added."` 只是写入文件头部的**注释字符串**，没有任何代码执行它；因此一次重新生成就能把新增缺口写进基线而不被拦截。

## 2. 变更内容

改动集中在既有的 bilingual 结构门与其自测，不新增 job、不新增 required context。

1. `scripts/check_bilingual_docs.py`
   - 新增 `CI_BASELINE_PATH`：指向 `scripts/ci/baselines/bilingual-docs.txt`，并在注释里写明它由 `gates.yml` 的 ratchet 消费。
   - 抽出 `read_baseline_entries(path)`：注释行与空行不是条目，返回集合或在文件缺失时返回 `None`。
   - 新增 `check_baseline_copies_agree()`：读取两份集合，缺失一侧即失败；否则输出两个方向的差集条目。
   - `main()` 在读入主基线后调用它：任一条目只出现在一份文件里，就逐条打印 `::error::`（含文件名与该条目），再补一条汇总 `::error::`，返回 2。
   - `write_baseline()` 在写入前读取**旧**集合：
     - 旧基线缺失 → 拒绝写入（无法证明"只缩小"），返回 2；
     - 新集合含旧集合之外的条目 → 拒绝写入，逐条打印 `+ <path>`，返回 2，且不创建临时文件、不 `os.replace`；
     - 子集（含相等）→ 照旧写入。
2. `scripts/test_check_bilingual_docs.py`
   - `run_gate()` 现在同时写出 ratchet 副本，并支持 `ratchet_baseline` 参数制造漂移。
   - 新增 5 个一致性用例：两副本相同通过、条目仅在主副本、条目仅在 ratchet 副本、注释与空行不算条目、ratchet 副本缺失即失败。
   - 新增 3 个写入用例：新增条目被拒且文件未变、收缩集正常写入、旧基线缺失被拒。

## 3. 为什么这是"防止静默漂移"，而不是"新增门槛"

- **通过条件未改变。** 两份集合当前相等，因此在本变更前后，同样的仓库状态下所有既有门禁给出同样的判定；新增的只是"两份不一致就红"这一条，而它在 main 上恒为真。
- **没有新增 required context。** 检查挂在 `GOV-DOC-001 structural checks` 内部执行，workflow 未改动；`Bilingual docs coverage (ratchet)` 的输入文件与 `gate_ratchet.py` 的语义都未触碰。
- **不改任何现有判定语义。** `current_bilingual_gaps()`、两份基线的内容、`gate_ratchet.py` 的回归/失效判定全部保持原样。
- **防的是静默漂移。** 漂移发生时，两道门会继续各自通过，而"冻结清单"实际上已经有两份不同答案；这正是本检查要变成失败的那种状态。
- **把注释变成断言。** `--write-baseline` 原本是"唯一能抬基线"的路径，且没有任何阻挡；现在它只能在旧集合之内收缩。

## 4. 本地验证与边界

本地执行（Windows，Python 3，工作副本基于 `8722a37b`）：

| 命令 | 结果 |
|---|---|
| `python scripts/test_check_bilingual_docs.py` | 15 tests OK（原有 7 + 新增 8） |
| `python scripts/check_bilingual_docs.py`（BASE=origin/main, HEAD=分支） | 通过，未报告新增或已修复缺口 |
| `python scripts/ci/test_gate_ratchet.py` | 通过（未改动该脚本） |

边界：

- 不修改两份基线的任何条目，不重新生成基线。
- 不把两份文件合并为一份：结构门与 ratchet 有意各读一份，合并会改变 `gate_ratchet.py` 的接入方式。
- 不声称 CI 绿：16 项 required contexts 由 PR 运行产生。

## 5. 未做事项

- 未关闭或修改任何 Issue。
- 未改分支保护、未改 workflow。
- 未做独立评审；`review.status = NOT_ASSIGNED`。
