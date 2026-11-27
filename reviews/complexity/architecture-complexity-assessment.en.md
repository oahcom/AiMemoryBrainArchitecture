# Architecture Complexity Assessment and Budget (English)

- Assessor: X — Principal Architecture Complexity Assessment
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Exact baseline: `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Date: 2026-11-17
- Method: Static, source-grounded architecture assessment
- Status: **PROVISIONAL — NOT PROVEN**
- Scope: This report does not approve architecture, override Owner authority, certify implementation/performance/security, or claim complete review of every Owner branch.
- assessor: X — Principal Architecture Complexity Assessment
- assessed_version: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- evidence_baseline: `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001:reviews/complexity/architecture-complexity-assessment.en.md`
- signature_attached: 2026-11-27 by the AID-2026-250 rework — retrospective attachment, not a contemporaneous signature

## 0. Executive conclusion

**Is the current architecture complexity within an implementable, verifiable and maintainable range? NOT PROVEN.**

The central issue is not the number of modules. It is the interaction of cross-module state and proof semantics. End-to-end Forget depends on D canonical fence/producer barrier, E admission/derived registration/publication gate, F index watermarks and in-flight recall, G Context versions/delivery, H Adapter Applied/clear acknowledgement, I authorization epochs/retention/global completion, and Storage/Consistency atomic persistence and recovery. No local success can prove global completion.

System interaction and data-flow specifications deliberately distinguish Accepted, Compiler Completion, Canonical Commit, Index Applied, Context Applied and Forget completion. This separation is correctness-relevant, but creates many proof objects, states, cursors and cross-owner responsibilities. They must not be collapsed into a generic Success. Conversely, making each concept a separate service, queue, database, version or protocol would multiply complexity without demonstrated benefit.

**Current rating: High complexity; controllability not proven.** Continue controlled contract closure; do not infer readiness for a complete distributed implementation or freeze of all contracts.

## 1. Evidence, scope and method

### 1.1 Evidence directly inspected

- Main HEAD: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Issue #43: System-wide Architecture Consolidation & Feasibility Review, Open.
- PR #28: Draft/Open. Its description states repository-wide bilingual coverage is incomplete; C/G/H Applied and Storage/Consistency detailed contracts remain incomplete; ADR-001 is blocked; H36 and C-FR tests are NOT RUN; JF-10 is P0 OPEN / NOT IMPLEMENTED / NOT RUN.
- `01-system-architecture/component-interactions.md` and `data-flows.md`: end-to-end event acceptance, asynchronous compilation, canonical authority, index projection, recall, Context version/delivery/Applied and Forget flows.
- `reviews/integration/phase-2-defg-cross-session-reconciliation.md`: D/E/F/G branch reviews were not independent external sign-offs; designs remain candidate contracts and P0/P1 plus missing H/I contracts prevent freeze.
- D Owner-branch `forget-fence-and-completion-contract.md` (Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`) and `commit-cursor-semantics.md` (Blob `4688a0ca487bf4d853c7f0220408abe8d743d159`).
- E Owner-branch `forget-fence-and-derived-registration.md` (Blob `00e37ba56596e710513c8d0568acd79141d9101b`) and `accepted-receipt-and-idempotency-contract.md` (Blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46`).

Owner-branch documents are treated as candidate design evidence, not as merged, approved or implemented specifications. A failed branch-path read is not evidence that the document does not exist; that area is marked evidence-limited.

### 1.2 Scoring model

Each dimension is scored 1–5: 1 Low, 2 Moderate, 3 Significant, 4 High, 5 Extreme. Scores represent complexity to govern and verify—not quality, effort, probability of failure or maturity. Confidence is High/Medium/Low. Where authoritative contracts were unavailable, scores are provisional and confidence is reduced.

Dimensions:
- Internal: responsibilities, algorithms and local state.
- Dependency: cross-owner dependencies, shared contracts and fan-out.
- State: states, versions, identities, transitions and invariants.
- Concurrency: races, linearization, locks/transactions, retries and duplicate delivery.
- Recovery: crash windows, replay, repair and backup/restore.
- Verification: test layers, state space, fault injection and evidence.
- Operational: deployment, observability, upgrade and recovery.
- Cognitive: comprehension, change propagation, owner coordination and documentation.

Do not sum the eight scores into a project-wide total. Matrices locate bottlenecks; the overall conclusion follows critical paths, coupling and evidence gaps.

## 2. Module complexity matrix

Score order: Internal / Dependency / State / Concurrency / Recovery / Verification / Operational / Cognitive.

| Module/capability | Eight scores | Confidence | Evidence and dominant multipliers |
|---|---:|---|---|
| A Architecture governance/integration | 3/5/4/3/3/5/2/5 | Medium | Owner authority boundaries, blocked ADRs, bilingual/evidence traceability, PR/review gates; broad change propagation |
| B Domain Model | 4/5/5/3/3/5/2/5 | Medium | Fact/Claim, Scope, Principal/Actor, identity and revision are system-wide semantic roots; unresolved ADR/P0 propagates rework |
| C Agent Integration | 3/5/4/4/3/5/4/4 | Low-Medium | Agent request/inference boundary and Adapter Applied proof depend on H/G; C/G/H contracts and tests incomplete |
| D Memory Brain | 5/5/5/5/5/5/3/5 | Medium-High | Canonical lifecycle, commit cursor, Forget fence, dependency inventory, producer barrier and completion proof |
| E Memory Compiler | 5/5/5/5/5/5/4/5 | Medium-High | Durable admission, layered receipts, lease/retry/replay, derived registration and final publication gate; D/Storage atomic registration remains open |
| F Memory Runtime | 4/5/5/5/4/5/4/4 | Low-Medium | Multi-path retrieval, index watermark, freshness, permission filtering, in-flight recall vs Forget; detailed source baseline incomplete |
| G Memory Context | 4/5/5/4/4/5/4/4 | Low-Medium | Context version, ChangeSet, delivery retry, Adapter Applied, reconnect/snapshot/reconciliation; Applied depends on H/C |
| H BMCP / Adapter protocol | 4/5/5/5/5/5/4/5 | Low | Wire identity, capabilities, acknowledgement stages, boundary receipt, offline/reconnect and clear acknowledgement; insufficient main-branch normative evidence |
| I Security / Governance | 4/5/5/5/5/5/4/5 | Low | Principal/permission epoch, revocation, retention, global Forget, backup/external copies and physical erasure; insufficient normative evidence |
| Storage / Consistency | 5/5/5/5/5/5/5/5 | Low | Atomicity across authoritative state, outbox, fence/registration/publication, recovery and blocked topology ADR; detailed contract/topology unresolved |

D/E have directly inspected Owner source files, so their confidence is higher. H/I/Storage scores are inferred from responsibilities referenced by other modules and system flows; their Owners must calibrate these scores against authoritative contracts and technology decisions.

## 3. Cross-module complexity matrix

| Cross-module mechanism | Eight scores | Confidence | Complexity drivers / blockers |
|---|---:|---|---|
| Forget fence → producer admission → derived registration → publication gate | 5/5/5/5/5/5/5/5 | High | Registration and final publication must close fence races; local checks cannot replace an authoritative atomic boundary; D/E/Storage/I participate |
| Canonical commit → index watermark → retrieval freshness | 4/5/5/4/4/5/4/4 | Medium | Cursor, aggregate revision, partition watermark and coverage/schema version are not interchangeable; index proves only a contiguous applied prefix |
| Context desired version → delivery → Adapter Applied | 4/5/5/5/4/5/4/5 | Medium | Desired/applied separation, idempotent retries, stale ACKs, offline operation, snapshot catch-up and inference-boundary proof |
| Authorization/revocation epoch across operations | 4/5/5/5/5/5/4/5 | Low | Authorization may be revoked while asynchronous work runs; check point, epoch binding and invalidation propagation must be defined |
| Global Forget completion and residual evidence | 5/5/5/5/5/5/5/5 | Low-Medium | Canonical, derivatives, indexes, cache, context, adapter, replicas and backups have different completion semantics |
| Durable acceptance / outbox / replay | 4/5/4/5/5/5/4/4 | Medium | Accepted must correspond to recoverable data and processing intent; duplicate delivery must not duplicate events or side effects |
| Cross-owner bilingual contract/version traceability | 3/5/4/2/3/5/2/5 | Medium-High | Source Blob, translation parity, decision status, PR manifests and Owner authority create ongoing coordination cost |

**Finding:** The full Forget chain and its races with Publication and Applied are more complex than any one module. They require an explicit system-level budget rather than being hidden inside local module scores.

## 4. State-space analysis and combinatorial growth

### 4.1 Proof objects that must remain distinct

At minimum:
1. AcceptedReceipt: event and processing intent are durably recoverable.
2. ProducerRegistrationReceipt: producer work is admitted to D's barrier inventory.
3. CompilerCompletionReceipt: a compile run has a durable terminal outcome.
4. DerivedRegistrationReceipt: derivative lineage is registered.
5. CanonicalCommitReceipt: canonical mutation is committed.
6. IndexWatermark: a specified index partition has applied a contiguous prefix through a canonical cursor.
7. Context desired version and delivery state.
8. Adapter Applied acknowledgement: a specified Context version took effect at the agreed inference assembly boundary.
9. Forget target acknowledgement/global completion proof: applicable targets completed under I's policy or have approved residuals.

These prove different facts. Do not collapse them into Success or infer one from another.

### 4.2 Multipliers

- Each state machine intersects with permission epoch, scope, version/cursor, retry count, durability and failure windows.
- Independent sequences (CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark, ForgetFenceCursor, ContextVersion, PermissionEpoch) create incorrect comparisons and hidden coupling if their domains are not explicit.
- Combining online/offline, retryable/terminal, success/reject/partial states creates multiplicative test space.
- Duplicating state, receipt, retry and audit protocols per Owner multiplies maintenance.

### 4.3 Containment rules

Architecture must define:
- Unique owner, scope, monotonicity and comparison rules for every ID/cursor/revision/epoch.
- One authoritative writer per state machine; consumers hold explicitly labelled projections/caches/observations only.
- Transition tables with preconditions, durable point, idempotency key, failure outcome, retry and recovery action.
- Proof-object issuer, subject, scope, generation/version, durability, freshness and non-claims.
- Fail-closed behavior for stale/unknown/ambiguous cases; no fabricated completion state.

## 5. Concurrency and recovery analysis

### 5.1 Critical races

| Race | Required safety property | Complexity |
|---|---|---|
| Forget fence vs new Producer Admission | After fence, old-generation work cannot be admitted outside the barrier inventory | Extreme |
| Producer registration vs fence/barrier seal | No unregistered-but-publishable producer window | Extreme |
| Derived publication vs Forget | Final publication coordinates fence/permission checks at authoritative durable boundary | Extreme |
| In-flight Recall vs Forget | After fence, suppressed candidates cannot be returned; response finalization has a defined linearization point | High |
| Canonical commit vs index apply | Watermark advances only across a contiguous prefix | High |
| Context delivery vs new version/Forget | Old delivery/ACK cannot roll back a newer version or reintroduce removed content | High |
| Permission revocation vs async worker | Worker cannot perform sensitive side effects using stale authorization | Extreme |
| Crash vs partial cleanup | Replay is monotonic/idempotent; partial completion is never reported as global completion | Extreme |

### 5.2 Recovery is architectural

Define behavior for crashes after durable accept but before enqueue; compiler completion but before lineage registration; registration but before final publication; canonical commit but before index update; Context commit but before delivery; Adapter apply but before ACK; Forget fence but during partial target cleanup; backup restore that reintroduces old data; and recovery that revives old workers/messages.

Recovery evidence must prove that fence/generation remains effective, completed targets do not regress, repeated execution is safe, and stale snapshots cannot overwrite authoritative state. Available evidence does not close all these windows; recovery complexity is high and controllability is NOT PROVEN.

## 6. Hotspots, multipliers and bottlenecks

### Hotspots
- H1: D/E/Storage producer registration and publication gate.
- H2: I/D/F/G/H/Storage end-to-end Global Forget.
- H3: C/G/H Applied proof and inference boundary.
- H4: D/F Canonical cursor and IndexWatermark.
- H5: B Fact/Claim, Scope and Principal/Actor foundation.
- H6: Storage topology, transaction/log/outbox and recovery.
- H7: Repository-wide bilingual specifications, Owner Blob binding, status synchronization and PR review.

### Complexity multipliers
- The same fact is expressed by different Owners using duplicate names, states or receipts.
- Logical boundaries are implemented as separate processes/services/databases/queues by default.
- Each module independently reinvents retry, idempotency, audit, version and reconciliation frameworks.
- Multiple storage topologies, index backends and deployment modes are supported without validated demand.
- Downstream schemas are frozen while identity/Scope/Fact-Claim ADRs remain open.
- Documentation coverage, structural CI or simulated multi-role review is mistaken for semantic parity or feasibility proof.

### Bottlenecks
- Unresolved B/ADR foundation propagates into D/E/F/G/H/I.
- Undefined Storage atomic boundary prevents proof of critical D/E publication correctness.
- Unclosed H Applied and I Forget/retention contracts block G/C and global completion acceptance.
- End-to-end state-space and fault-injection evidence is incomplete.

## 7. Complexity budget and thresholds

These are X recommendations, not approved project SLAs or Owner decisions.

### 7.1 Module budget

- One authoritative writer per module; projections/caches must not become implicit second authorities.
- Budget one primary durable state machine per module; additional machines require an independent fault domain or correctness rationale.
- Every ID/cursor/version/epoch has one semantic definition and comparison rule; no same-name/different-meaning or cross-domain comparison.
- Each cross-module workflow has one traceable operation ID, one global state owner and a finite enumerated participant set.
- New service/database/message system/protocol must demonstrate why a modular monolith or existing infrastructure is insufficient.

### 7.2 Testing budget

Minimum layers:
1. Unit: local transitions, pure rules and boundaries.
2. Component: persistence/local transaction, idempotency, outbox and projection.
3. Contract: inter-owner schemas, receipts and state semantics.
4. State-space: valid/invalid transitions, duplicate, out-of-order, expired and partial success.
5. Concurrency: races around linearization and concurrent admission/publication/Forget.
6. Fault injection: crash before/after each durable boundary, timeout, partition and lost ACK.
7. Recovery: replay, checkpoint, backup/restore and stale workers/messages.
8. E2E: accept → compile → canonical → index → recall → context → Applied; plus complete Forget chain.

**Threshold:** Every P0/P1 invariant has at least one direct negative test; every durable boundary has crash-before/crash-after tests; every cross-module state machine covers duplicate, out-of-order, retry, partial failure and recovery. Critical safety invariants cannot rely on happy-path E2E alone.

### 7.3 Operational budget

First implementation phase: one modular-monolith deployment, one authoritative database and one recoverable work/outbox mechanism; indexes may be rebuildable projections. Monitor operation/correlation IDs, queue age, retries/DLQ, watermark lag, fence generation, reconciliation backlog, Applied lag, Forget residuals and backup/restore outcomes.

Do not initially introduce multi-database sharding, cross-region active-active, a microservice mesh or multiple message buses absent measured throughput, isolation, availability or regulatory needs.

### 7.4 Cognitive budget

- One glossary as the canonical terminology entry point.
- One cross-module protocol registry: owner, status, linearization point, proof object and consumers.
- One global state/cursor registry; prohibit scattered duplicate definitions.
- Define each decision only in its authoritative Owner document; other modules reference stable IDs instead of copying semantics.
- Maintain bilingual counterparts in the same change set; distinguish normative source, reader guide, translation and approval status.

## 8. Simplification recommendations and disposition

### MUST PRESERVE — correctness-required
- Separate canonical authority from derived projections.
- Keep Accepted, Canonical Commit, Index Applied, Context Applied and Forget completion proofs distinct.
- Forget fence, producer barrier, derived dependency registration and final publication gate.
- Scope/Principal/Permission boundary checks and revocation epoch.
- Idempotency, durable work intent, recoverable replay and stale-generation rejection.
- Contiguous-prefix index watermark semantics and exact Adapter boundary proof for Applied.
- Explicit Forget policy for backups/replicas/external copies.

### CAN SIMPLIFY
- Deploy logical Owner modules as a modular monolith initially; preserve module interfaces and transaction boundaries without network separation.
- Share a durable work/outbox/lease/retry framework while keeping domain state distinct.
- Use one cross-module operation envelope/correlation convention; add specialized fields only when needed.
- Start with a small set of explicit index types; do not create a service per retrieval strategy.
- Treat rebuildable indexes, caches and working sets as projections, not copies of canonical lifecycle.
- Use enumerated transition tables instead of repeating the same state machine in prose.

### CAN DEFER
- Microservice decomposition, cross-region active-active and complex physical multi-tenant isolation.
- Simultaneous operation of many pluggable vector/graph/search backends.
- Adaptive/auto-tuned complex retrieval fusion and learned policies.
- Advanced multi-tier checkpointing, compaction and backup-generation optimization (but basic backup/restore and Forget constraints cannot be deferred).
- Multi-stage Agent prediction and complex proactive activation; first validate bounded recall/context.

### REASSESS
- Whether each cursor/revision/epoch has an independent semantic need or duplicates generation.
- Required scope and throughput/locking cost of a global CanonicalCommitCursor.
- Exact producer-barrier participant set, seal protocol and linearization point.
- Whether Applied needs multiple intermediate ACKs or a smaller verifiable set.
- Whether physical erasure, logical suppression, backup expiry and external-copy proof should be layered rather than one global state.
- Whether ownership boundaries create excessive cross-module round trips; only relevant Owners may approve changes.

### MUST NOT INTRODUCE
- Abstraction layers, plugin frameworks, event buses or services justified only by hypothetical future extensibility.
- Multiple writable authoritative copies of the same data.
- Distributed transactions/global locks/global clocks without evidence-backed need.
- A generic Success that collapses Accepted/Applied/Forget completion.
- Timed retry/eventual consistency without generation/fence protection against stale work.
- Removal of necessary safety checks, audit or recovery proof merely to lower scores.

## 9. Modular-monolith suitability

**Recommended as the first engineering form.** Retain logical module/Owner boundaries, interfaces, domain state machines and contract tests, while deploying in one process, one unit and one authoritative database. Use local transactions, outbox, background workers and rebuildable projections; enforce boundaries through module APIs rather than network calls.

D/E/F/G core logic, internal BMCP gateway handling, governance policy execution, index projections and Context management are suitable. The Adapter should retain an independent boundary in the Agent runtime; external model/tool calls and future integrations remain external. Split services only after measured load, fault-isolation, security-boundary or deployment-autonomy evidence.

A modular monolith does not remove concurrency/recovery complexity, but reduces network partitions, distributed transactions, version negotiation, deployment orchestration and cross-service observability costs.

## 10. Architecture-stage vs implementation-stage work

**Must resolve at architecture stage:**
- Conflicting authoritative identity, Scope, Fact/Claim, cursor/revision/epoch semantics.
- Forget races with Admission/Registration/Publication and undefined linearization points.
- Confused proof boundaries among Applied, Index watermark, Canonical commit and Forget proof.
- Irrecoverable durable windows and read/write paths unable to detect stale generations.
- Owner responsibility gaps or dual authority.
- Unapproved topology/technology choices treated downstream as settled facts.

**Can be resolved during implementation:**
- Concrete lock types, SQL statements, index parameters, queue batch sizes and retry intervals, provided correctness contracts are defined.
- Monitoring products, deployment pipelines, alert thresholds and capacity parameters.
- Algorithm/cache/performance optimization within frozen contracts.
- Internal code structure that does not change external semantics.

## 11. X-proposed complexity-related architecture constraints

- X-CX-001: Register owner, scope, monotonicity, comparison rule and authoritative durable point for every state/cursor/revision/epoch.
- X-CX-002: Register participants, operation ID, linearization point, retryable stages, terminal states and recovery action for every cross-module operation.
- X-CX-003: Every Receipt/Manifest/Applied/Watermark states issuer, subject, scope, generation/version, durability, freshness and non-claims.
- X-CX-004: Logical module boundaries do not imply separate services; service decomposition requires quantified demand and operational budget.
- X-CX-005: Every P0/P1 concurrency/recovery invariant is tied to negative tests and fault-injection evidence.
- X-CX-006: Projections/caches/indexes cannot be second authorities; stale state must be detectable and rebuildable.
- X-CX-007: Any global completion claim is proven by the authorized Owner against the full target inventory and residual policy.
- X-CX-008: Unapproved ADRs/candidate contracts cannot serve as implementation freeze baselines.

These are X recommendations, not automatically project norms; A and relevant Owners must review them through governance.

## 12. Required questions answered

A. Most complex modules: D, E and Storage/Consistency; H/I are also high-complexity candidates given cross-module responsibilities and evidence gaps.  
B. Most complex cross-module mechanism: Forget fence–producer barrier–derived registration–publication gate–global completion.  
C. State-space explosion: state machines × cursors/epochs × retry/duplicate/out-of-order × crash windows × partial completion.  
D. Correctness-required complexity: authority boundaries, identity/permission, durable admission, fences, idempotency, proof separation, recovery and auditable residuals.  
E. Over-engineering risks: premature service decomposition, duplicated retry/outbox/audit/version frameworks, excess abstractions and unsupported multi-backend designs. Not every complex mechanism can currently be labelled over-engineering.  
F. Defer: microservices, active-active, multiple backends, adaptive retrieval and advanced proactive activation.  
G. Modular monolith: suitable for first phase while retaining logical Owner and contract boundaries.  
H. Future growth: Forget target types, index partitions/rebuilds, Agent/Adapter count, revocation propagation, backups/external copies, bilingual and evidence-version traceability.  
I. Testing/maintenance: high and not yet proven sustainable; complete cross-module concurrency/fault-injection and regression evidence is absent.  
J. Small-team failure points: D/E/Storage publication atomicity; I/D/F/G/H Forget completion; C/G/H Applied proof; and propagation of B foundation changes.

## 13. Acceptance gates and final disposition

NOT PROVEN may become an evidence-backed CONDITIONAL PASS only after:
1. Authorized resolution of B's P0 identity/Scope/Fact-Claim ADR and synchronized references.
2. D/E/Storage define and test atomic producer admission, dependency registration, barrier seal and publication gate.
3. H/C/G align Applied issuer, Adapter boundary, version, lost ACK, reconnect and stale ACK contracts and tests.
4. I/D/F/G/H/Storage define Global Forget target inventory, revocation, backup/external copies, residual exceptions and completion proof.
5. Storage topology/transaction/recovery ADR is explicit and crash/replay/restore evidence exists.
6. Each P0/P1 invariant has unit, contract, concurrency and fault-injection coverage; E2E includes normal and partial-failure paths.
7. Independent review inspects actual Owner source contracts, integrated versions and test results—not merely reader guides, PR descriptions or simulated-role reports.

Until that evidence exists, **do not claim architecture complexity is proven implementable, verifiable or maintainable. Final disposition: NOT PROVEN.**

## 14. Sources and exact revisions

- Main baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Issue #43: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43
- PR #28 (Draft): https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28
- D Forget contract Blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D cursor contract Blob: `4688a0ca487bf4d853c7f0220408abe8d743d159`
- E Forget/publication contract Blob: `00e37ba56596e710513c8d0568acd79141d9101b`
- E receipt/idempotency contract Blob: `5ca77a5b48e69afb3bc81429baf538be7dce4d46`
- System interaction/data-flow specifications and Phase 2 reconciliation report were read from the stated main baseline.
