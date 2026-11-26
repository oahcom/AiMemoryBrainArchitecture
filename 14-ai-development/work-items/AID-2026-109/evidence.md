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
        - "14-ai-development/work-items/AID-2026-109/manifest.yaml"
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
    canonical_scope: "AID-2026-109 restricted D source-root recovery evidence"
    canonical_scope_id: "ai-development/aid-2026-109-evidence"
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

# AID-2026-109 — Restricted D normative-root recovery evidence

Attribution: `user-authorized operator (delegated by account owner)`, 2026-11-26. Proxy registration only: **代理登记，非自然人 Owner 签署**.

## 1. Exact baseline and source provenance

- Main baseline fetched before branch creation: `92a759ec1a8c748fc4091015a3a3e8aa97ddc3e3`; latest main synchronization: `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`.
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
- Canonical/EN body suffix after the conflict notice is byte-identical to the source blob. The source body Git blob SHA remains `6b37c91033fda21f072e2a3bde6f274663b1e76e`.
- ZH-CN is a structural mirror based on the pre-existing translated mirror; headings are aligned to the 18 source sections (14 Performance, 15 Observability, 16 Failure, 17 Dependencies, 18 Open Questions) without changing the D source bytes.

## 5. Governance scope configuration

- `03-memory-brain` is added to `00-governance/document-scope-registry.yaml` as a governed root and to `scripts/check_bilingual_docs.py` `NORMATIVE_ROOTS`, as required by GOV-DOC-002 DM-14 and bilingual-root scope equality.
- This changes only the declared scan scope; no checker algorithm or validator semantics changed. The new root contains only the recovered canonical source in this PR.

## 6. Scope and non-claims

Documentation and work-item registration only. No runtime, validator semantics, schema, test, workflow, 04/05 source, Storage code, or Issue state changed. No D Owner acceptance, joint acceptance, wire-schema freeze, implementation conformance, production behavior, or Gate A closure is claimed. #1212 remains OPEN. The D canonical-store root presence moves from missing to **RESTORED — CANDIDATE / INFORMATIVE**; normative approval and exact Owner acceptance remain OPEN.


### 4.1 Exact blob and metadata comparison

| File | Source / prior-main blob SHA | New blob SHA | Added frontmatter blob SHA | Body treatment |
|---|---|---|---|---|
| Canonical `03-memory-brain/canonical-memory-store.md` | Source branch blob `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `1583a80211b7fa37c1d9b98d90b971810f18248f` | `1ed6b54072d5dbe2fbc9da7c969cda1a2867ed3c` | Original source bytes are the exact suffix after the mandatory conflict notice; unmodified source body blob readback reproduced the source SHA exactly. |
| EN mirror `docs/en/03-memory-brain/canonical-memory-store.md` | Prior main blob `414fe03fd40fb8ad46061d2d8c7d29ba2667f252` | `53b092af95f7e9cf36e4e9ddafa93e76f9a5f13e` | `088a9e882671f1f2c957ee1f7183c4f3d18b12f6` | Rebuilt from the exact canonical source body plus the same conflict notice to align section structure. |
| ZH-CN mirror `docs/zh-CN/03-memory-brain/canonical-memory-store.md` | Prior main blob `34e0755a079f085df65c2a180cc59b6aaea7ea78` | `41dd113497a5ad8f7cc522904a1bf855e92923ef` | `b0f28b7da314e9d2f297d64d06c73cedc83b5843` | Existing translation retained; sections 14–18 split to match canonical structure; same authority-conflict notice translated. |

The frontmatter SHA values above are Git blob SHAs of the exact added YAML frontmatter blocks (including delimiters). The source file's unmodified body, as a Git blob, hashes to `6b37c91033fda21f072e2a3bde6f274663b1e76e`, identical to the source branch blob.


### 4.2 Executed prompt snapshot

- Snapshot: `14-ai-development/work-items/AID-2026-109/prompt-v1.md`.
- SHA-256: `af29bd5b61d2a3a0d659fcfbb507111d5d7220baad5a335d4a7dca8c6e0f8462`.
- UTF-8 bytes: `2946`.
- Provenance: user prompt captured from the initiating chat; session ID itself remains NOT_RECORDED.
