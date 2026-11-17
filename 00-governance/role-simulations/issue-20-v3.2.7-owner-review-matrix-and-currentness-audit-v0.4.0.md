# Issue #20 — Storage v3.2.7 Currentness and Owner Review Matrix Audit v0.4.0
# Issue #20 — Storage v3.2.7 当前性与 Owner 审查矩阵审计 v0.4.0

- Date: 2026-11-17
- Status: **P COORDINATOR AUDIT / ROLE-SIMULATED / NOT OWNER ACCEPTANCE**
- Review target: Storage branch `session-storage-consistency-forget-atomicity-2026-11-16`, current manifest Blob `c4ce39e25bf57d97c28db4e2133087d4eca1fbb8`.
- Current H/C composition: Unified 1.2.14 × CSubmitOutcome 1.0.1 × RecoveryJoin 1.0.2 × RecoveryCutoff 1.0.5.

## 1. Executive decision / 总体结论

The core exact bundle is now materially stronger and the prior 25/27-test evidence gap is closed at the local schema/semantic/digest layer. C, I and D have each published current delegated reviews against H integrated authority-join mapping Blob `1cbe74eba69325510d6b1019d971661f965eabf8`; H has published its full-path fixture closure; Storage has refreshed v3.2.7 to bind the 32-test full-path evidence.

However, the current Storage v3.2.7 manifest Blob `c4ce39...` is **not yet a reliable joint-review register**:
1. Its §4 Owner matrix still cites old C Phase 3.8.15, I Phase 3.8.12 and D Phase 3.8.8 decisions, despite newer exact reviews existing.
2. Its §4 H row still describes the earlier callback-seam run 44068869146, not the current full-path closure.
3. Its §4 A row says no A review, which is true for the current manifest Blob; the available A Phase 1.F review pins predecessor manifest Blob `4435fc...` and the older 25-test suite, so it cannot be carried forward.
4. Its §3 repeats the exact same full positive fixture row twice.
5. The C/I/D review notes cite run `44069777296` (32 tests, commit `9eb063...`), while H's current exact-head closure and Storage manifest cite the later run `44069941327` (32 tests, commit `ba2c934...`). Both are SUCCESS and bind the same schema/validator/test/fixture Blobs; use `44069941327` as the canonical bundle run to eliminate avoidable ambiguity.

**Disposition: ACCEPT THE L1/L2 ARCHITECTURE CANDIDATE; RETURN STORAGE v3.2.7 MANIFEST FOR DOCUMENTARY CURRENTNESS REPAIR; DO NOT FREEZE.**

## 2. Exact current owner artifacts / 当前 Owner 精确工件

| Owner | Current review / artifact | Exact Blob | Exact scope and status |
|---|---|---|---|
| C | Phase 3.8.18 full-path fixture review | `4be9c1cd8f116086bab58340f07e38ddfc223e21` | Accepts H mapping `1cbe74...`, C schema `a631bc...`, H validator `eab961...`, test `dccf8...`, fixture `c80247...`, H closure `f9c8d...`; delegated C review, not independent human signature |
| I | Phase 3.8.14 full-path terminal callback review | `7c65650a37c8c0f270451fb0419e93259fc38151` | Accepts H mapping `1cbe74...`, I P0 `44986f...`, H validator/test/fixture/closure; callback test double only; trust/L3/production OPEN |
| D | Phase 3.8.10 full-path Forget clearance review | `ccdae9b45affb23c6741b5cceb27004b35a8e03e` | Accepts H mapping `1cbe74...`, D crosswalk `c4adf8...`, H validator/test/fixture/closure; callback test double only; lineage/L3/release OPEN |
| H | Phase 3.8.14 full-path exact-head closure | `5f487321b273ede41a7c23c3f94b6c0625968439` | H schema `09fcd1...`, C schema `a631bc...`, mapping `1cbe74...`, validator `eab961...`, test `dccf8...`, fixture `c80247...`; run 44069941327 |
| H | Full local validation evidence note | `b8bbac49ac99573911fe89f30f12325bbaa67b08` | Full local H envelope + C object schema/semantic/digest path; TEST-ONLY authority callback ceiling |
| Storage | v3.2.7 current manifest | `c4ce39e25bf57d97c28db4e2133087d4eca1fbb8` | Candidate bundle; matrix requires refresh |
| A | Phase 1.F review of predecessor manifest | `85cd97bb66461440c7c08c4397e6cd496217b6fd` | Pins Storage manifest `4435fc...`, test `53774a...`, run 44068247661 / 25 tests; **not a review of current manifest `c4ce39...`** |

All C/I/D/H review artifacts above are delegated role reviews in this coordinated workflow. They are technically meaningful exact-scope reviews, but they are not independent human Owner signatures or formal governance approvals.

## 3. CI evidence readback / CI 证据读回

Canonical current H run:
- Run: `44069941327`
- Tested commit: `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`
- Job: `133993324484` (`provider-outcome`)
- Conclusion: SUCCESS
- Exact log: `Ran 32 tests in 1.119s`; `OK`
- Test composition: 6 Python/Node C crypto interoperability methods + 26 H validator methods.

Full-path tests 21–25:
- Test 21: actual H/C schemas + C object dereference/equality + semantic predicates + recomputed C-P0 digest; VALID only when test authority callbacks return True.
- Test 22: duplicated wire/object mismatch → INVALID.
- Test 23: mutated C payload digest → INVALID after recomputation.
- Test 24: missing I/D/Storage verifiers → UNKNOWN.
- Test 25: each I/D/Storage contradiction → INVALID.

