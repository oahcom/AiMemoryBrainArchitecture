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
        - "07-agent-integration/agent-integration-overview.md"
        - "08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md"
        - "08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md"
        - "06-memory-context/README.md"
        - "https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7"
        - "https://github.com/oahcom/AiMemoryBrainArchitecture/pull/421"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Architecture synthesis from current main and GitHub records; Owner decisions and Runtime conformance remain pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Candidate
    canonical_scope: "Agent Integration: MCP northbound access and BMCP memory-control boundary"
    canonical_scope_id: "agent-integration/mcp-bmcp-architecture-boundary"
    canonical_scope_keywords:
      - agent-integration
      - MCP
      - BMCP
      - server-lifecycle
      - memory-context
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/07-agent-integration/agent-integration-architecture-completion.md"
    zh-CN: "docs/zh-CN/07-agent-integration/agent-integration-architecture-completion.md"
---

# Agent Integration Architecture Completion

- Document ID: AI-INT-ARCH-001 | Version: 0.1.0
- Owner: C — Agent Integration; cross-owner approval pending
- Status: CANDIDATE / NOT FROZEN / NOT IMPLEMENTATION AUTHORITY
- Chinese: [Agent Integration 架构完成说明](../docs/zh-CN/07-agent-integration/agent-integration-architecture-completion.md)
- English mirror: [Reader mirror](../docs/en/07-agent-integration/agent-integration-architecture-completion.md)

## 1. Purpose and status

This document completes the architecture-phase integration description for Agent, MCP (Model Context Protocol) and BMCP (Brain Memory Context Protocol). It proposes the boundary, call path, dependency contract, lifecycle, routing, security and future Runtime acceptance plan. It does not define or amend H-owned BMCP wire fields, transport envelopes, ACK families or validators, and does not authorize Runtime implementation.

Status vocabulary: DECIDED BASELINE = supported by an existing source or explicit Owner direction; CANDIDATE = proposed and awaiting the competent Owner; DEPENDENCY_NOT_FROZEN = upstream contract absent, incomplete or not accepted; NOT RUN / NOT VERIFIED = no executable evidence; PENDING_OWNER_DECISION = no competent Owner ruling is evidenced.

Issue #7 retains IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE. Its latest closeout says it was closed as superseded, not completed; the deferred/not-authorized disposition is not converted into implementation approval here.

## 2. Architecture overview and authority split

### 2.1 Logical topology

    External Agent
      -> Agent Host / MCP Client
      -> MCP Transport (Host-selected, MCP-standard)
      -> Agent Integration Server (northbound MCP endpoint)
         -> MCP method/tool/resource dispatch
         -> identity context propagation (I-authorized)
         -> validation, limits, tracing, error mapping
         -> BMCP Integration Boundary (typed internal adapter seam)
            -> BMCP transport + wire adapter (H-owned; not frozen)
            -> Memory service interfaces
               -> authorized Memory Retrieval (F/runtime service)
               -> Memory domain/store operations (D / Storage)
               -> Memory Context planning (G)
                  -> D publication/dependency gate + I authorization
                  -> H delivery/ACK evidence path

This is a logical dependency graph, not a claim that every component currently exists as a callable service. The repository has a Memory Context planning crate, but no complete Agent Integration Server, no callable end-to-end Memory Retrieval service, and no frozen BMCP Runtime transport.

The existing system architecture also distinguishes the Brain-to-Adapter context-delivery path: G Memory Context Manager creates the authoritative Context version/ChangeSet; the Context Synchronization Engine tracks delivery attempts/status and reconciliation but does not create Context semantics; the H Protocol Gateway/BMCP layer validates and transports the protocol; the C Agent Adapter applies managed Context at the agreed inference boundary; ACK/Applied evidence returns to G through the accepted H/C mapping. This delivery path is related to, but not the same wire protocol as, the northbound MCP tool request/response path.

### 2.2 MCP and BMCP are different layers

| Concern | MCP | BMCP |
|---|---|---|
| Relationship | Agent Host/Client to tool/resource server | Agent Adapter/Runtime to Memory Brain |
| Purpose | Standardized tool and resource interaction between Agent Host and Server | Brain Memory Context Protocol between Memory Brain and Agent Adapters: telemetry, event-ingress references, Context snapshots/deltas, delivery lifecycle, ACK, capability negotiation, Forget/revocation and administrative governance |
| Owns | MCP server lifecycle, methods, tool/resource exposure, MCP request/response and protocol errors | Memory-control message semantics and versioned BMCP contract |
| Transport | Selected according to adopted MCP specification | H-owned BMCP transport binding; not frozen |
| Authority | Does not itself grant access to Brain data | Does not replace I authorization, D lifecycle/Forget or G Context authority |
| Status | Proposed northbound integration; Runtime not implemented | Complete wire/transport/ACK/validator mapping is DEPENDENCY_NOT_FROZEN |

