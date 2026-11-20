# REQ-06 Quality and Efficiency Threshold Decision v1

- Decision ID: `REQ06-THRESHOLD-2026-11-20-01`
- Requirement: Issue #346 (REQ-06)
- Decision scope: development-baseline evaluation gates for the REQ-06 pilot; **not** production acceptance or production activation.
- Authority: delegated decision session under the Owner delegation instrument recorded in Issue #305, comment `7042461592` (authority to judge, record, and close requirement acceptance). This is a session decision, not a claim that a separate human Owner signed it.
- Evidence baseline: PR #360 merge `0a3e05dc1022f753d0dd6b9eb5ff1470e8dbb730`; experiment `REQ06-PILOT-2026-11-20-v1`; corpus SHA-256 `741636f2e9b7354fa6f56c2707cedb96621bb96971a8e84b43238bea722dea70`.

## Decision

Adopt the following **provisional development-baseline thresholds** for subsequent controlled REQ-06 evaluations. They are minimum screening gates calibrated against the small pilot, not statistically validated population or production SLOs.

| Dimension | Threshold | Pilot observation | Decision / rationale |
|---|---:|---:|---|
| Overall task success | 95% Wilson lower bound ≥ 0.60 | policy proxy 7/7; Wilson95 `[0.6457, 1.0]`; no-memory 1/7 `[0.0257, 0.5131]` | Passes on this fixture. 0.60 is a conservative floor below the observed 0.6457 lower bound; the interval remains wide and cannot support a superiority claim. |
| Positive-task hit rate | ≥ 0.80 | policy proxy 1.00; no-memory 0.00 | Passes on 6 positive pilot tasks. The floor is a minimum usefulness screen, not a claim of representative coverage. |
| Mean document precision | ≥ 0.40 | policy proxy 0.4444; lexical 0.4444 | Passes narrowly. The observed 0.4444 also shows substantial irrelevant in-scope retrieval; this floor must not be read as high precision. |
| Harmful activation | exactly 0 forgotten or out-of-scope activations | policy proxy 0; lexical baseline 6 | Passes the two explicit synthetic adversarial controls. Any non-zero activation fails this gate regardless of aggregate quality. |
| Relative local retrieval latency | median ≤ 1.25× the simple-lexical arm, measured in the same run/harness | 0.0763 ms / 0.0838 ms = 0.9105× | Passes in this local Python fixture. The 1.25× ceiling is an explicit development budget allowing up to 25% policy-check overhead; the observed ratio is evidence that this fixture did not consume that budget, not proof of service latency. |
| Additional model calls for deterministic policy filtering | 0 | 0 in this harness | Passes for this deterministic harness only. Model/inference cost is unmeasured and no model-call budget is inferred for an integrated runtime. |

## Measurement and interpretation rules

1. Compare arms on the same frozen corpus, task set, environment, and run. Report raw counts as well as rates; never hide the denominator.
2. Calculate the 95% Wilson interval for task success. A point estimate alone cannot pass the overall task-success gate.
3. Count forgotten and out-of-scope activation separately and in aggregate. The permitted count is zero; synthetic controls are test sentinels, not representative user data.
4. Report median local retrieval latency and the lexical-baseline ratio. Do not translate this into API, end-to-end, model, or production latency.
5. Report tokens, model calls, compile cost, and human intervention when those measurements exist. **No numeric token, inference, compile, or human-intervention threshold is adopted here** because the pilot collected no such data.
6. A pass on this pilot fixture is only a development-baseline result. It cannot establish the integrated Brain arm, real-user benefit, representative corpus validity, independent human relevance labels, or production readiness.

## Explicit pilot disposition

The policy-shaped reference proxy meets the provisional numerical gates on this fixture: Wilson lower bound `0.6457`, positive hit `1.00`, precision `0.4444`, harmful activations `0`, and local latency ratio `0.9105×`. This is **not** an AC6 end-to-end Brain result: the third arm is explicitly `brain_policy_reference_proxy_NOT_INTEGRATED`. The 7-task interval `[0.6457, 1.0]` is wide; no statistical superiority claim is made.

## Limitations and re-opening conditions

- The corpus contains 8 repository-grounded records plus 2 synthetic controls; 7 hand-authored tasks; no preference-retention or multi-session handoff; no real-user traces or independent human relevance adjudication.
- The third arm is a policy proxy, not the integrated Brain runtime. Its local scope/lifecycle/evidence predicates are not a production authorization or Forget-security certification.
- Local latency is Python function timing over seven tasks. No production latency or monetary cost was measured.
- Revisit these thresholds when an integrated Brain task path, representative privacy-safe corpus, independently adjudicated labels, or larger multi-run dataset exists. Any threshold change must include the new raw measurements and rationale.

## Prompt provenance

Source prompt: user instruction in the current ChatGPT conversation requesting completion of REQ-06 AC5. The execution environment does not expose a stable conversation/session ID or a prompt file/version/hash. Those identifiers are recorded as `NOT_EXPOSED` / `NOT_AVAILABLE`, not fabricated.
