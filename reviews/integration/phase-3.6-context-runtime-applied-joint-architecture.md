# Phase 3.6 — Context, Runtime & Applied Architecture Joint Closure (Session CFG)

- Owners: C — Agent Integration; F — Memory Runtime; G — Memory Context Manager
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Date: 2026-11-16
- Status: **C/F/G architecture decisions recorded; C and G approved A's Applied decision package with enumerated authority exceptions; H same-version approval PENDING; Applied Contract NOT FROZEN; CFG-01..20 and PI-01..08 SPECIFIED / NOT RUN; implementation NOT VERIFIED.**
- Decision package pinned: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`, Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`.
- This report is a CFG architecture decision and integration record. It is not an A final acceptance, H approval, I governance approval, D Forget completion, implementation certification or test report.

## 1. Branch-aware source baseline and evidence grades

The repository uses independent Owner branches. The live branch inventory includes `session-c-agent-integration-2026-11-16`, `session-f-memory-runtime`, `session-g-memory-context`, `session-h-bmcp-protocol`, `session-d-memory-brain-2026-11-16`, `session-i-security-governance-2026-11-16` and `session-a-integration-2026-11-16`. Owner branch presence, not `main`, is the artifact discovery authority.

### 1.1 Source artifacts read

| Owner | Branch | Artifact | Blob SHA read for this decision |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md` | `61d961c32138fd875069e8cbac4696bb031447c0` |
| A | session-a-integration-2026-11-16 | `reviews/integration/phase-3.6-context-runtime-evidence-joint-report.md` | `279e4b1fd12a3769085025c7e322a4f279999309` |
| A | session-a-integration-2026-11-16 | `reviews/integration/phase-3.6-cross-owner-freeze-and-executable-closure-plan.md` | `2845c2d6ed5a226d76af9b93dceb26bb1be5af68` |
| C | session-c-agent-integration-2026-11-16 | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `8db1140f0dd19fe9267e3f2b44a9c1be75a6c32b` |
| C | same | `07-agent-integration/inference-boundary-model.md` | `56b9e2e51804f8977797851a2cc41b6ebb7f2338` |
| C | same | `07-agent-integration/security-and-untrusted-memory-boundary.md` | `b32aeeb0b7b226cd3770d2af82b0ddfbf35a511d` |
| F | session-f-memory-runtime | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` | `176cd500bf5d9fa8519c5213e835a745567fcfad` |
| F | same | `05-memory-runtime/working-set-and-cache.md` | Read on Owner branch; retained semantics summarized below |
| G | session-g-memory-context | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `8f6b215de7b78bf0eec2281359d3e039e7c8d5f4` |
| G | same | `06-memory-context/context-versioning.md` | Read on Owner branch |
| G | same | `06-memory-context/context-edit-operations.md` | `10c94e85dfe89d20dcdb202cafc2bef767f076fc` |
| G | same | `06-memory-context/context-reconciliation.md` | `87063aceebed1c30b7840045ada8e3f348732688` |
| G | same | `06-memory-context/context-manager.md` | `ecc0549137a1738c197d02d12d94a1eb971ed6b5` |
| H | session-h-bmcp-protocol | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `ed6b43a29aa368d772c701ffc83309a5aadf3c00` |
| H | same | `08-bmcp-protocol/context-delivery-and-acknowledgement.md` | `bf9732cc39d156853b507c3a3a4e573159978f49` |
| H | same | `08-bmcp-protocol/forget-revocation-and-reconnect.md` | `695909360782987781e259187041618f495f1c8c` |
| H | same | `08-bmcp-protocol/phase-3.6-bih-joint-architecture-acceptance-addendum.md` | `adb2a879f263bb4c29232c7cfb4809fd5215cbe0` |
| D | session-d-memory-brain-2026-11-16 | `03-memory-brain/forget-fence-and-completion-contract.md` | `1f0391bc49d007c44ec74165bd33d37412cc7990` |
| I | session-i-security-governance-2026-11-16 | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | `74643a2f374179128d506c3b7e1d22da77119600` |
| I | same | `09-security-governance/scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` |
| I | same | `09-security-governance/threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` |

The C, F and G source files were subsequently extended by this CFG run. The resulting commits and post-write blob SHAs are recorded in §14. The source table above deliberately preserves the exact pre-decision blobs used for the review.

### 1.2 Evidence grade

- **Artifact Exists:** confirmed by fetching the exact Owner-branch file and Blob SHA.
- **Owner Decision:** C and G now record their decisions on the exact A package Blob SHA; F records its runtime integration decision.
- **Cross-module Agreement:** partial. H's current Owner addendum says C/F/G acceptance remains open and H36 is NOT RUN. No H approval of the exact A package Blob SHA is present in the inspected record.
- **Implementation Evidence:** absent for the CFG and PI suites. Specifications, static review, and commits are not execution evidence.

## 2. Final architecture and responsibility boundaries

### 2.1 C — Agent Integration and final request boundary

C owns Brain-to-Agent integration semantics, telemetry event meaning, Agent/Adapter/runtime/session binding requirements, Managed Region contract, final request boundary semantics and production of immutable final-submit evidence.

