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
| I36-GOV-09 (new; preserves existing I36-GOV-02) | Principal resolution, collision/alias migration and stable identity policy | I policy owner | Identity Governance + Security Governance; issuer owner for migration assertion | GOVERNANCE-BLOCKED | None located | None | None | No automatic merge/alias; ambiguous or unapproved migration denied |
| I36-GOV-02 | Delegation eligibility, depth, sub-delegation, audience/purpose, expiry and parent revocation | I policy owner | Security Governance + Identity Governance; Legal where agency/consent applies | GOVERNANCE-BLOCKED | None located | None | None | Strict intersection only; sub-delegation disabled by default |
| I36-GOV-10 (new) | ActorRef / Principal binding and verifier attribution policy | I policy owner with B/H technical mapping | Identity/Security Governance; H/I verifier control owners | GOVERNANCE-BLOCKED | None located | None | None | Verifier-produced per-operation binding only; caller-minted ActorRef rejected |
| I36-GOV-03 | Cross-Scope grants, inheritance/sharing algebra and ownership/applicability boundaries | I policy owner; B supplies Scope semantics | Security/Architecture Governance; B domain owner; data/tenant owner | GOVERNANCE-BLOCKED | None located | None | None | Cross-Scope denied absent explicit exact grant |
| I36-GOV-04 | Cross-Environment grants, bridge/federation and EnvironmentRef authority | I policy owner; Environment registry authority not assigned | Security/Architecture Governance; environment owner; data/tenant owner | GOVERNANCE-BLOCKED | None located | None | None | Cross-Environment denied; unresolved registry authority means deny |
| I36-GOV-06 | PermissionEpoch authority, policy-domain partitioning, increment/propagation and revocation ordering | I policy owner | Security Governance; identity/policy platform owner; all affected consumers | GOVERNANCE-BLOCKED | None located | None | None | I remains logical authority; no stale/offline lease; consumers must fail closed |
| I36-GOV-05 | Revocation semantics, in-flight linearization, offline behavior and already-disclosed data handling | I policy owner | Security Governance; D/E/F/G/H/C boundary owners; service owner | GOVERNANCE-BLOCKED | None located | None | None | Current-boundary revalidation; uncertain order pauses/denies |
| I36-GOV-07 | Unsupported Adapter/Producer capability, alternate controls, disablement and residual risk | I policy owner with H/C | Security Governance; H; service/product owner; Privacy/Legal if data leaves control | GOVERNANCE-BLOCKED | None located | None | None | Unsupported is Unknown/blocked; no inferred success |
| I36-GOV-08 | Global Forget authorization, external recipient/backup retention exceptions and physical-erasure policy | I policy owner | Privacy/Legal + Security Governance + data owner + storage/recipient owner | GOVERNANCE-BLOCKED | None located | None | None | No completion exception without explicit scoped approval and evidence |



**Decision-ID continuity:** the pre-existing I36-GOV-01..08 identifiers are retained with their original meanings from the I Owner trust-chain register. The two additional requested approval topics—Principal Resolution and ActorRef/Principal Binding—are newly allocated I36-GOV-09 and I36-GOV-10. This register does not silently renumber or supersede existing governance decisions.

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
- Consumer acceptance: **DESIGN-ACCEPTED for C/D/E/F/G/Storage** against A BIH package Blob `a45ae90b318a79bf009d14f4d917611881e9e214`; H's own BIH boundary acceptance is also recorded. Current branch readbacks and exact acceptance artifacts are reconciled in §11. A remains registrar only.
- Test evidence: I36 and H36 NOT RUN.
- Fact/Claim ADR-001: independently ADR-BLOCKED. No status change is made by this register.

## 8. Exit criteria

This phase cannot close until: (1) each I36-GOV-01..10 has formal approval evidence or remains explicitly blocked; (2) each consumer owner records acceptance/rejection against exact BIH commit; (3) I36/H36 tests execute on identified builds with reproducible fixtures/logs and owner sign-off; (4) cross-module discrepancies are resolved by the authority that owns the affected contract. No branch merge is authorized by this record.


