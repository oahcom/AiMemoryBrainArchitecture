# Session P — A-role Integration Review of Issue #20 v0.1.0
# Session P — A 角色 Issue #20 集成审查 v0.1.0

**Disposition:** ACCEPT AS CANDIDATE COMPOSITION WITH BLOCKING CONDITIONS. Joint contract freeze NOT APPROVED; production activation NOT AUTHORIZED.  
**Authority:** Session P role simulation only. This is not A Owner's signed decision or a PGA decision.  
**Review baseline:** Exact branch heads and source blobs recorded below; any movement invalidates this review snapshot.

## 1. Exact reviewed source set

| Owner | Branch HEAD | Reviewed source Blob |
|---|---|---|
| D | `5390f9ec9b3dbbb4c0d61aadd66e53e4eed6212d` | `a384ffb4fff7de9b35ba6b3011d2779ad529573d` — Phase 3.6.6 semantic authority addendum |
| I | `55942231d45837bd527f2cb00a5b72d90e4cf372` | `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` — Phase 3.7 current authorization |
| I | same | `cf4b76f151204fa47b156b5d807e7378c28fd268` — Phase 3.6.8 inventory/receipt/restore currentness |
| F | `348b5ec84c44a8a067122ce0aa72a594b9c06b66` | `29e9504c75d737c2dd200ebc3306eda555f0b0ac` — Phase 3.7 lifecycle |
| E | `df3f56cdebbb4bb85999e2e04b666dacf77da810` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` — Phase 3.7 lifecycle |
| G | `69ba55c5ffd473ced1ccb569e9bbf7fea48566aa` | `c1de241ec69834377d9b0e24aa4770a809796d4b` — Phase 3.7 lifecycle |
| H | `9fe480da1e610392bd277e8f8692f7ed6922d45d` | `a54f66914a819d77f00c6af04e76453ff9f654ee` — BMCP Unified 1.2.12 schema |
| Storage | `807ed18dd540c4dae3dd205ca61cc9603b1cb189` | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` — Storage Design v3.2.3 |
| Storage | same | `4f656163aeba532a441eaed1d293a48e2363cb4a` — Restore control-high-water contract |
| A | `1b1b76d8e2c50f7bd4400d42a26fdd0009c7adf0` | `fdf63550696948f77dc37c0a3788276ac4d525f5` — prior exact-version COC review |

## 2. Integration findings

### A-I20-01 — D work registration and D publication participant are separate gates
E Phase 3.7 explicitly requires D RegistrationReceipt before queue/lease/execute, while its crash-window correction requires Storage Prepare before D PublicationParticipant admission. These are two different D records and two different points in the lifecycle. Any implementation that collapses them into a single admission call creates an ordering gap or circular dependency. **Blocking until D/E/Storage publish exact typed schemas and transaction boundaries.**

### A-I20-02 — I receipt consumption is a single-use sequencer decision, not a detached permit
I Phase 3.7 returns COMMIT_WON, REVOCATION_WON or UNKNOWN/IN_DOUBT. The receipt binds the exact publication/Storage participant tuple. COMMIT_WON is not itself visibility. A later revocation waits for authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION. **Blocking until I/Storage exact tuple, consumption idempotency, lost-ACK lookup and same-XID resolution are adopted and tested.**

### A-I20-03 — D and I terminality remain independent
D owns ForgetFenceGeneration, producer-registration high-water, barrier membership, lineage closure and canonical suppression. I owns PermissionEpoch, IGateGeneration, ProducerDomainInventoryEpoch, global inventory/seal and I gate release. Their positions are opaque and must never be numerically compared. Neither owner may release based on the other's proof alone. **Blocking until reciprocal joins and generation-bound Owner release CAS are proven.**

### A-I20-04 — Storage v3.2.3 remains proposal-only
Storage Design v3.2.3 describes cutoff batches, owner gates, same-XID bridge and prepared participant identity. Its own status requires fresh exact-version Owner review; implementation/deployment/conformance are not established. A prior A review is bound to an earlier COC exact source set and cannot be silently reused as acceptance of v3.2.3. **Blocking until Storage selects DB/version/config and demonstrates durable prepare/lock retention, same-XID recovery, authoritative NO_PUBLICATION/COMMITTED_VISIBLE, crash/failover and restore CAS.**

