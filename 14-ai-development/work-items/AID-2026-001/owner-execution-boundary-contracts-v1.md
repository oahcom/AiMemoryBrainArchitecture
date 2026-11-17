# AID-2026-001 — Forget Execution Boundary Contracts v1
# AID-2026-001 — Forget 执行边界契约 v1

**Classification:** ARCH / R3 proposal; non-normative pending owner approval  
**Applies to:** E (Compiler/Orchestration), F (Runtime/Retrieval), G (Context), H (BMCP/Adapter), C (Agent/Inference/Telemetry), Storage/Backup  
**Parent contract:** [Joined Forget / Memory Lifecycle Contract Proposal v1](forget-lifecycle-joined-contract-proposal-v1.md)  
**Test extension:** [R3 Contract Test Matrix](r3-contract-test-matrix.md)  
**Baseline:** PR #72 target base `4f8c5218c8d33f5fdb690a7c4bdb671639ebb807`; this file is a proposal and does not amend owner normative guides.

## 1. Purpose and status

This document converts the high-level execution-boundary table in the joined D/I proposal into owner-specific obligations, interface expectations, evidence requirements, failure behavior and conformance cases. It is deliberately limited to each Owner's existing domain. It does not transfer canonical lifecycle authority from D, governance authority from I, or wire-schema authority from H.

**Status: PROPOSED / OWNER ACKNOWLEDGEMENTS PENDING / IMPLEMENTATION NOT VERIFIED / TESTS NOT RUN.**

No owner is deemed to have approved this document by its inclusion in PR #72. Each Owner must review the exact document SHA and either acknowledge it, submit a bounded change request, or explicitly reject it.

## 2. Shared execution contract

Every execution owner MUST:

1. Consume the canonical opaque `operation_id`, typed `target_id`, `inventory_revision`, required action, current D-issued `fence_generation`, and current I authorization/policy decision reference.
2. Register every in-scope target and derivative it owns before that derivative can become visible. Unknown or unregistered targets are never silently omitted.
3. Re-check the latest fence and applicable authorization at the final local visibility/irreversible-action boundary, not only when work is queued.
4. Produce append-only, integrity-protected evidence bound to `operation_id + inventory_revision + target_id + stage + attempt_id + lease_fence`. Evidence contains no forgotten payload.
5. Report only its own capability-bounded result. `ACK`, `Accepted`, `Delivered`, `Applied`, `Deleted`, `Erased`, and `Completed` are not interchangeable.
6. Fail closed when the current fence, policy, target scope, capability or authoritative state cannot be checked.
7. Treat timeout-after-side-effect as UNKNOWN until reconciled. Do not blindly repeat non-idempotent destructive actions.
8. Preserve evidence across retry, crash, replay, restore and inventory revision changes. A newer inventory revision invalidates older completion evaluation.
9. Expose a deterministic verifier path: fixture, command, expected output, actual output, source SHA, execution SHA and independent reviewer.
10. Never roll back or lower the Forget fence after the D-owned suppression linearization point.

### 2.1 Minimum target evidence envelope

The following is a logical cross-owner envelope, not a final wire schema. H owns encoding; D owns operation/fence semantics; I owns acceptance policy.

| Field | Requirement |
|---|---|
| operation_id / inventory_revision | Stable operation and monotonic inventory identity |
| target_id / target_class / owner_domain | Opaque target identity and accountable domain |
| required_action / action_version | Explicit action and versioned semantics |
| fence_generation | D-issued generation observed and enforced |
| authorization_decision_ref / permission_epoch | Current I decision/epoch at protected execution |
| capability_profile_ref | Declared and validated capability version |
| attempt_id / lease_fence | Unique attempt and current fencing token |
| target_state / result_code | Typed local result; UNKNOWN is explicit |
| evidence_ref / evidence_kind | Immutable evidence reference and evidence class |
| observed_at / verifier | Trusted observation time and verifier identity/method |
| provenance / integrity | Source system, authenticated producer, signature/checksum or equivalent |
| exception_ref / expires_at | Present only for I-approved bounded residual treatment |

No content payload, prompt transcript, hidden reasoning or forgotten bytes may be copied into the evidence envelope.

## 3. Owner E — Compiler and orchestration boundary

**Existing domain:** durable compile-work orchestration, source/provenance transformation, derived-memory production, retries/leases/replay and publication coordination. E does not own canonical lifecycle, Runtime retrieval, ContextVersion, Adapter wire semantics, global authorization policy or physical index implementation.

E MUST:

- Register source/derivative lineage and target inventory before a derived artifact is visible to downstream consumers.
- Keep compiled candidates and staged derivatives non-queryable/non-deliverable until the D canonical commit and the applicable publication gate succeed.
- Bind work items, stage checkpoints, outbox/inbox records and retry attempts to operation/fence generation and authorization/policy epoch.
- Re-check D's current fence and I's current authorization immediately before canonical-write request, index-publication notification and any replay/recompile publication.
- On a fence advance, suppress stale staged output, mark the affected checkpoint with a typed terminal/suppressed disposition, and retain only permitted minimal evidence.
- Treat a worker crash or timeout after an external side effect as uncertain; query/reconcile the side effect before retry.
- Prevent DLQ replay, lease recovery, duplicate event delivery or recompile from creating a new canonical identity from a forgotten source without a separately authorized new source/provenance event.
- Coordinate the producer-admission / dependency-registration / fence-installation race with D and Storage. An E-local preflight check is insufficient to prove atomicity.

**E evidence:** accepted-work identity; source and derivative opaque refs; lineage/dependency registration receipt; stage/checkpoint/attempt IDs; lease fence; canonical commit receipt or rejection; publication-gate decision; replay/DLQ suppression trace; current fence and permission epoch.

**E failure rules:** stale lease cannot commit; same idempotency key + same canonical request returns prior outcome; same key + different digest rejects; fence/policy lookup unavailable blocks publication; unknown external result is reconciled before retry.

## 4. Owner F — Runtime, retrieval, index and cache boundary

**Existing domain:** Recall routing, scope-first retrieval, candidate fusion/ranking, freshness/completeness, activation recommendations, disposable Working Sets and caches. F does not own canonical lifecycle or global policy.

F MUST:

- Enforce scope and authorization before candidate enumeration, ranking, aggregation, counts or evidence expansion that could leak protected information.
- Enforce the current D Forget fence before candidates enter a result set and again immediately before the response/activation handoff. A check performed only at query start is insufficient.
- Bind cache/working-set identity and validity to authenticated principal, effective scope, permission/policy epoch, canonical version and Forget generation. Cache hits cannot bypass a current fence check.
- Prevent in-flight reads and delayed cache fills from returning/reintroducing content when the fence advances during the request.
- Make index rebuilds consume current canonical state and the latest fence high-water mark; old snapshots, stale workers and lagging partitions cannot republish forgotten identities.
- Report index partition/watermark lag separately from Forget completion. An index watermark is not erasure evidence.
- Invalidate affected candidates, caches and Working Sets with generation-aware receipts. If invalidation is asynchronous, the serving path must remain fenced during the lag.
- Return explicit partial/stale/unavailable results when the authoritative fence or policy cannot be checked; never silently serve stale content.

**F evidence:** query trace with scope/policy/fence versions; pre-enumeration and pre-return checks; index partition/generation/watermark; cache namespace and generation; invalidation receipt; rebuild source snapshot and fence high-water mark; negative retrieval assertion.

**F failure rules:** permission/fence service unavailable means fail closed for protected data; stale cache fill is discarded; index lag is visible; rebuild cannot use a snapshot older than the enforced fence generation.

## 5. Owner G — Context, Snapshot, Delta and delivery-intent boundary

**Existing domain:** Context identity and membership, ContextVersion, ChangeSet, Snapshot/Delta planning, delivery intent, reconciliation and Context-side Forget invalidation. G does not own canonical Memory, retrieval/index, global authorization, wire encoding or final Agent inference application.

G MUST:

- Resolve every affected ContextEntry to opaque canonical target references and preserve source/version lineage; do not copy forgotten payload into audit evidence.
- Invalidate or quarantine affected ContextEntries, snapshots, deltas, compaction artifacts and pending delivery intents when the current fence advances.
- Advance the relevant Context revision using the existing G-owned version/concurrency contract; duplicate invalidation is idempotent and stale ChangeSets cannot restore an older membership state.
- Re-check current authorization and Forget generation before planning, dispatching, replaying or reconciling a delivery.
- Mark offline Adapter deliveries stale/superseded and require a full current-state reconciliation before any application after reconnect. No queued delta may be replayed merely because its transport delivery was previously accepted.
- Distinguish Prepared, Delivered, Received, Accepted and Applied. G may record delivery intent and Adapter attestations but cannot invent final-request Applied evidence.
- Preserve the semantic difference between Context Remove (local membership edit) and canonical Forget (governed cross-system suppression).

**G evidence:** affected Context IDs and opaque Entry refs; old/new ContextVersion; invalidation/supersession event; pending-delivery cancellation result; snapshot/delta generation; offline reconnect reconciliation receipt; delivery state transition evidence.

**G failure rules:** stale base version rejects or reconciles; permission/fence unavailable blocks delivery; offline/unknown Adapter remains pending/unknown; Applied is never inferred from Delivered or Accepted.

## 6. Owner H — BMCP and Adapter protocol boundary

**Existing domain:** BMCP wire envelope/versioning, message types, transport interactions, capability negotiation, ACK/attestation encoding and Adapter protocol state machines. H does not redefine D/G domain meaning or I authorization policy; C owns Agent integration semantics.

