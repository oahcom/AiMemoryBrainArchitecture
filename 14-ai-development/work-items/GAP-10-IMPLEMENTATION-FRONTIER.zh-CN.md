# GAP-10 · 实现前沿：每个领域究竟卡在什么上

**状态**：未关闭 — 本文是地图，不是缺陷
**领域**：跨领域
**目的**：用依赖排序的实现前沿，替换六个未测量的完成度百分比

## 为什么写这份文档

一份要求"推进关键缺失工作"的指令列出了六个领域及完成度估计：Memory Compiler 85% 未实现、Memory Context 80%、Agent Integration 90%、BMCP 60%、Phase 2 领域模型 100% 未启动、端到端 100% 未启动。

对照仓库实测，这六项中有三项明显不准，而且这六项并非并列——它们构成一条链：多数剩余工作被两个上游权威卡住（D 发布权威、H 传输冻结），因此"六路同时推进实现"会产生无法合并的工作。

本文用计数替换百分比，并按"真正未被阻塞"来排序。

## 1. 实测状态（在 `main @ caa37a7` 上核验）

> **修订说明**：本节早先版本测的是 `main @ 76b6470e`，并据此断言
> `PublicationAuthority` 有三个实现、全部位于 `#[cfg(test)]`，因而是
> "THE CHOKEPOINT"。该结论已不成立。`main` 在一天内先后推进了 #523、#545、
> #555、#570，§2 已相应重写，那个卡点已经关闭。

### 1.1 生产代码零桩

```sh
grep -rn "todo!\|unimplemented!" --include=*.rs crates/
```

3 处命中全部位于 `crates/memory-domain/tests/phase2_acceptance.rs`，且在 `#[ignore]` 的测试体内（607、872、880 行）。

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

`crates/memory-domain` 有 36 个单元测试加 20 个验收测试，其中 3 个被
`#[ignore]`。二十个中有九个已由 `main` 上的 #570（三个注册表/解析器加
`dm2_03` 向量）与 #574（`RelationTypeRegistry`、`scope_refs`）关闭。

因此 Phase 2 的现状是"类型与不变量已完成；三个关注点被刻意留开"。剩下三个
都需要决策，而不是代码：

| 测试 | 保持 ignore 的原因 | 需要什么才能关闭 |
|---|---|---|
| `dm2_06` | 跨 Owner 决策 `B-P2-XO-01`（§8 标 PENDING，§9 标 `PLACEHOLDER ONLY`） | 一个 Owner 决策 |
| `dm2_11` | Provenance DAG 为 `NOT TYPED`（§9） | 一个规格决策 |
| `dm2_12` | 同上 | 一个规格决策 |

三个都无法靠写代码关闭。`dm2_11`/`dm2_12` 需要
`phase-2-domain-extension.md` §9 先把 DAG 类型化、§7 先定下 cycle/compaction
策略；`dm2_06` 需要 `B-P2-XO-01` 有结论，且 §8 禁止推断授权。真正属于普通
实现工作的两项（`dm2_08`、`dm2_09`）已由 #574 完成。

Phase 3 是另一个问题，本文不涉及。

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
Phase 2 领域类型            已完成（剩 3 个 ignore，全部被决策阻塞）
        |
        v
memory-storage / memory-store  已完成，含 hidden prepare / explicit publish（#523）
        |
        v
memory-context                 77 行表：9 已实现，43 部分，25 缺失
        |                      其中 19 行可本地实现
        v
PublicationAuthority          已完成。AdmissionPublicationAuthority 是生产代码，
        |                      读持久准入台账，brain-cli 正在使用它。
        +--> memory-compiler::compile 可达  <-- brain-cli 已在调用
        +--> 25+43 行中 40 行解锁
        +--> Agent Integration 第 3-6 步解锁
        |
        v
BMCP 传输 + 服务端   <-- 不存在；现在是唯一剩下的咽喉点
        |
        v
端到端（brain-cli 越过上下文组装）
```

**`PublicationAuthority` 不再是咽喉点。** 截至 `main @ caa37a7`，有两类实现：

| 实现 | 位置 | 支撑 |
|---|---|---|
| `AdmissionPublicationAuthority` | `publication_authority.rs:50` | 持久准入台账 + storage prepare 行 |
| `EvidenceAuthority`、`TestAuthority`、`RecoveryAuthority` | `lib.rs:921/940/1355` | `#[cfg(test)] mod tests` |

`AdmissionPublicationAuthority` 不是测试替身。它接收 `AdmissionStore` 与
`&dyn MemoryStorage`，只读已提交行，生产者身份与 scope 边界取自持久准入请求，
而不是调用方传入的布尔值。`crates/brain-cli/src/main.rs:280` 用它构造
`MemoryCompiler` 并调用 `compile`，随后无条件向 stderr 报告
`published` / `blocked` / `suppressed`。GAP-07 (b)（"跳过不可见"）已由 sidecar
文件加二进制级测试 `crates/brain-cli/tests/compiler_skip_is_visible.rs` 关闭。

**唯一剩下的咽喉点是 BMCP 传输 + 服务端。** 它卡住 Agent Integration 与端到端
路径，而它以上的部分都不再卡住。

