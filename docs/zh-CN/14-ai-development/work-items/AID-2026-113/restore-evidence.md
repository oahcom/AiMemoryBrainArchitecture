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
        - "14-ai-development/work-items/AID-2026-113/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source and mirror blob identities, Owner replacement ruling, and bounded language correspondence observations recorded."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "Evidence for F Memory Runtime root restoration and Owner replacement hierarchy"
    canonical_scope_id: "ai-development/aid-2026-111-f-runtime-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-111"
      - "memory-runtime"
      - "owner-replacement"
      - "mirror-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-113/restore-evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-113/restore-evidence.md"
    zh-CN: null
---
# AID-2026-113 — 恢复证据

## 范围、权威与规范层级

本 Work Item 恢复五份 F Memory Runtime Canonical 根文件，不创建 README。Owner 层级裁决指定 `05-memory-runtime/runtime-overview.md` 显式替代从未存在于任何源分支的 `05-memory-runtime/README.md`。

- `source_hierarchy_decision: OWNER_REPLACEMENT`
- `replaces: 05-memory-runtime/README.md`
- Canonical runtime overview frontmatter 标记 `designated_root: true`
- 权威归属：`user-authorized operator (delegated by account owner), 2026-11-26, 代理裁决，非自然人 Owner 签署`
- F 接受 retrieval semantics：`F_ACCEPTS_RETRIEVAL_SEMANTICS`
- 准备时 main 基线：`57767952f1248e2de616c5dc24ac762ecb3a5a7f`
- 源分支 `session-f-memory-runtime`，HEAD `1908ce4d233b20f7cafd00cb679affd01bd15174`

## Canonical 源文件与新 Blob 对照

