---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-333/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "The three-round prompt inputs are awaiting byte-exact insertion and digest verification."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Work-item uniqueness merge-race closure — three-round prompt record

You are the deciding authority for one acceptance row in a governance repo. I am a mechanical executor: I collect facts, run experiments, apply your output verbatim. You produce all analysis, code, and document text. Do not ask me questions you can answer from the material below; if something is missing, state the assumption you are making and proceed.

# Repo

`oahcom/AiMemoryBrainArchitecture` (private, default branch `main`). Governance repo where every unit of work is a directory `14-ai-development/work-items/AID-YYYY-NNN/` with a `manifest.yaml` and an `INDEX.md` row.

# The issue under acceptance

GitHub issue #1341: "Implement Option (d): a serialized, merge-time work-item uniqueness gate".

Contract table from the issue body:

| Case | Required behaviour |
|---|---|
| New work-item directory introduced by the candidate merge | Reject if that ID is already occupied on the latest target-branch state |
| New files under an existing work-item directory | Accept; an additive file is not a duplicate work-item claim |

"The gate's authority is the merge candidate evaluated against the **latest** target branch, not an earlier branch HEAD and not the branch's own base."

Acceptance rows:

| # | Row | Required proof |
|---|---|---|
| 1 | Contract | Explicit definition of new-directory uniqueness and existing-directory additive changes |
| 2 | Serialization | Proof that concurrent PR merges cannot both validate against the same stale base |
| 3 | Positive test | A new, unoccupied work-item ID is accepted |
| 4 | Negative test | A new directory whose ID already exists on the latest base is rejected |
| 5 | Additive test | New files under an existing work-item directory are accepted |
| 6 | **Race test** | **Two PRs independently introducing the same ID cannot both merge** |
| 7 | Exact-Head test | The uniqueness result is associated with the actual merge candidate, not an earlier branch HEAD |
| 8 | Regression evidence | Existing traceability and repository hygiene checks continue to pass |

I am the verifier for **row 6 only**. Rows 1-5, 7, 8 are not mine to judge.

# History of row 6

