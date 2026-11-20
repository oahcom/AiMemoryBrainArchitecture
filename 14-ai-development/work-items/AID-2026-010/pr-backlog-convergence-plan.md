# PR Backlog Convergence Plan

**Decision:** AID-2026-028  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Observed main HEAD:** `a86b84633239bb1e501372802e68c4ca9cbf06a7`  
**Observed open PR count:** 17  
**Quota:** freeze line `≤10`; unfreeze threshold `≤6`  
**Disposition:** drain-under-freeze; this decision does **not** unfreeze the quota.

## 1. Ruling

The backlog is above both governance thresholds: 17 open PRs against a freeze line of 10 and an unfreeze threshold of 6. Thirteen are drafts and four are ready for review. Four PRs have a passing bilingual documentation gate, but their `rust-workspace-test` job is independently failing. Two PRs have merge conflicts. Seven PR heads predate the prompt-library files now present on `main`.

The backlog is not evidence that development entry has failed. `AID-2026-027` established scoped engineering-phase development-baseline entry as SATISFIED. The present issue is failure to converge the existing PR queue.

**Quota ruling:**

- The freeze remains in force.
- This is a drain-under-freeze decision, not an unfreeze.
- No new PR carrier is authorized by this decision.
- Existing PRs may be prepared for review and convergence under their existing carriers.
- This decision does not authorize direct writes to `main` or grant `main`-merge authority.
- A `REBASE-THEN-MERGE` disposition is a convergence path, not permission to merge. Any merge remains subject to the existing authorized review and merge controls.
- No role appointments are made.

## 2. Per-PR disposition

| PR | Observed condition | Disposition | Required action / rationale |
|---:|---|---|---|
| 320 | Bilingual gate fails only because PR body lacks the manifest declaration | `RETITLE-AND-DECLARE` | Keep the existing branch and carrier. Add the exact `BILINGUAL-MANIFEST: COMPLETE` declaration in §3. No source change is required for this reported gate failure. |
| 321 | Head predates `check_bilingual_docs.py` and the 31-file prompt library; gate cannot run | `REBASE-THEN-MERGE` | Rebase onto `a86b84633239bb1e501372802e68c4ca9cbf06a7`. Then rerun the workflow and all applicable checks. The old head cannot establish compliance because it lacks the gate and required prompt files. |
| 322 | Head predates the gate script and prompt library; gate cannot run | `REBASE-THEN-MERGE` | Rebase onto `a86b84633239bb1e501372802e68c4ca9cbf06a7`; rerun the workflow and applicable checks. |
| 323 | Dirty merge-conflicted PR; 109 commits; head also predates prompt library | `HOLD` | Do not blindly rebase or merge. First obtain a conflict-resolution plan and inspect the complete 109-commit history and resulting tree. Only after the conflict is understood and resolved may the owner determine whether a rebase onto the observed `main` HEAD is safe. |
| 326 | Head predates the gate script and prompt library; gate cannot run | `REBASE-THEN-MERGE` | Rebase onto `a86b84633239bb1e501372802e68c4ca9cbf06a7`; rerun the workflow and applicable checks. |
| 327 | Head predates the gate script and prompt library; gate cannot run | `REBASE-THEN-MERGE` | Rebase onto `a86b84633239bb1e501372802e68c4ca9cbf06a7`; rerun the workflow and applicable checks. The missing script means the old head cannot provide a valid gate result. |
| 328 | Bilingual gate fails because PR body declaration is missing; advisory `POLICY-INHERITANCE` notice also present | `RETITLE-AND-DECLARE` | Keep the existing branch. Add the exact manifest declaration. The advisory notice is not reported as an independent blocking failure; do not treat it as a reason to close the PR. |
| 330 | Dirty merge-conflicted PR; two body declarations missing | `HOLD` | Resolve and review the conflicts before changing the PR body or attempting a merge. Once the resulting source tree is stable, add the required declaration(s) and rerun the gate. The conflict state means this is not a body-only remediation. |
| 331 | Bilingual gate fails only because PR body declaration is missing | `RETITLE-AND-DECLARE` | Keep the existing branch and add the exact manifest declaration. |
| 332 | Bilingual gate passes; `rust-workspace-test` fails | `HOLD` | The documentation gate is not the blocker. Refer the Rust failure to the responsible domain owner for job-log diagnosis, reproduction, correction, and a green rerun. |
| 333 | Bilingual gate passes; `rust-workspace-test` fails | `HOLD` | Same boundary as PR 332: obtain PR-specific Rust failure evidence, reproduce and correct the failure, then rerun the job successfully. |
| 334 | Head predates the gate script and prompt library; gate cannot run | `REBASE-THEN-MERGE` | Rebase onto `a86b84633239bb1e501372802e68c4ca9cbf06a7`; rerun the workflow and applicable checks. |
| 335 | Ready for review, but head predates the prompt library; gate cannot run | `REBASE-THEN-MERGE` | Rebase onto `a86b84633239bb1e501372802e68c4ca9cbf06a7`; rerun the workflow and applicable checks before review can rely on the gate result. |
| 337 | Chinese normative file changed without English counterpart; PR body declaration also missing | `HOLD` | This is not a declaration-only failure. Supply and review the missing English counterpart, verify the intended source/counterpart mapping, then add the manifest declaration and rerun the gate. |
| 338 | Bilingual gate passes; `rust-workspace-test` fails | `HOLD` | Obtain PR-specific Rust failure logs, reproduction, correction evidence, and a successful rerun from the responsible domain owner. |
| 339 | Bilingual gate passes; `rust-workspace-test` fails | `HOLD` | Obtain PR-specific Rust failure logs, reproduction, correction evidence, and a successful rerun from the responsible domain owner. |
| 340 | Bilingual gate fails only because PR body declaration is missing | `RETITLE-AND-DECLARE` | Keep the existing branch and add the exact manifest declaration. |

