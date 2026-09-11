"""Windows desktop host for the Next.js + FastAPI DietaryIndex application."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path
from typing import Callable

import psutil


APP_NAME = "DietaryIndex"
SITE_KIND = "site"
API_KIND = "api"
DEFAULT_SITE_PORT = 3210
DEFAULT_API_PORT = 8210
MAX_LOG_BYTES = 5 * 1024 * 1024
MUTEX_NAME = "Local\\DietaryIndexDesktop-9AF0974C-69D9-48A2-AF56-D47E2E14F06B"
_mutex_handle: int | None = None


def _source_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parent


def _acquire_single_instance() -> bool:
    """Keep one desktop window alive so windows cannot stop each other's services."""
    global _mutex_handle
    if os.name != "nt":
        return True
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if not handle:
        return False
    if ctypes.get_last_error() == 183:
        kernel32.CloseHandle(ctypes.c_void_p(handle))
        return False
    _mutex_handle = int(handle)
    return True


def _release_single_instance() -> None:
    global _mutex_handle
    if os.name == "nt" and _mutex_handle:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CloseHandle(ctypes.c_void_p(_mutex_handle))
        _mutex_handle = None


def _local_app_root() -> Path:
    base = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    root = base / "DietaryIndexLocal"
    for child in ("runtime_data", "logs", "state", "webview"):
        (root / child).mkdir(parents=True, exist_ok=True)
    return root


SOURCE_ROOT = _source_root()
LOCAL_ROOT = _local_app_root()
STATE_DIR = LOCAL_ROOT / "state"
LOG_DIR = LOCAL_ROOT / "logs"
RUNTIME_DIR = LOCAL_ROOT / "runtime_data"
WEBVIEW_DIR = LOCAL_ROOT / "webview"
DESKTOP_RUNTIME = SOURCE_ROOT / "desktop_runtime"
SITE_ROOT = DESKTOP_RUNTIME / "site"
NODE_EXE = DESKTOP_RUNTIME / "node" / ("node.exe" if os.name == "nt" else "node")


def _state_path(kind: str) -> Path:
    return STATE_DIR / f"{kind}.json"


def _log_paths(kind: str) -> tuple[Path, Path]:
    return LOG_DIR / f"{kind}.log", LOG_DIR / f"{kind}.err.log"


def _rotate_log(path: Path) -> None:
    if not path.exists() or path.stat().st_size < MAX_LOG_BYTES:
        return
    backup = path.with_suffix(path.suffix + ".1")
    backup.unlink(missing_ok=True)
    path.replace(backup)


def _process_matches(kind: str, payload: dict) -> bool:
    try:
        process = psutil.Process(int(payload["pid"]))
        if not process.is_running() or process.status() == psutil.STATUS_ZOMBIE:
            return False
        expected_created = float(payload.get("created", 0))
        if expected_created and abs(process.create_time() - expected_created) > 2:
            return False
        command = " ".join(process.cmdline()).lower()
        marker = "server.js" if kind == SITE_KIND else "--serve-api"
        return marker in command
    except (psutil.Error, KeyError, TypeError, ValueError):
        return False


def _save_state(kind: str, process: subprocess.Popen, port: int) -> None:
    try:
        created = psutil.Process(process.pid).create_time()
    except psutil.Error:
        created = time.time()
    _state_path(kind).write_text(
        json.dumps({"pid": process.pid, "port": port, "created": created}, indent=2),
        encoding="utf-8",
    )


def _load_state(kind: str) -> dict | None:
    path = _state_path(kind)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        path.unlink(missing_ok=True)
        return None
    if not _process_matches(kind, payload):
        path.unlink(missing_ok=True)
        return None
    return payload


def _stop_service(kind: str) -> None:
    state = _load_state(kind)
    _state_path(kind).unlink(missing_ok=True)
    if not state:
        return
    try:
        parent = psutil.Process(int(state["pid"]))
        processes = parent.children(recursive=True)
        processes.append(parent)
        for process in reversed(processes):
            try:
                process.terminate()
            except psutil.Error:
                pass
        _, alive = psutil.wait_procs(processes, timeout=5)
        for process in alive:
            try:
                process.kill()
            except psutil.Error:
                pass
    except psutil.Error:
        return


