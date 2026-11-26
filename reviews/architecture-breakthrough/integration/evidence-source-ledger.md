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


## Independent A review evidence pins — ABR-AUDIT-007 / PR #100

- A source audit report: `reviews/architecture-authority/2026-11-18/ABR-INTEGRATION-SOURCE-AUDIT-007.en.md`, Blob `2bbe3e0a7ba237c082764e7ec9a4b73bd7f73afc`.
- PR #100 disposition: APPROVED_WITH_CONDITIONS for research integration accuracy only; not architecture approval.
- PR #86 RM prototype: `memory-operating-system/prototype.py`, Blob `72b9f493b58cb42791c39cde5a78f2163235002e`.
- PR #86 exact benchmark report: `prototype-and-benchmarks.md`, Blob `2053e4de179c80878fbdeee4f4874de5ad04057c`.
- Exact median latency: Direct Top-K 0.095 ms; Rerank + Budget 0.119 ms; Unified RM 0.306 ms. Single-threaded local Python microbenchmark, not service latency.
- PR #85 IR prototype: `prototype/memory_ir_prototype.py`, Blob `bd27e93e90aceacf1857ebdf56b97e59ae34eb32`.
- PR #85 synthetic fixture: `prototype/sample_experiences.json`, Blob `657268696ed95a481bf2836e9750fd59183d83e3`.
- PR #85 prototype README: Blob `f2a293a084942cbc77b7f9025b6e4d442757a56d`.
- PR #85 Direct-vs-IR report: Blob `087212cb9713d37d91fce8943efaf6d80249b87c`.
- PR #88 Python bounded model: `forget-formal-verification/model/forget_model.py`, Blob `8e75f2978a0b85b3f0311ac0a189d40125b8d461`.
- PR #88 F1–F8 invariants: Blob `14eb422c4ac7763d4682adacacd50b42b34fda6c`.
- PR #88 model results: Blob `2082e4a547dbe76c319d58bdd75022ccc532b6e2`.
- PR #88 state machine: Blob `4868832dab421f6d76caf4d3366da68e960abe99`.
- PR #88 counterexample catalog: Blob `254ab3c7c467ab9acfcae88ffe1dc92d1045e3aa`.
- PR #88 remediation proposals: Blob `9baef6654783182dc825f34a6d35426286541a66`.
- PR #84 TLA+ skeleton: `forget-model/ForgetModel.tla`, Blob `8b069efcafaf0d7ab7e42f3c4953ad3f4836cb29`.
- PR #84 TLC config: `forget-model/ForgetModel.cfg`, Blob `0e6e1bf9321a22afd856a4592efb3d23146d0119`.

## A exact H Applied review — PR #98

- Report: `reviews/architecture-authority/2026-11-18/H-APPLIED-DELIVERY-EVIDENCE-006.en.md`, Blob `44f79fc037a3aa15d171781fecf5a924e10a0388`.
- Disposition: DEFERRED — CANDIDATE IMPLEMENTATION WITH OPEN P0 CONDITIONS.
- H-ADE-001: duplicate top-level/nested JSON object keys are not rejected before standard JSON object materialization.
- H-ADE-002: CSubmitOutcome 1.0.1 semantic/identity/final-boundary/digest join is not explicit in H validator contract.
- H-ADE-003: current I authorization/PermissionEpoch, key status, audience/scope and D Forget fence must be rechecked before SAME_DIGEST_REPLAY returns original result ref.
- H schema/validator/test/workflow and H Phase 3.8.24 exact Blobs remain as listed in prior ledger section.

## C/I gateway-attestation order reviews — exact scope distinction

- C Phase 3.8.27: `07-agent-integration/phase-3.8.27-c-rereview-h-gateway-attestation-ordering.md`, Blob `3ca06dbfd7d59483e9604b7a68df924c719f60aa`.
- I Phase 3.8.23: `09-security-governance/phase-3.8.23-i-rereview-h-gateway-attestation-replay-acceptance-order.md` (not restored on main; see AID-2026-107 §10), Blob `85cdbad04ae4b688338cdf2b667c21d2f02d8b96`.
- These delegated role reviews accept C verification before H Unified 1.2.15 Gateway Attestation signing and the durable replay order. They do **not** accept the separate H Applied Delivery Evidence 1.0.0 message family.

