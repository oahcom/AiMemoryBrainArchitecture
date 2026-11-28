# 四份文件完整内容 + 一项必须先裁定的新事实（tip baseline 已是 4 条）

## 〇、必须先裁定的新事实
`daa935f7a` 上 `scripts/ci/baselines/manifest-blob-pins.txt` **已经正好是这 4 条**，原文：

```text
# AID-2026-268 manifest blob-pin baseline
# Current baseline contains exactly 4 observed failures.
# The other 11 previously recorded entries have been fixed and removed.
# Two remaining failures are historical prompt byte-count mismatches:
# AID-2026-101 and AID-2026-102 each declare 4470 bytes, while
# their current prompt-v1.md files contain 4412 bytes.
# Their corresponding prompt SHA-256 mismatches are no longer present
# in the current failure set and are therefore not retained here.
# Two additional failures are historical PATH_MISSING entries for
# AID-2026-261/prompt-v1.md. The path remains absent from the candidate
# tree, while the historical declarations remain present:
# one declares a byte count of 0 and the other declares an all-zero SHA-256.
# These four entries remain because gate_ratchet requires the baseline
# to equal the current failure set exactly. A fixed entry is stale;
# removing an entry that still fails is a regression.
MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-101/prompt-v1.md declared=4470 actual=4412
MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-102/prompt-v1.md declared=4470 actual=4412
PATH_MISSING path=14-ai-development/work-items/AID-2026-261/prompt-v1.md; declared=0
PATH_MISSING path=14-ai-development/work-items/AID-2026-261/prompt-v1.md; declared=0000000000000000000000000000000000000000000000000000000000000000
```

**因此 baseline 的合并结论可能根本不需要改文件。** 两种口径请你选：

| 选项 | 做法 | 结果 |
|---|---|---|
| **O1** | 直接采用 main 原文（theirs） | baseline 文件**零 diff**；18 条待审清单与 6 条缺陷记录作为新增审计材料 |
| **O2** | 保留 4 条，替换注释块为本轮裁定文本 | baseline 文件只有注释 diff（下方 §1 全文） |

O2 的理由：main 的注释只说「11 条已修复」，没有交代 18 条待审与 6 条转出；O1 的理由：注释已经准确描述了 4 条活动 finding，且 ratchet 只看条目不看注释。

## 一、baseline（O2 全文，17 行）
```text
# AID-2026-268 manifest blob-pin baseline
# Merged from base(15) / ours(39) / theirs(4) during the #1426 integration.
# Ruling of 2026-11-28 (Owner session 6b0a1b64):
#   deleted as superseded by current manifest values: 11
#   deleted as duplicate legacy-format entries:        2
#   transferred to standalone defect records:          6
#   retained in pending historical review ledger:     18
#   active ratchet findings retained at daa935f7a:     4
# The active baseline contains only findings reproduced by the
# current main checker at the pinned target commit.
# Historical diagnostics not reproduced by the current checker
# are tracked separately and are not treated as fixed or resolved.

MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-101/prompt-v1.md declared=4470 actual=4412
MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-102/prompt-v1.md declared=4470 actual=4412
PATH_MISSING path=14-ai-development/work-items/AID-2026-261/prompt-v1.md; declared=0
PATH_MISSING path=14-ai-development/work-items/AID-2026-261/prompt-v1.md; declared=0000000000000000000000000000000000000000000000000000000000000000
```

## 二、待审清单全文（26 行）
文件：`scripts/ci/baselines/pending-historical-diagnostics.md`

