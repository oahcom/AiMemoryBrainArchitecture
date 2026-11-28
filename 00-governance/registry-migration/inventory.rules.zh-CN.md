---
document_metadata:
  steward: "Architecture Governance"
  domain: architecture
  role: design-specification

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null

    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null

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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
---

# 工作项注册表迁移清单规则

## 1. 目的

`00-governance/registry-migration/inventory.yaml` 是迁移覆盖情况登记表。它记录发现了哪些工作项、它们的源清单、迁移状态，以及存在注册表目标文件时对应的目标路径。

它不是 title、owner、class、risk、status、提示词元数据、implementation、review 或 acceptance 的事实来源。

## 2. 必需文档结构

```yaml
inventory_version: 1
source_tree: "561e9f24"
source_prefix: "14-ai-development/work-items/"
entries:
  - work_item_id: AID-2026-001
    source_manifest: "14-ai-development/work-items/AID-2026-001/manifest.yaml"
    migration_state: NOT_MIGRATED
    registry_path: null
```

该文档必须包含：

- `inventory_version`：整数 `1`。
- `source_tree`：生成清单时固定的 Git commit 或 tree 标识符。
- `source_prefix`：必须精确为 `14-ai-development/work-items/`。
- `entries`：固定源树中发现的每一个可解析工作项身份都必须有且仅有一条对应记录。

每条记录必须包含：

- `work_item_id`
- `source_manifest`
- `migration_state`
- `registry_path`

对于 `NOT_MIGRATED`，`registry_path` 为 `null`。对于已迁移状态，该字段必须指向对应的规范注册表文件。被排除的项目必须在清单条目中保留其排除证据。

## 3. 发现与身份

规范发现集合是直接清单路径：

```text
14-ai-development/work-items/<AID-or-FIX-directory>/manifest.yaml
```

不得通过搜索任意 YAML 文件中看起来像身份字段的键来发现记录。不得包含 `authorization-manifest.yaml`。

身份提取严格支持：

1. 顶层 `work_item_id`；
2. 顶层旧版 `aid`；
3. 嵌套 `work_item.proposed_id`，但仅当同一个 `work_item` 映射包含 `identifier_status: coordinator_verified_unique_see_identifier_evidence` 时才支持。

接受的身份语法为：

```regex
^(?:AID-[0-9]{4}-[0-9]{3}|FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*)$
```

目录名称仅用于一致性检查。如果清单没有声明身份，不得利用目录名称制造身份。

如果多个受支持声明不一致、任何声明格式错误，或者清单无法读取或解析，则该项目为 `INCOMPLETE`。不得在没有说明的情况下将其省略。

## 4. 允许的迁移状态

`migration_state` 只允许以下值：

- `NOT_MIGRATED`
- `MIGRATED`
- `MIGRATED_WITH_UNCONFIRMED_FIELDS`
- `EXCLUDED_BY_AUTHORITY`

不得使用 `IN_PROGRESS`、`BLOCKED` 或任何其他值代替这些状态。

### 4.1 状态含义

| 状态 | 含义 | 必需的注册表条件 |
|---|---|---|
| `NOT_MIGRATED` | 已在源树中发现；尚未创建注册表记录 | 注册表文件不得存在；`registry_path: null` |
| `MIGRATED` | 注册表记录已创建并通过 schema 验证 | 必须恰好存在一个注册表文件，并通过 schema 验证 |
| `MIGRATED_WITH_UNCONFIRMED_FIELDS` | 注册表记录存在；一个或多个字段被明确标记为 `UNCONFIRMED` | 必须恰好存在一个注册表文件并通过 schema 验证；未解决的字段必须标记为 `UNCONFIRMED` |
| `EXCLUDED_BY_AUTHORITY` | 授权决定明确排除了该工作项 | 不要求注册表文件存在；条目必须携带授权来源引用和理由 |

## 5. 验证器状态矩阵

验证器必须应用以下矩阵：

