# B — Phase 3.6 Identity Trust Baseline Preservation & Consumer Status

- Owner: Session B — Domain Model
- Branch: `session-b-domain-model-phase3`
- Status: **B semantic baseline JOINT-DECIDED; downstream consumer acceptance OPEN; implementation conformance NOT VERIFIED**
- Scope: B-owned domain semantics and evidence inventory only. This record does not approve I policy, H wire schema, or any downstream consumer.

## 1. Live source baseline

| Artifact | Branch | Source HEAD at discovery | Path | Blob SHA |
|---|---|---|---|---|
| B typed identity joint closure | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |
| B Typed Reference Registry | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/typed-reference-registry.md` | `af23ca9e019ab067a5f8ff62da902d4a419db3f3` |
| B Principal/Actor mapping | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/principal-actor-binding-mapping.md` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` |
| I trust/authorization baseline | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| H protected-operation binding | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` |

## 2. Decision Preservation Table

No technical decision is reopened by this status record. The following are preserved as the current delegated BIH joint baseline; the I/H source documents contain the authoritative full decision text.

| Decision ID | Existing decision | Owner | Source SHA | Status | Change required |
|---|---|---|---|---|---|
| BIH36-JD-01 | PrincipalRef, IssuerRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and RuntimeSessionRef are distinct typed identities | B | `0a6b78a842e550b58533b797cdfcd2d954ed6826` | JOINT-DECIDED | None |
| BIH36-JD-02 | A Ref is not authentication, registration or permission proof; payload identity is a claim | B | `0a6b78a842e550b58533b797cdfcd2d954ed6826` | JOINT-DECIDED | None |
| BIH36-JD-03 | Principal resolution is issuer/trust-domain/tenant/kind/subject scoped and stable | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-04 | Issuer trust is explicit, local, non-transitive; no TOFU | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-05 | ActorRef is verifier-produced immutable per-operation attribution | B/I/H | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-06 | Agent/Adapter/Producer are distinct registered workload identities | B/I/H | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-07 | Delegation is strict intersection; no amplification/cycles; sub-delegation disabled absent approved profile | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-08 | Ownership/applicability Scope roles distinct; cross-Scope requires explicit current grant | B/I | `0a6b78a842e550b58533b797cdfcd2d954ed6826` | JOINT-DECIDED | None |
| BIH36-JD-09 | Cross-Environment denied by default; exact bridge and authorization required | B/I | `0a6b78a842e550b58533b797cdfcd2d954ed6826` | JOINT-DECIDED | None |
| BIH36-JD-10 | Protected operation authorization binds complete identity/action/resource/scope/environment/delegation/policy/epoch tuple | I + enforcement owner | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-11 | PermissionEpoch is I-owned and incomparable across policy domains | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-12 | Offline/stale authorization leases are prohibited in this baseline | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-13 | PermissionEpoch and D ForgetFence are independent namespaces/checks | I/D | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-14 | BMCP authentication context is protected verifier/transport context, not payload identity | H/I | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-15 | ACK binds authenticated identities, session, operation, scope, capability/permission epochs, fence and immutable evidence | H/I + operation owner | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-16 | Reconnect authenticates and revalidates issuer, identities, capability, epoch, fence and journal before resume | H/I/D/G | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-17 | Unknown/malformed/unsupported security-critical input fails closed | B/I/H | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |

## 3. B domain confirmation boundary

- B semantic confirmation: the delegated BIH joint decision is recorded as the B domain semantic baseline. This is not a separate human B Owner signature.
- AuthenticationContextRef remains an H/I verifier-internal opaque handle, not a tenth B domain Ref.
- B does not approve Issuer Trust, Delegation Policy, PermissionEpoch governance, H wire encoding or any downstream consumer's implementation.
- Environment Registry authority remains unassigned in the baseline; consumers must deny unresolved/unregistered environment bindings.

## 4. Consumer acceptance register

The current owner-branch artifacts below are evidence of contract existence/specification only. None is an explicit consumer-owner acceptance of BIH36-JD-01..17. Therefore all acceptance statuses below are **OPEN — NO OWNER ACCEPTANCE EVIDENCE**.

