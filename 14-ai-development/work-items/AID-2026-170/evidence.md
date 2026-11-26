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
        - "14-ai-development/work-items/AID-2026-170/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Both pinned blobs were read from the local object database and diffed directly; the single changed table cell and the remaining 5c0e2049 pins were re-read from origin/main. Not verified: which H schema is normatively current, and any Owner signature."
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
    canonical_status: Canonical
    canonical_scope: "Evidence for the SYS-RISK-001 I P0 allowlist pointer alignment from phase-3.8.9 (5c0e2049) to the Owner-designated current phase-3.8.10 (44986f5f)"
    canonical_scope_id: "ai-development/aid-2026-170-sys-risk-001-p0-pin"
    canonical_scope_keywords:
      - sys-risk-001
      - p0-allowlist
      - pin-reconciliation
      - phase-3.8.10
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-170/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md"
---
# AID-2026-170 — SYS-RISK-001 I P0 allowlist pointer alignment

- Work item: AID-2026-170; `id_status: PROVISIONAL`; `status: DISPATCHED`.
- Attribution: user-authorized operator (delegated by account owner); date: 2026-11-26.
- Main baseline when the branch was created: `8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`.
- Scope: one table cell in each of two review renditions. No allowlist body, no other pin, no restoration of `phase-3.8.9`.

## 1. Ruling applied

The dispatch brief records the Owner's final ruling: the **current** I P0 allowlist is `phase-3.8.10` (`44986f5f…`), and `phase-3.8.9` (`5c0e2049…`) is `SUPERSEDED_BY` it. This work item applies that ruling to the two places in `SYS-RISK-001` that still named the older pin. It records a delegated ruling; it does not create one and claims no Owner signature.

## 2. The one pointer changed

`reviews/architecture/SYS-RISK-001.en.md`, line 297 — before:

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md | 5c0e2049513d391dfc118f4f629a5ec95de456d6 | I-owned P0 projection candidate; production profile, trust roots, key custody, anti-rollback and complete P0 vectors remain open |
```

after:

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md | 44986f5f864bcdc1a79d34978273644d381a68c0 | I-owned P0 projection candidate; production profile, trust roots, key custody, anti-rollback and complete P0 vectors remain open; phase-3.8.9 Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6 (SUPERSEDED_BY); reconciled_by: AID-2026-170 |
```

`reviews/architecture/SYS-RISK-001.zh-CN.md`, line 296 — before:

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md | 5c0e2049513d391dfc118f4f629a5ec95de456d6 | I-owned P0 projection candidate；生产 Profile、Trust Roots、Key Custody、anti-rollback 和完整 P0 vectors 仍未完成 |
```

after:

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md | 44986f5f864bcdc1a79d34978273644d381a68c0 | I-owned P0 projection candidate；生产 Profile、Trust Roots、Key Custody、anti-rollback 和完整 P0 vectors 仍未完成；phase-3.8.9 Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6（SUPERSEDED_BY）；reconciled_by: AID-2026-170 |
```

Two notes on the shape of the change:

- The row's artifact **path** moves with the blob. Leaving `phase-3.8.9-…-1.2.13….md` in the path column while putting a `phase-3.8.10` blob in the blob column would manufacture a path/blob mismatch inside a document whose only purpose is exactness. Path and blob are one pointer; both were changed in the same cell.
- The rest of the cell — the owner HEAD `28df608b…`, "I-owned P0 projection candidate" and every open item after it — is preserved word for word. The older pin is not erased: it stays in the same cell as an explicit `SUPERSEDED_BY` record.

## 3. Blob identity and the difference between the two pins

| Pin | Full blob SHA | Object size | Status after this change |
|---|---|---|---|
| `phase-3.8.9` I P0 allowlist | `5c0e2049513d391dfc118f4f629a5ec95de456d6` | 20 906 bytes | `SUPERSEDED_BY` |
| `phase-3.8.10` I P0 allowlist | `44986f5f864bcdc1a79d34978273644d381a68c0` | 21 917 bytes | current |

Observed difference, read directly from the two objects:

```
git diff --text --stat 5c0e2049513d391dfc118f4f629a5ec95de456d6 44986f5f864bcdc1a79d34978273644d381a68c0
 1 file changed, 18 insertions(+), 11 deletions(-)
```

Everything in that diff falls into three groups:

