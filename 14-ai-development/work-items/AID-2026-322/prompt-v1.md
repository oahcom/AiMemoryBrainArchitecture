---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-322/evidence.md"
        - "14-ai-development/work-items/AID-2026-322/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "The governance frontmatter was prepended by the operator to the message that was sent. Accordingly, this committed snapshot contains the executed message plus this governance frontmatter, not the raw message. The manifest digest pins these committed file bytes, consistent with the repository convention also used by AID-2026-290. Provenance remains NOT_VERIFIED."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Informative executed-message snapshot for AID-2026-322, including the governance frontmatter prepended by the operator. The committed snapshot is not the raw message; its manifest digest pins the committed bytes. Provenance remains NOT_VERIFIED."
    canonical_scope_id: "ai-development/aid-2026-322-executed-message-snapshot"
    canonical_scope_keywords:
      - "AID-2026-322"
      - "executed message"
      - "prompt snapshot"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

You are the implementation session for a documentation-governance work item in the repository
oahcom/AiMemoryBrainArchitecture. I am the operator: I execute mechanically and do not author content.
Everything you write will be applied verbatim by a script, so it must be exact.

# 0. Hard constraints (repository rules; violating one turns CI red)

- New work item directory: `14-ai-development/work-items/AID-2026-322/` with exactly four files:
  `manifest.yaml`, `prompt-v1.md`, `evidence.md`, `session-evidence.md`.
- `prompt-v1.md` is the text of this message. Do not author it; I will place this exact prompt there.
  Therefore do not write a digest of `prompt-v1.md` anywhere in `prompt-v1.md`.
- `manifest.yaml` `session_evidence[0]` must carry, with these exact keys:
  `role`, `issue_refs`, `implementing_ai_session` (a single token, no spaces/semicolons/commas/pluses),
  `executed_prompt_snapshot_file`, `executed_prompt_sha256`, `executed_prompt_bytes`,
  `executed_prompt_provenance` (VERIFIED | NOT_VERIFIED | NOT_AVAILABLE), `session_reference_status`
  (e.g. RECORDED), `session_evidence_ref`.
  Because `prompt-v1.md` does not exist yet when you write the manifest, put the literal placeholders
  `__PROMPT_SHA256__` and `__PROMPT_BYTES__` in those two fields. I replace them with the measured
  values of the committed `prompt-v1.md` bytes after writing it. Do not invent a digest.
- `base_commit_sha` must be the 40-hex string `229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c`.
- `INDEX.md` gets exactly one new row, inserted after the table header block. En dashes in that file
  are U+2014 (`—`), never `--`. A duplicate row is rejected by T-04.
- The three `.md` files each need a `document_metadata` frontmatter block. Copy the shape of
  `AID-2026-290/evidence.md` exactly (I paste its frontmatter below). Requirements that are checked:
  `authority.canonical_scope_id` must differ across the three files; after the `authority:` block there
  must be a `bilingual_counterpart:` block with keys `source`, `en`, `zh-CN` (values may be null) and
  `steward: "user-authorized operator (delegated by account owner)"`;
  `last_verified_date` is `"2026-11-27"`.
- `session-evidence.md` must contain the literal section headings `## Session role`,
  `## Actual AI input`, `## AI-visible output`, each non-empty. `## Session identity` does not satisfy
  the check.
- The pull request body will carry, verbatim:
  `- Work Item ID: AID-2026-322`, `## Owning Issue`, `#1318`, `## Related issue(s)`, `#1318`,
  `## AI-assisted work`, `YES`, `## Session evidence reference(s)`,
  `` `14-ai-development/work-items/AID-2026-322/session-evidence.md` ``, `## Per-Issue AI session evidence`
  and a three-column table whose Issue row is `LEGACY_UNDECLARED` / `N/A`
  (issue #1318 was created 2026-11-26, before 2026-12-01, and its body contains no AI-assisted-work
  declaration).
- Scope discipline: this pull request carries ONE invariant — "a declared prompt pin must describe a
  committed byte". It must not add a checker, a workflow, a schema change, or re-introduce the removed
  `approval_scope.included_sections` / `included_assets` keys. Anything else you find is recorded as a
  finding, not fixed.

# 1. What I measured, on `main` = 229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c (2026-11-27)

Read-only script, `sha256` of the raw bytes of each pinned file, compared against the manifest field.
Shape A = `session_evidence[*].executed_prompt_sha256` / `executed_prompt_bytes` against
`executed_prompt_snapshot_file`. Shape B = top-level `prompt_sha256` / `prompt_bytes` against
`prompt_file`.

