---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      last_verified_date: "2026-11-25"
      last_verification_note: "This record states the state the first review actually examined, and not the state after the rewrite it produced. The rewrite is the author's own and is not covered by this verdict. Round 1 is the only round this work item has had."
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

# AID-2026-060 — Independent review, round 1

## 1. Commit and files examined

- Repository: `C:/Users/Administrator/AppData/Local/Temp/opencode/amb2`
- Fetched with `git fetch origin --prune`; reviewed against `origin/main` = `ebadbe84`
  (`feat(governance): recover the AI session evidence gate, fail-closed and PR-scoped (#965)`).
- Files read from `origin/main` (the working tree is on `req05/056-058-consistency`, 23 behind, and does not contain the work item):
  - `14-ai-development/work-items/AID-2026-060/manifest.yaml`
  - `14-ai-development/work-items/AID-2026-060/prompt-v1.md`
  - `14-ai-development/work-items/INDEX.md` (row 86)
- Read-only code checked: `scripts/ci/gate_ratchet.py`, `.github/workflows/gates.yml`,
  `scripts/check_bilingual_docs_full.py` (the wrapped command), `scripts/check_traceability.py`,
  `14-ai-development/work-items/AID-2026-058/manifest.yaml`, `AID-2026-056/REVIEW-01-INDEPENDENT.md`.
- Nothing in the repository was modified. Scratch work and this report live under
  `C:/Users/Administrator/AppData/Local/Temp/opencode/scratch-untracked/`.

---

## 2. Verdict

**`REQUEST-CHANGES`.**

The defect reproduces exactly as described, and the manifest's `findings[F1]` is correct that the
hole is wider than the empty baseline. But the work item as written orders two behaviours that
cannot both hold on the repository it ships into, and its acceptance criteria are satisfiable by an
implementation that fixes nothing that `F1` says must be fixed. It is not dispatchable.

---

## 3. Blocking findings

### B1 — Deliverable 2 contradicts AC7 and turns the only live CI check permanently red

The manifest requires, twice:

> `deliverables[1]`: "gate_ratchet.py fails when the command it runs exits non-zero, **regardless of
> the baseline's content**."
> prompt §4.2: "A non-zero exit from the command fails the ratchet, **independently of the
> baseline's content**."

The only caller in the repository wraps a command that **exits 1 by design**. `gates.yml:155-162`
runs the `bilingual` job as:

```
python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/bilingual-docs.txt \
  --format paths \
  --command "python3 scripts/check_bilingual_docs_full.py"
```

Measured:

```
$ python3 scripts/check_bilingual_docs_full.py; echo "EXIT=$?"
GOV-DOC-001 full scan: 661 in-scope Markdown files; 210 exempt; 77 violations.
...
GOV-DOC-001 full scan: FAIL
EXIT=1
```

```
$ python3 scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
    --format paths --command "python3 scripts/check_bilingual_docs_full.py"
ratchet: baseline=77 current=77 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT=0
```

The ratchet's entire purpose is to sit on top of a gate that is **currently red**; a red gate exits
non-zero. Under deliverable 2 read literally, this invocation must fail, and the `bilingual` job —
which the work item's own prompt §2 calls "the required check `Bilingual docs coverage (ratchet)`" —
goes red on every run and stays red.

AC7 asserts the opposite in the same document: "Both existing callers still pass". The two cannot
both hold. The manifest is therefore not a spec; it is two specs, and the implementer must guess.
An implementer who obeys §4.2 literally breaks AC7; an implementer who obeys AC7 must silently
weaken §4.2 to "non-zero exit **and** an empty current set", which the manifest never says.

AC7 also already carries the answer it demands and does not act on it:

> "If a caller currently relies on the pass-through behaviour this work item removes, that caller is
> named in the manifest rather than silently adjusted."

The caller does rely on it (measured above). It is not named.

The satisfiable reading exists — fail when the exit code is non-zero *and* the parsed current set is
empty — but it survives in no sentence of this manifest. **The manifest must state which rule is
intended and name `bilingual-docs.txt` / `check_bilingual_docs_full.py` as the caller whose exit 1
must continue to be ratcheted rather than failed.**

