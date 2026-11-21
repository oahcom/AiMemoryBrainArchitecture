---
document_metadata:
  domain: memory-compiler
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Owner authorized this root source/mirror topology in PR #429 comment 7061562608; content acceptance, bilingual semantic parity, independent review and CI remain pending."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Memory Compiler reading guide"
    canonical_scope_id: memory-compiler/reading-guide
    canonical_scope_keywords: []
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "04-memory-compiler/README.md"
    en: "docs/en/04-memory-compiler/README.md"
---

# Memory Compiler — 阅读指南

- 文档 ID：E-READING-GUIDE-001
- 版本：1.2
- Stage A 冻结快照基线：`c58878fce24528a0842b4f8887c93ddbf465b566`；来源 Blob：`1ce0146bfd4acfccc7c2747a5b1eaf6440002725`。
- 根目录阅读指南源文件：[`04-memory-compiler/README.md`](../../../04-memory-compiler/README.md)；来源 Blob：`414c6c6fd95fbc36829445e3e2dc3f4795af07fc`；本文为其非规范简体中文镜像。

## 已完成双语配对的源规范

1. [Compiler 总览](compiler-overview.md) — Pipeline、职责边界、确定性/模型辅助阶段和安全不变量。
2. [Accepted Receipt 与幂等契约](accepted-receipt-and-idempotency-contract.md) — 可靠接收、独立 Receipt、Retry/Replay 和 Evidence 边界。
3. [Compiler 状态机与 D Producer Admission](compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease 身份、D Registration、Barrier 和 Terminal Disposition。
4. [Compiler Stage Contract](compiler-stage-contract.md) — 五阶段 Rust 参考流水线；Provenance 是横切关注点，不是第六阶段。
   - 冻结基线双语来源 Pin：英文 Blob `6d733294232a93aa59123009d2a2801d9b83f459`；简体中文 Blob `ad386cac5636b4ba3eaf8b93ad93afcb444e8b46`（main `c58878fce24528a0842b4f8887c93ddbf465b566`）。

## 尚待双语化的核心源规范

E 分支清单还包含 Event Ingestion、Extraction/Normalization、Consolidation/Conflict Resolution、Evidence/Provenance，以及 Forget Fence/Derived Registration 规范。它们的完整双语伴随文档仍待完成，进度见[双语迁移状态](../../governance/translation-status.md)。

## 架构完成契约

当前 [Compiler 总览](compiler-overview.md) §§20–28 记录 Candidate IR / Canonical Schema 边界、五阶段拓扑、横切 Provenance、D/I 权威分工，以及 #459 执行生命周期覆盖层和其内存恢复能力限制。Option A + I1 已 DECIDED；B Schema Freeze/Consumer Acceptance、D Transaction/Currentness/Compatibility、I Attestor/Retention/Forget Mapping，以及所有跨 Owner Consumer Contract 仍为 OPEN。Runtime 验收矩阵仍是计划；Rust 参考 Crate 单元测试不构成矩阵或生产集成证据。

## 权威与状态

E 拥有来源接收/编译编排、Candidate 生成、Stage Lineage、Retry/Replay 和 Producer-side Derivative Evidence。D 拥有 Canonical Identity/Version/Lifecycle 和 D 侧 Forget Fence 语义。I 拥有 Authorization/PermissionEpoch、Revocation、Retention 和 Global Forget Policy/Completion。D/I 权威检查共同约束受保护发布。Storage/Consistency 默认不拥有领域语义；必须明确指定其实现责任 Owner。

CANDIDATE 描述不是已批准 Schema。E 仅输出中立 CandidateProposition/ExtractionIR；不得签发 ClaimRef/ClaimRevisionRef/FactRef/FactRevisionRef，也不得根据 Confidence 推断 Fact。D 拥有 Canonical Identity/Revision/Currentness/Lifecycle 和 D ForgetFence；I 拥有 Authorization/PermissionEpoch、Attestor Authorization、Retention 和 Global Forget Policy/Completion。精确 B/D/I/H/Storage Consumer Contract、Transaction 和 Compatibility Evidence 仍为 OPEN。未授权 Schema、DDL、Public API、Wire 或 Runtime Freeze。

**源文件/镜像状态：**本文是根目录 Informative 阅读指南 `04-memory-compiler/README.md` 的非规范简体中文镜像；英文文件是其配对语言镜像。规范规格各自拥有独立的根目录规范源文件。
