# C-REVIEW-001 — Agent Integration Independent Architecture Review & Remediation
# C-REVIEW-001 — Agent Integration 独立架构审查与整改

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Target: PR #69 — `research/tech-reality-001-c`
- Review baseline: PR #69 HEAD `a69007a016aea4fcd60a05dfebf5a66ccf7f2538`
- PR base / merge-base at review: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Current main at review: `e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Remediation branch: `review/c-review-001-remediation-2026-11-18`
- Status: **REVIEW FINDINGS RECORDED; C-OWNED DOCUMENTATION REMEDIATION APPLIED; CROSS-OWNER BLOCKERS OPEN; HUMAN INDEPENDENT REVIEW PENDING**
- Review authority: delegated AI review/remediation under explicit user authorization. This report does **not** claim an independent human reviewer, separate organizational Owner signature, or approval of another Owner's contracts.

## 1. Executive disposition / 总体结论

**PR #69 is not implementation-ready and is not merge-ready.** The research package contains useful and mostly cautious separation of Agent, Model, Provider, Tool, Request/Attempt, Brain commit, and G Applied semantics. However, the current-source evidence is stale in important places, the H Applied Delivery Evidence 1.0.0 test candidate now exists and passes its bounded CI, but exact C/H field mapping remains unaccepted/unverified; C end-to-end integration tests/benchmarks remain unrun.

Disposition:
- C0 Baseline: **PARTIAL** — refreshed source pins; PR branch still diverges from current main.
- C1 Boundary: **CANDIDATE** — no cross-owner architecture approval inferred.
- C2 Inference: **CANDIDATE / OPEN** — B/D/E/I typed semantics and trust dependencies remain.
- C3 Provider Outcome: **BLOCKED** — H 1.0.0 schema/validator candidate exists (11/11 CI), but C/H COutcomeRecord/final-boundary mapping is not accepted; C/H/I/Storage binding is not frozen.
- C4 Telemetry/Failure: **RESEARCHED / OPEN** — I privacy/retention approval and executable redaction evidence remain.
- C5 Cross-owner: **BLOCKED / PARTIAL** — exact H/G delta creates an explicit missing wire-mapping gate; Storage and trust mismatches remain.
- C6 Validation: **PLAN READY / NOT RUN** — no C end-to-end tests or benchmarks are claimed.
- C7 GitHub: **REMEDIATION PR PENDING / PR #69 STILL DRAFT**.
- C8 Independent review: **INDEPENDENT HUMAN REVIEW PENDING**.

No Provider/Agent framework selection, schema freeze, production activation, Brain implementation, Applied proof, Forget completion, physical erasure, or merge is approved by this review.

**中文结论：PR #69 尚未达到实现就绪或合并就绪。** 研究包正确地区分了 Agent、Model、Provider、Tool、Request/Attempt、Brain Commit 和 G Applied 等语义，但当前性证据存在过期，H Applied Delivery Evidence 契约尚未实现/冻结，C 集成测试和基准均未运行。

本审查没有批准 Provider/Agent Framework 选型、Schema 冻结、生产激活、Brain 实现、Applied 证明、Forget 完成、物理擦除或合并。

## 2. Exact evidence baseline / 精确证据基线

| Item | Verified value |
|---|---|
| PR #69 | Open, Draft, not merged |
| PR #69 HEAD | `a69007a016aea4fcd60a05dfebf5a66ccf7f2538` |
| Original base / merge-base | `b3c666e67982cb3d3374e759cfb6552c7765aacb` |
| Current main | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` |
| Compare current main...C head | 7 commits ahead / 2 behind |
| Changed files | 17 |
| Additions / deletions | 1,247 / 0 |
| PR reviews / inline comments / conversation comments | none returned at review time |
| C validation scenarios | V01–V22 defined; not executed |
| C Owner branch restored | `88992da...`; 136 blobs |
| C Provider Outcome candidate CI | run `44129914790`; 19 tests, 0 failures |
| H Owner branch restored | `4e65a2...`; 215 blobs |
| H Applied Delivery Evidence 1.0.0 CI | run `44130722532`; 11 tests, 0 failures |
| C/H integration mapping tests | NOT RUN / NOT IMPLEMENTED |
| C Provider/Tool/Brain integration tests | NOT RUN |
| C benchmarks | NOT RUN |

All 17 PR #69 paths were enumerated from GitHub and fetched at the exact PR HEAD; Blob SHAs were captured during the review. This review pass focused on the package index, baseline, cross-owner matrix, conflict register, decision record, validation plan/assets, Provider research, telemetry, failure semantics, and canonical boundary contract. It is not a claim that every sentence of every bilingual section has received a second human line-by-line review.

