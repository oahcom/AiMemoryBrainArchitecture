# Archive Producer Classification, Forget Fence, Inventory & Restore Atomicity — Storage Integration Realization v1

- Owner: Storage / Consistency
- Date: 2026-11-17
- Status: **STORAGE INTEGRATION PROPOSAL — OWNER ACCEPTANCE REQUIRED**
- Phase: Architecture design; no production implementation or activation implied.
- Scope: F Archive producer lifecycle, D Forget Fence/barrier, I global producer/recipient inventory, and Storage restore/PITR atomicity.
- This document consumes, but does not replace, D's Forget Fence contract, I's Global Forget inventory policy, F's Archive/Recall contract, G's Context lineage contract, E's compiler publication contract, or A's integration decision.

## 1. Decision summary

The four topics are one joined safety problem but are not one authority:

1. **Producer classification** decides which owner-local controls apply to an ingress, transformation, copy, derivative, or restore path.
2. **D Forget Fence** decides canonical suppression and the concrete D producer-work barrier for one Forget operation.
3. **I Producer Domain Inventory** decides whether the global producer/recipient/backup/restore universe is closed and whether a Global Forget evaluation may be considered complete.
4. **Storage restore atomicity** ensures data snapshots cannot roll back D/I control state and cannot become queryable before independent control replay and owner-local release.

The architecture has two inventory layers and multiple independent gates. They MUST NOT be collapsed into a single producer list, integer epoch, global cursor, or Storage-owned decision.

**Safety rule:** if producer class, authenticated producer identity, scope, lineage coverage, recipient route, inventory membership, D fence state, I authorization, or restore control prefix is unknown or unverifiable, the affected bytes remain private/quarantined and the operation remains UNKNOWN/PENDING.

## 2. Authority map

| Concern | Authority | Storage responsibility | Prohibited substitution |
|---|---|---|---|
| Producer class semantics and per-work admission | D for D-covered work; F/E/G for their local execution roles | Persist exact references/receipts and serialize assigned operations | Storage must not decide D lineage eligibility |
| Producer/recipient identity and global registration | I | Verify and retain authenticated evidence references | Payload producer ID or F catalog row is not I registration |
| Archive bytes, revisions, manifests, locators, Recall sessions/cursors/receipts/cache | F | Durable immutable bytes, WAL/backup integrity, quarantine and recovery | ArchiveLocator/ReadReceipt is not authorization or canonical Memory |
| Canonical ForgetFence, generation, work high-water, dependency inventory and barrier result | D | Provide linearizable persistence/atomicity primitive and durable readback | Storage tombstone/cache invalidation is not D fence |
| Context refs, ContextVersion, compaction, fidelity, lineage/loss and delivery intent | G | Preserve immutable versions and restore quarantine | G ContextVersion is not ForgetFence or global inventory epoch |
| Compiler work and canonical-derived publication | E, subject to D/I | Keep prepared/staged bytes hidden; atomically persist visibility record | E local success or object existence is not publication |
| PermissionEpoch, revocation, retention, inventory epoch/seal and global completion | I | Validate authoritative proof at assigned gates; preserve evidence | Storage-local cached policy is not I authority |
| Restore serving gate and durable publication visibility | Storage for its own data plane; each owner for its local gate | Atomic restore generation/serving state, no-visible-before-release | Storage cannot release D/I/F/G owner-local gates |

## 3. Archive Producer Classification

### 3.1 Classification is mandatory before protected processing

Every F Archive producer, importer, transformer, cache filler, indexer, exporter, recipient, backup writer, restore worker and derived-artifact producer MUST be represented by an authenticated producer identity and a versioned producer-class registration before it processes protected bytes.

A class is not an instance. A target is not a producer. A producer's self-declared ID is only a claim.

The minimum classification record is:

- `ProducerClassRef`, class contract version and owner;
- `ProducerIdentityRef`, authenticated issuer/Principal and instance or declared singleton identity;
- exact `ScopeRef` set and scope-binding digest;
- capability set/version: create, read, transform, cache, index, export, deliver, backup, restore, delete/crypto-erase;
- lineage role: source, transformer, derivative, recipient, replica, backup, restore destination, or mixed;
- data-domain classification: Archive-only transient, D-covered canonical lineage, mixed, external copy, or control/evidence-only;
- source/ancestor references and immutable revision identifiers where applicable;
- declared recipient, onward-recipient and backup/restore routes;
- retention/evidence profile and jurisdiction;
- lifecycle state: ENABLED, DISABLED, REVOKED, QUARANTINED, UNKNOWN;
- I inventory epoch/seal reference and D registry/version/work receipt references where applicable.

