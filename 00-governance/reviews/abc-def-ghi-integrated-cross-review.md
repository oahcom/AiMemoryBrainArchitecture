# Unified A–I Module Baseline Review & Cross-Module Reconciliation

- Review ID: P-UNIFIED-MBR-REVIEW-001
- Review date: 2026-11-17
- Prepared by: Session P — integration coordination and evidence audit
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review branch: `session-p-project-governance-baseline`
- Status: **PROPOSED REVIEW — NOT OWNER APPROVAL / NOT PROJECT G0 RATIFICATION**
- Scope: A–I module baseline proposals, ABC / DEF / GHI cross-module boundaries, evidence freshness, dependency closure and remediation.
- Authority boundary: This report may reconcile evidence and identify inconsistencies. It does not adopt any module baseline, resolve another Owner's ADR, approve I governance, freeze a shared contract, authorize implementation or merge branches.

## 1. Executive disposition

All nine Owner branches contain a module baseline/redlines proposal or equivalent proposal artifact. All nine artifacts are explicitly PROPOSED / Owner review required / not APPROVED. This is a successful first-round document submission, not a completed module-baseline acceptance gate.

The current evidence supports:
- module mission and authority boundaries are substantially documented across A–I;
- each proposal distinguishes owned semantics from non-owned semantics;
- B ADR-001 remains ADR-BLOCKED;
- D's JF-10 v2 acceptance is limited to D-owned semantics and enumerated exceptions;
- C/G/H Applied is not frozen to one shared version/digest;
- I governance and Global Forget completion remain blocked;
- implementation and conformance evidence remain separate from design review.

The current evidence does **not** support:
- any of the nine module baselines being APPROVED;
- project G0 ratification or PGA appointment;
- common C/G/H Applied contract freeze;
- production JF-10 closure;
- effective I security/governance policy or Global Forget completion;
- architecture freeze or merge authorization.

## 2. Live branch and artifact evidence

Branch HEADs below were re-fetched from GitHub during this review. Blob SHAs identify the exact module proposal files fetched from those branch refs. The branch HEAD and artifact blob are different identifiers and must not be conflated.

