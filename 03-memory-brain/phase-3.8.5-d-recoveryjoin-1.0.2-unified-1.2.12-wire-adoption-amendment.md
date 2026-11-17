# Phase 3.8.5 — D Wire Adoption Amendment: RecoveryJoin 1.0.2 / Unified 1.2.12
# Phase 3.8.5 — D Wire 采纳修订：RecoveryJoin 1.0.2 / Unified 1.2.12

- Owner perspective: D — Memory Brain / ForgetFence Authority
- Status: **D-ROLE CANDIDATE AMENDMENT / EXACT H CROSS-REVIEW REQUIRED / NOT FROZEN**
- Supersedes only the H-version applicability sentence in D membership proof contract Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd`; it does not alter D Fence or D proof authority.
- Exact H Unified schema: 1.2.12 Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`.
- Exact H RecoveryJoin: 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`.
- Reviewed Storage successor manifest: Blob `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7`.
- Provenance: coordinator-authored D-role simulation; not independent human D Owner approval.

## 1. D adoption decision / D 采纳决议

D adopts H Unified 1.2.12 and RecoveryJoin 1.0.2 as candidate structural carriers for D owner-snapshot membership proofs, subject to exact owner-authoritative resolution of each D row and the constraints below. This replaces the previous D contract's H Unified 1.2.11 applicability statement only. D remains the sole authority for D producer/work/attempt/derivative/barrier lineage and ForgetFence.

D 采纳 H Unified 1.2.12 与 RecoveryJoin 1.0.2 作为 D Membership Proof 的候选结构载体，但每一条 D 记录必须由 D 权威解析，并满足以下约束。本修订仅替换旧合同对 H Unified 1.2.11 的适用版本声明，不转移 D 的 Producer/Work/Attempt/Derivative/Barrier Lineage 与 ForgetFence 权威。

## 2. RecoveryJoin proof field mapping / RecoveryJoin 证明字段映射

| RecoveryJoin 1.0.2 field | D semantic meaning |
|---|---|
| `proof_ref`, `owner_kind` | immutable D proof identity; owner_kind MUST be `D` |
| `owner_authority_ref` | D BrainAuthority / producer-work authority |
| `issuer_ref`, `subject_ref`, `audience_ref`, `purpose` | D issuer/subject/audience and exact Recovery Cutoff membership purpose |
| `owner_ledger_ref/version` | exact D producer/work/attempt/derivative/barrier ledger and version |
| `owner_entry_ref/digest` | exact typed D row identity and immutable canonical row digest |
| `owner_admission_ref` | exact D producer/work admission identity |
| `owner_sequence_namespace/local_sequence/high_water` | D-local namespace, row sequence and applicable row-kind high-water |
| `owner_ledger_root` | D complete lineage-relevant ledger root |
| `owner_snapshot_ref/digest` | immutable D snapshot |
| `owner_snapshot_attestation_ref/digest` | D-signed snapshot and completeness attestation |
| `owner_gate_ref/generation` | D owner gate and D GateGeneration |
| `scope_ref/generation/binding_digest` | Forget target/source/ancestor lineage selector and applicability scope |
| `operation_identity_ref/digest` | ForgetOperationRef and immutable operation digest |
| `request_digest` | exact producer/work admission request digest |
| `anti_rollback_anchor_ref`, `key_status_generation` | D anti-rollback and current signing-key status |
| `signature_profile_ref`, `key_id`, `key_version`, `canonicalization_profile_ref`, `digest_profile_ref` | D-owned signing profile and key identity |
| `proof_digest`, `signature_ref` | derived proof digest and external D signature reference |

The exact row kind (producer registration, WorkItem, Attempt, Derivative or barrier record) is determined by the D-owned typed `owner_entry_ref` and the authoritative D ledger lookup. The row digest MUST cover its exact row-kind discriminator, all referenced lineage identities, source revision, dependency revision, relevant D high-water dimension and barrier/fence state. H MUST NOT infer D row kind or lineage from a COC participant.

## 3. Unified 1.2.12 and RecoveryJoin 1.0.2 joins / Join 规则

Each D admission row represented in a participant binding or owner-local no-participant disposition must bind:
- owner_kind D and exact D admission/entry/ledger/version;
- D-local sequence and high-water;
- D ledger root, snapshot and snapshot attestation;
- operation and scope-binding digests;
- exact membership proof ref/digest.

The full proof payload is carried in RecoveryJoin 1.0.2 `owner_snapshot_membership_proofs`; the corresponding owner-admission binding carries `owner_snapshot_membership_proof_ref` and `owner_snapshot_membership_proof_digest`. Both references must resolve to exactly one payload and match its proof digest. Duplicate, omitted, cross-owner or mismatched proof is INVALID.

D's owner snapshot `owner_specific_high_waters` must include distinct producer-registration, WorkItem, Attempt, Derivative and barrier dimensions. A single scalar high-water in an individual proof is interpreted only in its declared D-local sequence namespace and row kind; it never collapses or numerically compares D dimensions with I/C/COC counters.

## 4. D completeness and late-lineage behavior / D 完整性与迟发现 Lineage

Membership of one row does not prove complete D inventory. D must prove query identity, complete pagination, counts, ordered-set roots, producer/dependency registry revisions, all relevant high-water dimensions, source/ancestor lineage closure and anti-rollback checkpoint. A late-discovered pre-fence producer/work/ancestor invalidates the prior D snapshot and reopens the affected barrier for a successor cutoff round. Post-fence admissions remain blocked/quarantined and cannot publish.

H verification without D's owner-authoritative ledger/signature verifier returns UNKNOWN. Empty D membership requires D's separate signed COMPLETE_EMPTY proof; empty arrays/count zero alone are insufficient.

## 5. Negative requirements / 负向要求

Reject or return UNKNOWN for wrong owner kind, missing or duplicate proof, mismatched row digest, sequence above row-kind high-water, stale D Gate/FenceGeneration, missing lineage ancestor, incomplete dependency closure, incomplete pagination, stale key status, anti-rollback uncertainty or a proof whose scope/operation/request differs from the frozen D snapshot.

## 6. Status / 状态

- H Unified 1.2.12 + RecoveryJoin 1.0.2 structural applicability: **ADOPTED AS CANDIDATE**.
- D proof P0, Fence and lineage authority: **UNCHANGED / D-OWNED**.
- H owner verifier and production D ledger/signer: **NOT VERIFIED**.
- Late-lineage race, durable barrier and D release CAS execution: **NOT VERIFIED**.
- Independent D Owner signature and freeze: **NOT PROVIDED**.

H exact cross-review of this amendment is required before interoperability acceptance.
