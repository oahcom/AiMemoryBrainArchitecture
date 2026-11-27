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
        - "14-ai-development/work-items/AID-2026-113/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Verified coverage is limited to the existing source and mirror identity columns, the Owner replacement ruling, and bounded language correspondence observations. The new-blob identity columns in the two tables are explicitly excluded because their identities are not verifiable."
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
    canonical_scope: "Evidence for F Memory Runtime root restoration and Owner replacement hierarchy"
    canonical_scope_id: "ai-development/aid-2026-111-f-runtime-restore-evidence"
    canonical_scope_keywords:
      - "aid-2026-111"
      - "memory-runtime"
      - "owner-replacement"
      - "mirror-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-113/restore-evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-113/restore-evidence.md"
---
# AID-2026-113 — Restore Evidence

## Scope, authority and hierarchy

This work item restores five F Memory Runtime Canonical roots. It does not create a README. The Owner hierarchy ruling designates `05-memory-runtime/runtime-overview.md` as the explicit replacement for `05-memory-runtime/README.md`, which did not exist on any source branch.

- `source_hierarchy_decision: OWNER_REPLACEMENT`
- `replaces: 05-memory-runtime/README.md`
- `designated_root: true` on the Canonical runtime overview frontmatter
- Authority: `user-authorized operator (delegated by account owner), 2026-11-26, 代理裁决，非自然人 Owner 签署`
- F accepts retrieval semantics: `F_ACCEPTS_RETRIEVAL_SEMANTICS`
- Main baseline at preparation: `57767952f1248e2de616c5dc24ac762ecb3a5a7f`
- Source branch `session-f-memory-runtime`, head `1908ce4d233b20f7cafd00cb679affd01bd15174`

## Canonical source and new blob comparison

