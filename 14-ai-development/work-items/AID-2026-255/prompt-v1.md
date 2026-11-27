# IMMUTABLE IMPLEMENTATION PROMPT V1
# AID-2026-255 鈥?Manifest Blob Pin Integrity Ratchet

Repository: oahcom/AiMemoryBrainArchitecture
Default branch: main
Implementation issue: #1350
Defect issue: #1349
Work Item: AID-2026-255
Accountable Owner: Owner A
Implementer: Independent Implementation Session
Independent Reviewer: Separate Independent CI/Governance Reviewer
Acceptance Authority: Owner A

## 1. Mission

Implement a manifest blob-integrity checker and integrate it with the repository's existing exact-set ratchet.

The checker must independently calculate the identity of actual committed bytes for every applicable path-and-digest declaration.

The initial measured state at main commit:

`f18adc9fa1d06837433a09498f5297bf13b35756`

is:

- 15 applicable declarations.
- 3 matching declarations.
- 12 mismatching declarations.
- 9 mismatches in AID-2026-100.
- 3 mismatches in AID-2026-150.

These 12 known failures constitute the initial ratchet baseline.

Do not repair them in this implementation.

## 2. Mandatory reading

Before implementation, read the complete contents of:

1. `scripts/ci/check_manifest_parse.py`
2. `scripts/ci/gate_ratchet.py`
3. `scripts/ci/test_gate_ratchet.py`
4. `.github/workflows/gates.yml`
5. `scripts/ci/baselines/bilingual-docs.txt`
6. `14-ai-development/work-items/INDEX.md`

Then inspect:

7. Every committed `14-ai-development/work-items/*/manifest.yaml`.
8. Definitions of `root_blob`, `en_mirror_blob`, `zh_cn_mirror_blob`, `related_evidence`, `source.files`, `evidence_blob`, `prompt_sha256`, and other discovered reference fields.
9. Existing bilingual documentation gate implementation.
10. Existing workflow naming and required-check conventions.
11. Existing work-item manifests for prompt and evidence registration conventions.

Do not assume a field's meaning from its name alone.

## 3. Semantic contract

Use READING 3: TREE-RELATIVE EXACT-SET RATCHET.

The checker evaluates the candidate Git tree containing each manifest.

It must recompute the digest using the actual bytes from that tree.

The ratchet temporarily tolerates exactly the 12 measured existing failures.

It must reject:

- A new mismatch.
- A new missing path.
- A new malformed applicable declaration.
- A previously failing baseline item that unexpectedly stops failing without its baseline entry being removed.

The checker itself must report the actual failure set. It must not implement exemptions internally.

## 4. Git blob IDs and SHA-256

Two distinct algorithms are mandatory.

### Git blob ID

A 40-character hexadecimal Git blob ID means:

`SHA-1("blob " + decimal_byte_length + NUL + bytes)`

Use the Git object semantics, preferably through:

```bash
git hash-object --stdin
```

Equivalent computation is:

```python
hashlib.sha1(
    b"blob " + str(len(data)).encode("ascii") + b"\0" + data
).hexdigest()
```

Do not calculate ordinary SHA-1 of file contents.

Do not calculate SHA-256 for a Git blob ID.

### SHA-256

A 64-character SHA-256 declaration must use the documented byte representation.

Mandatory discovery targets:

- `*_sha256`
- `prompt_sha256`
- `model_blob_sha256_lf`

For ordinary raw-byte SHA-256:

```python
hashlib.sha256(data).hexdigest()
```

For any LF-normalized representation, inspect the defining contract and implement that exact transformation before hashing.

Do not infer normalization solely from the suffix.

### Byte counts

`prompt_bytes` is a count, not a digest.

It is outside the blob-integrity checker.

Do not expand this task into general count validation.

## 5. Sibling-key pairing

Discover path-and-digest relationships by sibling keys within the same YAML mapping.

Mandatory pairs:

| Path key | Digest key |
|---|---|
| `root` | `root_blob` |
| `en_mirror` | `en_mirror_blob` |
| `zh_cn_mirror` | `zh_cn_mirror_blob` |
| `path` | `blob` |
| `evidence_file` | `evidence_blob` |
| `prompt_file` | `prompt_sha256` |

Apply recursively to nested mappings and sequence members.

Do not pair a digest with a path found elsewhere in the manifest merely because the names look related.

Discover all additional applicable sibling-key pairs in the repository.

For every pair:

1. Extract the path from its sibling path key.
2. Extract the digest from its sibling digest key.
3. Resolve the path against the candidate tree.
4. Read the actual bytes.
5. Identify the correct digest algorithm.
6. Recompute the digest.
7. Compare the result with the declaration.

A missing path is a failure.

A mismatching digest is a failure.

An incomplete applicable pair is a failure.

## 6. Pathless digest fields

Explicitly inventory these observed fields:

- `reconstructed_root_blob`
- `aid_100_evidence_blob`
- `aid_107_evidence_blob`
- `latest_applied_evidence_blob`

The measured declarations do not have corresponding sibling path keys.

`reconstructed_root_blob` refers to an artifact removed from the original scope by an Owner ruling.

The other three are bare digest declarations without an identifiable path in their mapping.

Rules:

1. Do not invent paths.
2. Do not search arbitrary repository files for matching digests.
3. Do not associate unrelated paths.
4. Record their exact locations and definitions.
5. Classify them as pathless/unverifiable under the tree-relative contract.
6. Do not count them as verified.
7. If their governing definition establishes a required current-tree path, classify them as incomplete applicable declarations and reject them.
8. Do not turn unrelated inline-content digests into repository blob references.

The evidence must explain each classification.

## 7. Checker files

Create:

```text
scripts/ci/check_manifest_blob_pins.py
scripts/ci/test_check_manifest_blob_pins.py
```

Follow `scripts/ci/check_manifest_parse.py` conventions.

Required behavior:

- Module docstring explaining the defect being closed.
- Explicit Deliberate ceiling.
- Deterministic manifest discovery.
- Strict handling of applicable declaration shapes.
- Candidate-tree identity verification.
- Actual Git-tree byte resolution.
- Git blob ID support.
- SHA-256 support.
- Actionable diagnostics.
- GitHub `::error::` annotations.
- One-line success summary.
- No new third-party dependencies.
- PyYAML only, reusing existing dependency availability.

Exit codes:

| Code | Meaning |
|---|---|
| 0 | All applicable pins match |
| 1 | One or more actual integrity violations |
| 2 | Nothing verified, usage error, or incomplete execution |

If no applicable pins exist, print:

`No applicable blob pins found; nothing was verified.`

Also emit a GitHub error annotation and exit 2.

Never interpret zero pins as PASS.

## 8. Failure output contract

The checker must emit one deterministic stdout item per applicable failure.

The item identity must include:

- Manifest path.
- Full dotted field path, including sequence indices.
- Referenced repository path.

Use this format:

```text
::error::<manifest-path>#<dotted-field-path> -> <referenced-path> (declared=<digest>; actual=<digest>)
```

For missing paths:

```text
::error::<manifest-path>#<dotted-field-path> -> <referenced-path> (declared=<digest>; actual=MISSING)
```

For incomplete declarations, identify the missing sibling and the affected field.

The item identity before ` -> ` must remain deterministic.

The actual diagnostic must retain declared and actual values.

The output must be compatible with:

```bash
python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/manifest-blob-pins.txt \
  --format paths \
  --command "python3 scripts/ci/check_manifest_blob_pins.py"
```

The baseline entries must match the stable item identity before ` -> `.

Do not put timestamps, random IDs, temporary directories, or nondeterministic data in the item identity.

## 9. Initial baseline

Create:

`scripts/ci/baselines/manifest-blob-pins.txt`

