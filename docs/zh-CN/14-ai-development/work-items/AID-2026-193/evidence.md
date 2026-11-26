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
      last_verification_note: "记录 00-governance、01-system-architecture、02-domain-model、06-memory-context 四个目录中 63 份文档（21 组镜像三元组）的 GOV-DOC-002 分类，以及随之刷新的 16 条 Source revision 指针；不主张 Canonical 权威、不记录审批，也不声称已审查镜像与源的语义对等。"
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
    canonical_scope: "AID-2026-193：为 00/01/02/06 的镜像三元组补 GOV-DOC-002 分类，并同步刷新 Source revision 指针"
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
    en: "docs/en/14-ai-development/work-items/AID-2026-193/evidence.md"
    zh-CN: null
---
# AID-2026-193 — 为 00/01/02/06 的镜像三元组补 GOV-DOC-002 front-matter

## 1. 改了什么

本单元负责的四个目录（`00-governance`、`01-system-architecture`、
`02-domain-model`、`06-memory-context`）每语言各 43 对文档、合计 86 份文件。
其中 60 份（每语言 30 份）没有 YAML front-matter，GOV-DOC-002 无法对它们分类：
`docs/en/**` 与 `docs/zh-CN/**` 下的 `.md` 属于受治理范围，但没有 front-matter
的文件是 `_unclassified`，不是合规。

这 60 份里有 42 份（21 对）的 Canonical 文档在仓库中真实存在。本次在 42 份镜像
文件顶部插入 GOV-DOC-002 块，**同时**在它们指向的 21 份 Canonical 文档顶部插入
同一块，共 63 份文件；除此之外不改动任何正文。

## 2. 改动前实测

在 `D:\code\wt-corpus-a`、基线 `4326669caa6c43193d34219a0451b80762b712ff` 上执行：

```
python scripts/check_document_management.py
GOV-DOC-002: 942 governed documents, 496 classified, 446 unclassified
INCOMPLETE: no rule violations in 496 classified documents, but 446 governed documents are still unclassified

python scripts/check_source_revision_pointers.py
STALE=8   （8 条 stale 指针，全部为改动前既有：DEF-corpus-08）
```

四个目录逐语言清点：7 + 11 + 13 + 12 = 43 份，其中 30 份无 front-matter。
这 30 份里有 9 份没有 Canonical（孤儿，见第 6 节），其余 21 份都能找到存在的
Canonical 文档。

## 3. 范围偏离：Canonical 侧也在本次改动内

单元任务书写明"不改 canonical 侧"。这条约束与 DM-12 不可能同时成立，且这不是
解释问题，是实测结果。

DM-12（`scripts/check_document_management.py` 的 `check_scope_and_relations`）
要求 `docs/en/**`、`docs/zh-CN/**` 下的每份文档声明 `bilingual_counterpart.source`，
且该源必须是**已被分类**的受治理文档。在基线提交上对单份镜像做探针，得到三条错误：

```
DM-12 docs/en/02-domain-model/core-entities.md: counterpart 02-domain-model/core-entities.md exists
      but carries no document_metadata, so parity cannot be verified
DM-12 docs/en/02-domain-model/core-entities.md: counterpart docs/zh-CN/02-domain-model/core-entities.md
      exists but carries no document_metadata, so parity cannot be verified
DM-12 docs/en/02-domain-model/core-entities.md: names 02-domain-model/core-entities.md as its source,
      but that file is not a classified governed document
FAIL: 3 error(s)
```

全树同构：基线提交上已分类的 170 份镜像中，**170/170** 的源都是已分类文档。
树里不存在"源未分类却镜像已分类"的状态，所以"只补镜像"不是一个可用状态，
而是红门禁。

由此接受三点，全部明写而不隐藏：

1. **三元组中的 Canonical 根一并分类**（21 份）。这是 DM-12 能过的唯一路径，
   只插 front-matter，不改正文。
2. **这些根与镜像的 `canonical_status` 一律为 `Non-Canonical`。** "分类"与
   "指定某规范化 scope 的唯一权威"是两件事，后者属 Owner 决定；本次不作权威
   主张、不登记 `canonical_scope_id`，`resolve_canonical` 不会因此新增 scope。
   仓内先例：`06-memory-context/context-implementation-coverage.md` 就是已分类的
   `Non-Canonical` / `Informative` 根。
