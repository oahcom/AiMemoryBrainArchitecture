# AID-2026-040 Authority Log

## 0. 本文件性质

本文件是 AID-2026-040 的事后证据归档记录（post-hoc archival record）。

本文件记录原始授权材料的可恢复摘录、引用有效性核查结果及相关实测发现。

本文件不构成原始授权，不追溯创设授权，也不改变历史提交、PR 或仓库状态。

所有归档行为均明确标记为：

`POST_HOC_ARCHIVAL — NOT RETROACTIVE AUTHORIZATION`

## 1. 归档原因

AID-2026-040 的授权审计发现，原始授权材料中的部分文件路径无法在指定历史提交 `61a45da7` 的仓库树中找到。

进一步核查发现，引用所指向的内容具有真实性证据，但其原始文件的完整性、字节等价性及历史仓库存在情况无法得到充分证明。

因此，本次归档的目的仅限于：

1. 保存目前能够恢复的授权材料摘录。
2. 明确区分内容真实性与文件路径可审计性。
3. 记录指定历史提交的仓库树核查结果。
4. 防止事后恢复材料被误认为原始授权文件或追溯授权。
5. 记录相关 PR 的独立缺陷类别及其核实状态。

本次归档不改变原始授权的历史状态。

## 2. 原始授权材料归档

### 2.1 归档状态

```yaml
archival_status: POST_HOC_ARCHIVAL
original_authorization_recreated: false
source_material:
  completeness: EXCERPT
  byte_equivalence: NOT_ESTABLISHED
  repository_presence_at_61a45da7: ABSENT
  historical_never_present: NOT_ESTABLISHED
```

特别说明：

`repository_presence_at_61a45da7: ABSENT` 仅表示指定提交 `61a45da7` 的 Git tree 不包含相应文件。

`historical_never_present: NOT_ESTABLISHED` 表示目前没有足够证据证明这些文件在仓库历史中从未出现。

单个 commit 的 tree 不包含某个文件，不能单独证明该文件历史上从未进入仓库。

因此，不得将本次核查结果表述为「这些文件从未进入仓库」。

### 2.2 原始文件摘录

以下材料均为：

`EXCERPT — NOT BYTE-EQUIVALENT TO ORIGINAL`

这些摘录用于保存可恢复的授权内容，不代表原始文件的完整副本，也不代表原始文件已被重新创建。

#### 原始材料一

<待归档的上一轮已核实原始摘录正文>

- 完整性：`EXCERPT`
- SHA-256：沿用上一轮已核实记录
- 原始文件字节数：沿用上一轮已核实记录
- 字节等价性：`NOT_ESTABLISHED`
- 指定提交 `61a45da7` 中的仓库存在状态：`ABSENT`

#### 原始材料二

<待归档的上一轮已核实原始摘录正文>

- 完整性：`EXCERPT`
- SHA-256：沿用上一轮已核实记录
- 原始文件字节数：沿用上一轮已核实记录
- 字节等价性：`NOT_ESTABLISHED`
- 指定提交 `61a45da7` 中的仓库存在状态：`ABSENT`

**归档限制**

上述两个材料不得被称为原始授权文件的完整恢复版本。

SHA-256 和字节数记录用于标识本次可核实的材料，不构成原始文件字节等价性的证明。

本次归档不改变原始授权材料的历史存在状态。

## 3. 引用有效性判定

本次审计区分两个独立问题：

1. 引用内容是否真实，即引用所描述的授权材料或决策内容是否具有可核实依据。
2. 引用路径是否可审计，即指定历史提交中是否存在该路径及其对应文件。

两者不能相互替代。

即使引用内容真实，只要指定历史提交中的文件路径不存在，仍然构成路径悬空缺陷。

内容真实性不能消除文件路径不可审计性。

因此：

- 不得因为引用内容真实而认定路径有效。
- 不得因为当前能够恢复摘录而认定原始文件曾存在于指定提交。
- 不得将事后归档解释为原始授权文件的历史恢复。
- 不得将本次归档解释为追溯授权。

