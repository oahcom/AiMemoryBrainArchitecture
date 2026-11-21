# GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008

- Register ID: GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008
- Status: `OPEN` / `ACTIVE` / the gate's own implementation was merged with zero review
- Found at: 2026-11-21T07:10Z (data pulled 2026-11-21T07:20Z)
- Subject: repository `oahcom/AiMemoryBrainArchitecture`, PR #423 / Issue #420
- Prior registers: 005 (CI never executed), 006 (gate deadlock), 007 (self-reviewed merges)

## 1. Bottom line

PR #423 changed the bilingual gate's own implementation (`scripts/check_bilingual_docs.py` **+110 −3**, plus +40 in tests) and fixed a real defect (Issue #420: an exemption could be self-registered in the same commit that introduced the file).

It was merged, and:

- `reviews = 0` — **no review at all**, not even a self-review;
- all three check runs have `conclusion = failure` and `steps = 0` — the jobs never started;
- author = merger = `oahcom`;
- created 06:53:12Z → merged 06:59:08Z, a span of **5m56s**.

This is the **reverse** of the shape register 007 records. 007 records "`reviews=1` on the count, independence zero". #423 does not even have the form.

## 2. Facts

### 2.1 PR metadata

| Item | Value |
|---|---|
| PR | #423 `fix(governance): require independent bilingual exemption registration` |
| created | 2026-11-21T06:53:12Z |
| merged | 2026-11-21T06:59:08Z |
| span | 5m56s |
| author | `oahcom` |
| merger | `oahcom` |
| reviews | **0** |
| commits | 1 (`6d6c6ba57a`) |
| files | 2, `+150 −3` |
| merge commit | `360d88c99a47018ce78b870379be3ee43841a837` |
| head branch | `fix/issue-420-exemption-self-registration` |

### 2.2 What changed

```
6d6c6ba57a  scripts/check_bilingual_docs.py                        +110  -3
6d6c6ba57a  scripts/governance/evidence/test_gate_normative_roots.py +40  -0
```

It adds `check_embedded_registration_history()`, requiring every entry in `EMBEDDED_BILINGUAL_SOURCES` to be registered in a commit **later** than the one that created the file. Same-commit registrations are allowed only for three `SELF_REGISTERED_AT_CREATION` entries, pinned to their measured SHAs.

This is a **genuinely effective fix**. Issue #420's reproduction was: create `00-governance/new-spec.md` and, in the same commit, insert a self-invented reason into the exemption table — gate returns `EXIT=0`. After the fix that path is closed.

### 2.3 Commit identity

```
author    {'name': 'Ubuntu', 'email': 'ubuntu@localhost.localdomain', 'date': '2026-11-21T06:51:14Z'}
committer {'name': 'Ubuntu', 'email': 'ubuntu@localhost.localdomain', 'date': '2026-11-21T06:52:00Z'}
```

That is the **fifth** commit identity in this series. The first four: `oahcom`, `unknown <1491856051>`, `governance@localhost`, `oahcom <noreply@github.com>` (web commit).

### 2.4 Check runs

| name | status | conclusion | steps |
|---|---|---|---|
| GOV-DOC-001 structural checks | completed | **failure** | **0** |
| GOV-DOC-002 metadata checks | completed | **failure** | **0** |
| audit | completed | **failure** | **0** |

All three annotations read:

```
The job was not started because recent account payments have failed or your
spending limit needs to be increased. Please check the 'Billing & plans' settings
```

That is the `NOT_EXECUTED` shape register 005 records: `conclusion: failure` does not mean the tests failed, only that the job never started.

## 3. Why this is worse than 007

007 records reviews that are compliant on the count and empty on independence. It at least shows the executor knew a review requirement existed and was willing to go through the motion.

#423 does not go through the motion at all:

| Item | #418 (recorded in 007) | #423 (this register) |
|---|---|---|
| reviews | 1 (`COMMENTED`, the author) | **0** |
| review → merge | 12 seconds | no review to time |
| created → merge | — | 5m56s |
| what changed | exemption table, +5 lines | **gate implementation, +110 −3** |
| check state | not pulled | all three `steps=0` |

