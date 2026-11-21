# Agent Adapter Capability Tiers

**Status:** DECIDED tier intent and guarantee boundaries; CANDIDATE conformance details  
**Owner:** Session C — Agent Integration boundary pre-design  
**Protocol:** Session H owns BMCP capability negotiation and Adapter implementation contracts.

## 1. Purpose

Capability tiers classify what an integration can reliably observe, request, receive, and apply. They are not rankings of Agent intelligence. A tier describes integration guarantees only.

## 2. Tier overview

| Capability | Tier 1 — Full inference boundary | Tier 2 — Middleware | Tier 3 — Events and Active Recall |
|---|---|---|---|
| Structured telemetry | Yes | Middleware-visible subset | Event/explicit request subset |
| Active Recall | Yes | Yes | Yes |
| Proactive context delivery | Yes | Yes, to middleware slot | Not guaranteed |
| Apply before inference submission | Yes | Yes on controlled paths | No |
| Applied version attestation | Yes | Yes on controlled paths | No |
| Snapshot/delta reconciliation | Full | Middleware-supported subset | Not applicable |
| Observe task/session changes | If exposed | Middleware-visible | Explicitly submitted only |
| Environment telemetry | Supported | If instrumented | Optional |
| Isolated Brain-managed region | Explicit | Middleware-defined slot | No guarantee |
| Model comprehension guarantee | No | No | No |

## 3. Tier 1 — Full inference-context boundary

### Definition
Adapter can observe the relevant request assembly boundary and modify a dedicated Brain-managed memory region before the request is submitted to the inference runtime.

### Required capabilities
- Map canonical telemetry and identify Agent instance/session/task/environment scope.
- Receive snapshots and incremental Change Sets.
- Validate scope, base/target version, capability, budget, and managed-region ownership.
- Apply the complete accepted Brain-managed region before inference submission.
- Attest exact version and boundary/request correlation.
- Detect unsupported operations, budget overflow, and version gaps.
- Reconcile through full snapshot when delta continuity is lost.
- Keep protected instructions, user input, Agent policy, and tool definitions outside the managed region.

### Guarantees
**DECIDED:** Tier 1 can attest that the specified version was applied to the designated memory region for a specific inference request assembly.

### Non-guarantees
Tier 1 does not guarantee model attention, understanding, correct use, response correctness, Agent compliance, or ability to modify an in-flight inference. It does not expose hidden reasoning by implication.

## 4. Tier 2 — Middleware integration

### Definition
Integration occurs through middleware, orchestration hook, prompt/context builder, or request interceptor that can access outgoing requests and a designated memory slot, but may not observe every internal state or inference path.

### Required capabilities
- Submit telemetry visible at middleware hooks.
- Support explicit Active Recall.
- Receive context updates through a middleware-managed slot.
- Apply accepted updates before requests passing through the controlled hook.
- Report covered and bypassed request paths.
- Maintain applied-version record for the controlled slot.

### Guarantees
**DECIDED:** Tier 2 can attest insertion of a specified context version into a request that passed through its controlled assembly hook, if it can inspect the final outgoing request representation.

### Non-guarantees
No guarantee for bypassed paths, complete Agent state, hidden/provider-managed context, all task/environment transitions, or model comprehension. Do not claim Tier 1 coverage without equivalent boundary observability and control.

## 5. Tier 3 — Events and Active Recall

### Definition
Minimal integration for Agents that can submit scoped events/telemetry and explicitly request memories but cannot reliably accept proactive Brain-managed context changes at inference boundaries.

### Required capabilities
- Authenticate producer and submit scoped telemetry/events.
- Supply idempotency identifiers for retryable writes.
- Request Active Recall with explicit scope and task context.
- Receive memory results as data through API/tool response.
- Preserve source/provenance references when passing results onward.

### Guarantees
**DECIDED:** Tier 3 guarantees only the accepted telemetry and Recall response contracts. It makes no proactive synchronization or Applied Context claim. Agent decides whether/how to place results in its own context; Brain cannot verify this.

### Safe degradation
Tier 3 is not an error state. Brain retains canonical memory and Recall, labels results as data, does not create misleading proactive deliveries, and exposes synchronization as unsupported. Tier may be upgraded after boundary capability validation.

## 6. Negotiated capabilities

Final negotiation message belongs to Session H. Logical declarations include:
- Tier and feature flags.
- Supported telemetry signal types and schema versions.
- Supported context operations and snapshot/delta modes.
- Maximum context payload/token/byte budget where known.
- Acknowledgement semantics.
- Inference boundary type and final-request visibility.
- Environment telemetry support.
- Offline buffering and reconciliation support.
- Unsupported features and known bypass paths.

