@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0start_lan_api.ps1"
exit /b %errorlevel%
