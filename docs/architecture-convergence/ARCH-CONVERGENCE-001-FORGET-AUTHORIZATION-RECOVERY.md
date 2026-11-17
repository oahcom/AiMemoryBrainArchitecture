# ARCH-CONVERGENCE-001 — Forget, Authorization & Recovery Safety
# ARCH-CONVERGENCE-001 — Forget、授权与恢复安全合同

- Workstream: C — Forget, Authorization & Recovery Safety
- Status: **DRAFT / CONDITIONAL SAFETY CONTRACT / NON-NORMATIVE**
- Review anchor: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Sources: D `session-d-memory-brain-2026-11-16@194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`; E `session-e-memory-compiler-2026-11-16@ee098e14747d9915de5b3efb63b3a8dd77f670ed`; F `session-f-memory-runtime@1908ce4d233b20f7cafd00cb679affd01bd15174`; G `session-g-memory-context@763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`; H fetched branch `session-h-bmcp-protocol@6608cde89d959257db612d8ff8080f631333f3f3`; I `session-i-security-governance-2026-11-16@0d071bf1ee7cc71912398c6ae57e4496e08f44ab`; Storage `session-storage-consistency-forget-atomicity-2026-11-16@830a559bd2f4ec72608f5a51e1a0b43779f2b989`.
- Authority rule: this proposal does not replace D/I/F/G/H/Storage Owner state machines or claim production proof.

## 1. Executive safety disposition / 安全结论

Forget must be treated as three separate outcomes:

1. **Logical suppression:** D's durable ForgetFence makes covered canonical targets, descendants and registered derivatives unavailable to ordinary reads, candidate generation, reference resolution and new publication.
2. **Asynchronous cleanup:** E/F/G/H/Storage and registered recipients perform their own cleanup/invalidation and return target-scoped evidence.
3. **Physical erasure / global completion:** I evaluates backup, external-copy, recipient, retention and residual-exception obligations. D or an Adapter cannot declare this complete.

D's canonical Forget semantics are DECIDED in its Owner source, but cross-module execution and I global completion remain OPEN. I's PermissionEpoch and protected authorization conditions are confirmed as its normative technical baseline, while external governance profile approval and implementation remain blocked. The I global inventory contract is CANDIDATE; Storage restore proof is CANDIDATE; H ACK behavior is CANDIDATE; F runtime semantics are DECIDED in its addendum but implementation and cross-owner interfaces are not verified.

**No successful DELETE, HTTP/gRPC response, queue ACK, local suppression marker, index watermark or workflow completion proves global Forget.**

Forget 必须拆分为三个独立结果：

1. **逻辑抑制：** D 的持久化 ForgetFence 使覆盖的规范目标、后代及已登记派生物不能被普通读取、候选生成、引用解析或新发布。
2. **异步清理：** E/F/G/H/Storage 和已登记接收方分别执行清理/失效，并返回目标范围明确的证据。
3. **物理擦除/全局完成：** I 评估备份、外部副本、接收方、保留策略和残余例外义务。D 或 Adapter 无权自行声明全局完成。

D 的规范 Forget 语义在其 Owner 源文件中已决议，但跨模块执行和 I 全局完成仍 OPEN。I 的 PermissionEpoch 和受保护授权条件已确认为 I 技术规范基线，但外部治理配置批准和实现仍受阻。I 全局清单合同为 CANDIDATE；Storage Restore 证明为 CANDIDATE；H ACK 行为为 CANDIDATE；F Runtime 语义在其补充文件中已决议，但实现和跨 Owner 接口尚未验证。

**任何 DELETE 成功、HTTP/gRPC 响应、队列 ACK、本地抑制标记、IndexWatermark 或 Workflow 完成，都不能证明全局 Forget。**

## 2. Non-delegable authority / 不可委托权威

