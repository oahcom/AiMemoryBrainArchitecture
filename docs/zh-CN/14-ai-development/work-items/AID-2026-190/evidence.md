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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "本文是 canonical 记录的中文版本，所有数字均来自 canonical 文件在 2026-11-27、基线 4326669caa6c43193d34219a0451b80762b712ff 的本工作树上实测：由导入 scripts/check_bilingual_docs.py 并调用 current_bilingual_gaps() 得出，由第 7 节两个测试套件的实际运行得出，由一个临时 git 仓库上的双夹具探针得出。本文不声称任何未在本地产生的 CI 结果、门禁结论或合并结果；cjk/latin 是字符计数，不是翻译质量评估。"
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
    canonical_scope: "AID-2026-190 对 side-by-side 双语判定项的测量与修复：原先「任一文件含 1 个汉字」的判据让英文源文件为一份未翻译的配对背书"
    canonical_scope_id: "ai-development/aid-2026-190-side-by-side-cjk-designated-side"
    canonical_scope_keywords:
      - "bilingual"
      - "side-by-side"
      - "cjk-predicate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-190/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-190/evidence.md"
    zh-CN: null
---

# AID-2026-190 — 英文侧的一个汉字，为一份从未翻译的配对背了书

**状态：DRAFT —— 先测量，再修复。** 派单要求是「先测量，后决定」：改判定、数代价、只有新增缺口不超过三个才实施。下面的测量结果是：按字面理解指令（「partner 必须含中文」）会产生十二个新缺口，而这十二个全部是把英文文件当成 partner 造成的误报——判据分不清方向。真正实施的是「只有配对中被指定承载中文的那个文件才能为配对背书」，其代价是**零**个新缺口。

## 1. 缺陷

`scripts/check_bilingual_docs.py` 中的 `_side_by_side_bilingual()` 原先在**任一**文件含一个汉字时就接受配对：

```python
return _has_any_chinese(source) or _has_any_chinese(partner)
```

`source` 只是扫描先走到的那个文件：对 `.zh-CN.md` 来说它是中文文件，对 `.md` 来说它是英文文件。于是「英文源里顺手写了两个汉字 + 一份逐字复制的英文 `.zh-CN.md`」就构成「双语配对」：英文侧可以替整个配对背书，本该承载译文的那个文件从未被读取。

`test_issue_469_short_translation_is_accepted`（原位于 `scripts/governance/evidence/test_gate_normative_roots.py:649`）固定的是这条测试的**形状**（短也算数），不是这个漏洞：它的 `.zh-CN.md` 夹具里确实有中文，两种读法都会通过。漏洞没有被测试覆盖，也就没有被固定住。

## 2. 测量一 — 字面规则：partner 必须含中文

按指令原样实现该规则，再在已提交的树上跑 `current_bilingual_gaps()`：

| | |
|---|---|
| 改前缺口 | **77** |
| 改后缺口 | **89** |
| 新增缺口 | **12** |
| 消失缺口 | **0** |

十二大于三，按派单自己的阈值，这一读法应当标 `DEFERRED_TO_OWNER`。十二个新增缺口，逐条列出被标记的一侧及其 partner：