| 清单状态 / 观察到的条件 | 验证器结果 | 必需代码或解释 |
|---|---|---|
| `NOT_MIGRATED` 且注册表文件不存在 | `PASS` | 迁移按设计尚未完成；在覆盖报告中列出 |
| `NOT_MIGRATED` 但注册表文件存在 | `VIOLATION` | `INVENTORY_REGISTRY_STATE_MISMATCH` |
| `MIGRATED` 但注册表文件不存在 | `VIOLATION` | `MIGRATED_RECORD_MISSING` |
| `MIGRATED` 且文件存在，但缺少必需字段 | `VIOLATION` | `SCHEMA_REQUIRED_FIELD_MISSING` |
| `MIGRATED_WITH_UNCONFIRMED_FIELDS` 且未解决字段被正确标记 | `PASS` | 记录在结构上已完成迁移；不确定性仍被明确保留 |
| `EXCLUDED_BY_AUTHORITY` 缺少授权证据 | `VIOLATION` | `EXCLUSION_UNAUTHORIZED` |
| 在源树中发现清单身份，但不存在对应的清单条目 | `VIOLATION` | `INVENTORY_ENTRY_MISSING` |
| 清单身份没有对应源清单，也没有授权排除 | `VIOLATION` | `INVENTORY_SOURCE_MISSING` |
| 源清单无法读取或无法解析其身份 | `INCOMPLETE` | 不得将其归类为缺失的工作项 |
| 两份源清单解析出相同身份 | `VIOLATION` | 重复身份；必须报告两个源路径 |
| 清单包含重复身份条目 | `VIOLATION` | 清单身份重复 |
| 清单源树与验证器选定的源树不匹配 | `INCOMPLETE` | 该清单不适用于此源树 |

## 6. 覆盖不变量

定义：

```python
inventory_ids = all_valid_ids_discovered_from_legacy_manifests
registry_ids = all_ids_with_registry_records
not_migrated_ids = IDs whose state is NOT_MIGRATED
migrated_ids = IDs whose state is MIGRATED
migrated_unconfirmed_ids = IDs whose state is MIGRATED_WITH_UNCONFIRMED_FIELDS
excluded_ids = IDs whose state is EXCLUDED_BY_AUTHORITY
```

验证器必须强制执行：

```python
assert registry_ids <= inventory_ids
assert registry_ids.isdisjoint(unaccounted_duplicate_ids)

assert inventory_ids == (
    migrated_ids
    | migrated_unconfirmed_ids
    | not_migrated_ids
    | excluded_ids
)
```

每个身份在清单中必须恰好出现一次。每个注册表文件必须且只能对应一个清单身份。不得因为清单或注册表文件格式错误而静默丢弃任何清单记录。

无法解析身份的源清单不属于猜测得到的 `inventory_ids` 集合；它必须作为 `INCOMPLETE` 发现项，并附带其源路径。

## 7. 固定源树与新增工作项

清单记录用于创建该清单的源树。它不是永久性的发现快照。

验证后续候选源树时：

1. 从该候选源树重新发现规范清单集合。
2. 使用 §3 中受支持的声明解析身份。
3. 要求每个新发现的身份都恰好有一条清单条目。
4. 要求每条清单条目都能解析到一份源清单，除非它具有有效的授权排除。
5. 根据 §5 中的状态矩阵验证注册表文件是否存在。

清单中缺少的新清单属于 `INVENTORY_ENTRY_MISSING`，而不是隐式的 `NOT_MIGRATED`。

## 8. 排除证据

`EXCLUDED_BY_AUTHORITY` 必须同时具备：

- 指向授权记录的源引用；以及
- 一条非空理由，说明授权主体及排除决定。

没有可验证源引用的自由文本说明并不充分。迁移工具不得自动创建此状态。

## 9. 覆盖报告与严格清单

在渐进式迁移期间，验证器至少必须报告：

- 已发现的清单数量；
- 可解析的身份数量；
- 清单条目数量；
- `NOT_MIGRATED` 数量；
- `MIGRATED` 数量；
- `MIGRATED_WITH_UNCONFIRMED_FIELDS` 数量；
- `EXCLUDED_BY_AUTHORITY` 数量；
- 重复身份数量；
- 缺失清单条目数量；
- 缺少源清单的清单条目数量；
- 无法读取或无法识别身份的源清单数量。

在渐进式迁移期间，覆盖百分比低于 100% 本身并不构成 schema 违规。

`--strict-inventory` 强制验证完整的清单/源文件/注册表关系，并在出现任何 `INCOMPLETE` 或 `VIOLATION` 情况时失败。这并不意味着所有记录都必须已经完成迁移。在达到迁移切换标准之前，正确登记的 `NOT_MIGRATED` 记录仍然允许存在。

## 10. 切换条件

只有满足以下全部条件，INDEX 才能切换为基于注册表生成的投影：

```text
migrated_count + authorized_excluded_count = discovered_count
not_migrated_count = 0
schema_failures = 0
duplicate_ids = 0
incomplete = 0
```

INDEX 的生成与验证属于阶段 D 的职责：

```text
scripts/ci/generate_work_item_index.py
scripts/ci/check_work_item_index.py
```

清单验证器不得生成 INDEX，也不得将 INDEX 内容视为字段权威来源。
