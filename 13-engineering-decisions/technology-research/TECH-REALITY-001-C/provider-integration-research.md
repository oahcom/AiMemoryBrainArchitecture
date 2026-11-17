# Provider Integration Research / Provider 集成研究

## 1. Method / 方法
Desk research uses official documentation and inspected project source pages available on 2026-11-18. Moving documentation is not a pinned release. Exact SDK/API versions and licenses must be pinned before implementation. Where official current source was not retrieved, mark NOT VERIFIED rather than infer parity.

本研究于 2026-11-18 检查可访问的官方文档和公开源码页面。滚动文档不是固定 Release。实现前必须固定 SDK/API 版本与许可证。未取得官方当前来源的能力标记 NOT VERIFIED，不推断兼容。

## 2. Provider observations / Provider 观察
| Provider/runtime | Verified in this pass | Constraints / not inferred |
|---|---|---|
| OpenAI Responses API | Official docs describe SSE streaming; structured outputs support a subset of JSON Schema; response streaming and function-call argument streaming are documented. | Do not infer universal cancellation/idempotency or full JSON Schema. Request/response lifecycle and usage must be recorded separately. |
| Anthropic Messages API | Official current API details not inspected in this pass: **NOT VERIFIED**. | Do not claim identical event, cache, tool, batch, cancellation or error semantics to OpenAI. |
| Google Gemini API | Official `streamGenerateContent` docs show responseId, modelVersion, usageMetadata and functionCall proposal fields. Tool execution is client/system responsibility. | API shown as v1beta in retrieved docs; model/tool support varies. A functionCall is a proposal, not execution. |
| vLLM | Official docs list supported OpenAI-compatible endpoints including Chat Completions, Responses and Embeddings; exposes /metrics. Docs warn --api-key does not protect all endpoints (notably /invocations). | Compatibility is endpoint/feature-specific. Must harden network/auth independently and pin exact vLLM version. |
| llama.cpp server | Official source README lists OpenAI-compatible chat/responses/embeddings, Anthropic-compatible Messages, streaming, multimodal and function calling with template requirements. It explicitly avoids strong claims of full OpenAI spec compatibility. | Tool use may require --jinja/chat-template; endpoint semantics differ. |
| Ollama | Current official API capability matrix not inspected: **NOT VERIFIED**. | Treat as local candidate only; verify model-specific tool/structured/multimodal behavior and cancellation. |
| Hugging Face Inference | Current provider-specific inference API semantics not inspected: **NOT VERIFIED**. | Endpoint/provider/model deployment differences require individual adapter tests. |
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
