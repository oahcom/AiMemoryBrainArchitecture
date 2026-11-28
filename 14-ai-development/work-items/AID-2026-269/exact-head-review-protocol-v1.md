---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Reusable review protocol definition; no acceptance decision is asserted."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Reusable Exact-Head independent review protocol for AID-2026-269"
    canonical_scope_id: "ai-development/aid-2026-269-protocol"
    canonical_scope_keywords:
      - "exact-head-review"
      - "sha256-recomputation"
      - "historical-assertion"
      - "error-grading"
    canonical_conflict_status: None
    normative_status: Informative
---

# Exact-Head Independent Review Protocol v1.2

Protocol identifier: `Exact-Head Independent Review Protocol v1` (stable wire identifier, unchanged by document revision; this document is revision v1.2)
Owner work item: AID-2026-269
Status: reusable procedure. This document defines the judgement layer that sits above the automated checkers, plus the reference procedures, inputs, grading and evidence structure used where no checker covers a case. It does not contain a review result.

---

## 1. Scope and declaration taxonomy

### 1.1 What the protocol covers

The protocol is applicable to any declaration that can be recomputed from committed Git objects at a locked candidate commit. Required coverage classes:

1. SHA-256 values declared in `manifest.yaml`.
2. Prompt file digest and byte count.
3. Evidence blob identity.
4. Root blob identity.
5. Digests copied into `INDEX.md`.
6. Traceability claims: work-item attribution, PR number, merge SHA.
7. Executable acceptance assertions: test counts, passing test counts.
8. Any other claim independently recomputable from committed objects.

### 1.2 What the protocol does not cover

Claims that cannot be recomputed from committed objects are still in scope as declarations, but they are classified `NON_MACHINE_ASSERTION` and must be recorded as unverifiable. They are never defaulted to PASS.

### 1.3 Declaration taxonomy

Every declaration under review is assigned exactly one class before any computation starts. The class fixes the judging method.

| Class | Judging method | Required evidence |
|---|---|---|
| `BLOB_IDENTITY` | Read raw bytes from the committed object and recompute SHA-256 | blob object SHA, recomputed SHA-256, byte count, candidate SHA |
| `COMMIT_IDENTITY` | Parse and verify against the Git object database | full commit SHA, tree SHA, parent SHAs, object type check |
| `COUNT_ASSERTION` | Re-execute the named test command and count results | command line, exit code, raw count output, environment |
| `ATTRIBUTION` | Compare against commit, PR, work item, and original evidence records | commit SHA, PR number, work-item ID, evidence file reference |
| `HISTORICAL_ASSERTION` | Recompute within an explicitly bounded historical ref range | ref list, per-commit per-path digest table, search envelope statement |
| `NON_MACHINE_ASSERTION` | Mark as requiring human judgement | reason the claim is not machine-checkable; never a pass |

Rules:

- A declaration that cannot be assigned a class blocks completion; record it as `E4 INCOMPLETE_EVIDENCE`.
- A `NON_MACHINE_ASSERTION` is recorded as `E6 UNVERIFIABLE`, not as verified.
- Classification is per declaration field, not per file. One file may yield several declarations of different classes.

---

## 2. Division of labour with automated checkers

The mechanical recomputations this protocol once described are implemented as automated checkers. Where a checker exists, the protocol does **not** re-teach the recomputation: it does not restate the algorithm, and it does not compete with the checker's output. Checkers known at the time of writing:

| Checker | Covers |
|---|---|
| #1426 | blob-pin field discovery |
| #1451 | blob-pin integrity verification |
| #1449 | negative-sample / base-binding |

The protocol's normative content is the layer no checker can occupy:

1. **Envelope honesty.** Every conclusion states the refs, commits, paths and time it was computed over, and may claim absence only within that envelope (section 5.6). A conclusion whose envelope is unstated is not a conclusion.
2. **Immutable head binding.** A review is bound to a full commit SHA. A head is a named observation, not a moving "current" state: a later head is a new observation appended to the record, and no earlier head's findings, line numbers, counts or verdict are overwritten by it. Branch names, `main`, `HEAD` and PR heads are locators, never substitutes for a commit identity (section 3).
3. **Interpretation when multiple heads disagree.** Divergence between heads is expected and is not itself a defect. Each measurement is read only at the commit it is bound to, a later measurement never corrects an earlier one retroactively, and only candidate drift inside a single review is graded `E5` (sections 6 and 7).
4. **Adjudication ownership, and what an acceptance may claim.** Only the designated adjudicator assigns final grades. An acceptance may claim no more than the graded declarations it covers, at the SHA it names: it does not extend to other heads, and it does not rehabilitate an earlier head's findings.
5. **A mechanism's PASS is a statement about the mechanism, never about the truth of a declaration.** A green checker, a complete envelope, or a completed review says the machinery ran and was satisfied. It does not say the declaration is true, and it never converts an `E1`, `E2` or `E3` into a pass.

