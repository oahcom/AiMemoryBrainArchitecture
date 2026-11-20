# 证据链分级策略

- **文档 ID：** AI-DOC-EVIDENCE-TIERING
- **版本：** 1.0
- **状态：** PROPOSED（待项目治理权威正式采纳）
- **Owner：** G（流程架构）
- **英文对应：** [evidence-tiering-policy.en.md](evidence-tiering-policy.en.md)
- **上位依据：** AI-STD-001 §4.2（独立门禁证据）、AI-EXEC-001 v1.1（ADOPTED）、GOV-DOC-001
- **授权依据：** DEC-FIX-2026-P1-T4-GO-001
- **明确不作为依据：** AI-EXEC-002 v1.2（状态字段仍为 PENDING ADOPTION，其条件生效条款未被本策略引用）

## 1. 目的与定位

本策略按变更风险为证据链设定深度等级，减少低风险变更的证据开销，同时不放宽任何门禁。证据等级是**证据深度选择器**，不是状态轴、审查级别或生命周期阶段。

本策略的 **Level 1/2/3 指证据深度**，与相邻策略 `AI-DOC-BILINGUAL-TIERING` 的 **Tier 1/2/3（文档双语分层）**是两个不同刻度：前者决定必填证据字段，后者决定是否需要中英文对应版本（本策略 §7 引用后者）。两轴相互独立，任一轴的判定 MUST NOT 被用来推出另一轴。

三个维度必须保持独立：

| 维度 | 取值 | 决定什么 | 不得由其他维度替代 |
|---|---|---|---|
| 变更风险 | Level 1 / 2 / 3 | 证据深度（必填字段集合） | 不得由审查级别或变更规模推定 |
| 审查级别 | R0 / R1 / R2 / R3 | 独立审查与专业审查要求 | 不得由 Level 降低或替代 |
| 生命周期 | 12 状态 / 6 阶段 | 门禁里程碑与阶段归并 | 不受 Level 影响 |

任何 Level 均不得改变 VERIFIED、REVIEWED、INTEGRATION_READY 的独立门禁含义。证据缺失仍然 fail-closed。

## 2. 三级定义

| Level | 适用范围 | 必填证据 |
|---|---|---|
| **Level 1（严格）** | ARCHITECTURE、SECURITY、PERFORMANCE_CRITICAL、PUBLIC_API、DATA_MIGRATION、DOC_NORMATIVE；以及所有 R3 变更 | subject_head（40 位 commit SHA）、change_summary、design_doc、impact_analysis、test_log、review_record、rollback_plan、v3 绑定全套（protocol + subject tree 包含 + blob 一致 + **sidecar_path 与 sidecar_anchor**）、source_authenticity（NOT_VERIFIED 时须 authenticity.acknowledged=true） |
| **Level 2（标准）** | FEATURE、BUGFIX（有界范围、不改变契约） | subject_head、change_summary、test_log、review_record、v3 绑定（protocol + subject tree 包含 + blob 一致）、source_authenticity |
| **Level 3（轻量）** | DOC_EDITORIAL（不改变规范语义的编辑性文档）、OPS（非发布关键） | subject_head、change_summary、evidence.review_note、v3 绑定（protocol + subject tree 包含 + blob 一致） |

所有级别均 MUST 保留 40 位完整 subject_head 与变更简述；无例外。v3 绑定的具体范围见 §5：protocol、subject tree 包含性与 blob 一致性适用于全部等级；sidecar 锚点仅 Level 1 强制。`evidence.review_note` 是**指向确认记录的路径**，不是自由文本——自由文本无法被 Git 绑定。

## 3. 不可降级规则

