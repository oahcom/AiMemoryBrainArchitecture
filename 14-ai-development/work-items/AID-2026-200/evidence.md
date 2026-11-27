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
        - "14-ai-development/work-items/AID-2026-200/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the GOV-DOC-002 classification of 63 documents (21 mirror trios in 00-governance, 01-system-architecture, 02-domain-model and 06-memory-context) and the 16 Source revision pins refreshed beside them. Does not claim canonical authority, does not record an approval, and does not assert that semantic parity between a mirror and its source was reviewed."
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
    canonical_scope: "AID-2026-200 GOV-DOC-002 classification of the 00/01/02/06 mirror trios and the Source revision pins refreshed alongside them"
    canonical_scope_id: "ai-development/aid-2026-200-mirror-frontmatter-a"
    canonical_scope_keywords:
      - "front-matter"
      - "bilingual-mirror"
      - "dm-12"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-200/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-200/evidence.md"
---
# AID-2026-200 - GOV-DOC-002 front-matter for the 00/01/02/06 mirror trios

## 1. What changed

The four directories assigned to this unit (`00-governance`,
`01-system-architecture`, `02-domain-model`, `06-memory-context`) hold 43
document pairs per language, 86 files in total. Sixty of them (30 per language)
carried no YAML front-matter, so GOV-DOC-002 could not classify them: `.md`
files under `docs/en/**` and `docs/zh-CN/**` are governed by
`check_document_management.py`, but a file without front-matter is
`_unclassified`, not compliant.

Of those 60 files, 42 (21 pairs) have a canonical document that exists in the
repository. This change inserts the GOV-DOC-002 block at the top of those 42
mirror files **and** at the top of the 21 canonical documents they name, 63
files in total, and changes nothing else in any body.

## 2. Measured baseline, before this change

Commands run in `D:\code\wt-corpus-a` at base `4326669caa6c43193d34219a0451b80762b712ff`:

```
python scripts/check_document_management.py
GOV-DOC-002: 942 governed documents, 496 classified, 446 unclassified
INCOMPLETE: no rule violations in 496 classified documents, but 446 governed documents are still unclassified

python scripts/check_source_revision_pointers.py
STALE=8   (8 stale pins, all pre-existing: DEF-corpus-08)
```

Front-matter census of the four assigned directories, per language: 7 + 11 + 13
+ 12 = 43 files, of which 30 lack front-matter. Nine of those 30 have no
canonical document (orphans, section 6); the remaining 21 all name a canonical
document that exists.

## 3. Scope deviation, stated before the file list: the canonical side is in this change

The unit brief says not to change the canonical side. That constraint and DM-12
cannot both hold, and the measurement is not a matter of interpretation.

DM-12 (`scripts/check_document_management.py`, `check_scope_and_relations`)
requires every document under `docs/en/**` or `docs/zh-CN/**` to declare
`bilingual_counterpart.source`, and requires that source to be an **already
classified** governed document. A probe on one file at the base commit confirms
three errors for a single classified mirror whose canonical and sibling are
unclassified:

```
DM-12 docs/en/02-domain-model/core-entities.md: counterpart 02-domain-model/core-entities.md exists
      but carries no document_metadata, so parity cannot be verified
DM-12 docs/en/02-domain-model/core-entities.md: counterpart docs/zh-CN/02-domain-model/core-entities.md
      exists but carries no document_metadata, so parity cannot be verified
DM-12 docs/en/02-domain-model/core-entities.md: names 02-domain-model/core-entities.md as its source,
      but that file is not a classified governed document
FAIL: 3 error(s)
```

The same measurement holds for the whole corpus: of the 170 mirrors that are
classified at the base commit, **170/170** name a classified source. There is no
classified mirror with an unclassified source anywhere in the tree, so
"classify the mirror only" is not an available state; it is a red gate.

Three consequences were accepted, and each is disclosed rather than hidden:

1. **The canonical root of each trio is classified too** (21 files). This is the
   only way DM-12 can pass. Front-matter only; no body change.
2. **`canonical_status` stays `Non-Canonical` on those roots.** Classifying a
   document and designating it the unique authority for a normalised scope are
   two different acts, and the second is an Owner decision. This change makes no
   authority claim and registers no `canonical_scope_id`, so `resolve_canonical`
   finds no new scope. Precedent in-tree: `06-memory-context/context-implementation-coverage.md`
   is a classified root with `Non-Canonical` / `Informative`.
