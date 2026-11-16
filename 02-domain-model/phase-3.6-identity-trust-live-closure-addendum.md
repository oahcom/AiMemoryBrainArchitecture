# B — Phase 3.6 Identity Trust Live Closure Addendum

- Owner scope: B domain semantics only
- Discovery: 2026-11-16
- Branch: `session-b-domain-model-phase3`
- Parent HEAD: `da4bb48b785bd4c299bb871a2421b37bd6cfb178`
- Status: **BIH36-JD-01..17 preserved; B semantic baseline confirmed within delegated joint decision; no separate B human signature claimed; consumer acceptance OPEN; tests NOT RUN**
- This addendum records evidence and boundaries. It does not approve I policy, H wire format, or any consumer implementation.

## 1. Live B/I/H source readback

| Owner | Branch | HEAD at discovery | Artifact | Blob SHA |
|---|---|---|---|---|
| B | `session-b-domain-model-phase3` | `da4bb48b785bd4c299bb871a2421b37bd6cfb178` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |
| B | same | same | `02-domain-model/typed-reference-registry.md` | `af23ca9e019ab067a5f8ff62da902d4a419db3f3` |
| B | same | same | `02-domain-model/principal-actor-binding-mapping.md` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` |
| I | `session-i-security-governance-2026-11-16` | `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| I | same | same | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | `74643a2f374179128d506c3b7e1d22da77119600` |
| I | same | same | `09-security-governance/phase-3.6-governance-approval-and-consumer-acceptance-register.md` | `695e27d775ebaefc1b83081519db36f105b414c4` |
| H | `session-h-bmcp-protocol` | `cbef9b7f3d118da6a826aec0bc98faf246672d9a` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` |
| H | same | same | `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md` | `a43386d7bda8653a9a7675504cec2e6dacdd47f3` |

The SHAs above were fetched from the specified live branches in this discovery. Historical HEAD values embedded in earlier manifests are not current HEAD assertions.

## 2. Decision preservation

No semantic change is requested. Preserve the existing decision table:

| Decision ID | Existing decision | Owner | Source SHA | Status | Change required |
|---|---|---|---|---|---|
| BIH36-JD-01 | PrincipalRef, IssuerRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and RuntimeSessionRef are distinct typed identities | B | `0a6b78a842e550b58533b797cdfcd2d954ed6826` | JOINT-DECIDED | None |
| BIH36-JD-02 | A Ref is not authentication, registration or permission proof; payload identity is a claim | B | same | JOINT-DECIDED | None |
| BIH36-JD-03 | Principal resolution is issuer/trust-domain/tenant/kind/subject scoped and stable | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-04 | Issuer trust is explicit, local, non-transitive; no TOFU | I | same | JOINT-DECIDED | None |
| BIH36-JD-05 | ActorRef is verifier-produced immutable per-operation attribution | B/I/H | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-06 | Agent/Adapter/Producer are distinct registered workload identities | B/I/H | same | JOINT-DECIDED | None |
| BIH36-JD-07 | Delegation is strict intersection; no amplification/cycles; sub-delegation disabled absent approved profile | I | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-08 | Ownership/applicability Scope roles distinct; cross-Scope requires explicit current grant | B/I | `0a6b78a842e550b58533b797cdfcd2d954ed6826` | JOINT-DECIDED | None |
| BIH36-JD-09 | Cross-Environment denied by default; exact bridge and authorization required | B/I | same | JOINT-DECIDED | None |
| BIH36-JD-10 | Protected operation authorization binds complete identity/action/resource/scope/environment/delegation/policy/epoch tuple | I + enforcement owner | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED | None |
| BIH36-JD-11 | PermissionEpoch is I-owned and incomparable across policy domains | I | same | JOINT-DECIDED | None |
| BIH36-JD-12 | Offline/stale authorization leases are prohibited in this baseline | I | same | JOINT-DECIDED | None |
| BIH36-JD-13 | PermissionEpoch and D ForgetFence are independent namespaces/checks | I/D | same | JOINT-DECIDED | None |
| BIH36-JD-14 | BMCP authentication context is protected verifier/transport context, not payload identity | H/I | `9845c97ac43d7888732afafe12e28850ec02add8` | JOINT-DECIDED | None |
| BIH36-JD-15 | ACK binds authenticated identities, session, operation, scope, capability/permission epochs, fence and immutable evidence | H/I + operation owner | same | JOINT-DECIDED | None |
| BIH36-JD-16 | Reconnect authenticates and revalidates issuer, identities, capability, epoch, fence and journal before resume | H/I/D/G | same | JOINT-DECIDED | None |
| BIH36-JD-17 | Unknown/malformed/unsupported security-critical input fails closed | B/I/H | same | JOINT-DECIDED | None |

## 3. Consumer acceptance

All consumers remain **OPEN — NO EXPLICIT OWNER ACCEPTANCE EVIDENCE**. Their documents prove contract existence only.

| Consumer | Required identity/behavior acceptance | Owner | Status |
|---|---|---|---|
| C | PrincipalRef, ActorRef, Producer/Adapter identity, ScopeRef, EnvironmentRef, authenticated transport, PermissionEpoch/revocation, forged payload rejection, Unknown/Unsupported fail-closed | C | OPEN |
| D | Principal/Actor/Scope/Environment at canonical mutation; current epoch/revocation at commit; reject forged/unknown | D | OPEN |
| E | authenticated Producer/Adapter at ingress and publication; Scope/Environment; epoch/revocation; reject forged producer | E | OPEN |
| F | Principal/Actor/Scope/Environment before retrieval/candidate exposure; epoch/revocation; no side channel | F | OPEN |
| G | Principal/Actor/Scope/Environment; authenticated Adapter/session ACK; epoch/revocation; stale/unknown suppression | G | OPEN |
| H | protected transport identity, typed refs, PermissionEpoch, ACK/reconnect fail-closed | H | OPEN as separate consumer acceptance |
| Storage | authenticated commit context and current epoch at durable visibility; revocation ordering | Storage | OPEN |
| A | exact source/status registration only; no approval authority | A | Registrar only; not an approver |

No field-level acceptance is inferred from implementation or design documents.

## 4. Test execution

I36 and H36 specifications exist, but no test execution is evidenced. B/I/H and C/D/E/F/G/A/Storage branch trees inspected for this review contain Markdown artifacts only; no executable source, test runner, fixture bundle or workflow definition was present in those branch trees. Therefore no executable command can be truthfully reported from this repository snapshot.

- I36-T01..T20: NOT RUN.
- H36-01..18 and mandatory H36-SR additions: NOT RUN.
- Actual results/logs: none.
- PASS/FAIL count: zero recorded; all cases remain NOT RUN.

This is not a reduction of test scope.

## 5. Confirmation and independent ADR

- B domain type confirmation: delegated technical decision preserved; no separate B human signature claimed.
- I governance: external approval remains GOVERNANCE-BLOCKED.
- H protocol binding: delegated technical decision preserved; no separate H human signature claimed.
- Cross-module agreement: B/I/H technical baseline only.
- Consumer acceptance: OPEN.
- Fact/Claim ADR-001: remains independently ADR-BLOCKED.

No branch merge is authorized by this addendum.
