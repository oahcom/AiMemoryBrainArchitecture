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
        - "14-ai-development/work-items/AID-2026-191/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Snapshot of the dispatched worker contract as received. It was not authored by the executing session and no prompt digest is claimed as frozen."
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

# AID-2026-191 — dispatched contract snapshot (v1)

Snapshot of the worker contract received by the executing session on 2026-11-27: the unit file's requirement text and the common fix brief's constraints, quoted verbatim. Nothing in the body was rewritten; the premise statements are reproduced as dispatched so that the divergence measured in `evidence.md` section 2 can be checked against the order that produced it.

---

## 派发原文（逐字）

工作目录：`D:\code\wt-reg03`，分支 `fix/2026-11-27-baseline-copies`，基于 main `4326669c`。只在它里面干活，绝不碰 `D:\code\AiMemoryBrainArchitecture`。

缺陷：77 条冻结缺口清单实际被 **7 个文件**承载；AID-172 只给其中 **2 份**加了比较器（`check_baseline_copies_agree()`）。已有一份漂成 **81 条（多 9 / 缺 5）**，`ci-gates-and-ratchets.en.md:420/:516` 引用的 `baseline=81` 就是它。

要做：

1. 全仓枚举所有 77 条清单拷贝（按内容特征：`^\d{3}\.\s` 行块，或含 `bilingual` + 路径列表）。给完整清单：路径 / 行数 / 是否与权威副本逐条相同。
2. **指定唯一权威**：`scripts/ci/baselines/bilingual-docs.txt`（棘轮实际读取的那份）。
3. 扩展 `check_baseline_copies_agree()` 覆盖**全部**拷贝（不只是 2 份），不一致时逐条 `::error::` 打印双向差集 + exit 2。
4. 对已漂移的那份：**不删、不改内容**，把它标注为历史快照（改标题/加 `> HISTORICAL — not a gate input`），并把引用它的文档（`ci-gates-and-ratchets.en.md/.zh-CN.md`）改成引用权威副本 + 说明 81 是历史值。
5. 补测试：新增拷贝不一致 → 红；全部一致 → 绿。
6. 确认 `python scripts/check_bilingual_docs.py` 仍 exit 0、`77 frozen`。

禁止：不改任何清单的条目内容（除标注历史快照）、不重新生成基线、不改 `current_bilingual_gaps()`。

## 公共约束（FIX BRIEF · COMMON，逐字摘录）

- 只在你被分配的 worktree 里干活，绝不碰 `D:\code\AiMemoryBrainArchitecture`（多 worker 共享克隆）。
- 先 `git fetch origin main` 再 `git merge --no-ff origin/main`，避免 PR dirty 时 0 check runs。
- 取号必须先查占用：`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all&per_page=100`，标题/分支出现过的号不能用；已合并 170/172/173/188/189；INDEX 滞后，不可信。若已有 PR 在做同一件事，停手报告，不要重复开 PR。
- 元数据必须块式 YAML（内联 `{}` 会被 `_scalar()` 判 ParseError），每份都过 `read_metadata()` 自检，必须打印 `True`。
- PR 正文必须含 `Related issue(s): #1212`、`AI-assisted work: YES`、`Session evidence reference(s):` 指向能在 head 树解析的完整路径；`session-evidence.md` 必须含 `Session role / use case`、`Actual AI input`、`AI-visible output` 三节。
- 合并纪律：轮询 `commits/<head_sha>/check-runs`，16 个 required context 全部 completed/success 且无 pending；`strict: true` + `enforce_admins: true`，behind 必须 0；`merge_method: "merge"`；合并后逐文件比对 `git rev-parse origin/main:<path>` 与分支 blob。
- 硬禁止：不改分支保护、不关 Issue、不删 required context、不改与本单元无关的文件、不伪造任何 SHA/测试输出/门禁结果。门禁红且原因不在改动范围 → 停下报告失败 check 名与日志原文。
