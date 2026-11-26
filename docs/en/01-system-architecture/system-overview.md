---
document_metadata:
  domain: architecture
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Classified Informative because the existing EN/ZH guides explicitly state they are explanatory and do not replace Owner specifications or ADRs. Owner-authorized source/mirror topology for AID-2026-11-26-GOV-DOC-01; not a formal approval record. Pre-metadata content blob: c372dc0f8a725ccfd972887c6c8631542c94665d. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "System architecture overview guide"
    canonical_scope_id: architecture/system-overview-guide
    canonical_scope_keywords:
      - system-overview
      - architecture-guide
      - logical-components
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "01-system-architecture/system-overview.md"
    en: null
    zh-CN: "docs/zh-CN/01-system-architecture/system-overview.md"
---
# AI Memory Brain — System Architecture Overview

- Document ID: DOC-SYS-001
- Version: 1.0
- Chinese counterpart: [系统架构总览](../../zh-CN/01-system-architecture/system-overview.md)
- Status: Explanatory architecture guide; does not replace Owner specifications or ADRs

## Canonical-source structure mapping (explanatory mirror)

This document is an explanatory guide, not a section-by-section replacement for the canonical source at `01-system-architecture/system-overview.md`. Its nine-section reader-oriented structure intentionally regroups the source's twelve sections. This mapping records the editorial difference; the canonical source remains authoritative for complete wording and semantics.

| Canonical source section | Coverage in this explanatory guide |
|---|---|
| 1. Product definition | 1. The project in one sentence |
| 2. Goals | 1. The project in one sentence; 5. Three primary workflows |
| 3. Non-goals | 2. What does the Brain own—and what does it not own? |
| 4. Logical architecture | 3. System at a glance; 4. The six major parts; 7. A–I architecture ownership |
| 5. Logical data paths | 3. System at a glance; 5. Three primary workflows |
| 6. Memory and context separation | 6. Five distinctions that must remain clear |
| 7. Observation and activation model | 4.3. Memory Runtime; 5.2. From memory to inference context |
| 8. Context application boundary | 4.4. Memory Context; 4.5. BMCP and Agent Adapter |
| 9. Isolation model | 2. What does the Brain own—and what does it not own?; 4.6. Security & Governance |
| 10. Deployment and implementation neutrality | 3. System at a glance; 8. Current architecture status |
| 11. Primary quality attributes | 8. Current architecture status |
| 12. Open architecture questions | 8. Current architecture status |

The regrouping is editorial only. It does not remove, narrow, or replace any canonical-source decision, candidate, validation item, or open question. Where this guide is shorter, consult the canonical source.

## 1. The project in one sentence

**AI Memory Brain is an Agent- and model-independent long-term memory infrastructure. It turns experience into traceable, manageable memory assets, then organizes relevant memories into context an Agent can use at an inference boundary.**

The central goal is continuity: Agents, models, sessions, and execution environments may change, but valuable memory should not disappear with them or remain trapped inside one Agent's prompt or private database.

## 2. What does the Brain own—and what does it not own?

### The Brain owns
- Receiving memory sources such as conversations, observations, documents, and events.
- Organizing sources into structured memories while preserving evidence and provenance.
- Managing canonical Memory identity, versions, relationships, conflicts, lifecycle and Forget Fence mechanics (Owner D); global authorization, retention/legal-hold, external-copy policy, target inventory and completion criteria belong to Owner I.
- Retrieving and activating relevant memories according to task and environment.
- Managing its dedicated Memory Context: add, update, remove, reorder, compact, and version changes.
- Recording whether an Adapter applied a context version at the agreed inference boundary.
- Enforcing Scope, Permission, security, audit, and recovery constraints.

### The Brain does not own
- Agent reasoning, planning, task decomposition, or action selection.
- Tool, browser, terminal, or environment execution.
- Authorization for an Agent to perform external actions.
- A specific LLM, model vendor, or Agent framework.
- Automatic conversion of model-generated content into facts.

**In short: the Agent decides what to think and do; the Brain manages what is remembered, why it is believed, when it is offered, and how it is governed or forgotten.**

## 3. System at a glance

