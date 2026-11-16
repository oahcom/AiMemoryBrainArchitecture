# Session D — Memory Brain 三方六维度专项审查报告

**Review status:** 静态架构自审完成；不是独立第三方审查，也不代表 ADR、实现或安全验证通过。  
**Reviewed scope:** 五份 Session D 设计文档及 A/B/C 基线、Phase 1 integration review。  
**Baseline commit read:** e443b23f8a179ad12c163722ad93bc646fd3a80a (main at review start).

## 1. Review conclusion

**结论：有条件通过作为 Memory Brain 子系统候选规范；不允许据此冻结 Fact/Claim Schema、BMCP wire contract、全局授权或物理删除机制。** 设计把 Canonical Memory 权威、Agent 非职责、immutable version、Lifecycle、Entity/Relation、Forget domain support 和跨模块契约分开。仍有若干依赖总控 ADR、I/H/G 的问题必须保留 OPEN。

本报告只创建在 Session D 负责目录中，不修改公共基线或其他会话文件。

## 2. Decision status summary

### DECIDED (沿用既有治理基线)

- Brain 拥有 Canonical Memory 的逻辑权威；Agent 负责规划、推理、工具调用和行动。
- Canonical IDs opaque；Memory ID 稳定，MemoryVersion 不可变。
- Canonical truth 与可重建投影分离；Index/Cache/Graph projection 不拥有事实权威。
- Event、Memory、Claim、Fact、Entity、Relation、Evidence、Context 不得混同；具体 Fact/Claim 身份仍受 ADR 阻塞。
- Scope 与 Permission 分离；禁止 display name 推断身份和隐式跨 Scope 合并。
- Epistemic Status、Lifecycle、Confidence、Trust、Evidence Strength、Relevance 是独立维度。
- Context Remove 不等于 Forget；G 拥有 ContextVersion/ChangeSet。
- 记忆是数据而非指令，不得授予 System/Developer 权限或工具授权。
- 逻辑组件不等于独立服务/进程/crate。

### CANDIDATE

- FactRecord 作为独立、可审计的 attestation/qualification 对象；不代表客观真理，引用精确 ClaimRevision，拥有独立身份、Evidence、验证方法和修订历史。
- Claim identity 采用稳定 Claim ID + immutable ClaimRevision。
- LifecycleEvent append-only stream 是生命周期唯一权威；当前状态为可重建 fold/projection。
- Provenance DAG 为默认候选约束；禁止未声明的循环。
- 单一 canonical directed Relation edge，inverse traversal 默认按词汇声明派生。
- Forget 先 durable fence / access suppression，再依赖发现与异步目标清理；完成要求按 I 的 retention policy。
- MemoryVersion 快照 + CAS + outbox/recoverable publication。

### TO_VALIDATE

- 存储引擎、事务/outbox实现、快照与 delta 策略。
- Provenance、Relation、Conflict、Forget fan-out/depth 与延迟预算。
- Entity resolution 误合并/漏合并率与 merge/split 迁移规模。
- TimeValue 近似时间表达式的归一化正确率。
- Scope 授权批量评估和缓存隔离性能。
- Forget 部分失败、离线 Adapter、备份过期和恢复演练。

### OPEN

- INT-P0-01 Fact/Claim ADR 未批准。
- Generic Scope algebra、multi-owner/shared ownership。
- Principal/ActorRef 认证、issuer/delegation 与 H/I 身份边界。
- ContextVersion/ChangeSet 完整模型（G-owned）。
- Forget 对离线副本、不可变备份、外部模型数据的完成语义。
- Provenance DAG 最终决议及合法循环用例。
- Claim conflict/reinstatement、Consolidated/rejected 候选语义。
- vocabulary/schema 注册、未知值兼容和迁移政策。

## 3. INT-P0 status

### INT-P0-01 — Fact / Claim canonical conflict

**状态：CANDIDATE；阻塞 Schema/API 冻结。**

治理基线 I-04/P-04/README 把 Fact 与 Claim 作为不同领域概念；Domain Model 当前把 Fact 解释为 Claim 的资格解释。推荐 ADR 选择“FactRecord 是独立 attestation 对象”，而非把 Fact 当作 Claim 的别名或简单 enum。FactRecord 不声称客观真理，只记录在特定 scope、时间、验证方法和证据下，某个精确 ClaimRevision 达到声明标准。对比：

