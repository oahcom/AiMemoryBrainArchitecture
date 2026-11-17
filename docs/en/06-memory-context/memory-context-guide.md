# Memory Context — Architecture Guide

- Document ID: DOC-CONTEXT-001
- Version: 1.0
- Owner: G — Memory Context
- Source: G owner branch, Context architecture and Phase 3 integration contracts
- Chinese counterpart: [记忆上下文架构指南](../../zh-CN/06-memory-context/memory-context-guide.md)
- Status: Explanatory guide; internal model CANDIDATE and cross-module wire details OPEN

## 1. What Memory Context is

Memory Context is the Brain-owned, scoped, versioned working view of selected Canonical Memory assets for a particular Agent execution context.

It is not the full Memory Store, not the complete Agent prompt, and not the Agent's private working state. It is the managed memory region for which the Brain owns membership, ordering, qualification, expiry, budget policy, and version history.

## 2. Three distinct layers

| Layer | Authority | What it contains |
|---|---|---|
| Canonical Memory | D — canonical domain | Immutable Memory versions, Claims, Entities, Relations, Evidence/Provenance, lifecycle |
| Memory Context | G — Context Manager | Scoped entries referencing authorized canonical versions or governed renderings; ordering, rationale, validity, budget, version history |
| Applied Context | Adapter attestation, coordinated by G/H | What the Adapter says it installed in the managed region at a particular inference boundary, with version and evidence |

A Context Entry is a reference or bounded presentation, not a second canonical authority. Materialized text is a projection; its hash and source references support audit but do not grant access to the underlying source.

## 3. Context identity and isolation

A Context binds to resolved identity references such as owner/user, project, Agent, Agent instance, task, session, and Environment Scope. Environment identity is mandatory whenever selected memory or task semantics depend on a world, save, simulation, tenant, or workspace.

Missing, ambiguous, or reused environment identity must fail closed. A new task must not silently inherit another task's Context. Any inheritance must be explicit and authorized.

G stores resolved opaque references and re-checks authorization at read, plan, mutation, delivery, replay, and reconciliation. Agent-supplied Scope claims are hints, never authority.

## 4. What G owns

- Context identity and scoped membership.
- ContextEntry references and presentation metadata.
- ContextVersion and the authoritative version sequence for each Context.
- ChangeSet operations and optimistic concurrency/base-version rules.
- Ordering, activation rationale, expiry, budget, and sufficiency assessment.
- Snapshot/delta planning, delivery intent, and reconciliation state.
- Context-side Forget invalidation and suppression.

G does not own Canonical Memory versions (D), retrieval/index state (F), global identity and permission policy (I), BMCP wire encoding (H), or the Agent's final inference request and local application behavior (C/H).

## 5. Context operations and versioning

Typical operations include Add, Update, Remove, Replace, Reorder, Expire, Compact, and Reconcile. A mutation applies to G's managed Context, not to Canonical Memory.

Each change must be tied to an expected base version or explicit snapshot transition. Retries must be idempotent. Concurrent edits must be serialized or resolved with explicit concurrency control; there is one authoritative version sequence per Context.

Context Remove means “no longer include this entry in this Context.” It does not mean “forget the canonical memory.” Forget is a separate governance workflow that invalidates affected Context entries, snapshots, deltas, and pending deliveries.

## 6. Delivery is not Applied

G owns ContextVersion and delivery intent. H owns protocol delivery semantics; C/H Adapters own the evidence of what was actually materialized at the inference boundary.

Keep these milestones distinct:
- Prepared: a delivery package has been formed.
- Delivered: transport reports delivery.
- Accepted: Adapter validates and accepts the package.
- Applied: Adapter attests that the managed region in the final inference request contains the target Context version at the agreed boundary.
- Rejected/Expired/Superseded: delivery cannot or should not be applied.

An ACK for receipt or transport delivery is not an Applied attestation. Applied does not prove that the model attended to, understood, or followed the memory.

## 7. Applied evidence and boundary

A trustworthy Applied record must bind the relevant ContextVersion/ChangeSet and delivery identity to the Adapter identity/capability epoch, inference request or final request digest, resolved Scope and PermissionEpoch, and current ForgetFenceGeneration where required by the governing contract.

The evidence must correspond to the final managed region actually submitted for inference—not merely an intermediate buffer or an earlier prompt draft. If the Adapter cannot observe the final request, it must report a weaker capability/ACK class rather than claim Tier 1 Full Applied.

## 8. Forget and offline Adapter behavior

Forget invalidates affected Context entries, snapshots, deltas, and pending delivery intents. An offline Adapter must not later replay stale content as though it were current. On reconnect it must reconcile against current ContextVersion, PermissionEpoch, and Forget Fence state before applying anything.

An unavailable or unsupported Adapter target is not automatically success. It remains UNKNOWN/UNSUPPORTED or follows an explicitly approved residual-exception policy owned by I.

## 9. Budget and sufficiency

Context planning must respect the managed-region token budget and preserve critical coverage. A budget manager may compact or defer entries, but compaction must preserve canonical source references and provenance. It must not turn a low-confidence or disputed claim into an unqualified assertion.

Sufficiency is a task-relative assessment, not a guarantee of correct Agent behavior. Budget, ranking, and compaction thresholds remain subject to workload validation.

## 10. Failure and recovery

| Condition | Required behavior |
|---|---|
| Stale base version | Reject or reconcile; do not overwrite |
| Duplicate ChangeSet | Idempotent result |
| Adapter offline | Keep delivery pending/expired; do not mark Applied |
| Partial transport delivery | Resume or replace using explicit delivery state |
| Permission epoch changes | Re-authorize before application |
| Forget Fence advances | Cancel/suppress stale snapshots, deltas, and deliveries |
| Final request cannot be inspected | Do not claim Tier 1 Full Applied |
| Budget overflow | Compact/defer with provenance; never silently drop mandatory invariants |

## 11. Validation still required

- ContextVersion/ChangeSet concurrency and idempotency.
- Delivery state transitions and reconnect reconciliation.
- Final-request Applied evidence with C/H/I.
- PermissionEpoch and ForgetFenceGeneration race handling.
- Context Remove vs Forget isolation.
- Token-budget correctness and compaction provenance.
- Heterogeneous Agent integration and offline behavior.

See the [G owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-g-memory-context/06-memory-context) for detailed Context contracts.