- Brain owns canonical Memory, retrieval/activation policy, desired Context state and its managed-region target.
- Adapter may materialize, replace, reorder or clear content only inside the explicitly delimited Brain-managed region, under current G target, I authorization and D Forget fence.
- Adapter MUST NOT modify System or Developer instructions, raw User content, Agent policy, tool definitions, credentials, tool authorization or other host-owned regions.
- Agent retains reasoning, planning, tool selection, action policy and execution control. Memory content cannot grant those capabilities.
- Agent/Adapter telemetry claims are not identity proof. The receiver resolves identity from authenticated transport/session/workload binding and compares payload claims against authoritative registries.
- Final Request Submitted is established only after all prompt assembly/transforms and the actual successful handoff to the declared inference runtime/provider submit boundary are observed. A local render, middleware buffer, transport ACK or successful context insertion is insufficient.
- C issues immutable evidence for the exact request. Corrections are superseding records, never in-place edits. C does not commit G Applied and cannot infer Execution Started.

### 2.2 F — Memory Runtime

F owns retrieval candidate processing, scope-before-candidate enforcement, activation, Working Set, index freshness, cache namespaces, invalidation, scheduling/cancellation and F-local suppression evidence.

- Canonical D Memory/lifecycle and D ForgetFence remain authoritative.
- F's index, cache, Working Set and retrieval result are projections. They cannot override canonical lifecycle, I authorization or D fence state.
- F filters scope and authorization before candidate emission, fusion, reranking, count, trace or cache disclosure.
- F owns IndexWatermark and its partition/schema/coverage semantics, not canonical commit ordering or Forget completion.
- F may perform bounded canonical read-through when the index is behind, but only after current authorization/fence validation and within the request budget. If that cannot be proven, return explicitly incomplete/unavailable; never infer deletion from absence.
- F reports index/cache/Working Set invalidation only. It does not report G Applied, H Adapter purge, D global Forget completion, I policy completion or physical erasure.

### 2.3 G — Memory Context Manager

G owns the desired Brain-managed Context, membership/order, entry metadata, ContextVersion, ChangeSet commit, budget allocation, reconciliation, Delivery intent/target and Applied state.

- G references canonical MemoryVersionRefs; it does not own or mutate canonical Memory.
- ContextVersion is immutable and scoped to a Context. It is not a canonical Memory revision, IndexWatermark, PermissionEpoch, ForgetFenceGeneration, CapabilityEpoch or delivery attempt.
- A Context mutation is validated against one exact BaseVersion in a staged working copy. A successful non-no-op ChangeSet creates one immutable ContextVersion; no partial target is published.
- Before a Context target becomes a public head, sendable Snapshot/Delta or Prepared Delivery, every referenced dependency must be registered with D, D's final publication gate and current ForgetFence must be proven, I's current PermissionEpoch/decision must be proven, and G's BaseVersion CAS must succeed.
- G alone commits Applied after validating C/H/I/D evidence. G does not own wire ACK semantics or infer proof.

## 3. Canonical six-stage Applied lifecycle

`Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`

| Stage | Authority | Entry evidence | Explicit non-claim |
|---|---|---|---|
| Prepared | G | Immutable ContextVersion, validated target, ChangeSet and Delivery intent | Not sent or received |
| Delivered | H | Authenticated receipt for exact DeliveryId and attempt | Not materialized or applied |
| Materialized | Adapter/H; C consumes | Exact ManagedRegion identity/revision and materialized digest | Not proof of final request inclusion |
| Final Request Submitted | C | Immutable proof that exact final request crossed actual submit boundary | Not G Applied or runtime execution start |
| Applied | G | Per-request predicate validation and immutable G Applied record | Not model attention, comprehension, use or correctness |
| Execution Started | Runtime/provider | Separate start receipt correlated to actual InferenceRequestId | Not completion or success |

State outcomes include Rejected, Expired, Superseded and Unknown. After an Applied fact, a later Forget/revocation/supersession can produce InvalidatedForCurrentUse without rewriting historical truth. Partial, Bypassed, Unknown and Unsupported are evidence dispositions, not Full Applied states.

A single scalar `applied_version` is prohibited as the complete state representation. Applied identity is per Context, exact version, Delivery/attempt, Adapter instance, Runtime Session and InferenceRequestId.

## 4. Applied Contract — common semantic field registry

The semantic field names below are the common contract vocabulary. H must define the versioned wire representation and schema IDs. Tokens from different authorities are opaque and non-comparable.

