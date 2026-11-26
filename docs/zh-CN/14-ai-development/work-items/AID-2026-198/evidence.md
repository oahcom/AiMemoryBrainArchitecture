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
        - "14-ai-development/work-items/AID-2026-198/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "以下每个数字都在本工作树按所述 HEAD 重新测量：改前改后 blob 与字节数取自 git rev-parse 与 git cat-file，增删行数取自 git diff --numstat，门禁输出取自门禁自身 stdout。不主张的内容：英中镜像的语义等价未经审查，也不主张任何审批或验收决定。"
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
    canonical_scope: "AID-2026-198 证据：为 07-agent-integration 的 inference-boundary 与 telemetry 镜像组补 GOV-DOC-002 元数据，并记录 07/08/13 其余镜像的实测边界"
    canonical_scope_id: "ai-development/aid-2026-198-mirror-frontmatter-b-evidence"
    canonical_scope_keywords:
      - "gov-doc-002"
      - "frontmatter"
      - "bilingual-mirror"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-198/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-198/evidence.md"
    zh-CN: null
---

# AID-2026-198 — 为 07/08/13 镜像补 GOV-DOC-002 元数据

## 范围与归属

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 基础分支：`main`；分支 `fix/2026-11-27-mirror-frontmatter-b`，工作树 `D:\code\wt-corpus-b`
- 建分支时的基础提交：`4326669c`（完整 SHA 见 `manifest.yaml`）；开 PR 前再次并入 `origin/main`（`0c752ee6`）
- 归属：经用户授权的执行者（由账户所有者委派）。此处不主张任何自然人 Owner 签名、验收或批准。
- 单元简报：`unit-corpus-b.md`——“给 07/08/13 的镜像补 frontmatter”。其禁止项一并遵守：不改正文、不改基线、不动 `03/04/05/09`、不新建 canonical、不新建镜像。

## 缺陷

`docs/en/**` 与 `docs/zh-CN/**` 中存在首行不是 `---` 的镜像 Markdown 文件，GOV-DOC-002 无法对其分类（`check_document_management.py` 将其计为未分类）。本单元负责的三个目录里，此类镜像共 22 份（11 对）：

| 目录 | en | zh-CN | 对数 |
|---|---|---|---|
| `07-agent-integration` | 5 | 5 | 5 |
| `08-bmcp-protocol` | 3 | 3 | 3 |
| `13-engineering-decisions` | 3 | 3 | 3 |

## 本次改动

共 6 个文件，构成两个完整的镜像组。每组在根源补一个元数据块、两个镜像各补一个；所有文件的正文与改动前逐字节相同。

| 路径 | 改前 blob | 改后 blob | 字节 | 新增 | `--numstat` |
|---|---|---|---|---|---|
| `07-agent-integration/inference-boundary-model.md` | `e2d5cb6abd9ec40da6e3680531de5944fc8b14df` | `9afd414bb5f3224f28f605fd854ff06d9fd4ceb2` | 13533 → 15004 | +1471 | 46 / 0 |
| `docs/en/07-agent-integration/inference-boundary-model.md` | `e2d5cb6abd9ec40da6e3680531de5944fc8b14df` | `a1b7f7555cc0231860b325d1c4ca4890ce6d50a4` | 13533 → 14927 | +1394 | 45 / 0 |
| `docs/zh-CN/07-agent-integration/inference-boundary-model.md` | `ba3a737b7b4fcf1a4a88e4f99667ef2f2ee4bbea` | `8b208da3f013cfb572f3c7d390a1592bb8bca180` | 14022 → 15386 | +1364 | 45 / 0 |
| `07-agent-integration/telemetry-model.md` | `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0` | `7afef508b3d83c4381eb9cfc91c5dd9d03317856` | 15077 → 16497 | +1420 | 46 / 0 |
| `docs/en/07-agent-integration/telemetry-model.md` | `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0` | `5a23480422d1a74467bd20fb5cce542d1d25ef9c` | 15077 → 16429 | +1352 | 45 / 0 |
| `docs/zh-CN/07-agent-integration/telemetry-model.md` | `a8141952eed383a3827f3d4eb26aa9345740ca24` | `205338cc8fa2d7d337467d138919f94602b8aec9` | 15589 → 16911 | +1322 | 45 / 0 |

`git diff --numstat` 在六个文件上删除行均为 0：插入的就是元数据块本身（根源 46 行；镜像 45 行，因为镜像写 `source:` 而不是 `en:`/`zh-CN:` 两个键）。两个 `docs/en` 文件的改前 blob 与根源相同——原先它们是逐字节副本——所以改前 blob 编号成对重复。

结构沿用仓库中已分类的 `07-agent-integration/agent-integration-guide.md`：

- 根源：`canonical_status: Non-Canonical`、`normative_status: Informative`，且 `bilingual_counterpart` 同时列出两个镜像；
- 每个镜像：`bilingual_counterpart.source` 指向根源，并列出另一侧镜像；
- 组内 `domain`、`role`、`normative_status` 必须一致（DM-12 要求）；
- `decision_status: Draft`、`approver: null`：这些文档没有审批记录，此处也不主张。

## 本次不做的事，以及为什么（实测而非推测）

### 07/08/13 的 22 份镜像中有 16 份是孤儿 —— `ORPHAN_SKIPPED`

11 对里有 9 对的根源在树中不存在，镜像指向空处：

- `07-agent-integration`：`phase-3.6-c-submit-cross-authority-causal-order-contract.md`、
  `phase-3.6-final-request-evidence-contract.md`、
  `phase-3.8.19-c-exact-review-h-fullpath-38-test-current-head.md`
- `08-bmcp-protocol`：`adapter-capability-and-applied-attestation.md`、`bmcp-guide.md`、
  `phase-3.6-identity-binding-consumer-conformance-status.md`
