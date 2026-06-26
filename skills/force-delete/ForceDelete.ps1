<#
.SYNOPSIS
Forcefully delete protected directories.
.DESCRIPTION
Takes ownership, grants full control to Administrators, clears restrictive attributes,
and removes the specified paths. Supports WhatIf, Confirm, logging, and pipeline input.
If not running as Administrator, the script relaunches itself with elevation.
.PARAMETER Paths
One or more directory paths to delete (accepts pipeline input).
.PARAMETER LogFile
Optional path to write a log of all actions.
.PARAMETER WhatIf
Shows what would happen without making changes.
.PARAMETER Confirm
Prompts for confirmation before each deletion.
.EXAMPLE
.\ForceDelete.ps1 -Paths "D:\AAA","D:\BBB"
.EXAMPLE
Get-Content paths.txt | .\ForceDelete.ps1 -LogFile delete.log -WhatIf
#>

[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
    [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName)]
    [Alias('PSPath')]
    [string[]]$Paths,

    [string]$LogFile
)

begin {
    function Is-Admin {
        $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
        return $principal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
    }

    function Write-Log {
        param([string]$Message)
        Write-Host $Message
        if ($LogFile) {
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            Add-Content -Path $LogFile -Value "[$timestamp] $Message" -Encoding UTF8
        }
    }

    # Elevate if not admin
    if (-not (Is-Admin)) {
        $arg = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Paths " +
               ($Paths | ForEach-Object { "`"$($_)`"" } -join " ")
        if ($LogFile) { $arg += " -LogFile `"$LogFile`"" }
        if ($PSBoundParameters.ContainsKey('WhatIf')) { $arg += " -WhatIf" }
        if ($PSBoundParameters.ContainsKey('Confirm')) { $arg += " -Confirm" }
        Write-Host "Elevating script... You may see a UAC prompt." -ForegroundColor Yellow
        Start-Process -FilePath "powershell.exe" -ArgumentList $arg -Verb RunAs
        exit
    }
}

process {
    foreach ($p in $Paths) {
        if (Test-Path -LiteralPath $p) {
            Write-Log "Processing $p"

            if ($PSCmdlet.ShouldProcess($p, "Take ownership, grant control, delete")) {
                # Take ownership
                try { takeown.exe /F $p /R /D Y | Out-Null } catch { Write-Log "  takeown failed: $_" }

                # Grant full control
                try { icacls.exe $p /grant:r "*S-1-5-32-544:(F)" /T /C | Out-Null } catch { Write-Log "  icacls failed: $_" }

                # Clear attributes
                try { attrib -R -S -H $p /S /D | Out-Null } catch { Write-Log "  attrib failed: $_" }

                # Delete
                try {
                    Remove-Item -LiteralPath $p -Recurse -Force -ErrorAction Stop
                    Write-Log "  Deleted $p"
                } catch {
                    Write-Log "  Failed to delete $p : $_"
                }
            }
        } else {
            Write-Log "Path not found: $p"
        }
    }
}
