# Governance Convergence Definition and Execution Boundary

**Carrier**: `GOV-NC-CONVERGENCE-2026-11-20`
**Status**: `ACTIVE` — the behavioural constraints apply immediately; the platform-capability item awaits an Owner decision
**Source**: Owner ruling P5 (coordination session `6b00735c`, after the 2026-11-20 re-check)
**Related registers**: `DIRECT-MAIN-001`, `SELF-AUTH-002`, `MERGE-AFTER-RULING-003`, `AC-UNMET-CLOSURE-004`

---

## 1. Why this document exists

The previous approach assumed the gates could stop violations, then recorded the gates being violated.

That assumption has been refuted by three measurements:

| PR | reviews | check state at merge | open to merge |
|---|---:|---|---:|
| #390 | 0 | 2 × `NOT_EXECUTED` | 36m41s |
| #394 | 0 | 1 × `NOT_EXECUTED` | **14s** |
| #395 | 0 | 1 × `NOT_EXECUTED` | 9m49s |

Platform enforcement is unavailable (`branches/main/protection` → 403 while the token holds `admin: true`). So "a PR exists", "the check shows failure" and "it was merged" can no longer be treated as governance safety signals.

This document changes the governance objective from "assume the gates stop violations" to "record explicitly, constrain authorisation, verify results, and escalate the platform-capability gap to the Owner".

**This does not mean accepting merge-without-review as the normal flow.**

---

## 2. Three levels

### Level one: record completeness (executable now)

Criteria met:

- Every observed direct push, un-reviewed merge, unexecuted check and unauthorised exemption has its own register.
- Each register carries: time, commit SHA, PR number, attribution status of the actor, check result, disposition status.
- `NOT_EXECUTED` is counted as neither PASS nor substantive FAIL.
- The platform permitting a merge is not equated with governance compliance.
- Unverified root causes are not written as facts.

Current coverage:

| Failure class | Register | Scale |
|---|---|---|
| Changes reach `main` without a PR | `DIRECT-MAIN-001` | 53 commits |
| Adjudicating authority issued by the adjudicated party | `SELF-AUTH-002` | 1 instrument, 7 closures |
| PR exists but merges before its gates are satisfied | `MERGE-AFTER-RULING-003` | 3 PRs |
| Issue closed with its own ACs unmet | `AC-UNMET-CLOSURE-004` | 1 Issue, 4/10 ACs unmet |

### Level two: platform capability decision (awaits Owner)

The Owner must decide whether to:

1. Upgrade the repository's plan to obtain the applicable branch-protection capability;
2. Make the repository public to satisfy the corresponding feature condition;
3. Accept that the platform cannot enforce protection, and formally define the risk-acceptance boundary.

**Until that decision is made:**

- M-3 may not be claimed as resolved.
- M-3 may not be written as a plain "pending task".
- Its correct status is `PLATFORM_UNAVAILABLE`.

The single carrier for this item is Issue #283 (`PLATFORM-RESIDUAL — required-check enforcement and branch controls`). #396 has been folded into it.

### Level three: behavioural constraints (effective immediately, not a substitute for technical protection)

These are **this session's self-constraints**. They do not describe anyone else's capability and do not constitute a technical gate:

| # | Constraint |
|---|---|
| B-1 | A successfully created PR must not be treated as merge permission |
| B-2 | A PR without completed independent review and exact-Head checks must not be merged by this session |
| B-3 | An Owner instruction to stay OPEN retains governance force |
| B-4 | An unauthorised merge must be registered as non-compliance, never retroactively certified |
| B-5 | "The platform cannot prevent it" must not be rewritten as "governance permits it" |

---

## 3. Exact scope of the hold

While platform enforcement is unavailable, for governance changes that require a merge to `main`:

**Permitted:**

- Prepare files, tests and evidence.
- Create PRs.
- Run local verification.
- Run remote read-only verification.

**Not permitted:**

- This session merging a PR itself.
- Treating un-reviewed merges as a normal delivery path.
- Treating "merged" as "accepted".

**If another account with permission merges anyway:**

- Record the actual facts.
- Do not retroactively certify compliance.
- Do not change the register's `OPEN` status as a result.

This is not a claim to be able to stop other administrators. It defines this session's own authorisation boundary.

---

## 4. Consistency with existing rulings

| Ruling | Source | Correspondence here |
|---|---|---|
| No self-appointment of acceptance_authority / sponsor / accountable_owner | task book + coordination session | §2 level three B-2; `SELF-AUTH-002` §6 |
| Do not bypass branch protection | task book | §2 level two; not executable, therefore recorded as `PLATFORM_UNAVAILABLE` |
| Do not merge on one's own authority | task book + P6 | §3 not-permitted list |
| Do not treat unrun CI as tests passing | task book + P7 | §2 level one, third bullet |
| Do not describe a session's self-review as independent review | task book | all of `SELF-AUTH-002` |

This document creates no new authority, appoints nobody, and clears no `NOT_ASSIGNED` status.

---

## 5. What counts as converged

**Converged today:** level one. Every known failure has a retrievable register, and the registers are reproducible by a third party.

**Not converged today:** level two. It requires an Owner decision.

**Level three is not a convergence condition; it is a behavioural boundary.** It constrains this session, not others.

So the honest statement of governance state is:

> `RECORDED_NOT_PREVENTED`

That statement may not be upgraded to `REMEDIATED` until either:

1. The platform-capability decision is made and implemented; or
2. All participants keep complying without technical enforcement, over an observation window long enough to mean something.

**A complete record is not the disappearance of risk; an unenforceable platform is not permission to keep merging as before.**

---

## 6. Explicitly not done

- No Sponsor / accountable_owner / acceptance_authority appointed.
- No `NOT_ASSIGNED` cleared.
- No R2 released for AID-2026-023/024/026.
- No Issue reopened other than #384 (whose reopening rests on separate ruling P1).
- No commit reverted.
- No modification of `PR-GOVERNANCE-001`.
- No claim that this document has technical force.

---

## 7. Related

- `GOV-NC-2026-11-20-DIRECT-MAIN-001` §8 C-3, §13
- `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §8 M-3, §11.1
- Issue #283 (single carrier for the platform capability)
- Issue #352 (CI quota exhaustion)
- `14-ai-development/PR-GOVERNANCE-001.md` §3 / §4 / §5
