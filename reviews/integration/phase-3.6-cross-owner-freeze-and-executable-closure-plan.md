# Phase 3.6 — Cross-Owner Contract Freeze & Executable Closure Plan

- Owner: Session A — Principal Integration Architect
- Repository: oahcom/AiMemoryBrainArchitecture
- Status: **ACTIVE PLAN / NO OWNER APPROVAL IMPLIED**
- Baseline input: `reviews/integration/phase-3.6-context-runtime-evidence-joint-report.md`
- Scope: C/G/H Applied Evidence; B/I/H typed identity and authorization; D/E/Storage durable Forget linearization; C/F/G/H/D/E/I conformance evidence.

## 1. Executive mandate

This plan converts the Phase 3.6 cross-module findings into an ordered, evidence-driven closure program. A coordinates and records decisions; A does not acquire ownership of any module contract, wire schema, authorization policy, storage implementation, or runtime implementation.

The following states remain distinct and must never be collapsed:

1. **Specified** — normative contract and test oracle are written.
2. **Owner-Decided** — every authority owner for the affected semantics has explicitly approved the exact artifact/version.
3. **Frozen** — the complete cross-owner contract set is mutually consistent, version-pinned, and no unresolved normative field remains.
4. **Implemented** — executable code/configuration realizes the frozen contract.
5. **Verified** — reproducible tests and fault evidence pass against the identified build/deployment.
6. **Operationally Closed** — governance inventory, recovery, recipient/backup treatment, and global completion evidence are complete.

A document, branch commit, architecture decision, or test specification alone cannot establish Implemented, Verified, or Operationally Closed.

## 2. Current baseline carried forward

The CFG joint report records:
- C/F/G Phase 3.6 owner artifacts delivered and read-back verified.
- Applied evidence stages separated: Prepared, Delivered, Materialized, Final Request Submitted, Applied, Execution Started.
- F requires authority checks across retrieval and at final disclosure.
- G owns ContextVersion, Delivery and Applied state.
- H Phase 3.5 Applied/ACK/reconnect proposal remains CANDIDATE; no H wire freeze is implied.
- B/I/H typed identity, scope, environment and PermissionEpoch mapping still needs explicit approval.
- D/E/Storage have made a delegated joint **logical** linearization architecture decision.
- Concrete transaction authority, deployment configuration, durable implementation, crash/failover/restore proof and executable conformance remain unverified.

The baseline report's current acceptance values are carried forward until superseded by fresh evidence:
- Applied Contract Frozen: NO.
- Runtime Forget End-to-End Closed: NO.
- Test Executed: NO.
- Test Passed: NO.
- Implementation Verified: NO.

All branch tips are time-specific. Before each closure batch, A must re-query Owner branches and record branch name, observed HEAD, artifact path, blob SHA, and read-back time. A missing file on main is never evidence that an Owner artifact does not exist.

## 3. Workstream 1 — C/G/H Applied Evidence Contract Freeze

### 3.1 Authority and responsibility

| Concern | Authority | Required contribution |
|---|---|---|
| Final request boundary observation and immutable submission evidence | C | Define observable boundary, evidence identity, digest coverage, integrity, failure/unknown states and capability ceiling |
| ContextVersion, Delivery, Applied state and acceptance predicate | G | Define canonical state machine, idempotency, supersession, historical truth vs current-use validity |
| BMCP wire schema, authenticated ACK, replay protection, capability negotiation and reconnect | H | Define wire fields, authenticated principal/session binding, ACK classes, replay/duplicate/late semantics, CapabilityEpoch and reconnect protocol |
| Permission decision and PermissionEpoch currentness | I | Define the authorization decision evidence C/G/H must bind and revalidate |
| ForgetFence and source-lineage currentness | D | Define the exact fence/source-lineage predicate consumed at final submission and Applied acceptance |

### 3.2 Required freeze package

C, G and H must produce a version-pinned mapping table containing, at minimum:

- ContextVersion, DeliveryId, AttemptId, InferenceRequestId and FinalRequestBoundaryId.
- Authenticated Principal/Actor, Agent, Adapter, RuntimeSession and BMCP session identities.
- ScopeRef, EnvironmentRef and ManagedRegion identity.
- Complete managed-region content digest and canonicalization/version algorithm.
- PermissionDecisionId and PermissionEpoch, including decision issuer and currentness/revocation check.
- ForgetOperationId or equivalent lineage binding, ForgetFenceGeneration and source dependency set identity.
- CapabilityEpoch, negotiated capability profile and evidence tier.
- Delivery receipt, materialization evidence, final submission evidence, ACK evidence and Applied receipt identities.
- Integrity/authentication mechanism, signing or MAC authority, key/issuer rotation and verification failure behavior.
- Duplicate, replay, out-of-order, late ACK, old-session ACK, reconnect, timeout and ambiguous-boundary outcomes.
- Explicit behavior when the adapter cannot observe the actual final provider/runtime submission boundary.

### 3.3 Non-negotiable semantic invariants

1. Materialized is not Final Request Submitted; Final Request Submitted is not Applied; Applied is not Execution Started.
2. No Full Applied without exact request, version, delivery attempt, authenticated session, scope, managed-region digest, current PermissionEpoch, current ForgetFenceGeneration, current CapabilityEpoch and valid C/H evidence.
3. An evidence tier may claim no more than the adapter can actually observe and authenticate.
4. Missing, stale, mismatched, unverifiable or ambiguous authority fails closed; represent Unknown where the ordering cannot be proved.
5. Historical Applied evidence is immutable; Forget/revocation may invalidate current-use eligibility without rewriting historical truth.
6. Late or duplicate evidence cannot roll back a newer version/attempt/session.
7. ACKs are bound to the original authenticated session and attempt; they cannot be rebound after reconnect.
8. Applied does not claim model attention, comprehension or use.

### 3.4 Exit criteria

- C, G and H each explicitly approve the same versioned mapping and state machine.
- H's Candidate wire proposal is either superseded by an approved Phase 3.6 schema or explicitly retained as non-frozen with listed blockers.
- I and D confirm the authority fields and currentness predicates consumed by the Applied gate.
- Positive and negative schema fixtures are specified, including malformed identity, stale epoch, replay, altered digest, old session and unobservable boundary.
- A records immutable artifact SHAs and exact approval statements.

Until all criteria pass: **Applied Contract Frozen = NO**.

## 4. Workstream 2 — B/I/H Typed Identity, Scope and Authorization Freeze

### 4.1 Authority and responsibility

| Concern | Authority | Required contribution |
|---|---|---|
| Domain reference types and reference registry | B | Canonical PrincipalRef/ActorRef/AgentRef/AdapterRef/ScopeRef/EnvironmentRef semantics and consumer mappings |
| Issuer trust, principal/actor mapping, authorization policy, PermissionEpoch and revocation | I | Trusted issuer chain, delegation, decision authority, revocation/currentness and fail-closed policy |
| Wire identity, session authentication and adapter binding | H | Authenticated wire/session claims and mapping to B/I canonical references |
| Consumer use | C/F/G/D/E | Explicit field mapping and rejection behavior; no local reinterpretation |

### 4.2 Required identity mapping

The freeze package must answer, without overloaded or stringly-typed identifiers:

- Who is the Principal, Actor, Agent, Adapter, Issuer and Runtime Session?
- Which component authenticated each identity, and which issuer/key epoch is trusted?
- How does Actor map to Principal, and what delegation chain is valid?
- Which ScopeRef and EnvironmentRef apply to a request, memory item, context delivery, retrieval result and producer work item?
- Are references tenant-, user-, workspace-, project-, environment- or resource-scoped? Define hierarchy and non-inheritance.
- Which fields are identifiers, which are display labels, and which are authenticated claims?
- How are reference versioning, aliasing, migration, revocation and unknown references handled?
- Which consumer field is authoritative at C/F/G/H/D/E boundaries?

### 4.3 Required negative cases

- Payload-supplied Principal/Actor/Agent/Adapter/Issuer/Scope/Environment conflicts with authenticated channel identity.
- Valid identity but unauthorized Scope or Environment.
- Delegation expired, revoked, cyclic, wrong audience or wrong issuer.
- PermissionEpoch stale at candidate generation but current at final disclosure, and vice versa.
- Cross-tenant or cross-scope reference substitution.
- Unknown, malformed, aliased or deprecated reference type.
- Reconnect with a different principal, actor, adapter, session or capability epoch.
- Authorization service unavailable or revocation status indeterminate.

### 4.4 Exit criteria

- B, I and H approve one canonical typed reference and authenticated-claim mapping.
- Every consuming module lists its exact input field, source authority, validation point and failure behavior.
- PermissionEpoch partitioning/currentness and revocation freshness are explicit.
- Negative tests demonstrate no cross-scope disclosure, no payload-identity trust and no stale authorization acceptance.

Until all criteria pass: **Identity/Authorization Contract Frozen = NO**.

## 5. Workstream 3 — D/E/Storage Durable Forget Linearization: Implement and Prove

### 5.1 Decision status

The D/E/Storage logical architecture is **DECIDED** in the joint decision artifacts. This workstream must not reopen the selected logical model unless implementation evidence demonstrates an impossibility or a correctness defect.

The remaining gap is physical and executable: concrete transaction authority, database/engine/version/configuration, durable ledgers, cross-store visibility, crash recovery, failover, replay, restore and deterministic fault proof.

### 5.2 Required implementation package

D, E and Storage must jointly identify and deliver:

1. Canonical Memory Authority and its concrete serialization/transaction authority.
2. Database/engine/version, isolation level, durability mode, replication topology and relevant configuration.
3. Durable producer registry/admission ledger and ProducerRegistrationHighWater.
4. Stable WorkItemId, AttemptId, LeaseEpoch and DerivationRunId persistence and uniqueness constraints.
5. Durable ForgetFence/high-water and barrier terminality records.
6. Complete source/dependency registration receipt before queue, lease, execution or source dereference.
7. Private staged bytes and an explicit authoritative visibility marker/commit predicate.
8. Final authorization, fence, work, lease and dependency revalidation at visibility commit.
9. PublicationReceipt and idempotent acknowledgement ordering.
10. Reader visibility predicate proving staged/incomplete artifacts remain invisible.
11. Outbox/event publication and repair/reconciliation behavior.
12. Crash recovery, failover, replay, backup restore and disaster-recovery behavior that cannot resurrect pre-fence artifacts.
13. Operational evidence linking canonical source lineage to all derived artifacts, indexes, caches, replicas and backups.

### 5.3 Required deterministic race/fault tests

- Producer registration vs ForgetFence advance, both serialization orders.
- Dependency registration vs ForgetFence advance, both serialization orders.
- Final publish validation vs ForgetFence advance, both serialization orders.
- PermissionEpoch/revocation change immediately before final visibility commit.
- Crash after staged write but before dependency registration.
- Crash after dependency registration but before visibility commit.
- Crash during commit/receipt/outbox acknowledgement.
- Lease expiry and stale worker publish after a new LeaseEpoch.
- Duplicate retry, DLQ replay and recovery with stable WorkItemId.
- Failover during fence advancement and during publication.
- Restore from a backup containing pre-fence data, followed by mandatory fence/high-water replay before readers become available.
- Cross-store/index lag while canonical visibility changes.
- Missing or partial dependency registration.
- Barrier completion with producer registry or inventory epoch mismatch.

