import copy, hashlib, hmac, tempfile, unittest
import portable_exchange
from pathlib import Path
from portable_exchange import (Denied, JsonFileAdapter, SQLiteAdapter, Principal,
    TestAuthority, fixture_grant, make_record, migrate_v1_to_v2, rollback_v2_to_v1)

class PortableExchangeConformance(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.auth=TestAuthority(); self.principal=Principal("tenant.red","workspace.blue","agent.alpha","provider-json","model-alpha-v3")
        self.a=JsonFileAdapter(Path(self.tmp.name)/"a.json",self.auth,self.principal)
        self.b=SQLiteAdapter(Path(self.tmp.name)/"b.sqlite",self.auth,self.principal)
        self.record=make_record(); self.token=fixture_grant(self.auth); self.a.write(self.record,self.token)
    def test_contract_version_is_stable(self): self.assertEqual(self.a.contract_version,"ai-memory-portable-exchange/1.0")
    def test_json_sqlite_roundtrip_is_byte_identical(self):
        e=self.a.export(self.record.record_id,self.token); self.b.import_record(e,self.token); self.assertEqual(e,self.b.export(self.record.record_id,self.token))
    def test_three_leg_roundtrip_preserves_identity_lineage_lifecycle_provenance(self):
        e=self.a.export(self.record.record_id,self.token); self.b.import_record(e,self.token); e2=self.b.export(self.record.record_id,self.token); self.a.import_record(e2,self.token)
        r=self.a.read(self.record.record_id,self.token)
        self.assertEqual((r.record_id,r.resource,r.source_agent,r.source_provider,r.source_model,r.lineage,r.lifecycle,r.provenance),
          (self.record.record_id,self.record.resource,self.record.source_agent,self.record.source_provider,self.record.source_model,self.record.lineage,self.record.lifecycle,self.record.provenance))
    def test_provider_substitution_keeps_origin_attribution(self):
        self.b.import_record(self.a.export(self.record.record_id,self.token),self.token)
        r=self.b.read(self.record.record_id,self.token); self.assertEqual(r.source_provider,"provider-json"); self.assertEqual(self.b.provider_id,"provider-sqlite")
    def test_bad_signature_denied(self):
        t=copy.deepcopy(self.token); t["signature"]="0"*64
        with self.assertRaisesRegex(Denied,"GRANT_SIGNATURE_INVALID"): self.a.read(self.record.record_id,t)
    def test_untrusted_issuer_denied(self):
        t=copy.deepcopy(self.token); t["claims"]["issuer"]="attacker"
        with self.assertRaises(Denied): self.a.read(self.record.record_id,t)
    def test_wrong_tenant_denied(self):
        p=Principal("tenant.other","workspace.blue","agent.alpha","provider-json","model-alpha-v3")
        x=JsonFileAdapter(self.a.path,self.auth,p)
        with self.assertRaises(Denied): x.read(self.record.record_id,self.token)
    def test_wrong_workspace_denied(self):
        p=Principal("tenant.red","workspace.other","agent.alpha","provider-json","model-alpha-v3")
        x=JsonFileAdapter(self.a.path,self.auth,p)
        with self.assertRaises(Denied): x.read(self.record.record_id,self.token)
    def test_wrong_agent_denied(self):
        p=Principal("tenant.red","workspace.blue","agent.evil","provider-json","model-alpha-v3")
        x=JsonFileAdapter(self.a.path,self.auth,p)
        with self.assertRaises(Denied): x.read(self.record.record_id,self.token)
    def test_wrong_audience_denied(self):
        t=fixture_grant(self.auth); t["claims"]["audience"]="agent.evil"
        with self.assertRaises(Denied): self.a.read(self.record.record_id,t)
    def test_wrong_resource_denied(self):
        t=fixture_grant(self.auth,resource="memory.other")
        with self.assertRaises(Denied): self.a.read(self.record.record_id,t)
    def test_read_scope_required(self):
        t=fixture_grant(self.auth,actions=["write"])
        with self.assertRaisesRegex(Denied,"ACTION_NOT_GRANTED"): self.a.read(self.record.record_id,t)
    def test_write_scope_required(self):
        t=fixture_grant(self.auth,actions=["read"])
        with self.assertRaisesRegex(Denied,"ACTION_NOT_GRANTED"): self.a.write(self.record,t)
    def test_import_scope_required(self):
        t=fixture_grant(self.auth,actions=["read","write"])
        with self.assertRaisesRegex(Denied,"ACTION_NOT_GRANTED"): self.b.import_record(self.a.export(self.record.record_id,self.token),t)
    def test_share_scope_required(self):
        t=fixture_grant(self.auth,actions=["read","export"])
        with self.assertRaisesRegex(Denied,"ACTION_NOT_GRANTED"): self.a.share(self.record.record_id,t)
    def test_export_requires_export_and_read(self):
        t=fixture_grant(self.auth,actions=["read"])
        with self.assertRaises(Denied): self.a.export(self.record.record_id,t)
    def test_revocation_enforced_after_issuance(self):
        self.auth.revoke(self.token["claims"]["grant_id"])
        with self.assertRaisesRegex(Denied,"GRANT_REVOKED"): self.a.read(self.record.record_id,self.token)
    def test_expired_grant_denied(self):
        t=self.auth.issue(tenant="tenant.red",workspace="workspace.blue",agent="agent.alpha",audience="agent.alpha",resource="memory.demo.001",actions=["read"],expires_at=1)
        with self.assertRaisesRegex(Denied,"GRANT_EXPIRED"): self.a.read(self.record.record_id,t)
    def test_delegation_within_scope_accepted(self):
        parent=fixture_grant(self.auth,agent="agent.delegate",actions=["read","write","import","export","share","delegate"])
        child=fixture_grant(self.auth,actions=["read","write","import","export","share"],delegation_chain=(self.auth.issuer,"agent.delegate","agent.alpha"),parent_grant=parent["claims"]["grant_id"])
        self.assertEqual(self.a.read(self.record.record_id,child),self.record)
    def test_delegation_parent_agent_mismatch_rejected_at_issuance(self):
        parent=fixture_grant(self.auth,agent="agent.parent",actions=["read","delegate"])
        with self.assertRaisesRegex(ValueError,"DELEGATION_PARENT_AGENT_MISMATCH"):
            fixture_grant(self.auth,agent="agent.alpha",actions=["read"],
                delegation_chain=(self.auth.issuer,"agent.attacker","agent.alpha"),
                parent_grant=parent["claims"]["grant_id"])
    def test_tampered_delegation_chain_rejected_after_signature_recomputed(self):
        parent=fixture_grant(self.auth,agent="agent.parent",actions=["read","delegate"])
        child=fixture_grant(self.auth,agent="agent.alpha",actions=["read"],
            delegation_chain=(self.auth.issuer,"agent.parent","agent.alpha"),
            parent_grant=parent["claims"]["grant_id"])
        forged=copy.deepcopy(child)
        forged["claims"]["delegation_chain"][-2]="agent.attacker"
        forged["signature"]=hmac.new(self.auth._key,portable_exchange.canonical(forged["claims"]),hashlib.sha256).hexdigest()
        with self.assertRaisesRegex(Denied,"DELEGATION_PARENT_AGENT_MISMATCH"):
            self.auth.verify(forged,self.principal,self.record.resource,"read")
    def test_delegation_scope_escalation_rejected(self):
        parent=fixture_grant(self.auth,agent="agent.parent",actions=["read","delegate"])
        with self.assertRaisesRegex(ValueError,"DELEGATION_ACTION_ESCALATION"):
            fixture_grant(self.auth,agent="agent.child",actions=["read","write"],
                delegation_chain=(self.auth.issuer,"agent.parent","agent.child"),
                parent_grant=parent["claims"]["grant_id"])
    def test_delegation_parent_revocation_denied(self):
        parent=fixture_grant(self.auth,agent="agent.parent",actions=["read","delegate"])
        child=fixture_grant(self.auth,agent="agent.child",actions=["read"],
            delegation_chain=(self.auth.issuer,"agent.parent","agent.child"),
            parent_grant=parent["claims"]["grant_id"])
        self.auth.revoke(parent["claims"]["grant_id"])
        with self.assertRaisesRegex(Denied,"DELEGATION_PARENT_INVALID"): self.a.read(self.record.record_id,child)
    def test_tampered_envelope_denied(self):
        e=self.a.export(self.record.record_id,self.token); e["record"]["content"]="evil"
        with self.assertRaisesRegex(ValueError,"EXCHANGE_DIGEST_MISMATCH"): self.b.import_record(e,self.token)
    def test_confused_deputy_cross_tenant_import_denied(self):
        other=Principal("tenant.other","workspace.blue","agent.alpha","provider-sqlite","model-x")
        deputy=SQLiteAdapter(Path(self.tmp.name)/"deputy.sqlite",self.auth,other)
        with self.assertRaises(Denied): deputy.import_record(self.a.export(self.record.record_id,self.token),self.token)
    def test_confused_deputy_share_cannot_widen_audience(self):
        wrong=fixture_grant(self.auth,agent="agent.evil")
        with self.assertRaises(Denied): self.a.share(self.record.record_id,wrong)
    def test_forgotten_record_cannot_be_exported_or_shared(self):
        forgotten=make_record().__class__(**{**self.record.__dict__,"lifecycle":"forgotten"}); self.a._put(forgotten)
        with self.assertRaisesRegex(Denied,"RECORD_NOT_EXPORTABLE"): self.a.export(forgotten.record_id,self.token)
        with self.assertRaisesRegex(Denied,"RECORD_NOT_EXPORTABLE"): self.a.share(forgotten.record_id,self.token)
    def test_retracted_lifecycle_roundtrip_preserved(self):
        r=make_record().__class__(**{**self.record.__dict__,"lifecycle":"retracted"}); self.a._put(r)
        e=self.a.export(r.record_id,self.token); self.b.import_record(e,self.token); self.assertEqual(self.b.read(r.record_id,self.token).lifecycle,"retracted")
    def test_migration_rollback_restores_exact_v1_snapshot(self):
        e=self.a.export(self.record.record_id,self.token); migrated=migrate_v1_to_v2(e); self.assertEqual(migrated["schema_version"],2)
        self.assertEqual(rollback_v2_to_v1(migrated,e),e)
    def test_migration_corrupt_backup_rejected(self):
        e=self.a.export(self.record.record_id,self.token); m=migrate_v1_to_v2(e); bad=copy.deepcopy(e); bad["record"]["content"]="changed"
        with self.assertRaisesRegex(ValueError,"ROLLBACK_BACKUP_CORRUPT"): rollback_v2_to_v1(m,bad)
    def test_import_unknown_schema_rejected(self):
        e=self.a.export(self.record.record_id,self.token); e["schema_version"]=99
        with self.assertRaisesRegex(ValueError,"UNSUPPORTED_EXCHANGE_CONTRACT"): self.b.import_record(e,self.token)

if __name__ == "__main__": unittest.main(verbosity=2)
