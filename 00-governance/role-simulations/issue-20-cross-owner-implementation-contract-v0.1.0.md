# Issue #20 — Cross-Owner Implementation Contract v0.1.0
# Issue #20 — 跨 Owner 实现合同 v0.1.0

**Status / 状态:** Session P integration proposal; NON-NORMATIVE; exact Owner adoption required. / Session P 集成提案；非规范性；必须由各 Owner 精确版本采纳。  
**Issue:** #20 — Archive Producer Classification × Forget Fence × Inventory × Restore Atomicity.  
**No claim:** No production implementation, Owner approval, interface freeze, CI pass or physical/global erasure is asserted.

## 0. Exact source snapshot / 精确来源快照

Live branches and exact blobs were fetched before this proposal. They are evidence references, not approvals.

| Owner | Branch HEAD | Source Blob |
|---|---|---|
| D | `5390f9ec9b3dbbb4c0d61aadd66e53e4eed6212d` | D Phase 3.6.6 Forget Semantic Authority Addendum: `a384ffb4fff7de9b35ba6b3011d2779ad529573d` |
| I | `55942231d45837bd527f2cb00a5b72d90e4cf372` | I Phase 3.7 Current Authorization: `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`; Phase 3.6.8 Inventory/Receipt/Restore: `cf4b76f151204fa47b156b5d807e7378c28fd268` |
| F | `348b5ec84c44a8a067122ce0aa72a594b9c06b66` | F Phase 3.7 lifecycle: `29e9504c75d737c2dd200ebc3306eda555f0b0ac` |
| E | `df3f56cdebbb4bb85999e2e04b666dacf77da810` | E Phase 3.7 lifecycle: `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| G | `69ba55c5ffd473ced1ccb569e9bbf7fea48566aa` | G Phase 3.7 lifecycle: `c1de241ec69834377d9b0e24aa4770a809796d4b` |
| H | `9fe480da1e610392bd277e8f8692f7ed6922d45d` | BMCP Unified COC/JF-10 1.2.12 schema: `a54f66914a819d77f00c6af04e76453ff9f654ee` |
| Storage | `807ed18dd540c4dae3dd205ca61cc9603b1cb189` | Storage Design v3.2.3: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`; Restore contract: `4f656163aeba532a441eaed1d293a48e2363cb4a` |
| A | `1b1b76d8e2c50f7bd4400d42a26fdd0009c7adf0` | A exact-version review: `fdf63550696948f77dc37c0a3788276ac4d525f5` |

Storage v3.2.3 is explicitly a proposal requiring fresh exact-version Owner review. H 1.2.12 is an existing COC/JF-10 schema; this candidate does not replace it.

## 1. Authority split / 权威边界

- **D** owns canonical target coverage, ProducerClass/work registration, ForgetFenceGeneration, barrier membership, lineage closure, canonical suppression and D terminal proof. D cannot assert global recipient/backup inventory, physical erasure or Global Forget completion.
- **I** owns principal/workload trust, PolicyDomain, PermissionEpoch, revocation order, ProducerDomainInventoryEpoch, global inventory/seal, I receipt issue/consume and I gate release. I does not decide D Fence or Storage durability.
- **E** owns compiler work, derivation, queue/outbox and staged output. **F** owns runtime indexes/caches/Working Sets, recall suppression and cursor validity. **G** owns ContextVersion, delivery and Applied. None can infer canonical or cross-owner terminality from local completion.
- **H** owns wire schema, canonicalization and adapter transport mapping, not owner decisions.
- **Storage** owns prepared participant, DB identity/XID, private bytes, authoritative visibility/non-publication and restore fencing, not I/D decisions or G Applied.
- **A** owns integration decision and exact-version gate evaluation, not Owner decisions.

## 2. Two distinct D admission boundaries / 两个不同的 D 准入边界

E Phase 3.7 distinguishes two D actions; they MUST NOT be collapsed.

