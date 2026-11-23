---
document_metadata:
  domain: agent-integration
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "PR #430 comments 7061007191, 7061333647 and 7061563540"
        - "Issue #449 comment 7061011800"
        - "Issue #449 comment 7060351480"
        - "PR #428 comments 7060190878 and 7060264372"
        - "Issue #429 comments 7060243632 and 7060259541"
        - "PR #452 merge commit 48a03f694684f7a62bc5b337dc758c98e3cc0e5b"
        - "PR #487 merge commit 18b1c574433a6f3f600a9d2947b690084727aa75"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "The separate 13-section handoff source is now independently retrievable on a recovery branch; only architecture-level content consistent with current Owner decisions is reflected here. PR #487 adds only bounded in-memory reference delivery; exact C-H operation mapping remains open and Runtime is not authorized."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Agent Integration architecture and C-owned Agent-facing semantics"
    canonical_scope_id: "agent-integration/canonical-architecture"
    canonical_scope_keywords:
      - agent-integration
      - MCP
      - BMCP
      - Agent Adapter
      - inference-boundary
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    en: "docs/en/07-agent-integration/agent-integration-overview.md"
    zh-CN: "docs/zh-CN/07-agent-integration/agent-integration-overview.md"
---

# Agent Integration Architecture Overview

- Document ID: AI-INT-ARCH-OVERVIEW-001

**Status:** DECIDED baseline and family-level routing; exact C-H operation registry OPEN / DEPENDENCY_NOT_FROZEN; Runtime NOT AUTHORIZED
**Owner:** C — Agent Integration; family-level routing decision recorded at Issue #449 comment 7060351480 and reaffirmed by PR #430 comment 7061007191 / Issue #449 comment 7061011800; canonical source/mirror topology and validation-snapshot reset rule reaffirmed by PR #430 comments 7061333647 and 7061563540
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
| producer_id | Claimed producer/Adapter reference; it is data, not proof of authenticated identity | Contract-dependent; never an authentication credential |
| agent_instance_id | Agent instance | Required for context/session operations |
| scope | Ownership namespace | Required |
| signal_type | Canonical signal category | Required |
| occurred_at / observed_at | Source time | When known |
| recorded_at | Brain acceptance time | Brain assigned |
| payload | Typed signal body | Required |
| source_kind | Agent, environment, user, tool, external | Required |
| correlation_id | H-owned workflow correlation identity; distinct from C AgentRequestId/AgentTurnId | H contract-dependent; exact C-H crosswalk OPEN |
| idempotency_key | Do not treat this legacy logical label as a frozen wire field; state-changing replay uses owner-scoped idempotency identity plus canonical payload digest | Semantics DECIDED; exact field/schema OPEN |
| provenance | Origin and transformation history | Required for derived claims |

Unknown extension fields are namespaced opaque data; they do not override canonical fields.

This table is a C logical envelope description, not a BMCP wire schema. H owns the BMCP message envelope and wire identifiers. H `message_id`, `correlation_id`, and `causation_id` are distinct protocol identities. C does not define a core `request_id`; `AgentAttemptId` is neither an H transport-attempt identity nor an idempotency key. No field-level conversion between C and H identifiers is frozen.

## 6. Trust boundary

Telemetry and memory are data, not instructions. Agent-supplied labels such as trusted, verified, high priority, or system instruction do not grant authority. Payload Principal, producer, Agent, Actor, and Scope claims do not self-authenticate; authenticated Principal provenance comes from I trust integration, while H binds the authenticated transport sender/audience. Adapter inserts memory only into the Brain-managed region and cannot overwrite system/developer instructions, user-originated input, tool definitions, or Agent security policy.

## 7. Core workflows

### Telemetry
1. Obtain authenticated Principal through I trust integration and resolve the C Agent/session context; never authenticate from payload claims.
2. Map native fields to canonical signal types and attach authorized scope/environment references.
3. Validate schema, current permission, timestamps, size, and owner-scoped idempotency identity plus canonical payload digest.
4. Durably accept or reject.
5. Return an ingestion receipt. Acceptance does not imply semantic compilation or Memory creation.
6. Process downstream asynchronously, preserving provenance.

