# Evidence Index / 证据索引

Research capture date: 2026-11-18. Prefer official, versioned documentation; moving docs require re-check before implementation.

## Official provider/runtime sources
- OpenAI Responses streaming: https://developers.openai.com/api/docs/guides/streaming-responses
- OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Agents SDK capabilities: https://openai.github.io/openai-agents-python/
- OpenAI Agents tracing: https://openai.github.io/openai-agents-python/docs/tracing/
- Gemini GenerateContent / streamGenerateContent: https://ai.google.dev/api/generate-content
- vLLM OpenAI-compatible server: https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/
- llama.cpp server source/docs: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

## Agent framework source inspections
- Hermes Agent architecture: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/architecture.md
- Hermes Agent tools reference: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/tools-reference.md
- LangGraph interrupts/checkpointing: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/breakpoints/
- PydanticAI retries: https://pydantic.dev/docs/ai/core-concepts/retries/
- PydanticAI deferred tool results: https://github.com/pydantic/pydantic-ai/blob/main/docs/toolsets.md
- AutoGen migration context: https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/
- MCP specification changelog: https://modelcontextprotocol.io/specification/draft/changelog

## Observability/security
- OpenTelemetry context propagation: https://opentelemetry.io/docs/concepts/context-propagation/
- OTel GenAI conventions (moved): https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Project evidence
- Main baseline HEAD: b3c666e67982cb3d3374e759cfb6552c7765aacb
- A PR #45 research HEAD: 6c7c5919c1b50f38c4d24be679a3885ee3c15b97; A independent review PR #56 verdict REVISE.
- B PR #55 research HEAD: f95b479b223ebb63c8aebcfca13a4cd9b28d5331; Draft; B0 partial and B5 blocked.
- C old branch HEAD: 71047cdb51139ca4080ac67f451e38a48698859d; diverged from current main.
- D Forget contract Blob: 1f0391bc49d007c44ec74165bd33d37412cc7990.
- G Applied contract Blob: aa3afa73d8a76cc6f025839c52bfbff6a983046a.
- H Unified 1.2.15 schema Blob: 860fc4cec658db7d2703cd6adf72aa31a2723f6d.
- I governance register Blob: f5fd2558c657f4ef49396a7a00cdbcd0f226f853.
- Storage v3.3.2 manifest Blob: 5c614375e10698e4931d83deb57d20321445e068.

## Limitations / 限制
Anthropic Messages, Ollama, Hugging Face Inference, current AutoGen package versions, exact SDK releases/licenses, provider cancellation/idempotency semantics and complete current MCP security profiles were not fully verified in this pass. Do not treat absent sources as negative capability evidence.


## 中文证据索引

官方 Provider/Runtime 资料包括 OpenAI Responses 流式文档、OpenAI Structured Outputs、OpenAI Agents SDK、Gemini GenerateContent、vLLM OpenAI-Compatible Server 和 llama.cpp Server。它们用于核验具体 API/能力，不证明跨 Provider 完全等价。

Agent 框架资料包括 Hermes Architecture/Tools、LangGraph Interrupts、PydanticAI Retries/Deferred Tools、Microsoft AutoGen Migration 和 MCP Specification Changelog。滚动文档在正式实现前需重新固定版本。

OpenTelemetry Context Propagation 说明 Trace Context 跨进程传播，以及对不可信外部 Trace Header 和 Baggage 的安全注意事项。GenAI Semantic Conventions 页面已迁移，需检查新规范仓库。

项目证据：main HEAD b3c666...；A PR #45 Draft、A Review PR #56 REVISE；B PR #55 Draft；D/G/H/I/Storage 使用精确 Branch/Blob Pin。H 1.2.15 和 Storage v3.3.2 不匹配，G Applied 仍阻塞。

本轮未完整核验 Anthropic Messages、Ollama、Hugging Face Inference、AutoGen 当前包版本、全部 SDK 许可证、Provider Cancellation/Idempotency 语义及完整 MCP 安全配置。没有来源不代表能力不存在。



## Additional official sources verified / 新增已核验官方来源
- Anthropic Messages API reference (API version 2026-10-21): https://platform.claude.com/docs/en/api/http/beta/messages/create
- Ollama Chat endpoint: https://docs.ollama.com/api/chat
- Hugging Face Inference Providers: https://huggingface.co/docs/inference-providers/index
- Hugging Face provider routing/failover: https://huggingface.co/docs/inference-providers/routing
- MCP specification 2025-11-25: https://modelcontextprotocol.io/specification/2025-11-25
- OpenTelemetry GenAI conventions landing/migration page: https://opentelemetry.io/docs/specs/semconv/gen-ai/ (page says moved; current docs registry shows semantic conventions 1.45.0)

### 中文说明
上述来源补齐了 Anthropic Messages、Ollama Chat、Hugging Face Router/Failover、MCP 2025-11-25 和 OTel GenAI 规范迁移状态。它们只证明所列官方文档明确记载的能力，不证明完整 API 等价、稳定 Request ID、统一取消、幂等或许可证状态。上述未明确的内容仍需固定版本后逐项验证。
