$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$port = 8000
$url = "http://127.0.0.1:$port/docs"
$healthUrl = "http://127.0.0.1:$port/healthz"
$appDataRoot = Join-Path $env:LOCALAPPDATA "DietaryIndexLocal"
$logDir = Join-Path $appDataRoot "logs"
$env:DIETARYINDEX_RUNTIME_DIR = Join-Path $appDataRoot "runtime_data"
New-Item -ItemType Directory -Force -Path $logDir, $env:DIETARYINDEX_RUNTIME_DIR | Out-Null
$logPath = Join-Path $logDir "api_local.log"
$errPath = Join-Path $logDir "api_local.err.log"

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

function Test-LocalUrl($targetUrl) {
    try {
        $response = Invoke-WebRequest -Uri $targetUrl -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

Write-Host ""
Write-Host "DietaryIndex local API launcher" -ForegroundColor Green

if (-not (Test-PythonRuntime $venvPython)) {
    Write-Host "Local environment is missing or invalid." -ForegroundColor Red
    Write-Host "Expected runtime: $venvPython"
    Write-Host "Please run scripts\install_local.bat to create or repair the local environment."
    exit 1
}

if (Test-LocalUrl $healthUrl) {
    Write-Host "Local API is already running. Opening docs..." -ForegroundColor Yellow
    Start-Process $url
    exit 0
}

Write-Host "Starting local API on port $port..." -ForegroundColor Cyan
Start-Process -FilePath $venvPython `
    -ArgumentList "-m", "uvicorn", "dietaryindex_api.app:app", "--host", "127.0.0.1", "--port", "$port", "--reload" `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $logPath `
    -RedirectStandardError $errPath `
    -WindowStyle Hidden

$ready = $false
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-LocalUrl $healthUrl) {
        $ready = $true
        break
    }
}

if (-not $ready) {
    Write-Host "The local API did not start successfully." -ForegroundColor Red
    Write-Host "Check these log files for details:"
    Write-Host "  $logPath"
    Write-Host "  $errPath"
    exit 1
}

Write-Host "Local API is ready. Opening docs..." -ForegroundColor Green
Start-Process $url