## 9. Consumer/source artifact manifest (readback evidence)

The following artifacts were fetched from the listed live Owner branches during this review. Their presence proves only that the contracts/specifications exist; it does not establish acceptance.

| Consumer | Branch | Branch HEAD at discovery | Read artifact path | Blob SHA | Evidence interpretation |
|---|---|---|---|---|---|
| C | `session-c-agent-integration-2026-11-16` | `3b6c1d9a5d648f61daa04f5874d887f33475f098` | `07-agent-integration/telemetry-event-and-identity-contract.md` | `2bd9e640bd0c1d2c8b768da1e06b06096bc2a79e` | Consumer identity contract; no explicit BIH acceptance |
| C | `session-c-agent-integration-2026-11-16` | `3b6c1d9a5d648f61daa04f5874d887f33475f098` | `07-agent-integration/conformance-matrix.md` | `ae31eb8554f04b1d21f5aee80537425b1ddd5329` | Specification explicitly says tests not executed |
| D | `session-d-memory-brain-2026-11-16` | `968ce314cf2e44f50e3efd711060e495374cac98` | `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `b9f75456140eed6a34faa8d84be20436cd91c745` | D-owned operation/fence contract; no identity consumer sign-off |
| E | `session-e-memory-compiler-2026-11-16` | `e3afa99728f399d154767c959e37ff38f651b4b6` | `04-memory-compiler/compiler-state-and-producer-admission.md` | `e59f517fff161ab882aa0ddc4a5bda513964ae1a` | Producer admission contract; no explicit BIH acceptance |
| F | `session-f-memory-runtime` | `2da5209d7072272d5510d376c0f319bed0402a6f` | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` | `176cd500bf5d9fa8519c5213e835a745567fcfad` | Runtime suppression contract; no explicit BIH acceptance |
| G | `session-g-memory-context` | `ac32e980003aa41faf0ae958ffef3df5ab387984` | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `8f6b215de7b78bf0eec2281359d3e039e7c8d5f4` | Applied/Forget reconciliation contract; no explicit BIH acceptance |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `c0d01d81698fa6bc2a22e84b0e2ada66ce329815` | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` | `5e2d55c8b210997693a7f83d35a5a03588e4ae6b` | Proposed physical realization; explicitly not implemented/verified |
| A | `session-a-integration-2026-11-16` | `9c3dafb97b97aee50a8b61fe60836ed0a8e92fe3` | `reviews/integration/contract-registry.md` | `fa1774b673819a597f2f3082764ef2369ecc2189` | A registry; expressly not an approval authority |
| H | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/protocol-conformance-matrix.md` | `075b2ac6ebe9bda4ec83de04fad07e8027e6a440` | H protocol test specification; NOT RUN |
| H | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` | H36-01..18 and H36-SR additions; NOT RUN |

The live branch inventory also includes `main` at `8a6414158c9c056c1638222534e1993d1bbc99d2`; none of the above owner-branch artifacts is presumed to exist on main. No branches were merged.


## 10. Additional identity and protocol source readback

| Owner | Branch | Source HEAD | Artifact path | Blob SHA |
|---|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/typed-reference-and-scope-semantics.md` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` |
| B | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/principal-actor-binding-mapping.md` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` |
| I | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` |
| I | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` |
| H | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/message-envelope-and-versioning.md` | `5547ecd78d118bd63e571e5daad87194d9b694e4` |
| H | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md` | `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8` |
| H | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/forget-revocation-and-reconnect.md` | `695909360782987781e259187041618f495f1c8c` |

These readbacks cover the typed identity/Scope model, Principal/Actor mapping, Principal/authorization policy, Scope/revocation policy, BMCP envelope/versioning, ACK target binding, and reconnect/revocation semantics. They remain design artifacts and do not constitute runtime proof or consumer-owner acceptance.


## 5. Owner-side acceptance reconciliation — 2026-11-16 refresh

The following consumer Owner artifacts were independently fetched from their current Owner branches and reviewed against the exact B/H/I source Blob references recorded in each artifact. I now recognizes these as **design-level consumer acceptance evidence** for the named boundary. This registry reconciliation does not upgrade runtime conformance, external governance approval, or JF-10 closure.

