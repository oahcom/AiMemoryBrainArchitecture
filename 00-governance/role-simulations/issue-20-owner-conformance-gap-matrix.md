# Issue #20 — Owner Conformance Gap Matrix

- Prepared by: Session P cross-owner coordination / role simulation
- Status: **PROPOSED TEST PLAN — NOT an Owner acceptance, implementation result, or conformance certificate**
- Scope: D, I, F, E, G, H, Storage and A
- Rule: A source contract is not an executable test; a reference model is not a production adapter test; a passing schema test is not proof of cryptographic trust, transaction atomicity or restore safety.

## 1. Current observed evidence

The following inventory is based on the currently inspected Owner branch trees and source documents. Branch HEADs must be refreshed before an Owner adopts a test task.

| Owner | Observed executable test assets | Gap / boundary |
|---|---|---|
| D | No D-local test directory or D-specific Phase 3.8 publication/membership test file found in inspected branch tree | Need tests for Work Registration vs ForgetFence, Storage-Prepare-before-publication-admission, owner snapshot completeness, late row invalidation, terminal proof, release CAS and same-operation recovery |
| I | `09-security-governance/tests/global_forget_model.py`, `test_global_forget_model.py`; Phase 3.8.4 membership-proof contracts. Historical CI run `43963450717` at commit `8a6a6e67696c496e265b3d87f1a550fe5e8bb2a0`: 30 tests, SUCCESS | The 30-test suite is Global Forget inventory/completion logical model, not exact Phase 3.8 receipt/terminal proof, PermissionEpoch/revocation race, membership-vs-completeness, key-status/currentness or durable owner-sequencer conformance. Run predates current I branch HEAD. |
| F | `tests/anti_resurrection/f_runtime_model.py`, `tests/anti_resurrection/test_f_runtime_model.py`. Historical CI run `43961714501` at commit `f1ba5c478e395da6b126423e32e20d0990e61920`: 19 tests, SUCCESS | Existing anti-resurrection reference model is useful; add Phase 3.7 Recall per-page revalidation, cursor replay, cache/index invalidation, restore quarantine, exact D/I generation and archive completeness tests. Run predates current F branch HEAD. |
| E | No E-local test files found in inspected branch tree | Need stable WorkItem/Attempt/Lease identity, retry/DLQ nonterminality, frozen input digest, dependency registration, private staging, Storage prepare → D admission order, same-ID crash recovery and duplicate publication tests |
| G | No G-local test files found in inspected branch tree | Need ContextVersion lineage, compaction source-union, stale Snapshot/Delta rejection, Forget invalidation, delivery/ACK non-authority, reconnect and restore quarantine tests |
| H | RecoveryJoin 1.0.2, Unified Manifest 1.2.10–1.2.12, HRC semantics, two-phase recovery, strict JSON and wire interoperability suites under `08-bmcp-protocol/tests/conformance/recovery_cutoff/`. Run `44054587381` at commit `7711233ba6853967ae0e6b568e96421459f16d71`: 288 tests SUCCESS (22 skipped) | Strong structural/wire coverage exists; still needs owner trust adapter, complete-ledger integration, signature/key-status binding and end-to-end crash/recovery consumer tests. Run is a candidate semantic/wire suite, not production COC or owner-ledger evidence. |
| Storage | JF-10 linearization reference model and restore high-water model under `reviews/storage-consistency/reference_model/` and `restore_reference/`. Restore model run `43965501810` at commit `19798634fb0d55cb0c901c8f4194506fab96b75b`: 25 tests SUCCESS. PostgreSQL 18.7 physical backup/restore capability run `43959079703` at commit `83bdacbafa840808dca9be7a8c76c4df83c63504` reports physical base backup/restore, prepared-XID survival, same-XID commit, stale-read gate, current Forget replay and restored pointer+receipt PASS | This is meaningful isolated PostgreSQL 18.7 capability evidence, not proof that production uses this topology or that D/Storage share the required serializable transaction domain. Phase 3.8.2 ADR remains ADR-BLOCKED / NO TOPOLOGY SELECTED; still need exact deployed adapter, atomic pointer+outcome+outbox, failover/PITR, crash matrices and physical NO_PUBLICATION proof. |
| A | Phase 3.8 / 3.8.4 cross-owner integration reviews and decisions | Integration review is not executable conformance. Need exact-version gate matrix, source HEAD pins, negative-vector closure and explicit blockers for any freeze decision |

## 2. Required Owner-local suites

