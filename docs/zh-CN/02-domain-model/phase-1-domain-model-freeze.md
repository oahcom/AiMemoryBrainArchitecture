# Phase 1 领域模型冻结

**状态：** Phase 1 实现范围 **DECIDED**；全局未决决策继续保持 OPEN/CANDIDATE/TO_VALIDATE。  
**文档：** DOMAIN-MODEL-001 Phase 1 实现冻结  
**Owner：** Memory Domain Model（MB-01）

## 1. 冻结边界

Phase 1 只冻结以下最小领域闭环所需语义：

`Event -> Memory -> MemoryVersion -> Claim -> ScopeRef -> Provenance reference -> Queryable canonical state`。

本文件不冻结 ID 生成算法、BMCP Wire Format、SQLite DDL、Vector/Graph Index、LLM/Embedding Provider、物理 Forget 语义、Permission Policy Language 或分布式部署。

## 2. 规范领域对象

Phase 1 使用 Event、Memory、MemoryVersion、Claim、ClaimRevision、Fact、FactRevision、Entity、Relation、Evidence、Provenance、MemorySource、MemoryContext、ContextEntry、ScopeRef、ActorRef 和 TemporalRef。

Claim 表示命题身份及不可变 ClaimRevision 历史。

Fact 是引用精确 ClaimRevision 值的独立受治理 Attestation 对象。

Fact 不等同于客观真理、Confidence 或 Verified Claim 状态。

本次收敛决策取代此前 Phase 1 文档中相冲突的语义描述。

本决策仅确定语义方向，不批准物理 Schema、DDL、公开 API、Wire 契约、生产安全材料或实现符合性。

### Event

Event 表示捕获或接收的 occurrence、observation、report、transition 或其他受治理输入。Event 不证明所表示内容为真；Event acceptance 不等于 Memory Truth。

### Memory

Memory 是稳定、可寻址的 retained knowledge asset。Memory identity 跨版本稳定。Lifecycle 与 Claim Epistemic Status 独立。ContextEntry 不拥有 Memory，Context Remove 不是 Forget。

### MemoryVersion

MemoryVersion 是不可变语义快照。更新只能创建 successor version。Current-version pointer 与新的 Canonical Version Commit 必须处于同一个 Canonical Transaction Boundary。并发更新必须带 expected current/parent version；stale write 返回 conflict。

### Claim

Claim 是规范 proposition。Epistemic Status 为 Observed、Reported、Inferred、Verified、Disputed、Retracted。Confidence 不等于 Truth。冲突和撤回必须保留历史及 Evidence。

**身份边界：** Claim 跨 Memory Version 的稳定身份仍为 **OPEN**，不得通过 Phase 1 Contract 偷偷冻结。

### Evidence / Provenance

Evidence 用于支持、反驳或限定 Claim。Provenance 记录来源和派生链路。缺失 Source 必须表示为 unavailable，不得伪造。Model/Method Identity 本身不是 Truth Proof。

### Scope / Actor / Temporal Reference

Scope 表示对象的命名空间/适用范围，并与 Permission 分离。Actor 表示操作或来源的责任主体，不是 Permission Grant。TemporalRef 保留 Event/Recorded/Valid Time 区分；Unknown Time 不是 timeless。

## 3. 必须保持的领域不变量

1. Event 与 Memory 是不同概念。
2. Memory identity 跨版本稳定。
3. MemoryVersion immutable。
4. Version Number 单调递增，Stale Write 不得覆盖新版本。
5. Scope 必须显式存在，不得由显示名称推导。
6. 不同 Scope 不得隐式合并。
7. Permission 不由 ScopeRef 推导。
8. Planned/Predicted/Attempted 不得自动成为 Completed Outcome。
9. Claim Epistemic Status 与 Memory Lifecycle 独立。
10. 缺失 Provenance 必须显式表示，不得编造。
11. Context 操作不得直接修改 Canonical Memory。
12. Domain Validation 必须确定，且不依赖 LLM/Network/Storage。

## 4. Scope Isolation

Canonical Read/Write 必须携带 resolved Scope。不同 Scope 不得隐式可见。Scoped Object 缺失 Scope 或 Scope 不明确时必须拒绝。跨 Scope Reference 必须有显式 Sharing Authorization。

Same Scope 不等于 Permission Grant；Governance 仍拥有 Authorization Authority。

## 5. Domain API 边界

未来 Domain Crate 提供纯领域类型和确定性验证，包括 Event、Memory、MemoryVersion、Claim、ScopeRef、ProvenanceRef，以及 Version/Scope Compatibility 检查。Domain 不直接操作 Storage、HTTP、LLM 或外部 Framework。

## 6. 验收标准

DM-01 Object Separation；DM-02 Version Immutability；DM-03 Version Concurrency；DM-04 Claim Semantics；DM-05 Scope Isolation；DM-06 Provenance；DM-07 Outcome Boundary；DM-08 Deterministic Validation；DM-09 Dependency Boundary；DM-10 Open-decision Hygiene。

## 7. 决策状态

**Phase 1 DECIDED：** Event/Memory/MemoryVersion/Claim 边界、稳定 Memory Identity、Immutable MemoryVersion、Expected-parent Version Transition、Scope/Permission 分离、Phase 1 Scope Isolation、Claim Epistemic/Lifecycle 分离、确定且无外部依赖的 Domain Validation。

**保持原状态：** ID Generation CANDIDATE；Claim Global Identity OPEN；Relation Vocabulary OPEN；Evidence Strength TO_VALIDATE；Scope Algebra OPEN；Permission Policy Language OPEN；Physical Forget Semantics OPEN；Vector/Graph Technology 不进入 Phase 1。

## 8. 下一实现单元

Rust Workspace：建立 Cargo Workspace、`crates/memory-domain`、Rust 类型以及确定性的 DM-01..DM-10 测试；不引入 Storage/SQLite/Vector/Model 依赖。

> 本中文文件是 `02-domain-model/phase-1-domain-model-freeze.md` 的规范双语对应版本。
