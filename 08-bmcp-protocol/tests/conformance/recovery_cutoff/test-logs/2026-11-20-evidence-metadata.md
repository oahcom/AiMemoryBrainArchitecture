# F-43-03 Complete Test Evidence — 2026-11-20

## Execution Environment
- OS: Windows (Git Bash)
- Python: 3.12.3 (C:/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe)
- pip: 24.0
- jsonschema: 4.26.0
- Node.js: 22.22.2
- npm: 10.9.7

## Dependencies Installed
1. `rfc8785==0.1.4` via `pip install rfc8785==0.1.4` (Python 3.12.3) — SUCCESS
2. `canonicalize@2.1.0` via `npm install canonicalize@2.1.0` (Node 22.22.2) — SUCCESS

## Execution Command
```bash
cd C:/Users/Administrator/WorkBuddy/2026-11-18-18-46-31/state/repo
python -m unittest discover \
  -s 08-bmcp-protocol/tests/conformance/recovery_cutoff \
  -p "test_*.py" -v
```

## Result Summary
```
Ran 432 tests in 0.707s

OK (skipped=22)
```

- Exit code: 0
- PASS (ok): 410
- FAIL: 0
- ERROR: 0
- SKIP: 22 (all from test_unified_manifest_1_2_10.UnionSemanticsTests — "Legacy 1.2.10 semantics are superseded by 1.2.11/1.2.12")
- Count verification: 410 + 22 = 432 = Ran ✓

## Evidence Chain
- H HEAD commit: 1d5296e0effa7c6466c9e7aef9f071827ff8aa1c
- Test file Blob: 40694238e01139c764f03a9ba3cbfabfeb28d318
- Validator Blob: f572ef31c270f9fee8bb7dd84ad7d1b548650aa9 (unchanged)
- Raw log: test-logs/2026-11-20-full-suite-python312.log (72,653 bytes)
