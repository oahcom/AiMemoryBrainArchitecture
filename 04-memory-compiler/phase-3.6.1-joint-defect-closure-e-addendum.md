# Phase 3.6.1 — E Joint Defect Closure Addendum

- Authority: user-delegated DE-S Joint Architect; E producer semantics only
- Status: **JOINT SEMANTIC DECISIONS RECORDED / IMPLEMENTATION NOT VERIFIED**
- Applies with and refines `phase-3.6-joint-producer-publication-decision.md`.
- Does not claim I/D/Storage implementation or approval beyond the user's joint delegation.

## 1. JF-01 — Producer inventory and admission evidence

E MUST register every producer class and instance before it can ingest, enqueue, lease, execute, retry, replay, recompile or publish. E's class/instance inventory is versioned and reconciled against I's `ProducerDomainInventoryEpoch`; D's `ProducerRegistryVersion` and `ProducerRegistrationHighWater` remain distinct. E MUST NOT treat a D work high-water as proof that E has discovered all producer paths.

Every WorkItem registration request binds producer class/instance, stable WorkItemId, source EventRef/MemoryRef typed lineage, scope, request digest, root/parent, and inventory epoch observed. E may execute only after D returns a durable receipt and the applicable inventory seal is valid. Unknown or newly discovered producer paths stop admission and invalidate affected completion proofs.

## 2. JF-02 — Authorization gate binding

E supplies the exact action, principal/actor, artifact, source lineage, ScopeRef, WorkItemId, AttemptId, LeaseEpoch, DependencySetDigest and fence generation to the final gate. The gate must consume an I-authoritative AuthorizationCommitPermit bound to those exact values, PermissionEpoch, revocation watermark, policy version, audience, expiry and nonce.

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
