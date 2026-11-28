---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      approved_version: null
      approval_date: null
      approval_scope: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      verification_reference: null
    usage_status: Active
    modification_status: Unchanged
    supersession: null
    archival: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart: "policy.md"
---
```

# 工作项注册表迁移政策

**版本：** 1.1  
**政策基线：** p72 §2 和 §3；p74 注册表裁定  
**本次迁移运行的源树：** `efbdebfa`  
**范围：** 140 份工作项清单：139 条 AID 记录和 1 条 FIX 记录

## 1. 不可妥协的迁移规则

1. 旧版清单只能从指定源树中的 Git blob 读取。
2. 任何迁移操作都不得修改、规范化、重写或重新序列化旧版清单。
3. 解析得到的 YAML 值只是候选值，不会自动成为权威值。
4. 每个注册表字段都必须获得明确状态。不得将缺失证据转换为 `NOT_APPLICABLE`，也不得将冲突证据转换为 `UNKNOWN`。
5. 如果字段的源证据存在歧义、格式错误、无法读取或无法验证，则该字段为 `UNCONFIRMED`，而不是 `UNKNOWN`。
6. `session_evidence.*.executed_prompt_sha256` 以及所有其他已执行提示词摘要，都与已登记的 `prompt_sha256` 相互独立。它们绝不能作为 `prompt_sha256` 的候选值。
7. 迁移清单是覆盖情况登记表，不是字段值来源。
8. 迁移脚本的 dry-run 模式是只读的，不得向输出目录写入内容。

## 2. 工作项身份

### 2.1 支持的身份声明

身份提取严格支持以下三种声明形式：

| 形式 | YAML 路径 | 采纳规则 |
|---|---|---|
| 主声明 | `work_item_id` | 接受与 AID 或 FIX 标识符语法匹配的非空字符串 |
| 旧版顶层声明 | `aid` | 接受与 AID 或 FIX 标识符语法匹配的非空字符串 |
| 旧版嵌套声明 | `work_item.proposed_id` | 仅当 `work_item.identifier_status` 存在且等于 `coordinator_verified_unique_see_identifier_evidence` 时接受 |

其他任何身份字段或别名都不能作为身份来源。

如果多个受支持声明均有值：

- 如果所有值相同且均有效，则身份为 `KNOWN`；保留每一项声明作为候选值。
- 如果值不同，则身份为 `UNCONFIRMED`。
- 如果任何已填写的声明格式错误，则身份为 `UNCONFIRMED`。
- 如果没有任何受支持声明有值，则仅当清单已成功读取和解析时，身份才为 `UNKNOWN`。如果清单无法读取或解析，则身份为 `UNCONFIRMED`。

没有上述精确 `identifier_status` 值的 `work_item.proposed_id` 不是可采纳的身份声明。必须将其作为候选值保留，并记录拒绝原因；不得在没有说明的情况下将其提升为正式身份。

### 2.2 标识符语法

```regex
^(?:AID-[0-9]{4}-[0-9]{3}|FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*)$
```

清单目录名称仅用于与解析出的内容身份进行一致性检查，绝不是身份来源。

目录与内容不匹配时，状态为 `UNCONFIRMED`。两个清单路径解析出相同 ID 时，构成重复身份冲突；必须独立于目录不匹配问题报告。

### 2.3 记录范围

规范清单集合是直接位于以下路径中的工作项清单：

```text
14-ai-development/work-items/<AID-or-FIX-directory>/manifest.yaml
```

不得通过搜索任意 YAML 文件中的 `work_item_id` 来发现工作项。不得将 `authorization-manifest.yaml` 视为工作项清单。

## 3. 注册表字段状态

每个注册表字段必须且只能具有以下一种状态：

- `KNOWN`：存在一个权威且经过验证的值。
- `KNOWN_EMPTY`：证据证明该字段已被明确判定为空。
- `UNKNOWN`：未发现候选值或声明，并且相关来源已完整读取。
- `UNDECIDED`：已知该字段需要作出决定，但授权决策者尚未作出决定。
- `UNCONFIRMED`：存在候选证据，但证据存在冲突、格式错误、歧义、截断或无法验证。
- `NOT_APPLICABLE`：明确的适用性决定确认该字段不适用。

迁移脚本不得根据 YAML 键缺失推断 `KNOWN_EMPTY`、`UNDECIDED` 或 `NOT_APPLICABLE`。

## 4. 字段权威性与候选值规则

本次迁移的 12 个字段为：

```text
work_item_id
title
owner
class
risk
status
prompt_id
prompt_sha256
prompt_status
implementation
review
acceptance
```

### 4.1 `work_item_id`

使用 §2.1 中规定的身份声明。

有效、唯一且一致的身份为 `KNOWN`。别名冲突、声明格式错误、YAML 无法读取、身份重复或目录与内容不匹配，均为 `UNCONFIRMED`。

### 4.2 `title`

权威来源：从清单中解析得到的 YAML 顶层 `title` 标量值。

- 完整且不存在歧义的标量为 `KNOWN`。
- 成功解析的清单中缺少 title 时，为 `UNKNOWN`。
- 非标量、格式错误或存在歧义的 title 为 `UNCONFIRMED`。
- INDEX 中的 title 不具有权威性，不能覆盖清单中的值。
- 不得将未加引号的 ` #` 之后的文本追加到 YAML 普通标量中。按照 YAML 语法，当该序列作为注释分隔符出现时，它表示注释的开始。解析器确定的标量边界并不授权从注释中重建文本。
- 受歧义或无法恢复的截断影响的 title，必须保持 `UNCONFIRMED`，直到有独立可验证的源证据解决该问题。

