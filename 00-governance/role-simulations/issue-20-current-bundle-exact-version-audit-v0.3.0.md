# Issue #20 — Current H 1.2.14 / C 1.0.1 Multi-Owner Bundle Audit v0.3.0
# Issue #20 — 当前 H 1.2.14 / C 1.0.1 多 Owner Bundle 审计 v0.3.0

- Date: 2026-11-17
- Status: **P COORDINATOR AUDIT / ROLE SIMULATION / NOT OWNER ACCEPTANCE**
- Exact scope: H Unified 1.2.14 × CSubmitOutcome 1.0.1 × RecoveryJoin 1.0.2, with I/D/Storage callback authority joins.

## 1. Current conclusion / 当前结论

The current L1/L2 design is coherent, but the shared review bundle is still inconsistent. The defect has moved beyond the earlier 1.2.13/1.2.14 mismatch: **two H mapping artifacts now represent the same conceptual 1.2.14 authority-join mapping but pin different test/CI revisions.**

- Canonical current H mapping candidate: `08-bmcp-protocol/phase-3.8.10-h-c-provider-outcome-unified-1.2.14-exact-mapping.md`, Blob `579dd2a91edf47b86e744e897ba6668b839944bd`.
- Duplicate predecessor mapping candidate: `08-bmcp-protocol/phase-3.8.10-h-unified-1.2.14-c-submit-outcome-1.0.1-authority-join-mapping.md`, Blob `1cbe74eba69325510d6b1019d971661f965eabf8`.
- Their C object/wire semantics and validator core are aligned, but they differ in exact test Blob and CI evidence:
  - canonical: test Blob `70a3796446553464e71999f916b76bc22e47da11`, run `44068869146`, 27/27;
  - predecessor: test Blob `53774aca0224fd9a727dfa625ba142825f1754b0`, run `44068247661`, 25/25.
- C Phase 3.8.17 Blob `1dbbc16f937d075a90ddb7416c01177e6dc28a86` accepts the canonical `579dd...` mapping.
- I Phase 3.8.13 Blob `34b29f405d4e8ceb1a039666bfe84518f62355f8`, D Phase 3.8.9 Blob `40fee15d7e42d68da231ea161896f85df2921669`, and Storage v3.2.7 Blob `684908d0f1bc6def5be565dba76f4d2037545f71` still bind `1cbe...`.
- A Phase 1.F Blob `85cd97bb66461440c7c08c4397e6cd496217b6fd` binds an earlier Storage v3.2.7 manifest Blob `4435fc...`, test Blob `53774...` and 25-test CI, not the current Storage manifest Blob `684908...` and 27-test CI.

**Disposition: CURRENT L1/L2 C/H DESIGN ACCEPTED AS A CANDIDATE; I/D/Storage/A EXACT REVIEW SET NOT YET COHERENT; DO NOT FREEZE.**

## 2. Exact current artifacts / 当前精确工件

| Owner | Artifact | Blob | Review status |
|---|---|---|---|
| C | Phase 3.8.17 final review of H mapping/callbacks | `1dbbc16f937d075a90ddb7416c01177e6dc28a86` | Accepts H mapping `579dd...` |
| C | Phase 3.8.17 current validator/CI review | `36a50e6285bef512790583841e77349190076564` | Binds current core/test/CI; its mapping pin `c196...` is superseded by final review above |
| H | Unified schema 1.2.14 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current |
| H | C/H mapping candidate (canonical) | `579dd2a91edf47b86e744e897ba6668b839944bd` | Current C-accepted candidate |
| H | Duplicate mapping document | `1cbe74eba69325510d6b1019d971661f965eabf8` | Historical/predecessor; test/CI pins are older |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Current candidate |
| H | Validator tests | `70a3796446553464e71999f916b76bc22e47da11` | Current candidate |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Current workflow |
| H | Current CI | run `44068869146`, commit `e0d89f1b6dac3bdcf1f0ab4e3f062dd7bc53fdf8` | SUCCESS, 27/27 |
| I | Phase 3.8.13 mapping review | `34b29f405d4e8ceb1a039666bfe84518f62355f8` | Still pins H mapping `1cbe...`; refresh required |
| D | Phase 3.8.9 mapping review | `40fee15d7e42d68da231ea161896f85df2921669` | Still pins H mapping `1cbe...`; refresh required |
| Storage | v3.2.7 manifest | `684908d0f1bc6def5be565dba76f4d2037545f71` | Still pins mapping `1cbe...`; refresh required |
| A | Phase 1.F integration review | `85cd97bb66461440c7c08c4397e6cd496217b6fd` | Pins prior manifest `4435fc...`; refresh required |

Other fixed schema pins:
- CSubmitOutcome 1.0.1: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`.
- C sequence namespace amendment: `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`.
- RecoveryJoin 1.0.2: `4b664e3bce465499bcdfd93796349a4ba7074002`.
- RecoveryCutoff 1.0.5: `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`.
- I current P0 successor: `44986f5f864bcdc1a79d34978273644d381a68c0`.
- D current RecoveryJoin crosswalk: `c4adf827dd62d44c43b8e871dec4835581508adf`.
- Storage normative v3.2.3 body: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- Storage serialization ADR: `bb544ba2f346bdc130d524bd5c7310d86f367988` (L1 Option A selected; L4 physical deployment OPEN).

## 3. Canonical mapping decision / Canonical Mapping 决议

Use H mapping Blob `579dd...` as the single current mapping candidate because it is the mapping accepted by C Phase 3.8.17 and it pins the current H test Blob and 27-test CI. Keep `1cbe...` as immutable historical evidence; do not delete or rewrite it. H should explicitly mark the duplicate path as superseded and point to the canonical mapping Blob.

I and D must refresh their exact reviews from `1cbe...` to `579dd...`. Storage must issue v3.2.8 successor manifest from v3.2.7, binding `579dd...`, the current test Blob and run `44068869146`, and refreshed I/D reviews. A must review the actual current v3.2.8 manifest Blob, not the older manifest version referenced in Phase 1.F.

## 4. Evidence ceiling / 证据上限

H run `44068869146` is a real 27/27 success on exact validator/test/schema source. The orchestration tests use test doubles for underlying owner proof primitives and mock schema/semantic/digest functions in callback-orchestration cases. They prove separate I/D/Storage callback slots and fail-closed UNKNOWN when missing; they do **not** prove a complete unmocked H envelope + C object path or real owner-ledger/trust/Storage evidence.

C run `44059935858` passed 19 candidate tests. Neither run proves production C/I profile registration, production key custody, provider issuer truth, authoritative same-key lookup, live C egress linearization, I/D owner-ledger completeness, COC quorum, Storage same-GID recovery or L4 deployment.

## 5. Gate disposition / Gate 处置

- C/H L1/L2 mapping and callback seam design: **COHERENT CANDIDATE**.
- I/D exact acceptance of canonical mapping `579dd...`: **REVIEW REFRESH REQUIRED**.
- Storage exact bundle v3.2.8: **NOT YET PUBLISHED**.
- A review of current manifest: **REQUIRED**.
- H full unmocked validation and per-field mutation suite: **OPEN**.
- C/I production profiles/trust, C adapter and provider idempotency: **OPEN**.
- D/I live owner proof/currentness/release: **OPEN**.
- COC quorum and Storage L4 runtime/deployment/fault injection: **OPEN/BLOCKED**.
- JF-10 P0, Gate B/C, Multi-PolicyDomain, Global Forget, physical erasure and production activation: **OPEN / NOT AUTHORIZED**.

No joint freeze, Full Applied, Global Forget completion or universal exactly-once claim.
