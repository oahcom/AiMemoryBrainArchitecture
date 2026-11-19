# Phase 3.8 H-RJ-HW-01 — Typed Watermark and Fence Binding Contract
# Phase 3.8 H-RJ-HW-01 — 类型化高水位与 Fence 绑定契约

- **Document ID:** `PHASE-3.8-H-RJ-HW-01-TYPED-WATERMARK-AND-FENCE-BINDING-CONTRACT`
- **Status:** `CANDIDATE DESIGN RECORD; IMPLEMENTATION NOT VERIFIED; EXACT-HEAD CI NOT RUN`
- **Scope:** H-RJ-HW-01, ProducerRegistrationHighWater, ForgetFenceGeneration, Owner Snapshot Validator Contract, RecoveryJoin schema and runtime conformance.
- **Upstream authority:** Issue #25, registered remediation design comment `7006145800`, originating from dispatch `REMEDIATE-HRJHW01-001` (session `6afecafc`).
- **Basis pins:**
  - Main baseline HEAD: `4c38ae25b71383d661e4179622cafa04b66a046a`
  - H implementation branch: `session-h-bmcp-protocol` (not merged into main).
  - Schema Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`
  - RJ102 tests Blob: `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a`
  - Composed runtime Blob: `e26379d38825ee13d15f652d3bd019c4091da37d`
  - Validator 1.2.17 Blob: `17275eebd0013f8ad8765670a7faaa40866d99d8`
  - D control contract Blob: `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- **Non-claims:** This document does not claim Owner approval, implementation completion, schema deployment, validator unification, test execution, exact-head CI success, Storage conformance, production conformance, human R3 approval, production activation, or platform-independent gate completion.

## 1. Document identity and status

### 1.1 Normative identity

This document defines the candidate typed-watermark and fence-binding contract for Finding `H-RJ-HW-01`.

The Finding remains:

| Attribute | Value |
|---|---|
| Finding | `H-RJ-HW-01` |
| Severity | `P1` |
| Status | `OPEN` |
| Validation | `TO_VALIDATE` |
| Disposition | `HOLD` |
| Implementation status | `NOT VERIFIED` |
| Exact-head CI | `NOT RUN` |

The document is a versioned, single-file bilingual contract record. Its English and Chinese sections express the same requirements.

The recommended shared contract version is:

`OWNER-SNAPSHOT-CONTRACT-1.2.18`

This is a proposed version number, not a released or adopted version.

### 1.2 Normative interpretation

The following result values have distinct meanings:

- `VALID`: All required authoritative, type, namespace, equality, signature and currentness checks have succeeded.
- `INVALID`: A definite contradiction, malformed value, invalid signature, prohibited substitution or failed normative binding has been established.
- `UNKNOWN`: Required authoritative evidence is unavailable, incomplete or cannot be verified.

`UNKNOWN` MUST NOT be treated as `VALID`.

`NOT RUN` MUST NOT be treated as `PASS`.

`NOT_SUPPLIED` MUST NOT be treated as verified.

`ADVANCEABLE` MUST NOT be represented as `CLOSED`.

### 1.3 Closure conditions

| Condition | Current state | Coverage of this contract | Remaining gap | Blocking responsibility |
|---|---|---|---|---|
| 1. Exact ProducerRegistrationHighWater type, namespace and snapshot equality | ADVANCEABLE | Typed binding, fields, unique equality, sequence comparison and judgment rules | D-authoritative naming of `producer_registration_sequence_namespace_ref` and its actual snapshot/proof implementation have not been supplied | D Owner + H Owner |
| 2. Independent ForgetFenceGeneration type, ForgetOperation/target-set binding and currentness proof | ADVANCEABLE | Schema additions, currentness proof, judgment order and INVALID/UNKNOWN rules | Authoritative D Fence Currentness Proof format, signature and query interface have not been supplied | D Owner + H Owner |
| 3. Validator allowlist divergence and unique composition path | ADVANCEABLE | Shared allowlist recommendation, files, functions, modification regions and versioning rules | Actual modifications, imports, regression tests and composition-path implementation have not occurred | H Owner |
| 4. Four categories of new tests and dual-validator composition tests | ADVANCEABLE | Executable test vectors V01–V24 and ownership recommendations | Test code, fixtures, assertions and execution results have not been supplied | H Owner |
| 5. Exact-head CI Run, Job and test report | BLOCKED | Minimum evidence requirements and alternative local evidence checklist | No repaired exact HEAD, workflow, Run, Job or raw log is available | H Owner / CI responsibility role |
| 6. Same-version Storage field mapping verification | BLOCKED / NOT_SUPPLIED | Same-version criteria and field-level verification table | Storage JoinProof same-version schema, manifest, field mapping and direct verification materials have not been supplied | Storage Owner + H Owner |

State interpretation:

- `ADVANCEABLE`: Technical design may proceed to implementation. It does not mean the condition is satisfied.
- `BLOCKED`: Required evidence is missing and cannot be inferred. Design text cannot substitute for that evidence.
- `CLOSED`: No closure condition has reached `CLOSED` in this record.

Condition 5 MUST NOT become CLOSED because of historical CI success.

Condition 6 MUST NOT become CLOSED because of historical Issue #29 comments or similarly named fields in other versions.

## 2. Problem statement (F1/F2/F3 with measured evidence)

### 2.1 Finding and measured conclusions

Finding `H-RJ-HW-01` concerns D/E/I/Storage atomic producer admission and derivative visibility gating.

The three independently evidenced defects are:

| Defect | Measured conclusion | Required technical treatment |
|---|---|---|
| F1 — Validator allowlist divergence | The three Owner-domain field sets have mutually incompatible exact-set semantics and cannot simultaneously pass | Establish a shared versioned allowlist |
| F2 — Incorrect composed validation path | `validate_union()` invokes only the local validator; validator 1.2.17 does not participate in composed validation | Unify through a shared implementation and a unique composition entry point |
| F3 — D dual-high-water binding failure | Generic high-water is bound to `admission_high_water`, not the D Producer Registration high-water; Fence Generation lacks a snapshot carrier | Add type, namespace, snapshot equality and currentness bindings |

F1, F2 and F3 are independently supported by source and behavioral probes in the supplied evidence package. They are not conclusions inferred solely from the original Finding description.

### 2.2 Measured probe evidence

All 17 mechanical probes passed:

| Probe group | Probes | Measured scope |
|---|---|---|
| A | A1–A7 | Allowlist divergence |
| B | B1–B3 | Composed validator dispatch path |
| C | C1–C4 | ProducerRegistrationHighWater binding |
| D | D1–D2 | Type-validation differences |
| E | E1–E2 | Behavioral positive and negative cases |

Important measured result:

**E1 demonstrated that the composed path accepts a non-decimal `producer_registration_high_water` value and returns `VALID`.**

These probes establish defects in the examined source. They do not establish that a repair has been implemented.

### 2.3 Core design principles

1. `ProducerRegistrationHighWater` and `ForgetFenceGeneration` MUST be two different nominal types.
2. They MUST have different ledgers, namespaces, semantics and comparison domains.
3. Equal decimal strings MUST NOT establish equal types or equal provenance.
4. Only typed values supported by the corresponding Owner-authoritative proof MAY participate in cutoff judgments.
5. `UNKNOWN` MUST NOT be converted into `VALID`.
6. H schema extensions MUST NOT weaken the non-interchangeability requirement in D control contract §3.

## 3. Normative type: ProducerRegistrationHighWater

### 3.1 Definition

`ProducerRegistrationHighWater` is defined as:

> A D-owner-specific decimal counter representing the frozen admission cutoff of the ProducerWork Registration Ledger for one Canonical Memory Authority and one ForgetOperation context.

Its normative attributes are:

| Attribute | Required meaning |
|---|---|
| Owner | D |
| Ledger | ProducerWork Registration Ledger |
| Semantics | ProducerWork registration ordering |
| Purpose | ProducerWork cutoff for a specific ForgetOperation |
| Scope | Corresponding Canonical Memory Authority |
| Type | D-specific monotonic decimal counter |

It MUST NOT be interpreted as any of the following:

- Generic Admission HighWater.
- CanonicalCommitCursor.
- ForgetFenceGeneration.
- PermissionEpoch.
- I ProducerDomainInventoryEpoch.
- Storage Commit Position.

### 3.2 Namespace field

The snapshot MUST introduce:

`producer_registration_sequence_namespace_ref`

Type:

`$defs/ref`

This field represents the D Owner-authoritatively registered ProducerWork Registration Ledger sequence namespace.

Normative requirements:

1. Every Canonical Memory Authority MUST have a unique and stable D ProducerWork Registration Ledger namespace reference.
2. The namespace reference MUST be supplied by D Owner. H MUST NOT derive it from another counter.
3. The namespace reference MUST be bound to ledger identity and authority identity.
4. I inventory namespace, Storage namespace, ForgetFence namespace and generic admission namespace MUST NOT substitute for it.
5. The namespace reference MUST remain equal across snapshot, membership proof and admission row.

### 3.3 Relationship to `owner_sequence_namespace`

The only legal binding is:

```python
proof["owner_sequence_namespace"] \
    == row["owner_sequence_namespace"] \
    == snapshot["producer_registration_sequence_namespace_ref"]
```

Additionally:

```python
proof["owner_kind"] == "D"
row["owner_kind"] == "D"
snapshot["owner"] == "D"
```

Any inequality MUST produce `INVALID`.

The actual D-authoritative namespace URI/identifier encoding syntax is `NOT_SUPPLIED` in this package.

This contract therefore specifies the unique reference field and its equality relationship. It does not fabricate an existing D namespace string.

D Owner MUST supply the formal namespace identifier format, authority binding and canonicalization rules before implementation.

### 3.4 Snapshot and membership proof fields

The D snapshot MUST retain:

```json
{
  "producer_registration_high_water": "123"
}
```

The snapshot MUST add:

```json
{
  "producer_registration_sequence_namespace_ref": "d-producer-registration-ledger-namespace-ref"
}
```

The membership proof MUST add:

```json
{
  "producer_registration_sequence_namespace_ref": "d-producer-registration-ledger-namespace-ref",
  "producer_registration_high_water": "123"
}
```

These strings are structural examples only. They do not represent an existing real D namespace reference.

### 3.5 Unique equality

For a D admission row:

```python
proof["owner_high_water"] \
    == proof["producer_registration_high_water"] \
    == snapshot["owner_specific_high_waters"][
        "producer_registration_high_water"
    ]
```

Additionally:

```python
row["owner_high_water"] == proof["owner_high_water"]
```

The complete binding is:

```python
row["owner_high_water"] \
    == proof["owner_high_water"] \
    == proof["producer_registration_high_water"] \
    == snapshot["owner_specific_high_waters"][
        "producer_registration_high_water"
    ]
```

This is the only permitted conversion entry point from the generic D counter to the typed counter.

The following MUST NOT substitute for this equality:

```python
proof["owner_high_water"] == snapshot["admission_high_water"]
```

Nor may the following substitute:

```python
proof["owner_high_water"] == snapshot["work_item_high_water"]
```

Equal numeric strings in two fields MUST NOT establish that those fields belong to the same ledger.

### 3.6 ProducerRegistrationHighWater judgment table

| Condition | Result | Reason |
|---|---|---|
| Snapshot explicitly exists, but `producer_registration_high_water` differs from proof | INVALID | An authoritative value conflicts |
| `owner_high_water` differs from the typed value | INVALID | Unique binding equality is violated |
| Namespace references differ | INVALID | Explicit cross-ledger or cross-domain binding |
| Owner is not D | INVALID | Type-domain violation |
| Counter is a non-decimal string | INVALID | Type does not satisfy DECIMAL |
| Counter is negative or non-canonical decimal form | INVALID | Counter format violation |
| Snapshot is missing | UNKNOWN | Authoritative material is unavailable |
| Snapshot currentness cannot be proven | UNKNOWN | Current authoritative state cannot be confirmed |
| Proof is missing | UNKNOWN | Membership evidence is missing |
| Verifier returns UNKNOWN | UNKNOWN | Verification result is undetermined |
| Verifier explicitly rejects the signature | INVALID | Authoritative proof is invalid |

**A definite conflict between present fields MUST produce INVALID. It MUST NOT be concealed by returning UNKNOWN.**

### 3.7 Sequence cutoff

The existing membership proof comparison:

```python
owner_local_sequence <= owner_high_water
```

MUST retain its behavior while its D-domain semantics converge to:

```python
owner_local_sequence \
    <= producer_registration_high_water
```

Within the D domain:

```python
owner_local_sequence <= snapshot[
    "owner_specific_high_waters"
]["producer_registration_high_water"]
```

There MUST NOT be a second independent cutoff truth.

`owner_high_water` is only a generic proof-envelope field. Its D-domain meaning is established by the unique equality above.

A generic cutoff and a separate D cutoff MUST NOT be maintained as independently acceptable values.

## 4. Namespace binding and unique equality

### 4.1 Required namespace identity

`producer_registration_sequence_namespace_ref` identifies the D ProducerWork Registration Ledger namespace.

The following identities MUST remain distinct:

- D ProducerWork Registration Ledger namespace.
- ForgetFence namespace.
- I ProducerDomainInventory namespace.
- Storage namespace.
- Generic admission namespace.

A namespace reference MUST be validated as an identity binding, not merely as a non-empty string.

### 4.2 Snapshot, proof and row binding

The required three-party namespace equality is:

```python
proof["owner_sequence_namespace"] \
    == row["owner_sequence_namespace"] \
    == snapshot["producer_registration_sequence_namespace_ref"]
```

The required Owner identity is:

```python
proof["owner_kind"] == "D"
row["owner_kind"] == "D"
snapshot["owner"] == "D"
```

The required high-water equality is:

```python
row["owner_high_water"] \
    == proof["owner_high_water"] \
    == proof["producer_registration_high_water"] \
    == snapshot["owner_specific_high_waters"][
        "producer_registration_high_water"
    ]
```

All equalities are mandatory.

### 4.3 Judgment order

The normative D producer-admission judgment order is:

1. Validate that owner is D.
2. Validate snapshot completeness and currentness.
3. Validate namespace identity.
4. Validate typed counter format.
5. Validate generic counter format.
6. Validate unique equality.
7. Validate `owner_local_sequence <= producer_registration_high_water`.
8. Validate membership proof signature.
9. Validate other admission-row, proof and snapshot bindings.

Any definite conflict MUST produce `INVALID` before a successful signature result can establish validity.

### 4.4 Missing authoritative namespace material

The actual D namespace identifier format and canonicalization are `NOT_SUPPLIED`.

A proposed example namespace string MUST NOT be represented as an authoritative identifier.

Until D Owner supplies the required namespace authority material, the corresponding authority-dependent verification remains unavailable.

## 5. Normative type: ForgetFenceGeneration

