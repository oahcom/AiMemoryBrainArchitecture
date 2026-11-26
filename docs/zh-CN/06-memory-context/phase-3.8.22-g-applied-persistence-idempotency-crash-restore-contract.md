---
document_metadata:
  domain: memory-context
  role: design-specification
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
        - "14-ai-development/work-items/AID-2026-193/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: G-OWNED NORMATIVE DESIGN DRAFT; IMPLEMENTATION NOT VERIFIED; CROSS-OWNER ACCEPTANCE REQUIRED）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：a5b6642e0c449ea0d2cc18fef365e09b421acfa5。"
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md"
    en: "docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md"
    zh-CN: null
---
# G Applied 持久化、幂等、崩溃恢复与 Restore-Fencing

- 规范源文件：`06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md`
- 中文规范源文件：`06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`
- 状态：**已有参考模型；生产实现尚未验证**

## 阅读摘要

只有 G 拥有持久化 Full Applied 决策权。C 的 `HANDOFF_ACCEPTED` 是必要条件，但不是充分条件。G 必须关联精确的 C Provider Attempt/Outcome、经过认证的 H Delivery Evidence、COC Participant/Terminal Proof、当前 I Authorization、D ForgetFence、适用时 Storage Same-GID Terminal Result，以及 G 自身 Context/Delivery Predicate。

G Phase 3.8.22 规范定义逻辑 Applied Identity、Evidence-Revision 规则、相同身份/相同摘要重放、摘要变化冲突隔离、崩溃/重启行为与 Restore-Fencing。精确 Owner 验收和生产实现要求以规范源文件为准。

## 可执行参考证据 — 2026-11-18

合并 PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) 在 `06-memory-context/reference-model/` 下增加了有明确边界的单节点 SQLite 参考模型。

- 精确 PR Head 运行 [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388)：SUCCESS。
- 合并后 main 运行 [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305)：在 main Commit `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf` 上 SUCCESS；8 项测试通过。
- 覆盖：HANDOFF_ACCEPTED 正向提交；相同摘要幂等重放；摘要变化冲突且不覆盖原记录；拒绝四种非成功 C Outcome；缺失/失败 Gate Fail-Closed；重启读回；不同身份隔离；精确 Identity 字段集合校验。

## 证据上限

该参考模型不是生产 G Runtime 代码，也不是 G Owner 验收。它使用单个本地 SQLite 数据库和调用方提供的 Gate 布尔值，不能证明多副本线性化、分布式 Restore-Fencing、后续 I/D 变化后的 Current-Use Revalidation、真实 C/H/COC/I/D/Storage 权威解析、密码学认证或生产持久化拓扑。生产 G Applied 与跨 Owner Full Applied 仍为 **NOT VERIFIED / NOT FROZEN**。

本阅读摘要与 G Phase 3.8.22 双语规范源文件配对，不替代规范源文件。