```markdown
# Pending historical diagnostics — excluded from active blob-pin ratchet

Measured against `daa935f7a7ecc808f1775be8cf153cf715961b08` (2026-11-28).
These findings do not appear in the current main checker output. That is **not** a fix:
the checker no longer performs the corresponding check, or the field moved out of its read path.

| baseline ID | kind | manifest | field / path | original finding | why it no longer triggers | status |
|---|---|---|---|---|---|---|
| #16 | INCOMPLETE | `14-ai-development/work-items/AID-2026-093/manifest.yaml` | `prior_invariant_source_blob` | `INCOMPLETE UNRESOLVED(prior_invariant_source_blob blob locator): manifest=14-ai-development/work-items/AID-202` | checker no longer reads this key; field still present with value 50566d16… | PENDING REVIEW |
| #17 | INCOMPLETE | `14-ai-development/work-items/AID-2026-023/manifest.yaml` | `prompt_original_payload_sha256` | `INCOMPLETE UNRESOLVED(prompt_original_payload_sha256): manifest=14-ai-development/work-items/AID-2026-023/mani` | checker no longer reads this key; field still present | PENDING REVIEW |
| #18 | INCOMPLETE | `14-ai-development/work-items/AID-2026-026/manifest.yaml` | `prompt_original_payload_sha256` | `INCOMPLETE UNRESOLVED(prompt_original_payload_sha256): manifest=14-ai-development/work-items/AID-2026-026/mani` | checker no longer reads this key; field still present | PENDING REVIEW |
| #19 | INCOMPLETE | `14-ai-development/work-items/AID-2026-241/manifest.yaml` | `renumbering.previous_prompt_sha256` | `INCOMPLETE UNRESOLVED(renumbering.previous_prompt_sha256): manifest=14-ai-development/work-items/AID-2026-241/` | checker no longer reads this key; field still present | PENDING REVIEW |
| #25 | INCOMPLETE | `14-ai-development/work-items/AID-2026-150/manifest.yaml` | `manifest.scope.fence_conflict.source_blob` | `INCOMPLETE UNRESOLVED(missing field locator): manifest=14-ai-development/work-items/AID-2026-150/manifest.yaml` | checker no longer reads fence_conflict; field present at scope.fence_conflict.source_blob | PENDING REVIEW |
| #26 | INCOMPLETE | `14-ai-development/work-items/AID-2026-003/manifest.yaml` | `discovered.manifest.policy_unification_ruling.instruction_sha256` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-003/manifest.yaml discovered.manifest.policy_unifica` | checker no longer reads this key; value is still NOT_VERIFIED | PENDING REVIEW |
| #27 | INCOMPLETE | `14-ai-development/work-items/AID-2026-003/manifest.yaml` | `prompt_sha256` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-003/manifest.yaml prompt_sha256(top-level): invalid ` | tip checker only reads prompt.prompt_sha256 (nested); value is still NOT_VERIFIED | PENDING REVIEW |
| #28 | INCOMPLETE | `14-ai-development/work-items/AID-2026-004/manifest.yaml` | `prompt_sha256` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-004/manifest.yaml prompt_sha256(top-level): invalid ` | tip checker only reads prompt.prompt_sha256 (nested); value is still NOT_VERIFIED | PENDING REVIEW |
| #29 | INCOMPLETE | `14-ai-development/work-items/AID-2026-004/manifest.yaml` | `source_translation_pairs[0].translation_path` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-004/manifest.yaml source_translation_pairs[0].transl` | checker no longer validates translation_path locators; field still present | PENDING REVIEW |
| #30 | INCOMPLETE | `14-ai-development/work-items/AID-2026-004/manifest.yaml` | `source_translation_pairs[1].translation_path` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-004/manifest.yaml source_translation_pairs[1].transl` | checker no longer validates translation_path locators; field still present | PENDING REVIEW |
| #31 | INCOMPLETE | `14-ai-development/work-items/AID-2026-004/manifest.yaml` | `source_translation_pairs[2].translation_path` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-004/manifest.yaml source_translation_pairs[2].transl` | checker no longer validates translation_path locators; field still present | PENDING REVIEW |
| #32 | INCOMPLETE | `14-ai-development/work-items/AID-2026-064/manifest.yaml` | `prompt_sha256` | `INCOMPLETE manifest=14-ai-development/work-items/AID-2026-064/manifest.yaml prompt_sha256(top-level): invalid ` | tip checker only reads prompt.prompt_sha256 (nested); value is still NOT_VERIFIED | PENDING REVIEW |
| #34 | PATH_MISSING | `14-ai-development/work-items/AID-2026-170/manifest.yaml` | `owner_ruling.current_blob` | `PATH_MISSING owner_ruling.current_blob path=09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14` | checker no longer reads this key; field still present in AID-2026-170 | PENDING REVIEW |
| #35 | PATH_MISSING | `14-ai-development/work-items/AID-2026-170/manifest.yaml` | `owner_ruling.superseded_blob` | `PATH_MISSING owner_ruling.superseded_blob path=09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.` | checker no longer reads this key; field still present in AID-2026-170 | PENDING REVIEW |
| #36 | PATH_MISSING | `14-ai-development/work-items/AID-2026-170/manifest.yaml` | `reconciliation.pointers_changed[0].after_blob.target` | `PATH_MISSING reconciliation.pointers_changed[0].after_blob.target path=09-security-governance/phase-3.8.10-i-p` | checker no longer reads this key; before_blob/after_blob are flat keys (no .target sub-object) | PENDING REVIEW |
| #37 | PATH_MISSING | `14-ai-development/work-items/AID-2026-170/manifest.yaml` | `reconciliation.pointers_changed[0].before_blob.target` | `PATH_MISSING reconciliation.pointers_changed[0].before_blob.target path=09-security-governance/phase-3.8.9-i-p` | checker no longer reads this key; before_blob/after_blob are flat keys (no .target sub-object) | PENDING REVIEW |
| #38 | PATH_MISSING | `14-ai-development/work-items/AID-2026-170/manifest.yaml` | `reconciliation.pointers_changed[1].after_blob.target` | `PATH_MISSING reconciliation.pointers_changed[1].after_blob.target path=09-security-governance/phase-3.8.10-i-p` | checker no longer reads this key; before_blob/after_blob are flat keys (no .target sub-object) | PENDING REVIEW |
| #39 | PATH_MISSING | `14-ai-development/work-items/AID-2026-170/manifest.yaml` | `reconciliation.pointers_changed[1].before_blob.target` | `PATH_MISSING reconciliation.pointers_changed[1].before_blob.target path=09-security-governance/phase-3.8.9-i-p` | checker no longer reads this key; before_blob/after_blob are flat keys (no .target sub-object) | PENDING REVIEW |
```

（`original finding` 列为原始 finding 的前 110 字符，用于与 baseline ID 对应；完整原文在 `baseline-diff.md` 审计材料中。若你要求列完整原文，我可以改为全文，但表格会显著变宽。）

## 三、DEFECT-1 全文
```markdown
---
title: "frontmatter_blob_sha is a fragment digest, not a repository blob pin"
status: "OPEN"
classification: "contract-definition-gap"
discovered_at_commit: "daa935f7a7ecc808f1775be8cf153cf715961b08"
evidence:
  - "14-ai-development/work-items/AID-2026-109/manifest.yaml @ 9a2063ae1fa5d905b3817cd4eddba065a06daa73 (five frontmatter_blob_sha declarations)"
  - "09-security-governance/global-forget-target-inventory-and-completion-evidence.md @ 9a2063ae (frontmatter bytes, 45 lines between fences)"
  - "09-security-governance/forget-retention-backup-and-erasure-policy.md @ 9a2063ae"
  - "09-security-governance/principal-actor-and-authorization-contract.md @ 9a2063ae"
  - "09-security-governance/scope-and-revocation-policy.md @ 9a2063ae"
  - "09-security-governance/security-and-identity-overview.md @ 9a2063ae"
  - "scripts/ci/check_manifest_blob_pins.py @ 9a2063ae (emits UNCLASSIFIED for the five fields)"
  - "scripts/ci/check_manifest_blob_pins.py @ daa935f7a (no occurrence of frontmatter_blob_sha)"
