# R — System-wide Architecture Risk Assessment and Root Risk Register

- Review ID: SYS-RISK-001; Date: 2026-11-17
- Repository: oahcom/AiMemoryBrainArchitecture
- main baseline: b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Review branch: review/session-1-system-wide-risk-2026-11-17
- Status: **NOT READY FOR ARCHITECTURE FREEZE; candidate assessment pending independent review**
- This is the English peer of the Chinese report at the same revision.

## 1. Executive conclusion

**Overall disposition: NOT READY for architecture freeze.**

The project has a reasonable logical division: Canonical Memory is separate from derived indexes/Context; D owns Canonical Memory, Lineage and ForgetFence; I owns identity, authorization, revocation and Global Forget governance; C owns Provider side-effect facts; H owns protocol/Wire; Storage owns persistence, transactions, visibility and recovery. Documented responsibilities do not prove these boundaries compose under races, crashes, recovery and retries.

The root blockers are not a shortage of module documents:
1. Core domain semantics remain ADR-BLOCKED, preventing canonical identity and downstream contracts from being frozen.
2. The shared linearization foundation for final visibility and ForgetFence has not been selected.
3. Publication, Forget and recovery span independent authorities without a complete end-to-end race/crash proof.
4. Applied, Provider Outcome, Owner Admission, Storage Outcome and COC Recovery Evidence are distinct facts, not yet one unambiguous exact-version-bound completion proof.
5. Owner candidates continue to evolve; manifests and consumer adoption must be revalidated.
6. Governance and candidate protocol complexity have grown. Without executable reference models, explicit decision rights and freeze gates, governance itself may consume engineering capacity.

**Rating rationale:** Critical means a risk can directly invalidate a core correctness invariant or block architecture freeze. High means it can make cross-module behavior indeterminate, cause major rework or prevent production gates. Medium primarily affects evolution, operations or cost and can be deferred behind explicit gates. Low is isolated with controlled near-term impact. Lack of production implementation is not itself treated as an architecture defect.

## 2. Review baseline and exact evidence

### 2.1 Owner branch HEAD snapshots

| Owner | Branch | HEAD read in this review |
|---|---|---|
| main | main | b372b62c640a2b656e54b6db62a4ee67d7d8c001 |
| B | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 |
| C | session-c-agent-integration-2026-11-16 | f3251081c49e697fe4739a252e27f59e2ecd0a8f |
| D | session-d-memory-brain-2026-11-16 | 97e68fbd225bdf0ac71860c01077481afc162d50 |
| E | session-e-memory-compiler-2026-11-16 | fdb4f67a83083d995930b88f93975b5ee36080f3 |
| F | session-f-memory-runtime | 8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3 |
| G | session-g-memory-context | f9ca0ddc36e17f74041506f17039f0202d13042e |
| H | session-h-bmcp-protocol | f809be092a6c04db7982cc1bdbdd9c88787a4286 |
| I | session-i-security-governance-2026-11-16 | 28df608b075e619563c6367a8a1c171185c1faaf |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 17be31915b06d98d7f822e6e5270b8cde39eb0bb |

These are branch snapshots read in this review. They do not imply merge into main or acceptance of another Owner's exact version. Later branch changes require evidence refresh.

### 2.2 Key source files