1. **Level 1 强制底线**：凡属 R3、安全边界、授权、数据完整性、删除/遗忘、迁移、公开 API、架构语义或规范语义变更，MUST 为 Level 1。任何将其降为 Level 2/3 的判定无效。
2. **R2 不得自动降级**：R2 变更不得仅因改动规模小、文件数少或"看起来是文字修改"而降到 Level 3。确有必要时 MUST 同时提供三项：`downgrade_justification`（理由）、`downgrade_confirmed_by`（确认者，且不得等于 `assessed_by`）、`downgrade_confirmation_record`（须按 §5 第 6 条在 subject tree、工作树与 blob 三处校验）。任一项缺失或确认者为本人，均 BLOCKED。
3. **文档变更不等于低风险**：文档变更若改变规范含义、约束强度、接口/协议、数据模型、状态机或安全边界，MUST 升级为 DOC_NORMATIVE → Level 1。
4. **UNKNOWN 一律 BLOCKED**：无法确定分类时不得赋予任何 Level，判定为 BLOCKED / NEEDS_CLASSIFICATION，由有权 Owner 或治理授权者确认后重新判定。
5. **分类信任边界**：强制 Level 1 的类别（ARCHITECTURE、SECURITY、PERFORMANCE_CRITICAL、PUBLIC_API、DATA_MIGRATION、DOC_NORMATIVE）不得通过改标为 FEATURE/BUGFIX/DOC_EDITORIAL/OPS 而降级。凡声明为可降级类别（FEATURE、BUGFIX、DOC_EDITORIAL、OPS）者，MUST 提供 `classification_basis`（分类依据）、`classification_confirmed_by`（独立确认者，不得等于 `assessed_by`）与 `classification_record`（须按 §5 第 6 条在 subject tree、工作树与 blob 三处校验）；缺失或无法独立确认时 BLOCKED，不得默认相信申报者。`classification_basis` MUST 与实际变更影响对应（本次改动触及的文件、接口、边界或数据模型）；确认者 MUST 在 `classification_record` 中写明实际核对的对象与所得结论，仅复述申报标签不构成独立确认，判 BLOCKED。记录至少须覆盖三项：**核对对象**（被核对的文件、接口、边界或数据模型）、**核对结论**、**核对者**；三者缺一或只写「已确认」均不构成记录，判 BLOCKED。审查方 MUST 在其审查记录中逐项记录这三项的核对结果（Level 3 记入 `evidence.review_note` 所指向的确认记录）；缺项即 BLOCKED，且不得以「已审查」一句代替。
6. **不存在"自动通过"**：Level 只决定证据深度，不构成任何门禁的通过证据。

## 4. 判定与审计留痕

每条证据声明 MUST 记录以下审计字段，供独立审计复核：

| 字段 | 含义 | 机器强制 |
|---|---|---|
| `change_class` | 风险类别（枚举，见 §2） | 是 |
| `repository` | 声明所属仓库（owner/name），须与克隆的 origin 远程一致 | 是（不一致/无法核验即 BLOCKED） |
| `review_level` | 审查级别 R0–R3 | 是 |
| `evidence_level` | 1/2/3 | 是 |
| `assessed_by` | 判定人（Owner/会话标识） | 是（缺失即 BLOCKED） |
| `assessed_at` | 判定时间（含时区） | 是（缺失即 BLOCKED） |
| `rationale` | 判定理由（为何该 Level 足够） | 是（缺失即 BLOCKED） |
| `base_head` | 判定所依据的基线 commit（须为 subject_head 祖先） | 是（格式/祖先关系均校验） |
| `classification_basis` | 分类依据（为何该 change_class 成立） | 是（缺失即 BLOCKED） |
| `classification_confirmed_by` | 可降级类别的独立确认者（≠ assessed_by） | 可降级类别强制 |
| `classification_record` | 分类确认记录（须在 subject tree 中，并校验工作树/blob 一致） | 可降级类别强制 |
| `downgrade_justification` | 仅 R2→Level 3 时必填 | 该场景强制 |
| `downgrade_confirmed_by` | 降级确认者（≠ assessed_by） | 该场景强制 |
| `downgrade_confirmation_record` | 降级确认记录（须在 subject tree 中，并校验工作树/blob 一致） | 该场景强制 |
| `escalation_target` | 升级对象（分类不确定或需 Owner 决策时） | 否（记录用） |

缺少 `assessed_by` / `assessed_at` / `rationale` / `base_head` / `classification_basis` 中任一项的判定不得作为 Level 依据，检查器直接 BLOCKED。

## 5. 与既有证据基础设施的关系