### 5.1 Definition

The independent nominal type is:

`ForgetFenceGeneration`

Its normative definition is:

> A D-owner-issued monotonic generation counter in the ForgetFence namespace, scoped to the authoritative ForgetFence ordering and bound to one ForgetOperation and one immutable target-set digest.

`ForgetFenceGeneration` is not `ProducerRegistrationHighWater`.

Even when their numeric values are equal, they MUST NOT substitute for each other.

D control contract §3 defines:

```text
ForgetFenceCursor =
(forget_operation_id, fence_generation, target_set_digest)
```

Therefore, FenceGeneration MUST be validated together with its ForgetOperation and target set.

### 5.2 Existing schema deficiency

The RecoveryJoin 1.0.2 schema has the following deficiencies:

- `ownerSnapshot` does not contain ForgetFenceGeneration high-water.
- Membership proof does not contain the corresponding typed field.
- `fence_generation` exists only in the owner-evidence Forget branch.
- Validator 1.2.17's `forget_fence_generation_high_water` has no corresponding snapshot carrier in the schema.

### 5.3 Schema addition A — `forgetFenceGeneration`

The schema `$defs` MUST add:

```json
{
  "forgetFenceGeneration": {
    "type": "string",
    "pattern": "^(0|[1-9][0-9]*)$"
  }
}
```

This primitive schema validates numeric format only.

The nominal type is established jointly by field location, owner, namespace and operation binding.

JSON Schema alone MUST NOT be claimed to implement the complete strong type.

### 5.4 Schema addition B — `forgetFenceCurrentnessProof`

The schema `$defs` MUST add:

```json
{
  "forgetFenceCurrentnessProof": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "proof_ref": {
        "$ref": "#/$defs/ref"
      },
      "proof_digest": {
        "$ref": "#/$defs/digest"
      },
      "owner_kind": {
        "const": "D"
      },
      "forget_operation_ref": {
        "$ref": "#/$defs/ref"
      },
      "target_set_digest": {
        "$ref": "#/$defs/digest"
      },
      "forget_fence_namespace_ref": {
        "$ref": "#/$defs/ref"
      },
      "forget_fence_generation": {
        "$ref": "#/$defs/forgetFenceGeneration"
      },
      "forget_fence_generation_high_water": {
        "$ref": "#/$defs/forgetFenceGeneration"
      },
      "producer_registration_high_water": {
        "$ref": "#/$defs/counter"
      },
      "owner_snapshot_ref": {
        "$ref": "#/$defs/ref"
      },
      "owner_snapshot_digest": {
        "$ref": "#/$defs/digest"
      },
      "owner_gate_generation": {
        "$ref": "#/$defs/counter"
      },
      "anti_rollback_anchor_ref": {
        "$ref": "#/$defs/ref"
      },
      "currentness_status": {
        "enum": [
          "CURRENT",
          "STALE",
          "UNKNOWN"
        ]
      },
      "signature_ref": {
        "$ref": "#/$defs/ref"
      }
    },
    "required": [
      "proof_ref",
      "proof_digest",
      "owner_kind",
      "forget_operation_ref",
      "target_set_digest",
      "forget_fence_namespace_ref",
      "forget_fence_generation",
      "forget_fence_generation_high_water",
      "producer_registration_high_water",
      "owner_snapshot_ref",
      "owner_snapshot_digest",
      "owner_gate_generation",
      "anti_rollback_anchor_ref",
      "currentness_status",
      "signature_ref"
    ]
  }
}
```

This structure is an H-side design proposal. It MUST NOT be represented as a proof already issued by D.

D Owner MUST confirm its authenticity, field sources, signature and query semantics.

### 5.5 Schema addition C — `ownerSnapshot`

The following fields MUST be added:

```json
{
  "forget_fence_namespace_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_generation_high_water": {
    "$ref": "#/$defs/forgetFenceGeneration"
  },
  "forget_fence_currentness_proof_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_currentness_proof_digest": {
    "$ref": "#/$defs/digest"
  }
}
```

These fields MUST be required for a D owner snapshot.

I/C snapshots MUST NOT be forced to provide these D-specific fields.

The D Owner snapshot MUST also retain:

```json
{
  "producer_registration_high_water": "123"
}
```

Both high-water values MUST coexist in the same D snapshot. They MUST NOT be merged into one field.

### 5.6 Schema addition D — `ownerSnapshotMembershipProof`

The following fields MUST be added:

```json
{
  "forget_fence_namespace_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_generation_high_water": {
    "$ref": "#/$defs/forgetFenceGeneration"
  },
  "forget_fence_currentness_proof_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_currentness_proof_digest": {
    "$ref": "#/$defs/digest"
  }
}
```

For `owner_kind == "D"`, these fields MUST be conditionally required.

Other Owners MUST NOT use these fields to establish a D Fence proof.

### 5.7 Schema addition E — owner evidence Forget branch

The existing fields MUST be retained:

```json
{
  "forget_operation_ref": "...",
  "fence_generation": "..."
}
```

The following fields MUST be added:

```json
{
  "target_set_digest": {
    "$ref": "#/$defs/digest"
  },
  "forget_fence_namespace_ref": {
    "$ref": "#/$defs/ref"
  }
}
```

For D `LINEAGE` and `BARRIER_MEMBERSHIP` evidence, both fields SHOULD be conditionally required.

### 5.8 Target-set digest and lineage manifest digest

These two digests MUST NOT be assumed equal.

Definitions:

- `target_set_digest`: Immutable target-set digest established when the Fence is installed.
- `lineage_manifest_digest`: Digest of the Lineage Manifest content.

They have different semantics.

The proposed binding is:

```python
evidence["target_set_digest"] \
    == currentness_proof["target_set_digest"]
```

```python
evidence["lineage_manifest_digest"] \
    == currentness_proof["lineage_manifest_digest"]
```

The second equality requires `lineage_manifest_digest` to be added to the currentness proof. This field is part of the proposed formal implementation.

The content relationship between the target set and Lineage Manifest is:

```text
LineageManifest.TargetSetDigest
    == ForgetFenceCursor.target_set_digest
```

This relationship MAY be accepted only when the D-authoritative Lineage Manifest explicitly declares the binding.

The following MUST NOT be used as a default rule:

```python
target_set_digest == lineage_manifest_digest
```

The complete D Lineage Manifest schema was not supplied. Its canonicalization and digest domain are therefore `NOT_SUPPLIED`.

### 5.9 Unique Fence binding

The only legal relationships are:

```python
evidence["fence_generation"] \
    == currentness_proof["forget_fence_generation"]
```

```python
evidence["forget_operation_ref"] \
    == currentness_proof["forget_operation_ref"]
```

```python
evidence["target_set_digest"] \
    == currentness_proof["target_set_digest"]
```

```python
evidence["forget_fence_namespace_ref"] \
    == currentness_proof["forget_fence_namespace_ref"]
```

Additionally:

```python
currentness_proof["forget_fence_generation"] \
    <= currentness_proof["forget_fence_generation_high_water"]
```

The high-water MUST belong to the ForgetFence namespace. It MUST NOT be sourced from the ProducerWork Registration Ledger.

## 6. Fence currentness proof and judgment order

### 6.1 Required verification order

The following order is mandatory:

1. Verify D Owner identity.
2. Verify ForgetOperation reference.
3. Verify target-set digest.
4. Verify Fence namespace reference.
5. Verify decimal formats of FenceGeneration and FenceGenerationHighWater.
6. Verify equality between `evidence.fence_generation` and `proof.fence_generation`.
7. Verify FenceGeneration does not exceed the high-water of its corresponding namespace.
8. Verify Owner snapshot reference and digest.
9. Verify anti-rollback anchor.
10. Verify proof signature.
11. Verify D Owner ledger currentness.
12. Verify `currentness_status`.

### 6.2 Judgment table

| Condition | Result |
|---|---|
| Generation exceeds corresponding high-water | INVALID |
| Operation reference differs | INVALID |
| `target_set_digest` differs | INVALID |
| Namespace differs | INVALID |
| Proof generation differs from evidence generation | INVALID |
| Explicitly returns STALE | INVALID |
| Signature explicitly rejected | INVALID |
| Currentness proof is missing | UNKNOWN |
| Currentness query is unavailable | UNKNOWN |
| `currentness_status` is UNKNOWN | UNKNOWN |
| Anti-rollback cannot be verified | UNKNOWN |
| All checks pass and currentness is CURRENT | VALID |

### 6.3 Currentness requirement

**Merely proving that FenceGeneration is numerically below some high-water MUST NOT be considered proof that it is the latest applicable Fence.**

Currentness MUST be established by a D-authoritative currentness proof.

H MUST NOT infer currentness by independently comparing several counters.

The currentness proof structure in §5 is a proposed H-side design. Its authoritative D issuance, signature and query implementation remain unverified.

## 7. Schema additions (field name, type, requiredness, `$defs` location)

### 7.1 Schema contract additions

The proposed RecoveryJoin schema additions are summarized below.

| Schema location | Field | Type | Requiredness |
|---|---|---|---|
| `$defs/forgetFenceGeneration` | Primitive definition | String, `^(0|[1-9][0-9]*)$` | Used by typed Fence fields |
| `$defs/forgetFenceCurrentnessProof` | Proof object | Object, `additionalProperties: false` | All listed fields required |
| `ownerSnapshot` | `forget_fence_namespace_ref` | `$defs/ref` | Required for D |
| `ownerSnapshot` | `forget_fence_generation_high_water` | `$defs/forgetFenceGeneration` | Required for D |
| `ownerSnapshot` | `forget_fence_currentness_proof_ref` | `$defs/ref` | Required for D |
| `ownerSnapshot` | `forget_fence_currentness_proof_digest` | `$defs/digest` | Required for D |
| `ownerSnapshotMembershipProof` | `forget_fence_namespace_ref` | `$defs/ref` | Conditionally required for D |
| `ownerSnapshotMembershipProof` | `forget_fence_generation_high_water` | `$defs/forgetFenceGeneration` | Conditionally required for D |
| `ownerSnapshotMembershipProof` | `forget_fence_currentness_proof_ref` | `$defs/ref` | Conditionally required for D |
| `ownerSnapshotMembershipProof` | `forget_fence_currentness_proof_digest` | `$defs/digest` | Conditionally required for D |
| owner evidence Forget branch | `target_set_digest` | `$defs/digest` | Conditionally required for D LINEAGE and BARRIER_MEMBERSHIP |
| owner evidence Forget branch | `forget_fence_namespace_ref` | `$defs/ref` | Conditionally required for D LINEAGE and BARRIER_MEMBERSHIP |
| D snapshot | `producer_registration_sequence_namespace_ref` | `$defs/ref` | Required for D |
| D snapshot | `producer_registration_high_water` | Existing typed decimal field | Required for D producer cutoff binding |
| Membership proof | `producer_registration_sequence_namespace_ref` | `$defs/ref` | Required for D |
| Membership proof | `producer_registration_high_water` | `$defs/counter` | Required for D |

### 7.2 Nominal-type requirements

JSON Schema primitive validation alone MUST NOT be represented as complete nominal-type validation.

The complete type binding requires:

- Correct field position.
- Correct Owner.
- Correct namespace.
- Correct operation binding where applicable.
- Correct snapshot equality.
- Correct authoritative proof.
- Correct decimal format.
- Correct currentness where applicable.

### 7.3 Version compatibility

The proposed schema and runtime changes MUST be versioned together.

The proposed shared contract version is `OWNER-SNAPSHOT-CONTRACT-1.2.18`.

The existing RecoveryJoin schema identifier remains `bmcp.recovery-join-1.0.2.schema.json` in the supplied design.

If the actual schema is upgraded to 1.0.3, the file name and test naming MUST migrate accordingly. The old version number MUST NOT conceal a schema change.

## 8. Validator unification (option C, modification list, versioned contract)

### 8.1 Measured divergence

The probes establish:

- Both validators use exact-set semantics.
- D, I and C Owner allowlists are inconsistent.
- The same snapshot cannot pass both validators.
- `validate_union()` invokes only local `validate_owner_snapshot()`.
- Validator 1.2.17 does not participate in the composed invocation path.

The two validators MUST NOT continue to be described as merely having different but compatible strictness.

This is structural incompatibility.

### 8.2 Design options

| Option | Design | Advantage | Risk |
|---|---|---|---|
| A | Inline the 1.2.17 eight-key D allowlist in composed runtime | Fewer modifications | Duplicate definitions continue to drift |
| B | Make 1.2.17 the sole snapshot validator and delegate composition to it | Single validation implementation | Schema allowlist may still drift from other modules |
| C | Extract shared allowlist constants into a shared module referenced by both implementations | Resolves both definition drift and invocation inconsistency | Requires refactoring and more comprehensive regression tests |

**Recommended option: C — Shared Owner Snapshot Contract Module.**

Reasons:

1. The measured problem includes both incorrect composition dispatch and inconsistent allowlist definitions.
2. Delegation alone cannot prevent other modules from maintaining independent field sets.
3. A shared module provides one source of truth for the composed runtime and independent validator.
4. Schema field registration must also have a single managed source to prevent another schema/Python divergence.

### 8.3 Modification list

The following are real artifact paths supplied in the evidence package. Line numbers refer to the source excerpts supplied in that package. Unprovided full-file line numbers are not inferred.

| File | Function/region | Line range | Modification |
|---|---|---|---|
| `08-bmcp-protocol/runtime_reference/owner_snapshot_contract.py` | New module | New | Define versioned `OWNER_FIELDS`, field-type classifications and schema contract version |
| `08-bmcp-protocol/runtime_reference/unified_manifest_semantics.py` | `validate_owner_snapshot()` | 41–62 | Remove independent hardcoded allowlist and reference shared constants |
| Same | `validate_owner_snapshot_membership_proof_payload()` | 67–119 | Add D typed namespace, ProducerRegistrationHighWater and Fence proof bindings |
| Same | `validate_union()` | 123–190 | Replace generic admission binding at line 157; add dual-high-water and currentness judgments |
| `08-bmcp-protocol/runtime_reference/owner_snapshot_semantics_1_2_17.py` | `OWNER_FIELDS` | 17–31 | Import from shared module while retaining independent validator responsibility |
| Same | `validate_owner_snapshot_1_2_17()` | 39–91 | Use shared allowlist; retain DECIMAL, HEX64 and digest validation |
| `08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json` | `$defs` | NOT_SUPPLIED | Add typed fields and currentness proof schema |
| `08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` | RJ102 tests | NOT_SUPPLIED | Add new-version fixtures and all dual-run tests |

### 8.4 Shared module contract

The shared module SHOULD define:

