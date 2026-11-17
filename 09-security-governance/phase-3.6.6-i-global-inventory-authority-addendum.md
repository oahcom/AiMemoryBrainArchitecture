# Phase 3.6.6 — I Global Inventory Authority Addendum

- Owner: I — Security, Identity & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Status: **Global inventory semantic contract proposal; formal governance approval and runtime conformance OPEN**
- Base inventory contract Blob: `9100061fa986fb6676656169de3fcf9fc1c72664`
- Related: `global-forget-target-inventory-and-completion-evidence.md`, `phase-3.6.5-i36-governance-decision-proposal.md`.
- Authority boundary: I owns the global producer/recipient/backup/export inventory, inventory epoch, target seal, completeness proof and invalidation. D owns the per-operation canonical fence, work-item barrier and dependency closure.

## 1. Global inventory model

Global Inventory answers a different question from D's operation barrier:

- **I:** Have all domains, instances and custody locations capable of producing, receiving, retaining, copying, serving, exporting or restoring protected data been enumerated for this PolicyDomain and scope?
- **D:** Which concrete work items admitted before this Forget fence must terminalize, and which canonical derivatives belong to this operation?

Neither proof substitutes for the other. A complete D barrier cannot prove that an external recipient or backup is registered. A complete I registry cannot prove that a particular work item drained or a canonical derivative was suppressed.

## 2. Producer / Recipient Registry

I maintains one authenticated registry with typed entries and explicit roles. A single system may hold multiple role entries; role is not inferred from product name.

Required registry record:
- stable, non-recycled `InventoryEntryRef` and `InventoryEntryGeneration`;
- `PolicyDomainRef`, exact `ScopeRef` set and scope-binding fingerprint;
- authenticated `OwnerPrincipalRef`, `IssuerRef`, accountable organization/team and authority basis;
- authenticated service/instance identity, environment and jurisdiction;
- role set: `PRODUCER`, `TRANSFORMER`, `RECIPIENT`, `REPLICA`, `BACKUP_CUSTODIAN`, `EXPORTER`, `RESTORE_AUTHORITY`, `AUDIT_CUSTODIAN`;
- data classes and capability/action set, contract version and evidence profile;
- upstream/downstream lineage and onward-recipient relationships;
- storage/custody locations, replicas, caches, queues, backup sets, snapshots, WAL/archive and restore destinations as applicable;
- retention class, expiry/deletion mechanism, legal hold basis, residency/jurisdiction and subprocessors;
- lifecycle state: `ACTIVE`, `SUSPENDED`, `REVOKED`, `RETIRED`, `UNKNOWN`;
- first/last verified time, last inventory epoch, evidence references, verifier and next review deadline.

A registry entry is accepted only after issuer/owner authentication and exact binding to PolicyDomain, Scope, environment, instance and declared capability. Payload IDs, DNS names, tenant labels or self-asserted owner strings are claims, not identity proof.

### 2.1 Class coverage

At minimum, registry taxonomy MUST account for:
1. canonical stores and control ledgers;
2. ingress, producers, compilers, workers, queues, leases, retries, DLQ and replay;
3. indexes, embeddings, caches, Working Sets and rebuild systems;
4. Context snapshots/deltas, delivery intents, adapters, local buffers and reconnect paths;
5. replicas, snapshots, backups, WAL/archive, disaster-recovery and restore destinations;
6. exports, webhooks, sync, analytics, support/admin exports and human-accessible bundles;
7. model/inference providers, subprocessors and every onward recipient;
8. audit, observability, traces, metrics, tombstones and incident attachments;
9. unknown or newly discovered domains, explicitly represented as inventory gaps rather than omitted.

Each class has an accountable owner and required evidence profile. A class without authenticated owner or scope is `UNKNOWN` and blocks completeness.

## 3. ProducerDomainInventoryEpoch

`ProducerDomainInventoryEpoch` is an I-issued, monotonic, non-reusable epoch scoped to a `PolicyDomainRef` and a declared inventory boundary (scope/environment/jurisdiction). It versions the entire relevant registry snapshot, including membership, role, owner, scope, capability, custody, lineage, retention and evidence-profile changes.

Epoch rules:
- every add/remove, role change, owner/issuer change, scope/capability change, custody/recipient/backup change, retirement, revocation or evidence-profile change advances the epoch;
- epoch issuance is serialized by the authoritative I governance registry/sequencer and bound to the prior epoch, registry snapshot digest and change-set digest;
- an epoch is never reused, decremented or compared numerically with D FenceGeneration, PermissionEpoch from another PolicyDomain, COC index, F watermark, G ContextVersion or Storage LSN;
- retirement does not erase history or prove deletion; it changes current membership only with durable disposition and retained historical evidence;
- an unavailable or forked epoch authority yields `UNKNOWN` and prevents a new seal.

A Forget evaluation MUST name the exact epoch and inventory boundary it relies on.

## 4. Target Inventory Seal

A `TargetInventorySeal` is a per-Forget, immutable commitment over the global target population derived from an authenticated ProducerDomainInventoryEpoch and the operation's exact PolicyDomain/Scope/target lineage.

The seal binds:
- `ForgetOperationRef`, normalized request digest and D fence/target-set reference;
- `PolicyDomainRef`, exact ScopeRefs, jurisdiction and declared inventory boundary;
- `ProducerDomainInventoryEpoch`, registry snapshot digest and registry change-set digest;
- all included InventoryEntryRefs, role/instance generations and their target-enumeration manifests;
- per-entry target counts/digests, evidence profiles, retention/backup/recipient obligations and onward-recipient closure;
- explicit `NotApplicable` determinations with positive absence evidence and independent verifier;
- all unresolved/unknown/unsupported entries (which prevent a complete seal);
- canonicalization/schema version, signer identity, signature/key version, issue time and audit reference.

