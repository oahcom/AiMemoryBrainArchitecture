# A Owner Source Refresh 004 — Exact Owner Refs, Contract Blobs, CI and Gate Disposition

- Review ID: **A-OWNER-SOURCE-REFRESH-004**
- Authority: A / Principal System Architecture Authority
- Status: **READ-ONLY SOURCE AUDIT / INTEGRATION DISPOSITION**
- Main baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Audit date: 2026-11-18
- Scope: B/C/D/E/F/G/H/I/Storage current branch refs, selected normative/candidate contract Blobs, relevant PRs, bounded CI evidence, H/C tree-integrity recovery and Gate status.
- This report does not amend any Owner contract, approve an ADR, merge a PR, release a Gate or authorize implementation/production.

## 1. Executive disposition

**Overall: DEFERRED / ARCHITECTURE_NOT_READY.**

The live main ref is unchanged at `e52594f181d2edb77448adcfed64a0fbdffaf3aa`. All nine Owner branch refs were independently resolved by comparing each branch against itself. Exact key contract files were fetched from the named branches and their Blob SHAs recorded below.

The H/C tree-integrity incident is now **substantially reconciled at the source-tree level**:
- C's truncated incident snapshot was restored to a 136-Blob branch at `88992da...`, which remains the live C branch HEAD.
- H's truncated incident snapshot was restored at `4e65a2...` (215 Blobs), then advanced to live HEAD `6608cde...` (216 Blobs).
- The H changes from tested commit `4e65a2...` to current `6608cde...` are two documentation-only files; the schema, validator, tests and workflow are unchanged.
- This closes the narrow question “were the missing H/C files restored?” It does **not** close the broader questions of independent Owner approval, C/H wire mapping, production trust, durable replay, or end-to-end integration.

A new blocking contradiction was found in Storage's exact Option A ADR: its header says Option A is selected for L1, while §3 says no option is selected by the ADR and Option A is only a preferred candidate. Storage v3.3.2 repeats the “selected” interpretation. Until Storage resolves the contradiction in its own authoritative source, L1 must be treated as **CONFLICTED / NOT SAFE TO FREEZE**, not as a cleanly selected topology.

Other unchanged blockers:
- B Fact/Claim remains ADR-BLOCKED.
- I36-GOV-01..10 remain GOVERNANCE-BLOCKED; no effective governance approvals are recorded.
- D/I/Storage Phase 3.9 terminalization documents remain proposals; no shared exact-version Owner acceptance is evidenced.
- H-ADE-001..003 remain open and blocking for protected Applied/Replay paths.
- Issue #7 remains OPEN; G3 implementation entry remains BLOCKED.

## 2. Frozen main baseline and branch graph

