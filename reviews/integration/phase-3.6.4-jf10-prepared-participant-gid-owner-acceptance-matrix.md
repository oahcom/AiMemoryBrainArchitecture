# Phase 3.6.4 — JF-10 Prepared Participant Identity Exact Owner Acceptance Matrix

- Owner: A — Principal Integration Architect
- Exact Storage COC protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- Exact A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- Exact B typed-reference registry Blob: `b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- Exact H BMCP 1.1.1 schema candidate Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Date: 2026-11-17
- Status: **AMENDED §14 EXACT OWNER REVIEW COMPLETE WITH CONDITIONS; NOT IMPLEMENTED**

## 1. Exact owner review evidence

| Owner | Acceptance artifact Blob SHA | Branch HEAD at verification | Decision scope |
|---|---|---|---|
| B | `8b63fa17be2397820ed8e462582b6fd9c3cd0fd0` | `7ca1719c603451f9c50aa6dfa83289805e96cb51` | PreparedParticipantRef / GID / native XID semantic type separation. |
| C | `dd6c28a88aad019fcb513e789dcfffc20934e852` | `b053a2c8b1790046b4cdfe3bb05ec333757df291` | Provider idempotency remains distinct; no GID/native-XID substitution. |
| D | `3cba777f8951a5d88e27a314a37c000aeedc19d0` | `c57fc9323f01b3bb46d8048741df014d13136e9c` | D barrier participant key and preallocation/cutoff ordering. |
| E | `057c1c2096e97798e60e07710f301ae7cc522bbc` | `e593b387fd3b18f3bf53ecbfb9c2c97c25948335` | Producer retry/publication lifecycle binds same pair. |
| G | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `ecb8062c0b533a960656aca2fba2f294981f8ab2` | Full Applied proof binds same pair and Storage resolution. |
| H | `98321da4b93d39ada9d227f4e03f2e55ba45aa29` | `c92fc4a0deb6b4d07be8ef3bf27ea116af9d6136` | Wire mapping and BMCP 1.1.1 candidate. |
| I | `20fc13bbfe7b93c0d6f6233fd714c57dadca1fda` | `553355afa017e82b4972315493abdc8b0f5b6603` | I terminal receipt/consumption binds pair; governance remains separate. |
| A | `d6402bd4cc5d13a4f17f6c40398cfa31d9820f9d` | `8ee08da3e613c4260804a7cf4e252a58cbda1b15` | Integrated COC prepare-intent, participant and recovery mapping. |
| Storage | `984ea06c7380e31ee7761195990a62bc9dcc9f85` | `db226387b0f2dede30a32a19a1478136b368cc1e` | Storage-owned GID allocation, same-GID resolution and DB evidence. |

## 2. Integrated architecture decision

All nine Owner perspectives have reviewed the same exact amended Storage protocol Blob `86ff3b...` and the same A mapping Blob `a71251...`. H has additionally accepted the 1.1.1 candidate wire schema `c0bbfc...` and reports 34/34 schema/parser tests passing in CI run `43964080044`.

The accepted identifier model is:

- `PreparedParticipantRef`: stable engine-neutral participant identity.
- `PreparedTransactionGID`: client-chosen PostgreSQL prepared-transaction handle, Storage allocated and bound to the immutable operation tuple before COC prepare-intent.
- `EngineNativeTransactionXIDRef`: engine-assigned observation after PREPARE, never preallocated and never used as participant identity.

COC intent must durably record the exact participant/GID binding before Storage PREPARE. I terminal decision, D barrier, C provider flow, E producer lifecycle and G Full Applied proof bind the same pair. Native XID, cluster identity, database OID, prepare timeline/LSN and Storage signer/key version remain supporting Storage evidence.

**Gate B disposition for amended §14 revision: DESIGN-LEVEL EXACT OWNER ACCEPTANCE COMPLETE WITH CONDITIONS.**

## 3. Non-waived limits

1. No COC Raft/quorum service or production Storage participant ledger/API is implemented.
2. No signed PreparedParticipantReceipt/StorageResolutionProof integration with real I/D/COC services is executed.
3. Storage GID collision/rebinding and preallocation-cancellation behavior are architecture requirements; H JSON Schema does not enforce cross-message equality/uniqueness. The Storage ledger and semantic verifier must.
4. The 34-test H run validates 1.1.0/1.1.1 schemas and strict parser reference logic only; no cryptographic signature, channel binding, issuer trust, replay-resistant transport or SDK interoperability.
5. PostgreSQL 18.7 remains a qualified capability candidate, not production deployment selection.
6. Gate C distributed fault injection and end-to-end owner races are deferred to engineering.
7. I36-GOV-01..10 remain GOVERNANCE-BLOCKED; Fact/Claim ADR-001 remains ADR-BLOCKED; multi-PolicyDomain atomicity remains blocked.
8. Global Forget target inventory, external recipient proof, backup restore in a real Forget operation and physical erasure remain open.

## 4. Phase boundary and final disposition

`IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. This is exact architecture design acceptance, not implementation PASS, deployment approval, production readiness, schema freeze or system freeze.

- Gate B amended protocol §14: DESIGN-LEVEL ACCEPTANCE COMPLETE WITH CONDITIONS.
- Gate B implementation/conformance: NOT RUN; deferred.
- Gate C: DEFERRED TO ENGINEERING.
- JF-10 runtime P0: OPEN.
- Gate A: remains subject to the remaining Storage/restore architecture contract and I/D high-water proof closure.
- TAB-001: CANDIDATE / NOT FROZEN.
- Production activation: NOT AUTHORIZED.