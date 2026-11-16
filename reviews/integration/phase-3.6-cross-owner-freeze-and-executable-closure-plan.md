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


## 13.2 I Owner exact-version authority confirmation — CGH-APPLIED-1.0

I has now issued an explicit decision against the exact A package and H schema candidate:

- Exact A package Blob: `122b164bcc0760b83bf555072a36fc55631623e1`
- I Owner branch: `session-i-security-governance-2026-11-16`
- I artifact: `09-security-governance/phase-3.6-cgh-applied-1.0-i-owner-authoritative-confirmation.md`
- I artifact readback Blob: `9b09a31b786c0d49669bffb2c8cca332308c7098`
- I commit: `d65ba193fe31199d9bb9ec9c8a6f2647376932e9`
- Decision: **I APPROVES CGH-APPLIED-1.0 WITH ENUMERATED I-OWNED EXCEPTIONS**.

### Confirmed I-owned authority

I confirms issuer/Principal trust, verifier-resolved Actor attribution, canonical I PolicyDomainRef, I-issued monotonic PermissionEpoch, online currentness, no offline/stale grace, complete authorization tuple, final-boundary enforcement, revocation effective point at I durable sequencer epoch advance, and exact-operation race outcomes. I confirms that H transports but does not mint, refresh, interpret or validate I authorization.

### Binding exceptions

1. H `bmcp.applied-ack / 1.0.0` carries PermissionDecision references and PermissionEpoch but does not yet explicitly carry the I CommitAuthorizationReceipt reference and I sequencer terminal-order proof needed for protected final-boundary disclosure. Receipt consumption and ordering evidence are mandatory at the actual owner-final-gate. C/H must reconcile an exact versioned opaque reference/evidence mapping; H must not synthesize or validate it.
2. TLS 1.3 exporter binding and SHA-256 digest are acceptable design mechanisms, but exact signature/MAC suite, key custody, key rotation, compromise response and federation require separate I/Security governance approval.
3. I36-GOV-01..10 remain GOVERNANCE-BLOCKED; ProducerDomainInventoryEpoch/InventorySeal remain CANDIDATE/OPEN where required; multi-policy-domain authorization remains BLOCKED/NOT ACCEPTED.
4. D ForgetFence, lineage, barrier and cross-authority ordering remain D-owned and are not approved by I.
5. I36/H36/CGH tests remain SPECIFIED / NOT RUN; implementation and production interoperability remain NOT VERIFIED.

### Updated A integration gate

- I exact-version authorization disposition: **RECORDED — APPROVE WITH ENUMERATED EXCEPTIONS**.
- D exact-version ForgetFence/lineage/order confirmation: **STILL REQUIRED**.
- H schema candidate 1.0.0: **NOT PRODUCTION-FROZEN**.
- Applied Contract Frozen: **NO**.
- Issue #3 remains OPEN; no branch merge authorized.
