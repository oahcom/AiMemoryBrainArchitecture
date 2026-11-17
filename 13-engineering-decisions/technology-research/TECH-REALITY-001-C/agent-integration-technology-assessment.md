# Agent Integration Technology Assessment / Agent 集成技术评估

## 1. Architecture options / 架构方案
| Option | Shape | Benefits | Costs/risks | Current disposition |
|---|---|---|---|---|
| A Direct Provider | Agent runtime uses native provider SDK and Brain API | Low latency, simple deployment, provider features visible | Repeated adapter/evidence/privacy logic; inconsistent retries | Candidate for tiny single-agent spike only |
| B Central Gateway | All Agent/Provider calls through gateway | Central policy, routing and telemetry | Gateway becomes availability bottleneck and duplicate state authority risk; does not replace I | Defer until multiple clients need central routing |
| C Modular Integration Layer | Agent interface, Provider adapters, Tool boundary, Evidence, Telemetry, Brain client as modules in one deployable | Clear logical boundaries, testable adapters, no forced microservices | Requires disciplined module contracts | **Preferred candidate for current phase** |
| D Distributed services | Separate Agent/Provider/Tool/Integration services | Isolation and independent scaling | Operational, consistency, trace and recovery complexity; premature for current local-first phase | Deferred/rejected as initial topology |

## 2. Recommendation / 推荐
**CANDIDATE — modular Integration Layer inside the A-candidate local-first Rust modular monolith**, with Agent-specific adapters and optional isolated inference worker. Do not make the Brain own an Agent planner or tool catalog. Do not require Kubernetes, broker or centralized gateway for the first vertical slice. This aligns with A's candidate stack but does not approve A's topology.

**候选方案：** 在 A 提出的本地优先 Rust 模块化单体候选中实现模块化 Integration Layer，Agent 专属 Adapter 独立适配，推理 Worker 可选隔离。Brain 不拥有 Agent Planner 或通用 Tool Catalog。首个垂直切片不强制 Kubernetes、Broker 或中央 Gateway。此方向与 A 的候选技术栈一致，但不代表批准 A 的拓扑。

## 3. Provider adapter options / Provider Adapter 方案
| Option | Advantages | Losses/risks | Disposition |
|---|---|---|---|
| A independent adapter per provider | Full native behavior | Duplication and inconsistent semantics | Keep native adapters as implementation units |
| B one normalized interface | Simple callers | Capability loss and false parity | Reject as sole abstraction |
| C capability registry + adapters | Explicit support matrix and extensions | Registry maintenance | Preferred candidate |
| D common request + capability negotiation | Useful for routing | Negotiation itself cannot guarantee execution semantics | Combine with C, not substitute |

Standardize request/attempt/evidence lifecycle, error categories, stream envelope and optional usage. Preserve provider-native fields for response IDs, model versions, safety, modality, cache/usage, batch, cancellation and tool-call IDs.

## 4. Framework fit / Agent 框架适用性
- Hermes: useful real-world single-process Python runtime reference (provider resolver, tool registry, SQLite sessions, gateways). Not Brain core; broad built-in tools and mutable runtime session state are not canonical memory authority.
- LangGraph: strong workflow/checkpoint/HITL reference; checkpoint replay can re-execute node code, so external side effects need explicit idempotency. Optional Agent runtime, not a Brain dependency.
- PydanticAI: typed validation, retries, deferred tool result pattern; useful Python client adapter or prototype. Its retry counter semantics are framework-specific.
- OpenAI Agents SDK: tools, handoffs, sessions, MCP and built-in traces; useful provider-specific runtime option, not vendor-neutral Brain core or audit authority.
- AutoGen: evolving ecosystem with migration toward Microsoft Agent Framework; do not freeze dependency without current support/license review.
- MCP: tool/resource integration protocol, not Agent identity, permission policy or canonical Memory protocol.

## 5. Technology layers / 技术层
| Layer | Candidate | Constraint |
|---|---|---|
| Core runtime | Rust + Tokio (A candidate) | Project language direction exists; Tokio selection still needs ADR/prototype |
| Provider SDK | Native SDK per provider behind adapter port | Pin versions and capability conformance |
| Local inference | vLLM / llama.cpp / Ollama | vLLM and llama.cpp source-inspected; Ollama NOT VERIFIED in this pass |
| Protocol | H/BMCP for Brain contract; MCP only where tool ecosystem requires | H owns BMCP; no replacement by MCP |
| Serialization | JSON Schema for versioned external envelopes; Serde for Rust mapping | Exact schema/field authority remains owner-specific |
| Retry | Explicit attempt state machine + provider-specific idempotency | Never generic retry on timeout |
| Streaming | Provider-native stream parser, normalized internal event envelope | SSE/WebSocket not interchangeable guarantees |
| Telemetry | OpenTelemetry + structured redacted logs + aggregate metrics | I privacy/audit approval required |

## 6. Selection classification / 选型分类
- DECIDED: no provider/framework is made canonical by this report; Agent/Model/Provider are distinct roles.
- CANDIDATE: modular Integration Layer, layered capability registry and provider-specific adapters.
- TO_VALIDATE: Rust SDK ecosystem, streaming, cancellation, local inference, telemetry overhead, multi-provider failover.
- DEFERRED: distributed Agent gateway/services, mandatory broker, vector retrieval and multi-agent orchestration in Brain.
- REJECTED: single success enum; framework-owned canonical memory; blind retry; treating OpenAI-compatible as full semantic compatibility.
