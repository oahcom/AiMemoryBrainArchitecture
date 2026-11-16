# Module C — Agent Integration Baseline & Redlines

- Module: C — Agent Integration Architect
- Proposal version: 0.1.0
- Status: **PROPOSED — C Owner review required; not APPROVED**
- Owner branch: `session-c-agent-integration-2026-11-16`
- Prepared against observed branch tip: `702263dee9b40cf78fe95481731f52adb775c0d2`
- Scope: Agent integration semantics, telemetry, request-boundary evidence, Brain-managed Memory Region and Agent security boundary
- Template note: `00-governance/module-baseline-and-redlines-template.md` was not found in the live governance directory. This proposal follows the repository's existing status vocabulary and records the template gap as OPEN.

## 1. Purpose and authority

C defines the semantic contract at the Agent/Brain boundary: structured telemetry, source and trust labels, task/session/environment correlation, final inference-request evidence, capability ceilings, Brain-managed Memory Region isolation and Agent-side conformance requirements.

C preserves the division of authority:
- Agent owns reasoning, planning, action selection, tool invocation and Agent safety policy.
- Brain owns canonical Memory, retrieval/activation policy and authoritative Brain-managed Context version.
- Adapter maps Agent signals, validates capability/boundary constraints and applies Brain-managed context only in an explicitly delimited region at an inference assembly boundary.
- Environment Adapter reports source-qualified observations and environment identity; it does not actuate the environment on Brain's behalf.
- H owns BMCP wire, transport authentication binding, Adapter protocol and ACK/reconnect mechanics.
- G owns Context membership/version/change sets, delivery intent, reconciliation and Applied acceptance.
- I owns issuer trust, Principal/ProducerIdentity, authorization, delegation, PermissionEpoch, revocation and risk acceptance.
- B owns typed ActorRef/ScopeRef/EnvironmentRef domain semantics.
- D owns canonical Memory lifecycle/ForgetFence; E owns durable telemetry acceptance and compilation; F owns retrieval/runtime suppression.

C cannot decide G Applied semantics, H wire protocol, I authorization policy, B typed-reference definitions or D/E canonical ingestion/lifecycle semantics.

## 2. Status vocabulary and evidence discipline

- **DECIDED** — C-owned semantic invariant explicitly recorded in C artifacts.
- **PROPOSED / CANDIDATE** — C field/profile/execution recommendation awaiting relevant Owner decisions.
- **OPEN** — unresolved cross-owner contract, provider/runtime capability or enforcement question.
- **ADR-BLOCKED** — dependent domain behavior blocked by an unresolved ADR, including B ADR-001 where Fact/Claim semantics are implicated.
- **TO_VALIDATE** — requires concrete Adapter/runtime/provider experiments or implementation verification.
- **NOT RUN** — test is specified but no reproducible execution evidence exists.

Telemetry submission is not durable acceptance; acceptance is not compilation; compilation is not canonical commit; delivery is not application; test specification is not test pass.

## 3. Agent integration baseline

### 3.1 DECIDED responsibilities and boundaries

- Agent performs reasoning, planning, task decomposition, action selection and tool execution.
- Brain provides memory assets, retrieval/activation and versioned context targets; it does not become an Agent framework or action executor.
- Adapter translates Agent-native signals into Brain semantic contracts and applies context only at a future inference assembly boundary.
- In-flight inference requests are immutable from Brain's perspective; context changes affect a future boundary.
- Agent/Adapter may truthfully acknowledge receipt, acceptance, materialization, submission or application only with evidence appropriate to that stage.
- Full hidden Chain of Thought, private scratchpads, token-by-token reasoning and proprietary inference traces are not required.
- A concise PlanSummary is an Agent-authored report, not a faithful hidden-reasoning trace and not proof that planned steps occurred.

### 3.2 Integration modes

1. Telemetry ingress: structured task, intent, plan summary, pending action, tool call, observation, outcome, uncertainty, risk and environment-delta signals.
2. Active Recall: Agent requests scoped memory for a task/entity/environment/question.
3. Context synchronization: Brain publishes versioned Context snapshots/changes; Adapter validates and applies them at a future inference boundary.

Telemetry and Recall may share a gateway but have different latency/durability goals. Separate physical lanes remain CANDIDATE pending performance evidence.

## 4. Telemetry semantic baseline

### 4.1 Distinct signal kinds

The following remain distinct; consumers MUST NOT collapse them into a generic completed event:
- Task State
- Intent
- PlanSummary
- Active Entities
- PendingAction
- ToolCall
- Observation
- Outcome
- Uncertainty
- Risk Signal
- EnvironmentDelta

