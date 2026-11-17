# Phase 3.8.5 — I Wire Adoption Amendment: RecoveryJoin 1.0.2 / Unified 1.2.12
# Phase 3.8.5 — I Wire 采纳修订：RecoveryJoin 1.0.2 / Unified 1.2.12

- Owner perspective: I — Security, Identity and Governance
- Status: **I-ROLE CANDIDATE AMENDMENT / EXACT H CROSS-REVIEW REQUIRED / NOT FROZEN**
- Supersedes only the H-version applicability sentence in I membership proof contract Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7`; it does not alter I P0 or I signing authority.
- Exact H Unified schema: 1.2.12 Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`.
- Exact H RecoveryJoin: 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`.
- Reviewed Storage successor manifest: Blob `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7`.
- Provenance: coordinator-authored I-role simulation; not independent human I Owner approval.

## 1. I adoption decision / I 采纳决议

I adopts H Unified 1.2.12 and RecoveryJoin 1.0.2 as the candidate structural wire carriers for I owner-snapshot membership evidence, subject to the semantic mapping and conditions below. This replaces the earlier I contract's applicability reference to Unified 1.2.11 only. I does not delegate any I trust or ledger authority to H.

I 采纳 H Unified 1.2.12 与 RecoveryJoin 1.0.2，作为 I Owner Snapshot Membership 证据的候选结构载体，但必须满足以下语义映射与条件。本修订仅替换旧合同中对 Unified 1.2.11 的适用版本引用，不向 H 转移任何 I 信任或账本权威。

## 2. Exact RecoveryJoin proof mapping / RecoveryJoin 精确证明映射

The RecoveryJoin 1.0.2 `$defs.ownerSnapshotMembershipProof` required fields map to I-owned P0 as follows:

| RecoveryJoin field | I semantic meaning |
|---|---|
| `proof_ref` | immutable IAdmissionSnapshotMembershipProof identity |
| `owner_kind` | constant `I` |
| `owner_authority_ref` | exact I PolicyDomain authority |
| `issuer_ref`, `subject_ref`, `audience_ref`, `purpose` | I issuer/subject/audience and purpose `COC_RECOVERY_CUTOFF_MANIFEST_MEMBERSHIP` |
| `owner_ledger_ref`, `owner_ledger_version` | exact I request/admission/receipt ledger and version |
| `owner_entry_ref`, `owner_entry_digest` | exact I admission or receipt event row and canonical entry digest |
| `owner_admission_ref` | exact I owner admission identity |
| `owner_sequence_namespace`, `owner_local_sequence`, `owner_high_water` | I-local sequence namespace, row sequence and applicable frozen high-water |
| `owner_ledger_root` | complete I ledger root for the declared query/scope |
| `owner_snapshot_ref/digest` | immutable I snapshot identity/digest |
| `owner_snapshot_attestation_ref/digest` | I-signed snapshot completeness attestation |
| `owner_gate_ref/generation` | I Gate and exact I GateGeneration |
| `scope_ref/generation/binding_digest` | PolicyDomain and exact action/resource/principal scope |
| `operation_identity_ref/digest`, `request_digest` | exact authorization operation, request and payload binding |
| `anti_rollback_anchor_ref`, `key_status_generation` | I anti-rollback checkpoint and current key-status generation |
| `signature_profile_ref`, `key_id`, `key_version`, `canonicalization_profile_ref`, `digest_profile_ref` | I-governed signing and digest profile identities |
| `proof_digest`, `signature_ref` | derived proof digest and external I signature reference |

I's proof P0 remains owner-defined. The H schema's field layout is a transport representation only. I's signature preimage, canonicalization and digest remain governed by I's registered profile. H MUST NOT add, remove, reorder semantically, or re-sign I P0.

## 3. Unified 1.2.12 row and snapshot joins / Unified 1.2.12 行与快照 Join

For each I row in an owner admission binding or no-participant disposition:
- `owner_kind=I`;
- `owner_admission_ref`, `owner_entry_ref`, `owner_ledger_ref/version`, `owner_local_sequence`, `owner_high_water`, `owner_entry_digest`, `owner_ledger_root`;
- `owner_snapshot_ref/digest`, `owner_snapshot_attestation_ref/digest`;
- `operation_digest`, `scope_binding_digest`;
- `owner_snapshot_membership_proof_ref` and `owner_snapshot_membership_proof_digest`.

The exact proof payload appears in RecoveryJoin 1.0.2 `owner_snapshot_membership_proofs`. Its ref and digest in the owner-admission join MUST resolve to exactly one payload. Duplicate, missing, cross-owner or digest-mismatched proof is INVALID. Missing I verifier, incomplete query/pagination, unavailable key status or anti-rollback uncertainty is UNKNOWN, never VALID or COMPLETE_EMPTY.

I rows require complete I request/receipt/authorization ledger enumeration through I's own high-waters. The I owner snapshot's owner-specific high-water vector must preserve distinct request and admission/receipt dimensions. No arithmetic comparison with D/C/COC counters is permitted.

## 4. Negative requirements / 负向要求

Reject or return UNKNOWN for:
1. proof with owner_kind other than I;
2. I entry digest, admission ref, ledger version or local sequence mismatch;
3. row sequence above the captured I high-water;
4. snapshot/attestation/root mismatch or incomplete pagination;
5. stale/revoked/unknown key status or anti-rollback anchor;
6. proof payload ref/digest missing from either the admission join or proof array;
7. scope/operation/request mismatch;
8. any attempt by H/Storage/COC to issue or interpret I permission or receipt terminality.

## 5. Status / 状态

- H Unified 1.2.12 + RecoveryJoin 1.0.2 structural applicability: **ADOPTED AS CANDIDATE**.
- I P0 and trust authority: **UNCHANGED / I-OWNED**.
- H semantic adapter and production I verifier: **NOT VERIFIED**.
- I ledger completeness and release CAS runtime proof: **NOT VERIFIED**.
- Independent I Owner signature and freeze: **NOT PROVIDED**.

H exact cross-review of this amendment is required before this mapping is considered interoperable.
