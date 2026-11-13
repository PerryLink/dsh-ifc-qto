import test from 'node:test'
import assert from 'node:assert/strict'
import { checkUnits } from '../lib/core/ifc.js'
import { createTools } from '../lib/plugin/tools.js'

const withUnits = [
  'ISO-10303-21;', "FILE_SCHEMA(('IFC4'));",
  '#1=IFCSIUNIT(*,.LENGTHUNIT.,.MILLI.,.METRE.);',
  '#2=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);',
  '#3=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);',
  '#4=IFCUNITASSIGNMENT((#1,#2,#3));',
  'ENDSEC;', 'END-ISO-10303-21;',
].join('\n')
const withoutUnits = 'ISO-10303-21;\nFILE_SCHEMA((\'IFC4\'));\n#1=IFCWALL(\'g\',#2,\'W\',\'x\');\nENDSEC;\nEND-ISO-10303-21;'

test('a model with the three SI units passes', () => {
  const r = checkUnits(withUnits)
  assert.equal(r.assignment, true)
  assert.equal(r.length.prefix, 'MILLI')
  assert.equal(r.length.unit, 'METRE')
  assert.equal(r.area.unit, 'SQUARE_METRE')
  assert.equal(r.volume.unit, 'CUBIC_METRE')
  assert.deepEqual(r.issues, [])
})

test('a model without units reports every missing piece', () => {
  const r = checkUnits(withoutUnits)
  assert.equal(r.assignment, false)
  assert.ok(r.issues.includes('E_IFC_UNITASSIGNMENT_MISSING'))
  assert.ok(r.issues.includes('E_IFC_LENGTHUNIT_MISSING'))
  assert.ok(r.issues.includes('E_IFC_AREAUNIT_MISSING'))
  assert.ok(r.issues.includes('E_IFC_VOLUMEUNIT_MISSING'))
})

test('the tool returns the same verdict with compact unit strings', async () => {
  const tools = Object.fromEntries(createTools({ models: { map: new Map(), get(){}, entries(){ return [] }, put(){} }, baseDir: '/tmp/ifc-units' }).map((t) => [t.name, t]))
  const r = await tools['ifc_unit_check'].execute({ ifc_text: withUnits }, { callId: 'u' })
  assert.equal(r.assignment, true)
  assert.equal(r.length, 'MILLI|METRE')
  assert.equal(r.issues.length, 0)
})