| Field | Definition / source | Authority | Produced / validated | Invalidated when | Missing behavior |
|---|---|---|---|---|---|
| ContextVersion | Immutable G target version | G | On successful ChangeSet commit; G validates exact head/target | Supersession, tombstone, expiry, scope/lineage invalidation | Reject Full; no float-to-latest |
| DeliveryId | Stable logical delivery identity | G | On Delivery intent; H binds receipt | Target superseded, cancelled or expired | No Delivered/Applied |
| DeliveryAttempt | Unique attempt under one DeliveryId | G issues; H receipts it | On each retry/attempt; H verifies exact attempt | Retry supersedes prior attempt, session/target changes | Treat as unknown attempt |
| InferenceRequestId | Actual runtime/provider request identifier | Runtime/provider assigns; C correlates | At submit boundary; C/H/G verify same request | Request/session correlation invalid or replayed | No Final Request Submitted / Full |
| AgentIdentity | Authenticated Agent principal/reference/instance | I trust; B types; H binds transport | Session establishment and each protected boundary | Credential, issuer, grant, binding or session revoked/expired | Fail closed |
| AdapterIdentity | Authenticated Adapter principal/reference/instance | I trust; B types; H binds transport | Adapter authentication and ACK/evidence validation | Instance replacement, credential revocation or binding mismatch | No trusted materialization/Applied |
| RuntimeSession | Authenticated runtime/session instance and generation | H transport/session binding; I policy consumes | Session establishment; C binds evidence | Session close/reconnect/replacement | Old evidence cannot be rebound |
| ManagedRegion | Exact Brain-controlled region, revision and coverage inventory | H/Adapter defines mechanism; G defines expected target; C observes final region | Materialization and final request inspection | Region layout/revision/capability change | Partial/Unknown; no Full |
| ContentDigest | Digest over complete ManagedRegion as present in final request, with canonicalization profile | C computes; H integrity-protects; G compares | After final transformations at submit boundary | Any content, coverage or canonicalization mismatch | Reject Full; quarantine mismatch |
| PermissionEpoch | I-issued generation in a named policy domain | I | At each protected operation and submit boundary | I policy/revocation event or epoch freshness loss | Fail closed; no cached ALLOW |
| ForgetFenceGeneration | D-issued suppression generation/cursor with exact target/lineage coverage | D | D fence publication; each consumer validates current coverage | New fence, lineage expansion or unproven cursor continuity | Suppress affected content |
| CapabilityEpoch | H-issued generation for exact Adapter instance/capability profile | H | Capability negotiation; H validates evidence tier | Build/config/runtime hook/region/coverage/key/profile changes | No Full; renegotiate |
| FinalRequestBoundary | C-defined actual final immutable request submit hook and boundary profile | C | At successful runtime/provider handoff | Hook bypass, transform after hook, boundary profile change | Unknown; no Full |
| SubmissionEvidence | Immutable C evidence binding request ID, boundary, target, digest, identity and authority snapshots | C | After successful observed submit; H transports/verifies; G consumes | Invalid integrity, replay, mismatch or superseding correction | No Final Request Submitted / Full |
| AuthorizationDecisionRef | I decision for exact principal/action/resource/audience/scope/purpose | I | At each protected disclosure/mutation/submit boundary | PermissionEpoch, grant, credential, scope or decision expiry/revocation | Fail closed |
| ScopeRef / EnvironmentRef | Typed, registry-backed ownership/applicability and environment references | B types; I authorizes | Resolve before candidate generation, Context mutation, delivery and submit | Registry change, grant revocation, environment/session switch | Reject cross-scope/environment |
| EvidenceIntegrity | Signature/MAC/key/issuer/schema/nonce/canonicalization evidence | I policy; H protocol; C issuer | At evidence creation and every acceptance | Key revoked/rotated, schema downgrade, nonce replay, digest mismatch | Quarantine / fail closed |
| AppliedRecordId | Immutable per-request G decision record | G | Only after complete predicate acceptance | Never rewritten; current-use projection may change | No Applied claim |
| ExecutionStartReceipt | Runtime/provider start fact bound to InferenceRequestId | Runtime/provider | When execution actually starts | Invalid correlation or integrity | Remain Applied; no Execution Started |

### 4.1 Full Applied predicate

G may append Full Applied only if all of the following are true:

1. Exact G ContextId/ContextVersion and active non-superseded DeliveryId/attempt match.
2. Actual InferenceRequestId and FinalRequestBoundary identify the same immutable submitted request.
3. Agent, Adapter, Runtime and Session identities are authenticated, registered, current and mutually bound.
4. Typed ScopeRef and required EnvironmentRef match the target and I decision.
5. ManagedRegion identity/revision/inventory is complete and matches the delivered target.
6. ContentDigest is computed over the complete region in the actual final request using the negotiated canonicalization profile.
7. C SubmissionEvidence is immutable, integrity-valid, non-replayed and demonstrates successful submit.
8. H delivery/identity/capability evidence binds the exact attempt, Adapter instance, session and CapabilityEpoch.
9. I AuthorizationDecisionRef and PermissionEpoch are current at the submission boundary.
10. D ForgetFenceGeneration and lineage coverage are current at the submission boundary.
11. No supersession, revocation, fence, scope/environment change, session replacement or capability downgrade linearized before submission.
12. No bypass, truncation, omitted path or unknown coverage gap exists.

No weaker receipt combination can be promoted to Full. Transport ACK, Forget ACK, materialization digest and local prompt buffer are separate evidence families.

## 5. Temporal ordering: ForgetFence and PermissionEpoch

ForgetFence and PermissionEpoch are independent:

- D ForgetFence controls canonical Forget suppression and lineage coverage.
- I PermissionEpoch controls authorization policy freshness and revocation.
- They have separate issuers, namespaces, monotonicity domains, event streams and validators.
- They MUST NOT be combined into a scalar, numerically compared, converted or used as substitutes.

### 5.1 Required boundary ordering

At each protected operation, validate both independently. The final submit boundary is the decisive disclosure linearization point for Applied:

| Ordering at authoritative boundary | Historical Applied | Current-use eligibility |
|---|---|---|
| Current PermissionEpoch and D fence validated; submit occurs; later Forget/revocation | Preserve historical fact if proof and causal ordering are valid | Immediately invalid after later transition |
| ForgetFence advances before submit | Reject Full; suppress target | Ineligible |
| PermissionEpoch revocation wins before submit | Reject/Unknown; no stale ALLOW | Ineligible |
| Both change concurrently and authoritative order is proven | Apply the proven order above | Recompute after both |
| Cross-authority order cannot be proven | Unknown; no Full | Suppress |
| Requester revoked after D fence commit | Preserve D suppression obligation | Cleanup only under a currently authorized service/continuity principal |

