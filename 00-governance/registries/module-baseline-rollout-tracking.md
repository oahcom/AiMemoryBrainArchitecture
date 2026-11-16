# Module Baseline & Redlines Rollout Tracking

- Tracking version: 0.1.0
- Updated: 2026-11-17
- Status: **FIRST-ROUND OWNER PROPOSALS SUBMITTED — FORMAL ADOPTION / CROSS-MODULE CLOSURE OPEN**
- Authority: Session P coordinates only. Each Module Owner owns authorship and decision of its module baseline.
- Project governance status: **PROPOSED / GOVERNANCE-OPEN**. No PGA appointment or formal G0 ratification is evidenced.
- Main baseline rechecked: `8a6414158c9c056c1638222534e1993d1bbc99d2`.

## Fresh branch inventory

The following are live branch-tip SHAs fetched from GitHub branch metadata on 2026-11-17. They are branch HEADs, not merely file blob SHAs.

| Module | Owner branch | Fresh HEAD SHA | Branch protected | Module baseline proposal |
|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `fb061aee907c28f7da198e68161ff57ebac160b7` | No | PROPOSED — Owner adoption open |
| B | `session-b-domain-model-phase3` | `861fa9b2c3e1f572336543b15c7dc392493891db` | No | PROPOSED — Owner adoption open |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | No | PROPOSED — Owner adoption open |
| D | `session-d-memory-brain-2026-11-16` | `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8` | No | PROPOSED — Owner adoption open |
| E | `session-e-memory-compiler-2026-11-16` | `4402549c39824b89a0dc49973226187c62e056c5` | No | PROPOSED — Owner adoption open |
| F | `session-f-memory-runtime` | `a370d9a3bc0bd35a21a12dfe87d53c298237de8e` | No | PROPOSED — Owner adoption open |
| G | `session-g-memory-context` | `72a8066b4401f9586fe10775d545384b82736f07` | No | PROPOSED — Owner adoption open |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` | No | PROPOSED — Owner adoption open |
| I | `session-i-security-governance-2026-11-16` | `1fc3b3293ebf2077edfd6ad253647d382173d9fa` | No | PROPOSED — Owner adoption open |
| P | `session-p-project-governance-baseline` | Coordination branch — see latest P commit | No | Coordination branch |

## Owner deliverable status

No module baseline/redlines deliverable has yet been submitted under the rollout contract. Existing module design documents, ADRs, contract decisions and review artifacts are source evidence; they are not automatically module baseline approvals.

Each Owner's submission must:
1. Be authored on that Owner's branch.
2. Use the project module baseline/redlines template.
3. Mark each statement DECIDED / PROPOSED / OPEN / ADR-BLOCKED / TO_VALIDATE as appropriate.
4. Cite exact source paths, current branch HEAD and relevant blob SHAs.
5. Separate owner decisions from consumer acceptance, implementation and verification evidence.
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
| A | `00-governance/proposals/module-a-integration-governance-proposal.md` | PROPOSED / P-prepared | A Owner review, correct, adopt or reject on A branch |
| B | `00-governance/proposals/module-b-domain-model-proposal.md` | PROPOSED / P-prepared | B Owner review, preserve ADR-001 blocker, adopt or reject on B branch |
| C | `00-governance/proposals/module-c-agent-integration-proposal.md` | PROPOSED / P-prepared | C Owner review, adopt or reject on C branch |
| D | `00-governance/proposals/module-d-memory-brain-proposal.md` | PROPOSED / P-prepared | D Owner review, preserve JF-10 boundaries, adopt or reject on D branch |
| E | `00-governance/proposals/module-e-memory-compiler-proposal.md` | PROPOSED / P-prepared | E Owner review, preserve publication blockers, adopt or reject on E branch |
| F | `00-governance/proposals/module-f-memory-runtime-proposal.md` | PROPOSED / P-prepared | F Owner review, preserve backend/cancellation validation, adopt or reject on F branch |
| G | `00-governance/proposals/module-g-memory-context-proposal.md` | PROPOSED / P-prepared | G Owner review, preserve C/G/H Applied freeze blocker, adopt or reject on G branch |
| H | `00-governance/proposals/module-h-bmcp-protocol-proposal.md` | PROPOSED / P-prepared | H Owner review, preserve B/I identity dependencies and H36 NOT RUN, adopt or reject on H branch |
| I | `00-governance/proposals/module-i-security-governance-proposal.md` | PROPOSED / P-prepared | I Owner review, preserve external governance/consumer/test blockers, adopt or reject on I branch |

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
