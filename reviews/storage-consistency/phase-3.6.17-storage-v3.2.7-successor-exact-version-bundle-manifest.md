# Phase 3.6.17 — Storage v3.2.7 Successor Exact-Version Bundle Manifest
# Phase 3.6.17 — Storage v3.2.7 后继精确版本 Bundle 清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 CANDIDATE BUNDLE BOUND; FRESH OWNER REVIEWS AND A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor exact bundle: Storage v3.2.6, Blob `dbfa37617d109d5891a067769e858085e2ce547a`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; **not an independent human Storage Owner signature**.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the C/H exact-version candidate pins in Storage v3.2.6 §3 and its H evidence status. It does not rewrite Storage v3.2.3 S0a–S4, alter the COC Batch-before-Manifest order, or transfer earlier Owner decisions to changed Blobs. Storage v3.2.3 remains the normative technical body; v3.2.6 remains the historical predecessor bundle.

本清单仅替代 Storage v3.2.6 §3 中 C/H 精确版本候选绑定及其 H 证据状态。不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不将旧 Owner 决议转移到新 Blob。Storage v3.2.3 仍是规范技术正文；v3.2.6 是历史前序 Bundle。

A changed Blob invalidates every review that pins the old Blob. Branch names and paths are not version bindings. No 1.2.13 review transfers to 1.2.14. No C/I/D/H role simulation is an independent human Owner signature.

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Storage durable log/recovery protocol v3.2.3 | 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge, same-GID recovery and evidence boundaries |
| COC | COC durable log/recovery companion §§15–17 | 5b950a3a29bd7a5276b92a49a9114d700718b987 | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest ordering amendment | 9704d110a06d0c2ee98be960054e0396d0b68546 | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | 0477f0329997e42a1cbf6ecb8127c5c01fa47051 | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.6 successor bundle | dbfa37617d109d5891a067769e858085e2ce547a | Historical H 1.2.13 / C 1.0.1 candidate bundle |

The v3.2.3 S0a–S4 order remains unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through their independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit the distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current C/H candidate pair / 当前 C/H 精确候选组合

| Role | Artifact | Exact Blob / run | Meaning and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema artifact 1.2.14 / wire 1.3.0 | 09fcd1fa29fe24255fbd87cae79dafb406594a59 | Current schema artifact; D ForgetFenceGeneration and owner gate generation carriers |
| H | RecoveryJoin schema 1.0.2 | 4b664e3bce465499bcdfd93796349a4ba7074002 | Separate owner_snapshot_membership_proofs and bidirectional owner-admission joins |
| H | RecoveryCutoff schema 1.0.5 | 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7 | Exact recovery cutoff structural family |
| H | Phase 3.8.10 Unified 1.2.14 / C 1.0.1 authority-join mapping | 1cbe74eba69325510d6b1019d971661f965eabf8 | Exact mapping candidate and separate I/D/Storage verifier seam contract |
| H | Provider Outcome validator core | eab961a08d41e871f38543b18ee60cf024977414 | Exact schema identity, C 1.0.1 dereference/equality and tri-state orchestration; authority adapters remain unconnected |
| H | Provider Outcome validator tests | 53774aca0224fd9a727dfa625ba142825f1754b0 | 25 tests; callback seam orchestration tests use test doubles for schema/semantic/digest primitives |
| H | Provider Outcome workflow | 4459d19f5b4eea058377d9819e48e81eed5c8c4b | CI workflow path filters include H 1.2.14 schema, validator and tests |
| H | Exact callback-seam CI | Run 44068247661; tested commit 0701b12c3f43e1e6d5706c8eb2747e1c583d60b7 | SUCCESS, 25 tests, 0 failed; tested validator/test Blobs equal the exact rows above; later H commit only added mapping evidence |
| C | CSubmitOutcome immutable schema 1.0.1 | a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda | C-owned object; required signed sequence_namespace_ref |
| C | Phase 3.11.1 sequence namespace amendment | 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb | C record_sequence and CKeyStatusEvent event_sequence share the durable C namespace |
| I | Phase 3.8.8 review of C 1.0.1 namespace | 0d78e5b2bfcf66cae6b757314cead84b9c942601 | Accepts required signed namespace field; does not register C/I profiles |

### 3.1 Meaning of H callback CI / H 回调 CI 的含义

The exact H run `44068247661` is a real GitHub Actions success on the exact validator and test Blobs pinned above. Its 25 tests include three independent Python/Node crypto interop suites and H validator unit tests. New tests call the actual `validate_provider_outcome` orchestration function and prove:
- I terminal decision, D Forget clearance and Storage resolution each have distinct callback slots;
- all three callbacks can participate in a VALID orchestration result when test doubles return True;
- missing all three callbacks yields UNKNOWN, never VALID.

**The tests mock schema validation, semantic validation and candidate digest/preimage calculation for the orchestration cases. They are not an end-to-end positive H envelope + C object validation test, do not authenticate real I/D/Storage proof payloads, and do not connect production authority stores.** Therefore the CI result is bounded orchestration evidence only.

