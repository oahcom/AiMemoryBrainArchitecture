# Phase 3 — B→A Protocol Convergence and Storage Topology Integration Review
# 第三阶段 — B→A 协议收敛与 Storage 拓扑集成审查

- Reviewer perspective: A — Principal Integration Architecture (delegated role simulation)
- Review date: 2026-11-17
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review branch: `review/a-b-to-a-protocol-topology-2026-11-17`
- Base: `main` at `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Scope: B first (C/H/D/I exact protocol joins), then A (Storage/D serialization topology)
- Status: **B = L1/L2 CANDIDATE WITH EXACT-PIN GAPS; A = CONDITIONAL L1 ARCHITECTURE ACCEPTANCE; SYSTEM FREEZE = NOT READY**
- Provenance: this is a delegated integration-review artifact, not an independent human A Owner signature or any other Owner approval.
- English and Chinese are normative peers.

---

## 1. Executive decision / 执行结论

### B — Protocol convergence

The previous apparent C/H version drift has materially progressed. The current candidate pair is:

- BMCP Unified **1.2.14**, wire family **1.3.0**;
- immutable CSubmitOutcome **1.0.1**;
- RecoveryJoin **1.0.2**;
- RecoveryCutoff **1.0.5**.

H has published an exact 1.2.14 → C 1.0.1 mapping. C has re-reviewed that mapping and accepted it as an L1/L2 candidate. D has accepted the 1.2.14 D-specific ForgetFence high-water carrier and its RecoveryJoin crosswalk as an L1/L2 candidate. C and H candidate CI evidence is reported and the H provider-outcome job was read back as SUCCESS, 22/22 tests.

**B is not yet a single fully current cross-owner bundle.** The H mapping still pins an older D crosswalk Blob; the corrected D crosswalk now pins the corrected H schema Blob. H's mapping status still says C review is required even though the exact C re-review exists. The current I P0 addendum has corrected its H schema pin, but the H review of that P0 and the I review of the Storage anchor still cite the prior I P0/H schema bundle. Storage v3.2.4's successor manifest still carries older C/H 1.0.0/1.2.11-era references.

### A — Storage/D topology

Storage has now selected **Option A: one logical serializable transaction domain and one durable per-Canonical-Authority serialization anchor** as the normative v1 *logical* topology. I has accepted the anchor concept with strict PolicyDomain separation.

A finds Option A to be the strongest and simplest v1 architecture candidate for the project's modular-monolith direction. It keeps D and Storage semantic authority separate while giving their fence/admission/final-visibility transitions one physical linearization substrate.

This is **conditional L1 acceptance only**. D has not yet issued an exact decision on the Storage topology ADR itself. The ADR has an internal stale sentence that still says no option is selected. The transaction API/row-write boundary and an independently verifiable anti-rollback witness for database restore need to be specified. Physical engine selection, deployment, HA/PITR, read-path enforcement and fault campaigns remain L4 OPEN.

**Overall disposition: ACCEPT OPTION A AS THE V1 LOGICAL TOPOLOGY CANDIDATE WITH ENUMERATED BLOCKERS — DO NOT FREEZE.**

---

## 2. Exact source snapshot / 精确源快照

### 2.1 Owner branch heads

| Owner | Exact branch | Current HEAD commit | Latest relevant evidence |
|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `71dea4964a15d5a770567fdc5be97ef4b054b038` | Phase 1.F review of Storage v3.2.7; historical relative to current ADR/manifest |
| C | `session-c-agent-integration-2026-11-16` | `07faa308e4b7eb441fa69867a5e259df06b6be15` | Phase 3.8.16 exact re-review of H 1.2.14 mapping |
| D | `session-d-memory-brain-2026-11-16` | `3d6066977d2213ef6757ac23716937d6b43dd447` | Phase 3.8.7 exact H 1.2.14 / RecoveryJoin review |
| H | `session-h-bmcp-protocol` | `837b9b8909b3ecad47ad499070135ad2d7cda6b6` | Phase 3.8.11 mapping; final RecoveryCutoff Blob pin corrected |
| I | `session-i-security-governance-2026-11-16` | `c5e332f1654819b237285e42f61922701efadc8e` | Current I P0 successor and Phase 3.8.11 Storage-anchor review |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `01f2cc30b6e483f4afeed16106774a67f02e0185` | Phase 3.8.2 topology ADR with Option A addenda through §8.7 |

HEADs were read from the named live branches. The review does not treat old A review conclusions or old Storage manifest pins as current merely because they remain in branch history.

### 2.2 Exact artifacts

| Owner | Path | Blob SHA | Review meaning |
|---|---|---|---|
| H | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.14.schema.json` | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Corrected Unified 1.2.14 schema; wire 1.3.0 |
| C | `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C object schema 1.0.1 |
| H | `08-bmcp-protocol/phase-3.8.11-h-exact-mapping-unified-1.2.14-c-submit-outcome-1.0.1.md` | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` | Exact H wire/object mapping candidate |
| C | `07-agent-integration/phase-3.8.16-c-exact-rereview-h-mapping-1.2.14-csubmitoutcome-1.0.1.md` | `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c` | C accepts the exact H mapping candidate |
| C | Phase 3.11.1 explicit sequence-namespace amendment (exact Blob; path not resolved in this readback) | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | Adds signed `sequence_namespace_ref`; exact schema 1.0.1 |
| I | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` (not restored on main; see AID-2026-107 §10) | `44986f5f864bcdc1a79d34978273644d381a68c0` | Current I P0 successor; now pins corrected H schema 1.2.14 |
| I | `09-security-governance/phase-3.8.11-i-review-storage-serialization-anchor.md` (not restored on main; see AID-2026-107 §10) | `b3df8ae7f82a4c7ddc38568a965f8d39cecfad45` | I accepts Option A with strict PolicyDomain separation; its P0 pin needs refresh |
| D | `03-memory-brain/phase-3.8.7-d-exact-review-h-1.2.14-recoveryjoin-1.0.2.md` | `55ae7bc33b37f0e729949fdd2a694eb6211bbc55` | D accepts current H 1.2.14 / RecoveryJoin 1.0.2 carrier as L1/L2 candidate |
| D | Phase 3.8.6 RecoveryJoin P0 crosswalk (exact Blob; path not resolved in this readback) | `c4adf827dd62d44c43b8e871dec4835581508adf` | Corrected D crosswalk now pins H schema Blob `09fcd1...` |
| Storage | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `bb544ba2f346bdc130d524bd5c7310d86f367988` | Option A selected at L1; physical engine/deployment L4 OPEN |
| Storage | `reviews/storage-consistency/phase-3.6.14-storage-v3.2.4-successor-exact-version-binding-manifest.md` | `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7` | Published successor manifest, but its C/H pins are now stale |
| A | `reviews/architecture-feasibility/phase-1f-a-exact-integration-review-jf10-storage-v3.2.7.md` | `85cd97bb66461440c7c08c4397e6cd496217b6fd` | Prior A review targets v3.2.7 / older mapping; not a current review of ADR Blob `bb544...` |

### 2.3 CI evidence readback

- H provider-outcome run **44067666900**, exact tested commit `9892c21b9311fa08976c4b24c34fe87a509a71ea`: provider-outcome job **SUCCESS**, all steps completed. C's exact re-review records **22/22 tests**.
- C candidate run **44059935858**: 19 tests reported successful in the C 1.0.1 amendment and I's review.
- H's earlier RecoveryJoin/HRC run **44051851164**: job SUCCESS; the manifest records 266 passed, 22 skipped, 0 failed. Skipped historical fixtures are not counted as passed.

These are bounded candidate schema/reference-model/crypto-vector tests. They do not prove production profile registration, trust-root/key custody, a live C sequencer, provider-side-effect truth, authoritative same-key lookup, production H callbacks, COC quorum durability, Storage transaction topology or distributed crash recovery.

---

## 3. B — protocol integration review / B 阶段协议集成审查

### 3.1 What is now coherent

1. **Version pair:** H Unified 1.2.14 / wire 1.3.0 and CSubmitOutcome 1.0.1 are explicitly bound.
2. **C object immutability:** C 1.0.1 adds required `sequence_namespace_ref`; it is included in C-P0 and changes the digest/signature. Version 1.0.0 remains historical and cannot be silently interpreted as 1.0.1.
3. **Sequence namespace:** I accepts the namespace as a required signed C field. H must compare C outcome namespace, C key-status event namespace and the same durable C sequencer. No timestamp or unrelated counter may substitute.
4. **Provider outcome truth:** C owns ProviderAttempt/Gate/Request/Idempotency Namespace, Outcome and SideEffectStatus. H validates and joins; H cannot infer provider truth from an enum.
5. **D high-water:** D owns `forget_fence_generation_high_water`; it is distinct from D GateGeneration, BarrierGeneration, I PermissionEpoch, C sequence, COC position and Storage serialization revision.
6. **Candidate test evidence:** H's 22/22 candidate suite was read back as SUCCESS; it remains bounded evidence only.

### 3.2 Exact-pin gaps that prevent B closure

**B-01 — H mapping still pins the predecessor D crosswalk. P1 / L1-L2.**

H mapping Blob `c196fd...` binds D crosswalk Blob `bf35b7...`, which itself pins the earlier H schema Blob `fee452...`. D's current Phase 3.8.6 crosswalk is Blob `c4adf...` and pins corrected H schema Blob `09fcd1...`. H's mapping must be revised to the current D crosswalk; because the H mapping Blob will change, C must re-review that successor mapping. The old C acceptance of Blob `c196fd...` does not automatically transfer.

**B-02 — I P0 current source and H review are not on one exact pin. P1 / L1-L2.**

I's current P0 successor is Blob `44986f...` and pins corrected H schema `09fcd1...`. The H review artifact Blob `daf3ea...` still references older I P0 Blob `35e684...` and H schema Blob `fee452...`. The two H schema Blobs differ only in two descriptive strings (top-level artifact description and common-envelope schema-version description), not in schema constraints; nevertheless, the exact-version governance rule requires a refreshed H review against the current exact Blob. I's Storage-anchor review Blob `b3df8a...` also names the old I P0 Blob `35e684...`; I must refresh that exact reference after H review.

**B-03 — H mapping disposition is stale. P2 / L1.**

H mapping Blob `c196fd...` still says C review is required, while C has published Phase 3.8.16 Blob `f2d33a...` accepting that exact mapping as a candidate. H should publish a closure/currentness addendum recording the C review and H CI readback. This status correction does not itself authorize freeze.

**B-04 — Storage successor manifest is stale. P1 / L1.**

Storage manifest v3.2.4 Blob `6fc0be...` still references C 1.0.0 / H 1.2.11-era contracts and describes the C/H migration as open. It does not bind the current H mapping `c196fd...`, C re-review `f2d33a...`, corrected D crosswalk `c4adf...`, current I P0 `44986f...`, current D review `55ae7b...` and current I anchor review `b3df8a...` as one exact successor bundle. Storage must publish a successor exact-version manifest after the upstream pin corrections; do not hand-edit the Owner branch from this A review.

**B disposition:** the core C/H candidate mapping is coherent, but the integrated C/H/D/I/Storage evidence bundle is **NOT YET CURRENT / NOT JOINTLY ACCEPTED**. No protocol freeze.

---

## 4. A — Storage/D serialization topology review / A 阶段 Storage/D 拓扑审查

### 4.1 Option A is the right v1 logical candidate

Storage ADR Blob `bb544b...` selects one logical SERIALIZABLE transaction domain per `BrainAuthorityRef`, with one durable `CanonicalAuthoritySerializationAnchor`. The anchor binds `BrainAuthorityRef`, `SerializationDomainRef`, `DatabaseIncarnationRef`, monotonic `serialization_revision`, and the last transition identity/digest. Every protected transition updates the anchor and appends a transition record in the same transaction as the relevant D or Storage owner record.

The protected set includes:
- D ProducerWork admission/registration before E queue, lease, protected-source dereference or execution;
- complete direct/transitive dependency-set registration;
- D PublicationParticipant admission;
- D InstallForgetFence / ForgetFenceGeneration advancement;
- Storage final VisibilityPointer + COMMITTED_VISIBLE outcome + PublicationReceipt + outbox;
- authoritative Storage NO_PUBLICATION terminal outcome.

This is a strong architecture choice because the D fence/admission/publication race is resolved in one physical serialization domain rather than a cross-service coordinator protocol. Option C (check-then-write, queue, process mutex or outbox-only ordering) is correctly rejected. Option B is not a casual fallback; it requires a successor ADR with its own durable coordinator and failure proof.

### 4.2 Authority boundaries remain correct

- D alone owns ProducerWork, dependency/lineage, ForgetFence, PublicationParticipant and D terminality.
- Storage alone owns PREPARED_HIDDEN, VisibilityPointer, Storage visibility outcome, PublicationReceipt and outbox durability.
- I remains the sole authority for PermissionEpoch, authorization, revocation order and its single-use CommitAuthorizationReceipt in its own PolicyDomain sequencer.
- C remains the provider handoff/outcome authority.
- COC remains a separate quorum-ordered causal/recovery log; it is not silently folded into the D/Storage transaction or made an XA participant by implication.

I's exact anchor review accepts Option A only with strict PolicyDomain separation: I COMMIT_WON is a pre-commit proof; I post-outcome terminal proof follows the exact Storage outcome; the Storage anchor cannot decide COMMIT_WON/REVOCATION_WON; multi-PolicyDomain atomicity remains unsupported/blocked.

### 4.3 Required corrections and missing proof obligations

**A-01 — Stale statement inside the Storage ADR. P1 / document consistency.**

ADR §3 still says “Therefore no option is selected by this ADR”, while §7 labels the earlier disposition historical and §8 selects Option A as the normative v1 logical architecture. §8 says it supersedes the earlier no-selection phrase, but §3 is not itself marked historical. Storage should amend §3 to explicitly label it as the pre-addendum position, so the current normative decision is unambiguous.

**A-02 — D must review the exact Storage anchor contract. P1 / Owner adoption.**

D's current Phase 3.8.7 review accepts the H 1.2.14 D Fence high-water carrier and RecoveryJoin crosswalk. It does not accept the exact Storage ADR Blob `bb544b...` or the shared-anchor write/transaction contract. The ADR's own T8 gate requires D, I, Storage and A decisions. Obtain a fresh D exact-Blob decision on the Storage anchor and transaction boundary; do not infer it from D's schema/crosswalk acceptance.

**A-03 — Shared transaction API and row-write ownership are underspecified. P1 / L2.**

The ADR says D and Storage owner-authoritative rows and the Storage-owned anchor/transition record are updated in the same transaction. It must specify the modular-monolith transaction boundary without collapsing semantic ownership:
- one per-authority transaction/UoW capability supplied by the Storage persistence boundary;
- D may submit only D-owned state transitions and Storage only Storage-owned state transitions;
- the shared anchor update is a narrowly scoped physical serialization operation, not a generic cross-module write permission;
- transaction retry must reuse the same immutable transition ref/digest;
- no module may directly write another module's canonical rows or mint another Owner's receipt.

This is a contract/API clarification, not a reason to abandon Option A.

**A-04 — Database restore anti-rollback needs an independent witness. P1 / L2.**

The anchor row and append-only transition table are stored in the same transaction domain. A stale PITR/backup restore can roll both back together and may appear internally consistent. The ADR requires RESTORE_FENCED when history is uncertain, but must specify how a stale restore is detected. Require an independently durable, monotonic checkpoint/witness for the latest committed `SerializationTransitionRef` + digest and `DatabaseIncarnationRef` (or an equivalent non-rollbackable authority). It must be outside the restored database failure domain. Do not compare its sequence numerically with D/I/C/COC counters. If the witness is unavailable or mismatched, restore remains fenced/UNKNOWN.

**A-05 — COC/JF-10 composition must remain explicitly separate. P1 / L2-L3.**

Option A solves the D/Storage visibility serialization boundary; it does not create cross-log atomic commit with I or COC. The JF-10 PreparedTransactionGID / DB-incarnation same-XID bridge remains distinct from StorageVisibilityParticipantRef. The exact sequence must continue to state which COC Batch/Manifest and JF-10 proofs are prerequisites to D/I release, which are pre-commit proofs, and which are post-outcome records. No COC acceptance may substitute for I/D/C/Storage truth, and unresolved cross-log joins remain held.

**A-06 — Physical feasibility is still L4 OPEN.**

No actual database product/version/configuration, DB adapter, canonical-authority deployment, HA/PITR topology, old-primary fencing, production operator/on-call, authoritative read path or measured anchor contention profile is selected. PostgreSQL 18.7 JF-10 capability probes are not proof that Option A's serializable transaction domain is deployed or conforms. The selected engine must prove:
- serializable (or formally equivalent strict-serializable) anchor transactions;
- durable commit acknowledgement and same-operation lost-ACK resolution;
- old-primary fencing and authoritative read-after-commit;
- restore continuity plus independent anti-rollback witness;
- protected reads cannot use stale replicas/cache/object URLs before pointer commit;
- D Fence-first and participant-first races, crash windows and restore rollback behave as specified.

### 4.4 A integration disposition

**CONDITIONAL ACCEPTANCE:** Option A is accepted as the preferred v1 *logical* serialization architecture candidate. This review does not claim independent D/I/Storage/A Owner approval, a selected DB engine, physical linearizability, deployment, JF-10 closure or production readiness.

Option B is not a fallback that can be silently activated. If the chosen engine cannot satisfy Option A, the project must return to an explicit successor ADR and prove Option B's coordinator, durability, split-brain, recovery and operator model.

---

## 5. Combined blocker register / 综合阻塞登记

| ID | Severity | Level | Owner(s) | Required closure |
|---|---|---|---|---|
| B-01 | P1 | L1-L2 | H, D, C | H mapping pins current D crosswalk; C re-reviews successor mapping |
| B-02 | P1 | L1-L2 | I, H | H re-reviews current I P0 against H schema 1.2.14 Blob 09fcd; I refreshes anchor review |
| B-03 | P2 | L1 | H | Update mapping status with exact C review and CI readback |
| B-04 | P1 | L1 | Storage, A-I | Publish successor manifest binding all current exact source/consumer/review Blobs |
| A-01 | P1 | L1 | Storage | Mark §3 no-selection text as historical; align with §8 Option A decision |
| A-02 | P1 | L1 | D | Exact D review of Storage ADR Blob bb544... |
| A-03 | P1 | L2 | D, Storage, A | Define scoped shared transaction/UoW and anchor row-write ownership |
| A-04 | P1 | L2-L3 | Storage, I, A | Define independent anti-rollback witness for anchor/DB incarnation across restore |
| A-05 | P1 | L2-L3 | D, I, Storage, H | Explicitly join COC/JF-10 with Option A without cross-log atomicity or authority synthesis |
| A-06 | P1 | L4 | Storage, Engineering, A | Select engine/deployment and prove physical transaction, HA, restore and read-path properties |

---

## 6. Required next sequence / 后续执行顺序

### B closure first

1. H publishes a successor exact mapping pinning D crosswalk Blob `c4adf...`, current I P0 Blob `44986f...` and the corrected H schema Blob `09fcd1...`; H updates its review status.
2. H publishes an exact review of current I P0 Blob `44986f...` against H schema Blob `09fcd1...`.
3. C re-reviews the successor H mapping Blob; I refreshes its anchor review to the exact current P0/H review pair.
4. Storage publishes a successor exact-version manifest that binds the current H/C/D/I source and consumer artifacts and the Storage ADR.
5. A performs a fresh exact-bundle integration review. Old C acceptance of a changed H mapping does not transfer.

### A closure second

6. Storage resolves the §3/§8 wording contradiction.
7. D issues an exact decision on the shared-anchor transaction contract.
8. D/Storage specify the scoped transaction/UoW API and owner row-write permissions.
9. Storage/I define the independent anti-rollback witness and restore-fencing evidence.
10. A re-reviews the exact successor bundle; only then can the project assess whether the L1 topology gate is ready to close.

### Gates that remain open regardless

- JF-10 P0, persistent COC Gate B and deterministic physical Gate C;
- R1 Recovery Cutoff Batch completeness and R2 owner-local gate linearization/release;
- C/I profile registration, trust roots, key custody, historical verification and anti-rollback deployment;
- provider-specific same-key lookup and actual multi-replica egress race/fault tests;
- Full Applied evidence chain, Global Forget completion and physical restore anti-resurrection;
- B Fact/Claim ADR and the remaining system-wide security/governance blockers;
- L4 database/cluster/read-path/operator selection and physical conformance.

No schema freeze, implementation authorization, merge, deployment, provider activation or production readiness is claimed.

---

## 7. Final verdict / 最终结论

**B:** The H 1.2.14 / C 1.0.1 protocol candidate is materially converged and has bounded CI evidence, but exact D/I cross-pins and the Storage successor manifest are not yet aligned. Keep it as a candidate; do not freeze.

**A:** Option A is the right v1 logical topology candidate. The per-authority anchor is a materially stronger and more precise design than the previous unspecified topology. Accept it conditionally, subject to D's exact decision, transaction API/ownership clarification, independent restore anti-rollback and exact bundle refresh. Physical engine/deployment remains L4.

**SYSTEM:** **NOT READY FOR ARCHITECTURE FREEZE.** The project should proceed B → A exactly as requested: close exact protocol joins first, then complete the logical topology's remaining owner and proof obligations, then separately prove physical feasibility.

**中文结论：**

**B：** H 1.2.14 / C 1.0.1 协议候选已实质收敛，并有有限 CI 证据；但 D/I 精确交叉绑定与 Storage 后继清单尚未对齐。保持候选状态，不冻结。

**A：** Option A 是 v1 最合理的逻辑拓扑候选。每 Authority Serialization Anchor 比此前未选定拓扑的设计更明确、更强。建议有条件接受，但必须补齐 D 精确决议、Transaction API/Owner 写权限边界、独立 Restore Anti-Rollback 证明和精确版本包更新。物理引擎/部署仍属 L4。

**系统：** **尚不具备架构冻结条件。** 严格按 B→A 推进：先关闭协议精确 Join，再关闭逻辑拓扑 Owner/证明义务，最后独立验证物理可行性。



---

## 7. Owner execution packet and dependency order / Owner 执行包与依赖顺序

This section converts the findings into exact Owner-scoped work. It is a coordination specification, not permission for this review role to write to Owner branches. Each Owner must make its own changes on its own branch, publish a successor artifact, and provide exact branch HEAD, commit SHA, Blob SHA, and CI evidence. No approval is inferred from task assignment.

本节将审查发现转化为精确的 Owner 任务。它是协调规范，不授权本审查角色写入 Owner 分支。每个 Owner 必须在自己的分支上完成修改、发布后继工件，并提供精确 branch HEAD、commit SHA、Blob SHA 与 CI 证据。不得因任务分配而推定批准。

### Wave 1 — B exact protocol pins / 第一波 — B 协议精确绑定

| Order | Owner | Required action | Required evidence / exit condition |
|---|---|---|---|
| 1 | H | Publish successor to mapping Blob `c196fd...`; replace predecessor D crosswalk `bf35b7...` with current D crosswalk `c4adf827dd62d44c43b8e871dec4835581508adf`; pin H schema `09fcd1fa29fe24255fbd87cae79dafb406594a59`; update C review status truthfully. | New mapping path + Blob; exact source pin table; mapping status no longer says C review required for a predecessor mapping; H CI run/commit readback. |
| 2 | C | Re-review the exact successor H mapping Blob from step 1; do not reuse acceptance of predecessor Blob `c196fd...`. | New C review naming exact H mapping Blob, disposition and any conditions; candidate CI run and tested commit. |
| 3 | H | Publish a fresh H review of current I P0 Blob `44986f5f864bcdc1a79d34978273644d381a68c0` against H schema Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`; supersede stale review `daf3ea...`. | New H review with exact I P0 + H schema Blob pins and explicit scope/limitations. |
| 4 | I | Refresh Storage-anchor review after step 3; replace stale I P0 pin `35e684...` with `44986f...` and bind the new H review Blob. | New I review Blob; explicit PolicyDomain separation; no cross-domain atomicity implied. |