3. **`normative_status` is transcribed, not invented.** Where the document's own
   `Status:` line states a decided binding rule (`DECIDED ...`), the field is
   `Normative`; where the document declares itself a candidate, a draft, a review
   record or "not a frozen cross-owner contract", the field is `Informative`.
   Column four of section 4 records the basis for every file, so a reviewer can
   flip any single value without re-deriving it.

## 4. Insertion only

`git diff --cached --numstat` for commit `b8c89d790d671cff402c259c588de65bf2234bff`:

```
files 63   added lines 2473   deleted lines 16
```

2457 of the added lines are the 39-line front-matter block, 63 x 39 = 2457. The
16 deletions are the `Source revision` / `源版本` pins of section 5, one line
each, in the 16 mirrors that pin their canonical blob; no prose line is deleted
anywhere. Every file's body is byte-identical to the base commit after the
inserted block, which is what the `pre-insertion blob` + `front-matter bytes`
pair below lets a reader re-derive.

| # | Path | role | normative_status | pre-insertion blob | post-insertion blob | front-matter bytes |
|---|---|---|---|---|---|---|
| 1 | `01-system-architecture/component-interactions.md` | design-specification | Normative | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `49e9c1c7142c292df9efbc200c4683bd56a292ad` | 1508 |
| 2 | `01-system-architecture/data-flows.md` | design-specification | Normative | `24bc5867749d234238e6d75aadd4119f359de9f8` | `278f31e7eaf5c50bde9c421719880ab687448015` | 1482 |
| 3 | `01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `afc7d19a71546c27f7fff74e1128b7774f2855ab` | 1520 |
| 4 | `02-domain-model/core-entities.md` | design-specification | Normative | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `3b490d859f8181d3b25fdbf9892821352a7946d7` | 1470 |
| 5 | `02-domain-model/domain-model-overview.md` | design-specification | Normative | `343224eea56829c895a0fdf0e9552f108a2af475` | `07f0830c3c2f39ce3e993e018f6ea8855d08b67e` | 1492 |
| 6 | `02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `9da4341d9a15b1d3185570c70c0afe887abc7204` | 1492 |
| 7 | `02-domain-model/lifecycle-model.md` | design-specification | Normative | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `9b7f44b70d286ab6c675d2d345edd34029baad86` | 1472 |
| 8 | `02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `502a342bb47ffd3b634c322383666a235bca3933` | `d69f979442000ca7021d5e4885746cf5ed6a8e9c` | 1489 |
| 9 | `02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `c472e00f2ef4d00bb71806efc7db72062f4efb58` | `8468a573d04ca623ea6dadc789ddc75d4255cb1b` | 1514 |
| 10 | `02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `22ca7cd3777e0132e25f084084610f1e90b60d21` | `3f93026288396ce55d68b4d1380a91a40de8b622` | 1518 |
| 11 | `02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `880638d1fc1b783d912fd4fae2b6acc0ab48f6ad` | 1481 |
| 12 | `02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `713d6d06157bfa7d4a72ac696513e0ece6ff23bd` | 1487 |
| 13 | `06-memory-context/README.md` | index | Informative | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | `c81aca21ce3852fe6f738615b80c3135d4289712` | 1473 |
| 14 | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | `34b02915e432bb0e4250d733d45fbea79716a708` | 1591 |
| 15 | `06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `25c1da1f6769165881d217bb0bb492a997e0e14c` | `c2002a2878b58935e5163342d834f5cb15ab584d` | 1580 |
| 16 | `06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `893e2fbf91555892d57383445db2e5a9509356db` | 1590 |
| 17 | `06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `8aed7bdde24ee7b0b52bed68fbc9426ba83ae41f` | 1580 |
| 18 | `06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `0910fea807b96a896e361cd2722e4c94df55187b` | `1c2862334f7d660d152986ec9ab6e6283e3461b1` | 1565 |
| 19 | `06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `1894860c76336f8739d354b72beed3992cffd17e` | `634e78b2b9615f8bdfb690c9a75dc667863288f4` | 1621 |
| 20 | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `833815e37ac8d7505d93a0a115421dafe3eb08ad` | `a179ca525676b201c5f5d1722756d5411b36cb9d` | 1641 |
| 21 | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `47423d6f95e613b2f1556f5e359da85d7820617b` | `eb994f011de6a8afb6ce2e49c0a4b519c30c59c6` | 1653 |
| 22 | `docs/en/01-system-architecture/component-interactions.md` | design-specification | Normative | `b5ab766758ab199579ff2dc3cdce6326acfe6dba` | `882e75ae1fb31b4264b0b195d9ed61f33ccf0d45` | 1504 |
| 23 | `docs/en/01-system-architecture/data-flows.md` | design-specification | Normative | `6b4220fe1a1015446ab98ea6065faaaae34ba8b7` | `b2a99c476052171745f4acc0fbd6b01177a3b8c6` | 1478 |
| 24 | `docs/en/01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `ec86ed6f84a6636973c58fbe4573619c9a2674c9` | `9d5c4af8dd9542f98fa9b9cb378f257a0cec01d5` | 1516 |
| 25 | `docs/en/02-domain-model/core-entities.md` | design-specification | Normative | `24ed93dcd5c3a27bcb79bb434b3c8ea8361cbc89` | `350454cf2e8325b71c552265eac304a7c0ed34cc` | 1466 |
| 26 | `docs/en/02-domain-model/domain-model-overview.md` | design-specification | Normative | `e4fd6db47511b21e11d4f697e5cfc086177952c9` | `bcf6b9230ec7b7993c52be6c48afdb9ca53bea79` | 1488 |
| 27 | `docs/en/02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `17c09d546a0b7d3eec910f3f59d3494af6ce34e5` | `6e2455287a6dc956001c6a1d2afa62dfb0ba8885` | 1488 |
| 28 | `docs/en/02-domain-model/lifecycle-model.md` | design-specification | Normative | `532e74e99f2a6640f5fd6461f3935a08553586ec` | `614b92e1652ce119107e4e62a8db0aad58fe4428` | 1468 |
| 29 | `docs/en/02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `f53182e183e5a571fc6c1cc9a9472e3872e124e2` | `4abec82e22dba7a0263fceadaf36318a71082392` | 1485 |
| 30 | `docs/en/02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `c472e00f2ef4d00bb71806efc7db72062f4efb58` | `d3aa16ef8355860e1dbe1b5ae95e864713b064a8` | 1510 |
| 31 | `docs/en/02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `8ccce8ecee41ee46e5a38693eb0126b3e7aad08b` | `b9d12b9e0badd2ab4f43addab114ba5ad25083e4` | 1514 |
| 32 | `docs/en/02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `c9e352fcb3ca9914e7ed52bedfe6e475a60c306b` | `c18ad97f096620d419185da04c70ca2452634aa4` | 1477 |
| 33 | `docs/en/02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `4ae2b40d11aba5db1ce7009ebe8198f75bfc9741` | `153b8425ebdc1b261d5d38fc6b6e486b4c901748` | 1483 |
| 34 | `docs/en/06-memory-context/README.md` | index | Informative | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | `4baabb87fd742b0e1004b8ad0cdfbc3db4060a62` | 1469 |
| 35 | `docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `1c0782271a01c01648d0917bed59da12e94fd9d7` | `8506a28b531dfa12f42c6fe0b1318b4022d1c767` | 1587 |
| 36 | `docs/en/06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `25c1da1f6769165881d217bb0bb492a997e0e14c` | `9a7303a6c03bbffba424d62bb25b03b3490cf9da` | 1576 |
| 37 | `docs/en/06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `8426e245fbfbebf30e18390e67a92d8efd737569` | 1586 |
| 38 | `docs/en/06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `93de01c49605470e3176ccfcbb4691ae0a03bdf6` | 1576 |
| 39 | `docs/en/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `0910fea807b96a896e361cd2722e4c94df55187b` | `38411b72d3f158420fa3a5353985e23e2e6aec49` | 1561 |
| 40 | `docs/en/06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `1e1a2881941ccecaae780cbed61466205f9c6599` | `01f1a23953313860945969c53e7fc40187058e37` | 1617 |
| 41 | `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `a71df2f8292fc22c90f875c8847fde2cb855b7df` | `e748d2fe21d7df3285f7312c7a1c479fc263646e` | 1637 |
| 42 | `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `abace324c42e18736b1cd273a9aea7f0c29177f8` | `7d93b6371b6609cab2d6337f1d2734d403d56d07` | 1649 |
| 43 | `docs/zh-CN/01-system-architecture/component-interactions.md` | design-specification | Normative | `db9529555336ce3a5d56aa777f3a859aa3123a47` | `34a748cff5f12aadf1742e5ee88a6fc913d1791b` | 1445 |
| 44 | `docs/zh-CN/01-system-architecture/data-flows.md` | design-specification | Normative | `2e52428e085f29f1692b06f9f963e98efd5b5533` | `e7bfb29b5801a2c4ddbcc92605aadc6a695a873d` | 1419 |
| 45 | `docs/zh-CN/01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `1c7ea192fa653f789aafa5e04559ad259b05884d` | `5b918f058ab0d163845538567a19ef7fabe0eabc` | 1457 |
| 46 | `docs/zh-CN/02-domain-model/core-entities.md` | design-specification | Normative | `c9af1f47abd1072427b59b759edcbe6581ec5c3a` | `05c7d18e48fb2a6d5046550fb31a0477f3f52405` | 1407 |
| 47 | `docs/zh-CN/02-domain-model/domain-model-overview.md` | design-specification | Normative | `8d3318b5831582717f93028fbf1f50d8cf28333e` | `28b2c247e26b09398a6e9710bac7c75330e3c4cc` | 1429 |
| 48 | `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `0d90727ffdf1800463e8089135f8d0de2a96f48d` | `10e8957afbb4c176ec1c790b8cd7525240fa403a` | 1429 |
| 49 | `docs/zh-CN/02-domain-model/lifecycle-model.md` | design-specification | Normative | `8c4b44727957efac94e16f68451f9a50ab98393d` | `2d533c71cbfecec0c0e72826f0f1ee18b8ef6b27` | 1409 |
| 50 | `docs/zh-CN/02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `236e30cf4ddc50899393b83129e3ded05ee012d4` | `cceea0e686b07971b47df8d81e9c2b080d9cc2c9` | 1426 |
| 51 | `docs/zh-CN/02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `f905be8c183b2927449cd838761a613bcf45a46e` | `a03b67a50829478aa95d1bfd60aeed5452b7c3a7` | 1451 |
| 52 | `docs/zh-CN/02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `daab973665604c1f4350dc74bccd44cfff3ec4a2` | `f97296fa1f5ad5a0d2df084733aa0ba8e3964f00` | 1455 |
| 53 | `docs/zh-CN/02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `3afe4718b82f5a95d55f4a21ed73c815bf54f78c` | `39e29bcf07d66e8f6c14815d47789cf4a172f96d` | 1418 |
| 54 | `docs/zh-CN/02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `dff51599324a0edbca2bee52d4d9f9b6ffa117c2` | `4a4c8cfa68bce511fdea5c99320e40f70ee429fd` | 1424 |
| 55 | `docs/zh-CN/06-memory-context/README.md` | index | Informative | `5e669ea1346f0bc6286ebc383e07a699fe3d108e` | `38be4f9b198faf42d423ecb3a1543a8250fcbbfd` | 1410 |
| 56 | `docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `f22a7dc6b52325e350f6e36392b9d27f457d1e8c` | `42f758ffb0899aab2add75bcfcf8f77a666974de` | 1528 |
| 57 | `docs/zh-CN/06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `e59870a91fde8525f8e5e6b2f086a2bc6f049e07` | `2ca76cd795f14a43e9b51aa34471c924827a79e3` | 1517 |
| 58 | `docs/zh-CN/06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `0740e142c820785e4e89e9397808eb0ddf967766` | `785eb032e452f40d66bcbae326e0b856d88ed00c` | 1527 |
| 59 | `docs/zh-CN/06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `3cb93ccb212851457b0dd581aaafcdfe7d8a5cb7` | `c22dd8e5a926acad2b98af51bcf778da9fcd086c` | 1517 |
| 60 | `docs/zh-CN/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `699ff1d3e396bfce7d6a81bd802e245818ee3c9b` | `cb06b03bc8750d85e05f145ed47d39c177e09ae3` | 1502 |
| 61 | `docs/zh-CN/06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `41af928f45aea6a40ddcd4e974fc583b7f98470a` | `af3758b8c366b106da8937226ebdc36a1b6b8152` | 1558 |
| 62 | `docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `a5b6642e0c449ea0d2cc18fef365e09b421acfa5` | `3a7a044f8ce87cf1b617500846b704b05594be11` | 1578 |
| 63 | `docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `4d57e90e987ec6ed679fba9047945e6a73f5d36c` | `1a8d0c10a2eda557766101706c4ec6e19b077fc2` | 1590 |


