# G Module Baseline & Redlines — PROPOSED

- Proposal ID: G-MBR-001
- Version: 0.1.0
- Status: PROPOSED — NOT APPROVED
- Owner role: G — Memory Context Architect
- Branch: `session-g-memory-context`
- Reviewed branch HEAD: `f6e7c46da9963ffee02c7805330b3f14291ab540`
- Date: 2026-11-17
- Template: requested `00-governance/module-baseline-and-redlines-template.md` returned 404 on main; no matching template exists in the reviewed G tree. This proposal preserves the requested 14-section structure without claiming template compliance.
- Scope: G authority only. This file does not approve project governance, H wire semantics, C final-request facts, I permission, D ForgetFence, or B typed-reference semantics.

## 1. Module Mission

G owns the Brain-managed, scoped, versioned Memory Context: membership, ordering, qualification, expiry, budget, immutable ContextVersion history, ChangeSets, Snapshot/Delta equivalence, reconciliation, Delivery Intent, Applied record, freshness and Context-side Forget invalidation.

Context is a bounded projection of authorized canonical memory, not a second canonical store, full prompt, Agent working state, instruction channel or execution authority. G determines the desired Context state. The Adapter determines what it actually materialized at a specific boundary. C owns final inference-request submission facts; H owns protocol/Adapter transport and ACK evidence; I owns authorization; D owns canonical ForgetFence and lineage.

## 2. Ownership Baseline

**G is authoritative for:**
- Context identity within resolved B/I identity and Scope bindings.
- Context membership, ordering, tiers, validity, expiry and budget.
- ContextVersion sequence, immutable snapshots, ChangeSet commit and base-version concurrency.
- Snapshot/Delta construction and reconciliation decisions.
- Delivery Intent and per-delivery lifecycle tracking.
- Applied record persistence and Full/Partial/Bypassed/Unknown classification, but only after validating upstream evidence owned by C/H/I/D/B.
- Context-local tombstones, invalidation and freshness state.

**G is not authoritative for:** canonical memory truth/revision (D/B), retrieval ranking and index completeness (F), Agent planning/execution (C/Agent), wire encoding/transport/ACK truth (H), principal trust/PermissionEpoch (I), typed reference semantics (B), canonical ForgetFence/producer barrier (D), global inventory seal/completion (I), storage transaction implementation (Storage), or project governance approval (PGA).

## 3. Capability Baseline

| Capability | Baseline | Status |
|---|---|---|
| Context membership and scoped projection | Brain-owned, authorization-checked, source-version pinned | DECIDED |
| ContextVersion | Immutable complete desired state; per-Context monotonic sequence | DECIDED |
| ChangeSet | BaseVersion + target version, idempotency, CAS/equivalent serialization | DECIDED |
| Snapshot/Delta | Same target state; Snapshot is recovery authority, Delta is optimization | DECIDED |
| Reconciliation | Revalidate source lifecycle, permission, fence, freshness and delivery | DECIDED |
| Delivery Intent | G-owned desired target; transport delegated to H | DECIDED |
| Applied | Per Adapter/session/request evidence-bound G record | SEMANTIC RULE DECIDED; end-to-end freeze BLOCKED |
| Freshness | Typed per-source/partition watermarks; no scalar cross-domain comparison | DECIDED |
| Forget invalidation | Immediate logical block of G-owned projections and pending sends | SEMANTIC RULE DECIDED; runtime NOT VERIFIED |

Prepared, Delivered, Materialized, Final Request Submitted, Applied and Execution Started are separate facts. No state may be inferred from a later-looking transport or execution status. In particular, Delivered is not Materialized; Materialized is not Final Request Submitted; Final Request Submitted is not Applied; Applied is not Execution Started.

## 4. Domain Ownership

G owns Context, ContextVersion, ContextEntry membership/revision, ChangeSet, Snapshot, Delta, ReconciliationResult, DeliveryIntent, DeliveryId, DeliveryAttemptId, AppliedRecord, ContextFreshness and Context-side invalidation state.

G consumes (without redefining) B's PrincipalRef/ActorRef/ScopeRef/EnvironmentRef semantics; I's PermissionDecision/PermissionEpoch/revocation; D's canonical identity/version/lifecycle/ForgetFence/lineage/barrier; F's candidate and per-partition freshness/uncertainty; H's Adapter identity, CapabilityEpoch, delivery receipt, ACK and authenticated protocol evidence; C's immutable Final Request evidence and InferenceRequest/FinalRequestBoundary correlation.

## 5. Interface Baseline

