# Phase 3.8.7 — I Exact Review of H Owner Snapshot Attestation Schema
# Phase 3.8.7 — I 对 H Owner Snapshot Attestation Schema 的精确审查

- Reviewer: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Exact I P0 addendum: Blob `739dc15e3cca33aef3f012f713b988e5528d4ad9`
- Exact H schema: `bmcp.i-owner-snapshot-attestation/1.0.0`, Blob `ecf9971b089ca5fab9a92915663dc913c8ab1ba6`
- H exact review: Blob `b03a99943b374103bae3e599c68cb2cd97a561ca`
- H unified schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — I SNAPSHOT ATTESTATION STRUCTURE**
- English and Chinese are normative peers.

## 1. I decision / I 决议

I accepts H's standalone owner snapshot attestation schema as a structurally coherent carrier for the I-signed attestation defined by the I P0 addendum. The correction preserving `owner_authority_ref` as an opaque typed reference is mandatory and correct; H semantic validation must resolve it to the unique I authority.

I 接受 H 的独立 Owner Snapshot Attestation Schema 作为 I P0 补充所定义 I 签名证明的结构载体。将 `owner_authority_ref` 保持为不透明类型化引用的修订是强制且正确的；H Semantic Validator 必须将其解析为唯一 I Authority。

## 2. Exact identity/digest distinction / 精确身份与摘要区分

- `snapshot_digest` commits to the underlying I ledger snapshot.
- `attestation_digest` commits to the exact signed attestation P0.
- Outer H `owner_snapshot_attestation_ref` equals `attestation_ref`.
- Outer H `owner_snapshot_attestation_digest` equals `attestation_digest`.
- The COC `ownerSnapshot` summary must match the attestation's owner gate, generations, request/admission counts, high-waters, set digests, ledger roots, anti-rollback anchor and I-specific high-waters.
- No digest may be substituted for another or recomputed from an incomplete projection.

## 3. Binding I conditions / I 约束条件

1. I issues the attestation only after complete, authenticated enumeration of its request and admission ledgers at the exact high-water and scope generation.
2. COMPLETE enumeration requires pagination completion and a stable ledger root; UNKNOWN/INCOMPLETE is not an empty set.
3. Count zero requires a separate I-signed CompleteEmptyProof bound to owner ledger, version, query, high-water, scope generation, key-status generation and anti-rollback anchor. Count greater than zero forbids an empty proof reference.
4. I key-status generation and anti-rollback anchor must be current and verifiable; a stale or missing checkpoint yields UNKNOWN.
5. The profile reference must resolve to the exact I-approved profile and key version. No payload-selected profile or stale ACTIVE cache is accepted.
6. The schema's `attestation_digest` is outside P0 and must be recomputed from the exact I P0 projection. `signature_ref` is allocated before signing and is not derived from signature bytes.

## 4. Final I disposition / I 最终结论

**ACCEPT WITH ENUMERATED AMENDMENTS — I SNAPSHOT ATTESTATION STRUCTURE.**

I accepts H schema Blob `ecf9971b089ca5fab9a92915663dc913c8ab1ba6` and H review Blob `b03a99943b374103bae3e599c68cb2cd97a561ca` for the exact structure and mappings above. This does not prove live inventory completeness, deployed key registry, anti-rollback anchor, cryptographic implementation, or production Global Forget completion.

**有条件接受 — I Snapshot Attestation 结构。** I 接受精确 Schema 与审查 Blob 的结构/映射；不证明实时 Inventory 完整性、已部署 Key Registry、Anti-rollback Anchor、密码学实现或生产 Global Forget 完成。
