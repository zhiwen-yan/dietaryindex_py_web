# DietaryIndex Electron desktop host

This package replaces only the Windows desktop host. It deliberately reuses
the existing Next.js standalone site, loopback FastAPI service, and validated
Python compute engine.

## Development

Prepare the Next.js runtime once from the project root, then start Electron:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\prepare_desktop_runtime.ps1
cd electron_app
npm ci
npm start
```

The main process binds both local services to `127.0.0.1`, generates a new
random API token for every launch, and terminates the service processes when
the application exits. The renderer is sandboxed, has Node integration
disabled, and receives no filesystem or shell API.

## Windows release build

`npm run package` uses Electron Packager and the locally cached Electron ZIP
when available. It then explicitly writes and verifies all nine Electron v1
fuses before publishing `out/DietaryIndex-win32-x64`. The release configuration
disables RunAsNode, NODE_OPTIONS, CLI inspection, and extra `file://` privileges;
it enables cookie encryption, ASAR integrity validation, ASAR-only loading, and
WebAssembly trap handlers.

The project-level `scripts/build_windows_installer.ps1` also rebuilds the
Python sidecars, runs MCP and Electron smoke tests, and compiles the final Inno
Setup installer.
