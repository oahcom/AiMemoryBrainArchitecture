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

### `AdmissionStore` 不是 D 的账本 —— 这是定论，不是开放问题

此处原先的第一条记录了一项残余风险：`AdmissionStore` 可能是本地测试替身而非
D 侧账本，而树里既没有确认也没有否认它的权威。这个风险不存在。模块用自己的
doc comment 声明了自己的范围（`crates/memory-compiler/src/admission.rs:3-5`）：

```
//! This crate implements the E-side lifecycle and a local SQLite admission
//! ledger. It does not claim to be the D-authoritative producer ledger or to
//! provide a cross-service D/Storage visibility transaction.
```

`AdmissionStore` 是 E 侧的本地账本。它**不是** D 权威的 producer 账本，也不是
测试替身 —— 它是 E 为自己保留的持久记录。那条 bullet 悬置的问题，正是它所指向
的那个文件回答的。

对 D1 的后果：那里点名的持久发布记录，记录的是**E 的本地视图**，不是跨服务的
D/Storage 事务。日后若有人主张 `publication_receipts` 是 D 权威的，那将与模块自己的
doc comment 相矛盾；那是模块文档的缺陷、应当修正，而不是对它的某种读法。

### 仍然开放的

- 如果后续规范修订赋予 E 独立可见性授权，而 §8 目前禁止这一点。

原先的第二条 —— `canonical_commit_confirmed` 获得生产者 —— 已解决。它在此删除，
并记入下方 D8 增补，那里点名了生产者。

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

## 增补 —— D7，2026-11-22 02:52 +08:00 作出

D3 把 `publication_participant_admitted` 列为"来源不足"，而"后果"一节又承诺下一项
工作是"实现 D 侧的发布参与者登记表"。读过 C 契约之后，可以看出这个承诺在 E 这一层
就不该作出。这个标志需要的不是一张登记表，而是两个在本仓库里并不存在的组件。

