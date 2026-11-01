import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'

class T { map = new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }
const model = (quantities) => ['ISO-10303-21;', "FILE_SCHEMA(('IFC4'));",
  "#100=IFCWALL('g1',#1,'E1','x');", "#101=IFCSLAB('g2',#1,'E2','x');", ...quantities,
  'ENDSEC;', 'END-ISO-10303-21;'].join('\n')

test('totals are grouped per measurement kind', async () => {
  const tools = Object.fromEntries(createTools({ models: new T(), baseDir: '/tmp/ifc-qto' }).map((t) => [t.name, t]))
  const ingested = await tools['ifc.ingest'].execute({ ifc_text: model(["#900=IFCQUANTITYLENGTH('Length',$,10.5,$);", "#901=IFCQUANTITYLENGTH('Length2',$,4.5,$);", "#902=IFCQUANTITYAREA('NetSideArea',$,21.0,$);", "#903=IFCQUANTITYVOLUME('NetVolume',$,5.25,$);"]) }, { callId: 'q' })
  const r = await tools['ifc.qto_summary'].execute({ model_id: ingested.model_id }, { callId: 'q' })
  assert.equal(r.elements, 2)
  assert.equal(r.quantities, 4)
  assert.equal(r.totals.length.count, 2)
  assert.equal(r.totals.length.total, 15)
  assert.equal(r.totals.length.min, 4.5)
  assert.equal(r.totals.length.max, 10.5)
  assert.equal(r.totals.area.total, 21)
  assert.equal(r.totals.volume.total, 5.25)
  assert.equal(r.types.WALL, 1)
  assert.equal(r.issues.length, 0)
})

test('non-positive quantities are reported as data-quality issues', async () => {
  const tools = Object.fromEntries(createTools({ models: new T(), baseDir: '/tmp/ifc-qto' }).map((t) => [t.name, t]))
  const ingested = await tools['ifc.ingest'].execute({ ifc_text: model(["#900=IFCQUANTITYAREA('NetSideArea',$,0,$);"]) }, { callId: 'q' })
  const r = await tools['ifc.qto_summary'].execute({ model_id: ingested.model_id }, { callId: 'q' })
  assert.equal(r.issues.length, 1)
  assert.equal(r.issues[0].code, 'E_IFC_QUANTITY_NON_POSITIVE')
  assert.equal(r.issues[0].value, 0)
})

test('unknown model id is rejected', async () => {
  const tools = Object.fromEntries(createTools({ models: new T(), baseDir: '/tmp/ifc-qto' }).map((t) => [t.name, t]))
  await assert.rejects(() => tools['ifc.qto_summary'].execute({ model_id: 'nope' }, { callId: 'q' }), /E_IFC_UNREADABLE/)
})
