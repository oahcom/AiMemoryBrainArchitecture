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


## 完整中文版本

Trace 记录 Agent、Inference、Tool 和 Brain 之间的因果执行路径；Metrics 记录低基数聚合速率、延迟、Usage、队列深度、重试/失败/超时/取消数量；Logs 是经过脱敏和访问控制的结构化诊断事件；Audit 由 I 治理，普通日志/Trace 不能作为不可篡改审计证据。

TraceId/SpanId/ParentSpanId 表示分布式追踪；CorrelationId 表示业务关联；RequestId 是逻辑请求；AttemptId 是一次尝试；OperationId 是 Brain 领域操作；ProviderOperationId 由 Provider 提供；ToolInvocationId 表示工具调用；SessionId 表示运行时会话；Principal/Tenant/Scope 由 I/B 管理。禁止互相替代。外部 Trace Header 是不可信输入。

调用链可以从 User Request 到 Agent Run、Inference Attempt、Tool Invocation、Brain API、Domain Operation，再到异步 Evidence/Ack。真实父子关系使用 Parent Span；异步或汇聚关系可用 Span Link。Trace 不完整不代表业务事务未完成。

建议使用低基数标签记录请求数、延迟、Provider/Model Family、TTFT、Token 总量、Tool 时长、超时/重试/取消/失败、Outcome 分布、队列积压和 Brain API 延迟。禁止将用户、Tenant、SessionId、Prompt、Request/Operation ID 或任意 Tool 参数放入 Metric Label。默认不记录完整 Prompt、模型输出、Memory、源文件、Secret、API Key、Bearer Token 或原始工具参数。

OTel W3C Trace Context 用于传播 traceparent/tracestate。Baggage 是任意跨服务数据，不得放 PII、Secret、Tenant ID 或敏感 Memory。向不可信 Provider 传播内部 Trace/Baggage 必须受控。保留期限、访问、删除和 Legal Hold 由 I 决定。Trace Dashboard 不是 Audit Proof。

候选使用 OpenTelemetry API/SDK、W3C Trace Context、结构化脱敏日志和 Prometheus 兼容聚合指标。Collector/Grafana 是部署候选，不是强制架构。Rust SDK/Exporter 版本和数据驻留策略仍待验证。



## OTel semantic convention currentness / OTel 语义规范当前性
The previously linked OpenTelemetry GenAI semantic-conventions page now explicitly says the conventions moved to the dedicated GenAI semantic-conventions repository and that the old page is no longer maintained. The current OTel documentation shell identifies semantic conventions release 1.45.0. Treat GenAI span/attribute names as versioned conventions to pin, not as a timeless stable schema. C's privacy allowlist and I's audit policy remain project-owned regardless of OTel conventions.

OpenTelemetry GenAI 语义规范原页面现明确说明规范已迁移至独立 GenAI semantic-conventions 仓库，旧页面不再维护；当前文档站标识的 Semantic Conventions 版本为 1.45.0。GenAI Span/Attribute 名称必须按版本固定，不能当作永恒不变的 Schema。无论采用何种 OTel 规范版本，C 的隐私白名单和 I 的 Audit Policy 仍由项目自身决定。
