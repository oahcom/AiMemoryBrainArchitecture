---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-352/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Snapshot bytes are pinned in the adjacent manifest; provenance is recorded as NOT_VERIFIED."
    usage_status: Active
    modification_status: Active-Modified
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
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Executed prompt snapshot - AID-2026-352

# 任务：Issue #266 的 AC4 与 AC6 精确化缺口 + 产出可判定交付物（AID-2026-352）

仓库：`oahcom/AiMemoryBrainArchitecture`，实测树 `origin/main = f0843a8f3`（2026-11-28）。
工作分支：`aid-2026-352`，worktree `C:\tmp\p352`（已从 origin/main 建好，干净）。
执行者负责机械落盘/提交/PR；**字段名、必填性、回填范围、负例内容全部由你决定**，我不自行裁定。

---

## 一、Issue #266 现行判定原文（逐字，来自 `D:\code\.tmp\i266.md`）

**AC4**（第 100 行）：
> - [ ] Work Items link relevant documents. / Work Item 链接相关文档。 — **PARTIAL**。引用很普遍：多数 `manifest.yaml` 在 `scope` 等处引用了 `work-items/` 之外的 `.md` 路径（基线 `e47dd6f0`）。**但没有字段承载它**：`documentation:` / `documents:` / `document_refs:` / `docs:` / `related_documents:` / `spec_refs:` 六种可能的名字在 83 份中**全部 0 命中**。根因在过去被记为「manifest 没有 schema」。当前实测（`cb5b3dcd`）该前提已不成立：`14-ai-development/work-items/work-item-manifest.schema.yaml` 已合入（`5ef1e18a`，AID-2026-251；70 行，`schema_version: "2"`，20 个 `required_top_level_keys`），另有分类登记 `manifest-schema-registry.yaml`（`4d8655eb`）、检查器 `scripts/ci/check_work_item_manifest_schema.py`……

**AC6**（第 102 行）：
> - [ ] Superseded documents retain historical references. / 被替代文档保留历史引用。 — **PARTIAL**。机制有两套：`schema:193` 的 `lifecycle.supersession.supersedes`（+ `supersession_reason` + `effective_date`）与 `schema:200-207` 的 `lifecycle.archival.archival_reference`。实测（基线 `e47dd6f0`）：**真正被使用的 supersedes 只有 1 条**；`supersession_reason` 与 `effective_date` 各只有 **4** 处非空。**`archival_reference` 是纯空壳**：**321** 份文档声明它，**321 份全部是字面 `null`**，非空值 **0**。历史引用真正靠的是散文：**58** 份文档正文写 `superseded by`。**关键证据**：`scripts/check_document_management.py:202` 把 `archival_reference` 放进 `ARCHIVAL_KEYS` 允许键集合，但**从不读它的值**（该集合只用于拒绝拼错的键）；全仓库 `scripts/*.py` 中对 `archival_reference` 的引用只有这一处。**填了也不会被检查，所以没人填。** **承接方：** #1257。这条需要范围决定（A 承认散文为机制 / B 降低结构化成本 / C 声明该块未使用），不是补覆盖。

---

## 二、我在 `origin/main = f0843a8f3` 上的实测事实（全部可复算）

### AC4 侧
- 工作项 `manifest.yaml`：**167** 份（`git ls-tree -r origin/main` 统计，不是旧的 83）。
- 含顶层 `documentation:` 键：**132** 份；缺失：**35** 份。
- `documentation` 条目总数 **508**；其中路径在**本工作项目录之外**的条目 **236** 条；**97** 份 manifest 至少有 1 条「本工作项目录之外」的引用（另 35 份只有自引用或完全没有）。
- `documentation[*].path` 不存在于 git tree 的：**0** 条（schema 规则 `path_must_exist_in_git_tree` 生效）。
- `documentation[*].relationship` 不在枚举内的：**6** 条，全部集中在 `AID-2026-284`（值分别是 `work-item metadata and immutable prompt digest` / `proxy scope determination superseding AID-2026-260 scope carrier` / `source blob, policy, Issue and comment evidence with recomputation commands` / `session role, actual input and AI-visible output record` / `structured prompt snapshot used to derive the work-item record` / `one work-item registry row`）——这是**真实存在的 schema 违规**（枚举外自由文本）。
- 缺失 `documentation` 的 35 个：`AID-2026-100,112,113,114,115,116,140,150,170,172,173,174,183,186,188,189,190,191,192,193,197,198,199,200,204,210,211,240,241,256,261,268,279,280,281`。这些目录里通常有 `evidence.md`、`session-evidence.md`、`prompt-v1.md` 等 `.md`（我已逐个列出候选文件，需要时给）。
- 检查器现状（`python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json`，HEAD=f0843a8f3）：
  ```
  Manifest schema v2: total=167 compliant=48
  AC4 violations: 36 manifest(s)
  Other schema violations: 119 manifest(s)
  Legacy ratchet new regressions: 0
  Legacy ratchet baseline tree: 5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0
  ```
  exit 0。基线文件只有两个键：`{"baseline_tree":"5be0d93f305ca0c1790abe41b4eb23cd7c71a6a0","cohort_tree":"e47dd6f0"}`。
- 现有 schema（`14-ai-development/work-items/work-item-manifest.schema.yaml`，schema_version "2"）已定义：
  ```yaml
  fields:
    documentation:
      kind: sequence
      required: true
      min_items: 1
      item_required_keys: [path, relationship]
      path_kind: repository-relative-path
      path_must_exist_in_git_tree: true
      relationship_enum: [normative, design, implementation, evidence, reference, code, schema]
  ```