**D Work Registration (before execution):**
- Enabled D ProducerClass + durable D RegistrationReceipt are required before queue insertion, lease acquisition, execution, source dereference or derivative construction for persistent/replayable work.
- EventRef-only ingress may register before Canonical MemoryRef exists only with authenticated producer, enabled ProducerClass/version, exact Scope, canonical request digest and D-approved opaque lineage token/digest.
- Later Canonical MemoryRef/MemoryVersionRef identities and revisions must link to original EventRef lineage before dependency closure/publication.
- Retry preserves ProducerWorkItemId and request digest; AttemptId/LeaseId rotate. Recompile uses a new DerivationRunId and explicit D-linked child/re-admission decision.

**D PublicationParticipant admission (after Storage Prepare):**
- The exact StorageVisibilityParticipantRef must exist before D accepts the publication participant.
- Storage Prepare alone remains private and grants no visibility.
- D PublicationParticipantRef binds exact publication, digest, scope, source lineage and exact Storage participant.
- D admission accepted but Storage participant missing => UNKNOWN/ledger inconsistency, not safe abort.
- Storage Prepare exists but D publication admission absent => private; reconcile/rollback by the same stable operation identity.

Thus: **D Work Registration precedes execution; Storage Prepare precedes D PublicationParticipant admission; I receipt consumption follows exact D/Storage binding.**

## 3. Publication protocol / 发布协议

1. **I authenticate + authorize source access.** Validate principal/workload, delegation, action, resource, purpose, audience, Scope, Environment, PolicyDomainRef, current PermissionEpoch and revocation/registry/key state. Payload identity is an untrusted assertion.
2. **D Work Registration.** Obtain durable RegistrationReceipt before queue/lease/execute. It is not protected-payload authorization.
3. **E compile/build privately.** Preserve stable WorkItem identity, attempt lineage, source refs/revisions and complete dependencies. Bytes remain non-serving.
4. **Storage Prepare.** Persist PreparedParticipantRef, GID, DB identity/incarnation, prepare attempt/generation, ledger version, PublicationOperationId, RequestDigest and ParticipantTupleDigest. Bytes/locks remain private.
5. **D PublicationParticipant admission.** Check current ForgetFence/lineage and durably bind exact D PublicationParticipantRef to the existing StorageVisibilityParticipantRef.
6. **I consumes single-use CommitAuthorizationReceipt** in its PolicyDomain sequencer, binding PreparedParticipantRef/GID, DatabaseIncarnationRef, PrepareAttemptRef/Generation, PublicationOperationId, RequestDigest, ParticipantTupleDigest and applicable COC PrepareIntent position/digest.
7. **Storage final visibility gate.** Verify exact D current clearance and I terminal proof independently, plus exact participant tuple and current attempt. Only I COMMIT_WON permits forward visibility. REVOCATION_WON / INDETERMINATE_ABORTED require same-XID rollback and authoritative NO_PUBLICATION. UNKNOWN/IN_DOUBT retains same XID/private bytes/locks.
8. **D and I independently close their participants** only after authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION. UNKNOWN leaves both unresolved. D barrier terminalization and I revocation release are separate decisions.
9. **Downstream F/G/H.** F revalidates current D/I evidence at protected read/materialization/cache/return. G revalidates before dispatch, Adapter Apply, final request submission and materialization. Delivery/ACK is not Applied. H transports evidence; it cannot upgrade outcomes.

I outcomes:
- `COMMIT_WON`: ordering evidence, not standalone visibility permission; later revocation waits for Storage terminal outcome.
- `REVOCATION_WON` or `INDETERMINATE_ABORTED`: no forward visibility; same participant resolves NO_PUBLICATION.
- `UNKNOWN/IN_DOUBT`: nonterminal, durable, blocking.

## 4. D Forget proof / D 遗忘证明

D proof binds ForgetOperationId, normalized request digest, initial target-set digest, resolution policy/version, coverage cursor, dependency inventory version, ProducerClass registry version, ForgetFenceGeneration, installation cursor, producer-registration high-water, exact barrier membership digest, dependency-closure digest/cursor, per-member terminal receipts, per-target suppression acknowledgements, reopen generation and final reconciliation cursor.

D outcomes are distinct: (a) Coverage established; (b) Canonical suppression established; (c) Global Forget completed (I-owned; D cannot assert it).

