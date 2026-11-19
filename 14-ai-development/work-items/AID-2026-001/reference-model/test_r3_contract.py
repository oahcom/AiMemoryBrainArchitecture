"""Executable R3 reference-model assertions; source IDs retained in method names."""
import unittest
from r3_contract_model import Authorization, ContractViolation, Lifecycle, Phase, Reconciliation, R3Model

def auth(**kw):
    d=dict(issuer_known=True,signature_valid=True,audience_matches=True,operation_matches=True,
           request_hash_matches=True,purpose_matches=True,scope_matches=True,not_before=0,
           expires_at=100,permission_epoch=7,nonce_unused=True,delegation_current=True)
    d.update(kw); return Authorization(**d)
def done():
    m=R3Model("mem"); m.authorize_and_suppress(auth(),10,7,"op"); return m

class DFI(unittest.TestCase):
    def test_DFI_001(self):
        m=done(); self.assertFalse(m.read_allowed(m.fence_generation)); self.assertFalse(m.read_allowed(None))
    def test_DFI_002(self):
        m=done(); m.phase=Phase.CLEANUP; self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN); self.assertNotEqual(m.phase,Phase.COMPLETED)
    def test_DFI_003(self):
        m=done(); f=m.fence_generation
        with self.assertRaises(ContractViolation): m.forgotten_transition("Cancel")
        self.assertEqual(m.fence_generation,f)
    def test_DFI_004(self):
        m=done(); m.set_required_targets(["required","unknown-required-target"]); m.mark_target("required","SUCCEEDED"); m.mark_target("unknown-required-target","UNKNOWN")
        self.assertFalse(m.domain_complete()); self.assertIn("unknown-required-target",m.unknown_required_targets)
    def test_DFI_005(self):
        m=done(); m.set_required_targets(["adapter"]); m.mark_target("adapter","ACKNOWLEDGED"); self.assertFalse(m.domain_complete())
    def test_DFI_006(self):
        m=done(); m.set_required_targets(["retained"]); m.mark_target("retained","POLICY_RETAINED"); self.assertFalse(m.domain_complete())
    def test_DFI_007(self):
        m=R3Model("m")
        with self.assertRaises(ContractViolation): m.authorize_and_suppress(auth(request_hash_matches=False),10,7,"op")
        self.assertEqual(m.lifecycle,Lifecycle.ACTIVE)
    def test_DFI_008(self):
        m=done(); a=m.start_attempt("a1"); b=m.start_attempt("a2")
        with self.assertRaises(ContractViolation): m.commit_stage("a1",a,"cleanup")
        m.commit_stage("a2",b,"cleanup")
    def test_DFI_009(self):
        m=done(); m.start_attempt("a1"); self.assertEqual(m.reconcile("UNKNOWN"),Reconciliation.UNKNOWN)
        with self.assertRaises(ContractViolation): m.retry("a2")
        m.reconcile("APPLIED"); m.retry("a2")
    def test_DFI_010(self):
        m=R3Model("m")
        with self.assertRaises(ContractViolation): m.authorize_and_suppress(auth(permission_epoch=6),10,7,"op")
        self.assertEqual(m.phase,Phase.FAILED)
    def test_DFI_011(self):
        m=done(); m.set_required_targets(["a"]); m.mark_target("a","SUCCEEDED"); self.assertTrue(m.domain_complete())
        rev=m.inventory_revision; m.set_required_targets(["a","b"]); self.assertGreater(m.inventory_revision,rev); self.assertFalse(m.domain_complete())
    def test_DFI_012(self):
        m=done(); m.begin_restore(0); self.assertFalse(m.restore_query_allowed())
        with self.assertRaises(ContractViolation): m.reconcile_restore(0,False)
        m.reconcile_restore(m.fence_generation,True); self.assertTrue(m.restore_query_allowed())
    def test_DFI_013(self):
        m=done(); self.assertFalse(m.read_allowed(m.fence_generation)); self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN)
    def test_DFI_014(self):
        m=done(); old=m.start_attempt("producer-old"); new=m.start_attempt("producer-new")
        with self.assertRaises(ContractViolation): m.commit_stage("producer-old",old,"publish")
        m.commit_stage("producer-new",new,"publish")
    def test_DFI_015(self):
        m=done(); self.assertFalse(m.read_allowed(m.fence_generation)); self.assertFalse(m.read_allowed(None))
    def test_DFI_016(self):
        m=done()
        with self.assertRaises(ContractViolation): m.promote_replica("lagging",m.fence_generation-1)
        m.promote_replica("current",m.fence_generation)
    def test_DFI_017(self):
        m=done(); self.assertFalse(m.read_allowed(m.fence_generation-1)); self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN)
    def test_DFI_018(self):
        m=R3Model("m"); self.assertEqual(m.lifecycle,Lifecycle.ACTIVE)
        m.authorize_and_suppress(auth(),10,7,"forget"); self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN)
    def test_DFI_019(self):
        m=done(); m.set_required_targets(["adapter"]); m.mark_target("adapter","ACKNOWLEDGED"); self.assertFalse(m.domain_complete())
    def test_DFI_020(self):
        m=done()
        with self.assertRaises(ContractViolation): m.forgotten_transition("AgentTelemetry")
        self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN)
    def test_DFI_021(self):
        m=R3Model("m"); m.phase=Phase.AUTHORIZED
        before=(m.lifecycle,m.fence_generation,m.phase,m.inventory_revision,dict(m.outbox))
        with self.assertRaises(ContractViolation): m.commit_suppression("op",fail_before_commit=True)
        self.assertEqual(before,(m.lifecycle,m.fence_generation,m.phase,m.inventory_revision,dict(m.outbox)))
        m.commit_suppression("op"); self.assertEqual(set(m.atomic_tuple),set(R3Model.ATOMIC_FIELDS))
    def test_DFI_022(self):
        m=done(); m.begin_restore(0); self.assertTrue(m.restore_quarantined); self.assertFalse(m.restore_query_allowed())

