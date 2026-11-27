"""Negative tests for the skip registry: an unregistered case or reason must fail main()."""
import subprocess
import sys
from pathlib import Path

HARNESS = r'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t

t.skip("T99 a case nobody registered", "some reason")
print("UNEXPECTED_SKIPS:", t.UNEXPECTED_SKIPS)
code = t.main()
print("MAIN_EXIT:", code)
sys.exit(0 if code == 1 else 2)
'''

HARNESS2 = r'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t

t.skip("T36 directory symlink is rejected as a governed root", "a different reason")
print("UNEXPECTED_SKIPS:", t.UNEXPECTED_SKIPS)
code = t.main()
print("MAIN_EXIT:", code)
sys.exit(0 if code == 1 else 2)
'''

for label, harness in (("unregistered-name", HARNESS), ("wrong-reason", HARNESS2)):
    r = subprocess.run([sys.executable, "-c", harness], capture_output=True, text=True,
                       cwd=str(Path.cwd()), encoding="utf-8", errors="replace")
    tail = [l for l in (r.stdout or "").splitlines() if l.startswith(("UNEXPECTED_SKIPS", "MAIN_EXIT"))]
    print(label, "->", "PASS" if r.returncode == 0 else "FAIL", tail[-2:])