| Consumer | Contract fields / required behavior | Owner | Acceptance status | Evidence / gap |
|---|---|---|---|---|
| C Agent Integration | Principal/Actor/Producer identity, Scope/Environment, authenticated transport, epoch/revocation, reject payload forgery, unknown fail-closed | C | OPEN | C conformance matrix is a specification; no explicit BIH acceptance or runtime proof |
| D Memory Brain | Principal/Actor/Scope/Environment at canonical mutation; current PermissionEpoch and revocation at commit; reject forged identity/unknown | D | OPEN | D Forget/commit contracts do not constitute explicit BIH consumer acceptance |
| E Memory Compiler | Producer/Adapter identity, authenticated ingress, Scope/Environment, epoch/revocation before publication; reject forged producer | E | OPEN | E producer/publication conformance is specified; explicit BIH acceptance absent |
| F Memory Runtime | Principal/Actor/Scope/Environment before retrieval/candidate exposure; current epoch/revocation; no side channel | F | OPEN | F runtime suppression contract exists; explicit BIH acceptance absent |
| G Context Manager | Principal/Actor/Scope/Environment, authenticated Adapter/session ACK, epoch/revocation and stale/unknown suppression | G | OPEN | G applied/forget reconciliation contract exists; explicit BIH acceptance absent |
| H BMCP | Protected transport identity, Principal/Actor/Producer/Adapter, typed scope/environment, PermissionEpoch, ACK/reconnect fail-closed | H | OPEN as consumer-owner acceptance | H protocol design is decided under delegated BIH authority; no separate consumer acceptance or runtime proof |
| Storage/Consistency | Authenticated operation context and current PermissionEpoch at visibility/commit; durable revocation ordering; reject unknown/forged identity | Storage | OPEN | Storage realization is design-only, not implemented/verified; no acceptance |
| A Integration Registry | Register exact source refs/status; do not infer approval from presence; preserve owner-specific acceptance evidence | A | OPEN | A is registrar/coordinator, not consumer approval authority |

## 5. Test execution status

No executable test environment, implementation build, command, fixture run, logs or reproducible result were found in the reviewed B/I/H branch artifacts. B does not claim test execution.

- I36: test specification exists in I; execution NOT RUN / no evidence.
- H36: 18 adversarial cases are specified in H; execution NOT RUN / no evidence.
- C conformance matrix explicitly describes tests as specified/not run.
- No test is PASS or FAIL on the basis of document review.

## 6. Non-claims and blockers

- I governance decisions remain GOVERNANCE-BLOCKED until formal external authority approval.
- Consumer acceptance remains OPEN until each corresponding Owner explicitly records acceptance against exact contract version/commit.
- Runtime and adversarial conformance remain NOT RUN.
- No branch is merged by this record.
- Fact/Claim ADR-001 remains independently ADR-BLOCKED and is not affected by this identity baseline.
- This file records B-owned domain status only; it cannot sign for C/D/E/F/G/H/Storage/A or governance authorities.


## 7. Owner-side consumer acceptance status refresh — 2026-11-16

The §4 OPEN table is the original discovery snapshot and is superseded for current design-acceptance status by the following verified Owner artifacts. BIH36-JD-01..17 remain unchanged.

| Consumer | Owner acceptance artifact | Blob SHA | Current design-acceptance state |
|---|---|---|---|
| D | `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md` on `session-d-memory-brain-2026-11-16` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | DESIGN-ACCEPTED |
| E | `04-memory-compiler/phase-3.6-bih-identity-consumer-acceptance.md` on `session-e-memory-compiler-2026-11-16` | `6f4100618695fcf971560fb784f7887a72798c96` | DESIGN-ACCEPTED |
| H | `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md` on `session-h-bmcp-protocol` | `ccbac2d30234df9b910565a7326d100d11a6494e` | DESIGN-ACCEPTED |
| Storage | `reviews/storage-consistency/phase-3.6-bih-identity-consumer-acceptance.md` on `session-storage-consistency-forget-atomicity-2026-11-16` | `ec8e49d0d11c72d37ad0c291611a96a1122ba6f5` | DESIGN-ACCEPTED |

Still OPEN: C, F and G. A is registrar only, not a consumer approver. The four accepted records are design-level owner evidence; none establishes executable implementation, runtime conformance or test PASS. I36 governance approvals remain GOVERNANCE-BLOCKED. JF-10 remains P0 OPEN; the I owner-gate ordering correction is recorded on I's Owner branch.

This status refresh is an evidence reconciliation only. It does not revise B domain semantics or BIH36-JD-01..17, sign for any consumer, or close G6/G7/G10.