Missing fields are not defaulted to NotApplicable. Unknown issuer, instance, scope, lineage role or recipient route yields DENY/QUARANTINE.

### 3.2 Normative classification matrix

| Class family | Example producer/target | D coverage | I inventory | Admission / visibility rule |
|---|---|---|---|---|
| F archive capture — Archive-only | New transient observation with no D-covered canonical ancestor | Not automatically a D canonical work item; F local suppression still applies | Mandatory I Producer/Recipient Domain entry | I authorization + F class enabled + immutable manifest; no canonical Memory implication |
| F archive capture — canonical-linked | Observation contains/derives from D-covered Memory or protected lineage | D ProducerWork registration before dereference/processing; complete source lineage | Mandatory I entry plus D class/work mapping | D fence checked at admission and final F publication/disclosure boundary |
| F archive transformer / summarizer | Redaction, extraction, embedding, summary, compaction input or transformed object | D-covered if any source ancestor is D-covered; transitive lineage cannot be dropped | Mandatory I entry | New immutable revision; dependency receipt before visibility; final D/I gate |
| F cache / Working Set / retrieval index | Cache fill, index build, materialized retrieval view | D-covered whenever any indexed source/ancestor is D-covered | Mandatory I entry, including partition/replica identity | F-local cache suppression plus D fence and I current permission on fill and hit; stale fill cannot publish |
| G Context derivative | ContextObservationReference, TSS, summary, ContextVersion, snapshot/delta | D-covered if it includes or derives from D-covered canonical lineage | Mandatory I entry for producer/recipient paths | D transitive lineage and G CAS/currentness; Context ref is not bearer authorization |
| E canonical compiler | Compiler worker, queue, retry, DLQ, staged output, derived artifact | D producer-work ledger and dependency inventory mandatory | Mandatory I entry | Stable ProducerWorkItemId; D/E/Storage final visibility serialization |
| Export / external recipient | Webhook, sync, analytics, inference/model provider, human/admin export | D-covered if bytes contain a D-covered target/derivative; recipient is a downstream lineage node | Mandatory I recipient entry and onward-copy route | Authenticated recipient and current permission; evidence/ACK does not prove deletion or onward-copy closure |
| Backup / replica / WAL / snapshot | Physical backup, object version, WAL archive, DR replica | D control lineage must be replayed independently; data copy is not authoritative fence source | Mandatory I target entry with backup/restore relationships | Restore quarantine; backup retention/erasure state remains I-governed |
| Restore destination / rebuild worker | New cluster, restored DB, re-index/rebuild, replay worker | D fence and all source ancestors re-applied before queryability | New or revalidated I inventory entry; destination and operator authenticated | New database incarnation where applicable; restore fence until all proofs validate |
| Control/evidence-only producer | Audit record, receipt, manifest or non-payload control event | D scope only if it carries protected target/lineage or changes a D barrier | I inventory according to policy taxonomy | Evidence cannot be reinterpreted as payload, authorization or completion |

### 3.3 The classification decision function

For each operation, resolve the following independently:

1. Authenticate producer instance and issuer under I.
2. Resolve class, capabilities, scope and current I inventory registration/seal.
3. Resolve source lineage and whether any source/ancestor is D-covered.
4. If D-covered or mixed, obtain D ProducerWork registration before protected execution and register every dependency before visibility.
5. Resolve recipient, replica, backup and restore destinations; unknown downstream routes block the operation.
6. Apply owner-local F/G/E gates and final D/I currentness checks at the boundary that discloses or publishes bytes.

Archive-only transient observations are not automatically canonical Memory and are not automatically D producer targets. However, an object cannot be labelled Archive-only merely because its canonical MemoryRef has not yet been minted. EventRef/opaque lineage must be retained and later linked to exact canonical refs/revisions before dependency registration or publication. Mixed/unknown lineage is quarantined until resolved.

## 4. Two inventory layers — separate authority and closure

### 4.1 I global closed-world inventory

I owns `ProducerDomainInventoryEpoch`, authenticated producer/recipient registration, target taxonomy, inventory digest, TargetInventorySeal, retention/exception policy and Global Forget evaluation.

The sealed universe must include every applicable:
- producer class and authenticated instance;
- F Archive object store, metadata catalog, revision, locator namespace, cache, Working Set and index partition;
- G Context materialization, snapshot, delta, delivery intent and local/remote recipient;
- E queues, workers, retries, leases, DLQ, staged output and derived artifacts;
- H Adapter managed regions, local buffers, offline queues and onward recipients;
- C/provider/external export and downstream recipient;
- backup catalog, replica, snapshot, WAL/archive log, DR copy and restore destination;
- newly discovered or late-created derivative/copy route.

