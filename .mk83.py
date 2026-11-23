import re

repo = r'D:\gate620\repo'
E = repo + r'\reviews\bmcp-architecture-followup\BMCP-ARCH-001.en.md'
Z = repo + r'\reviews\bmcp-architecture-followup\BMCP-ARCH-001.zh-CN.md'

et = open(E, encoding='utf-8').read()
zt = open(Z, encoding='utf-8').read()


def sub(t, key, stop):
    m = re.search(r'^### ' + key + r' .*$', t, re.M)
    s = m.start()
    m2 = re.search(stop, t[m.end():], re.M)
    return t[s: m.end() + m2.start()]


en_71 = sub(et, r'7\.1 H confirmation requests', r'^### 7\.1\.1 ')
zh_71 = sub(zt, r'7\.1 H 确认请求', r'^### 7\.1\.1 ')
en_712 = sub(et, r'7\.1\.2 ', r'^### 7\.2 ')
zh_712 = sub(zt, r'7\.1\.2 ', r'^### 7\.2 ')

body = """你是独立审查方。这是一份双语架构文档的**分批语义审查**，本批覆盖 §7.1 与 §7.1.2。

# 已有进度

- §7.1.1、§7.4、§8、§9、§12 已审查通过
- §1/§3/§11 已审查并修正（D/I 所有权对象被压缩、BMCP/H/C 三主体被缩为一个、not claimed 被写成 PENDING 等 8 项）
- §4/§5/§6 已审查（§4 修正了 immediately before 时点约束和 authorize side effects 措辞）

本批是 §7 剩余部分的第一半。§7.2/§7.3 会单独作为下一批。§7.1.1（含 H-CONFIRM-001..004 四个子节）已审过，不在本批范围内，但它紧接在 §7.1 之后，如果 §7.1 的表述与 §7.1.1 的结论冲突，请指出。

# 基线

- 仓库 oahcom/AiMemoryBrainArchitecture
- 文件 reviews/bmcp-architecture-followup/BMCP-ARCH-001
- 分类 REVIEW/HANDOFF PAIR ONLY — CANDIDATE / ARCHITECTURE_PARTIAL
- 英文为原文，中文为译文

# 英文 §7.1

```markdown
%s```

# 中文 §7.1

```markdown
%s```

# 英文 §7.1.2

```markdown
%s```

# 中文 §7.1.2

```markdown
%s```

# 请判定

1. **确认请求的性质**：§7.1 是 H 向 Owner 提出的确认请求清单。中文是否保持了「这是请求、不是已获批准」这个性质？有没有把 request 写成 decision 或 approval。
2. **每项请求的边界**：这些请求各自要求 H 确认什么、不确认什么。中文是否逐项对应，有无把某项请求的范围扩大或缩小。
3. **§7.1.2 的核心区分**：这一节专门区分「逻辑决议」与「精确工件状态」。这个区分是整份文档最容易被译坏的地方——中文是否保持了「逻辑上已决定」不等于「工件已冻结/已交付」这个界限。
4. **状态枚举**：PARTIALLY_DECIDED、EXACT_ARTIFACT_MAPPING_OPEN 这类状态值是否原样保留（应保留英文，不译成中文）。
5. **你自己的发现**：漏译、误译、添译、弱化。

# 输出格式

先一行：
VERDICT: ACCEPT / ACCEPT WITH AMENDMENTS / NEEDS REVISION / REJECT

然后：
## §7.1
## §7.1.2
每节 PASS / FAIL。FAIL 给出英文原文、中文现文、问题性质、可直接落盘的中文改法。

## 实质性问题清单
标 BLOCKER / MAJOR / MINOR。

## 与已审 §7.1.1 是否冲突
若 §7.1 或 §7.1.2 的表述与 §7.1.1 已确立的结论矛盾，指出。没有则明确写「无冲突」。

## 本批是否可视为语义等价

# 边界

- 只依据上面四段文本。
- 状态枚举值不应被翻译成中文；若中文把它们译了，请指出。
- 若某项你无法判断，明确说要人工确认。
""" % (en_71, zh_71, en_712, zh_712)

p = r'C:\Users\Administrator\.workbuddy\skills\chatgpt-session-ops\prompts\83-batch3a-s71-s712.md'
open(p, 'w', encoding='utf-8', newline='\n').write(body)
print('written', len(body), 'fences', body.count('```'))
print('en_71', len(en_71), 'zh_71', len(zh_71), 'en_712', len(en_712), 'zh_712', len(zh_712))
