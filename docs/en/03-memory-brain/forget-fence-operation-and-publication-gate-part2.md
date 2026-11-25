# Forget Fence Atomicity, Producer Admission and Publication Gate — Part 2

- Document ID: D-FORGET-GATE-001-P2
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: d3ddfff9500d9138d643989e8496d99b8d9ed79e
- Source: [canonical D source](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md) (source commit `b525e1f8fee2471a131e4a38efda99804045e424`; original source blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`).
- Chinese counterpart: [Part 2 — 可见性边界、证据、故障矩阵与裁决](../../zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate-part2.md)
- Source sections: 6–11

## 6. Derivative visibility atomic boundary

Artifact consumer-visible state and final fence/permission decision must have one externally observable linearization point. D owns the semantic rule; Storage/Consistency must nominate and validate the realization.

1. Staged artifact is private by default; no consumer-facing index, outbox, cache, canonical read or Context input can enumerate it.
2. D dependency registration durably commits artifact identity and every direct/transitive source edge before publication.
3. Final gate validates RegistrationReceipt, all DependencyRegistrationReceipts, work/attempt/lease liveness, exact ScopeRefs, every source ancestor's current fence status, and I current PermissionEpoch/authorization decision.
4. Same atomic/linearizable commit records successful PublicationReceipt and flips authoritative visibility marker. If commit aborts, neither success receipt nor visible state exists.
5. Cross-store prepare/commit is permitted only if prepare remains hidden; commit is one-time CAS/transaction bound to exact fence and permission decision; fence installation serializes with commit; recovery never exposes prepared/unknown artifact without committed proof.
6. After crash, replay, rebuild or restore, visibility is reconstructed only from committed publication records and revalidated against latest fence before exposure. Replayed dependency record alone cannot make artifact visible.

Lost ACK is resolved with ResolveProducerWork using same stable operation ID/digest. If committed, return original receipt; otherwise retry same idempotency key. Never create a new artifact identity or publication key to bypass uncertainty.

## 7. Publish Gate Evidence — minimum immutable binding

Every PublicationReceipt binds:
- WorkItemId and AttemptId; LeaseId when used;
- ProducerClassId and ProducerRegistryVersion;
- DerivationRunId;
- source MemoryVersionRef(s), exact SourceRevision(s), complete transitive lineage digest;
- ScopeRef set and scope/tenant/security-domain binding;
- Producer RegistrationReceipt ID + request digest + ProducerRegistrationSequence;
- observed ForgetFenceCursor and authoritative fence decision at commit (typed separately);
- I PermissionEpoch + authorization-decision reference/result;
- DerivedArtifactRef/version and private staging object/version identity;
- every DependencyRegistrationReceipt ID, inventory position and lineage digest;
- PublicationOperationId, request digest, visibility commit ID/CanonicalCommitCursor where applicable, final disposition.

Do not place FenceGeneration and PermissionEpoch in a shared integer field or compare them numerically. Do not omit AttemptId when delayed workers may return after lease replacement. Receipt is immutable and non-reconstructive: identifiers, digests and outcomes only, no forgotten plaintext.

## 8. E / Storage / I interface mapping

| Boundary | D provides / decides | E consumes / emits | Other owner / OPEN |
|---|---|---|---|
| Producer class | Registry identity/version/status/receipt and closed-world completeness | Register compiler/replay/rebuild classes before accepting work | I/A reconcile registry inventory across producer domains; owner mapping OPEN |
| Work admission | RegistrationReceipt, high-water sequence, disposition and barrier membership | Stable WorkItemId across retries; no queue/lease/run before receipt; ACK-loss lookup | H/I authenticated ProducerIdentity and Scope/Permission validation OPEN |
| Fence install | ForgetFenceCursor, install commit cursor, captured registry version + work high-water + target snapshot | Stop/park covered work and propagate typed fence | Storage/Consistency proves registration/fence serialization |
| Dependency inventory | Durable dependency receipt and inventory position | Register all direct/transitive lineage before visibility; staged output private | E owns lineage production; B typed-ref vocabulary may remain ADR-blocked |
| Publish gate | Final authoritative fence/registration decision and PublicationReceipt semantics | Submit evidence; expose only after successful committed receipt | Storage/Consistency atomically couples gate/visibility; I supplies current permission decision |
| Terminal work | Validated terminal receipt and barrier update | Preserve DLQ/retry/lease identity; submit terminal only when no publish path remains | E owns terminal truth; D validates barrier evidence |
| Reconciliation | D barrier receipt with exact high-water and unresolved counts | Supply registration/dependency/publication/terminal evidence | I consumes D result but decides global completion |
| Global Forget | D-local canonical suppression proof only | No global completion assertion | I owns policy, exceptions, backup/external-copy and physical erasure |

### 8.1 Storage/Consistency acceptance requirements — owner OPEN

A Storage/Consistency owner must be explicitly assigned before implementation approval. That owner must select and validate one of:
- a single ACID transaction covering fence state, registration ledger/dependency records and artifact visibility marker;
- serializable transactions or conditional writes/CAS sharing a linearizable fence version and publication decision;
- durable transactional outbox plus hidden prepare/commit protocol whose recovery preserves no-visible-before-commit;
- another formally specified equivalent with explicit serialization point and crash-recovery proof.

Evidence required: isolation/consistency model; transaction participants; linearization point; idempotency/uniqueness constraints; failure injection before/after each durable write; crash recovery; concurrent register/fence/publish tests; replica/read consistency; backup/restore fence reapplication; proof stale tokens cannot publish after newer fence. D does not select or certify a specific database, lock manager or distributed transaction product.

**OPEN: no formally named Storage/Consistency Owner or implementation evidence was found in the reviewed contract set.**

## 9. Fault/Race Conformance Matrix — design expectations, NOT RUN

| # | Initial state | Interleaving / fault | Required result | Forbidden result |
|---:|---|---|---|---|
| 1 | Class enabled; Work absent; Fence absent | RegisterProducerWork races InstallForgetFence | Shared serialization yields accepted + sequence <= captured H, or rejected/quarantined after fence | Accepted work omitted from H yet allowed to run/publish |
| 2 | Fence installed; registration committed but response lost | E retries same WorkItemId/digest or resolves | Same receipt/sequence returned; if fence won, authoritative rejection | New work ID, duplicate ledger row, assumed acceptance |
| 3 | Work registered; artifact staged privately; dependency receipt durable | Crash before Publish | Artifact stays private; recovery resolves same IDs and rechecks fence/permission | Staged artifact visible on restart/replay |
| 4 | Publish committed; response lost | E retries same PublicationOperationId | Same PublicationReceipt returned; visibility matches committed receipt | Duplicate publication or visible artifact without receipt |
| 5 | Work leased under Attempt A / Lease L1 | Lease expires; Worker B retries with Attempt B / Lease L2 | Same WorkItemId/lineage; old attempt fenced; new attempt refreshes permission/fence | Expiry closes barrier or old attempt publishes |
| 6 | Work in DLQ; registration open | Operator/system replays item | Same WorkItemId/lineage, new AttemptId; reauthorize/recheck fence; barrier stays open | New untracked admission or DLQ treated terminal |
| 7 | Dependency inventory contains artifact lineage | Index/backfill/rebuild replays old staged/visible data | Rebuild uses committed publication state and current fence; covered artifact suppressed before index visibility | Replay makes artifact visible without fresh fence check |
| 8 | Artifact staged and dependency registered at fence G | Fence advances to G+1 before final Publish | Final gate sees latest fence and rejects/quarantines; no visibility commit | Staging-time G authorizes publication |
| 9 | PermissionEpoch P observed at admission | I revokes/advances policy before final Publish | I decision at final gate denies/stales; artifact remains private | Numeric comparison with FenceGeneration or admission epoch treated as permanent |
| 10 | ProducerClass absent/disabled/unknown | Producer attempts registration/submit | Reject/quarantine; audit; barrier cannot be certified closed if inventory incomplete | Auto-register on first work or allow side-channel publish |

Additional mandatory variants: partial dependency receipts; same key/different digest; fence lookup unavailable; terminal ACK lost; late derivative after prior proof; overlapping Forget fences; restore from backup; publication CAS conflict; permission lookup timeout. All remain fail-closed and require deterministic reconciliation.

## 10. Decision status and unresolved owners

| Item | Decision | Owner / next action |
|---|---|---|
| Operation semantics and idempotency | DECIDED — D semantic contract | D maintains normative operation meanings |
| Register/Fence total order and two-outcome race | DECIDED — D semantic contract | Storage/Consistency implements/proves shared serialization |
| Dependency-before-visible rule | DECIDED — D semantic contract | E produces lineage; Storage/Consistency proves visibility boundary |
| Publish gate evidence | DECIDED — D semantic contract | I supplies permission decision; E supplies work/attempt evidence |
| PermissionEpoch/revocation policy | OPEN / I-owned | I defines current decision semantics and lookup |
| Authenticated ProducerIdentity / ActorRef / ScopeRef | OPEN / I-H-B-owned | I/H/B align identity and typed refs; D consumes verified refs |
| Producer class global completeness | OPEN / I + A + module owners | Reconcile D local registry with I global producer/recipient inventory |
| Storage transaction/CAS/lock/consistency | OPEN — OWNER UNASSIGNED | Architecture/Engineering names accountable owner; no D self-approval |
| E operation/API mapping and terminal evidence | OPEN / E + D | E maps compiler states to semantics; D defines receipt semantics |
| H/F/G producer/consumer enforcement | OPEN / H/F/G | Each owner supplies its own conformance; D does not edit their files |
| Global Forget, exceptions, backup/external copies, physical erasure | OPEN / I-owned | I decides policy and global proof |
| Runtime/fault-injection tests | NOT RUN | Storage + E + D + relevant consumers attach evidence |

## 11. D-local acceptance and non-claims

D-local documentation acceptance requires unambiguous operation contracts and two-outcome registration/fence order, minimum PublishReceipt evidence, and deterministic expected outcomes for all ten fault/race scenarios. This document meets the documentation/design specification criterion only.

It does not establish D APIs exist, E consumes a final approved schema, Storage atomicity is implemented, any fault test passed, H/F/G conform, I approved global policy, or Forget is end-to-end/physically complete. D-REV-P1-003 remains integration-open until owner implementation and conformance evidence are reviewed.




---

