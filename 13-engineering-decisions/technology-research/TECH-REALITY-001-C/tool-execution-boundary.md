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