| Authority | Owner | Minimum responsibility | Explicit non-authority |
|---|---|---|---|
| ForgetOperation / ForgetFence / canonical suppression | D | Stable operation identity, target lineage, monotonic fence, producer barrier, canonical-domain proof | I global/physical completion |
| Authorization / revocation / PermissionEpoch / global Forget policy | I | Authenticated principal/workload, policy domain, currentness, revocation order, target inventory/seal, exception approval | D canonical fence or Storage visibility |
| Compiler work / retry / DLQ / derived registration enforcement | E | Work/attempt/lease lifecycle, register-before-execute, lineage, current fence/permission checks | D admission ledger or canonical commit |
| Retrieval / index / cache / Working Set | F | Pre-filter, final disclosure revalidation, invalidation, rebuild suppression, per-partition watermarks | Canonical truth, I auth, global Forget |
| Context / delivery / Applied | G | Context version, tombstones, delivery cancellation/reconciliation, G Applied ledger | D Forget or C provider outcome |
| BMCP / Adapter / local clear ACK | H | Wire and authenticated Adapter-local clear/suppress/reconnect evidence | Global deletion or policy grant |
| Physical serialization / participant / restore | Storage | Atomic visibility, prepared participant, high-water reconciliation, quarantine | D/I/COC semantic decisions |

## 3. Forget state machines / Forget 状态机

### 3.1 D canonical operation state

D's operation state is distinct from Memory lifecycle:

`Requested → FenceEstablished → InventoryOpen → BarrierDraining → TargetReconciliation → CanonicalSuppressionComplete`

Alternative outcomes: `Blocked` or `Failed`. D's `CanonicalSuppressionComplete` proves only D's canonical-domain barrier and registered target suppression. It does not mean all modules or external copies are physically erased.

### 3.2 I global governance state

I's policy-level process is separate:

`Requested → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → CompletionEvaluated → Completed | CompletedWithPolicyException | Failed | Cancelled`

A policy exception must be I-authorized, target/scope-specific, durable, reasoned, time-bounded or review-bound, and auditable. D cannot invent or approve it.

### 3.3 Target evidence state

Each target has owner- and target-scoped evidence such as `discovered`, `suppression_requested`, `suppression_confirmed`, `cleanup_confirmed`, `failed`, `unknown`, or `excepted`. A retry does not convert UNKNOWN to success. A newly discovered derivative reopens/invalidate the closed-world proof as required.

### 3.4 Fence installation and admission linearization

- Every derivative-capable producer class is registered and enabled under a versioned D registry before work admission.
- Each work item is durably registered before queueing, leasing, protected-source dereference, execution, retry, DLQ replay or publication.
- Fence installation atomically captures the producer-registration high-water mark and target/lineage inventory snapshot.
- Registration concurrent with fence installation has exactly two safe outcomes: (a) registration commits first and is included in the barrier; or (b) fence commits first and registration is rejected/quarantined or admitted only as suppression/cleanup work.
- No admitted-but-unaccounted work may publish.
- Complete direct/transitive dependency registration must be durable before visibility.
- The latest applicable fence and current I authorization must be checked at the same final visibility/disclosure boundary; an old precheck or detached token is insufficient.

## 4. Authorization and revocation contract / 授权与撤销合同

### 4.1 I PermissionEpoch

I confirms PermissionEpoch as an opaque, monotonically advancing token issued solely by I within one explicit PolicyDomainRef. It is mandatory currentness input for protected operations.

- Epochs from different PolicyDomainRefs are incomparable.
- Consumers do not parse or numerically compare epoch tokens; they obtain currentness from I's authoritative sequencer/epoch service.
- Stale, gapped, unknown, incomparable, unverifiable or indeterminate state means DENY/PAUSE, never ALLOW.
- No offline authorization lease, stale-epoch grace or cached ALLOW without online currentness proof is allowed under the Phase 3.6 profile.
- PermissionEpoch is not ForgetFenceGeneration, CanonicalCommitCursor, IndexWatermark or ContextVersion.

### 4.2 Full protected authorization tuple

I requires the protected decision to bind at least:

`(IssuerRef, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ownership ScopeRef, applicability ScopeRef set, EnvironmentRef, DelegationChainRef, PolicyDomainRef, PermissionEpoch, authenticated workload/instance, RuntimeSessionRef)`

Authenticated transport/verifier context, not payload fields, establishes issuer, Principal, workload, audience and session. Ownership Scope and applicability Scope are independently evaluated; applicability is not permission. Cross-Scope and cross-Environment access require explicit current grants. Evidence dereference is separately authorized.

### 4.3 Final commit/disclosure ordering

