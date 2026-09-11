$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$launcherPath = Join-Path $projectRoot "desktop_launcher.py"
$runtimeServer = Join-Path $projectRoot "desktop_runtime\site\server.js"
$runtimeNode = Join-Path $projectRoot "desktop_runtime\node\node.exe"

function Test-PythonRuntime($pythonPath) {
    if (-not (Test-Path $pythonPath)) {
        return $false
    }

    try {
        & $pythonPath --version *> $null
        return $true
    }
    catch {
        return $false
    }
}

Write-Host ""
Write-Host "DietaryIndex desktop launcher" -ForegroundColor Green

if (-not (Test-PythonRuntime $venvPython)) {
    Write-Host "Local environment is missing or invalid." -ForegroundColor Red
    Write-Host "Expected runtime: $venvPython"
    Write-Host "Please run scripts\install_local.bat first."
    exit 1
}

if (-not (Test-Path $launcherPath)) {
    Write-Host "desktop_launcher.py was not found." -ForegroundColor Red
    Write-Host "Expected file: $launcherPath"
    exit 1
}

if ((-not (Test-Path $runtimeServer)) -or (-not (Test-Path $runtimeNode))) {
    Write-Host "Desktop web runtime is missing. Preparing it now..." -ForegroundColor Yellow
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $scriptDir "prepare_desktop_runtime.ps1")
    if ($LASTEXITCODE -ne 0) {
        throw "Desktop web runtime preparation failed."
    }
}

Write-Host "Opening DietaryIndex desktop launcher..." -ForegroundColor Cyan
Start-Process -FilePath $venvPython `
    -ArgumentList $launcherPath `
    -WorkingDirectory $projectRoot

Write-Host "Launcher started." -ForegroundColor Green
