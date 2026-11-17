# Phase 2 — Exact Evidence Ledger
# 第二阶段 — 精确证据登记册

- Review: ARCH-CONSOL-001 / Issue #43
- Snapshot date: 2026-11-17
- Branches are independent Owner workspaces. Main is not the authority for unmerged Owner decisions.
- Every entry below records a live branch HEAD and one or more exact readback Blobs. A Blob pin is immutable; a changed Blob requires a new review.

## 1. Branch-head snapshot / 分支 HEAD 快照

| Owner | Branch | HEAD commit | Exact source artifact(s) read / 本次读取工件 |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | f8895bf18df1e23f1f0ea1608b4d32398ac2c363 | Phase 1 reassessment: 1ffb788c7e193b8777e8d849c1e3cc11ededc545 |
| B | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 | Domain overview: 4d1debc0ec19b3917f9e76d04bb66da4df4cd346; BIH evidence ledger: 57242fd4342e3951aeab8c7ea6b57d02fea36f64 |
| C | session-c-agent-integration-2026-11-16 | fecd92502455a4deb4b1119f8de11504e5f6fedf | CSubmitOutcome schema 1.0.1: a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda; Provider Egress Gate: a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca; Phase 3.8.6 amendment: 392a3fd43790db59cb8aa5b3c919ca98e4bcddb4; Phase 3.8.8 projection: 06d9264124d85896ccd44ef7789d9af245d8255b; Phase 3.8.9 contract: 2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac |
| D | session-d-memory-brain-2026-11-16 | 73bcfaac2e4984dd9bb6f14a878146dd092b7e02 | Forget Fence operation contract: 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5; Phase 3.8 publication contract: 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78; Phase 3.8.5 wire adoption amendment: 46b6abd94f3396e5eef7d7456f9b62a3865d4ce2 |
| E | session-e-memory-compiler-2026-11-16 | df3f56cdebbb4bb85999e2e04b666dacf77da810 | Phase 3.7 lifecycle: 4fb9e58511941f59b4d777336f8f85ad88ecccf1; Phase 3.8 publication orchestration: 475fee41e5eea527af4edefbfe88c58c86967d0a |
| F | session-f-memory-runtime | 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | Phase 3.7 lifecycle: 29e9504c75d737c2dd200ebc3306eda555f0b0ac |
| G | session-g-memory-context | 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | Context architecture: 56fcc0ea112d423ef69a3f00e9d626bf4230ca0e; Context versioning: 05c0739d0c22576a1fd5affc7d73c078c89049b1; Phase 3.7 lifecycle: c1de241ec69834377d9b0e24aa4770a809796d4b |
| H | session-h-bmcp-protocol | c508098ee856c37826dff8a18713388a1af53726 | Unified schema 1.2.12: a54f66914a819d77f00c6af04e76453ff9f654ee; RecoveryJoin 1.0.2: 4b664e3bce465499bcdfd93796349a4ba7074002; R1/R2 wire crosswalk: 8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c; Provider Outcome validator contract bound to 1.2.11: ac800ddbb1fb13aa7eaef415e2282db971d73ff4 |
| I | session-i-security-governance-2026-11-16 | 80ecf0e94fc88cc08e1d0d4f587215292fa2ca5e | Current authorization/restore contract: e3b1b5d99eb36ac0b395854d8c19287d2b64b752; Phase 3.8 authorization receipt contract: 54bab0484bd232a5a258e65e34cc7425288b39a6; Phase 3.8.5 wire adoption amendment: b56b0c3690f1826f2fc965ec6af5d66a920004ae |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | ce07f528d1385dfb48c1f0a785f9427988ed37b5 | Storage v3.2.3 normative body: 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792; COC companion: 5b950a3a29bd7a5276b92a49a9114d700718b987; v3.2.4 successor manifest: 6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7; Phase 3.8 visibility contract: 175ee7b1349cfdb79a19898b311a88391ed88010; topology ADR: 080433f8e13a500522bc2754da64057edb0ae9d8 |

Main branch HEAD at snapshot: b372b62c640a2b656e54b6db62a4ee67d7d8c001. Review branch was created from main and does not modify it.

## 2. Evidence interpretation / 证据解释

