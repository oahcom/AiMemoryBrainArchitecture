# PR Backlog Convergence Plan

**Decision:** AID-2026-028  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Correction date:** 2026-11-20  
**Observed main HEAD:** `5972a1d2f1028893d17f28a00c84202b3083da43`  
**Current observed open PR count:** 9  
**Tracked PR inventory:** 17  
**Quota:** freeze line `≤10`; unfreeze threshold `≤6`  
**Disposition:** drain-under-freeze; this decision does **not** unfreeze the quota.

## Evidence validity

This plan must be read together with:

`14-ai-development/work-items/AID-2026-010/ci-evidence-validity-correction-2026-11-20.md`

GitHub Actions has been blocked by account billing restrictions since `2026-11-19T15:53Z`. The 100 workflow runs examined from `2026-11-19T16:00Z` onward all had zero executed steps. Consequently, neither red nor green CI conclusions generated after that boundary have evidentiary validity.

The historical statements in this plan that attribute failures or successes to GitHub Actions are not independently valid test evidence. In particular, a reported `rust-workspace-test` failure cannot establish that Rust tests failed when the job did not execute.

Where actual technical validation is required, use recorded remote-server local execution evidence, including the exact commit, command, exit code, and test output. Do not describe a non-executed CI job as passed.

## 1. Ruling

The current observed open-PR count is 9, within the governance freeze line of 10. The original inventory covered 17 PRs. Three of those PRs — 332, 333, and 339 — have since been merged and are recorded as converged.

The backlog remains governed by the existing quota freeze. Falling below the freeze line does not satisfy the unfreeze threshold of 6.

The previous assertion that four PRs had a passing bilingual documentation gate but independently failing `rust-workspace-test` is withdrawn as an evidentiary conclusion. The relevant CI execution was blocked and the reported failures cannot establish test outcomes.

The backlog is not evidence that development entry has failed. `AID-2026-027` established scoped engineering-phase development-baseline entry as SATISFIED. The present issue is convergence and evidence-backed disposition of the existing PR queue.

**Quota ruling:**

- The freeze remains in force.
- This is a drain-under-freeze decision, not an unfreeze.
- No new PR carrier is authorized by this decision.
- Existing PRs may be prepared for review and convergence under their existing carriers.
- This decision does not authorize direct writes to `main` or grant `main`-merge authority.
- A `REBASE-THEN-MERGE` disposition is a convergence path, not permission to merge.
- No role appointments are made.

## 2. Per-PR disposition

| PR | Observed condition | Disposition | Required action / rationale |
|---:|---|---|---|
| 320 | PR body lacks the manifest declaration | `RETITLE-AND-DECLARE` | Keep the existing branch and carrier. Add the exact `BILINGUAL-MANIFEST: COMPLETE` declaration in §3. The historical CI failure is not valid evidence of gate execution. |
| 321 | Head predates `check_bilingual_docs.py` and the 31-file prompt library | `REBASE-THEN-MERGE` | Rebase onto `5972a1d2f1028893d17f28a00c84202b3083da43`. Verify the current tree and run applicable checks locally while CI is blocked. |
| 322 | Head predates the gate script and prompt library | `REBASE-THEN-MERGE` | Rebase onto `5972a1d2f1028893d17f28a00c84202b3083da43`; verify the resulting tree and applicable checks. |
| 323 | Dirty merge-conflicted PR; 109 commits; head also predates prompt library | `HOLD` | Do not blindly rebase or merge. First obtain a conflict-resolution plan and inspect the complete 109-commit history and resulting tree. Only after the conflict is understood and resolved may the owner determine whether a rebase onto the observed `main` HEAD is safe. |
| 326 | Head predates the gate script and prompt library | `REBASE-THEN-MERGE` | Rebase onto `5972a1d2f1028893d17f28a00c84202b3083da43`; verify the current tree and applicable checks locally. |
| 327 | Head predates the gate script and prompt library | `REBASE-THEN-MERGE` | Rebase onto `5972a1d2f1028893d17f28a00c84202b3083da43`; verify the current tree and applicable checks locally. |
| 328 | PR body declaration is missing; advisory `POLICY-INHERITANCE` notice also present | `RETITLE-AND-DECLARE` | Keep the existing branch. Add the exact manifest declaration. The advisory notice is not an independently established blocking failure. |
| 330 | Dirty merge-conflicted PR; two body declarations missing | `HOLD` | Resolve and review the conflicts before changing the PR body or attempting a merge. Once the resulting source tree is stable, add the required declaration(s) and perform local validation. |
| 331 | PR body declaration is missing | `RETITLE-AND-DECLARE` | Keep the existing branch and add the exact manifest declaration. |
| 332 | Merged at `2026-11-20T08:43:53Z`; local Rust workspace test passed at head `8c21a2d0acb7` | `CONVERGED-MERGED` | Record the actual local execution result: `cargo test --workspace --all-targets -j 2`, exit 0. The historical CI failure classification is invalid and must not be retained. |
| 333 | Local Rust workspace test passed at head `7f24e25dda93`; merged status not independently supplied in this correction | `CONVERGED-VERIFIED` | Record the actual local execution result: `cargo test --workspace --all-targets -j 2`, exit 0. Do not retain the historical CI failure classification. Confirm the merge record in the existing carrier before treating it as merged. |
| 334 | Head predates the gate script and prompt library | `REBASE-THEN-MERGE` | Rebase onto `5972a1d2f1028893d17f28a00c84202b3083da43`; verify the resulting tree and applicable checks locally. |
| 335 | Ready for review, but head predates the prompt library | `REBASE-THEN-MERGE` | Rebase onto `5972a1d2f1028893d17f28a00c84202b3083da43`; verify the current tree and applicable checks locally before review. |
| 337 | Chinese normative file changed without English counterpart; PR body declaration also missing | `HOLD` | This is not a declaration-only issue. Supply and review the missing English counterpart, verify the intended source/counterpart mapping, then add the manifest declaration. The historical CI status is not evidence that the gate executed. |
| 338 | Historical `rust-workspace-test` failure classification has no execution evidence | `HOLD` | Obtain PR-specific real local execution evidence, including the exact head, command, exit code, and output. Do not treat the unexecuted CI job as a Rust test failure. |
| 339 | Merged at `2026-11-20T08:38:15Z`; local Rust workspace test passed at head `49b1db741634` | `CONVERGED-MERGED` | Record the actual local execution result: `cargo test --workspace --all-targets -j 2`, exit 0. The historical CI failure classification is invalid and must not be retained. |
| 340 | PR body declaration is missing | `RETITLE-AND-DECLARE` | Keep the existing branch and add the exact manifest declaration. |

