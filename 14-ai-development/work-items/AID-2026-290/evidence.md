# Evidence — AID-2026-290

## Source and implementation

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Assigned issue: #265 (AC6)
- Branch: `feat/aid-290-prompt-commit-trace`
- First PR validation head: `75a144e78c3d7a1590b509019deefaa2bcdac17b`
- Pull request: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1427

## GitHub Actions execution

- Workflow run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45950054911
- New checker regression tests: SUCCESS
- Main and PR snapshot generation: SUCCESS
- Snapshot artifact: https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/artifacts/15176112717/zip
- Ratchet enforcement: FAILURE, intentionally fail-closed because the reviewed committed baseline has not yet been added.
- The run's full check-runs collection contained 18 runs; this is not evidence that all 18 are required contexts.
- Existing unrelated failures in this run: REQ-01 assessment signature step in Schema non-empty audit, and Session Evidence. Other jobs were still running when the run was inspected.

## Interpretation and limitations

The regression-test step passed on the first PR head. It covers fixed decision precedence and the nine named manifest cases, with AID-2026-047 following the five-state rule as `DIGEST_UNPINNED` because its current manifest has no immutable prompt pin. This differs from the separate requested expectation that it be `TRACEABLE`; see the session evidence for the exact contradiction.

The snapshot artifact contains the machine-generated per-manifest baseline candidate and PR matrix. It has not been reviewed or committed as the ratchet baseline. The prior pin `756e1e25` is historical context only and is not represented as a new Actions result.

No claim is made that the required 16 contexts passed, that the PR is merge-ready, or that a merge occurred. Blob verification against a merge SHA and the #265 closeout comment remain pending.