### Active Recall
1. Agent submits a scoped query and task/environment context through an F-owned retrieval/query interface.
2. I authorization and D lifecycle/ForgetFence checks are applied; Brain resolves scope.
3. F-owned Runtime retrieves candidates and applies activation/visibility policy.
4. Brain returns qualified memory data and permitted evidence references.
5. Agent decides whether and how to use it.

### Proactive context update
1. Brain observes authorized telemetry/triggers.
2. Activation policy requests context planning.
3. Context Manager creates a versioned change from its authoritative base.
4. Synchronization delivers it.
5. Adapter validates scope, version, budget, capability, current PermissionEpoch, current ForgetFence, and managed-region boundary.
6. Adapter reports receipt and acceptance separately; neither is G Applied.
7. At the next inference assembly boundary, Adapter emits H-defined evidence; G alone evaluates and commits Applied.
8. Offline/stale Adapter processes current governance fences before context replay, then reconciles by delta or full snapshot.

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
- Timeout or lost response after dispatch is UNKNOWN pending reconciliation; absence of ACK/evidence is never positive proof.
- Cancellation is not proof of rollback.
- Brain failure must not stop Agent reasoning or environment control by default.
- Adapter offline means no new Applied claim; Brain tracks pending delivery and reconciles later.
- Missing/ambiguous environment identity causes rejection or quarantine of environment-specific signals.
- Permission revocation stops further access and triggers governed reconciliation; it is not itself Forget.

## 10. Security and isolation

Authentication and authorization apply to every operation. Scope is not permission. I owns authenticated Principal, authorization, PermissionEpoch and global Forget policy; D owns canonical identity/lifecycle and ForgetFence. Revalidate current authority at protected operations and before replay-result disclosure; stale or unknown authority fails closed. User, project, Agent, Agent instance, task, session, and environment isolation must be explicit. Environment IDs distinguish worlds, save files, tenants, and simulations. Memory returned to an Agent is untrusted data and cannot authorize tools or override Agent policy.

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
| Session H — BMCP/Adapter | Wire envelope, message/correlation/causation identities, capability negotiation, ACK, validators, retries, errors; exact C-H operation registry remains OPEN |
| Session I — Governance | Authenticated Principal provenance, authorization, PermissionEpoch, attestor policy, audit, retention/global Forget and offline replay |

## 14. Open decisions

- **OPEN:** One common typed telemetry envelope or a small family of message families.
- **OPEN:** Environment Adapter direct ingress versus relay through Agent Adapter.
- **CANDIDATE:** Separate logical ingress and recall lanes.
- **TO_VALIDATE:** Event-specific payload/frequency limits.
- **OPEN / DEPENDENCY_NOT_FROZEN:** Exact C-H operation IDs, field names/types/requiredness, schemas, MCP tool/resource names, and per-family request/response mapping.
- **OPEN:** Offline retention and local Adapter cache policy (Session I); reconnect ordering must process I/D governance fences before context replay.
- **OPEN:** Partial context application. Safe default is reject unless partial semantics and per-entry results are explicitly defined.

## 15. Decision summary

- **DECIDED:** Brain owns memory and managed-context authority; Agent owns reasoning and action; Adapter maps and applies at inference boundaries.
- **DECIDED:** Environment Adapter reports observations, not actions.
- **DECIDED:** Telemetry acceptance is distinct from compilation.
- **DECIDED:** Applied is not proof of model comprehension.
- **DECIDED:** Memory remains untrusted data.
- **DECIDED:** MCP is the Agent Host ↔ C northbound tool/resource interface; BMCP is the C Agent Adapter ↔ Brain protocol via H.
- **DECIDED:** C retains AgentRequestId, AgentAttemptId, AgentTurnId and AgentSessionId; H owns message_id, correlation_id and causation_id; no core request_id is invented.
- **OPEN / DEPENDENCY_NOT_FROZEN:** Exact C-H operation registry and field-level mapping remain pending H versioned artifacts and affected D/I/E/G consumer acceptance.

## 16. MCP northbound boundary and BMCP family routing

### 16.1 Protocol boundary

