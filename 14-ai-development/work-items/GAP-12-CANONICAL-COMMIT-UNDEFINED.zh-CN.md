# GAP-12 —— compiler 断言了一个它自己的 domain 拒绝定义的 canonical commit

**状态：** 未关闭 · **严重度：** Tier 1（阻断 `Published`） · **归属：** D（契约）、E（停止断言）
**测量点：** `444deef1` · **关联：** ADR `OWNER-DECISION-PUBLICATION-RECORD-001`（D3、D6）、GAP-07、#552

## 1. 一句话

`MemoryCompiler::compile` 少了调用方提供的游标就不往下走，随即把它记成
`canonical_commit_confirmed = true`，然后把"该标志为 false"作为理由交给发布 gate
去阻塞——而 domain 声明这个标志背后的契约根本没有定义。

## 2. 四处读取

| # | 位置 | 内容 |
|---|---|---|
| 1 | `crates/memory-compiler/src/lib.rs:633` | `if producer_request.admission_canonical_commit_cursor.is_none()` |
| 2 | `crates/memory-compiler/src/lib.rs:634` | `return Err(CompilerError::MissingCanonicalCommit);` |
| 3 | `crates/memory-compiler/src/lib.rs:641` | `staging.canonical_commit_confirmed = true;` |
| 4 | `crates/memory-compiler/src/publication_authority.rs:103` | `canonical_commit_confirmed: false,` |

第 4 项被送进 `PublicationGate::run`，其 `lib.rs:531` 的检查
（`!proof.canonical_commit_confirmed`）产出 `PublicationDisposition::Blocked`。

在 `#552` 上端到端实测，退出码 0：

```
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed;
false flags: [canonical_commit_confirmed, publication_participant_admitted, protected_visibility_authorized]
```

## 3. 为什么这不只是"某个标志没有生产者"

`admission_canonical_commit_cursor` 是 `ProducerRegistrationRequest` 的字段
（`crates/memory-compiler/src/admission.rs:127-137`），由调用方提供。账本存下它、
原样返回它。没有任何东西校验它。

也**无法**校验，因为 domain 明确声明目标契约不存在
（`crates/memory-domain/src/lib.rs:489-500`）：

```rust
/// NOT DEFINED: awaiting D. Required placeholder with no invented commit semantics.
/// `pending_d()` is public and any caller can create this placeholder. It has no
/// canonical-commit meaning until D freezes that contract.
pub struct CanonicalCommitRef(());
impl CanonicalCommitRef { pub const fn pending_d() -> Self { Self(()) } }
```

`CanonicalCommitRef` 装的是 `()`。它没有内容，也没有任何携带证据的构造函数；
`pending_d()` 是一个为无意义值开的公共工厂，而且已经被穿进 `ClaimRevision` 的字段
（`lib.rs:775,793,829,865`）。

因此：

- 该标志不可能是诚实的 `true`——没有提交、没有提交记录、也没有能命名它的引用类型；
- 适配器给的 `false` 不是保守，而是唯一真实的取值；
- 第 641 行的赋值构成 `compiler-stage-contract.md` §8 所禁止的替代授权决定。

## 4. 使它成为 Tier 1 的那个性质

第 2 项是**硬报错**，不是 disposition。也就是说，发布 gate 只有在调用方断言了游标时
才可达。gate 的全部可达性，依赖于它随后会拒绝的那个断言。

这就是为什么"把适配器改成 `true`"不是修复、且必须拒绝：它会把一条未校验的调用方
声明转换成 `Published`，而这正是 D2 存在的理由。

## 5. 修复，按依赖顺序

1. **（E，小，行为不变）** D6.2 —— 把 staging 的前置条件改名为
   `canonical_commit_cursor_recorded`；gate 标志仍为 `false`；所有 disposition 逐字节
   不变。消除矛盾而不改变输出。
2. **（D，阻塞）** 冻结 canonical commit 契约：携带内容的引用类型、持久记录、校验器。
   在此之前不可能有生产者，也不应模拟。
3. **（E，待 2 完成后）** 从该校验器取 `canonical_commit_confirmed`，并停止把游标当作
   证据（D6.3）。
4. **（D，阻塞，独立）** 发布参与者登记表，使 `publication_participant_admitted` 有签发者。
5. **（I，阻塞，独立）** 受保护可见性授权，使 `protected_visibility_authorized` 有签发者。

第 2、4、5 步的归属在 E 之外。第 1 步是今天唯一能落地的。

## 6. 关闭标准

1. `crates/memory-compiler` 中不再有任何一行把调用方提供的
   `admission_canonical_commit_cursor` 称作对任何事物的确认。
2. `StagingInput` 不再有名为 `canonical_commit_confirmed` 的字段；它携带的布尔量以
   它真正检查的那条记录命名。
3. 存在一个测试：若仅凭调用方提供的游标就能让任何 `PublicationProof` 的
   `canonical_commit_confirmed == true`，该测试失败。
4. `CanonicalCommitRef::pending_d()` 不出现在任何喂给 `PublicationGate` 的路径上。
5. `compile()` 仍返回 `Ok(Blocked)` 并点名该标志，`brain-cli` 仍以 0 退出——关闭动作
   不得改变可观察的 disposition。
6. 第 2/4/5 步连同归属方被记录为未完成项；GAP-12 不因第 1 步单独关闭。

## 7. 本文不主张什么

本文不主张 `AdmissionStore` 存下游标是错的。存储一条未校验的声明，只要标明它是声明，
是可以成立的。缺陷在于 compiler 把它读回来当成了裁决。
