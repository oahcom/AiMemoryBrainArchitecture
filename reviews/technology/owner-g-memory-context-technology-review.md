# G — Memory Context Technology Architecture Review

- Document: TAR-AI-001 / TAB-001 v0.1
- Owner: G — Memory Context Architect
- Branch: `session-g-memory-context`
- Reviewed branch HEAD: **PENDING exact parent-SHA verification during report publication**. Branch-local artifacts were read; the file reader exposed blob SHAs but not the resolved branch commit.
- Review date: 2026-11-17
- Report version: 1.0
- Verdict: **CONDITIONAL PASS**
- Review mode: static architecture and contract review; no implementation or runtime tests executed.

## 1. Executive Summary

G's authority model is sound and consistent with TAB-001: G alone owns Context membership/order/budget, ContextVersion, ChangeSet, reconciliation and Delivery intent. F supplies retrieval proposals; D supplies immutable canonical Memory refs and Forget state; H transports G-owned delivery; C/Agent supplies final inference boundary evidence; I owns authorization and global Forget policy. Context Remove is not Canonical Forget, and Delivered is not Applied.

The branch documents read show meaningful engineering semantics: ChangeSet operations are staged and all-or-nothing; Add pins exact MemoryVersion; Update uses expected entry revision; Remove creates a membership tombstone; Replace validates both sides; Reconcile consumes authoritative D/I state and F completeness; budget is a vector across tokens/bytes/count/fanout/latency; sufficiency is task-specific and cannot be inferred from Top-K. These are appropriate foundations.

Conditional acceptance is limited by three material gaps: the exact durable transaction/storage realization for ContextVersion + ChangeSet + Delivery state is not evidenced; the D/E/Storage producer/dependency/publication gate is still OPEN; and Full Applied requires a jointly verified C/H final-request proof profile bound to the exact G target and current I/D epochs. Tokenizer/context-window budgets and failure recovery remain unmeasured.

## 2. Review Scope and Evidence