The seal is not a list supplied by the requester. It is generated from the authoritative registry and authenticated per-entry enumeration responses. The target set is committed as a deterministic manifest/Merkle root (or equivalent collision-resistant canonical commitment), with retrievable member-level manifests. A root without member manifests is insufficient for audit or reconciliation.

A seal may be created in a **PROVISIONAL** state for analysis, but only a fully reconciled seal can be `SEALED_COMPLETE`. Provisional seals cannot authorize completion or exceptions.

## 5. Completeness Proof

I's `GlobalInventoryCompletenessProof` MUST establish all of the following for the exact seal and epoch:
1. registry snapshot is authenticated, current and non-forked;
2. every required domain class is represented or has independently verified `NotApplicable` evidence;
3. every registry entry has authenticated owner, instance, exact scope/capability and a current enumeration response;
4. each producer/transformer enumerated all relevant outputs, pending work, retry/replay paths and derivative destinations, reconciled with D's operation-specific dependency closure;
5. each recipient/exporter enumerated copies, onward recipients, local buffers and deletion/withdrawal evidence obligations;
6. each replica/backup custodian enumerated backup sets, snapshots, WAL/archive segments, retention deadlines, legal holds and restore destinations;
7. every target/entry is accounted for with owner-specific evidence state; no missing member is hidden by aggregate count;
8. every `NotApplicable` is supported by positive, scope-bound evidence and independent review;
9. all external/unknown/unreachable/unsupported entries remain explicit and block complete status unless a valid I-approved policy exception applies;
10. seal digest, manifests, epoch, verification times and evidence references are cryptographically bound and audit-retrievable.

The proof is **COMPLETE** only when no mandatory member is `UNKNOWN`, `PENDING`, `FAILED`, `UNREACHABLE`, `UNAUTHENTICATED` or otherwise unresolved, except a narrowly scoped, effective, authorized policy exception explicitly permitted by the governing policy. A non-response is Unknown, never success. A request receipt is not a deletion receipt. A registry count is not a completeness proof.

## 6. Invalidation and resealing

Any change that could alter the target universe or its evidence validity invalidates the current completeness proof and, where membership/coverage is affected, the seal for completion evaluation. Triggers include:
- new, reactivated or newly discovered producer, transformer, recipient, subprocessor, export, replica, backup or restore authority;
- changed owner, issuer, instance identity, role, scope, environment, jurisdiction, capability or onward-recipient relationship;
- changed target enumeration, lineage, copy/backup manifest, retention, legal hold or deletion capability;
- inventory epoch advance, registry fork/rollback, signature/key revocation or expired authentication/evidence;
- late owner response, newly discovered target, post-completion derivative, previously hidden export or restore resurrection;
- D barrier reopen, changed D dependency-closure digest/high-water or a mismatch between D canonical lineage and I global members;
- restore/recovery that cannot establish the current I epoch and D fence/control high-water.

Invalidation is append-only: preserve prior seal/proof and mark it `STALE` or `REVOKED_FOR_EVALUATION`, record trigger, old/new epoch, affected entries, detection time and responsible verifier, then create a new epoch/snapshot and reseal. Invalidation never erases the Forget fence or retroactively changes a historical proof's meaning.

A post-completion discovery reopens Global Forget evaluation immediately. The historical completion record remains immutable but is marked superseded for current compliance posture; the new target must be processed under the still-effective Forget obligation. No automatic success inheritance is permitted.

## 7. I/D handshake and ordering

For each Forget operation:
1. D resolves canonical request coverage and installs its durable fence with D high-water and barrier membership.
2. I captures the authoritative global registry epoch and obtains authenticated per-entry enumeration manifests for the same PolicyDomain/Scope/operation.
3. I reconciles its global target manifest with D's canonical dependency closure and each owner-specific inventory; mismatches remain open.
4. I creates a provisional TargetInventorySeal, verifies completeness and obtains all required target-specific owner evidence.
5. Any registry/lineage/barrier/restore change invalidates the affected proof and triggers reseal/reconciliation.
6. Only an authorized I governance decision evaluates the full completion evidence vector and may declare Global Forget complete.

The I seal does not close D's barrier. D barrier completion does not seal I's inventory. I cannot infer a D terminal receipt; D cannot mint an I inventory epoch or global completeness proof.

## 8. Governance and evidence boundary

This addendum defines semantics and evidence structure only. It does not approve I36-GOV-01..10, trusted issuers, delegation, cross-scope/environment grants, backup retention exceptions, external-recipient exceptions, legal holds or physical-erasure policy. Such approval requires the authorized governance body, exact policy hash/version, approver Principal/Issuer and authority basis, independent review where required, scope/jurisdiction, effective time, expiry/review and revocation conditions.

Technical Owner acceptance, repository commits, model tests and user instructions to continue work are not formal governance approval. Physical erasure requires separate custodian/media/key/copy evidence and cannot be inferred from inventory completeness or logical suppression.

## 9. Conformance boundary

The registry, epoch sequencer, authenticated enumeration protocol, target seal signer, completeness verifier, invalidation/reseal worker, external recipient integration, backup/restore catalog integration and production audit trail remain **NOT IMPLEMENTED / NOT VERIFIED** unless independently evidenced by exact artifacts and runs. This proposal does not authorize Production Activation or Global Forget completion.
