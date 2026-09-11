# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.build_main import Analysis, COLLECT, EXE, PYZ


project_root = Path.cwd()
datas = []
binaries = []
hiddenimports = []


def collect_project_tree(source_dir: Path, prefix: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        relative_parent = path.relative_to(source_dir).parent
        target_dir = Path(prefix) / relative_parent if str(relative_parent) != "." else Path(prefix)
        results.append((str(path), str(target_dir)))
    return results

packages = [
    "webview",
]

for package in packages:
    pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(package)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hiddenimports

hiddenimports += [
    "uvicorn.logging",
    "uvicorn.loops.auto",
    "uvicorn.loops.asyncio",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan.on",
    "uvicorn.lifespan.off",
]

datas += collect_project_tree(project_root / "dietaryindex", "dietaryindex")
datas += collect_project_tree(project_root / "dietaryindex_api", "dietaryindex_api")
datas += collect_project_tree(project_root / "docs", "docs")
datas += collect_project_tree(project_root / "desktop_runtime", "desktop_runtime")
datas += [
    (str(project_root / "README.md"), "."),
    (str(project_root / "LICENSE"), "."),
    (str(project_root / "NOTICE"), "."),
    (str(project_root / "CITATION.cff"), "."),
]

a = Analysis(
    [str(project_root / "desktop_launcher.py")],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name="DietaryIndexLocal",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="DietaryIndexLocal",
)
