---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "The verdict reproduced below is the reviewing session's own text, extracted from its reply and not summarised. Its six blocking items are dispositioned in the manifest's review.round_3, not in this file, so that the reviewer's words stay unedited next to the account of them."
    usage_status: Active
    modification_status: Unchanged
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
---

# Independent governance review — AID-2026-080, round 3

Round 3 of the exact-Head governance review required by section 9. The reviewing session is the
same separate ChatGPT session that performed rounds 1 and 2 (`6b07448b-ac9c-83ec-9115-f056a313f972`),
reading the branch through its own GitHub connector.

| field | value |
| --- | --- |
| Head requested | `489b6048db5095d3bca66b1b438b6399fc05e801` |
| Head reviewed | `489b6048db5095d3bca66b1b438b6399fc05e801` |
| Verdict | `NEEDS REVISION` |
| Blocking items | 6 |
| Requested by | this branch, in `review080_r3.md` |

The reviewer opened by stating, unasked, that PR #1215 had already merged at a later head
`f7bc0789`, and that a verdict on `489b6048` therefore could not be read as coverage of the merge.
That was correct and is the finding this round is mostly about: the repair arrived after the merge.

## Verdict, verbatim

The text below is the reviewer's reply, unedited. It is not a summary and nothing in it has been
reworded. Where it names a defect, the defect was real; the dispositions are in the manifest's
`review.round_3` and in `REVIEW-AMENDMENT.md`, not inserted here.