这就是"六路同时推进"行不通的原因：六项里有五项汇聚到同一个缺失的传输层。
早先的读法——汇聚到一个缺失的 trait 实现**加上**一个缺失的传输层——在
`76b6470e` 上成立，现在已解决了一半。

## 3. 现在真正未被阻塞的工作

按依赖排序。每一项今天就能派工，无需任何外部决定。

> **部分已被取代。** 下面的 T1.1 已由 `AdmissionPublicationAuthority` 与
> `brain-cli` 接线完成，见 §2 与 §8。T1.2、T2.2 仍然开放；T2.1 只剩决策项。

### 第一层 — 解锁最多下游

**T1.1 — 生产版 `PublicationAuthority`（GAP-07 方向 (a)）— 已完成**

由 `AdmissionPublicationAuthority` 关闭。它接收 `AdmissionStore` 与
`&dyn MemoryStorage`，只读已提交行，生产者身份与 scope 取自持久准入请求而非
调用方布尔值。`crates/brain-cli/src/main.rs:280` 用它构造 `MemoryCompiler`
并调用 `compile`，无条件向 stderr 报告 `published` / `blocked` /
`suppressed`，另有 sidecar 文件与二进制级测试
（`compiler_skip_is_visible.rs`）保证跳过不会被漏看。

`MemoryStore` 仍未暴露 `prepare_version` / `publish_prepared`。这已不再是
`compile` 的阻塞（权威直接读 storage），但仍是 Store 抽象上的一个洞；诚实的
说法是"咽喉点被绕过了"，而不是"抽象补完了"。

**T1.2 — 19 行可本地实现的 Memory Context**

在覆盖表中以 `本线程可做` 标出。值得注意的几项：候选集边际覆盖优化器、预算/充分性可观测性、投递尝试账本、带谱系安全输出的 Compact 操作。

这些不需要外部权威，且可独立测试。

### 第二层 — 已解锁但范围较窄

**T2.1 — Phase 2 注册表与剩余图能力**

Claim 身份分类器已由 PR #545 实现，函数名是
`claim_identity::classify`，不是 `classify_claim_change`。本工作项将
`dm2_03` 改为真实验收测试，使用 `ClaimRevision::initial` /
`ClaimRevision::successor` 构造输入，覆盖 10 条可达向量：CI-01..CI-04、
CI-07..CI-11 和 CI-13。CI-05、CI-06、CI-12 因 `ClaimRevision` 没有
quantifier、modality、confidence 字段而不可达，不得计为已覆盖。

其余被 ignore 的验收测试全部被决策阻塞，没有一项是实现工作：

| 测试 | 关闭条件 |
|---|---|
| `dm2_06` | Owner 决策 `B-P2-XO-01`；§8 禁止推断授权 |
| `dm2_11`、`dm2_12` | 规格决策 — §9 标 Provenance DAG `NOT TYPED`，§7 未定 cycle 策略 |

`ClaimRevisionRegistry`、`AcceptedRevisionState`、`ClaimRevisionResolver`
已由 #570 落地；`RelationTypeRegistry` 与 `scope_refs` 已由 #574 落地。
`EvidenceIndependence::validate` 在当前任何 ignore 理由中都不是被点名的阻塞项。

**T2.2 — 给现有闸门接 CI**

GAP-08 与 GAP-09 都是在红灯状态下进入 `main` 的，因为 PR 上只跑 `rust-phase1.yml`。把 schema 审计、protocol index 检查、一致性套件接进 CI 很小，且能防止复发。它不增加能力，但能阻止"测量成为唯一探测器"。

### 第三层 — 被阻塞，不得作为实现派工

| 工作 | 被什么卡住 | 解锁条件 |
|---|---|---|
| BMCP 传输/服务端 | H 尚未冻结传输契约 | H 决定 |
| Agent Integration RT-01..RT-09 | 同上，另加 D 与 I 闸门 | H + D + I |
| 40 行归属 `D` 的 context | ~~发布权威~~ 发布**记录**的形状 | `AdmissionPublicationAuthority` 已解锁 `compile`；这 40 行仍需一个经 `MemoryStore` 暴露的持久发布记录 |
| 8 行归属 `I` 的 context | 授权权威 | I 决定 |
| `dm2_06` | 跨 Owner 决策 `B-P2-XO-01` | Owner 决策 |
| `dm2_11`、`dm2_12` | Provenance DAG 为 `NOT TYPED`（§9） | 规格决策 |

为这些派工实现只会产出无法合并的工作。它们需要的是决定，不是代码。

## 4. 建议

**T1.1 已完成。接下来做 T1.2，然后 T2.2，然后是决策项。**

T1.2 的 19 行各自小且独立，不需要外部权威，是唯一一块既有分量、今天又能派工
的工作。T2.2（接 CI）不增加能力，但能阻止"测量成为唯一探测器"——正因为便宜，
值得早做。

第三层里需要决策的四项，应当作为决策上报。把它们当作实现来派工，正是 #573
的成因：那个 PR 重新实现了 #570 已经落地的内容，因为没人在写代码前重测
`main`。

## 5. 对既有估计的更正

