# GAP-07 · 编译阶段在生产路径上不可达

**状态**：**已关闭**（2026-11-22）— 生产可达性已确立。后继缺口登记于 `GAP-14-PUBLICATION-AUTHORITY-AND-STORE-LIFECYCLE.md`。
**领域**：GAP-01 / memory-compiler / brain-cli
**归属线**：Owner E（编译器准入）+ Owner A（端到端）
**关闭基线**：`main @ 87d503ba`

## 关闭记录

**已关闭 — 编译器生产可达性已确立。**

现在存在一个生产 `PublicationAuthority` 实现，且 `brain-cli` 通过非测试的生产路径调用 `MemoryCompiler::compile()`。

编译器的发布闸门真实执行，并在授权标志缺失时正确报告发布被阻断。CLI 通过 stderr 与 compiler-status sidecar 暴露该处置，非 verbose 模式下同样可见。

本次关闭确立的是**生产可达性**与**闸门执行可观测性**。它**不**确立发布成功、不确立持久发布权威、也不确立"事件被编译成已发布记忆"的端到端能力。

### 变化对照

| 原始缺口 | 当前证据 | 判定 |
|---|---|---|
| 无生产 `PublicationAuthority` | `crates/memory-compiler/src/publication_authority.rs:50` — `impl PublicationAuthority for AdmissionPublicationAuthority<'_>` | 已解决 |
| 无非测试调用方 | `crates/brain-cli/src/main.rs:4` 导入、`:246` 构造、`:285` `compiler.compile(...)` | 已解决 |
| 无二进制级集成验证 | `crates/brain-cli/tests/compiler_skip_is_visible.rs` — 4 个测试驱动 `env!("CARGO_BIN_EXE_brain")` | 已解决 |
| 阻断状态不可见 | stderr 无条件输出 + 产物旁的 `.compiler-status` sidecar | 已解决 |

### 四条关闭标准逐条核对

**标准 1** — 要么存在生产 authority 且 `compile()` 被非测试路径调用，要么每次成功运行都在无需 `--verbose` 的 stderr 上、以及产物内部或旁边报告该跳过。**两半均成立。** 前半直接满足；后半亦满足，因为发布被拒绝且拒绝被报告。

**标准 2** — 有测试通过二进制或非测试入口证明该行为。`compiler_skip_is_visible.rs` 将编译后的二进制作为子进程运行，断言确切的提示字符串、退出码 `0`、输出快照存在、以及 sidecar 内容。它不触碰 `#[cfg(test)]` 内部。

**标准 3** — `--verbose` 不再是报告该跳过的唯一位置。在 `main @ 87d503ba`、WSL Ubuntu / cargo 1.95.0 上实测：

```
$ brain compile --input crates/brain-cli/fixtures/event.json --out /tmp/o.json
EXIT=0
--- stdout ---
（空）
--- stderr ---
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed; false flags: [canonical_commit_confirmed, publication_participant_admitted, protected_visibility_authorized]
--- /tmp/o.json.compiler-status ---
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed; false flags: [canonical_commit_confirmed, publication_participant_admitted, protected_visibility_authorized]
--- /tmp/o.json ---
1256 字节，合法 JSON object
```

**标准 4** — 无文档把 `brain compile` 描述为执行编译。全仓检索 `compiler stage skipped|no production implementation|PublicationAuthority has no production` 得 10 处命中，全部在断言"无生产实现"这一现已为假的前提；无一处断言 `brain compile` 执行编译。这些过时断言按 2026-11-22 裁决处理：历史测量原样保留、当前状态记录更正、ADR 追加事实更正而非改写。

### 本次关闭刻意不宣称的部分

实际行为比原候选方向 (b) 更强：编译器不是被跳过，而是真实运行、被发布闸门拒绝、并指明是哪一面旗挡住。这相当于部分达成方向 (a) 加上完整达成 (b)。

但它**不**是发布成功的宣称。`canonical_commit_confirmed` 没有权威签发者（`OWNER-DECISION-PUBLICATION-RECORD-001` D3），因此生产运行停在 `Blocked`，永远到不了 `Published`。

三项彼此独立的关切仍然开放，**不**随本次关闭一并关闭。它们登记为 GAP-14：

