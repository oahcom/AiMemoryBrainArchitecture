# Issue #20 — Cross-Owner Implementation Contract v0.1.0
# Issue #20 — 跨 Owner 实现合同 v0.1.0

**Status / 状态:** Session P integration proposal; NON-NORMATIVE; exact Owner adoption required. / Session P 集成提案；非规范性；必须由各 Owner 精确版本采纳。  
**Issue:** #20 — Archive Producer Classification × Forget Fence × Inventory × Restore Atomicity  
**No claim:** No production implementation, Owner approval, interface freeze, CI pass or physical/global erasure is asserted.

## 0. Exact source snapshot / 精确来源快照

The following live branch heads and source blobs were fetched before authoring this contract. They are evidence references, not approvals.

| Owner | Branch HEAD | Exact source | Blob |
|---|---|---|---|
| D | `5390f9ec9b3dbbb4c0d61aadd66e53e4eed6212d` | `03-memory-brain/phase-3.6.6-d-forget-semantic-authority-addendum.md` | `a384ffb4fff7de9b35ba6b3011d2779ad529573d` |
| I | `55942231d45837bd527f2cb00a5b72d90e4cf372` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` |
| I | same | `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md` | `cf4b76f151204fa47b156b5d807e7378c28fd268` |
| F | `348b5ec84c44a8a067122ce0aa72a594b9c06b66` | `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `29e9504c75d737c2dd200ebc3306eda555f0b0ac` |
| E | `df3f56cdebbb4bb85999e2e04b666dacf77da810` | `04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| G | `69ba55c5ffd473ced1ccb569e9bbf7fea48566aa` | `06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `c1de241ec69834377d9b0e24aa4770a809796d4b` |
| H | `9fe480da1e610392bd277e8f8692f7ed6922d45d` | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.12.schema.json` | `a54f66914a819d77f00c6af04e76453ff9f654ee` |
| Storage | `807ed18dd540c4dae3dd205ca61cc9603b1cb189` | `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.3.md` | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` |
| Storage | same | `reviews/storage-consistency/phase-3.6.5-restore-control-highwater-and-quarantine-contract.md` | `4f656163aeba532a441eaed1d293a48e2363cb4a` |
| A | `1b1b76d8e2c50f7bd4400d42a26fdd0009c7adf0` | `reviews/integration/phase-3.6-coc-persistence-exact-version-review.md` | `fdf63550696948f77dc37c0a3788276ac4d525f5` |

The Storage v3.2.3 artifact is explicitly a proposal requiring fresh exact-version Owner review. H 1.2.12 is an existing COC/JF-10 schema artifact; this proposal does not replace or silently revise it.

## 1. Authority split / 权威边界

| Owner | Sole semantic authority | Must not claim |
|---|---|---|
| D | Canonical target coverage, ProducerClass/work registration, ForgetFenceGeneration, producer barrier membership, lineage closure, canonical suppression and D terminal proof | Global recipient/backup inventory, external deletion, physical erasure or Global Forget completion |
| I | Principal/workload trust, PolicyDomain, PermissionEpoch, revocation ordering, ProducerDomainInventoryEpoch, global inventory/seal, I receipt issue/consume and I gate release | D fence/barrier completion or Storage durability |
| E | Compiler work, derivation, queue/outbox, output staging and compiler-side lineage | Canonical authority or visibility from local completion |
| F | Runtime indexes/caches/Working Sets, recall suppression, cursor and F partition/reconciliation evidence | Canonical Memory or Forget terminality |
| G | Desired Context, ContextVersion, delivery and Applied records | D registration, C provider submission or I authorization |
| H | Wire schema, canonicalization and adapter transport mapping | Owner decisions or gate release |
| Storage | Prepared participant, database identity/XID, private bytes, authoritative visibility/non-publication proof and restore fencing | I authorization, D Forget decision, C provider outcome or G Applied |
| A | Integration decision and exact-version gate evaluation | Replacing Owner decisions |