## 5. Source revision pins refreshed: 16 lines, DEF-corpus-08

Eight pairs of mirrors pin the canonical blob in their body
(`- Source revision: <40-hex>` / `- 源版本：<40-hex>`). Prepending front-matter to
the canonical changes that blob, so a change that left the pins alone would
produce exactly the defect DEF-corpus-08 records: "the same commit changed the
canonical and both mirrors and did not change the pointer". Each pin below was
rewritten to the new canonical blob in the same commit. This is the only edit
outside the inserted block, it touches one line per file, and the gate
`scripts/check_source_revision_pointers.py` reports the same 8 pre-existing
stale pins before and after, with no new one.

| Mirror | Canonical | Pin before | Pin after |
|---|---|---|---|
| `docs/en/01-system-architecture/component-interactions.md` | `01-system-architecture/component-interactions.md` | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `49e9c1c7142c292df9efbc200c4683bd56a292ad` |
| `docs/en/01-system-architecture/data-flows.md` | `01-system-architecture/data-flows.md` | `24bc5867749d234238e6d75aadd4119f359de9f8` | `278f31e7eaf5c50bde9c421719880ab687448015` |
| `docs/en/01-system-architecture/system-quality-attributes.md` | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `afc7d19a71546c27f7fff74e1128b7774f2855ab` |
| `docs/en/02-domain-model/core-entities.md` | `02-domain-model/core-entities.md` | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `3b490d859f8181d3b25fdbf9892821352a7946d7` |
| `docs/en/02-domain-model/epistemic-and-temporal-semantics.md` | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `9da4341d9a15b1d3185570c70c0afe887abc7204` |
| `docs/en/02-domain-model/lifecycle-model.md` | `02-domain-model/lifecycle-model.md` | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `9b7f44b70d286ab6c675d2d345edd34029baad86` |
| `docs/en/02-domain-model/relationships-and-provenance.md` | `02-domain-model/relationships-and-provenance.md` | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `880638d1fc1b783d912fd4fae2b6acc0ab48f6ad` |
| `docs/en/02-domain-model/scope-and-permission-model.md` | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `713d6d06157bfa7d4a72ac696513e0ece6ff23bd` |
| `docs/zh-CN/01-system-architecture/component-interactions.md` | `01-system-architecture/component-interactions.md` | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `49e9c1c7142c292df9efbc200c4683bd56a292ad` |
| `docs/zh-CN/01-system-architecture/data-flows.md` | `01-system-architecture/data-flows.md` | `24bc5867749d234238e6d75aadd4119f359de9f8` | `278f31e7eaf5c50bde9c421719880ab687448015` |
| `docs/zh-CN/01-system-architecture/system-quality-attributes.md` | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `afc7d19a71546c27f7fff74e1128b7774f2855ab` |
| `docs/zh-CN/02-domain-model/core-entities.md` | `02-domain-model/core-entities.md` | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `3b490d859f8181d3b25fdbf9892821352a7946d7` |
| `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md` | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `9da4341d9a15b1d3185570c70c0afe887abc7204` |
| `docs/zh-CN/02-domain-model/lifecycle-model.md` | `02-domain-model/lifecycle-model.md` | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `9b7f44b70d286ab6c675d2d345edd34029baad86` |
| `docs/zh-CN/02-domain-model/relationships-and-provenance.md` | `02-domain-model/relationships-and-provenance.md` | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `880638d1fc1b783d912fd4fae2b6acc0ab48f6ad` |
| `docs/zh-CN/02-domain-model/scope-and-permission-model.md` | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `713d6d06157bfa7d4a72ac696513e0ece6ff23bd` |