### D — Canonical registration, ForgetFence and publication participant
1. Race RegisterProducerWork vs InstallForgetFence in both serial orders; no admission gap.
2. Reject publication admission until exact durable Storage PREPARED_HIDDEN participant is readable.
3. Bind D PublicationParticipant to exact Storage participant, publication tuple, scope, source lineage and current attempt.
4. Snapshot row-membership proof must not imply complete enumeration.
5. Require query/projection identity, pagination completion, count, ordered root, high-water, owner attestation and anti-rollback checkpoint.
6. Require signed COMPLETE_EMPTY for zero rows; reject count=0 alone.
7. Late-discovered pre-fence row invalidates snapshot and forces successor reconciliation.
8. UNKNOWN is nonterminal; D gate release requires exact generation/HWM CAS and all captured admissions terminal.
9. Same operation lookup after lost ACK; no new participant identity on retry.

### I — Authorization, revocation and inventory
1. Distinguish CommitAuthorizationRequest, consumed CommitAuthorizationReceipt and post-outcome ITerminalProof.
2. Storage may consume the I receipt at visibility linearization; it must not wait for ITerminalProof that depends on Storage outcome.
3. COMMIT_WON vs REVOCATION_WON race under one PolicyDomain sequencer.
4. UNKNOWN/IN_DOUBT holds I participant and revocation; no default allow.
5. PermissionEpoch/key-status/currentness checked at the defined linearization point.
6. Inventory membership and inventory completeness are separate; empty categories need explicit completeness evidence.
7. Late producer/backup/restore target invalidates old inventory seal.
8. Revocation/restore generation change invalidates old receipt and stale restore proof.

### F — Recall and runtime projection
1. Candidate/index/cache hit is only a hint; revalidate D eligibility and I authorization on every page.
2. Cursor binds query, scope, permission epoch, D generation, index snapshot and last stable key.
3. Stale cursor after Forget, permission change, restore or index rebuild is rejected/suppressed.
4. Cache, embedding, graph and lexical derivative invalidation is transitive by source lineage.
5. Integrity unknown or missing canonical source fails closed.
6. Restore starts isolated; no stale projection or Working Set is served before current D/I reconciliation.

### E — Compiler work and publication orchestration
1. WorkItemId + request digest immutable across retries; changed digest conflicts.
2. AttemptId/LeaseId/LeaseEpoch are distinct and monotonic; expired lease is not terminal no-publication.
3. Retry, timeout, worker loss and DLQ do not release D/I barriers.
4. Complete frozen input/dependency bundle is registered before source dereference or publication.
5. Private staging → durable Storage Prepare → D PublicationParticipant admission → I receipt → Storage visibility.
6. Crash at every boundary recovers by same stable IDs and authoritative lookup.
7. Duplicate outbox/queue delivery is idempotent; conflicting terminal outcome quarantines.

### G — Context and delivery
1. ContextVersion is distinct from canonical Memory version, F Working Set and E frozen input.
2. Every fragment retains direct and transitive source lineage.
3. Compaction creates a new immutable ContextVersion with unioned lineage and loss/fidelity evidence.
4. Stale Snapshot/Delta base is rejected; no silent merge.
5. Forget affecting any transitive source invalidates dependent ContextVersion and queued deliveries.
6. Delivery/ACK/Applied remains a bounded historical fact; none grants renewed send/serve permission.
7. Reconnect requires new authenticated session/capability and fresh current D/I checks.
8. Restore quarantines old payloads and ACKs until independent proofs pass.

### H — Schema and adapter
1. Validate strict canonicalization, duplicate-key rejection, unknown-critical rejection and typed owner positions.
2. Validate RecoveryCutoffBatch committed before Manifest reconciliation; crash resumes same pair.
3. Validate COC committed prefix union owner-local admissions using independent high-water values.
4. Validate all digest layers independently; no digest aliasing.
5. Validate D/I membership proof signatures and trust metadata via owner-provided verifier interfaces; schema-only validation is insufficient.
6. Cross-language wire vectors and negative signature/key-status/replay vectors.
7. Unknown outcome remains UNKNOWN; adapter ACK never upgrades owner terminal semantics.

### Storage — durable visibility and recovery
1. Real database/serialization topology selected and documented by Storage Owner.
2. Duplicate PrepareVisibility same tuple returns same participant; changed tuple conflicts.
3. Atomic CommitVisibility: validate PREPARED_HIDDEN + exact D current participant/fence + consumed I receipt + artifact/dependencies/scope/lease, then commit pointer + immutable outcome + outbox in one atomic boundary.
4. Same-operation lookup after lost prepare/commit ACK.
5. COMMITTED_VISIBLE vs NO_PUBLICATION cannot both exist; conflicts quarantine.
6. NO_PUBLICATION positively proves no pointer, no prepared writer, no delayed worker/outbox publisher and no restore resurrection.
7. Crash, process kill, DB restart, failover, split-brain, PITR and database-incarnation mismatch tests.
8. If PostgreSQL prepared-XID is used, test exact same-XID recovery and lock retention across restart/failover; a capability probe is not acceptance.