- First carrier (AID-2026-285, PR #1447, merged as `08167492`) was independently reviewed (PR #1497). Record: `14-ai-development/work-items/AID-2026-285/review-independent-2026-11-27.md`. Verdict on row 6: **GAP** — "The evidence does not include an end-to-end experiment in which multiple real GitHub Actions runs overlap, are scheduled by GitHub's concurrency service, and are then evaluated against the protected branch's required-check behavior." The reviewer also measured that two candidates introducing the same `AID-…/` directory from the same base both passed, both merged, and the post-merge check reported `introduced=0 occupied=0`, leaving the duplicate on the merged tree. The PR body's claim that `required_status_checks.strict: true` closed this was false: measured `strict = False`, `rulesets: []`.
- `main` then replaced that checker under AID-2026-311 (PR #1477, "tree-only work-item uniqueness verdict"). Whether that closes row 6 is what I had to measure.

# Current checker on origin/main (`scripts/ci/check_work_item_uniqueness.py`, verbatim)

```python
#!/usr/bin/env python3
"""Compare work-item directory contents using only the base and candidate trees.

No commit ancestry, merge-base, branch name, or commit ordering participates in
the verdict. Exit codes: 0 PASS; 1 VIOLATION/DELETION; 2 INCOMPLETE.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROOT = "14-ai-development/work-items"
PATTERN = re.compile(r"^14-ai-development/work-items/(AID-\d{4}-\d{3})/")
TIMEOUT = 30

class Incomplete(RuntimeError):
    """An input tree or required Git object cannot be read."""

def run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise Incomplete(f"git {args!r}: {type(exc).__name__}: {exc}") from exc
    if result.returncode:
        raise Incomplete(
            f"git {args!r} exited {result.returncode}: {result.stderr.strip()}"
        )
    return result.stdout.strip()

def resolve_tree(ref: str, label: str) -> str:
    if not ref:
        raise Incomplete(f"{label} ref is empty")
    return run_git("rev-parse", "--verify", f"{ref}^{{tree}}")

def item_paths(tree: str) -> dict[str, set[str]]:
    """Return each AID's tracked file paths relative to its directory."""
    paths: dict[str, set[str]] = {}
    for name in run_git("ls-tree", "-r", "--name-only", tree, "--", ROOT).splitlines():
        match = PATTERN.match(name)
        if match:
            item_id = match.group(1)
            prefix = f"{ROOT}/{item_id}/"
            paths.setdefault(item_id, set()).add(name[len(prefix):])
    return paths

def check(base_ref: str, head_ref: str) -> int:
    try:
        base_tree = resolve_tree(base_ref, "base")
        candidate_tree = resolve_tree(head_ref, "candidate")
        base_items = item_paths(base_tree)
        candidate_items = item_paths(candidate_tree)
    except Incomplete as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    violations: list[tuple[str, list[str]]] = []
    deletions: list[str] = []

    for item_id in sorted(base_items.keys() | candidate_items.keys()):
        if item_id not in candidate_items:
            deletions.append(item_id)
            continue
        if item_id not in base_items:
            # A new declaration is permitted. Merge queue serializes races.
            continue

        added_paths = sorted(candidate_items[item_id] - base_items[item_id])
        if added_paths:
            violations.append((item_id, added_paths))

    for item_id, added_paths in violations:
        print(
            f"VIOLATION: {ROOT}/{item_id} "
            f"new_paths={','.join(added_paths)}"
        )
    for item_id in deletions:
        print(f"DELETION: {ROOT}/{item_id} exists_on_base=true absent_on_candidate=true")

    if violations or deletions:
        verdict = "VIOLATION" if violations else "DELETION"
        print(
            f"WORK-ITEM UNIQUENESS: {verdict} "
            f"(base_tree={base_tree} candidate_tree={candidate_tree} "
            f"violations={len(violations)} deletions={len(deletions)})"
        )
        return 1

    print(
        "WORK-ITEM UNIQUENESS: PASS "
        f"(base_tree={base_tree} candidate_tree={candidate_tree} "
        f"violations=0 deletions=0)"
    )
    return 0

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="baseline commit or tree")
    parser.add_argument("--head", required=True, help="candidate commit or tree")
    args = parser.parse_args(argv)
    return check(args.base, args.head)

if __name__ == "__main__":
    sys.exit(main())
```

Its test file `scripts/ci/test_work_item_uniqueness.py` has 9 tests, all passing on main: four construction variants (`ordinary_pr`, `update_branch` rewritten merge-base, `squash`, `merge_group` two-parent synthetic commit) must all yield the identical `(base_tree, head_tree, exit=1, VIOLATION)` verdict for "add a file under an existing work item"; plus `test_new_declaration_is_allowed` (exit 0), deletion tests, an "only rev-parse and ls-tree" instrumentation test, and an INCOMPLETE test.

# Current wiring (`.github/workflows/document-management.yml`, job `GOV-DOC-002 metadata checks`)

Triggers: `pull_request: [opened, synchronize, reopened, ready_for_review]` and `push: branches: [main]`. **No `merge_group` trigger.** Concurrency group is per workflow + per PR/ref with `cancel-in-progress: false`; the comment says global serialization was deliberately abandoned because "the single pending slot replaced queued runs".

The step:

```yaml
      - name: Enforce work-item uniqueness against the current target base
        env:
          PR_BASE: ${{ github.event.pull_request.base.sha }}
          BASE_REF: ${{ github.event.pull_request.base.ref }}
          PUSH_BEFORE: ${{ github.event.before }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail

          if [ -n "$BASE_REF" ] && [ -n "$PR_BASE" ]; then
            git fetch origin "+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"
            python3 scripts/ci/check_work_item_uniqueness.py \
              --base "refs/remotes/origin/$BASE_REF" \
              --head "$CANDIDATE_SHA"
          elif [ -n "$PUSH_BEFORE" ] && [ "$PUSH_BEFORE" != "0000000000000000000000000000000000000000" ]; then
            python3 scripts/ci/check_work_item_uniqueness.py \
              --base "$PUSH_BEFORE" \
              --head "$CANDIDATE_SHA"
          else
            python3 scripts/ci/check_work_item_uniqueness.py
          fi
```

Note: on a PR event the step re-fetches the *current* target tip at run time, so the PR check is already evaluated against the latest target as of that run. On a push to `main`, base is `github.event.before` (the tip before the push) and head is the new tip.

`GOV-DOC-002 metadata checks` is one of 16 required contexts on `main`.

# Measured platform state (2026-11-28, token has repo admin)

- `GET /branches/main/protection` → `required_status_checks.strict = False`; contexts: `GOV-DOC-001 structural checks`, `Branch freshness vs base`, `audit`, `GOV-DOC-002 metadata checks`, `BMCP protocol index (hard gate)`, `BMCP conformance suite (hard gate)`, `Schema non-empty audit (hard gate)`, `Bilingual docs coverage (ratchet)`, `Rust clippy (hard gate)`, `Repository hygiene (hard gate)`, `Rust format (hard gate)`, `Rust doctests (hard gate)`, `Session Evidence`, `Session Evidence self-test (base)`, `Session Evidence self-test (head)`, `rust-workspace-test`.
- `GET /rulesets` → `[]`. GraphQL `branchProtectionRules` → `[{pattern: "main", requiresStrictStatusChecks: false, isAdminEnforced: true}]`. No merge queue is configured anywhere.
- Seven workflows *do* declare `merge_group:` (`gates.yml`, `repository-hygiene.yml`, `session-evidence.yml`, `branch-freshness.yml`, `bilingual-docs.yml`, `rust-phase1.yml`, `runner-admission-policy.yml`) with comments like "the queue only reports checks produced by `merge_group`". `document-management.yml` does not.

# Related post-merge detector that already exists

`scripts/check_traceability.py --index-only`, run as a step in `repository-hygiene.yml` ("Check INDEX rows against the work-item tree", a required context, triggered on `pull_request` and `push: main`). It asserts one row per AID (`T-04 duplicate INDEX entry {aid}`), every row resolves to a manifest, every manifest on disk is indexed. `.gitattributes` gives `14-ai-development/work-items/INDEX.md` `merge=union`, with a comment saying union is only safe because that duplicate detector runs.

`scripts/ci/check_repository_hygiene.py` additionally enforces tree-vs-INDEX membership (46 dirs ↔ 46 links, both directions).

# Experiment I ran (scratch repo, real checker copied from origin/main, real `.gitattributes`)

Scratch repo layout mirrors the governed paths: `14-ai-development/work-items/INDEX.md` (header + one row for AID-2026-001), `AID-2026-001/manifest.yaml`, `scripts/ci/check_work_item_uniqueness.py`, `.gitattributes` with `INDEX.md merge=union`. `B0` = baseline commit.

**Variant 1** — two claimants, same new AID dir, different files (A adds `AID-2026-999/manifest.yaml` + an INDEX row; B adds `AID-2026-999/evidence.md`, no INDEX row):

| Step | Command | Exit |
|---|---|---|
| A's PR gate at open | `check --base B0 --head A` | **0** PASS |
| B's PR gate at open | `check --base B0 --head B` | **0** PASS |
| A merged into main → M1; push check on main | `check --base B0 --head M1` | **0** PASS |
| B re-validated against post-A base | `check --base M1 --head B` | **1** VIOLATION `AID-2026-999 new_paths=evidence.md` |
| merge candidate containing A | `check --base M1 --head M2` | **1** VIOLATION `new_paths=evidence.md` |
| push check on main after B merged (M2) | `check --base M1 --head M2` | **1** VIOLATION `new_paths=evidence.md` |

Merged tree of M2 contains `AID-2026-999/evidence.md` and `AID-2026-999/manifest.yaml`; INDEX has exactly one row for AID-2026-999 (so the T-04 duplicate-row detector does **not** fire here — one claimant registered the row, the other never did).

**Variant 2** — both claimants add the same path `AID-2026-999/manifest.yaml` with different content and their own INDEX rows: both PR gates 0, `git merge` itself exits 1 with a textual conflict on `manifest.yaml`; after a hand resolution that keeps both INDEX rows, every checker run (re-run against post-A base, merge candidate, post-merge push) returns **0** PASS — the checker compares path sets only, so same-path/different-content is invisible to it. The only thing that stopped the second merge in V2 was git's own textual conflict, not the gate.

# What I need from you

1. **Verdict on row 6**, as one paragraph a reviewer can quote, grounded in the exit codes above and the measured platform state. Say plainly whether "two PRs independently introducing the same ID cannot both merge" holds today, and exactly which window remains open (naming the mechanism, not the symptom). Do not soften.

2. **If it does not hold**: the minimal mechanism that makes it hold, chosen from what this repo can actually carry. Constraints I have measured and you must respect:
   - I have repo admin on the token, so a settings change (strict, merge queue) is *possible* but is not a code change and cannot be reviewed in a PR; the owner would have to accept it. Say so explicitly if your mechanism requires one, and give me the exact API call so the record is complete.
   - A code-only mechanism cannot make GitHub re-run a check; it can only (a) make the two candidates' trees conflict, (b) make the post-merge push check fail loudly and name both claimants, or (c) require a queue trigger. Pick what you judge sufficient for the row as worded, and argue why the row is then satisfied rather than merely detected.
   - Whatever you pick must come with **a test that is red on `origin/main` and green after**, runnable by `python3 scripts/ci/test_work_item_uniqueness.py` (unittest, no third-party deps, no network), and it must not weaken any of the 9 existing tests.
   - The existing checker's design constraint is deliberate: only `rev-parse` and `ls-tree` are permitted git commands (there is an instrumentation test asserting exactly that). If your mechanism needs another git command (`rev-list`, `cat-file`, `merge-base`…), you must also give me the replacement instrumentation test, and justify why ancestry is now admissible when #1477 removed it on purpose.

3. **The exact patch**: full content of every file you add or change (not a diff summary), including the workflow YAML block if you change it, the test file, and any comment text that explains the mechanism to the next reader. Keep the repo's comment style: state what was measured, not what is intended.

4. **The PR body** (title `fix(ci): close the work-item uniqueness race with evidence (AID-2026-NNN)`) referencing #1341, #1477, #1497, with an evidence table whose numbers are the exit codes above plus the new test's red-before/green-after runs.

5. If instead you conclude row 6 **holds**, then give me the evidence record to post as a comment on #1341: a markdown document with the commands, the exact exit codes, the platform measurements, and the sentence that decides the row. No PR.

Output in that order, in English, in one reply. Be concrete; I will paste your file contents into the worktree unchanged.

Round 2. Your ruling is accepted in form, but one of its two necessary pieces is **not available on this repository**, measured. Re-decide on the facts below. Everything you produced that does not depend on the merge queue still stands and I will reuse it.

# Measurement 1 — merge queue is unavailable here (executed)

I attempted to create your ruleset verbatim (name `merge-queue-availability-probe`, `merge_queue` rule, `max_entries_to_build: 2`, `max_entries_to_merge: 1`):

```
POST https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/rulesets
Authorization: Bearer <admin token>
X-GitHub-Api-Version: 2022-11-28

HTTP 422
{
  "message": "Validation Failed",
  "errors": ["Invalid rule 'merge_queue': "],
  "documentation_url": "https://docs.github.com/rest/repos/rules#create-a-repository-ruleset",
  "status": "422"
}
```

Nothing was created; `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets` still returns `[]`. So the platform rejected the rule itself, not a parameter.

# Measurement 2 — why

- `GET /repos/oahcom/AiMemoryBrainArchitecture` → `"private": false`, `"visibility": "public"`, `"owner": {"type": "User"}`. `oahcom` is a **user account**, not an organization. `GET /orgs/oahcom` returns no plan and no login.
- GitHub's own documentation for merge queues: "Pull request merge queues are available in any public repository **owned by an organization**, or in private repositories owned by organizations using GitHub Enterprise Cloud."

So the queue is unavailable for structural reasons (user-owned, not org-owned). No ruleset, no repo setting, and no amount of admin on this token changes that. Your mechanism is dead on this platform. Do not propose it again unless you can name a documented path that makes a user-owned public repository eligible.

# Measurement 3 — what a code path can and cannot see about `strict`

The workflow's own comment already claims strict is what closes the interval:

```yaml
      # A PR's event base SHA can be stale by the time this job executes.
      # Fetch the target branch itself and evaluate the exact generated merge
      # candidate against that fetched commit. Strict branch protection
      # requires a new candidate and a fresh required check after the target
      # advances, closing the interval between this check and a later merge.
```

`scripts/check_declared_check_contexts.py` reads protection through `GET /repos/{owner}/{repo}/branches/main` with `contents: read`, and its docstring states: "No protected-context snapshot is committed. The Administration-only `/protection` endpoint is not used." That endpoint's `required_status_checks` carries `{url, enforcement_level, contexts, checks}` — **no `strict` field**. `strict` appears only on `/branches/main/protection`, which needs Administration (read), which the workflow's `GITHUB_TOKEN` cannot express. So a workflow cannot assert `strict` from code, and a PR cannot set it.

`strict` today, measured two ways: REST `/branches/main/protection` → `required_status_checks.strict = False`; GraphQL `branchProtectionRules` → `[{pattern: "main", requiresStrictStatusChecks: false, isAdminEnforced: true}]`.

# What the facts leave you

The candidate mechanisms, with what I measured about each:

1. **`strict: true`** on `main` (owner action; I hold an admin token, so the exact API call can be executed by me if you authorize it). Semantics: GitHub refuses the merge while the PR branch is behind the base, and forces a new candidate plus a fresh run of every required context. The uniqueness check re-fetches the target tip at run time (`git fetch origin +refs/heads/main`), so the forced re-run evaluates against a base that contains A and returns 1. Code cannot assert it afterwards; the drift the #1497 review found (a PR body claiming `strict: true` while the platform said `False`) would therefore remain unobservable to CI.
2. **A push-path detector that uses ancestry**: on the `push` event, base = `github.event.before`, head = new tip. If a merge commit has two parents and a given `AID-…/` directory is absent from *both* parents' trees but present in the merge tree, then two independent claimants each introduced that directory and both merges landed. Both parent SHAs and their subject lines ("Merge pull request #A", "Merge pull request #B") name the two claimants. This is detection after the fact, and it is the only mechanism that names both claimants. It needs `rev-list --parents` and per-parent `ls-tree`, which breaks the current instrumentation test's "only `rev-parse` and `ls-tree`" contract unless the check is a separate script (a new step in an already-required context, so no new required context is created).
3. **`strict: true` plus 2**, i.e. prevention by the platform and a named-claimant alarm when the setting is not in force.
4. Anything else you can justify.

I am not choosing. You are. Constraints that do not move:

- The change must be reviewable as a PR; a settings change cannot be, so if your mechanism needs one, say exactly which API call the owner must run and treat it as a precondition recorded in the PR, not as evidence.
- Row 6 is "Two PRs independently introducing the same ID cannot both merge". A mechanism that only detects the duplicate after both merged does not satisfy the wording; say so plainly if that is what you end up choosing, and say what would then be needed for the row to hold.
- Any test must run under `python3 scripts/ci/test_work_item_uniqueness.py` (unittest, stdlib only, no network), be red on `origin/main` and green after your patch, and not weaken the 10 existing tests.
- If your mechanism needs a new script, it needs a self-test and it must be wired into a step of a job that is already a required context (`GOV-DOC-002 metadata checks`, `Repository hygiene (hard gate)`, `GOV-DOC-001 structural checks`, …). Creating a new required context requires an owner action and a document change, so avoid it.
- The existing checker `scripts/ci/check_work_item_uniqueness.py` stays tree-only unless you argue otherwise; the #1477 rewrite removed ancestry on purpose and I will not undo it by accident.

# Also needed, whatever you decide

I will open the PR as `fix(ci): close the work-item uniqueness race with evidence (AID-2026-333)`. AID-2026-333 is reserved by me: it is absent from `main`'s work-item tree (occupied above 325: 325, 326, 340), absent from `aid-ledger` (which holds 281-287, 312, 313, 331, 332), and absent from all 1180 `origin/*` refs. `origin/main` is `cc3e9ed9dbe0eb860a583bc51d6b086248624766` at the time of writing.

Produce, in this order:

1. **The re-decision**, one paragraph, in the form a reviewer can quote: whether row 6 holds after your mechanism, and what is left open.
2. **The exact patch**: full content of every file added or changed. Nothing abbreviated. Comment style: state what was measured.
3. **The tests**: full file content, and the exact red-before command and its expected failure text.
4. **The owner action** (if any): the literal HTTP call, and where in the PR body it is recorded.
5. **The work-item registration for AID-2026-333**, conforming to the repo's existing shapes:
   - `14-ai-development/work-items/AID-2026-333/manifest.yaml`, modeled on AID-2026-311's manifest (I reproduce it below). Use `{{PROMPT_SHA256}}` and `{{PROMPT_BYTES}}` where the executed-prompt digest belongs — I will substitute the real values of the prompt snapshot I commit, computed from the two round files.
   - `14-ai-development/work-items/AID-2026-333/evidence.md`, whose metadata header follows the same shape as the other work records, containing the experiment table with the exit codes from round 1 plus the red-before/green-after runs.
   - `14-ai-development/work-items/AID-2026-333/session-evidence.md` in the shape the repo's Session Evidence gate expects (I will send you the gate's failure output if it rejects the first attempt).
   - The `INDEX.md` row, for this exact 10-column table:

```
| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
```

   - `14-ai-development/work-items/AID-2026-333/prompt-v1.md`: do not write this; I commit the two round files as the snapshot under a heading per round.
6. **The PR body**, with the evidence table.

AID-2026-311's manifest, verbatim, as the shape to follow:

```yaml
work_item_id: AID-2026-311
title: "Preserve work-item claim identity across Update branch in the uniqueness gate"
class: GATE/TEST
risk: R1
risk_rationale: >-
  Strengthens only the existing work-item uniqueness checker and its unit
  suite. No workflow, branch-protection, or merge-queue setting is touched.
status: DISPATCHED
id_status: PROVISIONAL
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED
acceptance_authority: NOT_ASSIGNED
attribution: "user-authorized operator (delegated by account owner)"
date: "2026-11-27"
repository:
  name: oahcom/AiMemoryBrainArchitecture
base_branch: main
base_commit_sha: 460f437eb3496e10737b9ef20f4b816e34d155c4
prompt_status: RECORDED_NOT_FROZEN
prompt_provenance: USER_AUTHORIZED_DELEGATED_REQUEST
identifier_allocation:
  id_status: PROVISIONAL
  observed_main: 460f437eb3496e10737b9ef20f4b816e34d155c4
  assigned_id: AID-2026-311
  allocation_rule: >-
    Checked the work-items directory on main and all pages of
    pulls?state=all&per_page=100 (pages 1 through 11); no AID-2026-311 through
    AID-2026-318 directory or PR title/body occurrence was found.
  recheck_rule: >-
    Recheck the directory and all-state PR listing immediately before opening
    or updating the PR.
scope:
  objective: >-
    ...
  changes:
    - path: "scripts/ci/check_work_item_uniqueness.py"
      detail: >-
        ...
  untouched:
    - "GitHub merge queue and branch protection settings"
non_goals:
  - "..."
evidence:
  record: "14-ai-development/work-items/AID-2026-311/evidence.md"
  prompt: "14-ai-development/work-items/AID-2026-311/prompt-v1.md"
  session: "14-ai-development/work-items/AID-2026-311/session-evidence.md"
documentation:
  - path: "scripts/ci/check_work_item_uniqueness.py"
    relationship: implementation
session_evidence:
  - role: "IMPLEMENTATION_SESSION"
    issue_refs:
      - "#1341"
    implementing_ai_session: "ChatGPT-GPT-6"
    executed_prompt_snapshot_file: "14-ai-development/work-items/AID-2026-311/prompt-v1.md"
    executed_prompt_sha256: "5a0d7d057a150fe009f97d07b8384934c297fcbfe6d149ffa8a5a2ab7bf17c7e"
    executed_prompt_bytes: 2821
    executed_prompt_provenance: "NOT_VERIFIED"
    session_reference_status: "RECORDED"
    session_evidence_ref: "14-ai-development/work-items/AID-2026-311/session-evidence.md"
implementation:
  status: IN_PROGRESS
  summary: >-
    ...
  files_changed:
    - "scripts/ci/check_work_item_uniqueness.py"
  tests:
    - "..."
```

Two notes on that template: the `class`/`risk` vocabulary in this repo is `GATE/TEST`, `DOC/GOVERNANCE`, `IMPL/TEST`, `Infrastructure`; `risk` is `R1`-`R3` or `Medium`; and the INDEX table has ten columns but rows in the table are sometimes written with fewer cells, so keep exactly ten.

Output everything in one reply, English, no preamble.

Round 3. Files A, B, C, D, E, F are applied to a worktree branched from `cc3e9ed9dbe0eb860a583bc51d6b086248624766`. Two measured results, then two small things I still need from you.

# Measured — red before (exit 1)

Command, with the original `main` workflow restored and your new test file in place:

```
python -X utf8 scripts/ci/test_work_item_uniqueness.py WorkItemUniquenessTreeTests.test_push_detector_is_wired_and_strict_limitation_is_recorded
```

Result: `Ran 1 test`, `FAILED (failures=1)`, exit 1, and the assertion text is exactly what you predicted:

```
AssertionError: 'Strict protection is an owner-side' not found in 'name: Architecture document management gate
...
' : workflow must record strict protection as an external prerequisite
```

# Measured — green after (11 of 12 pass; the twelfth is a pre-existing Windows-only failure)

Command, with all of your files applied:

```
python -X utf8 scripts/ci/test_work_item_uniqueness.py
```

Result: `Ran 12 tests in 16.055s`, `FAILED (failures=1)`. The single failure is `test_checker_executes_only_rev_parse_and_ls_tree`:

```
File "...\test_work_item_uniqueness.py", line 287, in test_checker_executes_only_rev_parse_and_ls_tree
    self.assertEqual(
AssertionError: 9009 != 1 :
```

Cause: that test spawns the checker with the literal interpreter `"python3"` (not `os.environ["PYTHON"]`), and on this Windows host `python3` resolves to the Microsoft Store stub, exit 9009. It is **pre-existing, not caused by your patch**: I ran the same test from `origin/main`'s own test file and checker in a clean directory and got the identical `AssertionError: 9009 != 1 :`. On ubuntu-latest, which is where the gate runs, `python3` is real. Your new test `test_push_detector_reports_both_independent_claimants` passes, and so does the wiring test, and the other nine.

Decision needed only if you disagree: I am recording this as "11 pass, 1 pre-existing Windows interpreter-resolution failure reproduced identically on origin/main; CI is authoritative" rather than changing `"python3"` to a portable resolution. If you want it fixed, say so and give the replacement lines.

# Correction you made, confirmed

You were right about the INDEX table: the header is nine columns (`Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance`), your row has nine cells, and I am inserting it as the first data row of the table. Nothing to redo.

# What I still need

1. `14-ai-development/work-items/AID-2026-333/prompt-v1.md`. It needs the same `document_metadata` header shape as the other work records (see AID-2026-311's, which I reproduce below), then a title, then the two round inputs. Write it with two literal placeholder lines, `{{ROUND_1}}` and `{{ROUND_2}}`, where the round bodies go — I insert the byte-exact contents of the two prompt files I actually sent and then compute the digest that fills `{{PROMPT_SHA256}}` and `{{PROMPT_BYTES}}` in the manifest. Do not paraphrase the rounds; do not paste them back.

2. A date correction. Today is **2026-11-28**, and the round-1 experiment was executed on 2026-11-28. Your `manifest.yaml`, `evidence.md` and `session-evidence.md` carry `date: "2026-11-27"` and `last_verified_date: "2026-11-27"`. Re-issue only the lines that change, in a form I can apply with exact string replacement: for each file, the old line and the new line. If a date appears inside prose rather than as a `date:`/`last_verified_date:` field, leave the prose alone and say so.

3. If the measured red-before/green-after results above change any sentence in `evidence.md` section 5 or in the PR body's regression table (they currently say "expected", and I now have actual values), give me the replacement sentences, marked by the section they belong to. Keep them factual: 11 of 12 pass on Windows, the twelfth is pre-existing, CI runs ubuntu.

For reference, AID-2026-311's `prompt-v1.md` header:

```markdown
---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-311/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation and CI verification are pending independent review."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
```

Output the file in full, then the replacement table for point 2, then the sentence replacements for point 3. English, no preamble.
