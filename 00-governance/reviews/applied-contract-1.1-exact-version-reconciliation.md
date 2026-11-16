# CGH-APPLIED-1.1 Exact-Version Reconciliation

- Assessment ID: P-APPLIED-1.1-EXACT-RECON-001
- Date: 2026-11-17
- Prepared by: Session P coordinator
- Status: **ALL REQUIRED DESIGN DECISIONS RECORDED WITH EXCEPTIONS — FREEZE / IMPLEMENTATION GATES STILL OPEN**
- Scope: Reconciliation of the current A package and live C/G/H/B/D/I/Storage Owner branch artifacts; no Owner decision is created or substituted.

## 1. Corrected executive result

The current successor contract is `CGH-APPLIED-1.1`, not the older `CGH-APPLIED-1.0`.

Current A package:
- `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Blob SHA: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC deployment/recovery architecture:
  `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`
- Companion Blob SHA: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Profile: `CausalOrderProfile/1.0`
- H schema target: `bmcp.applied-ack/1.1.0`

After re-reading the live Owner branch files (not relying only on historical Issue #3 comments), the current exact-version decision vector is:

| Owner | Live branch artifact | Current blob SHA | Decision on exact A package + COC companion |
|---|---|---|---|
| C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| D | `03-memory-brain/phase-3.6-d-forget-fence-causal-participant-barrier-contract.md` | `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| I | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | `5a5304d48aa912dcf6f817099bd5659371d8cdc8` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| B | `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md` | `3a1e77889cd9a90cd5822d9f0cb3437880868706` | APPROVE — B-owned typed-reference semantics unchanged |
| Storage | `reviews/storage-consistency/phase-3.6-coc-storage-boundary-acceptance.md` | `a589d983ac145244962c22e5da3a55427aa35ff8` | CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY |

**Correction to the initial version of this assessment:** C and H are not pending. Their exact-version acceptance artifacts are present in their live Owner branch files and pin the same current A package and companion COC blob. Earlier Issue #3 comments cite predecessor blob SHAs for the same Owner documents; those historical blob pins were not the current branch blob SHAs, but the current files independently contain the exact decision text and exact A/COC pair. No decision is inferred from comments alone.

Therefore:
- C/G/H exact 1.1 semantic/transport decisions: recorded with enumerated exceptions.
- B/D/I authority-boundary confirmations: recorded for the same exact package pair.
- Storage: confirms the architecture interface with changes only.
- Applied Contract Frozen: **NO**.
- Production wire schema frozen/generated/interoperability-tested: **NO**.
- COC operator/deployment: **NOT DESIGNATED / NOT DEPLOYED / NOT VERIFIED**.
- Runtime implementation and conformance: **NOT VERIFIED / NOT RUN**.

## 2. Exact source pins and current branch heads

