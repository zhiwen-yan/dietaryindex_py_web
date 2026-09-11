param(
    [string]$NodeVersion = "22.18.0",
    [switch]$SkipNpmInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir ".."))
$frontendRoot = Join-Path $projectRoot "web_frontend"
$runtimeRoot = Join-Path $projectRoot "desktop_runtime"
$nodeRuntimeRoot = Join-Path $runtimeRoot "node"
$siteRuntimeRoot = Join-Path $runtimeRoot "site"
$nextBuildRoot = Join-Path $frontendRoot ".next"
$cacheRoot = Join-Path $projectRoot ".desktop_build_cache"
$nodeFolderName = "node-v$NodeVersion-win-x64"
$nodeArchive = Join-Path $cacheRoot "$nodeFolderName.zip"
$nodeCacheRoot = Join-Path $cacheRoot $nodeFolderName
$nodeExe = Join-Path $nodeCacheRoot "node.exe"

function Assert-ChildPath([string]$Path, [string]$Parent) {
    $resolvedPath = [System.IO.Path]::GetFullPath($Path)
    $resolvedParent = [System.IO.Path]::GetFullPath($Parent).TrimEnd('\') + '\'
    if (-not $resolvedPath.StartsWith($resolvedParent, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to modify a path outside the project: $resolvedPath"
    }
}

function Reset-Directory([string]$Path) {
    Assert-ChildPath $Path $projectRoot
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

if (-not (Test-Path (Join-Path $frontendRoot "package-lock.json"))) {
    throw "web_frontend\package-lock.json was not found."
}

New-Item -ItemType Directory -Force -Path $cacheRoot | Out-Null

if (-not (Test-Path $nodeExe)) {
    if (-not (Test-Path $nodeArchive)) {
        $nodeUrl = "https://nodejs.org/dist/v$NodeVersion/$nodeFolderName.zip"
        Write-Host "Downloading the official Node.js runtime: $nodeUrl" -ForegroundColor Cyan
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeArchive
    }

    Write-Host "Extracting Node.js $NodeVersion..." -ForegroundColor Cyan
    Expand-Archive -LiteralPath $nodeArchive -DestinationPath $cacheRoot -Force
}

if (-not (Test-Path $nodeExe)) {
    throw "Node.js runtime was not prepared: $nodeExe"
}

$env:Path = "$nodeCacheRoot;$env:Path"
$env:NEXT_TELEMETRY_DISABLED = "1"

Push-Location $frontendRoot
try {
    if (-not $SkipNpmInstall) {
        Write-Host "Installing locked Next.js dependencies..." -ForegroundColor Cyan
        & (Join-Path $nodeCacheRoot "npm.cmd") ci
        if ($LASTEXITCODE -ne 0) {
            throw "npm ci failed."
        }
    }

    # Next.js writes hidden cache metadata on Windows. Reusing those generated
    # files can raise EPERM when the next build tries to truncate them, so every
    # release build starts from a checked, project-local .next directory.
    Reset-Directory $nextBuildRoot
    Write-Host "Building the Next.js standalone desktop site..." -ForegroundColor Cyan
    & (Join-Path $nodeCacheRoot "npm.cmd") run build
    if ($LASTEXITCODE -ne 0) {
        throw "Next.js production build failed."
    }
}
finally {
    Pop-Location
}

$standaloneRoot = Join-Path $frontendRoot ".next\standalone"
$standaloneServer = Join-Path $standaloneRoot "server.js"
if (-not (Test-Path $standaloneServer)) {
    throw "Next.js standalone output was not found: $standaloneServer"
}

Reset-Directory $nodeRuntimeRoot
Reset-Directory $siteRuntimeRoot
Copy-Item -LiteralPath $nodeExe -Destination (Join-Path $nodeRuntimeRoot "node.exe")
Copy-Item -Path (Join-Path $standaloneRoot "*") -Destination $siteRuntimeRoot -Recurse -Force

$siteNextRoot = Join-Path $siteRuntimeRoot ".next"
New-Item -ItemType Directory -Force -Path $siteNextRoot | Out-Null
Copy-Item -LiteralPath (Join-Path $frontendRoot ".next\static") -Destination $siteNextRoot -Recurse -Force

$publicRoot = Join-Path $frontendRoot "public"
if (Test-Path $publicRoot) {
    Copy-Item -LiteralPath $publicRoot -Destination $siteRuntimeRoot -Recurse -Force
}

$manifest = @{
    node_version = $NodeVersion
    site_version = (Get-Content (Join-Path $frontendRoot "package.json") -Raw | ConvertFrom-Json).version
    built_at_utc = [DateTime]::UtcNow.ToString("o")
} | ConvertTo-Json
Set-Content -LiteralPath (Join-Path $runtimeRoot "desktop-runtime.json") -Value $manifest -Encoding UTF8

Write-Host "Desktop runtime is ready: $runtimeRoot" -ForegroundColor Green
