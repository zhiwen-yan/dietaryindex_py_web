# DietaryIndex-Py 0.3.0

Released: 2026-09-11

## Scope

Version 0.3.0 is an engineering and access-layer release built on the frozen
v0.2.1 scientific results. It does not change the previously approved dietary
index formula results.

## Desktop

- Replaced the distributed pywebview/WebView2 host with Electron 43.
- Retained the validated Python calculation engine, FastAPI service, and Next.js interface.
- Added a one-file FastAPI sidecar, bundled Node/Next runtime, process cleanup,
  randomized loopback API tokens, strict navigation/permission rules, context
  isolation, sandboxing, ASAR integrity validation, and Electron fuses.
- Added source and packaged smoke tests plus an Electron-aware Windows installer build.

## MCP

- Migrated to the official Python MCP SDK 2.0.
- Restricted inputs to configured roots and outputs to a dedicated root.
- Added single-file, combined-size, file-count, and structured-payload limits.
- Added source and packaged STDIO tests for all seven tools and path-policy enforcement.

## Verification

- Python test suite: 97 tests.
- Six-interface HEI-2020 parity: Python, CLI, REST API, Next.js Web proxy,
  packaged Electron, and packaged MCP all produced identical participant scores
  at an absolute tolerance of 1e-12.
- The v0.2.1 formula-validation and independent dual-review freeze remains the
  scientific result authority; v0.3.0 adds a separate engineering freeze.

## Source snapshot correction (2026-09-11)

- Vendored the complete NHANES FNDDS codebooks used by the DASH, MEDI, and
  DI-GM FPED adapters. Standalone source and packaged builds no longer depend
  on a sibling R-source checkout or silently fall back to incomplete lists.
- Added a release regression test for all 15 vendored codebooks and an optional
  raw-NHANES-to-archived-R parity command.
- Recomputed 6,488 paired NHANES participants: DASH, MEDI, and DI-GM
  (`score_average`) were exact across every common result column; AHEI remained
  within `5.898e-12` in the current SAS/XPT reader environment.
- Standardized the validation-N definition and corrected the legacy summary
  counts. See `ACCURACY_AUDIT_2026-09-11.md`.
- Registered all 40 service entries in the Next.js release-consistency list;
  the 8 explicit `_V1` / `_V2` entries remain presented through the existing
  version selector.
- Updated Next.js from 16.3.0 to 16.3.4 and the `sharp` override from 0.35.0
  to 0.35.4. The refreshed production dependency audit reports zero known
  vulnerabilities.
- Full container verification after the correction: 99 Python tests passed
  with one upstream deprecation warning; the Next.js production build and
  TypeScript check passed.

Installers built before this correction must be rebuilt before distribution.

## Production release (2026-09-11)

- Published release `v0.3.0-20260911` at <https://dietaryindex.org> using the
  Next.js site and authenticated FastAPI service.
- Removed the legacy Streamlit application, dependencies, container, image,
  port, source directory, and reverse-proxy route from the production release.
- Published the rebuilt Electron installer and packaged seven-tool MCP server;
  install, upgrade, calculation, registration, cleanup, and uninstall checks passed.
- Set English as the default language for first-time visitors while retaining
  explicit URL selection and previously saved English or Chinese preferences.
- Public acceptance covered all 40 service entries, upload and computation,
  CSV/XLSX downloads, release downloads with byte ranges, and a 15-minute
  zero-restart observation window.
