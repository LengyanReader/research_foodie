#!/usr/bin/env pwsh
# Install this repo as an agent skill (optional; repo-as-skill needs no install).
# Copies SKILL.md + the referenced knowledge modules + catalogs into a skills dir,
# preserving relative paths so SKILL.md links keep working.

param(
    [string]$Dest = ""
)

$ErrorActionPreference = "Stop"
if (-not $Dest) { $Dest = Join-Path $HOME ".agents/skills/harness-factory" }

$src = $PSScriptRoot
New-Item -ItemType Directory -Force -Path $Dest | Out-Null

foreach ($item in @("SKILL.md", "core", "domains", "review", "sources", "reference")) {
    $from = Join-Path $src $item
    if (Test-Path -LiteralPath $from) {
        Copy-Item -Recurse -Force -LiteralPath $from -Destination $Dest
    }
}

$dataSrc = Join-Path $src "src/harness_factory/data"
$dataDest = Join-Path $Dest "src/harness_factory/data"
New-Item -ItemType Directory -Force -Path $dataDest | Out-Null
Copy-Item -Force -Path (Join-Path $dataSrc "*.json") -Destination $dataDest

Write-Host "harness-factory skill installed to: $Dest"
Write-Host "The assistant can now read SKILL.md and load modules on demand."