| Topic | Exact source (branch HEAD / Path / Blob SHA) | Verified status |
|---|---|---|
| Fact/Claim | B / 0df144ae25c2039c9934395fc88b2d17080eb119 / 02-domain-model/ADR-001-fact-claim-semantics.md / a1024938ff5baba069cf128c69496a44e143330c | VERIFIED: ADR-BLOCKED; no formal decision authority, approver or decision date |
| D Publication | D / 97e68fbd225bdf0ac71860c01077481afc162d50 / 03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md / 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 | VERIFIED: D-role proposal; Owner approval/API/conformance OPEN |
| E Orchestration | E / fdb4f67a83083d995930b88f93975b5ee36080f3 / 04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md / 475fee41e5eea527af4edefbfe88c58c86967d0a | VERIFIED: cross-Owner API, approval and conformance OPEN |
| F Lifecycle/Restore | F / 8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3 / 05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md / 29e9504c75d737c2dd200ebc3306eda555f0b0ac | VERIFIED: local semantic proposal; cross-Owner interfaces/implementation unverified |
| G Context/Applied | G / f9ca0ddc36e17f74041506f17039f0202d13042e / 06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md / c1de241ec69834377d9b0e24aa4770a809796d4b | VERIFIED: local proposal; C/G/H delivery and cross-Owner interfaces OPEN |
| H Unified 1.2.13 | H / f809be092a6c04db7982cc1bdbdd9c88787a4286 / 08-bmcp-protocol/phase-3.8.9-h-exact-mapping-unified-1.2.13-c-submit-outcome-1.0.1.md / 32bf9b0fd42abe8b58749b858b1d5c9aef39c5fd | VERIFIED: candidate mapping; exact CI rerun required; not frozen |
| I P0 Allowlist | I / 28df608b075e619563c6367a8a1c171185c1faaf / 09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md / 5c0e2049513d391dfc118f4f629a5ec95de456d6 | VERIFIED: P0 projection candidate; production profile/trust roots/key operations not approved |
| Storage Topology ADR | Storage / 17be31915b06d98d7f822e6e5270b8cde39eb0bb / reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md / 1ef47d4e5711c7db73a24d249adf1992be1f6aa4 | VERIFIED: ADR-BLOCKED; no deployed topology selected |
| Storage v3.2.5 Manifest | Storage / same HEAD / reviews/storage-consistency/phase-3.6.15-storage-v3.2.5-protocol-bundle-exact-version-manifest.md / bea90697e7a61d43bed00543d636a5cdf40cf5ca | VERIFIED: successor bundle published; not jointly accepted/not frozen |
| Storage Visibility | Storage / same HEAD / reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md / 175ee7b1349cfdb79a19898b311a88391ed88010 | VERIFIED: logical transaction proposal; physical topology and implementation proof OPEN |

**Status vocabulary:**
- VERIFIED: exact file/evidence was read or the file explicitly records the status; this does not prove mechanism correctness.
- PARTIALLY VERIFIED: local candidate, CI or model evidence exists, but end-to-end coverage, Owner approval or real-topology binding is missing.
- NOT PROVEN: the claimed property lacks sufficient reproducible proof.
- BLOCKED: an explicit ADR, Owner decision or Gate prerequisite remains unmet.

## 3. System-wide Risk Register

Probability is High/Medium/Low with rationale; severity and risk level are assessed separately.