| 领域 | 所述 | 实测 |
|---|---|---|
| Memory Compiler | 85% 未实现 | `compile` 现已通过 `AdmissionPublicationAuthority` 与 `brain-cli` 可达；准入/注册表/fence 已实现并测试。缺：`MemoryStore` 未暴露 prepare/publish |
| Memory Context | 80% 未实现 | 77 行表：9 已实现 / 43 部分 / 25 缺失。19 行可本地做，40 行等一个持久发布记录 |
| Agent Integration | 90% 未实现 | 对运行时而言准确；但阻塞来自 H/D/I，而非努力不足。RT-01..RT-09 全部 NOT RUN |
| BMCP | 60% 未实现 | 产物可观（32 schema、545 一致性测试）。传输/服务端完全缺失——那是一个二进制，不是一个百分比 |
| Phase 2 领域 | 100% 未启动 | **不成立。** 类型、不变量、`claim_identity::classify`、`ClaimRevisionRegistry`、`AcceptedRevisionState`、`ClaimRevisionResolver` 均已实现。剩 3 个 ignore，全部被决策阻塞（§1.2） |
| 端到端 | 100% 未启动 | **不成立。** `brain-cli` 已端到端跑通摄取 → 存储 → 上下文 → 编译器，包括发布闸门与可见的跳过 |

## 6. 在 `b29278a8` 上的重测（2026-11-22 02:05 +08:00）

本节是追加内容。它不修改上方 §1–§5，只记录那些章节写就之后发生变化的部分，
以及一个无法对上的数字。

### 6.1 测试总数变了

```
$ cargo test --workspace --all-targets
TOTAL passed=385 failed=0 ignored=10
```

逐 crate 单独测量：

| crate | 通过 |
|---|---|
| agent-integration | 33 |
| bmcp-protocol | 46 |
| brain-cli | 5 |
| memory-compiler | 59 |
| memory-context | 77 |
| memory-domain | 47 |
| memory-event-store | 2 |
| memory-event-store-sqlite | 31 |
| memory-storage | 3 |
| memory-storage-sqlite | 59 |
| memory-store | 23 |

### 6.2 有一个数字对不上，记录为未解决

本目录另一份文档记录 `1ebbab84` 上 **371 passed**。我在 `b29278a8` 上测得
**385**。#541 自身 diff 新增 19 个 `#[test]`，而 371 + 19 = 390 ≠ 385。所以两个
数字统计的是不同的目标集，或者其中之一是错的。此处不解释抹平，只做标注，让下一个
人重新推导而不是继承。

### 6.3 依赖图多了一条消费链接，没有减少

从 `crates/*/Cargo.toml` 实测：

```
agent-integration          -> memory-context, memory-domain
bmcp-protocol              -> NONE
brain-cli                  -> memory-domain, memory-storage-sqlite, memory-store,
                              memory-context, memory-compiler
memory-compiler            -> memory-domain, memory-event-store, memory-event-store-sqlite
memory-context             -> memory-domain, memory-event-store-sqlite, memory-store,
                              memory-storage, memory-storage-sqlite
memory-domain              -> NONE
memory-event-store         -> memory-domain
memory-event-store-sqlite  -> memory-domain, memory-event-store
memory-storage             -> memory-domain
memory-storage-sqlite      -> memory-domain, memory-storage
memory-store               -> memory-domain, memory-storage, memory-storage-sqlite

无任何使用者：  agent-integration, bmcp-protocol
唯一二进制：    brain-cli
```

上方 §1.5 与 §2 仍然成立：`brain-cli` 依旧既不 import `agent-integration`
也不 import `bmcp-protocol`。

### 6.4 Tier 1 第 2 项改变了形状

GAP-06 没有被 #541 关闭。#541 在既有的 *namespace* 围栏（`forget_fence`，主键
`namespace_key`）之外，新增了一套 *target* 围栏（`canonical_forget_fences`，主键
Memory/Version），位于不同 crate，且没有对账路径。
`forget_api_absence_is_detectable` 仍然通过 —— 而这正是它被写出来要检测的缺陷。
测量与关闭条件见 `GAP-11-FORGET-FENCE-SPLIT-AUTHORITY.md`。因此 Tier 1 第 2 项
不是"把围栏接进去"，而是"先决定哪一套围栏是权威，再删除另一套"。

### 6.5 闸门未变，其中一个现在可测量

- `08-bmcp-protocol/scripts/check_protocol_index.py` → `missing=0 extra=0
  duplicate_types=0 invalid_rows=0 PASS`。
- `08-bmcp-protocol/schemas/test_nonempty_audit.py` → **exit 1**，5506 条未登记
  约束（GAP-09，未变）。
- `python3 -m unittest discover -s tests/conformance` → **Ran 493 tests**，
  6 errors，27 skipped。6 个 error 全部是
  `ModuleNotFoundError: No module named 'rfc8785'`，即未安装的已声明依赖
  （`requirements.txt` 锁定 `rfc8785==0.1.4`），不是代码缺陷。在 #540 之前，
  这条命令发现 0 条测试并因 ImportError 直接死掉。
- #546 已声明 GAP-08 报告的 Node 依赖；值得复验那三个 `.mjs` 引用在干净检出上
  是否已可解析。

### 6.6 CI 依然什么都不评估

