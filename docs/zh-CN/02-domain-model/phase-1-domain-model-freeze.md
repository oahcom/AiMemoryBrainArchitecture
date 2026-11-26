---
document_metadata:
  domain: domain-model
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Owner-authorized classification direction for AID-2026-11-26-GOV-DOC-01; this is not a formal approval record. Pre-metadata content blob: 6a6d8f3342974b3d3bb454a638d924815e47a793. Phase 1 semantic freeze does not authorize runtime implementation or deployment. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Phase 1 domain model freeze"
    canonical_scope_id: domain-model/phase-1-domain-model-freeze
    canonical_scope_keywords:
      - phase-1
      - domain-freeze
      - domain-semantics
      - implementation-binding
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "02-domain-model/phase-1-domain-model-freeze.md"
    en: "docs/en/02-domain-model/phase-1-domain-model-freeze.md"
    zh-CN: null
---
# Phase 1 领域模型冻结

**状态：** Phase 1 实现范围 **DECIDED**；全局未决决策继续保持 OPEN/CANDIDATE/TO_VALIDATE。  
**文档：** DOMAIN-MODEL-001 Phase 1 实现冻结  
**Owner：** Memory Domain Model（MB-01）

## 1. 冻结边界

Phase 1 只冻结以下最小领域闭环所需语义：

`Event -> Memory -> MemoryVersion -> Claim -> ScopeRef -> Provenance reference -> Queryable canonical state`。

本文件不冻结 ID 生成算法、BMCP Wire Format、SQLite DDL、Vector/Graph Index、LLM/Embedding Provider、物理 Forget 语义、Permission Policy Language 或分布式部署。

## 2. 规范领域对象

规范原文定义了七个 Phase 1 领域对象章节（2.1–2.7）。本镜像已补齐这些章节及其对象名称。下方 2.8–2.9 是对本指南提及的其他 Evidence、Provenance、Scope、Actor 和 Temporal 引用的解释性归组，不会向规范 Phase 1 冻结增加对象或扩大其范围；规范原文仍为权威依据。

Phase 1 使用 Event、Memory、MemoryVersion、Claim、ClaimRevision、Fact、FactRevision、Entity、Relation、Evidence、Provenance、MemorySource、MemoryContext、ContextEntry、ScopeRef、ActorRef 和 TemporalRef。

Claim 表示命题身份及不可变 ClaimRevision 历史。

Fact 是引用精确 ClaimRevision 值的独立受治理 Attestation 对象。

Fact 不等同于客观真理、Confidence 或 Verified Claim 状态。

本次收敛决策取代此前 Phase 1 文档中相冲突的语义描述。

本决策仅确定语义方向，不批准物理 Schema、DDL、公开 API、Wire 契约、生产安全材料或实现符合性。

### 2.1 OpaqueId

所有领域 ID 都是不透明标识：不携带业务语义、不由显示名称推导，并且在其定义的生命周期内不可复用。其序列化形式暂定为字符串；具体生成算法仍为 CANDIDATE。Phase 1 不允许通过 ID 的字典序、前缀或字符串内容推断业务含义。

### 2.2 ScopeRef

`ScopeRef` 是对象的命名空间/适用范围引用。

| 字段 | 约束 |
|---|---|
| `scope_id` | 必填；类型为 `OpaqueId` |
| `scope_kind` | 必填；受控枚举 |
| `namespace_key` | 必填；不得由显示名称推导 |

Phase 1 支持以下 Scope Kind：`user`、`project`、`agent`、`agent_instance`、`task`、`session`、`environment` 和 `system`。

**DECIDED：** Scope 与 Permission 分离。Domain Model 只表达 Scope 归属/适用范围，不把 Permission 或 Grant 嵌入 Memory 数据结构。

### 2.3 Event

Event 表示捕获或接收的 occurrence、observation、report、transition 或其他受治理输入。Event 不证明所表示内容为真；Event acceptance 不等于 Memory Truth。

### 2.4 Memory

Memory 是稳定、可寻址的 retained knowledge asset。Memory identity 跨版本稳定。Lifecycle 与 Claim Epistemic Status 独立。ContextEntry 不拥有 Memory，Context Remove 不是 Forget。

### 2.5 MemoryVersion

MemoryVersion 是不可变语义快照。更新只能创建 successor version。Current-version pointer 与新的 Canonical Version Commit 必须处于同一个 Canonical Transaction Boundary。并发更新必须带 expected current/parent version；stale write 返回 conflict。

### 2.6 Claim

Claim 是规范 proposition。Epistemic Status 为 Observed、Reported、Inferred、Verified、Disputed、Retracted。Confidence 不等于 Truth。冲突和撤回必须保留历史及 Evidence。

**身份边界：** Claim 命题身份跨 Memory Version 使用稳定 ClaimRef；每个不可变断言状态按 DOMAIN-MODEL-001 §2.4 使用精确 ClaimRevisionRef 标识。该语义分类已 DECIDED FOR CONVERGENCE。ID 生成算法仍为 CANDIDATE，本文件不予冻结。

### 2.7 ProvenanceRef

Phase 1 不重新定义完整 Provenance DAG；MemoryVersion 只保存不可变的 Provenance 引用。

每个 derived MemoryVersion 必须：

- 至少引用一个合法 source/provenance；或
- 明确记录 provenance unavailable 的原因；
- 不得伪造缺失的 source；
- 不得把 model/method identity 当作 truth proof。

完整 Provenance graph 留待后续 Compiler / Governance 工作。

### 2.8 Evidence and Provenance concepts

Evidence 用于支持、反驳或限定 Claim。Provenance 记录来源和派生链路。缺失 Source 必须表示为 unavailable，不得伪造。Model/Method Identity 本身不是 Truth Proof。

### 2.9 Scope / Actor / Temporal Reference

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

**已 DECIDED FOR CONVERGENCE：** 跨 Memory Version 的稳定 ClaimRef 命题身份，以及 DOMAIN-MODEL-001 §2.4 的 CI-01..CI-13 分类规则。

**保持原状态：** ID Generation CANDIDATE；Relation Vocabulary OPEN；Evidence Strength TO_VALIDATE；Scope Algebra OPEN；Permission Policy Language OPEN；Physical Forget Semantics OPEN；Vector/Graph Technology 不进入 Phase 1。

## 8. 工程交接——延期，不构成授权

本节仅记录未来工程阶段的可能交接内容，不是当前实施指令或授权。

- 控制性边界为 `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`（参见 Issue #7 和 #1197）。
- Phase 1 的 DECIDED 仅表示本文列明的领域语义已冻结为架构基线；不授权当前创建或扩展 Rust Workspace/Crate，也不授权 Brain Runtime、Storage Integration、生产实现或部署。
- 仓库中已经存在的有限 Phase 1 Rust 类型/测试属于历史工作（参见 Issue #200 记录的有界工作），不得将其解释为新工作或扩展工作的授权。
- 未来工程阶段可以重新评估 Cargo Workspace、`crates/memory-domain`、Rust 类型及 DM-01..DM-10 测试。只有工程阶段入口前提满足且取得单独、明确的 Owner 实施授权后，才能启动。
- 本 Freeze 不冻结 Crate、进程、服务或部署边界，也不授权 Storage、SQLite、Vector DB 或 Model Integration。

> 本中文文件是 `02-domain-model/phase-1-domain-model-freeze.md` 的规范双语对应版本。
