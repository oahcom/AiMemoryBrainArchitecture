---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Executed prompt snapshot; provenance is NOT_VERIFIED."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Executed prompt snapshot for AID-2026-269"
    canonical_scope_id: "ai-development/aid-2026-269-prompt"
    canonical_scope_keywords:
      - "exact-head-review"
      - "prompt-snapshot"
      - "execution-specification"
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-269 — Exact-Head Independent Review Protocol v1 执行规格快照

| 字段 | 值 |
|---|---|
| Work Item | AID-2026-269 |
| Renumbered from | `268` — 268 在 main 树、INDEX 和所有开启的 PR 中均未占用，但已关闭未合并的 PR #1371（分支 `fix/aid-268-manifest-blob-pins`，head `efac9a1c`）仍在分支空间保留 `268/` 目录；按 AID-2026-240 `identifier_allocation` 记录的仓库约定（分支空间计入占用），本工作项顺延为 269（Owner 裁决，`reply-6b08fa9b-124545.md` §1） |
| Prompt ID / version | `AID-2026-269-PROMPT` / v1 |
| Repository / base branch | `oahcom/AiMemoryBrainArchitecture` / `main` |
| Baseline commit | `987d26021affbb5ba6d651e0fb5985d6bd4026a5` |
| Carrier | #1278 — https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1278（本工作项不修复 #1278） |
| Class / risk | DOC/GOVERNANCE + GATE/PROTOCOL / R1 |
| Executing sessions | L2-A = `NOT_EXPOSED`；L2-B = `NOT_EXPOSED`；L2-C = `NOT_EXPOSED`；L3 = `PENDING`（平台不提供稳定会话标识，故以占位符记录，见 `session-evidence.md`） |
| Instruction source | `chatgpt-session-ops/scripts/accounts/acct3/replies/reply-6b08fa9b-115953.md` 的 `## R2 工作包 WP-2` 块（L1 裁决） |
| Snapshot nature | 分隔线以下为 L1 裁决 `## R2 工作包 WP-2` 的执行指令文本。唯一改动是工作项标识由 268 顺延为 `AID-2026-269`（Owner 裁决 §1）；其余字符未改写、未删减、未重排。`## R2 自设评估标准` 与 `## R2 下一轮方向` 不属于本工作项的执行规格，故不包含 |

## 七项核心要素映射（AI-STD-001 §5.1）

被复制的块使用裁决自身的章节名，未逐字携带七项要素名称。下表只做映射，不改变块内任何内容（工作项标识的顺延见上表 `Renumbered from`）。

| 七项核心要素 | 块内对应章节 |
|---|---|
| 1 任务标识 | `## R2 工作包 WP-2` 头部（载体 #1278、工作项 ID AID-2026-269、目标）；`### L2 子代理分工` |
| 2 目标与边界 | `- **目标（一句话）：**`；`### 产出物清单` 的“不修改现有规范根”；`### 冲突隔离` |
| 3 上下文与依赖 | `### 复核/实现规格` 五（#1278 待复核数据）；`### 产出物清单`；`### 冲突隔离` |
| 4 约束与执行指导 | `### 复核/实现规格` 一至七；`### L2 子代理分工` 职责边界 |
| 5 验收与交付物 | `### 产出物清单`；`### 验收判据` R2-01 … R2-20 |
| 6 证据与审查 | `### 验收判据` R2-11、R2-13、R2-14、R2-19、R2-20；`### L3 独立复核清单` |
| 7 停止条件与协调 | `### 冲突隔离`（INDEX 冲突即停止并重算）；`### L2 子代理分工`（职责边界与基线 SHA 记录） |

---

<!-- 执行指令开始：L1 裁决 `## R2 工作包 WP-2`，止于 `## R2 自设评估标准` 之前；工作项标识已按 Owner 裁决 §1 由 268 顺延为 AID-2026-269 -->

## R2 工作包 WP-2

- **载体：** #1278，新增工作项。
- **工作项 ID：AID-2026-269**
  - 依据：协调方提供的远端分支扫描显示 268 及以上未占用。
  - 动工时重新检查所有状态 PR、远端分支和 main 上已有工作项目录。
  - 如果 268 已被认领，依次顺延至 269、270，不得占用 a260/a261 的载体。
  - 该工作项为独立审查与治理协议，不承担 #1278 的修复实现。
- **目标（一句话）：**

  建立可复用、可独立执行、可机器判定的 Exact-Head Independent Review Protocol，并对 AID-2026-092 的错误 prompt digest 完成一次有历史证据、原始命令、独立 SHA-256 复算和最终判定的真实审查。

### 产出物清单

所有文件均为新增工作项目录中的记录，不修改现有规范根。

