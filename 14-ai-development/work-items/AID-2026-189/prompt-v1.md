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
        - "14-ai-development/work-items/AID-2026-189/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
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
      - "ci"
      - "cache"
      - "concurrency"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Prompt snapshot — AID-2026-189

**Scope snapshot, not a verbatim raw capture.** This file records the task as it was
dispatched to the implementing session. The dispatching session supplied a worker
contract; the brief below is the whole of the instruction that selected the scope, the
number band and the prohibitions.

## Task brief as received (verbatim)

```
你是修复 worker（因 `9router_hermes` 上游 429，本单元降级到 deepseek-v4.1-flash）。

## 工作目录（固定，不要碰其它目录）
`D:\code\wt-ci2`，分支 `fix/2026-11-26-ci-leftovers`。

## 事实（已实测）
1. AID-115（PR #1322，merge `ac301e09`）已给 8 个 required workflow 加 `concurrency`，
   给 4 个 Rust job 加 `Swatinem/rust-cache@v2`。
2. 回归：`gates.yml` 的 fmt job 也被加了 `rust-cache` + `Record resolved Rust
   toolchain version`，但它只跑 `cargo fmt --all -- --check`，不编译，缓存永远不可能
   命中（修复前 8s，合并后出现过 21s）。
3. 漏改：`h-applied` 与 `publication-protocol` 是「话题分支 push + main pull_request」
   双触发，两处分支真实存在，无 concurrency。
4. `repository-hygiene.yml:149-152` 会让"declared 但未产出"的 context 判红；
   `check_declared_check_contexts.py` 是"一 job 一 context"。

## 要做（只这 3 件）
A) 在 `gates.yml` 的 fmt job 删除 `Record resolved Rust toolchain version` step 与
   `Cache Rust dependencies and build artifacts`（`Swatinem/rust-cache@v2`）step。
   其余不动。不要动 clippy / doctest / rust-workspace-test 的缓存。
B) 给 `h-applied-delivery-evidence-conformance.yml` 与
   `publication-protocol-reference-model.yml` 加
   `concurrency.group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}`
   + `cancel-in-progress: true`。必须用 head SHA。加完确认 job 数与 job 名未变。
C) 只记录、不修：
   - `ready_for_review` 造成的已完成运行二次派发；含该触发的 4 个 workflow 实测 4/4 双跑。
     标 `DEFERRED_TO_OWNER`，写根因与至少两种候选修法。
   - 两个 required context 逐字节重复（`cargo test --workspace --doc`、
     `check_fmt.py --expect "$GITHUB_SHA"`）。合并会让 declared context 永不到达并判红。
     只记录。

## 禁止
不合并 job、不改 job 名、不改 `check_declared_check_contexts.py` 语义、不动
`fetch-depth`、不删 required context、不关 Issue、不改分支保护、不 force push。
```

## Constraints carried into execution

- Work only inside `D:\code\wt-ci2`; never touch another checkout.
- Do not delete another session's files: a non-empty work tree is reported, not cleaned.
- Fixed number band: `AID-2026-189` after 170/172/173 (merged) and 183/186/188 (open) were
  observed occupied; no INDEX `max+1` allocation.
- Every required context must be green on the exact head before merge; merge method `merge`;
  blob verified after merge.
