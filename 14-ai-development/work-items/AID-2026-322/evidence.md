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
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Operator-measured repository output and superseded values are transcribed here. The implementation session did not independently execute the measurement script."
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
    canonical_scope: "Measured execution-prompt digest mismatches, repin values and unresolved exceptional cases for AID-2026-322."
    canonical_scope_id: "ai-development/aid-2026-322-measurement-evidence"
    canonical_scope_keywords:
      - "AID-2026-322"
      - "prompt digest"
      - "committed bytes"
      - "repin evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-322 measurement evidence

## 1. Measurement authority and baseline

The operator supplied the following measured baseline:

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Branch: `main`
- Commit: `229c0a6b51f4c761ed969337f6ddf7d0bbbb7d0c`
- Measurement date: 2026-11-27
- Measurement method: SHA-256 of the raw committed bytes of each referenced file, compared with the manifest's declared digest and byte count.
- The implementation author did not run the operator's repository script and does not independently attest the measurements.

The following is the operator-provided measurement output, preserved as supplied.

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

The same script re-run on this tree after the patches were applied. The two remaining mismatches
are the entries the implementation ruling leaves untouched (F1, F2); `AID-2026-322[0]` is listed as
unpinned only because its manifest still carried the operator placeholders at the time of this run.
Operator note: this second block and the verbatim block above were inserted mechanically by the
operator from the script output; the surrounding prose is the implementation session's.

```text
worktree: D:\code\_lcs\fix-1318
manifests parsed: 128

[A] session_evidence executed_prompt_* : MATCH 94  MISMATCH 2  MISSING/UNPINNED 2
[B] top-level prompt_sha256/prompt_bytes: MATCH 64  MISMATCH 0  MISSING 0  NO prompt_file 4

[A] MISMATCH (2):
  AID-2026-186[0]  14-ai-development/work-items/AID-2026-186/prompt-v1-original.source.txt
      declared a421889d3654e49e2247b7207faef0113c188c0e28c7dd0caeea91127c21d67e / 2285   actual 698aee8404b032926c4c485c57347bf31c63111a1ee5bc6c9e0e49a56d8a7f50 / 2340   delta +55
  AID-2026-241[0]  14-ai-development/work-items/AID-2026-241/prompt-v1-original.source.txt
      declared 5c8f02062568720bb9132b27bdb3d6a4c9ac9fbb603d0c42a4818f6c2105002a / 6983   actual 90e14513ca0b8ab4a2bdb220d93461942852142a07955f764be7ccf53fda4c93 / 7130   delta +147

[B] MISMATCH (0):

[A] MISSING/UNPINNED (2):
  AID-2026-261[0]  file=14-ai-development/work-items/AID-2026-261/prompt-v1.md  sha=0000000000000000000000000000000000000000000000000000000000000000 bytes=0
  AID-2026-322[0]  file=14-ai-development/work-items/AID-2026-322/prompt-v1.md  sha=__PROMPT_SHA256__ bytes=__PROMPT_BYTES__

[B] MISSING (0): []
[B] NO prompt_file (4): AID-2026-001, AID-2026-003(NOT_VERIFIED), AID-2026-004, AID-2026-064

json: audit1318-after.json  (2 records)
```

## 2. Interpretation of the two pin shapes

Shape A is:

`session_evidence[*].executed_prompt_sha256` and `executed_prompt_bytes` compared with `executed_prompt_snapshot_file`.

Shape B is:

Top-level `prompt_sha256` and `prompt_bytes` compared with `prompt_file`.

The operator measured 42 Shape A mismatches, comprising 40 entries in the common -58-byte class and two line-ending exceptions. One additional Shape A entry has no usable committed snapshot pin.

Shape B has 64 matches and zero mismatches. Its four NO prompt_file cases are separately reported and are not Shape B digest mismatches.

The historical top-level repin in commit `27bfa597`, merged as PR #1321 in merge commit `a7cf5256`, corrected Shape B but did not update the corresponding Shape A entries. The residual 40-entry defect is therefore in the nested session-evidence fields.

The operator reports that `scripts/governance/session_evidence/validate.py`, through `check_11_prompt_snapshot_hashes`, compares the nested executed-prompt fields against committed prompt bytes.

