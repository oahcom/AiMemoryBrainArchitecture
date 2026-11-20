# REQ-06 integrated Brain runtime availability — Issue #374

**Disposition: BLOCKED — no integrated product runtime is present in this repository.**

## Repository evidence

The current `main/README.md` identifies this repository as architecture specifications and system-contract design, and explicitly states:

- Product-level runtime: **Not started**.
- The repository contains limited reference models, validators, and conformance tests, but no integrated product runtime.
- Performance and production validation have not been established through a running implementation and representative workloads.

This is the authoritative project-status statement in the repository at the time this record was prepared. The REQ-06 pilot threshold decision also explicitly identifies the third arm as `brain_policy_reference_proxy_NOT_INTEGRATED`, not an integrated Brain result.

## Exact missing integration surface

There is no product Brain runtime module in this repository to import or invoke, and no implemented callable task-execution API that exposes the integrated path. In particular, no real runtime API is available here to provide all of:

1. task input admission and trace identity;
2. canonical retrieval and retrieval evidence;
3. context compilation and versioned context output;
4. product adapter invocation and adapter/application evidence at the inference boundary;
5. task outcome and correlated end-to-end trace.

The missing dependency is therefore not a missing test fixture or a missing policy predicate: it is the **product-level Brain runtime plus its callable task-execution interface and integrated adapter/application boundary**. The repository does not declare a concrete module path or API symbol for these because product runtime implementation has not started. Inventing a module name or API signature would fabricate an integration contract.

## Fail-closed disposition

Do not create or label a policy proxy, reference model, fixture predicate, or synthetic adapter as the integrated Brain arm. Without the real runtime and adapter boundary, AC-1 cannot be truthfully implemented; AC-2 cannot run a three-arm controlled comparison; AC-4/AC-5 cannot report integrated-arm regression or cost evidence.

The provisional gates in `reviews/req06-evaluation-pilot/threshold-decision.md` remain development-baseline thresholds only. They are not production SLOs. R3 human expert review and production activation remain OUT-OF-SCOPE(dev-baseline).

## Required input to unblock

The accountable product-runtime implementer must publish or identify the actual runtime repository and exact branch/commit, then provide the callable integrated task API and adapter/application evidence contract (including how task, retrieval, context, inference-boundary application, and outcome IDs correlate). Once those exist, this harness can bind to that API without substituting a proxy.

## Local execution

**NOT_EXECUTED** in this delivery environment: Python data analysis is currently unavailable. No test or harness execution is claimed. After the runtime/API is supplied, run the repository's documented REQ-06 command from a checkout and record its actual exit code and output; no expected PASS is asserted here.

## Scope statement

This record documents the concrete runtime dependency and prevents false integrated-arm claims. It is not an implementation of the integrated evaluation harness and does not claim AC-1 through AC-5 are satisfied.
