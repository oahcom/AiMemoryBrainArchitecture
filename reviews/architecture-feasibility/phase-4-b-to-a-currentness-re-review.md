# Phase 4 — B→A Currentness Re-review and Conditional Integration Decision
# 第四阶段 — B→A 当前性复审与条件性集成裁决

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review date: 2026-11-17
- Reviewer perspective: A — delegated integration review; not a human Owner signature
- Base: `main` at `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- Branch: `review/a-b-to-a-currentness-reconciliation-2026-11-17`
- Scope: re-review newer Phase B PR #51, Phase A PR #54, and final A assessment PR #57; exact live readback of v3.3.0, Option A ADR and C/D/I anchor reviews
- Status: **B = CONDITIONALLY ALIGNED CANDIDATE, SAME-MAPPING ACCEPTANCE STILL OPEN; A = OPTION A ACCEPTED AS LOGICAL DIRECTION, A-01..A-05 NOT ADOPTED; SYSTEM = DEFERRED / NOT READY**
- Language: English and Chinese are normative peers.

---

## 1. Executive decision / 执行结论

### B — protocol

Storage v3.3.0 is real and its exact manifest Blob `c8407c9f10049d65426a3598ad20b6aa70f83c32` was fetched from the live Storage Owner branch. It explicitly supersedes the v3.2.7/v3.2.8/v3.2.9 manifest lineage for current candidate-bundle binding and records H Unified 1.2.14 / wire 1.3.0, RecoveryJoin 1.0.2, RecoveryCutoff 1.0.5 and CSubmitOutcome 1.0.1, with H 42-test CI and C/D/I role-review artifacts.

This resolves the **old v3.2.9 currentness problem at the manifest-publication level**. It does not close B completely. The Phase B closure plan still explicitly records that C has not reviewed H's integrated authority-join mapping Blob `1cbe74eba69325510d6b1019d971661f965eabf8`; C's earlier Provider Outcome-only review is not acceptance of the integrated I/D/Storage verifier seams. The v3.3.0 manifest's C review row describes C-P0 projection/mutation and nullable-COC candidate review, not an explicit C decision on that exact integrated mapping. The manifest itself says A review is required and is not jointly accepted/frozen.

**B disposition: CONDITIONALLY ALIGNED at L1/L2 candidate level against v3.3.0; exact integrated-mapping acceptance and same-bundle Owner disposition remain OPEN.** Do not call B frozen.

### A — Option A topology

The exact Storage topology ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988` selects Option A as the v1 logical direction. The current D, I and C anchor reviews have now been read directly:
- D review Blob `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a` accepts the anchor as D Fence/Participant ordering substrate.
- I review Blob `f22d31dec3a95f094c2942ab816c830f007e830e` accepts it with strict PolicyDomain separation.
- C review Blob `9e280ff6b3850871de118186b03d4831a5c259e9` accepts it while retaining C sequencer/outcome separation.

This corrects the earlier Phase 3 report's statement that D had not reviewed the exact baseline ADR. D has reviewed that exact ADR Blob. However, none of these reviews adopts the later A-01..A-05 amendment proposal Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`. The proposal explicitly remains NOT ADOPTED. The baseline ADR still has a stale “no option is selected” statement in §3, and the normative transaction/EffectPermit/scope/receipt/restore details remain incomplete.

**A disposition: ACCEPT OPTION A AS THE V1 LOGICAL DIRECTION WITH CONDITIONS; A-01..A-05 remain OPEN; L1/L2 not fully closed; L3/L4 OPEN.**

### System

PR #57's current A decision is **DEFERRED / ARCHITECTURE_NOT_READY**. It permits bounded preparatory work only; no Gate is passed and no protected-path implementation, deployment or production activation is authorized. This remains the correct overall outcome.

---

## 2. Exact evidence snapshot / 精确证据快照

