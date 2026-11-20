# REQ-06 integrated evaluation harness — availability gate

Status: **PARTIAL / BLOCKED at the integrated-runtime boundary**. This carrier does not claim an integrated Brain arm.

## Repository evidence

- The repository root README states: "Product-level runtime | Not started" and says the repository contains limited reference models, validators, and conformance tests, but no integrated product runtime.
- PR #360 supplies no-memory, simple lexical retrieval, and `brain_policy_reference_proxy_NOT_INTEGRATED`; its own merged description explicitly says the third arm is not integrated.
- The provisional threshold decision is `REQ06-THRESHOLD-2026-11-20-01` at `reviews/req06-evaluation-pilot/threshold-decision.md` (blob `a01ee75ff0ffc2d3c00a33197630d24ca2aaffe4`). It is a development-baseline gate, not a production SLO.

## Missing integration boundary

No product-runtime module or callable task-execution API is present in the repository baseline. The required boundary is an actual runtime entry point that accepts a task and returns retrieval/context evidence, plus the actual Agent Adapter application/acknowledgement evidence. The names `BrainRuntime.execute_task` and `AgentAdapter.apply_context` below describe the required capabilities, **not existing repository symbols or an invented implementation**.

This harness deliberately does not import the policy proxy as a Brain runtime. It fails closed until an owner supplies the real module and callable contract. No module name is guessed.

## Run

Python 3.10+, standard library only:

```sh
python reviews/req06-integrated-harness/runtime_probe.py
python -m unittest -v reviews/req06-integrated-harness/test_runtime_probe.py
```

Expected default result: `BLOCKED: integrated Brain runtime entrypoint is not configured` and exit 2. This is an availability result, not an evaluation pass.

## Remaining work (narrow follow-up)

Provide the actual integrated runtime module/API and adapter application evidence contract. Then extend the existing frozen pilot corpus with preference-retention and multi-session-handoff tasks, execute all three arms against the same corpus, and add the executable threshold gate plus per-task traces, uncertainty, harmful activation and measured efficiency/cost output. Keep all thresholds labelled development-baseline until separately authorized.

## Scope exclusions

R3 human expert review and production activation remain OUT-OF-SCOPE(dev-baseline). No Vector DB, Graph DB, RL, multimodal expansion, production SLO, or real-user benefit is claimed.
