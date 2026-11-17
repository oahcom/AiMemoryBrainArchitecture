# Memory IR / Memory Compiler 独立研究

**状态：** 启动基线已固定；领域映射与原型尚未完成。  
**基线：** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`（2026-11-18）  
**跟踪：** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## 研究目标

判断记忆形成流程是否值得引入 Typed Intermediate Representation（Memory IR），以减少阶段间重复解释、增强类型/语义校验、来源追踪、冲突诊断、确定性重处理和增量演化。

## 已知关键限制

Issue #43 当前仍将 B Fact/Claim ADR 标记为 ADR-BLOCKED，并记录相关消费者概念区分与规范对象身份尚未收敛。因此本研究不得自行决定 Fact/Claim 的 canonical identity，也不得把某个候选类型系统当成现行领域模型。

## 基线读取

精确读取当前 B Domain Model、ADR、I-04/P-04 消费者映射、Compiler/Ingestion/Extraction/Normalization、Entity Resolution、Provenance、Consolidation、Canonical Commit 及相关测试。每项来源记录 branch HEAD、path、Blob SHA、规范状态和读取时间。

## 候选流水线

Raw Experience → Parsing → Extraction → Memory IR → Type/Semantic Validation → Entity Resolution → Conflict Analysis → Optimization/Consolidation → Canonical Commit。

逐项检验阶段顺序，不预设该流水线正确。IR 至少评估 Fact/Claim/Assertion/Event/Entity/Relationship/Procedure 等候选表达，以及 Source Evidence、Confidence、Authority、Provenance、Scope、Temporal Semantics。不得为追求完整性把每个词都变成独立实体。

## 关键问题

1. 一个 IR 还是多层 IR？
2. IR 与 canonical domain model 的边界是什么？
3. Fact/Claim 区分应在何阶段发生，哪些决策必须等待 B/治理权威？
4. Provenance 是否不可变且贯穿各 compiler pass？
5. 如何表达矛盾、过期、推测、不确定性和时间有效区间？
6. 如何版本化 IR、编译器 pass、模型/规则与输出？
7. 如何实现确定性重处理和增量编译？
8. 如何处理 schema 演进、旧 IR 解释与迁移？
9. IR 是否减少复杂度，还是新增一层抽象和双重模型？

## 原型

使用相同固定种子的合成输入实现：
- Direct Pipeline：抽取后直接构造目标结构；
- IR Pipeline：生成 IR，再执行类型/语义校验与规范化。

比较 Provenance Completeness、Type Validation、Conflict Detection、Determinism、Incremental Processing、Schema Evolution、Error Localization、Processing Cost、Data Loss。公开代码、数据、命令和结果；不得宣称合成结果证明生产质量。

## 技术复用

比较 LLVM/MLIR IR 思想、JSON Schema、Protobuf、Avro、AST、Serde/Pydantic 和数据库迁移工具。必须比较采用成熟工具与自行开发的真实成本。

## 交付与边界

交付 pipeline 复杂度分析、IR 候选模型、compiler 方案、版本/来源策略、Direct-vs-IR 原型、技术复用矩阵、迁移风险和双语报告。仅修改本研究分支；不修改 B/I 等权威契约，不冻结 schema，不合并，不进入生产实现。所有结论标注 DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED。
