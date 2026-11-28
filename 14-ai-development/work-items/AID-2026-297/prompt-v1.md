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
        - "14-ai-development/work-items/AID-2026-297/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Implementation instructions for AID-2026-297 required-context execution auditing."
    canonical_scope_id: "ai-development/aid-2026-326-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-297"
      - "prompt"
      - "execution-audit"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# MIGRATION-POLICY 子代理 · 第 1 次投递：产出三个文件的正文

你此前给出的 p74 裁决（reply-6b07c97e-082656.md）与 p72 §2/§3（reply-6b07c97e-080615.md）是唯一权威。本轮只做一件事：把 p74 固化成可落盘的三个文件正文。不要重新设计、不要改口径、不要给替代方案。

## 已核实事实（来自 git 对象库，直接采用，不要再推断）

- 仓库 `oahcom/AiMemoryBrainArchitecture`，固定源树 `efbdebfa`（完整 `efbdebfaa9fede98c9f2501e2fb941f344d0ca03`）。
- `14-ai-development/work-items/<ID>/manifest.yaml` 深度 3 共 **140** 个：139 个 `AID-YYYY-NNN` + 1 个 `FIX-2026-P1-T1`。
- 同目录另有 10 个 `authorization-manifest.yaml`（`ADOPTION-EVIDENCE-2026-P1`、`FIX-2026-P1-GATE-ROOTS-001`、`FIX-2026-P1-INDEX-REFRESH-001`、`FIX-2026-P1-MANIFEST-YAML-001`、`FIX-2026-P1-T3`、`FIX-2026-P1-T4`、`FIX-2026-P1-T4-FU1`、`FIX-2026-P1-T4-FU2`、`FIX-2026-P1-T4-FU3`、`P2-T2-MEMORY-SCHEMA`），**不是**工作项 manifest，不纳入 inventory。
- 证据底表 `cells.csv` 2749 行，列固定为 `aid,field,source,raw,parsed,verdict`；`field` 实测取值 `{class, owner, prompt_bytes, prompt_id, prompt_path, prompt_sha256, prompt_status, prompt_version, provenance_note, risk, status, title}`；`verdict` 取值 `{AGREE, CONFLICT, MISSING, SINGLE_SOURCE, YAML_TRUNCATED}`；`source` 前缀 `{manifest, index, NOT_RECORDED}`。
- `conflicts.json`：117 个工作项 / 450 个单元格。
- 顶层标量截断实测 14 处（对 `efbdebfa` 跑只读扫描：AID-2026-002:12/45/46/49、003:12/56/60、014:16、030:10、059:2、064:2、092:6、106:3、174:2）；p74 的 37 处含嵌套与其余形态，口径以 p74 为准。
- `14-ai-development/work-items/INDEX.md` blob = `8ae0046746f21c28754d70fcacf92ded163c3d1d`。
- 目标 registry 的 12 个字段：`work_item_id, title, owner, class, risk, status, prompt_id, prompt_sha256, prompt_status, implementation, review, acceptance`。

## 你要产出的三件正文

### 1) `00-governance/registry-migration/policy.md`

把 p74 §1 的 12 字段规则固化为**可机械执行**的政策。每个字段必须包含：

- 权威来源（精确到 YAML 路径，例如 `authority.accountable_owner`）
- 次选来源（有序列表，逐级降级）
- `UNCONFIRMED` 触发条件（可机械判定，写成布尔条件）
- `KNOWN` 条件（可机械判定）
- 其余状态（`UNKNOWN` / `UNDECIDED` / `KNOWN_EMPTY` / `NOT_APPLICABLE`）的判定与禁止事项

另必须包含以下独立小节：

- **YAML scalar 边界（37 处截断）**：双引号/单引号/block scalar（`|`、`>`）/plain scalar 四类的边界判定算法；非法或边界不明 → `UNCONFIRMED`；禁止把 ` #` 之后当值拼接；必须从 git blob 原始字节解析，禁止用当前工作区文本。
- **摘要完全分离**：`prompt_sha256`（登记提示词文件摘要）与 `session_evidence.executed_prompt_sha256`（某次执行实际使用的提示词摘要）不得互为候选、次选或回填；即使字节相同也保持字段语义独立；36 项登记 prompt 缺失不得用 executed 摘要填补。
- **FIX 命名空间**：身份正则 `^(?:AID-[0-9]{4}-[0-9]{3}|FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*)$`；`record_kind: FIX`；不进 AID INDEX 的行数/唯一性/集合统计；每个字段独立判定，不得整条标 `UNDECIDED`。
- **裁决权**：只有有权主体能通过 adjudication 文件把 `UNCONFIRMED` 改为 `KNOWN`，必须同时给出 `decided_by` 与 `decided_at`；迁移程序不得自行升级。
- **fail-closed**：无路径/blob digest 无法校验时不得输出 `KNOWN`；解析失败不得降级为 `UNKNOWN` 冒充“无证据”。
- **与 `schema.json`、`inventory.yaml` 的关系**：三者职责边界与冲突时的失败行为。

### 2) `00-governance/registry-adjudications/schema.json`

按 p74 §4 的结构，JSON Schema **Draft 2020-12**：

- 根对象必填 `work_item_id`、`source_tree`、`decisions`；`additionalProperties: false`。
- `work_item_id` 用上面的扩展正则。
- `decisions` 是对象，键为 12 个字段名；每个字段对象必填 `state`、`candidates`、`decision`、`rationale`、`decided_by`、`decided_at`。
- **未裁决时后四项必须是 `null`，不得省略**（`required` 列出，类型含 `null`）。
- `candidates` 数组项必填 `source`、`value`、`source_blob_sha256`，可含 `path`、`line`。
- `state` 枚举与 policy 一致（`KNOWN`/`KNOWN_EMPTY`/`UNKNOWN`/`UNDECIDED`/`UNCONFIRMED`/`NOT_APPLICABLE`）。
- `source_tree` 为 7–40 位十六进制字符串。

### 3) `00-governance/registry-migration/inventory.yaml` 的**生成规则**

不要给 140 条具体名单（我按你的规则从 `origin/main` 实际生成）。给出：

- 文件顶层字段（`inventory_version`、`source_tree`、`source_prefix`、`entries` 等）
- 发现算法：`git ls-tree -r` 深度、路径正则、ID 正则、排除 `authorization-manifest.yaml`
- `record_kind` 判定（`AID` / `FIX`）
- `migration_state` 默认值与允许值
- `registry_path` 的取值规则（`NOT_MIGRATED` 时为 `null`）
- 排序规则
- 唯一性断言与覆盖断言（140 = 139 AID + 1 FIX；每个 ID 恰好一次）
- 与 registry 集合的关系断言（p72 §2.1 的集合公式）

用精确文字规则 + 可执行伪代码，不要名单。

## 输出格式（硬要求）

- 只输出三个文件正文，不要前言、不要总结、不要额外建议。
- 每个文件用下列标记逐字包裹，标记行必须单独成行：

```
<<<FILE: 00-governance/registry-migration/policy.md>>>
（正文）
<<<END FILE>>>
```

```
<<<FILE: 00-governance/registry-adjudications/schema.json>>>
（正文）
<<<END FILE>>>
```

```
<<<FILE: 00-governance/registry-migration/inventory.rules.md>>>
（inventory 生成规则正文）
<<<END FILE>>>
```

- 本轮**不要**给 `migrate_work_item_registry.py` 脚本，第 2 次投递再给。
- 目标环境：Windows PowerShell 5.1、Python 3.12、仅标准库 + PyYAML。
