# GAP-BASELINE-001 — 关键缺失工作负载基线

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 冻结时间：**2026-11-21 15:00 +08:00**
- 测量提交：`a8fd2b7`（main，从陈旧的 `67ab237` 执行 `git pull --ff-only` 之后）
- 本文件的提交：`1ad6c2c`（引入本文件的提交；其全部被测路径的树内容与 `a8fd2b7` 相同，因为该提交只新增了本文件）

**基线权威规则**：当本文件与某份派发提示词（dispatch prompt）指向不同 SHA 时，**派发提示词的 SHA 对「读取哪棵树」具有权威性**。`1ad6c2c` 与 `a8fd2b7` 恰好相差一个文件——即本文件。下文全部测量均在 `a8fd2b7` 上取得，并在 `1ad6c2c` 上仍然有效。

- 状态：**冻结基线 —— 不是验收决定**
- 权威性：Owner 层派发基线；每位 Owner 在其自身范围内保留规范权威。

## 本文件为何存在

曾有六个工作领域被列为关键缺失工作负载，并给出百分比（未实现 85% / 80% / 90% / 60% / 100% / 100%）。那些数字是针对更早的树得出的。此后仓库已前进 536 个提交。本文件在当前 base 提交上重新测量每一领域，使派发依据树，而非依据记忆中的数字。

**下文测量取代此前全部百分比。** 若某次测量与此前主张矛盾，以测量为准，并如实写出该矛盾。

## 在提交 `a8fd2b7`（即 `1ad6c2c` 的树）上的实测状态

### GAP-01 —— Memory Compiler 核心逻辑

| 项 | 实测 |
|---|---|
| 归属 Owner | **E**（Memory Compiler Architect） |
| 文档 | `04-memory-compiler/` 存在，含 2 个文件：`phase-1-event-store-contract.md` + `.zh-CN.md` |
| Rust 代码 | **0** —— `crates/` 下没有任何 crate 引用 `compiler`/`Compiler` |
| 参考模型 | 0 |
| 此前主张 | 未实现 85% |

**更正**：该领域不是未实现 85%，而是**代码实现 0%**、约 10% 已规范。现有两个文件是事件存储契约，不是编译阶段契约。不存在 `crates/memory-compiler`。

验收条件：存在一份编译阶段契约，指明阶段、输入、输出、来源字段与失败语义；并存在 `crates/memory-compiler`（或等价参考模型），其测试在固定工具链下运行并报告确切通过数。

### GAP-02 —— Memory Context 引擎

| 项 | 实测 |
|---|---|
| 归属 Owner | **G**（Memory Context Architect） |
| 设计文档 | 19 个 `.md` 文件 |
| Rust 实现 | `crates/memory-context/src/lib.rs` —— **472 行，7 个 `#[test]`** |
| Python 参考模型 | `06-memory-context/reference-model/g_applied_ledger.py` + 测试 |
| 此前主张 | 未实现 80% |

**更正：此前主张错误。** 存在一个真实、可编译的实现，具备确定性快照规划（`ContextBudget`、`ContextIdentity`、按构造即不可发送的投递意图）。该领域是部分实现，而非 80% 缺失。

残留缺口：该 crate 按设计止步于持久化与传输之前。投递意图不可发送，因此尚无端到端路径。

验收条件：每项已记录的关注点（预算/充分性、编辑操作、对账、版本化、管理器）要么映射到一个带测试的可执行模型，要么有一行明确的 `NOT IMPLEMENTED` 并写明阻塞原因。

### GAP-03 —— Agent Integration 核心

| 项 | 实测 |
|---|---|
| 归属 Owner | **C**（Agent Integration Architect） |
| 设计文档 | 4 个 `.md` 文件 |
| Rust 代码 | **0** —— 没有任何 crate 引用 adapter/agent-integration 类型 |
| 测试 | **0** |
| 此前主张 | 未实现 90% |

**更正**：确认——不存在任何可执行物。`crates/memory-*` 下匹配到的 `adapter` 是 SQLite 适配器命名，与 agent 适配器无关。

验收条件：一张绑定到具体操作的适配器能力分级表，外加一个可执行参考模型，演示分级强制与推理边界拒绝，并带测试。

### GAP-04 —— BMCP 完整协议栈