### 5.4 Exit criteria

- Concrete deployment and transaction authority are named and reviewed by the Storage engineering owner.
- Executable D/E/Storage APIs and durable schemas are committed.
- Reader visibility is proven against the selected transaction/serialization boundary.
- All deterministic races and fault tests pass with reproducible logs and environment identity.
- Restore/failover cannot expose a forgotten or incompletely registered artifact.
- I confirms the final PermissionEpoch/revocation predicate and global completion inventory requirements.

Until all criteria pass: **Runtime Forget End-to-End Closed = NO**.

## 6. Workstream 4 — C/F/G/H/D/E/I executable conformance

The CFG-01..20 and PI-01..08 matrices remain specified, not executed. The next test package must add:

- Stable fixture IDs and typed identity/scope.
- Initial and expected ContextVersion, DeliveryId/AttemptId, PermissionEpoch, ForgetFenceGeneration and CapabilityEpoch.
- Canonical lineage and producer work identity.
- Controlled concurrency latches that force each required serialization order.
- Expected states and explicitly forbidden states.
- Evidence sinks for C submission proof, H ACK, G Applied receipt, F final-return decision, D fence and Storage visibility receipt.
- Build SHA, schema version, database/configuration identity and test runner version.
- Reproducible test commands and raw logs.
- Owner sign-off for the semantics they own.

A test is Passed only when the raw evidence is available, reproducible, and reviewed by the relevant owner. A green unit test without race/fault coverage does not close a linearizability claim.

## 7. Governance and dependency order

The closure sequence is:

1. **C/G/H** — freeze Applied evidence, wire/ACK, capability and reconnect mapping; obtain D/I predicate confirmation.
2. **B/I/H** — freeze typed identity, issuer trust, delegation, Scope/Environment and PermissionEpoch semantics.
3. **D/E/Storage** — implement and prove the already-decided logical linearization architecture.
4. **F/G/C/H** — implement final disclosure, context invalidation/reconnect and evidence acceptance against frozen upstream contracts.
5. **All affected owners** — execute conformance and adversarial suites; record owner-specific results.
6. **I + D/E/Storage + A** — close producer/recipient/backup inventory, global Forget completion and operational governance.

Parallel work is allowed only where dependencies are explicit. No downstream implementation may silently invent or freeze an upstream field.

## 8. A integration control ledger

A maintains one row per finding with these mandatory fields:

| Field | Requirement |
|---|---|
| Finding ID | Stable identifier; never recycle |
| Owner(s) | Exact authority owner(s), not merely contributors |
| Required artifact | Exact path and version/blob SHA |
| Branch baseline | Branch name and observed HEAD |
| Decision | Proposed / Owner-Decided / Rejected / Superseded |
| Evidence | Test ID, raw evidence location, build/deployment identity |
| Blocker | Exact missing decision, artifact, implementation or proof |
| Exit predicate | Objective condition for closure |
| Status | OPEN / BLOCKED / NOT RUN / IMPLEMENTED / VERIFIED / CLOSED |
| Last checked | Timestamp and baseline freshness |

A may update integration findings and this plan. A must not edit owner-owned contracts to simulate approval.

## 9. Current integration findings and target states

| Finding | Owners | Current state | Closure condition |
|---|---|---|---|
| Applied evidence/wire/capability agreement | C/G/H + D/I/B | SEMANTIC DECISIONS RECORDED WITH EXCEPTIONS; NOT FROZEN | H versioned wire package; I governance approval; D executable ordering proof |
| Typed identity and Scope/Environment mapping | B/I/H | B SEMANTICS ACCEPTED WITH EXCEPTIONS; I POLICY BLOCKED | I trust/registry approval, Scope/Environment grant governance and negative tests |
| Physical Forget linearization and visibility | D/E/Storage | LOGICAL DECISION MADE; IMPLEMENTATION NOT VERIFIED | Concrete transaction authority, executable implementation and fault proof |
| Runtime retrieval/context invalidation | C/F/G/H + D/I | SPECIFIED; TEST NOT RUN | Executed deterministic races and owner-reviewed evidence |
| Prompt injection and provenance safety | B/C/F/G/I | SPECIFIED; TEST NOT RUN | PI-01..08 and extended identity/scope cases pass |
| Global Forget operational completion | D/E/Storage/I | BLOCKED | Complete producer/recipient/replica/backup inventory and durable completion proof |

## 10. Reporting rules

Every A report update must state:
- Exact branch HEADs observed and when.
- Exact owner artifact path and blob SHA.
- Which approvals are explicit and which are absent.
- Tests specified, executed, passed and failed separately.
- Implementation/deployment evidence separately from design decisions.
- Whether the branch was changed, merged or merely read.
- Remaining blockers and objective next actions.

Do not use “closed”, “complete”, “atomic”, “secure”, “fully applied” or “erased” as an unqualified claim without naming the evidence and scope that supports it.

## 11. Immediate next actions

1. Refresh C/G/H/B/I/D/E/Storage branch tips and re-read their current Phase 3.6 artifacts; retain exact artifact Blob SHAs.
2. Publish an owner-specific decision request for the C/G/H mapping package, preserving all current Candidate states until explicit approval.
3. Publish the B/I/H field-mapping and negative-test request.
4. Convert the D/E/Storage implementation gap into a deployment/evidence checklist with the Storage engineering owner.
5. Update the A integration control ledger only from observed branch and test evidence.

**No branch merge is authorized by this plan. No owner approval is implied by its publication.**


## 12. Phase 3.6.2 control-plan reconciliation

The C/G/H package decision request has received explicit same-version decisions: C, G and H each recorded APPROVE WITH ENUMERATED EXCEPTIONS against A package Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`. B separately accepted typed-reference semantics with exceptions; D confirmed D-owned fence/lineage semantics; I explicitly recorded CANDIDATE / NO APPROVAL.

The next closure order is now:
1. I governance: obtain formal issuer/Principal/delegation and PermissionEpoch policy approval, including the currentness/freshness and revocation effective-point protocol; until then the Applied authorization predicate remains blocked.
2. H wire: pin the exact versioned Applied/ACK schema, requiredness registry profile, integrity/canonicalization/replay and reconnect/receiver-ordering behavior; then cross-check against the accepted semantic mapping.
3. D/E/Storage: implement and prove the already-decided registration/fence/dependency/publication linearization with crash/failover/restore race evidence; D semantics alone do not close CR-P1-01.
4. C/F/G/H and I/D: build deterministic shared fixtures and execute CFG/PI plus H36/I36/D36/DE-S suites with raw reproducible logs and owner review.
5. A: update the integration control ledger only from exact owner artifact versions and evidence; no branch merge is authorized.

No Owner approval is implied by A's synthesis. No test is passed by specification or static review. Applied Contract Frozen and Runtime Forget End-to-End Closed remain **NO**.


## 13. Phase 3.6.3 live reconciliation — CGH-APPLIED-1.0 exact-version decisions

Observed Owner-branch readbacks on 2026-11-16. This addendum supersedes stale process-status statements in §12 for the C/G/H Applied workstream; it does not alter the separately pinned A decision package.

### Exact shared package and Owner decisions

- A decision package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`
- Common contract: **CGH-APPLIED-1.0**

| Owner | Branch | Owner artifact | Readback Blob SHA | Decision |
|---|---|---|---|---|
| C | `session-c-agent-integration-2026-11-16` | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | APPROVE WITH ENUMERATED EXCEPTIONS |
| G | `session-g-memory-context` | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `5406b3f2558daa3f5915f6bb46e808be8d90d3ca` | APPROVE WITH ENUMERATED EXCEPTIONS |
| H | `session-h-bmcp-protocol` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `1ea5dccdf2d965103b1a8474b79f00810f639187` | APPROVE WITH ENUMERATED EXCEPTIONS |

C approves its final-request evidence and lifecycle clauses; G approves its Context/Delivery/Applied predicate, commit/idempotency and historical/current-use split; H approves its transport, authenticated binding, wire evidence and reconnect clauses. Each Owner explicitly pins the same A package Blob above. These are independent Owner decisions, not A's inferred approvals.

### H versioned wire profile

H now records **`bmcp.applied-ack / 1.0.0`**, protocol major 1/minor 0, associated with CGH-APPLIED-1.0. The H artifact defines the envelope; Delivery, Materialization, Final Request Submission, Applied ACK, Forget Action ACK, Capability Negotiation, Reconnect and ACK Receipt message families; ACK/result vocabularies; idempotency namespace and receiver sequence; canonicalization and SHA-256 digest requirements; and TLS 1.3 exporter channel binding.

H explicitly marks this **SCHEMA CANDIDATE 1.0.0 / OWNER-DECIDED FOR CGH-APPLIED-1.0**, not production freeze or deployed interoperability. Exact signature/MAC suite, key custody, rotation and compromise policy require I/Security review before production activation. H36 suites remain SPECIFIED / NOT RUN.

### Remaining authority and acceptance gates

1. **I:** PermissionDecision/PermissionEpoch issuer, currentness and revocation ordering must be confirmed for this Applied gate; external I36-GOV-01..10 remain GOVERNANCE-BLOCKED. H cryptographic/key lifecycle approval is also pending I/Security.
2. **D:** ForgetFence token, source-lineage coverage and authoritative ordering proof remain D-owned; the C/G/H decisions do not substitute for D confirmation or executable proof.
3. **B:** B's ActorRef/ScopeRef/EnvironmentRef semantic mapping is approved (formal artifact Blob `729a706860b1259115816265e847a29683c3c233`); exact consumer field mapping remains owner-specific and is not a wire-format approval.
4. **Runtime and conformance:** C-FR-01..12, CGH-01..20 and H36 cases remain SPECIFIED / NOT RUN. No deployed interoperability, implementation verification, test PASS, global Forget completion or physical erasure is claimed.

### A integration disposition

- C/G/H exact-version Owner decisions: **RECORDED WITH ENUMERATED EXCEPTIONS**.
- H schema: **OWNER-DECIDED CANDIDATE 1.0.0; NOT PRODUCTION-FROZEN**.
- Applied Contract Frozen: **NO** pending I/D authority confirmations, I/Security crypto approval, cross-owner field-level reconciliation and executable conformance.
- Test Executed / Passed: **NO / NO**.
- Implementation Verified: **NO**.
- No branch merge is authorized.

The exact A decision package Blob SHA `122b164bcc0760b83bf555072a36fc55631623e1` is deliberately not changed: changing it would invalidate the common-version pin and require fresh explicit decisions from C, G and H.


### 13.1 I technical confirmation evidence — exact-package scope distinction

A re-read I's formal PermissionEpoch/authorization confirmation on `session-i-security-governance-2026-11-16`:

- Artifact: `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md`
- Readback Blob SHA: `bae6a24fe3a374bc816993979a8fa9af52517dea`
- I explicitly confirms PermissionEpoch authority/domain/monotonicity/currentness, epoch advancement and invalidation, complete authorization tuple, no offline lease/stale-epoch grace, revocation effective point, and protected-operation race semantics.
- It explicitly keeps external governance activation/approval BLOCKED and implementation/conformance NOT VERIFIED / NOT RUN.

This is strong I-owned technical consumer-contract evidence, but the artifact does not pin A's exact C/G/H package Blob `122b164bcc0760b83bf555072a36fc55631623e1` as an Issue #3 decision. Therefore A records **I technical semantics CONFIRMED; exact Issue #3 package disposition NOT RECORDED**. No exact-package approval is inferred. I36-GOV-01..10 remain GOVERNANCE-BLOCKED.


## 13.2 I / D / B Owner-branch authority confirmations — CGH-APPLIED-1.0

The earlier I-only exact-version note is superseded by this current branch-aware reconciliation. The exact common A package remains unchanged:

- Contract: `CGH-APPLIED-1.0`
- Package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`

Exact-version authority records have been committed to the respective Owner branches and read back. These records formalize the delegated Owner-scope decisions and their limits; they are not external governance signatures or production acceptance.

| Owner | Decision | Owner artifact | Readback Blob SHA | Commit |
|---|---|---|---|---|
| I | APPROVE WITH ENUMERATED EXCEPTIONS — I authorization semantics only | `09-security-governance/phase-3.6-cgh-applied-1.0-i-authority-confirmation.md` | `8004b0f21e523b203ae36870fe88a25f977e70fa` | `cc3cdc2e8d3a50be7551087f12d6fb4d6ce0d6f3` |
| D | APPROVE WITH ENUMERATED EXCEPTIONS — D ForgetFence/lineage semantics only | `03-memory-brain/phase-3.6-cgh-applied-1.0-d-forget-fence-authority-confirmation.md` | `b5a0354d263185723954ffb952fdf0b005f59ba8` | `302b9fc09e040db7ef32c56e39bd91272cc1abb9` |
| B | APPROVE — B semantic types and role mapping only | `02-domain-model/phase-3.6-cgh-applied-1.0-b-typed-reference-authority-confirmation.md` | `483f68f074348fda8eeb965a0b43143ae242337d` | `026e52c72bd8bdb65b63bdd77f25d925e0624f9f` |

### Confirmed authority boundaries

- **I:** PermissionEpoch authority/currentness, complete authorization tuple, default-deny, revocation effective point and commit-versus-revocation semantics are confirmed. I36-GOV-01..10 remain externally GOVERNANCE-BLOCKED. Signature/MAC suite, key custody and production conformance are not approved.
- **D:** ForgetFence namespace, target/source/ancestor lineage, fence-first ordering and ambiguous-order fail-closed semantics are confirmed. A production causal bridge proving C's actual submit boundary against D's fence remains OPEN; wall-clock timestamps alone are insufficient.
- **B:** ActorRef, role-preserving ScopeRef, EnvironmentRef orthogonality and no implicit string coercion are confirmed. Consumer wire paths, H serialization and registry authority designation remain outside B approval.

### Combined Applied gate disposition

- I/D/B authority-semantic confirmation for the exact CGH-APPLIED-1.0 package: **RECORDED WITH ENUMERATED SCOPE LIMITS**.
- C/G/H exact-version decisions: **RECORDED WITH ENUMERATED EXCEPTIONS**.
- H `bmcp.applied-ack/1.0.0`: **OWNER-DECIDED SCHEMA CANDIDATE; NOT DEPLOYED INTEROPERABILITY**.
- C-submit / D-fence causal proof: **OPEN / NOT ESTABLISHED**.
- External I governance approval: **BLOCKED**.
- CGH/I36/H36 tests: **NOT RUN**; implementation: **NOT VERIFIED**.
- Applied Contract Frozen: **NO** until remaining exceptions, concrete wire/receipt mapping and causal proof are closed and A revalidates all exact artifact versions.
- Issue #3 remains open. No branch merge is requested or authorized.


## 13.3 C / I / D cross-authority causal-order bridge — proposal issued, decisions pending

A published an integration-level proposal for the unresolved C final-submit / I PermissionEpoch-revocation / D ForgetFence ordering gap:

- Proposal: `reviews/integration/phase-3.6-cgh-applied-cross-authority-causal-ordering-proposal.md`
- Proposal Blob SHA: `6c858583aac8769d241a2bc53b026b972e65f91a`
- Exact common package remains `CGH-APPLIED-1.0`, Blob `122b164bcc0760b83bf555072a36fc55631623e1`.
- Issue #3 request for explicit C/I/D/G/H responses: comment `6919903078`.

The proposal defines a candidate durable shared ordering gate with owner-controlled I and D transition events and C's two-phase final-submit reservation/terminalization:
- `SUBMIT_WON` requires the actual provider-issued success receipt and exact request digest.
- `ABORTED` requires definitive no-handoff proof.
- `IN_DOUBT` is fail-closed and cannot promote Full Applied.
- I retains authorization/PermissionEpoch authority; D retains ForgetFence/lineage/barrier authority; C retains final-submit evidence authority; G alone commits Applied; H transports opaque evidence only.

This is an **A integration proposal only**. It is not an approved architecture, does not establish that a coordinator exists, and does not authorize modifications to I/D/C/H owner contracts. C, I and D must each explicitly accept, amend or reject the exact proposal Blob. G must confirm the minimum evidence consumed by Applied commit.

### H schema evidence reconciliation — conflicting records, freeze remains blocked

A re-read H's exact-version decision artifact:
- `08-bmcp-protocol/phase-3.6-cgh-applied-contract-exact-version-h-owner-decision.md`
- Blob SHA: `c0e10966e8dd95a9d1f5b1dfa156cb4b098b26e0`

That current H decision explicitly says the concrete versioned BMCP Applied/Delivery schema is **OPEN / NOT FROZEN / NOT YET DELIVERED**, with H-EX-01 outstanding. It requires schema IDs, exact field names/types/requiredness, separate Forget ACK and Applied families, canonicalization, replay, cryptographic profile and capability/reconnect mapping.

Earlier Issue #3 coordination comments and A's previous plan described `bmcp.applied-ack/1.0.0` as an owner-decided schema candidate. The current H branch tree inspected for this reconciliation does not expose a separately published concrete `bmcp.applied-ack/1.0.0` schema artifact. This is a **source-record discrepancy**, not grounds to infer that the schema never existed. H is asked to identify the authoritative artifact and Blob SHA or confirm that H-EX-01 remains undelivered. Until reconciled, the conservative gate is **CONCRETE H WIRE SCHEMA OPEN / NOT FROZEN**.

I's exact-version confirmation separately requires an I CommitAuthorizationReceipt reference and I sequencer terminal-order proof to be explicitly mapped at the protected owner-final-gate. The H schema reconciliation must include those opaque evidence references and conditional requiredness; H must not mint or validate I/D authority.

### Current disposition

- C/I/D shared causal order: **PROPOSAL ISSUED / OWNER DECISIONS PENDING**.
- Production coordinator: **NOT APPROVED / NOT IMPLEMENTATION-VERIFIED**.
- H concrete versioned schema and I receipt mapping: **OPEN; authoritative artifact reconciliation required**.
- Applied Contract Frozen: **NO**.
- CGH/I36/H36 tests: **NOT RUN**; implementation: **NOT VERIFIED**.
- No branch merge or architecture freeze authorized.


## 13.4 C / D / I owner causal-order contracts published — successor version proposed

After the A proposal was published, fresh Owner-branch reads found three new, independently authored contract addenda:

| Owner | Artifact | Blob SHA | Owner status |
|---|---|---|---|
| C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `543d04e10a95d1f5720c3da8050befe6d21cd0c6` | C-side contract specified; coordinator deployment and cross-owner acceptance OPEN |
| D | `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` | `317a9bc170c5a66720f738bf24bbf93c87385887` | D-side fence/barrier contract specified; coordinator/Storage deployment and cross-owner acceptance OPEN |
| I | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | `8a9d418593c7d6be12f072ec8eeb0b3a56eb4be8` | I-side receipt/ordering contract specified; service deployment, external governance and cross-owner acceptance OPEN |

All three target:
- `CausalOrderProfile/1.0`
- H schema `bmcp.applied-ack/1.1.0`
- proposed successor common package `CGH-APPLIED-1.1`

This is a meaningful advance from a proposal-only state: C/D/I have independently specified compatible participant-reservation, receipt, barrier and fail-closed semantics. It is **not** cross-owner acceptance, deployment selection, implementation or test evidence. The original `CGH-APPLIED-1.0` package and its approvals remain pinned to Blob `122b164bcc0760b83bf555072a36fc55631623e1`; do not silently relabel those approvals as approval of 1.1.

### Integration reconciliation still required before 1.1 can be baselined

1. **Version transition:** A must create/pin an explicit `CGH-APPLIED-1.1` successor package before any 1.1 acceptance. C/D/I addenda are not themselves a shared package or a freeze.
2. **Participant/receipt sequencing:** C's numbered sequence requests an I receipt before participant registration, while I requires the receipt to bind a ParticipantReservationRef or a pre-bound reservation nonce finalized before provider side effect. C/I/D must specify one deterministic issuance/registration/consumption order and its crash recovery.
3. **Terminal semantics:** I's `COMMIT_WON` is the I sequencer outcome for the exact protected owner gate, not proof that the provider actually accepted the request. C's provider receipt and CSubmitOutcomeRef remain separately required before C may emit Final Request Submitted. G must consume both without conflating them.
4. **Barrier coupling:** D keeps the participant/fence barrier open through unknown provider outcome and requires compatible I terminal evidence. I keeps revocation pending behind unresolved reservations. The common coordinator must prove these two barriers are the same durable transaction/reservation identity across failover/restore; no owner-local receipt alone is enough.
5. **H:** Current H exact-version decision Blob `c0e10966e8dd95a9d1f5b1dfa156cb4b098b26e0` still says concrete wire schema is OPEN / NOT DELIVERED. H must publish the actual `bmcp.applied-ack/1.1.0` schema, including I CommitAuthorizationReceiptRef, IAuthorizationTerminalRef, DParticipantClearanceRef, ParticipantReservationRef, CSubmitOutcomeRef and CausalOrderTerminalProofRef, with exact conditional requiredness and authority mapping.
6. **G:** G must explicitly accept the new terminal evidence and Full Applied predicate for 1.1. B's semantic type confirmation for 1.0 is not automatically an exact-version acceptance of a 1.1 package.
7. **Storage/coordinator:** C/D/I specifications all leave coordinator deployment, durable participant registry, HA/failover/restore and production transaction integration open. These remain implementation blockers.

### Updated status

- C/D/I owner-side causal-order contract specifications: **PUBLISHED / READ BACK**.
- Cross-owner acceptance of `CausalOrderProfile/1.0`: **OPEN**.
- `CGH-APPLIED-1.1` common package: **PROPOSED / NOT YET BASELINED**.
- H `bmcp.applied-ack/1.1.0`: **NOT YET DELIVERED / NOT FROZEN**.
- G acceptance of 1.1 evidence mapping: **OPEN**.
- Coordinator/participant implementation and conformance: **NOT VERIFIED / NOT RUN**.
- Original `CGH-APPLIED-1.0` remains **NOT FROZEN**; no approval is transferred to 1.1.


## 13.3 C-submit / I-authorization / D-ForgetFence causal-order architecture — 2026-11-16

This addendum addresses the previously open cross-authority causal bridge. It does not rewrite the immutable CGH-APPLIED-1.0 package or retroactively extend its Owner approvals. The proposed successor is **CGH-APPLIED-1.1**, with H profile **`bmcp.applied-ack/1.1.0`** and shared ordering profile **`CausalOrderProfile/1.0`**.

### 13.3.1 Architecture resolution

Independent I PermissionEpoch and D ForgetFenceGeneration sequences cannot be compared, and neither wall-clock time nor H receiver sequence proves the order of C's actual provider submit. The selected architecture is a **pre-side-effect participant-intent + owner-terminalization + participant-barrier protocol**:

1. C freezes the exact final request and digest, then obtains a durable `ParticipantIntentRef` from a common `CausalOrderCoordinator` before invoking the provider/runtime. Intent is not authorization.
2. I consumes a single-use `CommitAuthorizationReceipt` bound to the intent, exact authorization tuple, request digest and final boundary. I's own sequencer decides authorization-versus-revocation. If revocation wins, C aborts. If authorization wins, later revocation effectiveness is held behind this unresolved participant until its exact outcome is terminal.
3. D binds the same intent to the exact ForgetOperation/Fence and complete target/source/ancestor lineage. If a fence was already effective, fence wins. A later fence remains pending behind the unresolved participant until submit outcome or safe abort is durably terminal.
4. The coordinator validates the I and D owner-issued terminal/clearance evidence and finalizes a `ParticipantReservationRef`. Only then may C invoke the provider/runtime.
5. C records the actual provider/runtime outcome under that reservation. The coordinator emits a terminal proof binding C submit outcome, I receipt/terminal order, D fence/lineage/participant clearance and the coordinator's durable order.
6. A provider outcome that cannot be determined remains `IN_DOUBT`; the participant is not silently expired, retried as a new operation, or cleared. D/I barriers remain open until authoritative reconciliation.

This protocol preserves authority separation: I remains the only authorization/PermissionEpoch authority; D remains the only ForgetFence/lineage authority; C remains the only producer of actual submit evidence; the coordinator supplies durable cross-authority order and participant accounting only; H transports and integrity-binds evidence; G alone decides Applied/current-use.

### 13.3.2 Exact Owner artifacts and readback

| Owner | Owner-branch artifact | Readback Blob SHA | Commit | Status |
|---|---|---|---|---|
| C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `f2c5b379cacfedd81500e8496d3053b628e144a` | `8f017a5a17620c21f3e7f0075a087c4b098baa8e` | C-side contract specified; cross-owner acceptance pending |
| I | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | `71779133a4f95d63a24c4c7e606af174763366f1` | `2fb2bb9653350e83ebf2a6a56195a762d112189f` | I receipt/terminalization contract specified; governance/deployment pending |
| D | `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` | `317a9bc170c5a66720f738bf24bbf93c87385887` | `c0d51b3cc61f182a69632f008c43650e14c213ef` | D participant/fence barrier contract specified; deployment pending |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `5cbf0bb548a46671054cb22c6fab3c3d007365d4` | `f5ecd8e649efb578a06cedfa5a5dbd4f8c7bc84a` | H schema candidate 1.1.0 specified; not production-frozen |

### 13.3.3 H 1.1.0 schema additions

H's `bmcp.applied-ack/1.1.0` candidate adds typed references for:
- CausalOrderProfileRef, CausalOrderCoordinatorRef, CausalOrderTransactionRef, CausalOrderPosition and ParticipantIntentRef/ParticipantReservationRef;
- I CommitAuthorizationReceiptRef and IAuthorizationTerminalRef;
- D ForgetFenceRef, ForgetLineageCoverageRef and DParticipantClearanceRef;
- CSubmitOutcomeRef and CausalOrderTerminalProofRef.

It adds message families `CAUSAL_ORDER_INTENT`, `CAUSAL_ORDER_INTENT_RECEIPT`, `CAUSAL_ORDER_RESERVATION`, `I_AUTHORIZATION_TERMINAL`, `D_FENCE_TERMINAL`, `C_SUBMIT_OUTCOME`, `CAUSAL_ORDER_TERMINAL_PROOF` and `CAUSAL_ORDER_ACK`. H transports these opaque owner-issued references and does not mint or semantically decide them. 1.0.0 remains historical/transport evidence only and is insufficient for Full Applied claims requiring this three-authority proof.

### 13.3.4 Unresolved operational authority and gates

The architecture resolves the protocol-level causal-order design, but the **common coordinator is not yet concretely designated, deployed or accepted**. Its operator, durable store, HA/failover, retention, restore fencing, signing/key trust, participant recovery and service SLO must be named and approved by C, I, D and the relevant Storage/operator owner. The coordinator must not become a shadow authorization or Forget authority.

Required next gates:
1. C, I, D and H explicitly accept the same `CausalOrderProfile/1.0` and `bmcp.applied-ack/1.1.0` exact artifact versions; G must accept the resulting Applied evidence/current-use predicate; Storage/operator must accept the coordinator durability/restore design.
2. Specify coordinator API, durable schema, idempotency, participant recovery and monotonic restore/failover behavior.
3. Run C-CO, I-CO, D-CO and H36-CO deterministic races, including both orders, unknown provider outcome, coordinator crash/restore, lost receipt, duplicate and conflicting terminal proof.
4. Attach build/schema/deployment identity and raw reproducible logs; no test pass is implied by specification.

Current state:
- Cross-authority causal-order protocol: **SPECIFIED / OWNER-BOUND DRAFTS RECORDED**.
- C/I/D/H successor-profile exact-version acceptance: **PENDING**.
- Coordinator deployment/Storage acceptance: **OPEN**.
- C-submit/I-revocation/D-fence production ordering proof: **NOT YET VERIFIED**.
- C-CO/I-CO/D-CO/H36-CO tests: **SPECIFIED / NOT RUN**.
- Applied Contract Frozen: **NO**.
- Implementation Verified: **NO**.
- Issue #3 remains open; no branch merge is authorized.


## 13.5 A exact successor package created — CGH-APPLIED-1.1 candidate

A created and read back the explicit successor package:

- Path: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Blob SHA: `07a403f89f8d5bf50fc76f139371fa1fd6e4eca3`
- Commit: `c121df7c4c398da2da27e5a5a60d488e57ee321a`
- Profile: `CausalOrderProfile/1.0`
- H schema target: `bmcp.applied-ack/1.1.0`

The package integrates C/I/D participant-intent, I single-use receipt consumption, D fence/lineage clearance, durable reservation, actual C provider outcome and common terminal proof. It explicitly separates I COMMIT_WON from actual provider success and keeps G as sole Applied committer.

This is **A CANDIDATE / OWNER REVIEW REQUIRED / NOT FROZEN**. It does not alter the CGH-APPLIED-1.0 package or transfer any 1.0 approval. Required next decisions: exact-version accept/amend/reject by C/D/I/H/G/B; named coordinator/Storage operator acceptance; then implementation and reproducible conformance.

### Corrected latest Owner artifact pins

The latest branch readbacks supersede the earlier C/I hashes recorded in the first discovery note:
- C `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`: Blob `f0839e4f470588e6053c144b91ff318b6465e04c`, commit `96054e879abbd827f36ea8b766aa7ccaa4defef1`.
- I `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md`: Blob `71779133a4f95d63a24c4c7e606af174763366f1`, commit `2fb2bb9653350e83ebf2a6a56195a762d112189f`.
- D `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md`: Blob `1c60e7129c5b4255d6b9033bcb03e28e43b3b5af`, commit `99e13c308fe784508b70a48bea694493c00c12b2`.
- H `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`: Blob `a23b9a879a3ec0e212645a8247a6797bd0055360`, commit `ceb20c0aa0318e2c4c82f7ffb90b05432bd87255`. It now contains the `bmcp.applied-ack/1.1.0` schema candidate and message/field mapping; it remains NOT PRODUCTION-FROZEN / NOT DEPLOYED.

The earlier H exact-version decision artifact for CGH-APPLIED-1.0 remains valid for 1.0 only. Its H-EX-01 schema exception is superseded for the 1.1 candidate by the new H 1.1.0 candidate section, but the new schema is still not a production freeze and still requires exact 1.1 package acceptance and conformance.


### 13.3.5 Request-cutoff ordering refinement

The common coordinator log must also order the *request* points, not only terminal completion:
- D fence request is recorded with `DForgetFenceRequestRef` and a coordinator cutoff position. Any affected ParticipantIntentRef after that cutoff is rejected immediately, even if D's effective fence commit is delayed while earlier participants drain. D terminal evidence carries both request cutoff and effective positions.
- I revocation request is recorded with `IRevocationRequestRef` and a coordinator cutoff position. It immediately blocks new receipts/authorizations in the affected domain. If it precedes intent or receipt consumption, it wins; if I has already terminalized a receipt as COMMIT_WON, effective PermissionEpoch advancement waits behind that unresolved participant. I remains the authority for the actual epoch advance.
- The coordinator's common order is evidence of causality only. It does not issue I PermissionEpoch, D ForgetFenceGeneration, or owner terminal decisions.


## 13.6 CGH-APPLIED-1.1 cutoff-order refinement and current Owner pins

The 1.1 candidate now explicitly distinguishes **request/cutoff position** from **effective transition position** for both I revocation and D ForgetFence:

- I's `IAuthorizationTerminalRef` binds the applicable `IRevocationRequestRef` and cutoff position, or explicitly records that no earlier revocation request existed. A revocation request before ParticipantIntentRef blocks admission; a revocation request after intent but before receipt consumption may still win; after I `COMMIT_WON`, later revocation waits behind the unresolved participant.
- D's `DParticipantClearanceRef` binds `ParticipantIntentRef`, complete lineage and inventory version. `DForgetFenceRequestRef` cutoff and eventual `ForgetFenceRef` effective position are distinct. A fence request before intent rejects that intent even while the effective fence is draining earlier participants; an intent before the fence request is tracked in the barrier.
- C remains the only authority for actual provider success. I `COMMIT_WON` and D clearance do not prove provider handoff. CSubmitOutcome and the common terminal proof are both required before G may consider Full Applied.

The A candidate package was updated and its latest Blob is now:
- `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Blob SHA: `471c8ce86e93c036ad9a58a77d45d9daa0ab8af8`
- Commit: `78adae653730c740a9a711c3550b8094f0faa786`

