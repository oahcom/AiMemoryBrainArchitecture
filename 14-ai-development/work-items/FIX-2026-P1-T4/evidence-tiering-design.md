# FIX-2026-P1-T4 设计记录：证据链分级

- **Work Item：** FIX-2026-P1-T4
- **Owner：** G（流程架构）
- **授权：** DEC-FIX-2026-P1-T4-GO-001（2026-11-19）
- **基线：** `5f7918f90fe4defe39ccc3de242019f8d4003d86`
- **分支：** `ai/FIX-2026-P1-T4/G-evidence-tiering`
- **政策状态：** PROPOSED

## 1. 裁定链

1. **设计裁定**：Level 1/2/3 = 证据深度选择器（非状态轴）；与 R1/R2/R3 审查级别、12 状态/6 阶段三轴独立。
2. **授权形式裁定（选择 A）**：采用 P1-T3（PR #279，merge commit `5f7918f`）同构授权形式——正式 GO decision + manifest（allowed_write_paths + authorization_basis）即构成有效授权；`sponsor` / `accountable_owner` / `acceptance_authority` 显式登记 `NOT_ASSIGNED`，不得以 Owner G 替代。依据：AID-2026-008/009 亦为 `accountable_owner: NOT_ASSIGNED`。
3. **GO 裁定**：8 条写入路径全部批准；不修改 `.github/workflows`；不授予 main 合并权。

## 2. 三轴独立性

| 维度 | 取值 | 决定 | 不得替代 |
|---|---|---|---|
| 变更风险 | Level 1/2/3 | 证据深度 | 不得由审查级别/规模推定 |
| 审查级别 | R0–R3 | 独立与专业审查要求 | 不得由 Level 降低 |
| 生命周期 | 12 状态 / 6 阶段 | 门禁里程碑 | 不受 Level 影响 |

## 3. 风险类别 → 证据深度映射

| change_class | 允许 Level | 说明 |
|---|---|---|
| ARCHITECTURE | 1 | 架构决策与契约 |
| SECURITY | 1 | 安全边界/授权/遗忘删除 |
| PERFORMANCE_CRITICAL | 1 | 性能关键路径 |
| PUBLIC_API | 1 | 公开接口变更 |
| DATA_MIGRATION | 1 | 数据/模式迁移 |
| DOC_NORMATIVE | 1 | 改变规范语义的文档 |
| FEATURE | 1–2 | 有界功能实现 |
| BUGFIX | 1–2 | 一般缺陷修复 |
| DOC_EDITORIAL | 1–3 | 编辑性文档（无语义变化） |
| OPS | 1–3 | 非发布关键运维 |
| UNKNOWN | BLOCKED | 不得赋级 |

附加规则：R3 一律 Level 1；R2→Level 3 必须提供 `downgrade_justification`，否则 BLOCKED。

## 4. F 裁定落实

| 编号 | 裁定 | 落实位置 |
|---|---|---|
| F1 授权缺失（BLOCKING） | 由 DEC-FIX-2026-P1-T4-GO-001 关闭 | 本清单 + authorization-manifest |
| F2 分类边界 | 风险→深度映射表 | 政策 §2、§3；检查器 CLASS_ALLOWED_LEVELS |
| F3 安全降级 | Level 1 强制底线 | 政策 §3.1；检查器 CE_LEVEL_CLASS_CONFLICT / CE_R3_DOWNGRADE |
| F4 证据字段 | 全级 40 位 SHA + 简述 | 政策 §2；检查器 CE_NO_SUBJECT_HEAD / CE_BAD_SHA / CE_NO_SUMMARY |
| F5 审计留痕 | assessed_by/at/rationale/base_head 等 | 政策 §4 |
| F6 v3 兼容 | 保留全部绑定与真实性校验 | 政策 §5；检查器 binding.* 与 authenticity.* 判定 |
| F7 双语结构 | AI-STD-001 单文件 EN/ZH 交替，不建 docs/en 副本 | AI-STD-001 §4.2.1 |
| F8 上位依据 | 不以 AI-EXEC-002 v1.2 为依据 | 政策文首「明确不作为依据」 |

## 5. 检查器规格

输入：证据声明（扁平 YAML 子集，`evidence:` / `binding:` / `authenticity:` 三个嵌套块）。
输出：`VERDICT` / `LEVEL` / `REASON` / `SUMMARY` 记录；退出码 0/1/2。

8 项验收门槛逐项实现（原因码见政策 §6），并由 `test_evidence_tiering.py` 逐项断言 VERDICT/REASON 记录（非仅退出码），另有 3 个通过用例与 4 个附加 fail-closed 用例。

## 6. 偏离与限制（Deviations）

| 项 | 说明 |
|---|---|
| CI 接入 | 未接入 `.github/workflows`（授权范围外）。检查器当前为手动/流程调用，CI 集成需另行授权。 |
| 语义等价判断 | 检查器不判断中英文语义等价、不判断文档是否"实质改变规范语义"；`DOC_NORMATIVE` 的判定依赖人（Owner/审查者）并须留痕。脚本只校验声明结构与强制规则。 |
| 来源真实性 | 检查器不验证外部来源真实性；仅强制 VERIFIED 声明必须附 `verification_record`，否则 BLOCKED。 |
| 政策采纳 | 本次交付不构成政策采纳；状态保持 PROPOSED。 |

## 7. R1 缺陷修复映射

| R1 缺陷 | 修复 |
|---|---|
| B-01 v3 绑定未真实执行 | 仓库自动发现（无仓库即 `CE_NO_REPO`）；subject_head 强制 commit 对象校验；每条 evidence.* 路径以 `cat-file -e <subject>:<path>` 校验 subject tree 包含、以 `hash-object` 与 `rev-parse <subject>:<path>` 校验工作树/blob 一致；Level 1 额外校验 sidecar 摘要（`sha256:<64hex>` 格式、与 subject blob 实际摘要一致、最近触碰该 sidecar 的 commit message 携带摘要）；Level 3 亦执行 protocol/tree/blob 三项 |
| B-02 R2 降级可伪造 | R2→L3 须同时具备 `downgrade_justification`、`downgrade_confirmed_by`（≠ assessed_by）、`downgrade_confirmation_record`；三项各自独立原因码 |
| B-03 分类信任边界缺失 | 可降级类别（FEATURE/BUGFIX/DOC_EDITORIAL/OPS）须 `classification_basis` + 独立 `classification_confirmed_by` + subject tree 内 `classification_record`；强制 L1 类别改标即触发 `CE_LEVEL_CLASS_CONFLICT` |
| H-01 审计字段未强制 | `assessed_by`/`assessed_at`/`rationale`/`base_head` 强制；`base_head` 另校验为 subject_head 祖先 |
| H-02 测试缺 review_level 边界 | 新增缺失/非法 review_level、R2 降级三项负向测试 |
| H-03 解析器不严格 | 拒绝 tab、非 2 空格缩进、嵌套块头、重复键/块；全部 `CE_UNPARSABLE` |
| H-04 测试无真实 Git | 全部用例改为真实临时 Git 仓库 fixture（真实 commit/tree/blob/sidecar 与 commit message 锚定） |
| M-01 模板字段不全 | manifest `evidence_tiering` 增加 `review_level`、分类与降级确认字段、`declaration_path`，并写明与声明的同步要求 |
| M-02 Level 3 歧义 | 政策 §5 增加「v3 校验范围按等级」表：protocol/tree/blob 全等级强制，sidecar 仅 Level 1；中英文同步 |
