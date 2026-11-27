"""Force a recognized symlink-policy failure and verify exact skip accounting."""
import errno
import sys
from collections import Counter
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

# Use an explicit permission errno with no Windows winerror, exercising the
# portable errno fallback on every platform.
simulated_policy_error = OSError(errno.EPERM, "simulated: symlink privilege unavailable")

with mock.patch.object(Path, "symlink_to", side_effect=simulated_policy_error):
    t.run_symlink_boundary()

print("RESULTS:", t.RESULTS)
print("RESULTS_BY_NAME:", t.RESULTS_BY_NAME)
print("SKIPPED:", t.SKIPPED)
print("UNEXPECTED_SKIPS:", t.UNEXPECTED_SKIPS)

counts = Counter(t.SKIPPED)
count_per_name = {name: counts[name] for name in NAMES}
recorded = [name for name in NAMES if name in t.RESULTS_BY_NAME]
missing = [name for name in NAMES if counts[name] == 0 and name not in t.RESULTS_BY_NAME]
duplicates = [name for name in NAMES if counts[name] != 1]

print("SKIPPED_COUNT_PER_NAME:", count_per_name)
print("RECORDED_AS_RESULT:", recorded)
print("MISSING_FROM_EVERYTHING:", missing)
print("DUPLICATE_SKIPS:", duplicates)

ok = (
    all(counts[name] == 1 for name in NAMES)
    and not recorded
    and not missing
    and not duplicates
    and not t.UNEXPECTED_SKIPS
)
print("VERDICT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