H MUST:

- Encode the D/I/G-owned logical fields without changing their semantics: operation, opaque target, inventory revision, fence generation, policy/permission epoch references, capability epoch and evidence reference.
- Bind messages and acknowledgements to authenticated Adapter/transport identity, protocol/schema version, delivery/attempt identity, declared coverage and capability epoch.
- Distinguish transport receipt, Adapter receipt, validation acceptance, managed-region clear/quarantine and final inference-boundary application. These are separate acknowledgement classes.
- For Forget, report per-target managed-region coverage and action class (for example suppressed, cleared, quarantined, unsupported, unknown); never map a generic transport ACK to physical erase or global completion.
- Negotiate and version offline buffering, durable queue, idempotency, replay, snapshot/delta, clear/quarantine, reconnect reconciliation and capability-loss behavior.
- Downgrade capability state when the Adapter loses a required ability; invalidate claims that depend on the previous capability epoch.
- Require reconnect reconciliation against current ContextVersion, PermissionEpoch and ForgetFenceGeneration before stale buffered content can be reused.
- Fail closed on incompatible major schema, unknown required action, untrusted principal binding or unverifiable ACK provenance.

**H evidence:** negotiated capability profile and epoch; authenticated Adapter identity; protocol/schema version; message/delivery/attempt IDs; ACK class and declared coverage; signed/integrity-protected receipt; capability downgrade event; reconnect reconciliation trace.

**H failure rules:** timeout or lost response is UNKNOWN unless reconciled; unsupported region is explicit; ACK coverage cannot exceed declared capability; Tier 2/3 cannot claim Tier 1 Full Applied; no protocol-level status may claim global Forget completion.

## 7. Owner C — Agent integration, inference and telemetry boundary

**Existing domain:** Agent-facing integration semantics, telemetry meaning and inference-boundary requirements. C does not own BMCP wire encoding, authorization policy or canonical lifecycle.

C MUST:

- Treat Agent telemetry, plans, intent, reported outcomes and model-generated content as untrusted, scoped claims—not authorization, canonical truth or proof of execution.
- Never infer Forget authorization, lifecycle transitions, deletion completion or policy exceptions from telemetry, model output, tool result text or Agent assertions.
- Preserve source-kind, scope, timestamps, provenance and uncertainty. Do not promote a reported plan/outcome to verified fact without independent evidence.
- Before constructing a new candidate or inference context from memory-derived material, preserve lineage and reject any source whose canonical identity is Forgotten or whose current fence cannot be verified.
- Prevent stale context from being re-emitted as a “new” candidate by dropping the original source identity/provenance. Similar newly supplied information may only enter through a genuinely new authorized source event and new canonical identity, not a synthetic rewrap of forgotten material.
- Keep Brain-managed memory in its designated untrusted data region. Do not elevate it into system/developer instructions, safety policy or tool authorization.
- Respect the immutable in-flight inference boundary. Forget affects future eligible boundaries; do not claim that Brain can retract content already submitted to an external model/provider.
- Avoid requiring hidden chain-of-thought or private scratchpads as Forget evidence or provenance.

**C evidence:** source lineage and source-kind; scope and time qualification; fence-check decision before candidate/context emission; rejection trace for forgotten/unknown sources; final managed-region boundary metadata where observable; no authority-bearing telemetry fields.

**C failure rules:** missing provenance or unavailable fence means do not emit; model/Agent claims cannot override D/I; in-flight request is not retroactively mutable; external provider retention remains a separate I-governed target/exception.

## 8. Storage / Backup execution boundary

**Existing boundary:** Storage and Backup operators own persistence, controlled replicas, backup-set lifecycle and restore mechanics. This document does not assume a separate named Owner exists; accountable Storage/Backup operator must be assigned by the project.

Storage/Backup MUST:

- Atomically persist the canonical Memory transition to Forgotten, D-issued fence generation/tombstone, ForgetOperation state and durable outbox/publication intent, or provide an explicitly reviewed equivalent transactional protocol.
- Guarantee monotonic, durable fence generations across failover and replica promotion. A stale replica must not become an authority that serves a generation lower than the committed high-water mark.
- Make suppression effective before asynchronous physical cleanup begins. If a read path cannot consult the authoritative fence, it must fail closed or be isolated from serving.
- Inventory controlled primary and replica copies, record per-copy erase/de-identify action and evidence, and distinguish logical tombstone from physical erasure.
- Record backup-set identity, coverage, creation/expiry time, retention policy and restore constraints. A backup not yet expired is not erased.
- Before restored data becomes queryable or deliverable, apply the latest Forget fence/high-water mark and reconcile all Forget operations that post-date the backup snapshot.
- Treat restore as a possible resurrection event that invalidates prior completion evaluation until reconciliation finishes.
- Keep audit evidence minimal and content-free; integrity evidence must not become an unauthorized retained copy of forgotten content.

