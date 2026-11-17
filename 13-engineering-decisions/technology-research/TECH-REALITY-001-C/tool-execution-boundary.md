# Tool Execution Boundary / Tool 执行边界

## 1. Definition / 定义
A Tool is an independently identifiable capability invoked by an Agent. It may be an in-process function, sandboxed process, remote service, MCP server tool or hosted provider tool. Tool definition, invocation proposal, authorization, execution, side effect and observed result are distinct records.

Tool 是由 Agent 调用的、具有独立身份的能力，可以是进程内函数、沙箱进程、远程服务、MCP Server Tool 或 Provider 托管工具。Tool 定义、调用提议、授权、执行、副作用和观察结果是不同记录。

## 2. Authority split / 权威划分
- Agent chooses whether to request a tool and interprets the result.
- I authorizes principal/action/resource/scope, capability grants, delegation and revocation. A tool's self-declared capability is descriptive, not permission.
- C records invocation correlation with Agent/Inference Attempt and Provider/Tool handoff evidence; it does not authorize.
- Tool host/runtime enforces sandbox, credentials, network/filesystem limits and captures execution result.
- D owns canonical Memory mutation/lifecycle; a tool cannot write canonical storage directly.
- H owns BMCP wire and Adapter protocol, not tool business outcome.

## 3. Capability declaration / 能力声明
A versioned manifest SHOULD declare: tool identity/version; input/output schema; read/write resource classes; external side-effect classes; network destinations; filesystem roots; memory/context access requested; execution environment; timeout; cancellation behavior; idempotency support; evidence/reporting capability; secret requirements. I decides grants. Capabilities are not automatically inherited across tool versions or delegated agents.

版本化 Manifest 应声明 Tool 身份/版本、输入输出 Schema、读写资源类别、外部副作用类别、网络目的地、文件系统根、Memory/Context 访问请求、执行环境、超时、取消行为、幂等支持、证据能力和 Secret 需求。授权由 I 决定。Tool 升级或 Agent 委派不会自动继承能力。

## 4. Side-effect state / 副作用状态
Track NOT_STARTED, ADMITTED, EXECUTING, EFFECT_POSSIBLE, EFFECT_CONFIRMED, EFFECT_REJECTED, UNKNOWN, COMPENSATION_REQUESTED, COMPENSATED only if tool host can substantiate these semantics. These are C research labels, not H wire enums. Compensation is not rollback unless the external system confirms it.

## 5. Retry rules / 重试规则
- Read-only deterministic tool: retry may be allowed under bounded policy after verifying no side effect.
- Idempotent write: retry only with same stable tool operation key and documented receiver semantics.
- Non-idempotent write: after timeout/response loss, reconcile by querying external system or human intervention; do not blindly retry.
- Partial side effect: retain partial/unknown and require compensating workflow; do not report atomic success.
- Cancellation does not undo a completed external effect.
- Tool success response is an observation from the tool boundary, not proof the target external system reached the intended state unless independently verified.

## 6. Memory boundary / Memory 边界
A tool may submit a candidate with source refs, execution identity, result digest, event time and observed_at/recorded_at. It MUST NOT modify Canonical Memory rows, advance lifecycle state, fabricate Evidence/Applied attestations or claim Forget completion. Brain revalidates authorization and current Forget/scope predicates at submission and commit time.

Tool 可以提交包含来源引用、执行身份、结果 Digest、Event Time 和观察/记录时间的候选，但不得修改 Canonical Memory 行、推进生命周期、伪造 Evidence/Applied Attestation 或声明 Forget 完成。Brain 必须在提交与 Commit 时重新验证授权和当前 Forget/Scope 条件。


## 完整中文版本

Tool 是由 Agent 调用、具有独立身份的能力，可为进程内函数、沙箱进程、远程服务、MCP Server Tool 或 Provider 托管工具。定义、调用提议、授权、执行、副作用和结果观察必须区分。

Agent 选择是否调用 Tool 并解释结果；I 决定主体、动作、资源、Scope、委派和撤权；C 记录调用与推理 Attempt 的关联和交付证据，但不负责授权；Tool Host 执行沙箱、凭据、网络和文件系统限制并捕获结果；D 拥有 Canonical Memory 变更和生命周期；H 拥有 BMCP Wire/Adapter Protocol。

版本化能力清单应声明 Tool 身份/版本、输入输出 Schema、读写资源、外部副作用、网络目的地、文件系统根、Memory/Context 访问请求、执行环境、超时、取消行为、幂等性、证据能力和 Secret 需求。能力声明不等于授权，授权由 I 决定。版本升级不会自动继承权限。

只有在工具宿主能证明时，才记录 NOT_STARTED、ADMITTED、EXECUTING、EFFECT_POSSIBLE、EFFECT_CONFIRMED、EFFECT_REJECTED、UNKNOWN、COMPENSATION_REQUESTED 或 COMPENSATED。补偿不等于回滚，除非外部系统确认。只读确定性 Tool 可在有限策略下重试；幂等写入仅在稳定 Operation Key 和接收端语义明确时重试；非幂等写入在超时/响应丢失后必须先对账，禁止盲目重试。取消不撤销已完成副作用。

Tool 可提交候选及来源、执行身份、结果 Digest、Event Time 和观察时间，但不得直接修改 Canonical Storage、推进生命周期、伪造 Evidence/Applied Attestation 或声明 Forget 完成。Brain 必须重新验证当前授权和 Forget/Scope 条件。



## MCP security-specific requirements / MCP 安全专项要求
MCP 2025-11-25 defines Host/Client/Server roles over JSON-RPC 2.0 with stateful connections and capability negotiation. It explicitly warns that tool descriptions/annotations from untrusted servers must be treated as untrusted, tools can represent arbitrary code execution, and Hosts must obtain explicit user consent before invoking tools. C treats these as protocol security requirements to map into I authorization and tool-host enforcement; MCP itself does not grant the permission.

MCP 2025-11-25 使用 JSON-RPC 2.0 定义 Host/Client/Server、Stateful Connection 和能力协商。规范明确指出不可信 Server 的 Tool 描述/Annotation 必须视为不可信，Tool 可能代表任意代码执行，Host 在调用 Tool 前必须取得明确用户同意。C 将这些要求映射到 I 授权和 Tool Host 执行控制；MCP 本身不授予权限。
