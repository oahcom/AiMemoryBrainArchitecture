# Session G — Three-Party, Six-Dimension Architecture Review

- Date: 2026-11-16
- Subject: Session G Memory Context Manager architecture (six design documents)
- Review type: static document-level adversarial review; not implementation, security certification or runtime test
- Status: **Conditional Pass — coherent candidate architecture; cross-module contracts and proof details remain open**

The three perspectives below are architecture, engineering, and security/reliability review lenses. This report does not claim three independent human/model signatures.

## 1. Executive assessment

G establishes the required authority boundary: Brain owns desired Context membership, ordering, eligibility, budget and immutable version sequence; Adapter executes at the next inference assembly boundary; Agent retains reasoning and action authority. Context is neither the complete Canonical Store nor a full prompt or Agent Working State.

Strengths:
- immutable Context Versions and atomic Change Sets with Base/Target;
- serialization/CAS, idempotency and replay;
- separate Context, Delivery and Entry lifecycles;
- Forget/revocation tombstones blocking before asynchronous cleanup;
- Applied proof tied to the actual final inference request boundary;
- sufficiency based on coverage/evidence, not Top-K.

Suitable for controlled H/I integration design. Not sufficient to freeze BMCP wire schema, generic Scope schema, global Forget guarantee or Tier-1 digest format.

## 2. Six dimensions

### 1. Architecture and responsibility boundaries — Pass with conditions

G owns desired Context, not canonical memory or Agent prompt assembly. F retains retrieval/activation; G consumes and revalidates. H owns transport and Adapter application; G defines semantic snapshot/delta and delivery intent. I owns global authorization/Forget governance; G enforces tombstones in Context paths. Logical modules do not imply services/crates.

Conditions:
- Freeze boundary: G owns delivery intent/target semantics/state projection; H owns wire, transport, local apply and attestation capture.
- P0 Core must not be mistaken for trusted instructions; every tier remains data-only.
- H/C must provide stable identity binding before task/session/environment inheritance can be implemented.

### 2. Context domain model — Pass with conditions

MemoryContext, ContextEntry, ContextChangeSet, ContextVersion and ContextDelivery semantics are defined. Entry lifecycle is independent. Entries pin exact Memory ID/version; current permission/lifecycle is rechecked. P0–P3 are inclusion priorities, not instruction privilege.

Conditions:
- A scalar applied_version is insufficient for multiple adapters/sessions; retain per-delivery ledger.
- Preserve stable entry_id with immutable per-Context-Version entry revision.
- Align canonical projection/rendering refs and evidence access with D/I.

### 3. Versioning, concurrency and consistency — Pass with conditions

One monotonic sequence per Context, immutable snapshots, exact Base/Target, CAS/serialized writer, payload-hash idempotency, all-or-nothing Change Set. Snapshot is recovery authority; Delta requires exact base/hash and atomic apply. Rollback is a compensating version.

Conditions:
- Specify physical transaction for head + idempotency + outbox in Rust storage.
- Define canonical serialization/hash and schema migration with H.
- Bound idempotency retention without breaking retries/late ack.
- Cross-Context Forget is a resumable saga, not a global atomic transaction.

### 4. Scope, Forget and security — Pass on design; operationally TO_VALIDATE

Scope includes Agent instance, Task and Environment where applicable. Reauthorize at planning, edit, read, delivery and reconciliation. Forget tombstones immediately block entries/pending deliveries; offline adapters cannot reuse stale cache before reconnect reconciliation. Memory remains data, not instruction/tool authority.

Conditions:
- D/I define canonical Forget states, target inventory, dependency watermarks and retention; G cannot declare global completion.
- H defines clear/quarantine attestation and reconnect gate.
- Environment ID and permission epoch must be authoritatively bound, not accepted from display fields.
- Audit must avoid plaintext and unsafe content-reconstructable digests.
- Prompt injection remains a residual model-behavior risk; labels are not a guarantee the model ignores malicious memory.

### 5. Context budget and performance — Pass on model; thresholds TO_VALIDATE