Current Owner artifact readbacks supersede prior hashes:
- C: `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, Blob `f2c5b379cacfedd81500e8496d3053b628e144a0`, branch HEAD `8f017a5a17620c21f3e7f0075a087c4b098baa8e`.
- D: `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md`, Blob `317a9bc170c5a66720f738bf24bbf93c87385887`, branch HEAD `c0d51b3cc61f182a69632f008c43650e14c213ef`.
- I: `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md`, Blob `71779133a4f95d63a24c4c7e606af174763366f1`, branch HEAD `2fb2bb9653350e83ebf2a6a56195a762d112189f`.
- H: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `5cbf0bb548a46671054cb22c6fab3c3d007365d4`, branch HEAD `f5ecd8e649efb578a06cedfa5a5dbd4f8c7bc84a`.

These are still owner-side specifications/schema candidate, not explicit acceptance of the exact A 1.1 package. G and B exact 1.1 dispositions remain pending. Coordinator/operator deployment, Storage durability/restore acceptance and conformance remain open.


## 13.7 Live CGH-APPLIED-1.1 owner decision checkpoint — 2026-11-16 23:07 +08

The exact A successor candidate remains Blob `471c8ce86e93c036ad9a58a77d45d9daa0ab8af8`. Fresh Owner-branch readbacks confirm C/D/I have specified the causal-order mechanisms and H has a `bmcp.applied-ack/1.1.0` schema candidate, but their source artifacts still describe cross-owner acceptance as open/candidate. G's recorded approval is pinned to older CGH-APPLIED package Blob `61d961c32138fd875069e8cbac4696bb031447c0`, and B's approval is limited to typed semantic mapping; neither is an exact 1.1 package decision.

A requested exact-SHA ACCEPT / ACCEPT WITH ENUMERATED EXCEPTIONS / REJECT-REVISE decisions from C/D/I/H/G/B in Issue #3 comment `6920276322`. Each decision must be committed on its own Owner branch with artifact path, Blob SHA, exceptions and commit. A must not alter Owner branches or infer acceptance from source specifications.

The coordinator/operator and production durable participant registry remain unidentified/unverified. Storage's JF-10 Python reference model is in-memory and cannot satisfy this implementation gate. HA/failover/restore, deterministic cross-authority conformance and production causal proof remain NOT VERIFIED / NOT RUN. CGH-APPLIED-1.1 is therefore CANDIDATE / NOT OWNER-DECIDED / NOT FROZEN; G8 BLOCKED, G9 NOT RUN, G10 BLOCKED.


## 13.7 Causal Order Coordinator deployment and durable recovery architecture proposal

A has published a concrete deployment/operations proposal:
- Artifact: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`
- Commit: `a3e17f4f77d980bafab4268f8825a1cd61371d6e`
- Blob: `3f302a333f413e6ea7d5cbf1fe06473be6228a09`
- Branch: `session-a-integration-2026-11-16`

