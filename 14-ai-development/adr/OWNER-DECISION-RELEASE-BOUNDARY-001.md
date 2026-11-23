---
document_metadata:
  domain: ai-development
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Owner D acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open."
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "0f2e0ef7977269e0d84d682b5b5a1aee8036cc02d4b70263b15468249c9e5d73"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/adr/OWNER-DECISION-RELEASE-BOUNDARY-001.md — the DECIDED line in this document names the decider and the date"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure in §2 and §3 was measured at main e622dfd3 in this session: the add() signature and its validate() call were read from crates/memory-domain/src/provenance_graph.rs; the publish/license fields were read from all twelve crates/*/Cargo.toml; tag absence was checked with git tag and git ls-remote --tags; the pre-change signature was read at both 6418e9c and 65fa040f^; the PR #707 figures come from the GitHub API."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: there is no release boundary in this repository, therefore the ProvenanceGraph::add signature change is not a public API break; no compatibility layer is owed; and the release boundary must be declared in exactly one place before any artifact is published."
    canonical_scope_id: ai-development/release-boundary
    canonical_scope_keywords:
      - release-boundary
      - public-api
      - semver
      - provenance-graph
      - publish-false
    canonical_conflict_status: None
    normative_status: Normative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# OWNER-DECISION-RELEASE-BOUNDARY-001 — the three questions in register 028, answered against a boundary that does not exist

