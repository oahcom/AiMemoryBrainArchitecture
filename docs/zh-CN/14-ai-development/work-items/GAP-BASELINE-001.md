---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Frozen baseline measured at a8fd2b7; file introduced by 1ad6c2c"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Historical frozen measurements; this bilingual remediation does not remeasure implementation state."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/GAP-BASELINE-001.md"
---

# GAP-BASELINE-001 — 关键工作负载基线缺口

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 冻结时间：**2026-11-21 15:00 +08:00**
- 测量提交：`a8fd2b7`（main；从过期的 `67ab237` 执行 `git pull --ff-only` 后）
- 本文件提交：`1ad6c2c`（引入本文档的提交；由于该提交只新增本文档，所有被测路径的树内容与 `a8fd2b7` 相同）

**基线权威规则：**当本文档与派发提示词中的 SHA 不同，派发提示词中的 SHA 对“读取哪棵树”具有权威性。`1ad6c2c` 与 `a8fd2b7` 仅相差一个文件——就是本文档。以下所有测量均在 `a8fd2b7` 上完成，并在 `1ad6c2c` 上继续有效。
- 状态：**已冻结基线——不是验收决定**
- 权威：Owner 级派发基线；每个 Owner 在自己的职责范围内保留规范权威。

## 本文档存在的原因

此前列出了六个关键缺失工作领域，并给出了未实现比例（85% / 80% / 90% / 60% / 100% / 100%）。这些数字是基于更早的代码树得出的。
仓库随后前进了 536 个提交。本文档在当前基线提交上重新测量各领域，使派发依据实际代码树，而非记忆中的数字。

**此前所有百分比均由以下测量结果取代。**如果测量与先前说法矛盾，以测量为准，并明确说明矛盾。

## 提交 `a8fd2b7`（等于 `1ad6c2c` 的树内容）上的测量状态

### GAP-01 — Memory Compiler 核心逻辑

| 项目 | 测量结果 |
|---|---|
| 负责 Owner | **E**（Memory Compiler Architect） |
| 文档 | `04-memory-compiler/` 存在，含 2 个文件：`phase-1-event-store-contract.md` 及其 `.zh-CN.md` |
| Rust 代码 | **0**——`crates/` 下没有任何 crate 引用 `compiler` / `Compiler` |
| 参考模型 | 0 |
| 先前说法 | 85% 未实现 |

**更正：**该领域并非 85% 未实现——按代码计算是 **0% 已实现**，按规格计算约为 10%。现有两个文件是事件存储契约，不是编译器阶段契约。不存在 `crates/memory-compiler`。

验收条件：存在编译器阶段契约，明确阶段、输入、输出、来源信息字段及失败语义；并且存在 `crates/memory-compiler`（或等效参考模型），其测试在固定工具链下运行并报告精确通过数量。

### GAP-02 — Memory Context 引擎

| 项目 | 测量结果 |
|---|---|
| 负责 Owner | **G**（Memory Context Architect） |
| 设计文档 | 19 个 `.md` 文件 |
| Rust 实现 | `crates/memory-context/src/lib.rs`——**472 行，7 个 `#[test]`** |
| Python 参考模型 | `06-memory-context/reference-model/g_applied_ledger.py` + 测试 |
| 先前说法 | 80% 未实现 |

**更正：先前说法错误。**已经存在可编译的真实实现，具备确定性快照规划（`ContextBudget`、`ContextIdentity`，以及通过构造方式确保不可发送的 delivery intents）。该领域是部分实现，并非缺失 80%。

剩余缺口：该 crate 按设计止于持久化和传输之前。Delivery Intent 不可发送，因此不存在端到端路径。

验收条件：每个已记录关注点（budget/sufficiency、edit operations、reconciliation、versioning、manager）都必须映射到可执行且有测试的模型，或明确标记为 `NOT IMPLEMENTED` 并说明阻塞原因。

### GAP-03 — Agent Integration 核心

| 项目 | 测量结果 |
|---|---|
| 负责 Owner | **C**（Agent Integration Architect） |
| 设计文档 | 4 个 `.md` 文件 |
| Rust 代码 | **0**——没有 crate 引用 adapter / agent-integration 类型 |
| 测试 | **0** |
| 先前说法 | 90% 未实现 |

**更正：**已确认没有可执行实现。`crates/memory-*` 中匹配到的 `adapter` 是 SQLite adapter 命名，与 Agent Adapter 无关。

验收条件：能力层级表必须绑定到具体操作；并且存在可执行参考模型，演示层级强制执行和推理边界拒绝行为，且配有测试。

### GAP-04 — BMCP 完整协议栈

