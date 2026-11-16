# I — Phase 3.6 Governance Approval & Consumer Acceptance Register

- Owner: Session I — Security, Identity & Governance
- Branch: `session-i-security-governance-2026-11-16`
- Status: **Technical policy baseline JOINT-DECIDED; all external governance approvals GOVERNANCE-BLOCKED; consumer acceptance OPEN; I36 execution NOT RUN**
- Authority boundary: I organizes and records approval requests. This document is not an approval, does not simulate an approver, and does not activate any policy.

## 1. Live source baseline

| Artifact | Branch | Source HEAD at discovery | Path | Blob SHA |
|---|---|---|---|---|
| I joint trust policy | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| I trust chain / authorization / revocation | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | `74643a2f374179128d506c3b7e1d22da77119600` |
| I threat model / adversarial plan | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` |
| B typed identity closure | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |
| H protected-operation binding | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` |
| H protocol conformance matrix | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/protocol-conformance-matrix.md` | `075b2ac6ebe9bda4ec83de04fad07e8027e6a440` |

## 2. Decision preservation

BIH36-JD-01..17 remain the current delegated technical baseline. This register does not revise type/field semantics. The complete decision text and per-decision ownership are preserved in the I joint trust policy artifact at Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`, §9.3 and §10. Any genuine new conflict, consumer counterexample or security defect must be recorded as a versioned change with impact analysis and renewed approvals; none is asserted by this register.

## 3. Governance approval register

**Approval rule:** every row remains GOVERNANCE-BLOCKED until an authorized approver creates a durable record containing the exact policy text/hash, approver PrincipalRef and Issuer, authority basis, independent reviewer where required, scope/jurisdiction, approval evidence, effective policy version/time, expiry/review and revocation/supersession conditions. No approval evidence or effective version was present in the inspected I/A artifacts. An architect recommendation, commit, or user delegation to make technical decisions is not a governance approval.

| Decision ID | Policy | Proposed by | Approval authority | Approval status | Approval evidence | Effective version | Effective time | Remaining restriction |
|---|---|---|---|---|---|---|---|---|
| I36-GOV-01 | Trusted Issuer admission, federation, trust-domain and key/credential rotation/compromise | I policy owner | Identity/Security Governance; issuer owner; Privacy/Legal where jurisdictional | GOVERNANCE-BLOCKED | None located | None | None | No new issuer/federation activation; explicit local trust only |
| I36-GOV-02 | Principal resolution, collision/alias migration and stable identity policy | I policy owner | Identity Governance + Security Governance; issuer owner for migration assertion | GOVERNANCE-BLOCKED | None located | None | None | No automatic merge/alias; ambiguous or unapproved migration denied |
| I36-GOV-03 | Delegation eligibility, depth, sub-delegation, audience/purpose, expiry and parent revocation | I policy owner | Security Governance + Identity Governance; Legal where agency/consent applies | GOVERNANCE-BLOCKED | None located | None | None | Strict intersection only; sub-delegation disabled by default |
| I36-GOV-04 | ActorRef / Principal binding and verifier attribution policy | I policy owner with B/H technical mapping | Identity/Security Governance; H/I verifier control owners | GOVERNANCE-BLOCKED | None located | None | None | Verifier-produced per-operation binding only; caller-minted ActorRef rejected |
| I36-GOV-05 | Cross-Scope grants, inheritance/sharing algebra and ownership/applicability boundaries | I policy owner; B supplies Scope semantics | Security/Architecture Governance; B domain owner; data/tenant owner | GOVERNANCE-BLOCKED | None located | None | None | Cross-Scope denied absent explicit exact grant |
| I36-GOV-06 | Cross-Environment grants, bridge/federation and EnvironmentRef authority | I policy owner; Environment registry authority not assigned | Security/Architecture Governance; environment owner; data/tenant owner | GOVERNANCE-BLOCKED | None located | None | None | Cross-Environment denied; unresolved registry authority means deny |
| I36-GOV-07 | PermissionEpoch authority, policy-domain partitioning, increment/propagation and revocation ordering | I policy owner | Security Governance; identity/policy platform owner; all affected consumers | GOVERNANCE-BLOCKED | None located | None | None | I remains logical authority; no stale/offline lease; consumers must fail closed |
| I36-GOV-08 | Revocation semantics, in-flight linearization, offline behavior and already-disclosed data handling | I policy owner | Security Governance; D/E/F/G/H/C boundary owners; service owner | GOVERNANCE-BLOCKED | None located | None | None | Current-boundary revalidation; uncertain order pauses/denies |
| I36-GOV-09 | Unsupported Adapter/Producer capability, alternate controls, disablement and residual risk | I policy owner with H/C | Security Governance; H; service/product owner; Privacy/Legal if data leaves control | GOVERNANCE-BLOCKED | None located | None | None | Unsupported is Unknown/blocked; no inferred success |
| I36-GOV-10 | Global Forget authorization, external recipient/backup retention exceptions and physical-erasure policy | I policy owner | Privacy/Legal + Security Governance + data owner + storage/recipient owner | GOVERNANCE-BLOCKED | None located | None | None | No completion exception without explicit scoped approval and evidence |

