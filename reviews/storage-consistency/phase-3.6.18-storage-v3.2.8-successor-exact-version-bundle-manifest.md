# Phase 3.6.18 — Storage v3.2.8 Successor Exact-Version Bundle and Owner Review Manifest
# Phase 3.6.18 — Storage v3.2.8 后继精确版本 Bundle 与 Owner 复审清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 EXACT CANDIDATE BUNDLE BOUND; C/H/I/D ROLE REVIEWS RECORDED; H CURRENT CI PASS; FRESH A REVIEW REQUIRED; NOT JOINTLY FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor bundle: Storage v3.2.7, Blob `684908d0f1bc6def5be565dba76f4d2037545f71`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role successor manifest; **not an independent human Storage Owner signature**.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the exact C/H/I/D review and source pins in Storage v3.2.7. It does not rewrite Storage v3.2.3 S0a–S4, alter the COC Batch-before-Manifest ordering, or upgrade any production gate. Storage v3.2.3 remains the normative technical body; v3.2.7 remains the immediate predecessor.

本清单仅替代 Storage v3.2.7 中 C/H/I/D 精确复审与源文件绑定，不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不提升任何生产 Gate。Storage v3.2.3 仍为规范技术正文；v3.2.7 为直接前序。

Any changed Blob invalidates reviews that pin the previous Blob. Branch names and file paths are not version bindings. The current candidate pair is H Unified 1.2.14 / wire 1.3.0 and immutable CSubmitOutcome 1.0.1. The candidate is not a protocol freeze, production trust approval or deployment authorization.

任何 Blob 变化都会使绑定旧 Blob 的审查失效。分支名与文件路径不是版本绑定。当前候选版本对为 H Unified 1.2.14 / Wire 1.3.0 与不可变 CSubmitOutcome 1.0.1。本候选不构成协议冻结、生产信任批准或部署授权。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge and same-GID recovery |
| COC | Durable log/recovery companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.7 exact bundle manifest | `684908d0f1bc6def5be565dba76f4d2037545f71` | Historical candidate and prior review matrix |

The normative S0a–S4 order is unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current protocol and source bundle / 当前协议与源文件精确 Bundle

| Authority | Artifact | Exact Blob / Run | Meaning and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current schema; includes D ForgetFenceGeneration high-water carrier |
| H | Authority-Join mapping Phase 3.8.10 | `1cbe74eba69325510d6b1019d971661f965eabf8` | Exact C object/wire mapping and separate I/D/Storage authority callback seams |
| H | RecoveryJoin schema 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Closed generic owner membership proof carrier |
| H | RecoveryCutoff schema 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Exact Recovery Cutoff structure |
| H | C/D/I crosswalk review Phase 3.8.12 | `90cdadd7d80676c1338965576c955a5f336ad0bc` | Cross-review of C/D/I generic P0 and owner-digest dereference mappings |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | H 1.2.14 / C 1.0.1 fail-closed validator with ten authority callback classes |
| H | Current validator test source | `70a3796446553464e71999f916b76bc22e47da11` | Current exact 27-method test source; orchestration tests use test doubles for schema/semantic/digest primitives |
| H | Current-head CI/source closure Phase 3.8.13 | `9083ad54581352c83be21ac981aea845cd307382` | Exact current source pins and run readback; authority integration remains open |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Workflow path filters include H schema, validator and tests |
| H | Exact current CI | Run `44068869146`, tested commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`, job `133989610753` | completed/success; 27 tests per current Storage readback; bounded source-level conformance only |
| C | CSubmitOutcome immutable schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned object; signed sequence_namespace_ref |
| C | C sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C record_sequence and CKeyStatusEvent event_sequence share durable C namespace |
| C | C RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C row/digest indirection into generic RecoveryJoin P0 |
| C | C exact review Phase 3.8.17 plus CI addendum | `29c0ceec57b27d189bf38581e0403241d6713c8d` | Accepts H authority-join mapping; current H test/CI pins refreshed |
| I | I P0 allowlist successor for H 1.2.14 | `44986f5f864bcdc1a79d34978273644d381a68c0` | Exact I common-envelope and proof-family P0 candidate; corrected H schema pin |
| I | I exact review Phase 3.8.13 plus CI addendum | `34b29f405d4e8ceb1a039666bfe84518f62355f8` | Accepts I terminal callback boundary and H mapping candidate; trust/L3 remain open |
| D | D RecoveryJoin membership P0 crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D owner row/operation/scope/fence/barrier/lineage digest indirection |
| D | D exact review Phase 3.8.9 plus CI addendum | `40fee15d7e42d68da231ea161896f85df2921669` | Accepts D clearance callback boundary; lineage/currentness/release remain open |
| Storage | This v3.2.8 manifest | `self-reference intentionally omitted` | Exact bundle and review routing; not independent Storage approval |

## 4. Exact CI meaning and limitations / CI 精确含义与限制

Run `44068869146` completed successfully on exact commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8`, with current H validator Blob `eab961...` and test Blob `70a379...`. The suite contains 27 test methods: six Python/Node crypto interoperability methods and 21 H validator unit methods, as recorded by the current Storage evidence readback.

