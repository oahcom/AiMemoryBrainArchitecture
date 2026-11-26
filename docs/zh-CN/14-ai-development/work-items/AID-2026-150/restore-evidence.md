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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Work-item evidence; facts pinned to repository observations; no Owner acceptance or natural-person signature asserted."
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
    canonical_scope: "Exactly three D Memory Brain normative roots restored; 57 source paths deferred and 11 mirror pairs held pending decision"
    canonical_scope_id: "ai-development/aid-2026-150-d-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-150"
      - "memory-brain"
      - "normative-root"
      - "blob-comparison"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-150/restore-evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-150/restore-evidence.md"
    zh-CN: null
---
# AID-2026-150 — D Memory Brain 规范根恢复证据

## 范围与归属

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- Main 基线：`248cef62410cb4a412efb2d83326a1ce32345765`
- Main tree：`f14c234f98b5fa046c2f84bbbe7b5f7dd29b1945`
- D 源分支：`session-d-memory-brain-2026-11-16`
- D 源分支 HEAD：`b525e1f8fee2471a131e4a38efda99804045e424`
- D 源 tree object：`258f53ab74a6618493a15e6a0d190467997bec43`
- 工作项：`AID-2026-150`；账号固定号段 `AID-2026-150..159`；确认没有同号 Issue/PR 载体后选择 `AID-2026-150`。
- 归属：账号所有者授权的代理执行；不代表自然人 Owner 签署。
- 本记录仅证明源文件恢复与路径分类，不授予 Owner 接受、规范批准、实现授权或生产符合性。

## 1. 三份规范根 Blob 对照

| Canonical 路径 | 源 Blob SHA | 恢复后 Main Blob SHA | 正文处理 |
|---|---|---|---|
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `df07e7cc85ad68d35609f3499bd69ca7fc44d9c2` | `FRONTMATTER_ADDED`；源正文逐字节保留 |
| `03-memory-brain/commit-cursor-semantics.md` | `4688a0ca487bf4d853c7f0220408abe8d743d159` | `2c68161d039310b8df0e1387b4f1111ed74699db` | `FRONTMATTER_ADDED`；源正文逐字节保留 |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `f9555568b1c7b44f59f2d32f142e87e9582dbba5` | `FRONTMATTER_ADDED`；源正文逐字节保留 |

三份源 Blob 原本均无 GOV-DOC-002 frontmatter。恢复文件只在正文前增加有效 metadata；剥离新增 frontmatter 后，与源 Blob 正文逐字节相同，三项实测均为 `true`。因此新 Blob SHA 与源 Blob SHA 不同是预期结果。

三份文件均保持 `decision_status: Draft`、`normative_status: Informative`。`canonical_status: Canonical` 只表示恢复后的仓库规范路径，不表示 Owner 批准。

## 2. 现有 EN/ZH-CN 镜像处理

Canonical Memory Store 和 Commit Cursor Semantics 两对现有镜像予以保留。只增加 GOV-DOC-002 metadata 和三方 counterpart 引用；四份镜像正文逐字节未改。

| 镜像 | 原 Blob SHA | 新 Blob SHA | 正文 |
|---|---|---|---|
| EN canonical store | `414fe03fd40fb8ad46061d2d8c7d29ba2667f252` | `416bb38b961c6f5628857be23d12f7a475652a19` | 未改变 |
| ZH-CN canonical store | `34e0755a079f085df65c2a180cc59b6aaea7ea78` | `ea16b0c0527b63b1de35f76842d3d49866353dee` | 未改变 |
| EN cursor semantics | `2de7fe35229372ae5b06093e5e031c2c243fbd7c` | `4199bc66e4fc81fc460237c8bd65817f6c2288f2` | 未改变 |
| ZH-CN cursor semantics | `2589cecb258e029c5a18796d019ad5b9806cfbdc` | `bf9529b97ba65c2eacb627f4f5939bfb359c0006` | 未改变 |
| EN Fence 导航 Stub | `9c054932994bb078e2834df8bd66f73895aa04f5` | `5f3334322170c447868b2d20b4b55728f7a8dc35` | metadata + 源状态/路径修正；仍为非规范导航 Stub |
| ZH-CN Fence 导航 Stub | `15c60b9a72632975f89e507520eaf32a0b9e603d` | `5f8c8f9d4d61e4181fc7410165a24056f9127a01` | metadata + 源状态/路径修正；仍为非规范导航 Stub |
| EN Fence 导航 Stub | `9c054932994bb078e2834df8bd66f73895aa04f5` | `5f3334322170c447868b2d20b4b55728f7a8dc35` | metadata + 源状态/路径修正；仍为非规范导航 Stub |
| ZH-CN Fence 导航 Stub | `15c60b9a72632975f89e507520eaf32a0b9e603d` | `5f8c8f9d4d61e4181fc7410165a24056f9127a01` | metadata + 源状态/路径修正；仍为非规范导航 Stub |

