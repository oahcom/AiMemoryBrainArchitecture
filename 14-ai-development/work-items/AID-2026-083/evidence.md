---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: {scheme: git, value: null}
      approval_scope: {type: Full-document, included_sections: [], included_assets: []}
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: ["AID-2026-083", "PR #1220", "PR #1219", "2026-11-26 delegated authorization"]
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "GitHub tree/blob evidence read back; independent Owner acceptance and final exact-Head CI remain pending."
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
    canonical_scope: "SOURCE-RESTORE-02 execution evidence and Gate A mirror-derived reconstruction ledger"
    canonical_scope_id: "ai-development/source-restore-02"
    canonical_scope_keywords: ["source-restoration", "mirror-reconstruction", "blob-provenance", "work-item-registration"]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-083 — SOURCE-RESTORE-02 execution evidence

**Attribution:** `user-authorized operator (delegated by account owner)`  
**Date:** 2026-11-26  
**Carrier:** [PR #1220](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1220)  
**Repository:** `oahcom/AiMemoryBrainArchitecture`

This is a Stage 0 evidence record. It does not constitute Owner acceptance, source authority, Normative approval, merge approval, deployment authorization, or Issue closure.

## 1. Baseline and bounded identifier allocation

| Observation | Exact value |
|---|---|
| Current main at reconciliation | `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8` |
| PR #1220 head before reconciliation | `afbbbf6098bb1318093d9d3b26c4b1ccb0d2d5e9` |
| PR #1220 base at readback | `dcf9a6348ce5b0802e79f3a3f9c497109f0fb4a8` |
| Merge base | `dcf9a6348ce5b0802e79f3a3f9c497109f0fb4a8` |
| AID-2026-083 in current main | NOT_FOUND |
| AID-2026-083 in PR #1220 head | NOT_FOUND |
| Branch-name search for AID-2026-083 | NO RESULT |
| Exhaustive content scan of every active branch | NOT COMPLETED |

AID-2026-083 is allocated after checking current main, the target PR head, and branch-name search results. Global branch-content uniqueness is **NOT_FULLY_VERIFIED**; no exhaustive recursive scan of every active branch is claimed.

## 2. AID identity repair

### AID-2026-080 — original identity restored

- Restored the mainline manifest unchanged: `14-ai-development/work-items/AID-2026-080/manifest.yaml`, blob `c58f0b6761b7ee40cfa90a1ecc2a027a7240a490`.
- Restored the mainline prompt snapshot unchanged: `14-ai-development/work-items/AID-2026-080/prompt-v1.md`, blob `84342823a31a47fdad048e931314b0f0d8e6ca92`.
- Preserved the current main INDEX row for the original Issue #1201 work item, including its current merged-carrier status.
- The SOURCE-RESTORE-02 manifest and prompt that had occupied the AID-080 path on the PR branch were moved to AID-2026-083. The old AID-080 `session-evidence-source-restore.md` path is removed after its record is carried forward under AID-2026-083.

### AID-2026-081 — duplicate registration removed

- Restored the current mainline manifest unchanged: `14-ai-development/work-items/AID-2026-081/manifest.yaml`, blob `35658907734290f1aa8d472a8e0d3f9215620a9b`. Its identity is the existing GOV-DOC-001 ratchet / Issue #1081 work item.
- Preserved the corresponding mainline INDEX row.
- Removed the PR #1220-side DECISION-ACCEPTANCE-03 manifest and its duplicate INDEX row. No AID-081 identity is reassigned.

**Important current-state correction:** the user instruction referred to PR #1219's AID-081. The current PR #1219 body and manifest now identify DECISION-ACCEPTANCE-03 as **AID-2026-086**, not AID-2026-081. Current PR #1219 head: `590ddcb5f2f3a78f74dee5d33f4b3c82888d8e10`; its AID-086 manifest blob is `9e147ee0746f58d717eb4e0d42dd973d4f3fbcaf`. The older AID-081 declaration is superseded. This evidence therefore references **PR #1219 / AID-2026-086** as the current decision-acceptance carrier and records AID-081 only as the historical stale reference. The AID-081 path in main remains Issue #1081.

### AID-2026-082 — unchanged

- Manifest: `14-ai-development/work-items/AID-2026-082/manifest.yaml`, blob `a97beb77b76ed5249d0f23f4af07b7ca7a8a4e19`.
- Evidence: `14-ai-development/work-items/AID-2026-082/evidence.md`, blob `56f3305e58d17403d082ae72a311c8a98d527e69`.
- Its manifest, evidence, and registration identity are not modified by this repair. Its existing INDEX row is carried forward unchanged.

### AID-2026-083 — new registration

- New Stage 0 registration: `14-ai-development/work-items/AID-2026-083/manifest.yaml`.
- Evidence: this file.
- Historical task-specific prompt capture: `14-ai-development/work-items/AID-2026-083/prompt-v1.md`; original input hash `6f74f728dfa47141ebee108c462e7e853983f1700e91e25c8f98a7b47ec07a95`, 2130 bytes. Complete effective prompt remains NOT_VERIFIED.
- Session evidence: `14-ai-development/work-items/AID-2026-083/session-evidence-source-restore.md`; stable platform session identifier remains NOT_AVAILABLE.

## 3. Gate A — three RECONSTRUCTED roots

The three root paths below had no authoritative root-source blob in their enumerated Owner branch. Their bodies were reconstructed from existing EN mirror bodies. **These are RECONSTRUCTED, not RESTORED.** The EN mirror blob is evidence of the reconstruction input, not an authoritative source blob.

| Root path | New root blob | Existing EN mirror (source blob) | Existing ZH-CN mirror (comparison blob) | Owner branch checked |
|---|---|---|---|---|
| `04-memory-compiler/compiler-stage-contract.md` | `ed0f75e6a9382ee47676d5a45ec47eee8fb42a7e` | `docs/en/04-memory-compiler/compiler-stage-contract.md` — `6d733294232a93aa59123009d2a2801d9b83f459` | `docs/zh-CN/04-memory-compiler/compiler-stage-contract.md` — `ad386cac5636b4ba3eaf8b93ad93afcb444e8b46` | E `session-e-memory-compiler-2026-11-16` @ `ee098e14747d9915de5b3efb63b3a8dd77f670ed` |
| `05-memory-runtime/README.md` | `6a76cdba65088610d248717027ab17c0c4d19447` | `docs/en/05-memory-runtime/memory-runtime-guide.md` — `a45b868efe1367fb9934c17191109d8d87f48fab` | `docs/zh-CN/05-memory-runtime/memory-runtime-guide.md` — `0e0df43de9c55f8e41d6ed596d50471798fb23cc` | F `session-f-memory-runtime` @ `1908ce4d233b20f7cafd00cb679affd01bd15174` |
| `09-security-governance/README.md` | `939dd364a98d8a08dd31b53643d6658c36fe0f18` | `docs/en/09-security-governance/security-governance-guide.md` — `061c5847b3df879eeaf3c71e5eae0bfa162b276a` | `docs/zh-CN/09-security-governance/security-governance-guide.md` — `372d27c79dc79d09bcdb0f142c979efdba1c2b6e` | I `session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6` |

Exact-name EN/ZH-CN mirror paths were also created or metadata-updated for the three root documents so that each root has a paired path. These mirror blobs are:

| Pair | EN mirror blob | ZH-CN mirror blob |
|---|---|---|
| Compiler Stage Contract | `676630eb6ebed63c00a79d86dfb4159b093a46c0` | `b7ec5543cc5bec60057d5dee9736a3e64d56ad03` |
| Memory Runtime README | `08b26d63c9764c9ff764bb33ef2394955e5ff151` | `18c6db7614e1c29f459fc05d59b8b04b5ebe3bb2` |
| Security Governance README | `16e0e24c151602239cc3d1f88a4c31c130838563` | `1c093c0b531484a17280b966e8f019819245cbe2` |

Each reconstructed root has a top-of-document **Reconstruction notice**, status **Draft / Candidate / Informative**, and the exact provenance marker `RECONSTRUCTED_FROM_MIRROR`. No file is marked Approved or Normative. Relative links were adjusted only where the root location differs from the source mirror location.

**Metadata parser constraint:** GOV-DOC-002's current parser has a closed `document_metadata` key set and rejects unknown keys. To avoid changing validator semantics, each root records `# provenance: RECONSTRUCTED_FROM_MIRROR` in YAML frontmatter and repeats the exact provenance marker in the allowed `lifecycle.approval.evidence_reference` field. This is paired with the structured provenance records in this manifest and evidence ledger; no validator schema or parser change was made.

## 4. ZH-CN semantic alignment review

The existing ZH-CN bodies were compared against the pinned EN bodies. The review found no material semantic divergence in the examined requirements, boundaries, or status qualifications.

| Pair | Structural parity observed | Result |
|---|---|---|
| Compiler Stage Contract | Same section/subsection headings, 34 table rows, 29 numbered items, 132 bullets, 2 fenced blocks | No material divergence identified |
| Memory Runtime Guide | 11 numbered sections, 9 table rows, 25 bullets, 2 fenced blocks on both sides | No material divergence identified |
| Security Governance Guide | 12 numbered sections, 15 table rows, 30 numbered items, 33 bullets on both sides | No material divergence identified |

This is an implementation-session comparison, not domain Owner acceptance or an independent semantic review. Exact-version Owner acceptance remains pending.

## 5. RESTORED source-backed material — kept separate from RECONSTRUCTED

The following source-backed candidates are carried forward as **RESTORED** from exact Owner-branch source blobs. Their existing candidate status is not promoted by this record.

### D — 4 RESTORED roots

| Root path | Exact D source blob |
|---|---|
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` |
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |

### E — 5 RESTORED roots (5/25)

| Root path | Exact E source blob |
|---|---|
| `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` | `5ca77a5b48e69afb3bc81429baf538be7dce4d46` |
| `04-memory-compiler/compiler-state-and-producer-admission.md` | `e59f517fff161ab882aa0ddc4a5bda513964ae1a` |
| `04-memory-compiler/consolidation-and-conflict-resolution.md` | `d16f8e2e41a6cca81ad285e5f79f075d87e64edb` |
| `04-memory-compiler/event-ingestion-engine.md` | `9fa3db53175452bf9e6f0fce8b1540765e46905f` |
| `04-memory-compiler/evidence-and-provenance.md` | `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` |

Two additional E roots already existed on main and were not overwritten. The other 18/25 inventory entries still lack an existing EN/ZH-CN pair and remain blocked.

### F — 5 RESTORED roots (5/15 represented)

| Root path | Exact F source blob |
|---|---|
| `05-memory-runtime/runtime-overview.md` | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` |
| `05-memory-runtime/activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` |
| `05-memory-runtime/retrieval-engine.md` | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` |
| `05-memory-runtime/runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` |
| `05-memory-runtime/working-set-and-cache.md` | `a934491950c876701e8ac592a0e6aaea983b44e3` |

The other 10/15 F inventory entries lack existing EN/ZH-CN pairs and remain blocked. The three Gate A reconstructions above are not counted as F source restorations. No additional E/F candidate met the requested “exact source blob plus existing bilingual mirror” priority rule in this pass.

**Accounting:** RESTORED = 14 source-backed roots (D 4 + E 5 + F 5); RECONSTRUCTED = 3 Gate A roots. These categories are separate and must not be summed into a source-restoration count.

## 6. Validator, runtime, and governance boundaries

- No runtime/product code was modified.
- No executable validator implementation was modified. The PR branch's prior `scripts/check_bilingual_docs.py` NORMATIVE_ROOTS delta was not carried into the reconciled tree; the file is kept at current main's version.
- `manifest-schema-registry.yaml` is updated as per-record classification data: the obsolete Stage 0 exclusions for restored normal Work Items AID-080 and AID-081 are removed, AID-082 remains classified as Stage 0, and AID-083 is registered as Stage 0. No parser or validator logic is changed.
- AID-082 manifest and evidence content remain unchanged.
- No PR merge, Issue closure, deployment, schema/API implementation, or Owner acceptance is performed or inferred.

## 7. Remaining blockers

1. PR #1220 must be synchronized with current main and exact-Head CI must be observed after the resulting PR synchronize event.
2. The three reconstructed Gate A roots have no authoritative root-source blobs; they remain Draft/Candidate/Informative pending domain Owner review and exact-version acceptance.
3. PR #1219's current decision-acceptance Work Item is AID-086. The earlier AID-081 reference is stale; its current AID-086 scope/acceptance remains pending as recorded by PR #1219.
4. E has 18 remaining source candidates without existing EN/ZH-CN pairs; F has 10. New source-backed restorations require exact source blobs and faithful bilingual mirrors.
5. F watermark/scanned-through proof and E/F Owner exact-version acceptance remain pending.
6. I36-GOV-01..10 remain GOVERNANCE-BLOCKED; no I Owner approval evidence or effective policy version/time is supplied.
7. Global AID uniqueness across all active branch contents was not exhaustively scanned.
8. Independent review and all applicable exact-Head CI conclusions remain pending.

## 8. Explicit non-claims

- No claim that reconstructed roots are recovered authoritative source documents.
- No claim of Approved, Normative, production-ready, or Owner-accepted status.
- No claim that the 14 RESTORED source-backed roots are accepted by their domain Owners.
- No claim that AID-083 is globally unique across every historical or active branch.
- No claim that PR #1220 is merged or that any Issue is closed.
