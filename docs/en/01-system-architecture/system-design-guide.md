# System Design Guide — Principles, Interactions, and Quality

- Document ID: DOC-SYS-DESIGN-001
- Version: 1.0
- Source: 00-governance/design-principles.md and 01-system-architecture/*
- Chinese counterpart: [系统设计指南](../../zh-CN/01-system-architecture/system-design-guide.md)
- Status: Explanatory guide; detailed source specifications remain authoritative

## 1. How to read the system architecture

The system architecture describes logical responsibilities and contracts. It does not automatically prescribe process boundaries, microservices, or Rust crates. A box in a component diagram means “this responsibility exists,” not “deploy this as a separate service.”

Components communicate through explicit contracts. An interaction may be an in-process call, durable message, stream, or protocol request; the selected deployment topology remains a separate engineering decision.

## 2. The 16 design principles

| ID | Principle | Practical meaning |
|---|---|---|
| P-01 | Brain authority over memory | Brain owns canonical memory, lifecycle, provenance, relations, and its managed Context |
| P-02 | Agent/model independence | No dependency on one Agent framework, model family/vendor, prompt format, or inference API |
| P-03 | Brain-defined contracts | Adapters map Agent-native state to stable Brain contracts |
| P-04 | Explicit domain semantics | Event, Memory, Fact, Entity, Relation, and Evidence are not interchangeable |
| P-05 | Provenance by construction | Derived memory retains source and derivation lineage |
| P-06 | Temporal correctness | Event time, recording/ingestion time, and validity time remain distinct |
| P-07 | Intent is not outcome | Plan/prediction/pending action is not a completed outcome without evidence |
| P-08 | Canonical Memory vs Context | Context is a scoped view; editing it does not mutate canonical memory |
| P-09 | Inference-boundary synchronization | Context changes take effect at a defined future assembly boundary |
| P-10 | Explicit application ACK | Delivery, receipt, and Applied are distinct; Applied does not prove model attention |
| P-11 | Memory is data, not instruction | Memory cannot gain System/Developer authority or override Agent safety policy |
| P-12 | Scope isolation | User/project/Agent/session/environment boundaries are explicit |
| P-13 | Governed Forget | Context removal is not deletion; Forget covers applicable derivatives and backups |
| P-14 | Preserve conflict | Conflicting claims retain sources, time, epistemic status, and resolution history |
| P-15 | Measured performance | Latency, recall quality, resource use, and Agent benefit require reproducible measurement |
| P-16 | Logical architecture first | Responsibility boundaries do not automatically imply process/service/crate boundaries |

## 3. Component interaction rules

1. The primary owner defines semantics and authoritative state.
2. Supporting components may validate, transform, transport, or cache, but cannot create a competing authority.
3. Every external boundary checks identity, Scope, Permission, schema, and resource limits.
4. Asynchronous work has durable correlation and retry semantics.
5. State-changing retries are idempotent within their declared key scope.
6. MCM serializes Context version changes; Synchronization tracks delivery, not Context semantics.
7. Acknowledgements state only what was actually observed.

## 4. Main data paths

### Experience to canonical memory

~~~text
Agent / Environment / User
        ↓
Gateway and authorized Event Ingress
        ↓
Durable Event + Accepted Receipt + Compile Intent
        ↓
Compiler validation, normalization, extraction
        ↓
Evidence / Provenance / candidate assets
        ↓
D canonical lifecycle and version commit
        ↓
Index and projection publication
        ↓
Runtime availability
~~~

### Memory to inference context

~~~text
Agent Telemetry / Recall
        ↓
Authorization and Scope resolution
        ↓
Retrieval candidates with evidence/freshness
        ↓
Activation recommendation
        ↓
G Context planning and version commit
        ↓
H delivery protocol
        ↓
C/H Adapter at next inference assembly boundary
        ↓
Applied attestation (only if proof predicates pass)
~~~

### Forget and revocation

~~~text
Authorized request
        ↓
I policy and identity checks
        ↓
D durable Forget Fence / target inventory
        ↓
E/F/G/H/Storage target suppression and cleanup
        ↓
Per-target evidence and exception assessment
        ↓
I global completion decision
~~~

## 5. Synchronous and asynchronous work

| Interaction | Default | Reason |
|---|---|---|
| Authentication/schema/permission validation | Synchronous | No unauthorized operation proceeds |
| Durable Event acceptance | Synchronous to durable receipt | Caller receives a truthful acceptance result |
| Semantic compilation | Asynchronous | Model latency/outage must not block ingestion |
| Index/cache propagation | Asynchronous | Derived and rebuildable |
| Explicit Runtime Recall | Synchronous and bounded | Agent needs timely candidates |
| Background proactive recall | Asynchronous | Avoid blocking Agent task loop |
| Context version commit | Atomic MCM operation | One authoritative sequence |
| Context delivery | Asynchronous | Adapter may be offline |
| Applied acknowledgement | After boundary; reported asynchronously | Evidence follows actual application |
| Forget propagation | Durable staged workflow | Multi-target cleanup and recovery |

## 6. System-level failure containment

| Failure | Expected containment |
|---|---|
| Gateway unavailable | External operations unavailable; canonical data unchanged |
| Ingestion/storage failure | No Accepted receipt unless durable acceptance completed |
| Compiler/model failure | Accepted Events remain durable and pending/retryable |
| Canonical Store failure | Stop canonical mutations; no false success |
| Index/cache failure | Explicit degradation or safe fallback; canonical data remains authoritative |
| Retrieval failure | Explicit timeout/partial result; no implied Context mutation |
| MCM failure | No new Context version; last committed version remains authoritative |
| Sync/Adapter failure | Delivery pending; no false Applied |
| Governance failure | Fail closed for protected operations |
| Recovery/observability failure | Must not silently violate audit or consistency obligations |

## 7. Quality priorities

The Brain must be evaluated as memory infrastructure in real Agent workflows, not merely as a vector-search benchmark. Priorities are:

1. Correctness and epistemic integrity.
2. Scope isolation, authorization, and privacy.
3. Canonical/Context consistency and recoverability.
4. Provenance integrity and governed Forget.
5. Predictable latency and bounded resource use.
6. Adapter interoperability and evolvability.
7. Availability and fault containment.
8. Useful memory activation and measurable Agent-level benefit.
9. Operability, observability, and testability.

These priorities can trade off. For example, stronger provenance and authorization may add latency; caching may reduce latency but increase staleness risk; larger Context may improve coverage but consume tokens and distract the Agent.

## 8. Measurement rules

Numerical budgets remain OPEN until representative workloads and hardware baselines are declared. Every benchmark must state hardware, software revision, model/quantization, corpus, scope distribution, concurrency, query mix, cache state, arrival rate, duration, correctness labels, sample count, and percentile method.

Measure ingestion durability, compilation queue age/stage latency, Recall p50/p95/p99, activation false positives/misses, Context commit conflicts and token budget, delivery/Applied lag, authorization latency, Forget suppression latency, CPU/RAM/disk/GPU/VRAM, provenance coverage, scope leakage, and Agent-level utility.

No performance multiplier or quality improvement is an architectural fact without a reproducible comparison.

## 9. Acceptance approach

Use layered verification:
- Contract tests for schemas, ownership, statuses, and compatibility.
- Invariant/property tests for non-negotiable semantics.
- Integration tests for cross-component sequencing.
- Concurrency tests for version and race safety.
- Fault injection for crash/recovery and failure isolation.
- Security tests for isolation, authorization, and prompt injection.
- Performance tests for latency, throughput, and resource bounds.
- Agent-task evaluation for end-to-end utility.
- Governance tests for Forget, retention, backup, and external recipients.

## 10. Detailed source specifications

- [Design Principles](../../../00-governance/design-principles.md)
- [Component Interactions](../../../01-system-architecture/component-interactions.md)
- [Data Flows](../../../01-system-architecture/data-flows.md)
- [System Boundaries](../../../01-system-architecture/system-boundaries.md)
- [System Quality Attributes](../../../01-system-architecture/system-quality-attributes.md)

This guide is a reader-oriented synthesis. It does not replace detailed contracts or claim that unmeasured targets have been achieved.
