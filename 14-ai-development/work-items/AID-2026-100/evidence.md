---
id: AID-2026-100
id_status: PROVISIONAL
title: "#1037 evidence capture — blocked"
status: DRAFT
date: 2026-11-26
authority:
  canonical_status: Candidate
  normative_status: Informative
---

# AID-2026-100 — #1037 evidence capture (Canonical)

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-26  
**Scope:** #1037, residual evidence items associated with AID-2026-092  
**Status:** `NOT_CAPTURED`; this document does not resolve #1037.

## Pinned revisions

| Role | Commit |
|---|---|
| Baseline | `c6b7d987b959c42af5072932963dae9ed55721e4` |
| Fix (#1221 merge) | `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706` |

The fix commit's first parent was verified as the baseline commit.

## Capture attempt and limitation

Requested worktree command:

```sh
git -C /home/ubuntu/ai-projects/AiMemoryBrainArchitecture worktree add <TMP>/ev1037 c6b7d987b959c42af5072932963dae9ed55721e4
```

Observed result (verbatim):

```
Preparing worktree (detached HEAD c6b7d987)
fatal: unable to access 'https://github.com/oahcom/AiMemoryBrainArchitecture.git/': GnuTLS, handshake failed: The TLS connection was non-properly terminated.
fatal: could not fetch b5aab97ed03c822b08a98d59d0c3dca6697f447b from promisor remote
```

Exit code: `128`. This is the failed worktree-creation operation, **not** a checker run. No checker stdout/stderr, checker exit code, or checker output digest was captured for either revision. The source checkout also had 11 pre-existing staged/unstaged/untracked paths; it was left untouched.

## Evidence register

| Evidence | Command | Exit code | Raw output path | SHA-256 | Status |
|---|---|---:|---|---|---|
| Baseline checker stdout | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Baseline checker stderr | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix checker stdout | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix checker stderr | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Baseline command/exit metadata | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix command/exit metadata | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix frontmatter census raw inventory | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |

No SHA-256 values are supplied because the requested raw evidence files do not exist. No equivalence or difference conclusion can be drawn.

## Frontmatter census

A full-tree census at the fix commit was not executed. Therefore the following remain unmeasured: total documents, documents with/without frontmatter, field occurrence counts, missing-field counts, governed-document classification distribution, and Normative/Informative counts. No counts from another commit or prior report are substituted.

| Census dimension | Result |
|---|---:|
| Full document inventory | NOT_CAPTURED |
| Frontmatter field frequency table | NOT_CAPTURED |
| Missing-field table | NOT_CAPTURED |
| Governed / classified / unclassified | NOT_CAPTURED |
| Normative / Informative | NOT_CAPTURED |
| Raw inventory SHA-256 | NOT_CAPTURED |

## Resolution decision

**#1037 remains BLOCKED.** It must not be marked RESOLVED until both checker executions have complete raw stdout/stderr/exit-code records and SHA-256 digests, and the fix-commit frontmatter census has a complete raw inventory and digest. The current PR is a provisional evidence-tracking artifact only; it does not satisfy the acceptance criteria.

No runtime, validator, or workflow semantics were changed. No merge or Issue closure was performed.
