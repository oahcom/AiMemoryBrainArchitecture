import tempfile, unittest
from pathlib import Path
import yaml
from migrate_status import PHASES, run
from check_status_gates import check

class StatusMigrationTests(unittest.TestCase):
 def test_all_twelve_source_states_map(self):
  self.assertEqual(len(PHASES),12)
  self.assertEqual(PHASES["PROPOSED"],"INTAKE")
  self.assertEqual(PHASES["REVIEWED"],"VALIDATION")
  self.assertEqual(PHASES["CLOSED"],"COMPLETE")
 def test_dry_run_does_not_write(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"manifest.yaml"; p.write_text("status: 'IN_PROGRESS — active'\n")
   before=p.read_bytes(); result=run(p)
   self.assertEqual(result["result"],"WOULD_MIGRATE")
   self.assertEqual(p.read_bytes(),before)
 def test_apply_backup_and_rollback_exact_bytes(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"manifest.yaml"; original=b"status: VERIFIED\n"
   p.write_bytes(original); run(p,apply=True)
   d=yaml.safe_load(p.read_text())
   self.assertEqual(d["status"],"VERIFIED")
   self.assertEqual(d["lifecycle"]["phase"],"VALIDATION")
   self.assertEqual(d["lifecycle"]["gates"]["verified"]["status"],"NOT_RECORDED")
   run(p,rollback=True); self.assertEqual(p.read_bytes(),original)
 def test_unknown_state_fails_closed(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"manifest.yaml"; p.write_text("status: UNDER_REVIEW\n")
   with self.assertRaises(ValueError): run(p,apply=True)
   self.assertFalse(p.with_name(p.name+".pre-status-migration.bak").exists())
 def test_gate_checker_does_not_accept_placeholder(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"manifest.yaml"
   p.write_text("status: VERIFIED\nlifecycle:\n  phase: VALIDATION\n  source_status: VERIFIED\n  gates:\n    verified:\n      status: NOT_RECORDED\n")
   with self.assertRaises(ValueError): check(p)

if __name__=="__main__": unittest.main()