EN 与 ZH-CN 文件保留原有章节结构和类型化合同词汇。本次属于有界结构对应检查，不声称完成逐行认证翻译审查；没有重写任何镜像正文。

## 3. Fence 冲突判定

D 原始源 Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` 是一份完整的 74,846 字符文档，标题为 “Forget Fence Atomicity, Producer Admission and Publication Gate”。

Main 当前同名 EN/ZH-CN 文件不是这份完整文档：
- EN 导航/解除引用 Stub：1,910 字符，旧 Blob `9c054932994bb078e2834df8bd66f73895aa04f5`。
- ZH-CN 导航/解除引用 Stub：1,224 字符，旧 Blob `15c60b9a72632975f89e507520eaf32a0b9e603d`。
- 两份 Stub 均明确写明历史源 Blob 被保留，但当前没有可解析的规范源路径，并链接到四份拆分文件。
- EN Part 1–4 分别为 21,284、12,040、30,973、12,818 字符，合计 77,115 字符。各 Part 包含独立版本的 Phase 3.6 / JF-10 增补，不是对 74,846 字符源文件的无损分割。字符总数不同本身不能证明语义等价。

**处理裁定：** 将原始源正文恢复到规范根路径。不得用短 Stub 替代完整规范，也不得把 Part 1–4 拼接成合成替代品。EN/ZH-CN 导航 Stub 对只增加 GOV-DOC-002 metadata，并小幅修正源状态/路径，使其指向已恢复根文件；其正文仍是非规范导航页，不是完整翻译。Stub 对及四份拆分式 EN/ZH-CN 镜像仍列为 `ORPHAN_MIRROR_PENDING_DECISION`，等待 Owner 对语义归属作决定。根源路径选择已解决，根级 Fence metadata 使用 `canonical_conflict_status: None`。不创建或修改任何 README。

## 4. 其余 57 个 D 源路径——全部不恢复

以下 57 条路径来自 AID-2026-107 §10.4 的 D 分支逐文件清单。分类原样保留：29 条 `HISTORICAL_PHASE_RECORD`，28 条 `UNDECIDED`。本次均不复制到 main。

| D 源路径 | 源 Blob SHA | 分类 |
|---|---|---|
| `03-memory-brain/d-forget-normative-index-proposal.md` | `5d1000d93217012d52a5b44c8f6b4343c42f0397` | `UNDECIDED` |
| `03-memory-brain/decision-change-log.md` | `8e8380b8c179ca5176c510a13d496e0197e565b9` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/entity-and-relationship-manager.md` | `14697658d4d873381ca8d4e3bed7c1170368ec29` | `UNDECIDED` |
| `03-memory-brain/forget-fence-and-completion-contract.md` | `1f0391bc49d007c44ec74165bd33d37412cc7990` | `UNDECIDED` |
| `03-memory-brain/gate-release-currentness-cas-and-producer-admission.md` | `7f2861d9441b9be6c8e69f41fd0276636be483a8` | `UNDECIDED` |
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `UNDECIDED` |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | `UNDECIDED` |
| `03-memory-brain/memory-versioning.md` | `af747f339d03bdd4684b6ed60fca05957dc8e1fb` | `UNDECIDED` |
| `03-memory-brain/module-baseline-and-redlines.md` | `84e402f471d452c7dab63a7db344f86b5b57bd7c` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-cgh-applied-1.0-d-forget-fence-authority-confirmation.md` | `b5a0354d263185723954ffb952fdf0b005f59ba8` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` | `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-joint-forget-linearization-decision.md` | `1b6a312ecffd3947bbb4df59f902242482c98a40` | `UNDECIDED` |
| `03-memory-brain/phase-3.6-r1-r2-d-owner-gate-linearization-decision-candidate.md` | `a7cba2c72720bb7873d77f1a9d151df974605a9e` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.1-joint-defect-closure-d-addendum.md` | `53685b864fbbcbac010e60a67c59430be7f27fce` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.10-d-exact-version-recovery-cutoff-review.md` | `e03ca0db209fc8ac5b985e114a31c21fbb136859` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.14-d-exact-review-storage-v3.2.4-successor-manifest.md` | `55ffb6da64023b5f2c7a3d1a8d6bb562de70ab25` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.2-jf10-reference-model-consumption.md` | `a3555162827bd1cc7cf4c0918d4ab9b6ce94c8bb` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.3-d-coc-durable-protocol-acceptance.md` | `e2a74d138ccebfb4266d19ea0c0c03f58a815bf5` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.4-d-prepared-participant-gid-fence-acceptance.md` | `3cba777f8951a5d88e27a314a37c000aeedc19d0` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.5-d-restore-control-highwater-acceptance.md` | `211e54acfb4573b1c51d96f07af297671dfc4c4b` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.6-d-forget-semantic-authority-addendum.md` | `a384ffb4fff7de9b35ba6b3011d2779ad529573d` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.7-d-exact-version-owner-decision.md` | `3603aff5881dd8a375f22aad67b90ade312bbfad` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.7-d-owner-local-gate-admission-release-amendment.md` | `84f6875ce382fb37f35b01140c19a482fcfa9fab` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md` | `2d95099a2e19a8cbec325925b70da576f73d9899` | `UNDECIDED` |
| `03-memory-brain/phase-3.6.8-d-exact-version-owner-rereview-decision.md` | `35fa09e9bd5d15e6ad092c0c0ace52ca02a48692` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.8-d-exact-version-r1-r4-rereview-decision.md` | `5aafe8a977ec0cfa1287e7af8c47c8f67ee3a501` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.6.9-d-r1-r2-exact-version-delegated-disposition.md` | `7ab4f53c497bce597e422a6df9a85b31a2352602` | `UNDECIDED` |
| `03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` | `4c01713bc8793a8926ef18b625b72d132572173d` | `UNDECIDED` |
| `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` | `UNDECIDED` |
| `03-memory-brain/phase-3.8.10-d-review-h-full-path-forget-clearance-callback.md` | `fd576d05a6dbf18ce4920b6a1ce44b957f9f1850` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.11-d-exact-review-h-expanded-full-path-fence-storage-callbacks.md` | `7a9ed2bcf7fd34edc576a4a1be7f4388ee551b43` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.11-d-review-h-expanded-full-path-fence-clearance.md` | `1ce8f25db1971b692112e47aeae431af4e69b5e5` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.12-d-exact-rereview-h-c-p0-projection-test-39-method-ci.md` | `02b74a14c2c5ad35553b41eb7831b6eadceb0ffa` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.12-d-exact-review-h-42-test-cp0-nullable-intent-currentness-boundary.md` | `2bf4514fe7972b72f6c1f904e461f86488d04cda` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.12-d-review-h-nullable-coc-not-invoked-and-p0-matrix.md` | `8f064d29f4868ad5ad598aa49f12bf7709b9a993` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.13-d-review-h-outer-envelope-authenticated-ingress-gate.md` | `152627e00b96355e2ff370acd643a51168c4c78c` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.14-d-exact-review-h-applied-delivery-evidence-replay-fence.md` | `1ebbf827f92ee9244963a550855283421837a1b0` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.14-d-review-h-explicit-outer-signature-profile-requirement.md` | `4b512ad717296c6f8ab5b074048f2169dd9f6df2` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.2-d-recovery-join-and-visibility-exact-review.md` | `6f39475784458d34b347d8566824fa22b308b477` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.3-d-gate-release-currentness-exact-review.md` | `7d45e663b471b7d82a0af8ca5b2e1f14c88f2315` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.4-d-exact-review-h-owner-membership-proof.md` | `0edd96d07960292d938656d5d8a20095750f4cf1` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.4-d-owner-snapshot-membership-proof-contract.md` | `59ff706470f98617bda12397d8236377c73b067d` | `UNDECIDED` |
| `03-memory-brain/phase-3.8.5-d-exact-review-h-unified-1.2.13-owner-proof-compatibility.md` | `84196906cad92367a60c79a74dd241fd80abb96c` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.5-d-recoveryjoin-1.0.2-unified-1.2.12-wire-adoption-amendment.md` | `46b6abd94f3396e5eef7d7456f9b62a3865d4ce2` | `UNDECIDED` |
| `03-memory-brain/phase-3.8.5-d-storage-logical-serialization-topology-review.md` | `7b44f2b3e346eaa34840797bec391465af6130a3` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.6-d-exact-review-unified-1.2.13-recoveryjoin-1.0.2.md` | `1f03f3a83dda3fc1cc364ae9d2d18a3f1b96b590` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.6-d-recoveryjoin-1.0.2-membership-proof-p0-crosswalk.md` | `c4adf827dd62d44c43b8e871dec4835581508adf` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.7-d-exact-review-h-1.2.14-recoveryjoin-1.0.2.md` | `55ae7bc33b37f0e729949fdd2a694eb6211bbc55` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.7-d-exact-review-h-unified-1.2.14-fence-high-water-and-membership.md` | `49d572d4c35cb393009996606f5187eec5c571e5` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.8-d-exact-review-h-unified-1.2.14-current-schema-fence-high-water.md` | `6aca7d020caecf3c69debf614c903bf469583260` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.8-d-review-storage-serialization-anchor.md` | `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.9-d-exact-review-h-authority-join-mapping-1.2.14.md` | `40fee15d7e42d68da231ea161896f85df2921669` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.8.9-d-review-h-forget-clearance-verifier-seam.md` | `53613f383d064d25ac9f34a00e457f86730f16bf` | `HISTORICAL_PHASE_RECORD` |
| `03-memory-brain/phase-3.9-d-forget-terminal-semantics-and-linearization-closure-proposal.md` | `9c02b5680317f0092788ad0da66d621338b1c54c` | `UNDECIDED` |
| `03-memory-brain/tests/test_phase_3_9_forget_reference_model.py` | `b712f15bdb3770a3075070f8f3fce573c70defcf` | `UNDECIDED` |

分类依据：
- `HISTORICAL_PHASE_RECORD`：阶段 Review/Re-review、Reference Model 或 Conformance 产物、决策变更日志和模块基线，仅作为流程/历史证据保留，不提升为独立规范根。
- `UNDECIDED`：实质性阶段决策/补充条款/合同、子系统或概览文档、测试及替代方案；现有证据不足以确定其控制性、是否已被取代或是否不再需要，恢复前必须由 Owner 裁决。

## 5. 11 对现有镜像——待裁决，保持不动

以下 11 组文件名对应的 EN/ZH-CN 两份文件均不作为 D Canonical 根导入。两种语言的现有文件保持原样；不创建或修改 README。

| 现有镜像对 | 分类 |
|---|---|
| `docs/en/03-memory-brain/README.md` + `docs/zh-CN/03-memory-brain/README.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/entity-and-relationship-manager.md` + `docs/zh-CN/03-memory-brain/entity-and-relationship-manager.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part1.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part1.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part3.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part3.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md` + `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part4.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-brain-guide.md` + `docs/zh-CN/03-memory-brain/memory-brain-guide.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-brain-overview.md` + `docs/zh-CN/03-memory-brain/memory-brain-overview.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-lifecycle-manager.md` + `docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md` | `ORPHAN_MIRROR_PENDING_DECISION` |
| `docs/en/03-memory-brain/memory-versioning.md` + `docs/zh-CN/03-memory-brain/memory-versioning.md` | `ORPHAN_MIRROR_PENDING_DECISION` |

不删除、不拼接任何镜像，也不把它们当作规范源。Fence 导航 Stub 对仅增加 metadata 并修正源状态/路径；语义归属仍待决定。其余 10 对孤儿镜像不变。`ORPHAN_MIRROR_PENDING_DECISION` 是清单处置状态，不表示内容无效。

## 6. 门禁与接受边界

- 将 `03-memory-brain` 加入权威 `NORMATIVE_ROOTS`，使三份恢复的规范文档进入双语/文档治理门禁。
- 两对已链接的 EN/ZH-CN 正文保持不变；metadata 现在指向根级源文件和兄弟镜像。
- Fence Stub 对为满足 metadata 闭合而结构性连接到已恢复根源，但仍是非规范导航 Stub，语义处置待定；Part 1–4 不登记为镜像。
- 不修改任何 README、Runtime 实现、Validator 逻辑、Schema、Test、Workflow、Deployment 或 Production 产物。现有双语检查器仅将 `03-memory-brain` 加入 `NORMATIVE_ROOTS` 范围清单；独立 Scope Registry 同步登记该 governed root。
- 本证据不关闭任何 Issue。除非平台独立改变状态，#1212 保持 OPEN。
- 独立审查人：`NOT_ASSIGNED`；Owner 接受：`NOT_GRANTED`。

PR #1320 已创建。初始分支创建后 main 前进到 d6cad634f1341a8943aa89dd5ef8bf75f6d56199；现将分支刷新到该 main，再运行最终 CI/合并。最终 Head、检查结果和 merge SHA 将在合并后的 #1212 评论中记录。