## Storage Option A ADR status — exact supersession evidence

- Option A topology ADR: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`, Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`.
- §3 contains pre-addendum “no option selected” text; §8.6 explicitly marks that historical status superseded and states L1 is closed by the ADR with Option A selected as the normative v1 logical topology.
- Storage v3.3.2 exact-version manifest: `reviews/storage-consistency/phase-3.6.22-storage-v3.3.2-option-a-status-corrected-exact-version-manifest.md`, Blob `5c614375e10698e4931d83deb57d20321445e068`; its scope says it corrects Option A status to match the exact ADR, while the bundle remains NOT JOINTLY ACCEPTED / NOT FROZEN and L4 remains open.
- A PR #102 reports an L1 contradiction; this integration review disputes that interpretation because the exact ADR contains an explicit §8.6 supersession. Owner/A reconciliation requested.
- Direct commit metadata fetch for E HEAD `ee098e14747d9915de5b3efb63b3a8dd77f670ed` succeeded in this pass; returned tree `59d99c828c91bfdb28fc1ca353f1db38ae85c35e`, message “E: review per-authority Storage serialization anchor”. A PR #102's E lookup anomaly did not reproduce.

## B dual ADR source pins

- `02-domain-model/ADR-001-fact-claim-semantics.md`, Blob `a1024938ff5baba069cf128c69496a44e143330c`.
- `02-domain-model/adr/ADR-001-fact-claim-canonical-model.md`, Blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`.
- Both remain ADR-BLOCKED; the branch contains two related exact source artifacts and neither records a formal approving authority or approved option.

## Current integration branch audit responses

- ABR-AUDIT-007 / PR #100: exact RM latency correction applied; model/prototype/fixture Blob pins added; bounded-vs-production evidence classes retained.
- A-H-ADE-006 / PR #98: H-ADE-001..003 integrated; additional `integrity_proof_ref` P0 binding question tracked separately as an integration candidate finding.
- A-OWNER-SOURCE-REFRESH-004 / PR #102: Storage ADR §8.6 supersession and E commit metadata fetch rechecked; two findings require A/Storage reconciliation rather than silent adoption.


## ABR-INTEGRATION-005 — Forget cross-owner model audit

- Reviewed model: `reviews/architecture-breakthrough/integration/model/forget_cross_owner_model.py`, Blob `d45807b0b165e53aa6e92d211c221cc93b46ca60`.
- Regression test: `reviews/architecture-breakthrough/integration/model/test_forget_cross_owner_model.py`, Blob `64ee823eb1d3d81e020e73ef97817208326f42b5`.
- README: `reviews/architecture-breakthrough/integration/model/README.md`, Blob `c7dc620b3486e496de1792147cbf441a51cb3af0`.
- Historical model CI: run `44136327645`, SUCCESS at `89a680bbad7246952d51c61c137b0c3611f52a06`; 27,472 state/depth pairs through depth 14, 11 mutants. Not evidence that later ABR-INTEGRATION-005 documents were tested.
- D source: `03-memory-brain/forget-fence-operation-and-publication-gate.md`, branch `session-d-memory-brain-2026-11-16`, Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`.
- I source: `09-security-governance/global-forget-target-inventory-and-completion-evidence.md`, branch `session-i-security-governance-2026-11-16`, Blob `9100061fa986fb6676656169de3fcf9fc1c72664`.
- Storage source: `reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md`, branch `session-storage-consistency-forget-atomicity-2026-11-16`, Blob `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`.
- New bilingual audit:
  - `reviews/architecture-breakthrough/integration/forget-cross-owner-model-audit-zh-CN.md`, commit `9f3f84b11c51ed6257c098cccffa157db662af9a`.
  - `reviews/architecture-breakthrough/integration/forget-cross-owner-model-audit-en.md`, commit `c89900275ffacbddac76354bb8cd583e8f944918`.
- Findings: M-01 global_complete overclaims relative to I Completed; M-02 no normal terminal proof path for registered-but-never-started work; M-03 only one Fence generation modeled; M-04 physical crash cut points remain unmodeled; M-05 liveness/fairness must be separated from safety.
- Disposition: bounded research model accepted with conditions; global Forget and JF-10 remain NOT PROVEN.