**Disposition totals:**

- `RETITLE-AND-DECLARE`: 4 — PRs 320, 328, 331, 340.
- `REBASE-THEN-MERGE`: 6 — PRs 321, 322, 326, 327, 334, 335.
- `HOLD`: 4 — PRs 323, 330, 337, 338.
- `CONVERGED-MERGED`: 2 — PRs 332 and 339.
- `CONVERGED-VERIFIED`: 1 — PR 333, pending confirmation of its merge record.
- Total tracked PRs: 17.

No PR is being closed as superseded or abandoned by this correction.

## 3. Exact PR-body declaration

For a PR whose normative changes have complete English/Chinese counterpart coverage, use this exact declaration in the PR body:

```text
BILINGUAL-MANIFEST: COMPLETE
```

The required literal declaration is the complete block above. Do not substitute a paraphrase, a checkbox, or a statement that merely says the change is bilingual.

This declaration is not a substitute for actual counterpart files or semantic review. It must not be used to disguise missing translations, missing counterpart files, or unresolved semantic differences. In particular, PR 337 remains on `HOLD` until its missing English counterpart is supplied and reviewed.

No `BILINGUAL-EXCEPTION: APPROVED` is granted by this decision. An exception must not be self-declared by a PR author. Where an exception is separately authorized by the competent authority, its block must contain the gate's labelled fields with real, non-placeholder values, including a `Due date (YYYY-MM-DD)` field. A placeholder, omitted due date, or incomplete labelled field does not satisfy the exception parser.

## 4. Stale-base remediation

The seven stale PR heads are 321, 322, 323, 326, 327, 334, and 335.

For the six without a reported dirty/conflicted state — 321, 322, 326, 327, 334, and 335 — the current prescribed target is:

`5972a1d2f1028893d17f28a00c84202b3083da43`

The former target `a86b84633239bb1e501372802e68c4ca9cbf06a7` is no longer present in the current repository object database and must not be used as the rebase target.

These six are assigned `REBASE-THEN-MERGE`, not unconditional merge approval. A rebase must preserve the PR's intended changes, bring the current gate script and prompt-library tree into the PR head, and be followed by real local validation while GitHub Actions remains blocked.

If a rebase produces conflicts or changes the intended patch, stop and return the PR to `HOLD` for review. Do not recreate a PR merely because its head is stale; recreation is only a possible later remedy if the existing branch cannot be safely reconciled and the appropriate owner authorizes it.

PR 323 is different. Its dirty state and 109-commit history mean that a safe rebase cannot be inferred from the supplied facts. It remains `HOLD`; no automatic rebase or recreation is authorized. The conflict-resolution and history-review result must precede a decision on its base.

PR 330 is also `HOLD` because it is already dirty and conflicted. It is not among the seven reported stale-base PRs. Its two missing body declarations are secondary until the conflicted source tree is understood.

## 5. Rust workflow failures and replacement evidence

The previous classification of PRs 332, 333, 338, and 339 as having independently failing `rust-workspace-test` jobs is withdrawn.

The relevant GitHub Actions jobs did not execute. Their failure labels cannot establish a Rust test failure.

