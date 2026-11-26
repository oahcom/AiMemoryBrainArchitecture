---
document_metadata:
  domain: memory-runtime
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
        - "original source blob: a934491950c876701e8ac592a0e6aaea983b44e3"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact source Blob pinned; translated body retained; semantic parity review pending."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope_keywords:
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/working-set-and-cache.md"
    en: "docs/en/05-memory-runtime/working-set-and-cache.md"
    zh-CN: null
---

# Runtime Working Set 与 Cache

- 文档 ID：F-WORKING-SET-001
- 版本：1.0
- Owner：Session F — MR-03
- 源分支：session-f-memory-runtime
- 源 Blob：a934491950c876701e8ac592a0e6aaea983b44e3
- 对应英文：[Runtime Working Set and Cache](../../en/05-memory-runtime/working-set-and-cache.md)
- 状态：Authority/Isolation Semantics 已 DECIDED；Cache Topology 为 CANDIDATE；Sizing/TTL 为 TO_VALIDATE

## 1. 目的

定义有界、可丢弃的 Runtime-local State，用于加速 Recall，但不得成为 Canonical Memory，也不得绕过 Scope、Permission、Forget 或 Version Check。

## 2. 范围

拥有 Runtime Working Set、Session Isolation、Hot-memory/Entity/Query/Index Cache、Key Construction、Invalidation、TTL、Capacity Eviction 和 Cache Observability。

不拥有 Canonical Persistence、Index Publication、Context Version、Agent Planning State、Global Authorization Policy 或 Physical Deletion。

## 3. 职责 / 非职责

Working Set 是一个有界集合，包含 Runtime Session 中使用的 Active Reference，以及可选的、经过授权的 Materialized Snippet。它不是完整 Memory Database、持久化 User Profile、Context 或 Agent Plan。

Cache 只是优化：Cache Miss 必须保持正确性；Cache Hit 不能削弱正确性。

## 4. 输入 / 输出

输入：RuntimeSession Trusted Identity/Scope、准确 Memory Version Ref、已授权 Candidate/Evidence Metadata、Permission/Forget Epoch、Index Watermark、Canonical Change Event 和 Invalidation Event。

输出：已授权 Cache Hit/Miss；同一 Session 的 Working Set Snapshot；Invalidation/Eviction Event；Metric。任何 Cache API 都不得返回未经验证的受保护内容。

## 5. 数据模型

WorkingSet：runtime_session_id、session_generation、principal_ref、normalized_scope_digest、environment_scope_id、permission_epoch_ref + policy_domain/issuer、forget_fence_ref + forget_fence_generation、entries[]、byte/entry budget、created_at、expires_at。

WorkingSetEntry：memory_id、memory_version_id、scope_digest、permission_epoch_ref、forget_fence_ref/generation、适用时的 source_index_partition/generation、lifecycle snapshot、provenance refs、可选的有界 Rendering、inserted_at、last_accessed_at、expiry、F-local invalidation generation。优先保存 Reference；Materialized Content 是可选项，并需单独 Access Control。

Cache Family：
- Hot Memory Cache：准确 Memory Version Metadata/Rendering；Key 包含 memory_id + version_id + scope/auth epochs。
- Entity Cache：Canonical Entity Identity/Profile Version 和已授权 Alias；包含 Entity Scope 和 Policy Epoch。
- Query Cache：Query Fingerprint + Principal/Scope/Environment + Policy/Forget Epoch + Retrieval Config + Index Watermark + Consistency Fence。
- Index Cache：Backend-local Posting/Vector/Graph/Temporal Page；必须物理分区，或实施安全的 Scoped Access Semantics。

## 6. Session Isolation

每个 Runtime Session 都有自己的 Working Set Namespace。Agent、Agent Instance、Task、Session 或 Environment 之间不得隐式共享。

只有当低层 Cache Key 完整分区 Principal、Scope、Environment、Permission/Forget Epoch 和准确 Version，且每次 Read 都重新授权时，才允许跨 Session 复用。

Session Close 时销毁 Working Set Namespace，或使其不可访问，并等待有界清理。

## 7. Cache Key

