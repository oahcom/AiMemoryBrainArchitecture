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
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure was measured on 2026-11-23 at main f39dfb7b: §2 by replaying main's normative_changes construction over all 552 tracked normative paths; §3 by enumerating extensions over the same set; §4 and §5 by running the suite at 9944d07e and at 8ab40fb4 in a detached worktree; §6 by grepping .github/ for the suite name. No figure is carried over from another register."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-23-UNREACHABLE-GUARD-030.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-23-UNREACHABLE-GUARD-030.md"
---

# GOV-NC-2026-11-23-UNREACHABLE-GUARD-030

**Status:** `OPEN` — `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = f39dfb7b`
**Extends:** `...-SUFFIX-SCOPE-017.md`, `...-CWD-SPLIT-014.md`
**Register author:** owner-proxy session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. Two things: one already fixed, one created by the fix

This register answers what became of `SUFFIX-SCOPE-017`, and records a defect found while checking that answer — one caused by the fix itself.

| | Conclusion |
|---|---|
| 017's defect (a `.json` required to carry bilingual mirrors) | **Fixed** — `717dfbf0`, 2026-11-21 22:09:16 +0800, PR #527 |
| Is the fix the remedy 017 §5 proposed? | **No.** 017 proposed making the suffix filter root-agnostic. What was done instead was to narrow the upstream `normative_changes` to `.md` only. |
| Cost of the fix | `PAIR_ENFORCED_SUFFIXES` becomes **dead code**; all 167 non-`.md` files under the normative roots leave pairing entirely |
| The three tests the fix shipped with | **All broken**, by `8ab40fb4` (register 014's fix) |
| Register 014 §7.3's explanation of that | **Wrong**, see §5 |

---

## 1. 017 was true at its own measurement point, and fixed 80 minutes later

017 was measured at `d647e7d5` (2026-11-21 20:48:30 +0800). The decision chain on `main` was then:

```python
if Path(path).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}:
    normative_changes.append(path)
```

`717dfbf0` (22:09:16 +0800, 80 minutes later) changed it to:

```python
if Path(path).suffix.lower() == ".md":
```

One line, `+1 −1`, with three tests added in the same commit (`+71`). **That commit message does not mention 017**; a repo-wide `grep SUFFIX-SCOPE-017` hits nothing outside this register. This is the same failure mode 014 §7.4 recorded: fixed, but no back-reference.

## 2. The fix is not 017 §5's third branch, and the difference is substantive

017 §5 listed three states that would make its finding a non-issue; the third was "the suffix filter should be root-agnostic". Under that fix, `PAIR_ENFORCED_SUFFIXES` would move somewhere both branches can read it: `.md` stays subject to pairing, `.json` does not.

What was done instead narrowed the whole of `normative_changes` to `.md`. The consequence is that `check_normative_pairing()` can now never receive a non-`.md` file, so the suffix guard at line 1031 can never fire. Measured, by replaying main's construction logic over all 552 tracked normative paths:

```
normative_changes candidates   384
non-.md among them               0
=> times the suffix guard can fire   0
```

`PAIR_ENFORCED_SUFFIXES = {".md"}` is still declared at line 41 and still read at line 1031, but **it is now a tautology**. The code reads as "pairing is required only for Markdown"; what executes is "only Markdown arrives here". Those are different sentences, and the second one is not written down in any comment.

## 3. Cost: 167 files leave pairing, and 0 of them ever had a mirror

| Type | Count | Example |
|---|---|---|
| `.json` | 59 | `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` |
| `.py` | 54 | `08-bmcp-protocol/runtime_reference/*.py` |
| `.yaml` | 47 | `00-governance/architecture-document-metadata.schema.yaml` |
| `.mjs` | 4 | — |
| `.txt` / `.log` / no extension | 4 | — |

Non-`.md` files under `docs/en/` and `docs/zh-CN/`: **0**.

So 017's judgement — that a JSON schema cannot carry a Markdown translation of itself, and demanding one is unsatisfiable — **still holds after the fix**; the fix changed the demand from "unsatisfiable" to "not checked". That is the right outcome: an unsatisfiable requirement is better withdrawn than left standing. **This register does not argue for reverting it.**

It leaves two things unanswered:

1. **`.yaml` and `.json` are data; `.py` is not.** A schema and a validator are not the same question when it comes to "does this need Chinese prose", and they now share one exemption. 017 §7 already declined to claim "JSON schemas need no bilingual treatment"; this narrowing widened the scope of that sentence without recording where it widened to.
2. **`00-governance/architecture-document-metadata.schema.yaml` is the governance metadata schema itself**, and it is one of the 21 `EMBEDDED_BILINGUAL_SOURCES`, so it already had a reason. The other 46 `.yaml` files did not.

## 4. All three tests the fix shipped with are broken, by register 014's fix

The three tests added in `717dfbf0` all run through `_run_real_git_gate_for_change()`: it `git init`s a temp directory, commits, then asserts the gate's verdict. They depend on this helper:

```python
def load_gate(root: Path):
    mod.ROOT = root          # points at the temp repo
    return mod               # REPO_ROOT left alone
```

`8ab40fb4` (2026-11-22 10:37:32 +0800, register 014's fix) changed `changed_status()` from `cwd=ROOT` to `cwd=REPO_ROOT`. So the temp repo the helper builds is never consulted:

```
after load_gate(root=tmp)
  ROOT      = ...\Temp\tmpjv6rdbdy
  REPO_ROOT = <the real repository>   <- what changed_status() reads
```

`git diff A...B` therefore runs in the **real** repository against two SHAs that exist only in the temp one, and exits 128:

```
fatal: Invalid symmetric difference expression edf87e7b...3d443bfb
```

The timeline is hard:

| commit | time | the suite |
|---|---|---|
| `9944d07e` (#534, `sys.argv` patched) | 2026-11-21 23:36 | `Ran 52 tests` / **OK** |
| `8ab40fb4` (register 014's fix) | 2026-11-22 10:37 | `Ran 52 tests` / **FAILED (failures=3, errors=21)** |

Between them, only `8ab40fb4` touched `scripts/check_bilingual_docs.py` or that test file. **52 green tests became 24 problems because of 014's fix.**

## 5. Register 014 §7.3's causal explanation is wrong

014 §7.3 says:

> Those 24 failures are a pre-existing Windows temp-path problem (`run([...], cwd=WindowsPath('C:/Users/ADMINI~1/...'))` assertions that do not match), unrelated to this defect and identical in both states.

**"Identical in both states" is right. "Pre-existing" and "unrelated to this defect" are wrong.**

- Not pre-existing: before `8ab40fb4` the suite was 52 of 52 green.
- Directly related: it is precisely the `cwd=ROOT` → `cwd=REPO_ROOT` step — 014's fix itself — that broke the helper.
- The attribution is incomplete: of the 24, only 1 is a `WindowsPath` assertion; 10 are `current_bilingual_gaps()`'s `git ls-files` exiting 128; 11 are other; 2 are file-creation identity unavailable.

014 §7.3's **main conclusion still holds** — the defect can return with neither suite making a sound, because `scripts/test_check_bilingual_docs.py` (3 tests) is `OK` in both the fixed and broken states. But the explanation under it needs correcting, or a reader will take those 24 for historical noise and conclude the tests were never really green.

## 6. The `GOV-DOC-001 structural checks` job now runs this suite (corrected 2026-11-25)

This section was written on 2026-11-23 against main `f39dfb7b`: `grep -rn 'test_gate_normative_roots' .github/` then really returned nothing, and `.github/workflows/bilingual-docs.yml` ran only `scripts/test_check_bilingual_docs.py`. That observation was overturned the next day:

- `aaf6da96` (#892, 2026-11-24) added `python3 -m unittest scripts.governance.evidence.test_gate_normative_roots` to that same workflow, before the real gate. The job is named `GOV-DOC-001 structural checks`, one of the required contexts.
- The same commit removed §4's double root (`ROOT` / `REPO_ROOT`). Re-measured 2026-11-25: at `8ab40fb4` the suite is still `Ran 52 tests` / `FAILED (failures=3, errors=21)`; at main `a3a62021` it is `Ran 52 tests` / **OK**.

So §4's 24 failures would turn this required context red. They no longer exist: the suite runs on every PR and is green.

## 7. What this register does not claim

- It does not argue for reverting `717dfbf0`. The requirement 017 identified really was unsatisfiable, and withdrawing it was right.
- It does not claim `.py` needs bilingual mirrors. It claims only that sharing one exemption with `.json` was never recorded.
- It does not argue for reverting 014's fix. `cwd=REPO_ROOT` is correct; what is wrong is that the test helper was not changed with it, and how §7.3 attributed the result.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

## 8. Reproduction

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  f39dfb7b

# 1. the suffix guard cannot fire - replay main's normative_changes construction
#    output: 384 candidates, 0 non-.md

# 2. a .json edit now passes
git checkout -B probe origin/main
# change one character in 08-bmcp-protocol/schemas/*.schema.json, commit
BASE_SHA=HEAD~1 HEAD_SHA=HEAD PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
  python scripts/check_bilingual_docs.py
-> PASS (1 changed paths inspected)

# 3. revert the one line from 717dfbf0, same probe
-> FAIL
   ::error::08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
     requires all counterparts changed in this PR: ..., docs/en/..., docs/zh-CN/...

# 4. the suite either side of 8ab40fb4
git checkout 9944d07e && python -m unittest discover -s scripts/governance/evidence \
  -p test_gate_normative_roots.py -q
-> Ran 52 tests / OK
git checkout 8ab40fb4 && (same)
-> Ran 52 tests / FAILED (failures=3, errors=21)

# 5. nothing runs it
grep -rn 'test_gate_normative_roots' .github/
-> (empty)
```