---

### B2 — AC1 breaks AID-2026-058 on the day 058 lands, and AC7 promises it will not

`manifest.yaml` AC1: "Empty baseline, command exits 0: non-zero exit ... The empty case is treated as
a valid zero-item baseline [today]."
`deliverables[0]`: "gate_ratchet.py rejects a baseline file that exists but contains zero entries".

AID-2026-058 (`status: DISPATCHED`, INDEX row 44) requires the exact opposite of the same script on
the same input:

```
$ git show origin/main:14-ai-development/work-items/AID-2026-058/manifest.yaml | grep -n "AC4"
122:  - id: AC4
      text: "The baseline is brought to 0 entries, as a removal-only edit, in the same commit that
             lands the two inputs. ... `baseline_content_change` moves from NOT_GRANTED to
             GRANTED-FOR-SHRINK-ONLY for this criterion ..."
120:  - id: AC3
      text: "`gate_ratchet.py --baseline scripts/ci/baselines/traceability.txt --format paths
             --command 'python scripts/check_traceability.py'` exits 0 with regressions=0 ..."
```

058 empties `scripts/ci/baselines/traceability.txt` (it does not exist on `origin/main` yet:
`git cat-file -e origin/main:scripts/ci/baselines/traceability.txt` → `fatal: path ... does not
exist`, exit 128) and requires `gate_ratchet.py` over it to exit 0. 060 requires an empty baseline to
be rejected with a non-zero exit. After 060 lands, 058's AC3 is unsatisfiable — 058 is already
DISPATCHED and cannot be implemented.

060's AC7 states the false premise explicitly: "Both existing callers still pass: the bilingual-docs
ratchet (77 entries) and, **once AID-2026-058 lands, the traceability ratchet**". It will not pass,
because 058's own AC4 removes every entry from that baseline. 060's AC7 therefore asserts an outcome
that 060's AC1 forbids.

Note the ordering makes this certain, not hypothetical: OD-26 as quoted in the manifest requires 060
to land **before** 058's baseline generation is treated as trustworthy. So 060 lands first, and 058
lands into a ratchet that refuses its payload.

**One of the two work items must change, and 060 must say which.** Either 060's empty-baseline
rejection needs a named exemption route (an explicit "this baseline is intentionally empty" marker),
or 058's AC3/AC4 must be re-cut. A reviewer cannot resolve that on the implementer's behalf, and
060's manifest does not mention that a conflict exists.

---

### B3 — No machine-readable file authorisation: the same defect 056's round 1 raised as B5

`manifest.yaml` has no `authorization`, no `scope`, no `files_to_modify`, no `files_not_to_touch`,
and no `implementation_write` field. Verified by parsing with PyYAML:

```
$ py dupcheck.py m060.yaml
parsed_ok=True
duplicates: none
top_level_keys: ['work_item_id', 'title', 'class', 'risk', 'risk_rationale', 'security_scope',
 'status', 'sponsor', 'accountable_owner', 'implementing_ai_session', 'repository', 'base_branch',
 'base_commit_sha', 'tracking_issue', 'created_at', 'updated_at', 'prompt_id', 'prompt_version',
 'prompt_file', 'prompt_status', 'prompt_sha256', 'prompt_bytes', 'prompt_provenance_tier',
 'prompt_provenance_note', 'owner_decisions', 'deliverables', 'acceptance_criteria',
 'independent_reviewer', 'integration_reviewer', 'review', 'acceptance', 'implementation',
 'errata', 'findings']
  'authorization' present: False
  'scope' present: False
  'implementation_write' present: False
  'files_to_modify' present: False
  'files_not_to_touch' present: False
```