The tests exercise strict JSON handling, H/C schema pins, C sequence namespace, outcome conditional semantics, digest/profile behavior and separate I/D/Storage callback slots. The callback orchestration cases mock schema validation, semantic validation and candidate digest/preimage calculation. They do **not** constitute a complete unmocked H envelope + immutable C object positive/negative path, do not authenticate real I/D/Storage proof payloads, and do not connect production authority stores.

Run `44068869146` 在精确 Commit 上成功，使用当前 H Validator/Test Blob。套件共 27 个测试方法：6 个 Python/Node Crypto Interop 与 21 个 H Validator Unit Methods。测试覆盖 Strict JSON、H/C Schema Pin、C Sequence Namespace、Outcome 条件语义、Digest/Profile 与 I/D/Storage 独立 Callback。回调编排测试 Mock Schema、语义及候选 Digest/Preimage 计算。它们**不是完整未 Mock 的 H Envelope + C Object 正负路径**，不认证真实 I/D/Storage Proof，也未连接生产权威存储。

## 5. Exact owner review matrix / Owner 精确复审矩阵

| Owner | Exact review Blob | Scope and disposition | Remaining conditions |
|---|---|---|---|
| H | Mapping Blob `1cbe74...`; crosswalk review `90cdad...`; source closure `9083ad...` | Delegated H-role acceptance of L1/L2 mapping, generic P0 crosswalk and current source/CI | Independent human H adoption; full unmocked envelope/object path; production callbacks |
| C | Phase 3.8.17 review Blob `29c0ce...` | ACCEPT H authority-join mapping with CSubmitOutcome 1.0.1 as L1/L2 candidate | Production profile/key status, provider issuer, same-key lookup, adapter race/fault and live egress serialization |
| I | Phase 3.8.13 review Blob `34b29f...` | ACCEPT I terminal proof carrier/P0 compatibility as L1/L2 candidate | Trust root, key custody, L3 vectors, historical verification, anti-rollback and production authorization |
| D | Phase 3.8.9 review Blob `40fee1...` | ACCEPT D clearance carrier as L1/L2 candidate | Full lineage, late-discovery, currentness CAS and production release |
| Storage | This manifest | Binds exact bundle and owner review scope | Bidirectional COC joins, same-GID recovery, quorum durability and linearizable readback |
| A | No review of v3.2.8 yet | **PENDING** | Fresh exact-version A review required; v3.2.7 A decision does not transfer |

All C/H/I/D decisions above are delegated role simulations and source-level architecture reviews, not independent human Owner signatures. They do not constitute formal organizational approvals. A's review must preserve this distinction.

## 6. Required semantic and operational joins / 必需语义与运行 Join

1. C `payload_digest` equals H `c_submit_outcome_digest`; BMCP envelope digest and Provider Outcome Evidence digest remain separate domains.
2. C `sequence_namespace_ref` equals the authenticated CKeyStatusEvent namespace and durable C signing sequencer namespace.
3. I terminal authorization must verify the exact I-signed proof and applicable `COMMIT_WON`; a generic I terminal result is insufficient.
4. D Forget clearance must independently verify FenceGeneration, complete affected lineage/barrier membership and final effect boundary.
5. Storage resolution must independently verify DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing authority callback/evidence/currentness/anti-rollback is UNKNOWN; proven contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Owner-local release requires each Owner's own final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Any H/C/I/D/Storage Blob change invalidates the affected review and requires a new exact manifest/review.

## 7. Gate state and non-claims / Gate 状态与非声明

- Storage technical architecture v3.2.3: normative design candidate unchanged.
- Storage v3.2.8: **EXACT CANDIDATE BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H 1.2.14 / C 1.0.1 source-level CI: **SUCCESS; 27 tests; bounded unit/schema/fixture/crypto/callback-orchestration evidence**.
- Complete unmocked H envelope + C object positive/negative matrix: **OPEN**.
- Production I/D/Storage authority callback adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- C/I production profile registration, trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- D lineage completeness, late-discovery and final release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin, same-GID recovery, quorum durability and linearizable readback: **OPEN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- Production activation, provider egress, Provider exactly-once, Full Applied, Global Forget Completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

本清单不声称生产 Owner 签名、生产 Trust Root/Key Custody、真实 C/D/I Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 8. Required next sequence / 后续执行顺序

1. A performs a fresh exact-version integration review of this v3.2.8 manifest and all pinned Blobs.
2. H adds a complete unmocked positive H envelope + CSubmitOutcome 1.0.1 fixture and full-path negative mutations for every duplicated wire field, C-P0 digest, sequence namespace, I terminal result, D fence and Storage same-GID proof.
3. C/H/I complete independent P0/JCS/digest/signature-preimage vectors and production authority callback contracts.
4. D executes lineage membership, late-discovery and final release-CAS fault evidence.
5. Storage proves bidirectional COC participant ↔ I/D/C owner admission joins, same-GID RecoveryJoin, quorum persistence and linearizable readback.
6. Only after all actual evidence predicates close may the project consider Gate B/C, protocol freeze or production activation.

## 9. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Exact source Blobs and the H workflow run/job were read from GitHub. This is a version-binding and review-routing artifact, not an independent Storage Owner signature, runtime deployment result or production conformance statement.

本清单由协调会话模拟 Storage 角色编写。所有源 Blob 与 H Workflow Run/Job 均从 GitHub 读回。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名、Runtime 部署结果或生产符合性声明。