| Item | Exact reference | Current review meaning |
|---|---|---|
| Current main | `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` | Verified current main base for this review |
| Phase B PR #51 | head `e1f02639709502549439f67bcd1497a0cde8f6c4`; branch `review/arch-consol-002-protocol-alignment-2026-11-17` | Draft; v3.3.0 candidate and B closure plan |
| Phase A PR #54 | head `208c5e84f64ec68338045b963407bcb6d2463faf`; branch `review/arch-consol-003b-storage-topology-a-2026-11-17` | Draft; Option A review and unadopted amendment proposal |
| Final A PR #57 | head `d354ec41937731d8b606ca4791b968cfdc72d474`; base `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` | Draft; overall DEFERRED disposition |
| Phase B closure plan | Blob `c07bae49aaacd12509f5fe5502da344b63f9d20e` | Explicitly says C has not reviewed integrated H authority-join mapping |
| Storage v3.3.0 manifest | Blob `c8407c9f10049d65426a3598ad20b6aa70f83c32` | Current candidate exact-bundle manifest; A review required |
| Storage topology ADR | Blob `bb544ba2f346bdc130d524bd5c7310d86f367988` | Option A selected at logical level; stale §3 text and L1/L2 gaps remain |
| Option A amendment proposal | Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525` | Proposal only; NOT ADOPTED |
| Phase A review | Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3` | Conditional Option A acceptance; A-01..A-05 and L3/L4 open |
| D anchor review | Blob `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a` | Exact baseline ADR accepted as D Fence/Participant substrate; not approval of unadopted amendment |
| I anchor review | Blob `f22d31dec3a95f094c2942ab816c830f007e830e` | Strict PolicyDomain separation; I trust/receipt/restore gates remain open |
| C anchor review | Blob `9e280ff6b3850871de118186b03d4831a5c259e9` | C sequencer/outcome remains separate; not explicit acceptance of H integrated mapping `1cbe...` |
| FINAL-A-002 EN | Blob `86f5d31372260d7556310330549a5b34bb3649a0` | Overall DEFERRED; scoped conditional approvals only |

The source files above were fetched from their named live branch/ref or PR branch. The report does not treat PR body summaries as a substitute for exact artifact readback.

---

## 3. B — exact protocol findings / B 阶段精确协议发现

### B-01 — v3.3.0 fixes manifest lineage, but does not itself close same-bundle acceptance
**Severity: P1 · Level: L1/L2 · Owners: C, H, D, I, Storage; A integrates**

v3.3.0 resolves the earlier v3.2.9 stale-manifest condition and reconciles the v3.2.7/v3.2.8/v3.2.9 lineage. Its own status remains “A review required; not jointly accepted / not frozen”. Its C/D/I review table binds local candidate review artifacts; the table does not convert delegated role simulations into independent human Owner approvals.

**Required:** A reviews exact v3.3.0; each relevant Owner records acceptance of the same exact candidate bundle or clearly limits its acceptance to its local artifact. Do not describe manifest publication as joint Owner approval.

### B-02 — C review of H integrated authority-join mapping remains unproven
**Severity: P1 · Level: L1/L2 · Owners: C, H**

The Phase B closure plan Blob `c07bae...` explicitly says H has two distinct mappings:
- Provider Outcome mapping Blob `7739d8159b32702024583669f40974a80801782b`;
- integrated authority-join mapping Blob `1cbe74eba69325510d6b1019d971661f965eabf8`, which adds I terminal, D clearance and Storage resolution verifier seams.

The earlier C Provider Outcome-only review does not accept the integrated mapping. The v3.3.0 manifest lists C review Blob `61ff3716c9c3d3101a0058963c58f089aa1448b0` for C-P0 projection/full mutation/nullable COC semantics; the manifest's own accepted-scope description does not establish that C reviewed exact mapping `1cbe...`. C's anchor review Blob `9e280...` also pins a different H mapping Blob `579dd2a91edf47b86e744e897ba6668b839944bd`, and is an anchor-separation review, not a review of `1cbe...`.

**Required:** C must issue an exact review naming mapping Blob `1cbe...`, H schema `09fcd...`, C schema `a631...`, validator `eab961...`, test source `da1454...`, and the exact I/D/Storage callback semantics. H must state separately which mapping is used for Provider Outcome-only validation and which for integrated authority joins. The successor review must not inherit approval from the older mapping.

### B-03 — 42 tests are bounded local candidate evidence
**Severity: P1 · Level: L1/L2 evidence ceiling · Owners: H, C, D, I, Storage**

Manifest v3.3.0 pins H run `44072037563`, commit `c6faee294e503f32a802ba51f3f3b3eb4bee2cd7`, job `134000402978`, with 42 tests (36 H validator + 6 Python/Node C crypto interop). This is meaningful local candidate evidence for schema, duplicated-field equality, C-P0 mutation rejection, sequence namespace and local fail-closed callback predicates.

The same manifest explicitly states that I/D/Storage authority callbacks are deterministic test doubles. It does not authenticate production Owner-signed proofs or prove production trust roots/key custody, provider issuer truth, adapter send-vs-close/lost-ACK/failover, COC quorum durability, same-GID physical recovery, JF-10, Global Forget, Full Applied or production activation.

**Required:** Preserve this evidence ceiling. Separate the later unmocked authority-proof integration and physical fault evidence from the 42-test local suite.

### B disposition

