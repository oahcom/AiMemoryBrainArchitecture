# Manifest Blob Pin Ledger

This ledger records pin transitions append-only. Do not reorder or remove existing transition records. Add new records only after the corresponding repin commit has been created and its full commit SHA is known.

For a squash merge, `repin_commit` must identify the squash commit that actually entered the target history, not the pre-squash pull-request head. If an existing record points to a pre-squash commit that is not reachable from the target history, the only permitted in-place correction is to replace `repin_commit` with the corresponding landed squash commit, provided all five validity rules below still hold. The manifest, field, path, previous pin, new pin, and record order must remain unchanged.

Each record must satisfy all of the following validity rules:

1. `manifest`, `field`, and `path` identify exactly one declared pin in the manifest.
2. `previous_pin` equals the pin value in the first parent of `repin_commit`.
3. `new_pin` equals the pin value introduced by `repin_commit`.
4. `repin_commit` is a valid full commit SHA and is an ancestor of the commit being verified.
5. Records for the same `(manifest, field, path)` form a continuous history, and the target commit's pin equals the latest recorded `new_pin`.

| manifest | field | path | previous_pin | new_pin | repin_commit |
|---|---|---|---|---|---|
|14-ai-development/work-items/AID-2026-101/manifest.yaml|session_evidence[0].executed_prompt_snapshot_file|14-ai-development/work-items/AID-2026-101/prompt-v1.md|4470|4412|2ab66153dbcdd8a8f2d68d234914751a748a8f74|
|14-ai-development/work-items/AID-2026-102/manifest.yaml|session_evidence[0].executed_prompt_snapshot_file|14-ai-development/work-items/AID-2026-102/prompt-v1.md|4470|4412|2ab66153dbcdd8a8f2d68d234914751a748a8f74|
