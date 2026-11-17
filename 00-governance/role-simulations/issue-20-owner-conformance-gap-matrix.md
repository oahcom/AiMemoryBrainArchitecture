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
| I | `09-security-governance/tests/global_forget_model.py`, `test_global_forget_model.py`; Phase 3.8.4 membership-proof contracts | Need exact 3.8 receipt/terminal separation, PermissionEpoch and revocation race, membership vs completeness, key-status/currentness, and owner-sequencer durability tests |
| F | `tests/anti_resurrection/f_runtime_model.py`, `tests/anti_resurrection/test_f_runtime_model.py` | Existing anti-resurrection model is useful; add Phase 3.7 Recall per-page revalidation, cursor replay, cache/index invalidation, restore quarantine, exact D/I generation and archive completeness tests |
| E | No E-local test files found in inspected branch tree | Need stable WorkItem/Attempt/Lease identity, retry/DLQ nonterminality, frozen input digest, dependency registration, private staging, Storage prepare → D admission order, same-ID crash recovery and duplicate publication tests |
| G | No G-local test files found in inspected branch tree | Need ContextVersion lineage, compaction source-union, stale Snapshot/Delta rejection, Forget invalidation, delivery/ACK non-authority, reconnect and restore quarantine tests |
| H | RecoveryJoin 1.0.2, Unified Manifest 1.2.10–1.2.12, HRC semantics, two-phase recovery, strict JSON and wire interoperability suites under `08-bmcp-protocol/tests/conformance/recovery_cutoff/` | Strong structural/wire coverage exists; still needs owner trust adapter, complete-ledger integration, signature/key-status binding and end-to-end crash/recovery consumer tests |
| Storage | JF-10 linearization reference model and restore high-water model under `reviews/storage-consistency/reference_model/` and `restore_reference/`; Phase 3.8 logical visibility contract | No evidence of deployed DB topology, real serializable transaction adapter, same-XID recovery, atomic pointer+outcome+outbox, crash/failover/PITR or physical NO_PUBLICATION proof |
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
