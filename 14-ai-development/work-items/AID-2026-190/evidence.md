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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Every count below was produced locally in this working tree at base 4326669caa6c43193d34219a0451b80762b712ff by running the quoted git commands; the ten-case run against 8142b1ca was executed against files extracted with git archive from that commit. The two records this work item corrects are quoted, not re-asserted. No CI result, merge result or blob digest is claimed that was not produced by a command shown here."
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
    canonical_status: Canonical
    canonical_scope: "AID-2026-190 correction of two governance records whose pasted test output and new-blob identities cannot be reproduced from the repository tree"
    canonical_scope_id: "ai-development/aid-2026-190-unreproducible-governance-identities"
    canonical_scope_keywords:
      - "governance-register"
      - "restore-evidence"
      - "blob-identity"
      - "reproducibility"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-190/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-190/evidence.md"
---

# AID-2026-190 — Two governance records carry test output and blob identities the repository cannot reproduce

**Status: DRAFT — record and correction only.** No historical table, no historical claim and no front-matter declaration is edited. Each affected file received exactly one appended `## Correction (2026-11-27)` section, and the two `verification_status` fields keep the values their original authors wrote.

## 1. Why this record exists

Two merged records assert verification that the tree does not support:

- `14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` §2 pastes ten `ok` lines produced by `python -m unittest discover -s 04-memory-compiler/reference-model`, and §3 builds a mutation table (M0 baseline, M1/M2 KILLED, M3 SURVIVED) on top of that baseline. On `origin/main` there is no `04-memory-compiler/reference-model` directory and no test file containing any of the ten names.
- `14-ai-development/work-items/AID-2026-113/restore-evidence.md` declares `verification_status: Verified` with the note "Source and mirror blob identities … recorded", and its two tables list 15 new-blob SHAs. None of the 15 resolves as a git object; none equals the blob the path actually carries.

Both documents are cited later as if their numbers had been derived. A record that cannot be re-derived from the repository is worse than a missing record, because it transfers trust it never earned. This work item therefore does not rewrite either document. It appends the measurement that a reader of `main` can re-run, and states what that measurement does and does not support.

## 2. GOV-REV-2026-11-21-PR425-001 — ten `ok` lines, zero matching code

Measured at `origin/main` = `4326669caa6c43193d34219a0451b80762b712ff`.

| Quantity | Value | How it was measured |
|---|---|---|
| Files under `04-memory-compiler/` at HEAD | 7 | `git ls-tree -r --name-only HEAD -- 04-memory-compiler` |
| Files under `04-memory-compiler/reference-model/` at HEAD | 0 | same command with that path |
| Python files at HEAD containing any of the ten case names | 0 | ten separate `git grep -c -F "<name>" HEAD -- "*.py"`, each with no output and exit 1 |
| Documents at HEAD containing the ten names | 3 per name, plus `TEST-DRAFT-2026-11-21-PR425-M3.md` (canonical / en / zh-CN) for `test_validation_rejects_digest_mismatch` | `git grep -l -F "<name>" HEAD` |
| Commits reachable from `origin/main` that ever held `04-memory-compiler/reference-model` | 0 | `git merge-base --is-ancestor 8142b1ca origin/main` exits 1 |

### 2.1 The one place the ten cases do exist

`git ls-remote --heads origin owner-e/gap-01-memory-compiler-contract` returns `8142b1caadd17770685d0b1f2816e584065854ac`, i.e. the exact head recorded in §1 of the register, on a branch that was never merged. Extracting `04-memory-compiler/reference-model` from that commit with `git archive` and running the register's own discovery pattern there produced:

```
Ran 10 tests in 0.001s

OK
EXIT=0
```

So the appended correction does not call the pasted output fabricated. It records the narrower and checkable defect: the output is reproducible only against an unmerged branch that the record never names as a branch — §1 pins a commit object that is unreachable from `main` and present only after an explicit fetch. Anyone holding `main` alone cannot verify §2, and therefore cannot verify the M0 baseline that §3's three mutation verdicts are stated against.

Conclusion recorded in the file: `NOT_VERIFIABLE_FROM_REPOSITORY`.