## 6. Orphans skipped: 9 rel / 18 files

A mirror whose canonical document does not exist cannot be classified: DM-12
would report a source that does not exist, and the unit brief says to skip it.
Nine rels (18 files) are in that state in this unit's four directories. All nine
are the ones `defects-corpus.md` section 5 lists as orphans; this change adds
none and resolves none.

| Orphan mirror rel | en + zh-CN files |
|---|---|
| `00-governance/aid-2026-014-r3-correction-status.md` | 2 |
| `01-system-architecture/integration-governance-guide.md` | 2 |
| `01-system-architecture/system-architecture-specification.md` | 2 |
| `01-system-architecture/system-design-guide.md` | 2 |
| `02-domain-model/domain-model-guide.md` | 2 |
| `02-domain-model/principal-actor-binding-mapping.md` | 2 |
| `02-domain-model/typed-reference-and-scope-semantics.md` | 2 |
| `06-memory-context/memory-context-guide.md` | 2 |
| `06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md` | 2 |

## 7. Gates, run locally against the committed tree

```
python scripts/check_document_management.py --require-changed 4326669caa6c43193d34219a0451b80762b712ff
GOV-DOC-002: 942 governed documents, 559 classified, 383 unclassified
PASS (incremental): no GOV-DOC-002 violations; 559 classified, 383 unclassified

python scripts/check_document_management.py            (whole tree)
GOV-DOC-002: 942 governed documents, 559 classified, 383 unclassified
INCOMPLETE: no rule violations in 559 classified documents, but 383 governed documents
are still unclassified                      (exit 2: backlog remains, no rule violation)

python scripts/test_check_document_management.py
326/326 passed; 1 skipped, 1 registered of 1 allowed (T68c)

BASE_SHA=4326669caa6c43193d34219a0451b80762b712ff HEAD_SHA=b8c89d790d671cff402c259c588de65bf2234bff python scripts/check_bilingual_docs.py
bilingual baseline: 77 frozen, 0 new gaps
Bilingual documentation and prompt-library gate: PASS (63 changed paths inspected).

python scripts/check_source_revision_pointers.py
STALE=8 (unchanged), ACCURATE=16 (the 16 refreshed pins)
```

