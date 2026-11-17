# Phase 3.8.5 — H Owner-Authority Membership Verifier Adapter Contract
# Phase 3.8.5 — H Owner Authority Membership Verifier Adapter 合同

- Owner: H — BMCP Protocol / Wire and Interoperability Authority
- Status: **PROPOSED INTERFACE — NOT A PRODUCTION VERIFIER**
- Base semantic helper: `unified_manifest_semantics.py`, blob `e26379d38825ee13d15f652d3bd019c4091da37d`
- I proof profile source: `09-security-governance/phase-3.8.4-i-owner-snapshot-membership-proof-contract.md`, blob `88209bbea0ab600880c5c630cfe83af31ee16dd7`

## 1. Separation of duties / 职责分离

H validates wire shape, exact typed joins, canonical field presence and cross-message consistency. H MUST NOT select an owner's algorithm, canonicalization profile, digest preimage, key registry, trust root, anti-rollback authority or ledger-completeness policy. Those remain with the issuing owner (I/D/C).

H validates wire shape and join，不替 I/D/C 选择算法、规范化、Digest Preimage、Key Registry、Trust Root、Anti-Rollback 或 Ledger Completeness 策略。

## 2. Required adapter contract / 必需 Adapter 合同

The semantic integration boundary is an owner-authority verifier with the conceptual operation:

`verify_owner_membership_proof(proof_payload, owner_kind, frozen_snapshot) -> VALID | INVALID | UNKNOWN`

Inputs are immutable exact payload/snapshot objects. The adapter MUST route only to the authority identified by the authenticated `owner_kind` and `owner_authority_ref`; it MUST NOT accept an owner kind supplied only by an untrusted caller if it conflicts with the signed payload.

- `VALID`: owner authority verified signature, key status, issuer/audience/purpose, canonical P0/digest, snapshot attestation, anti-rollback anchor and row membership under its own authoritative ledger/snapshot.
- `INVALID`: cryptographic or semantic contradiction, wrong authority, wrong scope, wrong signature, digest mismatch, stale/revoked key explicitly established by owner authority, or row not included.
- `UNKNOWN`: verifier unavailable, owner registry unavailable, ledger/snapshot unavailable, key status indeterminate, anti-rollback unavailable, timeout, incomplete query, unsupported profile or any inability to prove either VALID or INVALID.

No exception, timeout, missing callback, missing key or unknown profile may be converted to VALID. Adapter exceptions fail closed as UNKNOWN unless the owner verifier returns an authenticated INVALID result.

## 3. Owner-specific routing / Owner 路由

The router MUST enforce:
- I → I-owned proof profile, key-status and PermissionDomain authority;
- D → D-owned proof profile, key-status and Brain/ForgetFence authority;
- C → C-owned proof profile, key-status and Adapter/ProviderAccount authority.

A verifier result is scoped to the exact proof digest and exact frozen snapshot digest. It cannot be cached across changed proof payload, snapshot, owner gate generation, scope version or key-status generation. Cross-owner counters are never compared.

## 4. Reference implementation boundary / 参考实现边界

The existing H helper `validate_owner_snapshot_membership_proof_payload(..., verify_owner_signature=...)` is a TEST-ONLY semantic reference. Its injected callback is not connected to real I/D/C authorities. It validates payload-to-row/snapshot equality and delegates signature trust. It does not establish production signature trust, full owner ledger completeness, or physical snapshot durability.

The production integration MUST provide an explicit adapter implementation behind the conceptual contract above, but H does not implement or own that adapter. Until I/D/C each publish their own verifier and authority evidence, the result for production acceptance remains UNKNOWN.

## 5. Mandatory negative and interoperability tests / 必需负向与互操作测试

At minimum, each owner adapter and H interop suite MUST cover:
1. correct owner + exact proof + exact snapshot → VALID;
2. wrong owner authority or owner-kind substitution → INVALID;
3. proof digest/signature/P0 mutation → INVALID;
4. row ref/digest or snapshot root mismatch → INVALID;
5. sequence above owner high-water → INVALID;
6. revoked key explicitly confirmed by owner registry → INVALID;
7. unavailable key registry or anti-rollback anchor → UNKNOWN;
8. missing/partial ledger query or pagination → UNKNOWN;
9. unknown signature/canonicalization profile → UNKNOWN;
10. verifier timeout/exception → UNKNOWN;
11. replay against changed GateGeneration/ScopeVersion/snapshot → INVALID or UNKNOWN according to owner-authoritative evidence, never VALID;
12. cross-language canonicalization/signature vectors per owner profile, not a single H-selected universal profile.

## 6. Freeze boundary / 冻结边界

This contract is an H interface proposal only. It does not approve I/D/C proof P0 profiles, select production cryptography or certify implementation. H schema and reference tests remain candidates until exact-version owner decisions and executable interoperability evidence exist. Gate B/C remain blocked as previously recorded; production activation is NOT AUTHORIZED.
