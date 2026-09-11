# DietaryIndex-Py 0.2.0 release candidate

> Historical build record. Scientific corrections made on 2026-08-13 changed
> the source after these artifacts were built. Rebuild and create a new
> manifest before distributing a release candidate.

Build date: 2026-08-09
Status: **release-candidate engineering checks passed**

## Acceptance evidence

| Check | Result |
|---|---:|
| Python test suite | 89 passed, 1 third-party deprecation warning |
| Base index registry | 32 |
| API catalogue | 40 version-aware entries |
| CLI catalogue | 40 version-aware entries |
| Canonical score scales | 40/40 entries |
| API health | PASS |
| Next.js site health | PASS |
| Next.js TypeScript check | PASS |
| npm high-severity audit | 0 vulnerabilities |
| Source MCP smoke | 7/7 tools PASS |
| Packaged desktop smoke | PASS |
| Packaged MCP smoke | 7/7 tools PASS |

Python 3.9 is no longer an advertised environment. The package requires Python
3.10 or newer; the release build used Python 3.12.10 and MCP 1.29.0.

The packaged MCP process emits a non-fatal closed-STDIO cleanup warning after
the smoke client has already completed all seven calls; its exit status remains
0. This is recorded as a packaging warning, not a functional failure.

Installer hashes and byte sizes are stored in `docs/release_manifest_0.2.0.json`
and can be checked with `python scripts/verify_release_manifest.py`.
Independent scientific validation is maintained in the sibling
`dietaryindex_validation/` project and is not bundled into the application.
