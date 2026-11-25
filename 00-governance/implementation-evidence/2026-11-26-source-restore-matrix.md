---
document_metadata:
  domain: security-governance
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Issues #1177, #1179, #1202, #1203"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Draft execution evidence; CI, semantic mirror review and Owner acceptance pending."
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
    canonical_status: Candidate
    canonical_scope: "Evidence record for AID-2026-11-26-SOURCE-RESTORE-02"
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
---

# AID-2026-11-26-SOURCE-RESTORE-02 — Source Restore Evidence Matrix

**Baseline main:** `6314a65bd8be48c1a4bb0768e9960c4c808110ab`  
**Candidate branch:** `impl/2026-11-26-normative-source-restore`  
**D source branch:** `session-d-memory-brain-2026-11-16`  
**D source commit:** `b525e1f8fee2471a131e4a38efda99804045e424`  
**Tracking issue:** #1177

## D — exact source and final Blob matrix

| Target path | Original source Blob | Candidate final Blob | EN companion Blob | ZH-CN companion Blob | Eligibility |
|---|---|---|---|---|---|
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `3965c1e6c0810ac1850b75a6c08fb966610828e0` | `b08ac206f4fe900d9edf08877ab094984ea2e20a` | `4fb3e9f20f142bcd5c8cc206019d4f123fce68ea` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `4d7d4db0585bb2e543881758bf27a8cbb0e323fa` | `211dd4fd068e2fc0d437c2194bfce48022da302f` | `8e22726092ca3dcc84317d191c0145c1e60e5787` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | `a644e6cb31d5674614f5edab9464cc03c2d7a077` | `e7c4824e9059db137b9ccc3d5c72b0bc0b1461b6` | `bfae8e94ecd05ab17a99e58244e493317811e378` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `d3ddfff9500d9138d643989e8496d99b8d9ed79e` | `bc546ae14bba0c502d1c5af63530ba1d9ddd9a5a` | `bd173a4e174b418fa23ba41f8931dc1f9a3b632e` | BLOCKED_OWNER_REVIEW |

All four source bodies were fetched at the exact D source commit and their original Blob SHAs matched #1177. The original source body is preserved byte-for-byte; a GOV-DOC-002 metadata wrapper is prepended, so the candidate final Blob differs. Each source document records the source branch, source commit and original source Blob in `evidence_reference`.

## D — Forget Fence bilingual section set

The existing four-part EN/ZH-CN reading set is retained. Every part now points to the exact candidate source Blob `d3ddfff9500d9138d643989e8496d99b8d9ed79e`:

| Part | EN companion Blob | ZH-CN companion Blob |
|---|---|---|
| part1 | `f78b0a7880928bc51394fb35381a4ad844615e75` | `afc5b30e42eb0522a05ffa1c2ae8e372a55e2e0f` |
| part2 | `c652a3c1fb722c45b34f9468a43f910b346ac40e` | `5aa49ee75530bfc4d62ff3245ab3f38c89b56126` |
| part3 | `eff0bb4e3b5164678a24e64bc415ca5cbd5ae233` | `ac5662eb2171813b48576233cf601c8929a33996` |
| part4 | `43c5fcc92eb8d6f8ea894e91dfe668955e382252` | `e3f46487478d2e8cd86192f21cf1fd34d3a4af06` |

The companion prose was not rewritten. Only source-revision/source links were refreshed; semantic parity remains a manual reviewer control and is not claimed as mechanically proven.

## D — governance and index changes

- `scripts/check_bilingual_docs.py`: add `03-memory-brain` to `NORMATIVE_ROOTS`.
- `00-governance/document-scope-registry.yaml`: add `03-memory-brain` to `governed`.
- `03-memory-brain/README.md`: add a source index with original and candidate final Blob pins.
- `docs/en/03-memory-brain/README.md` and `docs/zh-CN/03-memory-brain/README.md`: update bilingual index companions and GOV-DOC-002 metadata.
- GOV-DOC-002 metadata is added to the four root source documents and their four EN/ZH-CN companion pairs.
- Existing Forget Fence part documents and the composite D reading guides receive exact source pointers to the new root source/index.

All D source documents and mirrors remain `decision_status: Draft`, source `canonical_status: Candidate`, mirror `canonical_status: Non-Canonical`, and `normative_status: Informative`. This PR does not assert Owner acceptance or effective normative status.

## Eligibility and dependencies

- D Owner exact-final-Blob acceptance: **BLOCKED_OWNER_REVIEW** for all four files.
- D/E/Storage cross-owner acceptance: outstanding where the document's interfaces require it.
- Canonical Memory Store INT-P0-01: **ADR-BLOCKED**; no DDL/schema is introduced.
- Forget Fence E/Storage/I enforcement and cross-module conformance: OPEN.
- Governance root registration and root-set consistency: proposed in this PR; pending CI validation and independent Governance review.

## F / I / H dispositions

| Owner | Current candidate set | Eligibility | Minimum evidence required |
|---|---|---|---|
| F | Six registered Memory Runtime candidates | BLOCKED_OWNER_REVIEW / BLOCKED_SOURCE | F Owner must resolve candidate OPEN items and accept exact final versions; source pins for all six must be confirmed; watermark must retain `scanned_through` or equivalent continuous-coverage proof and distinguish visible / irrelevant / filtered / gap |
| I | I-owned Security & Governance source set; Phase 3.6 known candidate | BLOCKED_GOVERNANCE | I Owner review plus attributable I36-GOV-01..10 governance approvals and exact dependency acceptances |
| H | H-owned BMCP core specification set | BLOCKED_OWNER_REVIEW / BLOCKED_DEPENDENCY | H Owner must publish exact core inventory and accept exact versions; required C/D/E/F/G/I joint reviews and dependency ADR closure |

No F/I/H source files are restored in this PR. The prior whole-branch merge prohibition remains in force.

## Validation status

No local shell/worktree was available. The following are **NOT RUN locally** and must be verified by PR CI or an independent checkout:

```bash
git status --short
git diff --check
git diff --stat
git diff --name-status
git diff origin/main...HEAD
git ls-tree -r HEAD
git ls-tree -r origin/main
python3 scripts/check_bilingual_docs.py
python3 scripts/check_bilingual_docs_full.py
python3 scripts/check_document_management.py
python3 scripts/check_source_revision_pointers.py
```

No file is counted as restored to main. This Draft PR is a candidate-source review package. Merge eligibility remains blocked until D Owner, relevant dependency Owners and Governance accept the exact final Blobs.
