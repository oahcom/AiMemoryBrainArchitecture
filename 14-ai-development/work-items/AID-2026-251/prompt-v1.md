# AID-2026-251 dispatched task snapshot

Repository: oahcom/AiMemoryBrainArchitecture
Base branch: main
Assigned work item: AID-2026-251
Related issue: #266

Define a block-style YAML schema for Work Item manifests under
14-ai-development/work-items/. The schema must define the required top-level
key set and the documentation, session_evidence, and implementation shapes.
Add a read-only checker under scripts/ci/, integrate it into the existing
workflow job pattern without adding dependencies, and report all current
manifest compliance and violations without migrating existing manifests.
Preserve issue #266 as open. PR metadata must include the Related issue(s),
AI-assisted work declaration, and session evidence reference. Use the
delegated operator attribution and date 2026-11-27.

The operator must report only GitHub-observed CI, merge, and blob verification
results; do not fabricate check results or SHAs.
