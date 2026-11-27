# System Architecture Specification

- Document ID: SYS-ARCH-001
- Version: 1.0
- Source: [Normative source specification](../../../01-system-architecture/system-overview.md)
- Source revision: c3707831777feb14aedd7aea0eca1c162bf59fc6
- Chinese counterpart: [系统架构规范](../../zh-CN/01-system-architecture/system-architecture-specification.md)
- Status: DECIDED baseline with explicitly marked candidates and validation items

**Scope:** Logical system architecture; not a deployment or code-level design.

## 1. Product definition

AI Memory Brain is an independent memory infrastructure that captures experience, compiles durable memory assets, retrieves and activates relevant knowledge, and manages versioned memory context for Agents across sessions, models, and environments.

It is designed to preserve memory continuity even when the Agent implementation or underlying LLM changes.

## 2. Goals

- Durable, structured, traceable memory assets.
- Cross-session and cross-Agent memory reuse under explicit scope and permission.
- Memory formation from events, observations, documents, and user-provided information.
- Retrieval combining structured, lexical, semantic, temporal, and relational signals.
- Proactive memory activation based on structured Agent/environment telemetry.
- Brain-authoritative, versioned management of a dedicated memory region in Agent inference context.
- Explicit lifecycle, conflict, retention, forgetting, audit, and recovery semantics.
- Local-first operation with resource-aware model-assisted components where needed.

## 3. Non-goals

The Brain does not own:

- Agent planning, task decomposition, or action selection.
- Tool execution, browser/terminal control, or environment actuation.
- Agent safety policy, permission to perform external actions, or model guardrails.
- A specific LLM, Agent framework, prompt template, or proprietary hidden reasoning format.
- Skill execution. A Skill Library may be a separate subsystem that references memories.

## 4. Logical architecture

### 4.1 Memory Brain

Owns canonical memory identity and lifecycle:

- Domain semantics and canonical identifiers.
- Canonical memory persistence and version history.
- Entity and relationship management.
- Epistemic and temporal qualification.
- Provenance and evidence references.
- Retention and forgetting governance.

### 4.2 Memory Compiler

Transforms inputs into candidate and consolidated memory assets:

- Durable event ingress.
- Extraction and normalization.
- Entity resolution and relation proposals.
- Evidence and provenance attachment.
- Duplicate detection, consolidation, and conflict handling.
- Index/update event production.

The ingestion acknowledgement should not require synchronous LLM inference. Durable acceptance and semantic consolidation are separate stages.

### 4.3 Memory Runtime

Serves memory at interaction time:

- Retrieval routing and candidate generation.
- Activation policy evaluation.
- Bounded runtime working sets and caches.
- Context planning and sufficiency assessment.
- Context edits, versioning, reconciliation, and synchronization.

### 4.4 Agent Integration

Defines Brain-owned contracts and Agent-side execution:

- Structured telemetry mapping into a canonical schema.
- Context package delivery and capability negotiation.
- Adapter-side validation and application at inference boundaries.
- Explicit acknowledgement, rejection, and version reconciliation.

### 4.5 Cross-cutting infrastructure

- Storage and index infrastructure.
- Scope and permission enforcement.
- Consistency, idempotency, event replay, and recovery.
- Audit, observability, and performance measurement.

## 5. Logical data paths

### 5.1 Experience-to-memory path

Agent / Environment → Event Ingress → Durable Event Log → Memory Compiler → Canonical Memory Store → Index Updates → Runtime Availability

### 5.2 Memory-to-inference-context path

Agent Telemetry → Protocol Gateway → Memory Observer → Activation & Retrieval → Context Planner / Editor → Versioned Change Set → Adapter → Next Inference Boundary → Acknowledgement

### 5.3 Governance path

Authorized Request → Scope & Permission Check → Governance Policy → Canonical / Derived Data Actions → Index & Cache Reconciliation → Audit Record

## 6. Memory and context separation

- Canonical Memory is durable and authoritative.
- Memory Context is a scoped, versioned view for a particular Agent instance/task/environment.
- Applied Context records what the Adapter confirms it has installed at the agreed boundary.
- A memory may exist without being activated into any context.
- One canonical memory may appear in multiple contexts with different task-specific renderings.
- Removing a Context Entry does not delete its Canonical Memory.
- The Brain cannot assume that changing its managed memory region erases content already processed by a model.

## 7. Observation and activation model

The Brain uses structured telemetry as evidence of task state and likely memory needs. It does not require complete hidden chain-of-thought.

Canonical telemetry may include task state, intent, plan summary, active entities, pending actions, observations, outcomes, uncertainty, risk signals, and environment-state deltas.

Intent and plan fields are prospective state, not proof of outcomes. The Brain owns activation policy; Adapters translate Agent-native signals into the canonical schema.

**CANDIDATE:** combine asynchronous pre-activation during Agent work with synchronous checks before high-impact or irreversible actions. Trigger thresholds and scoring weights require validation.

## 8. Context application boundary

The Brain is the logical authority for the memory context it manages. The Adapter is the execution point that applies a package or change set.

The managed memory region must be explicitly delimited. It must not overwrite system/developer instructions, user-originated input, or Agent security policy. Changes are applied when the next inference context is assembled, not by assuming an in-flight inference can be rewritten.

## 9. Isolation model

Scope and permission are separate:

- Scope establishes ownership/namespace (user, project, Agent, Agent instance, session, environment).
- Permission determines allowed operations on resources within that scope.
- Environment identifiers must distinguish separate worlds, save files, tenants, or simulations where state can collide.
- Shared canonical memory does not imply shared working context or unrestricted access.

## 10. Deployment and implementation neutrality

**DECIDED:** logical subsystems do not imply separate processes, services, or Rust crates.

**CANDIDATE:** begin implementation as a modular monolith with clear internal contracts; split processes only when isolation, scaling, reliability, or deployment evidence justifies it.

## 11. Primary quality attributes

- Correctness and provenance integrity.
- Scope and permission isolation.
- Context version consistency and recoverability.
- Low and predictable retrieval/synchronization latency.
- Bounded CPU, memory, disk, and optional GPU consumption.
- Adapter interoperability and protocol evolution.
- Observable, reproducible Agent-level benefit.

Quantitative targets are **OPEN** until representative workloads and hardware baselines are defined.

## 12. Open architecture questions

1. What canonical memory granularity best supports event, claim, and evidence versioning?
2. Which telemetry fields are mandatory versus optional for each Adapter capability tier?
3. How should context sufficiency be measured across tasks without overfitting to one Agent?
4. What consistency guarantees are required between event log, canonical store, and indexes?
5. What is the minimum safe and useful local model-assisted compilation pipeline on 12–16 GB VRAM?
6. Which storage/index candidates win under representative mixed retrieval workloads?
7. What are the retention and physical-erasure guarantees for derived memories, caches, and backups?