The write boundary exists only in prose — prompt §6 ("In scope: `scripts/ci/gate_ratchet.py`, its
test module, and the comment inside it") and `security_scope: "None..."`. Prose is not an
authorisation. This is verbatim the finding `AID-2026-056/REVIEW-01-INDEPENDENT.md` §2 B5 recorded
against 056, and AID-2026-058 fixed it:

```
$ git show origin/main:14-ai-development/work-items/AID-2026-058/manifest.yaml | sed -n '88,102p'
authorization:
  implementation_write: "NOT_GRANTED - ..."
  gate_behaviour_change: "DECIDED by OD-23, ..."
  baseline_content_change: "GRANTED-FOR-SHRINK-ONLY - ..."
  ...
scope:
  files_to_create:
    - 00-governance/requirements-registry.yaml
    - scripts/ci/baselines/traceability.txt
  files_to_modify:
    - scripts/check_traceability.py
    - scripts/test_check_traceability.py
```

060 needs the same block, and it needs to say `files_to_modify: scripts/ci/gate_ratchet.py` plus a
named test path — see M4, the test module is never named anywhere in the manifest or prompt.

---

### B4 — No acceptance criterion fails if only the empty baseline is rejected, so the fix F1 demands is unverified

`findings[F1]` states the scope of the required change:

> "A fix that special-cases empty files would leave the general condition in place."

That general condition is real and I reproduced it. Non-empty 77-entry baseline, command emits
exactly the baseline set, command exits 9:

```
$ python3 scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
    --format paths --command "python3 .../emit_then_9.py"
ratchet: baseline=77 current=77 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT=0
```

(where `emit_then_9.py` prints the baseline file and then `sys.exit(9)`.)

No acceptance criterion exercises this case. AC3 comes closest but specifies only "command exits 9",
and the natural reading — a command that exits 9 having printed nothing — already fails today
(see M2). Concretely, an implementer who adds only

```python
if not baseline:
    raise SystemExit(f"gate_ratchet: empty baseline: {args.baseline}")
```

passes AC1, AC2, AC3, AC4 and can write a truthful AC5 mutation table for all four, while
`proc.returncode` remains unread and the case above still prints PASS. The work item would close
with `F1` unaddressed and its second deliverable unenforced.

A criterion of the shape "non-empty baseline, command exits non-zero **and** emits the baseline set:
non-zero exit, no PASS" is required, and AC5's mutation table must name the exit-code guard against
it. Without that, AC5 certifies a guard set that does not include the one `F1` exists for.

---

## 4. Material findings

### M1 — The stated root cause is wrong: the exit code is discarded in every `--format`, not "under `--format paths`"

`manifest.yaml` deliverable 2: "Today that exit code is discarded **under `--format paths`**."
`findings[F1]`: "**Under `--format paths`** the ratchet compares path sets only and discards the
command's exit code."

The exit code is never read at all. `scripts/ci/gate_ratchet.py:94-128`:

```
 94	    proc = subprocess.run(
 95	        args.command,
 ...
101	        errors="replace",
102	    )
103	    # Items are printed to stdout. stderr carries interpreter warnings and
104	    # tracebacks, which are not items; a crash yields zero items and is caught
105	    # below as a stale baseline (fail-closed), never as a pass.
105	    current = normalize(proc.stdout.splitlines(), args.format)
...
120	    if regressions or fixed:
...
127	    print("ratchet: PASS - failure set matches the baseline exactly.")
128	    return 0
```

`proc.returncode` appears nowhere in the file —
`grep -n "returncode\|check_returncode\|proc\." scripts/ci/gate_ratchet.py` returns exactly one line,
`105: current = normalize(proc.stdout.splitlines(), args.format)`. The verdict at 120-128 is computed
from set difference alone. `--format` selects one line of `normalize()` (`61-62`) and has no bearing
on the exit code.

Reproduced with the default format, which is `schema`, not `paths`:

```
$ python3 gate_ratchet.py --baseline empty.txt --command 'python3 -c "import sys;sys.exit(9)"'
ratchet: baseline=0 current=0 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
EXIT=0
```

This matters beyond pedantry: a fix written to the manifest's own diagnosis would guard the
`--format paths` branch, and every AC in the manifest passes with `--format paths`. The default
`schema` path would stay broken with all seven criteria green. (Impact is currently low — the file's
own ponytail note at line 21 says `schema` is uncalled — but the manifest must not encode a wrong
cause.)

### M2 — AC3's "Already true today" is false for the case that matters

AC3: "Non-empty baseline, command exits 9: non-zero exit, no PASS. Already true today (fixed=77 FAIL
exit 1)."