**Status:** DECIDED (owner-proxy decision, 2026-11-23)
**Decided by:** Owner D acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open. Same mechanism as `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, `D-OWNER-DECISION-CANONICAL-COMMIT-001`, `OWNER-DECISION-BMCP-MCP-DISPATCH-001` and `OWNER-DECISION-TYPED-OBJECT-REF-001`.
**Answers:** all three questions in `GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028` §5, and therefore its stated closure condition.
**Does not absorb:** the question of how the change entered `main`. That belongs to `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` and `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008`, which already own it. §6 explains why this document refuses to mint a new number for it.

---

## 1. The questions, as the register states them

`GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028` §5 asks:

> 1. 该破坏性 API 变更是否在当前发布边界内获得授权。
> 2. 是否需要兼容层或弃用过渡期。
> 3. 变更须附带何种迁移通告。

and §1 makes its own closure condition: "Owner 对兼容性策略作出裁定，且迁移通告与发布边界已确定".

The register is careful and it is right to refuse the easy answer. §4 says:

> 仓库内编译与测试只证明**仓库内**调用点已迁移，不证明下游兼容性。

That sentence is correct, and it is the reason this document exists rather than a one-line "fine, ship it". But the register leaves one premise unmeasured: it assumes there is a downstream. Question 1 asks whether the change is authorized *within the current release boundary*, and never establishes that a release boundary exists. It does not.

## 2. There is no release boundary in this repository

Measured at `main = e622dfd3`, all values read from the tree, not from any policy document:

| evidence | measurement |
|---|---|
| crates declaring `publish = false` | **11 of 12** |
| crates declaring `license` | 11 of 12, all `"UNLICENSED"` |
| crate with neither `publish` nor `license` | `crates/bmcp-server/Cargo.toml` |
| version of every crate | `0.1.0`, unchanged since `2bedbcf8` (2026-11-18), the commit that created the workspace |
| `publish = false` introduced | `2bedbcf8`, same commit — the crates were never publishable, not even on day one |
| git tags, local | `git tag` → 0 |
| git tags, remote | `git ls-remote --tags` → none |
| CHANGELOG | absent |
| version-bearing intra-workspace dependencies | **0** — every dependency on a sibling crate is `path = "…"` with no version |
| `cargo publish` reachability | blocked for all twelve: a path dependency without a version is rejected, and eleven of the twelve dependencies are themselves `publish = false` |

So the artifacts that would carry a public API have never existed, cannot currently be produced, and are not declared to be producible. A "downstream consumer" is not merely unproven; there is no mechanism by which one could have obtained this code except by cloning the repository.

This is the fact that decides all three questions, and it inverts the register's framing: register 028 classifies itself as `PUBLIC_API_BREAKING_CHANGE` with severity `DOWNSTREAM COMPILE BREAK`. Both labels presuppose a published surface. Neither is reachable.

## 3. The change itself, measured

`crates/memory-domain/src/provenance_graph.rs:42` at `main`:

```rust
pub fn add(&mut self, provenance: Provenance) -> Result<(), DomainError> {
    provenance.validate()?;
```

The two-parameter form is present at `6418e9c` and at `65fa040f^`, so the register's §2 "before" sample is accurate. The change is real, the signature is genuinely narrower, and the reason recorded in the function documentation — that a second `parents` argument lets a caller declare one lineage on the record and another on the graph — is a correct reason.

Blast radius inside the repository, measured by search:

| location | references `ProvenanceGraph` |
|---|---|
| `crates/memory-domain/src/provenance_graph.rs` | yes |
| `crates/memory-domain/tests/phase2_acceptance.rs` | yes |
| the other ten crates | **none**, although nine of them depend on `memory-domain` |

At `65fa040f` the in-repo call sites were migrated in the same commit, and the commit message documents the change at length, including the removal reason and the mutation test that keeps the rule from regressing.

## 4. Decisions

### D1 — `ProvenanceGraph::add` is not a public API, and the register's category and severity are wrong

Not because a policy says so, but because no artifact carrying it has ever been published or can be. The category `PUBLIC_API_BREAKING_CHANGE` and the severity `DOWNSTREAM COMPILE BREAK` describe a consumer population that cannot exist.

The correct classification is **in-repo signature change**. The register must be corrected on both fields; §7 records the erratum rather than silently rewriting them.

Consequence: question 1 ("是否在当前发布边界内获得授权") has a determinate answer, and it is not "yes". It is that **the question has no subject yet**. Nothing is authorized by this ruling; what this ruling establishes is that no authorization was required, because the obligation it would discharge has not started.

### D2 — No compatibility layer, no deprecation period

Question 2's answer is NO, and the reason is stronger than "there are no callers".

A deprecation shim exists to keep existing callers compiling while they migrate. Here there are zero external callers, and the two in-repo call sites migrated in the same commit that made the change. A `#[deprecated] add_with_parents(provenance, parents)` would consequently be a public surface with no user — and worse, it would **restore the exact defect the change removed**: a second, caller-supplied lineage source that can disagree with the record's own `parent_provenance_refs`. The register's §3 states this conflict as the motivation for the change. Adding a shim reintroduces it under a new name.

A compatibility layer whose only effect is to reintroduce the bug it was written to retire is not a compatibility layer. It is the bug, annotated.

There is also no evidence that the repository has ever carried a deprecated alias — `git grep deprecated -- '*.rs'` returns nothing — so there is no local convention that would create a countervailing expectation.

### D3 — No external migration notice; the notice owed is internal and already exists

Question 3's answer, for an external audience, is: none, because there is no external audience.

An internal notice is owed, and it is already discharged twice: the function's doc comment states the new contract and why the old one was wrong, and `65fa040f`'s commit message states the change, the reason, and the mutation test that holds it. A third document restating both would be a third copy to drift.

The obligation that remains is not a notice but a **precondition**, and it is the one thing here that is not yet satisfied: before any artifact is published — the first time a `version` appears on an intra-workspace dependency, or a `publish` field is removed, or a tag is cut — the release boundary must be declared in one place, and the `add` change must appear in that declaration's compatibility statement. Publishing first and writing the boundary afterwards would make this ruling retroactively false without changing a word of it.

### D4 — The release boundary must be declared in exactly one place, and `bmcp-server` must stop diverging from its eleven siblings

The measurement in §2 has one outlier: `crates/bmcp-server/Cargo.toml` declares neither `publish` nor `license`, while the other eleven declare both. Absence of `publish` is not a value meaning "no" — Cargo's default is publishable. Today `bmcp-server` still cannot publish, because its only sibling dependency is a versionless path dependency; but that is an accident of the dependency graph, not a declaration. The day that dependency gains a version, `bmcp-server` becomes publishable by default while every other crate stays blocked, and nobody will have decided that.

Ruling: `bmcp-server` must declare `publish = false` and a `license` matching its siblings. This is a one-line correction with no behavioural effect today, and it is the only action item this ruling creates.

Ruling: the release boundary, when first declared, is declared in one document that names (a) which crates are publishable, (b) what the version policy is, and (c) what compatibility promise attaches at 0.x. It must not be assembled from the twelve `Cargo.toml` files plus inference, which is what §2 had to do.

## 5. What this ruling does not do

It does not close register 027. `ProvenanceGraph::add` now calls `provenance.validate()?`, and 027 records that `validate()` does not revalidate the four reference fields element by element. D3 here changes nothing about that: the graph's integrity still depends on a `validate()` that a deserialized `Provenance` can bypass. That gap remains OPEN and NOT AUTHORIZED, and this document does not speak to it.

It does not authorize future signature changes. Every subsequent change gets the same question asked again, and the answer will change the moment a release boundary exists.

## 6. The question this ruling refuses to absorb

Register 028 records the change as arriving through PR #707. Measured:

| field | value |
|---|---|
| PR title | `feat(bmcp): route Storage.PreparedParticipantReceipt through its structural parser` |
| additions / deletions / files | 3671 / 67 / 16 |
| reviews | **0** |
| what the PR actually contains | a `bmcp` parser route, **and** an `Evidence` field-set change, **and** the deletion of the MC-03 `EvidenceRecord`/`ProvenanceRecord` registry, **and** the `ProvenanceGraph::add` breaking change |

A breaking domain-model signature change, an Evidence contract change and a registry deletion travelled into `main` under a title that mentions none of them, with no review. That is a real finding and it is more serious than the compatibility question this register was opened for.

It is also not a new finding. `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` and `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` already own "merged without review", and `GAP-27-THE-BACKLOG-IS-NOT-ONE-BACKLOG` records what happens when the same defect is re-registered under a new number each time it recurs. Minting `029` here would add a fourth description of one mechanism and make the backlog harder to close, not easier.

Ruling: this document records the PR #707 measurement as evidence, and does **not** open a new register for it. The evidence belongs to 003 and 008.

## 7. Errata to register 028, recorded rather than silently applied

Two statements in 028 do not survive measurement. They are listed here so the register's original text stays readable as a record of what was believed at the time.

**§2 "变更后（PR #707，提交 `bbd214f`）".** `bbd214f` is PR #707's head commit and it touches exactly eight markdown files — zero `.rs`. The signature change is `65fa040f` (`fix(domain): enforce provenance lineage, split Evidence scope, migrate MC-03`, 2026-11-22 13:36:00 +0800), which is an ancestor of `bbd214f` inside the same PR. Citing the PR head as "the commit" makes the change look like documentation work.

**§2 "变更前（基线 6418e9c）".** The signature at `6418e9c` is indeed the two-parameter form, so the sample is valid. But `6418e9c` is dated 2026-11-22 18:35 — *after* `65fa040f` at 13:36 — because it landed on `main` from a branch that had not yet seen PR #707. Calling it the baseline invites the reading that the change postdates it. The correct statement is: the two-parameter form is present at `65fa040f^`, and `6418e9c` is an independent later observation of the same pre-change state on the other lineage.

Neither erratum changes the change itself, and neither changes any answer in §4. They change what the register's citations prove.

## 8. What the register should now say

`GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028` §1 closure condition — "Owner 对兼容性策略作出裁定，且迁移通告与发布边界已确定" — is satisfied by §4 D1–D3: the compatibility position is ruled (none owed, and why), the notice is determined (internal, already discharged), and the release boundary is determined (none exists, and the evidence that none exists is enumerated).

The register may therefore move to CLOSED-BY-RULING, with the §7 errata attached, and with one residue that is not compatibility and must not be closed with it: `bmcp-server`'s `publish`/`license` divergence, D4 above.
