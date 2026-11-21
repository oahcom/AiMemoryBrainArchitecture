# GAP-BASELINE-004 · 第六次独立测量

**测量者**：Verifier（不写代码，只派工、独立核验、合并）
**基线**：`main @ 950d66c3`
**测量时间**：2026-11-21 22:00 (+08:00)
**环境**：WSL2 Ubuntu 24.04，`cargo 1.95.0`，`gcc 13.3.0`，16 核
**方法**：`git archive HEAD | tar -x` 干净导出 → 原生 ext4 副本 → `cargo test --workspace --all-targets`

---

## 1. 实测数字

```
agent-integration    lib            12 passed
agent-integration    delivery_lifecycle 19 passed
bmcp-protocol        lib            42 passed
bmcp-protocol        p0_conformance  4 passed
brain-cli            main            1 passed
memory-compiler      lib            53 passed
memory-context       lib            68 passed
memory-context       e2e_negative    8 passed, 1 ignored
memory-context       e2e_store       1 passed
memory-domain        lib            36 passed
memory-domain        phase2_accept   11 passed, 9 ignored
memory-event-store   lib             2 passed
memory-event-store-sqlite lib       18 passed
memory-event-store-sqlite forget_fence 5 passed
memory-event-store-sqlite resilience   6 passed
memory-storage       lib             3 passed
memory-storage-sqlite lib            1 + 1 + 35 passed
memory-store         lib             4 passed
memory-store         cross_crate     6 passed
memory-store         sqlite_integration 2 passed
```

**合计：338 passed / 0 failed / 10 ignored**

上一轮（GAP-BASELINE-003，`main @ e236193`）：218 passed。

**增量：+120 测试，全部真实执行。**

---

## 2. 六项缺口的当前状态

| 缺口 | 起点 | 现在 | 关键证据 | 生产权威接入 |
|---|---:|---:|---|:---:|
| GAP-01 Memory Compiler | 31 tests | **53 tests** | `compile()` 读 `producer_receipt`；`producer_registry` 表；`ProducerNotRegistered` 与 `MissingProducerAdmission` 分离 | **NO** |
| GAP-02 Memory Context | 20 tests | **68 tests** + 8 E2E | ChangeSet 编辑器（6 操作）；Sufficiency 评估器（10 维度，2 可测）；`Unknown ≠ Insufficient` | **NO** |
| GAP-03 Agent Integration | 4 tests | **12 + 19 tests** | `DeliveryPayload::from_snapshot` 强制走 `validate_snapshot`；`ApplyOutcome`；`VersionGap` 独立于 `VersionMismatch` | **NO** |
| GAP-04 BMCP | 0 可执行 | **42 + 4 tests** | RecoveryJoin 1.0.2 schema；`minProperties` 审计；非空约束守卫脚本 | **NO** |
| GAP-05 Phase 2/3 领域模型 | 0 类型 | **36 + 11 tests** | `Fact`、`FactOutcome`、`EntityIdentityStatus`、`RelationDefinition`、`EvidenceExtension`；5 个 `compile_fail` 不变量 | **NO** |
| GAP-06 端到端 | 1 happy path | **8 + 1 + 1 tests** | 跨 crate 负路径；file-backed 重启持久性；混合 scope 拒绝 | **NO** |

**生产权威接入仍然是六项全 NO。** 这不是实现问题，是批准链问题：Schema / DDL / Public API / H Wire Format / production keys / Trust Root / Crypto Profile / Storage L4 approval 全部 `NOT APPROVED`。这一项在 338 个测试之后依然没有移动一格。

---

## 3. 本轮发现的真实缺陷（5 个）

### 3.1 Owner G 推送的文件无法编译（已修 `112f54b`）

PR #493 报告 68 个测试通过——**数字是真的**——但推送的 `memory-context/src/lib.rs` 末尾多了一行：

```
[executed on device: VM-0-9-ubuntu (d03d92fd-4b5d-4bc1-a701-985eb5de69cc)]
```

