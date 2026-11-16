# Module Baseline & Redlines Rollout Tracking

- Tracking version: 0.1.0
- Updated: 2026-11-17
- Status: **FIRST-ROUND OWNER PROPOSALS SUBMITTED — FORMAL ADOPTION / CROSS-MODULE CLOSURE OPEN**
- Authority: Session P coordinates only. Each Module Owner owns authorship and decision of its module baseline.
- Project governance status: **PROPOSED / GOVERNANCE-OPEN**. No PGA appointment or formal G0 ratification is evidenced.
- Main baseline rechecked: `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`.

## Fresh branch inventory

The following are live branch-tip SHAs fetched from GitHub branch metadata on 2026-11-17. They are branch HEADs, not merely file blob SHAs.

| Module | Owner branch | Fresh HEAD SHA | Branch protected | Module baseline proposal |
|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f` | Not rechecked | PROPOSED — Owner adoption open |
| B | `session-b-domain-model-phase3` | `13613ed38965c4961d6eed5eca7c91d31e455f9c` | Not rechecked | PROPOSED — Owner adoption open |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | Not rechecked | PROPOSED — Owner adoption open |
| D | `session-d-memory-brain-2026-11-16` | `b42811141064e7445cd0326382af1789e77ff5b2` | Not rechecked | PROPOSED — Owner adoption open |
| E | `session-e-memory-compiler-2026-11-16` | `65416706bc3fe94b469812ac8bb8d83cc4d146e1` | Not rechecked | PROPOSED — Owner adoption open |
| F | `session-f-memory-runtime` | `714fe628fdcfe62b5e6ea901810b779c58ddddb3` | Not rechecked | PROPOSED — Owner adoption open |
| G | `session-g-memory-context` | `72a8066b4401f9586fe10775d545384b82736f07` | Not rechecked | PROPOSED — Owner adoption open |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` | Not rechecked | PROPOSED — Owner adoption open |
| I | `session-i-security-governance-2026-11-16` | `cdfaf4ebdef3f5cbe6d5a0d2229122930212377c` | Not rechecked | PROPOSED — Owner adoption open |
| P | `session-p-project-governance-baseline` | Coordination branch — see latest P commit | No | Coordination branch |


## Owner proposal artifact inventory — 2026-11-17

| Module | Proposal path | Current proposal Blob SHA | Sections | Disposition |
|---|---|---|---:|---|
| A | `reviews/integration/module-a-integration-governance-baseline-and-redlines.md` | `a43a8f2fa3d31681d64b79d584364fdae80f8866` | 13 | PROPOSED — not APPROVED |
| B | `02-domain-model/module-b-domain-model-baseline-and-redlines.md` | `410d6cc62294e1a7ee5efa0cfe4ef496a8179326` | 14 | PROPOSED — not APPROVED; ADR-001 blocked |
| C | `07-agent-integration/module-c-agent-integration-baseline-and-redlines.md` | `c79da952efaa490083c88ccb4608d62f526fcbae` | 14 | PROPOSED — not APPROVED |
| D | `03-memory-brain/module-baseline-and-redlines.md` | `84e402f471d452c7dab63a7db344f86b5b57bd7c` | 15 | PROPOSED — not APPROVED |
| E | `04-memory-compiler/module-baseline-and-redlines.md` | `7f037a7684723fdbddd593b3d131c7c348e2ccbe` | 15 | PROPOSED — not APPROVED |
| F | `05-memory-runtime/module-baseline-and-redlines.md` | `d4756cabda3151999cbe1ddde0adb554458004a1` | 15 | PROPOSED — not APPROVED; does not yet include new Observation Archive proposal |
| G | `reviews/governance/g-module-baseline-and-redlines-proposal.md` | `fb2eb805be385469b5ab5f25c4ef76f234feb4c2` | 14 | PROPOSED — not APPROVED; does not yet include TSS/compaction/fidelity research proposal |
| H | `reviews/governance/h-module-baseline-and-redlines-proposal.md` | `a4d961ac7b7e1a5fdf59422a4ebe21a6db95ace1` | 14 | PROPOSED — not APPROVED |
| I | `reviews/governance/i-module-baseline-and-redlines-proposal.md` | `b0493cf0366159c99536ee8847996916bc21c606` | 14 | PROPOSED — not APPROVED |

Structural normalization: A has 13 sections; B/C/G/H/I have 14; D/E/F have 15 including an Evidence section. No Owner proposal claims adoption of the P-only template. Preserve this as a governance/template decision rather than silently rewriting Owner artifacts.