| Ref | Exact SHA / comparison | Main-relative compare | Meaning |
|---|---|---:|---|
| main | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | identical to itself | Current audit anchor |
| B `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | 42 ahead / 58 behind; 25 changed paths reported | Diverged Owner branch |
| C `session-c-agent-integration-2026-11-16` | `88992da30331121b81cf2773acab11d921daf281` | 169 ahead / 58 behind; 106 changed paths reported | Restored current Owner branch |
| D `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | 109 ahead / 66 behind; 60 changed paths reported | Current D source snapshot |
| E `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63a3b8dd77f670ed` | 88 ahead / 66 behind; 28 changed paths reported | Branch ref resolves; commit metadata fetch anomaly noted below |
| F `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | 41 ahead / 66 behind; 23 changed paths reported | Current F source snapshot |
| G `session-g-memory-context` | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | 42 ahead / 66 behind; 24 changed paths reported | Current G source snapshot |
| H `session-h-bmcp-protocol` | `6608cde89d959257db612d8ff8080f631333f3f3` | 490 ahead / 58 behind; 182 changed paths reported | Restored, current H source snapshot |
| I `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | 203 ahead / 58 behind; 105 changed paths reported | Current I source snapshot |
| Storage `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | 359 ahead / 57 behind; 87 changed paths reported | Current Storage source snapshot |

The ahead/behind and changed-path counts are graph comparisons against main, not a recommendation to merge these branches. The Owner branches have materially diverged histories; do not bulk-merge or infer a safe integration base from these counts.

**E ref anomaly:** self-compare resolves the E branch HEAD to `ee098e...`, and fetching the E contract by branch ref succeeds. A direct commit metadata fetch for that SHA returned GitHub 422 “No commit found for SHA”. Treat the ref and Blob as observed, but require E to reconcile the commit-object lookup before using ancestry/commit metadata as a proof source.

## 3. Exact Owner source manifest

The Blob SHA is the exact content identity read from the live branch ref. “Candidate” or “draft” status is preserved; branch presence does not imply approval.

| Owner | Branch HEAD | Key exact source (path — Blob SHA) | Current source disposition |
|---|---|---|---|
| B | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | `02-domain-model/ADR-001-fact-claim-semantics.md` — `a1024938ff5baba069cf128c69496a44e143330c` | **ADR-BLOCKED**; no named governance authority, approver, selected option or effective decision |
| C | `88992da30331121b81cf2773acab11d921daf281` | `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` — `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; workflow `.github/workflows/c-provider-outcome-conformance.yml` — `a1f0b8f884f0f294fb3ec96da7c4f11e294e5142` | C schema candidate and bounded conformance; current workflow push filter omits the 1.0.1 schema path |
| D | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | `03-memory-brain/forget-fence-and-completion-contract.md` — `1f0391bc49d007c44ec74165bd33d37412cc7990`; `03-memory-brain/canonical-memory-store.md` — `6b37c91033fda21f072e2a3bde6f274663b1e76e` | D canonical Forget semantics decided; detailed record layouts/transaction implementation remain candidate; global completion is I-owned |
| E | `ee098e14747d9915de5b3efb63a3b8dd77f670ed` | `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` — `5ca77a5b48e69afb3bc81429baf538be7dce4d46` | Candidate E contract; Storage realization, D APIs, H envelope and I policy approval remain open |
| F | `1908ce4d233b20f7cafd00cb679affd01bd15174` | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` — `ce59252dbbdc5d10d016704797e9ba12d5a941bd`; model `tests/anti_resurrection/f_runtime_model.py` — `33fa2ca2dc29771aca241e194f13e078a4f8d774`; tests — `c2575327a75577923440ef770d42122218a1e091`; workflow — `c0fac9eff93ca46e466cda5fe04613bd4565e9b3` | F logical runtime safety semantics decided in its addendum; cross-owner interfaces open; production implementation not verified |
| G | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` — `bd297873bc1e593280484a43cb44b56058d9c4ff` | G-owned normative design draft; implementation not verified; cross-owner acceptance required; not an independent human Owner signature |
| H | `6608cde89d959257db612d8ff8080f631333f3f3` | Unified 1.2.15 schema — `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; Applied Delivery Evidence 1.0.0 schema — `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`; validator — `2f6de24eea737cf75a16ead7495bea4627bb1bb4`; tests — `bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5`; workflow — `7bd9bf3a4141d1e239d0f165e2e98fdd25961254` | Restored schema/validator/test candidate; bounded CI pass; H-ADE-001..003 remain OPEN |
| I | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` — `9100061fa986fb6676656169de3fcf9fc1c72664`; governance register — `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | Global inventory contract is candidate; I36-GOV-01..10 remain GOVERNANCE-BLOCKED; no effective policy approval |
| Storage | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | Option A ADR — `bb544ba2f346bdc130d524bd5c7310d86f367988`; v3.3.2 manifest — `5c614375e10698e4931d83deb57d20321445e068` | **L1 status internally conflicted**; L4 physical engine/deployment remains OPEN; v3.3.2 is not jointly accepted/frozen |

### 3.1 B — Fact/Claim remains blocked

The exact B ADR says:
- formal decision authority: NOT RECORDED;
- named approver(s): NOT RECORDED;
- approved option: NONE;
- approval record: NONE;
- status: ADR-BLOCKED.

B's Option A recommendation is a recommendation, not a decision. D's Canonical Memory Store independently states Fact/Claim persistence is ADR-BLOCKED and forbids freezing DDL, public schema, stable cross-module wire fields or immutable Fact/Claim identities from either alternative.

### 3.2 C — workflow trigger defect

The live C workflow Blob `a1f0b8...` watches the 1.0.0 schema path but not `c-submit-outcome-1.0.1.schema.json`. Draft PR #94 adds exactly that missing path; its workflow readback Blob is `75e294ab1552f24fde76c3e881ab2cf5e7b791e2`. PR #94 is not merged, and schema-only trigger execution is explicitly PENDING. The 19-test run below did include CSubmitOutcome 1.0.1 tests, but it does not prove the missing path filter would trigger on a schema-only change.

### 3.3 H — Applied Delivery Evidence blockers

A's exact review in PR #98 identifies three open blockers:
- **H-ADE-001:** strict parser uses standard JSON decoding and does not reject duplicate object keys before materialization; signed-message ambiguity/parser differential risk.
- **H-ADE-002:** CSubmitOutcome 1.0.1 semantic join is not explicit in H's validator contract; C immutable record, outcome/side-effect, final-boundary/request digest and lineage equality need a version-pinned resolver/verifier and C/G review.
- **H-ADE-003:** current I authorization/PermissionEpoch, key, audience/scope and applicable D Forget fence recheck before replay result-reference disclosure is underspecified.

These block authenticated production use, Full Applied and replay acceptance respectively. The 11-test H suite does not close them.

## 4. H/C branch integrity incident — exact reconciliation

| Event | Exact ref | Observed evidence |
|---|---|---|
| H incident snapshot | `0277a8b9ee63be850acc0b8b1b08625524aaa33b` | PR #91 reports a 7-path tree; 205 removals, 2 additions, 3 renames relative to prior H snapshot |
| C incident snapshot | `a5dff993e5c2928a28deb777c41023cfe923366f` | PR #91 reports a 5-path tree; 133 removals, 2 additions, 1 rename relative to prior C snapshot |
| H restored snapshot | `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6` | PR #92 records 215 Blobs; compare from H incident snapshot is 5 commits ahead / 0 behind |
| C restored/current snapshot | `88992da30331121b81cf2773acab11d921daf281` | PR #92 records 136 Blobs; compare from C incident snapshot is 1 commit ahead / 0 behind; this is still current C branch HEAD |
| H current snapshot | `6608cde89d959257db612d8ff8080f631333f3f3` | 216 Blobs recorded in A/C source refresh; 1 commit after tested restoration snapshot; compare shows only two Phase 3.8.24 documentation files changed |

The incident is reconciled for file-tree restoration and current ref identity. It is **not** evidence that all C/H contracts are accepted or production-ready. PR #92 remains Draft/Open and targets `research/tech-reality-001-c`, not main. It records C/H mapping as NOT ACCEPTED / NOT VERIFIED, independent human review PENDING, C Agent/Provider/Tool/Brain end-to-end tests NOT RUN.

## 5. Relevant PR state and authority boundary

| PR | State at audit | Exact scope / disposition |
|---|---|---|
| #55 | Open / Draft | B domain research proposal; not a Fact/Claim governance decision |
| #66 | Open / Draft | D Phase 3.9 terminalization proposal; base D branch `194c4c8...`, head `4d1a044...`; reports 19/19 local Python model tests, not GitHub CI or production proof |
| #68 | Open / Draft | I/D terminalization authorization proposal; base I branch `0d071bf...`, head `a71985e...`; requires exact D/I decisions and Storage boundary acceptance |
| #71 | Open / Draft | Storage Phase 3.9 review; base Storage branch `830a559...`, head `65c0387...`; explicitly role-simulated, not independent Storage Owner signature; conditional logical acceptance only |
| #91 | Open / Draft | A H/C tree-integrity incident report |
| #92 | Open / Draft; mergeable=false | C-REVIEW-001 restoration and consumer review; not merged, not main |
| #94 | Open / Draft | C workflow path-filter correction; one-line change; schema-only trigger execution pending |
| #98 | Open / Draft | A exact H Applied Delivery Evidence review; H-ADE-001..003 open |
| #99 | Open / Draft | ARCH-CONVERGENCE-001 source inventory; non-normative, requires this source-refresh delta |

Open/Draft/mergeable metadata is not Owner approval. A role-simulated review is not an independent human Owner signature. No PR listed above was merged by this audit.

## 6. CI and executable evidence — exact scope only

| Owner | Run / commit | Result | Evidence ceiling |
|---|---|---|---|
| B | No semantic ADR CI evidence identified | NOT ESTABLISHED | ADR decision is a governance action, not a test result |
| C | Run `44129914790`, commit `88992da...` | **19/19 PASS** | C schema/crypto candidate vectors; logs include 1.0.1 tests; no C/Brain end-to-end or production trust |
| D | PR #66 reports 19/19 local Python reference-model tests | **LOCAL ONLY** | Not GitHub Actions; not D/Storage/I physical conformance |
| E | No exact current-head CI evidence identified | NOT ESTABLISHED | E contract remains candidate; no implementation readiness inferred |
| F | Run `43961714501`, tested commit `f1ba5c...` | **19/19 PASS** | In-memory deterministic logical model; compare to current F HEAD `1908ce...` shows 9 commits later and documentation-only changes; model/test/workflow Blobs unchanged |
| G | No exact current-head CI evidence identified | NOT ESTABLISHED | G Applied contract explicitly says implementation not verified |
| H | Run `44130722532`, tested commit `4e65a2...` | **11/11 PASS** | H Applied Delivery Evidence 1.0.0 schema/semantic candidate; H Recovery Cutoff run `44130722851` also SUCCESS on the same commit; current H HEAD `6608cde...` differs only in two documentation files |
| I | Run `43963450717`, tested commit `8a6a6e...` | **30/30 PASS** | In-memory global inventory/completion logical model; current I HEAD `0d071b...` is 128 commits later, but compare shows no model/test/workflow path changes |
| Storage | Run `43965501810`, tested commit `1979863...` | **25/25 PASS** | In-memory restore-high-water logical model; current Storage HEAD `830a559...` is 158 commits later, but compare shows no model/test/workflow path changes; no real DB/HA/restore proof |

For F/I/Storage, “code-tree continuity” means the compared commits contain no changes to the relevant model/test/workflow paths. It does not convert old runs into exact-current-HEAD runs. For H, the same distinction is explicit: the tested code is unchanged, but the current HEAD itself was not the tested commit. CI PASS is not production proof.

## 7. Storage Option A — blocking source contradiction

Exact ADR Blob: `bb544ba2f346bdc130d524bd5c7310d86f367988`.

The header states:

> L1 LOGICAL TOPOLOGY SELECTED — OPTION A; L4 PHYSICAL ENGINE/DEPLOYMENT OPEN

But §3 states:

> Therefore no option is selected by this ADR. Option A is the preferred candidate only if the actual deployment proves it; otherwise Option B requires a separate ADR and proof bundle.

The v3.3.2 manifest Blob `5c614375...` describes Option A as selected for the normative v1 logical architecture and says it corrects the ADR status. That statement cannot resolve the contradictory body of the exact ADR. The same ADR also keeps T1–T8 open, including runtime identity, D/Storage row boundary, linearization, I proof, atomic outcome, HA/restore, read path and Owner decisions.

**A disposition:** do not claim a clean L1 Option A selection until Storage publishes an Owner-approved exact-Blob correction or successor ADR and D/Storage confirm the same scope. L4 physical engine/deployment remains OPEN regardless.

The Storage Phase 3.9 review in PR #71 is conditional and explicitly not an independent Storage Owner signature. The D/I/Storage Phase 3.9 proposal trio is not a normative joint protocol.

## 8. Gate status

| Gate | Current disposition | Exact reason |
|---|---|---|
| G1 — source freshness / provenance | **PARTIAL** | All nine branch refs and selected Blobs are pinned; H/C restoration is source-reconciled. Full per-file Owner-tree audit, independent Owner approval provenance and E commit-object discrepancy remain open |
| G2 — canonical domain semantics | **BLOCKED** | B Fact/Claim ADR is ADR-BLOCKED; main invariant/principle wording and domain overview conflict |
| G3 — runtime implementation entry | **BLOCKED** | Issue #7 remains OPEN; canonical runtime repository, accountable engineering owner, reproducible build/CI authority and deployment/operator map are not established |
| G4 — identity, authorization and governance | **BLOCKED** | I36-GOV-01..10 remain GOVERNANCE-BLOCKED; no effective approvals; global inventory contract remains candidate |
| G5 — canonical lifecycle / Forget / anti-resurrection | **BLOCKED / NOT PROVEN** | D/I/Storage Phase 3.9 are proposals; no shared exact-version acceptance; F model is logical only; production indexes, replicas, backups and external targets are not exercised |
| G6 — C/H/G Applied and provider evidence | **PARTIAL / NOT PASSED** | C 19/19 and H 11/11 bounded candidate CI; C/H exact mapping not accepted; PR #94 trigger fix pending; H-ADE-001..003 open; G contract is draft |
| G7 — Storage / COC / JF-10 physical consistency | **BLOCKED / NOT PROVEN** | Option A ADR contradiction; L4 open; v3.3.2 binds H 1.2.14/C 1.0.1 rather than H 1.2.15 plus Applied Delivery Evidence 1.0.0; no production DB/HA/restore proof |
| G8 — production readiness | **NOT READY** | No complete runtime location, Owner approvals, exact compatible bundle, production trust, physical transaction proof or end-to-end safety evidence |

### Overall A decision

**DEFERRED / ARCHITECTURE_NOT_READY.**

G1 remains PARTIAL. G2–G5 and G7 remain BLOCKED. G6 remains PARTIAL / NOT PASSED. G8 is NOT READY. No Gate is released by this report.

## 9. Required Owner actions (no A semantic substitution)

1. **B + Architecture Governance:** record the named decision authority, approver(s), Option A/B decision, rationale, timestamp and downstream migration/consumer approvals for Fact/Claim.
2. **C:** merge or otherwise Owner-approve the 1.0.1 workflow path correction through its governance process, then produce a schema-only trigger run; separately complete C/H/G exact field mapping and end-to-end scenarios.
3. **D:** state whether PR #66 Phase 3.9 supersedes any exact D clauses; publish an exact accepted successor only after Storage/I concurrence.
4. **E:** reconcile the current branch commit-object lookup anomaly and provide reproducible compiler/producer admission evidence.
5. **F:** retain the logical anti-resurrection model as a regression baseline; provide real index/cache/Working Set and restore/rebuild race evidence before runtime claims.
6. **G:** obtain C/H/I/D/Storage exact consumer decisions for the Applied contract; do not claim implementation from the design draft.
7. **H:** close H-ADE-001 strict duplicate-key parsing, H-ADE-002 C outcome/final-boundary join and H-ADE-003 current authorization/fence recheck before replay result disclosure; rerun exact-head CI after code changes.
8. **I:** resolve I36-GOV-01..10 with required external/independent approvals and bind the global inventory to D and every registered producer/recipient/backup surface.
9. **Storage + D:** resolve the Option A ADR contradiction, publish one exact L1 decision, and provide L4 runtime/engine/operator plus T1–T8 physical proof; issue a successor manifest bound to the exact H/C successor bundle.
10. **Project authority:** answer Issue #7 with canonical runtime repository, branch, code owners, build/CI, artifact SHA and deployment/operator map.

## 10. Explicit non-authorizations

This source refresh does **not** authorize:
- merging PR #55/#66/#68/#71/#92/#94/#98/#99 or any other PR;
- changing main or any Owner branch;
- approving B Fact/Claim or any Owner ADR;
- freezing Storage topology, C/H wire mapping, Applied schema or production crypto profile;
- declaring GlobalForgetCompleted or PhysicalErasureConfirmed;
- runtime implementation, production data access, provider side effects, deployment or production activation.

Only read-only source review, documentation-only A reporting and bounded synthetic feasibility work within existing governance limits are covered.

## 11. Reproduction pointers

- Main: `https://github.com/oahcom/AiMemoryBrainArchitecture/commit/e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- H/C integrity review: PR #91
- C restoration/consumer review: PR #92
- C workflow path correction: PR #94
- H Applied Evidence exact A review: PR #98
- Initial source inventory: PR #99
- D/I/Storage Phase 3.9 proposals: PRs #66/#68/#71
