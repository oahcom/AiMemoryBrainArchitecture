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