Budget includes tokens, bytes, count, latency, fan-out, refresh and compaction cost. Sufficiency covers semantic/entity/relation/environment/temporal/evidence/risk/uncertainty/freshness. Hard constraints precede ranking; P0 is not silently dropped. Compaction preserves provenance and uncertainty.

Conditions:
- Define task requirement profiles with F/C.
- Benchmark target tokenizers and Adapter rendering; estimated tokens are not exact.
- Establish compaction fidelity tests and omission/regression metrics.
- Bound relation/provenance expansion and expose incomplete coverage.

### 6. Protocol compatibility and observability — Conditional Pass

Delivery identity, Context/session/request correlation and capability epoch are part of proof. Timeout/late ack use query/reconciliation, not optimistic inference. Errors are typed and avoid cross-Scope disclosure.

Open:
- H: Snapshot/Delta wire schema, negotiation, errors, atomic apply.
- C/H: Tier-1 final-request boundary capture, digest canonicalization and Applied Coverage.
- E/F: event/index watermarks, completeness/truncation and freshness.
- I: permission/Forget epoch, audit, retention and external deletion boundary.
- Cross-system trace: telemetry → canonical revision → retrieval → Change Set/version → Delivery → final inference attestation.

## 3. Mandatory integration issue disposition

| Issue | G treatment | Status after G | Owner/next step |
|---|---|---|---|
| INT-P0-02 Scope Isolation | Exact scope tuple; environment mandatory when relevant; reauthorize every boundary; scoped snapshots/deltas/caches | **CANDIDATE / OPEN** generic schema and end-to-end tests | B/I/H; G enforces |
| INT-P0-03 Forget | Immediate tombstones, pending delivery cancellation, snapshot invalidation, Adapter clear, offline reconnect gate; pending/confirmed/failed/unknown | **DECIDED** G blocking behavior; **OPEN** global completion/physical erasure | I completion; D/E targets; H clear attestation |
| INT-P0-04 Prompt Injection | Structured data, provenance/trust/epistemic labels; no protected-region writes or tool authorization | **DECIDED** boundary; residual model risk **TO_VALIDATE** | I threat model; H conformance; Agent policy |
| INT-P1-01 Version/Change Set | Immutable versions, base/target, CAS, idempotency, atomic commit, snapshot/delta, replay | **CANDIDATE** schema/implementation pending integration | G semantics; H wire |
| INT-P1-05 Applied Proof | Delivery/session/request/capability epoch, complete managed region in actual final request | **DECIDED** necessary condition; proof encoding **OPEN** | C/H conformance |
| INT-P1-06 Forget/Reconcile | Canonical revision/retraction, entity/relation change, permission, index lag/incomplete retrieval | **DECIDED** workflow; source schemas/watermarks **OPEN** | D/E/F/I |
| INT-P1-02 Claim Revision/Conflict | Context pins exact Memory version; preserve conflict/epistemic metadata | **OPEN** canonical identity and Conflict Set | B/D/F |
| INT-P1-03 Telemetry | Structured task/intent/observation/outcome/uncertainty/risk; no CoT | **DECIDED** input boundary; shared profiles open | C/H/E |

## 4. Reviewer conclusions

**Architecture reviewer — Conditional Pass.** Authority boundaries and three-layer model are sound. Avoid overlap with H/I and keep G semantic, not wire-level.

**Engineering reviewer — Conditional Pass.** Immutable snapshots, atomic Change Sets and CAS are implementable. Before Rust work, specify head/idempotency/outbox transaction, hash canonicalization, replay compatibility and per-Context concurrency. Multi-Context Forget is a saga.

**Security/reliability reviewer — Conditional Pass.** Tombstone-first and reauthorization are correct. Offline Adapter cache, environment identity, external deletion and final request proof remain risks. Documents do not prove implementation security.

## 5. Decision register

- **DECIDED:** Brain owns desired Context; Adapter applies; Agent reasons/acts.
- **DECIDED:** Remove != Forget; Delivered != Applied; Applied != comprehension/use.
- **DECIDED:** no CoT requirement; memory is data, not instruction/tool authority.
- **DECIDED:** separate Context, Entry and Delivery lifecycles.
- **CANDIDATE:** per-Context serialized writer with CAS; immutable snapshot per committed sequence; atomic Change Set.
- **CANDIDATE:** stable entry_id with immutable per-version revision; P0–P3 capacity profile.
- **TO_VALIDATE:** performance, coverage thresholds, compaction fidelity, tombstone propagation and offline convergence.
- **OPEN:** generic Scope/permission epoch (B/I); global Forget completion/external copies (I); canonical event/index watermark (D/E/F); BMCP wire/clear ack (H); final inference proof (C/H).

