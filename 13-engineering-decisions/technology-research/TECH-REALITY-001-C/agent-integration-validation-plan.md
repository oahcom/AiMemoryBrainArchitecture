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
