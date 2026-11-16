# BMCP Protocol Overview

- Workstream: Session H — BMCP Protocol & Agent Context Adapter
- Protocol name: Brain Memory Context Protocol (BMCP)
- Status: **CANDIDATE architecture; dependent contract elements remain OPEN / ADR-BLOCKED**
- Owner: Session H
- Branch baseline: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
- Scope: wire envelope, protocol versioning, serialization, transport interaction, Adapter SDK, delivery/application acknowledgement and final-request attestation.

## 1. Authority and non-goals

H owns the wire contract and Adapter-facing protocol behavior. H does not own:
- Canonical Memory, Fact/Claim, Evidence, Entity, Relation, or lifecycle semantics (B/D).
- Context membership, ordering, budget, ContextVersion, or ContextChangeSet semantics (G).
- Retrieval ranking, freshness, or index watermark authority (F).
- Global Principal, authorization policy, grants, retention, audit policy, or Forget completion policy (I).
- Agent reasoning, planning, tool invocation, or Agent safety policy (C / Agent).

BMCP transports references and opaque domain payloads; it does not redefine their meaning. The Agent continues to operate if the Brain is unavailable, subject to Agent policy. BMCP cannot rewrite hidden provider prompts, provider-retained request copies, model internals, or model attention.

## 2. Normative vocabulary

The terms MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are used normatively.

- **Prepared**: Adapter has validated and staged a delivery but has not confirmed transport delivery.
- **Delivered**: transport endpoint accepted the delivery for the addressed Adapter. This is not application.
- **Applied**: Adapter attests to an explicitly defined application coverage at an inference boundary.
- **Rejected**: recipient explicitly refused the operation with a classified reason.
- **Expired**: operation passed its validity deadline without valid completion.
- **Superseded**: a newer authoritative Context target or governance epoch makes this operation obsolete.
- **Unknown**: outcome cannot be established, e.g. timeout, process loss, or offline state.

No protocol status implies another status unless an explicit transition and evidence are recorded. In particular, Delivered MUST NOT be interpreted as Applied; Applied MUST NOT be interpreted as model attention or use.

## 3. Message families

| Family | Direction | Purpose | Authority / dependency |
|---|---|---|---|
| Telemetry | Adapter → Brain | Agent observations, outcomes, intent, plan summaries, tool/environment events | C owns event semantics; I owns authenticated identity; E owns durable acceptance |
| Event Ingress | Producer → Brain | Submit a typed source Event with idempotency and provenance references | E owns durable receipt/processing; D owns canonical commit |
| Context Snapshot | Brain/Gateway → Adapter | Replace the complete managed Context view at a declared target version | G owns snapshot content and ContextVersion |
| Context Delta | Brain/Gateway → Adapter | Apply an atomic change set from an exact base to target version | G owns ChangeSet/CAS semantics |
| Delivery | Brain/Gateway → Adapter | Bind a snapshot/delta to a recipient, session and delivery lifecycle | G owns delivery intent; H owns wire and transport |
| Acknowledgement | Adapter → Brain | Report Prepared/Delivered/Applied/Rejected/Expired/Superseded/Unknown and evidence | H owns wire; G consumes delivery state |
| Capability Negotiation | Bidirectional | Negotiate supported protocol versions, message families, limits and proof tiers | H owns capability vocabulary; I-owned policy remains external |
| Forget / Revocation Notification | Brain/I → Adapter | Invalidate managed content, sessions, queued work and stale offline state | D owns canonical Forget fence; I owns global policy; G owns Context reconciliation |
| Administrative Governance Envelope | I/authorized control plane → Adapter/Gateway | Carry policy epoch, revocation, recipient scope and administrative control metadata | I owns authorization/policy meaning; H only encodes and transports |

Telemetry and Event Ingress are separate logical families even if an implementation shares a transport endpoint. A telemetry report is not automatically a canonical Event or Memory.

## 4. Protocol layering

1. **Authenticated transport** establishes a cryptographically authenticated peer / workload principal and channel properties.
2. **BMCP envelope** carries message identity, protocol version, routing, causal links, timestamps, payload type, integrity metadata and expiry.
3. **Family payload** carries a typed operation or opaque owner-defined object.
4. **Domain authority** validates semantics and authorization at the receiving boundary.
5. **Application boundary** is controlled by the Adapter and Agent integration, and is separately attested.

