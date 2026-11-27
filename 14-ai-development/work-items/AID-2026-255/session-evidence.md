# AID-2026-255 — Session Evidence

## Execution authority and scope ruling

The implementing session executed `14-ai-development/work-items/AID-2026-255/prompt-v1.md` as its authority:

- Prompt-v1 SHA-256: `cb009e755cde42f8553edca13fb1e013c40bacd4007fcceeddccdc1ea2059cfe`
- Prompt-v1 size: 16,491 bytes
- Prompt-v1 remains immutable.

Owner A's scope ruling is committed separately as `14-ai-development/work-items/AID-2026-255/prompt-v2.md`:

- Prompt-v2 SHA-256: `112d0371d90f89cfa895c8e2e62cc80cb751ab097355c5cbf72bb85378dd52f1`
- Prompt-v2 size: 2,711 bytes

Prompt-v1 is the executed authority; prompt-v2 is the subsequent Owner A scope ruling that constrains the delivered implementation to the explicitly authorized 12 field identities.

## Implementation

The implementing session committed the checker and its regression tests:

- `scripts/ci/check_manifest_blob_pins.py`
- `scripts/ci/test_check_manifest_blob_pins.py`

The checker is limited to the 12 authorized manifest field identities. For each identity it resolves the sibling path and declared digest from the candidate Git tree and compares the declared digest with the Git blob SHA-1. It does not infer additional path/digest pairs or inspect out-of-scope fields. The existing 12-entry ratchet baseline was not changed.

Measured base: `10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f`.

## Local validation — implementing session

The implementing session reports the following commands and observed outputs:

1. Command:

   `python scripts/ci/check_manifest_blob_pins.py`

   Output/result: exactly 12 failure lines; exit 1. This is the expected measured result on `main`, where the 12 authorized declarations currently mismatch their referenced Git blob identities.

2. Command:

   `python scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/manifest-blob-pins.txt --format paths --command "python scripts/ci/check_manifest_blob_pins.py"`

   Output:

   ```text
   baseline=12 current=12 regressions=0 fixed=0
   PASS
   ```

   Exit 0. The existing 12-entry baseline ratchets the measured findings without regression.

3. Command:

   `python scripts/ci/test_check_manifest_blob_pins.py`

   Output:

   ```text
   Ran 9 tests ... OK
   ```

   Exit 0.

4. Command:

   `python scripts/ci/check_manifest_parse.py`

   Output:

   ```text
   115 manifests found, 115 parsed, 0 failed
   ```

   Exit 0.

5. Command:

   `python scripts/ci/check_repository_hygiene.py --base <main> --head <head>`

   Output:

   ```text
   violations=0
   ```

   Exit 0.

These are local implementing-session results. They are not CI results and do not constitute independent review or acceptance.

## Current disposition

- Implementation: committed.
- Local validation: all five reported commands produced the outputs recorded above.
- CI: PENDING; no CI run is claimed.
- Independent review: PENDING; no reviewer or review result is recorded.
- Acceptance: PENDING; no Owner acceptance is claimed.
- Merge: PENDING; no merge is claimed.
