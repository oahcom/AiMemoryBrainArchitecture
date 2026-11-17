# Phase 3.8.4 — C Normative Provider Submit Outcome Contract
# Phase 3.8.4 — C 规范性 Provider Submit Outcome 合同

- Owner: C — Agent Integration / Provider Egress / Final Request Boundary
- Branch: `session-c-agent-integration-2026-11-16`
- Status: **C-OWNED NORMATIVE SEMANTIC CONTRACT — PROPOSED FOR EXACT OWNER REVIEW; NOT SHARED-WIRE-FROZEN**
- Supersedes: no earlier C contract; this document fills the missing canonical CSubmitOutcome source contract and composes with the existing Phase 3.6 C-submit causal-order contract.
- Exact H wire target reviewed: unified COC/JF-10/Provider Outcome schema artifact 1.2.8, Blob `70b892797d07489936300a26c0dedfafe1d6e746`.
- English and Chinese are normative peers.

## 1. Purpose and authority / 目的与权威

C is the sole semantic authority for whether a specific immutable final inference request was handed to a named Provider, whether that handoff was authoritatively accepted/rejected, whether it is proven not to have been invoked, or whether its result remains uncertain.

C owns:
- ProviderRef and ProviderAdapterRef binding for the actual egress path;
- ProviderAttempt identity, provider idempotency-key scope and same-key recovery semantics;
- the immutable CSubmitOutcome record and its evidence classification;
- the final egress gate and its close-vs-send ordering;
- the C-authored evidence that an actual provider handoff occurred or did not occur.

C does not own I authorization/PermissionEpoch, D ForgetFence/lineage, H wire representation/transport authentication, G Applied state, Storage visibility/COC/JF-10 outcome, model execution completion, response correctness or user delivery.

C 是判断某个不可变最终推理请求是否已交给指定 Provider、是否被权威接受/拒绝、是否能够证明从未调用，或结果是否仍不确定的唯一语义权威。

C 拥有实际 Egress 路径的 Provider/Adapter 绑定、ProviderAttempt 身份与幂等键恢复语义、不可变 CSubmitOutcome、最终 Egress Gate 及 Close-vs-Send 顺序，以及实际发生/未发生 Provider Handoff 的 C 证据。

C 不拥有 I 授权、D ForgetFence、H Wire、G Applied、Storage/COC/JF-10 Outcome，也不拥有模型执行完成、回答正确性或用户交付事实。

## 2. Normative outcome algebra / 规范结果代数

The exact H schema enum is retained without renaming:

`HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`.

| Outcome | Normative meaning | Terminal? | Permitted next action |
|---|---|---:|---|
| `HANDOFF_ACCEPTED` | C has authoritative evidence that the exact final request was handed to the identified provider and the provider accepted the request/attempt. | Terminal for the handoff fact only | No new send for this attempt. Later execution-start/completion is separate evidence. |
| `HANDOFF_REJECTED` | The provider authoritatively rejected the exact attempt and the evidence proves no provider side effect or execution was accepted. | Terminal for this attempt | A new attempt is allowed only under a new attempt identity and after fresh I/D/C gate checks; preserve the rejected attempt. |
| `NOT_INVOKED` | C proves that no provider handoff crossed the egress boundary for this attempt. | Terminal for this attempt | A new attempt may be created only after the no-handoff proof is authoritative and all gates are re-evaluated. |
| `UNKNOWN` | C cannot establish whether the request crossed the provider handoff boundary, or required authority/evidence is unavailable. | Nonterminal | Suppress retries and Full Applied; reconcile the same attempt and same provider idempotency key. |
| `IN_DOUBT` | A handoff may have occurred or provider side effect may exist, but no authoritative outcome is available. | Nonterminal and non-expiring | Do not create a new attempt or new idempotency key. Query/reconcile the same provider key; keep applicable owner barriers held. |

**Critical distinction:** a transport timeout, local exception, missing receipt, lost ACK, process crash, missing request row, empty queue, absent COC intent or provider lookup outage is never proof of `NOT_INVOKED` or `HANDOFF_REJECTED`. If a possible side effect exists, use `IN_DOUBT`; otherwise use `UNKNOWN` until a positive no-handoff proof is available.

