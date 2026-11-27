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
        - "docs/zh-CN/14-ai-development/work-items/AID-2026-105/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "基于 main 533d8646a3fb32b0a1c9d3ed40c01bce33a76b17 的 GitHub 回读形成证据清单；只记录缺口，不声称验收通过。"
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
    canonical_scope: "Issue #1189 验收证据清单的中文镜像"
    canonical_scope_id: "ai-development/issue-1189-acceptance-evidence"
    canonical_scope_keywords:
      - approval-provenance
      - owner-acceptance
      - joint-acceptance
      - evidence-gap
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-105/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-105/evidence.md"
---

# Issue #1189 — 验收证据清单

- Work Item：`AID-2026-105`
- ID 状态：`PROVISIONAL`
- 首次证据回读：`main` 提交 `533d8646a3fb32b0a1c9d3ed40c01bce33a76b17`；创建 PR 后同步基线：`main` 提交 `df54ed60321e2958c50e9649963608cb3cb3f3b1`；最新同步基线：`main` 提交 `2d52b0c81dc1b779e49516fceb69d89cdc1d9c31`。
- 基线日期：2026-11-26
- 归属：`user-authorized operator (delegated by account owner)`
- 归属说明：受授权代理登记；**代理登记，非自然人 Owner 签署**
- 性质：仅文档证据清单。它不是新的批准、Owner 接受、联合接受、治理批准或关闭 Issue 的裁决。

## 1. 结论

#1189 不只是缺少一条批准记录。2026-11-26 已记录一项新的、可归属的批准事件，由 PR #1256 承载并合并为 `64bce1321a33e8f0d70949f7bb5869c5f250522a`。剩余验收缺口是：尚无针对当前精确版本的责任 Owner、依赖/联合 Owner 与治理批准人的验收记录；版本/镜像一致性及治理检查证据也尚未闭合。

现有证据**不支持关闭 #1189**。Issue 仍保持 OPEN。

## 2. Issue 验收要求与证据判定

以下要求来自 Issue #1189 的 Acceptance criteria 及后续 DEC-13 验收清单。“已记录”只表示存在记录；不表示代理处置等同自然人签署，也不把未执行检查改写为 PASS。

| # | 验收要求 | 当前证据 | 判定 |
|---|---|---|---|
| 1 | 当前批准状态有可归属、版本固定的证据支持，或由授权决定更正状态。 | AID-2026-096 批准记录；PR #1256 合并提交 `64bce1321a33e8f0d70949f7bb5869c5f250522a`；原六个批准 Git blob pin 与六个正文 content-hash 见 §3。当前 `main` 六个 Git blob 在 `44b57170b86c7f3e56744da756ed24744b1c659c` 的元数据迁移后已不同；该提交已包含于 main 合并提交 `533d8646a3fb32b0a1c9d3ed40c01bce33a76b17`。 | **EVIDENCE_REQUIRED** — 需解决 AID-096“任何元数据变化都产生新 blob 并需要新批准事件”的表述，与后续删除两个废弃空元数据键之间的关系。取得授权处置，或重新 pin / 批准当前六个 blob。 |
| 2 | 不得虚构或推断批准人身份、日期。 | AID-2026-096 记录批准归属为 `user-authorized operator (delegated by account owner)`，指定来源为 account owner statement（2026-11-26），事件日期 2026-11-26，类型为 `NEW_APPROVAL`；Issue 评论 #7185429832 记录相同信息。 | **DOCUMENTED_WITH_LIMIT** — 代理归属与事件日期已记录；这不是自然人 Owner 签署，也不能替代单独的 Owner 验收清单。 |
| 3 | 对 P-01–P-16 与 Architecture Invariants 集合分别明确批准范围。 | AID-2026-096 批准证据将 Design Principles 与 Architecture Invariants 两个根文档及其 EN/ZH-CN 镜像列为 Full-document 范围，并列出六个精确 path/blob。该记录明确排除 P-01–P-16 的实现符合性。 | **DOCUMENTED_WITH_LIMIT** — 文档级范围已记录；未声称实现符合性。当前 blob 对账仍按第 1 项开放。 |
| 4 | 两份 canonical 文档有可归属、版本固定的批准证据，或有授权状态更正。 | 两份 canonical 文档的元数据为 `Approved`，含批准归属/日期，content-hash 值与 AID-096 记录的正文 hash 相同。但当前六个 Git blob ID 与批准记录中的六个 Git blob ID 不同。 | **PARTIAL / EVIDENCE_REQUIRED** — 正文 hash pin 仍被记录，但当前 Git blob 并非批准记录列出的精确 blob。不得推断发生了新批准。 |
| 5 | EN/ZH-CN 镜像携带与 canonical 文档相同且已验证的状态与 source pin。 | 当前六份文档均显示 `decision_status: Approved`、相同代理归属/日期和 `normative_status: Normative`。但六份均为 `evidence_verification.verification_status: Unverified`；canonical 根文档的验证备注仍称不存在正式批准记录；Architecture Invariants 根文档及英文正文仍称其为提议内容、等待单独批准。 | **EVIDENCE_REQUIRED** — 必须协调过期陈述，并在六个精确当前 blob 上重新核验语义与 source-revision pin。元数据相同不等于语义镜像一致。 |
| 6 | 治理检查应能检测缺少批准 provenance 的 Approved 决策，包括缺少 approver/date 以及未验证状态。 | 当前 `scripts/check_document_management.py` 的 DM-03 要求 Approved 文档具有 version、scope type 和 applicability。检查器会验证 verification-status 枚举，但不要求 approver/date 非空，也不要求状态为 `Verified`。Policy 的 M-02、M-03 明确将批准真实性和证据支持留给人工审查。 | **EVIDENCE_REQUIRED** — 当前检查器未执行该项验收要求。本 Work Item 不改变 validator 语义；需单独授权的 checker/test 修改及原始 CI 输出。 |

