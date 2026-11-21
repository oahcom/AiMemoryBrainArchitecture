# GAP-09 — The schema non-empty gate is red on main

**Status:** Open — `main` fails its own documented gate
**Area:** 08-bmcp-protocol / schema audit
**Owner track:** Owner H (Protocol)

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
