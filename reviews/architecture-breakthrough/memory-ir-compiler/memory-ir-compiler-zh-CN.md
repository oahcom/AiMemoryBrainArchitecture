# Memory IR 与 Memory Compiler 架构突破研究

- 研究编号：MB-IR-001
- 状态：CANDIDATE / TO_VALIDATE；不构成生产架构决议
- 仓库基线：`main` HEAD `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- 隔离分支：`research/memory-ir-compiler-session-c-2026-11-18`
- 权威边界：不修改 B Owner 领域模型，不解除 Fact/Claim ADR-BLOCKED，不修改生产 Pipeline。

## 1. 执行摘要

**建议引入一个轻量、分层、非权威的 Memory IR 候选层，但暂不将其纳入正式生产架构。**

当前 E Compiler 已经具备编译器式流水线：可靠接收、持久化 Work Item、Scope/Authorization 检查、确定性规范化、可选模型提取、Evidence/Provenance、Entity/Relation 提案、Conflict 提案、D Canonical Commit 和下游发布。Accepted、Compiled、Candidate Produced、Canonical Committed、Indexed、Context Applied 被明确区分。因此本研究不是要重新发明 Compiler。

真正值得验证的缺口是：是否需要一个跨阶段共享、可版本化、带类型、带诊断和依赖图的候选中间表示，避免每个阶段各自定义并重新解释候选数据。

推荐三层：
- L0 Source Envelope：不可变来源引用、摘要、接收和 Scope 元数据。
- L1 Extraction IR：Entity Mention、AssertionCandidate、EventCandidate、Evidence Span 等未规范化提案。
- L2 Semantic IR：经过类型/语义校验的候选图、时间/Scope 限定、Provenance DAG 和 ConflictSet。
- L3 Commit Projection：向当前 D Owner 精确合同的映射，不是第四种 Canonical Schema。

## 2. 当前基线和决策状态

Issue #43 将 B Fact/Claim ADR 明确标记为 ADR-BLOCKED。B Overview 的部分旧表述将 Claim 视为规范命题对象、Fact 视为限定解释；I-04/P-04 又将两者描述为不同概念/对象。B 双语指南明确要求 ADR 批准前不得冻结下游 Schema。

因此：
- 本研究只使用中性的 `AssertionCandidate`。
- 不决定 Fact 和 Claim 是同一对象、不同对象还是继承/特化关系。
- 依赖该映射的 L3 降级必须保持阻塞。
- 领域对象、身份、生命周期和规范存储仍由 B/D Owner 决定。

已检查来源：Issue #43；Main README 和文档入口；B Domain Model Overview（Issue #43 所列分支/Blob）；B 中英文指南；E 中英文 Compiler Guide。E 详细 Owner 分支中的全部字段级合同和测试未在本轮逐项读取，因此不能声称 IR 在详细 E 契约中完全不存在。

## 3. 为什么不是一个通用大 Schema

单一通用 Schema 会把原始来源、模型提取猜测、实体解析结果和可提交规范对象混在一个结构里，容易出现大量可空字段和“候选看起来像已批准”的问题。

分层 Typed IR 可以明确每一阶段允许知道什么：
- L1 的 Entity Mention 不等于 Canonical Entity。
- AssertionCandidate 不等于已决定的 Fact/Claim。
- ConfidenceEstimate 不等于 Truth、Trust 或 Evidence Strength。
- LifecycleHint 不等于 Canonical Lifecycle Transition。
- Entity Resolution 是 Scope 过滤后的提案，不在解析阶段赋予永久身份。
- ConflictSet 保存并列矛盾，不选择赢家。

## 4. 建议流水线

```text
Durable Accepted Event / Source Ref
  -> L0 Source Envelope
  -> Parse / deterministic extraction + optional model proposal
  -> L1 Extraction IR
  -> Type + structural validation
  -> Scope-filtered Entity/Relation resolution proposal
  -> L2 Semantic IR
  -> deterministic normalization / conflict / consolidation passes
  -> L3 D-contract-specific Commit Projection
  -> D Canonical Commit
  -> Index / Projection publication
