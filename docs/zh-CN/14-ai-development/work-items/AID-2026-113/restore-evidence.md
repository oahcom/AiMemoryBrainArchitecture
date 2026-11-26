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

## Correction (2026-11-27)

本节追加在原文之后。上文的两张表格、blob 引用与任何声明均未改动；front-matter 中的 `verification_status: Verified` 是原作者写的，原样保留。本节记录的是：**该声明对新 blob 身份列不成立。**

实测基线为 `origin/main`（`4326669caa6c43193d34219a0451b80762b712ff`）：

- 两张表共有 15 个新 blob 单元格：Canonical 源文件与新 blob 对照表 5 个，EN/ZH-CN 镜像原始与补后 blob 表 10 个。
- 15/15 无法通过 `git cat-file -t`，报 `fatal: git cat-file: could not get object info`（退出码 128）。它们不在对象库中，因此不可能是该路径任何已提交版本的身份。
- 0/15 等于文件实际所在的 blob——无论在 `origin/main` 还是在复原提交上。
- 同表中 17 个源 blob、原始 blob 与孤立镜像 blob 全部可解析，且 5 个 Canonical 源 blob 与 `1908ce4d:<path>` 完全一致。缺陷只在新 blob 一列。

### C1. 每个被记下的新 blob 都无法解析

逐条执行（15 次，未用循环），15 条输出完全相同：

```
$ git cat-file -t 028bc3b63693145617290ef1b8f8cd617f931e2e
fatal: git cat-file: could not get object info
$ echo "exit=$?"
exit=128
```

| # | 表中记的新 blob SHA | `git cat-file -t` |
|---|---|---|
| 1 | `028bc3b63693145617290ef1b8f8cd617f931e2e` | exit 128 |
| 2 | `e7220ec1435430f8d4113789428bca336862916f` | exit 128 |
| 3 | `dd98fda4aae0fbdc837835ed44f46dbc1bf7c094` | exit 128 |
| 4 | `ae879343a6871c51a42cb170d2d16fb4d34caf67` | exit 128 |
| 5 | `f5ee311573475df267d6ff5fb60180b73d6b4161` | exit 128 |
| 6 | `43aa4de7a4549ba59b5dcd3b5e30691373e91619` | exit 128 |
| 7 | `9d66e2d9acb8755b7cf2893eec3378db86451bc3` | exit 128 |
| 8 | `2e1878d66b0e45c6bce1ddc3e557e490d97613e2` | exit 128 |
| 9 | `9ff6b535b8fbe8d2c21cd8fb9916137cfbc77b61` | exit 128 |
| 10 | `ae4af4191f17e564dbabdbda4cefd71524780ba0` | exit 128 |
| 11 | `9e72ed4a6d502d0ab8bc7949abda51b1ac340fe6` | exit 128 |
| 12 | `833bebaed5847281bcbcbeb6348a0d52740b3984` | exit 128 |
| 13 | `e0f9735e8967d06936ab5f74bc44a68cda48ac99` | exit 128 |
| 14 | `8cce12a5a547b58c414778b45f2e741a4853d533` | exit 128 |
| 15 | `4851237cd1804690a2c5c3d5d9a839ddedcb99c7` | exit 128 |

### C2. 这些路径实际是什么 blob

`git rev-parse origin/main:<path>` 是当前身份；`git rev-parse 9142698f:<path>` 是复原提交建立的身份——"新 blob"一列本应描述的就是后者。