| 维度 | Fact 独立对象 | Fact 是 Claim qualification |
|---|---|---|
| 身份 | FactRecord 独立 ID，可引用一个/多个 ClaimRevision | 无独立身份，Fact 只是 Claim 状态/解释 |
| 生命周期 | 独立创建、复核、撤销/失效 | 随 Claim revision/status 变化 |
| Evidence | 既保留 Claim 的支持/反驳证据，又有 FactRecord 的验证证据 | 全部挂 Claim，需区分“支持主张”和“达到事实标准” |
| Version | FactRevision 指向精确 ClaimRevision | ClaimRevision 内部状态/解释字段 |
| 冲突 | 可存在互相竞争的 FactRecord，需 ConflictSet | Claim Disputed/Verified 状态复杂化 |
| 查询 | 可查 verified claim 与 attestation record | 查询更简单但语义粒度弱 |
| 权限 | FactRecord 可比 Claim/Evidence 更严格或独立治理 | 通常继承 Claim 权限，例外难表达 |
| 存储 | 多一类对象和引用边，复杂度更高 | 较轻量，但与 I-04/P-04 基线冲突 |

推荐理由：忠实保留治理基线的对象区分，允许验证主体、方法、时间、证据、撤销及权限独立审计。代价是额外身份和生命周期复杂度。ADR 未批准前禁止建立正式 Fact/Claim schema、DDL、公开接口或跨模块 wire 字段。需修改范围至少包括 README、00-governance/design-principles.md、architecture-invariants.md、terminology.md、02-domain-model/domain-model-overview.md、core-entities.md、epistemic-and-temporal-semantics.md、lifecycle-model.md，以及 E/F/G/H/I 所有消费 Claim/Fact 的契约；若选择独立对象则同步补全 FactRecord 规范。Session D 不得直接修改这些基线文件。

### INT-P0-02 — Scope end-to-end isolation

**状态：Brain 领域契约已提出；I/E/F/G/H 集成与负向测试仍 OPEN。**

Memory、Entity、Relation、Evidence、Provenance、Claim/Fact proposal 都必须携带 ownership ScopeRef 与 applicability ScopeRefs。ScopeRef 与 Permission 决策分离；每条引用都要检查 scope compatibility。display name、alias、Agent 自报标签不构成身份。候选过滤必须发生在 F candidate generation 之前，并贯穿关系扩展、rerank、聚合、缓存、Working Set、Context、日志、导出、恢复和异步任务。Merge/Split 不得越权。Owner：I 总负责授权机制；D 定义资源 scope 语义；E/F/G/H 各自执行本边界过滤与传递。

### INT-P0-03 — Forget end-to-end semantics

**状态：Brain 提供领域对象和依赖发现契约；I 拥有执行策略；完成证明 OPEN。**

ForgetOperation 包含目标、actor/scope、授权/策略版本、幂等键、suppression 时间、dependency snapshot/watermark、阶段、per-target 进度、失败、重试、残留例外和 completion proof。目标范围覆盖 MemoryVersion/Claim revision、Evidence、Provenance descendants、Entity/Relation references、索引/向量/图投影、缓存、Working Set、Context Entry/ChangeSet、备份/快照及外部接收方。逻辑访问阻断与物理删除分开。Brain 不声称可单方删除第三方模型已接收数据。Owner：I 执行治理/物理策略；D 提供 canonical dependency graph；E/G/H/F 提供 derivative targets 与失效/回执。

### INT-P0-04 — Memory prompt injection

**状态：Brain data contract 已定义；端到端防护验证 OPEN。**

保留 Source Identity、Epistemic Status、Trust Metadata、Evidence Reference 和 Provenance Lineage。Memory 内容在所有出口均标记/处理为不可信数据；不得进入 system/developer instruction channel，不得授予工具调用授权。下游必须测试伪造 system 标签、恶意记忆、多轮间接注入和跨 Scope 记忆污染。Owner：跨系统安全治理 I；D 提供来源/认知元数据，G/H/F 按上下文和协议边界实施。

## 4. INT-P1 / DM-001..013 traceability

| Issue | Status in Session D | Treatment / remaining owner |
|---|---|---|
| DM-001 / INT-P0-01 | OPEN, ADR-blocked | FactRecord vs Claim qualification proposal; no schema freeze. |
| DM-002 / INT-P1-01 | OPEN, G-owned | Brain exports pinned MemoryVersion refs; G defines ContextVersion/ChangeSet. |
| DM-003 / INT-P1-02 | CANDIDATE | Stable Claim ID + immutable ClaimRevision; ADR dependency remains. |
| DM-004 / INT-P1-02 | CANDIDATE | ConflictSet object proposed with members, dimensions, evidence and resolution history. |
| DM-005 / INT-P0-02 | OPEN | Generic ScopeRef minimum fields defined; full algebra/multi-owner semantics with B/I. |
| DM-006 / INT-P1-06 | CANDIDATE | TimeValue, TimeInterval, TypedObjectRef, ScopeRef, ContentRef, ActorRef, TypedPredicate/Value minimums described; H/I/B to finalize. |
| DM-007 / INT-P1-06 | CANDIDATE | Provenance DAG recommended; legal cycles require explicit typed exception and bounded traversal. |
| DM-008 / INT-P1-06 | CANDIDATE | LifecycleEvent stream is sole authority; projection is derived. Confirm Store implementation. |
| DM-009 / INT-P1-02 | CANDIDATE | Merge/Split and RelationMigration records; historical refs remain immutable. |
| DM-010 / INT-P0-02 | OPEN | Scope-before-candidate and per-edge checks specified; full cross-system test matrix owned by I/F/G/H. |
| DM-011 / INT-P0-03 | OPEN | Forget target inventory and state model defined; backup/external completion policy owned by I. |
| DM-012 | TO_VALIDATE | Bound fan-out/depth and benchmark under representative corpus/hardware. |
| DM-013 | OPEN | Vocabulary registry, schema evolution, unknown enum handling and migration compatibility. |