related_baseline_ids:
  - "#20"
  - "#21"
  - "#22"
  - "#23"
  - "#24"
scope: "diagnostic"
---

# DEFECT-1 — `frontmatter_blob_sha` is a fragment digest, not a repository blob pin

> 本记录只陈述调查结果。**尚未裁定修复方案，不构成 checker 变更授权，也不构成 baseline 处置授权。**

## 1. 声明与对象

样本 commit：`9a2063ae1fa5d905b3817cd4eddba065a06daa73`
目标 commit（现状复核）：`daa935f7a7ecc808f1775be8cf153cf715961b08`

| 字段路径（AID-2026-109） | 声明值 | 是否为仓库独立对象 |
|---|---|---|
| `source.selected_source_files[0].frontmatter_blob_sha` | `a0740d117603891c0a9633d093bd01cb9a92f8cf` | 否 |
| `source.selected_source_files[1].frontmatter_blob_sha` | `60b666d7b6ea38a9f2d70aa47744f3d076876e02` | 否 |
| `source.selected_source_files[2].frontmatter_blob_sha` | `d1b950f16ce89b8c23549c99bb885b0014a78dbf` | 否 |
| `source.selected_source_files[3].frontmatter_blob_sha` | `9252258fa0a5f64e3cea75513da4e5e48d6c7847` | 否 |
| `source.selected_source_files[4].frontmatter_blob_sha` | `fd42af80595cf8c4ef92795f64f5beacba38e7db` | 否 |