所有归档材料的性质仍为：

`POST_HOC_ARCHIVAL — NOT RETROACTIVE AUTHORIZATION`

## 4. 三处登记及核实结果

本节记录 #433、#436 和 #464 三处相关载体的独立核查结果。

| 载体 | 缺陷类别 | 核实状态 | 依据 |
|---|---|---|---|
| #433 | `MAIN_COVERAGE_ASSERTS_UNMERGED_BRANCH_CONTENT`（不是授权文件缺失） | `VERIFIED` | main 上 `06-memory-context/context-implementation-coverage.md` 第 103 行声称的 guard `current_use_allowed` 和测试 `test_current_use_requires_every_currentness_gate`，仅存在于未合并的 PR #433 head `81558c8999`；main 全树 grep = 0 |
| #436 | 未定位到 `gap-owner-*` 引用 | 就授权引用而言：`NOT_VERIFIED_BY_COORDINATOR`；就实测而言：`NO_AUTHORITY_CITATION_FOUND` | `/pulls/436/files` 中全部 4 个改动文件均已读取，未发现任何 `gap-owner-*` 引用 |
| #464 | `AUTHORITY_ARTIFACT_PATHS_UNREADABLE` | `VERIFIED ABSENT at 61a45da7` | 指定提交递归树共 1082 条目，grep = 0；两处引用内容真实，但对应授权文件路径不存在 |

### 4.1 PR #433：不同缺陷类别

PR #433 is not an instance of the missing-authority-artifact defect. The relevant main-branch coverage entry asserts a guard and test that are present in the unmerged PR #433 head but absent from main. PR #433 itself is open and has not been merged, based on the coordinator's reported API inspection. This is a different defect class.

实测事实如下：

| 项目 | 核实结果 |
|---|---|
| PR 状态 | `open` |
| Draft | `false` |
| Merged | `false` |
| Merged at | `null` |
| Created | `2026-11-21T07:35:22Z` |
| Updated | `2026-11-21T11:31:54Z` |
| Head | `81558c8999` |
| Base | `e9c1e16a81` |
| Changed files | 3 |

GitHub API `/pulls/433` 确认了 PR 状态及 head、base 信息。

`/pulls/433/files` 确认三个改动文件：

| 文件 | 改动 |
|---|---:|
| `06-memory-context/reference-model/g_context_model.py` | +216 |
| `06-memory-context/reference-model/test_g_context_model.py` | +128 |
| `crates/memory-context/src/lib.rs` | modified 598 |

main 分支上的覆盖声明：

`06-memory-context/context-implementation-coverage.md` 第 103 行：

```text
PARTIAL — current-use guard current_use_allowed;
test test_current_use_requires_every_currentness_gate
```

该文件由提交 `5cc54a5499` 引入 main，其父提交为 `8c58d4c679`，并经 merge commit `1575a32b0e`（PR #444）进入 first-parent 链。

实测结果：

- main 全树搜索 `current_use_allowed`：0 条（不计 coverage.md 自身的声明）。
- main 全树搜索 `test_current_use_requires_every_currentness_gate`：0 条（不计 coverage.md 自身的声明）。
- PR #433 head `81558c8999` 的 `g_context_model.py` 中存在 `current_use_allowed`。
- PR #433 head `81558c8999` 的 `test_g_context_model.py` 中存在 `test_current_use_requires_every_currentness_gate`，为该文件第 15 个测试。

因此，#433 的问题是 main 分支的覆盖记录声称存在仅在未合并分支中存在的实现和测试。

这属于：

`MAIN_COVERAGE_ASSERTS_UNMERGED_BRANCH_CONTENT`

不是授权文件缺失，也不得重新归类为授权文件缺失。

此前的连续三个 PR 表述必须根据本次实测修正：

```text
Earlier "three PRs in a row" characterization:
PARTIALLY REFUTED
```