### A — integration and freeze
1. Pin exact commit and blob SHA for every contract/schema/test result.
2. Check every dependency join, producer/consumer direction and owner-local authority boundary.
3. Require each Owner's explicit exact-version decision; role simulation cannot substitute.
4. Gate vector must distinguish candidate design, interface acceptance, implementation, CI, physical conformance and production authorization.
5. No interface freeze while D/I membership completeness, Storage topology/atomicity or unresolved P0 invariants remain open.

## 3. P coordination reference-model coverage

P tests are deliberately supplemental and non-normative. Current test modules cover:
- D admission/fence and release CAS;
- I receipt/revocation and Storage visibility handshake;
- Restore conjunctive proof gate;
- owner snapshot membership vs completeness, COMPLETE_EMPTY, late-row invalidation;
- Recovery Cutoff before manifest, COC prefix + independent owner HWM, stable recovery pair;
- F Recall final-gate checks;
- E stable WorkItem/Attempt and private staging/prepare/admission order;
- G lineage, stale delta, Forget invalidation and stale delivery rejection;
- Draft 2020-12 schema structure and positive/negative message payloads.

They do **not** prove real cryptographic signatures, authoritative source enumeration, durable Owner ledgers, real database transaction behavior, COC quorum persistence, cross-language production adapter deployment or production restore safety.

## 4. Required next evidence handoff

Each Owner should publish, on its own branch:
- exact contract/blob SHA and schema version/digest;
- runnable Owner-local tests and command/CI run ID;
- positive and negative vectors;
- fault-injection evidence and recovery readback;
- explicit accepted/rejected/conditional disposition with enumerated exceptions.

A should then publish an exact-version integration review. Session P can maintain the register and compare evidence, but cannot sign for Owners or approve its own proposals.

## 5. Current disposition

**Implementation-level contract/test plan: PROPOSED.**  
**P reference model: supplemental test harness only.**  
**Owner-local implementation/conformance: NOT ESTABLISHED.**  
**Issue #20: remains OPEN.**  
**Joint contract freeze / production activation: NOT AUTHORIZED.**

## 6. Historical Owner CI evidence readback / Owner 历史 CI 证据回读

The following successful runs were read back from GitHub Actions logs and are pinned to their exact tested commits. They are not all current-HEAD runs:
- H Recovery Cutoff Conformance: run `44054587381`, commit `7711233ba6853967ae0e6b568e96421459f16d71`, 288 tests, 22 skipped, SUCCESS.
- I Global Forget inventory/completion logical model: run `43963450717`, commit `8a6a6e67696c496e265b3d87f1a550fe5e8bb2a0`, 30 tests, SUCCESS.
- F Runtime anti-resurrection logical model: run `43961714501`, commit `f1ba5c478e395da6b126423e32e20d0990e61920`, 19 tests, SUCCESS.
- Storage restore control high-water model: run `43965501810`, commit `19798634fb0d55cb0c901c8f4194506fab96b75b`, 25 tests, SUCCESS.
- Storage PostgreSQL 18.7 isolated physical backup/restore experiment: run `43959079703`, commit `83bdacbafa840808dca9be7a8c76c4df83c63504`. Logs report base backup/restore, prepared-XID survival, same-XID commit after restore, stale restore read gate, replay of current Forget controls before reads, forgotten-artifact suppression, unrelated artifact readability and restored prepared visibility pointer + receipt all PASS. This is a capability experiment, not deployed-topology or production acceptance.
- P supplemental Issue #20 reference-model/schema: run `44054221711`, commit `fcafce4c316c49dd4f2f78740d1a19d0ef7aa13d`, 69 tests, SUCCESS.

Current branch heads at the time of this matrix refresh: C `f2ff6ee552ed63094acbf8f36095431f0e1964b3`; D `f0672a4e9ab95b8cd94d28b52153f54a05e17a73`; E `df3f56cdebbb4bb85999e2e04b666dacf77da810`; F `348b5ec84c44a8a067122ce0aa72a594b9c06b66`; G `69ba55c5ffd473ced1ccb569e9bbf7fea48566aa`; H `46a7c534b5068e274c21c460feaf333060cb45a2`; I `de29ebcf2bb901c7ce9cca63b7d7d21c9495e491`; Storage `bd6c1d23ed685db8d4bd13a75821611e04d138ba`; P `8698ebd35809c92c0508fd6829abcc157f6ee134`. Re-fetch before future exact-version acceptance.