The following real local execution results have been supplied:

| Target | Commit | Command | Result |
|---|---|---|---|
| PR 332 | `8c21a2d0acb7` | `cargo test --workspace --all-targets -j 2` | Exit 0; all tests OK |
| PR 333 | `7f24e25dda93` | `cargo test --workspace --all-targets -j 2` | Exit 0; all tests OK |
| PR 339 | `49b1db741634` | `cargo test --workspace --all-targets -j 2` | Exit 0; all tests OK |
| main | `803eaebd3f37` | `cargo test --workspace --all-targets -j 2` | Exit 0; all tests OK |

PR 338 has no corresponding successful local execution result in the supplied evidence. It remains `HOLD` pending actual verification, not because CI proved a failure.

For future Rust convergence, each PR must have its own evidence:

1. Exact commit SHA.
2. Actual local command and execution environment.
3. Exit code and test output.
4. Identification and correction of any real failure, if one exists.
5. Confirmation that the resulting tree preserves the intended changes.

A passing local test is evidence for the tested commit and command only. It does not prove that GitHub Actions executed, nor does it establish architecture acceptance.

## 6. G6 — bilingual semantic parity

G6 remains **NOT VERIFIED**.

The bilingual documentation workflow explicitly describes itself as a structural gate. It can check structural conditions such as file presence, counterpart coverage, and the required PR-body declaration. It does not establish paragraph-level semantic equivalence.

G6 requires an evidence-backed, paragraph-level review of the normative source and its counterpart, including:

- a complete inventory of normative files and their language counterparts in the declared scope;
- paragraph-level mapping showing that each source paragraph has the corresponding translated paragraph;
- review of meaning, normative force, conditions, exceptions, modality, terminology, and cross-references in both directions;
- explicit identification and resolution of omissions, additions, contradictions, and semantic drift;
- recorded review evidence and an accountable acceptance decision by the authority empowered to accept bilingual semantic parity.

A structural CI result alone cannot close G6. An unexecuted workflow cannot close it either.

The current PR set can contribute source and counterpart material to a future G6 review. It cannot, as currently evidenced, close G6. PR 337 is specifically incomplete because its changed Chinese normative file has no English counterpart. Other PRs may be included in the review inventory once their source trees and counterpart mappings are stable. No PR merge or declaration is deemed semantic-parity acceptance.

## 7. Authority boundary and unresolved decisions

This decision can classify the observed backlog and prescribe bounded remediation. It cannot manufacture missing authority or evidence.

The following remain outside this ruling:

- **Merge authorization:** No `main`-merge authority is granted. The six `REBASE-THEN-MERGE` dispositions do not bypass the repository's existing review and merge controls. A competent existing merge authority must authorize each merge under those controls.
- **PR 323 conflict/history decision:** The safety of rebasing its 109-commit dirty history cannot be decided without conflict-resolution and patch-preservation evidence.
- **PR 330 conflict decision:** The resulting tree must be reviewed after conflict resolution; this decision does not authorize resolving or merging it.
- **Rust verification:** PR 338 still requires real local execution evidence. No unexecuted CI label can substitute for it.
- **G6 acceptance:** Semantic parity requires qualified independent review and acceptance by the authority designated for that gate.
- **Architecture acceptance:** G8 remains **NOT READY**. The architecture remains **NOT ACCEPTED**. Local test success and PR convergence do not change either conclusion.
- **Quota unfreeze:** The current open-PR count is 9, within the freeze line of 10, but above the unfreeze threshold of 6. This ruling does not unfreeze the quota. Any future unfreeze requires a new count at or below 6 and the applicable governance decision.
- **Roles:** No owner, reviewer, maintainer, or domain role is appointed by this plan.

## 8. Acceptance and tracking conditions

The backlog should be considered converged only when the tracked PRs have explicit, evidence-backed dispositions and the current open-PR count is maintained within the applicable quota.

Track at least these separate outcomes:

1. PR body declarations corrected on 320, 328, 331, and 340.
2. Six stale heads rebased and locally validated against the current base.
3. PR 323 and 330 conflict/history decisions recorded before any merge path is reconsidered.
4. PRs 332, 333, and 339 recorded as merged and locally verified.
5. PR 338 validated using actual local execution evidence.
6. PR 337's missing English counterpart supplied and reviewed.
7. G6 semantic-parity review completed independently of structural checks.
8. Open-PR count remeasured; quota freeze remains until a separate decision changes it.
9. G8 and architecture acceptance tracked independently of PR backlog convergence.

**Final ruling:** The current open-PR count is 9. PRs 332 and 339 are merged; PR 333 has supplied successful local test evidence, with its merge record requiring confirmation. Historical CI failure classifications after the billing-block boundary are withdrawn as evidence. The repository remains under drain-under-freeze governance. No direct `main` writes, no new PR or Issue, no merge authority, no production activation, no architecture acceptance, and no quota unfreeze are granted.
