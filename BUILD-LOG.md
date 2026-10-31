# BUILD-LOG — @perrylink/dsh-ifc-qto
## 2026-10-31 — S1
- 2 tools; ifc domain; CSV; test 2/2; gate 4/4. Publish pending.
### Publish verified
- dist-tags latest/next alpha.0; tarball install/layer passed.

### Public MIT IFC samples (2026-10-31)

- Added 2 MIT IFC samples under `fixtures/public/mit/` with licenses/source; `test/public-ifc.test.mjs` passes 2/2.
- Parser sees elements/types; the samples have no IFCQUANTITY entities, so they validate element ingestion, not quantity extraction.
