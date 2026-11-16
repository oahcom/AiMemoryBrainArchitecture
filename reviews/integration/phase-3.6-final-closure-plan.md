# Phase 3.6 — Final Closure Plan

- Owner: Session A — Principal Integration Architect
- Status: **ACTIVE PLAN / NO CONTRACT FREEZE / NO IMPLEMENTATION SIGN-OFF**
- Baseline: `reviews/integration/phase-3.6-closure-tracking.md`
- Rule: preserve completed design decisions; assign only outstanding external approval, consumer acceptance, implementation and verification work.

## 1. Executive direction

The three workstreams are delivered. Their closure states are not equivalent:

- **DE-S:** logical architecture and two-round six-dimension design review are closed. Move directly to I authority/inventory integration, Storage deployment selection, implementation and executable fault proof. Do not repeat design review absent a new evidence-backed Finding or changed baseline.
- **BIH:** BIH36-JD-01..17 are a delegated joint technical baseline. Move to independent governance approval, explicit downstream consumer acceptance and I36/H36 execution. Do not re-decide the technical baseline absent a demonstrated contradiction.
- **CFG:** C/F/G semantic contracts are delivered. Move to one version-pinned C/G/H Applied contract approval package, D/I/B predicate confirmation, then integrated runtime/security test execution. Do not rewrite C/F/G semantics simply to restate their current decisions.

A records the exact evidence and gate state; A does not create governance approval, consumer acceptance, production deployment or test pass.

## 2. Workstream DE-S — implementation closure

### 2.1 Preserve the completed design baseline

Controlling design artifacts:
- D joint Forget linearization decision and JF-01..09 addendum.
- E joint producer publication decision, JF-01..09 addendum and E36-01..20 conformance specification.
- Storage logical durable atomicity decision, JF-01..09 addendum and two-round six-dimension review.

The Storage review records Round 1 and Round 2 PASS across all six dimensions, no new finding in either round, and explicitly labels the design self-review CLOSED. This plan treats that as completed design work.

### 2.2 Work packages

| ID | Remaining work | Responsible owner | Required inputs | Deliverable / acceptance evidence | Exit condition |
|---|---|---|---|---|---|
| DES-EXT-01 | Approve I authorization policy required by publication and revocation | I + independent Security/Identity Governance; Data/Scope and Environment Governance as applicable | I36-GOV-01..08 exact decision set; policy profiles and jurisdictions | Signed/effective governance entries with approver PrincipalRef, authority, decision ID, exact text/hash, time, version and expiry | All applicable I governance decisions effective |
| DES-EXT-02 | Designate Environment Registry Authority | Project governance / Environment Governance; I records and enforces | Exact registry responsibilities, trust domain, change control | Named accountable authority, registry schema/version, signed ownership and bridge policy | Cross-Environment resolution has a real authority; otherwise remains denied |
| DES-EXT-03 | Issue global Producer/Recipient Inventory seal | I (registry authority); D/E/F/G/H/Storage and external recipients/backup owners supply inventory | Authenticated owner/instance IDs, Scope, capabilities, lineage, backup/export/restore map | ProducerDomainInventoryEpoch, canonical inventory digest, complete member enumeration, InventorySealReceipt, explicit gaps/exclusions | I attests closed-world completeness or explicit approved exceptions |
| DES-EXT-04 | Issue AuthorizationCommitPermit/revocation serialization contract | I; D/E/Storage integrate | Effective I policy, exact principal/action/resource/Scope/work/attempt/manifest fields | Single-use/idempotent permit and proof revocation cannot become effective before an accepted publication commit | D/E/Storage can validate current authority at visibility linearization |
| DES-IMPL-01 | Select physical serialization/deployment topology | Accountable Storage engineering / DB platform owner (not yet named); Storage Owner documents | Production environment and constraints; I interfaces; D logical serialization requirements | Selected DB/coordinator product and version, isolation/linearizability proof, replication/failover, backup/restore, transaction/visibility authority, named approver | Deployment decision signed and pinned |
| DES-IMPL-02 | Implement durable Forget control ledger and visibility gate | D semantics + Storage implementation | DES-EXT-03/04 and DES-IMPL-01 | Code/build SHA, durable schema, fence/work/attempt/lease/manifest/dependency/permit/receipt records, one authoritative visibility predicate, all-reader enforcement | Implementation matches exact logical decision |
| DES-IMPL-03 | Implement E producer admission/publication protocol | E + Storage + D integration | D receipts/APIs, inventory seal, authorization permit, selected coordinator | Executable producer admission, private staging, dependency receipts, current manifest gate, idempotent publication and outcome lookup | No publish possible outside authoritative gate |
| DES-TEST-01 | Execute D36/E36/C01–C20 and addenda | D/E/Storage test owners; I provides authorization/inventory fixtures | Integrated build, selected topology, deterministic harness and all receipts | Per-test build/runner/seed, exact inputs, expected/actual, transaction traces, receipts, crash/failover/restore logs, reviewer | All mandatory race/fault/recovery invariants pass; failures become findings |

