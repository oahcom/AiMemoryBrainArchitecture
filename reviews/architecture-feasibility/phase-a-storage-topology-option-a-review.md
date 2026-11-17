# ARCH-CONSOL-003 — A: Option A Storage/D Serialization Topology Review
# ARCH-CONSOL-003 — A：Option A Storage/D 序列化拓扑审查

- Repository: oahcom/AiMemoryBrainArchitecture
- Review scope: Storage/D per-BrainAuthority serialization topology, Storage v3.2.9 exact bundle, C/D/I anchor reviews and D/E lifecycle contracts
- Exact topology ADR Blob: bb544ba2f346bdc130d524bd5c7310d86f367988
- Exact Storage v3.2.9 manifest Blob: bf323a1682f2bfadc3ff41ea4f86883d678a77e3
- Normative Storage v3.2.3 Blob: 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792
- COC companion Blob: 5b950a3a29bd7a5276b92a49a9114d700718b987
- H Unified 1.2.14 Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- H Authority-Join mapping Blob: 1cbe74eba69325510d6b1019d971661f965eabf8
- CSubmitOutcome 1.0.1 Blob: a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- D ForgetFence/Producer Admission contract Blob: 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5
- E lifecycle contract Blob: 4fb9e58511941f59b4d777336f8f85ad88ecccf1
- Storage v3.2.9 H local full-path CI: run 44069777296, commit 9eb06313e94e762f0fde4a606633a6dbe1bf8262, job 133992753552, 32 test methods
- Disposition: **CONDITIONAL ACCEPT OF OPTION A AS THE V1 LOGICAL TOPOLOGY; L1 CLARIFICATIONS REQUIRED; DO NOT FREEZE**
- Provenance: delegated A-role integration review; **not an independent human A Owner signature**
- English and Chinese are normative peers

## 1. Executive decision / 总体决议

Option A is the correct v1 direction among the three ADR options. A single serializable transaction domain per Canonical Memory authority, with one durable per-authority serialization anchor, is materially stronger than check-then-write or an unproven cross-service coordinator. The ADR correctly preserves D and Storage as separate semantic authorities while sharing only the physical serialization substrate; I's PolicyDomain sequencer, C's provider sequencer and the COC quorum log remain independent.

However, the current ADR is not yet a complete L1/L2 contract. The shared transaction domain is named, but the authority that executes cross-owner writes is not defined. The protected-transition list may also be narrower than D/E's lifecycle contract, particularly around lease/attempt/source-read/execution boundaries and late dependency/terminal updates. Cross-BrainAuthority operation scope and the exact I COMMIT_WON crash/revocation semantics also need explicit constraints.

**Decision:** keep Option A selected as the v1 logical candidate, but downgrade the ADR's blanket "L1 CLOSED" statement to **L1 CONDITIONALLY ACCEPTED** until the P1 clarifications below are incorporated and independently reviewed. No database product selection, production deployment, performance PASS or fault-campaign PASS is implied.

Option A 是三个 ADR 选项中正确的 v1 方向。每个 Canonical Memory Authority 使用一个 Serializable Transaction Domain 和一个持久化 per-authority Serialization Anchor，明显优于 Check-then-write 或未经证明的跨服务协调器。ADR 正确地将 D 与 Storage 保持为不同语义权威，只共享物理序列化底座；I PolicyDomain Sequencer、C Provider Sequencer 和 COC Quorum Log 仍独立。

但当前 ADR 还不是完整的 L1/L2 合同：共享事务域已经定义，但跨 Owner 写事务由谁执行尚不明确；受保护转换清单可能窄于 D/E 生命周期合同，尤其是 Lease/Attempt/Source Read/Execution 边界、迟到 Dependency 和 Terminal 更新；跨 BrainAuthority 操作范围以及 I COMMIT_WON 崩溃/撤销语义也需要明确约束。

**决议：** 保留 Option A 作为 v1 逻辑候选，但在下列 P1 澄清纳入 ADR 并完成独立复审前，将“L1 CLOSED”降为 **L1 CONDITIONALLY ACCEPTED**。这不代表选择了数据库产品、生产部署、性能 PASS 或故障演练 PASS。

## 2. What is sound in Option A / Option A 已成立的部分

