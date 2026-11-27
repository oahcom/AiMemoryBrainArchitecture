---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: "user-authorized operator (delegated by account owner)"
      decision_date: "2026-11-27"
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-253/evidence.md"
        - "docs/en/13-engineering-decisions/req02-fts5-vs-like-decision.md"
        - "14-ai-development/adr/ADR-RUN-001-durable-store-and-transaction-boundaries.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "基于当前 main 的有限证据作出边界明确的裁决；不推定生产 Profile 或 Owner 批准。"
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
    source: "13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md"
    en: "docs/en/13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md"
    zh-CN: "docs/zh-CN/13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md"
---

# REQ-04 — 成熟实现处置记录

- 决策记录：REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001
- 关联 Issue：#265
- 决策日期：2026-11-27
- 决策权限：user-authorized operator (delegated by account owner)
- 归属边界：**代理裁决，非自然人 Owner 签署。** 本记录仅为 AC4 证据作出边界明确的代理处置，不声称自然人 Owner 签署、跨 Owner 接受、生产批准或全局技术冻结。
- 总体状态：四项明确 DEFER；均非隐含拒绝。

## 1. SQLite 本地 Profile — DEFER

**裁决：** 暂缓选择 SQLite 作为最终 L4 部署/存储 Profile。保留现有 SQLite Adapter 与测试作为有限的本地参考实现，不将其提升为生产或跨主机权威存储 Profile。

**理由：** Main 已包含 SQLite Adapter crate 和集成测试；Phase 1 决策材料记录了同进程、独立连接 CAS 与幂等行为的有限证据。但这些证据不能证明代表性 Brain 工作负载、跨进程/多主机线性一致性、高可用/故障切换或完整备份恢复正确性。ADR-RUN-001 仍为 PROPOSED，并明确未声称数据库部署或恢复测试完成。

**重开条件：** (a) D 与 Storage 发布并接受精确逻辑行/写集合归属及 L4 Profile；(b) 对代表性 Brain 工作负载进行可复现基准测试；(c) 跨进程测试事务原子性与并发；(d) 崩溃、故障切换、备份和恢复测试覆盖全部规范状态及派生投影；(e) 与 PostgreSQL 在同等条件下比较，并由 Storage/D/Engineering 接受结果。

## 2. PostgreSQL Server Profile — DEFER

**裁决：** 暂缓选择 PostgreSQL 作为最终 L4 Server Profile。不得仅因其是成熟服务端数据库，就推定其适合作为 Brain 存储权威。

**理由：** 当前 main 证据集中没有与代表性 Brain 工作负载配套的可比 PostgreSQL 实现/Profile、精确 D/Storage 事务语义或完整 HA/备份恢复验收。PostgreSQL 的成熟度是开展评估的理由，不是其满足仓库不变量的证据。

**重开条件：** (a) 提供固定版本的 PostgreSQL Profile 及 Schema/Migration 集；(b) 运行与 SQLite 相同的代表性工作负载和正确性向量；(c) 测量隔离级别、原子写集合、幂等、高可用、故障切换、备份恢复及运维负担；(d) 与 SQLite Profile 对比；(e) Storage/D/Engineering 接受精确 Profile 和恢复契约。

## 3. Cedar PDP — DEFER

**裁决：** 暂缓将 Cedar 选为生产 Policy Decision Point。它可以继续作为 I 所有授权接口之后的有限候选评估器；不得因完成集成就将 Cedar 视为策略权威。

**理由：** 冲突登记册将 Cedar 记为候选。当前证据尚未证明所需 Wrapper 符合性向量、当前撤销行为、评估错误/UNKNOWN 的 fail-closed 处理，也没有 I/Security Owner 批准。策略语义、Principal 权威、撤销和 PermissionEpoch 仍归 I 所有。

**重开条件：** (a) 发布固定版本的 Cedar Policy/Model 和 Wrapper 契约；(b) allow/deny/unknown/error、畸形输入、策略过期、撤销及 replay 向量全部通过；(c) 证明 error 和 UNKNOWN 路径 fail closed；(d) 在规定副作用/披露边界重新检查当前 I 授权；(e) I 与 Security Governance 批准精确版本和证据。

## 4. Tantivy — DEFER，NOT REJECTED

**裁决：** 暂缓将 Tantivy 选为替代词法索引。此项**不是拒绝**，也不把现有有限范围的 SQLite FTS5 决策扩大为“FTS5 在所有场景都更优”。

**理由：** 现有 REQ02 词法 ADR 只为初始本地词法通道的有限范围选择 FTS5，并明确记录尚无 FTS5 与 Tantivy 的可比基准或运维比较。FTS5 对比 LIKE 的合成数据基准并未比较两种成熟全文实现，不能证明 Tantivy 较差。

**重开条件：** (a) 使用相同代表性语料、语言/分词假设、查询集和排序/正确性标准，开展可复现的 FTS5-vs-Tantivy 基准；(b) 测量结果一致性/相关性、索引吞吐、更新/删除压力、并发访问、重建时间、存储增长和延迟；(c) 测试原生 Adapter 集成及授权/Forget 过滤；(d) 证明相对约定工作负载阈值存在实质优势，并由相关 Owner 接受。

## 5. 后果与边界

- 四项明确处置满足 AC4 的“考虑并作出结论”要求；不代表选择了生产实现。
- 不向任何产品授予 Canonical Truth、Evidence、Authorization、Forget、Lifecycle 或 Applied 权威。
- CF-013 与 CF-014 在各自收口证据及 Owner 接受完成前仍保持未解决。
- 本记录为 Informative、Non-Canonical，不修改 Owner 契约或现有 FTS5 ADR。