**MCP Server is an access layer, not a substitute for BMCP.** An MCP tool call may map to an internal typed operation; it is not itself a BMCP message. MCP success does not mean BMCP acceptance, delivery, ACK or Applied. BMCP carries domain references and payloads but does not redefine Memory, Claim, Scope, Permission, ContextVersion or Forget semantics; those remain with B/D/G/I. Not every MCP tool call is serialized as BMCP: only operations explicitly crossing the accepted BMCP adapter boundary use H-defined BMCP wire/transport.

Only operations whose backend contract and authorization exist may be exposed. Until BMCP mapping is frozen, operations claiming BMCP delivery/application remain unavailable or return an explicit dependency-not-ready result. No placeholder BMCP message shape may be invented.

### 2.3 Ownership

- Agent / Host: reasoning, planning, task decomposition, action selection, tool invocation, native session state and Agent safety policy.
- Agent Integration (C): Agent-facing compatibility, MCP dispatch mapping, request correlation, validation and response mapping; it does not own H wire contracts.
- MCP Server Runtime: listener/process lifecycle and Model Context Protocol handling; it does not own canonical memory semantics.
- Context Synchronization Engine (Runtime subsystem; exact engineering owner/repository remains an engineering-phase assignment): delivery attempts/status and reconciliation; it does not create Context versions or semantic ChangeSets.
- Protocol Gateway / BMCP (H): authenticated protocol envelope, version/capability negotiation, wire schemas, transport, ACK encoding and validation; it does not interpret semantic truth or own memory.
- Agent Adapter (C): Agent-side integration and inference-boundary application; it does not redefine Brain memory policy or H wire encoding.
- Memory Context (G): desired Context membership, deterministic ordering/budget, Context version and private delivery intent.
- Memory domain/lifecycle (B/D/E/F/Storage): canonical identity, lifecycle, retrieval/activation, production and persistence within each Owner's authority.
- Identity and authorization (I): principal, policy decision, PermissionEpoch, trust and revocation semantics.
- Forget/lifecycle (D): ForgetFence, lineage and lifecycle gate.
- System integration (A): cross-module integration and deployment decision; it does not synthesize another Owner's approval.

## 3. Agent-to-Memory call chain

Logical chain: Agent Client -> MCP Client/Transport -> Agent Integration -> BMCP Integration Boundary -> Memory Services -> Memory Context / Memory Retrieval -> Response Mapping. Every field-level mapping across BMCP remains DEPENDENCY_NOT_FROZEN until H publishes and accepts the relevant versioned contract.

| Node | Owner and input/output | Protocol and data ownership | Security boundary | Failure, retry and timeout |
|---|---|---|---|---|
| Agent Client | Agent/Host; task intent -> MCP request | MCP client message; Agent owns task/session state | Host authenticates server and applies tool-consent policy; Agent-supplied identity is not authority | If side effect may have crossed boundary, timeout means unknown; retry only with same operation identity when backend supports idempotency |
| MCP Client/Transport | MCP Host/Runtime; request frames -> parsed MCP envelope | MCP transport only, not BMCP wire | Transport identity feeds I authorization but does not replace it | Pre-dispatch connection failure may retry; after dispatch reconcile before retry; timeout is not rollback |
| Agent Integration Server | C boundary/future Runtime; MCP envelope -> validated typed command -> MCP result/error | MCP methods/tools/resources and internal command; owns request correlation, not memory records | Validate method, schema, size, deadline, caller identity and tool allowlist before data access | Bound concurrency; per-request deadline; propagate cancellation; isolate exceptions; never auto-retry non-idempotent writes |
| BMCP Integration Boundary | C consumer adapter; H protocol authority; typed command -> H-defined BMCP operation -> typed result | Internal seam is candidate; wire/version/ACK/transport are H-owned | Bind authenticated principal/scope and authorization evidence; reject unsupported version/capability; infer no fields or aliases | DEPENDENCY_NOT_FROZEN: no send/retry until H contract pinned; then use only H-defined idempotency/replay/reconciliation |
| Memory Services | D/F/E/Storage by operation; authorized request -> domain result or durable receipt | Owner-defined interfaces; generic MCP/BMCP payload does not become canonical by itself | I authorization before protected read/write; D lifecycle/Forget checks before visibility/mutation | Unknown commit/ACK: query same operation/receipt; no blind second write; preserve owner and operation identity |
| Memory Context / Retrieval | G plans Context; F/runtime owns retrieval; candidates + identity/budget -> staged snapshot, or scoped query -> qualified memory | Current G crate builds deterministic snapshot/private non-sendable intent; it is not a retrieval service | Scope, lifecycle, lineage, evidence and budget checks; builder itself does not authenticate, authorize or query D/I | Invalid scope/lifecycle/lineage/budget fails closed; stale Context/Forget/Permission requires owner reconciliation |
| Response Mapping | C boundary/future Runtime; typed result -> MCP result/error | MCP response envelope; preserve backend state/evidence without inventing BMCP fields | Redact secrets and inaccessible references; do not disclose cross-scope existence | Distinguish malformed MCP, denial, dependency unavailable, domain rejection, unknown timeout and internal failure |

### 3.1 Retry and timeout invariants

