---
document_metadata:
  domain: ai-development
  role: reference
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-281/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Structured task capture; source provenance is recorded as NOT_VERIFIED in the adjacent manifest."
    usage_status: Active
    modification_status: Active-Modified
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

# 输出契约

只输出编辑块，第一个字符就是 `===FILE`。禁止计划、确认、摘要、"我会…"。本轮的块会被脚本逐字节套用，OLD 段必须与工作树现有字节完全一致。

```
===FILE: <路径>|REPLACE===
---OLD---
<逐字节原文>
---NEW---
<替换后>
===END===
```
新建文件 `|CREATE`，正文直接跟在头后（不需要 `---NEW---` 标记）。

# 本轮任务：补齐 AID-2026-281 的注册材料，让 `check_document_management.py --require-changed` 与 `check_bilingual_docs.py` 转绿

## 已实测的事实（直接用，不要改数字）

- 分支 HEAD `ce3d7cb8`，基于 main `788fbc011877a14976fc0a974ffe2e013dd9991b`。
- 已改动文件（`git diff --numstat`）：
  - `scripts/check_document_management.py` 3/3（M-02 两条字符串）
  - `docs/en/09-security-governance/README.md` 1/1
  - `docs/zh-CN/09-security-governance/README.md` 2/2
  - `05-memory-runtime/README.md` 2/0
  - `docs/en/05-memory-runtime/README.md` 2/0
  - `docs/zh-CN/05-memory-runtime/README.md` 2/0
  - `14-ai-development/work-items/AID-2026-113/restore-evidence.md` 1/1
  - `docs/en/14-ai-development/work-items/AID-2026-113/restore-evidence.md` 1/1
  - `docs/zh-CN/14-ai-development/work-items/AID-2026-113/restore-evidence.md` 1/1
- `check_document_management.py --require-changed origin/main` 现在 **exit 1**，两条错误：
  - `DM-01 missing document_metadata block: 14-ai-development/work-items/AID-2026-281/evidence.md`
  - `DM-01 missing document_metadata block: 14-ai-development/work-items/AID-2026-281/evidence-05-index.md`
- `check_bilingual_docs.py` 现在 **exit 1**，唯一原因：`Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED': 05-memory-runtime/README.md`。基线 `77 frozen, 0 new gaps`。
- `check_source_revision_pointers.py`：`POINTERS=50 ACCURATE=16 STALE=8 DEREFERENCED=26 BAD_DEREFERENCE=0 NON_BLOB_REFERENCE=6 BAD=14`，**本轮不改它，不接线**。
- 已生效的裁决：指针 14 条登记为债不改；AID-113 保留 `Verified` 但 note 收窄；05 README 降为索引。

## 要交付的块

### 1. `14-ai-development/work-items/AID-2026-281/evidence.md`（整份重写，含 frontmatter）

我先前已生成一份无 frontmatter 的骨架，内容如下（用 `---OLD---` 整份替换，或直接给 CREATE 覆盖；两者选一，注意 CREATE 遇已存在文件会被拒，所以请用 REPLACE + 完整 OLD 段）。骨架正文：

```
# AID-2026-281 — Evidence and declared exceptions

## 1. 基线

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base commit: `788fbc011877a14976fc0a974ffe2e013dd9991b`
- `check_source_revision_pointers.py` baseline:
  - POINTERS=50
  - ACCURATE=16
  - STALE=8
  - DEREFERENCED=26
  - BAD_DEREFERENCE=0
  - NON_BLOB_REFERENCE=6
  - BAD=14
  - exit=1
- The pointer checker is not connected to any workflow.
- No checker relaxation or workflow integration is authorized by this work item.

## 2. RC-1 — M-02 的文案对齐

## 3. RC-2 — Security Governance README

## 4. Source revision pointer debt

## 5. AID-2026-113
```

（骨架里各节正文是你上一轮写的，若你需要保留就按你的原意重写；**只要最终字节完整**。）

frontmatter 用这个形状（`canonical_status: Non-Canonical`，因此不需要登记 canonical scope；工作记录不在 `NORMATIVE_ROOTS` 内，因此 `bilingual_counterpart` 三个字段全为 null）：

