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

## 证据（在 `main @ b961ba31` 上核验）

以下每条断言都是一次仓库检索，无需阅读任何 Owner 交接即可复现。

**1. 两个 `PublicationAuthority` 实现都位于 `#[cfg(test)]` 内。**

```sh
grep -rn "impl PublicationAuthority" --include=*.rs crates/
```

```
crates/memory-compiler/src/lib.rs:899: impl PublicationAuthority for TestAuthority {
crates/memory-compiler/src/lib.rs:1227: impl PublicationAuthority for RecoveryAuthority {
```

`#[cfg(test)]` 出现在第 738、745、856、1177、1434 行。两个实现都落在 856 之后、1434 之前，即测试专用模块内部。非测试构建无法触达其中任何一个。

**2. `compile()` 仅被测试调用。**

```sh
grep -n "\.compile(" crates/memory-compiler/src/lib.rs
```

全部五处命中位于 1095–1157 行，处于测试模块内。在 `memory-compiler/src/lib.rs` 之外执行 `grep -rn "MemoryCompiler" crates/` 返回**零匹配**。

**3. `brain-cli` 引用编译器仅为获取版本字符串。**

```sh
grep -n "memory_compiler" crates/brain-cli/src/main.rs
```

```
1:use memory_compiler::COMPILER_VERSION;
```

CLI 串联了 `memory-domain` → `memory-storage-sqlite` → `memory-store` → `memory-context`，到此为止。它自身的 verbose 输出印证了这一顺序。

**4. 端到端实跑复现该跳过。**

一个真实事件 JSON 经 `brain compile --verbose` 产出了合法的 1103 字节 ContextSnapshot（1 条 entry），并打印了上述跳过提示。管道在上下文组装这一段确实是端到端的；编译器不在其中。

## 为何这比测试计数更重要

`GAP-BASELINE-004` 测得 338 个通过测试。其中相当一部分位于 `memory-compiler`（该次测量为 53 个），而这些测试全部在演练一条没有生产调用方能到达的 `compile` 路径。因此**测试数量不构成**"编译在产品中可用"的证据。任何形如"管道把事件编译成已发布的派生物"的表述，在 `cargo test` 之外目前都不成立。

这不是 Owner E 准入工作的缺陷。准入账本、生产者注册表、依赖闭包与 fence 均已实现并通过测试。缺口在于它们所供给的那个 authority 没有生产实现者。

## 候选方向

### (a) 交付真实的 `PublicationAuthority`

针对实际发布路径实现该 trait：从既有的持久发布记录中取得证明，取不到时返回类型化失败。这是唯一能让编译器变得可达的方向。它要求先确定生产发布存储——而该存储目前尚不存在。

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