- **GAP-14-A** — `MemoryStore` 未暴露 `prepare_version` / `publish_prepared` / `publication_state`；CLI 实际使用的门面暴露 10 个方法，无一涉及发布生命周期。
- **GAP-14-B** — 三个发布标志缺少权威签发者（D3）。受阻于该决策。
- **GAP-14-C** — 发布记录的持久性。`AdmissionStore::open(request.admission_path)` 只证明打开了一个文件路径，仅此而已。发布记录的跨进程恢复尚未验证，不得标记为已解决。

---

*以下章节是 `main @ 5643974b` 时的历史记录，原样保留。它们描述的是一个已不存在的状态。*

---

## 缺口陈述（已废止）

> **2026-11-22 废止。** 该陈述的两半现在都为假：生产 `PublicationAuthority` 已存在，且 `brain-cli` 是非测试调用方。保留作历史。

`MemoryCompiler::compile` 所需的 `PublicationAuthority` trait 没有任何生产实现，也不存在任何非测试调用方。因此仓库中唯一的可执行入口（`brain-cli`）完全跳过编译阶段，并在运行时明确说明：

```
compiler stage skipped: PublicationAuthority has no production implementation
```

`memory-context` 及其之前的每一段都真正端到端可用。`memory-compiler` 内部的一切只由 `#[cfg(test)]` 代码执行。

## 证据（在 `main @ 5643974b` 上重新核验，含 #523 与 #533）

以下每条断言都是一次仓库检索，无需阅读任何 Owner 交接即可复现。

**1. 三个 `PublicationAuthority` 实现全部位于 `#[cfg(test)]` 内。**

```sh
grep -rn "impl PublicationAuthority" --include=*.rs crates/
```

```
crates/memory-compiler/src/lib.rs:923: impl PublicationAuthority for EvidenceAuthority {
crates/memory-compiler/src/lib.rs:942: impl PublicationAuthority for TestAuthority {
crates/memory-compiler/src/lib.rs:1332: impl PublicationAuthority for RecoveryAuthority {
```

`#[cfg(test)]` 出现在第 757、764、875、1282、1539 行。875 行开启的模块覆盖 923 与 942；1282 行开启的模块覆盖 1332。因此三个实现都是测试专用，非测试构建无法触达其中任何一个。

需要说明：#533 新增 `EvidenceAuthority` 以建模四种发布处置，这是对测试模型的真实改进，且不改变本缺口——新增的是第三个实现，它同样是测试专用。

**2. `compile()` 仅被测试调用。**

```sh
grep -n "\.compile(" crates/memory-compiler/src/lib.rs
```

全部命中位于 1187–1249 行，处于 1282 行开启的 `#[cfg(test)]` 模块内。在 `memory-compiler/src/lib.rs` 之外执行 `grep -rn "MemoryCompiler" crates/` 返回**零匹配**。

**3. `brain-cli` 引用编译器仅为获取版本字符串。**

```sh
grep -n "memory_compiler" crates/brain-cli/src/main.rs
```

```
1:use memory_compiler::COMPILER_VERSION;
```

CLI 串联了 `memory-domain` → `memory-storage-sqlite` → `memory-store` → `memory-context`，到此为止。它自身的 verbose 输出印证了这一顺序。

**4. 发布原语已存在，但未被暴露。**

#523 恰好补上了 `PublicationProof.storage_prepared_hidden` 所需的存储操作。它位于 trait 上并在 SQLite 中实现：

```sh
grep -n "prepare_version\|publish_prepared" crates/memory-storage/src/lib.rs
```

```
74: fn prepare_version(&mut self, request: PrepareRequest, scope: &[ScopeRef]) -> Result<PreparedCommitReceipt, StorageError>;
77: fn publish_prepared(&mut self, publication_id: &str, expected_current_version: Option<OpaqueId>, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError>;
```

`memory-storage-sqlite` 实现了两者。但 CLI 实际使用的门面 `MemoryStore` 一个都没有暴露：

```sh
awk 'NR<200 && /pub fn /{print NR": "$0}' crates/memory-store/src/lib.rs
```

```
33:     pub fn new(storage: S) -> Self { Self { storage } }
35:     pub fn into_storage(self) -> S { self.storage }
37:     pub fn create_memory(
48:     pub fn read_current(
57:     pub fn read_revision(
67:     pub fn write_revision(
89:     pub fn resolve_idempotency(
```