| Canonical path | Source blob SHA | New blob SHA | Disposition |
|---|---|---|---|
| `05-memory-runtime/activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `028bc3b63693145617290ef1b8f8cd617f931e2e` | `FRONTMATTER_ADDED`; source body retained unchanged |
| `05-memory-runtime/retrieval-engine.md` | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | `e7220ec1435430f8d4113789428bca336862916f` | `FRONTMATTER_ADDED`; source body retained unchanged |
| `05-memory-runtime/runtime-overview.md` | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` | `dd98fda4aae0fbdc837835ed44f46dbc1bf7c094` | `FRONTMATTER_ADDED`; source body retained unchanged |
| `05-memory-runtime/runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `ae879343a6871c51a42cb170d2d16fb4d34caf67` | `FRONTMATTER_ADDED`; source body retained unchanged |
| `05-memory-runtime/working-set-and-cache.md` | `a934491950c876701e8ac592a0e6aaea983b44e3` | `f5ee311573475df267d6ff5fb60180b73d6b4161` | `FRONTMATTER_ADDED`; source body retained unchanged |

All five source files had no YAML frontmatter. The new blobs consist of GOV-DOC-002 frontmatter followed by the exact source body. The metadata leaves all five documents `decision_status: Draft` and `normative_status: Informative`.

## Five EN/ZH-CN mirror pairs: old and new blob SHAs

Only frontmatter was added to the five paired Canonical mirrors; each original mirror body remains unchanged. The orphan guide pair is excluded and left byte-for-byte untouched.

| Pair | EN original blob | EN new blob | ZH-CN original blob | ZH-CN new blob |
|---|---|---|---|---|
| `activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | `43aa4de7a4549ba59b5dcd3b5e30691373e91619` | `be79b8d879121996574cbda840b435624dbe3439` | `9d66e2d9acb8755b7cf2893eec3378db86451bc3` |
| `retrieval-engine.md` | `4baa1b693b3ae2d63d28a9e6716df756d68f0815` | `2e1878d66b0e45c6bce1ddc3e557e490d97613e2` | `1225fb5c629170f05436b3cd2930c90cdf85a4bb` | `9ff6b535b8fbe8d2c21cd8fb9916137cfbc77b61` |
| `runtime-overview.md` | `8ceeff2fe450be431b106d62cc13f33a8623b474` | `ae4af4191f17e564dbabdbda4cefd71524780ba0` | `bd6346e17d049ee716e4906bb2e6b38b2cdce957` | `9e72ed4a6d502d0ab8bc7949abda51b1ac340fe6` |
| `runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | `833bebaed5847281bcbcbeb6348a0d52740b3984` | `e30535af23890145456d1ad1738f538387360ce2` | `e0f9735e8967d06936ab5f74bc44a68cda48ac99` |
| `working-set-and-cache.md` | `edabf053502279b9b1d0652c056f695210976394` | `8cce12a5a547b58c414778b45f2e741a4853d533` | `276beab4861e4f3ddd63b12dbb30b0e6b44ef551` | `4851237cd1804690a2c5c3d5d9a839ddedcb99c7` |

## Language and semantic correspondence review

- `activation-policy-engine.md`: EN mirror is byte-identical to the English Canonical source; ZH-CN is a Chinese rendering with corresponding purpose/scope/responsibility sections.
- `retrieval-engine.md`: EN mirror is not byte-identical; reviewed delta includes a cross-reference target redirected from the uncommitted Phase 3.5 contract to `docs/governance/documentation-gaps.md`. The section structure and retrieval/scope/fusion semantics align. ZH-CN headings and section structure correspond.
- `runtime-overview.md`: EN mirror adds a GAP-01 note to the Phase 3.5 cross-reference; core purpose, scope, authority boundaries and request flow align. ZH-CN headings and sections correspond.
- `runtime-scheduling.md`: EN mirror is byte-identical to the English Canonical source; ZH-CN is a corresponding Chinese rendering.
- `working-set-and-cache.md`: EN mirror is not byte-identical; reviewed delta includes a cross-reference redirected to `docs/governance/documentation-gaps.md`. Working Set/cache isolation, invalidation, Forget and version semantics align. ZH-CN headings and section structure correspond.
- No obvious `MIRROR_MISMATCH` was found in this bounded heading/cross-reference/semantic review. This is not a line-by-line certification of every translated sentence.

## Orphan mirror

`docs/en/05-memory-runtime/memory-runtime-guide.md` and `docs/zh-CN/05-memory-runtime/memory-runtime-guide.md` are marked `ORPHAN_MIRROR_PENDING_DECISION`. Their original blobs remain unchanged: EN `a45b868efe1367fb9934c17191109d8d87f48fab`; ZH-CN `0e0df43de9c55f8e41d6ed596d50471798fb23cc`. No metadata or body edits are made because there is no Canonical source for GOV-DOC-002 three-way linkage. No Canonical guide is created, and neither mirror is promoted.

## Historical source records not restored

All ten records below are classified `HISTORICAL_PHASE_RECORD` and are not restored. The source branch contains nine `phase-*` files plus `module-baseline-and-redlines.md`; all ten remain historical records, not Canonical roots.

- `05-memory-runtime/module-baseline-and-redlines.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.5-reprocessing-change-log.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.6-anti-resurrection-reference-model-evidence.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.6.4-f-prepared-participant-gid-index-boundary-acceptance.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.6.5-f-restore-reconciliation-consumer-acceptance.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md` — HISTORICAL_PHASE_RECORD; not restored.
- `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md` — HISTORICAL_PHASE_RECORD; not restored.

## Governance and acceptance boundary

- `05-memory-runtime` is added to `00-governance/document-scope-registry.yaml` and `scripts/check_bilingual_docs.py:NORMATIVE_ROOTS` so the restored Canonical root is within the declared and enforced governed scope.
- No `05-memory-runtime/README.md` or README mirror is created.
- Five Canonical docs remain Draft and Informative; the Owner hierarchy replacement is recorded as delegated authority, not natural-person signature.
- No implementation, runtime code, schema, tests, workflow, deployment, production change or Issue closure is included.

## Correction (2026-11-27)

This section is appended after the original text. No table, blob reference or claim above is edited, and the front-matter field `verification_status: Verified` is left exactly as its original author wrote it. This section records that **that declaration does not hold for the new-blob identity columns of the two tables above.**

Measured against `origin/main` (`4326669caa6c43193d34219a0451b80762b712ff`):

- The two tables carry 15 new-blob cells: 5 in "Canonical source and new blob comparison", 10 in "Five EN/ZH-CN mirror pairs".
- 15/15 fail `git cat-file -t` with `fatal: git cat-file: could not get object info` (exit 128). None of them is in the object database, so none can be the identifier of any committed version of that path.
- 0/15 equal the blob the path actually carries, on `origin/main` or at the restoring commit.
- 17/17 source, original and orphan blob SHAs in the same tables do resolve, and the five Canonical source blobs equal `1908ce4d:<path>`. The defect is confined to the new-blob column.

### C1. Every claimed new blob fails to resolve

Executed once per SHA (fifteen times, not in a loop); all fifteen print the identical message:

```
$ git cat-file -t 028bc3b63693145617290ef1b8f8cd617f931e2e
fatal: git cat-file: could not get object info
$ echo "exit=$?"
exit=128
```

| # | Claimed "New blob SHA" | `git cat-file -t` |
|---|---|---|
| 1 | `028bc3b63693145617290ef1b8f8cd617f931e2e` | exit 128 |
| 2 | `e7220ec1435430f8d4113789428bca336862916f` | exit 128 |
| 3 | `dd98fda4aae0fbdc837835ed44f46dbc1bf7c094` | exit 128 |
| 4 | `ae879343a6871c51a42cb170d2d16fb4d34caf67` | exit 128 |
| 5 | `f5ee311573475df267d6ff5fb60180b73d6b4161` | exit 128 |
| 6 | `43aa4de7a4549ba59b5dcd3b5e30691373e91619` | exit 128 |
| 7 | `9d66e2d9acb8755b7cf2893eec3378db86451bc3` | exit 128 |
| 8 | `2e1878d66b0e45c6bce1ddc3e557e490d97613e2` | exit 128 |
| 9 | `9ff6b535b8fbe8d2c21cd8fb9916137cfbc77b61` | exit 128 |
| 10 | `ae4af4191f17e564dbabdbda4cefd71524780ba0` | exit 128 |
| 11 | `9e72ed4a6d502d0ab8bc7949abda51b1ac340fe6` | exit 128 |
| 12 | `833bebaed5847281bcbcbeb6348a0d52740b3984` | exit 128 |
| 13 | `e0f9735e8967d06936ab5f74bc44a68cda48ac99` | exit 128 |
| 14 | `8cce12a5a547b58c414778b45f2e741a4853d533` | exit 128 |
| 15 | `4851237cd1804690a2c5c3d5d9a839ddedcb99c7` | exit 128 |

### C2. What the paths actually carry

`git rev-parse origin/main:<path>` is the current identity; `git rev-parse 9142698f:<path>` is the identity the restoration commit created, which is what a "New blob SHA" column would be describing.

| # | Path | Claimed new blob | `origin/main` blob | blob at `9142698f` | Equal? |
|---|---|---|---|---|---|
| 1 | `05-memory-runtime/activation-policy-engine.md` | `028bc3b6…` | `11ee1a70c7cae7c7bf64b97e0d8c879db68c6dae` | `ce15bec184f0f358d84df91987de04a70216ad41` | no |
| 2 | `05-memory-runtime/retrieval-engine.md` | `e7220ec1…` | `38fb72395166b52d8c1b0380757110ecc508cc05` | `c49c9c9272d04dddc29885c9aa0ada28d3d15e1c` | no |
| 3 | `05-memory-runtime/runtime-overview.md` | `dd98fda4…` | `80879fd3ed23b2f4545e186b8bd3626c80960c70` | `d084c463b7527e8ee364557ae941c7d19197b1d6` | no |
| 4 | `05-memory-runtime/runtime-scheduling.md` | `ae879343…` | `cfbd78e7c0381f493ac0d9cd104709b8dbbec6bf` | `05e4b4b78eda3dfa260dd95bbbaf6fc57a85f861` | no |
| 5 | `05-memory-runtime/working-set-and-cache.md` | `f5ee3115…` | `a4d8af1c59ad8fc0b118d6818928478f68fa919a` | `b6ec474256f703fb81a6b60b15ad0b453e3d5b9f` | no |
| 6 | `docs/en/05-memory-runtime/activation-policy-engine.md` | `43aa4de7…` | `cbf018fb4f2454ebbc9db1d5cc4dc05fc5269bea` | `39012b82c6ce69f0b774d2d89fcf398d5f74666b` | no |
| 7 | `docs/en/05-memory-runtime/retrieval-engine.md` | `2e1878d6…` | `e293c4704421cfaea7ff0557ea20817623e5de1e` | `12dbc2f2c811e7d61eb415ccc7f7e463c13019d2` | no |
| 8 | `docs/en/05-memory-runtime/runtime-overview.md` | `ae4af419…` | `d65c4508e2ca492f99eaf796acb5ae71f9564208` | `244a3b6ab34a3e89a2c04a213a1500516b8ad826` | no |
| 9 | `docs/en/05-memory-runtime/runtime-scheduling.md` | `833bebae…` | `c2b2b22aa8eb7447e23feca43f398c9038045069` | `ab8c4364d87f9e9f1feda7ce091c00ac4d338f67` | no |
| 10 | `docs/en/05-memory-runtime/working-set-and-cache.md` | `8cce12a5…` | `fc2b4dc78dcd2c700f2cfc8073b7dfc17be3773c` | `8cac511c3bb0213313ba63772f5d0c80f7a0be7b` | no |
| 11 | `docs/zh-CN/05-memory-runtime/activation-policy-engine.md` | `9d66e2d9…` | `f2506ece4b77e328fba23b139492f00b171fb8ed` | `b71c72eaa4e28e04e22beb1e1f8f8ac79be221b0` | no |
| 12 | `docs/zh-CN/05-memory-runtime/retrieval-engine.md` | `9ff6b535…` | `e6a2c63e1eb773566d3412467e006b9c1465e0e4` | `9ed86618decfd8538d3d4af21ea0b4df683d2fe1` | no |
| 13 | `docs/zh-CN/05-memory-runtime/runtime-overview.md` | `9e72ed4a…` | `cfb77ea85655b217bba1cd57b07b35508e9eeef0` | `f7351faf3d126f28dcb427f8c986eb4c5ac8d89a` | no |
| 14 | `docs/zh-CN/05-memory-runtime/runtime-scheduling.md` | `e0f9735e…` | `f4c5e27d6115bdc6cfb47ee39ef5423404f22cea` | `f12ed42732e195e3ff0f0a937603e1d432eb6346` | no |
| 15 | `docs/zh-CN/05-memory-runtime/working-set-and-cache.md` | `4851237c…` | `4e2772b968672590a6268f1b46dbef8ee347644a` | `7d917c6cadb983d719c135bbfc42eaf5a574a8d0` | no |

### C3. What still holds

- Each of the fifteen paths exists at `origin/main`; the five Canonical ones and their ten mirrors are present, so the restore itself is real.
- Diffing each Canonical source blob (`1908ce4d:<path>`) against the blob at `9142698f:<path>` yields 0 removed lines and only frontmatter additions (47 / 48 / 53 / 47 / 48 added lines), which is consistent with `FRONTMATTER_ADDED; source body retained unchanged`.
- What is not verifiable is the recorded identity of the new blobs: fifteen SHAs that do not exist cannot identify the fifteen restored files.

**Conclusion: `NEW_BLOB_IDENTITIES_NOT_VERIFIABLE`.** The `verification_status: Verified` declaration and its note ("Source and mirror blob identities … recorded") do not hold as written: the blob identities recorded in the new-blob column are not resolvable in this repository and do not match the files they claim to identify.
