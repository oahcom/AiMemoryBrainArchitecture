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
        - "14-ai-development/work-items/AID-2026-300/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Snapshot of the task text actually received by the implementation session, transcribed verbatim to this file by the executing party. The body has not been rewritten by the session. This snapshot is not frozen, and no claim beyond the supplied digest is made."
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
    source: null
    en: null
    zh-CN: null
---

# AID-2026-300 — dispatched contract snapshot (v1)

本文件是投递给实现会话的提示词正文快照，由执行方逐字落盘；正文未经会话改写。正文中的 `AID-2026-261` 是投递时使用的编号，后因该编号在合并时刻已被 main 占用，本工作项改号为 `AID-2026-300`。

# 任务：实现 Option (d) —— 串行化、合并时刻的 work-item 唯一性门禁（Issue #1341 / AID-2026-261）

你是一个实现会话。下面是你需要的**全部**上下文：契约、实测事实、模板全文、输出格式。你看不到仓库，所以凡是你需要的仓库事实都在本文里；凡是本文没有的数字，一律用 `<FILL:名字>` 占位，由执行方实测后回填。

**本轮只做一件事**：按下面的格式，给出全部交付文件的**完整内容**（不是 diff、不是片段、不是"可自行调整"的骨架）。一轮给全，不要分轮，不要问我要更多信息。

---

## 1. 要实现的契约（Issue #1341 原文表格）

| 情形 | 要求行为 |
|---|---|
| 合并候选**新增** work-item 目录 | 该 ID 在**最新目标分支**上已占用 → 拒绝 |
| 在**已存在**的 work-item 目录下新增文件 | 接受（增量文件不是重复登记） |

权威对象：**合并候选 vs latest 目标分支**，不是更早的分支 HEAD，也不是分支自己的 base。

背景（缺陷机制，不是事故）：`scripts/check_traceability.py` 的 `T-04 duplicate INDEX entry` 只在**被检查的那棵树内部**查重。每个分支各有一行 `INDEX.md` 记录，所以分支上恒绿，合并到 main 后才红。五个 PR 在同一批次撞上 main 上已占用的 ID，就是这条机制的结果。

## 2. 验收证据表（8 行，交付物必须能逐行给证明）

| 证据 | 需要的证明 |
|---|---|
| 契约 | 明确定义「新目录唯一性」与「既有目录增量」 |
| 串行化 | 证明并发 PR 合并不可能都对着同一个陈旧 base 通过校验 |
| 正例 | 新的、未占用的 work-item ID 被接受 |
| 负例 | 新目录 ID 已在最新 base 上存在 → 拒绝 |
| 增量 | 既有 work-item 目录下新增文件被接受 |
| 竞态 | 两个 PR 各自引入同一 ID，不可能都合并 |
| 精确 head | 结论绑定真实合并候选，不是更早的分支 head |
| 回归 | 既有 traceability / hygiene / bilingual 门禁继续通过 |

**门禁"跑起来了"不算证据。** 负例与竞态必须真的变红（非零退出 + 明确消息），并且这个红必须来自被测检查器本身，不是环境错误。

## 3. 实测事实（在 base commit `a7a252eb670b31066a0ffea35dc28cbe6ef5b836` 上量的）

### 3.1 仓库与运行环境

- 仓库 `oahcom/AiMemoryBrainArchitecture`，目标分支 `main`，本文的 base commit = `a7a252eb670b31066a0ffea35dc28cbe6ef5b836`（PR #1364 的合并提交）。
- 工作分支 `fix/2026-11-27-aid261-workitem-uniqueness-gate`，worktree `C:\tmp\opencode\a261`。
- Python 3.12.3；CI 用 `actions/setup-python@v5` + `python-version: "3.12"`。
- 仓库所有文本文件在对象库里是 **LF**（`.gitattributes`: `* text=auto` + 逐类型 `eol=lf`）。你给的文件必须是 LF 语义（我落盘时会保持 LF）。
- **不要引入新依赖**：CI 的裸解释器只有标准库（只有个别 job 会 `pip install pyyaml`）。检查器请用标准库 + `git` 子进程。
- 所有 workflow job 必须 `runs-on: ubuntu-latest`，这是硬策略：`scripts/ci/audit_runner_admission.py` 静态读 `.github/workflows/*` 并拒绝任何非 `ubuntu-latest` 的 `runs-on`（包括动态表达式）。