| # | 路径 | 表中记的新 blob | `origin/main` blob | `9142698f` 处 blob | 相符 |
|---|---|---|---|---|---|
| 1 | `05-memory-runtime/activation-policy-engine.md` | `028bc3b6…` | `11ee1a70c7cae7c7bf64b97e0d8c879db68c6dae` | `ce15bec184f0f358d84df91987de04a70216ad41` | 否 |
| 2 | `05-memory-runtime/retrieval-engine.md` | `e7220ec1…` | `38fb72395166b52d8c1b0380757110ecc508cc05` | `c49c9c9272d04dddc29885c9aa0ada28d3d15e1c` | 否 |
| 3 | `05-memory-runtime/runtime-overview.md` | `dd98fda4…` | `80879fd3ed23b2f4545e186b8bd3626c80960c70` | `d084c463b7527e8ee364557ae941c7d19197b1d6` | 否 |
| 4 | `05-memory-runtime/runtime-scheduling.md` | `ae879343…` | `cfbd78e7c0381f493ac0d9cd104709b8dbbec6bf` | `05e4b4b78eda3dfa260dd95bbbaf6fc57a85f861` | 否 |
| 5 | `05-memory-runtime/working-set-and-cache.md` | `f5ee3115…` | `a4d8af1c59ad8fc0b118d6818928478f68fa919a` | `b6ec474256f703fb81a6b60b15ad0b453e3d5b9f` | 否 |
| 6 | `docs/en/05-memory-runtime/activation-policy-engine.md` | `43aa4de7…` | `cbf018fb4f2454ebbc9db1d5cc4dc05fc5269bea` | `39012b82c6ce69f0b774d2d89fcf398d5f74666b` | 否 |
| 7 | `docs/en/05-memory-runtime/retrieval-engine.md` | `2e1878d6…` | `e293c4704421cfaea7ff0557ea20817623e5de1e` | `12dbc2f2c811e7d61eb415ccc7f7e463c13019d2` | 否 |
| 8 | `docs/en/05-memory-runtime/runtime-overview.md` | `ae4af419…` | `d65c4508e2ca492f99eaf796acb5ae71f9564208` | `244a3b6ab34a3e89a2c04a213a1500516b8ad826` | 否 |
| 9 | `docs/en/05-memory-runtime/runtime-scheduling.md` | `833bebae…` | `c2b2b22aa8eb7447e23feca43f398c9038045069` | `ab8c4364d87f9e9f1feda7ce091c00ac4d338f67` | 否 |
| 10 | `docs/en/05-memory-runtime/working-set-and-cache.md` | `8cce12a5…` | `fc2b4dc78dcd2c700f2cfc8073b7dfc17be3773c` | `8cac511c3bb0213313ba63772f5d0c80f7a0be7b` | 否 |
| 11 | `docs/zh-CN/05-memory-runtime/activation-policy-engine.md` | `9d66e2d9…` | `f2506ece4b77e328fba23b139492f00b171fb8ed` | `b71c72eaa4e28e04e22beb1e1f8f8ac79be221b0` | 否 |
| 12 | `docs/zh-CN/05-memory-runtime/retrieval-engine.md` | `9ff6b535…` | `e6a2c63e1eb773566d3412467e006b9c1465e0e4` | `9ed86618decfd8538d3d4af21ea0b4df683d2fe1` | 否 |
| 13 | `docs/zh-CN/05-memory-runtime/runtime-overview.md` | `9e72ed4a…` | `cfb77ea85655b217bba1cd57b07b35508e9eeef0` | `f7351faf3d126f28dcb427f8c986eb4c5ac8d89a` | 否 |
| 14 | `docs/zh-CN/05-memory-runtime/runtime-scheduling.md` | `e0f9735e…` | `f4c5e27d6115bdc6cfb47ee39ef5423404f22cea` | `f12ed42732e195e3ff0f0a937603e1d432eb6346` | 否 |
| 15 | `docs/zh-CN/05-memory-runtime/working-set-and-cache.md` | `4851237c…` | `4e2772b968672590a6268f1b46dbef8ee347644a` | `7d917c6cadb983d719c135bbfc42eaf5a574a8d0` | 否 |

### C3. 仍然成立的部分

- 15 个路径在 `origin/main` 上全部存在；5 个 Canonical 与 10 个镜像都在，复原本身是真的。
- 把每个 Canonical 源 blob（`1908ce4d:<path>`）与 `9142698f:<path>` 的 blob 逐行对比：删除 0 行，新增只有 frontmatter（47 / 48 / 53 / 47 / 48 行），与 `FRONTMATTER_ADDED; source body retained unchanged` 一致。
- 无法验证的是新 blob 被记下的身份：15 个不存在的 SHA 不可能标识这 15 个被复原的文件。

**结论：`NEW_BLOB_IDENTITIES_NOT_VERIFIABLE`。** `verification_status: Verified` 及其说明（"Source and mirror blob identities … recorded"）按字面不成立：新 blob 一列记下的身份在本仓库中不可解析，也与它所声称标识的文件不符。