- 检查器 `validate_against_schema()` 已实现规则：`documentation.required` / `.kind.sequence` / `.min_items` / `.item.mapping` / `.item.required_key` / `.relationship.enum` / `.path.nonempty` / `.path.repository_relative` / `.path.exists_in_git_tree`，category 记为 `AC4`。
- 所以 AC4 现在的实际缺口**不再是「没有字段」**：字段有、规则有、97/132 份也填了外部引用。剩下的是**覆盖与语义**（35 份没有；`documentation` 是否要求「至少一条本工作项之外的引用」这一语义没被任何规则表达；6 条自由文本 relationship 违规挂着）。

### AC6 侧
- 用 `scripts/check_document_management.py` 的 `read_metadata()` 解析 `origin/main` 全部 `.md`：**902** 份成功解析（0 份解析失败）。
- `lifecycle.supersession.supersedes` 非空：**2** 条：
  - `14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md` → `14-ai-development/work-items/I-OWNER-DECISION-AUTHORIZATION-DECISION-001.md`
  - `14-ai-development/work-items/AID-2026-284/scope-confirmation.md` → `14-ai-development/work-items/AID-2026-260/scope-confirmation.md`
- `supersession_reason` 非空 **4**、`effective_date` 非空 **4**（与上面 2 条 supersedes 不必然对齐）。
- `lifecycle.archival.archival_reference`：声明 **769** 份，非空 **0** 份。
- 正文散文含 `superseded by`：**37** 份。
- 现有 DM-13（`scripts/check_document_management.py`，约 1603 行起）已校验：`supersedes` 必须是 list、target 必须是仓库相对路径且**文件存在**、不能自指、不能成环。
- DM-08：`lifecycle.supersession.superseded_by` 在 schema 的 `forbidden:` 里，**禁止手写**；policy §（`00-governance/architecture-document-management-policy.md` 第 249/329 行）写明 `superseded_by` 是 **CI 衍生**，只存在于生成索引中。
- 实测：全仓库 `scripts/`、`.github/` 中**没有任何代码生成 `superseded_by` 或任何 supersession 反向索引**（`git grep -ln "supersession" origin/main -- scripts .github` 只命中 `check_document_management.py` 与它的测试）。即：政策声明了一个衍生产物，但生成器不存在 → 「被替代文档保留历史引用」在结构上无处落地。
- `archival_reference` 在 `ARCHIVAL_KEYS` 里只用于拒绝拼错的键，值从不被读取（你原文已指出）。

---

## 三、需要你回答与产出（全部由你决定，我不代拟）

### 1. AC4 三问
(a) 现在能判到哪一步（哪些谓词已可判定、判定结果是什么）；
(b) 缺的**具体谓词**是什么（用可判定语言写，例如「每份 manifest 的 `documentation` 至少包含 1 条 path 不在本工作项目录下的条目」这种形式，或你判定的其它形式）；
(c) 补齐要改什么：manifest schema / 数据回填 / 检查器 / 文档，逐项说明改哪一处。

### 2. AC6 三问
同上三问。特别请裁定你原文给出的 A/B/C 三条路（承认散文为机制 / 降低结构化成本 / 声明该块未使用）选哪条，以及是否需要补生成器。

### 3. AC4 交付物（若判为需要改）
- 字段定义：直接给 `work-item-manifest.schema.yaml` 的**完整替换块**（字段名、必填/可选、min_items、是否新增「至少一条外部引用」这类谓词、relationship_enum 是否变化）。若判定沿用现有 `documentation` 字段，明确写出「不改 schema，只改 X」。
- 回填：给一个**幂等、可回滚、带 `--dry-run` 与影响文件数统计**的 Python 脚本全文（Windows、Python 3.11、PyYAML 可用；只改 `14-ai-development/work-items/*/manifest.yaml`，不碰其它文件；插入位置与 YAML 缩进必须与现有文件风格一致；重复执行结果字节一致）。回填范围（哪 35 份 / 是否连 132 份里的自引用也补外部引用 / `AID-2026-284` 那 6 条自由文本怎么处理）由你定。
- 检查器：给出**新增/修改的规则代码块**（贴在现有 `validate_against_schema()` 风格里，rule_id、category、pointer、message 都写全），以及**一条内联负例**（可直接运行的 fixture 或一段 manifest 片段 + 期望的 rule_id 与退出码），要求负例实测 exit 1。

### 4. AC6 交付物（若判为需要改）
- 规则与负例：例如「A 声明 `supersedes: B`，但 B 未记录被替代（`archival_reference` 未指向 A / 生成索引里没有反向边）→ 红」。给出规则代码块（改哪个文件、插在哪、rule id 用 DM-13 扩展还是新 DM-xx）、以及可直接跑出 exit 1 的负例。
- 若判「现有机制已足够、只是没被正确表述」：给出**可执行的检索命令与命中统计**（命令原文 + 输出），并说明为何不需要改代码。

### 5. 硬约束（我的执行边界，请你的方案落在边界内）
- 不放宽既有 schema 规则；不改 `.github/workflows`；不改基线 JSON 掩盖新失败。
- 提交后必须满足：`check_work_item_manifest_schema.py --tree HEAD --baseline ...` 的 `Legacy ratchet new regressions` 不因本次改动增加（当前是 0）；`check_document_management.py --require-changed origin/main` exit 0。
- 现有 2 条历史遗留问题：`AID-2026-016` 缺 `documentation` 与 `implementation`（在旧基线下不算回归，但在全量统计里计入）。若你的方案会触及它，请说明。

### 6. 输出格式
- 纯文本 + 围栏代码块，每个块首行注释写明目标文件路径（如 `# FILE: 14-ai-development/work-items/work-item-manifest.schema.yaml`）。
- 最后给一段「本次补了什么 / 什么仍未补」的清单，我要逐字搬进 PR 正文。
- 不要只给原则，要给可直接落盘的字节内容。