## 2. 重算证据（5/5 命中，唯一字节定义）

```
algorithm = git blob sha1   (sha1("blob <len>\0" + bytes))
bytes     = 从文件首行 "---" 起，到闭合 "---" 行（含）为止的原始字节
            （含首尾 fence，含行尾换行，按文件原始换行符）
source    = 同级 restored_blob_sha 所指文件内容
```

对每条声明各测 21 种候选字节定义（7 种字节切片 × 3 种哈希：`git-blob-sha1` / `sha1(raw)` / `sha256`），只有上述一种命中。
7 种切片：frontmatter body（去 fence）、body + 尾换行、含双 fence、含双 fence + 尾换行、`strip()` 后的 body、LF 规范化后的 body、LF 规范化 + 尾换行。

**口径限定**：这是本轮调查的实测结果，**不等于契约已经定义**该字段的摘要对象、算法或作用域。

## 3. 语义结论（限定于已测事实）

- 声明值是有效的 Git-blob-sha1 摘要；
- 摘要对象是**文件 frontmatter 片段的原始字节**，该片段从不作为独立 Git 对象存在；
- 同 manifest 的 `source_blob_sha` / `restored_blob_sha` 指向完整文件，且为真实存在的 Git 对象。

## 4. checker 行为

- `9a2063ae`：`#1426` checker 报 `UNCLASSIFIED … source declaration has no blob_pins registration`（293 条中的 5 条）
- `daa935f7a`：tip checker 全文不含 `frontmatter_blob_sha`（字符串计数 0），不再报告
- **checker 停止扫描 ≠ 问题解决**

## 5. 契约缺口

- 全树（`9a2063ae`，md/yaml/yml/json/py）只有 `AID-2026-109/manifest.yaml` 出现该字段字样
- 没有任何文档定义该字段的摘要对象、算法或作用域

## 6. 未决问题（本记录不裁定）

1. 该字段是否应纳入 blob-pin 契约？
2. 若纳入，pin 的 locator 如何表达「文件内的片段」？
3. 若不纳入，是否需要显式标注「非仓库对象摘要」，以免再次被键名启发式命中？

## 7. 复现

```
git cat-file -e a0740d117603891c0a9633d093bd01cb9a92f8cf     # rc=1，对象不存在
git cat-file -e daa935f7a:14-ai-development/work-items/AID-2026-109/manifest.yaml
```
```

## 四、DEFECT-2 全文
```markdown
---
title: "Nested gate_a_reconstruction declarations are not inspected by the blob-pin checker"
status: "OPEN"
classification: "checker-contract-gap"
discovered_at_commit: "daa935f7a7ecc808f1775be8cf153cf715961b08"
evidence:
  - "14-ai-development/work-items/AID-2026-100/manifest.yaml @ daa935f7a (nested baseline_and_source_evidence.gate_a_reconstruction[0])"
  - "scripts/ci/check_manifest_blob_pins.py @ daa935f7a (line 207 reads top-level only; lines 220-221 show the nested fallback used for authored_indexes)"
  - "scripts/ci/check_manifest_blob_pins.py --commit daa935f7a output (4 findings, none for gate_a_reconstruction)"
  - "git cat-file -e daa935f7a:04-memory-compiler/compiler-stage-contract.md (absent)"