Separate Storage branch: `session-storage-consistency-forget-atomicity-2026-11-16`, current HEAD at inventory `d026add5cfaec0d395537e8763317cdbd8255398`; it is not one of the A–I modules.

## Owner deliverable status

**All nine A–I Owner branches now contain a module baseline/redlines proposal**, and all nine were fetched and read back on 2026-11-17. Every artifact explicitly remains PROPOSED / not APPROVED; formal Owner adoption and affected-consumer acceptance remain OPEN. Existing module design documents, ADRs, contract decisions and review artifacts are source evidence, not automatic baseline approvals.

Each Owner's submission must:
1. Be authored on that Owner's branch.
2. Use the canonical template only after it is formally published/adopted; the P template currently exists only on the P branch and is not on main or ratified. Current Owner proposals explicitly record this template gap.
3. Mark each statement DECIDED / PROPOSED / OPEN / ADR-BLOCKED / TO_VALIDATE as appropriate.
4. Cite exact source paths, source branch HEAD and relevant blob SHAs.
5. Separate Owner decisions from consumer acceptance, implementation and verification evidence.
6. Preserve open dependencies and explicitly identify non-owned semantics.
7. Record the Owner's explicit decision and any required affected-consumer acceptance.

## Sequence and blockers

1. **A–I Owner proposal authoring:** may proceed in parallel as PROPOSED drafts; no project governance ratification is implied.
2. **Cross-module reconciliation:** A coordinates; it cannot override Owner decisions.
3. **Open ADR/contract decisions:** relevant domain/producer/consumer authorities decide within their remit.
4. **Conformance evidence:** Verification Owner supplies reproducible test evidence; static document review is not implementation proof.
5. **G0 approval:** blocked until a Project Governance Authority is formally appointed and approves the exact project baseline, redlines, authority model and gate rules.

## Non-claims

- Fresh HEAD reads do not prove branch contents were fully inventoried.
- Existing design artifacts do not prove a module baseline proposal was submitted or accepted.
- Branch protection is currently reported false for the listed branches; this inventory does not change repository settings.
- No Owner branch was modified, no PR was merged, and main was not changed by this tracking update.


## Prepared owner-review proposal packages (Session P, 2026-11-17)

Nine module-specific 14-section proposal packages have been prepared from the source artifacts listed in each file. They are located on the P coordination branch only; they are not committed to Owner branches and are not represented as Owner-authored decisions.

| Module | Proposal path | Prepared status | Owner action required |
|---|---|---|---|
| A | `00-governance/proposals/module-a-integration-governance-proposal.md` | `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f` | Not rechecked |
| B | `00-governance/proposals/module-b-domain-model-proposal.md` | `13613ed38965c4961d6eed5eca7c91d31e455f9c` | Not rechecked |
| C | `00-governance/proposals/module-c-agent-integration-proposal.md` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | Not rechecked |
| D | `00-governance/proposals/module-d-memory-brain-proposal.md` | `b42811141064e7445cd0326382af1789e77ff5b2` | Not rechecked |
| E | `00-governance/proposals/module-e-memory-compiler-proposal.md` | `65416706bc3fe94b469812ac8bb8d83cc4d146e1` | Not rechecked |
| F | `00-governance/proposals/module-f-memory-runtime-proposal.md` | `714fe628fdcfe62b5e6ea901810b779c58ddddb3` | Not rechecked |
| G | `00-governance/proposals/module-g-memory-context-proposal.md` | `72a8066b4401f9586fe10775d545384b82736f07` | Not rechecked |
| H | `00-governance/proposals/module-h-bmcp-protocol-proposal.md` | `242d8ab5da890181e762561bb3d3a662287fb63c` | Not rechecked |
| I | `00-governance/proposals/module-i-security-governance-proposal.md` | `cdfaf4ebdef3f5cbe6d5a0d2229122930212377c` | Not rechecked |

Readback verified all nine proposal files on P. Their current blob SHAs are recorded by the GitHub fetch evidence in the Session P work log. Each package includes mission, ownership, capabilities, domain ownership, interfaces, security, module redlines, forbidden cross-module actions, dependencies, conformance, acceptance, change authority, open decisions and non-claims.

**Adoption gate:** A package is not a module baseline until its named Owner explicitly reviews and adopts a specific version on the corresponding Owner branch. Session P has not written to A–I branches. No Owner decision, cross-module acceptance, project G0 approval or implementation/test result is inferred.


## Concurrent Owner branch movement observed during this pass