| ID / Risk | Description, root cause, affected components and failure consequence | Probability / Severity / Level | Trigger conditions | Mitigation, required decision and responsible Owner | Verification evidence, residual risk and Blocking Gate |
|---|---|---|---|---|---|
| R-01 Domain semantics and Canonical Identity remain open | B Fact/Claim ADR is unresolved. If Identity, Scope, Actor/Principal and Environment types are not aligned, D/E/F/G/H may interpret the same object differently, causing incorrect merge, authorization, retention/Forget or schema. Affected: B/D/E/F/G/H/I. | High (explicit ADR blocker and waiting consumers) / Critical / **Critical** | Before freezing canonical Fact/Claim schemas, APIs, indexes or cross-module references | B publishes options and consumer mapping; formal governance decides Fact/Claim; B/I/H/D fix nominal types, identity provenance, Scope algebra and unknown rules. Owner: B + Architecture Governance; I/H/D review consumer impact. | B Blob a1024938…143330c explicitly lacks authority/decision. Closure: formal ADR, named approver, downstream mapping and counterexample tests. Residual: migration of new types. Gate: G2/G3 BLOCKED. |
| R-02 No shared serialization foundation for ForgetFence and final visibility | Without a shared atomic transaction domain or equivalent linearizable coordinator for D Fence/Lineage and Storage Visibility Commit, check-then-write races can republish forgotten data, expose unauthorized content or close barriers incorrectly. Affected: D/Storage/E/F/G/I. | High (Storage ADR has no selected topology) / Critical / **Critical** | Concurrent publication and Forget, failover, cross-service writes or recovery | Select a provable topology: one Serializable Transaction Domain per Canonical Authority, or an equivalent coordinator with linearizability and durable participant ledger; define D row boundary, Storage final commit point and I proof validation. Owner: Storage (physical mechanism) + D (Fence) + I (authorization). | Storage ADR Blob 1ef47d…f6aa4 is ADR-BLOCKED; Visibility Blob 175ee7…8010 is logical proposal only. Closure: topology ADR, both race orders, crash/lost-ACK/failover tests. Residual: deployment failure domains. Gate: G3/G4/G5 BLOCKED. |
| R-03 End-to-end anti-resurrection proof for Forget/Revocation/Restore is missing | Forget completion depends on closed-world inventory of Producer, Attempt, Derivative, Queue, Retry, DLQ, Outbox, Index, Context, Adapter and Backup/Restore. Any delayed work or old snapshot omitted from the barrier can re-expose data after completion. Affected: D/I/E/F/G/H/C/Storage/COC. | High (multiple Owner docs still mark end-to-end interfaces/proofs OPEN) / Critical / **Critical** | Forget concurrent with derivation, retry, offline Adapter, index rebuild, restore or rollback | D defines FenceGeneration, ProducerWork/Lineage/Barrier terminality; I defines global inventory/residual policy; E/F/G/H/C/Storage provide membership/currentness evidence. UNKNOWN, inventory gap or stale high-water blocks completion and serving after restore. Owner: D + I; execution Owners own local ledgers. | D Blob 17e538…55ac78, F Blob 29e950…f0b0ac and G Blob c1de24…796d4b remain proposal/OPEN. Closure: Forget-vs-publish/replay/restore/offline reconnect/late derivative matrix and post-restore anti-resurrection negatives. Residual: third-party copies/legal retention. Gate: G4 BLOCKED. |
| R-04 Cross-Owner publication state machine and COC/JF-10 composition are unproven | Prepare→Admission→Authorization→Visibility→Closeout is describable, but Participant identity, durable order, COC Recovery Cutoff and JF-10 Prepared Participant are separate protocol domains. Treating them as one coordinator or inferring terminality from one Owner ACK can cause duplicate commit, orphan participants, false Abort or endless reconciliation. Affected: D/E/H/I/Storage/COC/A. | High (contracts mark proposal, exact review or conformance OPEN) / Critical / **Critical** | Crash after Prepare, lost D Admission ACK, I decision/revocation race, lost Storage commit response, new requests during COC recovery | Freeze each protocol's authority, stable Participant/GID, tuple digest, single-use proof, terminal states and UNKNOWN rules. COC records ordering/participant evidence only; it does not replace I/D/C decisions. Keep JF-10 separate. Owner: Storage/I/D/H; E/A integrate. | Current D/E/Storage Blobs above; Storage v3.2.5 manifest is not jointly accepted. Closure: both race orders, crash points, lost ACK, duplicate/changed digest, recovery truncation and requests-during-recovery tests against one exact bundle. Residual: coordinator operations failure. Gate: G3/G4 BLOCKED. |
| R-05 Applied and Provider Outcome evidence may be conflated | G Applied proves only a specific Context/request predicate; C Provider Outcome proves provider side effects; H transports/validates protocol evidence. Transport ACK, Adapter ACK, provider rejection label and actual model use of Context are not equivalent. Missing proof or version mismatch interpreted as success creates false audit and duplicate side effects. Affected: C/G/H/I/D/Storage. | Medium-High (boundaries defined, latest mapping Candidate, exact CI not rerun) / Critical / **High** | Request retry, redirect/failover, late ACK, stale ContextVersion, provider may have received request but outcome unknown | Freeze exact CSubmitOutcome 1.0.1 ↔ H Unified 1.2.13 mapping, C sequence namespace, signed projections and Owner Outcome dereference. Applied remains G's predicate. UNKNOWN/IN_DOUBT cannot become success or safe retry. Owner: C (Provider Truth), G (Applied), H (Wire), I (trust). | H Blob 32bf9b…c5fd explicitly says Candidate/exact CI rerun required/not frozen; G Blob c1de24…796d4b marks interfaces OPEN. Closure: current-head exact-schema CI, cross-Owner semantic negatives and final-send-boundary conformance. Residual: unobservable Provider side effects. Gate: G2/G4 BLOCKED. |
| R-06 Identity, authorization, Scope and cryptographic boundaries remain open | Principal/Actor/Workload/Environment/PolicyDomain, PermissionEpoch, KeyStatus, Issuer/Audience and anti-rollback require independent validation. Cached ALLOW, historical signatures, wrong audience or cross-domain counter comparisons can authorize incorrectly. Multi-PolicyDomain atomicity cannot be inferred from one local PermissionEpoch. Affected: I/B/H/C/D/F/G/Storage. | Medium-High (P0 projection improved, production trust roots/key governance and multi-domain decision open) / Critical / **High** | Key rotation/revocation, concurrent PolicyDomains, old snapshot restore, cross-Scope query, signed-field changes | I remains sole authorization/revocation authority; pin signed projections per message family, issuer/audience/profile/key status; compare high-waters only within each domain. Decide cross-domain atomic semantics in a separate ADR; do not concatenate local epochs. Owner: I; H/C/D/B are consumers. | I Blob 5c0e204…d456d6 leaves production profile, key custody, external anti-rollback and full P0 vectors open. Closure: exact P0 dual implementation, negative mutation matrix, revocation/restore tests and PolicyDomain ADR. Residual: supply-chain/key operations. Gate: G4/G5 BLOCKED. |
| R-07 Exact-version and evidence freshness drift | Owner branches evolve. Any Schema, Validator, Manifest or Consumer Mapping Blob change invalidates old acceptance/CI for the new combination. Path/branch names are not Blob pins; role simulation is not independent Owner approval. Affected: A–I/Storage/CI. | High (successor bundle and exact rerun gaps observed) / High / **High** | Owner changes Schema, signed projection, error code, state machine or Manifest while consumers retain old pins | Automate evidence ledger: branch HEAD, commit, path, Blob, consumer pin, approver, test run/head SHA and supersession. Blob changes invalidate affected reviews. Owner: A maintains integration ledger; each Owner signs own specification. | C/H/I/Storage sources show multiple candidate versions; H requires exact CI rerun. Closure: full consumer matrix, approval provenance, current HEAD readback and bilingual parity. Residual: transient parallel-update windows. Gate: G1/G2 BLOCKED. |
| R-08 Cross-domain Cursor/Revision/Receipt/Manifest mixing | Each Owner's sequence, epoch, watermark, generation and cursor belongs to a separate authority domain. Combining them into one scalar high-water, comparing cross-domain numbers or treating missing records as no side effect can lose revocation/Forget/Provider outcomes during recovery. Affected: B/C/D/E/F/G/H/I/COC/Storage. | Medium-High (F/G/I/H define independent watermarks; system proof incomplete) / Critical / **High** | PITR, snapshot rollback, partial log loss, cross-domain recovery batch, index gap, KeyStatus unavailable | Bind each watermark to issuer/domain/epoch/digest/continuity proof; use conjunctive recovery Manifest and validate domains independently; prohibit cross-domain numeric comparison; gap/truncation/unknown stays quarantined. Owner: each Owner owns its ledger; Storage/COC own physical/order evidence; A integrates. | F Blob 29e950…f0b0ac says IndexWatermark is partition-local and zero hits do not prove deletion; I Blob 5c0e…d456d6 requires independent anti-rollback. Closure: recovery dependency DAG, rollback/partial-prefix adversarial tests and per-domain proof completeness. Residual: external-anchor outage can halt service. Gate: G4/G5 BLOCKED. |
| R-09 Governance complexity may exceed engineering value | Multiple Owners, versions, receipts/manifests/proofs and layered Gates increase coordination cost. Without runnable reference models, decision deadlines and deprecation policy, the team may maintain governance artifacts instead of a verifiable system; implementation may duplicate state machines and become opaque to operate. Affected: system-wide; primary owners A + Architecture Governance. | Medium-High (candidate protocols, role-simulated reviews and exact pins growing quickly) / High / **High** | Same semantics in multiple protocols, manual mapping for every revision, no decision deadline, Gate dependency chains expand indefinitely | Each new proof/field must state independent failure mode, non-substitutability and minimum consumers. Build executable state-machine/fault models. Give Candidates expiry dates, freeze criteria and deprecation. Preserve necessary authority boundaries; do not merge semantics merely to simplify. Owner: A + Architecture Governance; each Owner budgets complexity. | Issue #43 scope and current protocols show substantial governance work, but no effort/throughput data exists. PARTIALLY VERIFIED; net-negative value is not proven. Closure: engineering estimate, critical-path model, minimum end-to-end slice and complexity/value review. Residual: changing requirements. Gate: G5/G8. |
| R-10 Production deployment and disaster-recovery operability lack an acceptable plan | Technology blueprint remains Candidate; Storage has not selected DB/Coordinator/failure domains/RPO/RTO/KMS/HSM/backup/on-call/SLO. If logical protocols cannot map to operable persistence/recovery, the system cannot safely launch or recover. Affected: Storage/I/A/all runtime modules. | Medium (can wait during design, mandatory before production) / Critical / **High** | Engineering/deployment review, service-boundary selection, regional/database failure | Keep architecture and engineering phases distinct. Before engineering, designate Canonical Authority, transaction domain, Coordinator, failure domains, backup/recovery and key custody; define RPO/RTO/SLO, drills, runbooks and production gates. Owner: Storage + I + designated Engineering/Operations Owner; A integrates. | Storage ADR Blob 1ef47d…f6aa4 has T1–T8 OPEN; Issue #43 calls TAB-001 Candidate. Closure: approved blueprint/topology ADR/recovery drills/operations sign-off. Residual: cloud/vendor-region failure. Gate: G5/G8 BLOCKED. |