1. **Context identity:** bind exact required Principal/tenant, project/workspace, Agent, AgentInstance, Session, Task and Environment references. Environment is mandatory when any selected memory or task semantics are environment-dependent. Missing, ambiguous, retired or mismatched identity fails closed.
2. **Versioning:** every committed ChangeSet identifies ContextId, BaseVersion, TargetVersion and immutable snapshot digest. Concurrent updates use compare-and-swap or equivalent per-Context serialization. A version sequence is never reused.
3. **Entry references:** pin exact MemoryId + MemoryVersion and rendering/schema version. Never silently dereference "latest". Every read, plan, mutation, delivery, replay and reconciliation rechecks authorization and canonical validity.
4. **Snapshot/Delta:** Delta is valid only against its exact base version and digest. Gaps, unknown base, schema incompatibility or digest mismatch require a full Snapshot or blocked reconciliation.
5. **Delivery:** DeliveryIntent binds exact ContextId/Version/digest, target Adapter/Agent/Runtime/Session, capability epoch, scope/environment, PermissionEpoch and applicable D fence/lineage. H controls wire transport.
6. **Applied:** Full requires exact target ContextVersion, Delivery+attempt, authenticated target/session, complete managed-region inventory and digest, current I authorization/PermissionEpoch, current D fence/lineage, H authenticated ACK/capability evidence, and C immutable final-submit proof for the same InferenceRequest/FinalRequestBoundary. G alone commits the Applied record after all predicates validate.
7. **Freshness:** CanonicalCommitCursor, IndexWatermark, PermissionEpoch, ForgetFenceGeneration, ProducerDomainInventoryEpoch, CapabilityEpoch and ContextVersion are distinct typed namespaces. Never cast, numerically compare or substitute them.
8. **Forget:** G blocks affected Context entries, snapshots, deltas, ChangeSets, queues and sendable deliveries before cleanup. Offline Adapter state remains Pending/Unknown until authenticated reconnect, fresh authorization/fence resolution, stale-state discard and exact attestation.

## 6. Security Baseline

- No unauthenticated, unresolved or caller-asserted identity may authorize protected Context operations.
- ActorRef and ScopeRef are references, not credentials or permission grants.
- Current I PermissionEpoch and decision must be revalidated at every protected boundary; stale epoch, missing issuer, unknown identity or authority outage pauses/denies.
- Revocation ordering is I-owned. G may not invent an order for races or rely on cached ALLOW.
- Context is data, never System/Developer instructions, tool definitions, tool authorization or Agent policy. Protected prompt regions remain outside G's mutable region.
- Context tier/priority does not confer trust or instruction authority.
- Candidate content is rechecked against canonical lifecycle, scope, permission and D fence before materialization and delivery.
- Unknown targets, unsupported capabilities, missing managed-region coverage, digest conflict or incomplete evidence remain Unknown/blocked.
- Adapter ACK is limited to authenticated Adapter/Session/Target/Region/CapabilityEpoch and declared evidence coverage. It is not Global Forget.
- Historical Applied truth is immutable if validly established; current-use eligibility is recomputed against current Context head, permission, fence, scope, session and capability. Revocation does not rewrite history but blocks future use.

## 7. Module Redlines

| ID | Redline | Required behavior |
|---|---|---|
| G-RL-01 | Delivered != Applied | Never infer Applied from send success, transport receipt or ACK alone |
| G-RL-02 | Materialized != Submitted | Require C-owned immutable final request submission evidence |
| G-RL-03 | Submitted != Execution Started | Keep runtime execution evidence separate |
| G-RL-04 | Context cannot mutate protected prompt regions | Reject overlapping/ambiguous managed-region writes |
| G-RL-05 | Context cannot override Agent policy or execute actions | Memory remains untrusted descriptive data |
| G-RL-06 | No stale permission/fence use | Revalidate current I PermissionEpoch and D fence at final gate |
| G-RL-07 | No source-version substitution | Pin exact canonical MemoryVersion and lineage |
| G-RL-08 | Unknown Target/capability is not success | Quarantine or block; no silent skip |
| G-RL-09 | Delta gaps/digest mismatch fail closed | Full Snapshot or blocked reconciliation |
| G-RL-10 | Forget blocks replay/reconnect resurrection | Tombstone and suppress before physical cleanup |
| G-RL-11 | No scalar epoch conflation | Preserve typed namespace boundaries |
| G-RL-12 | No cross-owner authority | G cannot decide C/H/I/D/B-owned facts |

## 8. Forbidden Cross-module Actions

G must not:
- Define or reinterpret B's typed reference or domain semantics.
- Decide C's Final Request Submitted fact, provider receipt or Execution Started.
- Decide H's Adapter ACK, wire schema, transport authentication or CapabilityEpoch.
- Mint identity credentials, permission grants, revocation order or PermissionEpoch (I).
- Mint/advance D's ForgetFence, ProducerRegistrationHighWater or canonical publication barrier.
- Declare I's ProducerDomainInventory complete, seal it, approve exceptions or declare Global Forget complete.
- Promote a design contract, test plan or branch commit to implementation/conformance evidence.
- Modify another Owner branch, main, or merge any branch as part of this proposal.

## 9. Dependency Contracts

