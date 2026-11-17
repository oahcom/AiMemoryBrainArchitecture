# Agent Integration — Architecture Guide

- Document ID: DOC-AGENT-001
- Version: 1.0
- Owner: C — Agent Integration
- Source: C owner branch, Agent Integration Architecture Overview
- Chinese counterpart: [Agent 集成架构指南](../../zh-CN/07-agent-integration/agent-integration-guide.md)
- Status: Explanatory guide; execution details CANDIDATE and protocol details OPEN/H-owned

## 1. Purpose

Agent Integration defines how a model- and Agent-independent Brain collaborates with heterogeneous Agents while preserving a clean authority boundary.

The Brain owns canonical memory and its managed Context. The Agent owns reasoning, planning, action selection, tool execution, and its safety policy. The Adapter connects the two without turning the Brain into an Agent framework.

## 2. The three participants

| Participant | Owns | Must not take over |
|---|---|---|
| Memory Brain | Canonical memory, selection/activation policy, managed Context version authority, Brain-resource authorization | Agent planning, tool execution, external action policy |
| Agent | Reasoning, planning, task decomposition, action choice, tools, native task state, safety policy | Brain's internal memory semantics |
| Agent Adapter | Telemetry mapping, capability declaration, context validation/application at inference boundary, truthful ACK | Canonical memory, activation policy, authoritative ContextVersion |

Environment Adapter normalizes environment observations, binds environment identity and provenance, and reports observations; it does not actuate the environment for the Brain. The LLM/inference runtime owns model inference and token processing.

## 3. What telemetry is required

The Brain needs structured signals about the Agent's task and environment, not private chain-of-thought. Useful telemetry includes task state, intent, plan summary, active entities, tool call/pending action, observations, outcome, uncertainty, risk signals, and environment delta.

Intent, plan, prediction, and pending action must remain distinct from completed outcomes. Telemetry is untrusted input: it can guide relevance and memory needs, but it does not prove truth or grant permission.

## 4. Two-way integration

~~~text
Agent → Adapter → BMCP Gateway → Brain
   task/intent/observations/outcomes       |
                                           | recall / activation / context changes
Agent ← Adapter ← BMCP Gateway ← Brain
        managed context at inference boundary
~~~

The Agent may request Active Recall. The Brain may initiate context updates when its policy and telemetry indicate they are useful. In either direction, the Adapter validates scope, capability, version, and authorization.

## 5. Inference-boundary application

Context changes are applied only in a defined inference-context assembly boundary and only inside the Brain-managed region. The Adapter must not rewrite System/Developer instructions, original user input, or Agent safety policy.

For Tier 1 Full Applied, the Adapter must be able to observe the final request submitted to the inference runtime and attest the exact managed-region version/content at that boundary. If it can observe only an intermediate buffer or transport receipt, it must report a weaker capability and must not claim Full Applied.

Applied means “the Adapter applied this managed context at the agreed boundary.” It does not mean the model attended to, understood, remembered, or followed it.

## 6. Integration deployment options

Possible Adapter shapes include:
- Embedded SDK/library inside the Agent process.
- Local sidecar process with an explicit IPC boundary.
- Local or remote Gateway client for Agents that cannot embed the SDK.

These are candidates, not a frozen deployment choice. Select based on whether the integration can reliably observe the final inference request, preserve the managed-region boundary, authenticate identity, support reconnect, and produce trustworthy evidence. A transport connection alone is not Tier 1 integration.

## 7. Capability and compatibility

The Adapter declares supported protocol versions, telemetry types, context operations, maximum context budget, inference-boundary visibility, clear/suppression support, and reconnect behavior. Capability negotiation must be explicit and versioned.

H owns BMCP wire schemas and message semantics. C owns Agent-side integration requirements and compatibility behavior. Language-specific SDKs or FFI must not change the protocol's canonical field names or security semantics.

## 8. Failure and recovery

| Condition | Required behavior |
|---|---|
| Agent does not expose final request | No Tier 1 Full Applied claim |
| Adapter offline | Queue only under explicit policy; reconcile current version and Forget state on reconnect |
| Unsupported context operation | Reject or negotiate a supported fallback; never silently ignore |
| Scope/identity ambiguous | Fail closed |
| Permission epoch changed | Re-authorize before applying |
| Forget Fence advanced | Clear/suppress local managed region and acknowledge the actual capability/result |
| Partial context materialization | Report partial/rejected; do not ACK Applied |
| Agent prompt layout changed | Revalidate managed-region locator before next application |

## 9. Trust and safety boundary

Memory content is untrusted data, not instructions. The Adapter must preserve a clearly delimited managed region and must not elevate retrieved content to System/Developer authority. Brain memory does not authorize external actions; Agent safety and tool authorization remain with the Agent.

Telemetry must not require hidden chain-of-thought. Plan summaries and structured observations are sufficient when they carry source, time, scope, and uncertainty.

## 10. Validation still required

- Embedded, sidecar, and Gateway integration feasibility.
- Final-request observation and Applied attestation.
- Adapter identity, capability epoch, PermissionEpoch, and ForgetFence binding.
- Offline/reconnect, clear/suppression, and partial delivery.
- Prompt injection and managed-region isolation.
- Multi-language Agent compatibility and conformance tests.

See the [C owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-c-agent-integration-2026-11-16/07-agent-integration) and H's BMCP protocol specifications for detailed contracts.