Sections 4 and 5 are **reference procedures**: normative only where no checker covers the case. Where a checker covers a case, its recorded output is the evidence and sections 4–5 describe how to read that output; where no checker covers the case, sections 4–5 are the procedure and their requirements bind as before. A hand recomputation does not outvote a checker on a case the checker covers; where both exist, the stated envelope decides which result is admissible.

---

## 3. Exact-Head locking (inputs)

### 3.1 Lock commands

Execute in order, at review start, from a clean checkout of the review repository. `CANDIDATE_SHA` must be a full 40-character commit SHA supplied as input, not a branch name, tag, or abbreviated SHA.

Prohibited substitutions: `CANDIDATE_SHA` is never filled from `base_sha`, `origin/main`, `main`, `HEAD`, `HEAD~N`, `@{u}`, a tag, a remote-tracking ref, or any other ref expression, even when the resulting SHA is full-length and even when the substituted expression happens to resolve to the same commit. A candidate obtained by `git rev-parse HEAD` is not a supplied candidate. The outputs of `git rev-parse origin/main` and `git rev-parse HEAD` are recorded only as observed values (`base_sha` in section 3.2, and a note), never as `candidate_sha`.

Grade: a lock performed against a substituted ref is `E4 INCOMPLETE_EVIDENCE` on the lock step — the required input was not obtained, so nothing downstream is a complete pass. Where the substituted expression resolves to a different commit during the review, the same review is additionally `E5 CANDIDATE_DRIFT`. Re-lock from the supplied `CANDIDATE_SHA` and re-run from this section before proceeding.

```bash
git fetch origin --prune

git rev-parse origin/main

git rev-parse --verify "$CANDIDATE_SHA^{commit}"

git rev-parse "$CANDIDATE_SHA^{tree}"
```

`git rev-parse --verify "$CANDIDATE_SHA^{commit}"` must echo the full commit SHA. If it fails, or if the echoed SHA differs from the supplied `CANDIDATE_SHA`, stop and record `E5 CANDIDATE_DRIFT`.

### 3.2 Mandatory metadata block

Record before any declaration is checked. An incomplete metadata block is `E4 INCOMPLETE_EVIDENCE`.

```text
review_start_utc        # ISO-8601, Z suffix
repository              # owner/name
base_sha                # output of: git rev-parse origin/main
candidate_sha           # full commit SHA
candidate_tree_sha      # output of: git rev-parse "$CANDIDATE_SHA^{tree}"
pr_number               # integer, or null when absent
reviewer_identity       # session or agent identifier, distinct from author
git_version             # output of: git --version
python_version          # output of: python3 --version, or null when no Python recomputation ran
fetch_command           # exact fetch line executed
```

### 3.3 Candidate-tree vs working-tree rule

All byte reads come from the candidate commit's tree, addressed as `$CANDIDATE_SHA:$PATH` or via `git cat-file blob "$BLOB_SHA"`. The working tree is never a source of truth. A result computed from the working tree is `E4 INCOMPLETE_EVIDENCE`.

### 3.4 Drift rule

Any change to `candidate_sha` during the review invalidates every prior conclusion in that review. Re-lock and re-run from section 3.1. A review whose candidate SHA changed and was not re-run end to end is `E5 CANDIDATE_DRIFT`.

---

## 4. Blob recomputation

