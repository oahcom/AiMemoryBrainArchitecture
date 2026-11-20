# REQ-06 pilot evaluation v1

**Status:** reproducible local pilot; not acceptance of the integrated product Brain.

## Question and scope

This experiment asks whether a small, provenance-backed corpus can distinguish useful retrieval from irrelevant and policy-ineligible activation. It is deliberately limited to repository-grounded factual tasks. It does **not** claim representative user behavior or full product value.

## Corpus provenance and coverage

corpus.jsonl contains 8 source records excerpted from repository documents at baseline main@bc114263d700692d32b20a099f3db9be9338d490; every record pins the source path and Git blob SHA. Two additional synthetic adversarial controls model a forgotten record and a record from another project scope. They are marked synthetic_control, have no repository provenance, and must never be treated as evidence about the product.

Seven fixed tasks are hand-authored from the source material: long-horizon continuity, factual recall (three tasks), planning/routing, correction/forget, and one negative abstention task. Preference-retention and multi-session handoff tasks are not represented. Labels are document-level relevance labels authored for this pilot, not user judgments.

## Arms

1. no_memory: return no context.
2. simple_lexical_top3: deterministic token overlap, top 3; no lifecycle or scope gate.
3. brain_policy_reference_proxy_NOT_INTEGRATED: same lexical candidate scorer after strict project-scope, active-lifecycle, documented-evidence and repository-blob filters. This is a **policy-shaped reference proxy**, not the integrated Brain path, not a runtime adapter, and not an implementation claim.

## Metrics

- Task success: positive tasks succeed when at least one labelled relevant document is returned; the negative task succeeds only when the arm abstains.
- Positive hit rate, mean document recall, mean precision, MRR.
- Harmful activation: selected forgotten or out-of-scope records. Irrelevant in-scope results are additionally exposed by precision and per-task selected IDs.
- Task-success uncertainty: 95% Wilson interval over 7 fixed tasks. This interval describes this tiny pilot only; it is not a population estimate.
- Median local Python function latency; not service or end-to-end latency.

## Reproduction

Python 3.10+; standard library only; no network or package installation.

    python evaluate.py
    python evaluate.py --json
    python -m unittest -v test_evaluate.py

pilot-results.json is the captured machine-readable output from the exact run included with this change. evaluate.py is deterministic apart from measured local latency. No random sampling is used (seed=not_applicable_deterministic_no_sampling).

## Pilot result (captured)

See pilot-results.json for per-task selected IDs and full metrics. Key result: no-memory positive hit rate 0%; simple lexical top-3 100% but selected 6 harmful records; policy proxy 100% with zero harmful records on this fixture. Both retrieval arms have mean precision 0.4444, showing that policy filtering removes harmful records but does not eliminate irrelevant in-scope retrieval. The 7-task Wilson interval for 7/7 success is [0.6457, 1.0], too wide for a superiority claim.

## Validity limits / non-claims

- No preference-retention or multi-session handoff task; corpus is small and repository-specific.
- No real user-task traces, human relevance adjudication, semantic embeddings, LLM, production tokenizer, inference, integrated Brain runtime, persistent storage, actual Adapter or Applied-context evidence.
- The proxy's scope/lifecycle/evidence checks are local fixture predicates, not authorization or Forget security certification.
- The synthetic controls are intentionally adversarial and affect simple retrieval's false activation count.
- Latency is local function timing only; not a production performance or cost result.
- No acceptance threshold is proposed or adopted here. This pilot supplies evidence and exposes the remaining gap; it does not authorize production activation.
