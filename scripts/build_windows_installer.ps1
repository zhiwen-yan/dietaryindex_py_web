param(
    [string]$ElectronMirror = $env:ELECTRON_MIRROR
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
$backendSpecPath = Join-Path $projectRoot "packaging\windows\dietaryindex_backend.spec"
$mcpSpecPath = Join-Path $projectRoot "packaging\windows\dietaryindex_mcp.spec"
$issPath = Join-Path $projectRoot "packaging\windows\DietaryIndexLocal.iss"
$pyprojectPath = Join-Path $projectRoot "pyproject.toml"
$installerOutputDir = Join-Path $projectRoot "dist\installer"
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$prepareRuntimeScript = Join-Path $projectRoot "scripts\prepare_desktop_runtime.ps1"
$backendExe = Join-Path $projectRoot "dist\DietaryIndexBackend.exe"
$mcpExe = Join-Path $projectRoot "dist\DietaryIndexMCP.exe"
$electronRoot = Join-Path $projectRoot "electron_app"
$electronExe = Join-Path $electronRoot "out\DietaryIndex-win32-x64\DietaryIndex.exe"
$electronSmokeReport = Join-Path $projectRoot "electron_smoke_packaged.json"
$bundledNodeDir = Join-Path $projectRoot "desktop_runtime\node"
$mcpSmokeScript = Join-Path $projectRoot "scripts\smoke_mcp_server.py"

function Get-RequiredCommand($name) {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $command) { throw "Required command not found in PATH: $name" }
    return $command.Source
}

function Test-PythonRuntime($pythonPath) {
    if (-not (Test-Path $pythonPath)) { return $false }
    try {
        & $pythonPath --version *> $null
        return $true
    }
    catch { return $false }
}

function Get-InnoSetupCompiler() {
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) { return $candidate }
    }
    $command = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    throw "Inno Setup 6 was not found. Please install Inno Setup 6 first."
}

foreach ($requiredPath in @($backendSpecPath, $mcpSpecPath, $issPath, $prepareRuntimeScript, $mcpSmokeScript)) {
    if (-not (Test-Path $requiredPath)) { throw "Required build input not found: $requiredPath" }
}

$pythonExe = if (Test-PythonRuntime $venvPython) { $venvPython } else { Get-RequiredCommand "python" }
$null = Get-RequiredCommand "npm"
$isccExe = Get-InnoSetupCompiler
$versionMatch = Select-String -Path $pyprojectPath -Pattern '^version\s*=\s*"([^"]+)"'
if (-not $versionMatch) { throw "Unable to read version from pyproject.toml" }
$appVersion = $versionMatch.Matches[0].Groups[1].Value

Write-Host ""
Write-Host "Building DietaryIndex Electron Windows installer" -ForegroundColor Green
Write-Host "Project root: $projectRoot"
Write-Host "Version: $appVersion"
Write-Host "Python: $pythonExe"
Write-Host "Inno Setup: $isccExe"
Write-Host ""

Push-Location $projectRoot
try {
    Write-Host "Step 1/9: Installing Python release dependencies..." -ForegroundColor Cyan
    & $pythonExe -m pip install -e "$projectRoot[api,adapters,desktop]" pyinstaller
    if ($LASTEXITCODE -ne 0) { throw "Python dependency installation failed." }

    Write-Host "Step 2/9: Preparing the bundled Node.js + Next.js runtime..." -ForegroundColor Cyan
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $prepareRuntimeScript
    if ($LASTEXITCODE -ne 0) { throw "Desktop web runtime preparation failed." }

    Write-Host "Step 3/9: Building the FastAPI sidecar..." -ForegroundColor Cyan
    & $pythonExe -m PyInstaller --noconfirm --clean $backendSpecPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $backendExe)) { throw "Backend PyInstaller build failed." }

    Write-Host "Step 4/9: Building the standalone MCP server..." -ForegroundColor Cyan
    & $pythonExe -m PyInstaller --noconfirm --clean $mcpSpecPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $mcpExe)) { throw "MCP PyInstaller build failed." }

    Write-Host "Step 5/9: Testing the standalone MCP server..." -ForegroundColor Cyan
    & $pythonExe $mcpSmokeScript --command $mcpExe
    if ($LASTEXITCODE -ne 0) { throw "Packaged MCP smoke test failed." }

    Write-Host "Step 6/9: Installing and testing the Electron host..." -ForegroundColor Cyan
    Push-Location $electronRoot
    try {
        & npm ci
        if ($LASTEXITCODE -ne 0) { throw "Electron npm ci failed." }
        & npm test
        if ($LASTEXITCODE -ne 0) { throw "Electron unit tests failed." }

        # Electron Packager 20 requires Node >=22.12. Use the bundled runtime
        # so the release build does not depend on the system Node version.
        $env:PATH = "$bundledNodeDir;$env:PATH"
        if ($ElectronMirror) { $env:ELECTRON_MIRROR = $ElectronMirror }
        $env:CI = "1"
        & npm run package
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $electronExe)) { throw "Electron package build failed." }
    }
    finally { Pop-Location }

    Write-Host "Step 7/9: Running the packaged Electron smoke test..." -ForegroundColor Cyan
    Remove-Item -LiteralPath $electronSmokeReport -Force -ErrorAction SilentlyContinue
    $smokeProcess = Start-Process -FilePath $electronExe -ArgumentList @(
        "--smoke-test",
        "--smoke-output=$electronSmokeReport"
    ) -PassThru -WindowStyle Hidden
    $smokeProcess.WaitForExit()
    if ($smokeProcess.ExitCode -ne 0 -or -not (Test-Path $electronSmokeReport)) {
        throw "Packaged Electron smoke test failed. The installer was not produced."
    }
    $smokeResult = Get-Content -LiteralPath $electronSmokeReport -Raw | ConvertFrom-Json
    if (-not $smokeResult.passed) { throw "Packaged Electron smoke checks did not pass." }

    Write-Host "Step 8/9: Verifying release version alignment..." -ForegroundColor Cyan
    if ($smokeResult.version -ne $appVersion) {
        throw "Electron version $($smokeResult.version) does not match pyproject version $appVersion."
    }

    Write-Host "Step 9/9: Building setup.exe with Inno Setup..." -ForegroundColor Cyan
    & $isccExe "/DProjectRoot=$projectRoot" "/DAppVersion=$appVersion" $issPath
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup build failed." }
}
finally { Pop-Location }

Write-Host ""
Write-Host "Build completed." -ForegroundColor Green
Write-Host "Installer output folder: $installerOutputDir"
Write-Host ""
