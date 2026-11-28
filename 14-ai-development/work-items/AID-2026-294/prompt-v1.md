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
        - "14-ai-development/work-items/AID-2026-294/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Implementation and CI verification are pending independent review."
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
    canonical_scope_keywords:
      - "merge-queue"
      - "required-context"
      - "document-management"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# MQ-FIX-01 执行包：请裁决并给出逐字交付正文

执行者：实施子 Agent MQ-FIX-01（Windows，PowerShell 5.1，禁用 WSL）。仓库 `D:\code\AiMemoryBrainArchitecture`，独立 worktree `D:\code\_aimb\wt-mq01`，分支 `fix/2026-11-28-docmgmt-merge-group`，base = `origin/main` = `a0500d5196dc990d899d8ccaca2e270faaf29efc`。

权威：`reply-6b07c97e-081917.md` §3（GAP-05：gates.yml = 7 条）与 §4（GAP-07：concurrency 形态），以及编排方追加的「防复发门禁要一并覆盖这两条」。上述两项已按 §3/§4 逐字落地（concurrency 块与你给的 YAML 完全一致；gates.yml 注释 Six→Seven）。

## 一、#1453 删除 merge_group 的取证（已完成的只读取证）

1. `31c1e5d83` = PR #1453 合并提交，标题 `Merge pull request #1453 from oahcom/fix/aid-2026-252-steward-coverage`，body 仅一行 `AID-2026-252 增量修补（非新工单）`。
2. PR #1453 API：title `AID-2026-252 增量修补（非新工单）`，merged=true，head `8faf593a5`，base `159095f3c`。PR body 摘要：实现 steward 采纳机制增量（Issue #266 AC3）——schema 要求 steward、DM-15 扩展、DM-15b 基线、`--list-missing --json` 普查、把普查输出加到既有 `GOV-DOC-002 metadata checks` job（"no new required check name"）、84 份文档补 steward、回归覆盖 DM-15/DM-15b 三条。**全文无 merge_group / merge queue / MG_BASE / 事件接线字样。**
3. `GET /issues/1453/comments` = 0 条；`GET /pulls/1453/comments`（review comments）= 0 条。无任何讨论。
4. PR 分支 52 个 commit message 全文 grep `merge_group|merge queue|MG_BASE` = 0 命中。
5. 文件级证据（`git show <c>:.github/workflows/document-management.yml` 中 `merge_group|MG_BASE` 命中数）：
   - `159095f3c`（#1453 的 base，含 #1436）= 8
   - `1434c1653`（分支早期父提交，早于 #1436）= 0
   - `45bb9cea5`（governance: add steward census and baseline ratchet）= 0
   - `ab9e816bb`（Merge main into steward coverage branch，**第一父 = `da69e43f`，即 #1436 合并提交，该父上命中数 = 8**）= 0
   - `08f19a426` / `34f1d90f2` / `3e21551d9` / `02577a532` / `8faf593a5` = 0
   - `git log -S merge_group --reverse 159095f3c..8faf593a5 -- 该文件` = 空（pickaxe 未追 merge 差异）
6. `git merge-base --is-ancestor da69e43f 8faf593a5` = 0（是祖先）→ 不是基线过旧。
7. `31c1e5d83^1..31c1e5d83` 该文件 diff：删除 `merge_group: types:[checks_requested]` 及 2 行注释；删除 `EVENT_NAME`/`MG_BASE` 环境变量；删除整个 `elif [ "$EVENT_NAME" = "merge_group" ]` 分支（含 base_sha 校验、exit 2、`--base $MG_BASE --head $CANDIDATE_SHA`）；`Validate document metadata` 的 `PR_BASE` 从 `github.event_name == 'merge_group' && ...base_sha || ...pull_request.base.sha` 退回 `github.event.pull_request.base.sha`；同时新增 `Emit steward adoption census` step。