**CONDITIONALLY ALIGNED candidate only.** The earlier v3.2.9 staleness finding is superseded by v3.3.0; B-02 integrated mapping review and explicit same-bundle Owner acceptance remain open. No protocol freeze.

---

## 4. A — Option A topology findings / A 阶段 Option A 拓扑发现

### A-01 — Shared transaction executor and row-write authority
**P1 · L1/L2 · Owners: Storage, D**

The amendment proposal defines per-owner immutable Mutation Commands and a shared transaction context that atomically commits authorized D mutation, Storage mutation, anchor CAS and transition append. This is a useful proposal, but the live Storage ADR Blob `bb544...` does not normatively define the executor API, credential/capability boundary or DB-role enforcement. The proposal is NOT ADOPTED.

**Required:** Storage publishes an ADR successor adopting or rejecting the exact clause; D reviews exact successor. Specify that the executor cannot mint D/Storage semantic decisions or receipts and that each module can mutate only its own canonical rows.

### A-02 — D fence-sensitive lifecycle and EffectPermit coverage
**P1 · L1/L2/L3 · Owner: D; Storage implements substrate**

The proposal extends the protected set to Attempt/Lease, Retry, Replay, Restore/Rebuild/Backfill, late dependency expansion and D terminalization, and defines a typed EffectPermit. The current D anchor review accepts the anchor as ordering substrate but explicitly leaves row schemas, full dependency pagination and late-discovery fault campaign OPEN. It does not adopt the full EffectPermit/lifecycle proposal.

**Required:** D owns the normative lifecycle/EffectPermit decision; Storage supplies the physical ordering primitive. Define permit issuance/consumption linearization against InstallForgetFence, late-dependency barrier reopening, and why NO_PUBLICATION cannot become terminal while delayed work can still publish.

### A-03 — One BrainAuthority per atomic v1 operation
**P1 · L1/L2 · Owners: D, Storage, I**

The proposal explicitly prohibits cross-BrainAuthority atomicity in v1 and requires Global Forget fan-out into independent per-authority fences plus complete inventory/terminal proofs. The baseline ADR's “one domain per Canonical Memory authority” is not a complete cross-operation scope rule. This remains a proposal.

**Required:** Adopt exact single-authority scope, define global fan-out/partial completion and prevent any global coordinator from inferring completion from a partial set.

### A-04 — I COMMIT_WON receipt crash/revocation/replay semantics
**P1 · L2 · Owner: I**

I's current anchor review preserves PolicyDomain separation and states that COMMIT_WON is a pre-commit proof and post-outcome terminal proof follows Storage's exact outcome. It does not fully specify single-use tuple binding, replay after crash, or the unresolved COMMIT_WON-before-Storage-commit recovery outcome proposed in PR #54.

**Required:** I must adopt the immutable tuple binding and exact replay semantics; Storage must resolve the same operation to COMMITTED_VISIBLE or authoritative NO_PUBLICATION. UNKNOWN/IN_DOUBT never authorizes visibility.

### A-05 — Anchor restore anti-rollback witness
**P1 · L2/L3 · Owners: Storage, I, D**

The proposal requires a verifiable transition checkpoint/root, database incarnation continuity, old-primary fencing and owner-ledger reconciliation. However, the proposal still does not identify the independent durable witness service/storage, its failure domain, monotonicity mechanism, authentication and recovery procedure. A checkpoint stored only in the database being restored can roll back with that database.

**Required:** Specify a witness outside the restored DB failure domain, or an equivalent non-rollbackable authority. If unavailable, stale, forked or mismatched, remain RESTORE_FENCED/UNKNOWN. Then execute restore/failover vectors.

### A-06 — ADR §3 conflicts with §8
**P1 · L1 document consistency · Owner: Storage**

The live ADR §3 still says “Therefore no option is selected by this ADR”, while the later §8 addendum selects Option A. The later addendum's precedence note does not make the earlier normative sentence safe for readers who consume §3 in isolation.

**Required:** Mark the earlier no-selection paragraph as historical/pre-addendum or replace it with an explicit reference to the current §8 decision.

### A disposition

**Option A remains the correct v1 logical direction and has baseline D/I/C acceptance with their stated authority boundaries.** The five normative clarifications remain unadopted; D's acceptance of the baseline anchor is not D's acceptance of the PR #54 proposal. L1/L2 are not fully closed. L3 reference-model/concurrency/fault proof and L4 engine/deployment/HA/PITR/operator proof remain OPEN.

---

## 5. Cross-PR currentness and governance / 跨 PR 当前性与治理