### 4.2 PR #436：授权引用尚未核实

针对 #436，协调层未能定位其引用不存在授权文件的具体文本。

本次补充实测确认：

- PR #436 已合并。
- Base：`a730880efd`
- Head：`1ffed9ed12`
- Changed files：4

四个改动文件：

| 文件 | 改动 |
|---|---:|
| `08-bmcp-protocol/protocol-index.md` | +36 |
| `08-bmcp-protocol/protocol-index.zh-CN.md` | +36 |
| `provider_outcome/requirements.txt` | modified 1 |
| `provider_outcome/test_provider_outcome.py` | +122 |

全部四个文件均已读取，未发现任何 `gap-owner-*` 引用。

因此，必须区分：

```yaml
PR-436-AUTHORITY-CITATION:
  status: NOT_VERIFIED_BY_COORDINATOR

PR-436-FILES-INSPECTION:
  status: NO_AUTHORITY_CITATION_FOUND
```

前者表示协调层未能定位授权引用的具体文本；后者表示本次实际读取的四个改动文件中未发现该类引用。

这不构成对 PR #436 全部历史内容的证实或排除，也不能据此补造授权引用证据。

不得将 #436 认定为已证实的授权文件缺失实例，也不得将其认定为已彻底排除的实例。

### 4.3 PR #464：授权文件路径不可读取

PR #464 的两处授权文件引用指向：

- `gap-owner-w1w3-decision.md`
- `gap-owner-v1v4-decision.md`

两处引用所指向的内容具有真实性依据。

但指定历史提交 `61a45da7` 的递归仓库树核查结果为：

- 递归树条目数：1082。
- 对两处授权文件路径及相关文件名进行搜索：0 条匹配。
- 两个授权文件均未出现在该提交的仓库树中。

因此，该实例确认属于：

`AUTHORITY_ARTIFACT_PATHS_UNREADABLE`

核实状态：

`VERIFIED ABSENT at 61a45da7`

该结论仅针对指定提交的仓库树，不推断两个文件在整个 Git 历史中从未出现。

引用内容真实，不意味着授权文件路径有效。

这仍然是独立的、可审计性层面的缺陷。

## 模式主张的状态

```text
Earlier "three PRs in a row" characterization:
PARTIALLY REFUTED

pattern_claim:
  id: THREE_CONSECUTIVE_UNREADABLE_AUTHORITY_REFERENCES
  status: PARTIALLY_REFUTED
  instances:
    - pr: 433
      status: DIFFERENT_DEFECT_CLASS
      finding: MAIN_COVERAGE_ASSERTS_UNMERGED_BRANCH_CONTENT
    - pr: 436
      status: NOT_VERIFIED
    - pr: 464
      status: CONFIRMED
      finding: AUTHORITY_ARTIFACT_PATHS_UNREADABLE
  conclusion: SINGLE_CONFIRMED_INSTANCE_PATTERN_NOT_ESTABLISHED
```

本次证据核查表明，原先「连续三个 PR 均存在不可读取授权引用」的模式主张不能继续作为已经证实的事实使用。

#433 已证实属于不同缺陷类别；#436 的授权引用尚未得到核实；#464 则是目前唯一得到确认的授权文件路径不可读取实例。

因此，现有证据不足以建立三个连续实例构成的模式。

归档记录的职责是准确保存证据及其边界，而不是维护先前评论的叙事一致性。此前评论中的概括性表述必须服从后来获得的实测证据。对于已被部分证伪的主张，应明确记录其修正状态，不得为了保持原有叙事而重新归类 #433，也不得为 #436 补造尚未定位的证据。

## 5. 相关发现：b9ddd241 提交信息中的事实错误

### 5.1 原始提交说明

提交 `b9ddd241` 的提交信息包含以下表述：

```text
#433 is merged and one of its rows cites a guard ... that do not exist in main.
```

其中：

```text
#433 is merged
```

与实际 PR 状态不符。

