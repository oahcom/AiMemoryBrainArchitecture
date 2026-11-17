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



## Exact C handoff semantics readback / C Handoff 精确语义读回

C Phase 3.8.4 Blob `819705037da89834e10b6dd2ec6e66c1b8c70886` is the exact C-owned semantic contract read in this pass. It explicitly says C alone classifies whether the exact immutable final inference request was handed to the named Provider and whether the handoff was accepted/rejected/not invoked/uncertain. It expressly does **not** own model execution completion, answer correctness, H wire, G Applied, I authorization, D ForgetFence or Storage/COC/JF-10 outcome.

| C outcome | Exact semantic boundary | Retry/recovery rule |
|---|---|---|
| `HANDOFF_ACCEPTED` | Provider accepted the exact handed-off attempt; terminal for the handoff fact only | No second send for this Attempt; execution start/completion is separate evidence |
| `HANDOFF_REJECTED` | Authoritative provider rejection proves no accepted execution/side effect for this attempt | New Attempt only with new identity and fresh I/D/C gates |
| `NOT_INVOKED` | Positive C evidence proves no handoff crossed the egress boundary | New Attempt only after authoritative no-handoff proof and gate recheck |
| `UNKNOWN` | C cannot establish whether boundary was crossed | Nonterminal/non-expiring; reconcile; do not infer absence |
| `IN_DOUBT` | Handoff or provider side effect may have occurred, but authoritative outcome is unavailable | Nonterminal/non-expiring; no new Attempt/key; query same Provider key |

A transport timeout, local exception, missing receipt/ACK, process crash, missing request row, empty queue, absent COC intent or provider lookup outage is never proof of NOT_INVOKED or HANDOFF_REJECTED. A same-attempt recovery reuses the exact provider idempotency key and immutable request digest. If the Provider offers no authoritative same-key idempotency/lookup, C cannot promise exactly-once effects; ambiguous handoff remains IN_DOUBT and automatic retry is disabled.

CSubmitOutcome 1.0.1 schema Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` validates structure only. Its description explicitly leaves issuer authentication, append-only ledger inclusion, gate linearization, provider evidence and COC joins to semantic validation. The schema requires `sequence_namespace_ref`; Phase 3.11.1 binds record_sequence and key-status event sequence to the same durable monotonic namespace. The candidate signature profile `AIMBA-C-CRYPTO-1.0` remains NOT REGISTERED. This is not a production signing deployment.

### 中文精确语义
C Phase 3.8.4 明确规定：C 仅判断不可变最终推理请求是否跨越指定 Provider 的 Handoff 边界，以及该 Handoff 是否被接受、拒绝、证明未发生或仍不确定。C 不拥有模型执行完成、回答正确性、H Wire、G Applied、I 授权、D ForgetFence 或 Storage/COC/JF-10 结果。

HANDOFF_ACCEPTED 仅对 Handoff 事实终态，不代表推理完成；HANDOFF_REJECTED 必须有权威拒绝和无副作用证据；NOT_INVOKED 必须有正向证据证明未越过 Egress；UNKNOWN 与 IN_DOUBT 均为非终态、不得自动过期。IN_DOUBT 下禁止创建新 Attempt 或新幂等键，必须用同一 Provider Key 对账。若 Provider 不提供权威幂等/查询能力，C 不能承诺 Exactly-Once，自动重试必须禁用。

CSubmitOutcome 1.0.1 Schema 仅验证结构；Issuer Authentication、Append-only Ledger、Gate Linearization、Provider Evidence 和 COC Join 仍需语义验证。Schema 要求 sequence_namespace_ref；Phase 3.11.1 要求签名记录序列和 Key Status Event 序列位于同一持久单调命名空间。候选签名配置 AIMBA-C-CRYPTO-1.0 仍 NOT REGISTERED，不是生产签名部署。