| # | 新增缺口（被标记的一侧） | cjk | latin | 比值 | 其 partner | cjk | latin | 比值 |
|---:|---|---:|---:|---:|---|---:|---:|---:|
| 1 | `02-domain-model/phase-2-domain-extension.zh-CN.md` | 5135 | 9172 | 0.5599 | `02-domain-model/phase-2-domain-extension.md` | 0 | 26074 | 0.0 |
| 2 | `07-agent-integration/adapter-capability-tiers.zh-CN.md` | 3168 | 2916 | 1.0864 | `07-agent-integration/adapter-capability-tiers.md` | 0 | 11640 | 0.0 |
| 3 | `08-bmcp-protocol/protocol-index.zh-CN.md` | 2052 | 9606 | 0.2136 | `08-bmcp-protocol/protocol-index.md` | 0 | 16524 | 0.0 |
| 4 | `08-bmcp-protocol/schema-nonempty-audit.zh-CN.md` | 260510 | 485305 | 0.5368 | `08-bmcp-protocol/schema-nonempty-audit.md` | 0 | 1317582 | 0.0 |
| 5 | `14-ai-development/PR-MERGE-EVIDENCE-SUMMARY-001.zh-CN.md` | 1536 | 4767 | 0.3222 | `14-ai-development/PR-MERGE-EVIDENCE-SUMMARY-001.en.md` | 0 | 10205 | 0.0 |
| 6 | `14-ai-development/bilingual-tiering-policy.md` | 2298 | 890 | 2.5820 | `14-ai-development/bilingual-tiering-policy.en.md` | 0 | 9078 | 0.0 |
| 7 | `14-ai-development/ci-gates-and-ratchets.zh-CN.md` | 5461 | 7037 | 0.7760 | `14-ai-development/ci-gates-and-ratchets.en.md` | 0 | 22268 | 0.0 |
| 8 | `14-ai-development/evidence-tiering-policy.md` | 2206 | 3822 | 0.5772 | `14-ai-development/evidence-tiering-policy.en.md` | 0 | 11331 | 0.0 |
| 9 | `14-ai-development/governance-register/GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.md` | 3139 | 4982 | 0.6301 | `…/GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004.en.md` | 0 | 13368 | 0.0 |
| 10 | `14-ai-development/governance-register/GOV-NC-CONVERGENCE-2026-11-20.md` | 1196 | 717 | 1.6681 | `…/GOV-NC-CONVERGENCE-2026-11-20.en.md` | 0 | 4735 | 0.0 |
| 11 | `14-ai-development/governance-register/README.md` | 1228 | 2739 | 0.4483 | `14-ai-development/governance-register/README.en.md` | 0 | 6937 | 0.0 |
| 12 | `14-ai-development/status-migration-map.zh-CN.md` | 490 | 519 | 0.9441 | `14-ai-development/status-migration-map.en.md` | 0 | 2126 | 0.0 |

这十二对都是「中文文件才是真的、partner 是英文」：中文侧含 490 到 260,510 个汉字，partner 一个汉字都没有。字面规则把十二对全部判为未配对，原因是 `side_by_side_partner()` 是对称的——`side_by_side_partner("X.md")` 返回 `X.zh-CN.md`，`side_by_side_partner("X.zh-CN.md")` 返回 `X.md`。因此「partner 必须含中文」在扫描先遇到中文文件时，等于要求**英文**文件含中文。这十二个缺口是措辞的产物，不是未翻译的配对；就算采纳，基线本身也会拒绝：`--write-baseline` 只允许收缩，会报出十二条待增条目。

## 3. 测量二 — 指定侧规则

实施的规则：一对文件中，被指定承载中文的那个文件必须至少含一个汉字。指定是明确的命名约定：出现 `.zh-CN.md` 就是它；否则是朴素的根 `.md`（Shape 3：根文件是中文原文，`.en.md` 是英文版本）。英文侧永远不计数。

| | |
|---|---|
| 改前缺口 | **77** |
| 改后缺口 | **77** |
| 新增缺口 | **0** |
| 消失缺口 | **0** |

因此两份冻结基线都不需要改，收缩写入也不触发：没有条目新增，也没有条目消失。`scripts/bilingual-baseline.txt` 与 `scripts/ci/baselines/bilingual-docs.txt` 本次均未改动。

## 4. 为什么这个漏洞是潜伏的

在已提交的树上，`side_by_side_partner()` 共解析出 **103** 对：

- **26** 对两侧都有中文；
- **76** 对只有指定的中文侧有中文（英文源 + 中文 partner，即正常形态）；
- **1** 对两侧都没有中文，靠 `docs/en` + `docs/zh-CN` 镜像配对，与本判定无关；
- **0** 对是仅靠英文侧才被接受的。

「0」正是修复代价为零的原因：今天树里没有任何一对是被删掉的那半个分支背书的，因此收紧判据不会把任何条目推进缺口集。登记 013 §3.1 已经测过这个漏洞可达；本文补充的是：它目前没有被占用。