**关键区别：** Transport Timeout、本地异常、Receipt 缺失、ACK 丢失、进程崩溃、请求行缺失、队列为空、COC Intent 缺失或 Provider Lookup 不可用，都不能证明 `NOT_INVOKED` 或 `HANDOFF_REJECTED`。可能存在副作用时使用 `IN_DOUBT`；无法证明是否越过发送边界时使用 `UNKNOWN`，直至取得正向未发送证明。

## 3. State machine and linearization / 状态机与线性化

`CREATED → REQUEST_FROZEN → OWNER_GATES_VALIDATED → EGRESS_ADMITTED → HANDOFF_ATTEMPTED → {HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT}`

1. `REQUEST_FROZEN`: C binds the exact post-transformation request bytes/semantic projection, actual final request boundary, request digest, Context/Delivery/Managed Region references and authenticated runtime/Adapter identity.
2. `OWNER_GATES_VALIDATED`: all required I authorization (including the exact I sequencer COMMIT_WON decision where applicable), D fence/lineage/participant predicates, and required COC/Storage participant proofs are validated for the same immutable tuple. No provider side effect is permitted before this state.
3. `EGRESS_ADMITTED`: C's own egress gate has atomically admitted this exact attempt. The gate and the final transport handoff MUST share one per-gate serialization authority.
4. `HANDOFF_ATTEMPTED`: the concrete transport-owning adapter begins the physical provider handoff under the same stable ProviderIdempotencyKeyRef.
5. A terminal handoff outcome is written append-only. A process-local flag or caller-supplied status is not authoritative.

**Close-vs-send race:** exactly one order wins at the C egress serialization point:
- Gate close wins first → no provider bytes/side effect may leave; C can issue `NOT_INVOKED` only with positive proof that the transport handoff did not occur.
- Egress admission/handoff wins first → the exact attempt is captured as pre-close in-flight work. A later close cannot erase it; C must resolve the same provider key and emit a terminal outcome or remain `UNKNOWN/IN_DOUBT`.
- If C cannot prove which order won, outcome is `UNKNOWN`; no new send is allowed.

Gate 关闭与发送竞争必须在 C 的同一 Egress Serialization Point 上排序：
- Gate Close 先赢：不得有 Provider Bytes/副作用离开；只有取得正向未发送证明时才可签发 `NOT_INVOKED`。
- Egress Admission/Handoff 先赢：该 Attempt 被记录为 Close 前在途工作，后续 Close 不得抹去它；C 必须用同一 Provider Key 解决，或保持 `UNKNOWN/IN_DOUBT`。
- 无法证明顺序时为 `UNKNOWN`，禁止新发送。

## 4. Required immutable CSubmitOutcome tuple / 不可变结果元组

Every outcome MUST bind the same immutable attempt tuple. The following are semantically mandatory even where H's structural schema makes a field conditionally optional:

- `CSubmitOutcomeRef`, `CSubmitOutcomeDigest`, outcome enum and C authority/version;
- `ProviderRef`, `ProviderAdapterRef`, provider account/tenant/model/endpoint scope and `ProviderIdempotencyKeyRef`;
- `ProviderRequestRef` and `ProviderReceiptRef` when accepted/rejected evidence exists;
- `FinalRequestBoundaryId`, exact actual request digest and actual `InferenceRequestId` when assigned;
- `CausalOrderTransactionRef`, `ParticipantIntentRef`, `ParticipantReservationRef` where applicable;
- exact `PreparedParticipantRef`, `PrepareAttemptRef/Generation`, `ParticipantLedgerRef/Version` and `ParticipantTupleDigest` where JF-10 applies;
- I terminal decision/receipt reference and D clearance/fence/lineage reference;
- C owner admission reference/digest, owner ledger/version/local sequence/high-water/root;
- C-authored `ProviderOutcomeEvidenceRef`, and exactly the applicable no-handoff, not-invoked, same-key lookup or unknown-reason evidence;
- H integrity/signature profile references and C-owned signature reference;
- COC record/position/commit proof. If there is no COC participant intent, `coc_participant_intent_ref=null` MUST be accompanied by a non-empty `coc_absence_reason`; null is not silently treated as an empty string.