## 6. Exit gates

Before H freezes wire: Snapshot/Delta schema, atomic apply, delivery idempotency/query, final-request proof and clear/reconnect semantics.

Before I freezes governance: Forget target inventory, access-block point, cleanup states, external boundary, permission epoch/revocation order, audit retention and data classification.

Before Rust implementation: test CAS races; same-key same/different payload; commit/outbox crash; duplicate Delta; base mismatch; partial Adapter apply; late Applied ack; revocation during delivery; Forget while offline; incomplete retrieval.

**Conclusion:** Session G is ready for cross-module integration review as a candidate architecture, not a frozen implementation or wire specification.


---

# Phase 3.5 cross-module re-review addendum

- Review date: 2026-11-16
- Review baseline: G branch plus the owner branches listed below as observed during this re-review.
- Review type: static cross-branch contract reconciliation; no runtime, storage, security or performance test was executed.
- Disposition: **Conditional Pass for continued integration; NOT READY for contract freeze or implementation sign-off.**
- This addendum supersedes earlier OPEN descriptions only where it records an explicit G-owned semantic clarification. It does not approve another owner's candidate contract or close implementation gates.

## 7. Branch and evidence baseline

| Owner | Branch | HEAD observed |
|---|---|---|
| A / shared baseline | main | 8a6414158c9c056c1638222534e1993d1bbc99d2 |
| B | session-b-domain-model-phase3 | 66adf6bdcf5ec69a146fe75afe20ce3b85af8448 |
| C | session-c-agent-integration-2026-11-16 | a585307222b0169c007915c25ff8ed0da517f3e4 |
| D | session-d-memory-brain-2026-11-16 | da8e5882d0b238d765d00b2225b79eea45a483b1 |
| E | session-e-memory-compiler-2026-11-16 | c2f14408ba62447c11172d65b93a279fef96d175 |
| F | session-f-memory-runtime | badc8b9998236c0075ab32c4ae8dc58c8c51984a |
| G | session-g-memory-context | 3d2c065be863bc1d349faaeece6f6eaa0047abae |
| H | session-h-bmcp-protocol | 1ee65928f123d92a4758b0de09bc8d6df1e46253 |
| I | session-i-security-governance-2026-11-16 | 5591ad3620ec3f5d74194bd79556dcf3e25bea07 |
| Storage/Consistency | session-storage-consistency-forget-atomicity-2026-11-16 | 3a14550648f21c0bc2725dac38b29e099c2f3196 |

The G branch contained all six required design documents before this addendum. This re-review updates only the six G-owned files and this G review file. No A/B/C/D/E/F/H/I/Storage or governance file is changed.

## 8. Cross-module decisions consumed

### 8.1 D — canonical Forget and producer publication gate

G consumes D's semantic operations: RegisterProducerClass, RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier.

G is a registered derivative producer for Context membership/materializations, ChangeSets, Snapshots, Deltas and Delivery Intents. Producer work must be durably registered before enqueue, lease, protected source dereference or execution. Complete dependency lineage is registered before visibility. The latest D fence and current I authorization must be validated at the same linearizable visibility decision. A local check-then-publish is forbidden.

**Critical OPEN gate:** D explicitly states that these are semantic operations, not proof of callable APIs or a physical transaction. Storage/Consistency has not yet supplied conformance evidence for the cross-owner visibility boundary. Until a shared transaction or proven recoverable prepare/commit protocol exists, G must keep staged derivative artifacts private, must not advance a visible Context head and must not create a sendable delivery.

### 8.2 E — compiler lineage and durable producer work

G accepts only canonical committed Memory IDs/versions, never Accepted telemetry, compiler candidates or uncommitted outputs. E's stable work/run/attempt identities, private staging, dependency registration and final publication-gate semantics are relevant to G's own producer boundary. E must refresh any stale D baseline references in its own files; G does not edit E-owned material.