#541 head commit 与 `main` 上的四个 check run 携带同一条注解，原文：

> The job was not started because recent account payments have failed or your
> spending limit needs to be increased.

`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` →

```
403 — Upgrade to GitHub Pro or make this repository public to enable this feature.
```

本文中每一处"绿"都是本地测量。没有任何一项经过 workflow 检查。

## 7. 在 `dba34a35` 上的重测（2026-11-22 03:05 +08:00）

同样是追加。§1-§6 未改动。自 `b29278a8` 以来 main 上有六处变化，其中一处
使一条 `#[ignore]` 理由变成假的，而不是关闭了一个缺口。

### 7.1 测试总数变了，ignore 数的变化是错的原因

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets
binaries: 26
TOTAL passed=438 failed=0 ignored=9
```

§6.1 在 `b29278a8` 记录的是 385 / 0 / 10。+53 通过是真实的工作量。10 → 9
**不是**转化了一条测试：见 §7.2。

同一轮运行的按 crate 拆分：

| crate | 单元 | 集成 |
|---|---|---|
| agent-integration | 36 | 2 + 19 |
| bmcp-protocol | 42 | 4 |
| brain-cli | 1 | 4 |
| memory-compiler | 62 | 1 |
| memory-context | 68 | 8 + 1 |
| memory-domain | 55 | 11（+9 ignored） |
| memory-event-store | 2 | — |
| memory-event-store-sqlite | 18 | 5 + 2 + 6 |
| memory-storage | 3 | — |
| memory-storage-sqlite | 60 | — |
| memory-store | 15 | 6 + 3 + 2 |

§6.2 标记的 `371 vs 385` 分歧在这里也没有解决。现在能确定的是：§6.1 的表与
本表统计的目标集合不同——`--all-targets` 包含集成二进制，而 §6.1 的数字与
只跑 `--lib` 一致。

### 7.2 dm2_03 已改为覆盖现有分类器的真实验收测试

PR #545（合并提交 `444deef1`）新增了
`crates/memory-domain/src/claim_identity.rs`，并通过公开导出提供
`claim_identity::classify`。分类器不是缺失 API，本工作项不修改其实现。

当前 `dm2_03_ci_classification_vectors` 已处于启用状态，但此前版本使用
JSON 修改辅助函数，未通过规范构造器完整覆盖可达 CI。本工作项改用真实的
`ClaimRevision::initial` / `ClaimRevision::successor`，断言 CI-01、CI-02、
CI-03、CI-04、CI-07、CI-08、CI-09、CI-10、CI-11、CI-13（可达维度 10/10）。

CI-05、CI-06、CI-12 不伪装成通过测试。`ClaimRevision` 结构体没有
quantifier、modality 或 confidence 字段。字段形状检查命令：

```sh
sed -n '/^pub struct ClaimRevision {/,/^}/p' crates/memory-domain/src/lib.rs | grep -En '\\b(quantifier|modality|confidence)\\b'
```

预期结果：无输出；由于结构体内不存在这些字段，`grep` 退出码为 1。
这三条是当前类型下不可达，而不是已覆盖。

分类器将任何 qualifier 变化都归为
`QualifierSubstantivenessUnprovable`，必须显式进入治理决策，不得猜测为
`NewClaim` 或 `NewRevision`。测试还验证规范化后仅显示标签变化时结果为
`NewRevision/LabelOnly`。

### 7.3 GAP-07 的缺口陈述现在是假的；它的闭环条件只满足一半

> **状态更正（2026-11-22）：** 所引 GAP-07 缺口陈述已被 PR #552 及后续生产集成取代。`AdmissionPublicationAuthority` 现提供生产实现，`brain-cli` 通过非测试路径调用 `MemoryCompiler::compile()`。GAP-07 因此**就生产可达性而言已关闭**——其四条闭环标准均已在 `main @ 87d503ba` 核实。发布成功与持久发布权威仍未解决，另登记于 `GAP-14-PUBLICATION-AUTHORITY-AND-STORE-LIFECYCLE.md`（A：门面未暴露 prepare/publish；B：三个标志在 D3 下无签发者；C：持久性未验证）。以下正文保留为产生本次更正的测量记录。

GAP-07 §1.2 原文称 `compile` "no production implementation of its required
`PublicationAuthority` trait, and no non-test caller"。两半现在都错了：

```
$ grep -rn "impl.*PublicationAuthority for" --include=*.rs crates/
crates/memory-compiler/src/lib.rs:921:  impl PublicationAuthority for EvidenceAuthority      (cfg(test))
crates/memory-compiler/src/lib.rs:940:  impl PublicationAuthority for TestAuthority          (cfg(test))
crates/memory-compiler/src/lib.rs:1355: impl PublicationAuthority for RecoveryAuthority      (cfg(test))
crates/memory-compiler/src/publication_authority.rs:50:
        impl PublicationAuthority for AdmissionPublicationAuthority<'_>   (生产)
```

`brain-cli/src/main.rs:4` 引入 `memory_compiler::publication_authority::AdmissionPublicationAuthority`，
在第 245 行构造，`run_compiler_stage` 在第 285 行调用 `compiler.compile(...)`。
一次真实运行：

```
$ brain compile --input fixtures/event.json --out ctx.json --verbose
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed;
  false flags: [canonical_commit_confirmed, publication_participant_admitted,
                protected_visibility_authorized]
