# Agent Integration Architecture Overview

**Status:** DECIDED baseline; CANDIDATE execution details; OPEN protocol details  
**Owner:** Session C — Agent Integration boundary pre-design  
**Scope:** Logical integration boundary. BMCP wire specification and concrete Adapter architecture belong to Session H.

## 1. Purpose

Define how a model- and Agent-independent Memory Brain collaborates with heterogeneous Agents. The integration must preserve Brain authority over memory while leaving reasoning, planning, action selection, tool execution, and safety policy with the Agent.

Goals:
- Standardize structured telemetry without requiring private reasoning traces.
- Support Agent-initiated Active Recall and Brain-initiated context updates.
- Apply context only at a defined inference assembly boundary.
- Make capability, delivery, acceptance, and application guarantees explicit.
- Keep Agent-specific protocols behind Adapters.
- Preserve scope, permission, provenance, and trust boundaries.

## 2. System boundary

~~~mermaid
flowchart LR
  subgraph AgentSide["Agent execution domain"]
    A[Agent: reason, plan, act]
    L[LLM / inference runtime]
    AA[Agent Adapter]
    EA[Environment Adapter]
    SL[Skill Library]
    A <--> L
    A <--> SL
    A <--> AA
    EA --> AA
    AA --> L
  end
  subgraph BrainSide["Memory Brain domain"]
    PG[BMCP integration gateway]
    T[Telemetry normalization]
    O[Memory observer]
    R[Retrieval and activation]
    C[Memory Context Manager]
    S[Context synchronization]
    PG --> T --> O --> R --> C --> S
    PG <--> S
  end
  AA <--> PG
  EA --> PG
~~~

### Ownership

**DECIDED — Brain owns**
- Canonical memory semantics, identity, lifecycle, provenance, and governance.
- Memory selection and activation policy.
- The authoritative version sequence of each managed Memory Context.
- Scope and permission decisions for Brain resources.

**DECIDED — Agent owns**
- Reasoning, planning, task decomposition, action selection, and tool invocation.
- Agent-native task state and private execution structures.
- Agent safety policy and authorization of external actions.
- Whether and how to act on returned memories.

**DECIDED — Agent Adapter owns**
- Mapping Agent-native signals to Brain-defined telemetry.
- Capability declaration and boundary validation.
- Receiving and validating context changes.
- Applying Brain-managed context only in a delimited region at an inference assembly boundary.
- Truthful acknowledgement of receipt, acceptance, application, rejection, and reconciliation.

Adapter does not own canonical memory, activation policy, or authoritative context versions.

**DECIDED — Environment Adapter owns**
- Translating environment-specific observations and state changes into normalized, source-qualified signals.
- Attaching environment identity and observation provenance.
- Reporting observations, not asserting unobserved state as fact.
- It does not actuate the environment on behalf of Brain.

**DECIDED — LLM/runtime owns** inference and token processing. Brain does not control model internals.

**DECIDED — Skill Library owns** executable skills and procedures. Brain may store experience referencing a skill, but does not execute skills or turn memories into executable code.

## 3. Responsibility matrix

| Capability | Brain | Agent | Agent Adapter | Environment Adapter |
|---|---|---|---|---|
| Canonical memory lifecycle | Primary | — | — | — |
| Planning and action choice | — | Primary | — | — |
| Telemetry source | Consumes | Primary | Maps | Supplies observations |
| Telemetry semantics | Defines | Supplies | Maps | Supplies observations |
| Retrieval and activation | Primary | May request | Transports | — |
| Context version authority | Primary | — | Tracks applied version | — |
| Inference context application | Defines target | Invokes inference | Executes | — |
| Environment observation | Consumes | May interpret | Transports | Primary |
| Environment actuation | — | Primary | May expose Agent API | — |
| Skill execution | — | Primary | Optional mapping | — |

Supporting a capability does not confer its authority.

## 4. Integration modes

**DECIDED:** Three patterns may coexist.

1. **Telemetry ingress:** Agent/Adapter submits structured task, intent, observation, outcome, uncertainty, risk, and environment signals.
2. **Active Recall:** Agent requests scoped memories for a task, entity, environment, or question.
3. **Context synchronization:** Brain publishes versioned snapshots or changes; Adapter applies them at a future inference boundary and acknowledges the result.

Telemetry ingress and Runtime Recall have different latency and durability goals. They may share a gateway, but must not be forced into one synchronous processing path. **CANDIDATE:** separate logical lanes/priority classes with a common identity and scope envelope. Physical separation requires evidence.

## 5. Canonical integration envelope

The final BMCP message shape belongs to Session H. The logical envelope includes:

| Field | Semantics | Requirement |
|---|---|---|
| telemetry_id | Stable submission identifier | Required |
| schema_version | Canonical schema version | Required |
| producer_id | Authenticated Adapter identity | Required |
| agent_instance_id | Agent instance | Required for context/session operations |
| scope | Ownership namespace | Required |
| signal_type | Canonical signal category | Required |
| occurred_at / observed_at | Source time | When known |
| recorded_at | Brain acceptance time | Brain assigned |
| payload | Typed signal body | Required |
| source_kind | Agent, environment, user, tool, external | Required |
| correlation_id | Task/turn/action correlation | Recommended |
| idempotency_key | Retry deduplication identity | Required for retryable writes |
| provenance | Origin and transformation history | Required for derived claims |

Unknown extension fields are namespaced opaque data; they do not override canonical fields.

## 6. Trust boundary

