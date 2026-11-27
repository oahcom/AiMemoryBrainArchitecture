# AID-2026-255 — Independent Review

## 1. Review identity and independence disclosure

**Work item:** AID-2026-255  
**Issue:** #1350 (defect parent #1349)  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Branch:** `work/AID-2026-255-manifest-blob-pin-integrity`

**Exact head designated for review:**

`6fed932dadcaa074ac18c30ad4b8c61e2cb9d813c`

**Independence disclosure**

I am a separate ChatGPT conversation reading frozen artifacts supplied as text. This provides conversation/context isolation only. It does not establish model, provider, runtime or statistical independence, and it is not multi-model consensus.

I did not write the implementation and have no access to the implementing session.

### Evidence available

The orchestrator supplied:

1. Immutable implementation prompt v1.
2. Owner A scope ruling v2.
3. `check_manifest_blob_pins.py`.
4. `test_check_manifest_blob_pins.py`.
5. `manifest-blob-pins.txt`.
6. `blob-field-inventory.md`.
7. `candidate-tree-resolution.md`.
8. `negative-fixtures.md`.
9. `exact-head-verification.md`.
10. `regression-gates.log`.
11. `blob-rehash-ledger.tsv`.

### Evidence unavailable

I was not given:

- Live repository access.
- The actual Git objects or candidate tree.
- The complete `gate_ratchet.py` implementation.
- `test_gate_ratchet.py`.
- The new GitHub Actions workflow.
- The complete work-item manifest and INDEX registration.
- The raw negative-fixture execution log.
- The actual CI run records.
- An ability to execute code or independently reproduce test results.

Consequently, this is a static review of supplied source and evidence, not an independently executed verification.

**Important identity discrepancy:** The supplied implementation evidence identifies candidate `f1319b32ad23a050f9f6092f10cb26e6478676cc`, whereas this dispatch designates `6fed932dadcaa074ac18c30ad4b8c61e2cb9d813c`. I cannot establish that the supplied source files are the contents of the designated head.

---

## 2. Question 1 — Does the checker prove the invariant?

**Assessment: The core byte-integrity mechanism is correctly implemented in the supplied source.**

### 2.1 Actual committed bytes, not working-tree bytes

Relevant symbol: `tree_bytes()` in `scripts/ci/check_manifest_blob_pins.py`.

The implementation executes:

```python
git cat-file -e HEAD:<path>
git cat-file -t HEAD:<path>
git cat-file blob HEAD:<path>
```

It obtains the referenced content from the Git object database.

It does not read the referenced file using `Path.read_bytes()` or trust the working-tree contents.

This establishes the important distinction between committed bytes and potentially modified working-tree bytes.

**Result: PASS, at source-inspection level.**

### 2.2 Git blob identity calculation

Relevant symbol: `git_blob_id()` in `scripts/ci/check_manifest_blob_pins.py`.

Implementation:

```python
header = b"blob " + str(len(data)).encode("ascii") + b"\0"
return hashlib.sha1(header + data).hexdigest()
```

This correctly implements:

`SHA-1("blob " + decimal_byte_length + NUL + bytes)`

It does not use ordinary SHA-1 of file contents or SHA-256.

**Result: PASS.**

### 2.3 Mismatching declarations

Relevant symbols: `main()` and `emit_failure()`.

`main()` retrieves the declared digest from the authorized manifest field, obtains the referenced Git-tree bytes, calculates their Git blob ID and compares the calculated value against the declaration.

The comparison is:

```python
if actual.lower() != declared_value.lower():
```

A mismatch increments `failures` and emits a diagnostic containing both values.

The function returns exit code 1 when failures exist.

**Result: PASS.**

### 2.4 Missing referenced paths

Relevant symbol: `tree_bytes()`.

A missing Git object, invalid path or non-blob object produces `None`.

Relevant symbol: `main()`.

A `None` result produces:

```text
(declared=<digest>; actual=MISSING)
```

The failure counter is incremented.

The checker therefore does not silently accept a missing referenced file.

**Result: PASS.**

### 2.5 Missing manifests

Relevant symbols: `main()` and `tree_bytes()`.

Before checking individual pins, `main()` loads both manifest paths listed in `AUTHORIZED_PINS`.

If either manifest cannot be obtained from the candidate tree, the checker emits an error and returns exit code 2.

It does not interpret an absent manifest as an empty mapping or successful zero-pin result.