The fourth row is the important difference: **#418 changed data (an exemption list); #423 changed the criterion (the gate implementation).** The first decides whether one file may pass. The second decides the rule by which every PR is judged.

A zero-review PR changed the definition of compliance, and the first thing that definition judges afterwards is every PR that follows it.

## 4. The chain it closes

006 records the gate being unsatisfiable on main; #418 lifted it via F-1; #420 pointed out that F-1's path can be abused by self-registration; #423 closed the self-registration.

Four steps, each either a direct push or a zero/self-reviewed merge:

```
ae37a419  direct push, unpaired normative doc      → 006
#418      self-review, 12s, +5 exemption lines    → 006 §12
#420      records the self-registration defect    → this register §2.2
#423      zero review, 5m56s, +110 −3 gate change → this register
```

Each step has a defensible reason on its own: direct push to move fast, F-1 because the template is machine-consumed, the fix because the defect is real. **But no step had independent review, and in series they rewrote the judging rule.**

## 5. A question that has to be asked

`check_embedded_registration_history()` depends on `git log --diff-filter=A` and `git log -S`, i.e. full git history. And register 005's state is: **CI has never executed this script**.

So the new criterion was never verified by any automation at merge time. Its test, `test_gate_normative_roots.py` (+40 lines), was not executed either.

This is not inference. `steps=0` on all three check runs is the evidence.

## 6. Measured: how the new criterion behaves on real history

Running the upgraded gate on a real full clone (770 commits) against the existing 21 exemptions:

```
::error::Unable to verify embedded bilingual registration history for
  00-governance/architecture-document-management-policy.md:
  Command '['git', 'log', '--format=%H', '-S', '"...policy.md"', 'HEAD', '--',
  'scripts/check_bilingual_docs.py']' returned non-zero exit status 128.
```

All 21 report the same class of error.

**Attribution, which must be stated**: that run used a `--filter=blob:none` partial clone; `git log -S` needs historical blobs, the promisor fetch failed (network), hence `exit 128`. **That is a defect in my environment, not in #423.** It cannot be used to claim the criterion fails on a normal clone.

But one observation does follow and must be recorded: **the new criterion changes the gate from "reads the working tree" to "depends on full history and a working network".** `current_bilingual_gaps()` only did `rglob` over the working tree; it now also does 21 `git log -S` calls. In CI that is fine (`fetch-depth: 0`). Offline or in a shallow clone it fails wholesale.

## 7. Inferences not made

- It does **not** rule that #423's author "deliberately" skipped review. The evidence shows `reviews=0`, checks `steps=0`, merged in 5m56s.
- It does **not** rule that #423's change is wrong. §2.2 treats it as a real fix, and Issue #420's reproduction is on record.
- It does **not** rule that the new criterion fails on a normal clone. §6 attributes the failure to my clone.
- It does **not** read this as "#420 should not have been fixed". It should have been. The question is how it landed.

## 8. Relation to the other registers

| Register | Relation |
|---|---|
| 005 | this register's three `steps=0` runs are another instance of 005's finding, still occurring after 005's window |
| 006 | #423 is the fourth step in 006's chain; it closes the hole in the fix path #418 used |
| 007 | this register records a regression from 007's shape: #418 had one review, #423 has none |
| #400 | #400 concluded "the exemption table is an unaudited expansion surface"; #423 is one implementation of that conclusion |

## 9. Reproduction

```bash
# 1) PR metadata
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/423 \
  | jq '{created_at, merged_at, merged, merged_by: .merged_by.login, additions, deletions, changed_files}'

# 2) review count
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/423/reviews | jq 'length'
# -> 0

# 3) check runs: three failures, all steps empty
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/6d6c6ba57a/check-runs \
  | jq '.check_runs[] | {name, conclusion, steps: (.steps | length)}'

# 4) changed lines
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/6d6c6ba57a \
  | jq '.files[] | {filename, additions, deletions}'
```

**Register status**: `OPEN` / `ACTIVE` / the gate implementation merged with `reviews=0` / three checks `steps=0` / the fix itself is effective / the process did not satisfy PR-GOVERNANCE-001 §5