| 项目 | 测量结果 |
|---|---|
| 负责 Owner | **H**（BMCP Protocol Architect） |
| 契约 | 4 个 `.md` 文件 |
| Schema | 1 个（`bmcp.applied-delivery-evidence-1.0.0.schema.json`） |
| Validator | 1 个（`applied_delivery_evidence_validator.py`） |
| 一致性套件 | `applied_delivery_evidence` 有测试文件；`provider_outcome` 只有 fixtures + requirements.txt，没有测试 |
| Rust 代码 | **0**——没有 crate 或工具引用 BMCP |
| 先前说法 | 60% 未实现 |

**更正：**按代码计算，该领域约有 85% 未实现。两个一致性套件中只有一个可以执行；协议本身没有 Runtime 实现。

验收条件：每个 Schema 都有 Validator 和可执行一致性套件；`provider_outcome` fixtures 增加测试文件；协议索引枚举所有消息类型及其已实现/未实现状态。

### GAP-05 — Phase 2/3 Domain Model 扩展

| 项目 | 测量结果 |
|---|---|
| 负责 Owner | **B**（Domain Model Architect） |
| `02-domain-model/` 文档 | 10 个 `.md` 文件，全部属于 Phase 1 范围（`phase-1-*` ×4） |
| Rust 代码 | `crates/memory-domain/src/lib.rs`——679 行，13 个 `#[test]` |
| Phase 2 工件 | **0** |
| Phase 3 工件 | **0** |
| 先前说法 | 100% 未开始 |

**更正：**若严格限定在 Phase 2/3，“100% 未开始”是准确的，但必须狭义理解——Phase 1 Domain Model **已经**通过 Rust 实现。缺口是 Phase 2/3 扩展，而不是整个 Domain Model。

验收条件：存在 Phase 2 Domain 扩展规格，包含实体、不变量和迁移说明，并由 Owner B 接受，或明确标记为阻塞且指出具体依赖。

### GAP-06 — 端到端测试

| 项目 | 测量结果 |
|---|---|
| 负责 Owner | **A**（Principal Integration Architect） |
| 仓库根目录 `tests/` | 2 个文件：`test_check_bilingual_docs_full.py`、`test_policy_inheritance.py`——均为治理测试，不是跨模块测试 |
| 集成测试 | `crates/memory-event-store-sqlite/tests/{forget_fence,resilience}.rs`、`crates/memory-store/tests/sqlite_integration.rs`——每个测试只覆盖一个 crate |
| E2E Harness | 存在 `benchmarks/req10_e2e/`，含 `benchmark.py` + `fixture_runtime.py` |
| E2E 实际运行 | **NOT_MEASURED**——Harness README 声明“development baseline only. Integrated product-runtime measurements: NOT_MEASURED”以及“The fixture is not a substitute for the runtime” |
| 先前说法 | 100% 未开始 |

**更正：**“100% 未开始”低估了已有工作——Harness 契约和协议已经存在。但 Harness **没有执行真实产品路径的 Adapter**，因此实际上没有端到端测试运行。该领域约完成 20%（Harness）/ 0%（真实路径）。

验收条件：至少有一个测试针对真实产品路径，跨越 `{compiler, context, agent-integration, bmcp}` 中两个或更多模块，断言可观察的契约结果，并可通过单条文档化命令运行。

## 更正后的汇总表

| 缺口 | Owner | 先前说法 | 测量现实 | 对先前说法的判定 |
|---|---|---|---|---|
| 01 Compiler | E | 缺失 85% | 0% 代码，约 10% 规格 | **低估缺口**——实际情况比所说更差 |
| 02 Context | G | 缺失 80% | 部分实现：472 行 Rust + 7 个测试 | **高估缺口**——真实代码已存在 |
| 03 Agent Integration | C | 缺失 90% | 0% 代码 | 确认 |
| 04 BMCP | H | 缺失 60% | 按代码约缺失 85%；两个套件中仅一个可执行 | **低估缺口** |
| 05 Phase 2/3 | B | 100% 未开始 | 100% 未开始（Phase 1 已完成） | 确认，但需限定范围 |
| 06 E2E | A | 100% 未开始 | Harness 存在，但没有真实 Adapter → 无实际路径运行 | **低估缺口**——已有工作开始 |

## 派发规则

1. 每个缺口只派发给一个 Owner 会话。任何 Owner 都不得编辑其他 Owner 的规范性契约。
2. 跨 Owner 问题必须在 Owner 回复中逐字记录，并在该边界停止。记录边界问题本身是有效终态。
3. 禁止自我批准。每项交付都必须由一个使用冻结输入的独立审查会话审查。
4. 本文档中的百分比是对 `a8fd2b7` 的测量；任何后续状态报告都必须重新测量，不得直接引用。

## 明确不作出的声明

- 本基线不授权合并、生产激活，或关闭 R3 缺陷登记册中的任何 Finding。
- 上述更正结论测量的是代码树中*是否存在*相关内容，而不是对现有代码质量的判断。
