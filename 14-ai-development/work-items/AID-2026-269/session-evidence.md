---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Session evidence; no acceptance decision is asserted."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Session evidence for AID-2026-269"
    canonical_scope_id: "ai-development/aid-2026-269-session-evidence"
    canonical_scope_keywords:
      - "exact-head-review"
      - "session-evidence"
      - "prompt-digest"
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-269 — Session Evidence

**Work Item:** AID-2026-269  
**Renumbered from:** `268` — 268 was free on main, in INDEX.md and in every open pull request, but closed-unmerged PR #1371 (branch `fix/aid-268-manifest-blob-pins`, head `efac9a1c`) still publishes an `268/` directory in branch space; branch space counts as occupied under the convention recorded in AID-2026-240 `identifier_allocation`, so the Owner moved the unit to 269 (`reply-6b08fa9b-124545.md` §1).  
**Carrier branch:** `review/2026-11-27-aid269-exact-head-review`  
**Carrier:** #1278 — https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1278  
**Baseline commit:** `987d26021affbb5ba6d651e0fb5985d6bd4026a5`  
**Executed prompt snapshot:** `14-ai-development/work-items/AID-2026-269/prompt-v1.md` — 16877 bytes, SHA-256 `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170`  
**Prompt provenance:** `NOT_VERIFIED` (the snapshot is the composed payload; no platform-side delivery receipt exists)  
**Session reference status:** `NOT_AVAILABLE` — the platform exposes no stable session identifier, so every session is recorded as `NOT_EXPOSED` rather than invented.

This document is one container with four session sections, because the WP-2 deliverable list names exactly one session-evidence file. The manifest records the deviation (`session_evidence_container`) and why per-session entries were not used: `check_09` rejects a shared `session_evidence_ref`, so separate entries would require separate files.

## Session role

| Session | Role | Output owned | Status at 2026-11-27T04:39:33Z |
|---|---|---|---|
| L2-A | 协议设计 — author of the reusable protocol | `exact-head-review-protocol-v1.md` | file present |
| L2-B | 真实用例复核 — #1278 / AID-2026-092 execution | `review-case-1278.md`, `evidence.md` | files present |
| L2-C | 治理记录 — manifest, prompt snapshot, this record, INDEX row | `manifest.yaml`, `prompt-v1.md`, `session-evidence.md`, INDEX row | this record |
| L3 | 独立复核 — independent re-execution of the protocol at the final head | none | `PENDING — not yet executed` |

## Actual AI input

The common executed instruction for L2-A, L2-B and L2-C is the L1 ruling's `## R2 工作包 WP-2` block, pinned as `prompt-v1.md` with the work-item identifier advanced to 269 by the renumber ruling. The per-session slice is the row each session was given in `### L2 子代理分工`.

**L2-A — 协议设计.** Dispatched brief: the WP-2 block as pinned, with the row `L2-A：协议设计 | exact-head-review-protocol-v1.md | 可复用的精确 Head 复核协议 | 自检：章节完整性检查；逐项验证协议字段`, plus the boundary `L2-A 不负责判定 #1278 是否真实存在缺陷`.

**L2-B — 真实用例复核.** Dispatched brief: the same WP-2 block, with the row `L2-B：真实用例复核 | AID-2026-092、#1278 历史数据 | review-case-1278.md、历史摘要清单、原始复算输出 | 自检：重新运行 Git 历史枚举和 SHA-256 计算`, plus the boundary `L2-B 不负责修改协议`. The block's own warning applies unchanged: the numbers quoted in `### 复核/实现规格` 五 are 待复核输入，不是预先授予的验收结果.

**L2-C — 治理记录.** Dispatched brief: the same WP-2 block, with the row `L2-C：治理记录 | manifest、prompt、evidence、session-evidence、INDEX | 完整工作项记录和 GitHub 投递文本 | 自检：YAML 解析、prompt 摘要、INDEX 唯一性检查`, plus the boundary `L2-C 不负责生成或修改任何被审查对象` and `所有 L2 必须记录自己的基线 SHA`. This session's own baseline is `987d26021affbb5ba6d651e0fb5985d6bd4026a5`.

**L3 — 独立复核.** Dispatched brief, not yet executed: `### L3 独立复核清单` items 1–24, with `L3 必须是与 L0、L2-A、L2-B、L2-C 不同的执行会话` and `L3 必须提供自己的命令日志和独立计算结果，不能只在 L2 的报告上签字`. No result exists and none is recorded here.

## AI-visible output

**L2-A.** `14-ai-development/work-items/AID-2026-269/exact-head-review-protocol-v1.md` — 27398 bytes, SHA-256 `779d51036a87b474865073f7d3d61f81c08532e5221f78c98cc83dec1cb756bc`, re-read after the renumber. That digest is a timestamped observation, not a final-head verification; R2-19 requires the digest to be re-read at the final head.

**L2-B.** `14-ai-development/work-items/AID-2026-269/review-case-1278.md` — 61851 bytes, SHA-256 `3e0a910bded388ef21632c852332f005834ab608a8096f1eb93d47e2abd5ece0`; `14-ai-development/work-items/AID-2026-269/evidence.md` — 32345 bytes, SHA-256 `eed924b22abfc5c88c682e57bd27ee58c3a3f2cd99da506fa5fe6964b9ee65d9`; both re-read after the renumber, with the same caveat. The verdict inside them belongs to the reviewed declaration and is not restated here.

**L2-C.** `14-ai-development/work-items/AID-2026-269/prompt-v1.md` — 16877 bytes, SHA-256 `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170`; `14-ai-development/work-items/AID-2026-269/manifest.yaml`; `14-ai-development/work-items/INDEX.md` one appended row for AID-2026-269. This file is the fourth output and carries no digest of itself, because a document cannot contain its own SHA-256.

**L3.** `PENDING — not yet executed`. No output, no verdict, no command log, and no digest is claimed.

## Prompt snapshot

| Session | Snapshot file | Bytes | SHA-256 | Provenance |
|---|---|---|---|---|
| L2-A | `14-ai-development/work-items/AID-2026-269/prompt-v1.md` | 16877 | `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170` | `NOT_VERIFIED` |
| L2-B | `14-ai-development/work-items/AID-2026-269/prompt-v1.md` | 16877 | `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170` | `NOT_VERIFIED` |
| L2-C | `14-ai-development/work-items/AID-2026-269/prompt-v1.md` | 16877 | `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170` | `NOT_VERIFIED` |
| L3 | `14-ai-development/work-items/AID-2026-269/prompt-v1.md` (to be executed) | 16877 | `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170` | `NOT_VERIFIED` |

The three executing sessions consumed the same pinned payload, which is why the digest is identical rather than three separately hashed prompts. The digest was computed from the written file after the last edit; a stale digest fails the Session Evidence gate.

## Session references

`implementing_ai_session` is `NOT_EXPOSED` for every session. The subagent platform does not expose a stable, verifiable session identifier to the session itself, and inventing one would be a fabricated reference. `session_reference_status: NOT_AVAILABLE` records the limitation, per `prompt-and-evidence-template.md` §3.1. If the coordinator can observe the platform-side session ids, they can be added here without touching `prompt-v1.md`, and its digest would remain valid.
