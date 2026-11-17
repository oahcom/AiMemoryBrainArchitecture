# Issue #20 — Outer Envelope Authentication / 60-Test / Owner Currentness Audit v0.6.0
# Issue #20 — 外层 Envelope Authentication / 60 项测试 / Owner 当前性审计 v0.6.0

- Status: **P COORDINATOR CROSS-OWNER AUDIT / ROLE SIMULATION ONLY**
- Snapshot: 2026-11-17
- Repository: `oahcom/AiMemoryBrainArchitecture`
- P HEAD before this audit: `d89b0b66ef43de25799b53855a01bd6b8e5088db`
- Current Owner branch heads:
  - A: `9bdf938b980413f592a4db9fe94f4bf2c299fb01`
  - C: `2e8414f361b0b5d7de959be8a971aadc9e62d6a9`
  - D: `76fcc92225666a11893b7241825261319edb621e`
  - H: `8e24342048d29ef29195b153b8b9ec53ba7c75d9`
  - I: `9dd97ea81669ea832ca72a84004541611cf4782b`
  - Storage: `431138e7c7af8bee716f3d8dcbc20114c046bd36`
- Decision: **H 60-test authenticated-ingress reference gate is a valid L1/L2 orchestration advance, but it is not cryptographic envelope authentication. C signer decision documents are internally unreconciled; I has accepted the two-object separation only as a candidate; Storage v3.2.11 manifest lineage is stale/ambiguous; A exact review of the current 60-test manifest is absent. Prepare v3.3.1 as P draft; do not freeze.**

## 1. Executive conclusion / 执行结论

H has moved beyond the earlier 42-test inner Provider Outcome path. Phase 3.8.19 adds a distinct authenticated-ingress wrapper and 18 outer-envelope orchestration tests. Exact H Provider Outcome run `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527`, completed SUCCESS with **60 tests / 0 failures**. The current H branch still contains the exact validator/test/fixture/closure Blobs pinned by that run; later H commits add review/mapping documents.

This is an important interface and ordering improvement, not production cryptographic verification. The 18 envelope tests inject deterministic verifier callbacks. The reference wrapper does not itself implement the outer-envelope P0 extractor, digest recomputation, signature verification, production trust/key status, protected transport/channel binding or durable replay store. H's own closure explicitly says these are NOT PROVEN.

C now has a corrected outer-envelope signer/P0 decision candidate and H has published an exact JSON-Pointer mapping. I has reviewed the corrected two-signed-object separation as a candidate. However, C's later 60-test review still says the signer/attestation model remains OPEN and recommends a distinct H-gateway attestation while the earlier corrected C decision candidate assigns the outer origin signature to the C provider adapter. This is an unresolved C document/decision reconciliation, not something P can decide on C's behalf.

Storage has published a 60-test v3.2.11 manifest, but:
- a different v3.2.11 manifest already exists for the 64-field/42-test bundle;
- v3.3.0 is another 42-test consolidation artifact;
- the 60-test v3.2.11 manifest pins the older C/I review artifacts and does not bind the corrected C decision, H JSON-Pointer mapping or I corrected P0 review;
- A Phase 1.L reviews the other v3.2.11 manifest Blob `d7a99...`, not the current 60-test manifest Blob `54a4...`.

**Disposition: ACCEPT H reference gate as L1/L2 orchestration evidence; KEEP outer-envelope cryptographic acceptance, C signer decision, I registration, Storage durable-ingress semantics, exact bundle and A review OPEN. Prepare Storage v3.3.1 successor draft; NOT FROZEN / NOT PRODUCTION-AUTHORIZED.**

## 2. Exact H 60-test source and evidence / H 60 项精确源与证据