1. Timeout is not proof of failure; cancellation request is not proof of rollback.
2. Missing ACK is not proof that a remote operation did not commit.
3. A retryable mutation reuses the same owner-defined operation/idempotency identity and reconciles before creating another logical operation.
4. No exactly-once claim may be made from MCP request ID, HTTP status, transport connection or trace ID.
5. Trace ID, MCP request ID, BMCP operation identity, provider attempt identity and domain record identity remain distinct.
6. Runtime establishes an absolute deadline or remaining-time budget; downstream calls may shorten but not extend it. Concrete durations are deployment/SLO decisions.
7. Cancellation propagates to cancellable work. Non-cancellable or committed work is reconciled and reported unknown/in-progress, not falsely rolled back.

## 4. BMCP integration dependency contract

### 4.1 H-owned boundary

H owns authoritative BMCP wire and transport contracts: versioned message schemas/families; transport envelope, connection/session and reconnect; ACK families and exact receipt/acceptance/delivery/Applied meanings; validator behavior and negative vectors; replay, duplicate, ordering and protocol error semantics.

Agent Integration may define consumer requirements and typed internal interfaces. It MUST NOT add/rename H fields, invent URI semantics, equate similar field names, or treat candidate schemas as frozen.

### 4.2 Current dependency status

| Dependency | Evidence on current main / GitHub | Disposition |
|---|---|---|
| Agent Integration logical boundary | C overview, capability tiers, inference-boundary and telemetry models exist | Baseline exists; this document adds candidate MCP-facing architecture |
| Model Context Protocol Runtime/source docs | No separate MCP-specific guide, SDK integration or Runtime implementation path found in current main; current protocol guide is specifically BMCP | MCP Server remains architecture proposal; no SDK/version/transport is claimed implemented |
| Identity binding | H Phase 3.6 identity record says technical protocol-binding design is JOINT-DECIDED; C/F/G consumer acceptance remains OPEN, external governance approval is GOVERNANCE-BLOCKED, and H36 tests are NOT RUN | Not production authentication/conformance; exact consumer acceptance and runtime evidence remain pending |
| Applied Delivery Evidence | Main contains H Applied Delivery Evidence 1.0.0 schema, validator and conformance tests; H addenda 3.8.25/3.8.26 describe candidate hardening | Candidate evidence family only; not complete BMCP mapping or production trust |
| Complete message-family mapping | Issue #3 history records unresolved eight-family causal-order mapping gaps; it was closed as superseded, not technical acceptance | DEPENDENCY_NOT_FROZEN; refresh controlling successor artifacts and H decision |
| H transport binding | No accepted complete Agent Integration transport binding identified in current main source set | DEPENDENCY_NOT_FROZEN |
| ACK/replay/reconnect | Candidate Applied evidence exists; production durable replay, live adapter integration and cross-owner acceptance remain open in H addenda | DEPENDENCY_NOT_FROZEN |
| Validator/trust | Candidate validator/fixtures exist; they do not establish H production trust roots, registered profile/key lifecycle or durable replay | DEPENDENCY_NOT_FROZEN |
| MCP-to-BMCP mapping | No approved mapping specification found in current main | Candidate internal seam only; no wire conversion rules assumed |

H addenda explicitly leave live C ledger/signature verification, production trust roots, durable replay, crash-safe reservation and Runtime Adapter integration open. Issue #3 history states that Applied Delivery Evidence and JF-10 schemas do not automatically satisfy the separate eight-family causal-order mapping. Closing Issue #3 as superseded does not turn those gaps into approval.


### 4.3 Logical BMCP families and delivery truth

The current H-owned BMCP architecture guide lists these nine logical message families. This is a family inventory only; it does not freeze field names, wire schemas, transport framing or version negotiation.

| Family | Direction in H guide | Purpose |
|---|---|---|
| Telemetry | Adapter -> Brain | Structured Agent observations and outcomes |
| Event Ingress | Producer -> Brain | Typed source Events with provenance/idempotency references |
| Context Snapshot | Brain -> Adapter | Complete managed Context view at a target version |
| Context Delta | Brain -> Adapter | Atomic ChangeSet from exact base to target version |
| Delivery | Brain -> Adapter | Bind snapshot/delta to recipient/session and delivery lifecycle |
| Acknowledgement | Adapter -> Brain | Report lifecycle state and evidence |
| Capability Negotiation | Bidirectional | Negotiate protocol versions, families, limits and proof tiers |
| Forget / Revocation | Brain/I -> Adapter | Invalidate managed content, sessions, queued work and stale offline state |
| Administrative Governance | I/control plane -> Adapter/Gateway | Carry policy epochs, revocation, recipient scope and control directives |

The H guide distinguishes Prepared, Delivered, Applied, Rejected, Expired, Superseded and Unknown. These states are not interchangeable: Delivered is not Applied, and Applied does not prove model attention or comprehension. Only a Tier 1 final-request-observable Adapter may emit Full Applied, and only when every approved per-request predicate passes; Tier 2 and Tier 3 MUST NOT claim Full Applied.

