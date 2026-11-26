---
document_metadata:
  domain: domain-model
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
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: DECIDED for the Phase 1 orchestration boundary）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：236e30cf4ddc50899393b83129e3ded05ee012d4。"
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
    normative_status: Normative
  bilingual_counterpart:
    source: "02-domain-model/phase-1-memory-store.md"
    en: "docs/en/02-domain-model/phase-1-memory-store.md"
    zh-CN: null
---
# Phase 1 Memory Store Facade

状态：Phase 1 编排边界 DECIDED；Storage 后端仍保持可替换。

## 目的
提供最小应用层 Facade，将已冻结 Domain Model 与后端无关的 MemoryStorage Port 组合起来。

## 职责
- 在进入 Storage 前校验 Memory / MemoryVersion 领域不变量；
- 每个操作都要求已解析 Scope；
- 保持 Memory identity 与不可变 MemoryVersion/revision 语义；
- 在提交前拒绝 memory_id 与 revision.memory_id 不一致；
- 将 CAS、幂等和可见性约束委托给 MemoryStorage；
- 提供 current/revision 读取与幂等解析，但不拥有持久化。

## 非职责
不定义 SQLite DDL、分布式共识、Physical Forget、Permission Policy、索引、Embedding、LLM 或部署拓扑。

## Revision 边界
Phase 1 将 MemoryVersion 作为规范不可变 revision 表示。MemoryRevision 只是 API alias，不产生第二个持久化对象。

## Scope 边界
每个 Facade 操作都要求非空 resolved Scope。Scope 兼容不等于 Permission 授权。

## 幂等写入边界
Revision write 同时携带 expected-current-version、Idempotency Key 和 Request Digest。身份不一致必须在进入 Storage 前拒绝；重放/冲突语义由 Storage Port 负责。

## 验收
Create/Read 必须有有效 Scope；revision identity mismatch 必须在后端调用前失败；stale transition 必须被拒绝；相同 Key + Digest 可以解析到原 Receipt；不同 Scope 不得隐式可见；Facade 不得引入后端特定依赖。

## 下一单元
待该最小 Facade 稳定后，再继续更高层 Memory Store 行为和应用集成；不引入 Vector/Graph/LLM 依赖。