A and D advanced after the initial inventory while Session P was preparing the proposal packages. Their tips were re-fetched and the tracking table has been corrected:
- A current HEAD: `7d73102576660fb602376c7ce2f2522a0a8b29ad`; latest commit records D + Storage exact JF-10 bundle decision closure at architecture/interface level and Gate A engineering evidence as next blocker. A freeze remains NOT AUTHORIZED.
- D current HEAD: `1460fbd17ee38ea4044dc6c75cfe49039c7fc585`; latest commit records exact JF-10 v2 acceptance with enumerated exceptions, limited to D-owned semantics. Implementation, DB capability, recovery/fault conformance and multi-domain remain open.

The A and D proposal packages on P were refreshed with these live decisions. The other seven branch tips were rechecked and remained at the initially recorded SHAs at the time of the final inventory. Because branches are live, all Owners must pin their own HEAD again when adopting a proposal.


## Unified review and remediation — 2026-11-17

The first-round A–I Owner branch submissions have now been fetched and read back. Each module has a baseline/redlines proposal, all explicitly PROPOSED and not APPROVED. The live Owner branch HEADs and exact proposal blob SHAs are recorded in `00-governance/reviews/abc-def-ghi-integrated-cross-review.md`.

Unified coordination artifacts added on this P branch:
- `00-governance/reviews/abc-def-ghi-integrated-cross-review.md` — consolidated ABC, DEF and GHI cross-review, source freshness, template structure and shared blockers.
- `00-governance/registries/unified-remediation-and-evidence-register.md` — priority actions UMR-001..012, independent evidence dimensions and gate snapshot.

Current consolidated findings:
- ABC: authority boundaries are directionally aligned; B ADR-001 remains ADR-BLOCKED and B/I/H typed identity/permission binding remains OPEN.
- DEF: D has ACCEPT WITH ENUMERATED EXCEPTIONS for D-owned JF-10 v2 semantics only; Storage physical recovery, accountable deployment/operator, I authorization integration and conformance remain OPEN. Storage PR #12 is closed but its description only claims a single-node probe scope and does not establish production/failover readiness.
- GHI: G/H Applied semantics are compatible in principle, but no common C/G/H schema version/digest and exact three-Owner acceptance has been evidenced. I governance and Global Forget remain GOVERNANCE-BLOCKED.
- The 14-section template exists on P only (blob `408979f2125b67e7599118038b9a415a213399ee`), not on main. It is a proposed governance artifact, not an approved project-wide standard.
- Current structural counts: A 13 sections; B/C/G/H/I 14; D/E/F 15. Owner mapping/normalization is required after the template authority is resolved.
- C/F/G/H technology reports are static conditional reviews. No separate TAR-AI-001 report was found in inspected B/D/E/I artifacts; this is a coverage gap, not a rejection.
- No module baseline is marked APPROVED. No project G0 ratification, PGA appointment, Applied freeze, JF-10 P0 closure, Global Forget completion or architecture freeze is inferred.

The unified review is a coordination/audit record only. It does not substitute for Owner decisions, consumer acceptance, external governance approval, implementation evidence or tests. No A–I branch or main was modified by Session P in this reconciliation.


## TAB-001 mainline refresh and integration drift — 2026-11-17

A new mainline technology architecture workstream was discovered and reviewed:
- Main HEAD: `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`.
- TAB-001 candidate blueprint: `13-engineering-decisions/technology-architecture-blueprint.md`, blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`.
- TAB-001 Owner review task pack: `reviews/integration/tab-001-a-i-technology-architecture-review-task-pack.md`, blob `cf903cd5812cfed3a64a52b169a3bd84209ba3f5`.
- Phase 1 review tasks: `reviews/technology/phase-1-a-i-technology-architecture-review-tasks.md`, blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`.
- Roadmap: `ARCHITECTURE_ROADMAP.md`, blob `29289361973ec4369f067706132190793cd57a6b`.

TAB-001 remains CANDIDATE / NOT A TECHNOLOGY FREEZE. It recommends a local-first Rust modular monolith, SQLite + WAL as a first single-node prototype candidate, content-addressed blob storage, rebuildable lexical/vector indexes, bounded in-process cache and optional isolated inference worker. PostgreSQL is a comparison/evolution candidate; Storage's PostgreSQL 18.7 prepared-XID probe is not a final database selection or production-readiness proof. TEC-003/004 remain OPEN/TO_VALIDATE until D/E/Storage prove exact transaction, locking, recovery and workload requirements.

