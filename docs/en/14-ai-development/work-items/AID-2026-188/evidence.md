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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-188/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every number below was produced by running the committed files at base 1e9341da603dec78377fed240f4d6dbabaa8838e in this working tree: the root set and gap set were read by importing the gate module, the two baselines by read_baseline_entries(), the registry by reading its declared keys, and the two test suites by running them. No gate result, CI result or merge outcome is claimed that was not produced locally."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: "AID-2026-188 verification that the 03-memory-brain normative root and its three canonical documents are already registered, and that no further registration change is owed"
    canonical_scope_id: "ai-development/aid-2026-188-memory-brain-root-registration-verification"
    canonical_scope_keywords:
      - "bilingual"
      - "normative-root"
      - "memory-brain"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-188/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-188/evidence.md"
---

# AID-2026-188 — The `03-memory-brain` normative root is already registered: verification, not a repair

**Status: DRAFT — record only.** This work item changes no checker line, no baseline entry, no registry value and no mirror. It exists because the registration it was dispatched to perform had already landed, and a dispatch premise that stays uncorrected will keep producing the same no-op task.

## 1. Why this record exists

A repair contract was dispatched to add `"03-memory-brain"` to `NORMATIVE_ROOTS` in `scripts/check_bilingual_docs.py`, on the stated premise that the set held 13 entries and did not contain that root. The measurement below contradicts the premise: the root is the fourth entry of the set, the set is 13 entries *because* it contains that root, and adding it again is a no-op rather than a repair.

This is the third dispatch of the same unit. The first two failed for an unrelated upstream reason; the number of attempts is not itself evidence about the premise, but it does mean a fourth attempt would be dispatched from the same description unless the description is corrected on the record. Section 2 states the divergence as measured, section 3 gives the reproducible measurements, and section 6 lists what was deliberately not changed.

Nothing here asserts that the earlier registration was correct, complete or sufficient. It asserts only that the change being requested is already present at the stated base, so the requested edit cannot express it and a further edit pretending to make it would be a false claim.

## 2. Dispatch premise against the measured state

| # | Dispatched premise | Measured at `1e9341da` | Verdict |
|---|---|---|---|
| P1 | `NORMATIVE_ROOTS` holds 13 entries and does not contain `03-memory-brain`. | Holds 13 entries and contains `03-memory-brain` as the fourth entry (`check_bilingual_docs.py:20`). Without that root the literal would hold 12. | **Contradicted.** The count and the membership cannot both be as described. |
| P2 | `03-memory-brain/` has three canonical documents and `docs/en`, `docs/zh-CN` hold 13 mirrors each, including the three. | `03-memory-brain/` 3 files; `docs/en/03-memory-brain/` 13 files; `docs/zh-CN/03-memory-brain/` 13 files; all three canonical names present on both sides. | **Confirmed.** |
| P3 | Adding the root in-process moves `current_bilingual_gaps()` from 77 to 77, `new=0`, `gone=0`. | Reproduced, and it is the signature of an element already in a Python `set`: `set | {"03-memory-brain"} == set`. The observation is therefore consistent with the root already being present, not with a pending registration. | **Reproduced, reinterpreted.** A no-op proves the element was already there. |
| P4 | A second root inventory may exist in `check_bilingual_docs_full.py` and may need the same edit. | No second literal. That file imports `NORMATIVE_ROOTS` and *derives* the set from the tree, exiting 2 when the two disagree. | **Single definition.** |

P1 and P3 are the reason this work item is a verification record. A literal that already carries an element cannot be "fixed" by adding it: `NORMATIVE_ROOTS = {...}` is a `set` display, so the edit is absorbed silently and produces a zero-byte diff, which would have been reported as "applied" by any check that only compared exit codes.

## 3. Measurements

All commands were run in this working tree with `PYTHONUTF8=1` (section 8). Base is `origin/main` = `1e9341da603dec78377fed240f4d6dbabaa8838e`.

### 3.1 The root set

`scripts/check_bilingual_docs.py:19-24`:

```
19 : NORMATIVE_ROOTS = {
20 :     "00-governance", "01-system-architecture", "02-domain-model", "03-memory-brain",
21 :     "04-memory-compiler", "05-memory-runtime", "06-memory-context", "07-agent-integration",
22 :     "08-bmcp-protocol", "09-security-governance", "10-storage-consistency", "13-engineering-decisions",
23 :     "14-ai-development",
24 : }
```

`git blame` on that range attributes lines 19-20 to `6ab36b3697a0994d8de449d2b9c344f23aac0fda` (2026-11-26 22:02:51 +0800, `docs(memory-brain): restore three D normative roots (AID-2026-150)`). The original literal came from `32a35f422ba6442d1f700cfb327f348c0740a7f2`; the restore commit is the one that made `03-memory-brain` part of the enforced scope at this base.

Importing the module and reading the constant:

```
NORMATIVE_ROOTS count = 13
roots = ['00-governance', '01-system-architecture', '02-domain-model', '03-memory-brain',
         '04-memory-compiler', '05-memory-runtime', '06-memory-context', '07-agent-integration',
         '08-bmcp-protocol', '09-security-governance', '10-storage-consistency',
         '13-engineering-decisions', '14-ai-development']
03 in roots: True
```

### 3.2 Gaps, both baselines, copy agreement

```
gaps 77 baseline 77 new 0 gone 0
ci baseline entries 77
copies agree []
memory-brain gaps: []
```

- `current_bilingual_gaps()` = 77; `read_baseline()` (from `scripts/bilingual-baseline.txt`) = 77; `read_baseline_entries(CI_BASELINE_PATH)` (from `scripts/ci/baselines/bilingual-docs.txt`) = 77.
- `new = gaps - baseline = 0`, `gone = baseline - gaps = 0`: the gate's verdict is unchanged by the registration.
- `check_baseline_copies_agree()` returns `[]`, so the AID-2026-172 comparison sees the two frozen copies agreeing.
- No path under `03-memory-brain/` appears in the gap set, i.e. all three canonical documents are paired.

### 3.3 The other root list is derived, not copied

`scripts/check_bilingual_docs_full.py`:

- `:24-28` imports `EMBEDDED_BILINGUAL_SOURCES`, `NORMATIVE_ROOTS`, `PAIR_EXEMPT_PREFIXES` from the authority module.
- `:35-39` derives `_DERIVED_ROOTS` from `ROOT.iterdir()` by the `NN-name` shape.
- `:40-45` exits 2 when `_DERIVED_ROOTS != NORMATIVE_ROOTS`, printing both sets.

There is therefore exactly one root literal in the repository's Python sources, and the whole-tree inventory is bound to it by an equality assertion. **Only one definition exists**; no second list was updated because there is no second list to update. The comment at `:15-23` records why: this file previously carried its own copy, named seven directories that do not exist (including `03-memory-brain` at `:19`), and disagreed with the authority about the same bytes.

### 3.4 Whole-tree bilingual inventory

```
GOV-DOC-001 full scan: 906 in-scope Markdown files; 371 exempt; 77 violations.
```

That tool is the strict whole-repository inventory, not the incremental required gate, and it reports every baseline entry as a violation because it has no baseline of its own. Its count equals the frozen inventory, so it agrees with section 3.2 rather than contradicting it. Run at the post-change head it reports the same 77: this work item adds Markdown under `14-ai-development/work-items/`, which is a `PAIR_EXEMPT_PREFIXES` subtree, so no pairing obligation attaches.

### 3.5 The three documents are already governed documents

`00-governance/document-scope-registry.yaml:46-59` declares thirteen `governed:` roots, and `03-memory-brain` is line 50:

```
46 : governed:
47 :   - 00-governance
48 :   - 01-system-architecture
49 :   - 02-domain-model
50 :   - 03-memory-brain
...
59 :   - 14-ai-development
```

`scripts/check_document_management.py` classifies the files in that root:

```
03-memory-brain: 3/3 classified
GOV-DOC-002: 934 governed documents, 488 classified, 446 unclassified
```

`3/3` is the direct answer to the registry half of the dispatch: the three canonical documents are inside a governed root, are scanned, and carry parseable metadata. The 446 unclassified documents are the pre-existing whole-tree state and are reported by that gate for every root; they are not produced by this change.

