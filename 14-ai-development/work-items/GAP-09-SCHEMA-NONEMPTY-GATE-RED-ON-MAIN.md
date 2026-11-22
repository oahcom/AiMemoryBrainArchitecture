# GAP-09 — The schema non-empty gate is red on main

**Status:** Closed — gate green on `main @ 62827fbb` since `6897e53c` (2026-11-22). Closure criterion 4 (CI wiring) remains open; see the amendment at the end.
**Area:** 08-bmcp-protocol / schema audit
**Owner track:** Owner H (Protocol)
**Re-measured at:** `main @ 62827fbb`, 2026-11-22T07:54:32Z

## Gap statement

`08-bmcp-protocol/schemas/test_nonempty_audit.py` exits **1** on `main`. It
reports 5506 constraints that exist in schemas but are not registered in
`schema-nonempty-audit.md`.

The audit table was written against a baseline of **2** schemas. `#500` merged
**30** more and did not touch the table.

This is the gate working, not failing. GAP-04 built it to catch exactly this,
and it caught it. The defect is that the merge landed with the gate red and
nobody noticed, because the gate is not wired into CI.

## Evidence (verified on `main @ dc32fce3`)

**1. The gate exits 1 today.**

```sh
cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py; echo "EXIT=$?"
```

```
EXIT=1
```

5506 lines of output, every one of the form
`<schema>.json:<json-pointer>:<constraint>`, which is the script's
`item not in registered` branch (line 103). No `AUDIT_STALE:` lines appear, so
this is entirely unregistered constraints — the schemas grew, the table did not.

**2. It passed before #500.**

