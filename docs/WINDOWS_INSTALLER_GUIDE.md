# Windows Installer Guide

## What this delivers

Version 0.3.0 packages the project as a Windows local-first Electron app:

1. The user double-clicks `DietaryIndexElectronSetup-<version>.exe`
2. The installer adds a desktop shortcut
3. The user clicks the shortcut
4. Electron starts the bundled Next.js site and FastAPI service on loopback-only ports
5. The application opens in a sandboxed Electron renderer
6. The installer optionally registers the packaged STDIO MCP server for Codex

The interface uses web technology, but all computation and runtime data stay local by default.

## Build requirements

You only need these on the build machine:

- Python 3.10+
- Node.js 22.12+ (the build script uses the bundled Node 22 runtime)
- PyInstaller
- Inno Setup 6

The end user does not need Python.

## Build steps

From the project root:

1. Run `scripts\build_windows_installer.bat`
2. PyInstaller produces `dist\DietaryIndexBackend.exe` and `dist\DietaryIndexMCP.exe`
3. Electron Packager produces `electron_app\out\DietaryIndex-win32-x64\`
4. The pipeline runs MCP and packaged-Electron smoke tests
5. Inno Setup produces `dist\installer\DietaryIndexElectronSetup-<version>.exe`

## Source-mode Electron host

Before building the installer, you can test the desktop-style workflow from source:

1. Run `scripts\prepare_desktop_runtime.ps1`
2. Run `npm ci` in `electron_app`
3. Run `npm start` in `electron_app`

This opens the same Electron host logic that the packaged app uses.

## End-user experience

After installation, the user will be able to:

- open the home page
- open the FII database
- open the first-use guide
- use the local FastAPI service through the authenticated Next.js proxy
- stop all owned local services by closing the application
- register the packaged MCP server for Codex

## Local data location

The packaged app stores runtime files here:

`%LOCALAPPDATA%\DietaryIndex\`

That folder contains:

- `runtime_data\`
- `mcp_results\` (when MCP tools write result files)

## Current limitations

- This is a Windows delivery path
- The current installer targets Windows x64-compatible systems
- Large scientific dependencies can make the installer fairly large
- Code signing is not included yet

## Recommended next polish

1. Add a custom app icon
2. Add a branded installer bitmap
3. Add versioned release notes
4. Add code signing before public release
5. Add an installed/uninstalled virtual-machine acceptance test
