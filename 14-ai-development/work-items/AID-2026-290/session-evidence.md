# Session Evidence — AID-2026-290

## Session role / use case

Implementation and validation session for Issue #265 AC6, assigned as AID-2026-290. The task is to add a read-only prompt-to-implementation trace checker, regression tests, a ratchet baseline, and a required GitHub Actions gate. Repository mutations in this session were performed through the GitHub API connector; no local repository execution is claimed.

## Actual AI input

The user supplied R3 requiring:
- support both nested `implementation.implementation_commit_sha` and legacy top-level `implementation_commit_sha`;
- prefer `implementation.merge_commit_sha` as the reachability target, otherwise compare against `--base` / `origin/main`;
- treat either `prompt_file_blob_sha` or `prompt_file_commit_sha` as an independent immutable pin, validating both when both exist;
- use five primary statuses in the fixed order `NO_TRACE`, `DIGEST_UNPINNED`, `DIGEST_MISMATCH`, `COMMIT_UNREACHABLE`, `TRACEABLE`;
- default `--commit` to `origin/main`, require a real ratchet baseline, add the nine named manifest assertions, run Actions, and do not inspect branch protection.

## AI-visible output

The session updated `scripts/ci/check_prompt_commit_trace.py`, added `scripts/ci/test_check_prompt_commit_trace.py`, and added the `Prompt-to-commit trace (ratchet)` job to `.github/workflows/gates.yml`. The job ran on PR #1427 at head `75a144e78c3d7a1590b509019deefaa2bcdac17b`. Its regression-test step completed successfully, and the main/PR snapshot artifact was uploaded. The final ratchet step failed closed because the committed baseline file is not yet present.

The same Actions run also exposed unrelated failures in the existing `Schema non-empty audit (hard gate)` job's REQ-01 assessment signature step and the `Session Evidence` job. The workflow run was not a merge approval.

A semantic conflict remains in the supplied R3 acceptance criteria: AID-2026-047 has no immutable prompt pin fields in its current main manifest, while R3 both requires every unpinned HEAD_MATCH case to be `DIGEST_UNPINNED` and lists AID-2026-047 as the unique `TRACEABLE` manifest. The implementation follows the explicit five-state definition and tests AID-2026-047 as `DIGEST_UNPINNED`; no exception is fabricated.

No merge, Owner acceptance, baseline ratification, or Issue #265 closeout comment is claimed.
