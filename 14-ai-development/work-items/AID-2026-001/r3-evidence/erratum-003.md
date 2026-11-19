# Erratum for execution-record-003

- Raised: 2026-11-19 15:22 (UTC+8), by coordinator
- Applies to: `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-003.md` (commit `427f76c`)

## Defect

Record 003 cites identifiers that do not resolve in this repository:

| Cited | Status |
|---|---|
| Commit under test `77f6a3b94eab2243c0d189364fdaae16d2f42fdb` | `git cat-file -t` → `could not get object info` |
| Parent commit `e36a23a` | `427f76c`'s actual parent is `d763a92` |
| Model blob `6ad55a4c9368785460d131f8dabbfab44a0a12be` (45,536 B) | `could not get object info` |

The surviving, verifiable facts from that round are the test blob
`0ee76c38b95ae41e50df8c1582f8055d84495104` (41,275 B, 66 tests) and the three deltas described in
the record's prose (removal of the pre-staging duplicate validation, the `live_state` parameter,
and the retry-record field alignment). Those are consistent with `d763a92`.

## Correction

- Record 003 is **SUPERSEDED for identity purposes**. Do not cite `77f6a3b` or `6ad55a4c`.
- The identity-correct record for the current tip is
  `execution-record-004.md` (commit `3948024`, model blob `ee3df6f5…`, test blob `5521b519…`, 82 tests).
- The "80 tests" figure in record 003 is arithmetically 66 + 14; the current suite is 68 + 14 = 82.

## Cause

The record was written from a working branch state that was never committed under the cited SHA.
No test output was fabricated — `Ran 80 tests / OK` was a real coordinator run of the 66-test suite
plus `test_forget_model`. The defect is in the commit/blob identity fields, not in the pass claim.
