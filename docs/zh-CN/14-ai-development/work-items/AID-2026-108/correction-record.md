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
        - "14-ai-development/work-items/AID-2026-108/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-108/correction-record.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Historical statements and PR #1283 merge metadata were read from GitHub; this record does not claim implementation or backend conformance."
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
    canonical_scope: "Historical-baseline correction record for AID-2026-099's AID-2026-098 Storage dependency pin"
    canonical_scope_id: "ai-development/aid-2026-108-baseline-correction"
    canonical_scope_keywords:
      - baseline-correction
      - storage-consistency
      - idempotency
      - evidence-boundary
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: 14-ai-development/work-items/AID-2026-108/correction-record.md
    en: "docs/en/14-ai-development/work-items/AID-2026-108/correction-record.md"
---

# AID-2026-108 — AID-2026-099 基线可得性纠正记录

- 日期：2026-11-26
- 署名：user-authorized operator (delegated by account owner)；仅代理登记，不构成自然人 Owner 签署
- 状态：Draft / Informative；仅为纠正记录

## 1. 目的与边界

本记录纠正一条曾在 AID-2026-099 原始写作基线上准确、但在 AID-2026-098 合并进 main 后已经过期的可得性表述。这是历史基线过期纠正，不改变 AID-2026-099 的任何规范结论。HIR-06 对 AID-2026-098 的引用仍然成立。

## 2. 纠正前原文（逐字保留）

### 2.1 AID-2026-099 manifest，原第 68 行

文件：14-ai-development/work-items/AID-2026-099/manifest.yaml

~~~yaml
storage_aid_2026_098_exact_pin: "NOT_AVAILABLE_ON_BASELINE"
~~~

### 2.2 H 合同原第 88 行段落（Canonical 与 EN 镜像）

文件：08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md

~~~text
**Storage / AID-2026-098 dependency:** this main baseline contains no AID-2026-098 directory or manifest, and no discoverable PR with that identifier. Its exact Storage contract version/blob is therefore **NOT AVAILABLE ON THIS BASELINE**. This proposal reserves Storage atomicity and persistence details to AID-2026-098 and does not invent or duplicate them. Before cross-owner freeze, pin its exact path/version/blob and verify H/Storage mapping. The Storage Trait above is only a candidate seam, not a substitute.
~~~

EN 镜像包含相同段落。ZH-CN 镜像包含对应的原始表述：

~~~text
**Storage / AID-2026-098 依赖：** 此 main 基线不存在 AID-2026-098 目录或 manifest，也未发现该编号的 PR。因此其精确 Storage 合同版本/blob 为 **NOT AVAILABLE ON THIS BASELINE**。本提案将 Storage 原子性与持久化细节留给 AID-2026-098，不臆造或重复定义。跨 Owner 冻结前，必须 pin 其精确路径/版本/blob 并核验 H/Storage 映射。上述 Storage Trait 只是候选 seam，不能替代 AID-2026-098。
~~~

## 3. 纠正后的事实

- AID-2026-098 已通过 PR #1283 合并进 main。
- Merge commit：cdba0b7360b81ba2693c57f0d89ad2e28832272c。
- PR Head：7da2195bccf07ec51af545a7313dcc1d11bdd1e3。
- Storage 合同现有三份文件：
  - 10-storage-consistency/storage-physical-consistency-contract.md
  - docs/en/10-storage-consistency/storage-physical-consistency-contract.md
  - docs/zh-CN/10-storage-consistency/storage-physical-consistency-contract.md
- AID-2026-098 记录了 18 个检查点：10 个 DOCUMENTED_ONLY，8 个 EVIDENCE_REQUIRED。8 个证据必需检查点仍未获得证据；候选合同文件存在，不等于实现、后端符合性、生产持久性、崩溃恢复或 Owner 接受已得到证明。

## 4. 精确纠正与不产生的影响

099 manifest 的 storage_aid_2026_098_exact_pin 值，以及 H 合同三份镜像中的 Storage 依赖段落，现已更新为指向已合并的 AID-2026-098 / PR #1283 和本纠正记录。每个修改位置均标记 corrected_by: AID-2026-108。

本次纠正：
- 不改变 AID-2026-099 的任何规范结论或检查点结果；
- 不改变 HIR-06；其对 AID-2026-098 的引用仍然成立；
- 不修改 AID-2026-098 的任何文件或内容；
- 不声称 HIR-06、HIR-16、HIR-17 或 HIR-18 已有实现证据；
- 不声称 Storage 已实现或符合性已验证；
- 不关闭 Issue #1211 或任何其他 Issue。

## 5. 证据边界

已通过 GitHub 核验合并元数据及当前文件存在性。18 个检查点的分类统计来自 AID-2026-098 manifest 的既有登记，不是本轮新执行的测试结果。现在可以对照真实的 Storage 候选合同核验 HIR-06 映射；但 HIR-06/16/17/18 的实现证据仍然缺失。