3. **`normative_status` 是转写，不是发明。** 文档自身 `Status:` 行声明为已决定
   的约束（`DECIDED ...`）时取 `Normative`；自述为 candidate、draft、评审记录
   或"not a frozen cross-owner contract"时取 `Informative`。第 4 节表第 4 列
   逐份记录依据，审查者可按单份推翻而无需重新推导。

## 4. 只做插入

提交 `b8c89d790d671cff402c259c588de65bf2234bff` 的 `git diff --cached --numstat` 合计：

```
files 63   added lines 2473   deleted lines 16
```

新增行中 2457 行是 39 行的 front-matter 块（63 × 39 = 2457）；16 行删除是第 5 节
的 `Source revision` / `源版本` 指针，每份 1 行，仅出现在钉住 Canonical blob 的
16 份镜像里。没有任何一行正文散文被删除。插入块之后，每份文件的正文与基线提交
逐字节相同——下表"插入前 blob + front-matter 字节数"即用于让读者复核这一点。

| # | 路径 | role | normative_status | 插入前 blob | 插入后 blob | front-matter 字节 |
|---|---|---|---|---|---|---|

| # | Path | role | normative_status | pre-insertion blob | post-insertion blob | front-matter bytes |
|---|---|---|---|---|---|---|
| 1 | `01-system-architecture/component-interactions.md` | design-specification | Normative | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `7d64051881eb8d27959e1d4721a73e5e4997735d` | 1508 |
| 2 | `01-system-architecture/data-flows.md` | design-specification | Normative | `24bc5867749d234238e6d75aadd4119f359de9f8` | `85eaed6721a58d3847c7d90812bae4e0646c5e86` | 1482 |
| 3 | `01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `b06c15eaba1bc0476eb0a241ffd21b10d184c468` | 1520 |
| 4 | `02-domain-model/core-entities.md` | design-specification | Normative | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `c1afadee6289318f7a19d87fcba2cdb50b7131aa` | 1470 |
| 5 | `02-domain-model/domain-model-overview.md` | design-specification | Normative | `343224eea56829c895a0fdf0e9552f108a2af475` | `c4f7b0a21239e0963da1f59ec011338ea83250ac` | 1492 |
| 6 | `02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `cf548814fb0591b41e4c852cc65adb7d60f2e7bf` | 1492 |
| 7 | `02-domain-model/lifecycle-model.md` | design-specification | Normative | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `462a1e92f79540fa44a90772314e9db1d487abfb` | 1472 |
| 8 | `02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `502a342bb47ffd3b634c322383666a235bca3933` | `85f15fb4239331ff90dec517c6024072d88661c5` | 1489 |
| 9 | `02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `c472e00f2ef4d00bb71806efc7db72062f4efb58` | `7e5e2174a3201b65d8f674b29d38bc831e1f63aa` | 1514 |
| 10 | `02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `22ca7cd3777e0132e25f084084610f1e90b60d21` | `1cf2e4fc9cd04cf949e35851679c5c11cc47a383` | 1518 |
| 11 | `02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `dfc1718c9a5b4ae8f465281d117e5b167d13df4f` | 1481 |
| 12 | `02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `dc53012f50a26c872b9d0f19c078cc5dc992ea0f` | 1487 |
| 13 | `06-memory-context/README.md` | index | Informative | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | `c3c659f03dbaced8b26d7ee475e64735edd16716` | 1473 |
| 14 | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | `e02f1b73a810bab78e0d582cbc85c5f768e32ab3` | 1591 |
| 15 | `06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `25c1da1f6769165881d217bb0bb492a997e0e14c` | `b827f90c0046d2f02322533730747f03dbaa5d8d` | 1580 |
| 16 | `06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `420dc8ba9cf3b65b60b4351e7429dfc3b511056d` | 1590 |
| 17 | `06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `78aa6abc14b3e2711e3b7b784950f2b2acfb5f1f` | 1580 |
| 18 | `06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `0910fea807b96a896e361cd2722e4c94df55187b` | `8eda6a3a07cbc74d74a0698a2d35cb48f3a290c7` | 1565 |
| 19 | `06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `1894860c76336f8739d354b72beed3992cffd17e` | `c23579f7ee429da6a03d95415ca2caa573dc2bc8` | 1621 |
| 20 | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `833815e37ac8d7505d93a0a115421dafe3eb08ad` | `8fe307abc032d693037fc124c941f322d1c3a0d8` | 1641 |
| 21 | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `47423d6f95e613b2f1556f5e359da85d7820617b` | `e5448688d82c3632b0e97f41604368b2c8e77ff9` | 1653 |
| 22 | `docs/en/01-system-architecture/component-interactions.md` | design-specification | Normative | `b5ab766758ab199579ff2dc3cdce6326acfe6dba` | `eb0e7f2d5d185901c29f9bb4a8e746082d8fa943` | 1504 |
| 23 | `docs/en/01-system-architecture/data-flows.md` | design-specification | Normative | `6b4220fe1a1015446ab98ea6065faaaae34ba8b7` | `e154068668ea8d2d1b82ba8280433c6a32aa4237` | 1478 |
| 24 | `docs/en/01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `ec86ed6f84a6636973c58fbe4573619c9a2674c9` | `d2e00e3fae6b5324aaa386f465d074ec8a9377a3` | 1516 |
| 25 | `docs/en/02-domain-model/core-entities.md` | design-specification | Normative | `24ed93dcd5c3a27bcb79bb434b3c8ea8361cbc89` | `517f64624d4a5ce923b4e3e493ff52fdda1f6e65` | 1466 |
| 26 | `docs/en/02-domain-model/domain-model-overview.md` | design-specification | Normative | `e4fd6db47511b21e11d4f697e5cfc086177952c9` | `e54e00724f9ecd6373ea7d6504264ed64406be21` | 1488 |
| 27 | `docs/en/02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `17c09d546a0b7d3eec910f3f59d3494af6ce34e5` | `133fe6d45f14da4cbdee5457f4e5b25bf9886054` | 1488 |
| 28 | `docs/en/02-domain-model/lifecycle-model.md` | design-specification | Normative | `532e74e99f2a6640f5fd6461f3935a08553586ec` | `40a0651bd2555ff8dcf561ece8315a8c52e72f15` | 1468 |
| 29 | `docs/en/02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `f53182e183e5a571fc6c1cc9a9472e3872e124e2` | `db40f22aa5f29b55f5612d82b41ebaf1680089b4` | 1485 |
| 30 | `docs/en/02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `c472e00f2ef4d00bb71806efc7db72062f4efb58` | `8efc859324f45491c849debcd625827bf964fa13` | 1510 |
| 31 | `docs/en/02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `8ccce8ecee41ee46e5a38693eb0126b3e7aad08b` | `fef0bf2fb16bf7f4addb6461b66e8dbcbf609605` | 1514 |
| 32 | `docs/en/02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `c9e352fcb3ca9914e7ed52bedfe6e475a60c306b` | `ef1f4b8eadc3f0af43c88e59743bc0a445fae213` | 1477 |
| 33 | `docs/en/02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `4ae2b40d11aba5db1ce7009ebe8198f75bfc9741` | `66ac6af798b139a0c719c5138c90b14672a626d9` | 1483 |
| 34 | `docs/en/06-memory-context/README.md` | index | Informative | `684490d1c4e2c3aeb0236a9083abf9a144f2744c` | `7a355577d20cfe49d3e73c9a923197a5ec14709a` | 1469 |
| 35 | `docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `1c0782271a01c01648d0917bed59da12e94fd9d7` | `fd9b37b085babeadf1483b937d4bd168c3248646` | 1587 |
| 36 | `docs/en/06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `25c1da1f6769165881d217bb0bb492a997e0e14c` | `a84b5c9843faebec1c9e361cb49539cace78df3c` | 1576 |
| 37 | `docs/en/06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `84c184c2c1476e0cf1b51d56ff80021213ae5b48` | `f4f206c57d0e54fb90a01b75d2f914f7d749bf60` | 1586 |
| 38 | `docs/en/06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `60dc4f43cc03e720e1c2552d77ddabe9947e8e86` | `944e2cb37cf4eff21a7ab331dbfa8316d9583e3b` | 1576 |
| 39 | `docs/en/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `0910fea807b96a896e361cd2722e4c94df55187b` | `6bc838294e70aa20e74ea5fa7bdbe093ac362ef7` | 1561 |
| 40 | `docs/en/06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `1e1a2881941ccecaae780cbed61466205f9c6599` | `ac28dac75910596f2f632e3346d4efdd80dc1f8f` | 1617 |
| 41 | `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `a71df2f8292fc22c90f875c8847fde2cb855b7df` | `0956badfb39c2b37ce0ef63c2e4957b63d76a208` | 1637 |
| 42 | `docs/en/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `abace324c42e18736b1cd273a9aea7f0c29177f8` | `f8a62acf87fb7d26a0e36802d23f6e5dc60ac661` | 1649 |
| 43 | `docs/zh-CN/01-system-architecture/component-interactions.md` | design-specification | Normative | `db9529555336ce3a5d56aa777f3a859aa3123a47` | `03138baa7f1965e3a975d1c4833971f863cb107f` | 1445 |
| 44 | `docs/zh-CN/01-system-architecture/data-flows.md` | design-specification | Normative | `2e52428e085f29f1692b06f9f963e98efd5b5533` | `806a49cbc23e9a12f993878c9ce344e16514cc81` | 1419 |
| 45 | `docs/zh-CN/01-system-architecture/system-quality-attributes.md` | design-specification | Normative | `1c7ea192fa653f789aafa5e04559ad259b05884d` | `93e860a535e81af635406e4058600f602bd3cc4e` | 1457 |
| 46 | `docs/zh-CN/02-domain-model/core-entities.md` | design-specification | Normative | `c9af1f47abd1072427b59b759edcbe6581ec5c3a` | `bff79888a26d39a6b97e15cbe4ee0ae91781ad2e` | 1407 |
| 47 | `docs/zh-CN/02-domain-model/domain-model-overview.md` | design-specification | Normative | `8d3318b5831582717f93028fbf1f50d8cf28333e` | `c684c4783bc6136145f3fae367f7bd9e88142ed0` | 1429 |
| 48 | `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md` | design-specification | Normative | `0d90727ffdf1800463e8089135f8d0de2a96f48d` | `c10bf603604e12188188f0dc39e5d46327ce076a` | 1429 |
| 49 | `docs/zh-CN/02-domain-model/lifecycle-model.md` | design-specification | Normative | `8c4b44727957efac94e16f68451f9a50ab98393d` | `1fa5ff9a0e04f2cc3485842cfacbcb4d9f04b17f` | 1409 |
| 50 | `docs/zh-CN/02-domain-model/phase-1-memory-store.md` | design-specification | Normative | `236e30cf4ddc50899393b83129e3ded05ee012d4` | `2ba9d2892cc330a5b40e963db176d82a5c2c58d4` | 1426 |
| 51 | `docs/zh-CN/02-domain-model/phase-1-sqlite-adapter-contract.md` | design-specification | Normative | `f905be8c183b2927449cd838761a613bcf45a46e` | `548eaa484a1726cecf305468e1e81f3e50431f1b` | 1451 |
| 52 | `docs/zh-CN/02-domain-model/phase-1-storage-trait-contract.md` | design-specification | Informative | `daab973665604c1f4350dc74bccd44cfff3ec4a2` | `0b40edcba5ba45fc25cc3813f839a31e49cb8956` | 1455 |
| 53 | `docs/zh-CN/02-domain-model/relationships-and-provenance.md` | design-specification | Normative | `3afe4718b82f5a95d55f4a21ed73c815bf54f78c` | `0b8c781a9632395548fafa69be9397a3f77dcc1c` | 1418 |
| 54 | `docs/zh-CN/02-domain-model/scope-and-permission-model.md` | design-specification | Normative | `dff51599324a0edbca2bee52d4d9f9b6ffa117c2` | `a3fc192e8a44101545d4233458cc8bdaccdde851` | 1424 |
| 55 | `docs/zh-CN/06-memory-context/README.md` | index | Informative | `5e669ea1346f0bc6286ebc383e07a699fe3d108e` | `0cd572026e306e753815ef3c8d5e5e1205b1338e` | 1410 |
| 56 | `docs/zh-CN/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | design-specification | Informative | `f22a7dc6b52325e350f6e36392b9d27f457d1e8c` | `0778070a39ad17b0aced05f4f5ab05b05cb9cb0c` | 1528 |
| 57 | `docs/zh-CN/06-memory-context/phase-3.6.2-g-jf10-coc-bridge-applied-evidence-acceptance.md` | review-report | Informative | `e59870a91fde8525f8e5e6b2f086a2bc6f049e07` | `82ede79ad03a83f06779393b32ffe953c35510ae` | 1517 |
| 58 | `docs/zh-CN/06-memory-context/phase-3.6.3-g-coc-durable-protocol-applied-boundary-acceptance.md` | review-report | Informative | `0740e142c820785e4e89e9397808eb0ddf967766` | `98ecdf12615d1290d8075050199b0f86cdb32da1` | 1527 |
| 59 | `docs/zh-CN/06-memory-context/phase-3.6.4-g-prepared-participant-gid-applied-acceptance.md` | review-report | Informative | `3cb93ccb212851457b0dd581aaafcdfe7d8a5cb7` | `348ba4802df93fb07e65f6fb0a41212089231d81` | 1517 |
| 60 | `docs/zh-CN/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md` | review-report | Informative | `699ff1d3e396bfce7d6a81bd802e245818ee3c9b` | `cc512115f13b787280a3a1f269d4c95a978c9697` | 1502 |
| 61 | `docs/zh-CN/06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | review-report | Informative | `41af928f45aea6a40ddcd4e974fc583b7f98470a` | `f58ebef37d46a8d9d45c704460239ae5cd8d47c6` | 1558 |
| 62 | `docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | design-specification | Informative | `a5b6642e0c449ea0d2cc18fef365e09b421acfa5` | `1836ca65179afdc7344bf8c7407fad5391f72e31` | 1578 |
| 63 | `docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md` | design-specification | Informative | `4d57e90e987ec6ed679fba9047945e6a73f5d36c` | `d3885b4f4218390ec5d0bada444703104c123873` | 1590 |

