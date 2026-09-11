@echo off
setlocal

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0install_local.ps1"
if errorlevel 1 (
    echo.
    echo Installation did not complete successfully.
    pause
    exit /b 1
)

echo.
echo Installation finished. You can now run start_local_web.bat.
pause