迁移报告必须在可获得时保留源路径、行号、Git blob SHA、原始标量证据以及解析器生成的值。

### 4.3 `owner`

按以下优先级识别可确认责任归属的字段位置：

1. `authority.accountable_owner`
2. `governance.accountable_owner`
3. 顶层 `accountable_owner`
4. 顶层 `owner`

`attribution` 不是责任归属字段，绝不能作为 owner 的回退来源。

规则：

- 如果所有已填写的责任归属位置一致，则采用优先级最高的已填写位置，并保留所有一致的候选值。
- 如果已填写的责任归属位置之间存在冲突，则 `owner` 为 `UNCONFIRMED`。
- 如果只有较低优先级的位置有值，则可以将其判定为 `KNOWN`，但必须记录精确的源路径。
- 如果只有 `attribution` 有值，则 `owner` 为 `UNKNOWN`。
- 如果完整解析的清单中不存在任何已识别的责任归属位置，则 `owner` 为 `UNKNOWN`。
- 候选值格式错误或无法读取时，为 `UNCONFIRMED`。

### 4.4 `class`

权威来源：清单顶层的 `class`。

class 值必须是符合以下表达式的非空字符串：

```regex
^[A-Z][A-Z0-9_-]*(?:/[A-Z][A-Z0-9_-]*)*(?:[ ]*\+[ ]*[A-Z][A-Z0-9_-]*(?:/[A-Z][A-Z0-9_-]*)*)*$
```

该语法允许已经观察到的复合形式，例如 `GATE/TEST`、`DOC/GOVERNANCE`、`GATE/TEST + DOC/GOVERNANCE` 和 `ARCH + DOC`。

以下值不能作为有效且已确认的 class 值：

- `NOT_ASSIGNED`
- 自由文本或临时裁定说明
- 包含作为 class 组成部分的 risk 标记的值，包括 `ARCH/R1`、`ARCH/R2` 和 `ARCH/R3`

特别是，`ARCH/R3` 属于 `UNCONFIRMED`；不得在没有说明的情况下将其改写为 `ARCH`，或将 `R3` 移入 `risk`。拆分或更正混合值必须另行取得授权裁定。

成功解析的清单中缺少 class 时，为 `UNKNOWN`。格式错误或存在歧义的值为 `UNCONFIRMED`。

