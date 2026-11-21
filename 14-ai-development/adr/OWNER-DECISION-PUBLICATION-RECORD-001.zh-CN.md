# OWNER-DECISION-PUBLICATION-RECORD-001 —— 持久发布记录是什么

**状态：** 已决（owner 代理决策，2026-11-22）
**决策者：** Verifier，以 owner 代理身份。依据是常设指令：当阻塞性决定没有人类可
裁决时，应当作出并记录，而不是留在开放状态。
**效力：** 解锁 GAP-07 Tier-1 第 1 项。本身不授予发布权。
**取代：** 无。编译阶段契约与既有 ADR 都没有点名这份记录 —— 这正是该项被阻塞的原因。

## 阻塞的那个问题

GAP-07 与 GAP-10 都终止于同一句话：编译阶段不可达，因为 `PublicationAuthority`
没有生产实现，而实现它需要先回答 *持久发布记录是什么*。没有人回答过，于是三个领域
（compiler、context、agent-integration）一起卡在一个未命名的决定后面。

这个框架有一处是错的，而纠正这一点就是本决定的大半内容。

## 发现 1 —— 记录已经存在，且在生产代码里

`crates/memory-compiler/src/admission.rs` **不是**测试模块。它在 `lib.rs:6` 声明为
`pub mod admission;`，共 1388 行，唯一的 `#[cfg(test)]` 在第 977 行，并以 SQLite
为后端，含五张表：

```
admission_meta(  singleton, fence_generation, protocol_sequence )
producer_registry( producer_id, registered_at, registry_digest )
producer_work(  work_item_id, ... )
dependency_edges( artifact_ref, artifact_version, receipt_json, ... )
publication_receipts( publication_id, artifact_ref, artifact_version,
                      request_digest, receipt_json )
```

`admission.rs:261-292`。

`AdmissionStore::final_publication_gate`（`admission.rs:738`）已在一个 `IMMEDIATE`
事务内完成：

1. 以 `publication_operation_id` + `request_digest` 做幂等，重放返回已存回执，
   digest 不匹配返回 `IdempotencyConflict`；
2. 对 `admission_meta` 做 `StaleFence` / `StaleProtocol` 比较交换；
3. producer-work 存在性检查；
4. 依赖闭包完整性（`dependency_receipt_ids` 必须与已存集合完全相等，排序后比较，
   否则 `ReceiptMismatch`）；
5. 一份持久的 `PublicationReceipt`，绑定 artifact ref、artifact version、
   `fence_generation`、`permission_epoch`、`protocol_sequence` 与 `visible`；
6. 单调推进 `protocol_sequence`。

那就是一份持久发布记录。它不是授权机构，但记录并不缺。

**所以这个决定不是"发明一份记录"，而是"指定这一份"。**

## 发现 2 —— 八个证明标志中六个有来源，两个没有

`PublicationProof`（`lib.rs:285-294`）携带八个字段。逐个追踪其在
`memory-compiler/src/lib.rs` 之外的生产者：

| 证明字段 | 生产来源 | 位置 |
|---|---|---|
| `producer_admitted` | **有** | `AdmissionStore::is_producer_registered` / `producer_work` 行，`admission.rs:449,461` |
| `dependency_closure_complete` | **有** | `AdmissionStore::dependencies_complete`，`admission.rs:655` |
| `canonical_commit_confirmed` | **无** | 全树无生产者；`admission_canonical_commit_cursor: Option<OpaqueId>` 只作为请求字段存在，且所有构造处均为 `None` |
| `storage_prepared_hidden` | **部分** | 状态存在（`publication_preparations.state='PreparedHidden'`，`memory-storage-sqlite/src/lib.rs:111,699`），但没有任何 `MemoryStorage` trait 方法暴露它；`prepare_version` 返回的 `PreparedCommitReceipt` 不含状态 |
| `publication_participant_admitted` | **无** | `lib.rs` 之外零出现；无注册表、无请求类型 |
| `protected_visibility_authorized` | **无** | `lib.rs` 之外零出现；无策略输入、无表 |

测量命令：

```sh
for f in producer_admitted dependency_closure_complete canonical_commit_confirmed \
         storage_prepared_hidden publication_participant_admitted \
         protected_visibility_authorized; do
  grep -rln "$f" crates/ --include=*.rs | grep -v "memory-compiler/src/lib.rs"
done
```

六个里有四个返回空。其中两个（`canonical_commit_confirmed`、
`protected_visibility_authorized`）连表、请求类型、以及"由谁签发"的规范句子都没有。