A record has one primary semantic kind; related records use typed references. Intent and plan are prospective. PendingAction is not a completed effect. ToolCall invocation/acknowledgement is not proof of external side effect. Observation is source-qualified and not automatically independently verified. Outcome must retain whether it is reported or independently evidenced. Uncertainty remains explicit; missing data is not certainty.

### 4.2 Telemetry envelope semantics

C's logical profile includes stable telemetry/event identity, schema version, producer claim, Agent/instance/session/task correlation, typed Scope and required Environment, signal type, occurred/observed/Brain-recorded times, source kind, correlation/idempotency, typed payload, provenance and namespaced extensions.

These are semantic requirements, not H's final BMCP wire field names, serialization, envelope or signature format. Producer timestamps and payload identity are claims. Brain acceptance time is assigned by the receiving Brain boundary.

### 4.3 Ordering and correction

- Preserve producer-scoped event identity, stream identity/epoch/sequence where available, occurred/observed/recorded times, clock quality and causal references.
- Exact duplicate is idempotent only within authenticated producer/stream namespace and matching payload digest.
- Same identity with a different digest is a conflict and must be quarantined/audited.
- Sequence gaps make source completeness unknown; do not fabricate missing events.
- Out-of-order and late records preserve original source time and arrival/recorded time; they cannot silently overwrite newer state.
- Corrections/retractions are append-only references to prior source events. They do not physically erase data and are not canonical Memory Forget.
- Environment switches require an explicit new Environment identity or authorized mapping.
- C defines source semantics; E owns durable receipt/idempotency and compilation, D owns canonical commit/lifecycle, H owns wire serialization.

## 5. Final Request Evidence baseline

### 5.1 Stage separation

| Stage | Meaning | Evidence authority | Does not prove |
|---|---|---|---|
| Prepared | G creates immutable authorized Context target and delivery intent | G ContextVersion/ChangeSet/Delivery intent | Delivery or application |
| Delivered | H transport endpoint accepts delivery attempt | H authenticated delivery receipt | Adapter materialization |
| Materialized | Adapter installs exact content in declared Brain-managed region | Adapter region identity and digest evidence | Final request inclusion/submission |
| Final Request Submitted | Exact immutable post-transformation request crosses observed runtime/provider submit boundary | C produces request-bound submission evidence | Model attention, understanding or execution start |
| Applied | G accepts required evidence under G's predicate | G authoritative Applied record | Model attention, comprehension, memory use or correct behavior |
| Execution Started | Runtime/provider reports execution start for the correlated request | Runtime/provider receipt | Completion or correctness |

Delivered is not Materialized. Materialized is not Submitted. Submitted is not Applied. Applied is not Execution Started.

### 5.2 C submission evidence

C may emit immutable per-request evidence only when the actual final immutable request, after all transformations, and successful handoff to the inference runtime/provider are observable.

The evidence profile includes actual InferenceRequestId, boundary ID/type, exact ContextVersion, DeliveryId/attempt, authenticated Agent/Adapter/runtime/session binding, Scope and required Environment, managed-region identity and complete content digest, PermissionEpoch/decision reference, ForgetFence generation/cursor reference, Adapter capability epoch/profile, submission outcome/time/ordering, integrity issuer/signature reference, schema version, correlation/causation/audit refs and coverage declaration.

C MUST NOT invent InferenceRequestId from DeliveryId, treat a local render as successful submission, or infer execution start from submit. Digest canonicalization/signature/wire representation remain H/C-dependent candidate details.

### 5.3 Capability ceilings

- Tier 1 — full final-request observable: may produce candidate Full evidence for G only when all exact request, complete region and current authority proof requirements are met.
- Tier 2 — middleware/managed-region observable but final transformations or submit not fully observable: Partial/Unknown only; MUST NOT claim Full Applied.
- Tier 3 — transport/basic event/Recall only: no Applied claim.
- Unsupported/Limited: explicit unsupported/bypassed/unknown result; no Full claim.

Tier is demonstrated capability, not a vendor label. Per-request bypass or missing observation reduces that request's evidence ceiling.

## 6. Brain-managed Memory Region and protected-region baseline

### 6.1 Protected regions

The runtime MUST keep these regions distinct:
- System Instructions — platform/Agent-owned and immutable to Brain.
- Developer Instructions — application/developer-owned and immutable to Brain.
- User Original Input — original user-originated bytes/structure; Brain cannot rewrite or silently summarize it.
- Agent Safety Policy — Agent-owned policy and action authorization; immutable to Brain.
- Agent-owned Context — cannot be mutated by Brain without a separate explicit authorized interface.
- Brain-managed Memory Context — only explicitly authorized data-only region for the target Agent, Scope, Environment, session and Permission Epoch.

If the runtime cannot isolate the Brain-managed region from protected regions, application must be rejected or reported Bypassed/Unknown. Memory must never be merged into privileged instruction roles.

