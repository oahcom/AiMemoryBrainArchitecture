---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Restored byte-for-byte from Owner source branch; Owner acceptance remains pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "E-domain Memory Compiler record phase-3.6.1-joint-defect-closure-e-addendum.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-6-1-joint-defect-closure-e-addendum"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-1-joint-defect-closure-e-addendum
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6.1 — E Joint Defect Closure Addendum

- Authority: user-delegated DE-S Joint Architect; E producer semantics only
- Status: **JOINT SEMANTIC DECISIONS RECORDED / IMPLEMENTATION NOT VERIFIED**
- Applies with and refines `phase-3.6-joint-producer-publication-decision.md`.
- Does not claim I/D/Storage implementation or approval beyond the user's joint delegation.

## 1. JF-01 — Producer inventory and admission evidence

E MUST register every producer class and instance before it can ingest, enqueue, lease, execute, retry, replay, recompile or publish. E's class/instance inventory is versioned and reconciled against I's `ProducerDomainInventoryEpoch`; D's `ProducerRegistryVersion` and `ProducerRegistrationHighWater` remain distinct. E MUST NOT treat a D work high-water as proof that E has discovered all producer paths.

Every WorkItem registration request binds producer class/instance, stable WorkItemId, source EventRef/MemoryRef typed lineage, scope, request digest, root/parent, and inventory epoch observed. E may execute only after D returns a durable receipt and the applicable inventory seal is valid. Unknown or newly discovered producer paths stop admission and invalidate affected completion proofs.

## 2. JF-02 — Authorization gate binding

E supplies the exact action, principal/actor, artifact, source lineage, ScopeRef, WorkItemId, AttemptId, LeaseEpoch, DependencySetDigest and fence generation to the final gate. The gate must consume an I-authoritative CommitAuthorizationReceipt bound to those exact values, PermissionEpoch, revocation watermark, policy version, audience, expiry and nonce.

A cached policy result, stale epoch, expired permit, mismatched scope, or unprovable revocation ordering is denial. E cannot mint or extend authorization. The permit must remain valid under a commit/revocation serialization protocol through the actual visibility linearization point; validation only when entering PublishGatePending is insufficient. If I cannot provide this guarantee, E leaves the artifact private and reports blocked/unknown, never Published.

## 3. JF-03 — Frozen output manifest

Before any output can be submitted to dependency registration or publication, E durably freezes an `OutputManifestVersion` and digest for the root WorkItem. It enumerates every output slot/ArtifactId, expected cardinality or closed-discovery marker, child WorkItem, DerivationRunId and lineage relation. Output publication is per artifact and does not imply atomic all-output visibility.

Any new output, child, changed digest or dependency mutation creates a new manifest version and invalidates prior dependency-complete and root-terminal evidence. E must reopen, rebuild and refreeze the manifest; no in-place mutation is permitted. Root terminality requires all outputs in the final frozen manifest to have terminal dispositions, all children and attempts to be accounted for, and no unknown commit outcome or still-valid stale worker path.

## 4. JF-04 — Unknown outcome and idempotent recovery

For every D/Storage operation, E persists the exact idempotency key, request digest and returned receipt before advancing its local state. Lost ACK/timeout transitions to `OutcomeUnknown`; E queries the authoritative owner using the same key and digest. It does not create a new WorkItemId, AttemptId-independent operation key, dependency key or publication key to bypass uncertainty.

Only a confirmed receipt or confirmed rejection resolves the state. If the authority is unavailable or cannot prove the outcome, E remains non-terminal, keeps bytes private and does not emit Published. Duplicate response delivery is idempotent; same key/different digest is a conflict.

## 5. JF-05 — All consumer paths respect authoritative visibility

E's producer success, compiler indexes, event streams, outbox notifications and derived-artifact lookup are not visibility authorities. E may emit a downstream notification only after the authoritative PublicationReceipt is committed. Every E-owned reader/consumer rechecks authoritative visibility and applicable fence at use/response time; stale index or event replay cannot resurrect a suppressed artifact. E must propagate ArtifactId, digest, lineage and publication receipt so consumers can verify the same object. Consumer-specific enforcement remains with its owner; E does not claim F/G/H compliance.

## 6. JF-06 — Restore and replay safety

After worker, queue, database or object-store restore, E reconciles D's current Forget control watermark, current inventory epoch, work/attempt/lease ledger, frozen output manifest, dependency receipts, visibility receipts and I authorization/revocation watermark before resuming work. A restored queue item is not authority to execute. Stale lease epochs, stale fence observations or unknown publication outcomes are quarantined.

Object bytes remain private until the current gate succeeds. A restored Published marker is not trusted unless its receipt and digest reconcile with the current control ledger. If control-state continuity cannot be proven, E stops publication and remains recovery-blocked.

## 7. E lifecycle refinement