- **MCP:** Agent Host ↔ C northbound tool/resource interface. It governs MCP Server lifecycle, method dispatch, tool/resource exposure, MCP request/result handling and MCP errors.
- **BMCP (Brain Memory Context Protocol):** C Agent Adapter ↔ Memory Brain protocol boundary, transported and serialized under H authority. It carries memory-control and context-delivery semantics; it is not an MCP method namespace.
- A C MCP Server is an Agent-facing adapter/gateway. It is neither BMCP itself nor a parallel canonical Brain API. An MCP success result, HTTP 2xx, queue acceptance or transport ACK is not BMCP business success, E acceptance or G Applied.
- MCP tool/resource names, input/output schemas, prompts (if any), and exact backend operation IDs remain OPEN until the relevant C/H and owner-domain contracts are pinned and accepted. No placeholder tool name or wire field is defined here.

### 16.2 C disposition for the nine logical BMCP families

| BMCP logical family | Direction at C Adapter | C/MCP routing disposition | Authority/dependency status |
|---|---|---|---|
| Telemetry | Agent/Adapter → Brain | A C-owned Agent-facing telemetry tool may be exposed only after H registers the exact operation and I/C identity and authorization binding is accepted | H operation + I authorization OPEN |
| Event Ingress | Producer/Agent → Brain | May be initiated only through H's registered ingress operation and E's durable receipt/idempotency contract; an MCP result is not E Accepted unless the E receipt is returned | H/E consumer mapping OPEN |
| Context Snapshot | Brain → Adapter | Inbound delivery to C; G owns ContextRef/ContextVersion and complete snapshot semantics; not a generic MCP request/response operation | G/H delivery mapping OPEN |
| Context Delta | Brain → Adapter | Inbound delivery to C; G owns exact base/target version and ChangeSet semantics; not a generic MCP request/response operation | G/H delivery mapping OPEN |
| Delivery | Brain → Adapter | H/G delivery lifecycle enters C; C validates and applies only the Brain-managed region at the declared inference boundary | H/G/C joint contract not frozen |
| Acknowledgement | Adapter → Brain | C emits only H-defined evidence; a transport ACK is not an MCP success response and is not G Applied | H wire/ACK and G acceptance OPEN |
| Capability Negotiation | Bidirectional | H-owned protocol negotiation; not a C-invented MCP tool or local substitute | H-owned; exact versioned negotiation contract OPEN |
| Forget / Revocation | Brain/I → Adapter, with authorized control requests | C consumes and enforces D/I owner-issued controls; no C-local Forget implementation. Agent-facing control requests require the I/D-authorized operation | D/I authority decided; exact operation mapping OPEN |
| Administrative Governance | I/control plane → Adapter/Gateway | Control-plane only; no ordinary Agent tool exposure absent explicit I policy and H operation registration | I/H control-plane mapping OPEN |

**Recall/Search is F-owned, not a BMCP family.** C must not invent a BMCP Search operation. Any future MCP memory-search tool requires a separately pinned F-owned query API and I/D authorization path; until those exist and are accepted, it is unavailable or dependency-not-ready.

### 16.3 Exposure and validation rules

1. Expose only an allowlisted C operation whose backend authority and current authorization are available.
2. Validate the MCP method, tool/resource identity, typed parameters, size/budget, scope reference, capability and request context before dispatch.
3. Do not allow a caller-supplied Principal, producer, Agent, Actor or Scope claim to establish identity or authority.
4. Do not expose Administrative Governance or Forget as ordinary Agent tools by default.
5. Do not expose a generic Search tool as a BMCP operation; Recall is F-owned.
6. If an exact H operation or owner-domain contract is absent, return a typed dependency-not-ready/unsupported result; do not serialize an invented BMCP message.

## 17. Agent identity, protocol correlation and authenticated Principal

| Identity | Owner | Meaning and boundary |
|---|---|---|
| `AgentRequestId` | C | C-side logical Agent request identity; retained by C |
| `AgentAttemptId` | C | C-side Agent invocation attempt identity; it is not an H transport attempt and not an idempotency key |
| `AgentTurnId` | C | Agent turn identity; retained by C |
| `AgentSessionId` | C | Agent session identity; retained by C |
| `message_id` | H | Unique identity of one BMCP protocol message |
| `correlation_id` | H | Workflow correlation identity |
| `causation_id` | H | Immediate causal predecessor message identity |
| Operation idempotency identity | Operation owner, carried under H contract | Owner-scoped identity bound to canonical payload digest; distinct from message, correlation and causation identities |