H run `44068247661` 是真实 GitHub Actions 成功，且测试的 Validator/Test Blob 与本清单精确绑定一致。25 项测试包括三组 Python/Node 密码学互操作套件和 H Validator 单元测试。新增测试调用真实 `validate_provider_outcome` 编排函数，证明 I Terminal、D Forget Clearance、Storage Resolution 各有独立回调；Test Double 全部返回 True 时可得到 VALID 编排结果；缺少三者时只能得到 UNKNOWN。

**编排测试对 Schema 校验、语义校验和候选摘要/Preimage 计算使用了 Mock。它们不是完整 H Envelope + C Object 端到端正向验证，不认证真实 I/D/Storage 证明载荷，也未连接生产权威存储。** 因此 CI 仅是有限的编排证据。

## 4. Owner review/adoption matrix / Owner 精确审查与采纳矩阵

| Owner | Current exact evidence | Required decision against this v3.2.7 bundle |
|---|---|---|
| H | Phase 3.8.10 mapping Blob 1cbe74eba69325510d6b1019d971661f965eabf8; CI 44068247661 | Fresh H exact review of schema + validator + tests + CI; independent H Owner adoption still outstanding |
| C | C schema 1.0.1 Blob a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda; amendment Blob 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb; prior H 1.2.13 review only | Fresh C exact review of H 1.2.14 mapping and callback requirements; v3.2.13/1.2.13 review does not transfer |
| I | I namespace review Blob 0d78e5b2bfcf66cae6b757314cead84b9c942601 | Fresh I review of H 1.2.14 proof carrier and exact terminal-decision callback boundary; profile registration remains separate and NOT APPROVED |
| D | D H 1.2.13 / RecoveryJoin 1.0.2 proof-carrier review is historical for this schema revision | Fresh D exact review of 1.2.14 ForgetFenceGeneration / barrier-generation carrier and D clearance verifier boundary |
| Storage | This v3.2.7 candidate manifest | Storage source review and actual bidirectional COC↔I/D/C join / same-GID evidence remain outstanding |
| A | Prior v3.2.6 integration review Blob d34e19f239c8e3c59ec5fbc3ec795b6e3c1453ea | Fresh A exact integration review of this v3.2.7 manifest required; prior A decision does not transfer |

All previous role reviews were delegated simulations in the coordinating session, not independent human Owner signatures. Silence is not approval. This matrix records required adoption work; it does not manufacture it.

## 5. Required semantic and operational joins / 必需语义与运行 Join

1. C `payload_digest` equals H `c_submit_outcome_digest`; BMCP envelope digest and Provider Outcome Evidence digest remain distinct domains.
2. C `sequence_namespace_ref` must match authenticated CKeyStatusEvent namespace and the durable C signing sequencer.
3. I terminal decision is independently verified; provider invocation authorization requires the applicable I `COMMIT_WON` proof, not merely any I terminal outcome.
4. D Forget clearance independently verifies FenceGeneration, barrier/lineage membership and final effect boundary.
5. Storage resolution independently verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing authority callback/evidence/currentness/anti-rollback is UNKNOWN; proven contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Owner-local release requires each Owner's fresh final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Any H/C/I/D/Storage Blob change invalidates the affected review and requires a new exact manifest/review.

## 6. Gate state and non-claims / Gate 状态与非声明

- Storage technical architecture v3.2.3: normative candidate body unchanged.
- Storage v3.2.7: **CANDIDATE EXACT BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H 1.2.14 / C 1.0.1 callback CI: **SUCCESS, 25 tests; bounded orchestration only**.
- Complete unmocked H envelope + C object positive/negative matrix: **OPEN**.
- Production I/D/Storage authority callback adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C/I production profile registration, trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- Production activation, production provider egress, Provider exactly-once, Full Applied, Global Forget Completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

本清单不声称生产 Owner 签名、生产 Trust Root/Key Custody、真实 I/D/C Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 7. Required next sequence / 后续执行顺序

1. H Owner independently reviews exact schema/validator/test/mapping Blobs and CI 44068247661.
2. C and I independently review H 1.2.14 mapping and their own proof/authority obligations; no C/I profile registration is implied.
3. D independently reviews the exact 1.2.14 D fence/barrier carrier and D verifier boundary.
4. Add a complete unmocked positive H envelope + CSubmitOutcome 1.0.1 fixture and full-path negative mutations for wire duplicates, C-P0 digest, sequence namespace, I terminal result, D fence and Storage same-GID proof.
5. Bind production adapters to owner-authoritative I/D/Storage ledgers and trust/currentness sources; until then missing adapters remain UNKNOWN.
6. Storage proves bidirectional COC participant ↔ I/D/C owner admission joins, same-GID RecoveryJoin, quorum persistence and linearizable readback.
7. A performs fresh exact-version integration review of this manifest. No Gate or activation upgrade follows from CI alone.

## 8. Provenance / 来源说明

This manifest was authored in delegated Storage-role coordination mode. Exact file Blobs were fetched from their named owner branches and the H workflow run/job logs were read directly. This is a candidate version-binding and review-routing artifact, not an independent Storage Owner signature or runtime deployment result.

本清单由协调会话模拟 Storage 角色编写。精确文件 Blob 来自对应 Owner 分支读取，H Workflow Run/Job Log 已直接核验。本文件仅为候选版本绑定与复审路由工件，不是独立 Storage Owner 签名，也不是 Runtime 部署结果。