Issue #3 history uses the phrase eight-family causal-order mapping gap for its historical workset. That wording is not an assertion that the current H guide lists only eight logical families; the current guide lists nine. Exact mapping/version acceptance remains H-owned and open.

### 4.4 BMCP URI and transport semantics

- Agent Integration sources do not define bmcp:// as a complete URI scheme. Authority, grammar, default port, path semantics, discovery, authentication, TLS, framing, error mapping and client implementation are unspecified.
- BMCP is an application-level memory-control protocol, not a URI scheme or transport.
- HTTP, if selected by H, is a separate transport binding/adapter. An HTTP endpoint does not itself prove BMCP conformance.
- MCP transport is selected independently. An MCP Streamable HTTP endpoint is not automatically a BMCP HTTP endpoint.
- A client opening bmcp:// requires a URI-scheme adapter mapped to a specified transport and implemented client handler. No such adapter is claimed to exist.
- Ordinary curl cannot claim bmcp:// validation unless the exact curl build demonstrably supports a registered/custom bmcp handler. Standard HTTP curl validates only the HTTP endpoint.
- Future tests must exercise the selected BMCP client/transport against H-pinned schema/validator and assert semantic request/ACK/replay behavior. HTTP 200 alone is insufficient.

No health path, BMCP URI response body, envelope or transport mapping is frozen here.

## 5. Future Runtime server lifecycle contract

This is a Runtime obligation, not an implementation claim.

| Stage | Required behavior | Evidence |
|---|---|---|
| start | Validate config; initialize handlers/dependencies; bind listener; report success only after bind and required startup checks succeed | Bound socket/address, startup result, dependency readiness and logs |
| startup failure | Actionable typed errors for address, permission, port conflict, TLS/config, handler or dependency failure; release partial resources | Failure injection; no false-ready state |
| request dispatch | Admit supported MCP methods; establish request context, principal, scope, deadline and trace; validate before service call | Method traces and malformed-input tests |
| health | Separate process liveness from dependency/protocol readiness; HTTP liveness proves only process/HTTP handler response | Independent liveness/readiness tests; BMCP readiness needs H-defined protocol probe |
| concurrency | Bound in-flight requests; isolate request state; enforce per-principal/resource limits | Load/race tests; no cross-request leakage |
| timeout/cancellation | Enforce deadline; propagate cancellation; distinguish cancellation request from rollback | Deterministic timeout/cancellation-race traces |
| graceful shutdown | Stop accepting; drain in-flight requests to deadline; cancel/terminate remaining work under explicit policy; close listeners/resources | Drain test and listener/port release check |
| repeated shutdown | Idempotent or stable already-closed result; no double-release/panic | Repeated shutdown test |
| post-shutdown | Reject new requests; expose closed state; no listener remains bound | Connection failure and successful socket rebind |

### 5.1 Health state model

Future Runtime must distinguish process liveness, MCP readiness, memory dependency readiness and BMCP readiness. BMCP readiness requires H-defined transport negotiation and a protocol-level probe against a pinned version. HTTP /health 200 may indicate process liveness only. It MUST NOT be represented as BMCP readiness, authorization success, Memory Context publication, ACK or Applied.

Actual path names and response schema are Runtime decisions after repository and deployment authorization. Do not hardcode success.

## 6. Request routing and error contract

### 6.1 Routing stages

1. Parse transport frame and MCP envelope.
2. Reject malformed framing/JSON, unsupported protocol version or invalid method before Brain data access.
3. Resolve authenticated principal and scope from trusted Host/transport identity; do not trust caller-supplied principal/tenant labels.
4. Authorize the tool/resource operation using I-owned policy semantics.
5. Validate tool name, resource URI, argument shape, size, deadline and supported capability.
6. Map to a typed internal command. Serialize as BMCP only after H freezes the corresponding family.
7. Invoke the owning Memory service and preserve D/I/G/Storage result identity/evidence.
8. Map to MCP result without changing semantic state.

### 6.2 Error classes

| Failure | Boundary | Required behavior |
|---|---|---|
| Malformed transport/MCP envelope | MCP transport/server | MCP/transport-defined invalid request; no service call |
| Unknown MCP method | MCP dispatcher | MCP-defined method-not-found |
| Unknown tool/resource | MCP dispatcher | Explicit not-found/unsupported; no fallback |
| Invalid tool arguments | Agent Integration | Parameter validation error; no backend side effect |
| Authentication/authorization denied | I boundary | Deny before protected access; sanitized denial |
| PermissionEpoch changed | I currentness | Re-authorize under I semantics; no stale authorization reuse |
| ForgetFence conflict/stale lineage | D lifecycle | Suppress/reject protected operation; no local override |
| Unsupported BMCP version/family | H protocol | Explicit unsupported result; no silent downgrade |
| BMCP validator rejection | H validator | Preserve failure/evidence; do not reinterpret as success |
| BMCP ACK missing/timeout after send | H transport + operation ledger | UNKNOWN/IN_DOUBT until same-operation reconciliation; no blind retry |
| Memory service unavailable | Owning service | Dependency unavailable; retryable only if operation semantics prove safe |
| Internal exception/panic | Runtime | Isolate request, redact internals, trace safe error class; keep server alive where possible |

