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
      last_verified_date: "2026-11-25"
      last_verification_note: "Every command and count below was run in this session. The protected set was read from GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main three times on 2026-11-25 (T09:5xZ, T10:10Z, T10:40Z); the last two reads both landed on main = 30c7277e and returned 16 contexts, and the first landed on 95adfd77 and also returned 16. The declared set was read from PR-GOVERNANCE-001 section 7. The token-absent behaviour was observed by running the checker, not inferred."
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

# Session role / use case

IMPLEMENTER. Issue #1029 asked for two things and one of them was already done
before this session started. This record separates them, because reporting
"fixed 12 → 15" would be false twice over: the number was not 15, and it was not
12 by the time I read it.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction
the change was carried out against, pinned at
`78044dfbc68873766fc6773768099a2a7b5b08d67594ca5bf09decbeb991a915`, 3967 bytes.
`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
session read.

The issue's own numbers are **not** the input this session measured. They are
quoted below only to show what was wrong with them.

# Measurement A — the count

## What the issue claimed, and what is actually there

The title says `PR-GOVERNANCE-001.md` §7 declares **12** and the platform requires
**15**. Read twice in this session, on two different `main` commits, because
`main` moved while I was measuring:

```
$ GITHUB_TOKEN=$(cat …/gh_token.txt) python3 -c "
import json,urllib.request,os
r=urllib.request.Request('https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/branches/main',
    headers={'User-Agent':'x','Authorization':'Bearer '+os.environ['GITHUB_TOKEN']})
d=json.load(urllib.request.urlopen(r))
c=d['protection']['required_status_checks']['contexts']
print('main =',d['commit']['sha']); print('len =',len(c)); print(chr(10).join(c))
"

main = 30c7277e1fc1f08f2b11fa1d3cf4ad80793a4184
len = 16
GOV-DOC-001 structural checks
Branch freshness vs base
audit
GOV-DOC-002 metadata checks
BMCP protocol index (hard gate)
BMCP conformance suite (hard gate)
Schema non-empty audit (hard gate)
Bilingual docs coverage (ratchet)
Rust clippy (hard gate)
Repository hygiene (hard gate)
Rust format (hard gate)
Rust doctests (hard gate)
Session Evidence
Session Evidence self-test (base)
Session Evidence self-test (head)
rust-workspace-test
```

**The measured value is 16, not 15.** The command above was run three times on
`2026-11-25`: at `T09:5xZ` against `main = 95adfd77`, and at `T10:10Z` and
`T10:40Z` against `main = 30c7277e`. All three returned 16. The count is not a
stale read of one commit, and it did not move when `main` advanced. The declared block in §7 carries the same sixteen names in the same
order, so `declared - protected` and `protected - declared` are both empty on
`main` today:

```
$ python3 scripts/check_declared_check_contexts.py
::notice::16 declared check contexts, all produced by a job in .github/workflows and all required on main
DECLARED CHECK CONTEXTS: PASS
$ echo $?
0
```

Neither the issue's 12 nor its 15 is the current value. #1033 (`2570ba0c`)
corrected §7 to 16, and `rust-workspace-test` became required between the
issue's two readings — the issue's own addendum comment `7151419335` records the
15 → 16 move inside the same hour. So this work item does **not** perform a
12 → 15 correction; performing one would have written a number the payload
contradicts. What was still broken is the second half, below.

## The protected-side values, read directly

| field | value | endpoint |
|---|---|---|
| `required_status_checks.strict` | `true` | `/protection` |
| `required_status_checks.contexts` | 16 | `/protection` **and** `/branches/main` |
| `enforce_admins.enabled` | `true` | `/protection` |
| `required_pull_request_reviews` | **key absent** (not `null`) | `/protection` |
| `allow_force_pushes.enabled` | `false` | `/protection` |
| `allow_deletions.enabled` | `false` | `/protection` |
| `checks[].app_id` | `15368` for all 16 | `/protection` and `/branches/main` |

`/branches/main` returns the same 16 names in the same order as `/protection`.
That equivalence is what makes the comparison runnable in CI, and it is verified
here rather than assumed:

```
$ python3 - <<'PY'
b = GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main
p = GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection
PY
len 16 16
order equal True
app_ids [15368]
strict True enforce_admins True
rpr present False
```

One limit on that check, stated because the sample is small: the **anonymous**
read was not repeatable from this machine — the unauthenticated rate limit was
already exhausted (`HTTP 403 rate limit exceeded`), so both reads above carried
the token. What the token-absent path does is therefore proved against a local
server rather than against api.github.com; see "The token-absent path" below.

# Measurement B — what the old checker could not see

`scripts/check_declared_check_contexts.py` asserted `declared ⊆ produced`. A
subset test gets *more* true when you delete a line from the left side. Run
against a pristine `git archive` of `origin/main`, mutating the declared block and
restoring it after each case:

```
$ cd <archive of origin/main> && python3 - <<'PY'
import pathlib, subprocess, sys
doc = pathlib.Path("14-ai-development/PR-GOVERNANCE-001.md")
orig = doc.read_text(encoding="utf-8")
for label, old, new in [
    ("drop 'Session Evidence'", "Session Evidence\n", ""),
    ("drop 'rust-workspace-test'", "rust-workspace-test\n", ""),
    ("add a context nothing produces", "rust-workspace-test\n",
     "rust-workspace-test\nContext That Does Not Exist\n"),
]:
    doc.write_text(orig.replace(old, new, 1), encoding="utf-8")
    r = subprocess.run([sys.executable, "scripts/check_declared_check_contexts.py"],
                       capture_output=True, text=True)
    print(f"[{label}] rc={r.returncode} | {r.stderr.strip().splitlines()[-1]}")