## 5. 双夹具实测（改前 / 改后）

在一个一次性 git 仓库里建 `02-domain-model/`，放入一个顺手写了汉字的英文源、一份英文 `.zh-CN.md` 复制件，以及一份真正的中文短译文，在两个版本上分别跑 `current_bilingual_gaps()`：

| 夹具 | 改前 | 改后 |
|---|---|---|
| `zz-stray.md` = `English source naming 方案 and 编排 in passing.`，`zz-stray.zh-CN.md` = `English source naming the plan and the orchestration in passing.` | 配对被接受；两侧都不在缺口集 | 配对被拒绝；**两侧**都在缺口集 |
| `zz-short.md` = `English source.`，`zz-short.zh-CN.md` = `中文翻译。` | 配对被接受 | 配对被接受（不变） |

第二行即 #469 的义务：简短仍不被惩罚，因为下限仍是「指定侧一个汉字」。

## 6. 改了什么，以及刻意没改什么

改动：

- `scripts/check_bilingual_docs.py` — 新增 `_chinese_side(source, partner)` 指出指定文件；`_side_by_side_bilingual()` 只读该文件。`_has_any_chinese()` 及其一个汉字的阈值、`_carries_chinese()` 及其 100 字阈值、`PARTIAL_SIDE_BY_SIDE_PAIRS`、镜像分支全部未动。
- `scripts/governance/evidence/test_gate_normative_roots.py` — `test_issue_469_short_translation_is_accepted` 改名为它实际测的规则 `test_short_translation_on_the_chinese_side_is_accepted`；新增两个回归测试 `test_stray_cjk_in_english_source_does_not_vouch_for_the_pair` 与 `test_english_copy_without_cjk_under_zh_cn_name_is_rejected`。测试数 52 → 54。

刻意不做：

- 不删镜像、不写译文：第 2 节的十二个文件与 77 条基线条目全部未动。
- 不移动 `_carries_chinese()` 的 100 字阈值，side-by-side 下限仍是一个汉字。
- 不新增、不删除、不重排任何基线条目；不动任何工作流、required context 或分支保护。
- 不关闭任何 Issue。

## 7. 测试证据

在该 head、该工作树上以 `PYTHONUTF8=1` 运行两套测试：

| 命令 | 结果 |
|---|---|
| `python -m unittest scripts.governance.evidence.test_gate_normative_roots` | `Ran 54 tests … OK`，退出码 0 |
| `python -m unittest discover -s scripts -p "test_check_bilingual*"` | `Ran 15 tests … OK`，退出码 0 |

CI 的 `GOV-DOC-001 structural checks` 在跑门禁本体之前正是执行这两条命令，因此本地跑的就是 required context 跑的。

## 8. `DEFERRED_TO_OWNER`

- **D1 — 一个汉字的下限本身。** 登记 013 §3.2 与 `OWNER-DECISION-EMBEDDED-BILINGUAL-001.md` §4 要求配对较短一侧达到 100 字下限。把现有 `_carries_chinese()` 的 100 汉字阈值用在指定侧（而不是一个汉字）的实测代价：缺口 77 → 77，新增 0，消失 0——与第 3 节同样是零。本次**未**采纳，因为本单元被明确要求不得改动该阈值，且该下限属于 `AID-2026-054` 的授权范围。两者的重叠是真实的：落 054 的人会重写同一个函数，两处改动彼此独立但相邻。
- **D2 — 镜像分支仍只做结构判断。** `mirrored` 只要 `docs/en/X` 与 `docs/zh-CN/X` 同时存在就算配对，不读内容，因此 `docs/zh-CN` 路径下可以放英文而照样通过。一个实测的现成例子（未修复）：`docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` 含 0 个汉字、1,073 个拉丁字母，它通过是因为 `docs/zh-CN` 的同名文件存在，而不是因为任何内容被翻译过。关闭该分支是另一个判据、对 77 条基线是另一笔代价，不在本单元范围内。

合并本改动只证明仓库集成，不构成 Owner 验收、独立评审或译文充分性的任何主张。