EXIT=0
```

对照 GAP-07 自己的闭环条件：

1. **满足** — 存在生产权威，且有一条非测试路径调用 `compile`。
2. **满足** — `crates/brain-cli/tests/compiler_skip_is_visible.rs`，4 个测试，
   启动构建出的二进制，断言提示在 stderr 上恰好出现一次、在 sidecar 里出现
   一次，且退出码为 0。
3. **满足** — 提示是无条件的，不在 `--verbose` 之内。
4. **不满足，且这是唯一还站着的** — GAP-07 仍在用现在时描述自己为 open，
   而它的主语已不存在。

三个 `false` 标志不是 bug。`OWNER-DECISION-PUBLICATION-RECORD-001` D3 规定该
适配器 "never computes, infers, defaults or substitutes a flag"，
`compiler-stage-contract.md` §8 规定 "E MUST NOT implement substitute
authorization decisions"。在没有权威签发者时报 `false` 是必需行为。因此这次
运行是**正确地拒绝发布**，与"该阶段没有运行"是两种不同的结果。

这正是 GAP-10 §5 想抓的那类文档缺陷：关于现在的陈述过期了，被继承而不是
被重新推导。

### 7.4 E2E 的说法从"假"变成"到发布闸门为止为真"

§5 关于 E2E 的那行写 "`brain-cli` runs ingestion → storage → context end to
end. It stops at the compiler skip"。现在的路径跑的是 ingestion → extraction →
normalization → staging → `compile` → 取证明 → 拒绝。比 §5 记录的多了两个
阶段，且拒绝是来自真实权威的真实决定，不是跳过。

仍然缺的是**一次成功的发布**。仓库里没有任何东西能产出 `Published`
处置，因为三个证明字段没有签发者。没有任何非测试路径的测试断言过
`PublicationDisposition::Published`。

### 7.5 双语门禁被未跟踪的构建产物污染

```
$ BASE_SHA=HEAD~1 HEAD_SHA=HEAD python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 08-bmcp-protocol/.pytest_cache/README.md
::error::New bilingual gap outside frozen baseline: 08-bmcp-protocol/tests/conformance/.pytest_cache/README.md
EXIT=2
```

两个路径都是未跟踪的（`.gitignore` 第 6 行有 `.pytest_cache/`），而
`current_bilingual_gaps()` 用 `root.rglob("*.md")` 走文件系统，不是
`git ls-files`。所以任何一次本地 pytest 都会让门禁在 CI 里不可能存在的文件
上变红。移除它们后：

```
bilingual baseline: 77 frozen, 0 new gaps
EXIT=1   （只剩 PR body 的 manifest 错误）
```

这不是新缺口，是**可复现性缺陷**：门禁的答案依赖未跟踪的本地状态，因此
"门禁通过"不是关于该提交的陈述。

### 7.6 77 条基线没动，其形状现在完全归因

`current_bilingual_gaps()` 本地返回 79，干净树上返回 77。干净树的分布：

| 根 | 缺口 | 说明 |
|---|---:|---|
| `13-engineering-decisions` | 58 | 58 个 `.md`，0 个 `.en.md`，0 个 `docs/en` 镜像 |
| `06-memory-context` | 10 | |
| `08-bmcp-protocol` | 6 | |
| `14-ai-development` | 4 | 全是 `research/phase-0/SESSION-*.md` |
| `00-governance` | 1 | `reports/gov-doc-001-full-scan-2026-11-20.md` |

`13-engineering-decisions` 是**它自己子树的 100%**，占整个基线的 75%。
`PAIR_EXEMPT_PREFIXES` 覆盖 14 下的 `work-items/`、`prompts/`、`adr/`，13 下
一个都没有；`EMBEDDED_BILINGUAL_SOURCES` 共 21 条，13 下**零条**。所以整个根
之所以在基线里，是因为从未为它创建过门禁认可的任何形态——与 GAP-10 §1 和
登记 015 为 77 条确立的机制相同，现在定位到单个根。

`14-ai-development/governance-register/` 有 31 个 `.md` 却**不在**基线里：19 个
有 `docs/en` + `docs/zh-CN` 镜像，剩下 12 个是并排配对（`README.md` +
`README.en.md`，以及五对 `GOV-NC-2026-11-20-*`）。`side_by_side_partner()`
全部解析得到。这是机制按设计工作，也是 §7.5 的反例：登记目录干净，因为它的
文件被跟踪、配对是真实的。

## 8. 整个工作区可以构建、测试全绿（2026-11-22 12:00 +08:00）

本节存在的原因：§7 以及它之前的若干 PR 正文都断言过一件在本机上并不成立的
事——六个 crate 因为 `libsqlite3-sys`（bundled）需要 C 编译器而无法构建。

那是**测量错误，不是环境限制。** 机器上一直有一个可用的 C 编译器。

### 8.1 真正坏在哪里

`~/.local/bin/gcc.exe` 是真正的 MinGW-w64 GCC 14.2.0，但它的 `libexec` 目录
缺失，所以 `cc1` 无法被拉起：

```
$ gcc t.c -o t.exe
gcc.exe: fatal error: cannot execute 'cc1': CreateProcess: No such file or directory
```

`gcc -print-search-dirs` 仍指向
`~/.local/libexec/gcc/x86_64-w64-mingw32/14.2.0/`，而该目录不存在。于是 `cc`
在 `PATH` 上、能报版本号、却在第一个编译单元上失败——这是最坏的失败形态，
因为版本检查会说它正常。

MSVC 确实缺失（无 `link.exe`），这就是 `+stable-x86_64-pc-windows-msvc` 也
失败的原因。

### 8.2 已经装好的东西

`%LOCALAPPDATA%/Temp/zigpkg/ziglang/zig.exe`（190 MB）处有一套完整的 Zig
工具链，另有 `2026-11-18-13-49-20/_l0probe/zigcc.exe`——一个早先探测留下的
`zigcc` 包装器，它启动 `zig cc -fno-sanitize=all` 并转发参数。

§7 自己的命令行已经在用它：

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets
TOTAL passed=438 failed=0 ignored=9
```

