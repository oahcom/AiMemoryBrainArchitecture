# P Draft — Storage v3.2.8 Successor Exact-Version Bundle
# P 草案 — Storage v3.2.8 后继精确版本 Bundle

- Status / 状态: **P COORDINATOR DRAFT / NOT STORAGE OWNER ISSUED / NOT JOINTLY ACCEPTED / NOT FROZEN**
- Predecessor: Storage v3.2.7 manifest Blob `4435fc0340a4fce10751679a95f3b4c821bdae4d`.
- Normative Storage body: v3.2.3 Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- Provenance: simulated Storage role in Session P only.

## 1. Exact candidate bundle / 精确候选 Bundle

| Role | Artifact | Exact Blob / run | Status |
|---|---|---|---|
| Storage | Normative v3.2.3 technical body | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative candidate; L4 topology/deployment open |
| COC | Companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest and union semantics |
| Storage | v3.2.7 predecessor manifest | `4435fc0340a4fce10751679a95f3b4c821bdae4d` | Historical; H 25-test pin superseded |
| H | Unified 1.2.14 / wire 1.3.0 schema | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Current |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Current |
| H | Phase 3.8.11 base C mapping | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` | C accepts as L1/L2 candidate |
| H | Phase 3.8.10 authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Callback candidate; C/D/I/Storage re-review outstanding |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Integration seam only |
| H | Validator tests | `70a3796446553464e71999f916b76bc22e47da11` | Current 27-test source; mock boundaries disclosed |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Current workflow |
| H | Provider Outcome CI | Run `44068869146`, commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8` | 27/27 PASS; bounded orchestration/reference evidence |
| H | RecoveryCutoff CI | Run `44068869090`, same commit | 288 total; 266 passed / 22 skipped / 0 failed |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C immutable object |
| C | Sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C sequence namespace |
| C | Base mapping exact review | `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c` | Does not yet accept callback mapping |
| D | Current RecoveryJoin crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | Current D source |
| D | Current schema review | `6aca7d020caecf3c69debf614c903bf469583260` | Pins old crosswalk bf35; fresh D review required |
| H | D cross-review | `6d45398885a842b0e5effc860bc97d7ecd3a8435` | H accepts D carrier; not D Owner approval |
| I | Current P0 allowlists | `44986f5f864bcdc1a79d34978273644d381a68c0` | Current I source |
| I | Current schema review | `fbd44d57bdb4fc15c4c254fcd9d8ac4c58d365fc` | Pins old P0 35e684; fresh I review required |
| H | I cross-review | `7acafcdc38079cdc51965f7b416d547372083965` | Pins older I P0 5c0e; fresh H review required |
| Storage | v3.2.7 manifest | `4435fc0340a4fce10751679a95f3b4c821bdae4d` | Predecessor; not current H test/run |
| A | v3.2.8 integration review | Not issued | Required after same exact Owner bundle is reviewed |

## 2. Required Owner actions / 必须的 Owner 行动

1. H issues current closure for the exact mapping/schema/validator/test/run tuple.
2. C adopts or rejects the I/D/Storage callback mapping explicitly.
3. D reviews current crosswalk `c4adf82...` and D clearance callback.
4. I reviews current P0 `44986f5...` and I terminal-decision callback.
5. Storage confirms same-GID resolution, bidirectional COC ↔ owner admission joins, quorum durability and linearizable readback.
6. A reviews the same v3.2.8 manifest and exact Owner decisions.

## 3. Gate / 非声明

The draft is not a Storage Owner publication and does not select a physical DB topology. Production trust registration, C provider adapter certification, production I/D/Storage callbacks, complete unmocked H+C validation, COC quorum, JF-10 P0, R1/R2, Gate B/C, Global Forget and production activation remain OPEN / NOT AUTHORIZED.