### A-I20-05 — F runtime evidence is not canonical deletion evidence
F owns indexes, caches, Working Sets, recall cursors and partition coverage. Gaps/truncation/stale replicas are UNKNOWN; zero hits are not deletion proof. F cannot close D barriers. **Blocking until F partition completeness, cursor invalidation and restore reconciliation tests run against real stores.**

### A-I20-06 — E derivative lifecycle needs exact D/Storage/I composition
E preserves WorkItem/Attempt/DerivationRun identities, private staging, full dependency/lineage set and same-ID recovery. D RegistrationReceipt does not authorize protected payload or final visibility. **Blocking until exact E PublicationRequest, D PublicationParticipantRef, I receipt and Storage participant schemas share one digest-bound tuple.**

### A-I20-07 — G delivery, Applied and Context lineage are non-substitutable
G ContextVersion is distinct from F WorkingSet and E frozen input bundle. H Delivered/ACK/Materialized does not prove G Applied or C provider submit. Old ACK/Applied after restore cannot authorize resend. **Blocking until G/H/C boundaries and negative replay tests are exact-version accepted.**

### A-I20-08 — H 1.2.12 is not automatically the Issue #20 schema
The current H 1.2.12 artifact is the Unified COC/JF-10/Provider Outcome schema. The Session P Issue #20 schema is a separate candidate containing D/I/F/E/G/Storage objects. It must not be represented as H-approved or silently appended to 1.2.12. H must review nominal position types, canonicalization, signature profile, critical-field behavior and generated interoperability. **Blocking.**

### A-I20-09 — Restore requires conjunctive owner proofs and anti-rollback
Restore begins fenced/non-serving. Storage/COC/I/D/F/E/G/Adapter evidence remains separate, bound to one RestoreAttempt/checkpoint but not collapsed into a global scalar. Any missing/stale/contradictory proof prevents Serving CAS. **Blocking until real restore/PITR/failover tests demonstrate current proof replay and anti-rollback.**

## 3. Test evidence reviewed

Session P added a deterministic reference model and schema structure tests:
- `tests/issue20_reference_model.py`
- `tests/test_issue20_reference_model.py`
- `tests/test_issue20_schema_structure.py`
- Workflow `.github/workflows/issue20-contract-tests.yml`

This is a useful executable contract check, but not proof of concurrent database transactions, PostgreSQL prepared-XID behavior, SQLite profile semantics, COC quorum durability, provider idempotency, production adapters or restore correctness. Passing model tests does not close the above blockers.

## 4. Decision

**Simulated A disposition: ACCEPT AS CANDIDATE COMPOSITION WITH BLOCKING CONDITIONS.** No interface freeze, architecture baseline freeze, production readiness, Global Forget completion or Restore Serving authorization is granted.

Required next Owner actions:
1. D/I: publish exact schemas and owner-local linearization/receipt-consumption tests.
2. E/Storage: prove the two-stage D registration + Storage Prepare + D publication participant order and one final visibility gate.
3. F/G: publish generation-bound page/delivery/restore receipts and run negative replay tests.
4. H: review the Issue #20 schema candidate and publish exact compatibility/interop evidence.
5. Storage: choose the actual persistence profile and run crash/failover/same-XID/PITR fault suites.
6. A: re-fetch all branches, re-pin all exact blobs, reconcile every Owner decision and issue a new integration disposition.

Issue #20 remains OPEN. This role simulation does not impersonate independent Owner approval.

## 5. Phase 3.8.4 exact-version refresh / Phase 3.8.4 精确版本刷新

This addendum supersedes the earlier A-role verdict wording above where it implied that the candidate composition itself was rejected. The correct current disposition is candidate acceptance with blockers, consistent with the latest A branch artifacts. It does NOT authorize joint contract freeze or production activation.