也就是说 §7 记录了可用的调用方式，紧接着其正文又声称工作区无法构建。这两句
从未被对上。

`zigar` 并不存在，用同一套包装器模式补上：

```c
nv[n++] = "C:/Users/Administrator/AppData/Local/Temp/zigpkg/ziglang/zig.exe";
nv[n++] = "ar";
```

### 8.3 实测结果

```
$ CC=<zigcc> AR=<zigar> cargo test --workspace --all-targets --offline
TOTAL passed=476 failed=0 ignored=3
```

| crate | 通过 | ignore |
|---|---:|---:|
| agent-integration | 57 | 0 |
| bmcp-protocol | 48 | 0 |
| brain-cli | 6 | 0 |
| memory-compiler | 66 | 0 |
| memory-context | 91 | 0 |
| memory-domain | 77 | 3 |
| memory-event-store | 2 | 0 |
| memory-event-store-sqlite | 38 | 0 |
| memory-storage | 3 | 0 |
| memory-storage-sqlite | 62 | 0 |
| memory-store | 26 | 0 |
| **合计** | **476** | **3** |

3 个 ignore 就是 §1.2 里那三个被决策阻塞的 `dm2_06`、`dm2_11`、`dm2_12`。
工作区其余测试全部运行。

同时全绿：

```
cargo clippy --workspace --all-targets -- -D warnings   # clean
cargo fmt --all -- --check                              # clean
```

### 8.4 为什么这不只是一个数字

有三个 PR（#573、#574、#581）被收窄到 `memory-domain`，其正文告诉审阅者
"六个 crate 在本机无法构建"。那条免责声明是错的，它让这些 PR 显得比实际更小、
更不可验证。正确的表述一直存在：整个工作区可以构建，任何关于
`memory-compiler` 或 `brain-cli` 的主张都能本地核验。

教训具体且值得记下：**一个能报版本号却编不出东西的编译器，比没有编译器更糟**，
因为所有"装了吗"的检查都会通过。能抓到它的检查是一个编译单元，不是 `--version`。

### 8.5 这没有改变什么

§8 以上的内容无一失效。§2 的咽喉点分析、§1.3 的归属计数、§1.2 的决策阻塞项
全部成立。改变的是"工作区在本机不可构建"这一主张——它是错的，而且它正是若干
PR 验证不足的原因。

环境修复没有进入仓库：`CC`/`AR` 按次传入，没有 vendored 工具链。未来的贡献者
仍会撞上坏掉的 `gcc`，除非知道要覆盖它。把可用的调用方式记在本节，是唯一
持久化的产物。

## 9. 在 `d89fd5fa8` 处的重测（2026-11-22 12:30 +08:00）

仍然是增量。§1-§8 未改动。本节存在的原因是：原始请求里的六个百分比被第四次重述，
而 §8 自己的数字在落地时就已经过期。

观测时间 `2026-11-22T04:29:28Z`，树 `d89fd5fa8`。

### 9.1 整个工作区全绿，ignore 降到一条

```
$ CC=<zigcc> AR=<zigar> cargo test --workspace --all-targets --offline
TOTAL passed=503 failed=0 ignored=1
$ cargo clippy --workspace --all-targets -- -D warnings   # clean
$ cargo fmt --all -- --check                              # clean
```

§8.3 在 `0ae644f32` 记录的是 `476 / 0 / 3`。在那一提交与本提交之间，
`fe9e25a5c` 落地了 `ProvenanceGraph` 与证据独立性，闭合了 `dm2_11` 与 `dm2_12`。

仅剩的一条 ignore 是 `dm2_06_missing_authorization_ref_blocks_fact_publication`。
它的原因不是缺 API：`FactRevision::initial` **要求**一个 `AuthorizationDecisionRef`，
而唯一公开构造是 `AuthorizationDecisionRef::pending_i()`。要证明"缺失授权会被拒绝"，
需要能区分"不存在"与"I 已签发"的类型状态，而 `phase-2-domain-extension.md` §8
禁止推断授权。所以这一条是决策阻塞，不是代码阻塞——与 §1.2 归入的类别相同，
只是现在该类只剩它一个成员。