~~~mermaid
flowchart TB
    Agent[Agent: reason, plan, act]
    Adapter[Agent Adapter: telemetry mapping and inference-boundary application]
    Protocol[BMCP: memory context protocol]
    Compiler[Memory Compiler: compile experience into memory]
    Brain[Memory Brain: canonical memory and lifecycle]
    Runtime[Memory Runtime: retrieval and activation]
    Context[Memory Context: task-oriented context]
    Governance[Security & Governance: identity, permission, forgetting, audit]
    Storage[Storage / Index / Cache: persistence and derived indexes]
    Agent <--> Adapter
    Adapter <--> Protocol
    Protocol <--> Compiler
    Protocol <--> Runtime
    Compiler --> Brain
    Brain --> Storage
    Storage --> Runtime
    Runtime --> Context
    Context --> Protocol
    Governance -. governs .-> Compiler
    Governance -. governs .-> Brain
    Governance -. governs .-> Runtime
    Governance -. governs .-> Context
~~~

The diagram shows logical relationships. It does not mean every box must become a separate process, service, or Rust crate.

## 4. The six major parts

### 4.1 Memory Brain — canonical memory authority
Owner D owns canonical Memory identity, versions, evidence/provenance links, relationships, lifecycle, canonical Forget mechanics and Forget Fence. Owner I owns global authorization, retention/legal-hold, external-copy policy, the global Forget target inventory and global completion criteria. The Memory Brain logical area aggregates these responsibilities without transferring either Owner's authority. Global Forget Completion is jointly determined by Owner D and every relevant execution Owner under a completion-evidence contract accepted by those Owners; neither D nor I may declare it unilaterally. The contract remains pending the relevant Owners' acceptance. It answers: What is this memory? Where did it come from? Which version is current? What evidence supports or contradicts it? Does it conflict with other memories? Is it still valid, and should it be archived or forgotten?

Global Forget Completion is jointly determined by Owner D and every relevant execution Owner, based on a completion-evidence contract jointly accepted by those Owners. Neither D nor I may declare global completion unilaterally. The contract remains pending the relevant Owners' acceptance; this direction is not evidence of that acceptance.

### 4.2 Memory Compiler — turning experience into memory
It receives raw events and content, then validates, extracts, normalizes, resolves entities, links evidence, handles conflicts, and consolidates candidate memories.

These states are distinct:
- **Accepted:** the source was durably accepted.
- **Compiled:** the compiler workflow processed it.
- **Canonical Committed:** it was committed to authoritative memory.
- **Indexed:** retrieval indexes were updated.

Acceptance does not mean a memory has been formed, and compilation does not mean indexing has completed.

### 4.3 Memory Runtime — serving memory during interaction
It retrieves candidate memories, evaluates activation value, maintains bounded working sets, and provides recommendations to the Context Manager. Runtime does not own Canonical Memory or Context Version authority.

### 4.4 Memory Context — the memory view needed for a task
It is neither the entire memory database nor the full prompt. It is a scoped, versioned set of memories assembled by the Brain for an Agent, task, environment, permission context, and budget. The Brain applies Add, Update, Remove, Replace, Reorder, and Compact operations to the region it manages. Changes take effect at the agreed next inference-context assembly boundary.

### 4.5 BMCP and Agent Adapter — connecting the Brain to Agents
BMCP defines messages, context delivery, capability negotiation, and acknowledgement semantics. The Adapter maps structured Agent telemetry to Brain contracts and applies Brain-managed context at the Agent's inference boundary. It must not rewrite the Agent's System, Developer, or original user content, nor bypass the Agent's own safety policy.

### 4.6 Security & Governance — cross-cutting controls
Identity, Scope, Permission, retention, Forget, audit, and recovery are system-wide constraints. They apply across ingestion, compilation, storage, retrieval, context delivery, and backup restoration.

## 5. Three primary workflows

### 5.1 From experience to memory

~~~text
Agent / Environment / User
        ↓
Event Ingress
        ↓
Durable Acceptance
        ↓
Memory Compiler (extraction, normalization, evidence linking)
        ↓
Canonical Memory (authoritative commit)
        ↓
Index Updates
        ↓
Available to Memory Runtime
~~~

### 5.2 From memory to inference context

~~~text
Agent Telemetry (task and environment signals)
        ↓
BMCP
        ↓
Retrieval & Activation
        ↓