1. **One anchor per BrainAuthority.** A single anchor row and append-only transition record establish one physical serialization point per Canonical Memory authority, rather than one installation-wide global counter.
2. **D/Storage semantic separation.** D owns ProducerClass, ProducerWork admission, ForgetFence, lineage/dependency completeness, PublicationParticipant and D terminality. Storage owns PREPARED_HIDDEN, VisibilityPointer, Storage outcome, PublicationReceipt and outbox durability. The physical anchor does not grant Storage D policy authority.
3. **Fence/participant race has two legal outcomes.** Fence-first rejects/quarantines; participant-first makes the exact participant visible in the D barrier. There is no admitted-but-unaccounted participant.
4. **Private prepare is safe.** PREPARED_HIDDEN may exist before D admission because it has no public pointer or serving capability. It cannot be made visible without the final D/I/Storage proof join.
5. **I/C/COC remain independent.** I COMMIT_WON is an I-issued authorization fact; C Provider Outcome remains C-owned; COC remains a quorum causal/recovery log and not the JF-10 coordinator.
6. **Lost ACK is addressed by stable identity.** The same SerializationTransitionRef + digest resolves an ambiguous commit; same ref/different digest is an integrity incident.
7. **Restore/failover fail closed.** Unknown DB incarnation, old-primary fencing or missing transition history leads to RESTORE_FENCED/UNKNOWN.
8. **L1 vs L4 is correctly separated in principle.** A logical topology can be decided before a DB engine, deployment, operator or physical fault campaign is selected.

These principles are compatible with D's normative requirement that producer admission and ForgetFence installation share a linearizable order, and with E's requirement that registration precede queue/lease/execution and that source reads, execution, dependency registration and publication revalidate current I permission and D fence.

## 3. P1 architecture clarifications / P1 架构澄清

### A-01 — Cross-owner transaction executor and write-authority boundary is unspecified
**Severity:** P1 · **Level:** L1/L2 · **Owners:** A, D, Storage

Option A requires one DB transaction to update both D owner-authoritative records and Storage owner-authoritative records. The ADR says the anchor is Storage-owned physical metadata and is not D authorization, but does not define who opens/owns the transaction, how D authorizes its row mutations, or how Storage is prevented from directly minting or rewriting D semantic records.

Required contract:
- Define the transaction executor/coordinator (or shared transaction-context capability) and its trust boundary.
- D must authorize/sign the exact D semantic mutation and expected D state; Storage may only commit the physical transaction containing that authorized mutation.
- Storage DB credentials must not permit arbitrary D ledger mutation; D credentials must not mint Storage VisibilityPointer/PublicationReceipt.
- The commit receipt must prove the exact D and Storage records plus anchor transition committed atomically, without merging issuer identity or semantic authority.
- If the services are separate processes, specify the actual shared transaction API/context; do not assume two independent service transactions can become one atomic transaction.

Without this, “same transaction domain” is a deployment slogan rather than an implementable authority-preserving protocol.

### A-02 — D fence-sensitive lifecycle transitions are not fully mapped to the anchor
**Severity:** P1 · **Level:** L1/L2 · **Owners:** A, D, E, Storage

D's ForgetFence contract says no derivative-capable producer may enqueue, lease, dereference protected source payload, execute, retry, DLQ-replay or publish before durable D ProducerWork registration. E further requires current I permission and D fence/lineage revalidation at every source-read, execution, dependency-registration and publication boundary. The anchor transition list currently names ProducerWork admission, dependency-set registration, PublicationParticipant admission, Fence installation, Storage final visibility and NO_PUBLICATION, but does not explicitly classify:
- Attempt/Lease acquisition or replacement;
- retry/DLQ/replay/restore reactivation;
- protected source-read and execution permits;
- late dependency expansion or recompile child registration;
- D CompleteProducerWork / ResolveProducerWork / barrier terminalization.

Required contract:
- State which are pure local operations on an already admitted WorkItem and which change D inventory/barrier membership or authorize a protected effect.
- Any transition that can add new affected work, dependency, attempt, lease, replay capability or publication possibility must be serialized with the same per-authority anchor (or be explicitly covered by an already admitted immutable WorkItem barrier record).
- Define the exact fence-generation/anchor-revision check for a source-read or execution permit, including a fence racing between check and actual read/execute.
- Define how late-discovered dependencies invalidate/reopen a prior barrier snapshot and how no delayed writer can survive terminal NO_PUBLICATION.

