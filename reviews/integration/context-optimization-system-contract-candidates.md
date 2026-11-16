# Context Optimization — System Contract Candidates

- Owner: A / Principal Integration Architect
- Status: candidate coordination contract; NOT API/schema freeze.
- Authority: each Owner defines its own object semantics; A records cross-module constraints only.

## 1. Status vocabulary

DECIDED = system invariant supported by baseline. CONDITIONAL = concept acceptable subject to Owner contract/evidence. BLOCKED = no implementation/exposure until P0 proof. OPEN = unresolved. REJECTED = excluded.

## 2. Authority map

| Concern | Authority |
|---|---|
| Canonical Memory, canonical revisions, CanonicalCommitCursor, ForgetOperation/Fence, canonical producer barrier | D |
| Compiler work lifecycle, canonical-derived registration and Publication Gate enforcement | E |
| Archive capture, immutable revisions, locator, read sessions/cursors/receipts, F metadata catalog/cache/completeness | F |
| Context membership/reference, TSS, ContextVersion, compaction, fidelity, lineage/loss, reconciliation/delivery intent | G |
| Principal/Actor/Scope, authorization, PermissionEpoch, retention, revocation/global Forget policy | I |
| BMCP wire, authenticated transport, ACK, cancellation, Adapter reconnect | H |
| Agent/Adapter inference boundary, final request evidence, protected prompt regions | C |
| Typed domain identity, Scope, epistemic/temporal semantics | B |
| Durability, atomic publication, backup/restore/PITR | Storage with D/I |
| Cross-module register and gate | A; cannot replace Owner acceptance |

Logical boundary does not mandate separate process/database/crate.

## 3. Core reference model

### 3.1 ArchiveLocator (F-owned)

Opaque reference to one immutable Archive object revision, exact content hash, source identity/revision and selector coordinate system. It is not authorization. It becomes unusable when stale, expired, suppressed, revoked or unverifiable.

### 3.2 ContextObservationReference (G-owned)

Context-versioned edge to an exact F ArchiveLocator, source revision/hash and optional range/ReadReceipt. Excerpt is optional; if present, it must be bound to exact bytes, range and revision. It does not clone mutable F lifecycle state.

ArchiveLocator and ContextObservationReference are distinct identities.

### 3.3 RecallIntent (G→F)

G-owned bounded recall request. H/I resolve authenticated actor and trusted scope. Caller labels and ContextVersion are not grants; ContextVersion is correlation only.

### 3.4 RecallSession / ReadCursor (F-owned)

Session binds authenticated security domain, trusted Scope, I PermissionEpoch, applicable D ForgetFence, exact object revision/hash/source revision, selector digest, budget and expiry. Cursor is subordinate to one session/object/revision/selector and cannot cross session, object, ContextVersion or source revision. A later ContextVersion opens a new authorized session.

### 3.5 ReadReceipt (F-owned immutable fact)

Binds exact returned range/page, object/archive/source revision, hash, integrity, permission/fence checkpoints, budget and completeness. Proves what F returned under that checkpoint only. It is not truth, grant, Canonical Evidence, Applied proof or durable read authorization.

### 3.6 ObservationRecallResult (F→G)

Authorized locators, optional bounded excerpts, ranges/receipts, provenance, integrity, freshness, completeness/omissions, budget exhaustion and typed failures. F never mutates Context or silently upgrades partial to complete. G revalidates dependencies before inclusion.

## 4. Object mapping

| Object | Creator | Authority | Consumer | Lifecycle | Permission | Forget |
|---|---|---|---|---|---|---|
| ArchiveObjectManifest | F | F runtime; D/I govern canonical ancestry/policy | F/G | immutable; active/quarantined/suppressed/expired | I | D if covered lineage; I retention |
| ArchiveLocator | F | F | G/F | revision-pinned/expiring | every dereference | source/ancestor fence |
| RecallIntent | G | G intent; H/I identity | F | request-scoped | before session/read | target fence |
| RecallSession | F | F | F/G | active/partial/complete/stale/suppressed | every read | D/I |
| ReadBudget | F; G hint | F consumed accounting | F/G | reserved/consumed/released | no grant | no bypass |
| ReadCursor | F | F | F/G | session/object/selector bound | every continuation | invalidated on fence/revoke |
| ReadReceipt | F | F | G/audit | immutable | later use reauthorized | retention/lineage |
| ObservationRecallResult | F | F facts; G acceptance | G | complete/partial/stale/etc. | final handoff | source lineage |
| CompletenessMetadata | F | F | G | immutable per result | no grant | omission/fence |
| WorkingSetObservationEntry | F | F | F/G | cache projection | every hit | inherits source lineage |
| TSS | G | G Context projection | H/C | ContextVersion-bound | I/D before publish | transitive sources |
| ContextObservationReference | G | G | G/H/C | ContextVersion-bound | I/D at commit/delivery | Archive/source fence |
| Compaction records | G | G | G/F/D audit | immutable/append-only | governed | transitive fence |
| ContextVersion linkage | G | G | H/C/F | immutable per Context | current I/D | dependency invalidation |

## 5. State/error semantics

Minimum outcomes; exact enum/wire codes are H-owned and OPEN.

