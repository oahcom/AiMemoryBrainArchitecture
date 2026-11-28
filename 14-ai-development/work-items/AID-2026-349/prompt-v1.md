---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-349/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
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
    canonical_scope: "Repair instructions for AID-2026-349: dangling Phase 3.5 contract references in memory-runtime documents and mirrors."
    canonical_scope_id: "ai-development/aid-2026-349-prompt-v1"
    canonical_scope_keywords:
      - "AID-2026-349"
      - "prompt"
      - "dangling-reference"
      - "memory-runtime"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# 任务 DEF-refs-03：残留两处缺失规范引用修复

## 0. 角色与边界

你是 `oahcom/AiMemoryBrainArchitecture` 的修复作者。你没有仓库读写权限，**只输出逐字编辑块**，由调用方机械套用。不要写计划、不要写总结、不要输出 diff、不要解释流程，只按第 6 节的输出契约给结果。

仓库基线：`origin/main`（本任务材料全部取自 `git show origin/main:<path>`，逐字，未经改写）。所有 `OLD` 块必须能在该基线的对应文件里**恰好匹配一次**。

## 1. 缺陷

`05-memory-runtime` 的两份 Canonical 文档仍把 `phase-3.5-forget-suppression-and-cursor-consumption.md` 当作存在的规范文件来链接，但该文件**在 `main` 的工作树与可达历史中都不存在**（见 `docs/governance/documentation-gaps.md` 的 GAP-01）。

- `05-memory-runtime/retrieval-engine.md:149`
- `05-memory-runtime/working-set-and-cache.md:144`

同批的第三处 `05-memory-runtime/runtime-overview.md` 已在 PR #1492 修好，修法就是模板（见第 3 节）。

## 2. 已核实事实（与任务下发的假设不同，请以此为准）

1. **镜像里是有对应句子的**，不是"没有"。`docs/en/` 与 `docs/zh-CN/` 的四个镜像文件都带有同一句话，且**已经**把链接目标改成了 `../../governance/documentation-gaps.md`。也就是说镜像侧已经被改过，Canonical 侧落后了。
2. 但**披露措辞不齐**：`docs/en/05-memory-runtime/retrieval-engine.md:149` 带有 `(unsubmitted and not restored; see ...)`；`docs/en/05-memory-runtime/working-set-and-cache.md:144` **没有**这句披露；`docs/zh-CN` 的两个镜像**都没有**"该文件未提交、未恢复"的披露。
3. `docs/governance/documentation-gaps.md` GAP-01 的处置要求原文是：「The owning party for `05-memory-runtime` supplies the actual contract, or the six referencing passages are amended to state that the contract is not yet published.」并明确 "the references are **not** satisfiable by rewriting them to a different file"（指不能用另一份规范替代其规范内容）——注意 `runtime-overview.md` 的既有修法保留了原文件名、只把**链接**指向 `documentation-gaps.md` 并加披露，这是被接受的做法。
4. 项目规则：Canonical 改动必须同 PR 带上所有 counterpart（`docs/en/...`、`docs/zh-CN/...`），由 `scripts/check_bilingual_docs.py` 把关。该脚本证明的是"三份都在、互相指认"，不读正文（GAP-04）。所以：**Canonical 一旦改动，你必须给出让三侧语义一致的落地方案**，而不是只说"镜像不用改"。

## 3. 已修好的模板（`runtime-overview.md`，逐字，作为写法基准）

Canonical `05-memory-runtime/runtime-overview.md:149`：

```
The normative F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation contract, index rebuild contract and ten conformance specifications are historically associated with `phase-3.5-forget-suppression-and-cursor-consumption.md` (unsubmitted and not restored; see [documentation gaps](../docs/governance/documentation-gaps.md)).
```

Canonical `05-memory-runtime/runtime-overview.md:60`：

```
**Phase 3.5 dependency review:** D/E/I/G/H/C/B owner-branch contracts are present and were re-read at the exact heads historically recorded in `phase-3.5-forget-suppression-and-cursor-consumption.md` (unsubmitted and not restored; see [GAP-01](../docs/governance/documentation-gaps.md)). F's consumer semantics are DECIDED; callable cross-module schemas, Storage realization and runtime conformance remain OPEN. No wire schema is frozen by this document.
```

`docs/en/05-memory-runtime/runtime-overview.md:144`：

```
The normative F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation contract, index rebuild contract and ten conformance specifications are historically associated with `phase-3.5-forget-suppression-and-cursor-consumption.md` (unsubmitted and not restored; see [documentation gaps](../../governance/documentation-gaps.md)).
```

`docs/zh-CN/05-memory-runtime/runtime-overview.md:174`：

```
规范性 F Consumer Matrix、Retrieval-stage Suppression Matrix、Cache/Working Set Invalidation Contract、Index Rebuild Contract 和十项 Conformance Specification 维护于 [phase-3.5-forget-suppression-and-cursor-consumption.md](../../governance/documentation-gaps.md)。
```

（zh-CN 的对应写法是"维护于 [原文件名](documentation-gaps 链接)"，不含单独披露句；en 的对应写法含 `(unsubmitted and not restored; see ...)`。这是 PR #1492 实际落地的三侧形态。）