### 9.2 六个百分比里有四个现在可测地是错的

| 领域 | 陈述值 | 在 `d89fd5fa8` 实测 |
|---|---|---|
| Memory Compiler | 85% 未实现 | `compile` 已通过生产版 `AdmissionPublicationAuthority` 从 `brain-cli` 可达。66 个测试。五个阶段都有入口。`Published` 仍不可达，原因有三个且都已具名（GAP-12/13/14），其中没有一条是"编译器还有 85% 没写"。 |
| Memory Context | 80% 未实现 | 77 行覆盖图的计数未变（9 已实现 / 42 部分 / 26 缺失），但该 crate 现在跑 **82 单测 + 17 集成 = 99 个测试**，此前是 68+9。覆盖图自代码移动后未重新归属；应视为行数过期，而非测试过期。 |
| Agent Integration | 90% 未实现 | **错。** 该 crate 现在运行时依赖 `memory-context` **与** `memory-domain`，`brain-cli` 已消费它（`crates/brain-cli/Cargo.toml:13`），并跑 36 单测 + 21 集成测试，其中 `context_snapshot_delivery.rs` 携带真实 `ContextSnapshot` 跨 crate 边界。#525 的前提已死。 |
| BMCP | 60% 未实现 | 协议产物充实；`bmcp-protocol` 有 44 单测 + 4 一致性测试。**在 `61b9d743` 修正：** 传输监听器确实存在（`crates/bmcp-server`，`lib.rs` 723 行，`:4` 处 `TcpListener`），所以"传输/服务端缺失"是错的。仍然成立的是：schema 声明 22 个 `message_type`，Rust 解析器 1 个，且监听器一个都触达不到——它唯一的 `bmcp_protocol` 引用是 `#[allow(dead_code)]`。见 GAP-16。 |
| Phase 2 领域模型 | 100% 未启动 | **错。** 70 单测 + 20 验收测试，1 条 ignore（`dm2_06`），决策阻塞。`ClaimRevisionRegistry`、`ClaimRevisionResolver`、`AcceptedRevisionState`、`RelationTypeRegistry`、`ProvenanceGraph`、`EvidenceIndependence` 与 `claim_identity::classify` 均已实现。 |
| 端到端 | 100% 未启动 | **错。** `brain-cli` 跑通 摄取 → 抽取 → 规范化 → 暂存 → `compile` → 取证明 → 上下文装配 → 适配器投递。`crates/brain-cli/tests/e2e_full_chain.rs` 断言了整条链，含持久化快照与拒绝通告。一个测试，3.6 秒，通过。 |

值得点名的规律：**这六个数字在某个更早的提交上都曾为真。** 它们不是谎言，是化石。
不重测就重述，才是它们变错的原因。

### 9.3 真正缺失的只有三件事

上述全部是已存在的代码。完全没有任何实现的、已规格化的工作，现在是：

1. **一次成功的 `Published` 处置。** 被三个无签发者的证明字段阻塞，各自已立项：
   GAP-12（canonical commit）、GAP-13（参与者准入，外部且三方）、
   GAP-14（存储生命周期加上另外两个）。
2. **BMCP 线映射，然后是 21 个解析器。** §9 原本写"`crates/` 里没有
   `TcpListener`"。这句话在 `61b9d743` 上已不成立：`crates/bmcp-server/src/lib.rs:4`
   正是 `use std::net::{SocketAddr, TcpListener, TcpStream};`，且该 crate 是
   workspace 成员。测量修正见 GAP-16。仍然成立的是更窄、也更有用的部分：
   该监听器只实现了一个 JSON-RPC 方法（`initialize`），且从不触达解析器——
   它整个 crate 里唯一的 `bmcp_protocol` 引用是一个 `#[allow(dead_code)]`
   格式化函数，注释写着"留给未来的证据校验调用点"。framing、session、handshake
   仍由 H 冻结，因此在现有 JSON-RPC/TCP 选择之上继续搭建，等于搭建在
   一个未记录的premise上。21 个解析器与"线到解析器"的路由不被任何决策冻结，
   可以推进。
3. **`dm2_06` 的授权类型状态。** §9 原本把它归入 `B-P2-XO-01`。它不属于那里——
   见 `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`，该裁定把"这份授权是否真实"
   （I 的问题，仍然开放）与"是否存在一份授权"（类型状态问题，已裁定）分开。

这才是诚实的前沿：一个决策阻塞的处置、一个未冻结的线映射、一个已裁定的
类型状态。不是六个百分比。

### 9.4 `13-engineering-decisions` 的双语缺口仍占基线 75%

§7.6 测到该单一 root 占 77 个缺口中的 58 个，至今未变：

```
$ BASE_SHA=HEAD~1 HEAD_SHA=HEAD python scripts/check_bilingual_docs.py
bilingual baseline: 77 frozen, 0 new gaps
```

`PAIR_EXEMPT_PREFIXES` 与 `EMBEDDED_BILINGUAL_SOURCES` 仍不覆盖
`13-engineering-decisions` 下任何内容。这不是代码缺陷，也不是文档缺陷；
是该 root 从未满足过的一种策略形态。记在此处，免得下一位读者重新推导。

### 9.5 两条治理记录在 main 上为红，其中一条是没落地的裁定

