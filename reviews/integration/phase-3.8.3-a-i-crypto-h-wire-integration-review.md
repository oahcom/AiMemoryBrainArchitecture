# Phase 3.8.3 — A Integration Review: I Cryptographic Profile × H Wire Mapping
# Phase 3.8.3 — A 集成审查：I 密码学配置 × H Wire 映射

- Reviewer: A — Principal Integration Architect
- Decision: **ACCEPT AS CANDIDATE SECURITY/WIRE COMPOSITION WITH BLOCKING CONDITIONS**
- Freeze decision: **BLOCKED — NOT FROZEN / NOT PRODUCTION-ACCEPTED**
- Provenance: delegated A-role simulation at the user's direction; not an independent human A Owner or governance signature.
- Language: English and Chinese are normative peers.

## 1. Exact reviewed bundle / 精确审查版本

| Owner | Artifact | Exact Blob |
|---|---|---|
| I | Phase 3.8.3 `AIMBA-I-CRYPTO-1.0` profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| I | I exact review R3 of H crypto mapping | `93afe9c9e06d20de5ce1c2a0f676b4785123fbcf` |
| H | Phase 3.8.3 I crypto wire mapping | `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` |
| H | Unified COC/JF-10 schema 1.2.8 | `70b892797d07489936300a26c0dedfafe1d6e746` |
| H | RecoveryJoin schema 1.0.1 | `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c` |
| H | Schema 1.2.8 / RecoveryJoin 1.0.1 CI result | `3973156204d98c787589ffcaf744f17f467a0d48` |
| H | Schema test source | `ff2b735ccdbf5d45f3c6b2ee9a25d14db2e3c7ad` |

CI run: [44043259259](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44043259259), job `133902679119`, **97/97 PASS**.

## 2. Integration findings / 集成发现

### A-CRYPTO-01 — Authority separation

**ACCEPT.** I owns trust roots, issuer/key status, PermissionDomain/PermissionEpoch, nonce consumption, revocation ordering and I terminal proof. H owns wire projection/schema/parser. C, D, Storage and COC retain independent authority. The I profile does not become a universal signature policy for all owners.

### A-CRYPTO-02 — Three independent proof layers

**ACCEPT.** The design separates:
1. owner-authored semantic record signature;
2. COC quorum/append attestation;
3. H authenticated transport/channel binding.

No one layer can synthesize another. A valid COC quorum record does not prove I authorization; an I signature does not prove COC append; a transport ACK does not prove either.

### A-CRYPTO-03 — Digest and signature construction

**ACCEPT AS CANDIDATE.** The two-stage P0 → payload_digest → final signed projection is non-circular and uses domain separation by profile bundle and message type. H's exact allowlists for I pending gate, I gate release and I JF10 terminal decision improve determinism.

The profile uses RFC 8785 JCS, SHA-256 and Ed25519 as a proposed suite. Ed25519 regulatory/FIPS suitability is not decided. No production algorithm approval is inferred.

### A-CRYPTO-04 — Snapshot and completeness proofs

**ACCEPT AS SCHEMA CANDIDATE.** Unified schema 1.2.8 adds an owner snapshot attestation digest. RecoveryJoin 1.0.1 defines typed COMPLETE_EMPTY and OUT_OF_SCOPE proof objects with query, pagination, high-water, key-status and anti-rollback fields. This is materially better than treating a locator or count=0 as proof.

The semantic validator must still verify the referenced proof, exact digest, current key status and complete ledger query. Structural presence is not authoritative enumeration.

### A-CRYPTO-05 — Versioning and downgrade

**ACCEPT WITH CONDITION.** Schema artifact revision 1.2.8 is distinct from on-wire family version 1.2.0. The optional `signature_profile_id` is backward-compatible structurally, but protected I messages MUST reject a missing, unknown or mismatched profile semantically. Old strict consumers may reject the new field; that is a safe incompatibility, not a reason to strip the field or downgrade.

### A-CRYPTO-06 — CI evidence scope

**ACCEPT LIMITED EVIDENCE.** H's 97/97 CI run validates the current reference-model/schema candidate tests, including the two new schema assertions. The existing Python/Node differential fixture covers fixed UTF-8/digest bytes only. It does not validate RFC 8785 JCS for all I projections or Ed25519 across independent implementations.

## 3. Blocking conditions / 阻断条件

1. **I-H-CRYPTO-03:** define deterministic preallocated `owner_signature_ref` / `signature_ref` construction, namespace, uniqueness, digest mapping and restore behavior.
2. **I-H-CRYPTO-04:** implement two independent JCS + Ed25519 stacks and byte-for-byte positive/negative vectors for all I P0 projections, including nested snapshot, COMPLETE_EMPTY and OUT_OF_SCOPE proofs.
3. **I operational approval:** decide regulatory/FIPS suitability, trust-root ceremony, HSM/KMS, key rotation/overlap, compromise response, revocation propagation, nonce/receipt retention and external anti-rollback checkpoint.
4. **I runtime:** implement durable single-use nonce/receipt consumption in the PolicyDomain sequencer and prove revocation-vs-commit linearization, lost ACK and restore continuity.
5. **Storage acceptance:** Storage must verify the exact ICommitAuthorizationProof at the actual final visibility linearization point, with same D/Storage tuple and no circular ITerminalProof dependency.
6. **Independent governance:** obtain actual human Owner and governance approval; delegated role simulation is not independent approval.

## 4. Cross-phase implications / 对 Phase 3.8 全局影响

This update advances only the I/H cryptographic and schema contract. It does not resolve:
- Storage T1–T8 topology ADR (**ADR-BLOCKED / NO TOPOLOGY SELECTED**);
- integrated JF-10 same-GID/same-DB-incarnation physical conformance;
- C real provider adapter, same-key lookup and durable CSubmitOutcome;
- live COC quorum enumeration and owner-local release CAS;
- Global Forget inventory, external recipient/backup/restore terminal evidence;
- production activation, TAB-001 or Multi-PolicyDomain atomicity.

本次只推进 I/H 密码学与 Schema 合同，不解决 Storage T1–T8 拓扑 ADR、JF-10 物理一致性、C Provider Adapter/同键恢复、Live COC/Owner CAS、Global Forget 全量证据、生产激活、TAB-001 或 Multi-PolicyDomain 原子性。

## 5. Final A ruling / A 最终裁决

**CANDIDATE SECURITY/WIRE COMPOSITION: ACCEPTED WITH BLOCKING CONDITIONS.**

**JOINT CONTRACT FREEZE: NOT ACCEPTED.**

**PRODUCTION ACTIVATION: NOT AUTHORIZED.**

The exact I/H bundle is now coherent enough to advance to executable cryptographic conformance work, but not to freeze. No earlier HRC 66/66 or current 97/97 schema candidate pass can be reinterpreted as production cryptographic interoperability.

**候选 Security/Wire 组合：有条件接受。联合合同冻结：不接受。生产激活：未授权。** 精确 I/H Bundle 可进入可执行密码学一致性验证阶段，但尚不具备冻结条件。此前 HRC 66/66 或当前 97/97 Schema 候选测试均不能解释为生产密码学互操作通过。