### Wave 2 — A topology closure / 第二波 — A 拓扑收敛

| Order | Owner | Required action | Required evidence / exit condition |
|---|---|---|---|
| 5 | Storage | Amend ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`: label §3 no-selection text as historical; preserve §8 Option A as current normative v1 logical decision; specify scoped transaction/UoW capability, row-write ownership, retry identity and independent restore anti-rollback witness. | Successor ADR Blob; explicit API/ownership contract; restore witness failure behavior (unavailable/mismatch => RESTORE_FENCED/UNKNOWN); no DB engine or L4 claim unless separately evidenced. |
| 6 | D | Review the exact successor Storage ADR Blob and transaction/UoW contract; explicitly decide D-owned row writes, anchor operation scope, D Fence/admission/publication race ordering and any objections. | D exact-Blob decision (ACCEPT / CONDITIONAL / REJECT), assumptions, unresolved items and evidence; do not substitute H carrier review for this decision. |
| 7 | H, D, I, Storage | Jointly reconcile COC/JF-10 ordering with Option A while retaining separate authority/logs. | Exact sequence showing pre-commit proofs, post-outcome records, participant identities and fail-closed UNKNOWN behavior; no XA or cross-log atomicity claim. |
| 8 | Storage | Publish a successor exact-version binding manifest only after steps 1–7 settle. Bind current C/H/D/I/Storage source, consumer-review and CI artifacts, including the exact successor H mapping, C re-review, D crosswalk/review, current I P0/H review/I anchor review and Storage ADR. | Manifest Blob with no stale predecessor pins; explicit supersession ledger; CI and branch-head readback. |
| 9 | A (integration) | Re-read all named Owner branch HEADs and exact successor Blobs; re-run B→A integration and contradiction review. | Updated integration report and gate matrix; no inferred Owner acceptance; retain NOT READY if any required proof is absent. |

### Required execution semantics / 执行语义

1. **Strict sequence:** H mapping successor → C exact re-review; H review of current I P0 → I anchor-review refresh; Storage ADR successor ↔ D exact review; Storage manifest only after all upstream pins settle.
2. **No cross-Owner writes:** A/integration may coordinate and review but must not commit to H/C/D/I/Storage Owner branches or rewrite their artifacts.
3. **Exact-version invalidation:** any changed source Blob invalidates downstream reviews that cite the predecessor Blob. Re-run only the affected downstream review chain, but never silently transfer approval.
4. **No gate laundering:** schema CI, reference-model tests, document existence, delegated role simulation or draft PR status cannot close physical, production, owner-approval or architecture-freeze gates.
5. **No merge or freeze:** PR #52 remains Draft. This report and its execution packet do not authorize merge, Owner branch merge, implementation, deployment or production activation.

1. **严格顺序：** H mapping 后继版本 → C 精确复审；H 对当前 I P0 的复审 → I 更新 anchor review；Storage ADR 后继版本 ↔ D 精确审查；所有上游 pin 稳定后 Storage 才能发布 manifest。
2. **禁止跨 Owner 写入：** A/集成角色可以协调和审查，但不得向 H/C/D/I/Storage Owner 分支提交或改写其工件。
3. **精确版本失效：** 任一源 Blob 变化，引用旧 Blob 的下游审查即失效。只重跑受影响的下游链，但不得静默继承批准。
4. **禁止 Gate 洗白：** Schema CI、参考模型测试、文档存在、委托角色模拟或 Draft PR 状态，均不能关闭物理、生产、Owner 批准或架构冻结门禁。
5. **禁止合并或冻结：** PR #52 保持 Draft。本报告及执行包不授权合并、Owner 分支合并、实现、部署或生产启用。

### Stop conditions / 停止条件

Stop the chain and retain the affected item as BLOCKED if: (a) a named exact source Blob cannot be read; (b) a successor review omits its exact predecessor Blob; (c) an Owner rejects or materially conditions the contract; (d) a required witness/authority is unavailable; (e) any workflow resolves UNKNOWN as success/abort/terminality; or (f) the physical transaction/restore proof is asserted without reproducible evidence.

如出现以下任一情况，停止依赖链并将相关事项保持为 BLOCKED：(a) 无法读取指定精确源 Blob；(b) 后继审查未列明其精确前序 Blob；(c) Owner 拒绝或对契约提出实质条件；(d) 所需 witness/authority 不可用；(e) 任一工作流将 UNKNOWN 解释为成功/中止/终态；(f) 未提供可复现证据却宣称物理事务/恢复证明成立。