UNKNOWN, timeout, expired lease, missing worker/queue row, absent ACK or ambiguous commit is nonterminal. Late lineage, changed registry/high-water, missing/revoked/contradictory proof or restore rollback invalidates the proof attempt. Reopen retains the active fence, increments reconciliation generation and reruns closure; it never rolls back the fence or deletes the trigger.

## 5. I inventory and currentness / I 全局清单与当前性

I reconciliation is a typed envelope over independent Owner snapshots, not a globally atomic snapshot. It binds:
- I Gate ref/state, IGateGeneration, IRequestHighWater, ordered request refs/count/root, PermissionEpoch and I sequencer position;
- PolicyDomainRef, ScopeBindingFingerprint, ProducerDomainInventoryEpoch, registry digest, relevant InventoryEntryRef/generations, TargetInventorySealRef/digest, completeness generation/status and signer/key status generation;
- D ForgetOperationRef/request digest, ForgetFenceGeneration, producer/work/attempt high-waters, barrier membership root/count/generation and dependency-closure digest/cursor;
- COC RecoveryEpoch, exact committed prefix and Recovery Cutoff Batch/participant manifest identities/digests;
- exact Storage participant tuple and RestoreAttempt/checkpoint anti-rollback anchor where applicable.

I re-reads registry, relevant entry generations, scope/policy mapping, seal/completeness, signer/key status, PermissionEpoch, sequencer and anti-rollback generation at issue/consume/release. Final I operation is one sequencer/CAS transaction. Stale/unavailable authority => UNKNOWN; I gate stays closed. D canonical suppression is necessary but insufficient for Global Forget completion.

## 6. F/E/G local contract / F/E/G 本地合同

**F:** Consumer/projection maintainer, not canonical Memory producer. Runtime derivatives carry exact lineage and Scope. Registration timeout is UNKNOWN. Index gaps, truncation, stale replicas or unknown partition coverage => INCOMPLETE/UNKNOWN; zero hits are not deletion evidence. Every protected read/materialization/cache/Working Set/derivative registration/return boundary revalidates I authorization and D eligibility. Stale Recall cursor is rejected before page disclosure. Restore quarantines bytes, queues, caches, indexes and Working Sets until current conjunctive proofs pass.

**E:** D Work Registration before queue/lease/execute/source dereference. Storage Prepare before D PublicationParticipant admission. Staged bytes private. Dependencies and lineage digest form one immutable unit. Visibility requires authoritative atomic commit checking current D fence, I authorization, D registration, dependencies, active attempt/lease, Scope and exact artifact digest. Lost ACK resolves by same stable ID+digest; UNKNOWN keeps private. DLQ/replay/recompile never resets lineage or inherits publication permission.

**G:** Persistent/replayable Context derivatives require D-enabled ProducerClass and RegistrationReceipt before queue/lease/build/source dereference/publication. ContextVersion, F WorkingSet and E frozen compiler input are distinct nominal types. DeliveryId/Attempt, H ACK, Delivered or Materialized do not prove D registration, provider submit or G Applied. Old payload/Delivery/ACK/session after restore are audit-only/quarantined; reconnect creates a new authenticated session/capability and safe ContextVersion.

## 7. COC recovery and Storage restore / COC 恢复与 Storage 恢复

Each I/D owner closes its own gate and captures its own request set/high-water atomically in its authority. Their counters are separate opaque namespaces. COC binds exact RecoveryEpoch, committed prefix P, both Owner attestations, request-set digests/high-waters, participant manifest identity/digest/count and batch idempotency identity.

Commit cutoff batch and participant-set reconciliation as two immutable quorum-committed records. Crash between them => RECOVERY_FENCED; resume same batch/manifest identity. Each Owner separately signs release after full reconciliation and final unchanged-high-water/generation CAS. COC cannot release I or D. RECOVERY_EPOCH_COMPLETED means COC recovery only.

Restore starts RESTORE_FENCED/non-serving. Replay/verify Storage/COC control records and Owner receipts; anti-rollback cannot rely only on rollback-prone restored snapshot. Independently validate current I policy/revocation/registry/PermissionEpoch and D ForgetFence/producer ledger/lineage/barrier. F/E/G/Adapter reconcile their partitions, derivatives, queues, indexes, cursors, Context and sessions. Proofs bind the same RestoreAttemptRef/checkpoint digest but retain issuer, schema, signature and opaque authority-local positions. Final Serving CAS binds data snapshot, DB incarnation, COC prefix/checkpoint, I/D proof digests, F/E/G/Adapter reconciliation digests and RestoreAttempt generation. Any missing/stale/contradictory proof => remain RESTORE_FENCED.