## 4. Root-first ranking

1. **R-01 Domain semantics and identity:** without stable identity and semantics, persistence, authorization and index correctness cannot be defined.
2. **R-02 Shared linearization of ForgetFence and Visibility:** determines whether writes and Forget can both be correct.
3. **R-03 Forget/Revocation/Restore anti-resurrection:** determines whether Forget is real, provable and safe under recovery.
4. **R-04 Cross-Owner publication and recovery state machine:** determines whether modules compose into one transaction semantics.
5. **R-06 Identity and authorization trust boundary:** determines whether protected data is accessed by the right principal, purpose and environment.
6. **R-05 Applied and Provider Outcome:** determines whether external side effects and Context delivery can be proven.
7. **R-08 Cross-domain Cursor/Manifest/Recovery:** determines whether restore avoids reviving revoked state or losing committed facts.
8. **R-07 Version and evidence freshness:** determines whether PASS applies to the current architecture.
9. **R-10 Production operability:** determines whether logical guarantees survive on a real topology.
10. **R-09 Governance complexity:** determines whether the engineering organization can deliver without being consumed by protocol overhead.

## 5. Formal answers to questions A–I

**A. Ten root risks:** R-01 through R-10 form a dependency chain across semantics, linearization, Forget, cross-Owner transactions, trust, evidence, recovery, versioning, deployment and governance.