`GOV-DOC-002` 在 `main` 上恰好报两个错误，都是 `NO_AUTHORITATIVE_SOURCE`：

| scope | 声明文件 | 当前状态 |
|---|---|---|
| `memory-compiler/reading-guide` | `04-memory-compiler/README.md:15` | `Non-Canonical` |
| `protocol/bmcp-message-type-index` | `08-bmcp-protocol/protocol-index.md:14` | `Candidate` |

第一条是 Architecture Owner 已经裁定过的那一个。PR #496 以
`canonical_status: Non-Canonical` 合并了 root README，而裁定是
`Canonical / Informative`。合并没有携带裁定。修法是改一行元数据、并在两个镜像里
改同样一行——而这是一次内容权威性断言，不是代码改动，所以它需要所有者，而不是补丁。

第二条从未有过裁定。`protocol-index.md` 是在固定基线上审计生成的清单；
它对 message-type 命名空间究竟是**权威**，还是只是**关于**它的报告，尚未决定。

两条都记录在 #564。本文档不修复其中任何一条。

## 10. §9 的勘误，在 `61b9d743` 处实测（2026-11-22 13:30 +08:00）

上文 §9 未被编辑。它有两处陈述在写下时就是错的，另有一处在 `main` 前进后变错。
它们在此更正而非就地改写，因为一份测量值被静默重写的治理文档无法审计——
下一位读者分不清哪句是更正、哪句是原始断言。

### 10.1 `bmcp-server` 存在，而 §9 说它不存在

§9 第 2 条写道：

> `crates/` 里没有 `TcpListener`、没有 `hyper`、没有 `axum`。

在 `61b9d743` 上不成立。`crates/bmcp-server` 是 workspace 成员——`lib.rs` 723 行、
`main.rs` 67 行、`rt_scenarios.rs` 166 行——而它第四行就是：

```rust
use std::net::{SocketAddr, TcpListener, TcpStream};
```

这个错误的性质值得点名，因为它正是 §9 要诊断的那一类：**在未检查工件的情况下
报告缺失**。我当时是从一棵早于该 crate 的树上测量的 `crates/`。

### 10.2 修正后的 BMCP 结论更窄，也更有用

真实情况既不是"传输缺失"，也不是"传输已就绪"：

- 32 个 schema 声明了 22 个唯一 `message_type`，索引检查器通过
  （`unique_message_types=22`、`missing=0`、`extra=0`）。
- 其中**恰好一个**有 Rust 解析器：`parse_and_validate` 的返回类型点名
  `AppliedDeliveryEvidence`，而 `message_type` 检查是常量比较
  （`lib.rs:892-903`），任何其他类型都会得到 `WrongConst`。
- `bmcp-server` 只实现一个 JSON-RPC 方法（`initialize`），其余一律
  `-32601 Method not found`。
- `bmcp-server` 从不触达解析器。它整个 crate 里唯一的 `bmcp_protocol` 引用是：

```rust
// lib.rs:718-723
// This local formatter is available for a future evidence-validation call site.
#[allow(dead_code)]
fn describe(error: &bmcp_protocol::validate::EvidenceError) -> String {
```

`#[allow(dead_code)]`、"留给未来的调用点"、零个调用点。

所以：**监听器存在，而 22 个消息类型一个都到不了解析器。** 这是一个路由缺口
加上 21 个缺失解析器，不是一个缺失的二进制。21 个解析器是针对既有 JSON Schema
的转写，不被任何决策冻结。framing、session、handshake 仍由 H 冻结——
`TECH-REALITY-001-C/README.md:70` 仍写着 *"H wire mapping remains NOT FROZEN"*——
所以在现有 JSON-RPC/TCP 选择之上继续搭建，等于搭建在一个未记录的前提上。

完整测量见 GAP-16。

### 10.3 §9 把 `dm2_06` 归错了所有者

§9 第 3 条说 `dm2_06` "被 `B-P2-XO-01` 与 §8 的禁止推断授权阻塞"。后半句对，
前半句是混淆。

`B-P2-XO-01` 问的是*这份授权是否真实*——I 的问题，仍然开放。
`dm2_06` 问的是*是否存在一份授权*——类型状态问题。
`FactRevision::initial` 把 `AuthorizationDecisionRef` 作为**必填、非 `Option`**
参数（`memory-domain/src/lib.rs:831`），而该类型是单元结构体，唯一构造器是
`pending_i() -> Self(())`，因此它的任何值都不可能表示"缺失"。这就是负例写不出来
的原因，而它不需要 I 提供任何东西。

已由 `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` 裁定：三态
（`Absent` / `Placeholder` / `Issued`），只有 `Absent` 阻断，且该类型不得被命名为
"证明"。

### 10.4 §9 中未变的部分

四项被证伪的百分比、`503 / 0 / 1` 的测量、`13-engineering-decisions` 占 77 行中的
58 行、以及两个 `NO_AUTHORITATIVE_SOURCE` scope 属"退役"而非"提升"的裁定，全部不变。
§9 的核心主张——六个百分比是错误框架——被这些更正加强而非削弱：同一类错误
（报告状态而不重新测量）在同一份反对该错误的文档里出现了三次。