Wall-clock timestamps from independent services are not sufficient causal proof. Use a trusted authority receipt, shared serialization point or approved causal ordering proof. If no such proof exists, Unknown is mandatory. Already disclosed bytes cannot be recalled; block future access and invoke the applicable recipient/Forget workflow.

## 6. Context lifecycle and state transitions

G Context is a versioned desired-state object, not a copy of canonical Memory.

### 6.1 ChangeSet contract

Each operation is scoped to one Context and exact BaseVersion and carries stable operation_id, operation type, target entry, typed payload, preconditions, actor, reason, policy epoch and idempotency identity. Operations execute in deterministic order against a staged working copy. No partial target is visible.

- Exact duplicate operation identity and payload is idempotent.
- Same identity with altered payload is a conflict/quarantine.
- Stale BaseVersion is a conflict requiring reconciliation; no silent rebase.
- Successful non-no-op ChangeSet produces one immutable ContextVersion.
- A no-op may deduplicate without version bump only under the G-approved idempotency rule.
- No operation mutates canonical Memory by default.

### 6.2 Operation semantics

| Operation | Context effect | Canonical Memory effect | Required guard |
|---|---|---|---|
| Add | Add a new legal entry/reference and metadata | None | Canonical ref/version eligible, authorized, not tombstoned; budget passes |
| Update | Change entry metadata or replace exact referenced version under explicit policy | None | Exact BaseVersion and target; canonical version remains valid |
| Remove | Remove membership and write G membership tombstone | **No Forget** | Idempotent entry operation; old Snapshot/Delta cannot restore membership |
| Replace | Atomically substitute entry/set within one new ContextVersion | None | Whole ChangeSet validated; no partial publication |
| Reorder | Change deterministic order/priority only | None | Stable entry IDs and deterministic ordering |
| Expire | Make entry non-serving at authoritative expiry/policy boundary | None | Time/policy validation; replay cannot resurrect expired entry |
| Compact | Produce derived summary/compacted entry with lineage/provenance/trust/conflict metadata | None | Preserve source lineage and trust labels; never upgrade trust or instruction authority |
| Reconcile | Revalidate refs, versions, lifecycle, scope, permission, time, retrieval freshness and Adapter state; produce safe successor version or block | None | D/I authoritative checks; no implicit version float |

### 6.3 Context visibility gate

A ChangeSet may be staged privately while D/E/Storage work is pending. It is not a public Context head, sendable Snapshot/Delta or Prepared Delivery until all are true: D dependency registration is durable; D final publication gate validates current ForgetFence; I current PermissionEpoch/decision validates the actor and exact Scope; G BaseVersion CAS succeeds. Unknown means private/quarantined and not sendable. This does not presume a physical cross-store transaction or a callable D API.

## 7. Runtime consistency model

### 7.1 Scope-before-candidate

Authentication, typed Scope resolution and I authorization precede lexical, ANN, structured, temporal, graph, evidence and provenance candidate generation. Scope predicates must be pushed into candidate sources before top-k/fusion/ranking/counting. Post-filtering is insufficient because candidate counts, ranking and traces can leak existence.

Every evidence/provenance reference is independently authorized. An authorized parent Memory does not imply access to its evidence or graph endpoints.

### 7.2 Index lag and watermarks

IndexWatermark is F-owned, per index/channel/partition, and records a contiguous accounted-through canonical cursor plus schema and coverage. It is not D CanonicalCommitCursor, ForgetFence, global completion or proof of absence.

- Missing/delayed/failed/schema-incompatible events stop advancement before the gap.
- Multi-partition freshness is a vector, not a fabricated global maximum.
- On lag, F may bounded-read-through to canonical D for exact authorized refs; otherwise it marks the result incomplete/unavailable.
- Index rebuild/backfill/replay registers derivative-capable work with D before queue/lease/dereference/execution and validates current D fence + I permission at final publication.
- High watermark, successful rebuild or zero-hit query is never a Forget proof.

### 7.3 Cache and Working Set

Protected cache namespace binds principal/security domain, exact Scope and Environment, Agent/Task/RuntimeSession, PermissionEpoch, ForgetFence, exact MemoryVersion or index generation/watermark/schema/coverage, query fingerprint and validity. Cache keys are not grants. Every protected hit revalidates I/D/canonical lifecycle.

On fence/revocation: increment local invalidation generation; deny affected lineage; cancel in-flight fills/prefetch/graph expansion/reranking/materialization; evict or quarantine matching cache/Working Set entries; recheck at final visibility. A late fill cannot write or disclose stale content.

Working Set entries are references first. Snippets are protected cached content. ContextVersion remains G authority and is not a replacement for canonical MemoryVersion, watermark, permission, fence or capability epoch.

## 8. Runtime Forget Suppression end-to-end

The following sequence is normative at the architecture boundary. Each consumer emits only its own action-specific evidence.

