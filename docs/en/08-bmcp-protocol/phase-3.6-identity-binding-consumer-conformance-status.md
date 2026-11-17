# H — Phase 3.6 Identity Binding Consumer & Conformance Status

- Document ID: H36-IDENTITY-CONSUMER-STATUS
- Owner: Session H — BMCP Protocol
- Source branch: `session-h-bmcp-protocol`
- Source path: `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md`
- Exact source blob SHA: `8afb914731a34d8ab44331f54f1f39bfd8ec37ce`
- Source status: **Protocol-binding technical design JOINT-DECIDED; consumer-owner acceptance OPEN; governance approval GOVERNANCE-BLOCKED; H36 NOT RUN**
- Companion status: **BILINGUAL READING COMPANION; source decision state unchanged**
- Chinese companion: [简体中文](../../zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md)
- Scope: H-owned protocol binding and conformance evidence only. This record is not external governance approval or downstream consumer sign-off.

> Source-snapshot note: the source's §1 records the historical discovery baseline. A fresh read of the live H branch found the protected-operation binding at blob `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`, not the historical `9845c97ac43d7888732afafe12e28850ec02add8` recorded below. This companion preserves the source record verbatim in substance; the discrepancy is a currentness finding, not silently rewritten history.

## 1. Live source baseline

| Artifact | Branch | Source HEAD at discovery | Path | Blob SHA |
|---|---|---|---|---|
| H protected-operation binding | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `9845c97ac43d7888732afafe12e28850ec02add8` |
| H protocol conformance matrix | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/protocol-conformance-matrix.md` | `075b2ac6ebe9bda4ec83de04fad07e8027e6a440` |
| H ACK/target binding | `session-h-bmcp-protocol` | `59926f5090dfd2e2ad78d9c25bd0d9062b4bcabc` | `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md` | Current path confirmed; this record does not change its semantics |
| I joint trust policy | `session-i-security-governance-2026-11-16` | `6a92f49bd740f6e2db11568d9bd61e8c58132cbc` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` |
| B typed identity closure | `session-b-domain-model-phase3` | `2148dcf1a53ff7aab194ba1bf799fa5a6a3b697f` | `02-domain-model/phase-3.6-typed-identity-trust-closure.md` | `0a6b78a842e550b58533b797cdfcd2d954ed6826` |

## 2. Decision preservation

BIH36-JD-01..17 remain unchanged. H preserves these protocol implications:
- Protected verifier/transport context, not payload, is authoritative for issuer, principal, ActorRef, workload, audience and session.
- Authenticated channel/session binding is distinct from message integrity and authorization.
- ACK evidence is bound to the authenticated Adapter instance, Agent/runtime, fresh RuntimeSessionRef, ActorRef, operation/delivery/forget identity, exact Scope roles, CapabilityEpoch, PermissionEpoch, applicable ForgetFence, evidence digest and immutable ACK ID.
- ACK duplicates with the same identity+digest are idempotent; the same ID with a different digest is conflict.
- D/G/I order acceptance on their own authoritative sequencers. H ingress receipt sequence is evidence only and is never numerically compared with owner cursors or local wall-clock time.
- Reconnect must reauthenticate, revalidate issuer/workload/capability/PermissionEpoch/ForgetFence, suppress stale state, reconcile journals, and only then resume.
- Unknown/malformed/unsupported required security fields fail closed; no downgrade or payload fallback.

No change to technical semantics is proposed by this status record.

## 3. H conformance inventory

The existing H36 matrix is preserved without reducing scope. All 18 cases are **Specified / NOT RUN**.

| Test ID | Scenario | Required result | Execution environment | Command | Input / actual | Logs / evidence | Status |
|---|---|---|---|---|---|---|---|
| H36-01 | Forged PrincipalRef in payload | Protected Principal remains authoritative; reject mismatch | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-02 | Forged ActorRef | Reject caller-minted/mismatched ActorRef | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-03 | Forged ProducerRef | Require authenticated workload mapped to registered Producer | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-04 | Unknown Issuer | Reject before Principal resolution | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-05 | Revoked Issuer/key | Reject; invalidate affected session and reconcile | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-06 | Expired Credential | Reject at reconnect and protected boundary | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-07 | Expired Delegation | Deny; do not act as grantor | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-08 | Revoked Delegation | Deny and require current PermissionEpoch | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-09 | Stale PermissionEpoch | Reject protected operation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-10 | Cross-Scope access | Deny absent explicit I-approved grant | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-11 | Cross-Environment access | Deny absent exact bridge/grant | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-12 | Authenticated Principal / payload ActorRef mismatch | Reject/quarantine and audit | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-13 | Old Session ACK replay | Historical only; no new-session state mutation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-14 | Reconnect during revocation | Do not resume before fresh trust/epoch/fence/reconciliation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-15 | Unauthorized Forget Operation | Deny before target/fence mutation | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-16 | ACK ID reused with different digest | IDEMPOTENCY_CONFLICT; no state change | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-17 | Missing required Scope/Environment | Deny; no wildcard/default | Not supplied | Not supplied | Not executed | None | NOT RUN |
| H36-18 | Protocol major downgrade | VERSION_UNSUPPORTED; no weakened auth | Not supplied | Not supplied | Not executed | None | NOT RUN |

### Mandatory H36-SR additions — also NOT RUN