## 3. Findings / 发现

### CR-001 — Stale baseline and source pins [C-owned, HIGH]

The package README and baseline described `b3c666...` as current main and contained an intermediate C branch SHA `274f5ec...` as the refresh snapshot, while live PR metadata identified C HEAD `1a1d6f2...` and current main had advanced to `e52594f...`. The current-main comparison reports 6 commits ahead / 2 behind.

**Risk:** reviewers cannot reproduce which exact baseline was reviewed; downstream merges may be evaluated against an obsolete base.

**Remediation:** README and baseline now distinguish original merge-base, current main, exact PR HEAD, and compare result. A current-main rebase/equivalent reconciliation and fresh diff check are still required before PR #69 can merge.

### CR-002 — G/H source pins stale; H current branch materially changed [C-owned evidence refresh + H-owned blocker, BLOCKING]

The cross-owner matrix pinned G at `3367438...` and H at `0d363244...`. Live branch reads show:
- G current HEAD: `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`; the G Applied Persistence EN contract Blob is `bd297873...`, and the latest Chinese companion Blob is `82553a47...`.
- H incident snapshot: `0277a8b9ee63be850acc0b8b1b08625524aaa33b`; restored current H Owner HEAD: `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`.

At the incident snapshot H's latest commit had parent `0d363244...` and removed the prior Unified 1.2.15 schema, Gateway/Provider validators, conformance tests and most of the previous H branch tree. The H Owner branch was subsequently restored at `4e65a2...` with 215 blobs, including those artifacts and the new Applied Delivery Evidence 1.0.0 candidate.

**Risk:** the C matrix and validation index could be read as asserting that old H schema/validator artifacts are current branch contents. Historical CI is not current branch conformance and is not production trust proof.

**Remediation:** C baseline and matrix now pin the current G/H heads and explicitly label H 1.2.15/CI as historical evidence. C must not recreate or edit H-owned schema/validator files.

### CR-003 — H Applied Delivery Evidence is a separate message family; candidate implemented, C/H mapping still open [Cross-owner, BLOCKING]

H Phase 3.8.23 (EN Blob `be308261c3e000e712a3cdbd3dbf60507156127b`; zh-CN Blob `641abd9b5a4ed271c3c4b561747c99d7cde79463`) explicitly distinguishes:
- Unified 1.2.15 `C_PROVIDER_OUTCOME_RECORDED` Gateway Attestation; and
- Adapter/Runtime Applied Delivery Evidence.

H states that the existing P0 allowlist/schema/validator must not be widened in place. H Phase 3.8.24 now supplies a separate `bmcp.applied-delivery-evidence` 1.0.0 schema (Blob `2ce8776...`), validator (Blob `2f6de24...`) and tests (Blob `bb2bb6c...`). Exact-head GitHub Actions run `44130722532` passed 11/11 tests. The artifact is explicitly a test/conformance candidate, not production crypto or durable replay. Wire mapping remains **NOT FROZEN**.

**Required closure:**
1. H publishes the exact successor schema, validator, P0 vectors, and CI.
2. C reviews exact CSubmitOutcome 1.0.1 field duplication and equality of `final_request_boundary_id` against the H-owned delivery evidence.
3. G confirms Delivery/Context/Applied binding.
4. I approves signer/profile/key registry and trust roots.
5. Storage binds the exact successor bundle in a reviewed manifest.

C may define and test its consumer mapping, but cannot author or freeze H's wire fields.

### CR-004 — Validation count and evidence-status contradictions [C-owned, MEDIUM]

The validation plan contains V01–V20 plus V21 and V22. The validation README said 20 scenarios. It also marked H 1.2.15 exact validator CI as NOT VERIFIED in one section while listing the historical 91-test and 288-test CI results later in the same file.

**Remediation:** the validation README now states V01–V22 and labels the H CI as historical bounded evidence at ancestor `0d363244...`, explicitly not current H branch content and not C integration CI.

### CR-005 — Provider capability matrix contradicted its own current-source addendum [C-owned, MEDIUM]

The initial Provider matrix marked Anthropic, Ollama and Hugging Face API facts as wholly NOT VERIFIED, while the later 2026-11-18 addendum recorded official endpoint/routing facts for all three.

**Remediation:** the matrix and Chinese summary now record the verified endpoint/routing facts while retaining NOT VERIFIED for stable operation identity, full error taxonomy, cancellation, per-model support, SDK/license pins and idempotency. No cross-provider semantic parity is claimed.