Cache Key 必须绑定所有可能改变可见性/语义的维度：
- authenticated principal/tenant；
- ownership/applicability Scope Set（Canonical Sorted ID，不是 Display Name）；
- 需要时的 Agent/Instance/Session/Task/Environment 维度；
- I PermissionEpoch Ref 及其 Policy-domain/Issuer Binding（不透明，由 I 校验）；
- D ForgetFence Ref/Generation 及适用 Target/Lineage Coverage（不透明，由 D 校验）；
- 准确 Memory/Entity Version，或 Index Generation/Watermark；
- Normalized Query Fingerprint 和 Filter；
- Retrieval/Activation Policy Configuration Version；
- 时间改变 Validity 时使用的 Temporal Bucket；
- 缓存 Evidence 时使用的 Evidence Access Class。

缺少任何必需维度时，不得缓存受保护结果。Cache Key 本身不是 Authorization；Hit 必须通过当前 Authorization 和 Canonical/Forget Validation。

## 8. Invalidation 与 Forget — INT-P0-03

Forget 是异步 Physical Cleanup 之前的 Logical Access Barrier。I/D 发布持久化 Forget Fence 后：

1. 读取持久化 D ForgetFence Ref/Generation，并将所有覆盖的 Target/Descendant 标记为不可读。只有 D 能推进 ForgetFenceGeneration；F 只能推进自己的 Local Invalidation Generation。
2. 立即阻止该 Target 的 Candidate Generation 和 Cache Return，包括 In-flight Result。
3. 从所有受影响 Working Set 中移除或隔离 Target Reference/Materialized Data。
4. 取消或标记 In-flight Retrieval/Activation Task 为 Stale；Response/G Handoff 前再次检查 Fence。
5. 使 Hot-memory、Entity、Query 和 Index-derived Cache Entry 失效；即使 Physical Purge 延迟，也必须通过 Fence 拒绝 Read。
6. 持久化 Invalidation Progress 并报告逐 Target Status；Runtime 不得声称已完成 Global Physical Erasure。
7. Rebuild/Index Replay 必须检查 Canonical Forget State 和 Tombstone，防止已遗忘内容复活。

Runtime 不拥有 Forget Completion。它向 I 报告 Suppression、Cache/Working Set Invalidation 和 Residual Status。Tombstone Retention 由 I/D 管理，不得违反 Policy 保留被遗忘内容。

## 9. Permission Revocation

Revocation Epoch 改变时，即使 Physical Eviction 尚未完成，受影响 Entry 也必须立即不可读。Cache Hit Return、Working Set Reuse、Evidence Dereference 和 G Handoff 前都要重新验证。如果无法取得当前 Policy Epoch，则 Fail-closed。

Revocation 可能只影响 Session 的一部分；Invalidation 必须准确识别受影响的 Principal/Scope/Resource Dimension。

## 10. Memory Version Change / Lifecycle

新的 Canonical Version 使依赖旧 Version 的 Exact-version Hot Entry 和 Query Result 失效。只有 Canonical Policy 允许历史读取时，旧不可变 Version 才能继续访问。

Lifecycle Transition（Superseded、Retracted、Archived、Forgotten）使 Derived Recommendation 失效；Forget 始终具有 Suppressive Effect。Index Generation 变化会使依赖 Index 的 Query Entry 失效或逐渐过期。

## 11. TTL 与 Capacity Eviction

TTL 只是优化边界，不能替代 Revocation 或 Forget。不同 Cache Family 可以有不同候选 TTL 和 Sensitivity；全部为 CANDIDATE/TO_VALIDATE。

Capacity Eviction 可以采用 LRU/LFU/Segmented Policy，但绝不能 Evict Authoritative Data，因为 F 不拥有 Authoritative Data。Eviction 后正确性回退到已授权 Source Read。

Working Set 必须具有严格的 Per-session/Global Byte/Entry Limit，并实施 Admission Control。

## 12. 故障处理

Invalidation Event 丢失时，通过每次 Read 比较 Epoch/Fence 修复。Cache Service 故障时降级为 Uncached Retrieval。Stale Cache Entry 必须丢弃；如果可能泄露被禁止内容，不能仅加 Warning 后返回。

Session Identity 不匹配或 Scope 有歧义时，清除访问资格。Partial Invalidation Status 必须可观察；受影响 Target 必须 Fail-closed。

## 13. 性能预算

