# -*- mode: python ; coding: utf-8 -*-

"""PyInstaller spec for the standalone DietaryIndex MCP server."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, EXE, PYZ


project_root = Path.cwd()
datas = collect_data_files("dietaryindex", includes=["data/*.csv"])
binaries = []
hiddenimports = []

hiddenimports += [
    "mcp.server.mcpserver",
    "mcp.server.lowlevel",
    "mcp.types",
    "mcp_types",
]

a = Analysis(
    [str(project_root / "dietaryindex" / "mcp_server.py")],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "tkinter", "webview"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="DietaryIndexMCP",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
)