**Storage evidence:** transaction/WAL commit receipt; operation/fence generation; replica high-water observation; per-copy erase/de-identification receipt; backup-set manifest and expiry proof; restore preflight/reconciliation trace; negative query/delivery test after restore.

**Storage failure rules:** no atomicity proof means no suppression-committed claim; replication lag cannot lower the fence; backup restore remains quarantined until fenced; missing backup inventory is UNKNOWN, not erased.

## 9. Cross-owner handshakes (no authority transfer)

| Handshake | Required agreement | Cannot be inferred from |
|---|---|---|
| D ↔ Storage | Atomic linearization and monotonic fence durability | E/F/G local preflight |
| D ↔ E | Producer admission/dependency registration/publication race closure | Compiler-local fence check |
| D ↔ F | Fence semantics and read/rebuild visibility boundary | Cache invalidation ACK alone |
| D ↔ G | Canonical target-to-Context dependency and terminal identity semantics | Context Remove |
| I ↔ each executor | Current authorization, scope, retention/legal-hold re-check and evidence acceptance | Authorization captured only at enqueue |
| G ↔ H ↔ C | Context delivery state vs final inference-boundary attestation | Transport receipt or local buffer digest |
| H ↔ I | Authenticated transport principal, permission epoch and revocation binding | Agent-supplied identity string |
| All executors ↔ I | Target inventory completeness, capability profile and evidence classification | Self-reported “done” without verifiable receipt |

Any unresolved handshake becomes a named blocker with owner, exact question, affected test IDs and fail-closed interim behavior. No team may silently resolve another team's authority.

## 10. Conformance additions

The following tests are specified in the R3 matrix as DFI-013…DFI-022. They are not executed by this document.

| Test | Owner focus | Required negative assertion |
|---|---|---|
| DFI-013 | E producer admission vs Forget fence | No derivative becomes visible when fence wins the race; no late publication after fence |
| DFI-014 | E lease/DLQ/recompile recovery | Stale lease, replay or recompile cannot publish forgotten source |
| DFI-015 | F in-flight Recall/cache fill | No result or cache fill after a newer fence wins before response |
| DFI-016 | F index rebuild | Rebuild from stale snapshot cannot reintroduce forgotten identity |
| DFI-017 | G offline Snapshot/Delta replay | Reconnected Adapter must reconcile before applying; stale delta rejected |
| DFI-018 | G Context Remove vs Forget | Remove changes only Context membership; Forget invalidates every affected projection/delivery |
| DFI-019 | H ACK and capability downgrade | Limited ACK/old capability epoch cannot be promoted to erase or Full Applied proof |
| DFI-020 | C telemetry/inference re-emission | Agent/model claim cannot authorize or re-emit forgotten source as fresh candidate |
| DFI-021 | Storage atomic commit/failover | Crash/failover cannot expose Forgotten content or lose committed fence/operation |
| DFI-022 | Storage backup restore | Restored copy remains quarantined until latest fence is applied; stale backup cannot resurrect content |

Each test requires: exact source contract SHAs; deterministic fixture; concurrency/fault schedule; command; expected and actual output; assertion logs; test harness/version; execution commit SHA; and non-implementing reviewer. If a production component or harness does not yet exist, mark NOT IMPLEMENTED / NOT RUN and record the missing dependency—do not replace it with a prose walkthrough.

## 11. Owner acknowledgement template

Each owner must reply against the exact blob SHA of this document:

- Decision: ACKNOWLEDGED / ACKNOWLEDGED_WITH_CHANGES / REJECTED.
- Owned sections:
- Exact document SHA:
- Confirmed capability boundary:
- Evidence currently available (exact refs/SHAs):
- Missing implementation or tests:
- Cross-owner blockers:
- Tests accepted for this owner:
- Signature/identity and date:

A response from the coordinator or another Owner cannot substitute for the accountable Owner's acknowledgement.

---

# 中文版本

## 1. 目的与状态

本文将 D/I 联合提案中的高层执行边界表，细化为各 Owner 可实现、可测试、可审计的义务、接口预期、证据要求和故障行为。严格限制在各 Owner 既有领域内，不转移 D 的规范生命周期权威、I 的治理权威或 H 的 Wire Schema 权威。

**状态：PROPOSED / OWNER 确认待定 / 实现未验证 / 测试未执行。**

文件进入 PR #72 不代表任何 Owner 已批准。每个 Owner 必须针对准确文档 SHA 审查，并明确确认、提出有边界的修改请求或拒绝。

## 2. 共享执行契约

每个执行 Owner MUST：

