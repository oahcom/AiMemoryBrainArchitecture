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
        - "14-ai-development/work-items/AID-2026-261/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-001 and both fixture suites passed on the initial PR head. GOV-DOC-002 metadata validation initially identified this record's missing document_metadata block; the block is now added. Full 16-context and negative-control proof remain pending."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "owner-namespace"
      - "governance-operation-traceability"
      - "ci-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-261 — Execution evidence

- Attribution: user-authorized operator (delegated by account owner)
- Date: 2026-11-27
- Decision status: 代理裁决，非自然人 Owner 签署
- Repository: oahcom/AiMemoryBrainArchitecture
- Base observed before branch creation: `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`
- Work branch: `s6c/aid-2026-261-owner-governance-read-only`

## Coverage determination

Issue #1237 is not covered by #1341 or #1350. The former enforces uniqueness of work-item identifiers; the latter resolves manifest blob pins to committed bytes. Neither predicate checks whether Owner A–I is confused with SYS-* subsystem identifiers, nor whether a governance operation separately names policy/authorization authority, canonical-state authority, and physical executor.

The relevant implementation is in:
- `scripts/check_owner_namespace_references.py`: `PATTERNS` and `violations()` (Owner/SYS/capability identity distinction and table handling).
- `scripts/check_governance_operation_traceability.py`: `HEADERS`, `EXPECTED_OPERATION_MARKERS`, `FALSE_COMPLETION`, and `check()` (three role columns, operation inventory, collapsed roles, and unilateral completion assertions).
- `tests/test_check_owner_namespace_references.py` and `tests/test_check_governance_operation_traceability.py`: existing fixtures and added targeted cases.

## Required-context wiring

The existing `.github/workflows/bilingual-docs.yml` job is named `GOV-DOC-001 structural checks`. Its `pull_request` trigger has no `paths:` filter. GitHub's `branches/main` response at base observation returned the required context list with `GOV-DOC-001 structural checks` first of 16. No branch-protection setting was changed and no job was added.

The duplicate `.github/workflows/architecture-governance-traceability.yml` was removed. Its two job names were absent from both the live 16-context list and the declared list in `14-ai-development/PR-GOVERNANCE-001.md` §7.

## Fixture evidence — actual GitHub Actions output

Observed on PR #1383 head `70a94cfd0da5b27d1c7a50aea530b400b2a4e13f`:
- Run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940185696
- Job: `GOV-DOC-001 structural checks`, job ID `140312488830`, conclusion `success`.
- Checker output: `OWNER NAMESPACE: PASS (15 registered documents scanned)`; `GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)`.
- Owner suite: `Ran 12 tests in 0.001s`; `OK`.
- Governance suite: `Ran 16 tests in 0.028s`; `OK`.

Each required fixture's actual verbose unittest line was emitted as `... ok`:
| # | Test function | Observed output |
|---|---|---|
| 1 | `test_bare_a_as_owner_identity_is_rejected` | `... ok` |
| 2 | `test_explicit_sys_and_owner_a_references_are_accepted` | `... ok` |
| 3 | `test_owner_crosswalk_table_qualifies_bare_owner_letters` | `... ok` |
| 4 | `test_sys_and_unqualified_owner_letter_in_same_table_are_rejected` | `... ok` |
| 5 | `test_forget_operation_with_three_distinct_roles_is_accepted` | `... ok` |
| 6 | `test_retention_and_legal_hold_operation_is_accepted` | `... ok` |
| 7 | `test_physical_erasure_operation_is_accepted` | `... ok` |
| 8 | `test_backup_expiry_operation_is_accepted` | `... ok` |
| 9 | `test_external_recipient_completion_evidence_is_accepted` | `... ok` |
| 10 | `test_executor_cannot_stand_in_for_canonical_authority` | `... ok` |
| 11 | `test_unilateral_global_completion_claim_is_rejected` | `... ok` |

These are GitHub Actions outputs, not local execution. The final PR Head will be re-run after base synchronization; the above run remains a historical, directly linked measurement.

## Blocking experiment — demonstrated red

Temporary negative-control PR #1386, based on the implementation branch, appended the deliberately invalid line `A owns this subsystem. [temporary negative-control fixture; do not merge]` to the scanned `01-system-architecture/system-boundaries.md`.