## 3. 批准记录与当前精确版本

### 3.1 PR #1256 承载的批准记录

已合并批准证据位于 `14-ai-development/work-items/AID-2026-096/approval-evidence.md`（当前 main blob：`bff9a63ad88e027e92529bcc4001250840dade8d`）。其记录：

- 批准事件：`NEW_APPROVAL`，日期 2026-11-26。
- 批准归属：`user-authorized operator (delegated by account owner)`。
- 指定来源：account owner statement，2026-11-26。
- 范围：Design Principles 与 Architecture Invariants 的全文批准，分别包含 EN/ZH-CN 镜像。
- 排除项：P-01–P-16 实现符合性、runtime、validator、部署与生产符合性。
- 承载合并：PR #1256，merge commit `64bce1321a33e8f0d70949f7bb5869c5f250522a`。

AID-2026-096 原批准 Git blob SHA-1：

| 路径 | AID-2026-096 记录的 blob |
|---|---|
| `00-governance/design-principles.md` | `352b969fa8c07ad1f2848797f06404293242db13` |
| `00-governance/architecture-invariants.md` | `3c64217fde34fe67f463856b648a3e8a935a1654` |
| `docs/en/00-governance/design-principles.md` | `50d1d1d0907f25e2104414ba9bb48a31fb470b1d` |
| `docs/en/00-governance/architecture-invariants.md` | `ca7052afa486ce124e180c63812e082a6def5ebc` |
| `docs/zh-CN/00-governance/design-principles.md` | `cf6ce6c08970dea58e3a93514cea1f801e55a666` |
| `docs/zh-CN/00-governance/architecture-invariants.md` | `de534192ce8c343318d7da4add21daf0bbf1e04b` |

同一记录列出的批准正文 content hash（这些值仍保留在当前文档的 `approved_version.scheme: content-hash` 字段）：Design Principles 根文档 `273f048d8dd3401ec62e2c177fa00787ab6f6cb855e190b471b3a0c7f3b81523`；Invariants 根文档 `6df99f23052dd5475d22d397cdee160436464dc3a95946fe6d6e12f93aea1071`；EN Design Principles `e467d7cf3e8feb0457843b5f4f0fd038b01608c32a9fbe35e585cc41e49c665a`；EN Invariants `6b818d9b1884530bdf208507d6a7913699c8598d4c0f351f238cfaff449c0a3a`；ZH-CN Design Principles `7cd923872a16ec0b01174798614d6ccf867b20fa18edfe9c3c08b4f3e31e3e00`；ZH-CN Invariants `88bbebd033e0b5669bafc83c71afa2831cebb4a2e3a6cfa47573cf6b3259b293`。

### 3.2 当前 main 精确 Git blob

下列每个当前 blob 均从 `main`（提交 `2d52b0c81dc1b779e49516fceb69d89cdc1d9c31`）重新读取。main 经 PR #1291（AID-2026-106）从 `df54ed60321e2958c50e9649963608cb3cb3f3b1` 前进后，六个 blob SHA 均未变化。

| 路径 | 当前 main blob SHA-1 | 是否匹配 AID-096 Git blob pin |
|---|---|---|
| `00-governance/design-principles.md` | `9fb729a4bd6ebcfa9576e5318804a65e2a95abe2` | 否 |
| `00-governance/architecture-invariants.md` | `15daf882febb71e4cda9317bdd7f0538fbae2404` | 否 |
| `docs/en/00-governance/design-principles.md` | `214b8f376497cc3c3c04e2d6bce2951427a84f2c` | 否 |
| `docs/en/00-governance/architecture-invariants.md` | `a223001bece95bcdb1d41407910d5df7e1ffd313` | 否 |
| `docs/zh-CN/00-governance/design-principles.md` | `40b5984eeae38795efe51da25bb2a3708a6d1135` | 否 |
| `docs/zh-CN/00-governance/architecture-invariants.md` | `97c652b9d30a53a10036a2030419432ddd41c144` | 否 |

