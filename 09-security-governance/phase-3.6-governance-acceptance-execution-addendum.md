# I — Phase 3.6 Governance Approval & I36 Execution Addendum

- Owner: Session I — Security, Identity & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Parent HEAD: `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb`
- Status: **Technical policy baseline JOINT-DECIDED; all external approvals GOVERNANCE-BLOCKED; consumer acceptance OPEN; I36 NOT RUN**
- This is an I-owned evidence/status record. It does not grant approval, impersonate an authority, activate a policy or sign for a consumer.

## 1. Live I source baseline

| Artifact | Branch | HEAD at discovery | Blob SHA |
|---|---|---|---|
| Joint trust policy | `session-i-security-governance-2026-11-16` | `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| Principal trust / authorization / revocation | same | same | `74643a2f374179128d506c3b7e1d22da77119600` |
| Governance approval / consumer register | same | same | `695e27d775ebaefc1b83081519db36f105b414c4` |
| Threat model / adversarial test plan | same | same | `4227ac0e26228ca3504589efdee022b5d0802e12` |

Related current technical source refs:
- B HEAD `da4bb48b785bd4c299bb871a2421b37bd6cfb178`.
- H HEAD `cbef9b7f3d118da6a826aec0bc98faf246672d9a`.

## 2. Decision preservation

BIH36-JD-01..17 remain JOINT-DECIDED and unchanged. No new conflict, consumer counterexample or security defect is asserted by this addendum. Any future change requires versioned impact analysis and renewed approval.

## 3. Formal governance approval register

Approval rule: each item remains GOVERNANCE-BLOCKED until the authorized external authority creates durable evidence bound to exact policy text/hash, approver identity and authority basis, scope, effective version/time, review/expiry and revocation/supersession conditions. No such evidence was located in the reviewed artifacts. I cannot approve its own policy by writing this record.

| Decision ID | Policy | Proposed by | Approval authority | Approval status | Approval evidence | Effective version | Effective time | Remaining restriction |
|---|---|---|---|---|---|---|---|---|
| I36-GOV-01 | Trusted Issuer admission, federation, trust-domain, key/credential rotation and compromise | I | Identity/Security Governance; issuer owner; Privacy/Legal where applicable | GOVERNANCE-BLOCKED | None located | None | None | No new issuer/federation activation; explicit local trust only |
| I36-GOV-09 | Principal resolution, collision/alias migration and stable identity policy | I | Identity Governance + Security Governance; issuer owner for migration assertion | GOVERNANCE-BLOCKED | None located | None | None | No automatic merge/alias; ambiguous migration denied |
| I36-GOV-02 | Delegation eligibility, depth, sub-delegation, audience/purpose, expiry and parent revocation | I | Security Governance + Identity Governance; Legal where applicable | GOVERNANCE-BLOCKED | None located | None | None | Strict intersection; sub-delegation disabled by default |
| I36-GOV-10 | ActorRef / Principal binding and verifier attribution policy | I with B/H mapping | Identity/Security Governance; H/I verifier control owners | GOVERNANCE-BLOCKED | None located | None | None | Verifier-produced per-operation binding only |
| I36-GOV-03 | Cross-Scope grants, inheritance/sharing algebra and ownership/applicability boundaries | I; B supplies semantics | Security/Architecture Governance; B domain owner; data/tenant owner | GOVERNANCE-BLOCKED | None located | None | None | Cross-Scope denied absent exact current grant |
| I36-GOV-04 | Cross-Environment grants, bridge/federation and EnvironmentRef authority | I; Environment registry authority unassigned | Security/Architecture Governance; environment owner; data/tenant owner | GOVERNANCE-BLOCKED | None located | None | None | Cross-Environment denied; unresolved registry authority means deny |
| I36-GOV-06 | PermissionEpoch authority, policy-domain partitioning, increment/propagation and revocation ordering | I | Security Governance; identity/policy platform owner; affected consumers | GOVERNANCE-BLOCKED | None located | None | None | I remains logical authority; stale/offline lease prohibited |
| I36-GOV-05 | Revocation semantics, in-flight linearization, offline behavior and disclosed-data handling | I | Security Governance; D/E/F/G/H/C boundary owners; service owner | GOVERNANCE-BLOCKED | None located | None | None | Current-boundary revalidation; uncertain order pauses/denies |
| I36-GOV-07 | Unsupported Adapter/Producer capability, alternate controls, disablement and residual risk | I with H/C | Security Governance; H; service/product owner; Privacy/Legal if applicable | GOVERNANCE-BLOCKED | None located | None | None | Unsupported is Unknown/blocked; no inferred success |
| I36-GOV-08 | Global Forget authorization, recipient/backup retention exceptions and physical-erasure policy | I | Privacy/Legal + Security Governance + data owner + storage/recipient owner | GOVERNANCE-BLOCKED | None located | None | None | No completion exception without scoped approval and evidence |

Decision-ID continuity is intentional: existing I36-GOV-01..08 retain their original meanings; Principal Resolution and ActorRef/Principal Binding use I36-GOV-09 and I36-GOV-10. No silent renumbering.

## 4. Consumer acceptance register

Acceptance requires an explicit statement by the corresponding Owner against exact BIH contract version/commit. Artifact presence, code, default compatibility, A registration or this I record is not acceptance.

| Consumer | Fields / required behavior awaiting explicit acceptance | Owner | Status | Required evidence |
|---|---|---|---|---|
| C | PrincipalRef, ActorRef, Producer/Adapter, ScopeRef, EnvironmentRef, authenticated transport, epoch/revocation, forged identity rejection, Unknown/Unsupported | C | OPEN | C Owner signed acceptance/rejection against exact BIH refs |
| D | Principal/Actor/Scope/Environment at canonical mutation; epoch/revocation at commit; forged/unknown rejection | D | OPEN | D Owner operation-boundary acceptance |
| E | authenticated Producer/Adapter, Scope/Environment, epoch/revocation at ingress/publication; forged producer rejection | E | OPEN | E Owner ingress and publication acceptance |
| F | Principal/Actor/Scope/Environment before retrieval/candidate; current epoch/revocation; no side channel | F | OPEN | F Owner retrieval/cache acceptance |
| G | Principal/Actor/Scope/Environment; authenticated Adapter/session ACK; epoch/revocation; stale/unknown suppression | G | OPEN | G Owner delivery/ACK/applied acceptance |
| H | protected transport identity, typed refs, PermissionEpoch, ACK/reconnect and fail-closed behavior | H | OPEN as separate consumer acceptance | H Owner explicit acceptance and runtime proof |
| Storage | authenticated commit context, current PermissionEpoch and durable revocation ordering | Storage | OPEN | Storage Owner acceptance and transaction evidence |
| A | source refs/status registration | A | Registrar only | A cannot approve on behalf of consumers |

No acceptance is recorded for any of the ten required identity/security behavior checks at the individual consumer level. The fields requiring explicit acknowledgement include PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Producer/Adapter identity, authenticated transport binding, PermissionEpoch validation, revocation, forged payload identity rejection and Unknown/Unsupported handling.

## 5. I36 test execution

Authoritative specification: `09-security-governance/threat-model-and-adversarial-test-plan.md` §Phase 3.6, with detailed requirements in `phase-3.6-principal-trust-chain-authorization-revocation.md` §9.

| Test IDs | Coverage | Execution environment | Command | Input / expected / actual | Evidence | Status |
|---|---|---|---|---|---|---|
| I36-T01..T20 | Forged Principal/Actor; unknown/revoked issuer; expired/revoked delegation; stale/gapped epoch; cross-Scope/Environment; Producer/Adapter spoof; revocation races at E/F/G/H/C boundaries; epoch/fence confusion; post-disclosure revocation; unauthorized cleanup; unsupported recipient | No executable environment supplied | No runnable test command found | Specified expected outcomes; actual not executed | No logs/artifacts | NOT RUN |

The full 20-case specification is retained without reduction. In addition, the adversarial plan's broader SEC-001..042 and race/fault gates remain applicable; this addendum does not mark any of them passed.

Repository discovery across B/I/H/C/D/E/F/G/A/Storage branch trees found Markdown artifacts only: no executable source, test runner, fixtures or workflow definitions. Consequently this repository snapshot supplies no truthful executable command or environment for I36. No test is PASS or FAIL.

## 6. Joint confirmation and blockers

- B domain type confirmation: delegated technical baseline preserved; separate human signature not claimed.
- I governance: policy technical baseline JOINT-DECIDED; formal external approvals remain GOVERNANCE-BLOCKED.
- H protocol binding: delegated technical baseline preserved; separate human signature not claimed.
- Cross-module technical agreement: B/I/H baseline only.
- Consumer acceptance: OPEN for C/D/E/F/G/H/Storage; A is registrar only.
- I36 execution: NOT RUN.
- Fact/Claim ADR-001: independently ADR-BLOCKED; no change.

No branch merge or policy activation is authorized by this record.


## 7. Consumer field-by-field acceptance matrix

Legend: **OPEN** means no explicit acceptance evidence was found for this field/behavior on the consumer Owner branch. It is not a claim that the consumer implementation necessarily lacks the behavior. A source document or compatible implementation is not acceptance.

| Consumer | PrincipalRef | ActorRef | ScopeRef | EnvironmentRef | Producer/Adapter Identity | Authenticated Transport Binding | PermissionEpoch Validation | Revocation | Forged Payload Identity Rejection | Unknown / Unsupported Handling |
|---|---|---|---|---|---|---|---|---|---|---|
| C Agent Integration | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| D Memory Brain | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| E Memory Compiler | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| F Memory Runtime | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| G Context Manager | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| H BMCP | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Storage/Consistency | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| A Integration Registry | N/A — registrar, not consumer approver | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

For C/D/E/F/G/H/Storage, every cell remains OPEN pending an explicit statement by that Owner tied to the exact BIH contract version/commit. No acceptance is inferred from the documents read during this review.