Context Planner / Editor
        ↓
Context Version / ChangeSet
        ↓
Adapter Delivery
        ↓
Next inference-context assembly boundary
        ↓
Applied Acknowledgement
~~~

Applied proves that the Adapter applied the corresponding version at the agreed boundary. It does not prove that the model noticed, understood, or followed the memory.

### 5.3 Forget and revocation

~~~text
Authorized Forget Request
        ↓
Governance Authorization
        ↓
Forget Fence + Producer Barrier
        ↓
Block old work and late derivatives from publication
        ↓
Purge or suppress Canonical / Index / Cache / Context / Adapter / Backup
        ↓
Collect evidence from every target
        ↓
Global Forget Completion Decision
~~~

**Context Remove is not Forget.** Removing a memory from the current task context does not mean its canonical memory was deleted. Forget must also prevent old work, index rebuilds, cache fills, or offline Adapters from reintroducing forgotten content.

## 6. Five distinctions that must remain clear

| Commonly confused concepts | Correct distinction |
|---|---|
| Event / Memory / Claim | An Event is a captured occurrence or input; a Memory is a retained knowledge asset; a Claim is a proposition it contains or references. |
| Canonical Memory / Memory Context | The former is authoritative memory; the latter is a task-scoped, versioned view. |
| Context Remove / Forget | The former changes current context; the latter is a governed memory revocation and cleanup workflow. |
| Accepted / Applied | Accepted means durably received; Applied means the Adapter applied context at the agreed inference boundary. |
| Confidence / Relevance | Confidence measures support; Relevance measures usefulness for the current task. |

## 7. A–I architecture ownership

| Owner | Authority |
|---|---|
| A — Principal Integration | System integration, cross-module conflict resolution, final architecture decisions |
| B — Domain Model | Domain objects, identity semantics, canonical model |
| C — Agent Integration | Agent Adapter, inference boundary, final-request evidence |
| D — Memory Brain | Canonical Memory identity, versions, lifecycle, canonical Forget mechanics and Forget Fence; D-domain completion predicate |
| E — Memory Compiler | Ingestion, extraction, normalization, evidence, derivative production |
| F — Memory Runtime | Retrieval, activation, working sets, cache |
| G — Memory Context | Context Version, ChangeSet, Delivery intent |
| H — BMCP Protocol | Protocol envelope, messages, versions, acknowledgement semantics |
| I — Security & Governance | Global authorization, retention/legal-hold, external-copy policy, global target inventory and global completion criteria; policy/evidence requirements for joint completion |

Cross-module collaboration does not transfer domain authority. Storage/Consistency provides durable transaction execution; it does not replace domain owners' authority over semantics.

## 8. Current architecture status

- **DECIDED:** The Brain is independent of Agents/models; Canonical Memory and Context are separate; memory is data rather than instruction authority; Scope and Permission are separate; Forget must cover derived representations.
- **CANDIDATE:** A modular Rust monolith for the first deployment; SQLite WAL as the first storage prototype; specific indexes, vector retrieval, inference backends, and transport technologies.
- **OPEN / BLOCKED:** Fact/Claim ADR; atomic D/E/Storage producer admission, Forget Fence, dependency registration, and publication; application-level JF-10 and COC recovery; end-to-end Applied proof; complete Global Forget target closure.
- **TO_VALIDATE:** Real concurrency, crash/recovery, index anti-resurrection, cache invalidation, resource budgets, and P95/P99 performance.

This guide describes the architecture baseline and candidate implementation direction. It does not claim the system has been implemented or passed production acceptance.

## 9. Recommended reading path

1. [Architecture Invariants](../../../00-governance/architecture-invariants.md)
2. [Canonical Terminology](../../../00-governance/terminology.md)
3. [Logical Component Map](../../../01-system-architecture/component-map.md)
4. [Subsystem Responsibility Matrix](../../../01-system-architecture/responsibility-matrix.md)
5. [Domain Model Overview](../../../02-domain-model/domain-model-overview.md)
6. Detailed Owner specifications
7. [Technology Architecture Overview](../13-engineering-decisions/technology-architecture-overview.md)

---
**Chinese counterpart:** [AI Memory Brain 系统架构总览](../../zh-CN/01-system-architecture/system-overview.md)