| Step | Authority event / handler | State and ordering | Confirmation | Failure, retry and recovery |
|---|---|---|---|---|
| 1. Forget commit | D commits ForgetOperation and advances durable ForgetFence for exact targets/lineage | D canonical suppression obligation is durable before downstream cleanup | D fence/operation receipt | If authorization is revoked before fence commit, stop/re-authorize; after commit, obligation persists |
| 2. Runtime suppression | F consumes D fence; blocks candidate admission, final return and in-flight dereference | Suppressed immediately on unknown/stale fence; cancel in-flight work | F suppression receipt with target digest/checkpoint | Retry idempotently; reconcile cursor gaps from D; never serve during gap |
| 3. Index invalidation | F marks affected index partitions/artifacts stale and quarantined | Watermark cannot cross unaccounted event; rebuild work is D-registered | Per-partition invalidation and watermark vector | Retry rebuild only after D/I gates; quarantine stale snapshot; no absence claim |
| 4. Cache invalidation | F evicts/quarantines exact lineage and dependent cache namespaces | Invalidation generation advances; read-time authority recheck remains mandatory | Cache namespace/target digest and purge outcome | Lost notification repaired by read-time D/I check and replay; byte purge Unknown absent physical proof |
| 5. Working Set reconciliation | F suppresses refs/snippets, cancels fills and prefetch, invalidates session namespace | Old Working Set non-restorable | Session/namespace/checkpoint evidence | Keep deny markers only as I permits; reconnect from current authority, not old snapshot |
| 6. Context invalidation | G installs durable deny tombstone; invalidates affected entries, versions, ChangeSets and projections | Affected targets become non-serving before cleanup; historical Applied retained but current-use invalid | G tombstone/Context target evidence | Retry idempotently; stale staged ChangeSet remains private; reconcile new safe ContextVersion |
| 7. Delivery suppression | G cancels/supersedes pending attempts; H suppresses/clears Adapter ManagedRegion and local queues/caches | No old delivery is newly applied; ACK is target/action-specific | H status: SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN or UNSUPPORTED | Unknown/offline remains Pending; retry against same target identity; never promote one action status to another |
| 8. Adapter reconnect reconciliation | H authenticates new session and negotiates current capability; I/D provide current authority; G supplies current target; F supplies fresh runtime state | Old snapshot/delta/ACK quarantined; only current authorized target can be restored | New-session reconciliation receipt and exact current target binding | Reauthenticate, recheck both epochs/fence, suppress stale region before apply; full Snapshot only after authority continuity established |

**Completion boundary:** each row confirms only that owner's local action. Reconnect completion means one Adapter session is reconciled to a current authorized G target. It does not mean global Forget completion, provider-side deletion, physical erasure or model-internal state erasure.

## 9. Adapter boundary, reconnect and recovery

### 9.1 Adapter capability tiers

- **Tier 1:** exact final immutable request and successful submit are observable; complete region digest and request correlation are verifiable; may emit candidate Full evidence for G.
- **Tier 2:** managed region is observable but later transforms/submit are not; Partial/Unknown only.
- **Tier 3:** protocol transport/events only; no Applied claim.
- **Unsupported/Limited:** no demonstrated boundary/identity/digest/authority checks; no Full.

CapabilityEpoch changes when build/config/runtime hook, region isolation, coverage inventory, key binding, digest profile or relevant capabilities change. Evidence is evaluated against the epoch that produced it; no rebinding to a new Adapter instance/session.

### 9.2 Reconnect sequence

1. H authenticates transport, issuer, principal, Agent/Adapter/runtime instance and establishes a fresh RuntimeSession.
2. H negotiates protocol/schema/capability profile and current CapabilityEpoch.
3. I provides current PermissionEpoch and exact action/Scope authorization.
4. D provides current ForgetFence and target/lineage coverage.
5. F reconciles invalidation checkpoints and suppresses stale Working Set/cache/index projections.
6. G persists/revalidates deny tombstones, current Context head, delivery ledger and unresolved attempts.
7. Adapter/H suppresses or clears stale ManagedRegion, local caches and queued retries; emits action-specific evidence.
8. G rejects old Snapshot if superseded/tombstoned/stale/cross-scope/unauthorized. Delta is accepted only if its exact base equals the known current Adapter base and target remains current/authorized.
9. Unknown continuity requires a new full Snapshot only after current identity, permission, fence and Context target checks. Unknown authority blocks.
10. Revalidate I PermissionEpoch, D fence, G target/delivery state and H CapabilityEpoch immediately before apply and again before final submit.
11. C emits final-submit evidence for the exact new request; G accepts Applied only through the full predicate.

No queued payload or old Session ACK is replayed before this sequence. Offline is Pending/Unknown, never implicitly clear.

## 10. D/I/H compatibility and authority ordering

- D owns ForgetOperation, canonical target/lineage, ForgetFence generation/cursor, producer registration/barrier and canonical suppression proof.
- I owns Principal/Issuer/delegation trust, authorization decisions, PermissionEpoch, revocation, global inventory, retention and global completion policy.
- H owns BMCP envelope/field encoding, transport binding, ACK wire semantics, capability negotiation, replay/idempotency and reconnect execution.
- B owns typed ActorRef/ScopeRef/EnvironmentRef semantics.
- C/F/G consume these authorities; none redefines them.

PermissionEpoch and ForgetFence are independent. A Forget request is separately authorized under current I policy. If requester revocation precedes authorized fence commit, the operation must stop or be reauthorized. If the fence is already committed, revocation does not roll back the suppression obligation; cleanup may continue only under a currently authorized service/continuity principal. Every protected boundary reauthorizes; an old session, queued admission, cached ALLOW or unexpired TTL is not a reusable grant.

After final request submission, later Forget/revocation cannot retract the already-disclosed request. If submit-before-transition ordering is provable, G may retain historical Applied but must immediately invalidate current-use. If transition-before-submit is proven, reject Full. If incomparable/ambiguous, Unknown and suppress.