For irreversible protected operations, I issues a single-use `CommitAuthorizationReceipt` bound to the exact immutable operation ID, request digest, security tuple and owner boundary. I's sequencer orders this against revocation and records one terminal outcome:

- `COMMIT_WON`: exact operation was ordered before conflicting revocation; this is authorization ordering only.
- `REVOCATION_WON`: revocation was ordered first; no visibility/dispatch success.
- `INDETERMINATE_ABORTED`: I durably terminates as non-success when safe order cannot be established.
- `UNKNOWN/PENDING`: outcome not yet authoritative; remain blocked/private.

I accepts its technical JF-10 interface, but JF-10 overall remains OPEN until D/Storage acceptance, implementation and crash/recovery conformance exist. A later epoch change does not rewrite an already durable COMMIT_WON for the exact operation, but it grants no permission to a new operation.

### 4.4 PDP failure

A PDP is an evaluator, not the authorization authority. Cedar remains a candidate only. Any evaluator error, missing/unknown input, invalid policy bundle, timeout or indeterminate result must be converted by the Brain-owned wrapper to DENY/PAUSE. A Permit from another policy rule must not mask a relevant evaluation error. No PDP outage or parser failure may fall back to Permit.

## 5. Visibility and anti-resurrection contract / 可见性与防复活合同

| Boundary | Required fence/auth check | Failure behavior |
|---|---|---|
| Ingress / producer admission | I identity+permission; D producer class/work registration and current fence | No enqueue/lease/run while admission unknown |
| Compiler execution/retry/replay | Same WorkItemId/lineage; fresh PermissionEpoch and latest fence | Suppress/quarantine; expired lease is not terminal |
| Dependency registration | Complete exact direct/transitive lineage, current fence and permission | Partial/unknown registration remains private |
| Final derived publication | D participant/fence ordering + I COMMIT_WON + Storage atomic visibility | No VisibilityPointer; UNKNOWN remains private |
| Retrieval candidate generation | Authenticated scope and current I/D state before candidate emission | No candidate or protected existence leakage |
| Final retrieval return/handoff | Revalidate current I/D after ranking/materialization and immediately before serialization | Strip affected data or fail closed |
| Cache hit/fill | Key includes principal/scope/environment/policy/fence/version; current authority on every hit and fill | Evict/quarantine; late fill cannot publish |
| Index rebuild/backfill | D work registration, current fence, contiguous CanonicalCommitCursor coverage, final publish gate | Old snapshot quarantined; watermark cannot imply Forget |
| Context snapshot/delta/delivery | G ContextVersion and tombstone; current I/D; cancel/supersede pending deliveries | Old snapshot never current; late ACK cannot reverse fence |
| Adapter reconnect | Authenticate; obtain current I PermissionEpoch and D Fence; reconcile G delivery; clear/suppress before applying queued context | No stale cached Context reuse |
| Backup/restore | COC, I, D and Storage current control high-waters; same-GID participant resolution | RESTORE_FENCED; no listener, reads, index rebuild or Adapter reconnect |

F's logical anti-resurrection reference model reports 19/19 tests passing in CI. It is an in-memory deterministic model, not a real index/cache implementation, physical database transaction, concurrent service, network partition, Adapter or backup/restore test. It closes a logical regression-evidence gap only.

## 6. Restore safety contract / 恢复安全合同

A restored Canonical Authority starts quarantined as `RESTORE_FENCED`. PITR success or internally consistent local tables are insufficient.

### 6.1 Required independent proofs

| Proof | Issuer | Minimum binding | What it does not prove |
|---|---|---|---|
| COCCommittedPrefixProof | COC | Causal domain, cluster, coordinator epoch/index, voter config, contiguous prefix digest, snapshot/checkpoint, external monotonic anchor | I authorization, D Forget or Storage visibility |
| IControlHighWaterProof | I, one per affected PolicyDomainRef | PermissionEpoch, I sequencer position, revocation/control high-water, ProducerDomainInventoryEpoch, registry digest, active Forget TargetInventorySeal | D barrier completion or Storage participant resolution |
| DForgetControlHighWaterProof | D | All relevant Forget operations, FenceGeneration, request cutoff, ProducerRegistrationHighWater, lineage inventory digest, barrier terminal state | I permission or Storage visibility |
| StorageParticipantLedgerProof | Storage | DB incarnation, backup/snapshot/LSN, all PreparedParticipant/GID/native-XID tuples and terminal states | COC/I/D semantic authority |
| RestoreReconciliationReceipt | Storage | Restore operation, DB authority, exact backup/WAL target and all proof refs/digests | Global Forget, authorization grant or permission to serve |

