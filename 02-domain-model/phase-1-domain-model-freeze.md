# Phase 1 Domain Model Freeze

**Status:** DECIDED for Phase 1 implementation scope; global unresolved decisions remain OPEN/CANDIDATE/TO_VALIDATE as recorded by the domain-model documents.  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Purpose:** 将现有 Domain Model 规范收敛为 Phase 1 可实现、可测试、可持久化的最小领域契约。  
**Source documents:** `02-domain-model/domain-model-overview.md`, `02-domain-model/core-entities.md`, `02-domain-model/relationships-and-provenance.md`, `02-domain-model/scope-and-permission-model.md`.

## 1. Freeze boundary

Phase 1 只冻结实现最小闭环所必需的领域语义：

```
Event
  -> Memory
  -> MemoryVersion
  -> Claim
  -> ScopeRef
  -> Provenance reference
  -> Queryable canonical state
```

本文件**不**冻结：

- ID 的具体生成算法（UUIDv7 等仍为 CANDIDATE）。
- BMCP wire format。
- SQLite DDL。
- Vector / graph index。
- LLM / embedding provider。
- 物理 Forget 语义。
- 权限策略语言。
- 分布式一致性或多节点部署。

这些决策继续由原领域文档及后续 ADR 管理。

## 2. Canonical Phase 1 objects

### 2.1 OpaqueId

所有领域 ID 都是：

- 不携带业务语义；
- 不由显示名称推导；
- 在其定义的生命周期内不可复用；
- 序列化形式暂定为字符串；
- 具体生成算法保持 CANDIDATE。

Phase 1 不允许通过 ID 的字典序、前缀或字符串内容推断业务含义。

### 2.2 ScopeRef

`ScopeRef` 是对象的命名空间/适用范围引用。

最小字段：

| 字段 | 约束 |
|---|---|
| scope_id | 必填、OpaqueId |
| scope_kind | 必填、受控枚举 |
| namespace_key | 必填、不可由显示名称推导 |

Phase 1 支持以下 scope kind：

- user
- project
- agent
- agent_instance
- task
- session
- environment
- system

**DECIDED：** Scope 与 Permission 分离。Domain Model 只表达 scope 归属/适用范围，不把 permission/grant 嵌入 Memory 数据结构。

### 2.3 Event

Event 表示 Brain 捕获或接收的 occurrence、observation、report、transition 或其他受治理输入。

最小字段：

| 字段 | 约束 |
|---|---|
| event_id | 必填 |
| event_kind | 必填 |
| source_type | 必填 |
| source_id | 必填 |
| payload_ref | 必填 |
| event_time | 可为空 |
| recorded_at | 必填、不可变 |
| scope_refs | 必填、至少一个 |
| classification | 必填 |
| schema_version | 必填 |
| retention_class | 必填 |
| idempotency_key | 可按操作要求必填 |

Phase 1 classification 至少支持：

- observed
- reported
- planned
- predicted
- attempted
- outcome
- administrative
- unknown

**不变量：**

1. Event 不等于 Memory。
2. Event acceptance 不证明事件内容为真。
3. planned / predicted / attempted 不得自动升级为 outcome。
4. 相同 idempotency key 对应不同 payload digest 时必须视为冲突。

### 2.4 Memory

Memory 是稳定可寻址的 retained knowledge asset。

最小字段：

| 字段 | 约束 |
|---|---|
| memory_id | 必填、跨版本稳定 |
| memory_kind | 必填 |
| scope_refs | 必填 |
| current_version_id | 首次提交后必填 |
| lifecycle_state | 必填 |
| retention_class | 必填 |
| sensitivity | 必填 |
| created_at | 必填 |
| updated_at | 必填 |

Phase 1 lifecycle state：

- candidate
- consolidated
- active
- superseded
- archived
- forgotten

**不变量：**