```text
worktree: D:\code\_lcs\fix-1318
manifests parsed: 127

[A] session_evidence executed_prompt_* : MATCH 54  MISMATCH 42  MISSING/UNPINNED 1
[B] top-level prompt_sha256/prompt_bytes: MATCH 64  MISMATCH 0  MISSING 0  NO prompt_file 4

[A] MISMATCH (42):
  AID-2026-059[0]  14-ai-development/work-items/AID-2026-059/prompt-v1.md
      declared 65474e7f0927d2dfeaad33814fdbd7d576635cc8a0e8d2a3a7441e3a65ab7317 / 3866   actual 4881d6292e96154d5f7364816ae3e9977365e09b88e8475f4dd9d655e3e34a8c / 3808   delta -58
  AID-2026-059[1]  14-ai-development/work-items/AID-2026-059/prompt-1015.md
      declared 245dbfc39ca8b20cec30bba392c4b2f5e0db383b404eb4e8e10a8f7cee899f46 / 7986   actual 2be1e84c9fc262066e687bf21a57d80a090fed73d3c6765f26fc6fc02d3c0b51 / 7928   delta -58
  AID-2026-059[2]  14-ai-development/work-items/AID-2026-059/prompt-1026-v1.md
      declared 25058389340c796a557746ae5ed90cf73cada98998e62da1692bb5ce4a3e4bd9 / 4811   actual 8ca8bfc89774fa728e1671808510af4aa9def9b9860a9cc9016c5ca8bba87ea5 / 4753   delta -58
  AID-2026-059[3]  14-ai-development/work-items/AID-2026-059/prompt-1042-1048-v1.md
      declared ceae6530d70c60803b58ba91a3f5ed28671a525bcc640c32aa8f020d3defaffd / 6507   actual 8aa0b29ce5ce620c77ac3621531b4b8df908010675f5486672d056345eb76b11 / 6449   delta -58
  AID-2026-059[4]  14-ai-development/work-items/AID-2026-059/prompt-1029-1076-v1.md
      declared f0a315582ba51212758d82c6dfacedaaa676575f2b0ffcec4170fbded05f229e / 9166   actual 81e070af08045cec4635201b99861bab00a2ffa7e1caafab3342608d0adde22a / 9108   delta -58
  AID-2026-059[5]  14-ai-development/work-items/AID-2026-059/prompt-1223-v1.md
      declared 5de7adc61dcb6659b16a4da5e35826cd635f616ad664654d327c9a1836cade95 / 3961   actual 642f8c20076565ac083a5fd0873c39890238659dac101564aced1c4d328385f8 / 3903   delta -58
  AID-2026-061[0]  14-ai-development/work-items/AID-2026-061/prompt-v1.md
      declared 7ea255ab98c081d797820fa48d7744d2209eb285c0bda17cee6c4f22d66f0b81 / 18776   actual 6c0a9cc7e47f2e30505f8b765d08663b1c032cda128f7fb79a148152cff6e3cd / 18718   delta -58
  AID-2026-062[0]  14-ai-development/work-items/AID-2026-062/prompt-v1.md
      declared 3f57662579cfe90c230585b7ab7ff87c10e0074df167ac1d6c79e5fe8b9766de / 2927   actual 96358a3a9af4452d0b51b13f3483f319d93b38eb2ac414eb39d674a0a61c6c42 / 2869   delta -58
  AID-2026-063[0]  14-ai-development/work-items/AID-2026-063/prompt-v1.md
      declared 4cf341c81da42e332e7e352a47f6fa8eb9e82e2b266134dbe2497b874629efd8 / 2691   actual 411a0be8d6e73a4953f86740b60418db81bb96da7be3f8696a82bf880781b4b5 / 2633   delta -58
  AID-2026-064[0]  14-ai-development/work-items/AID-2026-064/prompt-v1.md
      declared 57decec9de8752e099d6a72588fcdd00904bffbe4cecb614ddf9c34a441fdbb8 / 7188   actual f169ed7738a1ed56a67e371ffdf57de944c4db9b344b9732001e51edfe052672 / 7130   delta -58
  AID-2026-066[0]  14-ai-development/work-items/AID-2026-066/prompt-v1.md
      declared 1ae516e747ae3417d9a34cc5fc870128da2efbd603d4d958fceaf18a3791c6ae / 5921   actual d6afe924427aebf974c86a742bee679a3ca6cc247d58d691297ede9002619c6c / 5863   delta -58
  AID-2026-067[0]  14-ai-development/work-items/AID-2026-067/prompt-v1.md
      declared 07b49d7fa41ec6a5e9025dd3440e9f181654c8903288aa0d430d9324df5ac0da / 5261   actual c73aa6e35fddb745b7925d6b350fb661d538beb3e5f9b975c89d1e1bc4906ab5 / 5203   delta -58
  AID-2026-068[0]  14-ai-development/work-items/AID-2026-068/prompt-v1.md
      declared 7d55d2011f931207ec4d63a6d0a94715a82ab16365cef390cf7423f8e7ab5a31 / 6031   actual 9a1e0e823d200aedebfefeb1f4bb26de3cbd1569938e6625f56a5e6599eb71f5 / 5973   delta -58
  AID-2026-069[0]  14-ai-development/work-items/AID-2026-069/prompt-v1.md
      declared 360c3273a8e6b28cefe583aabe9c5f3d119e94212735c2fae626bbad72816db6 / 6062   actual 12a7ebc07e9d2f048157caa4f56e3ba0b18b9078290316816c83d361451e4c7e / 6004   delta -58
  AID-2026-070[0]  14-ai-development/work-items/AID-2026-070/prompt-v1.md
      declared b0013ed25ebdf4c5a0cc200551d9e89edf6993138828527abb2fab137fda024a / 6371   actual 6df00b015153a2105dc52f131d2b58c2b8207511e001ab00d572a462fc030d31 / 6313   delta -58
  AID-2026-071[0]  14-ai-development/work-items/AID-2026-071/prompt-v1.md
      declared 4c735edd42b80f43d04c26fdbbcc8e29662d96456394fbf5417a8386d88609c7 / 4303   actual 8080149aa3a0a9ec3f68071b25e62d856f4f55d9e36acfab245d0903ff631af5 / 4245   delta -58
  AID-2026-072[0]  14-ai-development/work-items/AID-2026-072/prompt-v1.md
      declared 1c8f58cff7d248f7bd3a7b87aff836a2f497e57512e64376c1aa778085b67ea7 / 8623   actual 5e29f0695537e19bbf2e64ee4bf4fe85d03e732126f5d7dec92b2cacacc67a8f / 8565   delta -58
  AID-2026-073[0]  14-ai-development/work-items/AID-2026-073/prompt-v1.md
      declared 08eb2369f7f6228adbbb4dfc4df88b6ceaf9381be1a5d4bf90ad61ec32145c1a / 5089   actual 278e8a975be335e6904af591b7f45367f34204ed4a9d33f81a19d6cfa5b3a7cd / 5031   delta -58
  AID-2026-074[0]  14-ai-development/work-items/AID-2026-074/prompt-v1.md
      declared 78044dfbc68873766fc6773768099a2a7b5b08d67594ca5bf09decbeb991a915 / 3967   actual b5c8c5470850be9e58f23f55a31ee0dd7b2d6e560f7b12486c2a968f41f802fe / 3909   delta -58
  AID-2026-075[0]  14-ai-development/work-items/AID-2026-075/prompt-v1.md
      declared e85f9ae067792717fbe989322dfee804091c776b2ad4317a03f2a95970ee4d83 / 4961   actual 0a1b6f82484207b81736a230ef51507de1dc83ed90bfcbd4fdd19b9554a2d0df / 4903   delta -58
  AID-2026-076[0]  14-ai-development/work-items/AID-2026-076/prompt-v1.md
      declared 06ee5615ab9fc696afa769183141d637ec5287776b60cc0b06afd117a024f6b2 / 5525   actual 6974846995878c7d76dac9f7fad320bc26613e598d48b68f023564dd66a424c0 / 5467   delta -58
  AID-2026-077[0]  14-ai-development/work-items/AID-2026-077/prompt-v1.md
      declared 0339f07cd6bd5dbd5211b45066ee5c1bba78d4768d763beeac4ce24aa368a931 / 5621   actual 9de48039bb47ac8320d565205e67616a1345858d0f29c8e8e850d368fe134aee / 5563   delta -58
  AID-2026-078[0]  14-ai-development/work-items/AID-2026-078/prompt-v1.md
      declared c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2 / 7533   actual cb9890fc1c4e2ff07ec808f2f1401bc5082b3c3e4e89e5dac0450aa1a81eb5d6 / 7475   delta -58
  AID-2026-078[1]  14-ai-development/work-items/AID-2026-078/prompt-v1.md
      declared c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2 / 7533   actual cb9890fc1c4e2ff07ec808f2f1401bc5082b3c3e4e89e5dac0450aa1a81eb5d6 / 7475   delta -58
  AID-2026-079[0]  14-ai-development/work-items/AID-2026-079/prompt-v1.md
      declared a2d216ee647954b02a6487349716191403e67171d63a82acd7ab15c9feafc81f / 5790   actual af8ad57de5eddf104c3d1ff4eb40e377e352c8ab62e98f86d422139b3b5e03a8 / 5732   delta -58
  AID-2026-080[0]  14-ai-development/work-items/AID-2026-080/prompt-v1.md
      declared 08f5e42efdef2c3380056fd8528cf057d6d2a7b25c366566a8599e2aff4df19a / 9932   actual c071d0ee5978785a09ff5c9b902e5c3959f4bf7f611e7e35ab36d4c40996c2b8 / 9874   delta -58
  AID-2026-081[0]  14-ai-development/work-items/AID-2026-081/prompt-v1.md
      declared 7b761550e7cf5a64a3000b908b0a838e4e316b6db69f72d50d890c475f1eb3de / 4428   actual a0272451912214b9608f4050f2168f22fece00010de305fca039ac892ac44f0c / 4370   delta -58
  AID-2026-082[0]  14-ai-development/work-items/AID-2026-082/prompt-v1.md
      declared 79bcd0738f9c0f0c5b3dcf05675629c12a7eb51bcaaff0e184ba1ec93e31b7cb / 5831   actual ff3eccdc7154cd2f95858c25215ba4198e1a96a2210186b0784e975dd5e7c5cd / 5773   delta -58
  AID-2026-084[0]  14-ai-development/work-items/AID-2026-084/prompt-v1.md
      declared acdd40d2b2b2357ecfea7411122b146e43d4daab7fd8230bc32ba96009c86b55 / 4775   actual 3e02da52ac4560ec1d8a2eca1b88a9102354401e14377b8476961740c05d6745 / 4717   delta -58
  AID-2026-085[0]  14-ai-development/work-items/AID-2026-085/prompt-v1.md
      declared 17a8cd7583b88aaa348024bf445c9c3bbb86e463c38e49495df9d07edbb3f35e / 7689   actual 80a1ecb80d093c69b3a1921eb7146852df44a0bf4aa5da775f8907fd4f5447f9 / 7631   delta -58
  AID-2026-089[0]  14-ai-development/work-items/AID-2026-089/prompt-v1.md
      declared 7682d9287605c24109c6502963b0dd73f133a46b608ba495bc0a0da10292a903 / 4258   actual e75f603f054dbd8cc433f54c1f125ee31d60b46653caf8f76c63703756409064 / 4200   delta -58
  AID-2026-090[0]  14-ai-development/work-items/AID-2026-090/prompt-v1.md
      declared 32e5a263ab34d2806110ba09500c3b750613360c20cb082eb1e69fd3cd3fe3a3 / 2034   actual 79288220c2196f5af81e0e5a62bf2264b6874b8814614757e08c61764b808d6c / 1976   delta -58
  AID-2026-091[0]  14-ai-development/work-items/AID-2026-091/prompt-v1.md
      declared 11b2d92aa94d1af88ee403def9fa2977bb7cee8c9c32ff957fbc4c06e91ac5d8 / 2058   actual a531954b26c831a555486684e9130eedd1bcd57152ac55ed89ea3010dc9e88ac / 2000   delta -58
  AID-2026-094[0]  14-ai-development/work-items/AID-2026-094/prompt-v1.md
      declared 81644f71a94a155c6162f102dac6fe46670127b8c0ecf134c9321245096ba2c5 / 6972   actual 766d5bd3f8ed61c03ac6630f04ad63daecf49d1751ccd2e1e585d5bad95b6d4e / 6914   delta -58
  AID-2026-096[0]  14-ai-development/work-items/AID-2026-096/prompt-v1.md
      declared 0ebc78aefd4d29d66ee6a77cf760a590eb67c70a1e215ef384b8bc41aee128ca / 2757   actual 13b231991e54dce2b485a1709d4bce03b527e43f29b66a876c53235032e52771 / 2699   delta -58
  AID-2026-097[0]  14-ai-development/work-items/AID-2026-097/prompt-v1.md
      declared 4e3dbbd35d002403849329a14d2f5c6357f695ea835327ff56c151cde00fed56 / 4283   actual 70f4eb79f8c4203f2d657e28c715d390a5a15ac2b54366c1db5e460302554d91 / 4225   delta -58
  AID-2026-098[0]  14-ai-development/work-items/AID-2026-098/prompt-v1.md
      declared f9b83206744d38bfaa782e47d34ff11e696f2cd04c1c31b4e6fe5b0a1843cc06 / 3241   actual 6b6c7407e27773e4420cad0148c574735ead00f25ef7e36282a64613831a0b1c / 3183   delta -58
  AID-2026-099[0]  14-ai-development/work-items/AID-2026-099/prompt-v1.md
      declared eed5a5b7cee82bc4893ed57a93d11957b86926700befa91661da40fe8c645c73 / 2418   actual 53abd3e3119e4c7eb486b70ce9e90b363d91317ddfd12bf4952526248f3a56e3 / 2360   delta -58
  AID-2026-101[0]  14-ai-development/work-items/AID-2026-101/prompt-v1.md
      declared 89ac65f2d58e187451b7c0a98648d0dd4352e3dac79f521b8029b0432f7e94c1 / 4470   actual de3b9b80c952096d7ba14b5226517eed8c14b61593328f80d3a3cf3f1122fc94 / 4412   delta -58
  AID-2026-102[0]  14-ai-development/work-items/AID-2026-102/prompt-v1.md
      declared df3c53282d858ecc7302ba86b4fb419bf6a31c8030d30cee256b64840b4e4e7a / 4470   actual 468a1d4fd8f43d81c8ffba081afd46497b54a2b427849838946163785716072d / 4412   delta -58
  AID-2026-186[0]  14-ai-development/work-items/AID-2026-186/prompt-v1-original.source.txt
      declared a421889d3654e49e2247b7207faef0113c188c0e28c7dd0caeea91127c21d67e / 2285   actual 698aee8404b032926c4c485c57347bf31c63111a1ee5bc6c9e0e49a56d8a7f50 / 2340   delta +55
  AID-2026-241[0]  14-ai-development/work-items/AID-2026-241/prompt-v1-original.source.txt
      declared 5c8f02062568720bb9132b27bdb3d6a4c9ac9fbb603d0c42a4818f6c2105002a / 6983   actual 90e14513ca0b8ab4a2bdb220d93461942852142a07955f764be7ccf53fda4c93 / 7130   delta +147

[B] MISMATCH (0):

[A] MISSING/UNPINNED (1):
  AID-2026-261[0]  file=14-ai-development/work-items/AID-2026-261/prompt-v1.md  sha=0000000000000000000000000000000000000000000000000000000000000000 bytes=0

[B] MISSING (0): []
[B] NO prompt_file (4): AID-2026-001, AID-2026-003(NOT_VERIFIED), AID-2026-004, AID-2026-064

json: audit1318-before.json  (42 records)
```

