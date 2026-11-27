# Evidence — AID-2026-291

## Source and implementation

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Assigned issue: #265 (AC6)
- Branch: `feat/aid-290-prompt-commit-trace`
- PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1427
- Baseline main SHA at synchronization: `056209b71c2e559efa3526a31870187a8e6e47f2`
- Prior branch head retained as a merge parent: `417c2e4b573eaee51ee9383f9498ccfc25c53c6b`

## Actions evidence

- The earlier run at `417c2e4b573eaee51ee9383f9498ccfc25c53c6b` passed the checker regression tests and snapshot generation, uploaded its snapshot artifact, and failed closed at ratchet enforcement because the baseline file was absent.
- Earlier run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45950219615
- The earlier run is stale-base evidence only; the final synchronized head must be validated again.
- The baseline file is intended to be generated from the Actions main snapshot, reviewed, and committed at `14-ai-development/work-items/AID-2026-291/baseline.json`. Its `commit` field must equal the exact main SHA used for the scan.
- No required-context success, final five-state count, final matrix, merge, or post-merge blob verification is claimed in this preliminary evidence.

## R4 adjudication

AID-2026-047 has no `prompt_file_blob_sha` or `prompt_file_commit_sha` in its current main manifest. Its prompt bytes match HEAD, and its implementation commit is reachable. It is therefore `DIGEST_UNPINNED`, prompt dimension `HEAD_MATCH`, commit dimension `REACHABLE`; findings include `digest_unpinned` and exclude `digest_head_mismatch`. It is not promoted to TRACEABLE and no manifest pin is added. The expected TRACEABLE count on the baseline main snapshot is zero.

## Scope constraints

No change is made to the existing Schema non-empty audit job, token permissions, unrelated jobs, branch protection, or Issue #265 body. The #265 closeout comment is deferred until exact-Head checks, merge, and per-file blob verification are complete.
