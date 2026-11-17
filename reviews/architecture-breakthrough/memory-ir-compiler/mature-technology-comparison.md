# Mature Technology Comparison

- Status: RESEARCH; technology choices are candidates, not project decisions.
- Core recommendation: reuse mature serialization/validation libraries; own only the thin memory-specific IR semantics and pass contracts.

## 1. Options

| Technology | Reusable capability | Fit | Gap / caution |
|---|---|---|---|
| LLVM IR | Typed low-level SSA, verifier, optimization pipeline | Inspiration for explicit typed values and verification | Wrong abstraction level; memory semantics are epistemic, temporal, scoped, evidence-bearing and side-effect/governance aware |
| MLIR | Extensible dialects/types/ops, traits/interfaces, passes, multi-level lowering, diagnostics and bytecode version hooks | Best conceptual model for layered IR and pass boundaries | Heavy C++ compiler infrastructure; do not embed MLIR runtime merely to store memory assertions |
| Rust compiler (rustc) | Query-based dependency graph, incremental recomputation, diagnostics | Inspiration for dependency-keyed invalidation and query caching | Not a reusable memory compiler library; implementation patterns only |
| TypeScript Compiler API | Parser/AST/type checker/transformer pipeline | Useful front-end analogy and inspectable AST | Language-specific, not a general memory semantic runtime |
| SQL AST / query planner | Parse tree, logical plan, rewrite, physical plan | Good analogy for separating user expression, logical semantics, and execution | Query plans optimize result execution, not truth/evidence; don't use SQL AST as domain model |
| JSON Schema | Interoperable structural validation, schema IDs and vocabularies | Good envelope/payload validation boundary | Weak for cross-node graph invariants, temporal conflict semantics and provenance DAG constraints |
| Protocol Buffers | Compact typed messages, generated code, field numbers and wire compatibility | Strong candidate for stable internal message transport if Rust services require it | Unknown-field/oneof/evolution discipline needed; schema does not define truth or pass semantics |
| Apache Avro | Writer/reader schema resolution and schema evolution | Useful for stored event/IR envelopes in data pipelines | Additional registry/runtime operations; not necessary for an early single-repo prototype |
| Pydantic / Serde | Runtime validation (Pydantic) and typed serialization/deserialization (Serde) | Strong implementation tools for Python/Rust boundaries | Validation library is not the IR architecture; avoid coupling semantic rules to one language |
| Database migration tools | Ordered, versioned physical schema changes | Needed for physical store evolution | Does not version historical IR semantics or transform retained IR documents by itself |

## 2. Suggested adoption

- Define the IR semantic contract as a small language-neutral specification (JSON examples + explicit enums/invariants).
- For early experiments, JSON Schema validates each envelope and node payload; add custom semantic validators for graph and temporal rules.
- If the runtime implementation is Rust, use Serde for typed parsing/serialization. Consider Protobuf only if cross-process contract and wire stability justify generated schemas.
- Use explicit schema IDs and immutable raw/IR artifacts; introduce Avro only if event streaming or long-lived writer/reader compatibility is a real requirement.
- Use existing database migration tooling for physical tables, but keep IR schema migration separate.
- Borrow MLIR's dialect/pass concepts and rustc's dependency invalidation model; do not depend on LLVM/MLIR as an embedded runtime.

## 3. Build-vs-buy boundary

Buy/reuse:
- JSON Schema validator;
- Pydantic or Serde for typed decoding;
- standard UUID/digest/serialization libraries;
- database migration tooling;
- established workflow/retry engine where selected elsewhere.

Build narrowly:
- candidate node vocabulary;
- evidence/provenance graph contract;
- pass manifest and dependency keys;
- memory-specific semantic checks and conservative conflict proposals;
- D-owned commit projection adapter.

Do not build:
- a general-purpose optimizer framework;
- a new schema registry unless a real multi-service governance need exists;
- an alternative canonical domain model;
- a custom compiler language/parser unless JSON representation proves inadequate.

## 4. Primary references

- MLIR Language Reference: https://mlir.llvm.org/docs/LangRef/
- MLIR Pass Infrastructure: https://mlir.llvm.org/docs/PassManagement/
- LLVM Language Reference: https://llvm.org/docs/LangRef.html
- rustc development guide (query system): https://rustc-dev-guide.rust-lang.org/queries/incremental-compilation-in-detail.html
- TypeScript Compiler API: https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API
- JSON Schema: https://json-schema.org/learn/getting-started-step-by-step
- Protocol Buffers evolution: https://protobuf.dev/programming-guides/proto3/#updating
- Avro schema resolution: https://avro.apache.org/docs/current/specification/
- Pydantic: https://docs.pydantic.dev/latest/concepts/models/
- Serde: https://serde.rs/
- SQLGlot AST: https://sqlglot.com/sqlglot/expressions.html

References describe product capabilities; they do not constitute project adoption or compatibility proof.
