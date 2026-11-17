# Agent Integration Validation Plan / Agent 集成验证计划

**Execution status: ALL SCENARIOS NOT RUN unless separately evidenced.** Design plan is not test completion.

| ID | Given | When | Then / expected outcome | Evidence | Failure condition | Owner / contract |
|---|---|---|---|---|---|---|
| V01 | One Agent + one Provider | Invoke structured request | Attempt and provider handoff evidence distinct from output validation | request/attempt/result refs | One success flag only | C |
| V02 | One Agent, two configured Providers | Switch provider | ProviderRef/ModelRef and capabilities change explicitly | adapter config + trace | silently inherit capability | C/I |
| V03 | Provider supports structured output | Return valid/invalid payload | Parse and domain validation separately recorded | raw digest + validator result | parse treated as truth | C/B |
| V04 | Provider returns 429/5xx | Receive error | Native code retained; retry policy bounded | error class/retry-after | generic retry | C |
| V05 | Request sent, client timeout | Timeout before final provider outcome | UNKNOWN/IN_DOUBT; same Attempt reconciled | handoff/receipt/provider lookup | new attempt blindly sent | C |
| V06 | Tool read-only | Tool succeeds | Tool result evidence linked to invocation | tool receipt/result digest | result becomes canonical directly | I/C/D |
| V07 | Tool side effect then response lost | Client retries | Reconcile target system; no blind duplicate | external operation ref | duplicate side effect | I/tool host |
| V08 | Same logical request retried | Retry policy permits | New Attempt identity; idempotency namespace explicit | attempt ledger | attempt identity reused | C |
| V09 | Duplicate identical result | Result arrives twice | Duplicate observation linked by digest | result refs | overwrite history | C/H |
| V10 | Late conflicting result | Different result arrives late | preserve both; reconciliation required | timestamps/digests | last-write-wins | C |
| V11 | Valid candidate input | Submit to Brain | Candidate accepted/rejected, no direct lifecycle bypass | candidate receipt | Agent writes canonical store | C/D/E |
| V12 | Brain accepted but not Applied | Read receipt | report operation status accurately; no Applied claim | D receipt, G record absent | receipt interpreted as Applied | D/G |
| V13 | Context version stale | Agent requests use | reject or reconcile stale reference | ContextVersion and invalidation evidence | stale context silently reused | F/G/H |
| V14 | Forget fence advances during inference | Late output submits candidate | current fence/lineage check suppresses stale result | fence cursor + result provenance | resurrection | D/E/F/I |
| V15 | Two Agents, separate Sessions | concurrent requests | scope/session identity isolation | typed refs and trace | cross-session leakage | B/I |
| V16 | Tenant A principal targets Tenant B | Brain request | deny before resource disclosure | authorization decision/audit | data returned | I |
| V17 | Trace crosses Agent/Provider/Tool/Brain | propagate trace context | causal parent/link preserved; IDs remain distinct | exported trace | TraceId used as RequestId | C/Observability |
| V18 | Prompt/output contains sensitive data | telemetry export | redacted/minimized; no high-cardinality user labels | redaction test and captured export | secret/content leakage | I/Observability |
| V19 | Provider cancel requested | provider still completes late | retain cancel request and late completion separately | event ordering | cancellation treated as rollback | C |
| V20 | Brain commit succeeds, ACK lost | caller retries | same OperationId/idempotency resolves existing commit | commit receipt | duplicate canonical operation | D/Storage |

## Benchmark plan / 基准计划
Measure provider invocation latency, Brain client latency, time-to-first-token, tool duration, retry overhead and telemetry overhead. Report workload, machine, provider/model version, concurrency, warm/cold state, sample count, p50/p95/p99 and confidence intervals. Separate observed measurements, provider-published claims, estimates and hypotheses. No benchmark executed in this research: **NOT RUN**.


## 完整中文版本

**执行状态：以下全部场景均 NOT RUN。** 设计方案不等于测试完成。

V01 单 Agent/单 Provider：分别记录 Attempt、Handoff 和输出验证。V02 单 Agent 切换两个 Provider：Provider/Model 和能力必须显式变化。V03 结构化输出：解析和领域验证分离。V04 Provider 429/5xx：保留原生错误并受控重试。V05 已发送后客户端超时：记录 UNKNOWN/IN_DOUBT，对账同一 Attempt。V06 Tool 成功：结果证据关联调用，不直接变 Canonical。V07 Tool 副作用后响应丢失：先对账外部系统，防止重复副作用。V08 重试相同逻辑请求：创建新 Attempt，幂等命名空间明确。V09 重复结果：按 Digest 关联，不覆盖历史。V10 迟到冲突结果：保留双方并要求 Reconciliation。V11 Memory 候选提交：不允许 Agent 绕过 D/E。V12 Brain 已接受但未 Applied：不得将 Receipt 当 Applied。V13 Context Version 失效：拒绝或 Reconcile 旧引用。V14 Forget 与迟到推理竞争：Fence/Lineage 检查阻止复活。V15 多 Agent 不同 Session：隔离身份和 Scope。V16 跨 Tenant 请求：I 在资源访问前拒绝。V17 Trace 跨 Agent/Provider/Tool/Brain：因果关系传播，ID 不混用。V18 敏感内容遥测：导出前正确脱敏。V19 Provider 取消后迟到完成：分别记录取消请求和实际完成。V20 Brain Commit 成功但 ACK 丢失：相同 OperationId/幂等键恢复。

基准测试测量 Provider 调用延迟、Brain Client 延迟、首 Token 时间、Tool 执行时间、重试开销和遥测开销。必须记录工作负载、机器、Provider/Model 版本、并发度、冷热状态、样本数和 p50/p95/p99。区分实测、Provider 文档声明、估计和假设。本研究没有执行任何基准：NOT RUN。



## Additional conformance scenarios / 补充符合性场景

- **V21 — Router-level provider failover:** Given an inference router that can retry another provider, when the first provider fails, then record router-selected actual provider, router retry/failover observation and logical C Attempt separately; do not collapse router retries into an invisible exactly-once claim. Evidence: router/provider response metadata and trace. Owner: C/provider router.
- **V22 — MCP tool consent and untrusted annotations:** Given an MCP Server exposes a tool and annotations/descriptions, when the Host proposes invocation, then Host/I policy must treat untrusted server annotations as untrusted, require explicit user consent as applicable, and enforce tool safety/data access policy before execution. Evidence: consent decision, server identity, tool manifest and invocation receipt. Owner: I/H/tool host.

### 中文补充
V21 验证推理路由器内部切换 Provider 时，记录实际 Provider、路由器内部重试和 C 逻辑 Attempt，不能把路由器切换隐藏成 exactly-once。V22 验证 MCP Tool 调用前的用户同意、Server 身份、工具描述可信度和 I 授权，不能把 Tool Annotation 当作安全证明。
