# Executed prompt snapshot - AID-2026-254

Source: user-provided W11 task brief in the originating ChatGPT session.
Provenance: structured capture of the dispatched requirements, not a byte-for-byte platform transcript; source provenance is therefore NOT_VERIFIED.

## Required outcome

Create Work Item AID-2026-254 for W11 / Issue #265 AC8. Add a read-only, dependency-free measurement script under scripts/ that computes a reproducible attention/context-switching cost proxy from committed Work Item scope. Include at least one real repository measurement with exact source and output, define a budget and thresholds, and specify how to handle overruns.

Use only GitHub connector/API operations for repository changes. Do not change Issue #265 body or close the Issue. PR description must declare Related issue(s): #265, AI-assisted work: YES, and the resolvable session-evidence path. Merge only after all sixteen required contexts succeed on the exact head and the branch is current with main. Use a merge commit, then read back every changed file blob from main. After merge, leave a comment on Issue #265 with the metric definition, measured values, thresholds, and proposed AC8 wording.

Fixed attribution: user-authorized operator (delegated by account owner). Date: 2026-11-27. Work-item identifier: AID-2026-254.
