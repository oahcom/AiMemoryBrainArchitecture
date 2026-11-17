# P Draft — Storage v3.2.9 Successor Exact-Version Bundle
# P 草案 — Storage v3.2.9 后继精确版本 Bundle

- Status: **P COORDINATOR DRAFT / NOT STORAGE OWNER ISSUED / NOT JOINTLY ACCEPTED / NOT FROZEN**
- Predecessor: Storage v3.2.8 manifest Blob `b8a736e885a42d09f4776c34e8b6a93e6402b900`.
- Normative Storage v3.2.3 body: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- COC companion §§15–17: `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- Provenance: P simulated Storage role only.

## 1. Exact current bundle / 当前精确 Bundle

| Authority | Artifact | Exact Blob / Run | Status |
|---|---|---|---|
| Storage | v3.2.3 normative body | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative design candidate; L4 open |
| COC | Companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest / union |
| Storage | v3.2.8 predecessor manifest | `b8a736e885a42d09f4776c34e8b6a93e6402b900` | Historical; 27-test pin superseded |
| H | Unified 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Current |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Current |
| H | Authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | C/D/I callback interface candidate |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Current local validator |
| H | Full-path test source | `dccf8c099c18807ec072870d32604d0912209f01` | Full local path and negative mutations |
| H | Full positive fixture | `c80247a6ecfbb4a29ff0993e8e2aea4829d00626` | Synthetic fixture; owner proofs remain test doubles |
| H | Full-path closure | `5f487321b273ede41a7c23c3f94b6c0625968439` | Current H closure Blob |
| H | Provider Outcome CI | Run `44069941327`, commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251` | **32 tests, SUCCESS** |
| H | RecoveryCutoff CI | Run `44070707497`, commit `362cc113cfb5b595a4002a6f6e980d19ae2d2d15` | **288 total, 266 passed / 22 skipped / 0 failed** |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned immutable object |
| C | Sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C durable sequence namespace |
| C | Authority-join review | `29c0ceec57b27d189bf38581e0403241d6713c8d` | Delegated review of mapping 1cbe |
| C | Full-path review | `4be9c1cd8f116086bab58340f07e38ddfc223e21` | Existing review; refresh closure Blob/run pin |
| D | Current D crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | Current |
| D | Full-path clearance review | `ccdae9b45affb23c6741b5cceb27004b35a8e03e` | Existing review; refresh closure Blob/run pin |
| I | Current I P0 allowlist | `44986f5f864bcdc1a79d34978273644d381a68c0` | Current |
| I | Authority-join review | `34b29f405d4e8ceb1a039666bfe84518f62355f8` | Delegated review of callback contract |
| I | Full-path terminal review | `7c65650a37c8c0f270451fb0419e93259fc38151` | Existing review; refresh closure Blob/run pin |
| H | D proof cross-review | `6d45398885a842b0e5effc860bc97d7ecd3a8435` | H review only |
| H | I proof cross-review | `7acafcdc38079cdc51965f7b416d547372083965` | H review only |
| A | v3.2.8 Phase 1.G review | `cb2cb04d63ee05d929b5fb956687c8ed598563f5` | Historical; does not review v3.2.9 |
| A | v3.2.9 review | Not issued | Required after this exact manifest and refreshed C/D/I/H pins |

## 2. Exact reference correction / 精确引用修正

C Phase 3.8.18, D Phase 3.8.10 and I Phase 3.8.14 documents cite H commit SHA `f9c8d797d9a1ae9ea500c22534e98eb2f98cdff4` as a closure “Blob”. The actual H closure file Blob is `5f487321b273ede41a7c23c3f94b6c0625968439`. Their prior CI run `44069777296` is superseded by exact source rerun `44069941327` (32 tests). P provides role-simulation addenda; actual Owners must publish or confirm the corrected exact pins.

## 3. Required owner actions / 必需 Owner 行动

1. H keeps the current full-path closure and exact source/run pins current; any test/source Blob change requires a new run/closure.
2. C/D/I publish exact re-review addenda pinning closure Blob `5f487321...` and run `44069941327`.
3. Storage publishes actual v3.2.9 on its own branch, binding these exact sources and all review decisions.
4. A performs fresh exact review of the Storage-issued v3.2.9 manifest.
5. All production authority callbacks remain UNKNOWN unless connected to their respective authoritative sources; do not promote test-double VALID to production VALID.

## 4. Gate state / Gate 状态

- Full local H envelope + C object schema/semantic/digest path: **PASS**.
- I/D/Storage callback behavior: **test doubles only; production adapters NOT VERIFIED**.
- C provider issuer/same-key lookup/egress races: **OPEN**.
- I trust/profile/key custody/anti-rollback: **OPEN**.
- D full lineage/currentness/release CAS: **OPEN**.
- Storage same-GID/COC quorum/linearizable readback/L4 topology: **OPEN**.
- JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, Full Applied and production activation: **OPEN / BLOCKED / NOT AUTHORIZED**.

This is a P coordinator draft, not a Storage Owner publication, not a production readiness statement and not an architecture freeze.