1. **不替换、不削弱** 既有 applied-delivery-evidence validator 及其 CI workflow（本策略不修改 `.github/workflows`）。
2. **保留证据绑定协议 v3**：subject_head 必须是 commit 对象；证据文件必须位于 subject tree；工作树字节必须与 subject blob 一致。
3. **v3 校验范围按等级明确**（消除歧义）。本表只调整证据深度，**不改变绑定完整性**：前三项在全部等级强制，`sidecar` 项属 Level 1 的深度要求，其缺失 MUST NOT 被解释为证据可以脱离受审对象：

| v3 校验项 | 适用范围 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| `subject_head` 为 commit 对象 | ALL LEVELS | 强制 | 强制 | 强制 |
| 证据路径存在于 subject tree | ALL LEVELS | 强制 | 强制 | 强制 |
| 工作树字节 == subject blob | ALL LEVELS | 强制 | 强制 | 强制 |
| `sidecar_path` + `sidecar_anchor`（sha256 + commit message 锚定） | LEVEL 1 ONLY | 强制 | 不适用 | 不适用 |

「适用范围」列是范围的**唯一规范来源**；三个等级单元格只表达该校验项在各等级的要求，不得单独用以推断范围。两者不得各自演化。

4. **source_authenticity 边界不变**：内容完整性不等于来源真实性；声称 VERIFIED 必须附 `authenticity.verification_record`，否则 BLOCKED。
5. Level 1 的 `sidecar_anchor` 与 v3 锚点协议一致：锚点为 `sha256:<64 hex>`，等于 subject tree 中 sidecar 字节的 SHA-256，且最近触碰该 sidecar 的 commit message MUST 携带该摘要。
6. **治理确认记录同样按 v3 校验**：`classification_record` 与 `downgrade_confirmation_record` MUST 存在于 subject tree，且工作树字节与 subject blob 一致。填写不存在的路径即 BLOCKED（`CE_CLASS_RECORD_NOT_IN_SUBJECT` / `CE_DOWNGRADE_RECORD_NOT_IN_SUBJECT`）；记录不是可任意填写的字符串。
7. **仓库身份**：声明 MUST 包含 `repository`（owner/name），且与克隆的 `origin` 远程一致；远程缺失或不在允许格式内（`CE_REPO_IDENTITY_UNVERIFIED`）、声明与远程不符（`CE_REPO_IDENTITY_MISMATCH`）均 BLOCKED。允许的 origin 格式仅有三种（用户名必须为 `git`，主机精确为 `github.com`，路径恰为 `owner/repo` 且可选 `.git` 后缀，不接受端口、query、fragment）：

   | 格式 | 示例 |
   |---|---|
   | HTTPS | `https://github.com/owner/repo[.git]` |
   | SSH URL | `ssh://git@github.com/owner/repo[.git]` |
   | SCP | `git@github.com:owner/repo[.git]` |

   `http://`、`git://`、非 `git` 用户名、带端口的 URL 一律拒绝。这界定了"证据在哪个仓库被验证"的信任边界，但不证明来源真实性。

8. **路径解析基准**：所有证据路径（含 `evidence.review_note` 与 `declaration_path`）按 subject 提交的**仓库根**解析，**不按声明文件所在目录**解析；`evidence.review_note` 须指向 subject tree 内真实存在的确认记录，填写自由文本或包内相对名即 `CE_EVIDENCE_NOT_IN_SUBJECT`。本条**不新增校验层级**，只统一第 3 条与第 6 条的路径解析语义——校验范围与适用对象仍分别由那两条决定。

## 6. 检查器

检查器：`scripts/governance/evidence/check-evidence-tiering.py`（stdlib，无第三方依赖）。

必须逐项判定的 BLOCKED 场景（缺一不可）：