## 3. All superseded digest and byte-count values

The following table preserves every old value changed by this work item. Each NEW value is the operator-measured SHA-256 and byte count of the referenced committed prompt file.

| Work item / entry | Snapshot file | Old SHA-256 | Old bytes | New SHA-256 | New bytes |
|---|---|---|---:|---|---:|
| AID-2026-059[0] | prompt-v1.md | `65474e7f0927d2dfeaad33814fdbd7d576635cc8a0e8d2a3a7441e3a65ab7317` | 3866 | `4881d6292e96154d5f7364816ae3e9977365e09b88e8475f4dd9d655e3e34a8c` | 3808 |
| AID-2026-059[1] | prompt-1015.md | `245dbfc39ca8b20cec30bba392c4b2f5e0db383b404eb4e8e10a8f7cee899f46` | 7986 | `2be1e84c9fc262066e687bf21a57d80a090fed73d3c6765f26fc6fc02d3c0b51` | 7928 |
| AID-2026-059[2] | prompt-1026-v1.md | `25058389340c796a557746ae5ed90cf73cada98998e62da1692bb5ce4a3e4bd9` | 4811 | `8ca8bfc89774fa728e1671808510af4aa9def9b9860a9cc9016c5ca8bba87ea5` | 4753 |
| AID-2026-059[3] | prompt-1042-1048-v1.md | `ceae6530d70c60803b58ba91a3f5ed28671a525bcc640c32aa8f020d3defaffd` | 6507 | `8aa0b29ce5ce620c77ac3621531b4b8df908010675f5486672d056345eb76b11` | 6449 |
| AID-2026-059[4] | prompt-1029-1076-v1.md | `f0a315582ba51212758d82c6dfacedaaa676575f2b0ffcec4170fbded05f229e` | 9166 | `81e070af08045cec4635201b99861bab00a2ffa7e1caafab3342608d0adde22a` | 9108 |
| AID-2026-059[5] | prompt-1223-v1.md | `5de7adc61dcb6659b16a4da5e35826cd635f616ad664654d327c9a1836cade95` | 3961 | `642f8c20076565ac083a5fd0873c39890238659dac101564aced1c4d328385f8` | 3903 |
| AID-2026-061[0] | prompt-v1.md | `7ea255ab98c081d797820fa48d7744d2209eb285c0bda17cee6c4f22d66f0b81` | 18776 | `6c0a9cc7e47f2e30505f8b765d08663b1c032cda128f7fb79a148152cff6e3cd` | 18718 |
| AID-2026-062[0] | prompt-v1.md | `3f57662579cfe90c230585b7ab7ff87c10e0074df167ac1d6c79e5fe8b9766de` | 2927 | `96358a3a9af4452d0b51b13f3483f319d93b38eb2ac414eb39d674a0a61c6c42` | 2869 |
| AID-2026-063[0] | prompt-v1.md | `4cf341c81da42e332e7e352a47f6fa8eb9e82e2b266134dbe2497b874629efd8` | 2691 | `411a0be8d6e73a4953f86740b60418db81bb96da7be3f8696a82bf880781b4b5` | 2633 |
| AID-2026-064[0] | prompt-v1.md | `57decec9de8752e099d6a72588fcdd00904bffbe4cecb614ddf9c34a441fdbb8` | 7188 | `f169ed7738a1ed56a67e371ffdf57de944c4db9b344b9732001e51edfe052672` | 7130 |
| AID-2026-066[0] | prompt-v1.md | `1ae516e747ae3417d9a34cc5fc870128da2efbd603d4d958fceaf18a3791c6ae` | 5921 | `d6afe924427aebf974c86a742bee679a3ca6cc247d58d691297ede9002619c6c` | 5863 |
| AID-2026-067[0] | prompt-v1.md | `07b49d7fa41ec6a5e9025dd3440e9f181654c8903288aa0d430d9324df5ac0da` | 5261 | `c73aa6e35fddb745b7925d6b350fb661d538beb3e5f9b975c89d1e1bc4906ab5` | 5203 |
| AID-2026-068[0] | prompt-v1.md | `7d55d2011f931207ec4d63a6d0a94715a82ab16365cef390cf7423f8e7ab5a31` | 6031 | `9a1e0e823d200aedebfefeb1f4bb26de3cbd1569938e6625f56a5e6599eb71f5` | 5973 |
| AID-2026-069[0] | prompt-v1.md | `360c3273a8e6b28cefe583aabe9c5f3d119e94212735c2fae626bbad72816db6` | 6062 | `12a7ebc07e9d2f048157caa4f56e3ba0b18b9078290316816c83d361451e4c7e` | 6004 |
| AID-2026-070[0] | prompt-v1.md | `b0013ed25ebdf4c5a0cc200551d9e89edf6993138828527abb2fab137fda024a` | 6371 | `6df00b015153a2105dc52f131d2b58c2b8207511e001ab00d572a462fc030d31` | 6313 |
| AID-2026-071[0] | prompt-v1.md | `4c735edd42b80f43d04c26fdbbcc8e29662d96456394fbf5417a8386d88609c7` | 4303 | `8080149aa3a0a9ec3f68071b25e62d856f4f55d9e36acfab245d0903ff631af5` | 4245 |
| AID-2026-072[0] | prompt-v1.md | `1c8f58cff7d248f7bd3a7b87aff836a2f497e57512e64376c1aa778085b67ea7` | 8623 | `5e29f0695537e19bbf2e64ee4bf4fe85d03e732126f5d7dec92b2cacacc67a8f` | 8565 |
| AID-2026-073[0] | prompt-v1.md | `08eb2369f7f6228adbbb4dfc4df88b6ceaf9381be1a5d4bf90ad61ec32145c1a` | 5089 | `278e8a975be335e6904af591b7f45367f34204ed4a9d33f81a19d6cfa5b3a7cd` | 5031 |
| AID-2026-074[0] | prompt-v1.md | `78044dfbc68873766fc6773768099a2a7b5b08d67594ca5bf09decbeb991a915` | 3967 | `b5c8c5470850be9e58f23f55a31ee0dd7b2d6e560f7b12486c2a968f41f802fe` | 3909 |
| AID-2026-075[0] | prompt-v1.md | `e85f9ae067792717fbe989322dfee804091c776b2ad4317a03f2a95970ee4d83` | 4961 | `0a1b6f82484207b81736a230ef51507de1dc83ed90bfcbd4fdd19b9554a2d0df` | 4903 |
| AID-2026-076[0] | prompt-v1.md | `06ee5615ab9fc696afa769183141d637ec5287776b60cc0b06afd117a024f6b2` | 5525 | `6974846995878c7d76dac9f7fad320bc26613e598d48b68f023564dd66a424c0` | 5467 |
| AID-2026-077[0] | prompt-v1.md | `0339f07cd6bd5dbd5211b45066ee5c1bba78d4768d763beeac4ce24aa368a931` | 5621 | `9de48039bb47ac8320d565205e67616a1345858d0f29c8e8e850d368fe134aee` | 5563 |
| AID-2026-078[0] (#266) | prompt-v1.md | `c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2` | 7533 | `cb9890fc1c4e2ff07ec808f2f1401bc5082b3c3e4e89e5dac0450aa1a81eb5d6` | 7475 |
| AID-2026-078[1] (#1126) | prompt-v1.md | `c2ae6f744dbfc383ef1468516bc116744a7bf38a27566685c51c63a337d4b1a2` | 7533 | `cb9890fc1c4e2ff07ec808f2f1401bc5082b3c3e4e89e5dac0450aa1a81eb5d6` | 7475 |
| AID-2026-079[0] | prompt-v1.md | `a2d216ee647954b02a6487349716191403e67171d63a82acd7ab15c9feafc81f` | 5790 | `af8ad57de5eddf104c3d1ff4eb40e377e352c8ab62e98f86d422139b3b5e03a8` | 5732 |
| AID-2026-080[0] | prompt-v1.md | `08f5e42efdef2c3380056fd8528cf057d6d2a7b25c366566a8599e2aff4df19a` | 9932 | `c071d0ee5978785a09ff5c9b902e5c3959f4bf7f611e7e35ab36d4c40996c2b8` | 9874 |
| AID-2026-081[0] | prompt-v1.md | `7b761550e7cf5a64a3000b908b0a838e4e316b6db69f72d50d890c475f1eb3de` | 4428 | `a0272451912214b9608f4050f2168f22fece00010de305fca039ac892ac44f0c` | 4370 |
| AID-2026-082[0] | prompt-v1.md | `79bcd0738f9c0f0c5b3dcf05675629c12a7eb51bcaaff0e184ba1ec93e31b7cb` | 5831 | `ff3eccdc7154cd2f95858c25215ba4198e1a96a2210186b0784e975dd5e7c5cd` | 5773 |
| AID-2026-084[0] | prompt-v1.md | `acdd40d2b2b2357ecfea7411122b146e43d4daab7fd8230bc32ba96009c86b55` | 4775 | `3e02da52ac4560ec1d8a2eca1b88a9102354401e14377b8476961740c05d6745` | 4717 |
| AID-2026-085[0] | prompt-v1.md | `17a8cd7583b88aaa348024bf445c9c3bbb86e463c38e49495df9d07edbb3f35e` | 7689 | `80a1ecb80d093c69b3a1921eb7146852df44a0bf4aa5da775f8907fd4f5447f9` | 7631 |
| AID-2026-089[0] | prompt-v1.md | `7682d9287605c24109c6502963b0dd73f133a46b608ba495bc0a0da10292a903` | 4258 | `e75f603f054dbd8cc433f54c1f125ee31d60b46653caf8f76c63703756409064` | 4200 |
| AID-2026-090[0] | prompt-v1.md | `32e5a263ab34d2806110ba09500c3b750613360c20cb082eb1e69fd3cd3fe3a3` | 2034 | `79288220c2196f5af81e0e5a62bf2264b6874b8814614757e08c61764b808d6c` | 1976 |
| AID-2026-091[0] | prompt-v1.md | `11b2d92aa94d1af88ee403def9fa2977bb7cee8c9c32ff957fbc4c06e91ac5d8` | 2058 | `a531954b26c831a555486684e9130eedd1bcd57152ac55ed89ea3010dc9e88ac` | 2000 |
| AID-2026-094[0] | prompt-v1.md | `81644f71a94a155c6162f102dac6fe46670127b8c0ecf134c9321245096ba2c5` | 6972 | `766d5bd3f8ed61c03ac6630f04ad63daecf49d1751ccd2e1e585d5bad95b6d4e` | 6914 |
| AID-2026-096[0] | prompt-v1.md | `0ebc78aefd4d29d66ee6a77cf760a590eb67c70a1e215ef384b8bc41aee128ca` | 2757 | `13b231991e54dce2b485a1709d4bce03b527e43f29b66a876c53235032e52771` | 2699 |
| AID-2026-097[0] | prompt-v1.md | `4e3dbbd35d002403849329a14d2f5c6357f695ea835327ff56c151cde00fed56` | 4283 | `70f4eb79f8c4203f2d657e28c715d390a5a15ac2b54366c1db5e460302554d91` | 4225 |
| AID-2026-098[0] | prompt-v1.md | `f9b83206744d38bfaa782e47d34ff11e696f2cd04c1c31b4e6fe5b0a1843cc06` | 3241 | `6b6c7407e27773e4420cad0148c574735ead00f25ef7e36282a64613831a0b1c` | 3183 |
| AID-2026-099[0] | prompt-v1.md | `eed5a5b7cee82bc4893ed57a93d11957b86926700befa91661da40fe8c645c73` | 2418 | `53abd3e3119e4c7eb486b70ce9e90b363d91317ddfd12bf4952526248f3a56e3` | 2360 |
| AID-2026-101[0] | prompt-v1.md | `89ac65f2d58e187451b7c0a98648d0dd4352e3dac79f521b8029b0432f7e94c1` | 4470 | `de3b9b80c952096d7ba14b5226517eed8c14b61593328f80d3a3cf3f1122fc94` | 4412 |
| AID-2026-102[0] | prompt-v1.md | `df3c53282d858ecc7302ba86b4fb419bf6a31c8030d30cee256b64840b4e4e7a` | 4470 | `468a1d4fd8f43d81c8ffba081afd46497b54a2b427849838946163785716072d` | 4412 |

The 40 rows above represent 40 entry-level changes in 34 distinct manifests. AID-2026-078 contributes two entries with the same digest and byte count but different issue references and session-evidence references.

## 4. The common -58-byte class

The operator measured a delta of exactly -58 bytes for all 40 entries in the repair set.

The cause identified in the issue record is the removal of:

- `approval_scope.included_sections`
- `approval_scope.included_assets`

from the affected prompt snapshots.

The removal was required by ruling 76 and is enforced by DM-02. The prompt files already contain the committed post-removal form. The stale values reside in the nested manifest declarations.

The repair therefore moves the declared pins to the measured committed bytes. It does not restore the removed keys.

## 5. Exceptional entries

### AID-2026-186[0]

- File: `14-ai-development/work-items/AID-2026-186/prompt-v1-original.source.txt`
- Declared bytes: 2285
- Committed bytes: 2340
- Difference: +55
- Provenance: `NOT_VERIFIED`

The measured difference consists of 55 CR characters. The digest declared in the manifest describes an LF rendering, whereas the committed file is CRLF.

The filename explicitly identifies an original-source artifact. The committed CRLF sequence is retained as the repository artifact. However, the historical execution input is not independently established. Changing the digest to the CRLF hash would assert an execution identity not demonstrated by the evidence. No change is made.

### AID-2026-241[0]

- File: `14-ai-development/work-items/AID-2026-241/prompt-v1-original.source.txt`
- Declared bytes: 6983
- Committed bytes: 7130
- Difference: +147
- Provenance: `NOT_VERIFIED`

The measured difference consists of 147 CR characters. The same distinction applies: the committed artifact is CRLF, while the declaration represents the LF rendering.

No normalization or repin is made without evidence establishing which byte sequence was actually executed.

The other AID-2026-241 session entry, referencing `prompt-w3-v1.md`, is not part of the mismatch set and is unchanged.

### AID-2026-261[0]

- File: `14-ai-development/work-items/AID-2026-261/prompt-v1.md`
- Declared SHA-256: 64 zero characters
- Declared bytes: 0
- Provenance: `NOT_VERIFIED`
- Session reference status: `NOT_RECORDED`

The referenced prompt snapshot is not committed. There is no committed byte sequence to hash. No replacement digest can be calculated for this missing artifact. The entry remains unchanged.

## 6. Already-completed attribution corrections

The attribution defect described in the original Issue #1318 body has already been corrected on the selected main history.

The operator reports that commit `27bfa597`:

- Corrected AID-2026-072 to identify AID-2026-101.
- Corrected AID-2026-076 to identify AID-2026-101.
- Corrected AID-2026-047 to identify AID-2026-116.
- Replaced the incorrect merge attribution of PR #1255 with PR #1241 in the relevant AID-2026-101 history.

A grep over the three attribution records found no remaining matches for the incorrect correction attribution to AID-2026-090.

Those already-corrected sentences are outside this repair and are not edited.

## 7. INDEX measurement

The operator measured zero occurrences of the stale AID-2026-101 digest values in the current `INDEX.md`.

The original issue's 33-cell historical description therefore does not describe the selected baseline. No historical digest cells are reconstructed, invented, or rewritten.

This work item adds exactly one new navigation row for AID-2026-322.

## 8. Verification boundary

The measurements in this document are operator-supplied results. The implementation author did not run the repository script, inspect the operator's worktree, or independently reproduce the raw-byte measurements.

The operator is responsible for:

1. Applying the exact patches.
2. Running the repository's required gates.
3. Measuring the final committed prompt snapshot bytes.
4. Measuring the committed prompt file and writing its SHA-256 digest and byte count into the manifest.
5. Confirming that the final manifest pins match the committed bytes.

## 9. Ratchet baseline edit

The operator removed 80 lines from `scripts/ci/baselines/manifest-blob-pins.txt`: the 40 SHA-256 and 40 byte-count `MISMATCH session_evidence[...].executed_prompt_snapshot_file` entries resolved by this work item. The seven-line header was replaced by a six-line header recording the removal and the eleven surviving entries: 3 AID-2026-100 related-evidence pins, 6 authored-index pins, and 2 AID-2026-261 `PATH_MISSING` entries. The edit is required because `gate_ratchet` requires every entry to remain failing; a fixed entry is stale/red. The measured local result was `violations=0` and `Repository new-file admission passed`.

No test count, CI result, merge, or independent verification is claimed here.
