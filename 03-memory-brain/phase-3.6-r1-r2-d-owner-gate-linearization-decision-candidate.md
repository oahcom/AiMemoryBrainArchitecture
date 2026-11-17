# Phase 3.6 — D Owner R1/R2 Gate Linearization Decision Candidate
# Phase 3.6 — D Owner R1/R2 Gate 线性化决议候选

- Owner perspective: D — Memory Brain / ForgetFence and Producer Work Authority
- Status: **CANDIDATE / NO INDEPENDENT OWNER APPROVAL**
- Source proposal: P-COC-R1-R2-TECH-001, blob `eac0b079f43da8c52521397e0cd256fda3fd3333`
- A review: blob `fdf63550696948f77dc37c0a3788276ac4d525f5`, Issue #14 R1/R2
- Scope: D producer registration, WorkItem/Attempt/Derivative admission, ForgetFence and D-only outage-gate release.

## 1. D authority and scope key / D 权限与作用域键

D owns the authoritative serialization boundary for Forget work and producer-derived work. The minimum scope key binds `ForgetOperationRef`, target scope digest, source scope digest, ancestor-lineage selector/digest and the applicable producer/dependency registry revision. A newly discovered applicable producer, source or ancestor expands ScopeVersion and invalidates the old seal. I PermissionEpoch and C provider counters remain opaque.

D 对 Forget 工作及 Producer 派生工作拥有权威串行化边界。作用域键必须绑定 ForgetOperation、目标/来源/祖先 lineage 及适用的 Producer/Dependency Registry 修订。发现新的适用 Producer、来源或祖先时必须扩张 ScopeVersion 并使旧封印失效。

## 2. Exact linearization point / 精确线性化点

A D producer/work admission and a D Forget-fence request MUST serialize against the same D-authoritative gate state. The durable transaction/CAS atomically:
1. validates authenticated producer/request identity, immutable source revision and target/source/ancestor scope;
2. deduplicates by stable D request or admission identity; same digest returns the original result, changed digest is CONFLICT;
3. appends the request/admission to the D ledger and allocates D-local sequence;
4. advances AcceptedRequestHighWater or InFlightAdmissionHighWater and applicable producer/dependency ScopeVersion;
5. closes the affected producer/work/derivative admission gate and advances GateGeneration/FenceGeneration as appropriate;
6. prevents queue insertion, lease acquisition, retry, replay, derivative compilation, publication reservation or other protected progress from committing after closure.

The durable commit is the exact D-local linearization point. Queue/lease/worker checks performed only after a non-atomic OPEN read do not satisfy the contract.

D 的 Producer/Work 准入与 Forget Fence 请求必须针对同一 D 权威 Gate 状态串行化。事务原子追加请求/准入账本、分配本地序号、推进 HighWater/ScopeVersion、关闭 Gate，并阻止 Queue、Lease、Retry、Replay、Derivative、Publication 等受保护进展越过关闭点。持久化提交即线性化点。

## 3. Pre-COC in-flight work / COC 前在途工作

Before returning admission success, D MUST durably append a DAdmissionRef/WorkItemRef with immutable source revision, dependency inventory revision/digest, target/source/ancestor lineage, observed GateGeneration/FenceGeneration, local sequence and lifecycle phase. Work admitted before closure but not yet COC-registered remains enumerable in the D in-flight ledger; it cannot disappear because it has not yet entered the COC participant registry.

At seal, D captures request high-water H_D and in-flight high-water F_D under the same serialization boundary, plus producer-registration, WorkItem, Attempt, Derivative and barrier high-waters. Every row through F_D must be joined to the exact COC prefix/manifest, retained as owner-local admission for reconciliation, or proven terminal/rejected without publication or visibility. Late-discovered pre-fence lineage invalidates the snapshot and reopens the affected barrier for a successor round.

D 在向调用方确认准入前必须持久化 DAdmissionRef/WorkItemRef。即使尚未注册到 COC，Fence 前准入的工作也必须能从 D 在途账本完整枚举，不得因未进入 COC 而丢失。

## 4. Repeated cutoff rounds and D-only release / 重复批次与 D 独立释放

D's immutable seal binds GateGeneration, FenceGeneration, ScopeVersion, request/in-flight high-waters, producer/dependency registry versions, counts, ordered-set roots/digests, exact query identity and anti-rollback anchor. Requests or scope changes after sealing remain blocked and force a later cutoff batch.

D releases only its outage-admission gate via owner-local CAS after exact Batch-before-Manifest pair readback and reconciliation. CAS requires unchanged GateGeneration, FenceGeneration, ScopeVersion and high-waters; every producer/work/attempt/derivative/barrier member and every owner-local admission is accounted for; no UNKNOWN/IN_DOUBT, late lineage or incomplete dependency closure remains. Any mismatch keeps the gate closed and requires a successor seal/batch. This release does not clear the effective ForgetFence or mean Forget completion.

D 只能在精确 Batch/Manifest 顺序读回及成员协调完成后，通过自己的 CAS 释放 outage-admission gate；不得清除有效 ForgetFence，也不得据此宣称 Forget 完成。

## 5. Required evidence and tests / 必需证据与测试

Required: register-vs-fence race at the shared serialization point; queue/lease/retry/replay-vs-close races; late producer registration and ancestor discovery; immutable source revision/dependency drift; high-water advancement during reconciliation; same-identity idempotent retry and changed-digest conflict; crash-after-commit-before-ACK; owner-only release CAS; and proof that absent/partial D ledger enumeration is UNKNOWN, not empty.

## 6. Decision boundary / 决议边界

This is a coordinator-authored D-role candidate, not independent D Owner approval. D must independently adopt/amend/reject and pin exact source versions. Durable producer/work ledgers, sequencer/CAS, queue/worker integration, anti-rollback, signer and executable concurrency/fault tests remain NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED. No Forget completion or production activation is claimed.