def _is_url_ready(url: str, timeout: float = 1.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return 200 <= response.status < 400
    except Exception:
        return False


def _is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def _choose_port(preferred: int) -> int:
    for port in range(preferred, preferred + 50):
        if _is_port_available(port):
            return port
    raise RuntimeError(f"No local port is available near {preferred}.")


def _wait_for(url: str, seconds: float, status: Callable[[str], None] | None = None) -> bool:
    deadline = time.time() + seconds
    while time.time() < deadline:
        if _is_url_ready(url):
            return True
        if status:
            status(f"正在启动本地服务… {max(0, int(deadline - time.time()))} 秒")
        time.sleep(0.35)
    return False


def _creation_flags() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)


def _api_child_command(port: int) -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, "--serve-api", "--port", str(port)]
    return [sys.executable, str(Path(__file__).resolve()), "--serve-api", "--port", str(port)]


def _spawn(kind: str, command: list[str], port: int, cwd: Path, env: dict[str, str]) -> None:
    stdout_path, stderr_path = _log_paths(kind)
    _rotate_log(stdout_path)
    _rotate_log(stderr_path)
    with stdout_path.open("a", encoding="utf-8") as stdout_handle, stderr_path.open("a", encoding="utf-8") as stderr_handle:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=env,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=_creation_flags(),
        )
    _save_state(kind, process, port)


def _ensure_api(status: Callable[[str], None] | None = None) -> tuple[str, int]:
    state = _load_state(API_KIND)
    if state:
        port = int(state["port"])
        url = f"http://127.0.0.1:{port}"
        if _is_url_ready(f"{url}/healthz"):
            return url, port
        _stop_service(API_KIND)

    port = _choose_port(DEFAULT_API_PORT)
    env = os.environ.copy()
    env["DIETARYINDEX_RUNTIME_DIR"] = str(RUNTIME_DIR)
    env["DIETARYINDEX_DESKTOP_MODE"] = "1"
    _spawn(API_KIND, _api_child_command(port), port, SOURCE_ROOT, env)
    url = f"http://127.0.0.1:{port}"
    if not _wait_for(f"{url}/healthz", 30, status):
        _stop_service(API_KIND)
        _, error_log = _log_paths(API_KIND)
        raise RuntimeError(f"计算服务启动失败，请检查：\n{error_log}")
    return url, port


def _validate_site_runtime() -> None:
    missing = [path for path in (NODE_EXE, SITE_ROOT / "server.js") if not path.exists()]
    if missing:
        details = "\n".join(str(path) for path in missing)
        raise RuntimeError(
            "桌面网站运行资源尚未生成。\n"
            "源码模式请先运行 scripts\\prepare_desktop_runtime.ps1。\n\n"
            f"缺少：\n{details}"
        )


def _ensure_site(api_url: str, status: Callable[[str], None] | None = None) -> tuple[str, int]:
    _validate_site_runtime()
    state = _load_state(SITE_KIND)
    if state:
        port = int(state["port"])
        url = f"http://127.0.0.1:{port}"
        if _is_url_ready(url):
            return url, port
        _stop_service(SITE_KIND)

    port = _choose_port(DEFAULT_SITE_PORT)
    env = os.environ.copy()
    env.update(
        {
            "NODE_ENV": "production",
            "NEXT_TELEMETRY_DISABLED": "1",
            "HOSTNAME": "127.0.0.1",
            "PORT": str(port),
            "DIETARYINDEX_API_INTERNAL_URL": api_url,
            "DIETARYINDEX_DESKTOP_MODE": "1",
        }
    )
    _spawn(SITE_KIND, [str(NODE_EXE), "server.js"], port, SITE_ROOT, env)
    url = f"http://127.0.0.1:{port}"
    if not _wait_for(url, 30, status):
        _stop_service(SITE_KIND)
        _, error_log = _log_paths(SITE_KIND)
        raise RuntimeError(f"桌面网站启动失败，请检查：\n{error_log}")
    return url, port


def _ensure_desktop_services(status: Callable[[str], None] | None = None) -> str:
    if status:
        status("正在启动计算服务…")
    api_url, _ = _ensure_api(status)
    if status:
        status("正在启动桌面网站…")
    site_url, _ = _ensure_site(api_url, status)
    return site_url


def _ensure_source_importable() -> None:
    source = str(SOURCE_ROOT)
    if source not in sys.path:
        sys.path.insert(0, source)


