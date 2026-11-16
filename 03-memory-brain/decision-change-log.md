# Session D — Phase 3 Decision / Change Log

- **Branch:** `session-d-memory-brain-2026-11-16`
- **Base commit:** `9dc08c63f6912320e290a963c634748ec44a81c8`
- **Scope:** D-owned files under `03-memory-brain/` only.
- **Date:** 2026-11-16
- **Delivery status:** candidate architecture remediation; no merge, contract freeze or implementation sign-off.

## 1. Decisions

| ID | Status | Decision |
|---|---|---|
| D-REV-P1-001 | **DECIDED — D-local semantic closure** | Memory lifecycle is Candidate/Consolidated/Active/Superseded/Archived/Forgotten only. Forgetting is not a Memory state. ForgetOperation/fence/suppression is a separate durable workflow. Forgotten lifecycle transition is appended only after I supplies the applicable governance criterion. |
| D-REV-P1-002 | **DECIDED — D domain cursor semantics** | One global CanonicalCommitCursor per Brain authority; AggregateRevision per aggregate; LifecycleEventCursor per Memory; IndexWatermark per F index partition; ForgetFenceCursor per ForgetOperation/target set. Typed cursors are not interchangeable. Transaction visibility, gap, replay and resume rules are specified. |
| D-REV-P1-003 | **DECIDED — D canonical barrier contract; integration OPEN** | Durable ForgetOperation ID, monotonic fence generation, closed producer registry/barrier, register-before-visible dependency inventory, final publish fence check, target acknowledgements and canonical suppression proof specified. E/F/G/H execution and I global completion policy remain open. |
| INT-P0-01 | **ADR-BLOCKED** | Main has no approved B Fact/Claim ADR file. Claim/ClaimRevision/ConflictSet remain candidate sketches; no schema freeze. |
| INT-P0-02 | **OPEN — I/H/B and module enforcement** | D Scope-bearing canonical references remain domain inputs only. Principal/ActorRef/permission epoch and end-to-end enforcement are not decided by D. |
| INT-P0-03 | **OPEN — cross-module/global** | D closes canonical fence/barrier semantics only. I owns policy and global completion; E/F/G/H own execution/acknowledgement. No physical erasure proof. |
| INT-P1-01 | **G-OWNED** | D emits exact MemoryVersion refs and canonical invalidation signals; no ContextVersion or ChangeSet authority. |
| INT-P1-03 | **OPEN — B/H/I** | ActorRef issuer/authentication/delegation remains upstream; D consumes typed ActorRef only. |
| INT-P1-06 | **PARTIAL / OPEN** | D cursor distinctions specified; E/F/G consumer conformance, provenance cycle policy and vocabulary/schema compatibility remain open. |
| DM-009 | **DECIDED — D migration semantics** | Entity Merge/Split and Relation migration are append-only; historical refs remain immutable; current mapping is explicit, authorized and auditable. |

## 2. Changed paths

- Updated: `03-memory-brain/memory-brain-overview.md`
- Updated: `03-memory-brain/canonical-memory-store.md`
- Updated: `03-memory-brain/memory-versioning.md`
- Updated: `03-memory-brain/memory-lifecycle-manager.md`
- Updated: `03-memory-brain/entity-and-relationship-manager.md`
- Added: `03-memory-brain/forget-fence-and-completion-contract.md`
- Added: `03-memory-brain/commit-cursor-semantics.md`
- Added: `03-memory-brain/decision-change-log.md`

## 3. Interface impact matrix

