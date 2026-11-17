# PRODUCT-FIRST-001 — Session 05
# Agent Runtime & Integration Product Adoption Research
# Agent Runtime 与集成产品采用性研究

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Research branch: `research/product-first-001-session-05-agent-runtime`
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Date: 2026-11-18
- Status: **DRAFT RESEARCH / NOT AN ADR / NO PRODUCT APPROVED**
- Relationship: **Supplement to C Owner research; does not amend C-owned contracts**
- Language: English and Chinese in this file

---

## 0. Executive conclusion / 执行结论

**Recommendation: adopt mature Agent Runtime capabilities through a replaceable Integration Adapter; do not make any external runtime the Brain runtime or Canonical Memory authority.**

The project should not build a general-purpose Agent framework, planner, tool loop, multi-agent scheduler, or model-provider SDK from scratch. Those are execution concerns and have mature implementations. The Brain should build only the narrow integration boundary it uniquely needs: authenticated Brain API client, capability negotiation, Context delivery/application evidence integration, typed event submission, and provider/tool evidence mapping where required by C/H contracts.

Recommended adoption posture:

1. **LangGraph — conditional runtime candidate**, especially for Python-based workflow/long-running Agent experiments. Reuse its graph orchestration, checkpointing, streaming and human-interrupt patterns. Do not delegate Brain lifecycle, Forget, authorization, Applied, or Canonical Memory to its checkpointer/store.
2. **Hermes Agent — reference product and optional external Agent**, not a Brain dependency. Study its practical tool registry, provider resolution, session persistence, profiles, gateway, plugin and subagent patterns. Its bundled memory/session model is not the Brain's canonical store.
3. **Letta — reference/optional Agent product**, not a canonical memory backend. Its stateful-agent identity, conversation history, memory blocks/MemFS and App Server are useful product patterns, but its agent-owned persistent memory creates a second authority if treated as Brain truth.
4. **MCP — adopt at the tool ecosystem edge** for connecting MCP servers/tools where useful. MCP is not a replacement for BMCP, C's inference contract, I authorization, or Brain Memory semantics.
5. **BMCP — retain as the Brain-owned protocol boundary under H ownership.** Reuse MCP SDKs/transports/tool ecosystem selectively; do not rename MCP as BMCP or silently replace BMCP envelopes, Context/Applied semantics, ACKs, or governance.
6. **One runtime adapter first.** Keep provider adapters separate from Agent runtime adapters. Do not maintain LangGraph + Hermes + Letta runtime adapters in the first vertical slice.
7. **Inference and Agent execution should be separable from Brain core**, initially by in-process modules or a process boundary, not by prematurely deploying a distributed gateway/microservice fleet.

This is a product-adoption recommendation, not a technology selection, architecture freeze, implementation authorization, or amendment to C/H/I/D/G/Storage contracts.

**中文结论：采用成熟 Agent Runtime 的执行能力，通过可替换 Integration Adapter 接入；任何外部 Runtime 都不能成为 Brain Runtime 或 Canonical Memory Authority。**

项目不应从零构建通用 Agent Framework、Planner、Tool Loop、多 Agent Scheduler 或 Model Provider SDK。上述属于执行层能力，已有成熟实现。Brain 只应构建自身不可替代的窄集成边界：经过认证的 Brain API Client、Capability Negotiation、Context Delivery/Applied Evidence 集成、Typed Event Submission，以及 C/H 契约要求的 Provider/Tool Evidence 映射。

建议：LangGraph 作为有条件的 Runtime 候选；Hermes 作为产品参考或可选外部 Agent；Letta 作为 Stateful Agent 产品参考而非 Canonical Memory 后端；MCP 用于 Tool 生态接入；BMCP 继续作为 H Owner 管理的 Brain 协议。首个垂直切片只维护一种 Agent Runtime Adapter。推理与 Agent 执行应从 Brain Core 解耦，但初期优先模块化或进程隔离，不急于拆分微服务。

---

## 1. Current Baseline / 当前基线

### 1.1 Exact repository baseline

| Item | Verified value | Status |
|---|---|---|
| Default branch | `main` | VERIFIED |
| Main HEAD | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | VERIFIED from C baseline and PR #73 remediation base |
| Repository mission | Independent, model-agnostic Memory Brain | VERIFIED from main README |
| Implementation status | Not started by design | VERIFIED from main README |
| Brain boundary | Brain owns memory assets/lifecycle/retrieval/activation/context authority; Agent owns reasoning and acting | VERIFIED from main README |
| C current research | PR #69, Draft/Open, branch `research/tech-reality-001-c`, head `1a1d6f26a793fc285a1806edf21b696f748a8fed` | VERIFIED |
| C contract status | C-owned semantic requirements proposed; not cross-owner wire-frozen | VERIFIED from C contract |
| H protocol status | H owns BMCP schema/wire/ACK and Adapter protocol | VERIFIED from C contract and main integration docs |
| Adapter tiers | Tier intent DECIDED; conformance details CANDIDATE | VERIFIED from main |
| Main implementation | No production Brain Runtime implementation established by these sources | VERIFIED AS DOCUMENTED NON-CLAIM |

### 1.2 Sources read from the repository

**Main branch source pins:**

- `README.md` Blob `429e873bd5bf081e10a449b27e3495428e1046f1`.
- `07-agent-integration/agent-integration-overview.md` Blob `073ff4ddf71fbcaf959107bb06ab724bfa48e63b`.
- `07-agent-integration/inference-boundary-model.md` Blob `e2d5cb6abd9ec40da6e3680531de5944fc8b14df`.
- `07-agent-integration/adapter-capability-tiers.md` Blob `09c5932350c48f950ee16f6b246f54e661f0c420`.
- `07-agent-integration/telemetry-model.md` Blob `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0`.