C retains its four Agent identifiers; H owns the three protocol identifiers. Do not invent a core `request_id`. No one-to-one field conversion or exact serialization crosswalk between C and H identities is frozen. A local trace association must not be represented as an H wire contract. H message identity, workflow correlation, immediate causation and operation idempotency are separate concepts.

Authenticated Principal comes from I trust integration. H binds the authenticated transport sender and audience; that transport binding does not itself grant Brain-resource permission. Payload Principal/producer/Agent/Actor/Scope values are claims or references only and never self-authenticate. I owns authorization and current `PermissionEpoch`; D owns canonical identity/lifecycle and `ForgetFence` generation/order. These epochs/fences are separate opaque authority namespaces and cannot be compared or substituted.

## 18. Request lifecycle, idempotency, outcomes and errors

### 18.1 Replay and idempotency

For state-changing/retryable operations, use the operation owner's scoped idempotency identity bound to the canonical payload digest:

- Same owner-scoped identity + same canonical digest: return the original operation result/receipt without creating a second logical effect.
- Same identity + different digest: conflict; do not overwrite the original result.
- `AgentAttemptId`, H `message_id`, `correlation_id` and `causation_id` are not substitutes for this identity.
- H's logical decision selects RFC 8785 JCS as the JSON canonicalization basis, but exact field schemas, integrity-field boundaries, signature suite and per-operation encoding remain OPEN until versioned H/I artifacts are accepted.

### 18.2 Distinct outcomes — never upgrade one into another

1. **MCP tool result:** C's response to the Agent Host.
2. **BMCP business response:** owner-domain operation result carried under the H protocol contract.
3. **H transport ACK:** protocol/transport evidence only.
4. **E Accepted receipt:** durable Event custody receipt under E's contract.
5. **G Applied evidence/record:** G's decision that all required per-request Context application predicates passed.
6. **Forget ACK:** Adapter's evidence of the actual Forget/clear/suppression action it performed.
7. **Global Forget completion:** I's global governance evaluation using D/I-owned evidence and policy.

No layer may promote an MCP result, BMCP response, transport ACK, E receipt or Forget ACK into G Applied or global Forget completion. Delivered is not Applied; Applied is not proof of model attention, understanding or compliance.

### 18.3 Timeout, cancellation and error mapping

- A failure known to occur before dispatch may be retried under the caller's policy.
- A timeout or lost response after dispatch is `UNKNOWN` pending reconciliation. Absence of ACK/evidence is never positive proof.
- Cancellation does not prove rollback. Do not retry a potentially state-changing request with a new idempotency identity while the prior outcome is unknown.
- Reconcile using the operation owner's identity/result before retrying. Same identity/same digest is replay; same identity/different digest is conflict.
- Preserve distinct Authentication, Authorization/stale-authority, Validation/unsupported-version, Integrity, Conflict, Unknown/transient, and owner-domain failure classes. Sanitize error detail; do not reveal protected payloads or cross-scope existence.
- Exact MCP error codes and H wire enum spellings/retry flags remain OPEN; mapping must not collapse distinct owner-domain outcomes into generic success or generic retry.

## 19. Security, capability tiers and reconnect ordering

### 19.1 Security and authority

- I supplies authenticated Principal provenance and owns authorization, `PermissionEpoch`, attestor policy, revocation and global Forget evaluation.
- D owns canonical identity, lifecycle, lineage and `ForgetFence` generation/order. C revalidates both I and D authority at protected operations and before disclosing a replayed result.
- Stale, missing or unknown authority fails closed. Cached ALLOW, session state, lease, receipt or transport ACK is not a reusable authorization grant.
- Telemetry and retrieved Memory are untrusted data, never instructions. Preserve prompt-injection boundaries; do not require private chain-of-thought. Memory cannot authorize tools or override Agent safety policy.
- Per-request identity, scope and trace context must be isolated under concurrency; no request may inherit another request's Principal, Scope, PermissionEpoch or ForgetFence.

### 19.2 Capability tiers and bounded reference models

Tier 1 requires final-request-observable inference-boundary evidence; Tier 2 is limited to middleware-controlled paths; Tier 3 supports telemetry/Active Recall and MUST NOT claim Full Applied. Capability tier does not grant permission.