Exporting `main @ b961ba31` (the commit before #500) and running the same
script:

```
OK: 2 schemas; 93 registered constraints; no unregistered or stale entries.
EXIT=0
```

So this is a regression introduced by #500, not a pre-existing condition.

**3. #500 did not touch the audit table.**

```sh
git show 9a98956f --stat | grep -i audit
```

Zero matches. The table's last change is `3aaf761f` (#505).

**4. The table still declares the old baseline.**

`schema-nonempty-audit.md` opens with:

```
**Audit baseline:** `main` at `88bf4875...`. Scope: every direct-child `*.json`
in `08-bmcp-protocol/schemas/`; 2 files were present.
```

The schema directory now holds 32 `*.json` files.

**5. The sibling gate in the same area is green.**

`#535` added `08-bmcp-protocol/scripts/check_protocol_index.py` and
`tests/test_protocol_index_consistency.py`. Both pass on the same commit:

```
indexed_unique=22
missing=0
extra=0
duplicate_types=0
invalid_rows=0
PASS
```

```
8 passed in 0.14s
```

This matters because it rules out the excuse that the repository is simply in
a transitional state where gates cannot pass. Someone is actively adding
guards to this exact directory and getting them green. The non-empty audit was
skipped, not blocked.

It also means the red audit is not the only unautomated gate: neither
`check_protocol_index.py` nor `test_protocol_index_consistency.py` appears in
any workflow either. Only `rust-phase1.yml` runs tests on PRs.

## Why the obvious fix is wrong

The tempting fix is to regenerate the 5506 rows programmatically so the gate
goes green. That would destroy the artefact's purpose.

Every row in the table carries a human judgment that a generator cannot make:

| column | what it asserts |
|---|---|
| may be legally empty? | whether `""`/`[]` is a valid protocol state for this field |
| disposition | retain, narrow, or change |
| rationale | why, in domain terms |

The table's own summary shows these are real distinctions, not boilerplate: of
93 constraints, 2 conditional ones were **changed** because the previous
catch-all required highwaters even when the count was zero — "zero-count
incomplete/unavailable states may remain empty" and must not synthesize a
highwater.

Auto-registering 5506 unread rows would convert an audit into a manifest and
make the gate permanently green regardless of what any new schema does.

## Candidate directions

### (a) Audit the 30 new schemas properly, grouped by constraint family

5506 raw rows is not 5506 decisions. The new schemas come from a small number
of protocol families (`coc-jf10-unified` 1.2.0–1.2.17, `applied-ack`,
`recovery-cutoff`, `recovery-join`, `storage-prepared-participant-proof`,
`i-owner-snapshot-attestation`). Constraints repeat with identical meaning
across versions, so the work is a handful of family-level rulings plus a
generated projection of those rulings.

This is the only direction that preserves the artifact's meaning. It is Owner
H's decision because it encodes protocol semantics.

### (b) Scope the audit to a declared schema set

Change the script to audit only schemas listed in the table's baseline, so
adding a schema does not silently break the gate. This makes the gate green by
narrowing what it covers. It is honest only if the table explicitly says which
schemas are unaudited, and it creates a growing set of unreviewed schemas.

### (c) Fail closed in CI

Independent of (a) or (b): wire the script into CI so a red gate blocks the
merge instead of being discovered by a later measurement. Without this, the
same thing recurs on the next large schema merge.

## Recommendation

**(c) first, then (a).** CI wiring is small, and it converts this from "found
by accident during a measurement" into "cannot merge". Then do (a) as
family-level rulings, not row-by-row.

Direction (b) should be rejected unless the project genuinely intends to
support unaudited schemas, because it trades a visible red gate for an
invisible coverage hole.

## Closure criteria

1. `python3 test_nonempty_audit.py` exits 0 on `main`.
2. The table's stated baseline and inspected-schema count match reality.
3. Every schema in the directory is either audited or explicitly listed as
   out of scope with a reason.
4. The script runs in CI and blocks merges, so a red gate is not discovered
   weeks later.

## Round-eight re-measurement (2026-11-22 02:25 +08:00, `main @ 6696ca8a`)

Appended; §above is unchanged and still accurate. This narrows the numbers and
confirms the mechanism.

```
$ cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py; echo "EXIT=$?"
... 5506 lines of  <schema>.json:<pointer>:<constraint>  ...
EXIT=1
```

Unchanged from the previous measurement. Nothing was fixed in between; the item is
still red.

### The gap is now attributable to a single number

```
$ ls 08-bmcp-protocol/schemas/*.json | wc -l
32

$ sed -n 3p 08-bmcp-protocol/schema-nonempty-audit.md
**Audit baseline:** `main` at `88bf4875...` (2026-11-21). Scope: every
direct-child `*.json` in `08-bmcp-protocol/schemas/`; 2 files were present.
```

The audit table's own declared scope is *every direct-child `*.json` in this
directory*. It audited 2. The directory holds 32. The 30-file difference is the
5506 unregistered constraints, and the arithmetic is checkable: 93 registered
constraints over 2 files, 5506 unregistered over 30.

Provenance, from `git log --diff-filter=A`:

| commit | effect |
|---|---|
| `9a98956f` (#500) | merged the H protocol schemas — this is where the 30 files arrived |
| `3aaf761f` (#505) | last edit to the audit table itself |

`#500` added the schemas and did not extend the audit. `#505` touched the table
afterwards without noticing the scope mismatch. Both facts are in the log; neither
is an inference.

### Why regenerating the 5506 rows is still the wrong repair

The table is not a list of constraint strings. Each row carries a judgement:

```
| schema | location | constraint | may be legally empty? | disposition | rationale |
```

The table's own Summary documents that 2 conditional constraints were deliberately
*changed* in `#505` — "zero-count PARTIAL/NOT_ENUMERATED/UNAVAILABLE/UNKNOWN
states may have no reportable highwater and must not synthesize one". That ruling
required reading the schema's semantics. Auto-generating 5506 rows with a default
disposition would produce a table that passes the script and contains zero
judgements, which is a worse state than a red gate: it would be a green gate that
certifies nothing.

So closure criterion 3 ("every schema is either audited or explicitly listed as
out of scope with a reason") is the real work, and it is a reading task, not a
scripting task.

### Sibling-gate contrast, unchanged

For the same directory family, two other gates are green and measurable:

- `08-bmcp-protocol/scripts/check_protocol_index.py` → `missing=0 extra=0
  duplicate_types=0 invalid_rows=0 PASS`, exit 0.
- `08-bmcp-protocol/tests/conformance` → 585 passed / 27 skipped / 0 failed when
  `requirements.txt` is installed (see GAP-08's round-eight section).

Both are green. Only the non-empty audit is red. That removes the "the area is in
transition" explanation: three gates over one directory, two fine, one red, and the
red one is red because of a merge that predates the last edit to its own table.

### CI status, unchanged and now decisive

`#536` merged a workspace-wide rustfmt pass. CI did not run for it either. As
established in GAP-11 §6, every check run in this repository currently carries

> The job was not started because recent account payments have failed or your
> spending limit needs to be increased.

so wiring direction (c) today would import a red gate into a workflow that cannot
execute. That does not weaken the recommendation — it makes the ordering explicit:
**(a) must land before (c) is meaningful**, otherwise CI will be red for a reason
nobody can observe.

## Round-eleven closure of criteria 1–3 (2026-11-22, `main @ f3ddeb76`)

Direction (a) landed. The 30 unregistered schemas are audited by family-level
rulings in `08-bmcp-protocol/schema-nonempty-audit.md`; the rows are the
projection of those rulings, not a generated list.

```
$ cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py; echo "EXIT=$?"
OK: 32 schemas; 5599 registered constraints; no unregistered or stale entries.
EXIT=0
```

| criterion | state |
|---|---|
| 1. guard exits 0 on `main` | **met** — `OK: 32 schemas; 5599 registered constraints` |
| 2. stated baseline and inspected count match reality | **met** — baseline `f3ddeb76`, 2026-11-22, 32 files |
| 3. every schema audited or listed out of scope with a reason | **met** — 32/32 audited; nothing declared out of scope |
| 4. guard runs in CI and blocks merges | **NOT met** — unchanged, see below |

### What the audit actually decided

29 field-class rulings cover 223 distinct `(field, constraint)` pairs across
5506 triples. The classes are: reference/identity, fixed-width digest, canonical
counter, typed sequence/generation/position, signature, reason, PostgreSQL engine
identity, and purpose. Each class gets one ruling with its own domain rationale;
rows inherit it. Nine rows carry their own ruling instead, because their
semantics differ from their family:

- `owner_snapshots` `minItems: 3` — one snapshot per owner authority.
- `owner_release_refs` `minItems: 3` — epoch completion needs all three releases.
- `required_owner_release_refs` — `minItems: 1` in 1.0.0, `minItems: 3` from 1.0.1.
- `request_members` / `admission_members` / `members` / `participant_refs` /
  `participant_entries` `minItems: 1` — all five sit in `then` branches
  conditioned on COMPLETE_NON_EMPTY, and the COMPLETE_EMPTY branch caps the same
  array at `maxItems: 0`.
- `owner_admission_bindings` `minItems: 0` — the schema's own description says
  the empty array is a represented state.
- `recovery_observations` `minItems: 0` — no observation to report.
- `owner_snapshot_refs` / `owner_snapshot_digests` `minProperties: 1` — also
  `required: [I, D, C]`, so the floor is met by construction.
- `request_highwaters` / `admission_highwaters` — unconditional in 1.0.0/1.0.1,
  conditional from 1.0.2. The 1.0.2 form is the correct ruling; the older
  unconditional floors are frozen artefacts and are marked as superseded.

14 of the 5506 rows are recorded as legally empty; the other 5492 as not. That
split is the point: a generator with a default disposition would have produced
5506 identical verdicts and the gate would certify nothing.

### Two schema defects found while reading, not repaired

Neither is a non-empty question, so neither is fixed here — fixing either means
editing a schema.

1. `bmcp.recovery-cutoff` 1.0.3–1.0.5: `secondary_high_waters.propertyNames`
   requires `^[A-Z][A-Za-z0-9]*$`, while the sibling `allOf` branches require
   `receipt_issue`, `producer_registration`, `provider_attempt` and six other
   snake_case keys. Under `owner_kind` I/D/C those revisions have no satisfiable
   instance. 1.0.0–1.0.2 have no such branches and are unaffected.
2. `bmcp.coc-jf10-unified` 1.2.5: `owner_snapshots` changes from a 3-element
   array (1.2.0–1.2.4) to a `required: [I, D, C]` object. Both are non-empty by
   construction, but a consumer sharing one code path across 1.2.4 and 1.2.5
   sees a type change.

Both need an Owner H ruling. They are recorded in the audit table's "Open
questions for Owner H" section so they are not lost with this work item.

### Criterion 4 remains open

CI is still unable to execute: every check run in this repository carries the
billing message quoted above. Wiring `test_nonempty_audit.py` into a workflow
today would add a gate nobody can observe, which is the failure mode this item
was opened to name. Criterion 4 stays open until CI billing is restored; the
ordering established in the previous round is unchanged — (a) is now done, so
(c) becomes meaningful the moment CI can run.

## Amendment — GAP-09 closure re-verified, 2026-11-22T07:54:32Z, `main @ 62827fbb`

The gap statement and every round above are unchanged. This section records that
the gate is closed, and — more importantly — that the closure was re-verified
independently rather than accepted from the commit that claimed it.

### 1. The gate is green

```
$ python3 08-bmcp-protocol/schemas/test_nonempty_audit.py; echo "EXIT=$?"
OK: 32 schemas; 5599 registered constraints; no unregistered or stale entries.
EXIT=0
```

Same output and exit code at `62827fbb` (the commit named in the header) and at
current `origin/main` (`7d816980`). The pre-fix state reproduces too: at
`6897e53c^` the same script prints 5506 findings and exits 1.

### 2. The fix is a table extension, not a loosened check

The whole risk in a closure like this is that someone made the gate pass by
weakening the gate. It did not happen, and that is checkable four ways.

**The audit script was not touched.** Fix commit `6897e53cddbce58e1a28d7f1b7bf83fd439a39c5`:

```
$ git show 6897e53c -- 08-bmcp-protocol/schemas/test_nonempty_audit.py
(empty — 0 bytes, 0 lines)

$ git show --name-only --format="" 6897e53c
08-bmcp-protocol/schema-nonempty-audit.md
08-bmcp-protocol/schema-nonempty-audit.zh-CN.md
14-ai-development/work-items/GAP-09-SCHEMA-NONEMPTY-GATE-RED-ON-MAIN.md
14-ai-development/work-items/GAP-09-SCHEMA-NONEMPTY-GATE-RED-ON-MAIN.zh-CN.md
```

No file under `08-bmcp-protocol/schemas/` appears in the commit at all. The
script's git blob is byte-identical at all four points in the history:

```
$ for r in 6897e53c^ 6897e53c 62827fbb HEAD; do echo -n "$r: "; \
    git rev-parse "$r:08-bmcp-protocol/schemas/test_nonempty_audit.py"; done
6897e53c^: 88a6f33676c60860a139fb1ac0bb6f8ef6e7e742
6897e53c:  88a6f33676c60860a139fb1ac0bb6f8ef6e7e742
62827fbb:  88a6f33676c60860a139fb1ac0bb6f8ef6e7e742
HEAD:      88a6f33676c60860a139fb1ac0bb6f8ef6e7e742
```

**The script does not read the disposition column.** `test_nonempty_audit.py:81`
assigns `disposition = cells[4]` and never uses it again; registration is keyed on
`(schema, location, constraint)` only (`:83`). So a row cannot pass by
carrying a permissive disposition — either the triple is registered or it is not.
This is why "the dispositions were not downgraded" is a claim about the audit's
meaning, not about whether the script could be fooled.

**The change is additive.** `git show --numstat 6897e53c`:

| file | + | − |
|---|---|---|
| `08-bmcp-protocol/schema-nonempty-audit.md` | 5574 | 8 |
| `08-bmcp-protocol/schema-nonempty-audit.zh-CN.md` | 5574 | 7 |
| `GAP-09-SCHEMA-NONEMPTY-GATE-RED-ON-MAIN.md` | 75 | 0 |
| `GAP-09-SCHEMA-NONEMPTY-GATE-RED-ON-MAIN.zh-CN.md` | 62 | 0 |

The 8 deleted lines in the English table are all prose, and they are enumerated
here so the claim is auditable rather than asserted:

```
$ git diff 6897e53c^ 6897e53c -- 08-bmcp-protocol/schema-nonempty-audit.md \
    | awk '/^---/{next} /^-/{print}'
```

1 baseline line (`88bf4875` / 2 files), 5 Summary bullets (old counts), 1
`## Complete inventory` heading, 1 paragraph under it. The heading was replaced
by `## Pattern note`; the old Summary was replaced by the new one. **Zero table
data rows were deleted or altered** — all 107 survive verbatim.

### 3. Row and constraint counts, before and after

Parsed with a pipe-escape-aware splitter (the `pattern` cells contain escaped
`\|`, which naive splitting miscounts):

| | before `6897e53c` | after `6897e53c` |
|---|---|---|
| table sections | 1 | 7 |
| data rows | 107 | 5613 |
| rows that are constraints | 93 | 5599 |
| rows that are notes (`Retain required; no minItems`) | 14 | 14 |
| empty `rationale` cells | 0 | 0 |
| shortest `rationale` (chars) | 48 | 48 |
| pre-existing rows preserved verbatim | — | 107 / 107 |

5506 constraint rows added, 93 + 5506 = 5599 — which is exactly the number the
script reports as registered. The 14 note rows are the same 14 in both states.

### 4. No disposition was downgraded

The 93 `Retain, narrowed` dispositions are all still present, by exact string
count in the file (`grep -c "Retain, narrowed"` → 93 before, 93 after). Every one
of the 5599 constraint rows carries a disposition beginning with `Retain`; there
are zero rows with a disposition that does not (`Accept`, `Exempt`, `Drop`, or
empty). Full distribution:

| disposition | rows |
|---|---|
| `Retain` | 5478 |
| `Retain, narrowed` | 93 |
| `Retain, conditional` | 17 |
| `Retain; schema defect recorded` | 6 |
| `Retain; narrowed in 1.0.2` | 4 |
| `Retain; superseded by 1.0.1` | 1 |

The distribution also shows the rows are not boilerplate: 14 rows are recorded as
legally empty (`Yes — …`) and the other 5585 as not, and there are 38 distinct
rationale strings and 29 distinct "may be legally empty?" strings. A generator
with one default verdict would have produced one value in each column.

### What this amendment does not claim

Criterion 4 from §Closure criteria is still **not met**: `test_nonempty_audit.py`
is still not wired into CI. The gate is green because the table is complete, not
because a merge would now be blocked if it went red again. That remains the open
half of this work item, and it is blocked on CI billing, not on the audit.

The two schema defects recorded in §Two schema defects found while reading are
also still unrepaired and still need an Owner H ruling. Closing the gate did not
close them.