**Important authority allocation:** I owns the global inventory and PermissionEpoch/authorization. D owns Forget semantics and the per-operation barrier. E owns producer execution. Storage owns physical transaction and recovery realization. Storage deployment approver is not named in the current artifact; do not assign this approval to A or assume the Storage architecture author is the production engineering approver.

## 3. Work package BIH — governance and consumer acceptance

### 3.1 Preserve the joint technical baseline

BIH36-JD-01..17 are recorded in the current B, I and H Phase 3.6 artifacts. The decisions cover distinct typed identities, protected verifier context, issuer-scoped Principal resolution, non-amplifying delegation, explicit Scope/Environment grants, PermissionEpoch currentness, non-transferable authorization, ACK binding, reconnect ordering and fail-closed unknown fields.

This baseline is accepted as the delegated technical design. It does not mean I governance is effective or that downstream consumers have accepted the fields.

### 3.2 Governance approval package

| ID | Policy decision | Required approving body | Evidence to record | Owner |
|---|---|---|---|---|
| BIH-GOV-01 | Trusted issuer admission/federation | Named Security Governance approver | Issuer/trust-domain profile, exact version, approver and effective time | I |
| BIH-GOV-02 | Principal taxonomy/registration/cross-issuer linking | Identity Governance | Principal namespace and linking policy version | I |
| BIH-GOV-03 | Delegation depth/sub-delegation/acting-for | Security Governance; Identity/Legal where required | Signed grant profile and revocation semantics | I |
| BIH-GOV-04 | Cross-Scope grants/sharing/inheritance/break-glass | Data/Scope Governance | Exact Scope roles, source/target, action/resource/purpose/audience | I + B semantics |
| BIH-GOV-05 | Cross-Environment bridge/federation | Named Environment Governance authority | Registry authority, mapping and effective bridge policy | I + Environment owner |
| BIH-GOV-06 | PermissionEpoch domains, leases/staleness and revocation SLA | Security Governance | Effective epoch service/profile and freshness/revocation SLA | I |
| BIH-GOV-07 | Revocation effective point/in-flight semantics | Security Governance plus boundary-owner acknowledgements | D/E/F/G/H/C boundary acknowledgements and ordering profile | I |
| BIH-GOV-08 | Administrative/break-glass | Independent approver; Privacy/Legal as applicable | Reason, scope, expiry, dual-control and immutable audit | I |

I's governance register must be updated by I, not A. Each entry needs named approver identity/authority, decision ID, exact policy text/hash, approval timestamp, effective version, scope/jurisdiction, expiry/review and supersession.

### 3.3 Consumer acceptance campaign