| Canonical 路径 | 源 Blob SHA | 新 Blob SHA | 处置 |
|---|---|---|---|
| `05-memory-runtime/activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `028bc3b63693145617290ef1b8f8cd617f931e2e` | `FRONTMATTER_ADDED`；原源正文保持不变 |
| `05-memory-runtime/retrieval-engine.md` | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | `e7220ec1435430f8d4113789428bca336862916f` | `FRONTMATTER_ADDED`；原源正文保持不变 |
| `05-memory-runtime/runtime-overview.md` | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` | `dd98fda4aae0fbdc837835ed44f46dbc1bf7c094` | `FRONTMATTER_ADDED`；原源正文保持不变 |
| `05-memory-runtime/runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `ae879343a6871c51a42cb170d2d16fb4d34caf67` | `FRONTMATTER_ADDED`；原源正文保持不变 |
| `05-memory-runtime/working-set-and-cache.md` | `a934491950c876701e8ac592a0e6aaea983b44e3` | `f5ee311573475df267d6ff5fb60180b73d6b4161` | `FRONTMATTER_ADDED`；原源正文保持不变 |

五份源文件原先均无 YAML frontmatter。新 Blob 由 GOV-DOC-002 frontmatter 与原源正文直接拼接而成。五份文档均保持 `decision_status: Draft`、`normative_status: Informative`。

## 六对 EN/ZH-CN 镜像：原始与补后 Blob SHA

仅对五对有 Canonical 源的镜像增加 frontmatter；每份原正文保持不变。孤儿 guide 镜像对排除在外并保持逐字节不变。

| 镜像对 | EN 原始 Blob | EN 补后 Blob | ZH-CN 原始 Blob | ZH-CN 补后 Blob |
|---|---|---|---|---|
| `activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `43aa4de7a4549ba59b5dcd3b5e30691373e91619` | `be79b8d879121996574cbda840b435624dbe3439` | `9d66e2d9acb8755b7cf2893eec3378db86451bc3` |
| `retrieval-engine.md` | `4baa1b693b3ae2d63d28a9e6716df756d68f0815` | `2e1878d66b0e45c6bce1ddc3e557e490d97613e2` | `1225fb5c629170f05436b3cd2930c90cdf85a4bb` | `9ff6b535b8fbe8d2c21cd8fb9916137cfbc77b61` |
| `runtime-overview.md` | `8ceeff2fe450be431b106d62cc13f33a8623b474` | `ae4af4191f17e564dbabdbda4cefd71524780ba0` | `bd6346e17d049ee716e4906bb2e6b38b2cdce957` | `9e72ed4a6d502d0ab8bc7949abda51b1ac340fe6` |
| `runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `833bebaed5847281bcbcbeb6348a0d52740b3984` | `e30535af23890145456d1ad1738f538387360ce2` | `e0f9735e8967d06936ab5f74bc44a68cda48ac99` |
| `working-set-and-cache.md` | `edabf053502279b9b1d0652c056f695210976394` | `8cce12a5a547b58c414778b45f2e741a4853d533` | `276beab4861e4f3ddd63b12dbb30b0e6b44ef551` | `4851237cd1804690a2c5c3d5d9a839ddedcb99c7` |

## 语种与语义对应核对

- `activation-policy-engine.md`：EN 镜像与英文 Canonical 源文件逐字节相同；ZH-CN 为中文呈现，目的、范围、职责章节对应。
- `retrieval-engine.md`：EN 镜像与源文件并非逐字节相同；已观察到的差异包括把未提交的 Phase 3.5 契约链接改指向 `docs/governance/documentation-gaps.md`。章节结构及 retrieval/scope/fusion 语义对应；ZH-CN 标题和章节结构对应。
- `runtime-overview.md`：EN 镜像在 Phase 3.5 交叉引用处增加 GAP-01 说明；核心目的、范围、权威边界与请求流程对应；ZH-CN 标题与章节对应。
- `runtime-scheduling.md`：EN 镜像与英文 Canonical 源文件逐字节相同；ZH-CN 为对应中文呈现。
- `working-set-and-cache.md`：EN 镜像与源文件并非逐字节相同；已观察到的差异包括把交叉引用改指向 `docs/governance/documentation-gaps.md`。Working Set/cache 隔离、失效、Forget 与版本语义对应；ZH-CN 标题和章节结构对应。
- 本次有界核对未发现明显的 `MIRROR_MISMATCH`。这不等于逐句认证全部译文。

## 孤儿镜像

`docs/en/05-memory-runtime/memory-runtime-guide.md` 与 `docs/zh-CN/05-memory-runtime/memory-runtime-guide.md` 标记为 `ORPHAN_MIRROR_PENDING_DECISION`。原始 Blob 保持不变：EN `a45b868efe1367fb9934c17191109d8d87f48fab`；ZH-CN `0e0df43de9c55f8e41d6ed596d50471798fb23cc`。由于不存在 Canonical source，无法满足 GOV-DOC-002 三向链接，本 PR 不增加元数据，也不改正文。不创建 Canonical guide，也不提升任一镜像。

## 未恢复的历史源记录

以下十份均标记为 `HISTORICAL_PHASE_RECORD`，本 PR 不恢复。源分支实际包含九份 `phase-*` 文件及一份 `module-baseline-and-redlines.md`；十份均按历史记录处理，不提升为 Canonical 根。

- `05-memory-runtime/module-baseline-and-redlines.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.5-reprocessing-change-log.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.6-anti-resurrection-reference-model-evidence.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.6.4-f-prepared-participant-gid-index-boundary-acceptance.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.6.5-f-restore-reconciliation-consumer-acceptance.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md` — HISTORICAL_PHASE_RECORD；未恢复。
- `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md` — HISTORICAL_PHASE_RECORD；未恢复。

## 治理与接受边界

- 将 `05-memory-runtime` 加入 `00-governance/document-scope-registry.yaml` 与 `scripts/check_bilingual_docs.py:NORMATIVE_ROOTS`，使恢复后的 Canonical 根进入声明和执行的治理范围。
- 不创建 `05-memory-runtime/README.md` 或任何 README 镜像。
- 五份 Canonical 文档仍为 Draft、Informative；Owner 层级替代裁决记录为代理授权，不伪装为自然人签署。
- 不包含实现、runtime 代码、schema、tests、workflow、deployment、production 变更或 Issue 关闭。