**B. Risks that can invalidate correctness:** R-01/R-02/R-03/R-04 are direct root threats; R-06/R-08 can invalidate security and recovery correctness. Correctness cannot be claimed as proven while these remain open.

**C. Unclosed decisions:** Fact/Claim ADR; D/Storage final-visibility topology; D/I/E/Storage Publication participant/terminal composition; frozen CSubmitOutcome 1.0.1 ↔ H Unified 1.2.13 mapping and exact CI; I production crypto profile/trust roots/key lifecycle/anti-rollback; Multi-PolicyDomain atomicity; Global Forget closed-world inventory/residual policy; technology blueprint/topology/RPO/RTO/SLO/operations ownership.

**D. Integration amplification:** R-02/R-03/R-04/R-05/R-06/R-08. Downstream over-interpretation of local UNKNOWN, receipt, watermark or terminal state creates composition errors.

**E. Major rework if deferred:** R-01/R-02/R-04/R-05/R-06/R-08 affect core schemas, transaction boundaries, error models, retry semantics, index/Context versions, audit and recovery protocols.

**F. Direct production blockers:** R-02/R-03/R-04/R-06/R-08/R-10, especially unselected topology, unproven Forget/Restore, authorization/anti-rollback and operational recovery.

**G. Safe-looking but unproven mechanisms:**
- UNKNOWN remains private is only a policy statement unless enforced on every Read Path, Cache, Index, Object URL, Adapter and Restore path.
- Atomic Pointer + Receipt + Outbox is unproven without the real transaction domain, read path and crash recovery.
- Signature + allowlist does not prove current authorization without current KeyStatus, Issuer/Audience, revocation and anti-rollback.
- RecoveryJoin/Manifest does not prove recovery closure without complete Owner Ledgers, Prefix Continuity and independent high-water checks.
- Applied does not prove actual behavior unless bound to exact request, ContextVersion, Provider Outcome and current authorization.

