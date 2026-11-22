# 两次合并、同一个字段、相反的断言 —— 类型状态决定被应用了两次，且互不兼容

**Status:** 已由 `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` 裁决 —— 两个 PR 均未合并关闭；它暴露的残留是 `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER` §3 Step 3
**Language note:** 本文件为中文正文。凡引用裁决或决定原文处，保留英文原句并附中文释义；逐字引用不得改写，否则失去证据效力。
**Area:** memory-domain / governance
**Measured at:** `main @ 4a7624da86`，`2026-11-22T07:10Z`；裁决于 `2026-11-22T08:06:21Z` 加入
**Related:** `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`、`I-OWNER-DECISION-AUTHORIZATION-DECISION-001`、`OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025`、`GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER`、`GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER`、PR #623、PR #634、`dm2_06`

## 1. 发生了什么

两个 PR，相隔十一分钟，由两个不同会话开启，都解除 `dm2_06` 的 ignore，都重写同一个结构体上的同一个字段。它们对该字段断言**相反**的事情，并且都引用了权威文书。

| | PR #623 | PR #634 |
|---|---|---|
| 开启时间 | `2026-11-22T06:30:31Z` | `2026-11-22T06:59:28Z` |
| base | `87f54bb4` | `85504756` |
| 规模 | +522 / −44，2 文件 | +214 / −64，2 文件 |
| 字段类型 | `AuthorizationDecisionRef`（改为携带 `Pending \| Issued(data)`） | `AuthorizationDecisionState { Absent \| Placeholder \| Issued }` |
| `dm2_06` 断言 | `pending` **必须**使 `validate()` 失败，错误为 `EmptyRequiredField("authorization_decision_ref")` | `Absent` **必须失败**，`Placeholder` **必须通过** |
| 引用 | `I-OWNER-DECISION-AUTHORIZATION-DECISION-001`（#595） | `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` |

两份权威文书当时都已合并、都在树里；两个 PR 都处于开启状态且 `mergeable: true`。只可能有一个是对的。

## 2. 矛盾，用权威文书自己的话

`OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §3：

> **D3. Only `Absent` blocks publication.** `Placeholder` and `Issued` both pass the presence gate, because presence is all this gate can check. This is deliberate: the gate's job is "did someone record an authorization", not "was it real". Asserting the second is `B-P2-XO-01`'s job and I's contract.

（D3：只有 `Absent` 阻断发布。`Placeholder` 与 `Issued` 都通过存在性门，因为存在性是这个门唯一能检查的东西。这是刻意的：门的职责是「是否有人记录了授权」，不是「是否真实」。断言后者属于 `B-P2-XO-01` 与 I 的契约。）

其 §4：

> It stops being `unimplemented!()` and becomes two assertions:
> 1. `FactRevision` constructed with `Absent` authorization and `FactOutcome::Attested` fails `validate()` with a named error.
> 2. The same revision with `Placeholder` authorization validates — pinning that presence, not authenticity, is what this gate checks.
>
> The second assertion is the one that keeps the decision honest. Without it, a future reader sees only "absent is rejected" and assumes "present is verified", which is the error this decision exists to prevent.

（它不再是 `unimplemented!()`，而变成两条断言：1. 以 `Absent` 授权与 `FactOutcome::Attested` 构造的 `FactRevision` 使 `validate()` 以具名错误失败。2. 同一 revision 换成 `Placeholder` 授权则通过 —— 钉住的是存在性而非真实性。第二条才是让决定保持诚实的那条：没有它，后来的读者只看到「缺失被拒绝」，就假定「存在即已验证」，而这正是本决定要防止的错误。）

PR #623 实现的是 D3 的反面：

```rust
        if self.authorization_decision_ref.is_pending() {
            // ponytail: reuses EmptyRequiredField to avoid a new variant this round;
            // rename when the variant set is next revised.
            return Err(DomainError::EmptyRequiredField("authorization_decision_ref"));
        }
