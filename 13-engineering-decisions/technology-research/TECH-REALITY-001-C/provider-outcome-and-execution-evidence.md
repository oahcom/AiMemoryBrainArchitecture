# Provider Outcome and Execution Evidence / Provider Outcome 与执行证据

## 1. Existing C semantic contract / 既有 C 语义合同
Historical C Phase 3.8.4 defines the C-owned handoff algebra:
`HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`.
This is more precise than collapsing all provider behavior into SUCCEEDED/FAILED/TIMED_OUT. It is a historical C branch proposal and is not jointly frozen with current H/I/Storage.

历史 C Phase 3.8.4 定义 C 负责的 Handoff 结果代数。它比将所有 Provider 行为压缩为 SUCCEEDED/FAILED/TIMED_OUT 更精确。但它仍是历史 C 分支提案，尚未与当前 H/I/Storage 联合冻结。

- HANDOFF_ACCEPTED: exact request handoff and provider acceptance are evidenced; proves handoff only, not generation completion.
- HANDOFF_REJECTED: authoritative rejection proves no accepted execution/side effect for that attempt.
- NOT_INVOKED: positive evidence proves no provider handoff crossed the egress boundary.
- UNKNOWN: boundary crossing or authority cannot be established.
- IN_DOUBT: handoff/side effect may exist; terminal result unavailable; non-expiring until reconciled.

Timeout, lost ACK, socket close, process crash, empty queue or provider lookup outage never proves NOT_INVOKED. When side effect may exist, retain IN_DOUBT and suppress unsafe new attempt.

## 2. Request and Attempt / Request 与 Attempt
- One logical InferenceRequest may have multiple Attempts only after the prior Attempt's retry predicate is satisfied.
- Every Attempt gets a new immutable Attempt identity and records ProviderRef, ModelRef, adapter version, request digest, provider idempotency scope/key reference, and its own outcome evidence.
- Reuse the same provider idempotency key only for recovery of the same provider operation where provider semantics guarantee it. A new attempt must not be disguised as the same operation.
- Provider-internal retries are separate from client retries; capture them only if provider reports them.
- Brain idempotency and Provider idempotency are distinct namespaces and authorities.

## 3. Outcome dimensions / 结果维度
Do not overload a single status. Track separately:
1. Submission/handoff outcome (C-owned).
2. Provider execution lifecycle (started/running/completed/failed/cancelled/unknown when actually observable).
3. Response receipt/stream completeness (complete/partial/invalid/missing).
4. Parse and validation result.
5. Tool side-effect outcome.
6. Brain operation acceptance/commit/visibility (D/Storage).
7. Context Applied (G).
8. User-visible delivery.

## 4. Evidence minimum / 最小证据
| Evidence | Required rule |
|---|---|
| RequestRef / AttemptRef | Stable opaque B-compatible identities; exact scope defined |
| ProviderRef / ModelRef | Configured identities; model version if reported |
| ExecutionRef | Provider/runtime-issued where available; otherwise explicit UNAVAILABLE |
| CorrelationRef | Cross-boundary correlation only; not an operation identity |
| Start/completion times | Preserve source event time and Brain recorded_at separately |
| Outcome | C handoff algebra plus separate execution/result dimensions |
| Error | Provider-native code/category plus normalized retryability; preserve raw code safely |
| ResultRef/digest | Content reference and integrity digest; do not log raw output by default |
| Usage | Tokens/cost/cache/media only when reported; preserve provider source |
| Validation | Schema/domain validator identity/version and result |
| Provenance | Provider adapter, SDK, model, request digest and source refs |

Missing metadata uses distinct states: UNAVAILABLE = capability/source cannot supply; NOT_REPORTED = field supported but absent in this response; UNKNOWN = system cannot determine; NOT_APPLICABLE = concept does not apply. Never substitute zero, empty string or fabricated timestamp.