### 3.2 work-item 目录与 INDEX

- 目录：`14-ai-development/work-items/AID-YYYY-NNN/`，每个目录里有 `manifest.yaml`（可另有 `evidence.md` / `session-evidence.md` / `prompt-v1.md` 等）。
- base 上：`14-ai-development/work-items/` 下 **120 个目录**，**110 个 `manifest.yaml`**，`INDEX.md` 里 **109 行** `| [AID-...` 记录。本分支已先提交一个 `AID-2026-261` 骨架（+1 目录 / +1 manifest / +1 行），所以现在实测是 121 / 111 / 110。
- `AID-2026-261` 在 base 上**未被占用**：120 个目录里没有它，`INDEX.md` 里没有它，全部 `refs/remotes/origin/*` 里也没有它的目录，11 个 open PR 的文件清单里也没有。
- `INDEX.md` 表头（第 50 行）与分隔行（第 68 行）：

```
| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
|---|---|---|---|---|---|---|---|---|
```

  注意：表头 9 列，历史行有的写了 9 个单元格，有的把 `Class/Risk` 与 `Status` 合并成 8 个单元格；两种都在树里存在，检查器不能假设列数固定。
- `.gitattributes` 给这一个路径开了 union 合并驱动：`14-ai-development/work-items/INDEX.md merge=union`。注释里写明理由：并发的两行登记都要保留，冲突只是文本相邻；而 union 会把「同一 AID 出现在两行」变成静默重复，所以必须有重复检测先跑（`check_traceability.py --index-only` 的 T-04）。
- `INDEX.md` 现有行的两个格式样本（照这个风格写，不要换列语义）：

