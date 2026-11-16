# Module A — Integration Governance Baseline & Redlines

- Module: A — Principal Integration Architect
- Proposal version: 0.1.0
- Status: **PROPOSED — Owner review required; not APPROVED**
- Owner branch: `session-a-integration-2026-11-16`
- Prepared against observed branch tip: `f8b16ce08b3e1ab3b67e502a8f1d48702bd433a9`
- Scope: Module A integration coordination and evidence governance only
- Template note: `00-governance/module-baseline-and-redlines-template.md` was not found in the live `main` governance directory or A branch governance directory during this review. This proposal follows the repository's extant governance vocabulary and records the missing template as an OPEN governance gap.

## 1. Purpose and authority

A coordinates cross-module architecture integration, maintains integration evidence and readiness records, and makes dependencies and conflicts visible to accountable Owners. A is not a project-wide approval authority and does not own the internal semantics of B–I or Storage.

A may:
- maintain the cross-module Contract Registry and typed integration registries;
- record exact source branch, HEAD, artifact path, Blob SHA and decision status;
- identify interface mismatches, stale evidence, missing approvals and gate blockers;
- coordinate Owner-to-Owner resolution and track Gate Readiness;
- define integration review procedure, evidence completeness rules and cross-module conformance plans.

A must not:
- decide or override B domain semantics, C Agent evidence semantics, D canonical commit/Forget semantics, E compiler/producer semantics, F runtime semantics, G Context Applied semantics, H BMCP wire semantics, I identity/authorization policy, or Storage physical realization;
- grant project governance approval or accept residual security/legal risk;
- infer Owner approval from artifact existence, a review comment, branch presence or a static review;
- label a design, test plan or proposed implementation as implemented, verified or passed.

## 2. Baseline status vocabulary

Every tracked statement MUST use one of the following, with evidence and authority:
- **DECIDED** — explicit normative decision by the authority Owner within that Owner's remit.
- **PROPOSED** — a proposal awaiting its Owner's decision; not normative approval.
- **OPEN** — unresolved question, dependency or missing evidence.
- **ADR-BLOCKED** — decision cannot proceed until the named ADR authority resolves it.
- **TO_VALIDATE** — hypothesis or design requiring experiment, implementation or reproducible verification.
- **NOT RUN** — required test has a specification but no execution evidence.

Artifact existence, Owner decision, cross-Owner acceptance, external governance approval, implementation evidence and test result are independent dimensions. No dimension may be inferred from another.

## 3. A-owned baseline

### 3.1 DECIDED within A's remit

- A owns cross-module coordination records, Contract Registry maintenance, Integration Findings, source-evidence freshness tracking and Gate Readiness reporting.
- The Registry is descriptive and traceable; it records other Owners' decisions but does not create or change them.
- Branch HEAD SHA and file Blob SHA are different identifiers and MUST be recorded separately.
- A review is reproducible only when the referenced file is fetched from its Owner branch and its exact Blob SHA is captured.
- Historical embedded HEAD values are snapshots, not live evidence. Every gate review MUST refresh branch refs before relying on them.
- A finding closes only when its authority Owner's required evidence is present and revalidated; document presence alone is insufficient.

### 3.2 PROPOSED operating rules

- Each contract entry should identify producer, consumer, semantic authority, transport authority (if any), schema/version, compatibility rule, failure behavior, security boundary, status and acceptance evidence.
- Each integration finding should include ID, severity, affected modules, source evidence, decision authority, closure criteria, current state and last verified HEAD.
- Gate Readiness should be reported as a vector: artifact completeness, owner decision, cross-owner acceptance, governance approval, implementation evidence and test execution.
- A should publish additive A-owned coordination artifacts; it should not edit another Owner's files to make a status appear closed.

## 4. Module boundaries and authority map

| Concern | Semantic / decision authority | A responsibility |
|---|---|---|
| Domain objects, ActorRef, ScopeRef, typed references, Fact/Claim | B; Fact/Claim ADR requires its designated ADR authority | Record dependency and exact B decision; do not redefine |
| Agent telemetry, final-request evidence, protected/managed regions | C | Record C contract and consumers; do not reinterpret evidence |
| Canonical Memory commit, ForgetOperation/Fence, canonical cursor | D | Track interfaces and cross-owner acceptance |
| Compiler admission, accepted receipts, producer publication | E | Track interface and closure evidence |
| Retrieval, index/cache, suppression and IndexWatermark | F | Track compatibility and test evidence |
| Context membership/version/change sets and Applied state | G | Track exact version alignment; do not decide Applied |
| BMCP wire, Adapter capability, ACK/reconnect | H | Track schema/version and wire-consumer alignment |
| Principal trust, authorization, PermissionEpoch, global inventory/Forget governance | I | Track governance approvals; never approve on I's behalf |
| Physical persistence, transaction, visibility and recovery | Storage accountable engineering authority | Track realization evidence; do not choose/approve implementation |
| Cross-module registry/findings/readiness process | A | Primary owner |