```python
CONTRACT_VERSION = "OWNER-SNAPSHOT-CONTRACT-1.2.18"

OWNER_FIELDS = {
    "I": {
        "receipt_issue_high_water",
        "receipt_consume_high_water",
        "permission_epoch",
        "producer_domain_inventory_epoch_ref",
        "registry_snapshot_digest",
        "relevant_entry_set_root",
    },
    "D": {
        "producer_registration_high_water",
        "work_item_high_water",
        "attempt_high_water",
        "barrier_generation",
        "barrier_root",
        "forget_fence_generation_high_water",
        "dependency_closure_cursor",
        "dependency_closure_root",
    },
    "C": {
        "reservation_high_water",
        "provider_attempt_high_water",
        "provider_outcome_high_water",
        "provider_idempotency_namespace_ref",
        "final_request_boundary_generation",
    },
}
```

`1.2.18` is a proposed new contract version. It is not a released version or a factual extension of existing 1.2.17.

The new version MUST undergo schema, runtime, fixture and test consistency verification before it may be declared effective.

### 8.5 Field-set separation

If composed runtime requires additional fields, it MUST NOT insert those extension fields directly into `OWNER_FIELDS`.

The following separation is recommended:

```python
OWNER_FIELDS
OWNER_SNAPSHOT_BASE_FIELDS
OWNER_SNAPSHOT_COMPOSITION_EXTENSION_FIELDS
```

Validation MUST explicitly distinguish:

- Owner-specific fields.
- Snapshot base fields.
- Composition extension fields.

All three sets MUST be managed by the same versioned contract.

Exact-set semantics MUST be retained.

The implementation MUST NOT replace exact-set validation with unconstrained subset/contains checks merely to make both validators pass.

### 8.6 Existing test impact

The following existing tests require fixture updates. Some old fixtures are expected to turn red.

| Test | Expected impact |
|---|---|
| RJ102-01 schema metadata | Update schema metadata and version assertions |
| RJ102-02 exact owner membership proof | Old proof missing D typed binding fields MUST be INVALID |
| RJ102-03 missing snapshot attestation digest | Retain existing negative case |
| RJ102-04 missing anti-rollback anchor | Retain existing negative case |
| RJ102-05 wrong purpose | Retain existing negative case |
| RJ102-06 admission join | D proof fixture MUST add dual-high-water binding |
| RJ102-07 no participant disposition | Same D proof fixture update |
| RJ102-08 owner proof inventory | Update D proof inventory |
| RJ102-09 missing verifier | Retain UNKNOWN |
| RJ102-10 valid owner verifier | Update to complete typed fixture |
| RJ102-11 entry digest mismatch | Retain INVALID |
| RJ102-12 sequence above highwater | Change to exact ProducerRegistrationHighWater cutoff test |
| RJ102-13 UNKNOWN signature result | Retain UNKNOWN |
| RJ102-14 rejected signature | Retain INVALID |

Additional requirements:

1. Old five-key D fixtures in 1.2.17 tests MUST turn red. The incorrect five-key definition MUST NOT be retained merely for fixture compatibility.
2. The I-domain old field name `inventory_epoch_ref` MUST be consistently migrated to `producer_domain_inventory_epoch_ref`.
3. Old three-key C fixtures MUST be supplemented with the extension fields already required by 1.2.17.
4. Any historical-fixture migration through an explicit legacy decoder requires a separately defined migration strategy. A legacy decoder MUST NOT participate in a new-version RecoveryJoin `VALID` judgment.

### 8.7 Version equality

The following equality MUST hold:

```text
Schema Contract Version
    == Shared Owner Snapshot Contract Version
    == Composed Runtime Contract Version
    == Independent Validator Contract Version
```

If any version differs:

- The implementation MUST NOT return `VALID`.
- An explicit version conflict MUST return `INVALID`.
- Missing authoritative version information MUST return `UNKNOWN`.

Further requirements:

1. Schema extensions MUST be registered in the shared module.
2. Any Owner field change MUST synchronously increase the contract version.
3. Modifying only the schema without modifying runtime is prohibited.
4. Modifying only the independent validator without modifying composed runtime is prohibited.
5. Tests MUST generate expected field sets from shared constants.
6. At least one independently hardcoded expected fixture MUST be retained to prevent shared implementation and tests from reproducing the same error.
7. The composed path MUST use the shared validator implementation and MUST NOT duplicate another copy of the validation logic.

## 9. Permanently forbidden combinations

The following combinations MUST produce `INVALID`, regardless of whether their numeric values are equal.

| Forbidden combination | Judgment | Corresponding D control contract §3 |
|---|---|---|
| ProducerRegistrationHighWater substituted for ForgetFenceGeneration | INVALID | They are not interchangeable |
| ForgetFenceGeneration substituted for ProducerRegistrationHighWater | INVALID | They are not interchangeable |
| ProducerRegistrationHighWater compared with CanonicalCommitCursor | INVALID | They are not interchangeable |
| ForgetFenceGeneration compared with CanonicalCommitCursor | INVALID | They are not interchangeable |
| ProducerRegistrationHighWater compared with or substituted for PermissionEpoch | INVALID | They are not interchangeable |
| ProducerRegistrationHighWater substituted for I ProducerDomainInventoryEpoch | INVALID | They are not interchangeable |
| ForgetFenceGeneration substituted for I ProducerDomainInventoryEpoch | INVALID | They are not interchangeable |
| D ProducerWork namespace mixed with ForgetFence namespace | INVALID | Type and namespace are independent |
| D ProducerWork namespace mixed with I inventory namespace | INVALID | Explicitly prohibited by §3 |
| ProducerRegistration namespaces from different Canonical Memory Authorities mixed | INVALID | Authority scopes differ |
| High-water values from different ledger sources substituted because their numbers match | INVALID | Numeric equality does not establish provenance |
| `owner_high_water` differs from the typed snapshot value | INVALID | Snapshot equality fails |
| `evidence.fence_generation` differs from currentness proof | INVALID | Fence cursor binding fails |
| Fence proofs with different `target_set_digest` values mixed | INVALID | ForgetFenceCursor target set differs |
| `lineage_manifest_digest` substituted for `target_set_digest` | INVALID | Digest semantics differ |
| UNKNOWN currentness treated as CURRENT | INVALID | UNKNOWN does not establish currentness |
| Extra fields deleted to make one of the two validators pass | INVALID | Exact-set contract is violated |

Corresponding D control contract §3:

> ProducerRegistrationHighWater is scoped to the ProducerWork Registration Ledger of that Canonical Memory Authority. CanonicalCommitCursor is an independent per-Brain Authority Commit Order/Audit Cursor. Neither is interchangeable with FenceGeneration, PermissionEpoch or I ProducerDomainInventoryEpoch.

H MUST comply with this provision and MUST NOT independently expand the comparison domain of any counter.

## 10. Conformance test vectors V01–V24

### 10.1 Test status

The following vectors are normative design requirements.

**NOT RUN — These vectors have not been executed as part of this design record.**

Suggested test file:

`08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py`

New tests SHOULD be grouped by contract version.

If the actual schema is upgraded to 1.0.3, the file name and test naming MUST migrate accordingly. An old version number MUST NOT conceal a schema change.

### 10.2 Complete test vector table

| ID | Vector name | Exact input change | Expected result | Basis | Test file |
|---|---|---|---|---|---|
| V01 | D producer cutoff below | `owner_local_sequence="4"`; ProducerRegistrationHighWater=`"5"` | VALID | D §3; 1.2.17:82–88 | recovery_join |
| V02 | D producer cutoff equal | `owner_local_sequence="5"`; ProducerRegistrationHighWater=`"5"` | VALID | D §3; 1.2.17:82–88 | recovery_join |
| V03 | D producer cutoff above | `owner_local_sequence="6"`; ProducerRegistrationHighWater=`"5"` | INVALID | D §3; 1.2.17:86–88 | recovery_join |
| V04 | Fence changes, producer fixed | ProducerRegistrationHighWater=`"5"`` unchanged; FenceGeneration changes from `"3"` to `"4"`, both with corresponding valid Fence proofs | VALID; member cutoff judgment unchanged | D §3; ForgetFenceCursor semantics | recovery_join |
| V05 | Producer changes, fence fixed | FenceGeneration=`"3"` unchanged; ProducerRegistrationHighWater changes from `"5"` to `"4"`; local sequence=`"5"` | INVALID | D §3; 1.2.17:86–88 | recovery_join |
| V06 | Fence substituted as producer cutoff | `owner_high_water="3"`; FenceGeneration=`"3"`; ProducerRegistrationHighWater=`"5"` | INVALID | D §3; 1.2.17:82–88 | recovery_join |
| V07 | Producer substituted as fence generation | `evidence.fence_generation="5"`; `proof.fence_generation="3"` | INVALID | D §3; ForgetFenceCursor semantics | recovery_join |
| V08 | Producer namespace mismatch | `proof.owner_sequence_namespace="namespace-A"`; `snapshot.producer_registration_sequence_namespace_ref="namespace-B"` | INVALID | D §3; namespace binding | recovery_join |
| V09 | Fence namespace mismatch | `evidence.forget_fence_namespace_ref="fence-A"`; `proof.forget_fence_namespace_ref="fence-B"` | INVALID | D §3; ForgetFenceCursor semantics | recovery_join |
| V10 | Producer non-decimal | `snapshot.producer_registration_high_water="NOT_A_NUMBER"` | INVALID | 1.2.17:86–88 | recovery_join |
| V11 | Fence non-decimal | `snapshot.forget_fence_generation_high_water="NOT_A_NUMBER"` | INVALID | 1.2.17 numeric validation principle | recovery_join |
| V12 | Same value, different source | `owner_high_water="5"`; `snapshot.producer_registration_high_water="5"`; namespace points to another ledger | INVALID | D §3 | recovery_join |
| V13 | Generic/specific mismatch | `proof.owner_high_water="6"`; `proof.producer_registration_high_water="5"` | INVALID | D §3; snapshot equality | recovery_join |
| V14 | Missing fence currentness | Remove `forget_fence_currentness_proof_ref` | UNKNOWN | D latest applicable Fence requirement | recovery_join |
| V15 | Stale fence | `currentness_status="STALE"` | INVALID | D §3; latest applicable Fence | recovery_join |
| V16 | Dual-validator same fixture | Invoke composed validator and independent validator separately with the same complete D fixture | Both MUST return the same result | 1.2.17:49–91; composed runtime:123–139 | recovery_join + owner_snapshot_semantics |
| V17 | D allowlist exact equality | Delete `dependency_closure_root` | INVALID | 1.2.17:63–65 | owner_snapshot_semantics |
| V18 | I allowlist alignment | Use the complete set containing `producer_domain_inventory_epoch_ref` and `permission_epoch` | Both validators MUST return the same result | 1.2.17:17–21 | recovery_join |
| V19 | C allowlist alignment | Add `provider_idempotency_namespace_ref` and `final_request_boundary_generation` | Both validators MUST return the same result | 1.2.17:27–30 | recovery_join |
| V20 | Fence generation beyond highwater | `forget_fence_generation="6"`; high-water=`"5"` | INVALID | ForgetFence namespace monotonicity | recovery_join |
| V21 | Target digest mismatch | `evidence.target_set_digest` differs from `currentness_proof.target_set_digest` | INVALID | D ForgetFenceCursor tuple | recovery_join |
| V22 | UNKNOWN signature | Fence currentness proof signature verifier returns UNKNOWN | UNKNOWN | Existing RJ102-13 semantics | recovery_join |
| V23 | Missing producer namespace | Delete `snapshot.producer_registration_sequence_namespace_ref` | UNKNOWN | Namespace authority unavailable | recovery_join |
| V24 | Missing producer high-water | Delete `producer_registration_high_water` from D snapshot | UNKNOWN | 1.2.17:60–65 | recovery_join |

### 10.3 V16 dual-validator requirements

V16 MUST NOT merely compare whether both validators return the same Boolean.

It MUST use the same fixture, same version and same verifier inputs, and compare:

```python
result_composed == result_independent
```

For a VALID fixture, both MUST return `VALID`.

For an INVALID fixture, both MUST return `INVALID`.

For a fixture missing authoritative proof, both MUST return `UNKNOWN`.

Surface consistency MUST NOT be manufactured through:

- Different fixtures.
- Different allowlists.
- Different schema versions.
- Different input snapshots.
- Different signature-verification results.

### 10.4 Cross-version negative test

An additional cross-version negative test MUST be added.

An old 1.2.17 snapshot MUST NOT be treated directly as new-version `VALID` when new-version required fields are missing.

## 11. Evidence status: probes, NOT RUN declaration, Storage NOT_SUPPLIED, minimum substitutes

### 11.1 Mechanical probe status

The highest available evidence in this record is:

**17 mechanical probes: ALL PASS.**

| Probe group | Result |
|---|---|
| A1–A7 | PASS |
| B1–B3 | PASS |
| C1–C4 | PASS |
| D1–D2 | PASS |
| E1–E2 | PASS |

These probes establish the identified defects in the examined source.

They do not prove that repairs have occurred.

### 11.2 Historical CI exclusion

Historical CI evidence:

| Attribute | Value |
|---|---|
| Run | `44215993536` |
| Job | `134505846435` |
| HEAD | `654d4449fd491cdda37d9761fe63a3efca55dc9d` |
| Discovered | 390 |
| Skipped | 22 |
| Executed | 368 |

This CI was executed against a different HEAD from the repaired target.

It proves only that the tests covered by that historical execution passed at that time.

**Historical Run `44215993536` / Job `134505846435` MUST NOT be used to close H-RJ-HW-01.**

### 11.3 Minimum alternative implementation evidence

While the runtime repository has not yet been merged into main, the minimum alternative evidence deliverable is:

1. Exact repaired branch HEAD SHA.
2. Blob SHA for every modified file.
3. Actual new schema contents and version number.
4. Complete source of the shared allowlist module.
5. Complete source of the modified composed runtime.
6. Complete source of the modified independent validator.
7. Complete source of added test functions.
8. Positive and negative fixtures.
9. Local test commands and raw stdout/stderr.
10. Test discovery count, executed count and skipped count.
11. Actual assertion results for every new test.
12. Raw results of dual-validator execution using the same fixture.

These materials may serve only as alternative technical evidence during implementation.

They MUST NOT substitute for exact-head CI.

### 11.4 Condition 5 — Exact-head CI requirements

Condition 5 can be closed only when the following are supplied:

| Item | Requirement |
|---|---|
| Exact Head | Complete repaired commit SHA |
| Workflow | Actual workflow file path and Blob SHA |
| Run | GitHub Actions Run ID |
| Job | Corresponding Job ID |
| Test report | Total, executed, skipped and failed test counts |
| Raw log | Verifiable original log |
| New tests | Actual execution records for V01–V24 |
| Existing tests | RJ102 and 1.2.17 regression results |
| Double validator | Raw same-fixture dual-run results |
| Schema | Schema version and SHA at exact HEAD |

Branch names, PR titles, commit messages and historical Runs MUST NOT substitute for exact HEAD evidence.

**Current condition 5: BLOCKED.**

### 11.5 Mandatory NOT RUN declaration

```text
NOT RUN — GitHub Actions CI was not run on the repaired exact HEAD in this session.
Historical Run 44215993536 / Job 134505846435 belongs to HEAD 654d4449fd491cdda37d9761fe63a3efca55dc9d and does not constitute repair-validation evidence for this Finding.
The 17 mechanical probes in this session establish only the defect state of the examined source. They do not prove repair, integration or CI success.
NOT RUN MUST NOT be converted into PASS.
```

### 11.6 Prohibited claims

While the runtime repository has not been merged into main, this record MUST NOT claim:

- Main contains the repair.
- RecoveryJoin composed validation has been unified.
- ProducerRegistrationHighWater has valid composed-path binding.
- ForgetFenceGeneration has an implemented currentness proof.
- Both validators have passed the new tests.
- Same-version Storage mapping has been completed.
- Production conforms to the protocol.
- D/E/I/Storage Owners have approved the changes.
- Human R3 review has completed.
- Production activation has completed.
- Platform-independent gates have passed.

Human R3 review, production activation and platform-independent gates are `OUT-OF-SCOPE` for this technical closure record.

### 11.7 Storage evidence status

<badge color="danger">BLOCKED / NOT_SUPPLIED</badge>

The same-version Storage JoinProof source was not provided in this evidence package.

Therefore, this contract MUST NOT infer Storage fields or use historical Issue #29 comments as verification evidence.

The following version identifiers MUST be verified together:

| Artifact | Required identifier | Current status |
|---|---|---|
| Storage manifest | Exact version, commit SHA and Blob SHA | NOT_SUPPLIED |
| Storage JoinProof schema | Exact version and Blob SHA | NOT_SUPPLIED |
| Storage JoinProof implementation | Exact path and Blob SHA | NOT_SUPPLIED |
| D control contract source | `03-memory-brain/forget-fence-operation-and-publication-gate-part4.md`, Blob SHA `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | SUPPLIED |
| H RecoveryJoin schema | `bmcp.recovery-join-1.0.2.schema.json`, Blob SHA `4b664e3bce465499bcdfd93796349a4ba7074002` | SUPPLIED |
| H composed runtime | `unified_manifest_semantics.py`, Blob SHA `e26379d38825ee13d15f652d3bd019c4091da37d` | SUPPLIED |
| H independent validator | `owner_snapshot_semantics_1_2_17.py`, Blob SHA `17275eebd0013f8ad8765670a7faaa40866d99d8` | SUPPLIED |

