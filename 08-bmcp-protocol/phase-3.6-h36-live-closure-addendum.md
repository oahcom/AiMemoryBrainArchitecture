# H — Phase 3.6 BMCP Identity Binding & H36 Live Closure Addendum

- Owner: Session H — BMCP Protocol
- Branch: `session-h-bmcp-protocol`
- Parent HEAD: `cbef9b7f3d118da6a826aec0bc98faf246672d9a`
- Status: **Protocol binding technical baseline JOINT-DECIDED; external governance GOVERNANCE-BLOCKED; consumer acceptance OPEN; H36 NOT RUN**
- This H-owned addendum records protocol status only. It is not external governance approval or a downstream consumer sign-off.

## 1. Live source readback

| Owner | Branch | HEAD at discovery | Artifact | Blob SHA |
|---|---|---|---|---|
| H | `session-h-bmcp-protocol` | `cbef9b7f3d118da6a826aec0bc98faf246672d9a` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` |
| H | same | same | `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md` | `a43386d7bda8653a9a7675504cec2e6dacdd47f3` |
| H | same | same | `08-bmcp-protocol/protocol-conformance-matrix.md` | `075b2ac6ebe9bda4ec83de04fad07e8027e6a440` |
| I | `session-i-security-governance-2026-11-16` | `8d1ddadb6af70a7c387105d20ca8f2f6de80c5fb` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| B | `session-b-domain-model-phase3` | `da4bb48b785bd4c299bb871a2421b37bd6cfb178` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |

## 2. Decision preservation

BIH36-JD-01..17 remain unchanged. H preserves:
- Protected verifier/transport context, not payload, is authoritative for issuer, principal, ActorRef, workload, audience and session.
- Authenticated channel/session binding is distinct from message integrity and authorization.
- ACK binds authenticated identities, session, operation/target, exact Scope, CapabilityEpoch, PermissionEpoch, applicable ForgetFence and immutable evidence.
- Same ACK ID and digest is idempotent; same ID with different digest is conflict.
- Reconnect reauthenticates and revalidates issuer, workload, capability, PermissionEpoch, ForgetFence and journal before resume.
- Unknown/malformed/unsupported required security fields fail closed; no downgrade or payload fallback.

No wire or semantic change is proposed.

## 3. H36 execution matrix

The existing H36 matrix is preserved without reducing scope. All 18 cases are specified and **NOT RUN**.

| Test ID | Scenario | Expected result | Environment | Command | Input / actual | Evidence | Status |
|---|---|---|---|---|---|---|---|
| H36-01 | Forged PrincipalRef in payload | Protected Principal authoritative; reject mismatch | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-02 | Forged ActorRef | Reject caller-minted/mismatched ActorRef | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-03 | Forged ProducerRef | Require authenticated workload mapped to registered Producer | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-04 | Unknown Issuer | Reject before Principal resolution | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-05 | Revoked Issuer/key | Reject and invalidate dependent session | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-06 | Expired Credential | Reject at reconnect and protected boundary | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-07 | Expired Delegation | Deny; do not act as grantor | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-08 | Revoked Delegation | Deny and require current PermissionEpoch | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-09 | Stale PermissionEpoch | Reject protected operation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-10 | Cross-Scope access | Deny absent explicit current grant | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-11 | Cross-Environment access | Deny absent exact bridge/grant | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-12 | Principal / payload ActorRef mismatch | Reject/quarantine and audit | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-13 | Old Session ACK replay | Historical only; no new-session mutation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-14 | Reconnect during revocation | No resume before fresh trust/epoch/fence/reconciliation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-15 | Unauthorized Forget Operation | Deny before target/fence mutation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-16 | ACK ID reused with different digest | IDEMPOTENCY_CONFLICT; no state change | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-17 | Missing required Scope/Environment | Deny; no wildcard/default | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-18 | Protocol major downgrade | VERSION_UNSUPPORTED; no weakened auth | Not supplied | Not supplied | Not executed | None | NOT RUN |

Mandatory H36-SR additions remain in scope and NOT RUN:
1. Channel-binding mismatch.
2. Same message replayed across sessions/audiences.
3. Nonce reuse.
4. Canonicalization duplicate-key ambiguity.
5. Missing/unknown Operation Requiredness Registry profile.
6. Sender suppresses an applicable EnvironmentRef.
7. Cross-Adapter ACK ID collision.
8. Same ACK ID with different digest.
9. ACK racing revocation/fence advance in both orders.
10. Reconnect replay after Adapter instance replacement.
11. Capability downgrade with an old valid session.
12. I sequencer/epoch read and commit race; multi-domain coordinator outage cases.

No executable environment, command, fixture, expected/actual output, logs or signed test artifact was available. No case is PASS or FAIL.

## 4. Consumer acceptance

No explicit consumer-owner acceptance against the exact BIH/H contract version was found. H's protocol specification and this H-owned record do not sign for other Owners.

| Consumer | H contract fields / required behavior | Owner | Acceptance | Required evidence |
|---|---|---|---|---|
| C Agent Integration | Authenticated Agent/runtime and Adapter; final request boundary; session/epoch/fence; reject payload identity mismatch and unsupported capability | C | OPEN | C Owner acceptance and final-request enforcement evidence |
| D Memory Brain | Authenticated ACK identity, operation/target binding; D-local fence ordering; old-session/revoked ACK historical only | D | OPEN | D Owner acceptance and sequencer evidence |
| E Memory Compiler | Authenticated Producer/Adapter; ingress receipt/idempotency; permission/fence at publication | E | OPEN | E Owner acceptance at ingress/publication |
| F Memory Runtime | Authenticated retrieval principal/Adapter/session; current permission/revocation; stale candidate suppression | F | OPEN | F Owner acceptance at candidate/cache boundary |
| G Context Manager | Authenticated Adapter ACK; ContextVersion/Delivery/session binding; epoch/revocation; reconnect/late ACK | G | OPEN | G Owner acceptance at Applied transition |
| H BMCP | Envelope, protected verifier context, channel binding, requiredness, ACK and reconnect | H | JOINT-DECIDED design; separate consumer acceptance not recorded | Independent H-session acceptance and runtime proof |
| Storage/Consistency | Authenticated commit context and current PermissionEpoch/fence at durable visibility | Storage | OPEN | Storage Owner acceptance and transaction evidence |
| A Integration Registry | Register exact H source/status; never infer acceptance | A | Registrar only | A cannot approve for consumers |

No evidence proves end-to-end consumer acceptance of all ten required behaviors: PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Producer/Adapter identity, authenticated transport, PermissionEpoch, revocation, forged-payload rejection and Unknown/Unsupported handling.

## 5. Confirmation and blockers

- B domain type confirmation: delegated joint technical baseline preserved; no separate B-session signature claimed.
- I governance confirmation: technical baseline preserved; external approvals GOVERNANCE-BLOCKED.
- H protocol binding confirmation: delegated joint technical baseline preserved; no separate H-session signature claimed.
- Cross-module technical agreement: B/I/H only.
- Consumer acceptance: OPEN for C/D/E/F/G/Storage; A registrar only.
- H36 execution: NOT RUN; I36 execution: NOT RUN.
- Fact/Claim ADR-001: independently ADR-BLOCKED.

No branch merge is authorized by this addendum.