This is not a request to put every CPU instruction under a DB lock. It is a requirement to make the effect-permit and inventory-membership linearization points explicit.

### A-03 — Cross-BrainAuthority operation scope is unstated
**Severity:** P1 · **Level:** L1 · **Owners:** A, D, Storage

The anchor is per BrainAuthorityRef, but the ADR explicitly blocks cross-PolicyDomain atomicity without explicitly saying whether one PublicationOperation/ForgetOperation may span multiple BrainAuthorityRefs.

Required contract:
- v1 operation scope is exactly one BrainAuthorityRef per atomic publication/fence transaction; or
- if multi-BrainAuthority operations are required, specify a separate coordinator, ordering and partial-completion/restore semantics.

Do not infer cross-authority atomicity from one anchor per authority. Global Forget may fan out into independently fenced per-authority operations, but its global completion proof must remain separate and composable.

### A-04 — I COMMIT_WON receipt consumption and revocation race needs an explicit crash rule
**Severity:** P1 · **Level:** L2 · **Owners:** I, D, Storage

The ADR consumes I's single-use CommitAuthorizationReceipt before the Storage final visibility transaction. It says only COMMIT_WON proceeds, but should explicitly state the meaning after consumption:
- COMMIT_WON reserves authorization for one exact PublicationOperationId/tuple and is not retroactively revoked by a later revocation event;
- replay of the same receipt/tuple after crash returns the same COMMIT_WON result and cannot authorize another tuple;
- REVOCATION_WON forbids visibility;
- crash after COMMIT_WON but before Storage commit remains unresolved until the same Storage operation resolves to COMMITTED_VISIBLE or authoritative NO_PUBLICATION;
- UNKNOWN/IN_DOUBT never authorizes visibility.

Otherwise a reader may interpret “current permission at final gate” as requiring a second, differently ordered I read that can race or consume a second receipt.

### A-05 — Anchor transition history, incarnation and restore anti-rollback need a composable proof
**Severity:** P1 · **Level:** L2/L3 · **Owners:** Storage, D, I

The ADR correctly requires append-only transition records, DatabaseIncarnationRef, old-primary fencing and RESTORE_FENCED on uncertainty. It does not yet define the exact snapshot/root/checkpoint that proves the anchor revision and all transitions survive failover/PITR without rollback or fork.

Required contract:
- Define the durable anchor transition log root/checkpoint and monotonic incarnation transition.
- Define old-primary fencing evidence and single-writer ownership.
- Define how a restore reconciles anchor revision, transition records, D owner ledger and Storage participant/outcome records before reopening writes.
- If any part is missing or forked, the affected BrainAuthority remains RESTORE_FENCED.

This is an L2/L3 proof obligation; the physical drill is L4.

## 4. P2 consistency and documentation findings / P2 一致性与文档问题

### A-06 — ADR contains a stale pre-addendum “no option selected” statement
Section 3 says “no option is selected by this ADR”, while §8.1 later selects Option A and §8.6 calls L1 closed. The addendum says it supersedes the old disposition, but Section 3 itself is not visibly marked historical. Mark Sections 1–7 as the pre-addendum decision state or replace the stale sentence with a clear reference to §8.

### A-07 — Map T1–T8 to L1/L2/L3/L4 explicitly
The ADR says L1 is closed, but its earlier gate table still leaves owner-approved transaction diagram, deterministic race tests, atomic outcome proof, read-path enforcement and owner decisions open. Add a gate mapping:
- L1: logical topology and authority boundaries;
- L2: exact owner transaction contract and proof composition;
- L3: deterministic reference model/concurrency/fault vectors;
- L4: selected engine, deployment, operator, HA/PITR and physical drills.
This prevents “L1 closed” from being read as “the topology is fully accepted and all architecture gates are closed”.

### A-08 — Anchor contention is an explicit v1 tradeoff, not a hidden defect
One anchor row per BrainAuthority is correctness-first and may be a hotspot. The ADR correctly forbids sharding without successor proof. Performance benchmarking belongs to L4; no throughput claim is made here.