| Consumer | Acceptance scope | Owner | Required acceptance artifact |
|---|---|---|---|
| C | Principal/Actor/Agent/RuntimeSession and Producer bindings; Scope/Environment; PermissionEpoch; final request and disclosure boundary | C | C acceptance record pinned to BIH artifact digests plus forged identity/Scope negatives |
| D | Principal/Actor/Producer; Scope/Environment; action/resource; AuthorizationCommitPermit and PermissionEpoch; separation from ForgetFence | D | D acceptance record and fence-vs-revocation/permit tests |
| E | Producer class/instance, source lineage, Actor/Scope, inventory epoch/seal, permit at final publish | E | E acceptance record and producer admission/publication tests |
| F | Identity and Scope filtering before candidate generation; current epoch and D fence at final return/cache/rebuild | F | F acceptance record and retrieval/cache/rebuild race tests |
| G | Authenticated delivery/ACK identity, exact ContextVersion/attempt, Scope/Environment, PermissionEpoch, ForgetFence, CapabilityEpoch | G | G acceptance record and Applied/reconnect/late-ACK tests |
| Storage | Commit-time authorization permit, Scope, inventory seal, work/attempt/lease, manifest/dependency digest and fence | Storage engineering owner | Signed physical transaction predicate acceptance and recovery proof |

Each consumer must record accepted artifact SHA/version, exact fields, semantics, negative cases, exceptions and approver. A branch commit or document fetch does not count.

### 3.4 BIH test execution

After governance and consumer prerequisites, run I36-01..15 and H36-01..18. The runner must include issuer/key and delegation fixtures, protected transport, authoritative registries, Environment Registry, Scope grants, PermissionEpoch/revocation oracle, Adapter instance/capability, D fence, reconnect and ACK replay harness, build SHA and retained evidence. No test may be marked passed without expected/actual output and reviewer.

## 4. Work package CFG — Applied contract and runtime verification

### 4.1 Do not rewrite delivered C/F/G contracts

C owns final immutable request submission evidence; F owns retrieval/index/cache suppression and final-return revalidation; G owns ContextVersion, Delivery and Applied state. Their existing semantic contracts remain Owner-owned.

### 4.2 C/G/H Applied freeze sequence

1. C, G and H jointly produce one versioned Applied contract package with a canonical digest. It must define lifecycle stages, field names/types/requiredness, digest/canonicalization, signature/key profile, replay/idempotency, Adapter capability/region coverage, ACK taxonomy/ordering, historical versus current-use validity, reconnect/supersession and fail-closed errors.
2. C explicitly approves the producer/final-request boundary and evidence completeness.
3. G explicitly approves the Applied state machine, acceptance predicate and current-use projection.
4. H explicitly approves wire schema, protected authentication binding, ACK, capability and reconnect semantics.
5. D confirms fence/lineage ordering; I confirms PermissionEpoch/revocation and authorization predicate; B confirms typed Actor/Scope/Environment meanings.
6. A pins the exact version/digest and records explicit approval statements, approver authorities, timestamps and exceptions in the approval ledger.

The three current contract commits are different source artifacts, not one shared version. Until steps 1–6 complete, Applied Contract Frozen = NO.

### 4.3 Runtime and security execution

Run CFG-01..20 and PI-01..08 from the A joint report after the approved contract and upstream implementation are available. Fixtures must include stable identities, typed Scope/Environment, ContextVersion/Delivery attempt, PermissionEpoch, ForgetFenceGeneration, CapabilityEpoch, canonical lineage, deterministic operation latches, final request evidence, prompt-injection corpus, expected/forbidden state, build/runner IDs and durable evidence. Include D/E/Storage race and I/H auth/reconnect dependencies in the integrated environment.

## 5. Overall gates and exit criteria