## 发现 3 —— 规范禁止 compiler 自行发明缺失的那几个

`docs/en/04-memory-compiler/compiler-stage-contract.md` §8 按操作列出所需权限。对
两个无来源标志，它写的是：

| Operation | Required authority | E authority |
|---|---|---|
| PublicationParticipant Admission | D authoritative Fence/Admission | Invoke and preserve exact evidence |
| Protected visibility advancement | Storage and applicable D/I authorization | **No independent authority** |

紧接着一句：

> E MUST NOT implement substitute authorization decisions.

所以那个诱人的实现 —— 一个 `AdmissionAuthority`，读 `final_publication_gate`，用它
填六个可用标志，另两个硬编码为 `true` —— 是**不合规**的，而且它正是三个测试专用
authority 已经在做的事（`lib.rs:926,945,1335`；各自硬编码
`dependency_closure_complete: true, canonical_commit_confirmed: true` 之类）。把这个
形状抄进生产，等于把可见缺口换成不可见的假授权，比现在的跳过通知严格更糟。

## 决定

**D1. 持久发布记录 = `AdmissionStore::final_publication_gate` 写入的
`publication_receipts` 行，与同一 publication 身份下 storage
`publication_preparations` 状态为 `PreparedHidden` 的行之联合。** 二者都已存在。
不得复制或重新实现其中任何一个。

**D2. 生产用 `PublicationAuthority` 必须是适配器，不是决策者。** 它只能转述这两份
记录说了什么。八个标志中的任何一个都不得被计算、推断、默认或硬编码。

**D3. 三个来源不足的标志（`publication_participant_admitted`、
`protected_visibility_authorized` 无来源；`canonical_commit_confirmed` 无生产者）
在权威签发方存在之前，生产适配器必须报 `false`。** 由于 `PublicationGate::run`
（`lib.rs:544-562`）把 `false` 映射为 `Blocked`，直接后果是：

```
compile() 变为可达，并返回 Ok(Blocked)，处置得以保留。
它不返回 Published，也不得假装返回。
```

**D4. `storage_prepared_hidden` 必须有来源**，做法是在 storage 端口加一个读方法
（`MemoryStorage::publication_state(publication_id) -> Option<PublicationState>`
或等价物），因为该状态已经持久化，不暴露它只会逼出一个事实错误的 `false`。这是本
决定授权的唯一新增生产 API。

**D5. GAP-07 建议 (b) 维持 #538 的实现。** 在 D3 的 blocked 路径取代它之前，跳过
通知继续打印，且两者不得同时静默。

## 为什么这优于其他选项

- **相比继续悬空：** 三个领域会继续卡在一个未命名的问题后。问题现在被命名并回答了，
  而答案本来就在树里 —— 只是从没有人指向它。
- **相比让 authority 把两个标志硬编码成 `true`：** 那是违反规范 §8 的，并且它把缺失
  授权洗成 `Published` 处置。一个带具名原因的 `Blocked` 处置是诚实且可测试的。
- **相比在 D 与 I 交付缺失签发方之前什么都不做：** 那会让 compiler 无限期不可达，也
  让适配器永远无法针对那两份**确实存在**的记录被测到。

## 后果，直说

- 本决定之后，`brain compile` 将报告**发布被阻塞**，而不是阶段被跳过。这是进步，但
  对所有只读通知文本的人来说会看起来像退步。通知文本必须改为说明是哪个标志阻塞了它。
- 在任何现实输入上，八个标志中会有六个为 `true`，因此管线的可观测行为几乎不变。
  价值在于门禁现在被真正执行，而不是被绕过。
- 由此直接产生两项新工作：实现 D4 的 storage 读方法，以及实现 D 侧
  publication-participant 注册表，让 `publication_participant_admitted` 有来源。
- 此处没有任何内容授权 `Published`。生产中的第一次 `Published` 需要八个标志全部来自
  真实签发方。

## 什么情况会重开本决定

- 如果 D 的 fence/admission 权威并非 `AdmissionStore` —— 即如果 `AdmissionStore`
  本意是本地测试替身而非 D 侧账本。待查证据：`07-agent-integration` 或
  `01-system-architecture` 中是否指定了别的 crate 作为 producer registry。目前树里
  没有任何东西与"视之为权威"矛盾；但也没有任何东西明确确认它，这一残余风险记录在此。
