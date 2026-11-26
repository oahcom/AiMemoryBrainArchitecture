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
    canonical_scope_id: "security-governance/source-restore-matrix"
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

| Target path | Original source Blob | Candidate final Blob | Eligibility |
|---|---|---|---|
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `9ca153df403d09264a50add8ad78bb5a6111c7c0` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `d47366d1ca04da37ff77f6edd31fe42efc93e0f9` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | `453d42592942d0508b00a4b8c5ed9320b9ced3f7` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `c6f343011a8be0fa0d4bae2659ecffc33d9557ac` | BLOCKED_OWNER_REVIEW |

## D — Forget Fence bilingual section set

The existing four-part EN/ZH-CN reading set remains unchanged. The primary EN/ZH-CN companion documents and D source index now point to the exact candidate source Blob `d3ddfff9500d9138d643989e8496d99b8d9ed79e`. The four split reading parts are retained as existing informational companions; their historical part-level source pointers are not promoted as independent mirror groups in this PR. Their prose is not rewritten.

## D — governance and index changes

- `scripts/check_bilingual_docs.py`: add `03-memory-brain` to `NORMATIVE_ROOTS`.
- `00-governance/document-scope-registry.yaml`: add `03-memory-brain` to `governed`.
- `03-memory-brain/README.md`: add a source index with original and candidate final Blob pins.
- `docs/en/03-memory-brain/README.md` and `docs/zh-CN/03-memory-brain/README.md`: update bilingual index companions and GOV-DOC-002 metadata.
- GOV-DOC-002 metadata is added to the four root source documents and their four EN/ZH-CN companion pairs.
- Existing Forget Fence part documents and composite D reading guides are preserved without content changes; primary source companions and the D index carry the exact candidate source pointers.

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

## Initial CI observations on candidate Head `5fa45e1e6944f95c3a1005715a9a598d4fbb0eaf`

- Architecture document management gate, run `45706218102` / run #1857: **SUCCESS**. The changed D sources and metadata passed GOV-DOC-002 after the scope-ID and directional mirror fixes.
- Existing gates, run `45706218053` / run #893: **SUCCESS**. Rust doctests, Rust clippy, Rust format, BMCP conformance, BMCP protocol index, bilingual coverage ratchet and schema non-empty audit all passed.
- Bilingual documentation gate, run `45706218141` / run #2492: **FAIL at execution time** because the PR body still contained `BILINGUAL-MANIFEST: PENDING`. The PR body was subsequently updated to `BILINGUAL-MANIFEST: COMPLETE`; a new exact-Head run is required before any PASS claim.
- Session Evidence gate, run `45706218102` / run #275: **FAIL** because the validator accepts only `AID-YYYY-NNN` or `NONE`, while this authorized workflow AID is `AID-2026-11-26-SOURCE-RESTORE-02`. This is retained as a blocker; no false standard ID or NO-AI declaration is substituted.
- These workflow results are not local executions of the requested shell commands. Exact-Head local `git diff` / `git ls-tree` and Python checks remain NOT RUN in this session.

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