## 5. Cross-module integration baseline

The following is the current integration interpretation, subject to refresh against each authority Owner's live branch:

1. Typed references are not credentials or permissions. B owns domain typing; I owns trust and authorization; H owns authenticated transport/wire binding; C consumes validated bindings.
2. Telemetry acceptance, compiler processing, canonical commit, indexing, Context preparation, delivery, materialization, final request submission and Applied are distinct lifecycle/evidence stages.
3. C produces final-request submission evidence; H owns protocol/transport evidence; G alone decides Applied; I owns authorization; D owns Forget fence semantics.
4. Delivered does not mean Materialized; Materialized does not mean Final Request Submitted; Submitted does not mean Applied; Applied does not prove model attention, comprehension or successful action.
5. Memory and evidence remain data, not system/developer instructions, user-original-input replacement, tool definitions or authorization grants.
6. Canonical cursor, index watermark, Context version, source sequence, inventory epoch and permission epoch are distinct typed namespaces. A MUST NOT collapse them into one generic sequence.
7. Fact/Claim-dependent interfaces remain constrained by B's ADR-001 status; no integration artifact may silently resolve that ADR.

## 6. Integration interfaces and contracts

| Interface family | Producer / authority | Consumer(s) | A review obligation | Current status |
|---|---|---|---|---|
| Typed identity and scope | B semantics; I trust/authorization; H authenticated binding | C and other protected consumers | Ensure semantic, authentication and permission roles remain distinct | OPEN / cross-owner |
| Telemetry and provenance | C semantic contract; H transport; E ingestion | E/D/F/G | Verify lifecycle and evidence boundaries are preserved | DECIDED semantics in C; downstream conformance OPEN |
| Canonical commit / Forget | D | E/F/G/H/I/Storage | Track cursor/fence contract and durable realization separately | D semantics DECIDED; realization/conformance OPEN |
| Producer admission/publication | E, dependent on D/Storage/I | D/F/G | Track accepted receipt, barriers, retries and publication gate | Design artifacts exist; implementation NOT VERIFIED |
| Context / Applied | G state; C final request; H ACK/wire; I/D predicates | Runtime/Agent consumers | Require same exact contract version and explicit owner decisions | OPEN / P0 per A findings |
| BMCP envelope / ACK / reconnect | H | C/G and all protocol consumers | Record exact schema and capability version; no wire assumptions | H-owned; candidate until H decision |
| Authorization / revocation | I | All protected modules | Require effective policy decision and current epoch evidence | Governance OPEN / BLOCKED |
| Storage durability / recovery | Storage | D/E/F/G/H/I | Require concrete engine, topology, transaction and failure evidence | TO_VALIDATE / NOT VERIFIED |
| Cross-module conformance | Each authority Owner; test operator TBD | All affected modules | Track test IDs, builds, fixtures, traces and Owner review | NOT RUN unless execution evidence is attached |

## 7. Security redlines

A integration artifacts MUST enforce these non-negotiable coordination constraints:
- No module may consume an untrusted payload identity claim as authenticated identity.
- ScopeRef is not permission; authentication is not authorization; source authenticity is not truth.
- No stale, revoked, ambiguous or cross-scope/environment data may be treated as valid merely because an upstream artifact exists.
- No Agent intent, plan, tool invocation or delivery ACK may be promoted to completed outcome or Applied.
- No Brain-managed Memory may override System/Developer instructions, original User input or Agent safety policy.
- No A registry or finding may grant tool authority, data access, retention exception, erasure exception or residual-risk acceptance.
- Security-critical uncertainty fails closed at the owning enforcement boundary; A records the finding and evidence rather than inventing enforcement behavior.

## 8. Test and verification requirements

