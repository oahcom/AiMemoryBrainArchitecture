---
name: Work item with AI session evidence
about: An Issue that a PR will link. Declares whether AI assisted the work and where the session evidence lives.
title: ""
labels: ""
assignees: ""
---

<!--
`AI-assisted work` and `Session evidence reference(s)` are read verbatim by
`scripts/governance/session_evidence/validate.py`: the heading is the field
name, the first non-empty line below it is the value. Keep both headings.
-->

## Summary

<!-- What this Issue asks for, and why. -->

## AI-assisted work

YES | NO

## Session evidence reference(s)

`path/to/session/evidence.md` — or `N/A` when the line above is `NO`

## Related issue(s)

#NNN

## Acceptance criteria

<!-- How a reviewer can tell this is done. -->

---

This template is not a hard gate. `/session-evidence` reads the declaration
above only on an Issue created after the gate's effective time and linked by
a PR; every other Issue is never read by it.
本模板不构成强制门禁：门禁只校验「生效时间之后创建、且被某个 PR 链接」的 Issue 的声明，
其余 Issue 不会被读取。