当前 main 合并提交 `533d8646a3fb32b0a1c9d3ed40c01bce33a76b17` 的一个父提交是 `44b57170b86c7f3e56744da756ed24744b1c659c`。该提交从 schema 和文档库中删除废弃的空 `approval_scope.included_sections` 与 `approval_scope.included_assets`。其对六份已批准文档的 diff 只修改 frontmatter，没有显示正文行变化。GOV-DOC-002 的正文 hash 算法会剥离 frontmatter，因此正文 hash 可以保持不变，而 Git blob ID 已改变。这解释了为何两个 pin 会不同，但**不能替 AID-096 的更严格表述（“任何内容或元数据变化都会生成新 blob 并需要新批准事件”）作出该 schema 迁移是否可免于重新批准的裁定**。本证据清单不作此推断。

## 4. 其他 main 证据与未解决矛盾

| 证据 | 当前 main 路径与 blob | 能证明什么 / 限制 |
|---|---|---|
| 先前 Issue 审计 | `14-ai-development/work-items/AID-2026-092/ISSUE-1189-approval-provenance.md`，`fbaae7eb5a175944cb89d12fe8949aa1535c9d98` | 其基线上的历史“未发现批准”结论。它早于 AID-096 新批准事件，现已被后续事件取代；不得把旧 blob pin 当作当前 pin。 |
| DEC-13 证据 | `14-ai-development/work-items/AID-2026-093/evidence.md`，`69ce490157adb1e018e5608e7405c6ef4d233de3` | 将 DEC-13 评论 #7174867715 读回为 10 项未勾选 / 0 项已勾选，并记录 20/20 评论回读；这证明清单已登记，不证明已接受。 |
| DEC-13 登记表 | `00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md`，`4810c6f8d3b5676a44288dea5782681e0745af6f` | 明确区分方向批准、Owner 接受、规范生效、实现授权、实现验证和生产符合性。 |
| A–I / Storage 矩阵 | `00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md`，`a180459fa70f713de9232f372b94c8feb2c0c90d` | 记录 10 个角色的代理处置：3 ACCEPT / 7 CONDITIONAL / 0 REJECT。它明确自然人 Owner 接受数为 0，DEC-13 / Gate A 验收仍开放。 |
| EN / ZH-CN DEC-13 登记表镜像 | `docs/en/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md`，`dcae8a7cb5c6e03bf220d1d681744cc68361e87d`；`docs/zh-CN/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md`，`49b3aff58991b77545ab143d12782b65e71a5a69` | 镜像文件存在不证明语义 parity 或 Owner 接受。 |
| EN / ZH-CN A–I / Storage 矩阵镜像 | `docs/en/00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md`，`5e6a388be1e55a0acaa49e67006f8ad3404a1a72`；`docs/zh-CN/00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md`，`149f3657e980826b1b44d560b83e71f837c8ffab` | 镜像文件存在不证明语义 parity 或 Owner 接受。 |
| AID-096 manifest | `14-ai-development/work-items/AID-2026-096/manifest.yaml`，`df16f4ad6d563f3f2a9a4596ee94a855b8431e19` | 状态为 `APPROVAL_RECORDED_OWNER_ACCEPTANCE_PENDING`；未声称 Owner / 联合接受已完成。 |
| AID-096 session evidence | `14-ai-development/work-items/AID-2026-096/session-evidence.md`，`45a1c1aebb54a93b28c2446c9ade96d6abc84654` | 记录代理归属、prompt/session provenance 限制及非自然人签署边界。 |
| AID-096 prompt snapshot | `14-ai-development/work-items/AID-2026-096/prompt-v1.md`，`042f0f21e7d2410f01d5aeca4cbb2d4597422f11` | 记录代理批准任务及其明确范围/排除项。 |
| Issue #1189 决策/验收评论 | 评论 `7174316473`、`7174519803`、`7174867715`、`7185367827`、`7185429832` 和 `7186346059` | 分别记录不批准方向、D-12、DEC-13 未勾选清单、保持 OPEN 的审计、新批准事件及合并后状态；最新批准评论仍明确 Owner/联合接受待完成。 |
| Work Item index | `14-ai-development/work-items/INDEX.md`，`02bacd620ea147bd9b2fb63868648d8b7dd55474` | AID-096 Acceptance 栏仍为 pending；AID-093 记录的是代理处置及自然人接受数为 0。 |

### 4.1 DEC-13 责任 Owner 与联合接受