```yaml
---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-281/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "<一句话，写清每个数字都是本工作树实测、无 CI/合并声明>"
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

**硬要求**：`approval_scope`、`evidence_reference`、`supersession`、`archival` 必须是块式 YAML（不得出现 `{` 开头的流式写法，解析器会 ParseError）。

### 2. `14-ai-development/work-items/AID-2026-281/evidence-05-index.md`（整份替换，同上 frontmatter 形状，`role: work-record`）

正文用你上一轮给的那份（角色对照表 + 裁决 + 未删除证明），把 `TODO_SECTION_COUNT_ROOT` / `TODO_SECTION_COUNT_OVERVIEW` 换成 `TODO`（执行方实测填）。

### 3. `14-ai-development/work-items/AID-2026-281/manifest.yaml`（整份替换，去掉全部 TODO）

按下面这份**真实通过门禁的同仓样例**的键集与粒度写，字段值换成本工作项：

```yaml
work_item_id: AID-2026-199
title: >-
  Make the three gate helpers fail closed: index membership refuses an absent directory side
  or index, both workflow readers cover .yaml, and a comment no longer supplies a context, a
  discovery root or test reachability
class: CI/GOVERNANCE
risk: R1
risk_rationale: >-
  Three helper edits plus their tests. No job is added, renamed, merged or removed; the sixteen
  declared contexts and the sixteen produced contexts are unchanged; no required context, index
  row or baseline entry is added or deleted. Every new failing branch fires only on an input that
  previously produced a silent pass, and the real tree stays green at the same counts it reported
  before the change.
status: DISPATCHED
id_status: PROVISIONAL
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED
acceptance_authority: NOT_ASSIGNED
attribution: user-authorized operator (delegated by account owner)
date: 2026-11-27
repository: oahcom/AiMemoryBrainArchitecture
base_branch: main
base_commit_sha: 9dc98a526703917bd28862f97f75054beacf1388
prompt_status: NOT_RECORDED
prompt_provenance: DISPATCHED_TASK_FILE
identifier_allocation:
  id_status: PROVISIONAL
  observed_main: 2f4f4118bd2c2d8e43a23975f667deeb06553f3c
  assigned_id: AID-2026-199
  allocation_rule: >-
    First allocation was AID-2026-192: at the time, pull-request titles and branch names reached
    AID-2026-191, 190 and 191 were carried by pull requests still open, and 192 appeared in no
    title, no branch name (1048 refs through git/matching-refs) and no path in this tree. Before
    this branch could be merged, main advanced to 9dc98a52 carrying its own AID-2026-192 and
    AID-2026-197/AID-2026-198, which made the branch conflict add/add on every AID-2026-192
    path. The recheck rule fired: this work item was renumbered to AID-2026-199, the first
    number outside the main tree (highest 198), the open pull requests (190, 191, 192, 193, 198)
    and the remote branch names, in one push that moved every path and reference. No INDEX
    maximum plus one was used.
  observed_occupied: [170, 172, 173, 183, 186, 188, 189, 190, 191, 192, 193, 197, 198]
  recheck_rule: >-
    Immediately before merge, re-read open pull requests, remote branches and the main tree for
    AID-2026-199; if occupied, take the next free number and update every path and reference in
    the same push.
scope:
  objective: >-
    Close the three false-PASS branches the unit brief names: an index-membership check that
    answered "no violations" when either side of the relation was absent, two workflow readers
    that could not see a `.yaml` workflow or a `jobs:` header with a trailing comment, and a
    reachability rule that counted a test name mentioned in a comment as executed.
  changes:
    - path: "scripts/ci/check_repository_hygiene.py"
      detail: >-
        `check_index_membership` raises `RuntimeError` -- the file's exit-2 channel -- instead of
        returning `[]` when no work-item directory is found, and again when INDEX.md is absent
        from the head tree. `CHECK_VERSION` moves to 2026-11-27.2 because the rule set changed.
    - path: "scripts/check_declared_check_contexts.py"
      detail: >-
        Adds `strip_yaml_comment` / `strip_yaml_comments` and applies them inside
        `produced_contexts`, so `jobs:  # comment` is read as the jobs header and a commented-out
        job line produces nothing. Workflow discovery globs `*.yml` and `*.yaml`.
    - path: "scripts/ci/check_test_reachability.py"
      detail: >-
        Workflow discovery globs `*.yml` and `*.yaml`; both branches (Rule B substring match and
        the `discover -s` extraction) read a comment-stripped view of each workflow through the
        existing `strip_comment` helper instead of the raw file.
    - path: "scripts/test_check_repository_hygiene.py"
      detail: >-
        Adds the two fail-closed cases and a `with_index` fixture switch; the shared `commit`
        helper now carries one work-item directory and an INDEX.md row for every directory the
        fixture contains, because the membership check no longer passes without them.
    - path: "scripts/test_check_declared_check_contexts.py"
      detail: >-
        Adds three cases: a commented `jobs:` header still produces contexts, a job named only in
        a comment is not produced, and a `.yaml` workflow is read.
    - path: "scripts/ci/test_check_test_reachability.py"
      detail: >-
        Adds three cases: a test named only in a comment is unreachable, a `discover` command in
        a comment is not a discovery root, and a `.yaml` workflow reaches tests and wires gates.
  untouched:
    - "every job id and job display name, in every workflow"
    - "the sixteen declared required contexts and the sixteen produced contexts"
    - "scripts/ci/baselines/gate-wiring.txt (3 unwired, 3 baselined, unchanged)"
    - "every other checker and every document outside this work item"
    - "the judgement in each checker: no threshold was relaxed, no violation class removed"
evidence:
  record: 14-ai-development/work-items/AID-2026-199/evidence.md
  mirrors:
    - docs/en/14-ai-development/work-items/AID-2026-199/evidence.md
    - docs/zh-CN/14-ai-development/work-items/AID-2026-199/evidence.md
  measured_at: 2f4f4118bd2c2d8e43a23975f667deeb06553f3c
  measured_at_note: "Defect measurements (sections 2-4) at 2f4f4118; suite counts at 9dc98a52; gate counts at each merge, named by SHA (3b2cd3e1 over main 76684cb2, 980e54d9 over main 980e54d9)"
  measurements:
    index_membership_no_directories_before: "returns [] -> checker exit 0"
    index_membership_no_directories_after: "RuntimeError -> checker exit 2"
    index_membership_no_index_before: "returns [] -> checker exit 0"
    index_membership_no_index_after: "RuntimeError -> checker exit 2"
    produced_contexts_jobs_comment_before: 0
    produced_contexts_jobs_comment_after: 3
    declared_checker_yaml_only_workflow_before: "exit 2 (INCOMPLETE: no workflows under .github/workflows)"
    declared_checker_yaml_only_workflow_after: "exit 0"
    reachability_commented_test_name_before: "exit 0 (silent pass)"
    reachability_commented_test_name_after: "exit 1, pkg/test_x.py named"
    declared_contexts_before_after: "16 declared / 16 produced, unchanged"
    index_membership_counts_before_after: "both sides equal and exit 0 in every run, with exactly one directory and one row more than the main merged in: 110 / 110 at main 9dc98a52, 114 / 114 at 3b2cd3e1, 115 / 115 at 980e54d9"
    reachability_totals_before_after: "0 unreachable on both sides; 18 gate scripts / 3 unwired / 3 baselined on both sides; 66 test files at both 9dc98a52 and 3b2cd3e1"
    checker_version_before: "2026-11-27.1 (the unqualified-run contract change, already on main)"
    checker_version_after: "2026-11-27.2 (this rule change)"
    tests_hygiene_before_after: "101 -> 103 (1 skipped both sides)"
    tests_reachability_before_after: "24 -> 27"
    tests_declared_before_after: "13 -> 16"
  local_runs:
    - command: python scripts/test_check_repository_hygiene.py
      result: "Ran 103 tests / OK (skipped=1) / exit 0"
    - command: python scripts/ci/test_check_test_reachability.py
      result: "Ran 27 tests / OK / exit 0"
    - command: (cd scripts && python -m unittest test_check_declared_check_contexts)
      result: "Ran 16 tests / OK / exit 0"
    - command: python scripts/ci/check_repository_hygiene.py --head-tree-only
      result: "directories=115 linked=115 with this work item (114 / 114 on main 980e54d9, 113 / 113 on main 76684cb2); exit 0; new-file admission reported SKIPPED, as the 2026-11-27.1 contract requires"
    - command: python scripts/ci/check_test_reachability.py
      result: "66 test files / 66 reachable / exit 0"
    - command: python -c "... check_declared_check_contexts.main(root, declared_contexts(...))"
      result: "16 declared, all produced; exit 0 (the protected side injected, no network call)"
  not_measured:
    - No CI context result is claimed at any SHA in this document
    - No merge SHA is claimed
    - The live branch-protection payload is not read here; the protected side is injected from the declaration
    - No claim is made about any workflow this change does not touch
implementation:
  status: NOT_STARTED
  pull_request: PENDING
  merge_commit_sha: NOT_MERGED
session_evidence:
  - role: "IMPLEMENTATION_SESSION"
    issue_refs:
      - "#1212"
    implementing_ai_session: "opencode-go/deepseek-v4.1-flash"
    executed_prompt_snapshot_file: "14-ai-development/work-items/AID-2026-199/prompt-v1.md"
    executed_prompt_sha256: "3522e9ee41f8372aabd74292e4bbccd842543d77887145facb8cb05017536b1c"
    executed_prompt_bytes: 7965
    executed_prompt_provenance: "NOT_VERIFIED"
    session_reference_status: "NOT_RECORDED"
    session_evidence_ref: "14-ai-development/work-items/AID-2026-199/session-evidence.md"
non_goals:
  - Changing any required context name, count or protection entry
  - Adding, renaming, merging or removing any job
  - Relaxing any judgement, threshold or violation class in the three checkers
  - Adding a gate-wiring baseline entry instead of wiring a new gate
  - Repairing any checker this unit did not name
notes:
  - >-
    This work item was allocated as AID-2026-192 and renumbered to AID-2026-199 before merge.
    Main advanced from 2f4f4118 to 9dc98a52 while the branch was in review, and that main
    carries its own AID-2026-192 (plus 197 and 198), so the pull request went `dirty` with
    add/add conflicts on every AID-2026-192 path and GitHub created no check runs for it. The
    renumber moved all three directory trees and every reference in one commit; the prompt
    snapshot digest in this manifest and in the INDEX row was recomputed because the snapshot
    carries its own path. `observed_main` and `evidence.measured_at` still name 2f4f4118, the
    tree every measurement in evidence.md was taken on.
  - >-
    The two fail-closed branches were measured against the pre-fix file taken from origin/main,
    not asserted from reading: the old function returned `[]` for a tree with no work-item
    directory, and the old checker printed "Repository hygiene check passed" for it.
  - >-
    Reverting each fix in isolation makes exactly the new tests fail and nothing else: without
    comment stripping the declared-contexts suite fails the commented-header case, without the
    `.yaml` glob both readers fail their `.yaml` case, and without comment stripping in Rule B
    the commented-name case passes again. The three reverts are recorded in evidence.md.
  - >-
    The shared hydration fixture in scripts/test_check_repository_hygiene.py now writes one
    work-item directory and an INDEX.md row for it by default. That is not a case being
    weakened: the fixture trees previously relied on the very silent pass this change removes,
    so without both sides they would have gone red on an unrelated check.
carrier:
  branch: fix/2026-11-27-gates-b
  pull_request: null
  merge_sha: null
  merge_method: merge
  required_contexts: "to be recorded from the pull request head; none claimed here"
  merge_authorization: >-
    Only after all required contexts succeed on the exact final PR head and branch freshness is
    rechecked.
review:
  status: NOT_ASSIGNED
  independent_reviewer: NOT_ASSIGNED
  natural_person_owner_acceptance: NOT_RECORDED
acceptance:
  gate: PENDING_CI

```

### 4. `14-ai-development/work-items/AID-2026-281/session-evidence.md`（CREATE）

三节必备：`# Session role / use case`、`# Actual AI input`、`# AI-visible output`，同样 frontmatter 形状（`role: work-record`）。

### 5. `14-ai-development/work-items/INDEX.md`（REPLACE）

表头是：
```
| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
```
在表体最后一行之后追加一行 AID-2026-281。表体最后一行现在是：

```
| [AID-2026-192](AID-2026-192/manifest.yaml) | Correct a stale count pair and an addition error in the governance record, and grade three inherited execution fields | USER-PRINCIPAL-DELEGATED | DOC/GOVERNANCE / R1 | DRAFT - PR PENDING; `id_status: PROVISIONAL`; GAP-03 26/196 to 27/198 with a tree-pin annotation; AID-2026-111 `## Correction` keeps the recorded 0/36/52 and establishes 0/34/54 over 88 rows; AID-2026-112 `## Provenance correction` marks Exit code / Failed count / Test binaries `INHERITED_ASSUMPTION`; no verdict, blob pin or test changed | `AID-2026-192-PROMPT` - `prompt_status: NOT_RECORDED`; structured snapshot only, no live capture claimed | DOCUMENTATION ONLY - canonical + EN + ZH-CN for both work items; no runtime/validator/schema/test/workflow changes; DM gate INCOMPLETE with zero rule violations (pre-existing backlog) | NOT_ASSIGNED - independent exact-Head review not recorded | PENDING - no Owner acceptance asserted; #1211/#1212 remain OPEN |
```

请给 `---OLD---` = 这一整行，`---NEW---` = 这一行 + 换行 + 你的新行。

## 另外：PR 正文

单独给一个 ```text 代码块（不是 `===FILE` 块），内容是完整 PR 正文，必须含：
- `Related issue(s): #1212`
- `AI-assisted work: YES`
- `Session evidence reference(s): 14-ai-development/work-items/AID-2026-281/session-evidence.md`
- `BILINGUAL-MANIFEST: COMPLETE`
- 以及一段说明：`05-memory-runtime/README.md` 只加了一行导读，EN/ZH 两侧同步加了等价行，语义一致。