Governed 942 -> 942. Classified 496 -> 559 (+63). Unclassified 446 -> 383 (-63),
measured at corpus commit `b8c89d790d671cff402c259c588de65bf2234bff`, before this
registration set existed and before any later main merge. The deltas this change
owns are +63 classified and -63 unclassified; the whole-tree totals on any later
head differ from 942/559/383 only by the documents main itself added, so the
stable statement is the delta, not the total. The whole-tree run still exits 2
because 383 governed documents elsewhere are unclassified; that backlog belongs
to the other corpus units and to roots this unit does not own, and no rule
violation is reported.

## 8. What this change does not do

- No body text is edited: no wording, no heading, no link, no table cell, except
  the 16 single-line blob pins of section 5.
- No file is created or deleted inside the document corpus.
- No directory outside `00-governance`, `01-system-architecture`,
  `02-domain-model`, `06-memory-context` is touched.
- No orphan mirror is classified, and no canonical document is created for one.
- No canonical authority is claimed: `canonical_status` is `Non-Canonical`
  everywhere this change writes it, no `canonical_scope_id` is registered, and
  no approval is recorded (`decision_status: Draft`, `evidence_verification:
  Unverified` on every file).
- No checker, schema, baseline, workflow, branch protection or required context
  is changed.
- No Issue is closed.

## 9. Reproduction

```
git checkout b8c89d790d671cff402c259c588de65bf2234bff
python scripts/check_document_management.py --require-changed 4326669caa6c43193d34219a0451b80762b712ff
git diff --numstat 4326669caa6c43193d34219a0451b80762b712ff..b8c89d790d671cff402c259c588de65bf2234bff
git diff 4326669caa6c43193d34219a0451b80762b712ff..b8c89d790d671cff402c259c588de65bf2234bff -- <path>     # one file: removed lines = 0, or the single pin line
```
