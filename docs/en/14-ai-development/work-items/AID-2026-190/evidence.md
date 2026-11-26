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
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the measured before/after verdicts of the two gates on a GBK console, the added tests and the files whose encoding the run showed to be necessary; claims no CI result and no independent review."
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
    canonical_scope: "AID-2026-190 locale-independent Git output decoding in the documentation and bilingual gates"
    canonical_scope_id: "ai-development/aid-2026-190-git-output-decode-locale"
    canonical_scope_keywords:
      - git-output-decoding
      - locale
      - gbk
      - dm-10
      - fail-closed
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-190/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-190/evidence.md"
---
# AID-2026-190 — Gates that read Git output treated a decode failure as a content finding

- Work item: AID-2026-190; id_status: PROVISIONAL.
- Attribution: user-authorized operator (delegated by account owner); date: 2026-11-27.
- base_commit_sha: `4326669caa6c43193d34219a0451b80762b712ff` (the `origin/main` the branch was cut from).
- Conclusion first: `subprocess(text=True)` decodes Git output with the console's locale codec. On a GBK console the decode failed, `stdout` became `None`, and the caller read "I could not decode this" as "this does not exist". After the change the GBK console and a UTF-8 environment reach the same verdict.
- This record claims no CI result, no independent review and no Owner acceptance.

## 1. What was observed

### 1.1 Root cause

`git()` in `check_document_management.py` and `_git_log_output()` in `check_bilingual_docs.py` both read Git output with `subprocess.run(..., text=True)`. The codec behind `text=True` is the **locale** codec: UTF-8 on CI, GBK on a default Windows console (code page 936). When GBK cannot decode a UTF-8 document, `subprocess`'s reader thread raises `UnicodeDecodeError` and the main thread is handed `stdout = None`. The caller then read `None` as "this Git command produced no output", which it translated into "this file does not exist at that commit" — a piece of history that was never read, asserted as a certainty.

The same defect is a crash rather than a misreading in `check_bilingual_docs.py`: the AID-173 worker's `git show` raised `UnicodeDecodeError` on GBK and `_embedded_sources_in_revision()` fed `None` straight into `ast.parse`.

### 1.2 Measured (same tree, same machine)

`git cat-file -e <pin>:<path>` reports all nine files named by the nine DM-10 errors as present. That matches the defect report.

| Tree | Console | Exit | `DM-10 … did not exist` | `UnicodeDecodeError: 'gbk'` | Final verdict |
|---|---|---|---|---|---|
| `main` @ `4326669c` | code page 936, no `PYTHONUTF8` | **1** | **9** | **9** | `FAIL: 9 error(s)` |
| `main` @ `4326669c` | `PYTHONUTF8=1` | 2 | 0 | 0 | `INCOMPLETE` (496 classified / 446 unclassified) |
| this branch (fixed) | code page 936, no `PYTHONUTF8` | 2 | 0 | 0 | `INCOMPLETE` (496 / 446) |

Comparing rows two and three line by line: the verdict lines, the count lines and `DM-10 out-of-scope stale bindings: 0` are identical. The only difference is how the advisory section echoes body `- Status:` values through the console, and `main` already shows the same kind of difference between its own GBK and UTF-8 runs. In other words: before the change the GBK console produced nine extra errors and nine crashes relative to CI; after it, the two agree.

## 2. What changed

### 2.1 `scripts/check_bilingual_docs.py` (the decoding primitive and the entry point)

1. Added `GIT_TEXT_ENCODING = "utf-8"`, `GitOutputDecodeError(RuntimeError)` and `decode_git_output(raw, what)`: strict UTF-8 decoding that raises an exception whose message contains `decode` and no wording that sounds like "absent" or a content finding.
2. `_git_log_output()` now captures bytes with `capture_output=True` and hands them to `decode_git_output()`, **not** `text=True`.
3. The six remaining Git reads (`rev-parse --is-shallow-repository`, `git status --porcelain`, `git diff --name-status` twice, `rev-parse --verify <rev>:<path>`) take `encoding="utf-8", errors="replace"`.
4. `main()` catches the `GitOutputDecodeError` raised by registration-history verification, prints `::error::` and returns **2** (INCOMPLETE), instead of letting it crash or degrading it to a content verdict (1).