TAB-001 Owner review coverage at the task-pack paths:
- Present: C, F, G, H (static/conditional reviews).
- Missing: A, B, D, E, I.
- C/F/G/H reports cite pre-publication source snapshots. Their source-to-current comparisons show report updates; G additionally added two context-optimization research artifacts. Each must add a current-source impact note.

G's current branch also contains:
- `reviews/06-memory-context/nvidia-context-optimization-impact-assessment.md`, blob `3fb9f011e24c93a748442018d48c5954584e4f43`, RESEARCH ASSESSMENT / PROPOSED ONLY.
- `reviews/06-memory-context/context-optimization-implementation-candidates.md`, blob `eadefd4e0fe541ef8479a030a2a99a0d57dbcf8b`, candidate register only.
These are valuable design inputs but not a G baseline change or implementation result. Cross-owner dependencies are recorded in the unified review and UMR-014.

## Main/P branch divergence

At the review point, P compared with main is ahead 30 / behind 4. Main's four additional files/changes are the TAB-001 blueprint, its integration review task pack, the Phase 1 Owner review task document and the roadmap update. The branches are diverged; no merge or force update is authorized. UMR-015 tracks a reviewed, non-destructive reconciliation before any future integration.

The unified report and remediation register have been updated to include this mainline workstream. No A–I Owner branch or main was modified by Session P.


## JF-10 PostgreSQL 18.7 evidence refresh — 2026-11-17

Storage's current branch HEAD is `a1fbbd15d3a7993bbb61821ad44957e4f69d3ed1`; dossier blob `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1`; executable conformance plan blob `49056cd46fd30445c0e564c99e0e234f60f065c4`.

Correction to prior status: Storage has expanded beyond the earlier single-node probe. Seven PostgreSQL 18.7 CI workflows all completed SUCCESS on evidence commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`: prepared-XID/restart, synchronous standby promotion, physical backup/restore, explicit-LSN PITR, prepared-XID PITR plus WAL negatives, synchronous-standby-unavailable fail-closed, and old-primary rewind/rejoin. Exact run IDs and scope boundaries are in `00-governance/reviews/jf10-storage-evidence-assessment.md`.

The strongest evidence is the isolated PITR fixture proving prepared-XID and lock retention with no visibility, commit pointer+receipt atomic visibility, rollback non-publication, and missing/corrupt/incomplete WAL fail-closed. These are PostgreSQL engine capability fixtures using isolated `jf10_*` tables, not production I/D/COC or Canonical Authority runtime integration.

Storage's current dossier records that no production runtime source tree, Canonical Authority DB adapter, migration package or application deployment manifest was found in the inspected repository branch. This is now the principal Gate A stop condition. Gate A = PARTIAL PASS / OPEN; Gate B/C BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED.

Database comparison implication: PostgreSQL 18.7 has stronger direct prepared-XID evidence for JF-10 than SQLite + WAL. SQLite remains a candidate only if D/E/I/Storage specify and prove an alternate durable participant/intent protocol preserving the same invariants. TEC-003/004 remain CANDIDATE / TO_VALIDATE; no final DB selection is made.

Full coordinator assessment: `00-governance/reviews/jf10-storage-evidence-assessment.md`.


## Current JF-10 and Applied source reconciliation — 2026-11-17

### Applied 1.1 exact decisions

The live C/D/G/H/I Owner artifacts now all explicitly pin A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`:
- C `45a48249717c8cddb07ab96197730ef93d406c22`: ACCEPT WITH ENUMERATED EXCEPTIONS.
- D `ed7c491f4ca10fee67203a9978cfaa0e0748c0a2`: ACCEPT WITH ENUMERATED EXCEPTIONS.
- G `aa3afa73d8a76cc6f025839c52bfbff6a983046a`: ACCEPT WITH ENUMERATED EXCEPTIONS.
- H `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`: ACCEPT WITH ENUMERATED EXCEPTIONS.
- I `5a5304d48aa912dcf6f817099bd5659371d8cdc8`: ACCEPT WITH ENUMERATED EXCEPTIONS.
- B `3a1e77889cd9a90cd5822d9f0cb3437880868706`: APPROVE — no B semantic type change.
- Storage `a589d983ac145244962c22e5da3a55427aa35ff8`: CONFIRMED WITH CHANGES — ARCHITECTURE INTERFACE ONLY.