**H. Individually correct modules that compose incorrectly:**
1. D Fence and Storage Visibility can each be correct yet race without a shared linearization point.
2. I PermissionEpoch and D FenceGeneration cannot be compared numerically or substituted across domains.
3. H Wire ACK is not G Context Applied.
4. C Provider Outcome is not G Applied.
5. COC Recovery Cutoff is not the JF-10 Participant Bridge; COC is not JF-10 Coordinator and cannot issue I/D decisions.
6. F IndexWatermark is not D Producer high-water or Forget completion proof.

**I. Governance complexity vs engineering value:** The risk exists, but net-negative value is not proven. Identities, signed projections, Manifests, Participant Receipts, Owner Gates and exact pins increase correctness as well as verification/operations costs. Justify them with runnable reference models, end-to-end slices, engineering estimates and fault coverage. Do not remove necessary authority boundaries merely to simplify, and do not grow protocol complexity without a budget.

## 6. Risk dependency analysis

~~~mermaid
flowchart TD
 R1[R-01 Domain semantics / identity]
 R2[R-02 Shared serialization / visibility]
 R6[R-06 Identity and authorization]
 R4[R-04 Cross-owner publication state machine]
 R3[R-03 Forget / revocation / restore]
 R5[R-05 Applied / Provider Outcome]
 R8[R-08 Cursor / manifest / recovery]
 R7[R-07 Exact-version freshness]
 R10[R-10 Production operability]
 R9[R-09 Governance complexity]
 R1 --> R2
 R1 --> R4
 R1 --> R6
 R2 --> R3
 R2 --> R4
 R6 --> R3
 R6 --> R4
 R4 --> R5
 R3 --> R8
 R4 --> R8
 R7 --> R4
 R7 --> R5
 R8 --> R10
 R2 --> R10
 R9 -. amplifies .-> R7
 R9 -. amplifies .-> R4
~~~

