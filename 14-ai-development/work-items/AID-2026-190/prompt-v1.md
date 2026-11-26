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
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task scope, not a full raw transcript; the session identifier and the verbatim model input stream were not captured."
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
      - "gate"
      - "hygiene"
      - "silent-skip"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Prompt snapshot — AID-2026-190

**Scope snapshot, not a verbatim raw capture.** This records the task as dispatched to the
implementing session: a unit brief plus a shared brief that every unit in the batch received.
The full model input stream and the session identifier were not captured.

## Unit brief as received (verbatim, `unit-hygiene.md`)

```
# UNIT hygiene · 静默跳过却打印 passed

仓库：`D:\code\AiMemoryBrainArchitecture`。worktree：`D:\code\wt-hygiene`，分支 `fix/2026-11-27-hygiene-silent-skip`。

## 缺陷
`check_repository_hygiene.py:968-979`：无 `--base/--head` 时**静默跳过**新文件准入，仍打印同一句 `Repository hygiene check passed`。CI 对同一脚本正是这么跑两次的（其中一次无 base/head）。

## 要做
1. 无 `--base/--head` 时：**不得**打印 `passed`。改为打印 `SKIPPED (new-file admission requires --base and --head)` 并 **exit 2**；或在 CI 里补上 base/head 参数使检查真正执行。二选一，给出理由。
2. 若选"CI 补参数"：改 workflow 传入 `--base origin/${{ github.base_ref }} --head ${{ github.sha }}`，并确认 job 数/名不变、16 个 context 不变。
3. 补测试：无参数 → 非零退出且输出含 `SKIPPED`；有参数 → 正常判定。
4. 跑一遍 `check_repository_hygiene.py` 两种调用，记录输出与退出码。

## 禁止
不改 `--base/--head` 存在时的判定逻辑、不新增 required context。
```

## Shared brief as received (shape only, `fix-brief-common.md`)

The batch brief fixed the working directory and branch, the credential source, the work-item
registration set, the block-style metadata shape, the PR body fields, and the merge discipline:
sixteen required contexts completed and successful on the exact head, `behind` 0 at merge time,
merge method `merge`, and a per-file blob comparison against `origin/main` after the merge. It
also recorded that both 9router routes were returning 429, so this batch runs on
`opencode-go/deepseek-v4.1-flash`.

## The two branches the brief left open, and where this work item went

The brief offered a choice and required a reason. The choice taken is the script-side refusal:
without `--base/--head` the checker exits 2 with `SKIPPED`, and the head-tree half of the same
script stays reachable behind an explicit `--head-tree-only` flag. Passing the range in CI alone
was rejected because it repairs the one caller instead of the output contract, leaving every
other caller able to print a pass for admission that never ran — including the 27 self-tests that
call the script without a range. The full argument is in `manifest.yaml` under `decision:`.

The CI half of the brief was still implemented, because after the refusal the job's unqualified
step would go red: the duplicated invocation pair collapses to one step that supplies the range.
Job count, job id, job display name and the sixteen declared contexts are unchanged.
