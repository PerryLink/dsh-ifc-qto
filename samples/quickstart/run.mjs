/**
 * PS1 quickstart: run the shipped sample through the real tool layer.
 *
 *   node samples/quickstart/run.mjs            # human-readable run (used for the screenshot)
 *   node samples/quickstart/run.mjs --json     # the gold JSON on stdout (used by scripts/acceptance.mjs)
 *
 * No network, no model, no customer data: the sample is hand-written synthetic IFC4.
 * Requires `pnpm build` (or `tsc -p tsconfig.json`) first because it imports lib/.
 */
import { createHash } from 'node:crypto'
import { mkdtempSync, readFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createTools } from '../../lib/plugin/tools.js'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..')
const jsonOnly = process.argv.includes('--json')
const sha256 = (value) => createHash('sha256').update(value).digest('hex')

class MemoryTable {
  constructor() { this.map = new Map() }
  get(key) { return this.map.get(key) }
  entries() { return this.map.entries() }
  get size() { return this.map.size }
  async put(key, value) { this.map.set(key, value) }
}

const sampleRel = 'samples/quickstart/input/sample-building.ifc'
const samplePath = path.join(root, sampleRel)
const ifcText = readFileSync(samplePath, 'utf8')
const sampleSha = sha256(ifcText)

const workDir = mkdtempSync(path.join(tmpdir(), 'dsh-ifc-qto-quickstart-'))
const exec = { callId: 'quickstart', agent: { id: 'quickstart' } }
const orMissing = (value) => value ?? 'missing'

try {
  const tools = createTools({ models: new MemoryTable(), baseDir: workDir })
  const byName = Object.fromEntries(tools.map((tool) => [tool.name, tool]))

  const units = await byName['ifc.unit_check'].execute({ ifc_text: ifcText }, exec)
  const ingested = await byName['ifc.ingest'].execute({ ifc_text: ifcText, source_name: 'sample-building.ifc' }, exec)
  const qto = await byName['ifc.qto_summary'].execute({ model_id: ingested.model_id }, exec)
  const exported = await byName['ifc.export_csv'].execute({ model_id: ingested.model_id }, exec)
  const csv = readFileSync(exported.path, 'utf8')

  const gold = {
    _note: 'Real tool output. The export path is normalised to exports/<file>.csv (the run directory is a temp dir); everything else is verbatim.',
    sample: { path: sampleRel, bytes: Buffer.byteLength(ifcText), sha256: sampleSha },
    units: {
      assignment: units.assignment,
      length: units.length,
      area: units.area,
      volume: units.volume,
      issues: units.issues,
    },
    ingest: { elements: ingested.elements, quantities: ingested.quantities, types: ingested.types },
    qto: { elements: qto.elements, quantities: qto.quantities, totals: qto.totals, issues: qto.issues },
    export: {
      path: `exports/${path.basename(exported.path)}`,
      rows: exported.rows,
      csv_sha256: exported.sha256,
    },
  }

  if (jsonOnly) {
    process.stdout.write(`${JSON.stringify(gold, null, 2)}\n`)
  } else {
    const typeLine = Object.entries(ingested.types).map(([type, count]) => `${type}:${count}`).join(' ')
    const kindLine = (kind) => {
      const t = qto.totals[kind]
      return t ? `${kind.padEnd(6)} qty=${t.count} total=${t.total} min=${t.min} max=${t.max}` : `${kind}: none`
    }
    console.log(`sample: ${sampleRel} (${Buffer.byteLength(ifcText)} B, sha256 ${sampleSha.slice(0, 16)}…)`)
    console.log('sample is synthetic: fictional project/element ids, no customer model')
    console.log(`ifc.unit_check   assignment=${units.assignment} length=${orMissing(units.length)} area=${orMissing(units.area)} volume=${orMissing(units.volume)} issues=${units.issues.length}`)
    console.log(`ifc.ingest       elements=${ingested.elements} quantities=${ingested.quantities} types=${typeLine}`)
    console.log(`ifc.qto_summary  ${kindLine('length')}`)
    console.log(`                 ${kindLine('area')}`)
    console.log(`                 ${kindLine('volume')}`)
    console.log(`data quality     ${qto.issues.length} issue(s): ${qto.issues.map((i) => `${i.code} ${i.name}=${i.value}`).join(', ') || 'none'}`)
    console.log(`ifc.export_csv   ${exported.rows} rows -> exports/${path.basename(exported.path)} (sha256 ${exported.sha256.slice(0, 16)}…)`)
    console.log(csv.trimEnd().split('\n').map((line) => `  ${line}`).join('\n'))
    console.log(`ok: quickstart finished (4 tool calls, ${qto.issues.length} data-quality issue)`)
  }
} finally {
  rmSync(workDir, { recursive: true, force: true })
}
