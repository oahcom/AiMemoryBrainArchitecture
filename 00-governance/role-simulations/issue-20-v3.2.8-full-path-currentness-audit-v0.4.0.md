# Issue #20 — v3.2.8 Full-Path Currentness Audit v0.4.0
# Issue #20 — v3.2.8 Full-Path 当前性审计 v0.4.0

- Status / 状态: **P COORDINATOR CROSS-REVIEW / ROLE SIMULATION ONLY**
- Snapshot date / 快照日期: 2026-11-17
- C HEAD: `81f1e81307315a31c3bbeae17eb801e8a4f47e10`
- D HEAD: `7d01732521a8b9db202f10cde2c2547e50071d58`
- H HEAD: `8b83494ffc5366d524ed466f70a6354244bbf044`
- I HEAD: `a68bb3587fe88aa72398e2dc8d136f94cee9a63f`
- Storage HEAD: `85785fac51a249e9e9684eaef584633ff513e67d`
- A HEAD: `0bb77a3df8023ef0a5e27d79a0a9c49509a5b3f7`
- P HEAD before this audit: `220d7bc5179afc62715ee2a0571167363b27864c`
- Decision / 结论: **The v3.2.8 base bundle is coherent at L1/L2, and H now has a full local H-envelope + C-object schema/semantic/digest path. v3.2.8 manifest is stale to that evidence; C/D/I review documents also mislabel an H commit SHA as a Blob. Prepare v3.2.9; NOT JOINTLY FROZEN.**

## 1. Executive result / 执行结论

This is a material advance from the callback-seam-only stage:
- H Phase 3.8.14 now supplies a synthetic positive H envelope + immutable CSubmitOutcome 1.0.1 fixture and calls the actual validator with real H/C schemas, real local semantic predicates and real C-P0 digest recomputation.
- H Provider Outcome run `44069941327` passed **32 tests** on commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`; current H source/test/fixture blobs match the pinned closure.
- C Phase 3.8.17/3.8.18, D Phase 3.8.10 and I Phase 3.8.13/3.8.14 have published delegated role reviews of the callback boundaries and full-path evidence.
- A Phase 1.G has reviewed Storage v3.2.8 and conditionally accepted it as a coherent candidate with blockers; it is not independent human approval.
- Storage v3.2.8 exists as a candidate successor manifest.

The v3.2.8 manifest is no longer current because it pins the earlier 27-test source/run `70a379...` / `44068869146`, whereas H's full-path test source is `dccf8c...`, full fixture is `c80247...`, current H closure is Blob `5f487321...`, and full-path run `44069941327` reports 32 tests.

A second exact-reference defect remains in the C/D/I full-path review documents: each labels H commit `f9c8d797...` as an “H closure Blob”. The actual H closure file Blob is `5f487321...`; `f9c8d797...` is a commit SHA. The reviews also cite the earlier run `44069777296`, while the same exact H test/fixture/core/schema Blobs have since been rerun successfully in `44069941327`.

**Disposition: ACCEPT AS COHERENT L1/L2 ARCHITECTURE CANDIDATE; PREPARE v3.2.9 EXACT SUCCESSOR; DO NOT FREEZE.**

## 2. Exact current source inventory / 当前精确源清单

| Owner | Artifact | Exact Blob / run | Status |
|---|---|---|---|
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Current |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Current |
| H | Authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Current callback contract |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Current |
| H | Full-path validator tests | `dccf8c099c18807ec072870d32604d0912209f01` | Current 32-test source set |
| H | Full positive H envelope + C object fixture | `c80247a6ecfbb4a29ff0993e8e2aea4829d00626` | Synthetic test fixture |
| H | Full-path closure | `5f487321b273ede41a7c23c3f94b6c0625968439` | Current H closure Blob |
| H | Provider Outcome CI | Run `44069941327`, commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251` | **32 tests, SUCCESS** |
| H | RecoveryCutoff CI | Run `44070707497`, commit `362cc113cfb5b595a4002a6f6e980d19ae2d2d15` | **288 total, 266 passed / 22 skipped / 0 failed** |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Current |
| C | C sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | Current |
| C | H authority-join review | `29c0ceec57b27d189bf38581e0403241d6713c8d` | Accepts mapping `1cbe74e...` as L1/L2 |
| C | H full-path review | `4be9c1cd8f116086bab58340f07e38ddfc223e21` | Accepts local full path; closure pin/run require refresh |
| D | Current RecoveryJoin crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | Current D proof source |
| D | H full-path / clearance review | `ccdae9b45affb23c6741b5cceb27004b35a8e03e` | Accepts local D callback boundary; closure pin/run require refresh |
| I | Current I P0 allowlist | `44986f5f864bcdc1a79d34978273644d381a68c0` | Current |
| I | H authority-join review | `34b29f405d4e8ceb1a039666bfe84518f62355f8` | Accepts I carrier/callback candidate |
| I | H full-path / terminal callback review | `7c65650a37c8c0f270451fb0419e93259fc38151` | Accepts local I callback boundary; closure pin/run require refresh |
| H | H review of D crosswalk | `6d45398885a842b0e5effc860bc97d7ecd3a8435` | H-side review; not D Owner signature |
| H | H review of I P0 | `7acafcdc38079cdc51965f7b416d547372083965` | H-side review; not I Owner signature |
| Storage | v3.2.8 manifest | `b8a736e885a42d09f4776c34e8b6a93e6402b900` | Candidate; test/run pins stale |
| A | Phase 1.G review of v3.2.8 | `cb2cb04d63ee05d929b5fb956687c8ed598563f5` | Conditional candidate acceptance; stale to new full-path evidence/v3.2.9 |
| Storage | Normative v3.2.3 body | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative technical candidate |
| Storage | COC companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest / union semantics |

