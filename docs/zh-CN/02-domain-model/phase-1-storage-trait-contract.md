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
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: CANDIDATE implementation seam; no backend is selected）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：daab973665604c1f4350dc74bccd44cfff3ec4a2。"
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
    source: "02-domain-model/phase-1-storage-trait-contract.md"
    en: "docs/en/02-domain-model/phase-1-storage-trait-contract.md"
    zh-CN: null
---
# Phase 1 Storage Trait 契约

状态：CANDIDATE 实现边界；本文件不选择具体后端。

## 目的

定义纯 memory-domain 与未来持久化实现之间与后端无关的 Application Port。

## 操作

- create_memory (with resolved scope)
- read_current
- read_version
- commit_version
- list_changes
- resolve_idempotency

## 提交边界

后端实现 MUST 将不可变 Version、Current-Version CAS、Idempotency Record 与 Canonical Commit Sequence 视为一个可恢复提交边界。本 Trait 不规定 SQLite DDL 或分布式事务协议。

## 安全

每次读写都接收已解析 Scope，包括 create_memory。后端 MUST 在解析幂等 Receipt 前完成 Scope 授权，并 MUST 拒绝 memory_id != new_version.memory_id。后端 MUST NOT 将陈旧 Projection 当作 Canonical State。expected_current_version 是乐观并发保护。

## 幂等

相同 Idempotency Key + Request Digest 可以返回原 Receipt；相同 Key + 不同 Digest MUST 返回 IdempotencyConflict。

## 明确不包含

不包含 SQLite Adapter、Event Store、Memory Store facade、网络传输、Vector/Graph Index、物理 Forget 或生产持久化能力声明。

## 验证边界

本 Crate 只包含纯 Rust 契约形态测试，不证明后端原子性、崩溃恢复、跨进程并发、序列化或持久化能力。


> 双语同步说明：本文件与 `docs/en/02-domain-model/phase-1-storage-trait-contract.md` 同一提交更新，语义保持一致。