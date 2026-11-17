# P Draft — Storage v3.2.10 Successor Full-Path 38-Test Exact Bundle
# P 草案 — Storage v3.2.10 后继 Full-Path 38-Test 精确 Bundle

- Status: **P COORDINATOR / SIMULATED STORAGE ROLE DRAFT; NOT STORAGE OWNER ISSUED; NOT JOINTLY ACCEPTED; NOT FROZEN**
- Predecessor: Storage v3.2.9 manifest Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3`.
- Normative Storage body: v3.2.3 Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- Date: 2026-11-17.
- Provenance: Session P simulated Storage role. This draft is not a Storage Owner signature or deployment record.

## 1. Purpose and supersession / 目的与替代关系

This successor draft updates only the exact H full-path source/test/fixture/CI and C/I/D review pins in v3.2.9. It preserves the v3.2.3 S0a–S4 normative body, COC Batch-before-Manifest order and all prior non-claims. It does not promote test doubles to production authorities, select a physical database engine, or close JF-10 P0, R1/R2 or Gate B/C.

本后继草案仅更新 v3.2.9 中 H Full-Path Source/Test/Fixture/CI 与 C/I/D 复审精确绑定。保留 v3.2.3 S0a–S4 规范正文、COC Batch-before-Manifest 顺序及所有既有非声明。不将 Test Double 提升为生产权威，不选择物理数据库引擎，也不关闭 JF-10 P0、R1/R2 或 Gate B/C。

## 2. Unchanged normative base / 不变的规范基线

| Authority | Artifact | Exact Blob | Status |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative design body; L4 implementation OPEN |
| COC | Companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Dual-ledger union, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with backlink |
| Storage | R1/R2 successor-round/release addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.9 manifest | `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` | Historical 32-test source bundle |

Normative S0a–S4 remains:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit a distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current protocol/source set / 当前协议与源文件精确集合

| Authority | Artifact | Exact Blob / Run | Scope and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current H envelope schema; D ForgetFenceGeneration carrier |
| H | Authority-Join mapping Phase 3.8.10 | `1cbe74eba69325510d6b1019d971661f965eabf8` | Exact C object/wire mapping and independent I/D/Storage callback seams |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Generic owner membership proof carrier |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Exact recovery cutoff structure |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | H 1.2.14 / C 1.0.1 local validation and tri-state callback orchestration |
| H | Expanded full-path test source | `540056d7c4f290c31290b17c264c69cfd76b1cb2` | 32 H validator test methods; tests 21–31 exercise local full path and negative mutations |
| H | Full positive fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic fixture; all ten authority callbacks/test proofs remain test-only |
| H | Expanded full-path closure Phase 3.8.15 | `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504` | Exact source/fixture/test/run pins and 22-field mutation matrix |
| H | C crypto interop test sources | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node crypto interoperability methods |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Provider Outcome unittest discovery |
| H | Exact expanded CI | Run `44070924346`; commit `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`; job `133996627914` | SUCCESS; **38 tests** (32 H validator + 6 crypto interop) |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C-owned provider outcome; signed sequence_namespace_ref |
| C | Sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome and CKeyStatusEvent share durable C namespace |
| C | RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C row/digest indirection into generic RecoveryJoin P0 |
| C | Expanded full-path mutation review Phase 3.8.19 | `5edff732fdf0ece1fdcecd38b582ad33aa071b2a` | Accepts 22-field local mutation matrix; production C trust/provider truth open |
| I | I P0 allowlist | `44986f5f864bcdc1a79d34978273644d381a68c0` | I-owned common envelope/proof-family P0 candidate |
| I | Expanded full-path/envelope-auth review Phase 3.8.15 | `df869ef90e6279602b4d46128a81b2dc6ba01d71` | Accepts local callback test boundary; explicitly identifies outer envelope authentication gap |
| D | RecoveryJoin P0 crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D owner row/operation/scope/fence/barrier/lineage digest indirection |
| D | Expanded fence-clearance review Phase 3.8.11 | `1ce8f25db1971b692112e47aeae431af4e69b5e5` | Accepts local D callback mutation evidence; production lineage/release open |
| Storage | This v3.2.10 draft | Self-reference omitted | Candidate exact bundle only; not independent Storage approval |

All C/I/D reviews above are delegated role simulations and technical source reviews, not independent human Owner signatures or formal governance approvals. Any changed source Blob invalidates the corresponding review pin.

## 4. Exact CI meaning / CI 精确含义

Run `44070924346` completed SUCCESS on exact commit `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`, job `133996627914`. The job log reports `Ran 38 tests` and `OK`.

The 32 H validator methods include:
- actual H/C JSON Schema validation and complete synthetic H envelope + immutable C object path;
- exact object/wire equality and C semantic predicates;
- actual C-P0 digest recomputation;
- one-at-a-time mutation of all 22 duplicated wire fields present in the fixture;
- C-P0 member + synchronized wire mutation with old digest retained;
- C sequence namespace contradiction;
- I callback rejects REVOCATION_WON when COMMIT_WON is required;
- D callback rejects wrong ForgetOperation/FenceGeneration;
- Storage callback rejects wrong DB incarnation/GID/PrepareAttempt/participant-ledger tuple;
- missing authority callback → UNKNOWN; proven contradiction → INVALID.

The six remaining methods are Python/Node C cryptographic interoperability checks.

**Evidence ceiling:** The ten I/D/Storage/C-key-status authority callbacks in the fixture remain deterministic test doubles. This run proves local H/C schema, semantic, digest and bounded callback-predicate behavior. It does not prove production C signature/key-status/sequencer, provider issuer truth, authoritative same-key lookup, production I/D/Storage proof authentication, complete owner-ledger pagination, live currentness CAS, external anti-rollback, provider adapter race/fault, COC quorum, same-GID physical recovery, linearizable visibility or production deployment.

## 5. Owner review matrix / Owner 复审矩阵

| Owner | Exact review Blob | Decision/scope | Still open |
|---|---|---|---|
| C | `5edff732fdf0ece1fdcecd38b582ad33aa071b2a` | Accepts expanded 22-field local C semantic/wire mutation evidence on H mapping `1cbe74...`, test `540056...`, fixture `f911...`, closure `60e5...`, run `44070924346` | Production C trust/key status/sequencer, provider issuer truth, same-key lookup, adapter race/fault and egress serialization |
| I | `df869ef90e6279602b4d46128a81b2dc6ba01d71` | Accepts local I callback boundary; confirms outer envelope authentication is not covered by Provider Outcome tests | Real I proof verifier, trust roots, key custody, historical verification, anti-rollback, outer H Gateway/Auth |
| D | `1ce8f25db1971b692112e47aeae431af4e69b5e5` | Accepts local D clearance callback mutation as L1/L2 evidence | Complete lineage pagination, late discovery, barrier terminality, D currentness/release CAS |
| H | `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504` | Accepts expanded local full-path and 22-field mutation suite | Outer envelope authentication, production owner adapters, L3 completeness, COC/Storage durability |
| Storage | This draft | Binds exact bundle and review routing | Bidirectional COC joins, same-GID recovery, quorum durability and linearizable readback |
| A | v3.2.9 review Blob `df79f918c26a8e59e777bb100aa8d7a5c368d98a` | Reviews predecessor v3.2.9 manifest `bf323a...`, not this v3.2.10 draft | Fresh A review of actual Storage-issued v3.2.10 Blob required |

## 6. New explicit security boundary / 新增明确安全边界

The Provider Outcome validator does not authenticate the outer H envelope's own payload digest/signature, channel binding, key status or sender identity against the authenticated transport principal. I Phase 3.8.15 requires a separate H Gateway/Auth step before durable acceptance:

1. verify canonical outer-envelope payload digest and signature under an approved H profile;
2. authenticate channel-binding proof and issuer key status;
3. bind sender_authority_ref / sender_subject_ref / issuer_ref to the authenticated transport principal and registered authority;
4. reject replay/duplicate, stale key, wrong audience, PolicyDomain mismatch, signature/digest substitution and principal mismatch;
5. enforce order: outer-envelope authentication → H/C schema + C-P0 validation → C/I/D/Storage authority joins → durable acceptance.

Until a separately reviewed H Gateway/Auth contract and negative test suite exist, outer-envelope authentication remains OPEN. C object signature/digest verification must never be mistaken for H envelope authentication.

## 7. Gate state / Gate 状态

- Local H/C full-path schema/semantic/digest: **PASS, 38-test exact CI**.
- 22 duplicated wire-field mutation matrix: **PASS in local test fixture**.
- I/D/Storage callback predicates: **TEST-ONLY; production authority not verified**.
- Outer H envelope authentication/channel binding/transport principal binding: **OPEN / P0 SECURITY GATE**.
- C production trust/provider issuer/same-key lookup/egress: **OPEN**.
- I trust/key custody/history/anti-rollback: **OPEN**.
- D complete lineage/late discovery/release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin/same-GID/quorum/linearizable readback/L4: **OPEN**.
- JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, Full Applied, physical erasure and production activation: **OPEN / BLOCKED / NOT AUTHORIZED**.

## 8. Required next sequence / 后续顺序

1. H defines and tests the separate outer-envelope Gateway/Auth validation contract, including transport-principal binding, replay/audience/key-status and negative vectors.
2. C/I/D/H confirm the exact 38-test source/fixture/closure pins; no review transfers if any Blob changes.
3. Storage Owner publishes actual v3.2.10 on the Storage branch; do not modify v3.2.9 in place.
4. A independently reviews the actual Storage-issued v3.2.10 manifest.
5. Implement production authority adapters and close C/D/I/Storage evidence obligations independently.
6. Only after independent evidence and governance approvals may any freeze or production Gate transition be considered.

**Disposition: BOUND FOR JOINT REVIEW ONLY; NOT JOINTLY ACCEPTED / NOT FROZEN.**