The full per-entry repin table (manifest line numbers included):

```text
rows: 42  manifests: 36  dup-sha groups: [('AID-2026-078', 'c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2')]

AID-2026-059[0]  14-ai-development/work-items/AID-2026-059/prompt-v1.md
    manifest lines: sha@136 bytes@137
    OLD 65474e7f0927d2dfeaad33814fdbd7d576635cc8a0e8d2a3a7441e3a65ab7317 / 3866
    NEW 4881d6292e96154d5f7364816ae3e9977365e09b88e8475f4dd9d655e3e34a8c / 3808   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-799-orchestrator
AID-2026-059[1]  14-ai-development/work-items/AID-2026-059/prompt-1015.md
    manifest lines: sha@145 bytes@146
    OLD 245dbfc39ca8b20cec30bba392c4b2f5e0db383b404eb4e8e10a8f7cee899f46 / 7986
    NEW 2be1e84c9fc262066e687bf21a57d80a090fed73d3c6765f26fc6fc02d3c0b51 / 7928   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-1015-workflow-shape-guard
AID-2026-059[2]  14-ai-development/work-items/AID-2026-059/prompt-1026-v1.md
    manifest lines: sha@160 bytes@161
    OLD 25058389340c796a557746ae5ed90cf73cada98998e62da1692bb5ce4a3e4bd9 / 4811
    NEW 8ca8bfc89774fa728e1671808510af4aa9def9b9860a9cc9016c5ca8bba87ea5 / 4753   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-1026-validate-ordering
AID-2026-059[3]  14-ai-development/work-items/AID-2026-059/prompt-1042-1048-v1.md
    manifest lines: sha@178 bytes@179
    OLD ceae6530d70c60803b58ba91a3f5ed28671a525bcc640c32aa8f020d3defaffd / 6507
    NEW 8aa0b29ce5ce620c77ac3621531b4b8df908010675f5486672d056345eb76b11 / 6449   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-1042-1048-residuals
AID-2026-059[4]  14-ai-development/work-items/AID-2026-059/prompt-1029-1076-v1.md
    manifest lines: sha@203 bytes@204
    OLD f0a315582ba51212758d82c6dfacedaaa676575f2b0ffcec4170fbded05f229e / 9166
    NEW 81e070af08045cec4635201b99861bab00a2ffa7e1caafab3342608d0adde22a / 9108   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-1029-1076-residuals
AID-2026-059[5]  14-ai-development/work-items/AID-2026-059/prompt-1223-v1.md
    manifest lines: sha@221 bytes@222
    OLD 5de7adc61dcb6659b16a4da5e35826cd635f616ad664654d327c9a1836cade95 / 3961
    NEW 642f8c20076565ac083a5fd0873c39890238659dac101564aced1c4d328385f8 / 3903   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-1223-duplicate-blindness
AID-2026-061[0]  14-ai-development/work-items/AID-2026-061/prompt-v1.md
    manifest lines: sha@82 bytes@83
    OLD 7ea255ab98c081d797820fa48d7744d2209eb285c0bda17cee6c4f22d66f0b81 / 18776
    NEW 6c0a9cc7e47f2e30505f8b765d08663b1c032cda128f7fb79a148152cff6e3cd / 18718   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-req01-r32
AID-2026-062[0]  14-ai-development/work-items/AID-2026-062/prompt-v1.md
    manifest lines: sha@74 bytes@75
    OLD 3f57662579cfe90c230585b7ab7ff87c10e0074df167ac1d6c79e5fe8b9766de / 2927
    NEW 96358a3a9af4452d0b51b13f3483f319d93b38eb2ac414eb39d674a0a61c6c42 / 2869   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-req01-r34
AID-2026-063[0]  14-ai-development/work-items/AID-2026-063/prompt-v1.md
    manifest lines: sha@74 bytes@75
    OLD 4cf341c81da42e332e7e352a47f6fa8eb9e82e2b266134dbe2497b874629efd8 / 2691
    NEW 411a0be8d6e73a4953f86740b60418db81bb96da7be3f8696a82bf880781b4b5 / 2633   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-req01-r35
AID-2026-064[0]  14-ai-development/work-items/AID-2026-064/prompt-v1.md
    manifest lines: sha@100 bytes@101
    OLD 57decec9de8752e099d6a72588fcdd00904bffbe4cecb614ddf9c34a441fdbb8 / 7188
    NEW f169ed7738a1ed56a67e371ffdf57de944c4db9b344b9732001e51edfe052672 / 7130   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=a955
AID-2026-066[0]  14-ai-development/work-items/AID-2026-066/prompt-v1.md
    manifest lines: sha@89 bytes@90
    OLD 1ae516e747ae3417d9a34cc5fc870128da2efbd603d4d958fceaf18a3791c6ae / 5921
    NEW d6afe924427aebf974c86a742bee679a3ca6cc247d58d691297ede9002619c6c / 5863   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-r44-reg-b
AID-2026-067[0]  14-ai-development/work-items/AID-2026-067/prompt-v1.md
    manifest lines: sha@77 bytes@78
    OLD 07b49d7fa41ec6a5e9025dd3440e9f181654c8903288aa0d430d9324df5ac0da / 5261
    NEW c73aa6e35fddb745b7925d6b350fb661d538beb3e5f9b975c89d1e1bc4906ab5 / 5203   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-r44-reg-b
AID-2026-068[0]  14-ai-development/work-items/AID-2026-068/prompt-v1.md
    manifest lines: sha@85 bytes@86
    OLD 7d55d2011f931207ec4d63a6d0a94715a82ab16365cef390cf7423f8e7ab5a31 / 6031
    NEW 9a1e0e823d200aedebfefeb1f4bb26de3cbd1569938e6625f56a5e6599eb71f5 / 5973   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-r44-reg-b
AID-2026-069[0]  14-ai-development/work-items/AID-2026-069/prompt-v1.md
    manifest lines: sha@78 bytes@79
    OLD 360c3273a8e6b28cefe583aabe9c5f3d119e94212735c2fae626bbad72816db6 / 6062
    NEW 12a7ebc07e9d2f048157caa4f56e3ba0b18b9078290316816c83d361451e4c7e / 6004   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-r45-coordinator
AID-2026-070[0]  14-ai-development/work-items/AID-2026-070/prompt-v1.md
    manifest lines: sha@82 bytes@83
    OLD b0013ed25ebdf4c5a0cc200551d9e89edf6993138828527abb2fab137fda024a / 6371
    NEW 6df00b015153a2105dc52f131d2b58c2b8207511e001ab00d572a462fc030d31 / 6313   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-r45-coordinator
AID-2026-071[0]  14-ai-development/work-items/AID-2026-071/prompt-v1.md
    manifest lines: sha@98 bytes@99
    OLD 4c735edd42b80f43d04c26fdbbcc8e29662d96456394fbf5417a8386d88609c7 / 4303
    NEW 8080149aa3a0a9ec3f68071b25e62d856f4f55d9e36acfab245d0903ff631af5 / 4245   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-r45-coordinator
AID-2026-072[0]  14-ai-development/work-items/AID-2026-072/prompt-v1.md
    manifest lines: sha@90 bytes@91
    OLD 1c8f58cff7d248f7bd3a7b87aff836a2f497e57512e64376c1aa778085b67ea7 / 8623
    NEW 5e29f0695537e19bbf2e64ee4bf4fe85d03e732126f5d7dec92b2cacacc67a8f / 8565   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-903-fixture-collision
AID-2026-073[0]  14-ai-development/work-items/AID-2026-073/prompt-v1.md
    manifest lines: sha@81 bytes@82
    OLD 08eb2369f7f6228adbbb4dfc4df88b6ceaf9381be1a5d4bf90ad61ec32145c1a / 5089
    NEW 278e8a975be335e6904af591b7f45367f34204ed4a9d33f81a19d6cfa5b3a7cd / 5031   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-w1081-tests
AID-2026-074[0]  14-ai-development/work-items/AID-2026-074/prompt-v1.md
    manifest lines: sha@83 bytes@84
    OLD 78044dfbc68873766fc6773768099a2a7b5b08d67594ca5bf09decbeb991a915 / 3967
    NEW b5c8c5470850be9e58f23f55a31ee0dd7b2d6e560f7b12486c2a968f41f802fe / 3909   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-1029-declared-vs-protected
AID-2026-075[0]  14-ai-development/work-items/AID-2026-075/prompt-v1.md
    manifest lines: sha@128 bytes@129
    OLD e85f9ae067792717fbe989322dfee804091c776b2ad4317a03f2a95970ee4d83 / 4961
    NEW 0a1b6f82484207b81736a230ef51507de1dc83ed90bfcbd4fdd19b9554a2d0df / 4903   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-wo01-r47-coordinator
AID-2026-076[0]  14-ai-development/work-items/AID-2026-076/prompt-v1.md
    manifest lines: sha@94 bytes@95
    OLD 06ee5615ab9fc696afa769183141d637ec5287776b60cc0b06afd117a024f6b2 / 5525
    NEW 6974846995878c7d76dac9f7fad320bc26613e598d48b68f023564dd66a424c0 / 5467   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-w1088-edited-trigger
AID-2026-077[0]  14-ai-development/work-items/AID-2026-077/prompt-v1.md
    manifest lines: sha@97 bytes@98
    OLD 0339f07cd6bd5dbd5211b45066ee5c1bba78d4768d763beeac4ce24aa368a931 / 5621
    NEW 9de48039bb47ac8320d565205e67616a1345858d0f29c8e8e850d368fe134aee / 5563   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-a1084
AID-2026-078[0]  14-ai-development/work-items/AID-2026-078/prompt-v1.md
    manifest lines: sha@195 bytes@196
    OLD c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2 / 7533
    NEW cb9890fc1c4e2ff07ec808f2f1401bc5082b3c3e4e89e5dac0450aa1a81eb5d6 / 7475   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=req05-convergence-session-identity-not-recorded
AID-2026-078[1]  14-ai-development/work-items/AID-2026-078/prompt-v1.md
    manifest lines: sha@195 bytes@196
    OLD c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2 / 7533
    NEW cb9890fc1c4e2ff07ec808f2f1401bc5082b3c3e4e89e5dac0450aa1a81eb5d6 / 7475   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=req05-convergence-session-identity-not-recorded
AID-2026-079[0]  14-ai-development/work-items/AID-2026-079/prompt-v1.md
    manifest lines: sha@161 bytes@162
    OLD a2d216ee647954b02a6487349716191403e67171d63a82acd7ab15c9feafc81f / 5790
    NEW af8ad57de5eddf104c3d1ff4eb40e377e352c8ab62e98f86d422139b3b5e03a8 / 5732   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=a1078-pr1078-rebase-session
AID-2026-080[0]  14-ai-development/work-items/AID-2026-080/prompt-v1.md
    manifest lines: sha@500 bytes@501
    OLD 08f5e42efdef2c3380056fd8528cf057d6d2a7b25c366566a8599e2aff4df19a / 9932
    NEW c071d0ee5978785a09ff5c9b902e5c3959f4bf7f611e7e35ab36d4c40996c2b8 / 9874   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=req05-convergence-session-identity-not-recorded
AID-2026-081[0]  14-ai-development/work-items/AID-2026-081/prompt-v1.md
    manifest lines: sha@159 bytes@160
    OLD 7b761550e7cf5a64a3000b908b0a838e4e316b6db69f72d50d890c475f1eb3de / 4428
    NEW a0272451912214b9608f4050f2168f22fece00010de305fca039ac892ac44f0c / 4370   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=a1081-opencode-author
AID-2026-082[0]  14-ai-development/work-items/AID-2026-082/prompt-v1.md
    manifest lines: sha@152 bytes@153
    OLD 79bcd0738f9c0f0c5b3dcf05675629c12a7eb51bcaaff0e184ba1ec93e31b7cb / 5831
    NEW ff3eccdc7154cd2f95858c25215ba4198e1a96a2210186b0784e975dd5e7c5cd / 5773   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=NOT_RECORDED
AID-2026-084[0]  14-ai-development/work-items/AID-2026-084/prompt-v1.md
    manifest lines: sha@152 bytes@153
    OLD acdd40d2b2b2357ecfea7411122b146e43d4daab7fd8230bc32ba96009c86b55 / 4775
    NEW 3e02da52ac4560ec1d8a2eca1b88a9102354401e14377b8476961740c05d6745 / 4717   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=a944-opencode-author
AID-2026-085[0]  14-ai-development/work-items/AID-2026-085/prompt-v1.md
    manifest lines: sha@206 bytes@207
    OLD 17a8cd7583b88aaa348024bf445c9c3bbb86e463c38e49495df9d07edbb3f35e / 7689
    NEW 80a1ecb80d093c69b3a1921eb7146852df44a0bf4aa5da775f8907fd4f5447f9 / 7631   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=a925-opencode-author
AID-2026-089[0]  14-ai-development/work-items/AID-2026-089/prompt-v1.md
    manifest lines: sha@86 bytes@87
    OLD 7682d9287605c24109c6502963b0dd73f133a46b608ba495bc0a0da10292a903 / 4258
    NEW e75f603f054dbd8cc433f54c1f125ee31d60b46653caf8f76c63703756409064 / 4200   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=NOT_RECORDED
AID-2026-090[0]  14-ai-development/work-items/AID-2026-090/prompt-v1.md
    manifest lines: sha@62 bytes@63
    OLD 32e5a263ab34d2806110ba09500c3b750613360c20cb082eb1e69fd3cd3fe3a3 / 2034
    NEW 79288220c2196f5af81e0e5a62bf2264b6874b8814614757e08c61764b808d6c / 1976   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=NOT_RECORDED
AID-2026-091[0]  14-ai-development/work-items/AID-2026-091/prompt-v1.md
    manifest lines: sha@67 bytes@68
    OLD 11b2d92aa94d1af88ee403def9fa2977bb7cee8c9c32ff957fbc4c06e91ac5d8 / 2058
    NEW a531954b26c831a555486684e9130eedd1bcd57152ac55ed89ea3010dc9e88ac / 2000   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=NOT_RECORDED
AID-2026-094[0]  14-ai-development/work-items/AID-2026-094/prompt-v1.md
    manifest lines: sha@122 bytes@123
    OLD 81644f71a94a155c6162f102dac6fe46670127b8c0ecf134c9321245096ba2c5 / 6972
    NEW 766d5bd3f8ed61c03ac6630f04ad63daecf49d1751ccd2e1e585d5bad95b6d4e / 6914   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=a752-opencode-author
AID-2026-096[0]  14-ai-development/work-items/AID-2026-096/prompt-v1.md
    manifest lines: sha@45 bytes@46
    OLD 0ebc78aefd4d29d66ee6a77cf760a590eb67c70a1e215ef384b8bc41aee128ca / 2757
    NEW 13b231991e54dce2b485a1709d4bce03b527e43f29b66a876c53235032e52771 / 2699   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=NOT_RECORDED
AID-2026-097[0]  14-ai-development/work-items/AID-2026-097/prompt-v1.md
    manifest lines: sha@95 bytes@96
    OLD 4e3dbbd35d002403849329a14d2f5c6357f695ea835327ff56c151cde00fed56 / 4283
    NEW 70f4eb79f8c4203f2d657e28c715d390a5a15ac2b54366c1db5e460302554d91 / 4225   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=session-283-f02-residuals
AID-2026-098[0]  14-ai-development/work-items/AID-2026-098/prompt-v1.md
    manifest lines: sha@82 bytes@83
    OLD f9b83206744d38bfaa782e47d34ff11e696f2cd04c1c31b4e6fe5b0a1843cc06 / 3241
    NEW 6b6c7407e27773e4420cad0148c574735ead00f25ef7e36282a64613831a0b1c / 3183   delta -58
    provenance=NOT_VERIFIED status=NOT_RECORDED session=NOT_RECORDED
AID-2026-099[0]  14-ai-development/work-items/AID-2026-099/prompt-v1.md
    manifest lines: sha@81 bytes@82
    OLD eed5a5b7cee82bc4893ed57a93d11957b86926700befa91661da40fe8c645c73 / 2418
    NEW 53abd3e3119e4c7eb486b70ce9e90b363d91317ddfd12bf4952526248f3a56e3 / 2360   delta -58
    provenance=RECORDED_SNAPSHOT; SESSION_ID_NOT_AVAILABLE status=NOT_RECORDED session=NOT_RECORDED
AID-2026-101[0]  14-ai-development/work-items/AID-2026-101/prompt-v1.md
    manifest lines: sha@264 bytes@265
    OLD 89ac65f2d58e187451b7c0a98648d0dd4352e3dac79f521b8029b0432f7e94c1 / 4470
    NEW de3b9b80c952096d7ba14b5226517eed8c14b61593328f80d3a3cf3f1122fc94 / 4412   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=owner-proxy-2026-11-26
AID-2026-102[0]  14-ai-development/work-items/AID-2026-102/prompt-v1.md
    manifest lines: sha@196 bytes@197
    OLD df3c53282d858ecc7302ba86b4fb419bf6a31c8030d30cee256b64840b4e4e7a / 4470
    NEW 468a1d4fd8f43d81c8ffba081afd46497b54a2b427849838946163785716072d / 4412   delta -58
    provenance=NOT_VERIFIED status=RECORDED session=owner-proxy-2026-11-26
AID-2026-186[0]  14-ai-development/work-items/AID-2026-186/prompt-v1-original.source.txt
    manifest lines: sha@61 bytes@62
    OLD a421889d3654e49e2247b7207faef0113c188c0e28c7dd0caeea91127c21d67e / 2285
    NEW 698aee8404b032926c4c485c57347bf31c63111a1ee5bc6c9e0e49a56d8a7f50 / 2340   delta +55
    provenance=NOT_VERIFIED status=RECORDED session=NOT_RECORDED
AID-2026-241[0]  14-ai-development/work-items/AID-2026-241/prompt-v1-original.source.txt
    manifest lines: sha@210 bytes@211
    OLD 5c8f02062568720bb9132b27bdb3d6a4c9ac9fbb603d0c42a4818f6c2105002a / 6983
    NEW 90e14513ca0b8ab4a2bdb220d93461942852142a07955f764be7ccf53fda4c93 / 7130   delta +147
    provenance=NOT_VERIFIED status=RECORDED session=req05-convergence-session-identity-not-recorded

--- delta histogram: Counter({-58: 40, 55: 1, 147: 1})
--- distinct manifests: AID-2026-059, AID-2026-061, AID-2026-062, AID-2026-063, AID-2026-064, AID-2026-066, AID-2026-067, AID-2026-068, AID-2026-069, AID-2026-070, AID-2026-071, AID-2026-072, AID-2026-073, AID-2026-074, AID-2026-075, AID-2026-076, AID-2026-077, AID-2026-078, AID-2026-079, AID-2026-080, AID-2026-081, AID-2026-082, AID-2026-084, AID-2026-085, AID-2026-089, AID-2026-090, AID-2026-091, AID-2026-094, AID-2026-096, AID-2026-097, AID-2026-098, AID-2026-099, AID-2026-101, AID-2026-102, AID-2026-186, AID-2026-241
```

