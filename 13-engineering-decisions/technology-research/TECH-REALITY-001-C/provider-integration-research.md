# Provider Integration Research / Provider 集成研究

## 1. Method / 方法
Desk research uses official documentation and inspected project source pages available on 2026-11-18. Moving documentation is not a pinned release. Exact SDK/API versions and licenses must be pinned before implementation. Where official current source was not retrieved, mark NOT VERIFIED rather than infer parity.

本研究于 2026-11-18 检查可访问的官方文档和公开源码页面。滚动文档不是固定 Release。实现前必须固定 SDK/API 版本与许可证。未取得官方当前来源的能力标记 NOT VERIFIED，不推断兼容。

## 2. Provider observations / Provider 观察
| Provider/runtime | Verified in this pass | Constraints / not inferred |
|---|---|---|
| OpenAI Responses API | Official docs describe SSE streaming; structured outputs support a subset of JSON Schema; response streaming and function-call argument streaming are documented. | Do not infer universal cancellation/idempotency or full JSON Schema. Request/response lifecycle and usage must be recorded separately. |
| Anthropic Messages API | Official Messages reference inspected (API version `2026-10-21`): SSE streaming, message id/model/stop_reason/usage, client `tool_use` / `tool_result`; batch cancellation may leave in-progress non-interruptible requests running. | Stable request-id header, general synchronous cancellation, full error taxonomy and idempotency remain NOT VERIFIED; do not infer OpenAI parity. |
| Google Gemini API | Official `streamGenerateContent` docs show responseId, modelVersion, usageMetadata and functionCall proposal fields. Tool execution is client/system responsibility. | API shown as v1beta in retrieved docs; model/tool support varies. A functionCall is a proposal, not execution. |
| vLLM | Official docs list supported OpenAI-compatible endpoints including Chat Completions, Responses and Embeddings; exposes /metrics. Docs warn --api-key does not protect all endpoints (notably /invocations). | Compatibility is endpoint/feature-specific. Must harden network/auth independently and pin exact vLLM version. |
| llama.cpp server | Official source README lists OpenAI-compatible chat/responses/embeddings, Anthropic-compatible Messages, streaming, multimodal and function calling with template requirements. It explicitly avoids strong claims of full OpenAI spec compatibility. | Tool use may require --jinja/chat-template; endpoint semantics differ. |
| Ollama Chat API | Official `/api/chat` endpoint inspected: streaming default, optional tools and JSON/JSON Schema format; response includes done/done_reason, timing and token counters. | The inspected endpoint does not establish provider operation ID, cancellation or idempotency; model-specific capability coverage remains TO_VALIDATE. |
| Hugging Face Inference Providers | Official router/routing docs inspected: provider selection and failover can switch serving provider; Chat Completions, beta Responses, Messages, Tool Calling and Structured Outputs are listed with provider/model-dependent support. | Router-level failover is distinct from C Attempt and Brain idempotency; stable operation identity, exact per-model semantics, cancellation and idempotency remain NOT VERIFIED. |
| OpenAI-compatible endpoints | Useful transport/request-shape compatibility layer. | Does not prove equivalent semantics, streaming events, usage, tool behavior, cancellation, idempotency or security. |

## 3. Agent framework observations / Agent 框架
- Hermes Agent: inspected official architecture docs/source pages. Its loop resolves provider, calls model, dispatches registered tools, persists sessions in SQLite, supports gateway/cron/ACP entrypoints and profile isolation. It is a complete Python Agent runtime, not a Brain core.
- LangGraph: official interrupt docs describe checkpointed pause/resume using thread_id and persistence; resumed nodes restart from the beginning, so pre-interrupt side effects must be idempotent/guarded.
- PydanticAI: official docs describe typed agent/tool interfaces, tool retry budgets and deferred tool results. Retry policy is runtime behavior, not proof a side effect is safe to repeat.
- OpenAI Agents SDK: official docs describe tools, MCP integration, sessions, human-in-the-loop and built-in tracing. Tracing has product/data-retention constraints; it cannot replace Brain audit.
- AutoGen: current Microsoft migration docs describe a migration path to Microsoft Agent Framework and differing runtime/tool capabilities. Treat AutoGen as an evolving candidate, not a stable cross-provider core.
- MCP: protocol is a tool/resource/prompt integration protocol, not an authorization authority. Current protocol revision and transport/session details must be pinned; do not confuse MCP identity with I Principal.

