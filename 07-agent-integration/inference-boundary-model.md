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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Classified as Non-Canonical Informative; the document records semantic boundaries and asserts no Runtime implementation or approval."
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
    canonical_status: Non-Canonical
    canonical_scope: "Inference boundary model for Agent inference requests"
    canonical_scope_id: null
    canonical_scope_keywords:
      - inference-boundary
      - applied-context
      - delivery-acknowledgement
      - agent-integration
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/07-agent-integration/inference-boundary-model.md"
    zh-CN: "docs/zh-CN/07-agent-integration/inference-boundary-model.md"
---

# Inference Boundary Model

**Status:** DECIDED safety/semantic boundaries; CANDIDATE execution details; OPEN provider mapping  
**Owner:** Session C — Agent Integration boundary pre-design  
**Dependencies:** Session G — Memory Context; Session H — BMCP/Adapter; Session I — consistency and recovery.

## 1. Purpose

Define when a Brain-managed Memory Context can be considered applied to an Agent inference request. This prevents assuming Brain can rewrite an in-flight model context and prevents delivery acknowledgements from being misrepresented as application.

The inference boundary is where the Agent/Adapter assembles the effective context for a particular inference invocation and commits that request to the inference runtime.

## 2. Normative principles

- **DECIDED:** Brain is authoritative for its managed Memory Context version.
- **DECIDED:** Adapter applies the desired context at the Agent inference assembly boundary.
- **DECIDED:** Changes take effect at a future boundary.
- **DECIDED:** An in-flight request is immutable from Brain's perspective.
- **DECIDED:** Received, Accepted, and Applied are distinct.
- **DECIDED:** Applied proves only that the Adapter applied a specified version at the agreed boundary.
- **DECIDED:** Applied does not prove model attention, comprehension, recall, or behavioral compliance.
- **DECIDED:** Brain cannot overwrite system/developer instructions, user input, Agent safety policy, or tool authorization.
- **DECIDED:** Context Remove is not Canonical Memory Forget.

## 3. Boundary sequence

~~~mermaid
sequenceDiagram
  participant B as Brain Context Manager
  participant S as Context Sync
  participant A as Agent Adapter
  participant R as Request Assembler
  participant L as LLM Runtime
  B->>S: Change Set base v to target v+1
  S->>A: Deliver
  A-->>S: Received(delivery id)
  A->>A: Validate scope, version, budget, operations
  A-->>S: Accepted or Rejected
  Note over A,R: Wait for next inference assembly boundary
  R->>A: Prepare request
  A->>R: Apply managed region v+1
  R->>L: Submit immutable request
  A-->>S: Applied(v+1, boundary correlation)
  L-->>R: Response
~~~

The boundary can be a prompt builder, middleware hook, request interceptor, context API, or equivalent. Logical semantics do not depend on implementation.

## 4. Context composition and protected regions

| Region | Owner | Brain may modify? |
|---|---|---:|
| System instructions | Platform/runtime or Agent deployment | No |
| Developer instructions | Application/developer | No |
| Agent safety/tool policy | Agent/application | No |
| User-originated input | User/application capture | No |
| Brain-managed memory region | Brain defines content; Adapter applies | Yes, only by contract |
| Agent working state | Agent | No absent a separate contract |
| Tool schemas/authorization | Agent/platform | No |

Adapter must identify the exact managed region. If the Agent cannot isolate it, integration cannot claim Tier 1. Memory is serialized as untrusted data, never elevated instructions.

**CANDIDATE:** Delimit the managed region with context ID, version, scope, and content classification metadata. Delimiters alone are not a security boundary; enforcement belongs in Adapter and request assembly.

## 5. Delivery, receipt, acceptance, application

| State/term | Meaning | Evidence |
|---|---|---|
| Prepared | Brain produced a delivery artifact | Brain delivery record |
| Delivered | Transport handed artifact to Adapter endpoint | Transport result |
| Received | Adapter confirms artifact receipt | Adapter receipt |
| Accepted | Adapter validated scope, version, capability, budget, operations | Adapter acceptance |
| Applied | Exact target version materialized in managed region at an inference boundary | Adapter attestation |
| Rejected | Adapter declines artifact with typed reason | Adapter rejection |
| Expired | Artifact no longer eligible under validity policy | Brain delivery state |
| Superseded | Newer authoritative version makes delivery obsolete | Brain context/delivery record |

