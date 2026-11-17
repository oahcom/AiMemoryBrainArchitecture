# Memory IR prototype

Requirements: Python 3.10+; standard library only.

Run from any working directory:

```bash
python3 reviews/architecture-breakthrough/memory-ir-compiler/prototype/memory_ir_prototype.py
```

The script reads `sample_experiences.json` next to itself and prints a deterministic JSON report. No network, database, model API, or third-party package is required.

This is a synthetic comparison, not production-quality evidence. The parser is a deterministic fixture, not an NLP extractor. Entity resolution, persistent incremental caches, schema migrations, canonical commit, authorization, Forget, and real workload benchmarks are out of scope. Conflict detection emits review proposals only; it never chooses a winner.