Issue 评论 #7174867715 指定 Accountable decision Owner C，以及 required dependent/joint Owners A 与 governance approver。清单分别列出 canonical source 更新、EN 镜像核验、ZH-CN 镜像核验、交叉引用/依赖 ADR、独立验收标准、验证方法/原始输出、Accountable Owner 接受、每个 required dependent/joint Owner 接受、治理批准及限制/失败/恢复文档等未完成项。

AID-2026-093 的证据回读记录 DEC-13 有 10 项未勾选、0 项已勾选。A–I / Storage 矩阵中的 10 个角色处置均明确是代理登记，不是自然人签署；自然人 Owner 接受计数为 0。因此，Owner C、联合 Owner A 和 governance approver 针对当前精确版本的接受仍为 **EVIDENCE_REQUIRED**。代理处置不能关闭这些验收框。

### 4.2 当前文档一致性观察

- 两份 canonical 文档的 frontmatter 仍为 `evidence_verification.verification_status: Unverified`。
- 两份 canonical 根文档的 `last_verification_note` 仍声称不存在正式批准记录/批准人/日期，与后续 AID-096 新批准记录冲突。
- Architecture Invariants 根文档与英文正文仍将不变量称为提议内容、等待单独批准，和当前 Approved / Normative 元数据冲突。这是正文级矛盾，不只是 blob ID 不同。
- EN Design Principles 镜像保留 source revision 字符串 `9792e189d63fbbc3694ab891fc4aeba5143b3b1c`；ZH-CN 对应文档也带有 source revision 字符串。必须在同一精确提交上重新回读这些 source pin 与六份正文的语义一致性。

本 Work Item 不修正这些观察。修改 canonical 批准元数据或规范正文需要相关授权决定及单独审查。

## 5. GOV-DOC-002 检查器覆盖范围

当前 main 源 pin：

- `scripts/check_document_management.py`：blob `4221de3cdf59c4985b19fd258163780866271167`。
- `00-governance/architecture-document-metadata.schema.yaml`：blob `a3ce83d6afc38eb960c39b5636704798cbd299cd`。
- `00-governance/architecture-document-management-policy.md`：blob `3f800279708bf6c101ee5295158b62ef137e0758`。

检查器的 DM-03 要求 Approved 文档绑定 `approved_version.value`、`approval_scope.type` 和 `approval_applicability`。Schema 将 `approver` 与 `decision_date` 声明为 nullable string，而不是非空必填字段。检查器只将 `evidence_verification.verification_status` 校验为枚举值，并接受 `Unverified`；它不要求 Approved 必须为 `Verified`。Policy 的 M-02 与 M-03 明确将批准真实性和证据支持留给批准人/审查者人工判断。因此，当前实现不满足 Issue #1189 第 6 项的原文要求。

**最小路径：** 单独授权的治理变更必须定义 Approved + approver/date 缺失及 Approved + Unverified 的精确规则，增加正向/负向 fixture（含 mutation control），并在该变更的精确提交上提供所需 CI job 结果。本 AID-2026-105 仅做证据登记，不修改 checker、schema、tests、workflow、runtime 或 validator 语义。

## 6. 最小闭合路径

1. 责任 Owner C 对当前精确版本的 Design Principles 与 Architecture Invariants 作出接受或拒绝，并分别明确 P-01–P-16 与 I-01–I-24 范围。
2. required joint Owner A 与 governance approver 针对同一组六个当前 path/blob 和精确证据包，分别记录其权限范围内的接受。每条记录必须保留真实归属；代理登记不能伪装成自然人签署。
3. 授权决策人裁定 #904 的元数据-only schema 迁移是否按 AID-096 的 exact-blob 约束视为批准中性；否则提供新批准事件/更新后的精确 blob 范围。本记录不作推断。
4. 协调矛盾的 verification notes 与 proposed-status 正文，并在一个提交上重新核验 Canonical/EN/ZH-CN 语义 parity 与 source revision pins。未经授权不得更改规范内容。
5. 单独授权并实现 GOV-DOC-002 对 approver/date 缺失和 Approved 未验证状态的检查；附原始测试与 CI 输出。
6. 独立核验全部 DEC-13 验收项，附精确 Head 验证输出，然后才考虑关闭 #1189。本证据记录不声称生产或 P-01–P-16 实现符合性。

## 7. 明确不主张的事项

- 不识别或推断任何历史批准人。
- 不声称自然人 Owner 或 governance approver 已接受。
- 不把代理角色处置改写为人类签名。
- 不声称当前 Git blob 等于 AID-096 原批准 blob。
- 没有证据的语义 parity 或治理检查不标记为 PASS。
- 本 Work Item 不修改 runtime、validator、schema、tests、workflow、canonical source 或生产状态。
- Issue #1189 继续保持 OPEN。
