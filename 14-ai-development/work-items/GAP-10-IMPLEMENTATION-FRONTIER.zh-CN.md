# GAP-10 · 实现前沿：每个领域究竟卡在什么上

**状态**：未关闭 — 本文是地图，不是缺陷
**领域**：跨领域
**目的**：用依赖排序的实现前沿，替换六个未测量的完成度百分比

## 为什么写这份文档

一份要求"推进关键缺失工作"的指令列出了六个领域及完成度估计：Memory Compiler 85% 未实现、Memory Context 80%、Agent Integration 90%、BMCP 60%、Phase 2 领域模型 100% 未启动、端到端 100% 未启动。

对照仓库实测，这六项中有三项明显不准，而且这六项并非并列——它们构成一条链：多数剩余工作被两个上游权威卡住（D 发布权威、H 传输冻结），因此"六路同时推进实现"会产生无法合并的工作。

本文用计数替换百分比，并按"真正未被阻塞"来排序。

## 1. 实测状态（在 `main @ 76b6470e` 上核验）

### 1.1 生产代码零桩

```sh
grep -rn "todo!\|unimplemented!" --include=*.rs crates/
```

8 处命中全部位于 `crates/memory-domain/tests/phase2_acceptance.rs`，且在 `#[ignore]` 的测试体内（154、162、191、257、332、340、403、411 行）。

工作区里没有任何半写的生产代码。此处的"未实现"指**有规格但一行代码都没有**，而不是"函数没写完"。这一区分很重要：它意味着下一个增量永远是"写出 X 的第一版"，而不是"把 X 补完"。

### 1.2 Phase 2 领域模型大体已实现，不是 0%

"Phase 2/3 领域模型 100% 未启动"这一说法对 Phase 2 不成立。类型已存在并有测试：

```sh
grep -n "pub struct Fact\b\|pub struct FactRevision\|pub enum EntityIdentityStatus\|pub struct RelationDefinition\|pub struct EvidenceExtension\|pub struct ClaimRevision" crates/memory-domain/src/lib.rs
```

```
365: pub struct ClaimRevisionRef(OpaqueId);
369: pub struct FactRevisionRef(OpaqueId);
435: pub struct ClaimRevision {
504: pub struct Fact { fact_ref: FactRef, initial_revision: Box<FactRevision> }
522: pub struct FactRevision {
605: pub enum EntityIdentityStatus { Provisional, Resolved, Merged, Split, Retired }
664: pub struct RelationDefinition { pub relation_type: String, ... }
686: pub struct EvidenceExtension {
```

`crates/memory-domain` 运行 36 个单元测试加 11 个验收测试，其中 9 个被 `#[ignore]` 并各自写明缺失的 API（无 `ClaimRevisionRegistry`、无 `classify_claim_change`、无 `RelationTypeRegistry`、无 `ProvenanceGraph` 等）。

所以 Phase 2 大致是"类型与不变量已完成，注册表与分类器缺失"。Phase 3 是另一个问题，本文不涉及。

### 1.3 Memory Context 已有 77 行实测覆盖表

`06-memory-context/context-implementation-coverage.md` 已对每个关注点做了分类。其最新一轮记录为 77 行中 **25 未实现 / 43 部分 / 9 已实现**。

关键在于每行都标注了责任方。统计归属列：

| 归属 | 行数 |
|---|---|
| `D`（发布权威） | 40 |
| `本线程可做`（现在就能本地实现） | 19 |
| `不在范围` | 10 |
| `I`（授权权威） | 8 |

因此"80% 未实现"不可执行，但**19 行可本地实现**，另有 40 行在等 D。这才是缺口的真实形状。

### 1.4 全仓没有任何网络传输

```sh
grep -rn "TcpListener\|hyper\|axum\|transport" --include=*.rs crates/
```

除明确声明"不含传输"的文档注释外无匹配（`agent-integration/src/lib.rs:3`"不执行……网络传输"，`memory-context/src/lib.rs:3`"刻意停在持久化与传输之前"）。

工作区唯一的二进制是 `crates/brain-cli/src/main.rs`。

所以"BMCP 完整协议栈 60% 未实现"是错的框架。协议**产物**相当可观：32 个 JSON schema、5 个 Python 校验器、545 个通过的一致性测试，加上 Rust 的 `bmcp-protocol`（1372 行：`evidence`、`strict_json`、`validate`、`digest`、`parse_and_validate`）。不存在的是**传输与服务端**——那是一个东西，不是协议栈的 60%。

### 1.5 Agent Integration 是被阻塞，不是被忽视

`07-agent-integration/agent-integration-architecture-completion.md` §8.3 列出 7 步集成序列，并明说第 3–6 步在当前工作区不是可调用路径。§9 列出 RT-01..RT-09 验收场景，全部标记为 NOT RUN 或 BLOCKED / DEPENDENCY_NOT_FROZEN。

阻塞点写得很明确：D 的发布/依赖/最终闸门、I 的授权、H 的 BMCP 传输/ACK。Agent Integration 无法在这些之前实现，除非凭空发明契约。

## 2. 依赖链