The initial baseline contains exactly these 12 entries:

```text
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[0].root_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[0].en_mirror_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[0].zh_cn_mirror_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[1].root_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[1].en_mirror_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#baseline_and_source_evidence.authored_indexes[1].zh_cn_mirror_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#related_evidence[0].blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#related_evidence[0].en_mirror_blob
::error::14-ai-development/work-items/AID-2026-100/manifest.yaml#related_evidence[0].zh_cn_mirror_blob
::error::14-ai-development/work-items/AID-2026-150/manifest.yaml#source.files[0].blob
::error::14-ai-development/work-items/AID-2026-150/manifest.yaml#source.files[1].blob
::error::14-ai-development/work-items/AID-2026-150/manifest.yaml#source.files[2].blob
```

The baseline format is one stable failure identity per line.

The exact-set comparison is performed by the existing ratchet.

Do not modify the existing baseline entries for unrelated gates.

## 10. Required tests

Implement isolated regression tests.

### Positive

1. Valid Git blob ID.
2. Valid SHA-256 declaration.
3. Valid nested sibling pair.
4. Valid list of references.
5. Multiple legal pins in one manifest.
6. Legal pins produce no false-positive annotations.
7. Non-blob scalar values remain outside scope.
8. Pathless historical declarations are classified correctly.

### Negative

9. Modify exactly one byte of a referenced file while retaining its original digest.
   - Expected: exit 1.
   - Expected diagnostic: declared and actual values.

10. Delete a referenced file while retaining its manifest declaration.
    - Expected: exit 1.
    - Expected diagnostic: missing path.

11. Remove a required sibling path from an applicable pair.
    - Expected: exit 1.

12. Remove a required sibling digest from an applicable pair.
    - Expected: exit 1.

13. Introduce one additional mismatch beyond the baseline.
    - Expected: ratchet exit 1.

14. Fix one baseline item without updating the baseline.
    - Expected: ratchet exit 1 due to stale baseline.

### Boundary

15. Inline-content SHA-256 without a repository path.
    - Expected: no false-positive blob failure.

16. Zero applicable pins.
    - Expected: checker exit 2.
    - Expected explicit nothing-verified diagnostic.

17. Git blob ID must not be calculated as plain SHA-1 or SHA-256.

Use temporary repositories or isolated fixtures.

Do not mutate committed historical manifests for tests.

## 11. Ratchet integration

Do not convert this gate into a hard gate.

Use the existing:

`scripts/ci/gate_ratchet.py`

Use the new:

`scripts/ci/baselines/manifest-blob-pins.txt`

Invocation:

```bash
python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/manifest-blob-pins.txt \
  --format paths \
  --command "python3 scripts/ci/check_manifest_blob_pins.py"
```

The existing wrapper's contract must remain intact.

Do not create a new ratchet framework.

Do not weaken existing ratchets.

If a necessary change to `gate_ratchet.py` is unavoidable, document it, add regression tests, and justify why the existing interface cannot satisfy this contract. Do not change its comparison semantics casually.

## 12. CI workflow

Create:

`.github/workflows/aid-2026-255-manifest-blob-pins.yml`

Required:

- Trigger on `pull_request` targeting main.
- Trigger on `push` to main.
- No path filtering.
- Use `actions/checkout@v4` without an explicit ref for pull requests.
- Verify checkout SHA against `github.sha`.
- Execute the checker through the exact-set ratchet.
- Run checker tests.
- Run the ratchet's existing self-tests.
- Use a distinct job/check name.
- Do not modify unrelated workflow jobs.

No `merge_group` integration is needed because the measured repository has no merge queue configuration or existing merge-group workflow.

The workflow must use the actual PR merge-candidate tree.

## 13. Work-item and evidence files

Under:

`14-ai-development/work-items/AID-2026-255/`

Create:

```text
manifest.yaml
prompt-v1.md
session-evidence.md
blob-field-inventory.md
candidate-tree-resolution.md
blob-rehash-ledger.tsv
negative-fixtures.md
negative-mismatch.log
negative-missing.log
positive-legal-pin.log
exact-head-verification.md
regression-gates.log
```

`prompt-v1.md` must be byte-identical to this committed immutable prompt.

The manifest must follow the current repository's work-item conventions.

Register AID-2026-255 in:

`14-ai-development/work-items/INDEX.md`

Do not create an unrelated normative document.

### blob-field-inventory.md

Include:

- Exact field.
- Defining document and location.
- Manifest occurrence.
- Actual shape.
- Sibling path key.
- Digest key.
- Algorithm.
- Applicable/excluded classification.
- Reason for classification.

### candidate-tree-resolution.md

Include every applicable declaration and its actual candidate-tree resolution.

### blob-rehash-ledger.tsv

Required columns:

```text
manifest_path	field_path	referenced_path	algorithm	declared_digest	actual_digest	result
```

### negative-fixtures.md

Record the deliberate one-byte mutation and deletion tests.

### exact-head-verification.md

Record actual:

- Base SHA.
- PR head SHA.
- Candidate SHA.
- Git tree SHA.
- Workflow run ID.
- Checker invocation.
- Independent reviewer identity.
- Reviewed head SHA.

Never invent values.

## 14. Verification commands

Execute:

```bash
python3 scripts/ci/check_manifest_parse.py

python3 scripts/ci/check_manifest_blob_pins.py

python3 scripts/ci/test_check_manifest_blob_pins.py

python3 scripts/ci/test_gate_ratchet.py

python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/manifest-blob-pins.txt \
  --format paths \
  --command "python3 scripts/ci/check_manifest_blob_pins.py"

python3 scripts/check_traceability.py

python3 scripts/check_repository_hygiene.py
```

Also execute the repository's actual bilingual documentation verification command, discovered from the existing workflow.

Record all outputs and exit codes.

The direct checker is expected to return 1 on the initial known-red main tree.

The ratchet is expected to return 0 when and only when its current failure set exactly matches the 12-item baseline.

This distinction is mandatory.

## 15. Branch and PR

Branch:

```text
work/AID-2026-255-manifest-blob-pin-integrity
```

Create from the latest verified origin/main.

Open one PR against main.

Do not modify other open branches.

## 16. Forbidden actions

- Do not modify main directly.
- Do not merge the PR.
- Do not repair the 12 existing pins in this task.
- Do not renumber any existing work item.
- Do not edit the eight existing open PR branches.
- Do not use SHA-256 for Git blob IDs.
- Do not use plain SHA-1 for Git blob IDs.
- Do not resolve paths through guesses.
- Do not silently skip applicable declarations.
- Do not count pathless declarations as verified.
- Do not turn the ratchet into an exemption that accepts arbitrary new failures.
- Do not make the gate hard while main has known failures.
- Do not introduce unrelated schema validation.
- Do not weaken existing CI.
- Do not self-review.
- Do not claim Owner acceptance.
- Do not invent SHAs or test results.
- Do not modify this prompt after commitment.

## 17. Completion condition

Implementation is complete only when:

1. All applicable declaration families are inventoried.
2. Git blob IDs and SHA-256 values use the correct algorithms.
3. Every applicable path resolves against the candidate tree.
4. The deliberate one-byte mutation is rejected.
5. The deliberate deletion is rejected.
6. Legal pins pass.
7. Pathless declarations are explicitly classified.
8. The 12-item baseline matches the measured initial failure set.
9. Additional failures make the ratchet red.
10. Fixed baseline items make the ratchet red until the baseline is lowered.
11. Existing regression checks pass.
12. Evidence is bound to the final candidate SHA.
13. An independent reviewer reviews that exact final head.

Submit the PR and all evidence to Owner A.

Only Owner A may accept the implementation.
