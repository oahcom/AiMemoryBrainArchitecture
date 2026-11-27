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
        - "14-ai-development/work-items/AID-2026-242/manifest.yaml"
        - "00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Source tree, exact blob, current mirrors, AID-2026-089 ruling and current-main INDEX were read; PR exact-head CI and independent D acceptance remain pending."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "AID-2026-242 restricted D source-root recovery evidence"
    canonical_scope_id: "ai-development/aid-2026-242-evidence"
    canonical_scope_keywords:
      - d-memory-brain
      - source-recovery
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-242 — Restricted D normative-root recovery evidence

Attribution: `user-authorized operator (delegated by account owner)`, 2026-11-27. Proxy registration only: **代理登记，非自然人 Owner 签署**.

## 1. Exact baseline and source provenance

- Main baseline fetched before branch creation: `92a759ec1a8c748fc4091015a3a3e8aa97ddc3e3`; latest main synchronization before this task: `b5e1f2a3a54e16fd64fd0f6adb9ab3f3753bb40c`; current fetched main: `788fbc011877a14976fc0a974ffe2e013dd9991b`.
- Source branch: `session-d-memory-brain-2026-11-16`, exact head `b525e1f8fee2471a131e4a38efda99804045e424`.
- Source file: `03-memory-brain/canonical-memory-store.md`, source blob `6b37c91033fda21f072e2a3bde6f274663b1e76e`.
- Main had no `03-memory-brain/` tree at the baseline. Existing EN mirror blob: `414fe03fd40fb8ad46061d2d8c7d29ba2667f252`; existing ZH-CN mirror blob: `34e0755a079f085df65c2a180cc59b6aaea7ea78`.

## 2. Flow-by-flow derivation from the current-main composition review

| Flow | Exact blocking passage / why it matters | D source implicated | Decision |
|---|---|---|---|
| F1 | E Event Store is a candidate seam; E receipt/admission roots are missing. D is mentioned only as the authority boundary; it does not name a missing D file. | No D file to restore for F1. | No D restore from F1. |
| F2 | “D canonical store root is absent.” The same review's missing-root inventory names `03-memory-brain/canonical-memory-store.md`. | `03-memory-brain/canonical-memory-store.md`. | Restore. |
| F3 | “D canonical feed root also absent; no source defines contiguous watermark proof.” The F2/F3 missing-root item is the same canonical store root; its recovered body contains CanonicalCommitCursor, F-owned IndexWatermark, contiguous-prefix, gap-repair and replay clauses. | `03-memory-brain/canonical-memory-store.md` (same file as F2, not a second root). | Restore once; do not infer runtime or F acceptance. |
| F4 | “D Fence source is Draft/Unverified/Informative and not a wire schema.” This is a status/schema gap, not a missing D root. Current main already has `01-system-architecture/forget-fence-and-completion-contract.md` (blob `b3562da378c5dcc54cbdba71f759288a0fe36142`); AID-2026-089 supplies the D-only logical authority boundary. | No extra D Fence file restored. | Keep existing source; wire schema and cross-owner conformance remain open. |
| F5 | D Fence appears as one of the joined facts; no missing D path is named. | No D file to restore for F5. | No D restore from F5. |
| F6 | I root is absent; D is not the missing provider. | No D file to restore for F6. | No D restore from F6. |
| F7 | I global inventory/completion root is absent; D Fence remains a distinct D fact. | No additional D path named. | No D restore from F7; I remains outside scope. |
| F8 | D Fence is identified as a projection boundary; physical storage proof is missing. | No D file to restore for F8. | No D restore from F8. |

## 3. Per-document disposition and AID-2026-089 conflict