doc.write_text(orig, encoding="utf-8")
PY

[drop 'Session Evidence'] rc=0 | DECLARED CHECK CONTEXTS: PASS
[drop 'rust-workspace-test'] rc=0 | DECLARED CHECK CONTEXTS: PASS
[add a context nothing produces] rc=1 | DECLARED CHECK CONTEXTS: FAIL (1 of 17 unproduced)
```

Deleting a required context from the document left every gate green. That is the
defect. The same four cases against the checker in this branch:

```
$ cd C:/tmp/opencode/w1082 && GITHUB_TOKEN=… python3 - <<'PY'  # same loop, same mutations
[pristine] rc=0 | DECLARED CHECK CONTEXTS: PASS
[drop 'Session Evidence'] rc=1 | DECLARED CHECK CONTEXTS: FAIL (declared 15, protected 16; 0 declared-not-protected, 1 protected-not-declared)
[drop 'rust-workspace-test'] rc=1 | DECLARED CHECK CONTEXTS: FAIL (declared 15, protected 16; 0 declared-not-protected, 1 protected-not-declared)
[add a context nothing produces] rc=1 | DECLARED CHECK CONTEXTS: FAIL (1 of 17 unproduced)
restored: True
```

The two deletion cases now fail, and the message says which direction drifted.
The third case still fails — the `produced` half is unchanged and still works.

# The token-absent path — measured, not described

The issue body proposes a fixture fallback "if that makes it impractical in CI",
because the author believed the protection payload needs an admin credential.
Comment `7151816460` corrects that: `/branches/{branch}` carries the contexts
under **Contents (read)**. So the token-absent path is not "skip"; on a public
repository it is a normal successful read, and the checker is written to treat it
that way.

Proved with both token variables unset, against a local server that returns a
payload, so the network is not a variable:

```
$ python3 _w1082_srv.py      # HTTP server on 127.0.0.1, GITHUB_API_URL points at it
--- no token, payload == declared
env token set: False
::notice::16 declared check contexts, all produced by a job in .github/workflows and all required on main
DECLARED CHECK CONTEXTS: PASS
EXIT: 0

