# Agent Integration Telemetry / Agent 集成遥测

## 1. Signals / 信号
- Traces: causal execution path across Agent, inference, tool and Brain spans.
- Metrics: bounded aggregate rates, latency histograms, token/usage totals where reported, queue depth, retry/failure/timeout/cancellation/outcome counts.
- Logs: structured diagnostic events with redaction and access controls.
- Audit: I-governed security/authorization/retention records; ordinary logs/traces are not immutable audit evidence.

## 2. Identifier separation / 标识符隔离
| Identifier | Meaning | Owner/source |
|---|---|---|
| TraceId / SpanId / ParentSpanId | Distributed causal trace | OTel instrumentation |
| CorrelationId | Business/workflow cross-link | B/C/H contract as agreed |
| RequestId | One logical inference or Brain request | Owning request authority |
| AttemptId | One execution attempt of a request | C/runtime contract |
| OperationId | One Brain domain operation | D/Brain authority |
| ProviderOperationId | Provider-issued operation handle | Provider, if available |
| ToolInvocationId | One tool invocation | Tool runtime |
| SessionId | Runtime/conversation scope | B/I typed identity authority |
| PrincipalRef / Tenant / ScopeRef | Authenticated identity and data boundary | I authorization + B typed refs |

Never substitute TraceId for RequestId, OperationId, idempotency key or authenticated Principal. External trace headers are untrusted input and must be sanitized or restarted at trust boundary.

## 3. Trace structure / Trace 结构
Root User Request → Agent Run → Inference Attempt → Tool Invocation (zero or more) → Brain API Request → Domain Operation → asynchronous evidence/ack spans. Preserve parent-child causality when actual propagation exists; use links for asynchronous or fan-in relationships. A trace can be incomplete and is not a business transaction log.

## 4. Metrics / 指标
Recommended low-cardinality metrics: request count/latency; provider latency by provider/model family; time-to-first-token; input/output token totals by provider/model family; tool duration by tool class; timeout/retry/cancel/failure counts; outcome distribution; backlog/queue age; Brain request latency. Do not label by user, tenant, SessionId, raw model prompt, request/operation ID or arbitrary tool arguments.

## 5. Logs / 日志
Log lifecycle event type, normalized error class, provider/tool family, opaque non-sensitive references where approved, attempt ordinal, durations and validation result. Do not default-log full prompts, model output, memory content, source documents, secrets, API keys, bearer tokens or raw tool arguments. Redaction must occur before export. Sampling must not suppress required security/audit records.

## 6. Privacy and audit / 隐私与审计
OTel W3C Trace Context propagates traceparent/tracestate; Baggage is arbitrary cross-service data and must not carry PII, secrets, tenant identifiers or sensitive memory. Do not forward internal trace/baggage to untrusted external Providers unless allowlisted. Retention, access, deletion and legal hold are I-owned policy decisions. Audit records require I-defined integrity, access, retention and export controls; a dashboard trace is not audit proof.

## 7. Implementation candidate / 实现候选
CANDIDATE: OpenTelemetry API/SDK with W3C Trace Context, structured redacted logs and Prometheus-compatible aggregate metrics. OTel Collector and Grafana are deployment options, not mandatory architecture. Exact Rust SDK/exporter versions and data residency policy remain TO_VALIDATE.
