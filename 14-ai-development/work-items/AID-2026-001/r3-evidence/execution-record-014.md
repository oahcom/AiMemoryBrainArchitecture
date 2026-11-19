# R3 Execution Record 014 (Storage documentation amendments closure)

- Timestamp: 2026-11-19 21:25 (UTC+8)
- Executor: WorkBuddy coordinator (L0)
- Basis: Storage `F-STOR-20261119-01-R4` **ACCEPT_WITH_AMENDMENTS** (record-011):
  *"3 amendments (documentation): snapshot integrity defaults, test accounting
  (76+14 vs 90), commit binding evidence."*
- Commit at registration: `745c768deca0a5826d436744213bed3beb65cd85` (remediation tip)
- Tests at registration: `Ran 92 tests — OK` (78 contract + 14 forget), exit code 0.

This record closes the three documentation amendments. No code change is made;
the amendments fix what the evidence documents state, not model behavior.

## Amendment 1 — Snapshot integrity defaults

**Default rule (now normative for all AID-2026-001 evidence snapshots):**
every captured state item used for a zero-side-effect comparison MUST be a
copy, never a live reference. Concretely:

| Mutability | Capture form | Example |
|---|---|---|
| dict | `dict(...)` | `dict(atomic_tuple)`, `dict(outbox)`, `dict(operation_registry)` |
| list | `list(...)` | `list(audit)`, `list(retry_audit)` |
| set | `set(...)` | `set(nonce_registry)` |
| scalar / immutable | by value | `fence_generation`, `commit_counter`, `inventory_revision`, `lifecycle` |

Authoritative locations:
- `test_r3_contract.py` `test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit` (L1535+) — `before_tuple = dict(fresh.atomic_tuple)` (L1610) and the eleven-item snapshot set fixed by `5bdcd32`.
- `r3_contract_model.py` `_commit_snapshot` / `_restore_commit_snapshot` (L475–497) — model-side rollback snapshot follows the same copy convention.

A partial write is detected only if every compared field is a copy; a live
reference would silently track the mutation and vacate the assertion.

## Amendment 2 — Test accounting

**Convention (now normative):** every execution record states per-suite counts
and their explicit sum (e.g. `78 contract + 14 forget = 92 tests`). A bare
total without the breakdown is insufficient.

Ledger of suite counts by commit (each record's number describes its own run):

| Commit | Record | contract + forget | Sum |
|---|---|---|---|
| `6347445` | record-011 era | 76 + 14 | 90 |
| `5bdcd32` | record-012 | 77 + 14 | 91 |
| `95347a5` | record-013 | 78 + 14 | 92 |
| `745c768` | this record (registration run) | 78 + 14 | 92 |

The record-011 phrase "test accounting (76+14 vs 90)" is resolved by this
convention: 76+14=90 was arithmetically correct at its own commit; later
growth to 77/78 contract tests is documented above. No historical record
misstated its own run, and future records must keep the breakdown form.

## Amendment 3 — Commit binding evidence

**Binding rule:** the registry entry and the published commit are bound by
**object identity** (`is` / `is not`), never by field equality. A field-equal
but distinct `AtomicCommit` instance is a different object and must be
rejected.

Evidence chain:
- `b87a7ea` — publisher-side identity check + `test_FSTOR_18_published_commit_identity_must_match_registry` (test_r3_contract.py L2216).
- `5bdcd32` — registry-side check + `test_FSTOR_17_registry_must_hold_the_authoritative_object` (L2153): swaps `operation_registry[key]["commit"]` to a field-equal, distinct `AtomicCommit` and asserts refusal.
- `95347a5` / record-013 — absent-credential residual: the projection/credential agreement checks run unconditionally, closing the `receipt is not None` bypass.

The three agreement checks (receipt_id / nonce / permission_epoch) plus
identity binding together constitute the commit binding evidence; none of the
three alone is sufficient.

## Residual boundary (unchanged)

OUT-OF-SCOPE(dev-baseline) items remain as registered in record-011/012:
real cryptographic verification, production issuer, production verifier
enforcement, DFI-013 concurrency linearisation, DFI-021 WAL durability.

## Registration

| Field | Value |
|---|---|
| Decision_ID | `AID-2026-001-DOC-AMEND-001` |
| Delta_Scope | Documentation only (3 amendments from `F-STOR-20261119-01-R4`) |
| Relevant_Artifacts | `execution-record-011.md` (source), `execution-record-012.md`, `execution-record-013.md`, `test_r3_contract.py` (FSTOR_10/17/18), `r3_contract_model.py` (`_commit_snapshot` L475–497) at `745c768` |
| Evidence | `Ran 92 tests — OK` (78+14) at `745c768`; citations above with line anchors |
| Unresolved_Findings | None for the three amendments. F-STOR-02 PARTIAL (test accounting) is satisfied by Amendment 2's convention + ledger. |

All three documentation amendments from `F-STOR-20261119-01-R4` are now
closed.