紧跟 test module 闭合大括号之后。`cargo build`：

```
error: expected at least one digit in exponent  --> lib.rs:3469:61
error: expected item, found `[`                --> lib.rs:3469:1
```

**这是本轮最重要的一条：它证明了「贴出测试输出」这个防线不够。** Owner G 的输出是真的，它跑的文件和它推的文件差了一行。删掉那行后 68 个测试确实全过。

Owner G 的修复不是改代码，是写 `scripts/precheck_delivery.py`：扫 `.rs` 末尾的工具标注污染 + 括号净差。它自己跑了 3 个测试并推了 PR #503。

### 3.2 Owner B 的模型改动打破了并发新增的验收测试（43 个错误）

时间线：

| 时间 | 事件 |
|---|---|
| 19:46 | Owner B 的 Round 3 基线 `8a7f81e`（`tests/` 目录不存在） |
| 20:43 | 另一个会话提交 `88bf4875`，新增 `phase2_acceptance.rs`（421 行，旧公开字段 API） |
| 20:47 | Owner B 的 Round 4 `c8f496ae`（私有字段 + 构造器） |

B 从 `8a7f81e` 起分支，那个时点 `tests/` 还不存在。它没有覆盖任何东西——是另一个会话的文件在它之后出现。

**43 个错误：`has no field named subject_ref`、`field claim_ref is private`、`no field claim_revision_ref`。**

处理：我没有回退 B，而是建 `integration/gap-05-canonical` 分支（main + B），让 B 在这个分支上迁移验收测试。B 迁移后 43 → 0，且把 4 个 `#[ignore]` 打开（parent mismatch、alias 不合并身份、relation 端点类型、evidence availability），全部通过。

### 3.3 Owner B 的 `Vec` 依据行号错了 15 行

B 引用「`domain-model-overview.md` 第 367 行，§8.1，item 3」。实际是**第 352 行**，章节标题是 `#### 3. Shared Fact visibility`（在 `§5 Forget` 之下，不是 §8.1）。

**引用内容正确，位置描述错误。** 原文确实支持多值：

> A FactRevision linked to multiple ClaimRevisions may remain visible only if every disclosed dependency is independently authorized and not suppressed by an applicable Forget decision.

裁定：保留 `Vec`。依据成立，行号错误不构成否决理由——但它说明一件事：**一个 Owner 引用文档时，引用的准确性需要独立核验，不能因为「它引了原文」就接受。**

### 3.4 我自己的 `git reset --hard` 第四次丢掉已合并的工作

- 第 1 次：丢 Owner C 的 adapter（`618862d`），C 指出
- 第 2 次：丢 Owner C 的 round-6 快照接入（`765f5cf`），C 再次指出
- 第 3 次：给 Owner B 的指令里写「从含你 Round 4 的 main 起分支」，而那个合并只存在于本地 `wip/merge-round9`，B 指出
- 第 4 次（本轮）：`git reset --hard origin/main` 在 `ef7f731`，再次丢 C 的工作

**我在 GAP-BASELINE-003 里把这个错误写下来了，然后我又犯了两次。写下来不等于改掉。**

流程修正（已生效）：任何 reset 之前先 `git branch -f wip/<round> HEAD`；合并后立刻从 `git archive` 干净导出跑全量，绿了才推。

### 3.5 双语文档门禁：我上一轮的判断是错的

我在 GAP-BASELINE-003 里写「英文-only 的 `X.zh-CN.md` 能通过 side-by-side 检查」。本轮实测：

```
A. 英文-only 的 side-by-side 对  -> bilingual? False   （被拒绝，我上轮说错了）
B. 含 1 个汉字的对             -> bilingual? True    （真的漏洞在这里）
```

`_side_by_side_bilingual()` 用 `_has_any_chinese()`，阈值是 **1 个 CJK 字符**。一段 6000 词的英文加一个「中」字就能通过。docstring 自己写了理由：

> One CJK character anywhere in either file is enough: a short but genuine translation must not be rejected for being brief.

**这个理由本身站得住**（短翻译不该因为短被拒），但它与「≥100 字符」的 `_carries_chinese()` 并存，意味着同一份文档走不同配对分支会有两个相差 100 倍的阈值。这是一个真实的策略不一致，不是实现 bug。

另外验证：`docs/en` + `docs/zh-CN` 双向镜像分支**完全不检查内容语言**——`mirrored = english.is_file() and chinese.is_file()`，只要两个文件存在就算配对。这一条我没有修，因为它属于治理策略，需要 Owner 裁定。

---

## 4. 架构分歧：GAP-03 的类型边界（已裁定）

PR #465（`52eae78`，`fix(agent-integration): distinguish delivery payload from Brain snapshot`）在我给 Owner C 下「用 `memory_context::ContextSnapshot` 替换本地类型」的指令之后，做了一次**相反方向**的决定，并合并进 main：

> This adapter-boundary payload is deliberately distinct from `memory_context::ContextSnapshot`, which is the Brain-side build artifact containing context identity, entries, and rendered-byte accounting.

**我的裁定：PR #465 是对的，但它的实现留了一个真实漏洞。**

- 分离是对的：`ContextSnapshot` 有 `identity`、`entries`、`tombstones`、`operation_records`、`rendered_bytes`——把 Brain 的内部记账结构暴露给 Agent 边界没有必要
- 漏洞是：`DeliveryPayload::new(version, content)` 是公开构造器，**任何调用者都能造一个与任何真实上下文无关的 payload**，`apply()` 只检查版本号连续

Owner C 的 Round 8 修复了这个漏洞：

```rust
pub fn from_snapshot(snapshot: &ContextSnapshot) -> Result<Self, AdapterError>
```

内部先 `validate_snapshot()` 再 `serialize()`，版本取 `context_version`。原 `new` 降为 `#[cfg(test)] fn new_for_test`。新增 `InvalidSnapshot { reason }`。

**这才是 Round 6 指令的真实意图**——不是改类型名，是让载荷无法伪造。

---

## 5. 仍然开放的问题

| 问题 | 状态 | 归属 |
|---|---|---|
| 生产权威接入（六项全 NO） | 未移动 | 批准链，非实现 |
| GAP-06 forget 路径 | `#[ignore]` + `GAP-06-FORGET-PATH-UNREACHABLE` 文档 | Owner A 已交付 |
| 9 个 `phase2_acceptance` ignore | 理由已指向具体缺失类型 | 需要 Phase 2/3 继续实现 |
| 8/10 Sufficiency 维度不可测 | 返回 `Unknown`，不返回 `Insufficient` | 设计正确，能力受限 |
| 双语文档门禁阈值不一致（1 vs 100） | 未修 | 治理策略裁定 |
| `docs/en`+`docs/zh-CN` 镜像不检查内容语言 | 未修 | 治理策略裁定 |
| `AttestorRef`/`AuthorizationDecisionRef` 占位可伪造 | 有测试固定（`fact_with_placeholder_attestor_validates_today`） | 等 I/D 授权 |

---

## 6. 计数规则（沿用）

每项交付完成后只记三件事：

1. **实测数字**（命令输出，不是声称）
2. **未实现清单**（明确列出，含 ignore 理由）
3. **是否有生产权威接入**（YES/NO + 依据）

本轮新增第 4 条：**交付文件是否与测试文件字节一致**（GAP-03.1 的教训）。

---

## 7. 这份文档自己的可信度

这份测量里的每一个数字，都是我从 `git archive` 干净导出后在 WSL2 上跑出来的。没有引用任何 Owner 的回执数字。

但我要明确记录：**这份文档的前一版（GAP-BASELINE-003）里有一条结论是错的**（双语文档 side-by-side 漏洞的描述）。我在本轮实测推翻了它，并把它写在第 3.5 节。

一份从不自我修正的测量文档，只是一份更长的声称。
