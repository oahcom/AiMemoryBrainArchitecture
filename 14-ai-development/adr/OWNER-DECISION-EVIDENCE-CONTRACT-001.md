---
document_metadata:
  domain: ai-development
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner (repository owner), converging under standing instruction (Issue #751)"
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "67793326476f5b3288f8388bba0ea9e1c1790a6de5d72e7c9fdc5bcde811df66"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Issue #751 comment 7097692424"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "The four contract types and EvidenceKind construction sites were measured at main 13c6d95d. Instant has 44 occurrences in 9 files across bmcp-server (28), memory-storage-sqlite (8), memory-domain (6) and memory-event-store-sqlite (2): 38 std::time::Instant and 6 TimeValue::Instant(String). Comparing 13c6d95d..1c47002 shows no changes in those four crates, so the count remains current at main 1c47002. The BMCP enum and Cargo dependency boundary were read directly; no construction site of the four removed EvidenceKind values exists outside tests."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026's two work packages are not the same kind of problem, the BMCP evidence module is not a consumer of the domain Evidence entity, and WP-A is blocked on three undefined contract types while WP-B is not blocked at all."
    canonical_scope_id: ai-development/evidence-contract-split
    canonical_scope_keywords:
      - evidence-contract
      - work-package-split
      - wp-a
      - wp-b
      - evidence-kind
      - contract-types
    canonical_conflict_status: None
    normative_status: Normative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# OWNER-DECISION-EVIDENCE-CONTRACT-001 — WP-A and WP-B are one register but two different problems, and only one of them is blocked

**Status:** DECIDED (owner-proxy decision, 2026-11-23)
**Decided by:** Owner D acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open. Same mechanism as `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, `D-OWNER-DECISION-CANONICAL-COMMIT-001`, `OWNER-DECISION-BMCP-MCP-DISPATCH-001`, `OWNER-DECISION-TYPED-OBJECT-REF-001` and `OWNER-DECISION-RELEASE-BOUNDARY-001`.
**Narrows:** `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026`. Its §2 states that neither work package can close the register alone. That stays true. What changes is that WP-B becomes authorizable now, and WP-A becomes blocked on a decision the register never named.
**Does not close:** the register. Conditions 9 and 10 of its §9 both remain unmet.

---

## 1. The register's own structure

`GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` §2 defines two work packages:

> **WP-A：Evidence Structure Conformance** — 13 个契约字段、`excerpt_ref` 缺失、身份重复、命名差异、类型差异、`TypedObjectRef`/`Instant`/`Locator`/`ContentRef` 的落实
>
> **WP-B：Evidence Enum Conformance** — `EvidenceKind` 值域、`EvidenceAvailability` 值域、Serde 表示、旧值迁移策略、所有构造点与协议映射

and concludes:

> 两个工作包必须分别通过测试。任何一个工作包完成都不能单独关闭本登记。

The register is right that the two must be verified separately. It treats them as two halves of one migration, which is why it also treats them as equally blocked: §3's prohibition list applies to "获得独立实施授权之前" as a whole.

That is the error. WP-A and WP-B fail for different reasons, at different depths, and one of them is not blocked at all.

## 2. WP-A is blocked on three types that do not exist

§8 of `02-domain-model/core-entities.md` types Evidence's fields with four names beyond the ones the implementation already has: `TypedObjectRef`, `Locator`, `ContentRef`, `Instant`.

Measured at `13c6d95d`, searching `crates/` for a definition of each; the Instant occurrence inventory was revalidated against current `main @ 1c47002` (the intervening commits changed none of the four affected crates):

| contract type | defined anywhere in `crates/`? | occurrences |
|---|---|---|
| `TypedObjectRef` | **no** | 0 |
| `Locator` | **no** | 0 |
| `ContentRef` | **no** | 0 |
| `Instant` | **no** | 44 across 9 files in 4 crates (38 `std::time::Instant`; 6 domain `TimeValue::Instant(String)`) — unrelated to the contract type |

`TypedObjectRef` has since been ruled — `OWNER-DECISION-TYPED-OBJECT-REF-001` freezes it at the §14 candidate shape. The other three have **no definition and no ruling**. The contract uses them, §8 depends on them for five of its thirteen fields, and nothing anywhere says what they are:

- `Instant` — §14 lists "timestamp precision" as an **OPEN** decision. Until it is decided, `Instant` cannot be typed, and `recorded_at` and `observed_at` cannot move off `String`.
- `Locator` — §8 gives five examples ("message span, page, JSON path, time range, environment tick") and no structure. Five examples are not a type.
- `ContentRef` — §14 does not mention it at all. It appears at two field sites and nowhere else.

So WP-A's checklist item "`recorded_at` 满足 Instant 契约" is not implementable as written. It reads like a migration step; it is actually a request to invent a type. Three of them.

This is the same defect class as `TypedObjectRef`, which was caught and ruled. These three were not caught, because the register lists them as hex items to "落实" rather than as undefined names to define.

**Ruling D1:** WP-A is BLOCKED on `Instant`, `Locator` and `ContentRef` being defined. No implementation work on WP-A may start, and no dispatch is owed, until those three definitions exist. Work that migrates `Evidence` to conform to §8 before they exist would have to guess their shapes, and a guessed shape frozen into thirteen fields is exactly the situation `OWNER-DECISION-TYPED-OBJECT-REF-001` was written to prevent.

## 3. WP-B is not blocked, and it is far smaller than its checklist implies

WP-B asks for `EvidenceKind` and `EvidenceAvailability` to match the contract, plus migration of every construction site, match arm, protocol mapping and test.

Measured blast radius at `13c6d95d`:

| item | measurement |
|---|---|
| `EvidenceKind` construction sites in the workspace | **1** — `EvidenceKind::Document` at `memory-domain/src/lib.rs:1700`, `memory-compiler/tests/evidence.rs:48` and `phase2_acceptance.rs:894` |
| `EvidenceKind::Message` constructed anywhere | **0** |
| `EvidenceKind::Record` constructed anywhere | **0** |
| `EvidenceKind::Dataset` constructed anywhere | **0** |
| `EvidenceKind::Other(..)` constructed anywhere | **0** |
| `EvidenceAvailability` match arms | **5** — one four-arm match in `memory-compiler/src/evidence.rs:142-155`, plus tests |
| persisted data to migrate | **0** — no `.db`/`.sqlite` files tracked, no `*.sql` migration files, no serialized fixtures |

The four non-contract `EvidenceKind` values have **zero construction sites**. They exist only as enum variants. The register's §7 instruction "不进行没有证据支持的自动值域映射" is therefore nearly moot for them: there is nothing to map, because nothing produces them. Removing them is not a migration; it is deleting unused variants, and adding the five missing contract values is adding unused variants. Neither touches behaviour.

That is the opposite of what "Enum Conformance" sounds like. WP-B is a small, low-risk change whose only real semantic question is one value.

## 4. That one value is `Unavailable`

`EvidenceAvailability` today: `Available`, `Restricted`, `Unavailable`, `Forgotten`.
Contract: `available`, `restricted`, `expired`, `forgotten`, `external_unavailable`.

Four of the five map exactly. `Unavailable` is the odd one out: it is a single catch-all where the contract has two distinct states, `Expired` and `ExternalUnavailable`.

`memory-compiler/src/evidence.rs:143` is the only place it is interpreted:

```rust
EvidenceAvailability::Unavailable => AttachmentDecision::Defer {
    reason: "unavailable: source payload is not retained".into(),
},
```

and the only place it is constructed is a test at `memory-compiler/tests/evidence.rs:243`.

**Ruling D2:** `Unavailable` cannot be mechanically split, and must not be. Splitting it requires knowing which of the two contract states a given record is in, and the implementation never recorded that — the reason string says "not retained", which is consistent with *both* `Expired` and `ExternalUnavailable` and distinguishes neither. A ruling that picked one would be inventing the distinction it claims to discover.

The disposition is therefore:

1. `Expired` and `ExternalUnavailable` are added, because the contract requires both.
2. `Unavailable` is **removed**, not renamed to either.
3. The single construction site — a test — is rewritten to name the state it actually means, and choosing that state is the implementer's call to state explicitly, not to infer.
4. Serde must reject a payload carrying `Unavailable` rather than coerce it. §7 already forbids "把缺乏迁移依据的旧值静默映射为新值", and there is no persisted data to preserve, so rejection costs nothing.

This is the only place in WP-B where a decision was owed. Every other item is mechanical.

## 5. The BMCP evidence module is not a consumer, and the checklist item is wrong

§7 item 4 requires "验证 BMCP 协议映射", and the §8 WP-B checklist repeats it. That item presupposes that `bmcp-protocol` maps the domain `EvidenceKind`. It does not.

`crates/bmcp-protocol/src/lib.rs` defines its own `EvidenceKind`, inside `pub mod evidence`, with four values:

```rust
pub enum EvidenceKind {
    #[serde(rename = "FINAL_REQUEST_SUBMITTED")] FinalRequestSubmitted,
    #[serde(rename = "APPLIED_CONTEXT_OBSERVED")] AppliedContextObserved,
    #[serde(rename = "EXECUTION_STARTED")] ExecutionStarted,
    #[serde(rename = "RECONCILIATION_OBSERVED")] ReconciliationObserved,
}
```

These are delivery evidence classes. None of them corresponds to `source_span`, `document`, `observation` or any other domain `EvidenceKind` value. Measured:

| check | result |
|---|---|
| does `bmcp-protocol/Cargo.toml` depend on `memory-domain`? | **no** |
| does `bmcp-protocol` mention `memory_domain` anywhere? | **no** |
| is `evidence::EvidenceKind` referenced outside `bmcp-protocol`? | **no** |
| is there any conversion between the two enums? | **none** |

**Ruling D3:** the two `EvidenceKind` enums are unrelated types that share a name. There is no protocol mapping to verify, because there is no mapping. §7 item 4 and the WP-B checklist entry must be struck as measuring something that does not exist.

This also means a WP-B dispatch must **not** touch `bmcp-protocol`. The register's §3 forbids "不修改 BMCP 协议 schema" and that prohibition is unnecessary here rather than inconvenient — a change to the delivery enum would be a change to a different domain's vocabulary under cover of a domain-model fix. The name collision is a hazard for exactly that mistake, and it is worth recording as such.

## 6. Consequences

**WP-B becomes authorizable now.** It is small (one construction site, five match arms, zero persisted data), its only semantic question is ruled in D2, and its only collision hazard is ruled out in D3. Nothing about it depends on the three undefined types.

**WP-A stays blocked, and for a reason the register did not record.** Not "not authorized" as a policy stance, but "not writable" as a fact: three of its thirteen fields are typed with names that have no definition. Authorization cannot unblock it. Only three type definitions can, and each of those is its own ruling — `Instant` needs the OPEN timestamp-precision decision resolved first.

**The register stays OPEN.** §2's "neither work package alone closes it" is unchanged. So are conditions 9 and 10.

## 7. What this ruling deliberately does not do

It does not define `Instant`, `Locator` or `ContentRef`. Defining them requires deciding timestamp precision (an OPEN item in §14), the locator's five-example structure, and whether a content reference is an id, a digest, a range or a union. Each is a real design decision with consequences across every entity that uses the type, and none of them can be inferred from what §8 says. Ruling them in this document, alongside a package split, would bury three architectural decisions in a housekeeping record.

It does not authorize WP-B implementation. It establishes that WP-B **can** be authorized, and what the authorization's scope must be. The dispatch is a separate document.

It does not touch condition 10. Implementation authorization and approval for the migration remain unmet, and this document grants neither.

## 8. What a WP-B dispatch must therefore contain

Recorded here so the dispatch does not have to re-derive it, and so a reader can check the dispatch against this ruling:

1. Add `SourceSpan`, `UserStatement`, `ToolResult`, `Attestation`, `DerivedExcerpt` to `EvidenceKind`; remove `Message`, `Record`, `Dataset`, `Other(String)`; keep `Document`, `Observation`.
2. Add `Expired` and `ExternalUnavailable` to `EvidenceAvailability`; remove `Unavailable`.
3. Rewrite the one `Unavailable` construction site to name its actual state, and say which and why.
4. Serde rejects the removed values; no silent coercion.
5. `bmcp-protocol` is untouched, and the dispatch says so explicitly.
6. Every removed variant is removed because it has zero construction sites — verified, not assumed.
7. No change to `Evidence`'s fields. That is WP-A, and WP-A is blocked.