### M-02 source refinement — E pre-execution terminal candidate

- E current source: `04-memory-compiler/forget-fence-and-derived-registration.md`, branch `session-e-memory-compiler-2026-11-16`, Blob `00e37ba56596e710513c8d0568acd79141d9101b`.
- E source status: CANDIDATE E enforcement contract; D/E/Storage atomic registration and final publication gate OPEN/BLOCKING.
- E §3.2 has Cancelled/Rejected durable terminal disposition and no-publication semantics; E §7 Producer terminal acknowledgement remains OPEN (D response schema + reconciliation semantics).
- Refined M-02: the semantic candidate exists, but exact E→D terminal receipt mapping, pre-execution cancellation authority, idempotency, late-worker fencing and D barrier-ledger linearization remain OPEN; integration model has no corresponding transition.


### M-02 regression test added (CI not yet observed)

- Updated test: `reviews/architecture-breakthrough/integration/model/test_forget_cross_owner_model.py`, Blob `434cd370350f2091151a93b6440651f61d8a03e7`, commit `8d7d5a50b45d2137cb3816a21c15bd5760ffc5fd`.
- New test: `test_registered_fenced_never_started_has_no_pre_execution_terminal_transition`.
- It records the exact bounded-model gap: after register + install_fence, the current action set has no cancel_before_execution transition; terminalize, resolve_no_publication and close_barrier are not legal from that state.
- The historical CI list currently shows only runs `44136327645` and `44136537336`, neither tests commit `8d7d5a5...`. The new regression test is committed but **CI execution is not yet observed**; do not report it as passing.


## ABR-INTEGRATION-005 current-model correction and verified CI

The current cross-owner model revision supersedes earlier M-01/M-02 statements in the initial audit text:

- Model current Blob: `05ed37fe4c673ed938672b0f7ce4f3da85f58472` (commit `27da6a7686896f884750faf2ae9289200578782e`).
- Test current Blob: `6192f18a8b94a39be6fcef999f62edcb4542383a` (commit `2a936b38e62facad69813d94968d1e70568ee248`).
- README current Blob: `1abcc3f92d97cea4f18049d2b0fcd18eca3a2952` (commit `b5adbba92c6d447e4cbdcddbebb42deeafc02914`).
- M-01: model now uses `core_barrier_ready`, explicitly not I GlobalForget Completed. CLOSED at model naming/scope level only; I full completion vector remains unmodeled.
- M-02: model now has `record_no_publication_proof`, proof-required terminal invariant, stale-worker mutant and regression path. CLOSED as a missing model transition; E→D terminal receipt schema/authority mapping and Storage no-publication proof remain OPEN.
- M-03 remains open: one Fence generation only; overlapping Forget not modeled.
- M-04 remains open: real D/I/Storage crash cut points, prepared transaction and WAL/MVCC/2PC recovery absent.
- M-05 remains open: liveness/fairness and external progress assumptions require explicit treatment.

Verified successful runs:
- Run `44140051181`, SUCCESS, exact tested commit `c6c6e136f3d1c1b24448e28b754bfe083fe1a0f8`; model and unittest steps both SUCCESS; 14 tests; 28,383 state/depth pairs; 13 mutants.
- Run `44140042792`, SUCCESS, exact tested commit `6b762b8cbcb5ca235ee230e0111322628661b7e0`; model and unittest steps both SUCCESS.
- Earlier run `44139591931` failed because the model state count had expanded to 28,383 while the old assertion expected 27,472. Subsequent baseline/test fixes are covered by the later successful runs; failure history retained.
- Run `44140003348` and `44139992597` also failed during intermediate sequential commits (stale count / stale test references). They are superseded by the successful later runs and are not hidden.


### README CI pointer refresh

- Current model README Blob: `4316d7e59cb2ec6668e4a68f79000b2ac28987e9`, commit `5f92e2301def1770499efccfff93c4b7cb769e65`; it now points to successful run `44140051181` and records 14 tests.
- Documentation-only README commit triggered a fresh workflow run `44140438929`, which was queued/in progress at last readback. This later run is not yet claimed as passed; the model code/test success remains the exact run `44140051181`.