## 4. Provider capability matrix / Provider 能力矩阵
Normalize only stable concepts: request identity, attempt identity, provider/model identity, capability declaration, stream event envelope, parsed output reference, error class, usage where reported, timestamps, cancellation request and reconciliation handle. Keep provider-native extensions for response IDs, safety/block reasons, cache accounting, modality, tool-call IDs, batch operations, server-side status lookup and model-version metadata.

只标准化稳定概念：Request/Attempt 身份、Provider/Model 身份、能力声明、流事件封套、解析输出引用、错误类别、可用 Usage、时间、取消请求和对账句柄。Provider 原生扩展保留 Response ID、安全拦截原因、缓存计量、多模态、Tool Call ID、Batch 操作、服务端状态查询和 Model Version 元数据。

## 5. Adapter design conclusion / Adapter 结论
**CANDIDATE:** layered capability registry + provider-specific adapters. Define a narrow Brain-facing port and preserve raw provider response metadata in a bounded extension envelope. Capability negotiation is explicit and versioned. Unsupported capability must fail closed or degrade explicitly; never silently emulate a semantic guarantee.
- Standardize lifecycle/evidence fields, not every provider request field.
- Keep provider SDK native features accessible through explicit extensions.
- Separate provider adapter from Agent framework and Tool executor.
- Test streaming event order, partial output, finish/error, usage and cancellation independently per provider/model family.

## 6. License and version / 许可证与版本
Official docs pages reviewed do not establish a pinned SDK release/license for every framework/provider. **NOT VERIFIED** for Anthropic SDK, Gemini SDK, Ollama, Hugging Face Inference, AutoGen package and MCP SDK versions/licenses in this pass. No package is approved by this report.


## 完整中文版本

本研究于 2026-11-18 检查官方文档和公开源码。滚动文档不等于固定 Release。实现前必须固定 API/SDK 版本和许可证。没有检查到官方当前证据的能力标记 NOT VERIFIED，不能推断 Provider 之间完全兼容。

OpenAI Responses 官方资料说明 SSE 流式响应和 Structured Outputs 的 JSON Schema 子集；不能据此推断所有 Schema 均支持，也不能推断所有请求都有取消或幂等保证。Anthropic Messages 已补充核验官方 API 版本 `2026-10-21`、SSE、Message ID/Model/Stop Reason/Usage 和客户端 Tool 往返；稳定 Request ID、通用同步取消、完整错误分类和幂等语义仍 NOT VERIFIED。Gemini streamGenerateContent 文档展示 responseId、modelVersion、usageMetadata 和 functionCall；functionCall 是模型提出的调用，不是系统已经执行工具。vLLM 官方文档列出部分 OpenAI-compatible Chat、Responses、Embeddings API，并提供 /metrics；其文档明确警告 --api-key 并不保护所有端点。llama.cpp Server 文档列出 OpenAI-compatible 和 Anthropic-compatible 路由、流式、多模态和工具调用，但不承诺完全符合 OpenAI 规范；工具调用可能依赖 Jinja/Chat Template。Ollama Chat 与 Hugging Face Inference Providers 已补充核验具体端点/路由事实；逐模型能力覆盖、稳定操作身份、取消和幂等语义仍 NOT VERIFIED。

Hermes 是具有 Provider Resolver、Tool Registry、SQLite Session、Gateway 等模块的 Python Agent Runtime，可供架构参考，但不是 Brain Core。LangGraph 提供 Checkpoint/Interrupt/HITL，恢复时节点可能从头执行，因此副作用必须具备幂等保护。PydanticAI 提供类型化工具、重试和 Deferred Tool Result；重试预算是框架行为，不代表副作用安全。OpenAI Agents SDK 提供工具、MCP、Session、HITL 和内建 Tracing，但 Tracing 不能替代 Brain Audit。AutoGen 生态正在演进，不应未经版本/支持审查冻结依赖。MCP 是工具/资源集成协议，不是身份授权权威。