### 6.2 Data-only rules

- Memory, Evidence, Provenance, summaries, compacted text, retrieval snippets, observations, tool outputs and historical Agent outputs are untrusted data, regardless of authentication or canonical storage.
- Imperative wording, repetition, confidence, source label or prior Agent authorship cannot grant instruction authority.
- Memory cannot override System/Developer instructions, User Original Input, Agent Safety Policy, tool definitions, tool availability, tool authorization or user consent.
- Memory may describe a tool/action but cannot authorize or execute it.
- Provenance, trust, Scope, Environment, freshness and transformation lineage survive summarization/compaction.
- Scope, PermissionEpoch and ForgetFence are revalidated at retrieval/application/final submit boundaries as required by owner contracts.
- Unknown identity, scope, environment, policy or fence state fails closed.
- This is a containment requirement, not a guarantee that every model ignores adversarial text; I owns threat-model governance and residual-risk acceptance.

## 7. Security redlines

1. Never equate Agent intent with completed result.
2. Never equate Delivered, Received, Accepted or Materialized with Applied.
3. Never equate Applied with model attention, comprehension, execution or behavioral compliance.
4. Never accept payload Agent/Adapter/Producer/Principal identity as authenticated proof.
5. Never treat ScopeRef as permission or a task ID as a grant.
6. Never allow Brain Memory to mutate protected instructions, original user input, Agent policy or tool authority.
7. Never promote untrusted Memory/Evidence/Summary/Tool Observation into instruction role.
8. Never infer external side effect from ToolCall invocation or ACK alone.
9. Never cross Scope/Environment boundaries through fallback, missing identifiers or silent remapping.
10. Never claim Tier 1/Full when final request, region coverage, request ID, identity, freshness or submit evidence is incomplete.
11. Never suppress evidence of uncertainty, bypass, partial coverage, conflict, late arrival or stale/revoked state.
12. Never retain forgotten plaintext solely to preserve an attestation; apply I retention policy and keep only permitted non-reconstructive evidence.

## 8. Interfaces and dependencies

| Partner | C input/output contract | Partner authority / open boundary |
|---|---|---|
| B | Consume typed Principal/Actor/Scope/Environment refs | B owns type semantics; ADR-001 remains ADR-BLOCKED |
| D | Preserve canonical refs, commit cursor, lifecycle and ForgetFence lineage | D owns canonical commit/Forget; C does not mutate canonical Memory |
| E | Supply stable source event/idempotency semantics and typed telemetry payloads | E owns durable Accepted receipt, compilation, retry/replay |
| F | Supply freshness, uncertainty, provenance and environment dimensions | F owns retrieval/index/suppression |
| G | Supply exact Context/session/request correlation and C submission evidence | G owns ContextVersion, delivery intent, Applied predicate and record |
| H | Consume authenticated transport/Adapter binding, capability and delivery evidence | H owns BMCP wire, transport, ACK/reconnect and capability protocol |
| I | Consume current trusted Principal/issuer/Producer binding and authorization/fence decisions | I owns trust, authorization, revocation, PermissionEpoch, global inventory and risk acceptance |
| Agent/runtime | Expose final immutable request and actual submit boundary | Runtime/platform engineering owns provider hook and execution-start evidence |

## 9. Conformance and test requirements

C conformance must cover:
- telemetry semantic non-collapse (intent/plan/pending/tool call/observation/outcome/uncertainty);
- no-CoT requirement and normal operation without hidden reasoning traces;
- authenticated transport identity versus payload identity claims;
- duplicate, collision, gap, out-of-order, late and correction/retraction handling;
- Scope/Environment isolation and task/session transition;
- exact ContextVersion/Delivery attempt/managed-region digest/request ID/final submit evidence;
- Tier 1/2/3 capability ceilings and per-request bypass coverage;
- stale PermissionEpoch, revocation, ForgetFence advance, session replacement and reconnect replay;
- protected System/Developer/User/Agent policy digests remain unchanged;
- Memory prompt injection, cross-scope/environment exfiltration and unauthorized tool requests;
- failure-closed behavior for unknown/mismatched identity, scope, environment, capability or fence.

Required evidence for PASS: test ID and contract version, exact source/build SHA, Adapter tier/capability epoch, protocol/schema version, fixture digest, authenticated principal/issuer class, Scope/Environment/PermissionEpoch, ContextVersion/Delivery/ForgetFence where relevant, expected/actual result, logs/traces, reproducible command/procedure and Owner review. No hidden CoT, credentials or unnecessary prompt plaintext should be retained.

Existing C conformance cases and matrices are specifications only. Unless a reproducible execution record is attached, all such tests remain **NOT RUN**. This proposal claims no implementation, penetration test, end-to-end test or runtime conformance pass.