## 4. 待改文件逐字上下文

### 4.1 `05-memory-runtime/retrieval-engine.md`（Canonical，188 行）

第 147–149 行：

```
## Phase 3.5 — Typed Cursor and Forget Suppression Addendum (normative supplement)

The detailed owner/consumer contract is in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This supplement supersedes any earlier provisional wording in this file where the two differ.
```

### 4.2 `docs/en/05-memory-runtime/retrieval-engine.md`（188 行）

第 147–149 行：

```
## Phase 3.5 — Typed Cursor and Forget Suppression Addendum (normative supplement)

The detailed owner/consumer contract is in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../../governance/documentation-gaps.md). This supplement supersedes any earlier provisional wording in this file where the two differ.
```

### 4.3 `docs/zh-CN/05-memory-runtime/retrieval-engine.md`（223 行）

第 183–185 行：

```
## Phase 3.5 — 类型化 Cursor 与 Forget Suppression 补充（规范性补充）

详细 Owner/Consumer Contract 见 [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../../governance/documentation-gaps.md)。本补充在冲突时取代本文更早的临时措辞。
```

### 4.4 `05-memory-runtime/working-set-and-cache.md`（Canonical，177 行）

第 142–144 行：

```
## Phase 3.5 — Forget Fence and Permission Invalidation Addendum (normative supplement)

The detailed contract and conformance cases are in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](phase-3.5-forget-suppression-and-cursor-consumption.md). This addendum supersedes earlier provisional wording where inconsistent.
```

### 4.5 `docs/en/05-memory-runtime/working-set-and-cache.md`（177 行）

第 142–144 行：

```
## Phase 3.5 — Forget Fence and Permission Invalidation Addendum (normative supplement)

The detailed contract and conformance cases are in [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../../governance/documentation-gaps.md). This addendum supersedes earlier provisional wording where inconsistent.
```

### 4.6 `docs/zh-CN/05-memory-runtime/working-set-and-cache.md`（235 行）

第 197–199 行：

```
## Phase 3.5 — Forget Fence 与 Permission Invalidation 补充（规范性补充）

详细 Contract 和 Conformance Case 见 [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../../governance/documentation-gaps.md)。本补充在不一致时取代之前的临时措辞。
```

## 5. 你必须做出的判定（先判定，再给块）

1. **Canonical 两处怎么改**：是否采用 `runtime-overview.md` 的既有形态——保留原文件名、把链接指向 `../docs/governance/documentation-gaps.md`、并加 `(unsubmitted and not restored; see [documentation gaps](...))` 披露。注意 Canonical 位于仓库根，指向 governance 的相对路径是 `../docs/governance/documentation-gaps.md`。
2. **双语门禁怎么过**：Canonical 改动后，`docs/en/` 与 `docs/zh-CN/` 必须同 PR 对齐。可选做法（你选一个并说明）：
   - (a) 只补披露措辞，使 en 两份、zh-CN 两份与 Canonical 语义一致（en 补 `(unsubmitted and not restored; see ...)`，zh-CN 补"该文件未提交、未恢复"），**不新增任何译文以外的规范内容**；
   - (b) 判定镜像已经指向 `documentation-gaps` 且语义等价，给出 `|SKIP===` + 一行理由，并说明为何该 PR 能过 `check_bilingual_docs.py`。
   若你选 (a)，必须给全 en/zh-CN 的块；若选 (b)，必须对每个镜像文件单独给 `|SKIP===` 块。
3. 若某文件判定不改，用 `|SKIP===` 明确写出，不要漏项：**六个文件（Canonical 2 + en 2 + zh-CN 2）每个都要有一个块或一个 SKIP**。

## 6. 输出契约（固定，不得变更）

每个文件一段，顺序任意，格式严格如下：

```
===FILE: <仓库根相对路径>|REPLACE===
---OLD---
<逐字原文>
---NEW---
<逐字新文>
===END===
```

- 新增文件用 `===FILE: <路径>|CREATE===`。
- 判定不改用：
  ```
  ===FILE: <路径>|SKIP===
  <一行理由>
  ===END===
  ```
- `OLD` 必须是逐字可匹配的原文（含所有反引号、括号、标点、破折号 `—`），并且在该文件中**只出现一次**；需要时把整行（含句末句号）作为 `OLD`，不要截取片段。
- `NEW` 同样逐字给全，不要写"同上"、不要用省略号。
- 块外不要写任何解释性正文；判定结论放在块**之前**，最多 10 行。

## 7. 硬约束

- 不恢复、不重建 `phase-3.5-forget-suppression-and-cursor-consumption.md`，也不得臆造其内容。
- 不新增规范内容，不改任何约束语义（"supersedes earlier provisional wording" 这类语义必须保留）。
- 不改标题、不改章节编号、不动第 4 节给出的上下文之外的行。
- 不引入新的交叉引用目标；只允许指向已存在的 `docs/governance/documentation-gaps.md`。
- 中文镜像的改动必须是"披露句"级别，不得重译整段、不得改变术语大小写风格。
- 不写计划、不写验证步骤、不写"建议后续"。