候选采用分层 Capability Registry 加 Provider 专属 Adapter。标准化 Request/Attempt/Evidence、错误分类、流事件封套和可用 Usage；保留 Provider 原生 Response ID、Model Version、安全拦截、多模态、缓存计量、Batch、取消和 Tool Call ID。能力缺失必须显式降级或拒绝，不能静默模拟保证。



## Additional official-source verification — 2026-11-18 / 官方来源补充核验

### Newly verified provider facts / 新核验 Provider 事实
- **Anthropic Messages API:** current reference identifies API version `2026-10-21` and `POST /v1/messages`; `stream=true` streams server-sent events. The response exposes a message id, model, stop_reason and usage (including cache counters). Client tool definitions may yield `tool_use` blocks; the client executes tools and returns `tool_result`. Batch cancellation can enter `canceling` while in-progress non-interruptible requests may still complete. A stable request-id header and general synchronous cancellation guarantee were not verified.
- **Ollama Chat API:** `POST /api/chat`; `stream` defaults true; request supports optional `tools` and `format` as JSON or JSON Schema. Response reports `done`, `done_reason`, total/load/eval durations and token counts. The inspected endpoint page does not establish a provider operation ID or cancellation/idempotency guarantee.
- **Hugging Face Inference Providers:** requests pass through an HF router; for language models OpenRouter selects a serving provider and can retry on another provider if it fails. Routing considers price, speed/TTFT and reliability; provider can change over time. This is a distinct router-level retry/failover layer and must not be confused with a C client Attempt or Brain idempotency. The documentation lists Chat Completion, Responses API (beta), Messages, Tool Calling, Structured Outputs, Prompt Caching and Embeddings; exact support remains model/provider dependent.
- **MCP Specification 2025-11-25:** JSON-RPC 2.0 host/client/server roles, stateful connections and capability negotiation; resources, prompts and tools; cancellation, progress, error reporting and logging. Security principles explicitly cover user consent, privacy and tool safety; tools can represent arbitrary code execution. MCP is a tool/context protocol, not a Brain identity or canonical Memory authority.

### Revised provider status / 修订状态
Anthropic, Ollama and Hugging Face are no longer marked wholly NOT VERIFIED: the above endpoint/routing facts are now source-inspected. Their full error taxonomy, stable request identifiers, per-model capability coverage, cancellation semantics, SDK release/license and idempotency behavior remain **NOT VERIFIED** and require per-version conformance tests.

### 中文补充
Anthropic 当前 Messages API 参考版本为 `2026-10-21`，接口为 `POST /v1/messages`；`stream=true` 使用 SSE。响应包含 Message ID、Model、Stop Reason 和 Usage（含缓存计量）。客户端 Tool 定义可能产生 `tool_use`，实际工具由客户端执行，再以 `tool_result` 返回。Batch 取消进入 canceling 后，已在执行且不可中断的请求仍可能完成。稳定 Request-ID Header 和通用同步取消保证本轮未核实。

Ollama `POST /api/chat` 默认启用 Streaming，支持可选 Tools 和 JSON/JSON Schema Format；响应提供 done、done_reason、总耗时/加载/推理耗时和 Token 数量。当前检查的接口页没有证明 Provider Operation ID、取消或幂等保证。

Hugging Face Inference Providers 通过 Router 处理请求；语言模型由 OpenRouter 选择实际 Provider，失败时可能切换另一个 Provider。路由会考虑价格、速度/首 Token 时间和可靠性。该路由器重试是独立于 C Client Attempt 和 Brain 幂等性的另一层。文档列出 Chat Completion、Responses API beta、Messages、Tool Calling、Structured Outputs、Prompt Caching 和 Embeddings，但具体能力依赖模型和 Provider。

MCP 2025-11-25 规范使用 JSON-RPC 2.0，定义 Host/Client/Server、Stateful Connection、能力协商、Resources/Prompts/Tools，并提供 Cancellation、Progress、Error Reporting 和 Logging。安全原则明确要求用户同意、数据隐私和 Tool 安全；Tool 可能代表任意代码执行。MCP 不是 Brain 身份或 Canonical Memory 权威。

因此 Anthropic、Ollama 和 Hugging Face 不再整体标记为 NOT VERIFIED；上述具体事实已核验。但完整错误分类、稳定请求标识、逐模型能力、取消语义、SDK 版本/许可证和幂等行为仍未核验。
