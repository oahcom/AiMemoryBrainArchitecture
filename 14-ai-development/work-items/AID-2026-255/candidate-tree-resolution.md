# AID-2026-255 — Candidate Tree Resolution

## Candidate identity and method

- Candidate commit: `f1319b32ad23a050f9f6092f10cb26e6478676cc`
- Candidate short identity: `f1319b32`
- Base commit: `242cf101c8b79007ad2fb8d9c89681224577188d`
- Resolution source: candidate Git tree at commit `f1319b32ad23a050f9f6092f10cb26e6478676cc`
- Resolution result: all 12 referenced paths resolved.
- Byte source: the bytes used for the Git blob calculations came from the Git tree, not the working copy.

For each row, the declared Git blob ID was compared with the actual Git blob ID calculated from the candidate-tree object. All 12 declarations are `MISMATCH`.

## Resolved identities

| # | Manifest | Field | Referenced path | Resolution | Declared Git blob ID | Actual Git blob ID |
|---:|---|---|---|---|---|---|
| 1 | AID-2026-100 | `baseline_and_source_evidence.authored_indexes[0].root_blob` | `05-memory-runtime/README.md` | resolved | `107c225b631eaa5732bab90bc09144799a542502` | `13570e9fe2ad87958c387696088f145f6a24103d` |
| 2 | AID-2026-100 | `baseline_and_source_evidence.authored_indexes[0].en_mirror_blob` | `docs/en/05-memory-runtime/README.md` | resolved | `2fac42740167293c941c1450437ca780d0488b5d` | `ad36c55cf572a94c60557104b3a51652b75668cb` |
| 3 | AID-2026-100 | `baseline_and_source_evidence.authored_indexes[0].zh_cn_mirror_blob` | `docs/zh-CN/05-memory-runtime/README.md` | resolved | `9881fd88fcbfe1b3760154503c8d13e781ad89f0` | `a5c9e3d9406c31020c1943d03561a7f381a03829` |
| 4 | AID-2026-100 | `baseline_and_source_evidence.authored_indexes[1].root_blob` | `09-security-governance/README.md` | resolved | `1046665b0990183b689ed6db88edc9ba1089c83e` | `37b4c8a7f6b807bc22e9f278106972cbe84af8c8` |
| 5 | AID-2026-100 | `baseline_and_source_evidence.authored_indexes[1].en_mirror_blob` | `docs/en/09-security-governance/README.md` | resolved | `7c8b434c7161c47c5e35e0ffcadc736981996c4a` | `d5b9495f2a2461a66546291091a942bef778e9ed` |
| 6 | AID-2026-100 | `baseline_and_source_evidence.authored_indexes[1].zh_cn_mirror_blob` | `docs/zh-CN/09-security-governance/README.md` | resolved | `772025aa9da8afe706af6f607ae47e35c5020522` | `3d9be0a60a6c53e450d606222ff666add553ce96` |
| 7 | AID-2026-100 | `related_evidence[0].blob` | `14-ai-development/work-items/AID-2026-100/evidence.md` | resolved | `87adf4a8cde8ba5c4c14596932f3488ec988a38c` | `ae46c7a4424778d0c8e4c5b21c6535023a9b460d` |
| 8 | AID-2026-100 | `related_evidence[0].en_mirror_blob` | `docs/en/14-ai-development/work-items/AID-2026-100/evidence.md` | resolved | `da156fe2409f17b364e9af65446bb73ab709e539` | `425e5eaf6c99286342e20f5ecf525ee297d75e0c` |
| 9 | AID-2026-100 | `related_evidence[0].zh_cn_mirror_blob` | `docs/zh-CN/14-ai-development/work-items/AID-2026-100/evidence.md` | resolved | `d750ef5555916bfb82180f30a6e83b3a0766fdfc` | `fda38f1355f6160db78facde996fee3345905ea1` |
| 10 | AID-2026-150 | `source.files[0].blob` | `03-memory-brain/canonical-memory-store.md` | resolved | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `2e10e23f651f1f6cb03247f01727f2b7ff5342f1` |
| 11 | AID-2026-150 | `source.files[1].blob` | `03-memory-brain/commit-cursor-semantics.md` | resolved | `4688a0ca487bf4d853c7f0220408abe8d743d159` | `2c68161d039310b8df0e1387b4f1111ed74699db` |
| 12 | AID-2026-150 | `source.files[2].blob` | `03-memory-brain/forget-fence-operation-and-publication-gate.md` | resolved | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `dd26e3cae2e60dbdc44a6e084004effcd2033efa` |

## Result

- Authorized identities examined: 12
- Resolved candidate-tree paths: 12
- Missing candidate-tree paths: 0
- Matching declared/actual blob IDs: 0
- Mismatching declared/actual blob IDs: 12

The complete per-pin rehash ledger is captured in `blob-rehash-ledger.tsv`. The measured mismatch output is captured in `negative-mismatch.log`.