| Module | Owner branch | Live HEAD SHA | Baseline artifact | Blob SHA | Status |
|---|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `fb061aee907c28f7da198e68161ff57ebac160b7` | `reviews/integration/module-a-integration-governance-baseline-and-redlines.md` | `a43a8f2fa3d31681d64b79d584364fdae80f8866` | PROPOSED |
| B | `session-b-domain-model-phase3` | `861fa9b2c3e1f572336543b15c7dc392493891db` | `02-domain-model/module-b-domain-model-baseline-and-redlines.md` | `410d6cc62294e1a7ee5efa0cfe4ef496a8179326` | PROPOSED |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | `07-agent-integration/module-c-agent-integration-baseline-and-redlines.md` | `c79da952efaa490083c88ccb4608d62f526fcbae` | PROPOSED |
| D | `session-d-memory-brain-2026-11-16` | `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8` | `03-memory-brain/module-baseline-and-redlines.md` | `84e402f471d452c7dab63a7db344f86b5b57bd7c` | PROPOSED |
| E | `session-e-memory-compiler-2026-11-16` | `4402549c39824b89a0dc49973226187c62e056c5` | `04-memory-compiler/module-baseline-and-redlines.md` | `7f037a7684723fdbddd593b3d131c7c348e2ccbe` | PROPOSED |
| F | `session-f-memory-runtime` | `a370d9a3bc0bd35a21a12dfe87d53c298237de8e` | `05-memory-runtime/module-baseline-and-redlines.md` | `d4756cabda3151999cbe1ddde0adb554458004a1` | PROPOSED |
| G | `session-g-memory-context` | `72a8066b4401f9586fe10775d545384b82736f07` | `reviews/governance/g-module-baseline-and-redlines-proposal.md` | `fb2eb805be385469b5ab5f25c4ef76f234feb4c2` | PROPOSED |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` | `reviews/governance/h-module-baseline-and-redlines-proposal.md` | `a4d961ac7b7e1a5fdf59422a4ebe21a6db95ace1` | PROPOSED |
| I | `session-i-security-governance-2026-11-16` | `1fc3b3293ebf2077edfd6ad253647d382173d9fa` | `reviews/governance/i-module-baseline-and-redlines-proposal.md` | `b0493cf0366159c99536ee8847996916bc21c606` | PROPOSED |

The current A/C/F/G/H tips have advanced beyond earlier inventory snapshots. A, B and C baseline headers still cite older “prepared against” HEADs; those are historical source snapshots, not current branch tips. The technology reports also cite their reviewed source HEAD separately from their publication commits. This is not itself a semantic defect, but each report must explicitly distinguish source snapshot, report commit and current branch HEAD.

## 3. Template and structural conformity

The proposed 14-section template exists on the P coordination branch at:
`00-governance/module-baseline-and-redlines-template.md`, blob `408979f2125b67e7599118038b9a415a213399ee`.

It does **not** exist on `main` at the time of this review. The template on P is a governance proposal and is not yet an approved project-wide normative template.

Structural comparison:
- A has 13 second-level sections and lacks the template's distinct Section 14 evidence/version-history section.
- B and C each have 14 second-level sections.
- D, E and F each have 15 second-level sections; their numbering/section mapping needs a normalization check against the proposed template.
- G, H and I each have 14 second-level sections.

Action: retain the existing Owner documents as their own proposals; do not rewrite them centrally. Ask each Owner to map its current document to the proposed 14-section template after the project template itself is ratified or explicitly adopted for this rollout. At minimum, A must add a distinct evidence/version-history section; D/E/F must explain any additional section and ensure the required fourteen topics are all present.

## 4. ABC cross-review

### A — Integration Governance
A's baseline correctly limits A to integration coordination, evidence registries, dependency visibility and gate tracking. It explicitly denies A authority to override B–I or Storage semantics, approve project governance, or infer implementation/test acceptance.

Cross-review findings:
- A's integration baseline appropriately keeps Fact/Claim-dependent interfaces blocked by B ADR-001.
- A correctly requires the same exact Applied contract version and explicit C/G/H decisions.
- A's current baseline file was prepared against `f8b16ce08b3e1ab3b67e502a8f1d48702bd433a9`, while the live A branch HEAD is now `fb061aee907c28f7da198e68161ff57ebac160b7`. Keep the former as source provenance and add the latter as current publication/verification HEAD.
- A's phase 3.6 closure tracking file remains the authoritative integration workstream evidence register; its older internal source-snapshot table must not be mistaken for the current live branch inventory.

### B — Domain Model
B's baseline correctly owns logical domain semantics and typed reference meaning, not authentication, permission, wire encoding, canonical persistence or physical storage.

Cross-review findings:
- ADR-001 is explicitly ADR-BLOCKED; Option A is a recommendation only, not a decision.
- Principal/ActorRef/Issuer, ScopeRef, EnvironmentRef and permission binding require B/I/H alignment. Typed references alone do not authenticate an actor or grant authority.
- Consumer mappings are not consumer acceptance.
- B baseline's prepared-against HEAD is `0cf703a3...`; current B HEAD is `861fa9b2...`. Preserve provenance and record current HEAD.
- The 14-section document is structurally aligned with the proposed P template at heading-count level; Owner must still validate content completeness.

### C — Agent Integration
C correctly owns Agent-side telemetry and final inference-request boundary evidence, while G owns Applied, H owns protocol/transport evidence, I owns authorization and D owns ForgetFence.

Cross-review findings:
- C must not manufacture Applied or infer it from Delivered, Materialized or Submitted.
- C's final-request evidence must be cryptographically/integrity-bound to the exact final request, managed-region digest, session/Adapter/capability and current policy/fence predicates as required by the common profile.
- The C baseline prepared-against HEAD is `702263dee9...`; current C HEAD is `2e577602...`. The technology report's source HEAD is a separate snapshot and must be called out explicitly.
- C's technology review is a static architecture review; it does not prove Agent runtime hooks, request interception, or end-to-end Applied execution.

**ABC disposition:** authority boundaries are directionally consistent. No ABC contract freeze is granted. B ADR-001 and typed identity binding remain blockers; A must remain coordinator, not approver of B/C decisions.

## 5. DEF cross-review

### D — Memory Brain
D owns canonical memory and ForgetFence semantics, canonical cursor and producer barrier semantics. D does not own compiler work state, runtime index/cache, Context, Adapter protocol, I policy or Storage engine internals.

Current exact D decision is ACCEPT WITH ENUMERATED EXCEPTIONS for the single-I-PolicyDomain JF-10 v2 bundle, limited to D-owned ForgetFence, producer registration, dependency inventory, lineage and barrier semantics. This is architecture/interface acceptance only. It does not establish D implementation, durable ledger/locks, participant recovery, COC deployment, Storage physical correctness or production conformance. D36/JF10-01..13 and crash/fault suites remain NOT RUN; JF-10 P0 remains OPEN; multi-PolicyDomain atomicity remains BLOCKED.

### E — Memory Compiler
E owns compiler work/attempt/lease/retry/DLQ/replay, staging and derivative lineage. E does not own canonical Memory commit, I authorization, D fence, Storage visibility or G Context.

Cross-review findings:
- Staged/private artifacts must remain invisible until D registration/fence, current I authorization and Storage publication visibility all succeed.
- WorkItemId, AttemptId and LeaseId must remain distinct and fenced; retries/recompiles cannot escape root barrier accounting.
- E's module proposal must not imply that a chosen database or Storage capability probe constitutes production JF-10 acceptance.
- E's older database wording must be updated only to the extent supported by exact Storage evidence: PostgreSQL 18.7 is a capability-probe candidate with isolated single-node CI evidence; not a production Canonical Authority deployment decision.

### F — Memory Runtime
F owns retrieval, ranking, index/cache execution and runtime suppression/invalidation. It consumes D fences/cursors, I authorization, E publication state and G completeness/sufficiency but cannot redefine them.

Cross-review findings:
- Candidate backends (FTS5/Tantivy/ANN) remain candidates until workload benchmarks and deterministic rebuild/fence tests exist.
- Authorization and Forget filtering must occur before candidate emission and at final return; graph/provenance dereference must not bypass it.
- Cache TTL, capacity, latency SLO and technology freeze require measured workload evidence.
- F's technology report is static and conditional; it does not prove runtime suppression or index rebuild behavior.

### Storage / JF-10 evidence
The Storage branch contains the PostgreSQL 18.7 prepared-XID capability probe. PR #12 is closed; its description limits the probe to single-node CI and expressly excludes replication/failover, production restore, hardware durability, operator readiness and JF-10 P0 closure. PR closed state alone is not proof that every probe passed; the workflow run/result must be inspected before recording a pass.

**DEF disposition:** logical design responsibilities are coherent, and D's bounded architecture decision is real. The physical serialization/deployment, accountable operator, same-XID recovery/failover, atomic visibility and end-to-end crash/fault conformance remain OPEN. Do not repeat design review as if it were implementation validation.

## 6. GHI cross-review

### G — Memory Context
G owns Context membership/order/budget, ContextVersion, ChangeSet, reconciliation, delivery intent and authoritative Applied record. G consumes C final-request evidence, H delivery/materialization evidence, D canonical/Forget state, F retrieval completeness and I authorization.

Cross-review findings:
- Delivered, Materialized and Submitted are not Applied.
- Applied must bind exact ContextVersion, Delivery, inference request, Agent/session, Adapter identity/instance, CapabilityEpoch, PermissionEpoch, ForgetFenceGeneration, managed-region integrity and C-owned final-request submission evidence.
- G cannot declare canonical Forget or global erasure; Context removal is not Forget.
- G's technology report is a static conditional review. Persistence/recovery, token/window budget and Applied verifier negative tests remain unverified.

### H — BMCP Protocol
H owns wire envelope, versioning, compatibility, Adapter capability declarations, transport delivery receipts and reconnect/replay mechanics. H does not own Principal identity meaning, permission policy, Context Applied semantics, canonical Forget or global completion.

Cross-review findings:
- Payload ActorRef/source claims are not authenticated identity.
- JSON/RFC 8785 and HTTP/local IPC/gRPC remain candidates, not approved wire/transport decisions.
- ACK evidence is attempt- and target-scoped. Delivered is not Applied, local purge, suppression or global Forget.
- H36, SDK interoperability, generated schema, cryptographic binding and reconnect/fault tests remain NOT RUN.
- H's technology report is a static conditional review, not runtime interoperability certification.

### I — Security & Governance
I owns issuer trust, Principal/ActorRef authorization binding, delegation, PermissionEpoch, revocation, policy, Global Forget inventory/seal and completion/retention criteria.

Cross-review findings:
- I governance decisions I35-DEC and I36-GOV must remain Proposed/Governance-Blocked until named authorized approvers and exact effective policy versions are recorded.
- Inventory completeness needs a signed closed-world InventorySealReceipt and explicit target/exclusion/retirement treatment.
- External recipients, backups, restore targets and erasure exceptions need accountable owners and evidence.
- No downstream module can infer global completion from local ACK, Adapter purge, canonical tombstone or storage deletion.
- I's proposal must not imply that a candidate inventory contract is an operationally complete inventory.

**GHI disposition:** G/H Applied responsibilities are conceptually compatible but lack a common frozen schema/digest and explicit C/G/H acceptance. I authorization and global completion remain independent gates. No Applied or Global Forget freeze is granted.

## 7. Cross-group dependency reconciliation

| Contract / dependency | Authorities | Current disposition | Freeze condition |
|---|---|---|---|
| Fact / Claim semantics | B + designated ADR authority; affected consumers | ADR-001 ADR-BLOCKED | Formal ADR-001 decision with exact option, approver, timestamp, version and migration/consumer impact |
| Principal / ActorRef / Issuer / Scope / Environment binding | B + I + H; C/D/E/F/G consumers | OPEN / not fully accepted | Exact shared field semantics, authenticated transport binding, permission mapping, negative tests and each affected Owner's exact-version acceptance |
| JF-10 v2 single PolicyDomain | D + E + Storage + I; C/F/G/H consumers | D bounded architecture decision; engineering/governance OPEN | Named DB/platform operator, approved I sequencer interface, durable participant/visibility implementation, same-XID restart/failover recovery, atomic visibility, D36/JF10 and crash/fault tests |
| Applied proof / BMCP ACK | C + G + H; I/D/B predicate authorities | OPEN / not frozen | One schema/version/digest, explicit C/G/H acceptance, I/D/B predicate mapping, verifier and negative/transform/replay tests |
| Global Forget | I + D/E/F/G/H/Storage and external recipients/backups | GOVERNANCE-BLOCKED / operational evidence incomplete | Signed inventory seal, target-state matrix, external/backup/restore receipts, physical deletion evidence, approved exceptions and I36 governance approvals |
| Retrieval/backend technology | F + D/E/I/G/H consumers | Candidate only | Representative workload benchmark, authorization-before-emission tests, rebuild/fence and recovery evidence |
| BMCP wire/transport | H + B/I/C/G/D | Candidate only | Approved identity/profile dependencies, encoding/transport ADR, generated SDK interoperability and H36 tests |

## 8. Technology review coverage

Current technology architecture review reports found on Owner branches:
- C — Agent Integration Technology Architecture Review, static review / conditional.
- F — Memory Runtime Technology Architecture Review, static review / conditional.
- G — Memory Context Technology Architecture Review, static review / conditional.
- H — BMCP Protocol Technology Architecture Review, static review / conditional.

Owner-specific TAB-001 technology review coverage at the assigned paths under `reviews/technology/` is: C, F, G and H present; A, B, D, E and I not found on their current Owner branches. The four present reports are static/conditional owner reviews and must be refreshed against the current blueprint and any later Owner changes. The five missing reports are outstanding deliverables, not rejections. Do not infer a technical verdict for a missing report.

## 9. Required unified actions

1. Refresh source HEAD and blob SHA in every Owner artifact without overwriting historical provenance.
2. Each Owner records a specific decision on its own branch: ADOPT / ADOPT WITH EXCEPTIONS / REVISE / REJECT, exact proposal version and current branch HEAD. Session P cannot make this decision for them.
3. Normalize all nine documents against the proposed 14-section template after governance authority resolves whether the P template is the rollout standard.
4. B/ADR authority resolves ADR-001; B/I/H jointly pin typed identity and permission binding; consumers acknowledge exact versions.
5. C/G/H publish one Applied contract candidate with exact schema version and digest, then each records explicit acceptance; I/D/B predicate authorities confirm their fields without surrendering their own authority.
6. D/E/Storage/I finish JF-10 engineering and governance gates; inspect PR #12 workflow evidence and do not equate PR closure with probe pass.
7. I supplies governance approvals and signed Global Forget inventory/target-state evidence.
8. A updates the integration registry and gate vector only after exact evidence is present.
9. No architecture freeze, production sign-off or merge follows from this report.

## 10. Review verdict

**PASS WITH MAJOR OPEN BLOCKERS — DOCUMENTATION / BOUNDARY REVIEW ONLY.**

The nine module proposals are suitable as first-round review inputs. They are not yet approved module baselines. The cross-module architecture remains unfrozen. The highest priority is exact-version closure for Applied and typed identity, formal ADR-001 disposition, and JF-10 physical recovery/governance evidence. Global Forget remains I-governed and incomplete until its independent evidence gates close.

## 11. Explicit non-claims

This report does not:
- approve any A–I module baseline;
- resolve ADR-001;
- accept or freeze Applied, BIH identity or JF-10 as a production contract;
- approve I security policy or external governance;
- claim implementation, CI pass, conformance pass, production readiness or Global Forget completion;
- authorize branch merge, main modification or architecture freeze.


## 12. TAB-001 technology blueprint reconciliation (main refresh)

### 12.1 Mainline source snapshot

During this review, `main` advanced to `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`. The current TAB-001 source is:
- `13-engineering-decisions/technology-architecture-blueprint.md`, blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`, TAB-001 v0.1, **CANDIDATE SYSTEM-WIDE BLUEPRINT — NOT A TECHNOLOGY FREEZE**.
- `reviews/integration/tab-001-a-i-technology-architecture-review-task-pack.md`, blob `cf903cd5812cfed3a64a52b169a3bd84209ba3f5`.
- `reviews/technology/phase-1-a-i-technology-architecture-review-tasks.md`, blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`.
- `ARCHITECTURE_ROADMAP.md`, blob `29289361973ec4369f067706132190793cd57a6b`.

The task pack requires nine independent Owner reviews on the existing Owner branches, six dimensions R1–R6, exact reviewed branch HEAD and blueprint blob SHA, and one Owner-specific report at the assigned path. It explicitly says the task pack is not Owner acceptance, ADR approval or implementation sign-off.

### 12.2 Technology direction consistency

TAB-001's current candidate direction is a local-first Rust modular monolith, one transactional authority, content-addressed blob storage, rebuildable structured/lexical/vector indexes, bounded in-process cache, optional isolated inference worker, and versioned BMCP transport adapters. The blueprint explicitly keeps domain/Owner boundaries unchanged and all unvalidated technology decisions candidate/open.

This direction is broadly compatible with A–I's documented logical architecture. The following are not contradictions, but they are mandatory proof obligations:
- SQLite + WAL is recommended only as the first single-node prototype candidate; PostgreSQL is a comparison/evolution candidate. Neither is selected as the final production database.
- Storage's PostgreSQL 18.7 prepared-XID probe is a capability experiment, not a production database selection. It does not negate TAB-001's SQLite prototype recommendation, nor prove that SQLite can implement JF-10's required atomicity. A D/E/Storage spike must explicitly compare the exact required transaction/locking/recovery semantics across the candidate database profiles.
- TAB-001 itself states SQLite WAL alone does not prove the D/E Forget race contract and requires a real linearization point plus crash/race tests. This is the correct boundary and must remain a hard gate.
- FTS5 is a first lexical comparison candidate; Tantivy and vector ANN/sqlite-vec remain candidates requiring benchmark evidence.
- JSON, HTTP/local IPC, gRPC, cryptography/key custody, GPU/model backend and deployment splitting remain open or candidate and stay under H/I/affected Owner authority.
- 12–16 GB VRAM and host-RAM profiles are planning envelopes, not verified user hardware or performance claims. Actual hardware, workload, concurrency, corpus, RTO/RPO and SLOs remain unknown.

### 12.3 TAB-001 findings requiring action

| Finding | Severity | Owner(s) | Required closure |
|---|---|---|---|
| TAB-REV-001 — Storage candidate-to-JF-10 production binding gap | P0 | D, E, Storage, I | PostgreSQL 18.7 isolated CI capability suite is now 7/7 PASS; bind the suite to the actual canonical runtime/adapter, D/E/I ledgers, real reader path and production operations; keep final DB choice OPEN until this is evidenced |
| TAB-REV-002 — Exact Applied/identity dependencies remain upstream blockers | P0 | B, C, G, H, I, D | Same exact version/digest, typed identity/permission binding, final-request proof, verifier and negative tests |
| TAB-REV-003 — Five owner technology reports missing | P1 | A, B, D, E, I | Publish the five missing reports at assigned `reviews/technology/owner-*-technology-review.md` paths on their own branches |
| TAB-REV-004 — Four existing reports need source refresh | P1 | C, F, G, H | Reports currently cite reviewed source snapshots C `0a81f370...`, F `61814ec3...`, G `270ac553...`, H `6e7cb95f...`; compare each source-to-current delta and add a current-branch impact addendum. C/F/H report-only modifications should be identified as publication changes; G additionally added research artifacts |
| TAB-REV-005 — G context optimization research not yet reconciled to TAB-001 | P1 | G, A; B/C/D/E/F/H/I/Storage consulted by their contracts | G's NVIDIA impact assessment and candidate register are PROPOSED only; map the TSS, ObservationRef, compaction, six-axis fidelity, archive/recall, Forget invalidation and cost gate to TAB-001's Context, storage, inference and resource decisions. No implementation or baseline change inferred |
| TAB-REV-006 — Technology decision register needs owner dispositions | P1 | A coordinates; B–I decide own items | For TEC-001..018, capture accept/recommend/reject/defer/needs ADR, authority owner, source evidence and closure prototype; do not mark all recommendations approved |
| TAB-REV-007 — T0–T5 gates need explicit integration with A–I governance | P1 | A + Project Governance Authority when appointed | Map T0 owner review and T1–T4 prototypes to module/consumer/governance/test gates; T5 approval remains blocked until exact Owner decisions, ADRs and evidence exist |

### 12.4 G research addendum — context optimization

The live G branch advanced beyond its earlier technology-review source snapshot and now contains:
- `reviews/06-memory-context/nvidia-context-optimization-impact-assessment.md`, blob `3fb9f011e24c93a748442018d48c5954584e4f43`, 678 lines, RESEARCH ASSESSMENT / PROPOSED ONLY.
- `reviews/06-memory-context/context-optimization-implementation-candidates.md`, blob `eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b`, candidate register only.

The research's central architecture inference is to separate a compact forward-looking working state from immutable, selectively recallable evidence history, and to evaluate compaction at meaningful state boundaries under explicit economic and correctness gates. It recommends extending existing G components rather than creating a new subsystem.

The proposed candidates include boundary-triggered compaction evaluation, a dynamic economic decision record, conservative horizon/recovery-cost model, typed Task Semantic State (TSS), TSS lineage, six-axis fidelity validation, ObservationRef metadata, bounded exact range recall, compaction loss ledger, immutable ContextVersion per successful compaction, stale Snapshot/Delta rejection, expanded Forget invalidation, paired benchmark suites and held-out evaluation.

The research correctly marks these as PROPOSED / OPEN / NEEDS_CROSS_OWNER_APPROVAL / NOT_IMPLEMENTED. It explicitly rejects direct transplantation of SoL-Pi thresholds, treating summaries as canonical truth, importing Action Fusion into G, and bypassing D/I/H gates. It is research evidence and design input, not an approved G baseline or measured AiMemoryBrain performance result.

Cross-owner implications to retain:
- B: typed ObservationRef/source-reference and TSS schema semantics.
- C: task/subtask boundary signals and declared-versus-verified completion; no private chain-of-thought dependency.
- D/E/Storage: derivative producer registration, source lineage, dependency registration, atomic/recoverable publication and Forget races.
- F: exact range retrieval, completeness, recall cost/latency, index/cache invalidation.
- H: Snapshot/Delta representation, delivery, stale ACK and reconnect semantics.
- I: classification, authorization, retention, inventory and Global Forget.
- A: benchmark acceptance, evidence policy and architecture integration.

No candidate is promoted to DECIDED by this review.

### 12.5 Main/P branch divergence and integration safety

At the time of this refresh:
- `main` HEAD: `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`.
- P coordination branch HEAD before this addendum: `1d48297bf9449fded7450b61defb3f14f2533ace`.
- Comparing P against main reports P ahead by 30 and behind by 4; the four main-side commits add TAB-001 and its review/task material and update the roadmap.
- Comparing main against P identifies those four main-side changes as `13-engineering-decisions/technology-architecture-blueprint.md`, `reviews/integration/tab-001-a-i-technology-architecture-review-task-pack.md`, `reviews/technology/phase-1-a-i-technology-architecture-review-tasks.md`, and `ARCHITECTURE_ROADMAP.md`.

This is a genuine branch divergence, not a safe fast-forward. Do not merge or force-update either branch. Before any future PR/merge, reconcile the four main-side files into the P workstream through a reviewed, non-destructive integration and re-run the comparison. This report is on P and does not modify main.

## 13. Updated review verdict

**PASS WITH MAJOR OPEN BLOCKERS — MODULE DOCUMENT / CROSS-BOUNDARY REVIEW AND TAB-001 RECONCILIATION ONLY.**

The nine module proposals are valid first-round review inputs. The P governance proposal and TAB-001 remain candidates. Five of nine TAB-001 Owner technology review reports are missing; four existing reports are conditional and require source refresh against later branch movement. G's new context optimization research is valuable candidate input but is not yet cross-owner accepted. The system technology stack is not frozen; JF-10, Applied, ADR-001, identity binding and Global Forget remain blockers.



## 14. JF-10 Storage evidence reconciliation — 2026-11-17

The earlier review wording that Storage had only a single-node capability probe is superseded. The current Storage Owner branch is `a1fbbd15d3a7993bbb61821ad44957e4f69d3ed1`; its evidence dossier blob is `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1`. The executable conformance plan blob is `49056cd46fd30445c0e564c99e0e234f60f065c4`.

Seven PostgreSQL 18.7 GitHub Actions workflows completed SUCCESS on exact evidence commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`:
- Prepared-XID + restart: run 43955195289.
- Synchronous standby promotion: run 43955195323.
- Physical backup/restore: run 43955195219.
- Explicit-LSN WAL PITR: run 43955195388.
- Prepared-XID PITR + archive negatives: run 43955195460.
- Synchronous standby unavailable fail-closed: run 43955195197.
- Old-primary rewind/rejoin: run 43955195256.

