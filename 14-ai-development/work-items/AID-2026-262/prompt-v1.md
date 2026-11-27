---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-262/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Snapshot of the dispatching instruction as received by the implementation session. Not an authored prompt; provenance is NOT_VERIFIED."
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
      - "prompt-snapshot"
      - "merge-broker"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Prompt snapshot — AID-2026-262

Snapshot of the instruction this implementation session received, reproduced as
the dispatched task text. It is a snapshot, not an authored prompt: the text
originates from the dispatching session and its provenance is `NOT_VERIFIED`.

---

你是实现子 Agent IMPL-B。目标 Issue #1341（Option (d)：串行化、合并时刻的 work-item 唯一性门禁）。

## 权威事实（协调层实测）

- `AID-2026-255`、`AID-2026-242`、`AID-2026-261` 全部不可用：242 已被 PR #1297 合入 main；261 属另一条线的未 push 本地 worktree（其 HEAD `a7a252eb` 实为 `Merge PR #1364 — AID-2026-251 Work Item manifest schema`，与 261 无关）；255 是我方误分配。
- 唯一正确编号：`AID-2026-262`，分支名 `work-item/aid-2026-262-merge-broker`，基于 `origin/main`。
- GitHub REST API 配额已耗尽（403），全程只用 git；PR 创建放最后，403 就记录 `PR_NOT_CREATED_RATE_LIMIT`。
- 不要碰主工作树 `D:\code\AiMemoryBrainArchitecture`。

## 方案（Owner 已定，不得改写）

新文件 `.github/workflows/work-item-merge-broker.yml`，语义 = serialized merge broker：

- 触发 `pull_request` 的 `labeled`（标签 `merge-ready`）+ `workflow_dispatch`
- `concurrency: { group: main-work-item-merge-broker, cancel-in-progress: false }`
- `runs-on: ubuntu-latest`，无自托管
- 权限最小化：该 workflow 才有 `contents: write`、`pull-requests: write`
- 每次运行重新枚举所有 open 且带 `merge-ready` 的 PR，逐个处理（不复用事件旧快照）
- 每个 PR 重新读最新 main SHA、head SHA、required check-runs、merge candidate
- 对候选 merge tree 计算新增 work-item 目录集合：新目录 ID 已在最新 main → 拒绝；目录已存在但候选只增文件 → 允许
- 通过后用 merge API 传精确 `sha=<已验证 head SHA>`
- 若无法在本 PR 内强制「main 只能经 broker 更新」的排他边界，必须在 workflow 注释、工作项 evidence 与 PR body 中明确写 `BROKER_SERIALIZATION_UNPROVEN`，不得宣称串行保证成立

## 工作流

1. 建 worktree `D:\code\_aimb\wt-a262`，分支 `work-item/aid-2026-262-merge-broker`，基于 `origin/main`。
2. 读 Issue #1331 全部评论与 #1341 正文，把 Option (d) 完整规格与 8 行验收证据表落到 `AID-2026-262/evidence.md`。
3. 实现判定脚本，broker workflow 调用它。
4. 单测覆盖：新目录未占用→0、新目录已占用→1、既有目录仅增文件→0、两候选同 ID 先后求值→第二个在更新后 base 上返回 1、非法树→2。
5. 建 `14-ai-development/work-items/AID-2026-262/`（manifest.yaml、prompt-v1.md、session-evidence.md、evidence.md），更新 `INDEX.md`。
6. 本地跑新增单测 + `python scripts/check_traceability.py --index-only`，保存原始输出。
7. push 分支（不 force）；尝试开 draft PR（标题 `feat(gov): serialized merge-time work-item uniqueness broker (AID-2026-262)`，body 含 `AI-assisted work: YES`、`Work Item ID: AID-2026-262`、`Session evidence reference(s): 14-ai-development/work-items/AID-2026-262/session-evidence.md`、`Related issues: #1331, #1341`，并逐条列出 8 行验收中尚未取得的行，尤其 serialization 与 race）。
8. 交付报告。

硬约束：不新增 required context、不把 broker 声明成 required check、不改 main 的 branch protection（只能建议）、不合并、不关闭 Issue、未实测不写 PASS。

---

## Deviation recorded by the implementation session

Step 3 asked for a new judgement script. `main` already carries
`scripts/ci/check_work_item_uniqueness.py` (AID-2026-279, merged as PR #1372)
with exactly that contract, wired into the required GOV-DOC-002 job. Adding a
second checker would recreate the duplicate-identity defect this issue exists to
remove, and overwriting the merged file would break the wired caller. The broker
therefore calls the merged checker and adds the missing half — the serialized
merge boundary — plus composition tests. The deviation is recorded here, in
`manifest.yaml` (`scope.deviation`) and in `evidence.md` section 1.
