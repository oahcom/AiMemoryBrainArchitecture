import re

p = r'D:\gate620\repo\reviews\bmcp-architecture-followup\BMCP-ARCH-001.zh-CN.md'
raw = open(p, 'rb').read()
crlf = b'\r\n' in raw
t = raw.decode('utf-8').replace('\r\n', '\n')

pairs = [
    # S8 minor: 措辞精确化
    ("这些文件仍归 H 所有；文件存在不等于批准或冻结。",
     "这些文件仍归 H 所有；这些文件的存在不构成批准或冻结。"),
    # S1+S2+S3: D / I 所有权，补回 B 整句，BMCP/H/C 三主体
    ("D 拥有 Canonical Identity/Lifecycle 和 D Forget Fence；I 拥有授权和 PermissionEpoch。BMCP 消费这些权威，不得创建替代机制。",
     "B 拥有语义词汇与认识论含义。D 拥有规范 ID 分配、修订提交与当前性、生命周期、谱系、ConflictSet，以及 D ForgetOperation/Fence。I 拥有 Principal/Actor 授权、attestor 授权、PermissionEpoch、撤销、保留策略/法律保全/备份，以及全局 Forget 策略与评估。BMCP/H/C 必须消费由 Owner 签发的不透明引用（opaque owner-issued refs），且 MUST NOT 创建替代物。"),
    # S6: Metadata-only
    ("| `docs/governance/translation-status.md` | Governance Register | 仅元数据 |",
     "| `docs/governance/translation-status.md` | Governance Register | 仅允许元数据变更 |"),
    # S5: not claimed != PENDING
    ("作者准备双语 Pair；独立一致性审查 PENDING",
     "已进行 Owner-delegate 语义审查；不声称已进行独立一致性审查"),
    # S4: 补 B/D/I owner pins
    ("main `c58878fce24528a0842b4f8887c93ddbf465b566`；H `3e8b33df18b9e6fc757ca84ff07a12faebc78e74`",
     "main `c58878fce24528a0842b4f8887c93ddbf465b566`；H `3e8b33df18b9e6fc757ca84ff07a12faebc78e74`；\u00a72/\u00a77 中的 B/D/I Owner 固定版本引用"),
]

for i, (o, n) in enumerate(pairs, 1):
    c = t.count(o)
    assert c == 1, (i, c, o[:60])
    t = t.replace(o, n, 1)
    print('[%d] OK' % i)

# S7: 删除中文单边添加的声明性句子
extra = "结构配对不等于语义双语一致性审查。"
print('extra sentence count:', t.count(extra))

open(p, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
print('written crlf=', crlf)
