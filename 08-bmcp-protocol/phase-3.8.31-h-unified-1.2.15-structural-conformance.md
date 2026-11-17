# Phase 3.8.31 — Unified COC/JF-10 Schema 1.2.15 Structural Conformance
# Phase 3.8.31 — Unified COC/JF-10 Schema 1.2.15 结构符合性验证

- Date: 2026-11-18
- Exact H Owner branch Head: `5c1e492825910370c5fe6afd7e239d94a01559ec`
- H Unified schema Blob: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- New test Blob: `d8d09ec54a2cc95761c3670fb2a69e325caed5e9`
- Workflow: [H Recovery Cutoff Conformance #44190526491](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44190526491)
- Job: `semantic-and-wire-tests` — SUCCESS
- Log: `Ran 306 tests in 1.007s`, `OK`

## 1. Gap closed

The H Owner branch had a Unified COC/JF-10 schema artifact revision 1.2.15 (wire version 1.3.0), but the existing Recovery Cutoff test inventory did not include a dedicated structural conformance test for that exact 1.2.15 artifact. Older 1.2.10/1.2.11/1.2.12 suites did not prove the latest artifact's declared surface.

Added `test_unified_manifest_1_2_15.py` with 18 structural checks.

## 2. Exact coverage

The 18 checks cover:
1. artifact revision 1.2.15 vs wire version 1.3.0 distinction;
2. exact 11 message families;
3. Recovery Cutoff Batch binding to I/D/C owner snapshots and union manifest digests/counts/roots;
4. typed, unique COC_PARTICIPANT / OWNER_LOCAL_ADMISSION union;
5. owner-admission bindings on COC participants;
6. explicit null COC ref + absence reason + membership proof for unregistered owner admissions;
7. separate request and admission high-waters/counts/digests/roots;
8–10. I, D and C owner-specific high-water shapes;
11. I/D/C owner snapshot root set;
12. owner-admission membership proof binding;
13. RecoveryEpochCompleted exact Batch/Manifest position/digest binding;
14. C Provider Outcome final request boundary requirement;
15. typed JF-10 PreparedParticipant/GID/database-incarnation binding;
16. common envelope origin and signing-sequence metadata declaration;
17. rejection of unevaluated properties in every message branch;
18. Draft 2020-12 schema validity.

## 3. Verification and limits

The complete H Recovery Cutoff workflow ran on exact Head `5c1e492825910370c5fe6afd7e239d94a01559ec`: **306 tests PASS**, including the new 18 schema checks and the existing HRC/RecoveryJoin/wire/I-crypto suites.

This is structural schema conformance only. It does not execute the H semantic validator against signed production fixtures, prove COC quorum or owner snapshot truth, verify cryptographic signatures/anti-rollback, prove the Storage PostgreSQL JF-10 bridge, or establish physical crash/failover/restore behavior.

**Disposition:** H Unified 1.2.15 structural surface — **PASS (18/18 dedicated checks)**. Full H candidate suite — **PASS (306 tests)**. Semantic cross-owner validation, live COC, production crypto/trust, physical JF-10 and production activation remain OPEN.