### Proposed deployment profile

- One logical Causal Order Coordinator backed by one strongly consistent append-only replicated consensus log; initial deployment target is a three-voter group across three independent failure domains, quorum two, with durable quorum commit before returning a committed position.
- Storage/Consistency is proposed as infrastructure custodian for replication, snapshots, restore fencing, retention and SLO, but this is NOT a designation or acceptance. Storage Owner must name the actual service operator and approve the durability/recovery contract.
- C/I/D remain semantic authorities; coordinator only orders durable request cutoffs, participant intents, owner terminal evidence, final reservations, C outcomes and terminal proofs.
- One log is deliberately selected for v1; sharding, multi-log and multi-policy-domain atomicity remain unsupported. Missing/ambiguous causal-domain mapping fails closed.
- Unresolved/IN_DOUBT participants never expire or disappear during compaction, failover, restore or operator action.
- Restore from an unprovable/stale checkpoint enters RESTORE_FENCED; no new intents, reservations, barrier releases or Full Applied until reconciliation.
- Provider ambiguity reuses the same transaction/reservation/idempotency key; no retry-as-new-operation or heuristic commit/abort.

### Exact acceptance requests

Storage/Consistency, C, I, D, H, G and Security/Governance must accept/revise the exact proposal and profile. Storage must specifically identify actual failure-domain placement, durability class, retention, RPO/RTO, operator, key custody interfaces and restore authority. The three-voter topology is a proposed target, not a claim about existing infrastructure.

### Current gate state

- Coordinator deployment architecture: **PROPOSED / A ARTIFACT COMMITTED AND READBACK VERIFIED**.
- Named operator / actual infrastructure: **NOT DESIGNATED**.
- Storage/Consistency durability and restore acceptance: **PENDING**.
- C/I/D/H/G exact proposal acceptance: **PENDING**.
- Security/key/admin governance: **PENDING**.
- COC-01..12 and consumer race suites: **SPECIFIED / NOT RUN**.
- Production causal proof: **NOT VERIFIED**.
- Applied Contract Frozen: **NO**.


## 13.8 CGH-APPLIED-1.1 package linked to concrete coordinator profile

The exact A successor package was updated to incorporate the companion coordinator deployment proposal:
- Package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Package commit: `fd0da725bdc27bc082b4b87be142542245b5aa53`
- Package Blob: `9be466004a93697828f92bf5d932037c6478da7c`
- Companion coordinator architecture Blob: `3f302a333f413e6ea7d5cbf1fe06473be6228a09`

This is a package amendment. Any previous exact-version acceptance of the older CGH-APPLIED-1.1 package Blob does not automatically approve this amended Blob. C/D/I/H/G/B and Storage/operator must make fresh exact-Blob decisions or explicitly state which unchanged clauses their prior decision covers and approve the amended package hash.

Current status remains A CANDIDATE / OWNER REVIEW REQUIRED / NOT FROZEN; coordinator operator not designated; Storage acceptance pending; tests not run.


## 13.9 Coordinator outage cutoff safety and latest package pins

A closed an outage race in the coordinator proposal: when I receives a revocation request or D receives a fence request while COC is unavailable, that owner locally blocks affected admissions/receipt issuance and returns PENDING/UNKNOWN. Admission cannot reopen until the request cutoff is durably recorded in COC. This ensures an owner-known request cannot be invisible to the common order.

Latest readback pins:
- Coordinator deployment artifact Blob: `65878e1e2b569b1dc6d0918f51a313da122236d4`, commit `56909a979239a57d04d7c6ce2e36a4a63dd96e60`.
- CGH-APPLIED-1.1 candidate package Blob: `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`, commit `e1113c3cd84787ad087a2ebb363cde165d563f1f`.

These amendments invalidate any prior exact-Blob approval of the earlier package or coordinator artifact. Fresh exact-version Owner decisions are required. Status remains proposed/not designated/not deployed; Storage and C/I/D/H/G/Security approvals pending; tests not run; Applied Contract Frozen NO.

## CGH-APPLIED-1.1 exact Owner decision reconciliation — 2026-11-16

A independently re-read the six Owner artifacts from their respective Owner branches. Every decision below is explicitly pinned to the same exact A candidate package Blob `9808b31f840606b329f1a794935dfc9c5084d63b` (`CGH-APPLIED-1.1`, `CausalOrderProfile/1.0`, H target `bmcp.applied-ack/1.1.0`). This is not an approval transfer from 1.0.

| Owner | Exact-version decision | Owner artifact | Verified readback Blob SHA |
|---|---|---|---|
| C | ACCEPT WITH ENUMERATED EXCEPTIONS — actual provider boundary/CSubmitOutcome | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `5723dba00de54fcd73552d9b82734a8c044550ec` |
| D | ACCEPT WITH ENUMERATED EXCEPTIONS — fence cutoff, lineage and participant barrier | `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` | `744b99942cdee437b85fdde90ff61ff09c391b05` |
| I | ACCEPT WITH ENUMERATED EXCEPTIONS — single-use authorization receipt and revocation cutoff | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | `bb4987268381bcb8485276c2d4e4906fe1e20b03` |
| H | ACCEPT WITH ENUMERATED EXCEPTIONS — 1.1.0 transport/schema candidate mapping | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `6686510bb8d8265d86ce9249286de8f49d90d178` |
| G | ACCEPT WITH ENUMERATED EXCEPTIONS — 1.1 Full Applied predicate and historical/current-use split | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `a96c61fe203e9e02921d4360d6cac17ad6a7b506` |
| B | APPROVE — typed-reference semantics and role-preserving bindings | `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md` | `ac9a092b467f78f2122f4adf08d7ba445e40e927` |

### Gate interpretation and remaining blockers

- The six requested Owner decisions are RECORDED against one exact A package Blob. Each Owner retains its own enumerated authority exceptions.
- H `bmcp.applied-ack/1.1.0` remains a schema candidate, NOT production-frozen, deployed or interoperably verified; crypto/key lifecycle still requires I/Security governance approval.
- C/D/I sequencers and the common coordinator/participant registry are specifications, not verified deployed services. Accountable coordinator/Storage operator, durable store, HA/failover/restore, retention and recovery acceptance remain OPEN.
- G's decision is a contract/predicate acceptance, not proof that its validator or Applied persistence consumes the complete 1.1 evidence set.
- C-CO/I-CO/D-CO/H36-CO/G conformance remains SPECIFIED / NOT RUN. Production causal proof and implementation remain NOT VERIFIED.
- Therefore Applied Contract Frozen = NO; G8 remains BLOCKED, G9 NOT RUN, G10 BLOCKED. No branch merge or production activation is authorized.


## 13.10 COC outage recovery batch — current exact package checkpoint

The current COC architecture Blob is `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`; the current companion CGH-APPLIED-1.1 package Blob is `4961ffefc0f9920efb8425a9b2a7af42d8f64819`. The package binds the exact companion pin and adds durable I/D owner-local pending gates for requests received during COC outage, one atomic recovery-cutoff batch (without deriving cross-owner order from local clocks), enumeration of all affected pre-batch ParticipantIntentRefs, I receipt/revocation reconciliation, D lineage-barrier reconciliation and owner high-water verification before gates reopen. Missing log prefix, intent, lineage or owner proof keeps the system RESTORE_FENCED/UNKNOWN/IN_DOUBT.

Six Owner decisions exist for historical package Blob `9808b31f840606b329f1a794935dfc9c5084d63b` only: C/D/I/H/G accepted with enumerated exceptions and B approved semantic typed-reference bindings. Those approvals do not automatically cover the recovery-batch amendment. Fresh exact-Blob decisions are requested in Issue #3 comment `6920481902`; Storage's exact COC decision is requested in Issue #2 comment `6920482983`.

Current gates: package A CANDIDATE / FRESH OWNER REVIEW REQUIRED / NOT FROZEN; coordinator proposal NOT DESIGNATED / NOT DEPLOYED; Storage operator/durability and Security/key governance PENDING; COC-01..16 and C/I/D/H/G consumer conformance NOT RUN; production causal proof NOT VERIFIED. G8 BLOCKED, G9 NOT RUN, G10 BLOCKED.


## 13.10 Exact CGH-APPLIED-1.1 Owner decision reconciliation — 2026-11-16

