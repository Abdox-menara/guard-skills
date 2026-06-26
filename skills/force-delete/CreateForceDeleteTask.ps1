<#
.SYNOPSIS
Creates a scheduled task that runs the ForceDelete.ps1 script with highest privileges.
.DESCRIPTION
The task is registered to run under the SYSTEM account ("Run with highest privileges")
and will trigger at logon (or you can change the trigger). It calls ForceDelete.ps1
with the two protected folder paths.

You must run this script from an elevated PowerShell session (Run as Administrator).

.PARAMETER TaskName
Name of the scheduled task to create.
.PARAMETER TriggerType
How to trigger the task – currently supports "AtLogOn" or "Once" (you can edit the script to change).

.EXAMPLE
# Create the task (run this script as admin)
.\CreateForceDeleteTask.ps1

# After creation you can run it immediately:
Start-ScheduledTask -TaskName "ForceDeleteProtectedFolders"
#>

param(
    [string]$TaskName = "ForceDeleteProtectedFolders",
    [ValidateSet("AtLogOn", "Once")]
    [string]$TriggerType = "AtLogOn",
    [datetime]$RunOnceTime = (Get-Date).AddMinutes(1) # used only if TriggerType is Once
)

# Absolute path to the ForceDelete script
$forceDeleteScript = "C:\opencodes\guard skills\skills\force-delete\ForceDelete.ps1"

# Arguments passed to PowerShell when the task runs
$psArgs = "-NoProfile -ExecutionPolicy Bypass -File `"$forceDeleteScript`" -Paths `"D:\\AAAAAAAAAAAAAAAAAAA\\ZZZZZZZZZZZZZ`",`"D:\\AAAAAAAAAAAAAAAAAAA\\ZZZZZZZZZZZZZZZ`""

# Create the action – call PowerShell.exe with the arguments above
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument $psArgs

# Use the SYSTEM account and run with highest privileges
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Define the trigger based on the selected type
if ($TriggerType -eq "AtLogOn") {
    $trigger = New-ScheduledTaskTrigger -AtLogOn
} elseif ($TriggerType -eq "Once") {
    $trigger = New-ScheduledTaskTrigger -Once -At $RunOnceTime
}

# Register (or update) the scheduled task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Description "Automatically deletes protected folders using ForceDelete.ps1" -Force
    Write-Host "✅ Scheduled task '$TaskName' created successfully." -ForegroundColor Green
    Write-Host "You can run it now with: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to create scheduled task: $_" -ForegroundColor Red
}