Each run has a completed successful job and the probe step succeeded. The Storage dossier records detailed PASS markers, including prepared-XID and lock retention, same-XID resolution, pointer/receipt atomicity at PITR boundaries, and missing/corrupt/incomplete WAL fail-closed behavior. The current Storage HEAD is six commits ahead of the exact test commit and not behind it; the test evidence is correctly pinned to the earlier commit, not attributed to untested later source.

A dedicated Storage probe uses isolated `jf10_*` fixture tables, not production COC or I/D tables. The Storage dossier explicitly limits the evidence to engine capability under a pinned single-runner Docker CI profile. It does not prove the production Canonical Authority adapter, I sequencer/COC, D fence/lineage state, E publication state, production reader path, real infrastructure STONITH/split-brain prevention, operator/runbook or RPO/RTO.

The decisive remaining gap is now more specific: Storage's recursive tree audit found no production runtime source tree, Canonical Authority DB adapter, migration package or application deployment manifest in the inspected repository branch. The responsible Owner must identify the actual implementation repository/branch and exact runtime entrypoint, adapter and schema path, or explicitly designate this repository as implementation home and deliver those artifacts. Until then Gate A is **PARTIAL PASS / OPEN**, Gate B and C remain blocked, JF-10 P0 remains OPEN and production activation is NOT AUTHORIZED.