| Consumer | Current Owner HEAD | Owner acceptance artifact | Blob SHA | I registry disposition | Remaining boundary |
|---|---|---|---|---|---|
| D | `df1b415bcddbbd066d7db6316e0caa14b3097d92` | `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | **DESIGN ACCEPTANCE RECOGNIZED** | D36 implementation/tests NOT RUN; JF-10 P0 open; I governance remains blocked |
| E | `2adc95ad4d6562f37d9bb6ed8743ce3514a1d615` | `04-memory-compiler/phase-3.6-bih-identity-consumer-acceptance.md` | `6f4100618695fcf971560fb784f7887a72798c96` | **DESIGN ACCEPTANCE RECOGNIZED** | E36 implementation/tests NOT RUN; JF-10 P0 open; I governance remains blocked |
| Storage | `eea8e645b84f73a668428a298dded3313a82353d` | `reviews/storage-consistency/phase-3.6-bih-identity-consumer-acceptance.md` | `ec8e49d0d11c72d37ad0c291611a96a1122ba6f5` | **DESIGN ACCEPTANCE RECOGNIZED** | Storage implementation/deployment verification NOT RUN; JF-10 P0 open; I governance remains blocked |

### 5.1 Accepted scope

Each of the three owner records explicitly accepts the BIH identity-trust semantics at its own boundary, including:
- typed PrincipalRef / ActorRef / ProducerRef / AdapterRef / ScopeRef / EnvironmentRef distinctions;
- verifier-established identity and rejection of payload-only or caller-minted identity;
- role-tagged Scope and exact Environment resolution;
- complete operation-bound authorization tuple and authenticated workload/session binding;
- I-owned PermissionEpoch currentness, with no offline/stale lease or cached ALLOW without online currentness proof;
- independent D ForgetFence checks;
- fail-closed handling for forged, malformed, unknown, unsupported and ambiguous inputs;
- single-use CommitAuthorizationReceipt binding and final-boundary submission;
- distinct I authorization ordering, D fence and Storage visibility authority.

The source refs are:
- B: `02-domain-model/phase-3.6-typed-identity-trust-closure.md`, Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`;
- H: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, Blob `9845c97ac43d7888732afafe12e28850ec02add8`;
- I: `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`, plus I execution addendum Blob `1f5d2e4aba7afa75c0696f3c8f025b0cb903e0ad`.

### 5.2 Matrix update

For the D, E and Storage rows of §4, the ten identity/security behavior columns (PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Producer/Adapter Identity, Authenticated Transport Binding, PermissionEpoch Validation, Revocation, Forged Payload Identity Rejection, Unknown/Unsupported Handling) are now **DESIGN-ACCEPTED** based on the exact owner artifacts above.

This does not mean implementation exists or that the tests passed. It does not change the OPEN status of C, F, G or H consumer acceptance. A remains registrar only.

### 5.3 Gate consequence

G6 BIH Consumer Acceptance has advanced from no DE-S consumer acceptance evidence to **PARTIAL / BLOCKED**: D, E and Storage design-level acceptance is now recorded; C, F, G and H remain OPEN. H's BIH ownership/design baseline is not a substitute for its separate consumer acceptance record. Runtime conformance remains unverified for every consumer.

No I36 governance decision is approved by this reconciliation. I36-GOV-01..10 remain GOVERNANCE-BLOCKED. JF-10 remains P0 OPEN and the corrective I owner-gate ordering decision is recorded separately. I36/H36/D36/E36 and Storage conformance remain NOT RUN.


## 6. H owner-side consumer acceptance reconciliation — 2026-11-16

H has now published an explicit delegated design-level consumer acceptance for its BMCP authentication, protected-message, ACK and reconnect boundary:

- H branch: `session-h-bmcp-protocol`
- H Owner HEAD: `50b0247725c03ba2155678a1dfeae841056a6fb9`
- Artifact: `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md`
- Blob SHA: `ccbac2d30234df9b910565a7326d100d11a6494e`
- Exact B/I/H source blobs and accepted field/behavior mapping are enumerated in the H artifact.

