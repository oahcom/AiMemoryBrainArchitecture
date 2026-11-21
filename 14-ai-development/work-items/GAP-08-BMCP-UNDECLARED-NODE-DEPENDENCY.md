# GAP-08 — BMCP conformance suite has an undeclared Node dependency

**Status:** Open — repository side done in #546; closure criteria 1 and 5 blocked by the CI billing interruption
**Area:** 08-bmcp-protocol / conformance
**Owner track:** Owner H (Protocol)

## Gap statement

Three `.mjs` cross-language reference implementations import the third-party
npm package `canonicalize`. The repository contains **no `package.json`, no
`package-lock.json`, no `pnpm-lock.yaml` and no `yarn.lock`**, so the dependency
is never installed and the tests that shell out to those files fail on any
clean checkout.

This is not a cryptography defect. Once the package is installed, all affected
tests pass unchanged.

## Evidence (verified on `main @ f057328d`)

**1. The imports exist.**

```sh
grep -rn "canonicalize" --include=*.mjs 08-bmcp-protocol/
```

```
tests/conformance/provider_outcome/c_crypto_profile_h_reference.mjs:2: import canonicalize from "canonicalize";
tests/conformance/provider_outcome/c_crypto_profile_h_reference_1_0_1.mjs:2: import canonicalize from "canonicalize";
tests/conformance/recovery_cutoff/i_crypto_profile_reference.mjs:2: import canonicalize from "canonicalize";
```

**2. No manifest declares it.**

```sh
find . -name "package.json" -o -name "package-lock.json" \
       -o -name "pnpm-lock.yaml" -o -name "yarn.lock" | grep -v node_modules
```

Zero results.

A Python dependency manifest does exist —
`08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt` — and it
declares `jsonschema`, `rfc8785` and `cryptography`. It cannot express the Node
dependency, and nothing else does.

**2b. The tests that need it are outside CI coverage.**

`.github/workflows/h-applied-delivery-evidence-conformance.yml` runs:

```
python -m unittest discover -s .../applied_delivery_evidence -p 'test_*.py' -v
python -m unittest discover -s .../recovery_cutoff -p 'test_recovery_join*.py' -v
```

The three files that require `canonicalize` are
`provider_outcome/test_c_crypto_profile_interop.py`,
`provider_outcome/test_c_crypto_profile_1_0_1_interop.py` and
`recovery_cutoff/test_i_crypto_profile.py`. None of them match either discover
pattern. So the failure cannot appear in CI, which is why an undeclared
dependency reached `main` unnoticed.

**3. The suite fails on a clean tree.**

```
FAILED provider_outcome/test_c_crypto_profile_1_0_1_interop.py::...test_CI03_h_node_and_python_independent_implementations_match_expected
FAILED provider_outcome/test_c_crypto_profile_interop.py::...test_CI03_h_node_and_python_independent_implementations_match_expected
FAILED recovery_cutoff/test_i_crypto_profile.py::...test_CRYPTO_01_all_i_p0_families_match_node_rfc8785_and_ed25519

3 failed, 555 passed, 27 skipped, 1 error
```

The underlying Node error is unambiguous:

```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'canonicalize'
```

**4. Installing the package fixes them.**

After `npm install canonicalize`, the three affected files pass:

```
13 passed in 0.73s
```

## A second, separate issue: wrong test runner

`recovery_cutoff/test_hrc_semantics.py` reports `ERROR ... fixture 'value' not
found` under pytest. This is not a defect in the file: it defines a plain
helper named `test_digest(value, domain=...)`, which pytest collects as a test
and then cannot resolve a fixture for.

Its own module docstring specifies the runner:

```
Run:
    python -m unittest -v test_hrc_semantics.py
```

Under the documented runner it is clean:

```
Ran 44 tests in 0.008s
OK
```

So the suite has two invocation contracts — pytest for most files, unittest for
this one — and nothing declares which applies. Running the whole directory under
either single runner produces a spurious failure.

## Candidate directions

### (a) Add a `package.json` pinning `canonicalize`

Smallest change that makes the dependency real and reproducible. The reference
implementations stay third-party, which is the point of a cross-language
independent check: they must not reuse the Rust implementation's own
canonicalization.

### (b) Vendor a self-contained RFC 8785 implementation

Removes the dependency but weakens the independence claim if the vendored code
is derived from the Rust side. Only worth it if the project wants zero npm
dependencies.

### (c) Drop the Node cross-language tests

Loses the only independent check that the Rust canonicalization matches another
implementation. Not recommended: RFC 8785 divergence is exactly the class of
bug that only a second implementation catches.

## Recommendation

**(a).** Add a `package.json` next to the conformance tests pinning
`canonicalize` to an exact version, plus a lockfile. Also add a marker so the
mixed-runner issue is explicit: either rename `test_digest` to `digest` (it is
a helper, not a test) or add a `pytest.ini`/`conftest.py` that excludes it.
Renaming is one line and needs no configuration.

The project should state in `protocol-index.md` which runner each directory
expects, so "run the conformance suite" has one meaning.

## Closure criteria

1. A clean checkout with no pre-installed `node_modules` passes the full
   conformance suite without manual `npm install`.
2. The Node dependency is pinned and its lockfile committed.
3. `test_hrc_semantics.py` either runs cleanly under pytest or the runner
   contract is documented per directory.
4. The suite's pass count is reported with the runner and dependency state
   attached, so a future measurement does not repeat the 3-failure result as if
   it were a code defect.
5. CI actually executes the three files that depend on Node. A dependency that
   no workflow ever installs is indistinguishable from one that is missing.

## Status after #546

The repository side is complete: the dependency is pinned with a committed
lockfile, the helper no longer collides with pytest collection, and the workflow
now executes all four previously uncovered files.

Criteria 2, 3 and 4 are met, and each was measured locally rather than inferred;
the measurements are attached to the PR body. Criterion 1 requires an automatic
install on a clean checkout, and criterion 5 requires CI to execute the three
Node-dependent files. Both are blocked by the same billing interruption, which is
outside this work item.

This item stays open until those two are measured.