Latest source branch heads observed:
- D `e326e6ec11f01776fa8c1655da232e8e0e5c4706`
- I `ac12267ab5bca6ac462893a053c93965eaa6b3b9`
- F `348b5ec84c44a8a067122ce0aa72a594b9c06b66`
- E `df3f56cdebbb4bb85999e2e04b666dacf77da810`
- G `69ba55c5ffd473ced1ccb569e9bbf7fea48566aa`
- H `ba99eea9334d77c2a014ed45d9287ef514a4d895`
- Storage `93c9546bae5e17f6b62e4219e792b947c5fbd816`
- A `6d6f08ae7704e0fa0cf0f2eee0512bf5e3eb624f`

Additional exact evidence:
- D Publication Participant and Terminal Contract Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`.
- D Owner Snapshot Membership Proof Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd`.
- I Commit Authorization Receipt / Revocation Sequencer Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`.
- I Owner Snapshot Membership Proof Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7`.
- H RecoveryJoin 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`; H Unified Manifest Union Contract Blob `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175`.
- Storage Visibility Participant / Atomic Outcome Contract Blob `175ee7b1349cfdb79a19898b311a88391ed88010`; Storage Serialization Topology ADR Blob `080433f8e13a500522bc2754da64057edb0ae9d8`.
- Current A Phase 3.8.4 Membership Proof Cross-Owner Review Blob `81d8956eedceb0b8842034c4ea1989e765dd6e4e`.
- A Phase 3.8 D/E/I/Storage Atomic Registration-to-Visibility Decision Blob `6338be6c2a45fdd35f6709beb7978725a3b8fb37`.

### A-COC-I20-10 — Membership is not completeness

RecoveryJoin 1.0.2 gives typed owner-signed row-membership proof payloads. Exact inclusion in an owner snapshot does not prove complete enumeration. Each I/D/C owner must separately prove query identity, pagination completion, count, ordered set root, owner-local high-water vector, snapshot attestation and anti-rollback. Empty sets require a signed COMPLETE_EMPTY proof. H transports/validates structure and joins references; it cannot assert owner ledger completeness or key trust.

### A-COC-I20-11 — Canonical union and digest layers

The Manifest is the disjoint typed union of quorum-committed COC participants at/before prefix P and applicable unjoined I/D/C owner-local admissions at/below each owner's independently frozen high-water. No synthetic participant identity or cross-owner numeric order is allowed. Keep `member_set_root`, `manifest_content_digest`, `manifest_record_entry_digest`, `batch_digest` and `batch_entry_digest` distinct. RecoveryCutoffBatch commits before ParticipantSetReconciliation; crash between them leaves the epoch fenced and recovery must resume the same pair.

### A-COC-I20-12 — I pre-commit and post-commit proofs are different

The consumed I CommitAuthorizationReceipt is the pre-commit ICommitAuthorizationProof validated by Storage at the visibility linearization point. ITerminalProof is issued only after authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION and is used for closeout. Storage must not require ITerminalProof to create the Storage outcome. I 3.8 receipt outcomes are COMMIT_WON, REVOCATION_WON and UNKNOWN/IN_DOUBT.

### A-COC-I20-13 — Physical Storage topology remains BLOCKED

Storage 3.8 visibility is a logical transaction proposal. Storage 3.8.2 topology ADR is ADR-BLOCKED / NO TOPOLOGY SELECTED. Option A (single serializable transaction domain per Canonical Memory authority) and Option B (durable linearizable coordinator) remain candidates; check-then-write/eventual coordination is rejected. The current branch does not prove actual deployment topology, database/adapter binding, same-XID recovery or physical crash/failover/restore conformance.

### Refreshed simulated A verdict

**ACCEPT AS CANDIDATE COMPOSITION WITH BLOCKING CONDITIONS.** Gate A remains PARTIAL PASS / OPEN; Gate B BLOCKED; Gate C BLOCKED; R1/R2 OPEN; JF-10 P0 OPEN; multi-PolicyDomain atomicity BLOCKED. The latest A branch review itself is a delegated role review, not an independent human Owner/governance signature. No interface freeze or production activation.
