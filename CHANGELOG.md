# Changelog

## [0.1.0] — 2026-11-03

### Stable

- First non-alpha release: tool names and the CLI surface are covered by a
  compatibility promise (breaking changes require a minor bump).
- Ships a quickstart sample, a one-line prompt, a permission block and real captures.

## [0.1.0] — 2026-11-01

### Security / Fixes

- Release configuration hardening: wider host peer range and a build step before publish.


### Added

- `ifc.unit_check`: verify the model declares an `IFCUNITASSIGNMENT` with length, area and volume SI units before any take-off is trusted. Verified by `node --test test/*.test.mjs` (12/12).

## [Unreleased]

### Added

- `ifc.qto_summary`: quantity take-off summary for a stored model — totals/count/min/max per measurement kind, element-type distribution and non-positive quantity detection. Read-only; quantities follow the IFC 4.3 quantity-entity model. Verified by `node --test test/*.test.mjs` (9/9).

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