```
我会把 `489b6048` 作为本轮指定对象，不把 PR 当前状态或分支最新提交替代它。先指出一个需要单独处理的事实：GitHub 当前返回的 #1215 元数据已显示 PR 合并，且其 `head.sha` 是 `f7bc0789…`，不是本轮指定的 `489b6048`。因此，即使 `489b6048` 本身通过审查，也不能据此推定实际合并的 Head 已通过本轮审查。

# Round 3 — Exact-Head governance review

**VERDICT: NEEDS REVISION**

**HEAD REVIEWED:** `489b6048db5095d3bca66b1b438b6399fc05e801`

The central clause correction remains sound. The executed-prompt bytes have been restored without retaking the historical digest, and the Session Evidence check genuinely ran its manifest and digest checks before returning `NOT_APPLICABLE`.

However, I found defects in C8, the population measurements, and the INDEX projection. More importantly, `489b6048` was not the final PR head: GitHub shows #1215 subsequently advanced to `f7bc0789…` and was merged. The required exact-Head review has not been established for that final head.

## 1. Round-2 blocking items

| Round-2 blocker | Result | Finding |
|---|---|---|
| 1. Repair the prompt snapshot without rewriting historical evidence | **CLOSED** | The new-path snapshot has the same Git blob as the old-path snapshot at `a538dbf2`. The recorded digest and byte count were restored, not retaken. |
| 2. Obtain a successful Session Evidence check on the exact Head | **CLOSED for `489b6048`** | The exact-Head check run succeeded. Its `NOT_APPLICABLE` label does not mean the manifest checks were skipped. |
| 3. Review the final merge candidate at its exact Head | **NOT CLOSED** | This review assesses `489b6048`, but the actual PR head later became `f7bc0789…`. That final head has not received the exact-Head governance review required by the blocker. |

### Blocker 1 — the repair is correct

I fetched both:

- `a538dbf289cb21fc04a03fb412c90482619187bc:14-ai-development/work-items/AID-2026-079/prompt-v1.md`
- `489b6048db5095d3bca66b1b438b6399fc05e801:14-ai-development/work-items/AID-2026-080/prompt-v1.md`

They have the **same Git blob SHA**:

`84342823a31a47fdad048e931314b0f0d8e6ca92`

The current manifest also restores the historical values:

- `executed_prompt_sha256`: `08f5e42efdef2c3380056fd8528cf057d6d2a7b25c366566a8599e2aff4df19a`
- `executed_prompt_bytes`: `9932`
- `prompt_sha256` / `prompt_bytes`: the same values.

The original manifest at `a538dbf2` records those same values. The amendment is in `REVIEW-AMENDMENT.md`, not appended to the snapshot.

This is the correct repair. It preserves the historical pin instead of changing the historical claim to fit an amended file.

### Blocker 2 — `NOT_APPLICABLE` is not a skipped validation

<badge color="success">CLOSED</badge>

I independently inspected `_run_checks`, `_historical_not_applicable`, `_check_manifest_entries`, and `check_11_prompt_snapshot_hashes` in the validator at `489b6048`.

The relevant execution path is:

1. The early historical return at lines 2177–2185 applies only when the PR has **no** AI-assisted-work declaration and no session-evidence-reference declaration.
2. This PR declares `AI-assisted work: YES`, so it does not take that early return.
3. On the historical-Issue path, `_run_checks` calls:
   - `check_04_head_tree_evidence_paths`
   - `_validate_reference_scopes`
   - `_check_manifest_entries`
4. `_check_manifest_entries` calls `check_09_manifest_and_evidence_entries` and then `check_11_prompt_snapshot_hashes`.
5. `check_11_prompt_snapshot_hashes` hashes the original Git blob bytes with SHA-256 and separately checks the byte count.

I also verified the dates: Issue #1201 was opened on `2026-11-25`, before the workflow's `2026-12-01T00:00:00Z` effective time.

The actual Session Evidence job for `489b6048` completed successfully. Its log reports:

```text
AI-SESSION-EVIDENCE: NOT_APPLICABLE (linked issue #1201 predates 2026-12-01T00:00:00Z)
```

That is consistent with the validator's historical rule. It is not evidence that the digest comparison was skipped.

The exact-Head GitHub check-runs API returned **16 checks, all completed successfully**, including `Session Evidence`.

## 2. §5 validation items 1–4

| Item | Result | Check and qualification |
|---|---|---|
| 1. Original executed-prompt snapshot independently available | **SATISFIED** | Retrieved the old-path file at `a538dbf2` and the new-path file at `489b6048`; both resolve to the same Git blob SHA. |
| 2. SHA-256 and byte count match recorded execution evidence | **SATISFIED, for the recorded pin** | The old and current manifests both record `08f5e42e…` / `9932`. The exact-Head Session Evidence workflow ran `check_11_prompt_snapshot_hashes`, which checks the raw blob SHA-256 and byte length, and succeeded. This does **not** independently prove the prompt was actually the input used; see C8 below. |
| 3. Review amendment remains separately identifiable | **SATISFIED** | `REVIEW-AMENDMENT.md` contains the amendment separately and explicitly says it is not the executed prompt. The manifest's `prompt_supersession` identifies the retired passage. |
| 4. Session Evidence workflow passes on the resulting exact Head | **SATISFIED** | Retrieved the actual successful `Session Evidence` check run and its log for `489b6048`; confirmed the historical path still executes the manifest and prompt-snapshot checks. |

## 3. C8 — correct invariant, invalid measurement

**C8 does not adequately pin the invariant as written.**

Its intended rule is correct: a review amendment must not change the prompt snapshot that the execution evidence identifies.

But its stated measurement says:

> `git diff --name-only` against the base does not list `AID-2026-080/prompt-v1.md`

That condition is false at this Head.

I compared `8d84c16e...` to `489b6048...`. Git reports:

```text
14-ai-development/work-items/AID-2026-080/prompt-v1.md
status: added
additions: 192
```

The file must appear as an addition because the work item has been renumbered and the new path did not exist at the base. The fact that its bytes match the old-path snapshot does not make the new path disappear from the diff.

There is a second limitation. The validator checks that the current file matches the digest currently recorded in the manifest. If a future amendment changed both the file and the manifest's digest and byte count, that check alone would accept the new pair. It does not independently enforce that the original historical digest remains immutable.

There is also an explicit provenance limitation in the repository:

- The current manifest says `executed_prompt_provenance: NOT_VERIFIED`.
- The original manifest at `a538dbf2` says the same.
- `session-evidence-1201.md` identifies a standing instruction as the “Actual AI input” and records the implementing session identity as `NOT_RECORDED`.

Therefore the evidence proves that the current snapshot matches the recorded historical pin. It does **not** independently establish that `prompt-v1.md` was the actual input executed by the session.

**C8 needs revision.** Its measurement should compare the new-path blob and immutable recorded pin against the original historical snapshot, rather than assert that a newly added path is absent from the base diff. It must also distinguish byte-integrity verification from execution-provenance verification.

## 4. Renumbering — legitimate, not laundering

<badge color="success">LEGITIMATE</badge>

I verified the two registrations:

- `AID-2026-079` now resolves to PR #1078's T92 fault-injection work item, with its own manifest, prompt, and session evidence.
- `AID-2026-080` is the §5 location-rule correction, with its own manifest and work-item directory.

The new manifest explicitly records the reassignment and explains why it occurred. The PR body also explains the collision. The INDEX has separate rows for the two IDs.

The old title in the pinned snapshot:

```text
# AID-2026-079 — Make §5 item (2) satisfiable
```

is **not itself a traceability defect**. It is part of the historical snapshot whose bytes are being preserved. Renaming that title would alter the snapshot and break the historical pin. The manifest and PR body provide the mapping needed to interpret it.

The branch name `gov/aid-079-s5-location` is stale, but a branch name is not the work-item identity authority. The mapping is discoverable elsewhere.

The renumbering itself does not launder the collision. The failure of the duplicate-ID gate to detect two registrations created on separate branches is accurately disclosed as a separate, unauthorized gate-scope issue.

## 5. Additional findings

### F1 — INDEX still records the rejected, retaken prompt pin

<badge color="danger">BLOCKING</badge>

This is the most consequential defect I found beyond the items you identified.

At `489b6048`, the AID-2026-080 row in `14-ai-development/work-items/INDEX.md` still says:

- `11496 bytes`
- SHA-256 `3e0fdfc7…`
- “pin re-taken after the review's round 1 amendment”

That is the exact retaken pin that the round-2 review rejected.

The current manifest and actual snapshot instead record:

- `9932 bytes`
- SHA-256 `08f5e42e…`

The INDEX is therefore materially inconsistent with the repaired manifest and snapshot. It presents the rejected historical-evidence rewrite as the current prompt pin.

The row also still projects `ROUND_1_ACCEPT_WITH_AMENDMENTS`, while the manifest records the round-2 `NEEDS_REVISION` disposition. This is not just an old title or harmless historical note: it is a current registry row containing obsolete and contradictory evidence.

**Required correction:** update the AID-2026-080 INDEX row to the restored digest and byte count, and make its review-state projection agree with the manifest.

### F2 — the manifest population is 56, not 55

<badge color="danger">BLOCKING FOR THE MEASUREMENT CLAIMS</badge>

I queried the recursive Git tree at `489b6048` and counted paths matching:

```text
14-ai-development/work-items/AID-YYYY-NNN/manifest.yaml
```

The result is **56 manifests**, not 55.

The paths include both:

- `AID-2026-079/manifest.yaml` — T92 fault injection
- `AID-2026-080/manifest.yaml` — this work item

This agrees with the reported repository-hygiene result of 56 manifests. It contradicts the 55-manifest denominator in the amendment's measurement and C3/C4.

I have not independently rerun `parse_manifest_session_entries` across all 56 files, so I will not invent a replacement accepted count. The claims `21 of 55` and `48 of 55` are not valid as branch-tip population claims until the population is recounted and the parser measurement rerun.

**Required correction:** rerun the clause and parser measurements over all 56 manifest paths at the exact Head, and update C3, C4, and `REVIEW-AMENDMENT.md` accordingly.

### F3 — the final PR head differs from the reviewed Head

<badge color="danger">BLOCKING</badge>

The PR API currently reports:

| Field | GitHub result |
|---|---|
| PR | #1215 |
| Current PR head | `f7bc07895809d31af443b088fea869b1e6a091a6` |
| Base | `8d84c16ed833786b01e0f490d5ad38e2d5c2c458` |
| Merge commit | `19952b0a86e38d577c7d5c2bfc8c3991ffef6c0f` |
| State | Merged |

The PR commit list contains `489b6048`, followed by a later merge-from-main commit. The comparison from `489b6048` to `f7bc0789` shows two commits and a change to `scripts/check_traceability.py` from the merged main history.

The final head also has 16 successful checks, including Session Evidence. That is useful verification, but it does not substitute for the exact-Head governance review.

This response reviews `489b6048`, not `f7bc0789`. The PR was merged at a later head without the required exact-Head review being established here. The actual integration is a GitHub fact; it does not by itself establish that the merge satisfied the standard's review requirement.

### F4 — merge-state projection is stale after integration

The current work-item manifest still records:

```yaml
implementation:
  status: NOT_STARTED
  pull_request: PENDING
  merge_commit_sha: NOT_MERGED
```

The INDEX row still says `PR_OPEN`.

GitHub now reports PR #1215 merged at `19952b0a…`. These repository records need a post-merge update. This is a state-projection defect, not evidence that the renumbering was illegitimate.

### F5 — the clause change and non-exemption sentence are correctly scoped

<badge color="success">PASS</badge>

I compared the actual standard at `8d84c16e` and `489b6048`:

- `PR-GOVERNANCE-001.md` has 2 additions and 2 deletions.
- The English and Chinese clause lines are the two changed lines.
- The English non-exemption sentence is byte-identical.
- The Chinese non-exemption sentence at line 151 is byte-identical.
- No other sentence in that paragraph changed.

The compare against the requested base also confirms the nine changed paths you listed. No path under `scripts/`, `.github/`, `tests/`, or `crates/` is part of the `489b6048` change set.

The location wording remains acceptable. It constrains the two location classes and does not incorrectly require one particular `session_evidence` entry. The principal-identity requirement remains untouched; its unresolved registry dependency is a separate issue.

## 6. Required closure before treating the work item as accepted

**Blocking**

1. Correct C8's measurement so it compares the new-path snapshot to the original historical snapshot and does not rely on the false “not listed in the base diff” condition.
2. Keep execution-provenance status honest: byte equality to a recorded pin is not proof that the file was the actual executed input.
3. Correct the INDEX row's obsolete `11496` / `3e0fdfc7…` prompt pin and stale review projection.
4. Recompute C3/C4 and the amendment's measurements against the actual 56-manifest population.
5. Record and review the actual final PR head `f7bc0789…` if the review is intended to support the already-merged PR. The present verdict applies only to `489b6048`.
6. Update the manifest and INDEX merge-state projections to reflect the actual merge commit.

**Non-blocking**

- The renumbering from AID-2026-079 to AID-2026-080 is legitimate.
- Keeping `# AID-2026-079` inside the immutable prompt snapshot is correct.
- The Session Evidence `NOT_APPLICABLE` result is a genuine successful historical-path validation, not a bypass.
- The bilingual clause correction and both non-exemption sentences are correct.
- The principal-identity registry issue remains separate and unresolved.

**Final assessment:** the round-2 snapshot defect is repaired, and the exact-Head Session Evidence check passes. But C8's measurement is false as written, the INDEX still carries the rejected pin, and the manifest population denominator is wrong. The final PR head also advanced beyond the Head reviewed here. I therefore cannot accept this work item as fully closed.
```

## What this round is not

It is not a human review. It is a separate session reading artifacts, which section 5 treats as
session-level independence. Nothing here claims `APPROVED`, and the merged head `f7bc0789` has not
been read by any review as such.