## 8. H wire contract / H 协议合同

The accompanying `issue20.archive-forget-restore.v0.1.0.schema.json` is structural candidate only. It defines nominally separate ProducerInstanceRef, DRegistrationReceipt, DForgetBarrierProof, IInventorySeal, ICommitAuthorizationReceipt, StorageVisibilityParticipantRef, StorageOutcomeProof, FRecallCursor, EPublicationRequest, GContextLineageManifest and RestoreProofBundle.

It does not merge D ForgetFenceGeneration, I PermissionEpoch/InventoryEpoch, F IndexGeneration, G ContextVersion, COC CoordinatorIndex or Storage XID/commit cursor into one scalar. Cryptographic projection, canonicalization, key status, authorization, completeness, same-XID recovery and CAS semantics remain validator/Owner responsibilities. It does not supersede H unified COC/JF-10 schema 1.2.12.

## 9. Race/fault matrix / 并发故障矩阵

| ID | Interleaving | Required result |
|---|---|---|
| P-01 | D Work Registration ACK lost | same ID+digest returns original receipt; no duplicate |
| P-02 | Fence closes before Work Registration | reject before queue/lease/execute |
| P-03 | Storage Prepare exists, D PublicationParticipant absent | private; same operation reconciliation |
| P-04 | D PublicationParticipant accepted but Storage participant missing | UNKNOWN; do not release |
| P-05 | D Fence advances before final visibility | stale D clearance; final gate rejects |
| P-06 | I revocation wins before receipt consume | REVOCATION_WON; same participant NO_PUBLICATION |
| P-07 | I COMMIT_WON then revocation races Storage | revocation pending until Storage terminal |
| P-08 | I receipt replay with changed digest/attempt/GID | conflict; no second consume |
| P-09 | Storage ACK lost | same participant/XID lookup; UNKNOWN remains private |
| P-10 | Storage participant missing after D admission | UNKNOWN, not inferred abort |
| P-11 | Unknown lineage/missing dependency edge | CLOSURE_OPEN |
| P-12 | Late descendant after D proof | reopen generation; old proof invalid |
| P-13 | F index gap/truncation | INCOMPLETE/UNKNOWN |
| P-14 | F cursor after I/D generation change | reject before disclosure |
| P-15 | E DLQ/recompile after Forget | lineage retained; fresh D decision |
| P-16 | G old ACK/Applied after restore | audit-only; no resend/serve |
| P-17 | Restore missing any owner proof | RESTORE_FENCED |
| P-18 | Restore stale PermissionEpoch or D FenceGeneration | Serving CAS fails |
| P-19 | COC batch committed, manifest record absent | RECOVERY_FENCED; resume same manifest |
| P-20 | I/D gate release high-water changed | CAS fails; new cutoff round |

Adjacent reference-model tests cover a deterministic subset. They are not PostgreSQL/SQLite, quorum COC, production adapter or true concurrent integration tests.

## 10. Acceptance gates / 验收门

1. D adopts exact work/publication admission, linearization, terminal proof and reopen semantics on D branch.
2. I adopts inventory seal/currentness, single-use receipt tuple, sequencer outcomes and gate release on I branch.
3. E/F/G adopt typed boundary and lifecycle contracts on their branches.
4. H adopts schema IDs, canonicalization/signature profile, compatibility and strict negative vectors on H branch.
5. Storage selects DB/version/config and proves prepare/lock/visibility/same-XID recovery/restore Serving CAS with fault tests.
6. A re-pins exact Owner blobs and issues a new integration disposition.
7. CI runs schema validation, model tests, Owner suites and DB/adapter fault tests with immutable run artifacts.

**Verdict:** IMPLEMENTATION CONTRACT PROPOSAL. Interface freeze NOT AUTHORIZED. Production readiness NOT ESTABLISHED. Issue #20 remains OPEN. No Owner signature is simulated as real.
