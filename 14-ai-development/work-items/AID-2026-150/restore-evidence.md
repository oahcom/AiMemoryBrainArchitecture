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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source Git objects, path mappings, body preservation, bilingual pairing requirements and prior classification evidence checked; Owner acceptance remains unrecorded."
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
    canonical_status: Canonical
    canonical_scope: "Evidence for bounded restoration of three D Memory Brain canonical roots"
    canonical_scope_id: "ai-development/aid-2026-150-d-root-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-150"
      - "memory-brain"
      - "canonical-root-restore"
      - "source-blob-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# AID-2026-150 — D Canonical Root Restore Evidence

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Main baseline: `17bfc43c2b9f2f9c91cb0eb074580141e701c0b3`
- INDEX blob used only for exact AID-2026-150 occupancy (not max+1): `4aad6150e3ddc22ce23bffa0b0f827375bb36e30`
- Source branch: `session-d-memory-brain-2026-11-16`; source head/tree: `b525e1f8fee2471a131e4a38efda99804045e424`
- Attribution: user-authorized operator (delegated by account owner); not a natural-person Owner signature.

## Canonical source blob comparison

| Canonical path | Source branch blob SHA | New canonical blob SHA | Body result |
|---|---|---|---|
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `e1daa858237e97c9f9972fc8a9969f1c09340790` | source body preserved byte-for-byte; GOV-DOC-002 frontmatter prepended |
| `03-memory-brain/commit-cursor-semantics.md` | `4688a0ca487bf4d853c7f0220408abe8d743d159` | `99d29021bf2a8afbdd94bb891126f2113083cb33` | source body preserved byte-for-byte; GOV-DOC-002 frontmatter prepended |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `5062b2d457ec319b10c8bc500ae2ae5a654ed44e` | source body preserved byte-for-byte; GOV-DOC-002 frontmatter prepended |

Each source path on the named D branch resolves to the exact supplied blob SHA. Each new canonical file is exactly its metadata prefix followed by the fetched source text; no source paragraph was translated, rewritten or removed.

## Existing EN/ZH-CN mirror updates

The bilingual gate requires each canonical source and both language counterparts to change together. Six existing mirror files therefore received GOV-DOC-002 metadata and only the minimum source-provenance correction. Their translated/companion body is otherwise unchanged.

| Mirror path | Previous blob | New blob |
|---|---|---|
| `docs/en/03-memory-brain/canonical-memory-store.md` | `414fe03fd40fb8ad46061d2d8c7d29ba2667f252` | `cda88579827d3253a899ee33cb3cab288958a08d` |
| `docs/en/03-memory-brain/commit-cursor-semantics.md` | `2de7fe35229372ae5b06093e5e031c2c243fbd7c` | `2687fd9a743e9c02f1c2922ff93fe683bc36d921` |
| `docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md` | `9c054932994bb078e2834df8bd66f73895aa04f5` | `1c2b174a6f60b33fd7746bfb4453edebb0b2bd06` |
| `docs/zh-CN/03-memory-brain/canonical-memory-store.md` | `34e0755a079f085df65c2a180cc59b6aaea7ea78` | `d2e3c42509f87d1099b238d67de00ba07c94ad45` |
| `docs/zh-CN/03-memory-brain/commit-cursor-semantics.md` | `2589cecb258e029c5a18796d019ad5b9806cfbdc` | `2d4f6daea751385807de5823461905f9045d7a9c` |
| `docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md` | `15c60b9a72632975f89e507520eaf32a0b9e603d` | `b2b2afa26a8e08779f3c3696555d6d9c8ce90852` |

The cursor and Fence pairs remain `ORPHAN_MIRROR_PENDING_DECISION`: these mechanical updates do not adopt the translation, grant normative authority, or resolve Owner adoption/retirement.

## Root-scope gate correction