**C Owner research branch (PR #69; not merged):**

- `agent-integration-canonical-contract.md` Blob `eaf8c2d3d4449a5fefe78498a8a22d2764796059`.
- `agent-integration-technology-assessment.md` Blob `519ab338481ecc2d1b932ee8040e30da6cb65484`.
- `agent-integration-telemetry.md` Blob `3c69cb2d1c72490d574d8944ec5b05868fa54177`.
- `inference-boundary-and-trust-model.md` was read from the exact C research branch.
- `tool-execution-boundary.md` Blob `9a8688f0c81abb4b8e51efc9d094b96628915a4b`.
- `existing-integration-baseline.md` Blob `56ed1c7e5280a0dc911a3c3741632daeef649cb6`.

**Protocol evidence boundary:** the current main README maps `08-protocols/` to BMCP specifications. C's contract explicitly assigns BMCP schema/wire/ACK to H. C's baseline records H branch `session-h-bmcp-protocol`, HEAD `0d36324457e39bd50ad56ae902d477c4ea765b61`, Unified 1.2.15 schema Blob `860fc4cec658db7d2703cd6adf72aa31a2723f6d`, and mapping Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924`. These are separate-branch snapshots, not main-merged protocol adoption. This Session 05 report does not modify or re-specify them.

### 1.3 Related PR status / 相关 PR

| PR | Purpose | Verified state | Relevance to Session 05 |
|---|---|---|---|
| #45 | A technology reality research | Open/Draft; historical base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`; head `6c7c5919c1b50f38c4d24be679a3885ee3c15b97` | Contains broad runtime/product research; not current-main authority |
| #56 | Independent review of #45 | Open/Draft; verdict REVISE; feasibility NOT YET PROVEN | Three P1 blockers and P2 corrections remain; review does not approve a runtime |
| #73 | Current-source remediation of #45 | Open/Draft; based on current main `b3c666e...`; role-simulated remediation | Explicitly says no real Owner approval, implementation/conformance, or independent review |
| #69 | C Agent integration/inference research | Open/Draft; base `b3c666e...`; head `1a1d6f26a793fc285a1806edf21b696f748a8fed` | C-owned boundaries and product assessments; this report supplements, not overrides |

PR #69 records: C0 PARTIAL; C5 BLOCKED/PARTIAL; C6 validation plan ready but C end-to-end tests NOT RUN; independent review pending. It recommends a modular Integration Layer with capability registry and provider-specific adapters, not a lossy single Provider interface or premature distributed gateway.

PR #56's REVISE finding on #45 remains relevant: historical research currentness and exact Owner-source reconciliation matter; a research report or mergeability flag does not establish architecture acceptance. PR #73 is a role-simulated remediation, not a substitute for Owner approvals.

**中文基线说明：** 本次以 main 的精确 HEAD `b3c666e...` 为仓库基线。C 的完整集成研究位于 PR #69 的独立 Draft 分支，不是 main 已合并规范。PR #45 是历史技术研究，PR #56 对其给出 REVISE，PR #73 是角色模拟的当前源整改，均不能被解释为技术批准。Session 05 只补充产品采用性，不覆盖 C 的职责边界。

---

## 2. Product Landscape / 产品生态

### 2.1 LangGraph

**What it provides:** a low-level Python orchestration framework/runtime for long-running stateful agents, graph-defined state/control flow, checkpoints, thread persistence, streaming, interrupts and human-in-the-loop. Checkpointers preserve per-thread graph state; Stores persist application-defined data across threads. Checkpointing supports recovery and replay, but replayed graph code and external side effects still require idempotency discipline.

**Adoption value:** high for a Python Agent/workflow spike or optional external runtime. It can remove the need to hand-build a graph executor, state machine, checkpoint persistence and HITL pause/resume.

**Boundary risks:** its graph state/checkpointer is execution state, not Brain Canonical Memory. Its Store must not silently become the Brain's long-term truth store. Node replay must not repeat non-idempotent tools or Brain writes. The project baseline is Rust-oriented; LangGraph introduces a Python runtime/process and operational dependency if embedded in the core.

**Disposition:** CONDITIONAL ADOPT for a separately hosted Agent Runtime experiment; NOT a Brain core dependency in the first vertical slice.

### 2.2 Hermes Agent

**What it provides:** a complete practical Agent product with an agent loop, provider resolver, central tool registry, toolsets/plugins, SQLite session/state persistence, context assembly/compression, MCP client, multiple execution backends, gateway/platform adapters, cron and subagent delegation. The official architecture describes one Agent facade serving CLI, gateway, ACP, batch and API entry points, with optional subsystems loosely coupled.

**Adoption value:** very high as a product-level reference and potential user-facing Agent. It demonstrates how an actual runtime packages the tool loop, provider switching, profiles, sessions, tools, gateway and skills without requiring the Brain to own these features.

**Boundary risks:** Hermes' own session history, memory/context engine and memory-provider plugin can form a separate persistence authority. Built-in tools can have broad machine access; they must not inherit Brain authorization. Its runtime is Python, and its product scope is broader than the Brain integration contract.

**Disposition:** REFERENCE / OPTIONAL EXTERNAL AGENT. Do not embed Hermes as Brain core. If integrated, treat it like any other untrusted Agent Host behind a capability-limited adapter.

### 2.3 Letta Agent Runtime

**What it provides:** persistent stateful Agent identities, model/tool configuration, conversations, message history, memory blocks/MemFS, local and hosted execution, App Server and Agent SDK. Its current documentation distinguishes agents from conversations and supports local or self-hosted runtime deployment.

**Adoption value:** high for understanding persistent Agent identity, cross-conversation state, agent lifecycle, SDK/App Server, and how an Agent product exposes streaming and approvals.

**Boundary risks:** Letta's product concept intentionally makes memory part of the stateful Agent identity. That is not the same as a shared, cross-Agent, Brain-governed Canonical Memory. If both Letta memory and Brain memory are writable truths, users and Agents will see divergent facts, Forget behavior and provenance. A Letta Memory provider is not automatically an authoritative Brain adapter.

**Disposition:** REFERENCE / OPTIONAL EXTERNAL AGENT. Use only with Brain memory integration explicitly configured as a controlled external source/consumer; disable or isolate overlapping memory authority for any conformance experiment.

### 2.4 MCP ecosystem

**What it provides:** an interoperable Host/Client/Server protocol and ecosystem for tools and other context capabilities. The 2025-11-25 specification uses JSON-RPC and supports stdio and Streamable HTTP transports; it has capability negotiation and HTTP authorization guidance. MCP servers expose tools/resources/prompts; client and server SDKs reduce bespoke integration work.

**Adoption value:** high for tool discovery and invocation interoperability. Prefer existing MCP servers and maintained SDKs over inventing a parallel tool plugin protocol where MCP semantics fit.

**Boundary risks:** MCP does not decide the Brain's Principal, scope, policy grants, tool sandbox, canonical memory state, ContextVersion, Applied, Forget, or Provider outcome. Tool metadata from remote servers is untrusted. A tool call may execute arbitrary code or external side effects. MCP transport authentication is not a substitute for I authorization at the Brain boundary.

**Disposition:** ADOPT SELECTIVELY at the Tool ecosystem edge, with an I-governed authorization and sandbox wrapper.

### 2.5 BMCP

BMCP is the Brain's protocol boundary, with schema/wire/ACK and Adapter protocol owned by H. It carries Brain-specific semantics that MCP does not provide: Brain-scoped identity and permissions, typed telemetry, Context delivery/versioning, receipt/acceptance/application distinctions, and Brain protocol lifecycle.

**Disposition:** KEEP BMCP. Reuse MCP transports, SDK patterns, JSON-RPC libraries or MCP servers only through explicit adapters where semantics map without loss. Do not make MCP a wire-compatible substitute by assumption. Do not allow a product Runtime to define or modify BMCP semantics.

### 2.6 Other useful candidates

- **PydanticAI:** typed Agent/tool interfaces, dependency injection and validation; useful for small Python adapter prototypes, not a new canonical runtime commitment.
- **OpenAI Agents SDK:** useful reference for tools, handoffs, sessions, MCP and tracing; provider/product-specific option, not the Brain's provider-neutral core.
- **AutoGen / Microsoft Agent Framework:** evolving ecosystem; keep under observation, not a first-slice dependency.
- **Temporal / Restate / DBOS:** durable execution products are relevant for workflow reliability but belong to the durable execution decision (not an automatic Agent Runtime choice). Their state machines cannot replace Brain D/I/Storage invariants.

**中文产品观察：** LangGraph 最强在图式编排、Checkpoint、恢复与人工介入；Hermes 最强在完整 Agent 产品工程化，包括工具注册、Provider、Session、Gateway、Skills 和子 Agent；Letta 最强在持久化 Agent Identity 与 Agent 自身 Memory；MCP 最强在工具生态互操作。四者不是同一类产品，也不能互相替换。BMCP 与 MCP 的目标边界不同，应该通过 Adapter 协作而不是合并概念。

---

## 3. Runtime Capability Matrix / Runtime 能力矩阵

Legend: **N** native capability; **A** adapter/integration required; **P** partial or product-dependent; **—** not the product's primary responsibility. Ratings are qualitative desk research, not conformance test results.

| Capability | LangGraph | Hermes Agent | Letta Runtime | MCP ecosystem | Brain requirement |
|---|---:|---:|---:|---:|---|
| Agent execution loop | N | N | N | — | External Runtime |
| Graph/workflow orchestration | N | P | P | — | Runtime choice |
| Agent state/checkpoint | N | N (SQLite sessions) | N (persistent agent state) | — | Runtime-owned, noncanonical |
| Tool registry/dispatch | A/P | N | N | N protocol surface | Runtime + MCP adapter |
| Tool authorization | A | P (product controls) | P (server/tool controls) | A (host policy) | I owns policy; host enforces |
| Tool sandbox/isolation | A | N/P (multiple backends) | P (server/client tool modes) | — | Separate Tool Host boundary |
| Agent protocol | A | P (ACP/product gateway) | P (App Server protocol/SDK) | N (MCP) | H owns BMCP |
| Context injection | A | N (prompt builder) | N (memory blocks) | — | Adapter at inference boundary |
| Brain Memory Adapter | A | A/plugin | A | A | Brain-owned API adapter |
| Model Provider Adapter | N/P | N | N | — | Provider-specific adapter |
| Multi-agent coordination | N | N (subagents) | P | — | Defer from Brain core |
| Session management | N | N | N | — | Runtime session ≠ Brain scope |
| Streaming | N | N | N | P (transport events) | Adapter normalizes evidence |
| Tracing | A/N via ecosystem | P | P | P | OTel correlation; I audit separate |
| Human approval | N | N | P/N by product | P (elicitation not policy) | I policy + explicit approval |
| Durable execution | N (checkpoints) | P (jobs/session recovery) | P (server/runtime state) | — | Must test side effects/recovery |
| Runtime isolation | A (deployment) | N/P (execution backends) | P (local/server separation) | A (host process/container) | Explicit process/tool isolation |

Important: a native feature is not automatically a Brain-conformant feature. A Runtime's checkpoint, memory, approval, identity, trace or tool registry must never be equated with Brain-owned proof.

### 3.1 Capability ownership interpretation

- **Agent Execution / Agent State:** Runtime-owned. Runtime state can be disposable/rebuilt or persisted according to the Runtime's needs, but it is not Canonical Memory.
- **Tool Execution:** Tool Host executes; Agent proposes; I authorizes; C records integration evidence; D/Storage remain the only route for Canonical Memory changes.
- **Tool Registry:** Runtime/MCP can discover and describe tools. A registry entry is not an authorization grant.
- **Context Injection:** Adapter applies Brain-managed data at the actual inference assembly boundary. Runtime prompt builders can host the hook, but cannot invent Applied evidence.
- **Model Provider Adapter:** Provider-specific capabilities and raw metadata must be preserved; a normalized facade must not erase semantic differences.
- **Session:** Runtime conversation/run identity is not Principal, Tenant, Scope, Brain Context, or Canonical Memory identity.
- **Tracing:** trace correlation is observability, not I audit evidence or C Provider Outcome proof.
- **Durable execution:** checkpoint/replay is useful, but it does not guarantee exactly-once external side effects or Brain transaction correctness.

**中文矩阵解释：** 产品原生具备某项能力，不代表该能力满足 Brain 的规范语义。Runtime Checkpoint 不是 Canonical Memory；Tool Registry 不是授权；MCP Server 声明不是权限；Runtime Approval 不自动等于 I 授权；Trace 不是 Audit；Context 注入不自动等于 G Applied；Checkpoint Replay 也不等于外部副作用 Exactly-Once。

---

## 4. Protocol / SDK Adoption / 协议与 SDK 采用

### 4.1 MCP adoption boundary

Adopt MCP for:
- connecting existing third-party tools and MCP servers;
- discovering tool definitions and schemas;
- standard request/response and streaming transport where supported;
- reducing bespoke connectors for external tool ecosystems.

Do not use MCP as:
- Brain canonical memory API or event schema;
- replacement for BMCP Context delivery/ACK/application semantics;
- authorization policy engine or Principal authority;
- a guarantee that tool execution is sandboxed, safe, idempotent or reversible;
- Provider inference lifecycle or CSubmitOutcome.

### 4.2 BMCP remains normative for Brain integration

H owns BMCP wire/schema/ACK and Adapter protocol. Any bridge must explicitly map:

1. authenticated Adapter identity and negotiated capabilities;
2. Brain scope and authorized operations;
3. telemetry schema/version and idempotency;
4. Context delivery identity, version, validity and reconciliation;
5. Received / Accepted / Applied / Rejected / Superseded distinctions;
6. acknowledgements and retry/replay behavior;
7. Forget/revocation and stale-reference rejection;
8. evidence references and trace correlation.

A bridge must reject lossy mapping. If MCP cannot express a Brain-specific guarantee, that guarantee stays in BMCP or a Brain API operation; do not silently drop it.

### 4.3 SDK strategy

- Prefer maintained official MCP SDKs for supported languages/transports; pin versions and test the exact feature subset used.
- Implement a small internal `BrainClient` port independent of LangGraph/Hermes/Letta SDK types.
- Implement one `AgentRuntimeAdapter` first and one `McpToolHostAdapter` only if MCP tools are in the first product slice.
- Keep `ProviderAdapter` separate from `AgentRuntimeAdapter`; Provider SDKs are not Agent frameworks.
- Preserve native provider fields and streaming event types behind typed extension payloads.
- Do not import an entire framework's memory abstractions into Brain domain crates.

**中文协议建议：** MCP 只作为外部 Tool 生态入口，BMCP 继续承担 Brain 专属协议。所有桥接都必须显式映射身份、Scope、授权、Telemetry、Context Version、ACK、Applied、Forget 和 Evidence。不能无损表达的语义不得丢弃。内部只定义稳定的 BrainClient 与 AgentRuntimeAdapter 接口，避免业务层依赖 LangGraph/Hermes/Letta 的类型。

---

## 5. Agent / Brain Boundary / Agent 与 Brain 边界

### 5.1 Recommended logical architecture

```text
User / Product / External Agent
             |
             v
      Agent Runtime (replaceable)
   LangGraph / Hermes / Letta / custom
             |
             +---- Provider Adapter ----> Model Provider / Local Inference
             |
             +---- Tool Host / MCP Client ----> MCP Servers / Sandboxed Tools
             |
             v
     Agent Runtime Adapter
  - authenticated adapter identity
  - capability negotiation
  - session/task/telemetry mapping
  - Brain Context delivery integration
  - evidence and correlation mapping
             |
             | BMCP (H-owned) / Brain API
             v
       Memory Brain Boundary
  - I: principal / authorization / scope / trust
  - D: canonical lifecycle / Forget
  - E: derived-memory production
  - F: retrieval / activation
  - G: ContextVersion / Applied authority
  - H: protocol / schema / ACK
  - Storage: durable commit / visibility
             |
             v
       Canonical Memory Authority
```

### 5.2 Dependency direction

Allowed:
- Runtime Adapter depends on BrainClient contract.
- Brain integration boundary knows protocol contracts, not LangGraph/Hermes/Letta internal classes.
- Runtime can call Brain APIs and receive authorized data.
- Brain may deliver context/evidence requests to a registered Adapter through H-owned protocol.

Forbidden:
- Brain domain/core importing or depending on a concrete Agent Runtime.
- Runtime writing Canonical Memory tables or lifecycle state.
- Runtime checkpointer being treated as a Brain replica or recovery authority.
- Brain using Runtime tool registry as its own authorization registry.
- Runtime payload identity being accepted as authenticated Principal.
- Runtime claiming Applied, Forget, Canonical Commit or authorization outcomes.

### 5.3 Preventing circular dependency

Use ports and adapters with a one-way dependency rule:

1. Brain domain contracts define Brain-facing operations and typed results.
2. Integration layer implements the BrainClient-facing endpoint/port.
3. Runtime Adapter maps runtime-native objects to the stable contract.
4. Concrete Runtime packages depend on the Adapter port, never the reverse.
5. Contract tests run against a fake Runtime and a fake Brain endpoint before any real framework is integrated.

The Brain must remain usable by a CLI, custom Agent, external service or future Runtime without importing the selected framework.

### 5.4 Memory authority isolation

External Runtime state is explicitly classified as one of:
- **Execution State:** graph nodes, checkpoints, tool call state, retries, run metadata.
- **Conversation State:** messages and session history owned by the Runtime/product.
- **Candidate Memory Input:** a source-qualified proposal submitted to Brain.
- **Canonical Memory:** Brain-only authority, changed only through authorized Brain operations.
- **Context Projection:** a versioned Brain-managed view materialized by Adapter at an inference boundary.

No implicit promotion between these categories is allowed. A Runtime's learned summary or memory block is a candidate/source, not Canonical Memory. Brain Memory returned to an Agent is data, not an instruction channel.

**中文架构边界：** 外部 Runtime 只负责执行、会话、工具编排和自身恢复状态。Brain 通过稳定的 API/BMCP 与 Runtime 通信。依赖方向只能是 Runtime Adapter 调用 Brain 接口，不能让 Brain Core 反向依赖具体 Agent Framework。外部 Runtime 的 Memory、摘要、Checkpoint 都只能属于执行/会话状态或候选来源，不能自动升级为 Canonical Memory。

---

## 6. Security and Data Authority / 安全与数据权威

| Concern | Authority | Runtime's permitted role | Prohibited interpretation |
|---|---|---|---|
| Principal identity | I (typed by B) | Present authenticated credentials/context | Agent ID is not Principal |
| Scope/tenant | I/B | Carry references and requested scope | Runtime session is not scope |
| Tool permission | I | Request capability; host enforces grant | Tool manifest is not a grant |
| Tool sandbox | Tool Host / deployment | Execute within bounded environment | MCP does not sandbox by itself |
| Canonical Memory | D/Brain + Storage | Submit candidate/source refs | No direct writes |
| Derived memory | E under Brain governance | Submit observations | Runtime summary is not validated truth |
| Retrieval/activation | F | Request/consume scoped results | Runtime cache is not authoritative |
| Context version | G | Apply managed region at boundary | Checkpoint version is not ContextVersion |
| Applied evidence | G, with H/C boundary evidence | Emit truthful adapter evidence | Receipt/queue/cache ≠ Applied |
| BMCP wire/ACK | H | Implement compatible client/adapter | Runtime may not redefine wire |
| Provider handoff evidence | C | Supply raw/provider-specific observations | HTTP success ≠ inference complete |
| Forget/revocation | D/I/Storage per owned contracts | Purge local copies/caches and reject stale refs | Runtime deletion ≠ Brain Forget proof |
| Audit/privacy | I | Emit minimized diagnostics | OTel trace ≠ immutable audit |

Mandatory controls:
- authenticated adapter registration and version-bound capabilities;
- least-privilege scopes per Agent, Runtime, Tool, Model and environment;
- per-tool authorization at invocation time, not only at tool discovery;
- process/container isolation for arbitrary code and MCP servers;
- explicit approval for consequential external side effects;
- stable operation/idempotency keys and reconciliation after ambiguous outcomes;
- no secrets, full prompts, raw memory or tool arguments in default telemetry;
- revocation/Forget propagation to local Runtime caches, vector stores, checkpoints and conversation projections according to I/D policy;
- stale Context/Memory reference rejection after revocation or Forget;
- no trust elevation from model self-report, tool metadata or runtime-generated summaries.

**中文安全要求：** Runtime、Agent、Tool、Provider、Session 的标识不能代替 I 认证主体。Tool 能力清单不是授权。发现 Tool 后仍须在调用时检查权限。任意代码和 MCP Server 应在受限进程/容器运行。Forget 和撤权必须覆盖外部缓存、Checkpoint、Memory Projection；但 Runtime 清理本地副本不等于 Brain Forget 已完成。普通 Trace/Log 不能代替 I 审计证据。

---

## 7. Complexity Reduction / 复杂度削减

### 7.1 Build only what is unique

Do not build in Brain:
- general Agent loop/planner/reasoner;
- generic graph/workflow editor;
- generic tool marketplace/registry;
- multi-agent delegation scheduler;
- model vendor SDKs and streaming protocol parsers;
- Agent conversation history store;
- generic HITL UI or gateway;
- another long-term agent memory store.

Build or own narrowly:
- BrainClient and protocol boundary;
- Agent Runtime Adapter port;
- capability/adapter registration and conformance;
- mapping from runtime events to canonical telemetry;
- Context delivery and exact inference-boundary application evidence;
- security checks and Brain-owned data lifecycle.

### 7.2 One adapter first

First vertical slice:
1. one Runtime selected for the first target product/use case;
2. one AgentRuntimeAdapter;
3. one ProviderAdapter path (not one per runtime);
4. one BrainClient;
5. optionally one MCP client/Tool Host if a real first-slice tool requires it;
6. Tier 3 (telemetry + Active Recall) first if inference boundary control is unavailable;
7. upgrade to Tier 2/1 only after boundary coverage and Applied conformance pass.

Do not implement adapters for all frameworks pre-emptively. Add a second runtime only when there is a real deployment/customer requirement, a distinct capability, or an independently validated migration path.

### 7.3 Avoid false unification

Use a common minimum contract plus capability-specific extension points. Do not flatten:
- Provider Handoff vs model execution vs response receipt;
- Tool invocation vs side effect vs compensation;
- Runtime Session vs Brain Scope vs Principal;
- Context Delivered vs Received vs Accepted vs Applied;
- Runtime checkpoint vs Canonical Memory;
- Trace correlation vs audit evidence.

### 7.4 Deployment simplicity

Start as a modular Integration Layer in the selected application deployment. Isolate arbitrary tools and optionally isolate inference in worker processes. Do not require Kubernetes, a centralized Agent Gateway, a broker, or distributed multi-agent control plane for the first vertical slice. Extract services only when measured isolation, throughput, independent scaling, availability or security needs justify the cost.

**中文复杂度建议：** Brain 不需要重复开发通用 Agent Loop、Planner、Workflow Editor、Tool Marketplace、Multi-Agent Scheduler、Provider SDK、会话历史库或通用 HITL UI。只建设 Brain 独有的协议、适配、权限、Context Applied Evidence 和 Memory Authority。第一阶段只接一种 Runtime，优先 Tier 3，再按真实能力升级。不要为了“兼容生态”提前维护多个 Runtime Adapter。

---

## 8. Adoption Matrix / 采用决策矩阵

| Product / technology | Decision | Scope | Gate / condition |
|---|---|---|---|
| LangGraph | CONDITIONAL ADOPT | Optional external Agent/workflow runtime | Python boundary, replay/idempotency tests, Brain memory disabled as authority |
| Hermes Agent | REFERENCE / OPTIONAL | Product reference or external Agent | Treat as untrusted host; isolate tools and its own memory |
| Letta Runtime | REFERENCE / OPTIONAL | Stateful Agent product reference | No dual canonical memory; explicit memory bridge and Forget behavior |
| MCP SDK/ecosystem | ADOPT SELECTIVELY | Tool discovery/invocation edge | I authorization, sandbox, server trust and conformance |
| BMCP | KEEP / H-OWNED | Brain integration protocol | No Session 05 wire/schema changes |
| PydanticAI | SPIKE ONLY | Small typed Agent client experiments | Do not introduce second runtime abstraction without need |
| OpenAI Agents SDK | REFERENCE / OPTIONAL | Provider/product-specific runtime | Keep Brain contracts vendor-neutral |
| AutoGen / Microsoft Agent Framework | WATCH | Future candidate | Reassess maturity, migration and license before use |
| Multiple Runtime Adapters | DEFER | Future portability | Add only with demonstrated requirement |
| Brain-owned Agent Runtime | REJECT AS CURRENT SCOPE | None | Brain remains Memory Brain, not Agent framework |
| Brain-owned general Tool Registry | REJECT AS DUPLICATE | Brain only stores authorization/capability references needed by its contract | I and Runtime/Tool Host retain their authority |
| Separate inference worker | CONDITIONAL | Process isolation and resource control | Introduce when model lifecycle/resource contention warrants it |

Decision vocabulary:
- **ADOPT SELECTIVELY:** reuse a bounded ecosystem capability behind an adapter.
- **CONDITIONAL ADOPT:** candidate for a real prototype, no production selection yet.
- **REFERENCE:** learn from product architecture; no runtime dependency.
- **DEFER:** not needed in the first vertical slice.
- **REJECT AS CURRENT SCOPE:** violates project boundary or creates duplicate authority.

**中文采用矩阵：** 当前真正值得直接采用的是 MCP 工具生态的互操作能力；LangGraph 适合条件性 Runtime Spike；Hermes 和 Letta 更适合作为产品级参考或外部 Agent。BMCP 保留。多 Runtime Adapter、Brain 自研 Agent Runtime 和通用 Tool Registry 均不应进入首个最小集。

---

## 9. Recommended Integration Architecture / 推荐集成架构

### 9.1 Minimum viable sequence

**Phase 0 — Contract alignment (no runtime commitment)**
- Pin current main and exact C/H/I/D/G/Storage contracts.
- Confirm which BMCP/Adapter contract is normative and which branch artifacts remain candidates.
- Define one minimal BrainClient contract without importing framework types.
- Record which adapter tier is actually achievable.

**Phase 1 — First runnable slice**
- Select one Agent Runtime based on the first target workload; if the project needs a Python graph workflow, run a bounded LangGraph spike. If the goal is a ready-to-use Agent product, test Hermes as an external Agent rather than embedding it. Do not start with both.
- Implement one Runtime Adapter and a BrainClient.
- Use Tier 3: authenticated telemetry ingress and scoped Active Recall.
- No proactive Context Applied claim yet.
- Use MCP only for a concrete required tool, with I authorization and isolated Tool Host.
- Keep Runtime state in its own namespace/database; Brain owns canonical memory.

**Phase 2 — Inference boundary**
- Add controlled context injection only where the Adapter can inspect the actual final request assembly.
- Implement snapshot/delta reconciliation, capability downgrade, stale reference rejection and exact per-request application evidence.
- Pass Tier 2 or Tier 1 conformance before advertising those guarantees.
- Keep C final-request evidence and G Applied decision separate.

**Phase 3 — Reliability and optional portability**
- Add durable workflow/checkpointing only if real long-running jobs or human approvals require it.
- Test replay around every side-effect boundary; external calls must be idempotent or reconciled.
- Add a second Runtime Adapter only after a concrete need and conformance suite exist.
- Consider isolated inference worker when GPU/CPU resource contention or fault isolation requires it.

### 9.2 Runtime selection heuristic

- Need explicit graph control, pause/resume, replay and HITL: prototype LangGraph.
- Need a ready-to-use personal/coding Agent, multi-platform gateway, skills and tools: evaluate Hermes as a standalone Agent product.
- Need persistent Agent identity and Agent-owned evolving memory as a product feature: evaluate Letta, but keep its memory separate from Brain Canonical Memory.
- Need only tool interoperability: MCP SDK/server; no need to adopt a whole Agent Runtime.
- Need a Brain Memory API: use BrainClient/BMCP, not an Agent framework's memory API.

### 9.3 Runtime isolation profile

The initial integration should support:
- separate process identity for Runtime and Brain where practical;
- authenticated, versioned adapter connection;
- scoped capability tokens with short validity and revocation;
- bounded request/response sizes and timeouts;
- no shared database credentials;
- no Runtime filesystem access to Brain storage;
- explicit network egress allowlists for Tool Host;
- independent Runtime state retention and purge policy;
- replay/reconciliation tests for lost ACK, crash and duplicate event.

**中文推荐架构：** 先完成契约对齐，再选一种 Runtime 做最小可运行切片。第一阶段只实现认证 Telemetry + Scoped Active Recall（Tier 3），不声称主动 Context Applied。随后在可观测的推理请求组装边界上实现 Context Injection，经过 Tier 2/1 符合性测试后再升级。长任务、人工审批或故障恢复确实需要时再引入 Durable Runtime。第二种 Runtime 必须由真实需求触发。

---

## 10. Acceptance Criteria / 验收标准

A product/runtime adoption is not accepted merely because a demo works. All applicable criteria below require recorded evidence.

### A. Architecture and authority
1. Brain core has no dependency on LangGraph, Hermes, Letta or any concrete Agent Runtime.
2. Runtime Adapter communicates only through stable BrainClient/BMCP contracts.
3. Runtime state, conversation state, Candidate Memory Input, Canonical Memory and Context Projection are separately typed/stored.
4. No Runtime can directly write Canonical Memory or lifecycle tables.
5. C/D/E/F/G/H/I/Storage ownership is preserved; this document changes none of their contracts.

### B. Identity, authorization and tools
6. Adapter identity is authenticated and bound to version/capability registration.
7. Principal, Tenant, Scope, Agent, Runtime, Session, Request, Attempt, Operation and Trace IDs are not conflated.
8. I authorization is enforced at each protected operation and tool invocation.
9. MCP server/tool metadata is treated as untrusted input.
10. Arbitrary tools execute in a constrained Tool Host with explicit network/filesystem/secret limits.
11. Ambiguous tool side effects are reconciled; no blind retry of non-idempotent operations.

### C. Memory, Context and Forget
12. Runtime checkpoints and memory blocks cannot be interpreted as Canonical Memory.
13. Brain Memory returned to Runtime is data, not instruction authority.
14. Candidate submissions preserve source/provenance and are revalidated by Brain.
15. Context Received, Accepted and Applied remain distinct.
16. Applied is emitted only at the actual managed-region inference assembly boundary, with request correlation and exact version.
17. Forget/revocation invalidates stale references and is propagated to Runtime caches/projections under I/D policy.
18. Runtime-local deletion is never reported as Brain Forget completion.

### D. Reliability and observability
19. Checkpoint replay cannot duplicate external side effects or Brain writes.
20. Provider handoff, execution completion, response receipt, Tool side effects, Brain commit and G Applied remain separate evidence.
21. OTel traces and logs are redacted, low-cardinality and not treated as audit proof.
22. Lost ACK, duplicate delivery, process crash, timeout and stale capability tests pass.
23. Runtime and Brain can restart independently without shared hidden state.

### E. Product adoption and operations
24. The chosen Runtime has pinned version, license, deployment model, upgrade/rollback and security review.
25. Adapter capability claims pass the relevant Tier 1/2/3 conformance suite.
26. No second Runtime adapter is added without a documented requirement and incremental maintenance budget.
27. Benchmarks measure end-to-end latency, recovery behavior, tool isolation overhead, resource use and context application correctness on the target deployment.
28. Open issues and non-passing criteria remain visible; no product adoption status is upgraded from CANDIDATE based on a demo.

**Current status:** all implementation/conformance criteria are **NOT RUN** by this research. This report is desk research plus repository source readback. It does not claim a working Runtime integration, Brain prototype, security audit, benchmark, end-to-end Applied proof or production readiness.

### 10.1 Open questions and closure conditions

| ID | Open question | Closure evidence | Owner |
|---|---|---|---|
| PF05-01 | Which first Runtime matches the first real product workload? | Explicit workload and one bounded spike comparison | A + product owner |
| PF05-02 | Which BMCP version/Adapter contract is normative today? | H exact branch/manifest and Owner disposition | H |
| PF05-03 | What exact identity and capability token binds Runtime Adapter? | Approved principal/delegation/scope contract | I + B + H |
| PF05-04 | Which Context tier can the selected Runtime actually satisfy? | Per-request boundary coverage and conformance tests | C + G + H |
| PF05-05 | How are external Runtime caches purged on Forget/revocation? | D/I policy and fault-injection evidence | D + I + Runtime owner |
| PF05-06 | Is MCP needed in the first vertical slice? | Concrete tool requirement and threat model | C + I |
| PF05-07 | Does the Python Runtime boundary fit the deployment model? | Process isolation, latency and operational spike | A + C |
| PF05-08 | Are multiple Agent adapters worth maintaining? | Second real workload and measured benefit | A + C |

### 10.2 Final disposition

**CONDITIONAL PRODUCT ADOPTION DIRECTION — NOT APPROVED FOR PRODUCTION.**

The architecture should reuse Agent Runtime and Tool ecosystem products while keeping Brain-specific authority and proof semantics in Brain-owned contracts. The smallest sensible first step is one Runtime Adapter, one BrainClient, Tier 3 telemetry/Active Recall, and optional MCP for a concrete tool. LangGraph/Hermes/Letta remain replaceable choices outside Brain core. MCP complements but does not replace BMCP.

**最终裁决：有条件的产品采用方向，尚未批准生产采用。** 复用 Agent Runtime 和 Tool 生态，同时把 Brain 专属权威与证明语义留在 Brain 契约内。最小合理起步是一个 Runtime Adapter、一个 BrainClient、Tier 3 Telemetry/Active Recall，以及在确有工具需求时选择性接入 MCP。LangGraph/Hermes/Letta 都必须保持在 Brain Core 之外且可替换；MCP 补充 BMCP，不替代 BMCP。

---

## 11. Evidence Register / 证据登记

### Repository evidence
- Main README and C source pins: see §1.2.
- Main Adapter tiers and inference boundary: `07-agent-integration/adapter-capability-tiers.md`, `inference-boundary-model.md`.
- C-owned semantic boundary and product assessment: PR #69 branch files listed in §1.2. They are not merged into main.
- A research and review chain: PR #45, #56, #73; exact state and limitations in §1.3.
- H protocol snapshot: H branch HEAD and Blob pins in §1.2; separate branch, not main-merged.

### External official sources (accessed 2026-11-18)
1. LangGraph overview: https://docs.langchain.com/oss/python/langgraph/overview
2. LangGraph persistence/checkpointers: https://docs.langchain.com/oss/python/langgraph/persistence
3. LangGraph checkpoint semantics: https://docs.langchain.com/oss/python/langgraph/checkpointing
4. LangGraph durable execution: https://docs.langchain.com/oss/python/langgraph/durable-execution
5. LangGraph repository and MIT license: https://github.com/langchain-ai/langgraph and https://github.com/langchain-ai/langgraph/blob/main/LICENSE
6. Hermes Agent architecture: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture/
7. Hermes Agent repository/license: https://github.com/NousResearch/hermes-agent
8. Letta stateful agents: https://docs.letta.com/concepts/stateful-agents
9. Letta current source/runtime: https://github.com/letta-ai/letta-code and https://docs.letta.com/self-hosting/app-server/
10. Letta self-hosting: https://docs.letta.com/self-hosting/
11. MCP 2025-11-25 specification: https://modelcontextprotocol.io/specification/2025-11-25
12. MCP transport requirements: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
13. MCP authorization: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
14. MCP 2025-11-25 changelog: https://modelcontextprotocol.io/specification/2025-11-25/changelog

### Evidence status / 证据状态

| Claim | Status | Limitation |
|---|---|---|
| Main HEAD and README baseline | VERIFIED | Exact repository snapshot only |
| C Owner boundary/PR #69 | VERIFIED | Draft proposal, not cross-owner freeze |
| Main adapter tier semantics | VERIFIED | Conformance details remain candidate |
| LangGraph capabilities | OFFICIAL DOC VERIFIED | Not tested against Brain contracts |
| Hermes architecture | OFFICIAL DOC/REPO VERIFIED | Product behavior/version can evolve |
| Letta runtime/state model | OFFICIAL DOC/REPO VERIFIED | Not tested as Brain adapter |
| MCP protocol/transport | OFFICIAL SPEC VERIFIED | Does not establish I policy or Brain conformance |
| MCP SDK language parity | NOT EXHAUSTIVELY VERIFIED | Must pin chosen SDK and feature subset |
| BMCP full normative schema | PARTIAL / OWNER SOURCE PINNED | H branch artifacts separate; Session 05 does not claim full protocol revalidation |
| Runtime security/isolation | DESIGN REQUIREMENTS ONLY | No production audit or sandbox tests |
| Runtime performance | NOT RUN | No Brain prototype or target workload benchmark |
| End-to-end Applied/Forget | NOT RUN | Requires C/G/H/I/D/Storage integration tests |

---

## 12. Non-claims / 非声明

- No Agent Runtime, framework, provider, MCP SDK or deployment topology is approved/frozen by this report.
- No C-owned contract, BMCP schema, wire version, ACK, Applied semantics, Provider Outcome or Telemetry contract is changed.
- No Brain implementation, Runtime adapter, MCP server, sandbox, benchmark or production deployment was created.
- No cross-owner approval, security audit, production key registration, end-to-end Forget/Applied proof or independent review is claimed.
- No PR is merged and no architecture freeze or production activation is requested.

本报告不批准或冻结任何 Agent Runtime、Framework、Provider、MCP SDK 或部署拓扑；不修改 C Owner 契约、BMCP Schema/Wire/ACK、Applied 语义、Provider Outcome 或 Telemetry 合同；未创建 Brain 实现、Runtime Adapter、MCP Server、Sandbox、基准测试或生产部署；不声称跨 Owner 批准、安全审计、生产密钥注册、Forget/Applied 端到端证明或独立审查通过；不合并 PR，也不请求架构冻结或生产激活。
