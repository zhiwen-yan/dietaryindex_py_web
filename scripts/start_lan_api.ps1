$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$port = 8000
$healthUrl = "http://127.0.0.1:$port/healthz"
$docsUrl = "http://127.0.0.1:$port/docs"
$appDataRoot = Join-Path $env:LOCALAPPDATA "DietaryIndexLocal"
$logDir = Join-Path $appDataRoot "logs"
$env:DIETARYINDEX_RUNTIME_DIR = Join-Path $appDataRoot "runtime_data"
New-Item -ItemType Directory -Force -Path $logDir, $env:DIETARYINDEX_RUNTIME_DIR | Out-Null
$logPath = Join-Path $logDir "api_lan.log"
$errPath = Join-Path $logDir "api_lan.err.log"

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

function Test-Url($targetUrl) {
    try {
        $response = Invoke-WebRequest -Uri $targetUrl -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

function Get-PrimaryIPv4() {
    $ip = Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254*' } |
        Sort-Object InterfaceMetric, SkipAsSource |
        Select-Object -First 1 -ExpandProperty IPAddress

    if (-not $ip) {
        throw "No active IPv4 address was found for LAN testing."
    }

    return $ip
}

Write-Host ""
Write-Host "DietaryIndex LAN API launcher" -ForegroundColor Green

if (-not (Test-PythonRuntime $venvPython)) {
    Write-Host "Local environment is missing or invalid." -ForegroundColor Red
    Write-Host "Expected runtime: $venvPython"
    Write-Host "Please run scripts\install_local.bat to create or repair the local environment."
    exit 1
}

$lanIp = Get-PrimaryIPv4
$lanDocsUrl = "http://${lanIp}:$port/docs"

if (Test-Url $healthUrl) {
    Write-Host "LAN API is already running." -ForegroundColor Yellow
    Write-Host "Local docs: $docsUrl"
    Write-Host "LAN docs:   $lanDocsUrl"
    Start-Process $docsUrl
    exit 0
}

Write-Host "Starting FastAPI service for LAN access on port $port..." -ForegroundColor Cyan
Start-Process -FilePath $venvPython `
    -ArgumentList "-m", "uvicorn", "dietaryindex_api.app:app", "--host", "0.0.0.0", "--port", "$port" `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $logPath `
    -RedirectStandardError $errPath `
    -WindowStyle Hidden

$ready = $false
for ($i = 0; $i -lt 25; $i++) {
    Start-Sleep -Milliseconds 600
    if (Test-Url $healthUrl) {
        $ready = $true
        break
    }
}

if (-not $ready) {
    Write-Host "The LAN API did not start successfully." -ForegroundColor Red
    Write-Host "Check these log files for details:"
    Write-Host "  $logPath"
    Write-Host "  $errPath"
    exit 1
}

Write-Host "LAN API is ready." -ForegroundColor Green
Write-Host "Local docs: $docsUrl"
Write-Host "LAN docs:   $lanDocsUrl"
Write-Host ""
Write-Host "If another device cannot open the LAN docs URL, allow Python/Uvicorn through the Windows firewall." -ForegroundColor Yellow
Start-Process $docsUrl
