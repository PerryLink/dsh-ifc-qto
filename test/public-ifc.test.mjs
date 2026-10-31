import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, readdirSync } from 'node:fs'
import path from 'node:path'
import { parseIfc } from '../lib/core/ifc.js'

const dir = path.resolve(process.cwd(), 'fixtures/public/mit')
for (const name of readdirSync(dir).filter((file) => file.endsWith('.ifc')).sort()) {
  test(`public MIT IFC: ${name}`, () => {
    const model = parseIfc(readFileSync(path.join(dir, name), 'utf8'))
    assert.ok(model.elements.length > 0)
    assert.ok(Object.keys(model.types).length > 0)
  })
}