Malformed MCP envelopes and valid MCP tool invocations denied by domain authorization are distinct. A domain denial is not malformed JSON-RPC. Exact error codes follow the adopted MCP version and H BMCP definitions; this document invents no BMCP error codes.

## 7. Security and isolation contract

1. Agent, Agent instance, user/tenant/workspace/project, session, task and environment are distinct typed identities. A request body cannot self-assert authenticated identity. A caller-constructed ActorRef is not proof of authentication; H binds the authenticated transport principal and I defines trust policy.
2. I owns PermissionDecision, PermissionEpoch, trust, revocation and global Forget governance policy. Agent Integration consumes I's authoritative decision/currentness; it does not mint, indefinitely cache or locally reinterpret permission.
3. PermissionEpoch changes invalidate cached authorization for protected operations. Revalidation follows I ordering/currentness; local timestamp comparison is not a substitute.
4. D owns the canonical ForgetOperation, target references, ForgetFence generation, lineage and D-domain ordering. I owns initiation/approval authority, cross-system target-inventory policy, evidence-acceptance criteria, retention/legal-hold/backup policy and global governance evaluation; I does not redefine D-domain completion. Protected memory candidates, context publication and late results honor D's current fence. Agent/MCP callers cannot bypass it by resubmitting.
5. Scope is not permission. Resolve and authorize scope before retrieval; missing required scope dimensions are deny/indeterminate, never wildcard. Test cross-tenant, cross-agent, cross-session and confused-deputy attempts.
6. Agent telemetry, memory text, resource content, tool descriptions and annotations are untrusted data, not instructions. Retrieved memory cannot elevate itself to System/Developer authority or authorize a tool.
7. Exposing an MCP tool does not authorize execution. Host consent and I/tool-host policy authorize invocation and data access at the actual execution boundary.
8. Principal, scope, deadline, cancellation token and trace context are request-local. No mutable authorization or memory state is shared across requests without an explicit concurrency-safe contract.
9. Do not log raw memory content, secrets, credentials, prompt bodies or private reasoning by default. Log stable references and bounded diagnostics under I privacy/retention rules.
10. External errors disclose no secret, cross-scope resource existence, key material, raw stack trace or trust registry detail.
11. Replay/idempotency uses only owner-defined operation identity and replay rules. MCP request IDs and trace IDs are not idempotency keys.
12. Propagate causal trace links while keeping identity domains distinct. Authorization references and validator outcomes are evidence, but trace correlation is not authority.

## 8. Memory Context integration matrix

### 8.1 Verified PR #421 outcome

PR #421 is merged, not Draft:

