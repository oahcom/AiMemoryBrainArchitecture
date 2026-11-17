# Issue #20 — F/E/G/H/Storage/A Role Simulations and Integrated Resolution Draft

**Status:** COORDINATOR-AUTHORED ROLE SIMULATIONS / NON-NORMATIVE / NOT OWNER DECISIONS  
**Exact Storage target:** commit `a65973093bb33c7c06ae503f421e096fadb5796b`, Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`  
**Depends on:** D and I role-simulation drafts plus D/I cross-review reconciliation in this directory.

## F — Archive and Recall role simulation

### Proposed F-owned contract
1. Distinguish immutable ArchiveObjectId, ArchiveRevisionId, CaptureOperationId, RecallSessionId, CursorId and RestoreGeneration. Never reuse one identity for another.
2. Every captured object carries producer classification receipt, source revision digest, lineage digest, capture policy version and D/I authority references. Mixed/unknown classification remains quarantined from canonical Recall.
3. Recall authorization is checked on each page, not only session creation: cache hit, page fetch, cursor resume, export and onward handoff all revalidate current D FenceGeneration and I PermissionEpoch/SealGeneration.
4. Cursor is an opaque signed continuation bound to subject, scope, object-set digest, policy, D/I generations, F index generation and expiry. Any generation change invalidates it; client cannot edit offsets or substitute a cursor across principals.
5. F RestoreReadiness receipt proves object catalog, revisions, indexes, caches, cursors and active sessions have reconciled against current D/I controls. F-local release is independent of Storage serving.
6. Partial/corrupt capture or missing lineage remains unavailable; restore cannot promote it to complete.

### Required tests
Stale cursor after Forget; cached object after PermissionEpoch change; mixed object; duplicate capture retry; partial upload; index lag; restore with old snapshot; export race with fence; cursor replay across tenant/principal.

### F simulated verdict
**ACCEPT WITH CONDITIONS** for the lifecycle direction only. F must choose exact object/cursor fields, index consistency model and release authority. No F Owner acceptance or implementation is evidenced.

## E — Compiler Producer Lifecycle role simulation

### Proposed E-owned contract
1. Stable WorkItemId, WorkGeneration, AttemptId, OutputId and PublicationId. Attempts change on retry; logical work and output identity do not.
2. E cannot schedule/execute D-covered work until it has durable DProducerAdmissionReceipt and valid I producer authorization reference.
3. Every output binds exact input revision IDs/digests, dependency closure digest, compiler build/config digest, schema version and deterministic request digest.
4. Output remains private/staged until D confirms dependency closure and current FenceGeneration, I confirms authorization and inventory validity, and the owning publication transaction commits.
5. Lost acknowledgement is resolved by querying the same PublicationId/OutputId and durable receipt. Never issue a new logical publication ID to escape UNKNOWN.
6. Queue, lease, worker replacement, retry, DLQ and replay all preserve work lineage; a restore must reconcile every queue state and staged output before E-local release.

### Required tests
Crash before schedule, after lease, during compile, after stage, after visibility commit before ACK; retry with same IDs; duplicate worker; DLQ replay after Forget; stale I permission; dependency added after compile; restore with queued and leased work.

### E simulated verdict
**ACCEPT WITH CONDITIONS** for producer lifecycle direction only. Durable queue, ledger, publication adapter and crash tests are not evidenced.

## G — Context and Derivative role simulation

### Proposed G-owned contract
1. Context, Task Semantic State, ContextVersion, Snapshot and Delta carry per-fragment provenance, not only one top-level source pointer.
2. A mixed context's effective D lineage is the union of every D-covered ancestor. A missing or unresolved fragment makes the aggregate MIXED_OR_UNKNOWN and suppresses it from governed serving.
3. Compaction preserves source lineage and cannot convert evidence into canonical truth. Summaries remain derivative and cannot erase ancestor references.
4. Validate D FenceGeneration and I PermissionEpoch/SealGeneration on assembly, compaction, reuse, snapshot creation, delta application, cache fill and delivery.
5. Snapshot/Delta application is conditional on exact base version, lineage digest and current generations. Stale snapshots never become valid merely because restore replay completed.
6. G-local release requires Context/TSS high-water reconciliation, lineage union verification, stale Snapshot/Delta invalidation and cache rebuild receipt.

### Required tests
Mixed source fragments; missing ancestor; compaction racing Forget; stale delta replay; snapshot restore from before fence; cache hit after revoke; late lineage after completion; TSS reconstruction from partial archive.

### G simulated verdict
**NEEDS REVISION** to Storage v1's broad derivative treatment until per-fragment provenance, monotonic lineage union and G-local release are explicit. No G Owner decision is evidenced.

## H — BMCP wire contract role simulation

### Proposed H-owned schema work
H consumes D/I/F/E/G semantic decisions and defines strict versioned wire representations. It must not decide their policy semantics.

Required named schemas (candidate names, subject to Owner agreement):
- ProducerInstanceRef
- ProducerAuthorizationRef
- DProducerAdmissionReceipt
- DDependencyClosureReceipt
- DForgetFenceReceipt
- TargetInventorySealRef
- ProducerClassificationReceipt
- ArchiveManifestReceipt
- RecallCursor
- CompilerPublicationReceipt
- ContextLineageManifest
- RestoreReadinessManifest
- OwnerRestoreReleaseReceipt
- StorageRestoreCommitReceipt

Each schema must define required/optional/null semantics, canonical encoding, digest preimage, issuer/audience/purpose, key ID and signature algorithm identifiers, expiry/revocation behavior, replay protection, unknown-critical-field behavior, downgrade rejection and compatibility policy. Authority-specific refs remain nominally typed; D sequence cannot be parsed as I epoch; Storage cannot mint D/I/F/E/G owner receipts.

### Required tests
Canonicalization vectors; duplicate JSON keys; unknown critical field; omitted vs null; invalid signature/audience/purpose; stale epoch; replay; cross-domain ref substitution; downgrade; generated SDK round trip; schema compatibility and malformed cursor.

### H simulated verdict
**NEEDS REVISION / BLOCKED ON OWNER SEMANTICS.** Do not freeze schema or SDK before D/I/F/E/G pin the exact fields. No H Owner acceptance or generated conformance is evidenced.

## Storage — persistence and restore atomicity role simulation

### Proposed Storage-owned realization
1. Store each Owner receipt as immutable evidence with issuer, schema digest, canonical payload digest, signature envelope, operation ID and source generation. Storage verifies authenticity/consistency but does not mint Owner semantics.
2. Separate durable control plane from restorable data plane. PITR/data snapshot rollback must never roll back D Fence, I inventory/revocation, permission epochs, producer registry, or owner release generations.
3. Restore sequence: restore data privately -> replay durable D/I control logs -> reconcile D dependency/Forget closure -> reconcile I inventory/seals/revocations -> reconcile F/E/G local state -> verify cross-owner join -> execute Storage serving CAS.
4. Serving CAS binds restore generation, data snapshot identity, D control high-water/generation, I InventoryEpoch/PermissionEpoch/SealGeneration, module release receipt digests and schema set digest. Any mismatch or concurrent generation advance aborts CAS.
5. Storage restore commit is not equivalent to owner release; owner releases are independent preconditions. On lost ACK, query same restore operation ID and same transaction identity; UNKNOWN fails closed.
6. Every write path is staged/non-serving until final CAS. No fallback to last-known-good owner receipt if its generation is stale.

### Required evidence
Selected DB/version/config; transaction/locking model; durable log ordering; exact crash-point table; restore from older snapshot while newer D/I control state exists; CAS races; same-operation recovery; backup/replica/DR source reconciliation; fail-closed tests.

### Storage simulated verdict
**NEEDS REVISION / OWNER DECISION REQUIRED.** v1 correctly recognizes independent authorities but cannot claim atomic restore safety until receipt schemas, replay order, serving CAS and real transaction behavior are pinned and tested. No DB product or production evidence is inferred.

## A — Principal Integration Architect role simulation

### Proposed integration decision criteria
A accepts only a complete exact-version bundle with:
- D and I independently signed semantic decisions and reciprocal join proof;
- F/E/G independent lifecycle decisions and local release receipts/contracts;
- H exact schema source, generated artifacts and compatibility/negative vectors;
- Storage exact persistence mapping, selected transaction profile and crash/recovery evidence;
- one canonical version-binding manifest with commit and blob SHA for every source;
- explicit unresolved exceptions and named Owner acceptance conditions.

A rejects:
- coordinator role simulations counted as Owner approval;
- Storage proposal treated as a substitute for Owner contracts;
- H schema invented before semantic Owners;
- Storage serving treated as module release;
- restore from stale data snapshot that rewinds D/I control state;
- any missing/unknown inventory or lineage silently treated as empty.

### Simulated integration verdict
**FREEZE NOT APPROVED.** The design direction is coherent if authority boundaries and independent generations are preserved, but Owner decisions, exact schema bindings, persistence profile and executable fault evidence remain absent. This is a coordinator simulation, not A's actual decision.

## Cross-role conflict resolution

1. Shared identity: `ProducerInstanceRef=(PolicyDomainId, ProducerDomainId, ProducerId, ProducerInstanceId, IdentityGeneration)`; I owns identity enrollment/generation, D references it in ProducerWork.
2. Independent generations: D FenceGeneration/admission sequence; I InventoryEpoch/SealGeneration/PermissionEpoch; F index/cursor generation; E work/publication generation; G ContextVersion/lineage generation; Storage RestoreGeneration. No cross-domain arithmetic or implicit coercion.
3. Global completion requires all authority-specific receipts, not a single Storage flag.
4. Unknown/mixed lineage and incomplete inventory fail closed.
5. Every module has an independent local release condition; A verifies binding and conflict resolution, not substitutes its own receipt for module receipts.

## Final simulated disposition

- D: PROPOSED; requires Owner decision.
- I: PROPOSED; requires Owner decision.
- F: ACCEPT WITH CONDITIONS (simulation only).
- E: ACCEPT WITH CONDITIONS (simulation only).
- G: NEEDS REVISION (simulation only).
- H: BLOCKED ON SEMANTIC OWNER FIELDS (simulation only).
- Storage: NEEDS REVISION / exact persistence evidence required (simulation only).
- A: FREEZE NOT APPROVED (simulation only).

Issue #20 remains OPEN. No Owner decision, implementation, CI pass, production conformance, external governance approval or merge is claimed.
