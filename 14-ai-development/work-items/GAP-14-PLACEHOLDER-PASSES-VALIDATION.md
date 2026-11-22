# GAP-14 — a validating `FactRevision` cannot tell a real I/D reference from a placeholder

**Status:** open · **Severity:** Tier 2 (no reachable exploit today; closes a validation window) · **Owner:** I, D
**Measured at:** `b093b59f` · **Related:** ADR `OWNER-DECISION-PUBLICATION-RECORD-001` (D6), GAP-12, GAP-13

## 1. What validates, and what it cannot see

`FactRevision::validate` (`crates/memory-domain/src/lib.rs:956`) returns `Ok(())` for a
revision whose attestor and canonical-commit references were both minted by public
placeholder factories. The code says so itself, three lines above the function:

> Structural validation cannot distinguish a real I-issued attestor/authorization
> reference from public `pending_i()` placeholders, nor a D-issued commit from
> `pending_d()`. A FactRevision using placeholders can therefore validate today.
> This known temporary construction window closes only after I and D freeze their
> contracts and the placeholders are replaced with validated, non-forgeable refs.
> `Ok(())` here is not evidence of authorization or canonical acceptance.

The comment is accurate and unusually candid. The problem is not that it is wrong.
It is that it exists only in a source comment, so:

- a caller reading `validate() -> Result<(), DomainError>` concludes the revision is
  valid;
- nothing in `14-ai-development/` records the window as an open gap
  (`grep -rln "pending_i|known temporary construction window" 14-ai-development/`
  → 0 matches before this document);
- the two placeholder factories are `pub`, so "non-forgeable" is currently false.

## 2. Measured facts

| claim | measurement |
|---|---|
| `pending_d()` is public | `lib.rs:548` `pub const fn pending_d()` |
| `pending_i()` is public | `lib.rs:523` and `:533` (two impls, both `pub const`) |
| placeholders satisfy `validate()` | the doc comment states it; `validate` checks presence, not provenance |
| `FactRevision` reaches the compiler | `grep FactRevision crates/memory-compiler/` → 0 matches |
| placeholders used outside tests | `grep pending_d() crates/` → only `memory-domain` tests + `phase2_acceptance.rs` |

The last two rows matter for severity: because `FactRevision` never enters
`memory-compiler`, this cannot currently produce a `Published` disposition. It is a
dormant window, not a live bypass. That is why this is Tier 2 and not Tier 1.

## 3. Why it is worth recording anyway

The gap is a *validation* gap, and validation gaps become live the moment a caller
appears. The realistic sequence is: someone wires `FactRevision` into the compiler to
satisfy a future publication requirement, calls `validate()` to gate it, sees
`Ok(())`, and ships. Every step of that sequence is reasonable in isolation, and the
warning they would need is in a comment above a function they did not write.

Recording it converts a comment into a tracked constraint. That is the entire value.

## 4. Repair, in order

1. **(I, D)** Freeze the attestor and canonical-commit contracts, each with a
   content-bearing reference type and a constructor that only the issuer can call.
2. **(I, D)** Replace `pending_i()` / `pending_d()` with a single
   `NotYetIssued` marker that `validate()` rejects, so the temporary window is
   closed by construction rather than by comment.
3. **(domain)** Make `validate()` fail on placeholders. Any test currently relying on
   a placeholder validating becomes a test that asserts the placeholder is rejected —
   a strictly better assertion.
4. **(domain)** Remove the `pub` from both factories, or keep them `pub` and have
   `validate()` reject their output. Non-forgeability must be a property, not a
   doc sentence.

## 5. Closure criteria

1. `FactRevision::validate()` returns `Err` for a revision built with any placeholder
   reference; a test proves it.
2. `pending_i()` / `pending_d()` either no longer exist, or are unreachable from
   outside the crate.
3. The doc comment at `lib.rs:955-960` is deleted, because the condition it warns
   about no longer exists — not merely reworded.
4. `14-ai-development` records the closure, so the next reader does not have to
   rediscover the window from a comment.

## 6. What this document does not claim

It does not claim the placeholder design was wrong. A declared placeholder with a
candid warning is a reasonable way to unblock dependent work before two owners freeze
contracts. The claim is narrower: a warning that lives only in a comment is not a
control, and it was not visible anywhere a reader of the gap register would look.
