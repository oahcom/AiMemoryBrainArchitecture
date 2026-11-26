---
id: AID-2026-100
id_status: PROVISIONAL
title: "#1037 evidence capture — blocked"
status: DRAFT
date: 2026-11-26
authority:
  canonical_status: Non-Canonical
  normative_status: Informative
---

# AID-2026-100 — #1037 evidence capture (English)

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-26  
**Status:** `NOT_CAPTURED`. This record does not resolve #1037.

## Pinned commits

- Baseline: `c6b7d987b959c42af5072932963dae9ed55721e4`
- Fix (#1221 merge): `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`

The fix commit's first parent was verified to be the baseline.

## Capture failure

Attempted:

```sh
git -C /home/ubuntu/ai-projects/AiMemoryBrainArchitecture worktree add <TMP>/ev1037 c6b7d987b959c42af5072932963dae9ed55721e4
```

Verbatim result:

```
Preparing worktree (detached HEAD c6b7d987)
fatal: unable to access 'https://github.com/oahcom/AiMemoryBrainArchitecture.git/': GnuTLS, handshake failed: The TLS connection was non-properly terminated.
fatal: could not fetch b5aab97ed03c822b08a98d59d0c3dca6697f447b from promisor remote
```

Exit code: `128`. Worktree creation failed while fetching a missing object from the partial-clone promisor remote. This was not a checker execution. The existing source working tree had 11 pre-existing changes and was not modified.

## Raw evidence inventory

| Artifact | Command | Exit code | Path | SHA-256 | Status |
|---|---|---:|---|---|---|
| Baseline checker stdout/stderr | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix checker stdout/stderr | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Baseline command metadata | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix command metadata | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix frontmatter inventory | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |

No raw checker output or census inventory was produced, so no digest is claimed and byte-equivalence remains unproven.

## Frontmatter census

The complete fix-commit census was not run. Document totals, frontmatter field frequencies, missing fields, governed-document classification counts, and Normative/Informative counts are all `NOT_CAPTURED`. No previous-commit values are reused as substitutes.

| Metric | Result |
|---|---:|
| Document inventory | NOT_CAPTURED |
| Field occurrence counts | NOT_CAPTURED |
| Missing-field counts | NOT_CAPTURED |
| Governed / classified / unclassified | NOT_CAPTURED |
| Normative / Informative | NOT_CAPTURED |
| Inventory SHA-256 | NOT_CAPTURED |

## Disposition

#1037 remains **BLOCKED**, not RESOLVED. Resolution requires the two complete checker captures (exact command, exit code, full stdout, full stderr, and SHA-256 for each output) plus the full fix-commit census inventory and its SHA-256.

No runtime/validator semantics or existing workflow semantics were changed. Nothing was merged or closed.
