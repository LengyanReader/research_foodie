# research_foodie — L-6 one-command self-check / 一键自检
# Offline safety net: unit tests + mock integration + evolution cadence.
# Usage:
#   ./self_check.ps1          # offline (~15s, zero LLM)
#   ./self_check.ps1 -Full    # + live judge cadence (~1.5 min)
#   ./self_check.ps1 -WithReal  # also real opencode pipeline run
param(
    [switch]$Full,
    [switch]$WithReal
)

$ErrorActionPreference = 'Stop'
# Working ML env (see docs/setup-runbook.md §3). Override with $env:RF_PY.
$PY = if ($env:RF_PY) { $env:RF_PY } else { 'C:\Users\data\miniconda3\envs\ds0509\python.exe' }

$argv = @('-X', 'utf8', '-m', 'tools.eval.self_check')
if ($Full)     { $argv += '--full' }
if ($WithReal) { $argv += '--with-real' }

Push-Location $PSScriptRoot
try {
    & $PY @argv
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
