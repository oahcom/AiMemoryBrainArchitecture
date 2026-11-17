# Phase 3.6.9 — Storage v3.2.3 Currentness & Exact-Review Gate Audit
# Phase 3.6.9 — Storage v3.2.3 当前性与精确复审门审计

- Date: 2026-11-17
- Reviewer perspective: Storage / cross-owner coordination (delegated role simulation)
- Status: **CURRENTNESS AUDIT COMPLETE / v3.2.3 NOT READY FOR JOINT REVIEW FREEZE**
- Target Storage proposal: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.3.md`
- Exact Storage Blob: `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- This audit is a version-binding check, not an Owner acceptance, schema freeze, or implementation result.

## 1. Executive result / 执行结论

Storage v3.2.3 has a coherent S0a–S4 two-record recovery sequence and an explicit union of COC participants plus pre-COC I/D/C owner-local admissions. However, its §21.1 exact bundle is already stale against the live H and C Owner branches. The current document pins H unified schema 1.2.5 and C Provider Outcome source `f538d921...`, while the live branches expose H unified schema 1.2.12 and a newer C source composition that includes owner-local admission/recovery and the transport-owning egress adapter.

**Disposition: do not treat v3.2.3 as a fully bound cross-owner review bundle.** Storage must publish a successor exact-version binding amendment (or a new v3.2.4 proposal) and obtain fresh C/H decisions against the exact same bundle. A must then review the exact successor bundle. Historical approvals of earlier C/H blobs do not transfer.

## 2. Exact live readbacks / 当前精确读回

| Artifact | Exact live Blob | Observation |
|---|---|---|
| Storage v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Current audit target |
| H unified schema 1.2.12 | `a54f66914a819d77f00c6af04e76453ff9f654ee` | Artifact revision 1.2.12; schema description declares wire version 1.3.0 |
| H R1/R2 wire crosswalk | `8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c` | Explicitly binds unified 1.2.12, RecoveryCutoff 1.0.5 and RecoveryJoin 1.0.2 |
| H owner-authority membership verifier adapter contract | `5b462c79082a27b64a03f9c8b6da1d4e93075b89` | Interface only; callback/helper remains TEST-ONLY |
| C provider outcome exact-owner binding decision | `1353572f7d5655e3007b2fb5b3f10066f483e6bb` | Delegated C-role decision; canonical C source composition |
| C owner-local admission/recovery amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` | C gate, admission ledger and recovery release |
| C concrete provider egress gate adapter | `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` | Transport-owning adapter CAS and send/close boundary |
| CSubmitOutcome 1.0.0 schema/conformance contract | `7939c84e950b50f3ec44e4e2fbe5e7f93e544c2e` | Candidate object schema and bounded structural/semantic tests |

The current H CI previously pinned by the H exact review is run `44051851164` on H HEAD `ba99eea9334d77c2a014ed45d9287ef514a4d895`: 288 tests, 266 passed, 22 skipped, 0 failed. The 22 skipped tests are historical 1.2.10 fixtures and are not counted as passes. This run does not prove production owner verifiers, canonical-byte interoperability across independent implementations, quorum evidence, or gate linearization.

## 3. Blocking currentness findings / 阻塞性当前性发现

### V323-CUR-01 — H schema pin drift (BLOCKING)

Storage v3.2.3 §21.1/§21.4 pins H unified schema 1.2.5 Blob `164ec3c436558d5d93032edc51e127d15e03db4`. The live H branch has unified schema 1.2.12 Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`, with wire version 1.3.0 and later owner-specific high-water/membership-proof semantics. H's own crosswalk Blob `8b5b2c...` confirms 1.2.12 is current. Storage must not silently substitute the newer schema: publish a successor exact binding and obtain H's fresh exact-version decision.

### V323-CUR-02 — C provider outcome source set incomplete (BLOCKING)

Storage v3.2.3 pins C Provider Outcome Blob `f538d921...` and causal submit Blob `45a482...`, but does not bind the complete current C source composition. C's current decision Blob `1353572f...` identifies the normative composition as:
- final-request evidence Blob `fd2f47ba...`;
- causal submit contract Blob `45a482...`;
- owner-local admission/recovery amendment Blob `9609b252...`;
- concrete provider egress gate adapter Blob `a8d1cfc4...`.

The v3.2.3 exact bundle must add the latter two C-owned contracts and bind CSubmitOutcome schema/conformance Blob `7939c84...` where wire/object joins are in scope. C must issue a fresh exact-version decision against the successor Storage + H bundle; prior C acceptance of v3.2.2/v3.2.3 predecessors does not transfer.

### V323-CUR-03 — H semantic verifier boundary remains non-production (BLOCKING FOR CLAIMS, NOT FOR ARCHITECTURE DRAFTING)

H's adapter contract explicitly leaves owner authority, key status, ledger inclusion and anti-rollback verification to I/D/C. The present helper/callback is TEST-ONLY. The successor bundle must retain tri-state VALID/INVALID/UNKNOWN and must not claim that schema validity proves complete owner ledger membership, atomic gate close, or final currentness CAS.

### V323-CUR-04 — Exact A integration review must follow C/H decisions (BLOCKING)

A's integration review must pin one exact successor set: Storage, COC companion, I, D, C, H schema/crosswalk, Storage ordering addendum and relevant membership proof artifacts. A review of a moving branch or mixed historical blobs is not an exact integration decision.

## 4. Required successor sequence / 后续动作

1. Storage publishes a successor exact binding manifest or v3.2.4 that supersedes only the stale pins and preserves v3.2.3 S0a–S4 semantics unless a substantive change is explicitly identified.
2. C reviews the exact successor Storage + H bundle, specifically C owner-local admission, transport egress CAS, same-key provider outcome and the exact CSubmitOutcome object/wire joins.
3. H reviews the exact successor Storage + C bundle, specifically unified schema 1.2.12 (or its explicitly selected successor), owner snapshot/membership proof joins, canonical bytes, requiredness/nullability and semantic validator obligations.
4. I and D confirm that the new union manifest and C membership/effect evidence do not weaken their owner-local request/admission high-water and release predicates. Their earlier I36.8-R1..R4 / D36.8-R1..R4 decisions remain scoped to their exact source blobs.
5. Storage refreshes the exact binding manifest after C/H decisions; A performs the final exact-version integration review.
6. Keep all runtime/conformance/production claims separate. H reference tests and C schema unit tests are bounded evidence, not owner-signature verification, provider exactly-once, persistent COC or production activation.

## 5. Gate vector / Gate 状态

- Storage Gate A architecture design: **CONDITIONAL PASS** within the accepted contract scope; implementation/deployment/operations deferred to engineering.
- Gate B COC architecture: **design proposal; current v3.2.3 cross-owner exact review incomplete**.
- Gate B implementation/conformance: **NOT RUN / DEFERRED_TO_ENGINEERING_PHASE**.
- Gate C distributed end-to-end fault injection: **DEFERRED_TO_ENGINEERING_PHASE**.
- R1/R2 and JF-10 P0: **OPEN** pending the controlling exact-version Owner/A integration gates.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- Production activation: **NOT AUTHORIZED**.

## 6. Provenance / 来源

This audit was authored by the coordinating session in delegated Storage/cross-owner review mode. It is not an independent Storage, C, H, I, D or A Owner signature. All exact hashes above were read from the named Owner branches; no source files were modified by this audit.