It also rejects a non-mapping manifest root and YAML parsing failures.

The implementation does not discover manifests dynamically, but this is consistent with Owner A's closed authorization ruling: the two authorized manifests are fixed.

**Result: PASS for the authorized manifest set.**

### 2.6 Candidate identity qualification

Relevant symbol: `main()`.

The checker executes:

```python
git(root, "rev-parse", "--verify", "HEAD^{tree}")
```

This confirms that HEAD resolves to a Git tree, but the returned tree SHA is discarded.

The checker consequently establishes that its reads use HEAD, not that HEAD is the particular PR candidate SHA designated by the review.

That latter binding must be established by the workflow and exact-head evidence.

The workflow was not supplied.

**Result: PASS for HEAD-relative resolution; candidate-to-PR identity binding remains unverified.**

---

## 3. Question 2 — Is the closed 12-identity scope faithful to Owner A?

**Assessment: PASS at source-inspection level.**

Relevant symbol: `AUTHORIZED_PINS` in `scripts/ci/check_manifest_blob_pins.py`.

The authorization table contains exactly 12 entries:

- Six authored-index declarations in AID-2026-100.
- Three related-evidence declarations in AID-2026-100.
- Three source-file declarations in AID-2026-150.

The implementation uses explicit manifest paths, field paths and sibling path keys.

It does not recursively discover arbitrary path/digest relationships.

This is the correct implementation strategy for Owner A's v2 ruling.

### Excluded families

| Family | Source-level disposition |
|---|---|
| `prompt_file` / `prompt_sha256` | Excluded |
| `scope.changes[].path` | Excluded |
| Other path-only fields | Excluded |
| Generic `path` / `blob` inference | Excluded |
| `reconstructed_root_blob` | Excluded |
| `aid_100_evidence_blob` | Excluded |
| `aid_107_evidence_blob` | Excluded |
| `latest_applied_evidence_blob` | Excluded |

The checker never traverses these declarations to create additional findings.

### Out-of-scope mismatch behavior

Relevant test symbols:

- `test_out_of_scope_prompt_hash_and_scope_path_are_ignored()`
- `test_out_of_scope_digest_mismatch_does_not_change_result()`

The supplied tests add out-of-scope prompt and path-only declarations, and separately add an unrelated `path`/`blob` mismatch.

They expect successful checking without additional annotations.

This directly exercises the closed-set behavior.

There is no apparent mechanism by which an additional out-of-scope digest mismatch can expand `AUTHORIZED_PINS` automatically.

One qualification: the supplied tests do not exercise every excluded historical pathless declaration individually. Their exclusion is established primarily by the implementation's explicit authorization table, not by exhaustive fixture coverage.

**Conclusion:** The implementation follows the Owner A ruling. No scope-expansion defect is established in the supplied checker.

---

## 4. Question 3 — Do the tests prove what they claim?

**Assessment: Partially. The central integrity tests are useful, but the test suite does not establish the complete claimed regression coverage.**

### Test-by-test assessment

| Test symbol | What it establishes | Review |
|---|---|---|
| `test_authorization_table_contains_exactly_twelve_identities` | The authorized field identities equal the expected 12 identities | PASS, with qualification below |
| `test_main_equivalent_fixture_produces_exactly_twelve_items` | Twelve mismatching fixture declarations produce twelve findings | PASS for fixture behavior |
| `test_all_twelve_authorized_pins_are_individually_verified` | A fixture with twelve correctly calculated pins succeeds | PASS for fixture behavior |
| `test_out_of_scope_prompt_hash_and_scope_path_are_ignored` | Prompt and path-only declarations do not add findings | PASS |
| `test_out_of_scope_digest_mismatch_does_not_change_result` | An unrelated path/blob mismatch is ignored | PASS |
| `test_one_byte_mutation_inside_authorized_pin_is_caught` | Changed committed bytes produce a mismatch diagnostic | PASS |
| `test_deleted_authorized_path_is_caught_as_missing` | Deleting a referenced committed path produces a missing-path finding | PASS |
| `test_missing_required_manifest_exits_two` | Missing authorized manifest fails closed | PASS |
| `test_missing_repository_path_does_not_affect_other_pins` | One missing reference does not prevent checking the remaining pins | PASS |

### 4.1 Important fixture-coupling weakness

Relevant symbols:

- `Fixture.__init__()`
- `Fixture.write_manifests()`
- `test_all_twelve_authorized_pins_are_individually_verified()`

The fixture constructs the manifests by iterating over the implementation's own `AUTHORIZED_PINS` table.

It also obtains the associated sibling path key from that same table.

Consequently, a defect in the authorization table's path-key association can be reproduced consistently by the fixture.

For example, if an authorized digest field is accidentally associated with the wrong sibling path key, the fixture may construct a manifest matching that incorrect association and then report success.

The test:

`test_authorization_table_contains_exactly_twelve_identities()`

independently checks the 12 field identities, but its expected set contains only `(manifest, field_path)` pairs. It does not independently assert the complete `(manifest, field_path, path_key)` triples.

This means the test suite does not independently establish all twelve path-to-digest associations.

This is a genuine test-design weakness, not evidence that the current associations are incorrect.

### 4.2 Missing negative cases

The supplied suite does not contain explicit tests for:

1. Removing the sibling path key from an authorized declaration.
2. Removing the sibling digest key from an authorized declaration.
3. Replacing an authorized digest with a malformed 40-character value.
4. Replacing an authorized digest with a non-string value.
5. Explicitly checking all twelve authorized path-key associations against an independently authored expected table.

The implementation appears to handle missing path and digest declarations through `main()`, but the corresponding behavior is not established by the supplied regression suite.

### 4.3 Tests that cannot establish repository measurements

`test_main_equivalent_fixture_produces_exactly_twelve_items()` creates a synthetic repository.

It demonstrates that the checker can emit twelve failures for twelve synthetic mismatches.

It does not independently establish that the actual PR candidate has twelve failures.

That claim depends on the candidate-tree evidence and execution logs.

### 4.4 Pathless declaration coverage

The tests do not individually introduce all four historical pathless declarations and verify their exclusion.

The implementation's closed authorization table makes accidental inclusion unlikely, but the evidence should not characterize these four individual exclusions as independently regression-tested.

**Conclusion:** The nine tests provide meaningful evidence for the main checker behaviors, but they do not justify claiming complete coverage of all required negative and boundary cases.

---

## 5. Question 4 — Is the ratchet honest?

**Assessment: The supplied measurements are consistent with an honest exact-set ratchet, but its complete behavior cannot be independently verified from the supplied artifacts.**

### 5.1 Baseline

The supplied baseline contains exactly twelve identities.

They correspond to the twelve entries in Owner A's authorization table.

The candidate-tree resolution ledger reports:

- 12 declarations examined.
- 12 referenced paths resolved.
- 0 matching declarations.
- 12 mismatching declarations.

The baseline therefore has the expected cardinality and identity set.

### 5.2 Additional failure behavior

The required behavior is:

- Current failure set = baseline: exit 0.
- Current failure set contains a new item: exit 1.
- Current failure set omits an existing baseline item: exit 1.

The supplied `exact-head-verification.md` reports:

```text
baseline=12 current=12 regressions=0 fixed=0
ratchet: PASS - failure set matches the baseline exactly.
```

This establishes the reported result for one execution.

It does not establish how the ratchet behaves when the failure set changes.

The supplied `test_check_manifest_blob_pins.py` does not test ratchet behavior.

### 5.3 Checker crash behavior

The checker explicitly distinguishes:

- Exit 0: successful verification.
- Exit 1: actual integrity failures.
- Exit 2: incomplete execution or inability to verify.

Whether `gate_ratchet.py` treats exit 2 as a hard failure cannot be established without inspecting its implementation.

In particular, I cannot certify that an execution error cannot be misinterpreted as an empty failure set or successful ratchet comparison.

### 5.4 Required ratchet evidence

The following files were not supplied:

- `scripts/ci/gate_ratchet.py`
- `scripts/ci/test_gate_ratchet.py`

The reported regression log contains an execution of the ratchet against the current baseline, but not the required mutation and stale-baseline scenarios.

**Conclusion:** The observed baseline comparison is consistent with correct operation. The three critical ratchet properties remain unverified.

---

## 6. Findings

### Finding 1 — Supplied evidence is not bound to the designated review head

<badge color="danger">Blocking</badge>

**Files:**

- `14-ai-development/work-items/AID-2026-255/exact-head-verification.md` — `Head SHA`
- `14-ai-development/work-items/AID-2026-255/candidate-tree-resolution.md` — `Candidate commit`

**Observed discrepancy:**