I recognizes this as **H DESIGN ACCEPTANCE RECORDED** for BIH36-JD-01..17 at the H-owned boundary. It covers protected verifier context, typed Principal/Actor/Scope/Environment/Producer/Adapter identities, PermissionEpoch carriage/currentness handling, revocation, payload forgery rejection, fail-closed Unknown/Unsupported handling, ACK identity/digest binding and reconnect revalidation.

This recognition is limited to design acceptance. H36 and H36-SR tests remain NOT RUN; no runtime conformance, external governance approval, or production BMCP schema freeze is inferred.

### 6.1 Matrix and G6 consequence

The H row in §4 is updated from OPEN to **DESIGN-ACCEPTED** for all ten identity/security behavior columns, against the exact source and acceptance Blob references above.

G6 BIH Consumer Acceptance is now **PARTIAL / BLOCKED**:
- Design acceptance recognized: D, E, H and Storage.
- Still OPEN: C, F and G.
- Runtime conformance: NOT VERIFIED / NOT RUN for every consumer.
- A remains registrar only, not a consumer approver.

I36-GOV-01..10 remain GOVERNANCE-BLOCKED. JF-10 remains P0 OPEN under the separate I36-SR-02 owner-gate ordering correction. This register update does not close G6, G5, G7 or G10.


## 11. C/F/G BIH consumer acceptance — current Owner-branch reconciliation (2026-11-17)

This section supersedes the historical OPEN/PARTIAL consumer status in §§5.3 and 7 for the **design-acceptance subrequirement only**. It does not change I36-GOV-01..10, H36/I36 execution, implementation or overall Phase 3.6 acceptance.

Exact A BIH package: `reviews/integration/phase-3.6-identity-trust-joint-architecture.md`, Blob `a45ae90b318a79bf009d14f4d917611881e9e214`.

| Consumer | Current branch HEAD | Owner acceptance artifact | Current readback Blob | Decision |
|---|---|---|---|---|
| C | `c408d2c138d1975eff1167bd5889ba45a13b126b` | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| D | `f5cbe59561b73c75708a52f28b0bf12707d75c71` | `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | DESIGN-LEVEL ACCEPTANCE RECORDED |
| E | `fb063e15ee31569e501f5fa0a3198b3cf0b67a9c` | `04-memory-compiler/phase-3.6-bih-identity-consumer-acceptance.md` | `6f4100618695fcf971560fb784f7887a72798c96` | DESIGN-LEVEL ACCEPTANCE RECORDED |
| F | `86c013814fbbfff1829729eb18fdc3a5de265969` | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` | `ce59252dbbdc5d10d016704797e9ba12d5a941bd` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| G | `466e2bf5992ea5944ef6ecebd79a39eeb21cdc97` | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | ACCEPT WITH ENUMERATED EXCEPTIONS |
| Storage | `f0f9d9fefd31251fc1ee27e543d4351f398627e8` | `reviews/storage-consistency/phase-3.6-bih-identity-consumer-acceptance.md` | `ec8e49d0d11c72d37ad0c291611a96a1122ba6f5` | DESIGN-LEVEL ACCEPTANCE RECORDED |

Additional H owner-side BIH boundary evidence:
- H branch HEAD: `7924f68bd55c1ab8020713d496c30bc9bed41a2c`.
- H artifact: `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md`.
- Current readback Blob: `ccbac2d30234df9b910565a7326d100d11a6494e`.
- Disposition: DESIGN-LEVEL ACCEPTANCE RECORDED; H36 NOT RUN.

The earlier A Issue #6 reconciliation comment `6919649724` reported G's acceptance Blob as `5406b3f2558daa3f5915f6bb46e808be8d90d3ca`. The current G branch readback is Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; the current file still contains the exact A BIH package pin and G's ACCEPT WITH ENUMERATED EXCEPTIONS disposition. This register uses the current readback Blob and retains the earlier A comment as historical evidence.