H's current Owner acceptance addendum reports its BIH joint acceptance only within that scope, says C/F/G acceptance remains open, and says H36 is NOT RUN. It does not approve this Applied package. No H wire schema freeze is claimed here.

## 11. Prompt-injection threat model

All Memory, Evidence, Provenance, summaries, entity descriptions, tool observations, historical Agent outputs, inferred claims and compacted content are untrusted data, even when authenticated or canonically stored. Authentication is source identity, not instruction authority or truth.

| Threat | Required defense | Evidence needed |
|---|---|---|
| Memory Instruction Injection | Memory stays in isolated managed data region; never enters System/Developer or Agent policy | Region inventory/digest and protected-region unchanged proof |
| Evidence Injection | Evidence and observations remain data with provenance; no tool/action authority | Source/provenance chain and no tool dispatch |
| Provenance Laundering | Summary/compaction preserves source lineage, trust, uncertainty and conflict; otherwise mark incomplete/quarantine | Before/after lineage and trust-label comparison |
| Cross-Scope Injection | Scope filter before candidate generation/fusion/count/materialization; independent endpoint/evidence authorization | Typed Scope decision and candidate exclusion trace |
| Malicious Memory Tool Instruction | Text describing a tool call is not authorization or execution; Agent policy independently authorizes tools | Tool-dispatch authorization and actual tool receipt |
| Forged Identity | Payload Agent/Adapter/Issuer/Actor/Scope/session claims compared with protected authenticated context | Transport/session binding and mismatch rejection |
| Reconnect Replay | Nonce/sequence, session/capability epoch, exact target/digest and durable idempotency; old ACK never rebound | Old/new session, replay decision, journal receipt |
| Forget / Revocation Race | D fence and I PermissionEpoch independently checked at each boundary; uncertain order fails closed | Authority receipts and deterministic submit ordering |

Cross-cutting rules:
- Memory cannot modify System/Developer/User regions or tool definitions/authorization.
- Summary/compaction is a derived untrusted artifact; it cannot gain trust merely by being summarized.
- Cross-Scope/Environment references are denied before they influence candidate counts or ranking.
- A forged ActorRef or AdapterId in payload is not a credential.
- A claimed tool result without a genuine tool execution receipt remains a claim/intent.
- A valid signature does not make malicious content safe.
- The system cannot guarantee that a model ignores malicious natural-language content after inclusion; residual model-behavior risk remains with Agent action policy and I risk acceptance.

## 12. Architecture conformance matrix — CFG-01..20

All cases below are **SPECIFIED / NOT RUN**. “NO” is not a test failure; it records absence of execution evidence.

| ID | Scenario / operation ordering | Expected architecture behavior | Test executed | Test passed |
|---|---|---|---|---|
| CFG-01 | Fence advances during Retrieval | F final disclosure gate suppresses affected content | NO | NO |
| CFG-02 | Fence advances during Context Delivery | G/H final delivery/apply gate cancels or supersedes stale attempt | NO | NO |
| CFG-03 | Late derivative after Forget | D/E publication gate rejects/quarantines; no runtime/context resurrection | NO | NO |
| CFG-04 | Index rebuild consumes old artifact | F revalidates current D fence and Published Artifact lineage | NO | NO |
| CFG-05 | Cache hit contains forgotten Memory | Read-time fence check suppresses entry | NO | NO |
| CFG-06 | Invalidation event lost | Durable D/I authority revalidation blocks stale disclosure; checkpoint resync | NO | NO |
| CFG-07 | Reconnect restores old Working Set | Suppress/clear, reauthenticate, reconcile epochs/fence/G; reject old state | NO | NO |
| CFG-08 | PermissionEpoch changes during Retrieval | F reauthorizes at final disclosure; stale result suppressed | NO | NO |
| CFG-09 | PermissionEpoch changes before Applied decision | G rejects Full unless current I decision valid at submit boundary | NO | NO |
| CFG-10 | Cross-Scope Context Delivery | B/I typed scope and authorization mismatch fails closed | NO | NO |
| CFG-11 | Agent/Adapter identity mismatch | H/I binding rejects; no Applied | NO | NO |
| CFG-12 | Revocation during final request assembly | C/H/G boundary recheck blocks or marks Unknown; no stale Full | NO | NO |
| CFG-13 | Materialized but no Final Request Submitted | G remains Materialized; no Applied | NO | NO |
| CFG-14 | Submitted but no G acceptance | FinalRequestSubmitted only | NO | NO |
| CFG-15 | Applied but Execution not started | Historical Applied only; no ExecutionStarted claim | NO | NO |
| CFG-16 | Late ACK after newer Context/delivery | Historical only; no rollback | NO | NO |
| CFG-17 | Duplicate ACK | Same digest idempotent; altered digest conflict | NO | NO |
| CFG-18 | Old Session ACK after reconnect | Reject or historical only; never rebind | NO | NO |
| CFG-19 | Context supersession | Old delivery/ACK cannot become current Applied | NO | NO |
| CFG-20 | Forget races Final Request Submission | D/I/C authoritative order decides; ambiguous ordering blocks | NO | NO |

Each executed test must record test ID, source commit and Blob SHAs, build/deployment and runner identity, Adapter/runtime/provider version, Tier/CapabilityEpoch, schema version, authenticated identity class, Scope/Environment, ContextVersion/Delivery, PermissionEpoch, ForgetFence, deterministic latches, expected/actual output, request/region digests, raw logs and reviewer. Static document review is not execution.

## 13. Prompt-injection conformance matrix — PI-01..08

