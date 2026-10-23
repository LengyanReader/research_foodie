#!/usr/bin/env pwsh
# Scheduled self-update for harness_factory (P30).
# One observe-only cycle: refresh (file + tracked feeds + LLM if configured) ->
# then the rest of the loop (probe-domains -> trace-audit -> evolve ->
# cycle audit -> scoreboard) via `full-update --offline`.
# Never edits docs/catalogs. See tasks/REFRESH.md for scheduling.

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

if (-not $NoEvolve -and -not $DryRun) {
    $fullArgs = @("-m", "harness_factory", "full-update", "--offline")
    if ($Root) { $fullArgs += @("--root", $Root) }
    & python @fullArgs
    if ($LASTEXITCODE -ne 0) { $code = $LASTEXITCODE }
}

exit $code
