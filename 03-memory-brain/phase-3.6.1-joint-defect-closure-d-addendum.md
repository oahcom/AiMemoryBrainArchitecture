# Phase 3.6.1 — D Joint Defect Closure Addendum

- Authority: user-delegated DE-S Joint Architect; D semantics only
- Status: **JOINT SEMANTIC DECISIONS RECORDED / IMPLEMENTATION NOT VERIFIED**
- Applies with and refines `phase-3.6-joint-forget-linearization-decision.md`.
- Does not approve or modify I/F/G/H/B ownership contracts.

## 1. JF-01 — Closed-world inventory is not the work high-water

The following are distinct, non-substitutable evidence:

1. `ProducerDomainInventoryEpoch`: I-authoritative closed-world inventory of producer/recipient classes and instances.
2. `ProducerRegistryVersion`: D-local version of producer classes registered and enabled/disabled in the D Forget authority.
3. `ProducerRegistrationHighWater`: D-local sequence cutoff of concrete WorkItems captured by one fence.
4. `ForgetFenceGeneration`: monotonic suppression generation.

A FenceSnapshotReceipt MUST bind all four values (and authority ID, ForgetOperationId, target-set digest, commit cursor and schema version). D MUST NOT infer global inventory completeness from a contiguous work sequence or a complete local producer registry.

Before D may issue a closed-world barrier snapshot, it requires an I-authoritative InventorySealReceipt binding the exact ProducerDomainInventoryEpoch, inventory digest, included/excluded class and instance identities, and explicit status for every inventory member. Every included producer class must map to a D ProducerClass registration or a durable, owner-authorized disabled/retired disposition. Missing, stale, unknown or digest-mismatched inventory evidence leaves the barrier **InventoryUnsealed** and prevents CanonicalSuppressionComplete. A later inventory epoch or newly discovered producer invalidates the seal and reopens reconciliation.

D owns validation and persistence of the seal reference; I alone defines and attests the global inventory. No I receipt means no global closed-world claim.

## 2. JF-02 — Authorization freshness at visibility linearization

D's Forget predicate and I's authorization predicate are separate mandatory predicates. The final visibility decision MUST bind an I-authoritative CommitAuthorizationReceipt to the exact principal/actor, action, resource/artifact, source lineage, ScopeRef, ForgetOperationId/fence generation, WorkItemId, AttemptId, LeaseEpoch, DependencySetDigest, and intended visibility operation.

The permit MUST carry PermissionEpoch, revocation watermark, decision ID, policy version, issuance/expiry, audience and unique nonce. It must be cryptographically verifiable and single-use/idempotently consumable. A cached authorization decision or a permit for another scope/action is invalid.

Freshness cannot be manufactured by comparing a locally cached PermissionEpoch. The deployment MUST implement one of these equivalent safety mechanisms:
- I and the visibility coordinator participate in the same linearizable commit domain; or
- I issues a linearizable commit permit/fencing grant whose validity is serialized against revocation, and revocation cannot become effective while an older permit can still commit; or
- a formally specified distributed commit protocol provides the same revocation-vs-publication ordering and crash recovery.

If the selected I interface cannot prove that ordering, publication fails closed. D does not mint permits or decide authorization policy. I confirmation/integration remains an external dependency and is not claimed by this addendum.

## 3. JF-03 — Output manifest freeze and root terminality

Every root WorkItem MUST have a durable output manifest with monotonic `OutputManifestVersion`, immutable manifest digest, declared output identities/slots, expected output count or explicit open-ended marker, derivation/child lineage, and state.

The manifest lifecycle is:
`Open → Frozen(version,digest) → Reopened(new version) → Frozen(...)`.
Only a frozen manifest may enter complete dependency registration and publication-gate evaluation. Any output addition/removal, changed output identity/digest, newly discovered child, or changed dependency set creates a new manifest version and invalidates dependent completeness/terminal receipts. A frozen manifest is never edited in place.

An open-ended producer must first durably close discovery and freeze a complete manifest; elapsed time, queue emptiness or worker completion is not proof of completeness. Each output has its own visibility decision and PublicationReceipt; atomic simultaneous visibility of all outputs is not implied. Root terminality is separate: it requires every frozen output to have a durable terminal disposition, all child WorkItems accounted for, every attempt/replay path closed, and no stale lease or outstanding commit outcome capable of later publication.