### 签发者是规定好的，而且不在本地

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:137`
（中文镜像 `docs/zh-CN/.../phase-3.6-c-submit-...:137`）对 C 的约束是：

> C MUST NOT invoke a protected provider side effect until the exact participant has
> a quorum-committed `JF10_PREPARE_INTENT_REGISTERED`, a **Storage-signed**
> `PreparedParticipantReceipt` is durably registered as
> `JF10_PREPARED_PARTICIPANT_REGISTERED`, and the I owner-final gate has produced an
> authoritative terminal decision for the exact immutable tuple.

三个签发者，各有其名：COC 的 quorum、Storage 的签名、I 的 terminal decision。

### 这三者在本仓库里都不存在

| 元素 | 状态 | 实测方式 |
|---|---|---|
| Rust 中的 `JF10_*` 状态 | 不存在 | `grep -rn "JF10" --include=*.rs crates/` → 0 处 |
| 回执的线上形状 | 仅候选 | schema 标题："… — **candidate**"；描述："does not select or verify a cryptographic suite, canonicalization profile, key policy, or cross-message owner authority" |
| 一致性结论 | 无人主张 | `08-bmcp-protocol/protocol-index.md:55` → "no dedicated validator or production conformance claim" |
| C 侧条件 | 已规定、未运行 | C 契约："C-CO-01..10 and H-JF10-01..10 remain SPECIFIED / NOT RUN" |

### 为什么本地登记表是错误的修法

要把 `publication_participant_admitted` 记成 `true`，系统必须接受一份
`PreparedParticipantReceipt` 并把它当作"已准入"。但是：

- 没有任何密钥策略可以校验"Storage 签名"这一要求，而 schema 明确声明自己不是密码学 profile；
- 没有 quorum，无法确立 `JF10_PREPARE_INTENT_REGISTERED`；
- 没有 I 的 terminal decision 来绑定精确 tuple。

在这些条件下写出来的登记表，只会存下无法校验的声明，并把它报告成准入。那就是
`compiler-stage-contract.md` §8 所禁止的替代授权决定，而且比 `false` 更糟：它看起来
像一个真实的见证，实际只是调用方断言的转发器。这与 D6 从 canonical commit 路径上
移除的缺陷，是同一类，只是低了一层。

### 决定

**D7.1. `publication_participant_admitted` 保持 `false`；在 Storage 签名、COC quorum
与 I terminal decision 存在之前，E 不得构建发布参与者登记表。** 本增补撤回"后果"一节
中关于 D 侧登记表的承诺。

**D7.2. 阻塞依赖记为外部依赖，并点名归属：** COC（quorum）、Storage（签名 +
`JF10_PREPARED_PARTICIPANT_REGISTERED` 的持久注册）、I（针对精确 tuple 的 terminal
decision）。三者 E 都无法提供。

**D7.3. 协议索引对这一映射的记录偏弱。** `protocol-index.md:68` 把
`Storage.PreparedParticipantReceipt` 记为 "Schema-local definition; no separate
normative source mapped in this scoped audit"，而 C 契约第 137 行正是它的规范来源。
"in this scoped audit" 这个限定是诚实的，但索引是本仓库"什么实现了什么"的权威，
该行应当引用 C 契约。

### 后果

三个缺失的证明标志中，有两个现在用同样的方式解释清楚了，而且都无法由 E 关闭：
`canonical_commit_confirmed`（D6：契约未由 D 定义）与
`publication_participant_admitted`（D7：签发者需要 Storage 签名 + COC quorum + I 决定）。
`Published` 依然不可达，但现在有三个点名的原因，而不是一个含糊的原因。这就是 E 权限
范围内能给出的、诚实的收敛结论。

## 决策后事实更正 — 2026-11-22

PR #552 及后续生产集成已取代"阻断本项的问题"一节中的事实前提，即
`PublicationAuthority` 没有生产实现。

`AdmissionPublicationAuthority`
（`crates/memory-compiler/src/publication_authority.rs:50`）现已作为生产实现存在，
且 `brain-cli` 通过非测试执行路径调用 `MemoryCompiler::compile()`
（`crates/brain-cli/src/main.rs:4`、`:246`、`:285`）。GAP-07 已于 2026-11-22
基于该证据就生产可达性关闭。

本次更正不使历史决策失效，也不确立发布授权已经完整。上文关于"持久发布记录是什么"的
决策本身不变，D3 以及本修正案中的 D6/D7 结论亦不变。

未解决的关切仍然存在，另登记于
`GAP-14-PUBLICATION-AUTHORITY-AND-STORE-LIFECYCLE.md`：

1. `MemoryStore` 未暴露生产 prepare/publish 生命周期（GAP-14-A）。
2. 三个发布标志在 D3 下缺少权威签发者（GAP-14-B）。
3. 发布记录的持久恢复尚未经独立验证（GAP-14-C）。

原文保留于上而非改写，因为一份所述前提被静默修改的决策记录是无法审计的。

## 增补 —— D8，2026-11-22 作出（GAP-12 第 3 步落地之后）

三处更正，全部读自 `main` 的 `4a7624da`（#622 的合并提交，head 为 `0b446492`）。

### D8.1 —— `AdmissionStore` 是 E 的账本，D1 按此读

`crates/memory-compiler/src/admission.rs:3-5`：

```
//! This crate implements the E-side lifecycle and a local SQLite admission
//! ledger. It does not claim to be the D-authoritative producer ledger or to
//! provide a cross-service D/Storage visibility transaction.
```

因此 D1 的记录，是 E 对自己准入与发布了什么的本地视图，并与 storage 的
`PreparedHidden` 行做联合。它不是跨服务 D/Storage 可见性事务，本 ADR 也不这样主张。
"什么情况会重开本决定"下的那条残余风险予以撤回：它不是开放问题，而是一个没被读到
的定论否定。

### D8.2 —— `canonical_commit_confirmed` 已有生产者

`D-OWNER-DECISION-CANONICAL-COMMIT-001` 冻结了契约；#622 实现了它。链条在
`4a7624da` 上：

| 步骤 | 位置 |
|---|---|
| 签发记录 | `AdmissionStore::issue_canonical_commit`，`admission.rs:996` |
| 校验记录，三态 | `AdmissionStore::validate_canonical_commit`，`admission.rs:1069` |
| 读入标志 | `AdmissionPublicationAuthority::canonical_commit_confirmed`，`publication_authority.rs:56-73` |
| 报告标志 | `publication_authority.rs:132` 的 `canonical_commit_confirmed,`，取代 D3 要求的字面 `false` |

"什么情况会重开本决定"下的第二条已删除，而不是留成陈旧条目：它的条件已经发生，
本小节就是它去的地方。D6.1 的暂停由它所等待的契约解除 —— 一个可构造、携带内容的
引用类型，以及针对它的校验器。

有一项范围事实必须随之记录，因为这份记录并不是生产身份：签发者是 dev-baseline
签发者（`d-owner-proxy/dev-baseline-v1`），其自身决策称它为 "an explicit
development trust anchor, not a production cryptographic identity"。该标志确认的是
一份 dev-baseline 记录。

### D8.3 —— `Published` 仍然不可达

`publication_authority.rs:133-139` 仍然如此报告，D3 的注释原样保留：

```rust
publication_participant_admitted: false,
protected_visibility_authorized: false,
```

`PublicationGate::run` 把其中任一为 `false` 映射为 `Suppressed`（`lib.rs:646-650`），
所以一次带有合法 canonical-commit 记录的运行报告 `Suppressed`，永远不会是 `Published`。
原因是 D7 与 D3，未变：没有 Storage 签名、没有 COC quorum、没有 I terminal decision，
也没有 E 的独立可见性授权。

这就是 D8 之后的收敛结论：三个无来源标志中一个有了来源，两个仍然没有，而 `Published`
仍然需要八个全部成立。