| Producer → Consumer | D-owned contract output | Consumer-owned obligation / boundary |
|---|---|---|
| D → E | ForgetOperation ID, fence cursor, dependency refs, producer barrier and canonical commit cursor | E registers every queue/lease/retry/DLQ/replay work item; checks fence before canonical publication; emits derivative/terminal acknowledgements |
| D → F | Exact canonical refs/revisions, commit cursor, lifecycle signals, fence cursor | F enforces candidate/in-flight/cache/Working Set/index-rebuild suppression; owns IndexWatermark |
| D → G | Exact MemoryVersion refs, lifecycle/migration invalidation and fence | G owns ContextVersion/ChangeSet/snapshot/delta/delivery reconciliation and blocks stale Applied state |
| D → H | Opaque target refs, fence status and required target acknowledgement semantics | H owns BMCP wire, Adapter managed-region clear, offline reconnect and application acknowledgement |
| D ↔ I | Canonical Forget inventory, fence, target progress and domain proof reference | I owns authorization, Principal/revocation, retention, backup/external-copy, residual exception approval, global completion and physical erasure |
| D ↔ B | Canonical reference/revision mechanics after approved ADR | B/Governance own Fact/Claim ADR; D does not freeze Claim/ClaimRevision/ConflictSet |

## 4. Required acceptance evidence (not yet executed)

- Lifecycle vocabulary scan finds no Memory lifecycle state “Forgetting”; ForgetOperation phases appear only in operation model.
- Atomic commit tests prove whole-transaction visibility and no cursor/revision consumption on abort.
- Replay tests prove gap blocks contiguous watermark and snapshot bootstrap is deterministic.
- Race tests cover E queued/leased/retry/DLQ/replay, F in-flight/cache/rebuild, G snapshot/delta/Prepared/Delivered/late Applied, H offline reconnect, and concurrent canonical write.
- Producer registration gap, expired lease, unknown target and missing acknowledgement all block barrier closure.
- Entity merge/split correction and Relation migration preserve historical refs and rebuild deterministic current projections.
- D-only suppression proof is not reported as global Forget completion or physical erasure.

## 5. Interface dependencies and unresolved items

- **E:** Phase 3 baseline branch has the five original Compiler documents; the task-pack's dedicated Forget-fence/derived-registration contract is not present in the inspected E branch tree. E must deliver its own enforcement contract.
- **F:** Phase 3 baseline branch has the five original Runtime documents; the task-pack's dedicated cursor/freshness/Forget-enforcement contract is not present in the inspected F branch tree. F must deliver its own enforcement contract.
- **G:** six Context documents are present. Existing reconciliation/versioning documents already describe tombstones, offline Adapter as unknown, stale delivery and I-owned completion. G still owns its detailed remediation outputs and cannot be replaced by D.
- **H/I:** no H BMCP/protocol package or I Security/Governance package exists in the inspected main tree. Their contracts and approvals are missing; do not assume acknowledgement or global completion semantics are approved.
- **B:** no `02-domain-model/adr/ADR-001-fact-claim-canonical-model.md` and no `02-domain-model/adr/` directory exists on inspected main. INT-P0-01 remains ADR-BLOCKED.
- **Storage/Consistency:** atomic transaction/outbox implementation, durable snapshot retention and crash-recovery behavior require engineering validation.
- **I:** global completion criteria for offline adapters, immutable backups, external recipients and physical erasure remain I-owned OPEN items.

## 6. Ownership non-regression

This delivery does not define G ContextVersion, H BMCP wire/Adapter state machine, I global authorization/revocation policy, I retention/backup/external-copy policy or physical-erasure proof. It does not modify governance, A/B/C, E/F/G/H/I files or other branches. No implementation, security, performance or global Forget sign-off is asserted.


## 7. Phase 3.5 — Forget Fence Atomicity & Producer Admission

- **Issue:** CR-P1-01 / D-REV-P1-003.
- **Status:** D operation semantics DECIDED; cross-module implementation and conformance OPEN.
- **Reviewed D branch HEAD before this change:** 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6.
- **Reviewed E branch HEAD:** 3dea6096eefa6779eb12e4e788bcf9429d2a3f83.
- **Reviewed cross-module review:** reviews/integration/phase-3-defghi-cross-module-contract-review.md, commit 8a6414158c9c056c1638222534e1993d1bbc99d2.
- **Reviewed remediation task pack:** commit 3cae375aadfc2a8b2facce5cb006ff1e55c2dfe1.

### 7.1 Decisions