| Document | Classification | Evidence / reason | Treatment |
|---|---|---|---|
| `03-memory-brain/canonical-memory-store.md` | **CONFLICTS_WITH AID-2026-089** (narrowly, §17 dependency wording only) | §17 says “I for authorization, Forget fence, retention and erasure policy.” AID-2026-089 / PR #1232 says D is sole logical issuer of ForgetOperation identity/state and ForgetFence generation/cursor; Storage rows are rebuildable D-derived projections; I owns authorization, global policy and Global Forget Completion. | Restore the historical body, add a permanent top-of-file conflict notice, set `canonical_status: Candidate` and `normative_status: Informative`. The conflicting §17 phrase is not current authority. All other body bytes are preserved. |
| `03-memory-brain/commit-cursor-semantics.md` | NOT RESTORED — not named as a missing D root by F2/F3 inventory | It has EN/ZH-CN mirrors, but F3's missing canonical feed root maps to the single listed canonical-memory-store root, which already contains contiguous watermark semantics. | Excluded to avoid expanding the restore set. |
| `03-memory-brain/forget-fence-and-completion-contract.md` | NOT RESTORED — no missing D path | The main canonical Fence source is already `01-system-architecture/forget-fence-and-completion-contract.md`; AID-2026-089 is the controlling logical-authority ruling. | Do not create a duplicate D Fence root. |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` and other Phase 3.6–3.9 D artifacts | NOT RESTORED — not named by the F1–F8 missing-root passages | Historical owner-branch material, later boundary decisions and candidate proposals would risk reopening stale authority. | Leave branch-only. |

AID-2026-089 was merged by PR #1232 as `d914e8a1f8a1ba24c21c41a9249489d544388185`. Its decision: D is sole logical authority for ForgetOperation identity/state, typed target and transitive lineage coverage, Scope coverage, monotonic Fence generation/cursor, canonical suppression and D-domain proof; Storage Fence rows are derived/rebuildable projections with no independent generation/cursor or read/publication authority; I retains authorization, global policy and Global Forget Completion. This recovery does not amend or reapprove that decision.

## 4. GOV-DOC-002 and body-integrity record

- Canonical, EN and ZH-CN files carry complete `document_metadata` blocks using the current schema/template and the checker's actual field/enumeration contract.
- All three are `Draft`, `Unverified`, `Informative`; canonical file is `Candidate`, mirrors are `Non-Canonical`. No approval or natural-person Owner signature is claimed.
- The canonical body, reconstructed by removing the inserted authority-conflict notice and its surrounding blank lines, matches source blob `6b37c91033fda21f072e2a3bde6f274663b1e76e` byte-for-byte (17,387 bytes). The EN and ZH-CN files are translations/mirrors, not byte-identical copies of the source.
- ZH-CN is a structural mirror based on the pre-existing translated mirror; headings are aligned to the 18 source sections (14 Performance, 15 Observability, 16 Failure, 17 Dependencies, 18 Open Questions) without changing the D source bytes.

## 5. Governance scope configuration

- At the fetched main baseline `788fbc011877a14976fc0a974ffe2e013dd9991b`, both `03-memory-brain` and `09-security-governance` are already present in `00-governance/document-scope-registry.yaml` and `scripts/check_bilingual_docs.py` `NORMATIVE_ROOTS`.
- The branch intended to add `03-memory-brain` and `09-security-governance`; those additions are already satisfied on main. The final merge retains the complete main checker implementation, including UTF-8 Git-output decoding, full-history checks and designated-Chinese-side pairing. No checker algorithm or validator behavior is regressed.

## 6. Scope and non-claims

Documentation and work-item registration only. At fetched main `788fbc011877a14976fc0a974ffe2e013dd9991b`, the D canonical-store path is already present with `canonical_status: Canonical`; this PR does not claim a new path creation. It applies the permanent AID-2026-089 authority-conflict notice, changes the canonical status to **Candidate / Informative**, and restores the EN/ZH-CN mirror content from the historical source. No runtime, validator semantics, schema, test, workflow, 04/05 source, Storage code, or Issue state changed. No D Owner acceptance, joint acceptance, wire-schema freeze, implementation conformance, production behavior, or Gate A closure is claimed. #1212 remains OPEN.


### 4.1 Exact blob and metadata comparison

| File | Source / prior-main blob SHA | New blob SHA | Added frontmatter blob SHA | Body treatment |
|---|---|---|---|---|
| Canonical `03-memory-brain/canonical-memory-store.md` | Source branch blob `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `2e10e23f651f1f6cb03247f01727f2b7ff5342f1` | `3ddbdeff332f3646dabde1fd3509543efa0b99e5` | Removing the inserted AID-2026-089 notice and its surrounding blank lines reconstructs the 17,387-byte source blob exactly. |
| EN mirror `docs/en/03-memory-brain/canonical-memory-store.md` | Prior main blob `414fe03fd40fb8ad46061d2d8c7d29ba2667f252` | `8b225da74f42ccaec7418d56ea1f350bbfc19d16` | `5d21c22bfadde921fb6c02c88de723a18e12d416` | Restored full English mirror with the same authority notice; translated prose is not byte-identical to the Chinese source. |
| ZH-CN mirror `docs/zh-CN/03-memory-brain/canonical-memory-store.md` | Prior main blob `34e0755a079f085df65c2a180cc59b6aaea7ea78` | `09c16c7be5fbf1e2fb780ba5a3c52382baae9e41` | `04bd00583972c03d6933eb9d0445f203fb96b28f` | Existing translation aligned to the 18-section structure; same authority-conflict notice translated. |