Same-version does not mean that different artifacts must use the same numeric version.

It means:

1. The schema version declared by the Storage manifest matches the actual JoinProof schema.
2. Actual Storage JoinProof fields match the manifest fields they reference.
3. The D contract version referenced by Storage-to-H mapping is explicit.
4. D field semantics match H schema field semantics.
5. H schema version matches the contract version used by composed runtime.
6. Every mapping has an exact version, field path and direct evidence.
7. Historical-comment field names MUST NOT substitute for direct reading of current artifacts.

### 11.8 Storage field-level verification table

The following fields MUST be checked. Unknown Storage fields MUST NOT be inferred.

| Storage field | D field | Type | Same-version mapping | Evidence location |
|---|---|---|---|---|
| NOT_SUPPLIED | `producer_registration_high_water` | ProducerRegistrationHighWater | NOT_SUPPLIED | D §3 supplied; Storage not supplied |
| NOT_SUPPLIED | `producer_registration_sequence_namespace_ref` | D ProducerWork Ledger namespace ref | NOT_SUPPLIED | New design field; actual D carrier NOT_SUPPLIED |
| NOT_SUPPLIED | `forget_fence_generation_high_water` | ForgetFenceGeneration | NOT_SUPPLIED | 1.2.17 lines 23–25; Storage not supplied |
| NOT_SUPPLIED | `forget_fence_namespace_ref` | ForgetFence namespace ref | NOT_SUPPLIED | New design field |
| NOT_SUPPLIED | `forget_operation_ref` | ForgetOperation reference | NOT_SUPPLIED | D control contract and evidence schema |
| NOT_SUPPLIED | `target_set_digest` | Digest | NOT_SUPPLIED | D ForgetFenceCursor semantics |
| NOT_SUPPLIED | `lineage_manifest_digest` | Digest | NOT_SUPPLIED | D evidence schema |
| NOT_SUPPLIED | `fence_generation` | ForgetFenceGeneration | NOT_SUPPLIED | H owner evidence schema |
| NOT_SUPPLIED | `owner_snapshot_ref` | Snapshot reference | NOT_SUPPLIED | H membership proof schema |
| NOT_SUPPLIED | `owner_snapshot_digest` | Digest | NOT_SUPPLIED | H membership proof schema |
| NOT_SUPPLIED | `anti_rollback_anchor_ref` | Reference | NOT_SUPPLIED | H membership proof schema |
| NOT_SUPPLIED | `barrier_generation` | D barrier generation | NOT_SUPPLIED | 1.2.17 lines 23–25 |

### 11.9 Storage Owner deliverables

Storage Owner MUST supply:

1. Original Storage manifest and exact path.
2. Exact Storage manifest version and Blob SHA.
3. Original Storage JoinProof schema.
4. Exact Storage JoinProof schema version and Blob SHA.
5. Storage JoinProof producer/admission-related field definitions.
6. Direct mapping definition between Storage JoinProof and D ProducerRegistrationHighWater.
7. Direct mapping definition between Storage JoinProof and ForgetFenceGeneration.
8. Binding definition for ForgetOperation and target-set digest.
9. Storage currentness/anti-rollback proof fields.
10. Same-version implementation or conformance fixture.
11. Type, source and authoritative issuer for each field.
12. Reproducible field-level mapping verification results.

Only after these artifacts are supplied may `NOT_SUPPLIED` be changed into an actual verification result.

**Matching field names, similar types and historical Issue comments MUST NOT be treated as evidence of same-version mapping.**

## 12. Closure conditions mapping, review checkpoints, non-claims

### 12.1 Documentation and implementation carriers

The registered design identifies two suggested carriers:

**Issue #25 comment**

Register the complete design disposition, including:

- Closure conditions 1–6.
- F1–F3 measured conclusions.
- Recommended option C.
- NOT RUN declaration.
- Storage NOT_SUPPLIED status.
- Repair responsibilities and exit conditions.

Issue #25 remains the main tracking carrier for precise-version verification relating to the Phase 3.7/3.8 visibility protocol and RecoveryJoin.

**Independent PR document**

The proposed repository path is:

```text
08-bmcp-protocol/
  phase-3.8-h-rj-hw-01-typed-watermark-and-fence-binding-contract.md
```

This document is the proposed formal versioned carrier for the H-side semantic repair design.

Its scope includes:

1. ProducerRegistrationHighWater semantic contract.
2. ForgetFenceGeneration semantic contract.
3. Namespace binding.
4. Currentness proof.
5. Shared Validator contract.
6. Test vectors.
7. Storage mapping checklist.
8. Version compatibility and migration requirements.

A PR submitting this design or later implementation MUST NOT itself be treated as approval or merge evidence.

The repository bilingual documentation convention is satisfied by this single file. No separate `docs/en/` or `docs/zh-CN/` paired file is required by this document.

The actual bilingual gate remains subject to the final effective rules of GOV-DOC-001 v1.2 under PR #271. This document does not independently modify that governance process.

### 12.2 Suggested child Findings

Three child Findings are recommended without replacing `H-RJ-HW-01`.

| Suggested ID | Title | Severity | Relationship |
|---|---|---|---|
| H-RJ-HW-01A | D ProducerRegistrationHighWater Binding Failure | P1 | Child of H-RJ-HW-01 |
| H-RJ-HW-01B | ForgetFenceGeneration Snapshot and Currentness Binding Failure | P1 | Child of H-RJ-HW-01 |
| H-RJ-HW-01C | Owner Snapshot Validator Contract Divergence | P1 | Child of H-RJ-HW-01 |

F1 and F2 may be grouped under two independent technical assertions within 01C:

- 01C-1: allowlist exact-set divergence.
- 01C-2: composed validator dispatch divergence.

The three problems have different repair paths and verification vectors.

Creating new Finding IDs remains a repository Owner governance decision. This contract only recommends the split. It does not create Issues or change the existing Finding state.

### 12.3 Review disposition

**Recommended disposition: HOLD.**

Reasons:

- 17 probes establish definite defects in the original implementation.
- Conditions 1 and 2 still lack D-authoritative field definitions and proof implementation.
- Conditions 3 and 4 have no repair implementation evidence.
- Condition 5 has no exact-head CI evidence.
- Condition 6 is explicitly NOT_SUPPLIED.

The completion of this design MUST NOT cause Issue #25 to become closable.

### 12.4 Review checkpoints

| Checkpoint | Required deliverables | Exit criterion |
|---|---|---|
| R1 — D dual high-water | D namespace, snapshot and proof originals | Type and equality bindings are verifiable |
| R2 — Fence currentness | Original D Fence Currentness Proof | Operation, target, generation and currentness are verifiable |
| R3 — Validator unification | Shared module and both invocation paths | Same contract version and same allowlist |
| R4 — Behavioral tests | Actual V01–V24 tests and raw output | All positive and negative cases meet expected results |
| R5 — CI | Exact HEAD, Run, Job, workflow and raw log | Tests pass on the exact HEAD |
| R6 — Storage | Same-version manifest, schema and JoinProof | Field-level mapping verified individually |

After R1–R4 are complete, the technical implementation status may be submitted for reassessment.

After R5 is complete, the CI condition may be evaluated.

After R6 is complete, the Storage same-version mapping condition may be evaluated.

Even completion of all technical conditions MUST NOT automatically establish human R3 review, production activation or platform-independent gate completion.

### 12.5 Confirmed findings

The following are confirmed findings in the examined source:

1. The composed runtime D allowlist is incomplete.
2. The composed runtime and independent 1.2.17 validator have structurally incompatible D/I/C allowlists.
3. Composed `validate_union()` does not invoke the independent 1.2.17 validator.
4. The composed path incorrectly binds `owner_high_water` to generic `admission_high_water`.
5. The composed path does not correctly bind typed ProducerRegistrationHighWater.
6. The composed path lacks corresponding DECIMAL type validation.
7. RecoveryJoin 1.0.2 schema does not provide a snapshot carrier for ForgetFenceGeneration high-water.
8. `fence_generation` currently appears only in the evidence Forget branch.
9. Existing RJ102-01..14 tests do not establish the six closure conditions of this Finding.
10. All 17 mechanical probes passed, but no repaired exact-head CI evidence exists.

### 12.6 Explicit non-claims

The following are NOT established:

1. D Owner has approved this design.
2. D has supplied a new namespace canonicalization specification.
3. D has supplied an authoritative Fence Currentness Proof implementation.
4. H has completed schema and runtime modifications.
5. The two Validators have been unified.
6. New tests have been executed successfully.
7. Exact-head CI has passed.
8. Storage same-version mapping has been established.
9. D/E/I/Storage have achieved production conformance.
10. Human R3 review has completed.
11. Production activation has completed.
12. Platform-independent gates have completed.

### 12.7 Final status table

| Item | Current conclusion |
|---|---|
| H-RJ-HW-01 | OPEN |
| Severity | P1 |
| Validation | TO_VALIDATE |
| F1 | CONFIRMED |
| F2 | CONFIRMED |
| F3 | CONFIRMED |
| Condition 1 | ADVANCEABLE |
| Condition 2 | ADVANCEABLE |
| Condition 3 | ADVANCEABLE |
| Condition 4 | ADVANCEABLE |
| Condition 5 | BLOCKED |
| Condition 6 | BLOCKED / NOT_SUPPLIED |
| Recommended repair | Shared Owner Snapshot Contract Module |
| Issue management recommendation | HOLD |
| Production conformance | NOT ASSESSED |
| Human R3 review | OUT-OF-SCOPE |
| Production activation | OUT-OF-SCOPE |
| Platform-independent gate | OUT-OF-SCOPE |

### 12.8 Final disposition

**HOLD — REMEDIATION DESIGN PROVIDED / IMPLEMENTATION NOT VERIFIED.**

This document records the H-side semantic contract repair design. It is not acceptance of repair implementation.

`H-RJ-HW-01` MUST NOT be closed because this document has been published.

`ADVANCEABLE` MUST NOT be converted into `CLOSED`.

`NOT RUN` MUST NOT be converted into `PASS`.

`NOT_SUPPLIED` MUST NOT be represented as verified.

The recommended next execution responsibilities are:

- **H Owner:** Implement the shared contract, dual-high-water binding and currentness-proof integration according to the design.
- **D Owner:** Supply authoritative namespace and Fence Currentness Proof specifications.
- **Storage Owner:** Supply same-version JoinProof artifacts.

After all three parties' required materials are available, complete verification MUST be rerun against the exact repaired HEAD.

---

# Phase 3.8 H-RJ-HW-01 — 类型化高水位与 Fence 绑定契约