## 2. Critical distinction: two D admission boundaries / 两个 D 准入边界

The E Phase 3.7 amendments distinguish two different D actions. They MUST NOT be collapsed into one generic “D admission”.

**D Work Registration (pre-execution):**
- An enabled D ProducerClass and durable D RegistrationReceipt are required before queue insertion, lease acquisition, execution, source dereference or derivative construction for persistent/replayable work.
- EventRef-only ingress may register before a Canonical MemoryRef exists, but only with authenticated producer, enabled ProducerClass/version, exact Scope, canonical request digest and D-approved opaque lineage token/digest.
- Later canonical MemoryRef/MemoryVersionRef identities and revisions must be linked to original EventRef lineage before dependency closure/publication.
- Retry preserves ProducerWorkItemId and request digest; AttemptId/LeaseId rotate. Recompile uses a new DerivationRunId and explicit D-linked child/re-admission decision.

**D PublicationParticipant admission (after Storage Prepare):**
- E's current crash-window amendment requires the exact StorageVisibilityParticipantRef to exist before D accepts the publication participant.
- Storage Prepare alone is private and grants no visibility.
- D PublicationParticipantRef binds the exact publication, digest, scope, source lineage and exact Storage participant.
- If D Admission is accepted but the referenced Storage participant is absent, treat as UNKNOWN/ledger inconsistency, not safe abort.
- If Storage Prepare exists but D publication admission does not, remain private and resolve/rollback by the same stable operation identity.

This resolves the apparent ordering ambiguity: **D Work Registration precedes execution; Storage Prepare precedes D PublicationParticipant admission; I receipt consumption follows exact D/Storage binding.**

## 3. Publication protocol — exact ordering / 发布协议顺序

The following is the proposed cross-owner ordering for an E-produced derivative. F/G must apply equivalent currentness and lineage checks at their own protected materialization/delivery boundaries.

1. **Authenticate + authorize source access (I).** Validate principal/workload, delegation, action, resource, purpose, audience, Scope, Environment, PolicyDomainRef, current PermissionEpoch and revocation/registry/key state. Payload-supplied identity is an untrusted assertion.
2. **Register producer work (D).** Obtain durable D RegistrationReceipt before queue/lease/execute. This receipt is not authorization to expose protected payload.
3. **Compile/build privately (E).** Preserve stable WorkItem identity, attempt lineage, source refs/revisions and complete dependency set. Output bytes remain non-serving.
4. **Prepare exact Storage participant (Storage).** Persist PreparedParticipantRef, GID, DB identity/incarnation, prepare attempt/generation, participant ledger version, publication operation ID, request digest and tuple digest. Private bytes/locks remain retained.
5. **Admit publication participant (D).** D checks current ForgetFence/lineage and durably admits exact D PublicationParticipantRef bound to the already-existing StorageVisibilityParticipantRef. A fence winner blocks publication.
6. **Consume I CommitAuthorizationReceipt (I).** One single-use PolicyDomain sequencer transaction binds the exact immutable participant tuple, including PreparedParticipantRef/GID, DatabaseIncarnationRef, PrepareAttemptRef/Generation, PublicationOperationId, RequestDigest, ParticipantTupleDigest and COC PrepareIntent position/digest where applicable.
7. **Resolve final visibility (Storage).** One authoritative Storage final gate verifies exact D current clearance and I terminal proof, each in its own authority namespace, plus exact participant identity/digest and current attempt. Only I COMMIT_WON permits forward visibility. REVOCATION_WON / INDETERMINATE_ABORTED require same-XID rollback and authoritative NO_PUBLICATION. UNKNOWN/IN_DOUBT retains the same XID/private bytes/locks; no timeout or missing row inference.
8. **Close Owner participants independently.** D and I each consume the authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION proof and close only their own participant. UNKNOWN leaves both unresolved. D barrier terminalization and I revocation release are separate decisions.
9. **Expose downstream.** F may update indexes/caches only with current D/I evidence and complete lineage. G delivery/ACK is not Applied; Applied is G-owned. H only transports typed evidence. No downstream local status upgrades another Owner's outcome.

