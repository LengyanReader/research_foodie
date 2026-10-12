#!/usr/bin/env pwsh
# Scheduled self-update for harness_factory.
# Runs one observe-only cycle: refresh (file + tracked feeds + LLM if configured) ->
# intel extraction -> self-evolution audit. Never edits docs/catalogs.
# See tasks/REFRESH.md for scheduling (Task Scheduler / cron / GitHub Actions).

param(
    [string]$Root = "",
    [string]$Provider = "all",
    [switch]$Verify,
    [switch]$DryRun,
    [switch]$NoEvolve
)

$ErrorActionPreference = "Stop"

$src = Join-Path $PSScriptRoot "src"
if (Test-Path -LiteralPath $src) { $env:PYTHONPATH = $src }

$refreshArgs = @("-m", "harness_factory", "refresh", "--provider", $Provider, "--intel")
if ($Root) { $refreshArgs += @("--root", $Root) }
if ($Verify) { $refreshArgs += "--verify" }
if ($DryRun) { $refreshArgs += "--dry-run" }

& python @refreshArgs
$code = $LASTEXITCODE

if (-not $NoEvolve) {
    $evolveArgs = @("-m", "harness_factory", "evolve")
    if ($Root) { $evolveArgs += @("--root", $Root) }
    if ($DryRun) { $evolveArgs += "--dry-run" }
    & python @evolveArgs
    if ($LASTEXITCODE -ne 0) { $code = $LASTEXITCODE }
}

exit $code