1. 消费规范不透明 `operation_id`、类型化 `target_id`、`inventory_revision`、必需动作、D 当前签发的 `fence_generation`，以及 I 当前授权/策略决策引用。
2. 在派生项对下游可见前，登记其拥有的全部范围内目标和派生项。不得静默遗漏未知或未登记目标。
3. 在本地最终可见性/不可逆动作边界重新检查最新 Fence 和适用授权，而不只是入队时检查一次。
4. 生成只追加、完整性受保护的证据，并绑定 `operation_id + inventory_revision + target_id + stage + attempt_id + lease_fence`。证据不得包含已遗忘载荷。
5. 仅报告自身能力范围内的结果。`ACK`、`Accepted`、`Delivered`、`Applied`、`Deleted`、`Erased` 和 `Completed` 不可互换。
6. 无法检查当前 Fence、策略、目标 Scope、能力或权威状态时必须 Fail Closed。
7. 副作用发生后超时应标记 UNKNOWN，直到完成对账。不得盲目重复非幂等破坏性动作。
8. 在 Retry、Crash、Replay、Restore 和清单版本变化中保留证据。新清单版本会使旧完成评估失效。
9. 提供确定性验证路径：Fixture、命令、预期输出、实际输出、源 SHA、执行 SHA 和独立 Reviewer。
10. D 所有的抑制线性化点之后，绝不回滚或降低 Forget Fence。

### 2.1 最低逐目标证据封装

以下是跨 Owner 逻辑封装，不是最终 Wire Schema。H 拥有编码；D 拥有 Operation/Fence 语义；I 拥有接受策略。

| 字段 | 要求 |
|---|---|
| operation_id / inventory_revision | 稳定 Operation 和单调递增清单身份 |
| target_id / target_class / owner_domain | 不透明目标身份和负责领域 |
| required_action / action_version | 明确动作及其版本化语义 |
| fence_generation | 已观察并执行的 D 签发 Generation |
| authorization_decision_ref / permission_epoch | 受保护执行时 I 的当前决策/Epoch |
| capability_profile_ref | 已声明并验证的能力版本 |
| attempt_id / lease_fence | 唯一 Attempt 和当前 Fencing Token |
| target_state / result_code | 类型化本地结果；UNKNOWN 必须明确 |
| evidence_ref / evidence_kind | 不可变证据引用和证据类别 |
| observed_at / verifier | 可信观察时间及验证者身份/方法 |
| provenance / integrity | 来源系统、认证生产者、签名/校验和或等效完整性信息 |
| exception_ref / expires_at | 仅用于 I 批准的有边界残留处置 |

证据封装不得复制内容载荷、Prompt Transcript、隐藏推理或已遗忘字节。

## 3. Owner E — Compiler 与 Orchestration 边界

**既有领域：** 持久化 Compile Work 编排、来源/Provenance 转换、派生记忆生产、Retry/Lease/Replay 和发布协调。E 不拥有规范生命周期、Runtime 检索、ContextVersion、Adapter Wire 语义、全局授权策略或物理 Index 实现。

E MUST：

- 在派生资产对下游可见前，登记来源/派生 Lineage 和目标清单。
- 在 D 规范 Commit 和适用发布 Gate 成功前，保持编译 Candidate 和暂存派生项不可查询、不可交付。
- 将 Work Item、阶段 Checkpoint、Outbox/Inbox 和 Retry Attempt 绑定到 Operation/Fence Generation 及授权/策略 Epoch。
- 在 Canonical Write Request、Index Publication Notification 及任何 Replay/Recompile 发布前，重新检查 D 当前 Fence 和 I 当前授权。
- Fence 前进时抑制陈旧暂存输出，将相关 Checkpoint 标记为类型化终止/抑制结果，并仅保留策略允许的最小证据。
- Worker Crash 或外部副作用后超时时，视为结果不确定；重试前查询/对账副作用。
- 防止 DLQ Replay、Lease Recovery、重复 Event Delivery 或 Recompile 基于已遗忘来源创建新 Canonical Identity，除非存在独立授权的新来源事件。
- 与 D 和 Storage 协调 Producer Admission / Dependency Registration / Fence Installation 竞态。E 本地预检查不足以证明原子性。

**E 证据：** Accepted Work 身份；来源和派生不透明引用；Lineage/Dependency Registration Receipt；Stage/Checkpoint/Attempt ID；Lease Fence；Canonical Commit Receipt 或 Rejection；Publication Gate 决策；Replay/DLQ 抑制 Trace；当前 Fence 和 Permission Epoch。

**E 故障规则：** 陈旧 Lease 不得提交；相同幂等 Key 和相同规范请求返回先前结果；相同 Key 和不同 Digest 拒绝；Fence/Policy 查询不可用时阻止发布；外部结果未知时先对账再重试。

## 4. Owner F — Runtime、Retrieval、Index 与 Cache 边界

**既有领域：** Recall 路由、Scope 优先检索、Candidate 融合/排序、新鲜度/完整性、Activation Recommendation、可丢弃 Working Set 和 Cache。F 不拥有规范生命周期或全局策略。