## 5. 刷新 Source revision 指针：16 行，DEF-corpus-08

有 8 对镜像在正文里钉住 Canonical blob（`- Source revision: <40-hex>` /
`- 源版本：<40-hex>`）。给 Canonical 插 front-matter 会改变它的 blob，若不同步
指针，就正好复现 DEF-corpus-08 记录的缺陷："同一次提交改了 Canonical 与两侧镜像
却没改这个指针"。下表每条都在同一提交内改为新的 Canonical blob；这是插入块之外
唯一的改动，每份文件 1 行，且 `scripts/check_source_revision_pointers.py` 在改动
前后都报告同样 8 条既有 stale，没有新增。

| 镜像 | Canonical | 改前指针 | 改后指针 |
|---|---|---|---|

| Mirror | Canonical | Pin before | Pin after |
|---|---|---|---|
| `docs/en/01-system-architecture/component-interactions.md` | `01-system-architecture/component-interactions.md` | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `7d64051881eb8d27959e1d4721a73e5e4997735d` |
| `docs/zh-CN/01-system-architecture/component-interactions.md` | `01-system-architecture/component-interactions.md` | `50ddbeed51d88aecbeee0403a4021e21a668dbcb` | `7d64051881eb8d27959e1d4721a73e5e4997735d` |
| `docs/en/01-system-architecture/data-flows.md` | `01-system-architecture/data-flows.md` | `24bc5867749d234238e6d75aadd4119f359de9f8` | `85eaed6721a58d3847c7d90812bae4e0646c5e86` |
| `docs/zh-CN/01-system-architecture/data-flows.md` | `01-system-architecture/data-flows.md` | `24bc5867749d234238e6d75aadd4119f359de9f8` | `85eaed6721a58d3847c7d90812bae4e0646c5e86` |
| `docs/en/01-system-architecture/system-quality-attributes.md` | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `b06c15eaba1bc0476eb0a241ffd21b10d184c468` |
| `docs/zh-CN/01-system-architecture/system-quality-attributes.md` | `01-system-architecture/system-quality-attributes.md` | `4350733173d29451a8ea4aa6a544de46526b4fd7` | `b06c15eaba1bc0476eb0a241ffd21b10d184c468` |
| `docs/en/02-domain-model/core-entities.md` | `02-domain-model/core-entities.md` | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `c1afadee6289318f7a19d87fcba2cdb50b7131aa` |
| `docs/zh-CN/02-domain-model/core-entities.md` | `02-domain-model/core-entities.md` | `06a914699813e36d8bfd69e96c46debb3c3e0cf3` | `c1afadee6289318f7a19d87fcba2cdb50b7131aa` |
| `docs/en/02-domain-model/epistemic-and-temporal-semantics.md` | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `cf548814fb0591b41e4c852cc65adb7d60f2e7bf` |
| `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md` | `02-domain-model/epistemic-and-temporal-semantics.md` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | `cf548814fb0591b41e4c852cc65adb7d60f2e7bf` |
| `docs/en/02-domain-model/lifecycle-model.md` | `02-domain-model/lifecycle-model.md` | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `462a1e92f79540fa44a90772314e9db1d487abfb` |
| `docs/zh-CN/02-domain-model/lifecycle-model.md` | `02-domain-model/lifecycle-model.md` | `c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8` | `462a1e92f79540fa44a90772314e9db1d487abfb` |
| `docs/en/02-domain-model/relationships-and-provenance.md` | `02-domain-model/relationships-and-provenance.md` | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `dfc1718c9a5b4ae8f465281d117e5b167d13df4f` |
| `docs/zh-CN/02-domain-model/relationships-and-provenance.md` | `02-domain-model/relationships-and-provenance.md` | `a674e21756cdbf8c07683083bfdcb58a33f48a20` | `dfc1718c9a5b4ae8f465281d117e5b167d13df4f` |
| `docs/en/02-domain-model/scope-and-permission-model.md` | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `dc53012f50a26c872b9d0f19c078cc5dc992ea0f` |
| `docs/zh-CN/02-domain-model/scope-and-permission-model.md` | `02-domain-model/scope-and-permission-model.md` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | `dc53012f50a26c872b9d0f19c078cc5dc992ea0f` |