- Memory identity 不随版本变化。
- Memory lifecycle 不是 truth status。
- Context Entry 不拥有 Memory。
- Context Remove 不等于 Forget。

### 2.5 MemoryVersion

MemoryVersion 是 Memory 的不可变语义快照。

最小字段：

| 字段 | 约束 |
|---|---|
| memory_version_id | 必填 |
| memory_id | 必填 |
| version_number | 从 1 开始，单调递增 |
| parent_version_id | 初始版本为空，其余必填 |
| created_at | 必填 |
| author_kind | 必填 |
| change_reason | 必填 |
| claims | 必填，可包含多个 Claim |
| provenance_refs | 必填 |
| content_digest | 必填 |
| schema_version | 必填 |

**DECIDED：**

- Version 不允许原地修改。
- 新状态通过创建 successor version 实现。
- 当前版本指针与新 Version 的 canonical commit 必须属于同一事务边界。
- 并发更新必须带 expected current/parent version；过期写入返回 conflict，而不是覆盖。

### 2.6 Claim

Claim 是 Memory 中的 canonical proposition。

Phase 1 最小字段：

| 字段 | 约束 |
|---|---|
| claim_id | 必填 |
| subject_ref | 必填 |
| predicate | 必填 |
| object_value | 必填 |
| polarity | 必填 |
| epistemic_status | 必填 |
| confidence | 可为空 |
| valid_time | 可为空 |
| asserted_at | 必填 |
| scope_refs | 必填 |
| qualifiers | 必填 |

Phase 1 epistemic status：

- observed
- reported
- inferred
- verified
- disputed
- retracted

**不变量：**

- Claim 是 proposition，不是 source。
- Confidence 不等于 truth。
- Verified 必须存在相应 method/evidence 语义；仅高 confidence 不得自动 Verified。
- Disputed 必须保留相互冲突的位置或 dispute record。
- Retracted 保留历史断言及撤回原因。

**Phase 1 identity boundary：**

**身份边界：** Claim 命题身份跨 MemoryVersion 使用稳定 ClaimRef；每个不可变断言状态按 DOMAIN-MODEL-001 §2.4 使用精确 ClaimRevisionRef 标识。该语义分类已 DECIDED FOR CONVERGENCE。分类规则遵循 `docs/zh-CN/02-domain-model/domain-model-overview.md` §2.4 / DOMAIN-MODEL-001 §2.4（CI-01–CI-13）。ID 生成算法仍为 CANDIDATE，本文件不予冻结。

### 2.7 ProvenanceRef

Phase 1 不重新定义完整 Provenance DAG；MemoryVersion 只保存不可变的 provenance references。

每个 derived MemoryVersion 必须：

- 至少引用一个合法 source/provenance；
- 或明确记录 provenance unavailable reason；
- 不得伪造缺失 source；
- 不得把 model/method identity 当成 truth proof。

完整 Provenance graph 留待后续 Compiler / Governance 实现。

## 3. Domain invariants required by Phase 1

实现必须保证：

1. Event 与 Memory 是不同 aggregate/concept。
2. Memory identity 跨 Version 稳定。
3. MemoryVersion immutable。
4. Version number 对单个 Memory 单调递增且不复用。
5. Stale version update 不得覆盖最新版本。
6. ScopeRef 必须显式存在，不能从 display name 推断。
7. 不同 scope 的 Memory 不得因相同文本、相同 label 或相同 Agent name 自动合并。
8. Permission 不由 ScopeRef 推导。
9. Planned / predicted / attempted 不得自动成为 completed outcome。
10. Claim epistemic status 与 Memory lifecycle 独立。
11. Provenance 缺失必须显式表示，不得编造。
12. Unknown time 不得解释为 timeless。
13. Context 操作不得直接修改 Canonical Memory。
14. Domain validation 必须是确定性的，并且不依赖 LLM。
15. Domain object 不得依赖 SQLite、HTTP、Agent framework 或具体模型实现。