## 4. JF-04 — Commit outcome unknown is a first-class state

Every registration, fence, dependency, visibility and terminal operation has a stable idempotency key plus immutable request digest. A timeout, connection reset or lost ACK after submission yields `OutcomeUnknown`, never `Failed` and never `Succeeded`.

Recovery MUST query the authoritative linearization domain by the same key and digest:
- committed: return the original immutable receipt and commit cursor;
- durably rejected: return the original rejection receipt;
- proven not committed: retry the same key/digest;
- still indeterminate/unavailable: remain pending and fail closed.

Same key with a different digest is a permanent conflict. A caller MUST NOT create a replacement key to escape an unknown result. Publication ACK recovery reads the authoritative visibility record by ArtifactId + publication idempotency key and verifies digest, fence generation and receipt. Root work cannot terminalize while any operation outcome is unknown.

## 5. JF-05 — Canonical visibility applies to every read surface

D defines one authoritative visibility predicate; all read surfaces must enforce it, including direct canonical reads, retrieval/candidate APIs, reference resolution, indexes, caches, materialized views, exports and downstream consumers. An index/cache may be a candidate accelerator, never an independent authority.

Every returned artifact must be validated against its immutable ArtifactId/digest and current applicable ForgetFence/visibility state at response finalization. If the read path cannot prove current state, it returns no affected content (fail closed). Stale indexes may cause false negatives but must never cause false positives. Fence installation must invalidate or fence old cache/index generations; asynchronous invalidation alone is insufficient. F/F/G/H owner-specific enforcement remains their responsibility; D's contract does not claim their implementation.

## 6. JF-06 — Restore/recovery control-ledger barrier

The Forget control plane MUST be monotonic across data restore. Before any restored artifact, index, cache or replica serves reads or accepts publication, recovery must establish a control-ledger watermark at least as new as the authoritative pre-failure watermark and reconcile:
- ForgetOperation ledger and idempotency receipts;
- Fence generations and target-set digests;
- InventorySealReceipt / ProducerDomainInventoryEpoch;
- FenceSnapshotReceipt, registry versions and work high-waters;
- dependency completeness and output-manifest versions;
- publication/visibility and terminal receipts;
- authorization epoch/revocation watermark references;
- suppression and residual-exception references.

The preferred realization is an independently durable, monotonic control ledger or authoritative log replay with verified continuity. Restoring an older backup is not allowed to roll back a fence. If the latest control watermark cannot be proven, the authority remains **RecoveryQuarantined**: no affected reads, new publication, barrier completion or Global Forget claim. Reconciliation must be idempotent and produce a signed/immutable RecoveryReconciliationReceipt before reopening service.

## 7. D lifecycle and evidence consequences

`CanonicalSuppressionComplete` requires a sealed global inventory where I policy requires it, no unresolved captured work/output/attempt/outcome, and D's canonical target suppression proof. It remains distinct from I's Global Forget completion and physical erasure. A newly observed inventory epoch, output manifest mutation, unknown commit outcome or restore mismatch reopens the relevant proof.

These are architecture decisions, not implementation evidence. D36 race, recovery and fault tests remain **NOT RUN**.


## 8. Round-1 self-review closure — JF-07 / JF-08

### JF-07 — Manifest mutation and terminal disposition share one order

Output-manifest declaration, close-discovery, freeze, reopen, and root terminal disposition are durable D barrier events, not E-local metadata. Each event binds WorkItemId, root lineage, OutputManifestVersion, prior manifest digest, new manifest digest and idempotency key. The event must be ordered in the same authority as producer registration, fence installation and terminal disposition.

A manifest freeze is accepted only while the root is non-terminal and its current lease/producer authority is valid. Root terminalization must compare-and-set the exact final frozen version/digest and prove that no manifest mutation or child registration is pending or outcome-unknown. If manifest mutation wins, terminalization retries against the new version; if terminalization wins, subsequent mutation is rejected and cannot create an untracked output. Any legitimate later work must be a separately registered child/root obligation with explicit lineage and barrier accounting. No local E cache can decide this race.

### JF-08 — NOT_COMMITTED requires a completed authoritative decision barrier