| Role | Branch | Current HEAD | Artifact Blob | Decision scope |
|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `cf98cdb8fb3ee99d7b9aed54a14dc8888cf04175` | Package `4961ffefc0f9920efb8425a9b2a7af42d8f64819`; COC `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` | Current candidate package pair |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | `45a48249717c8cddb07ab96197730ef93d406c22` | Actual final-request/provider outcome |
| D | `session-d-memory-brain-2026-11-16` | `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8` | `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` | ForgetFence, lineage, cutoff/effective position, participant barrier |
| I | `session-i-security-governance-2026-11-16` | `1fc3b3293ebf2077edfd6ad253647d382173d9fa` | `5a5304d48aa912dcf6f817099bd5659371d8cdc8` | Policy-domain sequencer, single-use receipt, PermissionEpoch, revocation |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | Transport/schema/integrity/replay/reconnect |
| G | `session-g-memory-context` | `72a8066b4401f9586fe10775d545384b82736f07` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | Full Applied predicate, immutable Applied fact, current-use projection |
| B | `session-b-domain-model-phase3` | `861fa9b2c3e1f572336543b15c7dc392493891db` | `3a1e77889cd9a90cd5822d9f0cb3437880868706` | Typed Actor/Scope/Environment semantics |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3c8ab8ee4579a550300aa48aecab928149cf9370` | `a589d983ac145244962c22e5da3a55427aa35ff8` | COC/Storage architecture interface only |

## 3. Owner decision details and exceptions

### C — ACCEPT WITH ENUMERATED EXCEPTIONS

C accepts durable ParticipantIntent before provider side effect; exact I receipt consumption/terminal and D lineage-bound clearance; coordinator-finalized reservation; actual provider handoff; immutable CSubmitOutcome; and common terminal proof. I COMMIT_WON, D clearance, reservation, coordinator intent or H ACK alone never proves provider success. C alone emits CSubmitOutcome from actual provider observation.

Exceptions: COC/operator and participant registry remain undesignated/undeployed; provider-specific same-key idempotency and crash recovery remain unverified; production wire encoding for every recovery-batch evidence item is not yet pinned; C-CO/provider fault tests remain NOT RUN.

### D — ACCEPT WITH ENUMERATED EXCEPTIONS

D accepts durable owner-local pending gates for fence requests received during COC outage, atomic recovery-cutoff batch without local-clock ordering, pre-batch participant enumeration, complete lineage barrier, and separate fence-request cutoff versus fence-effective position. IN_DOUBT is not released by timeout, lease expiry, queue deletion, worker loss or missing ACK.

Exceptions: complete authoritative lineage inventory and late-discovery closure remain required; coordinator/operator/store are undesignated; COC recovery-batch and D-CO crash/failover/restore tests remain NOT RUN; no physical erasure or Global Forget completion is implied.

### I — ACCEPT WITH ENUMERATED EXCEPTIONS

I accepts the ParticipantIntent-bound single-use CommitAuthorizationReceipt, IAuthorizationTerminalRef binding the I sequencer outcome and applicable revocation request/cutoff (or explicit no-earlier-request assertion), and owner-local suspension of receipt issuance/consumption during COC outage. COC batch position cannot mint or replace I terminal evidence.

Exceptions: I sequencer/receipt service and crash/failover/restore durability unverified; COC operator/store undesignated; H crypto/key lifecycle and external I36 governance remain separate; I-CO/recovery-batch tests NOT RUN; multi-PolicyDomain atomicity blocked.

### H — ACCEPT WITH ENUMERATED EXCEPTIONS

H accepts the recovery-batch semantics as transportable evidence, including I/D owner-local pending-gate references, COC recovery-cutoff batch identity/position/digest, pre-batch ParticipantIntentRef set, I/D reconciliation outcomes and owner high-water attestations. H preserves owner-issued evidence as opaque references and does not synthesize I/D decisions.

H has also published the JSON Schema Draft 2020-12 candidate for five JF-10 bridge message families:
- Path: `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json`
- Blob: `a8a945cc3623c2907003b93625e3c79742150944`

Exceptions: exact field names, requiredness and canonicalization for all recovery-batch evidence are not fully frozen; signature/MAC suite and key custody/rotation/federation remain subject to I/Security; schema generation, interoperability, replay/reconnect and H36-CO tests NOT RUN; COC/operator deployment is not approved by H. The schema is a candidate, not generated/frozen/interoperability-tested.

### G — ACCEPT WITH ENUMERATED EXCEPTIONS

G accepts recovery-cutoff batch and pre-batch participant reconciliation as mandatory prerequisites for new Full Applied promotion. Missing/unknown COC order, owner-local pending-gate reconciliation, participant enumeration, I terminal outcome, D complete-lineage barrier or owner high-water proof prevents Full Applied and suppresses protected current use. The batch does not establish C provider success; exact CSubmitOutcome and determinate CausalOrderTerminalProof remain required.

Exceptions: G validator/Applied persistence has not been shown consuming all evidence; same-identity/digest replay, conflict quarantine and restore require executable tests; G-CO/Applied race suites SPECIFIED / NOT RUN; no implementation or production pass.

### B — APPROVE

B approves that the recovery-batch amendment introduces no new B semantic type and does not change PrincipalRef/IssuerRef/ActorRef, role-labelled ScopeBindingSet, EnvironmentRef or typed source/target/lineage identity semantics. Typed refs remain identifiers/attribution, not credentials, authorization receipts, coordinator positions, fence clearances or capabilities. Cross-Scope/Environment access remains deny-by-default; no legacy untyped string is silently cast.

Reservation: C/G/H own consumer field paths and wire representation; H owns recovery-batch wire encoding and requiredness. This is not I governance, deployment, D lineage completeness, Storage visibility atomicity, tests or production readiness.

### Storage — CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY

Storage confirms the exact A/COC package as a logical cross-authority causal-order service, with quorum-committed append-only records, immutable participant identity/digest, fail-closed behavior, durable owner-local pending gates, recovery-cutoff batch and pre-batch participant reconciliation.

The proposed three-voter/two-quorum profile is only a design target for evaluation. Storage does not confirm real independent failure domains, durable media, KMS, RPO/RTO, backup, or operations. This is not operator designation, deployment approval, production readiness, I policy approval or conformance.

## 4. What is actually closed, and what remains open

**Closed at design/interface-decision level:** exact A package/COC companion has current explicit decisions from C, D, G, H, I and B; Storage has a bounded interface confirmation with changes. This is materially stronger than the earlier state and should be reflected in Issue #3 and A's closure tracker.

**Still not closed:**
1. H schema production freeze: the schema remains a candidate; field requiredness/canonicalization for all recovery-batch evidence, generated IDL/SDK, signature/MAC/key lifecycle, parser behavior and interoperability are not fully verified.
2. COC deployment: no named/deployed operator, durable coordinator service, quorum infrastructure, failure-domain placement, runbook, restore/retention or RPO/RTO.
3. I sequencer/receipt service implementation and crash/failover/restore durability unverified.
4. D complete authoritative lineage inventory and late-discovery closure unproven.
5. C provider-specific idempotency and ambiguous-outcome recovery unverified.
6. G Applied validator/persistence implementation and recovery semantics unverified.
7. Storage production Canonical Authority runtime/DB adapter not identified in the inspected repository.
8. C-CO, D-CO, I-CO, G-CO and H36-CO conformance suites remain SPECIFIED / NOT RUN; production implementation is not verified.
9. JF-10 P0 remains OPEN; multi-PolicyDomain remains BLOCKED; production activation NOT AUTHORIZED.

## 5. Integration freshness discrepancy

A's live `reviews/integration/phase-3.6-closure-tracking.md` blob `554d4b85a94f433856506dce4c020b9c00183e69` still ends at §13.43 and records Storage head `df60b547...` with the deep PITR workflow failing. Storage's live branch has since advanced to `3c8ab8ee4579a550300aa48aecab928149cf9370`; its current dossier blob `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1` records the corrected deep PITR run and seven-workflow regression batch PASS on evidence commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`.

