$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$venvDir = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"

Write-Host ""
Write-Host "DietaryIndex local installer" -ForegroundColor Green
Write-Host "Project root: $projectRoot"
Write-Host ""

function Test-Command($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

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

if ((Test-Path $venvDir) -and (-not (Test-PythonRuntime $venvPython))) {
    Write-Host "Existing local environment is broken. Rebuilding .venv..." -ForegroundColor Yellow
    Remove-Item -LiteralPath $venvDir -Recurse -Force
}

if (-not (Test-PythonRuntime $venvPython)) {
    if (-not (Test-Command "python")) {
        Write-Host "Python was not found in PATH." -ForegroundColor Red
        Write-Host "Please install Python 3.10+ first, then run this installer again."
        exit 1
    }

    Write-Host "Creating local virtual environment..." -ForegroundColor Cyan
    & python -m venv $venvDir
}
else {
    Write-Host "Using existing virtual environment: $venvDir" -ForegroundColor Yellow
}

Write-Host "Upgrading pip..." -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip

Write-Host "Installing DietaryIndex local package and app dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install -e "$projectRoot[api,adapters,desktop]"
if ($LASTEXITCODE -ne 0) {
    throw "Python dependency installation failed."
}

Write-Host "Preparing the Next.js desktop runtime..." -ForegroundColor Cyan
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $scriptDir "prepare_desktop_runtime.ps1")
if ($LASTEXITCODE -ne 0) {
    throw "Desktop web runtime preparation failed."
}

Write-Host ""
Write-Host "Installation completed." -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  Double-click scripts\start_desktop_launcher.bat"
Write-Host ""