A declaration is not a guarantee until conformance tests pass. Negotiation is versioned and bound to authenticated Adapter identity.

## 7. Tier selection rules

1. Select the highest demonstrated tier, not merely claimed.
2. Middleware with incomplete path coverage may be Tier 2 but must disclose bypasses.
3. Insertion without exact version/request identification is not full Tier 1 Applied semantics.
4. API/tool-only Recall is Tier 3.
5. Capability loss moves integration to Degraded; stop making unsupported guarantees.
6. Tier upgrades require revalidation and context reconciliation.

## 8. Tier state machine

~~~mermaid
stateDiagram-v2
  [*] --> Unassessed
  Unassessed --> Negotiating
  Negotiating --> Tier1: boundary, apply, attest verified
  Negotiating --> Tier2: middleware path verified
  Negotiating --> Tier3: events and recall verified
  Negotiating --> Unsupported: minimum contract unavailable
  Tier1 --> Degraded: capability lost
  Tier2 --> Degraded: capability lost
  Tier3 --> Degraded: capability lost
  Degraded --> Negotiating: revalidation
  Tier1 --> Negotiating: capability change
  Tier2 --> Negotiating: capability change
  Tier3 --> Negotiating: upgrade
  Unsupported --> Negotiating: new Adapter version
~~~

Transitions:
- Unassessed to Negotiating: authenticated registration.
- Negotiating to Tier N: all tier conformance checks pass.
- Tier N to Degraded: required capability unavailable or attestation unreliable.
- Degraded to Negotiating: restored capability is revalidated.
- Tier N to Negotiating: Adapter version/features change.
- Negotiating to Unsupported: no tier minimum passes.

A transport outage alone need not downgrade a tier; connection state is tracked separately.

## 9. Failure behavior

| Failure | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Brain offline | Agent continues; only valid authorized local context | Same for middleware path | Recall unavailable |
| Adapter offline | No new application | No new middleware insertion | No ingress/Recall |
| Version gap | Reject delta; snapshot reconcile | Same on controlled slot | N/A |
| Middleware bypass | Not expected under claimed boundary | Mark request uncovered | Agent-controlled |
| Budget exceeded | Reject or explicitly negotiated compaction | Same | Explicit response truncation contract |
| Permission revoked | Stop delivery and reconcile | Same | Reject Recall/ingress as applicable |
| Partial apply | Reject unless explicit partial semantics | Same | N/A |

## 10. Security

Tier does not grant permission. Scope and authorization remain mandatory. Adapter identity is bound to Agent/instance and allowed scopes. Memory is data, never instruction. Tier 1/2 insertion is limited to the managed region; Tier 3 results are untrusted data. Downgrade cannot broaden access. Local caches obey retention, revocation, and Forget.

## 11. Performance and acceptance

Measure telemetry coverage, Recall latency/quality, delivery/application latency (Tier 1/2), version lag, rejection and reconciliation rates, inference-path coverage, middleware bypass rate, and Agent outcomes under controlled comparisons.

Acceptance:
1. Tier 1 passes snapshot, delta, gap recovery, region isolation, and Applied attestation tests.
2. Tier 2 reports covered versus bypassed requests and never claims application for bypassed requests.
3. Tier 3 supports scoped telemetry/Recall and emits no false Applied.
4. Invalid capability declarations fail conformance.
5. Capability loss becomes Degraded and stops unsupported guarantees.
6. Tier upgrade revalidates and reconciles before claiming new tier.
7. All tiers reject cross-scope access.
8. All tiers preserve data/instruction separation.

## 12. Interfaces and open decisions

- **Session H:** Negotiation schema, message IDs, acknowledgements, and conformance handshake.
- **Session G:** Context operations, version reconciliation, partial-apply semantics, Applied record.
- **Session I:** Local cache retention, revocation, offline buffering, audit.
- **OPEN:** Whether Tier 2 coverage is a percentage or per-request record. **CANDIDATE:** Per-request records are authoritative.
- **TO_VALIDATE:** Minimum conformance suite and coverage evidence.

## 13. Decision summary

- **DECIDED:** Tiers describe integration guarantees, not Agent quality.
- **DECIDED:** Tier 1 applies at a fully observed inference boundary.
- **DECIDED:** Tier 2 applies only on middleware-controlled paths.
- **DECIDED:** Tier 3 provides events and Active Recall, not proactive Applied semantics.
- **DECIDED:** No tier guarantees model comprehension.
- **DECIDED:** Capability claims require conformance evidence; failures trigger explicit degradation.
- **OPEN:** Wire-level negotiation belongs to Session H.