```
| [AID-2026-240](AID-2026-240/manifest.yaml) | Make the 77-entry frozen bilingual inventory have one authority: ... | USER-PRINCIPAL-DELEGATED | GATE/TEST / R1 | DRAFT — PR PENDING; `id_status: PROVISIONAL`; ... | `AID-2026-240-PROMPT` v1 — `14-ai-development/work-items/AID-2026-240/prompt-v1.md`, 4717 bytes, SHA-256 `0becb142...`; `prompt_status: NOT_RECORDED` | CODE + TESTS + DOCS — ... | NOT_ASSIGNED — independent review not recorded | PENDING — `#1212` remains OPEN; no acceptance decision asserted |
| [AID-2026-251](AID-2026-251/manifest.yaml) | Define the Work Item manifest schema, documentation references, session evidence and implementation block; measure legacy compliance without migration | USER-PRINCIPAL-DELEGATED | GATE/TEST / R1 | PR pending; schema and read-only checker introduced; baseline inventory 108 manifests at f18adc9f | ChatGPT GPT-6; actual task input and visible output recorded in session-evidence.md | Schema + checker + workflow; no legacy manifest migration | NOT_ASSIGNED | PENDING — no Owner acceptance asserted; #266 remains open |
```

本分支 `INDEX.md` 末尾当前有一行（我写的骨架，**你要给的是它的最终版本**，可以整行替换）：

```
| [AID-2026-261](AID-2026-261/manifest.yaml) | Serialized, merge-time work-item uniqueness gate: judge the merge candidate against the latest target branch, not the branch own base (Issue #1341, defect #1331) | USER-PRINCIPAL-DELEGATED | GATE/TEST / R1 | DISPATCHED 2026-11-27; number reserved in the tree so parallel units cannot allocate it; `id_status: PROVISIONAL`; implementation not started | NOT_RECORDED | NOT_STARTED | NOT_ASSIGNED | PENDING - no acceptance decision asserted; #1341 remains OPEN |
```

### 3.3 既有门禁的真实形状（你的检查器必须与它们互补，不许重复或打架）

**(a) `scripts/check_traceability.py`（986 行）**，标准库 + `git`。关键事实：

- `REGISTRY_PATH = Path("00-governance/requirements-registry.yaml")`，而**这个文件在树里不存在**（#1071/#1064）。所以裸跑 `python scripts/check_traceability.py` 会 `FAIL ... ERROR required registry unavailable` 并 exit 1。CI 跑的是 `python3 scripts/check_traceability.py --index-only`（`.github/workflows/repository-hygiene.yml:146`），这个入口只做 INDEX/manifest 那一半，不需要 registry。
- 退出码词汇：`0 PASS / 1 FAIL(errors) / 2 INCOMPLETE(indeterminate)`。`--index-only` 在 base 上的输出是 `PASS TRACEABILITY: 0 requirements / 109 work items / 0 errors / 108 warnings`，exit 0。
- 重复检测就在第 745 行：`reporter.error("T-04 duplicate INDEX entry {}".format(aid))`，它遍历的是**当前工作树的 `INDEX.md`**，所以只查树内重复。`validate_index_and_manifests()`（725–858 行）做四件事：每个 INDEX 行必须解析到存在的 manifest；INDEX id 必须等于 manifest 所在目录名；每个磁盘上的 manifest 必须有 INDEX 行；manifest 的 `work_item_id` 必须等于目录名（`manifest_identity()`，其中 legacy `aid` 键只对白名单 ID 兼容）。
- **你的检查器不得复制这四件事**，只做"候选 vs 目标"的跨树判定。

**(b) `.github/workflows/branch-freshness.yml`（全文，42 行）** —— 已存在的"新鲜度"门禁，它只检查「分支包含它的 base」：

```yaml
name: Branch freshness

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
  cancel-in-progress: true

# #719: a PR's diff is computed from merge-base(base, head) to head, so a stale
# branch shows changes it did not make and hides changes main made that it
# re-implements. The diff cannot report its own staleness; the commit graph can.
#
# GitHub-hosted runner. Server-side/self-hosted Actions runners are retired;
# the repository policy workflow rejects any non-ubuntu-latest job.
#
# `fetch-depth: 0` is load-bearing: a shallow clone does not contain the merge
# base, and the gate exits 2 rather than guessing.

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

permissions:
  contents: read

jobs:
  freshness:
    name: Branch freshness vs base
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout pull request with full history
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Self-check the branch freshness gate
        run: python3 scripts/ci/test_check_branch_freshness.py

      - name: Check the branch contains its base
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        run: python3 scripts/ci/check_branch_freshness.py
```

**(c) 仓库的 concurrency 惯例**：11 个 workflow 全部是

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
  cancel-in-progress: true
```

这个形态是**按 head SHA 分组**：同一 PR 的新提交会取消旧运行，**不同 PR 之间完全不串行**。如果你的串行化依赖 concurrency，必须解释它和这个惯例的差别，以及 `cancel-in-progress: false` 为什么是必需的。

**(d) 平台侧的实测事实（这些决定了"串行化"能论证到什么程度，必须诚实对待）**：

- `main` 的 branch protection payload（`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main`）只暴露 `enabled` 与 `required_status_checks`，16 个必需上下文是：`GOV-DOC-001 structural checks`、`Branch freshness vs base`、`audit`、`GOV-DOC-002 metadata checks`、`BMCP protocol index (hard gate)`、`BMCP conformance suite (hard gate)`、`Schema non-empty audit (hard gate)`、`Bilingual docs coverage (ratchet)`、`Rust clippy (hard gate)`、`Repository hygiene (hard gate)`、`Rust format (hard gate)`、`Rust doctests (hard gate)`、`Session Evidence`、`Session Evidence self-test (base)`、`Session Evidence self-test (head)`、`rust-workspace-test`。
- 该 payload 里 `required_status_checks.strict` 是 `null`（即"合并前要求分支与 base 同步"这一项从 payload 上看**没有开启**）。
- `.github/workflows/` 下 **`merge_group` 出现 0 次**（`git grep -ln merge_group -- .github` 无匹配），也没有任何 merge queue 的痕迹。
- 结论性事实：**本仓库今天没有可用的 merge queue**，且"合并前必须与 base 同步"从 payload 上看没开。所以"两个 PR 不可能都对着陈旧 base 通过"**不能**靠"我们有 merge queue"来论证。你要么给出树内可强制、可复现的机制，要么把机制拆成「树内已强制」+「平台依赖项（未验证，明确标注）」两部分，并说清残余窗口。**不许声称 branch protection 或 merge queue 已经加入/启用。**
- workflow 的 `permissions:` 惯例是 `contents: read`。如果你要读 `pulls` API（例如读其他 open PR 的树），必须显式加 `pull-requests: read`，并在注释里说明为什么需要它、以及 token 不可用时如何 fail closed。

**(e) 声明上下文校验**：`scripts/check_declared_check_contexts.py` 读 `14-ai-development/PR-GOVERNANCE-001.md` 里 `<!-- declared-check-contexts` 标记后的清单，做两个方向的比较：`declared → produced`（声明的每个名字必须由树里某个 job 产出，**多出来的 job 允许**）和 `declared → protected`（声明的集合与平台 payload 的必需集合必须相等）。所以：**新增一个 job 不会破坏它，但你不得去改 `PR-GOVERNANCE-001.md` 假装新 job 已是必需上下文。**

**(f) `gates.yml` 的注释传统**（12.7KB，硬门禁 / ratchet 的显式区分），原文节选：

```yaml
name: Existing gates

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
  cancel-in-progress: true

# All jobs execute on GitHub-hosted `ubuntu-latest` runners. This workflow is
# both a pull-request gate and a post-merge detector; it must never depend on
# the development server or a self-hosted Actions runner.
#
# ---------------------------------------------------------------------------
# TWO KINDS OF JOB, and the difference is deliberate:
#
#   * HARD GATES fail on any deviation. The gate is green today and must stay
#     green: `protocol-index`, `conformance`, `schema-nonempty`, `clippy`, `fmt`,
#     `doctest`.
#
#   * RATCHETS fail only when the failure set gets WORSE than the recorded
#     baseline: `bilingual`. ...
#
# A GATE MOVES FROM RATCHET TO HARD GATE THE DAY IT GOES GREEN, and it must, or
# the ratchet becomes a permanent exemption. ...
```

新 job 若是硬门禁，注释里必须写明"今天在 main 上绿，且必须保持绿"。

### 3.4 检查器风格基线（`scripts/check_source_revision_pointers.py`，202 行，标准库）

结构要点（照这个风格写）：

```python
#!/usr/bin/env python3
"""<一句话说明这个门禁判定什么，以及它曾经怎么被骗过去（若有）>"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scan(root: Path) -> tuple[dict[str, int], list[str]]:
    totals = {...}
    details: list[str] = []
    ...
    return totals, details


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="...")
    args = parser.parse_args(argv)
    totals, details = scan(args.root.resolve())
    bad = ...
    print("SOURCE_POINTER_SCAN")
    for key in (...):
        print(f"{key.upper()}={totals[key]}")
    print(f"BAD={bad}")
    for detail in details:
        print(detail)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
```

即：`--root` 可覆盖；`KEY=VALUE` 汇总行；每条判定一行明细；`exit 0/1`（本仓库另有 `2 = INCOMPLETE` 的词汇，检查器读不到目标 ref 这类"无法判定"必须 exit 2，不能当 0）。

`git` 调用的既有写法：

```python
def git_blob(root: Path, path: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=root,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    return result.stdout.strip()
```

### 3.5 单元测试的落位与跑法

- 位置：`tests/test_check_work_item_uniqueness.py`（若你给检查器换名字，测试名同步换）。
- 跑法（验收命令，逐字）：`python -m unittest discover -s tests -p "test_check_work_item_uniqueness.py" -v`
- 另一个跑法在 CI 里是 `working-directory: tests` + `python -m unittest -v test_xxx.py`。所以测试文件**不得**依赖 `cwd` 必须是仓库根：用 `Path(__file__).resolve().parents[1]` 定位仓库根，或者自建临时 git 仓库（推荐后者，见下）。
- 测试要能在**任何机器**上跑，不依赖本仓库当前分支状态。推荐做法：`tempfile.TemporaryDirectory()` 里 `git init`，造 `14-ai-development/work-items/` 与 `INDEX.md`，`git add/commit` 造出 target 与 candidate 两个 ref，然后调检查器的 `main([...])` 或 `scan()` 断言退出码与消息。这样正例/负例/增量/精确 head/竞态都能离线复现。
- 竞态行：两个 PR 各自引入同一 ID。用临时仓库造两个 candidate ref（`refs/heads/pr-a`、`refs/heads/pr-b`），让它们都从同一个 target 分出，各自新增同一 ID 的目录。然后断言：串行执行两次判定时，第二次必须红（或按你设计的机制，给出"第二个不可能通过"的可执行证明）。**如果只是"两个都跑起来了"，这一行不算证据。**
- 测试里调用 `git` 需要 `-c user.name=... -c user.email=...`，或 `git commit --author`，否则 CI 容器没有身份会失败。

### 3.6 已存在但**不属于**你要改的东西

- `scripts/ci/check_work_item_manifest_schema.py`（PR #1364 引入，只读，永远 exit 0）：校验 manifest 的 20 个必需顶层键、`documentation` 序列（每项 `{path, relationship}`，`relationship ∈ {normative, design, implementation, evidence, reference}`，`path` 必须是仓库相对 `.md`）、`session_evidence` 非空序列（每项必须有 `role`/`issue_refs`/`implementing_ai_session`/`session_evidence_ref`，后者必须以 `session-evidence.md` 结尾）、`implementation`（`status ∈ {NOT_STARTED, IN_PROGRESS, IMPLEMENTED, BLOCKED, NOT_APPLICABLE}`，`summary`，`files_changed` 序列，`tests` 序列）。**你给的 `manifest.yaml` 必须过这个校验。**
- 20 个必需顶层键（顺序即此）：`work_item_id, title, class, risk, risk_rationale, status, id_status, sponsor, accountable_owner, acceptance_authority, attribution, date, repository, base_branch, base_commit_sha, scope, evidence, documentation, session_evidence, implementation`。

### 3.7 manifest 结构模板（`14-ai-development/work-items/AID-2026-240/manifest.yaml` 全文，150 行）

```yaml
work_item_id: AID-2026-240
title: >-
  Make the 77-entry frozen bilingual inventory have one authority: declare every
  copy, compare all of them in check_baseline_copies_agree(), and mark the drifted
  81-entry review snapshot as a historical record rather than a gate input
class: GATE/TEST
risk: R1
risk_rationale: >-
  One standard-library checker and its unit tests, plus heading-level annotations on
  two review snapshots and three clarifications on two guide pages. No baseline entry,
  no NORMATIVE_ROOTS value, no workflow and no branch protection changes; the gate's
  decision semantics for a repository whose copies agree are unchanged. The residual
  risk is the opposite of damage: a comparator that silently covers only the copies it
  was told about is exactly the defect being repaired, so the new discovery step fails
  closed on any tracked file that carries most of the inventory without being declared,
  and a real-tree test asserts that the declared set is the whole set at this head.
status: DISPATCHED
id_status: PROVISIONAL
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED
acceptance_authority: NOT_ASSIGNED
attribution: user-authorized operator (delegated by account owner)
date: 2026-11-27
repository: oahcom/AiMemoryBrainArchitecture
base_branch: main
base_commit_sha: 951051313b6cac60b1a3acb069e08de6c5e796c0
prompt_status: NOT_RECORDED
prompt_provenance: DISPATCHED_TASK_FILE
identifier_allocation:
  id_status: PROVISIONAL
  observed_main: 951051313b6cac60b1a3acb069e08de6c5e796c0
  assigned_id: AID-2026-240
  allocation_rule: >-
    This branch was allocated three numbers while it stayed open, because parallel
    repair units were allocating from the same range and each one merged first. 190 was
    taken by PR #1343 and 191 by PR #1345 after this branch had claimed them; neither is
    claimed here and no path under either is created or modified. At the third allocation
    the highest number observed in any pull-request title, branch, body or tree path was
    AID-2026-204, with 190-199 and 204 occupied; 240 was chosen well clear of the range
    the parallel units are drawing from, and no AID-2026-2xx string above 204 existed in
    the tree or in any branch name at that time.
  observed_occupied: [170, 172, 173, 188, 189, 190, 191, 192, 193, 197, 198, 199, 204]
evidence:
  record: 14-ai-development/work-items/AID-2026-240/evidence.md
  mirrors:
    - docs/en/14-ai-development/work-items/AID-2026-240/evidence.md
    - docs/zh-CN/14-ai-development/work-items/AID-2026-240/evidence.md
  measurements:
    inventory_authority: scripts/ci/baselines/bilingual-docs.txt
    authority_entries: 77
    copies_enumerated: 7
    copies_structurally_gated: 6
    copies_equal_to_authority: 2
    copies_superset_of_authority: 1
    copies_marked_historical: 2
    copies_dated_snapshot: 1
    copies_prose_only: 1
    drifted_snapshot_entries: 81
    drifted_snapshot_extra: 8
    drifted_snapshot_absent: 4
    copy_errors_before_widening: 0
    copy_errors_after_widening: 0
    copy_notices_after_widening: 2
    undeclared_inventory_copies: 0
    bilingual_gaps: 77
    ratchet_baseline_entries: 77
    ratchet_result: "baseline=77 current=77 regressions=0 fixed=0 PASS"
  test_runs:
    - command: python -m unittest discover -s scripts -p "test_check_bilingual*"
      result: "Ran 25 tests, OK (was 15)"
    - command: python -m unittest discover -s tests -p "test_check_bilingual*"
      result: "Ran 7 tests, OK"
  not_measured:
    - No CI context result is claimed at any SHA
    - No merge SHA or post-merge blob digest is claimed
    - "Both test runs and the ratchet run are local executions in this worktree"

# prompt_status above records that no prompt-library registration exists. The
# dispatched contract text itself was captured by the operator into prompt-v1.md and
# pinned so the requirement set can be read against what was measured and changed.
session_evidence:
  - role: "GATE_REPAIR_AUTHOR"
    issue_refs:
      - "#1212"
    implementing_ai_session: "opencode-go/deepseek-v4.1-flash"
    executed_prompt_snapshot_file: "14-ai-development/work-items/AID-2026-240/prompt-v1.md"
    executed_prompt_sha256: "0becb14207ff1b1405833a464d0bd098a0442db6ae699f67299d28420c79aba8"
    executed_prompt_bytes: 4717
    executed_prompt_provenance: "NOT_VERIFIED"
    session_reference_status: "NOT_RECORDED"
    session_evidence_ref: "14-ai-development/work-items/AID-2026-240/session-evidence.md"

scope:
  files_to_create:
    - 14-ai-development/work-items/AID-2026-240/manifest.yaml
    - 14-ai-development/work-items/AID-2026-240/evidence.md
    - 14-ai-development/work-items/AID-2026-240/prompt-v1.md
    - 14-ai-development/work-items/AID-2026-240/session-evidence.md
    - docs/en/14-ai-development/work-items/AID-2026-240/evidence.md
    - docs/zh-CN/14-ai-development/work-items/AID-2026-240/evidence.md
  files_to_modify:
    - scripts/check_bilingual_docs.py
    - scripts/test_check_bilingual_docs.py
    - 14-ai-development/ci-gates-and-ratchets.en.md
    - 14-ai-development/ci-gates-and-ratchets.zh-CN.md
    - reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md
    - reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md
    - 14-ai-development/work-items/INDEX.md
  files_out_of_scope:
    - scripts/ci/baselines/bilingual-docs.txt content
    - scripts/bilingual-baseline.txt content
    - scripts/check_bilingual_docs_full.py
    - current_bilingual_gaps()
    - 00-governance/reports/gov-doc-001-full-scan-2026-11-20.md content
    - 14-ai-development/governance-register/evidence/main-paths.json content
    - .github/workflows
    - branch protection

non_goals:
  - Changing any entry of any copy of the inventory, including the 81-entry snapshot
  - Regenerating either baseline, or making the frozen set smaller
  - Ruling on whether the 77 frozen gaps are acceptable
  - Closing #1212 or asserting Owner acceptance

carrier:
  branch: fix/2026-11-27-baseline-copies
  pull_request: PENDING
  merge_sha: PENDING
  merge_method: merge
  required_contexts: "PENDING"
review:
  status: NOT_ASSIGNED
  independent_reviewer: NOT_ASSIGNED
  natural_person_owner_acceptance: NOT_RECORDED
acceptance:
  gate: PENDING_CI
notes:
  - >-
    The dispatched premise said the drifted copy is "多 9 / 缺 5". Measured against
    scripts/ci/baselines/bilingual-docs.txt, the 81-entry table in
    BMCP-ARCH-001.{en,zh-CN}.md holds 8 entries the authority does not and omits 4 that
    it holds; 73 shared, 73 + 8 = 81 = 77 - 4. The arithmetic of the premise holds, the
    two operands do not, and the measured numbers are the ones recorded here.
  - >-
    "7 files" reproduces, but not as seven equal copies: two hold the 77 entries
    exactly, one is an 803-path governance register that contains all 77, one is a
    dated 83-finding scan record, two are the 81-finding review snapshot in both
    languages, and one is a work-item proposal that mentions 62 of the paths in prose
    with no list block. Only the first two can be compared entry by entry, so the gate
    declares one role per file instead of pretending all seven are the same thing.
```

### 3.8 evidence.md 的 frontmatter 模板（`AID-2026-240/evidence.md` 第 1–46 行）

```markdown
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
      last_verification_note: "Every number below was produced by running the files in this worktree at base 951051313b6cac60b1a3acb069e08de6c5e796c0: ... No CI result, merge SHA or post-merge blob is claimed."
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
    canonical_status: Canonical
    canonical_scope: "AID-2026-240 designation of ... "
    canonical_scope_id: "ai-development/aid-2026-240-frozen-inventory-single-authority"
    canonical_scope_keywords:
      - "bilingual"
      - "baseline"
      - "frozen-inventory"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-240/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-240/evidence.md"
---
```

注意：`bilingual_counterpart` 如果写了 `en`/`zh-CN` 路径，那两个镜像文件必须存在（GOV-DOC-001 会查配对）。**本工作项不要造双语镜像**——把 `en` 与 `zh-CN` 都写 `null`，`source` 也 `null`，避免引入两份必须同步的镜像文档。

### 3.9 session-evidence.md 的 frontmatter 模板（`AID-2026-240/session-evidence.md` 第 1–43 行）

```markdown
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
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the request as received, the environment it ran in, and the commands whose output is quoted in evidence.md. No platform session identifier is available, so the session identity is recorded as NOT_RECORDED rather than inferred."
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
    source: null
    en: null
    zh-CN: null
---
```

正文结构（照 `AID-2026-240/session-evidence.md` 的小节名）：`## Session role / use case`、`## Actual AI input`、`## Environment`、`## Commands run and where their output is quoted`、`## What this session did not do`。要求：只写你能从本文件内容真实知道的事；会话身份写 `NOT_RECORDED`，不要编模型名或会话 id。

---

## 4. 必须产出的 7 个交付物

用围栏块逐个给出，围栏信息行写成 `path=<仓库相对路径>`，块内是**完整文件内容**：

1. `scripts/check_work_item_uniqueness.py`（或你定的名字；若改名，测试与 workflow 同步）
   命令行必须支持 `--target <ref>`（默认 `origin/main`）与 `--candidate <ref>`（默认 `HEAD`），并能被这样调用：`python scripts/check_work_item_uniqueness.py --target origin/main --candidate HEAD`。
   要求：
   - 只读，不改树、不写文件（除 stdout）。
   - 判定对象是"候选提交的树 vs 目标 ref 当前指向的树"，两棵树都通过 `git ls-tree`/`git cat-file` 读，不依赖工作区。
   - 目标 ref 解析不到 → `exit 2`（INCOMPLETE），不许当 0。
   - 输出带 `candidate=<sha>` 与 `target=<sha>` 两个实测 SHA（"精确 head"这一行靠它证明），再给 `KEY=VALUE` 汇总与逐条明细。
   - 既有目录下的新增文件必须放行；只有"候选新增了一个目录，而该目录名在目标树里已存在"才是冲突。
   - 与 `check_traceability.py` 的 T-04 互补：T-04 查单棵树内部重复，你查跨树占用。

2. `tests/test_check_work_item_uniqueness.py`（unittest，标准库，自建临时 git 仓库）
   至少覆盖：正例（新 ID 接受）、负例（目标上已占用 → 拒绝，断言退出码与消息）、增量（既有目录下加文件 → 接受）、精确 head（同一 candidate ref 在两个不同 target 状态下结论不同；证明结论跟 target 走，不跟分支自己的 base 走）、竞态（两个 candidate ref 引入同一 ID 的串行判定，第二个必须红）。回归语义（不误报既有 110 个 manifest）也要有一个用例：对真实仓库跑 `--target HEAD --candidate HEAD` 必须 PASS（自比较不产生冲突）。

3. `.github/workflows/<你定的名字>.yml`
   要求：
   - job 名与文件里必须有注释解释**串行化机制**：为什么两个 PR 不能同时对陈旧 base 通过。逐条写清"这条防线由谁强制"。
   - 如果依赖平台设置（merge queue / strict up-to-date / branch protection 必需上下文），必须写成显式的依赖项并标注**当前未验证/未启用**，同时给出树内已强制的部分。不许写成"已加入 branch protection"。
   - `runs-on: ubuntu-latest`、`timeout-minutes`、`permissions` 最小化、checkout 需要 `fetch-depth: 0`（要读两个 ref 的历史）。
   - 若是硬门禁，注释里写"今天在 main 上绿，且必须保持绿"。
   - 事件触发要说明为什么选它：`pull_request` 的 base 变化不会触发新 run，这是"陈旧 base"漏洞的一半，你必须正面处理这个事实。

4. `14-ai-development/work-items/AID-2026-261/manifest.yaml`（完整替换骨架；必须过 3.6 的 schema 校验，`base_commit_sha: a7a252eb670b31066a0ffea35dc28cbe6ef5b836`，`status: DISPATCHED`，`id_status: PROVISIONAL`，`issue_refs: ["#1341", "#1331"]`，`implementation.status: IMPLEMENTED`，`implementation.files_changed` 与 `tests` 写实际文件与测试命令，实测数字用占位）

5. `14-ai-development/work-items/AID-2026-261/evidence.md`
   必须包含 **8 行证据表**（契约/串行化/正例/负例/增量/竞态/精确 head/回归），每行写"证明方式 + 复现命令 + 期望输出"。串行化那一行必须是论证，不是"加了 concurrency 字段"。frontmatter 用 3.8 模板，`bilingual_counterpart` 全 `null`。

6. `14-ai-development/work-items/AID-2026-261/session-evidence.md`（3.9 模板 + 五个小节）

7. `14-ai-development/work-items/INDEX.md` 的那一行（只给这一行，我负责替换骨架行）

另外给一段 `## 串行化论证` 的纯文本（不进文件，直接放回复里），用 3–8 条把"为什么两个 PR 不能同时对陈旧 base 通过"讲完，并明确标出残余窗口与它由谁关闭。

---

## 5. 占位符约定

只允许这几种占位，格式 `<FILL:名字>`，我回填实测值：

- `<FILL:test_count>`（unittest 用例数）
- `<FILL:test_output_summary>`（如 `Ran 12 tests in 0.4s / OK`）
- `<FILL:checker_output_positive>`、`<FILL:checker_output_negative>`、`<FILL:checker_output_race>`（真实 stdout 片段）
- `<FILL:head_sha>`、`<FILL:pr_number>`、`<FILL:prompt_sha256>`、`<FILL:prompt_bytes>`
- `<FILL:run_date>`（形如 `2026-11-27T05:00:00Z`）
- `<FILL:workitem_dirs>`、`<FILL:manifest_count>`（回填时的实测计数）

**不要**用占位符代替设计内容或代码逻辑。凡是你自己能定的（路径、job 名、函数名、消息文案、测试断言），一律写死。

## 6. 输出格式（严格执行）

- 每个文件一个围栏块，信息行 `path=...`，块内是完整文件内容，不要 `+`/`-` diff 前缀，不要省略号，不要"其余同上"。
- 顺序按第 4 节 1→7，最后给 `## 串行化论证`。
- 不要输出解释性前言、不要复述本提示词、不要问问题。第一行就是第一个围栏块。