F MUST：

- 在 Candidate 枚举、排序、聚合、计数或可能泄露受保护信息的 Evidence 展开前执行 Scope 和授权过滤。
- 在 Candidate 进入结果集前执行 D 当前 Forget Fence，并在响应/Activation 交接前再次执行。仅在 Query 开始时检查不够。
- 将 Cache/Working Set 身份及有效性绑定到认证 Principal、有效 Scope、Permission/Policy Epoch、Canonical Version 和 Forget Generation。Cache Hit 不能绕过当前 Fence 检查。
- Fence 在请求期间前进时，阻止在途读取和延迟 Cache Fill 返回/重新引入内容。
- 让 Index Rebuild 消费当前 Canonical 状态和最新 Fence High-water Mark；旧 Snapshot、陈旧 Worker 和落后 Partition 不得重新发布 Forgotten Identity。
- 分开报告 Index Partition/Watermark 延迟与 Forget 完成。Index Watermark 不是擦除证据。
- 使用 Generation 感知 Receipt 失效受影响 Candidate、Cache 和 Working Set。若失效异步进行，服务路径在延迟期间仍必须受 Fence 保护。
- 无法检查权威 Fence 或 Policy 时，返回明确 Partial/Stale/Unavailable 结果，绝不静默提供陈旧内容。

**F 证据：** 带 Scope/Policy/Fence 版本的 Query Trace；枚举前与返回前检查；Index Partition/Generation/Watermark；Cache Namespace/Generation；失效 Receipt；Rebuild 来源 Snapshot 和 Fence High-water Mark；负向 Retrieval 断言。

**F 故障规则：** Permission/Fence 服务不可用时，受保护数据 Fail Closed；陈旧 Cache Fill 丢弃；Index 延迟必须可见；Rebuild 不得使用早于已执行 Fence Generation 的 Snapshot。

## 5. Owner G — Context、Snapshot、Delta 与 Delivery Intent 边界

**既有领域：** Context 身份和成员、ContextVersion、ChangeSet、Snapshot/Delta 规划、Delivery Intent、协调及 Context 侧 Forget 失效。G 不拥有 Canonical Memory、Retrieval/Index、全局授权、Wire 编码或 Agent 最终推理应用。

G MUST：

- 将受影响 ContextEntry 解析到不透明 Canonical Target 引用并保留来源/版本 Lineage；不得把已遗忘载荷复制到审计证据。
- Fence 前进时，失效或隔离受影响 ContextEntry、Snapshot、Delta、Compaction Artifact 和待处理 Delivery Intent。
- 使用 G 所有的版本/并发契约推进相关 Context Revision；重复失效必须幂等，陈旧 ChangeSet 不得恢复旧成员状态。
- 在规划、Dispatch、Replay 或 Reconcile Delivery 前，重新检查当前授权和 Forget Generation。
- 将离线 Adapter Delivery 标记为 Stale/Superseded；重连后应用任何内容前，必须先对账完整当前状态。不得仅因某个 Delta 曾被传输接受，就重新 Replay。
- 区分 Prepared、Delivered、Received、Accepted 和 Applied。G 可以记录 Delivery Intent 和 Adapter Attestation，但不能伪造最终请求 Applied 证据。
- 保留 Context Remove（局部成员编辑）与 Canonical Forget（受治理的跨系统抑制）之间的语义差异。

**G 证据：** 受影响 Context ID 和不透明 Entry 引用；旧/新 ContextVersion；失效/Supersession Event；待处理 Delivery 取消结果；Snapshot/Delta Generation；离线重连对账 Receipt；Delivery 状态转换证据。

**G 故障规则：** Base Version 过期时拒绝或对账；Permission/Fence 不可用时阻止 Delivery；离线/未知 Adapter 保持 Pending/Unknown；绝不从 Delivered 或 Accepted 推断 Applied。

## 6. Owner H — BMCP 与 Adapter 协议边界

**既有领域：** BMCP Wire Envelope/版本、消息类型、传输交互、能力协商、ACK/Attestation 编码和 Adapter 协议状态机。H 不重新定义 D/G 领域含义或 I 授权策略；C 拥有 Agent 集成语义。

H MUST：

