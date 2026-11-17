# Session 4 — A: H Branch Baseline Integrity Incident
# Session 4 — A：H 分支基线完整性事件

- Date: 2026-11-18
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Main HEAD: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`; tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`
- H branch HEAD: `0277a8b9ee63be850acc0b8b1b08625524aaa33b`
- H parent / last reviewed H HEAD: `0d36324457e39bd50ad56ae902d477c4ea765b61`
- Disposition: **DEFERRED — CRITICAL BASELINE INTEGRITY REGRESSION**
- Scope: read-only detection and governance escalation. No Owner branch mutation.

## 1. Incident summary

While continuing the H 1.2.15 issuer-side closure review, the H branch had advanced by one commit:
`0277a8b9ee63be850acc0b8b1b08625524aaa33b`
Message: `docs(H): record exact Applied delivery evidence mapping decision`.

The commit's parent is exactly the last reviewed H HEAD `0d36324457e39bd50ad56ae902d477c4ea765b61`. The GitHub commit endpoint reports 160 additions and 92,969 deletions. The compare endpoint identifies 205 removed files and three workflow renames. The current recursive H tree contains only seven entries, including two new Phase 3.8.23 review documents and three workflows. The prior 1.2.15 schema, validators, tests, fixtures, and the bulk of the H protocol source are absent from the current H branch tree.

This is not a normal additive evidence update. It is a destructive branch-level baseline change that makes the previous H source bundle unavailable from current H HEAD.

## 2. Main isolation check

Current main HEAD is `e52594f181d2edb77448adcfed64a0fbdffaf3aa`, with tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`, exactly the same tree previously recorded for main. The destructive H branch commit is not on main. No change to main's file tree was detected.

The A review PR #67 remains OPEN / DRAFT / unmerged and retains its original two-file report head `abd9156d3e9aa171eeb03693b2be1e722e8d33ff`. It does not contain or merge the H branch deletion commit.

## 3. Impact on prior 1.2.15 conclusions

The previous successful CI evidence remains historically attributable only to old H commit `0d363244...`:
- Provider Outcome run `44079842914`: 91 tests, 0 failures.
- Recovery Cutoff run `44079842878`: 288 tests, 22 skipped, 0 failures.

Those runs do not validate the new H HEAD `0277a8b9...`. No current-head CI evidence was established in this review. Because the 1.2.15 schema/validator/test files are absent from the current H tree, the previous exact bundle cannot be considered the current H branch candidate.

The issuer-side C-before-H-signing gap, production Trust/Key lifecycle, origin transport authentication and durable replay gaps remain unresolved. This branch regression is an additional critical blocker, not a substitute for those conditions.

## 4. Required recovery actions

| ID | Owner | Required evidence | Closure |
|---|---|---|---|
| H-BI-01 | H | Explicitly explain the intent and scope of commit `0277a8b9...`; identify whether the mass deletion is intentional, accidental, or a branch migration | H Owner decision recorded against exact commit |
| H-BI-02 | H | Restore or formally relocate the authoritative H protocol source, schemas, validators, tests, fixtures and workflows; no silent loss of current contracts | Exact current tree inventory and source pins |
| H-BI-03 | H | Publish a new immutable 1.2.15 candidate manifest based on the recovered current H tree | Exact blob manifest read back |
| H-BI-04 | H | Rerun required CI against the recovered exact H HEAD; establish no skipped/missing critical 1.2.15 suites | Successful run/job SHA evidence |
| H-BI-05 | C + I + A | Re-review the recovered exact bundle; prior reviews do not transfer automatically across changed/missing blobs | Exact-version C/I decisions and A rereview |

No deadline is invented. A condition closes only when the listed evidence is published and read back.

## 5. Governance disposition

**DEFERRED.** Treat H 1.2.15 as NOT CURRENTLY PRESENT IN THE H BRANCH HEAD. The previous successful CI is historical evidence for the previous commit only. Do not claim current H conformance, schema freeze, Gate A completion, Gate B/C readiness, or production authorization.

Do not revert, force-push, or otherwise mutate the H Owner branch from this coordinating review. H must provide the intent and recovery decision. Do not merge PRs, close Issues, or release Gates.