**我的初判（需你裁决并给出报告口径原文）**：`ab9e816bb` 第一父 `da69e43f` 上有 8 处 merge_group/MG_BASE，合并结果树为 0，且没有任何 commit message / PR body / 评论提到删除 → 冲突解决取了分支侧旧版本，属**意外回归**。

请回答：Q1 判定「意外回归」还是「有意删除」，并给出一段可直接抄进报告的结论正文（含证据引用）。Q2 若判为意外回归，恢复接线是否成立；若你认为还有「不该恢复」的理由，直接给出处理口径。

## 二、恢复后的 YAML 现状（当前 worktree 实际文件，139 行）

```yaml
name: Architecture document management gate

# Work-item uniqueness is a shared target-branch invariant, not a
# per-candidate invariant. PRs targeting the same branch must not run this
# gate in independent concurrency groups. Do not cancel a running decision
# when another candidate arrives.
concurrency:
  # Target-branch serialization, not per-candidate. A merge-group candidate has
  # no `pull_request` object, so the old group fell through to `github.ref_name`
  # (`gh-readonly-queue/main/pr-<n>-<sha>`): one group per candidate, which is
  # exactly the split this block exists to prevent. PR events normalize to
  # `refs/heads/<target>` so a PR run and a queue run on the same branch share
  # one group. `queue: max` is required: with `cancel-in-progress: false` the
  # default single pending slot makes a new pending run evict the older one.
  group: >-
    ${{ github.workflow }}-${{
      github.event.pull_request.base.ref
      && format('refs/heads/{0}', github.event.pull_request.base.ref)
      || github.event.merge_group.base_ref
      || github.ref
    }}
  cancel-in-progress: false
  queue: max

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  # `GOV-DOC-002 metadata checks` is required; the queue only reports checks
  # produced by `merge_group`.
  merge_group:
    types: [checks_requested]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  document-management:
    name: GOV-DOC-002 metadata checks
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          # Full history: DM-10 compares the current body against the body at
          # approval.approved_version, which may be any ancestor commit.
          # The uniqueness gate also needs the merge-base and target history.
          fetch-depth: 0

      - name: Self-check the gate
        run: python3 scripts/test_check_document_management.py

      - name: Self-test work-item uniqueness gate
        run: python3 scripts/ci/test_work_item_uniqueness.py

      # A PR's event base SHA can be stale by the time this job executes.
      # Fetch the target branch itself and evaluate the exact generated merge
      # candidate against that fetched commit. Strict branch protection
      # requires a new candidate and a fresh required check after the target
      # advances, closing the interval between this check and a later merge.
      - name: Enforce work-item uniqueness against the current target base
        env:
          EVENT_NAME: ${{ github.event_name }}
          PR_BASE: ${{ github.event.pull_request.base.sha }}
          BASE_REF: ${{ github.event.pull_request.base.ref }}
          MG_BASE: ${{ github.event.merge_group.base_sha }}
          MG_HEAD: ${{ github.event.merge_group.head_sha }}
          PUSH_BEFORE: ${{ github.event.before }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail

          if [ -n "$BASE_REF" ] && [ -n "$PR_BASE" ]; then
            git fetch origin "+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"
            python3 scripts/ci/check_work_item_uniqueness.py \
              --base "refs/remotes/origin/$BASE_REF" \
              --head "$CANDIDATE_SHA"
          elif [ "$EVENT_NAME" = "merge_group" ]; then
            # A merge group carries its own base. There is no branch ref to
            # refresh here, and pull_request.base.sha is never a fallback: an
            # unusable base is INCOMPLETE (2), not a silent pass.
            if ! [[ "$MG_BASE" =~ ^[0-9a-fA-F]{40}$ ]] || [ "$MG_BASE" = "0000000000000000000000000000000000000000" ]; then
              echo "::error::merge_group carries no usable base_sha; the uniqueness verdict is INCOMPLETE"
              exit 2
            fi
            if ! [[ "$MG_HEAD" =~ ^[0-9a-fA-F]{40}$ ]] || [ "$MG_HEAD" = "0000000000000000000000000000000000000000" ]; then
              echo "::error::merge_group carries no usable head_sha; the uniqueness verdict is INCOMPLETE"
              exit 2
            fi
            python3 scripts/ci/check_work_item_uniqueness.py \
              --base "$MG_BASE" \
              --head "$MG_HEAD"
          elif [ -n "$PUSH_BEFORE" ] && [ "$PUSH_BEFORE" != "0000000000000000000000000000000000000000" ]; then
            python3 scripts/ci/check_work_item_uniqueness.py \
              --base "$PUSH_BEFORE" \
              --head "$CANDIDATE_SHA"
          else
            python3 scripts/ci/check_work_item_uniqueness.py
          fi

      - name: Emit steward adoption census (baseline evidence)
        env:
          PR_BASE: ${{ github.event_name == 'merge_group' && github.event.merge_group.base_sha || github.event.pull_request.base.sha }}
        run: |
          PIN="${PR_BASE:-$GITHUB_SHA}"
          set +e
          python3 scripts/check_document_management.py --list-missing --json --pin "$PIN"
          status=$?
          # Exit 2 means the census completed but unclassified governed documents remain.
          if [ "$status" -ne 0 ] && [ "$status" -ne 2 ]; then
            exit "$status"
          fi

      # Every governed file added or modified here must carry metadata. The
      # backlog stays unclassified; it may not grow. Both event kinds are
      # covered: a pull request diffs against its base commit, a direct push
      # diffs against github.event.before (GAP-02).
      - name: Validate document metadata (changed files must be classified)
        env:
          PR_BASE: ${{ github.event_name == 'merge_group' && github.event.merge_group.base_sha || github.event.pull_request.base.sha }}
          PUSH_BEFORE: ${{ github.event.before }}
        run: |
          REF=""
          if [ -n "$PR_BASE" ] && [ "$PR_BASE" != "0000000000000000000000000000000000000000" ]; then
            REF="$PR_BASE"
          elif [ -n "$PUSH_BEFORE" ] && [ "$PUSH_BEFORE" != "0000000000000000000000000000000000000000" ]; then
            REF="$PUSH_BEFORE"
          fi
          if [ -n "$REF" ]; then
            python3 scripts/check_document_management.py --require-changed "$REF" || {
              status=$?
              # Exit 3 is only an empty increment (no paths to verify). A REF
              # selection error is exit 1 and must remain a failed check.
              [ "$status" -eq 3 ] && { echo "::notice::incremental verification not applicable: no changed paths to inspect"; exit 0; }
              exit "$status"
            }
          else
            # No base to diff against (first push of a branch). Whole-tree scan.
            # It now exits 2 (INCOMPLETE) while backlog remains, so this step
            # fails loudly instead of printing PASS over an unclassified tree.
            # It still cannot prove the NEW files are classified: GAP-02.
            python3 scripts/check_document_management.py || {
              status=$?
              # 2 = INCOMPLETE (backlog, no rule violation); 1 = violations.
              [ "$status" -eq 2 ] && echo "::error::No base commit to diff against and the tree still has an adoption backlog (GAP-02). Run this job from a pull request, or classify the backlog."
              exit "$status"
            }
          fi


```