### 5.2 实际核实状态

GitHub API `/pulls/433` 返回：

```yaml
state: open
draft: false
merged: false
merged_at: null
```

因此，PR #433 在相关核查时仍处于 open 状态，尚未合并。

### 5.3 分类

```yaml
b9ddd241:
  statement: "#433 is merged"
  actual_pr_state: OPEN
  merged: false
  classification: FACTUALLY_INCORRECT_COMMIT_MESSAGE
```

### 5.4 责任与边界

本项登记仅用于纠正提交说明中的事实错误。

目前没有证据表明该错误属于有意误导。

不将这一处事实错误扩大为独立的行为违规事件，也不据此推断提交者的主观意图。

本项分类为：

`FACTUALLY_INCORRECT_COMMIT_MESSAGE`

### 5.5 影响

提交 `b9ddd241` 已进入 main 的提交历史。

因此，其中关于「#433 is merged」的错误前提会继续存在于不可追溯修改的历史提交说明中，并可能在后续引用或审计中继续传播。

本次登记用于明确纠正该错误前提，避免后续审计将该提交信息误认为 PR #433 已合并的证据。

本登记不改变提交历史，也不改变 PR #433 的实际状态。

## 6. 相关但独立的更正：PR #464 描述

PR #464 描述中存在一处 SHA 字段名称错误。

原描述将 manifest blob SHA 误写为：

`prompt_file_blob_sha`

该描述错误应予以更正。

核实后的对应关系：

| SHA | 实际对象 |
|---|---|
| `2fe294f5...` | manifest blob |
| `6eb1a1fd...` | prompt blob |

已合并 manifest 中的 `prompt_file_blob_sha` 字段本身正确。

因此：

- 需要更正的是 PR #464 描述中的错误表述。
- 不需要修改已合并 manifest。
- 不得将该描述更正扩大为修改 manifest 内容的授权。
- 不得借此改变已合并文件中的正确字段值。

该事项属于 PR 描述的事实纠正，与本文件记录的授权文件路径不可读取问题相互独立。

## 7. 禁止性声明

为防止事后归档被误用，明确以下五项禁止：

1. **禁止追溯授权。** 不得将本次归档解释为原始授权，不得将归档时间写成原始授权时间。
2. **禁止伪造完整性。** 不得将 EXCERPT 摘录称为原始文件完整副本，不得声称已证明字节等价。
3. **禁止虚构历史存在状态。** 不得声称相关文件历史上从未进入仓库；目前只能确认其在指定提交 `61a45da7` 的 tree 中不存在。
4. **禁止以内容真实性替代路径有效性。** 不得因引用内容真实而忽略路径悬空缺陷或认定其具有完整可审计性。
5. **禁止篡改缺陷分类及证据状态。** 不得将 #433 重新归类为授权文件缺失，不得将 #436 未核实的授权引用写成已证实或已排除，不得继续将「连续三个」作为已确认模式传播。

## 8. 最终归档声明

本文件记录的是基于现有材料及实测证据形成的事后归档结果。

归档保留原始材料的摘录性质、完整性限制、字节等价性限制，以及指定历史提交中的文件缺失事实。

对于 #433，确认其属于 main 分支覆盖记录引用未合并分支内容的不同缺陷类别。

对于 #436，保留授权引用未核实状态，并记录已读取的四个改动文件中未发现相关引用的实测结果。

对于 #464，确认授权文件路径在指定历史提交 `61a45da7` 中不可读取。

对于 `b9ddd241`，登记其提交说明中的合并状态事实错误，但不推断主观意图或扩大为独立行为违规事件。

对于 PR #464 描述中的 SHA 字段错误，单独记录其事实更正边界，不修改已合并 manifest 中正确的字段。

本文件不构成任何形式的原始授权补发、授权恢复或追溯批准。

**最终状态：**

`POST_HOC_ARCHIVAL — NOT RETROACTIVE AUTHORIZATION`
