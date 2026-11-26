# AID-2026-111 — Executed prompt snapshot

Attribution: user-authorized operator (delegated by account owner), 2026-11-26.

Allocation correction: the initially selected provisional ID AID-2026-109 was already occupied on main at the merge-time rescan. AID-2026-110 was reserved by PR #1304 (and had a prior historical use in PR #1287). This work item is therefore renumbered to AID-2026-111; preserve RENUMBERED_FROM: AID-2026-109.

Task: Map the 94 supplied SQLite backend test names from exact HEAD a123ea4e414c9f74fa0c576fbd718049a7d9f917 to the literal predicates in SC-01..SC-18 and HIR-01..HIR-18. Rejudge all 72 AID-095 Gate A matrix cells and all 16 EVIDENCE_REQUIRED rows using only PASS, PARTIAL_EVIDENCE or UNCHANGED. PASS requires complete named-test coverage; do not infer PASS from green test suite status. Preserve the 94 exact test names, command, HEAD, exit code, test binary count, passed/failed count, stdout byte count and SHA-256. Also preserve the supplementary pure-Rust run at 44dc21a4970192118ba434801b8ca05702ac582c and the Windows workspace build failure as negative toolchain evidence.

Mandatory boundaries: Linux + bundled SQLite local execution, not CI; not distributed backend, not multi-replica linearizability, not production topology. SC-17 cross-resource GID participants, SC-18 RPO/RTO backup/failover, HIR-17 H Attempt/C/G DeliveryAttempt and G Applied join, HIR-18 I PermissionEpoch/current authorization recheck, and D/I anti-rollback anchor linkage must not be promoted without their missing evidence.

Create Canonical + EN + ZH-CN work records with complete GOV-DOC-002 metadata. No runtime, validator, schema, API, DDL, tests or workflow changes. Keep #1211 and #1212 open. Open a Draft PR, wait for all 16 required contexts on exact final Head, merge only after a fresh pre-merge check, verify blobs, then comment on #1211 and #1212 with the resulting counts.