There is one further structural point, and it is the reason the dispatched `documents:` edit is not owed. The registry has exactly four top-level keys — `governed:`, `governed_files:`, `backlog:`, `excluded:` — and **no `documents:` key at all**. Per-file registration exists only as `governed_files:` (`:70`), whose one entry is `docs/governance/documentation-gaps.md`: a file whose *directory* is not governed. Listing `03-memory-brain/*.md` there would assert that their directory is not governed, which is the opposite of the truth at line 50. The accounting identity the gate enforces is declared-scope-versus-disk, not a per-file roster inside a governed root, so appending three paths would make the exception list say something false and would not change any verdict.

## 4. Test results

Both suites that cover the script were run, because the dispatch named one path and the AID-2026-172 cases live in the other.

```
$ python -m unittest discover -s scripts -p "test_check_bilingual*"
Ran 15 tests in 8.353s
OK

$ python -m unittest discover -s tests -p "test_check_bilingual*"
Ran 7 tests in 0.000s
OK
```

The 15 are the AID-2026-172 additions: `BaselineCopyConsistencyTests` (5: identical copies pass, entry only in the frozen copy, entry only in the ratchet copy, missing ratchet copy fails closed, comments and blanks are not entries), `ChangedPathTests` (7, including `test_added_entry_refuses_and_leaves_file_untouched`, `test_missing_current_baseline_refuses`, `test_shrinking_set_is_written`), and `test_same_head_is_not_applicable_not_pass`. All pass unmodified. The 7 in `tests/` are the whole-tree inventory's own cases and pass as well.

`test_pair_checked_normative_doc_still_needs_manifest` is the case that would have gone red if a normative-root change had been made without its declaration; nothing here exercises it, because no such change was made.

## 5. What a reader should and should not conclude

Should: the registration described in the dispatch is present and enforced at `1e9341da`, the gap count is unchanged at 77 with zero new and zero resolved, the two frozen baselines still agree, the three canonical documents are paired and carry metadata, and the dispatch premise was wrong in a way that a fourth dispatch of the same text would repeat.

Should not: that the registration is *sufficient*, that the 77 gaps are acceptable, that the nine other canonical documents named in related work items have been restored, or that any Owner acceptance has occurred. `#1212` remains OPEN. `normative_status` here is `Informative`: this is a record of measurement, not a ruling.

## 6. Actions deliberately not taken

| Not done | Reason |
|---|---|
| Editing `NORMATIVE_ROOTS` | The element is already present; a set display cannot hold it twice, so the edit would produce an empty diff while appearing to satisfy the contract. |
| Regenerating either baseline | Both hold the same 77 entries, `new` and `gone` are 0, and the shrink-only writer would refuse a change that adds any entry. |
| Adding a `documents:` roster to the registry | No such key exists (section 3.5); `governed_files:` means "file outside a governed directory" and would misstate these three. |
| Adding `03-memory-brain/*.md` to `governed_files:` | Same reason, plus it would grow an exception list that exists to stay as small as its reason. |
| Any checker semantic change | Out of scope by the dispatch, and unnecessary: the verdict is already the intended one. |
| Restoring the remaining canonical documents | Explicitly excluded. Their absence is a separate, open decision. |
| Deleting or editing any mirror | Outside scope; the mirrors are what make the three documents paired. |
| Closing an Issue | Out of scope. |

## 7. Bilingual counterparts

`docs/en/14-ai-development/work-items/AID-2026-188/evidence.md` carries the same body with `canonical_status: Non-Canonical` and `source` pointing at this file. `docs/zh-CN/14-ai-development/work-items/AID-2026-188/evidence.md` carries the Chinese translation of the same sections. Both are mirrors of this document, not independent authorities, and neither claims semantic parity beyond a full rendering of sections 1-11.

## 8. Environment note (locale artefact, not a defect)

`PYTHONUTF8=1` is required on this host. Without it, Python's `subprocess` capture of `git` and `python` output decodes UTF-8 bytes under a GBK console codepage and raises `UnicodeDecodeError` on non-ASCII paths; the gate then reports a decoding failure that has nothing to do with the tree. Every command quoted above was run with `PYTHONUTF8=1`. This is a property of the Windows host locale, not of the checker, and no fix is proposed here.

