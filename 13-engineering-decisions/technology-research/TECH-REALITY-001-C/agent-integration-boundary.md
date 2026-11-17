# Agent Integration Boundary / Agent 集成边界

## 1. System boundary / 系统边界
An Agent is an execution actor/runtime composition that plans, reasons, chooses actions and coordinates tools. It is not identical to a model, provider, process, session or authenticated Principal. A model generates outputs; a Provider hosts or exposes inference; an Agent Runtime manages the loop; a Session scopes a conversation/execution history. Identity and authorization are I-owned and B-typed.

Agent 是执行主体与运行时能力的组合，负责规划、推理、选择行动和协调工具。它不等同于模型、Provider、进程、Session 或经过认证的 Principal。模型生成输出；Provider 承载或暴露推理；Agent Runtime 管理执行循环；Session 界定会话/执行历史。身份和授权由 I 负责，类型语义由 B 负责。

## 2. Category distinctions / 类别区分
- External / Embedded / Autonomous / Workflow / Coding / Conversational / Multi-agent describe deployment or behavior patterns, not necessarily domain entities.
- Agent Host is the environment that owns the user interaction and policy integration; Agent Client is a protocol client; Agent Gateway is an optional ingress/routing façade; Agent Runtime executes turns, state and tool loops.
- Agent ≠ Model; one Agent may route among multiple Models and Providers, subject to explicit capability and policy checks.
- Agent ≠ Session; one Agent may have many concurrent Sessions. Session identity must not be inferred from an Agent label.
- Agent ≠ Principal; authenticated Principal and delegated authority are resolved by I, not asserted by Agent payload.
- Multiple Agents may share a user's Memory only through I-authorized scope grants and Brain-enforced scope/permission checks.
- Cross-session persistence is Brain-owned canonical Memory or Agent-owned state only as separately governed; a runtime's local history is not canonical Memory.

## 3. Responsibility split / 责任划分
| Concern | Agent / Runtime | Memory Brain | Joint boundary |
|---|---|---|---|
| Reasoning, planning, task decomposition | Authority | No | Context is advisory data |
| Model selection/invocation | Chooses within policy | Provider-independent integration contract | Capability negotiation and evidence |
| Tool proposal/dispatch | Agent chooses and orchestrates | No arbitrary tool execution | Tool capability/authorization at execution |
| Memory candidate | Submits proposal/source | Validates, governs, lifecycle applies | Provenance and validation evidence |
| Canonical Memory | No direct mutation | D canonical authority; E derived production | Typed request, authorization and receipt |
| Retrieval/activation | Requests and consumes | F owns retrieval/activation | Scope, freshness and reference validity |
| Context | Supplies runtime/session context | G owns ContextVersion and Applied record | H delivery; C final request evidence |
| Identity/authorization | Presents authenticated identity context | I enforces | Never trust payload claims |
| Telemetry | Emits runtime signals | Normalizes Brain-side trace/events | Correlation without authority confusion |

## 4. Prohibited patterns / 禁止模式
1. Direct writes to canonical storage: violates D/Storage authority and atomicity.
2. Agent-driven lifecycle transitions: bypasses D and Forget fences.
3. Treating LLM text as verified truth: confuses generation with evidence and B epistemic status.
4. Bypassing I authorization: cross-tenant and delegated-principal escalation.
5. Forging Applied or C/H attestations: evidence integrity failure; G/H/I own their respective checks.
6. Treating Tool success as Provider outcome or Memory Applied: different actors and boundaries.
7. Treating HTTP 200 as business success: transport status is not domain acceptance/commit.
8. Global unscoped Memory namespace: cross-user/session/environment leakage.
9. Cross-user Context without authenticated owner and grant: tenant isolation breach.
10. Reusing invalidated Memory references after Forget/revocation: stale data resurrection and disclosure.

## 5. Normative boundary / 规范边界
All state-changing Brain calls MUST resolve authenticated principal, scope, authorization and idempotency at the authoritative boundary. Agent/Provider/Tool payload identifiers are references/claims, never authentication. Canonical writes are accepted only through D-authorized Brain operations. Agent frameworks remain replaceable adapters, not the Memory Brain domain authority.

所有 Brain 状态变更调用必须在权威边界解析认证主体、Scope、授权和幂等性。Agent/Provider/Tool 载荷中的标识只是引用或声明，不是认证凭据。规范写入只能通过 D 授权的 Brain 操作完成。Agent Framework 是可替换适配器，不是 Memory Brain 领域权威。

## 6. Open owner decisions / Owner 未决项
B must confirm Agent/Principal/Session typed references and scope cardinalities. I must approve principal/delegation and tenant policy. H must confirm wire envelope/capability semantics. D/E/F/G must confirm write, derived-memory, retrieval and Context boundaries. These are not inferred from C's proposal.


## 完整中文版本

Agent 是负责规划、推理、选择行动和协调工具的执行主体/运行时组合，不等同于 Model、Provider、Process、Session 或 Principal。一个 Agent 可以调用多个 Model/Provider；一个 Agent 可以拥有多个并发 Session。Principal 身份及授权必须由 I 根据认证上下文解析，不能由 Agent 载荷自报。

External、Embedded、Autonomous、Workflow、Coding、Conversational 和 Multi-agent 是部署或行为类别，不必全部成为领域实体。Agent Host 管理交互环境，Agent Client 是协议客户端，Gateway 是可选入口/路由层，Runtime 执行推理和工具循环。

Agent/Runtime 负责推理、规划、任务拆分、行动选择、工具调用和 Agent 原生状态。Memory Brain 负责受控请求入口、规范领域规则、Canonical Memory 生命周期、受控 Retrieval/Context、Evidence/Provenance 和可验证操作结果。Provider 负责模型推理服务及其原生执行/响应元数据，不决定 Brain 业务状态。Tool Runtime 负责工具执行环境、副作用隔离和执行结果证据。I 负责身份、授权、委派和撤权；H 负责 BMCP Wire、Adapter Protocol 和 ACK；D/E/F/G 分别负责规范生命周期/Forget、派生记忆、检索激活、ContextVersion/Applied。

禁止 Agent 直接写 Canonical Storage、绕过 D 修改生命周期、将 LLM 输出声明为已验证事实、绕过 I 授权、伪造 Applied Attestation、将 Tool Success 当 Provider Outcome、将 HTTP 200 当业务成功、使用无 Scope 的全局 Namespace、跨用户共享未授权 Context，以及 Forget 后继续使用失效 Memory Reference。

所有状态变更请求必须在权威边界解析认证主体、Scope、授权和幂等性。载荷中的 ID 只是引用，不是认证凭据。Agent Framework 是可替换 Adapter，不是 Memory Brain 的领域权威。
