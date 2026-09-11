@echo off
setlocal

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start_local_api.ps1"
if errorlevel 1 (
    echo.
    echo Local API launch failed.
    pause
    exit /b 1
)
