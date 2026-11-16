# Phase 3 — Cross-Module Contract Registry

- Role: Session A / Principal Integration Architect
- Status: **CANDIDATE coordination register; not an ADR and not an approval to freeze schemas/wire contracts**
- Repository baseline: `main @ 8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
- D/E/F/G reviewed at the exact Phase 3 task-pack refs recorded below.
- H/I: no formal design package was present in the inspected main tree. Their authority is intentionally not inferred.

## 1. Authority and decision vocabulary

This register coordinates interfaces; it does not supersede subsystem ownership.

- **DECIDED** — explicitly established by an approved governance baseline or an owner-approved normative decision in its own authority. This label does not imply implementation conformance.
- **CANDIDATE** — proposed integration shape requiring owner review and/or ADR approval.
- **ADR-BLOCKED** — cannot be finalized before a named ADR/decision authority acts.
- **OPEN** — missing owner decision, definition, or evidence.
- **TO_VALIDATE** — sufficiently specified to test, but no reproducible test evidence has been accepted.

A cross-module recommendation in this document is never an approved ADR. Governance files are read-only in this workstream. No Fact/Claim, Forget, BMCP, Applied, identity, or Security contract is frozen here.

## 2. Source baseline and authority map

| Area | Exact reviewed ref | Authoritative owner boundary | Integration consequence |
|---|---|---|---|
| A/B/C | main @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | A: system boundaries; B: domain semantics; C: Agent telemetry/inference boundary | Current main documents only |
| D | `session-d-memory-brain-2026-11-16 @ 9dc08c63f6912320e290a963c634748ec44a81c8` | D: canonical Memory identity/version, LifecycleEvent, canonical Forget records/fence semantics | D does not own ContextVersion, wire protocol, global authorization or physical-erasure policy |
| E | `session-e-memory-compiler-2026-11-16 @ 54df136d1e410af834461950e3c61c5c80abd6ad` | E: durable Event ingress, compilation, provenance/derivative production and publication intent | E does not own canonical commit, Runtime indexes or Context versions |
| F | `session-f-memory-runtime @ dad5deb6bfaa2df9956930d0b1372df354112567` | F: retrieval, candidate generation, index freshness consumption, Working Set/cache and activation recommendation | F does not own canonical records or Context versions |
| G | `session-g-memory-context @ 3d2c065be863bc1d349faaeece6f6eaa0047abae` | G: Context membership/order/budget, ContextVersion, ChangeSet, reconciliation and delivery intent | G does not own canonical Memory or Adapter wire execution |
| H | Not present | Proposed owner: BMCP wire/Adapter SDK/delivery and final-request attestation | **OPEN**; no H artifact or approved authority contract assumed |
| I | Not present | Proposed owner: global identity/authorization, revocation, retention, Forget completion and security governance | **OPEN**; no I artifact or approved authority contract assumed |
| Storage / Consistency | No formal owner package identified in inspected paths | Durable transaction, partition/log mechanics, outbox, recovery and backup substrate | Engineering owner must be named before implementation sign-off |

### Branch bookkeeping

The repository branch listing contained main and the four exact D/E/F/G branches, but no A-named branch. A dedicated branch `session-a-integration-2026-11-16` was therefore created from the inspected main HEAD above. No module branch was changed or merged.

## 3. Decision register — Phase 1/2 INT issues

Accountable owner is singular per row; contributors are not co-owners of that accountability. Closure requires owner-approved decision plus cited artifact and evidence where applicable.

| ID | Accountable owner | State | Dependency | Closure evidence / exit criterion |
|---|---|---|---|---|
| INT-P0-01 Fact vs Claim normative identity | Architecture Governance | ADR-BLOCKED | B domain alternatives; D/E/F consumer impact | Approved ADR; synchronized governance/README/terminology/domain references; consumer mapping; no schema freeze before approval |
| INT-P0-02 Scope/Identity/Permission end-to-end | Session I (not yet staffed/package absent) | OPEN | B Scope semantics; C/H identity binding; D/E/F/G enforcement | Approved identity/permission authority contract; authenticated Principal/Actor binding; negative tests at every candidate/read/write/cache/delivery/replay boundary |
| INT-P0-03 Forget/retention completion and anti-resurrection | Session I (not yet staffed/package absent) | OPEN | D durable fence/operation; E producer barrier/derivative registration; F index/cache suppression; G delivery/context clear; H adapter clear; storage/backup policy | Approved completion policy and per-target proof; race matrix; unknown/offline/backup/external exceptions visible; no completion from tombstone alone |
| INT-P0-04 Memory prompt-injection residual risk | Session I (not yet staffed/package absent) | OPEN | B/E provenance and trust labels; C/H protected inference boundary; Agent tool authorization | Threat model and mitigations approved by security owner; adversarial tests; explicit residual-risk statement; no claim of complete prevention |
| INT-P1-01 ContextVersion / ChangeSet authority | Session G | CANDIDATE | H delivery/retry contract; C final request boundary; INT-P0-02/03 | G owner-approved version/CAS/idempotency contract; H/C proof mapping; duplicate/base-conflict/late-ack tests |
| INT-P1-02 Claim identity/revision, ConflictSet, Entity Merge/Split | Session B | ADR-BLOCKED | INT-P0-01; D persistence and E/F/G consumers | B/Governance-approved domain decision; D/E/F/G mapping; historical reference and migration tests |
| INT-P1-03 Telemetry identity/event/ordering | Session C | CANDIDATE | B typed refs/Scope; H envelope; I authenticated identity; E durable ingress | C owner-approved event taxonomy and identity binding; out-of-order/duplicate/correction tests; plan-vs-outcome negatives |
| INT-P1-04 Accepted durability/idempotency | Session E | CANDIDATE | H envelope; I identity/retention; Storage transaction/outbox | Durable receipt contract and crash evidence; same-key/same-digest replay; same-key/different-digest conflict; receipt retention decision |
| INT-P1-05 Applied final-request proof | Session G | CANDIDATE | C inference boundary; H Adapter attestation; INT-P0-02/03 | H/C/G approved proof semantics; exact request/session/version/delivery/capability correlation; final-boundary conformance evidence |
| INT-P1-06 Provenance/Lifecycle/reference semantics | Session B | OPEN | D LifecycleEvent authority; E provenance; I retention; typed cursor work | B domain reference/time/provenance semantics; D/E owner alignment; cycle/unknown-source/Forget traversal tests |

## 4. Decision register — INT-X work items

| ID | Accountable owner | State | Dependency | Closure evidence / exit criterion |
|---|---|---|---|---|
| INT-X-01 Typed cursor/watermark namespaces and causal ordering | Session A coordinates; D is canonical-cursor decision owner | CANDIDATE | D-REV-P1-002; Storage/Consistency; E/F/G consumer review | Owner-reviewed typed contract; all namespaces and resume/gap semantics specified; interop tests pass with evidence |
| INT-X-02 Forget fence, producer barrier, derivative registration and completion | Session I | OPEN | INT-P0-02/03; D/E/F/G/H boundary contracts | Approved global protocol; late-derivative race matrix; per-target acknowledgements and residual exceptions |
| INT-X-03 Principal/ActorRef/ScopeRef/permission epoch/environment binding | Session I | OPEN | INT-P0-02; B domain refs; C/H transport; D/E/F/G enforcement | Authenticated binding contract and cross-scope negative tests |
| INT-X-04 Context delivery, final-request Applied, clear/reconnect | Session H | OPEN | G Context model; C final inference boundary; INT-P1-01/05; INT-P0-03 | H package, G/C owner sign-off, delivery/reconnect/late-ack/final-request evidence |
| INT-X-05 Canonical lifecycle authority, Claim revision and ConflictSet | Session B | ADR-BLOCKED | INT-P0-01; D lifecycle and canonical store; E/F/G consumers | Approved B ADR/domain semantics plus D owner alignment and migration/historical tests |
| INT-X-06 Accepted receipt, idempotency, replay ordering and retention | Session E | CANDIDATE | INT-P1-03/04; H/I; Storage/Consistency | E/H/I owner-approved schema; crash/replay/retention evidence |
| INT-X-07 Shared conformance and fault-injection suite | Session A coordinates; Testing owner TBD | TO_VALIDATE | INT-X-01..06 candidate contracts | Executable versioned suite, environment/data declaration, raw logs/artifacts, reproducible rerun; no PASS without evidence |
| INT-X-08 Representative workload benchmarks/resource budgets | Engineering owner TBD | OPEN | Stable candidate interfaces; correct conformance first | Reproducible workloads/hardware/data/config and results; no SLO or performance claim before measurement |

## 5. D-local review remediation register

| ID | Accountable owner | State | Dependency | Closure evidence / exit criterion |
|---|---|---|---|---|
| D-REV-P1-001 Forgetting vs Memory lifecycle vocabulary | Session D | CANDIDATE | D lifecycle owner approval; I completion policy | D branch contains one normative lifecycle table: in-progress work is ForgetOperation/fence, not a competing Memory lifecycle state; cross-doc consistency check |
| D-REV-P1-002 canonical commit sequence scope | Session D | OPEN | Storage/Consistency; E/F/G cursor consumers | D selects and documents global/partitioned commit cursor and per-aggregate revision separately; transaction visibility, gaps, replay and lifecycle relation tested |
| D-REV-P1-003 durable Forget fence and late-derivative barrier | Session D | OPEN | Session I global completion; E producer registration; F/G/H enforcement | Durable operation/fence plus producer inventory/barrier/watermarks; all in-flight and late derivative race tests; no resurrection |

## 6. Interface matrix — ownership and operational contract

This is a coordination matrix, not a wire schema. Immutable IDs and version fields below are semantic identifiers; serialization remains owned by the protocol owner.

| Interface | Producer → consumer | Authoritative owner | Immutable ID / version | Consistency expectation | Failure behavior | Retry / idempotency |
|---|---|---|---|---|---|---|
| Source Event ingress | C/H Adapter → E | E owns accepted Event/receipt; I owns authorization | EventID, ReceiptID, schema version, source cursor | Accepted only after durable Event + payload ref + idempotency + compile intent | Reject/Unavailable before Accepted; post-accept work remains recoverable | Same authenticated producer + scope + key + digest returns same receipt; changed digest conflicts |
| Canonical proposal/commit | E → D | D owns Memory/MemoryVersion and canonical commit | MemoryID, MemoryVersionID, per-aggregate revision, canonical cursor | Atomic/recoverable canonical commit and outbox; no partial visible commit | Stale base/conflict/reject; unknown outcome resolved by idempotency lookup | operation/idempotency key + request digest |
| Lifecycle change | D → E/F/G/I | D owns LifecycleEvent stream; I owns policy | LifecycleEventID + per-Memory lifecycle cursor | Append-only, ordered within aggregate; projections may lag | Consumers mark stale/blocked; canonical lifecycle wins | At-least-once event delivery; dedupe by LifecycleEventID |
| Canonical publication | D outbox/E publisher → F index | D owns canonical source; publisher owns per-index publication progress | Outbox EventID; index partition watermark | Per-index/partition contiguous applied prefix; lag explicit | Partial/stale; canonical read-through or bounded wait, else unavailable | Idempotent by source event ID + index generation |
| Retrieval | F → G | D owns canonical facts; F owns RetrievalResult/ActivationRecommendation | RequestID, candidate MemoryVersion refs, freshness vector | Scope-before-candidate; canonical/Forget revalidation; partial completeness explicit | Fail closed on auth/Forget uncertainty; partial on non-security channel lag | Read retries bounded; no stale result cache reuse across epochs |
| Context mutation | G → G | G owns Context/ContextVersion/ChangeSet | ContextID, ChangeSetID, immutable ContextVersion | CAS/per-Context serialization; atomic all-or-nothing commit | Base mismatch -> Conflict/replan; no partial target version | principal+context+operation family+key+payload hash |
| Context delivery | G → H Adapter | G owns desired version and Delivery record; H owns transport/Adapter behavior | DeliveryID, delivery sequence, target ContextVersion | Per delivery/session evidence; Applied only at final inference boundary | timeout = Unknown; stale/forgotten target blocked | DeliveryID stable across retry; duplicate returns prior result; new sequence for new delivery |
| Applied attestation | H/C inference boundary → G | H owns Adapter attestation; C owns inference request boundary; G records consumer history | DeliveryID, InferenceRequestID, capability epoch, boundary proof | Exact target fully materialized in managed region of exact submitted request | Partial/Bypassed/Unknown are not Full Applied | Attestation ID dedupe; late ack historical only, cannot roll back head |
| Forget suppression/clear | D/I → E/F/G/H | D owns canonical fence record; I owns global policy/completion | ForgetOperationID, typed fence epoch, target refs | Suppression before cleanup; fence checked before read/write/publish/delivery/apply | Unknown target remains pending/exception; no false completion | Monotonic fence; per-target idempotent action; resumable saga |
| Capability negotiation | H Adapter ↔ C/Agent runtime; G consumes | H owns Adapter capability epoch | AdapterID, capability epoch, negotiated tier | Epoch increments on capability/config identity change; proof bound to epoch | Unknown/unsupported capability lowers claim; never infer Tier 1 | Negotiation idempotent per adapter session; stale epoch rejected |
| Authorization decision | I → all protected producers/consumers | I | Principal/ActorRef, ScopeRef, policy/permission epoch | Reauthorize at each security-sensitive boundary; scope != permission | Fail closed if authority unavailable or epoch stale | Decision ID/request ID dedupe; current epoch always rechecked |

## 7. Coordination decisions and non-decisions

### DECIDED (baseline facts only)
- Brain is logical authority for canonical memory and managed Context; Agent owns reasoning/action/tool policy.
- D owns canonical Memory identity/version and LifecycleEvent authority; G owns ContextVersion; F owns retrieval projections/results, not Context.
- E Accepted is a durable receipt and is distinct from Compiled, CanonicalCommitted and Indexed.
- Indexes and caches are projections/derivatives; they never override canonical lifecycle, authorization or Forget.
- ContextVersion, Delivery and Applied are distinct state machines/facts.
- Context Remove is not canonical Forget; Applied is not proof of model attention.
- Memory payload is untrusted data; Scope and Permission remain distinct.
- No performance claim without reproducible measurement.

### CANDIDATE (requires owner review)
- Partitioned canonical commit cursor plus per-aggregate revision (rather than a single overloaded integer).
- E-owned source Event log cursor separate from source-provided producer sequence.
- Per-index/per-partition contiguous publication watermarks.
- Forget fence checked at every visibility/publication boundary and bound to a typed epoch.
- Delivery ID/sequence and Adapter capability epoch kept distinct from ContextVersion and InferenceRequestID.

### ADR-BLOCKED
- Fact/Claim identity and any schema derived from it.
- Claim revision/ConflictSet semantics dependent on Fact/Claim ADR.
- Global authorization and Forget completion policy pending I and applicable governance approval.

### OPEN / TO_VALIDATE
- Storage partitioning, transaction/WAL implementation, retention horizon and outbox topology.
- H BMCP wire envelope, exact Applied proof canonicalization and capability handshake.
- I principal binding, permission epoch scope, revocation SLA, backup/external erasure policy.
- Actual conformance, performance and hardware budgets.

## 8. Gate discipline and evidence policy

No row is closed by this registry alone. A row can move to DECIDED only when the accountable owner supplies an approved decision artifact and all dependencies are explicit. Security and erasure claims additionally require implementation evidence and policy approval. A test is **PASS** only with test ID/version, code or executable procedure, declared environment, input fixture, expected result, actual result, logs/artifact reference, and reproducible rerun. Otherwise use NOT_RUN, BLOCKED, FAIL, or TO_VALIDATE.

H/I absence is a blocking dependency for their owned decisions, not a reason to invent defaults. D/E/F/G branches remain separate. This branch does not merge or edit any module/governance file.