```

按这条规则，`Placeholder` —— 当时任何调用方唯一能构造的状态 —— 被拒绝。这让 `dm2_06` 通过，同时让所有用 `pending_i()` 的 `FactRevision` 构造路径失败。正因如此，#623 还必须把 `phase2_acceptance.rs` 里的 fixture 从 `pending_i()` 改写成新的 `issued_authorization(..)` 辅助函数，并把单测断言改成 `assert!(!revision.authorization_decision_ref.is_pending())`。

所以 #623 不是同一决定的另一种实现。它是一个**更严的门**，拒绝占位符，并且只能靠在测试 fixture 里先伪造 issued 引用才让自己的套件通过。

## 3. 裁决，以及为什么它是读法而不是选择

`OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025`（合并为 `c9036544`）解决了这一点。其 §1：

> `Placeholder` satisfies the presence gate. `FactRevision::validate()` MUST reject `Absent` and MUST NOT reject `Placeholder`. `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §4.3 does not require otherwise: it requires `dm2_06` to assert a propagated authority `Err`, and that error is produced by the `AdmissionStore`-backed validator of §4.1, not by `FactRevision::validate()`. `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D3 is correct as written. Neither open PR may merge as written: #634 on a measurable regression, #623 on crate-boundary scope.

（`Placeholder` 满足存在性门。`FactRevision::validate()` 必须拒绝 `Absent`，且不得拒绝 `Placeholder`。`I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §4.3 并无相反要求：它要求 `dm2_06` 断言一个**被传播的权威 `Err`**，而该错误由 §4.1 的 `AdmissionStore` 校验器产生，不是由 `FactRevision::validate()` 产生。`OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D3 按原样正确。两个开放 PR 都不能按原样合并：#634 因一项可测量的回归，#623 因 crate 边界越界。）

它没有推翻任何决定。它读的是 `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.3 —— 那不是裁决会话自己的文书，而且它自己就能解决这个问题：

> The validator is **not** a `FactRevision::validate()` responsibility. Domain validation may validate candidate field syntax and reject Pending, but only the compiler's AdmissionStore-backed validator can establish durable existence and authority. Structural validation must not claim a candidate reference is issued.

（校验器**不是** `FactRevision::validate()` 的职责。领域校验可以校验候选字段语法并拒绝 Pending，但只有编译器的、以 AdmissionStore 为后端的校验器才能确立持久存在性与权威。结构校验不得声称某个候选引用已被签发。）

决定性的一步是裁决 §2：

> `FactRevision::validate()` returning `Err` is not the propagated authority error. It is a *second, earlier, unrelated* error of the same shape. Asserting it satisfies the letter of "assert an `Err`" while destroying the distinction §4.3 exists to protect — and §3.3 forbids it in the same document, in the sentence immediately before the validator is introduced.

（`FactRevision::validate()` 返回 `Err` 并不是被传播的权威错误。它是**同一形状的第二个、更早的、无关的**错误。断言它满足了「断言一个 `Err`」的字面要求，却摧毁了 §4.3 存在的意义；而同一份文件在引入校验器的上一句就禁止了它。）

所以两份权威从未矛盾。**是 #623 误读了 #595。** 本文 §1 曾把矛盾表述为「占位符是否满足存在性门？#595 从没说」—— 就所提的问题而言这是真的，就所需的答案而言是假的：#595 不必说，因为它把拒绝放在了完全不同的地方，而且说了两遍。

本文早先草稿的 §4 用「specificity（更具体者优先）」来裁断。该论证已被取代并删除：它不需要，它是裁决明确拒绝依赖的那类读法，而且它碰巧以错误的理由得出了正确的答案。

## 4. #634 另因一项独立的、可测量的回归被拒绝

与上述读法无关，#634 还带着一项回归。此处以 blob SHA 核实，而非 `contents?ref=`（#612 审计发现后者可能返回陈旧正文）。

在 #634 自己的 base `85504756b8`：