### I receipt outcomes

- `COMMIT_WON`: ordering decision only; not permission to bypass D or Storage final gate. Later revocation waits for Storage terminal outcome.
- `REVOCATION_WON`: no provider/visibility forward progress; same participant must resolve to NO_PUBLICATION.
- `INDETERMINATE_ABORTED`: no provider/visibility forward progress; same participant rollback/non-publication.
- `UNKNOWN/IN_DOUBT`: nonterminal, durable, blocking; retain participant and gates.

## 4. D Forget proof and reopening / D 遗忘证明与重开

D proof must bind:
- ForgetOperationId, normalized request digest, initial target-set digest and resolution policy/version;
- coverage status/cursor, dependency-inventory version and ProducerClass registry version;
- ForgetFenceGeneration and installation cursor;
- producer-registration high-water and exact barrier membership digest;
- dependency-closure digest/cursor and all relevant lineage edges;
- per-member terminal receipts bound to operation/work/attempt/producer/source lineage/fence generation;
- per-target suppression acknowledgements;
- reopen generation and final reconciliation cursor.

D outcomes are distinct:
- Coverage established;
- Canonical suppression established;
- Global Forget completed (I-owned; D cannot assert it).

UNKNOWN, timeout, expired lease, missing worker/queue row, absent ACK or ambiguous commit is nonterminal. Late lineage, changed registry/high-water, missing/revoked/contradictory proof or restore rollback invalidates the prior proof attempt. Reopen is monotonic evidence invalidation: retain the active fence, increment reconciliation generation and rerun closure; never delete the trigger or roll back the fence.

## 5. I inventory and currentness / I 全局清单与当前性

I's reconciliation tuple is a typed envelope over independent owner snapshots, not a claim that all owners took one globally atomic snapshot. It binds:
- I Gate ref/state, IGateGeneration, IRequestHighWater, ordered request refs/count/root, PermissionEpoch and I sequencer position;
- PolicyDomainRef, ScopeBindingFingerprint, ProducerDomainInventoryEpoch, registry snapshot digest, relevant InventoryEntryRef/generation set, TargetInventorySealRef/digest, completeness proof generation/status and signer/key status generation;
- D ForgetOperationRef/request digest, ForgetFenceGeneration, producer/work/attempt high-waters, barrier membership root/count/generation and dependency-closure digest/cursor;
- COC RecoveryEpoch, exact committed prefix and Recovery Cutoff Batch/participant manifest identities/digests;
- exact Storage participant tuple and RestoreAttempt/checkpoint anti-rollback anchor where applicable.

I must re-read current registry, relevant entry generations, scope/policy mapping, seal/completeness generation, signer/key status, PermissionEpoch, sequencer and anti-rollback generation at the authoritative issue/consume/release boundary. The final I operation is one sequencer/CAS transaction. Any stale or unavailable authority => UNKNOWN; I gate stays closed.

I alone owns GlobalInventoryCompletenessProof, TargetInventorySeal, I receipt consumption and IGateReleaseReceipt. D's canonical suppression proof is necessary but insufficient for Global Forget completion.

## 6. F/E/G local contracts / F/E/G 本地合同

**F — Runtime**
- F is a consumer/projection maintainer, not canonical Memory producer.
- Runtime-local derivatives carry exact source lineage and Scope.
- Registration timeout is UNKNOWN; never mint a new identity to bypass a barrier.
- Index gaps, truncation, stale replicas or unknown partition coverage => INCOMPLETE/UNKNOWN; zero hits are not deletion evidence.
- Every protected source read, materialization, cache/Working Set access, derivative registration and final return/visibility boundary revalidates current I authorization and D eligibility.
- Recall cursor/page resume binds principal, scope, object-set digest, policy and relevant authority generations; stale authority invalidates cursor.
- Restore quarantines bytes, queues, caches, indexes and Working Sets until Storage/COC/I/D/F proofs are current and conjunctive.

