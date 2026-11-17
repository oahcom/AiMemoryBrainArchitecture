# Agent Integration Failure Semantics / Agent 集成失败语义

| Scenario | Observable / unknown | Safe action | Retry | Duplicate risk | Evidence / owner / gate |
|---|---|---|---|---|---|
| DNS/connection failure before proven handoff | no provider receipt; handoff boundary may be unknown | classify UNKNOWN unless positive NOT_INVOKED proof | only after same-attempt reconciliation | possible | resolver/transport logs; C; C3 |
| Provider 429/rate limit | provider-native status/retry-after if received | preserve exact response; obey bounded retry policy | new Attempt only if rejection proves no side effect | medium | provider response ID/error; C |
| Provider 5xx/connection reset after send | provider may have processed | IN_DOUBT; query same provider key/operation | no new attempt until reconciled | high | attempt, key, provider receipt; C/Storage |
| Partial/malformed stream | output incomplete or parser uncertain | retain partial result separately; no final output claim | resume only if provider supports; else new Attempt after disposition | medium | stream sequence, terminal marker, raw digest; C |
| Agent crash/restart | local session/checkpoint may be stale | restore checkpoint, revalidate I/D/G currentness | resume idempotent step only | high | checkpoint version, attempt IDs; Agent owner/C |
| Tool side effect completed, response lost | external state unknown to caller | reconcile target system before retry | no blind retry | high | ToolInvocationId, external operation receipt; I/tool host |
| Tool cancellation race | cancellation requested, completion may race | record request separately from observed terminal result | no assumption of rollback | high | cancellation and completion timestamps; tool host |
| Brain accepted/committed, ACK lost | caller sees timeout; operation may exist | query/replay same OperationId/idempotency key | same operation only | high | D receipt/commit evidence; D/Storage |
| Duplicate/late Provider result | same Attempt receives multiple observations | immutable append; digest compare; conflict => reconcile | no new attempt due result arrival | medium | result digest and sequence; C/H |
| Forget races with inference/tool result | stale lineage may return after fence | D fence check at candidate/commit; suppress stale references | reject or quarantine | critical | ForgetFenceGeneration, lineage proof; D/E/F/I |
| Context invalidated mid-run | ContextVersion/capability/permission changed | stop future reuse; G reconciliation; do not relabel historical Applied | new ContextVersion only | medium | G Applied/invalidated records; G/I |
| Cross-tenant request | principal/scope mismatch | deny before data access and log security event | no retry absent changed authority | critical | authenticated principal, policy epoch; I |
| Provider result after Session closure | session no longer active | retain only under policy; no automatic context reopen | no | low/medium | session state and result provenance; B/I/C |

## General invariants / 通用不变量
Timeout ≠ failure. Cancellation request ≠ rollback. HTTP 200 ≠ business success. Missing ACK ≠ no commit. Provider acceptance ≠ model completion. Tool success ≠ external state verification. Applied ≠ model attention. Forget suppression ≠ physical erasure.

超时不等于失败；取消请求不等于回滚；HTTP 200 不等于业务成功；ACK 缺失不等于未提交；Provider 接受不等于模型完成；Tool 成功不等于外部状态已验证；Applied 不等于模型注意；Forget 抑制不等于物理擦除。