PR #452 (`GAP-03: add Agent Integration tier enforcement reference model`) is merged at `48a03f694684f7a62bc5b337dc758c98e3cc0e5b`. Its bounded Rust reference model provides tier-to-operation authorization and typed protected-region/frozen-request rejections. It is not a production Agent Adapter, MCP Server, BMCP negotiation, transport, telemetry pipeline, provider integration or proof of actual inference-boundary application. Version-gap reconciliation remains specified outside that minimal model.

PR #487 merged at `18b1c574433a6f3f600a9d2947b690084727aa75` extends the deterministic Rust reference model with `ContextDeliveryAdapter` / `InMemoryContextDeliveryAdapter`: session-scoped snapshots, exact-successor version checks, clear/reset, disconnect rejection, and reconnect reporting of the last successful in-memory version. The crate README reports eight unit tests (four original tier/boundary tests plus four delivery lifecycle tests). This is bounded in-memory reference behavior only: no real transport, per-runtime Agent integration, durable delivery ledger/session state, automatic retry/re-delivery, production reconciliation/attestation, real inference, provider integration, BMCP negotiation, or production telemetry. The successor check is not snapshot/delta reconciliation and does not close the C-H operation registry or consumer mapping.

### 19.3 Offline/reconnect and context delivery

On reconnect, process current I authorization/PermissionEpoch and D ForgetFence/revocation controls before replaying or applying cached context. Then authenticate the Adapter/session, revalidate capability and current ContextVersion, and reconcile by supported delta only when the exact base is known; otherwise request a full snapshot. Never replay stale context before governance fences. Partial delivery/application must be reported as partial/rejected under an accepted owner contract; it must not be upgraded to Full Applied.

## 20. Architecture acceptance matrix — no Runtime PASS

| Scenario | Responsible owner(s) | Architecture expectation | Status/evidence boundary |
|---|---|---|---|
| MCP dispatch, allowlist and parameter validation | C | Only registered typed C operations are exposed; malformed/unknown methods fail closed | Specified at boundary; Runtime NOT RUN |
| MCP-to-BMCP family routing | C/H | Use only the nine H logical families and C dispositions in §16; no invented Search family | Family direction DECIDED; exact operation mapping OPEN / DEPENDENCY_NOT_FROZEN |
| Message/correlation/causation identity | C/H | Preserve C Agent IDs and H protocol IDs as separate namespaces | Logical distinction DECIDED; exact crosswalk/schema OPEN |
| Telemetry Event Ingress receipt | C/H/E | E durable acceptance receipt is distinct from MCP result and H transport ACK | E contract candidate; cross-owner acceptance OPEN |
| Snapshot/Delta/Delivery and Applied | C/G/H | G owns Context version/ChangeSet and Applied decision; C applies only managed region; H transports evidence | PR #487 covers exact-successor in-memory snapshot apply/clear/reconnect only; not delta recovery or production; C/G/H freeze BLOCKED |
| PermissionEpoch and authenticated Principal | C/I/H | Principal is I-trust-derived; protected operations revalidate current I authority | Authority boundary DECIDED; callable integration NOT RUN |
| ForgetFence and revocation | C/D/I/H | D fence/lifecycle and I global policy are consumed; no C-local substitute | Authority boundary DECIDED; exact operation mapping OPEN |
| Replay/idempotency/digest conflict | C/H/E and operation owner | Same identity/same digest replays; same identity/different digest conflicts | Logical semantics DECIDED; per-family schema OPEN |
| Timeout/lost response/cancellation | C/H/E/G | Post-dispatch unknown is UNKNOWN; reconcile before retry; cancellation is not rollback | Architecture specified; Runtime NOT RUN |
| Offline/reconnect/partial delivery | C/D/G/H/I | Governance fences first, then version/capability reconciliation; no stale replay | Architecture specified; cross-owner conformance NOT RUN |
| Protected region/prompt injection | C | Brain-managed region only; untrusted memory remains data; no CoT requirement | Source boundary DECIDED; PR #452 tier/boundary and PR #487 in-memory delivery are bounded reference models only |
| Runtime startup/transport/ACK/validator/concurrency | C/H plus engineering owners | Requires authorized Runtime repository and frozen contracts | PLANNED_NOT_RUN / NOT AUTHORIZED |