- 编码 D/I/G 所有的逻辑字段，但不得改变其语义：Operation、不透明 Target、Inventory Revision、Fence Generation、Policy/Permission Epoch 引用、Capability Epoch 和 Evidence Reference。
- 将消息和 ACK 绑定到认证 Adapter/Transport Identity、协议/Schema 版本、Delivery/Attempt Identity、声明覆盖范围和 Capability Epoch。
- 区分 Transport Receipt、Adapter Receipt、Validation Acceptance、Managed-region Clear/Quarantine 和最终推理边界 Application。这些是不同 ACK 类别。
- Forget ACK 必须报告逐目标 Managed-region 覆盖范围和动作类别（例如 suppressed、cleared、quarantined、unsupported、unknown）；不得把通用 Transport ACK 映射成物理擦除或全局完成。
- 协商并版本化 Offline Buffering、Durable Queue、Idempotency、Replay、Snapshot/Delta、Clear/Quarantine、Reconnect Reconciliation 和 Capability-loss 行为。
- Adapter 丧失必需能力时降级 Capability State；使依赖旧 Capability Epoch 的声明失效。
- 要求离线 Adapter 重连后，在复用陈旧缓冲内容前，先根据当前 ContextVersion、PermissionEpoch 和 ForgetFenceGeneration 完成对账。
- 对不兼容主 Schema、未知必需动作、不可信 Principal Binding 或不可验证 ACK Provenance 执行 Fail Closed。

**H 证据：** 已协商 Capability Profile/Epoch；认证 Adapter 身份；协议/Schema 版本；Message/Delivery/Attempt ID；ACK Class 和声明覆盖范围；签名/完整性保护 Receipt；Capability Downgrade Event；Reconnect Reconciliation Trace。

**H 故障规则：** 超时或响应丢失时为 UNKNOWN，除非已完成对账；不支持区域必须明确报告；ACK 覆盖不得超出声明能力；Tier 2/3 不得声称 Tier 1 Full Applied；任何协议状态不得声明全局 Forget 完成。

## 7. Owner C — Agent 集成、推理与 Telemetry 边界

**既有领域：** Agent 集成语义、Telemetry 含义和推理边界要求。C 不拥有 BMCP Wire 编码、授权策略或规范生命周期。

C MUST：

- 将 Agent Telemetry、Plan、Intent、Reported Outcome 和模型生成内容视为不可信、带 Scope 的声明，而不是授权、规范真相或执行证明。
- 绝不从 Telemetry、模型输出、工具结果文本或 Agent 声明推断 Forget 授权、生命周期转换、删除完成或策略例外。
- 保留 Source Kind、Scope、时间戳、Provenance 和不确定性。没有独立证据，不得将 Reported Plan/Outcome 提升为 Verified Fact。
- 在基于 Memory 派生材料构造新 Candidate 或推理 Context 前保留 Lineage；若来源 Canonical Identity 为 Forgotten 或无法验证当前 Fence，必须拒绝。
- 防止通过丢弃原始 Source Identity/Provenance，把陈旧 Context 重新包装成“新”Candidate。相似的新提交信息只能通过真正新的、经授权的来源事件和新的 Canonical Identity 进入，不能通过合成包装已遗忘材料进入。
- 将 Brain-managed Memory 保持在指定的不可信数据区域。不得提升为 System/Developer Instruction、安全策略或工具授权。
- 遵守不可变的在途推理边界。Forget 影响未来符合条件的边界；不得声称 Brain 可以撤回已提交给外部模型/Provider 的内容。
- 不要求隐藏 Chain-of-Thought 或私有 Scratchpad 作为 Forget 证据或 Provenance。

**C 证据：** Source Lineage 和 Source Kind；Scope/时间限定；Candidate/Context 输出前 Fence 检查决策；Forgotten/Unknown 来源拒绝 Trace；可观察时的最终受管区域边界元数据；不存在权威性 Telemetry 字段。

**C 故障规则：** Provenance 缺失或 Fence 不可用时不得输出；模型/Agent 声明不能覆盖 D/I；在途 Request 不可追溯修改；External Provider Retention 属于 I 治理的独立目标/例外。

## 8. Storage / Backup 执行边界

**既有边界：** Storage 和 Backup Operator 负责持久化、受控 Replica、Backup Set 生命周期和 Restore 机制。本文不假设仓库中已有独立命名 Owner；项目必须指定负责的 Storage/Backup Operator。

Storage/Backup MUST：

- 原子持久化规范 Memory → Forgotten 转换、D 签发 Fence Generation/Tombstone、ForgetOperation 状态和 Durable Outbox/Publication Intent，或提供经过明确审查的等效事务协议。
- 保证 Fence Generation 在 Failover 和 Replica Promotion 后仍单调、持久。陈旧 Replica 不得成为低于已提交 High-water Mark 的内容服务权威。
- 在异步物理清理开始前使抑制生效。如果读取路径无法查询权威 Fence，必须 Fail Closed 或禁止该路径提供服务。
- 清点受控 Primary/Replica 副本，记录每个副本的 Erase/De-identify 动作和证据，并区分逻辑 Tombstone 与物理擦除。
- 记录 Backup Set 身份、覆盖范围、创建/到期时间、Retention 策略和 Restore 约束。尚未到期的 Backup 不能算作已擦除。
- 在 Restore 数据变为可查询/可交付前，应用最新 Forget Fence/High-water Mark，并对账 Backup Snapshot 之后发生的全部适用 Forget Operation。
- 将 Restore 视为潜在复活事件；在对账完成前使此前完成评估失效。
- 保持审计证据最小化且不包含内容；完整性证据不得成为未经授权保留的已遗忘内容副本。

