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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Both admissions were run, not read. The rejection of AID-2026-055/manifest.yaml was produced by scripts/ci/check_repository_hygiene.py --base HEAD~1 --head HEAD on a branch containing exactly that file, and it is also the CI annotation on PR #889 check run 138238290710. The admission of .md came from the same script's ALLOWED_DOCUMENT_SUFFIXES read at main 215f87b5, and from the fact that the three .md files in this change passed the same gate. The dating of cfcafc98a and a3c6280aa came from git log --diff-filter=A."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032.md"
---

# GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 215f87b5`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. Conclusion first

Since `cfcafc98a` (#844, 2026-11-24, `ci(hygiene): admit new files through an explicit whitelist`), **no new AID work order can be registered**.

The reason is that the admission whitelist allows `.md` and source suffixes, while `.yaml` is allowed only under `.github/workflows/` and `.github/actions/` — and every AID lives in `14-ai-development/work-items/AID-…/manifest.yaml`, which no rule covers.

Measured (by running the gate, not by reading it):

```
$ python scripts/ci/check_repository_hygiene.py --base HEAD~1 --head HEAD
::error::new-file admission violation: no allowlist rule for
        '14-ai-development/work-items/AID-2026-055/manifest.yaml'
```

This is not a corner case. It is **the dispatch channel itself, closed**. The repository now has 30 unmeasured registers, several marked `OPEN` / `NOT_ASSIGNED`, and the only mechanism that turns any of them into work — an AID work order — can no longer be created.

This register records that closure and explains why this session does not open it.

---

## 2. The timeline is hard

| Event | Commit | Date |
|---|---|---|
| `AID-2026-054`'s `manifest.yaml` merged | `a3c6280aa` (#823) | 2026-11-23 |
| Admission whitelist introduced | `cfcafc98a` (#844) | **2026-11-24** |
| This session attempts to register `AID-2026-055` | branch `gov/aid-2026-055` | 2026-11-24 |

The whitelist arrived one day after the last work order. So `054`'s carrier predates the rule; it is not evidence that the rule intends to admit it — it simply never came before the rule.

**This is a timing fact, not an inference**: `git log --diff-filter=A` gives the commit that introduced 054's manifest; `git log` gives the commit that introduced the whitelist script; the date relation is as above.

---

## 3. What the whitelist actually says

`is_allowed_new_path()` in `scripts/ci/check_repository_hygiene.py` admits five classes:

| Rule | Content | Covers `manifest.yaml` |
|---|---|---|
| `ALLOWED_DOCUMENT_SUFFIXES` | `.md` `.rst` `.adoc` | no |
| `ALLOWED_SOURCE_SUFFIXES` | `.py` `.sh` `.rs` `.ts` … | no |
| `ALLOWED_CONFIG_PATHS` | **exact filenames** such as `.gitignore`, `Cargo.toml`, `package.json` | no |
| root `requirements*.txt` | — | no |
| `.yml`/`.yaml` under `.github/workflows/` or `.github/actions/` | — | no |

Anything outside those five is rejected. `manifest.yaml` is in none of them.

By contrast, `scripts/check_bilingual_docs.py` puts all of `14-ai-development/work-items/` into `PAIR_EXEMPT_PREFIXES` on the grounds that these are "operational records or prompt templates, not bilingual specifications" — the same directory is formal operational record to one gate and unadmitted file type to the other.

---

## 4. Why this session does not change that line itself

The change needed is one line: let `.yaml` under `14-ai-development/work-items/` through admission. It lives in `is_allowed_new_path()`, which is gate source.

This session has consistently refused to modify gate source — `AID-2026-054`'s prompt lists `check_bilingual_docs.py` as read-only, and this session has not broken that. To make an exception here, the reason for the exception could only be "I need it":

> The only party that wants this door open is the only party with an incentive to open it wider than needed.

That is structurally the same as `SELF-REVIEW-007` and `SELF-AUTH-002`, moved to a different location. The repository currently has **one writable identity** and **zero independent reviews** (README records 675 PRs / 0 APPROVED), so "the party who needs it widens it" is precisely the check that is missing. **This session does not sign that widening, in its owner-proxy capacity.**

Its disposition is therefore: record, do not implement; keep the work order's content in §6, ready to register within a minute of the widening landing.

---

## 5. This is not a defect I am inventing; it is where two existing records cross

- The admission whitelist was introduced deliberately by `#844`, whose own message says "explicit whitelist", so its exclusivity is intent, not oversight.
- The work-order carrier is `manifest.yaml`, the shape in use since `AID-2026-001`; every row of `INDEX.md` links to a `manifest.yaml`.

Each is reasonable alone. What nobody tested is the crossing: **when the whitelist landed, nobody tested whether the existing work-order shape could be created again.** That is the same shape as register 030 — the repair is correct, and the repair's side effect is untested.

---

## 6. The work order awaiting registration (usable once the widening lands)

Preserved here so the measurement does not vanish with an unmerged branch.

**Object:** `scripts/governance/evidence/test_gate_normative_roots.py` + `.github/workflows/repository-hygiene.yml`

**Basis:** at `main @ ef7266db`, `Ran 52 tests / FAILED (failures=3, errors=21)` and `grep -rn 'test_gate_normative_roots' .github/` returns nothing. The cause is in `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030` §4: `load_gate()` sets only `mod.ROOT`, while `changed_status()` uses `cwd=REPO_ROOT`, so a test that builds a throwaway repository runs `git diff` in the real one and exits 128.

**Acceptance criteria (each independently checkable)**

1. 52 tests stay 52, 0 failures, 0 errors; nothing deleted, skipped, or marked `expectedFailure`.
2. After the change, no test in the file can reach the real repository — passing must not depend on the real repository happening to be clean.
3. A per-problem attribution table: test name, exception text, whether the helper fix resolved it.
4. Mutation test A: delete `and not partial_side_by_side`; at least one test must go red; paste the output.
5. Mutation test B: revert `cwd=REPO_ROOT` to `cwd=ROOT`; the suite must go red. If it does not, the helper fix has made the suite indifferent to the change it exists to detect, and that must be written down rather than worked around.
6. Add one line to the existing `for f in \` list in `repository-hygiene.yml`, in alphabetical position.
7. `scripts/check_bilingual_docs.py` is read-only; `register_closure: NOT_GRANTED`.

**Why these criteria matter:** this suite exists to catch one regression, and it was silently disarmed. Making it green without proving it can go red repeats that failure with better numbers.

---

## 7. What this register does not claim

- That the whitelist is wrong. Admitting arbitrary `.yaml` would let snapshots and data files flood in; `#844`'s reasoning holds.
- That `#844` should be reverted. What is needed is a **prefix-bounded** rule, not the absence of rules.
- That this session has the authority to implement it — or that the next reader does not. The issuing authority is the Owner's, not this session's.
- That any of the 30 unmeasured registers turns red or green because of this. Their status is unchanged by this register.
- An independent reviewer. That seat is `NOT_ASSIGNED`, and this register cannot fill it.

**Blocking chain:** independent review `NOT_ASSIGNED`, widening authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 8. Reproduction

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  215f87b5

# 1. the whitelist rejects the work-order carrier (on a branch containing manifest.yaml)
python scripts/ci/check_repository_hygiene.py --base HEAD~1 --head HEAD
-> ::error::new-file admission violation: no allowlist rule for
   '14-ai-development/work-items/AID-2026-055/manifest.yaml'

# 2. the whitelist admits .md
#    on the same branch, with only .md changes, the same command prints
-> Repository new-file admission passed: N new path(s) checked.

# 3. the timing
git log --diff-filter=A --format='%h %ad %s' --date=short \
  -- 14-ai-development/work-items/AID-2026-054/manifest.yaml     # -> a3c6280aa  2026-11-23
git log --format='%h %ad %s' --date=short -2 \
  -- scripts/ci/check_repository_hygiene.py                      # -> cfcafc98a  2026-11-24

# 4. the measurement behind the closed work order
python -m unittest scripts.governance.evidence.test_gate_normative_roots
-> Ran 52 tests in 72.708s / FAILED (failures=3, errors=21)
grep -rn 'test_gate_normative_roots' .github/
-> (no output)
```