The current immutable candidate remains `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`, Blob `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`. Do not edit that candidate in place after Owner decisions; any amendment creates a new candidate SHA and requires fresh decisions.

All six authority owners have now recorded a fresh decision against that exact same candidate Blob, with Owner-branch readback verified:

| Owner | Decision | Owner artifact Blob | Commit |
|---|---|---|---|
| C | ACCEPT WITH ENUMERATED EXCEPTIONS | `323a3d2ce304a77d2751544da765f6365a32279e` | `108e6969a02afadd4f8a7ef36a8c7b1f619517e0` |
| D | ACCEPT WITH ENUMERATED EXCEPTIONS | `b2ef7a235af8bef87d829a25057e50449d3a4be8` | `23864cd99abf6028c59da0c6bb422c54c2f7dc2b` |
| I | ACCEPT WITH ENUMERATED EXCEPTIONS | `d1f234cd802e86a2bf291d2cc721fb5ae7894142` | `767440eab745a161711591da6553168636a06c2d` |
| H | ACCEPT WITH ENUMERATED EXCEPTIONS | `01b102d66715b02889a8a8f59f3cc559704a9990` | `01d00d7db784051b7f2fa294038146a708fc1493` |
| G | ACCEPT WITH ENUMERATED EXCEPTIONS | `aa38af8e4917af292e66ebd21266b775f6db0215` | `159735aa4d268080f3f6c341754a4ee8a69a9167` |
| B | APPROVE — typed-reference semantics/role-preserving bindings | `504f8478ab7db3bf49fbaf778838e18e7a8a3470` | `7e81c4d521e9001d3783bc318e0e838a29a32b13` |

H's 1.1.0 schema decision now includes field encoding, common envelope requirements, per-message requiredness, conditional I revocation reference presence/explicit none state, separate D request-cutoff/effective positions, outcome-conditional provider evidence, canonicalization/digest, replay/idempotency, unknown-critical-field rejection, reconnect preservation and downgrade rejection for 1.1 Full Applied.

A recorded the exact six-owner reconciliation on Issue #3 comment `6920517731` (readback verified).

**Gate interpretation:** the six Owner contract/semantic decisions are RECORDED WITH ENUMERATED EXCEPTIONS. They do not close coordinator/Storage operator designation, durable participant store deployment, HA/failover/restore, key governance, implementation verification or conformance. C-CO/I-CO/D-CO/H36-CO/G remain SPECIFIED / NOT RUN. Applied Contract Frozen = NO; implementation verified = NO; G10 = BLOCKED. No merge or production activation is authorized.


## 13.11 Storage Owner decision recorded — architecture interface accepted with changes

Storage has issued a formal exact-Blob decision: `CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY`.

Decision artifact `reviews/storage-consistency/phase-3.6-coc-storage-boundary-acceptance.md`, Blob `a589d983ac145244962c22e5da3a55427aa35ff8`, on Storage Owner branch `session-storage-consistency-forget-atomicity-2026-11-16` (HEAD/commit `7b83e61c44dd4b67fa2059a3bff83d453aeaf757`). It reviews exact A COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` and exact CGH package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.

The accepted boundary is three distinct authorities: (a) COC cross-authority causal-order ledger; (b) I policy-domain sequencer plus I-approved JF-10 owner-gate participating prepared transaction/2PC; and (c) one durable serializable (or proven equivalent) per-Canonical-Memory-Authority Storage transaction for D work/fence/dependency/final visibility/VisibilityPointer/PublicationReceipt/terminal disposition/outbox. Object bytes remain private until Storage's authoritative visibility transaction commits. Outbox and COC messages are notification/reconciliation evidence only. No cross-domain atomicity or publication is inferred from COC position, reservation, copied receipt or terminal proof.

**Remaining hard blockers:** no named COC operator or actual infrastructure owner; actual voter/failure-domain/quorum/media implementation unverified; snapshot/rollback/total-loss restore unverified; operational retention, RPO/RTO, SLO, residency, KMS and escalation open; Canonical Authority DB product/isolation/HA/prepared-XID unselected; I's exact JF-10 2PC/COC bridge blocked; combined COC+JF-10+Storage visibility atomicity unproven; production code/tests not verified/run. Storage expressly says activation NOT AUTHORIZED and Applied Contract Frozen NO.

Accordingly mark **Storage architecture-interface acceptance = CONFIRMED WITH CHANGES**, but keep Storage deployment/durability acceptance = OPEN, G8 BLOCKED, G9 NOT RUN, G10 BLOCKED. This decision is pinned only to the exact A SHAs above; any later A amendment requires fresh Storage review.

## 13.11 Current CGH-APPLIED-1.1 recovery-batch exact decisions and Storage boundary — 2026-11-16

Current A candidate and companion profile:
- CGH-APPLIED-1.1 package Blob: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.
- Causal Order Coordinator architecture Blob: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- Profile: `CausalOrderProfile/1.0`; H schema target: `bmcp.applied-ack/1.1.0`.

All six semantic owners have now independently recorded a fresh decision against the exact 4961 package and fc3 COC companion, with Owner-branch readback verified:

| Owner | Decision on recovery-batch amendment | Current Owner artifact Blob |
|---|---|---|
| C | ACCEPT WITH ENUMERATED EXCEPTIONS | `a72a3eb1e5207f67c01f804508311f42db9a6e0a` |
| D | ACCEPT WITH ENUMERATED EXCEPTIONS | `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` |
| I | ACCEPT WITH ENUMERATED EXCEPTIONS | `5a5304d48aa912dcf6f817099bd5659371d8cdc8` |
| H | ACCEPT WITH ENUMERATED EXCEPTIONS — wire mapping still needs addendum | `22853b21d583d2cae75eb3ef1c580c68b4cf4c70` |
| G | ACCEPT WITH ENUMERATED EXCEPTIONS — recovery evidence required for Full Applied | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| B | APPROVE — no new B semantic type introduced | `3a1e77889cd9a90cd5822d9f0cb3437880868706` |

Storage/Consistency also published exact COC/package review:
- Decision: **CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY**.
- Artifact: `reviews/storage-consistency/phase-3.6-coc-storage-boundary-acceptance.md`.
- Blob: `a589d983ac145244962c22e5da3a55427aa35ff8`; commit `7b83e61c44dd4b67fa2059a3bff83d453aeaf757`.
- Storage readiness addendum Blob: `445cdf31832f5ac914ff39d6c90801e6e1931fbc`.

### Binding constraints / open gates

- COC is a cross-authority causal-order ledger, not the Canonical Memory Authority VisibilityPointer/PublicationReceipt transaction and not I's policy-domain sequencer/JF-10 2PC coordinator.
- Storage's per-Canonical-Memory-authority serializable visibility transaction remains separate. I's owner-gate-participating JF-10 protocol and any COC↔JF-10 bridge remain BLOCKED until I specifies/approves exact composition and C/D/Storage accept it.
- H accepts recovery semantics but exact wire field names, message requiredness and canonicalization for every recovery-batch evidence item remain an H schema addendum requirement. 1.1.0 is not production-frozen.
- Actual COC operator, infrastructure, voter/failure-domain placement, DB engine/version/isolation, prepared-XID capability, RPO/RTO, SLO, retention, restore, encryption/KMS and key governance remain OPEN / NOT VERIFIED.
- COC-01..16, JF10-01..17, Storage C01..C23 and consumer conformance remain SPECIFIED / NOT RUN. Reference model is in-memory only; no production implementation verified.

**Current gate:** exact 1.1 recovery-batch semantic owner decisions = RECORDED WITH ENUMERATED EXCEPTIONS; Storage COC interface = CONFIRMED WITH CHANGES. Applied Contract Frozen = NO; production coordinator/operator = NOT DESIGNATED; combined COC/JF-10/Storage atomicity = NOT PROVEN; implementation verified = NO; G8 BLOCKED, G9 NOT RUN, G10 BLOCKED. No merge or production activation authorized.


## 13.11 I formal JF-10 prepared-participant ↔ COC bridge decision

I has recorded a formal decision in `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`:
- Decision: **ACCEPT WITH BINDING BRIDGE AMENDMENTS — SINGLE I POLICY DOMAIN ONLY**.
- I Owner commit: `dea5061a342ad328103c7aee0afc68b121563463`.
- I artifact readback Blob: `1dedce596761807b25d337daf4a0d21bb797a197`.
- Exact A COC proposal reviewed: Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- Exact D/Storage current JF-10 shared recovery contract reviewed: Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`.
- Issue #4 decision comment: `6920679097` (readback verified).

I's decisive authority split: COC is the cross-owner causal-order and participant-accounting log; I's policy-domain sequencer remains the sole durable COMMIT/ABORT decision coordinator for the prepared Storage XID; Storage alone resolves that exact XID and publishes VisibilityPointer/PublicationReceipt; D alone owns fence/lineage/barrier semantics. COC and I positions are distinct typed orders and cannot be compared or substituted.

Binding amendments require COC to register a stable preallocated XID/operation/digest/boundary before Storage PREPARE, register Storage's signed PreparedParticipantReceipt after durable prepare, require I to linearly verify both before owner-final-gate decision, record I's signed terminal proof and Storage's same-XID resolution idempotently, and preserve forward-COMMIT/rollback-ABORT recovery direction. Ten new JF10-COC fault cases are specified in I artifact §10.8.

**Gate status:** I's interface decision is RECORDED WITH BINDING AMENDMENTS; the current A COC artifact must be amended to include these bridge records/API and exact state transitions before it is fully reconciled. Multi-policy-domain atomicity remains BLOCKED. JF-10 remains P0 OPEN; JF10-COC-01..10 and other conformance remain SPECIFIED / NOT RUN; implementation NOT VERIFIED; no deployment or production approval.

## 13.12 H recovery-batch schema addendum, I composition boundary and JF-10 model CI — 2026-11-16

### H 1.1.0 recovery-batch schema candidate addendum

