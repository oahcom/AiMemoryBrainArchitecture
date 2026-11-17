# Synthetic Prototype and Benchmarks

**Status:** exploratory synthetic experiment; not user behavior, production load or runtime conformance evidence.

## Experiment question

Does a shared resource allocator improve fairness under contention, and what quality/latency trade-off does it introduce versus simple retrieval and rerank+budget?

## Reproduction

- Python 3.11+; standard library only.
- Fixed random seed: 20261118.
- 30 independent tasks; 24 candidate memories per task (720 candidates).
- Four task-required candidates per task (120 total required).
- Candidate token cost uniformly sampled from 25–110.
- Global context token budget: 9,000; per-task cap: 650.
- 4% candidate permission-ineligible; 1.5% forgotten (generated independently).
- Relevant candidates receive high initial relevance; distractors overlap and may score high.
- Rerank score = 0.35 relevance + 0.20 authority + 0.15 freshness + 0.15 evidence + 0.15 task value.
- RM reserves an equal floor (global budget / 30) then round-robins by lowest normalized task allocation; each task has 650 cap.
- All methods apply the same hard eligibility filter before selection.

## Algorithms

1. **Direct Top-K:** take top 6 by relevance per task, then fill shared global budget by relevance.
2. **Retrieval + Reranking + Budget:** globally rank eligible candidates by rerank score / token cost and greedily fill the same global budget.
3. **Unified Resource Manager:** same eligible candidate/rerank set, but allocate a per-task reservation floor and distribute remaining budget fairly under per-task cap.

## Metrics

- Recall = selected required candidates / all 120 task-required candidates.
- Precision = required selected / all selected.
- Token efficiency = required-candidate tokens / all selected tokens.
- Redundancy = extra selections after the first candidate for each task-topic bucket / selected count.
- Task coverage = mean fraction of four required candidates selected per task.
- Starvation = tasks receiving zero selected candidates.
- Fairness = Jain index over per-task required-candidate coverage.
- Budget utilization = used tokens / 9,000.
- Latency = median of 100 local in-process runs; single-threaded Python microbenchmark, not service latency.

## Results

| Metric | Direct Top-K | Rerank + Budget | Unified RM |
|---|---:|---:|---:|
| Recall | 0.5333 | **0.5417** | 0.5083 |
| Precision | **0.4741** | 0.2863 | 0.2699 |
| Token efficiency | **0.4817** | 0.3064 | 0.2984 |
| Redundancy rate | **0.2815** | 0.4097 | 0.4071 |
| Mean task coverage | 0.5333 | **0.5417** | 0.5083 |
| Starved tasks | 1 | 0 | **0** |
| Jain fairness | 0.8325 | 0.8141 | **0.8554** |
| Budget utilization | 0.9997 | 0.9996 | 0.9973 |
| Median selection latency (ms) | **0.095** | 0.119 | 0.306 |

## Interpretation

- RM eliminated starvation and improved fairness in this workload, but did **not** improve recall, precision, token efficiency or redundancy.
- The fairness gain is purchased by reserving capacity for every task, including tasks whose candidates are lower value. That is an intentional service guarantee, not free efficiency.
- Direct Top-K had the best precision and token efficiency but starved one task and left some tasks less evenly covered.
- Rerank+Budget gave the best aggregate recall/task coverage, but the lowest Jain fairness.
- RM's measured latency was about 3.3x Direct Top-K in this tiny Python prototype. This is algorithm overhead, not a production performance estimate.
- The benchmark supports only a conditional conclusion: shared resource arbitration is useful when fairness is a product requirement; it does not prove a universal retrieval-quality improvement.

## Re-run command

Save the prototype as `prototype.py` and run:

```bash
python3 prototype.py
```

The harness should print the fixed seed, parameters, all nine metrics and medians across 100 runs. Any implementation change must preserve the exact seed/parameter manifest or publish a new experiment ID.

## Validity limitations

No natural-language embedding, actual index, model tokenizer, user preference labels, real task traces, multi-process contention, IO, CPU saturation, GPU, network, cache invalidation, Forget races or storage recovery are simulated. Scores are synthetic scalars. Latency excludes retrieval backend, authorization RPC, canonical revalidation, serialization and inference provider. Results must not be described as real user behavior or production capacity evidence.
