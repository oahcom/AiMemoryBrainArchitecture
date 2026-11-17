# Storage-role draft — v3.2.8 successor exact-version bundle manifest
# Storage 角色草案 — v3.2.8 后继精确版本 Bundle 清单

- Status: **P COORDINATOR DRAFT / NOT STORAGE OWNER ISSUED / NOT JOINTLY ACCEPTED / NOT FROZEN**
- Predecessor Storage v3.2.7 current manifest Blob: `684908d0f1bc6def5be565dba76f4d2037545f71`.
- Normative Storage v3.2.3 body: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- COC companion §§15–17: `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- Provenance: P coordinator Storage-role simulation, not independent Storage Owner issuance.

## 1. Purpose / 目的

v3.2.8 is required because the current v3.2.7 manifest still pins the older H mapping Blob `1cbe...`, while C Phase 3.8.17 accepts canonical H mapping Blob `579dd...`. The new successor must bind one exact mapping, test source, CI run and current I/D reviews. It must not rewrite v3.2.7 or Storage v3.2.3.

## 2. Exact candidate source set / 精确候选源集合

| Owner | Artifact | Exact Blob / run | Binding |
|---|---|---|---|
| Storage | Normative v3.2.3 technical body | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | S0a–S4, recovery batch/manifest, JF-10, same-GID and visibility boundary |
| Storage | COC companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest, digest chain, union manifest |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Distinct Batch then Manifest |
| Storage | R1/R2 round/release addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound, owner-local release |
| Storage | Serialization ADR | `bb544ba2f346bdc130d524bd5c7310d86f367988` | L1 Option A selected; L4 physical engine/deployment OPEN |
| H | Unified schema 1.2.14 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Exact artifact revision 1.2.14 / wire 1.3.0 |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Owner membership proof carrier |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Recovery cutoff carrier |
| H | Canonical authority-join mapping | `579dd2a91edf47b86e744e897ba6668b839944bd` | C-accepted current mapping; supersedes duplicate `1cbe...` |
| H | Validator core / tests / workflow | `eab961a08d41e871f38543b18ee60cf024977414` / `70a3796446553464e71999f916b76bc22e47da11` / `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Current validator/test/workflow |
| H | Exact current CI | Run `44068869146`, commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8` | SUCCESS, 27/27; callback orchestration with test doubles |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C object |
| C | Sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C signing/key-status sequence namespace |
| C | Phase 3.8.17 final mapping review | `1dbbc16f937d075a90ddb7416c01177e6dc28a86` | Accepts canonical mapping `579dd...` and callbacks as L1/L2 candidate |
| I | P0 allowlist successor | `44986f5f864bcdc1a79d34978273644d381a68c0` | I-owned P0 candidate |
| I | Current mapping review (refresh required) | `34b29f405d4e8ceb1a039666bfe84518f62355f8` | Pins old H mapping `1cbe...`; P simulated refresh `issue-20-i-phase-3.8.14-review-canonical-h-mapping-v0.1.0.md` |
| D | RecoveryJoin crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D-owned proof P0 mapping |
| D | Current mapping review (refresh required) | `40fee15d7e42d68da231ea161896f85df2921669` | Pins old H mapping `1cbe...`; P simulated refresh `issue-20-d-phase-3.8.10-review-canonical-h-mapping-v0.1.0.md` |

## 3. Authority separation / 权威隔离

- C owns Provider Outcome truth and C immutable object/P0.
- I owns authorization, revocation, trust/key status, I P0 and I-local gate release.
- D owns ForgetOperation, FenceGeneration, lineage, barrier and D-local gate release.
- H owns BMCP schema/mapping/validator orchestration, not the truth of C/I/D/Storage ledgers.
- Storage owns COC persistence, same-GID recovery, Storage visibility and pointer/receipt/outcome/outbox atomicity.
- A integrates and gates; it cannot replace Owner evidence.

The H callback seams are test-only orchestration interfaces. Missing authority/evidence returns UNKNOWN; COC does not substitute for I, D or Storage.

## 4. Required successor actions / 后继行动

1. H marks mapping Blob `1cbe...` historical and `579dd...` canonical; retain immutable history.
2. I refreshes its exact review to `579dd...` while retaining I's own P0 and trust boundaries.
3. D refreshes its exact review to `579dd...` while retaining D's own fence/lineage authority.
4. Storage Owner publishes actual v3.2.8 on its branch with the exact source set above and a corrected review matrix.
5. A publishes a fresh review against the actual v3.2.8 manifest Blob; the old Phase 1.F review of manifest `4435...` is historical only.
6. Keep L3, production and physical Storage gates open until unmocked end-to-end and deployed evidence exists.

## 5. Evidence ceiling and gates / 证据上限与 Gate

H CI run `44068869146`: 27/27 PASS; the orchestration tests mock schema/semantic/digest primitives and do not authenticate real owner proofs or execute production callbacks. C candidate CI `44059935858`: 19 PASS. No production C/I profile registration, provider same-key lookup, live C egress linearization, I/D ledger completeness, COC quorum, Storage same-GID deployment, physical engine, HA/restore or distributed fault-injection campaign is proven.

- L1 logical serialization Option A: selected by ADR `bb544...`.
- L4 physical engine/runtime/deployment: OPEN.
- JF-10 P0 / R1 / R2: OPEN.
- Gate B: BLOCKED; Gate C: DEFERRED / NOT RUN.
- Multi-PolicyDomain atomicity: BLOCKED.
- Global Forget completion, physical erasure, Full Applied and production activation: NOT AUTHORIZED.

**Draft disposition: BOUND FOR JOINT REVIEW ONLY; NOT JOINTLY ACCEPTED / NOT FROZEN.**
