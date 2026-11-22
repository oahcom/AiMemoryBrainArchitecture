---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: 14-ai-development/governance-register/GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024.md
---

# GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024 —— PR #623 与 PR #634 之间的授权门矛盾

**状态：** 已裁决（RESOLVED）—— 历史冲突记录。本文记录在过去某个测量点上确实存在的一处矛盾，以及将其关闭的 Owner 裁决。它不再是一份待答问题清单，本身也不作出任何裁决。

- **测量点：** `main` = `f34d96a92975bb4e42e8b3121e345963ea4b7ab2`
- **登记时间：** 由 PR #640 记录，早于 `2026-11-22T07:30:33Z`；Owner 裁决在其后约八分钟作出。
- **作者身份：** 由承担本文书写的协调会话完成。该会话**不是** #623 或 #634 的独立审查者，也**不是**任何一项变更的 accountable owner。
- **裁决出处：**
  - Issue #347 评论 `7075955802`，`2026-11-22T07:30:33Z`
  - Issue #595 评论 `7076098820`，`2026-11-22T07:45:02Z`（正式的 Owner scope amendment）
- **已被取代的表述：** 本登记早期版本把三个问题列为「只有 Owner 能回答」，并明确表示不予裁决。这些问题已有答案；第 3 节记录该答案，第 5 节记录本文不涉及的范围。

---

## 1. 本文是什么

本文是一份**历史冲突记录**。它出于审计目的，完整保留了两个未合并 PR 在同一份契约中引入的语义矛盾的原始形态，以及解决该矛盾的裁决和由裁决产生的后果。

它被保留而非删除，原因是这处矛盾对工具链不可见：两个 PR 对各自 base 都能干净合并，CI 与合并冲突都没有把它暴露出来。将来在历史中遇到 #623 与 #634、或重新推导同一套三态授权模型的人，需要看到为什么这两种主张不能同时成立，以及 Owner 选择了哪一种。

本文为 Informative（说明性）且 Non-Canonical（非规范）。具有约束力的文本是上文与第 3 节所引的 Owner 裁决；若本文与裁决不一致，以裁决为准。

## 2. 当时的冲突形态

两个 PR 都改动了同一个字段 `FactRevision::authorization_decision_ref` 的语义，并就它主张互斥的不变量。

| 方面 | PR #623 | PR #634 |
| --- | --- | --- |
| 开启时间 | `2026-11-22T06:30:31Z` | `2026-11-22T06:59:28Z` |
| 登记时的 base commit | `87f54bb4` | `85504756` |
| 登记时的规模（文件数 / 行数） | 2 文件，+522 / −44 | 2 文件，+214 / −64 |
| `authorization_decision_ref` 的字段类型 | 在存在性层拒绝：pending 引用被视为不可采纳，`Placeholder` 无法通过 `FactRevision::validate()` | 三态存在性门：`Absent` / `Placeholder` / `Issued`，`Placeholder` 可通过 `FactRevision::validate()` |
| `dm2_06` 断言 | `Pending` → `Err` | 在存在性层断言 `Absent` 与 `Placeholder` 的行为 |
| 引用依据 | 更早的 I 决定 §4.3 与 §6.4 | `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4 |

上表数字是**登记时刻**的取值，因为本文描述的正是那一时刻。两个 PR 其后均已 rebase 且仍未合并，其当前 base 与规模已与这些单元格不同；本文不复述实时值，因为一份记录过去冲突的文档不应悄悄跟随变动的输入。当前值请直接查阅两个 PR。

frontmatter 中 `verification_status: Unverified` 的原因是：裁决文本尚未针对两份被引决定的后续修订再核对。

### 2.1 保留引文 —— 更早的 I 决定

更早的 I 决定中有两处片段对这场冲突具有支撑作用，因为 #623 引用了它们：

- §4.3：`dm2_06` must test `Pending` → `Err`.
- §6.4：structured `FactRevision::validate()` rejects pending evidence.

以上片段按它们被带入冲突时的原样保留。更早的 I 决定的上下文**不**在本文全文复述；它以引用方式保留，其操作性解读现由 `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4 管辖，详见第 3 节。

### 2.2 从冲突中带来的片段 —— #623 的存在性层谓词

```rust
// 逐字取自 PR #623 的 `FactRevision::validate()`，如被取代的登记所载。
if self.authorization_decision_ref.is_pending() {
    // ponytail: reuses EmptyRequiredField to avoid a new variant this round;
    // rename when the variant set is next revised.
    return Err(DomainError::EmptyRequiredField("authorization_decision_ref"));
}
```

引用该谓词仅用于说明 #623 是通过什么机制把「尚未签发」塌缩为「不可采纳」。它不具规范性，也不代表本文认可该做法。

### 2.3 为什么这不是合并冲突

1. 两个 PR 触及同一份契约的不同区域，因此 git 合并两者时没有产生文本冲突。
2. 分歧是语义层面的，不是文本层面的：争点是该字段应当维护哪一条不变量，而不是哪些行能留下来。
3. 因此两条分支都能以绿色状态合并，无论先后，却仍会让仓库对同一个字段保留两种互斥解读。
4. 当前流水线中没有任何 CI 作业、linter 或审查机器人跨开放 PR 比对不变量，因此没有任何机制自动暴露这处矛盾。它是通过把两份 diff 相互对照阅读才被发现的。

## 3. 裁决

Owner 裁决记录于 Issue #347 评论 `7075955802`（`2026-11-22T07:30:33Z`），并在 Issue #595 评论 `7076098820`（`2026-11-22T07:45:02Z`）作为正式 scope amendment 重述。操作性要点，逐字引用：

