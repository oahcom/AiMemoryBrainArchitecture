# A 独立源码审计 — ABR-INTEGRATION-001
# Review ABR-AUDIT-007

- Main 基线：`e52594f181d2edb77448adcfed64a0fbdffaf3aa`（Tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`）
- 集成 PR #93 Head：`0f3ba5293add8d6147a4375796b04c8bc6ae75e1`
- 研究输入：PR #84 `c6e76b34cbf099d36631b284c9b8a75d778d707f`；PR #85 `c5013d3585d54457f38bef37984645e2055ff7cf`；PR #86 `3892916ce2379f807a0ddcd0039816f6e88ecee1`；PR #88 `bf35b32295d0d3f337c80c3dc406db0a41de6830`。
- 裁决：**仅对研究整合准确性作有条件批准；不构成架构批准。**
- 范围：只读逐源码核验集成报告与原始源码、实验报告、Fixture、模型工件的一致性。

## 1. 执行结果

集成报告的核心结论得到支持：
- Forget 证据是有界逻辑探索，不是 TLC、无界证明或生产证据。
- Resource Manager Option B 是具有质量/延迟权衡的条件公平性候选，不是普遍改进。
- Memory IR 是小型合成设计探针，不是生产 Compiler 证据。
- 整体架构优越性仍未确定。
- 不产生 Owner 签字、Gate 关闭、架构冻结或生产授权。

发现 PR #93 有一项可复现性缺陷：整合报告引用的 Resource Manager 延迟数值与 PR #86 当前精确源码报告不一致。PR #93 的 Evidence Ledger 也缺少若干关键模型/原型/Fixture 的精确 Blob Pin。这些问题不推翻总体研究结论，但必须修正后才能将整合报告视为精确可复现证据包。

## 2. 独立读回的精确源码 Pin

### Forget / PR #88
| 工件 | Blob |
|---|---|
| Python 有界模型 `forget-formal-verification/model/forget_model.py` | `8e75f2978a0b85b3f0311ac0a189d40125b8d461` |
| F1–F8 不变量裁定 | `14eb422c4ac7763d4682adacacd50b42b34fda6c` |
| Model Checking Results | `2082e4a547dbe76c319d58bdd75022ccc532b6e2` |
| State Machine | `4868832dab421f6d76caf4d3366da68e960abe99` |
| Counterexample Catalog | `254ab3c7c467ab9acfcae88ffe1dc92d1045e3aa` |
| Remediation Proposals | `9baef6654783182dc825f34a6d35426286541a66` |

### Session 0 / PR #84
| 工件 | Blob |
|---|---|
| TLA+ Skeleton `forget-model/ForgetModel.tla` | `8b069efcafaf0d7ab7e42f3c4953ad3f4836cb29` |
| TLC Config `forget-model/ForgetModel.cfg` | `0e6e1bf9321a22afd856a4592efb3d23146d0119` |

### Resource Manager / PR #86
| 工件 | Blob |
|---|---|
| Benchmark 源码 `memory-operating-system/prototype.py` | `72b9f493b58cb42791c39cde5a78f2163235002e` |
| Benchmark 报告 `prototype-and-benchmarks.md` | `2053e4de179c80878fbdeee4f4874de5ad04057c` |

### Memory IR / PR #85
| 工件 | Blob |
|---|---|
| Prototype `prototype/memory_ir_prototype.py` | `bd27e93e90aceacf1857ebdf56b97e59ae34eb32` |
| Synthetic Input Fixture `prototype/sample_experiences.json` | `657268696ed95a481bf2836e9750fd59183d83e3` |
| Prototype README | `f2a293a084942cbc77b7f9025b6e4d442757a56d` |
| Direct-vs-IR 报告 | `087212cb9713d37d91fce8943efaf6d80249b87c` |

PR #93 的 Evidence Ledger 当前固定了关键叙述性报告，但没有列出这些底层可执行源码/Fixture Blob SHA。应补齐，以便读者复现真实证据，而不是依赖报告摘要。

## 3. 发现 ABR-007-01 — Resource Manager 延迟数据不一致

**严重度：** P1（可复现性/证据准确性）  
**Owner：** PR #93 集成报告作者；PR #86 实验作者负责源码说明  
**阻塞：** 是，阻塞将集成 Evidence Ledger 声称为精确证据账本；不阻塞研究级总体结论。

PR #86 当前 Benchmark 报告 Blob `2053e4de...` 记录：
- Direct Top-K 中位选择延迟：**0.095 ms**
- Rerank + Budget：**0.119 ms**
- Unified RM：**0.306 ms**

PR #93 英文整合报告写成 Direct Top-K **0.099 ms**、Unified RM **0.324 ms**。这些数值与 PR #86 当前精确报告 Blob 不一致。整合报告关于“本地原型延迟约 3.3 倍”的定性描述方向仍正确，但具体数值不一致。

要求修正：
1. 使用 PR #86 固定报告中的数值；或明确标识另一轮 Benchmark 的独立来源，并固定其代码、参数、输出与 Commit。
2. 保留其仅为单线程本地 Python 微基准、不是服务延迟的限定。
3. 保留真实权衡：Unified RM 的 Starved Tasks 为零、Jain Task-Coverage Fairness 最好，但 Recall/Precision/Token Efficiency 低于 Direct Top-K，且本地延迟更高。
4. 不得将其称为生产容量、系统整体效率或产品净收益证据。

## 4. 发现 ABR-007-02 — Forget 证据有界且依赖 Guard 假设

**严重度：** P1（范围/结论边界）  
**Owner：** A/Forget 研究作者与 PR #93 集成作者  
**阻塞：** 是，阻塞任何形式化证明或生产安全声明；不阻塞研究候选裁定。

Python 模型只有一个状态记录，包含一个 Admission/Work Item、一个 Fence Generation、一次 Publication、一个 Index/Cache Projection、一个 Receipt 和一次 Restore。其状态计数是 `(State, depth)` 组合，不是全局唯一语义状态数。安全结果依赖 `step()` 中编码的 Guards/Assumptions；Mutant 则刻意移除单个 Guard。

模型的 `violates()` 只检查编码的不变量，不证明 Liveness、Fairness、任意 Dependency Closure、多操作并发行为或实现 Refinement。结果文件正确标记为 Bounded Abstraction Only。

Session 0 的 TLA+ Module 是另一份独立 Skeleton。它具有有限 Producers/Artifacts/Targets，并包含 Suppression、Register-Before-Visible、Barrier Soundness 与 High-Water 不变量。CFG 文件存在，但报告与仓库证据均未证明 TLC 已执行。Restore Action 只是把模型变量赋为 currentControlGeneration，不是物理 Backup/PITR 回滚演练。

要求修正/后续：
- Python 有界结果与 TLA+ Skeleton 必须分开标记。
- 不得把任一结果标记为 TLC Pass 或生产证明。
- 扩展模型：多 Producer Lease/Attempt、DLQ/Replay、每个 Durable Boundary 前后的 Lost ACK、多个重叠 Forget、PermissionEpoch、I Inventory Seal/Change、Derived Dependency DAG、G/H/F Projection、Storage Prepared Participant、Split-Brain/Failover 与 Restore Rollback。
- 只有在环境和公平性假设明确后，才添加 Liveness/Fairness Properties。
- 定义模型变量/动作到 D/E/I/Storage/F/G/H 精确 Owner 合同和可执行测试的 Refinement Mapping。

## 5. 发现 ABR-007-03 — Memory IR 实验只是五条合成样本的结构探针

**严重度：** P2（证据范围）  
**Owner：** C 研究作者 / PR #93 集成作者  
**阻塞：** 不阻塞 Candidate/Shadow-only 分类；阻塞生产质量、类型准确率或复杂度下降声明。

精确 Fixture 只有五条记录：四条格式正确，一条缺少 source_id。包含两个冲突的 lives_in 值，以及另外两条断言。Prototype 使用确定性的合成规则提取器，零模型调用，无实体解析、无持久化缓存。它展示了确定性输出、阶段级诊断，以及单条输入编辑时未受影响节点 ID 的稳定性。它没有证明 LLM 提取质量、语义正确性、并发、持久增量编译、崩溃恢复、Forget/Permission 或 D Canonical Commit。

报告正确说明 Direct Baseline 是刻意简化的实现，实验不是统计有效 Benchmark。必须保留此限定；不能把 IR 增加的元数据直接解释成净复杂度下降的证明。

下一步证据：
- 20–50 条经批准的代表性匿名/合成边界 Fixture，并说明覆盖理由；
- Temporal Interval 边界、Scope 隔离、Malformed Input、Provenance Graph Closure、Version Migration、Invalidation 的 Property-based Tests；
- Parser/Extractor/IR/Transform 版本变化时的 Deterministic Replay；
- 旧 Forget/Permission Receipt 不得授权新 Derivation 的显式测试；
- 在 E 内部进行 Shadow Comparison，保持 D Commit 不变，测量阶段诊断、Provenance 完整性、CPU/Memory、Cache Invalidation 与运维负担。

## 6. 集成结论与裁决

以下结论仍然成立：
- Forget：生产 P0 / NOT READY；逻辑模型证据有界且有条件。
- Resource Manager Option B：CANDIDATE / SHADOW ONLY；公平性是产品权衡，不是免费的效率收益。
- Memory IR：E 内部 CANDIDATE / SHADOW ONLY；不改变 B Fact/Claim ADR 或 D Canonical Commit 权威。
- 架构优越性：UNRESOLVED。
- Issue #43 G1–G8 与既有 P0 Blocker 仍保持 OPEN。

**ABR-AUDIT-007 裁决：仅对研究整合准确性作 APPROVED_WITH_CONDITIONS。** 条件：
1. 修正 RM 延迟数值，或固定另一轮精确实验来源。
2. 补充 Python Model、TLA+ Skeleton/Config、RM Prototype/Report、IR Prototype/Fixture/Report 的精确 Blob Pin。
3. 将有界模型、合成 Benchmark、Prototype、物理生产证据保持为不同证据类别。
4. Owner 分支推进时重新读取并固定所有 Source Pin。

不修改任何 Owner 合同，不合并 PR，不释放 Gate，不授予生产授权。
