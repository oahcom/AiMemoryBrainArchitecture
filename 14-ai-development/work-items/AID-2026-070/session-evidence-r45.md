---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The unconditional write, the primary-key declaration, the three stage lines and the test that pins the defect as expected behaviour were re-read on 2026-11-25 from the immutable snapshot of main at a1533c67; the prompt digest and byte count were computed from the committed file rather than copied from another work item."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session role / use case

IMPLEMENTER, registration only. Register WO-03 / E2 as an accountable work item
against Issue #262 AC7: a second compile that cannot reach Context construction
is a defect with no work item, so AC7 cannot be evaluated for it.

This session did not write, build or test production code. It wrote three
governance artefacts for this work item and re-measured the code it points at.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction
this registration was carried out against. It is the file the manifest pins by
digest (`b0013ed25ebdf4c5a0cc200551d9e89edf6993138828527abb2fab137fda024a`,
6371 bytes).

One edit was made to that text before it was committed, and it is disclosed here
rather than left to a diff: the prompt names the F8 work order in its exclusion
section, and that reference was updated from the number it was drafted under
(`AID-2026-064`) to the number this registration actually occupies
(`AID-2026-069`). No other byte changed.

**Read before writing:**

| input | what it settled |
|---|---|
| `crates/brain-cli/src/main.rs` at `a1533c67` | `:694-696` creates unconditionally; `:747` `build_context`; `:795` `deliver_snapshot`; the three stage lines at `:824`, `:825-827`, `:830` |
| `crates/memory-storage-sqlite/src/lib.rs:86` | `memory_id TEXT PRIMARY KEY`, which is why the second insert is a constraint violation rather than a query |
| `crates/brain-cli/tests/compile_persists_store.rs` | 335 lines, three tests at `:144`, `:212`, `:271`; `:308-317` asserts the second run must fail |
| `facts/r44_ac2_ac4.remeasured.md` | WO-03 is three files, and it is ordered after WO-02 |
| `AID-2026-066..068` manifests | the `session_evidence` field set — shape copied, values not |

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
executing session read.

Two standing directives governed the session and are reproduced verbatim because
the acceptance text is stated against them:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可。

> 不能自己动手写代码。

# AI-visible output

Three files created, no production file changed:

```
14-ai-development/work-items/AID-2026-070/manifest.yaml
14-ai-development/work-items/AID-2026-070/prompt-v1.md
14-ai-development/work-items/AID-2026-070/session-evidence-r45.md
```

Measurements taken at `a1533c67` and re-read on 2026-11-25:

```
crates/brain-cli/src/main.rs
  694-696  store.create_memory(...)     unconditional; error flattened at :696
  698-708  write_revision               never reached on the second run
  711-713  read_current                 never reached
  747-755  build_context(               never reached; :749 passes the literal 1
  795      deliver_snapshot(            never reached
  824      memory-store: ... read_current succeeded
  825-827  memory-context: build_context produced {n} entry/ies
  830      output: {path} ({n} bytes)

crates/memory-storage-sqlite/src/lib.rs
     86    memory_id TEXT PRIMARY KEY     the collision is structural

crates/brain-cli/tests/compile_persists_store.rs
  271-334  a_failed_compile_leaves_no_readable_store_of_its_own
    307    the second compile
  308-311  asserts exit Some(1), "re-compiling ... must fail"
  313-317  asserts stderr contains "create_memory failed"
```

Rows four and seven are the constraint on how this work order can be accepted: a
test currently asserts that the second run fails, so "the second run succeeds"
cannot be demonstrated without editing it. Editing it is the work.

# Limitations

1. **Nothing in this work item is implemented.** `status: DISPATCHED` records
   dispatch, not progress. Every acceptance criterion is a future observable.
2. **C2 is stated against the three stage lines and the output file, not against
   an exit code.** An exit code of 0 is producible by skipping the stages, which
   is the defect with a different symptom.
3. **C8 exists to keep this work order from absorbing F7.** Reaching
   `build_context` is not producing a legitimate new version; the literal `1` at
   `:749` is the F7 work order's subject (AID-2026-066) and is out of scope here.
4. **This work order depends on AID-2026-069 and does not satisfy it.** If the
   distinction between "already exists" and "invalid reference" is not in the
   contract, C3 can only be met by matching a message string, which is not the
   named rule the criterion asks for.