**Disposition totals:**

- `RETITLE-AND-DECLARE`: 4 — PRs 320, 328, 331, 340.
- `REBASE-THEN-MERGE`: 6 — PRs 321, 322, 326, 327, 334, 335.
- `HOLD`: 7 — PRs 323, 330, 332, 333, 337, 338, 339.
- `MERGE`: 0.
- `CLOSE-SUPERSEDED`: 0.
- `CLOSE-ABANDONED`: 0.

No PR is being closed as superseded or abandoned: the supplied comparison found that all 17 contain divergent work not duplicated by content already on `main`.

## 3. Exact PR-body declaration

For a PR whose normative changes have complete English/Chinese counterpart coverage, use this exact declaration in the PR body:

```text
BILINGUAL-MANIFEST: COMPLETE
```

The required literal declaration is the complete block above. Do not substitute a paraphrase, a checkbox, or a statement that merely says the change is bilingual.

This declaration is not a substitute for actual counterpart files or semantic review. It must not be used to disguise missing translations, missing counterpart files, or unresolved semantic differences. In particular, PR 337 remains on `HOLD` until its missing English counterpart is supplied and reviewed.

No `BILINGUAL-EXCEPTION: APPROVED` is granted by this decision. An exception must not be self-declared by a PR author. Where an exception is separately authorized by the competent authority, its block must contain the gate's labelled fields with real, non-placeholder values, including a `Due date (YYYY-MM-DD` field. A placeholder, omitted due date, or incomplete labelled field does not satisfy the exception parser.

## 4. Stale-base remediation

The seven stale PR heads are 321, 322, 323, 326, 327, 334, and 335.

For the six without a reported dirty/conflicted state — 321, 322, 326, 327, 334, and 335 — the prescribed target is the exact observed `main` commit:

`a86b84633239bb1e501372802e68c4ca9cbf06a7`

These six are assigned `REBASE-THEN-MERGE`, not unconditional merge approval. A rebase must preserve the PR's intended changes, bring the current gate script and prompt-library tree into the PR head, and be followed by a fresh workflow run. If a rebase produces conflicts or changes the intended patch, stop and return the PR to `HOLD` for review. Do not recreate a PR merely because its head is stale; recreation is only a possible later remedy if the existing branch cannot be safely reconciled and the appropriate owner authorizes it.

PR 323 is different. Its dirty state and 109-commit history mean that a safe rebase cannot be inferred from the supplied facts. It remains `HOLD`; no automatic rebase or recreation is authorized. The conflict-resolution and history-review result must precede a decision on its base.

PR 330 is also `HOLD` because it is already dirty and conflicted. It is not among the seven reported stale-base PRs. Its two missing body declarations are secondary until the conflicted source tree is understood.