| ID | Status | Decision |
|---|---|---|
| D35-01 | DECIDED — D semantic contract | RegisterProducerClass and RegisterProducerWork are distinct; unknown/disabled classes fail closed; registration has stable idempotent identity and durable receipt. |
| D35-02 | DECIDED — D semantic contract | RegisterProducerWork and InstallForgetFence share one linearizable serialization order. Accepted work is included in the captured high-water, or post-fence work is rejected/quarantined/cleanup-only. No third outcome. |
| D35-03 | DECIDED — D semantic contract | InstallForgetFence atomically captures ProducerRegistryVersion and ProducerRegistrationHighWater with durable fence installation; CaptureProducerRegistrationHighWater verifies the immutable snapshot and cannot silently move it. |
| D35-04 | DECIDED — D semantic contract | RegisterDerivedDependency durably registers artifact identity and complete direct/transitive lineage before visibility; partial/unknown registration remains private. |
| D35-05 | DECIDED — D semantic contract | PublishDerivedIfFenceCurrent is linearized with the visibility transition and rechecks latest applicable fence plus current I authorization. An uncoordinated check-then-write or free-standing token is invalid. |
| D35-06 | DECIDED — D semantic contract | CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier define durable terminal evidence, ACK-loss recovery and immutable barrier reconciliation. Lease expiry/DLQ parking are not terminal. |
| D35-07 | DECIDED — D evidence contract | PublicationReceipt binds WorkItemId/AttemptId, ProducerClass, source revisions, ScopeRefs, RegistrationReceipt, observed/authoritative fence, PermissionEpoch, DerivedArtifact and DependencyRegistrationEvidence. FenceGeneration and PermissionEpoch are distinct types. |
| D35-08 | OPEN — Storage/Consistency | No formal Storage/Consistency Owner identified. Transaction/CAS/lock/serialization and crash-recovery realization must be assigned and validated externally; D does not approve an implementation. |
| D35-09 | OPEN — E/I/H/B and registry coordination | E must map compiler state/attempt/replay behavior to D operations; I owns PermissionEpoch semantics/global producer inventory; H/I/B align authenticated ProducerIdentity/ActorRef/ScopeRef. |
| D35-10 | NOT RUN | Ten required race/fault scenarios and additional replay/restore variants are specified; no runtime conformance evidence is claimed. |

### 7.2 Changed paths in this delivery

- Added: 03-memory-brain/forget-fence-operation-and-publication-gate.md
- Updated: 03-memory-brain/forget-fence-and-completion-contract.md
- Updated: 03-memory-brain/decision-change-log.md

No E, I, H, A, F, G, B or governance files were modified. No branch was merged.

### 7.3 Interface impact and OPEN owners

- **E:** consumes D's semantic operations; E's current compiler contract already distinguishes stable ProducerWorkItemId, AttemptId, LeaseId, DependencyRegistrationId and PublicationOperationId, and requires hidden staging, ACK-loss lookup, retry identity preservation and final gate. D has now specified semantic linearization/evidence; E's API mapping and conformance remain OPEN / E-owned.
- **Storage/Consistency:** must provide a named accountable owner and validate transaction/CAS/serialization, hidden prepare/commit if needed, replica consistency, crash recovery, restore and stale-token rejection. **Owner unassigned — OPEN.**
- **I:** owns PermissionEpoch, current authorization/revocation, global producer/recipient inventory, exceptions and global Forget completion. D does not define numeric relation to FenceGeneration.
- **H/B:** authenticated producer binding and typed ActorRef/ScopeRef semantics remain cross-owner OPEN; D consumes verified typed references only.
- **F/G/H:** their derivative-producing and consumer boundaries remain owned by those modules and require their own conformance evidence.

### 7.4 Non-claims

This delivery is a D-owned documentation contract only. It does not prove a D API exists, a Storage transaction is implemented, E has adopted a final schema, any race test passed, downstream F/G/H enforcement passed, I approved global policy, or Forget is globally/physically complete. D-REV-P1-003 remains integration OPEN pending owner implementation and conformance evidence.