| Gate | Current state | Exit criterion |
|---|---|---|
| G0 Baseline Integrity | PASS | Refresh branch refs and re-read artifacts before each decision |
| G1 DE-S Design Closure | PASS | Remains closed unless a new evidence-backed design Finding or source-baseline change invalidates it |
| G2 DE-S External Dependency Approval | BLOCKED | I governance, inventory seal, authorization permit and Storage deployment owner/decision recorded |
| G3 DE-S Implementation Verification | BLOCKED | Concrete implementation/build, durable receipts, all-reader predicate, recovery and D36/E36/C01–C20 evidence |
| G4 BIH Technical Agreement | CONDITIONAL PASS | BIH36-JD-01..17 remain the pinned technical baseline |
| G5 BIH Governance Approval | BLOCKED | I36-GOV decisions approved and effective |
| G6 BIH Consumer Acceptance | BLOCKED | C/D/E/F/G/Storage explicit acceptance records |
| G7 BIH Test Verification | NOT RUN | I36/H36 executed and reviewed |
| G8 CFG Applied Contract Freeze | BLOCKED | One common C/G/H version/digest and all owner/predicate approvals |
| G9 CFG Runtime/Security Verification | NOT RUN | CFG-01..20 and PI-01..08 executed and reviewed |
| G10 Overall Implementation Readiness | BLOCKED | All required governance, consumer, implementation and test gates pass |

No overall readiness, production readiness, Runtime Forget End-to-End Closed, Global Forget Complete or physical-erasure claim is permitted while any required gate remains blocked/not run.

## 6. A governance and change-control responsibilities

A shall:
- refresh branch HEADs and artifact Blob SHAs before each closure batch;
- maintain separate approval, consumer, implementation and test evidence states;
- issue only outstanding work to the relevant Owner;
- record new Findings only when supported by exact contradictory/missing evidence;
- never change Owner contracts, invent approvers, merge branches or infer acceptance;
- re-run the relevant gate after exact evidence is delivered.

## 7. Immediate next actions

1. I: return the named governance approver/effective policy decision package and designate Environment Registry Authority.
2. I + all inventory participants: publish a sealed Producer/Recipient/Backup inventory and AuthorizationCommitPermit/revocation contract.
3. Storage engineering leadership: name the accountable deployment decision-maker and select the concrete transaction/coordinator topology.
4. D/E/Storage: implement the already-decided logical protocol and prepare D36/E36/C01–C20 harness; no design reset.
5. B/I/H: preserve the BIH technical baseline and obtain I governance approval; then collect C/D/E/F/G/Storage consumer acceptances.
6. C/G/H: pin one Applied contract version and obtain explicit same-version approvals plus D/I/B predicate confirmations.
7. C/F/G/H/D/E/I/Storage: execute the integrated conformance and security suites; retain reproducible evidence.
8. A: refresh source baselines, update approval ledger and issue final G0–G10 disposition.



## 8. Phase 3.6.2 closure update — I JF-10 disposition consumed

I has accepted the common D/E/Storage JF-10 v2 for a **single policy domain**, with binding clarifications. The exact I disposition is `b7b0287cde3922434a560fca90051cc5b418d987`; multi-policy-domain atomicity remains BLOCKED / NOT ACCEPTED. D/E/Storage have consumed the disposition in identical protocol files (Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`). Storage's deterministic conformance plan is published (Blob `634b856a878234bac186c55b2937344392f5d5ff`).

This resolves the **I architecture decision** portion of the former JF-10 blocker. It does not close JF-10 P0, G2 or G3. Concrete DB/coordinator selection, named deployment approver, implementation, durable prepared-XID/failover/restore proof, executable harness and test execution remain outstanding. InventorySeal, I36-GOV-01..10 and Global Forget Completion remain I-owned blockers. The current safe profile is single policy domain only; multi-domain requests must reject or remain BLOCKED/UNKNOWN.

The plan's gate interpretation is unchanged: G0 must be refreshed before each closure batch; G1 remains PASS; G2/G3 remain BLOCKED; G4 conditional; G5/G6/G8 remain BLOCKED; G7/G9 NOT RUN; G10 BLOCKED. No production readiness, implementation sign-off, Global Forget completion or Phase 3.6 freeze is authorized.

Next DE-S work is implementation mapping and deployment selection, not another architecture redesign: name the accountable Storage engineering approver; select and prove the concrete DB/coordinator profile; map H01–H13 to implementation hooks; implement authoritative I lookup and same-XID recovery; then run the evidence-backed suite. A must continue the BIH governance/consumer and CFG Applied freeze work in parallel under their respective Owner authorities.
