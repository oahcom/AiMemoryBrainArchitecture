# Session C — Phase 3 Targeted Remediation Decision Change Log

- Owner: Session C
- Branch: session-c-agent-integration-2026-11-16
- Baseline before this round: 3dc476b096c5491c6153e9e6b78235e1383913aa
- Date: 2026-11-16
- Status: C-owned requirements updated; cross-owner contracts remain candidate/open.

## 1. Changes

| ID | Change | Status / boundary |
|---|---|---|
| C-DEC-21 | Complete telemetry identity tuple and three-layer trust chain | C consumption requirement DECIDED; H/I/B dependencies OPEN |
| C-DEC-22 | Per-class identity, Scope, Environment and Permission validation | C-side requirement DECIDED; I algorithm not owned by C |
| C-DEC-23 | Task State, Active Entities and Risk Signal semantics | C taxonomy DECIDED; no canonical write authority |
| C-DEC-24 | Duplicate, out-of-order, late, gap, clock-skew and correction semantics | Semantic requirement DECIDED; H/E implementation mapping OPEN |
| C-DEC-25 | Prepared/Delivered/Applied/Submitted/Execution Started split | DECIDED; G/H own state/wire |
| C-DEC-26 | Full Applied tuple expanded to identity/session/request/Context/Delivery/region/epochs/digest/boundary | Semantic requirement DECIDED; encoding/signing OPEN |
| C-DEC-27 | Final submit race requires current version/permission/fence at linearization | Safety outcome DECIDED; concrete protocol candidate |
| C-DEC-28 | Forget/Clear/Reconnect Agent capability matrix | Agent requirements DECIDED; no global completion claim |
| C-DEC-29 | Untrusted Memory boundary and eight Prompt Injection cases | Agent boundary DECIDED; I risk acceptance OPEN |
| C-DEC-30 | Tier 1/2/3 aligned to H terminology | C classification DECIDED; H wire mapping OPEN |
| C-DEC-31 | Cross-module map and exact dependency snapshots | C ownership statement DECIDED; external candidates not approved |

## 2. Exact current source snapshots inspected

| Module | Branch | HEAD | Inspection/status |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | e270118dd22e47140a5232f5f131d97e965d39dc | Coordination baseline |
| B | session-b-domain-model-phase3 | ab19afbf92f67fe0a7679e9aa3a35b015fed89f4 | Typed Reference/Scope candidate; ADR-001 ADR-BLOCKED |
| C | session-c-agent-integration-2026-11-16 | 3dc476b096c5491c6153e9e6b78235e1383913aa | Pre-round baseline |
| D | session-d-memory-brain-2026-11-16 | 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6 | Canonical refs/ForgetFence consumer dependency |
| G | session-g-memory-context | 3d2c065be863bc1d349faaeece6f6eaa0047abae | Context architecture/versioning/reconciliation; no separate Applied consumer or Forget/reconnect extension file at this HEAD |
| H | session-h-bmcp-protocol | fcc5103399b4c322e52d642cae5a2414969399a7 | Envelope, Delivery/ACK, capability/Applied and Forget/reconnect candidates |
| I | session-i-security-governance-2026-11-16 | 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb | Principal/Actor, Scope/revocation, global Forget evidence vector and threat model candidates |

HEADs were fetched from current GitHub branch refs during this round; they are exact inspected snapshots, not a guarantee that branches cannot move.

## 3. Cross-module OPEN register

| Item | Owner(s) | Status | C position |
|---|---|---|---|
| Principal/issuer/ProducerIdentity and authenticated transport binding | I/H | OPEN candidate | Require proof; payload IDs are claims |
| ActorRef/ScopeRef types and B/I mapping | B/I | OPEN candidate | Consume typed refs only |
| Permission Epoch issuance, partition and consistency | I | OPEN candidate | Carry/revalidate opaque epoch; fail closed |
| BMCP identity/capability/Applied ACK encoding | H | OPEN candidate | C supplies semantic requirements |
| ContextVersion/ChangeSet/Delivery mapping | G | OPEN integration | Bind evidence to exact target |
| Applied state transition and late ACK | G/H | OPEN integration | C supplies request proof; G decides state |
| ForgetFence and H/G target mapping | D/H/G/I | OPEN integration | C validates freshness; no fence authority |
| Global Forget completion/external copies | I | OPEN | C reports local coverage only |
| Prompt Injection risk acceptance | I + Agent/product security | OPEN | C defines tests, not acceptance |
| E receipt/sequence/idempotency alignment | E/H/C/I | OPEN | C defines source semantics |
| Fact/Claim ADR | B + Architecture Governance | ADR-BLOCKED | C does not approve |

## 4. Status discipline

DECIDED means C-owned semantics/Agent requirements only. CANDIDATE means implementation profile awaiting owner agreement. OPEN means external decision, mapping or implementation evidence is absent. ADR-BLOCKED prevents canonical schema/type freeze. TO_VALIDATE requires executable evidence. No item here marks INT-P0-02, INT-P0-04, CR-P1-05 or INT-X-03/04 globally CLOSED.


## Phase 3.5 — 2026-11-16 — Identity, final-submit and untrusted-memory conformance

- Added `phase-3.5-agent-identity-applied-attestation-untrusted-memory.md` as the consolidated C-owned consumer contract.
- Separated authenticated Principal, payload Agent identity, Adapter identity, Runtime Session, Task Identity, ActorRef, ScopeRef, EnvironmentRef and I PermissionEpoch.
- Added per-signal telemetry identity/scope/environment/time/provenance/trust requirements and explicit non-equivalence rules.
- Tightened Full Applied to require exact final immutable request submission observability and the complete Agent/Adapter/session/request/Context/Delivery/Managed Region/Permission/Fence/Capability/digest/boundary binding.
- Clarified Suppress/Clear/Purge/Cancel/Revalidate/Reconnect and fail-closed behavior.
- Expanded adversarial tests PI35-01..12. Tests remain NOT EXECUTED; INT-P0-04 remains OPEN.
- Superseded ambiguous Tier 2 wording: Tier 2 cannot claim Full Applied without actual final submission evidence.
- Upstream B/I/H/G/D artifacts were read at recorded branch heads; no upstream files modified and no candidate status promoted.