- Run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940254262
- Required job: `GOV-DOC-001 structural checks`, job ID `140312696258`, conclusion `failure`.
- Actual log: `ERROR 01-system-architecture/system-boundaries.md:253: BARE_LETTER_AS_OWNER: A owns this subsystem. [temporary negative-control fixture; do not merge]`
- The job then exited 1: `Process completed with exit code 1.`
- The temporary input was reverted on the negative-control branch by commit `8e62f9c7c66abec09c4bc28b1d2512875bee29ce`; PR #1386 was closed unmerged. The injected line is absent from the branch's restored file.

This is direct evidence that the required GOV-DOC-001 context goes red for a real checker violation. The temporary PR was never merged.

## Other observed gates

- GOV-DOC-002 metadata checks: run `45940180469`, job `140312463571`, `success` after adding the required `document_metadata` blocks to this evidence and session-evidence record.
- Repository hygiene: run `45940180512`, job `140312464159`, `success`.
- `check_test_reachability.py`: same hygiene log reports `Test reachability: 67 test files, 67 reachable, 0 unreachable`.

The initial Session Evidence failure was corrected in the PR body: because #1237 predates the effective date and has no Issue-level AI-assisted declaration, its mapping is `LEGACY_UNDECLARED` / `N/A`; the PR-level declaration remains `AI-assisted work: YES`. The manifest records the exact prompt snapshot as `NOT_RECORDED` / `NOT_VERIFIED`, with a missing snapshot path and zero-byte sentinel; no prompt hash or verbatim capture is claimed.

## Main synchronization and 16 required contexts

The implementation branch was updated with the then-current `main` using a GitHub merge commit:
- Main included: `a588cd9914949c2c9db7b2c5704d906fd3f05b70`
- Branch synchronization commit: `11fe4d081cbe1a77e445db660a00151128855981`
- GitHub compare result: `ahead=16, behind=0`.

At synchronized Head `11fe4d081cbe1a77e445db660a00151128855981`, the required contexts returned 16/16 `completed/success`:
1. GOV-DOC-001 structural checks
2. Branch freshness vs base
3. audit
4. GOV-DOC-002 metadata checks
5. BMCP protocol index (hard gate)
6. BMCP conformance suite (hard gate)
7. Schema non-empty audit (hard gate)
8. Bilingual docs coverage (ratchet)
9. Rust clippy (hard gate)
10. Repository hygiene (hard gate)
11. Rust format (hard gate)
12. Rust doctests (hard gate)
13. Session Evidence
14. Session Evidence self-test (base)
15. Session Evidence self-test (head)
16. rust-workspace-test

Run links for this synchronized Head:
- Bilingual documentation / GOV-DOC-001: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575457
- Existing gates (audit, BMCP, Rust and schema contexts): https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575421
- Repository hygiene / reachability: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575491
- GOV-DOC-002: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575594
- Branch freshness: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575573
- Session Evidence: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575661
- Rust workspace: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575545
- Runner admission policy: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45940575731

## Latest main synchronization and exact-Head validation

A further parallel main update was integrated before merge. The latest observed main and the merge commit bringing it into this branch are:
- Latest main included: `6f597e2dd8b6e879bf7539aa16b88a39504d9c49`
- Synchronization merge commit: `81680b0f61d79ebc9a3fa2f54c19db94d66b94d9`
- Compare immediately after synchronization: `ahead=21, behind=0`.

On exact synchronized Head `81680b0f61d79ebc9a3fa2f54c19db94d66b94d9`, all 16 required contexts were observed `completed/success`. The latest run set was:
- GOV-DOC-001: run `45941445883`, job `140316450731`, PASS; checker output `OWNER NAMESPACE: PASS (15 registered documents scanned)` and `GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)`; suites `12 tests OK` and `16 tests OK`.
- GOV-DOC-002: run `45941445889`, success.
- Repository hygiene: run `45941446418`, success; `Test reachability: 67 test files, 67 reachable, 0 unreachable`.
- Branch freshness: run `45941445932`, success.
- Session Evidence and self-tests: run `45941445933`, success.
- Existing required checks (audit, BMCP, schema, Rust): run `45941445918`, success.
- Rust workspace tests: run `45941445940`, success.
- Runner admission policy: run `45941445902`, success.

The eleven fixture functions all emitted `... ok` in GOV-DOC-001 run `45941445883`; see the PR table for each function and assertion. The negative-control failure remains independently demonstrated by run `45940254262` and was reverted/closed as recorded above.

This evidence/manifest refresh itself follows the exact-Head validation above and changes only the AID-2026-261 evidence and manifest records; the PR's final resulting Head is required to rerun the full required contexts before merge. No merge SHA or post-merge blob identity is claimed yet.

## Session record

See `session-evidence.md` for Session role / use case, Actual AI input, and AI-visible output.