## 5. Retry, idempotency and late results / 重试、幂等和迟到结果
- Retry decision is based on authoritative attempt state, provider idempotency semantics, side-effect risk, authorization and D/I gates.
- A client timeout after possible handoff becomes UNKNOWN/IN_DOUBT; reconcile the same attempt/key before any new attempt.
- A late result is a new immutable observation attached to the original Attempt. It cannot overwrite prior history or bypass current authorization/Forget checks.
- Duplicate identical result: record duplicate observation and link to original digest. Conflicting result: preserve both, mark reconciliation required; never last-write-wins.
- Cancellation is a request to stop. It is not proof that provider execution stopped or external side effects were rolled back.
- Result after Session closure may be retained as evidence under retention policy but cannot revive closed context or stale references.
- Provider idempotency does not imply Brain idempotency; neither implies exactly-once external execution.

## 6. C key/sequence status / C 密钥与序列状态
C Phase 3.11.0 proposes C data-plane Ed25519 keys and an I-governed trust root, but the C and I crypto profiles are NOT REGISTERED. CSubmitOutcome 1.0.1 adds `sequence_namespace_ref` so record_sequence and key-status events share a durable monotonic namespace; this schema and vectors are proposed, not a production trust deployment. H 1.2.15 adds origin transport receipt and H signing-sequence fields but is candidate only.

C Phase 3.11.0 提议 C 数据面 Ed25519 密钥和 I 治理信任根，但 C/I 密码配置均未注册。CSubmitOutcome 1.0.1 增加 sequence_namespace_ref，使记录序列和密钥状态事件共享持久单调命名空间；Schema/向量仍为提案，不是生产信任部署。H 1.2.15 增加 Origin Transport Receipt 与 H Signing Sequence 字段，但仍仅为候选。


## 完整中文版本

历史 C Phase 3.8.4 定义五种 Handoff Outcome：HANDOFF_ACCEPTED、HANDOFF_REJECTED、NOT_INVOKED、UNKNOWN、IN_DOUBT。该代数比单一成功/失败/超时更准确，但仍未与当前 H/I/Storage 联合冻结。HANDOFF_ACCEPTED 只证明请求已交付并被 Provider 接受，不证明生成完成。HANDOFF_REJECTED 必须有权威拒绝证据且证明该 Attempt 未被接受。NOT_INVOKED 必须有正向证据证明请求未越过 Egress 边界。UNKNOWN 表示无法确定是否越界或权威证据不可用。IN_DOUBT 表示可能已交付或产生副作用，但终态未知，必须保留并对账。

超时、ACK 丢失、Socket 关闭、进程崩溃、队列为空或 Provider 查询不可用，都不能单独证明 NOT_INVOKED。可能存在副作用时，应保留 UNKNOWN/IN_DOUBT 并禁止不安全的新 Attempt。

一个逻辑 InferenceRequest 可在前一 Attempt 满足重试条件后创建多个 Attempt。每个 Attempt 有独立不可变身份、Provider/Model、Adapter 版本、Request Digest、Provider 幂等键作用域和 Outcome。Provider 内部重试与客户端重试不同；只有 Provider 报告时才记录内部重试。Provider 幂等与 Brain 幂等属于不同命名空间。

分别记录 Handoff、Provider 执行生命周期、响应/流完整性、解析与验证、Tool 副作用、Brain 接受/Commit/Visibility、G Applied 和用户交付。需要 Request/Attempt、Provider/Model、Execution、Correlation、开始/完成时间、Outcome、错误分类、Result 引用/Digest、Usage、Validation 和 Provenance。缺失值必须区分 UNAVAILABLE、NOT_REPORTED、UNKNOWN 和 NOT_APPLICABLE，不得伪造零值或时间戳。

只有在权威 Attempt 状态、Provider 幂等语义、副作用风险、授权和 D/I Gate 都允许时才可重试。超时后先对账同一 Attempt 和 Provider Key。迟到结果作为原 Attempt 的新不可变观察记录；重复结果按 Digest 关联，冲突结果保留双方并进入 Reconciliation。取消请求不证明 Provider 已停止，也不证明外部副作用回滚。

C Phase 3.11.0 提议 Ed25519 数据密钥和 I 治理信任根，但 C/I 配置尚未注册。CSubmitOutcome 1.0.1 增加 sequence_namespace_ref，以绑定签名序列与密钥状态事件的单调序列命名空间；仍是提案而非生产信任部署。H 1.2.15 也仍为候选。
