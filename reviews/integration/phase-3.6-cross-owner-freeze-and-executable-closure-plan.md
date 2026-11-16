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