The Section 10.6 additions remain in scope and must not be omitted:
1. Channel-binding mismatch.
2. Same message replayed across sessions/audiences.
3. Nonce reuse.
4. Canonicalization duplicate-key ambiguity.
5. Missing/unknown Operation Requiredness Registry profile.
6. Sender suppresses an applicable EnvironmentRef.
7. Cross-Adapter ACK ID collision.
8. Same ACK ID with different digest.
9. ACK arrival racing revocation/fence advance in both orders.
10. Reconnect replay after Adapter instance replacement.
11. Capability downgrade with an old valid session.
12. I sequencer/epoch read and commit race; multi-domain coordinator outage cases required by I36-SR-07.

No environment, command, fixture, expected/actual output, logs, or signed test artifact was available. No test is PASS or FAIL.

## 4. Consumer acceptance

Reading H protocol docs or consuming a BMCP message does not constitute owner acceptance. The source's original discovery snapshot found no explicit consumer-owner acceptance against the exact H36/BIH contract version.

| Consumer | H-provided contract fields / required behavior | Consumer owner | Acceptance status | Required evidence |
|---|---|---|---|---|
| C Agent Integration | Authenticated Agent/runtime and Adapter identity; final request boundary; session/epoch/fence; reject payload identity mismatch and unsupported capability | C | OPEN | C Owner acceptance tied to H contract commit and final-request enforcement |
| D Memory Brain | Authenticated ACK identity, operation and target binding; owner-local ForgetFence ordering; old-session/revoked ACK historical only | D | OPEN | D Owner acceptance and D sequencer acceptance evidence |
| E Memory Compiler | Authenticated Producer/Adapter binding; ingress receipt and idempotency; permission/fence check at publication | E | OPEN | E Owner acceptance at ingress/publication boundaries |
| F Memory Runtime | Authenticated retrieval principal/adapter/session; current permission and revocation; suppress stale candidates | F | OPEN | F Owner acceptance at candidate emission/cache boundary |
| G Context Manager | Authenticated Adapter ACK; ContextVersion/Delivery/session binding; PermissionEpoch and revocation ordering; reconnect/late ACK behavior | G | OPEN | G Owner acceptance at Applied state transition |
| H BMCP | Wire envelope, protected verifier context, channel binding, requiredness, ACK and reconnect | H | JOINT-DECIDED technical design; separate consumer acceptance not recorded | No independent H-session signature or runtime proof claimed |
| Storage/Consistency | Authenticated commit context and current PermissionEpoch/fence at durable visibility boundary | Storage | OPEN | Storage Owner acceptance of protocol-to-storage binding and durable transaction evidence |
| A Integration Registry | Exact H source ref/status registration; never infer acceptance from artifact existence | A | OPEN as registry activity; not an approver | A may register owner evidence, but cannot approve for consumers |

All consumer-side identity fields not explicitly accepted remain unaccepted. No evidence in this record proves that each consumer accepts PrincipalRef, ActorRef, ScopeRef, EnvironmentRef, Producer/Adapter identity, authenticated transport binding, PermissionEpoch validation, revocation, forged-payload rejection and Unknown/Unsupported behavior end-to-end.

## 5. B/I/H confirmation and governance boundary

- B domain type confirmation: delegated joint technical baseline; no separate B-session signature claimed.
- I governance confirmation: technical policy baseline decided; external approvals remain GOVERNANCE-BLOCKED.
- H protocol binding confirmation: delegated joint technical baseline; no separate H-session signature claimed.
- Cross-module technical agreement: B/I/H only.
- Consumer acceptance: OPEN for C/D/E/F/G/Storage; A registry-only.
- H36 execution: NOT RUN.
- I36 execution: NOT RUN.
- Fact/Claim ADR-001 remains independently ADR-BLOCKED.

## 6. Exit criteria

H36 cannot be marked conformant until every mandatory H36 and H36-SR case is executed on an identified build with authenticated fixtures, expected/actual result, retained non-sensitive logs and owner review. Cross-module consumer acceptance requires explicit acceptance from each consumer Owner. External governance approval must be supplied by the named governance authorities, not inferred from this commit. No branch merge is authorized by this record.

## 7. Consumer acceptance status refresh — 2026-11-16

The §4 table is the original discovery snapshot. The following current Owner artifacts provide design-level acceptance evidence and supersede the prior OPEN status for those consumers only:

| Consumer | Owner acceptance artifact | Blob SHA | Current design-acceptance state |
|---|---|---|---|
| D | `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md` on `session-d-memory-brain-2026-11-16` | `184423d2d8191a12f2d4a869bc63f5e7fafaf96a` | DESIGN-ACCEPTED |
| E | `04-memory-compiler/phase-3.6-bih-identity-consumer-acceptance.md` on `session-e-memory-compiler-2026-11-16` | `6f4100618695fcf971560fb784f7887a72798c96` | DESIGN-ACCEPTED |
| H (self-consumer boundary) | `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md` on `session-h-bmcp-protocol` | `ccbac2d30234df9b910565a7326d100d11a6494e` | DESIGN-ACCEPTED |
| Storage | `reviews/storage-consistency/phase-3.6-bih-identity-consumer-acceptance.md` on `session-storage-consistency-forget-atomicity-2026-11-16` | `ec8e49d0d11c72d37ad0c291611a96a1122ba6f5` | DESIGN-ACCEPTED |

Still OPEN: C, F and G. A remains registrar only. These acceptances cover design semantics only; runtime implementation and conformance remain NOT VERIFIED / NOT RUN. External I governance approvals remain GOVERNANCE-BLOCKED. JF-10 remains P0 OPEN and H does not accept the current split Phase-B/Phase-C candidate as conformant to I36-SR-02.

This status refresh does not change BIH36-JD-01..17, claim a human signature, or close G6/G7/G10.