The full-tree bilingual gate derives numbered roots from the repository tree and requires exact equality with `NORMATIVE_ROOTS`. PR #1232 encountered the missing-`03-memory-brain` mismatch and relocated its source to `01-system-architecture`. This PR keeps the requested path and adds `03-memory-brain` to both `scripts/check_bilingual_docs.py` `NORMATIVE_ROOTS` and `00-governance/document-scope-registry.yaml` `governed`. No checker logic or workflow semantics are changed.

## Remaining 57 source paths

The 57 non-root source paths are not restored. Their path-level classifications and source blob SHAs remain recorded in `14-ai-development/work-items/AID-2026-107/evidence.md` §10.4.

| Source group | Total | HISTORICAL_PHASE_RECORD | UNDECIDED |
|---|---:|---:|---:|
| Phase 3.6 | 20 | 5 | 15 |
| Phase 3.7 | 1 | 0 | 1 |
| Phase 3.8 | 25 | 22 | 3 |
| Phase 3.9 | 1 | 0 | 1 |
| Other/root-level and test paths | 10 | 2 | 8 |
| **Total** | **57** | **29** | **28** |

No `HISTORICAL_PHASE_RECORD` or `UNDECIDED` source path enters main.

## 11 orphan mirror pairs

All 11 remain `ORPHAN_MIRROR_PENDING_DECISION`; none is promoted to canonical authority or accepted as a semantic counterpart:

1. `commit-cursor-semantics.md`
2. `entity-and-relationship-manager.md`
3. `forget-fence-operation-and-publication-gate.md`
4. `forget-fence-operation-and-publication-gate-part1.md`
5. `forget-fence-operation-and-publication-gate-part2.md`
6. `forget-fence-operation-and-publication-gate-part3.md`
7. `forget-fence-operation-and-publication-gate-part4.md`
8. `memory-brain-guide.md`
9. `memory-brain-overview.md`
10. `memory-lifecycle-manager.md`
11. `memory-versioning.md`

The cursor and Fence pairs received only path/provenance corrections for structural pairing; Owner adoption/retirement remains pending. The 11 mirror pairs are separate from and not counted in the 57 source paths.

## Fence conflict determination

AID-2026-089 / PR #1232 is the existing Fence authority carrier. Its merged decision makes D the sole logical authority for ForgetOperation identity/state, target and lineage coverage, monotonic ForgetFence generation/cursor, canonical suppression and D-domain proof. Storage-local Fence rows are D-derived, rebuildable projections without independent generation/cursor or signing authority. I retains authorization and global Forget completion authority.

**Determination: CURRENT; no signer/authority conflict found.** AID-2026-089 Owner acceptance remains PENDING; normative approval NOT_CLAIMED; implementation authorization NOT_GRANTED. D operation semantics are DECIDED; implementation and cross-owner conformance remain OPEN.

## Required branch-protection contexts

1. GOV-DOC-001 structural checks
2. Branch freshness vs base
3. audit
4. GOV-DOC-002 metadata checks
5. BMCP protocol index (hard gate)
6. BMCP conformance suite (hard gate)
7. Schema non-empty audit (hard gate)
8. Bilingual docs coverage (ratchet)
9. Rust clippy (hard gate)
10. Repository hygiene (hard gate)
11. Rust format (hard gate)
12. Rust doctests (hard gate)
13. Session Evidence
14. Session Evidence self-test (base)
15. Session Evidence self-test (head)
16. rust-workspace-test

Merge only after all 16 are SUCCESS on the exact final PR head and `behind == 0`; refresh-to-merge must remain within 1–2 minutes.

## Acceptance boundary

- Exactly three canonical D source paths restored; no README added.
- 57 other D source paths not restored; 29 historical and 28 undecided.
- 11 orphan mirror pairs remain pending Owner decision.
- Canonical lifecycle remains Draft; canonical path status does not imply Owner acceptance; `normative_status: Informative`.
- No runtime/product implementation, checker logic, schema, tests, workflow, deployment, production or Issue closure.
- #1212 remains OPEN; post-merge comment will report source presence, superseded items and Gate A item 5 D status.
