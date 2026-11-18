# Phase 1 领域模型冻结

**状态：** DECIDED（Phase 1 实现范围）；全局未决事项继续保持 OPEN/CANDIDATE/TO_VALIDATE。  
**目的：** 将现有领域模型规范收敛为 Phase 1 最小可实现、可测试、可持久化契约。

## 1. 冻结边界

Phase 1 只冻结以下最小闭环所需语义：

```
Event -> Memory -> MemoryVersion -> Claim -> ScopeRef -> Provenance reference -> Queryable canonical state
```

本文件不决定具体 ID 算法、BMCP Wire Format、SQLite DDL、Vector/Graph Index、LLM/Embedding Provider、Claim 跨版本稳定身份、物理 Forget、权限策略语言或分布式一致性。这些继续由现有领域规范及后续 ADR 管理。

## 2. 规范对象

### OpaqueId
领域 ID 不携带业务语义，不由显示名称推导，在生命周期内不得复用，Phase 1 序列化为字符串。生成算法继续保持 CANDIDATE。

### ScopeRef
最小字段为 `scope_id`、`scope_kind`、`namespace_key`。支持 user、project、agent、agent_instance、task、session、environment、system。

**DECIDED：** Scope 与 Permission 分离。Scope 表达命名空间/适用范围，不自动授予读写权限。

### Event
Event 表示 Brain 捕获或接收的 occurrence、observation、report、transition 或其他受治理输入。必须具备身份、类型、来源、payload 引用、记录时间、Scope、分类、Schema Version、Retention Class，以及按操作要求提供幂等键。

planned/predicted/attempted 不得自动升级为 outcome；相同幂等键对应不同 payload digest 时必须视为冲突；Event 接收不证明内容为真。

### Memory
Memory 是稳定、可寻址的保留知识资产。Memory identity 跨版本稳定。Lifecycle State 与 truth status 分离。ContextEntry 不拥有 Memory，Context Remove 不等于 Forget。

### MemoryVersion
MemoryVersion 是不可变语义快照。新状态必须创建 successor version，禁止原地修改。当前版本指针与 canonical commit 属于同一事务边界。并发写入必须携带 expected current/parent version，过期写入必须冲突而不得覆盖。

### Claim
Claim 是 Memory 中的规范命题，包含 subject、predicate、object、polarity、epistemic status、可选 confidence/valid time、asserted time、scope 和 qualifiers。

Phase 1 状态：observed、reported、inferred、verified、disputed、retracted。

Confidence 不等于 truth；Verified 必须有相应 method/evidence 语义；Disputed 与 Retracted 必须保留相关历史。

**身份边界：** `claim_id` 只要求在 immutable MemoryVersion 内唯一；跨 MemoryVersion 的稳定 Claim identity 继续保持 **OPEN**。

### ProvenanceRef
Phase 1 保存不可变 Provenance 引用，但不冻结完整 Provenance DAG。派生版本必须存在合法 lineage 或明确记录 unavailable reason；不得伪造缺失 source，也不得把 model/method identity 当作 truth proof。

## 3. Phase 1 必须保证的不变量

1. Event 与 Memory 是不同概念。
2. Memory identity 跨 Version 稳定。
3. MemoryVersion immutable。
4. 单个 Memory 的 Version number 单调递增且不得复用。
5. stale update 不得覆盖最新 Version。
6. Scope 必须显式存在，不得从 display name 推导。
7. 不同 Scope 不得因相同文本、label 或 Agent name 自动合并。
8. Permission 不得由 Scope 推导。
9. planned/predicted/attempted 不得自动成为 completed outcome。
10. Claim epistemic status 与 Memory lifecycle 独立。
11. Provenance 缺失必须显式表示，不得编造。
12. Unknown time 不得解释为 timeless。
13. Context 操作不得直接修改 Canonical Memory。
14. Domain validation 必须确定性且不依赖 LLM。
15. Domain 对象不得依赖 SQLite、HTTP、Agent framework 或具体模型实现。

## 4. Scope Isolation

Canonical read/write 必须带 resolved Scope：

```
same scope      -> eligible for domain-level access
different scope -> not implicitly visible
ambiguous scope -> reject
missing scope   -> reject for scoped objects
```

这不是完整 Permission Policy。Governance 决定权限；Same Scope 只代表语义命名空间兼容，不代表当前 Actor 自动拥有读写权限。

验收至少覆盖：跨 Environment 读取被拒绝；相同 Agent identity + 不同 Environment Scope 不自动合并；未解析 Scope 的对象不得进入 canonical scoped storage；跨 Scope reference 必须存在显式 sharing semantics；Scope filtering 必须在形成 query result 前生效。

## 5. Domain API 边界

后续 Domain crate 只提供纯领域类型与验证，不直接操作 Storage：

```
validate_event(...)
validate_memory(...)
validate_memory_version(...)
validate_claim(...)
validate_scope(...)
check_version_transition(...)
check_scope_compatibility(...)
```

Storage、Compiler、Runtime、Governance 通过 application ports 调用这些能力。

## 6. Phase 1 验收证据

| ID | 验收项 | 必须证明 |
|---|---|---|
| DM-01 | Object separation | Event / Memory / Version / Claim 可独立表达 |
| DM-02 | Version immutability | 更新只能产生 successor Version |
| DM-03 | Version concurrency | stale version 被拒绝 |
| DM-04 | Claim semantics | epistemic status 与 lifecycle 分离 |
| DM-05 | Scope isolation | 不同 Scope 不会隐式可见/合并 |
| DM-06 | Provenance | 有 lineage 或明确 unavailable |
| DM-07 | Outcome boundary | plan/prediction/attempt 不升级为 outcome |
| DM-08 | Determinism | 不依赖模型或外部服务 |
| DM-09 | Dependency boundary | 不依赖 SQLite/HTTP/LLM |
| DM-10 | Open-decision hygiene | 未验证决策不被偷偷冻结 |

## 7. 决策状态

Phase 1 DECIDED：对象边界、Memory 跨版本稳定 identity、MemoryVersion immutable、expected-parent transition、Scope/Permission 分离、Scope isolation baseline、Claim epistemic/lifecycle 分离、纯领域验证边界。

继续保持：ID generation CANDIDATE；Claim global identity OPEN；Relation vocabulary OPEN；Evidence strength TO_VALIDATE；Scope algebra OPEN；Permission policy OPEN；Physical Forget OPEN；Vector/Graph 不进入 Phase 1。

## 8. 下一实现单元

**Rust Workspace**：建立 Cargo workspace 与 `crates/memory-domain`；实现冻结的核心类型和领域不变量测试；不得引入 Storage、SQLite、Vector DB 或模型依赖。

> 双语同步说明：本文件是 Phase 1 领域模型冻结的中文规范对应版本。其决策状态和章节结构必须与英文对应版本保持同步。
