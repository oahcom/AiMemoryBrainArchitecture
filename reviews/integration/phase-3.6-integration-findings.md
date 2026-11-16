# Phase 3.6 — Integration Findings Register (Live Reconciliation)

- Owner: Session A — Principal Integration Architect
- Branch: session-a-integration-2026-11-16
- Baseline source snapshot: A HEAD 70552cb4d232da657a16dc469ebf6d5ca10f2624
- Status: OPEN FINDINGS; NO CONTRACT FREEZE
- Authority rule: A records cross-module findings and assigns decision authority. A does not decide I policy, D Forget semantics, E producer semantics, Storage physical realization, B domain semantics, H wire semantics, C final-request evidence or G Applied state.

## Findings

| ID | Severity | Finding / evidence | Decision authority | Required closure evidence | State |
|---|---|---|---|---|---|
| A36-P0-01 JF-10 owner-gate ordering | P0 | D/E candidate Blob ff83abbad8172d4efec5a7f088064f31f21844b9 is explicitly Candidate. I correction Blob 57474cfb0c5da07a2cbcbeff1fc792ced36c5dd6 says an earlier standalone COMMIT_WON followed by independent Storage commit does not satisfy I36-SR-02. | I owns policy-domain order/receipt; D owns ForgetFence; Storage owns visibility transaction; E owns producer lifecycle | Joint D/E/Storage protocol revision accepted by I, exact participant/linearization and D-fence ordering, crash/recovery matrix, implementation traces and JF10 cases | OPEN / P0 |
| A36-P0-02 Global Producer Inventory and Forget seal | P0 | I inventory/Completion artifact remains Candidate; no ProducerDomainInventoryEpoch/InventorySealReceipt seal evidence; I36-GOV-07/08 blocked. Repository issue #4 remains OPEN. | I owns global inventory, seal and Global Forget policy; each producer/recipient/backup owner supplies registration | Named authority, closed-world membership, epoch/digest, seal signer/verifier, exclusions/late discovery, recipient/backup coverage and approved completion evidence | OPEN / P0 |
| A36-P0-03 Authorization governance and Environment authority | P0 | I register Blob 11c4bfde5de02a684cc6e5df46d1f9676f5a40a5 states I36-GOV-01..10 GOVERNANCE-BLOCKED; no approval evidence/effective version. Environment Registry Authority unassigned. | I plus named independent Security/Identity/Data/Scope/Environment/Privacy/Legal approvers as applicable | Exact approved policy hash, approver PrincipalRef/Issuer and authority basis, jurisdiction, effective version/time, expiry/review, Environment Registry Authority designation | OPEN / P0 |
| A36-P0-04 Storage concrete deployment and verification | P0 | Storage Blob 765b10978813680985a71600e82fc15caa75bf2c selects a logical local transactional profile only. Concrete engine/runtime deployment and named independent engineering approver remain blocked; deployment implemented NO. | Storage engineering/platform owner; Storage documents realization | Concrete engine/version/topology, isolation/linearizability, failover/restore, named approver, code/build SHA, durable receipts and D36/E36/C01-C20 results | OPEN / P0 |
| A36-P0-05 BIH consumer and governance closure | P0 | BIH36-JD-01..17 are jointly decided. D/E/H/Storage have design-level acceptance artifacts; C/F/G remain OPEN. I36/H36 NOT RUN. | I owns policy; each consumer Owner accepts its own mapping; B/H/I own technical domains | I governance approvals; C/F/G acceptance pinned to exact B/I/H version; all mandatory I36/H36 cases executed and reviewed | PARTIAL / BLOCKED |
| A36-P0-06 C/G/H Applied common version | P0 | C Blob 8db1140f0dd19fe9267e3f2b44a9c1be75a6c32b, G Blob 8f6b215de7b78bf0eec2281359d3e039e7c8d5f4 and H protocol binding are distinct artifacts. No common Applied schema release/digest or C/G/H approval exists. | C owns final-request evidence; G owns Applied; H owns wire/ACK/capability; D/I/B confirm predicates | One canonical version/digest, field and state mapping, replay/late-ACK/reconnect rules, explicit same-version C/G/H approval and D/I/B confirmations | OPEN / P0 |
| A36-P0-07 Runtime and cross-module conformance | P0 | D36/E36/C01-C20, I36/H36, CFG-01..20 and PI-01..08 are specifications; no execution evidence supplied. | Each test-owning module and Storage; A tracks evidence | Identified builds, deterministic fixtures/order, commands, expected/actual outputs, traces/logs, retained evidence and Owner review | NOT RUN |
| A36-P1-01 Fact/Claim ADR isolation | P1 / scope-dependent | B explicitly keeps ADR-001 ADR-BLOCKED. Identity closure does not resolve Fact/Claim semantics. | B domain owner and designated ADR governance authority | Separate ADR decision and consumer mapping before any dependent schema/wire freeze | ADR-BLOCKED |