- **Document ID：** `PHASE-3.8-H-RJ-HW-01-TYPED-WATERMARK-AND-FENCE-BINDING-CONTRACT`
- **状态：** `CANDIDATE DESIGN RECORD; IMPLEMENTATION NOT VERIFIED; EXACT-HEAD CI NOT RUN`
- **范围：** H-RJ-HW-01、ProducerRegistrationHighWater、ForgetFenceGeneration、Owner Snapshot Validator Contract、RecoveryJoin schema 与 runtime 一致性。
- **上游权威依据：** Issue #25，已登记的修复设计评论 `7006145800`，源自派发 `REMEDIATE-HRJHW01-001`（会话 `6afecafc`）。
- **基准钉定：**
  - main 基准 HEAD：`4c38ae25b71383d661e4179622cafa04b66a046a`
  - H 实现分支：`session-h-bmcp-protocol`（尚未合入 main）。
  - Schema Blob：`4b664e3bce465499bcdfd93796349a4ba7074002`
  - RJ102 测试 Blob：`3c61cc8c9d973a27f890e1452305e3fb0ad09f1a`
  - 组合 runtime Blob：`e26379d38825ee13d15f652d3bd019c4091da37d`
  - Validator 1.2.17 Blob：`17275eebd0013f8ad8765670a7faaa40866d99d8`
  - D 控制契约 Blob：`4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- **非声明事项：** 本文档不声称 Owner 已批准、实现已完成、schema 已部署、Validator 已合一、测试已执行、精确 Head CI 已通过、Storage 已符合要求、生产已符合协议、真人 R3 已批准、生产激活已完成或平台独立门禁已完成。

## 1. 文档标识与状态

### 1.1 规范身份

本文档定义 Finding `H-RJ-HW-01` 的候选类型化高水位与 Fence 绑定契约。

该 Finding 当前保持：

| 属性 | 值 |
|---|---|
| Finding | `H-RJ-HW-01` |
| 严重性 | `P1` |
| 状态 | `OPEN` |
| 验证状态 | `TO_VALIDATE` |
| 处置 | `HOLD` |
| 实现状态 | `NOT VERIFIED` |
| 精确 Head CI | `NOT RUN` |

本文档是版本化的单文件双语契约记录。英文和中文章节表达相同的要求。

推荐的共享契约版本为：

`OWNER-SNAPSHOT-CONTRACT-1.2.18`

这是建议版本号，不是已发布或已采纳的版本。

### 1.2 规范性解释

以下结果具有不同含义：

- `VALID`：全部必需的权威性、类型、命名空间、等式、签名和当前性检查均已成功。
- `INVALID`：已经确定存在明确矛盾、格式错误、无效签名、禁止替代或规范绑定失败。
- `UNKNOWN`：必需的权威证据不可用、不完整或无法验证。

`UNKNOWN` MUST NOT 被视为 `VALID`。

`NOT RUN` MUST NOT 被视为 `PASS`。

`NOT_SUPPLIED` MUST NOT 被视为已核验。

`ADVANCEABLE` MUST NOT 被表述为 `CLOSED`。

### 1.3 关闭条件

| 条件 | 当前状态 | 本契约覆盖范围 | 剩余缺口 | 阻塞责任 |
|---|---|---|---|---|
| 1. ProducerRegistrationHighWater 精确类型、命名空间和 snapshot equality | ADVANCEABLE | 类型化绑定、字段、唯一等式、序号比较及判定规则 | `producer_registration_sequence_namespace_ref` 的 D 权威命名及其实际 snapshot/proof 实现尚未提供 | D Owner + H Owner |
| 2. ForgetFenceGeneration 独立类型、ForgetOperation/target-set 绑定及当前性证明 | ADVANCEABLE | Schema 新增字段、currentness proof、判定顺序及 INVALID/UNKNOWN 规则 | D Fence Currentness Proof 权威格式、签名和查询接口尚未提供 | D Owner + H Owner |
| 3. Validator allowlist 差异及唯一组合路径 | ADVANCEABLE | 共享 allowlist 方案、文件、函数、修改区间和版本化规则 | 实际修改、导入、回归测试及组合路径实现尚未发生 | H Owner |
| 4. 四类新增测试及双 Validator 组合测试 | ADVANCEABLE | 可执行测试向量 V01–V24 及归属建议 | 测试代码、fixture、断言及执行结果尚未提供 | H Owner |
| 5. 精确 Head CI Run、Job 和测试报告 | BLOCKED | 最低证据要求及替代性本地证据清单 | 没有修复后的精确 HEAD、workflow、Run、Job 和 raw log | H Owner / CI 责任角色 |
| 6. Storage 同版本字段映射核验 | BLOCKED / NOT_SUPPLIED | 同版本判定标准和字段级核验表 | Storage JoinProof 同版本 schema、manifest、字段映射及直接核验材料尚未提供 | Storage Owner + H Owner |

状态解释：

- `ADVANCEABLE`：技术设计可以进入实现阶段，不代表条件已经满足。
- `BLOCKED`：缺少本轮不可推定的必要证据，不得以设计文本替代。
- `CLOSED`：本记录中没有任何关闭条件达到 `CLOSED`。

条件 5 不得因历史 CI 通过而变为 CLOSED。

条件 6 不得因历史 Issue #29 评论或其他版本中字段名称相似而变为 CLOSED。

## 2. 问题陈述（F1/F2/F3 及实测证据）

### 2.1 Finding 与实测结论

Finding `H-RJ-HW-01` 涉及 D/E/I/Storage 原子化 producer admission 和 derivative visibility gate。

三个具有独立证据支持的缺陷如下：

| 缺陷 | 实测结论 | 必需技术处置 |
|---|---|---|
| F1 — Validator allowlist 分叉 | 三个 Owner 域字段集合具有相互不兼容的 exact-set 语义，无法同时通过 | 建立共享版本化 allowlist |
| F2 — 组合校验路径错误 | `validate_union()` 仅调用本地 validator，1.2.17 validator 未参与组合校验 | 统一为共享实现及唯一组合入口 |
| F3 — D 双高水位未绑定 | 泛型高水位绑定到 `admission_high_water`，而非 D Producer Registration 高水位；Fence Generation 缺少 snapshot 载体 | 增加类型、命名空间、snapshot equality 和 currentness 绑定 |

F1、F2、F3 均由所提供证据包中的独立源码和行为探针支持，不是仅从原 Finding 描述循环推导。

### 2.2 实测探针证据

17 项机械探针全部通过：

| 探针组 | 探针 | 实测范围 |
|---|---|---|
| A | A1–A7 | Allowlist divergence |
| B | B1–B3 | 组合 Validator 调用路径 |
| C | C1–C4 | ProducerRegistrationHighWater 绑定 |
| D | D1–D2 | 类型校验差异 |
| E | E1–E2 | 行为级正例和负例 |

重要实测结果：

**E1 证明组合路径接受非十进制的 `producer_registration_high_water` 值，并返回 `VALID`。**

这些探针证明被检查源码存在所列缺陷，不证明修复已经实现。

### 2.3 核心设计原则

1. `ProducerRegistrationHighWater` 与 `ForgetFenceGeneration` MUST 是两个不同的名义类型。
2. 两者 MUST 具有不同的账本、命名空间、语义和比较域。
3. 相同的十进制字符串 MUST NOT 证明类型相同或来源相同。
4. 只有获得对应 Owner 权威证明支持的类型化值，MAY 参与 cutoff 判定。
5. `UNKNOWN` MUST NOT 转换为 `VALID`。
6. H 的 schema 扩展 MUST NOT 削弱 D 控制契约 §3 的不可互换要求。

## 3. 规范类型：ProducerRegistrationHighWater

### 3.1 定义

`ProducerRegistrationHighWater` 定义为：

> 一个由 D Owner 专属签发的十进制计数器，表示针对一个 Canonical Memory Authority 和一个 ForgetOperation 上下文的 ProducerWork Registration Ledger 冻结 admission cutoff。

其规范属性如下：

| 属性 | 必需含义 |
|---|---|
| Owner | D |
| Ledger | ProducerWork Registration Ledger |
| 语义 | ProducerWork 注册顺序 |
| 用途 | 特定 ForgetOperation 的 ProducerWork cutoff |
| 范围 | 对应 Canonical Memory Authority |
| 类型 | D 专属单调十进制计数器 |

不得将其解释为以下任何类型或位置：

- 泛型 Admission HighWater。
- CanonicalCommitCursor。
- ForgetFenceGeneration。
- PermissionEpoch。
- I ProducerDomainInventoryEpoch。
- Storage Commit Position。

### 3.2 命名空间字段

Snapshot MUST 新增：

`producer_registration_sequence_namespace_ref`

类型：

`$defs/ref`

该字段表示由 D Owner 权威登记的 ProducerWork Registration Ledger 序列命名空间。

规范要求：

1. 每个 Canonical Memory Authority MUST 具有唯一且稳定的 D ProducerWork Registration Ledger namespace reference。
2. namespace reference MUST 由 D Owner 提供。H MUST NOT 根据其他 counter 推导。
3. namespace reference MUST 与 ledger identity、authority identity 绑定。
4. I inventory namespace、Storage namespace、ForgetFence namespace 和通用 admission namespace MUST NOT 替代该字段。
5. namespace reference MUST 在 snapshot、membership proof 和 admission row 之间保持相等。

### 3.3 与 `owner_sequence_namespace` 的关系

唯一合法绑定为：

```python
proof["owner_sequence_namespace"] \
    == row["owner_sequence_namespace"] \
    == snapshot["producer_registration_sequence_namespace_ref"]
```

同时：

```python
proof["owner_kind"] == "D"
row["owner_kind"] == "D"
snapshot["owner"] == "D"
```

任何不等均 MUST 判定为 `INVALID`。

本证据包中的 D 权威 namespace URI/标识符实际编码语法为 `NOT_SUPPLIED`。

因此，本契约规定唯一引用字段及其相等关系，但不伪造已经存在的 D namespace 字符串。

D Owner MUST 在实现前提供正式 namespace 标识符格式、authority 绑定和 canonicalization 规则。

### 3.4 Snapshot 和 membership proof 字段

D snapshot MUST 保留：

```json
{
  "producer_registration_high_water": "123"
}
```

Snapshot MUST 新增：

```json
{
  "producer_registration_sequence_namespace_ref": "d-producer-registration-ledger-namespace-ref"
}
```

Membership proof MUST 新增：

```json
{
  "producer_registration_sequence_namespace_ref": "d-producer-registration-ledger-namespace-ref",
  "producer_registration_high_water": "123"
}
```

这些字符串仅为结构示例，不代表已经存在的真实 D namespace reference。

### 3.5 唯一等式

对于 D admission row：

```python
proof["owner_high_water"] \
    == proof["producer_registration_high_water"] \
    == snapshot["owner_specific_high_waters"][
        "producer_registration_high_water"
    ]
```

并且：

```python
row["owner_high_water"] == proof["owner_high_water"]
```

完整绑定为：

```python
row["owner_high_water"] \
    == proof["owner_high_water"] \
    == proof["producer_registration_high_water"] \
    == snapshot["owner_specific_high_waters"][
        "producer_registration_high_water"
    ]
```

这是泛型 D counter 转换为类型化 counter 的唯一允许入口。

以下内容 MUST NOT 替代该等式：

```python
proof["owner_high_water"] == snapshot["admission_high_water"]
```

以下内容同样 MUST NOT 替代：

```python
proof["owner_high_water"] == snapshot["work_item_high_water"]
```

两个字段的数值字符串相同，MUST NOT 被认定为属于同一账本。

### 3.6 ProducerRegistrationHighWater 判定表

| 情况 | 结果 | 原因 |
|---|---|---|
| Snapshot 明确存在，但 `producer_registration_high_water` 与 proof 不相等 | INVALID | 权威值发生冲突 |
| `owner_high_water` 与类型化值不相等 | INVALID | 唯一绑定等式被违反 |
| Namespace reference 不相等 | INVALID | 明确跨账本或跨域绑定 |
| Owner 不是 D | INVALID | 类型域错误 |
| Counter 为非十进制字符串 | INVALID | 类型不符合 DECIMAL |
| Counter 为负数或非规范十进制形式 | INVALID | Counter 格式违反要求 |
| Snapshot 缺失 | UNKNOWN | 权威资料不可用 |
| Snapshot currentness 无法证明 | UNKNOWN | 无法确认当前权威状态 |
| Proof 缺失 | UNKNOWN | 缺少 membership 证明 |
| Verifier 返回 UNKNOWN | UNKNOWN | 验证结果未确定 |
| Verifier 明确拒绝签名 | INVALID | 权威证明无效 |

**字段存在且发生明确冲突时 MUST 判定为 INVALID。MUST NOT 通过返回 UNKNOWN 隐藏确定性矛盾。**

### 3.7 序号 cutoff

现有 membership proof 比较：

```python
owner_local_sequence <= owner_high_water
```

MUST 保留其行为，但其 D 域语义 MUST 收敛为：

```python
owner_local_sequence \
    <= producer_registration_high_water
```

在 D 域内：

```python
owner_local_sequence <= snapshot[
    "owner_specific_high_waters"
]["producer_registration_high_water"]
```

MUST NOT 存在第二套独立 cutoff 真相。

`owner_high_water` 仅是通用 proof envelope 字段。其 D 域含义由上述唯一等式建立。

MUST NOT 同时维护泛型 cutoff 和独立 D cutoff，并允许两者分别通过。

## 4. 命名空间绑定与唯一等式

### 4.1 必需的命名空间身份

`producer_registration_sequence_namespace_ref` 用于标识 D ProducerWork Registration Ledger namespace。

以下身份 MUST 保持独立：

- D ProducerWork Registration Ledger namespace。
- ForgetFence namespace。
- I ProducerDomainInventory namespace。
- Storage namespace。
- Generic admission namespace。

Namespace reference MUST 作为身份绑定进行验证，而不仅仅作为非空字符串进行验证。

### 4.2 Snapshot、proof 和 row 绑定

必需的三方 namespace 等式为：

```python
proof["owner_sequence_namespace"] \
    == row["owner_sequence_namespace"] \
    == snapshot["producer_registration_sequence_namespace_ref"]
```

必需的 Owner 身份为：

```python
proof["owner_kind"] == "D"
row["owner_kind"] == "D"
snapshot["owner"] == "D"
```

必需的 high-water 等式为：

```python
row["owner_high_water"] \
    == proof["owner_high_water"] \
    == proof["producer_registration_high_water"] \
    == snapshot["owner_specific_high_waters"][
        "producer_registration_high_water"
    ]
