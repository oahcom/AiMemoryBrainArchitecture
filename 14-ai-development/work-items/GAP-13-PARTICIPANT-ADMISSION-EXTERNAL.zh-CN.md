# GAP-13 —— 参与者准入被卡在 Storage 签名与 COC quorum 之后

**状态：** 未关闭 · **严重度：** Tier 1（`Published` 的三个阻断之一） · **归属：** Storage、COC、I —— 不是 E
**测量点：** `444deef1` · **关联：** ADR `OWNER-DECISION-PUBLICATION-RECORD-001`（D3、D7）、GAP-07、GAP-12

## 1. 缺的是什么

`PublicationProof::publication_participant_admitted` 没有签发者。生产适配器把它报成
`false`（`publication_authority.rs:104`），若其余四个标志通过，
`PublicationGate::run` 随后返回 `Suppressed`（`lib.rs:540`）。

## 2. 签发者是规定好的

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:137`：

> C MUST NOT invoke a protected provider side effect until the exact participant has a
> quorum-committed `JF10_PREPARE_INTENT_REGISTERED`, a Storage-signed
> `PreparedParticipantReceipt` is durably registered as
> `JF10_PREPARED_PARTICIPANT_REGISTERED`, and the I owner-final gate has produced an
> authoritative terminal decision for the exact immutable tuple.

所以"准入"是一个由三方签发的事实，不是一次本地查表。

## 3. 实测到的缺失

| 元素 | 状态 | 测量方式 |
|---|---|---|
| Rust 中的 `JF10_*` | 不存在 | `grep -rn "JF10" --include=*.rs crates/` → 0 |
| 回执形状 | 候选 | schema 标题写明 "candidate"；描述明确放弃密码学套件、规范化、密钥策略与跨消息 owner 权威 |
| 校验器 | 无 | `protocol-index.md:55` → "no dedicated validator or production conformance claim" |
| C 侧条件 | 已规定未运行 | "C-CO-01..10 and H-JF10-01..10 remain SPECIFIED / NOT RUN" |
| Storage 签名密钥策略 | 无 | 树中没有密钥托管、轮换或校验代码 |

## 4. 为什么 E 不能自建登记表

一张存下 `PreparedParticipantReceipt` 并报告"已准入"的登记表，等于：

- 把无法校验的签名当作签名已校验；
- 把关于 quorum 的声明当作 quorum 已达成；
- 把 tuple 绑定当作 I 已作出决定。

这就是 `compiler-stage-contract.md` §8 所禁止的替代授权决定。它比 `false` 更糟：
它用调用方断言造出一个"长得像见证"的值——与 GAP-12 从 canonical commit 路径上移除的
缺陷属于同一类。

## 5. E 能做什么、不能做什么

- **不能：** 签发该标志、校验签名、确立 quorum、绑定 I 的决定。
- **能：** 保持 `false`；保持 disposition 诚实（其余四旗通过后为 `Suppressed`）；
  把该依赖写清楚，使它不被误认成 E 侧的实现缺口。

## 6. 关闭标准

1. Storage 给出 `PreparedParticipantReceipt` 的签名 profile，含密钥托管与轮换，并提供
   E 可调用的校验器。
2. COC 针对精确 participant/operation digest 暴露持久的
   `JF10_PREPARE_INTENT_REGISTERED` quorum 记录。
3. I 针对精确不可变 tuple 暴露 owner-final terminal decision。
4. 只有到那时：E 从校验器取该标志，并附一个测试——未签名或未绑定的回执若得出 `true`
   则测试失败。
5. 协议索引中 `Storage.PreparedParticipantReceipt` 一行引用 C 契约作为规范来源（D7.3）。

## 7. 关于当前索引的诚实性

`protocol-index.md:68` 写的是 "no separate normative source mapped in this scoped
audit"。这个限定是准确的——那次审计确实是限定范围的——但想找签发者的人在那里找不到。
D7.3 要求的是补上引用，不是重做审计。