### 2.2 `scripts/check_document_management.py` (the DM-10 read path)

1. `git()` captures bytes and decodes them with `decode_git_output()`. A spawn failure still returns `None` (the contract T92a pins is unchanged), but a **decode failure no longer returns `None`**: it raises `GitOutputDecodeError`.
2. DM-10's two reads (`rev-parse --verify <pin>^{commit}` and `git show <commit>:<rel>`) each catch that exception and append to the existing `unanswerable` channel, so the run prints `INCOMPLETE` and returns **2**.
3. `None` / empty output no longer means "absent" by itself: `git cat-file -s <commit>:<rel>` is asked first.
   - Object absent → the original `did not exist at approved_version` finding stands (exit 1; the assertion is still available).
   - Object present but unreadable (`None`, or an empty string whose byte count is not zero) → recorded as unanswerable (exit 2), with a message that names a decode/read failure rather than pretending the file was absent.
   - Object present and genuinely zero bytes → an empty file is a real, readable version and takes part in the hash as empty text (unchanged behaviour).
4. A decode failure in `changed_paths()` or in the `is_git` probe also becomes `::error::` plus exit 2, instead of landing in the "does not resolve to a commit" branch (exit 1).

### 2.3 The other gates that read Git output

`check_bilingual_docs_full.py` (an undecodable `git ls-files -z` stream prints `git output decode failed` and exits 2), `check_fmt.py`, `check_policy_inheritance.py`, `check_source_revision_pointers.py`, `check_traceability.py`, `ci/check_branch_freshness.py`, `governance/evidence/check-evidence-tiering.py` (which had `errors="replace"` but no `encoding`, so it was still decoding with the locale) and the Python embedded in `governance/bilingual/check-bilingual-tiering.sh`: all take `encoding="utf-8", errors="replace"`.

`scripts/governance/status_migration/check_status_gates.py` is a sidecar-anchored protected file (`PR272-evidence-hardening.sha256`). Its `git log --format=%B` reads this repository's commit messages, which contain Chinese, and it failed the same way on GBK: `test_status_migration.py` produced 28 `UnicodeDecodeError` errors before the fix. The sidecar was regenerated through the mechanism that file documents, and the new sidecar's SHA-256 (`06ea8d36581b0eeea60c93dbd4a3b8dec216bde2839fe6ba8f6cb7a123389c17`) is recorded in the commit message. That is the auditable path it prescribes, not a bypass.

### 2.4 Tests

1. `scripts/test_check_document_management.py` gains `run_git_decode_locale()`:
   - **T95a**: make the approved version a non-UTF-8 blob → assert exit 2, output contains `decode`, and does **not** contain `did not exist`;
   - **T95b**: the counterfactual — the pinned commit genuinely lacks the file → assert exit 1 and that the message is still `DM-10 … did not exist at approved_version`. Without this case, "a decode failure no longer claims absence" could degrade into "neither case speaks".
2. `scripts/test_check_bilingual_docs.py` gains two cases: a non-UTF-8 blob through `_git_log_output()` raises `GitOutputDecodeError` (message contains `decode`, not `not exist`), and `main()` reports it as exit 2 rather than 1 or a traceback.
3. The fixture Git helpers of the affected self-checks (`test_check_line_endings`, `test_check_repository_hygiene`, `test_check_traceability`, `test_check_fmt`, `ci/test_check_branch_freshness`, `governance/bilingual/test_bilingual_scripts`, `governance/evidence/test_gate_normative_roots`, `governance/status_migration/test_status_migration`) decode as UTF-8, so those self-checks no longer need `PYTHONUTF8` on a GBK console either.

## 3. Why this changes no gate's pass condition

