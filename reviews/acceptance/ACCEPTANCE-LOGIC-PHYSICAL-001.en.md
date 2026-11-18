# Acceptance Matrix — Logic vs Physical Acceptance (Issues #25 / #43)

- Artifact ID: ACCEPTANCE-LOGIC-PHYSICAL-001
- Version: 1.0.0
- Status: PROPOSED / REVIEW REQUIRED
- Scope: additive acceptance governance for Issue #25 (D/E/I/Storage atomic producer admission and derivative visibility) and Issue #43 (system-wide architecture consolidation).
- Related contracts and work: RFC-IDE-001 v1.0.0 (Draft PR #251); callable interface candidate (PR #252); A architecture live-source delta (PR #188).
- This artifact does not supersede those deliverables, approve an Owner's semantics, select physical topology, authorize implementation, or close either issue.

## 1. Governing rule

**Logical acceptance and physical acceptance are separate gates and must be recorded separately.** Passing a logical model, document review, schema validation, or reference-model CI is not evidence that a deployed adapter, database, transaction domain, recovery process, or production environment satisfies the contract.

Each claim must be tagged with its evidence class:
- DESIGN: proposal/document review only.
- OWNER-APPROVED: explicit decision by the accountable authority, pinned to exact artifact version.
- LOGICAL-TESTED: deterministic model/unit/property tests; state the model boundary.
- PHYSICAL-TESTED: tests against the actual technology/configuration (for SQLite, a real file-backed DB where persistence/concurrency/crash behavior is claimed).
- INTEGRATION-TESTED: cross-module tests using the actual adapters and authority boundaries.
- OPERATIONALLY-VERIFIED: deployment, monitoring, backup/restore, failover and operator evidence in the target environment.

Evidence classes are not interchangeable. A later class does not retroactively approve another Owner's domain semantics.

## 2. Acceptance matrix

| Gate | Acceptance object | Required authority / decision owner | Minimum evidence | Does NOT prove |
|---|---|---|---|---|
| L0 — source baseline | Exact current source and dependency pins | A coordinates; each artifact Owner confirms own source | Branch, commit, path, Blob SHA, readback time, supersession/freshness | Semantic correctness or approval |
| L1 — logical contract | Producer identity, Scope, key namespace, Digest/replay, Receipt semantics; domain types and invariants | Producer/domain identity authority (B for canonical domain identity, subject to explicit authority confirmation); I for security/Scope authorization; Event Store contract owner for event semantics; A only reconciles | Explicit section-level decision; bilingual parity; exact version; unresolved candidates listed | Physical uniqueness, auth enforcement, transaction atomicity |
| L1 entry for idempotency | RFC-IDE-001 v1.0.0 | Domain/Producer Identity authority + I/Scope Security authority; Event Store owner acknowledges consumer obligations | Review PR #251; record ACCEPT / ACCEPT_WITH_CONDITIONS / NEEDS_REVISION / REJECT per authority; preserve TTL and cleanup as CANDIDATE until policy decision | That SQLite Adapter already conforms |
| L2 — logical composition | End-to-end state machine, linearization order, race outcomes, UNKNOWN behavior | A owns integration disposition; D, E, I and Storage each decide their own state/operation semantics | Deterministic reference-model tests for both race orders, crash cut points, lost ACK, duplicate/replay, stale lease, revocation and dependency substitution | Real DB isolation, durability, crash recovery |
| L3 — protocol contract | Nominal types, wire fields, canonicalization, signatures, versioning and error mapping | H owns protocol/wire decisions; I owns trust/security policy; producer/consumer Owners acknowledge their boundary | Exact schema/version, positive/negative vectors, signature and downgrade tests, independent Owner review | Runtime enforcement or durable commit |
| P0 — physical topology | Actual serialization/transaction owner and consistency domain for producer admission, fence, authorization, dependency registration and visibility | Storage/Consistency Owner decides storage topology; D/I/E own their respective authority-side participant behavior; A cannot select on their behalf | Selected topology, authority boundaries, transaction/participant protocol, deployment assumptions and owner approval | Correctness merely from a proposed topology diagram |
| P1 — physical atomicity | Event/Receipt and hidden participant/visibility commit boundaries | Storage implementation Owner for DB atomicity; Event Store owner for event+Receipt transaction; D/I Owners for participant acceptance/terminal proofs | Real file DB / actual adapter tests; transaction rollback; uniqueness/CAS; durability settings; concurrent independent connections; no partial visible state | Failover/restore correctness |
| P2 — physical recovery | Crash, restart, failover, restore, UNKNOWN reconciliation, stale replica and split-brain prevention | Storage/Consistency Owner for recovery substrate; D/I for their durable ledgers and currentness proofs; operators for operational procedures | Fault injection at every durable boundary; restart/reconciliation; backup/restore and failover drills; exact CI Run IDs and environment/configuration | Production readiness without target-environment operations |
| P3 — integration conformance | D→E→I→Storage→F/G consumers use exact committed artifacts and authority proofs | Each producer and consumer Owner signs own contract; A records cross-owner integration disposition | Actual adapter-to-adapter tests; substitution/replay/cross-Scope tests; current authorization/fence checks at protected boundaries; full dependency set | Independent Owner approval inferred from A's report |
| P4 — operational acceptance | Production deployment, monitoring, retention, key lifecycle, backup, incident response | Named operational/service Owner + I/security/privacy/legal authorities where applicable | Runbooks, SLO/alerts, restore evidence, retention/legal-hold policy, security approvals, deployment sign-off | Architecture freeze if logical blockers remain |
| F — freeze disposition | Architecture readiness | A publishes recommendation; each authority retains veto over its own domain; project governance authority approves project-level freeze | G1–G8 evidence ledger; all P0/P1 risks proven or explicitly blocking; bilingual consistency | Permission to deploy unless separately authorized |

## 3. Owner decision rights and verification responsibility

| Owner | Decision authority (bounded to owned domain) | Logical acceptance responsibility | Physical / conformance responsibility |
|---|---|---|---|
| A — Integration | Cross-module composition and integration disposition only; cannot approve B–I or Storage semantics | Maintain source/evidence ledger, dependency graph, contradictions, cross-owner acceptance matrix; issue integration verdict | Coordinate end-to-end conformance evidence; cannot self-certify another Owner's physical system |
| B — Domain Model | Canonical domain objects and nominal identity semantics, including the canonical ProducerIdentity type if assigned by project governance | Approve typed identity equality, domain references and canonical object semantics | Provide serialization/round-trip and domain invariant tests; not storage durability approval |
| C — Agent / Inference | Inference boundary, request/agent identity and C-owned telemetry semantics | Approve C-owned inputs/outputs and trust boundaries | Validate actual adapter/provider boundary and evidence capture within C scope |
| D — Memory Brain | Canonical Memory authority, ProducerWork admission, ForgetFence, lineage and D terminalization | Approve D participant lifecycle, admission/fence semantics and D-owned state transitions | Prove D durable ledger, fencing/currentness checks and D race/recovery behavior against its implementation |
| E — Memory Compiler | Compiler ingress, staging, lineage, dependency completeness and publication orchestration | Approve E queue/lease/run/derivation and private staging semantics | Prove register-before-work, dependency registration, stale lease, retry and publication integration in E implementation |
| F — Memory Runtime | Retrieval/index/cache consumption and final suppression | Approve F's consumption rule: only exact committed/published artifacts and current authorization/fence state | Test index/rebuild/backfill/replay and disclosure suppression against actual stores |
| G — Memory Context | Context versioning, delivery/removal and Applied evidence | Approve G-owned context/delivery/Applied state semantics | Prove actual delivery/removal/reconciliation and evidence durability within G boundary |
| H — BMCP Protocol | Wire schema, nominal wire types, canonical encoding, version negotiation and protocol error vocabulary | Approve protocol contract and interoperability vectors | Run cross-implementation serialization/signature/interoperability tests; not owner of I's trust policy |
| I — Security Governance | Principal/permission/Scope/PolicyDomain, revocation, key trust, retention and security policy | Approve authorization semantics, currentness and protected-boundary requirements | Prove actual issuer/key/policy/registry/PermissionEpoch enforcement, revocation races, historical verification and audit evidence |
| Storage / Consistency | Physical transaction topology, database consistency domain, durable participant ledger, visibility serialization and recovery substrate | Confirm that proposed logical protocol is physically realizable; cannot redefine D/I/E semantics | Own real database/adapter transaction, durability, crash, failover, restore, split-brain and physical conformance evidence |
| Event Store / SQLite Adapter | Event append and Receipt storage contract within Event Store boundary | Acknowledge RFC-IDE-001 and event/Receipt logical atomicity requirements | Prove file-backed SQLite transaction atomicity, durable uniqueness/CAS, restart replay/conflict and cleanup safety |

Owner boundaries are not inferred from job titles or branch names. If project governance has not formally assigned an authority, mark the row **AUTHORITY UNCONFIRMED / BLOCKING** and obtain explicit designation. A coordinator, implementer, or reviewer cannot sign for another authority.

## 4. Issue-specific application

### Issue #25 — D/E/I/Storage atomic producer admission and derivative visibility

The acceptance chain must be evaluated as separate proofs:

1. **L1 contract:** D's admission/fence and lineage semantics; E's register-before-queue/lease/run and complete dependency semantics; I's current authorization and terminal proof; Storage's visibility participant semantics. RFC-IDE-001 v1.0.0 is the idempotent ProducerIdentity/Scope/Key entry contract. PR #251 is the review location; PR #252 consumes it and is not a substitute for its approval.
2. **L2 composition:** preserve the currently proposed crash-safe order: Storage hidden durable participant → D PublicationParticipantRef bound to that participant → I consumes the single-use CommitAuthorizationReceipt → Storage final visibility commit validates current D fence/participant and exact I terminal proof → D/I close only after COMMITTED_VISIBLE or proven NO_PUBLICATION. UNKNOWN keeps the artifact private and barriers open.
3. **P0/P1:** Storage Owner must select and approve the physical serialization/transaction topology. Demonstrate that visibility cannot race past D fence installation or I revocation and that participant, authorization proof and visibility receipt cannot be substituted.
4. **P2/P3:** real-adapter tests for crash before/after each durable boundary, lost ACK, same/different digest retry, Scope isolation, independent connection races, restart, failover/restore and complete dependency set.
5. **Exit:** Issue #25 remains OPEN until exact Owner decisions and physical/integration evidence are recorded. PR #252's successful documentation gate is documentation evidence only, not implementation conformance.

### Issue #43 — system-wide architecture consolidation

Apply the same separation to every critical path across A–I and Storage:
- G1 exact live source pins and freshness;
- G2 authority/consumer acceptance matrix with no inferred approvals;
- G3 contradiction-free end-to-end logical model or explicitly blocking conflicts;
- G4 P0/P1 race, crash, recovery, identity and trust proofs;
- G5 technology/topology feasibility with accountable decisions and reproducible evidence;
- G6 bilingual parity;
- G7 A integration disposition plus independent Owner decisions;
- G8 explicit READY / READY WITH ENUMERATED BLOCKERS / NOT READY recommendation.

Issue #43 cannot be closed by this matrix or by PR #188's bounded live-source delta. The matrix is a governance aid, not the missing full G1–G8 report. Preserve NOT READY while critical physical topology, trust, Forget/restore and independent Owner evidence remain unproven.

## 5. Current evidence ledger and freshness notes

| Item | Current known state | Classification / use |
|---|---|---|
| RFC-IDE-001 PR #251 | Draft/Open; HEAD de0dfd157769aac67f28437a918fd1cbc0899f24; bilingual gate Run 44264890385 SUCCESS | Documentation CI only; L1 review entry, not Owner approval |
| Callable interface PR #252 | Draft/Open; HEAD f34d89d56a607eb2e321b41c73824f8765fe12d2; GOV-DOC-001 Run 44271607842 SUCCESS | Candidate logical interface/documentation; not schema freeze or physical conformance |
| A live-source delta PR #188 | Draft; source commit/head and report pins recorded in Issue #43; workflow intentionally not run under that workstream's no-workflow constraint | Bounded integration review; not full G1–G8 completion |
| PR #248/#249/#250 | Reported open and mergeable=clean at refresh handoff | Refresh exact head/reviews/checks before relying on them; mergeable is not acceptance |
| Issue #25 | Open; latest issue activity includes PR #252 documentation-gate success; owner decisions and physical topology remain open | Main D/E/I/Storage acceptance track |
| Issue #43 | Open; latest cited A report remains bounded and explicitly incomplete | System-wide consolidation and freeze gate |

A status such as OPEN, mergeable, green documentation CI, or a passing reference-model test is not a decision or physical acceptance. Before a later disposition, refresh exact PR heads, exact-head CI Run IDs, review states and Owner branch heads. User-provided refresh facts are treated as handoff input until independently refreshed.

## 6. Required decision record format

Every Owner decision must include:
- decision: ACCEPT / ACCEPT_WITH_CONDITIONS / NEEDS_REVISION / REJECT / CANDIDATE_NO_APPROVAL;
- exact artifact branch, commit, path, Blob SHA and version;
- sections/fields accepted and rejected, with replacement normative text;
- blocking and non-blocking findings;
- tests and evidence class, exact commit SHA and CI Run ID (or explicit "not run");
- physical environment/configuration and fault coverage where physical claims are made;
- downstream consumers requiring acknowledgement;
- approver identity and evidence of decision authority.

No response, file existence, PR mergeability, or another Owner's simulated role is acceptance.

## 7. Next actions and exit criteria

1. Obtain explicit B/domain identity and I/Scope-security reviews of RFC-IDE-001; leave TTL and reclamation CANDIDATE until policy evidence exists.
2. Obtain D, E, I and Storage section-level decisions on the exact Phase 3.8 source pins in Issue #25; H reviews wire-level nominal types and canonicalization.
3. Require Storage to publish selected physical topology and reproducible real-adapter transaction/recovery evidence.
4. Require D/I/E physical participant and currentness evidence at each protected boundary.
5. Reconcile F/G consumers and actual index/context delivery behavior.
6. Feed exact evidence into Issue #43 G1–G8; A issues an integration disposition without replacing Owner approvals.

Until those conditions are met, both issues remain OPEN; architecture freeze and production activation remain NOT AUTHORIZED.
