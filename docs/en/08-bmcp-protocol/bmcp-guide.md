# BMCP — Protocol Architecture Guide

- Document ID: DOC-BMCP-001
- Version: 1.0
- Owner: H — BMCP Protocol
- Source: H owner branch, protocol overview and Adapter capability/Applied attestation contracts
- Chinese counterpart: [BMCP 协议架构指南](../../zh-CN/08-bmcp-protocol/bmcp-guide.md)
- Status: CANDIDATE architecture; dependent wire/identity elements remain OPEN or ADR-BLOCKED

## 1. What BMCP does

Brain Memory Context Protocol (BMCP) is the Brain-defined contract between the Memory Brain and Agent Adapters. It transports structured telemetry, event ingress references, Context snapshots/deltas, delivery lifecycle, acknowledgements, capability negotiation, and Forget/revocation notifications.

BMCP carries domain references and payloads; it does not redefine the meaning of Memory, Claim, Scope, Permission, ContextVersion, or Forget. Those meanings remain owned by B/D/G/I. H owns wire encoding, protocol versioning, transport interaction, Adapter-facing capability vocabulary, and ACK/attestation encoding.

## 2. Ownership boundaries

| Owner | Authority |
|---|---|
| B/D | Domain objects, canonical identity, lifecycle, canonical Forget state |
| C | Agent integration semantics, telemetry meaning, Agent-side boundary requirements |
| G | Context membership, ContextVersion, ChangeSet, delivery intent semantics |
| H | BMCP wire envelope, versioning, message families, transport and ACK encoding |
| I | Principal trust, authorization policy, permission epochs, global Forget policy |

BMCP does not make an Agent continue to function when the Brain is unavailable; the Agent remains responsible for its own operation and safety policy. BMCP cannot rewrite hidden provider prompts, provider-retained request copies, model internals, or model attention.

## 3. Message families

| Family | Direction | Purpose |
|---|---|---|
| Telemetry | Adapter → Brain | Structured Agent observations, outcomes, intent, plan summaries, tool/environment events |
| Event Ingress | Producer → Brain | Submit typed source Events with idempotency and provenance references |
| Context Snapshot | Brain → Adapter | Replace the complete managed Context view at a target version |
| Context Delta | Brain → Adapter | Apply an atomic ChangeSet from an exact base to target version |
| Delivery | Brain → Adapter | Bind snapshot/delta to recipient, session, and delivery lifecycle |
| Acknowledgement | Adapter → Brain | Report lifecycle status and evidence |
| Capability Negotiation | Bidirectional | Negotiate protocol versions, message families, limits, and proof tiers |
| Forget / Revocation | Brain/I → Adapter | Invalidate managed content, sessions, queued work, and stale offline state |
| Administrative Governance | I/control plane → Adapter/Gateway | Carry policy epochs, revocation, recipient Scope, and control directives |

## 4. Delivery statuses are not interchangeable

- Prepared: Adapter validated and staged a delivery; transport delivery is not confirmed.
- Delivered: transport endpoint accepted it for the addressed Adapter.
- Applied: Adapter attests to defined application coverage at an inference boundary.
- Rejected: recipient explicitly refused with a classified reason.
- Expired: validity deadline passed without valid completion.
- Superseded: a newer Context target or governance epoch made it obsolete.
- Unknown: outcome cannot be established, such as timeout, process loss, or offline state.

No status implies another without an explicit transition and evidence. Delivered MUST NOT be interpreted as Applied. Applied MUST NOT be interpreted as model attention or use.

## 5. Adapter capability tiers

### Tier 1 — Final-request observable
The Adapter observes the exact final request after all assembly and transformations, identifies the request submitted to the inference runtime, proves managed-region completeness and exact target ContextVersion, computes a declared digest over that region, correlates request/delivery/session/context/capability identity, and emits integrity-protected evidence.

Only Tier 1 may emit Full Applied, and only when every per-request proof predicate passes. Otherwise it reports Partial, Bypassed, or Unknown.

### Tier 2 — Managed-region observable, final submit not observable
The Adapter can validate its local managed region but cannot prove the exact final request was submitted; later middleware may change or discard it. A local buffer digest is not final-request proof. Tier 2 MUST NOT claim Full Applied.

### Tier 3 — Transport/basic integration
The Adapter validates protocol envelope/version and transports messages, reporting transport delivery, rejection, and unknown outcomes. It does not claim that Context was applied to an inference request and MUST NOT emit Applied=Full.

## 6. Capability epochs and attestation

Capabilities are explicit, versioned declarations—not inferred from product name or transport reachability. They may include supported protocol/schema versions, message families, Snapshot/Delta operations, payload limits, durable queue behavior, idempotency, managed-region isolation, final-request visibility, runtime handoff observation, request correlation, digest/evidence capability, Forget clearing/reconnect behavior, ACK coverage, and context-size limits.

A capability-changing binary/configuration/runtime change creates a new Adapter capability epoch and requires renegotiation. An attestation is evaluated against the epoch that produced it, not whichever capability set is current later.

## 7. Applied evidence

An Applied attestation must bind the delivery attempt to the target Context and version, actual applied version, coverage, Adapter identity and capability epoch, authenticated transport principal, inference request/final-request identity or digest, relevant Scope/PermissionEpoch, and current Forget Fence generation as required by the approved contract.

A receipt ACK or local buffer hash alone is insufficient. Applied proves only the Adapter's declared boundary operation, not model comprehension or behavioral compliance.

## 8. Forget, revocation, and reconnect

Forget/revocation notifications must invalidate the managed region and stale queued deliveries. Offline Adapters must reconcile current Context target, authorization epoch, and Forget Fence before reusing local content after reconnect. Unsupported or unreachable targets remain UNKNOWN/UNSUPPORTED unless I approves a documented residual exception; they are not silently counted as success.

## 9. Compatibility and failure handling

- Version negotiation must be explicit; incompatible major versions fail closed.
- Unknown required fields or unsupported operations must be rejected or handled under declared forward-compatibility rules.
- Duplicate state-changing messages must be idempotent within their defined key scope.
- Partial transport or local application must be reported accurately.
- Timeouts and process loss produce Unknown unless stronger evidence exists.
- Capability downgrade must not preserve a Full Applied claim.

## 10. Open dependencies and validation

- Final-request Applied proof requires joint C/G/H/I agreement.
- Principal/ActorRef/ScopeRef and authenticated transport binding remain dependent on B/I/H decisions.
- Forget ACK classes must map to I's per-target completion vector.
- Cross-language schema and signature canonicalization require conformance vectors.
- Reconnect, replay, duplicate delivery, capability downgrade, and final-request mutation require fault tests.

See the [H owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-h-bmcp-protocol/08-bmcp-protocol) for the detailed candidate protocol documents.