The parenthetical is true only for a command that prints nothing, because all 77 entries then become
"fixed". Measured:

```
$ python3 scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
    --format paths --command 'python3 -c "import sys;sys.exit(9)"'
ratchet: baseline=77 current=0 regressions=0 fixed=77
...
ratchet: FAIL - lower the baseline by 77 fixed item(s).
EXIT=1
```

With output, the same exit code PASSes (`B4` measurement: `baseline=77 current=77 ... PASS EXIT=0`).
So AC3 is not a regression guard, it is a new requirement, and its justification makes it look
already-satisfied. It is also the exact case AC7 says must continue to pass — the same contradiction
as B1, seen from the other side.

### M3 — `base_commit_sha` is 39 commits behind `origin/main`; the measurements still hold

```
$ git rev-list --count b80e5a40..origin/main
39
$ git cat-file -t b80e5a4059e7503136697d89935ce8dddc6c87f9
commit
$ git diff b80e5a40 origin/main -- scripts/ci/gate_ratchet.py
(no output)
$ wc -l scripts/ci/baselines/bilingual-docs.txt
77
```

The subject file is byte-identical between the declared base and `origin/main`, and the 77-entry
figure in AC3 and AC7 still holds at `origin/main`. No action required; recorded so the next round
does not have to re-derive it.

### M4 — The test module is never named

Prompt §6 says "its test module"; the manifest says "Tests cover the four cases in AC1-AC4". No path
appears in either file, and none exists on `origin/main`
(`git ls-tree -r --name-only origin/main | grep -i "ratchet.*test\|test.*ratchet"` is empty).
The repository has a convention for a test sitting next to a `scripts/ci/` subject —
`scripts/ci/test_audit_runner_admission.py`, `scripts/ci/test_check_branch_freshness.py`,
`scripts/ci/test_check_test_reachability.py`. AC5 is unsatisfiable as a check until the path and the
invocation are written down; 056's round-1 B4 was the adjacent defect ("names a module that does not
exist"). Fold the concrete path and command into the `scope` block B3 requires.

### M5 — AC5 and AC6 are self-certifying

AC5 requires the manifest to "name the specific guard whose removal makes that test fail". Nothing
requires anyone to *remove* the guard and observe the failure; an implementer writes a plausible
sentence and AC5 is met. AC6 ("the comment no longer claims a guarantee the code does not provide")
has no mechanical check either. Both are prose criteria graded by prose. AC5 is the criterion the
whole work item leans on for credibility. It should require the reviewer, not the implementer, to
perform at least the four deletions and record the observed failures — or state plainly that AC5 is
reviewed by reading, so that no one mistakes the mutation table for evidence.

### M6 — The INDEX row repeats the overbroad requirement

`INDEX.md:86` records the deliverable as "command exit code must fail the ratchet". It is consistent
with the manifest (status PROPOSED, `GATE/CODE/TEST / R2`, SHA-256
`f9a01079...c5e9`, 7797 bytes all match), so the index defect is the manifest's defect, not a
separate one. It must change when B1 is resolved, or the index will keep asserting the contradiction
after the manifest stops.

---

## 5. Acceptance criteria — falsifiability