## 4. Consumer acceptance register

**Acceptance standard:** only an explicit statement by the corresponding consumer Owner, tied to the exact BIH contract version/commit and covering field mapping plus required behavior, qualifies. Reading a document, implementation code, compatible defaults, an A registry entry, or this joint architect's review does not qualify.

The following branch refs are live at discovery. They identify the source snapshot reviewed, not an acceptance signature.

| Consumer | Branch / reviewed HEAD | Contract fields and required behavior | Owner | Acceptance status | Evidence and outstanding action |
|---|---|---|---|---|---|
| C Agent Integration | `session-c-agent-integration-2026-11-16` / `3b6c1d9a5d648f61daa04f5874d887f33475f098` | PrincipalRef, ActorRef, ProducerRef/Adapter identity, ScopeRef, EnvironmentRef, authenticated transport binding, PermissionEpoch/revocation, payload mismatch rejection, Unknown/Unsupported fail-closed | C | OPEN — no explicit acceptance | `07-agent-integration/conformance-matrix.md` is a test specification marked not run. C Owner must explicitly accept exact BIH fields/behaviors and add any consumer-side contract mapping. |
| D Memory Brain | `session-d-memory-brain-2026-11-16` / `968ce314cf2e44f50e3efd711060e495374cac98` | Principal/Actor/Scope/Environment at canonical mutation; current PermissionEpoch and revocation at commit; forged identity rejected; Unknown blocks | D | OPEN — no explicit acceptance | D Forget/fence contract is not identity consumer sign-off. D Owner must accept exact operation-boundary checks. |
| E Memory Compiler | `session-e-memory-compiler-2026-11-16` / `e3afa99728f399d154767c959e37ff38f651b4b6` | Authenticated Producer/Adapter identity; Scope/Environment; current PermissionEpoch/revocation at admission/publication; reject forged producer and unsupported identity | E | OPEN — no explicit acceptance | E producer/publication conformance is a design specification; E Owner must explicitly accept ingress and final visibility checks. |
| F Memory Runtime | `session-f-memory-runtime` / `2da5209d7072272d5510d376c0f319bed0402a6f` | Principal/Actor/Scope/Environment before retrieval/candidate exposure; current epoch/revocation; no side channel; forged claims and unknown refs rejected | F | OPEN — no explicit acceptance | Runtime suppression contract is not identity acceptance. F Owner must accept candidate and cache boundaries. |
| G Context Manager | `session-g-memory-context` / `ac32e980003aa41faf0ae958ffef3df5ab387984` | Principal/Actor/Scope/Environment; authenticated Adapter/session ACK; PermissionEpoch/revocation; old-session replay and unknown/unsupported suppression | G | OPEN — no explicit acceptance | Applied/Forget reconciliation contract is not explicit BIH acceptance. G Owner must accept delivery, ACK and final applied checks. |
| H BMCP | `session-h-bmcp-protocol` / `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | Protected authenticated transport binding; Principal/Actor/Producer/Adapter; Scope/Environment; PermissionEpoch; payload identity mismatch; ACK/reconnect and Unknown/Unsupported fail-closed | H | OPEN as consumer-owner acceptance | H technical binding is jointly decided under delegated authority; H36 runtime tests NOT RUN; no separate H consumer acceptance record. |
| Storage/Consistency | `session-storage-consistency-forget-atomicity-2026-11-16` / `c0d01d81698fa6bc2a22e84b0e2ada66ce329815` | Authenticated protected-operation context and current PermissionEpoch at commit/visibility; revocation ordering; forged/unknown identities rejected; no prepared artifact exposure | Storage | OPEN — no explicit acceptance | Storage realization review is proposed design, explicitly not implemented/verified. Storage owner must accept exact final-commit gate and evidence. |
| A Integration Registry | `session-a-integration-2026-11-16` / `9c3dafb97b97aee50a8b61fe60836ed0a8e92fe3` | Record exact owner branches, contract fields, statuses and evidence without inferring acceptance | A | OPEN — registry role only | A is coordinator/registrar, not consumer approval authority. A may register only after each owner supplies explicit evidence. |

### Required consumer response fields

Each consumer owner must add a durable record in its own branch with: BIH contract commit/Blob SHA; each of PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Producer/Adapter identity, authenticated transport, PermissionEpoch, revocation, forged-payload rejection and Unknown/Unsupported behavior; accepted/rejected/conditional disposition per field; exact local enforcement boundary; compatibility impact; owner identity and approval timestamp. Until then, status remains OPEN.

## 5. I36 test execution ledger

The I36 adversarial plan and H36 matrix are specifications, not executions. No executable implementation build, test command, fixture output, runtime environment, logs, or owner-signed result was available in the reviewed branches. All test cases remain NOT RUN.

| Test ID | Scenario | Required result | Environment / command / input / actual / evidence | Status |
|---|---|---|---|---|
| I36-T01 | Forged PrincipalRef | Reject payload mismatch | No runtime/build/command/log supplied | NOT RUN |
| I36-T02 | Forged ActorRef | Reject caller-minted/unbound ActorRef | No runtime/build/command/log supplied | NOT RUN |
| I36-T03 | Unknown Issuer/key | Deny/indeterminate; no TOFU | No runtime/build/command/log supplied | NOT RUN |
| I36-T04 | Revoked Issuer/key | Reject new auth; invalidate dependent sessions/grants | No runtime/build/command/log supplied | NOT RUN |
| I36-T05 | Expired delegation/parent grant | Deny delegate and descendants | No runtime/build/command/log supplied | NOT RUN |
| I36-T06 | Delegation cycle/depth/amplification | Deny chain | No runtime/build/command/log supplied | NOT RUN |
| I36-T07 | Stale PermissionEpoch/cached ALLOW | Deny/pause | No runtime/build/command/log supplied | NOT RUN |
| I36-T08 | PermissionEpoch gap/authority unavailable | Pause and reconcile | No runtime/build/command/log supplied | NOT RUN |
| I36-T09 | Cross-Scope access | Deny absent explicit grant | No runtime/build/command/log supplied | NOT RUN |
| I36-T10 | Cross-Environment access | Deny absent exact bridge/grant | No runtime/build/command/log supplied | NOT RUN |
| I36-T11 | Unauthorized/forged Producer | Reject before enqueue/compile | No runtime/build/command/log supplied | NOT RUN |
| I36-T12 | Unauthorized/forged Adapter | Reject; managed region suppressed | No runtime/build/command/log supplied | NOT RUN |
| I36-T13 | Revocation vs E publication | Staged artifact remains private; publication denied if revocation wins | No runtime/build/command/log supplied | NOT RUN |
| I36-T14 | Revocation vs F retrieval | No candidate/count/snippet disclosure | No runtime/build/command/log supplied | NOT RUN |
| I36-T15 | Revocation vs G/H delivery/apply | Cancel/quarantine; reconnect reauthenticates | No runtime/build/command/log supplied | NOT RUN |
| I36-T16 | Revocation vs C final submission | No submit if revocation wins; no false Full Applied | No runtime/build/command/log supplied | NOT RUN |
| I36-T17 | PermissionEpoch substituted for ForgetFence | Reject typed namespace mismatch | No runtime/build/command/log supplied | NOT RUN |
| I36-T18 | Revocation after disclosure | No false recall; block future access and start recipient workflow | No runtime/build/command/log supplied | NOT RUN |
| I36-T19 | Requester revoked after Forget fence | Obligation persists; current continuity principal only | No runtime/build/command/log supplied | NOT RUN |
| I36-T20 | Unsupported Adapter/offline recipient during Global Forget | Unknown/Pending; no completion absent approved exception | No runtime/build/command/log supplied | NOT RUN |

## 6. H36 test execution ledger

| Test ID | Scenario | Required result | Environment / command / input / actual / evidence | Status |
|---|---|---|---|---|
| H36-01 | Forged PrincipalRef | Protected Principal remains source of truth; reject mismatch | No runtime/build/command/log supplied | NOT RUN |
| H36-02 | Forged ActorRef | Reject caller-minted/mismatched ActorRef | No runtime/build/command/log supplied | NOT RUN |
| H36-03 | Forged ProducerRef | Require authenticated workload registration | No runtime/build/command/log supplied | NOT RUN |
| H36-04 | Unknown Issuer | Reject before Principal resolution | No runtime/build/command/log supplied | NOT RUN |
| H36-05 | Revoked Issuer/key | Reject and invalidate session | No runtime/build/command/log supplied | NOT RUN |
| H36-06 | Expired Credential | Reject at reconnect/protected boundary | No runtime/build/command/log supplied | NOT RUN |
| H36-07 | Expired Delegation | Deny; no grantor fallback | No runtime/build/command/log supplied | NOT RUN |
| H36-08 | Revoked Delegation | Deny and require current epoch | No runtime/build/command/log supplied | NOT RUN |
| H36-09 | Stale PermissionEpoch | Reject protected operation | No runtime/build/command/log supplied | NOT RUN |
| H36-10 | Cross-Scope | Deny absent explicit grant | No runtime/build/command/log supplied | NOT RUN |
| H36-11 | Cross-Environment | Deny absent exact bridge/grant | No runtime/build/command/log supplied | NOT RUN |
| H36-12 | Authenticated Principal / payload Actor mismatch | Reject/quarantine and audit | No runtime/build/command/log supplied | NOT RUN |
| H36-13 | Old Session ACK replay | Historical only; no new-session mutation | No runtime/build/command/log supplied | NOT RUN |
| H36-14 | Reconnect during revocation | No resume before fresh auth/epoch/fence/reconcile | No runtime/build/command/log supplied | NOT RUN |
| H36-15 | Unauthorized Forget | Deny before target/fence mutation | No runtime/build/command/log supplied | NOT RUN |
| H36-16 | ACK ID reused with different digest | IDEMPOTENCY_CONFLICT; no state change | No runtime/build/command/log supplied | NOT RUN |
| H36-17 | Missing required Scope/Environment | Deny; no wildcard/default | No runtime/build/command/log supplied | NOT RUN |
| H36-18 | Protocol major downgrade | VERSION_UNSUPPORTED; no weakened auth | No runtime/build/command/log supplied | NOT RUN |

H36-SR-02/SR-03/SR-04/SR-05/SR-07 additional cases remain mandatory and NOT RUN: channel-binding mismatch; cross-session/audience replay; nonce reuse; duplicate-key canonicalization; missing/unknown requiredness profile; suppressed EnvironmentRef; cross-Adapter ACK ID collision; ACK same-ID/different-digest; ACK/revocation race both orders; reconnect after Adapter replacement; capability downgrade; sequencer/epoch race and multi-domain coordinator failure.

## 7. B/I/H confirmation and governance separation

- B domain type confirmation: joint technical baseline preserved; no separate B-session signature claimed.
- I governance confirmation: I policy technical baseline preserved; external approvals remain GOVERNANCE-BLOCKED.
- H protocol binding confirmation: joint technical baseline preserved; no separate H-session signature claimed.
- Cross-module technical agreement: B/I/H only, under delegated joint technical decision.
- Consumer acceptance: OPEN for C/D/E/F/G/H/Storage; A is registrar only.
- Test evidence: I36 and H36 NOT RUN.
- Fact/Claim ADR-001: independently ADR-BLOCKED. No status change is made by this register.

## 8. Exit criteria

This phase cannot close until: (1) each I36-GOV-01..10 has formal approval evidence or remains explicitly blocked; (2) each consumer owner records acceptance/rejection against exact BIH commit; (3) I36/H36 tests execute on identified builds with reproducible fixtures/logs and owner sign-off; (4) cross-module discrepancies are resolved by the authority that owns the affected contract. No branch merge is authorized by this record.
