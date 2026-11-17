# PR-RECOVERY-002 Individual PR Decisions / 单 PR 恢复决议

**Baseline:** 68 Open PRs at 2026-11-18 01:10 +08:00; main `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.  
**Decision status:** first-pass triage only; not a final source audit or merge authorization.

## Individually inspected PRs / 已逐项检查

### PR #23 — AID-2026-001 governance package
- Classification: `NEEDS_REBASE`; P1.
- Exact head: `b6b9d2662729fdf2c112ae689cda34e235fdc82f`.
- Compare to frozen main: 22 ahead / 52 behind; 12 changed files.
- Formal reviews: none; requested reviewers: none; current-head status contexts/workflow runs: none observed.
- Decision: do not merge. Safely update/rebase against main, inspect full post-update diff, verify Owner decision status and bilingual parity, obtain A and relevant domain Owner reviews.
- Recovery comment posted: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/23

### PR #27 — persistent Ubuntu worker
- Classification: `SECURITY_REVIEW_REQUIRED`; P0.
- Exact head: `6c70b2fadf39220b31824c3f32114e4e65b617f4`.
- Compare to frozen main: 8 ahead / 51 behind; 3 changed files.
- Formal reviews: none; requested reviewers: none. One Runner Admission Policy workflow run succeeded; no status contexts were reported.
- Decision: do not merge. Require independent I/security review and verification of host identity, runner service identity, sudo boundary, reboot recovery, untrusted-code isolation, branch protection and least privilege. Operator-confirmed state is not independent host verification.
- Recovery comment posted: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/27

### PR #94 — C Provider Outcome workflow path (historical initial triage; now merged)
- Initial classification was `DRAFT_ACTIVE`; P1 candidate. This status was superseded by the verified merge recorded below.
- Exact merged PR head: `47e41a739de42621452a07e041b64d9826098c4a`; target C Owner branch `session-c-agent-integration-2026-11-16`; merge SHA `62c3e799b36c56bd82972a4d7d561f246598deaf`.
- One-line diff adds the CSubmitOutcome 1.0.1 schema path to workflow push filters; no schema semantics changed.
- Workflow run on merge commit, controlled schema-only trigger run and restore run all completed SUCCESS: 44151236345, 44151284885, 44151338457. Current C Owner branch head read as `a9a587e9f73266c74c84c65fda1beeb4246f5a80`.
- Only submitted PR review was author-account COMMENTED; classify `MERGED_REVIEW_GAP` for retrospective independent review provenance. Technical trigger validation is complete.
- Merge log and inventory contain exact evidence; PR #94 is not a main-target PR.

### PR #95 — A minimum engineering slice entry contract
- Classification: `DRAFT_ACTIVE`; P1 candidate; defect open.
- Exact head: `a1b500e7331e89e8f7deac2c35c6d77c9580d640`; 2 commits ahead / 0 behind frozen main; two new 190-line bilingual files.
- Formal reviews and current-head checks: none observed.
- Finding: both language versions state Storage Option A is selected for L1. PR #102's exact-source audit reports the Storage ADR is internally contradictory and classifies L1 as `CONFLICTED / NOT SAFE TO FREEZE`.
- Decision: correct both language versions or cite an approved successor ADR; recheck bilingual parity; keep Draft pending independent review.
- Recovery comment posted: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/95

### PR #102 — A exact Owner source refresh
- Classification: `DRAFT_ACTIVE`; P1/P2.
- Exact head: `a4c9e30be1416d5b36d3d3904ea8166748c986db`.
- Scope: bilingual current-source and contract-Blob audit; explicitly does not amend Owner contracts or authorize merges.
- Formal reviews: none.
- Decision: retain as a high-value source-audit input; verify every cited ref/Blob/run against live source before relying on it; obtain independent A review and relevant Owner responses.

### PR #103 — ARCH-CONVERGENCE-001 C
- Classification: `DRAFT_ACTIVE`; P1/P2.
- Exact head: `669a24deefe1195187915014f70a2d97f71e0ebf`.
- Scope: C Forget, authorization and recovery safety; Draft.
- Decision: no promotion/merge until C/D/I/Storage and relevant downstream Owners review exact fields and acceptance boundaries. Full independent review pending.

### PR #104 — ARCH-CONVERGENCE-001 D (post-baseline intake)
- Classification: `BLOCKED_BY_DEPENDENCY`; P2; post-baseline addition, not part of frozen 68.
- Exact head: `bf3ac0e76ae060ff118cc0e6545cd188c3e85205`.
- Scope: Context Applied/runtime integration contract; explicitly Draft and non-normative.
- Formal reviews: none.
- Decision: require exact C/G/H/I/D/Storage review of identity/evidence joins, current H/C source pins, bilingual parity and relevant conformance/fault tests. Keep Draft.
- Recovery comment posted: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/104

## Remaining initial inventory

All other initial-inventory rows not individually discussed above retain metadata-first provisional classifications in `PR-RECOVERY-002-INVENTORY.csv`; they are not individually cleared. Each requires full changed-file review, formal review/thread and check reconciliation, linked Issue/dependency analysis, and an accountable Owner confirmation. Non-main-target PRs are provisionally `BLOCKED_BY_DEPENDENCY`; other Drafts remain `DRAFT_ACTIVE` until source review supports a stronger disposition.


### PR #31–#35 — AI-RUN-003 stacked runtime proposal chain
- #31 is the parent targeting main; #32 stacks on #31; #33 stacks on #32; #34 stacks on #33; #35 stacks on #34.
- #31 adds the event-driven Owner Worker runtime and ADR-RUN-001; #32 adds GitHub App/webhook security ADR; #33 adds worker isolation ADR; #34 adds idempotency, prompt authorization and branch-gate ADRs; #35 adds logical runtime data model, migration contract, validation workflow/script and review package.
- All five are Draft; no formal reviews were returned for #34/#35. #34/#35 documents are bilingual and explicitly PROPOSED; #35's workflow checks the exact PR revision and uses read-only permissions.
- Classification: #31 DRAFT_ACTIVE / P2; #32–#35 BLOCKED_BY_DEPENDENCY / P2.
- Decision: do not rebase child PRs directly to main or merge as a batch. Require runtime architecture Owner, I/security and Storage/Consistency review of exact ADRs; execute validator/tests on each final head; review workflow trigger trust and migration non-authorization; integrate parent-to-child only after each parent independently passes all gates.

### PR #44, #51, #54 — architecture consolidation stack
- #44 is the main-target parent; #51 stacks on #44; #54 stacks on #51.
- #44 adds bilingual contradiction register, exact evidence ledger and system-wide consolidation. It records unresolved P0/P1 architecture proof obligations rather than claiming they are solved.
- #51 updates the evidence ledger and protocol alignment; its own text describes B alignment as conditional and notes role-simulated Owner reviews are not independent human signatures.
- #54 is a Storage/D topology proposal stacked on #51; it explicitly says D Phase 3.9 changes are not accepted until D and Storage accept the same exact successor Blob.
- Classification: #44 DRAFT_ACTIVE / P1; #51 and #54 BLOCKED_BY_DEPENDENCY / P1.
- No formal reviews found on #44/#51/#54. Do not promote or merge until the relevant A/B/C/D/H/I/Storage Owners review exact source blobs and P0 reference-model proof obligations are closed or explicitly retained as blockers.

### PR #66, #68, #71, #72 — joined Forget terminalization proposals
- #66: D Phase 3.9 bilingual proposal, normative index and reference-model tests; base is D Owner branch.
- #68: I Phase 3.9-I bilingual authorization proposal; base is I Owner branch.
- #71: Storage read-suppression/terminalization proposal; base is Storage Owner branch.
- #72: large joined D/I R3 contract, execution-boundary package and Python reference model/tests; stacks on #42.
- All are Draft and have no formal reviews in the inspected set. Their own headers preserve PROPOSAL / NOT NORMATIVE status.
- Classification: #66/#68/#71 BLOCKED_BY_DEPENDENCY / P1-R3; #72 BLOCKED_BY_DEPENDENCY / P0-R3.
- Require exact bilateral D/I decisions, Storage and all affected execution-domain reviews, source-pin refresh, and exact-head reference-model/fault tests. Do not merge proposals or claim Forget/physical-erasure completion from these artifacts.

### PR #104–#106 — rolling intake
- #104: ARCH-CONVERGENCE-001 D; Open/Draft/main; BLOCKED_BY_DEPENDENCY / P2. Exact current head must be refreshed; C/G/H/I/D/Storage field/evidence joins remain required.
- #105: this PR-RECOVERY-002 evidence package; Open/Draft/main; DRAFT_ACTIVE / P1. Head is self-updating and must be read live; the branch currently contains eight recovery artifacts, 98 commits ahead / 0 behind main by ancestry. No formal review or status contexts; self-review is prohibited.
- #106: ARCH-CONVERGENCE-001 E; Open/Draft/main; BLOCKED_BY_DEPENDENCY / P2. Requires A–I/Storage review of minimum runnable architecture and roadmap before promotion.

### PR #23 — updated disposition
- Classification: `DRAFT_ACTIVE` + `NEEDS_REBASE`; P1. Exact head unchanged: `b6b9d2662729fdf2c112ae689cda34e235fdc82f`; 12 changed files / 22 commits; 22 ahead / 52 behind the frozen main at comparison time.
- Converted to Draft. No formal reviews, status contexts or workflow runs observed.
- Diff confirms proposed standards remain PROPOSED, A's integration authority is explicitly bounded, and preliminary assessment does not claim nine independent reviews. Blocking: stale source pins, missing bilingual counterparts for new governance standards, independent A–I reports and project-governance approval.

### PR #27 — updated disposition
- Classification: `SECURITY_REVIEW_REQUIRED`; P0/P1 security; Open/Draft/main.
- Latest head after a second redaction pass: `27cd318047041e941d78156755dfa885eb41f8df`. Host/runner identifiers, proxy endpoints/ranges, internal egress service names and diagnostic environment-value output have been removed from the three PR files.
- Issue #26 now says SECURITY_ACCEPTANCE_BLOCKED. The runbook records deployment active but security acceptance blocked; service-account deviation is OWNER_REVIEW_REQUIRED.
- Still blocked by sudo-capable runner identity, unverified L3 controls, untested reboot/emergency stop, operator-only password rotation evidence and absence of independent security review. Do not merge.

### PR #94 — updated disposition
- **MERGED** into C Owner branch at `62c3e799b36c56bd82972a4d7d561f246598deaf`; merge-commit, controlled schema-only trigger and restore workflow runs all SUCCESS.
- Technical workflow path defect is resolved. Review provenance remains `MERGED_REVIEW_GAP` because only author-account COMMENTED review is recorded; retrospective independent C Owner review remains required.

### PR #95 — updated disposition
- Classification: `DRAFT_ACTIVE`; P1; exact source contradiction remains open. Both language versions incorrectly state Storage Option A selected for L1 while the cited Storage ADR is internally contradictory / NOT SAFE TO FREEZE per #102. Correct source statement and bilingual parity before promotion.


### PR #28 — repository-wide bilingual documentation expansion
- Classification: `DRAFT_ACTIVE`; P1. Large bilingual expansion across architecture, Owner prompts, translation inventory, governance policy and checker workflow.
- Changes GOV-DOC-001 from v1.0 to v1.1 and labels it NORMATIVE; no formal review was found.
- Shared-file conflict with #23 on four files under `14-ai-development/`; integration must be coordinated and combined diff re-read.
- Required: A governance-owner and I/security review, exact-head checker execution, full EN/ZH semantic parity, pinned workflow actions and current source-pin validation. Keep Draft.

### PR #36 — bounded Codex Owner worker pilot
- Classification: `SECURITY_REVIEW_REQUIRED`; P1. The design separates a read-only Codex job from a write-capable publisher job and restricts proposed output to Markdown; no self-merge/approval is present.
- Blocking security questions: who is authorized to apply `ai:ready`; whether label presence is a valid Owner approval; OPENAI_API_KEY exposure and network/prompt-injection boundary; artifact provenance; and publisher-side independent revalidation of paths/types/symlinks/protected paths.
- No formal review found. Keep Draft pending independent I/security review and adversarial tests.

### PR #46–#50 — assessment portfolio and duplicate candidates
- #46: DRAFT_ACTIVE / P2; bilingual engineering planning assessment, explicitly not implementation authorization; source pins stale and role simulation is not independent Owner approval.
- #47 and #49: DRAFT_ACTIVE / P2; same X complexity assessment scope/date/baseline and NOT PROVEN conclusion, but distinct content/file structures. Duplicate/supersession candidates only; author must designate canonical artifact.
- #48 and #50: DRAFT_ACTIVE / P1; same R system-wide risk assessment scope/date/Issue #43. Exact content/source-delta and explicit supersession decision required before either is closed.
- No formal reviews found on #46–#50. Refresh source pins to current main and retain NOT READY / NOT PROVEN ceilings; no architecture freeze is implied.


### PR #57–#58 — A final architecture package duplicates / successor chain
- #57: `DRAFT_ACTIVE` / P1; 20 bilingual A assessment files, historical base `8c0c5b11...`, no formal submitted review.
- #58: `DRAFT_ACTIVE` / P1; another 20-file A package against the same historical base with clean-base wording. Neither is merge-eligible.
- #60 is the later, broader 26-file package containing the ten EN/ZH pairs plus FINAL-A-003, FINAL-A-004 and CURRENT-SOURCE-RECONCILIATION-003. #60 remains Draft and based on historical `ca69d50...`, 63 ahead / 7 behind current main at its latest recorded comparison.
- Triage comments posted to #57/#58. A must explicitly nominate the canonical package and disposition #57/#58 as superseded before closure; do not merge duplicate assessment packages separately.

### PR #59 and #61 — A/B architecture feasibility re-reviews
- #59: `DRAFT_ACTIVE` / P1; 193-line bilingual B→A currentness re-review, historical base `8c0c5b11...`, no formal review. It records delegated review, not a human Owner signature. Reconcile with #60's current-source addenda and current C/H/I/D/Storage evidence.
- #61: `DRAFT_ACTIVE` / P1; B-02 C/H 1.2.15 successor delta. Correctly keeps B-02 OPEN and distinguishes schema-shape acceptance from integrated authority mapping, validator/CI and same-bundle Owner closure. Historical base `8c0c5b11...`; no formal review. Re-pin exact current artifacts and obtain independent B/C/H/Storage review.

### PR #60 — A final architecture assessment
- Classification: `DRAFT_ACTIVE` / P1; 26 changed files, latest inspected head `bd0e99fcb14152de78b7a7472305a99a97a3490a`, base `ca69d50...`, Draft.
- Contains 13 bilingual A assessment/addendum pairs and current-source reconciliation. Its controlling addendum records overall DEFERRED / ARCHITECTURE_NOT_READY; G2–G5 blocked, G6 partial/not passed, B5 blocked and B6 independent review pending.
- The 2026-11-18 reconciliation says current main is `e52594f...`, tree `7096e0bc...`, same content tree as earlier baseline despite history divergence; #60 remains 63 ahead / 7 behind with merge base `ca69d50...`. Tree identity does not replace a full post-update diff review.
- The reconciliation identifies outdated v3.3.0 wording in eight bilingual pairs and points to Storage v3.3.2 manifest candidate. This is a material correction but does not create same-manifest C/H/D/I approval or production authorization.
- Formal review list contains COMMENTED entries by the PR author account only; these are not independent approvals. Keep Draft; require independent A/domain/Storage review and current-source successor reconciliation.

### PR #62 and #65 — R/X/F/D/P current-source refresh lineage
- #62: `DRAFT_ACTIVE` / P2; historical ten-file delta against `ca69d50...`, later correction and currentness trail. The review comments identify #65 as successor; do not merge #62 as current evidence.
- #65: `DRAFT_ACTIVE` / P1; six bilingual B5/RX-FDP current-source files, head `1a0e36517e782f71db8e2081d423aea572caca81`, base `b3c666e...`, Draft. It records B5 findings A-B5-001..010 and latest B #55 head `e9554bd...`; B5 remains BLOCKED / NOT PASSED and B6 independent review pending.
- #65's listed review submissions are COMMENTED by `oahcom`; they are not independent reviewer approvals. Re-pin against current main `e52594f...` and exact current B/C/H/I/D/Storage branch heads; independent review required.

### PR #56 — TECH-REALITY-001-A independent review artifact
- Classification: `DRAFT_ACTIVE` / P1. Two review documents target PR #45 head `6c7c5919...` and include a follow-up correcting the earlier mergeability observation; no formal review submissions exist on #56.
- The artifact is useful evidence but must not be self-counted as an independent approval of #45. Refresh #45 exact head/base and source pins, verify reviewer identity/authority and review scope, and obtain a distinct independent review submission before it can satisfy M7.


### PR #67 — H Unified 1.2.15 validator / CI / trust review
- Classification: `DRAFT_ACTIVE` / P1. Bilingual A coordination report; no formal review submissions or review threads.
- Exact H HEAD evidence recorded: Provider Outcome run 44079842914 (91 tests, 0 failures) and Recovery Cutoff run 44079842878 (288 tests, 22 skipped, 0 failures). Evidence ceiling is local/reference conformance only.
- Blocking: no issuer pre-sign executable proof, no 1.2.15 integrated authority-join successor, no exact C/I review of current executable Blobs, no production trust/key registration, no durable replay and no Storage successor manifest. Keep Draft.
 
### PR #69 — TECH-REALITY-001-C agent integration research
- Classification: `DRAFT_ACTIVE` / P1. 17-file C research package spanning canonical contract, cross-Owner matrix, failure semantics, telemetry, provider outcome, tool execution and trust boundary.
- Explicit status is RESEARCH IN PROGRESS / NOT FROZEN / INDEPENDENT REVIEW PENDING; not implementation-ready. Base `b3c666e...` is historical to current main. No formal reviews found.
- Require C Owner canonical-source confirmation and scoped B/D/E/F/G/H/I/Storage review of only their authority rows; verify exact source pins, evidence and bilingual claims before any normative adoption.

### PR #70 — B-02 multi-role remediation review
- Classification: `DRAFT_ACTIVE` / P1. Coordinated A role analysis, not independent Owner approval; no formal review.
- Records B-02 PARTIAL/OPEN and P0 blockers: H issuer pre-sign path, H 1.2.15 integrated mapping successor, C exact review, I trust/registration, D currentness/Forget seam, Storage successor manifest. Current branch pins use historical `b3c666e...`.
- Required order: H R1/R2 → C/I/D exact review → Storage successor manifest → A same-bundle readback. Keep Draft.

### PR #66/#68 — D/I Forget terminalization proposals (refined)
- Both are explicitly PROPOSAL / NOT NORMATIVE and have zero formal reviews.
- #66 targets D Owner branch and adds normative-index proposal plus reference-model tests; #68 targets I Owner branch and explicitly requires D/I exact-Blob acceptance. They are not mergeable independently to main; cross-owner contract and exact source pin reconciliation required.


### PR #73 — TECH-REALITY-001-A multi-owner remediation
- Classification: `DRAFT_ACTIVE` / P1. 17-file update to A technology-reality research, includes I authorization/publication reference-model tests.
- README still identifies PARTIAL / NOT YET PROVEN and independent review not started; source baseline `b372b62c...` is stale. No formal review or review threads.
- Require exact-head test execution, source-pin refresh and I/D/Storage Owner review of their respective contract seams. Research remediation must not silently amend domain contracts.

### PR #74–#77 — PRODUCT-FIRST-001 product adoption studies
- All four remain Draft research artifacts, not ADRs or product approvals; all use historical `b3c666e...` baseline.
- #74 (Session 01, memory products): partially verified official-source study; no Brain prototype/benchmark. Graphiti/Mem0/Hindsight remain derivative candidates, never Canonical Memory authority.
- #75 (Session 02, durable execution): SQL-backed outbox/work table + bounded workers is a candidate; Temporal/Restate/DBOS remain conditional. Execution progress must not become Canonical Commit, provider side-effect, Forget terminality or Applied proof.
- #76 (Session 04, security): Cedar is only a bounded PDP prototype candidate. Wrapper must fail closed on evaluator error/unknown; do not let policy skip-on-error be masked by another Permit. I/security review and conformance tests required.
- #77 (Session 05, agent runtime): BMCP remains H-owned; MCP only at external tool edge; LangGraph only an isolated conditional spike. Runtime checkpoint/session/memory is not Brain Canonical Memory, authorization, Forget or Applied evidence.
- Each has only a COMMENTED review by the PR author account; none has an independent approval or review thread. Keep Draft until source pins and applicable Owner reviews are complete.


### PR #78–#79 — PRODUCT-FIRST-001 research continuation
- #78 Session 03 storage/search: `DRAFT_ACTIVE` / P2; 1,010-line adoption study, not ADR or technology freeze. SQLite-local vs PostgreSQL-server is a candidate profile, not Storage L4 decision; dual-write Canonical Memory authority is prohibited. Only author-account COMMENTED review; no independent approval.
- #79 Session 06 simplification: `DRAFT_ACTIVE` / P2; modular-monolith/minimal-deployment is a candidate synthesis, not physical deployment approval or permission to collapse A–I boundaries. Author-account COMMENTED review only; stale session-reference finding requires exact reconciliation.

### PR #80–#82 — architecture breakthrough research kickoffs
- #80 Forget formal verification: `DRAFT_ACTIVE` / P1; research charter only, not completed model checking. Requires executable counterexamples, assumptions, reproducible results, and independent D/Storage/I review.
- #81 Memory Operating System alternatives: `DRAFT_ACTIVE` / P2; design/experiments not complete; requires bounded comparison and explicit domain mapping, no new module/renaming authority.
- #82 Memory IR/Compiler: `DRAFT_ACTIVE` / P1; domain mapping/prototype not complete. B Fact/Claim remains ADR-BLOCKED; B Owner source mapping and independent B/C review required.
- All #78–#82 are pinned to historical `b3c666e...`; #80–#82 have no formal reviews; no research kickoff can be represented as proof or implementation approval.


### PR #83–#87 — architecture breakthrough workstream portfolio
- #83 coordination record: `DRAFT_ACTIVE` / P2; four isolated research branches registered, explicitly not an architecture decision; historical baseline, no formal review.
- #84 combined architecture breakthrough overview: `DRAFT_ACTIVE` / P1; includes TLA+ Forget model/config and comparative research; CANDIDATE/TO_VALIDATE only, no formal review. TLC execution, counterexamples, model assumptions and exact D/Storage/I mapping not evidenced.
- #85 Memory IR/Compiler: `DRAFT_ACTIVE` / P1; 13 files including Python prototype and synthetic sample; README recommends shadow IR only, NOT READY for formal adoption. B Fact/Claim ADR remains blocked; no formal review or prototype execution evidence.
- #86 Memory Operating System: `DRAFT_ACTIVE` / P2; 17 files including prototype and bilingual alternatives; recommends thin resource-manager candidate B only, not full kernel C. Needs same-workload A/B benchmarks and F/G review; no formal review.
- #87 Phase 8 B-02 issuer state machine: `DRAFT_ACTIVE` / P1; current main baseline is e52594f but Owner source pins H/C/I/D/Storage remain older. No formal review. It overlaps #67/#70; canonical A-side report and exact-source refresh required.


### PR #88–#93 — latest breakthrough integration and integrity review
- #88 bounded Forget model: `DRAFT_ACTIVE` / P1; 10 files including explicit-state Python model, invariants, counterexamples and reported results. Main base current `e52594f...`; no check-runs on exact head `bf35b322...` and no formal reviews. Must reproduce model command/results and obtain D/Storage/I independent review.
- #89 PRODUCT-FIRST-001 integration: `DRAFT_ACTIVE` / P2; non-normative synthesis of Sessions 01–06, no ADR/product freeze; no formal reviews.
- #90 H branch integrity incident: `SECURITY_REVIEW_REQUIRED` / P0 historical incident report. Its incident head `0277a8b9...` is no longer current. Current H branch is `6608cde...`, recursive tree 248 entries; compare from prior good `0d363244...` is 7 ahead/0 behind, 8 added/0 removed; from incident head, 211 added/0 removed. Current-main compare 490 ahead/58 behind, 182 added/0 removed. Branch tree is restored relative to prior complete baseline; owner acknowledgment and exact H current-source/CI revalidation remain.
- #91 H/C branch integrity incident: `SECURITY_REVIEW_REQUIRED` / P0 historical incident report. Current H `6608cde...` tree 248; current C `a69007a...` tree 147. C compare from prior good `71047cdb...` is diverged 63 ahead/167 behind, 65 added/3 modified/0 removed; against incident `a5dff993...`, 65 added/3 modified/0 removed. Current-main C compare 7 ahead/2 behind, 17 added/0 removed. No current branch tree truncation detected; owner acknowledgment and exact readback remain.
- #92 C-REVIEW-001 evidence refresh: `BLOCKED_BY_DEPENDENCY` / P1; stacked on C research branch. Tree-integrity blocker no longer present in current C ref, but it still depends on #69/C source and needs exact-head validation and C/H/G/I/Storage review.
- #93 architecture-breakthrough integration: `DRAFT_ACTIVE` / P1; latest head `c6c6e136...`; exact-head `bounded-model` check completed SUCCESS. Workflow still uses mutable checkout/setup-python tags; pin immutable SHAs and rerun. No formal review; bounded model success does not prove production or global Applied closure.


### PR #98–#103 — latest architecture review and convergence artifacts
- #98: `DRAFT_ACTIVE` / P1; A exact review of H Applied Delivery Evidence 1.0.0. It records H-ADE-001 strict duplicate-key parsing, H-ADE-002 C Outcome immutable-record/Outcome/SideEffect/Request-boundary resolver, and H-ADE-003 current I authorization/PermissionEpoch + D fence checks before replay result disclosure as OPEN. Bounded 11-test CI on 4e65a2e is real but not production trust/replay. Delegated A review, no formal review.
- #99: `DRAFT_ACTIVE` / P1; three-file A source-of-truth/conflict/dependency inventory. It must refresh H/C incident refs and verify path absence against exact current main/Owner refs; C Owner branch is 88992da, separate C research branch is a69007a.
- #100: `DRAFT_ACTIVE` / P1; A source audit of #93. Its #93 pin 0f3ba529 is stale; latest #93 head c6c6e136 has bounded-model SUCCESS. Re-read current PR #93 head and preserve bounded evidence ceiling.
- #101: `ARCHITECTURE_CONFLICT` / P1; B canonical transaction proposal asserts Storage L1 Option A selected, contradicting exact Storage ADR Blob bb544ba2... whose §3 says no option selected. Correct to CONFLICTED / NOT SAFE TO FREEZE pending Storage Owner successor/correction and D/Storage acceptance.
- #102: `DRAFT_ACTIVE` / P1; nine-Owner source refresh with current refs and bounded CI evidence. It records H/C restoration, Storage ADR contradiction and G1 PARTIAL / G2–G5,G7 BLOCKED / G6 PARTIAL / G8 NOT READY. Strong audit artifact, but no independent formal review.
- #103: `DRAFT_ACTIVE` / P1; C Forget/authorization/recovery safety contract with 20 race scenarios, explicitly conditional/non-normative. Requires D/I/E/F/G/H/Storage exact source review and executable tests; physical restore and production safety remain unproven.

### PR #104–#107 — ARCH-CONVERGENCE-001 rolling intake
- #104 D Context Applied/runtime: `DRAFT_ACTIVE` / P1; preserves separate Prepared/Delivered/Materialized/FinalRequestSubmitted/GApplied stages. Refresh H-ADE-001..003 and current exact C/G/H/I/D/Storage pins; no global Applied freeze.
- #105 this recovery package: `DRAFT_ACTIVE` / P1; 8 changed files, 42 commits on dedicated recovery branch; no self-approval; independent review and exact-head checks pending.
- #106 E minimum runnable roadmap: `DRAFT_ACTIVE` / P1; distinguishes Canonical Core Slice from complete Minimum Runnable Brain; no implementation authorized; must correct Storage L1 Option A as conflicted and retain B Fact/Claim blocker.
- #107 cross-workstream synthesis/adversarial matrix: `DRAFT_ACTIVE` / P1; test definitions only/not executed; separates L0–L4 evidence layers; exact C/G/H mapping and Storage contradiction require resolution.

### PR #108–#111 — AI-DEV-OS-001 Phase 0 publication PRs (updated disposition)
- #108/#109 are merged into main as research publications; both remain `MERGED_REVIEW_GAP` because their only review was author-account COMMENTED. Retrospective independent review is required before relying on recommendations.
- #110 Session 4: Ready, current head `5f42acb1391a06703f9aa1a7b615f4dd62d5cbea`, target current main `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`, mergeable=true. Technical re-check found no new blocking content defect, but no independent exact-head approval or status/check evidence; do not merge.
- #111 Session 3: Ready, current head `c6fc822c64c6afa728e1eff884012384256958cf`, target current main, mergeable=true. BLOCKER severity and lifecycle crosswalk are corrected; P1 blocking policy is explicitly proposed, not existing AI-STD-001 norm. No independent exact-head approval or status/check evidence; do not merge.
- The recovery-session technical re-check comments on #110/#111 are explicitly non-independent because authenticated GitHub identity `oahcom` is the PR author. They are not GitHub APPROVE reviews.


### PR #1 — G Memory Context Manager Owner package
- Classification: `NEEDS_REBASE` / P1. 24-file G package targets main from historical base `e443b23...`; head equals live G Owner branch `763b3d31...`; no formal review.
- Includes core G architecture/lifecycle, Applied/Forget reconciliation, COC/JF-10 bridge, G 3.8.22 Applied persistence contract and technology/review artifacts.
- Rebase/update to current main and inspect full combined diff; consider splitting normative G contract from research/acceptance artifacts. Obtain G Owner and C/H/I/D/Storage exact consumer reviews. G contract itself says implementation unverified and cross-owner acceptance required.

### PR #42 — ChatGPT-native execution model / AID-2026-001
- Classification: `ARCHITECTURE_CONFLICT` / P1. 35 files; historical base `b372b62...`; current head `84d91b10...`; no current-head CI or independent review.
- Only review record is COMMENTED by PR author account against old head `1d6ab393...`. Conflicts/overlaps with #23 governance, #31 Owner Worker and #36 Codex pilot plus Issue #41 channel restrictions.
- Requires one Session 0 decision on authorized execution channels, current governance source reconciliation and I/security review. Proposal only; no runtime authorization.

### PR #44/#51/#52/#54 — ARCH-CONSOL Phase 2/3 lineage
- #44: `DRAFT_ACTIVE` / P1 parent, three-file contradiction/evidence/consolidation package; old main base, no formal review.
- #51: `BLOCKED_BY_DEPENDENCY` / P1, four-file Phase B child stacked on #44; older H protocol and Storage v3.3.0 assumptions, no formal review.
- #52: `ARCHITECTURE_CONFLICT` / P1, delegated A B→A protocol/topology review, not independent Owner signature; conditionally accepts L1 Option A contrary to exact Storage ADR contradiction.
- #54: `ARCHITECTURE_CONFLICT` / P1, two-file proposed normative amendment to Storage ADR, explicitly NOT ADOPTED, stacked on #51.
- Required: refresh #44/#51 evidence from #102; Storage Owner must correct/supersede exact ADR Blob and D/Storage accept the same version before any Option A normative amendment. No child retargeting to main until parent acceptance.

### PR #45/#55/#63–#65 — research and A review lineage
- #45 TECH-REALITY-001-A: `DRAFT_ACTIVE` / P1, 14-file PARTIAL/NOT YET PROVEN research; #56 is a review artifact, not submitted independent review; #73 is later remediation.
- #55 DOMAIN-REALITY-001-B: `DRAFT_ACTIVE` / P1, 22-file B research; B0 PARTIAL, B5 BLOCKED, B6 independent review pending; A-B5-001..010 findings remain; Fact/Claim ADR-BLOCKED.
- #63 G1 currentness audit: `STALE_UNCERTAIN` / P2; historical main 901e38 snapshot, later #65/#102 current-source work. Await A canonical supersession decision.
- #64 B-02 delta review: `STALE_UNCERTAIN` / P1; delegated analysis on historical main 901e38, partially superseded by #65/#67/#70/#87/#98/#102.
- #65 R/X/F/D/P + B5 refresh: `DRAFT_ACTIVE` / P1; B5 remains BLOCKED/B6 independent review pending; no formal review.

### PR #94–#95 — C workflow and minimum-slice entry
- #94: **MERGED** into C Owner branch; trigger and restore validation SUCCESS; independent-review provenance gap tracked separately. It was never a main-target merge.
- #95: `DRAFT_ACTIVE` / P1; A minimum-slice entry proposal, DEFERRED/NOT IMPLEMENTATION AUTHORIZATION; Issue #7 open and B/Storage blockers remain.



## Latest portfolio addendum — 2026-11-18

- Live Open PR count is 73 (71 Draft, 2 Ready); 62 target main / 11 target non-main. Three of the original 76 tracked PRs are now merged: #94, #108, #109.
- PR #112/#113 were maintenance-only synchronization merges from main into recovery/Session 4 branches; neither changed main.
- PR #94's technical trigger validation is complete with three SUCCESS workflow runs, but its author-account-only COMMENTED review remains a governance provenance gap.
- #110/#111 are the only Ready Open PRs. Neither has a current-head independent APPROVE or current-head status/check-run evidence. The recovery-session technical re-checks are not independent approvals.


## Live merged-PR reconciliation — 2026-11-18

The REST closed-PR census confirms 15 of the original 76 tracked PRs are merged. All 15 remain classified `MERGED_REVIEW_GAP` until retrospective independent review/Owner disposition is recorded:

- **Zero formal PR review submissions:** #32, #33, #34, #35, #51, #54, #66, #68, #71, #72, #92. Each was merged into a non-main runtime, Owner, architecture-review or research branch. Exact merge SHAs and target branches are in the merge log.
- **Author-account COMMENTED only:** #94, #108, #109, #110. None has an independent APPROVE in the PR review API.
- #94 has three SUCCESS workflow runs for merge commit, controlled schema-only trigger and restore. This validates the C workflow trigger behavior but does not replace C Owner/independent review.
- #108/#109 are research publication merges into main. #110 is a research publication merge into main at `4a0acc1608f0909bafb64ac90f0a724b8223d546`; the merge commit has no status contexts or PR workflow runs.
- Current main: `4a0acc1608f0909bafb64ac90f0a724b8223d546`.
- Current Open PRs: 61 (60 Draft, 1 Ready); all target main. #111 is the only Ready PR.
- #111 was rebased onto current main without changing the report blob. Exact current head: `9a7ba7ac8cfc6d3de0d732bb7e677ff2288a4ca5`; compare 1 ahead / 0 behind. No current-head status/check evidence or independent review.
- #105 recovery package was compacted/rebased onto current main. It remains Draft, contains only the eight recovery artifacts and cannot self-review or self-approve.
- The authenticated GitHub identity is `oahcom`, which authored all 61 current Open PRs. The Recovery Principal Reviewer role can conduct technical re-checks but cannot create a separate GitHub identity or satisfy the source standard's separate-session/agent requirement by assertion.
