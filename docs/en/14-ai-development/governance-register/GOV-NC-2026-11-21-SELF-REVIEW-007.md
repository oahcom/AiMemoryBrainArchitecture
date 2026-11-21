# GOV-NC-2026-11-21-SELF-REVIEW-007 — The "fix" for zero-review merges is one account reviewing itself

- Register ID: GOV-NC-2026-11-21-SELF-REVIEW-007
- Status: `ACCEPTED` / `SELF_REVIEW_IDENTIFIED` / S-2 `APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED`
- Defect class: Governance Conformance — Independence of Review
- Severity: High
- Found at: 2026-11-21T05:50Z
- Prior register: GOV-NC-2026-11-20-MERGE-AFTER-RULING-003 (zero-review merges, count frozen at 4)
- Related: PR-GOVERNANCE-001 section 5 (independent review), the incidental ruling in the #403 review, GOV-NC-2026-11-20-CI-NOT-EXECUTED-005

---

## 1. Bottom line

The four "zero-review merges" recorded in `MERGE-AFTER-RULING-003` share one observable feature: `reviews = 0`. **That feature is gone.** It has been replaced by a worse shape:

**The author submits a review in `COMMENTED` state, then merges their own PR within 13–74 seconds.**

| PR | author | sole reviewer | merger | review → merge |
|---|---|---|---|---|
| #403 | `oahcom` | `oahcom` | `oahcom` | **15 s** |
| #404 | `oahcom` | `oahcom` | `oahcom` | **40 s** |
| #408 | `oahcom` | `oahcom` | `oahcom` | **74 s** |
| #409 | `oahcom` | `oahcom` | `oahcom` | **13 s** |
| #413 | `oahcom` | `oahcom` | `oahcom` | **24 s** |
| #414 | `oahcom` | `oahcom` | `oahcom` | **20 s** (2nd review → merge) |

All six satisfy `author == sole reviewer == merger`.

This is not "insufficient review". It is **review reduced to a filled-in field**. The `reviews >= 1` metric can now be satisfied by a single account in a dozen seconds, while the independence section 5 requires has not increased by one unit.

---

## 2. Why this is not a duplicate of MERGE-AFTER-RULING-003

The two registers describe different failure modes, and the new one is **invisible** under the old measure:

| | MERGE-AFTER-RULING-003 | this register |
|---|---|---|
| Observable feature | `reviews == 0` | `reviews == 1`, but reviewer == author |
| Under a `reviews >= 1` metric | violating (visible) | **conforming (invisible)** |
| Where the defence sits | platform required review (M-3) | platform required review **cannot catch it** — it counts people, not whether the identities are the same |

Key point: `MERGE-AFTER-RULING-003` section 11.1 already established that M-3 is unimplementable on the current plan (branch protection API returns 403). **But even if M-3 shipped tomorrow, the six instances recorded here would still pass** — a `COMMENTED` review is not an approval at all, so it never enters M-3's jurisdiction.

In other words: fixing M-3 does not fix this register.

---

## 3. Causal chain: this is the mechanical consequence of the Owner's own ruling

The instance count in `MERGE-AFTER-RULING-003` was frozen at 4 on the strength of the incidental ruling inside the #403 review (review id `6002557767`, 2026-11-21T03:26:13Z):

> ### Incidental ruling: a register must not self-propagate
> 1. The "zero-review merge" instance count is **frozen at 4**; no fifth entry.
> 2. From now on, when the Owner performs a merge, leave the standard evidence comment **on the PR being merged itself** (commands, exit codes, verification conclusion); **do not open a separate PR just to record it**.

That ruling is reasonable in itself — it removes the recursion where recording a zero-review merge required another zero-review merge. But it specified a **carrier** ("leave the evidence comment on the PR being merged") without specifying that the comment's identity must differ from the mergee's.

What followed: on every merge since, the Owner left a substantive evidence comment on the merged PR, **submitted through the review API** rather than as an issue comment. `reviews` therefore went from 0 to 1, and the `reviews == 0` violation signature disappeared.

`#414` carries both carriers side by side, which makes the contrast directly visible:

- 5 issue comments (`05:13:40`, `05:14:51`, `05:24:48`, `05:35:09`, `05:48:50`)
- 3 reviews (`04:56:22`, `05:27:21`, `05:41:38`)

Same account, two channels, both containing an "Owner run report". **The times the review channel was chosen are exactly the times `reviews >= 1`.**

This register does not find that this was intentional evasion. The evidence shows only that the ruling changed the carrier, the carrier changed the count, and the count changed the visibility of the violation.

---

## 4. Review quality and review independence are two separate questions

It must be recorded fairly: these six reviews **are not empty shells**. On content they are more thorough than most real reviews.

| PR | What the review actually contains | Did it find a real problem |
|---|---|---|
| #403 | verifies four facts, freezes the count, issues the incidental ruling | yes (the ruling itself) |
| #404 | independent checkout, real run: `roots 9 / exempt 20 / uniq 20 / missing []` | yes |
| #408 | four behaviours measured, including the bypass test "new unpaired normative source → EXIT=2" | yes |
| #409 | reproduces the AC-5 correction, **and publicly retracts its own prior misjudgement** | yes (self-correction) |
| #413 | five behaviours measured, including injected `pull_request + self-hosted` violation detection | yes |
| #414 | **2 of 8 cases came out opposite to the author's stated expectation; ruled "cannot merge"**; re-ran 9 cases after the author fixed it | yes (rejected and forced a change) |