Delivered is not Received; Received is not Accepted; Accepted is not Applied.

Adapter MUST NOT report Applied merely because it received, parsed, queued, cached, appended to an unused template, or forwarded an update upstream without confirmation of actual managed-region materialization at the boundary.

## 6. Applied attestation

Logical Applied record fields:

| Field | Meaning |
|---|---|
| context_id | Brain-managed context identity |
| context_session_id | Target Agent context session |
| target_context_version | Exact version applied |
| adapter_id / adapter_instance_id | Authenticated applying Adapter |
| agent_instance_id | Agent instance |
| boundary_id | Inference assembly hook identity |
| inference_request_id | Request correlation when available |
| applied_at | Adapter application time |
| applied_region_digest | Optional digest of materialized region |
| application_mode | Snapshot, delta materialization, etc. |
| coverage | Whether complete managed region is covered |
| capability_epoch | Capability declaration under which applied |

Digest is optional and must not expose sensitive content; canonicalization must be versioned. Applied is an Adapter attestation, not provider-side proof.

**OPEN:** Whether inference_request_id is mandatory. **CANDIDATE:** Require it when exposed; otherwise require a unique boundary invocation ID.

## 7. Version and base rules

- Brain Context Manager owns the authoritative context version sequence.
- Adapter keeps a local applied-version watermark per context session.
- Delta applies only when its base matches the Adapter's materialized version.
- Unknown base, gaps, or unexpected version require rejection/reconciliation, not guesswork.
- Reconcile by full snapshot or explicitly supported recovery operation.
- Applied versions are monotonic within a context session except governed reset to a new session identity.
- Newer context versions may supersede pending deliveries.
- Context Remove affects only the context entry; canonical Memory remains unless a separate Forget workflow is authorized and completed.

## 8. Delivery state machine

~~~mermaid
stateDiagram-v2
  [*] --> Prepared
  Prepared --> Delivered: transport handoff
  Delivered --> Received: Adapter receipt
  Delivered --> Expired: TTL elapsed
  Received --> Accepted: validation succeeds
  Received --> Rejected: validation fails
  Accepted --> Applied: applied at inference boundary
  Accepted --> Rejected: pre-apply condition invalid
  Prepared --> Superseded: newer version
  Delivered --> Superseded: newer version
  Received --> Superseded: newer version
  Accepted --> Superseded: newer version before apply
  Rejected --> [*]
  Applied --> [*]
  Expired --> [*]
  Superseded --> [*]
~~~

Terminal delivery states are Applied, Rejected, Expired, and Superseded. A retry after terminal failure uses a new delivery identity unless protocol semantics explicitly define retry identity.

Transitions:
- Prepared to Delivered: transport confirms handoff.
- Delivered to Received: Adapter receipt for delivery ID.
- Received to Accepted: scope/schema/capability/base/budget validation passes.
- Received to Rejected: validation fails.
- Accepted to Applied: exact target version is materialized at an inference boundary.
- Accepted to Rejected: pre-application condition becomes invalid.
- Pending state to Superseded: newer authoritative version invalidates artifact.
- Pending state to Expired: validity policy elapses before application.

Timeout is not Applied or Rejected. Record pending/unknown transport outcome and reconcile by delivery ID/version.

## 9. Snapshot and delta

**CANDIDATE:**
- Deltas for normal incremental updates when base continuity is known.
- Full snapshots for bootstrap, recovery, version gaps, untrusted local state, or incompatible history.
- Adapter materializes the complete target region before reporting Applied.
- Parsing a delta is not application; the resulting region must be used at the boundary.

If an operation cannot be applied, default to rejecting the delivery. Partial application requires explicit Session G/H semantics, per-entry results, and a distinct non-full acknowledgement. Until defined, Applied means full managed-region application.

## 10. Concurrency and inference races

1. Adapter chooses one serialization point for materialization at the boundary.
2. Request assembler obtains one immutable managed-region snapshot per invocation.
3. Update arriving before snapshot freeze may be applied if validated.
4. Update arriving after freeze applies only to a later request.
5. An in-flight request is never relabeled with a newer context version.
6. Brain serializes concurrent context changes; Adapter rejects unknown-base deltas.
7. Request retries record whether they reuse the same context version or assemble a newer one.