- Archive: ACTIVE, QUARANTINED, SUPPRESSED, EXPIRED, STALE, UNAVAILABLE.
- Recall: COMPLETE, EMPTY_COMPLETE, PARTIAL, DEGRADED, STALE, UNAVAILABLE, SUPPRESSED, UNKNOWN, CANCELLED, EXPIRED.
- Context ref: VALID, STALE, EXPIRED, SUPPRESSED, UNAVAILABLE, REQUIRES_RECALL.
- Compaction: NOT_SELECTED, STAGED, VALIDATED, REJECTED_FIDELITY, ABORTED_DEPENDENCY, COMMITTED, DELIVERY_PENDING.
- Authority gap, unknown fence, stale permission, hash mismatch, cursor mismatch or uncertain terminal outcome fails closed.

## 6. Scope, Permission and Forget

I defines actor, trusted scopes, operation permission, PermissionEpoch, retention and revocation. D defines ForgetOperation, target lineage, fence generation and canonical producer barrier. F checks current I/D authority at capture admission, archive publication, each page, cursor continuation, cache hit, cache-fill publication and final F→G serialization. G checks I/D at Context staging/commit, compaction, delivery preparation and reconciliation. H reauthenticates on reconnect and suppresses before cached Context restore. C binds final request evidence to exact ContextVersion and applicable authority refs.

Locator, cursor, receipt, hash, cache key, ContextVersion and Applied attestation never grant authorization. Cached authorization requires an I-approved revocation guarantee; otherwise revalidate online. Unknown authority/fence/epoch/registration/terminal state means quarantine.

## 7. Typed token registry

| Token | Owner | Namespace/use |
|---|---|---|
| CanonicalCommitCursor | D | global canonical sequence per authority |
| AggregateRevision | D | one aggregate |
| LifecycleEventCursor | D | one Memory lifecycle |
| IndexWatermark | F | one index/channel partition, contiguous canonical coverage |
| ForgetFence Generation | D | independent fence namespace |
| PermissionEpoch | I | one policy domain |
| Archive ReadCursor | F | one RecallSession/object revision/selector |
| ContextVersion | G | one Context |
| Adapter CapabilityEpoch | H | Adapter capability scope |
| DeliveryId / InferenceRequestId | H/C | delivery/request correlation |

All tokens are opaque outside owner-defined operations. No cross-type comparison, arithmetic, max, coercion or substitution.

## 8. Canonical derivatives and Archive classification

Runtime-only observations are not Canonical Memory and do not automatically enter E's canonical index. F registers producer classes/work items with D when processing D-covered canonical sources or creating canonical-derived artifacts; D/I decide the complete producer/target inventory. TSS and Context compaction remain G-owned projections, not canonical truth, but D dependency registration/barrier applies when source lineage is D-covered. Only canonical Memory/index publication uses E/D canonical Publication Gate. F metadata catalog has its own F publication/invalidation, still subject to D/I lineage gates.

Every preview, normalized form, summary, embedding, page map, metadata index, cache, snapshot, delta and offline copy inherits applicable Scope, Permission, retention and Forget constraints.

## 9. Compaction

Boundary completion is an evaluation opportunity, not an unconditional command. G decision record includes remaining horizon/uncertainty, token/cache savings, compaction/cache write cost, recall/recovery cost, omission risk, repeated compaction overhead, latency/deadline and task class.

TSS is a versioned G Context projection, never Canonical Memory, Agent private state or CoT. Preserve epistemic status, time, scope and provenance. Fidelity hard checks cover goal/progress, constraints/negative conditions, fact/epistemic status, temporal order, provenance/recoverability and Scope/Permission/Forget. Hard veto beats aggregate score. Every successful compaction links ContextVersion to original sources and records omissions/loss. Staged work is non-visible until CAS and D/I gates pass.

## 10. Failure handling

Hash/revision mismatch → STALE/QUARANTINED. Permission denied/unknown → fail closed. Fence advanced/unknown → SUPPRESSED/QUARANTINED. Cursor mismatch → INVALID_CURSOR. Budget/timeout/partial index → PARTIAL. Receipt/validator mismatch → REJECTED_FIDELITY. Context CAS conflict → abort/rebase. Crash before final gate → non-visible recovery. Ambiguous terminal result → UNKNOWN/IN_DOUBT. Restore without authoritative fence reconciliation → QUARANTINED. Delivery failure never implies Applied.

## 11. Status register

| Item | Status | Acceptors |
|---|---|---|
| F Archive boundary | DECIDED conceptually | F, D, I |
| F/G Recall semantics | CONDITIONAL | F, G, B, H, I |
| Locator vs Context ref distinction | DECIDED conceptually | F, G, B |
| Excerpt optional/receipt-bound | CONDITIONAL | F, G |
| TSS | CONDITIONAL | G, B, C, D |
| Dynamic compaction | CONDITIONAL | G, C, H, F |
| Fidelity validator | CONDITIONAL | G, B, D, F |
| Lineage/loss ledger | CONDITIONAL | G, D, I |
| F metadata catalog distinct from E index | DECIDED | F, E, D, I |
| Archive retention/authorization | BLOCKED | I, D, F, H |
| Forget race/restore proof | BLOCKED | D, E, F, G, H, I, C, Storage |
| API/wire freeze | BLOCKED | B–I |
| Rust implementation | BLOCKED | B–I, Storage, A |
| Independent Observation Service | REJECTED | A |
| SAC default / Action Fusion in G/F | REJECTED | A |

This is a system candidate, not frozen API, wire schema, persistence layout or implementation behavior.