### 14.1 Database candidate consequence

The PostgreSQL 18 documentation describes a native external transaction-manager two-phase lifecycle: `PREPARE TRANSACTION` persists prepared state on disk, later sessions may `COMMIT PREPARED` or `ROLLBACK PREPARED`, and prepared transactions retain their locks. PostgreSQL also warns that long-lived prepared transactions can interfere with VACUUM and transaction-ID wraparound; the feature requires explicit `max_prepared_transactions` configuration.
- https://www.postgresql.org/docs/18/sql-prepare-transaction.html
- https://www.postgresql.org/docs/18/two-phase.html
- https://www.postgresql.org/docs/18/runtime-config-resource.html

SQLite WAL provides atomic commit and reader/writer concurrency on a same-host shared-memory arrangement, but SQLite documents one writer at a time. Its documented transaction/WAL interface is not the PostgreSQL external transaction-manager PREPARE/COMMIT PREPARED participant lifecycle.
- https://www.sqlite.org/wal.html
- https://www.sqlite.org/isolation.html

Therefore PostgreSQL 18.7 now has materially stronger direct evidence for the JF-10 prepared-participant requirement than SQLite + WAL. This does **not** select PostgreSQL for production. SQLite may remain a single-node candidate only if the Owners specify and prove an alternate durable participant/intent protocol that preserves the same JF-10 invariants without assuming native prepared-XID support. TEC-003/004 remain CANDIDATE / TO_VALIDATE until production adapter and operational evidence is bound.

