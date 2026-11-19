#!/usr/bin/env python3
"""Regression tests for bilingual governance scripts (stdlib only)."""
import os,subprocess,sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
TIERING=HERE/"check-bilingual-tiering.sh"; SYNC=HERE/"check-bilingual-sync.sh"; TRANSLATOR=HERE/"translate-document.py"
# On Windows, plain BASH may resolve to the WSL launcher; BASH_BIN lets
# callers point at a real POSIX bash (e.g. Git Bash) explicitly.
BASH=os.environ.get("BASH_BIN","bash")
class Tests(unittest.TestCase):
    def run_cmd(self,cmd,**kw):
        # MSYS bash eats backslash escapes in Windows-style paths; pass POSIX
        # style paths and decode robustly on any platform.
        cmd=[c.as_posix() if isinstance(c,Path) else c for c in cmd]
        return subprocess.run(cmd,text=True,capture_output=True,check=False,
                              encoding="utf-8",errors="replace",**kw)
    def test_unknown_is_reported_not_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); subprocess.run(["git","init","-q",str(root)],check=True)
            subprocess.run(["git","-C",str(root),"config","user.email","test@example.invalid"],check=True)
            subprocess.run(["git","-C",str(root),"config","user.name","Test"],check=True)
            (root/"docs").mkdir(); (root/"docs"/"new.md").write_text("# new\n",encoding="utf-8")
            mapping=root/"mapping.yaml"; mapping.write_text("tier1:\n  files:\n    - path: known.md\ntier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules:\n    - directory: docs/\n      tier: UNKNOWN\n",encoding="utf-8")
            subprocess.run(["git","-C",str(root),"add","."],check=True); subprocess.run(["git","-C",str(root),"commit","-qm","fixture"],check=True)
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,2,r.stdout+r.stderr); self.assertIn("UNKNOWN\tdocs/new.md",r.stdout); self.assertIn("NEEDS_CONFIRMATION",r.stderr)
    def test_sync_failure_exit_propagates(self):
        with tempfile.TemporaryDirectory() as d:
            stub=Path(d)/"python-fails"; stub.write_text("#!/bin/sh\nexit 23\n",encoding="utf-8"); stub.chmod(0o755)
            r=self.run_cmd([BASH,SYNC,"--source","s.md","--counterpart","t.md"],env={**os.environ,"PYTHON_BIN":str(stub.as_posix())})
            self.assertEqual(r.returncode,23,r.stdout+r.stderr)
    def test_sync_source_revision_and_pairing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s,t=root/"s.md",root/"t.md"
            s.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: t.md -->\n",encoding="utf-8")
            t.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: s.md -->\n",encoding="utf-8")
            r=self.run_cmd([BASH,SYNC,"--source",s,"--counterpart",t])
            self.assertEqual(r.returncode,0,r.stdout+r.stderr); self.assertIn("PASS",r.stdout)
    def test_translation_diff_work_order(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s,t,o=root/"zh.md",root/"en.md",root/"work.md"
            s.write_text("# 标题\nMUST 保留。\n",encoding="utf-8"); t.write_text("# Title\nMUST preserve.\n",encoding="utf-8")
            r=self.run_cmd([sys.executable,TRANSLATOR,"--source",s,"--target",t,"--output",o])
            self.assertEqual(r.returncode,0,r.stdout+r.stderr); body=o.read_text(encoding="utf-8")
            self.assertIn("status: PENDING_TRANSLATION",body); self.assertIn("Human translator/reviewer",body); self.assertIn("no model/API invocation",body)
    def test_translation_failure_status_registered(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); o=root/"failed.md"
            r=self.run_cmd([sys.executable,TRANSLATOR,"--source",root/"missing.md","--target",root/"t.md","--output",o])
            self.assertEqual(r.returncode,1,r.stdout+r.stderr); self.assertTrue(o.is_file()); body=o.read_text(encoding="utf-8")
            self.assertIn("status: FAILED",body); self.assertIn("failure:",body)
if __name__=="__main__": unittest.main(verbosity=2)