The A deployment-binding record correctly retains Gate A PARTIAL PASS / OPEN and production deployment NOT DESIGNATED. The stale part is the detailed evidence freshness in A's closure tracker, not the remaining production blockers. A must refresh its source pins and test-state vector; P cannot update A's Owner record on A's behalf.

## 6. Final verdict

- Exact CGH-APPLIED-1.1 package/companion design decisions: **RECORDED WITH ENUMERATED EXCEPTIONS**.
- Applied Contract Frozen: **NO**.
- Production schema freeze / generated SDK / interoperability: **NO / NOT VERIFIED**.
- COC operator/deployment: **NOT DESIGNATED / NOT DEPLOYED**.
- C/G/D/I/H runtime implementation: **NOT VERIFIED**.
- C-CO/D-CO/I-CO/G-CO/H36-CO tests: **SPECIFIED / NOT RUN**.
- JF-10 P0: **OPEN**.
- Production activation: **NOT AUTHORIZED**.

This assessment corrects the prior version's false statement that C/H exact-version decisions were pending. It does not convert design acceptance into implementation, test, deployment or production approval.


## 7. COC companion and bridge architecture — distinct exact artifacts, decision reconciled

The exact decision vector in §§1–3 remains valid for the exact pair:
- CGH-APPLIED-1.1 package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`;
- companion COC architecture Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.

However, A's current file at the same companion path `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md` is now Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, a later amended version containing the I/JF-10 bridge §§12.1–12.8.

Live Owner evidence:
- C, D, H, I and Storage have separate exact-version acceptance/readback evidence for A COC architecture Blob `a3c51...`.
- C, D, G, H, I and Storage have exact-version decisions for Applied package Blob `4961...` + companion Blob `fc3...`; B approves unchanged B-owned type semantics.
- G's exact Applied decision still pins `4961 + fc3` and does not mention `a3c51`.

A's current Owner acceptance matrix now explicitly distinguishes the roles and records exact decisions for both artifact sets: `4961 + fc3` is the immutable Applied package/companion pair; `a3c51` is the separate COC/JF-10 bridge architecture. The matrix records G's decision for both roles, alongside the other affected Owners. This resolves the prior ambiguity at the design-decision level. No package rewrite is required; do not substitute `a3c51` for the package's pinned `fc3` companion. The new Storage COC protocol/specification is a separate review target and is not covered by either older acceptance set.

Therefore the earlier “design decisions recorded with exceptions” result remains true for the exact old pair, and the separate COC/JF-10 bridge architecture has its own exact acceptance vector. UMR-024 is CLOSED at the design-decision level. The contract is still not frozen because H schema, new COC protocol amendments, implementation and conformance remain open.