1. the version string `1.2.13` → `1.2.14` in the two title lines, §4, §12.1 and §13 (English and Chinese);
2. the header schema blob `8e7f6a6c9663388863db88548f9c37d0fdb1bd97` → `09fcd1fa29fe24255fbd87cae79dafb406594a59` (one place);
3. a new §14 that records one H-side addition (`forget_fence_generation_high_water` to the **D** owner-specific high-water union) and explicitly states that I's five-field high-water object and I P0 are unchanged.

The §2–§12 field lists are identical line for line. No field was added to, or removed from, the I P0 projection.

## 4. Why this is registration alignment, not a semantic change

The two blobs are the same allowlist one version string apart: the only content difference is the H version the allowlist binds to, the matching schema blob, and a note that the new D field does not touch I's namespace or I P0 — so re-pinning `SYS-RISK-001` to `44986f5f` changes which artifact the report **names**, not what the report **requires**; nothing in the I contract, the field set or the open-item list moves.

## 5. Other files on main that still pin `5c0e2049` (listed, not changed)

`git grep -n 5c0e2049 origin/main` returns five lines in four files. The two lines in §2 above were the only ones inside `SYS-RISK-001`; the rest are left exactly as they are, for a separate ruling:

| File | Line | What the line is |
|---|---|---|
| `14-ai-development/work-items/AID-2026-107/evidence.md` | 515 | evidence-ledger row for the phase-3.8.9 allowlist, disposition `UNDECIDED`, reason `U-OWNER-DECISION` |
| `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md` | 512 | EN mirror of the same row |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md` | 512 | ZH-CN mirror of the same row |
| `reviews/architecture-feasibility/phase-2-contradiction-register.md` | 150 | "Resolution evidence" sentence (English) citing the 3.8.9 P0 blob |
| `reviews/architecture-feasibility/phase-2-contradiction-register.md` | 154 | the same sentence in Chinese |

Two observations that are recorded, not acted on:

- The AID-2026-107 rows are a ledger with a live `UNDECIDED` disposition. Flipping them here would rewrite another work item's adjudication state, which the dispatch brief forbids.
- The contradiction register's sentences describe how ARC-02/03 evidence was resolved **at the time of writing**. They are historical narrative about a past readback; they are not a pointer to "the current I P0", so the Owner ruling does not mechanically apply to them.

Files that already pin `44986f5f…` (`reviews/architecture-authority/2026-11-17/FINAL-A-002.{en,zh-CN}.md`, `SYS-RISK-002.{en,zh-CN}.md`, `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md`) needed no edit and got none.

## 6. Verification performed, and its limits

Performed here:

- `git grep -n 5c0e2049 origin/main` and `git grep -n 44986f5f origin/main` — pin inventory above.
- `git diff --text --stat` and a full `git diff --text` read of the two blobs — the 18+/11- figure and the three-group classification in §3 are read from the objects, not repeated from the brief.
- `git diff -U0` on the two changed files — the change is one line per file: 2 files changed, 2 insertions(+), 2 deletions(-).
- `git ls-tree -r --name-only origin/main` — no `i-p0-allowlists` artifact exists on main, and `reviews/architecture/SYS-RISK-001.md` (a root rendition) does not exist; the EN and ZH-CN renditions are the whole set, and both were changed.

Not performed, and not claimed:

- No re-derivation of which H unified schema version is normatively current, no Owner signature, no review.
- The two allowlist artifacts are branch artifacts, not main paths. Their paths are quoted as the brief records them and as they appear in `FINAL-A-002` / the AID-2026-107 ledger; only their blob identities were verified, by content.
- No claim that this closes any risk in SYS-RISK-001. R-01…R-10 and every "remaining open" item in the I row are untouched.

## 7. Files in this change

| File | Action |
|---|---|
| `reviews/architecture/SYS-RISK-001.en.md` | line 297: one pointer cell re-pinned, `reconciled_by` added |
| `reviews/architecture/SYS-RISK-001.zh-CN.md` | line 296: the same change, structure preserved |
| `14-ai-development/work-items/AID-2026-170/manifest.yaml` | new |
| `14-ai-development/work-items/AID-2026-170/prompt-v1.md` | new — executed prompt snapshot |
| `14-ai-development/work-items/AID-2026-170/session-evidence.md` | new |
| `14-ai-development/work-items/AID-2026-170/evidence.md` | new — this file |
| `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md` | new — EN rendition |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md` | new — ZH-CN rendition |
| `14-ai-development/work-items/INDEX.md` | one appended row |
