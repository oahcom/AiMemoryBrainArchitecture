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
| **Level 1（严格）** | ARCHITECTURE、SECURITY、PERFORMANCE_CRITICAL、PUBLIC_API、DATA_MIGRATION、DOC_NORMATIVE；以及所有 R3 变更 | subject_head（40 位 commit SHA）、change_summary、design_doc、impact_analysis、test_log、review_record、rollback_plan、binding.protocol=v3、binding.subject_tree_contains_evidence、binding.sidecar_anchor、source_authenticity（NOT_VERIFIED 时须 authenticity.acknowledged=true） |
| **Level 2（标准）** | FEATURE、BUGFIX（有界范围、不改变契约） | subject_head、change_summary、test_log、review_record、binding.protocol=v3、binding.subject_tree_contains_evidence、source_authenticity |
| **Level 3（轻量）** | DOC_EDITORIAL（不改变规范语义的编辑性文档）、OPS（非发布关键） | subject_head、change_summary、evidence.review_note |

所有级别均 MUST 保留 40 位完整 subject_head 与变更简述；无例外。

## 3. 不可降级规则

1. **Level 1 强制底线**：凡属 R3、安全边界、授权、数据完整性、删除/遗忘、迁移、公开 API、架构语义或规范语义变更，MUST 为 Level 1。任何将其降为 Level 2/3 的判定无效。
2. **R2 不得自动降级**：R2 变更不得仅因改动规模小、文件数少或"看起来是文字修改"而降到 Level 3。确有必要时须提供 `downgrade_justification` 并由审查者确认；无该字段即 BLOCKED。
3. **文档变更不等于低风险**：文档变更若改变规范含义、约束强度、接口/协议、数据模型、状态机或安全边界，MUST 升级为 DOC_NORMATIVE → Level 1。
4. **UNKNOWN 一律 BLOCKED**：无法确定分类时不得赋予任何 Level，判定为 BLOCKED / NEEDS_CLASSIFICATION，由有权 Owner 或治理授权者确认后重新判定。
5. **不存在"自动通过"**：Level 只决定证据深度，不构成任何门禁的通过证据。

## 4. 判定与审计留痕

每条证据声明 MUST 记录以下审计字段，供独立审计复核：

| 字段 | 含义 |
|---|---|
| `change_class` | 风险类别（枚举，见 §2） |
| `review_level` | 审查级别 R0–R3 |
| `evidence_level` | 1/2/3 |
| `assessed_by` | 判定人（Owner/会话标识） |
| `assessed_at` | 判定时间（含时区） |
| `rationale` | 判定理由（为何该 Level 足够） |
| `base_head` | 判定所依据的基线 commit |
| `downgrade_justification` | 仅 R2→Level 3 时必填 |
| `escalation_target` | 升级对象（分类不确定或需 Owner 决策时） |

缺少 `assessed_by` / `assessed_at` / `rationale` 的判定不得作为 Level 依据。

## 5. 与既有证据基础设施的关系

1. **不替换、不削弱** 既有 applied-delivery-evidence validator 及其 CI workflow（本策略不修改 `.github/workflows`）。
2. **保留证据绑定协议 v3**：subject_head 必须是 commit 对象、证据文件必须位于 subject tree、工作树字节与 subject blob 一致、sidecar SHA 锚点继续有效。
3. **source_authenticity 边界不变**：内容完整性不等于来源真实性；声称 VERIFIED 必须附 `authenticity.verification_record`，否则 BLOCKED。
4. Level 1 的 `sidecar_anchor` 与 v3 锚点协议一致（最近触碰 sidecar 的 commit message 携带 sidecar 字节的 SHA-256）。

## 6. 检查器

检查器：`scripts/governance/evidence/check-evidence-tiering.py`（stdlib，无第三方依赖）。

必须逐项判定的 BLOCKED 场景（缺一不可）：

| # | 场景 | 原因码 |
|---|---|---|
| 1 | 缺失证据级别声明 | `CE_NO_LEVEL` |
| 2 | Level 与风险类别冲突 | `CE_LEVEL_CLASS_CONFLICT` / `CE_R3_DOWNGRADE` |
| 3 | Level 1 任一必填字段缺失 | `CE_L1_MISSING_FIELD` |
| 4 | UNKNOWN 被赋级 | `CE_UNKNOWN_CLASS` |
| 5 | v3 绑定字段缺失 | `CE_NO_BINDING_PROTOCOL` / `CE_NO_BINDING_TREE` / `CE_NO_SIDECAR_ANCHOR` |
| 6 | SHA 格式或长度错误 | `CE_BAD_SHA` / `CE_BAD_SUBJECT` |
| 7 | NOT_VERIFIED 被静默放行 / VERIFIED 无据 | `CE_AUTH_NOT_ACK` / `CE_UNFOUNDED_VERIFIED` |
| 8 | 输入不可解析或异常 | `CE_UNPARSABLE` / `CE_INTERNAL_ERROR` |

检查器输出 `VERDICT`、`LEVEL`、`REASON`、`SUMMARY` 记录。**仅凭退出码不得作为验收证据**：验收方 MUST 核对上述逐项记录的实际判定。

退出码：0 = PASS；1 = BLOCKED（声明缺陷）；2 = BLOCKED（输入/用法错误，仍 fail-closed）。

## 7. 双语义务

本策略属 Tier 1 文档（架构/治理政策），中英文必须同一变更集更新，语义一致、义务强度一致、双向链接齐全。缺少对应版本即 NOT DONE。

## 8. 变更与生效

1. Level 定义、必填字段集合或不可降级规则的任何变更，须经正式变更记录（理由、影响文件、提议者、批准者、生效版本）。
2. 本策略在治理权威正式采纳前为 PROPOSED；工程实施通过独立审查与合并，不构成政策采纳。
3. 采纳记录须明确批准者、生效日期、适用的检查器版本及其 commit SHA。