## 4. Scope isolation contract for Phase 1

Phase 1 的 canonical read/write 必须带 resolved scope。

最小安全规则：

```
same scope      -> eligible for domain-level access
different scope -> not implicitly visible
ambiguous scope -> reject
missing scope   -> reject for scoped objects
```

这不是完整 Permission Policy。

Permission 仍由 Governance 层决定；因此：

> “同 Scope”只表示语义上允许进入同一命名空间，不代表当前 Actor 自动拥有 read/write 权限。

Phase 1 的 Scope isolation acceptance 至少覆盖：

- Agent A / Environment A 不可通过普通查询读取 Environment B 的 memory。
- 相同 Agent identity + 不同 Environment Scope 不得自动合并。
- 未解析 Scope 的对象不得进入 canonical scoped store。
- 跨 Scope reference 必须有显式 sharing semantics；没有则拒绝。
- Scope filtering 必须在 query result 形成之前生效。

## 5. Phase 1 domain API boundary

Domain crate 后续只提供纯领域语义和类型/验证能力，不直接操作存储。

目标接口形态：

```text
Event
Memory
MemoryVersion
Claim
ScopeRef
ProvenanceRef

validate_event(...)
validate_memory(...)
validate_memory_version(...)
validate_claim(...)
validate_scope(...)
check_version_transition(...)
check_scope_compatibility(...)
```

Storage、Compiler、Runtime、Governance 通过 application ports 调用这些能力。

## 6. Acceptance evidence

Phase 1 Domain Model 单元验收：

| ID | 验收项 | 必须证明 |
|---|---|---|
| DM-01 | Object separation | Event / Memory / Version / Claim 可独立表达 |
| DM-02 | Version immutability | 更新只能产生 successor Version |
| DM-03 | Version concurrency | stale parent/current version 被拒绝 |
| DM-04 | Claim semantics | epistemic status 与 lifecycle 分离 |
| DM-05 | Scope isolation | 不同 scope 不会隐式可见/合并 |
| DM-06 | Provenance | derived object 必须有 lineage 或明确 unavailable |
| DM-07 | Outcome boundary | plan/prediction/attempt 不升级为 outcome |
| DM-08 | Determinism | domain validation 不依赖模型或外部服务 |
| DM-09 | Dependency boundary | domain 层不依赖 SQLite/HTTP/LLM |
| DM-10 | Open-decision hygiene | 未决事项（ID generation 及 §7 列出的其余未决项）不得被实现偷偷冻结；已 DECIDED FOR CONVERGENCE 的稳定 Claim identity / ClaimRevision 语义不得再作为未验证项 |

## 7. Decision status after this freeze

本单元将以下内容作为 **Phase 1 DECIDED implementation contract**：

- Event / Memory / MemoryVersion / Claim 的边界；
- Memory identity 跨版本稳定；
- MemoryVersion immutable；
- version transition 的 expected-parent 语义；
- Scope 与 Permission 分离；
- Phase 1 scope isolation baseline；
- Claim epistemic status 与 Memory lifecycle 分离；
- Domain validation 的纯函数/无外部依赖边界；

以下状态**不变**：

- ID generation：CANDIDATE；
- Relation vocabulary：OPEN；
- Evidence strength formula：TO_VALIDATE；
- Scope algebra：OPEN；
- Permission policy language：OPEN；
- Physical Forget semantics：OPEN；
- Vector/Graph technology：未进入 Phase 1。

## 8. Next implementation unit

本单元完成后，下一逻辑单元为：

**Rust Workspace**

目标：

1. 建立 Cargo workspace；
2. 建立 `crates/memory-domain`；
3. 将本文件冻结的核心对象转成 Rust 类型；
4. 加入领域不变量单元测试；
5. 不引入 Storage、SQLite、Vector DB 或模型依赖；
6. 以本 PR 的 Domain Model 作为唯一 Phase 1 实现基线。
