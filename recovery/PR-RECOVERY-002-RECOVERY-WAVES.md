# PR-RECOVERY-002 Recovery Waves / 恢复波次

## Wave 0 — Repository safety (ACTIVE / PARTIAL)
- Main frozen at `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.
- Repository write/admin capability confirmed.
- Auto-merge disabled; merge/squash/rebase methods allowed.
- Branch protection and rulesets remain UNKNOWN (403); required checks and rollback policy not independently verified.
- Exit requires administrator-supplied branch-rule evidence or a permitted API read, plus a stable merge/rollback procedure.

## Wave 1 — Independent low-risk candidates (ACTIVE / NO MERGE QUALIFIED)
- #94 was a one-line C workflow path correction; it is now merged into the C Owner branch and the merge, schema-only trigger and restore workflow runs passed. Independent-review provenance remains a retrospective governance gap.
- #95 is a small bilingual proposal but contains a material Storage Option A status contradiction. Fix and independent review required.
- #23 is Ready but diverged 22 ahead / 52 behind; no formal review or checks. Rebase/update and re-review required.
- No PR currently satisfies all applicable M1–M10 gates.

## Wave 2 — Dependency chains (QUEUED)
- #31 → #32 → #33 → #34 → #35.
- #44 → #51 → #54.
- #42 → #72.
- #69 → #92.
- Integrate parent only after its own review and gates; refresh main and revalidate child after each parent.

## Wave 3 — Draft and research reconciliation (QUEUED)
- Reconcile #74–#89 PRODUCT-FIRST and architecture-breakthrough research streams for overlap, supersession and evidence provenance.
- Reconcile #90–#104 architecture-convergence and current-source review stream; #104 is post-baseline rolling intake.
- Review large-scope PR #28 (162 files / 298 commits) for split/supersession only after exact diff and overlap analysis.
- Do not auto-promote Drafts.

## Wave 4 — Governance and closure (QUEUED)
- Obtain accountable Owner assignments and independent reviewers.
- Establish Ready-for-review criteria, review SLA, integration SLA, blocked escalation and post-merge verification.
- Close duplicates/superseded work only after exact replacement and provenance are proven.
- Publish final evidence in a dedicated recovery PR; no direct push to main.


## Wave 1 status refresh — 2026-11-18
- No PR currently qualifies for merge. Live portfolio is 71 Open / 71 Draft / 0 Ready.
- #23 and #27 were moved back to Draft; #27 has bounded redaction/status remediation committed, but security acceptance remains blocked.
- #94's technical trigger validation is complete; its independent-review provenance gap remains open for retrospective C Owner review.
- #95 remains blocked on the Storage Option A source contradiction.
- #105 recovery artifact PR remains Draft and requires independent review; it cannot self-approve its own baseline.

## Wave 2 — dependency chains (ACTIVE / BLOCKED)
- AI-RUN-003: #31 → #32 → #33 → #34 → #35.
- Architecture consolidation: #44 → #51 → #54.
- ChatGPT-native/Forget remediation: #42 → #72.
- C research/remediation: #69 → #92.
- D/I/Storage Forget proposals #66/#68/#71 require exact cross-owner agreement; they are not a simple merge chain.
- No child may be retargeted to main before parent acceptance and exact diff re-evaluation.


## Wave 2A — A/B assessment artifact reconciliation
1. Preserve #60 as the current A assessment candidate, but do not merge: stale/diverged base, eight EN/ZH pairs retain obsolete Storage v3.3.0-era wording, and author-account COMMENTED records are not independent approvals.
2. Obtain explicit A decision whether #57/#58 are superseded by #60; close only after that disposition is recorded.
3. Reconcile #59/#61 with latest B/C/H/I/D/Storage sources; retain B-02 OPEN, B5 BLOCKED and G6 PARTIAL/NOT PASSED until independent evidence supports change.
4. Treat #62 as historical if A confirms #65 supersedes it; #65 still requires re-pin to current main and independent review.
5. #56 cannot satisfy independent review for #45 by itself; verify distinct reviewer identity and actual submitted review on #45.


## Wave 2B — H 1.2.15 / B-02
- Retain #67 and #70 as Draft review artifacts; both document evidence ceilings and unresolved P0/P1 blockers.
- H must first publish issuer pre-sign chain and immutable integrated authority-join successor mapping; tests must prove INVALID/UNKNOWN C objects cannot trigger H signing or durable ingress.
- C/I/D review exact current Blobs and CI; Storage publishes an immutable successor manifest only after those decisions; A performs same-bundle readback.
- Current local CI success on H HEAD does not prove production trust, signing-key custody, issuer ordering, durable replay, or physical Storage conformance.


## Wave 3A — product / technology research
- Preserve #74–#77 as Draft research. Refresh source pins, validate official-source claims and require independent reviews.
- Run only bounded isolated spikes after domain Owners accept the relevant boundary and acceptance criteria.
- No technology is frozen and no external product becomes a runtime dependency solely by virtue of these reports.


## Wave 3B — architecture breakthrough research
- #80: require executable formal model and counterexample-first results before promotion.
- #81: require bounded alternative comparison and explicit owner mapping before any design decision.
- #82: require B Fact/Claim source authority and prototype evidence; keep canonical identity unresolved until B decision.
- Research kickoff PRs stay Draft and do not block unrelated qualified integration.


## Wave 3C — breakthrough research validation
- #84: execute formal model checker and preserve counterexamples before calling it verified; coordinate with #80.
- #85: reproducibly run direct-vs-IR prototype; retain shadow-only status until B/C/E acceptance.
- #86: benchmark thin resource manager against current A under identical workload; require F/G review.
- #87: reconcile overlapping A-side B-02 reports (#67/#70/#87), refresh H/C/I/D/Storage source pins and obtain independent Owner review.


## Wave 2C — H/C branch integrity incident reconciliation
- Historical truncation incident in #90/#91 is not present in refreshed refs: H and C recursive trees are complete as reported and current compare shows zero removed paths.
- Do not close incident records solely from tree counts. Obtain H/C Owner acknowledgment, exact tree inventory/readback of critical contracts/tests/workflows and exact-head CI.
- H current head `6608cde...` has `semantic-and-wire-tests` SUCCESS; Applied Delivery Evidence conformance run 44130722532 passed on parent/test commit `4e65a2e...`. Verify coverage against current head before acceptance.


## Wave 4 — ARCH-CONVERGENCE-001 and AI-DEV-OS-001 publication intake
- #99–#103 provide source inventory, A review, B canonical transaction proposal, Owner refresh and C safety contract; all remain Draft pending Owner review.
- #104–#107 workstreams D/E/integration are draft/non-normative; no implementation authorization or executed adversarial matrix.
- #108–#111 are Ready for independent Session 0 review but not merge-eligible: no formal reviews, no check-runs, no review threads. Their one-file documentation scope does not waive M7.


## Wave 2D — G Owner and architecture consolidation lineage
- #1: rebase/update G Owner package, split if needed, then obtain exact C/H/I/D/Storage consumer reviews.
- #44 → #51 → #54: parent-first; refresh all sources, resolve Storage L1 ADR contradiction before accepting any proposed normative amendment.
- #42: hold until Session 0 resolves ChatGPT-native vs event-driven/Codex execution boundary.
- #45/#55: retain research-only status; no technology/domain freeze; independent B/TECH-REALITY reviews pending.

## Wave 2E — C workflow and entry-contract
- #94: **MERGED** into C Owner branch; merge-commit, controlled schema-only trigger and restore runs all SUCCESS; no main merge. Retrospective independent review remains outstanding.
- #95: no implementation authorization; align to #102/#103/#107 and wait for Owner acceptance.


## Live portfolio sequencing refresh — 2026-11-18

Historical REST snapshot at that checkpoint: **74 Open PRs = 72 Draft + 2 Ready (#110, #111); 62 target main + 12 target non-main.** Main is `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`. Exact stacked-base edges are refreshed in `PR-RECOVERY-002-DEPENDENCY-GRAPH.md`.

### Wave A — resolve hard dependency roots before children

1. **AI-RUN-003:** #31 → #32 → #33 → #34 → #35. Review and accept each parent independently; after each integration, refresh main, rebase/update the next child, inspect its complete new diff and rerun exact-head checks. Do not batch merge.
2. **Architecture consolidation:** #44 → #51 → #54. #44 must first close or explicitly retain its P0/P1 proof obligations; #51 must reconcile exact B/C/D/H/I/Storage evidence; #54 requires same-successor D and Storage acceptance and resolution of the Storage ADR contradiction.
3. **ChatGPT-native execution / Forget:** #42 → #72. Hold until Session 0 resolves the #23/#31/#36/Issue #41 execution-governance boundary and the #42 exact-head integrity/review blockers; #72 then requires D/I/Storage and affected execution-owner review.
4. **C research remediation:** #69 → #92. Treat #92 as a branch-stacked remediation of C research, not C Owner branch acceptance or runtime contract approval. Re-pin #69 and #92 and verify C Owner disposition.

### Wave B — cross-Owner contract agreement (parallel review, single joined decision)

- #66 (D), #68 (I), #71 (Storage) must be reconciled as one agreement set, with exact same successor Blob references and explicit Owner decisions. These are not a serial PR chain.
- B-02/H 1.2.15 path: H issuer pre-sign and integrated authority-join successor → C/I/D exact review → Storage immutable successor manifest → A same-bundle readback. #67/#70/#87 are A coordination evidence, not Owner approvals.
- ARCH-CONVERGENCE-001 B/C/D/E (#101/#103/#104/#106) require scoped Owner acceptance and shared contract evidence; A synthesis #99/#102/#107 cannot substitute for those decisions.

### Wave C — independent roots and bounded review

- #110/#111 are the only non-Draft PRs in the live snapshot. They are Ready for independent review, not approved; verify formal independent exact-head review and checks before any merge consideration.
- #94 may be integrated only into the C Owner branch after C Owner approval and exact schema-only workflow trigger test; it is not a main-target candidate.
- #23/#28 shared-file conflict must be reviewed as a combined integration boundary. Do not merge one and assume the other remains unchanged.
- #47/#49, #48/#50 and #57/#58/#60 require exact content/source-delta comparison plus explicit canonical artifact designation before closure or supersession.

### Wave D — research portfolios; do not let research block unrelated roots

- #74–#79 PRODUCT-FIRST research and #80–#89 architecture-breakthrough research remain non-normative research. Refresh historical source pins and obtain independent reviews; only promote a bounded spike when the relevant domain Owner accepts its authority boundary.
- #45/#56/#73 TECH-REALITY lineage: verify exact source head, review provenance and actual independent review submission on the target PR. Review documents alone do not satisfy the review gate.
- #90/#91 branch-integrity incident reports are historical evidence; H/C tree restoration does not replace Owner acknowledgment, critical-path readback and exact-head CI.

### Execution guardrails

- No automatic base retargeting of the 12 non-main PRs to main.
- No merge based solely on `mergeable=true`, Draft=false, author-account COMMENTED review, or successful bounded/reference tests.
- Every integration step must record: exact parent head, current main SHA, complete changed-file diff, conflicts, required Owner decisions, independent review at the final head, checks/statuses, merge SHA, and post-merge verification.
- This is a dependency-aware ordering proposal, not an authorization to merge. No PR was merged or closed in this refresh.


## Non-main integration policy correction — 2026-11-18

A non-main target is a legitimate integration destination, not a blocker. Merge into the declared target branch once its parent/dependency, exact-head independent review, checks and accountable Owner acceptance pass. Never retarget to main solely to clear backlog.

Live status correction:
- PR #94 is already CLOSED / MERGED into the C Owner branch; remove it from the pending wave and separately verify its post-merge workflow evidence.
- The 11 remaining non-main PRs (#92, #72, #71, #68, #66, #54, #51, #35, #34, #33, #32) currently report `mergeable=true` / `mergeable_state=clean`, but all are Draft with no requested reviewers. They are technically conflict-free, not approved.
- Parent-first merge order remains mandatory for #32→#35, #44→#51→#54, #42→#72, and #69→#92. Each child merges into its stated parent branch only after its parent is accepted and the child's exact diff is re-reviewed.
- #66/#68/#71 can merge into their respective D/I/Storage Owner branches only after exact Owner acceptance and cross-Owner contract reconciliation. These are parallel branch-local integrations, not a single merge chain.

This corrects the earlier overbroad “non-main target blocked” language. The real gates are parent readiness, Owner authority, independent review, required checks and contract consistency.


## Non-main integration execution — COMPLETE

The entire live non-main-target set has been integrated into its declared branch destinations: #94, #92, #72, #71, #68, #66, #54, #51, #35, #34, #33 and #32 are all verified CLOSED / MERGED. The AI-RUN-003 and architecture-consolidation stacks were merged leaf-to-root. No target was changed to main. Exact merge commits and destination branches are recorded in the dependency graph.

This closes the non-main-target backlog wave. Next work moves to the main-target PR queue and post-merge verification of the Owner/research branches. A merge into an Owner/research branch is branch integration only; it does not by itself make a proposal normative or authorize production behavior.


## Latest live wave status — 2026-11-18

- Current REST snapshot: **73 Open PRs = 71 Draft + 2 Ready (#110, #111); 62 target main + 11 target non-main.**
- Main remains `4bee3e886cc0dec4a8d03817acd180ba979f8ceb`.
- #94 is merged to C Owner branch; its exact trigger/restore runs passed. It is no longer queued as a pending merge, but independent-review provenance remains open.
- #110 exact head `5f42acb1391a06703f9aa1a7b615f4dd62d5cbea` and #111 exact head `c6fc822c64c6afa728e1eff884012384256958cf` are mergeable=true but lack independent exact-head approval and current-head status/check evidence. Both remain blocked at the formal review/verification gates.
- #105 recovery package is Draft and self-authored; it cannot review or approve itself. Its branch is 98 commits ahead / 0 behind main by ancestry and changes only the eight recovery artifact files in the PR diff; independent review remains required.
- No current main-target PR has a GitHub `review:approved` result. Do not merge by substituting the current Recovery Principal Reviewer technical re-check for the required separate AI session/agent.