## 5. Rust workflow failures

PRs 332, 333, 338, and 339 pass the bilingual documentation gate. Their `unstable` state comes from `rust-workspace-test`, not from the documentation gate.

Their technical convergence is in scope for backlog tracking, but adjudication of the Rust failures belongs to the responsible domain owners. This decision does not infer a common cause or declare the failures harmless.

Each of the four PRs needs its own evidence:

1. The exact failing workflow run and job log for that PR head.
2. A reproducible identification of the failing test, build step, or environment condition.
3. A correction or a documented, independently authorized disposition of the failure.
4. A successful rerun of `rust-workspace-test` against the resulting PR head.
5. Confirmation that the rerun did not invalidate the passing bilingual documentation gate.

Until that evidence exists, all four remain `HOLD`. A passing documentation gate cannot substitute for a failing Rust job.

## 6. G6 — bilingual semantic parity

G6 remains **NOT VERIFIED**.

The bilingual documentation workflow explicitly describes itself as a structural gate. It can check structural conditions such as file presence, counterpart coverage, and the required PR-body declaration. It expressly does not establish paragraph-level semantic equivalence.

G6 requires an evidence-backed, paragraph-level review of the normative source and its counterpart, including:

- a complete inventory of normative files and their language counterparts in the declared scope;
- paragraph-level mapping showing that each source paragraph has the corresponding translated paragraph;
- review of meaning, normative force, conditions, exceptions, modality, terminology, and cross-references in both directions;
- explicit identification and resolution of omissions, additions, contradictions, and semantic drift;
- recorded review evidence and an accountable acceptance decision by the authority empowered to accept bilingual semantic parity.

A green structural CI result alone cannot close G6.

The current PR set can contribute source and counterpart material to a future G6 review. It cannot, as currently evidenced, close G6. PR 337 is specifically incomplete because its changed Chinese normative file has no English counterpart. Other PRs may be included in the review inventory once their source trees and counterpart mappings are stable. No PR merge or declaration is deemed semantic-parity acceptance.

## 7. Authority boundary and unresolved decisions

This decision can classify the observed backlog and prescribe bounded remediation. It cannot manufacture missing authority or evidence.

The following remain outside this ruling:

- **Merge authorization:** No `main`-merge authority is granted. The six `REBASE-THEN-MERGE` dispositions do not bypass the repository's existing review and merge controls. A competent existing merge authority must authorize each merge under those controls.
- **PR 323 conflict/history decision:** The safety of rebasing its 109-commit dirty history cannot be decided without conflict-resolution and patch-preservation evidence. The responsible repository/engineering authority must review that evidence.
- **PR 330 conflict decision:** The resulting tree must be reviewed after conflict resolution; this decision does not authorize resolving or merging it.
- **Rust failures:** Their technical disposition requires the responsible domain owners and PR-specific job evidence.
- **G6 acceptance:** Semantic parity requires qualified independent review and acceptance by the authority designated for that gate. Structural CI cannot supply that authority.
- **Quota unfreeze:** The open-PR count is 17, so the unfreeze threshold of 6 is not met. This ruling does not unfreeze the quota. Any future unfreeze requires a new count at or below 6 and the applicable governance decision.
- **Roles:** No owner, reviewer, maintainer, or domain role is appointed by this plan.

## 8. Acceptance and tracking conditions

The backlog should be considered drained only when the open-PR count is brought within the applicable quota and each remaining PR has an explicit, evidence-backed disposition. A green documentation gate is necessary where applicable, but is not sufficient for Rust, semantic-parity, architecture, or production acceptance.

Track at least these separate outcomes:

1. PR body declarations corrected on 320, 328, 331, and 340.
2. Six stale heads rebased and their current-head workflows rerun.
3. PR 323 and 330 conflict/history decisions recorded before any merge path is reconsidered.
4. Rust workflow failures on 332, 333, 338, and 339 resolved with PR-specific evidence.
5. PR 337's missing English counterpart supplied and reviewed.
6. G6 semantic-parity review completed independently of the structural workflow.
7. Open-PR count remeasured; freeze remains until a separate decision changes it.

**Final ruling:** 17 open PRs; freeze remains active. This is drain-under-freeze, not quota unfreeze. No direct `main` writes, no merge authority, no production activation, and no role appointments are granted.
