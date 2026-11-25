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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every count in this prompt came from a measurement run on 2026-11-25 against main 68591920, not copied from another record."
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

# AID-2026-077 — Parse every work-item manifest, not one of them

## The gap, measured

At `68591920` there are **50** `14-ai-development/work-items/AID-*/manifest.yaml` files.
All **50** parse under a loader that rejects duplicate keys. That is the good news, and it
is the reason this is a gate work item rather than a repair one: the corpus is clean today,
so a gate can be made to enforce that without first having to make it true.

The bad news is that nothing enforces it.

`.github/workflows/aid-2026-001-manifest-validation.yml` is the only strict-parse job in
CI. Its trigger names one path:

```yaml
on:
  pull_request:
    paths:
      - "14-ai-development/work-items/AID-2026-001/manifest.yaml"
```

and the job itself hard-codes the same file:

```python
path = Path("14-ai-development/work-items/AID-2026-001/manifest.yaml")
```

So the loader is correct, the regression guards are correct, and the coverage is one file
in fifty. A manifest other than `AID-2026-001` can be unparseable and no check runs.

`scripts/ci/check_repository_hygiene.py` looks like it covers manifests and does not. It
contains no `import yaml` and no `safe_load`; it reads manifest content as text and pulls
scalars out with `_top_level_manifest_scalar`, a regular expression over unindented lines.
Its summary line `manifests=50 violations=0` is a statement about that text scan. A
structurally broken but valid-UTF-8 manifest cannot fail it.

## Why this is not a re-filing

`b34c8e37` (on `main`) repaired the last four unparseable manifests and closed with:

> 49 manifests are parsed by nothing. That gap is recorded here, **not fixed here** —
> widening it needs its own work item, since a job that starts failing on 3 existing files
> cannot be made required without first making them pass, which is what this commit does.

That commit made them pass. This work item is the "own work item" it defers to. The
ordering the commit describes is now satisfiable in the order it described.

## The silent case, which is the reason for a strict loader

The dangerous manifest is not the one that fails loudly. `AID-2026-029` before `b34c8e37`
declared `related_prs` twice:

```yaml
related_prs: [356]     # line 8, added by d8fdf54 (the closeout commit)
related_prs: []        # line 9, added earlier by 84b1255
```

`yaml.safe_load` returns a document, `related_prs` comes back `[]`, and PR 356 — the pull
request that carried the implementation — is discarded with no error. `b34c8e37` records
that the project's line-based parser read the *first* value while PyYAML read the *last*,
so the same file said two different things to two readers.

A check that only asserted "the file loads" would have passed that file both before and
after. The duplicate-key rejection is the whole point, not a nicety.

## Scope

One checker, one test module, one workflow step. The checker must:

1. enumerate every `14-ai-development/work-items/AID-*/manifest.yaml`;
2. parse each with a duplicate-key-rejecting loader;
3. exit non-zero naming the path and the parser message on any failure;
4. state, in its own output, what it does **not** verify.

Point 4 is a requirement and not a courtesy: `manifests=50 violations=0` has already been
read as parseability evidence once. The new check must not create a second line that can be
misread the same way.

## Acceptance criteria

**AC1 — every manifest is parsed, and the count is printed.** A run over the real tree
prints the number of manifests found and exits 0. Settled by the run itself, and by the
printed count equalling `ls -d 14-ai-development/work-items/AID-*/ | wc -l`.

**AC2 — a duplicate key fails where the default loader succeeds.** A fixture declaring the
same key twice parses under `yaml.safe_load` and the check exits non-zero. Settled by the
fixture, asserting both halves: that `safe_load` returns a document, and that the check
rejects it.

**AC3 — a syntax error in any manifest fails, naming the path.** A fixture with an
unquoted scalar containing `": "` makes the check exit non-zero and print that path.
Settled by the fixture and by the path appearing in the output.

**AC4 — it runs on every pull request.** The check is named in a workflow step with no
`paths:` filter that excludes manifests. Settled by the workflow file and by the check
appearing in a pull request's job log.

**AC5 — a green run is not read as semantic correctness.** The output states that the check
verifies parseability only and does not verify that fields mean what they say, that
referenced commits exist, or that status values are current. Settled by that sentence being
present in the output of a passing run.

**AC6 — the four manifests repaired by `b34c8e37` are parse-checked at this work item's
landing commit.** The check exits 0 over `AID-2026-023`, `-029`, `-040` and `-055`.
Settled by a run over the real tree, and by naming those four so that a future reintroduction
of the defect is a visible regression of this work item rather than a new discovery.

## What this does not authorise

- No change to `check_repository_hygiene.py`. Its text scan is the subject of this work
  item, not a thing this work item edits.
- No change to `aid-2026-001-manifest-validation.yml`'s existing behaviour for
  `AID-2026-001`; the new check is additional.
- No required status context. The concern `b34c8e37` raised — that a job cannot be made
  required while it fails on existing files — is answered by AC6, not by this work item
  promoting itself into branch protection.
- No semantic validation of manifest contents. AC5 exists to keep that boundary explicit.

## Provenance, stated plainly

This work item was written after `b34c8e37` had already repaired the four manifests. An
earlier draft prepared independently in this session repaired the same four files without
knowledge of `b34c8e37`; when `origin/main` was fetched that work was found to be redundant
and was dropped rather than merged alongside. The measurement above is against `68591920`,
which contains `b34c8e37`. The repairs are not claimed here as this work item's, and the
ordering — repairs first, gate second, by different commits — is recorded rather than
presented as a single clean act.