| 事实 | 值 |
|---|---|
| `lib.rs` 中 `mod canonical_commit;` 存在 | **True** |
| `lib.rs` 中 `pub use canonical_commit::*;` 存在 | **True** |
| `lib.rs` 中 `pub struct CanonicalCommitRef(())` 存在 | **False** |
| `tests/phase2_acceptance.rs` 中 `dm2_15` 测试存在 | **True** |

在 #634 的 head `d55f4996ca`：

| 事实 | 值 |
|---|---|
| `lib.rs` 中 `mod canonical_commit;` 存在 | **False** |
| `lib.rs` 中 `pub use canonical_commit::*;` 存在 | **False** |
| `lib.rs` 中 `pub struct CanonicalCommitRef(())` 存在 | **True** |
| `tests/phase2_acceptance.rs` 中 `dm2_15` 测试存在 | **False** |

`CanonicalCommitRef` 是 `D-OWNER-DECISION-CANONICAL-COMMIT-001` 的标的。在 `main` 上它是带私有状态 `CanonicalCommitRefState { Pending | Issued(data) }` 的有内容类型，定义于 `crates/memory-domain/src/canonical_commit.rs`。#634 把它换成了 unit struct，并停止了该模块的编译。`dm2_15_legacy_pending_canonical_commit_keeps_its_unit_representation` —— 那条钉住 legacy `null` wire 形态、援引该决定 §5 与 §8 准则 3 的回归测试 —— 被删除。

用裁决的话说：

> That is not a difference of opinion about authorization. It reverts a merged decision about canonical commit, in a PR about `dm2_06`, and it deletes the test that would have caught it.

（这不是关于授权的意见分歧。它在一个关于 `dm2_06` 的 PR 里回退了一项关于 canonical commit 的已合并决定，并删掉了本该抓住它的那条测试。）

## 5. 处置

- **PR #634** 于 `2026-11-22T08:13:06Z` 未合并关闭。它的授权层是正确的；阻断它的是那项回归。
- **PR #623** 于 `2026-11-22T08:14:06Z` 未合并关闭。它的 crate 边界错了：它把门放进了 `memory-domain`，而该 crate 只有一个依赖（`serde`），无法承载以 `AdmissionStore` 为后端的校验器。
- **本文（PR #640）** 于 `2026-11-22T08:13:30Z` 合并，早于裁决落地。裁决 §6 说它「应当合并：其测量正确，其拒绝裁决是正确的做法。其 §4 的『specificity』读法被上文 §2 取代。」

本次修订做的正是这件事：§3 现在承载裁决而非 specificity 论证，§4 记录裁决所测量的那项回归。§1、§2 与 §4 的测量内容未变，因为它们本来就是对的。

本次修订也说明裁决剩余要求目前的落点。`GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER` §3 Step 3 就是那项要求，且尚未满足：`dm2_06` 在 `memory-domain` 里证明的是存在性，而 `crates/memory-compiler/tests/` 中没有任何测试断言被传播的权威 `Err`。本文不复述那份工作单；它只记录裁决 §5 第 4 步仍未闭合，以免读者看完上文 §3 就以为裁决已经把它关掉了。

## 6. 裁决刻意没有决定的事

- `Placeholder` 最终是否应在发布时被拒绝。那是 `B-P2-XO-01`，仍为 `PENDING CROSS-OWNER DECISION`。
- 任何 `Issued` 值的真实性。同一 owner，同一理由。
- `CanonicalCommitRef` 回归的成因。裁决将其记为一个 rebase 问题，而不是一个决定。

## 7. 权威与独立性披露

§1–§2 与 §4 的测量是我的。我写了 PR #634，这使我没有资格裁决其是非，我也没有裁决 —— 那次拒绝正是裁决唯一称赞为正确的做法。

`OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` 不是我写的，我也不是其作者的代理人。我在这里记录的是：它存在、它说了什么、以及它取代了本文早先草稿的 §4。若将来的变更与该裁决冲突，正确做法是提出新的 Owner 裁决，而不是修改本文。
