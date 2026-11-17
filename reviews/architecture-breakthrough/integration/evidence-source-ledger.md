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
| #84 | `research/architecture-breakthrough-session-0-2026-11-18` | `c6e76b34cbf099d36631b284c9b8a75d778d707f` | `28fb37e21fa4ba2b871f7816fe669128618c063e` | `reviews/architecture-breakthrough/architecture-breakthrough-overview-zh-CN.md` | `c31726f6414eeb87a9447ab7154d26743f75d5f3` |
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


## Live Owner branch refresh — ABR-INTEGRATION-002 (2026-11-18)

Current main: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`; tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`.

| Owner | Branch | HEAD | Selected source Blob pins |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | ADR-001 Fact/Claim `df77e4a93cb8fef689ae7c828888d960cbf381d6` |
| C | `session-c-agent-integration-2026-11-16` | `88992da30331121b81cf2773acab11d921daf281` | CSubmitOutcome 1.0.1 `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; Phase 3.8.23 `4860c627b4d7e84e23fb39ad83411674f3b88c7b`; workflow `a1f0b8f884f0f294fb3ec96da7c4f11e294e5142` |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Forget gate `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Derived registration `00e37ba56596e710513c8d0568acd79141d9101b` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | Forget suppression `ce59252dbbdc5d10d016704797e9ba12d5a941bd` |
| G | `session-g-memory-context` | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | Applied contract EN `bd297873bc1e593280484a43cb44b56058d9c4ff`; ZH `82553a47fae2d5e796e0742b46231afe465e75b2` |
| H | `session-h-bmcp-protocol` | `6608cde89d959257db612d8ff8080f631333f3f3` | Applied schema `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`; validator `2f6de24eea737cf75a16ead7495bea4627bb1bb4`; H 3.8.24 report `f193113f142506b0d0848c7131f780db93a83aef` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | Global inventory `9100061fa986fb6676656169de3fcf9fc1c72664`; PermissionEpoch `bae6a24fe3a374bc816993979a8fa9af52517dea`; Commit Authorization proposal `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | Producer/Dependency/Visibility `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`; topology ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`; restore high-water `4f656163aeba532a441eaed1d293a48e2363cb4a` |

## H/C branch integrity incident recovery

- H pre-incident `0d36324457e39bd50ad56ae902d477c4ea765b61` → destructive `0277a8b9ee63be850acc0b8b1b08625524aaa33b` (205 removed) → restoration `1ca07ed575be1fb2a690e3c2e110a89880ea6454` → current `6608cde89d959257db612d8ff8080f631333f3f3`. Pre-incident to current compare: 7 ahead, 0 behind, 8 added, 0 removed/modified/renamed.
- C pre-incident `71047cdb51139ca4080ac67f451e38a48698859d` → destructive `a5dff993e5c2928a28deb777c41023cfe923366f` (133 removed) → restoration/current `88992da30331121b81cf2773acab11d921daf281`. Pre-incident to current compare: 2 ahead, 0 behind, 2 added, 0 removed/modified/renamed.

## Exact CI runs

- H Applied Delivery Evidence Conformance: run `44130722532`, SUCCESS, tested commit `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`; report lists 11 tests.
- H Recovery Cutoff Conformance: run `44130905292`, SUCCESS, tested current H HEAD `6608cde...`.
- H Provider Outcome Conformance: run `44129938964`, SUCCESS, tested H restoration commit `1ca07ed...`.
- C Provider Outcome Conformance: run `44129914790`, SUCCESS, tested current C HEAD `88992da...`.

## Workflow trigger follow-up

- Current C workflow Blob `a1f0b8f884f0f294fb3ec96da7c4f11e294e5142` omits the 1.0.1 schema path from push.paths.
- PR #94 adds `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json`; PR remains Draft and trigger behavior for a schema-only push is not yet verified.

## Applied Delivery Evidence 1.0.0 exact pins

- H identity review: `08-bmcp-protocol/phase-3.8.23-h-exact-review-g-applied-delivery-evidence-mapping.md`, Blob `be308261c3e000e712a3cdbd3dbf60507156127b`.
- H candidate report: `08-bmcp-protocol/phase-3.8.24-h-applied-delivery-evidence-1.0.0-schema-validator-candidate.md`, Blob `f193113f142506b0d0848c7131f780db93a83aef`.
- H schema: `08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json`, Blob `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`.
- H validator: `08-bmcp-protocol/validators/applied_delivery_evidence_validator.py`, Blob `2f6de24eea737cf75a16ead7495bea4627bb1bb4`.
- H tests: `08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py`, Blob `bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5`.
- H workflow: `.github/workflows/h-applied-delivery-evidence-conformance.yml`, Blob `7bd9bf3a4141d1e239d0f165e2e98fdd25961254`.
- C exact identity review: `07-agent-integration/phase-3.8.23-c-exact-review-g-applied-persistence-identity.md`, Blob `4860c627b4d7e84e23fb39ad83411674f3b88c7b`; this does not accept the new H 1.0.0 wire mapping.
- No exact G or C consumer acceptance of H 1.0.0 was found in current Owner trees.


## ABR-INTEGRATION-003 — Cross-owner Forget model and CI pins

- Model: `reviews/architecture-breakthrough/integration/model/forget_cross_owner_model.py`, Blob `d45807b0b165e53aa6e92d211c221cc93b46ca60`.
- Regression tests: `reviews/architecture-breakthrough/integration/model/test_forget_cross_owner_model.py`, Blob `64ee823eb1d3d81e020e73ef97817208326f42b5`.
- Bounded model README: `reviews/architecture-breakthrough/integration/model/README.md`, Blob `c7dc620b3486e496de1792147cbf441a51cb3af0`.
- Branch-only workflow: `.github/workflows/abr-forget-cross-owner-model.yml`, Blob `31304a8718c464065ae735d35f5120edee418217`.
- GitHub Actions run: `44136327645`, SUCCESS; tested commit `89a680bbad7246952d51c61c137b0c3611f52a06`.
- Result: 27,472 state/depth pairs through depth 14; 11 weakened-guard mutants; model command and unittest suite passed.
- Model result is bounded logical evidence only; it is not TLC, unbounded proof, or physical/production evidence.