## Preserved completed work

1. DE-S logical Forget/producer/storage architecture and two-round six-dimension design review remain closed. No redesign is requested absent new evidence.
2. BIH36-JD-01..17 remain the delegated joint technical baseline. Governance approval and consumer acceptance are separate dimensions.
3. C/F/G semantic contracts remain delivered. C Final Request Submitted, G Applied and F suppression semantics are preserved.
4. Typed cursor/authority namespaces remain distinct; no A registry edit can collapse their owners or ordering semantics.

## Integration disposition

No finding is closed by document presence alone. An Owner decision, cross-owner acceptance, external governance approval, implementation evidence and test pass are recorded as separate dimensions. A finding closes only when the exact required evidence is fetched from its authority Owner branch and revalidated against live HEADs.


## Consumer acceptance status refresh — C/F/G BIH decisions verified (2026-11-16)


Issue #6 comment `6919556745` records C, F and G each accepting the exact A BIH package Blob `a45ae90b318a79bf009d14f4d917611881e9e214` with enumerated exceptions. A independently fetched the three Owner artifacts from their respective branches and verified exact Blob matches:

- C: `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`
- F: `ce59252dbbdc5d10d016704797e9ba12d5a941bd`
- G: `5406b3f2558daa3f5915f6bb46e808be8d90d3ca`

**A36-P0-05 is updated to PARTIAL / BLOCKED:** C/F/G BIH consumer acceptance is COMPLETE — ACCEPTED WITH ENUMERATED EXCEPTIONS. The finding remains open because I36-GOV-01..10 external governance approvals and I36/H36 runtime verification are independent outstanding requirements.

**A36-P0-06 remains OPEN / P0.** C/F/G BIH consumer acceptance does not itself establish a common C/G/H Applied contract schema version/digest, same-version C/G/H acceptance, D/I/B predicate closure, or runtime conformance. Do not close this finding on the basis of Issue #6 comment 6919556745.

No runtime suite is upgraded from NOT RUN. No governance approval, implementation conformance, production readiness or G10 closure is inferred.


## A36-P0-06 update — CGH-APPLIED-1.1 successor source reconciliation (2026-11-16)

The C/I/D causal-order protocol has advanced to published Owner specifications with explicit ParticipantIntentRef admission cutoff, I receipt-consumption outcome, D fence-request cutoff, final ParticipantReservationRef, actual C provider outcome and common terminal proof. This closes a specification ambiguity, not the cross-owner acceptance gate.

The current A candidate is `CGH-APPLIED-1.1`, Blob `9808b31f840606b329f1a794935dfc9c5084d63b`. It pins C `f2c5b379cacfedd81500e8496d3053b628e144a0`, D `317a9bc170c5a66720f738bf24bbf93c87385887`, I `71779133a4f95d63a24c4c7e606af174763366f1`, and H `5cbf0bb548a46671054cb22c6fab3c3d007365d4`. Existing G and B decisions remain semantic/1.0 baselines and are not exact 1.1 acceptance.

Issue #3 comment `6920297962` requests fresh exact-package decisions against this exact Blob from C/D/I/H/G/B. The coordinator/Storage operator remains unnamed and deployment/HA/failover/restore acceptance remains absent. H 1.1.0 is a schema candidate, not production-frozen or deployed. C-CO/I-CO/D-CO/H36-CO/G 1.1 conformance remains NOT RUN. **A36-P0-06 remains OPEN / P0**; Applied Contract Frozen NO.
