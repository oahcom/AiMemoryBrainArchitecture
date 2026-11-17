# D — Current-main Dependency and Critical Path Reassessment (Delta)
- Assessment: DEP-DAG-001-D1
- Baseline: `main@ca69d50d1fc6c19a930128de700b0f2328bf32fb`
- Parent: PR #46 F/D/P report Blob `081610b1734ec08dc7c35c75fae1cae3ca713be4`.
- Delta evidence: B parity audit Blob `a877ceff906da01e70e277a81b95978982af3ede`.

## Dependency delta
Add a documentation-evidence dependency, not a runtime dependency:

`B research translation remediation → independent clause/row parity review → B Owner decision/ADR status confirmation → exact downstream consumer pin/adoption → A G2/G6 re-evaluation`.

The audit lists PARTIAL and PROVISIONAL files as well as files marked translated but awaiting manual parity review. Do not treat the latter as complete. The dependency is scoped to any decision that relies on those B research artifacts; unrelated Owner work and bounded synthetic spikes may proceed in parallel.

## Critical path impact
The current-main delta does not alter the physical critical path for Storage/COC/JF-10, D/E/I Forget/publication, or C/G/H Applied. It adds a governance/documentation branch that must converge before B research can be used as normative evidence and before the corresponding B-dependent G2/G6 claims can close.

Hard dependency: independent semantic parity review before normative reliance on affected B research artifacts.
Soft/parallel dependency: translation automation and link/ID/status lint can run while unrelated technical evidence is collected.
Ordering constraint: B Owner's semantic decision follows verified evidence; translation does not itself decide Fact/Claim.
Evidence dependency: exact branch HEAD + Blob readback for every remediated file.

## Required DAG record
- Upstream: B source remediation and current source pins.
- Intermediate: independent bilingual parity review and status/ID/link audit.
- Downstream: B Owner ADR/decision, consumer adoption, A G2/G6.
- Accountable: B for source; independent reviewer for parity; each consumer Owner for adoption; A for integration gate tracking.
- Exit evidence: per-file parity result, exact Blob SHA, unresolved-row register, Owner decision, consumer acceptance.

## Disposition
No change to existing technical dependency graph or physical Gate A→B→C sequence. Add this documentation-evidence path to the verification DAG. Do not promote it to a universal blocker for unrelated preparation or use it to bypass Owner authority.