R-01 precedes downstream types/references/authorization; R-02/R-06 precede safe publication/Forget races and authorization gates; R-03/R-04 establish auditable terminality; R-05 proves outcomes at the Agent/Provider boundary; R-08 carries durable authority state into recovery; R-10 determines whether logical guarantees survive on a real topology. R-07 is a horizontal evidence-validity risk; R-09 amplifies evidence-governance cost and integration delay.

## 7. Unresolved Architecture Decisions

| ID | Decision | Authority owner | Current status | Boundary |
|---|---|---|---|---|
| UAD-01 | Canonical Fact/Claim semantics, identity and revision | Architecture Governance; B proposes | ADR-BLOCKED | R does not choose for B/governance |
| UAD-02 | Shared serialization topology for D Fence and Storage Visibility | D + Storage; I reviews authorization commit point | ADR-BLOCKED | R does not define D Fence or choose Storage DB |
| UAD-03 | Exact binding and terminal state for JF-10 Prepared Participant | I + Storage; H owns Wire | OPEN / exact review | COC is not JF-10 Coordinator |
| UAD-04 | Global Forget inventory, external copies/backups and completion policy | I (governance) + D (Lineage/Fence) | OPEN / BLOCKED | R does not approve external deletion/legal retention |
| UAD-05 | Frozen CSubmitOutcome 1.0.1 ↔ H Unified 1.2.13 mapping | C + H; I reviews trust fields | C/H Candidate | H does not define Provider Truth |
| UAD-06 | Applied predicate and C/H/I/D evidence composition | G (Applied) + C (Provider) + H (Wire) | OPEN / NOT PROVEN | G does not claim model understood/used Context |
| UAD-07 | Multi-PolicyDomain cross-domain atomicity | I + Architecture Governance | BLOCKED / unproven | Do not combine local PermissionEpoch into global counter |
| UAD-08 | Production crypto profile, key lifecycle, anti-rollback anchor | I + Security/Operations | Candidate / OPEN | Candidate projection is not production approval |
| UAD-09 | Canonical Authority, DB/Coordinator, failure domains and recovery objectives | Storage + designated Engineering/Operations | ADR-BLOCKED / Candidate | Logical transaction proposal is not deployed topology |
| UAD-10 | Cross-Owner exact-version and evidence invalidation policy | A + all Owners | OPEN | A maintains integration evidence, not semantic Owner acceptance |

## 8. Closure criteria for Critical / High risks

| Risk | Minimum closure criteria |
|---|---|
| R-01 | Formal domain ADR; authority/approver/date/rationale recorded; exact consumer mappings; identity/Scope/unknown counterexamples pass |
| R-02 | Approved serialization topology; both Fence-first and Publication-first models; all crash points, lost ACK, failover and restore rollback preserve unique outcome or UNKNOWN |
| R-03 | Full Producer/Attempt/Derivative/Retry/DLQ/Outbox/Index/Context/Adapter/Backup inventory; Forget-vs-every-effect races; post-restore anti-resurrection negatives; I accepts residual exceptions |
| R-04 | Separate D/E/I/Storage/COC/JF-10 state machines; consistent Participant identity/digest; exact-bundle race/crash/replay tests; independent acceptance by each authority |
| R-05 | Frozen C/H exact schema mapping; explicit G Applied predicate; Provider send/unknown/retry/late-ACK tests; ACK cannot imply Applied/no-handoff |
| R-06 | Exact signed projection per message family; dual-implementation canonicalization parity; KeyStatus/revocation/issuer/audience/anti-rollback negatives; Multi-PolicyDomain ADR |
| R-07 | Automated traceable ledger of Owner HEAD/Blob pins/consumer matrix/Owner acceptance/exact CI head; Blob changes trigger re-review |
| R-08 | Independent cursor/high-water/epoch per domain; conjunctive Recovery Manifest; truncation/rollback/missing/stale replicas quarantined; no cross-domain numeric comparison |
| R-09 | Engineering cost/value assessment; runnable reference model; minimum end-to-end slice; proof each Gate covers a distinct risk without duplicate authority |
| R-10 | Approved topology/technology blueprint; RPO/RTO/SLO, backup, keys, failure domains, on-call and recovery drills; Engineering/Operations sign-off |

