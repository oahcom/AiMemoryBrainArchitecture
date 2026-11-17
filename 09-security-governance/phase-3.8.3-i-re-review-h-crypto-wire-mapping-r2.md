# Phase 3.8.3 — I Re-review of H I-Crypto Wire Mapping Revision
# Phase 3.8.3 — I 对 H I-Crypto Wire Mapping 修订版复审

- Reviewer: I — Security, Identity and Governance
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: delegated I-role simulation at the user's direction; not an independent human Owner signature.
- Status: candidate only; no cryptographic freeze, deployment or TAB-001 approval.
- English and Chinese are normative peers.

## 1. Exact version / 精确版本

- I profile proposal: `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- H mapping revision: `77d0bb31196c722cb2cdda8c2ff55d8ade201db5`
- H schema artifact 1.2.7: `e9748a5b904d2b975e47a32a0cbb31de31636854`
- HRC/JPF/WIRE/SCHEMA prior candidate suite: `60a2f4db4bd12f2131ecd147db9bbe328da6db50`, `1a4e754ba9bfa57eb973c6d39731e9f89443b323`, `67aba74c120f2916d768e7b01c45408ee2624f3a` (these do not test the crypto profile).

## 2. What is now accepted / 本轮接受内容

The revised H mapping now provides:
- explicit common signed fields and explicit common exclusions;
- exact additional field allowlists for I-owned pending gate, gate release and JF10 I terminal decision;
- explicit distinction between the I-signed nested snapshot attestation and the COC-signed outer record;
- owner signature / COC quorum / transport channel-binding separation;
- semantic rejection of missing or mismatched I signature profile IDs despite the additive optional schema field;
- no profile inheritance to C/D/Storage/COC.

I accepts these as the candidate field-projection boundary, subject to the snapshot-attestation and independent-vector conditions below.

修订版 H Mapping 已提供 Common Signed Fields 与 Exclusions、I Pending Gate/Gate Release/JF10 Terminal 的字段 Allowlist、嵌套 I Snapshot 与外层 COC Record 的分离、三类 Proof 的 Authority 边界、缺失/不匹配 Profile ID 的语义拒绝，以及禁止跨 Owner 继承 I Profile。I 将其作为候选字段投影边界接受，但仍保留以下条件。

## 3. Remaining amendments / 剩余修订

### I-H-CRYPTO-01 — Snapshot attestation must be content-bound

H's mapping correctly requires dereferencing `owner_snapshot_attestation_ref`, but the current schema field is a locator and the mapping has not yet pinned a content digest field or a guaranteed content-addressed resolver contract. H must do one of:
- add an explicit `owner_snapshot_attestation_digest` in a new schema artifact and require exact equality; or
- normatively require the resolver to return an immutable content-addressed ref whose digest is cryptographically verified and included in the COC-signed snapshot.

A mutable locator without digest binding is insufficient.

### I-H-CRYPTO-02 — Empty-set and out-of-scope proof schema

H must pin the exact schema/projection for I-signed COMPLETE_EMPTY and OUT_OF_SCOPE_WITH_PROOF assertions, including scope, ledger query/high-water, pagination completion, count=0, canonical empty root, key status and anti-rollback anchor. The current unified schema does not itself define those proof families.

### I-H-CRYPTO-03 — Exact signature reference semantics

`owner_signature_ref` may be included in P0 only if it is allocated before signing, immutable and not derived from signature bytes. H must state its stable reference construction and exact dereference rule.

### I-H-CRYPTO-04 — Executable independent vectors

The exact P0 field projections must be exercised by at least two independent canonicalization/signature implementations. The test-only HRC digest helper and its 66/66 result do not satisfy this requirement.

### I-H-CRYPTO-05 — I production trust and operational decisions

I still must separately approve algorithm/regulatory suitability, trust-root ceremony, HSM/KMS profile, key rotation/overlap, compromise handling, retention, revocation propagation, external anti-rollback checkpoint and PolicyDomain sequencer implementation. This document does not close those decisions.

## 4. I final decision / I 最终决议

**ACCEPT WITH ENUMERATED AMENDMENTS** for H mapping Blob `77d0bb31196c722cb2cdda8c2ff55d8ade201db5` against I profile Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2` and schema 1.2.7 Blob `e9748a5b904d2b975e47a32a0cbb31de31636854`.

No production trust profile, key provisioning, sequencer, Storage proof-verification or TAB-001 freeze is approved. The exact snapshot digest binding, empty/out-of-scope proof family, and independent byte-for-byte implementations remain blocking.

**有条件接受**该精确版本组合。生产 Trust Profile、Key Provisioning、Sequencer、Storage Proof Verification 或 TAB-001 冻结均未获批准。Snapshot Digest Binding、Empty/Out-of-scope Proof Family 和独立字节级实现仍是阻断项。