> The later `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` (§§3–4) is the **controlling refinement** of the earlier I decision's use of `dm2_06`.

（中文释义：更晚的 `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4 是更早 I 决定中 `dm2_06` 用法的**支配性细化**。）

此前被混为一谈的两个问题必须分开：

1. **存在性（domain invariant，领域不变量）。** `FactRevision.authorization_decision_state` 区分 `Absent` / `Placeholder` / `Issued`。`FactRevision::validate()` 仅在 `outcome == Attested` 时拒绝 `Absent`；`Placeholder` 可以通过。
2. **真实性与持久权威（I validator）。** `AuthorizationDecisionRef::Pending` 不构成权威。由 AdmissionStore 支撑的 `validate_authorization_decision()` 必须对 Pending、缺行、畸形行、不匹配引用一律返回 `Err`；`validate_attestor()` 必须独立拒绝 pending、缺失或损坏的 attestor 证据。只有匹配的持久记录且 `decision_kind == Approved`，才能满足无条件授权要求。

裁决产生的后果（引自或紧贴上述两条评论转述）：

- 更早 I 决定 §4.3 中「`dm2_06` 必须测 `Pending` → `Err`」的要求**保留**，但**改归**为一个独立的 I validator 测试，例如 `authorization_validator_rejects_pending_reference` 或 `validate_authorization_decision_rejects_pending_reference`。它不再是 `dm2_06` 的语义。
- §6.4 的表述被**收窄**：pending 证据由 I publication-authority validator 在成功发布前拒绝，而不是由仅做存在性检查的 `FactRevision::validate()` 拒绝。
- `#634 must preserve the three-state presence gate and dm2_06 absent/placeholder assertions.`（#634 必须保留三态存在性门，以及 `dm2_06` 的 absent/placeholder 断言。）
- `#623 must not make FactRevision::validate() reject Placeholder.`（#623 不得让 `FactRevision::validate()` 拒绝 `Placeholder`。）
- 不引入第四个状态。状态集合仍为 `Absent` / `Placeholder` / `Issued`。
- 该裁决不授予生产密码学权威。dev-baseline `i-owner-proxy/dev-baseline-v1` 仍是逻辑信任锚；生产签名与密钥托管仍属 OUT-OF-SCOPE。

一句话概括：**存在性是由领域类型回答的三态问题；权威是由 validator 回答的持久性问题。** #623 把第二个问题拿到第一个问题的层面上作答；#634 保持了两层分离。Owner 维持了这一分离。

## 4. 由此产生的变化

- **PR #634** 必须保留三态存在性门以及 `dm2_06` 的 absent/placeholder 断言。其存在性层按原样成立。
- **PR #623** 不得让 `FactRevision::validate()` 拒绝 `Placeholder`。它在存在性层对 pending 引用的拒绝，不能作为领域不变量被采纳；它想要的拒绝应归入 I validator。
- **新增测试义务：** 必须有一个独立的 I validator 测试断言 `Pending` → `Err`（命名示例见第 3 节）。这是更早 I 决定 §4.3 要求的存续归属。
- **`dm2_06`** 不再承载 pending 拒绝语义。它只断言存在性行为：在 `outcome` 非 `Attested` 时的 `Absent`，以及 `Placeholder` 通过校验。
- **本登记**从待答问题清单重新定性为已裁决的历史记录（即本文）。

## 5. 本文不裁决什么

- 它**不**裁决 #623 或 #634 能否合并、以何顺序合并、在何种审查条件下合并。合并处置权属于 Owner，本文不予记录。
- 它**不**构成对任一 PR 的独立审查。产出本文的会话是协调会话，见第 6 节。
- 它**不**授予生产密码学权威，也不改变生产签名与密钥托管的 OUT-OF-SCOPE 状态。
- 它**不**重新开启该裁决。若将来的变更与 `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4 冲突，正确做法是提出新的 Owner 决定，而不是修改本文。
- 它**不**主张 #623 与 #634 的**当前**开启日期、规模或 base commit。第 2 节的单元格是登记时刻的取值；两条分支其后均已 rebase。

## 6. 权威与独立性披露

本文由一个协调会话撰写。适用的披露义务如下，本文选择直接陈述而不是绕开：

- **Owner 角色可由同一会话持有。** 依据 #305 §2（委托文书 `7042461592`），Owner 角色并不绑定到某个独立会话；撰写某项变更的会话，也可以对该变更作出 Owner 处置。
- **但该处置不得表述为独立审查。** 依据 #305 §4，代表不得成为自己实现的唯一审查者，也不得把该审查表述为独立审查。这是一项**披露义务，不是合并禁令**：无法确立独立性时，正确做法是记录 `INDEPENDENCE_UNVERIFIABLE` 并继续，而不是停工。
- **因此本文作者不主张任何独立性。** 作者不是 #623 或 #634 的 accountable owner，也不主张对任一者做过独立审查。上文引用裁决之处，是作为 Owner 的文本引用，而不是作为作者的判断。
- **提示词配对独立性未经验证。** 治理基线要求独立性由**不同会话且不同提示词**确立。GitHub 作者不同，不足以证明其中任何一项。产出 #623 与 #634 的会话标识、以及提示词版本或哈希，本文**均未记录**；早期版本中「两个 PR 由两个不同会话撰写」的说法因缺乏支撑而撤回。状态：`INDEPENDENCE_UNVERIFIABLE` —— prompt-pair independence not verified（提示词配对独立性未验证）。
- **补齐方式：** 分别记录 #623 与 #634 的会话标识与提示词版本或哈希，使会话互异与提示词互异可被检查而非假定。

---

仅文档变更，本文不修改任何源代码。