### CR-006 — Storage/H version and trust remain unresolved [Cross-owner, BLOCKING]

Storage v3.3.2 still pins H 1.2.14 and CSubmitOutcome 1.0.1, not the historical H 1.2.15 candidate or the proposed Applied Delivery Evidence successor. C/I crypto profiles remain NOT REGISTERED. H local CI, even when successful at the historical H commit, does not prove production issuer authentication, live signing order, durable replay, anti-rollback or I/D/Storage service integration.

**Closure:** H/Storage/C/I exact-version successor manifest and Owner decisions, plus production trust and replay evidence. C cannot close this conflict by updating a version string.

### CR-007 — G Applied, D Forget and B semantics remain external gates [Cross-owner, BLOCKING/HIGH]

- G Applied remains blocked; G owns the Full Applied predicate and durable Applied record.
- D ForgetFence and I authorization/revocation are independent mandatory predicates.
- D/I/Storage Phase 3.9 PRs #66/#68/#71 remain Draft proposals, not normative approvals or production proof.
- B PR #55 remains Draft; B0/B5 are not passed and Fact/Claim remains ADR-BLOCKED.
- Issue #7 remains open: authoritative runtime implementation repository and accountable engineering owner are not established.

**Closure:** exact-version Owner decisions and executable consumer conformance; no C-only document edit can close these gates.

### CR-008 — Validation and benchmark evidence absent [C-owned / Runtime dependency, HIGH]

The 22 scenarios are a design plan. C Agent/Provider/Tool/Brain end-to-end tests, real Provider tests, real Tool side-effect/recovery tests, Forget-vs-late-result fault injection, G Applied end-to-end tests, production trust tests and representative benchmarks are all NOT RUN.

**Closure:** a version-pinned, reproducible harness, synthetic fixtures, explicit environment and run logs. Until then, C6 remains NOT RUN.

## 4. C-owned remediation applied in this branch / 本分支已执行的 C 自有整改

The following edits were applied on `review/c-review-001-remediation-2026-11-18`, based on PR #69 HEAD `a69007a...` after merging its latest field-mapping addendum:

1. `TECH-REALITY-001-C/README.md` — corrected baseline and current-source status; distinguished historical H CI from current H branch contents.
2. `existing-integration-baseline.md` — corrected current main, PR #69 head, G/H branch heads, and historical H artifact status.
3. `agent-integration-cross-owner-contract-matrix.md` — refreshed G/H pins and added H Phase 3.8.23 delivery-evidence mapping delta.
4. `agent-integration-conflict-register.md` — added C-CON-017 (H successor mapping blocker) and C-CON-018 (stale C base); clarified historical H version evidence.
5. `validation/README.md` — corrected V01–V22 count and H CI status.
6. `provider-integration-research.md` — reconciled initial provider matrix with its later official-source addendum.
7. This review report — records evidence, boundaries, findings and closure conditions.

No H/D/G/I/Storage authoritative contract was modified. No C executable tests or benchmarks were represented as run.

## 5. Required next gates / 后续 Gate

| Gate | Required action | Current status |
|---|---|---|
| C0 | Reconcile current main and all exact Owner source pins | PARTIAL |
| C3 | C/H Applied Delivery Evidence successor mapping and exact-version acceptance | BLOCKED |
| C5 | C/G/H/I/Storage exact bundle and Owner acceptance | BLOCKED |
| C6 | Execute C conformance, race/fault tests and benchmarks | NOT RUN |
| C8 | Independent human reviewer reads exact remediation HEAD and all changed blobs | PENDING |

**No merge is requested.** PR #69 must remain Draft until the above blockers are resolved and the remediation branch is read back at exact HEAD/Blob SHAs. The review PR itself should also remain Draft until a human independent reviewer has inspected this report and the patch.

**中文后续要求：** 不请求合并。PR #69 应继续保持 Draft，直到上述阻塞项解决，并按精确 HEAD/Blob SHA 读回整改分支。整改 PR 也应保持 Draft，直至独立人类审查者检查本报告和补丁。

## 6. Evidence links / 证据链接

- PR #69: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/69
- Current main: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/e52594f181d2edb77448adcfed64a0fbdffaf3aa
- C reviewed HEAD: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/1a1d6f26a793fc285a1806edf21b696f748a8fed
- G current HEAD: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/763b3d31e910db8fd29c6e4dbaff9273b7fb66b8
- H current HEAD: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6
- H historical 1.2.15 evidence commit: https://github.com/oahcom/AiMemoryBrainArchitecture/commit/0d36324457e39bd50ad56ae902d477c4ea765b61
- H Phase 3.8.23 mapping decision: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-h-bmcp-protocol/08-bmcp-protocol/phase-3.8.23-h-exact-review-g-applied-delivery-evidence-mapping.md
- G Phase 3.8.22 Applied Persistence contract: https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-g-memory-context/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md