An authoritative outcome lookup may return NOT_COMMITTED only after the coordinator has established a read/decision barrier that is ordered after the operation's possible commit point and has resolved every in-flight transaction/participant decision for that idempotency key. The result must include the barrier cursor/epoch and prove no committed receipt exists at or before that barrier. A stale replica, negative cache, absent row during an in-flight transaction, expired client timeout or coordinator unavailability is never proof of absence and must return UNKNOWN. If the commit decision cannot be fenced/resolved, retry is prohibited except as same-key idempotent replay when the coordinator explicitly supports it; terminality remains blocked.


### JF-09 — Publication must bind the current inventory seal and manifest version

The final publication predicate is extended: the gate must bind the current valid InventorySealReceipt / ProducerDomainInventoryEpoch (where the D closed-world contract requires it) and the exact current frozen OutputManifestVersion/digest. A stale seal, inventory epoch advance, manifest reopen, superseded freeze or mismatched digest denies publication. The coordinator checks these values at the visibility linearization point, not only when the producer entered PublishGatePending. If the inventory epoch advances or the manifest reopens before visibility commit, the producer must reconcile and obtain fresh receipts; an earlier dependency-complete receipt is not a permit.


## 9. Phase 3.6 deployment-profile consumption decision

D preserves all previously decided operation and linearization semantics. For the physical realization, D accepts the Storage-selected **single transactional database per Canonical Memory Authority with per-authority coordinator/serializable transaction** as the preferred logical deployment profile. D requires ProducerWork registration, Fence installation/high-water capture, dependency completeness, final visibility commit and terminal disposition to participate in the same authoritative serialization domain exactly as already specified.

CAS/conditional updates are acceptable as transaction-internal guards, not as a substitute for atomic dependent writes. A durable Work Ledger is required; a transactional outbox is a same-transaction delivery supplement, never visibility authority. Object/blob bytes remain private until the authoritative visibility pointer and PublicationReceipt commit.

This is not a concrete database selection or deployment approval. No engine/version/configuration, schema, HA/replication, failover or restore implementation is present in the repository. D does not certify implementation or tests.

**I external dependency remains BLOCKED:** I's current ProducerDomainInventoryEpoch/InventorySeal and PermissionEpoch/revocation commit contract are not governance-approved. Until I supplies current, commit-usable authorization evidence and inventory seal, D/E/Storage fail closed; D does not mint or approve I evidence. The I Owner request is tracked in repository issue #4.


## 10. I Phase 3.6 technical contract refresh — CommitAuthorizationReceipt

The current I branch now contains `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` (HEAD observed `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`). It supersedes earlier I technical Candidate/Open wording for the delegated BIH technical baseline only; it does **not** clear I governance approval or make I policy active.

D adopts the exact I-owned `CommitAuthorizationReceipt` terminology and consumption fields. The receipt binds policy domain, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation ID, operation payload digest, owner boundary and I decision ID. It is single-use, non-transferable and not an offline lease.

For final publication, D requires the E/Storage gate to submit/consume this receipt in the same I policy-domain commit-ordering protocol that serializes authorization decisions against revocation. The gate records I receipt ID, decision ID, policy-domain sequencer position, PermissionEpoch, operation digest, owner commit cursor/transaction ID, relevant revocation event/epoch and terminal outcome `COMMIT_WON`, `REVOCATION_WON` or `INDETERMINATE_ABORTED`. Indeterminate is never success. Offline leases and stale-epoch grace are prohibited in this Phase 3.6 baseline.

**JF-10 — I sequencer / Storage visibility commit crash-coupling remains OPEN (P0 integration blocker).** I specifies the single-use receipt and common per-domain ordering requirement, but the inspected I artifact does not fully define the crash-atomic protocol that binds an I sequencer outcome to the Storage VisibilityPointer + PublicationReceipt transaction (including I commit-won followed by owner DB crash/rollback, lost ACK and replay). D will not invent that cross-owner protocol. I + Storage must specify a recoverable, idempotent commit handshake/transaction participation whose durable terminal outcome proves both revocation order and owner visibility commit. Until then, final publication remains fail-closed and not implementation-approved.

I's ProducerDomainInventoryEpoch / InventorySeal and Global Forget Completion governance dependencies remain separately BLOCKED. The I inventory contract remains CANDIDATE; this technical authorization update does not approve it.