**E — Compiler**
- D Work Registration before queue/lease/execute/source dereference.
- Storage Prepare before D PublicationParticipant admission; both bind the same exact stable operation/digest/participant tuple.
- Staged bytes stay private. Dependencies and lineage digest commit as one complete immutable unit.
- Visibility only through the authoritative atomic final commit checking current D fence, I authorization, D registration, dependencies, active attempt/lease, Scope and exact artifact digest.
- Lost ACK resolves by same stable ID+digest. UNKNOWN keeps artifact private and barrier open.
- Queue/DLQ/replay/recompile never resets lineage or reuses old publication permission.

**G — Context and delivery**
- Persistent/replayable Context derivatives require D-enabled ProducerClass and D RegistrationReceipt before queue/lease/build/source dereference/publication.
- ContextVersion, F WorkingSet and E frozen compiler input bundle are distinct nominal types.
- DeliveryId/Attempt, H receipt/ACK, Delivered or Materialized do not prove D registration, provider submit or G Applied.
- Revalidate current I authorization and D eligibility before dispatch, Adapter Apply, final request submission and protected materialization.
- Old Context payload, Delivery, ACK and Adapter session after restore are audit-only/quarantined; reconnect creates a new authenticated session/capability and a new safe ContextVersion.

## 7. Storage COC, cutoff and restore / Storage COC、截止批次与恢复

**COC recovery cutoff**
- Each I/D owner closes its own gate and captures its own request set/high-water atomically in its authority.
- I and D counters are separate opaque namespaces; never sort/compare them.
- COC binds exact RecoveryEpoch, committed prefix P, both Owner snapshot attestations, request-set digests/high-waters, participant manifest identity/digest/count and exact batch idempotency identity.
- Commit cutoff batch and participant-set reconciliation as two immutable quorum-committed records to avoid circular digest dependency.
- A crash between them leaves RECOVERY_FENCED; resume same batch/manifest identity. No replacement batch.
- Each Owner separately signs release after complete request/participant reconciliation and a final unchanged-high-water/generation CAS. COC cannot release I or D.
- RECOVERY_EPOCH_COMPLETED means COC recovery only, not I authorization, D Forget, Storage visibility, C provider outcome or G Applied.

**Restore**
- Start RESTORE_FENCED / non-serving.
- Replay and verify Storage/COC control records and exact owner receipts; anti-rollback must not rely only on the rollback-prone restored snapshot.
- Independently validate current I policy/revocation/registry/PermissionEpoch and D ForgetFence/producer ledger/lineage/barrier.
- F/E/G/Adapter reconcile their own partitions, derivatives, queues, indexes, cursors, Context and sessions.
- All proofs bind the same RestoreAttemptRef/checkpoint digest but retain issuer, schema, signature and opaque authority-local positions.
- Final Serving CAS binds data snapshot, DB incarnation, COC prefix/checkpoint, I and D proof digests, F/E/G/Adapter reconciliation digests and RestoreAttempt generation.
- Missing/stale/contradictory proof, UNKNOWN, key revocation, sequencer fork, lineage gap or participant mismatch => remain RESTORE_FENCED.

## 8. H wire contract and schema / H 协议与 Schema

The accompanying `issue20.archive-forget-restore.v0.1.0.schema.json` is a structural candidate only. It defines nominally separate objects for:
- ProducerInstanceRef;
- DRegistrationReceipt and DForgetBarrierProof;
- IInventorySeal and ICommitAuthorizationReceipt;
- StorageVisibilityParticipantRef and StorageOutcomeProof;
- FRecallCursor;
- EPublicationRequest;
- GContextLineageManifest;
- RestoreProofBundle.