Telemetry and memory are data, not instructions. Agent-supplied labels such as trusted, verified, high priority, or system instruction do not grant authority. Adapter inserts memory only into the Brain-managed region and cannot overwrite system/developer instructions, user-originated input, tool definitions, or Agent security policy.

## 7. Core workflows

### Telemetry
1. Authenticate producer and resolve identity.
2. Map native fields to canonical signal types and attach scope/environment.
3. Validate schema, permission, timestamps, size, and idempotency.
4. Durably accept or reject.
5. Return an ingestion receipt. Acceptance does not imply semantic compilation or Memory creation.
6. Process downstream asynchronously, preserving provenance.

### Active Recall
1. Agent submits a scoped query and task/environment context.
2. Brain authorizes and resolves scope.
3. Runtime retrieves candidates and applies activation/visibility policy.
4. Brain returns qualified memory data and permitted evidence references.
5. Agent decides whether and how to use it.

### Proactive context update
1. Brain observes authorized telemetry/triggers.
2. Activation policy requests context planning.
3. Context Manager creates a versioned change from its authoritative base.
4. Synchronization delivers it.
5. Adapter validates scope, version, budget, and managed-region boundary.
6. Adapter reports receipt and acceptance separately.
7. At the next inference assembly boundary, Adapter applies the version and reports Applied.
8. Offline/stale Adapter is reconciled by delta or full snapshot.

## 8. State and authority

| State | Authority |
|---|---|
| Canonical Memory | Brain |
| Telemetry acceptance | Brain |
| Activation decision | Brain |
| Memory Context version | Brain Context Manager |
| Delivery state | Brain synchronization subsystem |
| Local applied version | Adapter, reported as attestation to Brain |
| Inference execution | Agent/runtime |

Applied Context is an acknowledgement record, not a second canonical context.

## 9. Reliability, consistency, and degradation

- A durable-acceptance receipt means the accepted telemetry survives restart under the declared durability contract.
- Duplicate retries under the same scoped idempotency key create one logical accepted event.
- Context versions are ordered by Brain authority.
- Unknown base versions and gaps are rejected or reconciled, never guessed.
- Brain failure must not stop Agent reasoning or environment control by default.
- Adapter offline means no new Applied claim; Brain tracks pending delivery and reconciles later.
- Missing/ambiguous environment identity causes rejection or quarantine of environment-specific signals.
- Permission revocation stops further access and triggers governed reconciliation; it is not itself Forget.

## 10. Security and isolation

Authentication and authorization apply to every operation. Scope is not permission. User, project, Agent, Agent instance, task, session, and environment isolation must be explicit. Environment IDs distinguish worlds, save files, tenants, and simulations. Memory returned to an Agent is untrusted data and cannot authorize tools or override Agent policy.

## 11. Performance and observability

Measure telemetry acceptance latency/durability, duplicate suppression, Recall p50/p95/p99, context generation-to-delivery and acceptance-to-applied latency, applied-version lag, reconciliation rate, rejection/error rate, and Agent task outcomes under controlled comparisons.

**TO_VALIDATE:** SLO values, payload budgets, telemetry cadence, activation thresholds, and local buffering windows. No performance multiplier is assumed.

## 12. Acceptance criteria

1. Changing Agent framework or LLM does not change canonical Brain semantics.
2. Planning, tool execution, and external action policy remain Agent-owned.
3. Telemetry can be durably accepted independently of model-assisted compilation.
4. Intent/plan/pending action cannot become a completed outcome solely by submission.
5. Received, Accepted, and Applied are separately observable.
6. Applied identifies Adapter, Agent instance, context session, version, and boundary correlation.
7. Brain cannot overwrite protected instruction/user/policy regions.
8. Invalid cross-scope or unauthorized operations fail closed.
9. Tier 3 can use telemetry and Recall without false proactive-sync claims.
10. Agent continues its primary task during Brain integration outage, subject to Agent policy.

## 13. Cross-session interfaces

| Partner | Required confirmation |
|---|---|
| Session B — Domain Model | Scope tuple, epistemic/time semantics, Event and provenance identity |
| Session E — Compiler | Telemetry-to-Event mapping and durable ingress |
| Session F — Runtime | Recall query context, activation triggers, risk/freshness signals |
| Session G — Context | Context/session identity, versions, Change Set and Applied record |
| Session H — BMCP/Adapter | Wire envelope, capability negotiation, acknowledgements, retries, errors |
| Session I — Governance | Authentication, authorization, audit, retention, idempotency and offline replay |

## 14. Open decisions

- **OPEN:** One common typed telemetry envelope or a small family of message families.
- **OPEN:** Environment Adapter direct ingress versus relay through Agent Adapter.
- **CANDIDATE:** Separate logical ingress and recall lanes.
- **TO_VALIDATE:** Event-specific payload/frequency limits.
- **OPEN:** Offline retention and local Adapter cache policy (Session I).
- **OPEN:** Partial context application. Safe default is reject unless partial semantics and per-entry results are explicitly defined.

## 15. Decision summary

- **DECIDED:** Brain owns memory and managed-context authority; Agent owns reasoning and action; Adapter maps and applies at inference boundaries.
- **DECIDED:** Environment Adapter reports observations, not actions.
- **DECIDED:** Telemetry acceptance is distinct from compilation.
- **DECIDED:** Applied is not proof of model comprehension.
- **DECIDED:** Memory remains untrusted data.
- **OPEN:** BMCP wire details remain Session H's responsibility.