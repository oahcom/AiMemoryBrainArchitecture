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
        - "14-ai-development/work-items/AID-2026-140/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source, merged and corrected Git blob identities and the original exact-Head CI readback are recorded; no Owner acceptance is asserted."
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
    canonical_scope: "Evidence for F Memory Runtime source restoration, fixed-range Work Item re-registration and metadata reconciliation"
    canonical_scope_id: "ai-development/aid-2026-140-f-runtime-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-140"
      - "memory-runtime"
      - "owner-replacement"
      - "blob-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-140/restore-evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-140/restore-evidence.md"
    zh-CN: null
---
# AID-2026-140 — F Memory Runtime 恢复与编号纠正证据

## 范围、授权与重新编号

本记录承接 PR #1314 已恢复的五份 F Memory Runtime Canonical 根文件，并按账号固定号段将当前 Work Item 重新登记为 **AID-2026-140**。原并发载体使用 AID-2026-113 和 INDEX max+1 分配；该号码不在本账号固定号段内，不再作为当前 Work Item 编号。

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 重新登记基线 main：`0786a3b89e060266cbd249e81f4571b9dc3f51d5`
- 原源分支：`session-f-memory-runtime`
- 源分支 HEAD：`1908ce4d233b20f7cafd00cb679affd01bd15174`
- 原载体：PR [#1314](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1314)，Head `9142698fae340271e44c3a097fad0cc6455666b3`，merge commit `d6cad634f1341a8943aa89dd5ef8bf75f6d56199`
- 当前 Work Item：`AID-2026-140`；原编号仅作为历史来源记录：`AID-2026-113`。
- 编号规则：仅在 `AID-2026-140`–`AID-2026-149` 中选首个未占用编号；不使用 INDEX max+1。
- 归属：user-authorized operator (delegated by account owner)；不代表自然人 Owner 签署。

F 规范层级方向：
- `source_hierarchy_decision: OWNER_REPLACEMENT`
- `replaces: 05-memory-runtime/README.md`
- `05-memory-runtime/runtime-overview.md` 标记 `designated_root: true`
- 顶层 authority 精确值：`user-authorized operator (delegated by account owner), 2026-11-26`

原 PR 使用 `source_hierarchy_decision_authority` 且带有额外后缀。本次将其替换为用户指定的精确 `authority` 键和值。保留 `retrieval_semantics_acceptance: F_ACCEPTS_RETRIEVAL_SEMANTICS`。

## 五份 Canonical 源 Blob 对照

| Canonical 路径 | 源分支 Blob | AID-113 合并后 main Blob | AID-140 纠正后 Blob |
|---|---|---|---|
| `05-memory-runtime/activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `ce15bec184f0f358d84df91987de04a70216ad41` | `11ee1a70c7cae7c7bf64b97e0d8c879db68c6dae` |
| `05-memory-runtime/retrieval-engine.md` | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | `c49c9c9272d04dddc29885c9aa0ada28d3d15e1c` | `38fb72395166b52d8c1b0380757110ecc508cc05` |
| `05-memory-runtime/runtime-overview.md` | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` | `d084c463b7527e8ee364557ae941c7d19197b1d6` | `80879fd3ed23b2f4545e186b8bd3626c80960c70` |
| `05-memory-runtime/runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `05e4b4b78eda3dfa260dd95bbbaf6fc57a85f861` | `cfbd78e7c0381f493ac0d9cd104709b8dbbec6bf` |
| `05-memory-runtime/working-set-and-cache.md` | `a934491950c876701e8ac592a0e6aaea983b44e3` | `b6ec474256f703fb81a6b60b15ad0b453e3d5b9f` | `a4d8af1c59ad8fc0b118d6818928478f68fa919a` |

五份源正文均逐字节保留。AID-140 仅更新 GOV-DOC-002 evidence 引用；`runtime-overview.md` 另外将顶层 `authority` 键和值修正为用户指定的精确形式。不翻译或改写源正文。

## 五组有 Canonical 源的 EN/ZH-CN 镜像

| 镜像组 | EN 原始 Blob | EN AID-113 Blob | EN AID-140 Blob | ZH-CN 原始 Blob | ZH-CN AID-113 Blob | ZH-CN AID-140 Blob |
|---|---|---|---|---|---|---|
| `activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `39012b82c6ce69f0b774d2d89fcf398d5f74666b` | `cbf018fb4f2454ebbc9db1d5cc4dc05fc5269bea` | `be79b8d879121996574cbda840b435624dbe3439` | `b71c72eaa4e28e04e22beb1e1f8f8ac79be221b0` | `f2506ece4b77e328fba23b139492f00b171fb8ed` |
| `retrieval-engine.md` | `4baa1b693b3ae2d63d28a9e6716df756d68f0815` | `12dbc2f2c811e7d61eb415ccc7f7e463c13019d2` | `e293c4704421cfaea7ff0557ea20817623e5de1e` | `1225fb5c629170f05436b3cd2930c90cdf85a4bb` | `9ed86618decfd8538d3d4af21ea0b4df683d2fe1` | `e6a2c63e1eb773566d3412467e006b9c1465e0e4` |
| `runtime-overview.md` | `8ceeff2fe450be431b106d62cc13f33a8623b474` | `244a3b6ab34a3e89a2c04a213a1500516b8ad826` | `d65c4508e2ca492f99eaf796acb5ae71f9564208` | `bd6346e17d049ee716e4906bb2e6b38b2cdce957` | `f7351faf3d126f28dcb427f8c986eb4c5ac8d89a` | `cfb77ea85655b217bba1cd57b07b35508e9eeef0` |
| `runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `ab8c4364d87f9e9f1feda7ce091c00ac4d338f67` | `c2b2b22aa8eb7447e23feca43f398c9038045069` | `e30535af23890145456d1ad1738f538387360ce2` | `f12ed42732e195e3ff0f0a937603e1d432eb6346` | `f4c5e27d6115bdc6cfb47ee39ef5423404f22cea` |
| `working-set-and-cache.md` | `edabf053502279b9b1d0652c056f695210976394` | `8cac511c3bb0213313ba63772f5d0c80f7a0be7b` | `fc2b4dc78dcd2c700f2cfc8073b7dfc17be3773c` | `276beab4861e4f3ddd63b12dbb30b0e6b44ef551` | `7d917c6cadb983d719c135bbfc42eaf5a574a8d0` | `4e2772b968672590a6268f1b46dbef8ee347644a` |

十份镜像正文均逐字节保留。仅将 GOV-DOC-002 元数据中的 Work Item evidence 引用从 AID-113 改为 AID-140。

### 双语对应核对

- `activation-policy-engine.md`：EN 镜像正文与英文源文件逐字节相同；ZH-CN 标题和职责章节对应。
- `retrieval-engine.md`：EN 镜像存在指向 `documentation-gaps.md` 的有限交叉引用差异；章节结构及 retrieval/scope/fusion 语义对应。
- `runtime-overview.md`：EN 镜像对 Phase 3.5 引用增加 GAP-01 来源说明；核心目的、范围、权威边界和请求流对应。
- `runtime-scheduling.md`：EN 镜像正文与英文源文件逐字节相同；ZH-CN 为对应中文版本。
- `working-set-and-cache.md`：EN 镜像存在指向 `documentation-gaps.md` 的有限交叉引用差异；Working Set/Cache 隔离、失效和 Forget 语义对应。
- 有界标题、交叉引用和语义核对未发现明显 `MIRROR_MISMATCH`；不声称完成逐行翻译认证。

## 孤儿镜像与历史源记录

`memory-runtime-guide.md` 镜像对保持 `ORPHAN_MIRROR_PENDING_DECISION`，完全不动。原 Blob 仍为：
- EN：`a45b868efe1367fb9934c17191109d8d87f48fab`
- ZH-CN：`0e0df43de9c55f8e41d6ed596d50471798fb23cc`

源分支实际包含九份 `phase-*` 文件，另有 `module-baseline-and-redlines.md`。十份记录全部归类为 `HISTORICAL_PHASE_RECORD`，均不恢复：
- `05-memory-runtime/module-baseline-and-redlines.md`
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md`
- `05-memory-runtime/phase-3.5-reprocessing-change-log.md`
- `05-memory-runtime/phase-3.6-anti-resurrection-reference-model-evidence.md`
- `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md`
- `05-memory-runtime/phase-3.6.4-f-prepared-participant-gid-index-boundary-acceptance.md`
- `05-memory-runtime/phase-3.6.5-f-restore-reconciliation-consumer-acceptance.md`
- `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md`
- `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md`
- `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md`

不创建 `05-memory-runtime/README.md` 或 README 镜像。`04-memory-compiler/compiler-stage-contract.md` 不恢复；PR-C 仍取消。

## 原载体验证

PR #1314 以 `d6cad634f1341a8943aa89dd5ef8bf75f6d56199` 合并。原 PR Head 为 `9142698fae340271e44c3a097fad0cc6455666b3`，base 为 `57767952f1248e2de616c5dc24ac762ecb3a5a7f`，compare 为 `ahead_by=1`、`behind_by=0`。

原载体 exact-Head 的 16 项检查全部 SUCCESS：
- `audit`：SUCCESS
- `rust-workspace-test`：SUCCESS
- `Rust doctests (hard gate)`：SUCCESS
- `Session Evidence self-test (head)`：SUCCESS
- `Schema non-empty audit (hard gate)`：SUCCESS
- `BMCP conformance suite (hard gate)`：SUCCESS
- `GOV-DOC-001 structural checks`：SUCCESS
- `BMCP protocol index (hard gate)`：SUCCESS
- `Session Evidence self-test (base)`：SUCCESS
- `Bilingual docs coverage (ratchet)`：SUCCESS
- `Rust format (hard gate)`：SUCCESS
- `Session Evidence`：SUCCESS
- `Repository hygiene (hard gate)`：SUCCESS
- `Branch freshness vs base`：SUCCESS
- `Rust clippy (hard gate)`：SUCCESS
- `GOV-DOC-002 metadata checks`：SUCCESS

原 #1212 closeout 评论为 [comment 7193607161](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7193607161)。本次 AID-140 follow-up 仅重新登记固定号段 Work Item 并修正 authority 字段；不关闭 #1212。

## 治理与接受边界

- PR #1314 已将 `05-memory-runtime` 纳入 `00-governance/document-scope-registry.yaml` 和 `scripts/check_bilingual_docs.py:NORMATIVE_ROOTS`。
- 五份 Canonical 文档继续保持 `decision_status: Draft` 和 `normative_status: Informative`。
- OWNER_REPLACEMENT 是代理操作方向记录，不是自然人 Owner 签署或 F Owner 规范性接受。
- 不修改 Runtime 实现、validator、schema、tests、workflow、deployment 或 production。