H has published and read-back verified its recovery-batch field/message mapping:
- H artifact: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`
- Blob: `d2759386ab1cd4e5518fdb1820e2ad7044ad1871`
- Commit: `879d0f0248047482de3b7bf0fbc3f82a8acc6d1a`
- New message families: `OWNER_LOCAL_PENDING_GATE`, `COC_RECOVERY_CUTOFF_BATCH`, `PRE_BATCH_PARTICIPANT_RECONCILIATION`, `OWNER_LOCAL_GATE_RELEASE`, `COC_RESTORE_FENCED`.
- Required fields, conditional I/D owner refs, complete pre-batch participant set, owner high-water attestations, batch digest/prefix, owner-only gate release and restore-fenced behavior are specified.
- H recovery-batch field-mapping exception is closed at the documentation/schema-candidate level for the exact A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.

H schema remains candidate, NOT generated/frozen/interoperability-tested. Signature/MAC suite, key lifecycle and federation remain subject to I/Security approval. H-CO-17..23 are SPECIFIED / NOT RUN.

### I COC / JF-10 composition boundary

I has published an exact technical disposition:
- Artifact: `09-security-governance/phase-3.6.2-i-coc-jf10-composition-boundary.md`
- Blob: `9e1f66ddbe0952f17068b1638feb8ab0094588c3`
- Commit: `2105ead17dfc21ea1a33c21865db24336d2b75da`

I accepts COC as the CGH cross-authority causal-order evidence service with I-issued authorization/revocation evidence. I does **not** approve automatic COC↔JF-10 composition. JF-10 v2 remains separately governed by I's policy-domain owner-gate-participating 2PC protocol; multi-domain atomicity remains BLOCKED. Any future operation requiring both protocols needs a new exact-version joint bridge design. This is technical architecture disposition, not external I governance approval.

### Storage exact COC interface decision

Storage exact decision remains:
- Artifact Blob: `a589d983ac145244962c22e5da3a55427aa35ff8`.
- Decision: **CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY**.
- COC, I JF-10 sequencer/2PC, and per-Canonical-Memory-authority Storage visibility remain separate consistency authorities. Combined atomicity is NOT PROVEN and remains fail-closed.

### JF-10 reference-model CI result

- Workflow run: `43895971452`
- URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43895971452
- Head commit: `684ac873bec331649c18a45a992007d04f211832`
- Test source Blob: `a38d73b4a5e7c65210fb414a62fb91b30649b788`
- 15 deterministic in-memory unittest methods: **CI SUCCESS**.

This is only a logical Python reference-model pass. It does not verify production DB prepared-XID durability, I sequencer integration, COC quorum, D/Storage shared transactions, process crash, HA/failover/restore, object-store/reader behavior or production JF10/COC/Storage conformance. JF-10 P0 remains OPEN; G3 remains BLOCKED.

### Current exact gates

- CGH-APPLIED-1.1 recovery-batch exact C/D/I/H/G/B decisions: RECORDED WITH ENUMERATED EXCEPTIONS / APPROVE for exact package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- H recovery-batch schema documentation: candidate mapping published; production freeze NO.
- Storage COC interface: CONFIRMED WITH CHANGES, architecture only.
- I COC↔JF-10: no automatic composition; any combined flow remains BLOCKED pending new joint bridge.
- Named COC operator / actual infrastructure / DB engine / RPO-RTO / SLO / KMS: OPEN / NOT VERIFIED.
- COC-01..16, H-CO-17..23, JF10-01..17, Storage C01..C23, I-CO and G-CO: NOT RUN (except the separate in-memory reference-model suite above).
- Applied Contract Frozen: NO; implementation verified: NO; G8 BLOCKED; G9 NOT RUN; G10 BLOCKED.

## 13.13 COC outage-recovery logical model and CI — 2026-11-16

A added a deterministic in-memory reference model for the COC outage recovery-batch semantics:
- Model: `reviews/integration/reference_model/coc_recovery_model.py`, Blob `10091e727874cf35eda619e745fb316683a9e978`.
- Tests: `reviews/integration/reference_model/test_coc_recovery_model.py`, Blob `daf3016cf99970414b804be5fef9174f99fa8eab`.
- Workflow: `.github/workflows/coc-recovery-reference-model.yml`, Blob `4f3e849f9f6861f6f0ed45fec8fc81631b65f933`.
- README: Blob `6947279443b79aa3d85ca1ca3ebac5e3010697d2`.

The first CI run exposed an incorrect test expectation: while the single global COC log is unavailable, all protected submits must fail closed, not merely those matching a D lineage request. The test was corrected to assert global fail-closed during outage and owner-local lineage scoping after COC returns while the D pending gate remains closed.

**Corrected CI result:**
- Workflow run: `43897053156`.
- URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43897053156
- Head commit: `553b81880ead745cca6afd426955b2df45ef4913`.
- Job: `Deterministic COC recovery-batch model tests`.
- Result: **SUCCESS — 10 tests passed** (`Ran 10 tests ... OK`).

Coverage includes I/D local pending gates, global outage fail-closed, affected-lineage gate after recovery, no new intent while pending, simultaneous I/D requests in one batch without local-time ordering, pre-batch participant enumeration, unresolved participant retention, owner-specific high-water checks before gate release, RESTORE_FENCED for missing prefix/incomplete request set, and immutable request digest conflict.

**Strict limitation:** this is an in-memory logical reference model, not a Raft/quorum COC, durable owner-local gate, production I sequencer, D fence service, persistent participant registry, process crash/failover/restore, or cross-protocol atomicity test. It does not pass COC-01..16 production conformance or Phase 3.6 G10. Production COC remains NOT IMPLEMENTED / NOT VERIFIED; deployment/operator remains NOT DESIGNATED.

## 13.12 A COC architecture amendment — I JF-10 prepared participant bridge

A amended `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md` on `session-a-integration-2026-11-16` to incorporate I's formal JF-10 bridge decision (I disposition Blob `1dedce596761807b25d337daf4a0d21bb797a197`).

- A COC architecture exact post-amendment Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`.
- Commit: `78b811ee12499413d6e7a2e03ee5b36e6a0a2f38`.
- Readback from A Owner branch verified §12, all five required JF-10 bridge record names, and all ten `JF10-COC-01..10` case identifiers.

The amendment makes the authority boundary normative: COC orders and observes; I's policy-domain sequencer alone decides COMMIT/ABORT; Storage resolves the exact same XID; D owns ForgetFence and barrier semantics. It adds pre-PREPARE intent registration, Storage-signed PreparedParticipantReceipt registration before I's owner-final gate, exact tuple binding, typed non-comparable COC/I positions, same-XID recovery, outage handling and ten new conformance specifications.

**Status correction:** A architecture text amended and readback-verified. This is not fresh I/C/D/H/Storage exact-Blob acceptance, not implementation evidence, not deployment/operator designation, and not a test pass. COC-01..12 and JF10-COC-01..10 remain NOT RUN; JF-10 remains P0 OPEN; multi-policy-domain atomicity remains BLOCKED. Next closure actions are fresh I and relevant Owner decisions on the new A Blob, plus explicit D barrier and Storage prepared-XID/same-XID recovery acceptance; H must approve any required 1.1.0 wire mapping.


## 13.14 I-approved JF-10 ↔ COC bridge — C/D/Storage joint decision gate

