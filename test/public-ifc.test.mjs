import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, readdirSync } from 'node:fs'
import path from 'node:path'
import { parseIfc } from '../lib/core/ifc.js'

const dir = path.resolve(process.cwd(), 'fixtures/public/mit')
for (const name of readdirSync(dir).filter((file) => file.endsWith('.ifc')).sort()) {
  test(`public MIT/Apache IFC: ${name}`, () => {
    const model = parseIfc(readFileSync(path.join(dir, name), 'utf8'))
    assert.ok(model.elements.length + model.quantities.length > 0)
    assert.ok(Object.keys(model.types).length > 0 || model.quantities.length > 0)
    if (name === 'wall-precision-legacy.ifc') assert.ok(model.quantities.length > 0)
  })
}
