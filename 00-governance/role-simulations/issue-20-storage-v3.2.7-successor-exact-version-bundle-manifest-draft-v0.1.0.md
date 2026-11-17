# Storage-role draft — v3.2.7 successor exact-version bundle manifest
# Storage 角色草案 — v3.2.7 后继精确版本 Bundle 清单

- Status: **P COORDINATOR DRAFT / NOT STORAGE OWNER ISSUED / NOT JOINTLY ACCEPTED / NOT FROZEN**
- Supersedes for review routing: Storage v3.2.6 manifest Blob `dbfa37617d109d5891a067769e858085e2ce547a`.
- Normative Storage body remains v3.2.3 Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- Provenance: Session P simulated Storage role; not independent Storage Owner approval.

## 1. Purpose / 目的

This draft updates the successor review bundle from H Unified 1.2.13 to the current H Unified 1.2.14 and rebinds the exact C/H/I/D sources. It does not rewrite Storage v3.2.3, modify v3.2.6, select a physical database engine or authorize deployment.

本草案将后继审查 Bundle 从 H Unified 1.2.13 更新为当前 H Unified 1.2.14，并重新绑定 C/H/I/D 精确源。它不改写 Storage v3.2.3、不修改 v3.2.6、不选择物理数据库引擎，也不授权部署。

## 2. Normative Storage/COC source set / Storage/COC 规范源

| Artifact | Blob | Binding |
|---|---|---|
| Storage v3.2.3 normative protocol body | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | S0a–S4, Recovery Cutoff Batch, Participant Manifest, same-GID recovery, visibility proof |
| COC companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest, digest chain, participant union |
| Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Distinct immutable Batch then Manifest with backlink |
| R1/R2 recovery-round addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable successor RecoveryRound and owner-local release |
| Serialization topology ADR | `bb544ba2f346bdc130d524bd5c7310d86f367988` | L1 Option A selected; L4 physical engine/deployment OPEN |
| Historical v3.2.6 manifest | `dbfa37617d109d5891a067769e858085e2ce547a` | Historical predecessor; not current 1.2.14 binding |

## 3. Current C/H exact source set / 当前 C/H 精确源集合

| Owner | Artifact | Exact Blob |
|---|---|---|
| C | Normative Provider Outcome semantic contract | `819705037da89834e10b6dd2ec6e66c1b8c70886` |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C | C sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` |
| C | C profile identifier decision | `5067dadb9c646a054d78f03c56e635facc36311a` |
| C | Current exact review (needs refresh) | `28d6044ed702565ebfbad9b93555759aaf5fdbe1` — pins old H mapping `8c5c22...` |
| H | Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` |
| H | RecoveryCutoff 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` |
| H | Current Phase 3.8.11 mapping | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` |
| H | Phase 3.8.12 closure (needs refresh) | `d9c09f0eab9d0ca23e01627e2bd399363d20e2cd` — pins old H mapping `8c5c22...` |

## 4. Current I/D exact source set / 当前 I/D 精确源集合

| Owner | Artifact | Exact Blob | Status |
|---|---|---|---|
| I | Phase 3.8.10 P0 allowlists | `35e6843da8becbf3b152512a561b05cf5486819b` | I-owned L1 field contract candidate |
| I | Phase 3.8.12 exact review | `fbd44d57bdb4fc15c4c254fcd9d8ac4c58d365fc` | Accepts current H schema `09fcd...` and mapping `c196...`; trust/L3 open |
| D | Phase 3.8.6 membership P0 crosswalk | `bf35b7f047a374268920b99199b1d5c9aef39c5fd` | D-owned proof mapping candidate |
| D | Phase 3.8.8 exact schema/fence review | `6aca7d020caecf3c69debf614c903bf469583260` | Accepts current H schema/mapping; L3 open |
| D | Historical Storage-anchor review | `723ea31efcb94eae317e941f16259720b0d633fb` | Pins superseded H schema `fee452...`; refresh or retain as historical only |

## 5. Authority and transaction boundaries / 权威与事务边界

- C alone issues Provider Outcome truth from actual transport/provider evidence and same-key authoritative lookup.
- I owns policy authorization, revocation, trust registration, key status and I owner-local gate/release.
- D owns ForgetOperation, ForgetFenceGeneration, producer/work/attempt/derivative lineage, barrier and D release.
- H owns schema, wire mapping, strict decoding, digest/signature validation orchestration and cross-owner typed joins; it cannot synthesize C/I/D/Storage truth.
- Storage owns COC durable records, participant/manifest ordering, physical persistence, StorageVisibilityOutcome and pointer/receipt/outbox atomicity.
- A integrates exact contracts and gates; it cannot replace an Owner signature or evidence.

C `HANDOFF_ACCEPTED` is not Storage `COMMITTED_VISIBLE`; Storage visibility does not prove provider acceptance. I `COMMIT_WON` authorizes only the exact tuple and does not prove provider handoff. D clearance remains independently D-owned. UNKNOWN/IN_DOUBT holds the affected participant/gate; no retry-as-new.

## 6. Required owner updates before a joint bundle / 共同 Bundle 前置 Owner 更新

1. C refreshes Phase 3.8.15 to pin current H mapping Blob `c196fd...`.
2. H refreshes Phase 3.8.12 closure to pin `c196fd...` and the exact H 1.2.14 schema/RecoveryCutoff 1.0.5 set.
3. D refreshes or explicitly retires its anchor-review pin `fee452...`, retaining D Phase 3.8.8 current-schema review `6aca...`.
4. Storage publishes the actual v3.2.7 successor manifest on the Storage branch, preserving v3.2.3 normative body and not rewriting v3.2.6.
5. I confirms its P0/Trust/Profile scope against the same exact manifest; the C profile remains NOT REGISTERED and I production trust remains OPEN.
6. A independently reviews the actual Storage-issued v3.2.7 Blob and the exact C/H/I/D decisions.

## 7. Evidence and gates / 证据与 Gate

- H Provider Outcome: run `44067666900` 22/22 PASS on `9892c21...`; later run `44068247661` 25 tests PASS on `0701b12...`.
- H RecoveryCutoff: run `44068545618` 266 passed / 22 legacy skipped / 0 failed on `88f370b...`.
- C candidate: run `44059935858` 19 tests PASS on `b499663...`.
- These are candidate suites only. They do not prove production profile registration, provider adapter truth/idempotency, live owner ledger completeness, COC quorum, Storage L4 deployment, physical serialization, HA/restore or end-to-end fault injection.

Current gates:
- L1 logical serialization: Option A selected in ADR `bb544...`.
- L4 physical engine/runtime/deployment: OPEN; no production DB selected.
- JF-10 P0, R1/R2, owner release CAS, I/C profile trust, C provider adapter, COC quorum and Gate B/C: OPEN/BLOCKED.
- Multi-PolicyDomain, Global Forget completion, physical erasure and production activation: NOT AUTHORIZED.

## 8. Draft disposition / 草案结论

**BOUND FOR JOINT REVIEW ONLY; NOT JOINTLY ACCEPTED / NOT FROZEN.**

This P draft is not the Storage Owner-issued v3.2.7 manifest. No actual Owner branch has been modified. The Storage Owner must issue the successor and the other Owners must review the same immutable Blob set before A can consider a conditional release recommendation.
