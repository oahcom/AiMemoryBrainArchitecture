---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The prompt snapshot was hashed from its committed bytes after adding the required DM-15 steward field; the digest and byte count below are reproducible with sha256sum and wc -c."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Evidence — AID-2026-116 prompt digest recalculation

The prompt snapshot `prompt-v1.md` received the required DM-15 steward metadata:

`steward: \"user-authorized operator (delegated by account owner)\"`

**因 DM-15 补 steward 重算。** The top-level manifest `prompt_sha256` / `prompt_bytes` and `session_evidence[0].executed_prompt_sha256` / `executed_prompt_bytes` were recomputed from the resulting file bytes, without changing any of the 33 digest correction records or their target/attribution conclusions.

- Previous prompt SHA-256: `3b8f72e2e124b24625035c42398c0529655be4d8e8e48ddfc4b7369b89ce1c94`
- Previous prompt bytes: `8274`
- Recomputed prompt SHA-256: `6fd626bfd4674e3e98f107baa93b4f2ef1061eac36c80c66a7778714ab5b725e`
- Recomputed prompt bytes: `8341`
- Reproduction: `sha256sum 14-ai-development/work-items/AID-2026-116/prompt-v1.md` and `wc -c < 14-ai-development/work-items/AID-2026-116/prompt-v1.md`

---

## AC6 is falsified on `main` (measured 2026-11-27)

`acceptance_criteria.AC6` states: *"All 32 repinned manifests and AID-2026-106 hash to the committed bytes of the prompt they pin, and all 33 INDEX cells that restate a digest or byte count agree with them."*

The **manifest half holds**: every pinned manifest on `main` hashes to its committed prompt bytes (64/64 checked, 0 mismatches). The **INDEX half does not**. On `main` at the time of this measurement, **32 INDEX Prompt cells restate a value that no committed byte sequence has**.