- A Phase 1 report is an in-progress reassessment, not a final freeze decision.
- B's domain overview is a DECIDED semantic baseline, but the Fact/Claim ADR remains ADR-BLOCKED.
- C's schema 1.0.1 exists on the current branch; the C Phase 3.8.9 contract still binds schema 1.0.0 and H 1.2.11.
- D/I Phase 3.8.5 amendments adopt H 1.2.12 / RecoveryJoin 1.0.2 as candidates only; both explicitly require H cross-review and do not claim independent human Owner approval.
- H Unified 1.2.12, RecoveryJoin 1.0.2 and the R1/R2 crosswalk are candidate structural artifacts. The H Provider Outcome semantic validator contract read in this snapshot is still tied to Unified 1.2.11.
- E/F/G Phase 3.7 lifecycle files are Owner-local semantic proposals; cross-owner interfaces and conformance remain open.
- Storage v3.2.4 is an exact-version successor manifest, not a rewritten normative v3.2.4 protocol. Storage v3.2.3 remains the normative technical body.
- Storage topology ADR 080433... is ADR-BLOCKED / NO TOPOLOGY SELECTED.
- C/H key-status CI runs (C 12 tests; H 11 tests) are bounded schema/state-machine evidence only. They do not register production trust roots, keys or custody.
- H's earlier recovery/semantic suites and COC reference models are bounded evidence. They do not prove live COC quorum, production owner ledgers, provider adapter races, deployed topology or physical recovery.

## 3. Bounded CI evidence recorded in source artifacts / 源工件记录的有限 CI 证据

| Evidence | Result | Ceiling / 证据上限 |
|---|---|---|
| H candidate RecoveryJoin / Unified suite, run 44051851164 | 288 total; 266 passed; 22 skipped; 0 failed | Structural/reference candidate only; exact test scope and skipped cases must be rechecked before L3 closure. |
| C key-status suite, run 44059137081 | 12 passed | Schema/state-machine only; no production key registry or trust-root approval. |
| H key-status callback suite, run 44058962672 | 11 passed | Schema and fail-closed callback behavior; no production trust service or external anti-rollback. |
| COC outage recovery model, run 43897364938 | 11 passed | In-memory logical model only; not deployed quorum COC or physical recovery. |
| JF-10 PostgreSQL 18.7 Gate A capability classes, Issue #10 | Five CI classes reported successful: single-node restart, synchronous standby promotion/same-GID resolution, physical restore, coordinator crash fixture, TCP response loss/same-XID reconciliation | Gate A remains PARTIAL PASS / OPEN; Gate B persistent COC and Gate C fault campaign remain BLOCKED. Does not prove designated Canonical Authority runtime, PITR, old-primary fencing, real I/D ledger integration or production operator. |
| PostgreSQL 18.7 capability CI, Issue #10 | Gate A PARTIAL PASS | Pinned capability profile only; not selection/deployment of Canonical Authority topology. |

## 4. Freshness and supersession rules / 时效与替代规则

1. A branch name does not identify an immutable decision. Use branch HEAD + commit + path + Blob.
2. A Blob change invalidates any decision that reviewed the old Blob unless the Owner explicitly defines a compatible range.
3. A schema artifact revision is not necessarily the wire-family version; record both.
4. Role-simulated decisions are technical analysis only. They do not satisfy independent Owner or external governance approval.
5. This ledger is a snapshot. Re-fetch all Owner branch heads and exact source Blobs before final freeze disposition.



## 5. 中文镜像：Owner 分支与精确工件 / Chinese mirror of the Owner snapshot

| Owner | 分支 | HEAD Commit | 本次读取的精确工件 Blob |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | f8895bf18df1e23f1f0ea1608b4d32398ac2c363 | Phase 1 总审查：1ffb788c7e193b8777e8d849c1e3cc11ededc545 |
| B | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 | 领域模型总览：4d1debc0ec19b3917f9e76d04bb66da4df4cd346；BIH 证据登记册：57242fd4342e3951aeab8c7ea6b57d02fea36f64 |
| C | session-c-agent-integration-2026-11-16 | fecd92502455a4deb4b1119f8de11504e5f6fedf | CSubmitOutcome 1.0.1 Schema：a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda；Provider Egress Gate：a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca；3.8.6 语义修订：392a3fd43790db59cb8aa5b3c919ca98e4bcddb4；3.8.8 签名投影：06d9264124d85896ccd44ef7789d9af245d8255b；3.8.9 Schema/Conformance 合同：2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac |
| D | session-d-memory-brain-2026-11-16 | 73bcfaac2e4984dd9bb6f14a878146dd092b7e02 | Forget Fence 合同：4da0b61ba3656a768ea56b4a2a24e09da4e21cd5；3.8 发布合同：17e53890dd6cce9bea9eacc1be2e64b0ef55ac78；3.8.5 Wire 采纳修订：46b6abd94f3396e5eef7d7456f9b62a3865d4ce2 |
| E | session-e-memory-compiler-2026-11-16 | df3f56cdebbb4bb85999e2e04b666dacf77da810 | 3.7 生命周期：4fb9e58511941f59b4d777336f8f85ad88ecccf1；3.8 发布编排：475fee41e5eea527af4edefbfe88c58c86967d0a |
| F | session-f-memory-runtime | 348b5ec84c44a8a067122ce0aa72a594b9c06b66 | 3.7 生命周期：29e9504c75d737c2dd200ebc3306eda555f0b0ac |
| G | session-g-memory-context | 69ba55c5ffd473ced1ccb569e9bbf7fea48566aa | Context 架构：56fcc0ea112d423ef69a3f00e9d626bf4230ca0e；Context 版本：05c0739d0c22576a1fd5affc7d73c078c89049b1；3.7 生命周期：c1de241ec69834377d9b0e24aa4770a809796d4b |
| H | session-h-bmcp-protocol | c508098ee856c37826dff8a18713388a1af53726 | Unified Schema 1.2.12：a54f66914a819d77f00c6af04e76453ff9f654ee；RecoveryJoin 1.0.2：4b664e3bce465499bcdfd93796349a4ba7074002；R1/R2 Wire Crosswalk：8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c；仍绑定 1.2.11 的 Provider Outcome Validator：ac800ddbb1fb13aa7eaef415e2282db971d73ff4 |
| I | session-i-security-governance-2026-11-16 | 80ecf0e94fc88cc08e1d0d4f587215292fa2ca5e | 3.7 授权/恢复合同：e3b1b5d99eb36ac0b395854d8c19287d2b64b752；3.8 授权 Receipt 合同：54bab0484bd232a5a258e65e34cc7425288b39a6；3.8.5 Wire 采纳修订：b56b0c3690f1826f2fc965ec6af5d66a920004ae |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | ce07f528d1385dfb48c1f0a785f9427988ed37b5 | Storage v3.2.3 规范正文：5cee0d58575adc0fb3dd20a5c7ab68c2a2711792；COC 配套协议：5b950a3a29bd7a5276b92a49a9114d700718b987；v3.2.4 后继绑定清单：6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7；3.8 可见性合同：175ee7b1349cfdb79a19898b311a88391ed88010；拓扑 ADR：080433f8e13a500522bc2754da64057edb0ae9d8 |