```

所有等式均为强制要求。

### 4.3 判定顺序

D producer-admission 的规范判定顺序为：

1. 校验 owner 为 D。
2. 校验 snapshot 完整性和 currentness。
3. 校验 namespace identity。
4. 校验类型化 counter 格式。
5. 校验泛型 counter 格式。
6. 校验唯一 equality。
7. 校验 `owner_local_sequence <= producer_registration_high_water`。
8. 校验 membership proof 签名。
9. 校验 admission row、proof 和 snapshot 的其他绑定。

任何明确冲突 MUST 在签名成功结果能够建立有效性之前判定为 `INVALID`。

### 4.4 缺失的权威 namespace 材料

D namespace 标识符实际格式和 canonicalization 为 `NOT_SUPPLIED`。

建议的示例 namespace 字符串 MUST NOT 被表述为权威标识符。

在 D Owner 提供所需 namespace 权威材料之前，对应的权威依赖验证仍不可用。

## 5. 规范类型：ForgetFenceGeneration

### 5.1 定义

独立名义类型为：

`ForgetFenceGeneration`

其规范定义为：

> 一个由 D Owner 签发的单调 generation counter，属于 ForgetFence namespace，受权威 ForgetFence 顺序约束，并绑定到一个 ForgetOperation 和一个不可变的 target-set digest。

`ForgetFenceGeneration` 不是 `ProducerRegistrationHighWater`。

即使两者数值相等，也 MUST NOT 相互替代。

D 控制契约 §3 已定义：

```text
ForgetFenceCursor =
(forget_operation_id, fence_generation, target_set_digest)
```

因此，FenceGeneration MUST 与 ForgetOperation 和目标集合一起验证。

### 5.2 现有 Schema 缺陷

RecoveryJoin 1.0.2 schema 存在以下缺陷：

- `ownerSnapshot` 没有 ForgetFenceGeneration high-water。
- Membership proof 没有对应的类型化字段。
- `fence_generation` 仅存在于 owner evidence 的 Forget 分支。
- 1.2.17 validator 的 `forget_fence_generation_high_water` 在 schema 中没有对应 snapshot 载体。

### 5.3 Schema 新增 A — `forgetFenceGeneration`

Schema `$defs` MUST 新增：

```json
{
  "forgetFenceGeneration": {
    "type": "string",
    "pattern": "^(0|[1-9][0-9]*)$"
  }
}
```

该 primitive schema 仅验证数值格式。

名义类型由字段位置、owner、namespace 和 operation binding 共同建立。

MUST NOT 声称仅凭 JSON Schema 已实现完整强类型。

### 5.4 Schema 新增 B — `forgetFenceCurrentnessProof`

Schema `$defs` MUST 新增：

```json
{
  "forgetFenceCurrentnessProof": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "proof_ref": {
        "$ref": "#/$defs/ref"
      },
      "proof_digest": {
        "$ref": "#/$defs/digest"
      },
      "owner_kind": {
        "const": "D"
      },
      "forget_operation_ref": {
        "$ref": "#/$defs/ref"
      },
      "target_set_digest": {
        "$ref": "#/$defs/digest"
      },
      "forget_fence_namespace_ref": {
        "$ref": "#/$defs/ref"
      },
      "forget_fence_generation": {
        "$ref": "#/$defs/forgetFenceGeneration"
      },
      "forget_fence_generation_high_water": {
        "$ref": "#/$defs/forgetFenceGeneration"
      },
      "producer_registration_high_water": {
        "$ref": "#/$defs/counter"
      },
      "owner_snapshot_ref": {
        "$ref": "#/$defs/ref"
      },
      "owner_snapshot_digest": {
        "$ref": "#/$defs/digest"
      },
      "owner_gate_generation": {
        "$ref": "#/$defs/counter"
      },
      "anti_rollback_anchor_ref": {
        "$ref": "#/$defs/ref"
      },
      "currentness_status": {
        "enum": [
          "CURRENT",
          "STALE",
          "UNKNOWN"
        ]
      },
      "signature_ref": {
        "$ref": "#/$defs/ref"
      }
    },
    "required": [
      "proof_ref",
      "proof_digest",
      "owner_kind",
      "forget_operation_ref",
      "target_set_digest",
      "forget_fence_namespace_ref",
      "forget_fence_generation",
      "forget_fence_generation_high_water",
      "producer_registration_high_water",
      "owner_snapshot_ref",
      "owner_snapshot_digest",
      "owner_gate_generation",
      "anti_rollback_anchor_ref",
      "currentness_status",
      "signature_ref"
    ]
  }
}
```

该结构是 H 侧设计提案，MUST NOT 被表述为 D 已经签发的证明。

D Owner MUST 确认其真实性、字段来源、签名和查询语义。

### 5.5 Schema 新增 C — `ownerSnapshot`

MUST 新增以下字段：

```json
{
  "forget_fence_namespace_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_generation_high_water": {
    "$ref": "#/$defs/forgetFenceGeneration"
  },
  "forget_fence_currentness_proof_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_currentness_proof_digest": {
    "$ref": "#/$defs/digest"
  }
}
```

这些字段对 D owner snapshot MUST 为必填。

MUST NOT 强制 I/C snapshot 提供这些 D 专属字段。

D Owner snapshot 还 MUST 保留：

```json
{
  "producer_registration_high_water": "123"
}
```

两个 high-water 值 MUST 在同一份 D snapshot 中并列存在。MUST NOT 合并为一个字段。

### 5.6 Schema 新增 D — `ownerSnapshotMembershipProof`

MUST 新增以下字段：

```json
{
  "forget_fence_namespace_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_generation_high_water": {
    "$ref": "#/$defs/forgetFenceGeneration"
  },
  "forget_fence_currentness_proof_ref": {
    "$ref": "#/$defs/ref"
  },
  "forget_fence_currentness_proof_digest": {
    "$ref": "#/$defs/digest"
  }
}
```

当 `owner_kind == "D"` 时，这些字段 MUST 条件必填。

其他 Owner MUST NOT 使用这些字段建立 D Fence 证明。

### 5.7 Schema 新增 E — owner evidence Forget 分支

现有字段 MUST 保留：

```json
{
  "forget_operation_ref": "...",
  "fence_generation": "..."
}
```

MUST 新增：

```json
{
  "target_set_digest": {
    "$ref": "#/$defs/digest"
  },
  "forget_fence_namespace_ref": {
    "$ref": "#/$defs/ref"
  }
}
```

对于 D 的 `LINEAGE` 和 `BARRIER_MEMBERSHIP` evidence，两个字段 SHOULD 条件必填。

### 5.8 Target-set digest 与 lineage manifest digest

不得直接假定两个 digest 相等。

定义：

- `target_set_digest`：Fence 安装时确定的不可变目标集合摘要。
- `lineage_manifest_digest`：Lineage Manifest 内容摘要。

二者语义不同。

建议绑定为：

```python
evidence["target_set_digest"] \
    == currentness_proof["target_set_digest"]
```

```python
evidence["lineage_manifest_digest"] \
    == currentness_proof["lineage_manifest_digest"]
```

第二个等式要求 currentness proof 增加 `lineage_manifest_digest`。该字段属于本轮建议的正式实现。

Target set 与 Lineage Manifest 的内容关系为：

```text
LineageManifest.TargetSetDigest
    == ForgetFenceCursor.target_set_digest
```

只有 D 权威 Lineage Manifest 明确声明该绑定时，才 MAY 接受此关系。

以下内容 MUST NOT 作为默认规则：

```python
target_set_digest == lineage_manifest_digest
```

本证据包没有提供完整的 D Lineage Manifest schema，因此其 canonicalization 和 digest domain 为 `NOT_SUPPLIED`。

### 5.9 唯一 Fence 绑定

唯一合法关系为：

```python
evidence["fence_generation"] \
    == currentness_proof["forget_fence_generation"]
```

```python
evidence["forget_operation_ref"] \
    == currentness_proof["forget_operation_ref"]
```

```python
evidence["target_set_digest"] \
    == currentness_proof["target_set_digest"]
```

```python
evidence["forget_fence_namespace_ref"] \
    == currentness_proof["forget_fence_namespace_ref"]
```

同时：

```python
currentness_proof["forget_fence_generation"] \
    <= currentness_proof["forget_fence_generation_high_water"]
```

High-water MUST 属于 ForgetFence namespace。MUST NOT 来源于 ProducerWork Registration Ledger。

## 6. Fence 当前性证明与判定顺序

### 6.1 必需验证顺序

MUST 按照以下顺序执行：

1. 验证 D Owner 身份。
2. 验证 ForgetOperation reference。
3. 验证目标集合摘要。
4. 验证 Fence namespace reference。
5. 验证 FenceGeneration 和 FenceGenerationHighWater 的十进制格式。
6. 验证 `evidence.fence_generation` 与 `proof.fence_generation` 相等。
7. 验证 FenceGeneration 不超过其对应 namespace 的 high-water。
8. 验证 Owner snapshot reference 和 digest。
9. 验证 anti-rollback anchor。
10. 验证 proof signature。
11. 验证 D Owner ledger currentness。
12. 验证 `currentness_status`。

### 6.2 判定表

| 条件 | 结果 |
|---|---|
| Generation 大于对应 high-water | INVALID |
| Operation reference 不相等 | INVALID |
| `target_set_digest` 不相等 | INVALID |
| Namespace 不相等 | INVALID |
| Proof generation 与 evidence generation 不相等 | INVALID |
| 明确返回 STALE | INVALID |
| 签名明确被拒绝 | INVALID |
| Currentness proof 缺失 | UNKNOWN |
| Currentness 查询不可用 | UNKNOWN |
| `currentness_status` 为 UNKNOWN | UNKNOWN |
| Anti-rollback 无法验证 | UNKNOWN |
| 所有检查通过且 currentness 为 CURRENT | VALID |

### 6.3 当前性要求

**仅仅证明 FenceGeneration 数值小于某个 high-water，MUST NOT 被视为已经证明它是最新适用 Fence。**

当前性 MUST 由 D 权威 currentness proof 证明。

H MUST NOT 通过独立比较多个 counter 自行推定当前性。

§5 中的 currentness proof 结构是 H 侧设计提案。其 D 权威签发、签名和查询实现仍未核验。

## 7. Schema 新增（字段名、类型、必填性、`$defs` 位置）

### 7.1 Schema 契约新增内容

建议的 RecoveryJoin schema 新增内容汇总如下。

| Schema 位置 | 字段 | 类型 | 必填性 |
|---|---|---|---|
| `$defs/forgetFenceGeneration` | Primitive 定义 | String，`^(0|[1-9][0-9]*)$` | 供类型化 Fence 字段使用 |
| `$defs/forgetFenceCurrentnessProof` | Proof object | Object，`additionalProperties: false` | 所列全部字段必填 |
| `ownerSnapshot` | `forget_fence_namespace_ref` | `$defs/ref` | D 必填 |
| `ownerSnapshot` | `forget_fence_generation_high_water` | `$defs/forgetFenceGeneration` | D 必填 |
| `ownerSnapshot` | `forget_fence_currentness_proof_ref` | `$defs/ref` | D 必填 |
| `ownerSnapshot` | `forget_fence_currentness_proof_digest` | `$defs/digest` | D 必填 |
| `ownerSnapshotMembershipProof` | `forget_fence_namespace_ref` | `$defs/ref` | D 条件必填 |
| `ownerSnapshotMembershipProof` | `forget_fence_generation_high_water` | `$defs/forgetFenceGeneration` | D 条件必填 |
| `ownerSnapshotMembershipProof` | `forget_fence_currentness_proof_ref` | `$defs/ref` | D 条件必填 |
| `ownerSnapshotMembershipProof` | `forget_fence_currentness_proof_digest` | `$defs/digest` | D 条件必填 |
| owner evidence Forget 分支 | `target_set_digest` | `$defs/digest` | D LINEAGE 和 BARRIER_MEMBERSHIP 条件必填 |
| owner evidence Forget 分支 | `forget_fence_namespace_ref` | `$defs/ref` | D LINEAGE 和 BARRIER_MEMBERSHIP 条件必填 |
| D snapshot | `producer_registration_sequence_namespace_ref` | `$defs/ref` | D 必填 |
| D snapshot | `producer_registration_high_water` | 现有类型化十进制字段 | D producer cutoff 绑定必填 |
| Membership proof | `producer_registration_sequence_namespace_ref` | `$defs/ref` | D 必填 |
| Membership proof | `producer_registration_high_water` | `$defs/counter` | D 必填 |

### 7.2 名义类型要求

MUST NOT 将 JSON Schema 的 primitive 校验单独表述为完整名义类型校验。

完整类型绑定要求：

- 正确的字段位置。
- 正确的 Owner。
- 正确的 namespace。
- 适用时正确的 operation binding。
- 正确的 snapshot equality。
- 正确的权威证明。
- 正确的十进制格式。
- 适用时正确的 currentness。

### 7.3 版本兼容

建议的 schema 和 runtime 修改 MUST 一起版本化。

建议的共享契约版本为 `OWNER-SNAPSHOT-CONTRACT-1.2.18`。

所提供设计中的现有 RecoveryJoin schema 标识仍为 `bmcp.recovery-join-1.0.2.schema.json`。

如果实际 schema 升级为 1.0.3，则文件名和测试命名 MUST 相应迁移。MUST NOT 使用旧版本号掩盖 schema 变更。

## 8. Validator 合一（方案 C、修改清单、版本化契约）

### 8.1 实测分叉

探针已经证明：

- 两个 Validator 使用 exact-set 语义。
- D、I、C Owner allowlist 不一致。
- 同一个 snapshot 不可能同时通过两个 Validator。
- `validate_union()` 仅调用本地 `validate_owner_snapshot()`。
- 1.2.17 Validator 没有参与组合调用路径。

MUST NOT 继续将两个 Validator 描述为仅有严格程度差异但彼此兼容。

这是结构性不兼容。

### 8.2 设计方案

| 方案 | 设计 | 优点 | 风险 |
|---|---|---|---|
| A | 在组合 runtime 内联 1.2.17 的 8 键 D allowlist | 修改较少 | 双份定义继续漂移 |
| B | 让 1.2.17 成为唯一 snapshot validator，组合路径委派调用 | 单一验证实现 | Schema allowlist 仍可能与其他模块漂移 |
| C | 抽取共享 allowlist 常量模块，两处引用同一个真相源 | 同时解决定义漂移和调用不一致 | 需要重构及更完整的回归测试 |

**推荐方案：C — Shared Owner Snapshot Contract Module。**

理由：

1. 实测问题同时包括组合调用错误和 allowlist 定义不一致。
2. 单纯委派无法防止其他模块重新维护独立字段集合。
3. 共享模块能够为组合 runtime 和独立 Validator 提供同一个真相源。
4. Schema 字段登记也必须具有唯一的受管理来源，以防再次出现 schema/Python 分叉。

### 8.3 修改清单

以下为证据包提供的真实工件路径。行号以该证据包提供的源码片段为准。未提供完整文件的行号不作推定。

| 文件 | 函数/区域 | 行区间 | 修改 |
|---|---|---|---|
| `08-bmcp-protocol/runtime_reference/owner_snapshot_contract.py` | 新模块 | 新增 | 定义版本化 `OWNER_FIELDS`、字段类型分类及 schema contract version |
| `08-bmcp-protocol/runtime_reference/unified_manifest_semantics.py` | `validate_owner_snapshot()` | 41–62 | 移除独立硬编码 allowlist，引用共享常量 |
| 同上 | `validate_owner_snapshot_membership_proof_payload()` | 67–119 | 增加 D 类型化 namespace、ProducerRegistrationHighWater 及 Fence proof 绑定 |
| 同上 | `validate_union()` | 123–190 | 替换第 157 行泛型 admission binding；增加双高水位及 currentness 判定 |
| `08-bmcp-protocol/runtime_reference/owner_snapshot_semantics_1_2_17.py` | `OWNER_FIELDS` | 17–31 | 从共享模块导入，同时保留独立 Validator 的职责 |
| 同上 | `validate_owner_snapshot_1_2_17()` | 39–91 | 使用共享 allowlist；保留 DECIMAL、HEX64 和 digest 校验 |
| `08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json` | `$defs` | NOT_SUPPLIED | 新增类型化字段及 currentness proof schema |
| `08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` | RJ102 tests | NOT_SUPPLIED | 增加新版本 fixture 和全部双跑测试 |

### 8.4 共享模块契约

共享模块 SHOULD 定义：

```python
CONTRACT_VERSION = "OWNER-SNAPSHOT-CONTRACT-1.2.18"

