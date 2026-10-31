# dsh-ifc-qto

> 🧊 **FROZEN — 2026-10-31. No new features.** This public/synthetic S1 demo is not GA; it stays installable and only genuine breakage is fixed.

## Maintenance status: 🧊 FROZEN

Frozen on 2026-10-31. This repository is a public/synthetic S1 demo, not a validated product. The npm package stays installable; no new features are planned.


IFC (ISO-10303-21) element/quantity inventory and CSV takeoff for DeepSeek Harness.

> **Status: alpha / public-synthetic / partial / not counted / not GA.** No customer evidence, customer data, or production-readiness claim. All acceptance rows are `counted=false`.

## Install

```sh
dsh plugin --profile <profile> add dsh-ifc-qto
dsh --profile <profile> --dump-config | grep dsh-ifc-qto
```

Requires DSH `>=0.2.1-rc.3 <0.3.0` and Node `>=24.9 <25`.

<details>
<summary>中文摘要</summary>

IFC 构件/工程量清单与 CSV 导出。 安装：`dsh plugin --profile <profile> add dsh-ifc-qto`。公开/合成、alpha、非 GA。

</details>

## Tools

| Tool | What it does | Risk |
|---|---|---|
| `ifc.ingest` | Parse an IFC file and inventory elements and quantity properties | R1 local write |
| `ifc.export_csv` | Export the element/quantity inventory as CSV | R1 local write |

## Input / output

**Input:** an IFC (ISO-10303-21) file. **Output:** an element/quantity inventory and a CSV takeoff. Quantities depend on the properties present in the IFC file; missing quantities are reported as missing, not guessed.

## Configuration

| Env | Default | Meaning |
|---|---|---|
| `DSH_IFC_HOME` | `$DSH_HOME/storages/dsh-ifc-qto` | local domain and exports |

## Limits / non-claims

- No geometry engine, WASM kernel, rendering, or 50k-element performance claim.
- No BCF, model federation, or Client surface.
- Public MIT/Apache IFC samples only; no customer model.
- No customer evidence, customer data, or production-readiness claim; all fixtures are public/synthetic.

## Public sample

4 MIT/Apache IFC samples with quantity-bearing models; `ACCEPTANCE.csv` lists 5 public checks.

## 中文说明

IFC（ISO-10303-21）构件/工程量清单与 CSV 导出。**公开/合成、alpha、非 GA**；没有客户模型。

### 安装

```sh
dsh plugin --profile <profile> add dsh-ifc-qto
```

### 工具

| 工具 | 作用 |
|---|---|
| `ifc.ingest` | 解析 IFC，盘点构件与工程量属性 |
| `ifc.export_csv` | 导出构件/工程量 CSV |

### 输入 / 输出

输入一个 IFC 文件；输出构件/工程量清单与 CSV。数量取决于 IFC 中实际存在的属性，缺失就报缺失，不猜。

### 边界

- 不做几何引擎、WASM、渲染，也没有“5 万构件”性能承诺。
- 不做 BCF、模型合模、Client。
- 只有 MIT/Apache 公开 IFC 样例，没有客户模型。

## Development

```sh
pnpm install --frozen-lockfile
pnpm build && pnpm lint && pnpm typecheck && pnpm test && pnpm gate:sku07
```

## License

Apache-2.0. See `LICENSE`, `NOTICE`, `THIRD-PARTY-NOTICES`.