IControlHighWaterProof is accepted as a technical boundary by I, but proof API, signed format, audience/key verification and real restore integration are not implemented/not run. Storage restore contract remains a candidate requiring exact I/D/A review.

### 6.2 Required restore order

1. Restore to isolated target; no public listener, authoritative read/write, cache/index rebuild, Adapter reconnect or content serving.
2. Verify base backup, timeline and all WAL through exact target LSN; fence old primary before promotion.
3. Verify and replay current COC committed prefix; gaps or stale epochs block.
4. Obtain fresh I proofs for every affected PolicyDomainRef and current inventory/target seals; stale epoch, missing seal or registry gap blocks.
5. Obtain fresh D Forget high-water proof covering all relevant operations, full lineage and producer barriers; open/unknown work blocks.
6. Enumerate every Storage prepared participant and resolve by the same immutable GID/DB incarnation tuple; never infer terminality from absence in a local prepared-XID view.
7. Reconcile VisibilityPointer, PublicationReceipt, outcome and outbox; no pointer without exact D/I evidence.
8. Issue Storage RestoreReconciliationReceipt, then separately revalidate current owner serving gates. A restore receipt alone does not authorize serving.

## 7. Adversarial race and fault-injection matrix / 对抗性竞争与故障注入矩阵

The following 20 cases are required. These are test definitions, not executed results.

| ID | Scenario | Required result | Forbidden result | Evidence / automated test |
|---|---|---|---|---|
| C-01 | Duplicate ingestion request | Same scoped key+digest returns original receipt/work IDs | Duplicate logical work | Receipt lookup and idempotency ledger test |
| C-02 | Concurrent ingestion of same logical fact | Apply only approved identity/conflict rule; while B ADR blocked retain neutral candidate | Silent overwrite, invented Fact/Claim identity | Concurrent CAS/identity test; candidate-neutral guard |
| C-03 | Crash before canonical commit | No canonical visibility; retry same operation | Partial MemoryVersion or cursor | Kill before transaction commit; readback |
| C-04 | Crash immediately after canonical commit | Original receipt/cursor recoverable | Second commit or lost receipt | Kill after commit before ACK; same-key lookup |
| C-05 | Worker lease expiration | Lease invalid; barrier remains open | Lease expiry counted terminal | Expire lease while fence drains |
| C-06 | Retry after partial processing | Same WorkItemId/lineage, new AttemptId; fresh auth/fence | New identity bypasses old fence | Retry/DLQ/replay mutation test |
| C-07 | Duplicate outbox delivery | Idempotent projection; contiguous watermark preserved | Duplicate side effect or watermark jump | Deliver same event twice and out of order |
| C-08 | Forget races with ingestion | One linearized order: pre-fence registration included; post-fence rejected/quarantined | Admitted-but-unaccounted producer | Barrier/registration race with deterministic scheduler |
| C-09 | Forget races with retrieval | Final disclosure revalidates latest fence; affected result suppressed | Candidate disclosed after fence | Pause after ranking, install fence, resume |
| C-10 | Forget races with index publication | Final pointer/segment publication serialized against fence | Stale segment visible | Pause before index swap, install fence, resume |
| C-11 | Late worker publishes stale projection | Reject/quarantine late result; barrier/incident remains visible | Stale worker overwrites current projection | Lease expiry + late worker commit test |
| C-12 | Authorization revoked after retrieval before dispatch | I final-boundary currentness denies/pauses dispatch | Cached ALLOW or prior retrieval authorizes dispatch | Pause before dispatch, advance PermissionEpoch |
| C-13 | PermissionEpoch changes during context assembly | G/C final boundary revalidates and rebuilds/blocks | Old epoch treated as current | Advance epoch between candidate and final request |
| C-14 | PDP evaluation failure | Fail closed to DENY/PAUSE | Skip-on-error becomes Permit | Inject parser/evaluator/timeout/unknown input with mixed rules |
| C-15 | Crash after provider dispatch before Applied persistence | Outcome remains UNKNOWN until exact C/G reconciliation; no assumed Applied | Dispatch ACK or timeout promoted to Applied | Crash after egress; replay same attempt and G idempotency |
| C-16 | Duplicate provider callback | Same immutable attempt/outcome identity is idempotent; conflicting digest rejected | Duplicate side effect or Applied mutation | Deliver identical and conflicting callbacks |
| C-17 | Restore backup older than Forget fence | RESTORE_FENCED until current COC/I/D/Storage high-waters reconcile | Old snapshot serves forgotten content | Restore old snapshot with newer fence/inventory |
| C-18 | Index rebuild after Forget | Current fence checked before batches and final publication; old snapshot quarantined | Rebuilt index resurrects target | Rebuild from pre-fence snapshot after Forget |
| C-19 | Cross-tenant/principal retrieval | Scope/authorization filter before candidate emission/count/rank | Existence, count or snippet leakage | Cross-scope candidate/index/cache probes |
| C-20 | MCP tool attempts to bypass Brain authorization | Tool call re-enters I PEP and Brain scope/fence checks; MCP grant is not authority | Tool/runtime role or connector RBAC bypasses Brain | Invoke protected tool with forged scope/principal and revoked epoch |

