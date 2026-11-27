# AID-2026-255 — Blob Field Inventory

## Scope and method

The checker uses a closed authorization set of exactly 12 field identities: nine identities in `AID-2026-100/manifest.yaml` and three in `AID-2026-150/manifest.yaml`.

A field is in scope only when its exact manifest path and field identity appear in that authorization set. The checker does not discover pins by recursively matching arbitrary `path` and digest keys. Out-of-scope families are explicitly attributed below; they are excluded rather than silently dropped.

The digest algorithm for every in-scope identity is Git blob SHA-1:

`SHA-1(b"blob " + decimal_byte_length + NUL + file_bytes)`

The path and digest are resolved from the candidate Git tree.

## Authorized field families

| Definition location | Declaration shape | Path key | Digest key | Algorithm | Disposition and reason |
|---|---|---|---|---|---|
| `14-ai-development/work-items/AID-2026-100/manifest.yaml` — `baseline_and_source_evidence.authored_indexes[0]` and `[1]` | Two authored-index records, each with root, English mirror and Chinese mirror path/digest pairs | `root`, `en_mirror`, `zh_cn_mirror` | `root_blob`, `en_mirror_blob`, `zh_cn_mirror_blob` | Git blob SHA-1 | IN SCOPE — six exact field identities explicitly authorized by Owner A |
| `14-ai-development/work-items/AID-2026-100/manifest.yaml` — `related_evidence[0]` | One related-evidence record with root, English mirror and Chinese mirror path/digest pairs | `path`, `en_mirror`, `zh_cn_mirror` | `blob`, `en_mirror_blob`, `zh_cn_mirror_blob` | Git blob SHA-1 | IN SCOPE — three exact field identities explicitly authorized by Owner A |
| `14-ai-development/work-items/AID-2026-150/manifest.yaml` — `source.files[0]`, `[1]`, `[2]` | Three source-file records, each with a path and blob digest | `path` | `blob` | Git blob SHA-1 | IN SCOPE — three exact field identities explicitly authorized by Owner A |

## Measured out-of-scope families

| Definition location / family | Declaration shape | Path key | Digest key | Algorithm | Measured count | Disposition and reason |
|---|---|---|---|---|---:|---|
| Manifest prompt declarations: `prompt_file` with `prompt_sha256`, including `prompt_addenda[].prompt_sha256` | Prompt-file reference and SHA-256 declaration | `prompt_file` (or corresponding prompt-file sibling) | `prompt_sha256` | SHA-256 | 41 mismatching; 3 without a sibling path; 1 non-digest value (`NOT_VERIFIED`) | EXCLUDED — invariant owned by #1318 and #1278; not part of the 12 authorized Git blob identities |
| `scope.changes[].path`, `declared_exceptions[].path`, `documentation[].path` | Path-only entries without a corresponding digest key | `path` | None | None | 108 | EXCLUDED — a path list is not a content pin |
| `reconstructed_root_blob` (AID-2026-100), `aid_100_evidence_blob` (AID-2026-107), `aid_107_evidence_blob` (AID-2026-111), `latest_applied_evidence_blob` (AID-2026-093) | Digest declarations without a tree-relative sibling path | None | Field-specific pathless digest field | Not verifiable under the tree-relative contract | 4 | EXCLUDED — PATHLESS / NOT VERIFIABLE; no referenced tree path is available for resolution |

## Closed-set rule

Only the 12 enumerated field identities are authorized. No additional path/digest pair is inferred from field names, neighboring data, recursive traversal, prompt metadata, or other manifest content. The out-of-scope families above are recorded with their measured counts and ownership/disposition so their exclusion is explicit and auditable.