## 5. Required concurrency/reference-model proof / 必需并发参考模型

Before L3 acceptance, build a deterministic model covering at least:

1. D RegisterProducerWork vs InstallForgetFence (both commit orders).
2. D DependencyRegistration vs InstallForgetFence (including late-discovered dependency).
3. D Attempt/Lease/Retry/Replay/Restore activation vs InstallForgetFence.
4. D PublicationParticipant vs InstallForgetFence.
5. I CommitAuthorizationReceipt COMMIT_WON vs REVOCATION_WON, including lost ACK and crash before Storage final commit.
6. Storage final VisibilityPointer commit vs InstallForgetFence.
7. Storage NO_PUBLICATION vs delayed writer/retry/lease resurrection.
8. Anchor CAS serialization failure and same-transition retry.
9. Lost commit ACK followed by exact transition lookup.
10. Primary failover, stale old primary, DB incarnation change and restore with missing/forked transition records.
11. D barrier close vs late dependency/attempt/derivative discovery.
12. Read path/cache/index event before and after VisibilityPointer commit.

Every scenario must assert not just final status but the exact serialization revision, transition record, D fence generation, I PolicyDomain position, Storage outcome and visible-pointer state. Cross-domain counters are never numerically compared.

## 6. Gate disposition / Gate 裁决

| Gate | Current disposition |
|---|---|
| L1 logical Option A direction | **CONDITIONALLY ACCEPTED** — P1 A-01/A-02/A-03 must be clarified |
| L2 exact D/Storage transaction and I receipt composition | **OPEN** — A-01/A-04/A-05 |
| L3 concurrency/reference-model/fault evidence | **OPEN** — Section 5 matrix not yet evidenced as executed |
| L4 DB engine/deployment/operator/HA/PITR/physical drills | **OPEN / DEFERRED** |
| Protocol freeze | **NOT AUTHORIZED** |
| Production activation | **NOT AUTHORIZED** |

## 7. Final A disposition / A 最终结论

**CONDITIONAL ACCEPT OF OPTION A AS THE V1 LOGICAL TOPOLOGY; L1 NOT FULLY CLOSED; DO NOT FREEZE.**

Option A should remain the chosen v1 direction. Option B is not an automatic fallback and requires a successor ADR with equivalent proof; Option C remains rejected. Before A can declare the logical topology fully closed, resolve A-01 through A-05 in the ADR and obtain fresh D/Storage/I/C exact reviews where their authority contracts are affected.

The current Storage v3.2.9 bundle and A's earlier v3.2.8 integration review do not replace this topology review. The latter is a separate A-role technical simulation, not independent human A Owner approval.

**有条件接受 Option A 作为 v1 逻辑拓扑；L1 尚未完全关闭；不得冻结。**

Option A 应继续作为 v1 方向。Option B 不是自动后备方案，必须通过后继 ADR 证明等价安全性；Option C 继续拒绝。A 宣布逻辑拓扑完全关闭前，必须在 ADR 中解决 A-01 至 A-05，并在受影响的 Owner 权威合同上取得 D/Storage/I/C 新的精确复审。

当前 Storage v3.2.9 Bundle 及 A 对 v3.2.8 的旧集成审查不能替代本次拓扑审查。本文件仍是 A 角色技术模拟，不是独立人类 A Owner 批准。

## 8. Evidence and provenance / 证据与来源

- Storage/D topology ADR: Blob bb544ba2f346bdc130d524bd5c7310d86f367988.
- Storage v3.2.9 manifest: Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3.
- Storage v3.2.3 normative body: Blob 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792.
- D ForgetFence/Producer Admission contract: Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5.
- E lifecycle contract: Blob 4fb9e58511941f59b4d777336f8f85ad88ecccf1.
- H authority-join mapping: Blob 1cbe74eba69325510d6b1019d971661f965eabf8.
- C per-authority anchor review: commit ab260fcc34d1b460156c99fbfcdc7291e49e3443.
- D refreshed anchor review: commit c00afeee0dfb71d15f2839f15c217496a0087636.
- I refreshed anchor review: commit ae209389b4ebb78a878ed5ea9084562cae26fd92.
- A v3.2.8 exact integration review: commit 0bb77a3df8023ef0a5e27d79a0a9c49509a5b3f7 (does not replace this v3.2.9/topology review).
- H local full-path CI: run 44069777296, 32 tests, with deterministic I/D/Storage callback doubles.

