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


## 完整中文版本

### 架构方案
A Direct Provider：Agent Runtime 直接使用 Provider SDK 和 Brain API，部署简单、原生能力完整，但 Adapter/证据/隐私逻辑重复，仅适合极小型单 Agent Spike。B Central Gateway：统一身份路由和遥测，但 Gateway 可能成为单点和重复状态权威，且不能替代 I，当前阶段暂缓。C Modular Integration Layer：在单一可部署模块化结构内分离 Agent Interface、Provider Adapter、Tool Boundary、Execution Evidence、Telemetry 和 Brain Client，复杂度适中，最适合当前候选阶段。D Distributed Services：隔离和独立扩展能力强，但带来运维、一致性、Trace 和恢复复杂度，当前阶段延期。

候选在本地优先 Rust 模块化单体内建设模块化 Integration Layer，Agent 专属 Adapter 独立适配，Inference Worker 可选隔离。不把 Agent Planner 或 Tool Catalog 放入 Brain Core，不强制 Kubernetes、Broker 或中央 Gateway。此为候选，不是 A 的部署拓扑批准。

逐 Provider 独立 Adapter 保留原生能力但有重复；单一统一接口易丢失能力；Capability Registry 加专属 Adapter 可明确支持矩阵和扩展字段；统一请求加能力协商可与 Registry 结合，但不能保证运行语义等价。建议采用后两者组合。

Hermes 适合作为真实 Python Agent Runtime 参考，不是 Brain Core。LangGraph 的 Checkpoint/HITL 能力有用，但恢复时节点可能重跑。PydanticAI 提供类型化验证和 Deferred Tool。OpenAI Agents SDK 提供内建 Trace，但不能作为 Brain Audit。AutoGen 生态仍在演进。MCP 是工具协议，不是身份授权或规范 Memory 协议。

技术层候选包括 Rust/Tokio、Provider 原生 SDK、vLLM/llama.cpp/Ollama 本地推理、H 所有的 BMCP、按需使用 MCP、JSON Schema/Serde、显式 Attempt State Machine、Provider 原生 Streaming、OpenTelemetry 和脱敏日志。除既有项目语言方向外，不应仅凭本报告将任何技术升级为正式决策。

DECIDED：Agent/Model/Provider 是不同角色。CANDIDATE：模块化 Integration Layer、Capability Registry 和 Provider 专属 Adapter。TO_VALIDATE：Rust SDK、Streaming、Cancellation、本地推理、遥测开销。DEFERRED：分布式 Gateway、Broker、多 Agent Brain Orchestration。REJECTED：单一 Success 枚举、Framework 拥有 Canonical Memory、超时盲目重试、将 OpenAI-Compatible 当成完全等价。