The review dispatch identifies:

`6fed932dadcaa074ac18c30ad4b8c61e2cb9d813c`

Both supplied verification documents identify:

`f1319b32ad23a050f9f6092f10cb26e6478676cc`

These are different commits.

The candidate-tree ledger, test results, baseline result and regression-gate results therefore cannot be attributed to the designated review head.

**Required change:**

Provide the actual contents and verification evidence for `6fed932dadcaa074ac18c30ad4b8c61e2cb9d813c`.

At minimum:

1. Verify the exact head SHA.
2. Verify its Git tree SHA.
3. Re-run the checker and tests against that tree.
4. Re-run the exact-set ratchet.
5. Bind the results to the exact reviewed head.
6. Supply the corresponding CI run evidence when available.

Do not substitute the previously documented candidate.

### Finding 2 — Authorized sibling-key associations lack independent regression assertions

<badge color="warning">Required</badge>

**File:** `scripts/ci/test_check_manifest_blob_pins.py`

**Symbols:**

- `Fixture.__init__()`
- `test_authorization_table_contains_exactly_twelve_identities()`
- `test_all_twelve_authorized_pins_are_individually_verified()`

**Problem:**

The fixture constructs path/digest relationships using the implementation's own `AUTHORIZED_PINS` table.

The authorization-table test independently verifies field identities but does not independently verify their associated sibling path keys.

An incorrect path-key association could therefore survive the existing positive fixture tests.

**Required change:**

Add an independently authored expected mapping of all twelve complete identities:

`(manifest_path, field_path, sibling_path_key)`

Assert equality against the implementation's complete authorization table.

The expected mapping must not be generated from `AUTHORIZED_PINS`.

Also add explicit negative tests for:

- Missing authorized sibling path.
- Missing authorized sibling digest.

Each must assert exit 1 and the corresponding stable identity and diagnostic.

### Finding 3 — Ratchet mutation and fail-closed behavior are not established by supplied evidence

<badge color="warning">Required evidence</badge>

**File:** `scripts/ci/test_check_manifest_blob_pins.py`

**Symbol:** `ClosedAuthorizationTests`

**Problem:**

The supplied checker tests do not exercise the ratchet.

The supplied verification log demonstrates only the current 12-versus-12 comparison.

It does not establish:

- New failure rejection.
- Stale baseline rejection after fixing an existing failure.
- Checker exit 2 rejection.

The actual ratchet implementation and self-tests were not supplied, so I cannot determine whether these behaviors are already correct.

**Required change:**

Supply the existing ratchet implementation and self-test source, together with execution evidence for all three scenarios.

Do not modify ratchet semantics merely to satisfy this review.

---

## 7. Questions for the orchestrator

These are evidence requests, not additional code findings.

1. Is `6fed932d` the intended final PR head, and why do the supplied evidence documents identify `f1319b32` instead?
2. Can the complete `.github/workflows/aid-2026-255-manifest-blob-pins.yml` be supplied?
3. Can `gate_ratchet.py` and `test_gate_ratchet.py` be supplied verbatim?
4. Can the actual `negative-fixtures.log`, `positive-legal-pin.log` and complete `regression-gates.log` be supplied?
5. Can the workflow check-run records for the exact reviewed head be supplied?

**CI disposition: PENDING.**

The dispatch explicitly reports zero workflow runs. Missing checks are an evidence gap, not a demonstrated implementation defect. They must not be represented as successful checks.

The reported `check_traceability.py` failure is attributed by the implementation evidence to a registry missing on the comparison base. I cannot independently confirm that attribution without the repository.

---

## 8. Verdict

# ACCEPT WITH REQUIRED CHANGES

The supplied checker has a sound core implementation for the Owner-A-authorized twelve Git blob declarations.

In particular:

- It reads committed Git-tree bytes.
- It correctly computes Git blob SHA-1.
- It detects mismatches.
- It detects missing referenced paths.
- It fails closed when an authorized manifest is unavailable.
- It implements a closed twelve-identity authorization table.
- It does not expand into the excluded prompt, path-only or pathless digest families.

However, acceptance of this exact implementation head is blocked by the mismatch between the designated review SHA and the SHA documented by the supplied evidence.

The tests also need stronger independent assertions for sibling-key associations, and the ratchet's regression properties remain unverified.

**No Owner acceptance is granted or implied by this review. Only Owner A may accept AID-2026-255.**