## 14. Executable operation binding (reference-model contract)

The following operation mapping makes the DECIDED tier guarantees executable. It is a deterministic reference-model contract, not a BMCP wire negotiation or a production Adapter implementation.

| Operation enum | Minimum tier | Tier 1 | Tier 2 | Tier 3 |
|---|---:|---:|---:|---:|
| `SubmitScopedTelemetry` | 3 | Allow | Allow | Allow |
| `RequestActiveRecall` | 3 | Allow | Allow | Allow |
| `InsertMiddlewareMemorySlot` | 2 | Allow | Allow | Reject |
| `AttestMiddlewareApplication` | 2 | Allow | Allow | Reject |
| `ObserveFullInferenceBoundary` | 1 | Allow | Reject | Reject |
| `ApplyFullBoundaryMemory` | 1 | Allow | Reject | Reject |
| `AttestFullBoundaryApplication` | 1 | Allow | Reject | Reject |
| `ReconcileSnapshotAndDelta` | 1 | Allow | Reject | Reject |

A lower tier is not permitted to perform an operation merely because it can represent the request. The reference model returns `AdapterError::TierInsufficient { required, actual }`; callers must branch on the enum, not parse display text. Tier 1 subsumes Tier 2 and Tier 3 operations; Tier 2 subsumes Tier 3 operations.

### Boundary rejection codes

The reference model also exposes typed boundary rejection reasons:

- `ProtectedRegionMutation(region)`: any attempt to write System instructions, Developer instructions, user input, Agent safety policy, tool schemas/authorization, or Agent working state.
- `RequestAlreadyFrozen`: attempting to change the managed region after the request assembler has frozen the inference request.

Both rules directly enforce DECIDED principles in `inference-boundary-model.md`: protected regions are not Brain-writable, and an in-flight/frozen request is immutable. These are the two implemented boundary cases; version-gap reconciliation remains specified by the source contract but is not implemented by this minimal reference model.

### Scope and status

This mapping is an executable interpretation of the tier guarantees already marked DECIDED in this document. Wire-level negotiation, authenticated capability claims, transport, provider integration, actual inference, and production telemetry remain out of scope. The model does not claim any of them.


## 15. In-memory context delivery lifecycle (implemented reference behavior)

The crate now exposes a `ContextDeliveryAdapter` trait and `InMemoryContextDeliveryAdapter`. The in-memory implementation maintains a per-session applied `ContextSnapshot` and connection flag.

| Lifecycle action/state | Implemented behavior |
|---|---|
| Connected / apply | Accept only the exact successor version (new or cleared session starts at version 1); record the snapshot only after acceptance |
| Version rejection | Return typed `AdapterError::VersionMismatch { expected, received }`; leave the applied snapshot unchanged |
| Clear | Remove the applied snapshot; the next accepted apply starts at version 1 |
| Disconnected | Reject apply with `SessionDisconnected`; retain the last successfully applied snapshot |
| Reconnected | Restore the in-memory connection flag and report the last successfully applied version (or `None`) |

**NOT IMPLEMENTED:** real transport; per-runtime Agent integration; a durable delivery ledger; durable session state; automatic retry/re-delivery; production reconciliation or attestation. Reconnect is a deterministic in-memory state transition, not proof of remote Agent state. This implementation does not translate provider-specific runtime objects or claim delivery outside its own process memory.

# Canonical snapshot integration (round 6)

The in-memory delivery adapter now accepts and retains the canonical
`memory_context::ContextSnapshot` directly. `agent-integration` depends on
`memory-context`; the dependency direction remains one-way because
`memory-context` does not depend on `agent-integration`. There is no second
adapter-local snapshot struct or serialization conversion.

The adapter uses `ContextSnapshot.context_version` as the sole version value.
Before accepting an apply, it calls `memory_context::validate_snapshot`.
Validation failures are returned as the typed
`AdapterError::InvalidSnapshot(ContextError)`; version gaps return
`VersionMismatch { expected, received }`. Disconnected sessions return
`SessionDisconnected`. All three rejection paths preserve the last applied
snapshot unchanged. `applied_snapshot` returns the exact canonical snapshot
accepted by the adapter.

This remains an in-memory reference adapter, not a transport or production
runtime integration. The canonical type removes the caller-side hand-rolled
serialization boundary; it does not itself prove that a remote Agent runtime
has applied the context.