## 3. AID-2026-113 — fifteen new-blob identities, none resolvable

| Quantity | Value |
|---|---|
| New-blob cells in the two tables | 15 (5 Canonical + 10 mirror) |
| New-blob SHAs that resolve via `git cat-file -t` | 0 of 15 (`fatal: git cat-file: could not get object info`, exit 128) |
| New-blob SHAs equal to the blob at `origin/main:<path>` | 0 of 15 |
| New-blob SHAs equal to the blob at the restoring commit `9142698f:<path>` | 0 of 15 |
| Source, original and orphan blob SHAs in the same tables that resolve | 17 of 17 |
| Canonical source blobs equal to `1908ce4d:<path>` | 5 of 5 |
| Lines removed when diffing `1908ce4d:<path>` against `9142698f:<path>` | 0 for all five |
| Frontmatter lines added by the restore | 47 / 48 / 53 / 47 / 48 |

The restoration itself is real: all fifteen paths exist on `main`, and each Canonical file gained frontmatter only, which is what `FRONTMATTER_ADDED; source body retained unchanged` says. What fails is the identity column. A SHA-1 absent from the object database cannot identify any committed version of that path, so the column cannot describe the restoration the document reports, and the `Verified` note that rests on it does not hold as written.

Conclusion recorded in the file: `NEW_BLOB_IDENTITIES_NOT_VERIFIABLE`.

## 4. What was changed, and what was not

Six files were modified, by appending only:

| File | Lines added | Lines removed |
|---|---|---|
| `14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` | 91 | 0 |
| `docs/en/14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` | 91 | 0 |
| `docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-21-PR425-001.md` | 91 | 0 |
| `14-ai-development/work-items/AID-2026-113/restore-evidence.md` | 70 | 0 |
| `docs/en/14-ai-development/work-items/AID-2026-113/restore-evidence.md` | 70 | 0 |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-113/restore-evidence.md` | 70 | 0 |

Not changed, deliberately:

- no historical table cell, no pasted output block, no prose paragraph above the appended section;
- no `verification_status`, `last_verified_date` or `last_verification_note` value — the original declarations stay readable exactly as written, and the correction states next to them that they do not hold;
- no blob, no canonical document under `05-memory-runtime/`, no file under `04-memory-compiler/`;
- no checker, baseline, registry, workflow or required context;
- no re-declaration of either document as verified, and no claim about what a §5 reviewer would conclude.

## 5. Reproduction

```bash
# GOV-REV-2026-11-21-PR425-001
git ls-tree -r --name-only HEAD -- 04-memory-compiler/reference-model        # zero lines, exit 0
git ls-tree -r --name-only HEAD -- 04-memory-compiler                        # seven files, no reference-model/
git grep -c -F "test_derive_identity_is_stable" HEAD -- "*.py"               # no output, exit 1
git grep -l -F "test_validation_rejects_digest_mismatch" HEAD                # six documents, no code
git ls-remote --heads origin owner-e/gap-01-memory-compiler-contract
git merge-base --is-ancestor 8142b1ca origin/main; echo $?                   # 1

# AID-2026-113
git cat-file -t 028bc3b63693145617290ef1b8f8cd617f931e2e                     # fatal, exit 128
git rev-parse origin/main:05-memory-runtime/activation-policy-engine.md      # 11ee1a70…
git rev-parse 9142698f:05-memory-runtime/activation-policy-engine.md         # ce15bec1…
```

Every `git grep ... -- "*.py"` above was run separately for each of the ten names in the correction section; all ten printed nothing and exited 1.

## 6. What this record does not claim

- It does not claim the pasted ten `ok` lines were invented; it records that they cannot be reproduced from anything reachable from `main`, and names the branch where they can.
- It does not claim the AID-2026-113 restoration did not happen; it records that the identity column describing it is unresolvable while the restoration content itself checks out.
- It does not assert that either original author acted in bad faith. Identity columns and pasted terminal output are the easiest things to transcribe by hand and the hardest to notice when wrong.
- It does not close or reopen any Issue, and it asserts no acceptance decision for either document.
