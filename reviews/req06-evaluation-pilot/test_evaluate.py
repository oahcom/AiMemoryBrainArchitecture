#!/usr/bin/env python3
import importlib.util, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("evaluate",HERE/"evaluate.py")
ev=importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)
class PilotTests(unittest.TestCase):
 def test_corpus_provenance_and_controls(self):
  rows=ev.load_corpus(); self.assertEqual(len(rows),10)
  self.assertEqual(sum(r["source_kind"]=="repository_document" for r in rows),8)
  self.assertTrue(all(len(r["source_blob"])==40 for r in rows if r["source_kind"]=="repository_document"))
 def test_policy_proxy_excludes_forgotten_and_other_scope(self):
  rows=ev.load_corpus(); selected=ev.brain_policy_proxy(ev.TASKS[4],rows)
  self.assertNotIn("CONTROL-FORGOTTEN",selected); self.assertNotIn("CONTROL-OTHER-SCOPE",selected)
 def test_negative_task_abstains(self):
  rows=ev.load_corpus(); task=ev.TASKS[-1]
  self.assertEqual(ev.brain_policy_proxy(task,rows),[])
 def test_three_arms_are_deterministic(self):
  rows=ev.load_corpus()
  first=[ev.evaluate("none",f,rows) for f in (ev.no_memory,ev.lexical,ev.brain_policy_proxy)]
  second=[ev.evaluate("none",f,rows) for f in (ev.no_memory,ev.lexical,ev.brain_policy_proxy)]
  for a,b in zip(first,second):
   for key in ("task_success_rate","positive_task_hit_rate","mean_recall","mean_precision","mrr_all_tasks","harmful_activations","selected_count"):
    self.assertEqual(a[key],b[key])
 def test_confidence_interval_bounds(self):
  lo,hi=ev.wilson(4,7); self.assertLessEqual(lo,4/7); self.assertGreaterEqual(hi,4/7)
if __name__=="__main__": unittest.main(verbosity=2)
