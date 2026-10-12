#!/usr/bin/env pwsh
# Scheduled self-update for harness_factory.
# Runs one refresh cycle: collect -> audit -> proposal -> journal (never edits docs).
# See tasks/REFRESH.md for scheduling (Task Scheduler / cron / GitHub Actions).

param(
    [string]$Root = "",
    [string]$Provider = "auto",
    [switch]$Verify,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$src = Join-Path $PSScriptRoot "src"
if (Test-Path -LiteralPath $src) { $env:PYTHONPATH = $src }

$cliArgs = @("-m", "harness_factory", "refresh", "--provider", $Provider)
if ($Root) { $cliArgs += @("--root", $Root) }
if ($Verify) { $cliArgs += "--verify" }
if ($DryRun) { $cliArgs += "--dry-run" }

& python @cliArgs
exit $LASTEXITCODE