related_baseline_ids:
  - "#33"
scope: "diagnostic"
---

# DEFECT-2 — Nested `gate_a_reconstruction` declarations are not inspected by the blob-pin checker

> 本记录只陈述调查结果。**尚未裁定修复方案，不构成 checker 变更授权，也不构成 manifest 修改授权。**

## 1. 三个事实必须分开看

### 事实 A — 底层路径缺失
`04-memory-compiler/compiler-stage-contract.md` 在目标 commit `daa935f7a` 中**不存在**；
`docs/en/04-memory-compiler/compiler-stage-contract.md` 存在。

### 事实 B — manifest 声明仍存在
AID-2026-100 仍声明（字段已迁入 `baseline_and_source_evidence`）：

```yaml
baseline_and_source_evidence:
  gate_a_reconstruction:
    - root: 04-memory-compiler/compiler-stage-contract.md
      reconstructed_root_blob: 1f79eeb40fb234423290f97fcce934e11bdca9bf
      disposition: REMOVED_FROM_PR_SCOPE_BY_OWNER_RULING_ON_OA_MERGE_2026_11_26_01
      note: The reconstruction was produced at commit cae1b31e and is retained there; ...
```

### 事实 C — checker 因读取位置不兼容而漏读
tip checker 第 207 行读取 `doc.get("gate_a_reconstruction")`（**仅顶层**）；
同一函数在 `authored_indexes` 上做了嵌套兼容（第 220–221 行）：

```python
source_evidence = as_mapping(doc.get("baseline_and_source_evidence"))
authored_indexes = source_evidence.get("authored_indexes", doc.get("authored_indexes", []))
```

`gate_a_reconstruction` 没有对应的嵌套回退。

**不得把事实 C 描述为「已修复」。**

## 2. 结果

- `daa935f7a` 上 main checker 输出 4 条 finding，**不含** #33
- 因此 #33 的消失不是「路径已恢复」，也不是「声明已撤回」，而是读取位置不兼容
- 同一 commit 上 `#1426` checker 因整套 `blob_pins[]` 模型报 384 条 UNCLASSIFIED，也未对该嵌套字段给出分类结论

## 3. 未决问题（本记录不裁定）

1. 修 checker 增加嵌套兼容，还是要求 manifest 把 `gate_a_reconstruction` 放回顶层？
2. `disposition: REMOVED_FROM_PR_SCOPE_BY_OWNER_RULING_…` 是否构成「不再校验该 pin」的正当豁免依据？（当前 checker 不读 `disposition`）
3. 未声明 `source_commit` / `commit`，`note` 中 `commit cae1b31e` 为短 SHA —— 是否满足 pin 的 scope 要求？

## 4. 复现

```
git cat-file -e daa935f7a:04-memory-compiler/compiler-stage-contract.md            # 不存在
git cat-file -e daa935f7a:docs/en/04-memory-compiler/compiler-stage-contract.md    # 存在
python scripts/ci/check_manifest_blob_pins.py --commit daa935f7a7ecc808f1775be8cf153cf715961b08
# 输出 4 条 finding，其中没有 gate_a_reconstruction
```
```

## 五、请你裁定
1. **O1 还是 O2**（baseline 零 diff，还是替换注释块）？
2. 三份新增/更新文件是否可按上述全文逐字落地？
3. 若批准，是否授权：基于 `daa935f7a` 建独立 worktree → 写入这 4 个路径 → 单条本地 commit `ci: reconcile manifest blob-pin baseline diagnostics`（不 push、不 merge）？

## 六、边界
未创建 worktree、未写仓库文件、未 push、未 merge；两个 checkpoint 与 `wt-1426-rebase` merge 状态未动。