All Runtime acceptance rows remain `PLANNED_NOT_RUN / NOT AUTHORIZED`. This document is not Runtime implementation or production conformance evidence.

## 21. Decision register and exact source pins

### 21.1 Decision register

| Item | Status | Evidence / limit |
|---|---|---|
| MCP northbound vs BMCP boundary | DECIDED | Issue #449 comment 7060351480; MCP is C Agent Host interface, BMCP is C Adapter ↔ Brain via H |
| Nine-family routing disposition | DECIDED at family level | Issue #449 comment 7060351480; operation IDs/fields/tool names remain OPEN |
| C Agent identity vs H protocol identity | DECIDED as distinct ownership | PR #430 comment 7061007191 and Issue #449 comment 7061011800; no core `request_id` |
| H logical identity, JCS, ACK/replay and validator principles | DECIDED at logical level only | PR #428 comments 7060190878 and 7060264372; exact schemas/registry/crypto/transport remain OPEN |
| D canonical identity/lifecycle/ForgetFence boundary | DECIDED at semantic boundary | Issue #429 comment 7060243632; no schema/API/wire freeze |
| I Principal/authorization/PermissionEpoch/global Forget boundary | DECIDED at semantic boundary | Issue #429 comment 7060259541; no exact cross-owner wire/API freeze |
| E durable Event receipt/idempotency | CANDIDATE implementation seam | Current main Event Store contract; C/E consumer acceptance not evidenced |
| G ContextVersion/Applied/Forget reconciliation | G semantic decisions recorded; cross-owner freeze BLOCKED | Current main G source pins below; implementation and C/G/H acceptance not verified |
| PR #452 capability-tier reference model | MERGED, bounded reference model only | Merge commit `48a03f694684f7a62bc5b337dc758c98e3cc0e5b`; not MCP/BMCP/Runtime proof |
| PR #487 in-memory context-delivery reference model | MERGED, bounded in-memory behavior only | Merge commit `18b1c574433a6f3f600a9d2947b690084727aa75`; eight unit tests; no transport/durable state/production Runtime proof |
| Issue #7 implementation binding | DEFERRED_TO_ENGINEERING_PHASE | No Runtime implementation authorization |

### 21.2 C source and reader-guide pins at the live-main validation snapshot

Live main snapshot at the start of this rebase/validation batch: `5a1964fa77f6dff024c8cef9e4e6a43f3bd051af`.

| Path | Blob SHA |
|---|---|
| `07-agent-integration/agent-integration-overview.md` | `073ff4ddf71fbcaf959107bb06ab724bfa48e63b` |
| `07-agent-integration/adapter-capability-tiers.md` | `60bce314c36313a14dffe476a6f2a5cf7aa03b37` |
| `07-agent-integration/inference-boundary-model.md` | `e2d5cb6abd9ec40da6e3680531de5944fc8b14df` |
| `07-agent-integration/telemetry-model.md` | `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0` |
| `docs/en/07-agent-integration/agent-integration-guide.md` | `c4e076887634a9e8e46df076efb0f4b70d816e0a` |
| `docs/zh-CN/07-agent-integration/agent-integration-guide.md` | `b68f90f70ccf0c79bc8063e70b9a084b605ba9bf` |

Additional non-canonical translation and implementation-reference pins:
- Chinese capability-tier reader translation: `07-agent-integration/adapter-capability-tiers.zh-CN.md`, Blob `85a77163d1761a38074678983ad8d89ccf25d040`; translation only, not a second source.
- PR #487 reference-model README: `crates/agent-integration/README.md`, Blob `ee68705248f80972232ebf28a4713554f377908e`.
- PR #487 deterministic reference-model implementation: `crates/agent-integration/src/lib.rs`, Blob `125ebfb382a43c8e7ea79b547f86eaa7b611e202`. These are bounded in-memory reference evidence, not production Adapter/Runtime proof.

The four root documents remain the normative C-owned source baseline. The guide pair remains explanatory; it does not replace or duplicate the normative sources.

### 21.3 Current H/G/E source pins and evidence ceiling