### 8.3 F — candidate completeness and per-partition freshness

F RetrievalResult/ActivationRecommendation remains an immutable candidate proposal. G independently checks exact canonical MemoryVersion, lifecycle, Scope, I PermissionEpoch and D ForgetFence before inclusion. G consumes per-index/per-partition IndexWatermark and completeness/truncation/uncertainty. A maximum or scalar watermark cannot conceal a lagging partition. F's cache/index suppression and rebuild proof is F-owned; G cannot infer it from Context state.

### 8.4 H/C — delivery, final request and Adapter evidence

H separates DELIVERED transport receipt, MANAGED_REGION_MATERIALIZED local postcondition, FINAL_REQUEST_SUBMITTED evidence and later EXECUTION_STARTED. G Delivery Applied is accepted only when C's Full Applied predicates and H's evidence bind the exact ContextVersion, DeliveryId/attempt, authenticated Adapter/Agent/runtime/session, Scope/Environment, CapabilityEpoch, current I PermissionEpoch, applicable D ForgetFence, complete Managed Region inventory, InferenceRequestId and FinalRequestBoundaryId.

H's Adapter Forget ACKs are action-specific: SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED. They are not Applied ACKs and do not establish I global completion. Tier 2/3 or a path without final immutable request visibility cannot claim Full Applied.

### 8.5 I — identity, target inventory and global completion

I owns Principal/Issuer trust, authorization, PermissionEpoch, ProducerDomainInventoryEpoch, TargetInventorySeal, TargetId, per-target state, PolicyException and Global Forget Completion. G supplies only its own Context/snapshot/delta/ChangeSet/delivery target evidence, bound to I-issued target/seal, exact ScopeRef, D fence, I epoch, G producer identity, artifact/delivery refs, action/postcondition, attempt and integrity evidence. G cannot mint target IDs, mark global state, approve exceptions or claim physical erasure.

D ProducerRegistrationHighWater, I ProducerDomainInventoryEpoch, F IndexWatermark and G ContextVersion are distinct; no one is a substitute for another.

## 9. INT-* disposition after G rework

| Issue | G disposition | Current status | Remaining owner/gate |
|---|---|---|---|
| INT-P0-02 Scope Isolation | Exact resolved identity tuple; EnvironmentRef mandatory when applicable; reauthorize at plan/edit/reconcile/publication/delivery; scope-bound snapshots and entries | **PARTIAL** | B typed refs and I/H authenticated binding/permission semantics; cross-scope conformance tests |
| INT-P0-03 Forget | Tombstone-first Context suppression; invalidate staged and historical delivery paths; G producer registration/dependency/publication gate; per-G-target evidence; offline reconnect block | **PARTIAL** | D/E/Storage atomic gate; I sealed inventory/global completion; F cache/index evidence; H action-specific ACK and reconnect conformance |
| INT-P0-04 Prompt Injection | Structured data-only managed region; preserve source/trust/epistemic/provenance; no tool or policy authority; protected regions immutable | **DECIDED as G boundary** | Residual model-behavior risk remains TO_VALIDATE with I/C/H adversarial tests; no guarantee that model ignores malicious natural language |
| INT-P1-01 Context Version / ChangeSet | Immutable target snapshots, explicit Base/Target, per-Context CAS/serialization, idempotency, atomic ChangeSet, Snapshot/Delta and replay | **CANDIDATE / semantics specified** | Storage realization, H wire schema, cross-owner visibility linearization and conformance |
| INT-P1-05 Applied Proof | Full requires complete managed region in exact final immutable request with exact Context/Delivery/session/capability/permission/fence/request binding | **DECIDED necessary predicate; encoding OPEN** | C/H proof capture, canonical digest profile and Adapter conformance |
| INT-P1-06 Forget / Reconciliation | Reconcile canonical revision/retraction/supersession, Entity/Relation changes, permission, fence, index gaps and incomplete retrieval; tombstone first | **CANDIDATE workflow / safety order DECIDED** | D/E event schemas, F completeness/watermark vectors, I currentness and H ACK evidence |
| INT-P1-02 Claim Revision / Conflict Set | Pin exact MemoryVersion and preserve epistemic/conflict metadata; G does not define canonical Claim identity | **OPEN / ADR-dependent** | B ADR and D/F canonical consumer contracts |
| INT-P1-03 Telemetry | Structured task/intent/observation/outcome/uncertainty/risk only; no full CoT requirement; telemetry is not Canonical Memory | **DECIDED input boundary** | C/H schema/profile and E canonical commit signal |
| INT-P1-04 Accepted durability | G rejects Accepted/Compiled as proof of Canonical Memory existence; only D committed refs are eligible | **NOT G-owned** | E/H/Storage acceptance and commit evidence |