1. PR #51 and PR #54 are Draft review artifacts whose merge base is historical `b372b62c...`; compared with current main `8c0c5b11...`, PR #51 is 32 commits ahead / 26 behind and PR #54 is 26 ahead / 26 behind. PR #52 is 3 ahead / 26 behind. Their reports remain useful evidence, but they are not current-main-integrated changes and must not be merged without a fresh source-delta/rebase review.
2. PR #57 is based on current main `8c0c5b11...`, but FINAL-A-002 explicitly says it has not completed a source-by-source delta audit against that main; G1 remains PARTIAL. It also retains B-01..B-04 as conditions, including the old v3.2.9 manifest condition. That specific v3.2.9 publication requirement is superseded by v3.3.0; the residual condition should be rewritten as fresh A review plus exact integrated-mapping and same-bundle Owner closure.
3. All C/D/I anchor reviews and the v3.3.0 manifest identify delegated role simulation/provenance, not independent human Owner signatures. Do not upgrade them to formal governance approval.
4. No existing PR, Owner branch, or main was modified by this re-review. It is a new isolated A review branch only.

---

## 6. Ordered next actions / 后续执行顺序

| Order | Owner | Action | Exit evidence |
|---|---|---|---|
| 1 | H | Separate Provider Outcome mapping from integrated authority-join mapping; pin current exact schemas, validator and CI; correct status text | H successor mapping/closure Blob and exact CI run/commit/job |
| 2 | C | Review exact integrated mapping Blob `1cbe...` (or H successor) rather than only Provider Outcome mapping | C exact-Blob review with explicit ACCEPT/CONDITIONAL/REJECT and scope |
| 3 | D, I | Confirm their current reviews cover the exact integrated mapping and v3.3.0 source bundle; refresh only if exact dependencies changed | D/I successor reviews naming exact predecessor Blobs |
| 4 | Storage | Keep v3.3.0 as current candidate manifest until upstream changes; publish successor only after exact mapping and owner reviews settle | New manifest with complete supersession ledger and no stale pins |
| 5 | Storage + D | Decide A-01/A-02/A-03 in a successor topology ADR | Exact successor ADR and D decision |
| 6 | I + Storage + D | Decide A-04/A-05 and independent restore witness design | Exact successor contract and failure/restore semantics |
| 7 | H/C/D/I/Storage | Reconcile COC/JF-10 ordering without cross-log/XA or cross-PolicyDomain atomicity claims | Exact sequence, participant identities and fail-closed recovery rules |
| 8 | A | Re-read current main and all Owner branches; update G1/G2/G6 and final A disposition | New exact-version integration ledger and explicit Gate decision |

### Stop conditions / 停止条件

Stop and retain BLOCKED if an exact Blob is unreadable; a review cites a predecessor Blob; an Owner rejects or materially conditions its authority contract; an external witness/authority is unavailable; UNKNOWN is treated as success/abort/terminality; or a physical/production claim lacks reproducible evidence.

Do not merge PR #51/#54/#57/#52, close Issue #43, pass a Gate, freeze schema/technology, authorize protected-path implementation, deploy or activate production on the basis of this review.

---

## 7. Final decision / 最终裁决

**B:** CONDITIONALLY ALIGNED candidate against Storage v3.3.0. The v3.2.9 manifest-currentness defect is superseded; C review of the exact integrated H authority-join mapping and same-bundle Owner closure remain OPEN.

**A:** Option A is accepted as the v1 logical direction with baseline D/I/C boundaries. A-01..A-05 are proposals, not adopted normative contract. ADR §3/§8 inconsistency remains. L1/L2 not fully closed; L3/L4 OPEN.

**SYSTEM:** **DEFERRED / ARCHITECTURE_NOT_READY.** Bounded preparatory work only. No Gate passed; no protected-path implementation entry, freeze, deployment or production activation.

**中文最终裁决：**

**B：** 基于 Storage v3.3.0 的 CONDITIONALLY ALIGNED 候选。v3.2.9 Manifest 当前性缺陷已被后继版本替代；C 对精确 H 集成 Authority-Join Mapping 的审查和同一 Bundle 的 Owner 闭环仍 OPEN。

**A：** Option A 作为 v1 逻辑方向获得接受，D/I/C 基础权威边界已有对应审查。A-01 至 A-05 仍是提案，尚未成为规范合同；ADR §3/§8 冲突仍存在。L1/L2 尚未完全关闭，L3/L4 OPEN。

**系统：** **DEFERRED / ARCHITECTURE_NOT_READY（延期 / 不具备架构冻结条件）**。仅允许有界准备工作。没有任何 Gate 通过；不授权受保护路径实现、架构冻结、部署或生产启用。