The authenticated transport principal is supplied by the transport/security integration, not by a payload field. A payload `ActorRef`, `producer_id`, `agent_id`, or display name is an assertion/selector only. It MUST be compared with authenticated binding and I's current policy before use. Payload identity never authenticates itself.

## 5. Core processing principles

- Every state-changing request has a stable message ID and an explicit idempotency scope/key.
- Correlation IDs group a workflow; causation IDs identify the immediate message/event that caused this message. Neither replaces an idempotency key.
- Context deltas are applied atomically against an exact G-owned base version. Base mismatch triggers rejection or full-snapshot reconciliation; never best-effort patching.
- Stale versions, stale Forget fences, stale permission epochs and stale capability epochs are rejected or superseded before application.
- Adapter local buffers are not proof of final inference application.
- An offline Adapter cannot acknowledge current application. On reconnect it must process governance fences before accepting context replay.
- Memory payloads are untrusted data and are restricted to the managed memory region. They cannot modify protected instructions, user input, Agent policy, tool definitions, or tool authorization.

## 6. Conformance tiers

| Tier | Summary | Minimum evidence |
|---|---|---|
| Tier 1 — Final-request observable | Can prove complete managed-region inclusion in the exact final request submitted to the inference runtime | Final request ID, Context target/version, managed-region digest, request-boundary evidence, capability epoch and integrity-protected attestation |
| Tier 2 — Managed-region observable | Can prove managed-region materialization at the Adapter's pre-submit assembly boundary, but cannot independently observe actual runtime submission | Boundary-local evidence; Applied coverage MUST be Partial or Unknown, never Full |
| Tier 3 — Transport/basic integration | Can negotiate and receive protocol messages, validate versions and report transport/receipt state, but cannot prove application | Delivered/Rejected/Unknown only; no Applied claim unless a separately validated stronger capability exists |

Tier labels are conformance ceilings, not product quality rankings. Tier 2 and Tier 3 MUST NOT claim Tier 1 Full Applied.

## 7. Dependencies and freeze gates

| Dependency | H consumes | Status at H baseline |
|---|---|---|
| C — telemetry and final inference boundary | Event types, producer context, protected-region boundary, final-request observation requirements | C overview read; detailed C contract files not confirmed at named paths; keep interface CANDIDATE |
| D — canonical refs / Forget | Stable object/version references, canonical ForgetOperation ID and fence | Exact branch/baseline named in task pack; owner contract dependency OPEN |
| E — receipt | Accepted receipt, idempotency scope, durable-ingress result | Exact branch/baseline named; receipt file not confirmed at guessed path; OPEN |
| F — retrieval | Retrieval result and typed freshness/watermark context | Exact branch/baseline named; OPEN |
| G — Context delivery | ContextVersion, snapshot/delta, delivery intent, stale-base and supersession semantics | Exact branch/baseline named; G remains authority; OPEN |
| I — security/governance | Authenticated principal binding, ActorRef mapping, permission epoch, revocation, Forget policy | No I branch/package found at task start; BLOCKING dependency |

**Do not freeze** identity, permission, Forget completion, Context membership/version payloads, telemetry enum vocabulary, receipt fields, or cursor semantics while their owners' contracts remain open.

## 8. Delivery acceptance criteria

A BMCP implementation is conformant only when:
1. It negotiates a mutually supported version and capabilities before state-changing operations.
2. It validates envelope integrity, message identity, expiry, replay/idempotency and authenticated transport binding.
3. It keeps each message family semantically distinct.
4. It enforces exact Context base/target version and stale-fence rejection.
5. It distinguishes Prepared, Delivered and Applied with evidence.
6. It reports Full Applied only with Tier 1 final-request proof.
7. It clears/suppresses managed data on Forget/revocation and prevents stale reconnect resurrection.
8. It preserves protected Agent instruction and authorization regions.
9. It does not claim control over model-provider retained prompts, hidden context, or model internals.
10. It exposes unresolved policy/domain decisions instead of silently freezing them.