A TargetInventorySeal binds the I registry authority, epoch, canonical digest, scope, taxonomy version, signer/verifier and audit proof. Relevant class/capability/scope/owner/issuer/recipient/backup/evidence-contract changes invalidate the prior seal and require resealing. Empty categories require positive absence evidence plus independent review; no silent NotApplicable.

### 4.2 D per-Forget concrete work inventory

D owns `ProducerRegistryVersion`, `ProducerRegistrationHighWater`, `ForgetFenceGeneration`, per-operation `WorkItemBarrier`, dependency inventory and lineage reconciliation.

The D barrier enumerates concrete work items admitted under the captured D registration cutoff. It does not enumerate all global domains and cannot substitute for I's inventory epoch/seal.

### 4.3 Required join proof

For every D-covered class/instance in the I sealed universe, there must be a resolvable mapping to D's class/registry and applicable work ledger. The mapping proof includes exact class identity/version, owner, scope, lineage role, I epoch/seal, D registry version, and the evidence that D coverage is required or positively not applicable.

A mismatch between I inventory and D registration is a registry gap, not a harmless reporting difference. I epoch change during a Forget invalidates the prior global completion evaluation; D captures its own per-operation work high-water independently. No arithmetic comparison between I epoch and D cursor/generation is valid.

## 5. Forget Fence and Archive atomicity

### 5.1 Mandatory operation ordering

For D-covered or mixed lineage:

1. Authenticate producer, scope and I authorization.
2. Resolve current I inventory registration and relevant seal.
3. D durably registers `ProducerWorkItemId` and returns the stable RegistrationReceipt before queue, lease, dereference, execution or retry.
4. Producer captures immutable source revision/ancestor manifest and stable operation digest.
5. D registers complete direct/transitive dependencies before publication.
6. F/E/G stages immutable bytes privately; no locator, cache entry, index row, Context reference or outbox projection makes them queryable.
7. At final publication/disclosure, revalidate current I PermissionEpoch and D ForgetFence/ancestor lineage at one serialization boundary with the visibility transition.
8. Commit visibility marker and PublicationReceipt atomically. If any predicate is unknown or stale, retain private/quarantined state.
9. D terminalizes work only after all attempts, retries, DLQ/replay paths and outputs have authoritative terminal disposition.

For Archive-only transient data, D registration is not invented; F still enforces I permission, F-local suppression, immutable manifests and retention policy. If lineage changes or a D-covered ancestor is discovered later, the object and every derivative are reclassified, quarantined, linked to D lineage and reconciled against the active fence before any further disclosure.

### 5.2 Fence/register/publish race

Only two successful orders are legal:

- Registration/publication linearizes before fence: its exact work/dependency/publication evidence is included in the D captured high-water/barrier and reconciled.
- Fence linearizes first: later ordinary admission/publication for covered lineage is rejected or quarantined.

An ambiguous transaction, lost ACK, replica lag or crash is UNKNOWN. Resolve by the same stable operation/work IDs and authoritative ledger readback. Never allocate a replacement ID to escape the ambiguity.

### 5.3 Required atomic persistence boundary

For one Canonical Memory authority, the logical atomic unit is:

- D producer-work admission/registration and immutable request digest;
- D fence installation and captured registration high-water;
- complete dependency edge set and lineage digest;
- final current D fence/ancestor decision;
- I authorization/PermissionEpoch decision reference as verified under I's authority;
- immutable artifact/version identity;
- Storage visibility marker / VisibilityPointer;
- PublicationReceipt and owner outcome;
- transactional outbox/projection identity.

Preferred realization is one ACID transaction when all authoritative state shares one database/consistency boundary. If not, a durable hidden-prepare protocol is required. Prepare never makes bytes visible. Final commit must serialize with fence installation and consume a one-time decision bound to the exact participant tuple. Recovery must preserve hidden state until the exact commit proof is authoritative. Check-then-write, independently committed visibility, reusable approval token or cache-only fence check is invalid.

Storage supplies physical transaction and recovery semantics only. D defines the fence predicate; I defines permission and revocation semantics; E/F/G define their owner-local operation facts. The actual database/transaction selection remains an explicit architecture/engineering decision, not assumed here.

## 6. Restore/PITR atomicity and anti-resurrection

### 6.1 Restore is quarantine-only

Every restore, PITR, clone, replica promotion, rebuild or import creates a new `RestoreOperationId` and begins in `RESTORE_FENCED`. Restored data is not queryable, indexable, deliverable, cacheable or available to Recall/Context until the release protocol completes.