**Storage 证据：** Transaction/WAL Commit Receipt；Operation/Fence Generation；Replica High-water Observation；逐副本 Erase/De-identification Receipt；Backup Set Manifest 和到期证明；Restore Preflight/Reconciliation Trace；Restore 后负向 Query/Delivery 测试。

**Storage 故障规则：** 没有原子性证明不得声明 SuppressionCommitted；Replication Lag 不得降低 Fence；Backup Restore 在 Fence 前保持 Quarantined；Backup 清单缺失是 UNKNOWN，不是已擦除。

## 9. 跨 Owner 握手（不转移权威）

| 握手 | 必须达成的一致意见 | 不能从以下内容推断 |
|---|---|---|
| D ↔ Storage | 原子线性化和 Fence 单调持久化 | E/F/G 本地预检查 |
| D ↔ E | Producer Admission/Dependency Registration/Publication 竞态关闭 | Compiler 本地 Fence 检查 |
| D ↔ F | Fence 语义和 Read/Rebuild 可见性边界 | 单独的 Cache Invalidation ACK |
| D ↔ G | Canonical Target 到 Context Dependency 的映射及终态身份语义 | Context Remove |
| I ↔ 各执行方 | 当前授权、Scope、Retention/Legal Hold 复查和证据接受 | 仅入队时捕获的授权 |
| G ↔ H ↔ C | Context Delivery 状态与最终推理边界 Attestation | Transport Receipt 或 Local Buffer Digest |
| H ↔ I | 认证 Transport Principal、Permission Epoch 和 Revocation 绑定 | Agent 提供的身份字符串 |
| 全部执行方 ↔ I | 目标清单完整性、Capability Profile 和证据分类 | 没有可验证 Receipt 的自报“完成” |

未解决握手必须登记为明确 Blocker，包含 Owner、准确问题、受影响测试 ID 和 Fail-closed 临时行为。任何团队不得静默解决其他团队的权限问题。

## 10. 一致性测试扩展

以下测试在 R3 矩阵中定义为 DFI-013…DFI-022。本文不表示这些测试已经执行。

| 测试 | Owner 重点 | 必须成立的负向断言 |
|---|---|---|
| DFI-013 | E Producer Admission 与 Forget Fence 竞态 | Fence 获胜时不得有派生项可见；Fence 之后不得迟到发布 |
| DFI-014 | E Lease/DLQ/Recompile Recovery | 陈旧 Lease、Replay 或 Recompile 不得发布已遗忘来源 |
| DFI-015 | F 在途 Recall/Cache Fill | 新 Fence 在响应前获胜时，不得返回结果或填充 Cache |
| DFI-016 | F Index Rebuild | 基于陈旧 Snapshot 的 Rebuild 不得重新引入 Forgotten Identity |
| DFI-017 | G 离线 Snapshot/Delta Replay | Adapter 重连后必须先 Reconcile；陈旧 Delta 被拒绝 |
| DFI-018 | G Context Remove 与 Forget | Remove 仅改变 Context 成员；Forget 使所有受影响投影/Delivery 失效 |
| DFI-019 | H ACK 和 Capability Downgrade | 有限 ACK/旧 Capability Epoch 不得升级为擦除或 Full Applied 证明 |
| DFI-020 | C Telemetry/Inference 再输出 | Agent/模型声明不得授权或将已遗忘来源重新输出为新 Candidate |
| DFI-021 | Storage 原子提交/Failover | Crash/Failover 不得暴露 Forgotten 内容或丢失已提交 Fence/Operation |
| DFI-022 | Storage Backup Restore | 恢复副本在应用最新 Fence 前保持 Quarantined；旧 Backup 不得复活内容 |

每项测试必须记录：准确源契约 SHA；确定性 Fixture；并发/故障调度；命令；预期与实际输出；断言日志；测试 Harness/版本；执行 Commit SHA；非实施者 Reviewer。如果生产组件或 Harness 尚不存在，必须标记 NOT IMPLEMENTED / NOT RUN 并记录缺失依赖，不能用文字演练替代。

## 11. Owner 确认模板

每位 Owner 必须针对本文准确 Blob SHA 回复：

- 决策：ACKNOWLEDGED / ACKNOWLEDGED_WITH_CHANGES / REJECTED。
- 所属章节：
- 准确文档 SHA：
- 确认的能力边界：
- 当前可用证据（准确引用/SHA）：
- 缺失的实现或测试：
- 跨 Owner 阻塞项：
- 本 Owner 接受的测试：
- 签名/身份与日期：

协调人或其他 Owner 的回复不能代替责任 Owner 本人的确认。