## 三、防复发门禁现状（我起草的脚本，207 行）

```python
#!/usr/bin/env python3
"""Hold every declared required check context to the merge-queue wiring it needs.

Three conditions, each silent when broken:

1. WIRING. A context declared in PR-GOVERNANCE-001.md 搂7 must be produced by a
   workflow that also subscribes to `merge_group`. A context that only runs on
   `pull_request` is never reported on a queue candidate, so the queue silently
   loses that gate and no other check notices: `check_declared_check_contexts.py`
   compares names, not event wiring. #1453 dropped `merge_group` from
   document-management.yml this way; `GOV-DOC-002 metadata checks` left the
   queue with 15/16 and nothing went red.

2. SERIALIZATION. document-management.yml enforces a target-branch invariant,
   so its concurrency group must key off the target branch on every event and
   must not evict pending runs: `cancel-in-progress: false` plus `queue: max`.
   `github.ref_name` is the queue candidate's ref on `merge_group`, which splits
   one branch into one group per candidate.

3. COUNT. A workflow comment stating "<N> required contexts live in this file"
   must state the number of declared contexts that workflow actually produces.

Exit codes:
    0  PASS
    1  VIOLATION   a condition above is false
    2  INCOMPLETE  the declaration or a workflow file cannot be read
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from check_declared_check_contexts import (
    DOC_PATH,
    WORKFLOWS,
    declared_contexts,
    strip_yaml_comments,
    workflow_files,
)

SERIALIZED_WORKFLOW = "document-management.yml"

JOB_ID_RE = re.compile(r"^  ([A-Za-z_][\w-]*):\s*$")
JOB_NAME_RE = re.compile(r"^    name:\s*(.+?)\s*$")
MERGE_GROUP_RE = re.compile(r"^\s+merge_group\s*:")
COUNT_CLAIM_RE = re.compile(r"^#\s*([A-Za-z]+|\d+)\s+required contexts?\b")

NUMBERS = {
    word: value
    for value, word in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve "
        "thirteen fourteen fifteen sixteen".split()
    )
}


def block(lines: list[str], header: str) -> tuple[int, int] | None:
    """Line range (1-based, inclusive header) of a top-level `header:` mapping."""
    for index, line in enumerate(lines):
        if line.rstrip() == header:
            end = index + 1
            while end < len(lines):
                candidate = lines[end]
                if candidate.strip() and not candidate[0].isspace():
                    break
                end += 1
            return index + 1, end
    return None


def job_contexts(text: str) -> dict[str, int]:
    """Job id and display name -> 1-based line number, comments stripped."""
    found: dict[str, int] = {}
    stripped = strip_yaml_comments(text).splitlines()
    bounds = block(stripped, "jobs:")
    if bounds is None:
        return found
    start, end = bounds
    current: str | None = None
    for offset in range(start, end):
        line = stripped[offset]
        job_id = JOB_ID_RE.match(line)
        if job_id:
            current = job_id.group(1)
            found.setdefault(current, offset + 1)
            continue
        job_name = JOB_NAME_RE.match(line)
        if job_name and current is not None:
            found.setdefault(job_name.group(1).strip("'\""), offset + 1)
    return found


def merge_group_line(text: str) -> int | None:
    """Line number of `merge_group:` inside the workflow's `on:` block."""
    stripped = strip_yaml_comments(text).splitlines()
    bounds = block(stripped, "on:")
    if bounds is None:
        return None
    start, end = bounds
    for offset in range(start, end):
        if MERGE_GROUP_RE.match(stripped[offset]):
            return offset + 1
    return None


def count_claims(text: str) -> list[tuple[int, int]]:
    """(line number, claimed count) for every `<N> required contexts` comment."""
    claims = []
    for index, line in enumerate(text.splitlines()):
        match = COUNT_CLAIM_RE.match(line.strip())
        if not match:
            continue
        token = match.group(1).lower()
        if token.isdigit():
            claims.append((index + 1, int(token)))
        elif token in NUMBERS:
            claims.append((index + 1, NUMBERS[token]))
    return claims


def serialization_violations(path: str, text: str) -> list[str]:
    """document-management.yml must serialize by target branch, not candidate."""
    problems = []
    stripped = strip_yaml_comments(text).splitlines()
    bounds = block(stripped, "concurrency:")
    if bounds is None:
        return [f"::error::{path}: has no `concurrency:` block"]
    start, end = bounds
    body = "\n".join(stripped[start - 1:end])

    if not re.search(r"^\s*cancel-in-progress:\s*false\s*$", body, re.MULTILINE):
        problems.append(
            f"::error::{path}:{start}: concurrency must set `cancel-in-progress: false`"
        )
    if not re.search(r"^\s*queue:\s*max\s*$", body, re.MULTILINE):
        problems.append(
            f"::error::{path}:{start}: concurrency must set `queue: max`; with a "
            "single pending slot a new candidate evicts the older pending run"
        )
    if "github.ref_name" in body:
        problems.append(
            f"::error::{path}:{start}: the concurrency group must not use "
            "`github.ref_name`; on merge_group it is the queue candidate ref, "
            "which splits one target branch into one group per candidate"
        )
    if "github.event.merge_group.base_ref" not in body:
        problems.append(
            f"::error::{path}:{start}: the concurrency group must key off "
            "`github.event.merge_group.base_ref` for queue candidates"
        )
    return problems


def main(root: Path | None = None) -> int:
    root = Path(root or ".").resolve()
    doc = root / DOC_PATH
    if not doc.is_file():
        print(f"::error::INCOMPLETE: declaring document is absent: {DOC_PATH}", file=sys.stderr)
        return 2

    doc_text = doc.read_text(encoding="utf-8")
    contexts = declared_contexts(doc_text)
    if contexts is None:
        print(
            f"::error::INCOMPLETE: no declared-context block in {DOC_PATH}",
            file=sys.stderr,
        )
        return 2
    doc_lines = doc_text.splitlines()

    def doc_line(context: str) -> int:
        return next(
            (i + 1 for i, line in enumerate(doc_lines) if line.strip() == context), 0
        )

    workflows = workflow_files(root / WORKFLOWS)
    if not workflows:
        print(f"::error::INCOMPLETE: no workflows under {WORKFLOWS}", file=sys.stderr)
        return 2

    produced: dict[str, list[tuple[str, int, int | None]]] = {}
    violations: list[str] = []

    for path in workflows:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        merge_line = merge_group_line(text)
        for context, line in job_contexts(text).items():
            produced.setdefault(context, []).append((relative, line, merge_line))
        if path.name == SERIALIZED_WORKFLOW:
            violations.extend(serialization_violations(relative, text))

        declared_here = [c for c in contexts if any(p[0] == relative for p in produced.get(c, []))]
        for line, claimed in count_claims(text):
            if claimed != len(declared_here):
                violations.append(
                    f"::error::{relative}:{line}: the comment claims {claimed} required "
                    f"contexts, but this workflow produces {len(declared_here)} of the "
                    f"{len(contexts)} declared in {DOC_PATH}"
                )

    for context in contexts:
        sources = produced.get(context)
        where = f"{DOC_PATH}:{doc_line(context)}"
        if not sources:
            violations.append(
                f"::error::{where}: declares required context {context!r}, but no job "
                f"under {WORKFLOWS} produces it"
            )
            continue
        if any(merge_line is not None for _, _, merge_line in sources):
            continue
        path, line, _ = sources[0]
        violations.append(
            f"::error::{path}:{line}: produces required context {context!r} "
            f"(declared at {where}) but the `on:` block has no `merge_group` entry; "
            "a merge-queue candidate never reports this required context"
        )

    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        print(
            f"REQUIRED CONTEXT MERGE_GROUP WIRING: FAIL ({len(violations)} violation(s))",
            file=sys.stderr,
        )
        return 1

    for context in contexts:
        path, line, merge_line = produced[context][0]
        print(f"OK  {context}  {path}:{line}  merge_group={path}:{merge_line}", file=sys.stderr)
    print(
        f"REQUIRED CONTEXT MERGE_GROUP WIRING: PASS ({len(contexts)} contexts)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))

```

