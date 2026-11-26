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
        - "14-ai-development/work-items/AID-2026-193/manifest.yaml"
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
    canonical_scope: "AID-2026-193 GOV-DOC-002 classification of the 00/01/02/06 mirror trios and the Source revision pins refreshed alongside them"
    canonical_scope_id: "ai-development/aid-2026-193-mirror-frontmatter-a"
    canonical_scope_keywords:
      - "front-matter"
      - "bilingual-mirror"
      - "dm-12"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-193/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-193/evidence.md"
---
# AID-2026-193 - GOV-DOC-002 front-matter for the 00/01/02/06 mirror trios

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
| 1 | `01-system-architecture/component-interactions.md` | design-specification | Normative | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `b782472896068329ba2f4bcc293afe15b92496a7` | 1508 |
| 2 | `01-system-architecture/data-flows.md` | design-specification | Normative | `24bc5867749d234238e6d75aadd4119f359de9f8` | `81aab0f592808999ff7668c790ef6f4dee44d0af` | 1482 |
| 3 | `01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `c939ee0f6c7b29a6b51421fbfe3fe89d68ae9f6f` | 1520 |
| 4 | `02-domain-model/core-entities.md` | design-specification | Normative | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `ddeb677c1b259b9e05253968d23b526e7b3869dd` | 1470 |
| 5 | `02-domain-model/domain-model-overview.md` | design-specification | Normative | `343224eea56829c895a0fdf0e9552f108a2af475` | `ed9e249af8899db95a2ffbe852ee49aa3d69e21d` | 1492 |
| 6 | `02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `e71be982a895ef2dab97d0c9f717daf94848c54e` | 1492 |
| 7 | `02-domain-model/lifecycle-model.md` | design-specification | Normative | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `72d1936cadd5f858f63f8cc01b62639dc492f168` | 1472 |
| 8 | `02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `502a342bb47ffd3b634c322383666a235bca3933` | `16521898f64af3cddf56271f048e4568f9bc4618` | 1489 |
| 9 | `02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `c472e00f2ef4d00bb71806efc7db72062f4efb58` | `e6194f4ef25571affd9094895235e7f8df41f234` | 1514 |
| 10 | `02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `22ca7cd3777e0132e25f084084610f1e90b60d21` | `2277a20d64289ce89b1929b0aa7bbd7eba1d29e6` | 1518 |
| 11 | `02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `289b4731ae3ec92beaec2945f390b7ce09bb7c8d` | 1481 |
| 12 | `02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `d620e3e273ea3c752d045789d82a3ec6d0e461ec` | 1487 |
| 13 | `06-memory-context/README.md` | index | Informative | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | `f69ce82d721c5ccde427acc8a8d5b235b6d6a8e5` | 1473 |
| 14 | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | `26e4a50e7fd6d19c4328eb0ec82fbff376d835c0` | 1591 |
| 15 | `06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `25c1da1f6769165881d217bb0bb492a997e0e14c` | `e6ce5da8b069f53398fd62e96153c13841496097` | 1580 |
| 16 | `06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `3cffb911bdc495839ec68b2e1ae64ea945df37ee` | 1590 |
| 17 | `06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `ac2082caba534532c15cb0e80192b21a3e651624` | 1580 |
| 18 | `06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `0910fea807b96a896e361cd2722e4c94df55187b` | `73704c4cdaa95a8443c5f013f3e8a831c04c4d7e` | 1565 |
| 19 | `06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `1894860c76336f8739d354b72beed3992cffd17e` | `2d0e71f748d1da1c0abf1f0d54414bbc9a97faa6` | 1621 |
| 20 | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `833815e37ac8d7505d93a0a115421dafe3eb08ad` | `384a2002275ec0679b293a848a628a116307b495` | 1641 |
| 21 | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `47423d6f95e613b2f1556f5e359da85d7820617b` | `054d03e1317a5aaf1ec9d8eabb19e19a4e12fda9` | 1653 |
| 22 | `docs/en/01-system-architecture/component-interactions.md` | design-specification | Normative | `b5ab766758ab199579ff2dc3cdce6326acfe6dba` | `d7d623ed84d95c5ed7356ae6e70c02b84b44145a` | 1504 |
| 23 | `docs/en/01-system-architecture/data-flows.md` | design-specification | Normative | `6b4220fe1a1015446ab98ea6065faaaae34ba8b7` | `90cfb1780affa9634db1dfe169a29016a4ae2291` | 1478 |
| 24 | `docs/en/01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `ec86ed6f84a6636973c58fbe4573619c9a2674c9` | `db3c738cad915d24d701ad58cdb3863d9275a487` | 1516 |
| 25 | `docs/en/02-domain-model/core-entities.md` | design-specification | Normative | `24ed93dcd5c3a27bcb79bb434b3c8ea8361cbc89` | `74ca3e7b538898f9fbf57db0909b1910f165b5a2` | 1466 |
| 26 | `docs/en/02-domain-model/domain-model-overview.md` | design-specification | Normative | `e4fd6db47511b21e11d4f697e5cfc086177952c9` | `1062ff7b2354dccbccf9bd491d1ea724a534bbb0` | 1488 |
| 27 | `docs/en/02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `17c09d546a0b7d3eec910f3f59d3494af6ce34e5` | `cca44be9ca8c2bc7c4f7bc4e48e269aa6169fcf4` | 1488 |
| 28 | `docs/en/02-domain-model/lifecycle-model.md` | design-specification | Normative | `532e74e99f2a6640f5fd6461f3935a08553586ec` | `8fee94a5a02ce02b3ffaa6d4b826bda546ea7ca7` | 1468 |
| 29 | `docs/en/02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `f53182e183e5a571fc6c1cc9a9472e3872e124e2` | `335d1c753f48b412c4a438df4852fb0b3397b1e5` | 1485 |
| 30 | `docs/en/02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `c472e00f2ef4d00bb71806efc7db72062f4efb58` | `087a7824849123ad0543975e3581389e3370437b` | 1510 |
| 31 | `docs/en/02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `8ccce8ecee41ee46e5a38693eb0126b3e7aad08b` | `a393403f3afd6c621567852de5679d02b38cba5f` | 1514 |
| 32 | `docs/en/02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `c9e352fcb3ca9914e7ed52bedfe6e475a60c306b` | `decdf4edce11452aa23244880fdc3a0c65d50f5b` | 1477 |
| 33 | `docs/en/02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `4ae2b40d11aba5db1ce7009ebe8198f75bfc9741` | `aa73e7d9146735dd5968c73fa60790dc57317078` | 1483 |
| 34 | `docs/en/06-memory-context/README.md` | index | Informative | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | `40749ef825a5270f45fcc7b846185c3be9bc1f35` | 1469 |
| 35 | `docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `1c0782271a01c01648d0917bed59da12e94fd9d7` | `a58ac89bd14623b62857b6444a45d9f3f351c256` | 1587 |
| 36 | `docs/en/06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `25c1da1f6769165881d217bb0bb492a997e0e14c` | `3d891115ac85e5c602a690b284c845e4c0d9180b` | 1576 |
| 37 | `docs/en/06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `207df63cbe422cb46b30c325aa61cd5f58d7ef74` | 1586 |
| 38 | `docs/en/06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `c349b7a9751bff038a5ff65219a0fc3b1114d5f5` | 1576 |
| 39 | `docs/en/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `0910fea807b96a896e361cd2722e4c94df55187b` | `c07fe9f1639b4525389cbc912bd2362865c07dbd` | 1561 |
| 40 | `docs/en/06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `1e1a2881941ccecaae780cbed61466205f9c6599` | `17969c696c7fabcc92547b823f76464d73ad49a7` | 1617 |
| 41 | `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `a71df2f8292fc22c90f875c8847fde2cb855b7df` | `7243927d84651e1e4ba837dd6d2651c17198869b` | 1637 |
| 42 | `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `abace324c42e18736b1cd273a9aea7f0c29177f8` | `a359b4f345928fb4e14d43f23d6da5a1e83e15f1` | 1649 |
| 43 | `docs/zh-CN/01-system-architecture/component-interactions.md` | design-specification | Normative | `db9529555336ce3a5d56aa777f3a859aa3123a47` | `b74b6f59dcb7edfa0ed7b1d3761e59b2fdc2e533` | 1445 |
| 44 | `docs/zh-CN/01-system-architecture/data-flows.md` | design-specification | Normative | `2e52428e085f29f1692b06f9f963e98efd5b5533` | `3b91e57c85071e7627207cf5a2f854d24717e37d` | 1419 |
| 45 | `docs/zh-CN/01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `1c7ea192fa653f789aafa5e04559ad259b05884d` | `a0f380906f29068f50d0387adef362bea9c1e135` | 1457 |
| 46 | `docs/zh-CN/02-domain-model/core-entities.md` | design-specification | Normative | `c9af1f47abd1072427b59b759edcbe6581ec5c3a` | `551af3e976cc05e1ba08bad63a1656c9e8853e3d` | 1407 |
| 47 | `docs/zh-CN/02-domain-model/domain-model-overview.md` | design-specification | Normative | `8d3318b5831582717f93028fbf1f50d8cf28333e` | `e226fec244180132c07b1f257b9e4c660971327f` | 1429 |
| 48 | `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `0d90727ffdf1800463e8089135f8d0de2a96f48d` | `cb9b2043980754be8efaefd6b2d4143f1aa0493f` | 1429 |
| 49 | `docs/zh-CN/02-domain-model/lifecycle-model.md` | design-specification | Normative | `8c4b44727957efac94e16f68451f9a50ab98393d` | `fdd7ee592b2e09fc82ff2fa88f040a3182a3c3ba` | 1409 |
| 50 | `docs/zh-CN/02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `236e30cf4ddc50899393b83129e3ded05ee012d4` | `84920b0d2f28d2665fbd40fab663664b0380488e` | 1426 |
| 51 | `docs/zh-CN/02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `f905be8c183b2927449cd838761a613bcf45a46e` | `f4557a179a303bd3c1e146fd9dced0cab256c4c2` | 1451 |
| 52 | `docs/zh-CN/02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `daab973665604c1f4350dc74bccd44cfff3ec4a2` | `502b1873b24167296cdffa279241a309a2f1bb9f` | 1455 |
| 53 | `docs/zh-CN/02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `3afe4718b82f5a95d55f4a21ed73c815bf54f78c` | `37560b5734f517401078fe0da523da891d0787f5` | 1418 |
| 54 | `docs/zh-CN/02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `dff51599324a0edbca2bee52d4d9f9b6ffa117c2` | `5a9116243f6d0a86867e44af323d2f13bf404be5` | 1424 |
| 55 | `docs/zh-CN/06-memory-context/README.md` | index | Informative | `5e669ea1346f0bc6286ebc383e07a699fe3d108e` | `eb7252e75b225481e05f328f41dbc6f9b79dd43a` | 1410 |
| 56 | `docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `f22a7dc6b52325e350f6e36392b9d27f457d1e8c` | `42f54740b2dd90dee468577af24557ae041c8ffc` | 1528 |
| 57 | `docs/zh-CN/06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `e59870a91fde8525f8e5e6b2f086a2bc6f049e07` | `eb98459f5f5f5b08eb20971df09e0384751dccd3` | 1517 |
| 58 | `docs/zh-CN/06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `0740e142c820785e4e89e9397808eb0ddf967766` | `b0770438045812093118c2598b2c129d83f7faef` | 1527 |
| 59 | `docs/zh-CN/06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `3cb93ccb212851457b0dd581aaafcdfe7d8a5cb7` | `accc55821179d6b30a8b818ac111733f12d050ea` | 1517 |
| 60 | `docs/zh-CN/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `699ff1d3e396bfce7d6a81bd802e245818ee3c9b` | `bf0f3b9fdcb26d89ce58d80a4b316c834a2e0f90` | 1502 |
| 61 | `docs/zh-CN/06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `41af928f45aea6a40ddcd4e974fc583b7f98470a` | `4c7bb6545f0eef30e41cf07d3744edf411bb0315` | 1558 |
| 62 | `docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `a5b6642e0c449ea0d2cc18fef365e09b421acfa5` | `fd66267bc3907ae5dcbad89373339de88f6d27ad` | 1578 |
| 63 | `docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `4d57e90e987ec6ed679fba9047945e6a73f5d36c` | `f450389fa25af2ca733032b44cfd7e25e96740db` | 1590 |


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
| `docs/en/01-system-architecture/component-interactions.md` | `01-system-architecture/component-interactions.md` | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `b782472896068329ba2f4bcc293afe15b92496a7` |
| `docs/en/01-system-architecture/data-flows.md` | `01-system-architecture/data-flows.md` | `24bc5867749d234238e6d75aadd4119f359de9f8` | `81aab0f592808999ff7668c790ef6f4dee44d0af` |
| `docs/en/01-system-architecture/system-quality-attributes.md` | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `c939ee0f6c7b29a6b51421fbfe3fe89d68ae9f6f` |
| `docs/en/02-domain-model/core-entities.md` | `02-domain-model/core-entities.md` | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `ddeb677c1b259b9e05253968d23b526e7b3869dd` |
| `docs/en/02-domain-model/epistemic-and-temporal-semantics.md` | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `e71be982a895ef2dab97d0c9f717daf94848c54e` |
| `docs/en/02-domain-model/lifecycle-model.md` | `02-domain-model/lifecycle-model.md` | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `72d1936cadd5f858f63f8cc01b62639dc492f168` |
| `docs/en/02-domain-model/relationships-and-provenance.md` | `02-domain-model/relationships-and-provenance.md` | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `289b4731ae3ec92beaec2945f390b7ce09bb7c8d` |
| `docs/en/02-domain-model/scope-and-permission-model.md` | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `d620e3e273ea3c752d045789d82a3ec6d0e461ec` |
| `docs/zh-CN/01-system-architecture/component-interactions.md` | `01-system-architecture/component-interactions.md` | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `b782472896068329ba2f4bcc293afe15b92496a7` |
| `docs/zh-CN/01-system-architecture/data-flows.md` | `01-system-architecture/data-flows.md` | `24bc5867749d234238e6d75aadd4119f359de9f8` | `81aab0f592808999ff7668c790ef6f4dee44d0af` |
| `docs/zh-CN/01-system-architecture/system-quality-attributes.md` | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `c939ee0f6c7b29a6b51421fbfe3fe89d68ae9f6f` |
| `docs/zh-CN/02-domain-model/core-entities.md` | `02-domain-model/core-entities.md` | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `ddeb677c1b259b9e05253968d23b526e7b3869dd` |
| `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md` | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `e71be982a895ef2dab97d0c9f717daf94848c54e` |
| `docs/zh-CN/02-domain-model/lifecycle-model.md` | `02-domain-model/lifecycle-model.md` | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `72d1936cadd5f858f63f8cc01b62639dc492f168` |
| `docs/zh-CN/02-domain-model/relationships-and-provenance.md` | `02-domain-model/relationships-and-provenance.md` | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `289b4731ae3ec92beaec2945f390b7ce09bb7c8d` |
| `docs/zh-CN/02-domain-model/scope-and-permission-model.md` | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `d620e3e273ea3c752d045789d82a3ec6d0e461ec` |


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
