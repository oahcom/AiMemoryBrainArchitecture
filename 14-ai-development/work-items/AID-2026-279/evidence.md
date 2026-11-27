# AID-2026-279 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Issue:** #1341  
**Base observed at implementation start:** 40195e8bf96b9cc6aa254066b9b72968f29ac361

## Contract

| Candidate change | Latest target branch | Result |
|---|---|---|
| Candidate newly introduces AID-YYYY-NNN/ since merge-base | Same directory exists on latest target base | VIOLATION (exit 1) |
| Candidate newly introduces an unoccupied AID-YYYY-NNN/ | Directory absent from latest target base | PASS (exit 0) |
| Candidate adds files under a directory already present at merge-base | Existing directory | PASS (exit 0) |
| Base/head/merge-base/tree/diff cannot be read | Any | INCOMPLETE (exit 2; never PASS) |

The checker measures identity introduction from merge-base to candidate HEAD, then measures occupancy against the latest target-branch SHA supplied by the workflow. This catches a stale topic branch whose identifier was acquired on main after the topic branch forked, without treating ordinary file additions in an established work-item directory as a second identity declaration.

## Serialization mechanism

The check runs inside the existing GOV-DOC-002 metadata checks job, already one of the 16 required contexts. The workflow has fetch-depth: 0, PR_BASE, and PUSH_BEFORE. On PR it uses pull_request.base.sha and pull_request.head.sha; on push it uses github.event.before as base and github.sha as candidate. No job or required context is added.

The branch endpoint reports 16 required contexts including Branch freshness vs base. The branch-protection /protection endpoint returned HTTP 403 to this connection, so strict and enforce_admins are not asserted. Merge serialization through strict freshness remains unverified until those two fields can be independently read.

## Execution evidence

Raw stdout and exit codes for the deterministic scenarios are emitted by scripts/ci/test_work_item_uniqueness.py in the required GOV-DOC-002 check. This API-only implementation session did not execute Python locally. The PR and Issue evidence comment must carry the exact Actions output; absent Actions output is unverified.

## Boundaries

No branch-protection setting, job, required context, blob-pin checker, or repository-hygiene workflow is changed. No squash, rebase, force-push, or Issue closure is performed.
