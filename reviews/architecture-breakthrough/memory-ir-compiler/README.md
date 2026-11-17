# MB-IR-001 — Memory IR & Compiler Research

**Disposition: RECOMMEND SHADOW IR / NOT READY FOR FORMAL ARCHITECTURE ADOPTION**

This is an isolated research package. It does not change the main branch, B Owner domain authority, E production pipeline, or any canonical schema.

## Deliverables

- [Current formation pipeline analysis](current-formation-pipeline-analysis.md)
- [Memory IR domain model](memory-ir-domain-model.md)
- [Compiler architecture proposal](compiler-architecture-proposal.md)
- [IR versioning and provenance](ir-versioning-and-provenance.md)
- [Direct vs IR prototype analysis](direct-vs-ir-prototype.md)
- [Mature technology comparison](mature-technology-comparison.md)
- [Migration and risk analysis](migration-and-risk-analysis.md)
- [中文研究报告](memory-ir-compiler-zh-CN.md)
- [English research report](memory-ir-compiler-en.md)
- [Runnable prototype and synthetic data](prototype/README.md)

## Reproduction

```bash
python3 reviews/architecture-breakthrough/memory-ir-compiler/prototype/memory_ir_prototype.py
```

Python 3.10+, standard library only.

## Baseline and authority

- Main baseline read: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- B Overview pin referenced in Issue #43: branch `session-b-domain-model-phase3`, Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`
- B Fact/Claim ADR: ADR-BLOCKED per Issue #43 and bilingual B guide
- E compiler guide: stage topology CANDIDATE; resource/performance TO_VALIDATE
- Full detailed E Owner contracts/tests: not exhaustively read in this pass

## Explicit non-claims

No production benchmark, truth guarantee, entity-resolution proof, incremental persistence proof, crash/recovery proof, Forget/authorization conformance, canonical commit conformance, Owner approval, schema freeze, implementation authorization, merge or deployment is claimed.
