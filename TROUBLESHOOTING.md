# Troubleshooting — dsh-ifc-qto

每条错误都按 **症状 / 原因 / 动作** 三行写。错误格式：`<一句人话>（E_IFC_…）｜下一步：<一个动作>`。
日志在 `$DSH_HOME/storages/dsh-ifc-qto/` 下；报告问题时只发合成样例，**不要附加真实模型或客户数据**。

---

## E_IFC_UNREADABLE — 这不像 IFC 文件

- **症状**：`ifc.ingest` 直接失败，提示「这不像 IFC 文件（E_IFC_UNREADABLE）｜下一步：…」。
- **原因**：传来的不是 ISO-10303-21 文本 —— 例如另存成了二进制、把 `.rvt`/`.dwg` 改了后缀，或者文件被截断。
- **动作**：用文本编辑器确认首行是 `ISO-10303-21;`、并且有 `FILE_SCHEMA(('IFC4'))`；不是就回建模软件重新导出 IFC4。先用 `samples/quickstart/input/sample-building.ifc` 确认插件本身可用。

## E_IFC_UNREADABLE — 找不到这个模型

- **症状**：`ifc.qto_summary` / `ifc.export_csv` 提示「找不到这个模型（E_IFC_UNREADABLE）｜下一步：…」。
- **原因**：`model_id` 不存在或不是本次会话导入的（工具只认 `ifc.ingest` 返回的 id，不认文件路径）。
- **动作**：重新跑 `ifc.ingest`，把返回的 `model_id` 原样传给汇总/导出工具。

## E_IFC_EMPTY — 这个文件是空的

- **症状**：工具提示「这个文件是空的（E_IFC_EMPTY）｜下一步：…」。
- **原因**：文件 0 字节，或复制过程中被清空。
- **动作**：确认文件大小 > 0；重新从导出方拿一份，或改用自带样例。

## E_IFC_EXPORT_FAILED — CSV 没写出去

- **症状**：`ifc.export_csv` 提示「CSV 没写出去（E_IFC_EXPORT_FAILED）｜下一步：…」。
- **原因**：写入目录不可写（权限、只读挂载、磁盘满）。
- **动作**：把 `DSH_IFC_HOME` 指向一个可写目录后重试；不要写进只读仓库目录。

## E_IFC_QUANTITY_NON_POSITIVE — 工程量有 0 或负数

- **症状**：`ifc.qto_summary` 的 `issues` 里出现 `E_IFC_QUANTITY_NON_POSITIVE`（自带样例里是 `NetSideArea=0`）。
- **原因**：模型里漏填工程量，或导出时把空值写成了 0；也可能是负数（扣减算错）。
- **动作**：回模型核对该构件的量，修正后重新导出。**这不影响其余构件的汇总**，只是提示这一条不可直接用于报量。

## E_IFC_UNITASSIGNMENT_MISSING / E_IFC_LENGTHUNIT_MISSING / E_IFC_AREAUNIT_MISSING / E_IFC_VOLUMEUNIT_MISSING — 单位声明不全

- **症状**：`ifc.unit_check` 返回 `assignment=false`，或 `issues` 里出现上述代码。
- **原因**：模型没有 `IfcUnitAssignment`，或缺长度/面积/体积的 `IfcSIUnit`。没有单位，算出来的量不能直接用于报量。
- **动作**：在建模软件里设置项目单位后重新导出；至少补齐 `IfcSIUnit(*,.LENGTHUNIT.,.MILLI.,.METRE.)`、`.AREAUNIT.`、`.VOLUMEUNIT.` 三项。

---

## 装不上 / 启用不了

- **症状**：`dsh plugin add dsh-ifc-qto` 报版本不满足。
- **原因**：Node 或 DSH 版本低于包要求（`node >=24.9 <25`，`dsh >=0.2.1-rc.3 <0.4.0`）。
- **动作**：`node --version`、`dsh --version` 各看一次；升级后重试，并用 `dsh --profile <profile> --dump-config | grep dsh-ifc-qto` 确认已启用。

## 跑测试

```sh
pnpm install --frozen-lockfile
pnpm build && node --test test/*.test.mjs
```

## 报告

到 <https://github.com/PerryLink/dsh-ifc-qto/issues> 提交：包版本、命令、报错原文、一份**合成** `.ifc`。真实项目模型请先脱敏，或只描述结构。
