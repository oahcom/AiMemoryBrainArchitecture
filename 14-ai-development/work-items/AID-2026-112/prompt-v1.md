# AID-2026-112-PROMPT v1

Attribution: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Work item ID: AID-2026-112 (PROVISIONAL; alloc_at_push rechecked against main INDEX)

Rejudge SC-01…SC-18 and all HIR-01…HIR-18 using three supplied local execution records:
- SQLite backend: 99 passed, 0 failed, exact HEAD a123ea4e414c9f74fa0c576fbd718049a7d9f917; 94 test names supplied.
- Pure Rust layer: 276 passed, 0 failed, HEAD 44dc21a4970192118ba434801b8ca05702ac582c; aggregate only, no individual names.
- memory-context: 177 passed, 0 failed, exact HEAD a123ea4e414c9f74fa0c576fbd718049a7d9f917; 23 relevant names supplied.

Record exact commands, HEADs, exit codes, test-binary counts, stdout byte lengths and SHA-256. Use NOT_RECORDED where byte length was not supplied. Map every supplied SQLite and memory-context test name by literal semantics; explicitly mark no corresponding test where appropriate. Do not invent mappings for aggregate-only pure-Rust results.

PASS requires named tests to fully cover the entire predicate; otherwise use PARTIAL_EVIDENCE or UNCHANGED. Rejudge all 72 AID-095 flow cells and all 16 EVIDENCE_REQUIRED rows separately. Compile-intent tests map to SC-15, Fence tests are not SC-12 projection tests, and no ABORTED receipt path is evidenced. HIR-17 and SC-16 gain memory-context evidence but remain partial until cross-domain joins are proven.

Preserve the boundary: local WSL2/Linux bundled SQLite, not CI, not distributed backend, not multi-replica linearizability, not production topology. Keep Gate A/B conservative. No runtime/validator/schema/API/DDL/workflow/deployment changes. No IMPL2 restoration. Do not close #1211 or #1212. Create Canonical/EN/ZH-CN evidence docs with GOV-DOC-002 metadata, Draft PR, 16 exact-head required contexts, merge only after final-head freshness and all checks, verify merged blobs, and comment on #1211 and #1212.
