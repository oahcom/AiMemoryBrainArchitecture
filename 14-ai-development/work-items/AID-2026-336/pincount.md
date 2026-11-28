---
document_metadata:
  steward: USER-PRINCIPAL-DELEGATED
  domain: repository-governance
  role: pin-count-definition
  lifecycle: active
  authority: normative
---

# AID-2026-336 Pin Count and Exclusion Accounting

## 1. Counting definitions

This document distinguishes three different inventories. They must not be
combined or substituted for one another.

| Inventory | Count | Definition |
|---|---:|---|
| Manifest-visible declarations | 15 | The declaration inventory identified for the AID-336 scope assessment, before applying the in-scope/out-of-scope classification |
| AID-336 in-scope pins | 10 | The declarations governed by the AID-336 historical/current Git-blob pin semantics |
| Explicitly out-of-scope declarations | 5 | The declarations in the two explicitly excluded families |
| Prompt metadata entries | 150 | Prompt-related metadata entries excluded from the AID-336 in-scope pin inventory |

The first three values reconcile as:

```text
15 manifest-visible declarations
= 10 AID-336 in-scope pins
+ 5 explicitly out-of-scope declarations
```

The 150 prompt metadata entries are a separate metadata inventory. They are
not additional AID-336 in-scope pins and are not added to the 15 declaration
inventory.

## 2. AID-336 in-scope pin families

The 10 AID-336 in-scope pins comprise:

- top-level index and mirror declarations;
- authored-index declarations;
- related-evidence declarations;
- the execution-evidence file/blob declaration.

The exact path and reference mode determine how each declaration is verified:

- `authored_indexes[]` is historical;
- `related_evidence[]` must explicitly declare `historical` or `current`;
- current references are checked against the candidate commit tree;
- historical references are checked against reachable Git history at the exact
  declared path.

A missing or invalid related-evidence mode is a policy violation. It is not
silently defaulted to either mode.

## 3. `blob_sha256` declarations

Non-empty `blob_sha256` and qualified `*_blob_sha256` declarations are also
in-scope pins under the checker contract.

They are SHA-256 claims over committed file bytes, not Git blob object IDs.
The checker discovers them at arbitrary nesting depth, records their JSON
Pointer and field, and attempts to bind each declaration to a path in its own
containing mapping.

Their outcomes are accounted for separately:

- a matching bound declaration increments `ok`;
- a digest mismatch increments `mismatch`;
- a missing bound path increments `path_missing`;
- a declaration with no bindable path increments `unbound` and emits
  `UNBOUND_BLOB_SHA256`;
- malformed declarations or unreadable Git data increment `incomplete`.

Every non-empty `blob_sha256` declaration increments `pins`.

At the implementation commit, the measured checker result included two
successfully bound `blob_sha256` declarations:

```text
pins=12 ok=12 mismatch=0 path_missing=0 incomplete=0 excluded=163 unbound=0
```

Those two declarations are additional to the 10 AID-336 in-scope
historical/current Git-blob pins.

## 4. Explicit exclusions

The following families remain explicitly outside the AID-336 pin count:

- `gate_a_reconstruction`
- `d_source_blobs`

The four legacy prompt metadata key names and their related prompt snapshot
metadata are not promoted into the AID-336 candidate-tree blob-pin contract.
Session Evidence check 11 remains the authoritative prompt snapshot
digest/byte-count enforcement mechanism.

The explicit out-of-scope declaration count in the scope inventory is 5.
The prompt metadata inventory contains 150 entries.

## 5. Why `excluded=163` is not `150 + 5`

The checker's runtime `excluded=` summary field is an implementation counter
over the exclusion handling performed while scanning the manifests. It is not
the same as either:

- the manually inventoried 150 prompt metadata entries; or
- the five declaration instances classified as out of scope in the
  AID-336 declaration inventory.

The checker runtime counter can include separately encountered exclusion
keys/items and counts them according to its own traversal and counting rules.
Therefore, the measured runtime value:

```text
excluded=163
```

must be recorded as a checker execution metric, not used to overwrite the
declaration inventory values above.

No arithmetic reconciliation between `163`, `150`, and `5` is asserted here.
They have different definitions and counting domains.

## 6. Fixed negative fixture

The fixed negative fixture at commit
`9a2063ae1fa5d905b3817cd4eddba065a06daa73` produced:

```text
main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 manifests=108 pins=14 ok=7 mismatch=1 path_missing=0 incomplete=0 excluded=146 unbound=4
```

The assertion reported:

```text
NEGATIVE_ASSERTION_PASS
```

Its findings included four unbound SHA-256 declarations and one missing/invalid
related-evidence mode policy violation.

This fixture result is a separate runtime measurement. Its `pins=14` and
`excluded=146` values must not be substituted for the implementation-commit
scope inventory.

## 7. Implementation-commit count

At implementation commit `d8512eee5`, the checker reported:

```text
main=d8512eee59e8bfdfec5e280e4a3a01fc62c61074 manifests=161 pins=12 ok=12 mismatch=0 path_missing=0 incomplete=0 excluded=163 unbound=0
```

The measured `pins=12` is:

```text
10 AID-336 historical/current Git-blob pins
+ 2 bound blob_sha256 pins
= 12 runtime pins
```

The `excluded=163` value is retained as the runtime checker counter and is not
a replacement for the separate declaration and prompt metadata inventories.

## 8. Counting rule

For AID-336 reporting:

1. Use **10** for the AID-336 in-scope historical/current Git-blob declaration
   inventory.
2. Use **5** for the explicitly out-of-scope declaration inventory.
3. Use **150** for the prompt metadata inventory.
4. Use **12** for the implementation-commit runtime `pins=` result, which
   includes the 10 AID-336 pins plus two bound `blob_sha256` declarations.
5. Use **163** only when quoting the implementation-commit runtime
   `excluded=` result.
6. Do not add these numbers together or describe them as one common total.
