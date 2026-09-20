<#
.SYNOPSIS
  Register the daily research_foodie cadence as a Windows scheduled task (E-6).

.DESCRIPTION
  Idempotent: removes any existing task of the same name, then registers a fresh
  one that runs the *offline, key-free* cadence every day:

      python -m tools.eval.evolution_sprint --quick

  --quick runs the mock pipeline + zero-LLM health/dep checks and refreshes
  _eval_out/capability_report.md (its step 8). It makes NO model call and needs
  NO API key, so it is safe to run unattended. (The live, model-backed cadence
  is intentionally NOT scheduled here — it depends on a reachable judge, which
  is deferred.)

  This script only *defines* the task; it does not start the pipeline. Run it
  yourself to opt in. Requires PowerShell 5.1+/7 and rights to register a task
  (current-user tasks need no admin).

.PARAMETER PythonPath
  Absolute path to the interpreter (default: the ds0509 conda env used by this repo).

.PARAMETER RepoRoot
  Repo root to run from (default: parent of this script's tools/web folder).

.PARAMETER TaskName
  Scheduled-task name (default: research_foodie-daily-cadence).

.PARAMETER At
  Daily start time, 24h HH:mm (default: 07:30).

.PARAMETER Unregister
  Remove the task and exit (does not touch any files).

.EXAMPLE
  pwsh -File tools/web/schedule_task.ps1 -At 08:00
.EXAMPLE
  pwsh -File tools/web/schedule_task.ps1 -Unregister
#>
[CmdletBinding()]
param(
    [string]$PythonPath = "C:\Users\data\miniconda3\envs\ds0509\python.exe",
    [string]$RepoRoot   = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [string]$TaskName   = "research_foodie-daily-cadence",
    [string]$At         = "07:30",
    [switch]$Unregister
)

$ErrorActionPreference = "Stop"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "[schedule] removed existing task '$TaskName'"
}
if ($Unregister) {
    Write-Host "[schedule] unregistered; nothing scheduled."
    return
}

if (-not (Test-Path $PythonPath)) {
    throw "Python interpreter not found: $PythonPath (pass -PythonPath)"
}

# The task runs the offline cadence from the repo root. Argument list is passed
# explicitly so no shell quoting is needed at trigger time.
$Action  = New-ScheduledTaskAction -Execute $PythonPath `
            -Argument "-X utf8 -m tools.eval.evolution_sprint --quick" `
            -WorkingDirectory $RepoRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At $At
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
            -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
    -Settings $Settings -Description "Daily research_foodie key-free cadence + capability_report refresh." | Out-Null

Write-Host "[schedule] registered '$TaskName' -> daily $At from $RepoRoot"
Write-Host "[schedule] offline only (evolution_sprint --quick; no LLM, no key)."
Write-Host "[schedule] verify:  Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo"
Write-Host "[schedule] remove:  pwsh -File tools/web/schedule_task.ps1 -Unregister"