## 9. Root-first remediation recommendations

**P0 — System validity**
1. B and Architecture Governance close Fact/Claim ADR; do not freeze shared canonical Fact/Claim schemas beforehand.
2. D/Storage/I close final Visibility linearization topology ADR; define D Fence, I Commit Authorization and Storage atomic commit boundaries.
3. D/I define closed-world Forget/Revocation terminality; E/F/G/H/C/Storage each provide complete Producer/Derivative/Recipient/Restore ledgers.
4. A coordinates exact protocol-bundle review and keeps COC separate from JF-10; role simulation is not independent Owner approval.

**P1 — Correctness and integration proof**
5. Build Publication, Forget, Restore and Applied/Provider Outcome reference models against one exact version bundle.
6. Test both race orders, crashes around every durable boundary, lost ACK, duplicate request, changed digest, stale lease, old snapshot and UNKNOWN for each state machine.
7. Fix types/comparison rules for each authority-local cursor, epoch, watermark, receipt and manifest.
8. Complete C/H 1.0.1/1.2.13 exact mapping and I signed projection, KeyStatus and anti-rollback verification.

**P2 — Engineering operability**
9. Evaluate a Modular Monolith/single-authority transaction domain without presuming microservices; validate resource, index, cache and recovery with representative workloads and fault models.
10. Before engineering, designate Canonical Authority, Storage topology, Coordinator, DB adapter, backup, keys, RPO/RTO/SLO and operational responsibility.

**P3 — Governance cost**
11. Review every new Schema/Proof/Manifest against “independent failure mode — authority — consumer — test — cost.”
12. Give Candidates expiry dates, decision makers and escalation paths; do not let candidates become de facto facts.
13. Preserve bilingual semantic parity, but do not substitute translation completeness for architecture proof.

## 10. Gate assessment

| Gate | Assessment | Rationale |
|---|---|---|
| G1 Exact sources/freshness | PARTIALLY VERIFIED | Multiple Owner HEADs and key Blobs read; no automated full consumer matrix |
| G2 Owner authority/consumer acceptance | BLOCKED | Several role proposals/candidates; independent Owner acceptance incomplete |
| G3 End-to-end state/causal consistency | BLOCKED | Publication, Forget and COC/JF-10 composition lack complete proof |
| G4 P0/P1 race/crash/recovery/trust | NOT PROVEN / BLOCKED | Test specs and bounded CI exist, not end-to-end proof of current exact bundle |
| G5 Technology topology/operability | BLOCKED | Storage topology ADR-BLOCKED; TAB-001 Candidate |
| G6 Chinese/English semantic parity | PARTIALLY VERIFIED | Bilingual peer reports created here; no whole-repository audit claimed |
| G7 A integration disposition/Owner decisions | BLOCKED | R report is not A's decision or an Owner signature |
| G8 Architecture freeze recommendation | **NOT READY** | Critical risks remain open |

## 11. Conclusion and limitations

This report is based on GitHub branch snapshots and exact Blobs read on 2026-11-17. It does not claim every implementation will fail. It identifies that current design evidence does not yet prove key correctness invariants compose across Owners, failures and recovery paths.

- R-01 through R-04: Critical; close before architecture freeze.
- R-05 through R-08 and R-10: High; satisfy closure gates before the relevant freeze/production stage.
- R-09: High; validate with engineering cost and runnable reference models, not intuition.
- Owner decisions remain with their authorities; this report supplies risks, evidence and closure criteria only.
- No branch merge, Issue closure, Gate release, implementation authorization or production activation is performed.

**Disposition: NOT READY FOR ARCHITECTURE FREEZE.**
