# Manifest Blob Pin Ledger

This ledger is append-only with one narrowly scoped correction rule: existing pin-transition facts must not be edited, reordered, or removed. A `repin_commit` locator may be corrected only when independently verified Git history proves that the recorded SHA is not the commit that introduced the unchanged `previous_pin -> new_pin` transition. Such a correction must preserve the manifest, field, path, previous pin, and new pin, and must document the old and corrected commit SHA and the reason below. This exception does not authorize changing or deleting a pin-transition fact.

Correction record:
- AID-2026-101 and AID-2026-102: the original `repin_commit` locator `6045af65fcc2e89d1895e09ed666af4d737203bf` was not an ancestor of main. The actual main commit introducing both unchanged `4470 -> 4412` byte-count transitions is `2ab66153dbcdd8a8f2d68d234914751a748a8f74`. Only the locator is corrected; both transition facts remain unchanged.

Add new records only after the corresponding repin commit has been created and its full commit SHA is known.

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

New mode-aware records use the seven-column format. The legacy six-column table above is read as `reference_mode=current`; a record with a different mode is a distinct pin identity, so the same manifest/field/path may carry one chain per mode.

| manifest | field | path | reference_mode | previous_pin | new_pin | repin_commit |
|---|---|---|---|---|---|---|