## 7. Post-restoration exact C/H candidate review / 恢复后的 C/H 候选精确审查

### Owner branch restoration
A review PR #91 reported that C/H Owner branches had lost large portions of their trees. Subsequent exact branch reads show restoration commits:
- C `session-c-agent-integration-2026-11-16` HEAD `88992da30331121b81cf2773acab11d921daf281`, 136 blobs; Provider Outcome CI run `44129914790` passed 19/19.
- H `session-h-bmcp-protocol` HEAD `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`, 215 blobs; Applied Delivery Evidence CI run `44130722532` passed 11/11 and Recovery Cutoff workflow also succeeded.
- PR #69 remains on its distinct research branch HEAD `1a1d6f2...`; the restored C Owner branch is not automatically incorporated into PR #69 or PR #92.

### CR-009 — C/H 1.0.0 mapping is not executable end-to-end [Cross-owner, BLOCKING]
H 1.0.0 schema correctly exposes all seven `HDeliveryBindingIdentity` fields and seven `HObservationRecordIdentity` fields, plus `evidence_kind`. It also exposes C linkage fields `c_submit_outcome_ref`, `c_outcome_record_ref`, `c_outcome_record_sequence`, and `c_outcome_payload_digest`. CSubmitOutcome 1.0.1 defines `COutcomeRecordIdentity = (issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)` and includes `FinalRequestBoundaryRef`.

The H schema has no first-class C `issuer_authority_ref` or C `sequence_namespace_ref` fields. H documentation does not specify whether `c_submit_outcome_ref` resolves an immutable C record containing these omitted identity components, nor does it normatively define equality between duplicated H C fields and the resolved C record. `final_request_boundary_id` must equal the exact C `FinalRequestBoundaryRef`; the H validator only invokes injected `verify_c_final_boundary`, while all current test callbacks return True. No mismatch fixture tests boundary substitution, wrong C issuer/namespace, record sequence mismatch or payload digest mismatch.

**Disposition:** C/H mapping **NOT ACCEPTED / NOT VERIFIED**. H must define exact reference resolution or add the missing C identity fields; C/H must add real cross-schema positive and negative vectors that prove exact equality. H's current test run remains bounded reference-validator evidence only.

### CR-010 — C CI trigger omits the 1.0.1 schema [C-owned, MEDIUM]
The restored C workflow Blob `a1f0b8f...` watches `07-agent-integration/schemas/c-submit-outcome-1.0.0.schema.json` but not `c-submit-outcome-1.0.1.schema.json`, even though its test suite validates 1.0.1. A change limited to the 1.0.1 schema therefore does not match the schema path filter and may not trigger this workflow.

**Required fix:** include the 1.0.1 schema path and verify a schema-only change triggers the workflow. This is a C-owned workflow defect, not a reason to claim the current 19/19 run is invalid; it limits future change detection.

### Updated disposition
H successor schema/validator candidate: **IMPLEMENTED / CANDIDATE CI PASS 11/11**. C Provider Outcome candidate CI: **PASS 19/19**. C/H exact field mapping: **NOT ACCEPTED / NOT VERIFIED**. Production cryptographic trust, durable H replay, G Applied persistence, Storage successor binding, D/I Forget ordering and V01–V22 end-to-end tests remain open.


### CR-011 — G Phase 3.8.22 overstates missing H field [G-owned correction, HIGH]

C's exact-source addendum added in PR #69 head `a69007a...` inspects H Unified 1.2.15's `C_PROVIDER_OUTCOME_RECORDED` oneOf branch and the Gateway validator P0 allowlist. Both contain `final_request_boundary_id`; the schema branch requires it. The G Phase 3.8.22 contract Blob `bd297873...` states that this field is absent. The G statement appears to have inspected only root-level schema properties and missed the nested oneOf branch. C must not edit G's authoritative contract; G should publish a successor correction. `actual_inference_request_id` is also present but is not automatically equivalent to G's `inference_request_id`; five other HDeliveryBindingIdentity members remain absent as first-class 1.2.15 fields.

**Disposition:** HIGH evidence inconsistency; C5 remains blocked pending G correction and exact H/C/G consumer agreement.