### 4.5 `risk`

权威来源：清单顶层的 `risk`。

允许值：

```text
R1
R2
R3
NOT_ASSIGNED
NOT_ADJUDICATED
```

不在此精确集合中的值为 `UNCONFIRMED`；不得根据 class、title 或自由文本推断 risk。

成功解析的清单中缺少 risk 时，为 `UNKNOWN`。

### 4.6 `status`

权威来源：清单顶层的 `status`。

允许值：

```text
DISPATCHED
MERGED
REGISTERED
PROPOSED
IMPLEMENTED
VERIFIED
IMPLEMENTED_ACCEPTANCE_PENDING
REMEDIATION_IN_PROGRESS
CLOSED
ADOPTED
COMPLETE
PENDING_FORMAL_REGISTRATION
DRAFT
IMPLEMENTATION_IN_PROGRESS
IN_PROGRESS
```

匹配必须精确且区分大小写。

附加解释或自由文本尾部的值不是有效状态。例如：

```text
IN_PROGRESS — remediation after unauthorized integration of original PR
```

属于 `UNCONFIRMED`，而不是 `IN_PROGRESS`。

不得删除自由文本、将一种状态映射为另一种状态，或根据 GitHub PR 状态推断 status。

成功解析的清单中缺少 status 时，为 `UNKNOWN`。

### 4.7 `prompt_id`

已登记提示词 ID 的候选来源为：

- 顶层 `prompt_id`
- 嵌套 `prompt.id`

如果两者均有值且相等，该值可以为 `KNOWN`。如果两者不一致，则该字段为 `UNCONFIRMED`。

该值必须是符合以下表达式的非空字符串：

```regex
^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$
```

不得根据 session ID、PR 编号、工作项 ID 或自由文本来源说明推导 prompt ID。

### 4.8 `prompt_sha256`

已登记提示词摘要的候选来源仅限于：

- 顶层 `prompt_sha256`
- 嵌套 `prompt.sha256`
- 嵌套 `prompt.prompt_sha256`

候选值必须是由 64 个小写或大写十六进制字符组成的 SHA-256 摘要：

```regex
^[0-9A-Fa-f]{64}$
```

只有在以下所有条件均成立时，摘要才能成为 `KNOWN`：

1. 已通过受支持的已登记提示词路径字段明确声明已登记提示词路径。
2. 已通过受支持的已登记提示词提交字段明确声明已登记提示词提交。
3. 可以从该提交读取被引用的 Git blob。
4. 精确 blob 字节的 SHA-256 与已登记摘要相等。
5. 所有已填写的已登记摘要候选值一致。

如果任何一个条件不满足，则使用 `UNCONFIRMED`。

以下内容绝不能作为该字段的候选值：

- `session_evidence.executed_prompt_sha256`
- `prompt.executed_prompt_sha256`
- 任何其他嵌套层级中的 `executed_prompt_sha256` 键
- 任何被描述为已执行、已提交或会话提示词摘要的摘要

这些值描述的是执行证据，而不是已登记的提示词固定摘要。

### 4.9 `prompt_status`

已登记提示词状态的候选来源为：

- 顶层 `prompt_status`
- 嵌套 `prompt.prompt_status`

允许值：

```text
PINNED
NOT_PRESENT
```

只有精确匹配才接受为 `KNOWN`。任何其他已填写的值均为 `UNCONFIRMED`；成功解析的清单中缺少该值时为 `UNKNOWN`。

`PINNED` 状态本身不能证明固定摘要有效。§4.8 中的 `prompt_sha256` 验证必须独立成功。

### 4.10 `implementation`、`review` 和 `acceptance`

权威来源：独立维护的 registry-notes 记录：

```text
00-governance/registry-notes/AID-YYYY-NNN.yaml
00-governance/registry-notes/FIX-YYYY-....yaml
```

旧版 INDEX 自由文本不具有权威性，不能自动提升为正式记录。