## 10. Acceptance criteria

C proposal is ready for C Owner review when:
1. Agent and Brain authority boundaries are explicit.
2. Telemetry semantic types and evidence ceilings cannot be collapsed.
3. Prepared/Delivered/Materialized/Submitted/Applied/Execution Started remain distinct.
4. Full submission evidence binds the exact final immutable request and managed region.
5. Tier capability claims are evidence-based and fail closed.
6. Protected regions and data-only Memory boundary are explicit.
7. Security redlines preserve I/B/H/G/D/E/F authority.
8. Test cases cover adversarial, temporal, identity, reconnect and bypass scenarios.
9. OPEN, CANDIDATE, ADR-BLOCKED and NOT RUN states remain visible.

## 11. Change authority and compatibility

- C may change C-owned telemetry semantics, Agent evidence meaning, capability evidence requirements, protected-region requirements and C conformance expectations through versioned C decisions.
- C may not redefine G Applied acceptance, H wire/ACK/transport, I identity/authorization/risk policy, B typed references, D canonical Memory/Forget or E durable acceptance.
- Cross-module changes require explicit decisions from every affected authority and consumers must accept the exact version.
- C cannot mark another Owner's tests, implementation, policy or contract approved.
- Breaking telemetry or evidence semantics require schema/profile versioning and explicit consumer compatibility review.

## 12. Open / blocked / validation register

| ID | Item | Status | Required authority / evidence |
|---|---|---|---|
| C-G0-01 | Canonical governance template absent at requested path | OPEN | Governance Owner to publish/identify template |
| C-G0-02 | Exact H wire fields, signature and schema encoding | OPEN / H-owned | H protocol decision and C/H compatibility |
| C-G0-03 | Authenticated Principal/Agent/Adapter/Producer binding | OPEN / I/H/B | Exact trust policy, transport binding and typed-ref decisions |
| C-G0-04 | G Applied exact predicate/version and common C/G/H acceptance | OPEN / G/H/C | G decision and same-version C/G/H acceptance |
| C-G0-05 | Final immutable request submit observability per provider/runtime | TO_VALIDATE | Concrete runtime hooks, request IDs and trace evidence |
| C-G0-06 | Full managed-region digest/canonicalization and signing profile | OPEN / H/C | Exact digest, schema, integrity and key reference agreement |
| C-G0-07 | ForgetFence/currentness and PermissionEpoch revalidation | OPEN / D/I/H/G | Owner-owned protected boundary contracts and runtime evidence |
| C-G0-08 | Environment Registry authority and mapping | OPEN | I/Governance designation and B typed EnvironmentRef |
| C-G0-09 | Prompt-injection residual risk acceptance | OPEN | I threat governance; C requirements do not accept risk |
| C-G0-10 | Adapter/runtime conformance execution | NOT RUN | C/H/I/G/D/E/Agent runtime tests with reproducible evidence |
| C-G0-11 | Fact/Claim-dependent telemetry interpretation | ADR-BLOCKED where applicable | Preserve B ADR-001 block |

## 13. Evidence inspected

- C branch: `session-c-agent-integration-2026-11-16`, observed pre-write HEAD `702263dee9b40cf78fe95481731f52adb775c0d2`.
- `07-agent-integration/agent-integration-overview.md` Blob `b944dee9d0f1b232c4e0716c094ebbe230571e14`.
- `07-agent-integration/telemetry-model.md` Blob `efe3c2b1e82f64ee5ff57ab468d7a9c6b54e6157`.
- `07-agent-integration/telemetry-event-and-identity-contract.md` Blob `2bd9e640bd0c1d2c8b768da1e06b06096bc2a79e`.
- `07-agent-integration/inference-boundary-model.md` Blob `56b9e2e51804f8977797851a2cc41b6ebb7f2338`.
- `07-agent-integration/phase-3.5-agent-identity-applied-attestation-untrusted-memory.md` Blob `52c20764e6d74ba16392ded461690f50147f0343`.
- `07-agent-integration/phase-3.6-final-request-evidence-contract.md` Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`.
- `07-agent-integration/security-and-untrusted-memory-boundary.md` Blob `b32aeeb0b7b226cd3770d2af82b0ddfbf35a511d`.
- `07-agent-integration/adapter-conformance-cases.md` Blob `6569cb558805ca1247df07f17e3fafa15334528b`.
- `07-agent-integration/conformance-matrix.md` Blob `ae31eb8554f04b1d21f5aee80537425b1ddd5329`.

## 14. Proposal disposition

**PROPOSED 0.1.0.** This is a C-owned Agent integration baseline proposal only. It is not a G Applied decision, H wire approval, I security approval, B domain decision, D canonical Memory decision, implementation certification or test pass.
