---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-268/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the actual AI input and visible output for preparation of the ledger hotfix. It does not claim that a PR was created, CI was run, or the change was merged."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "AI session evidence for the AID-2026-268 manifest-pin ledger hotfix"
    canonical_scope_id: "ai-development/aid-2026-268-ledger-hotfix-session"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "ledger"
      - "session-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Session evidence — AID-2026-268 ledger hotfix

Attribution: user-authorized operator (delegated by account owner)

## Session role / use case

Prepare a narrowly scoped correction to the manifest blob-pin ledger in `scripts/ci/manifest-pin-ledger.md`.

The correction changes the two AID-2026-101 and AID-2026-102 `repin_commit` values from the PR-branch commit `6045af65fcc2e89d1895e09ed666af4d737203bf` to the squash commit `2ab66153dbcdd8a8f2d68d234914751a748a8f74`, which is the commit actually present in main history.

The purpose is to make the ledger's recorded repin commit satisfy its own ancestor rule. The checker semantics, manifest pin values, and AID-2026-261 sentinel declarations are not to be changed.

This session also reassesses the permitted delivery route after the user measured a change in the mainline work-item uniqueness checker. The intended carrier is a real AI-assisted PR with a new session-evidence file under the existing AID-2026-268 work-item directory.

## Actual AI input

The user supplied the following actual instructions and evidence in this conversation:

> 重要反转：work-item uniqueness 规则在 main 上已经改了，新增路径不再被拒。ledger hotfix 可以走真实 PR，请你改判 Q2

The user reported the following measured behavior:

> main 上现在这一版是 16744 字节 / 445 行，只校验 `ROOT/<AID|FIX>/manifest.yaml` 的声明唯一性，**没有 `new_paths` 概念**。

The user supplied this isolated-worktree probe result:

```text
python scripts/ci/check_work_item_uniqueness.py --base f0843a8f… --head <probe>
rc=0
WORK-ITEM UNIQUENESS: PASS (candidate_ids=167 target_ids=167 introduced=0 shared=167 duplicate_declarations=0)
```

The user explicitly requested the following deliverables:

> 请给**完整文件正文**（要能被 `scripts/governance/session_evidence/validate.py` 解析；它要求 `Session role / use case`、`Actual AI input`、`AI-visible output` 三节，我按你给的原文落盘）。

> 请给 body（按仓库模板）：Work Item ID、Related issue(s)（#1349）、AI-assisted work: YES、Session evidence reference(s) 指向上面的路径、Base/Head SHA 的写法（我会填实际值）、PR-GOVERNANCE-001 状态。

The user also requested a correction to the earlier #1349 hand-off that said the patch was awaiting a non-AI maintainer, and asked who should perform the merge if the required checks pass.

The user identified the intended change as the two-line `repin_commit` correction already tested locally. No request was made to alter the checker, baseline, or either AID-2026-261 sentinel.

## AI-visible output

The assistant's actual visible ruling in this conversation included:

> 批准路线：在 `AID-2026-268` 下新增本次真实 session evidence，连同 ledger 两行修正提交独立 PR，关联 #1349。

The assistant also stated:

> 证据必须忠实记录本次实际 AI 输入和输出，不能把尚未发生的操作写成已完成。

The assistant inspected the current mainline session-evidence validator, the AID-2026-268 manifest and existing session evidence, the repository pull-request template, the current #1349 issue body and comments, and the current manifest-pin ledger. This inspection established that the validator requires the PR-level evidence reference to resolve to a manifest `session_evidence` entry and that the evidence entry itself must satisfy the required manifest fields.

No PR creation, branch push, local file write, CI execution, or merge is claimed by this record.