All Owner reviews in the cited branches are delegated role simulations in this coordinating workflow. No independent human Owner or governance approval is claimed.


## 9. Post-review exact-currentness correction — Storage v3.2.9 is superseded by later Owner updates
## 9. 审查后精确当前性修正 — Storage v3.2.9 已被后续 Owner 更新超越

After this review snapshot, the live Owner branches advanced again:

| Owner | Latest branch HEAD | Exact change after v3.2.9 manifest |
|---|---|---|
| C | 81f1e81307315a31c3bbeae17eb801e8a4f47e10 | Corrected H Unified schema pin in the Phase 3.8.18 full-path review |
| H | 362cc113cfb5b595a4002a6f6e980d19ae2d2d15 | Updated exact CI binding to run 44069941327, tested commit ba2c9341fee4eb9ca9e665c74bdd37b4675dd251, job 133993324484 |
| D | 7d01732521a8b9db202f10cde2c2547e50071d58 | Corrected H Unified schema pin in the D full-path/clearance review |
| I | a68bb3587fe88aa72398e2dc8d136f94cee9a63f | Corrected H Unified schema pin in the I full-path/terminal review |
| Storage | 39a1e0429f6b4b08c6c437c8e3f5ace582a7315f | v3.2.9 manifest remains the current Storage branch manifest; it has not yet rebound the post-v3.2.9 review/CI updates |

Storage v3.2.9 Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3 still pins the earlier C/D/I full-path review Blobs 4be9c1cd8f116086bab58340f07e38ddfc223e21 / ccdae9b45affb23c6741b5cceb27004b35a8e03e / 7c65650a37c8c0f270451fb0419e93259fc38151 and the earlier H run 44069777296 / commit 9eb06313e94e762f0fde4a606633a6dbe1bf8262. The latest Owner branches have corrected those exact review pins and H CI binding. Therefore v3.2.9 is no longer the current exact review bundle, even though its source schema/mapping design remains the same.

**A-09 — Storage exact manifest is stale against current Owner review/CI Blobs**
- Severity: P1 · Level: L2
- Required: Storage publishes a successor manifest (v3.3.0 or equivalent) binding the corrected current C/D/I review Blobs, current H CI run/commit/job and current H source/CI closure Blob. C/H/D/I re-review that same exact successor manifest; A then performs final integration review on the successor.
- Do not call v3.2.9 jointly current or frozen. This is an exact-currentness/provenance gap, not a demonstrated semantic regression.

**A disposition update:** Option A topology review remains valid against ADR Blob bb544..., but the Storage bundle integration portion must be refreshed against the successor manifest before the overall B→A review can be considered current. The topology A-01–A-05 clarifications remain unchanged.

中文：本次审查快照之后，Owner 分支再次推进。C/D/I 分别修正 Full-Path Review 中的 H Schema 精确 Pin；H 将 CI 绑定更新到 Run 44069941327 / Commit ba2c934... / Job 133993324484。Storage v3.2.9 仍绑定旧 C/D/I Review Blob 和旧 H CI Run，因此虽然 Schema/Mapping 语义没有显示回退，v3.2.9 已不再是当前精确 Review Bundle。

**A-09：Storage 精确 Manifest 相对当前 Owner Review/CI Blob 已过期。** Storage 必须发布后继 Manifest（v3.3.0 或等效版本），绑定修正后的 C/D/I Review Blob、当前 H CI Run/Commit/Job 和 H Source/CI Closure Blob；C/H/D/I 对同一后继 Manifest 复审，随后 A 再做最终集成复审。这是精确当前性/来源证明缺口，不是已证明的语义回退。

**A 裁决更新：** Option A 拓扑审查对 ADR Blob bb544... 仍有效；但 Storage Bundle 集成部分必须基于后继 Manifest 重新审查。A-01 至 A-05 的拓扑澄清仍不变。