`memory-store` 中仅有的 `prepare_version`/`publish_prepared` 函数体位于第 212、286 行的 `FakeStorage` 上，处于 112 行开启的 `#[cfg(test)]` 模块内。也就是说：原语存在于比任何调用方都低一层的层里，而唯一能调用它的那一层没有把它暴露出来。

**5. 端到端实跑复现该跳过。**

一个真实事件 JSON 经 `brain compile --verbose` 产出了合法的 1103 字节 ContextSnapshot（1 条 entry），并打印了上述跳过提示。管道在上下文组装这一段确实是端到端的；编译器不在其中。

## 为何这比测试计数更重要

`GAP-BASELINE-004` 测得 338 个通过测试。其中相当一部分位于 `memory-compiler`（该次测量为 53 个），而这些测试全部在演练一条没有生产调用方能到达的 `compile` 路径。因此**测试数量不构成**"编译在产品中可用"的证据。任何形如"管道把事件编译成已发布的派生物"的表述，在 `cargo test` 之外目前都不成立。

这不是 Owner E 准入工作的缺陷。准入账本、生产者注册表、依赖闭包与 fence 均已实现并通过测试。缺口在于它们所供给的那个 authority 没有生产实现者。

## 候选方向（历史）

### (a) 交付真实的 `PublicationAuthority`

针对实际发布路径实现该 trait：从既有的持久发布记录中取得证明，取不到时返回类型化失败。这是唯一能让编译器变得可达的方向。

#523 实质性地减少了工作量：`prepare_version` 返回的 `PreparedCommitReceipt` 正好证明派生物已暂存但尚不可读，即 `storage_prepared_hidden` 所断言的内容。但在诚实实施之前仍缺两件事：`MemoryStore` 必须暴露 prepare/publish；且发布记录必须跨进程重启持久，而不是保存在编译器内存态准入存储里。

### (b) 让跳过变得不可忽略，并标记输出

本工作项的早期草稿建议"拒绝产出输出"。那太粗暴了：它会禁用唯一可用的入口，并移除唯一一个"摄取 → 存储 → 上下文组装确实可用"的可执行证明。真正的缺陷不是 CLI 在跑，而是它能产出一份看起来正确的输出，却没人得知最重要的阶段被跳过了。

最小且诚实的版本：

1. 无条件打印跳过提示，而不只在 `--verbose` 下。它目前位于 `if verbose` 块内，默认运行什么也不说。
2. 把该跳过记录进产物，让这一事实随文件走，而不是在没人读 stderr 时丢失。这不得改变 `ContextSnapshot` 的序列化契约；一个同级 sidecar 或快照之外的显式顶层标记即可。
3. 不动退出码，以免破坏既有调用方。

这样管道保持可运行，同时让"这份输出没有经过编译"无法被误认为"这份输出经过了编译"。

### (c) 保持现状，并停止称该路径为端到端

保留跳过，并在任何文档或报告中停止把 `brain compile` 描述为端到端管道。风险在于跳过提示位于 `--verbose` 的 stderr 中，极易被忽略。

## 建议（历史）

**先做 (b)，待发布存储被规定后再做 (a)。** 上述范围的 (b) 只有几行，且不削减能力。一个在跳过编译后仍返回上下文快照、且不带 `--verbose` 就沉默的 CLI，比一个直接拒绝的 CLI 更糟，因为输出看起来是正确的；但一个直接拒绝的 CLI 也会摧毁唯一可用的演示。让跳过变成无条件、并把它附着到输出上，既得到诚实，又不失去功能。

方向 (a) 不得即兴实施。针对临时拼凑的存储实现 `PublicationAuthority`，只会制造出本工作项所针对的同一类不可达抽象。

## 关闭标准（历史 — 四条已于 2026-11-22 全部核实）

1. 要么存在生产 `PublicationAuthority` 且 `compile()` 至少被一条非测试代码路径调用，要么每一次成功的 `brain compile` 运行都报告编译阶段被跳过——既在无需 `--verbose` 的 stderr 上，也在产物内部或旁边。
2. 有测试通过二进制或非测试入口证明所选行为——而非通过 `#[cfg(test)]` 内部。
3. `--verbose` 不再是报告该跳过的唯一位置。
4. 在 (1) 对真实权威成立之前，任何文档不得把 `brain compile` 描述为执行编译。