接入：`.github/workflows/repository-hygiene.yml` 中 `Self-check the declared-check-contexts gate` 之后插入两个 step：`Check required contexts are wired to merge_group`（`python3 scripts/check_required_contexts_merge_group.py`）与 `Self-check the merge_group wiring gate`（`cd scripts; python3 -m unittest -v test_check_required_contexts_merge_group`）。自检文件 `scripts/test_check_required_contexts_merge_group.py` 6 个用例全过。

红（origin/main `a0500d519` 干净树 + 仅投放该脚本）：
```text
::error::.github/workflows/document-management.yml:7: concurrency must set `queue: max`; with a single pending slot a new candidate evicts the older pending run
::error::.github/workflows/document-management.yml:7: the concurrency group must not use `github.ref_name`; on merge_group it is the queue candidate ref, which splits one target branch into one group per candidate
::error::.github/workflows/document-management.yml:7: the concurrency group must key off `github.event.merge_group.base_ref` for queue candidates
::error::.github/workflows/gates.yml:56: the comment claims 6 required contexts, but this workflow produces 7 of the 16 declared in 14-ai-development/PR-GOVERNANCE-001.md
::error::.github/workflows/document-management.yml:22: produces required context 'GOV-DOC-002 metadata checks' (declared at 14-ai-development/PR-GOVERNANCE-001.md:270) but the `on:` block has no `merge_group` entry; a merge-queue candidate never reports this required context
REQUIRED CONTEXT MERGE_GROUP WIRING: FAIL (5 violation(s))
exit=1
```