Interpretation, measured, not assumed:

- Shape B is already correct everywhere: 64 manifests match, 0 mismatch. Commit `27bfa597`
  (merged as PR #1321, merge commit `a7cf5256`) rewrote the **top-level** `prompt_sha256` /
  `prompt_bytes` lines and nothing else. Example, `git show 27bfa597 -- .../AID-2026-059/manifest.yaml`:
  it changed `prompt_sha256: 65474e7f...` / `prompt_bytes: 3866` to `4881d629...` / `3808`, while the
  same file's `session_evidence[0].executed_prompt_sha256` still reads `65474e7f...` / `3866`.
- So the residual defect is shape A: 40 entries in 34 manifests still pin the pre-#1281 bytes, every
  one exactly 58 bytes larger than the committed file. `scripts/governance/session_evidence/validate.py`
  (`check_11_prompt_snapshot_hashes`) compares exactly this field against the committed blob, so these
  40 entries would fail that validator the moment a pull request touched those manifests.
- Two entries are a different cause, not the -58 class: `AID-2026-186[0]` (+55) and `AID-2026-241[0]`
  (+147) pin `prompt-v1-original.source.txt`, whose committed blob is CRLF while the pinned digest is
  the LF rendering of the same text (147 CR and 55 CR respectively — exactly the delta). Their
  `executed_prompt_provenance` is `NOT_VERIFIED`.
- One entry declares no usable pin: `AID-2026-261[0]` points at a `prompt-v1.md` that is not committed,
  with `executed_prompt_sha256: "000...0"`, `executed_prompt_bytes: 0`,
  `executed_prompt_provenance: NOT_VERIFIED`, `session_reference_status: NOT_RECORDED`.
- Defect 2 of the issue (three attributions naming `AID-2026-090`) is already corrected in `main` by
  the same commit `27bfa597`: `AID-2026-072:67` now reads "Refreshed by AID-2026-101 ... that number
  belongs to the ContextVersion immutability work item, which merged as PR #1241", and
  `AID-2026-076:72` the same shape; `AID-2026-047`'s `prompt_digest_correction` carries
  "Corrected by AID-2026-116". Measured with `grep -n "Corrected by AID-2026-090|Refreshed by
  AID-2026-090"` over the three files: no match. Nothing in this pull request should re-edit those
  sentences; the work item states they are already correct and cites the commit.
- `INDEX.md` contains none of the stale digests (`grep -c "89ac65f2|de3b9b80"` = 0), so the issue's
  "33 INDEX cells" clause no longer describes this tree. State that rather than inventing cells to edit.

# 2. The issue this closes, verbatim

```markdown
## What was measured

Two defects, both found by re-running the digest sweep on the base this work item was prepared
against, rather than reported by anyone.

### 1. Thirty-three manifests pin a digest that describes no committed byte

PR #1281 (commit `44b57170`, merged 2026-11-26T11:18:08Z) removed
`approval_scope.included_sections` and `approval_scope.included_assets` from 36 prompt snapshots.
That removal is correct -- ruling 76 ordered it and DM-02 now enforces it. The defect is that the
pull request repinned only its own manifest:

```
$ git show --numstat --format="" 44b57170 | grep -c "prompt-v1.md"
36
$ git show 44b57170 | grep -c "^+prompt_sha256"
2
```

So 32 manifests were left declaring the digest of text that no longer exists. Every affected file is
exactly 58 bytes shorter than its manifest claimed -- the two removed lines plus their newlines --
which identifies the cause as one mechanical edit rather than 32 separate mistakes.

```
$ python3 digest_audit.py     # on main ba5b26b3
manifests whose digest matches the file it pins: 54
manifests whose digest does NOT match:           0
$ python3 digest_audit.py     # on main a7e7c64b
manifests whose digest matches the file it pins: 30
manifests whose digest does NOT match:          33
```

`AID-2026-106` is the same defect with the byte count unchanged (2998 before and after), so a
repin that guarded only size would have passed it.

The 33 INDEX cells that restate those digests were stale in the same way. Nothing checked them:
every audit run in the preceding sessions compared a manifest's `prompt_sha256` against the file it
pins, and none read the table.

### 2. Three corrections credit a work item that did not make them

`AID-2026-047`, `AID-2026-072` and `AID-2026-076` each end a field with "Corrected by
AID-2026-090". `AID-2026-090` is the ContextVersion immutability work item, merged by PR #1241 at
2026-11-26T06:57:20Z, and it never mentions any of the three:

```
$ grep -c "AID-2026-047\|AID-2026-072\|AID-2026-075\|AID-2026-076\|AID-2026-080\|AID-2026-101" \
    14-ai-development/work-items/AID-2026-090/manifest.yaml
0
```

The correction branch held four identifiers before it merged (080, 081, 090, 101). Those sentences
were written while it held 090; when the number went to another work item they were not revisited.
`AID-2026-101`'s own `identifier_history` declares 090 abandoned, so the three sentences
contradicted the record that performed the correction.

The same paragraph names **PR #1255** as the merge of `AID-2026-090`. #1255 closed without merging;
#1241 is the merge. Every other file in the tree cites #1241 correctly, so 101 is the outlier -- and
101 is the record whose subject is recording prior values accurately.

## Why the second one is worse than a dangling reference

`AID-2026-090` exists, it is a real manifest, and it is about an unrelated subject. A reader who
follows "Refreshed by AID-2026-090" lands on a plausible document, finds no prior values in it, and
has to decide whether the record is wrong or the manifest is. Nothing in the tree excludes either
reading.

## Scope of the correction

- 32 manifests repinned to the committed bytes, plus `AID-2026-106`.
- 33 INDEX cells repinned to match. Only the token that disagreed was touched.
- Three attribution sentences repointed to `AID-2026-101`, with the abandoned number left visible
  as abandoned rather than deleted.
- `AID-2026-101`'s `identifier_history` corrected to name #1241 and to record that #1255 closed
  unmerged.

No prompt file is restored: putting the two keys back would return the corpus to the state
`check_document_management.py` refuses. The digests move to the files, not the files to the digests.

## What is not fixed, and why

Nothing in CI reads a manifest's top-level `prompt_sha256`:

```
$ grep -rn "prompt_sha256" scripts/ | grep -v executed_prompt_sha256
(no matches)
```

That is why 32 stale pins sat in `main` with every required context green. Closing it needs a
checker, and this work item is documentation-only by instruction. The gap is recorded as F4 so the
next session can decide it deliberately rather than rediscover it.

## Acceptance

See `AID-2026-116/manifest.yaml` AC1-AC7. Every prior value is in `AID-2026-116/session-evidence.md`
with the old and new digest side by side.
```

# 3. What I need from you

Deliver, in this order, all inside one reply.

**(a) The repin patches.** For each of the 40 `-58` entries, one `=== PATCH:` block per manifest file,
rewriting only `executed_prompt_sha256` and `executed_prompt_bytes` to the measured `NEW` value in the
table above. `AID-2026-078` has two entries with the identical old digest; disambiguate with a two-line
`OLD` context that includes the differing line above each (the `executed_prompt_snapshot_file` line is
identical too, so include the following `executed_prompt_provenance` line or the preceding key if it
differs — check the file and choose context that occurs once).

**(b) A ruling, with reasons, on the three entries outside the -58 class** — `AID-2026-186[0]`,
`AID-2026-241[0]` (CRLF) and `AID-2026-261[0]` (unpinned). For each, choose exactly one:
repin to the committed bytes in this pull request, or leave untouched and record as a finding with the
reason. If you choose repin, give the patch block in the same format. Note that
`prompt-v1-original.source.txt` is named "original", so say explicitly which byte sequence you consider
the artifact and why.

**(c) The four work-item files** as `=== FILE:` blocks with fenced content:

    === FILE: 14-ai-development/work-items/AID-2026-322/manifest.yaml
    ```
    ...content...
    ```

Same for `evidence.md` and `session-evidence.md`. Do not emit `prompt-v1.md` (I supply it).

`evidence.md` must contain, as literal fenced `text` blocks, the measurement output above (you may
quote the sections you rely on) and a table of every superseded digest with old and new side by side,
so no prior value is lost. `session-evidence.md` must state truthfully: the implementation content was
authored by a ChatGPT session; the operator applied it mechanically and ran the commands; the digests
were measured by the operator's script on the tree, not asserted by the author.

**(d) The INDEX row**, as a `=== PATCH:` block against `14-ai-development/work-items/INDEX.md`,
inserted immediately after the last existing table row (I will tell the script where; give the OLD as
the final row of the table plus the following blank line, so the insertion point is unique). Column
shape must match the neighbouring rows; read `AID-2026-116`'s row in that file as the model and keep
the row to what the manifest states.

**(e) The answer to "why is this a data repair and not a re-introduction of `included_sections`"**,
in two or three sentences, to be quoted in the PR body.

# 4. Output format

- Patch blocks: exactly

      === PATCH: 14-ai-development/work-items/AID-2026-XXX/manifest.yaml
      ```
      --- OLD ---
      <exact existing text, byte for byte, including indentation>
      --- NEW ---
      <replacement>
      ```

  `OLD` must occur exactly once in the file. One `OLD`/`NEW` pair per field, or one pair covering both
  lines. No `+`/`-` diff markers, no ellipses, no "..." abbreviations.
- File blocks: `=== FILE: <path>` followed by a fence whose first line is the file's first line.
- No prose inside the fences. Explanations go outside them, before the block they explain.
- If you believe a measured value in this message is wrong, say so and give the command that shows it;
  do not silently "fix" a number.

# 5. Reference shape: `AID-2026-290/evidence.md` frontmatter (copy it, change the scope strings)

```yaml
---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-290/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "..."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "..."
    canonical_scope_id: "ai-development/aid-2026-322-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-322"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
```

# 6. Reference shape: `session_evidence` and `implementation` in a merged manifest

```yaml
session_evidence:
  - role: IMPLEMENTATION_SESSION
    issue_refs:
      - "#1268"
    implementing_ai_session: "6b090a00-c1b0-83ec-ad26-9668c882a144"
    session_evidence_ref: 14-ai-development/work-items/AID-2026-290/session-evidence.md
    executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-290/prompt-v1.md
    executed_prompt_sha256: "f588b712f1133ec58f2ed949b226ae73e6bf0622841da8be3e7838249cc1b895"
    executed_prompt_bytes: 4843
    executed_prompt_provenance: NOT_VERIFIED
    session_reference_status: "RECORDED"

implementation:
  status: IMPLEMENTED
  summary: >-
    ...
  files_changed:
    - 14-ai-development/work-items/AID-2026-322/manifest.yaml
    - 14-ai-development/work-items/AID-2026-322/prompt-v1.md
    - 14-ai-development/work-items/AID-2026-322/evidence.md
    - 14-ai-development/work-items/AID-2026-322/session-evidence.md
    - 14-ai-development/work-items/INDEX.md
```

Use `implementing_ai_session: "9router-hermes-aid-322-2026-11-27"` — a single token, the session that
produced this content. `executed_prompt_provenance: NOT_VERIFIED` is correct: the operator placed the
prompt and the session id is recorded, but the execution was not independently attested.

Begin. Nothing in this message asks you to evaluate whether the work should be done; it is decided.