| Owner/path | Current Blob SHA | Status/limit |
|---|---|---|
| H `08-bmcp-protocol/protocol-index.md` | `a5b64941cdc783b385348de1b22e0eaace2c003d` | Index now records RecoveryJoin 1.0.2 artifacts; artifact presence is not D proof adoption, production conformance, or a complete C-H operation registry |
| H `08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json` | `bbac8742401249230c629e858d033a09cd8f3acb` | RecoveryJoin 1.0.2 schema/validator/fixtures exist; this does not establish D proof adoption, production conformance, or a frozen C-H operation registry |
| H `08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md` | `d83cde77e98db2e74cf6827d874b0babb4157304` | Version 1.3.0 CANDIDATE |
| H `08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md` | `afa294bc42a8488e4569e6a8bdf5437c7a90e247` | Candidate remediation; exact CI and H/I/D acceptance pending |
| H `08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md` | `7b73491c765091728af6f5306b9efd502cf7f30a` | Resolver reference/tests added; real C ledger resolver and C/G acceptance open |
| H `08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` | `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` | One versioned evidence schema; not a complete family operation registry |
| G `06-memory-context/README.md` | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | Candidate architecture; not frozen cross-owner contract |
| G `06-memory-context/context-versioning.md` | `1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b` | ContextVersion/ChangeSet semantics; candidate encoding/serialization |
| G `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G semantic decisions recorded; C/G/H freeze blocked; implementation not verified |
| G `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | `833815e37ac8d7505d93a0a115421dafe3eb08ad` | G-owned normative design draft; cross-owner acceptance required |
| E `04-memory-compiler/phase-1-event-store-contract.md` | `17b14591d76160a7c125903b41e7dae014c3c5df` | DECIDED semantics / CANDIDATE implementation seam; not proof of C/E MCP acceptance |

D and I exact semantic decisions are pinned to Issue #429 comments 7060243632 and 7060259541 respectively. H logical decision and scope clarification are pinned to PR #428 comments 7060190878 and 7060264372. Those decisions do not freeze the C-H operation registry, exact field schemas, transport or Runtime.

PR #453 is closed/merged into the dedicated `bmcp-validation-base-c588` snapshot branch at merge commit `7c7801db396b92c57ad37020fe170f65f25e43ce`, not into live `main`; its `ARCHITECTURE_PARTIAL / NOT ACCEPTED` review artifact is not a substitute for H's versioned normative wire/operation artifacts. PR #430 is merged into `main` at `0cce40aae5c642f30fabef7b844ac8397322684b`; its three working-copy documents remain Non-Canonical / Informative and do not create a second canonical authority.
### 21.4 Historical 13-section handoff source (input only)

The separately reported 13-section source was recovered from the local Git object store and restored without changing its commit onto `recovery/agent-integration-13-section-source-b5658b0`. GitHub now resolves that recovery branch to commit `b5658b088fade8a15dc78ca9dbde19d2f6753564`. Its three exact source Blobs are:

| Path | Blob SHA |
|---|---|
| `07-agent-integration/agent-integration-architecture-completion.md` | `6c74f09e587017f5e17b1d5ae4589bb724133050` |
| `docs/en/07-agent-integration/agent-integration-architecture-completion.md` | `66ea3514c43f8829f3c9c5d7673c1e3ba03b6590` |
| `docs/zh-CN/07-agent-integration/agent-integration-architecture-completion.md` | `306046a2d47f54219bb2963c232c27767cad372a` |

Recovery status: RECOVERED / CURRENTLY RETRIEVABLE. The condition in PR #430 comment 7061563540 (exact commit and all three Blobs independently readable) is now satisfied; the original commit is unsigned, so no signature verification is claimed. This recovered artifact is an input, not a new canonical document. It is distinct from the three working-copy files in PR #430; those files have different Blob IDs and remain Non-Canonical / Informative. The recovered source's architecture-level content was compared with this overview and the PR #430 working copies. Its accepted boundary and workflow content is represented in §§1–4, 6–8, 16–20 and the decision/source registers. Its future Runtime lifecycle and acceptance-plan sections (§§5 and 9) are explicitly excluded from implementation claims and remain `PLANNED_NOT_RUN / NOT AUTHORIZED`. Its older Owner decision requests (§10) do not override the current Owner rulings. No whole-document copy was promoted or merged as a second authority.
