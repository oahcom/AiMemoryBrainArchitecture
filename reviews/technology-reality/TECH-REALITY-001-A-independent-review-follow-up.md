# TECH-REALITY-001-A Independent Review — Follow-up Correction & Expanded Current-Source Delta
# 独立审查后续更正与当前源差异扩展

- Review ID: `TECH-REALITY-001-A-IR-001`
- Parent report: `reviews/technology-reality/TECH-REALITY-001-A-independent-review.md`
- Target: PR #45, reviewed HEAD `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`
- Follow-up date: 2026-11-17
- Review branch: `review/TECH-REALITY-001-A-independent-review-2026-11-17`
- Status: supplemental correction; the original findings remain except where explicitly corrected below.

---

## 1. Correction to PR mergeability statement / PR 可合并状态更正

The parent report stated that PR #45 currently reported `mergeable=false`. That was true in the earlier live metadata read during the review, but a subsequent re-fetch reports:

- PR #45 remains OPEN and Draft.
- Head remains `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`.
- Base remains `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Current GitHub metadata reports `mergeable=true`.

Therefore **mergeability is not a current finding** and must not be used as a reason to reject PR #45. The historical base and stale source evidence remain substantive P1 findings independent of GitHub's mergeability flag.

**中文：** 主报告曾写 PR #45 当前 `mergeable=false`。这在审查早期读取时成立，但随后重新读取的 GitHub 元数据显示 PR #45 仍为 OPEN/Draft，Head/Base 未变，当前 `mergeable=true`。因此**可合并状态不再是当前审查发现**，不能作为拒绝 PR #45 的理由。历史基线与源证据过期仍是独立存在的 P1 问题。

## 2. Storage topology ADR exact readback / Storage 拓扑 ADR 精确读回

The current Storage branch artifact was directly re-fetched:

- Path: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`

The ADR §8 explicitly selects **Option A as the normative v1 logical serialization architecture profile**: one logical serializable transaction domain per Canonical Memory authority. It does **not** select a physical database product, executable deployment, adapter, HA profile or operator. L4 physical engine/deployment remains OPEN; T1–T8 remain OPEN. The ADR also preserves I as a separate PolicyDomain sequencer and COC as a separate quorum log; it explicitly does not claim XA or cross-log atomic commit.

This confirms the narrow distinction in parent finding P2-01:
- L1 logical serialization profile: SELECTED (Option A), with exact ADR pin above.
- L4 physical engine/deployment, D/Storage row ownership, read path, HA/failover/restore, anti-rollback and JF-10 physical bridge: OPEN / NOT PROVEN.

The parent report's phrase “logical v1 serialization architecture profile selected” is correct. Any shorthand saying “Storage topology entirely ADR-BLOCKED / no topology selected” is stale for L1; any shorthand saying “Storage topology solved” is false for L4.

**中文：** 当前 Storage 分支 ADR §8 明确选择 Option A 作为 v1 **逻辑序列化架构配置**：每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain。它没有选择具体数据库产品、可执行部署、Adapter、HA 配置或运维负责人。L4 物理引擎/部署仍 OPEN，T1–T8 仍 OPEN。I 仍是独立 PolicyDomain Sequencer，COC 仍是独立 Quorum Log；ADR 没有声称 XA 或跨日志原子提交。

因此主报告 P2-01 的窄区分成立：
- L1 逻辑序列化配置：已选择 Option A，精确 ADR 如上。
- L4 物理引擎/部署、D/Storage 行归属、Read Path、HA/Failover/Restore、Anti-rollback 和 JF-10 物理桥接：OPEN / NOT PROVEN。

把 Storage 概括为“L1 仍未选拓扑”已过期；把它概括为“Storage 拓扑已完全解决”则错误。

## 3. Current Phase 3.8 source family supersedes the Phase 3.7-only snapshot / Phase 3.8 当前源族已超越仅覆盖 Phase 3.7 的快照

The parent report correctly detected that the Phase 3.7 artifacts were absent from the research synthesis. Further issue/comment and live branch readback shows that the current proposal family has advanced again. The following exact artifacts were re-fetched:

| Owner | Current artifact | Branch | Blob SHA | Status |
|---|---|---|---|---|
| D | `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md` | `session-d-memory-brain-2026-11-16` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` | D-role proposal; exact Owner approval/API/conformance OPEN |
| E | `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md` | `session-e-memory-compiler-2026-11-16` | `475fee41e5eea527af4edefbfe88c58c86967d0a` | E-role proposal; D/I/Storage APIs and independent approval OPEN |
| I | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | `session-i-security-governance-2026-11-16` | `54bab0484bd232a5a258e65e34cc7425288b39a6` | I-role proposal; crypto profile and conformance OPEN |
| Storage | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `175ee7b1349cfdb79a19898b311a88391ed88010` | Storage logical transaction proposal; physical topology/implementation OPEN |
| Storage ADR | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | same Storage branch | `bb544ba2f346bdc130d524bd5c7310d86f367988` | L1 Option A selected; L4 physical realization OPEN |
| A | `reviews/integration/phase-3.8.1-a-contract-surface-and-exact-pin-refresh.md` | `session-a-integration-2026-11-16` | `89f81b16e398653ece127709346baa64baf078ab` | proposed contract surface; NOT OWNER-APPROVED / NOT FROZEN |

The E §3 lifecycle and D/E/I/Storage contracts agree on this logical publication order:

1. E persists ingress and obtains D durable ProducerWork registration before queue/lease/protected dereference/execution.
2. E freezes an immutable compiler input bundle and private-stages output.
3. D registers the complete direct/transitive dependency set.
4. Storage durably creates the exact hidden `StorageVisibilityParticipantRef`.
5. D admits `PublicationParticipantRef` bound to that exact Storage participant.
6. I consumes a single-use CommitAuthorization operation in its own PolicyDomain sequencer, bound to both exact participant refs.
7. Storage final serializable transaction validates the exact D proof and pre-commit I `COMMIT_WON` proof, then atomically commits visibility pointer, outcome, PublicationReceipt and outbox.
8. D and I independently close only after the same authoritative Storage outcome; UNKNOWN remains private and unresolved.

The Phase 3.8 artifacts also distinguish pre-commit I CommitAuthorizationProof from post-commit ITerminalProof. The latter is not a precondition to Storage commit; it is used for I participant closeout after Storage's authoritative result. This avoids the circular proof dependency identified in the issue history.

These are coherent **proposals**, not independent Owner signatures, frozen schema, selected L4 deployment, implementation or conformance proof.

**中文：** 主报告发现研究综合未纳入 Phase 3.7。进一步检查 Issue 与实时分支后发现，当前提案族已推进至 Phase 3.8。上表列出重新读取的精确 Blob。E 与 D/E/I/Storage 的逻辑顺序一致：E 先持久化入口并取得 D 注册；完成私有 Stage 与完整依赖登记；Storage 先持久化隐藏 Participant；D 再绑定该 Participant 准入；I 在自己的 PolicyDomain Sequencer 中单次消费；Storage 最终事务验证 D 和提交前 I COMMIT_WON 证明并原子提交 Visibility/Outcome/Receipt/Outbox；D/I 只有读取同一 Storage 权威结果后才分别关闭。UNKNOWN 保持私有且未解决。

Phase 3.8 还明确区分提交前 I CommitAuthorizationProof 与提交后 ITerminalProof。后者不是 Storage 提交前置条件，而是在 Storage 权威结果产生后用于 I Participant 关闭，避免循环证明依赖。

这些仍是**提案**，不是独立 Owner 签名、冻结 Schema、L4 部署选择、实现或符合性证明。

## 4. Phase 3.8.3 / H wire and I crypto evidence is also outside the research snapshot

Issue #25's latest evidence update records the following candidate artifacts and bounded test evidence:

- I candidate crypto profile `AIMBA-I-CRYPTO-1.0`: Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`.
- I exact review R3 of H mapping: Blob `93afe9c9e06d20de5ce1c2a0f676b4785123fbcf`, ACCEPT WITH ENUMERATED AMENDMENTS.
- H wire mapping: Blob `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`, candidate only.
- H Unified COC/JF-10 schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`.
- H RecoveryJoin schema 1.0.1: Blob `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`.
- H schema candidate CI run 44043259259: 97/97 PASS, structural/reference-model scope only.
- A later H candidate run 44044062849: 101 tests PASS, including four Python/Node JCS/Ed25519 differential candidate tests.

Issue #25 explicitly limits these results: they do not approve the I profile, production trust/key management/HSM/KMS, historical verification, revocation/anti-rollback operations, real COC/Owner adapters, Storage JoinProof durability, currentness CAS, JF-10 physical behavior or selected D/Storage topology. Test-only private seeds are not production keys. H candidate CI is not production wire/crypto or end-to-end Brain conformance.

The current C/Storage/COC evidence is also still bounded. Issue #25 comments identify C exact provider-side-effect review Blob `a7b57bd5531222559666f0f1d9df59a259cde61a`, while live owner-ledger adapters, provider fault/race evidence and C/G/H Applied end-to-end proof remain open. Issue #3 still states Applied Contract Frozen = NO, Test Executed/Passed = NO/NO and Implementation Verified = NO.

**Review impact:** The technology research must add a current-source delta for Phase 3.8/3.8.3. It must not treat these role proposals or candidate test passes as frozen APIs, production cryptographic validation, JF-10 physical proof or end-to-end Applied proof. Durable workflow products remain candidate orchestration mechanisms only; they do not replace the owner-specific D/I/Storage commit/recovery authorities.

**中文：** Issue #25 的后续证据还记录 I Crypto Profile、H Wire Mapping、Unified 1.2.8、RecoveryJoin 1.0.1，以及 H 97/97 和后续 101 项候选测试通过。但 Issue 明确限制其证明范围：不能批准 I Profile、生产信任/密钥管理/HSM/KMS、历史验证、撤销/Anti-rollback、真实 COC/Owner Adapter、Storage JoinProof 持久化、Currentness CAS、JF-10 物理行为或 D/Storage 拓扑。测试私钥不得用于生产。H 候选 CI 不等于生产 Wire/Crypto 或 Brain 端到端符合性。

Issue #25 评论还引用 C Provider Side-effect 精确复审 Blob `a7b57bd5531222559666f0f1d9df59a259cde61a`，但真实 Owner Ledger Adapter、Provider Fault/Race 证据及 C/G/H Applied 端到端证明仍开放。Issue #3 仍明确 Applied Contract Frozen = NO、Test Executed/Passed = NO/NO、Implementation Verified = NO。

## 5. Updated review disposition / 更新后的审查裁决

The parent verdict remains:

- Overall: **REVISE**
- Feasibility: **NOT YET PROVEN**
- Architecture freeze: **NOT READY**

The current-source delta makes P1-01/P1-02 more important, not less. The research package is not merely missing one Phase 3.7 addendum; it predates a larger Phase 3.8/3.8.3 proposal and evidence family. The corrected remediation should:

1. Preserve the research's historical baseline and exact pins.
2. Add a current-main/Owner-source delta through the current Phase 3.8/3.8.3 artifacts, with branch/commit/path/Blob pins.
3. Distinguish Storage L1 Option A selected from L4 engine/deployment still OPEN.
4. Distinguish logical D/E/I/Storage proposal sequence from exact Owner approval, schema freeze, runtime implementation, JF-10 physical proof and end-to-end conformance.
5. Record bounded H CI and I crypto candidate evidence with exact scope; do not elevate them to production proof.
6. Keep C/G/H Applied frozen/test/implementation status at NO until Issue #3's authorities and evidence change.
7. Re-run independent review after the research owner publishes the corrected exact HEAD.

No new Owner authority is exercised by this follow-up. No merge, schema freeze, implementation, Gate release, deployment or production activation is authorized.

**中文：** 主报告裁决不变：REVISE；NOT YET PROVEN；NOT READY。当前源差异进一步强化 P1-01/P1-02：研究不只是漏了一个 Phase 3.7 补充，而是落后于更完整的 Phase 3.8/3.8.3 提案与证据族。整改应保留历史基线，新增当前 Main/Owner 差异；区分 Storage L1 Option A 已选与 L4 物理部署未决；区分逻辑提案、Owner 批准、Schema Freeze、运行时实现、JF-10 物理证明和端到端符合性；准确限定 H CI/I Crypto 候选证据；在 Issue #3 权威和证据改变前继续保持 Applied 未冻结/未测试/未实现。修订后必须针对新精确 HEAD 再次独立复审。

本补充不行使任何 Owner 权威，不授权合并、Schema Freeze、实现、Gate 释放、部署或生产激活。
