@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0start_desktop_launcher.ps1"
exit /b %errorlevel%