## 10. Updated six-dimension review

### 10.1 Architecture and responsibility boundaries — Pass with conditions

G owns desired Context membership/order/eligibility/budget/version and reconciliation. D owns canonical Memory and Forget fence. F owns retrieval, index/cache and activation proposals. H owns BMCP wire and Adapter execution/evidence. I owns identity, authorization and global target/completion policy. C owns final-request proof predicates. Storage/Consistency owns physical atomicity realization. No authority is transferred by an interface.

The new producer-gate requirement is essential: G's Context artifacts are derivative materializations and cannot be published outside D's Forget fence. This does not make D the Context version owner.

### 10.2 Context domain model — Pass with conditions

The six G documents define MemoryContext, ContextEntry, ContextChangeSet, ContextVersion and ContextDelivery, with exact MemoryVersion pinning, per-version Entry revisions, P0–P3 priority tiers and separate lifecycle state machines. Phase 3.5 adds typed producer work, lineage receipts, I target evidence and H/C final request references.

Remaining: B ActorRef/ScopeRef and EnvironmentRef approval, I security binding, canonical projection/rendering contracts and stable schema evolution.

### 10.3 Versioning, concurrency and consistency — Conditional Pass

The semantic model is coherent: one monotonic sequence per Context; immutable snapshots; explicit Base/Target; CAS or serialized writer; idempotency by scoped key + canonical payload digest; all-or-nothing ChangeSet; Snapshot as full replacement; Delta as exact-base atomic transition; rollback by compensating version; replay never bypasses current authorization/fence.

**Blocking implementation gate:** G head visibility and D final publication gate must share one linearizable visibility decision. The D operation contract does not itself prove a callable transaction; Storage/Consistency realization remains OPEN. Until proven, G staged outputs remain private and delivery is disabled for them.

### 10.4 Scope, Forget and security — Partial / not globally closed

Tombstone-first invalidation and current I/D checks are specified for active entries, staged ChangeSets, snapshots, deltas, G caches, delivery intents and Adapter apply/reconnect. Offline state remains Unknown/Pending. G emits per-target evidence only for G-owned surfaces.

Global closure is not claimed: I owns inventory seal, target states, exceptions and completion; D owns canonical barrier; F/H/E each supply their own evidence. Physical erasure of backups/provider copies and already processed model tokens is outside G.

### 10.5 Context budget and performance — Pass on model; thresholds TO_VALIDATE

Vector budgets and task-specific sufficiency include semantic/entity/relation/environment/temporal/evidence/risk/uncertainty/freshness, redundancy and compaction cost. F's partition completeness is retained as a vector. Hard authorization/fence/canonical/evidence constraints precede ranking. No fixed latency or quality target is claimed without representative workload tests.

### 10.6 Protocol compatibility and observability — Conditional Pass

G's delivery semantics align with H's evidence stages and capability epoch. Applied proof is not inferred from transport receipt. Correlation chain retains Context/Version/ChangeSet/Delivery/Attempt, producer work, D fence/cursors, I epoch/target/seal, F partition watermarks and H request/boundary evidence.

Still OPEN: H wire schema/compatibility, B typed-reference approval, C/H digest profile and final-boundary conformance, I epoch currentness/target evidence acceptance, and redaction/retention rules.

## 11. DECIDED / CANDIDATE / TO_VALIDATE / OPEN

