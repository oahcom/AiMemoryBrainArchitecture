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
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: G-owned normative design draft; implementation NOT VERIFIED; cross-owner acceptance required）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：4d57e90e987ec6ed679fba9047945e6a73f5d36c。"
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
    source: "06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md"
    en: "docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md"
    zh-CN: null
---
# G Applied 持久化合同中文源文件的阅读镜像

本文件对应规范中文源文件：
`06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`。

该合同规定 Full Applied 的持久化决策仅归 G 所有。C `HANDOFF_ACCEPTED` 是必要条件但不充分；G 必须关联 C Provider Outcome、经过认证的 H Evidence、COC Participant/Terminal Proof、I Authorization、D ForgetFence、适用时 Storage Same-GID Resolution，以及 G Context/Delivery Predicate。

合并 PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) 加入了有明确边界的单节点 SQLite 参考模型。精确 PR Head 运行 [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388) 与合并后 main 运行 [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305) 均通过；后者绑定 main `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf`，报告 8 项测试通过。

该成果是参考/符合性原型，不是生产 G Runtime，也不是 Owner 验收。它不证明多副本线性化、分布式 Restore-Fencing、Current-Use Revalidation、真实权威解析、密码学认证或生产持久化能力。生产 G Applied 与跨 Owner Full Applied 仍为 **NOT VERIFIED / NOT FROZEN**。