The full bounded assessment is recorded at `00-governance/reviews/jf10-storage-evidence-assessment.md` on the P branch. It is Session P evidence reconciliation only, not Storage/D/E/I Owner acceptance or a database ADR.


## 15. CGH-APPLIED-1.1 exact Owner decisions and A tracker freshness correction — 2026-11-17

The initial Session P Applied assessment incorrectly marked C and H exact-version decisions as pending. That was based on stale/incorrect branch-artifact assumptions. The current live branch files were re-read and the exact A package/COC companion pair was verified:
- A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.
- Companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.

Live exact-pair decisions:
- C: `45a48249717c8cddb07ab96197730ef93d406c22` — ACCEPT WITH ENUMERATED EXCEPTIONS.
- D: `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2` — ACCEPT WITH ENUMERATED EXCEPTIONS.
- I: `5a5304d48aa912dcf6f817099bd5659371d8cdc8` — ACCEPT WITH ENUMERATED EXCEPTIONS.
- H: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` — ACCEPT WITH ENUMERATED EXCEPTIONS.
- G: `aa3afa73d8a76cc6f025839c52bfbff6a983046a` — ACCEPT WITH ENUMERATED EXCEPTIONS.
- B: `3a1e77889cd9a90cd5822d9f0cb3437880868706` — APPROVE; no B semantic type change.
- Storage: `a589d983ac145244962c22e5da3a55427aa35ff8` — CONFIRMED WITH CHANGES, architecture interface only.

Thus the exact CGH-APPLIED-1.1 recovery-batch package/companion design decisions are recorded. Applied Contract Frozen nevertheless remains NO: H schema is candidate/not generated/not interoperability-tested; COC operator/deployment remains undesignated; I sequencer, D barrier, C provider and G Applied runtime implementations are unverified; all owner conformance/race suites remain NOT RUN. JF-10 P0 and production activation gates remain open.

### 15.1 A integration tracker is stale against live Owner branches

A's current closure tracker blob `554d4b85a94f433856506dce4c020b9c00183e69` ends at §13.43. It records old C/D/I/H/G/B/Storage source pins and Storage branch head `df60b547...`, including the prior failing deep-PITR attempt. Current Storage branch HEAD is `3c8ab8ee4579a550300aa48aecab928149cf9370`, whose dossier blob `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1` records the corrected deep-PITR run and seven-workflow regression batch PASS on evidence commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`.

The A deployment-binding record correctly keeps Gate A PARTIAL PASS / OPEN and production deployment NOT DESIGNATED. A must refresh the detailed closure tracker and source pins; Session P cannot modify A's Owner record.

The full corrected exact-version decision vector is recorded in `00-governance/reviews/applied-contract-1.1-exact-version-reconciliation.md`.
