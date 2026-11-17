# Phase 3.12.0 — A Review: CSubmitOutcome 1.0.1, Key Status and BMCP 1.2.12

- Owner perspective: A — Principal Integration Architect
- Scope: C immutable object 1.0.1, C key-status event/lifecycle, I governance signature candidate, H BMCP 1.2.12 mapping/validator, C/H candidate crypto execution and Storage pins.
- Disposition: **ACCEPT DESIGN + BOUNDED CROSS-OWNER TEST EVIDENCE; DO NOT REGISTER OR FREEZE**
- Provenance: delegated A-role simulation at user's direction; not independent human A Owner approval.

## 1. Exact evidence reviewed

| Owner | Artifact | Exact Blob / Run |
|---|---|---|
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C | C 1.0.1 outcome fixtures | `c447f8c2908469c52cb52a448101495a331277c5` |
| C | C 1.0.1 crypto manifest | `3a5fb8502091636135a298de5891d728b550ba50` |
| C | C 1.0.1 expected vectors | `34e49a49551390f52198b1fa557e15a32a3f6ee2` |
| C | Phase 3.11.1 sequence namespace amendment | `73d98b532b7f9cadbeee12448d035c3285db9cd7` |
| C | CKeyStatusEvent schema | `908b293eba337e9fa75864cea3704e28a1a8d82e` |
| C | Phase 3.11.0 key lifecycle contract | `9339b168165a7a3dd34def5236ad61cfd3163418` |
| I | Phase 3.8.7 key-status governance review | `57d1b1ca616eaec6df1dee82ddaccc66519caca2` |
| I | Phase 3.8.8 C 1.0.1 namespace review | `40d223c55473fc7d101b6d16858ad6405d9db5ee` |
| H | BMCP schema 1.2.12 / wire 1.3.0 | `a54f66914a819d77f00c6af04e76453ff9f654ee` |
| H | Phase 3.8.7 exact 1.2.12 ↔ 1.0.1 mapping | `7d9c4f11446b5ec4ea5640725e17dfa5d03c25b2` |
| H | Fail-closed validator core | `1a92c0cf7146e2884bd38232005dd9a55d558a85` |
| H | Validator contract | `b3b203d140b7e785411f1b862c71fadfa66a0c91` |
| Storage | Exact version manifest current | `539288d66022a08df9356787ed06a9f09ee99560` |

## 2. Sequence namespace gap — RESOLVED AT DESIGN LEVEL

A identified that CSubmitOutcome 1.0.0 had a signing `record_sequence` but did not explicitly identify its sequence namespace, while CKeyStatusEvent carried `sequence_namespace_ref`. The earlier version therefore could not prove that outcome signing and key-status transitions shared one monotonic ordering domain.

C correctly published a new immutable schema revision 1.0.1 rather than mutating 1.0.0. The new required `sequence_namespace_ref` is part of C-P0 and therefore covered by the candidate digest/signature. H now requires 1.0.1 and its key-status callback must prove exact namespace equality and common durable sequencer allocation.

A accepts this as the correct design resolution. The existence and linearizability of the production sequencer are not yet evidenced.

## 3. C key-status lifecycle — ACCEPT AS DESIGN

CKeyStatusEvent 1.0.0 separates C data-plane keys from I-governed key-status signatures. The event binds key ID/version, profile, purpose, audience, public-key fingerprint, state, predecessor, sequence namespace and external anti-rollback anchor.

The state machine correctly prevents PENDING signing, restricts ACTIVE scope, forbids new signing after RETIRED/REVOKED/COMPROMISED, and preserves DESTROYED as terminal. The earliest compromise boundary is sequence-based. Missing status/checkpoint is UNKNOWN, not implicit ACTIVE.

I owns governance trust-root approval and key-status signing profile; C owns data-key lifecycle/event production; H validates the chain and currentness. A accepts the boundary. The actual registry, trust root, external checkpoint and custody system are not deployed/evidenced.

## 4. Candidate crypto evidence — ACCEPT WITH BOUNDED SCOPE

C CI run `44059935858` passed 19 tests at commit `b49966361b4b3121a2ebf4105b4e0c57a612e945`. H CI run `44060704553` passed 17 tests at commit `8c377a7218b70621d2348b47341d4cf4755b3733`.

The C/H tests validate:
- CSubmitOutcome 1.0.1 schema and ten synthetic semantic vectors;
- candidate JCS/SHA-256/Ed25519 construction over five outcome families;
- every present C-P0 member mutation invalidates the original test signature;
- static expected digests/preimage hashes/public keys/signatures;
- independent C and H Python/Node implementation agreement;
- sequence namespace presence and key-status schema/state-machine predicates.

The deterministic seed is public test-only material. These tests prove candidate construction, not operational trust. Neither C nor I profile is registered.

## 5. H validator and external authority boundaries — ACCEPT AS INTERFACE

H validator core is pinned to BMCP 1.2.12 / wire 1.3.0 and C object 1.0.1. It has explicit fail-closed callbacks for profile registration, key status, C signature, provider evidence, owner ledger, COC join and anti-rollback/currentness.

A accepts the interface and the INVALID/UNKNOWN distinction. The callbacks are not connected to production key registries, governance trust roots, provider issuer systems, C ledger or COC/Storage stores. Therefore the core cannot yet issue production VALID decisions.

The BMCP 1.2.12 C branch retains the same C-specific field names/types as 1.2.11, but 1.2.12 is the current envelope revision. The 1.2.11 mapping is historical.

## 6. Remaining release blockers

| Gate | Current status |
|---|---|
| CSubmitOutcome 1.0.1 / BMCP 1.2.12 design | ACCEPTED AS CANDIDATE |
| Candidate crypto and C/H cross-language tests | PASSED |
| I registration of C data profile | NOT APPROVED |
| I governance profile/trust root | NOT REGISTERED |
| C key-status registry and external anti-rollback | NOT DEPLOYED |
| C key custody/HSM/KMS, rotation/revocation/compromise drills | NOT EVIDENCED |
| Production H signature/key-status/provider/ledger/COC callbacks | NOT CONNECTED |
| C append-only ledger inclusion/currentness | OPEN |
| Provider-specific adapter race/fault/idempotency tests | NOT RUN |
| Deployment-grade COC/Storage joins and readback | OPEN |
| Final A freeze | NOT GRANTED |

## 7. Final decision

**ACCEPT CSubmitOutcome 1.0.1, C key-status lifecycle design, BMCP 1.2.12 mapping and bounded C/H candidate test evidence. DO NOT REGISTER OR FREEZE.**

The sequence namespace gap is resolved at the contract level. The remaining gap is operational: no production sequencer, key registry, I trust root, key custody, anti-rollback service, authority callback integration, provider adapter evidence or deployment-grade COC/Storage proof has been demonstrated.

No production provider egress, Full Applied, Global Forget Completion or universal exactly-once behavior is authorized. All Owner decisions are delegated role simulations, not independent human Owner signatures.