def run_api_server(port: int) -> None:
    _ensure_source_importable()
    import uvicorn
    from dietaryindex_api.app import app

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


class Splash:
    def __init__(self) -> None:
        import tkinter as tk

        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry("430x170")
        self.root.resizable(False, False)
        self.root.configure(bg="#fefcf8")
        tk.Label(self.root, text="DietaryIndex", bg="#fefcf8", fg="#1a6b56", font=("Segoe UI", 21, "bold")).pack(pady=(28, 6))
        self.status = tk.StringVar(value="正在准备桌面应用…")
        tk.Label(self.root, textvariable=self.status, bg="#fefcf8", fg="#5a5a5a", font=("Microsoft YaHei UI", 10)).pack()
        self.root.update()

    def update(self, text: str) -> None:
        self.status.set(text)
        self.root.update()

    def close(self) -> None:
        self.root.destroy()


def _run_browser_fallback(site_url: str, reason: Exception) -> None:
    """Keep the application usable when the WebView2 runtime is unavailable."""
    import tkinter as tk

    webbrowser.open(site_url)
    root = tk.Tk()
    root.title(f"{APP_NAME} - 浏览器兼容模式")
    root.geometry("520x230")
    root.resizable(False, False)
    root.configure(bg="#fefcf8")
    tk.Label(
        root,
        text="已切换到浏览器兼容模式",
        bg="#fefcf8",
        fg="#1a6b56",
        font=("Microsoft YaHei UI", 16, "bold"),
    ).pack(pady=(28, 10))
    tk.Label(
        root,
        text="系统未能启动 WebView2 桌面窗口，网站已在默认浏览器打开。\n"
        "关闭此控制窗口时，本地计算服务也会停止。",
        bg="#fefcf8",
        fg="#4f4f4f",
        font=("Microsoft YaHei UI", 10),
        justify="center",
    ).pack()
    tk.Label(
        root,
        text=f"原因：{reason}",
        bg="#fefcf8",
        fg="#8a6a3f",
        font=("Microsoft YaHei UI", 8),
        wraplength=460,
    ).pack(pady=(10, 12))
    tk.Button(root, text="关闭 DietaryIndex", command=root.destroy, width=22).pack()
    root.mainloop()


def run_desktop() -> int:
    if not _acquire_single_instance():
        from tkinter import messagebox

        messagebox.showinfo(APP_NAME, "DietaryIndex 已经在运行。")
        return 0

    splash = Splash()
    try:
        site_url = _ensure_desktop_services(splash.update)
        splash.update("正在打开桌面窗口…")
        import webview

        splash.close()
        try:
            webview.create_window(
                APP_NAME,
                site_url,
                width=1440,
                height=920,
                min_size=(1024, 700),
                resizable=True,
                confirm_close=False,
            )
            webview.start(gui="edgechromium", private_mode=False, storage_path=str(WEBVIEW_DIR))
        except Exception as webview_error:
            _run_browser_fallback(site_url, webview_error)
        finally:
            _stop_service(SITE_KIND)
            _stop_service(API_KIND)
        return 0
    except Exception as exc:
        try:
            splash.close()
        except Exception:
            pass
        _stop_service(SITE_KIND)
        _stop_service(API_KIND)
        from tkinter import messagebox

        messagebox.showerror(APP_NAME, str(exc))
        return 1
    finally:
        _release_single_instance()


def smoke_test() -> int:
    try:
        url = _ensure_desktop_services(print)
        checks = [
            (url, "desktop site"),
            (f"{url}/calculator?index=DII", "calculator"),
            (f"{url}/api/dietary/v1/indices/DII", "API proxy"),
        ]
        failed = [label for target, label in checks if not _is_url_ready(target, timeout=5)]
        if failed:
            print("FAILED:", ", ".join(failed))
            return 1
        print(f"Desktop smoke test passed: {url}")
        return 0
    finally:
        _stop_service(SITE_KIND)
        _stop_service(API_KIND)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--serve-api", action="store_true")
    parser.add_argument("--smoke-test", action="store_true")
    parser.add_argument("--port", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.serve_api:
        run_api_server(args.port or DEFAULT_API_PORT)
        return 0
    if args.smoke_test:
        return smoke_test()
    return run_desktop()


if __name__ == "__main__":
    raise SystemExit(main())