| 文件 | 作用 |
|---|---|
| `14-ai-development/work-items/AID-2026-269/manifest.yaml` | 工作项身份、范围、验收标准 |
| `14-ai-development/work-items/AID-2026-269/prompt-v1.md` | 执行规格快照 |
| `14-ai-development/work-items/AID-2026-269/exact-head-review-protocol-v1.md` | 可复用独立复核协议 |
| `14-ai-development/work-items/AID-2026-269/review-case-1278.md` | #1278 首个审查用例 |
| `14-ai-development/work-items/AID-2026-269/evidence.md` | 原始命令、输出、摘要和判定 |
| `14-ai-development/work-items/AID-2026-269/session-evidence.md` | 实际实施与独立审查会话证据 |
| `14-ai-development/work-items/INDEX.md` | 追加一条工作项登记 |

另外：

- 在 GitHub Issue #1278 发布独立审查结果评论。
- 评论必须链接 AID-2026-269 的证据文件及最终提交 SHA。
- 不关闭 #1278。
- 不把审查发现直接解释为修复完成。
- 不修改 AID-2026-092 的 manifest、prompt 或 INDEX 历史值。

### 复核/实现规格

本包不实现软件检查器。产出的是协议、真实复核记录和可重复的机器判定结果。

**一、协议适用范围**

协议名称：

`Exact-Head Independent Review Protocol v1`

适用于：

1. manifest 声明的 SHA-256。
2. prompt 文件摘要及字节数。
3. evidence blob 身份。
4. root blob 身份。
5. INDEX 中复制的摘要。
6. 工作项归属、PR、merge SHA 等可追溯声明。
7. 测试数量、测试通过数量等可执行验收断言。
8. 其他能够从已提交对象独立复算的声明。

每条声明必须归入以下类别：

| 类别 | 判定方法 |
|---|---|
| BLOB_IDENTITY | 从提交对象读取原始字节并重算 |
| COMMIT_IDENTITY | 从 Git 对象数据库解析并验证 |
| COUNT_ASSERTION | 重新执行指定测试并计数 |
| ATTRIBUTION | 对照提交、PR、工作项和原始证据 |
| HISTORICAL_ASSERTION | 在明确的历史引用范围内复算 |
| NON_MACHINE_ASSERTION | 标记为需要人工判断，不得伪装成机器验证 |

不能验证的声明必须明确记录，不能默认通过。

**二、精确 Head 锁定**

每次复核开始必须记录：

```bash
git fetch origin --prune

git rev-parse origin/main

git rev-parse --verify "$CANDIDATE_SHA^{commit}"

git rev-parse "$CANDIDATE_SHA^{tree}"
```

保存：

- 审查开始时间。
- repository。
- base SHA。
- candidate SHA。
- candidate tree SHA。
- PR 编号（如有）。
- 审查者身份。
- Git 版本。
- Python 版本（如执行 Python 复算）。

候选 SHA 必须是完整提交 SHA。

任何候选 SHA 变化，都意味着原审查结论失效，必须重新执行。

**三、blob 独立复算**

对每条声明：

```bash
git ls-tree -r -z "$CANDIDATE_SHA"

git cat-file blob "$BLOB_SHA"
```

使用独立计算程序：

```python
import hashlib

actual = hashlib.sha256(blob_bytes).hexdigest()
```

逐项记录：

```text
declaration_file
declaration_line
declaration_field
declared_path
declared_sha256
actual_blob_object_sha
actual_sha256
actual_bytes
candidate_sha
result
```

必须同时核对：

- 路径确实存在。
- 路径解析到正确对象。
- 实际字节可读取。
- 摘要计算没有经过文本转换。
- 声明值与实测值逐字相等。

**四、历史声明验证**

#1278 的核心不只是当前摘要不匹配，还包括声明值在任何可达历史提交中都不存在。

复核者必须检查：

```bash
git rev-list --all
```

再针对相关路径枚举历史版本：

```bash
git rev-list --all -- \
  14-ai-development/work-items/AID-2026-083/prompt-v1.md \
  14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

对每个实际存在的历史版本：

```bash
git show "$COMMIT:$PATH" | sha256sum
```

注意：命令中必须分别处理两个路径，不能将文件名、提交 SHA 和摘要混在一起导致归属丢失。

保存完整结果，按：

```text
commit_sha
path
byte_count
sha256
```

建立历史摘要清单。

历史结论必须明确其范围：

- 当前本地所有 refs。
- 本次 fetch 后的远端 refs。
- 可达提交集合。
- 不可达对象不在结论范围内。
- 未取得的历史 refs 不得宣称已检查。

**五、#1278 首个用例**

目标声明：

```yaml
prompt_id: AID-2026-083-PROMPT
prompt_file: 14-ai-development/work-items/AID-2026-092/prompt-v1.md
prompt_sha256: 9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1
prompt_bytes: 2455
```

Issue 已提供的待独立复核数据：

```text
声明字节数：2455
声明 SHA256：9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1