All cases are **SPECIFIED / NOT RUN**.

| ID | Attack fixture | Expected defense | Forbidden outcome | Executed / passed |
|---|---|---|---|---|
| PI-01 | Memory contains “ignore system policy” instruction | Retain as untrusted data in isolated region | Promote to System/Developer instruction | NO / NO |
| PI-02 | Evidence or summary contains malicious tool command | Data-only; no tool authorization | Execute based on Memory text | NO / NO |
| PI-03 | Summary/compaction omits source provenance | Reject or mark provenance-incomplete; no trust upgrade | Treat summary as verified canonical fact | NO / NO |
| PI-04 | Cross-Scope Memory snippet injected into retrieval result | Reject before fusion/materialization/final delivery | Leak snippet, count or existence across Scope | NO / NO |
| PI-05 | Payload forges Actor/Agent/Adapter/Issuer/Scope IDs | Compare with protected authenticated binding; reject mismatch | Trust payload identity as credential | NO / NO |
| PI-06 | Memory says a tool call succeeded without tool receipt | Preserve as claim/intent only | Promote to observed side effect | NO / NO |
| PI-07 | Malicious content attempts to escape Managed Region into privileged prompt slot | Region isolation rejects | Mutate protected instructions/tool definitions | NO / NO |
| PI-08 | Compaction merges conflicting claims and drops trust labels | Preserve conflict/provenance/epistemic metadata or refuse | Convert uncertain data into trusted fact | NO / NO |

These eight tests complement, and do not replace, I36-T01..T20, H36 cases, C final-boundary cases or the broader security plan. They do not certify model robustness or close I's governance risk acceptance.

## 14. Owner decisions and delivery evidence

### 14.1 C decision

C recorded **APPROVE WITH ENUMERATED EXCEPTIONS** for the C-owned final-request semantics and shared lifecycle against A package Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`.

- Commit: `2fe2e428de0cd623645d63710d2516d07aa53df4`
- Updated blob: `45cab0f9c538fa653ac9e3ca8ddba3dee1b8383b`
- File: `07-agent-integration/phase-3.6-final-request-evidence-contract.md`
- Exceptions: H wire schema/ACK/capability, I authorization/PermissionEpoch, D ForgetFence/lineage, B typed references and all implementation/test evidence remain under their respective authorities.

### 14.2 F decision

F recorded the runtime consistency, scope-before-candidate, index lag, cache/Working Set and dual-authority invalidation decisions.

- Commit: `4928ecdcb6a91e85f98d94e0fff9a57272a35b25`
- Updated blob: `cd34244a3d92aff2ade1fc7758874cf30e512564`
- File: `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md`
- F did not approve C/G/H wire or Applied authority on behalf of those owners.

### 14.3 G decision

G recorded **APPROVE WITH ENUMERATED EXCEPTIONS** for G-owned ContextVersion, Delivery and Applied semantics against the same A package Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`.

- Commit: `faa6bff02840d3188c78dd1a001b1144d7b80278`
- Updated blob: `6513932991fdbe13231b26e43440fc2c4fcbf7fa`
- File: `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`
- Exceptions: H wire schema/ACK/capability, C evidence production, I authorization, D ForgetFence, B typed references, and D/E/Storage publication realization remain under their respective authorities.

### 14.4 H and external authority ledger

| Authority | Current disposition for this Applied package | Required next decision |
|---|---|---|
| C | APPROVE WITH ENUMERATED EXCEPTIONS — recorded above | No further C semantic change unless package version changes |
| G | APPROVE WITH ENUMERATED EXCEPTIONS — recorded above | No further G semantic change unless package version changes |
| F | Runtime architecture decision recorded | F execution evidence later |
| H | **APPROVE WITH ENUMERATED EXCEPTIONS** — H-owned protocol binding only; exact wire schema remains open | H must explicitly accept the exact package Blob SHA or enumerate exceptions/replacement and repin common version |
| I | Predicate confirmation pending; I policy remains CANDIDATE / GOVERNANCE-BLOCKED | Approve PermissionEpoch/authorization mapping and governance version under I authority |
| D | Predicate confirmation pending; D canonical semantics decided but cross-owner execution open | Confirm ForgetFence/lineage ordering for exact Applied submit boundary |
| B | **APPROVE WITH ENUMERATED EXCEPTIONS** — B semantic reference mapping only; I registry/trust policy remains open | Confirm ActorRef/ScopeRef/EnvironmentRef bindings without reopening unrelated ADRs |

C/G approval is intentionally not represented as C/G/H joint acceptance. A's approval ledger remains A-owned and must be reconciled by A.

## 15. Remaining decisions and blockers