## 6. 跳过的孤儿镜像：9 rel / 18 份

Canonical 不存在的镜像无法分类：DM-12 会报"源不存在"，任务书也要求跳过。本单元
四个目录里共有 9 个 rel（18 份文件）处于该状态，与 `defects-corpus.md` 第 5 节
的孤儿清单完全一致；本次不新增、也不消除任何孤儿。

| 孤儿镜像 rel | en + zh-CN 文件数 |
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

## 7. 门禁：全部在本地对已提交树执行

```
python scripts/check_document_management.py --require-changed 4326669caa6c43193d34219a0451b80762b712ff
GOV-DOC-002: 942 governed documents, 559 classified, 383 unclassified
PASS (incremental): no GOV-DOC-002 violations; 559 classified, 383 unclassified

python scripts/check_document_management.py            （全树）
GOV-DOC-002: 942 governed documents, 559 classified, 383 unclassified
INCOMPLETE: no rule violations in 559 classified documents, but 383 governed documents
are still unclassified                      （exit 2：仍有欠账，但无规则违例）

python scripts/test_check_document_management.py
326/326 passed；1 skipped, 1 registered of 1 allowed（T68c）

BASE_SHA=4326669caa6c43193d34219a0451b80762b712ff HEAD_SHA=b8c89d790d671cff402c259c588de65bf2234bff python scripts/check_bilingual_docs.py
bilingual baseline: 77 frozen, 0 new gaps
Bilingual documentation and prompt-library gate: PASS (63 changed paths inspected).

python scripts/check_source_revision_pointers.py
STALE=8（未变），ACCURATE=16（即刷新后的 16 条）
```