It intentionally does not merge D ForgetFenceGeneration, I PermissionEpoch/InventoryEpoch, F IndexGeneration, G ContextVersion, COC CoordinatorIndex or Storage XID/commit cursor into one scalar. Cryptographic projection, canonicalization, key status, authorization, completeness, same-XID recovery and CAS semantics remain validator/Owner responsibilities. This candidate does not supersede H's unified COC/JF-10 1.2.12 schema.

## 9. Implementation and test matrix / 实现与测试矩阵

| ID | Race/fault | Required outcome |
|---|---|---|
| P-01 | D Work Registration ACK lost | same ID+digest lookup returns original receipt; no duplicate registration |
| P-02 | Fence closes before Work Registration | reject/quarantine before queue/lease/execute |
| P-03 | Storage Prepare exists, D PublicationParticipant absent | private; no visibility; same operation reconciliation |
| P-04 | D PublicationParticipant accepted but exact Storage participant absent | UNKNOWN/ledger inconsistency; do not release |
| P-05 | D Fence advances after admission before final visibility | stale D clearance; final gate rejects |
| P-06 | I revocation wins before receipt consume | REVOCATION_WON; same participant NO_PUBLICATION |
| P-07 | I COMMIT_WON then revocation races Storage | revocation remains pending until Storage terminal |
| P-08 | I receipt replay with changed digest/attempt/GID | conflict; no second consume |
| P-09 | Storage ACK lost after prepare/resolve | same participant/XID linearizable lookup; UNKNOWN remains private |
| P-10 | Storage participant missing after D admission | UNKNOWN, not inferred abort |
| P-11 | Unknown lineage or missing D dependency edge | CLOSURE_OPEN; no canonical suppression completion |
| P-12 | Late descendant after D proof | reopen generation; prior proof invalidated |
| P-13 | F index gap/truncated partition | INCOMPLETE/UNKNOWN; no deletion claim |
| P-14 | F cursor resumed after I/D generation change | reject page before disclosure |
| P-15 | E DLQ/recompile after Forget | same lineage; fresh D registration/child decision; no inherited visibility |
| P-16 | G old ACK/Applied after restore | audit-only; no resend/serve |
| P-17 | Restore missing any owner proof | RESTORE_FENCED |
| P-18 | Restore has stale PermissionEpoch or D FenceGeneration | Serving CAS fails |
| P-19 | COC batch committed, manifest record absent | RECOVERY_FENCED; same manifest recovery |
| P-20 | I/D gate release with high-water changed | owner CAS fails; new cutoff round required |

Executable reference-model tests in the adjacent `tests/` directory cover a subset of these invariants. They are deterministic protocol-model tests, not concurrency tests against PostgreSQL, SQLite, a quorum COC or production adapters.

## 10. Exact acceptance gates / 精确验收门

Before this package can be promoted:
1. D adopts exact D registration/publication participant semantics, linearization point, terminal proof and reopen behavior on D branch.
2. I adopts exact inventory seal/currentness, receipt single-use tuple, sequencer outcomes and gate release on I branch.
3. E/F/G adopt the typed boundary and lifecycle contracts on their own branches.
4. H adopts schema IDs, canonicalization/signature profile, compatibility policy and strict negative vectors on H branch.
5. Storage selects and documents the persistence profile, exact DB/version/config, prepare/lock/visibility semantics, same-XID recovery and restore Serving CAS; runs fault tests.
6. A re-pins every exact Owner Blob, reconciles all changed references and issues a new integration disposition.
7. CI executes schema validation, model tests, owner-specific tests and database/adapter fault suites with immutable run IDs/artifacts.

**Current verdict:** ARCHITECTURE / IMPLEMENTATION CONTRACT PROPOSAL. Interface freeze NOT AUTHORIZED. Production readiness NOT ESTABLISHED. Issue #20 remains OPEN. No Owner signature is simulated as real.
