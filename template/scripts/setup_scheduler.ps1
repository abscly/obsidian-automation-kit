# Obsidian Automation Kit — Windows Task Scheduler Setup
# Run as Administrator:
# powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1

param(
    [string]$VaultPath = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
)

$scriptsDir = Join-Path $VaultPath "scripts"
$python = 'python'

Write-Host '=================================================='
Write-Host '  Obsidian Automation Kit — Task Scheduler Setup' -ForegroundColor Cyan
Write-Host '=================================================='
Write-Host ''
Write-Host "  Vault: $VaultPath" -ForegroundColor DarkGray
Write-Host "  Scripts: $scriptsDir" -ForegroundColor DarkGray
Write-Host ''

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# ===================================================
# 1. Daily Note Auto-Generate (00:05)
# ===================================================
Write-Host '  [1/6] Daily Note Auto-Generate (00:05)...' -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $python -Argument """$scriptsDir\auto_daily.py""" -WorkingDirectory $scriptsDir
$trigger = New-ScheduledTaskTrigger -Daily -At '00:05'
Register-ScheduledTask -TaskName 'ObsidianKit-DailyGenerate' -Action $action -Trigger $trigger -Settings $settings -Description 'Daily Note Auto-Generate' -Force | Out-Null
Write-Host '  Done!' -ForegroundColor Green

# ===================================================
# 2. Git Sync — Every hour
# ===================================================
Write-Host '  [2/6] Git Sync (every 1 hour)...' -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $python -Argument """$scriptsDir\git_backup.py""" -WorkingDirectory $scriptsDir
$trigger = New-ScheduledTaskTrigger -Once -At '00:00' -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 365)
Register-ScheduledTask -TaskName 'ObsidianKit-GitSync' -Action $action -Trigger $trigger -Settings $settings -Description 'Git Sync (every 1 hour)' -Force | Out-Null
Write-Host '  Done!' -ForegroundColor Green

# ===================================================
# 3. AI Reporter — Every 3 hours
# ===================================================
Write-Host '  [3/6] AI Reporter (every 3 hours)...' -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $python -Argument """$scriptsDir\ai_reporter.py""" -WorkingDirectory $scriptsDir
$trigger = New-ScheduledTaskTrigger -Once -At '09:00' -RepetitionInterval (New-TimeSpan -Hours 3) -RepetitionDuration (New-TimeSpan -Days 365)
Register-ScheduledTask -TaskName 'ObsidianKit-AIReporter' -Action $action -Trigger $trigger -Settings $settings -Description 'AI Daily Report (every 3 hours)' -Force | Out-Null
Write-Host '  Done!' -ForegroundColor Green

# ===================================================
# 4. Weekly Review (Sunday 21:00)
# ===================================================
Write-Host '  [4/6] Weekly Review (Sunday 21:00)...' -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $python -Argument """$scriptsDir\master.py"" --weekly" -WorkingDirectory $scriptsDir
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At '21:00'
Register-ScheduledTask -TaskName 'ObsidianKit-WeeklyReview' -Action $action -Trigger $trigger -Settings $settings -Description 'Weekly Review' -Force | Out-Null
Write-Host '  Done!' -ForegroundColor Green

# ===================================================
# 5. Monthly Review (1st day 21:00)
# ===================================================
Write-Host '  [5/6] Monthly Review (1st 21:00)...' -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $python -Argument """$scriptsDir\master.py"" --monthly" -WorkingDirectory $scriptsDir
$trigger = New-ScheduledTaskTrigger -Daily -At '21:00'
Register-ScheduledTask -TaskName 'ObsidianKit-MonthlyReview' -Action $action -Trigger $trigger -Settings $settings -Description 'Monthly Review (1st day only)' -Force | Out-Null
Write-Host '  Done!' -ForegroundColor Green

# ===================================================
# 6. Master Pipeline (23:30)
# ===================================================
Write-Host '  [6/6] Master Pipeline (23:30)...' -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $python -Argument """$scriptsDir\master.py""" -WorkingDirectory $scriptsDir
$trigger = New-ScheduledTaskTrigger -Daily -At '23:30'
Register-ScheduledTask -TaskName 'ObsidianKit-MasterPipeline' -Action $action -Trigger $trigger -Settings $settings -Description 'Full daily pipeline' -Force | Out-Null
Write-Host '  Done!' -ForegroundColor Green

# Summary
Write-Host ''
Write-Host '=================================================='
Write-Host '  All 6 tasks registered!' -ForegroundColor Green
Write-Host '=================================================='
Write-Host ''
Write-Host '  ObsidianKit-DailyGenerate  : Daily 00:05'
Write-Host '  ObsidianKit-GitSync        : Every 1 hour' -ForegroundColor Cyan
Write-Host '  ObsidianKit-AIReporter     : Every 3 hours' -ForegroundColor Cyan
Write-Host '  ObsidianKit-WeeklyReview   : Sunday 21:00'
Write-Host '  ObsidianKit-MonthlyReview  : 1st day 21:00'
Write-Host '  ObsidianKit-MasterPipeline : Daily 23:30'
Write-Host ''