The tuple is immutable. Same outcome identity + same digest is idempotent. Same identity with a changed request digest, provider key, participant, attempt, owner admission or evidence projection is a hard conflict and must be quarantined. Late evidence is appended as a linked enrichment/superseding record; the original attempt identity and prior observation are never rewritten.

每个 Outcome 必须绑定同一个不可变 Attempt 元组。即使 H 结构 Schema 将字段设为条件可选，语义上仍必须满足上述字段。元组不可变；相同身份/摘要幂等，不同摘要、Provider Key、Participant、Attempt、Owner Admission 或证据投影发生变化时必须冲突隔离。迟到证据只能作为关联补充记录追加，不能重写原 Attempt 身份或历史观察。

## 5. Provider idempotency and recovery / Provider 幂等与恢复

1. The idempotency key is stable for one logical provider attempt and is scoped by ProviderRef + authenticated provider account/tenant + endpoint/model semantics + immutable RequestDigest.
2. A retry that resolves the same uncertain handoff MUST reuse the exact same ProviderIdempotencyKeyRef and request digest. It is a lookup/reconciliation of the same attempt, not a new send.
3. If the provider supports authoritative same-key lookup, C records the provider's lookup response, its authority/consistency semantics and lookup time/version as evidence. A weak eventually consistent status endpoint is not authoritative proof of absence.
4. If the provider does not support authoritative idempotency or lookup, C cannot promise exactly-once side effects. Any ambiguous handoff remains `IN_DOUBT`; automatic retry is disabled and the provider capability is not eligible for a guarantee that requires deterministic reconciliation.
5. A new request payload, changed request digest, new provider account/model/endpoint or changed semantic operation is a new attempt and MUST NOT reuse the old outcome identity or claim continuity.
6. No automatic SDK retry, redirect, region/account/model failover, stream restart or transport reconnect may bypass the C egress gate. Each physical send must be separately admitted and evidence-bound; if the provider's idempotency contract does not safely cover it, do not retry.

幂等键对一个逻辑 Provider Attempt 稳定，并绑定 Provider、认证账户/租户、Endpoint/Model 语义和不可变 RequestDigest。解决同一不确定发送时必须复用同一个 Key 和 Digest；这是同一 Attempt 的查询/恢复，不是新发送。不支持权威同键查询的 Provider 不得承诺 Exactly-once；模糊结果必须保持 IN_DOUBT，禁用自动重试。任何 SDK 自动重试、Redirect、Region/Account/Model Failover、Stream Restart 或 Reconnect 都不得绕过 C Gate。

## 6. Relationship to Applied and execution evidence / 与 Applied 和执行证据的关系

- `HANDOFF_ACCEPTED` proves only provider acceptance of the exact handoff; it does not prove inference execution started, completed, produced a response, or delivered anything to a user.
- `HANDOFF_REJECTED` and `NOT_INVOKED` cannot produce Full Applied.
- `UNKNOWN` and `IN_DOUBT` cannot produce Full Applied and keep protected content suppressed for current use.
- G alone decides Applied. G requires the exact C outcome plus H transport/materialization evidence, current I authorization, current D fence/lineage and G's own Context/Delivery predicate.
- ExecutionStarted, Completed, Failed, response delivery and user observation are separate evidence families; CSubmitOutcome must not overload them.

`HANDOFF_ACCEPTED` 仅证明 Provider 接受了精确发送，不证明推理已开始、完成、生成响应或已交付用户。拒绝/未调用不能产生 Full Applied；UNKNOWN/IN_DOUBT 不能产生 Full Applied，并必须继续抑制受保护内容。G 独立决定 Applied；执行开始、完成、失败、响应交付和用户观察均属于不同证据族。

## 7. H schema 1.2.8 mapping / H Schema 1.2.8 映射

Reviewed H artifact:
- `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.8.schema.json`
- Blob: `70b892797d07489936300a26c0dedfafe1d6e746`
- Message family: `C_PROVIDER_OUTCOME_RECORDED`
- Exact enum: `HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`

C accepts the structural outcome enum and typed evidence fields as a candidate mapping only. H owns structural schema and wire validation; C owns the semantic truth and evidence class. The current schema has required common C outcome fields and conditional fields for accepted/rejected/not-invoked/unknown states. C requires the semantic rules in §§2–6 to be applied after structural parsing.