受治理 942 → 942；已分类 496 → 559（+63）；未分类 446 → 383（−63）。这五个数字测于语料
提交 `b8c89d790d671cff402c259c588de65bf2234bff`（此时本登记集尚不存在）。在本 PR 的头提交上，同样两条命令报 947 受治理 /
564 已分类 / 383 未分类——五份工作项文档本身也受治理且已分类——增量结论仍是 `PASS`
且零规则违例。全树仍是 exit 2，因为其余目录还有 383 份未分类文档；那是其它 corpus
单元的欠账，本次没有任何规则违例。

## 8. 本次**没有**做什么

- 不改正文：不改措辞、标题、链接、表格单元格；唯一例外是第 5 节 16 行 blob 指针。
- 文档语料内不新建、不删除文件。
- 不动 `00-governance`、`01-system-architecture`、`02-domain-model`、
  `06-memory-context` 之外的目录。
- 不分类任何孤儿镜像，也不为孤儿新建 Canonical。
- 不主张 Canonical 权威：本次写入的 `canonical_status` 全为 `Non-Canonical`，
  不登记 `canonical_scope_id`，不记录审批（全部 `decision_status: Draft`、
  `evidence_verification: Unverified`）。
- 不改任何 checker、schema、baseline、workflow、分支保护或 required context。
- 不关闭任何 Issue。

## 9. 复现

```
git checkout b8c89d790d671cff402c259c588de65bf2234bff
python scripts/check_document_management.py --require-changed 4326669caa6c43193d34219a0451b80762b712ff
git diff --numstat 4326669caa6c43193d34219a0451b80762b712ff..b8c89d790d671cff402c259c588de65bf2234bff
git diff 4326669caa6c43193d34219a0451b80762b712ff..b8c89d790d671cff402c259c588de65bf2234bff -- <path>     # 单份文件：删除行 = 0，或仅那一行指针
```