Add `OutputManifestOpen`, `OutputManifestFrozen`, `OutcomeUnknown` and `RecoveryBlocked` as explicit durable states (or equivalent typed substates). None is terminal. Only the final immutable output manifest plus durable per-output terminal receipts can close the root obligation. DLQ, timeout, queue deletion, worker death, lease expiry and object-store existence remain non-terminal.

E36 race/fault/replay/restore tests remain **NOT RUN**. This document records semantics, not executable implementation.


## 8. Round-1 self-review closure — JF-07 / JF-08

### JF-07 — Manifest transitions are durable barrier events

E persists every output declaration, close-discovery, freeze, reopen and terminal request against the root WorkItemId with monotonic OutputManifestVersion and immutable digest. E obtains a durable D receipt for each barrier-relevant transition before it relies on that transition. Freeze and terminal requests race through D's shared authority: terminalization names the exact final frozen version/digest; a prior manifest mutation forces terminalization to re-evaluate, while a committed terminal disposition rejects later mutation. A newly discovered independent output after terminalization must be admitted as a new linked child WorkItem before any processing, never silently attached to a terminal root. E-local manifest state is not authoritative.

### JF-08 — Unknown is not negative

E treats missing receipt, empty lookup, timeout, replica lag and coordinator outage as OutcomeUnknown unless the authoritative coordinator returns a NOT_COMMITTED result carrying a completed decision-barrier cursor. E persists that cursor with the outcome. No new idempotency key may be minted while outcome is unknown; only same-key/digest replay or authoritative lookup is permitted. An unresolved outcome prevents Published and root terminality.


### JF-09 — Bind every publish attempt to current inventory and manifest

E includes the exact InventorySealReceipt / ProducerDomainInventoryEpoch required for the Forget domain and current frozen OutputManifestVersion/digest in every dependency registration and final publish request. If inventory epoch changes, manifest reopens, or a newer manifest version exists before visibility commit, E refreshes the inventory/manifest, rebuilds dependency completeness as needed, and resubmits with a new operation key bound to the new immutable request; the prior staged bytes remain private. A previously successful PublishGatePending check or dependency receipt cannot authorize visibility against a superseded manifest or inventory seal.


## 9. Phase 3.6 deployment-profile consumption decision

E accepts the Storage-selected **single transactional database per Canonical Memory Authority with per-authority coordinator/serializable transaction** as the preferred logical deployment profile. E preserves the existing Producer Registration → private staging → complete dependency/manifest registration → final Publish Gate → atomic visibility/PublicationReceipt → terminal disposition sequence.

E's queue, lease, retry, DLQ, replay, recompile and outbox are not authorities for admission, visibility or terminality. D's durable WorkItem receipt must precede queue/lease/source dereference/execution; the final visibility commit must use the selected authoritative transaction and the exact current fence/manifest/inventory and I authorization proof. CAS is only an in-transaction guard; the Work Ledger is required; outbox is a same-transaction notification mechanism.

This acceptance is a logical consumer mapping, not an executable E API, database deployment, or independent Storage engineering approval. The repository contains no E runtime, build/test harness, migration or database configuration. E36-01..20 remain NOT RUN.

**I external dependency remains BLOCKED:** no approved I ProducerDomainInventoryEpoch/InventorySeal or commit-usable PermissionEpoch/revocation interface has been supplied. E remains private/non-terminal on missing, stale or unknown proof. The I Owner request is tracked in repository issue #4.


## 10. I Phase 3.6 technical contract refresh — CommitAuthorizationReceipt

E adopts the current I-owned `CommitAuthorizationReceipt` from `phase-3.6-identity-trust-policy-joint-closure.md` (I HEAD observed `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`). This is the delegated technical baseline; I governance approval remains blocked and C/D/E/F/G/Storage consumer acceptance is not implied.

The receipt is single-use, non-transferable and bound to policy_domain_id, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation_id, operation_payload_digest, owner_boundary and decision_id. E supplies the exact operation identity/digest and submits the receipt to the final publication gate. The gate must participate in the same I per-domain linearizable sequencer that orders authorization decisions and revocation. E records receipt ID, I decision ID, sequencer position, epoch, operation digest, owner transaction/commit cursor and terminal outcome `COMMIT_WON`, `REVOCATION_WON` or `INDETERMINATE_ABORTED`.

No offline authorization lease, stale-epoch grace or cached ALLOW is usable in this baseline. If the current I sequencer cannot be reached, the receipt is stale/mismatched/replayed, or ordering is indeterminate, E keeps bytes private and the WorkItem non-terminal.

**JF-10 — I sequencer / Storage commit recovery protocol remains an integration blocker.** The I technical contract specifies the ordering requirement but the inspected artifact does not fully define recovery when the I sequencer has recorded COMMIT_WON and the Storage transaction/visibility commit crashes or its ACK is lost. E does not invent the cross-owner transaction protocol. I + Storage must define durable correlation, idempotent lookup, owner commit proof and reconciliation for both sequencer and owner transaction. Until that is defined and tested, E cannot acknowledge Published.
