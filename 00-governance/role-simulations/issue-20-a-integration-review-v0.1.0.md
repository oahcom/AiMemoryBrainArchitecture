# Session P — A-role Integration Review of Issue #20 v0.1.0
# Session P — A 角色 Issue #20 集成审查 v0.1.0

**Disposition:** BLOCKED — integration freeze NOT APPROVED.  
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

**Simulated A disposition: BLOCKED — no interface freeze, no architecture baseline freeze, no production readiness, no Global Forget completion, no Restore Serving authorization.**

Required next Owner actions:
1. D/I: publish exact schemas and owner-local linearization/receipt-consumption tests.
2. E/Storage: prove the two-stage D registration + Storage Prepare + D publication participant order and one final visibility gate.
3. F/G: publish generation-bound page/delivery/restore receipts and run negative replay tests.
4. H: review the Issue #20 schema candidate and publish exact compatibility/interop evidence.
5. Storage: choose the actual persistence profile and run crash/failover/same-XID/PITR fault suites.
6. A: re-fetch all branches, re-pin all exact blobs, reconcile every Owner decision and issue a new integration disposition.

Issue #20 remains OPEN. This role simulation does not impersonate independent Owner approval.
