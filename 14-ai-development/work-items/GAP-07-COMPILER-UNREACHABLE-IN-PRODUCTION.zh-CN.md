# GAP-07 · 编译阶段在生产路径上不可达

**状态**：未关闭 — 阻断一切关于"编译"的端到端结论
**领域**：GAP-01 / memory-compiler / brain-cli
**归属线**：Owner E（编译器准入）+ Owner A（端到端）

## 缺口陈述

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

## 候选方向

### (a) 交付真实的 `PublicationAuthority`

针对实际发布路径实现该 trait：从既有的持久发布记录中取得证明，取不到时返回类型化失败。这是唯一能让编译器变得可达的方向。

#523 实质性地减少了工作量：`prepare_version` 返回的 `PreparedCommitReceipt` 正好证明派生物已暂存但尚不可读，即 `storage_prepared_hidden` 所断言的内容。但在诚实实施之前仍缺两件事：`MemoryStore` 必须暴露 prepare/publish；且发布记录必须跨进程重启持久，而不是保存在编译器内存态准入存储里。

### (b) 让 `brain-cli` 失败关闭，而不是跳过

把 CLI 从"跳过编译阶段"改为"未配置发布权威时拒绝产出输出"。这不增加任何能力，但消除了"`brain compile` 会执行编译"这一错误印象。改动很小且诚实，并让缺口对运行二进制的人可见，而不只是对读源码的人可见。

### (c) 保持现状，并停止称该路径为端到端

保留跳过，并在任何文档或报告中停止把 `brain compile` 描述为端到端管道。风险在于跳过提示位于 `--verbose` 的 stderr 中，极易被忽略。

## 建议

**先做 (b)，待发布存储被规定后再做 (a)。** 目前跳过提示是"最重要的阶段没有运行"的唯一信号，而它在不带 `--verbose` 时被抑制。一个静默跳过编译后仍返回上下文快照的 CLI，比一个直接拒绝的 CLI 更糟，因为输出看起来是正确的。

方向 (a) 不得即兴实施。针对临时拼凑的存储实现 `PublicationAuthority`，只会制造出本工作项所针对的同一类不可达抽象。

## 关闭标准

1. 要么存在生产 `PublicationAuthority` 且 `compile()` 至少被一条非测试代码路径调用，要么 `brain-cli` 在编译阶段无法运行时拒绝产出输出。
2. 有测试通过二进制或非测试入口证明所选行为——而非通过 `#[cfg(test)]` 内部。
3. `--verbose` 不再是报告该跳过的唯一位置。
4. 在 (1) 对真实权威成立之前，任何文档不得把 `brain compile` 描述为执行编译。