### 6.2 Independent control sources

A data snapshot MUST NOT be the sole source for the controls that authorize its own release. Before release, verify independently:

- snapshot identity, manifest digest, exact WAL/archive segment coverage and continuous recovery prefix to the selected target;
- Storage database/authority identity and new incarnation rules for clone/restore/re-provision;
- D's latest authoritative ForgetFence generation/cursor, producer-registration high-water, dependency/lineage state and unresolved barrier manifest;
- I's latest PermissionEpoch/revocation state, ProducerDomainInventoryEpoch, TargetInventorySeal and invalidation/reopen events;
- authenticated producer/recipient/backup/restore destination inventory, including newly discovered routes;
- F cache, Working Set, index, RecallSession, ReadCursor and ReadReceipt invalidation/rebuild requirements;
- G Context refs, snapshots, deltas, deliveries and current-use suppression/reconciliation requirements;
- E queue/lease/DLQ/replay and staged-output reconciliation;
- H/C offline queue, Adapter and provider side-effect recovery evidence where in scope.

Missing, stale, corrupt, incomplete or unverifiable evidence keeps the restore fenced. No wall-clock timestamp or local snapshot cursor can substitute for an authoritative owner position.

### 6.3 Restore release protocol

1. **Fence:** Storage creates a durable restore generation and blocks all reader, Recall, cache-hit/fill, index, Context, delivery, export and publication paths for the restored dataset.
2. **Integrity:** verify snapshot and WAL continuity. Missing/corrupt/incomplete exact target segment => remain RESTORE_FENCED; no writable/serving authority.
3. **Control replay:** independently read and replay D and I control ledgers beyond the restored data cutoff. Verify monotonic anchors against independently retained checkpoints.
4. **Inventory reconcile:** reconcile all producers, recipients, replicas, backup paths and restore destinations. New/unknown entries invalidate prior seal and remain UNKNOWN/PENDING.
5. **Participant reconcile:** resolve every pre-cutoff producer work item, prepared participant, pending publication, COC cutoff batch, I/D local gate, queue/lease/DLQ/replay and external side-effect ambiguity.
6. **Local owner release:** D, I, F, G, E, H and C each release only their own local gate with a signed, idempotent receipt bound to the exact restore ID/generation, source snapshot/WAL digest, their own typed high-water/epoch, and reconciliation manifest digest. Storage cannot manufacture these receipts.
7. **Readiness manifest:** assemble immutable `RestoreReadinessManifest` with exact component receipts, inventory seal, D fence/barrier proof, participant reconciliation root, WAL proof, unresolved count = 0 for mandatory serving scope, and explicit scope of any separately quarantined partitions.
8. **Atomic serving release:** Storage performs one compare-and-swap/transaction from `RESTORE_FENCED` to `SERVING` bound to the exact manifest digest and restore generation. The serving gate and release receipt commit together. A stale generation, missing receipt, changed control high-water or new inventory epoch rejects the CAS.
9. **Post-release watch:** any late derivative, inventory epoch change, fence advance, revoked authority, restore mismatch or newly discovered copy immediately closes the affected serving gate and reopens reconciliation; no historical readiness manifest is silently reused.

This is a barrier protocol, not a claim that all owner databases share one distributed ACID transaction. Each owner retains its own authority and monotonic gate. The Storage serving CAS is the final data-plane gate, not a substitute for those owner releases.

### 6.4 Atomicity and rollback invariants

- Data restore may move data state backward; D/I control state and anti-rollback anchors must not move backward.
- Restoring an old snapshot cannot resurrect a forgotten target, stale permission, consumed authorization, revoked key, old inventory seal, cache cursor or pre-fence publication.
- Visibility is derived only from committed publication records plus current D/I validation; object existence or restored catalog rows never imply visibility.
- If WAL target or control prefix cannot be proved exact, remain RESTORE_FENCED.
- No operator force-release, timeout release, heuristic participant resolution or "best effort" serving.

## 7. Required immutable evidence types

The following are proposed cross-owner evidence contracts; exact field-level wire schemas remain H/I-owned:

- `ProducerClassificationReceipt`: class/version, authenticated producer identity, scope digest, capability set/version, lineage role, data-domain classification, I inventory epoch/seal, D registry mapping where applicable, issuer/key evidence and audit reference.
- `ArchiveManifestReceipt`: immutable object/revision/hash, source revision/EventRef, lineage digest, retention class, producer receipt, storage durability reference and publication disposition.
- `DProducerWorkRegistrationReceipt`: D work ID, class/registry version, request digest, scope, captured source/ancestor refs, registration sequence/high-water and fence observation.
- `DependencyRegistrationReceipt`: exact artifact/version, full direct/transitive parent set, source revisions, dependency digest and D inventory position.
- `TargetInventorySeal`: I registry epoch/digest, taxonomy version, full target set, completeness proof, issuer/signature and validity/invalidation state.
- `RestoreReadinessManifest`: restore ID/generation, snapshot/WAL digest/prefix, independent D/I control high-waters, inventory seal, participant reconciliation root, owner-local release receipts and serving scope.
- `RestoreReleaseReceipt`: exact readiness-manifest digest and Storage serving CAS transaction identity.

Receipts prove only their issuer's fact. No one receipt proves global Forget, authorization for a future operation, physical erasure, provider success, G Applied or another owner's gate release.

## 8. Mandatory negative/fault matrix

| ID | Fault/race | Required outcome |
|---|---|---|
| APC-01 | Unknown producer class/issuer/instance/scope | DENY/QUARANTINE before protected processing |
| APC-02 | Archive-only claimed but EventRef later resolves to D-covered lineage | Reclassify, quarantine, link lineage, reconcile before further disclosure |
| APC-03 | D-covered capture races Forget fence | Exactly one serialization order; pre-fence included or fence-first rejected |
| APC-04 | Producer class/capability/recipient changes after seal | I seal invalidated; no global completion |
| APC-05 | Unknown onward recipient/export route | UNKNOWN/PENDING; no success or NotApplicable |
| FNC-01 | Fence commits before registration | No ordinary work admission |
| FNC-02 | Registration commits before fence | Work included in immutable D high-water/barrier |
| FNC-03 | Dependency set partial or receipt lost | Private/quarantined; no visibility |
| FNC-04 | Fence advances after staging/before final commit | Final commit rejected |
| FNC-05 | Pre-fence cache fill finishes after fence | Fill rejected; stale hit denied |
| FNC-06 | Recall cursor resumes after fence/permission change | Cursor invalidated; no subsequent page or final handoff |
| RST-01 | Restore snapshot predates D fence | Remain RESTORE_FENCED until independent D replay |
| RST-02 | Restore snapshot predates I revocation/inventory seal | Remain RESTORE_FENCED; reauthorize and reseal |
| RST-03 | WAL gap/corrupt/incomplete exact segment | No writable/serving authority |
| RST-04 | Old cache/index/Context snapshot reintroduced | Suppress, invalidate and rebuild before serving |
| RST-05 | Owner gate release receipt missing/stale/wrong generation | Storage serving CAS rejected |
| RST-06 | Crash after all owner releases but before Storage serving CAS | Remain fenced; idempotently retry same manifest |
| RST-07 | Crash after serving CAS but before ACK | Lookup same RestoreOperationId returns committed receipt; never create new generation |
| RST-08 | Late target/recipient/derivative after release | Close affected gate; invalidate seal/readiness and reopen reconciliation |
| RST-09 | Restore clone reuses old DB incarnation | Reject unless explicit authorized migration proves continuity |
| RST-10 | Restore control prefix/anti-rollback anchor unavailable | RESTORE_FENCED; no heuristic release |

## 9. Acceptance and evidence boundaries

### Owner decisions required

- **D:** accept the classification-to-D-coverage mapping, EventRef handling, producer-work admission/fence ordering, complete dependency registration and final visibility predicate.
- **I:** accept producer/recipient class taxonomy, identity fields, inventory/seal lifecycle, unknown/NotApplicable rules, backup/restore coverage and Global Forget evidence mapping.
- **F:** accept Archive producer classes, capture/read/cache/index/restore enforcement and F-local release semantics.
- **E:** accept compiler/replay/queue/lease/DLQ mapping and publication participation.
- **G:** accept Context derivative/lineage/restore invalidation mapping.
- **H:** define strict wire schemas for classification and restore receipts; unknown-critical and downgrade behavior.
- **A:** integrate exact owner decisions and decide whether the common contract is ready for a freeze gate.
- **Storage:** own physical persistence, restore quarantine, WAL continuity and atomic serving release; no owner authority is overridden.

### Not claimed

- This proposal does not claim all owners have accepted it.
- It does not claim I governance approval, Global Forget completion, physical erasure or multi-policy-domain atomicity.
- It does not claim integrated executable Forget/Archive/Restore tests passed.
- PostgreSQL 18.7 capability CI is bounded engine evidence only; it is not proof of deployed F/D/I/E/G integration.
- No production database, topology, deployment, operator or runtime is designated by this document.

**Storage disposition:** architecture integration proposal complete for review; cross-owner acceptance and end-to-end conformance remain OPEN.
