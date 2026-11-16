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