| # | 场景 | 原因码 |
|---|---|---|
| 1 | 缺失证据级别声明 | `CE_NO_LEVEL` / `CE_BAD_LEVEL` |
| 2 | Level 与风险类别冲突 | `CE_LEVEL_CLASS_CONFLICT` / `CE_R3_DOWNGRADE` / `CE_R2_AUTO_DOWNGRADE` |
| 3 | Level 1 任一必填字段缺失 | `CE_L1_MISSING_FIELD`（Level 2/3 对应 `CE_L2_MISSING_FIELD` / `CE_L3_MISSING_FIELD`） |
| 4 | UNKNOWN 被赋级 | `CE_UNKNOWN_CLASS` |
| 5 | v3 绑定校验失败 | `CE_NO_BINDING_PROTOCOL` / `CE_BAD_BINDING_PROTOCOL` / `CE_EVIDENCE_NOT_IN_SUBJECT` / `CE_EVIDENCE_MISSING_WORKTREE` / `CE_BLOB_MISMATCH` / `CE_NO_SIDECAR_PATH` / `CE_NO_SIDECAR_ANCHOR` / `CE_BAD_SIDECAR_ANCHOR` / `CE_SIDECAR_MISSING` / `CE_SIDECAR_MISMATCH` / `CE_SIDECAR_UNANCHORED` |
| 6 | SHA 格式或长度错误 | `CE_BAD_SHA` / `CE_BAD_SUBJECT` / `CE_BAD_BASE_HEAD` / `CE_BASE_NOT_ANCESTOR` |
| 7 | NOT_VERIFIED 被静默放行 / VERIFIED 无据 | `CE_AUTH_NOT_ACK` / `CE_UNFOUNDED_VERIFIED` / `CE_NO_AUTHENTICITY` |
| 8 | 输入不可解析、无仓库或内部异常 | `CE_UNPARSABLE` / `CE_NO_REPO` / `CE_INTERNAL_ERROR` / `CE_INPUT_MISSING` |
| 附 | 分类与降级信任边界 | `CE_NO_CLASSIFICATION_BASIS` / `CE_CLASS_UNCONFIRMED` / `CE_CLASS_SELF_CONFIRMED` / `CE_NO_CLASSIFICATION_RECORD` / `CE_CLASS_RECORD_NOT_IN_SUBJECT` / `CE_CLASS_RECORD_MISSING_WORKTREE` / `CE_CLASS_RECORD_BLOB_MISMATCH` / `CE_R2_DOWNGRADE_UNCONFIRMED` / `CE_R2_DOWNGRADE_SELF_CONFIRMED` / `CE_R2_DOWNGRADE_NO_RECORD` / `CE_DOWNGRADE_RECORD_NOT_IN_SUBJECT` / `CE_DOWNGRADE_RECORD_MISSING_WORKTREE` / `CE_DOWNGRADE_RECORD_BLOB_MISMATCH` |
| 附 | 仓库身份 | `CE_NO_REPOSITORY` / `CE_REPO_IDENTITY_UNVERIFIED` / `CE_REPO_IDENTITY_MISMATCH` |
| 附 | 审计字段缺失 | `CE_NO_AUDIT_FIELD` / `CE_NO_REVIEW_LEVEL` / `CE_BAD_REVIEW_LEVEL` |

检查器运行 MUST 具备可用的 Git 仓库（自动从声明文件所在目录向上发现，或由 `--repo` 指定）；无仓库即 `CE_NO_REPO` → BLOCKED，不得以"无法验证"为由放行。

检查器输出 `VERDICT`、`LEVEL`、`REASON`、`SUMMARY` 记录。**仅凭退出码不得作为验收证据**：验收方 MUST 核对上述逐项记录的实际判定。

退出码：0 = PASS；1 = BLOCKED（声明缺陷）；2 = BLOCKED（输入/用法错误，仍 fail-closed）。

## 7. 双语义务

本策略属 Tier 1 文档（架构/治理政策），中英文必须同一变更集更新，语义一致、义务强度一致、双向链接齐全。缺少对应版本即 NOT DONE。

## 8. 变更与生效

1. Level 定义、必填字段集合或不可降级规则的任何变更，须经正式变更记录（理由、影响文件、提议者、批准者、生效版本）。
2. 本策略在治理权威正式采纳前为 PROPOSED；工程实施通过独立审查与合并，不构成政策采纳。
3. 采纳记录须明确批准者、生效日期、适用的检查器版本及其 commit SHA。
4. 采纳记录的空白表格见 `14-ai-development/work-items/ADOPTION-EVIDENCE-2026-P1/adoption-record-template.md`；已就绪证据与仍缺失证据的汇编见同目录 `adoption-evidence-dossier.md`。两份均为准备材料：不构成采纳，不得被引用为已采纳，也不得被引用为批准者已存在。