The frontmatter SHA values above are Git blob SHAs of the exact current YAML frontmatter blocks (including delimiters), recalculated after the AID-242 reference update. The canonical body reconstruction was compared byte-for-byte with the original source blob and matched exactly.


### 4.2 Executed prompt snapshots

- Original prompt-v1 digest before renumbering/path normalization: `33b4bfa744533c9dbf595e2520ff87c4c526e6e6f1c20625ed1fa6b90038af4a`, 4416 UTF-8 bytes.
- Normalized prompt-v1: `14-ai-development/work-items/AID-2026-242/prompt-v1.md`; SHA-256 `c9d765fce7debe0364cb20acbc706af421e88ba6bad4bb7253793b03798a89a1`; UTF-8 bytes `4422`.
- Current W4 prompt-v2: `14-ai-development/work-items/AID-2026-242/prompt-v2.md`; SHA-256 `4bd120dac05ef592acb87b7b6fb5929ca6ccf8617a7fda8be179f39730d1b5fb`; UTF-8 bytes `3501`.
- Session identifiers remain NOT_RECORDED; prompt-v2 was captured from the current user instruction in this conversation.


## 7. Renumbering and current-main reconciliation (2026-11-27)

- The original D work-item ID `AID-2026-109` collided with the distinct I Security & Governance work item already on main (`AID-2026-109`, PR #1300). Main's I directory and its `manifest.yaml`, `prompt-v1.md`, `session-evidence.md`, and report are preserved unchanged at that ID.
- This D work item is assigned `AID-2026-242` by the current task. Its four original files were moved to `14-ai-development/work-items/AID-2026-242/`; internal work-item paths, identifiers and prompt digest were updated.
- Original prompt-v1 digest before path normalization: `33b4bfa744533c9dbf595e2520ff87c4c526e6e6f1c20625ed1fa6b90038af4a` (4416 UTF-8 bytes). The normalized prompt-v1 digest is `c9d765fce7debe0364cb20acbc706af421e88ba6bad4bb7253793b03798a89a1` (4422 bytes); the current W4 prompt-v2 digest is `4bd120dac05ef592acb87b7b6fb5929ca6ccf8617a7fda8be179f39730d1b5fb` (3501 bytes). Both are recorded in the AID-242 manifest.
- The fetched main at `788fbc011877a14976fc0a974ffe2e013dd9991b` already contains `03-memory-brain/canonical-memory-store.md`, with AID-150 provenance and `canonical_status: Canonical`; this PR therefore does not claim that the path is absent at the current baseline. Its substantive correction is the permanent AID-2026-089 authority-conflict notice, demotion to `Candidate` / `Informative`, and restoration of the EN/ZH-CN mirrors from the historical source.
- Main already registers `03-memory-brain` and `09-security-governance` in both the GOV-DOC-002 governed-root registry and the bilingual checker's `NORMATIVE_ROOTS`. The branch's two root additions are therefore already satisfied; the current main checker implementation is retained in full, including UTF-8 Git-output decoding, full-history checks and designated-Chinese-side pairing.
- Attribution for this delegated continuation: `user-authorized operator (delegated by account owner)`, 2026-11-27. This is not a natural-person Owner signature or domain acceptance.


## 8. Local validation (2026-11-27)

- `python` is not installed as a command in the execution environment (`/bin/bash: python: command not found`); equivalent commands were run with `python3`.
- `python3 scripts/test_check_bilingual_docs.py`: `Ran 27 tests`; `OK`; exit 0. The invalid-base test emitted its expected Git fatal diagnostic and still passed.
- `BASE_SHA=788fbc011877a14976fc0a974ffe2e013dd9991b HEAD_SHA=2a0bbb23dc4837864efab85b4031481550d81ba5 PR_BODY='... BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py`: `bilingual baseline: 77 frozen, 0 new gaps`; `Bilingual documentation and prompt-library gate: PASS (9 changed paths inspected)`; exit 0.
- `python3 scripts/check_document_management.py --require-changed 788fbc011877a14976fc0a974ffe2e013dd9991b`: `PASS (incremental): no GOV-DOC-002 violations`; exit 0. The global inventory still reports 371 unclassified documents, which are outside this incremental verdict and this work item's scope.
- The full non-incremental `check_document_management.py` reports `INCOMPLETE` for the repository-wide 371-document backlog (exit 2); this is not a violation in the changed set.


## 9. Final branch synchronization (2026-11-27)

- After the initial merge of main `788fbc011877a14976fc0a974ffe2e013dd9991b`, main advanced by nine commits to `f18adc9fa1d06837433a09498f5297bf13b35756` through AID-2026-211 closeout. The changed paths were unrelated to this work item except the shared `INDEX.md`; that file auto-merged and both the AID-2026-211 row and AID-2026-242 row were retained.
- A second real `git merge --no-ff origin/main` completed without conflicts. Merge commit: `51ac5e254293242c1112f97579608bd89a66fb51`; behind count after merge: `0`.
- The AID-2026-109 I work item remains unchanged; AID-2026-242 remains absent from `origin/main` and is carried only by this PR.
- Final local validation against base `f18adc9fa1d06837433a09498f5297bf13b35756` and head `51ac5e254293242c1112f97579608bd89a66fb51`: 27 bilingual checker tests passed; bilingual gate PASS with 9 changed paths and 0 new gaps; GOV-DOC-002 incremental check PASS with no violations.


## 10. Exact-head GitHub checks and protection read (2026-11-27)

- Pushed PR head measured: `7f71f083aad6b14eefad804e23e66b963a169eb3`; PR #1297 base: `f18adc9fa1d06837433a09498f5297bf13b35756`.
- `GET /actions/runs?head_sha=7f71f083aad6b14eefad804e23e66b963a169eb3`: `total_count=10` (including the initial run and the two workflow reruns triggered by the corrected PR description).
- `GET /commits/7f71f083aad6b14eefad804e23e66b963a169eb3/check-runs`: 20 records across attempts; 16 distinct latest context names, all `completed/success`: `audit`; `GOV-DOC-002 metadata checks`; `Session Evidence`; `Session Evidence self-test (base)`; `Branch freshness vs base`; `Rust clippy (hard gate)`; `rust-workspace-test`; `Rust format (hard gate)`; `Bilingual docs coverage (ratchet)`; `Schema non-empty audit (hard gate)`; `Rust doctests (hard gate)`; `GOV-DOC-001 structural checks`; `Session Evidence self-test (head)`; `BMCP protocol index (hard gate)`; `Repository hygiene (hard gate)`; `BMCP conformance suite (hard gate)`.
- The first Session Evidence attempt failed because the PR body decorated the Work Item ID with explanatory text; the validator requires the ID line to contain only `AID-2026-242`. The PR body was corrected to `Work Item ID: AID-2026-242`; the rerun's Session Evidence job completed successfully.
- `GET /compare/main...docs/2026-11-26-aid-2026-109-d-memory-brain-root-restore`: `ahead_by=21`, `behind_by=0`, merge base equals current main `f18adc9fa1d06837433a09498f5297bf13b35756`.
- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` returned HTTP 403 `Resource not accessible by integration`. `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets` returned an empty list. Therefore `strict` and `enforce_admins` could not be independently read through the available GitHub connection. No merge is claimed or attempted without that required protection verification.


## 11. Manifest-schema gate and third main synchronization (2026-11-27)

- Main advanced from `f18adc9fa1d06837433a09498f5297bf13b35756` to `bc741bdce7b47d3695d85fa9649fe9506f23c595` through 21 commits, including AID-2026-251's Work Item manifest schema, read-only validator, workflow job and AID-2026-109 I-side evidence corrections. The changed AID-2026-109 paths belong to the I work item and remain at AID-2026-109; AID-2026-251's row was preserved in `INDEX.md`.
- A third `git merge --no-ff origin/main` completed without conflicts; merge commit `88a3bba2875f53bd5cac0b834bd202c159f7c1d2` has parents `3f076c8b95e643282d14e1c951b50590bb136390` and `bc741bdce7b47d3695d85fa9649fe9506f23c595`. The shared INDEX auto-merged and retained both the AID-2026-242 D row and concurrent rows.
- The new AID-2026-251 schema requires top-level `class`, `risk`, `risk_rationale`, `status`, `sponsor`, `accountable_owner`, `acceptance_authority`, `repository`, `base_branch`, `base_commit_sha`, `scope`, `evidence`, `documentation`, `session_evidence` and `implementation`. AID-2026-242 manifest was migrated to that structure without changing the GOV-DOC-002 document frontmatter.
- `python3 scripts/ci/check_work_item_manifest_schema.py`: `Manifest schema v1: total=111 compliant=1 violations=110`; AID-2026-242 is the single COMPLIANT manifest. The 110 legacy violations predate this work and are outside scope; the read-only validator exits 0.
- AID-2026-242 remains absent from the fetched main tree `bc741bdce7b47d3695d85fa9649fe9506f23c595`; its explicitly assigned ID is preserved. Behind count immediately after this merge: `0`.


## 12. Local validation after the third main merge (2026-11-27)

Tested merge-synchronized head `0df6ff549386ea0ba2cbb41700f62f7a20683ca9` against base `bc741bdce7b47d3695d85fa9649fe9506f23c595`:

- `python3 scripts/test_check_bilingual_docs.py`: 27 tests, `OK`, exit 0.
- `BASE_SHA=bc741bdce7b47d3695d85fa9649fe9506f23c595 HEAD_SHA=0df6ff549386ea0ba2cbb41700f62f7a20683ca9 PR_BODY='Work Item ID: AID-2026-242; Related issue(s): #1212; AI-assisted work: YES; Session evidence reference(s): 14-ai-development/work-items/AID-2026-242/session-evidence.md; BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py`: PASS; 9 changed paths inspected; 0 new gaps; exit 0.
- `python3 scripts/check_document_management.py --require-changed bc741bdce7b47d3695d85fa9649fe9506f23c595`: PASS (incremental); no GOV-DOC-002 violations in changed paths; exit 0.
- `python3 scripts/ci/check_work_item_manifest_schema.py`: `Manifest schema v1: total=111 compliant=1 violations=110`; AID-2026-242 appears under COMPLIANT; exit 0. The 110 legacy violations are pre-existing and outside this task.