A's own verification responsibilities are evidence-process checks, not implementation tests:
- branch inventory refreshed at review time; full 40-character HEAD recorded;
- exact Owner artifacts fetched from the named branch; Blob SHA recorded;
- embedded source HEAD checked for staleness and superseded explicitly where needed;
- contract producer/consumer/authority/version mapping checked for completeness;
- status transitions checked against explicit Owner decision evidence;
- every closure claim linked to reproducible test/build/runtime evidence where applicable.

Cross-module test evidence MUST include test ID, requirement/contract version, source commit/build SHA, fixture and environment, operation order, expected and actual result, logs/traces, reproducible command or procedure, failure disposition, and responsible Owner review. A test specification alone is NOT RUN, not PASS.

## 9. Acceptance criteria for Module A proposal

A proposal is ready for A Owner review when:
1. A responsibilities and prohibited authority are explicit.
2. Each integration contract identifies semantic authority, producer, consumer and version dependency.
3. DECIDED / PROPOSED / OPEN / ADR-BLOCKED / TO_VALIDATE / NOT RUN are not conflated.
4. Source branch/HEAD/Blob SHA provenance is captured and freshness limitations are visible.
5. Security redlines preserve B/C/D/E/F/G/H/I/Storage authority.
6. Findings include severity, owner, closure evidence and status.
7. Gate readiness separates documentation, decisions, acceptance, governance, implementation and tests.
8. No claim of project approval, contract freeze, implementation pass or test pass is made by this proposal.

## 10. Change authority and compatibility

- A may change A-owned registry structure, finding taxonomy, integration review procedure and evidence bookkeeping.
- A may propose cross-module interface changes but MUST route semantic changes to the authority Owner(s).
- A cannot alter another module's normative artifact, ADR, schema or acceptance record.
- A cannot close a finding on behalf of an Owner or governance approver.
- Breaking changes require the affected authority Owners to publish versioned decisions and consumers to accept the exact version.
- Registry corrections must preserve history and identify superseded snapshots; no silent rewriting of prior Owner decisions.

## 11. Open items and blockers

| ID | Item | Status | Required authority / closure |
|---|---|---|---|
| A-G0-01 | Canonical governance template absent at requested path | OPEN | Governance Owner to publish/identify canonical template; A must not invent a claim that it was followed |
| A-G0-02 | Current A findings and baseline manifest embed historical HEADs | OPEN / freshness | Reconcile A-owned evidence tables against live branch tips; retain historical records as historical |
| A-G0-03 | Exact current cross-module contract versions and consumer decisions | OPEN | Refresh B/C/D/E/F/G/H/I/Storage refs and require each affected Owner's exact-version decision |
| A-G0-04 | Applied common version and complete C/G/H/D/I/B predicate agreement | OPEN / P0 | C/G/H plus predicate authorities decide the same version; A only tracks |
| A-G0-05 | Authorization governance approval and Environment Registry authority | OPEN / P0 | I and designated independent governance authorities |
| A-G0-06 | Physical persistence deployment, recovery and named approver | TO_VALIDATE / P0 | Storage engineering authority; reproducible implementation/failure evidence |
| A-G0-07 | Shared conformance and fault-injection execution | NOT RUN | Test owners/operator to execute and publish results |
| A-G0-08 | Fact/Claim-dependent integration | ADR-BLOCKED | B's ADR-001 authority; preserve block until explicit ADR resolution |

## 12. Evidence inspected for this proposal

- A branch: `session-a-integration-2026-11-16`, observed pre-write HEAD `f8b16ce08b3e1ab3b67e502a8f1d48702bd433a9`.
- A `reviews/integration/contract-registry.md` Blob `b15a87e9e259de74df600defbdd449772b9b3daa`.
- A `reviews/integration/phase-3.6-integration-findings.md` Blob `e4f3fa18d59714ad2b042ffd553dfbbcf24c246d`.
- A `reviews/integration/phase-3.6-baseline-manifest.md` Blob `0a2dd28a1977f6e73340e2f5daafd8da5c8ff5c2`.
- A `01-system-architecture/responsibility-matrix.md` Blob `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3`.
- A `01-system-architecture/system-boundaries.md` Blob `ad9ea5ce00e74dba89d325601677270a50f30926`.
- Cross-module B/C source artifacts are to be pinned by their respective Owner proposals; A records their authority boundaries but does not supersede their semantics.

## 13. Proposal disposition

**PROPOSED 0.1.0.** This artifact is an A-owned module baseline proposal only. It is not a project governance decision, not a cross-module contract freeze, not implementation acceptance, and not test approval. A Owner review and any required external governance decisions remain OPEN.