| AC | Verdict | Reason |
|---|---|---|
| AC1 | **FAIL-ABLE, and currently failing as claimed** | Reproduced: empty baseline + exit 0 → `baseline=0 current=0 regressions=0 fixed=0 / PASS / EXIT=0`. A guard rejecting `not baseline` fails it. But see B2: this is the criterion that breaks AID-2026-058. |
| AC2 | **FAIL-ABLE, and currently failing as claimed** | Reproduced verbatim: empty baseline + exit 9 → `ratchet: baseline=0 current=0 regressions=0 fixed=0 / ratchet: PASS - failure set matches the baseline exactly. / EXIT=0`. Matches the manifest's claim exactly. |
| AC3 | **FAIL-ABLE but mislabelled** | "Already true today" holds only for a command emitting nothing (`fixed=77 FAIL EXIT=1`). With output the same exit code PASSes (M2), so this is a new requirement, and it collides with AC7 (B1). |
| AC4 | **FAIL-ABLE, currently passing** | Reproduced: `baseline=77 current=77 regressions=0 fixed=0 / PASS / EXIT=0` against a matching set. A guard that rejects everything fails it. Sound as a happy-path floor. |
| AC5 | **NOT falsifiable as written** | "The manifest names the guard whose removal makes the test fail" is satisfied by writing the name (M5). Nothing requires the deletion to be performed or observed. And it certifies only the guards AC1-AC4 pin down — which exclude the exit-code guard `F1` requires (B4). |
| AC6 | **Weakly falsifiable — reviewable prose only** | "No longer claims a guarantee the code does not provide" is a reading judgement, no command decides it. Acceptable if the manifest says so; as written it reads like a check. Current text being false is proven (`gate_ratchet.py:102-104`). |
| AC7 | **UNSATISFIABLE as written** | Requires both callers to keep passing. Caller 1 (bilingual) has a wrapped command exiting 1 today and PASSing; deliverable 2 forbids that. Caller 2 (traceability) will be a 0-entry baseline per AID-2026-058 AC4, which AC1 forbids. Neither half can hold (B1, B2). |

---

## 6. What I could not verify, and why

- **Whether the `bilingual` job is branch-protected as a required check.** The prompt asserts
  "required check"; I read `gates.yml` and the docs but repository branch-protection settings are not
  in the tree. B1 does not depend on it — a red ratchet on every push is enough.
- **AID-2026-059.** `findings[F3]` says it exists as an untracked work item in a concurrent session's
  tree. It is not in `origin/main` and not in this clone, so I cannot check the ID collision it
  describes beyond confirming 060 does not collide on `origin/main`.
- **`prompt_provenance_tier: T1`.** No definition of the tiers in the reviewed files; I did not go
  looking for the policy document.
- **The bilingual job's behaviour on the GitHub runner vs. Windows.** I ran `python3` under Windows;
  the wrapped command and the ratchet are pure-stdlib and shell-agnostic, and `gate_ratchet.py` is
  byte-identical to `origin/main`, but `shell=True` semantics differ between `cmd.exe` and
  `/bin/sh`. All conclusions above were re-derived with `python3 -c` and path arguments only, where
  the two agree.
- **Hash and byte count — verified, no finding.** `prompt-v1.md` at `origin/main` is 7797 bytes,
  SHA-256 `f9a01079c017cfbd1487ea09f3efe148c564d646b24ca55d5226967bb51ec5e9`, exactly as declared.
- **YAML duplicate keys — verified, none.** Parsed with `py` (Python 3.12.3, PyYAML 6.0.3) using a
  loader that reports duplicate mapping keys; `duplicates: none`.

---

## 7. What is right, stated because the negatives matter

- The defect is real and reproduces to the character, including the summary line the manifest quotes
  (`regressions=0 fixed=0`, `EXIT=0`).
- `findings[F1]`'s diagnosis that the hole is wider than the empty baseline is **correct** — I
  reproduced it on the 77-entry baseline (B4). It is the most valuable paragraph in the manifest.
- The prompt is frozen, and its hash and byte count match.
- The manifest parses, has no duplicate keys, and its INDEX row matches it field for field.
- The declared `base_commit_sha` exists, and the measurements taken there still hold at
  `origin/main` (M3).
- `security_scope: "None"` is accurate for this change.
- Naming the caller requirement in AC7 at all ("that caller is named in the manifest rather than
  silently adjusted") is the right instinct; the manifest simply fails to apply it to the caller that
  exists.