**Reference procedure — normative only where no checker covers the case.** Blob-pin field discovery (#1426) and blob-pin integrity verification (#1451) cover the ordinary case; this section applies where no checker does.

### 4.1 Enumerate the candidate tree

```bash
git ls-tree -r -z "$CANDIDATE_SHA"
```

Parse the `-z` output as NUL-delimited records of the form `<mode> SP <type> SP <object> TAB <path>`. Do not split on newlines; paths may contain characters that a line-based parser mangles. Build the path → object mapping from this output only.

### 4.2 Read raw bytes

```bash
git cat-file blob "$BLOB_SHA"
```

Redirect to a file or read as bytes in the recomputation program. Never pipe through anything that performs encoding conversion or newline translation.

### 4.3 Recompute

```python
import hashlib

actual = hashlib.sha256(blob_bytes).hexdigest()
```

`blob_bytes` must be the exact byte sequence stored in the object, obtained without decoding.

### 4.4 No text decoding before hashing

Hashing is performed on raw bytes only. Prohibited before the digest call:

- decoding to `str` (`.decode(...)`, `text=True`, `encoding=`), including UTF-8;
- newline normalization (`\r\n` ↔ `\n`), BOM stripping, or trailing-whitespace trimming;
- reading through a shell that re-encodes stdout (for example PowerShell redirection with a non-binary encoding);
- reading the working-tree file instead of the blob;
- reading `git show` output through a pager or a formatter.

Any digest produced after a text conversion is invalid and the declaration is `E4 INCOMPLETE_EVIDENCE`.

### 4.5 Two distinct identifiers

`actual_blob_object_sha` is the Git object name of the blob (SHA-1 object ID from `ls-tree`). `actual_sha256` is the SHA-256 of the blob content. They are different functions over different byte streams and must not be substituted for each other.

### 4.6 Mandatory per-declaration record

One record per declaration field. Missing fields make the record `E4 INCOMPLETE_EVIDENCE`.

```text
declaration_file          # path of the file that makes the claim
declaration_line          # 1-based line number of the claim
declaration_field         # field name, e.g. prompt_sha256
declared_path             # path the claim refers to
declared_sha256           # value as written in the declaration
actual_blob_object_sha    # Git object ID resolved from ls-tree
actual_sha256             # hashlib.sha256(blob_bytes).hexdigest()
actual_bytes              # len(blob_bytes)
candidate_sha             # locked full commit SHA
command                   # exact command line executed to obtain the bytes or the count
exit_code                 # integer exit status of that command
result                    # MATCH | MISMATCH | UNVERIFIABLE
```

An empty `command` field, or an `exit_code` that is missing, blank, or unrecorded, makes the record `E4 INCOMPLETE_EVIDENCE` even when `declared_sha256` equals `actual_sha256`. A record without an execution trace is not evidence of execution. A non-zero `exit_code` on a record that nonetheless carries a digest is also `E4`: the digest did not come from a successful read.

### 4.7 Checks that must all hold

1. The declared path exists in `git ls-tree -r "$CANDIDATE_SHA"`.
2. The path resolves to the object whose ID was recorded.
3. The object is of type `blob` and its bytes are readable.
4. The digest was computed without text conversion (section 4.4).
5. `declared_sha256` equals `actual_sha256` character for character, lowercase hex, no truncation.
6. Where a byte count is declared, it equals `actual_bytes`.

Failure of 1–4 is `E4`. Failure of 5 or 6 is `E1 DECLARATION_MISMATCH`.

---

## 5. Historical assertion verification

**Reference procedure — normative only where no checker covers the case.** Negative-sample and base-binding (#1449) cover the ordinary case; this section applies where no checker does.

### 5.1 What is being tested

A historical assertion claims that a value appeared, or never appeared, in history. Both directions require the same machinery: enumerate the reachable history, recompute every version of the relevant paths, and compare.

### 5.2 Enumerate reachable commits

```bash
git rev-list --all
```

### 5.3 Enumerate per-path history

Run once per path. Never combine paths into one invocation and then attribute results by guessing.

```bash
git rev-list --all -- \
  14-ai-development/work-items/AID-2026-083/prompt-v1.md \
  14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

For multi-path invocations, re-run per path (`-- <path>` one at a time) whenever attribution matters. Filenames, commit SHAs, and digests must never be mixed in a way that loses which commit belongs to which path.

### 5.4 Recompute each historical version

```bash
git show "$COMMIT:$PATH" | sha256sum
```

Byte-exact equivalent, preferred where any encoding layer is in play:

```bash
git cat-file blob "$COMMIT:$PATH" > /tmp/blob.bin
python3 -c "import hashlib,sys;print(hashlib.sha256(open('/tmp/blob.bin','rb').read()).hexdigest(), len(open('/tmp/blob.bin','rb').read()))"
```

Both forms must produce identical digests for the same object. A `git show ... | sha256sum` pipeline is acceptable only when the shell is byte-transparent; on Windows shells, use the `git cat-file` form.

### 5.5 Mandatory per-version record

```text
commit_sha
path
command        # exact command line executed for this version
exit_code      # integer exit status of that command
byte_count
sha256
```

An empty `command` field, or an `exit_code` that is missing, blank, or unrecorded, makes the row `E4 INCOMPLETE_EVIDENCE`, and any conclusion resting on that row inherits `E4`. A non-zero `exit_code` on a row that nonetheless records a digest is also `E4`: the digest did not come from a successful read.

Store every row. Do not store only a deduplicated or `sort -u` result: the un-deduplicated set is the evidence that the enumeration ran.

### 5.6 Mandatory search-envelope statement

Every historical conclusion carries an explicit envelope. A conclusion without one is `E4 INCOMPLETE_EVIDENCE`.

```text
refs_checked            # exact list of refs present after the fetch
fetch_command           # exact command, e.g. git fetch origin --prune
fetch_time_utc          # ISO-8601
reachable_commit_count  # wc -l of git rev-list --all
paths_checked           # exact path list
unreachable_objects     # "excluded"
refs_not_checked        # explicit list, or "none"
```

Rules:

- Unreachable objects (dangling commits, reflog-only commits, unreferenced packs) are excluded from the conclusion and must be named as excluded.
- Any ref not fetched, or not present at fetch time, must be listed under `refs_not_checked`. A ref that was not checked must never be described as checked.
- "Never appeared in history" may only be stated relative to the stated envelope, in the form: "no version with digest X exists in the commits reachable from the refs listed above, as of fetch_time_utc".

### 5.7 First-introduction claims

Where the assertion concerns the first commit that introduced a path or value:

```bash
git rev-list --all --reverse -- <path> | head -1
git log --diff-filter=A --format=%H -- <path>
```

Record the resulting commit SHA, then recompute that commit's version of the path per section 5.4 and record its byte count and digest. When two files are claimed to have appeared in the same commit, verify both paths resolve in that single commit; do not infer co-introduction from independent first-introduction results.

---

## 6. Error grading

Grades are assigned per declaration. The review's overall grade is the union of all declaration grades.

| Grade | Name | Trigger | Handling |
|---|---|---|---|
| `E0` | `VERIFIED` | All evidence independently recomputed and consistent | May contribute to PASS |
| `E1` | `DECLARATION_MISMATCH` | Declared value differs from the recomputed value | Never PASS |
| `E2` | `HISTORICAL_NONEXISTENCE` | Declared value never appears within the stated historical envelope | Never PASS |
| `E3` | `ATTRIBUTION_MISMATCH` | Attribution, commit, PR, or correction record is wrong | Never PASS |
| `E4` | `INCOMPLETE_EVIDENCE` | Original evidence missing or review envelope incomplete | Never a complete pass |
| `E5` | `CANDIDATE_DRIFT` | Candidate SHA changed during the review | Never a complete pass |
| `E6` | `UNVERIFIABLE` | Human-judgement claim that cannot be independently verified | Never a complete pass |

Grading rules:

1. `E1`, `E2`, and `E3` can never be graded PASS, individually or in aggregate.
2. `E4`, `E5`, and `E6` can never be declared a complete pass.
3. `E1` and `E2` may co-occur on the same declaration: a wrong current digest and a value absent from all history are two independent facts and both are recorded.
4. `E0` is assigned only after all six checks in section 4.7 hold and, where applicable, the section 5.6 envelope is complete.
5. A declaration that is both mismatched and unverifiable records `E1` plus `E6`; the mismatch is not downgraded to unverifiable.
6. `E5` voids the whole review, not just one declaration.

---

## 7. Final machine-readable result

### 7.1 Schema

Emitted as a JSON appendix to the evidence record.

```json
{
  "protocol": "Exact-Head Independent Review Protocol v1",
  "work_item": "AID-2026-269",
  "issue": 1278,
  "candidate_sha": "FULL_SHA",
  "candidate_tree_sha": "FULL_TREE_SHA",
  "review_complete": true,
  "declarations_checked": 0,
  "verified": 0,
  "failed": 0,
  "unverifiable": 0,
  "incomplete": 0,
  "findings": [],
  "overall_result": "FAIL"
}
```

### 7.2 Field rules

| Field | Type | Rule |
|---|---|---|
| `protocol` | string | Literal `Exact-Head Independent Review Protocol v1` (wire identifier; document revision v1.2) |
| `work_item` | string | Owning work-item ID |
| `issue` | integer | Issue number under review |
| `candidate_sha` | string | Full 40-char SHA supplied as input per section 3.1; never a ref expression |
| `candidate_tree_sha` | string | Full tree SHA from section 3.1 |
| `review_complete` | boolean | `true` only when every declaration has a terminal grade and no `E5` is open |
| `declarations_checked` | integer | Number of declaration fields actually processed |
| `verified` | integer | Count of `E0` — bucket `verified` |
| `failed` | integer | Count of `E1` + `E2` + `E3` — bucket `failed` |
| `unverifiable` | integer | Count of `E6` — bucket `unverifiable` |
| `incomplete` | integer | Count of `E4` + `E5` — bucket `incomplete` |
| `findings` | array | One object per non-`E0` declaration |
| `overall_result` | string | `PASS` \| `FAIL` \| `INCOMPLETE` |

The four counts are the only buckets, and every declaration lands in exactly one of them. `E6` and `E4`/`E5` are separate buckets because they are separate facts: `E6` means the claim cannot be machine-checked at all and human judgement is required, while `E4`/`E5` mean the machinery applied but the evidence or the lock was insufficient. Neither bucket may be folded into the other, and neither may be folded into `failed`.

| Bucket | Membership | Meaning for the verdict |
|---|---|---|
| `verified` | `E0` | The only bucket that can contribute to `PASS`. |
| `failed` | `E1`, `E2`, `E3` | Forces `overall_result: "FAIL"`. |
| `unverifiable` | `E6` | Blocks `PASS`; with no `failed` finding, verdict is `INCOMPLETE`. |
| `incomplete` | `E4`, `E5` | Blocks `PASS`; with no `failed` finding, verdict is `INCOMPLETE`. |

A declaration carrying grades from more than one bucket is counted once, in the bucket of its most severe grade, ordered `failed` > `incomplete` > `unverifiable` > `verified`; the co-occurring grades remain visible in `findings`.

Finding object:

```json
{
  "declaration_file": "PATH",
  "declaration_line": 0,
  "declaration_field": "FIELD",
  "declared_path": "PATH",
  "declared_sha256": "VALUE",
  "actual_blob_object_sha": "OBJECT_ID",
  "actual_sha256": "VALUE",
  "actual_bytes": 0,
  "candidate_sha": "FULL_SHA",
  "result": "MISMATCH",
  "grade": "E1",
  "declared": "VALUE",
  "actual": "VALUE",
  "note": "one-line justification"
}
```

Field rules for the finding object:

- `declared_path`, `declared_sha256`, `actual_blob_object_sha`, `actual_sha256`, `actual_bytes`, and `candidate_sha` carry the same values as the corresponding per-declaration record (section 4.6). For a `BLOB_IDENTITY` finding all six are mandatory. Where a declaration has no blob of its own (`COMMIT_IDENTITY`, `ATTRIBUTION`, `NON_MACHINE_ASSERTION`, and any finding whose evidence was never produced), the inapplicable fields are `null` rather than omitted, so the absence is explicit and distinguishable from an unrecorded value.
- `declared` and `actual` are short human-readable summaries only. They never replace the structured fields.
- `result` and `grade` are not interchangeable. `result` is the per-declaration outcome copied from the record: what the recomputation produced, one of `MATCH`, `MISMATCH`, `UNVERIFIABLE`. `grade` is the severity from section 6: what that outcome costs the review. Neither may be derived from the other alone.

| `result` | Permitted `grade` values | Reading |
|---|---|---|
| `MATCH` | `E0` | Declared value equals recomputed value, evidence trail intact. |
| `MATCH` | `E4` | Values agree but the evidence trail is invalid (text conversion before hashing, missing `command`/`exit_code`, working-tree read). The match is not accepted. |
| `MISMATCH` | `E1`, optionally with `E2`, `E4`, `E6` | Declared value differs from the recomputed value. |
| `UNVERIFIABLE` | `E6`, or `E4` when the cause is missing evidence rather than human judgement | No recomputation is possible or none was performed. |

`E3` and `E5` have no dedicated `result` value: they are review-level or attribution-level defects carried by `grade` and justified in `note`, while `result` records whatever the comparison itself produced.

### 7.3 Consistency requirements

1. Every count is produced by the actual run. Pre-filled, estimated, or templated counts are a protocol violation and the result is rejected.
2. `verified + failed + unverifiable + incomplete == declarations_checked`. Every declaration falls in exactly one bucket per section 7.2, so this identity holds by construction. A result that cannot satisfy it is malformed, not a case for an extra field.
3. No field outside the schema in section 7.1 may be added to reconcile counts. In particular, a free-form convention field that reassigns grades to buckets is a protocol violation and the result is rejected.
4. `len(findings) >= failed + unverifiable + incomplete`; every non-`E0` declaration has at least one finding.
5. `overall_result`:
   - `FAIL` if any finding is `E1`, `E2`, or `E3`;
   - `INCOMPLETE` if no `E1`/`E2`/`E3` exists but any `E4`, `E5`, or `E6` exists;
   - `PASS` only when `review_complete` is `true`, `failed == 0`, `unverifiable == 0`, `incomplete == 0`, and no `E4`/`E5` finding exists.
6. `review_complete` may be `true` while `overall_result` is `FAIL`. Completeness and verdict are independent axes.
7. `E5` forces `review_complete: false` and `overall_result: "INCOMPLETE"` for that run.

---

## 8. What this protocol does not establish

- It does not remediate. It produces findings; it does not fix manifests, prompts, INDEX entries, or historical records.
- It does not convert a `FAIL` finding into a work-item failure. A graded mismatch is evidence about a declaration, not a governance verdict on the work item, its author, or its acceptance status.
- It does not prove absence of defects beyond the stated envelope. Section 5.6 bounds every historical claim.
- It does not authorize changes to the reviewed artifacts, and it does not close the reviewed issue.
- It does not substitute for the independent L3 re-run. A result produced by the same session that authored the reviewed content is not an independent review.
- It does not certify that a declaration is true because a mechanism passed. A checker's `PASS` is a statement about the checker's coverage and inputs, and section 2.5 governs what an acceptance may claim.

---

## 9. Required-chapter mapping (R2-15)

| Required chapter | Section |
|---|---|
| Inputs (输入) | 3, metadata block 3.2 |
| Procedure (步骤) | 3.1, 4.1–4.3, 5.2–5.4 |
| Judgement (判定) | 1.3, 2, 4.7, 5.6 |
| Grading (分级) | 6 |
| Evidence structure (证据结构) | 4.6, 5.5, 5.6, 7 |

## 10. Reuse checklist

1. Lock head (section 3.1), record metadata block (section 3.2).
2. Enumerate tree (section 4.1), classify every declaration (section 1.3).
3. Recompute each blob byte-exactly (sections 4.2–4.7), emit one record per declaration.
4. For every historical claim, run sections 5.2–5.5 and write the envelope (section 5.6).
5. Assign grades (section 6), including co-occurrence rules.
6. Emit JSON (section 7), reconcile counts (section 7.3).
7. Append JSON to evidence; link the evidence file and the final commit SHA in the issue comment.

---

## 11. Revision history

| Version | Date | Change |
|---|---|---|
| v1 | 2026-11-27 | Initial protocol. |
| v1.1 | 2026-11-27 | Applied the independent review's D-2, D-5, D-6, D-7: added the `incomplete` bucket (`E4` + `E5`), defined bucket membership, and restated the count identity as `verified + failed + unverifiable + incomplete == declarations_checked`; added `command` and `exit_code` to the per-declaration and per-version records, with an empty command or missing exit code graded `E4`; added the seven structured finding fields and the `result` / `grade` mapping; added the explicit prohibition on substituting `base_sha`, `origin/main`, or `HEAD` for `CANDIDATE_SHA`, graded `E4` (plus `E5` on drift). |
| v1.2 | 2026-11-27 | Reframed as the judgement layer above automated checkers: added the division-of-labour section (#1426 blob-pin field discovery, #1451 blob-pin integrity verification, #1449 negative-sample/base-binding) and re-classified the blob-recomputation and historical-verification sections as reference procedures, normative only where no checker covers the case; named-head rule adopted — a head is a named observation bound to a commit SHA, a later head is appended rather than merged, and a mechanism's `PASS` is a statement about the mechanism, never about the truth of a declaration. |