OWNER_FIELDS = {
    "I": {
        "receipt_issue_high_water",
        "receipt_consume_high_water",
        "permission_epoch",
        "producer_domain_inventory_epoch_ref",
        "registry_snapshot_digest",
        "relevant_entry_set_root",
    },
    "D": {
        "producer_registration_high_water",
        "work_item_high_water",
        "attempt_high_water",
        "barrier_generation",
        "barrier_root",
        "forget_fence_generation_high_water",
        "dependency_closure_cursor",
        "dependency_closure_root",
    },
    "C": {
        "reservation_high_water",
        "provider_attempt_high_water",
        "provider_outcome_high_water",
        "provider_idempotency_namespace_ref",
        "final_request_boundary_generation",
    },
}
```

`1.2.18` 是建议的新契约版本号，不是已经发布的版本，也不是现有 1.2.17 的事实延伸。

新版本 MUST 经过 schema、runtime、fixture 和测试一致性验证后才能声明生效。

### 8.5 字段集合分离

如果组合 runtime 需要额外字段，MUST NOT 直接将扩展字段加入 `OWNER_FIELDS`。

建议分离为：

```python
OWNER_FIELDS
OWNER_SNAPSHOT_BASE_FIELDS
OWNER_SNAPSHOT_COMPOSITION_EXTENSION_FIELDS
```

判定时 MUST 明确区分：

- Owner-specific fields。
- Snapshot base fields。
- Composition extension fields。

三个集合均 MUST 由同一版本化 contract 管理。

MUST 保留 exact-set 语义。

MUST NOT 仅为让两个 Validator 同时通过而将 exact-set 校验改为不受约束的 subset/contains 判断。

### 8.6 既有测试影响

以下既有测试需要更新 fixture，部分旧 fixture 预期会转红。

| 测试 | 预期影响 |
|---|---|
| RJ102-01 schema metadata | 更新 schema metadata 和版本断言 |
| RJ102-02 exact owner membership proof | 缺少 D 类型化绑定字段的旧 proof MUST 为 INVALID |
| RJ102-03 missing snapshot attestation digest | 保留现有负例 |
| RJ102-04 missing anti-rollback anchor | 保留现有负例 |
| RJ102-05 wrong purpose | 保留现有负例 |
| RJ102-06 admission join | D proof fixture MUST 增加双高水位绑定 |
| RJ102-07 no participant disposition | 同样更新 D proof fixture |
| RJ102-08 owner proof inventory | 更新 D proof inventory |
| RJ102-09 missing verifier | 保留 UNKNOWN |
| RJ102-10 valid owner verifier | 更新为完整类型化 fixture |
| RJ102-11 entry digest mismatch | 保留 INVALID |
| RJ102-12 sequence above highwater | 改为针对 ProducerRegistrationHighWater 的精确 cutoff 测试 |
| RJ102-13 UNKNOWN signature result | 保留 UNKNOWN |
| RJ102-14 rejected signature | 保留 INVALID |

额外要求：

1. 1.2.17 测试中的旧五键 D fixture MUST 转红。MUST NOT 为了兼容 fixture 而保留错误的五键定义。
2. I 域旧字段名 `inventory_epoch_ref` MUST 统一迁移为 `producer_domain_inventory_epoch_ref`。
3. C 域旧三键 fixture MUST 补齐 1.2.17 已要求的扩展字段。
4. 通过显式 legacy decoder 读取历史 fixture，必须单独定义迁移策略。Legacy decoder MUST NOT 参与新版本 RecoveryJoin 的 `VALID` 判定。

### 8.7 版本相等要求

以下等式 MUST 成立：

```text
Schema Contract Version
    == Shared Owner Snapshot Contract Version
    == Composed Runtime Contract Version
    == Independent Validator Contract Version
```

如果任意版本不相等：

- 实现 MUST NOT 返回 `VALID`。
- 明确的版本冲突 MUST 返回 `INVALID`。
- 权威版本信息缺失 MUST 返回 `UNKNOWN`。

进一步要求：

1. Schema 扩展 MUST 在共享模块登记。
2. 任何 Owner 字段变更 MUST 同步提升 contract version。
3. 只修改 schema 而不修改 runtime 属于禁止行为。
4. 只修改独立 Validator 而不修改组合 runtime 属于禁止行为。
5. 测试 MUST 从共享常量生成预期字段集合。
6. MUST 至少保留一个独立硬编码的 expected fixture，以防共享实现和测试同时出现相同错误。
7. 组合路径 MUST 使用共享 Validator 实现，MUST NOT 复制另一份验证逻辑。

## 9. 永久禁止项

以下组合无论数值是否相同，均 MUST 判定为 `INVALID`。

| 禁止组合 | 判定 | 对应 D 控制契约 §3 |
|---|---|---|
| ProducerRegistrationHighWater 替代 ForgetFenceGeneration | INVALID | 两者不能互换 |
| ForgetFenceGeneration 替代 ProducerRegistrationHighWater | INVALID | 两者不能互换 |
| ProducerRegistrationHighWater 与 CanonicalCommitCursor 比较 | INVALID | 两者不能互换 |
| ForgetFenceGeneration 与 CanonicalCommitCursor 比较 | INVALID | 两者不能互换 |
| ProducerRegistrationHighWater 与 PermissionEpoch 比较或替代 | INVALID | 两者不能互换 |
| ProducerRegistrationHighWater 与 I ProducerDomainInventoryEpoch 替代 | INVALID | 两者不能互换 |
| ForgetFenceGeneration 与 I ProducerDomainInventoryEpoch 替代 | INVALID | 两者不能互换 |
| D ProducerWork namespace 与 ForgetFence namespace 混用 | INVALID | 类型和命名空间独立 |
| D ProducerWork namespace 与 I inventory namespace 混用 | INVALID | §3 明确禁止 |
| 不同 Canonical Memory Authority 的 ProducerRegistration namespace 混用 | INVALID | Authority scope 不同 |
| 因数值相同而使用不同账本来源的 high-water 相互替代 | INVALID | 数值相等不构成来源证明 |
| `owner_high_water` 与 snapshot 类型化值不相等 | INVALID | Snapshot equality 不成立 |
| `evidence.fence_generation` 与 currentness proof 不相等 | INVALID | Fence cursor 绑定失败 |
| 不同 `target_set_digest` 的 Fence proof 混用 | INVALID | ForgetFenceCursor 目标集合不一致 |
| 仅用 `lineage_manifest_digest` 替代 `target_set_digest` | INVALID | 摘要语义不同 |
| 将 UNKNOWN currentness 当作 CURRENT | INVALID | UNKNOWN 不构成当前性证明 |
| 通过删除额外字段使两个 Validator 中某一方通过 | INVALID | Exact-set contract 被破坏 |

对应 D 控制契约 §3：

> ProducerRegistrationHighWater 限定于该 Canonical Memory Authority 的 ProducerWork Registration Ledger。CanonicalCommitCursor 是独立的每个 Brain Authority Commit Order/Audit Cursor。两者都不能与 FenceGeneration、PermissionEpoch 或 I ProducerDomainInventoryEpoch 互换。

H MUST 遵守该条款，MUST NOT 自行扩大任何 counter 的比较域。

## 10. 一致性测试向量 V01–V24

### 10.1 测试状态

以下向量是规范性设计要求。

**NOT RUN — 本设计记录中尚未执行这些向量。**

建议测试文件：

`08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py`

新增测试 SHOULD 按 contract version 分组。

如果实际 schema 升级为 1.0.3，则文件名及测试命名 MUST 相应迁移。MUST NOT 使用旧版本号掩盖 schema 变更。

### 10.2 完整测试向量表

| ID | 向量名称 | 精确输入变更 | 预期结果 | 依据 | 测试文件 |
|---|---|---|---|---|---|
| V01 | D producer cutoff below | `owner_local_sequence="4"`；ProducerRegistrationHighWater=`"5"` | VALID | D §3；1.2.17:82–88 | recovery_join |
| V02 | D producer cutoff equal | `owner_local_sequence="5"`；ProducerRegistrationHighWater=`"5"` | VALID | D §3；1.2.17:82–88 | recovery_join |
| V03 | D producer cutoff above | `owner_local_sequence="6"`；ProducerRegistrationHighWater=`"5"` | INVALID | D §3；1.2.17:86–88 | recovery_join |
| V04 | Fence changes, producer fixed | ProducerRegistrationHighWater=`"5"` 不变；FenceGeneration 从 `"3"` 改为 `"4"`，两者均有对应有效 Fence proof | VALID，成员 cutoff 判定不变 | D §3；ForgetFenceCursor 语义 | recovery_join |
| V05 | Producer changes, fence fixed | FenceGeneration=`"3"` 不变；ProducerRegistrationHighWater 从 `"5"` 改为 `"4"`；local sequence=`"5"` | INVALID | D §3；1.2.17:86–88 | recovery_join |
| V06 | Fence substituted as producer cutoff | `owner_high_water="3"`；FenceGeneration=`"3"`；ProducerRegistrationHighWater=`"5"` | INVALID | D §3；1.2.17:82–88 | recovery_join |
| V07 | Producer substituted as fence generation | `evidence.fence_generation="5"`；`proof.fence_generation="3"` | INVALID | D §3；ForgetFenceCursor 语义 | recovery_join |
| V08 | Producer namespace mismatch | `proof.owner_sequence_namespace="namespace-A"`；`snapshot.producer_registration_sequence_namespace_ref="namespace-B"` | INVALID | D §3；namespace binding | recovery_join |
| V09 | Fence namespace mismatch | `evidence.forget_fence_namespace_ref="fence-A"`；`proof.forget_fence_namespace_ref="fence-B"` | INVALID | D §3；ForgetFenceCursor 语义 | recovery_join |
| V10 | Producer non-decimal | `snapshot.producer_registration_high_water="NOT_A_NUMBER"` | INVALID | 1.2.17:86–88 | recovery_join |
| V11 | Fence non-decimal | `snapshot.forget_fence_generation_high_water="NOT_A_NUMBER"` | INVALID | 1.2.17 数值校验原则 | recovery_join |
| V12 | Same value, different source | `owner_high_water="5"`；`snapshot.producer_registration_high_water="5"`；namespace 指向另一账本 | INVALID | D §3 | recovery_join |
| V13 | Generic/specific mismatch | `proof.owner_high_water="6"`；`proof.producer_registration_high_water="5"` | INVALID | D §3；snapshot equality | recovery_join |
| V14 | Missing fence currentness | 删除 `forget_fence_currentness_proof_ref` | UNKNOWN | D latest applicable Fence requirement | recovery_join |
| V15 | Stale fence | `currentness_status="STALE"` | INVALID | D §3；最新适用 Fence | recovery_join |
| V16 | Dual-validator same fixture | 使用同一份完整 D fixture，分别调用组合 Validator 和独立 Validator | 两者 MUST 返回相同结果 | 1.2.17:49–91；组合 runtime:123–139 | recovery_join + owner_snapshot_semantics |
| V17 | D allowlist exact equality | 删除 `dependency_closure_root` | INVALID | 1.2.17:63–65 | owner_snapshot_semantics |
| V18 | I allowlist alignment | 使用包含 `producer_domain_inventory_epoch_ref` 和 `permission_epoch` 的完整集合 | 两个 Validator MUST 返回相同结果 | 1.2.17:17–21 | recovery_join |
| V19 | C allowlist alignment | 增加 `provider_idempotency_namespace_ref` 和 `final_request_boundary_generation` | 两个 Validator MUST 返回相同结果 | 1.2.17:27–30 | recovery_join |
| V20 | Fence generation beyond highwater | `forget_fence_generation="6"`；high-water=`"5"` | INVALID | ForgetFence namespace monotonicity | recovery_join |
| V21 | Target digest mismatch | `evidence.target_set_digest` 与 `currentness_proof.target_set_digest` 不相等 | INVALID | D ForgetFenceCursor 三元组 | recovery_join |
| V22 | UNKNOWN signature | Fence currentness proof signature verifier 返回 UNKNOWN | UNKNOWN | 现有 RJ102-13 语义 | recovery_join |
| V23 | Missing producer namespace | 删除 `snapshot.producer_registration_sequence_namespace_ref` | UNKNOWN | Namespace authority unavailable | recovery_join |
| V24 | Missing producer high-water | 删除 D snapshot 中的 `producer_registration_high_water` | UNKNOWN | 1.2.17:60–65 | recovery_join |

### 10.3 V16 双 Validator 要求

V16 MUST NOT 仅比较两个 Validator 是否返回相同布尔值。

MUST 使用相同 fixture、相同版本和相同 verifier 输入，并比较：

```python
result_composed == result_independent
```

对于 VALID fixture，两者 MUST 均返回 `VALID`。

对于 INVALID fixture，两者 MUST 均返回 `INVALID`。

对于缺少权威证明的 fixture，两者 MUST 均返回 `UNKNOWN`。

MUST NOT 通过以下方式制造表面一致性：

- 不同 fixture。
- 不同 allowlist。
- 不同 schema version。
- 不同输入 snapshot。
- 不同签名验证结果。

### 10.4 跨版本负向测试

MUST 增加一个跨版本 negative test。

当旧 1.2.17 snapshot 缺少新版本必填字段时，MUST NOT 将其直接视为新版本 `VALID`。

## 11. 证据状态：探针、NOT RUN 声明、Storage NOT_SUPPLIED、最低替代证据

### 11.1 机械探针状态

本记录目前最高等级的证据为：

**17 项机械探针：全部 PASS。**

| 探针组 | 结果 |
|---|---|
| A1–A7 | PASS |
| B1–B3 | PASS |
| C1–C4 | PASS |
| D1–D2 | PASS |
| E1–E2 | PASS |

这些探针证明被检查源码存在已识别缺陷。

它们不证明修复已经发生。

### 11.2 历史 CI 排除

历史 CI 证据：

| 属性 | 值 |
|---|---|
| Run | `44215993536` |
| Job | `134505846435` |
| HEAD | `654d4449fd491cdda37d9761fe63a3efca55dc9d` |
| Discovered | 390 |
| Skipped | 22 |
| Executed | 368 |

该 CI 执行于与修复目标不同的 HEAD。

它只能证明当时该历史执行覆盖的测试通过。

**MUST NOT 使用历史 Run `44215993536` / Job `134505846435` 关闭 H-RJ-HW-01。**

### 11.3 最低替代性实现证据

在运行时仓尚未合入 main 的情况下，最低替代性交付证据为：

1. 修复分支 exact HEAD SHA。
2. 全部修改文件的 Blob SHA。
3. 新 schema 实际内容和版本号。
4. 共享 allowlist 模块完整源码。
5. 修改后的组合 runtime 完整源码。
6. 修改后的独立 Validator 完整源码。
7. 新增测试函数完整源码。
8. 正例和负例 fixture。
9. 本地测试命令及原始 stdout/stderr。
10. 测试 discovery 数量、executed 数量和 skipped 数量。
11. 每个新测试的实际断言结果。
12. 双 Validator 使用同一 fixture 执行的原始结果。

这些材料仅可作为实现阶段的替代性技术证据。

MUST NOT 用其替代 exact-head CI。

### 11.4 条件 5 — Exact-head CI 要求

条件 5 只有在提供以下材料后才能关闭：

| 项目 | 要求 |
|---|---|
| Exact Head | 修复后的完整 commit SHA |
| Workflow | 实际执行的 workflow 文件路径及 Blob SHA |
| Run | GitHub Actions Run ID |
| Job | 对应 Job ID |
| Test report | 测试总数、执行数、跳过数和失败数 |
| Raw log | 可核验的原始日志 |
| New tests | V01–V24 实际执行记录 |
| Existing tests | RJ102 和 1.2.17 回归结果 |
| Double validator | 同 fixture 双跑原始结果 |
| Schema | Exact HEAD 中的 schema 版本及 SHA |

分支名称、PR 标题、提交说明和历史 Run MUST NOT 替代 exact HEAD 证据。

**当前条件 5：BLOCKED。**

### 11.5 强制 NOT RUN 声明

```text
NOT RUN — 本会话未在修复后的 exact HEAD 上运行 GitHub Actions CI。
历史 Run 44215993536 / Job 134505846435 属于 HEAD 654d4449fd491cdda37d9761fe63a3efca55dc9d，不构成本 Finding 的修复验证证据。
本会话的 17 项机械探针仅证明已检查源码的缺陷状态，不证明修复、集成或 CI 成功。
NOT RUN MUST NOT 被转换为 PASS。
```

### 11.6 禁止性声明

在运行时仓尚未合入 main 时，本记录 MUST NOT 声称：

- main 已包含修复。
- RecoveryJoin 组合校验已统一。
- ProducerRegistrationHighWater 已具有有效的组合路径绑定。
- ForgetFenceGeneration 已实现当前性证明。
- 两个 Validator 已通过新测试。
- Storage 同版本映射已经完成。
- 生产环境符合协议。
- D/E/I/Storage Owner 已批准变更。
- 真人 R3 审查已经完成。
- 生产激活已经完成。
- 平台独立门禁已经通过。

真人 R3 审查、生产激活和平台独立门禁均为 `OUT-OF-SCOPE`，不属于本技术关闭记录的范围。

### 11.7 Storage 证据状态

<badge color="danger">BLOCKED / NOT_SUPPLIED</badge>

本证据包没有提供 Storage JoinProof 同版本原文。

因此，本契约 MUST NOT 推测 Storage 字段，也 MUST NOT 将历史 Issue #29 评论作为核验证据。

必须共同核验以下版本标识：

| 工件 | 必须提供的标识 | 当前状态 |
|---|---|---|
| Storage manifest | 精确版本号、commit SHA 和 Blob SHA | NOT_SUPPLIED |
| Storage JoinProof schema | 精确版本号和 Blob SHA | NOT_SUPPLIED |
| Storage JoinProof 实现 | 精确路径和 Blob SHA | NOT_SUPPLIED |
| D 控制契约源 | `03-memory-brain/forget-fence-operation-and-publication-gate-part4.md`，Blob SHA `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | SUPPLIED |
| H RecoveryJoin schema | `bmcp.recovery-join-1.0.2.schema.json`，Blob SHA `4b664e3bce465499bcdfd93796349a4ba7074002` | SUPPLIED |
| H 组合 runtime | `unified_manifest_semantics.py`，Blob SHA `e26379d38825ee13d15f652d3bd019c4091da37d` | SUPPLIED |
| H 独立 Validator | `owner_snapshot_semantics_1_2_17.py`，Blob SHA `17275eebd0013f8ad8765670a7faaa40866d99d8` | SUPPLIED |