| Source | Ref / Blob SHA | Use |
|---|---|---|
| TAB-001 | main; blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | Context architecture, persistence, transport and resource candidates |
| TAR-AI-001 | main; blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` | G-specific review requirements |
| Phase 2 reconciliation | main; blob `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7` | G branch-aware baseline and cross-module findings |
| Phase 3 D/E/H/I review | main; blob `edaccb802e0425f2d47bd4b613fab4dfde107144` | Forget/identity/typed cursor dependencies |
| G Context Edit Operations | G branch; blob `10c94e85dfe89d20dcdb202cafc2bef767f076fc` | Add/Update/Remove/Replace/Reconcile and atomicity |
| G Context Budget and Sufficiency | G branch; blob `a2f96a88f3123862ea263da11366dda4207d5b0a` | Budget vector, sufficiency and F candidate requirements |
| H BMCP Message Envelope and Versioning | H branch; blob `5547ecd78d118bd63e571e5daad87194d9b694e4` | ContextVersion/Delivery/epoch envelope mapping |
| H Context Delivery and Acknowledgement | H branch; blob `bf9732cc39d156853b507c3a3a4e573159978f49` | Delivery state machine and Full Applied conditions |
| C Final Inference Boundary | C branch; blob `f3b254fcfd9a652a0ec68921e801f78d93bb5163` | Applied binding tuple and final-request proof boundary |

Phase 2 records six G design documents and design commit `3d2c065be863bc1d349faaeece6f6eaa0047abae`; it is a historical baseline, not verified as current branch HEAD. Other G design paths were not all independently resolved in this retrieval; findings are bounded to the two fetched G artifacts plus cross-module reports.

## 3. Six-Dimension Review Matrix

| Dimension | Verdict | Finding |
|---|---|---|
| R1 Requirements & workload fit | CONDITIONAL | Context lifecycle, edits, budget and sufficiency are described; concurrent session workload, refresh rate, tokenization variance and delivery SLOs remain unquantified. |
| R2 Dependencies & boundaries | CONDITIONAL | G/F/H/C/D/I authority boundaries are coherent; D's derivative registration gate and I policy bindings remain open. |
| R3 Candidate technology selection | OPEN / TO_VALIDATE | SQLite tables/outbox are reasonable candidates; no persistence, queue, rendering or token-count benchmark has been run. |
| R4 Resource constraints | OPEN / TO_VALIDATE | Budget vector is sound, but numerical budgets, tokenizer/model profiles, peak memory and concurrency are not measured. |
| R5 Failure recovery & safety | CONDITIONAL | Atomic staged ChangeSet and stale replay rules are specified; transaction commit, delivery recovery and Forget races need implementation tests. |
| R6 Interface compatibility | CONDITIONAL | ContextVersion, Delivery, PermissionEpoch, ForgetFenceGeneration and capability epoch remain distinct; exact Applied evidence and wire schema are candidate. |

## 4. Component Dependency Analysis

- **F → G:** RetrievalResult/ActivationRecommendation are proposals with exact MemoryRef/MemoryVersionRef, ScopeRefs, evidence/provenance, temporal/epistemic metadata, completeness and per-index/per-partition IndexWatermark vector. G independently validates canonical eligibility and I/D authorization/fence. F does not create ContextEntry or ContextVersion.
- **D → G:** D supplies canonical identity/version/lifecycle, ForgetOperation/fence and producer/dependency/publication evidence. G must register Context-derived artifacts and prevent stale snapshots/deltas/deliveries from reintroducing forgotten lineage.
- **G internal authority:** one Context head and immutable ContextVersion sequence per Context; ChangeSet is an operation batch with BaseVersion/target and idempotency identity. Delivery attempts are a separate state machine and do not advance ContextVersion by themselves.
- **H → G:** H transports snapshots/deltas and ACKs; it cannot mint ContextVersion, reinterpret its ordering, or decide membership.
- **C/Agent → G:** C defines the final inference request boundary and request identifiers. G accepts Applied only when the evidence binds exact ContextVersion, Delivery, Agent/session, Adapter/capability epoch, inference request, PermissionEpoch and ForgetFenceGeneration.
- **I → G:** current Principal/Scope authorization and revocation/Forget governance. A valid old ChangeSet does not grant continued permission to deliver/apply it.
- **Storage → G:** durable transaction for ChangeSet, immutable ContextVersion, audit and outbox; delivery intent/attempt/ACK durability and recovery must be explicitly mapped. No storage authority is implied by the logical design.

## 5. Candidate Technology Comparison

| Option | Strengths | Risks / limits | Disposition |
|---|---|---|---|
| SQLite WAL tables + transaction/outbox | Local-first, transactional Context head CAS, low operational footprint | Single writer; crash/locking semantics and D dependency gate require proof | RECOMMEND first local prototype |
| PostgreSQL | Concurrent writers, mature transaction isolation and operational tooling | Additional service/ops; unnecessary until workload or multi-host needs justify | CANDIDATE scale-out alternative |
| In-memory Context state | Fast planning and render | Lost on crash, cannot be authoritative for version/delivery or idempotency | REJECT as durable authority; allow disposable cache only |
| Database-backed delivery outbox | Recovery, retry and explicit Pending/Unknown states | Requires lease, expiry, dedupe and supersession protocol | RECOMMEND candidate pattern |
| External broker | Throughput and decoupling | More failure modes and no need established for local-first initial deployment | DEFER pending measured queue pressure |
| JSON vs CBOR/MessagePack | JSON is inspectable; binary encodings reduce payload overhead | H owns wire; G must not freeze encoding or field names | NEEDS H decision after schema conformance |

G should start with durable Context metadata/state in the same transactional authority as its head/outbox where feasible. Large rendered projections can be content-addressed or recomputable only if provenance, retention and deterministic reconstruction rules are explicit.

## 6. Resource Budget Analysis

Budget is a vector, not a token-only scalar:

- tokens under target model/tokenizer profile;
- serialized bytes and transport max size;
- number of Context entries and distinct canonical refs;
- relation fan-out and provenance depth;
- planning, reconciliation and delivery latency;
- refresh frequency, CPU and memory;
- compaction cost and expansion cost;
- per-tier reserved capacity and protected-entry constraints.

Sizing equations:
- total managed token budget = min(model context window − reserved system/developer/user/tool/output/safety headroom, Agent-configured managed-region cap);
- serialized payload bytes = sum(rendered entry bytes + metadata/provenance refs + envelope overhead);
- Context memory = active Contexts × (entry metadata + cached rendering + snapshot/delta working buffers);
- delivery queue memory/disk = pending deliveries × mean payload/metadata size × retry retention factor.

Do not use one tokenizer estimate for all models. Unknown tokenizer requires conservative byte/count estimates and explicit token-estimate uncertainty. Measure worst-case Unicode, code, JSON, tool outputs, multimodal placeholders and model/provider changes. 12–16 GB GPU VRAM is not a Context storage budget; local inference and embedding concurrency are separately scheduled.

## 7. Failure & Recovery Matrix

| Failure | Durable authority / recovery | Required behavior | Proposed test |
|---|---|---|---|
| Crash during ChangeSet staging | G durable transaction + current Context head | No partial Context head; replay idempotently | G-REC-01 |
| Concurrent ChangeSets same BaseVersion | G head CAS/serialization | Exactly one commits; loser reloads/replans | G-CAS-01 |
| Duplicate operation key, same payload | G idempotency record | Return original immutable target result | G-IDEM-01 |
| Duplicate key, changed payload | G idempotency record/hash | Reject conflict; no side effect | G-IDEM-02 |
| Delivery sent, ACK lost | G delivery ledger + H reconciliation | Unknown until exact receipt/attestation recovered | G-ACK-01 |
| Adapter offline | G Pending/Unknown + H reconnect | Do not mark Applied; reconcile current target before replay | G-OFF-01 |
| Late ACK after supersession | G immutable delivery history/current head | Historical evidence only; never roll back head | G-ACK-02 |
| Forget during ChangeSet/delivery | D fence + I policy + G dependency gate | Invalidate affected staged/published artifacts and block stale apply | G-FRG-01 |
| Tokenizer/context window changes | target model profile + G budget policy | Re-render/rebudget; mark partial/insufficient rather than silently truncate | G-BUD-01 |
| F partition gap / stale index | F watermark vector + D canonical refs | Sufficiency Partial/Unknown; do not infer absence | G-FRESH-01 |

## 8. Interface Compatibility Findings

- ContextVersion is G-owned and distinct from D CanonicalCommitCursor, F IndexWatermark, H Delivery ID/attempt, I PermissionEpoch, D ForgetFenceGeneration and Adapter CapabilityEpoch.
- ChangeSet must bind Context ID, BaseVersion, ordered operations, normalized payload digest, authenticated actor, policy decision/epoch, and idempotency key. Commit must atomically publish exactly one immutable target ContextVersion or none.
- Add pins exact MemoryVersion; Update uses expected entry revision; Remove creates a G membership tombstone only; Replace validates old and new references; compaction preserves source refs/uncertainty and is a registered derivative.
- Delivery status is not ContextVersion status. Prepared/Delivered/Applied/Rejected/Expired/Superseded/Unknown must remain separate and attempt-scoped.
- H's Full Applied predicate is compatible in principle: exact target ContextVersion + complete managed region in final immutable request + request ID/submission evidence + integrity + current permission/fence/capability binding. C owns proof boundary semantics; H owns protocol evidence; G consumes it.
- A G Applied record must not be inferred from transport receipt, local Adapter buffer, token budget sufficiency or model response.
- Remove is not Forget. D/I Forget independently tombstones affected Context entries and invalidates snapshots/deltas/pending delivery; reconnect must reconcile current D/I/G state before replay.
- D/E/Storage atomic producer admission/dependency/publication API is not defined by prose and remains OPEN; G's staged artifact must remain private until that exact gate is available.
- B Fact/Claim and typed Scope/Actor references remain OPEN/ADR-BLOCKED; no dependent schema freeze.

## 9. Blocking Findings

| ID | Severity | Finding | Required closure |
|---|---|---|---|
| G-TAR-P1-001 | P1 | Durable ContextVersion/ChangeSet/Delivery transaction and recovery boundary not demonstrated | G/Storage prototype with crash/CAS/idempotency/restore tests |
| G-TAR-P1-002 | P1 | D/E producer/dependency/publication gate is still OPEN | D/E/Storage exact operation and failure contract; G artifact visibility test |
| G-TAR-P1-003 | P1 | Full Applied consumer proof requires exact C/H/G/I binding and verifier | Joint schema/profile and negative tests for missing/stale tuple fields |
| G-TAR-P1-004 | P1 | Forget invalidation across snapshot/delta/delivery/offline replay not executed | End-to-end fence race and reconnect anti-resurrection tests |
| G-TAR-P2-001 | P2 | Tokenizer/model profile and budget thresholds unmeasured | Multi-tokenizer/window benchmark and overflow fixtures |
| G-TAR-P2-002 | P2 | Compaction fidelity and deterministic reconstruction remain TO_VALIDATE | Source-preserving compaction tests with conflict/uncertainty cases |

## 10. Required ADRs

1. ADR-G-001: durable Context store, CAS/transaction boundary, outbox and delivery ledger.
2. ADR-G-002: Context snapshot/delta serialization and canonical rendering profile, jointly with H.
3. ADR-G-003: Applied attestation acceptance profile and verifier contract, jointly with C/H/I.
4. ADR-G-004: budget policy, tokenizer profile, truncation and compaction thresholds.

## 11. Required Prototypes and Tests

- SQLite WAL prototype for Context head CAS + ChangeSet + immutable version + audit/outbox atomic commit.
- Concurrent writer, crash before/after commit, duplicate idempotency, changed payload conflict and restore tests.
- Delivery state-machine harness: lost ACK, duplicate ACK, late ACK, expiry, supersession, offline reconnect and capability downgrade.
- Forget during staging, dependency registration, snapshot/delta send, final submit and reconnect; prove no stale resurrection.
- Applied verifier tests for each missing/mismatched field: ContextVersion, Delivery, inference_request_id, Adapter identity/instance, CapabilityEpoch, PermissionEpoch, ForgetFenceGeneration, protected-region integrity and submission evidence.
- Tokenizer/window matrix, byte/entry/fanout budgets, Unicode/code/tool-output and truncation tests.
- Compaction fidelity with provenance expansion, conflict preservation and unknown coverage.

## 12. Verdict

**CONDITIONAL PASS** for G's Context architecture direction. G may prototype a transactional Context head/ChangeSet/outbox model and vector budget enforcement. Do not freeze storage, wire schema, Applied proof profile, or Forget completion semantics until the P1 findings close.

## 13. Evidence and Exact SHAs

- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- TAR-AI-001 blob: `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- Phase 2 reconciliation blob: `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7`
- Phase 3 D/E/H/I review blob: `edaccb802e0425f2d47bd4b613fab4dfde107144`
- G Context Edit Operations blob: `10c94e85dfe89d20dcdb202cafc2bef767f076fc`
- G Context Budget and Sufficiency blob: `a2f96a88f3123862ea263da11366dda4207d5b0a`
- H Envelope blob: `5547ecd78d118bd63e571e5daad87194d9b694e4`
- H Delivery/Acknowledgement blob: `bf9732cc39d156853b507c3a3a4e573159978f49`
- C Final Inference Boundary blob: `f3b254fcfd9a652a0ec68921e801f78d93bb5163`
- G design baseline commit recorded by Phase 2: `3d2c065be863bc1d349faaeece6f6eaa0047abae` (not asserted to be current HEAD)
- Branch current HEAD: pending exact commit-parent verification; no fabricated SHA.
- No runtime, fault-injection, security, or performance tests executed in this review.