| Dependency | Required input/output | Owner | Current disposition |
|---|---|---|---|
| Typed references and scope | Resolved Principal/Actor/Scope/Environment semantics | B | Joint design exists; formal per-consumer status must be read from current owner records |
| Permission/revocation | Authenticated decision, current PermissionEpoch, ordered revocation | I | Design baseline; governance approvals blocked; runtime not verified |
| Canonical/fence | Exact memory versions, lineage, current ForgetFence and publication gate | D | Semantic contract exists; atomic runtime proof not established |
| Retrieval/freshness | Candidates, completeness, uncertainty, per-partition IndexWatermark | F | Consumer boundary; no authority transfer |
| BMCP/Adapter | Authenticated receipt, capability, ACK, reconnect and target coverage | H | Protocol semantics accepted with exceptions; H36 not run |
| Final request | Immutable exact request submission and provider handoff evidence | C | Required upstream fact; must not be inferred by G |
| Persistence | Durable CAS/version/Applied records and recovery | Storage | Implementation evidence not established |
| Project governance | Project-wide baseline approval | PGA | Not granted by this proposal |

## 10. Conformance Requirements

Required suites (all currently design/specification requirements unless separately evidenced):
- G-CV: immutable version sequence, CAS races, duplicate ChangeSet idempotency, changed-digest conflict.
- G-SD: Snapshot/Delta equivalence, base mismatch, missing delta, digest mismatch, schema downgrade and full-snapshot recovery.
- G-SCOPE: cross-Principal/Agent/Instance/Session/Task/Environment isolation and missing environment rejection.
- G-SEC: forged identity, stale PermissionEpoch, revocation races, unknown scope, unauthorized source reference and prompt-region overwrite rejection.
- G-APPLIED: all six evidence stages kept distinct; missing/stale/mismatched C/H/I/D evidence cannot promote Full Applied.
- G-CO: CGH causal-order race/recovery, same-identity replay, changed-digest conflict and terminal outcome consistency.
- G-FORGET: Forget during plan/commit/delivery/materialization/submit/reconnect; tombstone and stale artifact suppression.
- G-REC: offline Adapter reconnect, replacement Adapter/CapabilityEpoch, stale ACK replay and fresh Snapshot reconciliation.
- G-BUDGET: tokenizer/model-window variance, budget overflow, deterministic compaction and provenance preservation.
- G-RESTORE: restored Context/queue/cache cannot resurrect a forgotten projection.

Pass evidence must include exact commit/build, test command, fixtures, deterministic race schedule, expected/actual output, logs/artifacts and reviewer/owner record. Test specifications are NOT RUN until such evidence exists.

## 11. Acceptance Criteria

G proposal acceptance requires:
1. All ownership boundaries and state distinctions above are explicit and consistent with current B/C/D/F/H/I contracts.
2. Exact ContextVersion/Delivery/Adapter/Session/InferenceRequest/FinalRequestEvidence/Authorization/ForgetFence binding is specified.
3. Applied cannot be promoted from Delivered, Materialized or ACK alone.
4. Snapshot/Delta, CAS, replay, reconnect and Forget behavior are deterministic and idempotent.
5. Protected prompt regions and Agent policy are not writable by G.
6. Cross-module exact-version Applied package and digest are reconciled by C/G/H, with I/D/B evidence accepted only by their authorities.
7. Required conformance suites execute and pass before implementation acceptance; no test pass is claimed here.
8. Owner acceptance is recorded separately from proposal publication.

## 12. Change Authority

G alone changes Context semantics, ContextVersion, ChangeSet, reconciliation, Delivery Intent and Applied-record semantics. H changes BMCP wire/ACK/transport; C changes final-request evidence; I changes authorization and governance policy; D changes Canonical ForgetFence; B changes typed-reference semantics; PGA approves project-wide governance baseline. Any cross-boundary change requires versioned impact analysis and explicit decisions from every affected authority. This proposal itself is PROPOSED only.

## 13. Open Decisions

- Exact C/G/H Applied version + digest alignment: OPEN. G branch records acceptance of CGH-APPLIED-1.1 / CausalOrderProfile/1.0 and H schema target bmcp.applied-ack/1.1.0, but H's current exact formal decision artifact records an earlier package and explicitly says concrete schema freeze is OPEN. Exact same A package Blob acceptance across C/G/H must be proven.
- G consumer acceptance of BIH identity contract: OPEN / conflicting evidence. G has an issue-level acceptance statement in its Applied contract, while I's current approval register still lists G OPEN; reconcile exact artifact/version and fields.
- G validator and Applied persistence implementation consuming full 1.1 recovery evidence: TO_VALIDATE.
- CGH-01..20 and G-CO race/recovery tests: SPECIFIED / NOT RUN.
- H36/I36 live execution: NOT RUN.
- D atomic producer admission/fence/publication and Storage recovery: TO_VALIDATE / BLOCKED.
- Global Forget inventory seal, external targets, backup/restore evidence: OPEN.
- PGA external governance approval: GOVERNANCE-BLOCKED.
- Template availability: specified path 404 on main; no matching template found in G tree.

## 14. Explicit Non-Claims

This proposal does not claim Owner approval, project baseline approval, exact C/G/H 1.1 freeze, BIH consumer acceptance closure, H36/I36 or G conformance execution, production Applied persistence, live Adapter behavior, provider/model comprehension, global Forget completion, physical erasure, backup restore safety, storage atomicity, or production readiness. A Git commit of this proposal proves only publication of this PROPOSED artifact.