绿（修复分支）：16 行 `OK  <context>  <file>:<line>  merge_group=<file>:<line>` + `REQUIRED CONTEXT MERGE_GROUP WIRING: PASS (16 contexts)`，exit=0。

请回答：Q3 门禁检查项清单是否就是这三条（16 context 的 merge_group 接线；document-management.yml 的 concurrency = cancel-in-progress:false + queue:max + 不得 github.ref_name + 必须 merge_group.base_ref；workflow 注释计数与实际产出的 declared context 数一致）？缺什么、多什么？Q4 `gates.yml` 实际 9 个 job，其中 7 个是 declared required context（`work-item-manifest-schema`、`prompt-commit-trace` 不在 16 条内），所以我把断言实现为「等于该 workflow 产出的 declared context 数（7）」而不是「等于 job 数（9）」，请确认口径或给出正确口径。Q5 门禁接进 `repository-hygiene.yml`（既有入口，与 `check_declared_check_contexts.py` 同 job）是否正确，是否需要同时进别的 workflow？Q6 脚本名与 step 名是否可用，若有更符合仓库惯例的名字直接给最终名。

## 四、其他已知事实（供参考）

- `python scripts/ci/test_work_item_uniqueness.py` 本机 10 tests / 8 failures / 2 errors；干净 `origin/main` 同样 8/2，首个断言 `9009 != 1` → 本机无 `python3` 可执行，属环境差异，非本次改动引入。
- `python scripts/check_declared_check_contexts.py`（带 token）= `declared=16 required=16 produced=48`，`DECLARED CHECK CONTEXTS: PASS`。
- `scripts/test_check_document_management.py` = 376/376 passed（1 skipped）；`scripts/test_check_repository_hygiene.py` = 107 tests OK（skipped=1）。
- `document-management.yml` 的 `else` 兜底分支（无 PR base / 无 merge_group / 无 push before）不带参数调用 `check_work_item_uniqueness.py`，而 #1477 后 `--base/--head` 均 required → 该兜底必然 exit 2；该事件组合对本 workflow 不可达（只有 pull_request / merge_group / push）。是否本次一并处理？

## 五、交付要求

给出一份**逐字可转录**的交付块：1) Q1 结论正文（报告用）；2) `document-management.yml` 最终 `on:` 块、`concurrency:` 块、uniqueness step 的 env + run 分支（若与现状不同，给完整替换文本）；3) 门禁检查项清单（Q3/Q4/Q5/Q6 裁决）；4) 报告 `MQ-FIX-01.md` 的章节骨架与必须写明的结论句。