```
Phase 2 领域类型            已完成（注册表/分类器缺失）
        |
        v
memory-storage / memory-store  已完成，含 hidden prepare / explicit publish（#523）
        |
        v
memory-context                 77 行表：9 已实现，43 部分，25 缺失
        |                      其中 19 行可本地实现
        v
PublicationAuthority  <-- 咽喉点。3 个实现全部在 #[cfg(test)] 内
        |
        +--> memory-compiler::compile 可达
        +--> 25+43 行中 40 行解锁
        +--> Agent Integration 第 3-6 步解锁
        |
        v
BMCP 传输 + 服务端   <-- 不存在；同时也卡住 Agent Integration
        |
        v
端到端（brain-cli 越过上下文组装）
```

**咽喉点是 `PublicationAuthority`（GAP-07）。** 它是单个 trait 的单个缺失生产实现。链上它以上的部分要么已完成、要么可本地实现；它以下的部分全部被阻塞。

这就是"六路同时推进"行不通的原因：六项里有五项汇聚到同一个缺失的 trait 实现，加上一个缺失的传输层。

## 3. 现在真正未被阻塞的工作

按依赖排序。每一项今天就能派工，无需任何外部决定。

### 第一层 — 解锁最多下游

**T1.1 — 生产版 `PublicationAuthority`（GAP-07 方向 (a)）**

`prepare_version` / `publish_prepared` 已在 Storage trait 与 `memory-storage-sqlite` 中（#523）。缺的是：

- `MemoryStore` 没有暴露它们（只暴露 5 个方法，无 prepare/publish；仅有的函数体在 `cfg(test)` 内的 `FakeStorage` 上）。
- 编译器内存态准入存储之外，没有持久发布记录。

实现它使 `MemoryCompiler::compile` 可达，这是任何"系统能编译"主张的前提。

**T1.2 — 19 行可本地实现的 Memory Context**

在覆盖表中以 `本线程可做` 标出。值得注意的几项：候选集边际覆盖优化器、预算/充分性可观测性、投递尝试账本、带谱系安全输出的 Compact 操作。

这些不需要外部权威，且可独立测试。

### 第二层 — 已解锁但范围较窄

**T2.1 — Phase 2 注册表与分类器**

9 个 `#[ignore]` 的验收测试各自写明了缺失 API。实现 `ClaimRevisionRegistry`、`classify_claim_change`（CI-01..CI-13）、`RelationTypeRegistry`、`ProvenanceGraph` 与 `EvidenceIndependence::validate`，可把这 9 个 ignore 转成真实测试，并完成 DM2-01..DM2-14。

**T2.2 — 给现有闸门接 CI**

GAP-08 与 GAP-09 都是在红灯状态下进入 `main` 的，因为 PR 上只跑 `rust-phase1.yml`。把 schema 审计、protocol index 检查、一致性套件接进 CI 很小，且能防止复发。它不增加能力，但能阻止"测量成为唯一探测器"。

### 第三层 — 被阻塞，不得作为实现派工

| 工作 | 被什么卡住 | 解锁条件 |
|---|---|---|
| BMCP 传输/服务端 | H 尚未冻结传输契约 | H 决定 |
| Agent Integration RT-01..RT-09 | 同上，另加 D 与 I 闸门 | H + D + I |
| 40 行归属 `D` 的 context | 发布权威 | T1.1 |
| 8 行归属 `I` 的 context | 授权权威 | I 决定 |

为这些派工实现只会产出无法合并的工作。它们需要的是决定，不是代码。

## 4. 建议

**先 T1.1，再 T1.2，然后 T2.1/T2.2。** 第三层不得作为实现派工。

先做 T1.1 而不是更大的 T1.2，理由是：T1.1 是单个 trait 实现，却同时解锁 40 行归属 `D`、编译器、以及 Agent Integration 第 3–6 步。T1.2 的 19 行各自小且独立，可以与 T1.1 并行推进，也应该并行。

若 T1.1 确实卡在某个没人做出的决定上——即**持久发布记录究竟是什么**——那么该决定就是最高价值的事，因为它是最大一块工作前面的唯一闸门。

## 5. 对既有估计的更正

| 领域 | 所述 | 实测 |
|---|---|---|
| Memory Compiler | 85% 未实现 | `compile` 约 100% 不可达；准入/注册表/fence 已实现并测试（58 测试）。缺：生产权威、Store 层 prepare/publish 暴露 |
| Memory Context | 80% 未实现 | 77 行表：9 已实现 / 43 部分 / 25 缺失。19 行可本地做，40 行等 D |
| Agent Integration | 90% 未实现 | 对运行时而言准确；但阻塞来自 H/D/I，而非努力不足。RT-01..RT-09 全部 NOT RUN |
| BMCP | 60% 未实现 | 产物可观（32 schema、545 一致性测试）。传输/服务端完全缺失——那是一个二进制，不是一个百分比 |
| Phase 2 领域 | 100% 未启动 | **不成立。** 类型与不变量已实现，36 单元 + 11 验收测试；9 个因缺失注册表而 ignore |
| 端到端 | 100% 未启动 | 部分不成立。`brain-cli` 已端到端跑通摄取 → 存储 → 上下文，止于编译器跳过（GAP-07） |
