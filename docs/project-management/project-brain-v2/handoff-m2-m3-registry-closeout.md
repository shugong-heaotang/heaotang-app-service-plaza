# Project Brain v2 M2-M3 registry closeout Handoff

- exact base：`05eda778a08f6a4d63dd01a3f7511746e1f42c7a`
- 状态：registry-only candidate；不是authority，不激活M4/M5

## 必须独立验证

- authority中已存在M2 exact `d1531da...`与M3 exact `05eda77...`；
- 仅M2 remediation和M3 dashboard两个既有对象发生约定字段变化，只新增一个closeout对象；
- 其余全部既有对象、allowed paths及顶层字段逐字段不变；
- closeout恰7类路径，无active registry overlap；
- checklist、Exam、IR、合同、UTF-8、diff、secret、freshness全部通过。

独立Go前不得推送或集成；集成后下一阶段仍须另行激活M4，不得把本closeout解释为生产授权。

## 当前候选冻结前证据

- H1 exclusive lease已由中央在`2026-07-17T16:06:00.5863917+08:00`显式释放；lease内push count=`0`，H1 candidate=`none`，R4 preflight=`No-Go`；本closeout不修改或重标该失败证据；
- release后fresh remote仍为`05eda778a08f6a4d63dd01a3f7511746e1f42c7a`；
- current checklist=`26/26`，逐文件SHA-256 mismatch=`0`；
- governance exam=`EX-20260717-PROJECT-BRAIN-V2-M2-M3-REGISTRY-CLOSEOUT-1`，attempt 1，`8/8`，score=`100`，status=`passed`；
- implementation record=`IR-20260717-PROJECT-BRAIN-V2-M2-M3-REGISTRY-CLOSEOUT`，status=`verified`；
- registry semantic diff：`154 -> 155`，added精确一个closeout，removed=`0`，152个既有对象不变，只修改M2 remediation与M3 dashboard约定字段；
- changed paths=`7`，forbidden paths=`0`，新增secret pattern=`0`；
- collaboration、exam、IR、Service Plaza总合同、UTF-8 1648 files及`git diff --check`均通过；
- 仓库级checklist `--require-current`另有历史旧清单stale findings，本工作项不扩大范围修改，也不把这些旧债描述为通过；本current checklist已单独复算为0 mismatch。

exact candidate必须由Git提交后记录在独立验收报告中；本Handoff不预造循环引用的commit hash。candidate形成后仍须由未参与写入的reviewer按base、ancestry、七类路径、registry语义、历史报告hash和全部门禁独立复跑。