- `13-engineering-decisions`：`req02-fts5-vs-like-benchmark.md`、`req02-fts5-vs-like-decision.md`、
  `technology-architecture-overview.md`

DM-12 对孤儿镜像不接受任何形状。在 `docs/{en,zh-CN}/08-bmcp-protocol/bmcp-guide.md` 上实测（探针随后立即回滚，不属于本次改动）：

```
FAIL: 4 error(s)
  DM-12 docs/en/08-bmcp-protocol/bmcp-guide.md: bilingual_counterpart.source does not exist: 08-bmcp-protocol/bmcp-guide.md
  DM-12 docs/zh-CN/08-bmcp-protocol/bmcp-guide.md: bilingual_counterpart.source does not exist: 08-bmcp-protocol/bmcp-guide.md
  DM-12 docs/en/08-bmcp-protocol/bmcp-guide.md: names 08-bmcp-protocol/bmcp-guide.md as its source, but that file is not a classified governed document
  DM-12 docs/zh-CN/08-bmcp-protocol/bmcp-guide.md: names 08-bmcp-protocol/bmcp-guide.md as its source, but that file is not a classified governed document
```

不写 `source` 也不成立：镜像根下的文件缺少它会被判“不属于任何组”。补建缺失的 canonical 等于新建 canonical，本单元简报禁止，因此这 16 份保持原样，在此列出而不猜测处理。

### `13-engineering-decisions` 的 58 条冻结缺口维持冻结

`scripts/bilingual-baseline.txt` 共 77 条，分布为 `13-engineering-decisions: 58`、
`06-memory-context: 10`、`08-bmcp-protocol: 4`、`14-ai-development: 4`、`00-governance: 1`。这 58 条是
`13-engineering-decisions/domain-model-research/` 与 `13-engineering-decisions/technology-research/`
（外加 `technology-architecture-blueprint.md`）下没有 `docs/en`、也没有 `docs/zh-CN` 镜像的根源。

它们本就未分类（门禁打印 `13-engineering-decisions: 0/58 classified`）。给其中一份加元数据块是实测而非假设——探针打在
`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md`，随后立即回滚：

```
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md
Bilingual documentation gate: FAIL
```

两个必需的镜像并不存在。补建就会消解冻结缺口，而消解后的条目必须同一次改动里从 `scripts/bilingual-baseline.txt` 删除——那是只有 Owner 决定才能做的基线编辑。因此本任务不改变 77 条基线、不新增也不消除缺口：`13-engineering-decisions` 保持 `0/58` 已分类，这是刻意的。

## 门禁测量

改前 = `4326669c`（分支点，6 个文件未改）；改后 = `c27a23df` 并入 `origin/main` 之后。以下均为门禁自身 stdout。

| 门禁 | 改前 | 改后 |
|---|---|---|
| `check_document_management.py`（全树） | 942 受治理，496 已分类，446 未分类，0 规则违规，INCOMPLETE（存量待办） | 942 受治理，502 已分类，440 未分类，0 规则违规，INCOMPLETE（存量待办） |
| `check_document_management.py --require-changed origin/main` | 不适用（无改动） | PASS（增量）：无 GOV-DOC-002 违规；502 已分类，440 未分类 |
| `07-agent-integration` 分栏 | 6/8 已分类 | 8/8 已分类 |
| `docs` 分栏 | 173/343 已分类 | 177/343 已分类 |
| `13-engineering-decisions` 分栏 | 0/58 已分类 | 0/58 已分类 |
| `check_bilingual_docs.py`（增量） | NOT_APPLICABLE——零改动路径，未作判断 | PASS：`bilingual baseline: 77 frozen, 0 new gaps`（检查 6 条改动路径） |
| `check_bilingual_docs_full.py` + 棘轮 | 77 条，FAIL-即-基线 | `baseline=77 current=77 regressions=0 fixed=0`，PASS——失败集合与基线完全一致 |
| `test_check_document_management.py` | 326/326 通过 | 326/326 通过（本工作项未触及） |
| `test_check_bilingual_docs.py` | 15 项 OK | 15 项 OK |
| `test_gate_normative_roots` | 52 项 OK | 52 项 OK |
| `scripts/ci/check_line_endings.py` | 0 违规 | 1629 个文件，0 违规 |
| `scripts/ci/check_repository_hygiene.py --base --head` | 不适用 | 新文件准入检查 0 条路径，manifest 一致性 violations=0 |

冻结基线未被本工作项改变：改前改后均为 `baseline=77 current=77 regressions=0 fixed=0`。

### 最终 HEAD

上表隔离的是 6 份元数据文件。到最终 HEAD（同时还包含本登记集，以及从 refs 单元并入 `origin/main` 的登记——该登记本身编号为
AID-2026-190），同一门禁打印 **952 受治理，512 已分类，440 未分类**：其中 502 来自镜像改动，5 份受治理文档由本工作项新增
（根源侧三份工作记录文件加两个证据镜像），另有 5 份来自本次合并。规则违规仍为 0，未分类存量仍为 440，棘轮仍报告
`baseline=77 current=77 regressions=0 fixed=0`。

## 本记录的边界

- 不对英中镜像文本的语义等价作任何主张。本次只插入元数据，门禁检查结构，不检查翻译质量。
- 不主张这三个目录的 22 份缺陷已关闭：本次分类 6 份，其余 16 份作为 `ORPHAN_SKIPPED` 记录，并附上拒绝它们的门禁错误。
- 不涉及 `00/01/02/06`（单元 corpus-a）与 `03/04/05/09`（本批次所有单元的共同禁改范围）。
- 本工作项不修改任何 checker、workflow、schema、registry 或基线文件。