## 3. Full local validation result / 本地完整验证结果

H Phase 3.8.14 tests 21–25 load the real H Unified 1.2.14 schema, CSubmitOutcome 1.0.1 schema and synthetic fixture, then call the actual `validate_provider_outcome` implementation without patching:
- schema validation;
- local C semantic predicates;
- C-P0 canonical digest and signature-preimage construction.

Covered outcomes:
1. Full local H envelope + C object schema/semantic/digest path → VALID when authority test doubles return True.
2. Wire/object duplicate `provider_ref` mismatch → INVALID.
3. Mutated C `payload_digest` and matching wire digest, while P0 content remains unchanged → INVALID after recomputation.
4. Missing I/D/Storage callbacks → UNKNOWN.
5. Each I/D/Storage callback returning False → INVALID.

This closes the earlier gap for a full **local** schema/semantic/digest path. It does not authenticate real owner proof payloads: all ten authority callbacks in the fixture are deterministic test doubles. The fixture signature is not authenticated by a production trust root; provider evidence issuer, C key-status ledger, I terminal proof, D clearance proof, Storage same-GID proof and anti-rollback are not connected to production stores.

## 4. Exact-reference correction / 精确引用修正

The current C Phase 3.8.18, D Phase 3.8.10 and I Phase 3.8.14 full-path reviews each identify H closure commit `f9c8d797d9a1ae9ea500c22534e98eb2f98cdff4` as a “Blob”. This is not a Blob identity; it is an H branch commit SHA. The actual H closure file Blob is `5f487321b273ede41a7c23c3f94b6c0625968439`.

The C/D/I reviews cite H run `44069777296` at commit `9eb063...`. H subsequently ran the same exact test/fixture/core/schema source set in run `44069941327` at commit `ba2c934...`, with 32 tests and SUCCESS. H closure Blob `5f487321...` pins the latter exact run. Fresh C/D/I addenda should pin the actual closure Blob and current run, not a commit SHA mislabeled as a Blob.

## 5. Storage successor and A review / Storage 后继与 A 审查

Storage v3.2.8 manifest Blob `b8a736...` binds the callback mapping but pins H test Blob `70a379...` and 27-test run `44068869146`; it predates the full-path test source and run. A Phase 1.G review Blob `cb2cb0...` reviews exactly that v3.2.8 manifest and its 27-test ceiling. Neither automatically transfers to v3.2.9.

P therefore prepares a v3.2.9 draft binding:
- H current full-path closure Blob `5f487321...`;
- H test Blob `dccf8c...` and fixture Blob `c80247...`;
- H exact Provider Outcome run `44069941327` (32 tests);
- H RecoveryCutoff run `44070707497`;
- C/D/I current role-review source Blobs, with explicit refresh addenda correcting the H closure Blob/run pins;
- A Phase 1.G v3.2.8 review as historical predecessor only.

Storage must publish its actual v3.2.9 manifest on the Storage branch; P cannot issue it on Storage's behalf.

## 6. Gate disposition / Gate 处置

- H 1.2.14 × C 1.0.1 local schema/semantic/digest path: **PASS**.
- H full-path authority callbacks: **TEST DOUBLES ONLY**.
- C/D/I callback boundary reviews: **L1/L2 role-simulated acceptance; exact closure Blob/run refresh needed**.
- Production C signature/key status/provider issuer: **NOT VERIFIED**.
- Production I trust/key status/COMMIT_WON verifier: **NOT VERIFIED**.
- Production D lineage/fence/clearance/release CAS: **NOT VERIFIED**.
- Production Storage same-GID/COC quorum/visibility: **NOT VERIFIED**.
- JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, Full Applied and production activation: **OPEN / BLOCKED / NOT AUTHORIZED**.

## 7. Provenance / 来源说明

This is a Session P coordinator audit. It does not sign for C/D/H/I/Storage/A and does not turn delegated role simulations into independent human Owner decisions. No Owner branch or `main` is modified by this audit.

本文件是 Session P 协调者审计，不代替 C/D/H/I/Storage/A 签署，也不将角色模拟转化为独立人类 Owner 决议。本审计不修改任何 Owner 分支或 `main`。
