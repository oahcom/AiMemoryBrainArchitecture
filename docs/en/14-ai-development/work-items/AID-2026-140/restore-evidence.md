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
        - "14-ai-development/work-items/AID-2026-140/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source, merged and corrected Git blob identities and the original exact-Head CI readback are recorded; no Owner acceptance is asserted."
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
    canonical_status: Non-Canonical
    canonical_scope: "Evidence for F Memory Runtime source restoration, fixed-range Work Item re-registration and metadata reconciliation"
    canonical_scope_id: "ai-development/aid-2026-140-f-runtime-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-140"
      - "memory-runtime"
      - "owner-replacement"
      - "blob-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-140/restore-evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-140/restore-evidence.md"
---
# AID-2026-140 — F Memory Runtime Restoration and Reconciliation Evidence

## Scope, authority and renumbering

This record carries the five F Memory Runtime Canonical roots already restored by PR #1314, but re-registers the Work Item under the account-fixed identifier **AID-2026-140**. The original concurrent carrier used AID-2026-113 and an INDEX max+1 allocation; that identifier is outside this account's assigned range and is not retained as the current Work Item ID.

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Reconciliation baseline main: `0786a3b89e060266cbd249e81f4571b9dc3f51d5`
- Original source branch: `session-f-memory-runtime`
- Source branch HEAD: `1908ce4d233b20f7cafd00cb679affd01bd15174`
- Original carrier: PR [#1314](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1314), original head `9142698fae340271e44c3a097fad0cc6455666b3`, merge commit `d6cad634f1341a8943aa89dd5ef8bf75f6d56199`
- Current Work Item: `AID-2026-140`; prior identifier retained only as historical provenance: `AID-2026-113`.
- Allocation rule: first free identifier in `AID-2026-140`–`AID-2026-149`; no INDEX max+1.
- Attribution: user-authorized operator (delegated by account owner); not a natural-person Owner signature.

The F hierarchy direction is:
- `source_hierarchy_decision: OWNER_REPLACEMENT`
- `replaces: 05-memory-runtime/README.md`
- `designated_root: true` on `05-memory-runtime/runtime-overview.md`
- exact top-level authority value: `user-authorized operator (delegated by account owner), 2026-11-26`

The original PR had used `source_hierarchy_decision_authority` with an additional suffix. This follow-up replaces that key with the exact requested `authority` field and exact value. The root's `retrieval_semantics_acceptance: F_ACCEPTS_RETRIEVAL_SEMANTICS` annotation is preserved.

## Five Canonical source blob comparisons

| Canonical path | Source branch blob | AID-113 merged-main blob | AID-140 corrected blob |
|---|---|---|---|
| `05-memory-runtime/activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `ce15bec184f0f358d84df91987de04a70216ad41` | `11ee1a70c7cae7c7bf64b97e0d8c879db68c6dae` |
| `05-memory-runtime/retrieval-engine.md` | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | `c49c9c9272d04dddc29885c9aa0ada28d3d15e1c` | `38fb72395166b52d8c1b0380757110ecc508cc05` |
| `05-memory-runtime/runtime-overview.md` | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` | `d084c463b7527e8ee364557ae941c7d19197b1d6` | `80879fd3ed23b2f4545e186b8bd3626c80960c70` |
| `05-memory-runtime/runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `05e4b4b78eda3dfa260dd95bbbaf6fc57a85f861` | `cfbd78e7c0381f493ac0d9cd104709b8dbbec6bf` |
| `05-memory-runtime/working-set-and-cache.md` | `a934491950c876701e8ac592a0e6aaea983b44e3` | `b6ec474256f703fb81a6b60b15ad0b453e3d5b9f` | `a4d8af1c59ad8fc0b118d6818928478f68fa919a` |

The five source bodies are preserved byte-for-byte. The AID-140 update changes only GOV-DOC-002 evidence references; `runtime-overview.md` additionally receives the exact top-level `authority` key/value correction. No source prose is translated or rewritten.

## Five Canonical-backed EN/ZH-CN mirror pairs

| Pair | EN original blob | EN AID-113 blob | EN AID-140 blob | ZH-CN original blob | ZH-CN AID-113 blob | ZH-CN AID-140 blob |
|---|---|---|---|---|---|---|
| `activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `39012b82c6ce69f0b774d2d89fcf398d5f74666b` | `cbf018fb4f2454ebbc9db1d5cc4dc05fc5269bea` | `be79b8d879121996574cbda840b435624dbe3439` | `b71c72eaa4e28e04e22beb1e1f8f8ac79be221b0` | `f2506ece4b77e328fba23b139492f00b171fb8ed` |
| `retrieval-engine.md` | `4baa1b693b3ae2d63d28a9e6716df756d68f0815` | `12dbc2f2c811e7d61eb415ccc7f7e463c13019d2` | `e293c4704421cfaea7ff0557ea20817623e5de1e` | `1225fb5c629170f05436b3cd2930c90cdf85a4bb` | `9ed86618decfd8538d3d4af21ea0b4df683d2fe1` | `e6a2c63e1eb773566d3412467e006b9c1465e0e4` |
| `runtime-overview.md` | `8ceeff2fe450be431b106d62cc13f33a8623b474` | `244a3b6ab34a3e89a2c04a213a1500516b8ad826` | `d65c4508e2ca492f99eaf796acb5ae71f9564208` | `bd6346e17d049ee716e4906bb2e6b38b2cdce957` | `f7351faf3d126f28dcb427f8c986eb4c5ac8d89a` | `cfb77ea85655b217bba1cd57b07b35508e9eeef0` |
| `runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `ab8c4364d87f9e9f1feda7ce091c00ac4d338f67` | `c2b2b22aa8eb7447e23feca43f398c9038045069` | `e30535af23890145456d1ad1738f538387360ce2` | `f12ed42732e195e3ff0f0a937603e1d432eb6346` | `f4c5e27d6115bdc6cfb47ee39ef5423404f22cea` |
| `working-set-and-cache.md` | `edabf053502279b9b1d0652c056f695210976394` | `8cac511c3bb0213313ba63772f5d0c80f7a0be7b` | `fc2b4dc78dcd2c700f2cfc8073b7dfc17be3773c` | `276beab4861e4f3ddd63b12dbb30b0e6b44ef551` | `7d917c6cadb983d719c135bbfc42eaf5a574a8d0` | `4e2772b968672590a6268f1b46dbef8ee347644a` |

All ten mirror bodies remain byte-for-byte unchanged. Only the Work Item evidence reference in GOV-DOC-002 metadata is re-pointed from AID-113 to AID-140.

### Bilingual correspondence findings

- `activation-policy-engine.md`: EN mirror body was byte-identical to the English source; ZH-CN headings and responsibility sections correspond.
- `retrieval-engine.md`: EN mirror has a bounded cross-reference target difference to `documentation-gaps.md`; structure and retrieval/scope/fusion semantics correspond.
- `runtime-overview.md`: EN mirror carries a GAP-01 provenance note on the Phase 3.5 reference; core purpose, scope, authority boundaries and request flow correspond.
- `runtime-scheduling.md`: EN mirror body was byte-identical to the English source; ZH-CN is the corresponding Chinese rendering.
- `working-set-and-cache.md`: EN mirror has a bounded cross-reference target difference to `documentation-gaps.md`; Working Set/cache isolation, invalidation and Forget semantics correspond.
- No obvious `MIRROR_MISMATCH` was found in the bounded heading/cross-reference/semantic review. This is not a line-by-line translation certification.

## Orphan mirror and historical source records

The `memory-runtime-guide.md` pair remains `ORPHAN_MIRROR_PENDING_DECISION`, completely untouched. Its blobs remain:
- EN: `a45b868efe1367fb9934c17191109d8d87f48fab`
- ZH-CN: `0e0df43de9c55f8e41d6ed596d50471798fb23cc`

The source branch contains nine `phase-*` files plus `module-baseline-and-redlines.md`. All ten records are classified `HISTORICAL_PHASE_RECORD` and none is restored:
- `05-memory-runtime/module-baseline-and-redlines.md`
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md`
- `05-memory-runtime/phase-3.5-reprocessing-change-log.md`
- `05-memory-runtime/phase-3.6-anti-resurrection-reference-model-evidence.md`
- `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md`
- `05-memory-runtime/phase-3.6.4-f-prepared-participant-gid-index-boundary-acceptance.md`
- `05-memory-runtime/phase-3.6.5-f-restore-reconciliation-consumer-acceptance.md`
- `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md`
- `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md`
- `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md`

No `05-memory-runtime/README.md` or README mirror exists or is created. `04-memory-compiler/compiler-stage-contract.md` is not restored; PR-C remains cancelled.

## Original carrier verification

PR #1314 was merged as `d6cad634f1341a8943aa89dd5ef8bf75f6d56199`. Its exact PR head was `9142698fae340271e44c3a097fad0cc6455666b3`, based on `57767952f1248e2de616c5dc24ac762ecb3a5a7f`. The compare result was `ahead_by=1`, `behind_by=0`.

All 16 exact-head check runs on the original carrier completed SUCCESS:
- `audit`: SUCCESS
- `rust-workspace-test`: SUCCESS
- `Rust doctests (hard gate)`: SUCCESS
- `Session Evidence self-test (head)`: SUCCESS
- `Schema non-empty audit (hard gate)`: SUCCESS
- `BMCP conformance suite (hard gate)`: SUCCESS
- `GOV-DOC-001 structural checks`: SUCCESS
- `BMCP protocol index (hard gate)`: SUCCESS
- `Session Evidence self-test (base)`: SUCCESS
- `Bilingual docs coverage (ratchet)`: SUCCESS
- `Rust format (hard gate)`: SUCCESS
- `Session Evidence`: SUCCESS
- `Repository hygiene (hard gate)`: SUCCESS
- `Branch freshness vs base`: SUCCESS
- `Rust clippy (hard gate)`: SUCCESS
- `GOV-DOC-002 metadata checks`: SUCCESS

The original closeout comment on Issue #1212 is [comment 7193607161](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7193607161). This AID-140 follow-up adds the fixed-range Work Item re-registration and exact authority-field correction; it does not close #1212.

## Governance and acceptance boundary

- `05-memory-runtime` is already present in `00-governance/document-scope-registry.yaml` and `scripts/check_bilingual_docs.py:NORMATIVE_ROOTS` from PR #1314.
- Five Canonical documents remain `decision_status: Draft` and `normative_status: Informative`.
- The OWNER_REPLACEMENT hierarchy decision is delegated operator authority, not a natural-person Owner signature or F Owner normative acceptance.
- No runtime implementation, validator, schema, tests, workflow, deployment or production change is made.
