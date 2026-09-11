param(
    [switch]$Unregister,
    [string[]]$AllowedRoot = @($env:USERPROFILE),
    [string]$OutputRoot = (Join-Path $env:LOCALAPPDATA "DietaryIndex\runtime_data\mcp_results")
)

$ErrorActionPreference = "Stop"

$logDir = Join-Path $env:LOCALAPPDATA "DietaryIndex"
$logPath = Join-Path $logDir "mcp-registration.log"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Write-Log($message) {
    $line = "[$(Get-Date -Format s)] $message"
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
    Write-Host $line
}

function Show-Error($message) {
    try {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show(
            $message,
            "DietaryIndex MCP / DietaryIndex MCP",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        ) | Out-Null
    }
    catch {
        # Logging remains available if Windows Forms is unavailable.
    }
}

$mcpExe = Join-Path $PSScriptRoot "DietaryIndexMCP.exe"
if (-not $Unregister -and -not (Test-Path -LiteralPath $mcpExe)) {
    $message = "MCP executable not found: $mcpExe"
    Write-Log $message
    Show-Error $message
    exit 1
}

$codexCommand = Get-Command codex.exe -ErrorAction SilentlyContinue
if (-not $codexCommand) {
    $codexCommand = Get-Command codex -ErrorAction SilentlyContinue
}
if (-not $codexCommand) {
    Write-Log "Codex CLI was not found; MCP registration was skipped."
    exit 0
}

$codex = $codexCommand.Source
if ($Unregister) {
    & $codex mcp remove dietaryindex *> $null
    Write-Log "Removed dietaryindex MCP registration."
    exit 0
}

# Replace only this named server so re-running the installer is safe and idempotent.
& $codex mcp remove dietaryindex *> $null
$resolvedRoots = @(
    foreach ($root in $AllowedRoot) {
        if (-not [string]::IsNullOrWhiteSpace($root)) {
            [System.IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($root))
        }
    }
)
if ($resolvedRoots.Count -eq 0) {
    $message = "At least one MCP allowed input root is required."
    Write-Log $message
    Show-Error $message
    exit 1
}
$allowedRootsValue = $resolvedRoots -join [System.IO.Path]::PathSeparator
$resolvedOutputRoot = [System.IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($OutputRoot))
New-Item -ItemType Directory -Force -Path $resolvedOutputRoot | Out-Null

& $codex mcp add `
    --env "DIETARYINDEX_MCP_ALLOWED_ROOTS=$allowedRootsValue" `
    --env "DIETARYINDEX_MCP_OUTPUT_ROOT=$resolvedOutputRoot" `
    dietaryindex -- $mcpExe
if ($LASTEXITCODE -ne 0) {
    $message = "Codex MCP registration failed with exit code $LASTEXITCODE."
    Write-Log $message
    Show-Error $message
    exit $LASTEXITCODE
}

Write-Log "Registered dietaryindex MCP: $mcpExe; input roots: $allowedRootsValue; output root: $resolvedOutputRoot"