## 6. 中文镜像：证据边界 / Chinese mirror of evidence ceilings

- A Phase 1 文件是正在进行的重新审查，不是最终冻结裁决。
- B 领域总览是 DECIDED 基线，但 Fact/Claim ADR 仍 ADR-BLOCKED。
- C 当前分支存在 CSubmitOutcome 1.0.1；C 3.8.9 合同仍绑定 1.0.0，且仍引用 H 1.2.11。
- D/I 3.8.5 对 H 1.2.12 / RecoveryJoin 1.0.2 的采纳只是候选角色修订，不是独立人类 Owner 批准。
- H 1.2.12、RecoveryJoin 1.0.2 和 R1/R2 Crosswalk 是候选结构工件；本次读取的 Provider Outcome 语义 Validator 仍绑定 1.2.11。
- E/F/G 3.7 生命周期文件是各自 Owner 的局部语义提案；跨 Owner 接口和符合性仍 OPEN。
- Storage v3.2.4 是精确版本后继绑定清单，不代表规范技术正文已升级为 v3.2.4；规范正文仍是 v3.2.3。
- Storage 拓扑 ADR 明确为 ADR-BLOCKED / NO TOPOLOGY SELECTED。
- C/H Key Status CI 只证明 Schema/状态机的有限行为，不代表生产 Trust Root、Key Registry 或密钥托管已批准或部署。
- H 结构/语义候选套件、COC 参考模型和 PostgreSQL 能力 CI 都有明确证据上限；不能替代真实 COC Quorum、Owner 持久账本、Provider Adapter 竞争、生产拓扑或物理恢复证明。
- JF-10 的五类 PostgreSQL 18.7 能力 CI 已报告成功，但 Gate A 仍 PARTIAL PASS / OPEN；Gate B 持久化 COC 与 Gate C 确定性故障注入仍 BLOCKED。项目实际 Canonical Authority 运行时、PITR、旧主隔离、真实 I/D 账本和生产 Operator 尚未指定。

## 7. 中文镜像：有限 CI 证据 / Chinese mirror of bounded CI evidence

| 证据 | 结果 | 证据上限 |
|---|---|---|
| H RecoveryJoin / Unified 候选套件，Run 44051851164 | 288 总计；266 通过；22 跳过；0 失败 | 仅结构/参考候选；L3 关闭前必须复核测试范围与跳过项。 |
| C Key Status 套件，Run 44059137081 | 12 通过 | 仅 Schema/状态机；无生产 Key Registry 或 Trust Root 批准。 |
| H Key Status Callback 套件，Run 44058962672 | 11 通过 | 仅 Schema 与 Fail-closed Callback；无生产 Trust Service 或外部 Anti-rollback。 |
| COC Outage Recovery 模型，Run 43897364938 | 11 通过 | 仅内存逻辑模型；不是已部署 Quorum COC 或物理恢复。 |
| JF-10 PostgreSQL 18.7 Gate A，Issue #10 | 五类能力 CI 报告成功 | Gate A 仍 PARTIAL PASS；Gate B/C 仍 BLOCKED。不能证明项目已选定/部署 Canonical Authority。 |