- 如果 `canonical_commit_confirmed` 获得生产者（`admission_canonical_commit_cursor`
  字段暗示曾经打算有）。
- 如果后续规范修订赋予 E 独立可见性授权，而 §8 目前禁止这一点。

## 增补 —— D6，2026-11-22 02:35 +08:00 作出（#552、#545 落地之后）

D3 把 `canonical_commit_confirmed` 归为"没有生产者"的标志。这个理由是错的，
而错误的代价很具体：它会让下一个人去"把字段暗示的那个生产者补上"。没有这样的
生产者可补，因为它要产出的事实，其主人自己还没有定义。

### 矛盾，实测

以下四处读取均来自 `444deef1`。

| 位置 | 它说的是什么 |
|---|---|
| `memory-compiler/src/lib.rs:633-635` | `if producer_request.admission_canonical_commit_cursor.is_none() { return Err(MissingCanonicalCommit) }` |
| `memory-compiler/src/lib.rs:641` | `staging.canonical_commit_confirmed = true;` |
| `memory-compiler/src/publication_authority.rs:103` | `canonical_commit_confirmed: false,` |
| `memory-compiler/src/lib.rs:531` | `if !proof.canonical_commit_confirmed { return Blocked }` |

在一次 `compile()` 调用里，compiler 先断言提交已确认（否则直接报错不往下走），
随后又把"未确认"的证明交给 gate。gate 于是阻塞。这不是保守的默认值，而是同一个
布尔量在同一次运行里取了对立的值。

又因为 staging 对缺失游标是**硬报错**，要走到 gate，唯一的办法就是提供一个游标。
也就是说，gate 的可达性依赖于把那个事实断言出来。

### 被断言的事实从哪来

`admission_canonical_commit_cursor` 是 `ProducerRegistrationRequest` 的字段
（`admission.rs:127-137`），由调用方提供，账本只是把它存下来。没有任何东西校验它，
也无法校验：仓库里没有可用于比对的 canonical commit 记录类型。

domain 自己就是这么写的（`memory-domain/src/lib.rs:489-500`）：

```rust
/// NOT DEFINED: awaiting D. Required placeholder with no invented commit semantics.
/// `pending_d()` is public and any caller can create this placeholder.
pub struct CanonicalCommitRef(());
impl CanonicalCommitRef { pub const fn pending_d() -> Self { Self(()) } }
```

`CanonicalCommitRef` 不携带任何数据，`pending_d()` 让任何调用方都能凭空造一个。
它是一个公开声明的占位符，等待其主人冻结契约。

所以真实的链条是：调用方断言一个不透明游标 → 账本存下 → compiler 读回来称之为
"已确认的 canonical commit" → 而 domain 在另一处说这种契约根本不存在。这正是
`compiler-stage-contract.md` §8 所禁止的"替代授权决定"，而且它是今天通往发布
gate 的**唯一**路径。

### 决定

**D6.1. `canonical_commit_confirmed` 在生产适配器中保持 `false`，直到 owner D
冻结 canonical commit 契约，并给出可构造、携带内容的引用类型与校验器。**
不是"直到出现生产者"——那个貌似生产者的东西是调用方断言，把它提升上来，等于把
未校验的声明洗成 `Published`。

**D6.2. staging 不得再把调用方提供的游标称作"已确认的提交"。** 它的前置条件改名
为它真正校验的东西：`canonical_commit_cursor_recorded`。检查、错误与所有 disposition
逐字节不变，缩小的只是"声明"的幅度，让它回到证据范围内。

**D6.3. `ProducerRegistrationRequest::admission_canonical_commit_cursor` 在 E 侧
任何地方都不得被当作提交确认的证据**，注释与文档字符串同样适用。若它作为请求字段
继续存在，必须标注为未校验。

**D6.4. `CanonicalCommitRef::pending_d()` 不得出现在任何喂给发布授权的路径上。**
它是占位便利设施，不是证据。

### D6 不决定什么

D 何时交付该契约。那是 D 自己的前沿（frontier），§8 也不允许 E 代为发明。D6 只做一件事：
让 E 停止假装该契约已经存在。

### 后果

行为不变：`compile()` 仍返回 `Ok(Blocked)` 并指明 `canonical_commit_confirmed`，
`brain-cli` 仍以 0 退出。变的是：树里不再有一行断言"其自身 domain 拒绝定义的事实"。
`Published` 仍只能经由一份真实的 canonical commit 契约，加上 D3 已点名的那两个
参与者授权才能达成。
