# Phase 1 领域模型冻结

**状态：** 对 Phase 1 实现范围标记为 DECIDED；全局未决事项继续保持 OPEN/CANDIDATE/TO_VALIDATE。  
**仓库：** `oahcom/AiMemoryBrainArchitecture`

## 目的

冻结 Phase 1 实现与测试所必需的最小领域契约，同时禁止通过本阶段实现偷偷决定后续架构问题。

## 冻结边界

Phase 1 覆盖 Event、Memory、MemoryVersion、Claim、ScopeRef、Provenance 引用以及可查询的规范状态。

本阶段不冻结 ID 生成算法、BMCP Wire Format、SQLite DDL、Vector/Graph Index、LLM 或 Embedding Provider、跨版本 Claim 身份、物理 Forget 语义、Permission Policy 语言以及分布式部署语义。

## 规范对象

Phase 1 规范对象包括 Event、Memory、MemoryVersion、Claim、Entity、Relation、Evidence、Provenance、MemorySource、MemoryContext、ContextEntry、ScopeRef、ActorRef 和 TemporalRef。

Fact 不是 Phase 1 的独立对象。已验证事实以具有 Verified 认知状态的 Claim 表示，并保留所需的 Evidence、时间和 Scope 元数据。

## 核心不变量

- Event 与 Memory 是不同概念。
- Memory 身份在不可变版本之间保持稳定。
- MemoryVersion 不可变；更新通过创建后继版本完成。
- 并发更新必须携带 expected current/parent version；过期写入必须拒绝。
- Scope 必须显式存在，且 Scope 不等于 Permission。
- 不同 Scope 不得隐式可见或合并。
- Claim 的认知状态与 Memory 生命周期相互独立。
- Provenance 必须存在或明确标记不可用，不得伪造。
- Intent、Plan、Prediction、Attempt 没有 Outcome Evidence 时不得升级为完成结果。
- Domain Validation 必须确定、无副作用，并且不依赖 SQLite、HTTP、LLM 或 Agent Framework。

## Scope 隔离

规范 Scoped 读写必须具有已解析的 Scope。对 Scoped 对象而言，Scope 缺失或含糊必须拒绝。跨 Scope 引用必须具有显式共享语义。

## Domain API 边界

后续 Domain crate 只提供纯领域类型与校验能力，例如 Event、Memory、Version、Claim、Scope 校验，以及版本和 Scope 转换检查。Storage、Compiler、Runtime 和 Governance 通过 application ports 使用这些能力。

## 验收

DM-01 至 DM-10 覆盖对象分离、版本不可变性、并发、Claim 语义、Scope 隔离、Provenance、Outcome 边界、确定性、依赖边界以及未决决策卫生。

## 决策状态

本冻结只决定上述 Phase 1 实现语义。ID 生成、Claim 全局身份、Relation 词汇、Evidence Strength 公式、Scope Algebra、Permission Policy 语言和 Physical Forget 等事项，只要原领域规范仍标记为 OPEN/CANDIDATE/TO_VALIDATE，就继续保持未决。

## 下一单元

下一逻辑单元为 Rust Workspace：建立 Cargo Workspace，实现已冻结的领域类型和纯领域测试；不得引入 Storage、SQLite、Vector DB 或模型依赖。