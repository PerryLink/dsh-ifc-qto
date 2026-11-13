# Changelog

## [0.2.0] — 2026-11-13

### Breaking

- **Tool names now use underscores instead of dots.** The separator in every
  name changed from `.` to `_`: `ifc` + `.` + `ingest` → `ifc_ingest`,
  `ifc` + `.` + `export_csv` → `ifc_export_csv`, and likewise for `qto_summary`
  and `unit_check`. The provider validates every `tools[].name` against
  `^[a-zA-Z0-9_-]+$`; a dotted name makes it reject the whole `tools` array
  (`Invalid 'tools[N].name'`), so the plugin registered but no request carrying
  the tools could succeed. Dotted aliases cannot be put on the wire, so no
  compatibility alias is kept: callers must migrate to the underscore names.
  This is the minor bump that the 0.1.x compatibility promise requires for a
  breaking change.
- Added `test/tool-name-wire.test.mjs`: every registered tool name must match
  `^[a-zA-Z0-9_-]+$`, contain no dot, stay in the `ifc_` namespace and be unique.
- README (five languages), `TROUBLESHOOTING.md`, the flow diagrams, the
  quickstart output, the acceptance script and the compact tool names in source
  and tests were updated with the rename.

## [0.1.0] — 2026-11-03

### Stable

- First non-alpha release: tool names and the CLI surface are covered by a
  compatibility promise (breaking changes require a minor bump).
- Ships a quickstart sample, a one-line prompt, a permission block and real captures.

## [0.1.0] — 2026-11-01

### Security / Fixes

- Release configuration hardening: wider host peer range and a build step before publish.


### Added

- Unit-declaration check tool: verify the model declares an `IFCUNITASSIGNMENT` with length, area and volume SI units before any take-off is trusted. Verified by `node --test test/*.test.mjs` (12/12).

## [Unreleased]

### Added

- Quantity take-off summary tool: quantity take-off summary for a stored model — totals/count/min/max per measurement kind, element-type distribution and non-positive quantity detection. Read-only; quantities follow the IFC 4.3 quantity-entity model. Verified by `node --test test/*.test.mjs` (9/9).

## [0.1.0-alpha.9] — 2026-11-01

### Changed

- Documentation: five-language fixture/acceptance links now resolve on npm; added specific related-checker/tool links.
- Marketplace metadata: taxonomy category, archetype, domains and status; docs page now shows the same.

All notable changes to `dsh-ifc-qto` are documented here. The format follows Keep a Changelog; this project uses alpha versions.

## [0.1.0-alpha.8] — 2026-11-01

### Added

- Five-language READMEs: English, 简体中文, Español, Português, हिन्दी.
- Local workflow SVG at `docs/assets/dsh-ifc-qto-flow.svg`.
- Family cross-links (domain index, checker family, `dsh-kit`), compatibility, permissions, and related-work sections.
- Standard repository files: `SECURITY.md`, `PRIVACY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `icon.svg`.

### Changed

- README aligned with the PerryLink DSH checker/plugin family style; package remains public/synthetic, alpha, not GA.

### Maintenance

- 2026-11-01: active again — feature work, hardening and fresh evidence resumed.

## [Earlier]

Earlier alpha builds are available from npm and GitHub Releases; this file starts at the family-standard documentation wave.
