# AID-2026-042-PROMPT v1 — Patch sys.argv in real-git gate regression helper

## User dispatch

Repository: oahcom/AiMemoryBrainArchitecture, base main at d9c29a1c16b81f32eba82cd0e59a7e7b13de05a8.

Repair the three failing tests in scripts/governance/evidence/test_gate_normative_roots.py. The helper GateRootsTest._run_real_git_gate_for_change() calls self.gate.main() inside an ExitStack but does not isolate sys.argv. Under unittest discovery, process arguments are inherited by the gate CLI and cause exit code 2 with an unknown-argument diagnostic.

## Authorized minimal change

- Import sys if it is not already imported.
- In the existing contextlib.ExitStack(), enter patch.object(sys, "argv", ["scripts/check_bilingual_docs.py"]) before calling self.gate.main().
- Reuse the existing unittest.mock.patch import.

## Explicit exclusions

- Do not change scripts/check_bilingual_docs.py CLI argument handling.
- Do not weaken the three exit-code assertions.
- Do not change the JSON non-bilingual-document policy introduced by #527.
- Do not make unrelated changes.

## Acceptance

Run and record the original output for:

    python3 -m unittest discover -s scripts/governance/evidence -p 'test_gate*.py'
    BASE_SHA=$(git rev-parse HEAD) HEAD_SHA=$(git rev-parse HEAD) python3 scripts/check_bilingual_docs.py
    git diff -w --stat $(git rev-parse HEAD^) HEAD
    python3 scripts/precheck_delivery.py

Expected: 52/52 tests pass, the bilingual gate exits 0, and the implementation commit changes only the test file by a few lines. Open a PR titled "test(bilingual): patch sys.argv in the real-git gate regression helper".

## Provenance

Frozen from the user-provided task dispatch in this ChatGPT conversation on 2026-11-21. The platform raw prompt payload bytes and session identifier are not exposed. The recorded SHA-256 identifies the committed prompt-v1.md bytes only.
