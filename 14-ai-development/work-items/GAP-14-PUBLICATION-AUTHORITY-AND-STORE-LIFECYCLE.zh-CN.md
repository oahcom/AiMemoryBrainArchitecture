# GAP-14 · 生产发布权威与 MemoryStore 发布生命周期

**状态**：未关闭 — A 开放、B 受阻于 D3、C 未验证
**领域**：memory-store / memory-compiler / memory-storage-sqlite
**归属线**：Owner D（发布）+ Owner I（授权）
**拆分自**：GAP-07，2026-11-22 仅就生产可达性关闭
**测量基线**：`main @ 87d503ba`

## 为何拆成三项而非一项

GAP-07 只问了一个问题——*编译器能否从生产路径被调用？*——答案现在是能。那次关闭刻意没有吸收另外三个一直挤在它里面的问题，因为把它们揉成一团会让三者同时无法回答：

- 发布生命周期能否经由 CLI 实际使用的门面触达？（**A**）
- 三个授权标志中是否有任何一个能变成真？（**B**）
- 发布记录能否跨进程重启存活？（**C**）

它们有不同的归属方、不同的阻塞源、不同的取证要求。合并成一行"发布尚不完整"，会把"B 是没人做的决策"和"A 是几个转发方法"这两件性质完全不同的事藏起来。

## GAP-14-A — `MemoryStore` 未暴露发布生命周期

**状态**：开放 — 无需外部决策

`crates/memory-store/src/lib.rs`（1175 行）暴露十个 `pub fn`：

```
new, into_storage, create_memory, read_current, read_memory,
read_revision, write_revision, resolve_idempotency,
forget_memory, forget_version
```

`prepare_version`、`publish_prepared`、`publication_state` 在该文件中只出现在 `FakeStorage` 上，位于 `#[cfg(test)]` 模块内：

```
:317  fn publication_state       (FakeStorage)
:426  fn prepare_version         (FakeStorage)
:524  fn publish_prepared        (FakeStorage)
```

真实实现在下一层，`crates/memory-storage-sqlite/src/lib.rs`：

```
:388  fn publication_state
:606  fn prepare_version
:822  fn publish_prepared
```

也就是说：原语存在于任何调用方都够不到的地方，而唯一够得到的那一层没有暴露它。这与 GAP-07 原始缺陷是同一形状，只是低了一层。

**为何不是简单三个转发方法。** 三者各自带着契约，而不只是签名：

1. `PrepareRequest` / `PreparedCommitReceipt` —— "已暂存但不可读"到底指什么，哪些字段必须原样保留。
2. `publish_prepared(publication_id, expected_current_version, scope)` —— `expected_current_version` 是并发栅栏而非提示；传错会把"陈旧版本冲突"变成"静默覆盖"。
3. `publication_state` —— 它的答案对存储层之外的调用方是权威的，还是仅是一个局部观察。

**关闭标准**

1. 三个方法出现在 `MemoryStore<S: MemoryStorage>` 上，语义与 trait 一致，每次调用都走 `validate_scope`。
2. 至少一个测试通过 `MemoryStore` 驱动 `prepare_version` → `publication_state == PreparedHidden` → `publish_prepared`，且跑在真实 SQLite 上，不是 `FakeStorage`。
3. 一个测试证明陈旧的 `expected_current_version` 经门面被拒绝，而不是被静默接受。
4. 不引入新抽象：不新增第二个 trait、不新增 builder、不新增策略对象。三个方法及其测试。

**不得抢在 GAP-14-B 之前实现。** 在没有任何权威能够合法授权发布的情况下把 `publish_prepared` 暴露到门面上，会产出一个"可调用但没有完整授权契约"的 API——正是 GAP-07 警告过的不可达抽象那一类。2026-11-22 裁决因此把 B 排在 A 之前。

## GAP-14-B — 三个发布标志没有权威签发者

**状态**：受阻 — 需要 D3 决策

`PublicationProof` 携带八个标志。`brain-cli` 按闸门求值顺序报告为假的那几个：

```
canonical_commit_confirmed
publication_participant_admitted
protected_visibility_authorized
```

在 `main @ 87d503ba` 上实测，这三个在每一次真实运行中均为假，因此处置永远是 `Blocked`：

```
$ brain compile --input crates/brain-cli/fixtures/event.json --out /tmp/o.json
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed;
false flags: [canonical_commit_confirmed, publication_participant_admitted, protected_visibility_authorized]
```

`OWNER-DECISION-PUBLICATION-RECORD-001` D3 记载这三个标志没有权威签发者。代码对此是诚实的——`crates/brain-cli/src/main.rs:111` 的文档注释明说 `Blocked` 是真实运行的预期结果——但后果是 `Published` 处置在生产路径上当前不可达。

**关闭此项需要什么**

不是代码，而是三个答案：

1. 谁签发 `canonical_commit_confirmed`，依据哪份持久记录？
2. 谁准入发布参与者，按什么标准？
3. 谁授权受保护可见性，该授权可否委托？

**明确拒绝的做法**：给任何请求加 `authorized: bool`、从本地状态推导出标志、或让测试权威在生产构建里满足闸门。这三种做法都把一项未回答的治理问题转换成一个虚假的授权宣称。

## GAP-14-C — 发布记录的持久性未经验证

**状态**：未验证 — 无证据不得标记为已解决

`crates/brain-cli/src/main.rs:244` 按路径打开准入账本：

```rust
let authority_admission = AdmissionStore::open(request.admission_path)
```

这一行证明打开了一个文件路径。它**不**证明：

- 发布记录以能跨进程退出的形式被持久化；
- 重新打开同一路径能取回同一条记录；
- 取回的记录具备 D3 所要求的权威性；
- 取回的记录能够确认一次 canonical commit。

以上均未测试。本评估的早期草稿曾准备仅凭"文件路径"这一论据就把持久性称作"疑似已解决"；该推断不成立，此处记录它作为本项保持开放的理由。

**关闭标准**

1. 一个测试写入发布记录、退出进程、在新进程中重新打开同一路径、并读回同一条记录。
2. 一个测试证明"已准备但从未发布"的记录在重启后仍可与"已发布"记录区分。
3. 测试跑在真实落盘存储上，不是内存句柄。

## 顺序

```
GAP-14-B  （决策 — 谁签发那三个标志）
    |
    v
GAP-14-A  （门面 — 三个方法按已确定的契约设计）
    |
    v
GAP-14-C  （持久性 — 对真实存储验证恢复）
    |
    v
重新评估 Published 在生产路径上是否可达
```

先做 A 会产出一个背后没有权威的可调用发布 API。先做 C 会验证一条权威尚未定义的记录的恢复。B 排第一，因为它是三者中唯一一个"决策"而非"工作"。

## 本项不是什么

- 不是对 #552 的缺陷报告。那个 PR 做到了它宣称的事：让编译器可达，并对拒绝保持诚实。
- 不是"发布坏了"的宣称。它没坏；它按设计处于未授权状态，等 D3。
- 不是对 D3 的重新审理。本项记录 D3 的后果，不构成对 D3 的反对意见。