按 Per-session Bytes/Entries、Global Cache Bytes、Entry Size、Query Cardinality 和 In-flight Fill 限制内存。避免缓存大型 Evidence Payload。测量 Key Hashing/Epoch Validation 的 CPU 成本；预算 RAM；Disk Cache 可选，但必须按照 I Policy 加密/分区；Runtime Cache 不使用 GPU Memory。数值限制/TTL 为 TO_VALIDATE。

## 14. 可观测性

指标包括：按 Cache Family 区分的 Hit/Miss/Eviction、Invalidation Lag、Stale-entry Suppression、Working Set Size/Age、Per-session Quota Pressure、Invalidation Failure、Cache Rebuild 和 Epoch Mismatch。

绝不暴露未授权 Object Count/Content。使用 Correlation ID 和符合 Policy 的 Resource Ref 审计 Forget/Revocation Invalidation State Transition。

## 15. 接口

D 提供 Canonical Version/Lifecycle 和 Forget State；E 提供 Index Generation/Publication Event；I 提供 Permission/Revocation 和 Forget Fence；G 可以提供只读 Context Version，避免重复 Proposal，但不提供其权威 Entry；Runtime Scheduler 控制 Session Teardown/Cancellation。

Event Payload 必须包含 Resource/Scope Ref、Epoch、Generation、Idempotency、Schema Version 和 Retry Semantics。

## 16. 测试场景

跨 Session/Environment Key Collision；不同 Principal/Policy Epoch 下的同一 Query；Cache Fill 后 Permission 被撤销；Query In-flight 时发生 Forget；Cache Service 宕机；Invalidation Event 丢失但 Epoch 已推进；Memory Version 改变；Rebuild 后 Stale Index Cache；Session Close；Capacity Eviction；Index Rebuild/Replay 后已遗忘 Memory 不得复现。

## 17. 依赖

D Canonical Version/Lifecycle/Forget Identifier；E Index Generation/Rebuild Feed；G Context Read-only Hint；H Authenticated Session Identity；I Policy Epoch/Revocation/Forget Contract 和 Storage Protection。

## 18. 开放问题

OPEN：I Revocation Epoch Scope/Propagation SLA；D/E Forget Tombstone Format/Retention；G Minimal Context Summary；H Session Identity Semantics。

CANDIDATE：In-memory Per-session Working Set + Shared but Strictly Partitioned Read-through Cache。

TO_VALIDATE：TTL、Eviction Algorithm、Memory Limit 和目标硬件上的 Hit-rate Benefit。

## 19. Routing / Scheduling

Working Set Admission 只能发生在 Request Authorization 和 Session Binding 之后。Retrieval 只能将通过 Scope-before-Candidate 和 Canonical/Forget Revalidation 的 Candidate 放入 Working Set。

Scheduler 在插入前强制执行 Per-session/Global Entry/Byte Budget；Interactive Work 优先于 Background Warming；Session Close、Revocation 或 Forget 时取消 Fill。

只有在完整 Authorization/Freshness Key 匹配时，才允许 Coalesce Cache Fill；否则必须在隔离 Namespace 中执行请求。

## Phase 3.5 — Forget Fence 与 Permission Invalidation 补充（规范性补充）

详细 Contract 和 Conformance Case 见 [Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract](../../governance/documentation-gaps.md)。本补充在不一致时取代之前的临时措辞。

### 必需 Cache/Working Set Binding

每个受保护 Cache Key 和 Working Set Namespace，按适用情况绑定：Authenticated Principal/Issuer/Security Domain；Canonical ScopeRef Set；Agent/Instance/Task/Session/Environment；I PermissionEpoch；D ForgetFence Ref/Generation；准确 Memory/Entity Version 或 Index+Partition+Generation+Watermark+Coverage/Schema；Query/Filter Fingerprint；Retrieval Configuration；Temporal Validity；Evidence Access Class。

缺少必需维度时不得 Admission 受保护 Cache。Key 不是 Authorization：每次 Hit 都必须重新验证当前 I Permission 和 D Fence/Lifecycle。

### Invalidation 后置条件