### 11.1 G6 consequence

The explicit BIH design-consumer acceptance subrequirement for C/D/E/F/G/Storage is now **COMPLETE / ACCEPTED WITH ENUMERATED EXCEPTIONS** on current branch readbacks. H's own owner-side design acceptance is also recorded. This is the acceptance state only; it does not imply:
- I36-GOV-01..10 approval (still GOVERNANCE-BLOCKED);
- I36/H36/D36/E36/Storage/consumer runtime execution (NOT RUN or NOT VERIFIED);
- JF-10 P0 implementation closure or production coordinator deployment;
- CGH-APPLIED-1.1 production wire freeze or C/G/H contract freeze;
- Global Forget completion, Runtime Forget E2E closure or physical erasure.

A is the final G0–G10 registrar/acceptance authority and must update its own closure plan/ledger before treating G6 as closed. This I register does not rewrite A's gate state or approve on behalf of any consumer.


## 6. Phase 3.6.3 evidence reconciliation — BIH consumer acceptance (2026-11-17)

This append-only reconciliation supersedes the **discovery-time consumer status rows in Section 4 only**. It does not change BIH36-JD-01..17, I governance policy, external approval status, or test status.

### 6.1 Exact A-package acceptance

The exact A BIH package is `reviews/integration/phase-3.6-identity-trust-joint-architecture.md`, Blob SHA `a45ae90b318a79bf009d14f4d917611881e9e214`.

GitHub Issue #6 comment `6919556745` records C/F/G exact-version Owner decisions. A's subsequent reconciliation comment `6919649724` records the exact branch readbacks. The following Owner artifacts were independently fetched from their named branches in this reconciliation:

| Consumer | Owner artifact | Verified current Blob SHA | Disposition | Evidence |
|---|---|---|---|---|
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | ACCEPT WITH ENUMERATED EXCEPTIONS | Issue #6 comments 6919556745 / 6919649724; exact BIH package pin in Owner artifact |
| F | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` | `ce59252dbbdc5d10d016704797e9ba12d5a941bd` | ACCEPT WITH ENUMERATED EXCEPTIONS | Issue #6 comments 6919556745 / 6919649724; exact BIH package pin in Owner artifact |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | ACCEPT WITH ENUMERATED EXCEPTIONS | Issue #6 comments 6919556745 / 6919649724; current artifact retains the BIH acceptance section and subsequent G-owned Applied decisions |
| H | `08-bmcp-protocol/phase-3.6-a-package-exact-version-h-owner-acceptance.md` | `fe437a3d44790f249f613d1e6cafc0db40d45b10` | ACCEPTED WITH BINDING H-OWNED PROTOCOL BOUNDARIES | Issue #6 comment 6919218061; exact H Owner decision artifact read back |

The G artifact has advanced beyond the Blob SHA recorded in A's earlier reconciliation (`5406b3f2558daa3f5915f6bb46e808be8d90d3ca`). The current Blob was fetched and its retained Phase 3.6.3 BIH acceptance section was verified. Its additional G-owned Applied decisions are not treated as BIH changes or as transferable approvals for a different Applied package.

### 6.2 Corrected consumer status

- C: design-level BIH consumer acceptance complete, with enumerated exceptions.
- F: design-level BIH consumer acceptance complete, with enumerated exceptions.
- G: design-level BIH consumer acceptance complete, with enumerated exceptions.
- H: exact A-package BIH design acceptance complete, with binding H-owned protocol boundaries.
- D, E and Storage: this addendum makes no new claim about their acceptance; retain their separately evidenced status until exact Owner evidence is reconciled into this register.
- A: coordinator/registrar only; not a consumer approval authority.

The Section 4 discovery-time OPEN entries for C/F/G/H are therefore historical and superseded by this addendum. No cross-owner acceptance is inferred for any other consumer.

### 6.3 Gates not changed by this reconciliation

1. I36-GOV-01..10 remain **GOVERNANCE-BLOCKED**. No external approver, effective policy version, signed approval, Environment Registry Authority designation or policy activation is created by the consumer decisions.
2. I36-01..20, H36-01..18, F runtime cases, G Applied/COC cases, CFG-01..20 and PI-01..08 remain **SPECIFIED / NOT RUN** unless a separate executable run record proves otherwise.
3. No implementation, interoperability, deployment, security certification, Contract Freeze, Global Forget completion or physical-erasure status is advanced.
4. This update is an I-owned evidence-register correction only. A must independently refresh the integration ledger and overall G0–G10 disposition; this I record does not make A's final integration decision.

### 6.4 Next actions

- I: continue obtaining the named external authorities, effective policy approvals, Environment Registry Authority designation and I36 execution evidence.
- D/E/Storage: provide or refresh their exact-version BIH consumer acceptance evidence if still required by the A gate.
- A: consume this updated I register Blob and the exact C/F/G/H artifacts in the next integration reconciliation; do not reuse the earlier I register Blob.


## 12. Phase 3.6.7 — inventory component evidence completeness hardening — 2026-11-18

### I-INV-REF-01 — terminal component state could be marked Confirmed without evidence

Adversarial review of the I Global Forget inventory reference model found that `set_component(name, "Confirmed")` accepted a missing proof/verifier, while `evaluate()` checked only the component state for Confirmed. A caller of the reference model could therefore satisfy all component states without retaining a component-level proof reference. This was a model-level evidence-completeness defect; it is not evidence of a production I service or signed inventory seal.

### I-owned correction

- Model: `09-security-governance/tests/global_forget_model.py`, new Blob `977a3bae77c4d6b9342eaa774731052d2fce8e14`, commit `b869528647627eb125a2cb6eef576faeac1ae7e0`.
- Tests: `09-security-governance/tests/test_global_forget_model.py`, new Blob `5ec68fd6e948a72e28b10a28fac760b65a167c09`, commit `124b1cc1246cc40bf75cc38bc2aa11890a92ae62`.
- Correction: terminal component states `Confirmed`, `NotApplicable`, `PolicyException` and `Failed` now require a non-empty proof reference and verifier; unsupported states reject; completion rechecks retained proof/verifier rather than trusting the state label alone.
- Added tests reject Confirmed/PolicyException without proof+verifier and ensure evaluation returns Pending if a previously stored component proof is absent.

### Execution evidence boundary

- Workflow: `.github/workflows/i-global-forget-reference-model.yml`, Blob `2c16ef5381dd271789912e9b1c1e5c12941d2826`.
- Intended runner: Python 3.12; standard-library `py_compile` and `unittest`, no third-party dependency.
- Exact workflow commands: `python -m py_compile 09-security-governance/tests/global_forget_model.py 09-security-governance/tests/test_global_forget_model.py`; then, from `09-security-governance/tests`, `python -m unittest discover -v`.
- Trigger commit: `124b1cc1246cc40bf75cc38bc2aa11890a92ae62`.
- Current readback found no combined status/check run for that commit. **Execution: NOT RUN / NO VERIFIED CI RESULT.** No PASS is claimed. The workflow must be run on the exact test commit and its raw log retained.

This closes only the reference-model source defect. It does not create a real ProducerDomainInventoryEpoch, InventorySealReceipt, external governance approval, Environment Registry Authority, AuthorizationCommitPermit, I36 execution or Global Forget completion. I36-GOV-01..10 remain GOVERNANCE-BLOCKED; G2/G5 remain BLOCKED; G7 remains NOT RUN.


## 13. Project Governance Authority and G0 namespace clarification — 2026-11-18

The Project Governance Owner branch `session-p-project-governance-baseline` was discovered at HEAD `0559a03ccd4f9640ddb7d4af8e37a059930b55af`. Its current governance artifacts remain proposals:

- `00-governance/project-decision-authority.md`, Blob `ca3777acae5ceb38a2a421cbf9e738053e4a4057`: **PROPOSED — GOVERNANCE-OPEN**; no named Project Governance Authority (PGA), appointment mechanism, quorum, voting rule or delegated approval policy is evidenced. It expressly says A's Principal Integration Architect role does not imply PGA authority.
- `00-governance/project-acceptance-gates.md`, Blob `98fc0ab52cadccc22e3eec89b8dc15045904cc7d`: **PROPOSED — NOT APPROVED**; its G0 Project Governance exit requires a documented PGA appointment and approval process.

**Namespace distinction:** A's Phase 3.6 G0 is *Baseline Integrity* (branch/artifact freshness). P's project G0 is *Project Governance* (mission, redlines, authority and change control). They are different gates. A's baseline-integrity result must not be represented as project-governance approval. Project G0 remains BLOCKED / NOT AUTHORIZED until the sponsor appoints the PGA and the required approval evidence is recorded. I cannot appoint the PGA or approve project redlines on its behalf.

## 14. G6 BIH consumer-acceptance status correction — 2026-11-18

A's current Phase 3.6 closure plan Blob `0adca0f54ff6ee1e344949cb48334ff475fad247` §10 explicitly says C/G/H shared Applied-package acceptance and F's explicit BIH consumer acceptance remain outstanding. A's CGH-APPLIED-1.1 matrix Blob `ee35d3b39cb1fddd1feee0e0504b77e73e376893` is a different acceptance campaign: it records B/C/D/E/G/H/I/Storage decisions for the Applied/COC package and contains no F row. It is not BIH36 identity/authorization consumer acceptance.

This I register's §4 is the BIH-specific acceptance ledger. Its C, D, E, F, G, H and Storage rows remain **OPEN — no explicit BIH acceptance**; the I technical baseline is not a substitute for those consumer records. Therefore **A G6 remains BLOCKED**. Any earlier statement that all C/D/E/F/G/Storage BIH consumer acceptances were complete is not supported by the current A plan, A matrix or this I register and must not be used for gate promotion.

Required owner actions (no acceptance is created by this request):
1. C, D, E, F, G, H and Storage each publish an explicit acceptance in their own Owner branch, pinned to the exact BIH36-JD-01..17 artifact digests, with field mapping, protected enforcement boundary, conditional/rejected fields and negative-test evidence.
2. I publishes its own consumer mapping/technical acceptance separately from I36-GOV external approvals.
3. A re-reads every exact Owner Blob and updates the G6 ledger only after each required Owner record exists. A's CGH-APPLIED-1.1 matrix must remain a separate acceptance dimension.

I36-GOV-01..10 remain GOVERNANCE-BLOCKED; I36/H36 remain NOT RUN. This correction does not change BIH36-JD-01..17 or authorize G5/G7/G10.


## 15. Phase 3.6.7 follow-up — component exception path now fails closed — 2026-11-18

A second adversarial pass found that the first hardening revision still allowed a component `PolicyException` state when a caller supplied arbitrary proof/reviewer strings. That is insufficient to represent an authorized, scoped, expiring governance exception. The reference model has no component-exception authorization workflow, so it must not allow that state to complete.

- Model Blob: `207b797fc77358f31bb4d42a541d0b28a0713c5c`, commit `4b8a73c9e529a52e44bf6050f287fe32e1767586`.
- Test Blob: `ea4102ecbb4fa0b7120a4658f0c931afab341950`, commit `e87bcffe4876d7f7cf8dce687c8543f26247b9e6`.
- Change: component `PolicyException` is rejected by `set_component`; `evaluate()` returns Pending if that state is injected directly. Only Confirmed/NotApplicable component states can satisfy the component loop, and both require retained proof + verifier. Target-level exception logic remains separate and is not a substitute for component exception authority.
- Added regression test proves that even a populated proof/reviewer object cannot promote an unimplemented component exception path.

The I reference-model workflow remains the available executable harness (Python 3.12, standard-library compile/unittest), but no GitHub Actions run or combined status was observed for the earlier trigger commit; this follow-up commit also has no verified execution result at this readback. **All I reference-model tests remain NOT RUN / NOT PASS until the exact latest test commit is executed and its raw log is retained.** This is reference-model hardening only; I36-GOV-01..10 remain GOVERNANCE-BLOCKED and I36 remains NOT RUN.