同版本并不意味着不同工件必须使用相同数字版本号。

它意味着：

1. Storage manifest 声明的 schema version 与实际 JoinProof schema 一致。
2. Storage JoinProof 实际字段与被引用的 manifest 字段一致。
3. Storage → H 映射所引用的 D 契约版本明确。
4. D 字段语义与 H schema 字段语义一致。
5. H schema 版本与组合 runtime 使用的 contract version 一致。
6. 每个映射均具有精确版本、字段路径和直接证据。
7. MUST NOT 使用历史评论中的字段名称替代当前工件的直接读取结果。

### 11.8 Storage 字段级核验表

以下字段 MUST 核验。未知 Storage 字段 MUST NOT 推测。

| Storage 字段 | D 字段 | 类型 | 是否同版本可映射 | 证据位置 |
|---|---|---|---|---|
| NOT_SUPPLIED | `producer_registration_high_water` | ProducerRegistrationHighWater | NOT_SUPPLIED | D §3 已提供；Storage 未提供 |
| NOT_SUPPLIED | `producer_registration_sequence_namespace_ref` | D ProducerWork Ledger namespace ref | NOT_SUPPLIED | 本轮新增设计字段；D 实际载体 NOT_SUPPLIED |
| NOT_SUPPLIED | `forget_fence_generation_high_water` | ForgetFenceGeneration | NOT_SUPPLIED | 1.2.17 第 23–25 行；Storage 未提供 |
| NOT_SUPPLIED | `forget_fence_namespace_ref` | ForgetFence namespace ref | NOT_SUPPLIED | 本轮新增设计字段 |
| NOT_SUPPLIED | `forget_operation_ref` | ForgetOperation reference | NOT_SUPPLIED | D 控制契约及 evidence schema |
| NOT_SUPPLIED | `target_set_digest` | Digest | NOT_SUPPLIED | D ForgetFenceCursor 语义 |
| NOT_SUPPLIED | `lineage_manifest_digest` | Digest | NOT_SUPPLIED | D evidence schema |
| NOT_SUPPLIED | `fence_generation` | ForgetFenceGeneration | NOT_SUPPLIED | H owner evidence schema |
| NOT_SUPPLIED | `owner_snapshot_ref` | Snapshot reference | NOT_SUPPLIED | H membership proof schema |
| NOT_SUPPLIED | `owner_snapshot_digest` | Digest | NOT_SUPPLIED | H membership proof schema |
| NOT_SUPPLIED | `anti_rollback_anchor_ref` | Reference | NOT_SUPPLIED | H membership proof schema |
| NOT_SUPPLIED | `barrier_generation` | D barrier generation | NOT_SUPPLIED | 1.2.17 第 23–25 行 |

### 11.9 Storage Owner 交付要求

Storage Owner MUST 提供：

1. Storage manifest 原始文件及精确路径。
2. Storage manifest 精确版本号和 Blob SHA。
3. Storage JoinProof schema 原文。
4. Storage JoinProof schema 精确版本号和 Blob SHA。
5. Storage JoinProof producer/admission 相关字段定义。
6. Storage JoinProof 与 D ProducerRegistrationHighWater 的直接映射定义。
7. Storage JoinProof 与 ForgetFenceGeneration 的直接映射定义。
8. ForgetOperation 与 target-set digest 的绑定定义。
9. Storage currentness/anti-rollback 证明字段。
10. 同版本实现或 conformance fixture。
11. 每个字段的类型、来源和权威签发方。
12. 可重现的字段级映射核验结果。

只有取得上述工件后，才 MAY 将 `NOT_SUPPLIED` 转换为实际核验结果。

**字段同名、类型相似和历史 Issue 评论 MUST NOT 被视为同版本映射证据。**

## 12. 关闭条件映射、复查点与非声明事项

### 12.1 文档和实现载体

已登记设计确定了两个建议载体：

**Issue #25 评论**

登记完整设计处置，包括：

- 关闭条件 1–6。
- F1–F3 实测结论。
- 推荐方案 C。
- NOT RUN 声明。
- Storage NOT_SUPPLIED 状态。
- 修复责任和退出条件。

Issue #25 继续作为 Phase 3.7/3.8 visibility protocol 与 RecoveryJoin 相关精确版本核验的主要跟踪载体。

**独立 PR 文档**

建议仓库路径为：

```text
08-bmcp-protocol/
  phase-3.8-h-rj-hw-01-typed-watermark-and-fence-binding-contract.md
```

该文档是 H 侧语义修复设计的建议正式版本化载体。

其范围包括：

1. ProducerRegistrationHighWater 语义契约。
2. ForgetFenceGeneration 语义契约。
3. Namespace binding。
4. Currentness proof。
5. Shared Validator contract。
6. 测试向量。
7. Storage mapping checklist。
8. 版本兼容和迁移要求。

提交该设计或后续实现的 PR 本身 MUST NOT 被视为批准或合并证据。

本文件采用单文件双语，符合仓库双语文档载体要求。本文档不要求另建 `docs/en/` 或 `docs/zh-CN/` 配对文件。

实际双语门禁仍以 PR #271 中 GOV-DOC-001 v1.2 最终生效规则为准。本文档不独立修改该治理流程。

### 12.2 建议子 Finding

建议新增三个子 Finding，但不替代 `H-RJ-HW-01`。

| 建议 ID | 标题 | 严重性 | 关系 |
|---|---|---|---|
| H-RJ-HW-01A | D ProducerRegistrationHighWater Binding Failure | P1 | H-RJ-HW-01 子项 |
| H-RJ-HW-01B | ForgetFenceGeneration Snapshot and Currentness Binding Failure | P1 | H-RJ-HW-01 子项 |
| H-RJ-HW-01C | Owner Snapshot Validator Contract Divergence | P1 | H-RJ-HW-01 子项 |

F1 和 F2 可归入 01C 下两个独立技术断言：

- 01C-1：allowlist exact-set divergence。
- 01C-2：composed validator dispatch divergence。

三个问题具有不同的修复路径和验证向量。

是否创建新的 Finding ID 仍属于仓库 Owner 的治理决定。本契约只提出拆分建议，不创建 Issue，不改变现有 Finding 状态。

### 12.3 复查处置

**建议处置：HOLD。**

理由：

- 17 项探针已经证明原实现存在确定性缺陷。
- 条件 1、2 仍缺少 D 权威字段定义和证明实现。
- 条件 3、4 尚无修复实现证据。
- 条件 5 没有 exact-head CI 证据。
- 条件 6 明确为 NOT_SUPPLIED。

不得仅因本设计完成就将 Issue #25 改为可关闭状态。

### 12.4 复查点

| 复查点 | 必须交付的材料 | 退出标准 |
|---|---|---|
| R1 — D 双高水位 | D namespace、snapshot 和 proof 原文 | 类型及 equality 绑定可验证 |
| R2 — Fence currentness | D Fence Currentness Proof 原文 | Operation、target、generation 和 currentness 可验证 |
| R3 — Validator 合一 | 共享模块及两个调用路径 | 相同 contract version、相同 allowlist |
| R4 — 行为测试 | V01–V24 实际测试及 raw output | 所有正负例符合预期 |
| R5 — CI | Exact HEAD、Run、Job、workflow 和 raw log | 精确 HEAD 测试通过 |
| R6 — Storage | 同版本 manifest、schema 和 JoinProof | 字段级映射逐项核验 |

R1–R4 完成后，可提交技术实现状态重新评估。

R5 完成后，才能评估 CI 条件。

R6 完成后，才能评估 Storage 同版本映射条件。

即使全部技术条件完成，也 MUST NOT 自动认定真人 R3 审查、生产激活或平台独立门禁已经完成。

### 12.5 已确认发现

以下内容是被检查源码中的已确认发现：

1. 组合 runtime 的 D allowlist 不完整。
2. 组合 runtime 与独立 1.2.17 Validator 的 D/I/C allowlist 存在结构性互斥。
3. 组合 `validate_union()` 不调用独立 1.2.17 Validator。
4. 组合路径将 `owner_high_water` 错误绑定到泛型 `admission_high_water`。
5. 组合路径未正确绑定类型化 ProducerRegistrationHighWater。
6. 组合路径缺少对应的 DECIMAL 类型校验。
7. RecoveryJoin 1.0.2 schema 没有提供 ForgetFenceGeneration high-water 的 snapshot 载体。
8. `fence_generation` 目前只出现在 evidence 的 Forget 分支。
9. 既有 RJ102-01..14 测试不能证明本 Finding 的六项关闭条件。
10. 本轮 17 项机械探针全部 PASS，但没有修复后的 exact-head CI 证据。

### 12.6 明确非声明事项

以下事项均未得到证实：

1. D Owner 已批准本设计。
2. D 已提供新的 namespace canonicalization 规范。
3. D 已提供权威 Fence Currentness Proof 实现。
4. H 已完成 schema 和 runtime 修改。
5. 两个 Validator 已经合一。
6. 新测试已经成功执行。
7. Exact-head CI 已经通过。
8. Storage 同版本映射已经成立。
9. D/E/I/Storage 已实现生产 conformance。
10. 真人 R3 审查已经完成。
11. 生产激活已经完成。
12. 平台独立门禁已经完成。

### 12.7 最终状态表

| 项目 | 本轮结论 |
|---|---|
| H-RJ-HW-01 | OPEN |
| Severity | P1 |
| Validation | TO_VALIDATE |
| F1 | CONFIRMED |
| F2 | CONFIRMED |
| F3 | CONFIRMED |
| 条件 1 | ADVANCEABLE |
| 条件 2 | ADVANCEABLE |
| 条件 3 | ADVANCEABLE |
| 条件 4 | ADVANCEABLE |
| 条件 5 | BLOCKED |
| 条件 6 | BLOCKED / NOT_SUPPLIED |
| 推荐修复方案 | Shared Owner Snapshot Contract Module |
| Issue 管理建议 | HOLD |
| 生产符合性 | NOT ASSESSED |
| 真人 R3 审查 | OUT-OF-SCOPE |
| 生产激活 | OUT-OF-SCOPE |
| 平台独立门禁 | OUT-OF-SCOPE |

### 12.8 最终处置

**HOLD — REMEDIATION DESIGN PROVIDED / IMPLEMENTATION NOT VERIFIED。**

本文档记录的是 H 侧语义契约修复设计，不是修复实现验收。

`H-RJ-HW-01` MUST NOT 因本文档发布而关闭。

`ADVANCEABLE` MUST NOT 转换为 `CLOSED`。

`NOT RUN` MUST NOT 转换为 `PASS`。

`NOT_SUPPLIED` MUST NOT 被表述为已核验。

建议的下一步执行责任：

- **H Owner：** 按照设计实现共享 contract、双高水位绑定和 currentness proof 集成。
- **D Owner：** 补充权威 namespace 和 Fence Currentness Proof 规范。
- **Storage Owner：** 提供同版本 JoinProof 工件。

三方所需材料齐备后，必须针对精确修复 HEAD 重新执行完整验证。

---
