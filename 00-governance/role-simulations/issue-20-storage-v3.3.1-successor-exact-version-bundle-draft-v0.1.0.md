# P Draft — Storage v3.3.1 Successor Exact-Version Bundle
# P 草案 — Storage v3.3.1 后继精确版本 Bundle

- Status: **P COORDINATOR DRAFT / NOT STORAGE OWNER ISSUED / NOT JOINTLY ACCEPTED / NOT FROZEN**
- Predecessor: Storage v3.2.11 Phase 3.6.21 Blob `54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57`.
- Other conflicting predecessor: Storage v3.2.11 Phase 3.6.22 Blob `d7a99baa5b06ac8e67932f47946bab3775f8ecb3`.
- Earlier consolidated manifest: Storage v3.3.0 Blob `c8407c9f10049d65426a3598ad20b6aa70f83c32`.
- Normative Storage v3.2.3 body: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- COC companion §§14–17: `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- Provenance: P simulated Storage role only.

## 1. Purpose / 目的

This proposed v3.3.1 is a uniquely named successor intended to remove the duplicate v3.2.11 manifest identity and bind the latest H 60-test reference ingress gate, corrected C envelope P0 candidate, H JSON-Pointer mapping, I corrected trust-boundary review, C reconciliation requirement and fresh A review.

It does not claim production cryptographic acceptance. The H 60-test suite remains reference orchestration evidence only.

## 2. Exact source bundle / 精确源 Bundle

| Authority | Artifact | Exact Blob / Run | Status |
|---|---|---|---|
| Storage | Normative S0a–S4 body v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Architecture candidate; physical implementation open |
| COC | Companion §§14–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest and union semantics |
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current schema |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Membership proof carrier |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Cutoff structure |
| H | C/D/I/Storage authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Inner C object/owner joins; separate from outer auth |
| H | Outer-auth reference validator | `5c5079765f468eaf40690c0c7cbd6b03275a1ff8` | Reference callback orchestration only |
| H | Inner Provider Outcome validator | `b8cd692d261df7a31a0f65c3e003693e305f73a2` | C object/schema/semantic/digest path |
| H | Outer-auth test source | `ddf34e9c30edfc378a9482a30837ce04c4abcf97` | 18 reference methods |
| H | Provider Outcome test source | `da1454ed985c84160c4cb6a0462df9d1225fab7f` | 36 H/C methods |
| H | Positive fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic; authority callbacks are doubles |
| H | Outer-auth closure | `860c896a388597a4378eda5aa323f276390acf34` | Exact closure |
| H | Provider Outcome CI | Run `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527` | **60 tests, SUCCESS** |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C object |
| C | C sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C-owned durable sequence namespace |
| C | Corrected outer-envelope signer/P0 decision candidate | `310e7e0073d3c32f594bc151f10c249c828ce30f` | C origin signer candidate; C reconciliation with later review required |
| C | H 60-test review | `8fd6052cabf58a78962cc2e776398b2a40604bcd` | Accepts reference gate; signer model still open |
| H | Corrected outer P0 JSON-Pointer mapping | `4ba7e1699215d02224f805a15484b1da2e40c03f` | Candidate mapping; implementation open |
| H | Review of C signer/P0 candidate | `2a3a995396ee7a56d8fbbb03ec53b5d1d15e1f82` | Accepts C-origin signer architecture candidate |
| I | Corrected C P0 review | `63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00` | Accepts two-object separation as candidate; no crypto registration |
| I | C signer/trust review | `b6d1ea45825a1c2090abfba42474814f02f073a3` | Historical candidate review; corrected by 3.8.19 |
| D | H outer-auth upstream review | `152627e00b96355e2ff370acd643a51168c4c78c` | Upstream interface only; D proof/currentness remains D-owned |
| Storage | 60-test predecessor manifest | `54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57` | Historical; stale review matrix |
| A | v3.2.11 Phase 1.L review | `191f87505fc9c92f744aa2139b86aa77c45b2c44` | Reviews different manifest Blob `d7a99...`; does not transfer |
| A | Current outer-auth gap review | `e12cd7b5c79e2234178014243fd51f2e7d51272e` | Historical to 60-test/C/H/I corrections |
| A | v3.3.1 exact review | Not issued | Required after Storage Owner publishes exact successor |

## 3. Normative Storage boundary / 规范 Storage 边界

The v3.3.1 successor must not alter Storage v3.2.3 S0a–S4 or COC Batch-before-Manifest ordering. It only binds the exact protocol and owner evidence set.

Durable acceptance requirements must be made explicit:
1. no C-originated message is durably accepted before outer envelope authentication and inner C object verification;
2. replay identity and nonce are scoped to the exact message family, issuer/principal, audience and profile;
3. replay reservation has an explicit PENDING/COMMITTED/ABORTED lifecycle or equivalent;
4. crash between auth, replay reservation, domain validation and durable inbox commit is recoverable without duplicate provider side effects or permanently stuck reservations;
5. same-digest replay returns only a prior durable terminal result; no prior result or unresolved PENDING state => UNKNOWN;
6. conflict is INVALID; unavailable replay authority is UNKNOWN;
7. replay state and durable inbox/acceptance result must have a documented atomicity boundary and retention/compaction rules.

These are required Storage design conditions, not claims that current Storage code implements them.

## 4. Review matrix / 复审矩阵

| Owner | Required exact review | Current status |
|---|---|---|
| C | Reconcile corrected signer decision with later 60-test review; review exact H P0 mapping | OPEN |
| H | Confirm corrected C P0 mapping and implement exact P0/digest/signature/transport checks | Mapping candidate; implementation OPEN |
| I | Formal crypto suite/profile/trust/key lifecycle registration and exact verifier semantics | Candidate review only; NOT APPROVED |
| D | Confirm upstream H auth does not weaken D fence/lineage proof and refresh exact bundle if required | Existing interface review only |
| Storage | Publish this unique successor on Storage branch; define replay/durable-ingress crash semantics | P draft only |
| A | Review exact Storage-issued v3.3.1 Blob and all pins | OPEN |

## 5. Gate disposition / Gate 处置

- H reference ingress gate: **60/60 PASS, L1/L2 orchestration only**.
- Outer C envelope P0/signature: **CANDIDATE; executable verification NOT IMPLEMENTED**.
- C signer model: **OPEN pending C reconciliation**.
- I production crypto/profile/trust/key registration: **NOT APPROVED**.
- Protected transport/channel binding: **test doubles only**.
- Durable replay/ingress atomicity: **OPEN**.
- Storage v3.3.1: **P draft only**.
- A exact review: **PENDING**.
- C/D/I/Storage production verifiers, COC quorum, same-GID recovery, JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, Full Applied and production activation: **OPEN / BLOCKED / NOT AUTHORIZED**.

No freeze, merge, deployment, provider egress or production acceptance is authorized by this draft.
