---
document_metadata:
  domain: memory-context
  role: index
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
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Publication status: candidate architecture and historical review evidence）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：5e669ea1346f0bc6286ebc383e07a699fe3d108e。"
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
    source: "06-memory-context/README.md"
    en: "docs/en/06-memory-context/README.md"
    zh-CN: null
---
# Session G — Memory Context 包

**发布状态：**候选架构与历史评审证据；不是已冻结的跨 Owner 契约。

本包包含 G 提出的 Memory Context 架构、由 G 负责的语义决策以及委派评审记录。它作为有界设计基线发布，供后续集成继续使用；它不构成生产实现证据，也不构成全局 Applied/Forget 验收。

## 权限与证据边界

- G 负责期望的 Context 成员关系、排序、资格、预算、不可变 Context 版本、协调以及交付意图。
- D 负责 Canonical Memory 和 ForgetFence；F 负责检索/归档；I 负责身份、权限和全局治理；C 负责最终请求边界和提供方结果；H 负责传输/Adapter 证据；Storage 负责持久化序列化与恢复。
- 本包中的任何 G 文档都不会覆盖其他 Owner 的权限，也不能替代该 Owner 对精确版本所作的验收。
- 基于角色/委派的 G 评审与验收记录，是按照用户指示集中准备的。它们不是独立的人类 Owner 签署，不得被表述为此类签署。
- 部分评审工件固定了历史分支 HEAD 和 Blob SHA。在将某项决策用于当前集成之前，必须刷新对应的精确源分支，并重新评审精确的当前工件。
- Phase 3.8.22 契约仅是规范性设计草案：实现 NOT VERIFIED；崩溃/重启/恢复测试 NOT RUN；C/G/H Applied 冻结 NO；生产出站流量 NOT AUTHORIZED。
- 早先在 main 分支上的三方评审仍作为历史 FAIL 快照保留。后续评审单独存储，不会抹除该历史。

## 当前包的处置状态

**候选状态：可继续进行跨 Owner 集成 — 尚未冻结。** 通用 Scope、跨模块线协议细节、全局 Forget 完成状态、生产 Applied 证据、持久化重放、Storage 线性化以及精确的当前 Owner 验收仍处于开放状态。