实测字节数：3772
实测 SHA256：a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3
```

这些数值是待复核输入，不是预先授予的验收结果。

复核者必须从执行时锁定的 candidate SHA 重新取得文件，并独立计算。

随后检查声明值在可达历史提交中是否曾出现。

特别核对：

- `manifest.yaml` 首次引入提交。
- `prompt-v1.md` 首次引入提交。
- 两者是否在同一提交首次出现。
- 首次引入时的真实字节数。
- 首次引入时的真实摘要。
- INDEX 对同一声明的重复引用。
- 是否有其他提交曾包含声明的 2455 字节版本。

**六、错误分级**

| 等级 | 名称 | 处理 |
|---|---|---|
| E0 | VERIFIED | 全部证据独立复算一致 |
| E1 | DECLARATION_MISMATCH | 声明值与实际字节不一致 |
| E2 | HISTORICAL_NONEXISTENCE | 声明值在限定历史范围内从未出现 |
| E3 | ATTRIBUTION_MISMATCH | 归属、提交、PR 或修正记录错误 |
| E4 | INCOMPLETE_EVIDENCE | 缺少原始证据或复核范围不完整 |
| E5 | CANDIDATE_DRIFT | 审查期间候选 SHA 改变 |
| E6 | UNVERIFIABLE | 无法独立验证的人工性声明 |

E1、E2、E3 不允许判定为 PASS。

E4、E5、E6 不允许宣告完整审查通过。

E1 和 E2 可以同时出现。

**七、最终审查结果**

必须输出机器可解析的 JSON 结果，作为 evidence 的附录：

```json
{
  "protocol": "Exact-Head Independent Review Protocol v1",
  "work_item": "AID-2026-269",
  "issue": 1278,
  "candidate_sha": "FULL_SHA",
  "candidate_tree_sha": "FULL_TREE_SHA",
  "review_complete": true,
  "declarations_checked": 0,
  "verified": 0,
  "failed": 0,
  "unverifiable": 0,
  "findings": [],
  "overall_result": "FAIL"
}
```

字段值必须来自实际复核，不得预填虚构的完成数量。

### 验收判据

以下项目全部必须通过。

| 编号 | 判定项目 | 判定命令 | 期望输出 |
|---|---|---|---|
| R2-01 | 工作项目录 | `test -d 14-ai-development/work-items/AID-2026-269` | exit 0 |
| R2-02 | 协议文件 | `test -s 14-ai-development/work-items/AID-2026-269/exact-head-review-protocol-v1.md` | exit 0 |
| R2-03 | 用例文件 | `test -s 14-ai-development/work-items/AID-2026-269/review-case-1278.md` | exit 0 |
| R2-04 | manifest YAML | `python3 -c "import yaml; yaml.safe_load(open('14-ai-development/work-items/AID-2026-269/manifest.yaml'))"` | exit 0 |
| R2-05 | candidate 锁定 | `git rev-parse --verify "$CANDIDATE_SHA^{commit}"` | 完整 SHA |
| R2-06 | tree 锁定 | `git rev-parse "$CANDIDATE_SHA^{tree}"` | 完整 tree SHA |
| R2-07 | 当前摘要复算 | 对 AID-2026-092 的实际 prompt 执行 SHA-256 | 输出实际摘要和字节数 |
| R2-08 | 历史复算 | 对全部限定可达历史提交重新计算 SHA-256 | 每个历史版本都有记录 |
| R2-09 | 首次引入提交 | 对 manifest 和 prompt 分别执行历史枚举 | 两者的首次引入提交明确 |
| R2-10 | INDEX 对账 | 从候选树读取 INDEX 对应行 | 与 manifest 声明逐项对照 |
| R2-11 | 独立计算 | L3 使用独立脚本重算 | 与 L2 结果一致 |
| R2-12 | 错误分级 | 检查 JSON finding | 每个不一致声明有明确等级 |
| R2-13 | 证据完整 | `test -s 14-ai-development/work-items/AID-2026-269/evidence.md` | exit 0 |
| R2-14 | 会话证据 | 检查 session-evidence.md 必需字段 | 全部存在 |
| R2-15 | 协议复用性 | 检查协议是否定义输入、步骤、判定、分级、证据结构 | 6 个必需章节全部存在 |
| R2-16 | 既有门禁 | 执行当前 main 对应的 hygiene、traceability、bilingual 检查 | 全部 exit 0 |
| R2-17 | 文件隔离 | `git diff --name-only "$BASE_SHA...$CANDIDATE_SHA"` | 仅 WP-2 允许路径 |
| R2-18 | PR 证据 | 检查 #1278 评论及其引用 | 指向真实最终提交和证据 |
| R2-19 | SHA 绑定 | 对 evidence 中所有文件引用重新读取 | 文件摘要与记录一致 |
| R2-20 | 最终复核 | L3 对最终 head 重新执行完整协议 | 独立复核证据完整 |

特别要求：R2-08 的历史搜索范围必须随证据保存，不能只保存最后的 `sort -u` 结果。

### L2 子代理分工

**共 3 个 L2 会话。**

| 会话 | 负责范围 | 交付物 | 自检 |
|---|---|---|---|
| L2-A：协议设计 | `exact-head-review-protocol-v1.md` | 可复用的精确 Head 复核协议 | 章节完整性检查；逐项验证协议字段 |
| L2-B：真实用例复核 | AID-2026-092、#1278 历史数据 | `review-case-1278.md`、历史摘要清单、原始复算输出 | 重新运行 Git 历史枚举和 SHA-256 计算 |
| L2-C：治理记录 | manifest、prompt、evidence、session-evidence、INDEX | 完整工作项记录和 GitHub 投递文本 | YAML 解析、prompt 摘要、INDEX 唯一性检查 |

职责边界：

- L2-A 不负责判定 #1278 是否真实存在缺陷。
- L2-B 不负责修改协议。
- L2-C 不负责生成或修改任何被审查对象。
- L0 不承担审查设计、结论判断或实现。
- 所有 L2 必须记录自己的基线 SHA。

### L3 独立复核清单

L3 必须是与 L0、L2-A、L2-B、L2-C 不同的执行会话。

**协议审查：**

1. 检查协议是否规定完整 commit SHA。
2. 检查协议是否区分 candidate tree 和 working tree。
3. 检查协议是否规定历史引用范围。
4. 检查协议是否明确原始字节计算。
5. 检查协议是否规定无法验证时不得 PASS。
6. 检查协议是否要求保留原始命令和退出码。

**真实用例复核：**

7. 独立 fetch 当前远端 refs。
8. 独立锁定最终 candidate SHA。
9. 独立取得 AID-2026-092 的 manifest 和 prompt。
10. 重新计算实际字节数。
11. 重新计算实际 SHA-256。
12. 重新枚举相关历史提交。
13. 重新计算每个历史版本的摘要。
14. 独立确认声明值是否曾出现。
15. 独立核对首次引入提交。
16. 独立核对 INDEX 中的重复摘要。
17. 独立判定 E1/E2/E3/E4 等级。

**交付复核：**

18. 验证 evidence 所有 SHA。
19. 验证 JSON 结果与文本报告一致。
20. 验证最终审查结论绑定最终提交 SHA。
21. 检查没有对 AID-2026-092 进行修复性修改。
22. 检查 #1278 仍然保持开放。
23. 重跑当前 main 的 hygiene、traceability、bilingual 门禁。
24. 将独立复核结果附加到 evidence。

L3 必须提供自己的命令日志和独立计算结果，不能只在 L2 的报告上签字。

### 冲突隔离

**a260：**

完全不接触：

- `AID-2026-260/`
- `fix/2026-11-27-aid260-manifest-blob-pins`
- `scripts/ci/check_blob_pin_integrity.py`
- `scripts/ci/test_check_blob_pin_integrity.py`
- `.github/workflows/blob-pin-integrity.yml`

WP-2 不实现 blob-pin 检查器，也不对 a260 的代码提交进行修改。

**a261：**

完全不接触：

- `AID-2026-261/`
- a261 工作树中的 INDEX 修改。
- a261 的工作项唯一性门禁相关文件。

WP-2 仅允许在 INDEX 中追加 AID-2026-269 的一行；必须基于动工时最新 main，并先确认 a261 的 INDEX 修改已经进入或尚未进入 main。不得覆盖其未提交内容。

**其他活跃会话：**

禁止修改：

- `simple-gate`。
- AID-2026-211。
- RC-1/RC-2 已触碰文件。
- #1361、#1364 的 closeout 记录。
- 任何现有 workflow。
- 任何现有检查器。
- AID-2026-092 的原始文件。
- AID-2026-079 的原始文件。
- AID-2026-116 的原始文件。

本轮只新增 AID-2026-269 记录、追加 INDEX 一行，并在 #1278 投递审查结果。

如果 INDEX 的修改出现冲突，停止 INDEX 修改，重新基于最新 main 计算差异，不得覆盖其他会话的修改。
