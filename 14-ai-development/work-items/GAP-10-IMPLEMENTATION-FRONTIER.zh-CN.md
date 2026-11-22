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

`crates/memory-domain` 的 Claim 身份分类器已由 PR #545 实现，公开函数为
`claim_identity::classify`。其余被 ignore 的验收测试仍指向其他缺失能力，
例如 `ClaimRevisionRegistry`、`RelationTypeRegistry` 和 `ProvenanceGraph`；
`classify_claim_change` 并不是实际 API 名称，不得继续计为缺失符号。

因此 Phase 2 的现状是"类型、不变量和 Claim 身份分类已实现；部分注册表与图能力仍缺失"。
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

**T2.1 — Phase 2 注册表与剩余图能力**

Claim 身份分类器已由 PR #545 实现，函数名是
`claim_identity::classify`，不是 `classify_claim_change`。本工作项将
`dm2_03` 改为真实验收测试，使用 `ClaimRevision::initial` /
`ClaimRevision::successor` 构造输入，覆盖 10 条可达向量：CI-01..CI-04、
CI-07..CI-11 和 CI-13。CI-05、CI-06、CI-12 因 `ClaimRevision` 没有
quantifier、modality、confidence 字段而不可达，不得计为已覆盖。

其余被 ignore 的验收测试针对其他缺失 API，包括 `ClaimRevisionRegistry`、
`RelationTypeRegistry`、`ProvenanceGraph` 和
`EvidenceIndependence::validate`。这些能力与已经存在的 Claim 身份分类器
是不同缺口。

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
| Phase 2 领域 | 100% 未启动 | **不成立。** 类型、不变量和 `claim_identity::classify` 已实现；`dm2_03` 覆盖 10 条可达 CI 向量。CI-05/06/12 因 `ClaimRevision` 类型形状不可达；其他注册表/图能力仍有缺口 |
| 端到端 | 100% 未启动 | 部分不成立。`brain-cli` 已端到端跑通摄取 → 存储 → 上下文，止于编译器跳过（GAP-07） |

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