## 9. Reproduction

```powershell
cd <worktree>
$env:PYTHONUTF8="1"
python -c "import importlib.util as u; s=u.spec_from_file_location('c','scripts/check_bilingual_docs.py'); m=u.module_from_spec(s); s.loader.exec_module(m); g=m.current_bilingual_gaps(); b=m.read_baseline(); print(len(m.NORMATIVE_ROOTS), '03-memory-brain' in m.NORMATIVE_ROOTS, len(g), len(b), len(g-b), len(b-g), m.check_baseline_copies_agree())"
# -> 13 True 77 77 0 0 []
python scripts/check_bilingual_docs_full.py   # -> 906 in-scope; 371 exempt; 77 violations (whole-tree inventory)
python scripts/check_document_management.py   # -> 03-memory-brain: 3/3 classified
python -m unittest discover -s scripts -p "test_check_bilingual*"   # -> Ran 15 tests, OK
python -m unittest discover -s tests -p "test_check_bilingual*"     # -> Ran 7 tests, OK
```

## 10. Limits

- Only the two scoring scripts and the registry were read for root declarations. A root literal in a workflow, a shell script, a Rust file or a crate fixture would be outside this record; the search was over `scripts/**/*.py` and `00-governance/*.yaml`.
- `git blame` was run on a full clone at the stated base; a shallow clone would misreport the boundary commit as the origin of the literal.
- No CI context, merge SHA or blob digest is claimed. AID-2026-188 is `DISPATCHED` / `PROVISIONAL` and its carrier is whatever pull request this record ships in.
- The dispatch is quoted verbatim in `prompt-v1.md`, including its two premise statements, so the disagreement is checkable rather than paraphrased.

## 11. Session role, input and output

The Session Evidence gate requires three parts from every evidence document a pull-request
body cites. Sections 1-10 state the measurement and its limits; this section states what
the executing session was, what it was told, and what it produced.

### Session role / use case

Verification worker inside a dispatched repair contract. The contract asked for
`"03-memory-brain"` to be added to `NORMATIVE_ROOTS`, for the three canonical documents to
be registered in the document scope registry, and for both frozen baselines to be left
alone. The root was already the fourth entry of the set and the three documents were
already `3/3 classified`, so the session measured the state, changed no checker, baseline,
registry or mirror, and published the measurement as this record instead of a zero-byte
edit.

### Actual AI input

The dispatched contract instructed the session to work only in the existing worktree on
`docs/2026-11-26-normative-root-03`, to add the root in the existing format and ordering,
to look for a second root inventory and synchronise it or record that only one definition
exists, to change neither baseline and never regenerate them, to keep the AID-2026-172 unit
tests green, to register the three documents in the registry, to create a work item with a
block-style metadata block and one `INDEX.md` row, to take a number from the pull-request
list, and to merge only after 16 of 16 required contexts passed on the exact head with
branch behind equal to 0. It also stated the host constraint that `PYTHONUTF8=1` is
required because the GBK console codepage breaks decoding of captured `git` output. The
contract text is pinned verbatim in `prompt-v1.md` (5934 bytes, SHA-256
`e0741732d3bd920e93729ecbd088cccc9bed2145c0e679891733f0aa804df9d2`).

### AI-visible output

The session reported the measured tuple `13 True 77 77 0 0 []` (root count, membership,
gaps, frozen baseline, new, gone, copy agreement), an empty `memory-brain gaps` set, the
`3/3 classified` count for the root, the absence of any second root literal, and the
absence of a `documents:` key in the registry. It reported local gate runs at
`1e9341da` with `PYTHONUTF8=1`: bilingual gate PASS on 7 changed paths, incremental
`GOV-DOC-002` PASS, repository hygiene new-file admission passed for 6 new paths, line
endings 0 violations, manifest parse 93 parsed and 0 failed, session evidence workflow
shape PASS, governance operation traceability PASS, traceability 0 errors, and unit tests
`Ran 15 tests ... OK` plus `Ran 7 tests ... OK`. It made no claim about a CI result that
had not been observed on the head under test.