## 8. Formal and executable evidence ceiling / 形式化与可执行证据上限

- PR #88 reports a bounded Python explicit-state BFS model: 606 state/depth pairs through depth 10 in the safe-rule abstraction, with no modeled invariant violation. Five weakened-guard mutants produced counterexample traces. This is bounded abstraction evidence, not TLC/model-checker proof or production proof.
- PR #93 integrates the model findings and explicitly retains Forget as P0 / NOT READY. Producer/recipient inventory, D/E/Storage atomic publication, JF-10 and physical restore remain open.
- F's 19/19 anti-resurrection tests pass only in its deterministic in-memory reference model.
- Storage JF-10 conformance plan is TEST DESIGN / NOT EXECUTED. It requires production-equivalent coordinator and selected DB, crash hooks, owner evidence and physical recovery.
- No complete Forget race campaign, real multi-process concurrency test, physical restore drill, global recipient purge or production authorization audit is claimed.

## 9. Owner decisions and closure gates / Owner 决议与关闭门槛

| Gate | Accountable owner(s) | Closure evidence |
|---|---|---|
| C-G1 D Fence/admission and canonical suppression | D | Exact D source/head, durable registration/fence linearization, target barrier tests |
| C-G2 I auth/revocation and PermissionEpoch | I | Current technical contract + production governance profile, sequencer and PEP conformance |
| C-G3 E producer/derivative lifecycle | E + D + Storage | Durable work registration, complete dependency set, final gate and crash tests |
| C-G4 F retrieval/index/cache | F + D + I | Final-read revalidation, per-partition watermarks, rebuild/cache invalidation tests |
| C-G5 G Context/Applied | G + C + H + I + D + Storage | Current Context tombstones, exact request mapping, durable Applied and restore tests |
| C-G6 H Adapter/Forget ACK | H + I + D + G | Exact branch currentness, ACK scope, authenticated reconnect and offline queue tests |
| C-G7 Storage/JF-10/restore | Storage + D + I + COC | L4 profile, same-GID proof, physical crash/failover/PITR/anti-rollback evidence |
| C-G8 Global completion | I | Closed-world producer/recipient/backup inventory, seals, target evidence and approved exceptions |

**Workstream C status: P0 SAFETY CONTRACTS PARTIALLY RESOLVED; GLOBAL FORGET AND PHYSICAL RESTORE NOT READY.**

No Owner contract is amended. No global Forget completion is declared. No PDP product is approved. No restore test is claimed as run. No production activation is authorized.

**C 工作流状态：P0 安全合同部分明确；全局 Forget 和物理恢复尚未就绪。**

本文件不修改 Owner 合同，不声明全局 Forget 完成，不批准 PDP 产品，不声称恢复测试已执行，也不授权生产启用。
