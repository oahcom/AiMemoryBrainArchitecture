# GAP-08 · BMCP 一致性测试套件存在未声明的 Node 依赖

**状态**：未关闭 — 仓库侧已在 #546 完成；关闭标准 1 与 5 受 CI 计费中断阻塞
**领域**：08-bmcp-protocol / conformance
**归属线**：Owner H（协议）

## 缺口陈述

三个 `.mjs` 跨语言参考实现 `import` 了第三方 npm 包 `canonicalize`。仓库中**没有任何 `package.json`、`package-lock.json`、`pnpm-lock.yaml` 或 `yarn.lock`**，因此该依赖从未被安装，任何干净检出上调用这些文件的测试都会失败。

这不是密码学缺陷。装好该包之后，所有受影响测试原样通过。

## 证据（在 `main @ f057328d` 上核验）

**1. import 确实存在。**

```sh
grep -rn "canonicalize" --include=*.mjs 08-bmcp-protocol/
```

```
tests/conformance/provider_outcome/c_crypto_profile_h_reference.mjs:2: import canonicalize from "canonicalize";
tests/conformance/provider_outcome/c_crypto_profile_h_reference_1_0_1.mjs:2: import canonicalize from "canonicalize";
tests/conformance/recovery_cutoff/i_crypto_profile_reference.mjs:2: import canonicalize from "canonicalize";
```

**2. 没有任何清单声明它。**

```sh
find . -name "package.json" -o -name "package-lock.json" \
       -o -name "pnpm-lock.yaml" -o -name "yarn.lock" | grep -v node_modules
```

零结果。

Python 依赖清单确实存在——
`08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt`——它声明了
`jsonschema`、`rfc8785` 与 `cryptography`。它无法表达 Node 依赖，也没有别的东西
表达。

**2b. 需要它的测试不在 CI 覆盖范围内。**

`.github/workflows/h-applied-delivery-evidence-conformance.yml` 运行的是：

```
python -m unittest discover -s .../applied_delivery_evidence -p 'test_*.py' -v
python -m unittest discover -s .../recovery_cutoff -p 'test_recovery_join*.py' -v
```

需要 `canonicalize` 的三个文件是
`provider_outcome/test_c_crypto_profile_interop.py`、
`provider_outcome/test_c_crypto_profile_1_0_1_interop.py` 与
`recovery_cutoff/test_i_crypto_profile.py`。它们都不匹配上述任一 discover 模式。
因此该失败不可能在 CI 中暴露——这正是未声明依赖能悄悄进入 `main` 的原因。

**3. 干净树上套件失败。**

```
FAILED provider_outcome/test_c_crypto_profile_1_0_1_interop.py::...test_CI03_h_node_and_python_independent_implementations_match_expected
FAILED provider_outcome/test_c_crypto_profile_interop.py::...test_CI03_h_node_and_python_independent_implementations_match_expected
FAILED recovery_cutoff/test_i_crypto_profile.py::...test_CRYPTO_01_all_i_p0_families_match_node_rfc8785_and_ed25519

3 failed, 555 passed, 27 skipped, 1 error
```

底层 Node 报错毫无歧义：

```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'canonicalize'
```

**4. 装上该包后即修复。**

执行 `npm install canonicalize` 后，三个受影响文件通过：

```
13 passed in 0.73s
```

## 第二个独立问题：测试运行器用错

`recovery_cutoff/test_hrc_semantics.py` 在 pytest 下报 `ERROR ... fixture 'value' not found`。这不是该文件的缺陷：它定义了一个名为 `test_digest(value, domain=...)` 的普通辅助函数，pytest 把它当作测试收集，随后无法解析同名 fixture。

该文件自身的模块文档已规定运行方式：

```
Run:
    python -m unittest -v test_hrc_semantics.py
```

按文档运行器执行时是干净的：

```
Ran 44 tests in 0.008s
OK
```

因此套件存在两套调用契约——多数文件用 pytest，这一个用 unittest——而没有任何地方声明适用哪一套。用任一单一运行器跑整个目录都会产生一个假失败。

## 候选方向

### (a) 添加 `package.json` 锁定 `canonicalize`

让依赖真实且可复现的最小改动。参考实现仍为第三方，这正是跨语言独立校验的意义所在：它们不得复用 Rust 实现自身的规范化逻辑。

### (b) 内置一份自包含的 RFC 8785 实现

消除依赖，但若内置代码源自 Rust 一侧，则会削弱独立性主张。只有在项目要求零 npm 依赖时才值得。

### (c) 删除 Node 跨语言测试

丧失唯一的独立校验——即 Rust 规范化与另一实现是否一致。不建议：RFC 8785 分歧恰恰是只有第二实现才能抓到的那类缺陷。

## 建议

**(a)。** 在一致性测试旁添加 `package.json`，将 `canonicalize` 锁定到确切版本，并提交锁文件。同时让混合运行器问题显式化：要么把 `test_digest` 改名为 `digest`（它是辅助函数而非测试），要么添加 `pytest.ini`/`conftest.py` 将其排除。改名只需一行且无需配置。

项目应在 `protocol-index.md` 中声明每个目录期望的运行器，让"运行一致性套件"只有一个含义。

## 关闭标准

1. 在未预装 `node_modules` 的干净检出上，无需手工 `npm install` 即可通过完整一致性套件。
2. Node 依赖已锁定且锁文件已提交。
3. `test_hrc_semantics.py` 要么在 pytest 下干净通过，要么按目录记录运行器契约。
4. 报告套件通过数时必须附带运行器与依赖状态，以免未来的测量把这次的 3 个失败当作代码缺陷重演。
5. CI 必须真正执行那三个依赖 Node 的文件。一个从未被任何工作流安装过的依赖，
   与一个缺失的依赖没有区别。

## #546 之后的状态

仓库侧已完成：依赖已锁定并提交锁文件，辅助函数不再与 pytest 的测试收集冲突，工作流现在会执行此前未被覆盖的四份文件。

关闭标准 2、3、4 已满足，且每一条都在本机实测而非推断；测量结果附在该 PR 正文中。关闭标准 1 要求干净检出上自动安装依赖，关闭标准 5 要求 CI 真正执行那三个依赖 Node 的文件。两者都被同一次计费中断阻塞，而该中断不在本工作项范围内。

在被实测之前，本工作项保持开启。