- PR: [#421 feat(memory): implement Memory Context](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/421)
- Head commit: 0a4e84276fbcdb94f8efff33d881becc5be460a4
- Merge commit: d381e7a1fc17bea1dd14be54e8dfd497e8ca2e83
- Current main observed in this follow-up: 277daec7d0c6b5c93d785e9e9c7fd63889827c8f
- Changed files: Cargo.toml; crates/memory-context/Cargo.toml; crates/memory-context/src/lib.rs.

The merged crate provides deterministic scoped Context snapshot planning and a private non-sendable DeliveryIntent. Its builder accepts ContextIdentity, ContextBudget and already-provided ContextCandidate values. It validates scope membership, Active/Consolidated lifecycle, lineage, duplicate entries/memberships and entry/byte budgets, then orders candidates deterministically and serializes the staged snapshot.

The crate does not authenticate, authorize, query D/I, perform Memory Retrieval, persist an authoritative Context version, publish a visible Context head, send BMCP or produce Applied ACK. DeliveryVisibility has only PrivatePendingPublicationGate. The PR body says D producer/dependency/final-publication and I authorization interfaces are not exposed.

### 8.2 Dependency matrix

| Need | Memory Context provides now | Missing contract | Integration rule |
|---|---|---|---|
| Context identity/scope | ContextIdentity with Context, Agent, Agent instance, Session, optional Task/Environment and ScopeRefs | Authoritative principal/permission binding remains I-owned | Identity fields are not authentication/authorization |
| Candidate memory data | ContextCandidate input type | Authorized candidate retrieval API is not exposed by memory-context crate; identify retrieval owner/service | Pass only candidates from an independently authorized read path |
| Context planning | build_context with deterministic ordering and lifecycle/scope/lineage/budget checks | Cross-owner currentness and authoritative persistence | Treat result as staged snapshot only |
| Delivery | Serialized DeliveryIntent, fixed PrivatePendingPublicationGate | D publication/dependency/final gate, I authorization, H BMCP delivery/ACK | Do not send or expose as delivered |
| Applied result | No Applied record or ACK | G Applied authority and H evidence mapping | Never infer Applied from snapshot creation, MCP success or HTTP 200 |
| Retrieval response | No retrieval endpoint in this crate | F/runtime retrieval contract and I authorization | Builder is not Memory Retrieval implementation |

### 8.3 Required integration sequence

1. Obtain scoped candidates from an authorized retrieval service that applies I authorization and D lifecycle/Forget constraints.
2. Build a staged snapshot with G API; preserve Context identity, version, lineage and budget outcomes.
3. Obtain D producer/dependency registration and final publication gate plus I authorization through authoritative interfaces.
4. Only after those gates succeed prepare a sendable delivery operation under G/H accepted contracts.
5. H-defined BMCP transport sends the versioned delivery and validates ACK/evidence.
6. G records authoritative Context/Applied result using exact H/C boundary evidence and currentness rules.
7. Agent Integration maps the result to MCP without promoting receipt/acceptance to Applied.

Steps 3–6 are not available as a complete callable path in the current workspace. This is an architecture dependency, not a present-functionality claim.

## 9. Future Runtime acceptance plan

**All scenarios are NOT RUN.** These are acceptance requirements, not test results. BMCP cases are blocked until H publishes and relevant Owners accept the exact contract version.

| ID | Scenario | Agent Integration responsibility | H responsibility | Joint/external dependency | Evidence/status |
|---|---|---|---|---|---|
| RT-01 | Server startup | Validate config, bind listener, register MCP dispatch; no success before bind | N/A | Runtime environment | Bound socket/startup trace; NOT RUN |
| RT-02 | Port bind failure | Actionable startup error; release partial resources | N/A | OS/network | Failure log, no false readiness; NOT RUN |
| RT-03 | Health check | Separate liveness, MCP readiness and dependency readiness | Define BMCP probe after transport freeze | Runtime + H | HTTP liveness is not BMCP PASS; NOT RUN |
| RT-04 | MCP initialize/request | Implement adopted MCP version/method lifecycle | N/A | MCP conformance suite | Valid transcript; NOT RUN |
| RT-05 | BMCP request forwarding | Map typed command without inventing fields | Define family/schema/transport/validator | C/H mapping | Exact H-version request; BLOCKED / DEPENDENCY_NOT_FROZEN |
| RT-06 | BMCP ACK | Preserve ACK state and same-operation correlation | Define ACK family/semantics/ordering/replay | G/D/Storage reconciliation | Positive/negative/replay vectors; BLOCKED |
| RT-07 | BMCP validator | Invoke pinned validator; reject invalid payload | Own validator and canonical errors | H + consumer review | Schema/validator negative vectors; BLOCKED |
| RT-08 | Concurrent requests | Bound concurrency and isolate request context | Define transport/session concurrency if applicable | I scope isolation | Race/load test; NOT RUN |
| RT-09 | Timeout | Enforce deadline; return unknown if outcome uncertain | Define transport timeout/ACK semantics | Operation ledger | Same-operation reconciliation; NOT RUN |
| RT-10 | Cancellation | Propagate cancellation; do not claim rollback | Define protocol-level cancellation if any | D/Storage/provider side-effect owner | Cancel-vs-complete trace; NOT RUN |
| RT-11 | Graceful shutdown | Stop accept, drain/cancel, close listener/release port | N/A | Runtime | Drain and port-rebind proof; NOT RUN |
| RT-12 | Authorization denied | Deny before protected access; redact response | Carry identity evidence only as H defines | I policy | Denial decision/no-read proof; NOT RUN |
| RT-13 | PermissionEpoch change | Invalidate cached authorization and recheck | Bind protocol evidence only as H defines | I currentness | Stale-epoch rejection; NOT RUN |
| RT-14 | ForgetFence conflict | Stop/suppress protected use | Carry D fence evidence only as H defines | D fence/lineage; G currentness | Fence race/stale suppression; NOT RUN |
| RT-15 | Invalid protocol request | Reject malformed MCP envelope; do not route to memory | Reject invalid BMCP schema/version | MCP + H | Separate negative tests; NOT RUN |
| RT-16 | Unsupported protocol version | Report at correct protocol layer | Define BMCP negotiation/fallback | H + Runtime | No silent downgrade; BMCP BLOCKED |
| RT-17 | Unknown method/tool/resource | MCP method-not-found/explicit failure | N/A unless mapped BMCP op | MCP Runtime | Protocol-correct negative response; NOT RUN |
| RT-18 | Cross-tenant/confused deputy | Enforce request-local principal/scope | Preserve authenticated identity binding | I and adapter security | Adversarial isolation suite; NOT RUN |
| RT-19 | Context publication | Do not send private DeliveryIntent | Define delivery envelope/ACK | G + D + I + H | Gate evidence before send; BLOCKED |
| RT-20 | Applied truthfulness | Do not map receipt or MCP success to Applied | Validate H evidence family | C/G/H and I trust | Final-boundary/Applied join; BLOCKED |

### 9.1 Acceptance gates

- Gate A — MCP Runtime: startup, dispatch, health, concurrency, timeout, cancellation, shutdown and MCP conformance pass on the authorized Runtime repository.
- Gate B — BMCP contract: H publishes versioned schemas, transport, ACK, validator, error, replay and reconnect; H Owner decision and consumer mappings are recorded.
- Gate C — security/lifecycle: I approves identity/PermissionEpoch/trust; D approves ForgetFence/lineage; negative tests prove fail-closed behavior.
- Gate D — Memory Context end-to-end: authorized retrieval, G planning, D/I publication gates, H delivery/ACK and G Applied evidence join using exact identities and durable reconciliation.
- No gate is PASS because a design document exists. Runtime/BMCP gates remain NOT RUN or BLOCKED until reproducible evidence exists.

## 10. Owner decision requests

These requests seek decisions only within the named authority's scope. They do not sign for H, D, I, G or A.

### DECISION_REQUEST_ID: AI-INT-DR-001

- MODULE: Agent Integration
- ISSUE_OR_ADR: Existing Agent Integration baseline; H/BMCP sources under 08-bmcp-protocol; Issue #3 history is closed as superseded, not technical acceptance.
- DECISION_REQUIRED: H identifies and approves exact BMCP message-family, transport, ACK, validator, replay and reconnect contract versions for Agent Integration consumers.
- CURRENT_FACTS: Current main has Applied Delivery Evidence 1.0.0 candidate family and hardening addenda; complete cross-owner wire mapping and production trust are not established.
- DEPENDENCY_ON_H: Authoritative; H publishes exact version/Blob pins and wire/transport/ACK/validator decisions.
- DEPENDENCY_ON_D: ForgetFence and lineage fields/ordering remain D-owned; H fields do not redefine them.
- DEPENDENCY_ON_I: Authenticated identity, trust profile and PermissionEpoch remain I-owned; H does not grant authorization.
- MCP_BMCP_BOUNDARY: MCP dispatch maps to typed internal operation; BMCP serialization only through H-pinned contract.
- OPTIONS: A wait for complete H contract; B implement only MCP operations that do not claim BMCP behavior; C invent provisional BMCP payload. C is rejected.
- RECOMMENDED_OPTION: A for BMCP-dependent operations; B only for explicitly bounded MCP-only health/capability endpoints.
- RUNTIME_IMPLEMENTATION_IMPACT: No BMCP sender, URI handler, ACK parser or validator integration before H freeze.
- REQUIRED_AUTHORITY: H Owner; C consumer acceptance; affected D/I/G Owners for their own bindings.
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: Current main H addenda 3.8.25/3.8.26; BMCP guide DOC-BMCP-001 remains CANDIDATE; H Phase 3.6 identity-binding consumer status leaves C/F/G acceptance OPEN and governance approval BLOCKED; Issue #3 historical mapping gap; PR #428 is an open Draft candidate only.
- FOLLOW_UP_ACTIONS: H publishes exact pins; C records consumer mapping; affected Owners accept their bindings.

### DECISION_REQUEST_ID: AI-INT-DR-002

- MODULE: Agent Integration
- ISSUE_OR_ADR: I authorization contract and D ForgetFence/currentness contract; Issue #7 engineering-entry handoff.
- DECISION_REQUIRED: I and D identify exact callable authorization/currentness interfaces and required evidence at read, delivery, publication and late-result boundaries.
- CURRENT_FACTS: Agent Integration needs PermissionEpoch revalidation and ForgetFence/lineage enforcement; current Memory Context builder does not call I or D.
- DEPENDENCY_ON_H: H may carry references/evidence only as H specifies; it does not define I/D authority.
- DEPENDENCY_ON_D: D decides fence token, lineage, ordering and protected lifecycle gate.
- DEPENDENCY_ON_I: I decides principal, PermissionDecision, PermissionEpoch, trust, revocation and currentness.
- MCP_BMCP_BOUNDARY: Authenticated identity propagates from MCP Host/transport into internal command; BMCP binds it only through H-accepted representation.
- OPTIONS: A use exact callable I/D interfaces after publication; B block protected operations until interfaces exist; C synthesize epoch/fence semantics locally. C is rejected.
- RECOMMENDED_OPTION: B until A is evidenced.
- RUNTIME_IMPLEMENTATION_IMPACT: No protected retrieval/send/publication based solely on caller identity, cached permission or local fence approximation.
- REQUIRED_AUTHORITY: I Owner and D Owner independently; C/H/G consumers review their own bindings.
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: Agent Integration security boundary; merged PR #421 code/body; I Security Governance Guide and Scope/Permission Model; D/I authority statements.
- FOLLOW_UP_ACTIONS: I/D publish exact interfaces and test vectors; Runtime entry plan pins them without changing semantics.

### DECISION_REQUEST_ID: AI-INT-DR-003

- MODULE: Agent Integration
- ISSUE_OR_ADR: Runtime implementation entry / Issue #7.
- DECISION_REQUIRED: Owner and accountable engineering leadership authorize canonical Runtime repository/branch, maintainers, build/CI, deployment topology and MCP/BMCP transport implementation location.
- CURRENT_FACTS: Issue #7 preserves IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE and is closed as superseded, not completed. Current repository is architecture-definition scope.
- DEPENDENCY_ON_H: H must supply frozen BMCP transport/protocol contracts before BMCP Runtime implementation.
- DEPENDENCY_ON_D: D callable lifecycle/Forget interfaces and operational ownership are required for protected write/publication.
- DEPENDENCY_ON_I: I callable identity/authorization interfaces and trust/key operations are required.
- MCP_BMCP_BOUNDARY: MCP Server is northbound Agent tool interface; BMCP is a separate southbound memory-control protocol.
- OPTIONS: A designate existing canonical Runtime repository; B explicitly authorize a separate Runtime repository; C add placeholder Runtime code here. C is rejected.
- RECOMMENDED_OPTION: Engineering authority explicitly selects A or B; preserve architecture-only repository boundary.
- RUNTIME_IMPLEMENTATION_IMPACT: No Runtime Server, listener, bmcp:// handler or production activation in this repository.
- REQUIRED_AUTHORITY: Project Owner and accountable engineering leadership; A coordinates traceability.
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: Issue #7 latest superseding closeout; current repository main inventory and README scope.
- FOLLOW_UP_ACTIONS: Owner names repository/branch and engineering owners; engineering lead supplies build/test/deployment and artifact provenance plan.

## 11. Engineering-phase handoff checklist

Runtime entry remains pending until all are recorded:

1. H-approved BMCP message-family, wire, transport, ACK, validator, error, replay and reconnect contracts with exact version/Blob pins.
2. Explicit MCP version/transport and MCP-to-internal-command mapping; no MCP/BMCP conflation.
3. I-approved identity, PermissionDecision, PermissionEpoch, trust, revocation and key lifecycle interfaces.
4. D-approved ForgetFence, lineage, ordering and publication/lifecycle gate interfaces.
5. G-approved Context identity/version/Applied consumer binding and H evidence mapping.
6. Canonical Runtime repository/branch, accountable maintainers, write authority and explicit implementation authorization.
7. Build system, pinned dependencies, CI workflows, reproducible test commands and artifact/build SHA source.
8. Test/service topology, secret/key custody, logging/retention, monitoring, on-call, rollback and deployment authorization.
9. Convert Runtime acceptance matrix into executable tests with owner-specific fixtures and deterministic evidence.
10. Independent cross-owner review and Owner approval; proposal status is not production readiness.

## 12. Source inventory and traceability

Verified current-main source set:

- 07-agent-integration/agent-integration-overview.md
- 07-agent-integration/adapter-capability-tiers.md
- 07-agent-integration/inference-boundary-model.md
- 07-agent-integration/telemetry-model.md
- 01-system-architecture/system-overview.md
- 01-system-architecture/component-map.md
- 01-system-architecture/component-interactions.md
- 01-system-architecture/data-flows.md
- 01-system-architecture/responsibility-matrix.md
- 08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md
- 08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md
- docs/en/08-bmcp-protocol/bmcp-guide.md
- docs/en/08-bmcp-protocol/adapter-capability-and-applied-attestation.md
- docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md
- 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md
- 08-bmcp-protocol/phase-3.8-h-rj-hw-01-typed-watermark-and-fence-binding-contract.md
- 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
- 08-bmcp-protocol/validators/applied_delivery_evidence_validator.py
- 08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py
- 06-memory-context/README.md
- docs/en/02-domain-model/scope-and-permission-model.md
- docs/en/09-security-governance/security-governance-guide.md
- docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md
- 13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-validation-plan.md
- docs/architecture-convergence/ARCH-CONVERGENCE-001-CONTRACT-DEPENDENCY-MAP.md
- crates/memory-context/Cargo.toml
- crates/memory-context/src/lib.rs
- 00-governance/architecture-document-management-policy.md
- 00-governance/bilingual-documentation-policy.md

Related GitHub records:

- [Issue #7 — implementation entry; closed as superseded, deferred disposition retained](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7)
- [Issue #3 — historical C/G/H wire decision record; closed as superseded, not technical acceptance](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/3)
- [PR #421 — Memory Context, merged](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/421)
- [PR #428 — BMCP architecture contract, open Draft](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/428); review candidate only, not merged and not treated as H approval or a frozen BMCP contract.
- [Issue #381 — delegated-grant adapter-isolation follow-up, closed](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/381)
- [Issue #348 — REQ-08 interoperability proposal, closed](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/348)

This is an Informative/Candidate proposal. It does not supersede C source architecture, H BMCP contracts, G Context authority, D lifecycle, I authorization or Issue #7 disposition.

## 13. Final architecture disposition

- MCP/BMCP conceptual boundary: candidate definition; Owner confirmation pending.
- Agent-to-Memory call chain and ownership: documented; some upstream interfaces remain unavailable.
- H BMCP contract: DEPENDENCY_NOT_FROZEN.
- Memory Context: foundation merged; publication/delivery/Applied chain unavailable.
- Server lifecycle and routing: proposed contract; Runtime not implemented.
- Security dependencies: I/D authority preserved; callable integration not verified.
- Runtime acceptance: plan only; all tests NOT RUN.
- Issue #7: IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE.
- Production activation: not authorized by this document.
