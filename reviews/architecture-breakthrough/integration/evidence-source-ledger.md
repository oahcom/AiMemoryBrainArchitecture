# ABR-INTEGRATION-001 — Evidence & Source Ledger

## Baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Default branch: `main`
- Current main HEAD verified by compare: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Main system overview path: `01-system-architecture/system-overview.md`
- System overview Blob SHA read from main: `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256`
- `b3c666e67982cb3d3374e759cfb6552c7765aacb` to current main: 2 commits, 0 file changes (history-only difference in compare output).

## Research PR pins

| PR | Branch | Head SHA | Base SHA | Key report path | Report Blob SHA |
|---|---|---|---|---|---|
| #84 | `research/architecture-breakthrough-session-0-2026-11-18` | `c6e76b34cbf099d36631b284c9b8a75d778d707f` | `28fb37e21fa4ba2b871f7816fe669128618c063e` | `reviews/architecture-breakthrough/architecture-breakthrough-overview-zh-CN.md` | Read-back performed; exact Blob SHA to be appended after final pin |
| #88 | `review/forget-formal-verification-2026-11-18` | `bf35b32295d0d3f337c80c3dc406db0a41de6830` | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | `reviews/architecture-breakthrough/forget-formal-verification/forget-formal-verification-zh-CN.md` | `ea05c23da95ce926cd8ae4f645e5d5b5cc1097c4` |
| #86 | `research/memory-operating-system-architecture-2026-11-18` | `3892916ce2379f807a0ddcd0039816f6e88ecee1` | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | `reviews/architecture-breakthrough/memory-operating-system/memory-operating-system-zh-CN.md` | `2e5b50d6fdf181e7f87749349f450443a703c9eb` |
| #85 | `research/memory-ir-compiler-session-c-2026-11-18` | `c5013d3585d54457f38bef37984645e2055ff7cf` | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | `reviews/architecture-breakthrough/memory-ir-compiler/memory-ir-compiler-zh-CN.md` | `181652a431fd84429981825dbd63ca1b95468101` |

## Reproducible source checks

- PR metadata: GitHub PRs #84, #85, #86, #88.
- Ref topology: compare each PR head against `main` and against the cited historical base.
- Current main: compare `e52594f...` to `main` (identical).
- Historical content delta: compare `b3c666e...` to `e52594f...` (zero changed files).
- Main architecture overview: fetch `01-system-architecture/system-overview.md` at `main`.
- A bounded model command is documented in PR #88; B and C prototype commands are documented in their respective research PRs.

## Evidence caveats

- PR metadata and report self-declared baselines are separate facts; never normalize one into the other.
- Source pins inside research reports are historical snapshots, not automatically current Owner HEADs.
- The full Issue #43 integration scope remains broader than this A/B/C breakthrough review.
- This ledger records exact evidence read in this integration session; missing pins must remain explicitly missing rather than inferred.