### DECIDED (G-owned semantics or inherited invariant)
1. Brain owns desired Context; G owns one ContextVersion sequence per Context.
2. Adapter applies only at a future inference boundary; Agent retains reasoning/action/security authority.
3. Context, Entry and Delivery lifecycles are independent.
4. Remove is not Forget; Applied is not comprehension/use.
5. Context references exact canonical MemoryVersion and preserves provenance/epistemic/temporal metadata.
6. Forget/revocation tombstone blocks current use before asynchronous cleanup.
7. G consumes I TargetId/seal and never declares global completion.
8. No Context-derived artifact is visible/sendable without D dependency registration and final fence/permission gate.
9. No Full Applied without exact final immutable request evidence and complete managed-region coverage.

### CANDIDATE
1. Per-Context serialized writer plus CAS guard.
2. Immutable full snapshot per committed sequence; Delta for exact contiguous transition.
3. ChangeSet all-or-nothing; no-op does not advance version.
4. Event-driven invalidation plus periodic typed-watermark sweep.
5. I target evidence profile for G-owned Context/delivery surfaces, pending I acceptance.

### TO_VALIDATE
1. Storage/Consistency proof of the cross-owner G-head/D-publication linearization.
2. D producer registration and dependency receipt integration under crash/retry/race.
3. Tombstone fan-out latency, reconnect convergence and cache invalidation completeness.
4. Digest canonicalization, privacy and final-request evidence conformance.
5. Sufficiency weights, tokenizer variance, compaction fidelity and p95/p99 under declared workload.
6. Property/fault tests for CAS races, duplicate Delta, late ACK, Forget/revocation during delivery and offline Adapter.

### OPEN
1. B ActorRef/ScopeRef/EnvironmentRef final semantics and approval.
2. I PermissionEpoch currentness/fan-out API, inventory seal and target-evidence acceptance.
3. D/E callable producer/fence/dependency/publication APIs and E refresh to current D baseline.
4. F completeness and per-partition IndexWatermark schema.
5. H final wire schema, ACK/clear evidence, reconnect and capability negotiation.
6. C/H final immutable request proof profile/digest canonicalization.
7. Cross-store transaction/prepare-commit recovery and crash consistency.

## 12. Required conformance tests — NOT RUN

1. Producer registration races with D fence installation: exactly one ordering wins; no admitted-but-unaccounted G work.
2. Forget races with G Context head publication: if fence wins, artifact remains private/rejected; if publication wins, it is registered and included in the barrier.
3. Missing dependency receipt, stale PermissionEpoch or unknown fence prevents Context head advance and delivery.
4. Same ChangeSet key/same digest returns original TargetVersion; same key/different digest conflicts.
5. Concurrent same-Base edits cannot both advance the head.
6. Duplicate Delta, wrong Base, bad hash, unknown operation and partial Adapter application never produce a mixed target state.
7. A Forget fence invalidates old snapshots/deltas and cancels/supersedes pending deliveries; late ACK cannot restore content.
8. One F partition lagging produces Partial/Unknown sufficiency; scalar max watermark cannot hide it.
9. Reconnect after PermissionEpoch/fence advancement suppresses old local region before any cached Context reuse.
10. Applied Full is rejected if any identity, scope, epoch, managed-region inventory, request ID, boundary ID or final evidence is missing/stale.
11. H Forget ACK maps only to its exact Adapter target/action; it cannot satisfy a G/F/D/I target by implication.
12. Late derivative or changed I inventory seal reopens the relevant reconciliation evidence.

These are acceptance specifications only. No Rust code, database transaction, Adapter, inference runtime, concurrency, fault injection, penetration test, physical erasure or performance benchmark was executed.

## 13. Final review decision

**Session G: Conditional Pass for continued cross-module integration. Not approved for contract freeze, production implementation or global Forget completion.**

The six G documents now describe the required Context authority, edit/version/reconciliation/budget semantics and the Phase 3.5 D/E/F/H/I boundaries. The most important unresolved blocker is the physical/recoverable linearization connecting G's visible Context head with D's final ForgetFence publication gate. Until Storage/Consistency and D provide an implementable, tested boundary, G must keep derived Context artifacts private and must not claim a committed/deliverable target for that path.

No branch merge, main integration, wire freeze, implementation conformance, security certification or performance sign-off is implied.
