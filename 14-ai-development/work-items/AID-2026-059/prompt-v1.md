# Executed prompt record - AID-2026-059

PROVENANCE: NOT_VERIFIED. This file is the instruction set actually issued for
this work, consolidated after the session ran across several prompts. The digest
pinned in the manifest covers these bytes, not the byte-exact model input.

## Standing directives (verbatim)

> 端口上所有产出必须能被变异检验打穿；全绿不是证据。

> 不要写新逻辑，只做机械删除。

> 不能自己动手写代码 —— 逻辑设计必须由会话主导。

## Task

Implement deliverable A of Issue #799 in `oahcom/AiMemoryBrainArchitecture`.

A. Add an unconditional `pull_request` check that requires AI session evidence in

1. the pull request description,
2. every linked Issue,
3. the Work Item manifest.

B. Do not add the check to required contexts. Issue #799 withholds that status
until the check has run on real pull requests and an Owner has approved it
separately.

## Frozen constraints

1. The policy effective time is one constant in the workflow file.
2. The check must not be skippable via `paths:`, a job-level `if:`, or `needs:`.
3. A historical Issue must produce a successful `NOT_APPLICABLE` verdict, never
   `skipped` and never `neutral`.
4. After the policy effective time, a missing field must fail.
5. Multiple sessions are expressed as repeated manifest entries.
6. SHA-256 is taken over raw bytes, not over decoded text.
7. CI asserts structure and existence only. It does not judge whether the
   evidence is good.
8. Required Context needs calibration on real pull requests plus a separate
   Owner approval.
9. The seven-field model from #775 must not be replaced.
10. Self-hosted runners must not be restored.

## Repository constraints discovered while implementing

- There is no pytest: 55 of 58 `test_*.py` files use `unittest` and none import
  pytest, with no `pyproject.toml`, `pytest.ini`, `setup.cfg` or `tox.ini`. A
  suite that cannot run under `unittest discover` also fails
  `scripts/ci/check_test_reachability.py`.
- `scripts/ci/check_repository_hygiene.py` admits new files by anchored rule.
  `.py`, `.md` and `.github/workflows/*.yml` are admitted.
- `scripts/ci/check_line_endings.py` judges by the Git `text` attribute; write LF.
- `scripts/ci/gate_ratchet.py` compares against a bilingual baseline of 77 paths
  and requires no regression.
- `check_index_membership` reads the work-items directory and `INDEX.md` from the
  committed tree and validates both directions, so a new AID directory requires
  an INDEX row.
