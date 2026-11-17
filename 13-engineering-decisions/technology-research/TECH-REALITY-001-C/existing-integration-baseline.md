# Existing Integration Baseline / 现有集成基线

**Observed:** 2026-11-18 UTC | **Repository:** `oahcom/AiMemoryBrainArchitecture`

## Main baseline / Main 基线
- Default branch: `main`; HEAD: `b3c666e67982cb3d3374e759cfb6552c7765aacb`.
- Repository is private; connected GitHub permissions observed: admin/maintain/push/pull.
- Research branch created from this exact main SHA: `research/tech-reality-001-c`.
- Historical C branch `session-c-agent-integration-2026-11-16`: HEAD `71047cdb51139ca4080ac67f451e38a48698859d`; compare against main is DIVERGED, 167 ahead / 56 behind, 104 changed files. It is not the new research base.

## Main source pins / Main 源文件
| Area | Path | Blob SHA |
|---|---|---|
| Responsibility | `01-system-architecture/responsibility-matrix.md` | `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3` |
| AI development standard | `14-ai-development/ai-development-standard.md` | `f46867f97fc1860015adbe2a1f7b8262640c16fd` |
| B domain overview | `02-domain-model/domain-model-overview.md` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` |
| B core entities | `02-domain-model/core-entities.md` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` |
| B epistemic/time | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` |
| B scope/permission | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` |
| C overview | `07-agent-integration/agent-integration-overview.md` | `073ff4ddf71fbcaf959107bb06ab724bfa48e63b` |
| C inference | `07-agent-integration/inference-boundary-model.md` | `e2d5cb6abd9ec40da6e3680531de5944fc8b14df` |
| C capability tiers | `07-agent-integration/adapter-capability-tiers.md` | `09c5932350c48f950ee16f6b246f54e661f0c420` |
| C telemetry | `07-agent-integration/telemetry-model.md` | `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0` |
| Technology blueprint | `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` |

## A research / A 研究
- PR #45: Open / Draft; branch `ai/TECH-REALITY-001-A/principal-technology-research`; head `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`; historical base `b372b62c640a2b656e54b6db62a4ee67d7d8c001).
- A README Blob `e69498b4945213e797e9c7ba1ab5a4a3080c2b6a`; technology recommendation Blob `cc2269dfd5d95fe85089287e1be9579bddce1ef2`; mature-project research Blob `115f47af30183235f9bfbd096ff02e860c230204`; topology comparison Blob `b5269966b5a073371a50ea675aee87c23306835d`.
- PR #56 independent technology review: Open / Draft, verdict **REVISE**, feasibility **NOT YET PROVEN**. Review itself notes separate-session/context independence, not a different model/provider or human audit.
- A candidate stacks are not approved technology decisions. Its source/currentness findings remain relevant and are not silently accepted.

## B research / B 研究
- PR #55: Open / Draft; branch `research/domain-reality-001-b`; head `f95b479b223ebb63c8aebcfca13a4cd9b28d5331`; PR base SHA `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`.
- PR metadata reports B0 PARTIAL / NOT PASSED, B5 BLOCKED / NOT PASSED, B6 INDEPENDENT_REVIEW_PENDING. Fact/Claim remains ADR-BLOCKED.
- B's main-branch domain files above were read and their Blob SHAs verified. The complete B branch package and all changed files were not independently re-read in this C pass: **NOT VERIFIED**.

## Owner branch snapshots / Owner 分支快照
| Owner | Branch | HEAD | Exact relevant Blob(s) read |
|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Forget contract `1f0391bc49d007c44ec74165bd33d37412cc7990` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Local lifecycle producer `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | Local lifecycle/runtime `29e9504c75d737c2dd200ebc3306eda555f0b0ac` |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | Applied/Forget contract `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| H | `session-h-bmcp-protocol` | `0d36324457e39bd50ad56ae902d477c4ea765b61` | Unified 1.2.15 schema `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; mapping `2dc30f193d9c4f4bdc05ca4c137103687db28924` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | Governance register `f5fd2558c657f4ef49396a7a00cdbcd0f226f853`; commit authorization `5a5304d48aa912dcf6f817099bd5659371d8cdc8` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | Option A ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`; v3.3.2 manifest `5c614375e10698e4931d83deb57d20321445e068` |

## Verified gaps / 已确认缺口
- Current main is a consolidated baseline and does not contain the full historical D/E/F/G/H/I owner trees. Those owner snapshots are separate branches, not main-merged contracts.
- C historical branch diverges materially and is not current main.
- H 1.2.15 is a schema candidate; Storage v3.3.2 explicitly binds H 1.2.14 and CSubmitOutcome 1.0.1, not 1.2.15.
- C crypto profile `AIMBA-C-CRYPTO-1.0` and I governance signature profile remain NOT REGISTERED in C Phase 3.11.0.
- G states Applied contract freeze BLOCKED and implementation/execution NOT VERIFIED.
- I governance register is candidate; no policy decision is effective merely because a document exists.
- No complete production implementation is verified from these documents.

## 中文核验结论
以上 HEAD、Blob 和 PR 状态均为本次直接读取的 GitHub 证据。A/B 的研究提交均处于 Draft/未完成独立审查状态；C 历史分支与 main 分叉；D/E/F/G/H/I/Storage 的独立分支快照不能被当作 main 已采纳合同。未读取的文件明确保持 NOT VERIFIED。C0 因此为 PARTIAL，而非 PASS。