1. **H same-version acceptance:** no H approval of A package Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0` is recorded. H must approve or enumerate exceptions. Until then Applied Contract Frozen = NO.
2. **H concrete wire contract:** exact schema IDs, field encoding, ACK enums, signatures/MAC/key lifecycle, canonicalization, replay nonce/sequence, durable journal, receiver ordering, capability epoch and reconnect semantics require H-owned versioned schema and approval.
3. **I authorization governance:** PermissionEpoch policy domain/fan-out, issuer trust, delegation, revocation freshness, cross-Scope/Environment grants, exception authority and global Forget inventory/seal remain I-owned and not fully approved.
4. **D Forget ordering:** D has confirmed its fence/lineage semantics for the exact package: submit-before-fence may remain historical only; fence-before-submit rejects Full; ambiguous order is Unknown/suppressed. Executable causal ordering and D/E/Storage proof remain open. A fence token cannot be inferred from a watermark.
5. **B typed identity:** ActorRef/ScopeRef/EnvironmentRef and scope hierarchy remain B-owned. Fact/Claim ADR status is not changed by this CFG work.
6. **D/E/Storage publication realization:** durable producer/dependency registration, Forget barrier, final visibility gate, crash/failover/restore and callable API remain design-level/open to the DE-S owners. A staged G ChangeSet remains private without that proof.
7. **Executable implementation:** no executable C/F/G/H Adapter/provider/database environment, deterministic race runner, deployment identity or reproducible logs were supplied.
8. **Test execution:** CFG-01..20, PI-01..08, H36, I36 and relevant D/E/Storage suites remain NOT RUN unless separate execution artifacts are attached and reviewed.
9. **Residual prompt-injection risk:** region separation and data-only semantics reduce privilege escalation but cannot guarantee model behavior. I/Agent risk acceptance and adversarial testing remain required.

## 16. Final CFG disposition

- C/F/G semantic architecture: **DECIDED and preserved**, with explicit Owner addenda.
- C package decision: **APPROVE WITH ENUMERATED EXCEPTIONS**.
- G package decision: **APPROVE WITH ENUMERATED EXCEPTIONS**.
- F runtime integration: **DECIDED at architecture level**.
- C/G/H same-version semantic acceptance: **RECORDED WITH ENUMERATED EXCEPTIONS** (C, G and H decisions pinned to the same A package SHA); exact H wire schema and I/D authority predicates remain open.
- Applied Contract Freeze: **NO**.
- Runtime Forget end-to-end closure: **NO**.
- CFG-01..20: **SPECIFIED / NOT RUN**.
- PI-01..08: **SPECIFIED / NOT RUN**.
- Implementation verified: **NO**.
- Global Forget complete / physical erasure: **NOT CLAIMED**.

H and B have now recorded explicit decisions with enumerated exceptions against the pinned A package; D has confirmed its fence semantics; I has explicitly withheld approval pending governance. The next valid closure step is to resolve I governance and exact H wire schema, then obtain D/E/Storage executable linearization evidence and run cross-owner conformance. No architecture statement in this report substitutes for those decisions or evidence.


## 17. Phase 3.6.2 — Owner decision reconciliation (2026-11-16)

All decisions below reference the same A package Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`. These are owner-artifact decisions, not independent governance signatures.

| Owner | Updated owner artifact blob | Decision on the pinned package | Exact limit |
|---|---|---|---|
| C | `45cab0f9c538fa653ac9e3ca8ddba3dee1b8383b` | APPROVE WITH ENUMERATED EXCEPTIONS | C final-submit semantics only |
| G | `6513932991fdbe13231b26e43440fc2c4fcbf7fa` | APPROVE WITH ENUMERATED EXCEPTIONS | G Context/Delivery/Applied semantics only |
| H | `afe74345936e29c3d9cd4fb8b4ec0e665446d435` | APPROVE WITH ENUMERATED EXCEPTIONS | H protocol binding; concrete wire schema remains open |
| B | `08af297cb010f7e6ac5e3f29daa4469be112e12e` | APPROVE WITH ENUMERATED EXCEPTIONS | Typed-reference semantics only; I policy remains open |
| D | `f4447ae1c3db9bbe9a3e93f2079423e8631c690f` | APPROVE D-OWNED FENCE/LINEAGE SEMANTICS WITH AUTHORITY RESERVATIONS | Causal runtime proof and D/E/Storage realization remain open |
| I | `17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c` | CANDIDATE / NO APPROVAL | Governance, issuer trust, PermissionEpoch operational policy and global Forget policy blocked |

C/G/H have all made explicit decisions on the same exact A package version. This is **not** Applied Contract Freeze: H's concrete versioned wire package is not frozen, and I's required authorization approval is withheld. D's semantic confirmation does not replace executable serialization proof.

### 17.1 Updated closure state

- C/G/H same-version semantic decisions: **RECORDED WITH ENUMERATED EXCEPTIONS**.
- B typed-reference semantic confirmation: **RECORDED WITH ENUMERATED EXCEPTIONS**.
- D fence/lineage predicate confirmation: **RECORDED; EXECUTABLE ORDERING NOT VERIFIED**.
- I PermissionEpoch / authorization predicate: **BLOCKED — NO APPROVAL**.
- H concrete versioned Applied/ACK wire schema: **OPEN — NOT FROZEN**.
- Applied Contract Frozen: **NO**.
- Runtime Forget end-to-end closure: **NO**.
- CFG-01..20 / PI-01..08 / H36 / I36 / D36 / DE-S fault-race suites: **SPECIFIED / NOT RUN** unless separate raw execution artifacts are attached.
- Implementation verified: **NO**.
- Global Forget completion / physical erasure: **NOT CLAIMED**.

### 17.2 Exact owner artifact references

- H: `08-bmcp-protocol/phase-3.6-bih-joint-architecture-acceptance-addendum.md`, blob `afe74345936e29c3d9cd4fb8b4ec0e665446d435`.
- B: `02-domain-model/typed-reference-registry.md`, blob `08af297cb010f7e6ac5e3f29daa4469be112e12e`.
- I: `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md`, blob `17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c`.
- D: `03-memory-brain/forget-fence-operation-and-publication-gate.md`, blob `f4447ae1c3db9bbe9a3e93f2079423e8631c690f`.