## 5. Six-dimension review

### Dimension 1 — Architecture and responsibility boundaries

**Result: PASS with conditions.** Brain owns canonical identities, versions, lifecycle history and typed memory assets. E proposes; F reads/projects; G owns Context; H owns wire/Adapter; I owns policy and physical erasure. No Agent planning/tool authority was moved into Brain. Logical boundaries do not prescribe separate processes/crates. Condition: keep all Fact/Claim wire and storage semantics ADR-blocked.

### Dimension 2 — Domain model completeness

**Result: CONDITIONAL PASS.** MemoryVersion, LifecycleEvent, EntityVersion, RelationRevision, ConflictSet, ForgetOperation, ScopeRef and typed references are defined at candidate level. Fact/Claim, Claim revision and Generic Scope remain unresolved. Entity merge/split and Relation migration have explicit immutable records. Evidence remains separate from Claim and trust/confidence/relevance.

### Dimension 3 — Data flow and consistency

**Result: CONDITIONAL PASS.** CAS, immutable history, idempotency receipts, canonical sequence, outbox, rebuildable projections and exact historical references are specified. Lifecycle authority is proposed as append-only LifecycleEvent stream. Atomic commit/outbox and Forget watermark behavior require storage/recovery validation. Context versions remain G-owned.

### Dimension 4 — Security and governance

**Result: CONDITIONAL PASS; integration gate remains.** Scope is not Permission; typed identity, no display-name inference, pre-candidate filtering, per-edge graph checks, separate Evidence authorization, fail-closed behavior and suppression-first Forget are specified. End-to-end enforcement and backup/external deletion semantics remain I-led OPEN items. Memory is always untrusted data.

### Dimension 5 — Performance and resource use

**Result: TO_VALIDATE.** No unsupported latency promises. Explicit limits and measurement targets exist for traversal depth/fan-out, historical reads, CAS contention, merge/split migration, Forget dependency discovery and outbox lag. Benchmarks must not weaken scope/provenance correctness.

### Dimension 6 — Evolvability and observability

**Result: CONDITIONAL PASS.** Opaque IDs, schema versions, typed vocabulary references, append-only revisions, migration records and correlation/causation fields support evolution. Vocabulary registry, unknown enum policy, migration compatibility and audit retention remain OPEN (DM-013).

## 6. Cross-module contract summary

- **E Compiler:** submit proposal + evidence/provenance + source actor/scope/time + idempotency; Brain validates and commits canonical identity/version; no bypass of lifecycle; Fact/Claim output schema blocked by ADR.
- **F Runtime:** scoped canonical reads and exact versions; scope filtering before candidate generation and every graph expansion; projection/cache is disposable and must respect watermarks and Forget fences.
- **G Context:** Context Entry pins Memory ID + MemoryVersion ID; G alone owns ContextVersion/ChangeSet/state machine; canonical mutation emits invalidation/reconciliation signals.
- **H BMCP:** transport opaque typed refs and actor/scope envelope; H owns wire protocol, authentication and Adapter acknowledgement; no display-name identity.
- **I Governance:** authorizes every operation; owns grants/revocation, audit, retention, physical erasure and backup/external policy; Brain exposes dependencies and durable Forget progress; async reauthorization required.

All interfaces require explicit input/output, owner, version semantics, authorization context, structured errors and idempotent retry behavior. Detailed wire fields remain H-owned.

## 7. Remaining blockers

1. INT-P0-01 ADR approval before Claim/Fact schema or interface freeze.
2. I-led end-to-end Scope authorization and negative test matrix (INT-P0-02).
3. I-led Forget completion/backup/external-recipient policy and E/F/G/H derivative acknowledgements (INT-P0-03).
4. Cross-system prompt-injection threat model and tests (INT-P0-04).
5. G-owned ContextVersion/ChangeSet contract (INT-P1-01).
6. H/I/B final ActorRef/Principal identity and scope trust contract (INT-P1-03).
7. Provenance DAG and unique Lifecycle authority validation (INT-P1-06).
8. Vocabulary registry/schema migration compatibility (DM-013).

## 8. Files in this review

This report reviews only the Session D deliverables. It does not claim an external three-party review has occurred. A genuinely independent review should assign separate architecture, Rust engineering, and security reviewers after E/F/G/H/I contracts are available.

**End of review.**