Cause: the INDEX half of this work was carried on the branch `gov/aid-116-pin-and-attribution` and was **dropped by the merge commit** `a7cf5256` (PR #1321). The branch head says one thing, the merge commit says another, and the merge commit won:

| Ref | `AID-2026-059` cell | `AID-2026-101` cell |
|---|---|---|
| merge base `756e1e25` | 3866 bytes | 4470 bytes |
| branch head `f53cf728` (PR #1321) | 3808 bytes | 4412 bytes |
| merge commit `a7cf5256` | 3866 bytes | 4470 bytes |

GitHub does not execute the repository's `merge=union` attribute for `INDEX.md`, so the file was resolved by hand at merge time and the branch side was discarded. Nothing detected it: `check_traceability.py --index-only` and `check_repository_hygiene.py` both compare the manifest to the file it pins and neither reads the INDEX table, so a cell can drift from the manifest it summarises with nothing to notice. This is the same blind spot recorded as `how_it_was_missed` under F4.

### The 32 cells, as measured before repair

| Work item | INDEX cell states (stale) | Manifest declares (correct) | Delta |
|---|---|---|---|
| `AID-2026-059` | 3866 bytes, `65474e7f0927…` | 3808 bytes, `4881d6292e96…` | -58 |
| `AID-2026-060` | 7797 bytes, `f9a01079c017…` | 7739 bytes, `7a9793427868…` | -58 |
| `AID-2026-061` | 18776 bytes, `7ea255ab98c0…` | 18718 bytes, `6c0a9cc7e47f…` | -58 |
| `AID-2026-062` | 2927 bytes, `3f57662579cf…` | 2869 bytes, `96358a3a9af4…` | -58 |
| `AID-2026-063` | 2691 bytes, `4cf341c81da4…` | 2633 bytes, `411a0be8d6e7…` | -58 |
| `AID-2026-066` | 5921 bytes, `1ae516e747ae…` | 5863 bytes, `d6afe924427a…` | -58 |
| `AID-2026-067` | 5261 bytes, `07b49d7fa41e…` | 5203 bytes, `c73aa6e35fdd…` | -58 |
| `AID-2026-068` | 6031 bytes, `7d55d2011f93…` | 5973 bytes, `9a1e0e823d20…` | -58 |
| `AID-2026-069` | 6062 bytes, `360c3273a8e6…` | 6004 bytes, `12a7ebc07e9d…` | -58 |
| `AID-2026-070` | 6371 bytes, `b0013ed25ebd…` | 6313 bytes, `6df00b015153…` | -58 |
| `AID-2026-071` | 4303 bytes, `4c735edd42b8…` | 4245 bytes, `8080149aa3a0…` | -58 |
| `AID-2026-072` | 8623 bytes, `1c8f58cff7d2…` | 8565 bytes, `5e29f0695537…` | -58 |
| `AID-2026-073` | 5089 bytes, `08eb2369f7f6…` | 5031 bytes, `278e8a975be3…` | -58 |
| `AID-2026-074` | 3967 bytes, `78044dfbc688…` | 3909 bytes, `b5c8c5470850…` | -58 |
| `AID-2026-075` | 4961 bytes, `e85f9ae06779…` | 4903 bytes, `0a1b6f824842…` | -58 |
| `AID-2026-076` | 5525 bytes, `06ee5615ab9f…` | 5467 bytes, `697484699587…` | -58 |
| `AID-2026-077` | 5621 bytes, `0339f07cd6bd…` | 5563 bytes, `9de48039bb47…` | -58 |
| `AID-2026-078` | 7533 bytes, `c2ae6f744dbf…` | 7475 bytes, `cb9890fc1c4e…` | -58 |
| `AID-2026-079` | 5790 bytes, `a2d216ee6479…` | 5732 bytes, `af8ad57de5ed…` | -58 |
| `AID-2026-080` | 9932 bytes, `08f5e42efdef…` | 9874 bytes, `c071d0ee5978…` | -58 |
| `AID-2026-081` | 4428 bytes, `7b761550e7cf…` | 4370 bytes, `a02724519122…` | -58 |
| `AID-2026-082` | 5831 bytes, `79bcd0738f9c…` | 5773 bytes, `ff3eccdc7154…` | -58 |
| `AID-2026-084` | 4775 bytes, `acdd40d2b2b2…` | 4717 bytes, `3e02da52ac45…` | -58 |
| `AID-2026-085` | 7689 bytes, `17a8cd7583b8…` | 7631 bytes, `80a1ecb80d09…` | -58 |
| `AID-2026-089` | 4258 bytes, `7682d9287605…` | 4200 bytes, `e75f603f054d…` | -58 |
| `AID-2026-092` | 3772 bytes, `a459d7e523fb…` | 3714 bytes, `9de089512403…` | -58 |
| `AID-2026-094` | 6972 bytes, `81644f71a94a…` | 6914 bytes, `766d5bd3f8ed…` | -58 |
| `AID-2026-097` | 4283 bytes, `4e3dbbd35d00…` | 4225 bytes, `70f4eb79f8c4…` | -58 |
| `AID-2026-101` | 4470 bytes, `2ac71e563b9c…` | 4412 bytes, `de3b9b80c952…` | -58 |
| `AID-2026-102` | 4470 bytes, `df3c53282d85…` | 4412 bytes, `468a1d4fd8f4…` | -58 |
| `AID-2026-106` | 2998 bytes, `0ef830572575…` | 2998 bytes, `ed3345b0f9c7…` | 0 |
| `AID-2026-241` | 7038 bytes, `f8e6b0621208…` | 7105 bytes, `2bcdadfaa7a7…` | 67 |

Reproduce with:

```text
python verify_index_cells.py <repo> origin/main      # expect DISAGREE=32
python verify_index_cells.py <repo>                  # expect DISAGREE=0
```

31 of the 32 differ by exactly 58 bytes — the two frontmatter lines PR #1281 removed from every prompt snapshot, which the manifests were repinned for and the INDEX cells were not. `AID-2026-106` differs by digest only at an unchanged byte count, which is why a size comparison cannot see it (F5). `AID-2026-241` differs by +67 bytes and was never part of this work: its prompt file changed after the branch point, so its cell is stale for a different reason and is corrected here from the committed bytes rather than from the branch.