class OwnerIU011(unittest.TestCase):
    def _deny(self,**kw):
        m=R3Model("m")
        with self.assertRaises(ContractViolation): m.authorize_and_suppress(auth(**kw),10,7,"op")
        self.assertEqual(m.lifecycle,Lifecycle.ACTIVE); self.assertEqual(m.fence_generation,0)
    def test_T01(self): self._deny(issuer_known=False)
    def test_T02(self):
        for k in ("audience_matches","operation_matches","request_hash_matches","purpose_matches","scope_matches"):
            with self.subTest(k=k): self._deny(**{k:False})
    def test_T03(self): self._deny(expires_at=10); self._deny(not_before=11)
    def test_T04(self): self._deny(permission_epoch=6)
    def test_T05(self): self._deny(permission_epoch=6)
    def test_T06(self):
        m=done(); self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN); self.assertEqual(m.phase,Phase.SUPPRESSION_COMMITTED)
    def test_T07(self): self._deny(signature_valid=False)
    def test_T08(self): self._deny(delegation_current=False)
    def test_T09(self): self._deny(scope_matches=False)
    def test_T10(self): self._deny(issuer_known=False)
    def test_T11(self):
        m=done(); m.set_required_targets(["held"]); m.mark_target("held","POLICY_RETAINED"); self.assertFalse(m.domain_complete())
    def test_T12(self):
        m=done(); m.set_required_targets(["unknown"]); m.mark_target("unknown","UNKNOWN"); self.assertFalse(m.domain_complete())
    def test_T13(self):
        m=done(); m.set_required_targets(["a"]); m.mark_target("a","SUCCEEDED"); self.assertTrue(m.domain_complete())
        m.set_required_targets(["a","new"]); self.assertFalse(m.domain_complete())
    def test_T14(self):
        m=done(); m.set_required_targets(["held"]); m.mark_target("held","POLICY_RETAINED"); self.assertFalse(m.domain_complete())
    def test_T15(self): self.assertTrue(done().required_targets==set())
    def test_T16(self):
        m=done(); m.phase=Phase.CLEANUP; self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN); self.assertNotEqual(m.phase,Phase.COMPLETED)

class StorageFaults(unittest.TestCase):
    def test_STOR_01_concurrent_suppression_race(self):
        m=done()
        with self.assertRaises(ContractViolation): m.commit_suppression("duplicate")
        self.assertEqual(m.lifecycle,Lifecycle.FORGOTTEN)
    def test_STOR_02_replica_lag_failover(self):
        m=done()
        with self.assertRaises(ContractViolation): m.promote_replica("lag",m.fence_generation-1)
        self.assertFalse(m.read_allowed(None,False))
    def test_STOR_03_stale_worker_old_lease(self):
        m=done(); old=m.start_attempt("old"); new=m.start_attempt("new")
        with self.assertRaises(ContractViolation): m.commit_stage("old",old,"erase")
        m.commit_stage("new",new,"erase")
    def test_STOR_04_duplicate_events_outbox_replay(self):
        m=done(); self.assertFalse(m.replay_outbox("op")); self.assertTrue(m.replay_outbox("event")); self.assertFalse(m.replay_outbox("event"))
    def test_STOR_05_timeout_retry_reconciliation(self):
        m=done(); m.start_attempt("a1"); self.assertEqual(m.reconcile("UNKNOWN"),Reconciliation.UNKNOWN)
        with self.assertRaises(ContractViolation): m.retry("a2")
        m.reconcile("NOT_APPLIED"); m.retry("a2")
    def test_STOR_06_restore_isolation_reconciliation(self):
        m=done(); m.begin_restore(0); self.assertFalse(m.restore_query_allowed())
        m.reconcile_restore(m.fence_generation,True); self.assertTrue(m.restore_query_allowed())
    def test_STOR_07_missing_manifest_unknown(self):
        m=done(); m.set_backup_manifest(None); self.assertEqual(m.backup_coverage(),"UNKNOWN")
        m.set_backup_manifest({"authenticated":True,"copies":[]}); self.assertEqual(m.backup_coverage(),"UNKNOWN")

if __name__=="__main__": unittest.main(verbosity=2)