Formal exact-version Owner decision request is open as [Issue #8](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/8). The common review bundle pins:
- I bridge disposition §10.1–10.9: `1dedce596761807b25d337daf4a0d21bb797a197`;
- A COC architecture: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`;
- D and Storage shared JF-10 v2 protocol readback: `94679897e84a6f58fd8b9467b5249e1a885cb0b0`;
- C C-submit contract: `a72a3eb1e5207f67c01f804508311f42db9a6e0a`;
- Storage prior COC boundary decision: `a589d983ac145244962c22e5da3a55427aa35ff8`.

**Gate state: C = PENDING; D = PENDING; Storage = PENDING.** No prior CGH/COC acceptance is inherited as acceptance of this bridge. Each Owner must issue an append-only decision on its own branch against the same bundle. A will verify exact Blob SHAs and update this ledger only after readback.

The requested bridge preserves separate authority domains: COC causal-order/participant ledger; I policy-domain sequencer as sole JF-10 decision authority; Storage same-XID resolution and visibility authority; D fence/lineage/barrier authority. Scope is one I PolicyDomainRef. Multi-domain atomicity remains BLOCKED. Production implementation, deployment and conformance are not implied.

## 13.14 COC model invariant refinement and corrected CI — 2026-11-16

A found one further logical invariant during model review: a committed recovery-cutoff batch must remain an admission cutoff after an owner-local outage gate is released. Clearing the local pending gate cannot erase the committed I/D request cutoff. The model was corrected so the batch position is retained in the cutoff ledger and subsequent affected intents/submits remain blocked.

Current source pins:
- Model Blob: `e96f6929436b10d6a23e9022c197951aa4ee596a`.
- Test Blob: `d087d587f81eda83f1a0f7dff2affff10a2ef78f`.
- Workflow Blob: `4f3e849f9f6861f6f0ed45fec8fc81631b65f933`.

Corrected CI:
- Run: `43897364938`.
- URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43897364938
- Head commit: `386b03f4ae76cc175ab18c6013437a9c726de8a5`.
- Job: SUCCESS.
- Test log: **11 tests passed** (`Ran 11 tests ... OK`).

The new test proves that after the D owner-local pending gate is released, the batch-committed D cutoff still blocks later intents/submits in the affected lineage while unrelated lineage remains independently eligible after COC service recovery.

The earlier COC model CI run `43897053156` (10 tests) is superseded by this corrected 11-test run. This remains an in-memory logical model only; it does not implement consensus durability, real I/D owner gates, participant storage, HA/failover/restore or production COC conformance. COC-01..16 remain NOT RUN and G10 remains BLOCKED.

## 13.13 I exact-version acceptance of amended A COC bridge

I reviewed and formally accepted the exact amended A architecture Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` on A branch `session-a-integration-2026-11-16`. The decision is **ACCEPT — exact Blob, with binding single-I-PolicyDomain limitation**.

I Owner disposition readback:
- Path: `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`
- Branch: `session-i-security-governance-2026-11-16`
- Blob: `8069ff86988396442c8d9dc3fd58653683abe2f3`
- Commit: `f16a52ebc0bddb707565c0393f378a4baa782e54`
- Formal decision: §11, exact-version acceptance.

Issue #4 comment records the decision: `6920893505`.

**Remaining independent gates:** D must accept fence/barrier membership and cutoff ordering; Storage must accept durable preallocated-XID preparation, signed PreparedParticipantReceipt and exact-XID recovery; H must decide any required wire-schema mapping. I's acceptance is architecture-interface only and does not establish implementation, deployment, conformance or production approval. COC-01..12 and JF10-COC-01..10 remain NOT RUN; JF-10 remains P0 OPEN; multi-policy-domain atomicity remains BLOCKED.

## 13.14 D and Storage exact-version acceptance of JF-10 COC bridge

Both Owners reviewed the exact A COC architecture Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, §12.1–12.8, and recorded independent decisions:

| Owner | Decision artifact | Exact readback Blob | Commit | Disposition |
|---|---|---|---|---|
| D | `03-memory-brain/forget-fence-operation-and-publication-gate.md` on `session-d-memory-brain-2026-11-16` | `5a56c406578fdf257509315eb3f6f3f75456116c` | `edf35b8a80bb9d096748dab129cea5867561b5d3` | ACCEPT D-owned fence/barrier semantics for exact A Blob |
| Storage | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` on `session-storage-consistency-forget-atomicity-2026-11-16` | `55c01f4512f2e3d8aac767dd004e768ae073178e` | `76ca854aa91db1c7b2fcf0bf4174606624c72a46` | ACCEPT Storage participant contract subject to DB capability/deployment proof |

D confirms prepare-intent before fence cutoff is a barrier participant; fence-first rejects prepare; participant-first holds the barrier until I decision and Storage same-XID resolution; unknown never releases the barrier. D retains all ForgetFence/lineage/effective completion authority.

Storage confirms preallocated XID, durable prepared participant and locks, Storage-signed PreparedParticipantReceipt, exact same-XID forward-commit/rollback, authoritative readback and atomic VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox. Storage's acceptance is conditional on concrete database support; no engine/version, XA profile, operator or deployment has been selected or verified.

Issue #4 records both decisions in comment `6920938325`.

**Remaining gate:** H's exact 1.1.0 schema/wire mapping decision remains outstanding. Implementation, concrete DB capability, COC-01..12 and JF10-COC-01..10 conformance remain unverified/not run. JF-10 P0 remains OPEN; multi-policy-domain atomicity remains BLOCKED; production activation is NOT APPROVED.


## 13.15 JF-10 ↔ COC bridge decision refresh — 2026-11-16

The exact Owner evidence was refreshed and reconciled on Issue #8. I accepts A COC architecture Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` with the single-I-PolicyDomain limitation (I disposition Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`). D accepts that A Blob for D-owned fence/barrier semantics (D artifact Blob `5a56c406578fdf257509315eb3f6f3f75456116c`). Storage accepts the Storage participant contract for that A Blob, conditional on concrete database capability and deployment proof (Storage artifact Blob `55c01f4512f2e3d8aac767dd004e768ae073178e`). C's current artifact Blob `a72a3eb1e5207f67c01f804508311f42db9a6e0a` accepts the CGH-APPLIED-1.1 recovery-batch package/companion pair but does not yet record a distinct formal decision against the complete Issue #8 bridge bundle and A architecture Blob `a3c51ec...`.

A posted Issue #8 reconciliation comment (ID `6921025964`) asking C for exact-bundle acceptance/amendment/rejection and asking D/Storage to confirm their exact acceptances cover the complete corrected bundle. The bridge gate therefore remains OPEN pending readback of those clarifications. No production implementation, database capability, operator/deployment or conformance is implied. JF-10 P0 remains OPEN; JF10-COC-01..10 NOT RUN; multi-policy-domain atomicity BLOCKED.

## 13.15 H exact JF-10 bridge wire-schema decision

H has published an exact additive BMCP 1.1.0 schema-candidate mapping for A COC architecture §12, exact Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`.

- H artifact: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`
- H branch: `session-h-bmcp-protocol`
- H exact readback Blob: `1716b23741479740f9e12003cbf2bd1a80c63aab`
- H commit: `8a45a35e0993493e96e3e7e38dbaecf0927feee8`
- Decision: **ACCEPT THE JF-10 BRIDGE WIRE MAPPING FOR THIS EXACT A BLOB, WITH ENUMERATED EXCEPTIONS**, H §12.10.

H maps five distinct COC lifecycle records to five 1.1.0 message families: `JF10_PREPARE_INTENT_REGISTERED`, `JF10_PREPARED_PARTICIPANT_REGISTERED`, `I_JF10_TERMINAL_DECISION_OBSERVED`, `STORAGE_JF10_PARTICIPANT_RESOLVED`, and `JF10_BRIDGE_RECONCILIATION_RECORDED`. It specifies common envelope, typed opaque references, exact immutable tuple, separate COC/I/D/Storage positions, conditional requiredness, signatures/commit proofs, idempotency/conflict rules, fail-closed UNKNOWN behavior and H-JF10-01..10 conformance cases.

This is schema-candidate documentation acceptance only. Generated JSON Schema/IDL/SDK bindings and interoperability have not been produced or tested. Crypto suite/key custody remains subject to I/Security governance. H does not approve deployment, implementation, database capability or production activation. H-JF10-01..10 remain NOT RUN; JF-10 remains P0 OPEN; multi-policy-domain atomicity remains BLOCKED.


## 13.15 JF-10 ↔ COC bridge exact-version Owner reconciliation

Issue #8 now carries the corrected exact bundle and Owner readback:
- A COC architecture Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`.
- I §11.2 exact-version ACCEPT: I artifact Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`, single-I-PolicyDomain only.
- D exact-version ACCEPT: `forget-fence-operation-and-publication-gate.md`, Blob `5a56c406578fdf257509315eb3f6f3f75456116c`.
- Storage exact-version ACCEPT: `forget-atomicity-storage-realization-review.md`, Blob `55c01f4512f2e3d8aac767dd004e768ae073178e`.
- C decision remains pending for this exact A Blob; its current contract's recovery-batch decision is pinned to the older A/COC pair `4961ffefc0f9920efb8425a9b2a7af42d8f64819` / `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.

**Current exact bridge acceptance gate: I ACCEPT; D ACCEPT; Storage ACCEPT; C PENDING.** The outstanding action is an append-only C Owner decision on the amended A architecture exact Blob. No joint closure until C's artifact is published and read back. JF-10 P0, implementation, DB capability, COC deployment and conformance remain OPEN / NOT VERIFIED / NOT RUN.


## 13.16 H exact-version JF-10 bridge wire mapping — 2026-11-16

The previous H wire-mapping gap is closed at schema-candidate documentation level. H's current artifact `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, branch `session-h-bmcp-protocol`, Blob `1716b23741479740f9e12003cbf2bd1a80c63aab`, §12.10 explicitly ACCEPTS the five JF-10 ↔ COC bridge message-family mappings for exact A architecture Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, with enumerated exceptions. The five families are prepare-intent registration, prepared-participant registration, I terminal-decision observation, Storage participant resolution and bridge reconciliation observation.

This is not production schema freeze: generated JSON Schema/IDL, SDKs/interoperability and crypto/key governance remain open; H-JF10-01..10 are SPECIFIED / NOT RUN. Issue #8 was updated in comment `6921054285`. The overall bridge gate remains OPEN pending C's distinct exact-bundle decision and D/Storage clarification. JF-10 P0 remains OPEN; implementation/deployment NOT VERIFIED; multi-policy-domain atomicity BLOCKED.


## 13.16 H JF-10 bridge schema-candidate decision

H exact-version decision has been read back from its Owner branch:
- `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `1716b23741479740f9e12003cbf2bd1a80c63aab`, §12.10.
- Decision: ACCEPT the JF-10 bridge field-level wire mapping for exact A architecture Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, with enumerated exceptions.

H's five message-family mappings are recorded. The schema remains a candidate: generated schemas/SDKs and interoperability not produced/tested; crypto/key governance remains I/Security-owned; H-JF10-01..10 NOT RUN; production freeze NO.

**Updated Owner gate: I ACCEPT; D ACCEPT; Storage ACCEPT; H ACCEPT (schema candidate only); C PENDING.** The remaining requested action is C's exact-version acceptance against the same A Blob. JF-10 P0, implementation, deployment and conformance remain OPEN / NOT VERIFIED / NOT RUN.


## 13.16 C exact-bundle acceptance — JF-10 prepared participant ↔ COC bridge

C has published an independent append-only decision against the complete Issue #8 exact bridge bundle:
- C artifact: `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- C branch: `session-c-agent-integration-2026-11-16`
- C decision Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- C commit: `702263dee9b40cf78fe95481731f52adb775c0d2`
- Decision: **ACCEPT THE EXACT JF-10 ↔ COC BRIDGE BUNDLE WITH ENUMERATED C-OWNED CONDITIONS**.

C pins A `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, I `8069ff86988396442c8d9dc3fd58653683abe2f3`, D/Storage common JF-10 v2 protocol `94679897e84a6f58fd8b9467b5249e1a885cb0b0`, D `5a56c406578fdf257509315eb3f6f3f75456116c`, Storage `55c01f4512f2e3d8aac767dd004e768ae073178e`, and H §12.10 wire mapping `1716b23741479740f9e12003cbf2bd1a80c63aab`.

C accepts the provider boundary: no protected provider invocation before durable COC prepare-intent registration, Storage-signed same-XID prepared receipt registration, and authoritative I terminal decision. C alone emits actual CSubmitOutcome. UNKNOWN/IN_DOUBT retains the same participant, XID and provider idempotency key; no retry-as-new-operation and no barrier release. D fence-first blocks provider invocation; participant-first remains in D barrier through I/Storage/C terminal evidence. Scope is one I PolicyDomain only.

This closes the outstanding architecture/interface Owner-decision gate for the named bridge bundle. It does not close provider-specific idempotency proof, runtime implementation, DB capability, conformance, deployment or production gates. C-CO-01..10 and H-JF10-01..10 remain SPECIFIED / NOT RUN; H schema remains candidate/not production-frozen; Storage DB capability remains unproven; COC operator/deployment remains undesignated. JF-10 remains P0 OPEN; multi-PolicyDomain atomicity BLOCKED. The earlier §13.15 pending snapshot is historical and superseded by this §13.16 readback.


## 13.17 C exact-version JF-10 ↔ COC bridge acceptance — architecture/interface gate closed

C's Owner artifact has been read back from its branch:
- `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, Blob `45a48249717c8cddb07ab96197730ef93d406c22`.
- Decision: ACCEPT the exact JF-10 ↔ COC bridge bundle with enumerated C-owned conditions, explicitly pinning the same A/I/D/Storage/H/common JF-10 source SHAs recorded in §13.17 of the A tracking ledger.

**Architecture/interface gate is CLOSED WITH ENUMERATED EXCEPTIONS:** C ACCEPT; D ACCEPT; Storage ACCEPT; I ACCEPT (single I PolicyDomain); H ACCEPT (1.1.0 schema candidate only).

This does not close JF-10 P0 or any production gate. Durable prepared-XID/lock behavior, same-XID recovery on selected DB, COC operator/quorum/deployment, provider idempotency/fault recovery, generated H schema and SDK interoperability, crypto governance and crash/recovery conformance remain OPEN / NOT VERIFIED / NOT RUN. Multi-PolicyDomain atomicity remains BLOCKED. No production activation or merge is implied.


## 13.17 H machine-readable JF-10 bridge schema candidate

Following H's exact wire-mapping decision (§13.15), H has published a machine-readable JSON Schema Draft 2020-12 candidate for the five JF-10 bridge message families:
- Schema path: `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json`
- Schema Blob: `a8a945cc3623c2907003b93625e3c79742150944`
- Schema commit: `d1880f9de26e6ec29753ca847989926d8ea5d70e`
- H source/disposition document Blob after recording the schema: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- H source document commit: `08cca6341c3c44ad8502c215eba2b1941a8febb7`.

The JSON file was fetched back from H Owner branch and parsed as JSON; it contains exactly five message variants. It expresses common required envelope fields, per-message required fields, state/outcome enums, opaque reference length and SHA-256 syntax, and conditional revocation/Storage outcome requirements.

This is a schema candidate, not production-frozen or generated from an executable IDL pipeline. JSON Schema cannot prove signatures, quorum commit, exact tuple equality across messages, same-XID identity, causal ordering, owner authority or terminal reconciliation. Parser enforcement for duplicate keys/canonical bytes and semantic cross-message validators remain required. SDK generation, cross-implementation interoperability and H-JF10 conformance remain NOT RUN. The architecture/interface Owner-decision gate remains closed; implementation, runtime, DB/provider capability, conformance and production gates remain open. JF-10 P0 remains OPEN.
