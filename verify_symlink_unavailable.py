"""Force symlink creation to fail, then run only run_symlink_boundary().

Reproduces the platform that #1268 describes: Path.symlink_to raises OSError.
Prints RESULTS / RESULTS_BY_NAME / SKIPPED / UNEXPECTED_SKIPS as the suite
itself records them, so "skipped" in the log can be compared with "passed" in
the accounting.
"""
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t  # noqa: E402

NAMES = [
    "T36 directory symlink is rejected as a governed root",
    "T37 governed_files does not descend into a symlinked root",
    "T41 symlinked governed file is rejected",
    "T42 governed file reached through a symlinked parent is rejected",
]

with mock.patch.object(Path, "symlink_to", side_effect=OSError("simulated: no symlink support")):
    t.run_symlink_boundary()

print("RESULTS:", t.RESULTS)
print("RESULTS_BY_NAME:", t.RESULTS_BY_NAME)
print("SKIPPED:", t.SKIPPED)
print("UNEXPECTED_SKIPS:", t.UNEXPECTED_SKIPS)

recorded = [n for n in NAMES if n in t.RESULTS_BY_NAME]
missing = [n for n in NAMES if n not in t.RESULTS_BY_NAME and n not in t.SKIPPED]
print("RECORDED_AS_RESULT:", recorded)
print("MISSING_FROM_EVERYTHING:", missing)

ok = (
    not recorded
    and not t.UNEXPECTED_SKIPS
    and all(n in t.SKIPPED for n in NAMES)
)
print("VERDICT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