- **Forget：** 立即拒绝 Target/Descendant/Lineage Read；Evict/Quarantine Hot-memory/Entity/Query/Index-derived Entry；移除或使匹配 Working Set Ref/Snippet 不可访问；取消 In-flight Retrieval/Fill；在 Fill Publication 和 Final Return 前再次检查。
- **Permission Revocation：** 立即拒绝旧 Epoch Access；即使 Physical Eviction 延迟，也必须使受影响 Principal/Scope/Resource Namespace 和 Working Set 失效。
- **Duplicates：** 相同 Event/Operation ID + 相同 Target Digest 是幂等操作；Digest 改变则冲突。重复请求不得回退 Tombstone 或恢复 Entry。
- **Lost Notifications：** Durable D/I State 是权威。每次 Read 都重新验证；Reconnect/Anti-entropy 通过连续 Checkpoint 协调。存在 Gap 或 Authority 不可用时，受影响 Namespace 必须 Quarantine，直到 Resync。
- **Reconnect：** Authenticate，获取当前 I PermissionEpoch 和 D Fence，协调 G Context Target，然后才恢复仍符合资格的 Entry。绝不允许先恢复旧 Working Set、之后再清理。

### Cache Miss 与 Stale Entry

**Cache Miss** 表示完整 Key 对应的 Entry 不存在，允许正常的已授权 Source Read。

**Stale Entry** 表示 Entry 存在，但其 Authorization、Fence、Scope、Version、Watermark/Schema、Session 或 Environment Dimension 已过期/无法验证；必须 Drop/Quarantine，绝不能返回。如果 D/I Authority 不可用，不得将 Stale Hit 降级为 Miss 后继续提供。

TTL 只是优化，不是 Forget/Revocation Mechanism。F-local Invalidation Evidence 不构成 Global Completion 或 Physical Erasure 证明。

## Phase 3.5 Reprocessing — 类型化 Invalidation 与 Target Evidence

本节取代上文任何通用的 “Forget Epoch” 用法：F 不创建或推进 D Fence。

1. 每个受保护 Cache Key/Working Set Namespace 绑定 Authenticated Principal/Security Domain、Canonical Owner/Applicability ScopeRef、必需的 Agent/Instance/Task/Session/Environment Dimension、I PermissionEpoch Domain/Issuer、D ForgetFence Ref/Generation、准确 MemoryVersion/EntityVersion 或 Index+Partition+Generation+Coverage/Schema/Watermark，以及适用的 Query/Config/Temporal/Evidence Dimension。
2. Key 永远不是 Authorization。Hit 必须在 Payload Access 前验证当前 I Permission 和 D Target/Lineage Fence，然后验证 Canonical Version/Lifecycle，以及独立的 Evidence/Provenance Authorization。
3. Forget 时，F 只推进自己的 Invalidation Generation；阻止 Target/Descendant；Evict/Quarantine 匹配的 Hot/Entity/Query/Index-derived Entry；清除或使匹配 Working Set Ref/Snippet 不可访问；取消匹配的 In-flight Work/Fill；阻止迟到 Fill Publication。Revocation 对受影响 Principal/Scope/Resource Namespace 产生同样的逻辑拒绝效果。
4. Notification 只是优化。权威来源是 Durable D Fence/Target State 和 I PermissionEpoch/Revocation State。Checkpoint 丢失/出现 Gap 时，受影响 Namespace 必须 Quarantine，直到通过 Snapshot + Contiguous Replay 协调；没有经过验证的 Snapshot Base，绝不能将 Checkpoint 重置到 Latest。
5. Reconnect 顺序：Authenticate → 获取当前 I PermissionEpoch → 获取当前 D ForgetFence → 协调 G Context Target/Delivery State → Invalidate 旧 Working Set → 只恢复经过独立授权且未被 Fence 覆盖的准确 Version。禁止 Restore-first/Clean-later。
6. I 拥有 TargetId 和 Sealed Closed-world Inventory。F 报告 Per-index/Per-partition Watermark、Coverage/Schema、Suppression/Invalidation Checkpoint、受影响 Scope/Lineage Digest 和本地 Residual Status；F 不创建 TargetId，也不将 I 的 Global Target/Component 标记为 Confirmed。
7. Cache Miss 表示完整 Key 无 Entry，允许正常授权 Read。Stale Entry 表示一个或多个绑定维度已过期、不匹配、不完整或无法验证；必须 Drop/Quarantine，绝不能 Serve。D/I Authority 不可用时，不得将 Stale 降级为 Miss 后提供。
8. 相同 Owner Namespace + Operation/Event ID + Target Digest 的重复 Invalidation 必须幂等。相同 Idempotency Identity 配不同 Digest 属于冲突；重复或重试都不得恢复内容或回退 Tombstone。