Important semantic constraints over the current schema:
- `HANDOFF_ACCEPTED` requires actual provider request/receipt evidence and the exact participant reservation where applicable.
- `HANDOFF_REJECTED` requires authoritative rejection and positive no-side-effect/no-handoff proof; otherwise it is `IN_DOUBT`.
- `NOT_INVOKED` requires positive C transport-boundary proof; missing provider receipt is not sufficient.
- `UNKNOWN/IN_DOUBT` requires an explicit unknown reason and is nonterminal/non-expiring.
- COC intent absence must be explicit and reasoned; a null intent never means “no participant obligations”.
- C's signature profile is not I's profile. I remains the trust/key-status authority for issuer verification; C defines the owner-specific outcome projection and must obtain the applicable trust/profile approval. H does not infer profile authority from the common envelope.

## 8. Reference-model proof obligations / 参考模型证明义务

The following L3 cases are mandatory architecture validation. They may be implemented as pure state-machine/reference-model tests; no real Provider or deployed Adapter is required to establish the abstract semantics.

| ID | Interleaving / failure | Required result |
|---|---|---|
| CPO-01 | Gate close linearizes before egress admission | no handoff; NOT_INVOKED only with positive no-handoff proof |
| CPO-02 | Egress admission linearizes before gate close | attempt remains in-flight; same-key reconciliation required |
| CPO-03 | Crash after handoff before receipt persistence | UNKNOWN/IN_DOUBT; same key, same digest; no new attempt |
| CPO-04 | Provider receipt exists but C ACK is lost | same-key lookup returns original outcome; no duplicate send |
| CPO-05 | Provider rejects before side effect | HANDOFF_REJECTED with positive no-side-effect proof |
| CPO-06 | Provider rejection may follow side effect | IN_DOUBT, not HANDOFF_REJECTED |
| CPO-07 | Provider lookup unavailable/eventually consistent | UNKNOWN/IN_DOUBT; no absence inference |
| CPO-08 | SDK retries/redirects without gate re-entry | invalid architecture path; no Full Applied |
| CPO-09 | Request digest changes under same attempt/key | immutable identity conflict/quarantine |
| CPO-10 | I revocation wins before receipt consumption | provider invocation forbidden |
| CPO-11 | I COMMIT_WON, then later revocation while provider outcome unresolved | exact participant remains held until C terminal outcome |
| CPO-12 | D fence wins before participant admission | provider invocation forbidden |
| CPO-13 | D participant admitted before later fence | fence remains held behind unresolved participant |
| CPO-14 | C outcome says accepted but provider receipt/request binding mismatches | reject evidence; UNKNOWN; no Full Applied |
| CPO-15 | Late receipt arrives after UNKNOWN | append linked enrichment; never rewrite attempt identity |
| CPO-16 | Provider lacks authoritative idempotency lookup | ambiguous handoff remains IN_DOUBT; no automatic retry |

These are specified proof obligations. No execution or provider capability is claimed by this contract.

## 9. Decision and dependencies / 决议与依赖

**C decision:** establish this document as the C-owned normative source for CSubmitOutcome semantics, subject to exact H/I/G/Storage/A review. It supplements rather than replaces:
- C Phase 3.6 C-submit / I-authorization / D-ForgetFence causal-order contract (Blob `45a48249717c8cddb07ab96197730ef93d406c22`);
- C Phase 3.6 final-request evidence contract (Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`);
- H unified schema 1.2.8 (Blob `70b892797d07489936300a26c0dedfafe1d6e746`);
- I crypto profile candidate (Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`);
- G Applied contract and Storage/COC/JoinProof contracts as exact-version consumers.

**Not claimed:** production provider adapter, real provider lookup, exactly-once execution, production signatures, deployment, conformance PASS, Full Applied or architecture freeze.

**C 决议：** 本文档作为 CSubmitOutcome 的 C Owner 规范语义源，待 H/I/G/Storage/A 精确版本审查。它补充但不替代既有 C Submit 因果顺序合同和 Final Request Evidence 合同。

**不作以下声明：** 生产 Provider Adapter、真实 Provider Lookup、Exactly-once 执行、生产签名、部署、Conformance PASS、Full Applied 或架构冻结。