| 项 | 实测 |
|---|---|
| 归属 Owner | **H**（BMCP Protocol Architect） |
| 契约 | 4 个 `.md` 文件 |
| Schema | 1（`bmcp.applied-delivery-evidence-1.0.0.schema.json`） |
| 校验器 | 1（`applied_delivery_evidence_validator.py`） |
| 一致性套件 | `applied_delivery_evidence` 有测试文件；`provider_outcome` **只有 fixtures + requirements.txt，无测试** |
| Rust 代码 | **0** —— 没有 crate 或工具引用 BMCP |
| 此前主张 | 未实现 60% |

**更正**：该领域按代码计约未实现 85%。两个一致性套件中只有一个会执行；协议本身没有运行时实现。

验收条件：每个 schema 都有校验器和会执行的一致性套件；`provider_outcome` 的 fixtures 获得测试文件；一份协议索引枚举全部消息类型及其已实现/未实现状态。

### GAP-05 —— Phase 2/3 领域模型扩展

| 项 | 实测 |
|---|---|
| 归属 Owner | **B**（Domain Model Architect） |
| `02-domain-model/` 下文档 | 10 个 `.md` 文件，全部为 Phase-1 范围（`phase-1-*` ×4） |
| Rust 代码 | `crates/memory-domain/src/lib.rs` —— 679 行，13 个 `#[test]` |
| Phase 2 产物 | **0** |
| Phase 3 产物 | **0** |
| 此前主张 | 100% 未启动 |

**更正**：「100% 未启动」对 Phase 2/3 而言是准确的，但必须窄读——Phase 1 领域模型**确实**已在 Rust 中实现。缺口是 Phase 2/3 的扩展，而非整个领域模型。

验收条件：一份 Phase 2 领域扩展规范，含实体、不变量与迁移陈述，由 Owner B 接受，或明确阻塞并指明具名依赖。

### GAP-06 —— 端到端测试

| 项 | 实测 |
|---|---|
| 归属 Owner | **A**（Principal Integration Architect） |
| 仓库根 `tests/` | 2 个文件：`test_check_bilingual_docs_full.py`、`test_policy_inheritance.py` —— 均为治理类，均非跨模块 |
| 集成测试 | `crates/memory-event-store-sqlite/tests/{forget_fence,resilience}.rs`、`crates/memory-store/tests/sqlite_integration.rs` —— 各自只演练一个 crate |
| E2E 测试装置 | `benchmarks/req10_e2e/` 存在，含 `benchmark.py` + `fixture_runtime.py` |
| E2E 实际运行 | **NOT_MEASURED** —— 该装置的 README 写明「development baseline only. Integrated product-runtime measurements: NOT_MEASURED」以及「The fixture is not a substitute for the runtime」 |
| 此前主张 | 100% 未启动 |

**更正**：「100% 未启动」低估了已有工作——装置契约与协议已存在。但该装置**没有执行真实产品路径的适配器**，因此没有任何端到端测试真正运行。该领域约完成 20%（装置）/ 0%（真实路径）。

验收条件：至少一个测试执行跨越 {compiler, context, agent-integration, bmcp} 中两项或以上的路径，针对真实产品路径，并断言某个可观察的契约结果，且可由单条有文档记录的命令运行。

## 更正后的汇总表

| 缺口 | Owner | 此前主张 | 实测现实 | 对此前主张的判定 |
|---|---|---|---|---|
| 01 Compiler | E | 缺 85% | 代码 0%，已规范约 10% | **低估** —— 比主张更糟 |
| 02 Context | G | 缺 80% | 部分：472 行 Rust + 7 个测试 | **高估** —— 真实代码存在 |
| 03 Agent Integration | C | 缺 90% | 代码 0% | 确认 |
| 04 BMCP | H | 缺 60% | 按代码约缺 85%；两个套件仅一个执行 | **低估** |
| 05 Phase 2/3 | B | 100% 未启动 | 100% 未启动（Phase 1 已完成） | 确认，附带范围限定 |
| 06 E2E | A | 100% 未启动 | 装置存在，无真实适配器 → 无任何运行 | **低估** —— 工作已开始 |

## 派发规则

1. 每个缺口只派发给一个 Owner 会话。任何 Owner 不得编辑另一位 Owner 的规范契约。
2. 跨 Owner 的问题须逐字记录在该 Owner 的回复中，Owner 在该边界停止。记录一个边界问题是有效的终态。
3. 不得自我批准。每次交付都需要一个独立的审查会话，且输入冻结。
4. 此处的百分比是 `a8fd2b7` 上的测量值，任何后续状态报告都必须重新计算，不得引用。

## 明确的非主张

- 本基线不授权合并、生产启用，也不授权关闭 R3 缺陷登记中的任何发现。
- 上文的更正判定是对**树中是否存在**的测量，不是对既有代码的质量判断。
