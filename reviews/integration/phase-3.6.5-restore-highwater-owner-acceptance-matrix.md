# Phase 3.6.5 — Restore Control-High-Water Exact Owner Acceptance Matrix

- Owner: A — Principal Integration Architect
- Exact Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- Exact B typed-reference registry Blob: `63ccb4bf687b00dea2b21fc2773f3018648d76e6`
- Exact I/D proof acceptance artifacts are listed below.
- Date: 2026-11-17
- Status: **RESTORE CONTROL-HIGH-WATER ARCHITECTURE ACCEPTED BY ALL OWNER PERSPECTIVES WITH CONDITIONS; NOT IMPLEMENTED**

## 1. Exact owner acceptance evidence

| Owner | Acceptance artifact Blob SHA | Branch HEAD at verification | Acceptance scope |
|---|---|---|---|
| A | `fa5e066a208a64401c96a6b8790d8b53dc7f1585` | `0b774be6d9c6258d022cc48c45a6f438d246bf95` | System restore proof integration and owner-local release gates. |
| B | `5e7c6a869fa1a29d59dfc7f404cade3d66c410f2` | `e79ff629af3656e055a7ce10cc7b9fea468cf84f` | Typed proof refs and non-substitution invariants. |
| C | `1001553fcde31daac457754429cddebd0c88a055` | `c408d2c138d1975eff1167bd5889ba45a13b126b` | Provider-side-effect restore gate; Storage receipt not provider outcome. |
| D | `211e54acfb4573b1c51d96f07af297671dfc4c4b` | `f5cbe59561b73c75708a52f28b0bf12707d75c71` | D Forget/lineage high-water proof and fail-closed barrier. |
| E | `051a65c1c140f133ad06a73c649b27b1888e83ca` | `fb063e15ee31569e501f5fa0a3198b3cf0b67a9c` | Compiler artifact/queue/publication restore gate. |
| F | `d630933a2aa70b9bc182fdeab47856dd8bbec386` | `3cb98c5a8a60cfaf4ad446e53833fbabcaa0eddf` | Index/cache/Working Set anti-resurrection restore gate. |
| G | `0910fea807b96a896e361cd2722e4c94df55187b` | `466e2bf5992ea5944ef6ecebd79a39eeb21cdc97` | Context/Applied/delivery restore gate. |
| H | `5a4b9a768d7396eb4be58d0d1ed3c6c0021955ea` | `b116edbebc7302e4ab74326ef3f5a8df431344f9` | Proof transport/authority boundary; wire schema deferred. |
| I | `85d62b8858fc86addacd3b83f49476e42f49b785` | `23500d42b2ab3dd41f464810e30e08b1b639e747` | Per-PolicyDomain I control high-water, inventory and revocation proof. |
| Storage | `d3923fe42bec04d9f5233c7a810303da80b73bc2` | `22329a83c54e58e6368cc817331ef695cd185129` | Quarantined restore reconciliation and Storage receipt semantics. |

## 2. Cross-owner contract decision

All ten owner perspectives accepted the same Storage restore contract Blob `4f656163...` and the authority separation:

- COCCommittedPrefixProof — COC committed prefix/checkpoint and voter configuration only.
- IControlHighWaterProof — one proof per PolicyDomainRef, including PermissionEpoch/sequencer/revocation state and global ProducerDomainInventoryEpoch/registry digest.
- DForgetControlHighWaterProof — one proof per relevant ForgetOperation/lineage, including fence generation, request cutoff, producer high-water and barrier terminal state.
- StorageParticipantLedgerProof — complete restored participant/GID/native-XID/DB identity/terminal state ledger.
- RestoreReconciliationReceipt — Storage's `RECONCILED_BUT_FENCED` evidence only; not permission to serve, I authorization, D clearance, COC proof or Global Forget completion.

Owner-specific release gates remain in force: C cannot submit provider work; E cannot publish; F cannot serve restored derived indexes/caches; G cannot deliver Context; H cannot accept stale proof envelopes until current owner controls are verified.

## 3. Executable evidence

Storage restore high-water logical reference model: **25/25 PASS**, CI run `43965501810`, job `133643756066`, commit `19798634fb0d55cb0c901c8f4194506fab96b75b`. Model Blob `be0aef6232c8ee2ed6179df7b0a74473c3e25b3b`; test Blob `a9e1a96b449c6bf0e2b52c5fea394a8c32961a24`.

Tests cover missing/stale/gapped COC/I/D proofs, policy-domain coverage, I inventory seal ↔ D ForgetOperation binding, same-GID/native-XID/database identity, WAL/timeline, pointer/receipt atomicity, signature/key/audience, high-water advance during restore, quarantine, and the fact that RestoreReconciliationReceipt does not enable serving or Global Forget completion.

## 4. Final Gate A disposition and non-waived limits

Storage Gate A architecture design is **CONDITIONAL PASS**: the restore proof contract, owner authority boundaries, recheck order and fail-closed behavior are now accepted by all Owner perspectives. Storage implementation/deployment readiness remains NOT PASSED / DEFERRED.

Not claimed: production restore, real COC/I/D/Storage proof APIs, cryptographic signature verification, old-primary fencing, object-store ACL implementation, archive/checkpoint custody, measured RTO, production failure-domain placement, KMS, named operators, or Gate C distributed fault injection.

I36-GOV-01..10 remain GOVERNANCE-BLOCKED; Fact/Claim ADR-001 remains ADR-BLOCKED; Global Forget target inventory, external deletion and physical erasure remain open; multi-PolicyDomain atomicity remains blocked.

- Gate A architecture design: CONDITIONAL PASS.
- Gate A implementation/deployment: DEFERRED / NOT PASSED.
- Gate B amended COC §14 design: exact owner acceptance complete with conditions.
- Gate B implementation: NOT RUN.
- Gate C: DEFERRED TO ENGINEERING.
- JF-10 runtime P0: OPEN.
- TAB-001: CANDIDATE / NOT FROZEN.
- Production activation: NOT AUTHORIZED.