## 11. Offline, reconnect, restart, mismatch

**Adapter offline:** Brain tracks pending delivery subject to TTL/retention. Agent continues without fresh proactive updates. No Applied claim.

**Reconnect:** Adapter authenticates and reports context/session identity, capability epoch, and last known applied version.
- Equal version: resume.
- Behind with contiguous history: send deltas if supported.
- Behind with missing history: full snapshot.
- Unknown/invalid version: full reconciliation; do not trust arbitrary client advancement.
- Newer Brain version: obsolete pending deltas may become Superseded.

**Restart:** Durable integrity-checked applied state may be reported. Otherwise state is unknown and a full snapshot is required before claiming synchronization.

**Capability change:** Increment capability epoch. Revalidate accepted but unapplied deliveries. Old-epoch attestations do not prove coverage under new boundary.

## 12. Failure isolation

Brain outage must not fail Agent execution by default. Agent may continue with protected native context and previously applied local memory only if still authorized and valid under retention/revocation. If freshness cannot be established, Adapter marks it stale/unknown and Agent policy decides use.

Permission revocation, Forget, or retention expiry may require local context reconciliation. Brain cannot assume remote physical deletion without acknowledgement and a defined assurance model.

## 13. Security

- Authenticate Adapter and bind context/session identity.
- Authorize scope on every delivery and reconciliation.
- Validate client version against Brain session record.
- Treat memory as untrusted data.
- Protect instruction, user, policy, and tool regions.
- Prefer logging IDs, versions, digests, and outcomes over raw content.
- Ensure offline caches honor Forget, revocation, and retention.
- Treat Applied as auditable Adapter assertion, not proof of model behavior.

## 14. Metrics and tests

Measure generation-to-delivery, delivery-to-Received, Received-to-Accepted, Accepted-to-Applied latency; version lag; rejected/expired/superseded rates; snapshot/delta ratio; reconciliation success; boundary coverage; stale-context use; revocation propagation.

Acceptance scenarios:
1. Received but not Accepted is not Applied.
2. Accepted with no inference request remains Accepted.
3. Update arriving during request N applies no earlier than request N+1.
4. Wrong target version attestation is rejected.
5. Delta base mismatch triggers snapshot reconciliation.
6. Restart with unknown version requires full snapshot.
7. Middleware bypass has no Applied attestation.
8. Budget overflow does not produce false full Applied.
9. Permission revocation before boundary prevents application.
10. Context Remove leaves canonical Memory unchanged.
11. Forget invokes separate governance workflow.
12. Protected regions remain unchanged.
13. Duplicate delivery is idempotent.
14. Superseded old version cannot later be silently applied.

## 15. Interfaces and open questions

| Partner | Required agreement |
|---|---|
| Session G | Context/session IDs, version/base, snapshot/delta, Change Set atomicity, partial-apply policy |
| Session H | Message states, acknowledgement schema, retry identity, timeout, capability epoch, errors |
| Session I | Durable applied watermark, reconnect recovery, audit, retention, Forget propagation |
| Agent framework/runtime | Actual assembly hook, immutable submission point, request correlation, context slot |

**OPEN:** Whether Applied is emitted synchronously with request submission. **CANDIDATE:** Emit only after final region materialization and request commitment to submission path.

**OPEN:** Streaming/multi-stage inference may create multiple requests per Agent turn. **CANDIDATE:** Attest each inference request boundary and link them with a turn correlation.

**OPEN:** Evidence required for middleware to claim final request visibility is a Session H conformance question.

## 16. Decision summary

- **DECIDED:** Inference boundary is request-context assembly/commit.
- **DECIDED:** In-flight inference is not dynamically rewritten.
- **DECIDED:** Delivery, receipt, acceptance, and application are distinct.
- **DECIDED:** Applied identifies exact version and boundary; it does not prove comprehension.
- **DECIDED:** Brain modifies only its managed region.
- **CANDIDATE:** Deltas for normal sync; snapshots for bootstrap/recovery.
- **DECIDED:** Unknown base requires rejection or reconciliation.
- **OPEN:** Wire acknowledgements and Adapter conformance belong to Session H; context authority remains Session G.