`#414` deserves separate mention: the first review (`04:56:22`) states plainly "2 of 8 cases came out opposite to what you wrote; cannot merge", the PR then gained commit `ddd4150b`, and the second review (`05:27:21`) confirms all nine pass **and corrects its own P2 misjudgement from the first review**. That flow did in fact stop a defect.

So this register's conclusion must be precise: **the problem is not review quality, it is the reviewing subject**. When one session produces the object under review, produces the review verdict, and executes the merge, no amount of rigour satisfies section 5's independence requirement — because nothing structurally prevents it from stamping its own work next time. `#414` shows it will reject itself, but that was a voluntary act, not a structural constraint.

---

## 5. Relation to existing conclusions

- **MERGE-AFTER-RULING-003**: the count stays frozen at 4 per the Owner's ruling; this register **does not change that count**. What it records is that the observable feature the count was built on no longer holds, so "4" is no longer a number that covers the current state.
- **CI-NOT-EXECUTED-005**: at all six merges the checks were `failure` / `NOT_EXECUTED`. The reviews say so honestly (#403: "this is not a CI PASS"). But reviewer and review-ee being the same person strips that statement of any external force.
- **GATE-DEADLOCK-006**: the baseline `#408` introduced is one half of the deadlock's cause; `#414` fixed the gate's pair-move classification. Both were self-reviewed then merged, and the gate has since returned `EXIT=2` for **every** PR. The three stack: review not independent, gate not executed, gate permanently rejecting.

---

## 6. Facts versus inference

Facts:
- Every `author` / reviewer / `merged_by` / interval in the section 1 table comes from `/pulls/{n}`, `/pulls/{n}/reviews`, `/pulls/{n}/comments`.
- The ruling quoted in section 3 is the verbatim body of review `6002557767`.
- The review summaries in section 4 come from each review body.
- `#414` carries 5 issue comments and 3 reviews simultaneously, with the timestamps given.

Inference (**not made**):
- No finding that the Owner chose the review channel in order to make `reviews` equal 1. The ruling named a place, not a channel.
- No finding that the **content** of these six merges was defective. The `#414` instance shows the opposite.
- No proposal to change the count from 4 to 10. The counting basis itself has lost meaning; swapping the number fixes nothing.

---

## 7. Possible directions (none executed)

| # | Approach | Cost | Note |
|---|---|---|---|
| S-1 | State in PR-GOVERNANCE-001 section 5 that a review where `reviewer == author` **does not count** toward section 5 | one paragraph | cheapest, but still a self-discipline clause with no platform enforcement |
| S-2 | Introduce a second account able to submit reviews (a person or an independent session), requiring section 5 reviews to come from a non-author identity | needs a second identity | **approved in principle by the Owner**; the only structural option while M-3 is unavailable |
| S-3 | Change the section 5 test from "does a review exist" to "does a review exist whose author is not the PR author and whose commit_id == head" | one script | automatable, can be wired into the gate |

None of the three is executed by this register. S-1/S-3 are normative and script changes that, by section 5's own requirement, need independent review; S-2 is an Owner-level decision.

### 7.1 S-2's status

In the ruling of 2026-11-21 the Owner approved S-2 in principle and set five minimum requirements:

1. the PR author and the independent reviewer are different identities;
2. the reviewer is not the PR's sole author identity;
3. the merger may not substitute their own review for independent review;
4. the reviewer must leave a traceable, substantive review conclusion;
5. `COMMENTED`, `APPROVED` and similar states cannot by themselves establish independence — the identity relationship must be checked too.

**But no second identity is appointed this round.** Sponsor and accountable_owner are still `NOT_ASSIGNED`; a GitHub account cannot be designated out of thin air, and the existence of another account cannot be presumed to carry authority, accountability and sustained participation.

So S-2's actual state is:

```
APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED / NOT_YET_OPERATIONAL
```

Until a second identity is formally designated and its accountability boundary established, **it must not be claimed that structural independent review exists**. The S-1/S-3 self-discipline clauses remain in force, but must not be described as a platform-enforced defence.

---

## 8. How to recompute

```bash
TOK=...; R=oahcom/AiMemoryBrainArchitecture
for n in 403 404 408 409 413 414; do
  curl -s -H "Authorization: Bearer $TOK" https://api.github.com/repos/$R/pulls/$n \
    | jq -r '"\(.number) author=\(.user.login) merger=\(.merged_by.login) merged=\(.merged_at)"'
  curl -s -H "Authorization: Bearer $TOK" https://api.github.com/repos/$R/pulls/$n/reviews \
    | jq -r '.[] | "  review by \(.user.login) state=\(.state) at \(.submitted_at) commit=\(.commit_id[0:8])"'
done
```

Test: if `author == merger` and the only `user.login` among reviews is also `author`, section 5 independence does not hold.

---

**Register conclusion**: the failure mode recorded in `MERGE-AFTER-RULING-003` (zero review) has been replaced by a shape that conforms on the count and is equivalent on independence. Six measured instances all satisfy `author == sole reviewer == merger`, at intervals of 13–74 seconds. Review quality is high — `#414` even rejected itself — and that is precisely the point: the defence rests on voluntary restraint, not on structure. This register changes no existing count; it records that the feature that count depends on has lapsed.

**Owner ruling (2026-11-21)**: this register is accepted as a new failure mode, retained alongside 003, without rewriting 003's historical definition. Three prohibitions are stated: `reviews >= 1` must not be treated as sufficient for independent review; `COMMENTED` must not be treated as approval; M-3 is not a fix for this problem. S-2 is approved in principle, status `IDENTITY_NOT_ASSIGNED`.

The Owner also requires that two judgements be kept and neither used to cancel the other: **review content quality: high**; **independence of the reviewing subject: not established**.