--- no token, payload missing Session Evidence
env token set: False
::error::14-ai-development/PR-GOVERNANCE-001.md declares 'Session Evidence', but it is not a required context on main
DECLARED CHECK CONTEXTS: FAIL (declared 16, protected 15; 1 declared-not-protected, 0 protected-not-declared)
EXIT: 1

--- no token, payload has an extra context
env token set: False
::error::main requires 'Undeclared Context', but 14-ai-development/PR-GOVERNANCE-001.md does not declare it
DECLARED CHECK CONTEXTS: FAIL (declared 16, protected 17; 0 declared-not-protected, 1 protected-not-declared)
EXIT: 1
```

Three properties, each shown above:

1. **An absent token does not skip the comparison.** All three runs compare; the
   two that should fail do fail, by name, in the right direction.
2. **Both directions are reported separately.** `declared-not-protected` and
   `protected-not-declared` are different defects with different fixes, so they
   are different messages.
3. **An unreadable platform is INCOMPLETE.** With no token and the real API
   rate-limited, the checker exits **2**, not 0:

```
$ env -u GITHUB_TOKEN -u GH_TOKEN python3 scripts/check_declared_check_contexts.py
::error::INCOMPLETE: the branch-protection payload could not be read, so the declared set cannot be compared to it: HTTPError: HTTP Error 403: rate limit exceeded
$ echo $?
2
```

Exit-code vocabulary is the repository's: 0 PASS, 1 VIOLATION, 2 INCOMPLETE.

# AI-visible output

```
scripts/check_declared_check_contexts.py            + declared == protected, both directions, INCOMPLETE on unreadable
scripts/test_check_declared_check_contexts.py       12 cases, 4 new (2 directions, unreadable, empty payload)
.github/workflows/repository-hygiene.yml            step renamed; GITHUB_TOKEN passed; comment explains the two artifacts
14-ai-development/PR-GOVERNANCE-001.md              §7: the ratification recorded, both languages
14-ai-development/work-items/AID-2026-059/manifest.yaml   required_context_change: GRANTED, NOT_GRANTED preserved
14-ai-development/work-items/AID-2026-061/session-evidence-wo01.md   standing "twelve" marked superseded, not deleted
14-ai-development/work-items/AID-2026-074/          manifest, prompt, this record
14-ai-development/work-items/INDEX.md               one row
```

Self-check, run from `scripts/`:

```
$ python3 -m unittest test_check_declared_check_contexts
............
----------------------------------------------------------------------
Ran 12 tests in 0.044s

OK
```

# Limitations

1. **`strict`, `enforce_admins`, `allow_force_pushes`, `allow_deletions` are still
   a dated measurement.** `/branches/{branch}` does not return them; only
   `/protection` does, and that needs Administration (read) which
   `GITHUB_TOKEN` cannot hold. They have not moved in the window this issue
   covers, but nothing live holds them. Issue #134 keeps the wider question.
2. **`(context, app_id)` equality is not asserted.** Comment `7153866597` asks
   for it, on the grounds that all 16 entries carry `app_id 15368` and a name-only
   comparison would accept a same-named check from a different app.
   `/branches/main` returns `checks[].app_id`, so it is implementable — but it is
   a second assertion with its own failure mode, and adding it here would mean
   this work item changes two properties at once. Recorded as the next step
   rather than claimed.
3. **The count will drift again, and that is now the point.** When a context is
   added to protection without a §7 edit, the gate fails on the next run and
   names it. When §7 gains a line the platform does not require, the gate fails
   in the other direction. The gate is the enforcement; §7 is the single place
   the number lives.
4. **The ratification is recorded, not performed.** §7 and
   `AID-2026-059/manifest.yaml` now say the three session-evidence contexts are
   authorised from the window Issue #1029 comment `7153866597` identifies. That
   comment is the authority; this work item cites it and does not extend it.
5. **One carrier was left alone deliberately.**
   `AID-2026-055/session-evidence-1013-fix.md` states "15 required contexts" with
   its own timestamp inside the sentence. That is a dated measurement, correct
   for its moment, and rewriting it would destroy the record of the drift.