| Artifact | Exact identity | Status / ceiling |
|---|---|---|
| H Unified schema 1.2.14 / wire 1.3.0 | Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Structural schema |
| CSubmitOutcome 1.0.1 | Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned immutable provider semantic object |
| H outer-auth validator | Blob `5c5079765f468eaf40690c0c7cbd6b03275a1ff8` | Reference orchestration only |
| H Provider Outcome validator | Blob `b8cd692d261df7a31a0f65c3e003693e305f73a2` | Inner H/C schema/semantic/digest path |
| H outer-auth test source | Blob `ddf34e9c30edfc378a9482a30837ce04c4abcf97` | 18 callback/order/replay methods |
| H Provider Outcome tests | Blob `da1454ed985c84160c4cb6a0462df9d1225fab7f` | 36 H/C methods |
| H positive fixture | Blob `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic; callbacks are test doubles |
| H closure | Phase 3.8.19 Blob `860c896a388597a4378eda5aa323f276390acf34` | Exact 60-test source/run binding |
| H exact CI | Run `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527` | **60 tests, SUCCESS** |
| H RecoveryCutoff CI | Run `44074187153`, commit `10434b4df4b7c999206cbc296ffdbca4755fe3d2` | SUCCESS; separate recovery suite |

The 60 methods comprise 36 H/C Provider Outcome methods, 18 outer-envelope auth methods and six Python/Node candidate C crypto interoperability methods.

The 18 outer-auth tests cover strict raw parse/duplicate-key rejection, protected-context claim comparisons, fail-closed callback tri-state, replay NEW/SAME_DIGEST_REPLAY/CONFLICT/UNKNOWN, no replay reservation before auth success, and no downstream domain validation before auth. They do NOT calculate or verify a real outer-envelope signature.

### Code-level evidence boundary / 代码级证据边界

The exact `envelope_auth_validator.py` source calls injected callbacks for envelope integrity, key status, channel binding, identity binding and replay. Those callbacks return True/False/None in tests. The Python `ProtectedTransportContext` dataclass documents trusted provenance but cannot enforce that provenance; production construction must be restricted to the authenticated transport adapter. C's exact review also notes that replay reservation currently precedes domain validation and durable ingress commit; production must define reservation lifecycle, crash recovery, release/commit, retention and atomic publication of prior result.

Therefore:
- **PROVEN:** reference ordering, strict parsing, claim/context comparison, tri-state failure handling, replay callback ordering and wrapper-to-domain-validator gating.
- **NOT PROVEN:** outer P0 bytes, digest recomputation, signature cryptography, production profile, I trust registry, key lifecycle/revocation/history, transport principal, channel binding, durable replay ledger, crash recovery or Storage atomic durable acceptance.

## 3. C signer decision reconciliation / C Signer 决策协调

Exact artifacts:
- C corrected signer/P0 decision candidate: Blob `310e7e0073d3c32f594bc151f10c249c828ce30f`.
- H exact JSON-Pointer mapping and P0 correction: Blob `4ba7e1699215d02224f805a15484b1da2e40c03f`.
- I corrected C P0 review: Blob `63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00`.
- C exact H 60-test review: Blob `8fd6052cabf58a78962cc2e776398b2a40604bcd`.

C Phase 3.8.22 decision candidate says the C provider adapter signs both (a) immutable CSubmitOutcome under C object P0 and (b) the outer C_PROVIDER_OUTCOME_RECORDED envelope under a distinct C envelope P0/profile. An H gateway receipt may be additive but cannot replace the C origin signature. It explicitly prohibits reuse of the C object P0/profile for the envelope.

The corrected candidate includes `integrity_proof_ref` and `channel_binding_proof_ref` in the envelope P0. H Phase 3.8.20 converts the candidate into a JSON-Pointer inventory and binds the corrected C Blob. I Phase 3.8.19 accepts the corrected two-object separation and P0 field correction as candidates, but does NOT approve RFC8785/SHA-256/Ed25519 for production, profile registration, keys, custody, anti-rollback or deployment.

**Conflict requiring C reconciliation:** C's later Phase 3.8.22 exact review of H's 60-test gate says signer/attestation remains OPEN and its design recommendation favors a distinct H-gateway attestation plus separately authenticated original C transport, rather than explicitly reaffirming the earlier C-origin envelope-signature decision. These statements may be intended as different stages (architecture candidate vs H gate review), but they are not explicitly reconciled. P will not infer a final C Owner decision. C must publish a short supersession/addendum that either:
1. reaffirms the corrected C-origin envelope-signature candidate and updates the 60-test review to match; or
2. explicitly supersedes it with a distinct H gateway receipt/attestation model and states how C origin attribution is independently authenticated.

Until then, signer model = **OPEN / NOT CRYPTO-FROZEN**.

## 4. H/I exact mapping and trust boundary / H/I 精确 Mapping 与 Trust 边界

H Phase 3.8.20 mapping Blob `4ba7e1699215d02224f805a15484b1da2e40c03f` binds corrected C decision Blob `310e7e...`, H schema 1.2.14 and C object schema 1.0.1. It includes the two proof-reference fields that were missing in the original C P0 inventory. The document itself says implementation, I profile registration and executable full-path tests remain OPEN.

I Phase 3.8.19 Blob `63d7bfc...` accepts the corrected two-signed-object architecture and proof-reference inventory only as candidates. I's approval boundary remains: profile identifier/purpose/audience/signer authority, algorithm/parameters, trusted C issuer/workload principal, key custody/HSM/KMS, rotation/destruction, key status/history, revocation/compromise ordering, anti-rollback, cross-profile replay, cross-language vectors and incident response.

H current 60-test code has NOT implemented this exact P0 mapping. The 60-test suite's integrity/key/channel/identity callbacks remain test doubles. H must mechanically derive/verify the P0 from the schema and mapping, not assume a documented inventory equals executable implementation.

## 5. Storage manifest lineage and A exactness / Storage Manifest 谱系与 A 精确性

Current Storage branch HEAD: `431138e7c7af8bee716f3d8dcbc20114c046bd36`.

The latest Storage 60-test manifest is Phase 3.6.21, v3.2.11, Blob `54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57`. It binds H 60-test closure/run, but its review matrix still pins:
- C Phase 3.8.21 review Blob `3668c394...` (before corrected signer/P0 candidate and C 60-test review);
- I Phase 3.8.17 review Blob `893f240...` (before I corrected C P0 review);
- H mapping `1cbe74...` (inner C/D/I authority join, not new outer P0 mapping `4ba7e...`);
- D Phase 3.8.13 review Blob `152627...` (upstream-interface boundary only).

Additional version-lineage ambiguity:
- Storage v3.2.11 Phase 3.6.22 Blob `d7a99baa...` binds the 64-field C-P0 / nullable COC 42-test bundle.
- Storage v3.2.11 Phase 3.6.21 Blob `54a4f0...` binds the 60-test outer-auth reference gate.
- Storage v3.3.0 Blob `c8407c9...` is a separate 42-test consolidation manifest.
- A Phase 1.L Blob `191f875...` reviews the v3.2.11 manifest Blob `d7a99...`, **not** the 60-test v3.2.11 manifest Blob `54a4...`.
- A Phase 3.8.19 Blob `e12cd7...` reviews the pre-60-test outer-auth gap and does not review the corrected C/H/I P0 candidate set.

This is a version/manifest identity ambiguity, not merely a stale test count. P proposes a uniquely named Storage v3.3.1 successor, binding the exact H/C/I artifacts above and refreshed C/D/H/I/Storage review pins. A must then review that exact v3.3.1 Blob.

## 6. Owner matrix and current status / Owner 矩阵与当前状态

| Owner | Current exact artifact | Current result | Required next action |
|---|---|---|---|
| C | Corrected decision candidate `310e7e...`; H 60-test review `8fd605...` | Signer decision candidate vs later review not reconciled | Publish C supersession/addendum |
| H | 60-test closure `860c896...`; P0 mapping `4ba7e...` | Reference gate pass; P0/signature verifier not implemented | Implement exact extractor/crypto vectors and protected transport adapter |
| I | Corrected P0 review `63d7bfc...` | Accepts separation candidate; production crypto/trust NOT approved | Formal I crypto-governance approval and registration |
| D | Outer-auth upstream review `152627...`; current D HEAD `76fcc9...` | Interface boundary only; D proof/currentness still separate | Confirm whether a fresh D exact review is needed for successor; preserve D owner-local proof boundary |
| Storage | 60-test manifest `54a4f0...` | Exact H CI bound, but owner review pins and manifest identity stale/ambiguous | Publish unique v3.3.1 exact successor and define replay/durable-ingress atomicity |
| A | Phase 1.L `191f875...` reviews Blob `d7a99...` only | No A review of Blob `54a4...` or v3.3.1 | Fresh exact A integration review |

## 7. Gate disposition / Gate 处置

- H reference authenticated-ingress orchestration: **PASS, L1/L2 ONLY**.
- C origin signer and outer P0: **CANDIDATE / RECONCILIATION REQUIRED**.
- I profile suitability/registration/key custody/trust: **OPEN / NOT APPROVED**.
- H production P0/digest/signature verification: **NOT IMPLEMENTED / NOT VERIFIED**.
- Protected transport principal/channel binding: **TEST DOUBLES ONLY**.
- Replay reservation/durable ingress atomicity and crash recovery: **OPEN**.
- Storage v3.2.11 common exact bundle: **AMBIGUOUS / STALE TO C/I/H CORRECTIONS**.
- A exact review of latest Storage manifest: **PENDING**.
- Production I/D/Storage owner proof adapters: **NOT VERIFIED**.
- JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, Full Applied and production activation: **OPEN / BLOCKED / NOT AUTHORIZED**.

## 8. Next sequence / 后续顺序

1. C resolves its signer/attestation documents and publishes one exact current decision.
2. H updates its mapping if C supersedes the current decision; then implements P0 extraction/digest/signature verification with independent vectors.
3. I decides profile/algorithm/trust registration and key lifecycle, with no implicit profile reuse.
4. Storage publishes v3.3.1 with a unique version and atomic replay-reservation/durable-ingress semantics; bind exact Owner reviews.
5. A reviews the exact Storage v3.3.1 manifest.
6. Re-run H CI on the exact source commit and add real transport/trust/replay fault tests; preserve all existing non-claims.

## 9. Provenance / 来源

This is a Session P coordinator audit. It is not an independent C/D/H/I/Storage/A signature, does not authorize Owner branch writes, does not register cryptographic profiles, and does not authorize merge, deployment, provider egress or production activation.

本文件是 Session P 协调者审计，不代替 C/D/H/I/Storage/A 签署，不授权修改 Owner 分支，不注册密码学 Profile，也不授权 Merge、部署、Provider Egress 或生产激活。