- 可追溯且符合 schema 的 notes 声明可以为 `KNOWN`。
- 明确证明某字段被有意留空的证据可以为 `KNOWN_EMPTY`。
- 在完整扫描的 notes 集合中没有声明时，为 `UNKNOWN`。
- notes 声明存在冲突、格式错误，或候选文本无法追溯时，为 `UNCONFIRMED`。
- `UNDECIDED` 和 `NOT_APPLICABLE` 需要明确的授权声明。

初始迁移运行无权根据 PR 状态、提交消息、会话元数据或 INDEX 自由文本编造 implementation、review 或 acceptance 事实。

## 5. YAML 截断与原始证据

具有决定作用的证据是原始 Git blob，而不是重建得到的解析器值。

对于每个受影响的标量：

1. 保留源提交、Git blob SHA、源路径、行号和原始字节。
2. 根据 YAML 语法记录标量边界：
   - 带引号的标量在匹配的结束引号处结束；
   - 块标量按照 YAML 缩进和截断处理规则结束；
   - 普通标量按照 YAML token 和注释规则结束。
3. 单独记录解析器生成的值。
4. 不得将注释尾部追加到普通标量。
5. 不得使用行长度、下一键名启发式规则或假定的预期 title 作为权威依据。
6. 如果无法明确确定原始标量边界或预期值，则将字段标记为 `UNCONFIRMED`。

已知的 14 个顶层普通标量 ` #` 案例为：

```text
AID-2026-002:12
AID-2026-002:45
AID-2026-002:46
AID-2026-002:49
AID-2026-003:12
AID-2026-003:56
AID-2026-003:60
AID-2026-014:16
AID-2026-030:10
AID-2026-059:2
AID-2026-064:2
AID-2026-092:6
AID-2026-106:3
AID-2026-174:2
```

范围更广的 37 个案例截断清单还包括嵌套及其他标量形式。迁移必须检查所有清单标量位置，而不仅仅是上述 14 个顶层案例。

## 6. 迁移清单语义

清单记录身份覆盖情况和迁移状态，不是字段值来源。

允许的状态及其精确定义：

- `NOT_MIGRATED`：已在源树中发现；尚未创建注册表记录。
- `MIGRATED`：注册表记录已存在并通过 schema 验证。
- `MIGRATED_WITH_UNCONFIRMED_FIELDS`：注册表记录已存在；一个或多个字段被明确标记为 `UNCONFIRMED`。
- `EXCLUDED_BY_AUTHORITY`：授权来源引用及理由明确排除了该项目。

清单必须恰好覆盖每一个可解析身份。无法读取的清单或无法恢复的身份属于 `INCOMPLETE` 情况，而不是不存在的工作项。

迁移脚本必须针对选定的源树验证清单身份覆盖情况。不得将清单中的字段值或迁移标签视为字段权威来源。

## 7. Dry-run 输出契约

对于每个清单项目及其 12 个字段，输出：

```json
{
  "state": "KNOWN",
  "authority": "14-ai-development/work-items/AID-2026-001/manifest.yaml",
  "candidates": [
    {
      "source": "manifest.title",
      "path": "14-ai-development/work-items/AID-2026-001/manifest.yaml",
      "line": 2,
      "blob_sha256": "…",
      "value": "…"
    }
  ],
  "reason": "single valid candidate from the authoritative manifest field"
}
```

`authority` 是源路径或 `null`。候选项中的 `blob_sha256` 是源 Git blob 字节的 SHA-256，而不是解析后值的 SHA-256。

Dry-run 不得向仓库或输出目录写入注册表文件、报告、缓存或临时产物。

## 8. 阶段边界

- 阶段 A：schema 和 fixtures。
- 阶段 B：注册表验证器与清单一致性检查。
- 阶段 C：清单创建与渐进式注册表迁移。
- 阶段 D：INDEX 投影与 notes 完整性。

阶段 C 的迁移脚本不生成或修改 INDEX。INDEX 投影由以下脚本负责：

```text
scripts/ci/generate_work_item_index.py
scripts/ci/check_work_item_index.py