- **Same verdict**: replacing the locale codec with explicit UTF-8 moves the behaviour CI (UTF-8) already had onto the local machine. Rows two and three of the table in section 1 are identical line by line.
- **The failure direction is stricter, not looser**: a decode failure moves from "exit 1, a definitive error" or "a crash" to "exit 2, INCOMPLETE". The `document-management.yml` workflow treats 2 and 1 alike as a red check (only exit 3 is special-cased), so the merge bar is not lowered.
- **The one new failure surface**: Git output that genuinely is not UTF-8. Before, that case was a misreading/crash on GBK and a crash on UTF-8; after, it is "report the decode failure and stop" on any environment. That is not a new rule, it is stating a pre-existing uncertainty.
- **Untouched**: DM-10's stale-approval semantics, the contents of either bilingual baseline, `current_bilingual_gaps()`, any threshold, any workflow.

## 4. Local verification (Windows, code page 936, `PYTHONUTF8` unset)

| Command | Result |
|---|---|
| `python scripts/check_document_management.py` (`main` @ `4326669c`) | exit 1, `FAIL: 9 error(s)`, nine `did not exist` findings, nine GBK decode exceptions |
| `python scripts/check_document_management.py` (this branch) | exit 2, zero `did not exist`, zero decode exceptions, `INCOMPLETE` (496 / 446) |
| `python scripts/test_check_document_management.py` | `329/329 passed`, one registered skip (`T68c`) |
| `python scripts/test_check_bilingual_docs.py` | 17 tests OK (the earlier 15 plus 2) |
| `python scripts/check_bilingual_docs.py` (`BASE_SHA=origin/main`, `HEAD_SHA=this branch`) | recorded in section 6 |
| `python scripts/test_check_line_endings.py` | 17 tests OK |
| `python scripts/test_check_repository_hygiene.py` | 97 tests OK (1 skip) |
| `python scripts/test_check_traceability.py` | 41 tests OK |
| `python scripts/ci/test_check_branch_freshness.py` | 9/9 passed |
| `python -m scripts.governance.evidence.test_gate_normative_roots` | 52 tests OK |
| `python -m scripts.governance.evidence.test_evidence_tiering` | 67 tests OK |
| `python scripts/governance/status_migration/test_status_migration.py` | 26/27 OK. The remaining case, `test_sidecar_anchor_detects_silent_tampering`, **fails on this machine before this change as well**: it hashes the working-tree bytes of the sidecar, while a Windows checkout materialises CRLF where the committed blob is LF. The same single case fails when run against the `main` tree. The real anchor was checked directly: `_verify_sidecar_anchor(repo)` returns `True` (blob SHA-256 equals the `06ea8d36…` in the commit message) |
| `python -m pytest tests/test_check_bilingual_docs_full.py` | 7 passed |
| `python scripts/test_check_fmt.py` | 3 failures, **unrelated to this change**: the fixture fakes `cargo` with a shell script, which Windows refuses to execute (`WinError 193`). The same three fail with the `HEAD` copy of `check_fmt.py` |

## 5. What was not done

- No gate's pass condition, threshold, baseline content or workflow was changed; no required context was added.
- DM-10's stale-approval semantics and `current_bilingual_gaps()` were not touched.
- `text=True` calls unrelated to this defect (for example reading the stdout of `python`/`cargo` subprocesses) were left alone: their output is not Git output and is outside this Work Item.
- No independent review was performed (`review.status = NOT_ASSIGNED`); no Issue was closed or modified.

## 6. `check_bilingual_docs.py` measured (range `4326669c...f85257df`)

Code page 936, `PYTHONUTF8` unset, `BASE_SHA=4326669c…`, `HEAD_SHA=f85257df…`, `PR_BODY` containing `BILINGUAL-MANIFEST: COMPLETE`:

| Script version | Exit | Result |
|---|---|---|
| before (the `check_bilingual_docs.py` of `4326669c`, i.e. `main`) | 1 | `AttributeError: 'NoneType' object has no attribute 'strip'`, raised from `_embedded_sources_in_revision()` via `_git_log_output()`: the failed `git show` decode left `stdout` as `None`, and `.strip()` crashed on it. This is the same site the AID-173 worker hit |
| after | 0 | `bilingual baseline: 77 frozen, 0 new gaps`; `exemptions: 21`; `PASS (29 changed paths inspected)`; plus `NOTE: 2 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked` |

The bytes this gate reads over the same range are unchanged, so its verdict on CI is unchanged; what differed before was only the local decoder.