```

IR 是候选编译产物，不拥有 Canonical ID、Lifecycle、Permission、Forget 或可见性。模型只能提出候选，不确立事实、不批准生命周期、不解决授权问题。

## 5. 关键设计决策建议

| 问题 | 研究建议 | 状态 |
|---|---|---|
| 是否引入 IR | 先做 Shadow IR，测量后再决定正式采用 | CANDIDATE |
| 通用还是多层 | 三层 Typed IR + 单独 Commit Projection | CANDIDATE |
| Fact/Claim 区分 | 中性 AssertionCandidate，不做领域决议 | ADR-BLOCKED |
| Entity Resolution | 先提取 Mention，之后 Scope 过滤并提出匹配 | CANDIDATE |
| Provenance | 每个派生节点必需的图边 | CANDIDATE |
| 矛盾/过期/推测 | 分离 Epistemic、Temporal、Lifecycle、Conflict 维度 | CANDIDATE |
| 可重复处理 | 记录模型输出/Prompt/规则/Resolver Snapshot/Schema 版本 | CANDIDATE |
| 增量编译 | 按 Pass 依赖 DAG 进行精确失效 | TO_VALIDATE |
| 历史解释 | 原始版本保留、显式升级链、未知主版本 Fail Closed | CANDIDATE |
| 成熟工具 | 复用 JSON Schema、Serde/Pydantic、迁移工具 | RECOMMENDED |

## 6. Provenance 和可重复处理

Provenance 必须是 IR 一等图结构，而非一个自由文本字段。每个派生节点关联：
- EvidenceRef：来源版本、摘要、片段、可用性；
- Parent IR Node：父级候选节点；
- Pass Manifest：转换 ID、实现版本、输入输出摘要；
- Model Manifest：Provider/Model Revision、Prompt Digest、参数、Tool Result 和响应引用；
- Schema/Rules/Policy/Resolver Snapshot 版本；
- 脱敏、删除、不可用原因。

重放等级：
- R0：纯确定性 Pass，同输入和配置应字节一致。
- R1：外部依赖 Snapshot 固定后可重复。
- R2：重用已记录模型输出，保证下游转换可重复。
- R3：重新调用模型，属于新编译尝试，不声称确定性。

Permission、PermissionEpoch、Forget Fence、Retention 和最终 Visibility 是实时治理边界，不得仅靠缓存命中绕过。

## 7. 合成原型结果和限制

已在隔离分支加入标准库 Python 原型及合成数据：
- Direct Pipeline：一阶段映射到目标形状。
- IR Pipeline：Parse → Typed IR → Semantic Validation → Lowering。
- 同一份五条合成输入，包含一条缺失来源的无效输入和一组重叠时间的冲突陈述。
- 输出结构化诊断、冲突提案、来源链路、确定性重放摘要和增量节点复用计数。

复现：

```bash
python3 reviews/architecture-breakthrough/memory-ir-compiler/prototype/memory_ir_prototype.py
```

预期：5 条输入、4 条有效记录；两条路径均提出一个冲突集合；相同输入重复运行的 IR 输出稳定；修改一个来源后，其他未变来源的节点 ID 保持稳定。

**限制：** 这是合成数据和确定性规则夹具，不是生产质量证明。未测试真实 NLP/LLM、Entity Resolution、持久化增量缓存、并发、崩溃恢复、Canonical Commit、Forget、Authorization 或大规模成本。原型不证明 IR 的生产收益。

## 8. 成熟技术采用边界

- MLIR：借鉴 Dialect、Type、Pass、Verifier、Lowering、Diagnostics 和 IR Versioning；不引入完整 MLIR 运行时。
- LLVM IR：只借鉴强类型和验证思路，抽象层过低。
- rustc：借鉴依赖图和增量 Query 失效。
- TypeScript Compiler：借鉴 AST/语义分析阶段。
- SQL AST/Query Planner：借鉴逻辑计划与执行计划分离，不借用其真值语义。
- JSON Schema：用于结构验证；跨节点不变量需自定义验证。
- Protocol Buffers：Rust 多服务边界确有需要时再考虑。
- Avro：存在长期事件流和 Writer/Reader Schema Resolution 需求时再考虑。
- Pydantic / Serde：作为语言内验证和序列化工具，而不是 IR 架构本身。
- DB Migration：管理物理 Schema，不替代 IR 语义版本迁移。

## 9. 复杂度和迁移风险

IR 会增加序列化、版本兼容、Pass Manifest、诊断、缓存失效和历史升级成本。若当前 E 的详细合同已提供同等能力，额外 IR 可能是重复抽象。

因此采用顺序必须是：
1. 不改现有生产写路径；
2. 选择一种来源类型做 Shadow IR；
3. 比较候选结果、Provenance 完整度、诊断、冲突、Replay、资源成本；
4. 由 E/B/D/I 等 Owner 分别审查其权威边界；
5. 只有测量证明收益且审批完成后，才考虑单一窄路径迁移；
6. 保留 Direct Pipeline 回滚能力。

## 10. 最终裁决

1. IR 是否减少转换复杂度：**尚未证明**。它可能减少重复解释，但也增加阶段和版本治理成本。
2. 是否提高类型安全和来源追溯：**设计上有潜力，合成原型只展示了诊断和 lineage 表达能力**。
3. 是否改善冲突和增量演化：**IR 提供更好的承载结构；冲突算法本身并不会自动变好，持久化增量尚未实现**。
4. 是否过度抽象：**若做通用编译器框架或每种记忆类别独立类型，风险很高**。
5. 是否正式采用：**建议 Shadow Prototype，不建议当前冻结为正式层**。
6. 成熟工具能否替代：**可替代大部分序列化/验证基础设施，不能替代内存语义、Provenance 图和 Pass 合同**。
7. 如何迁移：**Shadow → 对照 → Owner 审查 → 单类型 Canary → 扩展/移除**。
8. 未解决：Fact/Claim ADR、E 详细合同是否已有 IR、Entity Resolution 的真实成本、Provenance/Forget 保留边界、跨服务增量和恢复语义。

**结论：RECOMMEND SHADOW IR / NOT READY FOR FORMAL ARCHITECTURE ADOPTION。**