The run proves a complete **local** H envelope + immutable C object schema/semantic/digest path. It does not prove production C signature/key-status, issuer truth, I/D/Storage proof authenticity, owner-ledger completeness, live currentness CAS, anti-rollback, provider same-key lookup, production adapter races, COC quorum, same-GID recovery or physical Storage visibility.

Run `44069777296` on commit `9eb063...` is also SUCCESS and uses the same pinned test/validator/schema/fixture Blobs. For one canonical manifest reference, prefer the later run `44069941327` on `ba2c934...`.

## 4. Manifest defects / Manifest 缺陷

### M-01 — Stale Owner matrix (P1)

Storage v3.2.7 §4 still references:
- C Phase 3.8.15 Blob `28d604...`, superseded for current full-path evidence by C Phase 3.8.18 Blob `4be9c1...`;
- I Phase 3.8.12 Blob `fbd44...`, superseded for the current full-path terminal callback boundary by I Phase 3.8.14 Blob `7c6565...`;
- D Phase 3.8.8 Blob `6aca7d...`, superseded for the current full-path clearance callback boundary by D Phase 3.8.10 Blob `ccdae9...`;
- H Phase 3.8.13 callback-seam evidence / run 44068869146, superseded by H Phase 3.8.14 full-path closure Blob `5f4873...` / run 44069941327.

The earlier reviews remain valid historical evidence for their narrower scope; they must not be described as current acceptance of the full-path source set.

### M-02 — A review is bound to a predecessor manifest (P1)

A Phase 1.F Blob `85cd97...` explicitly pins Storage manifest Blob `4435fc...`, test Blob `53774a...` and run 44068247661. Current Storage manifest is `c4ce39...` and current H full-path test Blob is `dccf8...`. A must issue a new exact review after Storage publishes a corrected successor manifest Blob.

### M-03 — Duplicate fixture row (P2)

Storage §3 lists the same fixture path and Blob `c80247...` twice. Remove one duplicate row. This is a documentation integrity defect; it does not alter schema/test semantics, but it reduces manifest clarity and weakens exact-set reviewability.

### M-04 — Canonical CI run reference (P2)

C/I/D reviews cite successful run 44069777296; H closure and Storage current manifest cite later successful run 44069941327. Both are valid against identical source Blobs, but the manifest should designate 44069941327 as canonical and optionally list 44069777296 as an earlier corroborating run.

## 5. Required next actions / 后续动作

1. Storage publishes a v3.2.8 successor manifest (or explicitly versioned correction) on the Storage branch, preserving v3.2.3 normative body and v3.2.7 as historical. Correct the §4 matrix, remove duplicate fixture row, and designate run 44069941327 canonical.
2. C confirms Phase 3.8.18 remains the current C acceptance for the exact v3.2.8 pins; if any Blob changes, C refreshes.
3. I confirms Phase 3.8.14 remains current for the exact I callback boundary and P0 source; trust/L3 remains open.
4. D confirms Phase 3.8.10 remains current for the exact D callback boundary and proof source; lineage/L3 remains open.
5. H confirms the exact full-path closure and source set; no schema/validator/test changes may be silently absorbed.
6. A performs a new exact integration review of the actual Storage-issued v3.2.8 manifest Blob.
7. Keep JF-10 P0, R1/R2, Gate B/C, production trust, provider adapter, COC quorum, Storage L4 deployment, Multi-PolicyDomain, Global Forget and physical erasure gates open.

## 6. A-role simulated decision / A 角色模拟裁决

**ACCEPT THE L1/L2 ARCHITECTURE CANDIDATE; RETURN THE CURRENT STORAGE MANIFEST FOR EXACT OWNER-MATRIX/CURRENTNESS REPAIR; DO NOT FREEZE.**

The C/H/I/D technical composition is coherent at the local schema/semantic/digest and callback-boundary level. Storage v3.2.7 is a valid candidate exact bundle, but its current Owner matrix is stale and contains a duplicate fixture row. A's existing review is bound to a predecessor manifest, so there is no current A acceptance of Blob `c4ce39...`.

This is a P coordinator A-role simulation, not an independent A Owner decision, not a formal PGA decision and not a release/merge authorization.

## 7. Gate state / Gate 状态

- L1/L2 schema + object + local digest path: **PASS (bounded candidate evidence)**.
- I/D/Storage callback seam design: **ACCEPTED AS L1/L2 CANDIDATE**.
- C/I/D/H exact source reviews: **CURRENT DELEGATED REVIEWS EXIST**.
- Storage v3.2.7 Owner matrix: **STALE / RETURN FOR CORRECTION**.
- A review of current manifest Blob `c4ce39...`: **NOT YET ISSUED**.
- Production authority adapters/trust roots/key lifecycle: **OPEN**.
- C provider issuer truth/same-key lookup/adapter races: **OPEN**.
- D lineage pagination/late discovery/release CAS: **OPEN**.
- I ledger completeness/revocation/currentness CAS/anti-rollback: **OPEN**.
- COC quorum/same-GID recovery/Storage L4 deployment: **OPEN / NOT VERIFIED**.
- JF-10 P0, R1/R2, Gate B/C, Multi-PolicyDomain, Global Forget, physical erasure and production activation: **OPEN / BLOCKED / NOT AUTHORIZED**.

No joint freeze, production activation, Full Applied or Global Forget completion claim.
