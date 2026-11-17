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


## 完整中文版本

| 场景 | 安全处理原则 |
|---|---|
| DNS/连接失败 | 若不能证明请求未越过 Provider 边界，记录 UNKNOWN，不自动标记 NOT_INVOKED。 |
| 429/限流 | 保留 Provider 原生状态和 Retry-After；仅在拒绝证明无副作用时允许新 Attempt。 |
| 发送后 5xx/连接重置 | Provider 可能已执行，记录 IN_DOUBT，先查询同一 Provider Operation/Key。 |
| 部分或畸形流 | 保留 Partial Result，不声明最终输出；记录事件序列和终止标记。 |
| Agent 崩溃 | 恢复检查点后重新验证 I/D/G 当前性；可能重复的步骤必须幂等。 |
| Tool 副作用完成但响应丢失 | 先查询外部系统对账，不盲目再次调用。 |
| 取消竞态 | 分别记录取消请求和实际完成；取消不代表副作用撤销。 |
| Brain 已 Commit 但 ACK 丢失 | 使用相同 OperationId/幂等键查询或重放，不创建新操作绕过未知状态。 |
| Provider 迟到/重复结果 | 不可变追加，按 Digest 识别重复，冲突进入 Reconciliation。 |
| Forget 与推理/工具结果竞争 | 候选和 Commit 阶段重新检查 Forget Fence/Lineage，抑制旧结果。 |
| Context 失效 | 禁止未来复用旧 Context，交由 G Reconcile；历史 Applied 记录保留。 |
| 跨 Tenant 请求 | I 在资源读取前拒绝，保留安全审计证据。 |
| Session 关闭后 Provider 返回 | 仅按保留策略记录证据，不自动重新打开 Session/Context。 |

通用不变量：Timeout 不等于 Failure；Cancel 不等于 Rollback；HTTP 200 不等于业务成功；ACK 缺失不等于未 Commit；Provider 接受不等于模型完成；Tool 成功不等于外部状态已验证；Applied 不等于模型注意；Forget 抑制不等于物理擦除。
