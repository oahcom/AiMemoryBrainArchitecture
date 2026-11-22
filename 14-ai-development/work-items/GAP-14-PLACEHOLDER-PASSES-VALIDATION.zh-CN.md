# GAP-14 —— 会做校验的 `FactRevision` 分不清真实的 I/D 引用与占位符

**状态：** 未关闭 · **严重度：** Tier 2（当前不可达，但需关闭一个校验窗口） · **归属：** I、D
**测量点：** `b093b59f` · **关联：** ADR `OWNER-DECISION-PUBLICATION-RECORD-001`（D6）、GAP-12、GAP-13

## 1. 校验了什么，看不见什么

`FactRevision::validate`（`crates/memory-domain/src/lib.rs:956`）对于"attestor 与
canonical commit 两个引用都由公开占位工厂造出来"的 revision，返回 `Ok(())`。代码自己
在函数上方三行就写明了：

> Structural validation cannot distinguish a real I-issued attestor/authorization
> reference from public `pending_i()` placeholders, nor a D-issued commit from
> `pending_d()`. A FactRevision using placeholders can therefore validate today.
> This known temporary construction window closes only after I and D freeze their
> contracts and the placeholders are replaced with validated, non-forgeable refs.
> `Ok(())` here is not evidence of authorization or canonical acceptance.

这段注释准确，而且坦率得少见。问题不在于它写错了，而在于它只存在于源码注释里：

- 读 `validate() -> Result<(), DomainError>` 的调用方会得出"这个 revision 有效"的结论；
- `14-ai-development/` 下没有任何地方把该窗口记为未关闭缺口
  （本文之前 `grep -rln "pending_i|known temporary construction window"
  14-ai-development/` → 0 命中）；
- 两个占位工厂都是 `pub`，所以"不可伪造"目前并不成立。

## 2. 实测事实

| 主张 | 测量 |
|---|---|
| `pending_d()` 是 public | `lib.rs:548` `pub const fn pending_d()` |
| `pending_i()` 是 public | `lib.rs:523` 与 `:533`（两处 impl，都是 `pub const`） |
| 占位符能通过 `validate()` | 注释即陈述此事；`validate` 查的是"存在"，不是"出处" |
| `FactRevision` 会进到 compiler | `grep FactRevision crates/memory-compiler/` → 0 命中 |
| 占位符在测试之外被使用 | `grep pending_d() crates/` → 仅 `memory-domain` 的测试与 `phase2_acceptance.rs` |

最后两行关系到严重度：因为 `FactRevision` 从未进入 `memory-compiler`，这项目前
不可能产出 `Published`。它是一个休眠的窗口，不是活的旁路。所以定级 Tier 2 而非 Tier 1。

## 3. 为什么仍然值得记录

这是一个**校验**缺口，而校验缺口会在调用方出现的那一刻变成活的。现实中的顺序会是：
有人为了满足未来某条发布要求，把 `FactRevision` 接进 compiler，用 `validate()` 做闸门，
看到 `Ok(())`，于是上线。这条路径的每一步单独看都合理，而他真正需要的警告，写在他
没有写过的那段函数上方的注释里。

把它记下来，等于把一句注释变成一条受追踪的约束。这就是全部价值。

## 4. 修复，按顺序

1. **（I、D）** 冻结 attestor 与 canonical commit 契约，各自给出携带内容的引用类型，以及
   只有签发者能调用的构造函数。
2. **（I、D）** 把 `pending_i()` / `pending_d()` 换成一个 `NotYetIssued` 标记，让
   `validate()` 拒绝它——让临时窗口由构造关闭，而不是由注释关闭。
3. **（domain）** 让 `validate()` 对占位符失败。任何目前依赖"占位符可通过"的测试，都会
   变成"断言占位符被拒绝"的测试——这是严格更好的断言。
4. **（domain）** 要么去掉两个工厂的 `pub`，要么保留 `pub` 但让 `validate()` 拒绝其产物。
   不可伪造必须是性质，不是一句文档。

## 5. 关闭标准

1. 用任何占位引用构造的 revision，`FactRevision::validate()` 返回 `Err`；有测试证明。
2. `pending_i()` / `pending_d()` 不再存在，或从 crate 外部不可达。
3. `lib.rs:955-960` 的注释被删除，因为它所警告的条件已不存在——不是改写了事。
4. `14-ai-development` 记录关闭事实，使下一个读者不必再从注释里重新发现这个窗口。

## 6. 本文不主张什么

不主张占位符设计本身是错的。在两个归属方冻结契约之前，用一个带坦率警告的显式占位符
来解除下游阻塞，是合理的做法。本文的主张更窄：只存在于注释里的警告不是控制手段，而且
它在缺口登记册的读者会去看的任何地方都看不见。
