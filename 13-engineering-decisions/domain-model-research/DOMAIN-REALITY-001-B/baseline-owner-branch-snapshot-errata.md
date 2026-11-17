# Baseline Owner Branch Snapshot Errata
# 基线 Owner 分支快照勘误

- ID: B-BASELINE-ADD-002
- Status: CORRECTIVE ADDENDUM — supersedes conflicting branch-tip rows in B-BASELINE-ADD-001
- Date: 2026-11-17

## 1. Correction / 更正

The earlier audit's Owner branch-tip table was assembled from an earlier tree snapshot and must not be treated as the latest branch inventory. The later Phase 3.8 branch-tip snapshot in `cross-owner-canonical-semantics-matrix.md`, Section 1A, is the controlling observed data for the listed Owner branches in this addendum.

此前审计中的 Owner 分支 Tip 表来自较早 Tree 快照，不得视为最新分支清单。跨 Owner 矩阵第 1A 节的后续 Phase 3.8 分支 Tip 快照，是本勘误所列 Owner 分支的控制性已观察数据。

| Owner | Branch | Later observed HEAD | Exact artifact pin |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | Phase 3.8.6 review `e2bc4c8dde9706bfbe443269b702f1b5aa6965f6` |
| C | `session-c-agent-integration-2026-11-16` | `2e8414f361b0b5d7de959be8a971aadc9e62d6a9` | Phase 3.8.22 review `8fd6052cabf58a78962cc2e776398b2a40604bcd` |
| D | `session-d-memory-brain-2026-11-16` | `76fcc92225666a11893b7241825261319edb621e` | Phase 3.8.13 review `152627e00b96355e2ff370acd643a51168c4c78c` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63a3b8dd77f670ed` | Phase 3.8.6 review `19d708bc29b6115d7bccb7d320781f452ee28b78` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | Phase 3.8.6 review `122238146830db6188f00a9788e018a82bfb3f90` |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | Phase 3.8.18 review `1894860c76336f8739d354b72beed3992cffd17e` |
| H | `session-h-bmcp-protocol` | `8e24342048d29ef29195b153b8b9ec53ba7c75d9` | Phase 3.8.20 review `4ba7e1699215d02224f805a15484b1da2e40c03f` |
| I | `session-i-security-governance-2026-11-16` | `2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9` | Phase 3.8.18 review `b6d1ea45825a1c2090abfba42474814f02f073a3` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `431138e7c7af8bee716f3d8dcbc20114c046bd36` | v3.2.11 manifest `54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57` |
| A | `session-a-integration-2026-11-16` | `9bdf938b980413f592a4db9fe94f4bf2c299fb01` | Phase 3.8.19 review `e12cd7b5c79e2234178014243fd51f2e7d51272e` |

These are observed snapshot values, not permanent branch tips. Re-fetch live refs and current Blobs before final acceptance or merge decisions.

以上是观察快照，不是永久分支 Tip。最终验收或合并决策前必须重新获取实时 Ref 和当前 Blob。

## 1A. 中文 Owner 分支快照对照

| Owner | 分支 | 后续观察到的 HEAD | 精确工件 Pin / 观察结果 |
|---|---|---|---|
| B | session-b-domain-model-phase3 | 2faf8ec38f14dba49e7263d7a60804dae1a74ee2 | Phase 3.8.6 复审 Blob e2bc4c8dde9706bfbe443269b702f1b5aa6965f6：仅批准每 Authority 名义类型边界。 |
| C | session-c-agent-integration-2026-11-16 | 2e8414f361b0b5d7de959be8a971aadc9e62d6a9 | Phase 3.8.22 复审 Blob 8fd6052cabf58a78962cc2e776398b2a40604bcd：接受 H Reference Gate/60 项测试边界，Signer/Attestation 仍开放。 |
| D | session-d-memory-brain-2026-11-16 | 76fcc92225666a11893b7241825261319edb621e | Phase 3.8.13 复审 Blob 152627e00b96355e2ff370acd643a51168c4c78c：H 仅为上游接口，不改变 D 权威。 |
| E | session-e-memory-compiler-2026-11-16 | ee098e14747d9915de5b3efb63b3a8dd77f670ed | Phase 3.8.6 复审 Blob 19d708bc29b6115d7bccb7d320781f452ee28b78：在 E 生命周期条件下接受。 |
| F | session-f-memory-runtime | 1908ce4d233b20f7cafd00cb679affd01bd15174 | Phase 3.8.6 复审 Blob 122238146830db6188f00a9788e018a82bfb3f90：在读路径/Cache 条件下接受。 |
| G | session-g-memory-context | 3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe | Phase 3.8.18 复审 Blob 1894860c76336f8739d354b72beed3992cffd17e：接受有限 L1/L2 映射，Applied Contract 仍未冻结。 |
| H | session-h-bmcp-protocol | 8e24342048d29ef29195b153b8b9ec53ba7c75d9 | Phase 3.8.20 复审 Blob 4ba7e1699215d02224f805a15484b1da2e40c03f：修正 P0 Proof Locator，认证实现仍开放。 |
| I | session-i-security-governance-2026-11-16 | 2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9 | Phase 3.8.18 复审 Blob b6d1ea45825a1c2090abfba42474814f02f073a3：接受 Signer 分离候选，Crypto/Trust 注册未批准。 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 431138e7c7af8bee716f3d8dcbc20114c046bd36 | v3.2.11 Manifest Blob 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57：精确候选包，尚未联合接受/冻结。 |
| A | session-a-integration-2026-11-16 | 9bdf938b980413f592a4db9fe94f4bf2c299fb01 | Phase 3.8.19 复审 Blob e12cd7b5c79e2234178014243fd51f2e7d51272e：外层认证为阻塞性架构缺口。 |

以上 HEAD 是分支快照，不是 Owner 批准或独立审查。最终决策前必须重新读取实时 Ref 和精确 Blob。

## 2. Scope and interpretation / 范围与解释

- The older C/D/E/G/H/I/Storage branch-tip rows in B-BASELINE-ADD-001 are superseded by this table.
- The B research branch `research/domain-reality-001-b` is distinct from the Owner branch `session-b-domain-model-phase3`.
- At the latest direct ref read during this audit, the research branch HEAD was `5797ff44db7e3fdbc0820a08e91ff78f76c4faac`; re-read it before relying on this value.
- Artifact Blob acceptance is exact-version and owner-scoped; a branch tip alone does not constitute approval.

- B-BASELINE-ADD-001 中较旧的 C/D/E/G/H/I/Storage 分支 Tip 行由本表取代。
- B 研究分支 `research/domain-reality-001-b` 与 Owner 分支 `session-b-domain-model-phase3` 不同。
- 本次审计最近一次直接读取到的研究分支 HEAD 为 `5797ff44db7e3fdbc0820a08e91ff78f76c4faac`；依赖此值前仍须重新读取。
- Artifact Blob 验收受精确版本和 Owner 权限范围约束；分支 Tip 本身不构成批准。

## 3. Gate effect / 门禁影响

This correction improves snapshot accuracy only. B0 remains PARTIAL / NOT PASSED; B3 remains NOT PASSED. No canonical freeze, schema freeze, implementation authorization or production readiness is inferred.

本勘误仅提高快照准确性。B0 仍为 PARTIAL / NOT PASSED；B3 仍未通过。不得推断规范冻结、Schema 冻结、实现授权或生产就绪。