Applied design decisions are recorded; freeze remains NO because H schema is not generated/frozen/interoperability-tested, COC deployment/operator is undesignated, runtime implementation is unverified and conformance suites are NOT RUN. The full decision reconciliation is in `00-governance/reviews/applied-contract-1.1-exact-version-reconciliation.md`.

### Storage current-source regression

Current Storage branch HEAD: `3c8ab8ee4579a550300aa48aecab928149cf9370`.
Current dossier blob: `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1`.
Current enhanced PITR probe blob: `7fa4bb3fb07eacc3f708f5682ea4c9e2019f267d`.
Current enhanced PITR run: `43957456225`, job `133615673051`, FAILURE.

The current probe adds an authoritative reader negative fixture (pointer-only/receipt-only rejection), exact target WAL/timeline/segment mapping and stricter negative-case assertions. The log confirms reader negative, prepared/private, commit pointer+receipt, rollback nonpublication and missing exact WAL checks PASS. The corrupt-WAL case reached PostgreSQL's `invalid magic number` fail-closed recovery, but the Python assertion did not accept that diagnostic string; it failed before the no-writable/read-only assertion. The incomplete-WAL case was not reached. Current branch batch is six workflows PASS and one PITR failure; earlier 7/7 PASS remains pinned to older source commit `8b8c749...`.

UMR-018 tracks the exact one-line assertion vocabulary correction and full rerun. JF-10 P0 remains OPEN; Gate A PARTIAL PASS / OPEN.

### A integration tracker freshness

A's live closure tracker blob `554d4b85a94f433856506dce4c020b9c00183e69` still records older Storage HEAD `df60b547...` and prior failed PITR attempt at §13.43. A must refresh its source pins and current regression vector; P does not modify A's Owner record.


## Live branch and Owner decision refresh — 2026-11-17 (supersedes earlier point-in-time HEAD table)

Fresh GitHub commit-ref reads:

| Role | Branch | Observed HEAD |
|---|---|---|
| main | `main` | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` |
| A | `session-a-integration-2026-11-16` | `bfdd091f7ced92bf67e18ab101f2040d9cc59381` |
| B | `session-b-domain-model-phase3` | `30580b094b9cb0ac747ff2849bec5ad68db3e272` |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` |
| D | `session-d-memory-brain-2026-11-16` | `75629584e4b692c83121bebd09e9cb0ea7607226` |
| E | `session-e-memory-compiler-2026-11-16` | `541f7b50f0e52021d6cb892318cc581d2cd8cde3` |
| F | `session-f-memory-runtime` | `5a9816ce5732a3f437e24bbd9a82630a5f4f2c6f` |
| G | `session-g-memory-context` | `4851b46b9de78ecae73186dc104b8be33bb4b519` |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` |
| I | `session-i-security-governance-2026-11-16` | `001204ba7ed73242ac18c59f5de83c3470d2dfe6` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `9f784a15ef33a6cde4b4cda1ab6fca2df8a705fa` |
| P | `session-p-project-governance-baseline` | `31d1ceed6ceb018b5bef2912646ccd7afddef435` before this tracking refresh commit |

P vs main: ahead 51 / behind 4 / diverged. No merge/force update.

The nine proposal artifact blobs were re-fetched and remain unchanged from the previous inventory: A `a43a8f2f...`, B `410d6cc6...`, C `c79da952...`, D `84e402f4...`, E `7f037a76...`, F `d4756cab...`, G `fb2eb805...`, H `a4d961ac...`, I `b0493cf0...`. All nine remain PROPOSED / not APPROVED; no module baseline adoption is inferred.

New cross-owner decisions (not module baseline adoption):
- B: bounded CGH-APPLIED-1.1 typed-reference acceptance; delegated review, not independent human signature.
- D/F/G/I: conditional acceptance of the Context Optimization / Observation Archive architecture boundaries; not interface/schema freeze, implementation or conformance.
- E: bounded JF-10 COC bridge producer-lifecycle acceptance; no production implementation or tests.
- A: exact COC persistence review ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED.
- Storage: COC 3.6.3 durable log/recovery protocol is PROPOSED / NOT IMPLEMENTED; current blob `6154d6c3...`.

Issue #14 remains OPEN with A R1–R6 review and no I/D/C/H response found at refresh. Applied package companion pin mismatch remains open. JF-10 P0 remains OPEN; Gate A PARTIAL PASS / OPEN; Gate B design activity authorized but acceptance open; Gate C deferred to engineering. Global Forget governance and ADR-001 remain blocked.

This addendum supersedes stale earlier HEAD values in this tracking file. Historical values above are retained as point-in-time records, not current branch tips.
